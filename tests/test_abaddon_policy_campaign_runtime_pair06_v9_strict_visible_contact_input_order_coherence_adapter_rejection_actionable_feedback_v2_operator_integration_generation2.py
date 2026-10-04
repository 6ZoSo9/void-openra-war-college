from __future__ import annotations

from types import FunctionType

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_operator_integration_generation2
    as integration,
)


def test_contract_is_source_only_and_requires_fresh_v2_lineage():
    out = integration.pair06_v9_actionable_feedback_v2_operator_integration_contract()

    assert out["actionable_feedback_v2_operator_integration_implemented"] is True
    assert out["reviewed_v1_operator_integration_reused"] is True
    assert out["historical_operator_code_object_reused"] is True
    assert out["call_scoped_dependency_binding_upgraded_to_v2"] is True
    assert out["call_scoped_parent_binding_upgraded_to_v2"] is True
    assert out["reviewed_actionable_feedback_v2_parent_used"] is True

    assert out["consumed_input_order_namespace_reusable"] is False
    assert out["consumed_input_order_attempt_retry_authorized"] is False
    assert out["fresh_attempt_namespace_required_before_execution_request"] is True
    assert out["fresh_actionable_feedback_v2_activation_authorization_required"] is True
    assert out["fresh_operator_source_required_before_execution_request"] is True

    assert out["new_execution_request_opened"] is False
    assert out["actionable_feedback_v2_activation_authorization_accepted"] is False
    assert out["runtime_execution_authorized"] is False
    assert out["automatic_retry"] is False


def test_builder_reuses_v1_operator_code_and_upgrades_only_scoped_bindings():
    v1_scoped = integration.v1_operator.build_pair06_v9_input_order_adapter_rejection_operator()
    scoped = integration.build_pair06_v9_actionable_feedback_v2_operator()

    assert isinstance(scoped, FunctionType)
    assert scoped.__code__ is v1_scoped.__code__
    assert scoped.__defaults__ == v1_scoped.__defaults__
    assert scoped.__closure__ == v1_scoped.__closure__
    assert scoped.__kwdefaults__ == v1_scoped.__kwdefaults__

    assert scoped.__globals__["_dependency_contracts"] is (
        integration._scoped_dependency_contracts
    )
    scoped_parent = scoped.__globals__["order_parent"]
    assert callable(
        scoped_parent
        .execute_pair06_v9_input_order_coherence_parent_supervisor_no_offload
    )
    assert (
        scoped_parent
        .execute_pair06_v9_input_order_coherence_parent_supervisor_no_offload
        is integration._execute_v2_parent
    )

    assert v1_scoped.__globals__["_dependency_contracts"] is (
        integration.ORIGINAL_V1_OPERATOR_DEPENDENCIES
    )
    assert v1_scoped.__globals__["order_parent"] is not scoped_parent


def test_scoped_dependency_snapshot_includes_v2_parent_review():
    out = integration._scoped_dependency_contracts()

    assert "adapter_rejection_parent_integration_review" in out
    assert "actionable_feedback_v2_parent_integration_review" in out

    parent = out["actionable_feedback_v2_parent_integration_review"]
    assert parent["pair06_v9_actionable_feedback_v2_parent_integration_reviewed"] is True
    assert parent["call_scoped_decision_response_binding_upgraded_to_v2"] is True
    assert parent["consumed_input_order_attempt_retry_authorized"] is False
    assert parent["runtime_execution_authorized"] is False


def test_v2_parent_adapter_preserves_three_historical_authority_checks(monkeypatch):
    calls = []

    def fake_parent_builder():
        calls.append("build")

        def fake_parent(**kwargs):
            calls.append(kwargs)
            return {"ok": True}

        return fake_parent

    monkeypatch.setattr(
        integration,
        "ORIGINAL_V2_PARENT_BUILD",
        fake_parent_builder,
    )

    out = integration._execute_v2_parent(
        attempt_id="a" * 64,
        attempt_claimed=True,
        runs_root="/tmp/runs",
        frozen_source_root="/tmp/source",
        exact_engine_root="/tmp/engine",
        policy_activation_authorized=True,
        order_coherence_activation_authorized=True,
        execution_authorized=True,
        authority_check=lambda pair_slot, arm: True,
    )

    assert out == {"ok": True}
    assert calls[0] == "build"
    assert calls[1]["execution_authorized"] is True

    with pytest.raises(
        integration.Pair06V9ActionableFeedbackV2OperatorIntegrationHold,
        match="POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
    ):
        integration._execute_v2_parent(
            attempt_id="a" * 64,
            attempt_claimed=True,
            runs_root="/tmp/runs",
            frozen_source_root="/tmp/source",
            exact_engine_root="/tmp/engine",
            policy_activation_authorized=False,
            order_coherence_activation_authorized=True,
            execution_authorized=True,
            authority_check=lambda pair_slot, arm: True,
        )


def test_builder_does_not_mutate_reviewed_v1_operator_or_v2_parent():
    before_operator = (
        integration.v1_operator.build_pair06_v9_input_order_adapter_rejection_operator
    )
    before_dependencies = integration.v1_operator._scoped_dependency_contracts
    before_parent = (
        integration.v2_parent.build_pair06_v9_actionable_feedback_v2_parent_run
    )

    integration.build_pair06_v9_actionable_feedback_v2_operator()

    assert (
        integration.v1_operator.build_pair06_v9_input_order_adapter_rejection_operator
        is before_operator
    )
    assert integration.v1_operator._scoped_dependency_contracts is before_dependencies
    assert (
        integration.v2_parent.build_pair06_v9_actionable_feedback_v2_parent_run
        is before_parent
    )


def test_reentrant_builders_have_independent_copied_globals():
    first = integration.build_pair06_v9_actionable_feedback_v2_operator()
    second = integration.build_pair06_v9_actionable_feedback_v2_operator()

    assert first is not second
    assert first.__globals__ is not second.__globals__
    assert first.__globals__["_dependency_contracts"] is (
        second.__globals__["_dependency_contracts"]
    )
    assert first.__globals__["order_parent"] is not second.__globals__["order_parent"]


@pytest.mark.parametrize(
    "field",
    (
        "process_global_operator_execute_mutated",
        "process_global_operator_dependencies_mutated",
        "process_global_operator_parent_binding_mutated",
        "builder_executes_operator",
        "builder_performs_host_io",
        "builder_loads_model",
        "builder_runs_inference",
        "builder_spawns_child",
        "builder_executes_game",
        "malformed_unit_ids_coerced",
        "malformed_unit_ids_accepted",
        "consumed_input_order_namespace_reusable",
        "consumed_input_order_attempt_retry_authorized",
        "new_execution_request_opened",
        "actionable_feedback_v2_activation_authorization_accepted",
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
    out = integration.pair06_v9_actionable_feedback_v2_operator_integration_contract()
    assert out[field] is False


def test_next_gate_is_exact_blob_review_only():
    out = integration.pair06_v9_actionable_feedback_v2_operator_integration_contract()
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_OPERATOR_INTEGRATION_"
        "SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_review_or_execute_holds():
    with pytest.raises(
        integration.Pair06V9ActionableFeedbackV2OperatorIntegrationHold,
        match="ACTIONABLE_FEEDBACK_V2_OPERATOR_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        integration.review_or_execute()
