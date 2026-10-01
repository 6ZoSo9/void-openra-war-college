from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_runtime_integration_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_runtime_integration_and_tests_to_repository_bytes():
    out = (
        review
        .pair06_v9_input_order_coherence_runtime_integration_review_contract()
    )

    assert out["integration_path"] == review.INTEGRATION_PATH
    assert out["integration_git_blob"] == review.INTEGRATION_GIT_BLOB
    assert out["integration_test_path"] == review.INTEGRATION_TEST_PATH
    assert out["integration_test_git_blob"] == review.INTEGRATION_TEST_GIT_BLOB

    assert (
        _git_blob_sha1((ROOT / review.INTEGRATION_PATH).read_bytes())
        == review.INTEGRATION_GIT_BLOB
    )
    assert (
        _git_blob_sha1((ROOT / review.INTEGRATION_TEST_PATH).read_bytes())
        == review.INTEGRATION_TEST_GIT_BLOB
    )


def test_one_byte_runtime_integration_drift_breaks_blob_identity():
    raw = (ROOT / review.INTEGRATION_PATH).read_bytes()
    assert _git_blob_sha1(raw) == review.INTEGRATION_GIT_BLOB

    mutated = raw[:-1] + bytes([raw[-1] ^ 1])
    assert _git_blob_sha1(mutated) != review.INTEGRATION_GIT_BLOB


def test_review_preserves_narrow_order_repair_runtime_boundary():
    out = (
        review
        .pair06_v9_input_order_coherence_runtime_integration_review_contract()
    )

    assert out[
        "pair06_v9_input_order_coherence_runtime_integration_reviewed"
    ] is True
    assert out["historical_v9_policy_source_modified"] is False
    assert out["historical_v9_runtime_integration_source_modified"] is False
    assert out["historical_adapted_decision_code_reused_reviewed"] is True
    assert out["call_scoped_policy_binding_reviewed"] is True
    assert out["process_global_policy_function_mutated"] is False
    assert out["concurrency_scope_leak_closed_reviewed"] is True
    assert out["typed_tool_membership_exact_match_required"] is True
    assert out["typed_tool_order_canonicalized_to_offered_order"] is True
    assert out["membership_drift_still_fail_closed"] is True


def test_review_contract_returns_fresh_validated_snapshot():
    first = (
        review
        .pair06_v9_input_order_coherence_runtime_integration_review_contract()
    )
    first["validated_integration"]["policy_id"] = "mutated"

    second = (
        review
        .pair06_v9_input_order_coherence_runtime_integration_review_contract()
    )
    assert second["validated_integration"]["policy_id"] == (
        "pair06-v9-strict-visible-contact-envelope-v1"
    )


@pytest.mark.parametrize(
    "field",
    (
        "consumed_v9_attempt_retry_authorized",
        "proto_child_repair_wiring_implemented",
        "parent_supervisor_repair_wiring_implemented",
        "operator_repair_wiring_implemented",
        "new_execution_request_opened",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
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
    out = (
        review
        .pair06_v9_input_order_coherence_runtime_integration_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_proto_child_wiring():
    out = (
        review
        .pair06_v9_input_order_coherence_runtime_integration_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "PROTO_CHILD_WIRING_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "PROTO_CHILD_WIRING_REQUIRED"
    )


def test_wire_or_execute_holds():
    with pytest.raises(
        review.Pair06V9InputOrderCoherenceRuntimeIntegrationReviewHold,
        match="INPUT_ORDER_COHERENCE_PROTO_CHILD_WIRING_REQUIRED",
    ):
        review.wire_or_execute()
