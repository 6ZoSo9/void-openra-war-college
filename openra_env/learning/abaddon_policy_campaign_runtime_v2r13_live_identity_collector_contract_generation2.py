"""Source-only V2R13 live-identity collector contract for Generation-2.

This module freezes the semantic requirements for the three V2R13 primitives
that still require real current-host observation:

* endpoint_liveness
* model_identity_verified
* runtime_image_identity_verified

It does not implement or execute any collector.

A future collector implementation must have its own separately reviewed source
identity and must emit a supplied receipt compatible with the canonical
V2R13 identity-receipt validator.  Neither this semantic contract SHA nor a
self-reported collector SHA is sufficient to admit collector identity.

The known game-facing chat-completions endpoint is explicitly forbidden as an
identity/liveness probe because that would cross the model-inference boundary.
No alternative non-inference route or runtime-image backend is invented here.

The generic designated-host read-only preflight source is bound only as a
mechanical design reference. It is explicitly not V2R13 identity proof.

No filesystem access, Git query, path resolution, subprocess execution, HTTP
request, endpoint/systemd probe, service action, runtime start/stop/reload,
model load/inference, game execution, training, deployment, VOID-chain
mutation, or funds action occurs here.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_activation_contract_generation2
    as activation_contract,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_observation_mechanics_generation2
    as observation_mechanics,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_identity_receipt_validator_generation2
    as identity_receipt_validator,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-live-identity-collector-contract.v1"
)
MANIFEST_SCHEMA = (
    "void.abaddon.generation2.v2r13-live-identity-collector-contract-manifest.v1"
)
IDENTITY_SCHEMA = (
    "void.abaddon.generation2.v2r13-live-identity-collector-contract-identity.v1"
)

ACTIVATION_CONTRACT_GIT_BLOB = "a3acb42280c334daa24a3b830105a04666fd603b"
OBSERVATION_MECHANICS_GIT_BLOB = "5fc94c056d1ad7de41b5d7156bce9b3f500f29ba"
IDENTITY_RECEIPT_VALIDATOR_GIT_BLOB = (
    "d1586ba032d78296e200d5016560682b82ee599d"
)
GENERIC_DESIGNATED_HOST_READONLY_REFERENCE_GIT_BLOB = (
    "aadcc32fbba9a11d9f4d53f2410a7321c46c0131"
)

EXPECTED_COLLECTOR_CONTRACT_SHA256 = "0bda63a4d82be7f38e604c15fe63f659051cc42527bc9281317df167f6145219"

_MANIFEST_JSON = r"""
{
  "activation_contract_git_blob": "a3acb42280c334daa24a3b830105a04666fd603b",
  "automatic_host_backend_selection": false,
  "channels": {
    "endpoint_liveness": {
      "backend_mechanism": "unresolved",
      "canonical_non_inference_probe_route_defined": false,
      "collector_implemented": false,
      "expected_loopback_host": "127.0.0.1",
      "expected_port": 11434,
      "may_call_chat_completions": false,
      "may_run_model_inference": false,
      "non_inference_route_required": true,
      "required": true
    },
    "model_identity_verified": {
      "backend_mechanism": "unresolved",
      "canonical_live_identity_route_defined": false,
      "collector_implemented": false,
      "expected_model_alias": "void-apollyon-candidate-v2r13:latest",
      "expected_model_digest": "b52834ea46c10362e9bb20cd2e721716016bb36f800ddbc62e7fbaa24fb40932",
      "may_run_model_inference": false,
      "required": true
    },
    "runtime_image_identity_verified": {
      "backend_mechanism": "unresolved",
      "canonical_live_identity_route_defined": false,
      "collector_implemented": false,
      "expected_runtime_image_id": "sha256:79f2f6800382489a2a648839fc0d58e546384938439378aeea06461363de25f5",
      "may_start_or_restart_runtime": false,
      "required": true
    }
  },
  "chat_completions_request_allowed_for_liveness": false,
  "collector_binding_activation": false,
  "collector_implementation_source_binding_required_before_admission": true,
  "collector_implementation_source_sha256": null,
  "collector_may_deploy": false,
  "collector_may_execute_game": false,
  "collector_may_move_funds": false,
  "collector_may_mutate": false,
  "collector_may_mutate_void_chain": false,
  "collector_may_promote_policy": false,
  "collector_may_reload_service": false,
  "collector_may_run_model_inference": false,
  "collector_may_start_runtime": false,
  "collector_may_stop_runtime": false,
  "collector_may_train": false,
  "collector_may_update_weights": false,
  "contract_version": 1,
  "expected_chat_completions_url": "http://127.0.0.1:11434/v1/chat/completions",
  "expected_model_alias": "void-apollyon-candidate-v2r13:latest",
  "expected_model_digest": "b52834ea46c10362e9bb20cd2e721716016bb36f800ddbc62e7fbaa24fb40932",
  "expected_runtime_image_id": "sha256:79f2f6800382489a2a648839fc0d58e546384938439378aeea06461363de25f5",
  "explicit_observation_authority_required": true,
  "generic_designated_host_readonly_reference_git_blob": "aadcc32fbba9a11d9f4d53f2410a7321c46c0131",
  "generic_designated_host_reference_admitted_as_v2r13_identity_proof": false,
  "generic_designated_host_reference_is_design_reference_only": true,
  "identity_probe_may_run_model_inference": false,
  "identity_receipt_validator_git_blob": "d1586ba032d78296e200d5016560682b82ee599d",
  "inference_endpoint_may_be_reused_as_identity_probe": false,
  "observation_mechanics_git_blob": "5fc94c056d1ad7de41b5d7156bce9b3f500f29ba",
  "observation_mode": "read_only",
  "receipt_schema": "void.abaddon.generation2.v2r13-runtime-identity-observation-receipt.v1",
  "remaining_unresolved_primitive_count_before_live_collection": 3,
  "remaining_unresolved_primitive_names": [
    "endpoint_liveness",
    "model_identity_verified",
    "runtime_image_identity_verified"
  ],
  "schema": "void.abaddon.generation2.v2r13-live-identity-collector-contract-manifest.v1",
  "snapshot_id": "apollyon-v2r13-qualified-predecessor",
  "supported_primitive_count_before_live_collection": 13
}
"""


class RuntimeV2R13LiveIdentityCollectorContractHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13LiveIdentityCollectorContractHold(message)


def collector_contract_manifest() -> dict[str, Any]:
    value = json.loads(_MANIFEST_JSON)
    _require(isinstance(value, dict), "V2R13 collector manifest must be object")
    return value


def _canonical_manifest_bytes() -> bytes:
    return json.dumps(
        collector_contract_manifest(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")


def collector_contract_sha256() -> str:
    return hashlib.sha256(_canonical_manifest_bytes()).hexdigest()


def validate_v2r13_live_identity_collector_contract() -> dict[str, Any]:
    manifest = collector_contract_manifest()

    _require(
        manifest.get("schema") == MANIFEST_SCHEMA,
        "V2R13 collector manifest schema drift",
    )
    _require(
        collector_contract_sha256() == EXPECTED_COLLECTOR_CONTRACT_SHA256,
        "V2R13 collector semantic contract SHA drift",
    )
    _require(
        manifest.get("snapshot_id") == activation_contract.V2R13,
        "V2R13 collector snapshot drift",
    )

    bindings = (
        ("activation_contract_git_blob", ACTIVATION_CONTRACT_GIT_BLOB),
        ("observation_mechanics_git_blob", OBSERVATION_MECHANICS_GIT_BLOB),
        (
            "identity_receipt_validator_git_blob",
            IDENTITY_RECEIPT_VALIDATOR_GIT_BLOB,
        ),
        (
            "generic_designated_host_readonly_reference_git_blob",
            GENERIC_DESIGNATED_HOST_READONLY_REFERENCE_GIT_BLOB,
        ),
    )
    for field, expected in bindings:
        _require(manifest.get(field) == expected, f"V2R13 blob drift: {field}")

    _require(
        manifest.get("expected_chat_completions_url")
        == activation_contract.LOOPBACK_11434,
        "V2R13 chat endpoint drift",
    )
    _require(
        manifest.get("expected_model_alias")
        == activation_contract.V2R13_MODEL_ALIAS,
        "V2R13 model alias drift",
    )
    _require(
        manifest.get("expected_model_digest")
        == activation_contract.V2R13_MODEL_DIGEST,
        "V2R13 model digest drift",
    )
    _require(
        manifest.get("expected_runtime_image_id")
        == activation_contract.V2R13_RUNTIME_IMAGE_ID,
        "V2R13 runtime image drift",
    )
    _require(
        manifest.get("receipt_schema") == identity_receipt_validator.RECEIPT_SCHEMA,
        "V2R13 identity receipt schema drift",
    )

    mechanics = observation_mechanics.observation_mechanics(activation_contract.V2R13)
    live_identity = mechanics.get("live_runtime_identity")
    _require(isinstance(live_identity, dict), "V2R13 live identity mechanics missing")
    _require(
        live_identity.get("canonical_source_defined_identity_route") is False,
        "V2R13 canonical identity route unexpectedly exists",
    )

    validator = (
        identity_receipt_validator.v2r13_runtime_identity_receipt_validator_contract()
    )
    _require(
        validator.get("collector_contract_binding_required_for_identity_admission")
        is True,
        "V2R13 collector binding requirement missing",
    )
    _require(
        validator.get("self_reported_collector_sha_is_sufficient") is False,
        "V2R13 self-reported collector SHA unexpectedly sufficient",
    )
    _require(
        validator.get("model_identity_provider_primitive_implemented") is False,
        "V2R13 model identity primitive prematurely implemented",
    )
    _require(
        validator.get("runtime_image_provider_primitive_implemented") is False,
        "V2R13 runtime image primitive prematurely implemented",
    )

    _require(
        manifest.get("observation_mode") == "read_only",
        "V2R13 collector observation mode drift",
    )
    _require(
        manifest.get("explicit_observation_authority_required") is True,
        "V2R13 explicit observation authority requirement lost",
    )
    _require(
        manifest.get("automatic_host_backend_selection") is False,
        "V2R13 automatic host backend selection enabled",
    )
    _require(
        manifest.get(
            "collector_implementation_source_binding_required_before_admission"
        )
        is True,
        "V2R13 collector implementation binding requirement lost",
    )
    _require(
        manifest.get("collector_implementation_source_sha256") is None,
        "V2R13 collector implementation prematurely pinned",
    )
    _require(
        manifest.get("collector_binding_activation") is False,
        "V2R13 collector binding prematurely activated",
    )

    _require(
        manifest.get(
            "generic_designated_host_reference_admitted_as_v2r13_identity_proof"
        )
        is False,
        "generic designated-host reference became V2R13 identity proof",
    )
    _require(
        manifest.get(
            "generic_designated_host_reference_is_design_reference_only"
        )
        is True,
        "generic designated-host reference lost design-only classification",
    )
    _require(
        manifest.get("inference_endpoint_may_be_reused_as_identity_probe") is False,
        "V2R13 inference endpoint was reinterpreted as identity probe",
    )
    _require(
        manifest.get("chat_completions_request_allowed_for_liveness") is False,
        "V2R13 chat completion was allowed for liveness",
    )
    _require(
        manifest.get("identity_probe_may_run_model_inference") is False,
        "V2R13 identity probe gained inference authority",
    )

    for field in (
        "collector_may_mutate",
        "collector_may_start_runtime",
        "collector_may_stop_runtime",
        "collector_may_reload_service",
        "collector_may_execute_game",
        "collector_may_run_model_inference",
        "collector_may_train",
        "collector_may_update_weights",
        "collector_may_promote_policy",
        "collector_may_deploy",
        "collector_may_mutate_void_chain",
        "collector_may_move_funds",
    ):
        _require(
            manifest.get(field) is False,
            f"V2R13 collector authority drift: {field}",
        )

    _require(
        manifest.get("supported_primitive_count_before_live_collection") == 13,
        "V2R13 supported primitive frontier drift",
    )
    _require(
        manifest.get("remaining_unresolved_primitive_count_before_live_collection")
        == 3,
        "V2R13 unresolved primitive frontier drift",
    )
    _require(
        tuple(manifest.get("remaining_unresolved_primitive_names", ()))
        == (
            "endpoint_liveness",
            "model_identity_verified",
            "runtime_image_identity_verified",
        ),
        "V2R13 unresolved primitive set drift",
    )

    channels = manifest.get("channels")
    _require(isinstance(channels, dict), "V2R13 collector channels missing")
    _require(
        set(channels)
        == {
            "endpoint_liveness",
            "model_identity_verified",
            "runtime_image_identity_verified",
        },
        "V2R13 collector channel set drift",
    )
    for name, row in channels.items():
        _require(isinstance(row, dict), f"V2R13 channel malformed: {name}")
        _require(row.get("required") is True, f"V2R13 channel not required: {name}")
        _require(
            row.get("collector_implemented") is False,
            f"V2R13 collector prematurely implemented: {name}",
        )
        _require(
            row.get("backend_mechanism") == "unresolved",
            f"V2R13 backend mechanism was invented: {name}",
        )

    endpoint = channels["endpoint_liveness"]
    _require(
        endpoint.get("expected_loopback_host") == "127.0.0.1"
        and endpoint.get("expected_port") == 11434,
        "V2R13 endpoint host/port drift",
    )
    _require(
        endpoint.get("non_inference_route_required") is True,
        "V2R13 non-inference liveness requirement lost",
    )
    _require(
        endpoint.get("canonical_non_inference_probe_route_defined") is False,
        "V2R13 non-inference liveness route prematurely defined",
    )
    _require(
        endpoint.get("may_call_chat_completions") is False,
        "V2R13 endpoint liveness may call chat completions",
    )
    _require(
        endpoint.get("may_run_model_inference") is False,
        "V2R13 endpoint liveness may run inference",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "collector_contract_sha256": EXPECTED_COLLECTOR_CONTRACT_SHA256,
        "semantic_contract_valid": True,
        "implementation_source_binding_required_before_admission": True,
        "implementation_source_sha256": None,
        "collector_binding_activation": False,
        "collector_implementation_present": False,
        "explicit_observation_authority_required": True,
        "automatic_host_backend_selection": False,
        "generic_reference_design_only": True,
        "endpoint_liveness_collector_implemented": False,
        "model_identity_collector_implemented": False,
        "runtime_image_identity_collector_implemented": False,
        "live_observation_performed": False,
        "collector_executed": False,
        "collector_identity_admitted": False,
        "model_identity_verified": False,
        "runtime_image_identity_verified": False,
        "supported_primitive_count_remains": 13,
        "remaining_unresolved_primitive_count_remains": 3,
        "canonical_provider_binding_present": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "manifest": deepcopy(manifest),
    }


def collector_contract_identity() -> dict[str, Any]:
    validated = validate_v2r13_live_identity_collector_contract()
    return {
        "schema": IDENTITY_SCHEMA,
        "collector_contract_sha256": validated["collector_contract_sha256"],
        "semantic_contract_valid": True,
        "implementation_source_binding_present": False,
        "collector_binding_activation": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
    }


def collect_v2r13_live_identity(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13LiveIdentityCollectorContractHold(
        "GENERATION2_V2R13_LIVE_IDENTITY_COLLECTOR_IMPLEMENTATION_NOT_PRESENT"
    )
