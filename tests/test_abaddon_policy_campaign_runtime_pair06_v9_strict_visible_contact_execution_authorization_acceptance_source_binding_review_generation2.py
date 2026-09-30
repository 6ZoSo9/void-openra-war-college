from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_execution_authorization_acceptance_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_acceptance_and_tests_to_repository_bytes():
    out = review.pair06_v9_execution_authorization_acceptance_review_contract()

    assert out["acceptance_path"] == review.ACCEPTANCE_PATH
    assert out["acceptance_git_blob"] == review.ACCEPTANCE_GIT_BLOB
    assert out["acceptance_test_path"] == review.ACCEPTANCE_TEST_PATH
    assert out["acceptance_test_git_blob"] == review.ACCEPTANCE_TEST_GIT_BLOB

    assert (
        _git_blob_sha1((ROOT / review.ACCEPTANCE_PATH).read_bytes())
        == review.ACCEPTANCE_GIT_BLOB
    )
    assert (
        _git_blob_sha1((ROOT / review.ACCEPTANCE_TEST_PATH).read_bytes())
        == review.ACCEPTANCE_TEST_GIT_BLOB
    )


def test_one_byte_acceptance_drift_breaks_blob_identity():
    raw = (ROOT / review.ACCEPTANCE_PATH).read_bytes()
    assert _git_blob_sha1(raw) == review.ACCEPTANCE_GIT_BLOB

    mutated = raw[:-1] + bytes([raw[-1] ^ 1])
    assert _git_blob_sha1(mutated) != review.ACCEPTANCE_GIT_BLOB


def test_review_binds_exact_authorization_text_and_request():
    out = review.pair06_v9_execution_authorization_acceptance_review_contract()

    assert out["authorization_text_sha256"] == (
        "d41fd580d15b4d59491fbb7a2b635946656bbb6c6ae61bcc9222085e23a45bd6"
    )
    assert out["authorization_text_bytes"] == 362
    assert len(out["authorized_request_sha256"]) == 64
    assert out["authorized_request_bytes"] > 0
    assert out["authorized_main_head"] == (
        "bfe8f06245ed2951d247973df927a756a37cfbfd"
    )


def test_review_authorizes_only_one_v9_preclaim_gpu_execution_lane():
    out = review.pair06_v9_execution_authorization_acceptance_review_contract()

    assert out["policy_id"] == "pair06-v9-strict-visible-contact-envelope-v1"
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    assert out["fresh_v9_evidence_namespace_required"] is True
    assert out["receipt_bound_preclaim_gpu_execution_authorized"] is True
    assert out["v9_policy_activation_authorized"] is True


def test_authorization_is_spent_after_attempt_claim():
    out = review.pair06_v9_execution_authorization_acceptance_review_contract()

    assert out["execution_authorization_reusable_after_attempt_claim"] is False
    assert out["policy_activation_authorization_reusable_after_attempt_claim"] is False


@pytest.mark.parametrize(
    "field",
    (
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
def test_review_grants_no_extra_authority(field):
    out = review.pair06_v9_execution_authorization_acceptance_review_contract()
    assert out[field] is False


def test_review_exposes_remaining_runtime_blockers():
    out = review.pair06_v9_execution_authorization_acceptance_review_contract()

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "fresh_preclaim_gpu_admission",
        "exact_current_main",
        "exact_operator_source",
        "fresh_create_only_v9_attempt_marker",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_RECEIPT_BOUND_PRECLAIM_GPU_"
        "EXECUTION_AUTHORIZED"
    )


def test_execute_holds():
    with pytest.raises(
        review.Pair06V9StrictVisibleContactAuthorizationAcceptanceReviewHold,
        match="RECEIPT_BOUND_PRECLAIM_GPU_EXECUTION_AUTHORIZED",
    ):
        review.execute()
