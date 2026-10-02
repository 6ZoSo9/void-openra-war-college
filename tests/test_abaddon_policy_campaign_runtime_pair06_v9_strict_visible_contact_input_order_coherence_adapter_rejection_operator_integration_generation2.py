from __future__ import annotations

from types import FunctionType

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_operator_integration_generation2
    as integration,
)


def test_contract_is_source_only_and_requires_fresh_lineage():
    out = (
        integration
        .pair06_v9_input_order_adapter_rejection_operator_integration_contract()
    )

    assert out["adapter_rejection_operator_integration_implemented"] is True
    assert out["historical_operator_source_modified"] is False
    assert out["historical_operator_code_object_reused"] is True
    assert out["call_scoped_dependency_binding_implemented"] is True
    assert out["call_scoped_parent_binding_implemented"] is True
    assert out["reviewed_repaired_parent_used"] is True

    assert out["consumed_input_order_namespace_reusable"] is False
    assert out["consumed_input_order_attempt_retry_authorized"] is False
    assert out["fresh_attempt_namespace_required_before_execution_request"] is True
    assert out[
        "fresh_repair_activation_authorization_required_before_execution_request"
    ] is True
    assert out["fresh_operator_source_required_before_execution_request"] is True

    assert out["new_execution_request_opened"] is False
    assert out["repair_activation_authorization_accepted"] is False
    assert out["runtime_execution_authorized"] is False
    assert out["automatic_retry"] is False


def test_builder_reuses_exact_historical_operator_code_with_two_scoped_bindings():
    scoped = (
        integration
        .build_pair06_v9_input_order_adapter_rejection_operator()
    )

    assert isinstance(scoped, FunctionType)
    assert scoped.__code__ is integration.ORIGINAL_OPERATOR_EXECUTE.__code__
    assert scoped.__defaults__ == integration.ORIGINAL_OPERATOR_EXECUTE.__defaults__
    assert scoped.__closure__ == integration.ORIGINAL_OPERATOR_EXECUTE.__closure__
    assert scoped.__kwdefaults__ == integration.ORIGINAL_OPERATOR_EXECUTE.__kwdefaults__

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
        is integration._execute_repaired_parent
    )


def test_builder_does_not_mutate_historical_operator_globals():
    before_execute = (
        integration.historical_operator
        .execute_pair06_v9_input_order_coherence_baseline_game
    )
    before_dependencies = integration.historical_operator._dependency_contracts
    before_parent = integration.historical_operator.order_parent

    integration.build_pair06_v9_input_order_adapter_rejection_operator()

    assert (
        integration.historical_operator
        .execute_pair06_v9_input_order_coherence_baseline_game
        is before_execute
    )
    assert integration.historical_operator._dependency_contracts is before_dependencies
    assert integration.historical_operator.order_parent is before_parent

    assert before_execute is integration.ORIGINAL_OPERATOR_EXECUTE
    assert before_dependencies is integration.ORIGINAL_OPERATOR_DEPENDENCIES
    assert before_parent is integration.ORIGINAL_OPERATOR_ORDER_PARENT


def test_reentrant_builders_have_independent_copied_globals():
    first = integration.build_pair06_v9_input_order_adapter_rejection_operator()
    second = integration.build_pair06_v9_input_order_adapter_rejection_operator()

    assert first is not second
    assert first.__globals__ is not second.__globals__
    assert first.__globals__ is not integration.ORIGINAL_OPERATOR_EXECUTE.__globals__
    assert second.__globals__ is not integration.ORIGINAL_OPERATOR_EXECUTE.__globals__

    assert first.__globals__["_dependency_contracts"] is (
        second.__globals__["_dependency_contracts"]
    )
    assert first.__globals__["order_parent"] is not second.__globals__["order_parent"]


def test_scoped_dependency_snapshot_includes_repaired_parent_review():
    out = integration._scoped_dependency_contracts()

    assert "adapter_rejection_parent_integration_review" in out
    repaired = out["adapter_rejection_parent_integration_review"]

    assert repaired[
        "pair06_v9_input_order_adapter_rejection_parent_integration_reviewed"
    ] is True
    assert repaired["consumed_input_order_attempt_retry_authorized"] is False
    assert repaired["runtime_execution_authorized"] is False


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
        "repair_activation_authorization_accepted",
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
    out = (
        integration
        .pair06_v9_input_order_adapter_rejection_operator_integration_contract()
    )
    assert out[field] is False


def test_next_gate_is_exact_blob_review_only():
    out = (
        integration
        .pair06_v9_input_order_adapter_rejection_operator_integration_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_OPERATOR_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_review_or_execute_holds():
    with pytest.raises(
        integration.Pair06V9InputOrderAdapterRejectionOperatorIntegrationHold,
        match="ADAPTER_REJECTION_OPERATOR_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        integration.review_or_execute()
