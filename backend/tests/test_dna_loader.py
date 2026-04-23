"""DNA loader sanity tests."""

import pytest

from sharpz.dna import DNALoadError, get_dna, list_active_test_types, load_all_dnas

EXPECTED_ACTIVE_TEST_TYPES = {
    "investor_pitch",
    "pricing_test",
    "crisis_response",
    "creative_test",
    "narrative_framing",
    "brand_sentiment_shift",
    "competitive_response",
    "controversial_launch",
    "product_launch",
    "campaign_planning",
    "churn_analysis",
    "electoral_sentiment",
    "policy_rollout",
    "audience_targeting",
    "b2b_pricing",
}


def test_load_all_dnas_finds_all_fifteen():
    dnas = load_all_dnas()
    assert set(dnas.keys()) == EXPECTED_ACTIVE_TEST_TYPES
    assert len(dnas) == 15


def test_list_active_test_types_matches_yaml_status():
    active = list_active_test_types()
    assert set(active) == EXPECTED_ACTIVE_TEST_TYPES


def test_get_dna_unknown_raises():
    with pytest.raises(DNALoadError):
        get_dna("not_a_real_test_type")


def test_investor_pitch_has_expected_shape():
    dna = get_dna("investor_pitch")
    assert dna["test_type"] == "investor_pitch"
    assert dna["simulation"]["mode"] == "deliberation"
    assert dna["venue"]["reference"].endswith("pitch_meeting.yaml")


def test_pricing_test_is_survey_batch():
    dna = get_dna("pricing_test")
    assert dna["simulation"]["mode"] == "survey_batch"
    assert dna["simulation"]["rounds"] == 1


def test_crisis_response_is_deliberation_hybrid():
    dna = get_dna("crisis_response")
    assert dna["simulation"]["mode"] == "deliberation"
    assert dna["venue"]["reference"].endswith("split_public_private.yaml")
