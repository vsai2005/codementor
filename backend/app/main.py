"""FastAPI application entry point (Phase 2)."""

from __future__ import annotations

import logging
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

from app.api.routes import auth, learning, problems, progress, submissions, tutor
from app.api.routes.sap import sap_router
from contextlib import asynccontextmanager
from sqlalchemy import text
from app.config import get_settings
from app.core.request_limits import BodySizeLimitMiddleware
from app.database import engine
from app.services.ratelimit import RateLimiterUnavailable
from app.schemas.api import HealthResponse

logging.basicConfig(level=logging.INFO)
settings = get_settings()

origins = settings.cors_origin_list
if "*" in origins:
    raise RuntimeError(
        "CORS misconfiguration: allow_origins cannot contain '*' when allow_credentials=True"
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Verify DB connectivity on boot in production
    if settings.is_production:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logging.info("Database connectivity check passed.")
        except Exception as exc:
            logging.error("Database connection check failed on startup: %s", exc)
            raise RuntimeError(f"Database connection check failed on startup: {exc}") from exc
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)

# Added before CORS so CORS stays outermost and 413/400 rejections still carry CORS headers.
app.add_middleware(BodySizeLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

for router in (auth.router, learning.router, problems.router, submissions.router,
               progress.router, tutor.router):
    app.include_router(router)
app.include_router(sap_router)


@app.exception_handler(OperationalError)
def _db_down(request: Request, exc: OperationalError) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"detail": "Database unavailable. Your code is saved locally — retry shortly.",
                 "retry_after_s": 5},
        headers={"Retry-After": "5"},
    )


@app.exception_handler(RateLimiterUnavailable)
def _rate_limiter_down(request: Request, exc: RateLimiterUnavailable) -> JSONResponse:
    # Fail closed (Redis is mandatory in production); never expose backend error details.
    logging.getLogger(__name__).error("rate limiter unavailable: %r", exc.__cause__)
    return JSONResponse(
        status_code=503,
        content={"detail": "Service temporarily unavailable. Please retry shortly.", "retry_after_s": 5},
        headers={"Retry-After": "5"},
    )


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")
