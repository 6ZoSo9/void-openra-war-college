"""Explicit-authority read-only live-collection backend for V2R13 Generation-2.

This module composes the already-reviewed V2R13 Ollama read-only observer and
rootless-Docker runtime-image backend into one candidate live-identity collection
surface for the final three live primitives:

* endpoint_liveness
* model_identity_verified
* runtime_image_identity_verified

Collection is impossible unless the caller explicitly supplies:

* ``observation_authorized=True``;
* an HTTP GET backend; and
* a Docker metadata command backend.

The module never selects host backends automatically. It never calls the
chat-completions inference route. The Docker path is restricted by the reviewed
backend to context/info/image-inspect metadata operations.

The resulting three primitive receipts use the already-reviewed per-primitive
source bindings expected by the Generation-2 collector implementation. This
source is not self-admitted: canonical live collection remains disabled until a
separate source-binding instrument reviews and pins this implementation.

No runtime start/stop/reload, model load/inference, game execution, training,
deployment, VOID mutation, or funds action is implemented here.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_collector_implementation_generation2
    as collector_implementation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_collector_implementation_binding_generation2
    as collector_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_ollama_observer_binding_generation2
    as ollama_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_ollama_readonly_observer_generation2
    as ollama_observer,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_post_admission_reconciliation_generation2
    as post_admission_reconciliation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_rootless_docker_image_backend_binding_generation2
    as docker_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_rootless_docker_image_backend_generation2
    as docker_backend,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    RUNTIME_AUTHORITY_BLOCKER,
    V2R13,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-live-collection-backend-contract.v1"
)
COLLECTION_SCHEMA = (
    "void.abaddon.generation2.v2r13-live-collection-candidate.v1"
)

POST_ADMISSION_RECONCILIATION_GIT_BLOB = (
    "fea52c8faf483e85f207ed65a384f34222d4c07a"
)
COLLECTOR_IMPLEMENTATION_BINDING_GIT_BLOB = (
    "bcc12598161a9516cb002d6e1c4eead7e914a425"
)
OLLAMA_OBSERVER_GIT_BLOB = "9b859e91b8833260a1af7e189ec5cd30d92d9451"
OLLAMA_BINDING_GIT_BLOB = "58364a1d5d71aead9df6dc0fc61661a557131508"
ROOTLESS_DOCKER_BACKEND_GIT_BLOB = (
    "488497f723ad5bc5ca63b3b2d69cece26bddaaa5"
)
ROOTLESS_DOCKER_BINDING_GIT_BLOB = (
    "7075ded7a19454239b95a09e7b4630413124a796"
)

POST_ADMISSION_RECONCILIATION_SOURCE_SHA256 = (
    "8548a745b617b46a72faf8b4f8b196916caf3e51c5c924a0dc68b3547a282346"
)
COLLECTOR_IMPLEMENTATION_BINDING_SOURCE_SHA256 = (
    "af4a51207a0ad1477eedd18c325ee1df2231b6ad990bbb6f4f8ba53ef5bffc1d"
)
OLLAMA_OBSERVER_SOURCE_SHA256 = (
    "c770d08621ff1d32996e64962bd539c783bd4ba5c259687d1a348a2db775a7ff"
)
OLLAMA_BINDING_SOURCE_SHA256 = (
    "c6b0bb746d017326e600f401a2d07a29fba79aced401687c4eb5238084ee9335"
)
ROOTLESS_DOCKER_BACKEND_SOURCE_SHA256 = (
    "25e8f41dcea700860ec1b97726b321a99c2622e00ddba12433246c7b121b11f6"
)
ROOTLESS_DOCKER_BINDING_SOURCE_SHA256 = (
    "74acc7248ee19d2d141aa4ec36fc3ce1c6068c56ca1801719c3287cd2c774f52"
)

LIVE_PRIMITIVES = (
    "endpoint_liveness",
    "model_identity_verified",
    "runtime_image_identity_verified",
)


class RuntimeV2R13LiveCollectionBackendHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13LiveCollectionBackendHold(message)


def _validate_dependencies() -> dict[str, Any]:
    reconciliation = (
        post_admission_reconciliation.v2r13_post_admission_reconciliation_contract()
    )
    collector = collector_binding.v2r13_collector_implementation_binding_contract()
    observer = ollama_observer.v2r13_ollama_readonly_observer_contract()
    observer_binding = ollama_binding.v2r13_ollama_observer_binding_contract()
    image_backend = docker_backend.v2r13_rootless_docker_image_backend_contract()
    image_binding = docker_binding.v2r13_rootless_docker_image_backend_binding_contract()

    _require(
        reconciliation.get("next_gate")
        == "V2R13_LIVE_COLLECTION_BACKEND_IMPLEMENTATION_REQUIRED",
        "post-admission reconciliation gate drift",
    )
    _require(
        reconciliation.get("canonical_live_collection_path_complete") is False,
        "post-admission reconciliation unexpectedly completes live collection",
    )
    _require(
        reconciliation.get("runtime_execution_authorized") is False,
        "post-admission reconciliation unexpectedly authorizes runtime",
    )

    primitive_bindings = collector_binding.reviewed_v2r13_primitive_source_bindings()
    _require(
        primitive_bindings.get("endpoint_liveness") == OLLAMA_BINDING_SOURCE_SHA256,
        "endpoint primitive source binding drift",
    )
    _require(
        primitive_bindings.get("model_identity_verified")
        == OLLAMA_BINDING_SOURCE_SHA256,
        "model primitive source binding drift",
    )
    _require(
        primitive_bindings.get("runtime_image_identity_verified")
        == ROOTLESS_DOCKER_BINDING_SOURCE_SHA256,
        "runtime-image primitive source binding drift",
    )
    _require(
        collector.get("canonical_primitive_source_bindings_present") is True,
        "collector primitive source bindings are not canonical",
    )
    _require(
        collector.get("canonical_collection_enabled") is False,
        "collector binding unexpectedly enables collection",
    )

    _require(
        observer.get("endpoint_liveness_observer_candidate_implemented") is True,
        "Ollama endpoint observer candidate missing",
    )
    _require(
        observer.get("running_model_identity_observer_candidate_implemented") is True,
        "Ollama model observer candidate missing",
    )
    _require(
        observer.get("observation_requires_explicit_authority") is True,
        "Ollama explicit observation authority requirement lost",
    )
    _require(
        observer.get("host_http_backend_factory_present") is True,
        "Ollama host HTTP backend factory missing",
    )
    _require(
        observer.get("automatic_host_backend_selection") is False,
        "Ollama automatic host backend selection enabled",
    )
    _require(
        observer.get("chat_completions_forbidden") is True,
        "Ollama chat-completions prohibition lost",
    )

    _require(
        observer_binding.get("canonical_observer_source_binding_present") is True,
        "Ollama observer source binding missing",
    )
    _require(
        observer_binding.get("supplied_bound_observation_validator_implemented") is True,
        "Ollama bound observation validator missing",
    )
    _require(
        observer_binding.get("binding_live_observation_implemented") is False,
        "Ollama binding unexpectedly performs live observation itself",
    )

    _require(
        image_backend.get("candidate_backend_implemented") is True,
        "rootless-Docker image backend candidate missing",
    )
    _require(
        image_backend.get("reviewed_source_binding_required") is True,
        "rootless-Docker reviewed source binding requirement lost",
    )
    _require(
        image_backend.get("canonical_backend_source_binding_present") is False,
        "rootless-Docker backend unexpectedly self-bound",
    )
    _require(
        image_backend.get("automatic_host_backend_selection") is False,
        "rootless-Docker backend automatic selection enabled",
    )

    _require(
        image_binding.get("canonical_backend_source_binding_present") is True,
        "rootless-Docker backend source binding missing",
    )
    _require(
        image_binding.get("supplied_bound_receipt_validator_implemented") is True,
        "rootless-Docker bound receipt validator missing",
    )
    _require(
        image_binding.get("binding_live_observation_implemented") is False,
        "rootless-Docker binding unexpectedly performs live observation itself",
    )

    for label, contract in (
        ("reconciliation", reconciliation),
        ("collector_binding", collector),
        ("observer", observer),
        ("observer_binding", observer_binding),
        ("image_backend", image_backend),
        ("image_binding", image_binding),
    ):
        _require(
            contract.get("runtime_execution_authorized") is False,
            f"{label} unexpectedly authorizes runtime execution",
        )

    return {
        "post_admission_reconciliation": deepcopy(reconciliation),
        "collector_implementation_binding": deepcopy(collector),
        "ollama_observer": deepcopy(observer),
        "ollama_observer_binding": deepcopy(observer_binding),
        "rootless_docker_backend": deepcopy(image_backend),
        "rootless_docker_binding": deepcopy(image_binding),
    }


def _primitive_receipt(
    *,
    primitive_name: str,
    source_sha256: str,
    value: Any,
) -> dict[str, Any]:
    _require(
        primitive_name in LIVE_PRIMITIVES,
        f"unsupported live primitive: {primitive_name!r}",
    )
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


def collect_v2r13_live_identity_candidate(
    *,
    observation_authorized: bool,
    http_get: Any,
    run_command: Any,
) -> dict[str, Any]:
    """Perform only explicitly authorized read-only V2R13 identity observation."""
    _require(
        observation_authorized is True,
        "GENERATION2_V2R13_LIVE_COLLECTION_NOT_AUTHORIZED",
    )
    _require(callable(http_get), "explicit V2R13 HTTP GET backend required")
    _require(callable(run_command), "explicit V2R13 Docker command backend required")

    dependencies = _validate_dependencies()

    ollama_raw = ollama_observer.observe_v2r13_ollama_readonly(
        observation_authorized=True,
        http_get=http_get,
    )
    ollama_validated = ollama_binding.validate_bound_ollama_observation(
        ollama_raw,
        observer_source_sha256=OLLAMA_OBSERVER_SOURCE_SHA256,
    )

    image_raw = docker_backend.collect_rootless_docker_runtime_image_receipt(
        observation_authorized=True,
        reviewed_source_sha256=ROOTLESS_DOCKER_BACKEND_SOURCE_SHA256,
        run_command=run_command,
    )

    # The reviewed Docker backend intentionally returns one non-canonical
    # diagnostic field ("_candidate_metadata") in addition to the canonical
    # runtime-image receipt. The binding validator is deliberately exact-field
    # fail-closed, so strip only that reviewed diagnostic envelope before
    # admission and preserve it separately for auditability.
    _require(
        set(image_raw)
        == set(docker_binding.runtime_image_interface.BACKEND_RECEIPT_FIELDS)
        | {"_candidate_metadata"},
        "rootless-Docker candidate receipt field-set drift",
    )
    image_receipt = {
        field: deepcopy(image_raw[field])
        for field in docker_binding.runtime_image_interface.BACKEND_RECEIPT_FIELDS
    }
    image_metadata = deepcopy(image_raw["_candidate_metadata"])

    image_validated = docker_binding.validate_bound_runtime_image_receipt(
        image_receipt
    )

    _require(
        ollama_validated.get("endpoint_liveness_verified") is True,
        "bound Ollama endpoint liveness was not verified",
    )
    _require(
        ollama_validated.get("model_identity_verified") is True,
        "bound Ollama model identity was not verified",
    )
    _require(
        image_validated.get("runtime_image_identity_verified") is True,
        "bound runtime-image identity was not verified",
    )

    primitive_values = {
        "endpoint_liveness": True,
        "model_identity_verified": True,
        "runtime_image_identity_verified": True,
    }
    primitive_receipts = {
        "endpoint_liveness": _primitive_receipt(
            primitive_name="endpoint_liveness",
            source_sha256=OLLAMA_BINDING_SOURCE_SHA256,
            value=True,
        ),
        "model_identity_verified": _primitive_receipt(
            primitive_name="model_identity_verified",
            source_sha256=OLLAMA_BINDING_SOURCE_SHA256,
            value=True,
        ),
        "runtime_image_identity_verified": _primitive_receipt(
            primitive_name="runtime_image_identity_verified",
            source_sha256=ROOTLESS_DOCKER_BINDING_SOURCE_SHA256,
            value=True,
        ),
    }

    return {
        "schema": COLLECTION_SCHEMA,
        "snapshot_id": V2R13,
        "observation_mode": "read_only",
        "observation_authorized": True,
        "explicit_http_backend_supplied": True,
        "explicit_docker_command_backend_supplied": True,
        "automatic_host_backend_selection": False,
        "primitive_values": deepcopy(primitive_values),
        "primitive_receipts": deepcopy(primitive_receipts),
        "live_primitive_count": 3,
        "provider_capability_supported_primitive_count": 16,
        "provider_capability_remaining_unresolved_primitive_count": 0,
        "provider_capability_complete": True,
        "live_observation_performed": True,
        "ollama_tags_request_performed": True,
        "ollama_ps_request_performed": True,
        "chat_completions_request_performed": False,
        "rootless_docker_context_inspect_performed": True,
        "rootless_docker_info_performed": True,
        "rootless_docker_image_inspect_performed": True,
        "docker_mutating_command_performed": False,
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
        "live_collection_backend_source_binding_present": False,
        "canonical_live_collection_path_complete": False,
        "canonical_collection_enabled": False,
        "collector_identity_admitted_by_backend": False,
        "runtime_readiness_admitted_by_backend": False,
        "runtime_execution_authorized": False,
        "holds": [
            "V2R13_LIVE_COLLECTION_BACKEND_SOURCE_BINDING_REQUIRED",
            "V2R13_CANONICAL_COLLECTION_NOT_ENABLED",
            RUNTIME_AUTHORITY_BLOCKER,
        ],
        "ollama_observation": deepcopy(ollama_raw),
        "ollama_bound_validation": deepcopy(ollama_validated),
        "runtime_image_receipt": deepcopy(image_receipt),
        "runtime_image_candidate_metadata": deepcopy(image_metadata),
        "runtime_image_bound_validation": deepcopy(image_validated),
        "dependency_contracts": dependencies,
    }


def v2r13_live_collection_backend_contract() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "snapshot_id": V2R13,
        "post_admission_reconciliation_git_blob": (
            POST_ADMISSION_RECONCILIATION_GIT_BLOB
        ),
        "post_admission_reconciliation_source_sha256": (
            POST_ADMISSION_RECONCILIATION_SOURCE_SHA256
        ),
        "collector_implementation_binding_git_blob": (
            COLLECTOR_IMPLEMENTATION_BINDING_GIT_BLOB
        ),
        "collector_implementation_binding_source_sha256": (
            COLLECTOR_IMPLEMENTATION_BINDING_SOURCE_SHA256
        ),
        "ollama_observer_git_blob": OLLAMA_OBSERVER_GIT_BLOB,
        "ollama_observer_source_sha256": OLLAMA_OBSERVER_SOURCE_SHA256,
        "ollama_binding_git_blob": OLLAMA_BINDING_GIT_BLOB,
        "ollama_binding_source_sha256": OLLAMA_BINDING_SOURCE_SHA256,
        "rootless_docker_backend_git_blob": ROOTLESS_DOCKER_BACKEND_GIT_BLOB,
        "rootless_docker_backend_source_sha256": (
            ROOTLESS_DOCKER_BACKEND_SOURCE_SHA256
        ),
        "rootless_docker_binding_git_blob": ROOTLESS_DOCKER_BINDING_GIT_BLOB,
        "rootless_docker_binding_source_sha256": (
            ROOTLESS_DOCKER_BINDING_SOURCE_SHA256
        ),
        "live_collection_backend_implementation_present": True,
        "live_collection_backend_composition_implemented": True,
        "live_collection_backend_requires_explicit_authority": True,
        "explicit_http_backend_injection_required": True,
        "explicit_docker_command_backend_injection_required": True,
        "automatic_host_backend_selection": False,
        "ollama_observer_invocation_implemented": True,
        "rootless_docker_backend_invocation_implemented": True,
        "chat_completions_forbidden": True,
        "live_primitive_names": LIVE_PRIMITIVES,
        "live_primitive_count": 3,
        "provider_capability_supported_primitive_count": 16,
        "provider_capability_remaining_unresolved_primitive_count": 0,
        "provider_capability_complete": True,
        "collector_primitive_receipt_composition_implemented": True,
        "live_collection_backend_source_binding_present": False,
        "canonical_live_collection_path_complete": False,
        "canonical_collection_enabled": False,
        "collector_identity_admission_implemented_by_backend": False,
        "runtime_readiness_admission_implemented_by_backend": False,
        "runtime_execution_authorized": False,
        "runtime_start_stop_reload_implemented": False,
        "model_load_implemented": False,
        "model_inference_implemented": False,
        "game_execution_implemented": False,
        "training_implemented": False,
        "deployment_implemented": False,
        "void_chain_mutation_implemented": False,
        "wallet_or_funds_action_implemented": False,
        "next_gate": "V2R13_LIVE_COLLECTION_BACKEND_SOURCE_BINDING_REQUIRED",
        "next_change_class": "source_only_live_collection_backend_binding",
        "dependency_contracts": dependencies,
    }


def enable_canonical_live_collection(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13LiveCollectionBackendHold(
        "V2R13_LIVE_COLLECTION_BACKEND_SOURCE_BINDING_REQUIRED"
    )


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13LiveCollectionBackendHold(
        "V2R13_LIVE_COLLECTION_SOURCE_BINDING_AND_RUNTIME_ACTIVATION_GAPS_REMAIN"
    )
