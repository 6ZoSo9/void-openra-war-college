"""Pure completion accounting for Generation-2 partial runtime evidence.

This module accepts an already-produced runtime-evidence integration record and
accounts, at exact activation-evidence leaf-path granularity, which required
paths are:

* supported by the integrated partial evidence,
* explicitly unresolved by the integrated partial evidence, or
* still unaccounted because no reviewed source-only surface supports them yet.

Reference-only keys used to validate nested evidence are tracked separately and
never counted as completed activation evidence.

Completion accounting is descriptive only.  It never converts field coverage
into collector admission, runtime-readiness admission, or runtime authority.

No filesystem access, Git command, subprocess, environment read, pip freeze,
endpoint/systemd probe, observer invocation, host-backend call, model load,
worktree creation, runtime/game/model execution, training, weight update,
promotion, deployment, VOID-chain mutation, or funds action occurs here.
"""

from __future__ import annotations

from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_activation_evidence_generation2
    as activation_evidence,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_evidence_integration_generation2
    as evidence_integration,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    RUNTIME_AUTHORITY_BLOCKER,
    V2R13,
    V8,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.runtime-evidence-completion-accounting-contract.v1"
)
ACCOUNTING_SCHEMA = (
    "void.abaddon.generation2.runtime-evidence-completion-accounting.v1"
)

INTEGRATION_SOURCE_SHA256 = (
    "0fcbc4375fcc3c8458b06ea92dcd34fdedaa53e50e180169365a64cab30a3b3a"
)
INTEGRATION_GIT_BLOB = "28f737514d38c5ef09e9ad9905a2489c0510c70c"
ACTIVATION_EVIDENCE_GIT_BLOB = "aac7964d9e80633535003b9f27066cac1bb4bac2"


class RuntimeEvidenceCompletionAccountingHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeEvidenceCompletionAccountingHold(message)


def _ordered_unique(values: list[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return tuple(result)


def _required_leaf_paths(snapshot_id: str) -> tuple[str, ...]:
    requirement = activation_evidence.evidence_requirement(snapshot_id)
    result: list[str] = []

    for field in requirement["required_fields"]:
        if snapshot_id == V2R13 and field == "frozen_source_worktree":
            result.extend(
                f"frozen_source_worktree.{child}"
                for child in requirement["frozen_source_worktree_fields"]
            )
        elif snapshot_id == V2R13 and field == "engine_worktree":
            result.extend(
                f"engine_worktree.{child}"
                for child in requirement["engine_worktree_fields"]
            )
        else:
            result.append(field)

    return tuple(result)


def _flatten_supported_fields(
    snapshot_id: str,
    fields: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    _require(
        isinstance(fields, Mapping),
        "combined supported activation-evidence fields must be object",
    )
    requirement = activation_evidence.evidence_requirement(snapshot_id)
    top_level_required = set(requirement["required_fields"])

    supported: dict[str, Any] = {}
    reference_only: dict[str, Any] = {}

    for key, value in fields.items():
        if key not in top_level_required:
            reference_only[key] = value
            continue

        if snapshot_id == V2R13 and key == "frozen_source_worktree":
            _require(
                isinstance(value, Mapping),
                "frozen_source_worktree supported value must be object",
            )
            allowed = set(requirement["frozen_source_worktree_fields"])
            extra = set(value) - allowed
            _require(
                not extra,
                f"unsupported frozen_source_worktree child fields: {sorted(extra)!r}",
            )
            for child, child_value in value.items():
                supported[f"frozen_source_worktree.{child}"] = child_value
            continue

        if snapshot_id == V2R13 and key == "engine_worktree":
            _require(
                isinstance(value, Mapping),
                "engine_worktree supported value must be object",
            )
            allowed = set(requirement["engine_worktree_fields"])
            extra = set(value) - allowed
            _require(
                not extra,
                f"unsupported engine_worktree child fields: {sorted(extra)!r}",
            )
            for child, child_value in value.items():
                supported[f"engine_worktree.{child}"] = child_value
            continue

        supported[key] = value

    return supported, reference_only


def account_integrated_evidence(
    snapshot_id: str,
    integrated_record: Mapping[str, Any],
) -> dict[str, Any]:
    """Account exact required leaf paths without admitting runtime evidence."""
    _require(
        snapshot_id in {V8, V2R13},
        f"unsupported completion-accounting snapshot: {snapshot_id!r}",
    )
    _require(
        isinstance(integrated_record, Mapping),
        "integrated evidence record must be object",
    )
    _require(
        integrated_record.get("schema") == evidence_integration.INTEGRATION_SCHEMA,
        "integrated evidence schema drift",
    )
    _require(
        integrated_record.get("snapshot_id") == snapshot_id,
        "integrated evidence snapshot drift",
    )
    _require(
        integrated_record.get("activation_evidence_shape_complete") is False,
        "completion accountant refuses pre-claimed complete evidence",
    )
    _require(
        integrated_record.get("collector_identity_admitted") is False,
        "completion accountant refuses pre-admitted collector identity",
    )
    _require(
        integrated_record.get("runtime_readiness_admitted") is False,
        "completion accountant refuses pre-admitted runtime readiness",
    )
    _require(
        integrated_record.get("runtime_execution_authorized") is False,
        "completion accountant refuses runtime execution authority",
    )

    combined = integrated_record.get(
        "combined_supported_activation_evidence_fields"
    )
    supported, reference_only = _flatten_supported_fields(
        snapshot_id,
        combined,
    )

    required = _required_leaf_paths(snapshot_id)
    required_set = set(required)

    extra_supported = set(supported) - required_set
    _require(
        not extra_supported,
        f"supported non-required evidence paths: {sorted(extra_supported)!r}",
    )

    unresolved_raw = integrated_record.get(
        "unresolved_activation_evidence_fields"
    )
    _require(
        isinstance(unresolved_raw, (tuple, list)),
        "unresolved activation-evidence fields must be sequence",
    )
    _require(
        all(isinstance(value, str) and value for value in unresolved_raw),
        "unresolved activation-evidence fields must be non-empty strings",
    )
    unresolved = _ordered_unique(list(unresolved_raw))

    unknown_unresolved = set(unresolved) - required_set
    _require(
        not unknown_unresolved,
        f"unresolved non-required evidence paths: {sorted(unknown_unresolved)!r}",
    )

    overlap = set(supported) & set(unresolved)
    _require(
        not overlap,
        f"evidence paths both supported and unresolved: {sorted(overlap)!r}",
    )

    supported_paths = tuple(path for path in required if path in supported)
    unresolved_paths = tuple(path for path in required if path in set(unresolved))
    unaccounted_paths = tuple(
        path
        for path in required
        if path not in supported and path not in set(unresolved)
    )

    _require(
        len(supported_paths) + len(unresolved_paths) + len(unaccounted_paths)
        == len(required),
        "completion accounting partition drift",
    )

    return {
        "schema": ACCOUNTING_SCHEMA,
        "snapshot_id": snapshot_id,
        "required_leaf_count": len(required),
        "supported_leaf_count": len(supported_paths),
        "unresolved_leaf_count": len(unresolved_paths),
        "unaccounted_leaf_count": len(unaccounted_paths),
        "required_leaf_paths": required,
        "supported_leaf_paths": supported_paths,
        "unresolved_leaf_paths": unresolved_paths,
        "unaccounted_leaf_paths": unaccounted_paths,
        "reference_only_field_count": len(reference_only),
        "reference_only_fields": dict(reference_only),
        "supported_unresolved_overlap": (),
        "all_required_paths_accounted":
            len(unaccounted_paths) == 0,
        "all_required_paths_resolved":
            len(unresolved_paths) == 0 and len(unaccounted_paths) == 0,
        "activation_evidence_shape_complete": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "live_observation_performed": False,
        "collector_executed": False,
        "runtime_execution_authorized": False,
        "holds": [
            "INTEGRATED_EVIDENCE_STILL_PARTIAL",
            "ACTIVATION_EVIDENCE_COLLECTOR_IDENTITY_NOT_ADMITTED",
            RUNTIME_AUTHORITY_BLOCKER,
        ],
    }


def evidence_completion_accounting_contract() -> dict[str, Any]:
    """Return the exact non-admitting completion-accounting boundary."""
    return {
        "schema": CONTRACT_SCHEMA,
        "integration_source_sha256": INTEGRATION_SOURCE_SHA256,
        "integration_git_blob": INTEGRATION_GIT_BLOB,
        "activation_evidence_git_blob": ACTIVATION_EVIDENCE_GIT_BLOB,
        "supported_snapshot_ids": (V2R13, V8),
        "required_leaf_path_accounting_implemented": True,
        "nested_v2r13_leaf_accounting_implemented": True,
        "reference_only_field_separation_implemented": True,
        "supported_unresolved_overlap_rejection_implemented": True,
        "completion_counts_are_descriptive_only": True,
        "activation_evidence_shape_completion_implemented": False,
        "collector_identity_admission_implemented": False,
        "runtime_readiness_admission_implemented": False,
        "live_observation_performed": False,
        "collector_execution_performed": False,
        "runtime_execution_authorized": False,
    }


def collect_or_admit_completion_evidence(*args: Any, **kwargs: Any) -> None:
    """Always hold: accounting cannot collect, complete, or admit evidence."""
    raise RuntimeEvidenceCompletionAccountingHold(
        "GENERATION2_COMPLETION_ACCOUNTING_COLLECTION_OR_ADMISSION_NOT_IMPLEMENTED"
    )
