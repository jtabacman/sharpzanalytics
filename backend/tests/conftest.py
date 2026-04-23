"""Pytest fixtures — in-memory async SQLite for fast isolated tests.

Production DB is Postgres; for unit tests we use aiosqlite which is
schema-compatible for our usage (JSONB → JSON on sqlite transparently
via sqlalchemy).
"""

import os
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

# Force test DB before importing app
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("SHARPZ_SYNC_KEY", "test-sync-key")

from sharpz import db as db_module  # noqa: E402
from sharpz import models  # noqa: E402,F401 — registers tables
from sharpz.main import app  # noqa: E402


@pytest_asyncio.fixture
async def test_engine() -> AsyncIterator:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session(test_engine) -> AsyncIterator[AsyncSession]:
    factory = async_sessionmaker(bind=test_engine, expire_on_commit=False, class_=AsyncSession)
    async with factory() as s:
        yield s


@pytest_asyncio.fixture
async def client(test_engine) -> AsyncIterator[AsyncClient]:
    # Swap the app-level session factory to our test engine
    factory = async_sessionmaker(bind=test_engine, expire_on_commit=False, class_=AsyncSession)
    db_module.async_session_factory = factory  # type: ignore[assignment]
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def op_headers() -> dict[str, str]:
    return {"X-Sharpz-Sync-Key": "test-sync-key"}
