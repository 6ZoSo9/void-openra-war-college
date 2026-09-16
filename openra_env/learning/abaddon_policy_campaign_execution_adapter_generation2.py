"""Fail-closed non-executing execution-adapter contract for Abaddon Generation-2.

This module bridges the canonical 36-arm Generation-2 orchestration ledger to
future execution machinery without implementing or authorizing execution.

It:
  * derives deterministic per-arm execution descriptors,
  * validates result-receipt records against the frozen ledger,
  * seals terminal opponent-protocol failures as no-retry/excluded pair slots,
  * derives a deterministic resume cursor from admitted result records, and
  * preserves the reviewed warm-start normalization contract.

It does NOT:
  * materialize argv,
  * allocate/create work directories,
  * select/start a runtime,
  * spawn a process,
  * call a network endpoint,
  * launch OpenRA or a model,
  * train/update weights/promote policy,
  * write campaign evidence.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from typing import Any

from tools.abaddon_policy_campaign_orchestrator_generation2 import arm_ledger

ADAPTER_SCHEMA = "void.abaddon.generation2.execution-adapter-contract.v1"
DESCRIPTOR_SCHEMA = "void.abaddon.generation2.execution-descriptor.v1"
RESUME_SCHEMA = "void.abaddon.generation2.resume-plan.v1"

STATUS_COMPLETED = "completed"
STATUS_TERMINAL_OPPONENT_PROTOCOL_FAILURE = (
    "terminal_opponent_protocol_failure"
)
OUTCOME_DRAW_OR_UNFINISHED = "DRAW_OR_UNFINISHED"
FAILURE_OPPONENT_MODEL_PROTOCOL = "OPPONENT_MODEL_PROTOCOL_FAILURE"

WARM_START_BINDING_SCHEMA = "void.apollyon.warm-start-pair-binding.v1"
WARM_START_NORMALIZATION = (
    "remove warm_start_header.run_id only; stable canonical JSONL"
)

RESULT_RECORD_FIELDS = frozenset(
    {
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
    }
)

BASE_RESULT_FIELDS = frozenset(
    {
        "arm",
        "held_out",
        "opponent_snapshot_id",
        "pair_slot",
        "seed",
        "status",
        "warm_start_sha256",
    }
)

COMPLETED_REQUIRED_FIELDS = BASE_RESULT_FIELDS | frozenset(
    {
        "outcome",
        "summary_sha256",
        "trajectory_sha256",
    }
)

TERMINAL_REQUIRED_FIELDS = BASE_RESULT_FIELDS | frozenset(
    {
        "failed_round",
        "failure_class",
        "pair_excluded_from_matched_scoring",
        "partial_trajectory_sha256",
        "rounds_completed",
        "terminal_no_retry",
    }
)

COMPLETED_FORBIDDEN_FIELDS = frozenset(
    {
        "failed_round",
        "failure_class",
        "pair_excluded_from_matched_scoring",
        "partial_trajectory_sha256",
        "rounds_completed",
        "terminal_no_retry",
    }
)

TERMINAL_FORBIDDEN_FIELDS = frozenset(
    {
        "outcome",
        "summary_sha256",
        "trajectory_sha256",
    }
)

EXECUTION_BLOCKERS = (
    "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
    "CROSS_CONTROL_RUNTIME_SELECTOR_NOT_IMPLEMENTED",
    "COMMAND_MATERIALIZER_NOT_IMPLEMENTED",
    "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
)


class ExecutionAdapterHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ExecutionAdapterHold(message)


def _sha256(value: Any, label: str) -> str:
    _require(
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value),
        f"{label} must be lowercase SHA-256",
    )
    return value


def _ledger_index() -> dict[tuple[int, str], dict[str, Any]]:
    rows = arm_ledger()
    _require(len(rows) == 36, "canonical arm ledger cardinality drift")

    result: dict[tuple[int, str], dict[str, Any]] = {}
    for row in rows:
        _require(isinstance(row, Mapping), "canonical arm ledger row malformed")
        pair_slot = row.get("pair_slot")
        arm = row.get("arm")
        _require(
            type(pair_slot) is int and 1 <= pair_slot <= 18,
            "canonical pair_slot malformed",
        )
        _require(arm in {"baseline", "candidate"}, "canonical arm malformed")
        key = (pair_slot, arm)
        _require(key not in result, f"duplicate canonical arm ledger key: {key}")
        result[key] = deepcopy(dict(row))
    return result


def _workdir_token(pair_slot: int, arm: str) -> str:
    return f"generation2/pair-{pair_slot:02d}/{arm}"


def execution_descriptor(*, pair_slot: int, arm: str) -> dict[str, Any]:
    """Return a deterministic, explicitly non-runnable per-arm descriptor."""
    ledger = _ledger_index()
    key = (pair_slot, arm)
    _require(key in ledger, f"unknown Generation-2 arm: {key}")
    row = ledger[key]

    return {
        "schema": DESCRIPTOR_SCHEMA,
        "pair_slot": pair_slot,
        "arm": arm,
        "held_out": row["held_out"],
        "execution_index": row["execution_index"],
        "runner_contract": deepcopy(row["runner_contract"]),
        "abaddon_policy": deepcopy(row["abaddon_policy"]),
        "apollyon_opponent": deepcopy(row["apollyon_opponent"]),
        "pair_binding": deepcopy(row["pair_binding"]),
        "terminal_policy": deepcopy(row["terminal_policy"]),
        "workdir": {
            "token": _workdir_token(pair_slot, arm),
            "path_materialized": False,
            "created": False,
            "isolation_required": True,
        },
        "expected_outputs": {
            "trajectory": "trajectory.jsonl",
            "summary": "summary.json",
            "collected": False,
        },
        "warm_start_pair_binding": {
            "schema": WARM_START_BINDING_SCHEMA,
            "normalization": WARM_START_NORMALIZATION,
            "raw_sha256_equality_required": False,
            "normalized_sha256_equality_required": True,
            "binding_module": "openra_env.analysis.spar_pair_binding",
            "binding_function": "warm_start_identity",
            "binding_performed": False,
        },
        "command": {
            "argv_materialized": False,
            "shell_command_materialized": False,
            "process_spawn_implemented": False,
        },
        "runtime": {
            "cross_control_selector_implemented": False,
            "selection_performed": False,
            "started": False,
        },
        "eligible": False,
        "reasons": list(EXECUTION_BLOCKERS),
        "authority": {
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


def all_execution_descriptors() -> list[dict[str, Any]]:
    """Return all 36 non-runnable descriptors in canonical ledger order."""
    rows = _ledger_index()
    ordered = sorted(
        rows.values(),
        key=lambda row: int(row["execution_index"]),
    )
    return [
        execution_descriptor(
            pair_slot=int(row["pair_slot"]),
            arm=str(row["arm"]),
        )
        for row in ordered
    ]


def validate_result_record(record: Mapping[str, Any]) -> dict[str, Any]:
    """Validate one result-receipt record against the frozen Generation-2 ledger."""
    _require(isinstance(record, Mapping), "result record must be object")
    keys = set(record)
    unknown = keys - RESULT_RECORD_FIELDS
    _require(not unknown, f"unknown result-record fields: {sorted(unknown)}")

    missing_base = BASE_RESULT_FIELDS - keys
    _require(
        not missing_base,
        f"missing base result-record fields: {sorted(missing_base)}",
    )

    pair_slot = record.get("pair_slot")
    arm = record.get("arm")
    _require(type(pair_slot) is int, "result pair_slot must be integer")
    _require(arm in {"baseline", "candidate"}, "result arm unsupported")

    ledger = _ledger_index()
    key = (pair_slot, str(arm))
    _require(key in ledger, f"result record not in frozen ledger: {key}")
    expected = ledger[key]

    _require(
        record.get("seed") == expected["runner_contract"]["cli_values"]["--seed"],
        "result seed does not match frozen ledger",
    )
    _require(
        record.get("held_out") is expected["held_out"],
        "result held_out does not match frozen ledger",
    )
    _require(
        record.get("opponent_snapshot_id")
        == expected["apollyon_opponent"]["snapshot_id"],
        "result opponent snapshot does not match frozen ledger",
    )
    _sha256(record.get("warm_start_sha256"), "warm_start_sha256")

    status = record.get("status")
    if status == STATUS_COMPLETED:
        missing = COMPLETED_REQUIRED_FIELDS - keys
        _require(
            not missing,
            f"completed result missing fields: {sorted(missing)}",
        )
        forbidden = COMPLETED_FORBIDDEN_FIELDS & keys
        _require(
            not forbidden,
            f"completed result contains terminal fields: {sorted(forbidden)}",
        )
        _require(
            record.get("outcome") == OUTCOME_DRAW_OR_UNFINISHED,
            "completed result outcome drift",
        )
        _sha256(record.get("trajectory_sha256"), "trajectory_sha256")
        _sha256(record.get("summary_sha256"), "summary_sha256")

    elif status == STATUS_TERMINAL_OPPONENT_PROTOCOL_FAILURE:
        missing = TERMINAL_REQUIRED_FIELDS - keys
        _require(
            not missing,
            f"terminal result missing fields: {sorted(missing)}",
        )
        forbidden = TERMINAL_FORBIDDEN_FIELDS & keys
        _require(
            not forbidden,
            f"terminal result contains completed fields: {sorted(forbidden)}",
        )
        _require(
            record.get("failure_class") == FAILURE_OPPONENT_MODEL_PROTOCOL,
            "terminal failure_class drift",
        )
        _require(
            record.get("terminal_no_retry") is True,
            "terminal opponent protocol failure must be no-retry",
        )
        _require(
            record.get("pair_excluded_from_matched_scoring") is True,
            "terminal opponent protocol failure must exclude matched pair",
        )
        failed_round = record.get("failed_round")
        rounds_completed = record.get("rounds_completed")
        round_limit = expected["runner_contract"]["cli_values"]["--rounds"]
        _require(
            type(failed_round) is int and 1 <= failed_round <= round_limit,
            "terminal failed_round out of frozen round range",
        )
        _require(
            type(rounds_completed) is int
            and 0 <= rounds_completed < round_limit,
            "terminal rounds_completed out of frozen round range",
        )
        _sha256(
            record.get("partial_trajectory_sha256"),
            "partial_trajectory_sha256",
        )

    else:
        raise ExecutionAdapterHold(f"unsupported result status: {status!r}")

    return deepcopy(dict(record))


def validate_result_records(
    records: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Validate and canonicalize an unordered partial campaign result set."""
    _require(
        isinstance(records, Sequence)
        and not isinstance(records, (str, bytes)),
        "records must be array",
    )
    _require(len(records) <= 36, "result record count exceeds frozen campaign")

    admitted: dict[tuple[int, str], dict[str, Any]] = {}
    for index, record in enumerate(records):
        checked = validate_result_record(record)
        key = (checked["pair_slot"], checked["arm"])
        _require(key not in admitted, f"duplicate result record: {key}")
        admitted[key] = checked

    return [
        admitted[key]
        for key in sorted(
            admitted,
            key=lambda item: (
                int(_ledger_index()[item]["execution_index"]),
            ),
        )
    ]


def resume_plan(
    records: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Derive deterministic next work without executing or materializing commands.

    A terminal no-retry opponent-protocol failure seals the entire pair slot out
    of matched scoring and schedules neither arm again. Otherwise missing arms
    are considered in canonical ledger order.
    """
    admitted_rows = validate_result_records(records)
    admitted = {
        (row["pair_slot"], row["arm"]): row for row in admitted_rows
    }
    descriptors = all_execution_descriptors()

    terminal_pairs = {
        row["pair_slot"]
        for row in admitted_rows
        if row["status"] == STATUS_TERMINAL_OPPONENT_PROTOCOL_FAILURE
        and row["terminal_no_retry"] is True
        and row["pair_excluded_from_matched_scoring"] is True
    }

    pair_states: list[dict[str, Any]] = []
    complete_pairs = 0
    pending_pairs = 0
    sealed_pairs = 0

    for pair_slot in range(1, 19):
        baseline = admitted.get((pair_slot, "baseline"))
        candidate = admitted.get((pair_slot, "candidate"))

        if pair_slot in terminal_pairs:
            state = "SEALED_EXCLUDED_NO_RETRY"
            sealed_pairs += 1
        elif (
            baseline is not None
            and candidate is not None
            and baseline["status"] == STATUS_COMPLETED
            and candidate["status"] == STATUS_COMPLETED
        ):
            state = "COMPLETE_SCORABLE"
            complete_pairs += 1
        else:
            state = "PENDING"
            pending_pairs += 1

        pair_states.append(
            {
                "pair_slot": pair_slot,
                "state": state,
                "baseline_status": (
                    baseline["status"] if baseline is not None else None
                ),
                "candidate_status": (
                    candidate["status"] if candidate is not None else None
                ),
            }
        )

    missing_descriptors = []
    for descriptor in descriptors:
        key = (descriptor["pair_slot"], descriptor["arm"])
        if descriptor["pair_slot"] in terminal_pairs:
            continue
        if key in admitted:
            continue
        missing_descriptors.append(descriptor)

    next_descriptor = (
        deepcopy(missing_descriptors[0]) if missing_descriptors else None
    )

    return {
        "schema": RESUME_SCHEMA,
        "adapter_schema": ADAPTER_SCHEMA,
        "observed_result_count": len(admitted_rows),
        "complete_pair_count": complete_pairs,
        "sealed_excluded_pair_count": sealed_pairs,
        "pending_pair_count": pending_pairs,
        "pair_states": pair_states,
        "remaining_arm_count": len(missing_descriptors),
        "next_descriptor": next_descriptor,
        "all_remaining_descriptors": deepcopy(missing_descriptors),
        "campaign_receipt_complete": not missing_descriptors,
        "matched_scoring_pair_slots": [
            row["pair_slot"]
            for row in pair_states
            if row["state"] == "COMPLETE_SCORABLE"
        ],
        "excluded_pair_slots": sorted(terminal_pairs),
        "commands_materialized": False,
        "runtime_selection_performed": False,
        "runtime_started": False,
        "runtime_execution_authorized": False,
        "game_execution": False,
        "model_execution": False,
        "training": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
    }


def execute(*args: Any, **kwargs: Any) -> None:
    """Always hold: this contract contains no execution implementation."""
    raise ExecutionAdapterHold(
        "EXECUTION_IMPLEMENTATION_NOT_PRESENT: "
        "Generation-2 execution adapter is contract-only"
    )
