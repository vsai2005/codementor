# CodeMentor AI

AI coding-practice platform: LLM code review with structured scoring, per-topic
adaptive difficulty, and pgvector-backed memory that persists across sessions.

```
Next.js 15  ──HTTP──▶  FastAPI  ──▶  sandbox (subprocess + netns + rlimits)
                          │
                          ├──▶  LLM (Claude | GPT, swapped by env var)
                          ├──▶  Postgres 16
                          └──▶  pgvector  ◀── memory notes, always WHERE user_id
```

## Run it

```bash
docker compose up -d                      # postgres:16 + pgvector

# backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                      # JWT_SECRET, GOOGLE_CLIENT_ID, API keys
alembic upgrade head
python -m app.seed                        # 6 topics, 18 problems
uvicorn app.main:app --reload             # http://localhost:8000/docs

# frontend (new terminal)
cd frontend
npm install
cp .env.local.example .env.local          # API base URL + Google client ID
npm run dev                               # http://localhost:3000
```

### Tests

```bash
cd backend
pytest                                    # 84 unit tests, no DB needed

# integration tests, opt-in:
export TEST_DATABASE_URL=postgresql+psycopg://codementor:codementor@localhost:5432/codementor_test
pytest -m integration                     # 12 tests: migration, pgvector, isolation

cd ../frontend
npm run typecheck && npm run build
```

## Layout

```
backend/app/
  services/     business logic — imports no FastAPI
    sandbox.py        untrusted code execution
    difficulty.py     pure tier function, no I/O
    review.py         LLM pipeline + degradation
    memory.py         RAG, user-scoped
    ratelimit.py      sliding window
    submissions.py    pipeline orchestration
  api/routes/   thin routers, Pydantic in and out
  models/       SQLAlchemy 2.x
  schemas/      request/response + LLM contract

frontend/
  app/          App Router: /, /login, /dashboard, /practice,
                /practice/[id], /tutor, /profile
  components/   the PRD 4.5 inventory
  lib/          api client, auth, types, autosave hook
```

## Four spec conflicts, resolved

**1. The sandbox couldn't pass its own network test.** `resource.setrlimit`
caps CPU, memory and file size — it does nothing about sockets, so
`subprocess + setrlimit` alone can't satisfy "no network access." Now two
layers: a network namespace via `unshare -n` when the host permits it, and a
socket-neutering harness in the child that works unprivileged. Both tested.

**2. Timeout conflict (15s vs 8s).** PRD §5.7 degraded at 15s while §4.4 gave
the frontend 8s — the user would see an error while the backend was still
waiting. Now 6s for the first LLM call, 4s for the retry. `LLM_TIMEOUT_S` is
env-tunable.

**3. Seed count (40–60 vs 12).** Seeds 18 across 6 topics. Six topics × five
tiers is 30 cells, so `/api/problems/next` widens outward from the target tier
instead of returning nothing. Add problems before claiming the adaptive engine
is fully exercised.

**4. Two orphaned requirements.** Rate limiting (§5.4 step 1) appeared in no
build prompt — implemented and tested. Phase 5 had no prompt at all — dashboard,
tutor UI and landing are now built.

## Deliberate deviations from the PRD

- **No NextAuth.js** (§4.1 names it). The backend already issues and owns the
  session JWT; adding NextAuth would mean two session systems to keep in sync.
  Google Identity Services returns an ID token, exchanged at
  `POST /api/auth/google`.
- **No GSAP/ScrollTrigger.** The landing page is short enough that scroll
  choreography would be decoration. Three.js is used for the hero as specced,
  and it no-ops under `prefers-reduced-motion`.
- **The LLM does not compute `overall_score`** and **does not get a vote on
  correctness.** It returns dimension scores; the server applies the weights and
  the wrong-answer cap, and overwrites correctness with real test results.
  Otherwise the cap is unenforceable.
- **Fewer than 3 submissions uses a plain mean.** Applying 0.5/0.3/0.2 to two
  scores gives 64 for someone who scored 80 twice — a silent deflation.
- **`MemoryService` re-filters by `user_id`** after the repository returns, so a
  leaky query stays a bug instead of becoming a breach. The suite includes a
  deliberately leaky repository to prove it.

## Verification status

Everything below was actually run, with output checked.

| Check | Result |
|---|---|
| `pytest` | 84 passed, 12 skipped (integration) |
| Sandbox network isolation | `unshare -n` confirmed blocking, live |
| Infinite loop + `sleep(600)` | both killed; CPU limit and wall clock each catch one |
| Tier convergence simulation | settles at true level by submission 5 |
| Backend route registration | 12 endpoints in the OpenAPI schema |
| `tsc --noEmit` (strict, `noUncheckedIndexedAccess`) | clean |
| `next build` | 9 routes compiled |
| `next start` + HTTP | `/`, `/login`, `/practice` all 200 with rendered content |

### Not verified — do this before trusting it

1. **The 12 integration tests have never run.** No Postgres was available in the
   build environment. They are written and they skip cleanly, but "written" is
   not "passing." Run them first — they cover the migration cycle, the ivfflat
   query, and cross-user isolation in real SQL.
2. **No live LLM call.** The review pipeline is tested only against a mocked
   client. Confirm the model returns the JSON shape and that p95 is under 8s.
3. **No browser testing.** The four review states, localStorage autosave,
   double-submit dedupe and the 375px layout are implemented and type-check, but
   nothing has been clicked. The PRD's manual checklist (§4.4) is still owed.
4. **Google OAuth end-to-end.** Needs a real client ID.

### Known security advisory

`npm audit` flags `next` (high) with no forward fix published — npm's suggested
remedy is a downgrade to Next 9, which has no App Router and is not viable.
Pinned to 15.5.22, the latest 15.x. `postcss` is pinned to 8.5.24 directly; the
remaining transitive warnings (`sharp`, `dompurify`, `monaco-editor`) arrive
through Next and clear when Next ships a patch. Re-run `npm audit` before
deploying.

## Deploy

- Backend: `render.yaml` blueprint, Docker, migrations run on boot.
- Frontend: `frontend/vercel.json`, framework preset.
- Set `CORS_ORIGINS` to the Vercel origin. Never `*`.

## Tests worth knowing about

| Test | Guards |
|---|---|
| `test_infinite_loop_times_out_without_hanging_the_caller` | sandbox |
| `test_consecutive_demotions_demote_once_then_cooldown_blocks` | tier logic |
| `test_user_a_never_receives_user_b_notes` | isolation (fakes) |
| `test_repository_never_returns_another_users_notes` | isolation (real SQL) |

```
tests/test_sandbox.py          13   execution, timeouts, network, memory, syntax
tests/test_difficulty.py       24   table-driven §3.2 + convergence simulation
tests/test_review.py           20   weights, cap, retry-once, degradation
tests/test_memory.py           16   isolation, dedupe, ordering, resilience
tests/test_ratelimit.py         5   window, per-user, concurrency
tests/test_auth.py              6   expiry, forged signature, alg=none
tests/test_db_integration.py   12   migration, pgvector, isolation  [needs DB]
```
