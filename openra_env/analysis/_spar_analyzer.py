"""Bounded JointAdvance trajectory analysis."""

from __future__ import annotations

import hashlib
from collections import Counter
from pathlib import Path
from typing import Any

from ._spar_contract import (
    HOSTILE,
    MARKER,
    MAX_SUMMARY_BYTES,
    MAX_TRAJECTORY_BYTES,
    PASSIVE,
    SHA256,
    SIDES,
    ContractError,
    _bool,
    _header,
    _int,
    _json_object,
    _jsonl,
    _obj,
    _pairs,
    _read,
    _str,
)
from ._spar_metrics import (
    _action,
    _delta,
    _perspectives,
    _production,
    _ratio,
    _side_metrics,
    _state,
    _summary,
    combat_count,
    contact_episodes,
    military,
    visible_count,
)


def _bound_row_identity(
    row: dict[str, Any],
    header: dict[str, Any],
    label: str,
) -> None:
    for key in ("run_id", "curriculum_id"):
        if row.get(key) != header[key]:
            raise ContractError(f"{label} {key} does not match run_header")
    for key in ("candidate_only", "training_candidate", "controller_authored"):
        _bool(row.get(key), f"{label}.{key}", True)


def _first_event(
    current: dict[str, Any] | None,
    *,
    round_number: int,
    tick: int,
    **details: Any,
) -> dict[str, Any] | None:
    if current is not None:
        return current
    return {"round": round_number, "tick": tick, **details}


def _side_report(
    data: dict[str, Any],
    *,
    rounds: int,
    final_state: dict[str, Any],
) -> dict[str, Any]:
    final_military = military(final_state)
    return {
        "tools": dict(sorted(data["tools"].items())),
        "no_command_rounds": data["no_command"],
        "no_command_fraction": len(data["no_command"]) / rounds,
        "passive_rounds": data["passive"],
        "passive_fraction": len(data["passive"]) / rounds,
        "hostile_rounds": data["hostile"],
        "hostile_fraction": len(data["hostile"]) / rounds,
        "contact_rounds": data["contact"],
        "contact_fraction": len(data["contact"]) / rounds,
        "contact_episodes": contact_episodes(data["contact"]),
        "command_rounds": data["orders"],
        "command_fraction": len(data["orders"]) / rounds,
        "retried_rounds": data["retried"],
        "first_enemy_visible": data["first_visible"],
        "first_hostile_order": data["first_hostile"],
        "first_damage_inflicted": data["first_inflicted"],
        "first_damage_received": data["first_received"],
        "first_combat_growth": data["first_growth"],
        "first_combat_capable_production": data["first_production"],
        "final_visible_enemy_count": visible_count(final_state),
        "final_combat_capable_units": combat_count(final_state),
        "final_military": final_military,
        "net_kill_cost": final_military["kills_cost"] - final_military["deaths_cost"],
        "trade_ratio": _ratio(final_military),
    }


def analyze_trajectory(
    trajectory_path: Path,
    *,
    summary_path: Path | None = None,
    expected_trajectory_sha256: str | None = None,
    expected_summary_sha256: str | None = None,
) -> dict[str, Any]:
    """Validate a bound trajectory generation and derive utility metrics."""
    for digest, label in (
        (expected_trajectory_sha256, "trajectory SHA-256"),
        (expected_summary_sha256, "summary SHA-256"),
    ):
        if digest is not None and SHA256.fullmatch(digest) is None:
            raise ContractError(f"{label} must be lowercase SHA-256")
    if expected_summary_sha256 and summary_path is None:
        raise ContractError("summary SHA-256 requires --summary")

    trajectory_raw = _read(
        trajectory_path,
        "trajectory",
        MAX_TRAJECTORY_BYTES,
    )
    trajectory_sha = hashlib.sha256(trajectory_raw).hexdigest()
    if (
        expected_trajectory_sha256
        and trajectory_sha != expected_trajectory_sha256
    ):
        raise ContractError("trajectory SHA-256 mismatch")

    rows = _jsonl(trajectory_raw)
    if not rows:
        raise ContractError("trajectory is empty")
    header = _header(rows[0])
    pairs = _pairs(rows[1:])
    if len(pairs) > header["round_limit"]:
        raise ContractError("trajectory exceeds run_header round_limit")

    summary: dict[str, Any] | None = None
    summary_sha: str | None = None
    if summary_path is not None:
        summary_raw = _read(summary_path, "summary", MAX_SUMMARY_BYTES)
        summary_sha = hashlib.sha256(summary_raw).hexdigest()
        if expected_summary_sha256 and summary_sha != expected_summary_sha256:
            raise ContractError("summary SHA-256 mismatch")
        summary = _json_object(summary_raw, "summary")

    side_data = {side: _side_metrics() for side in SIDES}
    latest_production_order: dict[str, dict[str, Any] | None] = {
        side: None for side in SIDES
    }
    previous_after: dict[str, dict[str, Any]] | None = None
    expected_start_tick = header["warm_start_handoff_tick"]
    contact_distribution: Counter[str] = Counter()
    first_damage_tick: int | None = None
    final: dict[str, dict[str, Any]] = {}
    phase = ""
    winner = ""

    for index, (decision, result) in enumerate(pairs, 1):
        _bound_row_identity(decision, header, f"round {index} decision")
        _bound_row_identity(result, header, f"round {index} result")

        start_tick = _int(decision.get("start_tick"), "decision.start_tick")
        result_start = _int(result.get("start_tick"), "result.start_tick")
        end_tick = _int(result.get("end_tick"), "result.end_tick")
        if start_tick != expected_start_tick:
            raise ContractError(
                f"round {index} does not continue the prior world clock"
            )
        if result_start != start_tick:
            raise ContractError("joint_result start_tick does not match decision")
        if end_tick <= start_tick:
            raise ContractError("joint_result did not advance the world clock")
        if end_tick - start_tick > header["ticks_per_round"]:
            raise ContractError("joint_result advanced beyond ticks_per_round")

        round_before: dict[str, dict[str, Any]] = {}
        round_after: dict[str, dict[str, Any]] = {}
        round_delta: dict[str, dict[str, int]] = {}
        after_visible: dict[str, int] = {}

        for side, (before_key, after_key) in SIDES.items():
            before = _obj(decision.get(before_key), f"round {index} {before_key}")
            after = _obj(result.get(after_key), f"round {index} {after_key}")
            _state(before, f"round {index} {before_key}", start_tick)
            _state(after, f"round {index} {after_key}", end_tick)
            if previous_after is not None and before != previous_after[side]:
                raise ContractError(
                    f"round {index} {side} state does not continue prior result"
                )

            before_military = military(before)
            after_military = military(after)
            change = _delta(before_military, after_military)
            round_before[side] = before
            round_after[side] = after
            round_delta[side] = change
            after_visible[side] = visible_count(after)

            tool, command_count, attempts_count = _action(decision, side, index)
            data = side_data[side]
            data["tools"][tool] += 1
            if command_count == 0:
                data["no_command"].append(index)
            else:
                data["orders"].append(index)
            if tool in PASSIVE:
                data["passive"].append(index)
            if tool in HOSTILE:
                data["hostile"].append(index)
                data["first_hostile"] = _first_event(
                    data["first_hostile"],
                    round_number=index,
                    tick=start_tick,
                    tool=tool,
                )
            if attempts_count > 1:
                data["retried"].append(index)
            if _production(tool) and command_count > 0:
                latest_production_order[side] = {
                    "round": index,
                    "tick": start_tick,
                    "tool": tool,
                }

            if after_visible[side] > 0:
                data["contact"].append(index)
                data["first_visible"] = _first_event(
                    data["first_visible"],
                    round_number=index,
                    tick=end_tick,
                    visible_enemy_count=after_visible[side],
                )

            inflicted = (
                change["units_killed"]
                or change["buildings_killed"]
                or change["kills_cost"]
            )
            received = (
                change["units_lost"]
                or change["buildings_lost"]
                or change["deaths_cost"]
            )
            if inflicted:
                data["first_inflicted"] = _first_event(
                    data["first_inflicted"],
                    round_number=index,
                    tick=end_tick,
                    units_killed_delta=change["units_killed"],
                    buildings_killed_delta=change["buildings_killed"],
                    kills_cost_delta=change["kills_cost"],
                )
            if received:
                data["first_received"] = _first_event(
                    data["first_received"],
                    round_number=index,
                    tick=end_tick,
                    units_lost_delta=change["units_lost"],
                    buildings_lost_delta=change["buildings_lost"],
                    deaths_cost_delta=change["deaths_cost"],
                )
            if inflicted or received:
                if first_damage_tick is None:
                    first_damage_tick = end_tick

            before_combat = combat_count(before)
            after_combat = combat_count(after)
            if after_combat > before_combat:
                data["first_growth"] = _first_event(
                    data["first_growth"],
                    round_number=index,
                    tick=end_tick,
                    before=before_combat,
                    after=after_combat,
                    delta=after_combat - before_combat,
                )
                order = latest_production_order[side]
                if data["first_production"] is None and order is not None:
                    data["first_production"] = {
                        "order": order,
                        "completion_round": index,
                        "completion_tick": end_tick,
                        "ticks_from_handoff": (
                            end_tick - header["warm_start_handoff_tick"]
                        ),
                        "attribution": (
                            "latest_prior_controller_production_order"
                        ),
                    }

        _perspectives(round_delta["apollyon"], round_delta["abaddon"])

        ap_contact = after_visible["apollyon"] > 0
        ab_contact = after_visible["abaddon"] > 0
        if ap_contact and ab_contact:
            pressure = "mutual"
        elif ap_contact:
            pressure = "apollyon_only"
        elif ab_contact:
            pressure = "abaddon_only"
        else:
            pressure = "none"
        contact_distribution[pressure] += 1

        phase = _str(result.get("phase"), "result.phase", empty=True)
        winner = _str(result.get("winner"), "result.winner", empty=True)
        if phase == "game_over" and index != len(pairs):
            raise ContractError("game_over result is not terminal")
        if winner and phase != "game_over":
            raise ContractError("winner is present before game_over")

        previous_after = round_after
        final = round_after
        expected_start_tick = end_tick

    final_tick = expected_start_tick
    if summary is not None:
        _summary(
            summary,
            header,
            trajectory_sha,
            len(pairs),
            final_tick,
            phase,
            winner,
            final,
        )

    if first_damage_tick is not None:
        classification = "TACTICAL_DAMAGE_PRESENT"
    elif side_data["apollyon"]["hostile"] or side_data["abaddon"]["hostile"]:
        classification = "HOSTILE_ORDERS_NO_DAMAGE"
    elif side_data["apollyon"]["contact"] or side_data["abaddon"]["contact"]:
        classification = "CONTACT_NO_DAMAGE"
    else:
        classification = "NO_CONTACT"

    distribution = {
        key: contact_distribution.get(key, 0)
        for key in ("none", "apollyon_only", "abaddon_only", "mutual")
    }

    return {
        "marker": MARKER,
        "version": 1,
        "provenance": {
            **header,
            "trajectory_sha256": trajectory_sha,
            "summary_sha256": summary_sha,
        },
        "integrity": {
            "trajectory_verified": True,
            "summary_verified": summary is not None,
            "rounds_completed": len(pairs),
            "final_tick": final_tick,
            "terminal_phase": phase or "playing",
            "winner": winner,
            "world_clock_contiguous": True,
            "perspective_accounting_consistent": True,
        },
        "training_utility": {
            "classification": classification,
            "first_damage_tick": first_damage_tick,
            "contact_distribution_rounds": distribution,
            "scenario_pressure_distribution": distribution,
        },
        "sides": {
            side: _side_report(
                side_data[side],
                rounds=len(pairs),
                final_state=final[side],
            )
            for side in SIDES
        },
        "authority": {
            "candidate_only": True,
            "review_required": True,
            "automatic_corpus_admission": False,
            "automatic_apollyon_weight_mutation": False,
            "automatic_abaddon_policy_promotion": False,
        },
    }
