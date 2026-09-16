"""Pure integration of Generation-2 partial runtime evidence.

This module combines two already-reviewed source-only layers:

* observer-evidence composition:
  validates supplied V8 asset or V2R13 Git observer receipts and emits bounded
  partial activation-evidence fields;
* evidence-shape progress:
  validates source/static or supplied pure facts without collecting anything.

Integration never converts those partial claims into collector admission,
runtime-readiness admission, or runtime authority.  It merges only fields whose
upstream validators have already accepted them, rejects conflicting duplicate
claims, and carries every unresolved field forward.

No filesystem access, Git command, subprocess, environment read, pip freeze,
endpoint/systemd probe, observer invocation, host-backend call, model load,
worktree creation, runtime/game/model execution, training, weight update,
promotion, deployment, VOID-chain mutation, or funds action occurs here.
"""

from __future__ import annotations

from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_evidence_shape_progress_generation2
    as shape_progress,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_observer_evidence_composition_generation2
    as observer_composition,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    RUNTIME_AUTHORITY_BLOCKER,
    V2R13,
    V8,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.runtime-evidence-integration-contract.v1"
)
INTEGRATION_SCHEMA = "void.abaddon.generation2.runtime-evidence-integration.v1"

OBSERVER_COMPOSITION_SOURCE_SHA256 = (
    "dbadd47bd5bf7354754220505857e881b9dea52989569d65669d90415cff0d9d"
)
OBSERVER_COMPOSITION_GIT_BLOB = "d069a0a1486b9531d084044d4de19e80893f7dfe"
SHAPE_PROGRESS_SOURCE_SHA256 = (
    "c6bdef2213ebbebe479ce37eeaa93c6634634942054ded1efb188c1d024a427f"
)
SHAPE_PROGRESS_GIT_BLOB = "412edc42c1735d8c26aa6d97a4e7cc607c28d8f2"


class RuntimeEvidenceIntegrationHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeEvidenceIntegrationHold(message)


def _merge_supported_fields(*records: Mapping[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for record in records:
        _require(
            isinstance(record, Mapping),
            "supported activation-evidence fields must be object",
        )
        for key, value in record.items():
            if key in merged:
                _require(
                    merged[key] == value,
                    f"conflicting supported activation-evidence field: {key}",
                )
            else:
                merged[key] = value
    return merged


def _ordered_unique(values: list[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return tuple(result)


def integrate_v8_partial_evidence(
    observer_record: Mapping[str, Any],
    *,
    path_input_record: Mapping[str, Any],
    environment_fact: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Combine V8 asset/path proof with optional supplied environment identity."""
    fragment = observer_composition.compose_observer_evidence_fragment(
        V8,
        observer_record,
        path_input_record=path_input_record,
    )
    progress = shape_progress.v8_evidence_shape_progress(environment_fact)

    _require(fragment.get("snapshot_id") == V8, "V8 fragment snapshot drift")
    _require(progress.get("snapshot_id") == V8, "V8 progress snapshot drift")
    _require(
        fragment.get("observer_record_valid") is True,
        "V8 observer fragment not valid",
    )
    _require(
        fragment.get("activation_evidence_shape_complete") is False,
        "V8 observer fragment unexpectedly complete",
    )
    _require(
        progress.get("activation_evidence_shape_complete") is False,
        "V8 shape progress unexpectedly complete",
    )

    static_fields = progress["source_static_activation_evidence_fields"]
    observer_fields = fragment["supported_activation_evidence_fields"]
    supplied_fields = progress["supplied_fact_activation_evidence_fields"]

    combined = _merge_supported_fields(
        static_fields,
        observer_fields,
        supplied_fields,
    )

    unresolved = list(fragment["unresolved_activation_evidence_fields"])
    for field in supplied_fields:
        unresolved = [value for value in unresolved if value != field]

    closed = set(combined)
    for field in progress["unresolved_activation_evidence_fields"]:
        if field not in closed:
            unresolved.append(field)

    unresolved_tuple = _ordered_unique(unresolved)

    _require(
        "collector_contract_sha256" in unresolved_tuple,
        "V8 integration lost collector-contract hold",
    )
    _require(
        "offline_only_verified" in unresolved_tuple,
        "V8 integration lost offline-only hold",
    )
    _require(
        "load_call_performed" in unresolved_tuple,
        "V8 integration lost load-call hold",
    )
    if environment_fact is None:
        _require(
            "runtime_environment_verified" in unresolved_tuple,
            "V8 integration lost unresolved environment field",
        )
    else:
        _require(
            combined.get("runtime_environment_verified") is True,
            "V8 supplied environment fact did not close shape value",
        )
        _require(
            "runtime_environment_verified" not in unresolved_tuple,
            "V8 environment field remained unresolved after valid supplied fact",
        )

    holds = _ordered_unique(
        list(fragment["holds"])
        + list(progress["holds"])
        + [
            "ACTIVATION_EVIDENCE_COLLECTOR_IDENTITY_NOT_ADMITTED",
            RUNTIME_AUTHORITY_BLOCKER,
        ]
    )

    return {
        "schema": INTEGRATION_SCHEMA,
        "snapshot_id": V8,
        "observer_fragment_valid": True,
        "shape_progress_valid": True,
        "source_static_field_count": len(static_fields),
        "observer_supported_field_count": len(observer_fields),
        "supplied_fact_supported_field_count": len(supplied_fields),
        "combined_supported_activation_evidence_fields": combined,
        "unresolved_activation_evidence_fields": unresolved_tuple,
        "activation_evidence_shape_complete": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "live_observation_performed_by_integrator": False,
        "pip_freeze_performed_by_integrator": False,
        "observer_invocation_performed_by_integrator": False,
        "runtime_selection_performed": False,
        "runtime_started": False,
        "runtime_execution_authorized": False,
        "holds": holds,
    }


def integrate_v2r13_partial_evidence(
    observer_record: Mapping[str, Any],
    *,
    path_input_record: Mapping[str, Any],
    portable_contract_fact: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Combine V2R13 Git/path proof with pure portable-contract identity."""
    fragment = observer_composition.compose_observer_evidence_fragment(
        V2R13,
        observer_record,
        path_input_record=path_input_record,
    )
    progress = shape_progress.v2r13_evidence_shape_progress(
        portable_contract_fact
    )

    _require(
        fragment.get("snapshot_id") == V2R13,
        "V2R13 fragment snapshot drift",
    )
    _require(
        progress.get("snapshot_id") == V2R13,
        "V2R13 progress snapshot drift",
    )
    _require(
        fragment.get("observer_record_valid") is True,
        "V2R13 observer fragment not valid",
    )
    _require(
        fragment.get("activation_evidence_shape_complete") is False,
        "V2R13 observer fragment unexpectedly complete",
    )
    _require(
        progress.get("activation_evidence_shape_complete") is False,
        "V2R13 shape progress unexpectedly complete",
    )

    static_fields = progress["expected_static_reference_fields"]
    observer_fields = fragment["supported_activation_evidence_fields"]
    progress_fields = progress["supported_activation_evidence_fields"]

    combined = _merge_supported_fields(
        static_fields,
        observer_fields,
        progress_fields,
    )

    unresolved = list(fragment["unresolved_activation_evidence_fields"])
    closed_top_level = set(combined)
    for field in progress["unresolved_activation_evidence_fields"]:
        if field not in closed_top_level:
            unresolved.append(field)

    unresolved_tuple = _ordered_unique(unresolved)

    for field in (
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
    ):
        _require(
            field in unresolved_tuple,
            f"V2R13 integration lost unresolved field: {field}",
        )

    _require(
        progress.get("portable_binding_attested") is False,
        "V2R13 integration invented portable binding attestation",
    )

    holds = _ordered_unique(
        list(fragment["holds"])
        + list(progress["holds"])
        + [
            "ACTIVATION_EVIDENCE_COLLECTOR_IDENTITY_NOT_ADMITTED",
            RUNTIME_AUTHORITY_BLOCKER,
        ]
    )

    return {
        "schema": INTEGRATION_SCHEMA,
        "snapshot_id": V2R13,
        "observer_fragment_valid": True,
        "shape_progress_valid": True,
        "portable_contract_identity_valid": progress[
            "portable_contract_identity_valid"
        ],
        "portable_binding_attested": False,
        "source_static_field_count": len(static_fields),
        "observer_supported_field_count": len(observer_fields),
        "shape_progress_supported_field_count": len(progress_fields),
        "combined_supported_activation_evidence_fields": combined,
        "unresolved_activation_evidence_fields": unresolved_tuple,
        "activation_evidence_shape_complete": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "live_observation_performed_by_integrator": False,
        "external_worktree_git_query_performed_by_integrator": False,
        "observer_invocation_performed_by_integrator": False,
        "runtime_selection_performed": False,
        "runtime_started": False,
        "runtime_execution_authorized": False,
        "holds": holds,
    }


def integrate_partial_evidence(
    snapshot_id: str,
    observer_record: Mapping[str, Any],
    *,
    path_input_record: Mapping[str, Any],
    supplied_fact: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Dispatch source-only partial integration for the two reviewed surfaces."""
    if snapshot_id == V8:
        return integrate_v8_partial_evidence(
            observer_record,
            path_input_record=path_input_record,
            environment_fact=supplied_fact,
        )
    if snapshot_id == V2R13:
        return integrate_v2r13_partial_evidence(
            observer_record,
            path_input_record=path_input_record,
            portable_contract_fact=supplied_fact,
        )
    raise RuntimeEvidenceIntegrationHold(
        f"unsupported partial-evidence integration snapshot: {snapshot_id!r}"
    )


def runtime_evidence_integration_contract() -> dict[str, Any]:
    """Return the exact source-only integration boundary."""
    return {
        "schema": CONTRACT_SCHEMA,
        "observer_composition_source_sha256":
            OBSERVER_COMPOSITION_SOURCE_SHA256,
        "observer_composition_git_blob": OBSERVER_COMPOSITION_GIT_BLOB,
        "shape_progress_source_sha256": SHAPE_PROGRESS_SOURCE_SHA256,
        "shape_progress_git_blob": SHAPE_PROGRESS_GIT_BLOB,
        "supported_snapshot_ids": (V2R13, V8),
        "partial_evidence_integration_implemented": True,
        "conflicting_supported_field_rejection_implemented": True,
        "final_activation_evidence_shape_composition_implemented": False,
        "collector_identity_admission_implemented": False,
        "runtime_readiness_admission_implemented": False,
        "live_observation_performed": False,
        "external_worktree_git_query_performed": False,
        "pip_freeze_performed": False,
        "observer_invocation_performed": False,
        "runtime_execution_authorized": False,
    }


def collect_or_admit_integrated_evidence(*args: Any, **kwargs: Any) -> None:
    """Always hold: integration neither collects nor admits runtime evidence."""
    raise RuntimeEvidenceIntegrationHold(
        "GENERATION2_INTEGRATED_EVIDENCE_COLLECTION_OR_ADMISSION_NOT_IMPLEMENTED"
    )
