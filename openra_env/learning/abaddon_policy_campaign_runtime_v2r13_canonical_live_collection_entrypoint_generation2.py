"""Explicit-authority V2R13 canonical live-collection entrypoint candidate.

This source composes the already-reviewed, source-bound canonical live-collection
adapter lane into one explicit entrypoint.  The entrypoint never chooses host
backends automatically.  A caller must explicitly authorize collection and
observation, supply the HTTP and Docker metadata backends, and supply the already
produced worktree receipt and portable-binding attestation.

The entrypoint invokes the reviewed adapter, then validates the returned adapter
candidate through the separately reviewed adapter source binding.  The resulting
receipt proves the full 16-primitive collection/readiness lane while preserving
all runtime-action boundaries.

This entrypoint implementation is not self-bound.  Canonical collection remains
disabled until a separate source-binding instrument reviews and pins this file.
Runtime execution remains independently closed.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_adapter_binding_generation2
    as adapter_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_adapter_generation2
    as adapter,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    RUNTIME_AUTHORITY_BLOCKER,
    V2R13,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-canonical-live-collection-entrypoint-contract.v1"
)
RECEIPT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-canonical-live-collection-entrypoint-receipt.v1"
)

ADAPTER_BINDING_GIT_BLOB = "4945f98a5dc12cff282c767013f81cac091e32e8"
ADAPTER_BINDING_SOURCE_SHA256 = (
    "55d85737e0c0ee55199505b20e5628e8e6f7cc171dba9210cd67c753ec03458c"
)
ADAPTER_GIT_BLOB = "29c4bfa11a841359b6c4f4083659c78c474d94ba"
ADAPTER_SOURCE_SHA256 = (
    "a4236e3c727fcf6eee915ee9e3b44d2ba2e2666e8ac52499c9b342fd71935afb"
)

NEXT_GATE = "V2R13_CANONICAL_LIVE_COLLECTION_ENTRYPOINT_SOURCE_BINDING_REQUIRED"


class RuntimeV2R13CanonicalLiveCollectionEntrypointHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13CanonicalLiveCollectionEntrypointHold(message)


def _validate_dependencies() -> dict[str, Any]:
    binding = (
        adapter_binding
        .v2r13_canonical_live_collection_adapter_binding_contract()
    )
    adapter_contract = adapter.v2r13_canonical_live_collection_adapter_contract()

    _require(
        binding.get("canonical_live_collection_adapter_source_binding_present")
        is True,
        "V2R13 canonical adapter source binding missing",
    )
    _require(
        binding.get("supplied_bound_adapter_candidate_validator_implemented")
        is True,
        "V2R13 bound adapter candidate validator missing",
    )
    _require(
        binding.get("adapter_collection_requires_explicit_authority") is True,
        "V2R13 adapter collection authority requirement lost",
    )
    _require(
        binding.get("adapter_observation_requires_explicit_authority") is True,
        "V2R13 adapter observation authority requirement lost",
    )
    _require(
        binding.get("explicit_http_backend_injection_required") is True,
        "V2R13 adapter HTTP backend injection requirement lost",
    )
    _require(
        binding.get("explicit_docker_command_backend_injection_required") is True,
        "V2R13 adapter Docker backend injection requirement lost",
    )
    _require(
        binding.get("automatic_host_backend_selection") is False,
        "V2R13 adapter binding automatic host selection enabled",
    )
    _require(
        binding.get("provider_capability_supported_primitive_count") == 16,
        "V2R13 provider supported primitive count drift",
    )
    _require(
        binding.get("provider_capability_remaining_unresolved_primitive_count") == 0,
        "V2R13 provider unresolved primitive count drift",
    )
    _require(
        binding.get("bound_candidate_collector_identity_admission_implemented")
        is True,
        "V2R13 collector identity admission binding missing",
    )
    _require(
        binding.get("bound_candidate_runtime_readiness_admission_implemented")
        is True,
        "V2R13 runtime readiness admission binding missing",
    )
    _require(
        binding.get("canonical_live_collection_path_complete") is False,
        "V2R13 canonical path unexpectedly complete before entrypoint",
    )
    _require(
        binding.get("canonical_collection_enabled") is False,
        "V2R13 canonical collection unexpectedly enabled before entrypoint",
    )
    _require(
        binding.get("runtime_execution_authorized") is False,
        "V2R13 adapter binding unexpectedly authorizes runtime execution",
    )
    _require(
        binding.get("next_gate")
        == "V2R13_CANONICAL_LIVE_COLLECTION_ENTRYPOINT_REQUIRED",
        "V2R13 adapter binding entrypoint gate drift",
    )

    _require(
        adapter_contract.get(
            "canonical_live_collection_adapter_implementation_present"
        )
        is True,
        "V2R13 canonical adapter implementation missing",
    )
    _require(
        adapter_contract.get("automatic_host_backend_selection") is False,
        "V2R13 canonical adapter automatic host selection enabled",
    )
    _require(
        adapter_contract.get("runtime_execution_authorized") is False,
        "V2R13 canonical adapter unexpectedly authorizes runtime execution",
    )

    return {
        "adapter_binding": deepcopy(binding),
        "adapter": deepcopy(adapter_contract),
    }


def collect_v2r13_canonical_live_collection(
    *,
    collection_authorized: bool,
    observation_authorized: bool,
    http_get: Any,
    run_command: Any,
    worktree_receipt: Mapping[str, Any],
    portable_binding_attestation: Mapping[str, Any],
) -> dict[str, Any]:
    """Collect and validate one V2R13 canonical live-collection candidate."""
    _require(
        collection_authorized is True,
        "GENERATION2_V2R13_CANONICAL_COLLECTION_NOT_AUTHORIZED",
    )
    _require(
        observation_authorized is True,
        "GENERATION2_V2R13_CANONICAL_OBSERVATION_NOT_AUTHORIZED",
    )
    _require(callable(http_get), "explicit V2R13 HTTP GET backend required")
    _require(callable(run_command), "explicit V2R13 Docker command backend required")
    _require(
        isinstance(worktree_receipt, Mapping),
        "supplied V2R13 worktree receipt required",
    )
    _require(
        isinstance(portable_binding_attestation, Mapping),
        "supplied V2R13 portable-binding attestation required",
    )

    dependencies = _validate_dependencies()

    candidate = adapter.collect_v2r13_live_collection_adapter_candidate(
        collection_authorized=True,
        observation_authorized=True,
        http_get=http_get,
        run_command=run_command,
        worktree_receipt=worktree_receipt,
        portable_binding_attestation=portable_binding_attestation,
    )
    validation = (
        adapter_binding
        .validate_bound_canonical_live_collection_adapter_candidate(
            candidate,
            adapter_source_sha256=ADAPTER_SOURCE_SHA256,
        )
    )

    _require(
        validation.get("bound_adapter_candidate_valid") is True,
        "V2R13 canonical adapter candidate not valid",
    )
    _require(
        validation.get(
            "canonical_live_collection_adapter_source_binding_present"
        )
        is True,
        "V2R13 canonical adapter source binding not verified",
    )
    _require(
        validation.get("provider_capability_supported_primitive_count") == 16,
        "V2R13 canonical entrypoint provider count drift",
    )
    _require(
        validation.get("provider_capability_remaining_unresolved_primitive_count")
        == 0,
        "V2R13 canonical entrypoint unresolved primitive count drift",
    )
    _require(
        validation.get("collector_identity_admitted") is True,
        "V2R13 canonical entrypoint collector identity not admitted",
    )
    _require(
        validation.get("runtime_readiness_admitted") is True,
        "V2R13 canonical entrypoint runtime readiness not admitted",
    )
    _require(
        validation.get("runtime_execution_authorized") is False,
        "V2R13 canonical entrypoint unexpectedly authorizes runtime execution",
    )

    return {
        "schema": RECEIPT_SCHEMA,
        "snapshot_id": V2R13,
        "collection_authorized": True,
        "observation_authorized": True,
        "explicit_http_backend_supplied": True,
        "explicit_docker_command_backend_supplied": True,
        "supplied_worktree_receipt_present": True,
        "supplied_portable_binding_attestation_present": True,
        "automatic_host_backend_selection": False,
        "entrypoint_invocation_performed": True,
        "adapter_invocation_performed": True,
        "adapter_binding_validation_performed": True,
        "live_observation_performed": True,
        "ollama_tags_request_performed": True,
        "ollama_ps_request_performed": True,
        "chat_completions_request_performed": False,
        "docker_metadata_command_count": 3,
        "docker_mutating_command_performed": False,
        "worktree_observation_performed_by_entrypoint": False,
        "portable_binding_install_performed_by_entrypoint": False,
        "provider_capability_supported_primitive_count": 16,
        "provider_capability_remaining_unresolved_primitive_count": 0,
        "provider_capability_complete": True,
        "collector_identity_admitted": True,
        "runtime_readiness_admitted": True,
        "mutation_performed": False,
        "service_action_performed": False,
        "runtime_start_performed": False,
        "runtime_stop_performed": False,
        "runtime_reload_performed": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "policy_promotion_performed": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "canonical_live_collection_entrypoint_implementation_present": True,
        "canonical_live_collection_entrypoint_source_binding_present": False,
        "canonical_live_collection_path_complete": False,
        "canonical_collection_enabled": False,
        "runtime_execution_authorized": False,
        "holds": [NEXT_GATE, RUNTIME_AUTHORITY_BLOCKER],
        "adapter_candidate": deepcopy(candidate),
        "adapter_bound_validation": deepcopy(validation),
        "activation_evidence": deepcopy(candidate["activation_evidence"]),
        "activation_evidence_admission": deepcopy(
            candidate["activation_evidence_admission"]
        ),
        "dependency_contracts": dependencies,
    }


def v2r13_canonical_live_collection_entrypoint_contract() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "snapshot_id": V2R13,
        "adapter_binding_git_blob": ADAPTER_BINDING_GIT_BLOB,
        "adapter_binding_source_sha256": ADAPTER_BINDING_SOURCE_SHA256,
        "adapter_git_blob": ADAPTER_GIT_BLOB,
        "adapter_source_sha256": ADAPTER_SOURCE_SHA256,
        "canonical_live_collection_entrypoint_implementation_present": True,
        "entrypoint_composition_implemented": True,
        "entrypoint_collection_requires_explicit_authority": True,
        "entrypoint_observation_requires_explicit_authority": True,
        "explicit_http_backend_injection_required": True,
        "explicit_docker_command_backend_injection_required": True,
        "supplied_worktree_receipt_required": True,
        "supplied_portable_binding_attestation_required": True,
        "automatic_host_backend_selection": False,
        "adapter_invocation_implemented": True,
        "adapter_binding_validation_implemented": True,
        "provider_capability_supported_primitive_count": 16,
        "provider_capability_remaining_unresolved_primitive_count": 0,
        "provider_capability_complete": True,
        "collector_identity_admission_implemented": True,
        "runtime_readiness_admission_implemented": True,
        "canonical_live_collection_entrypoint_source_binding_present": False,
        "canonical_live_collection_path_complete": False,
        "canonical_collection_enabled": False,
        "runtime_execution_authorized": False,
        "runtime_start_stop_reload_implemented": False,
        "model_load_implemented": False,
        "model_inference_implemented": False,
        "game_execution_implemented": False,
        "training_implemented": False,
        "deployment_implemented": False,
        "void_chain_mutation_implemented": False,
        "wallet_or_funds_action_implemented": False,
        "next_gate": NEXT_GATE,
        "next_change_class": (
            "source_only_canonical_live_collection_entrypoint_binding"
        ),
        "dependency_contracts": dependencies,
    }


def enable_canonical_live_collection(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13CanonicalLiveCollectionEntrypointHold(NEXT_GATE)


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13CanonicalLiveCollectionEntrypointHold(
        "V2R13_CANONICAL_COLLECTION_ENTRYPOINT_SOURCE_BINDING_AND_RUNTIME_ACTIVATION_GAPS_REMAIN"
    )
