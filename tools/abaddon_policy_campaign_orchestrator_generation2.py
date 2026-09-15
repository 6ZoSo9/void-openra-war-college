"""Fail-closed non-executing Abaddon Generation-2 campaign orchestrator.

This module is an orchestration contract only. It builds and validates the exact
36-arm ledger for the frozen Generation-2 candidate-252 campaign. It contains no
runtime/process/network/game execution implementation.

A separate reviewed execution implementation and explicit runtime authorization
are required before any arm can be launched.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning.abaddon_policy_campaign_plan_generation2 import (
    precommitted_campaign_plan,
)
from openra_env.learning.apollyon_opponent_runtime_realizations import (
    reviewed_opponent_runtime_realizations,
)

ORCHESTRATOR_SCHEMA = "void.abaddon.generation2.nonexecuting-orchestrator.v1"
EXECUTION_REQUEST_SCHEMA = "void.abaddon.generation2.execution-request.v1"

PLAN_FILE_SHA256 = "9a50b8100d33a6ae08578e5ef6e9bf59d5bd8edc537ed44853f3d8eca8bbb4e0"
PLAN_INTERNAL_SHA256 = "64e5003fa0d339ea1bea14eb0e4026e0dfe3455e86f38ef0fb9c0a26fbc4c594"
CANDIDATE_FILE_SHA256 = "3fabbe9bc9b44830ee8e13e748d84ada881c6a3604f40c27609a953cabfd7768"
CANDIDATE_GENOME_SHA256 = "8253ea5f1b3a709c8d64fb0432d13ac1c52ee82678e2f3b0ec730fe23d603089"
REVIEWED_WRAPPER_SHA256 = "686f88836e73acf9c78bfc1417db735b11100c07c34ce8da291047edd99eea9f"
LEGACY_RUNNER_SHA256 = "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
RUNTIME_REALIZATION_SET_SHA256 = (
    "1dbb861a3bc03a4423187846a519f228726cc890f4452c3b1d8607614288a7d8"
)
OPPONENT_SNAPSHOT_SET_SHA256 = (
    "d7bfce0cb1456ec440f6ab362c781057837c3912c557f865ae95b7ddc6278526"
)
PROTOCOL_PROPOSAL_SHA256 = (
    "3103a806c6b8b4cc1bc0897ddfa52297532b04d5c84394170011a476504639d3"
)
PROTOCOL_VALIDATION_SHA256 = (
    "7bac78ad8e74297b5645852a219d145cd6c4bc41293149e7331bfbe8e223dc38"
)
SOURCE_SPEC_SHA256 = (
    "9e4a870b549b00d6c2e05142caf23bb4d28fb2bab949e4a1b2f0ee1535f96cd7"
)

RUNNER_FLAGS = (
    "--seed",
    "--doctrine",
    "--rounds",
    "--ticks-per-round",
    "--starter-infantry",
    "--staging-max-ticks",
)

TERMINAL_POLICY = {
    "host_validation_weakening": False,
    "infrastructure_or_harness_failure": "STOP_CAMPAIGN",
    "matched_pair_scoring_excludes_terminal_pair_slots": True,
    "opponent_protocol_failure": "SEAL_NO_RETRY_CONTINUE",
    "synthetic_advance_fallback": False,
}

RESULT_RECORD_FIELDS = (
    "arm",
    "failed_round",
    "failure_class",
    "held_out",
    "last_host_rejection",
    "opponent_snapshot_id",
    "outcome",
    "pair_excluded_from_matched_scoring",
    "pair_slot",
    "partial_trajectory_sha256",
    "rounds_completed",
    "seed",
    "status",
    "summary_sha256",
    "terminal_no_retry",
    "trajectory_sha256",
    "warm_start_sha256",
)

EXPECTED_SNAPSHOT_IDS = {
    "apollyon-v13-v14-promoted",
    "apollyon-v13-v10-promoted",
    "apollyon-v2r13-qualified-predecessor",
    "apollyon-v3-v8-accepted-model-control",
}


class OrchestratorHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise OrchestratorHold(message)


def _collect_runtime_rows(value: Any, out: list[dict[str, Any]]) -> None:
    """Collect reviewed runtime descriptor objects without assuming container shape."""
    if isinstance(value, dict):
        snapshot_id = value.get("snapshot_id")
        if snapshot_id in EXPECTED_SNAPSHOT_IDS and "runtime_class" in value:
            out.append(value)
        for child in value.values():
            _collect_runtime_rows(child, out)
    elif isinstance(value, list):
        for child in value:
            _collect_runtime_rows(child, out)


def _runtime_index(realizations: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    _collect_runtime_rows(realizations, rows)

    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        snapshot_id = row.get("snapshot_id")
        _require(isinstance(snapshot_id, str), "runtime snapshot id malformed")
        frozen = deepcopy(row)
        if snapshot_id in result:
            _require(
                result[snapshot_id] == frozen,
                f"runtime descriptor disagreement: {snapshot_id}",
            )
        result[snapshot_id] = frozen

    _require(set(result) == EXPECTED_SNAPSHOT_IDS, "reviewed runtime snapshot set drift")

    for snapshot_id, row in result.items():
        _require(
            row.get("current_campaign_runtime_realized") is True,
            f"runtime not campaign realized: {snapshot_id}",
        )
        _require(
            row.get("runtime_surface_realized") is True,
            f"runtime surface unrealized: {snapshot_id}",
        )
        _require(
            row.get("warm_start_input_surface_compatible") is True,
            f"runtime warm-start incompatible: {snapshot_id}",
        )
        _require(
            row.get("portable_current_checkout_binding_complete") is True,
            f"runtime portable binding incomplete: {snapshot_id}",
        )
        _require(row.get("blockers") == [], f"runtime blockers present: {snapshot_id}")
    return result


def preflight() -> dict[str, Any]:
    plan = precommitted_campaign_plan()
    _require(
        plan.get("plan_sha256") == PLAN_INTERNAL_SHA256,
        "Generation-2 plan digest drift",
    )
    _require(
        plan.get("execution_eligible") is False,
        "Generation-2 plan unexpectedly execution eligible",
    )
    _require(
        plan.get("pre_execution_gates", {}).get("runtime_execution_authorized")
        is False,
        "Generation-2 runtime unexpectedly authorized",
    )
    _require(
        plan.get("opponent_runtime_realization_set_sha256")
        == RUNTIME_REALIZATION_SET_SHA256,
        "Generation-2 runtime realization-set binding drift",
    )
    _require(
        plan.get("opponent_snapshot_set_sha256") == OPPONENT_SNAPSHOT_SET_SHA256,
        "Generation-2 opponent snapshot-set binding drift",
    )

    realizations = reviewed_opponent_runtime_realizations()
    _require(
        realizations.get("realization_set_sha256")
        == RUNTIME_REALIZATION_SET_SHA256,
        "reviewed runtime realization-set digest drift",
    )
    _require(
        realizations.get("opponent_runtime_realization_complete") is True,
        "reviewed runtime realization set incomplete",
    )

    runtime_index = _runtime_index(realizations)
    pairs = plan.get("pair_slots")
    _require(
        isinstance(pairs, list) and len(pairs) == 18,
        "exactly 18 pair slots required",
    )
    for expected_slot, pair in enumerate(pairs, 1):
        _require(isinstance(pair, dict), f"pair {expected_slot} malformed")
        _require(
            pair.get("pair_slot") == expected_slot,
            f"pair slot order drift at {expected_slot}",
        )
        snapshot_id = pair.get("opponent_snapshot_id")
        _require(
            snapshot_id in runtime_index,
            f"pair {expected_slot} runtime binding missing",
        )
        runtime = runtime_index[snapshot_id]
        _require(
            runtime.get("snapshot_sha256")
            == pair.get("opponent_snapshot_sha256"),
            f"pair {expected_slot} runtime snapshot SHA drift",
        )
        _require(
            pair.get("execution_state") == "NOT_EXECUTED",
            f"pair {expected_slot} execution state drift",
        )

    return {
        "schema": ORCHESTRATOR_SCHEMA,
        "pair_slot_count": 18,
        "execution_count": 36,
        "runtime_binding_count": 4,
        "source_spec_sha256": SOURCE_SPEC_SHA256,
        "execution_implementation_present": False,
        "commands_materialized": False,
        "subprocess_invocation_materialized": False,
        "runtime_selection_performed": False,
        "runtime_started": False,
        "campaign_execution_authorized": False,
        "runtime_execution_authorized": False,
        "game_execution": False,
        "model_execution": False,
        "training": False,
        "weights_updated": False,
        "automatic_corpus_admission": False,
        "automatic_policy_promotion": False,
        "deployment": False,
    }


def arm_ledger() -> list[dict[str, Any]]:
    preflight()
    plan = precommitted_campaign_plan()
    runtime_index = _runtime_index(reviewed_opponent_runtime_realizations())

    rows: list[dict[str, Any]] = []
    execution_index = 1
    for pair in plan["pair_slots"]:
        snapshot_id = pair["opponent_snapshot_id"]
        runtime = runtime_index[snapshot_id]

        for arm_name, arm_key in (
            ("baseline", "baseline_arm"),
            ("candidate", "candidate_arm"),
        ):
            arm = pair[arm_key]
            candidate = arm_name == "candidate"
            rows.append(
                {
                    "execution_index": execution_index,
                    "pair_slot": pair["pair_slot"],
                    "arm": arm_name,
                    "held_out": pair["held_out"],
                    "execution_state": "NOT_EXECUTED",
                    "runner_contract": {
                        "legacy_runner_sha256": LEGACY_RUNNER_SHA256,
                        "flags": RUNNER_FLAGS,
                        "cli_values": {
                            "--seed": pair["seed"],
                            "--doctrine": pair["abaddon_doctrine"],
                            "--rounds": pair["rounds"],
                            "--ticks-per-round": pair["ticks_per_round"],
                            "--starter-infantry": pair["starter_infantry"],
                            "--staging-max-ticks": pair["staging_max_ticks"],
                        },
                        "command_materialized": False,
                        "subprocess_invocation_materialized": False,
                    },
                    "abaddon_policy": {
                        "policy_source": arm["policy_source"],
                        "genome_sha256": arm["abaddon_genome_sha256"],
                        "wrapper_required": candidate,
                        "reviewed_wrapper_sha256": (
                            REVIEWED_WRAPPER_SHA256 if candidate else None
                        ),
                        "candidate_file_sha256": (
                            CANDIDATE_FILE_SHA256 if candidate else None
                        ),
                        "candidate_genome_sha256": (
                            CANDIDATE_GENOME_SHA256 if candidate else None
                        ),
                    },
                    "apollyon_opponent": {
                        "snapshot_id": snapshot_id,
                        "snapshot_sha256": pair["opponent_snapshot_sha256"],
                        "role": pair["opponent_role"],
                        "selection_boundary": (
                            "EXTERNAL_PRELAUNCH_REVIEWED_RUNTIME_REALIZATION"
                        ),
                        "runtime_realization": deepcopy(runtime),
                        "selection_performed": False,
                        "runtime_started": False,
                    },
                    "pair_binding": deepcopy(pair["pair_binding"]),
                    "terminal_policy": deepcopy(TERMINAL_POLICY),
                    "expected_result_record_fields": RESULT_RECORD_FIELDS,
                    "authority": {
                        "campaign_execution_authorized": False,
                        "runtime_execution_authorized": False,
                        "game_execution": False,
                        "model_execution": False,
                        "training": False,
                        "weights_updated": False,
                        "automatic_corpus_admission": False,
                        "automatic_policy_promotion": False,
                        "deployment": False,
                    },
                }
            )
            execution_index += 1

    _require(len(rows) == 36, "exactly 36 execution arms required")
    _require(
        sum(row["arm"] == "baseline" for row in rows) == 18,
        "baseline arm count drift",
    )
    _require(
        sum(row["arm"] == "candidate" for row in rows) == 18,
        "candidate arm count drift",
    )
    return rows


def execution_request(*, pair_slot: int, arm: str) -> dict[str, Any]:
    """Return a fail-closed request descriptor; never materialize or run a command."""
    _require(
        type(pair_slot) is int and 1 <= pair_slot <= 18,
        "pair_slot out of range",
    )
    _require(arm in {"baseline", "candidate"}, "arm unsupported")

    rows = [
        row
        for row in arm_ledger()
        if row["pair_slot"] == pair_slot and row["arm"] == arm
    ]
    _require(len(rows) == 1, "requested arm does not resolve uniquely")
    return {
        "schema": EXECUTION_REQUEST_SCHEMA,
        "arm": rows[0],
        "execution_implementation_present": False,
        "command_materialized": False,
        "subprocess_invocation_materialized": False,
        "runtime_selection_performed": False,
        "runtime_started": False,
        "campaign_execution_authorized": False,
        "runtime_execution_authorized": False,
        "eligible": False,
        "reasons": [
            "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
            "EXECUTION_IMPLEMENTATION_NOT_PRESENT",
        ],
    }


def execute_campaign(*args: Any, **kwargs: Any) -> None:
    """Always hold: execution is deliberately absent from this source."""
    raise OrchestratorHold(
        "EXECUTION_IMPLEMENTATION_NOT_PRESENT: "
        "this reviewed orchestrator source is non-executing"
    )
