from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_policy_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_implementation_and_tests_to_repository_bytes():
    out = review.pair06_v9_strict_visible_contact_policy_review_contract()

    assert out["implementation_path"] == review.IMPLEMENTATION_PATH
    assert out["implementation_git_blob"] == review.IMPLEMENTATION_GIT_BLOB
    assert out["implementation_test_path"] == review.IMPLEMENTATION_TEST_PATH
    assert (
        out["implementation_test_git_blob"]
        == review.IMPLEMENTATION_TEST_GIT_BLOB
    )

    assert (
        _git_blob_sha1((ROOT / review.IMPLEMENTATION_PATH).read_bytes())
        == review.IMPLEMENTATION_GIT_BLOB
    )
    assert (
        _git_blob_sha1((ROOT / review.IMPLEMENTATION_TEST_PATH).read_bytes())
        == review.IMPLEMENTATION_TEST_GIT_BLOB
    )


def test_one_byte_implementation_drift_breaks_blob_identity():
    raw = (ROOT / review.IMPLEMENTATION_PATH).read_bytes()
    assert _git_blob_sha1(raw) == review.IMPLEMENTATION_GIT_BLOB

    mutated = raw[:-1] + bytes([raw[-1] ^ 1])
    assert _git_blob_sha1(mutated) != review.IMPLEMENTATION_GIT_BLOB


def test_review_closes_coherent_pure_implementation_frontier():
    out = review.pair06_v9_strict_visible_contact_policy_review_contract()

    assert out["pair06_v9_strict_visible_contact_policy_reviewed"] is True
    assert out["implementation_layer"] == (
        "pure_pre_inference_coherent_tool_surface_transform"
    )
    assert out["recovery_mode_shape_preserved"] is True
    assert out["normal_mode_identity_preserved"] is True
    assert out["strict_visible_contact_reinforcement_suppressed"] is True
    assert out["strict_visible_contact_engagement_and_controls_only"] is True
    assert out["production_functions_filtered_to_offered_surface"] is True
    assert out["legal_buildings_reconstructed_from_remaining_production"] is True
    assert out["legal_units_reconstructed_from_remaining_production"] is True
    assert out["translator_legal_building_mapping_invariant_required"] is True
    assert out["translator_legal_unit_mapping_invariant_required"] is True
    assert out["normal_mode_contract_identity_required"] is True
    assert out["v8_v1_v2_coherence_invariants_incorporated"] is True
    assert out["host_validation_unchanged"] is True
    assert out["runtime_integration_implemented"] is False
    assert out["new_execution_request_opened"] is False


@pytest.mark.parametrize(
    "field",
    (
        "runtime_execution_authorized",
        "replay_authorized",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ),
)
def test_review_grants_no_follow_on_authority(field):
    out = review.pair06_v9_strict_visible_contact_policy_review_contract()
    assert out[field] is False


def test_review_advances_only_to_runtime_integration():
    out = review.pair06_v9_strict_visible_contact_policy_review_contract()

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_RUNTIME_INTEGRATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_POLICY_RUNTIME_INTEGRATION_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_pair06_v9_strict_visible_contact_runtime_integration"
    )


def test_integrate_or_execute_holds():
    with pytest.raises(
        review.Pair06V9StrictVisibleContactPolicyReviewHold,
        match="POLICY_RUNTIME_INTEGRATION_REQUIRED",
    ):
        review.integrate_or_execute()
