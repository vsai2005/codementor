"""LLM abstraction (PRD 5.6).

One interface, provider chosen by env var, so swapping Claude -> GPT -> local
is a config change. No FastAPI imports here.
"""

from __future__ import annotations

import json
import os
import re
from abc import ABC, abstractmethod
from typing import Any


class LLMError(RuntimeError):
    """Provider failure: timeout, transport error, refusal."""


class LLMTimeout(LLMError):
    pass


def extract_json(raw: str) -> dict[str, Any]:
    """Pull a JSON object out of a model response.

    Models wrap JSON in prose or fences even when told not to. Failing the
    whole review over a stray ```json is a self-inflicted wound, so we strip
    fences and fall back to the outermost brace pair before giving up.
    """
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
        return json.loads(text[start : end + 1])
    raise ValueError("no JSON object found in model response")


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


def get_llm_client() -> LLMClient:
    provider = os.getenv("LLM_PROVIDER", "anthropic").lower()
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
    raise LLMError(f"unknown LLM_PROVIDER: {provider}")
