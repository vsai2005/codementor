"""Make the test process independent of the developer's machine configuration.

Two things leak developer configuration into tests:

* ``Settings`` reads ``.env`` from the current directory, and
* real process environment variables (``REDIS_URL``, ``JWT_SECRET``, LLM keys, ...),
  which both ``Settings`` and modules that call ``os.getenv`` directly pick up.

``isolate()`` removes both before any test module imports the app. Tests that need a
particular value set it themselves (``monkeypatch.setenv`` or explicit ``Settings(...)``
arguments). ``TEST_DATABASE_URL`` is not a setting, so it is preserved.
"""

from __future__ import annotations

import os
import re
from collections.abc import MutableMapping

# Variables read with os.getenv outside of Settings (see app/services/llm.py,
# embeddings.py, ratelimit.py, and app/config.py's ALLOWED_ORIGINS handling).
_DIRECT_ENV_NAMES = frozenset(
    {
        "ALLOWED_ORIGINS",
        "REDIS_URL",
        "LLM_PROVIDER",
        "LLM_MODEL",
        "EMBEDDING_MODEL",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "TUTOR_RATE_LIMIT",
        "TUTOR_RATE_WINDOW_S",
        "COACH_RATE_LIMIT",
        "COACH_RATE_WINDOW_S",
    }
)
# Families with numbered / suffixed variants (NVIDIA_TUTOR_KEY_1, NVIDIA_TUTOR_API_KEYS, ...).
_DIRECT_ENV_PATTERN = re.compile(r"^NVIDIA_[A-Z0-9_]+$")

_PRESERVED = frozenset({"TEST_DATABASE_URL"})


def settings_env_names() -> frozenset[str]:
    """Every environment variable name that ``Settings`` or the app reads for config."""
    from app.config import Settings

    names: set[str] = set(_DIRECT_ENV_NAMES)
    for field_name, field in Settings.model_fields.items():
        names.add(field_name.upper())
        alias = field.validation_alias
        choices = getattr(alias, "choices", None)
        if choices:
            names.update(str(c).upper() for c in choices)
        elif isinstance(alias, str):
            names.add(alias.upper())
    return frozenset(names)


def scrub_environ(environ: MutableMapping[str, str]) -> list[str]:
    """Delete configuration variables from ``environ``; return the names removed."""
    names = settings_env_names()
    removed = []
    for key in list(environ):
        upper = key.upper()
        if upper in _PRESERVED:
            continue
        if upper in names or _DIRECT_ENV_PATTERN.match(upper):
            del environ[key]
            removed.append(key)
    return removed


def isolate() -> None:
    """Apply isolation to this process. Call once, before the app is imported by tests."""
    from app.config import Settings, get_settings

    scrub_environ(os.environ)
    Settings.model_config["env_file"] = None
    get_settings.cache_clear()
