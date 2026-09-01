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
SCHEMA_VERSION = 1
GENERATION = "ad1926569b12466c"
WAR_COLLEGE_FROZEN_COMMIT = "973802ef0a614e5afa782ff20e231e18966ae3e5"
ENGINE_FROZEN_COMMIT = "1607a7a6501d42a47638393ecef8b22831064932"
RUNTIME_EVIDENCE = "PENDING_DESIGNATED_HOST"

TOP_LEVEL_KEYS = {
    "marker",
    "schema_version",
    "generation",
    "war_college_frozen_commit",
    "engine_frozen_commit",
    "world_tick",
    "controllers",
    "joint_evidence_sha256",
}
CONTROLLER_KEYS = {
    "player_id",
    "controller_id",
    "observation_subject_player_id",
    "visibility_owner_player_id",
    "action_actor_player_id",
    "observation_payload",
    "observation_sha256",
    "observation_binding_sha256",
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

        payload = record.get("observation_payload")
        if not isinstance(payload, dict):
            holds.add("HOLD_OBSERVATION_PAYLOAD_NOT_OBJECT")
            payload_valid = False
        else:
            payload_valid = True
            if payload.get("player_id") != player_id:
                holds.add("HOLD_PAYLOAD_PLAYER_BINDING")
            if payload.get("world_tick") != world_tick:
                holds.add("HOLD_PAYLOAD_TICK_BINDING")

        claimed_observation_sha = record.get("observation_sha256")
        if not _nonempty_string(claimed_observation_sha):
            holds.add("HOLD_OBSERVATION_DIGEST_INVALID")
        elif payload_valid and sha256_hex(payload) != claimed_observation_sha:
            holds.add("HOLD_OBSERVATION_DIGEST_MISMATCH")

        claimed_binding = record.get("observation_binding_sha256")
        if not _nonempty_string(claimed_binding):
            holds.add("HOLD_OBSERVATION_BINDING_INVALID")
        elif (
            _nonempty_string(player_id)
            and _nonempty_string(controller_id)
            and world_tick_valid
            and _nonempty_string(claimed_observation_sha)
        ):
            expected_binding = observation_binding(
                player_id=player_id,
                controller_id=controller_id,
                world_tick=world_tick,
                observation_sha256=claimed_observation_sha,
            )
            if claimed_binding != expected_binding:
                holds.add("HOLD_OBSERVATION_BINDING_MISMATCH")
            bindings.append(
                {
                    "controller_id": controller_id,
                    "observation_binding_sha256": claimed_binding,
                    "player_id": player_id,
                }
            )

    if len(player_ids) != len(set(player_ids)):
        holds.add("HOLD_DUPLICATE_PLAYER_ID")
    if len(controller_ids) != len(set(controller_ids)):
        holds.add("HOLD_DUPLICATE_CONTROLLER_ID")

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
