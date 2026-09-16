"""Dormant read-only Ollama observer candidate for V2R13 Generation-2.

This module implements a reviewed *candidate* observation mechanic for two of
the three still-unresolved V2R13 live-identity channels:

* endpoint/catalog liveness through GET /api/tags
* running model alias + digest through GET /api/ps

The routes are deliberately separate from the game-facing
/v1/chat/completions inference endpoint.  No chat/completions request is ever
constructed by this source.

The observer requires both:
* explicit ``observation_authorized=True``; and
* an explicitly supplied HTTP GET backend.

A bounded stdlib host backend factory is provided, but this module never selects
or invokes it automatically.  Merely importing the module or constructing the
backend performs no network I/O.

Runtime-image identity is intentionally NOT implemented here.  This observer
does not inspect Docker/Podman/containerd/systemd/process state and therefore
cannot satisfy ``runtime_image_identity_verified``.

No service action, runtime start/stop/reload, model load/inference, game
execution, training, deployment, VOID-chain mutation, or funds action occurs
merely by importing or inspecting this module.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from openra_env.learning import (
    abaddon_policy_campaign_runtime_activation_contract_generation2
    as activation_contract,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_live_identity_collector_contract_generation2
    as live_identity_contract,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-ollama-readonly-observer-contract.v1"
)
OBSERVATION_SCHEMA = (
    "void.abaddon.generation2.v2r13-ollama-readonly-observation.v1"
)

LIVE_IDENTITY_COLLECTOR_CONTRACT_GIT_BLOB = (
    "db9fbb58f3d5870c77a796641afb1014acc19ee4"
)
LIVE_IDENTITY_COLLECTOR_SEMANTIC_SHA256 = (
    "0bda63a4d82be7f38e604c15fe63f659051cc42527bc9281317df167f6145219"
)

OLLAMA_ORIGIN = "http://127.0.0.1:11434"
OLLAMA_TAGS_URL = f"{OLLAMA_ORIGIN}/api/tags"
OLLAMA_PS_URL = f"{OLLAMA_ORIGIN}/api/ps"
FORBIDDEN_CHAT_COMPLETIONS_URL = activation_contract.LOOPBACK_11434

MAX_RESPONSE_BYTES = 4 * 1024 * 1024
DEFAULT_TIMEOUT_SECONDS = 2.0

SHA256_HEX = frozenset("0123456789abcdef")


class RuntimeV2R13OllamaObserverHold(ValueError):
    pass


@dataclass(frozen=True)
class HttpGetResult:
    status: int
    body: bytes
    content_type: str | None = None


class HttpGetBackend(Protocol):
    def __call__(
        self,
        url: str,
        *,
        timeout_seconds: float,
        maximum_bytes: int,
    ) -> HttpGetResult:
        ...


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13OllamaObserverHold(message)


def _require_observation_authority(observation_authorized: bool) -> None:
    _require(
        observation_authorized is True,
        "GENERATION2_V2R13_OLLAMA_OBSERVATION_NOT_AUTHORIZED",
    )


def _is_sha256(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(char in SHA256_HEX for char in value)
    )


def _read_bounded(response: Any, maximum_bytes: int) -> bytes:
    _require(
        type(maximum_bytes) is int and maximum_bytes > 0,
        "maximum_bytes must be positive integer",
    )
    chunks: list[bytes] = []
    total = 0
    while True:
        remaining = maximum_bytes + 1 - total
        _require(remaining > 0, "V2R13_OLLAMA_RESPONSE_EXCEEDS_BOUND")
        chunk = response.read(min(65536, remaining))
        _require(isinstance(chunk, bytes), "V2R13_OLLAMA_RESPONSE_READ_TYPE")
        if not chunk:
            break
        total += len(chunk)
        _require(total <= maximum_bytes, "V2R13_OLLAMA_RESPONSE_EXCEEDS_BOUND")
        chunks.append(chunk)
    return b"".join(chunks)


def host_http_get(
    url: str,
    *,
    timeout_seconds: float,
    maximum_bytes: int,
) -> HttpGetResult:
    """Perform one bounded GET to an exact reviewed Ollama read-only route.

    This function is never called automatically.
    """
    _require(
        url in {OLLAMA_TAGS_URL, OLLAMA_PS_URL},
        "V2R13_OLLAMA_HOST_BACKEND_URL_NOT_REVIEWED",
    )
    _require(
        url != FORBIDDEN_CHAT_COMPLETIONS_URL,
        "V2R13_OLLAMA_CHAT_COMPLETIONS_FORBIDDEN",
    )
    _require(
        type(timeout_seconds) in {int, float}
        and 0 < float(timeout_seconds) <= 10.0,
        "timeout_seconds outside reviewed bound",
    )
    _require(
        type(maximum_bytes) is int
        and 0 < maximum_bytes <= MAX_RESPONSE_BYTES,
        "maximum_bytes outside reviewed bound",
    )

    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "Accept": "application/json",
            "User-Agent": "VOID-War-College-V2R13-ReadOnly-Observer/1",
        },
    )
    try:
        with urllib.request.urlopen(
            request,
            timeout=float(timeout_seconds),
        ) as response:
            status = int(response.getcode())
            body = _read_bounded(response, maximum_bytes)
            content_type = response.headers.get("Content-Type")
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise RuntimeV2R13OllamaObserverHold(
            f"V2R13_OLLAMA_GET_FAILED:{type(error).__name__}"
        ) from error

    return HttpGetResult(
        status=status,
        body=body,
        content_type=content_type,
    )


def _validate_http_result(
    result: HttpGetResult,
    *,
    label: str,
) -> Mapping[str, Any]:
    _require(isinstance(result, HttpGetResult), f"{label}: invalid HTTP result")
    _require(result.status == 200, f"{label}: HTTP status drift")
    _require(
        len(result.body) <= MAX_RESPONSE_BYTES,
        f"{label}: response exceeds bound",
    )
    try:
        value = json.loads(result.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeV2R13OllamaObserverHold(
            f"{label}: invalid UTF-8 JSON"
        ) from error
    _require(isinstance(value, Mapping), f"{label}: response must be object")
    return value


def _models(value: Mapping[str, Any], *, label: str) -> list[Mapping[str, Any]]:
    rows = value.get("models")
    _require(isinstance(rows, list), f"{label}: models must be list")
    result: list[Mapping[str, Any]] = []
    for row in rows:
        _require(isinstance(row, Mapping), f"{label}: model row must be object")
        result.append(row)
    return result


def _exact_model_match(
    rows: list[Mapping[str, Any]],
    *,
    label: str,
) -> Mapping[str, Any]:
    expected_alias = activation_contract.V2R13_MODEL_ALIAS
    expected_digest = activation_contract.V2R13_MODEL_DIGEST

    matches = [
        row
        for row in rows
        if row.get("name") == expected_alias or row.get("model") == expected_alias
    ]
    _require(len(matches) == 1, f"{label}: exact model alias match count drift")
    row = matches[0]
    _require(
        row.get("digest") == expected_digest,
        f"{label}: exact model digest drift",
    )
    _require(_is_sha256(row.get("digest")), f"{label}: model digest malformed")
    return row


def observe_v2r13_ollama_readonly(
    *,
    observation_authorized: bool,
    http_get: HttpGetBackend,
) -> dict[str, Any]:
    """Observe Ollama liveness + running-model identity without inference."""
    _require_observation_authority(observation_authorized)
    _require(callable(http_get), "V2R13 Ollama HTTP GET backend required")

    semantic = live_identity_contract.validate_v2r13_live_identity_collector_contract()
    _require(
        semantic.get("collector_contract_sha256")
        == LIVE_IDENTITY_COLLECTOR_SEMANTIC_SHA256,
        "V2R13 live identity collector semantic SHA drift",
    )
    _require(
        semantic.get("collector_binding_activation") is False,
        "V2R13 collector binding unexpectedly active",
    )

    tags_result = http_get(
        OLLAMA_TAGS_URL,
        timeout_seconds=DEFAULT_TIMEOUT_SECONDS,
        maximum_bytes=MAX_RESPONSE_BYTES,
    )
    tags_value = _validate_http_result(tags_result, label="V2R13_OLLAMA_TAGS")
    tags_match = _exact_model_match(
        _models(tags_value, label="V2R13_OLLAMA_TAGS"),
        label="V2R13_OLLAMA_TAGS",
    )

    ps_result = http_get(
        OLLAMA_PS_URL,
        timeout_seconds=DEFAULT_TIMEOUT_SECONDS,
        maximum_bytes=MAX_RESPONSE_BYTES,
    )
    ps_value = _validate_http_result(ps_result, label="V2R13_OLLAMA_PS")
    ps_match = _exact_model_match(
        _models(ps_value, label="V2R13_OLLAMA_PS"),
        label="V2R13_OLLAMA_PS",
    )

    return {
        "schema": OBSERVATION_SCHEMA,
        "snapshot_id": activation_contract.V2R13,
        "observation_mode": "read_only",
        "tags_url": OLLAMA_TAGS_URL,
        "ps_url": OLLAMA_PS_URL,
        "chat_completions_url": FORBIDDEN_CHAT_COMPLETIONS_URL,
        "chat_completions_request_performed": False,
        "endpoint_liveness_observed": True,
        "catalog_model_alias": tags_match.get("name") or tags_match.get("model"),
        "catalog_model_digest": tags_match["digest"],
        "running_model_alias": ps_match.get("name") or ps_match.get("model"),
        "running_model_digest": ps_match["digest"],
        "model_catalog_identity_matches_expected": True,
        "running_model_identity_matches_expected": True,
        "model_identity_observation_performed": True,
        "runtime_image_identity_observation_performed": False,
        "runtime_image_id": None,
        "runtime_image_identity_verified": False,
        "collector_identity_admitted": False,
        "canonical_provider_binding_present": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "mutation_performed": False,
        "service_action_performed": False,
        "runtime_start_performed": False,
        "runtime_stop_performed": False,
        "runtime_reload_performed": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
    }


def v2r13_ollama_readonly_observer_contract() -> dict[str, Any]:
    semantic = live_identity_contract.validate_v2r13_live_identity_collector_contract()
    return {
        "schema": CONTRACT_SCHEMA,
        "live_identity_collector_contract_git_blob": (
            LIVE_IDENTITY_COLLECTOR_CONTRACT_GIT_BLOB
        ),
        "live_identity_collector_semantic_sha256": (
            LIVE_IDENTITY_COLLECTOR_SEMANTIC_SHA256
        ),
        "semantic_contract_valid": semantic["semantic_contract_valid"],
        "tags_route": "/api/tags",
        "ps_route": "/api/ps",
        "tags_method": "GET",
        "ps_method": "GET",
        "chat_completions_route": "/v1/chat/completions",
        "chat_completions_forbidden": True,
        "endpoint_liveness_observer_candidate_implemented": True,
        "running_model_identity_observer_candidate_implemented": True,
        "runtime_image_identity_observer_implemented": False,
        "host_http_backend_factory_present": True,
        "automatic_host_backend_selection": False,
        "observation_requires_explicit_authority": True,
        "candidate_observation_does_not_admit_collector_identity": True,
        "candidate_observation_does_not_advance_primitive_frontier": True,
        "supported_primitive_count_remains": 13,
        "remaining_unresolved_primitive_count_remains": 3,
        "remaining_unresolved_primitive_names": (
            "endpoint_liveness",
            "model_identity_verified",
            "runtime_image_identity_verified",
        ),
        "service_action_implemented": False,
        "runtime_start_stop_reload_implemented": False,
        "model_load_implemented": False,
        "model_inference_implemented": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
    }
