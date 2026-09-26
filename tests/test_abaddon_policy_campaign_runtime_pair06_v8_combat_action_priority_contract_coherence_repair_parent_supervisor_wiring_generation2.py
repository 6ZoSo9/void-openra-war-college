from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_parent_supervisor_wiring_generation2
    as wiring,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_parent_supervisor_wiring_generation2
    as historical_parent,
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


def test_contract_binds_coherent_child_and_historical_parent():
    out = wiring.pair06_v8_combat_priority_coherent_parent_wiring_contract()
    assert out["coherent_child_review_main_head"] == (
        "b3293e69790ad90b02ae7e38fc4b078c1c15c707"
    )
    assert out["coherent_child_review_git_blob"] == (
        "b8aa17ee161f2b2377ef6d80f1408d04268a2f22"
    )
    assert out["historical_parent_wiring_git_blob"] == (
        "c30cf75b26d5e0cecee08286717d8a856e2233bd"
    )
    assert out["historical_parent_wiring_source_modified"] is False


def test_coherent_child_command_targets_coherent_entrypoint():
    command = wiring._coherent_child_command(
        child_fd=9,
        attempt_id="a" * 64,
        runs_root="/runs",
        frozen_source_root="/source",
        exact_engine_root="/engine",
    )
    assert command[1:3] == ["-B", "-m"]
    assert command[3] == wiring.COHERENT_CHILD_MODULE
    assert "--confirm" in command
    assert "--policy-confirm" in command


def test_parent_wrapper_scopes_builder_and_restores(monkeypatch):
    original = wiring.ORIGINAL_HISTORICAL_CHILD_COMMAND
    observed = {}
    monkeypatch.setattr(wiring, "_dependencies", lambda: {})
    monkeypatch.setattr(
        historical_parent,
        "_combat_priority_child_command",
        original,
    )

    def fake_execute(**kwargs):
        observed["builder"] = historical_parent._combat_priority_child_command
        observed["kwargs"] = kwargs
        return {"schema": "historical-parent-receipt"}

    monkeypatch.setattr(
        historical_parent,
        "execute_pair06_v8_combat_priority_parent_supervisor_no_offload",
        fake_execute,
    )

    result = wiring.execute_pair06_v8_combat_priority_coherent_parent_supervisor_no_offload(
        **_kwargs()
    )

    assert result == {"schema": "historical-parent-receipt"}
    assert observed["builder"] is wiring._coherent_child_command
    assert observed["kwargs"]["policy_activation_authorized"] is True
    assert observed["kwargs"]["execution_authorized"] is True
    assert historical_parent._combat_priority_child_command is original


def test_parent_wrapper_restores_builder_after_failure(monkeypatch):
    original = wiring.ORIGINAL_HISTORICAL_CHILD_COMMAND
    monkeypatch.setattr(wiring, "_dependencies", lambda: {})
    monkeypatch.setattr(
        historical_parent,
        "_combat_priority_child_command",
        original,
    )

    def fail(**kwargs):
        assert historical_parent._combat_priority_child_command is (
            wiring._coherent_child_command
        )
        raise RuntimeError("synthetic parent failure")

    monkeypatch.setattr(
        historical_parent,
        "execute_pair06_v8_combat_priority_parent_supervisor_no_offload",
        fail,
    )

    with pytest.raises(RuntimeError, match="synthetic parent failure"):
        wiring.execute_pair06_v8_combat_priority_coherent_parent_supervisor_no_offload(
            **_kwargs()
        )

    assert historical_parent._combat_priority_child_command is original


def test_parent_wrapper_requires_both_authorities(monkeypatch):
    monkeypatch.setattr(wiring, "_dependencies", lambda: {})

    values = _kwargs()
    values["policy_activation_authorized"] = False
    with pytest.raises(
        wiring.Pair06V8CombatPriorityCoherentParentWiringHold,
        match="POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
    ):
        wiring.execute_pair06_v8_combat_priority_coherent_parent_supervisor_no_offload(
            **values
        )

    values = _kwargs()
    values["execution_authorized"] = False
    with pytest.raises(
        wiring.Pair06V8CombatPriorityCoherentParentWiringHold,
        match="GAME_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        wiring.execute_pair06_v8_combat_priority_coherent_parent_supervisor_no_offload(
            **values
        )


def test_contract_seals_consumed_attempt_and_grants_no_retry():
    out = wiring.pair06_v8_combat_priority_coherent_parent_wiring_contract()
    assert out["production_functions_filtered_to_offered_surface"] is True
    assert out["consumed_attempt_marker_sha256"] == (
        "90d20bf736fc4b101cfbaab8cd70ee58bb3797c3eff315fae8bd5e59469382cf"
    )
    assert out["consumed_attempt_reusable"] is False
    for field in (
        "attempt_retry_authorized",
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
    out = wiring.pair06_v8_combat_priority_coherent_parent_wiring_contract()
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_PARENT_SUPERVISOR_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        wiring.Pair06V8CombatPriorityCoherentParentWiringHold,
        match="REPAIR_PARENT_SUPERVISOR_WIRING_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        wiring.wire_operator_or_execute()
