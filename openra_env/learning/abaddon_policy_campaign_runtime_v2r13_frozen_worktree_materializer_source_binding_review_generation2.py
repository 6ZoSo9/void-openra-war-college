"""Source-only review of the accepted V2R13 frozen-worktree materializer binding.

This separate instrument pins the accepted materializer implementation by exact
Git blob and SHA-256, validates its reviewed safety/authority surface, and closes
only the source-review side of the historical activation blocker.

It does not invoke materialization or cleanup and does not perform filesystem or
Git observation, subprocess execution, network/Ollama/Docker requests, service
actions, model load/inference, game/runtime execution, training, deployment,
VOID-chain mutation, or wallet/funds actions.

After this review, runtime authority is the only remaining V2R13 activation
blocker. Execution materialization remains separately open at the existing
cross-control selector, command materializer, and isolated-workdir frontiers.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_execution_adapter_generation2 as execution_adapter,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_activation_contract_generation2
    as activation_contract,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_activation_binding_review_generation2
    as activation_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_frozen_worktree_materializer_generation2
    as materializer,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-frozen-worktree-materializer-source-binding-review-contract.v1"
)
REVIEW_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-frozen-worktree-materializer-source-binding-review.v1"
)

MATERIALIZER_GIT_BLOB = "8c6fb13480e03f094f63fdb753ec19a0ce223c80"
MATERIALIZER_SOURCE_SHA256 = (
    "e1c189775b9b09d043f9e49d143d9f4ecab253ba5ea293fdf69820d0d2d86ff3"
)
ACTIVATION_REVIEW_GIT_BLOB = "9449b871cb745b67a7aa29f0d73de378f119a488"
ACTIVATION_REVIEW_SOURCE_SHA256 = (
    "7785cae74baeb5c4a1bfb541b95037019efc6e75134ffc58db4ffbdee041515f"
)
EXECUTION_ADAPTER_GIT_BLOB = "994d44d751c530619649322c72a65edf15f6a8c3"
ACTIVATION_CONTRACT_GIT_BLOB = "a3acb42280c334daa24a3b830105a04666fd603b"

MATERIALIZER_INTERNAL_DEPENDENCY_BLOBS = {
    "activation_review": "9449b871cb745b67a7aa29f0d73de378f119a488",
    "portable_checkout": "077fbf5a2847d85113eb8fcba3904b02343ebfef",
    "path_inputs": "f65735c7820da9da0205388f1933b6aa9d6dd737",
    "worktree_observer": "994f3be5d3344d6ac905c1f5fee9f9490fd4dd3f",
}

HISTORICAL_REMAINING_ACTIVATION_BLOCKERS = (
    "V2R13_FROZEN_WORKTREE_MATERIALIZER_NOT_REVIEWED",
    activation_contract.RUNTIME_AUTHORITY_BLOCKER,
)
REMAINING_ACTIVATION_BLOCKERS = (
    activation_contract.RUNTIME_AUTHORITY_BLOCKER,
)
EXECUTION_MATERIALIZATION_BLOCKERS = tuple(execution_adapter.EXECUTION_BLOCKERS)
EXECUTION_SOURCE_BLOCKERS = tuple(
    blocker
    for blocker in EXECUTION_MATERIALIZATION_BLOCKERS
    if blocker != activation_contract.RUNTIME_AUTHORITY_BLOCKER
)

NEXT_GATE = "CROSS_CONTROL_RUNTIME_SELECTOR_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_cross_control_runtime_selector_implementation"


class RuntimeV2R13FrozenWorktreeMaterializerSourceBindingReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13FrozenWorktreeMaterializerSourceBindingReviewHold(
            message
        )


def _validate_dependencies() -> dict[str, Any]:
    implementation = materializer.v2r13_frozen_worktree_materializer_contract()
    prior_review = activation_review.v2r13_activation_binding_review_contract()

    _require(
        implementation.get("frozen_worktree_materializer_implemented") is True,
        "V2R13 frozen-worktree materializer implementation missing",
    )
    _require(
        implementation.get("frozen_worktree_materializer_reviewed") is False,
        "V2R13 materializer unexpectedly self-reviews",
    )
    _require(
        implementation.get("next_gate")
        == "V2R13_FROZEN_WORKTREE_MATERIALIZER_SOURCE_BINDING_REVIEW_REQUIRED",
        "V2R13 materializer source-review gate drift",
    )
    _require(
        implementation.get("next_change_class")
        == "source_only_frozen_worktree_materializer_source_binding_review",
        "V2R13 materializer source-review change class drift",
    )

    expected_true = (
        "source_worktree_add_detached_implemented",
        "engine_worktree_add_detached_implemented",
        "destination_absence_preflight_implemented",
        "canonical_repository_snapshot_guard_implemented",
        "frozen_source_tree_verification_implemented",
        "materialized_commit_verification_implemented",
        "materialized_cleanliness_verification_implemented",
        "materialized_detached_head_verification_implemented",
        "partial_failure_rollback_implemented",
        "cleanup_implemented",
        "cleanup_idempotent",
        "cleanup_receipt_path_binding_implemented",
        "cleanup_registry_ownership_revalidation_implemented",
        "cleanup_commit_tree_clean_detached_revalidation_implemented",
        "cleanup_all_targets_preflight_before_removal_implemented",
        "cleanup_non_force_removal_implemented",
        "materialization_requires_explicit_authority",
        "cleanup_requires_explicit_authority",
        "git_runner_backend_injected",
        "path_exists_backend_injected",
    )
    for field in expected_true:
        _require(
            implementation.get(field) is True,
            f"V2R13 materializer safety/authority field lost: {field}",
        )

    expected_false = (
        "automatic_host_backend_selection",
        "real_subprocess_backend_implemented",
        "real_filesystem_backend_implemented",
        "materialization_performed",
        "cleanup_performed",
        "filesystem_mutation_performed",
        "git_worktree_admin_mutation_performed",
        "canonical_checkout_working_tree_mutation_performed",
        "activation_proven",
        "runtime_activation_performed",
        "runtime_execution_authorized",
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
            f"V2R13 materializer crossed source-only boundary: {field}",
        )

    _require(
        implementation.get("activation_review_git_blob")
        == MATERIALIZER_INTERNAL_DEPENDENCY_BLOBS["activation_review"],
        "V2R13 materializer activation-review dependency drift",
    )
    _require(
        implementation.get("portable_checkout_git_blob")
        == MATERIALIZER_INTERNAL_DEPENDENCY_BLOBS["portable_checkout"],
        "V2R13 materializer portable-checkout dependency drift",
    )
    _require(
        implementation.get("path_inputs_git_blob")
        == MATERIALIZER_INTERNAL_DEPENDENCY_BLOBS["path_inputs"],
        "V2R13 materializer path-input dependency drift",
    )
    _require(
        implementation.get("worktree_observer_git_blob")
        == MATERIALIZER_INTERNAL_DEPENDENCY_BLOBS["worktree_observer"],
        "V2R13 materializer worktree-observer dependency drift",
    )

    _require(
        tuple(prior_review.get("remaining_activation_blockers", ()))
        == HISTORICAL_REMAINING_ACTIVATION_BLOCKERS,
        "V2R13 historical remaining activation blocker set drift",
    )
    _require(
        prior_review.get("frozen_worktree_materializer_reviewed") is False,
        "historical activation review unexpectedly rewrote materializer review",
    )
    _require(
        prior_review.get("runtime_execution_authorized") is False,
        "historical activation review unexpectedly authorizes runtime",
    )
    _require(
        prior_review.get("execution_materialization_remains_open") is True,
        "historical activation review unexpectedly closes execution materialization",
    )
    _require(
        tuple(prior_review.get("execution_materialization_blockers", ()))
        == EXECUTION_MATERIALIZATION_BLOCKERS,
        "V2R13 execution materialization blocker set drift",
    )

    descriptors = [
        row
        for row in execution_adapter.all_execution_descriptors()
        if row.get("apollyon_opponent", {}).get("snapshot_id")
        == activation_contract.V2R13
    ]
    _require(len(descriptors) == 6, "V2R13 execution descriptor count drift")
    for row in descriptors:
        _require(
            tuple(row.get("reasons", ())) == EXECUTION_MATERIALIZATION_BLOCKERS,
            "V2R13 execution descriptor blocker set drift",
        )
        _require(
            row.get("eligible") is False,
            "V2R13 execution descriptor unexpectedly eligible",
        )
        _require(
            row.get("authority", {}).get("runtime_execution_authorized") is False,
            "V2R13 execution descriptor unexpectedly authorizes runtime",
        )

    return {
        "materializer_contract": deepcopy(implementation),
        "historical_activation_review_contract": deepcopy(prior_review),
        "v2r13_execution_descriptors": deepcopy(descriptors),
    }


def v2r13_frozen_worktree_materializer_source_binding_review() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    return {
        "schema": REVIEW_SCHEMA,
        "snapshot_id": activation_contract.V2R13,
        "frozen_worktree_materializer_implemented": True,
        "frozen_worktree_materializer_source_binding_present": True,
        "frozen_worktree_materializer_reviewed": True,
        "materializer_source_identity_pinned_by_git_blob": True,
        "materializer_source_identity_pinned_by_sha256": True,
        "materialization_requires_explicit_authority": True,
        "cleanup_requires_explicit_authority": True,
        "materializer_host_backend_bundled": False,
        "materializer_automatic_host_backend_selection": False,
        "materialization_performed_by_review": False,
        "cleanup_performed_by_review": False,
        "activation_binding_reviewed": True,
        "active_model_digest_probe_reviewed": True,
        "frozen_worktree_observer_reviewed": True,
        "remaining_activation_blockers": REMAINING_ACTIVATION_BLOCKERS,
        "remaining_activation_blocker_count": 1,
        "runtime_authority_is_only_remaining_activation_gap": True,
        "activation_source_review_frontier_complete": True,
        "activation_proven": False,
        "runtime_activation_performed": False,
        "runtime_activation_path_complete": False,
        "runtime_execution_authorized": False,
        "execution_materialization_blockers": EXECUTION_MATERIALIZATION_BLOCKERS,
        "execution_materialization_source_blockers": EXECUTION_SOURCE_BLOCKERS,
        "execution_materialization_remains_open": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "dependencies": dependencies,
    }


def v2r13_frozen_worktree_materializer_source_binding_review_contract() -> dict[str, Any]:
    review = v2r13_frozen_worktree_materializer_source_binding_review()
    return {
        "schema": CONTRACT_SCHEMA,
        "snapshot_id": activation_contract.V2R13,
        "materializer_git_blob": MATERIALIZER_GIT_BLOB,
        "materializer_source_sha256": MATERIALIZER_SOURCE_SHA256,
        "activation_review_git_blob": ACTIVATION_REVIEW_GIT_BLOB,
        "activation_review_source_sha256": ACTIVATION_REVIEW_SOURCE_SHA256,
        "execution_adapter_git_blob": EXECUTION_ADAPTER_GIT_BLOB,
        "activation_contract_git_blob": ACTIVATION_CONTRACT_GIT_BLOB,
        "materializer_source_identity_pinned_by_git_blob": True,
        "materializer_source_identity_pinned_by_sha256": True,
        "materializer_source_is_not_self_bound": True,
        "separate_review_instrument": True,
        "frozen_worktree_materializer_implemented": True,
        "frozen_worktree_materializer_source_binding_present": True,
        "frozen_worktree_materializer_reviewed": True,
        "materialization_requires_explicit_authority": True,
        "cleanup_requires_explicit_authority": True,
        "materializer_host_backend_bundled": False,
        "materializer_automatic_host_backend_selection": False,
        "remaining_activation_blockers": REMAINING_ACTIVATION_BLOCKERS,
        "remaining_activation_blocker_count": 1,
        "runtime_authority_is_only_remaining_activation_gap": True,
        "activation_source_review_frontier_complete": True,
        "activation_proven": False,
        "runtime_activation_performed": False,
        "runtime_activation_path_complete": False,
        "runtime_execution_authorized": False,
        "execution_materialization_blockers": EXECUTION_MATERIALIZATION_BLOCKERS,
        "execution_materialization_source_blockers": EXECUTION_SOURCE_BLOCKERS,
        "execution_materialization_remains_open": True,
        "review_materializer_invocation_implemented": False,
        "review_cleanup_invocation_implemented": False,
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
        "review_deployment_implemented": False,
        "review_void_chain_mutation_implemented": False,
        "review_wallet_or_funds_action_implemented": False,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "review": deepcopy(review),
    }


def materialize_frozen_worktrees(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13FrozenWorktreeMaterializerSourceBindingReviewHold(
        "GENERATION2_V2R13_FROZEN_WORKTREE_MATERIALIZATION_NOT_AUTHORIZED"
    )


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13FrozenWorktreeMaterializerSourceBindingReviewHold(
        activation_contract.RUNTIME_AUTHORITY_BLOCKER
    )


def advance_execution_materialization(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13FrozenWorktreeMaterializerSourceBindingReviewHold(
        NEXT_GATE
    )
