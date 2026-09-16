"""Explicit-authority V2R13 live-collection adapter candidate for Generation-2.

This module composes the already-reviewed V2R13 provider surfaces into one
candidate full activation-evidence collection lane:

* six zero-I/O common self-audit primitives;
* six primitives from an already-supplied validated worktree receipt;
* one primitive from an already-supplied validated portable-binding attestation;
* three live identity primitives from the reviewed live-collection backend.

The live identity leg is impossible unless the caller explicitly supplies
``collection_authorized=True``, ``observation_authorized=True``, an HTTP GET
backend, and a Docker metadata command backend.  Worktree and portable-binding
evidence remain supplied-receipt only in this adapter.

The resulting 16 source-bound primitive receipts are passed through the reviewed
collector implementation and then through the reviewed activation-evidence
admission binding.  That can produce a candidate whose collector identity and
runtime readiness are admitted from exact evidence, but THIS adapter is not
self-bound.  Canonical live collection remains disabled until a separate source
binding reviews and pins this adapter implementation.

No runtime start/stop/reload, model load/inference, game execution, training,
deployment, VOID-chain mutation, or funds action is implemented here.
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
    abaddon_policy_campaign_runtime_primitive_provider_source_only_generation2
    as source_only_provider,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_activation_evidence_collector_binding_generation2
    as activation_evidence_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_collector_implementation_binding_generation2
    as collector_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_live_collection_backend_binding_generation2
    as live_backend_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_live_collection_backend_generation2
    as live_backend,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_portable_binding_attestation_generation2
    as portable_attestation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_worktree_provider_adapter_generation2
    as worktree_adapter,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    RUNTIME_AUTHORITY_BLOCKER,
    V2R13,
    activation_descriptor,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-canonical-live-collection-adapter-contract.v1"
)
COLLECTION_SCHEMA = (
    "void.abaddon.generation2.v2r13-canonical-live-collection-adapter-candidate.v1"
)

LIVE_BACKEND_BINDING_GIT_BLOB = "1a480133382dc878c79e110b8f6d8f30d0d7229d"
LIVE_BACKEND_BINDING_SOURCE_SHA256 = (
    "9899e2024f7233aab72b05465ee9d89dfcdea059eacde18e9f5573300110f119"
)
LIVE_BACKEND_GIT_BLOB = "ee78726c7538aeb985ef00140d58792ec75fdcf3"
LIVE_BACKEND_SOURCE_SHA256 = (
    "1f8dacce44d355f2948359ff59c29b79d50c68e21a648814689ba6a85cce2c94"
)
COLLECTOR_IMPLEMENTATION_GIT_BLOB = "0003c24390194a4f621f13c6077e0604b9abcd98"
COLLECTOR_BINDING_GIT_BLOB = "bcc12598161a9516cb002d6e1c4eead7e914a425"
SOURCE_ONLY_PROVIDER_GIT_BLOB = "f3b48e624172aeed81e28a6e24508533b7b13661"
WORKTREE_ADAPTER_GIT_BLOB = "7e6f628c64fe02db42bd6adee67d3965e6b1ae92"
PORTABLE_ATTESTATION_GIT_BLOB = "afdc0421958565e713795dfd0d3c4c683041cc37"
ACTIVATION_EVIDENCE_BINDING_GIT_BLOB = (
    "ddda2bac0570f99295b2c15b2000baed8478aa4c"
)

NEXT_GATE = "V2R13_CANONICAL_LIVE_COLLECTION_ADAPTER_SOURCE_BINDING_REQUIRED"

COMMON_PRIMITIVES = (
    "observation_mode",
    "mutation_performed",
    "service_action_performed",
    "runtime_start_performed",
    "game_execution_performed",
    "model_inference_performed",
)
WORKTREE_PRIMITIVES = (
    "frozen_source_worktree.exists",
    "frozen_source_worktree.is_directory",
    "frozen_source_worktree.is_symlink",
    "engine_worktree.exists",
    "engine_worktree.is_directory",
    "engine_worktree.is_symlink",
)
LIVE_PRIMITIVES = (
    "endpoint_liveness",
    "model_identity_verified",
    "runtime_image_identity_verified",
)
PORTABLE_PRIMITIVE = "portable_binding_attested"


class RuntimeV2R13CanonicalLiveCollectionAdapterHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13CanonicalLiveCollectionAdapterHold(message)


def _validate_dependencies() -> dict[str, Any]:
    live = live_backend.v2r13_live_collection_backend_contract()
    live_binding = (
        live_backend_binding.v2r13_live_collection_backend_binding_contract()
    )
    collector = collector_binding.v2r13_collector_implementation_binding_contract()
    source_only = source_only_provider.source_only_provider_contract()
    worktree = worktree_adapter.v2r13_worktree_provider_adapter_contract()
    portable = portable_attestation.v2r13_portable_binding_attestation_contract()
    admission = (
        activation_evidence_binding
        .v2r13_activation_evidence_collector_binding_contract()
    )

    _require(
        live.get("live_collection_backend_implementation_present") is True,
        "V2R13 live backend implementation missing",
    )
    _require(
        live.get("live_collection_backend_requires_explicit_authority") is True,
        "V2R13 live backend explicit authority requirement lost",
    )
    _require(
        live.get("explicit_http_backend_injection_required") is True,
        "V2R13 live backend HTTP injection requirement lost",
    )
    _require(
        live.get("explicit_docker_command_backend_injection_required") is True,
        "V2R13 live backend Docker injection requirement lost",
    )
    _require(
        live.get("automatic_host_backend_selection") is False,
        "V2R13 live backend automatic host selection enabled",
    )
    _require(
        live.get("provider_capability_supported_primitive_count") == 16,
        "V2R13 live backend provider count drift",
    )

    _require(
        live_binding.get(
            "canonical_live_collection_backend_source_binding_present"
        )
        is True,
        "V2R13 live backend source binding missing",
    )
    _require(
        live_binding.get("live_collection_backend_git_blob")
        == LIVE_BACKEND_GIT_BLOB,
        "V2R13 live backend Git blob binding drift",
    )
    _require(
        live_binding.get("live_collection_backend_source_sha256")
        == LIVE_BACKEND_SOURCE_SHA256,
        "V2R13 live backend source SHA binding drift",
    )
    _require(
        live_binding.get("canonical_live_collection_path_complete") is False,
        "V2R13 live backend binding unexpectedly completes canonical path",
    )

    _require(
        collector.get("collector_implementation_source_binding_present") is True,
        "V2R13 collector implementation source binding missing",
    )
    _require(
        collector.get("canonical_primitive_source_bindings_present") is True,
        "V2R13 collector primitive source bindings missing",
    )
    _require(
        collector.get("primitive_source_binding_count") == 16,
        "V2R13 collector primitive binding count drift",
    )

    _require(
        source_only.get("common_self_audit_provider_implemented") is True,
        "V2R13 source-only common provider missing",
    )
    _require(
        worktree.get("six_worktree_primitives_implemented") is True,
        "V2R13 worktree provider missing six primitives",
    )
    _require(
        portable.get("supplied_attestation_validator_implemented") is True,
        "V2R13 portable attestation validator missing",
    )
    _require(
        admission.get("reviewed_collector_binding_present") is True,
        "V2R13 activation-evidence admission binding missing",
    )
    _require(
        admission.get("collector_identity_admission_implemented") is True,
        "V2R13 collector identity admission missing",
    )
    _require(
        admission.get("runtime_readiness_admission_implemented") is True,
        "V2R13 runtime readiness admission missing",
    )

    for label, contract in (
        ("live_backend", live),
        ("live_backend_binding", live_binding),
        ("collector_binding", collector),
        ("source_only_provider", source_only),
        ("worktree_adapter", worktree),
        ("portable_attestation", portable),
        ("activation_evidence_binding", admission),
    ):
        _require(
            contract.get("runtime_execution_authorized") is False,
            f"{label} unexpectedly authorizes runtime execution",
        )
        if "canonical_collection_enabled" in contract:
            _require(
                contract.get("canonical_collection_enabled") is False,
                f"{label} unexpectedly enables canonical collection",
            )

    return {
        "live_backend": deepcopy(live),
        "live_backend_binding": deepcopy(live_binding),
        "collector_binding": deepcopy(collector),
        "source_only_provider": deepcopy(source_only),
        "worktree_adapter": deepcopy(worktree),
        "portable_attestation": deepcopy(portable),
        "activation_evidence_binding": deepcopy(admission),
    }


def _primitive_receipt(
    *,
    primitive_name: str,
    source_sha256: str,
    value: Any,
) -> dict[str, Any]:
    return {
        "schema": collector_implementation.PRIMITIVE_RECEIPT_SCHEMA,
        "snapshot_id": V2R13,
        "primitive_name": primitive_name,
        "source_sha256": source_sha256,
        "observation_mode": "read_only",
        "value": deepcopy(value),
        "mutation_performed": False,
        "service_action_performed": False,
        "runtime_start_performed": False,
        "game_execution_performed": False,
        "model_inference_performed": False,
    }


def _base_evidence(
    *,
    live_candidate: Mapping[str, Any],
    worktree_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    requirement = activation_evidence.evidence_requirement(V2R13)
    activation = activation_descriptor(V2R13)

    ollama = live_candidate["ollama_observation"]
    image = live_candidate["runtime_image_receipt"]

    return {
        "schema": activation_evidence.EVIDENCE_SCHEMA,
        "snapshot_id": V2R13,
        "snapshot_sha256": activation["snapshot_sha256"],
        "runtime_class": activation["runtime_class"],
        "evidence_kind": requirement["evidence_kind"],
        "endpoint_url": activation["chat_completions_url"],
        "endpoint_loopback": True,
        "active_model_alias": ollama["running_model_alias"],
        "active_model_digest": ollama["running_model_digest"],
        "runtime_image_id": image["runtime_image_id"],
        "frozen_source_worktree": deepcopy(
            dict(worktree_receipt["frozen_source_worktree"])
        ),
        "engine_worktree": deepcopy(
            dict(worktree_receipt["engine_worktree"])
        ),
    }


def collect_v2r13_live_collection_adapter_candidate(
    *,
    collection_authorized: bool,
    observation_authorized: bool,
    http_get: Any,
    run_command: Any,
    worktree_receipt: Mapping[str, Any],
    portable_binding_attestation: Mapping[str, Any],
) -> dict[str, Any]:
    """Compose exact V2R13 evidence using only explicit authority and inputs."""
    _require(
        collection_authorized is True,
        "GENERATION2_V2R13_CANONICAL_ADAPTER_COLLECTION_NOT_AUTHORIZED",
    )
    _require(
        observation_authorized is True,
        "GENERATION2_V2R13_CANONICAL_ADAPTER_OBSERVATION_NOT_AUTHORIZED",
    )
    _require(callable(http_get), "explicit V2R13 HTTP GET backend required")
    _require(callable(run_command), "explicit V2R13 Docker command backend required")
    _require(
        isinstance(worktree_receipt, Mapping),
        "supplied V2R13 worktree receipt required",
    )
    _require(
        isinstance(portable_binding_attestation, Mapping),
        "supplied V2R13 portable-binding attestation required",
    )

    dependencies = _validate_dependencies()

    worktree_validation = (
        worktree_adapter.worktree_observer
        .validate_v2r13_worktree_observation(worktree_receipt)
    )
    _require(
        worktree_validation.get("receipt_valid") is True,
        "supplied V2R13 worktree receipt invalid",
    )
    worktree_values = worktree_adapter.v2r13_worktree_primitive_values(
        worktree_receipt
    )

    portable_validation = (
        portable_attestation.validate_v2r13_portable_binding_attestation(
            portable_binding_attestation
        )
    )
    _require(
        portable_validation.get("portable_binding_fully_attested") is True,
        "supplied V2R13 portable binding is not fully attested",
    )

    live_candidate = live_backend.collect_v2r13_live_identity_candidate(
        observation_authorized=True,
        http_get=http_get,
        run_command=run_command,
    )
    live_bound_validation = (
        live_backend_binding.validate_bound_live_collection_candidate(
            live_candidate,
            backend_source_sha256=LIVE_BACKEND_SOURCE_SHA256,
        )
    )
    _require(
        live_bound_validation.get("bound_live_collection_candidate_valid") is True,
        "V2R13 live backend candidate failed bound validation",
    )

    bindings = collector_binding.reviewed_v2r13_primitive_source_bindings()
    _require(
        len(bindings) == 16,
        "V2R13 reviewed primitive binding count drift",
    )

    receipts: dict[str, dict[str, Any]] = {}

    common_values = source_only_provider.source_only_self_audit_values(V2R13)
    _require(
        tuple(common_values) == COMMON_PRIMITIVES,
        "V2R13 common self-audit primitive ordering drift",
    )
    for name in COMMON_PRIMITIVES:
        receipts[name] = _primitive_receipt(
            primitive_name=name,
            source_sha256=bindings[name],
            value=common_values[name],
        )

    live_receipts = live_candidate["primitive_receipts"]
    _require(
        set(live_receipts) == set(LIVE_PRIMITIVES),
        "V2R13 live primitive receipt set drift",
    )
    for name in LIVE_PRIMITIVES:
        receipt = deepcopy(dict(live_receipts[name]))
        _require(
            receipt.get("source_sha256") == bindings[name],
            f"V2R13 live primitive source binding mismatch: {name}",
        )
        receipts[name] = receipt

    for name in WORKTREE_PRIMITIVES:
        receipts[name] = _primitive_receipt(
            primitive_name=name,
            source_sha256=bindings[name],
            value=worktree_values[name],
        )

    receipts[PORTABLE_PRIMITIVE] = _primitive_receipt(
        primitive_name=PORTABLE_PRIMITIVE,
        source_sha256=bindings[PORTABLE_PRIMITIVE],
        value=True,
    )

    required_names = collector_implementation.required_primitive_names(V2R13)
    _require(
        tuple(receipts) == required_names,
        "V2R13 adapter primitive ordering does not match collector",
    )
    _require(
        len(receipts) == 16,
        "V2R13 adapter primitive receipt count drift",
    )

    def primitive_provider(snapshot_id: str, primitive_name: str) -> Mapping[str, Any]:
        _require(snapshot_id == V2R13, "V2R13 adapter snapshot drift")
        _require(
            primitive_name in receipts,
            f"V2R13 adapter primitive not prepared: {primitive_name}",
        )
        return deepcopy(receipts[primitive_name])

    collector_candidate = collector_implementation.collect_candidate_with_provider(
        V2R13,
        _base_evidence(
            live_candidate=live_candidate,
            worktree_receipt=worktree_receipt,
        ),
        primitive_provider=primitive_provider,
        reviewed_primitive_source_bindings=bindings,
        collection_authorized=True,
    )
    _require(
        collector_candidate.get("activation_evidence_shape_valid") is True,
        "V2R13 collector candidate shape invalid",
    )

    evidence = collector_candidate["activation_evidence_candidate"]
    admission = activation_evidence_binding.admit_bound_v2r13_evidence(evidence)
    _require(
        admission.get("collector_identity_admitted") is True,
        "V2R13 collector identity not admitted",
    )
    _require(
        admission.get("runtime_readiness_admitted") is True,
        "V2R13 runtime readiness not admitted",
    )
    _require(
        admission.get("runtime_execution_authorized") is False,
        "V2R13 admission unexpectedly authorizes runtime execution",
    )

    return {
        "schema": COLLECTION_SCHEMA,
        "snapshot_id": V2R13,
        "collection_authorized": True,
        "observation_authorized": True,
        "explicit_http_backend_supplied": True,
        "explicit_docker_command_backend_supplied": True,
        "supplied_worktree_receipt_validated": True,
        "supplied_portable_binding_attestation_validated": True,
        "automatic_host_backend_selection": False,
        "primitive_receipt_count": 16,
        "primitive_receipt_names": tuple(receipts),
        "provider_capability_supported_primitive_count": 16,
        "provider_capability_remaining_unresolved_primitive_count": 0,
        "provider_capability_complete": True,
        "activation_evidence_shape_valid": True,
        "collector_identity_admitted": True,
        "runtime_readiness_admitted": True,
        "live_observation_performed": True,
        "ollama_tags_request_performed": True,
        "ollama_ps_request_performed": True,
        "chat_completions_request_performed": False,
        "docker_metadata_command_count": 3,
        "docker_mutating_command_performed": False,
        "worktree_observation_performed_by_adapter": False,
        "portable_binding_install_performed_by_adapter": False,
        "mutation_performed": False,
        "service_action_performed": False,
        "runtime_start_performed": False,
        "runtime_stop_performed": False,
        "runtime_reload_performed": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "policy_promotion_performed": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "canonical_live_collection_adapter_implementation_present": True,
        "canonical_live_collection_adapter_source_binding_present": False,
        "canonical_live_collection_path_complete": False,
        "canonical_collection_enabled": False,
        "runtime_execution_authorized": False,
        "holds": [
            NEXT_GATE,
            RUNTIME_AUTHORITY_BLOCKER,
        ],
        "worktree_validation": deepcopy(worktree_validation),
        "portable_binding_validation": deepcopy(portable_validation),
        "live_backend_candidate": deepcopy(live_candidate),
        "live_backend_bound_validation": deepcopy(live_bound_validation),
        "collector_candidate": deepcopy(collector_candidate),
        "activation_evidence": deepcopy(evidence),
        "activation_evidence_admission": deepcopy(admission),
        "dependency_contracts": dependencies,
    }


def v2r13_canonical_live_collection_adapter_contract() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "snapshot_id": V2R13,
        "live_backend_binding_git_blob": LIVE_BACKEND_BINDING_GIT_BLOB,
        "live_backend_binding_source_sha256": (
            LIVE_BACKEND_BINDING_SOURCE_SHA256
        ),
        "live_backend_git_blob": LIVE_BACKEND_GIT_BLOB,
        "live_backend_source_sha256": LIVE_BACKEND_SOURCE_SHA256,
        "collector_implementation_git_blob": COLLECTOR_IMPLEMENTATION_GIT_BLOB,
        "collector_binding_git_blob": COLLECTOR_BINDING_GIT_BLOB,
        "source_only_provider_git_blob": SOURCE_ONLY_PROVIDER_GIT_BLOB,
        "worktree_adapter_git_blob": WORKTREE_ADAPTER_GIT_BLOB,
        "portable_attestation_git_blob": PORTABLE_ATTESTATION_GIT_BLOB,
        "activation_evidence_binding_git_blob": (
            ACTIVATION_EVIDENCE_BINDING_GIT_BLOB
        ),
        "canonical_live_collection_adapter_implementation_present": True,
        "canonical_live_collection_adapter_composition_implemented": True,
        "adapter_collection_requires_explicit_authority": True,
        "adapter_observation_requires_explicit_authority": True,
        "explicit_http_backend_injection_required": True,
        "explicit_docker_command_backend_injection_required": True,
        "supplied_worktree_receipt_required": True,
        "supplied_portable_binding_attestation_required": True,
        "automatic_host_backend_selection": False,
        "source_only_common_primitive_composition_implemented": True,
        "supplied_worktree_primitive_composition_implemented": True,
        "supplied_portable_attestation_composition_implemented": True,
        "bound_live_identity_composition_implemented": True,
        "collector_candidate_composition_implemented": True,
        "activation_evidence_admission_composition_implemented": True,
        "provider_capability_supported_primitive_count": 16,
        "provider_capability_remaining_unresolved_primitive_count": 0,
        "provider_capability_complete": True,
        "candidate_collector_identity_admission_implemented": True,
        "candidate_runtime_readiness_admission_implemented": True,
        "canonical_live_collection_adapter_source_binding_present": False,
        "canonical_live_collection_path_complete": False,
        "canonical_collection_enabled": False,
        "runtime_execution_authorized": False,
        "runtime_start_stop_reload_implemented": False,
        "model_load_implemented": False,
        "model_inference_implemented": False,
        "game_execution_implemented": False,
        "training_implemented": False,
        "deployment_implemented": False,
        "void_chain_mutation_implemented": False,
        "wallet_or_funds_action_implemented": False,
        "next_gate": NEXT_GATE,
        "next_change_class": (
            "source_only_canonical_live_collection_adapter_binding"
        ),
        "dependency_contracts": dependencies,
    }


def enable_canonical_live_collection(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13CanonicalLiveCollectionAdapterHold(NEXT_GATE)


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13CanonicalLiveCollectionAdapterHold(
        "V2R13_CANONICAL_ADAPTER_SOURCE_BINDING_AND_RUNTIME_ACTIVATION_GAPS_REMAIN"
    )
