from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_no_offload_generation2
    as parent,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_parent_supervisor_wiring_generation2
    as wiring,
)


def _kwargs() -> dict:
    return {
        "attempt_id": "a" * 64,
        "attempt_claimed": True,
        "runs_root": "/runs",
        "frozen_source_root": "/source",
        "exact_engine_root": "/engine",
        "policy_activation_authorized": True,
        "order_coherence_activation_authorized": True,
        "execution_authorized": True,
        "authority_check": lambda slot, arm: slot == 6 and arm == "baseline",
    }


def test_contract_binds_reviewed_parent_and_order_coherent_child():
    out = wiring.pair06_v9_input_order_coherence_parent_wiring_contract()

    assert out["order_child_wiring_review_git_blob"] == (
        "7e96e32361b64f71ccf5c2cfd3c10a33c15429a1"
    )
    assert out["no_offload_parent_git_blob"] == (
        "231758aeced0a57949dc39165df0f994e8473ebc"
    )
    assert out["no_offload_parent_review_git_blob"] == (
        "6a65984b81e563def012c6da1405ad47747bb465"
    )
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"


@pytest.mark.parametrize(
    ("field", "message"),
    (
        (
            "policy_activation_authorized",
            "V9_STRICT_VISIBLE_CONTACT_POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
        ),
        (
            "order_coherence_activation_authorized",
            "V9_INPUT_ORDER_COHERENCE_ACTIVATION_AUTHORIZATION_REQUIRED",
        ),
        (
            "execution_authorized",
            "GAME_EXECUTION_AUTHORIZATION_REQUIRED",
        ),
    ),
)
def test_wrapper_requires_all_activation_and_execution_gates(field, message):
    kwargs = _kwargs()
    kwargs[field] = False

    with pytest.raises(
        wiring.Pair06V9InputOrderCoherenceParentWiringHold,
        match=message,
    ):
        wiring.execute_pair06_v9_input_order_coherence_parent_supervisor_no_offload(
            **kwargs
        )


def test_child_command_contains_three_distinct_confirmation_tokens():
    command = wiring._order_child_command(
        child_fd=9,
        attempt_id="b" * 64,
        runs_root="/runs",
        frozen_source_root="/source",
        exact_engine_root="/engine",
    )

    assert command[0] == str(parent.PROTO_PYTHON)
    assert command[1:3] == ["-B", "-m"]
    assert command[3] == wiring.ORDER_CHILD_MODULE
    assert command[command.index("--confirm") + 1] == wiring.child_entry.CONFIRM_TOKEN
    assert command[command.index("--policy-confirm") + 1] == (
        wiring.child_entry.POLICY_CONFIRM_TOKEN
    )
    assert command[command.index("--order-confirm") + 1] == (
        wiring.child_entry.ORDER_CONFIRM_TOKEN
    )
    assert len(
        {
            wiring.child_entry.CONFIRM_TOKEN,
            wiring.child_entry.POLICY_CONFIRM_TOKEN,
            wiring.child_entry.ORDER_CONFIRM_TOKEN,
        }
    ) == 3


def test_scoped_parent_run_binds_child_command_without_global_mutation():
    original_run = parent.execute_pair06_v8_parent_supervisor_no_offload
    original_command = parent._child_command

    scoped = wiring._scoped_parent_run()

    assert scoped is not original_run
    assert scoped.__code__ is original_run.__code__
    assert scoped.__globals__["_child_command"] is wiring._order_child_command
    assert parent._child_command is original_command
    assert parent.execute_pair06_v8_parent_supervisor_no_offload is original_run


def test_wrapper_delegates_without_global_parent_mutation(monkeypatch):
    observed = {}

    def fake_scoped_run(**kwargs):
        observed["command"] = wiring._order_child_command(
            child_fd=11,
            attempt_id=kwargs["attempt_id"],
            runs_root=kwargs["runs_root"],
            frozen_source_root=kwargs["frozen_source_root"],
            exact_engine_root=kwargs["exact_engine_root"],
        )
        observed["kwargs"] = kwargs
        return {
            "schema": "existing-parent-receipt",
            "automatic_retry": False,
        }

    monkeypatch.setattr(wiring, "_scoped_parent_run", lambda: fake_scoped_run)

    result = (
        wiring
        .execute_pair06_v9_input_order_coherence_parent_supervisor_no_offload(
            **_kwargs()
        )
    )

    assert result["schema"] == "existing-parent-receipt"
    assert observed["kwargs"]["attempt_claimed"] is True
    assert observed["kwargs"]["execution_authorized"] is True
    assert "--order-confirm" in observed["command"]
    assert parent._child_command is wiring.ORIGINAL_CHILD_COMMAND
    assert parent.execute_pair06_v8_parent_supervisor_no_offload is (
        wiring.ORIGINAL_PARENT_RUN
    )


def test_wrapper_keeps_globals_original_after_delegate_failure(monkeypatch):
    def fake_scoped_run(**kwargs):
        assert parent._child_command is wiring.ORIGINAL_CHILD_COMMAND
        raise RuntimeError("synthetic parent failure")

    monkeypatch.setattr(wiring, "_scoped_parent_run", lambda: fake_scoped_run)

    with pytest.raises(RuntimeError, match="synthetic parent failure"):
        wiring.execute_pair06_v9_input_order_coherence_parent_supervisor_no_offload(
            **_kwargs()
        )

    assert parent._child_command is wiring.ORIGINAL_CHILD_COMMAND
    assert parent.execute_pair06_v8_parent_supervisor_no_offload is (
        wiring.ORIGINAL_PARENT_RUN
    )


def test_contract_preserves_parent_and_creates_no_execution_lineage():
    out = wiring.pair06_v9_input_order_coherence_parent_wiring_contract()

    assert out["existing_no_offload_parent_source_modified"] is False
    assert out["historical_no_offload_parent_run_code_reused"] is True
    assert out["call_scoped_child_command_binding_implemented"] is True
    assert out["process_global_child_command_builder_mutated"] is False
    assert out["process_global_parent_run_function_mutated"] is False
    assert out["new_concurrency_scope_leak_introduced"] is False
    assert out["existing_no_offload_model_loader_reused"] is True
    assert out["existing_cuda0_placement_checks_reused"] is True
    assert out["existing_parent_decision_service_loop_reused"] is True
    assert out["existing_child_retirement_reused"] is True
    assert out["durable_attempt_claim_required_by_existing_parent"] is True
    assert out["consumed_v9_attempt_retry_authorized"] is False

    for field in (
        "attempt_claim_created_by_this_wiring",
        "execution_request_created_by_this_wiring",
        "attempt_created_by_this_wiring",
        "operator_entrypoint_wiring_implemented",
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
    ):
        assert out[field] is False


def test_parent_wiring_advances_only_to_source_review():
    out = wiring.pair06_v9_input_order_coherence_parent_wiring_contract()

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "PARENT_SUPERVISOR_WIRING_SOURCE_BINDING_REVIEW_REQUIRED",
    )


def test_entrypoint_holds():
    with pytest.raises(
        wiring.Pair06V9InputOrderCoherenceParentWiringHold,
        match="PARENT_SUPERVISOR_WIRING_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        wiring.review_or_execute()
