"""Dormant V2R13 live-identity collector implementation for Generation-2.

This module implements only pure composition/validation of already-supplied
read-only primitive receipts for the final three V2R13 live identity channels:

* endpoint_liveness
* model_identity_verified
* runtime_image_identity_verified

It does NOT implement collection. In particular it does not call an endpoint,
systemd, subprocesses, filesystem paths, Git, model servers, container tools,
or any host backend. It never automatically selects a backend.

The endpoint receipt is source-bound and may carry a supplied observed
``endpoint_liveness=true`` fact. The model/runtime-image receipt is validated by
the canonical V2R13 identity-receipt validator and must bind to the canonical
semantic collector-contract SHA.

These supplied facts remain unadmitted until a future reviewed collector
implementation source is separately pinned by the canonical admission path.

Therefore this module can validate a supplied observation bundle while still
returning:

* collector_identity_admitted = false
* endpoint_liveness_verified = false
* model_identity_verified = false
* runtime_image_identity_verified = false
* V2R13 frontier remains 13 supported / 3 unresolved

No live observation, filesystem access, external Git query, path resolution,
subprocess, HTTP/systemd probe, service action, runtime start/stop/reload,
model load/inference, game execution, training, deployment, VOID-chain
mutation, or funds action occurs here.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_activation_contract_generation2
    as activation_contract,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_identity_receipt_validator_generation2
    as identity_receipt_validator,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_live_identity_collector_contract_generation2
    as live_identity_contract,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-live-identity-collector-implementation-contract.v1"
)
ENDPOINT_RECEIPT_SCHEMA = (
    "void.abaddon.generation2.v2r13-endpoint-liveness-observation-receipt.v1"
)
CANDIDATE_SCHEMA = (
    "void.abaddon.generation2.v2r13-live-identity-collector-candidate.v1"
)

LIVE_IDENTITY_COLLECTOR_CONTRACT_GIT_BLOB = (
    "db9fbb58f3d5870c77a796641afb1014acc19ee4"
)
IDENTITY_RECEIPT_VALIDATOR_GIT_BLOB = (
    "d1586ba032d78296e200d5016560682b82ee599d"
)
ACTIVATION_CONTRACT_GIT_BLOB = "a3acb42280c334daa24a3b830105a04666fd603b"
LIVE_IDENTITY_COLLECTOR_SEMANTIC_SHA256 = (
    "0bda63a4d82be7f38e604c15fe63f659051cc42527bc9281317df167f6145219"
)

CANONICAL_IMPLEMENTATION_SOURCE_BINDING_PRESENT = False
CANONICAL_COLLECTION_ENABLED = False

SHA256_HEX = frozenset("0123456789abcdef")

ENDPOINT_RECEIPT_FIELDS = (
    "schema",
    "snapshot_id",
    "primitive_name",
    "source_sha256",
    "observation_mode",
    "endpoint_url",
    "endpoint_loopback",
    "endpoint_liveness",
    "mutation_performed",
    "service_action_performed",
    "runtime_start_performed",
    "runtime_stop_performed",
    "runtime_reload_performed",
    "model_load_performed",
    "model_inference_performed",
    "game_execution_performed",
)


class RuntimeV2R13LiveIdentityCollectorImplementationHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13LiveIdentityCollectorImplementationHold(message)


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
        validated.get("collector_implementation_present") is False,
        "V2R13 semantic contract unexpectedly claims implementation",
    )
    _require(
        validated.get("collector_binding_activation") is False,
        "V2R13 semantic contract unexpectedly activates collector binding",
    )
    _require(
        validated.get("automatic_host_backend_selection") is False,
        "V2R13 semantic contract unexpectedly enables automatic host backend",
    )
    return validated


def validate_endpoint_liveness_receipt(
    receipt: Mapping[str, Any],
    *,
    expected_source_sha256: str,
) -> dict[str, Any]:
    """Validate one already-supplied read-only endpoint-liveness receipt."""
    _require(isinstance(receipt, Mapping), "endpoint receipt must be object")
    _require(
        _is_sha256(expected_source_sha256),
        "endpoint expected source SHA malformed",
    )
    _require(
        set(receipt) == set(ENDPOINT_RECEIPT_FIELDS),
        "endpoint receipt field-set drift",
    )
    _require(
        receipt.get("schema") == ENDPOINT_RECEIPT_SCHEMA,
        "endpoint receipt schema drift",
    )
    _require(
        receipt.get("snapshot_id") == activation_contract.V2R13,
        "endpoint receipt snapshot drift",
    )
    _require(
        receipt.get("primitive_name") == "endpoint_liveness",
        "endpoint receipt primitive-name drift",
    )
    _require(
        receipt.get("source_sha256") == expected_source_sha256,
        "endpoint receipt source binding mismatch",
    )
    _require(
        receipt.get("observation_mode") == "read_only",
        "endpoint receipt observation mode must be read_only",
    )
    _require(
        receipt.get("endpoint_url") == activation_contract.LOOPBACK_11434,
        "endpoint receipt URL drift",
    )
    _require(
        receipt.get("endpoint_loopback") is True,
        "endpoint receipt is not loopback",
    )
    _require(
        receipt.get("endpoint_liveness") is True,
        "endpoint receipt lacks supplied liveness=true",
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
            f"endpoint receipt crossed authority boundary: {field}",
        )

    return {
        "endpoint_receipt_valid": True,
        "supplied_endpoint_liveness_observed": True,
        "endpoint_url": activation_contract.LOOPBACK_11434,
        "endpoint_loopback": True,
        "source_sha256": expected_source_sha256,
        "collector_identity_admitted": False,
        "endpoint_liveness_verified": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "validated_receipt": deepcopy(dict(receipt)),
    }


def assemble_candidate_from_supplied_receipts(
    *,
    endpoint_receipt: Mapping[str, Any],
    endpoint_source_sha256: str,
    identity_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Purely validate/compose supplied receipts; never perform observation."""
    semantic = _validate_semantic_contract()

    _require(
        identity_receipt.get("collector_contract_sha256")
        == LIVE_IDENTITY_COLLECTOR_SEMANTIC_SHA256,
        "identity receipt semantic collector-contract binding mismatch",
    )

    endpoint = validate_endpoint_liveness_receipt(
        endpoint_receipt,
        expected_source_sha256=endpoint_source_sha256,
    )
    identity = identity_receipt_validator.validate_v2r13_runtime_identity_receipt(
        identity_receipt
    )

    _require(
        identity.get("expected_identity_values_match") is True,
        "identity receipt expected values do not match",
    )
    _require(
        identity.get("collector_identity_admitted") is False,
        "identity receipt unexpectedly admits collector identity",
    )
    _require(
        identity.get("model_identity_verified") is False,
        "identity receipt unexpectedly verifies model identity",
    )
    _require(
        identity.get("runtime_image_identity_verified") is False,
        "identity receipt unexpectedly verifies runtime image identity",
    )

    return {
        "schema": CANDIDATE_SCHEMA,
        "snapshot_id": activation_contract.V2R13,
        "collector_contract_sha256": LIVE_IDENTITY_COLLECTOR_SEMANTIC_SHA256,
        "semantic_contract_valid": semantic["semantic_contract_valid"],
        "endpoint_source_sha256": endpoint_source_sha256,
        "identity_receipt_collector_contract_sha256": (
            identity["collector_contract_sha256"]
        ),
        "supplied_endpoint_liveness_observed": True,
        "supplied_identity_values_match": True,
        "expected_model_alias": identity["active_model_alias"],
        "expected_model_digest": identity["active_model_digest"],
        "expected_runtime_image_id": identity["runtime_image_id"],
        "endpoint_receipt_validation": deepcopy(endpoint),
        "identity_receipt_validation": deepcopy(identity),
        "collector_implementation_source_binding_admitted": False,
        "collector_identity_admitted": False,
        "endpoint_liveness_verified": False,
        "model_identity_verified": False,
        "runtime_image_identity_verified": False,
        "supported_primitive_count_remains": 13,
        "remaining_unresolved_primitive_count_remains": 3,
        "remaining_unresolved_primitive_names": (
            "endpoint_liveness",
            "model_identity_verified",
            "runtime_image_identity_verified",
        ),
        "canonical_provider_binding_present": False,
        "canonical_collection_enabled": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "live_observation_performed": False,
        "host_backend_invoked": False,
        "http_request_performed": False,
        "systemd_query_performed": False,
        "subprocess_execution_performed": False,
        "model_inference_performed": False,
    }


def v2r13_live_identity_collector_implementation_contract() -> dict[str, Any]:
    semantic = _validate_semantic_contract()
    return {
        "schema": CONTRACT_SCHEMA,
        "live_identity_collector_contract_git_blob": (
            LIVE_IDENTITY_COLLECTOR_CONTRACT_GIT_BLOB
        ),
        "identity_receipt_validator_git_blob": IDENTITY_RECEIPT_VALIDATOR_GIT_BLOB,
        "activation_contract_git_blob": ACTIVATION_CONTRACT_GIT_BLOB,
        "live_identity_collector_semantic_sha256": (
            LIVE_IDENTITY_COLLECTOR_SEMANTIC_SHA256
        ),
        "semantic_contract_valid": semantic["semantic_contract_valid"],
        "supplied_endpoint_receipt_validator_implemented": True,
        "supplied_identity_receipt_validator_reused": True,
        "supplied_receipt_composition_implemented": True,
        "endpoint_receipt_source_binding_enforced": True,
        "identity_receipt_semantic_contract_binding_enforced": True,
        "automatic_host_backend_selection": False,
        "host_backend_implementation_present": False,
        "live_collection_implemented": False,
        "canonical_implementation_source_binding_present": False,
        "canonical_collection_enabled": False,
        "collector_identity_admission_implemented": False,
        "endpoint_liveness_provider_primitive_implemented": False,
        "model_identity_provider_primitive_implemented": False,
        "runtime_image_provider_primitive_implemented": False,
        "supported_primitive_count_remains": 13,
        "remaining_unresolved_primitive_count_remains": 3,
        "remaining_unresolved_primitive_names": (
            "endpoint_liveness",
            "model_identity_verified",
            "runtime_image_identity_verified",
        ),
        "filesystem_observation_implemented": False,
        "external_git_query_implemented": False,
        "path_resolution_implemented": False,
        "subprocess_execution_implemented": False,
        "http_request_implemented": False,
        "endpoint_probe_implemented": False,
        "systemd_query_implemented": False,
        "service_action_implemented": False,
        "runtime_start_stop_reload_implemented": False,
        "model_load_implemented": False,
        "model_inference_implemented": False,
        "canonical_provider_binding_present": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
    }


def collect_v2r13_live_identity(*args: Any, **kwargs: Any) -> None:
    """Always hold: this source does not implement live collection."""
    _require(
        CANONICAL_IMPLEMENTATION_SOURCE_BINDING_PRESENT is True,
        "GENERATION2_V2R13_CANONICAL_IMPLEMENTATION_SOURCE_BINDING_NOT_PRESENT",
    )
    _require(
        CANONICAL_COLLECTION_ENABLED is True,
        "GENERATION2_V2R13_CANONICAL_COLLECTION_NOT_ENABLED",
    )
    raise RuntimeV2R13LiveIdentityCollectorImplementationHold(
        "GENERATION2_V2R13_LIVE_IDENTITY_COLLECTION_NOT_IMPLEMENTED"
    )
