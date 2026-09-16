"""Source-only reconciliation for the post-admission V2R13 runtime frontier.

Generation-2 now has a reviewed activation-evidence binding that can admit
collector identity and runtime readiness from exact supplied V2R13 evidence.
That does not make the older live-identity collector lane current: its frozen
semantic contract still reports the historical 13/3 capability frontier and
its dormant implementation still has no host backend or canonical live
collection.

This separate instrument reconciles those facts without rewriting accepted
historical sources. It pins the dormant live-identity collector implementation
by exact Git blob and source SHA-256, declares the newer 16/16 provider
capability frontier authoritative for capability accounting, and preserves the
remaining collection, activation, execution-materialization, and runtime
authority gaps.

No live observation, host I/O, runtime action, inference, game execution,
training, deployment, VOID mutation, or funds action occurs here.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_execution_adapter_generation2 as execution_adapter,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_activation_contract_generation2
    as activation_contract,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_activation_evidence_collector_binding_generation2
    as activation_evidence_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_live_identity_collector_contract_generation2
    as live_identity_contract,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_live_identity_collector_implementation_generation2
    as live_identity_implementation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_ollama_observer_binding_generation2
    as ollama_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_rootless_docker_image_backend_binding_generation2
    as runtime_image_binding,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-post-admission-collection-activation-reconciliation.v1"
)

ACTIVATION_CONTRACT_GIT_BLOB = "a3acb42280c334daa24a3b830105a04666fd603b"
EXECUTION_ADAPTER_GIT_BLOB = "994d44d751c530619649322c72a65edf15f6a8c3"
ACTIVATION_EVIDENCE_BINDING_GIT_BLOB = "ddda2bac0570f99295b2c15b2000baed8478aa4c"
LIVE_IDENTITY_CONTRACT_GIT_BLOB = "db9fbb58f3d5870c77a796641afb1014acc19ee4"
LIVE_IDENTITY_IMPLEMENTATION_GIT_BLOB = "49b1044a45cdb92d7077028b9856ef710f07b275"
OLLAMA_BINDING_GIT_BLOB = "58364a1d5d71aead9df6dc0fc61661a557131508"
RUNTIME_IMAGE_BINDING_GIT_BLOB = "7075ded7a19454239b95a09e7b4630413124a796"

ACTIVATION_EVIDENCE_BINDING_SOURCE_SHA256 = (
    "57b45d106f5d4f2e2531a445669910d925c2e0e4bfad725333714703a75b616e"
)
LIVE_IDENTITY_IMPLEMENTATION_SOURCE_SHA256 = "8c415a0f3690a96a95c051a365691d3dad501e5656b438b0bf57a502311db9c8"

HISTORICAL_LIVE_IDENTITY_SUPPORTED = 13
HISTORICAL_LIVE_IDENTITY_UNRESOLVED = (
    "endpoint_liveness",
    "model_identity_verified",
    "runtime_image_identity_verified",
)
CURRENT_PROVIDER_SUPPORTED = 16
CURRENT_PROVIDER_UNRESOLVED: tuple[str, ...] = ()

ACTIVATION_BLOCKERS = (
    "V2R13_ACTIVATION_BINDING_NOT_REVIEWED",
    "V2R13_ACTIVE_MODEL_DIGEST_PROBE_NOT_REVIEWED",
    "V2R13_FROZEN_WORKTREE_MATERIALIZER_NOT_REVIEWED",
    "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
)

EXECUTION_BLOCKERS = (
    "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
    "CROSS_CONTROL_RUNTIME_SELECTOR_NOT_IMPLEMENTED",
    "COMMAND_MATERIALIZER_NOT_IMPLEMENTED",
    "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
)


class RuntimeV2R13PostAdmissionReconciliationHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13PostAdmissionReconciliationHold(message)


def _validate_dependencies() -> dict[str, Any]:
    admission = (
        activation_evidence_binding
        .v2r13_activation_evidence_collector_binding_contract()
    )
    provider = ollama_binding.v2r13_ollama_observer_binding_contract()
    image = (
        runtime_image_binding
        .v2r13_rootless_docker_image_backend_binding_contract()
    )
    historical = (
        live_identity_contract
        .validate_v2r13_live_identity_collector_contract()
    )
    dormant = (
        live_identity_implementation
        .v2r13_live_identity_collector_implementation_contract()
    )
    activation = activation_contract.activation_descriptor(
        activation_contract.V2R13
    )
    descriptors = execution_adapter.all_execution_descriptors()
    v2r13_descriptors = [
        row
        for row in descriptors
        if row.get("apollyon_opponent", {}).get("snapshot_id")
        == activation_contract.V2R13
    ]

    _require(
        admission.get("reviewed_collector_binding_present") is True,
        "post-#116 reviewed collector binding missing",
    )
    _require(
        admission.get("collector_identity_admission_implemented") is True,
        "post-#116 collector identity admission missing",
    )
    _require(
        admission.get("runtime_readiness_admission_implemented") is True,
        "post-#116 runtime readiness admission missing",
    )
    _require(
        admission.get("runtime_execution_authorized") is False,
        "post-#116 admission unexpectedly authorizes runtime",
    )

    _require(
        provider.get("supported_primitive_count_after_binding")
        == CURRENT_PROVIDER_SUPPORTED,
        "current provider supported count drift",
    )
    _require(
        provider.get("remaining_unresolved_primitive_count") == 0,
        "current provider unresolved count drift",
    )
    _require(
        provider.get("all_v2r13_provider_primitives_implemented") is True,
        "current provider capability frontier incomplete",
    )
    _require(
        provider.get("binding_live_observation_implemented") is False,
        "provider binding unexpectedly performs live observation",
    )
    _require(
        provider.get("canonical_collection_enabled") is False,
        "provider binding unexpectedly enables canonical collection",
    )
    _require(
        image.get("runtime_image_identity_provider_primitive_implemented") is True,
        "runtime-image provider primitive missing",
    )

    _require(
        historical.get("supported_primitive_count_remains")
        == HISTORICAL_LIVE_IDENTITY_SUPPORTED,
        "historical live-identity supported count drift",
    )
    _require(
        historical.get("remaining_unresolved_primitive_count_remains") == 3,
        "historical live-identity unresolved count drift",
    )
    _require(
        historical.get("implementation_source_sha256") is None,
        "historical semantic contract unexpectedly self-pins implementation",
    )
    _require(
        historical.get("collector_binding_activation") is False,
        "historical semantic contract unexpectedly activates binding",
    )

    _require(
        dormant.get("supplied_receipt_composition_implemented") is True,
        "dormant live-identity receipt composition missing",
    )
    _require(
        dormant.get("host_backend_implementation_present") is False,
        "dormant live-identity implementation unexpectedly has host backend",
    )
    _require(
        dormant.get("live_collection_implemented") is False,
        "dormant live-identity implementation unexpectedly performs collection",
    )
    _require(
        dormant.get("canonical_implementation_source_binding_present") is False,
        "dormant live-identity implementation unexpectedly self-binds source",
    )
    _require(
        dormant.get("canonical_collection_enabled") is False,
        "dormant live-identity implementation unexpectedly enables collection",
    )

    _require(
        tuple(activation.get("blockers", ())) == ACTIVATION_BLOCKERS,
        "V2R13 activation blocker set drift",
    )
    _require(
        activation.get("activation_proven") is False,
        "V2R13 activation unexpectedly proven",
    )
    _require(
        activation.get("eligible") is False,
        "V2R13 activation unexpectedly eligible",
    )

    _require(
        len(v2r13_descriptors) == 6,
        "V2R13 execution-descriptor arm count drift",
    )
    for row in v2r13_descriptors:
        _require(
            tuple(row.get("reasons", ())) == EXECUTION_BLOCKERS,
            "V2R13 execution blocker set drift",
        )
        _require(
            row.get("eligible") is False,
            "V2R13 execution descriptor unexpectedly eligible",
        )

    return {
        "post116_activation_evidence_binding": deepcopy(admission),
        "provider_binding": deepcopy(provider),
        "runtime_image_binding": deepcopy(image),
        "historical_live_identity_contract": deepcopy(historical),
        "dormant_live_identity_implementation": deepcopy(dormant),
        "v2r13_activation_descriptor": deepcopy(activation),
        "v2r13_execution_descriptors": deepcopy(v2r13_descriptors),
    }


def v2r13_post_admission_reconciliation_contract() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "snapshot_id": activation_contract.V2R13,
        "activation_contract_git_blob": ACTIVATION_CONTRACT_GIT_BLOB,
        "execution_adapter_git_blob": EXECUTION_ADAPTER_GIT_BLOB,
        "activation_evidence_binding_git_blob": (
            ACTIVATION_EVIDENCE_BINDING_GIT_BLOB
        ),
        "activation_evidence_binding_source_sha256": (
            ACTIVATION_EVIDENCE_BINDING_SOURCE_SHA256
        ),
        "live_identity_contract_git_blob": LIVE_IDENTITY_CONTRACT_GIT_BLOB,
        "live_identity_implementation_git_blob": (
            LIVE_IDENTITY_IMPLEMENTATION_GIT_BLOB
        ),
        "live_identity_implementation_source_sha256": (
            LIVE_IDENTITY_IMPLEMENTATION_SOURCE_SHA256
        ),
        "live_identity_implementation_source_binding_present": True,
        "live_identity_implementation_source_identity_pinned_by_git_blob": True,
        "live_identity_implementation_source_identity_pinned_by_sha256": True,
        "live_identity_implementation_self_binding_present": False,
        "ollama_binding_git_blob": OLLAMA_BINDING_GIT_BLOB,
        "runtime_image_binding_git_blob": RUNTIME_IMAGE_BINDING_GIT_BLOB,
        "historical_live_identity_contract_retained": True,
        "historical_live_identity_supported_primitive_count": (
            HISTORICAL_LIVE_IDENTITY_SUPPORTED
        ),
        "historical_live_identity_remaining_unresolved_primitive_names": (
            HISTORICAL_LIVE_IDENTITY_UNRESOLVED
        ),
        "historical_live_identity_remaining_unresolved_primitive_count": 3,
        "historical_13_3_not_current_provider_capability": True,
        "provider_capability_frontier_authoritative": True,
        "current_provider_supported_primitive_count": CURRENT_PROVIDER_SUPPORTED,
        "current_provider_remaining_unresolved_primitive_names": (
            CURRENT_PROVIDER_UNRESOLVED
        ),
        "current_provider_remaining_unresolved_primitive_count": 0,
        "provider_capability_complete": True,
        "post_admission_readiness_layer_complete": True,
        "reviewed_collector_binding_present": True,
        "collector_identity_admission_implemented": True,
        "runtime_readiness_admission_implemented": True,
        "live_identity_supplied_receipt_composition_implemented": True,
        "live_collection_backend_implementation_present": False,
        "canonical_live_collection_path_complete": False,
        "canonical_collection_enabled": False,
        "runtime_activation_blockers": ACTIVATION_BLOCKERS,
        "runtime_activation_path_complete": False,
        "execution_materialization_blockers": EXECUTION_BLOCKERS,
        "execution_materialization_path_complete": False,
        "runtime_execution_authorized": False,
        "runtime_authority_is_not_only_remaining_gap": True,
        "next_gate": "V2R13_LIVE_COLLECTION_BACKEND_IMPLEMENTATION_REQUIRED",
        "next_change_class": (
            "explicit_authority_read_only_live_collection_backend_composition"
        ),
        "live_observation_required_for_this_change": False,
        "runtime_action_required_for_this_change": False,
        "deployment_required_for_this_change": False,
        "training_required_for_this_change": False,
        "funds_action_required_for_this_change": False,
        "reconciliation_live_observation_implemented": False,
        "reconciliation_filesystem_observation_implemented": False,
        "reconciliation_git_query_implemented": False,
        "reconciliation_subprocess_execution_implemented": False,
        "reconciliation_network_request_implemented": False,
        "reconciliation_ollama_request_implemented": False,
        "reconciliation_docker_command_implemented": False,
        "reconciliation_service_action_implemented": False,
        "reconciliation_runtime_start_implemented": False,
        "reconciliation_model_load_implemented": False,
        "reconciliation_model_inference_implemented": False,
        "reconciliation_game_execution_implemented": False,
        "reconciliation_training_implemented": False,
        "reconciliation_deployment_implemented": False,
        "reconciliation_void_chain_mutation_implemented": False,
        "reconciliation_wallet_or_funds_action_implemented": False,
        "dependency_contracts": dependencies,
    }


def enable_canonical_live_collection(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13PostAdmissionReconciliationHold(
        "V2R13_LIVE_COLLECTION_BACKEND_IMPLEMENTATION_REQUIRED"
    )


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13PostAdmissionReconciliationHold(
        "V2R13_COLLECTION_ACTIVATION_AND_EXECUTION_MATERIALIZATION_GAPS_REMAIN"
    )
