from __future__ import annotations

from types import FunctionType

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_parent_integration_generation2
    as integration,
)


def test_contract_is_source_only_and_preserves_consumed_attempt_boundary():
    out = (
        integration
        .pair06_v9_input_order_adapter_rejection_parent_integration_contract()
    )

    assert out["adapter_rejection_parent_integration_implemented"] is True
    assert out["historical_parent_source_modified"] is False
    assert out["historical_parent_run_code_reused"] is True
    assert out["call_scoped_child_command_binding_reused"] is True
    assert out["call_scoped_decision_response_binding_implemented"] is True
    assert out["input_order_child_command_used"] is True
    assert out["reviewed_adapter_rejection_response_used"] is True
    assert out["malformed_unit_ids_coerced"] is False
    assert out["malformed_unit_ids_accepted"] is False
    assert out["consumed_input_order_attempt_retry_authorized"] is False
    assert out["runtime_execution_authorized"] is False
    assert out["automatic_retry"] is False


def test_builder_reuses_exact_historical_code_with_only_two_scoped_bindings():
    scoped = (
        integration
        .build_pair06_v9_input_order_adapter_rejection_parent_run()
    )

    assert isinstance(scoped, FunctionType)
    assert scoped.__code__ is integration.ORIGINAL_PARENT_RUN.__code__
    assert scoped.__defaults__ == integration.ORIGINAL_PARENT_RUN.__defaults__
    assert scoped.__closure__ == integration.ORIGINAL_PARENT_RUN.__closure__
    assert scoped.__kwdefaults__ == integration.ORIGINAL_PARENT_RUN.__kwdefaults__

    assert scoped.__globals__["_child_command"] is (
        integration.order_parent._order_child_command
    )
    assert scoped.__globals__["_decision_response"] is (
        integration.adapter_response
        .decision_response_with_observed_adapter_rejection
    )


def test_builder_does_not_mutate_historical_parent_globals():
    before_child = integration.parent._child_command
    before_response = integration.parent._decision_response
    before_run = integration.parent.execute_pair06_v8_parent_supervisor_no_offload

    integration.build_pair06_v9_input_order_adapter_rejection_parent_run()

    assert integration.parent._child_command is before_child
    assert integration.parent._decision_response is before_response
    assert (
        integration.parent.execute_pair06_v8_parent_supervisor_no_offload
        is before_run
    )
    assert before_child is integration.ORIGINAL_CHILD_COMMAND
    assert before_response is integration.ORIGINAL_DECISION_RESPONSE
    assert before_run is integration.ORIGINAL_PARENT_RUN


def test_reentrant_builders_have_independent_copied_globals():
    first = integration.build_pair06_v9_input_order_adapter_rejection_parent_run()
    second = integration.build_pair06_v9_input_order_adapter_rejection_parent_run()

    assert first is not second
    assert first.__globals__ is not second.__globals__
    assert first.__globals__ is not integration.ORIGINAL_PARENT_RUN.__globals__
    assert second.__globals__ is not integration.ORIGINAL_PARENT_RUN.__globals__

    assert first.__globals__["_child_command"] is second.__globals__["_child_command"]
    assert first.__globals__["_decision_response"] is (
        second.__globals__["_decision_response"]
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
    out = (
        integration
        .pair06_v9_input_order_adapter_rejection_parent_integration_contract()
    )
    assert out[field] is False


def test_next_gate_is_exact_blob_review_only():
    out = (
        integration
        .pair06_v9_input_order_adapter_rejection_parent_integration_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_PARENT_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_review_or_execute_holds():
    with pytest.raises(
        integration.Pair06V9InputOrderAdapterRejectionParentIntegrationHold,
        match="ADAPTER_REJECTION_PARENT_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        integration.review_or_execute()
