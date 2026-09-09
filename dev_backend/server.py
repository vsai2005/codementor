"""Zero-dependency DEV backend for CodeMentor AI (Windows-friendly).

Speaks the exact HTTP API the Next.js frontend expects (see frontend/lib/api.ts
and frontend/lib/types.ts), but with NO Postgres, NO pgvector and NO Docker. It
exists so the app can be clicked through on a Windows box with none of those
installed.

What is real here:
  * The 18 seed problems and 6 topics are loaded from the real backend seed.py.
  * "Run" / "Submit" actually execute your editor code against the real test
    cases in a subprocess (child_runner.py), so pass/fail is genuine.
  * overall_score uses the real weights + wrong-answer cap from schemas/review.py.
  * If GEMINI_API_KEY is set (dev_backend/.env), the review + tutor call Google
    Gemini for real; otherwise both fall back to a local heuristic.

What is faked:
  * Auth: any id_token logs you in as a single demo user (no Google).
  * Adaptive difficulty + progress are tracked in memory and reset on restart.

Run:  python dev_backend/server.py      (listens on http://localhost:8000)
"""

from __future__ import annotations

import ast
import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
SEED_PATH = os.path.join(HERE, "..", "backend", "app", "seed.py")
CHILD_RUNNER = os.path.join(HERE, "child_runner.py")

sys.path.insert(0, os.path.join(HERE, "..", "backend"))
try:
    from app.core.curriculum_map import CURRICULUM_DAY_PRACTICE, PRACTICE_SLUG_TO_DAYS
except Exception:
    CURRICULUM_DAY_PRACTICE = {}
    PRACTICE_SLUG_TO_DAYS = {}



def _load_env() -> None:
    """Minimal .env loader (stdlib only) — reads dev_backend/.env if present."""
    path = os.path.join(HERE, ".env")
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip())


_load_env()
# Hosts (Render/Fly/Railway) inject $PORT and expect the app to bind 0.0.0.0.
PORT = int(os.getenv("PORT") or os.getenv("DEV_BACKEND_PORT") or "8000")
HOST = os.getenv("HOST", "0.0.0.0")
IS_PRODUCTION = os.getenv("ENVIRONMENT", "").lower() in ("production", "prod")
NS = uuid.UUID("00000000-0000-0000-0000-0000000c0de0")  # stable namespace for ids

# --- scoring, copied verbatim from backend/app/schemas/review.py -----------
WEIGHTS = {"correctness": 0.40, "time_complexity": 0.25, "readability": 0.15,
           "edge_cases": 0.12, "space_complexity": 0.08}
WRONG_ANSWER_CAP = 50
TIER_LABELS = {1: "Easy", 2: "Easy-Medium", 3: "Medium", 4: "Medium-Hard", 5: "Hard"}


def compute_overall(scores: dict) -> int:
    weighted = sum(WEIGHTS[f] * scores[f] for f in WEIGHTS)
    overall = int(round(weighted))
    if scores["correctness"] < 100:
        overall = min(overall, WRONG_ANSWER_CAP)
    return max(0, min(100, overall))


# --- load the real seed data without importing the (Linux-only) backend ----
def _load_seed():
    with open(SEED_PATH, encoding="utf-8") as fh:
        src = fh.read()
    snippet = src[src.index("TOPICS = ["):src.index("def seed(")]
    ns: dict = {}
    exec(snippet, ns)  # defines P, TOPICS, PROBLEMS -- uses only builtins
    return ns["TOPICS"], ns["PROBLEMS"]


TOPICS_RAW, PROBLEMS_RAW = _load_seed()

TOPICS: dict[str, dict] = {}
for slug, name in TOPICS_RAW:
    TOPICS[slug] = {"id": str(uuid.uuid5(NS, "topic:" + slug)), "slug": slug, "name": name}

PROBLEMS: dict[str, dict] = {}  # id -> full problem
PROBLEM_ORDER: list[str] = []
for spec in PROBLEMS_RAW:
    pid = str(uuid.uuid5(NS, "problem:" + spec["slug"]))
    topic = TOPICS[spec["topic"]]
    PROBLEMS[pid] = {
        "id": pid,
        "slug": spec["slug"],
        "title": spec["title"],
        "difficulty_tier": spec["difficulty_tier"],
        "topic": topic,
        "topic_slug": spec["topic"],
        "statement_md": spec["statement_md"],
        "constraints_md": spec["constraints_md"],
        "optimal_time": spec["optimal_time"],
        "optimal_space": spec["optimal_space"],
        "entry_point": spec["entry_point"],
        "starter_code": spec["starter_code"],
        "test_cases": spec["test_cases"],
        "reference_solution": spec.get("reference_solution", ""),
    }
    PROBLEM_ORDER.append(pid)


def _find_problem(pid_or_slug: str | None) -> dict | None:
    if not pid_or_slug:
        return None
    if pid_or_slug in PROBLEMS:
        return PROBLEMS[pid_or_slug]
    for p in PROBLEMS.values():
        if p.get("slug") == pid_or_slug:
            return p
    return None



DEMO_USER = {
    "id": str(uuid.uuid5(NS, "user:demo")),
    "email": "demo@codementor.local",
    "name": "Demo User",
    "avatar_url": None,
}

# --- per-user state ---------------------------------------------------------
# Learning state (submissions, topic tiers, spaced-repetition schedule,
# misconceptions, XP/badges) lives in a PER-USER store, resolved from the
# request's auth token and reached via _S(). See the authentication section for
# _new_store()/_store_for(). Generated problems remain global (shared content).


def _summary(problem: dict) -> dict:
    return {"id": problem["id"], "slug": problem["slug"], "title": problem["title"],
            "difficulty_tier": problem["difficulty_tier"], "topic": problem["topic"],
            "generated": problem.get("generated", False)}


def _params(problem: dict) -> list[str]:
    """Parameter names of the entry function, read from the starter code."""
    starter = problem["starter_code"].get("python", "")
    m = re.search(r"def\s+%s\s*\(([^)]*)\)" % re.escape(problem["entry_point"]), starter)
    if not m:
        return []
    return [p.strip().split("=")[0].strip()
            for p in m.group(1).split(",") if p.strip()]


def _examples_md(problem: dict) -> str:
    """Worked examples generated from the first couple of real test cases."""
    cases = problem["test_cases"][:2]
    if not cases:
        return ""
    params = _params(problem)
    out = ["**Examples**", ""]
    for i, case in enumerate(cases, 1):
        args = case.get("args", [])
        if params and len(params) == len(args):
            inp = ", ".join(f"{p} = {json.dumps(a)}" for p, a in zip(params, args))
        else:
            inp = ", ".join(json.dumps(a) for a in args)
        out += [f"**Example {i}**",
                f"Input: `{inp}`",
                f"Output: `{json.dumps(case.get('expected'))}`",
                ""]
    return "\n".join(out).rstrip()


def _detail(problem: dict) -> dict:
    statement = problem["statement_md"]
    examples = _examples_md(problem)
    if examples:
        statement = f"{statement.rstrip()}\n\n{examples}"
    return {**_summary(problem),
            "statement_md": statement,
            "constraints_md": problem["constraints_md"],
            "optimal_time": problem["optimal_time"],
            "optimal_space": problem["optimal_space"],
            "entry_point": problem["entry_point"],
            "starter_code": problem["starter_code"],
            "concept": CONCEPT_LESSONS.get(problem["topic_slug"])}


# --- code execution --------------------------------------------------------
# --- sandbox hardening -----------------------------------------------------
# Defence in depth for letting strangers run code: the child runs with a
# scrubbed env (no API keys) + restricted builtins (child_runner.py); here we
# add a static AST gate that rejects the obvious attacks BEFORE anything runs.
_ALLOWED_IMPORT_ROOTS = {
    "math", "cmath", "collections", "itertools", "functools", "heapq", "bisect",
    "string", "re", "random", "statistics", "operator", "typing", "numbers",
    "fractions", "decimal", "datetime", "copy", "array", "enum", "dataclasses",
    "abc", "queue",
}
_BLOCKED_NAMES = {"eval", "exec", "compile", "open", "input", "__import__",
                  "globals", "vars", "breakpoint", "exit", "quit", "memoryview"}
_BLOCKED_ATTRS = {
    "__globals__", "__subclasses__", "__bases__", "__mro__", "__builtins__",
    "__import__", "__code__", "__closure__", "__func__", "__self__", "__dict__",
    "__getattribute__", "__reduce__", "__reduce_ex__", "__class__", "__base__",
    "__subclasshook__", "__init_subclass__",
}
MAX_CODE_CHARS = 20_000
# Only the vars Python itself needs to start — NONE of the app's secrets.
_SCRUBBED_ENV = {k: v for k, v in os.environ.items()
                 if k.upper() in ("SYSTEMROOT", "PATH", "PATHEXT", "TEMP", "TMP",
                                  "LD_LIBRARY_PATH", "LANG", "LC_ALL")}


def _code_security_error(code: str) -> str | None:
    """Reason string if the code is unsafe to run, else None. Runs in the
    trusted parent (not the sandbox): blocks disallowed imports, dangerous
    builtins, and the dunder attribute/string tricks used to escape."""
    if len(code) > MAX_CODE_CHARS:
        return "Code is too long."
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None  # reported later with a friendlier message
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] not in _ALLOWED_IMPORT_ROOTS:
                    return f"Import of '{alias.name}' isn't allowed in the sandbox."
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            if node.level or root not in _ALLOWED_IMPORT_ROOTS:
                return f"Import from '{node.module}' isn't allowed in the sandbox."
        elif isinstance(node, ast.Name) and node.id in _BLOCKED_NAMES:
            return f"Use of '{node.id}' isn't allowed in the sandbox."
        elif isinstance(node, ast.Attribute) and node.attr in _BLOCKED_ATTRS:
            return f"Access to '{node.attr}' isn't allowed in the sandbox."
        elif isinstance(node, ast.Constant) and isinstance(node.value, str) \
                and node.value in _BLOCKED_ATTRS:
            return "That string literal isn't allowed in the sandbox."
    return None


def _run_one(code: str, entry_point: str, args: list, expected, index: int) -> dict:
    started = time.perf_counter()
    job = json.dumps({"code": code, "entry_point": entry_point, "args": args})
    try:
        proc = subprocess.run([sys.executable, CHILD_RUNNER], input=job,
                              capture_output=True, text=True, timeout=6,
                              env=_SCRUBBED_ENV)
    except subprocess.TimeoutExpired:
        ms = int((time.perf_counter() - started) * 1000)
        return {"index": index, "passed": False, "status": "timeout", "runtime_ms": ms,
                "stdout": "", "stderr": "Time Limit Exceeded"}

    ms = int((time.perf_counter() - started) * 1000)
    try:
        payload = json.loads(proc.stdout)
    except (ValueError, TypeError):
        return {"index": index, "passed": False, "status": "error", "runtime_ms": ms,
                "stdout": "", "stderr": (proc.stderr or "no parseable output")[:2000]}

    status = payload.get("status")
    if status == "error":
        return {"index": index, "passed": False, "status": "error", "runtime_ms": ms,
                "stdout": payload.get("stdout", ""),
                "stderr": f"{payload.get('error_type')}: {payload.get('stderr', '')}"[:2000]}

    returned = payload.get("returned")
    passed = returned == expected
    result = {"index": index, "passed": passed,
              "status": "ok" if passed else "wrong_answer", "runtime_ms": ms,
              "stdout": payload.get("stdout", ""),
              "stderr": "" if passed else f"expected {expected!r}, got {returned!r}"}
    if not passed:
        # Structured expected/got so the UI can show a clean diff, not just a string.
        result["expected"] = repr(expected)
        result["got"] = repr(returned)
    return result


def run_tests(problem: dict, code: str) -> dict:
    reason = _code_security_error(code)
    if reason:
        total = len(problem["test_cases"])
        results = [{"index": i, "passed": False, "status": "error", "runtime_ms": 0,
                    "stdout": "", "stderr": f"Blocked for security: {reason}"}
                   for i in range(total)]
        out = {"passed": 0, "total": total, "all_passed": False, "results": results}
        out["diagnosis"] = diagnose(problem, out)
        return out
    results = [_run_one(code, problem["entry_point"], c.get("args", []),
                        c.get("expected"), i)
               for i, c in enumerate(problem["test_cases"])]
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    out = {"passed": passed, "total": total,
           "all_passed": total > 0 and passed == total, "results": results}
    # When something failed, attach a direct "what's wrong + how to fix/optimize"
    # explanation so the learner sees it immediately on Run, without submitting.
    out["diagnosis"] = diagnose(problem, out)
    return out


# --- heuristic review (stands in for the LLM) ------------------------------
# Ordered big-O ranks so detected vs optimal can be compared. Keys are the
# complexity strings after lowercasing and stripping spaces.
_CX_RANK = {
    "o(1)": 0, "o(logn)": 1, "o(log(m+n))": 1, "o(d)": 1,
    "o(n)": 2, "o(m+n)": 2, "o(min(n,m))": 2,
    "o(nlogn)": 3,
    "o(n^2)": 4, "o(m*n)": 4, "o(v+e)": 4,
    "o(n^3)": 5,
}


def _rank(cx: str) -> int:
    return _CX_RANK.get(cx.lower().replace(" ", ""), 2)  # unknown ~ linear


def _analyze_complexity(code: str, entry_point: str) -> dict:
    """Estimate time/space from the code's structure using the AST.

    Far more honest than counting `for` keywords: it measures real loop-nesting
    depth, treats comprehensions as loops, and spots sorting and recursion — so
    a one-liner like `return sorted(s) == sorted(t)` is O(n log n), not O(1).
    Still a heuristic, not a proof.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {"time": "O(n)", "space": "O(n)"}
    func = next((n for n in ast.walk(tree)
                 if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                 and n.name == entry_point), None)
    if func is None:
        return {"time": "O(n)", "space": "O(n)"}

    def depth(node: ast.AST, d: int = 0) -> int:
        best = d
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, (ast.For, ast.While, ast.AsyncFor)):
                best = max(best, depth(ch, d + 1))
            elif isinstance(ch, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                g = len(ch.generators)
                best = max(best, d + g, depth(ch, d + g))
            else:
                best = max(best, depth(ch, d))
        return best

    nd = depth(func)
    uses_sort = any(
        isinstance(n, ast.Call) and (
            (isinstance(n.func, ast.Name) and n.func.id == "sorted")
            or (isinstance(n.func, ast.Attribute) and n.func.attr == "sort"))
        for n in ast.walk(func))
    recursive = any(
        isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == entry_point
        for n in ast.walk(func))
    allocates = uses_sort or any(
        isinstance(n, (ast.ListComp, ast.SetComp, ast.DictComp, ast.List, ast.Dict, ast.Set))
        for n in ast.walk(func))

    if nd >= 3:
        time_c = "O(n^3)"
    elif nd == 2:
        time_c = "O(n^2)"
    elif nd == 1:
        time_c = "O(n log n)" if uses_sort else "O(n)"
    elif uses_sort:
        time_c = "O(n log n)"
    elif recursive:
        time_c = "O(n)"
    else:
        time_c = "O(1)"

    space_c = "O(n)" if (allocates or recursive) else "O(1)"
    return {"time": time_c, "space": space_c}


def _score_complexity(detected: str, optimal: str) -> int:
    d, o = _rank(detected), _rank(optimal)
    if d <= o:
        return 92
    if d <= o + 1:
        return 70
    return 48


def build_review(problem: dict, code: str, tests: dict) -> dict:
    total = tests["total"] or 1
    correctness = int(100 * tests["passed"] / total)
    detected = _analyze_complexity(code, problem["entry_point"])
    optimal = {"time": problem["optimal_time"], "space": problem["optimal_space"]}
    time_score = _score_complexity(detected["time"], optimal["time"])
    space_score = _score_complexity(detected["space"], optimal["space"])
    optimal_time = _rank(detected["time"]) <= _rank(optimal["time"])

    if correctness == 100:
        scores = {"correctness": 100,
                  "time_complexity": time_score,
                  "space_complexity": space_score,
                  "readability": 82 if len(code) < 600 else 68,
                  "edge_cases": 85}
        summary = ("All tests pass. "
                   + ("Complexity is at or below the optimal target — clean work."
                      if optimal_time
                      else f"Correct, but detected {detected['time']} vs optimal "
                           f"{optimal['time']} — there's a faster approach."))
        issues = []
        if not optimal_time:
            issues.append({"severity": "minor", "title": "Sub-optimal time complexity",
                           "detail": f"Estimated {detected['time']}; the optimal is "
                                     f"{optimal['time']}.", "line": None})
        hint = ("Clean, correct and optimal. Move up a tier." if optimal_time
                else "Solid — now tighten it toward the optimal complexity.")
        weak = [] if optimal_time else [problem["topic_slug"]]
    else:
        # Wrong answers: don't reward complexity that never produced right output.
        scores = {"correctness": correctness,
                  "time_complexity": min(time_score, 55),
                  "space_complexity": min(space_score, 55),
                  "readability": 60, "edge_cases": 35}
        summary = (f"{tests['passed']} of {tests['total']} tests pass. "
                   "Failing cases usually mean an unhandled edge case.")
        issues = [{"severity": "major", "title": "Failing tests",
                   "detail": f"{tests['total'] - tests['passed']} case(s) produced the "
                             "wrong output. Check empty inputs and boundaries.",
                   "line": None}]
        hint = "Re-check the failing cases — often it's the empty or single-element input."
        weak = [problem["topic_slug"]]

    # A solution that fails any test scores 0 overall — partial credit would
    # imply the code "mostly works", which is not how correctness is judged.
    overall = compute_overall(scores) if correctness == 100 else 0

    return {"overall_score": overall, "scores": scores,
            "detected_complexity": detected, "optimal_complexity": optimal,
            "summary": summary, "issues": issues, "improvement_hint": hint,
            "weak_topics": weak, "review_degraded": False}


# --- real LLM path (Google Gemini) -----------------------------------------
class LLMError(RuntimeError):
    pass


def _extract_json(raw: str) -> dict:
    text = raw.strip()
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fenced:
        text = fenced.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        return json.loads(text[start:end + 1])
    raise ValueError("no JSON object in model response")


class QuotaError(LLMError):
    """Raised when a provider is rate/quota/credit limited — triggers failover
    to the next provider and a cooldown so we stop hammering the dead one."""


# --- provider pool ---------------------------------------------------------
# Multiple back-ends tried in order. When one is quota-limited we fail over to
# the next and put the exhausted one on a short cooldown, so the learner never
# sees a failure unless EVERY provider is down at once. Configure via .env:
#   GEMINI_API_KEY=...            (+ optional GEMINI_API_KEYS=k1,k2 for a pool)
#   NVIDIA_API_KEY=...            (OpenAI-compatible, generous free tier)
#   XAI_API_KEY=...              (Grok; paid — auto-skipped if out of credit)
def _build_providers() -> list[dict]:
    provs: list[dict] = []
    nmodel = os.getenv("NVIDIA_MODEL", "nvidia/nemotron-3-super-120b-a12b").strip() or "nvidia/nemotron-3-super-120b-a12b"
    nbase = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1").strip() or "https://integrate.api.nvidia.com/v1"

    # 1. NVIDIA Tutor keys (5 keys dedicated to learning/teacher)
    raw_tutor = (os.getenv("NVIDIA_TUTOR_API_KEYS") or os.getenv("NVIDIA_TUTOR_API_KEY") or "").strip()
    tutor_keys = [k.strip() for k in raw_tutor.split(",") if k.strip()]
    for i, k in enumerate(tutor_keys, 1):
        provs.append({"name": f"nvidia-tutor-{i}", "kind": "openai", "role": "tutor",
                      "base": nbase, "key": k, "model": nmodel})

    # 2. NVIDIA Practice keys (2 keys dedicated to practice review/coach)
    raw_practice = (os.getenv("NVIDIA_PRACTICE_API_KEYS") or os.getenv("NVIDIA_PRACTICE_API_KEY") or "").strip()
    practice_keys = [k.strip() for k in raw_practice.split(",") if k.strip()]
    for i, k in enumerate(practice_keys, 1):
        provs.append({"name": f"nvidia-practice-{i}", "kind": "openai", "role": "practice",
                      "base": nbase, "key": k, "model": nmodel})

    # 3. General NVIDIA keys
    gen_keys = [k.strip() for k in os.getenv("NVIDIA_API_KEYS", "").split(",") if k.strip()]
    if os.getenv("NVIDIA_API_KEY", "").strip():
        k = os.getenv("NVIDIA_API_KEY").strip()
        if k not in gen_keys:
            gen_keys.append(k)

    for i, k in enumerate(gen_keys, 1):
        if k not in tutor_keys and k not in practice_keys:
            provs.append({"name": f"nvidia-{i}", "kind": "openai", "role": "general",
                          "base": nbase, "key": k, "model": nmodel})

    # Backup: Gemini
    gkeys: list[str] = []
    if os.getenv("GEMINI_API_KEY", "").strip():
        gkeys.append(os.getenv("GEMINI_API_KEY").strip())
    for k in os.getenv("GEMINI_API_KEYS", "").split(","):
        if k.strip() and k.strip() not in gkeys:
            gkeys.append(k.strip())
    gmodel = os.getenv("GEMINI_MODEL", "gemini-flash-latest").strip() or "gemini-flash-latest"
    for i, k in enumerate(gkeys):
        provs.append({"name": f"gemini-{i + 1}", "kind": "gemini", "role": "backup", "key": k, "model": gmodel})

    # Backup: xAI
    if os.getenv("XAI_API_KEY", "").strip():
        provs.append({"name": "xai", "kind": "openai", "role": "backup", "base": "https://api.x.ai/v1",
                      "key": os.getenv("XAI_API_KEY").strip(),
                      "model": os.getenv("XAI_MODEL", "grok-4-latest").strip() or "grok-4-latest"})
    return provs


PROVIDERS = _build_providers()
_COOLDOWN: dict[str, float] = {}       # provider name -> unix ts until skippable
QUOTA_COOLDOWN_S = 120                  # skip a quota-limited provider for 2 min
ERROR_COOLDOWN_S = 30                   # shorter cooldown for transient errors
LLM_ENABLED = bool(PROVIDERS)


def _is_quota(code: int, detail: str) -> bool:
    d = detail.lower()
    return code == 429 or (code == 403 and ("quota" in d or "credit" in d
                                            or "permission-denied" in d or "spending" in d or "rate limit" in d))


def _call_gemini(key: str, model: str, prompt: str, system: str, temperature: float,
                 max_tokens: int, want_json: bool, timeout: float) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    gen: dict = {"temperature": temperature, "maxOutputTokens": max_tokens}
    if want_json:
        gen["responseMimeType"] = "application/json"
    contents = []
    if system:
        contents.append({"role": "user", "parts": [{"text": f"[System Instructions]\n{system}\n\n[Task]\nBegin."}]})
    contents.append({"role": "user", "parts": [{"text": prompt}]})
    body = {"contents": contents, "generationConfig": gen}
    req = urllib.request.Request(f"{url}?key={key}", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read()[:400].decode("utf-8", "replace")
        raise (QuotaError if _is_quota(exc.code, detail) else LLMError)(
            f"HTTP {exc.code}: {detail}") from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise LLMError(str(exc)) from exc
    try:
        parts = data["candidates"][0]["content"]["parts"]
        return "".join(p.get("text", "") for p in parts)
    except (KeyError, IndexError):
        raise LLMError(f"unexpected response: {json.dumps(data)[:300]}")


def _call_openai(base: str, key: str, model: str, prompt: str, system: str,
                 temperature: float, max_tokens: int, want_json: bool, timeout: float) -> str:
    """OpenAI-compatible chat completions (NVIDIA NIM, xAI Grok, etc.)."""
    messages = ([{"role": "system", "content": system}] if system else []) \
        + [{"role": "user", "content": prompt}]
    body = {"model": model, "messages": messages, "temperature": temperature,
            "max_tokens": max_tokens}
    req = urllib.request.Request(
        base.rstrip("/") + "/chat/completions", data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read()[:400].decode("utf-8", "replace")
        raise (QuotaError if _is_quota(exc.code, detail) else LLMError)(
            f"HTTP {exc.code}: {detail}") from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise LLMError(str(exc)) from exc
    try:
        msg = data["choices"][0]["message"]
        content = msg.get("content") or msg.get("reasoning_content")
    except (KeyError, IndexError):
        raise LLMError(f"unexpected response: {json.dumps(data)[:300]}")
    if not content:
        raise LLMError("empty content from provider")
    return content


def _dispatch(p: dict, prompt: str, system: str, temperature: float,
              max_tokens: int, want_json: bool, timeout: float) -> str:
    if p["kind"] == "gemini":
        return _call_gemini(p["key"], p["model"], prompt, system, temperature,
                            max_tokens, want_json, timeout)
    return _call_openai(p["base"], p["key"], p["model"], prompt, system, temperature,
                        max_tokens, want_json, timeout)


def llm_complete(prompt: str, *, system: str = "", temperature: float = 0.2,
                 max_tokens: int = 1200, want_json: bool = False,
                 timeout: float = 8.0, purpose: str = "general") -> str:
    """Try each provider in order, prioritizing based on purpose (tutor vs practice),
    skipping any on cooldown, and seamlessly failing over if rate-limited."""
    global PROVIDERS
    if not PROVIDERS:
        PROVIDERS = _build_providers()
    if not PROVIDERS:
        raise LLMError("no LLM provider configured (set NVIDIA_TUTOR_API_KEYS / NVIDIA_PRACTICE_API_KEYS)")

    def _priority_score(p: dict) -> int:
        role = p.get("role", "general")
        if purpose == "tutor":
            if role == "tutor": return 0
            if role == "general": return 1
            if role == "practice": return 2
            return 3
        elif purpose == "practice":
            if role == "practice": return 0
            if role == "general": return 1
            if role == "tutor": return 2
            return 3
        else:
            if role in ("practice", "tutor", "general"): return 0
            return 1

    ordered = sorted(PROVIDERS, key=_priority_score)
    now = time.time()
    fresh = [p for p in ordered if _COOLDOWN.get(p["name"], 0) <= now]
    if not fresh:
        fresh = sorted(ordered, key=lambda p: _COOLDOWN.get(p["name"], 0))[:1]

    last_exc: Exception | None = None
    for p in fresh[:3]:
        try:
            text = _dispatch(p, prompt, system, temperature, max_tokens, want_json, timeout)
            _COOLDOWN.pop(p["name"], None)
            return text
        except QuotaError as exc:
            _COOLDOWN[p["name"]] = time.time() + QUOTA_COOLDOWN_S
            last_exc = exc
            sys.stderr.write(f"  dev-backend: LLM {p['name']} quota/rate-limited -> failing over to next key\n")
        except LLMError as exc:
            _COOLDOWN[p["name"]] = time.time() + ERROR_COOLDOWN_S
            last_exc = exc
            sys.stderr.write(f"  dev-backend: LLM {p['name']} error ({str(exc)[:70]}) -> failing over to next key\n")
        except Exception as exc:
            _COOLDOWN[p["name"]] = time.time() + ERROR_COOLDOWN_S
            last_exc = exc
            sys.stderr.write(f"  dev-backend: LLM {p['name']} unexpected ({str(exc)[:70]}) -> failing over\n")
    raise last_exc or LLMError("all LLM providers failed")


# Back-compat alias: existing call sites use gemini_complete(...).
gemini_complete = llm_complete

REVIEW_SYSTEM = """You are a senior software engineer reviewing a candidate's \
solution. Be precise, specific and terse. Never praise code you would not merge.

Return ONLY a single JSON object, no prose or markdown fences:
{
  "scores": {"time_complexity": int, "space_complexity": int,
             "readability": int, "edge_cases": int},
  "detected_complexity": {"time": str, "space": str},
  "summary": str,
  "issues": [{"severity": "minor"|"major"|"critical", "title": str,
              "detail": str, "line": int|null}],
  "improvement_hint": str,
  "weak_topics": [str]
}
All scores are 0-100. Do NOT return correctness or an overall score — the server
computes those from real test results. Judge complexity, readability and edge
cases only."""


def _review_prompt(problem: dict, code: str, tests: dict) -> str:
    lines = [f"# Problem: {problem['title']}", problem["statement_md"].strip(), "",
             f"Optimal complexity: time {problem['optimal_time']}, "
             f"space {problem['optimal_space']}", "",
             f"# Candidate submission (python)", "```python", code.strip(), "```", "",
             "# Test results (authoritative — real executions)",
             f"Passed {tests['passed']} of {tests['total']}."]
    for r in tests["results"]:
        verdict = "PASS" if r["passed"] else f"FAIL ({r['status']})"
        lines.append(f"  case {r['index']}: {verdict} in {r['runtime_ms']}ms")
    lines += ["", "Review the code for time/space complexity, readability and "
              "edge-case handling. Return the JSON object only."]
    return "\n".join(lines)


def build_review_llm(problem: dict, code: str, tests: dict) -> dict:
    """LLM review via NVIDIA Nemotron / Gemini. Correctness stays test-driven; wrong answer -> 0."""
    raw = gemini_complete(_review_prompt(problem, code, tests),
                          system=REVIEW_SYSTEM, temperature=0.2, want_json=True,
                          timeout=20.0, purpose="practice")
    draft = _extract_json(raw)

    total = tests["total"] or 1
    correctness = int(100 * tests["passed"] / total)
    ds = draft.get("scores", {})

    def clamp(v, default):
        try:
            return max(0, min(100, int(v)))
        except (TypeError, ValueError):
            return default

    scores = {"correctness": correctness,
              "time_complexity": clamp(ds.get("time_complexity"), 60),
              "space_complexity": clamp(ds.get("space_complexity"), 60),
              "readability": clamp(ds.get("readability"), 70),
              "edge_cases": clamp(ds.get("edge_cases"), 60)}
    if correctness < 100:  # never reward complexity that produced wrong output
        scores["time_complexity"] = min(scores["time_complexity"], 55)
        scores["space_complexity"] = min(scores["space_complexity"], 55)

    detected = draft.get("detected_complexity") or _analyze_complexity(code, problem["entry_point"])
    detected = {"time": str(detected.get("time", "?")), "space": str(detected.get("space", "?"))}
    optimal = {"time": problem["optimal_time"], "space": problem["optimal_space"]}

    issues = []
    for it in draft.get("issues", [])[:6]:
        sev = it.get("severity")
        issues.append({"severity": sev if sev in ("minor", "major", "critical") else "minor",
                       "title": str(it.get("title", "Issue"))[:120],
                       "detail": str(it.get("detail", ""))[:500],
                       "line": it.get("line") if isinstance(it.get("line"), int) else None})

    overall = compute_overall(scores) if correctness == 100 else 0
    return {"overall_score": overall, "scores": scores,
            "detected_complexity": detected, "optimal_complexity": optimal,
            "summary": str(draft.get("summary", ""))[:800] or "Review complete.",
            "issues": issues,
            "improvement_hint": str(draft.get("improvement_hint", ""))[:400]
                                or "Keep practising.",
            "weak_topics": [str(t)[:40] for t in draft.get("weak_topics", [])][:5],
            "review_degraded": False}


def review_submission(problem: dict, code: str, tests: dict) -> dict:
    """Prefer the Gemini review; fall back to the heuristic if it fails."""
    if LLM_ENABLED:
        try:
            return build_review_llm(problem, code, tests)
        except (LLMError, ValueError, KeyError, TypeError) as exc:
            sys.stderr.write(f"  dev-backend: LLM review failed ({exc}); using heuristic\n")
    return build_review(problem, code, tests)


# --- AI tutor / coach (grounded in the learner's own code) -----------------
TUTOR_SYSTEM = """You are a warm, encouraging coding tutor helping a student who \
is actively solving a practice problem. They can SEE their own code — you are \
looking at it too.

Rules:
- Give HINTS and nudges, never the full solution. Guide them to the insight.
- Be specific: refer to their actual variables, lines, and logic.
- If they ask "what's wrong", point at the concrete bug or missing edge case
  without writing the fix for them.
- Keep it short (2-5 sentences). Warm, human, motivating. Short code snippets
  only when a single line clarifies an idea — never a complete answer."""

COACH_SYSTEM = """You are an inspiring senior engineer giving a student a \
post-submission debrief. Your job is to make them feel genuinely proud AND leave \
them smarter.

Structure your reply as warm flowing prose (no JSON, no headings):
1. Open with sincere, specific praise — name what they actually did well ("your
   brilliant use of a hash map here…"). Be generous but honest.
2. Then, gently, show exactly WHERE their logic can improve or where they can
   squeeze more out of the output — the one or two highest-leverage changes.
3. Close with a one-line motivating push forward.

If the student shared a PLAN (the approach they wrote down BEFORE coding), add
one sentence noting whether their code followed their plan and whether that plan
was aimed at the optimal approach — reward good planning, and if the plan drifted
from the code or missed the key insight, name that kindly.

Tone: brilliant mentor who believes in them. 4-7 sentences. Never condescending,
never generic."""


def _code_context(problem: dict, code: str) -> str:
    return "\n".join([
        f"# Problem: {problem['title']}",
        problem["statement_md"].strip(),
        "",
        f"Optimal complexity: time {problem['optimal_time']}, "
        f"space {problem['optimal_space']}",
        "",
        "# The student's current code (python):",
        "```python",
        (code or "").strip() or "(the editor is empty)",
        "```",
    ])


def tutor_reply(problem: dict | None, code: str, message: str) -> str:
    """Hint-style tutor answer, grounded in the student's live code."""
    if problem is not None:
        prompt = (_code_context(problem, code) + "\n\n# The student asks:\n"
                  + message + "\n\nGive a helpful hint (not the full solution).")
    else:
        prompt = message
    return gemini_complete(prompt, system=TUTOR_SYSTEM,
                           temperature=0.5, max_tokens=600, timeout=15.0, purpose="practice").strip()


def coach_debrief(problem: dict, code: str, review: dict, tests: dict,
                  plan: str = "") -> str:
    """Warm, praise-forward post-submit debrief with where-to-improve guidance."""
    passed = f"{tests.get('passed', 0)} of {tests.get('total', 0)} tests pass"
    lines = [_code_context(problem, code), ""]
    if plan.strip():
        lines += ["# The plan they wrote BEFORE coding:", plan.strip(), ""]
    lines += [
        "# Result of their submission:",
        f"- {passed}",
        f"- Overall score: {review.get('overall_score', 0)}/100",
        f"- Detected complexity: time {review.get('detected_complexity', {}).get('time', '?')}, "
        f"space {review.get('detected_complexity', {}).get('space', '?')}",
        f"- Summary: {review.get('summary', '')}",
        "",
        "Write their debrief now — praise them for real, then show where their "
        "logic can level up or where they can maximise the output.",
    ]
    return gemini_complete("\n".join(lines), system=COACH_SYSTEM,
                           temperature=0.6, max_tokens=700, timeout=15.0, purpose="practice").strip()


def _coach_fallback(review: dict, tests: dict, plan: str = "") -> str:
    """Heuristic praise + guidance when no LLM key is configured."""
    plan_note = ""
    if plan.strip():
        plan_note = (" And credit where it's due — you wrote a plan before coding, "
                     "which is exactly how strong engineers work: think first, then type.")
    all_passed = tests.get("passed", 0) == tests.get("total", 0) and tests.get("total", 0) > 0
    if all_passed:
        det = review.get("detected_complexity", {}).get("time", "?")
        opt = review.get("optimal_complexity", {}).get("time", "?")
        praise = ("Brilliant — every single test passes. That's real problem-solving: "
                  "you held the whole shape of the problem in your head and made it work.")
        if det != opt:
            improve = (f"Now the exciting part: your solution runs at {det}, and the "
                       f"optimal is {opt}. Look for repeated work you can cache or a "
                       "nested loop you can flatten with a hash map or two pointers — "
                       "that's where you unlock the next tier.")
        else:
            improve = ("And you hit the optimal complexity too — nothing to squeeze, "
                       "so push yourself on readability and naming so the next reader "
                       "(future you) reads it like a sentence.")
        return (f"{praise} {improve}{plan_note} "
                "You're clearly ready for harder problems — keep going. 🚀")
    return ("Genuinely good effort — you got a working structure down, and that's the "
            "hardest first step. " + review.get("improvement_hint", "")
            + " Focus on the failing case, especially empty or single-element input; "
            "fix that one thing and this clicks into place." + plan_note
            + " You're closer than it feels. 💪")


class DevBackendLLMClient:
    def complete(self, prompt: str, system: str = "", temperature: float = 0.35,
                 max_tokens: int = 450, timeout: float = 8.0) -> str:
        return gemini_complete(prompt, system=system, temperature=temperature,
                               max_tokens=max_tokens, timeout=timeout, purpose="tutor")


_dev_teacher_svc = None


def get_dev_teacher_svc():
    global _dev_teacher_svc
    if _dev_teacher_svc is None:
        try:
            from app.services.teacher import AITeacherService
            client = DevBackendLLMClient() if LLM_ENABLED else None
            _dev_teacher_svc = AITeacherService(client=client)
        except Exception as _e:
            sys.stderr.write(f"  dev-backend: could not load AITeacherService: {_e}\n")
    return _dev_teacher_svc


# --- adaptive difficulty (simplified) --------------------------------------
def apply_difficulty(topic_slug: str, score: int) -> dict:
    st = _S()["topic_state"].setdefault(
        topic_slug, {"tier": 1, "scores": [], "attempts": 0, "avg": 0.0, "last": None})
    st["scores"].insert(0, score)
    st["attempts"] += 1
    st["avg"] = round(sum(st["scores"]) / len(st["scores"]), 2)
    st["last"] = datetime.now(timezone.utc).isoformat()

    window = st["scores"][:3]
    if len(window) < 3:
        rolling = round(sum(window) / len(window), 4)
    else:
        rolling = round(0.5 * window[0] + 0.3 * window[1] + 0.2 * window[2], 4)

    tier_from = st["tier"]
    tier_to = tier_from
    direction = "hold"
    if rolling >= 80 and len(window) >= 3 and tier_from < 5:
        tier_to = tier_from + 1
        direction = "promote"
    elif rolling < 50 and tier_from > 1:
        tier_to = tier_from - 1
        direction = "demote"
    st["tier"] = tier_to

    label = TIER_LABELS[tier_to]
    s = int(round(rolling))
    if direction == "promote":
        banner = f"Score {s} → next problem moves up to {label}"
    elif direction == "demote":
        banner = f"Score {s} → next problem eases to {label}"
    else:
        banner = f"Score {s} → next problem stays at {label}"
    return {"from": tier_from, "to": tier_to, "rolling_score": rolling, "banner": banner}


def _mastery(avg: float, attempts: int) -> str:
    if attempts < 3:
        return "learning" if avg >= 50 else "weak"
    if avg >= 80:
        return "strong"
    if avg >= 50:
        return "learning"
    return "weak"


def progress_topics() -> dict:
    out = []
    topic_state = _S()["topic_state"]
    for slug, topic in TOPICS.items():
        st = topic_state.get(slug)
        if st:
            out.append({"topic": topic, "current_tier": st["tier"],
                        "attempts": st["attempts"], "avg_score": st["avg"],
                        "mastery": _mastery(st["avg"], st["attempts"]),
                        "last_practiced_at": st["last"]})
        else:
            out.append({"topic": topic, "current_tier": 1, "attempts": 0,
                        "avg_score": 0.0, "mastery": "weak", "last_practiced_at": None})
    return {"topics": out}


def next_problem() -> dict:
    """Highest-priority topic (weakest / least practiced), at its tier."""
    topic_state = _S()["topic_state"]
    last_pid = _S()["last_submitted"]["pid"]
    def priority(slug):
        st = topic_state.get(slug)
        if not st:
            return (1.0,)  # never practiced -> top priority
        return (1.0 - st["avg"] / 100.0,)
    ranked = sorted(TOPICS, key=priority, reverse=True)
    fallback = None
    for slug in ranked:
        tier = topic_state.get(slug, {}).get("tier", 1)
        for cand in (tier, tier - 1, tier + 1, tier - 2, tier + 2, tier - 3, tier + 3):
            if 1 <= cand <= 5:
                for pid in PROBLEM_ORDER:
                    p = PROBLEMS[pid]
                    if p["topic_slug"] == slug and p["difficulty_tier"] == cand:
                        if pid == last_pid:
                            fallback = fallback or p
                            continue
                        return p
    return fallback or PROBLEMS[PROBLEM_ORDER[0]]


# --- spaced repetition (SM-2, simplified) ----------------------------------
# Retention comes from re-retrieving a solved problem just before you'd forget
# it. After each *passing* submission we schedule the next review with an
# SM-2-style expanding interval; a weak/failed solve resets the interval so it
# comes back soon. State is in-memory and resets on restart (like the rest of
# this dev backend), so within a session you'll see the SCHEDULE build up under
# "upcoming" even though nothing is literally past-due yet.
def _quality(score: int, all_passed: bool) -> int:
    """Map an outcome to SM-2 recall quality 0-5."""
    if not all_passed:
        return 2
    if score >= 95:
        return 5
    if score >= 85:
        return 4
    return 3


def schedule_review(problem: dict, review: dict, all_passed: bool) -> dict:
    review_state = _S()["review_state"]
    pid = problem["id"]
    st = review_state.get(pid, {"ease": 2.5, "interval": 0, "reps": 0})
    q = _quality(review.get("overall_score", 0), all_passed)

    if q < 3:  # failed recall — relearn from the start, revisit tomorrow
        st["reps"] = 0
        st["interval"] = 1
    else:
        st["reps"] += 1
        if st["reps"] == 1:
            st["interval"] = 1
        elif st["reps"] == 2:
            st["interval"] = 3
        else:
            # Clamp AT the multiply so the value is never stored unbounded —
            # even if a concurrent same-user submit races on this shared dict.
            st["interval"] = max(1, min(365, round(st["interval"] * st["ease"])))
        # SM-2 ease adjustment; floor 1.3, CAP 3.0 so `ease` can't run away and
        # blow up the interval on the next solve.
        st["ease"] = max(1.3, min(3.0, st["ease"] + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))))
        st["ease"] = round(st["ease"], 3)

    # Final guard: interval is always a sane int (also covers the q<3 branch),
    # so timedelta can never overflow no matter how the writes interleave.
    st["interval"] = max(1, min(365, int(st["interval"])))
    due = datetime.now(timezone.utc) + timedelta(days=st["interval"])
    st["due_at"] = due.isoformat()
    st["last_score"] = review.get("overall_score", 0)
    st["title"] = problem["title"]
    review_state[pid] = st
    return {"interval_days": st["interval"], "due_at": st["due_at"],
            "reps": st["reps"], "ease": st["ease"]}


def _due_item(pid: str, st: dict) -> dict:
    now = datetime.now(timezone.utc)
    try:
        due_dt = datetime.fromisoformat(st["due_at"])
    except (KeyError, ValueError):
        due_dt = now
    days = (due_dt - now).total_seconds() / 86400.0
    return {**_summary(PROBLEMS[pid]),
            "due_at": st.get("due_at"),
            "last_score": st.get("last_score"),
            "reps": st.get("reps", 0),
            "due_in_days": max(0, round(days))}


def review_queue() -> dict:
    review_state = _S()["review_state"]
    now = datetime.now(timezone.utc)
    due, upcoming = [], []
    for pid, st in review_state.items():
        if pid not in PROBLEMS:
            continue
        item = _due_item(pid, st)
        try:
            is_due = datetime.fromisoformat(st["due_at"]) <= now
        except (KeyError, ValueError):
            is_due = True
        (due if is_due else upcoming).append(item)
    due.sort(key=lambda x: x.get("due_at") or "")
    upcoming.sort(key=lambda x: x.get("due_at") or "")
    return {"due": due, "upcoming": upcoming,
            "due_count": len(due), "tracked_count": len(review_state)}


def recent_solved(limit: int = 5) -> dict:
    """The learner's most recently solved problems, newest first.

    `stats["solved"]` is appended to in first-solve order, so the tail is the
    most recent. Problems that no longer exist (e.g. a generated one lost on
    restart) are skipped rather than shown as broken links."""
    solved = _S()["stats"]["solved"]
    items = []
    for pid in reversed(solved):
        problem = PROBLEMS.get(pid)
        if not problem:
            continue
        items.append({"id": pid, "title": problem["title"],
                      "topic": problem["topic"]})
        if len(items) >= limit:
            break
    return {"items": items, "solved_count": len(solved)}


def account_summary() -> dict:
    """Headline numbers for the profile's Account box: how many problems this
    learner has solved, how many exist in total, and their average score across
    every submission."""
    stats = _S()["stats"]
    subs = _S()["submissions"]
    scores = [s["overall_score"] for s in subs
              if isinstance(s.get("overall_score"), (int, float))]
    avg = round(sum(scores) / len(scores)) if scores else 0
    return {"solved_count": len(stats["solved"]),
            "total_problems": len(PROBLEMS),
            "avg_score": avg,
            "attempts": len(subs)}


# --- misconception tracking ------------------------------------------------
# A wrong submission is a signal, not just a zero. We classify *why* it failed
# and accumulate the pattern so the learner can see their recurring blind spots.
MISCONCEPTION_INFO = {
    "edge-cases": {
        "label": "Edge cases (empty / boundary inputs)",
        "tip": "Before submitting, dry-run your code on the empty input, a single "
               "element, and the largest boundary — that's where most fails hide."},
    "efficiency": {
        "label": "Efficiency (too slow / timed out)",
        "tip": "Hunt for a nested loop you can replace with a hash map, two pointers, "
               "or a sort — that usually drops you a whole complexity tier."},
    "runtime-error": {
        "label": "Runtime errors (crashes)",
        "tip": "Guard against index-out-of-range and None before you touch a value; "
               "read the error type printed on the failing case."},
    "logic": {
        "label": "Core logic (wrong output)",
        "tip": "Re-read the statement, then trace one failing example by hand — the "
               "bug is usually a flipped condition or an off-by-one."},
}


def _is_boundary(args: list) -> bool:
    for a in args:
        if a is None:
            return True
        if isinstance(a, (list, str, dict)) and len(a) <= 1:
            return True
        if isinstance(a, bool):
            continue
        if isinstance(a, (int, float)) and a == 0:
            return True
    return False


def _classify_misconception(problem: dict, tests: dict) -> str | None:
    if tests.get("all_passed"):
        return None
    failed = [r for r in tests.get("results", []) if not r.get("passed")]
    if not failed:
        return None
    statuses = {r.get("status") for r in failed}
    if "timeout" in statuses:
        return "efficiency"
    if "error" in statuses:
        return "runtime-error"
    cases = problem["test_cases"]
    for r in failed:
        idx = r.get("index")
        if isinstance(idx, int) and 0 <= idx < len(cases):
            if _is_boundary(cases[idx].get("args", [])):
                return "edge-cases"
    return "logic"


# Per-topic hint for "how to optimize more" — surfaced on Run so the learner
# gets a concrete direction, not just a pass/fail count.
OPTIMIZE_HINTS = {
    "arrays": "Try a single pass with a hash map / set or a running aggregate — "
              "that usually replaces a nested loop and drops you a complexity tier.",
    "two-pointers": "Two pointers (both ends, or fast/slow) often removes the "
                    "inner loop and turns O(n^2) into O(n).",
    "strings": "Count characters once with a dict / Counter instead of "
               "re-scanning the string for each character.",
    "stacks": "A stack lets you process each element exactly once (O(n)) instead "
              "of repeatedly re-scanning what came before.",
    "binary-search": "Halve the search space each step for O(log n) — look for a "
                     "monotonic property you can binary-search on.",
    "graphs": "Visit each node and edge once with BFS/DFS and a visited set — "
              "O(V+E). Re-exploring visited nodes is the usual slowdown.",
    "python-basics": "Use built-in functions, list comprehensions, and idiomatic Python features to keep logic concise and fast.",
    "linked-lists": "Use a dummy head node to simplify edge cases and avoid special-casing empty lists or head modifications.",
    "trees": "Recurse on subtrees with base cases for None nodes, or use level-order BFS with a deque for layered traversal.",
    "heaps": "Use heapq to maintain only the top K elements in O(N log K) instead of sorting the whole collection in O(N log N).",
    "searching-sorting": "Look for sorted order or binary search opportunities; sort once upfront if multiple queries are needed.",
    "hashing": "Track seen values or cumulative prefix sums in a hash map for O(1) instant lookups.",
    "greedy": "Sort by key criteria (like intervals by finish time) and make the best local choice without looking back.",
    "dynamic-programming": "Identify overlapping subproblems and state transitions; compress 2D DP arrays to 1D if only the previous row is needed.",
    "bit-manipulation": "Use bitwise XOR to cancel pairs, or n & (n - 1) to clear the lowest set bit in O(number of set bits).",
    "advanced-dsa": "Choose the optimal specialized data structure (Trie for prefixes, DSU for connectivity, Segment Tree for range queries).",
}


def _format_call(problem: dict, args: list) -> str:
    """Render a failing case as a readable call, e.g. two_sum(nums=[2,7], target=9)."""
    names = _params(problem)
    parts = []
    for i, a in enumerate(args):
        val = repr(a)
        if len(val) > 80:
            val = val[:77] + "..."
        parts.append(f"{names[i]}={val}" if i < len(names) else val)
    return f"{problem['entry_point']}({', '.join(parts)})"


def diagnose(problem: dict, tests: dict) -> dict | None:
    """Direct, learner-facing explanation of a failing Run: what's wrong, which
    case, and how to fix / optimize. Returns None when everything passed."""
    if tests.get("all_passed"):
        return None
    failed = [r for r in tests.get("results", []) if not r.get("passed")]
    if not failed:
        return None

    category = _classify_misconception(problem, tests) or "logic"
    info = MISCONCEPTION_INFO.get(category, MISCONCEPTION_INFO["logic"])
    first = failed[0]
    cases = problem["test_cases"]
    idx = first.get("index")
    case = cases[idx] if isinstance(idx, int) and 0 <= idx < len(cases) else None

    # Build the "what's wrong" line, concrete to the first failing case.
    first_failure = None
    if case is not None:
        call = _format_call(problem, case.get("args", []))
        if first.get("status") == "wrong_answer":
            summary = (f"Your code returned the wrong answer on case {idx + 1}. "
                       f"For {call} it should return {first.get('expected')}, "
                       f"but you returned {first.get('got')}.")
            first_failure = {"case": idx + 1, "call": call,
                             "expected": first.get("expected"),
                             "got": first.get("got")}
        elif first.get("status") == "timeout":
            summary = (f"Case {idx + 1} ({call}) ran too long and was stopped — "
                       "your solution is correct in spirit but too slow.")
            first_failure = {"case": idx + 1, "call": call,
                             "expected": None, "got": "Time Limit Exceeded"}
        else:  # error / security
            summary = (f"Your code crashed on case {idx + 1} ({call}): "
                       f"{first.get('stderr', '').strip()[:200]}")
            first_failure = {"case": idx + 1, "call": call,
                             "expected": None, "got": first.get("stderr", "")[:200]}
    else:
        summary = f"{len(failed)} case(s) did not pass."

    optimize = (f"Target complexity for this problem is time {problem['optimal_time']}, "
                f"space {problem['optimal_space']}. "
                + OPTIMIZE_HINTS.get(problem["topic_slug"], ""))

    return {
        "category": category,
        "title": info["label"],
        "summary": summary,
        "first_failure": first_failure,
        "failed_count": len(failed),
        "fix": info["tip"],
        "optimize": optimize.strip(),
    }


def record_misconception(problem: dict, tests: dict) -> dict | None:
    tag = _classify_misconception(problem, tests)
    if not tag:
        return None
    st = _S()["misconceptions"].setdefault(tag, {"count": 0, "last_at": None, "problems": []})
    st["count"] += 1
    st["last_at"] = datetime.now(timezone.utc).isoformat()
    title = problem["title"]
    st["problems"] = ([title] + [p for p in st["problems"] if p != title])[:5]
    info = MISCONCEPTION_INFO[tag]
    return {"tag": tag, "label": info["label"], "tip": info["tip"], "count": st["count"]}


def misconceptions_summary() -> dict:
    items = []
    for tag, st in _S()["misconceptions"].items():
        info = MISCONCEPTION_INFO.get(tag, {"label": tag, "tip": ""})
        items.append({"tag": tag, "label": info["label"], "tip": info["tip"],
                      "count": st["count"], "last_at": st["last_at"],
                      "problems": st["problems"]})
    items.sort(key=lambda x: x["count"], reverse=True)
    return {"items": items, "total": sum(i["count"] for i in items)}


# --- concept mini-lessons --------------------------------------------------
# The connective tissue that makes patterns transfer: each topic gets a short
# "why this pattern exists" explainer + a worked example. Attached to every
# problem's detail payload via _detail() so it shows right beside the statement.
CONCEPT_LESSONS = {
    "arrays": {
        "pattern": "Hash Map (Arrays & Hashing)",
        "summary": "Trade space for time: store what you've seen in a set or dict so "
                   "each lookup is O(1). It turns a nested O(n^2) scan into one O(n) pass.",
        "when_to_use": "You're asking \"have I seen this value / its complement before?\" "
                       "— duplicates, pair sums, grouping, counting frequencies.",
        "worked_example": "Two Sum: walk the array once, and for each x check if "
                          "`target - x` is already in a dict of value→index. If yes you're "
                          "done; otherwise store x. One pass, O(n) time, O(n) space.",
    },
    "two-pointers": {
        "pattern": "Two Pointers",
        "summary": "Two indices moving through the data (from both ends, or fast/slow) "
                   "let you scan in O(n) without a nested loop — usually on sorted input.",
        "when_to_use": "Sorted arrays, palindrome checks, pair/triplet targets, or "
                       "in-place partitioning where you shrink a window from both sides.",
        "worked_example": "Pair sum in a sorted array: put `lo` at the start, `hi` at the "
                          "end. If `nums[lo]+nums[hi]` is too big, move `hi` left; too "
                          "small, move `lo` right. Each step discards an impossible half.",
    },
    "strings": {
        "pattern": "Strings (frequency & sliding window)",
        "summary": "Most string problems reduce to counting characters or sliding a "
                   "window. A 26-slot count array or a dict is your workhorse.",
        "when_to_use": "Anagrams, substring searches, \"longest/shortest window with X\", "
                       "or anything comparing character composition.",
        "worked_example": "Valid Anagram: two strings are anagrams iff their character "
                          "counts match. Tally counts for the first, subtract for the "
                          "second, and every bucket must land back at zero — O(n).",
    },
    "stacks": {
        "pattern": "Stacks & Queues",
        "summary": "A stack remembers the most recent unresolved thing (LIFO) — perfect "
                   "for matching, nesting and \"undo the last\" logic. A queue is FIFO.",
        "when_to_use": "Balanced brackets, evaluating expressions, next-greater-element, "
                       "or any place you must pair an item with a later/earlier partner.",
        "worked_example": "Valid Parentheses: push every opening bracket; on a closing "
                          "bracket, the top of the stack must be its match — pop it. Empty "
                          "stack at the end means every bracket was paired. O(n).",
    },
    "binary-search": {
        "pattern": "Binary Search",
        "summary": "Halve the search space each step: O(log n). Works on any sorted range "
                   "— or on an answer space where a predicate flips from false to true.",
        "when_to_use": "Sorted lookups, first/last position, or \"smallest value that "
                       "satisfies a condition\" (binary-search-on-answer).",
        "worked_example": "Search a sorted array: compare the target to the midpoint; if "
                          "smaller, discard the right half, else the left. Keep the "
                          "`lo <= hi` invariant tight to avoid an infinite loop.",
    },
    "graphs": {
        "pattern": "Graphs & Trees (BFS / DFS)",
        "summary": "Model the problem as nodes + edges, then traverse: BFS (queue) for "
                   "shortest hops, DFS (stack/recursion) for reachability and structure.",
        "when_to_use": "Connectivity, shortest path in an unweighted grid, cycle "
                       "detection, or exploring every reachable state.",
        "worked_example": "Number of Islands: scan the grid; each unvisited land cell "
                          "starts a DFS/BFS that floods its whole island, marking cells "
                          "visited. Count how many floods you launch. O(rows × cols).",
    },
    "python-basics": {
        "pattern": "Idiomatic Python Foundations",
        "summary": "Leverage Python's expressive syntax, data structures, and built-ins to write "
                   "clean, maintainable, and bug-free code.",
        "when_to_use": "Basic algorithmic challenges, formatting, string manipulation, condition "
                       "branching, loops, and math operations.",
        "worked_example": "Celsius to Fahrenheit: apply formula celsius * 9 / 5 + 32 directly, "
                          "leveraging Python's arbitrary-precision integers and floating-point math.",
    },
    "linked-lists": {
        "pattern": "Pointer Manipulation & Sentinel Nodes",
        "summary": "Maintain pointers (head, prev, curr, next) to traverse and restructure node "
                   "connections in O(1) auxiliary space.",
        "when_to_use": "Reversing lists, merging sorted chains, cycle detection with fast/slow "
                       "pointers, or reordering nodes.",
        "worked_example": "Reverse Linked List: initialize prev = None, then iterate updating "
                          "next_node = curr.next, curr.next = prev, prev = curr, curr = next_node.",
    },
    "trees": {
        "pattern": "Tree Traversal & Divide-and-Conquer",
        "summary": "Break tree problems down into recursive subproblems on the left and right "
                   "subtrees, or traverse level-by-level with a queue.",
        "when_to_use": "Hierarchical relationships, binary search trees, finding max depth, "
                       "validating BST invariants, or computing paths.",
        "worked_example": "Maximum Depth of Binary Tree: compute 1 + max(max_depth(root.left), "
                          "max_depth(root.right)) with base case 0 when root is None.",
    },
    "heaps": {
        "pattern": "Priority Queue / Min-Heap & Max-Heap",
        "summary": "Keep track of the minimum or maximum element dynamically in O(log k) time "
                   "using a binary heap (heapq in Python).",
        "when_to_use": "Finding the Top K elements, merging K sorted streams, continuous median "
                       "tracking, or task scheduling.",
        "worked_example": "Kth Largest Element: maintain a min-heap of size K containing the "
                          "largest elements seen so far; the heap top is the Kth largest in O(N log K).",
    },
    "searching-sorting": {
        "pattern": "Divide & Conquer, Invariants & Sorting",
        "summary": "Order elements systematically (O(N log N) with merge sort, quicksort, or Timsort) "
                   "to unlock binary search and two-pointer efficiencies.",
        "when_to_use": "Ranking elements, interval intersections, grouping equal values, or "
                       "searching in rotated/sorted arrays.",
        "worked_example": "Merge Intervals: sort intervals by start time, then merge overlapping "
                          "adjacent pairs linearly in O(N log N) total time.",
    },
    "hashing": {
        "pattern": "Frequency Maps & Hash Tables",
        "summary": "Use hash maps (dict, Counter) and hash sets for O(1) average lookup, insertion, "
                   "and deletion.",
        "when_to_use": "Frequency counting, anagram grouping, subarray sum equals K (prefix sum + "
                       "hash map), and distinct element tracking.",
        "worked_example": "Subarray Sum Equals K: store prefix sum frequencies in a hash map; for "
                          "current sum s, add count of s - k to the total in O(N).",
    },
    "greedy": {
        "pattern": "Locally Optimal Choice",
        "summary": "Make the locally optimal decision at each step that leads to a globally optimal "
                   "outcome, often relying on sorted input.",
        "when_to_use": "Interval scheduling, activity selection, coin change (canonical denominations), "
                       "and fractional knapsack.",
        "worked_example": "Non-overlapping Intervals: sort intervals by end time and greedily keep "
                          "the interval that finishes earliest, maximizing remaining room.",
    },
    "dynamic-programming": {
        "pattern": "Optimal Substructure & Overlapping Subproblems",
        "summary": "Break complex decisions into simpler sub-decisions, memoizing intermediate states "
                   "(memoization or tabulation) to prevent redundant work.",
        "when_to_use": "Counting paths, min/max cost optimizations, knapsack variations, longest common "
                       "subsequence, and game theory.",
        "worked_example": "Coin Change: define dp[i] as min coins needed for amount i. Compute "
                          "dp[i] = min(dp[i - c] + 1) across all coins c.",
    },
    "bit-manipulation": {
        "pattern": "Bitwise Logic & Bitmasks",
        "summary": "Operate directly on binary bits using AND, OR, XOR, NOT, and bit shifts for "
                   "ultra-compact state and constant-time operations.",
        "when_to_use": "Single number identification, subset enumeration, power-of-two tests "
                       "(x & (x - 1) == 0), and compact set representation.",
        "worked_example": "Single Number: XOR every number in the array. Equal numbers cancel out "
                          "(x ^ x = 0), leaving only the unique element in O(N) time and O(1) space.",
    },
    "advanced-dsa": {
        "pattern": "Advanced Data Structures & Algorithms",
        "summary": "Combine sophisticated algorithmic paradigms (Segment Trees, Trie, Disjoint Set Union, "
                   "Topological Sort, Bridges) for complex scale.",
        "when_to_use": "Range query updates, prefix searching, dynamic connectivity, network flow, and "
                       "dependency resolution.",
        "worked_example": "Course Schedule: build an adjacency list and in-degree array, then process nodes "
                          "with in-degree 0 using BFS (Kahn's algorithm).",
    },
}


# --- momentum: streaks, daily goal, XP, levels, badges ---------------------
# Motivation is a real learning lever: consistency and visible progress keep a
# learner coming back. All in-memory (resets on restart, like everything here).
# XP/streak/badge state lives PER-USER in store["stats"] (lists, not sets, so it
# JSON-serialises to the user's database file). See _new_store().
DAILY_GOAL = 2

BADGES = [
    {"id": "first-blood", "emoji": "🎯", "label": "First Solve",
     "desc": "Pass every test on a problem for the first time."},
    {"id": "optimal-mind", "emoji": "⚡", "label": "Optimal Mind",
     "desc": "Solve a problem at the optimal time complexity."},
    {"id": "perfectionist", "emoji": "💎", "label": "Perfectionist",
     "desc": "Earn a perfect 100/100 overall score."},
    {"id": "streak-3", "emoji": "🔥", "label": "On a Roll",
     "desc": "Practice three days in a row."},
    {"id": "goal-met", "emoji": "✅", "label": "Goal Crusher",
     "desc": "Hit your daily solve goal."},
    {"id": "explorer", "emoji": "🧭", "label": "Explorer",
     "desc": "Solve problems across three different topics."},
    {"id": "level-5", "emoji": "🏆", "label": "Rising Star",
     "desc": "Reach level 5."},
]
BADGE_BY_ID = {b["id"]: b for b in BADGES}


def _badge_view(stats: dict, bid: str) -> dict:
    return {**BADGE_BY_ID[bid], "earned_at": stats["badges"].get(bid)}


def _level_for_xp(xp: int) -> tuple[int, int, int]:
    """Return (level, xp_at_start_of_level, xp_needed_to_next). 100, +50 per tier."""
    level, total, need = 1, 0, 100
    while xp >= total + need:
        total += need
        level += 1
        need += 50
    return level, total, need


def _streak(days: set[str]) -> tuple[int, int]:
    """(current streak ending today, longest run) over ISO dates."""
    if not days:
        return 0, 0
    ds = sorted(datetime.fromisoformat(d).date() for d in days)
    longest = cur = 1
    for i in range(1, len(ds)):
        gap = (ds[i] - ds[i - 1]).days
        if gap == 1:
            cur += 1
        elif gap == 0:
            continue
        else:
            cur = 1
        longest = max(longest, cur)
    today = datetime.now(timezone.utc).date()
    dayset = set(ds)
    cur_streak, d = 0, today
    while d in dayset:
        cur_streak += 1
        d = d - timedelta(days=1)
    return cur_streak, longest


def _check_badges(stats: dict, cur_streak: int, solved_today: int, level: int) -> list[str]:
    newly: list[str] = []

    def earn(bid: str) -> None:
        if bid not in stats["badges"]:
            stats["badges"][bid] = datetime.now(timezone.utc).isoformat()
            newly.append(bid)

    if stats["solved"]:
        earn("first-blood")
    if stats["optimal"]:
        earn("optimal-mind")
    if stats["perfect"] > 0:
        earn("perfectionist")
    if cur_streak >= 3:
        earn("streak-3")
    if solved_today >= DAILY_GOAL:
        earn("goal-met")
    if len(stats["topics_solved"]) >= 3:
        earn("explorer")
    if level >= 5:
        earn("level-5")
    return newly


def record_momentum(problem: dict, review: dict, tests: dict) -> dict:
    stats = _S()["stats"]
    all_passed = tests.get("all_passed", False)
    score = review.get("overall_score", 0)
    today = datetime.now(timezone.utc).date().isoformat()
    if today not in stats["practice_days"]:
        stats["practice_days"].append(today)
    pid = problem["id"]
    first_solve = all_passed and pid not in stats["solved"]
    tier = problem["difficulty_tier"]

    if all_passed:
        base = tier * 20 * (score / 100.0)
        # Full XP on the first solve; a small amount on re-solves so grinding
        # the same problem isn't the fast path to levelling up.
        xp_earned = max(int(round(base)) if first_solve else int(round(base * 0.2)),
                        5 if first_solve else 1)
    else:
        xp_earned = 3  # effort XP for a genuine attempt

    stats["xp"] += xp_earned
    if all_passed:
        if pid not in stats["solved"]:
            stats["solved"].append(pid)
        if problem["topic_slug"] not in stats["topics_solved"]:
            stats["topics_solved"].append(problem["topic_slug"])
        stats["solve_days_count"][today] = stats["solve_days_count"].get(today, 0) + 1
        det = review.get("detected_complexity", {}).get("time")
        opt = review.get("optimal_complexity", {}).get("time")
        if det and opt and _rank(str(det)) <= _rank(str(opt)) and pid not in stats["optimal"]:
            stats["optimal"].append(pid)
    if score >= 100:
        stats["perfect"] += 1

    cur, _ = _streak(stats["practice_days"])
    solved_today = stats["solve_days_count"].get(today, 0)
    level, floor_xp, span = _level_for_xp(stats["xp"])
    new_ids = _check_badges(stats, cur, solved_today, level)
    return {"xp_earned": xp_earned, "total_xp": stats["xp"], "level": level,
            "level_progress": stats["xp"] - floor_xp, "level_span": span,
            "streak": cur, "solved_today": solved_today, "daily_goal": DAILY_GOAL,
            "new_badges": [_badge_view(stats, i) for i in new_ids]}


def momentum_summary() -> dict:
    stats = _S()["stats"]
    cur, longest = _streak(stats["practice_days"])
    today = datetime.now(timezone.utc).date().isoformat()
    solved_today = stats["solve_days_count"].get(today, 0)
    level, floor_xp, span = _level_for_xp(stats["xp"])
    badges = [{**b, "earned": b["id"] in stats["badges"],
               "earned_at": stats["badges"].get(b["id"])} for b in BADGES]
    return {"xp": stats["xp"], "level": level,
            "level_progress": stats["xp"] - floor_xp, "level_span": span,
            "streak": cur, "longest_streak": longest,
            "daily_goal": DAILY_GOAL, "solved_today": solved_today,
            "solved_count": len(stats["solved"]),
            "badges": badges, "earned_count": len(stats["badges"])}


# --- learn by comparison: custom test runs + reference solutions -----------
def run_custom(problem: dict, code: str, args: list) -> dict:
    """Execute the learner's code against one arbitrary input (no grading)."""
    reason = _code_security_error(code)
    if reason:
        return {"status": "error", "returned": None, "stdout": "",
                "stderr": f"Blocked for security: {reason}", "runtime_ms": 0}
    started = time.perf_counter()
    job = json.dumps({"code": code, "entry_point": problem["entry_point"], "args": args})
    try:
        proc = subprocess.run([sys.executable, CHILD_RUNNER], input=job,
                              capture_output=True, text=True, timeout=6,
                              env=_SCRUBBED_ENV)
    except subprocess.TimeoutExpired:
        ms = int((time.perf_counter() - started) * 1000)
        return {"status": "timeout", "returned": None, "stdout": "",
                "stderr": "Time Limit Exceeded", "runtime_ms": ms}
    ms = int((time.perf_counter() - started) * 1000)
    try:
        payload = json.loads(proc.stdout)
    except (ValueError, TypeError):
        return {"status": "error", "returned": None, "stdout": "",
                "stderr": (proc.stderr or "no parseable output")[:2000], "runtime_ms": ms}
    if payload.get("status") == "error":
        return {"status": "error", "returned": None, "stdout": payload.get("stdout", ""),
                "stderr": f"{payload.get('error_type')}: {payload.get('stderr', '')}"[:2000],
                "runtime_ms": ms}
    return {"status": "ok", "returned": payload.get("returned"),
            "stdout": payload.get("stdout", ""), "stderr": "", "runtime_ms": ms}


def run_learning_snippet(code: str) -> dict:
    """Execute student code for interactive learning lessons in dev_backend."""
    reason = _code_security_error(code)
    if reason:
        return {"status": "error", "stdout": "",
                "stderr": f"Blocked for security: {reason}", "runtime_ms": 0}
    started = time.perf_counter()
    job = json.dumps({"code": code, "entry_point": None, "args": []})
    try:
        proc = subprocess.run([sys.executable, CHILD_RUNNER], input=job,
                              capture_output=True, text=True, timeout=6,
                              env=_SCRUBBED_ENV)
    except subprocess.TimeoutExpired:
        ms = int((time.perf_counter() - started) * 1000)
        return {"status": "timeout", "stdout": "",
                "stderr": "Time Limit Exceeded (Execution timed out)", "runtime_ms": ms}
    ms = int((time.perf_counter() - started) * 1000)
    try:
        payload = json.loads(proc.stdout)
    except (ValueError, TypeError):
        return {"status": "error", "stdout": "",
                "stderr": (proc.stderr or "no parseable output")[:2000], "runtime_ms": ms}
    if payload.get("status") == "error":
        return {"status": "error", "stdout": payload.get("stdout", ""),
                "stderr": f"{payload.get('error_type')}: {payload.get('stderr', '')}"[:2000],
                "runtime_ms": ms}
    return {
        "status": payload.get("status", "ok"),
        "stdout": payload.get("stdout", "")[:65536],
        "stderr": payload.get("stderr", "")[:65536],
        "runtime_ms": ms,
    }



REFERENCE_CACHE: dict[str, dict] = {}
REFERENCE_SYSTEM = """You are a staff engineer writing a model answer for a \
student who has ALREADY solved this problem. Give them the cleanest idiomatic \
Python solution to learn from.

Return ONLY a single JSON object, no markdown fences:
{"code": str, "commentary": str}
- "code" is a complete, runnable function named exactly as the entry point.
- "commentary" is 2-4 sentences: the key insight and the time/space complexity.
Do not include markdown code fences inside the strings."""


def reference_solution(problem: dict) -> dict:
    pid = problem["id"]
    if pid in REFERENCE_CACHE:
        return REFERENCE_CACHE[pid]
    ref = problem.get("reference_solution", "")
    if ref:
        opt_t = problem.get("optimal_time", "O(N)")
        opt_s = problem.get("optimal_space", "O(1)")
        commentary = (
            f"Optimal reference solution with {opt_t} time complexity and "
            f"{opt_s} space complexity."
        )
        result = {
            "available": True,
            "language": "python",
            "code": ref.strip(),
            "commentary": commentary,
        }
        REFERENCE_CACHE[pid] = result
        return result
    if not LLM_ENABLED:
        return {"available": False, "language": "python", "code": "",
                "commentary": "Reference solutions need the AI model, which isn't "
                              "configured in this offline session. Your Coach can still "
                              "walk you through the optimal approach step by step."}
    prompt = "\n".join([
        f"# Problem: {problem['title']}", problem["statement_md"].strip(), "",
        f"Entry point function: {problem['entry_point']}",
        f"Optimal complexity: time {problem['optimal_time']}, space {problem['optimal_space']}",
        "Starter code:", problem["starter_code"].get("python", ""), "",
        "Write the idiomatic optimal solution and commentary as JSON."])
    try:
        raw = gemini_complete(prompt, system=REFERENCE_SYSTEM, temperature=0.2,
                              want_json=True, max_tokens=900)
        draft = _extract_json(raw)
        result = {"available": True, "language": "python",
                  "code": str(draft.get("code", "")).strip(),
                  "commentary": str(draft.get("commentary", "")).strip()}
        if result["code"]:
            REFERENCE_CACHE[pid] = result
        return result
    except (LLMError, ValueError, KeyError, TypeError) as exc:
        sys.stderr.write(f"  dev-backend: reference gen failed ({exc})\n")
        return {"available": False, "language": "python", "code": "",
                "commentary": "Couldn't generate the reference solution right now — try "
                              "again in a moment, or ask your Coach for the optimal approach."}


# --- AI-generated adaptive problems ----------------------------------------
# The flagship: the model authors a brand-new problem for the learner's weakest
# topic, and we *validate* its test cases by executing the reference solution it
# also produces — so expected outputs are real, never hallucinated. A generated
# problem is registered into PROBLEMS like any other, so the entire existing
# pipeline (run/submit/review/momentum/spaced-rep/concept lessons) just works.
GENERATED: dict[str, dict] = {}  # pid -> {topic_slug, tier, created_at}

PROBLEM_GEN_SYSTEM = """You are an expert problem setter creating ONE original \
coding practice problem for a specific topic and difficulty tier.

Return ONLY a single JSON object (no markdown fences):
{
  "slug": str,                 // short kebab-case
  "title": str,
  "statement_md": str,         // clear statement in markdown, no example I/O
  "constraints_md": str,       // markdown bullet list of constraints
  "entry_point": str,          // snake_case function name
  "starter_code": str,         // python: "def <entry_point>(...):\\n    pass\\n"
  "reference_solution": str,   // python: a CORRECT solution defining <entry_point>
  "optimal_time": str,         // e.g. "O(n)"
  "optimal_space": str,        // e.g. "O(1)"
  "test_inputs": [[...], ...]  // 6-8 calls; each is the ARGUMENT LIST for one call
}

Rules:
- starter_code and reference_solution MUST define exactly <entry_point> with the
  same signature.
- Each element of test_inputs is the list of positional arguments for one call:
  for f(nums, target) an element looks like [[1,2,3], 5]. Include edge cases
  (empty, single element, boundaries).
- The reference_solution must be correct, self-contained, standard-library only,
  and run fast on the given inputs. It MUST `return` its answer (never mutate the
  input in place or print) and the return value must be JSON-serialisable.
- Match the requested topic and tier. Keep it solvable in under 30 lines.
- Keep test_inputs SMALL and compact (short arrays/graphs, ~6 cases) so the whole
  JSON stays concise and is never truncated.
- Do NOT put example input/output in the statement — the platform derives
  examples from the tests."""


def _pick_target() -> tuple[str, int]:
    """The topic you score LOWEST on, at its current tier.

    Untouched topics are deliberately excluded — AI generation reinforces where
    you're actively struggling, not where you simply haven't started yet.
    """
    practiced = [(slug, st) for slug, st in _S()["topic_state"].items()
                 if st.get("attempts", 0) > 0]
    if practiced:
        slug, st = min(practiced, key=lambda kv: kv[1]["avg"])
        return slug, max(1, min(5, st.get("tier", 1)))
    # No solve history yet — nothing to reinforce, so fall back to the first
    # topic at tier 1.
    return next(iter(TOPICS)), 1


def _validate_generated(entry: str, ref: str, inputs: list) -> list[dict]:
    """Run the model's reference solution to turn inputs into real expected
    outputs. Anything that errors/timeouts is silently dropped."""
    cases: list[dict] = []
    for args in inputs[:12]:
        if not isinstance(args, list):
            continue
        res = run_custom({"entry_point": entry}, ref, args)
        # Require a real return value: a reference that mutates in place and
        # returns None yields a degenerate problem, so drop those.
        if res["status"] == "ok" and res.get("returned") is not None:
            cases.append({"args": args, "expected": res["returned"]})
        if len(cases) >= 8:
            break
    return cases


def generate_problem(topic_slug: str | None = None, tier: int | None = None) -> dict:
    if not LLM_ENABLED:
        raise LLMError("problem generation needs the AI model (GEMINI_API_KEY)")
    if not topic_slug or topic_slug not in TOPICS:
        topic_slug, auto_tier = _pick_target()
        if tier is None:
            tier = auto_tier
    if tier is None:
        tier = _S()["topic_state"].get(topic_slug, {}).get("tier", 1)
    tier = max(1, min(5, int(tier)))
    topic_name = TOPICS.get(topic_slug, {}).get("name", topic_slug)

    prompt = "\n".join([
        f"Topic: {topic_name} (slug: {topic_slug})",
        f"Difficulty tier: {tier} of 5 ({TIER_LABELS.get(tier, '')})",
        "Create one original problem exactly as specified. Return JSON only."])

    # The model occasionally truncates or returns malformed JSON; give it a
    # second attempt before surfacing an error. max_tokens is generous enough to
    # fit a full statement + reference solution + tests without truncation.
    spec = entry = ref = None
    cases: list[dict] = []
    last_err: Exception | None = None
    for _ in range(3):
        try:
            raw = gemini_complete(prompt, system=PROBLEM_GEN_SYSTEM, temperature=0.7,
                                  want_json=True, max_tokens=4096, timeout=45.0)
            spec = _extract_json(raw)
            entry = str(spec.get("entry_point", "")).strip()
            ref = str(spec.get("reference_solution", "")).strip()
            if not entry or not ref:
                raise ValueError("generation missing entry_point/reference_solution")
            cases = _validate_generated(entry, ref, spec.get("test_inputs", []))
            if len(cases) < 3:
                raise ValueError("could not validate enough test cases from the reference")
            break
        except (ValueError, KeyError, TypeError) as exc:
            last_err = exc
            spec = None
    if spec is None:
        raise ValueError(str(last_err) if last_err else "generation failed")

    pid = str(uuid.uuid4())
    base_slug = str(spec.get("slug") or f"gen-{topic_slug}").strip() or f"gen-{topic_slug}"
    topic = TOPICS.get(topic_slug) or {
        "id": str(uuid.uuid5(NS, "topic:" + topic_slug)), "slug": topic_slug, "name": topic_name}
    starter = str(spec.get("starter_code", "")).strip() or f"def {entry}(*args):\n    pass\n"
    problem = {
        "id": pid, "slug": f"{base_slug}-{pid[:6]}",
        "title": str(spec.get("title", "Generated Problem")).strip() or "Generated Problem",
        "difficulty_tier": tier, "topic": topic, "topic_slug": topic_slug,
        "statement_md": str(spec.get("statement_md", "")).strip(),
        "constraints_md": str(spec.get("constraints_md", "")).strip(),
        "optimal_time": str(spec.get("optimal_time", "O(n)")).strip() or "O(n)",
        "optimal_space": str(spec.get("optimal_space", "O(n)")).strip() or "O(n)",
        "entry_point": entry,
        "starter_code": {"python": starter},
        "test_cases": cases,
        "generated": True,
    }
    PROBLEMS[pid] = problem
    PROBLEM_ORDER.append(pid)
    GENERATED[pid] = {"topic_slug": topic_slug, "tier": tier,
                      "created_at": datetime.now(timezone.utc).isoformat()}
    # The validated reference doubles as the "reveal reference solution" answer.
    REFERENCE_CACHE[pid] = {"available": True, "language": "python", "code": ref,
                            "commentary": f"This is the reference solution used to validate "
                                          f"the {len(cases)} test cases for this generated "
                                          f"problem — a clean, correct model answer."}
    return {**_detail(problem),
            "generation": {"topic": topic_name, "tier": tier,
                           "validated_cases": len(cases)}}


# --- authentication (username / email + password) --------------------------
# Sign up with a username (+ optional email) and a password. On registration we
# provision a PER-USER database keyed by username. Accounts (PBKDF2 password
# hash) persist to accounts.json / Upstash. Auth tokens are STATELESS, HMAC-
# signed (see _mint_session/_user_by_token) so they survive restarts and work
# across multiple instances — no server-side session store needed.
ACCOUNTS_PATH = os.path.join(HERE, "accounts.json")
USERDATA_DIR = os.path.join(HERE, "userdata")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
USERNAME_RE = re.compile(r"^[a-z0-9_.-]{3,20}$")
PBKDF2_ROUNDS = 200_000
_SAVE_LOCK = threading.Lock()
_ACCOUNTS_LOCK = threading.Lock()   # serialises the register read-modify-write

# Secret that signs auth tokens. MUST be a stable value from the environment in
# production (so tokens survive restarts and every instance shares it). Falls
# back to a random per-process secret in dev — which logs everyone out on
# restart, hence the startup warning if it isn't set.
AUTH_SECRET = os.getenv("AUTH_SECRET", "").strip() or secrets.token_hex(32)
AUTH_SECRET_FROM_ENV = bool(os.getenv("AUTH_SECRET", "").strip())
TOKEN_TTL_S = 7 * 24 * 3600         # a login lasts 7 days


def _atomic_write_json(path: str, data) -> None:
    """Crash-safe write: serialise to a temp file in the same directory, fsync
    it, then atomically os.replace() onto the target. A crash or a concurrent
    write can never leave a half-written / corrupt file — the target is always
    either the previous complete version or the new complete one."""
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)
    with _SAVE_LOCK:
        fd, tmp = tempfile.mkstemp(dir=directory, prefix=".tmp-", suffix=".json")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2)
                fh.flush()
                os.fsync(fh.fileno())
            # os.replace is atomic on both platforms, but on Windows it fails
            # with "access denied" while another handle (a reader, OneDrive,
            # antivirus) briefly holds the target. Those locks are transient —
            # retry with a short backoff before giving up.
            for attempt in range(12):
                try:
                    os.replace(tmp, path)
                    break
                except PermissionError:
                    if attempt == 11:
                        raise
                    time.sleep(0.03 * (attempt + 1))
        except BaseException:
            # Any failure (serialisation error, replace failure, interrupt):
            # discard the temp file. The target is never touched until the
            # atomic replace, so existing data is always preserved.
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise


# --- storage backend: durable cloud (Upstash Redis) or local files ---------
# If UPSTASH_REDIS_REST_URL + _TOKEN are set, accounts and per-user data live in
# Upstash (a free, persistent Redis with an HTTPS REST API — reachable with
# stdlib urllib, no extra deps). That means the data survives restarts/redeploys
# on ANY host, even a free ephemeral one. Without those vars it falls back to
# the local JSON files, so nothing changes for local dev.
UPSTASH_URL = os.getenv("UPSTASH_REDIS_REST_URL", "").strip().rstrip("/")
UPSTASH_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN", "").strip()
_USE_UPSTASH = bool(UPSTASH_URL and UPSTASH_TOKEN)
_KV_ACCOUNTS = "codementor:accounts"


def _kv_user_key(username: str) -> str:
    return f"codementor:user:{username}"


def _upstash_cmd(cmd: list):
    req = urllib.request.Request(
        UPSTASH_URL, data=json.dumps(cmd).encode(),
        headers={"Authorization": f"Bearer {UPSTASH_TOKEN}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
    if isinstance(data, dict) and data.get("error"):
        raise RuntimeError(data["error"])
    return data.get("result") if isinstance(data, dict) else None


def _kv_get(key: str):
    raw = _upstash_cmd(["GET", key])
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (ValueError, TypeError):
        return None


def _kv_set(key: str, value) -> None:
    _upstash_cmd(["SET", key, json.dumps(value)])


def _load_accounts() -> dict:
    if _USE_UPSTASH:
        try:
            return _kv_get(_KV_ACCOUNTS) or {}
        except Exception as exc:  # noqa: BLE001 -- degrade, don't crash on boot
            sys.stderr.write(f"  dev-backend: Upstash load accounts failed ({exc})\n")
            return {}
    try:
        with open(ACCOUNTS_PATH, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def _save_accounts() -> None:
    try:
        if _USE_UPSTASH:
            _kv_set(_KV_ACCOUNTS, ACCOUNTS)
        else:
            _atomic_write_json(ACCOUNTS_PATH, ACCOUNTS)
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"  dev-backend: could not save accounts ({exc})\n")


ACCOUNTS: dict[str, dict] = _load_accounts()   # username -> full account record
EMAIL_INDEX: dict[str, str] = {}               # email -> username (for email login)
for _uname, _acct in ACCOUNTS.items():
    if _acct.get("email"):
        EMAIL_INDEX[_acct["email"]] = _uname


# --- per-user data store ("their database") --------------------------------
_CTX = threading.local()   # holds the current request's store, set per request


def _new_store() -> dict:
    return {"submissions": [], "topic_state": {}, "last_submitted": {"pid": None},
            "review_state": {}, "misconceptions": {},
            "learning": {},
            "stats": {"xp": 0, "solved": [], "optimal": [], "perfect": 0,
                      "practice_days": [], "solve_days_count": {},
                      "topics_solved": [], "badges": {}}}


def _store_path(username: str) -> str:
    return os.path.join(USERDATA_DIR, username + ".json")


def _load_store(username: str) -> dict | None:
    data = None
    if _USE_UPSTASH:
        try:
            data = _kv_get(_kv_user_key(username))
        except Exception as exc:  # noqa: BLE001
            sys.stderr.write(f"  dev-backend: Upstash load store failed ({exc})\n")
            data = None
    else:
        try:
            with open(_store_path(username), encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, ValueError):
            data = None
    if data is None:
        return None
    base = _new_store()                                    # keep forward-compat keys
    base.update(data)
    base["learning"] = {**_new_store()["learning"], **data.get("learning", {})}
    base["stats"] = {**_new_store()["stats"], **data.get("stats", {})}
    return base


USER_DATA: dict[str, dict] = {}    # username -> store (lazy-loaded / cached)
_STORE_MTIMES: dict[str, float] = {}


def _store_for(username: str) -> dict:
    spath = _store_path(username)
    mtime = os.path.getmtime(spath) if os.path.exists(spath) else 0
    if username not in USER_DATA or mtime > _STORE_MTIMES.get(username, 0):
        loaded = _load_store(username)
        if loaded is not None:
            USER_DATA[username] = loaded
            _STORE_MTIMES[username] = mtime
        elif username not in USER_DATA:
            USER_DATA[username] = _new_store()
    return USER_DATA[username]


def _save_store(username: str) -> None:
    if username not in USER_DATA:
        return
    try:
        if _USE_UPSTASH:
            _kv_set(_kv_user_key(username), USER_DATA[username])
        else:
            _atomic_write_json(_store_path(username), USER_DATA[username])
            spath = _store_path(username)
            if os.path.exists(spath):
                _STORE_MTIMES[username] = os.path.getmtime(spath)
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"  dev-backend: could not save userdata ({exc})\n")


def _S() -> dict:
    """The current request's per-user store (set by the request handler)."""
    return _CTX.store


def compute_learning_progress(store: dict) -> dict:
    learning_days = store.setdefault("learning", {})
    completed_days = []
    day_states = {}
    found_current = False
    current_day = 1

    for day in range(1, 161):
        s_day = str(day)
        d_state = learning_days.get(s_day, {})
        lesson_done = bool(d_state.get("lesson_completed", False))
        practice_done = bool(d_state.get("practice_passed", False))
        is_completed = lesson_done and practice_done

        completed_at = d_state.get("completed_at")
        if is_completed and not completed_at:
            completed_at = datetime.now(timezone.utc).isoformat()
            d_state["completed_at"] = completed_at

        if is_completed:
            completed_days.append(day)

        is_unlocked = (day == 1) or ((day - 1) in completed_days)

        if is_completed:
            st = "completed"
        elif is_unlocked:
            if not found_current:
                st = "current"
                current_day = day
                found_current = True
            else:
                st = "available"
        else:
            st = "locked"

        day_states[s_day] = {
            "day_number": day,
            "lesson_completed": lesson_done,
            "lesson_completed_at": d_state.get("lesson_completed_at"),
            "practice_passed": practice_done,
            "practice_passed_at": d_state.get("practice_passed_at"),
            "completed": is_completed,
            "completed_at": completed_at,
            "unlocked": is_unlocked,
            "status": st,
            "practice_problem_slug": CURRICULUM_DAY_PRACTICE.get(day),
        }

    if not found_current and len(completed_days) == 160:
        current_day = 160

    return {
        "current_day": current_day,
        "completed_days": completed_days,
        "total_days": 160,
        "day_states": day_states,
    }


def complete_lesson(day_number: int) -> tuple[int, dict]:
    if not isinstance(day_number, int) or day_number < 1 or day_number > 160:
        return 400, {"detail": "Invalid day_number. Must be between 1 and 160."}

    progress = compute_learning_progress(_S())
    day_state = progress["day_states"].get(str(day_number))

    if not day_state or not day_state["unlocked"]:
        return 403, {"detail": f"Day {day_number} is locked. Complete Day {day_number - 1} first."}

    learning_days = _S().setdefault("learning", {})
    d_record = learning_days.setdefault(str(day_number), {
        "lesson_completed": False,
        "lesson_completed_at": None,
        "practice_passed": False,
        "practice_passed_at": None,
        "completed_at": None,
    })

    now_iso = datetime.now(timezone.utc).isoformat()
    d_record["lesson_completed"] = True
    if not d_record.get("lesson_completed_at"):
        d_record["lesson_completed_at"] = now_iso

    if d_record.get("practice_passed") and not d_record.get("completed_at"):
        d_record["completed_at"] = now_iso

    updated_progress = compute_learning_progress(_S())
    return 200, {
        "day_number": day_number,
        "lesson_completed": True,
        "day_completed": d_record.get("practice_passed", False),
        "unlocked_next_day": d_record.get("practice_passed", False) and day_number < 160,
        "current_day": updated_progress["current_day"],
        "day_state": updated_progress["day_states"][str(day_number)],
    }


def record_learning_practice_passed(problem_slug: str) -> dict | None:
    days = PRACTICE_SLUG_TO_DAYS.get(problem_slug, [])
    if not days:
        return None

    now_iso = datetime.now(timezone.utc).isoformat()
    learning_days = _S().setdefault("learning", {})
    affected = []
    newly_completed = []

    for day in days:
        d_record = learning_days.setdefault(str(day), {
            "lesson_completed": False,
            "lesson_completed_at": None,
            "practice_passed": False,
            "practice_passed_at": None,
            "completed_at": None,
        })
        d_record["practice_passed"] = True
        if not d_record.get("practice_passed_at"):
            d_record["practice_passed_at"] = now_iso

        if d_record.get("lesson_completed") and not d_record.get("completed_at"):
            d_record["completed_at"] = now_iso
            newly_completed.append(day)

        affected.append(day)

    updated = compute_learning_progress(_S())
    return {
        "affected_days": affected,
        "newly_completed_days": newly_completed,
        "unlocked_days": [d + 1 for d in newly_completed if d < 160],
        "current_day": updated["current_day"],
    }



# --- accounts & stateless tokens -------------------------------------------
def _b64u(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def _b64u_decode(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def _mint_session(username: str) -> str:
    """A stateless, HMAC-signed token: base64(payload).base64(signature). No
    server-side store — it verifies on any instance and survives restarts."""
    payload = json.dumps({"u": username, "exp": int(time.time()) + TOKEN_TTL_S},
                         separators=(",", ":")).encode()
    body = _b64u(payload)
    sig = _b64u(hmac.new(AUTH_SECRET.encode(), body.encode(), hashlib.sha256).digest())
    return f"{body}.{sig}"


def _public(acct: dict) -> dict:
    """The user object sent to the client — never the password hash/salt."""
    return {"id": acct["id"], "username": acct["username"],
            "email": acct.get("email"), "name": acct.get("name"),
            "avatar_url": acct.get("avatar_url")}


def _user_by_token(token: str | None) -> dict | None:
    if not token or "." not in token:
        return None
    body, _, sig = token.partition(".")
    expected = _b64u(hmac.new(AUTH_SECRET.encode(), body.encode(), hashlib.sha256).digest())
    if not hmac.compare_digest(sig, expected):
        return None
    try:
        data = json.loads(_b64u_decode(body))
    except (ValueError, TypeError):
        return None
    if not isinstance(data, dict) or data.get("exp", 0) < time.time():
        return None
    acct = ACCOUNTS.get(data.get("u"))
    return _public(acct) if acct else None


def _hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt),
                                 PBKDF2_ROUNDS).hex()
    return salt, digest


def auth_register(username, password, email=None, name=None) -> tuple[int, dict]:
    username = (username or "").strip().lower()
    password = password or ""
    email = (email or "").strip().lower() or None
    if not USERNAME_RE.match(username):
        return 400, {"detail": "Username must be 3-20 characters: letters, numbers, . _ -"}
    if len(password) < 6:
        return 400, {"detail": "Password must be at least 6 characters."}
    if email and not EMAIL_RE.match(email):
        return 400, {"detail": "Enter a valid email address (or leave it blank)."}
    salt, digest = _hash_password(password)   # slow (PBKDF2) — do it before the lock
    # Serialise the check-then-insert so two simultaneous signups can't both
    # claim the same username/email or clobber the shared accounts record.
    with _ACCOUNTS_LOCK:
        if _USE_UPSTASH:
            # ACCOUNTS is loaded once at process start and kept in memory; a
            # long-lived server (or another instance/process) can drift from
            # what's actually in Upstash. _save_accounts() writes the WHOLE
            # dict, so a stale copy would resurrect anything deleted directly
            # in the store. Re-sync right before mutating to close that window.
            fresh = _load_accounts()
            ACCOUNTS.clear()
            ACCOUNTS.update(fresh)
            EMAIL_INDEX.clear()
            for _u, _a in ACCOUNTS.items():
                if _a.get("email"):
                    EMAIL_INDEX[_a["email"]] = _u
        if username in ACCOUNTS:
            return 409, {"detail": "That username is already taken."}
        if email and email in EMAIL_INDEX:
            return 409, {"detail": "That email is already registered."}
        acct = {"id": str(uuid.uuid5(NS, "user:" + username)), "username": username,
                "email": email, "name": (name or "").strip() or username.title(),
                "avatar_url": None, "salt": salt, "pwd_hash": digest,
                "created_at": datetime.now(timezone.utc).isoformat()}
        ACCOUNTS[username] = acct
        if email:
            EMAIL_INDEX[email] = username
        _save_accounts()
    _store_for(username)          # provision + persist their personal database
    _save_store(username)
    return 200, {"access_token": _mint_session(username), "user": _public(acct)}


def auth_login(identifier, password) -> tuple[int, dict]:
    identifier = (identifier or "").strip().lower()
    username = identifier if identifier in ACCOUNTS else EMAIL_INDEX.get(identifier)
    acct = ACCOUNTS.get(username or "")
    if not acct or not acct.get("pwd_hash"):
        return 401, {"detail": "Incorrect username/email or password."}
    _, digest = _hash_password(password or "", acct["salt"])
    if not secrets.compare_digest(digest, acct["pwd_hash"]):
        return 401, {"detail": "Incorrect username/email or password."}
    return 200, {"access_token": _mint_session(acct["username"]), "user": _public(acct)}


# --- abuse protection & CORS -----------------------------------------------
# Locking CORS to your real frontend origin(s) and rate-limiting per IP keeps a
# public demo from being hammered or having its shared LLM quota drained.
ALLOWED_ORIGINS = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]
MAX_BODY_BYTES = 256 * 1024
_RATE_BUCKET: dict[tuple[str, str], list] = {}   # (ip, bucket) -> [count, window_start]
_RATE_LOCK = threading.Lock()
# Requests per minute per IP, per endpoint.
RATE_LIMITS = {
    "/api/auth/register": 10, "/api/auth/login": 10,
    "/api/submissions": 30, "/api/submissions/run": 45,
    "/api/submissions/run-custom": 45, "/api/problems/generate": 6,
    "/api/tutor/chat": 20, "/api/coach/debrief": 20,
    "/api/learning/run": 60,
    "/api/learning/tutor/chat": 20, "/api/learning/tutor/quick-action": 20,
}


def _rate_ok(ip: str, bucket: str, limit: int, window_s: int = 60) -> bool:
    now = time.time()
    key = (ip, bucket)
    with _RATE_LOCK:
        entry = _RATE_BUCKET.get(key)
        if not entry or now - entry[1] >= window_s:
            _RATE_BUCKET[key] = [1, now]
            return True
        if entry[0] >= limit:
            return False
        entry[0] += 1
        return True


# --- HTTP ------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        sys.stderr.write("  dev-backend: " + (fmt % args) + "\n")

    def _cors(self):
        origin = self.headers.get("Origin", "")
        if ALLOWED_ORIGINS:
            allow = origin if origin in ALLOWED_ORIGINS else ALLOWED_ORIGINS[0]
        else:
            allow = origin if origin else "http://localhost:3000"
        self.send_header("Access-Control-Allow-Origin", allow)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type, Accept, Origin, X-Requested-With")
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_header("Access-Control-Max-Age", "86400")
        self.send_header("Vary", "Origin")

    def _json(self, status: int, obj) -> None:
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0) or 0)
        if not length or length > MAX_BODY_BYTES:
            return {}
        try:
            return json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, TypeError):
            return {}

    def _bearer(self) -> str | None:
        header = self.headers.get("Authorization", "")
        return header[7:].strip() if header.lower().startswith("bearer ") else None

    def _client_ip(self) -> str:
        xff = self.headers.get("X-Forwarded-For", "")
        return xff.split(",")[0].strip() if xff else self.client_address[0]

    def _rate_limited(self, bucket: str, limit: int) -> bool:
        if _rate_ok(self._client_ip(), bucket, limit):
            return False
        self._json(429, {"detail": "Too many requests — please slow down a moment."})
        return True

    def _require(self) -> dict | None:
        """Resolve the signed-in user and bind their per-user store to this
        request. Sends 401 and returns None if not authenticated."""
        user = _user_by_token(self._bearer())
        if not user:
            self._json(401, {"detail": "Not authenticated"})
            return None
        _CTX.store = _store_for(user["username"])
        return user

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            return self._json(200, {"status": "ok"})
        if path == "/api/auth/me":
            user = _user_by_token(self._bearer())
            if not user:
                return self._json(401, {"detail": "Not authenticated"})
            return self._json(200, user)
        if path == "/api/problems":
            # Optional auth: if a valid token is present, mark which problems this
            # learner has already solved so the list can show a ✓. No token → no
            # 401, just every solved=False (the list stays public/browsable).
            solved: set = set()
            user = _user_by_token(self._bearer())
            if user:
                _CTX.store = _store_for(user["username"])
                solved = set(_S()["stats"]["solved"])
            items = []
            for pid in PROBLEM_ORDER:
                summary = _summary(PROBLEMS[pid])
                summary["solved"] = pid in solved
                items.append(summary)
            return self._json(200, {"items": items, "page": 1,
                                    "page_size": len(items), "total": len(items)})
        if path == "/api/problems/next":
            if not self._require():
                return
            return self._json(200, _detail(next_problem()))
        if path.startswith("/api/problems/") and path.endswith("/reference"):
            pid = path[len("/api/problems/"):-len("/reference")]
            problem = _find_problem(pid)
            if not problem:
                return self._json(404, {"detail": "Problem not found"})
            return self._json(200, reference_solution(problem))
        if path.startswith("/api/problems/"):
            pid = path.rsplit("/", 1)[-1]
            problem = _find_problem(pid)
            if not problem:
                return self._json(404, {"detail": "Problem not found"})
            return self._json(200, _detail(problem))
        if path == "/api/learning/progress":
            if not self._require():
                return
            return self._json(200, compute_learning_progress(_S()))
        if path == "/api/progress/topics":

            if not self._require():
                return
            return self._json(200, progress_topics())
        if path == "/api/progress/trend":
            if not self._require():
                return
            points = [{"submission_id": s["submission_id"],
                       "overall_score": s["overall_score"],
                       "created_at": s["created_at"]} for s in _S()["submissions"][-20:]]
            return self._json(200, {"points": points})
        if path == "/api/review/due":
            if not self._require():
                return
            return self._json(200, review_queue())
        if path == "/api/recent-solved":
            if not self._require():
                return
            return self._json(200, recent_solved())
        if path == "/api/account/summary":
            if not self._require():
                return
            return self._json(200, account_summary())
        if path == "/api/insights/misconceptions":
            if not self._require():
                return
            return self._json(200, misconceptions_summary())
        if path == "/api/momentum":
            if not self._require():
                return
            return self._json(200, momentum_summary())
        return self._json(404, {"detail": "Not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        limit = RATE_LIMITS.get(path)
        if limit is not None and self._rate_limited(path, limit):
            return
        body = self._body()

        if path == "/api/auth/register":
            status, payload = auth_register(body.get("username", ""), body.get("password", ""),
                                            body.get("email"), body.get("name"))
            return self._json(status, payload)

        if path in ("/api/auth/login", "/api/auth/google", "/api/auth/dev"):
            status, payload = auth_login(
                body.get("identifier") or body.get("username") or body.get("email", ""),
                body.get("password", ""))
            return self._json(status, payload)

        if path == "/api/problems/generate":
            if not self._require():
                return
            topic = body.get("topic")
            tier = body.get("tier")
            try:
                return self._json(200, generate_problem(topic, tier))
            except LLMError as exc:
                return self._json(503, {"detail": f"Couldn't generate a problem: {exc}"})
            except (ValueError, KeyError, TypeError) as exc:
                sys.stderr.write(f"  dev-backend: problem generation failed ({exc})\n")
                return self._json(502, {"detail": "The model returned an unusable problem. "
                                                   "Please try again."})

        if path.startswith("/api/problems/") and path.endswith("/run"):
            pid = path[len("/api/problems/"):-len("/run")]
            problem = _find_problem(pid)
            if not problem:
                return self._json(404, {"detail": "Problem not found"})
            return self._json(200, run_tests(problem, body.get("code", "")))

        if path.startswith("/api/problems/") and path.endswith("/submit"):
            user = self._require()
            if not user:
                return
            pid = path[len("/api/problems/"):-len("/submit")]
            problem = _find_problem(pid)
            if not problem:
                return self._json(404, {"detail": "Problem not found"})
            code = body.get("code", "")
            tests = run_tests(problem, code)
            review = review_submission(problem, code, tests)
            difficulty = apply_difficulty(problem["topic_slug"], review["overall_score"])
            _S()["last_submitted"]["pid"] = problem["id"]
            schedule = schedule_review(problem, review, tests["all_passed"])
            misconception = record_misconception(problem, tests)
            momentum = record_momentum(problem, review, tests)
            learning_update = None
            if tests.get("all_passed"):
                learning_update = record_learning_practice_passed(problem["slug"])
            sid = str(uuid.uuid4())
            _S()["submissions"].append({"submission_id": sid,
                                        "overall_score": review["overall_score"],
                                        "created_at": datetime.now(timezone.utc).isoformat()})
            _save_store(user["username"])
            return self._json(200, {"submission_id": sid, "tests": tests,
                                    "review": review, "difficulty": difficulty,
                                    "review_schedule": schedule,
                                    "misconception": misconception,
                                    "momentum": momentum,
                                    "learning_update": learning_update})

        if path == "/api/submissions/run":
            problem = _find_problem(body.get("problem_id"))
            if not problem:
                return self._json(404, {"detail": "Problem not found"})
            return self._json(200, run_tests(problem, body.get("code", "")))

        if path == "/api/submissions/run-custom":
            problem = _find_problem(body.get("problem_id"))
            if not problem:
                return self._json(404, {"detail": "Problem not found"})
            args = body.get("args")
            if not isinstance(args, list):
                return self._json(400, {"detail": "args must be a JSON array of arguments"})
            return self._json(200, run_custom(problem, body.get("code", ""), args))

        if path == "/api/learning/run":
            code = body.get("code", "")
            return self._json(200, run_learning_snippet(code))

        if path == "/api/learning/complete-lesson":
            user = self._require()
            if not user:
                return
            day_num = body.get("day_number")
            status_code, resp = complete_lesson(day_num)
            _save_store(user["username"])
            return self._json(status_code, resp)

        if path == "/api/learning/dev-set-progress":
            user = self._require()
            if not user:
                return
            completed_up_to = int(body.get("completed_up_to", 0))
            now_iso = datetime.now(timezone.utc).isoformat()
            learning_days = _S().setdefault("learning", {})
            for d in range(1, completed_up_to + 1):
                d_record = learning_days.setdefault(str(d), {})
                d_record["lesson_completed"] = True
                d_record["lesson_completed_at"] = now_iso
                d_record["practice_passed"] = True
                d_record["practice_passed_at"] = now_iso
                d_record["completed_at"] = now_iso
            _save_store(user["username"])
            return self._json(200, compute_learning_progress(_S()))

        if path == "/api/learning/tutor/chat":
            user = self._require()
            if not user:
                return
            msg = (body.get("message") or "").strip()
            user_code = body.get("user_code")
            day_num = int(body.get("day_number", 1))
            step_num = int(body.get("step_number", 1))
            history = body.get("history") or []
            step_ctx = body.get("step_context") or {}
            quick_act = body.get("quick_action")
            hint_lvl = int(body.get("hint_level", 1))

            try:
                from app.services.tutor_security import sanitize_tutor_input
                val_res = sanitize_tutor_input(msg, user_code)
                if not val_res.is_valid:
                    return self._json(400, {"detail": val_res.error_message or "Invalid message"})
                clean_msg = val_res.sanitized_message
                clean_code = val_res.sanitized_code
            except Exception:
                clean_msg = msg[:2000]
                clean_code = user_code[:20000] if user_code else None

            svc = get_dev_teacher_svc()
            if svc:
                resp = svc.generate_response(
                    day_number=day_num,
                    step_number=step_num,
                    query=clean_msg,
                    history=history,
                    user_code=clean_code,
                    step_context=step_ctx,
                    quick_action=quick_act,
                    hint_level=hint_lvl,
                )
            else:
                resp = {
                    "reply": "I'm your CodeMentor AI Teacher. How can I help you with today's lesson?",
                    "quick_action": quick_act,
                    "related_concepts": [],
                    "pedagogical_mode": "socratic",
                    "visual": None,
                }
            return self._json(200, resp)

        if path == "/api/learning/tutor/quick-action":
            user = self._require()
            if not user:
                return
            action = (body.get("action") or "").strip()
            if not action:
                return self._json(400, {"detail": "Action is required"})
            user_code = body.get("user_code")
            day_num = int(body.get("day_number", 1))
            step_num = int(body.get("step_number", 1))
            history = body.get("history") or []
            step_ctx = body.get("step_context") or {}
            hint_lvl = int(body.get("hint_level", 1))

            try:
                from app.services.tutor_security import sanitize_tutor_input
                val_res = sanitize_tutor_input(f"Action: {action}", user_code)
                clean_code = val_res.sanitized_code
            except Exception:
                clean_code = user_code[:20000] if user_code else None

            svc = get_dev_teacher_svc()
            if svc:
                resp = svc.generate_response(
                    day_number=day_num,
                    step_number=step_num,
                    query="",
                    history=history,
                    user_code=clean_code,
                    step_context=step_ctx,
                    quick_action=action,
                    hint_level=hint_lvl,
                )
            else:
                resp = {
                    "reply": f"Performing quick action: {action}",
                    "quick_action": action,
                    "related_concepts": [],
                    "pedagogical_mode": "socratic",
                    "visual": None,
                }
            return self._json(200, resp)

        if path == "/api/submissions":
            user = self._require()
            if not user:
                return
            problem = _find_problem(body.get("problem_id"))
            if not problem:
                return self._json(404, {"detail": "Problem not found"})
            code = body.get("code", "")
            tests = run_tests(problem, code)
            review = review_submission(problem, code, tests)
            difficulty = apply_difficulty(problem["topic_slug"], review["overall_score"])
            _S()["last_submitted"]["pid"] = problem["id"]
            # Spaced repetition + misconception tracking + momentum (additive).
            schedule = schedule_review(problem, review, tests["all_passed"])
            misconception = record_misconception(problem, tests)
            momentum = record_momentum(problem, review, tests)
            learning_update = None
            if tests.get("all_passed"):
                learning_update = record_learning_practice_passed(problem["slug"])
            sid = str(uuid.uuid4())
            _S()["submissions"].append({"submission_id": sid,
                                        "overall_score": review["overall_score"],
                                        "created_at": datetime.now(timezone.utc).isoformat()})
            _save_store(user["username"])   # persist this learner's database
            return self._json(200, {"submission_id": sid, "tests": tests,
                                    "review": review, "difficulty": difficulty,
                                    "review_schedule": schedule,
                                    "misconception": misconception,
                                    "momentum": momentum,
                                    "learning_update": learning_update})


        if path == "/api/tutor/chat":
            if not self._require():
                return
            msg = (body.get("message") or "").strip()
            code = body.get("code", "")
            problem = PROBLEMS.get(body.get("problem_id"))
            notes = []
            if _S()["submissions"]:
                notes = [{"id": str(uuid.uuid4()),
                          "content": "User tends to miss empty-input edge cases; "
                                     "prompt them to check boundaries first.",
                          "similarity": 0.82}]
            if LLM_ENABLED and msg:
                try:
                    reply = tutor_reply(problem, code, msg)
                except LLMError as exc:
                    sys.stderr.write(f"  dev-backend: tutor LLM failed ({exc})\n")
                    reply = ("I can't reach my brain right now — but look at your "
                             "failing edge cases first (empty / single-element "
                             "input), then see if any nested loop can collapse.")
            else:
                reply = ("Ask me for a hint and I'll guide you. "
                         "(No LLM key configured, so this is a canned reply.)")
            return self._json(200, {"reply": reply, "retrieved_notes": notes})

        if path == "/api/coach/debrief":
            if not self._require():
                return
            problem = PROBLEMS.get(body.get("problem_id"))
            if not problem:
                return self._json(404, {"detail": "Problem not found"})
            code = body.get("code", "")
            review = body.get("review") or {}
            tests = body.get("tests") or {}
            plan = (body.get("plan") or "").strip()
            if LLM_ENABLED:
                try:
                    message = coach_debrief(problem, code, review, tests, plan)
                except LLMError as exc:
                    sys.stderr.write(f"  dev-backend: coach LLM failed ({exc})\n")
                    message = _coach_fallback(review, tests, plan)
            else:
                message = _coach_fallback(review, tests, plan)
            return self._json(200, {"message": message})

        return self._json(404, {"detail": "Not found"})


def main():
    if PROVIDERS:
        pool = ", ".join(f"{p['name']}({p['model']})" for p in PROVIDERS)
    else:
        pool = "OFF (heuristic only)"
    storage = "Upstash Redis (durable, cloud)" if _USE_UPSTASH else "local files (dev)"
    print(f"CodeMentor backend")
    print(f"  loaded {len(TOPICS)} topics, {len(PROBLEMS)} problems from seed.py")
    print(f"  storage: {storage}")
    print(f"  auth tokens: stateless HMAC ({'AUTH_SECRET from env' if AUTH_SECRET_FROM_ENV else 'RANDOM per-process'})")
    print(f"  LLM providers (failover order): {pool}")

    # Production readiness warnings — loud, but non-fatal.
    warnings = []
    if not AUTH_SECRET_FROM_ENV:
        warnings.append("AUTH_SECRET not set -> logins will break on restart. Set it in production.")
    if not ALLOWED_ORIGINS:
        warnings.append("ALLOWED_ORIGINS not set -> CORS reflects any origin. Set it to your frontend URL in production.")
    if not _USE_UPSTASH and IS_PRODUCTION:
        warnings.append("No Upstash configured -> data is on local disk and may be lost on this host.")
    for w in warnings:
        sys.stderr.write(f"  dev-backend: WARNING - {w}\n")

    print(f"  listening on http://{HOST}:{PORT}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
