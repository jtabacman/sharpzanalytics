"""Test model — pipeline run associated with an approved Intake.

m1 scope: basic shell with DNA snapshot + status + cost tracking. Stage 2+
will extend with relationships (Environment, Variant, Simulation, ...).
"""

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

from sharpz.models.enums import TestStatus, Tier


def _utcnow() -> datetime:
    return datetime.now(UTC)


def _new_test_id() -> str:
    return f"test_{uuid4().hex[:16]}"


class Test(SQLModel, table=True):
    """A pipeline run. Created when operator approves an Intake.

    The DNA snapshot (dna_snapshot) is immutable — embedded at creation
    time so re-runs / replays use the same declarative config even if the
    DNA file evolves. This is the reproducibility guarantee from
    docs/dna-spec.md section 7.
    """

    __tablename__ = "test"

    id: str = Field(default_factory=_new_test_id, primary_key=True, max_length=32)
    intake_id: str = Field(
        sa_column=Column(ForeignKey("intake.id", ondelete="RESTRICT"), nullable=False, index=True)
    )
    status: TestStatus = Field(default=TestStatus.DRAFT, index=True)
    tier: Tier = Field(default=Tier.PRO)
    test_type: str = Field(max_length=60, index=True)

    # Immutable snapshot of the DNA YAML as of test creation
    dna_snapshot: dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSONB, nullable=False)
    )
    dna_version: str = Field(default="", max_length=20)

    # Cost tracking
    cost_usd_accumulated: float = Field(default=0.0)
    cost_cap_usd: float = Field(default=60.0)

    # Warnings surfaced during pipeline (for final report caveats)
    warnings: list[dict[str, Any]] = Field(
        default_factory=list, sa_column=Column(JSONB, nullable=False, server_default="[]")
    )

    # Halt info (when status in {HALTED_ALERT, HALTED_ABORT})
    halt_stage: int | None = Field(default=None)
    halt_reason: str | None = Field(default=None)
    halt_escalation_context: dict[str, Any] | None = Field(
        default=None, sa_column=Column(JSONB, nullable=True)
    )

    # Output references (populated across stages)
    report_url: str | None = Field(default=None, max_length=500)
    report_jwt: str | None = Field(default=None, max_length=500)
    one_pager_md: str | None = Field(default=None)

    # Timestamps
    created_at: datetime = Field(
        default_factory=_utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False, index=True),
    )
    updated_at: datetime = Field(
        default_factory=_utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    started_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True), nullable=True)
    )
    completed_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True), nullable=True)
    )

    __table_args__ = (
        Index("ix_test_status_created", "status", "created_at"),
    )
