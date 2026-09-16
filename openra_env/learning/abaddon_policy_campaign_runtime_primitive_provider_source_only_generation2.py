"""Zero-I/O partial primitive provider for Abaddon Generation-2.

This module implements only primitive values that are already justified without
live host observation:

* the six common collector self-audits for every reviewed snapshot;
* V8 ``load_call_performed = false``;
* validation of an explicitly supplied V8 interpreter/package identity through
  the already-reviewed pure validator.

It intentionally does NOT implement:

* endpoint liveness;
* V14/V10 live model identity;
* V14/V10 runtime-unit identity;
* V2R13 live model digest identity;
* V2R13 runtime-image identity;
* V2R13 source/engine path-classification leaves;
* V2R13 portable-binding attestation;
* V8 live ``pip freeze`` collection;
* V8 offline-only attestation.

The V2R13 reviewed Git observer proves exact Git identity, cleanliness, detached
source state, and path identity, but its returned receipt does not itself contain
the six ``exists/is_directory/is_symlink`` leaves required by activation
evidence.  This module therefore refuses to infer those leaves.

No filesystem access, Git command, subprocess, HTTP/systemd probe, observer or
host-backend invocation, model load, runtime/game/model execution, training,
promotion, deployment, VOID-chain mutation, or funds action occurs.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import apollyon_v8_campaign_runtime as v8_runtime
from openra_env.learning import (
    abaddon_policy_campaign_runtime_primitive_provider_contract_generation2
    as provider_contract,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    V10,
    V14,
    V2R13,
    V8,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.runtime-primitive-provider-source-only.v1"
)
PROGRESS_SCHEMA = (
    "void.abaddon.generation2.runtime-primitive-provider-progress.v1"
)
V8_SUPPLIED_ENVIRONMENT_SCHEMA = (
    "void.abaddon.generation2.runtime-v8-supplied-environment-fact.v1"
)

PROVIDER_CONTRACT_GIT_BLOB = "807335ae5ee2892917d02acfa6434fd65151960f"
PROVIDER_CONTRACT_SEMANTIC_SHA256 = (
    "58e84a058c332de983ccaef19bd1383a92071966b653e699d032c9e9e86c1114"
)
V8_RUNTIME_GIT_BLOB = "fd0e72767ba199e88af9e9eb2455c03ace027a14"

COMMON_SELF_AUDIT_VALUES = {
    "observation_mode": "read_only",
    "mutation_performed": False,
    "service_action_performed": False,
    "runtime_start_performed": False,
    "game_execution_performed": False,
    "model_inference_performed": False,
}

V14_UNRESOLVED = (
    "endpoint_liveness",
    "model_identity_verified",
    "runtime_unit_identity_verified",
)

V10_UNRESOLVED = V14_UNRESOLVED

V2R13_UNRESOLVED = (
    "endpoint_liveness",
    "model_identity_verified",
    "runtime_image_identity_verified",
    "frozen_source_worktree.exists",
    "frozen_source_worktree.is_directory",
    "frozen_source_worktree.is_symlink",
    "engine_worktree.exists",
    "engine_worktree.is_directory",
    "engine_worktree.is_symlink",
    "portable_binding_attested",
)

V8_UNRESOLVED_WITH_SUPPLIED_ENVIRONMENT = (
    "offline_only_verified",
)

V8_UNRESOLVED_WITHOUT_SUPPLIED_ENVIRONMENT = (
    "runtime_environment_verified",
    "offline_only_verified",
)


class RuntimePrimitiveProviderSourceOnlyHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimePrimitiveProviderSourceOnlyHold(message)


def _validate_contract_binding() -> dict[str, Any]:
    out = provider_contract.validate_provider_contract()
    _require(
        out.get("provider_contract_sha256")
        == PROVIDER_CONTRACT_SEMANTIC_SHA256,
        "provider contract semantic SHA drift",
    )
    _require(
        out.get("canonical_provider_bindings_present") is False,
        "canonical provider bindings unexpectedly present",
    )
    _require(
        out.get("canonical_collection_enabled") is False,
        "canonical collection unexpectedly enabled",
    )
    _require(
        out.get("reviewed_collector_binding_present") is False,
        "reviewed collector binding unexpectedly present",
    )
    _require(
        out.get("runtime_readiness_admission_enabled") is False,
        "runtime readiness admission unexpectedly enabled",
    )
    _require(
        out.get("runtime_execution_authorized") is False,
        "runtime execution unexpectedly authorized",
    )
    return out


def source_only_self_audit_values(snapshot_id: str) -> dict[str, Any]:
    """Return only values justified by this non-observing source itself."""
    _validate_contract_binding()
    _require(
        snapshot_id in {V14, V10, V2R13, V8},
        f"unsupported source-only provider snapshot: {snapshot_id!r}",
    )

    values = deepcopy(COMMON_SELF_AUDIT_VALUES)
    if snapshot_id == V8:
        values["load_call_performed"] = False
    return values


def validate_v8_supplied_environment_fact(
    record: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate supplied V8 environment identity without collecting it."""
    _validate_contract_binding()
    _require(isinstance(record, Mapping), "V8 environment fact must be object")
    _require(
        set(record)
        == {
            "schema",
            "python_major_minor",
            "pip_freeze_sha256",
            "collection_performed",
            "filesystem_observation_performed",
            "subprocess_execution_performed",
            "runtime_execution_performed",
            "model_execution_performed",
            "game_execution_performed",
        },
        "V8 environment fact field-set drift",
    )
    _require(
        record.get("schema") == V8_SUPPLIED_ENVIRONMENT_SCHEMA,
        "V8 environment fact schema drift",
    )

    python_major_minor = record.get("python_major_minor")
    _require(
        isinstance(python_major_minor, (list, tuple))
        and len(python_major_minor) == 2
        and all(type(value) is int for value in python_major_minor),
        "V8 environment python identity malformed",
    )

    pip_freeze_sha256 = record.get("pip_freeze_sha256")
    _require(
        isinstance(pip_freeze_sha256, str),
        "V8 environment pip-freeze SHA malformed",
    )

    for field in (
        "collection_performed",
        "filesystem_observation_performed",
        "subprocess_execution_performed",
        "runtime_execution_performed",
        "model_execution_performed",
        "game_execution_performed",
    ):
        _require(
            record.get(field) is False,
            f"V8 supplied environment fact crossed boundary: {field}",
        )

    validated = v8_runtime.validate_v8_runtime_environment(
        python_major_minor=(
            python_major_minor[0],
            python_major_minor[1],
        ),
        pip_freeze_sha256=pip_freeze_sha256,
    )

    _require(
        validated.get("runtime_execution_performed") is False,
        "V8 validator runtime-execution boundary drift",
    )
    _require(
        validated.get("model_execution_performed") is False,
        "V8 validator model-execution boundary drift",
    )

    return {
        "schema": V8_SUPPLIED_ENVIRONMENT_SCHEMA,
        "runtime_environment_verified": True,
        "python_major_minor": list(python_major_minor),
        "pip_freeze_sha256": pip_freeze_sha256,
        "collection_performed": False,
        "filesystem_observation_performed": False,
        "subprocess_execution_performed": False,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_execution_performed": False,
        "pure_validator_git_blob": V8_RUNTIME_GIT_BLOB,
    }


def source_only_provider_progress(
    snapshot_id: str,
    *,
    supplied_v8_environment_fact: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Describe exact progress without claiming provider completeness."""
    values = source_only_self_audit_values(snapshot_id)
    validated_environment: dict[str, Any] | None = None

    if snapshot_id == V14:
        unresolved = V14_UNRESOLVED
    elif snapshot_id == V10:
        unresolved = V10_UNRESOLVED
    elif snapshot_id == V2R13:
        unresolved = V2R13_UNRESOLVED
    elif snapshot_id == V8:
        if supplied_v8_environment_fact is None:
            unresolved = V8_UNRESOLVED_WITHOUT_SUPPLIED_ENVIRONMENT
        else:
            validated_environment = validate_v8_supplied_environment_fact(
                supplied_v8_environment_fact
            )
            unresolved = V8_UNRESOLVED_WITH_SUPPLIED_ENVIRONMENT
    else:  # pragma: no cover - guarded by source_only_self_audit_values
        raise RuntimePrimitiveProviderSourceOnlyHold(
            f"unsupported source-only provider snapshot: {snapshot_id!r}"
        )

    supported = tuple(values)
    if validated_environment is not None:
        supported = supported + ("runtime_environment_verified",)

    return {
        "schema": PROGRESS_SCHEMA,
        "snapshot_id": snapshot_id,
        "source_only_values": deepcopy(values),
        "validated_v8_environment_fact": deepcopy(validated_environment),
        "supported_primitive_names": supported,
        "supported_primitive_count": len(supported),
        "unresolved_primitive_names": tuple(unresolved),
        "unresolved_primitive_count": len(unresolved),
        "provider_complete": False,
        "canonical_provider_binding_present": False,
        "canonical_collection_enabled": False,
        "live_observation_performed": False,
        "filesystem_observation_performed": False,
        "external_worktree_git_query_performed": False,
        "observer_invocation_performed": False,
        "provider_host_io_performed": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
    }


def v2r13_path_adapter_gap() -> dict[str, Any]:
    """Record why the six path-classification leaves remain unresolved."""
    _validate_contract_binding()
    leaves = (
        "frozen_source_worktree.exists",
        "frozen_source_worktree.is_directory",
        "frozen_source_worktree.is_symlink",
        "engine_worktree.exists",
        "engine_worktree.is_directory",
        "engine_worktree.is_symlink",
    )
    return {
        "snapshot_id": V2R13,
        "reviewed_git_observer_present": True,
        "reviewed_git_observer_git_blob": (
            "cc4774e6aa934764c189cebd4040cd8ea4870517"
        ),
        "reviewed_git_observer_claims": (
            "exact resolved source path identity",
            "exact resolved engine path identity",
            "source HEAD commit",
            "source HEAD tree",
            "source clean full worktree",
            "source detached HEAD",
            "engine HEAD commit",
            "engine clean full worktree",
        ),
        "missing_activation_leaves": leaves,
        "observer_receipt_contains_missing_leaves": False,
        "inference_permitted": False,
        "adapter_implemented": False,
        "new_observation_primitive_required": True,
        "live_observation_performed": False,
        "runtime_execution_authorized": False,
    }


def source_only_provider_contract() -> dict[str, Any]:
    """Return the exact non-observing implementation boundary."""
    _validate_contract_binding()
    return {
        "schema": CONTRACT_SCHEMA,
        "provider_contract_git_blob": PROVIDER_CONTRACT_GIT_BLOB,
        "provider_contract_semantic_sha256": (
            PROVIDER_CONTRACT_SEMANTIC_SHA256
        ),
        "v8_runtime_git_blob": V8_RUNTIME_GIT_BLOB,
        "common_self_audit_provider_implemented": True,
        "v8_load_call_self_audit_implemented": True,
        "v8_supplied_environment_validator_implemented": True,
        "v8_live_environment_collector_implemented": False,
        "v8_offline_only_provider_implemented": False,
        "v2r13_path_adapter_implemented": False,
        "v2r13_live_model_identity_provider_implemented": False,
        "v2r13_runtime_image_provider_implemented": False,
        "v2r13_portable_attestation_provider_implemented": False,
        "v14_live_identity_provider_implemented": False,
        "v10_live_identity_provider_implemented": False,
        "endpoint_liveness_provider_implemented": False,
        "canonical_provider_binding_present": False,
        "canonical_collection_enabled": False,
        "live_observation_performed": False,
        "provider_host_io_performed": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
    }


def provide_live_primitive(*args: Any, **kwargs: Any) -> None:
    raise RuntimePrimitiveProviderSourceOnlyHold(
        "GENERATION2_LIVE_PRIMITIVE_PROVIDER_NOT_IMPLEMENTED"
    )
