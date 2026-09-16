"""Source-only V2R13 binding between activation evidence and the reviewed collector.

The canonical Generation-2 activation-evidence source deliberately keeps its
internal collector-admission switch closed.  This separate non-self-referential
binding pins that accepted activation-evidence source and the already-reviewed
V2R13 collector implementation binding, then implements only the admission step
for an already-supplied exact V2R13 evidence object.

The binding does not collect evidence, select a host backend, call Ollama or
Docker, start a runtime, run model inference, execute a game, train, deploy,
mutate VOID, or move funds.  Runtime execution authority remains closed.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_activation_evidence_generation2
    as activation_evidence,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_collector_implementation_generation2
    as collector_implementation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_collector_implementation_binding_generation2
    as collector_binding,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    RUNTIME_AUTHORITY_BLOCKER,
    V2R13,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-activation-evidence-collector-binding-contract.v1"
)
ADMISSION_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-bound-activation-evidence-admission.v1"
)

ACTIVATION_EVIDENCE_GIT_BLOB = "aac7964d9e80633535003b9f27066cac1bb4bac2"
ACTIVATION_EVIDENCE_SOURCE_SHA256 = (
    "c08a53842000343544f7ba63e8ae3bc4d24cb7f771294073caf4ab4a5ddc19a0"
)
COLLECTOR_IMPLEMENTATION_GIT_BLOB = "0003c24390194a4f621f13c6077e0604b9abcd98"
COLLECTOR_IMPLEMENTATION_SOURCE_SHA256 = (
    "91e094c71b838ad8116dced00fbc50b3e8a8bd138f75dfb5ae86b9bf5c97a8dc"
)
COLLECTOR_BINDING_GIT_BLOB = "bcc12598161a9516cb002d6e1c4eead7e914a425"
COLLECTOR_BINDING_SOURCE_SHA256 = (
    "af4a51207a0ad1477eedd18c325ee1df2231b6ad990bbb6f4f8ba53ef5bffc1d"
)
COLLECTOR_SEMANTIC_SHA256 = (
    "d11e45cabc10b42e09ab5e328e1e63721b633c7cdcfd7492038ec286b7f3e657"
)


class RuntimeV2R13ActivationEvidenceCollectorBindingHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13ActivationEvidenceCollectorBindingHold(message)


def _validate_dependencies() -> dict[str, Any]:
    binding = collector_binding.v2r13_collector_implementation_binding_contract()
    implementation = collector_implementation.collector_implementation_contract()
    evidence = activation_evidence.evidence_contract()

    _require(
        collector_implementation.COLLECTOR_SEMANTIC_SHA256
        == COLLECTOR_SEMANTIC_SHA256,
        "collector semantic SHA drift",
    )
    _require(
        collector_binding.COLLECTOR_IMPLEMENTATION_SOURCE_SHA256
        == COLLECTOR_IMPLEMENTATION_SOURCE_SHA256,
        "collector implementation source SHA binding drift",
    )

    _require(
        binding.get("collector_implementation_source_binding_present") is True,
        "collector implementation source binding absent",
    )
    _require(
        binding.get("canonical_primitive_source_bindings_present") is True,
        "canonical primitive source bindings absent",
    )
    _require(
        binding.get("primitive_source_binding_count") == 16,
        "primitive source-binding count drift",
    )
    _require(
        binding.get("reviewed_collector_binding_present") is False,
        "collector implementation binding unexpectedly performs activation admission",
    )
    _require(
        binding.get("canonical_collection_enabled") is False,
        "collector implementation binding unexpectedly enables collection",
    )
    _require(
        binding.get("runtime_readiness_admitted") is False,
        "collector implementation binding unexpectedly pre-admits readiness",
    )
    _require(
        binding.get("runtime_execution_authorized") is False,
        "collector implementation binding unexpectedly authorizes runtime",
    )

    _require(
        implementation.get("collector_semantic_sha256")
        == COLLECTOR_SEMANTIC_SHA256,
        "collector implementation semantic SHA drift",
    )
    _require(
        implementation.get("candidate_shape_validation_implemented") is True,
        "collector candidate shape validation missing",
    )
    _require(
        implementation.get("canonical_collection_enabled") is False,
        "collector implementation unexpectedly enables canonical collection",
    )
    _require(
        implementation.get("runtime_execution_authorized") is False,
        "collector implementation unexpectedly authorizes runtime",
    )

    _require(
        activation_evidence.REVIEWED_COLLECTOR_BINDING_PRESENT is False,
        "accepted activation-evidence source unexpectedly changed its internal binding",
    )
    _require(
        evidence.get("reviewed_collector_binding_present") is False,
        "accepted activation-evidence contract unexpectedly reports collector binding",
    )
    _require(
        evidence.get("runtime_execution_authorized") is False,
        "accepted activation-evidence contract unexpectedly authorizes runtime",
    )

    return {
        "collector_binding": deepcopy(binding),
        "collector_implementation": deepcopy(implementation),
        "activation_evidence_contract": deepcopy(evidence),
    }


def v2r13_activation_evidence_collector_binding_contract() -> dict[str, Any]:
    """Return the separate V2R13 collector-admission binding contract."""
    dependencies = _validate_dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "snapshot_id": V2R13,
        "activation_evidence_git_blob": ACTIVATION_EVIDENCE_GIT_BLOB,
        "activation_evidence_source_sha256": ACTIVATION_EVIDENCE_SOURCE_SHA256,
        "activation_evidence_source_binding_present": True,
        "collector_implementation_git_blob": COLLECTOR_IMPLEMENTATION_GIT_BLOB,
        "collector_implementation_source_sha256": (
            COLLECTOR_IMPLEMENTATION_SOURCE_SHA256
        ),
        "collector_binding_git_blob": COLLECTOR_BINDING_GIT_BLOB,
        "collector_binding_source_sha256": COLLECTOR_BINDING_SOURCE_SHA256,
        "collector_binding_source_identity_pinned_by_git_blob": True,
        "collector_binding_source_identity_pinned_by_sha256": True,
        "collector_semantic_sha256": COLLECTOR_SEMANTIC_SHA256,
        "canonical_primitive_source_bindings_present": True,
        "primitive_source_binding_count": 16,
        "reviewed_collector_binding_present": True,
        "collector_identity_admission_implemented": True,
        "runtime_readiness_admission_implemented": True,
        "admission_requires_supplied_exact_evidence": True,
        "canonical_provider_binding_present": False,
        "canonical_collection_enabled": False,
        "collector_identity_admitted_without_evidence": False,
        "runtime_readiness_admitted_without_evidence": False,
        "runtime_execution_authorized": False,
        "binding_live_observation_implemented": False,
        "binding_filesystem_observation_implemented": False,
        "binding_git_query_implemented": False,
        "binding_subprocess_execution_implemented": False,
        "binding_network_request_implemented": False,
        "binding_ollama_request_implemented": False,
        "binding_docker_command_implemented": False,
        "binding_service_action_implemented": False,
        "binding_model_load_implemented": False,
        "binding_model_inference_implemented": False,
        "binding_game_execution_implemented": False,
        "binding_training_implemented": False,
        "binding_deployment_implemented": False,
        "binding_void_chain_mutation_implemented": False,
        "binding_wallet_or_funds_action_implemented": False,
        "dependency_contracts": dependencies,
    }


def admit_bound_v2r13_evidence(record: Mapping[str, Any]) -> dict[str, Any]:
    """Admit exact supplied V2R13 evidence; never collect or execute anything."""
    _validate_dependencies()
    _require(isinstance(record, Mapping), "bound activation evidence must be object")
    _require(
        record.get("snapshot_id") == V2R13,
        "bound activation-evidence collector binding admits V2R13 only",
    )
    _require(
        record.get("collector_contract_sha256") == COLLECTOR_SEMANTIC_SHA256,
        "bound activation evidence collector semantic SHA mismatch",
    )

    shape = activation_evidence.validate_evidence_shape(record)
    _require(
        shape.get("evidence_shape_valid") is True,
        "bound activation evidence shape invalid",
    )
    _require(
        shape.get("collector_identity_admitted") is False,
        "base activation-evidence source unexpectedly admitted collector identity",
    )
    _require(
        shape.get("runtime_readiness_admitted") is False,
        "base activation-evidence source unexpectedly admitted readiness",
    )
    _require(
        shape.get("runtime_execution_authorized") is False,
        "base activation-evidence source unexpectedly authorized runtime",
    )

    return {
        "schema": ADMISSION_SCHEMA,
        "snapshot_id": V2R13,
        "collector_semantic_sha256": COLLECTOR_SEMANTIC_SHA256,
        "activation_evidence_source_binding_verified": True,
        "collector_implementation_source_binding_verified": True,
        "canonical_primitive_source_bindings_verified": True,
        "primitive_source_binding_count": 16,
        "evidence_shape_valid": True,
        "reviewed_collector_binding_present": True,
        "collector_identity_admitted": True,
        "runtime_readiness_admitted": True,
        "canonical_provider_binding_present": False,
        "canonical_collection_enabled": False,
        "runtime_execution_authorized": False,
        "evidence_collected_by_binding": False,
        "live_observation_performed": False,
        "filesystem_observation_performed": False,
        "git_query_performed": False,
        "subprocess_execution_performed": False,
        "network_request_performed": False,
        "ollama_request_performed": False,
        "docker_command_executed": False,
        "service_action_performed": False,
        "runtime_start_performed": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "policy_promotion_performed": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "superseded_base_shape_holds": tuple(shape.get("holds", ())),
        "holds": [RUNTIME_AUTHORITY_BLOCKER],
        "validated_evidence": deepcopy(dict(record)),
    }


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    """Always hold: readiness admission does not grant execution authority."""
    raise RuntimeV2R13ActivationEvidenceCollectorBindingHold(
        "V2R13_RUNTIME_READINESS_ADMITTED_BUT_RUNTIME_EXECUTION_NOT_AUTHORIZED"
    )
