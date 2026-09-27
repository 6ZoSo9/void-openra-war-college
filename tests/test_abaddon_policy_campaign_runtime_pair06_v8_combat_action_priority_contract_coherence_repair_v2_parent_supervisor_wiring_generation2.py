from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_parent_supervisor_wiring_generation2
    as v1_parent,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_parent_supervisor_wiring_generation2
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
        "execution_authorized": True,
        "authority_check": lambda slot, arm: slot == 6 and arm == "baseline",
    }


def test_contract_binds_v2_child_review_and_v1_parent():
    out = wiring.pair06_v8_combat_priority_coherent_v2_parent_wiring_contract()

    assert out["v2_child_review_main_head"] == (
        "c06de6b1a3b52e689064cd007e8d780dbcfcc9ce"
    )
    assert out["v2_child_review_git_blob"] == (
        "028565625eca8672e90126ec335d07279ae5d6d3"
    )
    assert out["v2_child_review_source_sha256"] == (
        "d4d94d94df6cf123c0a9c102f57c84f1d5dacce710094057509fe8311c6592a5"
    )
    assert out["v1_coherent_parent_wiring_git_blob"] == (
        "fa3dcc13b9150a88e12c8fee005f7bf16670a236"
    )
    assert out["v1_coherent_parent_wiring_source_modified"] is False


def test_v2_child_command_targets_v2_entrypoint():
    command = wiring._v2_child_command(
        child_fd=9,
        attempt_id="a" * 64,
        runs_root="/runs",
        frozen_source_root="/source",
        exact_engine_root="/engine",
    )
    assert command[1:3] == ["-B", "-m"]
    assert command[3] == wiring.V2_CHILD_MODULE
    assert "--confirm" in command
    assert "--policy-confirm" in command


def test_parent_wrapper_scopes_v2_builder_and_restores(monkeypatch):
    original = wiring.ORIGINAL_V1_COHERENT_CHILD_COMMAND
    observed = {}

    monkeypatch.setattr(wiring, "_dependencies", lambda: {})
    monkeypatch.setattr(v1_parent, "_coherent_child_command", original)

    def fake_execute(**kwargs):
        observed["builder"] = v1_parent._coherent_child_command
        observed["kwargs"] = kwargs
        return {"schema": "synthetic-v1-coherent-parent-receipt"}

    monkeypatch.setattr(
        v1_parent,
        "execute_pair06_v8_combat_priority_coherent_parent_supervisor_no_offload",
        fake_execute,
    )

    result = (
        wiring
        .execute_pair06_v8_combat_priority_coherent_v2_parent_supervisor_no_offload(
            **_kwargs()
        )
    )

    assert result == {"schema": "synthetic-v1-coherent-parent-receipt"}
    assert observed["builder"] is wiring._v2_child_command
    assert observed["kwargs"]["policy_activation_authorized"] is True
    assert observed["kwargs"]["execution_authorized"] is True
    assert v1_parent._coherent_child_command is original


def test_parent_wrapper_restores_v1_builder_after_failure(monkeypatch):
    original = wiring.ORIGINAL_V1_COHERENT_CHILD_COMMAND

    monkeypatch.setattr(wiring, "_dependencies", lambda: {})
    monkeypatch.setattr(v1_parent, "_coherent_child_command", original)

    def fail(**kwargs):
        assert v1_parent._coherent_child_command is wiring._v2_child_command
        raise RuntimeError("synthetic V1 coherent parent failure")

    monkeypatch.setattr(
        v1_parent,
        "execute_pair06_v8_combat_priority_coherent_parent_supervisor_no_offload",
        fail,
    )

    with pytest.raises(RuntimeError, match="synthetic V1 coherent parent failure"):
        wiring.execute_pair06_v8_combat_priority_coherent_v2_parent_supervisor_no_offload(
            **_kwargs()
        )

    assert v1_parent._coherent_child_command is original


def test_parent_wrapper_requires_both_authorities(monkeypatch):
    monkeypatch.setattr(wiring, "_dependencies", lambda: {})

    values = _kwargs()
    values["policy_activation_authorized"] = False
    with pytest.raises(
        wiring.Pair06V8CombatPriorityCoherentV2ParentWiringHold,
        match="POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
    ):
        wiring.execute_pair06_v8_combat_priority_coherent_v2_parent_supervisor_no_offload(
            **values
        )

    values = _kwargs()
    values["execution_authorized"] = False
    with pytest.raises(
        wiring.Pair06V8CombatPriorityCoherentV2ParentWiringHold,
        match="GAME_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        wiring.execute_pair06_v8_combat_priority_coherent_v2_parent_supervisor_no_offload(
            **values
        )


def test_contract_seals_consumed_attempt_and_grants_no_retry():
    out = wiring.pair06_v8_combat_priority_coherent_v2_parent_wiring_contract()

    assert out["translator_legal_building_mapping_coherent"] is True
    assert out["translator_legal_unit_mapping_coherent"] is True
    assert out["consumed_attempt_marker_sha256"] == (
        "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
    )
    assert out["consumed_attempt_reusable"] is False
    assert out["prior_authorization_reusable"] is False

    for field in (
        "attempt_retry_authorized",
        "operator_invocation_v2_wiring_implemented",
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
    out = wiring.pair06_v8_combat_priority_coherent_v2_parent_wiring_contract()
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_PARENT_SUPERVISOR_WIRING_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        wiring.Pair06V8CombatPriorityCoherentV2ParentWiringHold,
        match="REPAIR_V2_PARENT_SUPERVISOR_WIRING_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        wiring.wire_operator_or_execute()
