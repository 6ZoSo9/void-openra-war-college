"""Dormant backend-agnostic V2R13 runtime-image observer for Generation-2.

This module implements only the reviewable interface for the final unresolved
V2R13 live-identity channel:

* runtime_image_identity_verified

It deliberately does NOT choose or implement a host mechanism. In particular,
there is no Docker, Podman, containerd, systemd, process, filesystem, Git,
network, or subprocess backend in this source.

A caller may supply an explicitly reviewed read-only backend plus the backend's
separately reviewed source SHA-256. The public observation entrypoint requires
``observation_authorized=True`` before invoking that supplied backend.

A matching supplied result can prove only that the supplied backend record has
the expected frozen runtime-image ID and remained within the read-only authority
boundary. It does not admit the backend source, collector identity, provider
binding, runtime readiness, or runtime execution.

Therefore even a matching supplied backend result returns:

* runtime_image_identity_observed = true
* runtime_image_identity_matches_expected = true
* runtime_image_identity_verified = false
* collector_identity_admitted = false
* canonical_provider_binding_present = false
* V2R13 frontier remains 13 supported / 3 unresolved

No host observation occurs merely by importing or inspecting this module.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Protocol

from openra_env.learning import (
    abaddon_policy_campaign_runtime_activation_contract_generation2
    as activation_contract,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_live_identity_collector_contract_generation2
    as live_identity_contract,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-runtime-image-readonly-observer-contract.v1"
)
BACKEND_RECEIPT_SCHEMA = (
    "void.abaddon.generation2.v2r13-runtime-image-readonly-backend-receipt.v1"
)
OBSERVATION_SCHEMA = (
    "void.abaddon.generation2.v2r13-runtime-image-readonly-observation.v1"
)

LIVE_IDENTITY_COLLECTOR_CONTRACT_GIT_BLOB = (
    "db9fbb58f3d5870c77a796641afb1014acc19ee4"
)
ACTIVATION_CONTRACT_GIT_BLOB = "a3acb42280c334daa24a3b830105a04666fd603b"
LIVE_IDENTITY_COLLECTOR_SEMANTIC_SHA256 = (
    "0bda63a4d82be7f38e604c15fe63f659051cc42527bc9281317df167f6145219"
)

SHA256_HEX = frozenset("0123456789abcdef")

BACKEND_RECEIPT_FIELDS = (
    "schema",
    "snapshot_id",
    "primitive_name",
    "source_sha256",
    "backend_kind",
    "observation_mode",
    "runtime_image_id",
    "runtime_image_identity_observation_performed",
    "mutation_performed",
    "service_action_performed",
    "runtime_start_performed",
    "runtime_stop_performed",
    "runtime_reload_performed",
    "model_load_performed",
    "model_inference_performed",
    "game_execution_performed",
)


class RuntimeV2R13RuntimeImageObserverHold(ValueError):
    pass


class RuntimeImageBackend(Protocol):
    def __call__(self) -> Mapping[str, Any]:
        ...


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13RuntimeImageObserverHold(message)


def _require_observation_authority(observation_authorized: bool) -> None:
    _require(
        observation_authorized is True,
        "GENERATION2_V2R13_RUNTIME_IMAGE_OBSERVATION_NOT_AUTHORIZED",
    )


def _is_sha256(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(char in SHA256_HEX for char in value)
    )


def _validate_semantic_contract() -> Mapping[str, Any]:
    validated = live_identity_contract.validate_v2r13_live_identity_collector_contract()
    _require(
        validated.get("collector_contract_sha256")
        == LIVE_IDENTITY_COLLECTOR_SEMANTIC_SHA256,
        "V2R13 live identity collector semantic SHA drift",
    )
    _require(
        validated.get("collector_binding_activation") is False,
        "V2R13 collector binding unexpectedly active",
    )
    _require(
        validated.get("automatic_host_backend_selection") is False,
        "V2R13 semantic contract unexpectedly enables automatic host backend",
    )
    return validated


def validate_runtime_image_backend_receipt(
    receipt: Mapping[str, Any],
    *,
    expected_source_sha256: str,
) -> dict[str, Any]:
    """Validate one already-supplied runtime-image backend receipt."""
    _require(isinstance(receipt, Mapping), "runtime-image receipt must be object")
    _require(
        _is_sha256(expected_source_sha256),
        "runtime-image expected source SHA malformed",
    )
    _require(
        set(receipt) == set(BACKEND_RECEIPT_FIELDS),
        "runtime-image receipt field-set drift",
    )
    _require(
        receipt.get("schema") == BACKEND_RECEIPT_SCHEMA,
        "runtime-image receipt schema drift",
    )
    _require(
        receipt.get("snapshot_id") == activation_contract.V2R13,
        "runtime-image receipt snapshot drift",
    )
    _require(
        receipt.get("primitive_name") == "runtime_image_identity_verified",
        "runtime-image receipt primitive-name drift",
    )
    _require(
        receipt.get("source_sha256") == expected_source_sha256,
        "runtime-image receipt source binding mismatch",
    )
    _require(
        type(receipt.get("backend_kind")) is str
        and bool(receipt.get("backend_kind")),
        "runtime-image backend kind missing",
    )
    _require(
        receipt.get("observation_mode") == "read_only",
        "runtime-image receipt observation mode must be read_only",
    )
    _require(
        receipt.get("runtime_image_identity_observation_performed") is True,
        "runtime-image observation not performed in supplied receipt",
    )
    _require(
        receipt.get("runtime_image_id") == activation_contract.V2R13_RUNTIME_IMAGE_ID,
        "runtime-image identity drift",
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
    ):
        _require(
            receipt.get(field) is False,
            f"runtime-image receipt crossed authority boundary: {field}",
        )

    return {
        "backend_receipt_valid": True,
        "reviewed_backend_source_sha256": expected_source_sha256,
        "backend_kind": receipt["backend_kind"],
        "runtime_image_identity_observed": True,
        "runtime_image_id": receipt["runtime_image_id"],
        "runtime_image_identity_matches_expected": True,
        "canonical_backend_source_binding_present": False,
        "runtime_image_identity_verified": False,
        "collector_identity_admitted": False,
        "canonical_provider_binding_present": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "validated_receipt": deepcopy(dict(receipt)),
    }


def observe_v2r13_runtime_image_readonly(
    *,
    observation_authorized: bool,
    backend: RuntimeImageBackend,
    reviewed_backend_source_sha256: str,
) -> dict[str, Any]:
    """Invoke one explicitly supplied reviewed backend after authority check."""
    _require_observation_authority(observation_authorized)
    _require(callable(backend), "V2R13 runtime-image backend required")
    _require(
        _is_sha256(reviewed_backend_source_sha256),
        "reviewed runtime-image backend source SHA malformed",
    )

    semantic = _validate_semantic_contract()
    raw = backend()
    validated = validate_runtime_image_backend_receipt(
        raw,
        expected_source_sha256=reviewed_backend_source_sha256,
    )

    return {
        "schema": OBSERVATION_SCHEMA,
        "snapshot_id": activation_contract.V2R13,
        "collector_contract_sha256": LIVE_IDENTITY_COLLECTOR_SEMANTIC_SHA256,
        "semantic_contract_valid": semantic["semantic_contract_valid"],
        "reviewed_backend_source_sha256": reviewed_backend_source_sha256,
        "backend_kind": validated["backend_kind"],
        "runtime_image_identity_observed": True,
        "runtime_image_id": validated["runtime_image_id"],
        "runtime_image_identity_matches_expected": True,
        "runtime_image_identity_verified": False,
        "canonical_backend_source_binding_present": False,
        "collector_identity_admitted": False,
        "canonical_provider_binding_present": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "supported_primitive_count_remains": 13,
        "remaining_unresolved_primitive_count_remains": 3,
        "remaining_unresolved_primitive_names": (
            "endpoint_liveness",
            "model_identity_verified",
            "runtime_image_identity_verified",
        ),
        "host_backend_selected_automatically": False,
        "backend_receipt_validation": deepcopy(validated),
        "mutation_performed": False,
        "service_action_performed": False,
        "runtime_start_performed": False,
        "runtime_stop_performed": False,
        "runtime_reload_performed": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
    }


def v2r13_runtime_image_readonly_observer_contract() -> dict[str, Any]:
    semantic = _validate_semantic_contract()
    return {
        "schema": CONTRACT_SCHEMA,
        "live_identity_collector_contract_git_blob": (
            LIVE_IDENTITY_COLLECTOR_CONTRACT_GIT_BLOB
        ),
        "activation_contract_git_blob": ACTIVATION_CONTRACT_GIT_BLOB,
        "live_identity_collector_semantic_sha256": (
            LIVE_IDENTITY_COLLECTOR_SEMANTIC_SHA256
        ),
        "expected_runtime_image_id": activation_contract.V2R13_RUNTIME_IMAGE_ID,
        "semantic_contract_valid": semantic["semantic_contract_valid"],
        "runtime_image_backend_protocol_implemented": True,
        "supplied_backend_receipt_validator_implemented": True,
        "reviewed_backend_source_binding_required": True,
        "canonical_backend_source_binding_present": False,
        "automatic_backend_selection": False,
        "observation_requires_explicit_authority": True,
        "docker_backend_implemented": False,
        "podman_backend_implemented": False,
        "containerd_backend_implemented": False,
        "systemd_backend_implemented": False,
        "process_backend_implemented": False,
        "filesystem_backend_implemented": False,
        "network_backend_implemented": False,
        "subprocess_backend_implemented": False,
        "runtime_image_identity_provider_primitive_implemented": False,
        "candidate_observation_does_not_admit_collector_identity": True,
        "candidate_observation_does_not_advance_primitive_frontier": True,
        "supported_primitive_count_remains": 13,
        "remaining_unresolved_primitive_count_remains": 3,
        "remaining_unresolved_primitive_names": (
            "endpoint_liveness",
            "model_identity_verified",
            "runtime_image_identity_verified",
        ),
        "service_action_implemented": False,
        "runtime_start_stop_reload_implemented": False,
        "model_load_implemented": False,
        "model_inference_implemented": False,
        "canonical_provider_binding_present": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
    }
