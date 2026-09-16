"""Source-only binding for the reviewed V2R13 canonical live-collection adapter.

The adapter implementation was merged before this binding exists.  This separate
instrument pins that accepted implementation by exact Git blob and source
SHA-256, then validates only an already-supplied adapter candidate.

The binding never invokes the adapter collection entrypoint.  It performs no live
observation and never selects or calls HTTP, Ollama, Docker, filesystem, Git, or
portable-binding host backends.  It revalidates the supplied candidate through
the already-reviewed pure validation surfaces and deterministically recomputes
the collector candidate and activation-evidence admission from the supplied
source-bound primitive receipts.

A separately reviewed bound canonical collection entrypoint remains required
before canonical live collection can be enabled. Runtime execution remains
closed.
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
    abaddon_policy_campaign_runtime_v2r13_activation_evidence_collector_binding_generation2
    as activation_evidence_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_adapter_generation2
    as adapter,
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
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-canonical-live-collection-adapter-binding-contract.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-canonical-live-collection-adapter-bound-validation.v1"
)

ADAPTER_GIT_BLOB = "29c4bfa11a841359b6c4f4083659c78c474d94ba"
ADAPTER_SOURCE_SHA256 = (
    "a4236e3c727fcf6eee915ee9e3b44d2ba2e2666e8ac52499c9b342fd71935afb"
)
ACTIVATION_EVIDENCE_GIT_BLOB = "aac7964d9e80633535003b9f27066cac1bb4bac2"
ACTIVATION_EVIDENCE_BINDING_GIT_BLOB = (
    "ddda2bac0570f99295b2c15b2000baed8478aa4c"
)
COLLECTOR_IMPLEMENTATION_GIT_BLOB = "0003c24390194a4f621f13c6077e0604b9abcd98"
COLLECTOR_BINDING_GIT_BLOB = "bcc12598161a9516cb002d6e1c4eead7e914a425"
LIVE_BACKEND_BINDING_GIT_BLOB = "1a480133382dc878c79e110b8f6d8f30d0d7229d"
WORKTREE_ADAPTER_GIT_BLOB = "7e6f628c64fe02db42bd6adee67d3965e6b1ae92"
PORTABLE_ATTESTATION_GIT_BLOB = "afdc0421958565e713795dfd0d3c4c683041cc37"

NEXT_GATE = "V2R13_CANONICAL_LIVE_COLLECTION_ENTRYPOINT_REQUIRED"

EXPECTED_CANDIDATE_FIELDS = frozenset(
    {
        "schema",
        "snapshot_id",
        "collection_authorized",
        "observation_authorized",
        "explicit_http_backend_supplied",
        "explicit_docker_command_backend_supplied",
        "supplied_worktree_receipt_validated",
        "supplied_portable_binding_attestation_validated",
        "automatic_host_backend_selection",
        "primitive_receipt_count",
        "primitive_receipt_names",
        "provider_capability_supported_primitive_count",
        "provider_capability_remaining_unresolved_primitive_count",
        "provider_capability_complete",
        "activation_evidence_shape_valid",
        "collector_identity_admitted",
        "runtime_readiness_admitted",
        "live_observation_performed",
        "ollama_tags_request_performed",
        "ollama_ps_request_performed",
        "chat_completions_request_performed",
        "docker_metadata_command_count",
        "docker_mutating_command_performed",
        "worktree_observation_performed_by_adapter",
        "portable_binding_install_performed_by_adapter",
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "runtime_stop_performed",
        "runtime_reload_performed",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "policy_promotion_performed",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
        "canonical_live_collection_adapter_implementation_present",
        "canonical_live_collection_adapter_source_binding_present",
        "canonical_live_collection_path_complete",
        "canonical_collection_enabled",
        "runtime_execution_authorized",
        "holds",
        "worktree_validation",
        "portable_binding_validation",
        "live_backend_candidate",
        "live_backend_bound_validation",
        "collector_candidate",
        "activation_evidence",
        "activation_evidence_admission",
        "dependency_contracts",
    }
)

FALSE_ACTION_FIELDS = (
    "chat_completions_request_performed",
    "docker_mutating_command_performed",
    "worktree_observation_performed_by_adapter",
    "portable_binding_install_performed_by_adapter",
    "mutation_performed",
    "service_action_performed",
    "runtime_start_performed",
    "runtime_stop_performed",
    "runtime_reload_performed",
    "model_load_performed",
    "model_inference_performed",
    "game_execution_performed",
    "training_performed",
    "weights_updated",
    "policy_promotion_performed",
    "deployment_performed",
    "void_chain_mutation_performed",
    "wallet_or_funds_action_performed",
    "canonical_live_collection_adapter_source_binding_present",
    "canonical_live_collection_path_complete",
    "canonical_collection_enabled",
    "runtime_execution_authorized",
)


class RuntimeV2R13CanonicalLiveCollectionAdapterBindingHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13CanonicalLiveCollectionAdapterBindingHold(message)


def _validate_dependencies() -> dict[str, Any]:
    adapter_contract = adapter.v2r13_canonical_live_collection_adapter_contract()
    collector_contract = collector_binding.v2r13_collector_implementation_binding_contract()
    admission_contract = (
        activation_evidence_binding
        .v2r13_activation_evidence_collector_binding_contract()
    )
    live_binding_contract = (
        live_backend_binding.v2r13_live_collection_backend_binding_contract()
    )
    worktree_contract = worktree_adapter.v2r13_worktree_provider_adapter_contract()
    portable_contract = portable_attestation.v2r13_portable_binding_attestation_contract()

    _require(
        adapter_contract.get(
            "canonical_live_collection_adapter_implementation_present"
        )
        is True,
        "V2R13 canonical adapter implementation missing",
    )
    _require(
        adapter_contract.get(
            "canonical_live_collection_adapter_composition_implemented"
        )
        is True,
        "V2R13 canonical adapter composition missing",
    )
    _require(
        adapter_contract.get("adapter_collection_requires_explicit_authority")
        is True,
        "V2R13 adapter collection authority requirement lost",
    )
    _require(
        adapter_contract.get("adapter_observation_requires_explicit_authority")
        is True,
        "V2R13 adapter observation authority requirement lost",
    )
    _require(
        adapter_contract.get("explicit_http_backend_injection_required") is True,
        "V2R13 adapter HTTP injection requirement lost",
    )
    _require(
        adapter_contract.get("explicit_docker_command_backend_injection_required")
        is True,
        "V2R13 adapter Docker injection requirement lost",
    )
    _require(
        adapter_contract.get("automatic_host_backend_selection") is False,
        "V2R13 adapter automatic host selection enabled",
    )
    _require(
        adapter_contract.get(
            "canonical_live_collection_adapter_source_binding_present"
        )
        is False,
        "V2R13 adapter unexpectedly self-binds its source",
    )
    _require(
        adapter_contract.get("canonical_live_collection_path_complete") is False,
        "V2R13 canonical collection path unexpectedly complete before binding",
    )
    _require(
        adapter_contract.get("canonical_collection_enabled") is False,
        "V2R13 canonical collection unexpectedly enabled before binding",
    )
    _require(
        adapter_contract.get("runtime_execution_authorized") is False,
        "V2R13 adapter unexpectedly authorizes runtime execution",
    )
    _require(
        adapter_contract.get("next_gate")
        == "V2R13_CANONICAL_LIVE_COLLECTION_ADAPTER_SOURCE_BINDING_REQUIRED",
        "V2R13 adapter source-binding gate drift",
    )

    _require(
        collector_contract.get("canonical_primitive_source_bindings_present")
        is True,
        "V2R13 collector primitive source bindings missing",
    )
    _require(
        collector_contract.get("primitive_source_binding_count") == 16,
        "V2R13 collector primitive source-binding count drift",
    )
    _require(
        admission_contract.get("reviewed_collector_binding_present") is True,
        "V2R13 activation-evidence admission binding missing",
    )
    _require(
        admission_contract.get("collector_identity_admission_implemented") is True,
        "V2R13 collector identity admission missing",
    )
    _require(
        admission_contract.get("runtime_readiness_admission_implemented") is True,
        "V2R13 readiness admission missing",
    )
    _require(
        live_binding_contract.get(
            "canonical_live_collection_backend_source_binding_present"
        )
        is True,
        "V2R13 live-backend source binding missing",
    )
    _require(
        worktree_contract.get("six_worktree_primitives_implemented") is True,
        "V2R13 worktree adapter primitive coverage drift",
    )
    _require(
        portable_contract.get("supplied_attestation_validator_implemented") is True,
        "V2R13 portable attestation validator missing",
    )

    for label, contract in (
        ("adapter", adapter_contract),
        ("collector_binding", collector_contract),
        ("activation_evidence_binding", admission_contract),
        ("live_backend_binding", live_binding_contract),
        ("worktree_adapter", worktree_contract),
        ("portable_attestation", portable_contract),
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
        "adapter": deepcopy(adapter_contract),
        "collector_binding": deepcopy(collector_contract),
        "activation_evidence_binding": deepcopy(admission_contract),
        "live_backend_binding": deepcopy(live_binding_contract),
        "worktree_adapter": deepcopy(worktree_contract),
        "portable_attestation": deepcopy(portable_contract),
    }


def _validate_worktree_validation(value: Any) -> dict[str, Any]:
    expected = {
        "schema": worktree_adapter.worktree_observer.CONTRACT_SCHEMA,
        "receipt_valid": True,
        "path_classification_complete": True,
        "git_identity_complete": True,
        "activation_worktree_shape_complete": True,
        "canonical_provider_binding_present": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
    }
    _require(
        isinstance(value, Mapping) and dict(value) == expected,
        "V2R13 embedded worktree validation drift",
    )
    return deepcopy(expected)


def _validate_portable_validation(value: Any) -> dict[str, Any]:
    _require(
        isinstance(value, Mapping),
        "V2R13 embedded portable validation missing",
    )
    receipt = value.get("validated_receipt")
    _require(
        isinstance(receipt, Mapping),
        "V2R13 embedded portable validated receipt missing",
    )
    revalidated = portable_attestation.validate_v2r13_portable_binding_attestation(
        receipt
    )
    _require(
        dict(value) == revalidated,
        "V2R13 embedded portable validation mismatch",
    )
    return deepcopy(revalidated)


def _validate_live_binding(candidate: Mapping[str, Any]) -> dict[str, Any]:
    live_candidate = candidate.get("live_backend_candidate")
    _require(
        isinstance(live_candidate, Mapping),
        "V2R13 embedded live-backend candidate missing",
    )
    revalidated = live_backend_binding.validate_bound_live_collection_candidate(
        live_candidate,
        backend_source_sha256=adapter.LIVE_BACKEND_SOURCE_SHA256,
    )
    embedded = candidate.get("live_backend_bound_validation")
    _require(
        isinstance(embedded, Mapping) and dict(embedded) == revalidated,
        "V2R13 embedded live-backend bound validation mismatch",
    )
    return deepcopy(revalidated)


def _validate_primitive_receipts(
    collector_candidate: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    receipts = collector_candidate.get("primitive_receipts")
    _require(
        isinstance(receipts, list) and len(receipts) == 16,
        "V2R13 collector primitive receipt count drift",
    )

    required = collector_implementation.required_primitive_names(V2R13)
    bindings = collector_binding.reviewed_v2r13_primitive_source_bindings()
    _require(
        len(required) == 16 and len(bindings) == 16,
        "V2R13 reviewed primitive frontier drift",
    )

    result: dict[str, dict[str, Any]] = {}
    names: list[str] = []
    for receipt in receipts:
        _require(
            isinstance(receipt, Mapping),
            "V2R13 collector primitive receipt must be object",
        )
        name = receipt.get("primitive_name")
        _require(
            isinstance(name, str) and name in bindings,
            "V2R13 collector primitive receipt name drift",
        )
        _require(name not in result, f"duplicate V2R13 primitive receipt: {name}")
        _require(
            receipt.get("source_sha256") == bindings[name],
            f"V2R13 primitive source binding mismatch: {name}",
        )
        _require(
            receipt.get("schema")
            == collector_implementation.PRIMITIVE_RECEIPT_SCHEMA,
            f"V2R13 primitive receipt schema drift: {name}",
        )
        _require(
            receipt.get("snapshot_id") == V2R13,
            f"V2R13 primitive snapshot drift: {name}",
        )
        _require(
            receipt.get("observation_mode") == "read_only",
            f"V2R13 primitive observation mode drift: {name}",
        )
        for field in (
            "mutation_performed",
            "service_action_performed",
            "runtime_start_performed",
            "game_execution_performed",
            "model_inference_performed",
        ):
            _require(
                receipt.get(field) is False,
                f"V2R13 primitive crossed authority boundary: {name}:{field}",
            )
        names.append(name)
        result[name] = deepcopy(dict(receipt))

    _require(
        tuple(names) == required,
        "V2R13 collector primitive receipt ordering drift",
    )
    return result


def _recompute_collector_candidate(
    candidate: Mapping[str, Any],
) -> dict[str, Any]:
    collector_candidate = candidate.get("collector_candidate")
    _require(
        isinstance(collector_candidate, Mapping),
        "V2R13 embedded collector candidate missing",
    )
    receipts = _validate_primitive_receipts(collector_candidate)

    evidence = candidate.get("activation_evidence")
    _require(
        isinstance(evidence, Mapping),
        "V2R13 embedded activation evidence missing",
    )

    remove_top = {
        "collector_contract_sha256",
        *adapter.COMMON_PRIMITIVES,
        *adapter.LIVE_PRIMITIVES,
        adapter.PORTABLE_PRIMITIVE,
    }
    base_evidence = {
        key: deepcopy(value)
        for key, value in evidence.items()
        if key not in remove_top
    }

    bindings = collector_binding.reviewed_v2r13_primitive_source_bindings()

    def primitive_provider(
        snapshot_id: str,
        primitive_name: str,
    ) -> Mapping[str, Any]:
        _require(snapshot_id == V2R13, "V2R13 recompute snapshot drift")
        _require(
            primitive_name in receipts,
            f"V2R13 recompute primitive missing: {primitive_name}",
        )
        return deepcopy(receipts[primitive_name])

    recomputed = collector_implementation.collect_candidate_with_provider(
        V2R13,
        base_evidence,
        primitive_provider=primitive_provider,
        reviewed_primitive_source_bindings=bindings,
        collection_authorized=True,
    )
    _require(
        dict(collector_candidate) == recomputed,
        "V2R13 embedded collector candidate recomputation mismatch",
    )
    return deepcopy(recomputed)


def validate_bound_canonical_live_collection_adapter_candidate(
    candidate: Mapping[str, Any],
    *,
    adapter_source_sha256: str,
) -> dict[str, Any]:
    """Validate a supplied adapter candidate without performing live collection."""
    dependencies = _validate_dependencies()

    _require(
        isinstance(candidate, Mapping),
        "V2R13 bound canonical adapter candidate must be object",
    )
    _require(
        adapter_source_sha256 == ADAPTER_SOURCE_SHA256,
        "V2R13 canonical adapter source SHA mismatch",
    )
    _require(
        set(candidate) == EXPECTED_CANDIDATE_FIELDS,
        "V2R13 canonical adapter candidate field-set drift",
    )
    _require(
        candidate.get("schema") == adapter.COLLECTION_SCHEMA,
        "V2R13 canonical adapter candidate schema drift",
    )
    _require(
        candidate.get("snapshot_id") == V2R13,
        "V2R13 canonical adapter candidate snapshot drift",
    )

    for field in (
        "collection_authorized",
        "observation_authorized",
        "explicit_http_backend_supplied",
        "explicit_docker_command_backend_supplied",
        "supplied_worktree_receipt_validated",
        "supplied_portable_binding_attestation_validated",
        "provider_capability_complete",
        "activation_evidence_shape_valid",
        "collector_identity_admitted",
        "runtime_readiness_admitted",
        "live_observation_performed",
        "ollama_tags_request_performed",
        "ollama_ps_request_performed",
        "canonical_live_collection_adapter_implementation_present",
    ):
        _require(
            candidate.get(field) is True,
            f"V2R13 canonical adapter candidate missing true field: {field}",
        )

    _require(
        candidate.get("automatic_host_backend_selection") is False,
        "V2R13 canonical adapter candidate used automatic host selection",
    )
    _require(
        candidate.get("primitive_receipt_count") == 16,
        "V2R13 canonical adapter primitive receipt count drift",
    )
    expected_names = collector_implementation.required_primitive_names(V2R13)
    _require(
        tuple(candidate.get("primitive_receipt_names", ())) == expected_names,
        "V2R13 canonical adapter primitive-name order drift",
    )
    _require(
        candidate.get("provider_capability_supported_primitive_count") == 16,
        "V2R13 canonical adapter supported primitive count drift",
    )
    _require(
        candidate.get("provider_capability_remaining_unresolved_primitive_count")
        == 0,
        "V2R13 canonical adapter unresolved primitive count drift",
    )
    _require(
        candidate.get("docker_metadata_command_count") == 3,
        "V2R13 canonical adapter Docker metadata command count drift",
    )

    for field in FALSE_ACTION_FIELDS:
        _require(
            candidate.get(field) is False,
            f"V2R13 canonical adapter crossed boundary: {field}",
        )

    _require(
        list(candidate.get("holds", ()))
        == [
            "V2R13_CANONICAL_LIVE_COLLECTION_ADAPTER_SOURCE_BINDING_REQUIRED",
            RUNTIME_AUTHORITY_BLOCKER,
        ],
        "V2R13 canonical adapter hold set drift",
    )

    adapter_contract = dependencies["adapter"]
    _require(
        candidate.get("dependency_contracts")
        == adapter_contract.get("dependency_contracts"),
        "V2R13 canonical adapter dependency snapshot drift",
    )

    worktree_validation = _validate_worktree_validation(
        candidate.get("worktree_validation")
    )
    portable_validation = _validate_portable_validation(
        candidate.get("portable_binding_validation")
    )
    live_validation = _validate_live_binding(candidate)
    collector_candidate = _recompute_collector_candidate(candidate)

    evidence = candidate.get("activation_evidence")
    shape = activation_evidence.validate_evidence_shape(evidence)
    _require(
        shape.get("evidence_shape_valid") is True,
        "V2R13 bound adapter activation-evidence shape invalid",
    )

    admission = activation_evidence_binding.admit_bound_v2r13_evidence(evidence)
    embedded_admission = candidate.get("activation_evidence_admission")
    _require(
        isinstance(embedded_admission, Mapping)
        and dict(embedded_admission) == admission,
        "V2R13 embedded activation-evidence admission mismatch",
    )
    _require(
        admission.get("collector_identity_admitted") is True,
        "V2R13 bound adapter collector identity not admitted",
    )
    _require(
        admission.get("runtime_readiness_admitted") is True,
        "V2R13 bound adapter runtime readiness not admitted",
    )
    _require(
        admission.get("runtime_execution_authorized") is False,
        "V2R13 bound adapter unexpectedly authorizes runtime execution",
    )

    _require(
        collector_candidate.get("activation_evidence_candidate") == evidence,
        "V2R13 collector/evidence identity mismatch",
    )

    return {
        "schema": VALIDATION_SCHEMA,
        "snapshot_id": V2R13,
        "canonical_live_collection_adapter_source_binding_present": True,
        "bound_adapter_candidate_valid": True,
        "adapter_source_sha256": ADAPTER_SOURCE_SHA256,
        "adapter_git_blob": ADAPTER_GIT_BLOB,
        "supplied_live_observation_validated": True,
        "supplied_live_observation_performed": True,
        "binding_live_observation_performed": False,
        "binding_adapter_invocation_performed": False,
        "binding_http_request_performed": False,
        "binding_ollama_request_performed": False,
        "binding_docker_command_performed": False,
        "binding_worktree_observation_performed": False,
        "binding_portable_install_performed": False,
        "provider_capability_supported_primitive_count": 16,
        "provider_capability_remaining_unresolved_primitive_count": 0,
        "provider_capability_complete": True,
        "collector_identity_admitted": True,
        "runtime_readiness_admitted": True,
        "canonical_live_collection_path_complete": False,
        "canonical_collection_enabled": False,
        "runtime_execution_authorized": False,
        "next_gate": NEXT_GATE,
        "holds": [NEXT_GATE, RUNTIME_AUTHORITY_BLOCKER],
        "worktree_validation": worktree_validation,
        "portable_binding_validation": portable_validation,
        "live_backend_bound_validation": live_validation,
        "collector_candidate": collector_candidate,
        "activation_evidence_admission": deepcopy(admission),
        "validated_candidate": deepcopy(dict(candidate)),
    }


def v2r13_canonical_live_collection_adapter_binding_contract() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "snapshot_id": V2R13,
        "adapter_git_blob": ADAPTER_GIT_BLOB,
        "adapter_source_sha256": ADAPTER_SOURCE_SHA256,
        "adapter_source_identity_pinned_by_git_blob": True,
        "adapter_source_identity_pinned_by_sha256": True,
        "adapter_source_is_not_self_bound": True,
        "separate_binding_instrument": True,
        "canonical_live_collection_adapter_source_binding_present": True,
        "supplied_bound_adapter_candidate_validator_implemented": True,
        "binding_adapter_invocation_implemented": False,
        "binding_live_observation_implemented": False,
        "binding_http_request_implemented": False,
        "binding_ollama_request_implemented": False,
        "binding_docker_command_implemented": False,
        "binding_worktree_observation_implemented": False,
        "binding_portable_install_implemented": False,
        "adapter_collection_requires_explicit_authority": True,
        "adapter_observation_requires_explicit_authority": True,
        "explicit_http_backend_injection_required": True,
        "explicit_docker_command_backend_injection_required": True,
        "supplied_worktree_receipt_required": True,
        "supplied_portable_binding_attestation_required": True,
        "automatic_host_backend_selection": False,
        "provider_capability_supported_primitive_count": 16,
        "provider_capability_remaining_unresolved_primitive_count": 0,
        "provider_capability_complete": True,
        "bound_candidate_collector_identity_admission_implemented": True,
        "bound_candidate_runtime_readiness_admission_implemented": True,
        "canonical_live_collection_path_complete": False,
        "canonical_collection_enabled": False,
        "runtime_execution_authorized": False,
        "next_gate": NEXT_GATE,
        "next_change_class": (
            "explicit_authority_bound_canonical_live_collection_entrypoint"
        ),
        "dependency_contracts": dependencies,
    }


def collect_bound_canonical_live_collection(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13CanonicalLiveCollectionAdapterBindingHold(
        "GENERATION2_V2R13_BOUND_CANONICAL_LIVE_COLLECTION_ENTRYPOINT_NOT_IMPLEMENTED"
    )


def enable_canonical_live_collection(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13CanonicalLiveCollectionAdapterBindingHold(NEXT_GATE)


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13CanonicalLiveCollectionAdapterBindingHold(
        "V2R13_CANONICAL_COLLECTION_ENTRYPOINT_AND_RUNTIME_ACTIVATION_GAPS_REMAIN"
    )
