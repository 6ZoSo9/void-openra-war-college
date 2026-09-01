#!/usr/bin/env python3
"""Fail-closed verifier for War College controller evidence isolation.

This is a source-only evidence contract. Runtime truth remains pending until a
designated host emits a conforming record from the preserved generation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


MARKER = "VOID_WAR_COLLEGE_CONTROLLER_EVIDENCE_ISOLATION_V1"
SCHEMA_VERSION = 2
GENERATION = "ad1926569b12466c"
WAR_COLLEGE_FROZEN_COMMIT = "973802ef0a614e5afa782ff20e231e18966ae3e5"
ENGINE_FROZEN_COMMIT = "1607a7a6501d42a47638393ecef8b22831064932"
RUNTIME_EVIDENCE = "PENDING_DESIGNATED_HOST"

TOP_LEVEL_KEYS = {
    "marker", "schema_version", "generation", "war_college_frozen_commit",
    "engine_frozen_commit", "world_tick", "controllers",
    "joint_evidence_sha256",
}
CONTROLLER_KEYS = {
    "player_id", "controller_id", "observation_subject_player_id",
    "visibility_owner_player_id", "action_actor_player_id",
    "observation_payload", "observation_sha256",
    "observation_binding_sha256", "action_request_id", "action_payload",
    "action_sha256", "action_binding_sha256",
}
ACTION_PAYLOAD_KEYS = {
    "request_id", "player_id", "controller_id", "world_tick",
    "decision_observation_binding_sha256", "commands",
}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_hex(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def observation_binding(
    *,
    player_id: str,
    controller_id: str,
    world_tick: int,
    observation_sha256: str,
) -> str:
    return sha256_hex(
        {
            "controller_id": controller_id,
            "generation": GENERATION,
            "observation_sha256": observation_sha256,
            "player_id": player_id,
            "world_tick": world_tick,
        }
    )


def action_binding(
    *,
    player_id: str,
    controller_id: str,
    world_tick: int,
    action_request_id: str,
    action_sha256: str,
    decision_observation_binding_sha256: str,
) -> str:
    return sha256_hex(
        {
            "action_request_id": action_request_id,
            "action_sha256": action_sha256,
            "controller_id": controller_id,
            "decision_observation_binding_sha256": decision_observation_binding_sha256,
            "generation": GENERATION,
            "player_id": player_id,
            "world_tick": world_tick,
        }
    )


def joint_evidence_binding(
    *,
    world_tick: int,
    bindings: list[dict[str, str]],
) -> str:
    return sha256_hex(
        {
            "bindings": sorted(bindings, key=lambda item: item["player_id"]),
            "engine_frozen_commit": ENGINE_FROZEN_COMMIT,
            "generation": GENERATION,
            "war_college_frozen_commit": WAR_COLLEGE_FROZEN_COMMIT,
            "world_tick": world_tick,
        }
    )


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value) and value == value.strip()


def verify_evidence(evidence: Any) -> dict[str, Any]:
    holds: set[str] = set()
    checked_players: list[str] = []

    if not isinstance(evidence, dict):
        holds.add("HOLD_EVIDENCE_NOT_OBJECT")
        evidence = {}

    if set(evidence) != TOP_LEVEL_KEYS:
        holds.add("HOLD_TOP_LEVEL_SCHEMA_DRIFT")
    if evidence.get("marker") != MARKER:
        holds.add("HOLD_MARKER_MISMATCH")
    if evidence.get("schema_version") != SCHEMA_VERSION:
        holds.add("HOLD_SCHEMA_VERSION_MISMATCH")
    if evidence.get("generation") != GENERATION:
        holds.add("HOLD_GENERATION_MISMATCH")
    if evidence.get("war_college_frozen_commit") != WAR_COLLEGE_FROZEN_COMMIT:
        holds.add("HOLD_WAR_COLLEGE_BASE_MISMATCH")
    if evidence.get("engine_frozen_commit") != ENGINE_FROZEN_COMMIT:
        holds.add("HOLD_ENGINE_BASE_MISMATCH")

    world_tick = evidence.get("world_tick")
    if isinstance(world_tick, bool) or not isinstance(world_tick, int) or world_tick < 0:
        holds.add("HOLD_WORLD_TICK_INVALID")
        world_tick_valid = False
    else:
        world_tick_valid = True

    controllers = evidence.get("controllers")
    if not isinstance(controllers, list) or len(controllers) != 2:
        holds.add("HOLD_CONTROLLER_CARDINALITY")
        controllers = []

    player_ids: list[str] = []
    controller_ids: list[str] = []
    action_request_ids: list[str] = []
    bindings: list[dict[str, str]] = []

    for record in controllers:
        if not isinstance(record, dict):
            holds.add("HOLD_CONTROLLER_RECORD_NOT_OBJECT")
            continue
        if set(record) != CONTROLLER_KEYS:
            holds.add("HOLD_CONTROLLER_SCHEMA_DRIFT")

        player_id = record.get("player_id")
        controller_id = record.get("controller_id")
        if not _nonempty_string(player_id):
            holds.add("HOLD_PLAYER_ID_INVALID")
        else:
            player_ids.append(player_id)
            checked_players.append(player_id)
        if not _nonempty_string(controller_id):
            holds.add("HOLD_CONTROLLER_ID_INVALID")
        else:
            controller_ids.append(controller_id)

        if _nonempty_string(player_id):
            for field, hold in (
                ("observation_subject_player_id", "HOLD_CROSS_PLAYER_OBSERVATION"),
                ("visibility_owner_player_id", "HOLD_CROSS_PLAYER_VISIBILITY"),
                ("action_actor_player_id", "HOLD_CROSS_PLAYER_ACTION"),
            ):
                if record.get(field) != player_id:
                    holds.add(hold)

        observation_payload = record.get("observation_payload")
        if not isinstance(observation_payload, dict):
            holds.add("HOLD_OBSERVATION_PAYLOAD_NOT_OBJECT")
            observation_payload_valid = False
        else:
            observation_payload_valid = True
            if observation_payload.get("player_id") != player_id:
                holds.add("HOLD_PAYLOAD_PLAYER_BINDING")
            if observation_payload.get("world_tick") != world_tick:
                holds.add("HOLD_PAYLOAD_TICK_BINDING")

        claimed_observation_sha = record.get("observation_sha256")
        if not _nonempty_string(claimed_observation_sha):
            holds.add("HOLD_OBSERVATION_DIGEST_INVALID")
        elif observation_payload_valid and sha256_hex(observation_payload) != claimed_observation_sha:
            holds.add("HOLD_OBSERVATION_DIGEST_MISMATCH")

        claimed_observation_binding = record.get("observation_binding_sha256")
        observation_binding_inputs_valid = (
            _nonempty_string(player_id)
            and _nonempty_string(controller_id)
            and world_tick_valid
            and _nonempty_string(claimed_observation_sha)
        )
        if not _nonempty_string(claimed_observation_binding):
            holds.add("HOLD_OBSERVATION_BINDING_INVALID")
        elif observation_binding_inputs_valid:
            expected_observation_binding = observation_binding(
                player_id=player_id,
                controller_id=controller_id,
                world_tick=world_tick,
                observation_sha256=claimed_observation_sha,
            )
            if claimed_observation_binding != expected_observation_binding:
                holds.add("HOLD_OBSERVATION_BINDING_MISMATCH")

        action_request_id = record.get("action_request_id")
        if not _nonempty_string(action_request_id):
            holds.add("HOLD_ACTION_REQUEST_ID_INVALID")
        else:
            action_request_ids.append(action_request_id)

        action_payload = record.get("action_payload")
        if not isinstance(action_payload, dict):
            holds.add("HOLD_ACTION_PAYLOAD_NOT_OBJECT")
            action_payload_valid = False
            decision_observation_binding = None
        else:
            action_payload_valid = True
            if set(action_payload) != ACTION_PAYLOAD_KEYS:
                holds.add("HOLD_ACTION_PAYLOAD_SCHEMA_DRIFT")
            if action_payload.get("request_id") != action_request_id:
                holds.add("HOLD_ACTION_PAYLOAD_REQUEST_BINDING")
            if action_payload.get("player_id") != player_id:
                holds.add("HOLD_ACTION_PAYLOAD_PLAYER_BINDING")
            if action_payload.get("controller_id") != controller_id:
                holds.add("HOLD_ACTION_PAYLOAD_CONTROLLER_BINDING")
            if action_payload.get("world_tick") != world_tick:
                holds.add("HOLD_ACTION_PAYLOAD_TICK_BINDING")
            decision_observation_binding = action_payload.get(
                "decision_observation_binding_sha256"
            )
            if decision_observation_binding != claimed_observation_binding:
                holds.add("HOLD_ACTION_DECISION_OBSERVATION_BINDING")
            if not isinstance(action_payload.get("commands"), list):
                holds.add("HOLD_ACTION_COMMANDS_NOT_LIST")

        claimed_action_sha = record.get("action_sha256")
        if not _nonempty_string(claimed_action_sha):
            holds.add("HOLD_ACTION_DIGEST_INVALID")
        elif action_payload_valid and sha256_hex(action_payload) != claimed_action_sha:
            holds.add("HOLD_ACTION_DIGEST_MISMATCH")

        claimed_action_binding = record.get("action_binding_sha256")
        action_binding_inputs_valid = (
            _nonempty_string(player_id)
            and _nonempty_string(controller_id)
            and world_tick_valid
            and _nonempty_string(action_request_id)
            and _nonempty_string(claimed_action_sha)
            and _nonempty_string(decision_observation_binding)
        )
        if not _nonempty_string(claimed_action_binding):
            holds.add("HOLD_ACTION_BINDING_INVALID")
        elif action_binding_inputs_valid:
            expected_action_binding = action_binding(
                player_id=player_id,
                controller_id=controller_id,
                world_tick=world_tick,
                action_request_id=action_request_id,
                action_sha256=claimed_action_sha,
                decision_observation_binding_sha256=decision_observation_binding,
            )
            if claimed_action_binding != expected_action_binding:
                holds.add("HOLD_ACTION_BINDING_MISMATCH")

        if (
            observation_binding_inputs_valid
            and action_binding_inputs_valid
            and _nonempty_string(claimed_observation_binding)
            and _nonempty_string(claimed_action_binding)
        ):
            bindings.append(
                {
                    "action_binding_sha256": claimed_action_binding,
                    "controller_id": controller_id,
                    "observation_binding_sha256": claimed_observation_binding,
                    "player_id": player_id,
                }
            )

    if len(player_ids) != len(set(player_ids)):
        holds.add("HOLD_DUPLICATE_PLAYER_ID")
    if len(controller_ids) != len(set(controller_ids)):
        holds.add("HOLD_DUPLICATE_CONTROLLER_ID")
    if len(action_request_ids) != len(set(action_request_ids)):
        holds.add("HOLD_DUPLICATE_ACTION_REQUEST_ID")

    claimed_joint = evidence.get("joint_evidence_sha256")
    if not _nonempty_string(claimed_joint):
        holds.add("HOLD_JOINT_EVIDENCE_DIGEST_INVALID")
    elif world_tick_valid and len(bindings) == 2:
        expected_joint = joint_evidence_binding(world_tick=world_tick, bindings=bindings)
        if claimed_joint != expected_joint:
            holds.add("HOLD_JOINT_EVIDENCE_DIGEST_MISMATCH")

    ordered_holds = sorted(holds)
    return {
        "checked_players": sorted(set(checked_players)),
        "contract": "GREEN" if not ordered_holds else "HOLD",
        "engine_frozen_commit": ENGINE_FROZEN_COMMIT,
        "generation": GENERATION,
        "holds": ordered_holds,
        "marker": MARKER,
        "runtime_evidence": RUNTIME_EVIDENCE,
        "schema_version": SCHEMA_VERSION,
        "war_college_frozen_commit": WAR_COLLEGE_FROZEN_COMMIT,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args(argv)
    try:
        evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
        report = verify_evidence(evidence)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        report = {
            "checked_players": [],
            "contract": "HOLD",
            "engine_frozen_commit": ENGINE_FROZEN_COMMIT,
            "generation": GENERATION,
            "holds": [f"HOLD_EVIDENCE_READ_FAILURE:{type(error).__name__}"],
            "marker": MARKER,
            "runtime_evidence": RUNTIME_EVIDENCE,
            "schema_version": SCHEMA_VERSION,
            "war_college_frozen_commit": WAR_COLLEGE_FROZEN_COMMIT,
        }
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["contract"] == "GREEN" else 1


if __name__ == "__main__":
    sys.exit(main())
