"""Bounded source-only command materializer for Abaddon Generation-2.

This module closes only the deterministic command-materialization source gap.
It derives tokenized argv templates from the exact accepted Generation-2
orchestrator ledger and preserves the already-reviewed cross-control runtime
identity without resolving host paths, allocating workdirs, starting runtimes,
or executing commands.

No filesystem, Git, subprocess, network, Ollama, Docker, service, model, game,
training, deployment, VOID-chain, wallet, or funds action is performed here.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_cross_control_runtime_selector_generation2
    as selector,
)
from openra_env.learning import (
    abaddon_policy_campaign_cross_control_runtime_selector_source_binding_review_generation2
    as selector_review,
)
from tools import abaddon_policy_campaign_orchestrator_generation2 as orchestrator

CONTRACT_SCHEMA = "void.abaddon.generation2.command-materializer-contract.v1"
COMMAND_SCHEMA = "void.abaddon.generation2.materialized-command.v1"

SELECTOR_REVIEW_GIT_BLOB = "63b10239738980873bb26fc4f238b5c3e982a33e"
SELECTOR_GIT_BLOB = "3ddf54f0fe8a37006d1e272bab62d14faa5904c0"
EXECUTION_ADAPTER_GIT_BLOB = "994d44d751c530619649322c72a65edf15f6a8c3"
ORCHESTRATOR_GIT_BLOB = "8948b53d002e5d7e48a7aef2ec10ff5d690f5a1c"
CAMPAIGN_PLAN_GIT_BLOB = "86c6feb3072f9d540dbd4f7ee6462addcbac54aa"
CANDIDATE_WRAPPER_GIT_BLOB = "61eaefee39ebd90df0ddd8c649d9f0f9b64b1776"
CANDIDATE_FIXTURE_GIT_BLOB = "20091bff54edbb567127722fae81e5a5308737d2"

SELECTOR_SOURCE_SHA256 = (
    "19cd2c02e4232cee01e31286eee545237d61d7839542914899a1abf016fe26f4"
)
CANDIDATE_WRAPPER_SOURCE_SHA256 = (
    "686f88836e73acf9c78bfc1417db735b11100c07c34ce8da291047edd99eea9f"
)
CANDIDATE_FIXTURE_SHA256 = (
    "3fabbe9bc9b44830ee8e13e748d84ada881c6a3604f40c27609a953cabfd7768"
)
CANDIDATE_GENOME_SHA256 = (
    "8253ea5f1b3a709c8d64fb0432d13ac1c52ee82678e2f3b0ec730fe23d603089"
)
PARENT_GENOME_SHA256 = (
    "3c4346e0c92ea7225425d9ff4fd7ae12daa44162b06d471530179325b7d38a26"
)
LEGACY_RUNNER_SHA256 = (
    "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
)
LEGACY_RUNNER_BASENAME = (
    "void-actual-apollyon-vs-abaddon-warm-start-combat-spar-v1_4.py"
)

CANDIDATE_WRAPPER_REL = "tools/abaddon_policy_candidate_duel_wrapper.py"
CANDIDATE_FIXTURE_REL = (
    "fixtures/learning/abaddon-policy-genome-generation-2-candidate-252.json"
)

PYTHON_EXECUTABLE = "python3"
LEGACY_RUNNER_TOKEN = "<LEGACY_RUNNER_PATH>"
CANDIDATE_WRAPPER_TOKEN = "<CANDIDATE_WRAPPER_PATH>"
CANDIDATE_GENOME_TOKEN = "<CANDIDATE_GENOME_PATH>"

RUNNER_FLAGS = (
    "--seed",
    "--doctrine",
    "--rounds",
    "--ticks-per-round",
    "--starter-infantry",
    "--staging-max-ticks",
)

PRE_COMMAND_BLOCKERS = (
    "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
    "COMMAND_MATERIALIZER_NOT_IMPLEMENTED",
    "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
)
PRE_COMMAND_SOURCE_BLOCKERS = (
    "COMMAND_MATERIALIZER_NOT_IMPLEMENTED",
    "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
)
POST_COMMAND_BLOCKERS = (
    "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
    "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
)
POST_COMMAND_SOURCE_BLOCKERS = (
    "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
)

NEXT_GATE = "COMMAND_MATERIALIZER_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_command_materializer_source_binding_review"


class CommandMaterializerHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise CommandMaterializerHold(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


def _validate_review_frontier_constants() -> dict[str, Any]:
    """Validate accepted review constants without invoking its expensive census."""
    _require(
        selector_review.SELECTOR_GIT_BLOB == SELECTOR_GIT_BLOB,
        "selector-review accepted selector blob drift",
    )
    _require(
        selector_review.SELECTOR_SOURCE_SHA256 == SELECTOR_SOURCE_SHA256,
        "selector-review accepted selector SHA drift",
    )
    _require(
        tuple(selector_review.EXECUTION_MATERIALIZATION_BLOCKERS)
        == PRE_COMMAND_BLOCKERS,
        "pre-command execution blocker set drift",
    )
    _require(
        tuple(selector_review.EXECUTION_SOURCE_BLOCKERS)
        == PRE_COMMAND_SOURCE_BLOCKERS,
        "pre-command source blocker set drift",
    )
    _require(
        selector_review.NEXT_GATE == "COMMAND_MATERIALIZER_IMPLEMENTATION_REQUIRED",
        "accepted review next gate drift",
    )
    _require(
        selector_review.NEXT_CHANGE_CLASS
        == "source_only_command_materializer_implementation",
        "accepted review next change class drift",
    )
    _require(
        selector.POST_SELECTOR_BLOCKERS == PRE_COMMAND_BLOCKERS,
        "selector post-selector blockers drift",
    )
    _require(
        selector.POST_SELECTOR_SOURCE_BLOCKERS == PRE_COMMAND_SOURCE_BLOCKERS,
        "selector post-selector source blockers drift",
    )
    return {
        "selector_reviewed_by_separate_accepted_source": True,
        "selector_review_git_blob": SELECTOR_REVIEW_GIT_BLOB,
        "selector_git_blob": SELECTOR_GIT_BLOB,
        "selector_source_sha256": SELECTOR_SOURCE_SHA256,
        "runtime_execution_authorized": False,
        "command_materializer_implemented_before_this_source": False,
        "isolated_workdir_allocator_implemented": False,
        "pre_command_blockers": PRE_COMMAND_BLOCKERS,
        "pre_command_source_blockers": PRE_COMMAND_SOURCE_BLOCKERS,
    }


def _runtime_binding(row: Mapping[str, Any]) -> dict[str, Any]:
    opponent = row.get("apollyon_opponent")
    _require(isinstance(opponent, Mapping), "opponent binding missing")
    snapshot_id = opponent.get("snapshot_id")
    _require(
        snapshot_id in selector.EXPECTED_RUNTIME_BINDINGS,
        f"unreviewed runtime snapshot: {snapshot_id!r}",
    )
    expected = selector.EXPECTED_RUNTIME_BINDINGS[snapshot_id]
    _require(
        opponent.get("snapshot_sha256") == expected["snapshot_sha256"],
        f"runtime snapshot SHA drift: {snapshot_id}",
    )
    _require(
        opponent.get("selection_boundary")
        == "EXTERNAL_PRELAUNCH_REVIEWED_RUNTIME_REALIZATION",
        "runtime selection boundary drift",
    )
    _require(
        opponent.get("selection_performed") is False,
        "orchestrator unexpectedly performs runtime selection",
    )
    _require(
        opponent.get("runtime_started") is False,
        "orchestrator unexpectedly starts runtime",
    )
    realization = opponent.get("runtime_realization")
    _require(isinstance(realization, Mapping), "embedded runtime realization missing")
    _require(
        realization.get("snapshot_id") == snapshot_id,
        "embedded runtime snapshot identity drift",
    )
    _require(
        realization.get("snapshot_sha256") == expected["snapshot_sha256"],
        "embedded runtime snapshot SHA drift",
    )
    _require(
        realization.get("runtime_class") == expected["runtime_class"],
        "embedded runtime class drift",
    )
    _require(realization.get("blockers") == [], "embedded runtime blockers present")
    _require(
        realization.get("current_campaign_runtime_realized") is True,
        "runtime is not realized for current campaign",
    )
    _require(
        realization.get("portable_current_checkout_binding_complete") is True,
        "runtime portable binding incomplete",
    )
    return {
        "selection_key": snapshot_id,
        "opponent_snapshot_id": snapshot_id,
        "opponent_snapshot_sha256": expected["snapshot_sha256"],
        "runtime_class": expected["runtime_class"],
        "runtime_realization_sha256": _digest(realization),
        "selection_boundary": opponent["selection_boundary"],
        "selection_is_source_only": True,
        "runtime_started": False,
        "runtime_execution_authorized": False,
    }


@lru_cache(maxsize=1)
def _ledger_index_cached() -> dict[tuple[int, str], dict[str, Any]]:
    """Build the accepted 36-arm ledger exactly once per process."""
    _validate_review_frontier_constants()
    rows = orchestrator.arm_ledger()
    _require(len(rows) == 36, "orchestrator arm-ledger cardinality drift")

    result: dict[tuple[int, str], dict[str, Any]] = {}
    pair_runtime: dict[int, tuple[str, str]] = {}

    for row in rows:
        _require(isinstance(row, Mapping), "orchestrator ledger row malformed")
        pair_slot = row.get("pair_slot")
        arm = row.get("arm")
        _require(
            type(pair_slot) is int and 1 <= pair_slot <= 18,
            "orchestrator pair_slot drift",
        )
        _require(arm in {"baseline", "candidate"}, "orchestrator arm drift")
        key = (pair_slot, str(arm))
        _require(key not in result, f"duplicate orchestrator arm: {key}")
        _require(
            row.get("execution_state") == "NOT_EXECUTED",
            "orchestrator row unexpectedly executed",
        )
        authority = row.get("authority")
        _require(isinstance(authority, Mapping), "orchestrator authority missing")
        _require(
            authority.get("runtime_execution_authorized") is False,
            "orchestrator unexpectedly authorizes runtime",
        )
        _require(authority.get("game_execution") is False, "game execution boundary crossed")
        _require(authority.get("model_execution") is False, "model execution boundary crossed")
        _require(authority.get("training") is False, "training boundary crossed")
        _require(authority.get("weights_updated") is False, "weight boundary crossed")
        _require(authority.get("deployment") is False, "deployment boundary crossed")

        runner = row.get("runner_contract")
        _require(isinstance(runner, Mapping), "runner contract missing")
        _require(
            runner.get("legacy_runner_sha256") == LEGACY_RUNNER_SHA256,
            "legacy runner identity drift",
        )
        _require(tuple(runner.get("flags", ())) == RUNNER_FLAGS, "runner flags drift")
        values = runner.get("cli_values")
        _require(isinstance(values, Mapping), "runner CLI values missing")
        _require(set(values) == set(RUNNER_FLAGS), "runner CLI key set drift")
        _require(
            runner.get("command_materialized") is False,
            "orchestrator unexpectedly materializes command",
        )
        _require(
            runner.get("subprocess_invocation_materialized") is False,
            "orchestrator unexpectedly materializes subprocess",
        )

        policy = row.get("abaddon_policy")
        _require(isinstance(policy, Mapping), "Abaddon policy binding missing")
        candidate = arm == "candidate"
        _require(
            policy.get("wrapper_required") is candidate,
            "candidate-wrapper requirement drift",
        )
        if candidate:
            _require(
                policy.get("policy_source") == "bounded_deterministic_mutation",
                "candidate policy source drift",
            )
            _require(
                policy.get("genome_sha256") == CANDIDATE_GENOME_SHA256,
                "candidate genome identity drift",
            )
            _require(
                policy.get("reviewed_wrapper_sha256")
                == CANDIDATE_WRAPPER_SOURCE_SHA256,
                "reviewed wrapper SHA drift",
            )
            _require(
                policy.get("candidate_file_sha256") == CANDIDATE_FIXTURE_SHA256,
                "candidate fixture SHA drift",
            )
        else:
            _require(
                policy.get("policy_source") == "controller_defaults",
                "baseline policy source drift",
            )
            _require(
                policy.get("genome_sha256") == PARENT_GENOME_SHA256,
                "baseline genome identity drift",
            )

        runtime = _runtime_binding(row)
        binding = (runtime["selection_key"], runtime["runtime_realization_sha256"])
        if pair_slot in pair_runtime:
            _require(
                pair_runtime[pair_slot] == binding,
                f"matched-pair runtime disagreement: {pair_slot}",
            )
        else:
            pair_runtime[pair_slot] = binding

        result[key] = {
            **deepcopy(dict(row)),
            "_accepted_runtime_binding": runtime,
        }

    _require(len(result) == 36, "accepted ledger key count drift")
    _require(len(pair_runtime) == 18, "matched-pair runtime count drift")
    return result


def _canonical_row(*, pair_slot: int, arm: str) -> dict[str, Any]:
    _require(type(pair_slot) is int, "pair_slot must be int")
    _require(arm in {"baseline", "candidate"}, "unsupported arm")
    row = _ledger_index_cached().get((pair_slot, arm))
    _require(row is not None, "canonical ledger row not found")
    return deepcopy(row)


def _runner_argv(row: Mapping[str, Any]) -> tuple[str, ...]:
    values = row["runner_contract"]["cli_values"]
    output: list[str] = []
    for flag in RUNNER_FLAGS:
        value = values[flag]
        _require(
            isinstance(value, (str, int)) and not isinstance(value, bool),
            f"runner CLI value type unsupported: {flag}",
        )
        output.extend((flag, str(value)))
    return tuple(output)


def _path_bindings(arm: str) -> dict[str, dict[str, Any]]:
    legacy = {
        "token": LEGACY_RUNNER_TOKEN,
        "kind": "reviewed_external_exact_file",
        "path_resolved": False,
        "basename": LEGACY_RUNNER_BASENAME,
        "sha256": LEGACY_RUNNER_SHA256,
        "used_in_argv": arm == "baseline",
    }
    if arm == "baseline":
        return {"legacy_runner": legacy}
    return {
        "candidate_wrapper": {
            "token": CANDIDATE_WRAPPER_TOKEN,
            "kind": "accepted_checkout_relative_file",
            "path_resolved": False,
            "relative_path": CANDIDATE_WRAPPER_REL,
            "git_blob": CANDIDATE_WRAPPER_GIT_BLOB,
            "sha256": CANDIDATE_WRAPPER_SOURCE_SHA256,
            "used_in_argv": True,
        },
        "candidate_genome": {
            "token": CANDIDATE_GENOME_TOKEN,
            "kind": "accepted_checkout_relative_file",
            "path_resolved": False,
            "relative_path": CANDIDATE_FIXTURE_REL,
            "git_blob": CANDIDATE_FIXTURE_GIT_BLOB,
            "sha256": CANDIDATE_FIXTURE_SHA256,
            "semantic_genome_sha256": CANDIDATE_GENOME_SHA256,
            "used_in_argv": True,
        },
        "candidate_wrapper_legacy_runner_dependency": {
            **legacy,
            "used_in_argv": False,
            "consumer": "candidate_wrapper_internal_exact_dependency",
        },
    }


def materialize_command(*, pair_slot: int, arm: str) -> dict[str, Any]:
    """Return one deterministic tokenized argv receipt; execute nothing."""
    row = _canonical_row(pair_slot=pair_slot, arm=arm)
    runner_argv = _runner_argv(row)
    path_bindings = _path_bindings(arm)

    if arm == "baseline":
        argv_template = (
            PYTHON_EXECUTABLE,
            LEGACY_RUNNER_TOKEN,
            *runner_argv,
        )
    else:
        argv_template = (
            PYTHON_EXECUTABLE,
            CANDIDATE_WRAPPER_TOKEN,
            "--abaddon-candidate-genome",
            CANDIDATE_GENOME_TOKEN,
            "--expected-candidate-file-sha256",
            CANDIDATE_FIXTURE_SHA256,
            *runner_argv,
        )

    runtime = row.pop("_accepted_runtime_binding")
    body = {
        "schema": COMMAND_SCHEMA,
        "execution_index": row["execution_index"],
        "pair_slot": pair_slot,
        "arm": arm,
        "workdir_token": f"generation2/pair-{pair_slot:02d}/{arm}",
        "python_executable": PYTHON_EXECUTABLE,
        "argv_template": argv_template,
        "runner_argv": runner_argv,
        "path_bindings": path_bindings,
        "argv_template_materialized": True,
        "argv_materialized": True,
        "argv_contains_unresolved_path_tokens": True,
        "path_bindings_resolved": False,
        "shell_command_materialized": False,
        "subprocess_invocation_materialized": False,
        "process_spawn_implemented": False,
        "command_execution_performed": False,
        "workdir_materialized": False,
        "workdir_created": False,
        "runtime_selection_key": runtime["selection_key"],
        "opponent_snapshot_id": runtime["opponent_snapshot_id"],
        "opponent_snapshot_sha256": runtime["opponent_snapshot_sha256"],
        "runtime_realization_sha256": runtime["runtime_realization_sha256"],
        "runtime_class": runtime["runtime_class"],
        "runtime_selection_preserved": True,
        "runtime_selection_recomputed_by_selector": False,
        "runtime_started": False,
        "runtime_execution_authorized": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "remaining_blockers": POST_COMMAND_BLOCKERS,
        "remaining_source_blockers": POST_COMMAND_SOURCE_BLOCKERS,
    }
    return {**body, "command_sha256": _digest(body)}


def all_materialized_commands() -> list[dict[str, Any]]:
    index = _ledger_index_cached()
    ordered = sorted(index.values(), key=lambda row: int(row["execution_index"]))
    return [
        materialize_command(pair_slot=int(row["pair_slot"]), arm=str(row["arm"]))
        for row in ordered
    ]


def command_materializer_contract() -> dict[str, Any]:
    frontier = _validate_review_frontier_constants()
    index = _ledger_index_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "selector_review_git_blob": SELECTOR_REVIEW_GIT_BLOB,
        "selector_git_blob": SELECTOR_GIT_BLOB,
        "execution_adapter_git_blob": EXECUTION_ADAPTER_GIT_BLOB,
        "orchestrator_git_blob": ORCHESTRATOR_GIT_BLOB,
        "campaign_plan_git_blob": CAMPAIGN_PLAN_GIT_BLOB,
        "candidate_wrapper_git_blob": CANDIDATE_WRAPPER_GIT_BLOB,
        "candidate_wrapper_source_sha256": CANDIDATE_WRAPPER_SOURCE_SHA256,
        "candidate_fixture_git_blob": CANDIDATE_FIXTURE_GIT_BLOB,
        "candidate_fixture_sha256": CANDIDATE_FIXTURE_SHA256,
        "candidate_genome_sha256": CANDIDATE_GENOME_SHA256,
        "legacy_runner_sha256": LEGACY_RUNNER_SHA256,
        "command_materializer_implemented": True,
        "command_materializer_reviewed": False,
        "source_only_command_materialization": True,
        "accepted_frontier_validated_by_constants": True,
        "accepted_ledger_built_once_per_process": True,
        "argv_template_materialized": True,
        "path_bindings_explicit": True,
        "path_bindings_resolved": False,
        "isolated_workdir_allocator_implemented": False,
        "runtime_selection_preserved": True,
        "runtime_execution_authorized": False,
        "runtime_started": False,
        "process_spawn_implemented": False,
        "command_execution_performed": False,
        "shell_command_materialized": False,
        "execution_descriptor_count": len(index),
        "matched_pair_count": 18,
        "baseline_command_count": 18,
        "candidate_command_count": 18,
        "runner_flag_count": len(RUNNER_FLAGS),
        "runner_flags": RUNNER_FLAGS,
        "pre_command_blockers": PRE_COMMAND_BLOCKERS,
        "post_command_blockers": POST_COMMAND_BLOCKERS,
        "pre_command_source_blockers": PRE_COMMAND_SOURCE_BLOCKERS,
        "post_command_source_blockers": POST_COMMAND_SOURCE_BLOCKERS,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "frontier": frontier,
    }


def allocate_isolated_workdir(*args: Any, **kwargs: Any) -> None:
    raise CommandMaterializerHold(NEXT_GATE)


def advance_execution_materialization(*args: Any, **kwargs: Any) -> None:
    raise CommandMaterializerHold(NEXT_GATE)


def execute_materialized_command(*args: Any, **kwargs: Any) -> None:
    raise CommandMaterializerHold("RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED")


def start_runtime(*args: Any, **kwargs: Any) -> None:
    raise CommandMaterializerHold("RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED")


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    raise CommandMaterializerHold("RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED")
