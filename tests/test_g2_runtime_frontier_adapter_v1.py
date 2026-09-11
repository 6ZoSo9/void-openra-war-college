
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from openra_env.learning.g2_runtime_capability_projection import (
    CAPABILITIES,
    PROJECTION_SPEC_SHA256,
    canonical_json_bytes,
    project_live_game_state,
)
from openra_env.learning.g2_runtime_candidate_frontier import (
    action_identity_sha256,
    build_candidate_frontier,
    canonical_action_key,
)
from openra_env.learning.g2_runtime_compiled_comparator_gate import (
    EXPECTED_COMPARATOR_SHA256,
    G2RuntimeFrontierHold,
    RuntimeFrontierController,
    apply_compiled_comparator_gate,
    load_accepted_comparator,
)
from openra_env.learning.g2_runtime_tool_classification import (
    MUTATION_CAPABLE,
    OBSERVATION_CONTROL,
    ToolClassificationHold,
    classify_tool,
    validate_discovered_tool_surface,
)

ACCEPTED_COMPARATOR_SOURCE = '#!/usr/bin/env python3\n"""VOID Generation-2 compiled lexicographic policy comparator V1.\n\nPure deterministic tactical competence comparator.\n\nThis artifact is compiled from the reviewed V4/V5/V6 policy semantics.\nIt is NOT learned from examples and contains no trained weights.\n"""\nfrom __future__ import annotations\n\nimport hashlib\n\nSCHEMA = "void.generals.g2-compiled-lexicographic-comparator.v1"\nCANDIDATE_ID = "apollyon-g2-compiled-lexicographic-comparator-v1"\nSCOPE = "tactical_competence_only"\nCOMPARISON = "lexicographic_maximize_left_to_right"\n\nBRANCH_FEATURES = {\n    "restorative_available": (\n        "restorative_for_current_deficit",\n        "projected_min_capability",\n        "deficit_total_effect",\n        "projected_total_capability",\n    ),\n    "fallback_no_restorative": (\n        "projected_min_capability",\n        "projected_deficient_capability",\n        "projected_total_capability",\n    ),\n}\n\ndef normalize_tuple(branch, values):\n    if branch not in BRANCH_FEATURES:\n        raise ValueError("unknown_branch:" + str(branch))\n    if not isinstance(values, (list, tuple)):\n        raise TypeError("policy_tuple_not_sequence")\n    if len(values) != len(BRANCH_FEATURES[branch]):\n        raise ValueError(\n            "policy_tuple_dimension:"\n            + branch\n            + ":expected="\n            + str(len(BRANCH_FEATURES[branch]))\n            + ":actual="\n            + str(len(values))\n        )\n    out = tuple(values)\n    for value in out:\n        if isinstance(value, bool):\n            continue\n        if not isinstance(value, (int, float)):\n            raise TypeError("policy_tuple_non_numeric:" + repr(value))\n    return out\n\ndef compare(branch, left, right):\n    a = normalize_tuple(branch, left)\n    b = normalize_tuple(branch, right)\n    if a > b:\n        return 1\n    if a < b:\n        return -1\n    return 0\n\ndef prefers(branch, chosen, rejected):\n    return compare(branch, chosen, rejected) > 0\n\ndef frontier(branch, action_to_tuple):\n    if not isinstance(action_to_tuple, dict) or not action_to_tuple:\n        raise ValueError("empty_action_to_tuple")\n    keys = {\n        action: normalize_tuple(branch, value)\n        for action, value in action_to_tuple.items()\n    }\n    maximum = max(keys.values())\n    members = {\n        action for action, value in keys.items()\n        if value == maximum\n    }\n    if not members:\n        raise ValueError("empty_policy_frontier")\n    return maximum, members\n\ndef deterministic_frontier_member(members):\n    members = set(members)\n    if not members:\n        raise ValueError("empty_policy_frontier")\n    return min(\n        members,\n        key=lambda action: hashlib.sha256(\n            str(action).encode("utf-8")\n        ).hexdigest(),\n    )\n\ndef adapt(branch, proposed_action, action_to_tuple):\n    maximum, members = frontier(branch, action_to_tuple)\n    if proposed_action in members:\n        executed = proposed_action\n        overridden = False\n        reason = "proposal_on_policy_frontier"\n    else:\n        executed = deterministic_frontier_member(members)\n        overridden = True\n        reason = "proposal_off_policy_frontier"\n    return {\n        "proposed_action": proposed_action,\n        "executed_action": executed,\n        "overridden": overridden,\n        "override_reason": reason,\n        "maximum_policy_tuple": list(maximum),\n        "frontier_members": sorted(members),\n        "world_mutated_before_adapter_validation": False,\n    }\n'


def sample_state() -> dict:
    return {
        "economy": {"cash": 800, "ore": 200, "harvester_count": 2},
        "military": {"army_value": 900},
        "explored_percent": 40.0,
        "own_buildings": 5,
        "power_balance": 100,
    }


def with_sha(value: dict) -> dict:
    out = dict(value)
    out["sha256"] = hashlib.sha256(canonical_json_bytes(out)).hexdigest()
    return out


def evidence_for(projection: dict, rows: list[dict]) -> dict:
    return with_sha({
        "schema": "void.generals.g2-runtime-frontier-evidence.v1",
        "state_projection_sha256": projection["sha256"],
        "projection_spec_sha256": projection["projection_spec_sha256"],
        "tool_schema_is_concrete_candidate_action": False,
        "candidates": rows,
    })


def row(projection: dict, action: dict, immediate: dict, delayed=None, valid=True):
    if delayed is None:
        delayed = {name: 0 for name in CAPABILITIES}
    aid = action_identity_sha256(action)
    return {
        "action": action,
        "host_prevalidation": {
            "state_projection_sha256": projection["sha256"],
            "action_identity_sha256": aid,
            "valid": valid,
            "world_mutated_before_validation": False,
            "execution_authority": False,
        },
        "effect_evidence": {
            "supported": True,
            "support": 3,
            "immediate_mean_delta": immediate,
            "delayed_next_round_mean_delta": delayed,
        },
    }


class FakeEnv:
    def __init__(self, state):
        self.state = state
        self.calls = []

    async def call_tool(self, name, **kwargs):
        self.calls.append((name, kwargs))
        if name == "get_game_state":
            return dict(self.state)
        raise AssertionError("unexpected tool execution in source test:" + name)


class TestG2RuntimeFrontierV1(unittest.IsolatedAsyncioTestCase):
    def test_closed_tool_classification(self):
        self.assertEqual(classify_tool("get_game_state"), OBSERVATION_CONTROL)
        self.assertEqual(classify_tool("attack_move"), MUTATION_CAPABLE)
        self.assertEqual(
            validate_discovered_tool_surface(
                [SimpleNamespace(name="get_game_state"), SimpleNamespace(name="attack_move")]
            ),
            ("get_game_state", "attack_move"),
        )
        with self.assertRaises(ToolClassificationHold):
            validate_discovered_tool_surface(
                [SimpleNamespace(name="get_game_state"), SimpleNamespace(name="future_unknown")]
            )

    def test_projection_is_deterministic_bounded_and_visible_only(self):
        a = project_live_game_state(sample_state())
        b = project_live_game_state(sample_state())
        self.assertEqual(a, b)
        self.assertEqual(a["projection_spec_sha256"], PROJECTION_SPEC_SHA256)
        self.assertEqual(tuple(a["capabilities"]), CAPABILITIES)
        self.assertFalse(a["hidden_or_unobserved_opponent_state_used"])
        self.assertFalse(a["model_inference_used"])
        self.assertTrue(all(0 <= value <= 1000 for value in a["capabilities"].values()))

    def test_concrete_action_identity_binds_arguments(self):
        a = {"tool": "attack_move", "arguments": {"unit_ids": "1,2", "target_x": 10, "target_y": 20}}
        b = {"tool": "attack_move", "arguments": {"unit_ids": "1,2", "target_x": 11, "target_y": 20}}
        self.assertNotEqual(action_identity_sha256(a), action_identity_sha256(b))
        self.assertNotEqual(canonical_action_key(a), canonical_action_key(b))

    def test_host_invalid_candidate_is_excluded_and_tuple_order_is_frozen(self):
        projection = project_live_game_state(sample_state())
        zero = {name: 0 for name in CAPABILITIES}
        good = {"tool": "attack_move", "arguments": {"unit_ids": "1", "target_x": 20, "target_y": 20}}
        weak = {"tool": "move_units", "arguments": {"unit_ids": "1", "target_x": 5, "target_y": 5}}
        invalid = {"tool": "attack_target", "arguments": {"unit_ids": "1", "target_actor_id": 999}}
        # delivery is the deficient capability in this fixture.
        good_delta = dict(zero, delivery=3, sensing=1)
        weak_delta = dict(zero, delivery=1)
        ev = evidence_for(
            projection,
            [
                row(projection, good, good_delta),
                row(projection, weak, weak_delta),
                row(projection, invalid, dict(zero, delivery=100), valid=False),
            ],
        )
        frontier = build_candidate_frontier(projection, weak, ev)
        self.assertEqual(frontier["branch"], "restorative_available")
        self.assertNotIn(canonical_action_key(invalid), frontier["action_to_tuple"])
        self.assertTrue(frontier["all_candidates_host_prevalidated"])
        for values in frontier["action_to_tuple"].values():
            self.assertEqual(len(values), 4)
            self.assertEqual(values[0], 1)

    def test_exact_accepted_comparator_and_off_frontier_substitution(self):
        self.assertEqual(
            hashlib.sha256(ACCEPTED_COMPARATOR_SOURCE.encode()).hexdigest(),
            EXPECTED_COMPARATOR_SHA256,
        )
        projection = project_live_game_state(sample_state())
        zero = {name: 0 for name in CAPABILITIES}
        proposed = {"tool": "move_units", "arguments": {"unit_ids": "1", "target_x": 5, "target_y": 5}}
        better = {"tool": "attack_move", "arguments": {"unit_ids": "1", "target_x": 20, "target_y": 20}}
        ev = evidence_for(
            projection,
            [
                row(projection, proposed, dict(zero, delivery=1)),
                row(projection, better, dict(zero, delivery=3)),
            ],
        )
        with tempfile.TemporaryDirectory() as td:
            comp = Path(td) / "compiled.py"
            comp.write_text(ACCEPTED_COMPARATOR_SOURCE, encoding="utf-8")
            decision = apply_compiled_comparator_gate(
                projection=projection,
                proposed_action=proposed,
                evidence=ev,
                comparator_path=comp,
            )
            self.assertTrue(decision["overridden"])
            self.assertEqual(decision["executed_action"], better)
            self.assertFalse(decision["world_mutated_before_adapter_validation"])

    def test_comparator_hash_drift_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            comp = Path(td) / "compiled.py"
            comp.write_text(ACCEPTED_COMPARATOR_SOURCE + "# drift\n", encoding="utf-8")
            with self.assertRaises(G2RuntimeFrontierHold):
                load_accepted_comparator(comp)

    def test_on_frontier_proposal_passes_canonical_equivalent_unchanged(self):
        projection = project_live_game_state(sample_state())
        zero = {name: 0 for name in CAPABILITIES}
        proposed = {
            "tool": "attack_move",
            "arguments": {"target_y": 20, "unit_ids": "1", "target_x": 20},
        }
        ev = evidence_for(
            projection,
            [row(projection, proposed, dict(zero, delivery=3))],
        )
        with tempfile.TemporaryDirectory() as td:
            comp = Path(td) / "compiled.py"
            comp.write_text(ACCEPTED_COMPARATOR_SOURCE, encoding="utf-8")
            decision = apply_compiled_comparator_gate(
                projection=projection,
                proposed_action=proposed,
                evidence=ev,
                comparator_path=comp,
            )
        self.assertFalse(decision["overridden"])
        self.assertEqual(
            canonical_action_key(decision["executed_action"]),
            canonical_action_key(proposed),
        )

    def test_candidate_frontier_is_deterministic_for_same_state_and_evidence(self):
        projection = project_live_game_state(sample_state())
        zero = {name: 0 for name in CAPABILITIES}
        a = {"tool": "move_units", "arguments": {"unit_ids": "1", "target_x": 5, "target_y": 5}}
        b = {"tool": "attack_move", "arguments": {"unit_ids": "1", "target_x": 20, "target_y": 20}}
        ev = evidence_for(
            projection,
            [
                row(projection, a, dict(zero, delivery=1)),
                row(projection, b, dict(zero, delivery=3)),
            ],
        )
        self.assertEqual(
            build_candidate_frontier(projection, a, ev),
            build_candidate_frontier(projection, a, ev),
        )

    async def test_off_mode_is_behavior_transparent(self):
        controller = RuntimeFrontierController(
            mode="off",
            discovered_tools=[SimpleNamespace(name="future_unknown")],
        )
        env = FakeEnv(sample_state())
        arguments = {"non_json_value": object()}
        prepared = await controller.prepare_call(env, "future_unknown", arguments)
        self.assertEqual(env.calls, [])
        self.assertEqual(prepared.tool_name, "future_unknown")
        self.assertIs(prepared.arguments, arguments)
        self.assertIsNone(prepared.record)

    async def test_shadow_good_gate_records_would_execute_but_passes_proposal(self):
        tools = [
            SimpleNamespace(name="get_game_state"),
            SimpleNamespace(name="move_units"),
            SimpleNamespace(name="attack_move"),
        ]
        projection = project_live_game_state(sample_state())
        zero = {name: 0 for name in CAPABILITIES}
        proposed = {"tool": "move_units", "arguments": {"unit_ids": "1", "target_x": 5, "target_y": 5}}
        better = {"tool": "attack_move", "arguments": {"unit_ids": "1", "target_x": 20, "target_y": 20}}
        ev = evidence_for(
            projection,
            [
                row(projection, proposed, dict(zero, delivery=1)),
                row(projection, better, dict(zero, delivery=3)),
            ],
        )
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            comp = root / "compiled.py"
            evidence_path = root / "evidence.json"
            comp.write_text(ACCEPTED_COMPARATOR_SOURCE, encoding="utf-8")
            evidence_path.write_text(json.dumps(ev), encoding="utf-8")
            controller = RuntimeFrontierController(
                mode="shadow",
                discovered_tools=tools,
                comparator_path=comp,
                evidence_path=evidence_path,
            )
            env = FakeEnv(sample_state())
            prepared = await controller.prepare_call(
                env, proposed["tool"], proposed["arguments"]
            )
        self.assertEqual(env.calls, [("get_game_state", {})])
        self.assertEqual(prepared.tool_name, proposed["tool"])
        self.assertEqual(prepared.arguments, proposed["arguments"])
        self.assertEqual(prepared.record["would_execute_action"], better)
        self.assertEqual(prepared.record["actual_action"], proposed)
        self.assertTrue(prepared.record["shadow_does_not_replace_or_block"])

    async def test_shadow_refreshes_before_each_mutating_call_and_never_replaces_on_hold(self):
        tools = [
            SimpleNamespace(name="get_game_state"),
            SimpleNamespace(name="attack_move"),
        ]
        controller = RuntimeFrontierController(mode="shadow", discovered_tools=tools)
        env = FakeEnv(sample_state())
        first = await controller.prepare_call(
            env,
            "attack_move",
            {"unit_ids": "1", "target_x": 10, "target_y": 10},
        )
        second = await controller.prepare_call(
            env,
            "attack_move",
            {"unit_ids": "1", "target_x": 11, "target_y": 10},
        )
        self.assertEqual([name for name, _ in env.calls], ["get_game_state", "get_game_state"])
        self.assertEqual(first.tool_name, "attack_move")
        self.assertEqual(first.arguments["target_x"], 10)
        self.assertEqual(second.arguments["target_x"], 11)
        self.assertTrue(first.record["shadow_does_not_replace_or_block"])
        self.assertIn("comparator_path_not_configured", first.record["gate_hold"])

    async def test_enforce_failure_occurs_before_world_mutation(self):
        tools = [
            SimpleNamespace(name="get_game_state"),
            SimpleNamespace(name="attack_move"),
        ]
        controller = RuntimeFrontierController(mode="enforce", discovered_tools=tools)
        env = FakeEnv(sample_state())
        with self.assertRaises(G2RuntimeFrontierHold):
            await controller.prepare_call(
                env,
                "attack_move",
                {"unit_ids": "1", "target_x": 10, "target_y": 10},
            )
        self.assertEqual(env.calls, [("get_game_state", {})])

    async def test_observation_control_passes_without_refresh(self):
        tools = [SimpleNamespace(name="get_game_state")]
        controller = RuntimeFrontierController(mode="shadow", discovered_tools=tools)
        env = FakeEnv(sample_state())
        prepared = await controller.prepare_call(env, "get_game_state", {})
        self.assertEqual(env.calls, [])
        self.assertEqual(prepared.tool_name, "get_game_state")
        self.assertTrue(prepared.record["observation_or_control_passthrough"])


if __name__ == "__main__":
    unittest.main()
