#!/usr/bin/env python3
from __future__ import annotations

import unittest

from tests.test_verify_controller_evidence_isolation_v1 import (
    contract, finalize, make_evidence, refresh_action, verify,
)


def rehash_action(evidence: dict[str, object], index: int = 0) -> None:
    record = evidence["controllers"][index]
    refresh_action(record, evidence["world_tick"])
    finalize(evidence)


def base_command() -> dict[str, object]:
    return {
        "action": "no_op", "actor_id": 0, "target_actor_id": 0,
        "target_x": 0, "target_y": 0, "item_type": "", "queued": False,
    }


def valid_command(action: str) -> dict[str, object]:
    command = base_command()
    command["action"] = action
    if action in {"move", "attack_move", "patrol"}:
        command.update(actor_id=101, target_x=6, target_y=7, queued=True)
    elif action == "harvest":
        command.update(actor_id=101, target_x=6, target_y=7)
    elif action in {"stop", "deploy"}:
        command.update(actor_id=101)
    elif action == "unload":
        command.update(actor_id=102)
    elif action == "set_stance":
        command.update(actor_id=101, target_x=2)
    elif action == "attack":
        command.update(actor_id=101, target_actor_id=201, queued=True)
    elif action == "guard":
        command.update(actor_id=101, target_actor_id=1101, queued=True)
    elif action == "enter_transport":
        command.update(actor_id=101, target_actor_id=102)
    elif action in {"sell", "repair", "power_down", "set_primary"}:
        command.update(actor_id=1101)
    elif action == "set_rally_point":
        command.update(actor_id=1101, target_x=8, target_y=9)
    elif action in {"build", "train"}:
        command.update(item_type="e1")
    elif action == "place_building":
        command.update(item_type="powr", target_x=8, target_y=9)
    elif action == "cancel_production":
        command.update(item_type="powr")
    elif action in {"no_op", "surrender"}:
        pass
    else:
        raise AssertionError(action)
    return command


def set_player1_command(evidence: dict[str, object], command: dict[str, object]) -> None:
    record = evidence["controllers"][0]
    record["action_payload"]["commands"] = [command]
    rehash_action(evidence, 0)


class ControllerEvidenceCommandAuthorityTests(unittest.TestCase):
    def assert_hold(self, evidence: dict[str, object], code: str) -> None:
        report = verify(evidence)
        self.assertEqual(report["contract"], "HOLD")
        self.assertIn(code, report["holds"])

    def test_all_reviewed_controller_action_variants_have_valid_fixture(self) -> None:
        expected = {
            "no_op", "move", "attack_move", "attack", "stop", "harvest",
            "build", "train", "deploy", "sell", "repair", "place_building",
            "cancel_production", "set_rally_point", "guard", "set_stance",
            "enter_transport", "unload", "power_down", "set_primary", "surrender",
            "patrol",
        }
        self.assertEqual(contract.CONTROLLER_ACTIONS, expected)
        for action in sorted(expected):
            with self.subTest(action=action):
                evidence = make_evidence()
                set_player1_command(evidence, valid_command(action))
                report = verify(evidence)
                self.assertEqual(report["contract"], "GREEN", report["holds"])

    def test_fully_rehashed_cross_player_unit_actor_is_rejected(self) -> None:
        evidence = make_evidence()
        command = valid_command("move")
        command["actor_id"] = 201
        set_player1_command(evidence, command)
        self.assert_hold(evidence, "HOLD_ACTION_COMMAND_ACTOR_NOT_OWN_UNIT")

    def test_fully_rehashed_cross_player_building_actor_is_rejected(self) -> None:
        evidence = make_evidence()
        command = valid_command("sell")
        command["actor_id"] = 1201
        set_player1_command(evidence, command)
        self.assert_hold(evidence, "HOLD_ACTION_COMMAND_ACTOR_NOT_OWN_BUILDING")

    def test_attack_target_must_be_visible_enemy(self) -> None:
        evidence = make_evidence()
        command = valid_command("attack")
        command["target_actor_id"] = 102
        set_player1_command(evidence, command)
        self.assert_hold(evidence, "HOLD_ACTION_COMMAND_TARGET_NOT_VISIBLE_ENEMY")

    def test_guard_target_must_be_owned_actor(self) -> None:
        evidence = make_evidence()
        command = valid_command("guard")
        command["target_actor_id"] = 201
        set_player1_command(evidence, command)
        self.assert_hold(evidence, "HOLD_ACTION_COMMAND_TARGET_NOT_OWN_ACTOR")

    def test_transport_target_must_be_owned_unit(self) -> None:
        evidence = make_evidence()
        command = valid_command("enter_transport")
        command["target_actor_id"] = 201
        set_player1_command(evidence, command)
        self.assert_hold(evidence, "HOLD_ACTION_COMMAND_TARGET_NOT_OWN_UNIT")

    def test_train_item_must_be_available(self) -> None:
        evidence = make_evidence()
        command = valid_command("train")
        command["item_type"] = "notavailable"
        set_player1_command(evidence, command)
        self.assert_hold(evidence, "HOLD_ACTION_COMMAND_ITEM_NOT_AVAILABLE")

    def test_cancel_item_must_be_active_production(self) -> None:
        evidence = make_evidence()
        command = valid_command("cancel_production")
        command["item_type"] = "e1"
        set_player1_command(evidence, command)
        self.assert_hold(evidence, "HOLD_ACTION_COMMAND_ITEM_NOT_ACTIVE_PRODUCTION")

    def test_unknown_action_variant_fails_closed_after_rehash(self) -> None:
        evidence = make_evidence()
        command = base_command()
        command["action"] = "teleport"
        set_player1_command(evidence, command)
        self.assert_hold(evidence, "HOLD_ACTION_COMMAND_ACTION_UNSUPPORTED")

    def test_unknown_command_key_fails_closed_after_rehash(self) -> None:
        evidence = make_evidence()
        command = valid_command("move")
        command["unreviewed_authority"] = True
        set_player1_command(evidence, command)
        self.assert_hold(evidence, "HOLD_ACTION_COMMAND_SCHEMA_DRIFT")

    def test_unused_authority_field_must_stay_default(self) -> None:
        evidence = make_evidence()
        command = valid_command("stop")
        command["target_actor_id"] = 201
        set_player1_command(evidence, command)
        self.assert_hold(evidence, "HOLD_ACTION_COMMAND_UNUSED_FIELD_NONDEFAULT")

    def test_mixed_authority_command_list_fails_closed(self) -> None:
        evidence = make_evidence()
        good = valid_command("move")
        bad = valid_command("move")
        bad["actor_id"] = 201
        record = evidence["controllers"][0]
        record["action_payload"]["commands"] = [good, bad]
        rehash_action(evidence, 0)
        self.assert_hold(evidence, "HOLD_ACTION_COMMAND_ACTOR_NOT_OWN_UNIT")

    def test_observation_actor_classes_must_not_overlap(self) -> None:
        evidence = make_evidence()
        record = evidence["controllers"][0]
        record["observation_payload"]["visible_enemy_actor_ids"].append(101)
        record["observation_sha256"] = contract.sha256_hex(record["observation_payload"])
        record["observation_binding_sha256"] = contract.observation_binding(
            attempt_id=evidence["attempt_id"],
            controller_session_generation=evidence["controller_session_generation"],
            player_id=record["player_id"], controller_id=record["controller_id"],
            world_tick=evidence["world_tick"],
            observation_sha256=record["observation_sha256"],
        )
        record["action_payload"]["decision_observation_binding_sha256"] = record["observation_binding_sha256"]
        rehash_action(evidence, 0)
        self.assert_hold(evidence, "HOLD_OWN_AND_ENEMY_ACTOR_ID_OVERLAP")


if __name__ == "__main__":
    unittest.main()
