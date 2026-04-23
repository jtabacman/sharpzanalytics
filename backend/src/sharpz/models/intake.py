"""Intake model — form payload submitted by client."""

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import Column, DateTime, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

from sharpz.models.enums import IntakeStatus, Tier


def _utcnow() -> datetime:
    return datetime.now(UTC)


def _new_intake_id() -> str:
    return f"in_{uuid4().hex[:16]}"


class Intake(SQLModel, table=True):
    """Form payload as captured by the intake Vue SPA.

    Schema matches docs/intake-api-contract.md. Fields are permissive
    (most nullable) because drafts can be partial — validation strictens
    only at submit time.
    """

    __tablename__ = "intake"

    id: str = Field(default_factory=_new_intake_id, primary_key=True, max_length=32)
    status: IntakeStatus = Field(default=IntakeStatus.DRAFT, index=True)

    # Section 01 — Who writes
    company_name: str = Field(default="", max_length=200)
    contact_name: str = Field(default="", max_length=200)
    contact_email: str = Field(default="", max_length=320)
    contact_role: str = Field(default="", max_length=200)

    # Section 02 — Test type
    test_type_preference: str = Field(default="", max_length=60, index=True)
    test_title: str = Field(default="", max_length=200)

    # Section 03 — Objective
    test_objective: str = Field(default="", sa_column_kwargs={"nullable": False})
    decision_context: str = Field(default="")
    test_type_specific: dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSONB, nullable=False, server_default="{}")
    )

    # Section 04 — Product / brand
    product_name: str = Field(default="", max_length=200)
    product_description: str = Field(default="")
    launch_timing: str = Field(default="", max_length=100)
    brand_positioning: str = Field(default="")
    key_competitors: list[str] = Field(
        default_factory=list, sa_column=Column(JSONB, nullable=False, server_default="[]")
    )
    markets: list[str] = Field(
        default_factory=list, sa_column=Column(JSONB, nullable=False, server_default="[]")
    )
    key_facts_global: dict[str, str] = Field(
        default_factory=dict, sa_column=Column(JSONB, nullable=False, server_default="{}")
    )

    # Section 05 — Scenario (conditional)
    scenario: dict[str, Any] = Field(
        default_factory=dict, sa_column=Column(JSONB, nullable=False, server_default="{}")
    )

    # Section 06 — Audience
    target_audience_description: str = Field(default="")
    desired_archetypes: list[dict[str, Any]] = Field(
        default_factory=list, sa_column=Column(JSONB, nullable=False, server_default="[]")
    )
    must_include_archetypes: list[str] = Field(
        default_factory=list, sa_column=Column(JSONB, nullable=False, server_default="[]")
    )
    must_exclude_archetypes: list[str] = Field(
        default_factory=list, sa_column=Column(JSONB, nullable=False, server_default="[]")
    )
    audience_size_hint: int = Field(default=80)

    # Section 07 — Hypotheses
    hypotheses: list[str] = Field(
        default_factory=list, sa_column=Column(JSONB, nullable=False, server_default="[]")
    )
    success_metrics: list[str] = Field(
        default_factory=list, sa_column=Column(JSONB, nullable=False, server_default="[]")
    )
    expected_risks: str = Field(default="")

    # Section 08 — Variants
    variants: list[dict[str, Any]] = Field(
        default_factory=list, sa_column=Column(JSONB, nullable=False, server_default="[]")
    )

    # Section 09 — Branding
    client_logo_url: str = Field(default="", max_length=500)
    client_primary_color: str = Field(default="", max_length=20)
    sensitive_topics_to_avoid: str = Field(default="")
    legal_constraints: str = Field(default="")
    reference_urls: list[str] = Field(
        default_factory=list, sa_column=Column(JSONB, nullable=False, server_default="[]")
    )

    # Tier & payment (manual v0)
    tier_selected: Tier | None = Field(default=None)
    payment_status: str | None = Field(default=None, max_length=20)
    stripe_session_id: str | None = Field(default=None, max_length=120)

    # Rejection feedback (when status=rejected)
    operator_rejection_reason: str | None = Field(default=None)

    # Timestamps
    created_at: datetime = Field(
        default_factory=_utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False, index=True),
    )
    updated_at: datetime = Field(
        default_factory=_utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    submitted_at: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True), nullable=True)
    )

    __table_args__ = (
        Index("ix_intake_status_updated", "status", "updated_at"),
    )
