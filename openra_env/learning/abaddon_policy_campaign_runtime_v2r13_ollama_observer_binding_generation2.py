"""Source-only canonical binding for the V2R13 Ollama read-only observer.

This is the separate review/source-binding instrument for the already-merged
V2R13 Ollama observer. It pins that observer by BOTH:

* canonical Git blob identity; and
* reviewed source SHA-256.

The observer was merged before this file exists, so this binding is not
self-referential.

The bound observer is the reviewed provider candidate for the two V2R13
identity primitives that remain after canonical runtime-image binding:

* endpoint_liveness
* model_identity_verified

This module performs no HTTP request and never invokes the observer's host HTTP
backend. It validates only an already-supplied exact observer result and admits
those two provider primitives only after the pinned observer source identity is
supplied.

The previously canonical runtime-image provider remains a dependency. With all
three live-identity provider primitives implemented, capability coverage becomes
16/16; nevertheless full collector identity, canonical provider binding,
canonical collection, runtime readiness, and runtime execution remain closed.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_activation_contract_generation2
    as activation_contract,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_ollama_readonly_observer_generation2
    as ollama_observer,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_rootless_docker_image_backend_binding_generation2
    as runtime_image_binding,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-ollama-observer-binding-contract.v1"
)
VALIDATION_SCHEMA = (
    "void.abaddon.generation2.v2r13-ollama-observer-bound-validation.v1"
)

ACTIVATION_CONTRACT_GIT_BLOB = "a3acb42280c334daa24a3b830105a04666fd603b"
OLLAMA_OBSERVER_GIT_BLOB = "9b859e91b8833260a1af7e189ec5cd30d92d9451"
RUNTIME_IMAGE_BINDING_GIT_BLOB = "7075ded7a19454239b95a09e7b4630413124a796"

OLLAMA_OBSERVER_SOURCE_SHA256 = (
    "c770d08621ff1d32996e64962bd539c783bd4ba5c259687d1a348a2db775a7ff"
)
RUNTIME_IMAGE_BINDING_SOURCE_SHA256 = (
    "74acc7248ee19d2d141aa4ec36fc3ce1c6068c56ca1801719c3287cd2c774f52"
)

BASELINE_SUPPORTED_COUNT = 14
BOUND_SUPPORTED_COUNT = 16
BOUND_REMAINING_UNRESOLVED: tuple[str, ...] = ()

ENDPOINT_PRIMITIVE = "endpoint_liveness"
MODEL_PRIMITIVE = "model_identity_verified"


class RuntimeV2R13OllamaObserverBindingHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13OllamaObserverBindingHold(message)


def _validate_dependency_contracts() -> dict[str, Any]:
    observer = ollama_observer.v2r13_ollama_readonly_observer_contract()
    image_binding = (
        runtime_image_binding.v2r13_rootless_docker_image_backend_binding_contract()
    )

    _require(
        observer.get("endpoint_liveness_observer_candidate_implemented") is True,
        "V2R13 Ollama endpoint observer candidate missing",
    )
    _require(
        observer.get("running_model_identity_observer_candidate_implemented") is True,
        "V2R13 Ollama model observer candidate missing",
    )
    _require(
        observer.get("runtime_image_identity_observer_implemented") is False,
        "V2R13 Ollama observer unexpectedly implements runtime-image identity",
    )
    _require(
        observer.get("host_http_backend_factory_present") is True,
        "V2R13 Ollama host HTTP backend factory missing",
    )
    _require(
        observer.get("automatic_host_backend_selection") is False,
        "V2R13 Ollama automatic host backend selection enabled",
    )
    _require(
        observer.get("observation_requires_explicit_authority") is True,
        "V2R13 Ollama observation authority requirement lost",
    )
    _require(
        observer.get("chat_completions_forbidden") is True,
        "V2R13 Ollama chat-completions prohibition lost",
    )

    _require(
        image_binding.get("canonical_backend_source_binding_present") is True,
        "V2R13 runtime-image source binding is not canonical",
    )
    _require(
        image_binding.get("runtime_image_identity_provider_primitive_implemented")
        is True,
        "V2R13 runtime-image provider primitive missing",
    )
    _require(
        image_binding.get("supported_primitive_count_after_binding")
        == BASELINE_SUPPORTED_COUNT,
        "V2R13 post-image-binding supported count drift",
    )
    _require(
        image_binding.get("remaining_unresolved_primitive_count") == 2,
        "V2R13 post-image-binding unresolved count drift",
    )
    _require(
        tuple(image_binding.get("remaining_unresolved_primitive_names", ()))
        == (
            ENDPOINT_PRIMITIVE,
            MODEL_PRIMITIVE,
        ),
        "V2R13 post-image-binding unresolved set drift",
    )
    _require(
        image_binding.get("canonical_provider_binding_present") is False,
        "V2R13 runtime-image binding unexpectedly admits canonical provider",
    )
    _require(
        image_binding.get("runtime_readiness_admitted") is False,
        "V2R13 runtime-image binding unexpectedly admits readiness",
    )

    return {
        "observer": deepcopy(observer),
        "runtime_image_binding": deepcopy(image_binding),
    }


def _validate_exact_observation_fields(observation: Mapping[str, Any]) -> None:
    expected_fields = {
        "schema",
        "snapshot_id",
        "observation_mode",
        "tags_url",
        "ps_url",
        "chat_completions_url",
        "chat_completions_request_performed",
        "endpoint_liveness_observed",
        "catalog_model_alias",
        "catalog_model_digest",
        "running_model_alias",
        "running_model_digest",
        "model_catalog_identity_matches_expected",
        "running_model_identity_matches_expected",
        "model_identity_observation_performed",
        "runtime_image_identity_observation_performed",
        "runtime_image_id",
        "runtime_image_identity_verified",
        "collector_identity_admitted",
        "canonical_provider_binding_present",
        "runtime_readiness_admitted",
        "runtime_execution_authorized",
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "runtime_stop_performed",
        "runtime_reload_performed",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
    }
    _require(
        set(observation) == expected_fields,
        "V2R13 bound Ollama observation field-set drift",
    )


def validate_bound_ollama_observation(
    observation: Mapping[str, Any],
    *,
    observer_source_sha256: str,
) -> dict[str, Any]:
    """Admit endpoint + model provider primitives from supplied bound evidence."""
    dependencies = _validate_dependency_contracts()

    _require(
        isinstance(observation, Mapping),
        "V2R13 bound Ollama observation must be object",
    )
    _require(
        observer_source_sha256 == OLLAMA_OBSERVER_SOURCE_SHA256,
        "V2R13 bound Ollama observer source SHA mismatch",
    )
    _validate_exact_observation_fields(observation)

    _require(
        observation.get("schema") == ollama_observer.OBSERVATION_SCHEMA,
        "V2R13 bound Ollama observation schema drift",
    )
    _require(
        observation.get("snapshot_id") == activation_contract.V2R13,
        "V2R13 bound Ollama snapshot drift",
    )
    _require(
        observation.get("observation_mode") == "read_only",
        "V2R13 bound Ollama observation mode must be read_only",
    )

    _require(
        observation.get("tags_url") == ollama_observer.OLLAMA_TAGS_URL,
        "V2R13 bound Ollama tags URL drift",
    )
    _require(
        observation.get("ps_url") == ollama_observer.OLLAMA_PS_URL,
        "V2R13 bound Ollama ps URL drift",
    )
    _require(
        observation.get("chat_completions_url")
        == ollama_observer.FORBIDDEN_CHAT_COMPLETIONS_URL,
        "V2R13 bound Ollama chat-completions URL drift",
    )
    _require(
        observation.get("chat_completions_request_performed") is False,
        "V2R13 bound Ollama chat-completions request performed",
    )

    _require(
        observation.get("endpoint_liveness_observed") is True,
        "V2R13 bound Ollama endpoint liveness not observed",
    )
    _require(
        observation.get("catalog_model_alias")
        == activation_contract.V2R13_MODEL_ALIAS,
        "V2R13 bound Ollama catalog model alias drift",
    )
    _require(
        observation.get("catalog_model_digest")
        == activation_contract.V2R13_MODEL_DIGEST,
        "V2R13 bound Ollama catalog model digest drift",
    )
    _require(
        observation.get("running_model_alias")
        == activation_contract.V2R13_MODEL_ALIAS,
        "V2R13 bound Ollama running model alias drift",
    )
    _require(
        observation.get("running_model_digest")
        == activation_contract.V2R13_MODEL_DIGEST,
        "V2R13 bound Ollama running model digest drift",
    )
    _require(
        observation.get("model_catalog_identity_matches_expected") is True,
        "V2R13 bound Ollama catalog identity mismatch",
    )
    _require(
        observation.get("running_model_identity_matches_expected") is True,
        "V2R13 bound Ollama running identity mismatch",
    )
    _require(
        observation.get("model_identity_observation_performed") is True,
        "V2R13 bound Ollama model identity observation missing",
    )

    _require(
        observation.get("runtime_image_identity_observation_performed") is False,
        "V2R13 Ollama observer crossed into runtime-image observation",
    )
    _require(
        observation.get("runtime_image_id") is None,
        "V2R13 Ollama observer unexpectedly reports runtime-image ID",
    )
    _require(
        observation.get("runtime_image_identity_verified") is False,
        "V2R13 Ollama observer unexpectedly verifies runtime image",
    )

    for field in (
        "collector_identity_admitted",
        "canonical_provider_binding_present",
        "runtime_readiness_admitted",
        "runtime_execution_authorized",
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "runtime_stop_performed",
        "runtime_reload_performed",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
    ):
        _require(
            observation.get(field) is False,
            f"V2R13 bound Ollama observation crossed boundary: {field}",
        )

    primitive_values = {
        ENDPOINT_PRIMITIVE: True,
        MODEL_PRIMITIVE: True,
    }

    return {
        "schema": VALIDATION_SCHEMA,
        "snapshot_id": activation_contract.V2R13,
        "reviewed_observer_source_sha256": OLLAMA_OBSERVER_SOURCE_SHA256,
        "reviewed_observer_git_blob": OLLAMA_OBSERVER_GIT_BLOB,
        "canonical_observer_source_binding_present": True,
        "endpoint_liveness_verified": True,
        "model_identity_verified": True,
        "runtime_image_identity_provider_already_canonical": True,
        "primitive_values": primitive_values,
        "supported_primitive_count_after_binding": BOUND_SUPPORTED_COUNT,
        "remaining_unresolved_primitive_names": BOUND_REMAINING_UNRESOLVED,
        "remaining_unresolved_primitive_count": 0,
        "all_v2r13_provider_primitives_implemented": True,
        "full_collector_identity_admitted": False,
        "canonical_provider_binding_present": False,
        "canonical_collection_enabled": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "binding_http_request_performed": False,
        "binding_host_backend_invocation_performed": False,
        "binding_filesystem_observation_performed": False,
        "binding_git_query_performed": False,
        "binding_subprocess_execution_performed": False,
        "binding_model_inference_performed": False,
        "binding_game_execution_performed": False,
        "validated_observation": deepcopy(dict(observation)),
        "dependency_contracts": dependencies,
    }


def v2r13_ollama_observer_binding_contract() -> dict[str, Any]:
    dependencies = _validate_dependency_contracts()

    return {
        "schema": CONTRACT_SCHEMA,
        "activation_contract_git_blob": ACTIVATION_CONTRACT_GIT_BLOB,
        "ollama_observer_git_blob": OLLAMA_OBSERVER_GIT_BLOB,
        "runtime_image_binding_git_blob": RUNTIME_IMAGE_BINDING_GIT_BLOB,
        "ollama_observer_source_sha256": OLLAMA_OBSERVER_SOURCE_SHA256,
        "runtime_image_binding_source_sha256": (
            RUNTIME_IMAGE_BINDING_SOURCE_SHA256
        ),
        "snapshot_id": activation_contract.V2R13,
        "separate_binding_instrument": True,
        "observer_source_identity_pinned_by_git_blob": True,
        "observer_source_identity_pinned_by_sha256": True,
        "observer_source_is_not_self_bound": True,
        "canonical_observer_source_binding_present": True,
        "supplied_bound_observation_validator_implemented": True,
        "endpoint_liveness_provider_primitive_implemented": True,
        "model_identity_provider_primitive_implemented": True,
        "runtime_image_identity_provider_already_implemented": True,
        "baseline_supported_primitive_count": BASELINE_SUPPORTED_COUNT,
        "supported_primitive_count_after_binding": BOUND_SUPPORTED_COUNT,
        "remaining_unresolved_primitive_names": BOUND_REMAINING_UNRESOLVED,
        "remaining_unresolved_primitive_count": 0,
        "all_v2r13_provider_primitives_implemented": True,
        "full_collector_identity_admitted": False,
        "canonical_provider_binding_present": False,
        "canonical_collection_enabled": False,
        "automatic_host_backend_selection": False,
        "binding_live_observation_implemented": False,
        "binding_http_request_implemented": False,
        "binding_host_backend_invocation_implemented": False,
        "binding_filesystem_observation_implemented": False,
        "binding_git_query_implemented": False,
        "binding_subprocess_execution_implemented": False,
        "binding_model_inference_implemented": False,
        "binding_game_execution_implemented": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "dependency_contracts_valid": True,
        "dependency_contracts": dependencies,
    }


def collect_bound_ollama_identity(*args: Any, **kwargs: Any) -> None:
    """Always hold: this binding source never invokes the HTTP observer."""
    raise RuntimeV2R13OllamaObserverBindingHold(
        "GENERATION2_V2R13_BOUND_OLLAMA_LIVE_COLLECTION_NOT_IMPLEMENTED"
    )
