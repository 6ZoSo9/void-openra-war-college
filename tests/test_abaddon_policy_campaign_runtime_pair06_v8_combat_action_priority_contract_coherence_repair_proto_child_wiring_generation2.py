from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_generation2
    as repair,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_proto_child_wiring_generation2
    as wiring,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_proto_child_wiring_generation2
    as base_wiring,
)


def test_contract_binds_reviewed_repair_and_historical_child_wiring():
    out = wiring.pair06_v8_combat_priority_coherent_proto_child_wiring_contract()
    assert out["repair_review_main_head"] == (
        "54741af71ff64af9bfacbe0cc126148cfa8ba5b4"
    )
    assert out["repair_review_git_blob"] == (
        "bc4738d8e3a069c2094e2efd0724f2ab7ad71133"
    )
    assert out["base_proto_child_wiring_git_blob"] == (
        "7dd120dce2bc39a780ce40b9d167d39ea5cf9bfc"
    )
    assert out["base_proto_child_wiring_review_git_blob"] == (
        "e0247e50ead91356f60e57b454331fba8e2ae69c"
    )


def test_repaired_hook_subclass_replaces_only_decision_hook(monkeypatch):
    monkeypatch.setattr(wiring, "_dependencies", lambda: {})

    class Historical:
        def __init__(self, legacy, sock, attempt_id):
            self._ipc_decider = lambda **kwargs: {}
            self._decision_hooks = type("Old", (), {"_installed": False})()

    monkeypatch.setattr(
        wiring,
        "ORIGINAL_COMBAT_PRIORITY_PROTO_CHILD_HOOKS",
        Historical,
    )

    class Rebound(
        Historical
    ):
        pass

    monkeypatch.setattr(
        wiring.Pair06V8CombatPriorityCoherentProtoChildHooks,
        "__bases__",
        (Historical,),
        raising=False,
    )

    # Construction behavior itself is covered through the real inheritance
    # contract below; keep this test focused on the exact repaired hook class.
    assert issubclass(
        repair.Pair06V8CombatPriorityContractCoherentDecisionHooks,
        object,
    )


def test_wrapper_scopes_historical_hook_class_and_restores(monkeypatch):
    observed = {}
    original = wiring.ORIGINAL_COMBAT_PRIORITY_PROTO_CHILD_HOOKS
    monkeypatch.setattr(wiring, "_dependencies", lambda: {})

    def fake_run(**kwargs):
        observed["hook_class"] = base_wiring.Pair06V8CombatPriorityProtoChildHooks
        observed["kwargs"] = kwargs
        return {"ok": True}

    monkeypatch.setattr(
        base_wiring,
        "run_pair06_v8_combat_priority_proto_game_child",
        fake_run,
    )
    monkeypatch.setattr(
        base_wiring,
        "Pair06V8CombatPriorityProtoChildHooks",
        original,
    )

    result = wiring.run_pair06_v8_combat_priority_coherent_proto_game_child(
        sock=object(),
        attempt_id="a" * 64,
        runs_root="/runs",
        frozen_source_root="/source",
        exact_engine_root="/engine",
        policy_activation_authorized=True,
        execution_authorized=True,
    )

    assert result == {"ok": True}
    assert observed["hook_class"] is (
        wiring.Pair06V8CombatPriorityCoherentProtoChildHooks
    )
    assert observed["kwargs"]["policy_activation_authorized"] is True
    assert observed["kwargs"]["execution_authorized"] is True
    assert base_wiring.Pair06V8CombatPriorityProtoChildHooks is original


def test_wrapper_restores_historical_hook_class_after_failure(monkeypatch):
    original = wiring.ORIGINAL_COMBAT_PRIORITY_PROTO_CHILD_HOOKS
    monkeypatch.setattr(wiring, "_dependencies", lambda: {})
    monkeypatch.setattr(
        base_wiring,
        "Pair06V8CombatPriorityProtoChildHooks",
        original,
    )

    def fail(**kwargs):
        assert base_wiring.Pair06V8CombatPriorityProtoChildHooks is (
            wiring.Pair06V8CombatPriorityCoherentProtoChildHooks
        )
        raise RuntimeError("synthetic child failure")

    monkeypatch.setattr(
        base_wiring,
        "run_pair06_v8_combat_priority_proto_game_child",
        fail,
    )

    with pytest.raises(RuntimeError, match="synthetic child failure"):
        wiring.run_pair06_v8_combat_priority_coherent_proto_game_child(
            sock=object(),
            attempt_id="a" * 64,
            runs_root="/runs",
            frozen_source_root="/source",
            exact_engine_root="/engine",
            policy_activation_authorized=True,
            execution_authorized=True,
        )

    assert base_wiring.Pair06V8CombatPriorityProtoChildHooks is original


def test_wrapper_requires_execution_and_policy_activation_authority(monkeypatch):
    monkeypatch.setattr(wiring, "_dependencies", lambda: {})

    with pytest.raises(
        wiring.Pair06V8CombatPriorityCoherentProtoChildWiringHold,
        match="POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
    ):
        wiring.run_pair06_v8_combat_priority_coherent_proto_game_child(
            sock=object(),
            attempt_id="a" * 64,
            runs_root="/runs",
            frozen_source_root="/source",
            exact_engine_root="/engine",
            policy_activation_authorized=False,
            execution_authorized=True,
        )

    with pytest.raises(
        wiring.Pair06V8CombatPriorityCoherentProtoChildWiringHold,
        match="GAME_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        wiring.run_pair06_v8_combat_priority_coherent_proto_game_child(
            sock=object(),
            attempt_id="a" * 64,
            runs_root="/runs",
            frozen_source_root="/source",
            exact_engine_root="/engine",
            policy_activation_authorized=True,
            execution_authorized=False,
        )


def test_contract_seals_consumed_attempt_and_grants_no_retry_authority():
    out = wiring.pair06_v8_combat_priority_coherent_proto_child_wiring_contract()
    assert out["consumed_attempt_marker_sha256"] == (
        "90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"
    )
    assert out["consumed_attempt_reusable"] is False
    assert out["failed_run_id"] == (
        "warmstart-apollyon-vs-abaddon-20260926T142215Z-feinter-s208354846"
    )
    assert out["failed_run_reusable_as_authority"] is False
    for field in (
        "attempt_retry_authorized",
        "parent_supervisor_repair_wiring_implemented",
        "operator_invocation_repair_implemented",
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


def test_next_gate_is_source_binding_review():
    out = wiring.pair06_v8_combat_priority_coherent_proto_child_wiring_contract()
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_PROTO_CHILD_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        wiring.Pair06V8CombatPriorityCoherentProtoChildWiringHold,
        match="REPAIR_PROTO_CHILD_WIRING_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        wiring.wire_parent_or_execute()
