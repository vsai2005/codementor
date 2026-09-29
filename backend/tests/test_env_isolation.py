"""The test suite must not depend on the developer's .env file or exported variables."""

import json
import os
import subprocess
import sys
from pathlib import Path

from app.config import Settings
from tests._env_isolation import scrub_environ, settings_env_names

BACKEND_DIR = Path(__file__).resolve().parents[1]

HOSTILE_ENV_FILE = (
    "ENVIRONMENT=staging\n"
    "REDIS_URL=redis://localhost:6379/0\n"
    "JWT_SECRET=hostile-dev-secret\n"
    "NVIDIA_API_KEY=nvapi-hostile\n"
)
HOSTILE_ENVIRON = {
    "REDIS_URL": "redis://localhost:6379/0",
    "JWT_SECRET": "hostile-exported-secret",
    "LLM_PROVIDER": "anthropic",
    "NVIDIA_TUTOR_KEY_1": "nvapi-hostile",
}

_PROBE = """
import json, os, sys
sys.path.insert(0, {backend!r})
if {isolate!r}:
    from tests._env_isolation import isolate
    isolate()
from app.config import Settings
s = Settings()
print(json.dumps({{
    "environment": s.environment,
    "redis_url": s.redis_url,
    "jwt_secret": s.jwt_secret,
    "nvidia_key_in_environ": "NVIDIA_TUTOR_KEY_1" in os.environ,
}}))
"""


def _run_probe(tmp_path: Path, *, isolate: bool) -> dict:
    (tmp_path / ".env").write_text(HOSTILE_ENV_FILE, encoding="utf-8")
    env = {k: v for k, v in os.environ.items() if k.upper() not in settings_env_names()}
    env.update(HOSTILE_ENVIRON)
    env["PYTHONPATH"] = str(BACKEND_DIR)
    out = subprocess.run(
        [sys.executable, "-c", _PROBE.format(backend=str(BACKEND_DIR), isolate=isolate)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert out.returncode == 0, out.stderr
    return json.loads(out.stdout.strip().splitlines()[-1])


def test_probe_without_isolation_sees_developer_config(tmp_path):
    """Control: proves the hostile .env / environment really would leak."""
    seen = _run_probe(tmp_path, isolate=False)
    assert seen["environment"] == "staging"
    assert seen["redis_url"] == "redis://localhost:6379/0"
    assert seen["jwt_secret"] != "change-me-in-production"
    assert seen["nvidia_key_in_environ"] is True


def test_isolation_hides_developer_dotenv_and_environment(tmp_path):
    seen = _run_probe(tmp_path, isolate=True)
    assert seen["environment"] == "development"
    assert seen["redis_url"] is None
    assert seen["jwt_secret"] == "change-me-in-production"
    assert seen["nvidia_key_in_environ"] is False


def test_settings_do_not_load_dotenv_in_this_process(tmp_path, monkeypatch):
    assert Settings.model_config.get("env_file") is None
    (tmp_path / ".env").write_text(HOSTILE_ENV_FILE, encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    settings = Settings(
        environment="production",
        jwt_secret="super-secret-random-jwt-key-with-sufficient-length-32",
        database_url="postgresql+psycopg://codementor:secret@db.render.com:5432/codementor",
        redis_url="rediss://default:password@upstash-redis.com:6379",
        proxy_shared_secret="p" * 40,
    )
    assert settings.redis_url == "rediss://default:password@upstash-redis.com:6379"


def test_scrub_environ_removes_only_configuration_variables():
    environ = {
        "REDIS_URL": "x",
        "redis_url": "x",
        "JWT_SECRET": "x",
        "ENVIRONMENT": "production",
        "ALLOWED_ORIGINS": "x",
        "OPENAI_API_KEY": "x",
        "NVIDIA_TUTOR_KEY_3": "x",
        "NVIDIA_TUTOR_API_KEYS": "x",
        "TEST_DATABASE_URL": "keep-me",
        "PATH": "keep-me",
        "UNRELATED": "keep-me",
    }
    removed = scrub_environ(environ)
    assert environ == {"TEST_DATABASE_URL": "keep-me", "PATH": "keep-me", "UNRELATED": "keep-me"}
    assert "REDIS_URL" in removed and "NVIDIA_TUTOR_KEY_3" in removed


def test_settings_env_names_cover_aliases_and_fields():
    names = settings_env_names()
    assert {"REDIS_URL", "JWT_SECRET", "ENVIRONMENT", "DATABASE_URL", "ALLOWED_ORIGINS"} <= names
