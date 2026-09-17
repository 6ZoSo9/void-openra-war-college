"""Source-only review of the accepted Generation-2 cross-control runtime selector.

This separate instrument pins the accepted selector implementation by exact Git
blob and SHA-256, validates its deterministic four-control selection semantics,
and closes only the selector source-review frontier.

It does not start a runtime, materialize commands or workdirs, perform host or
network observation, launch OpenRA/models, train, deploy, mutate VOID, or move
funds. Runtime authority remains separate. Command materialization and isolated
workdir allocation remain the next source frontiers.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_cross_control_runtime_selector_generation2
    as selector,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_frozen_worktree_materializer_source_binding_review_generation2
    as materializer_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "cross-control-runtime-selector-source-binding-review-contract.v1"
)
REVIEW_SCHEMA = (
    "void.abaddon.generation2."
    "cross-control-runtime-selector-source-binding-review.v1"
)

SELECTOR_GIT_BLOB = "3ddf54f0fe8a37006d1e272bab62d14faa5904c0"
SELECTOR_SOURCE_SHA256 = (
    "19cd2c02e4232cee01e31286eee545237d61d7839542914899a1abf016fe26f4"
)
MATERIALIZER_REVIEW_GIT_BLOB = "3dcc325c431ec451a737b6e228c365ce1acb4f98"

EXPECTED_SELECTOR_INTERNAL_DEPENDENCY_BLOBS = {
    "execution_adapter_git_blob": "994d44d751c530619649322c72a65edf15f6a8c3",
    "runtime_realizations_git_blob": "0dbae61b0be96445e5fd6c23a07491a03f18b679",
    "materializer_review_git_blob": "3dcc325c431ec451a737b6e228c365ce1acb4f98",
    "orchestrator_git_blob": "8948b53d002e5d7e48a7aef2ec10ff5d690f5a1c",
}

RUNTIME_REALIZATION_SET_SHA256 = (
    "1dbb861a3bc03a4423187846a519f228726cc890f4452c3b1d8607614288a7d8"
)
OPPONENT_SNAPSHOT_SET_SHA256 = (
    "d7bfce0cb1456ec440f6ab362c781057837c3912c557f865ae95b7ddc6278526"
)

EXPECTED_RUNTIME_IDS = {
    "apollyon-v13-v14-promoted",
    "apollyon-v13-v10-promoted",
    "apollyon-v2r13-qualified-predecessor",
    "apollyon-v3-v8-accepted-model-control",
}

EXECUTION_MATERIALIZATION_BLOCKERS = tuple(selector.POST_SELECTOR_BLOCKERS)
EXECUTION_SOURCE_BLOCKERS = tuple(selector.POST_SELECTOR_SOURCE_BLOCKERS)

NEXT_GATE = "COMMAND_MATERIALIZER_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_command_materializer_implementation"


class CrossControlRuntimeSelectorSourceBindingReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise CrossControlRuntimeSelectorSourceBindingReviewHold(message)


def _validate_dependencies() -> dict[str, Any]:
    implementation = selector.cross_control_runtime_selector_contract()
    prior_review = (
        materializer_review
        .v2r13_frozen_worktree_materializer_source_binding_review_contract()
    )

    _require(
        implementation.get("cross_control_runtime_selector_implemented") is True,
        "cross-control runtime selector implementation missing",
    )
    _require(
        implementation.get("cross_control_runtime_selector_reviewed") is False,
        "cross-control runtime selector unexpectedly self-reviews",
    )
    _require(
        implementation.get("next_gate")
        == "CROSS_CONTROL_RUNTIME_SELECTOR_SOURCE_BINDING_REVIEW_REQUIRED",
        "selector source-binding review gate drift",
    )
    _require(
        implementation.get("next_change_class")
        == "source_only_cross_control_runtime_selector_source_binding_review",
        "selector source-binding review change class drift",
    )

    for field, expected_blob in EXPECTED_SELECTOR_INTERNAL_DEPENDENCY_BLOBS.items():
        _require(
            implementation.get(field) == expected_blob,
            f"selector internal dependency blob drift: {field}",
        )

    _require(
        implementation.get("runtime_realization_set_sha256")
        == RUNTIME_REALIZATION_SET_SHA256,
        "selector runtime realization-set digest drift",
    )
    _require(
        implementation.get("opponent_snapshot_set_sha256")
        == OPPONENT_SNAPSHOT_SET_SHA256,
        "selector opponent snapshot-set digest drift",
    )

    expected_true = (
        "runtime_class_is_not_selection_key",
        "selector_accepts_only_canonical_execution_descriptors",
        "selector_preserves_matched_pair_runtime_identity",
        "selector_removes_only_its_execution_blocker",
        "runtime_selection_source_only",
    )
    for field in expected_true:
        _require(
            implementation.get(field) is True,
            f"selector semantic field lost: {field}",
        )

    _require(
        implementation.get("selection_key") == "opponent_snapshot_id",
        "selector identity key drift",
    )
    _require(
        implementation.get("reviewed_runtime_count") == 4,
        "selector reviewed runtime count drift",
    )
    _require(
        implementation.get("reviewed_runtime_class_count") == 3,
        "selector reviewed runtime-class count drift",
    )
    _require(
        implementation.get("execution_descriptor_count") == 36,
        "selector execution descriptor count drift",
    )
    _require(
        implementation.get("matched_pair_count") == 18,
        "selector matched-pair count drift",
    )

    expected_false = (
        "runtime_selection_performed",
        "runtime_started",
        "command_materialized",
        "workdir_materialized",
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
            f"selector crossed source-only boundary: {field}",
        )

    _require(
        tuple(implementation.get("post_selector_blockers", ()))
        == EXECUTION_MATERIALIZATION_BLOCKERS,
        "selector post-selector blocker set drift",
    )
    _require(
        tuple(implementation.get("post_selector_source_blockers", ()))
        == EXECUTION_SOURCE_BLOCKERS,
        "selector post-selector source blocker set drift",
    )

    runtime_index = implementation.get("dependencies", {}).get("runtime_index")
    _require(isinstance(runtime_index, dict), "selector runtime index missing")
    _require(
        set(runtime_index) == EXPECTED_RUNTIME_IDS,
        "selector reviewed runtime identity set drift",
    )

    selected = selector.all_selected_execution_descriptors()
    _require(len(selected) == 36, "selected execution descriptor count drift")
    seen_runtime_ids: set[str] = set()
    pair_runtime_bindings: dict[int, str] = {}

    for row in selected:
        _require(
            row.get("eligible") is False,
            "selected execution descriptor unexpectedly eligible",
        )
        _require(
            tuple(row.get("reasons", ())) == EXECUTION_MATERIALIZATION_BLOCKERS,
            "selected execution descriptor blocker set drift",
        )
        _require(
            row.get("authority", {}).get("runtime_execution_authorized") is False,
            "selected descriptor unexpectedly authorizes runtime",
        )
        runtime = row.get("runtime")
        _require(isinstance(runtime, dict), "selected descriptor runtime missing")
        _require(
            runtime.get("cross_control_selector_implemented") is True,
            "selected descriptor lacks selector implementation",
        )
        _require(
            runtime.get("selection_performed") is True,
            "selected descriptor lacks deterministic source selection",
        )
        _require(
            runtime.get("started") is False,
            "selected descriptor unexpectedly starts runtime",
        )
        selection = runtime.get("selection")
        _require(isinstance(selection, dict), "selected runtime receipt missing")
        _require(
            selection.get("selection_is_source_only") is True,
            "selected runtime receipt not source-only",
        )
        _require(
            selection.get("runtime_started") is False,
            "selected runtime receipt starts runtime",
        )
        _require(
            selection.get("command_materialized") is False,
            "selected runtime receipt materializes command",
        )
        _require(
            selection.get("workdir_materialized") is False,
            "selected runtime receipt materializes workdir",
        )
        _require(
            selection.get("runtime_execution_authorized") is False,
            "selected runtime receipt authorizes execution",
        )

        snapshot_id = selection.get("opponent_snapshot_id")
        _require(
            snapshot_id in EXPECTED_RUNTIME_IDS,
            f"selected runtime identity drift: {snapshot_id!r}",
        )
        seen_runtime_ids.add(snapshot_id)

        pair_slot = row.get("pair_slot")
        runtime_sha = selection.get("runtime_realization_sha256")
        _require(
            type(pair_slot) is int and 1 <= pair_slot <= 18,
            "selected descriptor pair slot drift",
        )
        _require(
            isinstance(runtime_sha, str) and len(runtime_sha) == 64,
            "selected runtime realization digest malformed",
        )
        if pair_slot in pair_runtime_bindings:
            _require(
                pair_runtime_bindings[pair_slot] == runtime_sha,
                f"matched-pair runtime identity disagreement: {pair_slot}",
            )
        else:
            pair_runtime_bindings[pair_slot] = runtime_sha

    _require(
        seen_runtime_ids == EXPECTED_RUNTIME_IDS,
        "not all reviewed runtime controls selected",
    )
    _require(
        len(pair_runtime_bindings) == 18,
        "matched-pair selector binding count drift",
    )

    v14 = next(
        row["runtime"]["selection"]
        for row in selected
        if row["apollyon_opponent"]["snapshot_id"] == "apollyon-v13-v14-promoted"
    )
    v10 = next(
        row["runtime"]["selection"]
        for row in selected
        if row["apollyon_opponent"]["snapshot_id"] == "apollyon-v13-v10-promoted"
    )
    _require(
        v14["runtime_class"] == v10["runtime_class"],
        "expected V14/V10 shared runtime class drift",
    )
    _require(
        v14["selection_key"] != v10["selection_key"],
        "V14/V10 selector identities collapsed",
    )
    _require(
        v14["runtime_realization_sha256"] != v10["runtime_realization_sha256"],
        "V14/V10 realization identities collapsed",
    )

    _require(
        prior_review.get("activation_source_review_frontier_complete") is True,
        "historical activation source-review frontier drift",
    )
    _require(
        prior_review.get("runtime_authority_is_only_remaining_activation_gap")
        is True,
        "historical activation authority frontier drift",
    )
    _require(
        prior_review.get("runtime_execution_authorized") is False,
        "historical activation review unexpectedly authorizes runtime",
    )
    _require(
        prior_review.get("next_gate")
        == "CROSS_CONTROL_RUNTIME_SELECTOR_IMPLEMENTATION_REQUIRED",
        "historical source frontier was rewritten",
    )

    return {
        "selector_contract": deepcopy(implementation),
        "historical_materializer_review_contract": deepcopy(prior_review),
        "selected_execution_descriptors": deepcopy(selected),
    }


def cross_control_runtime_selector_source_binding_review() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    return {
        "schema": REVIEW_SCHEMA,
        "cross_control_runtime_selector_implemented": True,
        "cross_control_runtime_selector_source_binding_present": True,
        "cross_control_runtime_selector_reviewed": True,
        "selector_source_identity_pinned_by_git_blob": True,
        "selector_source_identity_pinned_by_sha256": True,
        "selection_key": "opponent_snapshot_id",
        "runtime_class_is_not_selection_key": True,
        "reviewed_runtime_count": 4,
        "reviewed_runtime_class_count": 3,
        "execution_descriptor_count": 36,
        "matched_pair_count": 18,
        "selector_accepts_only_canonical_execution_descriptors": True,
        "selector_preserves_matched_pair_runtime_identity": True,
        "selector_removes_only_its_execution_blocker": True,
        "runtime_selection_source_only": True,
        "runtime_selection_performed_by_review": False,
        "runtime_started": False,
        "runtime_execution_authorized": False,
        "command_materializer_implemented": False,
        "isolated_workdir_allocator_implemented": False,
        "execution_materialization_blockers": EXECUTION_MATERIALIZATION_BLOCKERS,
        "execution_materialization_source_blockers": EXECUTION_SOURCE_BLOCKERS,
        "execution_materialization_remains_open": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "dependencies": dependencies,
    }


def cross_control_runtime_selector_source_binding_review_contract() -> dict[str, Any]:
    review = cross_control_runtime_selector_source_binding_review()
    return {
        "schema": CONTRACT_SCHEMA,
        "selector_git_blob": SELECTOR_GIT_BLOB,
        "selector_source_sha256": SELECTOR_SOURCE_SHA256,
        "materializer_review_git_blob": MATERIALIZER_REVIEW_GIT_BLOB,
        "selector_source_identity_pinned_by_git_blob": True,
        "selector_source_identity_pinned_by_sha256": True,
        "selector_source_is_not_self_bound": True,
        "separate_review_instrument": True,
        "cross_control_runtime_selector_implemented": True,
        "cross_control_runtime_selector_source_binding_present": True,
        "cross_control_runtime_selector_reviewed": True,
        "selection_key": "opponent_snapshot_id",
        "runtime_class_is_not_selection_key": True,
        "reviewed_runtime_count": 4,
        "reviewed_runtime_class_count": 3,
        "execution_descriptor_count": 36,
        "matched_pair_count": 18,
        "selector_accepts_only_canonical_execution_descriptors": True,
        "selector_preserves_matched_pair_runtime_identity": True,
        "selector_removes_only_its_execution_blocker": True,
        "runtime_selection_source_only": True,
        "runtime_selection_performed_by_review": False,
        "runtime_started": False,
        "runtime_execution_authorized": False,
        "command_materializer_implemented": False,
        "isolated_workdir_allocator_implemented": False,
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
        "review_deployment_implemented": False,
        "review_void_chain_mutation_implemented": False,
        "review_wallet_or_funds_action_implemented": False,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "review": deepcopy(review),
    }


def materialize_command(*args: Any, **kwargs: Any) -> None:
    raise CrossControlRuntimeSelectorSourceBindingReviewHold(NEXT_GATE)


def allocate_isolated_workdir(*args: Any, **kwargs: Any) -> None:
    raise CrossControlRuntimeSelectorSourceBindingReviewHold(NEXT_GATE)


def advance_execution_materialization(*args: Any, **kwargs: Any) -> None:
    raise CrossControlRuntimeSelectorSourceBindingReviewHold(NEXT_GATE)


def start_runtime(*args: Any, **kwargs: Any) -> None:
    raise CrossControlRuntimeSelectorSourceBindingReviewHold(
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    raise CrossControlRuntimeSelectorSourceBindingReviewHold(
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED"
    )
