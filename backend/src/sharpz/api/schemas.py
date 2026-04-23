"""Request/response schemas for the Intake API.

Follows docs/intake-api-contract.md. Kept separate from SQLModel table
classes because the wire format is permissive (partial PATCH allowed)
while the DB schema has defaults + non-null constraints.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from sharpz.models.enums import IntakeStatus, Tier


class IntakeCreate(BaseModel):
    """Body of POST /api/intakes. All fields optional — a blank intake
    is valid as a draft."""

    model_config = ConfigDict(extra="ignore")

    company_name: str = ""
    contact_name: str = ""
    contact_email: str = ""
    contact_role: str = ""
    test_type_preference: str = ""
    test_title: str = ""


class IntakeUpdate(BaseModel):
    """Body of PATCH /api/intakes/:id. All fields optional; only provided
    ones are applied (merge semantics)."""

    model_config = ConfigDict(extra="ignore")

    company_name: str | None = None
    contact_name: str | None = None
    contact_email: str | None = None
    contact_role: str | None = None

    test_type_preference: str | None = None
    test_title: str | None = None

    test_objective: str | None = None
    decision_context: str | None = None
    test_type_specific: dict[str, Any] | None = None

    product_name: str | None = None
    product_description: str | None = None
    launch_timing: str | None = None
    brand_positioning: str | None = None
    key_competitors: list[str] | None = None
    markets: list[str] | None = None
    key_facts_global: dict[str, str] | None = None

    scenario: dict[str, Any] | None = None

    target_audience_description: str | None = None
    desired_archetypes: list[dict[str, Any]] | None = None
    must_include_archetypes: list[str] | None = None
    must_exclude_archetypes: list[str] | None = None
    audience_size_hint: int | None = None

    hypotheses: list[str] | None = None
    success_metrics: list[str] | None = None
    expected_risks: str | None = None

    variants: list[dict[str, Any]] | None = None

    client_logo_url: str | None = None
    client_primary_color: str | None = None
    sensitive_topics_to_avoid: str | None = None
    legal_constraints: str | None = None
    reference_urls: list[str] | None = None

    tier_selected: Tier | None = None


class IntakeRead(BaseModel):
    """Response shape — full intake as seen by client or operator."""

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: str
    status: IntakeStatus
    company_name: str
    contact_name: str
    contact_email: str
    contact_role: str
    test_type_preference: str
    test_title: str
    test_objective: str
    decision_context: str
    test_type_specific: dict[str, Any]
    product_name: str
    product_description: str
    launch_timing: str
    brand_positioning: str
    key_competitors: list[str]
    markets: list[str]
    key_facts_global: dict[str, str]
    scenario: dict[str, Any]
    target_audience_description: str
    desired_archetypes: list[dict[str, Any]]
    must_include_archetypes: list[str]
    must_exclude_archetypes: list[str]
    audience_size_hint: int
    hypotheses: list[str]
    success_metrics: list[str]
    expected_risks: str
    variants: list[dict[str, Any]]
    client_logo_url: str
    client_primary_color: str
    sensitive_topics_to_avoid: str
    legal_constraints: str
    reference_urls: list[str]
    tier_selected: Tier | None
    payment_status: str | None
    operator_rejection_reason: str | None
    created_at: datetime
    updated_at: datetime
    submitted_at: datetime | None


class IntakeSubmitResponse(BaseModel):
    id: str
    status: IntakeStatus
    submitted_at: datetime | None
    test_id: str | None = None
    next_action: str = Field(
        description="await_payment | await_operator_approval | approved"
    )


class IntakeSubmitError(BaseModel):
    errors: list[str]


class OperatorRejectBody(BaseModel):
    reason: str = Field(min_length=10, max_length=2000)


class IntakeListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    status: IntakeStatus
    company_name: str
    contact_name: str
    test_type_preference: str
    test_title: str
    tier_selected: Tier | None
    created_at: datetime
    updated_at: datetime
    submitted_at: datetime | None
