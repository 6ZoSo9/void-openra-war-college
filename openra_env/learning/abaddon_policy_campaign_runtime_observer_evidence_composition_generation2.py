"""Pure composition of supplied Generation-2 runtime observer records.

This module does not collect runtime evidence.  It validates already-produced
V8 asset-observer and V2R13 Git-observer records against the exact canonical
observer/path/evidence contracts, then emits bounded *partial* activation-
evidence fragments.

The distinction is deliberate:

* observer-record validation proves only that a supplied record has the exact
  shape and values expected from the reviewed observer surface;
* fragment composition exposes only fields actually supported by that supplied
  record plus lexical path binding;
* collector identity is not admitted;
* final activation-evidence shape is not complete;
* runtime readiness is not admitted;
* runtime execution is never authorized.

No filesystem I/O, Git command, subprocess, environment read, endpoint/systemd
probe, model load, observer invocation, worktree creation, game execution,
training, weight update, policy promotion, deployment, VOID-chain mutation, or
funds action occurs in this module.
"""

from __future__ import annotations

from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_observers_generation2 as observers,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    RUNTIME_AUTHORITY_BLOCKER,
    V10,
    V14,
    V2R13,
    V8,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_evidence_generation2 import (
    evidence_requirement,
)
from openra_env.learning.abaddon_policy_campaign_runtime_path_inputs_generation2 import (
    validate_explicit_path_inputs,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.runtime-observer-evidence-composition-contract.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2.runtime-observer-record-validation.v1"
)
FRAGMENT_SCHEMA = (
    "void.abaddon.generation2.runtime-observer-evidence-fragment.v1"
)

OBSERVER_SOURCE_SHA256 = (
    "cc02c4894a9fcb81152ca9f9f86c65a60443de4273e0d73282ea0f996469ab52"
)
OBSERVER_SOURCE_GIT_BLOB = "cc4774e6aa934764c189cebd4040cd8ea4870517"
ACTIVATION_EVIDENCE_SOURCE_GIT_BLOB = (
    "aac7964d9e80633535003b9f27066cac1bb4bac2"
)
PATH_INPUT_SOURCE_GIT_BLOB = "f65735c7820da9da0205388f1933b6aa9d6dd737"

V8_RECORD_FIELDS = (
    "schema",
    "snapshot_id",
    "asset_count",
    "assets",
    "all_assets_verified",
    "model_weights_loaded",
    "runtime_started",
    "runtime_execution_performed",
    "model_execution_performed",
    "game_execution_performed",
)

V8_ASSET_ROW_FIELDS = (
    "label",
    "root_field",
    "relative_path",
    "observation",
)

FILE_OBSERVATION_FIELDS = (
    "schema",
    "path",
    "expected_sha256",
    "actual_sha256",
    "byte_count",
    "maximum_bytes",
    "identity",
    "generation_stable",
    "regular_file",
    "symlink_followed",
    "runtime_execution_performed",
    "model_execution_performed",
)

V2R13_RECORD_FIELDS = (
    "schema",
    "snapshot_id",
    "source_root",
    "engine_root",
    "source_head_commit",
    "source_head_tree",
    "source_worktree_clean",
    "source_detached_head",
    "engine_head_commit",
    "engine_worktree_clean",
    "worktree_created",
    "checkout_mutation_performed",
    "runtime_execution_performed",
    "model_execution_performed",
    "game_execution_performed",
)


class RuntimeObserverEvidenceCompositionHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeObserverEvidenceCompositionHold(message)


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


def _require_exact_false(record: Mapping[str, Any], fields: tuple[str, ...]) -> None:
    for field in fields:
        _require(
            record.get(field) is False,
            f"observer record crossed authority boundary: {field}",
        )


def _validate_file_observation(
    record: Mapping[str, Any],
    *,
    expected_path: str,
    spec: observers.V8AssetSpec,
) -> None:
    _require(isinstance(record, Mapping), "V8 file observation must be object")
    _require_exact_fields(record, FILE_OBSERVATION_FIELDS, "V8 file observation")

    _require(
        record.get("schema") == observers.FILE_OBSERVATION_SCHEMA,
        "V8 file observation schema drift",
    )
    _require(record.get("path") == expected_path, "V8 file path binding drift")
    _require(
        record.get("expected_sha256") == spec.expected_sha256,
        "V8 expected SHA-256 drift",
    )
    _require(
        record.get("actual_sha256") == spec.expected_sha256,
        "V8 actual SHA-256 drift",
    )
    _require(
        record.get("maximum_bytes") == spec.maximum_bytes,
        "V8 file maximum-byte bound drift",
    )

    byte_count = record.get("byte_count")
    _require(
        type(byte_count) is int and 0 <= byte_count <= spec.maximum_bytes,
        "V8 file byte_count invalid",
    )

    identity = record.get("identity")
    _require(isinstance(identity, Mapping), "V8 file identity missing")
    _require_exact_fields(
        identity,
        observers.FILE_IDENTITY_FIELDS,
        "V8 file identity",
    )
    for field in observers.FILE_IDENTITY_FIELDS:
        _require(
            type(identity.get(field)) is int,
            f"V8 file identity field is not int: {field}",
        )
    _require(
        identity.get("st_size") == byte_count,
        "V8 file identity size/byte_count drift",
    )

    _require(record.get("generation_stable") is True, "V8 file generation unstable")
    _require(record.get("regular_file") is True, "V8 asset is not regular file")
    _require(record.get("symlink_followed") is False, "V8 asset followed symlink")
    _require_exact_false(
        record,
        ("runtime_execution_performed", "model_execution_performed"),
    )


def validate_v8_asset_observer_record(
    observer_record: Mapping[str, Any],
    *,
    path_input_record: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate one supplied V8 observer receipt without collecting anything."""
    _require(isinstance(observer_record, Mapping), "V8 observer record must be object")
    _require_exact_fields(observer_record, V8_RECORD_FIELDS, "V8 observer record")

    path_validation = validate_explicit_path_inputs(V8, path_input_record)
    paths = path_validation["paths"]

    _require(
        observer_record.get("schema") == observers.V8_OBSERVATION_SCHEMA,
        "V8 observer schema drift",
    )
    _require(observer_record.get("snapshot_id") == V8, "V8 observer snapshot drift")
    _require(
        observer_record.get("asset_count") == len(observers.V8_ASSET_SPECS) == 17,
        "V8 observer asset count drift",
    )
    _require(
        observer_record.get("all_assets_verified") is True,
        "V8 observer did not verify all assets",
    )
    _require_exact_false(
        observer_record,
        (
            "model_weights_loaded",
            "runtime_started",
            "runtime_execution_performed",
            "model_execution_performed",
            "game_execution_performed",
        ),
    )

    assets = observer_record.get("assets")
    _require(isinstance(assets, list), "V8 observer assets must be list")
    _require(len(assets) == 17, "V8 observer assets length drift")

    for index, (spec, row) in enumerate(zip(observers.V8_ASSET_SPECS, assets)):
        _require(isinstance(row, Mapping), f"V8 asset row {index} must be object")
        _require_exact_fields(row, V8_ASSET_ROW_FIELDS, f"V8 asset row {index}")
        _require(row.get("label") == spec.label, f"V8 asset label drift: {index}")
        _require(
            row.get("root_field") == spec.root_field,
            f"V8 asset root-field drift: {index}",
        )
        _require(
            row.get("relative_path") == spec.relative_path,
            f"V8 asset relative-path drift: {index}",
        )
        expected_path = f"{paths[spec.root_field]}/{spec.relative_path}"
        _validate_file_observation(
            row.get("observation"),
            expected_path=expected_path,
            spec=spec,
        )

    return {
        "schema": VALIDATION_SCHEMA,
        "snapshot_id": V8,
        "observer_schema": observers.V8_OBSERVATION_SCHEMA,
        "observer_record_valid": True,
        "path_input_shape_valid": True,
        "path_binding_verified": True,
        "asset_identity_verified": True,
        "asset_count": 17,
        "observation_performed_by_validator": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "holds": [
            "V8_RUNTIME_ENVIRONMENT_EVIDENCE_UNRESOLVED",
            "V8_OFFLINE_ONLY_EVIDENCE_UNRESOLVED",
            "V8_LOAD_CALL_EVIDENCE_UNRESOLVED",
            "ACTIVATION_EVIDENCE_COLLECTOR_IDENTITY_NOT_ADMITTED",
            RUNTIME_AUTHORITY_BLOCKER,
        ],
    }


def validate_v2r13_git_observer_record(
    observer_record: Mapping[str, Any],
    *,
    path_input_record: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate one supplied V2R13 Git receipt without running Git."""
    _require(
        isinstance(observer_record, Mapping),
        "V2R13 observer record must be object",
    )
    _require_exact_fields(
        observer_record,
        V2R13_RECORD_FIELDS,
        "V2R13 observer record",
    )

    path_validation = validate_explicit_path_inputs(V2R13, path_input_record)
    paths = path_validation["paths"]

    _require(
        observer_record.get("schema") == observers.V2R13_OBSERVATION_SCHEMA,
        "V2R13 observer schema drift",
    )
    _require(
        observer_record.get("snapshot_id") == V2R13,
        "V2R13 observer snapshot drift",
    )
    _require(
        observer_record.get("source_root") == paths["frozen_source_root"],
        "V2R13 source path binding drift",
    )
    _require(
        observer_record.get("engine_root") == paths["exact_engine_root"],
        "V2R13 engine path binding drift",
    )
    _require(
        observer_record.get("source_head_commit")
        == observers.FROZEN_WAR_COLLEGE_COMMIT,
        "V2R13 source HEAD drift",
    )
    _require(
        observer_record.get("source_head_tree")
        == observers.FROZEN_WAR_COLLEGE_TREE,
        "V2R13 source tree drift",
    )
    _require(
        observer_record.get("source_worktree_clean") is True,
        "V2R13 source worktree dirty",
    )
    _require(
        observer_record.get("source_detached_head") is True,
        "V2R13 source HEAD is not detached",
    )
    _require(
        observer_record.get("engine_head_commit") == observers.FROZEN_ENGINE_COMMIT,
        "V2R13 engine HEAD drift",
    )
    _require(
        observer_record.get("engine_worktree_clean") is True,
        "V2R13 engine worktree dirty",
    )
    _require_exact_false(
        observer_record,
        (
            "worktree_created",
            "checkout_mutation_performed",
            "runtime_execution_performed",
            "model_execution_performed",
            "game_execution_performed",
        ),
    )

    return {
        "schema": VALIDATION_SCHEMA,
        "snapshot_id": V2R13,
        "observer_schema": observers.V2R13_OBSERVATION_SCHEMA,
        "observer_record_valid": True,
        "path_input_shape_valid": True,
        "path_binding_verified": True,
        "git_identity_verified": True,
        "observation_performed_by_validator": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "holds": [
            "V2R13_WORKTREE_PATH_CLASSIFICATION_EVIDENCE_UNRESOLVED",
            "V2R13_ENDPOINT_EVIDENCE_UNRESOLVED",
            "V2R13_MODEL_IDENTITY_EVIDENCE_UNRESOLVED",
            "V2R13_RUNTIME_IMAGE_IDENTITY_EVIDENCE_UNRESOLVED",
            "V2R13_PORTABLE_BINDING_ATTESTATION_UNRESOLVED",
            "ACTIVATION_EVIDENCE_COLLECTOR_IDENTITY_NOT_ADMITTED",
            RUNTIME_AUTHORITY_BLOCKER,
        ],
    }


def validate_observer_record(
    snapshot_id: str,
    observer_record: Mapping[str, Any],
    *,
    path_input_record: Mapping[str, Any],
) -> dict[str, Any]:
    """Dispatch pure record validation for the two implemented observers."""
    if snapshot_id == V8:
        return validate_v8_asset_observer_record(
            observer_record,
            path_input_record=path_input_record,
        )
    if snapshot_id == V2R13:
        return validate_v2r13_git_observer_record(
            observer_record,
            path_input_record=path_input_record,
        )
    if snapshot_id in {V14, V10}:
        raise RuntimeObserverEvidenceCompositionHold(
            "GENERATION2_PROMOTED_LOOPBACK_OBSERVER_NOT_IMPLEMENTED"
        )
    raise RuntimeObserverEvidenceCompositionHold(
        f"unsupported reviewed snapshot: {snapshot_id!r}"
    )


def compose_observer_evidence_fragment(
    snapshot_id: str,
    observer_record: Mapping[str, Any],
    *,
    path_input_record: Mapping[str, Any],
) -> dict[str, Any]:
    """Compose only activation-evidence fields supported by a supplied receipt."""
    validation = validate_observer_record(
        snapshot_id,
        observer_record,
        path_input_record=path_input_record,
    )
    requirement = evidence_requirement(snapshot_id)
    path_validation = validate_explicit_path_inputs(snapshot_id, path_input_record)
    paths = path_validation["paths"]

    if snapshot_id == V8:
        supported = {
            "model_dir": paths["model_dir"],
            "adapter_dir": paths["adapter_dir"],
            "model_dir_bound": True,
            "adapter_dir_bound": True,
            "runtime_assets_verified": True,
            "model_weights_loaded": False,
        }
        unresolved = (
            "collector_contract_sha256",
            "runtime_environment_verified",
            "offline_only_verified",
            "load_call_performed",
        )
        fragment_kind = "v8_asset_identity"
    elif snapshot_id == V2R13:
        supported = {
            "frozen_source_worktree": {
                "path": observer_record["source_root"],
                "clean": True,
                "detached": True,
                "head_commit": observer_record["source_head_commit"],
                "tree_sha": observer_record["source_head_tree"],
            },
            "engine_worktree": {
                "path": observer_record["engine_root"],
                "clean": True,
                "head_commit": observer_record["engine_head_commit"],
            },
        }
        unresolved = (
            "collector_contract_sha256",
            "endpoint_liveness",
            "model_identity_verified",
            "runtime_image_identity_verified",
            "portable_binding_attested",
            "frozen_source_worktree.exists",
            "frozen_source_worktree.is_directory",
            "frozen_source_worktree.is_symlink",
            "engine_worktree.exists",
            "engine_worktree.is_directory",
            "engine_worktree.is_symlink",
        )
        fragment_kind = "v2r13_git_identity"
    else:
        raise RuntimeObserverEvidenceCompositionHold(
            "observer evidence composition is not available for snapshot"
        )

    return {
        "schema": FRAGMENT_SCHEMA,
        "snapshot_id": snapshot_id,
        "fragment_kind": fragment_kind,
        "observer_record_valid": validation["observer_record_valid"],
        "evidence_kind": requirement["evidence_kind"],
        "supported_activation_evidence_fields": supported,
        "unresolved_activation_evidence_fields": unresolved,
        "activation_evidence_shape_complete": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "observation_performed_by_composer": False,
        "runtime_selection_performed": False,
        "runtime_started": False,
        "runtime_execution_authorized": False,
        "holds": list(validation["holds"]),
    }


def observer_evidence_composition_contract() -> dict[str, Any]:
    """Return the pure composition boundary after canonical observer merge."""
    return {
        "schema": CONTRACT_SCHEMA,
        "observer_source_sha256": OBSERVER_SOURCE_SHA256,
        "observer_source_git_blob": OBSERVER_SOURCE_GIT_BLOB,
        "activation_evidence_source_git_blob":
            ACTIVATION_EVIDENCE_SOURCE_GIT_BLOB,
        "path_input_source_git_blob": PATH_INPUT_SOURCE_GIT_BLOB,
        "supported_snapshot_ids": (V2R13, V8),
        "promoted_loopback_snapshot_ids_unresolved": (V14, V10),
        "observer_record_validation_implemented": True,
        "partial_fragment_composition_implemented": True,
        "final_activation_evidence_shape_composition_implemented": False,
        "collector_identity_admission_implemented": False,
        "live_observation_performed": False,
        "host_backend_invoked": False,
        "external_worktree_git_query_performed": False,
        "pip_freeze_performed": False,
        "endpoint_probe_performed": False,
        "systemd_query_performed": False,
        "model_weights_loaded": False,
        "runtime_selection_performed": False,
        "runtime_started": False,
        "runtime_execution_authorized": False,
    }


def collect_or_observe_runtime_evidence(*args: Any, **kwargs: Any) -> None:
    """Always hold: composition accepts supplied records and never collects."""
    raise RuntimeObserverEvidenceCompositionHold(
        "GENERATION2_OBSERVER_EVIDENCE_COLLECTION_NOT_IMPLEMENTED"
    )
