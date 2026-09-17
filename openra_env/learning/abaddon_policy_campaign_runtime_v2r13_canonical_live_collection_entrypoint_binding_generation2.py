"""Source-only binding for the reviewed V2R13 canonical live-collection entrypoint.

This separate instrument pins the accepted entrypoint implementation by exact Git
blob and SHA-256 and validates only an already-supplied entrypoint receipt.

It never invokes the entrypoint, never performs live observation, and never
selects or calls HTTP, Ollama, Docker, filesystem, Git, or portable-binding host
backends.  The supplied receipt is revalidated through the reviewed adapter
source binding and checked against the exact entrypoint contract boundaries.

Once this binding is present, the reviewed canonical live-collection path is
source-complete, but canonical live collection is still not enabled.  A separate
explicitly authorized live-collection invocation remains required. Runtime
execution remains independently closed.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_adapter_binding_generation2
    as adapter_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_entrypoint_generation2
    as entrypoint,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    RUNTIME_AUTHORITY_BLOCKER,
    V2R13,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-canonical-live-collection-entrypoint-binding-contract.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-canonical-live-collection-entrypoint-bound-validation.v1"
)

ENTRYPOINT_GIT_BLOB = "48e579c5d8ef0c05db93d637777d4882493cbf9d"
ENTRYPOINT_SOURCE_SHA256 = (
    "e1cf2acb9fec1fec1d4282312fd26443979f72bda93a3244d1caa5556136d6fa"
)
ADAPTER_BINDING_GIT_BLOB = "4945f98a5dc12cff282c767013f81cac091e32e8"
ADAPTER_BINDING_SOURCE_SHA256 = (
    "55d85737e0c0ee55199505b20e5628e8e6f7cc171dba9210cd67c753ec03458c"
)

NEXT_GATE = "V2R13_CANONICAL_LIVE_COLLECTION_INVOCATION_AUTHORIZATION_REQUIRED"

EXPECTED_ENTRYPOINT_RECEIPT_FIELDS = frozenset(
    {
        "schema",
        "snapshot_id",
        "collection_authorized",
        "observation_authorized",
        "explicit_http_backend_supplied",
        "explicit_docker_command_backend_supplied",
        "supplied_worktree_receipt_present",
        "supplied_portable_binding_attestation_present",
        "automatic_host_backend_selection",
        "entrypoint_invocation_performed",
        "adapter_invocation_performed",
        "adapter_binding_validation_performed",
        "live_observation_performed",
        "ollama_tags_request_performed",
        "ollama_ps_request_performed",
        "chat_completions_request_performed",
        "docker_metadata_command_count",
        "docker_mutating_command_performed",
        "worktree_observation_performed_by_entrypoint",
        "portable_binding_install_performed_by_entrypoint",
        "provider_capability_supported_primitive_count",
        "provider_capability_remaining_unresolved_primitive_count",
        "provider_capability_complete",
        "collector_identity_admitted",
        "runtime_readiness_admitted",
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "runtime_stop_performed",
        "runtime_reload_performed",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "policy_promotion_performed",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
        "canonical_live_collection_entrypoint_implementation_present",
        "canonical_live_collection_entrypoint_source_binding_present",
        "canonical_live_collection_path_complete",
        "canonical_collection_enabled",
        "runtime_execution_authorized",
        "holds",
        "adapter_candidate",
        "adapter_bound_validation",
        "activation_evidence",
        "activation_evidence_admission",
        "dependency_contracts",
    }
)

FALSE_BOUNDARY_FIELDS = (
    "chat_completions_request_performed",
    "docker_mutating_command_performed",
    "worktree_observation_performed_by_entrypoint",
    "portable_binding_install_performed_by_entrypoint",
    "mutation_performed",
    "service_action_performed",
    "runtime_start_performed",
    "runtime_stop_performed",
    "runtime_reload_performed",
    "model_load_performed",
    "model_inference_performed",
    "game_execution_performed",
    "training_performed",
    "weights_updated",
    "policy_promotion_performed",
    "deployment_performed",
    "void_chain_mutation_performed",
    "wallet_or_funds_action_performed",
    "canonical_live_collection_entrypoint_source_binding_present",
    "canonical_live_collection_path_complete",
    "canonical_collection_enabled",
    "runtime_execution_authorized",
)


class RuntimeV2R13CanonicalLiveCollectionEntrypointBindingHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13CanonicalLiveCollectionEntrypointBindingHold(message)


def _validate_dependencies() -> dict[str, Any]:
    entry = entrypoint.v2r13_canonical_live_collection_entrypoint_contract()
    adapter_bound = (
        adapter_binding
        .v2r13_canonical_live_collection_adapter_binding_contract()
    )

    _require(
        entry.get("canonical_live_collection_entrypoint_implementation_present")
        is True,
        "V2R13 canonical entrypoint implementation missing",
    )
    _require(
        entry.get("entrypoint_composition_implemented") is True,
        "V2R13 canonical entrypoint composition missing",
    )
    _require(
        entry.get("entrypoint_collection_requires_explicit_authority") is True,
        "V2R13 entrypoint collection authority requirement lost",
    )
    _require(
        entry.get("entrypoint_observation_requires_explicit_authority") is True,
        "V2R13 entrypoint observation authority requirement lost",
    )
    _require(
        entry.get("explicit_http_backend_injection_required") is True,
        "V2R13 entrypoint HTTP backend injection requirement lost",
    )
    _require(
        entry.get("explicit_docker_command_backend_injection_required") is True,
        "V2R13 entrypoint Docker backend injection requirement lost",
    )
    _require(
        entry.get("automatic_host_backend_selection") is False,
        "V2R13 entrypoint automatic host selection enabled",
    )
    _require(
        entry.get("canonical_live_collection_entrypoint_source_binding_present")
        is False,
        "V2R13 entrypoint unexpectedly self-binds source",
    )
    _require(
        entry.get("canonical_live_collection_path_complete") is False,
        "V2R13 entrypoint unexpectedly claims canonical path complete",
    )
    _require(
        entry.get("canonical_collection_enabled") is False,
        "V2R13 entrypoint unexpectedly enables canonical collection",
    )
    _require(
        entry.get("runtime_execution_authorized") is False,
        "V2R13 entrypoint unexpectedly authorizes runtime execution",
    )
    _require(
        entry.get("next_gate")
        == "V2R13_CANONICAL_LIVE_COLLECTION_ENTRYPOINT_SOURCE_BINDING_REQUIRED",
        "V2R13 entrypoint source-binding gate drift",
    )

    _require(
        adapter_bound.get(
            "canonical_live_collection_adapter_source_binding_present"
        )
        is True,
        "V2R13 adapter source binding missing",
    )
    _require(
        adapter_bound.get("canonical_collection_enabled") is False,
        "V2R13 adapter binding unexpectedly enables canonical collection",
    )
    _require(
        adapter_bound.get("runtime_execution_authorized") is False,
        "V2R13 adapter binding unexpectedly authorizes runtime execution",
    )

    return {
        "entrypoint": deepcopy(entry),
        "adapter_binding": deepcopy(adapter_bound),
    }


def validate_bound_canonical_live_collection_entrypoint_receipt(
    receipt: Mapping[str, Any],
    *,
    entrypoint_source_sha256: str,
) -> dict[str, Any]:
    """Validate an already-supplied entrypoint receipt without invoking it."""
    dependencies = _validate_dependencies()

    _require(
        isinstance(receipt, Mapping),
        "V2R13 canonical entrypoint receipt must be object",
    )
    _require(
        entrypoint_source_sha256 == ENTRYPOINT_SOURCE_SHA256,
        "V2R13 canonical entrypoint source SHA mismatch",
    )
    _require(
        set(receipt) == EXPECTED_ENTRYPOINT_RECEIPT_FIELDS,
        "V2R13 canonical entrypoint receipt field-set drift",
    )
    _require(
        receipt.get("schema") == entrypoint.RECEIPT_SCHEMA,
        "V2R13 canonical entrypoint receipt schema drift",
    )
    _require(
        receipt.get("snapshot_id") == V2R13,
        "V2R13 canonical entrypoint receipt snapshot drift",
    )

    for field in (
        "collection_authorized",
        "observation_authorized",
        "explicit_http_backend_supplied",
        "explicit_docker_command_backend_supplied",
        "supplied_worktree_receipt_present",
        "supplied_portable_binding_attestation_present",
        "entrypoint_invocation_performed",
        "adapter_invocation_performed",
        "adapter_binding_validation_performed",
        "live_observation_performed",
        "ollama_tags_request_performed",
        "ollama_ps_request_performed",
        "provider_capability_complete",
        "collector_identity_admitted",
        "runtime_readiness_admitted",
        "canonical_live_collection_entrypoint_implementation_present",
    ):
        _require(
            receipt.get(field) is True,
            f"V2R13 canonical entrypoint receipt missing true field: {field}",
        )

    _require(
        receipt.get("automatic_host_backend_selection") is False,
        "V2R13 canonical entrypoint used automatic host selection",
    )
    _require(
        receipt.get("provider_capability_supported_primitive_count") == 16,
        "V2R13 canonical entrypoint supported primitive count drift",
    )
    _require(
        receipt.get("provider_capability_remaining_unresolved_primitive_count")
        == 0,
        "V2R13 canonical entrypoint unresolved primitive count drift",
    )
    _require(
        receipt.get("docker_metadata_command_count") == 3,
        "V2R13 canonical entrypoint Docker metadata command count drift",
    )

    for field in FALSE_BOUNDARY_FIELDS:
        _require(
            receipt.get(field) is False,
            f"V2R13 canonical entrypoint crossed boundary: {field}",
        )

    _require(
        list(receipt.get("holds", ()))
        == [
            "V2R13_CANONICAL_LIVE_COLLECTION_ENTRYPOINT_SOURCE_BINDING_REQUIRED",
            RUNTIME_AUTHORITY_BLOCKER,
        ],
        "V2R13 canonical entrypoint hold set drift",
    )

    adapter_candidate = receipt.get("adapter_candidate")
    _require(
        isinstance(adapter_candidate, Mapping),
        "V2R13 entrypoint embedded adapter candidate missing",
    )
    adapter_validation = (
        adapter_binding
        .validate_bound_canonical_live_collection_adapter_candidate(
            adapter_candidate,
            adapter_source_sha256=entrypoint.ADAPTER_SOURCE_SHA256,
        )
    )
    embedded_validation = receipt.get("adapter_bound_validation")
    _require(
        isinstance(embedded_validation, Mapping)
        and dict(embedded_validation) == adapter_validation,
        "V2R13 entrypoint embedded adapter validation mismatch",
    )

    _require(
        receipt.get("activation_evidence")
        == adapter_candidate.get("activation_evidence"),
        "V2R13 entrypoint activation evidence identity mismatch",
    )
    _require(
        receipt.get("activation_evidence_admission")
        == adapter_candidate.get("activation_evidence_admission"),
        "V2R13 entrypoint activation admission identity mismatch",
    )
    _require(
        receipt.get("dependency_contracts")
        == dependencies["entrypoint"].get("dependency_contracts"),
        "V2R13 entrypoint dependency snapshot drift",
    )

    return {
        "schema": VALIDATION_SCHEMA,
        "snapshot_id": V2R13,
        "entrypoint_git_blob": ENTRYPOINT_GIT_BLOB,
        "entrypoint_source_sha256": ENTRYPOINT_SOURCE_SHA256,
        "canonical_live_collection_entrypoint_source_binding_present": True,
        "bound_entrypoint_receipt_valid": True,
        "binding_entrypoint_invocation_performed": False,
        "binding_live_observation_performed": False,
        "binding_http_request_performed": False,
        "binding_ollama_request_performed": False,
        "binding_docker_command_performed": False,
        "binding_worktree_observation_performed": False,
        "binding_portable_install_performed": False,
        "provider_capability_supported_primitive_count": 16,
        "provider_capability_remaining_unresolved_primitive_count": 0,
        "provider_capability_complete": True,
        "collector_identity_admitted": True,
        "runtime_readiness_admitted": True,
        "canonical_live_collection_path_complete": True,
        "canonical_collection_enabled": False,
        "runtime_execution_authorized": False,
        "next_gate": NEXT_GATE,
        "holds": [NEXT_GATE, RUNTIME_AUTHORITY_BLOCKER],
        "adapter_bound_validation": deepcopy(adapter_validation),
        "activation_evidence": deepcopy(receipt["activation_evidence"]),
        "activation_evidence_admission": deepcopy(
            receipt["activation_evidence_admission"]
        ),
        "validated_receipt": deepcopy(dict(receipt)),
    }


def v2r13_canonical_live_collection_entrypoint_binding_contract() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "snapshot_id": V2R13,
        "entrypoint_git_blob": ENTRYPOINT_GIT_BLOB,
        "entrypoint_source_sha256": ENTRYPOINT_SOURCE_SHA256,
        "entrypoint_source_identity_pinned_by_git_blob": True,
        "entrypoint_source_identity_pinned_by_sha256": True,
        "entrypoint_source_is_not_self_bound": True,
        "separate_binding_instrument": True,
        "canonical_live_collection_entrypoint_source_binding_present": True,
        "supplied_bound_entrypoint_receipt_validator_implemented": True,
        "binding_entrypoint_invocation_implemented": False,
        "binding_live_observation_implemented": False,
        "binding_http_request_implemented": False,
        "binding_ollama_request_implemented": False,
        "binding_docker_command_implemented": False,
        "binding_worktree_observation_implemented": False,
        "binding_portable_install_implemented": False,
        "entrypoint_collection_requires_explicit_authority": True,
        "entrypoint_observation_requires_explicit_authority": True,
        "explicit_http_backend_injection_required": True,
        "explicit_docker_command_backend_injection_required": True,
        "supplied_worktree_receipt_required": True,
        "supplied_portable_binding_attestation_required": True,
        "automatic_host_backend_selection": False,
        "provider_capability_supported_primitive_count": 16,
        "provider_capability_remaining_unresolved_primitive_count": 0,
        "provider_capability_complete": True,
        "collector_identity_admission_implemented": True,
        "runtime_readiness_admission_implemented": True,
        "canonical_live_collection_path_complete": True,
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
        "next_change_class": "explicit_live_collection_authorization_and_invocation",
        "dependency_contracts": dependencies,
    }


def enable_canonical_live_collection(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13CanonicalLiveCollectionEntrypointBindingHold(NEXT_GATE)


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13CanonicalLiveCollectionEntrypointBindingHold(
        "V2R13_CANONICAL_COLLECTION_LIVE_INVOCATION_AND_RUNTIME_ACTIVATION_GAPS_REMAIN"
    )
