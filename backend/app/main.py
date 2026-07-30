"""FastAPI application entry point."""

from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

from app.api.routes import auth, problems, progress, submissions, tutor
from app.config import get_settings
from app.schemas.api import HealthResponse

logging.basicConfig(level=logging.INFO)
settings = get_settings()

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,  # never "*" — PRD 6
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

for router in (auth.router, problems.router, submissions.router,
               progress.router, tutor.router):
    app.include_router(router)


@app.exception_handler(OperationalError)
def _db_down(request: Request, exc: OperationalError) -> JSONResponse:
    # PRD 5.7 — 503 with a retry hint; the client keeps the user's code.
    return JSONResponse(
        status_code=503,
        content={"detail": "Database unavailable. Your code is saved locally — retry shortly.",
                 "retry_after_s": 5},
        headers={"Retry-After": "5"},
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")
