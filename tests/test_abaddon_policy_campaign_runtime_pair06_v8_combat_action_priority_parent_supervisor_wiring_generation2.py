from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_parent_supervisor_wiring_generation2
    as wiring,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_no_offload_generation2
    as parent,
)


def _kwargs() -> dict:
    return {
        "attempt_id": "a" * 64,
        "attempt_claimed": True,
        "runs_root": "/runs",
        "frozen_source_root": "/source",
        "exact_engine_root": "/engine",
        "policy_activation_authorized": True,
        "execution_authorized": True,
        "authority_check": lambda slot, arm: slot == 6 and arm == "baseline",
    }


def test_contract_binds_reviewed_no_offload_parent_and_child_wiring():
    out = wiring.pair06_v8_combat_priority_parent_supervisor_wiring_contract()
    assert out["child_wiring_review_main_head"] == (
        "83b852117c51bda876b1f4bc18ffd804922054b4"
    )
    assert out["child_wiring_review_git_blob"] == (
        "e0247e50ead91356f60e57b454331fba8e2ae69c"
    )
    assert out["no_offload_parent_git_blob"] == (
        "231758aeced0a57949dc39165df0f994e8473ebc"
    )
    assert out["no_offload_parent_source_sha256"] == (
        "1333cac233d6e9235a2d64c36b8398bb4773150cf2fe5025f28fed5457fe7d7f"
    )


def test_policy_activation_gate_holds_before_parent_delegation():
    original = parent._child_command
    kwargs = _kwargs()
    kwargs["policy_activation_authorized"] = False

    with pytest.raises(
        wiring.Pair06V8CombatPriorityParentWiringHold,
        match="POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
    ):
        wiring.execute_pair06_v8_combat_priority_parent_supervisor_no_offload(
            **kwargs
        )

    assert parent._child_command is original


def test_execution_gate_holds_before_parent_delegation():
    original = parent._child_command
    kwargs = _kwargs()
    kwargs["execution_authorized"] = False

    with pytest.raises(
        wiring.Pair06V8CombatPriorityParentWiringHold,
        match="GAME_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        wiring.execute_pair06_v8_combat_priority_parent_supervisor_no_offload(
            **kwargs
        )

    assert parent._child_command is original


def test_scoped_parent_wiring_changes_only_child_command_builder(monkeypatch):
    observed = {}

    def fake_execute(**kwargs):
        observed["command"] = parent._child_command(
            child_fd=9,
            attempt_id=kwargs["attempt_id"],
            runs_root=kwargs["runs_root"],
            frozen_source_root=kwargs["frozen_source_root"],
            exact_engine_root=kwargs["exact_engine_root"],
        )
        observed["kwargs"] = kwargs
        return {"schema": "existing-parent-receipt", "automatic_retry": False}

    monkeypatch.setattr(
        parent,
        "execute_pair06_v8_parent_supervisor_no_offload",
        fake_execute,
    )
    original = wiring.ORIGINAL_CHILD_COMMAND

    result = (
        wiring
        .execute_pair06_v8_combat_priority_parent_supervisor_no_offload(
            **_kwargs()
        )
    )

    assert result == {
        "schema": "existing-parent-receipt",
        "automatic_retry": False,
    }
    command = observed["command"]
    assert command[0] == str(parent.PROTO_PYTHON)
    assert command[1:3] == ["-B", "-m"]
    assert command[3] == wiring.COMBAT_PRIORITY_CHILD_MODULE
    assert "--confirm" in command
    assert "--policy-confirm" in command
    assert observed["kwargs"]["execution_authorized"] is True
    assert parent._child_command is original


def test_parent_child_command_builder_restored_after_delegate_failure(
    monkeypatch,
):
    def fake_execute(**kwargs):
        assert parent._child_command is wiring._combat_priority_child_command
        raise RuntimeError("synthetic parent failure")

    monkeypatch.setattr(
        parent,
        "execute_pair06_v8_parent_supervisor_no_offload",
        fake_execute,
    )
    original = wiring.ORIGINAL_CHILD_COMMAND

    with pytest.raises(RuntimeError, match="synthetic parent failure"):
        wiring.execute_pair06_v8_combat_priority_parent_supervisor_no_offload(
            **_kwargs()
        )

    assert parent._child_command is original


def test_contract_preserves_no_offload_and_grants_no_runtime_authority():
    out = wiring.pair06_v8_combat_priority_parent_supervisor_wiring_contract()
    assert out["existing_no_offload_parent_source_modified"] is False
    assert out["existing_no_offload_model_loader_reused"] is True
    assert out["existing_cuda0_placement_checks_reused"] is True
    assert out["existing_parent_decision_service_loop_reused"] is True
    assert out["existing_child_retirement_reused"] is True
    assert out["existing_parent_receipt_returned_unchanged"] is True
    assert out["existing_parent_automatic_retry"] is False

    for field in (
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
    ):
        assert out[field] is False


def test_parent_wiring_advances_only_to_source_review():
    out = wiring.pair06_v8_combat_priority_parent_supervisor_wiring_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_PARENT_SUPERVISOR_WIRING_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_PARENT_SUPERVISOR_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        wiring.Pair06V8CombatPriorityParentWiringHold,
        match="PARENT_SUPERVISOR_WIRING_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        wiring.wire_operator_or_execute()
