"""Source-only review of the accepted Generation-2 isolated-workdir allocator.

This separate review instrument pins the accepted allocator implementation by
exact Git blob and SHA-256, independently validates its deterministic 36
allocation receipts / 18 matched pairs, confirms the unresolved-root and
zero-filesystem-action boundaries, and closes only the allocator source-review
frontier.

It does not resolve a host path, create a directory, materialize a runtime
workdir, spawn a process, execute a command, start a runtime, load or run a
model, execute a game, train, deploy, mutate VOID, or move funds.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_isolated_workdir_allocator_generation2
    as allocator,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "isolated-workdir-allocator-source-binding-review-contract.v1"
)
REVIEW_SCHEMA = (
    "void.abaddon.generation2."
    "isolated-workdir-allocator-source-binding-review.v1"
)

ISOLATED_WORKDIR_ALLOCATOR_GIT_BLOB = "0890fb1e037ab21aa8312ab863e34cfc704e9ea2"
ISOLATED_WORKDIR_ALLOCATOR_SOURCE_SHA256 = (
    "7683a3e244f7d7a661816c48aef773abbbe2b805dc2cf95391ad1ab28ff986fb"
)
ISOLATED_WORKDIR_ALLOCATOR_TEST_GIT_BLOB = (
    "8eb3fcc0657211cf599388e132487bc45e2785ea"
)
ISOLATED_WORKDIR_ALLOCATOR_TEST_SHA256 = (
    "3d8eb684c6644901dbb7eb1c53cf04f5fb9bcf714fbd6ce072ae26d5cd459e6f"
)

MATERIALIZER_REVIEW_GIT_BLOB = "dee3750ce5d6acce014a45711e515fccac283574"
MATERIALIZER_REVIEW_SOURCE_SHA256 = (
    "2172c015b77e51d2d44cd1c3e37d1caac58d945daec0f0652594b9969756cc0b"
)
COMMAND_MATERIALIZER_GIT_BLOB = "4836360e0d284454f815a2a2e32078d2565e6dea"
COMMAND_MATERIALIZER_SOURCE_SHA256 = (
    "d02a23e7c0d3e4fc8a9c087e511a66d0d32f72b24e6702c62e9b886fb9dfee5d"
)

EXPECTED_RUNTIME_IDS = {
    "apollyon-v13-v14-promoted",
    "apollyon-v13-v10-promoted",
    "apollyon-v2r13-qualified-predecessor",
    "apollyon-v3-v8-accepted-model-control",
}

EXPECTED_ROOT_TOKEN = "<GENERATION2_ISOLATED_WORKDIR_ROOT>"

EXECUTION_MATERIALIZATION_BLOCKERS = tuple(allocator.POST_ALLOCATOR_BLOCKERS)
EXECUTION_SOURCE_BLOCKERS = tuple(allocator.POST_ALLOCATOR_SOURCE_BLOCKERS)

NEXT_GATE = "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED"
NEXT_CHANGE_CLASS = "runtime_execution_authorization"


class IsolatedWorkdirAllocatorSourceBindingReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise IsolatedWorkdirAllocatorSourceBindingReviewHold(message)


@lru_cache(maxsize=1)
def _validate_dependencies_cached() -> dict[str, Any]:
    implementation = allocator.isolated_workdir_allocator_contract()
    allocations = allocator.all_isolated_workdir_allocations()

    _require(
        allocator.MATERIALIZER_REVIEW_GIT_BLOB == MATERIALIZER_REVIEW_GIT_BLOB,
        "allocator materializer-review blob drift",
    )
    _require(
        allocator.MATERIALIZER_REVIEW_SOURCE_SHA256
        == MATERIALIZER_REVIEW_SOURCE_SHA256,
        "allocator materializer-review SHA drift",
    )
    _require(
        allocator.COMMAND_MATERIALIZER_GIT_BLOB == COMMAND_MATERIALIZER_GIT_BLOB,
        "allocator command-materializer blob drift",
    )
    _require(
        allocator.COMMAND_MATERIALIZER_SOURCE_SHA256
        == COMMAND_MATERIALIZER_SOURCE_SHA256,
        "allocator command-materializer SHA drift",
    )
    _require(
        implementation.get("isolated_workdir_allocator_implemented") is True,
        "isolated-workdir allocator implementation missing",
    )
    _require(
        implementation.get("isolated_workdir_allocator_reviewed") is False,
        "allocator unexpectedly self-reviews",
    )
    _require(
        implementation.get("next_gate")
        == "ISOLATED_WORKDIR_ALLOCATOR_SOURCE_BINDING_REVIEW_REQUIRED",
        "allocator review frontier drift",
    )
    _require(
        implementation.get("next_change_class")
        == "source_only_isolated_workdir_allocator_source_binding_review",
        "allocator next change class drift",
    )
    _require(
        tuple(implementation.get("post_allocator_blockers", ()))
        == ("RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",),
        "post-allocator execution blocker drift",
    )
    _require(
        tuple(implementation.get("post_allocator_source_blockers", ())) == (),
        "post-allocator source blocker drift",
    )
    _require(
        implementation.get("workdir_root_token") == EXPECTED_ROOT_TOKEN,
        "allocator root token drift",
    )

    for field in (
        "host_path_resolved",
        "filesystem_path_resolved",
        "workdir_materialized",
        "workdir_created",
        "filesystem_action_performed",
        "directory_creation_implemented",
        "path_bindings_resolved",
        "runtime_execution_authorized",
        "runtime_started",
        "process_spawn_implemented",
        "command_execution_performed",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        _require(implementation.get(field) is False, f"allocator boundary drift: {field}")

    _require(len(allocations) == 36, "allocation receipt cardinality drift")

    seen_keys: set[tuple[int, str]] = set()
    namespace_keys: set[str] = set()
    path_templates: set[str] = set()
    allocation_hashes: set[str] = set()
    runtime_ids: set[str] = set()
    by_pair: dict[int, dict[str, dict[str, Any]]] = {}

    for row in allocations:
        pair_slot = row.get("pair_slot")
        arm = row.get("arm")
        _require(
            type(pair_slot) is int and 1 <= pair_slot <= 18,
            "allocation pair-slot drift",
        )
        _require(arm in {"baseline", "candidate"}, "allocation arm drift")
        key = (pair_slot, str(arm))
        _require(key not in seen_keys, "duplicate allocation key")
        seen_keys.add(key)

        expected_token = f"generation2/pair-{pair_slot:02d}/{arm}"
        expected_pair_root = (
            f"{EXPECTED_ROOT_TOKEN}/generation2/pair-{pair_slot:02d}"
        )
        expected_path = f"{EXPECTED_ROOT_TOKEN}/{expected_token}"

        _require(row.get("workdir_token") == expected_token, "workdir token drift")
        _require(
            tuple(row.get("workdir_token_components", ()))
            == tuple(expected_token.split("/")),
            "workdir token component drift",
        )
        _require(
            row.get("workdir_root_token") == EXPECTED_ROOT_TOKEN,
            "allocation root token drift",
        )
        _require(
            row.get("pair_root_template") == expected_pair_root,
            "pair root template drift",
        )
        _require(
            row.get("workdir_path_template") == expected_path,
            "workdir path template drift",
        )

        _require(
            row.get("isolated_workdir_allocator_implemented") is True,
            "allocation does not bind allocator implementation",
        )
        _require(
            row.get("allocation_receipt_materialized") is True,
            "allocation receipt missing",
        )
        _require(
            row.get("allocation_is_source_only") is True,
            "allocation is not source-only",
        )
        _require(
            row.get("workdir_path_template_materialized") is True,
            "workdir path template missing",
        )

        for field in (
            "host_path_resolved",
            "filesystem_path_resolved",
            "path_bindings_resolved",
            "workdir_materialized",
            "workdir_created",
            "filesystem_action_performed",
            "directory_creation_implemented",
            "process_spawn_implemented",
            "command_execution_performed",
            "runtime_started",
            "runtime_execution_authorized",
            "model_load_performed",
            "model_inference_performed",
            "game_execution_performed",
            "training_performed",
            "weights_updated",
            "deployment_performed",
            "void_chain_mutation_performed",
            "wallet_or_funds_action_performed",
        ):
            _require(row.get(field) is False, f"allocation boundary drift: {field}")

        _require(
            tuple(row.get("remaining_blockers", ()))
            == ("RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",),
            "allocation remaining blocker drift",
        )
        _require(
            tuple(row.get("remaining_source_blockers", ())) == (),
            "allocation remaining source blocker drift",
        )

        namespace = row.get("namespace_key")
        path_template = row.get("workdir_path_template")
        allocation_sha = row.get("allocation_sha256")
        _require(
            isinstance(namespace, str) and len(namespace) == 64,
            "namespace key shape drift",
        )
        _require(
            isinstance(allocation_sha, str) and len(allocation_sha) == 64,
            "allocation digest shape drift",
        )
        _require(namespace not in namespace_keys, "namespace collision")
        _require(path_template not in path_templates, "path-template collision")
        _require(allocation_sha not in allocation_hashes, "allocation digest collision")
        namespace_keys.add(namespace)
        path_templates.add(str(path_template))
        allocation_hashes.add(allocation_sha)
        runtime_ids.add(str(row.get("opponent_snapshot_id")))
        by_pair.setdefault(pair_slot, {})[str(arm)] = row

    _require(len(seen_keys) == 36, "allocation key count drift")
    _require(len(namespace_keys) == 36, "namespace uniqueness drift")
    _require(len(path_templates) == 36, "path-template uniqueness drift")
    _require(len(allocation_hashes) == 36, "allocation digest uniqueness drift")
    _require(runtime_ids == EXPECTED_RUNTIME_IDS, "runtime control identity drift")
    _require(len(by_pair) == 18, "matched-pair count drift")

    for pair_slot, pair in by_pair.items():
        _require(
            set(pair) == {"baseline", "candidate"},
            f"matched-pair arm drift: {pair_slot}",
        )
        baseline = pair["baseline"]
        candidate = pair["candidate"]
        _require(
            baseline["pair_root_template"] == candidate["pair_root_template"],
            f"matched-pair root drift: {pair_slot}",
        )
        _require(
            baseline["workdir_path_template"] != candidate["workdir_path_template"],
            f"matched-pair path collision: {pair_slot}",
        )
        _require(
            baseline["namespace_key"] != candidate["namespace_key"],
            f"matched-pair namespace collision: {pair_slot}",
        )
        _require(
            baseline["runtime_selection_key"] == candidate["runtime_selection_key"],
            f"matched-pair runtime-selection drift: {pair_slot}",
        )
        _require(
            baseline["runtime_realization_sha256"]
            == candidate["runtime_realization_sha256"],
            f"matched-pair runtime-realization drift: {pair_slot}",
        )

    return {
        "allocator_git_blob": ISOLATED_WORKDIR_ALLOCATOR_GIT_BLOB,
        "allocator_source_sha256": ISOLATED_WORKDIR_ALLOCATOR_SOURCE_SHA256,
        "allocator_test_git_blob": ISOLATED_WORKDIR_ALLOCATOR_TEST_GIT_BLOB,
        "allocator_test_sha256": ISOLATED_WORKDIR_ALLOCATOR_TEST_SHA256,
        "materializer_review_git_blob": MATERIALIZER_REVIEW_GIT_BLOB,
        "materializer_review_source_sha256": MATERIALIZER_REVIEW_SOURCE_SHA256,
        "command_materializer_git_blob": COMMAND_MATERIALIZER_GIT_BLOB,
        "command_materializer_source_sha256": COMMAND_MATERIALIZER_SOURCE_SHA256,
        "allocator_source_identity_pinned": True,
        "allocator_source_is_not_self_bound": True,
        "allocation_receipt_count": 36,
        "matched_pair_count": 18,
        "baseline_allocation_count": 18,
        "candidate_allocation_count": 18,
        "runtime_control_count": 4,
        "unique_namespace_count": 36,
        "unique_path_template_count": 36,
        "unique_allocation_digest_count": 36,
        "workdir_root_token": EXPECTED_ROOT_TOKEN,
        "runtime_execution_authorized": False,
        "runtime_started": False,
        "filesystem_action_performed": False,
        "workdir_materialized": False,
        "allocations": deepcopy(allocations),
    }


def _validate_dependencies() -> dict[str, Any]:
    return deepcopy(_validate_dependencies_cached())


def isolated_workdir_allocator_source_binding_review() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    return {
        "schema": REVIEW_SCHEMA,
        "isolated_workdir_allocator_implemented": True,
        "isolated_workdir_allocator_source_binding_present": True,
        "isolated_workdir_allocator_reviewed": True,
        "allocator_source_identity_pinned_by_git_blob": True,
        "allocator_source_identity_pinned_by_sha256": True,
        "allocator_source_is_not_self_bound": True,
        "separate_review_instrument": True,
        "allocation_receipts_validated": True,
        "allocation_receipt_count": 36,
        "execution_descriptor_count": 36,
        "matched_pair_count": 18,
        "baseline_allocation_count": 18,
        "candidate_allocation_count": 18,
        "runtime_control_count": 4,
        "unique_namespace_count": 36,
        "unique_path_template_count": 36,
        "unique_allocation_digest_count": 36,
        "source_only_isolated_workdir_allocation": True,
        "workdir_root_token": EXPECTED_ROOT_TOKEN,
        "unresolved_root_token_preserved": True,
        "host_path_resolved": False,
        "filesystem_path_resolved": False,
        "path_bindings_resolved": False,
        "workdir_materialized": False,
        "workdir_created": False,
        "filesystem_action_performed": False,
        "directory_creation_implemented": False,
        "runtime_selection_preserved": True,
        "runtime_execution_authorized": False,
        "runtime_started": False,
        "process_spawn_implemented": False,
        "command_execution_performed": False,
        "execution_materialization_blockers": EXECUTION_MATERIALIZATION_BLOCKERS,
        "execution_materialization_source_blockers": EXECUTION_SOURCE_BLOCKERS,
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "dependencies": dependencies,
    }


def isolated_workdir_allocator_source_binding_review_contract() -> dict[str, Any]:
    review = isolated_workdir_allocator_source_binding_review()
    return {
        "schema": CONTRACT_SCHEMA,
        "allocator_git_blob": ISOLATED_WORKDIR_ALLOCATOR_GIT_BLOB,
        "allocator_source_sha256": ISOLATED_WORKDIR_ALLOCATOR_SOURCE_SHA256,
        "allocator_test_git_blob": ISOLATED_WORKDIR_ALLOCATOR_TEST_GIT_BLOB,
        "allocator_test_sha256": ISOLATED_WORKDIR_ALLOCATOR_TEST_SHA256,
        "allocator_source_identity_pinned_by_git_blob": True,
        "allocator_source_identity_pinned_by_sha256": True,
        "allocator_source_is_not_self_bound": True,
        "separate_review_instrument": True,
        "isolated_workdir_allocator_implemented": True,
        "isolated_workdir_allocator_source_binding_present": True,
        "isolated_workdir_allocator_reviewed": True,
        "allocation_receipts_validated": True,
        "allocation_receipt_count": 36,
        "matched_pair_count": 18,
        "baseline_allocation_count": 18,
        "candidate_allocation_count": 18,
        "runtime_control_count": 4,
        "unique_namespace_count": 36,
        "unique_path_template_count": 36,
        "unique_allocation_digest_count": 36,
        "workdir_root_token": EXPECTED_ROOT_TOKEN,
        "unresolved_root_token_preserved": True,
        "host_path_resolved": False,
        "filesystem_path_resolved": False,
        "path_bindings_resolved": False,
        "workdir_materialized": False,
        "workdir_created": False,
        "filesystem_action_performed": False,
        "directory_creation_implemented": False,
        "runtime_selection_preserved": True,
        "runtime_execution_authorized": False,
        "runtime_started": False,
        "process_spawn_implemented": False,
        "command_execution_performed": False,
        "review_live_observation_implemented": False,
        "review_filesystem_observation_implemented": False,
        "review_git_query_implemented": False,
        "review_subprocess_execution_implemented": False,
        "review_network_request_implemented": False,
        "review_ollama_request_implemented": False,
        "review_docker_command_implemented": False,
        "review_service_action_implemented": False,
        "review_model_load_implemented": False,
        "review_model_inference_implemented": False,
        "review_game_execution_implemented": False,
        "review_training_implemented": False,
        "review_weights_update_implemented": False,
        "review_deployment_implemented": False,
        "review_void_chain_mutation_implemented": False,
        "review_wallet_or_funds_action_implemented": False,
        "execution_materialization_blockers": EXECUTION_MATERIALIZATION_BLOCKERS,
        "execution_materialization_source_blockers": EXECUTION_SOURCE_BLOCKERS,
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "review": deepcopy(review),
    }


def advance_execution_materialization(*args: Any, **kwargs: Any) -> None:
    raise IsolatedWorkdirAllocatorSourceBindingReviewHold(NEXT_GATE)


def create_isolated_workdir(*args: Any, **kwargs: Any) -> None:
    raise IsolatedWorkdirAllocatorSourceBindingReviewHold(NEXT_GATE)


def execute_materialized_command(*args: Any, **kwargs: Any) -> None:
    raise IsolatedWorkdirAllocatorSourceBindingReviewHold(NEXT_GATE)


def start_runtime(*args: Any, **kwargs: Any) -> None:
    raise IsolatedWorkdirAllocatorSourceBindingReviewHold(NEXT_GATE)


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    raise IsolatedWorkdirAllocatorSourceBindingReviewHold(NEXT_GATE)
