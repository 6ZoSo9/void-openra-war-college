"""Pure common-evidence enrichment for Generation-2 partial integration records.

This module adds the canonical source-only common identity fields to an already
produced Generation-2 runtime-evidence integration record, and carries the six
common operational fields forward as unresolved collector-provenance evidence.

It deliberately preserves the existing integration schema so the canonical
completion accountant can validate the enriched record without a parallel
admission path.

After enrichment, all required V8/V2R13 activation-evidence leaf paths are
classified as either supported or unresolved.  Zero unaccounted paths means
classification is complete; it does not mean the evidence shape is complete,
collector identity is admitted, runtime readiness is admitted, or execution is
authorized.

No filesystem access, Git command, subprocess, environment read, pip freeze,
endpoint/systemd probe, observer invocation, host-backend call, model load,
worktree creation, runtime/game/model execution, training, weight update,
promotion, deployment, VOID-chain mutation, or funds action occurs here.
"""

from __future__ import annotations

from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_common_evidence_shape_generation2
    as common_shape,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_evidence_completion_accounting_generation2
    as completion_accounting,
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
    "void.abaddon.generation2.runtime-common-evidence-enrichment-contract.v1"
)

COMMON_SHAPE_SOURCE_SHA256 = (
    "d41f7ed063c858dd2c977df17badc1585c151d8ada7cd0b07f8a9843f0186aa0"
)
COMMON_SHAPE_GIT_BLOB = "88b3a178533b7878ea43e2b904cdb63a36b6d080"
INTEGRATION_SOURCE_SHA256 = (
    "0fcbc4375fcc3c8458b06ea92dcd34fdedaa53e50e180169365a64cab30a3b3a"
)
INTEGRATION_GIT_BLOB = "28f737514d38c5ef09e9ad9905a2489c0510c70c"
COMPLETION_ACCOUNTING_SOURCE_SHA256 = (
    "4195573dad83c9dee0dc8206c84366b9843b9dc968e865ebac032a457ac07325"
)
COMPLETION_ACCOUNTING_GIT_BLOB = (
    "6a998f3f14c4844450d3b303977c9c4b6d24119f"
)


class RuntimeCommonEvidenceEnrichmentHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeCommonEvidenceEnrichmentHold(message)


def _ordered_unique(values: list[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return tuple(result)


def _merge_supported_fields(
    base: Mapping[str, Any],
    common: Mapping[str, Any],
) -> dict[str, Any]:
    _require(isinstance(base, Mapping), "base supported fields must be object")
    _require(isinstance(common, Mapping), "common supported fields must be object")

    merged = dict(base)
    for key, value in common.items():
        if key in merged:
            _require(
                merged[key] == value,
                f"common enrichment supported-field conflict: {key}",
            )
        else:
            merged[key] = value
    return merged


def enrich_integrated_evidence(
    integrated_record: Mapping[str, Any],
) -> dict[str, Any]:
    """Add common source identity while preserving all operational holds."""
    _require(
        isinstance(integrated_record, Mapping),
        "integrated evidence record must be object",
    )
    _require(
        integrated_record.get("schema") == evidence_integration.INTEGRATION_SCHEMA,
        "integrated evidence schema drift",
    )

    snapshot_id = integrated_record.get("snapshot_id")
    _require(
        snapshot_id in {V8, V2R13},
        f"unsupported common-evidence enrichment snapshot: {snapshot_id!r}",
    )
    _require(
        integrated_record.get("activation_evidence_shape_complete") is False,
        "common enrichment refuses pre-claimed complete evidence",
    )
    _require(
        integrated_record.get("collector_identity_admitted") is False,
        "common enrichment refuses pre-admitted collector identity",
    )
    _require(
        integrated_record.get("runtime_readiness_admitted") is False,
        "common enrichment refuses pre-admitted runtime readiness",
    )
    _require(
        integrated_record.get("runtime_execution_authorized") is False,
        "common enrichment refuses runtime execution authority",
    )

    common = common_shape.compose_common_evidence_shape(str(snapshot_id))
    _require(
        common.get("activation_evidence_shape_complete") is False,
        "common shape unexpectedly claims evidence completion",
    )
    _require(
        common.get("collector_identity_admitted") is False,
        "common shape unexpectedly admits collector identity",
    )
    _require(
        common.get("runtime_readiness_admitted") is False,
        "common shape unexpectedly admits runtime readiness",
    )
    _require(
        common.get("runtime_execution_authorized") is False,
        "common shape unexpectedly authorizes runtime execution",
    )
    _require(
        common.get("supported_static_identity_field_count") == 5,
        "common static identity field count drift",
    )
    _require(
        common.get("unresolved_operational_field_count") == 6,
        "common operational field count drift",
    )

    base_supported = integrated_record.get(
        "combined_supported_activation_evidence_fields"
    )
    common_supported = common["supported_activation_evidence_fields"]
    combined = _merge_supported_fields(base_supported, common_supported)

    unresolved_raw = integrated_record.get(
        "unresolved_activation_evidence_fields"
    )
    _require(
        isinstance(unresolved_raw, (tuple, list)),
        "integrated unresolved activation-evidence fields must be sequence",
    )
    unresolved = _ordered_unique(
        list(unresolved_raw)
        + list(common["unresolved_activation_evidence_fields"])
    )

    overlap = set(combined) & set(unresolved)
    _require(
        not overlap,
        f"common enrichment supported/unresolved overlap: {sorted(overlap)!r}",
    )

    enriched = dict(integrated_record)
    enriched.update(
        {
            "schema": evidence_integration.INTEGRATION_SCHEMA,
            "combined_supported_activation_evidence_fields": combined,
            "unresolved_activation_evidence_fields": unresolved,
            "common_shape_enrichment_applied": True,
            "common_static_identity_supported_field_count": 5,
            "common_operational_unresolved_field_count": 6,
            "activation_evidence_shape_complete": False,
            "collector_identity_admitted": False,
            "runtime_readiness_admitted": False,
            "runtime_execution_authorized": False,
        }
    )

    holds = _ordered_unique(
        list(integrated_record.get("holds", ()))
        + list(common.get("holds", ()))
        + [
            "COMMON_EVIDENCE_CLASSIFICATION_COMPLETE_NOT_READINESS",
            "ACTIVATION_EVIDENCE_COLLECTOR_IDENTITY_NOT_ADMITTED",
            RUNTIME_AUTHORITY_BLOCKER,
        ]
    )
    enriched["holds"] = holds

    accounting = completion_accounting.account_integrated_evidence(
        str(snapshot_id),
        enriched,
    )
    _require(
        accounting["unaccounted_leaf_count"] == 0,
        "common enrichment did not classify every required evidence leaf",
    )
    _require(
        accounting["all_required_paths_accounted"] is True,
        "common enrichment accounting did not close classification",
    )
    _require(
        accounting["all_required_paths_resolved"] is False,
        "common enrichment unexpectedly resolved all evidence leaves",
    )
    _require(
        accounting["activation_evidence_shape_complete"] is False,
        "completion accountant unexpectedly claims evidence completion",
    )
    _require(
        accounting["collector_identity_admitted"] is False,
        "completion accountant unexpectedly admits collector identity",
    )
    _require(
        accounting["runtime_readiness_admitted"] is False,
        "completion accountant unexpectedly admits runtime readiness",
    )
    _require(
        accounting["runtime_execution_authorized"] is False,
        "completion accountant unexpectedly authorizes runtime execution",
    )

    enriched.update(
        {
            "post_enrichment_required_leaf_count":
                accounting["required_leaf_count"],
            "post_enrichment_supported_leaf_count":
                accounting["supported_leaf_count"],
            "post_enrichment_unresolved_leaf_count":
                accounting["unresolved_leaf_count"],
            "post_enrichment_unaccounted_leaf_count": 0,
            "post_enrichment_all_required_paths_accounted": True,
            "post_enrichment_all_required_paths_resolved": False,
        }
    )

    return enriched


def common_evidence_enrichment_contract() -> dict[str, Any]:
    """Return the exact non-admitting enrichment boundary."""
    return {
        "schema": CONTRACT_SCHEMA,
        "common_shape_source_sha256": COMMON_SHAPE_SOURCE_SHA256,
        "common_shape_git_blob": COMMON_SHAPE_GIT_BLOB,
        "integration_source_sha256": INTEGRATION_SOURCE_SHA256,
        "integration_git_blob": INTEGRATION_GIT_BLOB,
        "completion_accounting_source_sha256":
            COMPLETION_ACCOUNTING_SOURCE_SHA256,
        "completion_accounting_git_blob": COMPLETION_ACCOUNTING_GIT_BLOB,
        "preserves_integration_schema": True,
        "supported_snapshot_ids": (V2R13, V8),
        "common_static_identity_enrichment_implemented": True,
        "common_operational_hold_propagation_implemented": True,
        "all_required_leaf_classification_implemented": True,
        "zero_unaccounted_means_readiness": False,
        "operational_observation_evidence_implemented": False,
        "collector_contract_identity_support_implemented": False,
        "activation_evidence_shape_completion_implemented": False,
        "collector_identity_admission_implemented": False,
        "runtime_readiness_admission_implemented": False,
        "live_observation_performed": False,
        "collector_execution_performed": False,
        "runtime_execution_authorized": False,
    }


def collect_or_admit_enriched_evidence(*args: Any, **kwargs: Any) -> None:
    """Always hold: enrichment classifies; it neither collects nor admits."""
    raise RuntimeCommonEvidenceEnrichmentHold(
        "GENERATION2_COMMON_EVIDENCE_ENRICHMENT_COLLECTION_OR_ADMISSION_NOT_IMPLEMENTED"
    )
