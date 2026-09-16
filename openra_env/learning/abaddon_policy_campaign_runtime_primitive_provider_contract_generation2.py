"""Source-only primitive-provider contract for Abaddon Generation-2.

This module classifies every primitive required by the canonical dormant
collector implementation.  It deliberately separates:

* source-only collector self-audits that need no host I/O;
* fields adaptable from already-reviewed observer/validator source;
* fields that still require a genuinely new read-only live identity channel.

It does not implement or invoke any provider.

V14/V10 inference endpoints remain game-facing inference surfaces and are not
reinterpreted as identity probes. V8 live pip-freeze collection remains
unreviewed even though the pure supplied-fact validator is reusable.

No filesystem access, Git command, subprocess, HTTP/systemd probe, observer
invocation, host-backend selection, model load, runtime/game/model execution,
training, promotion, deployment, VOID-chain mutation, or funds action occurs.
"""

from __future__ import annotations

import hashlib
import json
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
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    V10,
    V14,
    V2R13,
    V8,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.runtime-primitive-provider-contract.v1"
)
MANIFEST_SCHEMA = (
    "void.abaddon.generation2.runtime-primitive-provider-contract-manifest.v1"
)

COLLECTOR_CONTRACT_GIT_BLOB = "8014431ad5329137e5ce12334d19d37c877a0b52"
COLLECTOR_IMPLEMENTATION_GIT_BLOB = (
    "0003c24390194a4f621f13c6077e0604b9abcd98"
)
RUNTIME_OBSERVERS_GIT_BLOB = "cc4774e6aa934764c189cebd4040cd8ea4870517"
V8_RUNTIME_GIT_BLOB = "fd0e72767ba199e88af9e9eb2455c03ace027a14"
PRIMITIVE_REVIEW_GIT_BLOB = "97e7b11ec4cb4214e7b9764121ec8059371dab51"
OBSERVATION_MECHANICS_GIT_BLOB = (
    "5fc94c056d1ad7de41b5d7156bce9b3f500f29ba"
)
COLLECTOR_SEMANTIC_SHA256 = (
    "d11e45cabc10b42e09ab5e328e1e63721b633c7cdcfd7492038ec286b7f3e657"
)
EXPECTED_PROVIDER_CONTRACT_SHA256 = (
    "58e84a058c332de983ccaef19bd1383a92071966b653e699d032c9e9e86c1114"
)

_MANIFEST_JSON = r"""
{
  "canonical_collection_enabled": false,
  "canonical_provider_bindings_present": false,
  "collector_contract_git_blob": "8014431ad5329137e5ce12334d19d37c877a0b52",
  "collector_implementation_git_blob": "0003c24390194a4f621f13c6077e0604b9abcd98",
  "collector_semantic_sha256": "d11e45cabc10b42e09ab5e328e1e63721b633c7cdcfd7492038ec286b7f3e657",
  "common_operational_primitives": {
    "game_execution_performed": {
      "class": "source_only_collector_self_audit",
      "expected_value": false,
      "host_io_required": false
    },
    "model_inference_performed": {
      "class": "source_only_collector_self_audit",
      "expected_value": false,
      "host_io_required": false
    },
    "mutation_performed": {
      "class": "source_only_collector_self_audit",
      "expected_value": false,
      "host_io_required": false
    },
    "observation_mode": {
      "class": "source_only_collector_self_audit",
      "expected_value": "read_only",
      "host_io_required": false
    },
    "runtime_start_performed": {
      "class": "source_only_collector_self_audit",
      "expected_value": false,
      "host_io_required": false
    },
    "service_action_performed": {
      "class": "source_only_collector_self_audit",
      "expected_value": false,
      "host_io_required": false
    }
  },
  "contract_version": 1,
  "identity_kind": "canonical-json-manifest-sha256",
  "observation_mechanics_git_blob": "5fc94c056d1ad7de41b5d7156bce9b3f500f29ba",
  "primitive_review_git_blob": "97e7b11ec4cb4214e7b9764121ec8059371dab51",
  "reviewed_collector_binding_present": false,
  "runtime_execution_authorized": false,
  "runtime_observers_git_blob": "cc4774e6aa934764c189cebd4040cd8ea4870517",
  "runtime_readiness_admission_enabled": false,
  "schema": "void.abaddon.generation2.runtime-primitive-provider-contract-manifest.v1",
  "snapshots": {
    "apollyon-v13-v10-promoted": {
      "primitive_contracts": {
        "endpoint_liveness": {
          "canonical_route_present": false,
          "class": "unresolved_read_only_liveness_probe",
          "host_io_required": true,
          "model_inference_permitted": false
        },
        "game_execution_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        },
        "model_identity_verified": {
          "canonical_route_present": false,
          "class": "unresolved_live_model_identity_channel",
          "host_io_required": true,
          "inference_endpoint_is_identity_probe": false
        },
        "model_inference_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        },
        "mutation_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        },
        "observation_mode": {
          "class": "source_only_collector_self_audit",
          "expected_value": "read_only",
          "host_io_required": false
        },
        "runtime_start_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        },
        "runtime_unit_identity_verified": {
          "canonical_route_present": false,
          "class": "unresolved_runtime_unit_identity_channel",
          "generic_designated_host_discovery_admitted": false,
          "host_io_required": true
        },
        "service_action_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        }
      },
      "required_primitive_count": 9
    },
    "apollyon-v13-v14-promoted": {
      "primitive_contracts": {
        "endpoint_liveness": {
          "canonical_route_present": false,
          "class": "unresolved_read_only_liveness_probe",
          "host_io_required": true,
          "model_inference_permitted": false
        },
        "game_execution_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        },
        "model_identity_verified": {
          "canonical_route_present": false,
          "class": "unresolved_live_model_identity_channel",
          "host_io_required": true,
          "inference_endpoint_is_identity_probe": false
        },
        "model_inference_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        },
        "mutation_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        },
        "observation_mode": {
          "class": "source_only_collector_self_audit",
          "expected_value": "read_only",
          "host_io_required": false
        },
        "runtime_start_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        },
        "runtime_unit_identity_verified": {
          "canonical_route_present": false,
          "class": "unresolved_runtime_unit_identity_channel",
          "generic_designated_host_discovery_admitted": false,
          "host_io_required": true
        },
        "service_action_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        }
      },
      "required_primitive_count": 9
    },
    "apollyon-v2r13-qualified-predecessor": {
      "primitive_contracts": {
        "endpoint_liveness": {
          "canonical_route_present": false,
          "class": "unresolved_read_only_liveness_probe",
          "host_io_required": true,
          "model_inference_permitted": false
        },
        "engine_worktree.exists": {
          "adapter_implementation_present": false,
          "class": "reviewed_v2r13_observer_adapter_required",
          "host_io_required": false,
          "reviewed_observer_function": "observe_v2r13_git_identity",
          "reviewed_observer_git_blob": "cc4774e6aa934764c189cebd4040cd8ea4870517"
        },
        "engine_worktree.is_directory": {
          "adapter_implementation_present": false,
          "class": "reviewed_v2r13_observer_adapter_required",
          "host_io_required": false,
          "reviewed_observer_function": "observe_v2r13_git_identity",
          "reviewed_observer_git_blob": "cc4774e6aa934764c189cebd4040cd8ea4870517"
        },
        "engine_worktree.is_symlink": {
          "adapter_implementation_present": false,
          "class": "reviewed_v2r13_observer_adapter_required",
          "host_io_required": false,
          "reviewed_observer_function": "observe_v2r13_git_identity",
          "reviewed_observer_git_blob": "cc4774e6aa934764c189cebd4040cd8ea4870517"
        },
        "frozen_source_worktree.exists": {
          "adapter_implementation_present": false,
          "class": "reviewed_v2r13_observer_adapter_required",
          "host_io_required": false,
          "reviewed_observer_function": "observe_v2r13_git_identity",
          "reviewed_observer_git_blob": "cc4774e6aa934764c189cebd4040cd8ea4870517"
        },
        "frozen_source_worktree.is_directory": {
          "adapter_implementation_present": false,
          "class": "reviewed_v2r13_observer_adapter_required",
          "host_io_required": false,
          "reviewed_observer_function": "observe_v2r13_git_identity",
          "reviewed_observer_git_blob": "cc4774e6aa934764c189cebd4040cd8ea4870517"
        },
        "frozen_source_worktree.is_symlink": {
          "adapter_implementation_present": false,
          "class": "reviewed_v2r13_observer_adapter_required",
          "host_io_required": false,
          "reviewed_observer_function": "observe_v2r13_git_identity",
          "reviewed_observer_git_blob": "cc4774e6aa934764c189cebd4040cd8ea4870517"
        },
        "game_execution_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        },
        "model_identity_verified": {
          "canonical_route_present": false,
          "class": "unresolved_live_model_digest_identity_channel",
          "host_io_required": true,
          "inference_endpoint_is_identity_probe": false
        },
        "model_inference_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        },
        "mutation_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        },
        "observation_mode": {
          "class": "source_only_collector_self_audit",
          "expected_value": "read_only",
          "host_io_required": false
        },
        "portable_binding_attested": {
          "attestation_composition_implemented": false,
          "class": "unresolved_portable_binding_attestation_composition",
          "host_io_required": false,
          "reviewed_git_observer_present": true,
          "reviewed_static_contract_present": true
        },
        "runtime_image_identity_verified": {
          "canonical_route_present": false,
          "class": "unresolved_runtime_image_identity_channel",
          "host_io_required": true
        },
        "runtime_start_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        },
        "service_action_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        }
      },
      "required_primitive_count": 16
    },
    "apollyon-v3-v8-accepted-model-control": {
      "primitive_contracts": {
        "game_execution_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        },
        "load_call_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false,
          "model_load_permitted": false
        },
        "model_inference_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        },
        "mutation_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        },
        "observation_mode": {
          "class": "source_only_collector_self_audit",
          "expected_value": "read_only",
          "host_io_required": false
        },
        "offline_only_verified": {
          "canonical_route_present": false,
          "class": "unresolved_offline_only_attestation",
          "host_io_required": true
        },
        "runtime_environment_verified": {
          "class": "supplied_fact_validator_or_unreviewed_live_collection",
          "host_io_required_for_supplied_facts": false,
          "live_collection_reviewed": false,
          "live_collector_function": "verify_v8_runtime_environment",
          "pure_validator_direct_reuse_admitted": true,
          "pure_validator_function": "validate_v8_runtime_environment",
          "pure_validator_git_blob": "fd0e72767ba199e88af9e9eb2455c03ace027a14"
        },
        "runtime_start_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        },
        "service_action_performed": {
          "class": "source_only_collector_self_audit",
          "expected_value": false,
          "host_io_required": false
        }
      },
      "required_primitive_count_with_supplied_environment": 8,
      "required_primitive_count_without_supplied_environment": 9
    }
  },
  "v8_runtime_git_blob": "fd0e72767ba199e88af9e9eb2455c03ace027a14"
}
"""


class RuntimePrimitiveProviderContractHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimePrimitiveProviderContractHold(message)


def provider_contract_manifest() -> dict[str, Any]:
    value = json.loads(_MANIFEST_JSON)
    _require(isinstance(value, dict), "provider manifest must decode to object")
    return value


def _canonical_manifest_bytes() -> bytes:
    return json.dumps(
        provider_contract_manifest(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")


def provider_contract_sha256() -> str:
    return hashlib.sha256(_canonical_manifest_bytes()).hexdigest()


def primitive_contract(
    snapshot_id: str,
    primitive_name: str,
) -> dict[str, Any]:
    manifest = provider_contract_manifest()
    snapshots = manifest["snapshots"]
    _require(
        snapshot_id in {V14, V10, V2R13, V8},
        f"unsupported provider snapshot: {snapshot_id!r}",
    )
    row = snapshots[snapshot_id]
    primitives = row["primitive_contracts"]
    _require(
        primitive_name in primitives,
        f"unknown provider primitive {snapshot_id!r}:{primitive_name!r}",
    )
    return deepcopy(dict(primitives[primitive_name]))


def validate_provider_contract() -> dict[str, Any]:
    manifest = provider_contract_manifest()
    _require(manifest.get("schema") == MANIFEST_SCHEMA, "provider schema drift")
    _require(
        provider_contract_sha256() == EXPECTED_PROVIDER_CONTRACT_SHA256,
        "provider semantic SHA drift",
    )
    _require(
        manifest.get("collector_contract_git_blob") == COLLECTOR_CONTRACT_GIT_BLOB,
        "collector-contract blob drift",
    )
    _require(
        manifest.get("collector_implementation_git_blob")
        == COLLECTOR_IMPLEMENTATION_GIT_BLOB,
        "collector-implementation blob drift",
    )
    _require(
        manifest.get("runtime_observers_git_blob") == RUNTIME_OBSERVERS_GIT_BLOB,
        "runtime-observers blob drift",
    )
    _require(
        manifest.get("v8_runtime_git_blob") == V8_RUNTIME_GIT_BLOB,
        "V8 runtime blob drift",
    )
    _require(
        manifest.get("primitive_review_git_blob") == PRIMITIVE_REVIEW_GIT_BLOB,
        "primitive-review blob drift",
    )
    _require(
        manifest.get("observation_mechanics_git_blob")
        == OBSERVATION_MECHANICS_GIT_BLOB,
        "observation-mechanics blob drift",
    )
    _require(
        manifest.get("collector_semantic_sha256") == COLLECTOR_SEMANTIC_SHA256,
        "collector semantic SHA drift",
    )

    implementation = collector_implementation.collector_implementation_contract()
    _require(
        implementation.get("canonical_primitive_source_bindings_present") is False,
        "canonical primitive bindings unexpectedly present",
    )
    _require(
        implementation.get("canonical_collection_enabled") is False,
        "canonical collection unexpectedly enabled",
    )
    collector = collector_contract.validate_collector_contract()
    _require(
        collector.get("reviewed_collector_binding_present") is False,
        "reviewed collector binding unexpectedly active",
    )

    for field in (
        "canonical_provider_bindings_present",
        "canonical_collection_enabled",
        "reviewed_collector_binding_present",
        "runtime_readiness_admission_enabled",
        "runtime_execution_authorized",
    ):
        _require(manifest.get(field) is False, f"provider boundary drift: {field}")

    snapshots = manifest["snapshots"]
    _require(set(snapshots) == {V14, V10, V2R13, V8}, "snapshot set drift")
    _require(snapshots[V14]["required_primitive_count"] == 9, "V14 count drift")
    _require(snapshots[V10]["required_primitive_count"] == 9, "V10 count drift")
    _require(snapshots[V2R13]["required_primitive_count"] == 16, "V2 count drift")
    _require(
        snapshots[V8]["required_primitive_count_with_supplied_environment"] == 8,
        "V8 supplied-env count drift",
    )
    _require(
        snapshots[V8]["required_primitive_count_without_supplied_environment"] == 9,
        "V8 live-env count drift",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "provider_contract_sha256": EXPECTED_PROVIDER_CONTRACT_SHA256,
        "semantic_contract_valid": True,
        "canonical_provider_bindings_present": False,
        "canonical_collection_enabled": False,
        "reviewed_collector_binding_present": False,
        "runtime_readiness_admission_enabled": False,
        "live_observation_performed": False,
        "provider_execution_performed": False,
        "runtime_execution_authorized": False,
        "manifest": deepcopy(manifest),
    }


def collect_provider_evidence(*args: Any, **kwargs: Any) -> None:
    raise RuntimePrimitiveProviderContractHold(
        "GENERATION2_CANONICAL_PRIMITIVE_PROVIDERS_NOT_IMPLEMENTED"
    )
