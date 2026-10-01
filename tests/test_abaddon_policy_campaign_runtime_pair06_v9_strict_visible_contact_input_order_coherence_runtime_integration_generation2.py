from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_runtime_integration_generation2
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


class _Base:
    @staticmethod
    def compact_state(state):
        return deepcopy(state)


class _Legacy:
    def __init__(self, typed_order, offered_order):
        self.typed_order = list(typed_order)
        self.offered_order = list(offered_order)
        self.apollyon_decision_typed = self._original
        self.validation_calls = []

    def _original(self, *args, **kwargs):
        return "original"

    def apollyon_tools_typed(self, base, state, pending):
        production_all = {
            "train_unit_e1": {
                "kind": "build_unit",
                "unit_type": "e1",
            },
        }
        contract = {
            "offered_tool_names": list(self.offered_order),
            "legal_units": ["e1"],
            "legal_buildings": [],
            "production_functions": {
                name: deepcopy(action)
                for name, action in production_all.items()
                if name in self.offered_order
            },
        }
        return [_tool(name) for name in self.typed_order], contract

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
        self.validation_calls.append({
            "name": name,
            "offered": tuple(contract["offered_tool_names"]),
            "production": tuple(contract["production_functions"]),
            "legal_units": tuple(contract["legal_units"]),
            "legal_buildings": tuple(contract["legal_buildings"]),
        })
        if name not in set(contract["offered_tool_names"]):
            return False, "not_offered", []
        return True, "accepted", [("command", name)]


def _state(combat: int, visible: int):
    return {
        "units_summary": [
            {"id": index + 1, "type": "e1", "can_attack": True}
            for index in range(combat)
        ],
        "enemy_summary": [
            {"id": 100 + index, "type": "e1"}
            for index in range(visible)
        ],
        "enemy_buildings_summary": [],
    }


def _result(tool: str):
    return {
        "host_mutation_performed": False,
        "campaign_action": {
            "tool": tool,
            "arguments": {},
        },
    }


def test_contract_pins_repair_and_historical_runtime_integration():
    out = integration.pair06_v9_input_order_coherence_runtime_integration_contract()

    assert out["repair_git_blob"] == (
        "917ed6c5800278abfb56f4afbae5349b3ad4b7d7"
    )
    assert out["repair_review_git_blob"] == (
        "132ef2916e72cf25cafab1ee368c06083d918e20"
    )
    assert out["historical_runtime_integration_git_blob"] == (
        "8aa8a3bae62a914dfa1c1b7daf2fca6b13ecf2ef"
    )
    assert out["historical_runtime_integration_review_git_blob"] == (
        "9e92605527aeea59f9d99cfcb798adea569f7309"
    )


def test_order_only_drift_reaches_historical_v9_policy_and_host_validator():
    typed_order = [
        "move_units",
        "attack_target",
        "train_unit_e1",
        "set_stance",
    ]
    offered_order = sorted(typed_order)
    legacy = _Legacy(typed_order, offered_order)
    seen = []

    def decider(**kwargs):
        seen.append(deepcopy(kwargs))
        return _result("attack_target")

    hooks = integration.Pair06V9InputOrderCoherentDecisionHooks(
        legacy,
        decider,
    )
    hooks.install()
    try:
        result = legacy.apollyon_decision_typed(
            _Base(),
            object(),
            _state(2, 1),
            {},
            object(),
            "FEINTER",
            1,
        )
    finally:
        hooks.restore()

    assert result[0] == "attack_target"
    assert tuple(
        tool["function"]["name"]
        for tool in seen[0]["typed_tools"]
    ) == (
        "attack_target",
        "move_units",
        "set_stance",
    )
    assert tuple(seen[0]["tool_contract"]["offered_tool_names"]) == (
        "attack_target",
        "move_units",
        "set_stance",
    )
    assert seen[0]["tool_contract"]["production_functions"] == {}
    assert seen[0]["tool_contract"]["legal_units"] == []
    assert len(legacy.validation_calls) == 1
    assert legacy.validation_calls[0]["name"] == "attack_target"


def test_membership_drift_still_fails_closed_before_decider():
    legacy = _Legacy(
        ["attack_target", "set_stance"],
        ["attack_target", "set_stance", "train_unit_e1"],
    )
    calls = []

    hooks = integration.Pair06V9InputOrderCoherentDecisionHooks(
        legacy,
        lambda **kwargs: calls.append(kwargs) or _result("attack_target"),
    )
    hooks.install()
    try:
        with pytest.raises(
            integration.repair.Pair06V9InputOrderCoherenceRepairHold,
            match="membership differs",
        ):
            legacy.apollyon_decision_typed(
                _Base(),
                object(),
                _state(2, 1),
                {},
                object(),
                "FEINTER",
                1,
            )
    finally:
        hooks.restore()

    assert calls == []
    assert legacy.validation_calls == []


def test_scoped_policy_substitution_restores_after_success():
    original = integration.ORIGINAL_V9_POLICY_APPLY
    typed_order = ["move_units", "attack_target", "set_stance"]
    legacy = _Legacy(typed_order, sorted(typed_order))

    hooks = integration.Pair06V9InputOrderCoherentDecisionHooks(
        legacy,
        lambda **kwargs: _result("attack_target"),
    )
    hooks.install()
    try:
        legacy.apollyon_decision_typed(
            _Base(),
            object(),
            _state(2, 1),
            {},
            object(),
            "FEINTER",
            1,
        )
    finally:
        hooks.restore()

    assert (
        integration.historical_integration.strict_policy
        .apply_pair06_v9_strict_visible_contact_policy
        is original
    )


def test_scoped_policy_substitution_restores_after_failure():
    original = integration.ORIGINAL_V9_POLICY_APPLY
    legacy = _Legacy(
        ["attack_target"],
        ["attack_target", "train_unit_e1"],
    )

    hooks = integration.Pair06V9InputOrderCoherentDecisionHooks(
        legacy,
        lambda **kwargs: _result("attack_target"),
    )
    hooks.install()
    try:
        with pytest.raises(
            integration.repair.Pair06V9InputOrderCoherenceRepairHold,
        ):
            legacy.apollyon_decision_typed(
                _Base(),
                object(),
                _state(2, 1),
                {},
                object(),
                "FEINTER",
                1,
            )
    finally:
        hooks.restore()

    assert (
        integration.historical_integration.strict_policy
        .apply_pair06_v9_strict_visible_contact_policy
        is original
    )


def test_contract_preserves_historical_runtime_and_grants_no_retry():
    out = integration.pair06_v9_input_order_coherence_runtime_integration_contract()

    assert out["historical_v9_policy_source_modified"] is False
    assert out["historical_v9_runtime_integration_source_modified"] is False
    assert out["scoped_policy_function_substitution_implemented"] is True
    assert out["policy_function_restored_in_finally"] is True
    assert out["typed_tool_membership_exact_match_required"] is True
    assert out["typed_tool_order_canonicalized_to_offered_order"] is True
    assert out["membership_drift_still_fail_closed"] is True
    assert out["unchanged_legacy_host_validator_reused"] is True
    assert out["six_attempt_fail_closed_loop_reused"] is True
    assert out["frozen_compact_state_reused"] is True
    assert out["consumed_v9_attempt_retry_authorized"] is False

    for field in (
        "proto_child_repair_wiring_implemented",
        "parent_supervisor_repair_wiring_implemented",
        "operator_repair_wiring_implemented",
        "new_execution_request_opened",
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
        "scheduler_mutation_authorized",
    ):
        assert out[field] is False


def test_integration_advances_only_to_source_review():
    out = integration.pair06_v9_input_order_coherence_runtime_integration_contract()

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "RUNTIME_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "RUNTIME_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_entrypoint_holds():
    with pytest.raises(
        integration.Pair06V9InputOrderCoherenceRuntimeIntegrationHold,
        match="RUNTIME_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        integration.review_wire_or_execute()
