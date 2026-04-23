"""Shared FastAPI dependencies: auth, DB session."""

from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from sharpz.config import settings
from sharpz.db import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def require_sync_key(
    x_sharpz_sync_key: Annotated[str | None, Header()] = None,
) -> None:
    """Operator-only endpoints require a shared secret header."""
    expected = settings.sharpz_sync_key
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="operator endpoints disabled: SHARPZ_SYNC_KEY not configured",
        )
    if not x_sharpz_sync_key or x_sharpz_sync_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing or invalid X-Sharpz-Sync-Key header",
        )


SyncKeyDep = Annotated[None, Depends(require_sync_key)]
