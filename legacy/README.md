# legacy/

Archived code that is **not** part of the running product.

- `dev_backend/` — the old stdlib-only dev server (in-memory demo auth, no Postgres). It has
  been superseded by `backend/` (FastAPI), which is the only active backend and the only one
  deployed (`render.yaml`, `docker-compose.yml`, `backend/Dockerfile`).

Nothing in `backend/`, `frontend/`, CI or deployment config imports or runs anything here.
It is retained only because several one-off scripts in `scratch/` import
`legacy.dev_backend.server` to read the seed problem bank. Run those from the repo root.
Do not add features here; delete this directory once those scripts are retired.
