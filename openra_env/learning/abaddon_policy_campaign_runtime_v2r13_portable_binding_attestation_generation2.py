"""Source-only V2R13 portable-binding attestation validator for Generation-2.

This module validates an already-produced ``PortableRunnerBinding.attestation()``
receipt.  It does not install a binding, load the base runner, touch paths, query
Git, inspect the filesystem, or invoke any host/runtime surface.

Only the *fully bound* canonical attestation is accepted:

* ``legacy_source_root_bound = true``
* ``legacy_engine_root_bound = true``
* ``base_loaded_and_bound = true``
* runtime/model/game execution flags remain false

The canonical attestation SHA-256 is recomputed from the exact reviewed body.
A pre-base-load attestation is deliberately rejected because it proves only the
legacy-module rebinding, not the loaded base-runner rebinding required for the
full portable-binding claim.

Validation does not create a canonical primitive-provider binding and does not
admit runtime readiness.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import apollyon_v2r13_portable_checkout as portable_checkout

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-portable-binding-attestation-contract.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2.v2r13-portable-binding-attestation-validation.v1"
)

PORTABLE_CHECKOUT_GIT_BLOB = "077fbf5a2847d85113eb8fcba3904b02343ebfef"
PORTABLE_CHECKOUT_SOURCE_SHA256 = (
    "92e16e281d5a9036d78d900f35d854c6fb9783b2bf156c2acab69408d13a015d"
)
PORTABLE_BINDING_CONTRACT_SHA256 = (
    "677e503e8d4827a9d8950a177f308ad08982f612d70881f16de2c271e3b10e49"
)
FULLY_BOUND_ATTESTATION_SHA256 = (
    "2235940543056b6c9154989c6d124362a524c3702de07b75f1654922525203f5"
)

ATTESTATION_FIELDS = (
    "schema",
    "legacy_source_root_bound",
    "legacy_engine_root_bound",
    "base_loaded_and_bound",
    "runtime_execution_performed",
    "model_execution_performed",
    "game_started",
    "attestation_sha256",
)

ATTESTATION_BODY_FIELDS = ATTESTATION_FIELDS[:-1]


class RuntimeV2R13PortableBindingAttestationHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13PortableBindingAttestationHold(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _sha256(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


def _validate_static_contract_binding() -> dict[str, Any]:
    contract = portable_checkout.portable_binding_contract()
    _require(
        contract.get("binding_contract_sha256")
        == PORTABLE_BINDING_CONTRACT_SHA256,
        "portable binding contract SHA drift",
    )
    _require(
        contract.get("runtime_execution_performed") is False,
        "portable binding contract runtime boundary drift",
    )
    _require(
        contract.get("model_execution_performed") is False,
        "portable binding contract model boundary drift",
    )
    _require(
        contract.get("game_started") is False,
        "portable binding contract game boundary drift",
    )
    return contract


def validate_v2r13_portable_binding_attestation(
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate one supplied fully-bound portable-binding attestation."""
    _validate_static_contract_binding()
    _require(
        isinstance(receipt, Mapping),
        "portable binding attestation must be object",
    )

    actual_fields = set(receipt)
    expected_fields = set(ATTESTATION_FIELDS)
    _require(
        actual_fields == expected_fields,
        "portable binding attestation field-set drift: "
        f"missing={sorted(expected_fields - actual_fields)!r} "
        f"extra={sorted(actual_fields - expected_fields)!r}",
    )

    _require(
        receipt.get("schema") == portable_checkout.BINDING_SCHEMA,
        "portable binding attestation schema drift",
    )

    _require(
        receipt.get("legacy_source_root_bound") is True,
        "portable binding legacy source root not bound",
    )
    _require(
        receipt.get("legacy_engine_root_bound") is True,
        "portable binding legacy engine root not bound",
    )
    _require(
        receipt.get("base_loaded_and_bound") is True,
        "portable binding base runner not loaded and bound",
    )

    for field in (
        "runtime_execution_performed",
        "model_execution_performed",
        "game_started",
    ):
        _require(
            receipt.get(field) is False,
            f"portable binding attestation crossed boundary: {field}",
        )

    body = {
        field: deepcopy(receipt[field])
        for field in ATTESTATION_BODY_FIELDS
    }
    expected_sha = _sha256(body)
    supplied_sha = receipt.get("attestation_sha256")
    _require(
        isinstance(supplied_sha, str),
        "portable binding attestation SHA malformed",
    )
    _require(
        supplied_sha == expected_sha,
        "portable binding attestation SHA mismatch",
    )
    _require(
        supplied_sha == FULLY_BOUND_ATTESTATION_SHA256,
        "portable binding fully-bound attestation identity drift",
    )

    return {
        "schema": VALIDATION_SCHEMA,
        "supplied_attestation_valid": True,
        "supplied_attestation_sha256": supplied_sha,
        "portable_binding_fully_attested": True,
        "legacy_source_root_bound": True,
        "legacy_engine_root_bound": True,
        "base_loaded_and_bound": True,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_started": False,
        "validator_filesystem_observation_performed": False,
        "validator_external_worktree_git_query_performed": False,
        "validator_path_resolution_performed": False,
        "validator_binding_install_performed": False,
        "validator_base_load_performed": False,
        "validator_observer_invocation_performed": False,
        "validator_host_backend_invocation_performed": False,
        "canonical_provider_binding_present": False,
        "canonical_collection_enabled": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "validated_receipt": deepcopy(dict(receipt)),
    }


def v2r13_portable_binding_attestation_contract() -> dict[str, Any]:
    _validate_static_contract_binding()
    return {
        "schema": CONTRACT_SCHEMA,
        "portable_checkout_git_blob": PORTABLE_CHECKOUT_GIT_BLOB,
        "portable_checkout_source_sha256": PORTABLE_CHECKOUT_SOURCE_SHA256,
        "portable_binding_contract_sha256": PORTABLE_BINDING_CONTRACT_SHA256,
        "fully_bound_attestation_sha256": FULLY_BOUND_ATTESTATION_SHA256,
        "supplied_attestation_validator_implemented": True,
        "full_legacy_source_binding_required": True,
        "full_legacy_engine_binding_required": True,
        "full_base_binding_required": True,
        "pre_base_load_attestation_admitted": False,
        "live_binding_install_implemented": False,
        "live_base_load_implemented": False,
        "validator_filesystem_observation_implemented": False,
        "validator_git_query_implemented": False,
        "validator_path_resolution_implemented": False,
        "validator_observer_invocation_implemented": False,
        "validator_host_backend_invocation_implemented": False,
        "canonical_provider_binding_present": False,
        "canonical_collection_enabled": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
    }


def validate_live_binding_state(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13PortableBindingAttestationHold(
        "GENERATION2_V2R13_LIVE_PORTABLE_BINDING_VALIDATION_NOT_IMPLEMENTED"
    )
