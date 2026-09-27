from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import apollyon_v10_campaign_translation as translator
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_generation2
    as repair_v1,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_generation2
    as repair_v2,
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
                "unit_type": "e1",
            },
            "build_structure_hbox": {
                "kind": "build_and_place",
                "building_type": "hbox",
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


def test_visible_contact_reconstructs_legality_and_passes_translator_validator():
    tools, contract = _surface()
    out = (
        repair_v2
        .apply_pair06_v8_combat_action_priority_contract_coherence_repair_v2(
            state=_state(combat=4, visible=1),
            typed_tools=tools,
            tool_contract=contract,
        )
    )

    assert out["mode"] == "VISIBLE_CONTACT"
    assert out["tool_contract"]["production_functions"] == {
        "train_unit_e1": {
            "kind": "build_unit",
            "unit_type": "e1",
        },
    }
    assert out["tool_contract"]["legal_units"] == ["e1"]
    assert out["tool_contract"]["legal_buildings"] == []
    translator._validate_tool_contract(out["tool_contract"])


def test_recovery_reconstructs_legality_and_passes_translator_validator():
    tools, contract = _surface()
    out = (
        repair_v2
        .apply_pair06_v8_combat_action_priority_contract_coherence_repair_v2(
            state=_state(combat=0, visible=0),
            typed_tools=tools,
            tool_contract=contract,
        )
    )

    assert out["mode"] == "RECOVERY"
    assert out["tool_contract"]["offered_tool_names"] == ["train_unit_e1"]
    assert out["tool_contract"]["legal_units"] == ["e1"]
    assert out["tool_contract"]["legal_buildings"] == []
    translator._validate_tool_contract(out["tool_contract"])


def test_normal_mode_preserves_complete_contract_exactly():
    tools, contract = _surface()
    out = (
        repair_v2
        .apply_pair06_v8_combat_action_priority_contract_coherence_repair_v2(
            state=_state(combat=4, visible=0),
            typed_tools=tools,
            tool_contract=contract,
        )
    )

    assert out["mode"] == "NORMAL"
    assert out["tool_contract"] == contract
    translator._validate_tool_contract(out["tool_contract"])


def test_v2_does_not_mutate_inputs():
    tools, contract = _surface()
    before_tools = deepcopy(tools)
    before_contract = deepcopy(contract)

    repair_v2.apply_pair06_v8_combat_action_priority_contract_coherence_repair_v2(
        state=_state(combat=4, visible=1),
        typed_tools=tools,
        tool_contract=contract,
    )

    assert tools == before_tools
    assert contract == before_contract


def test_v2_rejects_mapping_outside_reviewed_legality():
    tools, contract = _surface()
    contract["production_functions"]["build_structure_hbox"][
        "building_type"
    ] = "weap"

    with pytest.raises(
        repair_v2.Pair06V8CombatPriorityContractCoherenceV2Hold,
        match="mapped building escaped reviewed legal_buildings",
    ):
        repair_v2.apply_pair06_v8_combat_action_priority_contract_coherence_repair_v2(
            state=_state(combat=4, visible=0),
            typed_tools=tools,
            tool_contract=contract,
        )


def test_scoped_v2_hook_delivers_translator_valid_filtered_contract(monkeypatch):
    original_policy = repair_v1.ORIGINAL_POLICY_APPLY
    original_v1 = repair_v2.ORIGINAL_V1_REPAIR_APPLY

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
            translator._validate_tool_contract(contract)
            return True, "ok", ["command"]

    class FakeBase:
        @staticmethod
        def compact_state(state):
            return _state(combat=4, visible=1)

    seen = {}

    def decider(**kwargs):
        seen["contract"] = deepcopy(kwargs["tool_contract"])
        translator._validate_tool_contract(seen["contract"])
        return {
            "host_mutation_performed": False,
            "campaign_action": {
                "tool": "attack_target",
                "arguments": {},
            },
        }

    monkeypatch.setattr(integration, "_dependencies", lambda: {})
    monkeypatch.setattr(integration, "_validate_legacy_shape", lambda legacy: None)

    hooks = repair_v2.Pair06V8CombatPriorityContractCoherentV2DecisionHooks(
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
    assert seen["contract"]["legal_buildings"] == []
    assert seen["contract"]["legal_units"] == ["e1"]
    assert (
        repair_v1
        .apply_pair06_v8_combat_action_priority_contract_coherence_repair
        is original_v1
    )
    assert (
        integration.priority_policy.apply_pair06_v8_combat_action_priority_policy
        is original_policy
    )


def test_v2_contract_grants_no_retry_or_runtime_authority():
    out = (
        repair_v2
        .pair06_v8_combat_action_priority_contract_coherence_repair_v2_contract()
    )
    assert out["repair_v2_implemented"] is True
    assert out["translator_legal_building_mapping_invariant_required"] is True
    assert out["translator_legal_unit_mapping_invariant_required"] is True

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


def test_v2_advances_only_to_source_binding_review():
    out = (
        repair_v2
        .pair06_v8_combat_action_priority_contract_coherence_repair_v2_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_COMBAT_ACTION_PRIORITY_CONTRACT_COHERENCE_REPAIR_V2_SOURCE_BINDING_REVIEW_REQUIRED",
    )


def test_entrypoint_holds():
    with pytest.raises(
        repair_v2.Pair06V8CombatPriorityContractCoherenceV2Hold,
        match="CONTRACT_COHERENCE_REPAIR_V2_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        repair_v2.wire_or_execute()
