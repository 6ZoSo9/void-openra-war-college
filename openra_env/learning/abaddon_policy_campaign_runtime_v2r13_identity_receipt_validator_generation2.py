"""Source-only V2R13 runtime-identity receipt validator for Generation-2.

This module validates the shape and expected identity values of an already-
supplied read-only runtime-identity observation receipt.

It deliberately does NOT turn a self-reported receipt into admitted live
identity proof.  Until a separately reviewed collector contract is canonically
bound, the validator returns:

* ``expected_identity_values_match = true`` for an exact supplied receipt;
* ``collector_identity_admitted = false``;
* ``model_identity_verified = false``;
* ``runtime_image_identity_verified = false``.

The receipt may claim that a collector observed the active model and runtime
image, but this source never performs collection itself and never admits the
collector solely because it supplied a SHA-256 string.

No filesystem access, Git query, path resolution, subprocess execution,
endpoint/systemd probe, model load/inference, service action, runtime start,
game execution, training, deployment, VOID-chain mutation, or funds action
occurs in this module.
"""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_activation_contract_generation2
    as activation_contract,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-runtime-identity-receipt-validator-contract.v1"
)
RECEIPT_SCHEMA = (
    "void.abaddon.generation2.v2r13-runtime-identity-observation-receipt.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2.v2r13-runtime-identity-receipt-validation.v1"
)

ACTIVATION_CONTRACT_GIT_BLOB = "a3acb42280c334daa24a3b830105a04666fd603b"
ACTIVATION_EVIDENCE_GIT_BLOB = "aac7964d9e80633535003b9f27066cac1bb4bac2"
RUNTIME_REALIZATIONS_GIT_BLOB = "0dbae61b0be96445e5fd6c23a07491a03f18b679"

EXPECTED_MODEL_ALIAS = activation_contract.V2R13_MODEL_ALIAS
EXPECTED_MODEL_DIGEST = activation_contract.V2R13_MODEL_DIGEST
EXPECTED_RUNTIME_IMAGE_ID = activation_contract.V2R13_RUNTIME_IMAGE_ID

SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")

RECEIPT_FIELDS = (
    "schema",
    "snapshot_id",
    "observation_mode",
    "collector_contract_sha256",
    "active_model_alias",
    "active_model_digest",
    "runtime_image_id",
    "model_identity_observation_performed",
    "runtime_image_identity_observation_performed",
    "mutation_performed",
    "service_action_performed",
    "runtime_start_performed",
    "model_load_performed",
    "model_inference_performed",
    "game_execution_performed",
    "training_performed",
    "weights_updated",
    "deployment_performed",
)


class RuntimeV2R13IdentityReceiptValidatorHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13IdentityReceiptValidatorHold(message)


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and SHA256_RE.fullmatch(value) is not None


def validate_v2r13_runtime_identity_receipt(
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate supplied identity values without admitting collector identity."""
    _require(
        isinstance(receipt, Mapping),
        "V2R13 runtime identity receipt must be object",
    )
    actual = set(receipt)
    expected = set(RECEIPT_FIELDS)
    _require(
        actual == expected,
        "V2R13 runtime identity receipt field-set drift: "
        f"missing={sorted(expected - actual)!r} "
        f"extra={sorted(actual - expected)!r}",
    )

    _require(
        receipt.get("schema") == RECEIPT_SCHEMA,
        "V2R13 runtime identity receipt schema drift",
    )
    _require(
        receipt.get("snapshot_id") == activation_contract.V2R13,
        "V2R13 runtime identity snapshot drift",
    )
    _require(
        receipt.get("observation_mode") == "read_only",
        "V2R13 runtime identity observation mode must be read_only",
    )
    _require(
        _is_sha256(receipt.get("collector_contract_sha256")),
        "V2R13 runtime identity collector contract SHA malformed",
    )

    _require(
        receipt.get("active_model_alias") == EXPECTED_MODEL_ALIAS,
        "V2R13 active model alias drift",
    )
    _require(
        receipt.get("active_model_digest") == EXPECTED_MODEL_DIGEST,
        "V2R13 active model digest drift",
    )
    _require(
        receipt.get("runtime_image_id") == EXPECTED_RUNTIME_IMAGE_ID,
        "V2R13 runtime image identity drift",
    )

    _require(
        receipt.get("model_identity_observation_performed") is True,
        "V2R13 model identity observation not claimed",
    )
    _require(
        receipt.get("runtime_image_identity_observation_performed") is True,
        "V2R13 runtime image observation not claimed",
    )

    for field in (
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "deployment_performed",
    ):
        _require(
            receipt.get(field) is False,
            f"V2R13 runtime identity receipt crossed boundary: {field}",
        )

    return {
        "schema": VALIDATION_SCHEMA,
        "snapshot_id": activation_contract.V2R13,
        "receipt_shape_valid": True,
        "expected_identity_values_match": True,
        "active_model_alias": EXPECTED_MODEL_ALIAS,
        "active_model_digest": EXPECTED_MODEL_DIGEST,
        "runtime_image_id": EXPECTED_RUNTIME_IMAGE_ID,
        "model_identity_observation_claimed": True,
        "runtime_image_identity_observation_claimed": True,
        "collector_contract_sha256": receipt["collector_contract_sha256"],
        "collector_identity_admitted": False,
        "model_identity_verified": False,
        "runtime_image_identity_verified": False,
        "canonical_provider_binding_present": False,
        "canonical_collection_enabled": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "validator_collection_performed": False,
        "validator_filesystem_observation_performed": False,
        "validator_external_worktree_git_query_performed": False,
        "validator_path_resolution_performed": False,
        "validator_subprocess_execution_performed": False,
        "validator_endpoint_probe_performed": False,
        "validator_systemd_query_performed": False,
        "validator_model_load_performed": False,
        "validator_model_inference_performed": False,
        "validated_receipt": deepcopy(dict(receipt)),
    }


def v2r13_runtime_identity_receipt_validator_contract() -> dict[str, Any]:
    return {
        "schema": CONTRACT_SCHEMA,
        "activation_contract_git_blob": ACTIVATION_CONTRACT_GIT_BLOB,
        "activation_evidence_git_blob": ACTIVATION_EVIDENCE_GIT_BLOB,
        "runtime_realizations_git_blob": RUNTIME_REALIZATIONS_GIT_BLOB,
        "snapshot_id": activation_contract.V2R13,
        "expected_model_alias": EXPECTED_MODEL_ALIAS,
        "expected_model_digest": EXPECTED_MODEL_DIGEST,
        "expected_runtime_image_id": EXPECTED_RUNTIME_IMAGE_ID,
        "supplied_receipt_shape_validator_implemented": True,
        "collector_contract_binding_required_for_identity_admission": True,
        "self_reported_collector_sha_is_sufficient": False,
        "model_identity_provider_primitive_implemented": False,
        "runtime_image_provider_primitive_implemented": False,
        "supported_primitive_count_remains": 13,
        "remaining_unresolved_primitive_count_remains": 3,
        "remaining_unresolved_primitive_names": (
            "endpoint_liveness",
            "model_identity_verified",
            "runtime_image_identity_verified",
        ),
        "live_collection_implemented": False,
        "validator_filesystem_observation_implemented": False,
        "validator_git_query_implemented": False,
        "validator_path_resolution_implemented": False,
        "validator_subprocess_execution_implemented": False,
        "validator_endpoint_probe_implemented": False,
        "validator_systemd_query_implemented": False,
        "canonical_provider_binding_present": False,
        "canonical_collection_enabled": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
    }


def collect_live_v2r13_runtime_identity(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13IdentityReceiptValidatorHold(
        "GENERATION2_V2R13_LIVE_RUNTIME_IDENTITY_COLLECTION_NOT_IMPLEMENTED"
    )
