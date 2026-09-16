"""Source-only V2R13 primitive-provider composition for Generation-2.

This module composes already-reviewed, already-supplied evidence only:

* six source-only collector self-audits;
* six V2R13 worktree path-classification primitives from a validated supplied
  worktree-observation receipt;
* one portable-binding primitive from a validated supplied fully-bound
  ``PortableRunnerBinding.attestation()`` receipt.

It performs no live observation or binding action itself.  The remaining live
identity surfaces stay unresolved:

* endpoint liveness;
* model digest identity;
* runtime-image identity.

This composition does not create a canonical provider binding, enable canonical
collection, admit runtime readiness, or authorize runtime execution.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_primitive_provider_source_only_generation2
    as source_only_provider,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_portable_binding_attestation_generation2
    as portable_binding_attestation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_worktree_provider_adapter_generation2
    as worktree_provider,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    V2R13,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-provider-composition-contract.v1"
)
COMPOSITION_SCHEMA = (
    "void.abaddon.generation2.v2r13-provider-composition.v1"
)

SOURCE_ONLY_PROVIDER_GIT_BLOB = "f3b48e624172aeed81e28a6e24508533b7b13661"
WORKTREE_PROVIDER_GIT_BLOB = "7e6f628c64fe02db42bd6adee67d3965e6b1ae92"
PORTABLE_ATTESTATION_GIT_BLOB = "afdc0421958565e713795dfd0d3c4c683041cc37"

PORTABLE_BINDING_PRIMITIVE = "portable_binding_attested"

V2R13_REMAINING_UNRESOLVED = (
    "endpoint_liveness",
    "model_identity_verified",
    "runtime_image_identity_verified",
)


class RuntimeV2R13ProviderCompositionHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13ProviderCompositionHold(message)


def compose_v2r13_provider(
    *,
    worktree_receipt: Mapping[str, Any],
    portable_binding_attestation_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Compose 13 supplied/source-only V2R13 primitives without live I/O."""
    source_only = source_only_provider.source_only_provider_progress(V2R13)
    _require(
        source_only.get("supported_primitive_count") == 6,
        "V2R13 source-only provider count drift",
    )
    _require(
        source_only.get("unresolved_primitive_count") == 10,
        "V2R13 source-only unresolved count drift",
    )

    worktree = worktree_provider.adapt_v2r13_worktree_receipt(worktree_receipt)
    _require(
        worktree.get("combined_supported_primitive_count") == 12,
        "V2R13 worktree-composed supported count drift",
    )
    _require(
        worktree.get("remaining_unresolved_primitive_count") == 4,
        "V2R13 worktree-composed unresolved count drift",
    )
    _require(
        worktree.get("portable_binding_attested") is False,
        "V2R13 worktree adapter unexpectedly attested portable binding",
    )

    attestation = (
        portable_binding_attestation.validate_v2r13_portable_binding_attestation(
            portable_binding_attestation_receipt
        )
    )
    _require(
        attestation.get("supplied_attestation_valid") is True,
        "V2R13 portable binding attestation not valid",
    )
    _require(
        attestation.get("portable_binding_fully_attested") is True,
        "V2R13 portable binding not fully attested",
    )
    _require(
        attestation.get("base_loaded_and_bound") is True,
        "V2R13 portable binding base not fully bound",
    )

    source_values = deepcopy(source_only["source_only_values"])
    worktree_values = deepcopy(worktree["primitive_values"])
    portable_values = {PORTABLE_BINDING_PRIMITIVE: True}

    all_values = {
        **source_values,
        **worktree_values,
        **portable_values,
    }
    supported = tuple(all_values)

    _require(len(supported) == 13, "V2R13 composed supported count drift")
    _require(
        len(set(supported)) == 13,
        "V2R13 composed supported primitive overlap",
    )
    _require(
        supported[-1] == PORTABLE_BINDING_PRIMITIVE,
        "V2R13 portable primitive ordering drift",
    )

    return {
        "schema": COMPOSITION_SCHEMA,
        "snapshot_id": V2R13,
        "primitive_values": deepcopy(all_values),
        "supported_primitive_names": supported,
        "supported_primitive_count": 13,
        "remaining_unresolved_primitive_names": V2R13_REMAINING_UNRESOLVED,
        "remaining_unresolved_primitive_count": 3,
        "portable_binding_attested": True,
        "supplied_worktree_receipt_validated": True,
        "supplied_portable_attestation_validated": True,
        "worktree_receipt_reports_filesystem_observation": (
            worktree["supplied_receipt_reports_filesystem_observation"]
        ),
        "worktree_receipt_reports_git_query": (
            worktree["supplied_receipt_reports_git_query"]
        ),
        "portable_attestation_sha256": (
            attestation["supplied_attestation_sha256"]
        ),
        "composition_filesystem_observation_performed": False,
        "composition_external_worktree_git_query_performed": False,
        "composition_path_resolution_performed": False,
        "composition_binding_install_performed": False,
        "composition_base_load_performed": False,
        "composition_observer_invocation_performed": False,
        "composition_host_backend_invocation_performed": False,
        "composition_endpoint_probe_performed": False,
        "composition_systemd_query_performed": False,
        "provider_complete": False,
        "canonical_provider_binding_present": False,
        "canonical_collection_enabled": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "worktree_adapter_result": deepcopy(worktree),
        "portable_attestation_validation": deepcopy(attestation),
    }


def v2r13_provider_composition_contract() -> dict[str, Any]:
    source_contract = source_only_provider.source_only_provider_contract()
    worktree_contract = worktree_provider.v2r13_worktree_provider_adapter_contract()
    attestation_contract = (
        portable_binding_attestation.v2r13_portable_binding_attestation_contract()
    )

    _require(
        source_contract.get("canonical_provider_binding_present") is False,
        "source-only provider unexpectedly canonical",
    )
    _require(
        worktree_contract.get("six_worktree_primitives_implemented") is True,
        "six V2R13 worktree primitives missing",
    )
    _require(
        attestation_contract.get("supplied_attestation_validator_implemented")
        is True,
        "portable attestation validator missing",
    )
    _require(
        attestation_contract.get("pre_base_load_attestation_admitted") is False,
        "partial portable attestation unexpectedly admitted",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "source_only_provider_git_blob": SOURCE_ONLY_PROVIDER_GIT_BLOB,
        "worktree_provider_git_blob": WORKTREE_PROVIDER_GIT_BLOB,
        "portable_attestation_git_blob": PORTABLE_ATTESTATION_GIT_BLOB,
        "snapshot_id": V2R13,
        "source_only_primitive_count": 6,
        "worktree_primitive_count": 6,
        "portable_binding_primitive_count": 1,
        "combined_supported_primitive_count": 13,
        "remaining_unresolved_primitive_count": 3,
        "remaining_unresolved_primitive_names": V2R13_REMAINING_UNRESOLVED,
        "portable_binding_provider_primitive_implemented": True,
        "supplied_worktree_receipt_required": True,
        "supplied_portable_attestation_required": True,
        "live_endpoint_liveness_provider_implemented": False,
        "live_model_identity_provider_implemented": False,
        "live_runtime_image_provider_implemented": False,
        "composition_filesystem_observation_implemented": False,
        "composition_git_query_implemented": False,
        "composition_path_resolution_implemented": False,
        "composition_binding_install_implemented": False,
        "composition_base_load_implemented": False,
        "composition_observer_invocation_implemented": False,
        "composition_host_backend_invocation_implemented": False,
        "canonical_provider_binding_present": False,
        "canonical_collection_enabled": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
    }


def compose_live_v2r13_provider(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13ProviderCompositionHold(
        "GENERATION2_V2R13_LIVE_PROVIDER_COMPOSITION_NOT_IMPLEMENTED"
    )
