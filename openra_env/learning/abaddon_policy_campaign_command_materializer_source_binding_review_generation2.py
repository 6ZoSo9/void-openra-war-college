"""Source-only review of the accepted Generation-2 command materializer.

This separate instrument pins the accepted command-materializer implementation
by exact Git blob and SHA-256, validates the deterministic 36-command / 18-pair
receipt topology and unresolved path-token bindings, and closes only the
command-materializer source-review frontier.

It does not resolve host paths, allocate or create workdirs, start runtimes,
spawn processes, execute commands, observe the host, train, deploy, mutate
VOID, or move funds. Runtime authority remains separate. Isolated workdir
allocation remains the next source frontier.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_command_materializer_generation2
    as command_materializer,
)
from openra_env.learning import (
    abaddon_policy_campaign_cross_control_runtime_selector_source_binding_review_generation2
    as selector_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "command-materializer-source-binding-review-contract.v1"
)
REVIEW_SCHEMA = (
    "void.abaddon.generation2."
    "command-materializer-source-binding-review.v1"
)

COMMAND_MATERIALIZER_GIT_BLOB = "4836360e0d284454f815a2a2e32078d2565e6dea"
COMMAND_MATERIALIZER_SOURCE_SHA256 = (
    "d02a23e7c0d3e4fc8a9c087e511a66d0d32f72b24e6702c62e9b886fb9dfee5d"
)
SELECTOR_REVIEW_GIT_BLOB = "63b10239738980873bb26fc4f238b5c3e982a33e"
SELECTOR_REVIEW_SOURCE_SHA256 = (
    "3a84514c668a5c40f76dd50349a1716e778dcd414f4c1a21d63a6435bfdde334"
)

EXPECTED_MATERIALIZER_INTERNAL_DEPENDENCY_BLOBS = {
    "selector_review_git_blob": "63b10239738980873bb26fc4f238b5c3e982a33e",
    "selector_git_blob": "3ddf54f0fe8a37006d1e272bab62d14faa5904c0",
    "execution_adapter_git_blob": "994d44d751c530619649322c72a65edf15f6a8c3",
    "orchestrator_git_blob": "8948b53d002e5d7e48a7aef2ec10ff5d690f5a1c",
    "campaign_plan_git_blob": "86c6feb3072f9d540dbd4f7ee6462addcbac54aa",
    "candidate_wrapper_git_blob": "61eaefee39ebd90df0ddd8c649d9f0f9b64b1776",
    "candidate_fixture_git_blob": "20091bff54edbb567127722fae81e5a5308737d2",
}

EXPECTED_RUNTIME_IDS = {
    "apollyon-v13-v14-promoted",
    "apollyon-v13-v10-promoted",
    "apollyon-v2r13-qualified-predecessor",
    "apollyon-v3-v8-accepted-model-control",
}

EXECUTION_MATERIALIZATION_BLOCKERS = tuple(
    command_materializer.POST_COMMAND_BLOCKERS
)
EXECUTION_SOURCE_BLOCKERS = tuple(
    command_materializer.POST_COMMAND_SOURCE_BLOCKERS
)

NEXT_GATE = "ISOLATED_WORKDIR_ALLOCATOR_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_isolated_workdir_allocator_implementation"


class CommandMaterializerSourceBindingReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise CommandMaterializerSourceBindingReviewHold(message)


def _validate_historical_selector_review_constants() -> dict[str, Any]:
    """Pin the accepted predecessor without rerunning its expensive census."""
    _require(
        selector_review.SELECTOR_GIT_BLOB
        == command_materializer.SELECTOR_GIT_BLOB,
        "historical selector-review selector blob drift",
    )
    _require(
        selector_review.SELECTOR_SOURCE_SHA256
        == command_materializer.SELECTOR_SOURCE_SHA256,
        "historical selector-review selector SHA drift",
    )
    _require(
        tuple(selector_review.EXECUTION_MATERIALIZATION_BLOCKERS)
        == tuple(command_materializer.PRE_COMMAND_BLOCKERS),
        "historical execution blocker frontier drift",
    )
    _require(
        tuple(selector_review.EXECUTION_SOURCE_BLOCKERS)
        == tuple(command_materializer.PRE_COMMAND_SOURCE_BLOCKERS),
        "historical source blocker frontier drift",
    )
    _require(
        selector_review.NEXT_GATE == "COMMAND_MATERIALIZER_IMPLEMENTATION_REQUIRED",
        "historical selector-review next gate drift",
    )
    _require(
        selector_review.NEXT_CHANGE_CLASS
        == "source_only_command_materializer_implementation",
        "historical selector-review next change class drift",
    )
    return {
        "selector_review_git_blob": SELECTOR_REVIEW_GIT_BLOB,
        "selector_review_source_sha256": SELECTOR_REVIEW_SOURCE_SHA256,
        "selector_review_frontier_preserved": True,
        "historical_runtime_execution_authorized": False,
        "historical_command_materializer_implemented": False,
        "historical_isolated_workdir_allocator_implemented": False,
    }


@lru_cache(maxsize=1)
def _validate_dependencies_cached() -> dict[str, Any]:
    implementation = command_materializer.command_materializer_contract()
    historical = _validate_historical_selector_review_constants()

    _require(
        implementation.get("command_materializer_implemented") is True,
        "command materializer implementation missing",
    )
    _require(
        implementation.get("command_materializer_reviewed") is False,
        "command materializer unexpectedly self-reviews",
    )
    _require(
        implementation.get("next_gate")
        == "COMMAND_MATERIALIZER_SOURCE_BINDING_REVIEW_REQUIRED",
        "command materializer source-binding review gate drift",
    )
    _require(
        implementation.get("next_change_class")
        == "source_only_command_materializer_source_binding_review",
        "command materializer source-binding review change class drift",
    )

    for field, expected_blob in EXPECTED_MATERIALIZER_INTERNAL_DEPENDENCY_BLOBS.items():
        _require(
            implementation.get(field) == expected_blob,
            f"command materializer internal dependency blob drift: {field}",
        )

    expected_true = (
        "source_only_command_materialization",
        "accepted_frontier_validated_by_constants",
        "accepted_ledger_built_once_per_process",
        "argv_template_materialized",
        "path_bindings_explicit",
        "runtime_selection_preserved",
    )
    for field in expected_true:
        _require(
            implementation.get(field) is True,
            f"command materializer semantic field lost: {field}",
        )

    expected_false = (
        "path_bindings_resolved",
        "isolated_workdir_allocator_implemented",
        "runtime_execution_authorized",
        "runtime_started",
        "process_spawn_implemented",
        "command_execution_performed",
        "shell_command_materialized",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    )
    for field in expected_false:
        _require(
            implementation.get(field) is False,
            f"command materializer crossed source-only boundary: {field}",
        )

    _require(
        implementation.get("execution_descriptor_count") == 36,
        "command materializer execution descriptor count drift",
    )
    _require(
        implementation.get("matched_pair_count") == 18,
        "command materializer matched-pair count drift",
    )
    _require(
        implementation.get("baseline_command_count") == 18,
        "command materializer baseline command count drift",
    )
    _require(
        implementation.get("candidate_command_count") == 18,
        "command materializer candidate command count drift",
    )
    _require(
        tuple(implementation.get("post_command_blockers", ()))
        == EXECUTION_MATERIALIZATION_BLOCKERS,
        "post-command execution blocker set drift",
    )
    _require(
        tuple(implementation.get("post_command_source_blockers", ()))
        == EXECUTION_SOURCE_BLOCKERS,
        "post-command source blocker set drift",
    )

    commands = command_materializer.all_materialized_commands()
    _require(len(commands) == 36, "materialized command count drift")

    execution_indices: set[int] = set()
    command_digests: set[str] = set()
    seen_runtime_ids: set[str] = set()
    pair_rows: dict[int, dict[str, dict[str, Any]]] = {}

    for row in commands:
        execution_index = row.get("execution_index")
        pair_slot = row.get("pair_slot")
        arm = row.get("arm")

        _require(
            type(execution_index) is int and 1 <= execution_index <= 36,
            "command execution index drift",
        )
        _require(execution_index not in execution_indices, "duplicate execution index")
        execution_indices.add(execution_index)

        _require(
            type(pair_slot) is int and 1 <= pair_slot <= 18,
            "command pair slot drift",
        )
        _require(arm in {"baseline", "candidate"}, "command arm drift")

        command_sha = row.get("command_sha256")
        _require(
            isinstance(command_sha, str) and len(command_sha) == 64,
            "command digest malformed",
        )
        _require(command_sha not in command_digests, "duplicate command digest")
        command_digests.add(command_sha)

        _require(
            row.get("argv_template_materialized") is True,
            "argv template is not materialized",
        )
        _require(
            row.get("argv_materialized") is True,
            "argv receipt is not materialized",
        )
        _require(
            row.get("argv_contains_unresolved_path_tokens") is True,
            "unresolved path-token boundary drift",
        )
        _require(
            row.get("path_bindings_resolved") is False,
            "command materializer unexpectedly resolves host paths",
        )
        _require(
            row.get("shell_command_materialized") is False,
            "shell command unexpectedly materialized",
        )
        _require(
            row.get("subprocess_invocation_materialized") is False,
            "subprocess invocation unexpectedly materialized",
        )
        _require(
            row.get("process_spawn_implemented") is False,
            "process spawn unexpectedly implemented",
        )
        _require(
            row.get("command_execution_performed") is False,
            "command unexpectedly executed",
        )
        _require(
            row.get("workdir_materialized") is False,
            "workdir unexpectedly materialized",
        )
        _require(
            row.get("workdir_created") is False,
            "workdir unexpectedly created",
        )
        _require(
            row.get("runtime_selection_preserved") is True,
            "runtime selection identity not preserved",
        )
        _require(
            row.get("runtime_selection_recomputed_by_selector") is False,
            "selector census unexpectedly recomputed",
        )
        _require(row.get("runtime_started") is False, "runtime unexpectedly started")
        _require(
            row.get("runtime_execution_authorized") is False,
            "runtime unexpectedly authorized",
        )
        _require(
            tuple(row.get("remaining_blockers", ()))
            == EXECUTION_MATERIALIZATION_BLOCKERS,
            "command execution blocker set drift",
        )
        _require(
            tuple(row.get("remaining_source_blockers", ()))
            == EXECUTION_SOURCE_BLOCKERS,
            "command source blocker set drift",
        )

        for field in (
            "model_load_performed",
            "model_inference_performed",
            "game_execution_performed",
            "training_performed",
            "weights_updated",
            "deployment_performed",
            "void_chain_mutation_performed",
            "wallet_or_funds_action_performed",
        ):
            _require(
                row.get(field) is False,
                f"command crossed operational boundary: {field}",
            )

        snapshot_id = row.get("opponent_snapshot_id")
        _require(
            snapshot_id in EXPECTED_RUNTIME_IDS,
            f"runtime control identity drift: {snapshot_id!r}",
        )
        seen_runtime_ids.add(snapshot_id)

        path_bindings = row.get("path_bindings")
        _require(isinstance(path_bindings, dict), "command path bindings missing")
        if arm == "baseline":
            _require(
                set(path_bindings) == {"legacy_runner"},
                "baseline path binding set drift",
            )
            legacy = path_bindings["legacy_runner"]
            _require(
                legacy.get("token") == command_materializer.LEGACY_RUNNER_TOKEN,
                "baseline runner token drift",
            )
            _require(legacy.get("path_resolved") is False, "baseline path resolved")
            _require(legacy.get("used_in_argv") is True, "baseline runner not in argv")
            _require(
                legacy.get("sha256") == command_materializer.LEGACY_RUNNER_SHA256,
                "baseline runner SHA drift",
            )
        else:
            _require(
                set(path_bindings)
                == {
                    "candidate_wrapper",
                    "candidate_genome",
                    "candidate_wrapper_legacy_runner_dependency",
                },
                "candidate path binding set drift",
            )
            wrapper = path_bindings["candidate_wrapper"]
            genome = path_bindings["candidate_genome"]
            legacy = path_bindings["candidate_wrapper_legacy_runner_dependency"]
            _require(
                wrapper.get("git_blob")
                == command_materializer.CANDIDATE_WRAPPER_GIT_BLOB,
                "candidate wrapper blob drift",
            )
            _require(
                wrapper.get("sha256")
                == command_materializer.CANDIDATE_WRAPPER_SOURCE_SHA256,
                "candidate wrapper SHA drift",
            )
            _require(wrapper.get("path_resolved") is False, "wrapper path resolved")
            _require(wrapper.get("used_in_argv") is True, "wrapper missing from argv")
            _require(
                genome.get("git_blob")
                == command_materializer.CANDIDATE_FIXTURE_GIT_BLOB,
                "candidate genome blob drift",
            )
            _require(
                genome.get("sha256")
                == command_materializer.CANDIDATE_FIXTURE_SHA256,
                "candidate genome file SHA drift",
            )
            _require(
                genome.get("semantic_genome_sha256")
                == command_materializer.CANDIDATE_GENOME_SHA256,
                "candidate genome semantic SHA drift",
            )
            _require(genome.get("path_resolved") is False, "genome path resolved")
            _require(genome.get("used_in_argv") is True, "genome missing from argv")
            _require(
                legacy.get("sha256") == command_materializer.LEGACY_RUNNER_SHA256,
                "candidate wrapper legacy-runner dependency drift",
            )
            _require(
                legacy.get("consumer")
                == "candidate_wrapper_internal_exact_dependency",
                "candidate wrapper legacy-runner consumer drift",
            )
            _require(
                legacy.get("used_in_argv") is False,
                "candidate internal legacy runner leaked into outer argv",
            )

        pair_rows.setdefault(pair_slot, {})[str(arm)] = row

    _require(
        execution_indices == set(range(1, 37)),
        "execution index topology drift",
    )
    _require(
        seen_runtime_ids == EXPECTED_RUNTIME_IDS,
        "not all reviewed runtime controls remain represented",
    )
    _require(len(pair_rows) == 18, "matched-pair map count drift")

    for pair_slot, pair in pair_rows.items():
        _require(
            set(pair) == {"baseline", "candidate"},
            f"matched-pair arm set drift: {pair_slot}",
        )
        baseline = pair["baseline"]
        candidate = pair["candidate"]
        _require(
            tuple(baseline["runner_argv"]) == tuple(candidate["runner_argv"]),
            f"matched-pair runner argv disagreement: {pair_slot}",
        )
        _require(
            baseline["runtime_selection_key"]
            == candidate["runtime_selection_key"],
            f"matched-pair runtime key disagreement: {pair_slot}",
        )
        _require(
            baseline["runtime_realization_sha256"]
            == candidate["runtime_realization_sha256"],
            f"matched-pair runtime realization disagreement: {pair_slot}",
        )

    return {
        "command_materializer_contract": deepcopy(implementation),
        "historical_selector_review": deepcopy(historical),
        "materialized_commands": deepcopy(commands),
    }


def _validate_dependencies() -> dict[str, Any]:
    return deepcopy(_validate_dependencies_cached())


def command_materializer_source_binding_review() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    return {
        "schema": REVIEW_SCHEMA,
        "command_materializer_implemented": True,
        "command_materializer_source_binding_present": True,
        "command_materializer_reviewed": True,
        "materializer_source_identity_pinned_by_git_blob": True,
        "materializer_source_identity_pinned_by_sha256": True,
        "source_command_receipts_validated": True,
        "execution_descriptor_count": 36,
        "matched_pair_count": 18,
        "baseline_command_count": 18,
        "candidate_command_count": 18,
        "runtime_control_count": 4,
        "command_materializer_removes_only_its_execution_blocker": True,
        "source_only_command_materialization": True,
        "path_bindings_explicit": True,
        "path_bindings_resolved": False,
        "isolated_workdir_allocator_implemented": False,
        "runtime_selection_preserved": True,
        "runtime_execution_authorized": False,
        "runtime_started": False,
        "process_spawn_implemented": False,
        "command_execution_performed": False,
        "execution_materialization_blockers": EXECUTION_MATERIALIZATION_BLOCKERS,
        "execution_materialization_source_blockers": EXECUTION_SOURCE_BLOCKERS,
        "execution_materialization_remains_open": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "dependencies": dependencies,
    }


def command_materializer_source_binding_review_contract() -> dict[str, Any]:
    review = command_materializer_source_binding_review()
    return {
        "schema": CONTRACT_SCHEMA,
        "command_materializer_git_blob": COMMAND_MATERIALIZER_GIT_BLOB,
        "command_materializer_source_sha256": COMMAND_MATERIALIZER_SOURCE_SHA256,
        "selector_review_git_blob": SELECTOR_REVIEW_GIT_BLOB,
        "selector_review_source_sha256": SELECTOR_REVIEW_SOURCE_SHA256,
        "materializer_source_identity_pinned_by_git_blob": True,
        "materializer_source_identity_pinned_by_sha256": True,
        "materializer_source_is_not_self_bound": True,
        "separate_review_instrument": True,
        "command_materializer_implemented": True,
        "command_materializer_source_binding_present": True,
        "command_materializer_reviewed": True,
        "source_command_receipts_validated": True,
        "execution_descriptor_count": 36,
        "matched_pair_count": 18,
        "baseline_command_count": 18,
        "candidate_command_count": 18,
        "runtime_control_count": 4,
        "command_materializer_removes_only_its_execution_blocker": True,
        "source_only_command_materialization": True,
        "path_bindings_explicit": True,
        "path_bindings_resolved": False,
        "isolated_workdir_allocator_implemented": False,
        "runtime_selection_preserved": True,
        "runtime_execution_authorized": False,
        "runtime_started": False,
        "process_spawn_implemented": False,
        "command_execution_performed": False,
        "execution_materialization_blockers": EXECUTION_MATERIALIZATION_BLOCKERS,
        "execution_materialization_source_blockers": EXECUTION_SOURCE_BLOCKERS,
        "execution_materialization_remains_open": True,
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
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "review": deepcopy(review),
    }


def allocate_isolated_workdir(*args: Any, **kwargs: Any) -> None:
    raise CommandMaterializerSourceBindingReviewHold(NEXT_GATE)


def advance_execution_materialization(*args: Any, **kwargs: Any) -> None:
    raise CommandMaterializerSourceBindingReviewHold(NEXT_GATE)


def execute_materialized_command(*args: Any, **kwargs: Any) -> None:
    raise CommandMaterializerSourceBindingReviewHold(
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def start_runtime(*args: Any, **kwargs: Any) -> None:
    raise CommandMaterializerSourceBindingReviewHold(
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    raise CommandMaterializerSourceBindingReviewHold(
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED"
    )
