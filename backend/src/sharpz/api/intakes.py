"""Intake API — Stage 1 endpoints for the client-facing Vue SPA.

Contract: docs/intake-api-contract.md.
"""

from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from sharpz.api.deps import SessionDep
from sharpz.api.schemas import (
    IntakeCreate,
    IntakeRead,
    IntakeSubmitError,
    IntakeSubmitResponse,
    IntakeUpdate,
)
from sharpz.models.enums import IntakeStatus
from sharpz.models.intake import Intake
from sharpz.validation import validate_intake_submit

router = APIRouter(prefix="/api/intakes", tags=["intakes"])


def _utcnow() -> datetime:
    return datetime.now(UTC)


async def _load_or_404(session: SessionDep, intake_id: str) -> Intake:
    result = await session.execute(select(Intake).where(Intake.id == intake_id))
    intake = result.scalar_one_or_none()
    if intake is None:
        raise HTTPException(status_code=404, detail=f"intake {intake_id} not found")
    return intake


@router.post("", response_model=IntakeRead, status_code=status.HTTP_201_CREATED)
async def create_intake(body: IntakeCreate, session: SessionDep) -> Intake:
    intake = Intake(**body.model_dump())
    session.add(intake)
    await session.flush()
    await session.refresh(intake)
    return intake


@router.get("/{intake_id}", response_model=IntakeRead)
async def get_intake(intake_id: str, session: SessionDep) -> Intake:
    return await _load_or_404(session, intake_id)


@router.patch("/{intake_id}", response_model=IntakeRead)
async def update_intake(
    intake_id: str, body: IntakeUpdate, session: SessionDep
) -> Intake:
    intake = await _load_or_404(session, intake_id)
    if intake.status not in (IntakeStatus.DRAFT, IntakeStatus.REJECTED):
        raise HTTPException(
            status_code=409,
            detail=f"intake in status {intake.status.value} cannot be edited",
        )

    # If the intake was rejected, editing returns it to draft
    if intake.status == IntakeStatus.REJECTED:
        intake.status = IntakeStatus.DRAFT
        intake.operator_rejection_reason = None

    updates = body.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in updates.items():
        setattr(intake, key, value)
    intake.updated_at = _utcnow()

    session.add(intake)
    await session.flush()
    await session.refresh(intake)
    return intake


@router.post(
    "/{intake_id}/submit",
    response_model=IntakeSubmitResponse,
    responses={400: {"model": IntakeSubmitError}},
)
async def submit_intake(intake_id: str, session: SessionDep) -> IntakeSubmitResponse:
    intake = await _load_or_404(session, intake_id)

    if intake.status == IntakeStatus.SUBMITTED:
        # Idempotent: already submitted, return current state
        return IntakeSubmitResponse(
            id=intake.id,
            status=intake.status,
            submitted_at=intake.submitted_at,
            next_action="await_operator_approval",
        )

    if intake.status not in (IntakeStatus.DRAFT, IntakeStatus.REJECTED):
        raise HTTPException(
            status_code=409,
            detail=f"intake in status {intake.status.value} cannot be submitted",
        )

    errors = validate_intake_submit(intake)
    if errors:
        raise HTTPException(status_code=400, detail={"errors": errors})

    now = _utcnow()
    intake.status = IntakeStatus.SUBMITTED
    intake.submitted_at = now
    intake.updated_at = now
    session.add(intake)
    await session.flush()
    await session.refresh(intake)

    # v0 is manual payment — operator approves, no Stripe flow yet.
    return IntakeSubmitResponse(
        id=intake.id,
        status=intake.status,
        submitted_at=intake.submitted_at,
        test_id=None,
        next_action="await_operator_approval",
    )
