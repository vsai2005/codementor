"""FastAPI application entry point (Phase 2)."""

from __future__ import annotations

import logging
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

from app.api.routes import auth, learning, problems, progress, submissions, tutor
from app.config import get_settings
from app.schemas.api import HealthResponse

logging.basicConfig(level=logging.INFO)
settings = get_settings()

origins = settings.cors_origin_list
if "*" in origins:
    raise RuntimeError(
        "CORS misconfiguration: allow_origins cannot contain '*' when allow_credentials=True"
    )

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Cookie"],
)

for router in (auth.router, learning.router, problems.router, submissions.router,
               progress.router, tutor.router):
    app.include_router(router)


@app.exception_handler(OperationalError)
def _db_down(request: Request, exc: OperationalError) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"detail": "Database unavailable. Your code is saved locally — retry shortly.",
                 "retry_after_s": 5},
        headers={"Retry-After": "5"},
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")
