"""Source-only binding for the reviewed V2R13 live-collection backend.

The live-collection backend was merged before this file exists.  This separate
binding instrument pins that merged backend by BOTH canonical Git blob identity
and reviewed source SHA-256, avoiding self-reference.

The bound backend remains explicit-authority and injected-backend only.  This
binding NEVER performs live observation, selects host backends, performs an HTTP
request, invokes Docker, or enables canonical collection.  It validates only an
already-supplied candidate produced by the reviewed live-collection backend.

A separately reviewed canonical adapter remains required before any canonical
host-backed live collection can be enabled. Runtime execution remains closed.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_collector_implementation_binding_generation2
    as collector_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_live_collection_backend_generation2
    as live_backend,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_ollama_observer_binding_generation2
    as ollama_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_rootless_docker_image_backend_binding_generation2
    as docker_binding,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    RUNTIME_AUTHORITY_BLOCKER,
    V2R13,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-live-collection-backend-binding-contract.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2.v2r13-live-collection-backend-bound-validation.v1"
)

LIVE_COLLECTION_BACKEND_GIT_BLOB = "ee78726c7538aeb985ef00140d58792ec75fdcf3"
LIVE_COLLECTION_BACKEND_SOURCE_SHA256 = (
    "1f8dacce44d355f2948359ff59c29b79d50c68e21a648814689ba6a85cce2c94"
)
COLLECTOR_IMPLEMENTATION_BINDING_GIT_BLOB = (
    "bcc12598161a9516cb002d6e1c4eead7e914a425"
)
OLLAMA_BINDING_GIT_BLOB = "58364a1d5d71aead9df6dc0fc61661a557131508"
DOCKER_BINDING_GIT_BLOB = "7075ded7a19454239b95a09e7b4630413124a796"

EXPECTED_LIVE_PRIMITIVES = (
    "endpoint_liveness",
    "model_identity_verified",
    "runtime_image_identity_verified",
)
NEXT_GATE = "V2R13_CANONICAL_LIVE_COLLECTION_ADAPTER_REQUIRED"

EXPECTED_CANDIDATE_FIELDS = frozenset(
    {
        "schema",
        "snapshot_id",
        "observation_mode",
        "observation_authorized",
        "explicit_http_backend_supplied",
        "explicit_docker_command_backend_supplied",
        "automatic_host_backend_selection",
        "primitive_values",
        "primitive_receipts",
        "live_primitive_count",
        "provider_capability_supported_primitive_count",
        "provider_capability_remaining_unresolved_primitive_count",
        "provider_capability_complete",
        "live_observation_performed",
        "ollama_tags_request_performed",
        "ollama_ps_request_performed",
        "chat_completions_request_performed",
        "rootless_docker_context_inspect_performed",
        "rootless_docker_info_performed",
        "rootless_docker_image_inspect_performed",
        "docker_mutating_command_performed",
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
        "live_collection_backend_source_binding_present",
        "canonical_live_collection_path_complete",
        "canonical_collection_enabled",
        "collector_identity_admitted_by_backend",
        "runtime_readiness_admitted_by_backend",
        "runtime_execution_authorized",
        "holds",
        "ollama_observation",
        "ollama_bound_validation",
        "runtime_image_receipt",
        "runtime_image_candidate_metadata",
        "runtime_image_bound_validation",
        "dependency_contracts",
    }
)


class RuntimeV2R13LiveCollectionBackendBindingHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13LiveCollectionBackendBindingHold(message)


def _validate_dependencies() -> dict[str, Any]:
    backend = live_backend.v2r13_live_collection_backend_contract()
    collector = collector_binding.v2r13_collector_implementation_binding_contract()
    ollama = ollama_binding.v2r13_ollama_observer_binding_contract()
    docker = docker_binding.v2r13_rootless_docker_image_backend_binding_contract()

    _require(
        backend.get("live_collection_backend_implementation_present") is True,
        "V2R13 live-collection backend implementation missing",
    )
    _require(
        backend.get("live_collection_backend_composition_implemented") is True,
        "V2R13 live-collection backend composition missing",
    )
    _require(
        backend.get("live_collection_backend_requires_explicit_authority") is True,
        "V2R13 live-collection explicit authority requirement lost",
    )
    _require(
        backend.get("explicit_http_backend_injection_required") is True,
        "V2R13 live-collection HTTP backend injection requirement lost",
    )
    _require(
        backend.get("explicit_docker_command_backend_injection_required") is True,
        "V2R13 live-collection Docker backend injection requirement lost",
    )
    _require(
        backend.get("automatic_host_backend_selection") is False,
        "V2R13 live-collection automatic host backend selection enabled",
    )
    _require(
        backend.get("provider_capability_supported_primitive_count") == 16,
        "V2R13 provider supported primitive count drift",
    )
    _require(
        backend.get("provider_capability_remaining_unresolved_primitive_count") == 0,
        "V2R13 provider unresolved primitive count drift",
    )
    _require(
        tuple(backend.get("live_primitive_names", ())) == EXPECTED_LIVE_PRIMITIVES,
        "V2R13 live primitive set/order drift",
    )
    _require(
        backend.get("live_collection_backend_source_binding_present") is False,
        "V2R13 live-collection backend unexpectedly self-bound",
    )
    _require(
        backend.get("canonical_live_collection_path_complete") is False,
        "V2R13 live-collection path unexpectedly canonical before binding",
    )
    _require(
        backend.get("canonical_collection_enabled") is False,
        "V2R13 canonical collection unexpectedly enabled",
    )
    _require(
        backend.get("runtime_execution_authorized") is False,
        "V2R13 backend unexpectedly authorizes runtime execution",
    )
    _require(
        backend.get("next_gate")
        == "V2R13_LIVE_COLLECTION_BACKEND_SOURCE_BINDING_REQUIRED",
        "V2R13 backend source-binding gate drift",
    )

    _require(
        collector.get("canonical_primitive_source_bindings_present") is True,
        "V2R13 collector primitive source bindings are not canonical",
    )
    primitive_bindings = collector_binding.reviewed_v2r13_primitive_source_bindings()
    _require(
        set(EXPECTED_LIVE_PRIMITIVES).issubset(primitive_bindings),
        "V2R13 live primitive source bindings missing",
    )

    _require(
        ollama.get("canonical_observer_source_binding_present") is True,
        "V2R13 Ollama source binding missing",
    )
    _require(
        docker.get("canonical_backend_source_binding_present") is True,
        "V2R13 Docker source binding missing",
    )

    for label, contract in (
        ("backend", backend),
        ("collector_binding", collector),
        ("ollama_binding", ollama),
        ("docker_binding", docker),
    ):
        _require(
            contract.get("runtime_execution_authorized") is False,
            f"{label} unexpectedly authorizes runtime execution",
        )
        if "canonical_collection_enabled" in contract:
            _require(
                contract.get("canonical_collection_enabled") is False,
                f"{label} unexpectedly enables canonical collection",
            )

    return {
        "live_collection_backend": deepcopy(backend),
        "collector_implementation_binding": deepcopy(collector),
        "ollama_binding": deepcopy(ollama),
        "docker_binding": deepcopy(docker),
    }


def _validate_primitive_receipts(
    receipts: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    _require(
        isinstance(receipts, Mapping),
        "V2R13 bound live primitive receipts must be object",
    )
    _require(
        set(receipts) == set(EXPECTED_LIVE_PRIMITIVES),
        "V2R13 bound live primitive receipt set drift",
    )

    bindings = collector_binding.reviewed_v2r13_primitive_source_bindings()
    validated: dict[str, dict[str, Any]] = {}

    for name in EXPECTED_LIVE_PRIMITIVES:
        receipt = receipts[name]
        _require(
            isinstance(receipt, Mapping),
            f"V2R13 bound live primitive receipt must be object: {name}",
        )
        _require(
            set(receipt)
            == {
                "schema",
                "snapshot_id",
                "primitive_name",
                "source_sha256",
                "observation_mode",
                "value",
                "mutation_performed",
                "service_action_performed",
                "runtime_start_performed",
                "game_execution_performed",
                "model_inference_performed",
            },
            f"V2R13 bound live primitive receipt field-set drift: {name}",
        )
        _require(
            receipt.get("schema")
            == live_backend.collector_implementation.PRIMITIVE_RECEIPT_SCHEMA,
            f"V2R13 bound live primitive schema drift: {name}",
        )
        _require(
            receipt.get("snapshot_id") == V2R13,
            f"V2R13 bound live primitive snapshot drift: {name}",
        )
        _require(
            receipt.get("primitive_name") == name,
            f"V2R13 bound live primitive name drift: {name}",
        )
        _require(
            receipt.get("source_sha256") == bindings[name],
            f"V2R13 bound live primitive source binding mismatch: {name}",
        )
        _require(
            receipt.get("observation_mode") == "read_only",
            f"V2R13 bound live primitive observation mode drift: {name}",
        )
        _require(
            receipt.get("value") is True,
            f"V2R13 bound live primitive value not verified: {name}",
        )
        for field in (
            "mutation_performed",
            "service_action_performed",
            "runtime_start_performed",
            "game_execution_performed",
            "model_inference_performed",
        ):
            _require(
                receipt.get(field) is False,
                f"V2R13 bound live primitive crossed boundary: {name}:{field}",
            )
        validated[name] = deepcopy(dict(receipt))

    return validated


def validate_bound_live_collection_candidate(
    candidate: Mapping[str, Any],
    *,
    backend_source_sha256: str,
) -> dict[str, Any]:
    """Validate supplied live evidence against the reviewed backend source."""
    dependencies = _validate_dependencies()

    _require(
        isinstance(candidate, Mapping),
        "V2R13 bound live-collection candidate must be object",
    )
    _require(
        backend_source_sha256 == LIVE_COLLECTION_BACKEND_SOURCE_SHA256,
        "V2R13 live-collection backend source SHA mismatch",
    )
    _require(
        set(candidate) == EXPECTED_CANDIDATE_FIELDS,
        "V2R13 live-collection candidate field-set drift",
    )
    _require(
        candidate.get("schema") == live_backend.COLLECTION_SCHEMA,
        "V2R13 live-collection candidate schema drift",
    )
    _require(
        candidate.get("snapshot_id") == V2R13,
        "V2R13 live-collection candidate snapshot drift",
    )
    _require(
        candidate.get("observation_mode") == "read_only",
        "V2R13 live-collection candidate observation mode drift",
    )
    _require(
        candidate.get("observation_authorized") is True,
        "V2R13 supplied live observation was not explicitly authorized",
    )
    _require(
        candidate.get("explicit_http_backend_supplied") is True,
        "V2R13 supplied live observation lacks explicit HTTP backend",
    )
    _require(
        candidate.get("explicit_docker_command_backend_supplied") is True,
        "V2R13 supplied live observation lacks explicit Docker backend",
    )
    _require(
        candidate.get("automatic_host_backend_selection") is False,
        "V2R13 supplied live observation used automatic host backend selection",
    )
    _require(
        candidate.get("primitive_values")
        == {
            "endpoint_liveness": True,
            "model_identity_verified": True,
            "runtime_image_identity_verified": True,
        },
        "V2R13 supplied live primitive values drift",
    )

    validated_receipts = _validate_primitive_receipts(
        candidate.get("primitive_receipts")
    )

    _require(
        candidate.get("live_primitive_count") == 3,
        "V2R13 supplied live primitive count drift",
    )
    _require(
        candidate.get("provider_capability_supported_primitive_count") == 16,
        "V2R13 supplied provider supported primitive count drift",
    )
    _require(
        candidate.get("provider_capability_remaining_unresolved_primitive_count") == 0,
        "V2R13 supplied provider unresolved primitive count drift",
    )
    _require(
        candidate.get("provider_capability_complete") is True,
        "V2R13 supplied provider capability incomplete",
    )
    _require(
        candidate.get("live_observation_performed") is True,
        "V2R13 supplied candidate does not contain live observation",
    )
    _require(
        candidate.get("ollama_tags_request_performed") is True,
        "V2R13 supplied candidate lacks Ollama tags observation",
    )
    _require(
        candidate.get("ollama_ps_request_performed") is True,
        "V2R13 supplied candidate lacks Ollama ps observation",
    )
    _require(
        candidate.get("chat_completions_request_performed") is False,
        "V2R13 supplied candidate crossed into chat completions",
    )
    _require(
        candidate.get("rootless_docker_context_inspect_performed") is True,
        "V2R13 supplied candidate lacks Docker context metadata",
    )
    _require(
        candidate.get("rootless_docker_info_performed") is True,
        "V2R13 supplied candidate lacks Docker info metadata",
    )
    _require(
        candidate.get("rootless_docker_image_inspect_performed") is True,
        "V2R13 supplied candidate lacks Docker image metadata",
    )
    _require(
        candidate.get("docker_mutating_command_performed") is False,
        "V2R13 supplied candidate performed mutating Docker command",
    )

    for field in (
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
        "live_collection_backend_source_binding_present",
        "canonical_live_collection_path_complete",
        "canonical_collection_enabled",
        "collector_identity_admitted_by_backend",
        "runtime_readiness_admitted_by_backend",
        "runtime_execution_authorized",
    ):
        _require(
            candidate.get(field) is False,
            f"V2R13 supplied live candidate crossed boundary: {field}",
        )

    _require(
        candidate.get("holds")
        == [
            "V2R13_LIVE_COLLECTION_BACKEND_SOURCE_BINDING_REQUIRED",
            "V2R13_CANONICAL_COLLECTION_NOT_ENABLED",
            RUNTIME_AUTHORITY_BLOCKER,
        ],
        "V2R13 supplied live candidate hold set drift",
    )

    ollama_validation = candidate.get("ollama_bound_validation")
    image_validation = candidate.get("runtime_image_bound_validation")

    revalidated_ollama = ollama_binding.validate_bound_ollama_observation(
        candidate.get("ollama_observation"),
        observer_source_sha256=live_backend.OLLAMA_OBSERVER_SOURCE_SHA256,
    )
    revalidated_image = docker_binding.validate_bound_runtime_image_receipt(
        candidate.get("runtime_image_receipt")
    )

    _require(
        isinstance(ollama_validation, Mapping)
        and ollama_validation.get("endpoint_liveness_verified") is True
        and ollama_validation.get("model_identity_verified") is True
        and dict(ollama_validation) == revalidated_ollama,
        "V2R13 supplied Ollama bound validation drift",
    )
    _require(
        isinstance(image_validation, Mapping)
        and image_validation.get("runtime_image_identity_verified") is True
        and dict(image_validation) == revalidated_image,
        "V2R13 supplied runtime-image bound validation drift",
    )

    metadata = candidate.get("runtime_image_candidate_metadata")
    _require(
        isinstance(metadata, Mapping)
        and metadata.get("rootless_security") is True,
        "V2R13 supplied runtime-image candidate metadata drift",
    )

    return {
        "schema": VALIDATION_SCHEMA,
        "snapshot_id": V2R13,
        "reviewed_live_collection_backend_git_blob": LIVE_COLLECTION_BACKEND_GIT_BLOB,
        "reviewed_live_collection_backend_source_sha256": (
            LIVE_COLLECTION_BACKEND_SOURCE_SHA256
        ),
        "canonical_live_collection_backend_source_binding_present": True,
        "bound_live_collection_candidate_valid": True,
        "supplied_live_observation_validated": True,
        "supplied_live_observation_performed": True,
        "binding_live_observation_performed": False,
        "binding_http_request_performed": False,
        "binding_ollama_request_performed": False,
        "binding_docker_command_performed": False,
        "automatic_host_backend_selection": False,
        "provider_capability_supported_primitive_count": 16,
        "provider_capability_remaining_unresolved_primitive_count": 0,
        "provider_capability_complete": True,
        "primitive_values": deepcopy(dict(candidate["primitive_values"])),
        "validated_primitive_receipts": validated_receipts,
        "canonical_live_collection_path_complete": False,
        "canonical_collection_enabled": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "next_gate": NEXT_GATE,
        "validated_candidate": deepcopy(dict(candidate)),
        "dependency_contracts": dependencies,
    }


def v2r13_live_collection_backend_binding_contract() -> dict[str, Any]:
    dependencies = _validate_dependencies()

    return {
        "schema": CONTRACT_SCHEMA,
        "snapshot_id": V2R13,
        "live_collection_backend_git_blob": LIVE_COLLECTION_BACKEND_GIT_BLOB,
        "live_collection_backend_source_sha256": (
            LIVE_COLLECTION_BACKEND_SOURCE_SHA256
        ),
        "collector_implementation_binding_git_blob": (
            COLLECTOR_IMPLEMENTATION_BINDING_GIT_BLOB
        ),
        "ollama_binding_git_blob": OLLAMA_BINDING_GIT_BLOB,
        "docker_binding_git_blob": DOCKER_BINDING_GIT_BLOB,
        "separate_binding_instrument": True,
        "backend_source_identity_pinned_by_git_blob": True,
        "backend_source_identity_pinned_by_sha256": True,
        "backend_source_is_not_self_bound": True,
        "canonical_live_collection_backend_source_binding_present": True,
        "supplied_bound_candidate_validator_implemented": True,
        "explicit_observation_authority_required_by_backend": True,
        "explicit_http_backend_injection_required_by_backend": True,
        "explicit_docker_command_backend_injection_required_by_backend": True,
        "automatic_host_backend_selection": False,
        "provider_capability_supported_primitive_count": 16,
        "provider_capability_remaining_unresolved_primitive_count": 0,
        "provider_capability_complete": True,
        "binding_live_observation_implemented": False,
        "binding_http_request_implemented": False,
        "binding_ollama_request_implemented": False,
        "binding_docker_command_implemented": False,
        "binding_service_action_implemented": False,
        "binding_runtime_start_implemented": False,
        "binding_model_load_implemented": False,
        "binding_model_inference_implemented": False,
        "binding_game_execution_implemented": False,
        "binding_training_implemented": False,
        "binding_deployment_implemented": False,
        "binding_void_chain_mutation_implemented": False,
        "binding_wallet_or_funds_action_implemented": False,
        "canonical_live_collection_path_complete": False,
        "canonical_collection_enabled": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "next_gate": NEXT_GATE,
        "next_change_class": "explicit_authority_canonical_live_collection_adapter",
        "dependency_contracts_valid": True,
        "dependency_contracts": dependencies,
    }


def collect_bound_live_identity(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13LiveCollectionBackendBindingHold(
        "GENERATION2_V2R13_BOUND_LIVE_COLLECTION_ADAPTER_NOT_IMPLEMENTED"
    )


def enable_canonical_live_collection(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13LiveCollectionBackendBindingHold(NEXT_GATE)


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13LiveCollectionBackendBindingHold(
        "V2R13_LIVE_COLLECTION_ADAPTER_AND_RUNTIME_ACTIVATION_GAPS_REMAIN"
    )
