"""Operator-facing endpoints: queue, approve, reject, list.

All endpoints require X-Sharpz-Sync-Key header. In m3 we replace with JWT
session auth tied to an Operator model.
"""

from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import desc, select

from sharpz.api.deps import SessionDep, SyncKeyDep
from sharpz.api.schemas import IntakeListItem, IntakeRead, OperatorRejectBody
from sharpz.dna import get_dna
from sharpz.models.enums import IntakeStatus, TestStatus, Tier
from sharpz.models.intake import Intake
from sharpz.models.test import Test

router = APIRouter(prefix="/api/operator", tags=["operator"])


def _utcnow() -> datetime:
    return datetime.now(UTC)


@router.get("/intakes", response_model=list[IntakeListItem], dependencies=[SyncKeyDep])
async def list_intakes(
    session: SessionDep,
    status_filter: Annotated[IntakeStatus | None, Query(alias="status")] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
) -> list[Intake]:
    stmt = select(Intake).order_by(desc(Intake.updated_at)).limit(limit)
    if status_filter is not None:
        stmt = stmt.where(Intake.status == status_filter)
    result = await session.execute(stmt)
    return list(result.scalars().all())


@router.post(
    "/intakes/{intake_id}/approve",
    response_model=IntakeRead,
    dependencies=[SyncKeyDep],
)
async def approve_intake(intake_id: str, session: SessionDep) -> Intake:
    intake = await _load_intake(session, intake_id)
    if intake.status != IntakeStatus.SUBMITTED:
        raise HTTPException(
            status_code=409,
            detail=f"only submitted intakes can be approved (got {intake.status.value})",
        )

    now = _utcnow()
    intake.status = IntakeStatus.APPROVED
    intake.updated_at = now

    # Create the Test record with a snapshot of the DNA
    dna = get_dna(intake.test_type_preference)
    tier = intake.tier_selected or Tier.PRO
    cost_cap_map = {
        Tier.ECONOMY: 25.0,
        Tier.PRO: 60.0,
        Tier.PREMIUM: 120.0,
        Tier.ULTRA: 300.0,
    }
    test = Test(
        intake_id=intake.id,
        status=TestStatus.VALIDATED,
        tier=tier,
        test_type=intake.test_type_preference,
        dna_snapshot=dna,
        dna_version=dna.get("version", ""),
        cost_cap_usd=cost_cap_map[tier],
    )
    session.add(test)
    session.add(intake)
    await session.flush()
    await session.refresh(intake)
    return intake


@router.post(
    "/intakes/{intake_id}/reject",
    response_model=IntakeRead,
    dependencies=[SyncKeyDep],
)
async def reject_intake(
    intake_id: str, body: OperatorRejectBody, session: SessionDep
) -> Intake:
    intake = await _load_intake(session, intake_id)
    if intake.status != IntakeStatus.SUBMITTED:
        raise HTTPException(
            status_code=409,
            detail=f"only submitted intakes can be rejected (got {intake.status.value})",
        )
    intake.status = IntakeStatus.REJECTED
    intake.operator_rejection_reason = body.reason
    intake.updated_at = _utcnow()
    session.add(intake)
    await session.flush()
    await session.refresh(intake)
    return intake


async def _load_intake(session: SessionDep, intake_id: str) -> Intake:
    result = await session.execute(select(Intake).where(Intake.id == intake_id))
    intake = result.scalar_one_or_none()
    if intake is None:
        raise HTTPException(status_code=404, detail=f"intake {intake_id} not found")
    return intake
