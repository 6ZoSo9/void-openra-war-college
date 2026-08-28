from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from ._spar_conditional_v2_2 import TRAJECTORY_KEY, validate_conditional_v22_evidence
from ._spar_contract import (
    MAX_TRAJECTORY_BYTES,
    SHA256,
    ContractError,
    _jsonl,
    _obj,
    _pairs,
    _read,
    _str,
)
from ._spar_metrics import _delta, military, visible_count

CONVERSION_SCHEMA = "void.apollyon.conditional-engagement-v2-2-conversion-utility.v1"


def _mode(decision: Mapping[str, Any], round_number: int) -> str:
    raw = _obj(decision.get(TRAJECTORY_KEY), f"round {round_number} V2.2 evidence")
    prepared = _obj(raw.get("prepared"), f"round {round_number} V2.2 prepared")
    policy = _obj(prepared.get("decision"), f"round {round_number} V2.2 decision")
    return _str(policy.get("mode"), f"round {round_number} V2.2 mode")


def _tool(decision: Mapping[str, Any], round_number: int) -> str:
    apollyon = _obj(decision.get("apollyon"), f"round {round_number} Apollyon decision")
    return _str(apollyon.get("tool"), f"round {round_number} Apollyon tool")


def _damage_inflicted(before: Mapping[str, Any], after: Mapping[str, Any]) -> bool:
    change = _delta(military(dict(before)), military(dict(after)))
    return bool(
        change["units_killed"]
        or change["buildings_killed"]
        or change["kills_cost"]
    )


def derive_conversion_productivity(
    pairs: Sequence[tuple[Mapping[str, Any], Mapping[str, Any]]],
) -> dict[str, Any]:
    conversion_rounds: list[int] = []
    conversion_immediate_contact: list[int] = []
    conversion_immediate_damage: list[int] = []
    conversion_tools: Counter[str] = Counter()
    post_conversion_contact: list[int] = []
    post_conversion_damage: list[int] = []
    post_conversion_tools: Counter[str] = Counter()
    first_conversion_round: int | None = None

    for round_number, (decision, result) in enumerate(pairs, 1):
        mode = _mode(decision, round_number)
        tool = _tool(decision, round_number)
        before = _obj(decision.get("apollyon_state"), f"round {round_number} Apollyon before")
        after = _obj(result.get("apollyon_after"), f"round {round_number} Apollyon after")
        contact = visible_count(after) > 0
        damage = _damage_inflicted(before, after)

        if mode == "FORCE_CONVERSION":
            conversion_rounds.append(round_number)
            conversion_tools[tool] += 1
            if first_conversion_round is None:
                first_conversion_round = round_number
            if contact:
                conversion_immediate_contact.append(round_number)
            if damage:
                conversion_immediate_damage.append(round_number)

        if first_conversion_round is not None and round_number >= first_conversion_round:
            post_conversion_tools[tool] += 1
            if contact:
                post_conversion_contact.append(round_number)
            if damage:
                post_conversion_damage.append(round_number)

    applicable = first_conversion_round is not None
    contact_after = bool(post_conversion_contact)
    damage_after = bool(post_conversion_damage)
    gate_pass = (not applicable) or (contact_after and damage_after)
    post_rounds = sum(post_conversion_tools.values())
    post_attack_moves = post_conversion_tools.get("attack_move", 0)

    return {
        "conversion_productivity_applicable": applicable,
        "post_conversion_productivity_pass": gate_pass,
        "first_conversion_round": first_conversion_round,
        "conversion_rounds": conversion_rounds,
        "conversion_round_count": len(conversion_rounds),
        "conversion_selected_tools": dict(sorted(conversion_tools.items())),
        "conversion_rounds_with_immediate_contact": conversion_immediate_contact,
        "conversion_rounds_with_immediate_damage": conversion_immediate_damage,
        "post_conversion_round_count": post_rounds,
        "post_conversion_contact_rounds": post_conversion_contact,
        "post_conversion_damage_rounds": post_conversion_damage,
        "first_contact_round_after_conversion": (
            post_conversion_contact[0] if post_conversion_contact else None
        ),
        "first_damage_round_after_conversion": (
            post_conversion_damage[0] if post_conversion_damage else None
        ),
        "post_conversion_selected_tools": dict(sorted(post_conversion_tools.items())),
        "post_conversion_attack_move_fraction": (
            post_attack_moves / post_rounds if post_rounds else 0.0
        ),
    }


def analyze_conversion_productivity(
    trajectory_path: Path,
    *,
    expected_trajectory_sha256: str,
) -> dict[str, Any]:
    if SHA256.fullmatch(expected_trajectory_sha256) is None:
        raise ContractError("expected trajectory SHA-256 malformed for V2.2 conversion analysis")

    verified = validate_conditional_v22_evidence(
        trajectory_path,
        expected_trajectory_sha256=expected_trajectory_sha256,
    )
    if verified.get("present") is not True:
        raise ContractError("trajectory is not reviewed V2.2 evidence")

    raw = _read(trajectory_path, "trajectory", MAX_TRAJECTORY_BYTES)
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected_trajectory_sha256:
        raise ContractError("trajectory changed between V2.2 validation and conversion analysis")
    rows = _jsonl(raw)
    pairs = _pairs(rows[1:])
    metrics = derive_conversion_productivity(pairs)

    return {
        "schema": CONVERSION_SCHEMA,
        "candidate_only": True,
        "trajectory_sha256": actual,
        "reviewed_identity_verified": True,
        "v2_2_candidate_sha256": verified["candidate_sha256"],
        "rounds_verified": verified["rounds_verified"],
        **metrics,
        "authority": {
            "candidate_only": True,
            "automatic_corpus_admission": False,
            "automatic_apollyon_weight_mutation": False,
            "automatic_abaddon_policy_promotion": False,
        },
    }


def stable_json(value: Mapping[str, Any]) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    try:
        with temporary.open("x", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if temporary.exists():
            temporary.unlink()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Prove whether V2.2 FORCE_CONVERSION is followed by productive contact/damage"
    )
    parser.add_argument("--trajectory", required=True)
    parser.add_argument("--trajectory-sha256", required=True)
    parser.add_argument("--output")
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        report = analyze_conversion_productivity(
            Path(args.trajectory),
            expected_trajectory_sha256=args.trajectory_sha256,
        )
        encoded = stable_json(report)
        if args.output:
            atomic_write(Path(args.output), encoded)
        else:
            sys.stdout.write(encoded)
        return 0
    except (ContractError, OSError) as error:
        print(f"V2.2 conversion utility contract error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
