"""LLM abstraction and defensive response parsing (Phase 4).

One interface, provider chosen by env var, so swapping Claude -> GPT -> local
is a config change. No FastAPI imports here.
"""

from __future__ import annotations

import json
import os
import re
from abc import ABC, abstractmethod
from typing import Any, TypeVar

T = TypeVar("T")


class LLMError(RuntimeError):
    """Provider failure: timeout, transport error, refusal."""


class LLMTimeout(LLMError):
    pass


class LLMJsonParseError(LLMError):
    """Structured exception when LLM JSON extraction or validation fails."""

    def __init__(self, message: str, raw_text: str = "") -> None:
        super().__init__(message)
        self.raw_text = raw_text


def extract_json(raw: str) -> dict[str, Any]:
    """Pull a JSON object out of a model response with repair heuristic."""
    text = (raw or "").strip()
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fenced:
        text = fenced.group(1).strip()

    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    start, end = text.find("{"), text.rfind("}")
    if start != -1 and end > start:
        try:
            data = json.loads(text[start : end + 1])
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError as exc:
            raise LLMJsonParseError(f"JSON syntax repair failed: {exc}", raw_text=raw) from exc
    raise LLMJsonParseError("No valid JSON object found in model response", raw_text=raw)


def parse_llm_json(response_text: str, target_schema: type[T]) -> T:
    """Generic extraction and schema validation helper (Phase 4).

    1. Strips markdown fences.
    2. Attempts direct deserialization, falling back to outer bracket repair heuristic.
    3. Validates against target_schema (Pydantic model).
    4. Raises LLMJsonParseError instead of unhandled 500 runtime errors.
    """
    parsed_dict = extract_json(response_text)

    try:
        if hasattr(target_schema, "model_validate"):
            return target_schema.model_validate(parsed_dict)
        return target_schema(**parsed_dict)  # type: ignore[call-arg]
    except Exception as exc:
        schema_name = getattr(target_schema, "__name__", str(target_schema))
        raise LLMJsonParseError(
            f"Schema validation failed for {schema_name}: {exc}", raw_text=response_text
        ) from exc


class LLMClient(ABC):
    @abstractmethod
    def complete(self, prompt: str, *, system: str = "", temperature: float = 0.2,
                 max_tokens: int = 1500, timeout: float = 6.0) -> str:
        ...


class AnthropicClient(LLMClient):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6") -> None:
        self._api_key = api_key
        self._model = model

    def complete(self, prompt, *, system="", temperature=0.2,
                 max_tokens=1500, timeout=6.0) -> str:
        import httpx

        try:
            response = httpx.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self._api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": self._model,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "system": system,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=timeout,
            )
        except httpx.TimeoutException as exc:
            raise LLMTimeout(str(exc)) from exc
        except httpx.HTTPError as exc:
            raise LLMError(str(exc)) from exc

        if response.status_code >= 400:
            raise LLMError(f"{response.status_code}: {response.text[:300]}")

        blocks = response.json().get("content", [])
        return "".join(b.get("text", "") for b in blocks if b.get("type") == "text")


class OpenAIClient(LLMClient):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        self._api_key = api_key
        self._model = model

    def complete(self, prompt, *, system="", temperature=0.2,
                 max_tokens=1500, timeout=6.0) -> str:
        import httpx

        messages = ([{"role": "system", "content": system}] if system else []) + [
            {"role": "user", "content": prompt}
        ]
        try:
            response = httpx.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {self._api_key}"},
                json={
                    "model": self._model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "response_format": {"type": "json_object"},
                },
                timeout=timeout,
            )
        except httpx.TimeoutException as exc:
            raise LLMTimeout(str(exc)) from exc
        except httpx.HTTPError as exc:
            raise LLMError(str(exc)) from exc

        if response.status_code >= 400:
            raise LLMError(f"{response.status_code}: {response.text[:300]}")
        return response.json()["choices"][0]["message"]["content"]


class OpenAICompatibleClient(LLMClient):
    """Generic OpenAI-compatible client (NVIDIA NIM, xAI Grok, Local Ollama, etc.)."""
    def __init__(self, api_key: str, base_url: str = "https://integrate.api.nvidia.com/v1",
                 model: str = "nvidia/nemotron-3-ultra-550b-a55b") -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._model = model

    def complete(self, prompt, *, system="", temperature=0.2,
                 max_tokens=1500, timeout=8.0) -> str:
        import httpx

        messages = ([{"role": "system", "content": system}] if system else []) + [
            {"role": "user", "content": prompt}
        ]
        body = {
            "model": self._model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        try:
            response = httpx.post(
                f"{self._base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"},
                json=body,
                timeout=timeout,
            )
        except httpx.TimeoutException as exc:
            raise LLMTimeout(str(exc)) from exc
        except httpx.HTTPError as exc:
            raise LLMError(str(exc)) from exc

        if response.status_code >= 400:
            raise LLMError(f"{response.status_code}: {response.text[:300]}")
        data = response.json()
        msg = data["choices"][0]["message"]
        content = msg.get("content") or msg.get("reasoning_content") or ""
        return content


def get_llm_client() -> LLMClient:
    provider = os.getenv("LLM_PROVIDER", "").lower()

    # 1. Check NVIDIA Tutor / General keys first if configured
    tutor_keys: list[str] = []
    for idx in range(1, 10):
        val = (os.getenv(f"NVIDIA_TUTOR_KEY_{idx}") or os.getenv(f"NVIDIA_TUTOR_API_KEY_{idx}") or "").strip()
        if val and val not in tutor_keys:
            tutor_keys.append(val)
    raw_tutor = (os.getenv("NVIDIA_TUTOR_API_KEYS") or os.getenv("NVIDIA_TUTOR_API_KEY") or "").strip()
    for k in raw_tutor.split(","):
        k = k.strip()
        if k and k not in tutor_keys:
            tutor_keys.append(k)
    nkey = (tutor_keys[0] if tutor_keys else None) or os.getenv("NVIDIA_API_KEY")
    if provider == "nvidia" or (not provider and nkey):
        base = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
        model = os.getenv("NVIDIA_MODEL", "nvidia/nemotron-3-ultra-550b-a55b")
        if not nkey:
            raise LLMError("NVIDIA_TUTOR_API_KEYS or NVIDIA_API_KEY is not set")
        return OpenAICompatibleClient(api_key=nkey, base_url=base, model=model)

    if provider == "anthropic":
        key = os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise LLMError("ANTHROPIC_API_KEY is not set")
        return AnthropicClient(key, os.getenv("LLM_MODEL", "claude-sonnet-4-6"))
    if provider == "openai":
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise LLMError("OPENAI_API_KEY is not set")
        return OpenAIClient(key, os.getenv("LLM_MODEL", "gpt-4o-mini"))
    if nkey:
        base = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
        model = os.getenv("NVIDIA_MODEL", "nvidia/nemotron-3-ultra-550b-a55b")
        return OpenAICompatibleClient(api_key=nkey, base_url=base, model=model)
    raise LLMError(f"unknown LLM_PROVIDER: {provider or 'none'}")
