"""Source-only reviewed collector-contract specification for Generation-2.

This module defines the exact semantic contract that a future runtime-evidence
collector must satisfy. It does not implement or execute that collector.

The collector contract has two distinct identities:

1. semantic contract identity:
   SHA-256 of a canonical JSON manifest defined here;
2. implementation source identity:
   must be separately pinned by a future reviewed source revision before the
   activation-evidence contract may enable collector admission.

A correct semantic contract hash alone is intentionally insufficient to enable
admission.

The currently reviewed dormant observer primitives cover only:
* V8 exact asset observation;
* V2R13 exact Git identity observation.

V14/V10 observer collection and the remaining V8/V2R13 runtime/provenance
primitives remain unimplemented.

No filesystem access, Git command, subprocess, environment read, pip freeze,
endpoint/systemd probe, observer invocation, host-backend call, model load,
worktree creation, runtime/game/model execution, training, weight update,
promotion, deployment, VOID-chain mutation, or funds action occurs here.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_activation_evidence_generation2
    as activation_evidence,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_observers_generation2
    as runtime_observers,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    V10,
    V14,
    V2R13,
    V8,
)

CONTRACT_SCHEMA = "void.abaddon.generation2.runtime-collector-contract.v1"
MANIFEST_SCHEMA = (
    "void.abaddon.generation2.runtime-collector-contract-manifest.v1"
)
IDENTITY_SCHEMA = (
    "void.abaddon.generation2.runtime-collector-contract-identity.v1"
)

ACTIVATION_CONTRACT_GIT_BLOB = "a3acb42280c334daa24a3b830105a04666fd603b"
ACTIVATION_EVIDENCE_GIT_BLOB = "aac7964d9e80633535003b9f27066cac1bb4bac2"
RUNTIME_OBSERVERS_GIT_BLOB = "cc4774e6aa934764c189cebd4040cd8ea4870517"

EXPECTED_COLLECTOR_CONTRACT_SHA256 = (
    "d11e45cabc10b42e09ab5e328e1e63721b633c7cdcfd7492038ec286b7f3e657"
)

_MANIFEST_JSON = r"""
{
  "activation_contract_git_blob": "a3acb42280c334daa24a3b830105a04666fd603b",
  "activation_evidence_git_blob": "aac7964d9e80633535003b9f27066cac1bb4bac2",
  "automatic_host_backend_selection": false,
  "collector_binding_activation": false,
  "collector_implementation_source_binding_required_before_activation": true,
  "collector_implementation_source_sha256": null,
  "collector_may_deploy": false,
  "collector_may_execute_game": false,
  "collector_may_move_funds": false,
  "collector_may_mutate": false,
  "collector_may_mutate_void_chain": false,
  "collector_may_promote_policy": false,
  "collector_may_run_model_inference": false,
  "collector_may_start_runtime": false,
  "collector_may_train": false,
  "collector_may_update_weights": false,
  "contract_version": 1,
  "explicit_observation_authority_required": true,
  "identity_kind": "canonical-json-manifest-sha256",
  "observation_mode": "read_only",
  "runtime_observers_git_blob": "cc4774e6aa934764c189cebd4040cd8ea4870517",
  "schema": "void.abaddon.generation2.runtime-collector-contract-manifest.v1",
  "snapshot_contracts": {
    "apollyon-v13-v10-promoted": {
      "collector_owned_evidence_fields": [
        "collector_contract_sha256",
        "observation_mode",
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "game_execution_performed",
        "model_inference_performed",
        "endpoint_liveness",
        "model_identity_verified",
        "runtime_unit_identity_verified"
      ],
      "full_collector_implemented": false,
      "required_future_primitives": [
        "read_only_loopback_endpoint_liveness",
        "read_only_active_model_identity",
        "read_only_runtime_unit_identity",
        "common_operational_action_ledger"
      ],
      "reviewed_partial_observer_primitives_present": false
    },
    "apollyon-v13-v14-promoted": {
      "collector_owned_evidence_fields": [
        "collector_contract_sha256",
        "observation_mode",
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "game_execution_performed",
        "model_inference_performed",
        "endpoint_liveness",
        "model_identity_verified",
        "runtime_unit_identity_verified"
      ],
      "full_collector_implemented": false,
      "required_future_primitives": [
        "read_only_loopback_endpoint_liveness",
        "read_only_active_model_identity",
        "read_only_runtime_unit_identity",
        "common_operational_action_ledger"
      ],
      "reviewed_partial_observer_primitives_present": false
    },
    "apollyon-v2r13-qualified-predecessor": {
      "collector_owned_evidence_fields": [
        "collector_contract_sha256",
        "observation_mode",
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "game_execution_performed",
        "model_inference_performed",
        "endpoint_liveness",
        "model_identity_verified",
        "runtime_image_identity_verified",
        "frozen_source_worktree.exists",
        "frozen_source_worktree.is_directory",
        "frozen_source_worktree.is_symlink",
        "engine_worktree.exists",
        "engine_worktree.is_directory",
        "engine_worktree.is_symlink",
        "portable_binding_attested"
      ],
      "full_collector_implemented": false,
      "required_future_primitives": [
        "read_only_loopback_endpoint_liveness",
        "read_only_active_model_digest_identity",
        "read_only_runtime_image_identity",
        "read_only_worktree_path_classification",
        "portable_binding_attestation",
        "common_operational_action_ledger"
      ],
      "reviewed_partial_observer_primitives": [
        "observe_v2r13_git_identity"
      ],
      "reviewed_partial_observer_primitives_present": true
    },
    "apollyon-v3-v8-accepted-model-control": {
      "collector_owned_evidence_fields_with_supplied_environment": [
        "collector_contract_sha256",
        "observation_mode",
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "game_execution_performed",
        "model_inference_performed",
        "offline_only_verified",
        "load_call_performed"
      ],
      "collector_owned_evidence_fields_without_supplied_environment": [
        "collector_contract_sha256",
        "observation_mode",
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "game_execution_performed",
        "model_inference_performed",
        "runtime_environment_verified",
        "offline_only_verified",
        "load_call_performed"
      ],
      "full_collector_implemented": false,
      "required_future_primitives": [
        "read_only_runtime_environment_identity",
        "read_only_offline_only_attestation",
        "common_operational_action_ledger"
      ],
      "reviewed_partial_observer_primitives": [
        "observe_v8_assets",
        "observe_exact_regular_file"
      ],
      "reviewed_partial_observer_primitives_present": true
    }
  }
}
"""


class RuntimeCollectorContractHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeCollectorContractHold(message)


def collector_contract_manifest() -> dict[str, Any]:
    """Return the canonical semantic contract for a future reviewed collector."""
    value = json.loads(_MANIFEST_JSON)
    _require(isinstance(value, dict), "collector manifest must decode to object")
    return value


def _canonical_manifest_bytes() -> bytes:
    value = collector_contract_manifest()
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")


def collector_contract_sha256() -> str:
    """Return the semantic collector-contract SHA-256."""
    return hashlib.sha256(_canonical_manifest_bytes()).hexdigest()


def validate_collector_contract() -> dict[str, Any]:
    """Validate semantic identity and all fail-closed activation boundaries."""
    manifest = collector_contract_manifest()

    _require(
        manifest.get("schema") == MANIFEST_SCHEMA,
        "collector manifest schema drift",
    )
    _require(
        collector_contract_sha256() == EXPECTED_COLLECTOR_CONTRACT_SHA256,
        "collector semantic contract SHA drift",
    )
    _require(
        manifest.get("activation_contract_git_blob")
        == ACTIVATION_CONTRACT_GIT_BLOB,
        "activation-contract blob drift",
    )
    _require(
        manifest.get("activation_evidence_git_blob")
        == ACTIVATION_EVIDENCE_GIT_BLOB,
        "activation-evidence blob drift",
    )
    _require(
        manifest.get("runtime_observers_git_blob") == RUNTIME_OBSERVERS_GIT_BLOB,
        "runtime-observers blob drift",
    )

    _require(
        manifest.get("observation_mode") == "read_only",
        "collector mode drift",
    )
    for field in (
        "collector_may_mutate",
        "collector_may_start_runtime",
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
            f"collector authority drift: {field}",
        )

    _require(
        manifest.get("automatic_host_backend_selection") is False,
        "automatic host-backend selection became enabled",
    )
    _require(
        manifest.get("explicit_observation_authority_required") is True,
        "explicit observation authority requirement lost",
    )
    _require(
        manifest.get(
            "collector_implementation_source_binding_required_before_activation"
        )
        is True,
        "implementation source binding requirement lost",
    )
    _require(
        manifest.get("collector_implementation_source_sha256") is None,
        "collector implementation source was prematurely pinned",
    )
    _require(
        manifest.get("collector_binding_activation") is False,
        "collector binding was prematurely activated",
    )
    _require(
        activation_evidence.REVIEWED_COLLECTOR_BINDING_PRESENT is False,
        "activation-evidence collector binding unexpectedly active",
    )

    observer_contract = runtime_observers.runtime_observer_contract()
    _require(
        observer_contract.get("automatic_host_backend_selection") is False,
        "observer contract automatically selects host backend",
    )
    _require(
        observer_contract.get("observation_requires_explicit_authority") is True,
        "observer contract lost explicit authority gate",
    )

    snapshots = manifest.get("snapshot_contracts")
    _require(
        isinstance(snapshots, dict),
        "collector snapshot contract map missing",
    )
    _require(
        set(snapshots) == {V14, V10, V2R13, V8},
        "collector snapshot contract set drift",
    )
    for snapshot_id, row in snapshots.items():
        _require(
            row.get("full_collector_implemented") is False,
            f"full collector unexpectedly implemented: {snapshot_id}",
        )

    _require(
        snapshots[V14]["reviewed_partial_observer_primitives_present"] is False,
        "V14 observer primitive unexpectedly claimed",
    )
    _require(
        snapshots[V10]["reviewed_partial_observer_primitives_present"] is False,
        "V10 observer primitive unexpectedly claimed",
    )
    _require(
        snapshots[V2R13]["reviewed_partial_observer_primitives"]
        == ["observe_v2r13_git_identity"],
        "V2R13 reviewed primitive set drift",
    )
    _require(
        snapshots[V8]["reviewed_partial_observer_primitives"]
        == ["observe_v8_assets", "observe_exact_regular_file"],
        "V8 reviewed primitive set drift",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "collector_contract_sha256": EXPECTED_COLLECTOR_CONTRACT_SHA256,
        "semantic_contract_valid": True,
        "implementation_source_binding_required_before_activation": True,
        "implementation_source_sha256": None,
        "reviewed_collector_binding_present": False,
        "collector_binding_activation": False,
        "full_collector_implemented": False,
        "v14_full_collector_implemented": False,
        "v10_full_collector_implemented": False,
        "v2r13_full_collector_implemented": False,
        "v8_full_collector_implemented": False,
        "live_observation_performed": False,
        "collector_executed": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "manifest": deepcopy(manifest),
    }


def collector_contract_identity() -> dict[str, Any]:
    """Expose semantic identity without claiming implementation/admission."""
    validated = validate_collector_contract()
    return {
        "schema": IDENTITY_SCHEMA,
        "collector_contract_sha256": validated["collector_contract_sha256"],
        "identity_kind": "canonical-json-manifest-sha256",
        "semantic_contract_valid": True,
        "implementation_source_binding_present": False,
        "collector_binding_activation": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
    }


def collect_activation_evidence(*args: Any, **kwargs: Any) -> None:
    """Always hold: this module specifies a collector; it never executes one."""
    raise RuntimeCollectorContractHold(
        "GENERATION2_REVIEWED_COLLECTOR_IMPLEMENTATION_NOT_PRESENT"
    )
