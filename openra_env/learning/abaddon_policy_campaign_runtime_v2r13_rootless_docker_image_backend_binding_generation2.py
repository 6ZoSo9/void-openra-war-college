"""Source-only canonical binding for the V2R13 rootless-Docker image backend.

This module is the separate review/source-binding instrument required by the
Generation-2 trust model.  It binds the already-merged V2R13 rootless-Docker
local image-store backend by BOTH:

* canonical Git blob identity; and
* reviewed source SHA-256.

The bound backend source was merged before this file exists, so the binding is
not self-referential.

This module performs no host observation and never invokes Docker.  It accepts
only an already-supplied exact backend receipt, validates that receipt through
the canonical runtime-image interface using the pinned backend source SHA-256,
and then admits exactly one provider primitive:

* runtime_image_identity_verified

Endpoint liveness and active-model digest identity remain unresolved.  Full
collector identity, canonical provider binding, runtime readiness, and runtime
execution remain closed.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_activation_contract_generation2
    as activation_contract,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_provider_composition_generation2
    as provider_composition,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_rootless_docker_image_backend_generation2
    as docker_backend,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_runtime_image_readonly_observer_generation2
    as runtime_image_interface,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-rootless-docker-image-backend-binding-contract.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-rootless-docker-image-backend-bound-validation.v1"
)

ACTIVATION_CONTRACT_GIT_BLOB = "a3acb42280c334daa24a3b830105a04666fd603b"
PROVIDER_COMPOSITION_GIT_BLOB = "4efdf74ac7b140af5f29d5539eccde98694f4a3b"
RUNTIME_IMAGE_INTERFACE_GIT_BLOB = "8bc118684fb085361fa98dd80b6a1ee37edeb523"
ROOTLESS_DOCKER_BACKEND_GIT_BLOB = "488497f723ad5bc5ca63b3b2d69cece26bddaaa5"

ROOTLESS_DOCKER_BACKEND_SOURCE_SHA256 = (
    "25e8f41dcea700860ec1b97726b321a99c2622e00ddba12433246c7b121b11f6"
)
ROOTLESS_DOCKER_BACKEND_KIND = "rootless_docker_local_image_store_v1"

RUNTIME_IMAGE_PRIMITIVE = "runtime_image_identity_verified"
BASELINE_SUPPORTED_COUNT = 13
BOUND_SUPPORTED_COUNT = 14
BOUND_REMAINING_UNRESOLVED = (
    "endpoint_liveness",
    "model_identity_verified",
)


class RuntimeV2R13RootlessDockerImageBackendBindingHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13RootlessDockerImageBackendBindingHold(message)


def _validate_dependency_contracts() -> dict[str, Any]:
    backend = docker_backend.v2r13_rootless_docker_image_backend_contract()
    interface = runtime_image_interface.v2r13_runtime_image_readonly_observer_contract()
    baseline = provider_composition.v2r13_provider_composition_contract()

    _require(
        backend.get("backend_kind") == ROOTLESS_DOCKER_BACKEND_KIND,
        "V2R13 bound Docker backend kind drift",
    )
    _require(
        backend.get("expected_runtime_image_id")
        == activation_contract.V2R13_RUNTIME_IMAGE_ID,
        "V2R13 bound Docker backend image identity drift",
    )
    _require(
        backend.get("candidate_backend_implemented") is True,
        "V2R13 bound Docker backend candidate not implemented",
    )
    _require(
        backend.get("reviewed_source_binding_required") is True,
        "V2R13 Docker backend no longer requires source binding",
    )
    _require(
        backend.get("canonical_backend_source_binding_present") is False,
        "V2R13 Docker backend source unexpectedly self-bound",
    )
    _require(
        backend.get("automatic_host_backend_selection") is False,
        "V2R13 Docker backend automatic selection enabled",
    )

    _require(
        interface.get("runtime_image_backend_protocol_implemented") is True,
        "V2R13 runtime-image interface protocol missing",
    )
    _require(
        interface.get("supplied_backend_receipt_validator_implemented") is True,
        "V2R13 runtime-image receipt validator missing",
    )
    _require(
        interface.get("canonical_backend_source_binding_present") is False,
        "V2R13 runtime-image interface unexpectedly self-bound",
    )

    _require(
        baseline.get("combined_supported_primitive_count")
        == BASELINE_SUPPORTED_COUNT,
        "V2R13 provider baseline supported count drift",
    )
    _require(
        baseline.get("remaining_unresolved_primitive_count") == 3,
        "V2R13 provider baseline unresolved count drift",
    )
    _require(
        tuple(baseline.get("remaining_unresolved_primitive_names", ()))
        == (
            "endpoint_liveness",
            "model_identity_verified",
            "runtime_image_identity_verified",
        ),
        "V2R13 provider baseline unresolved set drift",
    )
    _require(
        baseline.get("live_runtime_image_provider_implemented") is False,
        "V2R13 provider baseline runtime-image primitive unexpectedly implemented",
    )
    _require(
        baseline.get("canonical_provider_binding_present") is False,
        "V2R13 provider baseline unexpectedly canonical",
    )

    return {
        "backend": deepcopy(backend),
        "interface": deepcopy(interface),
        "baseline": deepcopy(baseline),
    }


def validate_bound_runtime_image_receipt(
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Admit exactly the bound runtime-image primitive from supplied evidence."""
    dependencies = _validate_dependency_contracts()

    _require(
        isinstance(receipt, Mapping),
        "V2R13 bound runtime-image receipt must be object",
    )
    _require(
        set(receipt) == set(runtime_image_interface.BACKEND_RECEIPT_FIELDS),
        "V2R13 bound runtime-image receipt field-set drift",
    )
    _require(
        receipt.get("backend_kind") == ROOTLESS_DOCKER_BACKEND_KIND,
        "V2R13 bound runtime-image backend kind mismatch",
    )
    _require(
        receipt.get("source_sha256") == ROOTLESS_DOCKER_BACKEND_SOURCE_SHA256,
        "V2R13 bound runtime-image backend source SHA mismatch",
    )

    validated = runtime_image_interface.validate_runtime_image_backend_receipt(
        receipt,
        expected_source_sha256=ROOTLESS_DOCKER_BACKEND_SOURCE_SHA256,
    )

    _require(
        validated.get("backend_receipt_valid") is True,
        "V2R13 bound runtime-image backend receipt invalid",
    )
    _require(
        validated.get("runtime_image_identity_matches_expected") is True,
        "V2R13 bound runtime-image identity mismatch",
    )
    _require(
        validated.get("runtime_image_id")
        == activation_contract.V2R13_RUNTIME_IMAGE_ID,
        "V2R13 bound runtime-image ID drift",
    )
    _require(
        validated.get("runtime_image_identity_verified") is False,
        "unbound interface unexpectedly verified runtime image",
    )

    primitive_values = {
        RUNTIME_IMAGE_PRIMITIVE: True,
    }

    return {
        "schema": VALIDATION_SCHEMA,
        "snapshot_id": activation_contract.V2R13,
        "backend_kind": ROOTLESS_DOCKER_BACKEND_KIND,
        "reviewed_backend_source_sha256": ROOTLESS_DOCKER_BACKEND_SOURCE_SHA256,
        "reviewed_backend_git_blob": ROOTLESS_DOCKER_BACKEND_GIT_BLOB,
        "canonical_backend_source_binding_present": True,
        "backend_receipt_valid": True,
        "runtime_image_identity_observed": True,
        "runtime_image_identity_matches_expected": True,
        "runtime_image_id": activation_contract.V2R13_RUNTIME_IMAGE_ID,
        "runtime_image_identity_verified": True,
        "primitive_values": primitive_values,
        "supported_primitive_count_after_binding": BOUND_SUPPORTED_COUNT,
        "remaining_unresolved_primitive_names": BOUND_REMAINING_UNRESOLVED,
        "remaining_unresolved_primitive_count": len(BOUND_REMAINING_UNRESOLVED),
        "endpoint_liveness_verified": False,
        "model_identity_verified": False,
        "full_collector_identity_admitted": False,
        "canonical_provider_binding_present": False,
        "canonical_collection_enabled": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "binding_filesystem_observation_performed": False,
        "binding_git_query_performed": False,
        "binding_subprocess_execution_performed": False,
        "binding_host_backend_invocation_performed": False,
        "binding_network_probe_performed": False,
        "binding_ollama_http_request_performed": False,
        "binding_model_inference_performed": False,
        "binding_game_execution_performed": False,
        "interface_validation": deepcopy(validated),
        "dependency_contracts": dependencies,
    }


def v2r13_rootless_docker_image_backend_binding_contract() -> dict[str, Any]:
    dependencies = _validate_dependency_contracts()

    return {
        "schema": CONTRACT_SCHEMA,
        "activation_contract_git_blob": ACTIVATION_CONTRACT_GIT_BLOB,
        "provider_composition_git_blob": PROVIDER_COMPOSITION_GIT_BLOB,
        "runtime_image_interface_git_blob": RUNTIME_IMAGE_INTERFACE_GIT_BLOB,
        "rootless_docker_backend_git_blob": ROOTLESS_DOCKER_BACKEND_GIT_BLOB,
        "rootless_docker_backend_source_sha256": (
            ROOTLESS_DOCKER_BACKEND_SOURCE_SHA256
        ),
        "snapshot_id": activation_contract.V2R13,
        "backend_kind": ROOTLESS_DOCKER_BACKEND_KIND,
        "expected_runtime_image_id": activation_contract.V2R13_RUNTIME_IMAGE_ID,
        "separate_binding_instrument": True,
        "backend_source_identity_pinned_by_git_blob": True,
        "backend_source_identity_pinned_by_sha256": True,
        "backend_source_is_not_self_bound": True,
        "canonical_backend_source_binding_present": True,
        "supplied_bound_receipt_validator_implemented": True,
        "runtime_image_identity_provider_primitive_implemented": True,
        "runtime_image_identity_can_verify_from_bound_receipt": True,
        "baseline_supported_primitive_count": BASELINE_SUPPORTED_COUNT,
        "supported_primitive_count_after_binding": BOUND_SUPPORTED_COUNT,
        "remaining_unresolved_primitive_names": BOUND_REMAINING_UNRESOLVED,
        "remaining_unresolved_primitive_count": len(BOUND_REMAINING_UNRESOLVED),
        "endpoint_liveness_provider_implemented": False,
        "model_identity_provider_implemented": False,
        "full_collector_identity_admitted": False,
        "canonical_provider_binding_present": False,
        "canonical_collection_enabled": False,
        "automatic_host_backend_selection": False,
        "binding_live_observation_implemented": False,
        "binding_filesystem_observation_implemented": False,
        "binding_git_query_implemented": False,
        "binding_subprocess_execution_implemented": False,
        "binding_host_backend_invocation_implemented": False,
        "binding_network_probe_implemented": False,
        "binding_ollama_http_request_implemented": False,
        "binding_model_inference_implemented": False,
        "binding_game_execution_implemented": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "dependency_contracts_valid": True,
        "dependency_contracts": dependencies,
    }


def collect_bound_runtime_image_identity(*args: Any, **kwargs: Any) -> None:
    """Always hold: this binding source never invokes the host backend."""
    raise RuntimeV2R13RootlessDockerImageBackendBindingHold(
        "GENERATION2_V2R13_BOUND_RUNTIME_IMAGE_LIVE_COLLECTION_NOT_IMPLEMENTED"
    )
