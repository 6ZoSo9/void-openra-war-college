from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_authorized_execution_launcher_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_launcher_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_adapter_rejection_authorized_execution_launcher_review_contract()
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


def test_review_binds_four_gate_authorization_and_fresh_runtime_safety():
    out = (
        review
        .pair06_v9_adapter_rejection_authorized_execution_launcher_review_contract()
    )

    assert out[
        "pair06_v9_adapter_rejection_authorized_execution_launcher_reviewed"
    ] is True
    assert out["execution_authorization_accepted"] is True
    assert out["policy_activation_authorization_accepted"] is True
    assert out["order_coherence_activation_authorization_accepted"] is True
    assert out["repair_activation_authorization_accepted"] is True

    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["fresh_adapter_rejection_evidence_namespace_required"] is True


@pytest.mark.parametrize(
    "field",
    (
        "authorization_reusable_after_attempt_claim",
        "contract_inspection_performs_host_io",
        "contract_inspection_creates_attempt_marker",
        "contract_inspection_loads_model",
        "contract_inspection_runs_inference",
        "contract_inspection_executes_game",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_review_grants_no_extra_or_inspection_authority(field):
    out = (
        review
        .pair06_v9_adapter_rejection_authorized_execution_launcher_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_authorized_host_execution():
    out = (
        review
        .pair06_v9_adapter_rejection_authorized_execution_launcher_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_AUTHORIZED_HOST_EXECUTION_REQUIRED"
    )


def test_execute_holds():
    with pytest.raises(
        review.Pair06V9AdapterRejectionAuthorizedExecutionLauncherReviewHold,
        match="ADAPTER_REJECTION_AUTHORIZED_HOST_EXECUTION_REQUIRED",
    ):
        review.execute()
