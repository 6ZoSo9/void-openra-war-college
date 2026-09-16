"""Source-only reconciliation of V2R13 provider completion with the collector contract.

PR #113 completed the reviewed V2R13 provider-capability frontier: 16 supported
provider primitives and zero unresolved provider primitives.  The older
Generation-2 collector contract intentionally predates that completion and still
records its historical future-provider list.

This instrument reconciles those two reviewed facts without rewriting either
accepted source.  It does not admit collector identity, pin the collector
implementation into activation evidence, enable canonical collection, perform
live observation, authorize runtime execution, or cross any mutation boundary.

No filesystem access, Git command, subprocess, environment read, network/HTTP
request, Ollama request, Docker command, service action, model load, model
inference, game execution, training, weight update, promotion, deployment,
VOID-chain mutation, or funds action occurs here.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_collector_contract_generation2
    as collector_contract,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_collector_implementation_generation2
    as collector_implementation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_ollama_observer_binding_generation2
    as ollama_binding,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    V2R13,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-collector-reconciliation-contract.v1"
)

COLLECTOR_CONTRACT_GIT_BLOB = "8014431ad5329137e5ce12334d19d37c877a0b52"
COLLECTOR_CONTRACT_SOURCE_SHA256 = (
    "c48ad0871d4ea25e45efcde36e59622d1bb6b2a2fc4a4ed1f25988b543c2038f"
)
COLLECTOR_IMPLEMENTATION_GIT_BLOB = "0003c24390194a4f621f13c6077e0604b9abcd98"
COLLECTOR_IMPLEMENTATION_SOURCE_SHA256 = (
    "91e094c71b838ad8116dced00fbc50b3e8a8bd138f75dfb5ae86b9bf5c97a8dc"
)
V2R13_OLLAMA_BINDING_GIT_BLOB = "58364a1d5d71aead9df6dc0fc61661a557131508"
V2R13_OLLAMA_BINDING_SOURCE_SHA256 = (
    "c6b0bb746d017326e600f401a2d07a29fba79aced401687c4eb5238084ee9335"
)

HISTORICAL_REQUIRED_FUTURE_PRIMITIVES = (
    "read_only_loopback_endpoint_liveness",
    "read_only_active_model_digest_identity",
    "read_only_runtime_image_identity",
    "read_only_worktree_path_classification",
    "portable_binding_attestation",
    "common_operational_action_ledger",
)

PROVIDER_CAPABILITY_RECONCILIATION_STATUS = (
    "provider-capability-complete-collector-binding-still-closed"
)


class RuntimeV2R13CollectorReconciliationHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13CollectorReconciliationHold(message)


def v2r13_collector_reconciliation_contract() -> dict[str, Any]:
    """Reconcile provider completion without admitting canonical collection."""
    bound = ollama_binding.v2r13_ollama_observer_binding_contract()
    historical = collector_contract.validate_collector_contract()
    implementation = collector_implementation.collector_implementation_contract()

    manifest = historical.get("manifest")
    _require(isinstance(manifest, dict), "collector historical manifest missing")
    rows = manifest.get("snapshot_contracts")
    _require(isinstance(rows, dict), "collector historical snapshot map missing")
    row = rows.get(V2R13)
    _require(isinstance(row, dict), "collector historical V2R13 row missing")

    historical_future = tuple(row.get("required_future_primitives", ()))
    _require(
        historical_future == HISTORICAL_REQUIRED_FUTURE_PRIMITIVES,
        "collector historical V2R13 future-provider declaration drift",
    )
    _require(
        row.get("full_collector_implemented") is False,
        "historical collector unexpectedly claims full V2R13 implementation",
    )

    _require(
        bound.get("supported_primitive_count_after_binding") == 16,
        "V2R13 provider supported-count drift",
    )
    _require(
        bound.get("remaining_unresolved_primitive_count") == 0,
        "V2R13 provider unresolved-count drift",
    )
    _require(
        tuple(bound.get("remaining_unresolved_primitive_names", ())) == (),
        "V2R13 provider unresolved-set drift",
    )
    _require(
        bound.get("all_v2r13_provider_primitives_implemented") is True,
        "V2R13 reviewed provider capability set incomplete",
    )

    for field in (
        "full_collector_identity_admitted",
        "canonical_provider_binding_present",
        "canonical_collection_enabled",
        "runtime_readiness_admitted",
        "runtime_execution_authorized",
    ):
        _require(
            bound.get(field) is False,
            f"V2R13 Ollama binding crossed closed boundary: {field}",
        )

    _require(
        historical.get("implementation_source_binding_required_before_activation")
        is True,
        "collector implementation source-binding requirement lost",
    )
    _require(
        historical.get("implementation_source_sha256") is None,
        "collector implementation source unexpectedly admitted by historical contract",
    )
    _require(
        historical.get("reviewed_collector_binding_present") is False,
        "historical reviewed collector binding unexpectedly present",
    )
    _require(
        historical.get("collector_binding_activation") is False,
        "historical collector binding unexpectedly active",
    )

    _require(
        implementation.get("injected_primitive_orchestration_implemented") is True,
        "collector injected primitive orchestration missing",
    )
    _require(
        implementation.get("primitive_receipt_source_binding_enforced") is True,
        "collector primitive receipt source binding lost",
    )
    _require(
        implementation.get("canonical_primitive_source_bindings_present") is False,
        "collector canonical primitive bindings unexpectedly present",
    )
    _require(
        implementation.get("canonical_collection_enabled") is False,
        "collector canonical collection unexpectedly enabled",
    )
    _require(
        implementation.get(
            "collector_implementation_source_pinned_by_activation_contract"
        )
        is False,
        "collector implementation unexpectedly pinned by activation contract",
    )
    _require(
        implementation.get("reviewed_collector_binding_present") is False,
        "collector reviewed binding unexpectedly present",
    )
    _require(
        implementation.get("collector_identity_admission_implemented") is False,
        "collector identity admission unexpectedly implemented",
    )
    _require(
        implementation.get("runtime_readiness_admission_implemented") is False,
        "collector runtime-readiness admission unexpectedly implemented",
    )
    _require(
        implementation.get("runtime_execution_authorized") is False,
        "collector runtime execution unexpectedly authorized",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "snapshot_id": V2R13,
        "reconciliation_status": PROVIDER_CAPABILITY_RECONCILIATION_STATUS,
        "source_only_reconciliation": True,
        "historical_collector_contract_git_blob": COLLECTOR_CONTRACT_GIT_BLOB,
        "historical_collector_contract_source_sha256": (
            COLLECTOR_CONTRACT_SOURCE_SHA256
        ),
        "collector_implementation_git_blob": COLLECTOR_IMPLEMENTATION_GIT_BLOB,
        "collector_implementation_source_sha256": (
            COLLECTOR_IMPLEMENTATION_SOURCE_SHA256
        ),
        "v2r13_ollama_binding_git_blob": V2R13_OLLAMA_BINDING_GIT_BLOB,
        "v2r13_ollama_binding_source_sha256": (
            V2R13_OLLAMA_BINDING_SOURCE_SHA256
        ),
        "historical_required_future_primitives": historical_future,
        "historical_required_future_primitive_count": len(historical_future),
        "provider_supported_primitive_count": 16,
        "provider_remaining_unresolved_primitive_count": 0,
        "provider_remaining_unresolved_primitive_names": (),
        "provider_capability_coverage_complete": True,
        "historical_future_provider_gap_closed": True,
        "historical_contract_reconciliation_required": True,
        "collector_candidate_orchestration_present": True,
        "collector_implementation_source_binding_present": False,
        "canonical_primitive_source_bindings_present": False,
        "reviewed_collector_binding_present": False,
        "canonical_provider_binding_present": False,
        "canonical_collection_enabled": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "live_observation_performed": False,
        "http_request_performed": False,
        "host_backend_invoked": False,
        "ollama_request_performed": False,
        "docker_command_executed": False,
        "service_action_performed": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "policy_promotion_performed": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "historical_collector_contract": deepcopy(historical),
        "current_v2r13_provider_binding": deepcopy(bound),
        "current_collector_implementation_contract": deepcopy(implementation),
    }


def enable_canonical_collection(*args: Any, **kwargs: Any) -> None:
    """Hard hold: reconciliation is not collection admission."""
    raise RuntimeV2R13CollectorReconciliationHold(
        "V2R13_COLLECTOR_RECONCILIATION_DOES_NOT_AUTHORIZE_CANONICAL_COLLECTION"
    )
