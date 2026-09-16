"""Explicit path-input contract for Abaddon Generation-2 runtimes.

Canonical post-PR88 source defines no tracked source for:
  * V8 model_dir
  * V8 adapter_dir
  * V2R13 frozen_source_root
  * V2R13 exact_engine_root

The only V2R13 syntactic candidate is an internal pass-through call that accepts
already-supplied roots.  Therefore this contract deliberately keeps all four
paths as explicit caller-supplied external inputs.

This module validates only lexical path-input shape.  It does not:
  * discover or default a path,
  * read environment variables,
  * parse CLI arguments,
  * enumerate host directories,
  * touch the filesystem,
  * verify path existence or file identity,
  * create Git worktrees,
  * run pip freeze,
  * probe endpoints or systemd,
  * load model weights,
  * start runtimes/games,
  * grant runtime authority.

Filesystem/readiness verification remains a separate future collector concern.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import PurePosixPath
from typing import Any, Mapping

from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    RUNTIME_AUTHORITY_BLOCKER,
    V10,
    V14,
    V2R13,
    V8,
)
from openra_env.learning.abaddon_policy_campaign_runtime_observation_mechanics_generation2 import (
    observation_mechanics,
)

CONTRACT_SCHEMA = "void.abaddon.generation2.runtime-path-input-contract.v1"
REQUIREMENT_SCHEMA = "void.abaddon.generation2.runtime-path-input-requirement.v1"
RECORD_SCHEMA = "void.abaddon.generation2.runtime-path-input-record.v1"
VALIDATION_SCHEMA = "void.abaddon.generation2.runtime-path-input-validation.v1"

PATH_SOURCE_CENSUS_SHA256 = (
    "b6592bba2527d15d03557bb792888fad633892f7d6270976db6d021b4c354c03"
)

SOURCE_KIND = "explicit_external_input"

COMMON_AUTHORITY = {
    "path_discovery_performed": False,
    "environment_read_performed": False,
    "cli_parse_performed": False,
    "host_directory_enumeration_performed": False,
    "filesystem_observation_performed": False,
    "path_existence_verified": False,
    "path_identity_verified": False,
    "worktree_created": False,
    "pip_freeze_performed": False,
    "endpoint_probe_performed": False,
    "systemd_query_performed": False,
    "model_weights_loaded": False,
    "runtime_selection_performed": False,
    "runtime_started": False,
    "runtime_execution_authorized": False,
    "game_execution": False,
    "model_execution": False,
    "training": False,
    "weights_updated": False,
    "automatic_policy_promotion": False,
}


class RuntimePathInputHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimePathInputHold(message)


def _path_requirement(
    snapshot_id: str,
    *,
    fields: tuple[str, ...],
    canonical_consumers: tuple[str, ...],
) -> dict[str, Any]:
    mechanic = observation_mechanics(snapshot_id)
    _require(
        mechanic["snapshot_id"] == snapshot_id,
        "observation-mechanics snapshot drift",
    )
    return {
        "schema": REQUIREMENT_SCHEMA,
        "snapshot_id": snapshot_id,
        "source_kind": SOURCE_KIND,
        "path_fields": fields,
        "canonical_consumers": canonical_consumers,
        "tracked_source_defined_default": False,
        "tracked_source_defined_autodiscovery": False,
        "caller_must_supply_all_paths": True,
        "lexical_validation_only": True,
        "filesystem_observation_permitted": False,
        "path_existence_claimed": False,
        "path_identity_claimed": False,
        "runtime_readiness_claimed": False,
        "runtime_execution_authorized": False,
        "authority": deepcopy(COMMON_AUTHORITY),
    }


def path_input_requirement(snapshot_id: str) -> dict[str, Any]:
    """Return the exact caller-supplied path requirement for one runtime."""
    if snapshot_id == V2R13:
        return _path_requirement(
            V2R13,
            fields=("frozen_source_root", "exact_engine_root"),
            canonical_consumers=(
                "openra_env.learning.apollyon_v2r13_portable_checkout."
                "reviewed_path_binding",
                "openra_env.learning.apollyon_v2r13_portable_checkout."
                "PortableRunnerBinding.__init__",
            ),
        )

    if snapshot_id == V8:
        return _path_requirement(
            V8,
            fields=("model_dir", "adapter_dir"),
            canonical_consumers=(
                "openra_env.learning.apollyon_v8_campaign_runtime."
                "verify_v8_runtime_assets",
                "openra_env.learning.apollyon_v8_campaign_runtime."
                "FrozenV8LocalToolRuntime.load",
            ),
        )

    if snapshot_id in {V14, V10}:
        mechanic = observation_mechanics(snapshot_id)
        return {
            "schema": REQUIREMENT_SCHEMA,
            "snapshot_id": snapshot_id,
            "source_kind": None,
            "path_fields": (),
            "canonical_consumers": (),
            "tracked_source_defined_default": False,
            "tracked_source_defined_autodiscovery": False,
            "caller_must_supply_all_paths": False,
            "lexical_validation_only": True,
            "filesystem_observation_permitted": False,
            "path_existence_claimed": False,
            "path_identity_claimed": False,
            "runtime_readiness_claimed": False,
            "runtime_execution_authorized": False,
            "not_applicable_reason":
                "reviewed promoted-loopback runtime has no path-input surface",
            "observation_mechanic_class": mechanic["mechanic_class"],
            "authority": deepcopy(COMMON_AUTHORITY),
        }

    raise RuntimePathInputHold(f"unsupported reviewed snapshot: {snapshot_id!r}")


def path_input_contract() -> dict[str, Any]:
    """Return the complete four-runtime explicit-input contract."""
    requirements = [
        path_input_requirement(snapshot_id)
        for snapshot_id in (V14, V10, V2R13, V8)
    ]
    return {
        "schema": CONTRACT_SCHEMA,
        "path_source_census_sha256": PATH_SOURCE_CENSUS_SHA256,
        "runtime_count": 4,
        "requirements": requirements,
        "tracked_source_defined_path_source_count": 0,
        "explicit_external_input_runtime_count": 2,
        "explicit_external_input_path_count": 4,
        "path_defaults_implemented": False,
        "path_autodiscovery_implemented": False,
        "filesystem_observation_implemented": False,
        "collector_implementation_ready": False,
        "runtime_execution_authorized": False,
        "authority": deepcopy(COMMON_AUTHORITY),
    }


def _validate_absolute_lexical_path(value: Any, label: str) -> str:
    _require(type(value) is str and bool(value), f"{label} must be non-empty string")
    _require("\x00" not in value, f"{label} contains NUL")
    _require(not value.startswith("~"), f"{label} may not use tilde expansion")
    path = PurePosixPath(value)
    _require(path.is_absolute(), f"{label} must be absolute")
    _require(".." not in path.parts, f"{label} may not contain parent traversal")
    _require(
        str(path) == value,
        f"{label} must already be lexically normalized",
    )
    _require(value != "/", f"{label} may not be filesystem root")
    return value


def _expected_record_fields(requirement: Mapping[str, Any]) -> set[str]:
    return {
        "schema",
        "snapshot_id",
        "source_kind",
        *requirement["path_fields"],
    }


def validate_explicit_path_inputs(
    snapshot_id: str,
    record: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate explicit caller-supplied path strings without touching the host."""
    _require(isinstance(record, Mapping), "path-input record must be object")
    requirement = path_input_requirement(snapshot_id)
    _require(
        bool(requirement["path_fields"]),
        "runtime does not accept Generation-2 path inputs",
    )

    actual_fields = set(record)
    expected_fields = _expected_record_fields(requirement)
    _require(
        actual_fields == expected_fields,
        "path-input field set drift: "
        f"missing={sorted(expected_fields - actual_fields)!r} "
        f"extra={sorted(actual_fields - expected_fields)!r}",
    )
    _require(record.get("schema") == RECORD_SCHEMA, "path-input schema drift")
    _require(record.get("snapshot_id") == snapshot_id, "path-input snapshot drift")
    _require(
        record.get("source_kind") == SOURCE_KIND,
        "path-input source_kind must be explicit_external_input",
    )

    normalized: dict[str, str] = {}
    for field in requirement["path_fields"]:
        normalized[field] = _validate_absolute_lexical_path(
            record.get(field),
            field,
        )

    values = list(normalized.values())
    _require(len(values) == len(set(values)), "runtime path inputs must be distinct")

    return {
        "schema": VALIDATION_SCHEMA,
        "snapshot_id": snapshot_id,
        "source_kind": SOURCE_KIND,
        "paths": normalized,
        "path_input_shape_valid": True,
        "path_source_semantics_admitted": True,
        "path_existence_verified": False,
        "path_identity_verified": False,
        "runtime_readiness_admitted": False,
        "collector_implementation_ready": False,
        "runtime_execution_authorized": False,
        "holds": [
            "PATH_EXISTENCE_NOT_VERIFIED",
            "PATH_IDENTITY_NOT_VERIFIED",
            RUNTIME_AUTHORITY_BLOCKER,
        ],
        "authority": deepcopy(COMMON_AUTHORITY),
    }


def build_path_input_record(
    snapshot_id: str,
    **paths: str,
) -> dict[str, Any]:
    """Build an explicit record only when every required path is supplied."""
    requirement = path_input_requirement(snapshot_id)
    _require(
        bool(requirement["path_fields"]),
        "runtime does not accept Generation-2 path inputs",
    )
    _require(
        set(paths) == set(requirement["path_fields"]),
        "caller must supply exactly every required path",
    )
    record: dict[str, Any] = {
        "schema": RECORD_SCHEMA,
        "snapshot_id": snapshot_id,
        "source_kind": SOURCE_KIND,
        **paths,
    }
    validate_explicit_path_inputs(snapshot_id, record)
    return record


def discover_path_inputs(*args: Any, **kwargs: Any) -> None:
    """Always hold: tracked source defines no admissible path autodiscovery."""
    raise RuntimePathInputHold(
        "RUNTIME_PATH_AUTODISCOVERY_NOT_IMPLEMENTED: "
        "V8/V2R13 paths remain explicit external inputs"
    )


def observe_path_inputs(*args: Any, **kwargs: Any) -> None:
    """Always hold: filesystem observation belongs to a future collector."""
    raise RuntimePathInputHold(
        "RUNTIME_PATH_OBSERVATION_NOT_IMPLEMENTED: "
        "path-input contract performs lexical validation only"
    )
