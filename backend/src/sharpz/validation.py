"""Intake validation rules — docs/intake-api-contract.md section 4.

Drafts are permissive (auto-save tolerant). At submit time we enforce DNA-driven
constraints. Returns a list of human-readable error strings; empty = OK.
"""

from sharpz.dna import DNALoadError, get_dna
from sharpz.models.intake import Intake

_MIN_BRIEF_WORDS = 50
_MIN_PRODUCT_DESCRIPTION_CHARS = 100


def _words(text: str) -> int:
    return len([w for w in text.split() if w])


def validate_intake_submit(intake: Intake) -> list[str]:
    """Validate an intake for submission. Returns list of error messages."""
    errors: list[str] = []

    # Contact
    if not intake.company_name.strip():
        errors.append("company_name is required")
    if not intake.contact_name.strip():
        errors.append("contact_name is required")
    if not intake.contact_email.strip() or "@" not in intake.contact_email:
        errors.append("contact_email must be a valid email")

    # Test type
    if not intake.test_type_preference:
        errors.append("test_type_preference is required")
        return errors  # no point continuing without a type

    try:
        dna = get_dna(intake.test_type_preference)
    except DNALoadError as exc:
        errors.append(f"unknown test_type: {exc}")
        return errors

    if dna.get("status") != "active":
        errors.append(
            f"test_type {intake.test_type_preference!r} is not active "
            f"(status={dna.get('status')!r})"
        )

    # Title + brief + product
    if not intake.test_title.strip():
        errors.append("test_title is required")
    if len(intake.test_title) > 120:
        errors.append("test_title must be ≤ 120 characters")

    if _words(intake.test_objective) < _MIN_BRIEF_WORDS:
        errors.append(
            f"test_objective is too short (need ≥ {_MIN_BRIEF_WORDS} words, "
            f"got {_words(intake.test_objective)})"
        )

    if len(intake.product_description) < _MIN_PRODUCT_DESCRIPTION_CHARS:
        errors.append(
            f"product_description is too short (need ≥ {_MIN_PRODUCT_DESCRIPTION_CHARS} chars)"
        )

    # Archetypes (from panel.anchors_spec.count)
    anchors_spec = dna.get("panel", {}).get("anchors_spec", {})
    count_spec = anchors_spec.get("count", {})
    min_anchors = count_spec.get("min", 4)
    max_anchors = count_spec.get("max", 10)
    n_arch = len(intake.desired_archetypes)
    if n_arch < min_anchors:
        errors.append(f"need ≥ {min_anchors} desired_archetypes (got {n_arch})")
    if n_arch > max_anchors:
        errors.append(f"max {max_anchors} desired_archetypes (got {n_arch})")

    # Variants (from stimulus.variants_min / variants_max)
    stim = dna.get("stimulus", {})
    variants_min = stim.get("variants_min")
    variants_max = stim.get("variants_max")
    if variants_min is not None and len(intake.variants) < variants_min:
        errors.append(f"need ≥ {variants_min} variants (got {len(intake.variants)})")
    if variants_max is not None and len(intake.variants) > variants_max:
        errors.append(f"max {variants_max} variants (got {len(intake.variants)})")

    # Audience size hint vs DNA max
    sim = dna.get("simulation", {})
    panel_size = sim.get("panel_size", {})
    sim_max = panel_size.get("max")
    if sim_max is not None and intake.audience_size_hint > sim_max:
        errors.append(
            f"audience_size_hint={intake.audience_size_hint} exceeds DNA max {sim_max}"
        )

    return errors
