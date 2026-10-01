from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_parent_supervisor_wiring_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_child_entry_parent_wiring_and_tests():
    out = review.pair06_v9_input_order_coherence_parent_wiring_review_contract()

    for path_key, blob_key in (
        ("child_entry_path", "child_entry_git_blob"),
        ("child_entry_test_path", "child_entry_test_git_blob"),
        ("parent_wiring_path", "parent_wiring_git_blob"),
        ("parent_wiring_test_path", "parent_wiring_test_git_blob"),
    ):
        path = out[path_key]
        expected = out[blob_key]
        assert _git_blob_sha1((ROOT / path).read_bytes()) == expected


def test_review_preserves_parent_global_isolation_and_three_gates():
    out = review.pair06_v9_input_order_coherence_parent_wiring_review_contract()

    assert out["pair06_v9_input_order_coherence_parent_wiring_reviewed"] is True
    assert out["input_order_child_entrypoint_reviewed"] is True
    assert out["existing_no_offload_parent_source_modified"] is False
    assert out["historical_parent_run_code_reused_reviewed"] is True
    assert out["call_scoped_child_command_binding_reviewed"] is True
    assert out["process_global_child_command_builder_mutated"] is False
    assert out["process_global_parent_run_function_mutated"] is False
    assert out["new_concurrency_scope_leak_introduced"] is False
    assert out["execution_confirmation_token_preserved"] is True
    assert out["historical_v9_policy_activation_token_preserved"] is True
    assert out["distinct_order_coherence_activation_token_preserved"] is True
    assert out["durable_attempt_claim_prerequisite_preserved"] is True
    assert out["no_offload_cuda0_parent_path_preserved"] is True
    assert out["membership_drift_still_fail_closed"] is True


def test_review_returns_fresh_validated_snapshot():
    first = review.pair06_v9_input_order_coherence_parent_wiring_review_contract()
    first["validated"]["parent_wiring"]["policy_id"] = "mutated"

    second = review.pair06_v9_input_order_coherence_parent_wiring_review_contract()
    assert second["validated"]["parent_wiring"]["policy_id"] == (
        "pair06-v9-strict-visible-contact-envelope-v1"
    )


@pytest.mark.parametrize(
    "field",
    (
        "consumed_v9_attempt_retry_authorized",
        "operator_entrypoint_wiring_implemented",
        "execution_request_created",
        "attempt_claim_created",
        "attempt_created",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "automatic_retry",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_review_grants_no_retry_or_effect_authority(field):
    out = review.pair06_v9_input_order_coherence_parent_wiring_review_contract()
    assert out[field] is False


def test_review_advances_only_to_operator_entrypoint_wiring():
    out = review.pair06_v9_input_order_coherence_parent_wiring_review_contract()

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "OPERATOR_ENTRYPOINT_WIRING_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "OPERATOR_ENTRYPOINT_WIRING_REQUIRED"
    )


def test_wire_operator_or_execute_holds():
    with pytest.raises(
        review.Pair06V9InputOrderCoherenceParentWiringReviewHold,
        match="INPUT_ORDER_COHERENCE_OPERATOR_ENTRYPOINT_WIRING_REQUIRED",
    ):
        review.wire_operator_or_execute()
