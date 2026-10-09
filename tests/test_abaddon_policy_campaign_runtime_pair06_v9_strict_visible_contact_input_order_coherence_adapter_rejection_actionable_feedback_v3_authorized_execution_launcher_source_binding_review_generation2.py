from __future__ import annotations

import hashlib
from pathlib import Path

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_authorized_execution_launcher_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_launcher_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_actionable_feedback_v3_authorized_execution_launcher_review_contract()
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


def test_review_binds_exact_v3_authorization_and_consumed_v2_lineage():
    out = (
        review
        .pair06_v9_actionable_feedback_v3_authorized_execution_launcher_review_contract()
    )
    assert out["authorization_text_sha256"] == (
        "9fa7ed99b41b74f6ccfc161f8b2b20cc1fc76391b4a806e75583c6b3ee0ae932"
    )
    assert out["authorization_text_bytes"] == 624
    assert out["authorized_request_sha256"] == (
        "b3ff66271cabc9ed4d5be57c0a0fcd5b7e8cc69c65857fc0e35656f0c3464b2f"
    )
    assert out["authorized_main_at_authorization_head"] == (
        "077c26ece41b2272fbf208d8e862df6a57462d39"
    )
    assert out["consumed_v2_attempt_marker_sha256"] == (
        "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
    )
    assert out["v2_preservation_receipt_sha256"] == (
        "f898ffdbc16bfdf0b3658224e545bb05006600b711ff74d3e3591cc813c59021"
    )


def test_review_binds_all_five_gates_and_runtime_safety():
    out = (
        review
        .pair06_v9_actionable_feedback_v3_authorized_execution_launcher_review_contract()
    )

    assert out[
        "pair06_v9_actionable_feedback_v3_authorized_execution_launcher_reviewed"
    ] is True
    assert out["execution_authorization_accepted"] is True
    assert out["policy_activation_authorization_accepted"] is True
    assert out["order_coherence_activation_authorization_accepted"] is True
    assert out["repair_activation_authorization_accepted"] is True
    assert out["actionable_feedback_v3_activation_authorization_accepted"] is True
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["fresh_actionable_feedback_v3_evidence_namespace_required"] is True


def test_review_grants_no_extra_or_inspection_authority():
    out = (
        review
        .pair06_v9_actionable_feedback_v3_authorized_execution_launcher_review_contract()
    )

    for field in (
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
    ):
        assert out[field] is False


def test_review_advances_only_to_authorized_host_gate():
    out = (
        review
        .pair06_v9_actionable_feedback_v3_authorized_execution_launcher_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V3_AUTHORIZED_HOST_EXECUTION_REQUIRED"
    )
