from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_proto_child_wiring_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_wiring_and_tests_to_repository_bytes():
    out = review.pair06_v9_input_order_coherence_proto_child_wiring_review_contract()

    assert out["wiring_path"] == review.WIRING_PATH
    assert out["wiring_git_blob"] == review.WIRING_GIT_BLOB
    assert out["wiring_test_path"] == review.WIRING_TEST_PATH
    assert out["wiring_test_git_blob"] == review.WIRING_TEST_GIT_BLOB

    assert _git_blob_sha1((ROOT / review.WIRING_PATH).read_bytes()) == (
        review.WIRING_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.WIRING_TEST_PATH).read_bytes()) == (
        review.WIRING_TEST_GIT_BLOB
    )


def test_review_preserves_global_isolation_and_authorization_gates():
    out = review.pair06_v9_input_order_coherence_proto_child_wiring_review_contract()

    assert out["pair06_v9_input_order_coherence_proto_child_wiring_reviewed"] is True
    assert out["historical_v9_proto_child_source_modified"] is False
    assert out["existing_v8_proto_child_source_modified"] is False
    assert out["historical_v8_child_run_code_reused_reviewed"] is True
    assert out["call_scoped_child_hook_factory_binding_reviewed"] is True
    assert out["process_global_child_hook_factory_mutated"] is False
    assert out["process_global_child_run_function_mutated"] is False
    assert out["new_concurrency_scope_leak_introduced"] is False
    assert out["original_child_execution_authorization_gate_preserved"] is True
    assert out["historical_v9_policy_activation_gate_preserved"] is True
    assert out["additional_order_coherence_activation_gate_required"] is True
    assert out["order_coherent_decision_hook_reviewed"] is True
    assert out["membership_drift_still_fail_closed"] is True


def test_review_contract_returns_fresh_validated_snapshot():
    first = review.pair06_v9_input_order_coherence_proto_child_wiring_review_contract()
    first["validated_wiring"]["policy_id"] = "mutated"

    second = review.pair06_v9_input_order_coherence_proto_child_wiring_review_contract()
    assert second["validated_wiring"]["policy_id"] == (
        "pair06-v9-strict-visible-contact-envelope-v1"
    )


@pytest.mark.parametrize(
    "field",
    (
        "consumed_v9_attempt_retry_authorized",
        "parent_supervisor_repair_wiring_implemented",
        "operator_repair_wiring_implemented",
        "new_execution_request_opened",
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
    out = review.pair06_v9_input_order_coherence_proto_child_wiring_review_contract()
    assert out[field] is False


def test_review_advances_only_to_parent_supervisor_wiring():
    out = review.pair06_v9_input_order_coherence_proto_child_wiring_review_contract()

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "PARENT_SUPERVISOR_WIRING_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "PARENT_SUPERVISOR_WIRING_REQUIRED"
    )


def test_wire_parent_or_execute_holds():
    with pytest.raises(
        review.Pair06V9InputOrderCoherenceProtoChildWiringReviewHold,
        match="INPUT_ORDER_COHERENCE_PARENT_SUPERVISOR_WIRING_REQUIRED",
    ):
        review.wire_parent_or_execute()
