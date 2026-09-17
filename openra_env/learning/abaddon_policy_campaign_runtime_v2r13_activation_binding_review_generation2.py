"""Source-only review of the V2R13 runtime-activation binding frontier.

This instrument reconciles the historical activation contract with the later
accepted canonical live-collection evidence.  It records that the activation
binding and exact active-model digest observation are now reviewed, while
preserving the still-open frozen-worktree materializer and runtime-execution
authority boundaries.

It performs no live observation, filesystem observation, Git query, subprocess
execution, HTTP/Ollama/Docker request, service action, model load/inference,
game execution, training, deployment, VOID-chain mutation, or funds action.
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
    abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_invocation_acceptance_generation2
    as invocation_acceptance,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_ollama_observer_binding_generation2
    as ollama_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_worktree_observer_generation2
    as worktree_observer,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-activation-binding-review-contract.v1"
)
REVIEW_SCHEMA = (
    "void.abaddon.generation2.v2r13-activation-binding-review.v1"
)

ACTIVATION_CONTRACT_GIT_BLOB = "a3acb42280c334daa24a3b830105a04666fd603b"
ACTIVATION_CONTRACT_SOURCE_SHA256 = (
    "dc4c90175dee00f23ab28bc362cec41245a069345c0154d519215e3cb8150a3c"
)
INVOCATION_ACCEPTANCE_GIT_BLOB = "1ced66b86edbda59b33bdc25a185842d7bd71418"
INVOCATION_ACCEPTANCE_SOURCE_SHA256 = (
    "2a883510806ac6123c7e8bb6a2289f6d3d0dd501bb5aed0e738c435e7eda3045"
)
OLLAMA_BINDING_GIT_BLOB = "58364a1d5d71aead9df6dc0fc61661a557131508"
OLLAMA_BINDING_SOURCE_SHA256 = (
    "c6b0bb746d017326e600f401a2d07a29fba79aced401687c4eb5238084ee9335"
)
WORKTREE_OBSERVER_GIT_BLOB = "994f3be5d3344d6ac905c1f5fee9f9490fd4dd3f"
WORKTREE_OBSERVER_SOURCE_SHA256 = (
    "ad2544600833e3f88388e68df5e289a7f69b55f4e8c32f89e8899338e195aacf"
)
EXECUTION_ADAPTER_GIT_BLOB = "994d44d751c530619649322c72a65edf15f6a8c3"

HISTORICAL_ACTIVATION_BLOCKERS = (
    "V2R13_ACTIVATION_BINDING_NOT_REVIEWED",
    "V2R13_ACTIVE_MODEL_DIGEST_PROBE_NOT_REVIEWED",
    "V2R13_FROZEN_WORKTREE_MATERIALIZER_NOT_REVIEWED",
    activation_contract.RUNTIME_AUTHORITY_BLOCKER,
)
REMAINING_ACTIVATION_BLOCKERS = (
    "V2R13_FROZEN_WORKTREE_MATERIALIZER_NOT_REVIEWED",
    activation_contract.RUNTIME_AUTHORITY_BLOCKER,
)
EXECUTION_MATERIALIZATION_BLOCKERS = tuple(execution_adapter.EXECUTION_BLOCKERS)

NEXT_GATE = "V2R13_FROZEN_WORKTREE_MATERIALIZER_IMPLEMENTATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_frozen_worktree_materializer_implementation"


class RuntimeV2R13ActivationBindingReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13ActivationBindingReviewHold(message)


def _validate_dependencies() -> dict[str, Any]:
    activation = activation_contract.activation_descriptor(activation_contract.V2R13)
    accepted = (
        invocation_acceptance
        .v2r13_canonical_live_collection_invocation_acceptance_contract()
    )
    ollama = ollama_binding.v2r13_ollama_observer_binding_contract()
    worktree = worktree_observer.v2r13_worktree_observer_contract()

    _require(
        tuple(activation.get("blockers", ())) == HISTORICAL_ACTIVATION_BLOCKERS,
        "V2R13 historical activation blocker set drift",
    )
    _require(
        activation.get("runtime_specific_activation_binding_reviewed") is False,
        "historical activation contract unexpectedly rewrote activation review",
    )
    _require(
        activation.get("runtime_specific_identity_probe_reviewed") is False,
        "historical activation contract unexpectedly rewrote identity review",
    )
    _require(
        activation.get("portable_checkout", {}).get(
            "worktree_materialization_implemented"
        )
        is False,
        "historical activation contract unexpectedly implements worktree materialization",
    )
    _require(
        activation.get("activation_proven") is False,
        "historical activation contract unexpectedly proves activation",
    )
    _require(
        activation.get("eligible") is False,
        "historical activation descriptor unexpectedly eligible",
    )

    _require(
        accepted.get("canonical_live_collection_invocation_accepted") is True,
        "accepted canonical live invocation missing",
    )
    _require(
        accepted.get("provider_capability_complete") is True,
        "accepted provider capability incomplete",
    )
    _require(
        accepted.get("collector_identity_admitted") is True,
        "accepted collector identity missing",
    )
    _require(
        accepted.get("runtime_readiness_admitted") is True,
        "accepted runtime readiness missing",
    )
    _require(
        accepted.get("canonical_live_collection_path_complete") is True,
        "accepted canonical live collection path incomplete",
    )
    _require(
        accepted.get("canonical_collection_enabled") is False,
        "accepted invocation unexpectedly enables canonical collection",
    )
    _require(
        accepted.get("runtime_execution_authorized") is False,
        "accepted invocation unexpectedly authorizes runtime",
    )
    _require(
        accepted.get("next_gate")
        == "V2R13_ACTIVATION_BINDING_REVIEW_REQUIRED",
        "accepted invocation next-gate drift",
    )

    _require(
        ollama.get("canonical_observer_source_binding_present") is True,
        "canonical Ollama observer source binding missing",
    )
    _require(
        ollama.get("endpoint_liveness_provider_primitive_implemented") is True,
        "endpoint-liveness provider primitive missing",
    )
    _require(
        ollama.get("model_identity_provider_primitive_implemented") is True,
        "model-identity provider primitive missing",
    )
    _require(
        ollama.get("supported_primitive_count_after_binding") == 16,
        "V2R13 provider supported count drift",
    )
    _require(
        ollama.get("remaining_unresolved_primitive_count") == 0,
        "V2R13 provider unresolved count drift",
    )
    _require(
        ollama.get("all_v2r13_provider_primitives_implemented") is True,
        "V2R13 provider capability frontier incomplete",
    )
    _require(
        ollama.get("binding_live_observation_implemented") is False,
        "Ollama binding unexpectedly performs live observation",
    )
    _require(
        ollama.get("runtime_readiness_admitted") is False,
        "Ollama binding unexpectedly admits readiness itself",
    )
    _require(
        ollama.get("runtime_execution_authorized") is False,
        "Ollama binding unexpectedly authorizes runtime",
    )

    _require(
        worktree.get("six_path_classification_leaves_implemented") is True,
        "V2R13 worktree classification review missing",
    )
    _require(
        worktree.get("activation_worktree_shape_composition_implemented") is True,
        "V2R13 worktree activation shape composition missing",
    )
    _require(
        worktree.get("real_host_backend_implemented") is False,
        "V2R13 worktree observer unexpectedly has real host backend",
    )
    _require(
        worktree.get("automatic_host_backend_selection") is False,
        "V2R13 worktree observer unexpectedly auto-selects host backend",
    )
    _require(
        worktree.get("observation_performed") is False,
        "V2R13 worktree observer contract unexpectedly performs observation",
    )
    _require(
        worktree.get("runtime_execution_authorized") is False,
        "V2R13 worktree observer unexpectedly authorizes runtime",
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
            "V2R13 execution materialization blocker set drift",
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
        "historical_activation_descriptor": deepcopy(activation),
        "accepted_live_invocation_contract": deepcopy(accepted),
        "ollama_observer_binding_contract": deepcopy(ollama),
        "worktree_observer_contract": deepcopy(worktree),
        "v2r13_execution_descriptors": deepcopy(descriptors),
    }


def v2r13_activation_binding_review() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    return {
        "schema": REVIEW_SCHEMA,
        "snapshot_id": activation_contract.V2R13,
        "activation_binding_reviewed": True,
        "active_model_digest_probe_reviewed": True,
        "accepted_live_invocation_present": True,
        "accepted_live_invocation_count": 1,
        "provider_capability_complete": True,
        "provider_supported_primitive_count": 16,
        "provider_remaining_unresolved_primitive_count": 0,
        "frozen_worktree_observer_reviewed": True,
        "frozen_worktree_materializer_reviewed": False,
        "activation_proven": False,
        "runtime_activation_performed": False,
        "runtime_activation_path_complete": False,
        "canonical_collection_enabled": False,
        "runtime_execution_authorized": False,
        "execution_materialization_remains_open": True,
        "remaining_activation_blockers": REMAINING_ACTIVATION_BLOCKERS,
        "remaining_activation_blocker_count": len(
            REMAINING_ACTIVATION_BLOCKERS
        ),
        "execution_materialization_blockers": (
            EXECUTION_MATERIALIZATION_BLOCKERS
        ),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "dependencies": dependencies,
    }


def v2r13_activation_binding_review_contract() -> dict[str, Any]:
    review = v2r13_activation_binding_review()
    return {
        "schema": CONTRACT_SCHEMA,
        "snapshot_id": activation_contract.V2R13,
        "activation_contract_git_blob": ACTIVATION_CONTRACT_GIT_BLOB,
        "activation_contract_source_sha256": ACTIVATION_CONTRACT_SOURCE_SHA256,
        "invocation_acceptance_git_blob": INVOCATION_ACCEPTANCE_GIT_BLOB,
        "invocation_acceptance_source_sha256": (
            INVOCATION_ACCEPTANCE_SOURCE_SHA256
        ),
        "ollama_binding_git_blob": OLLAMA_BINDING_GIT_BLOB,
        "ollama_binding_source_sha256": OLLAMA_BINDING_SOURCE_SHA256,
        "worktree_observer_git_blob": WORKTREE_OBSERVER_GIT_BLOB,
        "worktree_observer_source_sha256": WORKTREE_OBSERVER_SOURCE_SHA256,
        "execution_adapter_git_blob": EXECUTION_ADAPTER_GIT_BLOB,
        "historical_activation_contract_retained": True,
        "historical_activation_blockers": HISTORICAL_ACTIVATION_BLOCKERS,
        "activation_binding_reviewed": True,
        "active_model_digest_probe_reviewed": True,
        "frozen_worktree_observer_reviewed": True,
        "frozen_worktree_materializer_reviewed": False,
        "remaining_activation_blockers": REMAINING_ACTIVATION_BLOCKERS,
        "remaining_activation_blocker_count": 2,
        "runtime_authority_is_not_only_remaining_gap": True,
        "activation_proven": False,
        "runtime_activation_performed": False,
        "runtime_activation_path_complete": False,
        "canonical_collection_enabled": False,
        "runtime_execution_authorized": False,
        "execution_materialization_blockers": (
            EXECUTION_MATERIALIZATION_BLOCKERS
        ),
        "execution_materialization_remains_open": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "live_observation_required_for_this_change": False,
        "filesystem_observation_required_for_this_change": False,
        "git_query_required_for_this_change": False,
        "runtime_action_required_for_this_change": False,
        "model_load_required_for_this_change": False,
        "model_inference_required_for_this_change": False,
        "game_execution_required_for_this_change": False,
        "training_required_for_this_change": False,
        "deployment_required_for_this_change": False,
        "void_chain_mutation_required_for_this_change": False,
        "funds_action_required_for_this_change": False,
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
        "review": deepcopy(review),
    }


def materialize_frozen_worktrees(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13ActivationBindingReviewHold(NEXT_GATE)


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13ActivationBindingReviewHold(
        activation_contract.RUNTIME_AUTHORITY_BLOCKER
    )
