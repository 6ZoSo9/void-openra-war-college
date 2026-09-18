"""Source-only isolated-workdir allocator for Abaddon Generation-2.

Consumes exact accepted command-materializer receipts and emits deterministic
isolated-workdir allocation receipts under an unresolved root token. This
module performs no host-path resolution, filesystem action, directory
creation, process spawn, command execution, or runtime start.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_command_materializer_generation2
    as command_materializer,
)
from openra_env.learning import (
    abaddon_policy_campaign_command_materializer_source_binding_review_generation2
    as materializer_review,
)

CONTRACT_SCHEMA = "void.abaddon.generation2.isolated-workdir-allocator-contract.v1"
ALLOCATION_SCHEMA = "void.abaddon.generation2.isolated-workdir-allocation.v1"

MATERIALIZER_REVIEW_GIT_BLOB = "dee3750ce5d6acce014a45711e515fccac283574"
MATERIALIZER_REVIEW_SOURCE_SHA256 = (
    "2172c015b77e51d2d44cd1c3e37d1caac58d945daec0f0652594b9969756cc0b"
)
COMMAND_MATERIALIZER_GIT_BLOB = "4836360e0d284454f815a2a2e32078d2565e6dea"
COMMAND_MATERIALIZER_SOURCE_SHA256 = (
    "d02a23e7c0d3e4fc8a9c087e511a66d0d32f72b24e6702c62e9b886fb9dfee5d"
)

ISOLATED_WORKDIR_ROOT_TOKEN = "<GENERATION2_ISOLATED_WORKDIR_ROOT>"

PRE_ALLOCATOR_BLOCKERS = (
    "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
    "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
)
PRE_ALLOCATOR_SOURCE_BLOCKERS = ("ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",)
POST_ALLOCATOR_BLOCKERS = ("RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",)
POST_ALLOCATOR_SOURCE_BLOCKERS: tuple[str, ...] = ()

NEXT_GATE = "ISOLATED_WORKDIR_ALLOCATOR_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_isolated_workdir_allocator_source_binding_review"


class IsolatedWorkdirAllocatorHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise IsolatedWorkdirAllocatorHold(message)


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
    _require(
        materializer_review.COMMAND_MATERIALIZER_GIT_BLOB
        == COMMAND_MATERIALIZER_GIT_BLOB,
        "accepted review command-materializer blob drift",
    )
    _require(
        materializer_review.COMMAND_MATERIALIZER_SOURCE_SHA256
        == COMMAND_MATERIALIZER_SOURCE_SHA256,
        "accepted review command-materializer SHA drift",
    )
    _require(
        tuple(materializer_review.EXECUTION_MATERIALIZATION_BLOCKERS)
        == PRE_ALLOCATOR_BLOCKERS,
        "pre-allocator execution blocker frontier drift",
    )
    _require(
        tuple(materializer_review.EXECUTION_SOURCE_BLOCKERS)
        == PRE_ALLOCATOR_SOURCE_BLOCKERS,
        "pre-allocator source blocker frontier drift",
    )
    _require(
        materializer_review.NEXT_GATE
        == "ISOLATED_WORKDIR_ALLOCATOR_IMPLEMENTATION_REQUIRED",
        "accepted review next gate drift",
    )
    _require(
        materializer_review.NEXT_CHANGE_CLASS
        == "source_only_isolated_workdir_allocator_implementation",
        "accepted review next change class drift",
    )
    _require(
        tuple(command_materializer.POST_COMMAND_BLOCKERS)
        == PRE_ALLOCATOR_BLOCKERS,
        "command-materializer blocker frontier drift",
    )
    _require(
        tuple(command_materializer.POST_COMMAND_SOURCE_BLOCKERS)
        == PRE_ALLOCATOR_SOURCE_BLOCKERS,
        "command-materializer source frontier drift",
    )
    return {
        "materializer_review_git_blob": MATERIALIZER_REVIEW_GIT_BLOB,
        "materializer_review_source_sha256": MATERIALIZER_REVIEW_SOURCE_SHA256,
        "command_materializer_git_blob": COMMAND_MATERIALIZER_GIT_BLOB,
        "command_materializer_source_sha256": COMMAND_MATERIALIZER_SOURCE_SHA256,
        "command_materializer_reviewed_by_separate_accepted_source": True,
        "runtime_execution_authorized": False,
        "isolated_workdir_allocator_implemented_before_this_source": False,
        "pre_allocator_blockers": PRE_ALLOCATOR_BLOCKERS,
        "pre_allocator_source_blockers": PRE_ALLOCATOR_SOURCE_BLOCKERS,
    }


def _validate_workdir_token(*, pair_slot: int, arm: str, token: str) -> tuple[str, ...]:
    expected = f"generation2/pair-{pair_slot:02d}/{arm}"
    _require(token == expected, "canonical workdir token drift")
    _require(not token.startswith("/"), "workdir token unexpectedly absolute")
    _require("\\" not in token, "workdir token contains backslash")
    parts = tuple(token.split("/"))
    _require(len(parts) == 3, "workdir token component count drift")
    _require(all(parts), "workdir token has empty component")
    _require(all(part not in {".", ".."} for part in parts), "workdir traversal component")
    _require(parts[0] == "generation2", "generation namespace drift")
    _require(parts[1] == f"pair-{pair_slot:02d}", "pair namespace drift")
    _require(parts[2] == arm, "arm namespace drift")
    return parts


@lru_cache(maxsize=1)
def _accepted_commands_cached() -> tuple[dict[str, Any], ...]:
    _validate_review_frontier_constants()
    rows = command_materializer.all_materialized_commands()
    _require(len(rows) == 36, "accepted command cardinality drift")
    seen: set[tuple[int, str]] = set()
    for row in rows:
        pair_slot = row.get("pair_slot")
        arm = row.get("arm")
        _require(type(pair_slot) is int and 1 <= pair_slot <= 18, "pair-slot drift")
        _require(arm in {"baseline", "candidate"}, "arm drift")
        key = (pair_slot, str(arm))
        _require(key not in seen, "duplicate accepted command key")
        seen.add(key)
        _validate_workdir_token(
            pair_slot=pair_slot,
            arm=str(arm),
            token=str(row.get("workdir_token")),
        )
        _require(
            tuple(row.get("remaining_blockers", ())) == PRE_ALLOCATOR_BLOCKERS,
            "accepted command blocker drift",
        )
        _require(
            tuple(row.get("remaining_source_blockers", ()))
            == PRE_ALLOCATOR_SOURCE_BLOCKERS,
            "accepted command source blocker drift",
        )
        _require(row.get("path_bindings_resolved") is False, "accepted command resolves paths")
        _require(row.get("workdir_materialized") is False, "accepted command materializes workdir")
        _require(row.get("workdir_created") is False, "accepted command creates workdir")
        _require(row.get("runtime_started") is False, "accepted command starts runtime")
        _require(
            row.get("runtime_execution_authorized") is False,
            "accepted command authorizes runtime",
        )
        _require(
            row.get("command_execution_performed") is False,
            "accepted command executes command",
        )
    _require(len(seen) == 36, "accepted command key count drift")
    return tuple(deepcopy(rows))


def _canonical_command(*, pair_slot: int, arm: str) -> dict[str, Any]:
    _require(type(pair_slot) is int, "pair_slot must be int")
    _require(arm in {"baseline", "candidate"}, "unsupported arm")
    for row in _accepted_commands_cached():
        if row["pair_slot"] == pair_slot and row["arm"] == arm:
            return deepcopy(row)
    raise IsolatedWorkdirAllocatorHold("canonical accepted command not found")


def allocate_from_materialized_command(
    command_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Build one deterministic allocation receipt; perform no host I/O."""
    _require(isinstance(command_receipt, Mapping), "command receipt must be object")
    pair_slot = command_receipt.get("pair_slot")
    arm = command_receipt.get("arm")
    _require(type(pair_slot) is int, "command pair_slot must be int")
    _require(arm in {"baseline", "candidate"}, "command arm unsupported")

    canonical = _canonical_command(pair_slot=pair_slot, arm=str(arm))
    _require(
        dict(command_receipt) == canonical,
        "command receipt is not canonical accepted materializer output",
    )

    token = canonical["workdir_token"]
    components = _validate_workdir_token(
        pair_slot=pair_slot,
        arm=str(arm),
        token=token,
    )
    pair_root_template = (
        f"{ISOLATED_WORKDIR_ROOT_TOKEN}/generation2/pair-{pair_slot:02d}"
    )
    path_template = f"{ISOLATED_WORKDIR_ROOT_TOKEN}/{token}"
    namespace_key = _digest(
        {
            "pair_slot": pair_slot,
            "arm": arm,
            "workdir_token": token,
            "command_sha256": canonical["command_sha256"],
        }
    )

    body = {
        "schema": ALLOCATION_SCHEMA,
        "execution_index": canonical["execution_index"],
        "pair_slot": pair_slot,
        "arm": arm,
        "command_sha256": canonical["command_sha256"],
        "workdir_token": token,
        "workdir_token_components": components,
        "workdir_root_token": ISOLATED_WORKDIR_ROOT_TOKEN,
        "pair_root_template": pair_root_template,
        "workdir_path_template": path_template,
        "namespace_key": namespace_key,
        "isolated_workdir_allocator_implemented": True,
        "allocation_receipt_materialized": True,
        "allocation_is_source_only": True,
        "workdir_path_template_materialized": True,
        "host_path_resolved": False,
        "filesystem_path_resolved": False,
        "path_bindings_resolved": False,
        "workdir_materialized": False,
        "workdir_created": False,
        "filesystem_action_performed": False,
        "directory_creation_implemented": False,
        "process_spawn_implemented": False,
        "command_execution_performed": False,
        "runtime_selection_key": canonical["runtime_selection_key"],
        "opponent_snapshot_id": canonical["opponent_snapshot_id"],
        "runtime_realization_sha256": canonical["runtime_realization_sha256"],
        "runtime_class": canonical["runtime_class"],
        "runtime_selection_preserved": True,
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
        "remaining_blockers": POST_ALLOCATOR_BLOCKERS,
        "remaining_source_blockers": POST_ALLOCATOR_SOURCE_BLOCKERS,
    }
    return {**body, "allocation_sha256": _digest(body)}


def allocate_isolated_workdir(*, pair_slot: int, arm: str) -> dict[str, Any]:
    return allocate_from_materialized_command(
        _canonical_command(pair_slot=pair_slot, arm=arm)
    )


def all_isolated_workdir_allocations() -> list[dict[str, Any]]:
    return [allocate_from_materialized_command(row) for row in _accepted_commands_cached()]


def isolated_workdir_allocator_contract() -> dict[str, Any]:
    frontier = _validate_review_frontier_constants()
    allocations = all_isolated_workdir_allocations()
    return {
        "schema": CONTRACT_SCHEMA,
        "materializer_review_git_blob": MATERIALIZER_REVIEW_GIT_BLOB,
        "materializer_review_source_sha256": MATERIALIZER_REVIEW_SOURCE_SHA256,
        "command_materializer_git_blob": COMMAND_MATERIALIZER_GIT_BLOB,
        "command_materializer_source_sha256": COMMAND_MATERIALIZER_SOURCE_SHA256,
        "isolated_workdir_allocator_implemented": True,
        "isolated_workdir_allocator_reviewed": False,
        "source_only_isolated_workdir_allocation": True,
        "canonical_command_receipt_required": True,
        "unresolved_root_token_required": True,
        "workdir_root_token": ISOLATED_WORKDIR_ROOT_TOKEN,
        "allocation_receipt_materialized": True,
        "workdir_path_template_materialized": True,
        "host_path_resolved": False,
        "filesystem_path_resolved": False,
        "workdir_materialized": False,
        "workdir_created": False,
        "filesystem_action_performed": False,
        "directory_creation_implemented": False,
        "path_bindings_resolved": False,
        "runtime_selection_preserved": True,
        "runtime_execution_authorized": False,
        "runtime_started": False,
        "process_spawn_implemented": False,
        "command_execution_performed": False,
        "execution_descriptor_count": len(allocations),
        "matched_pair_count": 18,
        "baseline_allocation_count": sum(row["arm"] == "baseline" for row in allocations),
        "candidate_allocation_count": sum(row["arm"] == "candidate" for row in allocations),
        "unique_namespace_count": len({row["namespace_key"] for row in allocations}),
        "unique_path_template_count": len(
            {row["workdir_path_template"] for row in allocations}
        ),
        "pre_allocator_blockers": PRE_ALLOCATOR_BLOCKERS,
        "post_allocator_blockers": POST_ALLOCATOR_BLOCKERS,
        "pre_allocator_source_blockers": PRE_ALLOCATOR_SOURCE_BLOCKERS,
        "post_allocator_source_blockers": POST_ALLOCATOR_SOURCE_BLOCKERS,
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


def advance_execution_materialization(*args: Any, **kwargs: Any) -> None:
    raise IsolatedWorkdirAllocatorHold(NEXT_GATE)


def create_isolated_workdir(*args: Any, **kwargs: Any) -> None:
    raise IsolatedWorkdirAllocatorHold("RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED")


def execute_materialized_command(*args: Any, **kwargs: Any) -> None:
    raise IsolatedWorkdirAllocatorHold("RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED")


def start_runtime(*args: Any, **kwargs: Any) -> None:
    raise IsolatedWorkdirAllocatorHold("RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED")


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    raise IsolatedWorkdirAllocatorHold("RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED")
