"""Pure common activation-evidence shape for Generation-2.

This module closes only common activation-evidence values that are canonical
source identity, not operational observations.

Supported source-only identity fields:
* schema
* snapshot_id
* snapshot_sha256
* runtime_class
* evidence_kind

Operational common evidence remains unresolved because those values describe
what an eventual reviewed collector actually did:
* observation_mode
* mutation_performed
* service_action_performed
* runtime_start_performed
* game_execution_performed
* model_inference_performed

The expected operational values are defined by the activation-evidence
contract, but this module does not turn those requirements into evidence.

No filesystem access, Git command, subprocess, environment read, pip freeze,
endpoint/systemd probe, observer invocation, host-backend call, model load,
worktree creation, runtime/game/model execution, training, weight update,
promotion, deployment, VOID-chain mutation, or funds action occurs here.
"""

from __future__ import annotations

from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_activation_evidence_generation2
    as activation_evidence,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    RUNTIME_AUTHORITY_BLOCKER,
    V2R13,
    V8,
)

CONTRACT_SCHEMA = "void.abaddon.generation2.runtime-common-evidence-shape-contract.v1"
PROGRESS_SCHEMA = "void.abaddon.generation2.runtime-common-evidence-shape-progress.v1"

ACTIVATION_EVIDENCE_GIT_BLOB = "aac7964d9e80633535003b9f27066cac1bb4bac2"

STATIC_IDENTITY_FIELDS = (
    "schema",
    "snapshot_id",
    "snapshot_sha256",
    "runtime_class",
    "evidence_kind",
)

OPERATIONAL_COMMON_FIELDS = (
    "observation_mode",
    "mutation_performed",
    "service_action_performed",
    "runtime_start_performed",
    "game_execution_performed",
    "model_inference_performed",
)


class RuntimeCommonEvidenceShapeHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeCommonEvidenceShapeHold(message)


def compose_common_evidence_shape(snapshot_id: str) -> dict[str, Any]:
    """Return source-only common evidence identity plus operational holds."""
    _require(
        snapshot_id in {V8, V2R13},
        f"unsupported common-evidence-shape snapshot: {snapshot_id!r}",
    )

    requirement = activation_evidence.evidence_requirement(snapshot_id)
    required_fields = set(requirement["required_fields"])

    supported = {
        "schema": activation_evidence.EVIDENCE_SCHEMA,
        "snapshot_id": requirement["snapshot_id"],
        "snapshot_sha256": requirement["snapshot_sha256"],
        "runtime_class": requirement["runtime_class"],
        "evidence_kind": requirement["evidence_kind"],
    }

    _require(
        tuple(supported) == STATIC_IDENTITY_FIELDS,
        "common static identity field order drift",
    )
    _require(
        set(supported).issubset(required_fields),
        "common static identity field is not required evidence",
    )
    _require(
        set(OPERATIONAL_COMMON_FIELDS).issubset(required_fields),
        "common operational field is not required evidence",
    )
    _require(
        not (set(supported) & set(OPERATIONAL_COMMON_FIELDS)),
        "common identity/operational field overlap",
    )
    _require(
        "collector_contract_sha256" not in supported,
        "collector contract identity cannot be inferred from source shape",
    )

    _require(
        requirement["required_false"] == activation_evidence.COMMON_REQUIRED_FALSE
        or all(
            field in requirement["required_false"]
            for field in activation_evidence.COMMON_REQUIRED_FALSE
        ),
        "common required-false contract drift",
    )

    return {
        "schema": PROGRESS_SCHEMA,
        "snapshot_id": snapshot_id,
        "supported_activation_evidence_fields": supported,
        "unresolved_activation_evidence_fields": OPERATIONAL_COMMON_FIELDS,
        "supported_static_identity_field_count": len(supported),
        "unresolved_operational_field_count": len(OPERATIONAL_COMMON_FIELDS),
        "collector_contract_sha256_supported": False,
        "operational_requirements_supported_as_evidence": False,
        "activation_evidence_shape_complete": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "live_observation_performed": False,
        "collector_executed": False,
        "runtime_execution_authorized": False,
        "holds": [
            "COMMON_OPERATIONAL_EVIDENCE_COLLECTOR_PROVENANCE_UNRESOLVED",
            "ACTIVATION_EVIDENCE_COLLECTOR_IDENTITY_NOT_ADMITTED",
            RUNTIME_AUTHORITY_BLOCKER,
        ],
    }


def common_evidence_shape_contract() -> dict[str, Any]:
    """Return the exact source-only common-evidence boundary."""
    return {
        "schema": CONTRACT_SCHEMA,
        "activation_evidence_git_blob": ACTIVATION_EVIDENCE_GIT_BLOB,
        "supported_snapshot_ids": (V2R13, V8),
        "static_identity_fields": STATIC_IDENTITY_FIELDS,
        "operational_common_fields": OPERATIONAL_COMMON_FIELDS,
        "static_identity_shape_composition_implemented": True,
        "operational_observation_evidence_implemented": False,
        "collector_contract_identity_support_implemented": False,
        "activation_evidence_shape_completion_implemented": False,
        "collector_identity_admission_implemented": False,
        "runtime_readiness_admission_implemented": False,
        "live_observation_performed": False,
        "collector_execution_performed": False,
        "runtime_execution_authorized": False,
    }


def collect_or_admit_common_evidence(*args: Any, **kwargs: Any) -> None:
    """Always hold: source identity composition neither collects nor admits."""
    raise RuntimeCommonEvidenceShapeHold(
        "GENERATION2_COMMON_EVIDENCE_COLLECTION_OR_ADMISSION_NOT_IMPLEMENTED"
    )
