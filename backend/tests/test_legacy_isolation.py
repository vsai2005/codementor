"""Archived code under legacy/ must never be reachable from the active backend or deploys.

These checks read repo-level files (deploy config, frontend config); they skip when the
tests are run from a bare backend copy that lacks them.
"""

import ast
import re
from pathlib import Path

import pytest

BACKEND = Path(__file__).resolve().parents[1]
REPO = BACKEND.parent
FORBIDDEN = re.compile(r"\b(legacy|dev_backend)\b")


def _python_files(root: Path):
    return [p for p in root.rglob("*.py") if "__pycache__" not in p.parts and ".venv" not in p.parts]


def _imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            modules.append(node.module)
    return modules


@pytest.mark.parametrize("subdir", ["app", "alembic"])
def test_active_backend_never_imports_legacy_code(subdir):
    offenders = [
        (str(p.relative_to(BACKEND)), m)
        for p in _python_files(BACKEND / subdir)
        for m in _imported_modules(p)
        if m.split(".")[0] in {"legacy", "dev_backend", "scratch"}
    ]
    assert offenders == []


def test_active_backend_never_touches_legacy_paths_or_sys_path():
    """No string literal in app/ or alembic/ points into legacy/ and nothing edits sys.path."""
    offenders = []
    for sub in ("app", "alembic"):
        for path in _python_files(BACKEND / sub):
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    if re.search(r"(^|[\/])(legacy|dev_backend)([\/]|$)", node.value):
                        offenders.append((path.name, node.value[:60]))
            if re.search(r"sys\.path", source):
                offenders.append((path.name, "sys.path access"))
    assert offenders == []


@pytest.mark.parametrize(
    "relative",
    ["render.yaml", "docker-compose.yml", "backend/Dockerfile", "frontend/vercel.json", "frontend/package.json"],
)
def test_deploy_and_build_config_never_reference_legacy(relative):
    path = REPO / relative
    if not path.exists():
        pytest.skip(f"{relative} not present in this checkout")
    assert FORBIDDEN.search(path.read_text(encoding="utf-8")) is None


def test_docker_image_copies_only_active_backend_sources():
    dockerfile = BACKEND / "Dockerfile"
    if not dockerfile.exists():
        pytest.skip("Dockerfile not present in this checkout")
    copied = [
        line.split()[1]
        for line in dockerfile.read_text(encoding="utf-8").splitlines()
        if line.strip().upper().startswith("COPY ")
    ]
    assert set(copied) <= {"requirements.txt", "app", "alembic", "alembic.ini"}


def test_render_starts_only_the_active_app():
    render = REPO / "render.yaml"
    if not render.exists():
        pytest.skip("render.yaml not present in this checkout")
    text = render.read_text(encoding="utf-8")
    assert "uvicorn app.main:app" in text
    assert "server.py" not in text


def test_legacy_directory_is_flagged_as_archived():
    readme = REPO / "legacy" / "README.md"
    server = REPO / "legacy" / "dev_backend" / "server.py"
    if not (readme.exists() and server.exists()):
        pytest.skip("legacy/ not present in this checkout")
    assert "Archived code" in readme.read_text(encoding="utf-8")
    assert "LEGACY / ARCHIVED" in server.read_text(encoding="utf-8")[:200]
