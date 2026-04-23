"""FastAPI entry point — Sharpz V2 backend."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sharpz import __version__
from sharpz.config import settings

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    logger.info("starting", version=__version__, env=settings.env)
    yield
    logger.info("shutting down")


app = FastAPI(
    title="Sharpz Analytics API",
    version=__version__,
    description="Backend API for synthetic buyer panel testing platform.",
    lifespan=lifespan,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__, "env": settings.env}


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "service": "sharpz-analytics",
        "version": __version__,
        "docs": "/docs" if not settings.is_production else "disabled",
    }
