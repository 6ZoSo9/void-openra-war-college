"""Source-only V2R13 worktree-receipt provider adapter for Generation-2.

This module consumes an already-produced, canonical V2R13 worktree-observation
receipt and exposes exactly the six path-classification primitive values needed
by the dormant collector.

It performs NO live observation.  The supplied receipt is first validated by
the canonical V2R13 worktree-observer validator, which checks exact activation
worktree shape, expected frozen source commit/tree, expected engine commit,
generation-stability claims, read-only mode, and no mutation/runtime execution.

The adapter deliberately does not infer or implement:
* endpoint liveness;
* live model digest identity;
* runtime-image identity;
* portable-binding attestation.

No filesystem access, Git query, path resolution, observer invocation, host
backend selection, endpoint/systemd probe, model load, runtime/game/model
execution, training, promotion, deployment, VOID-chain mutation, or funds
action occurs.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_primitive_provider_source_only_generation2
    as source_only_provider,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_worktree_observer_generation2
    as worktree_observer,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    V2R13,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-worktree-provider-adapter-contract.v1"
)
ADAPTER_SCHEMA = (
    "void.abaddon.generation2.v2r13-worktree-provider-adapter.v1"
)

SOURCE_ONLY_PROVIDER_GIT_BLOB = "f3b48e624172aeed81e28a6e24508533b7b13661"
WORKTREE_OBSERVER_GIT_BLOB = "994f3be5d3344d6ac905c1f5fee9f9490fd4dd3f"

V2R13_WORKTREE_PRIMITIVES = (
    "frozen_source_worktree.exists",
    "frozen_source_worktree.is_directory",
    "frozen_source_worktree.is_symlink",
    "engine_worktree.exists",
    "engine_worktree.is_directory",
    "engine_worktree.is_symlink",
)

V2R13_REMAINING_UNRESOLVED = (
    "endpoint_liveness",
    "model_identity_verified",
    "runtime_image_identity_verified",
    "portable_binding_attested",
)


class RuntimeV2R13WorktreeProviderAdapterHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13WorktreeProviderAdapterHold(message)


def _validated_receipt(
    receipt: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    _require(
        isinstance(receipt, Mapping),
        "V2R13 supplied worktree receipt must be object",
    )
    validation = worktree_observer.validate_v2r13_worktree_observation(receipt)
    _require(
        validation.get("receipt_valid") is True,
        "V2R13 supplied worktree receipt not valid",
    )
    _require(
        validation.get("path_classification_complete") is True,
        "V2R13 path classification not complete",
    )
    _require(
        validation.get("git_identity_complete") is True,
        "V2R13 Git identity not complete",
    )
    _require(
        validation.get("activation_worktree_shape_complete") is True,
        "V2R13 activation worktree shape not complete",
    )
    _require(
        validation.get("canonical_provider_binding_present") is False,
        "V2R13 receipt validator unexpectedly admitted provider binding",
    )
    _require(
        validation.get("runtime_readiness_admitted") is False,
        "V2R13 receipt validator unexpectedly admitted readiness",
    )
    _require(
        validation.get("runtime_execution_authorized") is False,
        "V2R13 receipt validator unexpectedly authorized runtime execution",
    )
    return deepcopy(dict(receipt)), validation


def v2r13_worktree_primitive_values(
    receipt: Mapping[str, Any],
) -> dict[str, bool]:
    """Return exactly six primitive values from one validated supplied receipt."""
    record, _validation = _validated_receipt(receipt)

    source = record["frozen_source_worktree"]
    engine = record["engine_worktree"]

    values = {
        "frozen_source_worktree.exists": source["exists"],
        "frozen_source_worktree.is_directory": source["is_directory"],
        "frozen_source_worktree.is_symlink": source["is_symlink"],
        "engine_worktree.exists": engine["exists"],
        "engine_worktree.is_directory": engine["is_directory"],
        "engine_worktree.is_symlink": engine["is_symlink"],
    }
    _require(
        tuple(values) == V2R13_WORKTREE_PRIMITIVES,
        "V2R13 worktree primitive ordering drift",
    )
    _require(
        values["frozen_source_worktree.exists"] is True,
        "V2R13 frozen source existence drift",
    )
    _require(
        values["frozen_source_worktree.is_directory"] is True,
        "V2R13 frozen source directory drift",
    )
    _require(
        values["frozen_source_worktree.is_symlink"] is False,
        "V2R13 frozen source symlink drift",
    )
    _require(
        values["engine_worktree.exists"] is True,
        "V2R13 engine existence drift",
    )
    _require(
        values["engine_worktree.is_directory"] is True,
        "V2R13 engine directory drift",
    )
    _require(
        values["engine_worktree.is_symlink"] is False,
        "V2R13 engine symlink drift",
    )
    return values


def adapt_v2r13_worktree_receipt(
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate and adapt one supplied worktree receipt without observing host."""
    record, validation = _validated_receipt(receipt)
    values = v2r13_worktree_primitive_values(record)

    source_only = source_only_provider.source_only_provider_progress(V2R13)
    _require(
        source_only.get("supported_primitive_count") == 6,
        "V2R13 source-only provider count drift",
    )

    combined_supported = (
        tuple(source_only["supported_primitive_names"])
        + V2R13_WORKTREE_PRIMITIVES
    )
    _require(
        len(combined_supported) == 12,
        "V2R13 combined supported primitive count drift",
    )
    _require(
        len(set(combined_supported)) == 12,
        "V2R13 combined supported primitive names overlap",
    )

    return {
        "schema": ADAPTER_SCHEMA,
        "snapshot_id": V2R13,
        "primitive_values": deepcopy(values),
        "primitive_names": V2R13_WORKTREE_PRIMITIVES,
        "primitive_count": 6,
        "supplied_receipt_schema": record["schema"],
        "supplied_receipt_validated": True,
        "supplied_receipt_reports_filesystem_observation": (
            record["filesystem_observation_performed"]
        ),
        "supplied_receipt_reports_git_query": record["git_query_performed"],
        "adapter_filesystem_observation_performed": False,
        "adapter_external_worktree_git_query_performed": False,
        "adapter_path_resolution_performed": False,
        "adapter_observer_invocation_performed": False,
        "adapter_host_backend_invocation_performed": False,
        "combined_supported_primitive_names": combined_supported,
        "combined_supported_primitive_count": 12,
        "remaining_unresolved_primitive_names": V2R13_REMAINING_UNRESOLVED,
        "remaining_unresolved_primitive_count": 4,
        "provider_complete": False,
        "portable_binding_attested": False,
        "canonical_provider_binding_present": False,
        "canonical_collection_enabled": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "validation": deepcopy(validation),
    }


def v2r13_worktree_provider_adapter_contract() -> dict[str, Any]:
    source_only = source_only_provider.source_only_provider_contract()
    observer = worktree_observer.v2r13_worktree_observer_contract()

    _require(
        source_only.get("canonical_provider_binding_present") is False,
        "source-only provider binding unexpectedly canonical",
    )
    _require(
        observer.get("six_path_classification_leaves_implemented") is True,
        "canonical worktree observer does not implement six leaves",
    )
    _require(
        observer.get("real_host_backend_implemented") is False,
        "canonical worktree observer unexpectedly has host backend",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "source_only_provider_git_blob": SOURCE_ONLY_PROVIDER_GIT_BLOB,
        "worktree_observer_git_blob": WORKTREE_OBSERVER_GIT_BLOB,
        "snapshot_id": V2R13,
        "supplied_receipt_validation_required": True,
        "supplied_receipt_validator": (
            "validate_v2r13_worktree_observation"
        ),
        "six_worktree_primitives_implemented": True,
        "combined_source_supported_primitive_count": 12,
        "remaining_unresolved_primitive_count": 4,
        "remaining_unresolved_primitive_names": V2R13_REMAINING_UNRESOLVED,
        "portable_binding_attestation_implemented": False,
        "adapter_filesystem_observation_implemented": False,
        "adapter_git_query_implemented": False,
        "adapter_path_resolution_implemented": False,
        "adapter_observer_invocation_implemented": False,
        "adapter_host_backend_invocation_implemented": False,
        "canonical_provider_binding_present": False,
        "canonical_collection_enabled": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
    }


def adapt_live_worktree_state(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13WorktreeProviderAdapterHold(
        "GENERATION2_V2R13_LIVE_WORKTREE_ADAPTER_NOT_IMPLEMENTED"
    )
