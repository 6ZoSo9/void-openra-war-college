from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_authorized_execution_launcher_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_launcher_and_tests_to_repository_bytes():
    out = (
        review
        .pair06_v9_input_order_authorized_execution_launcher_review_contract()
    )

    assert out["launcher_path"] == review.LAUNCHER_PATH
    assert out["launcher_git_blob"] == review.LAUNCHER_GIT_BLOB
    assert out["launcher_test_path"] == review.LAUNCHER_TEST_PATH
    assert out["launcher_test_git_blob"] == review.LAUNCHER_TEST_GIT_BLOB
    assert _git_blob_sha1((ROOT / review.LAUNCHER_PATH).read_bytes()) == (
        review.LAUNCHER_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.LAUNCHER_TEST_PATH).read_bytes()) == (
        review.LAUNCHER_TEST_GIT_BLOB
    )


def test_review_preserves_one_shot_gpu_and_canonical_blob_gates():
    out = (
        review
        .pair06_v9_input_order_authorized_execution_launcher_review_contract()
    )

    assert out[
        "pair06_v9_input_order_authorized_execution_launcher_reviewed"
    ] is True
    assert out["policy_id"] == "pair06-v9-strict-visible-contact-envelope-v1"
    assert out["intervention_id"] == "pair06-v9-input-order-coherence-repair-v1"
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    assert out["fresh_order_evidence_namespace_required"] is True
    assert out["exact_canonical_blobs_required_before_execution"] is True
    assert out["explicit_launcher_confirmation_required"] is True
    assert out["authorization_reusable_after_attempt_claim"] is False


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
    out = (
        review
        .pair06_v9_input_order_authorized_execution_launcher_review_contract()
    )
    assert out[field] is False


def test_review_exposes_host_execution_frontier():
    out = (
        review
        .pair06_v9_input_order_authorized_execution_launcher_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "explicit_launcher_confirmation",
        "exact_current_main_and_canonical_blobs",
        "fresh_preclaim_gpu_admission",
        "fresh_create_only_order_coherence_attempt_marker",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "HOST_EXECUTION_REQUIRED"
    )


def test_execute_holds():
    with pytest.raises(
        review.Pair06V9InputOrderCoherenceAuthorizedExecutionLauncherReviewHold,
        match="INPUT_ORDER_COHERENCE_HOST_EXECUTION_REQUIRED",
    ):
        review.execute()
