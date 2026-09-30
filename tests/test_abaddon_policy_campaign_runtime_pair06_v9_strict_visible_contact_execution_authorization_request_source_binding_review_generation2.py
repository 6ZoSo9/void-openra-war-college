from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_execution_authorization_request_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_request_source_and_tests_to_repository_bytes():
    out = review.pair06_v9_execution_authorization_request_review_contract()

    assert out["request_path"] == review.REQUEST_PATH
    assert out["request_git_blob"] == review.REQUEST_GIT_BLOB
    assert out["request_test_path"] == review.REQUEST_TEST_PATH
    assert out["request_test_git_blob"] == review.REQUEST_TEST_GIT_BLOB

    assert (
        _git_blob_sha1((ROOT / review.REQUEST_PATH).read_bytes())
        == review.REQUEST_GIT_BLOB
    )
    assert (
        _git_blob_sha1((ROOT / review.REQUEST_TEST_PATH).read_bytes())
        == review.REQUEST_TEST_GIT_BLOB
    )


def test_one_byte_request_source_drift_breaks_blob_identity():
    raw = (ROOT / review.REQUEST_PATH).read_bytes()
    assert _git_blob_sha1(raw) == review.REQUEST_GIT_BLOB

    mutated = raw[:-1] + bytes([raw[-1] ^ 1])
    assert _git_blob_sha1(mutated) != review.REQUEST_GIT_BLOB


def test_review_binds_exact_request_digest_from_canonical_builder():
    out = review.pair06_v9_execution_authorization_request_review_contract()
    validated = out["validated_request"]

    assert out["request_bytes_sha256"] == validated["request_sha256"]
    assert out["request_byte_length"] == validated["request_byte_length"]
    assert len(out["request_bytes_sha256"]) == 64
    assert out["request_byte_length"] > 0


def test_review_preserves_controlled_matched_scope_without_causal_claim():
    out = review.pair06_v9_execution_authorization_request_review_contract()

    assert out["policy_id"] == "pair06-v9-strict-visible-contact-envelope-v1"
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["doctrine"] == "FEINTER"
    assert out["seed"] == 208354846
    assert out["rounds"] == 36
    assert out["ticks_per_round"] == 25
    assert out["starter_infantry"] == 4
    assert out["staging_max_ticks"] == 800
    assert out["runtime_selection_key"] == "apollyon-v3-qwen35-4b-lora-v1"
    assert out["controlled_comparison_causal_claim_made"] is False


def test_review_preserves_fresh_gpu_and_nonreusable_predecessor_rules():
    out = review.pair06_v9_execution_authorization_request_review_contract()

    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    assert out["fresh_v9_evidence_namespace_required"] is True
    assert out["prior_v8_v2_attempt_reusable"] is False
    assert out["prior_v8_v2_authorization_reusable"] is False


def test_request_digest_is_not_authorization_and_fresh_text_is_required():
    out = review.pair06_v9_execution_authorization_request_review_contract()

    assert out["fresh_user_authorization_text_required"] is True
    assert out["matching_request_digest_grants_authority"] is False
    assert out["request_digest_reusable_as_authorization"] is False


@pytest.mark.parametrize(
    "field",
    (
        "v9_execution_authorization_accepted",
        "v9_policy_activation_authorization_accepted",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "automatic_retry",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "pair03_replay_authorized",
        "pair09_replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_review_grants_no_authority(field):
    out = review.pair06_v9_execution_authorization_request_review_contract()
    assert out[field] is False


def test_review_advances_only_to_fresh_explicit_authorization():
    out = review.pair06_v9_execution_authorization_request_review_contract()

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_EXECUTION_AUTHORIZATION_REQUIRED"
    )
    assert out["next_change_class"] == (
        "audit_only_pair06_v9_strict_visible_contact_execution_authorization_"
        "acceptance"
    )


def test_authorize_or_execute_holds():
    with pytest.raises(
        review.Pair06V9StrictVisibleContactRequestReviewHold,
        match="EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute()
