"""Pure source/supplied-fact progress for Generation-2 activation evidence.

This module closes only evidence-shape gaps that canonical pure functions can
support without live observation.

V8:
* static reviewed runtime identity fields are copied from the canonical
  activation-evidence requirement;
* a caller-supplied Python/package identity fact can be validated with the
  already-reviewed pure ``validate_v8_runtime_environment`` function;
* that validation may support the shape value
  ``runtime_environment_verified=True`` while collector provenance remains
  explicitly unadmitted.

V2R13:
* a caller-supplied portable-binding contract can be checked against the pure
  canonical ``portable_binding_contract``;
* this proves contract identity only.  It never claims that a live portable
  binding was installed, so ``portable_binding_attested`` remains unresolved.

No filesystem access, Git command, subprocess, environment read, pip freeze,
endpoint/systemd probe, observer invocation, host backend call, model load,
worktree creation, runtime/game/model execution, training, weight update,
promotion, deployment, VOID-chain mutation, or funds action occurs here.
"""

from __future__ import annotations

from typing import Any, Mapping

from openra_env.learning import apollyon_v2r13_portable_checkout as v2_portable
from openra_env.learning import apollyon_v8_campaign_runtime as v8_runtime
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    RUNTIME_AUTHORITY_BLOCKER,
    V2R13,
    V8,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_evidence_generation2 import (
    evidence_requirement,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.runtime-evidence-shape-progress-contract.v1"
)
FACT_SCHEMA = "void.abaddon.generation2.runtime-supplied-evidence-fact.v1"
VALIDATION_SCHEMA = (
    "void.abaddon.generation2.runtime-supplied-evidence-fact-validation.v1"
)
PROGRESS_SCHEMA = "void.abaddon.generation2.runtime-evidence-shape-progress.v1"

V8_ENVIRONMENT_FACT_KIND = "v8_runtime_environment_identity"
V2R13_PORTABLE_CONTRACT_FACT_KIND = "v2r13_portable_binding_contract_identity"

OBSERVER_COMPOSITION_SOURCE_SHA256 = (
    "dbadd47bd5bf7354754220505857e881b9dea52989569d65669d90415cff0d9d"
)
OBSERVER_COMPOSITION_GIT_BLOB = "d069a0a1486b9531d084044d4de19e80893f7dfe"
V8_RUNTIME_GIT_BLOB = "fd0e72767ba199e88af9e9eb2455c03ace027a14"
V2R13_PORTABLE_GIT_BLOB = "077fbf5a2847d85113eb8fcba3904b02343ebfef"
ACTIVATION_EVIDENCE_GIT_BLOB = "aac7964d9e80633535003b9f27066cac1bb4bac2"

FACT_SOURCE = "supplied_external_fact"

V8_ENVIRONMENT_FACT_FIELDS = (
    "schema",
    "snapshot_id",
    "fact_kind",
    "python_major_minor",
    "pip_freeze_sha256",
    "fact_source",
    "live_collection_performed",
    "collector_identity_admitted",
    "runtime_execution_performed",
    "model_execution_performed",
)

V2R13_PORTABLE_CONTRACT_FACT_FIELDS = (
    "schema",
    "snapshot_id",
    "fact_kind",
    "binding_contract",
    "fact_source",
    "live_binding_installation_attested",
    "collector_identity_admitted",
    "runtime_execution_performed",
    "model_execution_performed",
    "game_execution_performed",
)


class RuntimeEvidenceShapeProgressHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeEvidenceShapeProgressHold(message)


def _require_exact_fields(
    record: Mapping[str, Any],
    fields: tuple[str, ...],
    label: str,
) -> None:
    actual = set(record)
    expected = set(fields)
    _require(
        actual == expected,
        f"{label} field set drift: "
        f"missing={sorted(expected - actual)!r} "
        f"extra={sorted(actual - expected)!r}",
    )


def _require_false(record: Mapping[str, Any], fields: tuple[str, ...]) -> None:
    for field in fields:
        _require(
            record.get(field) is False,
            f"supplied fact crossed authority boundary: {field}",
        )


def _require_python_major_minor(value: Any) -> tuple[int, int]:
    _require(
        isinstance(value, (list, tuple)) and len(value) == 2,
        "V8 python_major_minor must contain exactly two integers",
    )
    major, minor = value
    _require(
        type(major) is int and type(minor) is int,
        "V8 python_major_minor values must be integers",
    )
    return major, minor


def validate_v8_environment_fact(record: Mapping[str, Any]) -> dict[str, Any]:
    """Validate supplied V8 interpreter/package identity using only pure logic."""
    _require(isinstance(record, Mapping), "V8 environment fact must be object")
    _require_exact_fields(
        record,
        V8_ENVIRONMENT_FACT_FIELDS,
        "V8 environment fact",
    )
    _require(record.get("schema") == FACT_SCHEMA, "V8 environment fact schema drift")
    _require(record.get("snapshot_id") == V8, "V8 environment fact snapshot drift")
    _require(
        record.get("fact_kind") == V8_ENVIRONMENT_FACT_KIND,
        "V8 environment fact kind drift",
    )
    _require(
        record.get("fact_source") == FACT_SOURCE,
        "V8 environment fact source drift",
    )
    _require_false(
        record,
        (
            "live_collection_performed",
            "collector_identity_admitted",
            "runtime_execution_performed",
            "model_execution_performed",
        ),
    )

    python_major_minor = _require_python_major_minor(
        record.get("python_major_minor")
    )
    result = v8_runtime.validate_v8_runtime_environment(
        python_major_minor=python_major_minor,
        pip_freeze_sha256=record.get("pip_freeze_sha256"),
    )
    _require(
        result.get("python_major_minor") == list(v8_runtime.RUNTIME_PYTHON_MAJOR_MINOR),
        "V8 canonical environment validator Python identity drift",
    )
    _require(
        result.get("pip_freeze_sha256") == v8_runtime.RUNTIME_PIP_FREEZE_SHA256,
        "V8 canonical environment validator package identity drift",
    )
    _require(
        result.get("runtime_execution_performed") is False,
        "V8 environment validation crossed runtime boundary",
    )
    _require(
        result.get("model_execution_performed") is False,
        "V8 environment validation crossed model boundary",
    )

    return {
        "schema": VALIDATION_SCHEMA,
        "snapshot_id": V8,
        "fact_kind": V8_ENVIRONMENT_FACT_KIND,
        "supplied_fact_shape_valid": True,
        "canonical_pure_validator_applied": True,
        "environment_identity_values_valid": True,
        "live_environment_collection_proven": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "activation_evidence_shape_field_support": {
            "runtime_environment_verified": True,
        },
        "holds": [
            "V8_RUNTIME_ENVIRONMENT_FACT_PROVENANCE_UNADMITTED",
            RUNTIME_AUTHORITY_BLOCKER,
        ],
    }


def v8_evidence_shape_progress(
    environment_fact: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return V8 shape progress without producing final activation evidence."""
    requirement = evidence_requirement(V8)
    expected = dict(requirement["expected"])

    supplied_fields: dict[str, Any] = {}
    holds = [
        "V8_COLLECTOR_CONTRACT_IDENTITY_UNRESOLVED",
        "V8_OFFLINE_ONLY_EVIDENCE_UNRESOLVED",
        "V8_LOAD_CALL_EVIDENCE_UNRESOLVED",
        RUNTIME_AUTHORITY_BLOCKER,
    ]

    if environment_fact is not None:
        validation = validate_v8_environment_fact(environment_fact)
        _require(
            validation["environment_identity_values_valid"] is True,
            "V8 environment identity validation did not close shape field",
        )
        supplied_fields["runtime_environment_verified"] = True
        holds.insert(0, "V8_RUNTIME_ENVIRONMENT_FACT_PROVENANCE_UNADMITTED")

    unresolved = [
        "collector_contract_sha256",
        "model_dir",
        "adapter_dir",
        "model_dir_bound",
        "adapter_dir_bound",
        "runtime_assets_verified",
        "offline_only_verified",
        "model_weights_loaded",
        "load_call_performed",
    ]
    if environment_fact is None:
        unresolved.append("runtime_environment_verified")

    return {
        "schema": PROGRESS_SCHEMA,
        "snapshot_id": V8,
        "source_static_activation_evidence_fields": expected,
        "supplied_fact_activation_evidence_fields": supplied_fields,
        "unresolved_activation_evidence_fields": tuple(unresolved),
        "activation_evidence_shape_complete": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "live_observation_performed": False,
        "pip_freeze_performed": False,
        "model_weights_loaded": False,
        "runtime_execution_authorized": False,
        "holds": holds,
    }


def validate_v2r13_portable_contract_fact(
    record: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate supplied portable-contract identity, not live installation."""
    _require(
        isinstance(record, Mapping),
        "V2R13 portable contract fact must be object",
    )
    _require_exact_fields(
        record,
        V2R13_PORTABLE_CONTRACT_FACT_FIELDS,
        "V2R13 portable contract fact",
    )
    _require(
        record.get("schema") == FACT_SCHEMA,
        "V2R13 portable contract fact schema drift",
    )
    _require(
        record.get("snapshot_id") == V2R13,
        "V2R13 portable contract fact snapshot drift",
    )
    _require(
        record.get("fact_kind") == V2R13_PORTABLE_CONTRACT_FACT_KIND,
        "V2R13 portable contract fact kind drift",
    )
    _require(
        record.get("fact_source") == FACT_SOURCE,
        "V2R13 portable contract fact source drift",
    )
    _require_false(
        record,
        (
            "live_binding_installation_attested",
            "collector_identity_admitted",
            "runtime_execution_performed",
            "model_execution_performed",
            "game_execution_performed",
        ),
    )

    canonical = v2_portable.portable_binding_contract()
    supplied = record.get("binding_contract")
    _require(
        isinstance(supplied, Mapping),
        "V2R13 portable binding contract missing",
    )
    _require(
        dict(supplied) == canonical,
        "V2R13 portable binding contract identity drift",
    )

    return {
        "schema": VALIDATION_SCHEMA,
        "snapshot_id": V2R13,
        "fact_kind": V2R13_PORTABLE_CONTRACT_FACT_KIND,
        "supplied_fact_shape_valid": True,
        "canonical_pure_contract_applied": True,
        "portable_contract_identity_valid": True,
        "live_binding_installation_attested": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "activation_evidence_shape_field_support": {},
        "holds": [
            "V2R13_PORTABLE_BINDING_LIVE_ATTESTATION_UNRESOLVED",
            RUNTIME_AUTHORITY_BLOCKER,
        ],
    }


def v2r13_evidence_shape_progress(
    portable_contract_fact: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Bind V2R13 static expectations without claiming live runtime facts."""
    requirement = evidence_requirement(V2R13)
    expected = dict(requirement["expected"])

    contract_identity_valid = False
    holds = [
        "V2R13_PORTABLE_BINDING_LIVE_ATTESTATION_UNRESOLVED",
        "V2R13_ENDPOINT_EVIDENCE_UNRESOLVED",
        "V2R13_MODEL_IDENTITY_EVIDENCE_UNRESOLVED",
        "V2R13_RUNTIME_IMAGE_IDENTITY_EVIDENCE_UNRESOLVED",
        "V2R13_COLLECTOR_CONTRACT_IDENTITY_UNRESOLVED",
        RUNTIME_AUTHORITY_BLOCKER,
    ]

    if portable_contract_fact is not None:
        validation = validate_v2r13_portable_contract_fact(
            portable_contract_fact
        )
        contract_identity_valid = validation["portable_contract_identity_valid"]

    return {
        "schema": PROGRESS_SCHEMA,
        "snapshot_id": V2R13,
        "expected_static_reference_fields": expected,
        "portable_contract_identity_valid": contract_identity_valid,
        "portable_binding_attested": False,
        "supported_activation_evidence_fields": {},
        "unresolved_activation_evidence_fields": (
            "collector_contract_sha256",
            "endpoint_liveness",
            "active_model_alias",
            "active_model_digest",
            "model_identity_verified",
            "runtime_image_id",
            "runtime_image_identity_verified",
            "frozen_source_worktree",
            "engine_worktree",
            "portable_binding_attested",
        ),
        "activation_evidence_shape_complete": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "live_observation_performed": False,
        "runtime_execution_authorized": False,
        "holds": holds,
    }


def evidence_shape_progress_contract() -> dict[str, Any]:
    """Return the exact no-collection evidence-shape progress boundary."""
    return {
        "schema": CONTRACT_SCHEMA,
        "observer_composition_source_sha256":
            OBSERVER_COMPOSITION_SOURCE_SHA256,
        "observer_composition_git_blob": OBSERVER_COMPOSITION_GIT_BLOB,
        "v8_runtime_git_blob": V8_RUNTIME_GIT_BLOB,
        "v2r13_portable_git_blob": V2R13_PORTABLE_GIT_BLOB,
        "activation_evidence_git_blob": ACTIVATION_EVIDENCE_GIT_BLOB,
        "v8_static_identity_shape_composition_implemented": True,
        "v8_supplied_environment_fact_validation_implemented": True,
        "v8_live_environment_collection_implemented": False,
        "v8_environment_collector_provenance_admitted": False,
        "v2r13_portable_contract_identity_validation_implemented": True,
        "v2r13_live_portable_binding_attestation_implemented": False,
        "final_activation_evidence_shape_composition_implemented": False,
        "collector_identity_admission_implemented": False,
        "runtime_readiness_admission_implemented": False,
        "live_observation_performed": False,
        "pip_freeze_performed": False,
        "observer_invocation_performed": False,
        "runtime_execution_authorized": False,
    }


def collect_evidence_shape_progress(*args: Any, **kwargs: Any) -> None:
    """Always hold: this module validates supplied facts and never collects."""
    raise RuntimeEvidenceShapeProgressHold(
        "GENERATION2_EVIDENCE_SHAPE_PROGRESS_COLLECTION_NOT_IMPLEMENTED"
    )
