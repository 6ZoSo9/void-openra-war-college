"""Non-executing observation-mechanics contract for Abaddon Generation-2.

This module records only observation mechanics that are supported by canonical
post-PR87 source.  It deliberately does not implement or perform evidence
collection.

Key distinction:

* V14/V10 have reviewed runtime identities and a game-facing chat-completions
  URL, but canonical source defines no runtime-specific identity observation
  route.  The inference endpoint must not be reinterpreted as an identity probe.
* V2R13 has a reviewed explicit path-binding surface for already-existing frozen
  source/engine roots, but no worktree creator and no reviewed active
  Ollama/model identity observation route.
* V8 has reviewed local preload verification surfaces.  Asset bytes can be
  verified without loading weights, and interpreter/package identity can be
  validated from supplied facts.  Actual `pip freeze` collection and the
  model/adapter path source remain separate collector concerns.  `load()` is
  outside the evidence boundary.

This source does not:
  * issue HTTP requests,
  * query systemd,
  * execute subprocesses,
  * create Git worktrees,
  * inspect live model servers,
  * load model weights,
  * start a runtime or game,
  * train/update/promote anything.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    RUNTIME_AUTHORITY_BLOCKER,
    V10,
    V14,
    V2R13,
    V8,
    activation_descriptor,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_evidence_generation2 import (
    evidence_requirement,
)

CONTRACT_SCHEMA = "void.abaddon.generation2.runtime-observation-mechanics.v1"
MECHANIC_SCHEMA = "void.abaddon.generation2.runtime-observation-mechanic.v1"

OBSERVATION_SURFACE_EXTRACT_SHA256 = (
    "2d0eef6e93021925b5e718b894f4099a83b1163797d4cb67e5d146cd782eb33c"
)

V8_RUNTIME_SOURCE_SHA256 = (
    "faf4b64ea4755fabdbdfc778f3df534a87f056a638763aa1560c7965c482b5af"
)
V2R13_PORTABLE_SOURCE_SHA256 = (
    "92e16e281d5a9036d78d900f35d854c6fb9783b2bf156c2acab69408d13a015d"
)

V8_ASSET_VERIFIER = (
    "openra_env.learning.apollyon_v8_campaign_runtime."
    "verify_v8_runtime_assets"
)
V8_ENVIRONMENT_VALIDATOR = (
    "openra_env.learning.apollyon_v8_campaign_runtime."
    "validate_v8_runtime_environment"
)
V8_LIVE_ENVIRONMENT_VERIFIER = (
    "openra_env.learning.apollyon_v8_campaign_runtime."
    "verify_v8_runtime_environment"
)
V8_MODEL_LOADER = (
    "openra_env.learning.apollyon_v8_campaign_runtime."
    "FrozenV8LocalToolRuntime.load"
)

V2R13_PATH_BINDER = (
    "openra_env.learning.apollyon_v2r13_portable_checkout."
    "reviewed_path_binding"
)
V2R13_PORTABLE_BINDING_CONTRACT = (
    "openra_env.learning.apollyon_v2r13_portable_checkout."
    "portable_binding_contract"
)

COMMON_AUTHORITY = {
    "collector_implementation_present": False,
    "observation_performed": False,
    "endpoint_probe_performed": False,
    "systemd_query_performed": False,
    "subprocess_execution_performed": False,
    "worktree_created": False,
    "model_weights_loaded": False,
    "runtime_selection_performed": False,
    "runtime_started": False,
    "runtime_execution_authorized": False,
    "game_execution": False,
    "model_execution": False,
    "training": False,
    "weights_updated": False,
    "automatic_policy_promotion": False,
}


class RuntimeObservationMechanicsHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeObservationMechanicsHold(message)


def _common(snapshot_id: str) -> dict[str, Any]:
    activation = activation_descriptor(snapshot_id)
    evidence = evidence_requirement(snapshot_id)
    _require(
        activation["snapshot_id"] == evidence["snapshot_id"],
        "activation/evidence snapshot mismatch",
    )
    _require(
        activation["snapshot_sha256"] == evidence["snapshot_sha256"],
        "activation/evidence snapshot SHA mismatch",
    )
    _require(
        activation["runtime_class"] == evidence["runtime_class"],
        "activation/evidence runtime class mismatch",
    )
    return {
        "schema": MECHANIC_SCHEMA,
        "snapshot_id": snapshot_id,
        "snapshot_sha256": activation["snapshot_sha256"],
        "runtime_class": activation["runtime_class"],
        "evidence_kind": evidence["evidence_kind"],
        "authority": deepcopy(COMMON_AUTHORITY),
    }


def _promoted_loopback_mechanics(snapshot_id: str) -> dict[str, Any]:
    activation = activation_descriptor(snapshot_id)
    evidence = evidence_requirement(snapshot_id)
    label = "V14" if snapshot_id == V14 else "V10"

    expected = evidence["expected"]
    _require(
        activation["chat_completions_url"] == expected["endpoint_url"],
        f"{label} activation/evidence endpoint drift",
    )
    _require(
        activation["expected_model_id"] == expected["active_model_id"],
        f"{label} activation/evidence model identity drift",
    )
    _require(
        activation["active_runtime_unit_sha256"]
        == expected["active_runtime_unit_sha256"],
        f"{label} activation/evidence runtime-unit drift",
    )

    return {
        **_common(snapshot_id),
        "mechanic_class": "unresolved_promoted_loopback_identity_channel",
        "known_inference_surface": {
            "chat_completions_url": activation["chat_completions_url"],
            "purpose": "game_facing_inference",
            "identity_probe_route": False,
            "identity_probe_may_reuse_inference_request": False,
        },
        "expected_identity": {
            "model_id": activation["expected_model_id"],
            "active_runtime_unit_sha256":
                activation["active_runtime_unit_sha256"],
        },
        "canonical_source_defined_identity_route": False,
        "generic_designated_host_systemd_discovery_admissible": False,
        "runtime_specific_service_name_defined": False,
        "collector_implementation_ready": False,
        "blockers": [
            f"{label}_IDENTITY_OBSERVATION_CHANNEL_UNRESOLVED",
            f"{label}_RUNTIME_UNIT_OBSERVATION_CHANNEL_UNRESOLVED",
            RUNTIME_AUTHORITY_BLOCKER,
        ],
    }


def _v2r13_mechanics() -> dict[str, Any]:
    activation = activation_descriptor(V2R13)
    evidence = evidence_requirement(V2R13)
    portable = activation["portable_checkout"]
    expected = evidence["expected"]

    _require(
        portable["frozen_war_college_commit"]
        == expected["frozen_war_college_commit"],
        "V2R13 source commit drift",
    )
    _require(
        portable["frozen_war_college_tree"]
        == expected["frozen_war_college_tree"],
        "V2R13 source tree drift",
    )
    _require(
        portable["frozen_engine_commit"] == expected["frozen_engine_commit"],
        "V2R13 engine commit drift",
    )

    return {
        **_common(V2R13),
        "mechanic_class": "split_preexisting_path_and_unresolved_live_identity",
        "known_inference_surface": {
            "chat_completions_url": activation["chat_completions_url"],
            "purpose": "game_facing_inference",
            "identity_probe_route": False,
            "identity_probe_may_reuse_inference_request": False,
        },
        "preexisting_path_binding": {
            "canonical_function": V2R13_PATH_BINDER,
            "canonical_source_sha256": V2R13_PORTABLE_SOURCE_SHA256,
            "portable_contract_function": V2R13_PORTABLE_BINDING_CONTRACT,
            "explicit_frozen_source_root_required": True,
            "explicit_exact_engine_root_required": True,
            "source_engine_roots_must_differ": True,
            "creates_worktrees": False,
            "mutates_canonical_checkout": False,
            "expected_frozen_war_college_commit":
                portable["frozen_war_college_commit"],
            "expected_frozen_war_college_tree":
                portable["frozen_war_college_tree"],
            "expected_frozen_engine_commit":
                portable["frozen_engine_commit"],
        },
        "live_runtime_identity": {
            "expected_model_alias": activation["expected_model_alias"],
            "expected_model_digest": activation["expected_model_digest"],
            "expected_runtime_image_id": activation["runtime_image_id"],
            "canonical_source_defined_identity_route": False,
        },
        "git_metadata_observation_implementation_present": False,
        "worktree_materializer_present": False,
        "live_model_identity_observation_implementation_present": False,
        "collector_implementation_ready": False,
        "blockers": [
            "V2R13_EXPLICIT_PREEXISTING_PATH_SOURCE_NOT_REVIEWED",
            "V2R13_GIT_METADATA_OBSERVATION_NOT_REVIEWED",
            "V2R13_LIVE_MODEL_IDENTITY_CHANNEL_UNRESOLVED",
            RUNTIME_AUTHORITY_BLOCKER,
        ],
    }


def _v8_mechanics() -> dict[str, Any]:
    activation = activation_descriptor(V8)
    evidence = evidence_requirement(V8)
    expected = evidence["expected"]

    _require(
        activation["tool_runtime_source_sha256"]
        == expected["tool_runtime_source_sha256"]
        == V8_RUNTIME_SOURCE_SHA256,
        "V8 runtime source identity drift",
    )

    return {
        **_common(V8),
        "mechanic_class": "local_preload_verification_with_unbound_paths",
        "asset_observation": {
            "canonical_function": V8_ASSET_VERIFIER,
            "canonical_source_sha256": V8_RUNTIME_SOURCE_SHA256,
            "model_dir_input_required": True,
            "adapter_dir_input_required": True,
            "preexisting_paths_required": True,
            "exact_file_hash_verification": True,
            "verified_file_count": 17,
            "loads_model_weights": False,
            "performs_model_inference": False,
            "collector_invocation_implemented": False,
        },
        "environment_observation": {
            "pure_validator_function": V8_ENVIRONMENT_VALIDATOR,
            "live_verifier_function": V8_LIVE_ENVIRONMENT_VERIFIER,
            "pure_validator_inputs": (
                "python_major_minor",
                "pip_freeze_sha256",
            ),
            "live_verifier_executes_pip_freeze": True,
            "live_verifier_collector_invocation_implemented": False,
        },
        "load_boundary": {
            "canonical_function": V8_MODEL_LOADER,
            "admissible_for_readiness_collection": False,
            "loads_model_weights": True,
            "must_remain_uninvoked": True,
        },
        "path_binding": {
            "model_dir_source_defined": False,
            "adapter_dir_source_defined": False,
            "explicit_preexisting_paths_required": True,
        },
        "collector_implementation_ready": False,
        "blockers": [
            "V8_MODEL_DIR_SOURCE_UNRESOLVED",
            "V8_ADAPTER_DIR_SOURCE_UNRESOLVED",
            "V8_LIVE_ENVIRONMENT_COLLECTION_NOT_REVIEWED",
            RUNTIME_AUTHORITY_BLOCKER,
        ],
    }


def observation_mechanics(snapshot_id: str) -> dict[str, Any]:
    """Return exact non-executing observation mechanics for one runtime."""
    if snapshot_id in {V14, V10}:
        return _promoted_loopback_mechanics(snapshot_id)
    if snapshot_id == V2R13:
        return _v2r13_mechanics()
    if snapshot_id == V8:
        return _v8_mechanics()
    raise RuntimeObservationMechanicsHold(
        f"unsupported reviewed snapshot: {snapshot_id!r}"
    )


def observation_mechanics_contract() -> dict[str, Any]:
    """Return the full four-runtime mechanics contract."""
    mechanics = [
        observation_mechanics(snapshot_id)
        for snapshot_id in (V14, V10, V2R13, V8)
    ]
    return {
        "schema": CONTRACT_SCHEMA,
        "observation_surface_extract_sha256":
            OBSERVATION_SURFACE_EXTRACT_SHA256,
        "runtime_count": 4,
        "mechanics": mechanics,
        "canonical_source_defined_api_path_count": 0,
        "chat_completions_urls_are_identity_probe_routes": False,
        "generic_designated_host_discovery_is_apollyon_identity_proof": False,
        "collector_implementation_present": False,
        "collector_implementation_ready": False,
        "runtime_execution_authorized": False,
        "authority": deepcopy(COMMON_AUTHORITY),
    }


def collector_build_request(snapshot_id: str) -> dict[str, Any]:
    """Return a fail-closed build descriptor; never implement or run a collector."""
    mechanic = observation_mechanics(snapshot_id)
    return {
        "snapshot_id": snapshot_id,
        "mechanic": mechanic,
        "collector_implementation_present": False,
        "collector_implementation_ready":
            mechanic["collector_implementation_ready"],
        "eligible": False,
        "reasons": list(mechanic["blockers"]),
        "runtime_execution_authorized": False,
    }


def collect_runtime_identity(*args: Any, **kwargs: Any) -> None:
    """Always hold: observation execution is deliberately absent."""
    raise RuntimeObservationMechanicsHold(
        "RUNTIME_IDENTITY_OBSERVATION_NOT_IMPLEMENTED: "
        "Generation-2 observation mechanics are source-only"
    )
