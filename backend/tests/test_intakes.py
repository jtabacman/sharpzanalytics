"""Intake API contract tests."""

from typing import Any

import pytest


async def _create_empty(client) -> str:
    r = await client.post("/api/intakes", json={})
    assert r.status_code == 201, r.text
    return r.json()["id"]


@pytest.mark.asyncio
async def test_create_get_draft(client):
    r = await client.post(
        "/api/intakes",
        json={"company_name": "TIAA", "contact_email": "ops@example.com"},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["id"].startswith("in_")
    assert body["status"] == "draft"
    assert body["company_name"] == "TIAA"

    r2 = await client.get(f"/api/intakes/{body['id']}")
    assert r2.status_code == 200
    assert r2.json()["id"] == body["id"]


@pytest.mark.asyncio
async def test_patch_autosave_merges(client):
    intake_id = await _create_empty(client)

    r = await client.patch(
        f"/api/intakes/{intake_id}",
        json={"test_title": "Test A", "markets": ["US", "AR"]},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["test_title"] == "Test A"
    assert body["markets"] == ["US", "AR"]


@pytest.mark.asyncio
async def test_submit_rejects_incomplete(client):
    intake_id = await _create_empty(client)
    r = await client.post(f"/api/intakes/{intake_id}/submit")
    assert r.status_code == 400
    errors: list[str] = r.json()["detail"]["errors"]
    assert any("company_name" in e for e in errors)
    assert any("test_type" in e for e in errors)


@pytest.mark.asyncio
async def test_submit_rejects_unknown_test_type(client):
    intake_id = await _create_empty(client)
    await client.patch(
        f"/api/intakes/{intake_id}",
        json={
            "company_name": "Acme",
            "contact_name": "Jane",
            "contact_email": "jane@acme.com",
            "test_type_preference": "not_a_real_test",
            "test_title": "x",
        },
    )
    r = await client.post(f"/api/intakes/{intake_id}/submit")
    assert r.status_code == 400
    errors: list[str] = r.json()["detail"]["errors"]
    assert any("unknown test_type" in e for e in errors)


def _valid_investor_pitch_payload() -> dict[str, Any]:
    """Minimum payload that should pass validation for investor_pitch."""
    return {
        "company_name": "Invernea Fund III",
        "contact_name": "Julian Tabacman",
        "contact_email": "jt@invernea.com",
        "contact_role": "GP",
        "test_type_preference": "investor_pitch",
        "test_title": "Invernea Fund III · pre-roadshow DD test",
        "test_objective": (
            "We want to validate whether our Fund III pitch deck is ready for "
            "roadshow to institutional LPs, specifically identifying which red "
            "flags we should address before meetings with US endowments and "
            "sovereign wealth funds focused on food security mandates."
        ),
        "product_description": (
            "Invernea is an Argentine agri PE fund raising a $300M Fund III "
            "focused on row-crop and cattle operations across the Pampas. "
            "Our thesis combines land appreciation with productivity upgrades "
            "via tech-enabled management. Fund II delivered 18% net IRR."
        ),
        "desired_archetypes": [
            {"name": "TIAA-Nuveen agri specialist", "short_label": "TIAA"},
            {"name": "Manulife IM real assets", "short_label": "Manulife"},
            {"name": "Harvard endowment", "short_label": "Harvard"},
            {"name": "Mubadala food security", "short_label": "Mubadala"},
            {"name": "Brazilian family office", "short_label": "BR-FO"},
            {"name": "DFI (IFC/IDB Invest)", "short_label": "DFI"},
        ],
        "audience_size_hint": 48,
        "variants": [
            {"name": "Current deck v12", "description": "Unchanged from last revision."},
            {"name": "Reworked with slide 12 detail", "description": "Adds carry waterfall."},
        ],
    }


@pytest.mark.asyncio
async def test_submit_happy_path(client):
    intake_id = await _create_empty(client)
    await client.patch(f"/api/intakes/{intake_id}", json=_valid_investor_pitch_payload())
    r = await client.post(f"/api/intakes/{intake_id}/submit")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["status"] == "submitted"
    assert body["next_action"] == "await_operator_approval"


@pytest.mark.asyncio
async def test_submit_is_idempotent(client):
    intake_id = await _create_empty(client)
    await client.patch(f"/api/intakes/{intake_id}", json=_valid_investor_pitch_payload())
    r1 = await client.post(f"/api/intakes/{intake_id}/submit")
    assert r1.status_code == 200
    r2 = await client.post(f"/api/intakes/{intake_id}/submit")
    assert r2.status_code == 200
    assert r1.json()["submitted_at"] == r2.json()["submitted_at"]


@pytest.mark.asyncio
async def test_cannot_patch_submitted_intake(client):
    intake_id = await _create_empty(client)
    await client.patch(f"/api/intakes/{intake_id}", json=_valid_investor_pitch_payload())
    await client.post(f"/api/intakes/{intake_id}/submit")
    r = await client.patch(f"/api/intakes/{intake_id}", json={"test_title": "Updated"})
    assert r.status_code == 409


@pytest.mark.asyncio
async def test_operator_list_requires_auth(client):
    r = await client.get("/api/operator/intakes")
    assert r.status_code == 401


@pytest.mark.asyncio
async def test_operator_approve_creates_test(client, op_headers):
    intake_id = await _create_empty(client)
    await client.patch(f"/api/intakes/{intake_id}", json=_valid_investor_pitch_payload())
    await client.post(f"/api/intakes/{intake_id}/submit")

    r = await client.post(
        f"/api/operator/intakes/{intake_id}/approve", headers=op_headers
    )
    assert r.status_code == 200, r.text
    assert r.json()["status"] == "approved"


@pytest.mark.asyncio
async def test_operator_reject_returns_to_draft_on_next_patch(client, op_headers):
    intake_id = await _create_empty(client)
    await client.patch(f"/api/intakes/{intake_id}", json=_valid_investor_pitch_payload())
    await client.post(f"/api/intakes/{intake_id}/submit")

    r = await client.post(
        f"/api/operator/intakes/{intake_id}/reject",
        headers=op_headers,
        json={"reason": "Need more detail on fund structure and carry waterfall."},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "rejected"

    # Editing a rejected intake returns it to draft
    r2 = await client.patch(
        f"/api/intakes/{intake_id}", json={"decision_context": "Addressed."}
    )
    assert r2.status_code == 200
    assert r2.json()["status"] == "draft"
