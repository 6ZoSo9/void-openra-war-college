from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_operator_entrypoint_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_operator_and_tests_to_repository_bytes():
    out = review.pair06_v9_strict_visible_contact_operator_review_contract()

    assert out["operator_path"] == review.OPERATOR_PATH
    assert out["operator_git_blob"] == review.OPERATOR_GIT_BLOB
    assert out["operator_test_path"] == review.OPERATOR_TEST_PATH
    assert out["operator_test_git_blob"] == review.OPERATOR_TEST_GIT_BLOB

    assert (
        _git_blob_sha1((ROOT / review.OPERATOR_PATH).read_bytes())
        == review.OPERATOR_GIT_BLOB
    )
    assert (
        _git_blob_sha1((ROOT / review.OPERATOR_TEST_PATH).read_bytes())
        == review.OPERATOR_TEST_GIT_BLOB
    )


def test_one_byte_operator_drift_breaks_blob_identity():
    raw = (ROOT / review.OPERATOR_PATH).read_bytes()
    assert _git_blob_sha1(raw) == review.OPERATOR_GIT_BLOB

    mutated = raw[:-1] + bytes([raw[-1] ^ 1])
    assert _git_blob_sha1(mutated) != review.OPERATOR_GIT_BLOB


def test_review_closes_only_operator_source_frontier():
    out = review.pair06_v9_strict_visible_contact_operator_review_contract()

    assert out[
        "pair06_v9_strict_visible_contact_operator_entrypoint_reviewed"
    ] is True
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["fresh_v9_evidence_namespace_required"] is True
    assert out["prior_v8_v2_attempt_reusable"] is False
    assert out["prior_v8_v2_authorization_reusable"] is False
    assert out["dual_explicit_authorizations_required"] is True
    assert out["dual_distinct_confirmation_tokens_required"] is True
    assert out["execution_request_created"] is False


@pytest.mark.parametrize(
    "field",
    (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_review_grants_no_effect_authority(field):
    out = review.pair06_v9_strict_visible_contact_operator_review_contract()
    assert out[field] is False


def test_review_advances_only_to_fresh_authorization_request():
    out = review.pair06_v9_strict_visible_contact_operator_review_contract()

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_EXECUTION_AUTHORIZATION_REQUEST_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_pair06_v9_strict_visible_contact_execution_authorization_request"
    )


def test_request_or_execute_holds():
    with pytest.raises(
        review.Pair06V9StrictVisibleContactOperatorReviewHold,
        match="EXECUTION_AUTHORIZATION_REQUEST_REQUIRED",
    ):
        review.request_or_execute()
