"""Pure pair-06 V8 combat-action availability auditor.

The successful run's trajectory persists, for every joint_decision row:
- the exact pre-decision Apollyon compact state;
- the accepted action and all validation attempts;
- the exact typed tool contract, including offered_tool_names, legal_units,
  legal_buildings, and production-function mappings.

This source parses exact trajectory bytes and reports whether combat-recovery
and engagement actions were actually available at relevant decision points.
It performs no host I/O, replay, model inference, game execution, training,
promotion, deployment, VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Iterable, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_hypothesis_generation2
    as hypothesis,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-availability-audit-contract.v1"
)
REPORT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-action-availability-audit-report.v1"
)

HYPOTHESIS_MAIN_HEAD = "6eb6c9912be8877ed8b2c22c477101b9cccb3bac"
HYPOTHESIS_GIT_BLOB = "2d60d5c5e963746c7ce04d993c18e36472cff9ab"

WARM_START_RUNNER_FIXTURE_GIT_BLOB = (
    "132a5b2df3c3dbc82df7c0ebc6d457e5b77ffb51"
)
JOINT_HOST_FIXTURE_GIT_BLOB = (
    "6e751b855da1d9425c4fd2bd5a997ae1c742ae11"
)
LEGACY_WARM_START_RUNNER_SHA256 = (
    "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
)

TRAJECTORY_SHA256 = (
    "2275f2bdc5b0d7ac86cda2b0f1fb6e2fc1a582bfcb86e727399593d160074ee1"
)
RUN_ID = "warmstart-apollyon-vs-abaddon-20260925T070348Z-feinter-s208354846"
EXPECTED_ROUNDS = 36

ENGAGEMENT_TOOL_NAMES = frozenset({
    "attack_target",
    "move_units",
    "attack_move",
})
CONTROL_TOOL_NAMES = frozenset({
    "advance",
    "stop_units",
    "set_stance",
    "guard_target",
})

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_AVAILABILITY_PRECISION_OBSERVATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "read_only_pair06_v8_combat_action_availability_precision_observation"
)


class Pair06V8CombatActionAvailabilityAuditHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatActionAvailabilityAuditHold(message)


def _validated_hypothesis() -> dict[str, Any]:
    out = hypothesis.pair06_v8_combat_action_priority_hypothesis_contract()
    _require(
        out.get("hypothesis_id") == "pair06-v8-combat-action-priority-v1",
        "pair06 combat-priority hypothesis drift",
    )
    _require(
        out.get("availability_audit_required_before_policy_proposal") is True,
        "pair06 availability-audit requirement drift",
    )
    _require(
        out.get("tool_availability_currently_proven") is False
        and out.get("policy_ranking_cause_currently_proven") is False,
        "pair06 hypothesis prematurely proves availability/ranking",
    )
    _require(
        out.get("policy_change_authorized") is False
        and out.get("runtime_execution_authorized") is False
        and out.get("training_authorized") is False,
        "pair06 hypothesis unexpectedly grants authority",
    )
    _require(
        out.get("next_gate")
        == "PAIR06_V8_COMBAT_ACTION_AVAILABILITY_AUDIT_REQUIRED",
        "pair06 availability-audit frontier drift",
    )
    return deepcopy(out)


def _combat_count(state: Mapping[str, Any]) -> int:
    units = state.get("units_summary")
    _require(isinstance(units, list), "apollyon units_summary missing")
    count = 0
    for unit in units:
        _require(isinstance(unit, Mapping), "apollyon unit row invalid")
        if unit.get("can_attack") is True:
            count += 1
    return count


def _visible_enemy_count(state: Mapping[str, Any]) -> int:
    enemies = state.get("enemy_summary")
    buildings = state.get("enemy_buildings_summary")
    _require(isinstance(enemies, list), "apollyon enemy_summary missing")
    _require(
        isinstance(buildings, list),
        "apollyon enemy_buildings_summary missing",
    )
    return len(enemies) + len(buildings)


def _string_list(value: Any, label: str) -> list[str]:
    _require(isinstance(value, list), label + " must be list")
    _require(
        all(isinstance(item, str) and bool(item) for item in value),
        label + " contains invalid item",
    )
    _require(len(value) == len(set(value)), label + " contains duplicates")
    return list(value)


def _decision_rows_from_payload(payload: bytes) -> list[dict[str, Any]]:
    _require(type(payload) is bytes, "trajectory must be exact bytes")
    _require(
        hashlib.sha256(payload).hexdigest() == TRAJECTORY_SHA256,
        "trajectory SHA drift",
    )
    try:
        text = payload.decode("utf-8")
    except UnicodeError:
        raise Pair06V8CombatActionAvailabilityAuditHold(
            "trajectory UTF-8 invalid"
        ) from None

    rows = []
    for line_no, line in enumerate(text.splitlines(), 1):
        if not line:
            continue
        try:
            value = json.loads(line)
        except Exception as exc:
            raise Pair06V8CombatActionAvailabilityAuditHold(
                f"trajectory JSON invalid at line {line_no}: {exc}"
            ) from exc
        _require(isinstance(value, dict), "trajectory row must be object")
        if value.get("event") == "joint_decision":
            rows.append(value)

    _require(len(rows) == EXPECTED_ROUNDS, "joint_decision row count drift")
    _require(
        [row.get("round") for row in rows]
        == list(range(1, EXPECTED_ROUNDS + 1)),
        "joint_decision round sequence drift",
    )
    return rows


def _audit_rows(rows: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = [dict(row) for row in rows]
    _require(len(rows) > 0, "availability audit rows empty")

    round_reports = []
    for row in rows:
        round_no = row.get("round")
        _require(type(round_no) is int and round_no >= 1, "round invalid")
        _require(row.get("run_id") == RUN_ID, "run id drift")

        state = row.get("apollyon_state")
        apollyon = row.get("apollyon")
        _require(isinstance(state, Mapping), "apollyon_state missing")
        _require(isinstance(apollyon, Mapping), "apollyon decision missing")

        tool_contract = apollyon.get("tool_contract")
        _require(isinstance(tool_contract, Mapping), "tool contract missing")
        offered = _string_list(
            tool_contract.get("offered_tool_names"),
            "offered_tool_names",
        )
        legal_units = _string_list(
            tool_contract.get("legal_units"),
            "legal_units",
        )
        legal_buildings = _string_list(
            tool_contract.get("legal_buildings"),
            "legal_buildings",
        )

        accepted = apollyon.get("tool")
        _require(
            isinstance(accepted, str) and accepted in set(offered),
            "accepted tool not offered",
        )
        attempts = apollyon.get("attempts")
        _require(isinstance(attempts, list) and attempts, "attempt list missing")
        _require(
            all(
                isinstance(attempt, Mapping)
                and attempt.get("function_was_offered") is True
                for attempt in attempts
                if attempt.get("accepted") is True
            ),
            "accepted attempt was not offered",
        )

        combat_count = _combat_count(state)
        visible_enemy_count = _visible_enemy_count(state)
        recovery_tools = sorted(
            name for name in offered if name.startswith("train_unit_")
        )
        engagement_tools = sorted(
            set(offered) & set(ENGAGEMENT_TOOL_NAMES)
        )

        round_reports.append({
            "round": round_no,
            "accepted_tool": accepted,
            "attempt_count": len(attempts),
            "combat_count": combat_count,
            "visible_enemy_count": visible_enemy_count,
            "offered_tool_count": len(offered),
            "offered_tool_names": offered,
            "legal_units": legal_units,
            "legal_buildings": legal_buildings,
            "recovery_tools": recovery_tools,
            "engagement_tools": engagement_tools,
            "combat_recovery_relevant": combat_count == 0,
            "combat_recovery_available": bool(recovery_tools),
            "engagement_relevant": (
                combat_count > 0 and visible_enemy_count > 0
            ),
            "engagement_available": bool(engagement_tools),
            "attack_target_available": "attack_target" in set(offered),
            "move_units_available": "move_units" in set(offered),
            "attack_move_available": "attack_move" in set(offered),
            "advance_available": "advance" in set(offered),
        })

    recovery_rounds = [
        row for row in round_reports if row["combat_recovery_relevant"]
    ]
    engagement_rounds = [
        row for row in round_reports if row["engagement_relevant"]
    ]

    return {
        "schema": REPORT_SCHEMA,
        "round_count": len(round_reports),
        "rounds": round_reports,
        "combat_recovery_relevant_rounds": [
            row["round"] for row in recovery_rounds
        ],
        "combat_recovery_available_rounds": [
            row["round"]
            for row in recovery_rounds
            if row["combat_recovery_available"]
        ],
        "combat_recovery_unavailable_rounds": [
            row["round"]
            for row in recovery_rounds
            if not row["combat_recovery_available"]
        ],
        "engagement_relevant_rounds": [
            row["round"] for row in engagement_rounds
        ],
        "engagement_available_rounds": [
            row["round"]
            for row in engagement_rounds
            if row["engagement_available"]
        ],
        "engagement_unavailable_rounds": [
            row["round"]
            for row in engagement_rounds
            if not row["engagement_available"]
        ],
        "all_recovery_relevant_rounds_had_recovery_tool": (
            bool(recovery_rounds)
            and all(row["combat_recovery_available"] for row in recovery_rounds)
        ),
        "all_engagement_relevant_rounds_had_engagement_tool": (
            bool(engagement_rounds)
            and all(row["engagement_available"] for row in engagement_rounds)
        ),
        "ranking_cause_supported_by_availability": (
            bool(recovery_rounds or engagement_rounds)
            and all(
                row["combat_recovery_available"]
                for row in recovery_rounds
            )
            and all(
                row["engagement_available"]
                for row in engagement_rounds
            )
        ),
    }


def audit_pair06_v8_combat_action_availability_trajectory(
    payload: bytes,
) -> dict[str, Any]:
    _validated_hypothesis()
    return _audit_rows(_decision_rows_from_payload(payload))


def pair06_v8_combat_action_availability_audit_contract() -> dict[str, Any]:
    reviewed = _validated_hypothesis()
    return {
        "schema": CONTRACT_SCHEMA,
        "hypothesis_main_head": HYPOTHESIS_MAIN_HEAD,
        "hypothesis_git_blob": HYPOTHESIS_GIT_BLOB,
        "warm_start_runner_fixture_git_blob": (
            WARM_START_RUNNER_FIXTURE_GIT_BLOB
        ),
        "joint_host_fixture_git_blob": JOINT_HOST_FIXTURE_GIT_BLOB,
        "legacy_warm_start_runner_sha256": (
            LEGACY_WARM_START_RUNNER_SHA256
        ),
        "trajectory_sha256": TRAJECTORY_SHA256,
        "run_id": RUN_ID,
        "expected_rounds": EXPECTED_ROUNDS,
        "trajectory_persists_exact_tool_contract": True,
        "offered_tool_names_audited_per_round": True,
        "typed_legal_units_audited_per_round": True,
        "predecision_combat_count_audited_per_round": True,
        "predecision_visible_enemy_count_audited_per_round": True,
        "recovery_tool_definition": "offered_name_prefix:train_unit_",
        "engagement_tool_names": sorted(ENGAGEMENT_TOOL_NAMES),
        "base_move_and_attack_move_require_combat_units": True,
        "base_attack_target_requires_combat_units_and_visible_enemy": True,
        "typed_training_functions_derive_from_current_legal_units": True,
        "audit_implemented": True,
        "host_file_read_implemented": False,
        "host_file_read_performed": False,
        "trajectory_audited_by_contract_inspection": False,
        "ranking_cause_supported_by_current_contract_inspection": False,
        "policy_change_authorized": False,
        "runtime_execution_authorized": False,
        "replay_authorized": False,
        "training_authorized": False,
        "automatic_corpus_admission": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_hypothesis": reviewed,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def observe_or_change_policy(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatActionAvailabilityAuditHold(NEXT_GATE)
