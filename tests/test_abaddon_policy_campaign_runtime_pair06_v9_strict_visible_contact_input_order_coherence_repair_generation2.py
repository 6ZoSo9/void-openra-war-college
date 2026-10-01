from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_repair_generation2
    as repair,
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


def _state(combat: int, visible: int) -> dict:
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


def _contract(names: list[str]) -> dict:
    return {
        "offered_tool_names": list(names),
        "legal_units": ["e1"],
        "legal_buildings": [],
        "production_functions": {
            "train_unit_e1": {
                "kind": "build_unit",
                "unit_type": "e1",
            }
        } if "train_unit_e1" in names else {},
    }


def test_contract_records_exact_runtime_failure_without_retry_authority():
    out = repair.pair06_v9_input_order_coherence_repair_contract()

    assert out["historical_policy_git_blob"] == (
        "e3930101947430deecc03013088ad9ccfd1d901e"
    )
    assert out["runtime_failure_signature"] == (
        "typed tools and offered_tool_names order or membership disagree"
    )
    assert out["historical_v9_policy_source_modified"] is False
    assert out["typed_tool_membership_exact_match_required"] is True
    assert out["typed_tool_order_may_differ_on_input"] is True
    assert out["typed_tool_order_canonicalized_to_offered_order"] is True
    assert out["membership_drift_still_fail_closed"] is True
    assert out["consumed_v9_attempt_retry_authorized"] is False


def test_order_only_drift_is_canonicalized_before_historical_policy():
    offered = ["set_stance", "attack_target", "train_unit_e1"]
    tools = [
        _tool("attack_target"),
        _tool("train_unit_e1"),
        _tool("set_stance"),
    ]

    out = repair.apply_pair06_v9_input_order_coherence_repair(
        state=_state(2, 1),
        typed_tools=tools,
        tool_contract=_contract(offered),
    )

    assert out["input_typed_tool_names"] == (
        "attack_target",
        "train_unit_e1",
        "set_stance",
    )
    assert out["input_offered_tool_names"] == tuple(offered)
    assert out["input_membership_matched"] is True
    assert out["input_order_matched"] is False
    assert out["input_order_canonicalized"] is True
    assert out["canonical_typed_tool_names"] == tuple(offered)

    # STRICT_VISIBLE_CONTACT suppresses reinforcement after canonicalization.
    assert out["mode"] == "STRICT_VISIBLE_CONTACT"
    assert out["filtered_offered_tool_names"] == (
        "set_stance",
        "attack_target",
    )
    assert tuple(
        tool["function"]["name"] for tool in out["typed_tools"]
    ) == (
        "set_stance",
        "attack_target",
    )


def test_already_aligned_order_is_preserved_without_false_repair_flag():
    names = ["advance", "train_unit_e1", "attack_move"]
    out = repair.apply_pair06_v9_input_order_coherence_repair(
        state=_state(2, 0),
        typed_tools=[_tool(name) for name in names],
        tool_contract=_contract(names),
    )

    assert out["mode"] == "NORMAL"
    assert out["input_order_matched"] is True
    assert out["input_order_canonicalized"] is False
    assert out["canonical_typed_tool_names"] == tuple(names)
    assert out["tool_contract"] == _contract(names)


def test_membership_drift_still_fails_closed():
    with pytest.raises(
        repair.Pair06V9InputOrderCoherenceRepairHold,
        match="membership differs",
    ):
        repair.apply_pair06_v9_input_order_coherence_repair(
            state=_state(1, 1),
            typed_tools=[
                _tool("attack_target"),
                _tool("set_stance"),
            ],
            tool_contract=_contract(
                ["attack_target", "set_stance", "train_unit_e1"]
            ),
        )


def test_duplicate_typed_tool_name_still_fails_closed():
    with pytest.raises(
        repair.Pair06V9InputOrderCoherenceRepairHold,
        match="typed tool names contain duplicates",
    ):
        repair.apply_pair06_v9_input_order_coherence_repair(
            state=_state(1, 1),
            typed_tools=[
                _tool("attack_target"),
                _tool("attack_target"),
            ],
            tool_contract=_contract(["attack_target"]),
        )


def test_inputs_are_not_mutated():
    state = _state(2, 1)
    tools = [_tool("attack_target"), _tool("set_stance")]
    contract = _contract(["set_stance", "attack_target"])
    state_before = deepcopy(state)
    tools_before = deepcopy(tools)
    contract_before = deepcopy(contract)

    repair.apply_pair06_v9_input_order_coherence_repair(
        state=state,
        typed_tools=tools,
        tool_contract=contract,
    )

    assert state == state_before
    assert tools == tools_before
    assert contract == contract_before


@pytest.mark.parametrize(
    "field",
    (
        "consumed_v9_attempt_retry_authorized",
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
    ),
)
def test_repair_grants_no_effect_or_retry_authority(field):
    out = repair.pair06_v9_input_order_coherence_repair_contract()
    assert out[field] is False


def test_repair_advances_only_to_source_review():
    out = repair.pair06_v9_input_order_coherence_repair_contract()

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_REPAIR_"
        "SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_REPAIR_"
        "SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_review_or_execute_holds():
    with pytest.raises(
        repair.Pair06V9InputOrderCoherenceRepairHold,
        match="INPUT_ORDER_COHERENCE_REPAIR_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        repair.review_or_execute()
