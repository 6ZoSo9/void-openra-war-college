from __future__ import annotations

from types import FunctionType

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_parent_integration_generation2
    as integration,
)


def _request() -> dict:
    return {
        "attempt_id": "a" * 64,
        "round_no": 6,
        "attempt_no": 2,
    }


def _response(tool: str) -> dict:
    return {
        "type": "DECIDE_RESPONSE",
        "seq": 9,
        "protocol_version": 1,
        "pair_slot": 6,
        "arm": "baseline",
        "attempt_id": "a" * 64,
        "round_no": 6,
        "attempt_no": 2,
        "campaign_action": {"tool": tool, "arguments": {}},
        "host_mutation_performed": False,
    }


def test_contract_is_source_only_and_preserves_attempt_boundary():
    out = integration.pair06_v9_actionable_feedback_v2_parent_integration_contract()

    assert out["actionable_feedback_v2_parent_integration_implemented"] is True
    assert out["reviewed_v1_parent_integration_reused"] is True
    assert out["historical_parent_run_code_reused"] is True
    assert out["call_scoped_child_command_binding_reused"] is True
    assert out["call_scoped_decision_response_binding_upgraded_to_v2"] is True
    assert out["reviewed_actionable_feedback_v2_used"] is True
    assert out["feedback_requires_quoted_unit_ids_string"] is True
    assert out["feedback_rejects_json_array_unit_ids"] is True
    assert out["feedback_rejects_bare_integer_unit_ids"] is True
    assert out["malformed_unit_ids_coerced"] is False
    assert out["malformed_unit_ids_accepted"] is False
    assert out["consumed_input_order_attempt_retry_authorized"] is False
    assert out["runtime_execution_authorized"] is False
    assert out["automatic_retry"] is False


def test_builder_reuses_v1_parent_code_and_child_binding_but_upgrades_feedback():
    v1_scoped = (
        integration.v1_parent
        .build_pair06_v9_input_order_adapter_rejection_parent_run()
    )
    scoped = integration.build_pair06_v9_actionable_feedback_v2_parent_run()

    assert isinstance(scoped, FunctionType)
    assert scoped.__code__ is v1_scoped.__code__
    assert scoped.__defaults__ == v1_scoped.__defaults__
    assert scoped.__closure__ == v1_scoped.__closure__
    assert scoped.__kwdefaults__ == v1_scoped.__kwdefaults__
    assert scoped.__globals__["_child_command"] is v1_scoped.__globals__["_child_command"]
    assert scoped.__globals__["_decision_response"] is (
        integration.v2_feedback
        .decision_response_with_actionable_adapter_rejection_feedback
    )
    assert v1_scoped.__globals__["_decision_response"] is (
        integration.ORIGINAL_V1_DECISION_RESPONSE
    )


def test_v2_sentinel_reaches_scoped_parent_binding(monkeypatch):
    original = _response(integration.v2_feedback.V1_SENTINEL_TOOL)
    monkeypatch.setattr(
        integration.v2_feedback,
        "ORIGINAL_V1_RESPONSE",
        lambda runtime, request, *, seq, authority_check: original,
    )

    scoped = integration.build_pair06_v9_actionable_feedback_v2_parent_run()
    handler = scoped.__globals__["_decision_response"]
    out = handler(
        object(),
        _request(),
        seq=9,
        authority_check=lambda pair_slot, arm: pair_slot == 6 and arm == "baseline",
    )

    assert out is not original
    assert original["campaign_action"]["tool"] == integration.v2_feedback.V1_SENTINEL_TOOL
    assert out["campaign_action"]["tool"] == integration.v2_feedback.V2_SENTINEL_TOOL
    assert out["campaign_action"]["arguments"] == {}
    assert out["host_mutation_performed"] is False


def test_non_sentinel_v1_response_passes_through_scoped_parent_by_identity(monkeypatch):
    expected = _response("advance")
    monkeypatch.setattr(
        integration.v2_feedback,
        "ORIGINAL_V1_RESPONSE",
        lambda runtime, request, *, seq, authority_check: expected,
    )

    scoped = integration.build_pair06_v9_actionable_feedback_v2_parent_run()
    out = scoped.__globals__["_decision_response"](
        object(),
        _request(),
        seq=9,
        authority_check=lambda pair_slot, arm: True,
    )

    assert out is expected


def test_scoped_v2_binding_rechecks_authority_before_sentinel_rewrite(monkeypatch):
    monkeypatch.setattr(
        integration.v2_feedback,
        "ORIGINAL_V1_RESPONSE",
        lambda runtime, request, *, seq, authority_check: _response(
            integration.v2_feedback.V1_SENTINEL_TOOL
        ),
    )

    scoped = integration.build_pair06_v9_actionable_feedback_v2_parent_run()
    with pytest.raises(
        integration.v2_feedback.Pair06V9AdapterRejectionActionableFeedbackV2Hold,
        match="AUTHORITY_REVOKED_AFTER_V1_SENTINEL",
    ):
        scoped.__globals__["_decision_response"](
            object(),
            _request(),
            seq=9,
            authority_check=lambda pair_slot, arm: False,
        )


def test_builder_does_not_mutate_reviewed_v1_parent_or_feedback_functions():
    before_build = (
        integration.v1_parent
        .build_pair06_v9_input_order_adapter_rejection_parent_run
    )
    before_v1 = (
        integration.v1_parent.adapter_response
        .decision_response_with_observed_adapter_rejection
    )
    before_v2 = (
        integration.v2_feedback
        .decision_response_with_actionable_adapter_rejection_feedback
    )

    integration.build_pair06_v9_actionable_feedback_v2_parent_run()

    assert (
        integration.v1_parent.build_pair06_v9_input_order_adapter_rejection_parent_run
        is before_build
    )
    assert (
        integration.v1_parent.adapter_response
        .decision_response_with_observed_adapter_rejection
        is before_v1
    )
    assert (
        integration.v2_feedback
        .decision_response_with_actionable_adapter_rejection_feedback
        is before_v2
    )


@pytest.mark.parametrize(
    "field",
    (
        "process_global_parent_run_function_mutated",
        "process_global_child_command_builder_mutated",
        "process_global_decision_response_mutated",
        "builder_executes_parent",
        "builder_performs_host_io",
        "builder_loads_model",
        "builder_runs_inference",
        "builder_spawns_child",
        "builder_executes_game",
        "new_execution_request_opened",
        "attempt_claim_created",
        "attempt_created",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "automatic_retry",
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
def test_contract_grants_no_runtime_or_follow_on_authority(field):
    out = integration.pair06_v9_actionable_feedback_v2_parent_integration_contract()
    assert out[field] is False


def test_next_gate_is_exact_blob_review_only():
    out = integration.pair06_v9_actionable_feedback_v2_parent_integration_contract()
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_PARENT_INTEGRATION_"
        "SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_review_or_execute_holds():
    with pytest.raises(
        integration.Pair06V9ActionableFeedbackV2ParentIntegrationHold,
        match="ACTIONABLE_FEEDBACK_V2_PARENT_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        integration.review_or_execute()
