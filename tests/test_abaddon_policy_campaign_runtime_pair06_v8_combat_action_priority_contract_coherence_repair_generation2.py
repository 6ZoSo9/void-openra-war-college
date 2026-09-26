from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_generation2
    as repair,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_runtime_integration_generation2
    as integration,
)


def _tool(name: str) -> dict:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": name,
            "parameters": {"type": "object", "properties": {}},
        },
    }


def _surface():
    names = [
        "attack_target",
        "move_units",
        "set_stance",
        "train_unit_e1",
        "build_structure_hbox",
        "advance",
    ]
    tools = [_tool(name) for name in names]
    contract = {
        "production_contract_version": "typed-production-functions-v1",
        "offered_tool_names": list(names),
        "legal_units": ["e1"],
        "legal_buildings": ["hbox"],
        "production_functions": {
            "train_unit_e1": {
                "kind": "build_unit",
                "value": "e1",
            },
            "build_structure_hbox": {
                "kind": "build_and_place",
                "value": "hbox",
            },
        },
    }
    return tools, contract


def _state(*, combat: int, visible: int) -> dict:
    return {
        "units_summary": [
            {"can_attack": True}
            for _ in range(combat)
        ],
        "enemy_summary": [
            {"id": f"enemy-{i}"}
            for i in range(visible)
        ],
        "enemy_buildings_summary": [],
    }


def test_visible_contact_prunes_suppressed_structure_production_mapping():
    tools, contract = _surface()
    out = repair.apply_pair06_v8_combat_action_priority_contract_coherence_repair(
        state=_state(combat=4, visible=1),
        typed_tools=tools,
        tool_contract=contract,
    )

    assert out["mode"] == "VISIBLE_CONTACT"
    assert "build_structure_hbox" not in out["tool_contract"]["offered_tool_names"]
    assert "build_structure_hbox" not in out["tool_contract"]["production_functions"]
    assert out["tool_contract"]["production_functions"] == {
        "train_unit_e1": {
            "kind": "build_unit",
            "value": "e1",
        },
    }
    assert out["suppressed_production_function_names"] == (
        "build_structure_hbox",
    )
    assert set(out["tool_contract"]["production_functions"]) <= set(
        out["tool_contract"]["offered_tool_names"]
    )


def test_recovery_keeps_only_currently_offered_recovery_production_mapping():
    tools, contract = _surface()
    out = repair.apply_pair06_v8_combat_action_priority_contract_coherence_repair(
        state=_state(combat=0, visible=0),
        typed_tools=tools,
        tool_contract=contract,
    )

    assert out["mode"] == "RECOVERY"
    assert out["tool_contract"]["offered_tool_names"] == ["train_unit_e1"]
    assert out["tool_contract"]["production_functions"] == {
        "train_unit_e1": {
            "kind": "build_unit",
            "value": "e1",
        },
    }


def test_normal_mode_preserves_original_production_mapping_exactly():
    tools, contract = _surface()
    out = repair.apply_pair06_v8_combat_action_priority_contract_coherence_repair(
        state=_state(combat=4, visible=0),
        typed_tools=tools,
        tool_contract=contract,
    )

    assert out["mode"] == "NORMAL"
    assert out["tool_contract"]["offered_tool_names"] == contract["offered_tool_names"]
    assert out["tool_contract"]["production_functions"] == contract["production_functions"]


def test_repair_does_not_mutate_inputs_or_legality_lists():
    tools, contract = _surface()
    before_tools = deepcopy(tools)
    before_contract = deepcopy(contract)

    out = repair.apply_pair06_v8_combat_action_priority_contract_coherence_repair(
        state=_state(combat=4, visible=1),
        typed_tools=tools,
        tool_contract=contract,
    )

    assert tools == before_tools
    assert contract == before_contract
    assert out["legal_units_preserved"] is True
    assert out["legal_buildings_preserved"] is True
    assert out["tool_contract"]["legal_units"] == contract["legal_units"]
    assert out["tool_contract"]["legal_buildings"] == contract["legal_buildings"]


def test_scoped_decision_hook_restores_historical_policy_function(monkeypatch):
    original = repair.ORIGINAL_POLICY_APPLY

    class FakeLegacy:
        def __init__(self):
            self.apollyon_decision_typed = lambda *args, **kwargs: None

        def apollyon_tools_typed(self, base, state, pending):
            return _surface()

        def decision_to_commands_typed(
            self,
            base,
            name,
            args,
            state,
            pending,
            pb2,
            contract,
        ):
            assert set(contract["production_functions"]) <= set(
                contract["offered_tool_names"]
            )
            return True, "ok", ["command"]

    class FakeBase:
        @staticmethod
        def compact_state(state):
            return _state(combat=4, visible=1)

    seen = {}

    def decider(**kwargs):
        seen["contract"] = deepcopy(kwargs["tool_contract"])
        return {
            "host_mutation_performed": False,
            "campaign_action": {
                "tool": "attack_target",
                "arguments": {},
            },
        }

    monkeypatch.setattr(integration, "_dependencies", lambda: {})
    monkeypatch.setattr(integration, "_validate_legacy_shape", lambda legacy: None)

    hooks = repair.Pair06V8CombatPriorityContractCoherentDecisionHooks(
        FakeLegacy(),
        decider,
    )
    hooks.install()
    try:
        result = hooks._adapted_decision(
            FakeBase(),
            None,
            {},
            None,
            None,
            "FEINTER",
            3,
        )
    finally:
        hooks.restore()

    assert result[0] == "attack_target"
    assert "build_structure_hbox" not in seen["contract"]["production_functions"]
    assert (
        integration.priority_policy.apply_pair06_v8_combat_action_priority_policy
        is original
    )


def test_repair_contract_grants_no_retry_or_runtime_authority():
    out = repair.pair06_v8_combat_action_priority_contract_coherence_repair_contract()
    assert out["production_functions_filtered_to_offered_surface"] is True
    assert out["policy_function_restored_in_finally"] is True
    for field in (
        "attempt_retry_authorized",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_repair_advances_only_to_source_binding_review():
    out = repair.pair06_v8_combat_action_priority_contract_coherence_repair_contract()
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        repair.Pair06V8CombatPriorityContractCoherenceHold,
        match="CONTRACT_COHERENCE_REPAIR_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        repair.wire_or_execute()
