from __future__ import annotations

from types import FunctionType

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_operator_integration_generation2
    as integration,
)


def test_v3_operator_builder_is_call_scoped_and_reuses_v2_code_object():
    scoped = integration.build_pair06_v9_actionable_feedback_v3_operator()

    assert isinstance(scoped, FunctionType)
    assert scoped.__code__ is integration.ORIGINAL_V2_OPERATOR_BUILD().__code__
    assert scoped.__globals__["_dependency_contracts"] is (
        integration._scoped_dependency_contracts
    )

    parent = scoped.__globals__["order_parent"]
    assert (
        parent.execute_pair06_v9_input_order_coherence_parent_supervisor_no_offload
        is integration._execute_v3_parent
    )

    assert integration.v2_operator.build_pair06_v9_actionable_feedback_v2_operator is (
        integration.ORIGINAL_V2_OPERATOR_BUILD
    )
    assert integration.v2_operator._scoped_dependency_contracts is (
        integration.ORIGINAL_V2_OPERATOR_DEPENDENCIES
    )
    assert (
        integration.v3_parent.build_pair06_v9_actionable_feedback_v3_parent_run
        is integration.ORIGINAL_V3_PARENT_BUILD
    )


def test_v3_parent_adapter_preserves_historical_authorization_shape(monkeypatch):
    calls = []

    def parent(**kwargs):
        calls.append(kwargs)
        return {"ok": True}

    monkeypatch.setattr(integration, "ORIGINAL_V3_PARENT_BUILD", lambda: parent)

    out = integration._execute_v3_parent(
        attempt_id="a" * 64,
        attempt_claimed=True,
        runs_root="/tmp/runs",
        frozen_source_root="/tmp/source",
        exact_engine_root="/tmp/engine",
        policy_activation_authorized=True,
        order_coherence_activation_authorized=True,
        execution_authorized=True,
        authority_check=lambda pair, arm: True,
    )

    assert out == {"ok": True}
    assert calls == [{
        "attempt_id": "a" * 64,
        "attempt_claimed": True,
        "runs_root": "/tmp/runs",
        "frozen_source_root": "/tmp/source",
        "exact_engine_root": "/tmp/engine",
        "execution_authorized": True,
        "authority_check": calls[0]["authority_check"],
    }]


@pytest.mark.parametrize(
    "field",
    (
        "reviewed_v2_operator_integration_reused",
        "historical_operator_code_object_reused",
        "call_scoped_dependency_binding_upgraded_to_v3",
        "call_scoped_parent_binding_upgraded_to_v3",
        "reviewed_actionable_feedback_v3_parent_used",
        "historical_preclaim_gpu_ordering_preserved",
        "historical_one_attempt_cardinality_preserved",
        "historical_automatic_retry_remains_false",
        "historical_execution_policy_order_authorizations_preserved",
        "structured_feedback_injected_into_user_prompt",
        "corrective_retry_transfer_prompt_preserved",
        "v2_adapter_rejection_fail_closed_shim_reused",
        "fresh_attempt_namespace_required_before_execution_request",
        "fresh_actionable_feedback_v3_activation_authorization_required",
        "fresh_operator_source_required_before_execution_request",
    ),
)
def test_v3_operator_invariants(field):
    out = integration.pair06_v9_actionable_feedback_v3_operator_integration_contract()
    assert out[field] is True


@pytest.mark.parametrize(
    "field",
    (
        "frozen_v8_tool_schema_modified",
        "frozen_v8_parser_modified",
        "frozen_v8_translator_modified",
        "host_validator_modified",
        "six_attempt_bound_modified",
        "malformed_unit_ids_coerced",
        "malformed_unit_ids_accepted",
        "v2_operator_integration_source_modified",
        "v3_parent_integration_source_modified",
        "process_global_operator_execute_mutated",
        "process_global_operator_dependencies_mutated",
        "process_global_operator_parent_binding_mutated",
        "builder_executes_operator",
        "builder_performs_host_io",
        "builder_loads_model",
        "builder_runs_inference",
        "builder_spawns_child",
        "builder_executes_game",
        "consumed_v2_namespace_reusable",
        "consumed_v2_attempt_retry_authorized",
        "new_execution_request_opened",
        "actionable_feedback_v3_activation_authorization_accepted",
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
def test_v3_operator_grants_no_runtime_or_extra_authority(field):
    out = integration.pair06_v9_actionable_feedback_v3_operator_integration_contract()
    assert out[field] is False


def test_v3_operator_stops_at_exact_blob_review():
    out = integration.pair06_v9_actionable_feedback_v3_operator_integration_contract()
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V3_OPERATOR_INTEGRATION_"
        "SOURCE_BINDING_REVIEW_REQUIRED"
    )

    with pytest.raises(
        integration.Pair06V9ActionableFeedbackV3OperatorIntegrationHold,
        match="SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        integration.review_or_execute()
