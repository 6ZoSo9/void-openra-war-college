"""Non-executing runtime-activation contract for Abaddon Generation-2.

This module refines the canonical Generation-2 execution descriptor into an
exact opponent-runtime activation requirement without implementing activation.

The four reviewed opponent surfaces are intentionally distinct:

* V14: externally activated promoted loopback OpenAI runtime on 127.0.0.1:11435
* V10: externally activated promoted loopback OpenAI runtime on 127.0.0.1:11435
* V2R13: externally activated legacy Ollama/OpenAI runtime on 127.0.0.1:11434,
         plus reviewed frozen-source/engine rebinding requirements
* V8: in-process accepted V8 runtime loader with exact model_dir/adapter_dir
      assets and live environment verification

A runtime descriptor or endpoint does NOT prove activation.  Every descriptor
remains ineligible until a separately reviewed activation implementation,
runtime-specific identity proof, and explicit runtime-execution authorization
exist.

This source never:
  * materializes an activation/start command,
  * starts/stops/reloads a service,
  * calls an HTTP/model endpoint,
  * creates a frozen worktree,
  * loads V8 model weights,
  * creates campaign output directories,
  * launches the legacy runner or candidate wrapper,
  * launches OpenRA,
  * trains, updates weights, or promotes policy.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning.abaddon_policy_campaign_execution_adapter_generation2 import (
    execution_descriptor,
)
from openra_env.learning.apollyon_opponent_runtime_realizations import (
    reviewed_opponent_runtime_realizations,
)

CONTRACT_SCHEMA = "void.abaddon.generation2.runtime-activation-contract.v1"
ACTIVATION_DESCRIPTOR_SCHEMA = (
    "void.abaddon.generation2.runtime-activation-descriptor.v1"
)
ARM_ACTIVATION_PLAN_SCHEMA = (
    "void.abaddon.generation2.arm-runtime-activation-plan.v1"
)

RUNTIME_REALIZATION_SET_SHA256 = (
    "1dbb861a3bc03a4423187846a519f228726cc890f4452c3b1d8607614288a7d8"
)
LEGACY_RUNNER_SHA256 = (
    "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
)

STRICT_EXECUTION_SURFACE_AUDIT_SHA256 = (
    "b3e086d669dd3f107f81cb8ddb32af9c98e9121ca6a4c4de37a70d6e6852899d"
)
LEGACY_RUN_IDENTITY_AUDIT_SHA256 = (
    "4ebe56524a5a849dc5ea55342b03acd98921ef8dee1cfd302a490c0fa05bfe0f"
)

V14 = "apollyon-v13-v14-promoted"
V10 = "apollyon-v13-v10-promoted"
V2R13 = "apollyon-v2r13-qualified-predecessor"
V8 = "apollyon-v3-v8-accepted-model-control"

EXPECTED_SNAPSHOT_IDS = {V14, V10, V2R13, V8}

V14_MODEL_ID = "void-apollyon-v3-v13-guard-first-v14-promoted"
V10_MODEL_ID = "void-apollyon-v3-v13-guard-first-v10-shadow"
V2R13_MODEL_ALIAS = "void-apollyon-candidate-v2r13:latest"
V2R13_MODEL_DIGEST = (
    "b52834ea46c10362e9bb20cd2e721716016bb36f800ddbc62e7fbaa24fb40932"
)

LOOPBACK_11435 = "http://127.0.0.1:11435/v1/chat/completions"
LOOPBACK_11434 = "http://127.0.0.1:11434/v1/chat/completions"

V14_ACTIVE_RUNTIME_UNIT_SHA256 = (
    "5ff3a1279f8cf387b9ff27975463c63f0d33da5b16998cfd8993fe2c88990b30"
)
V10_ACTIVE_RUNTIME_UNIT_SHA256 = (
    "407f5f8514502005ecbaefd7e7df7caf90d8024e496f948c3db90d6405d6f320"
)

V2R13_FROZEN_WAR_COLLEGE_COMMIT = (
    "973802ef0a614e5afa782ff20e231e18966ae3e5"
)
V2R13_FROZEN_WAR_COLLEGE_TREE = (
    "d8a2af418af00e95ca0f203a2f0264851f2308c6"
)
V2R13_FROZEN_ENGINE_COMMIT = (
    "1607a7a6501d42a47638393ecef8b22831064932"
)
V2R13_RUNTIME_IMAGE_ID = (
    "sha256:79f2f6800382489a2a648839fc0d58e546384938439378aeea06461363de25f5"
)

V8_TOOL_RUNTIME_SOURCE_SHA256 = (
    "faf4b64ea4755fabdbdfc778f3df534a87f056a638763aa1560c7965c482b5af"
)
V8_TOOL_RUNTIME_CONTRACT_SHA256 = (
    "ef28f9bf884d882ccbe40bb9774ea0010782791717ad527d5b01c649bdcbd334"
)
V8_BASE_MODEL_REVISION = "3764fa359b9082ea5a1e4a5e3ac3aaf6e9671636"
V8_BASE_MODEL_CONFIG_SHA256 = (
    "14687c353af8012cc1b563b3aeeefaa0b78d8780d8ea5270c73fe9fcdb7387f2"
)
V8_BASE_MODEL_SHARD1_SHA256 = (
    "26a93f066e1916adb13453dae5a0c707c0fbc71299ed98779571a907b8e74c61"
)
V8_BASE_MODEL_SHARD2_SHA256 = (
    "cb544bd9bfae93dc59b0f22b292f5933573854a7f9b97835c67060d7d910e188"
)
V8_CHAT_TEMPLATE_SHA256 = (
    "8452ca85cb1e0ff04304c02f417a53305d5ba17f6eb9d5693343ad8355f985a8"
)
V8_TOKENIZER_JSON_SHA256 = (
    "87a7830d63fcf43bf241c3c5242e96e62dd3fdc29224ca26fed8ea333db72de4"
)

RUNTIME_AUTHORITY_BLOCKER = "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED"

NATIVE_RUN_NAMESPACE = {
    "legacy_runner_sha256": LEGACY_RUNNER_SHA256,
    "runs_dir_formula": 'DOJO / "war-college" / "joint-duels"',
    "run_id_formula": (
        '"warmstart-apollyon-vs-abaddon-<UTC_%Y%m%dT%H%M%SZ>-"'
        ' + "<doctrine.lower()>-s<seed>"'
    ),
    "run_dir_formula": "RUNS_DIR / run_id",
    "timestamp_granularity": "seconds",
    "primary_outputs": (
        "warm-start.jsonl",
        "trajectory.jsonl",
        "summary.json",
    ),
    "primary_outputs_direct_children_of_run_dir": True,
    "run_dir_collision_check_present": True,
    "run_dir_mkdir_present": True,
    "overwrite_safe": True,
    "run_id_uniqueness_evidence_present": True,
    "run_id_uniqueness_guaranteed": False,
    "collision_refusal_required": True,
    "additional_outer_workdir_isolation_required": False,
}


class RuntimeActivationHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeActivationHold(message)


def _runtime_index() -> dict[str, dict[str, Any]]:
    value = reviewed_opponent_runtime_realizations()
    _require(
        value.get("realization_set_sha256") == RUNTIME_REALIZATION_SET_SHA256,
        "runtime realization-set SHA drift",
    )
    _require(
        value.get("opponent_runtime_realization_complete") is True,
        "runtime realization set incomplete",
    )
    rows = value.get("realizations")
    _require(isinstance(rows, list) and len(rows) == 4, "runtime realization count drift")

    result: dict[str, dict[str, Any]] = {}
    for raw in rows:
        _require(isinstance(raw, Mapping), "runtime realization malformed")
        snapshot_id = raw.get("snapshot_id")
        _require(snapshot_id in EXPECTED_SNAPSHOT_IDS, "unexpected runtime snapshot id")
        _require(snapshot_id not in result, "duplicate runtime snapshot id")
        _require(raw.get("current_campaign_runtime_realized") is True, "runtime not realized")
        _require(raw.get("runtime_surface_realized") is True, "runtime surface unrealized")
        _require(raw.get("warm_start_input_surface_compatible") is True, "warm-start incompatible")
        _require(
            raw.get("portable_current_checkout_binding_complete") is True,
            "portable checkout binding incomplete",
        )
        _require(raw.get("blockers") == [], "realization carries blocker")
        result[str(snapshot_id)] = deepcopy(dict(raw))

    _require(set(result) == EXPECTED_SNAPSHOT_IDS, "runtime snapshot set drift")
    return result


def _authority() -> dict[str, bool]:
    return {
        "runtime_execution_authorized": False,
        "runtime_selection_performed": False,
        "runtime_started": False,
        "model_execution": False,
        "game_execution": False,
        "training": False,
        "weights_updated": False,
        "automatic_corpus_admission": False,
        "automatic_policy_promotion": False,
        "deployment": False,
    }


def _external_loopback_descriptor(
    realization: Mapping[str, Any],
    *,
    model_id: str,
    active_runtime_unit_sha256: str,
    snapshot_label: str,
) -> dict[str, Any]:
    identity = realization["identity"]
    _require(identity.get("model_id") == model_id, f"{snapshot_label} model ID drift")
    _require(
        identity.get("active_runtime_unit_sha256") == active_runtime_unit_sha256,
        f"{snapshot_label} runtime-unit SHA drift",
    )
    _require(
        identity.get("chat_completions_url") == LOOPBACK_11435,
        f"{snapshot_label} endpoint drift",
    )

    return {
        "activation_kind": "external_loopback_openai_runtime",
        "chat_completions_url": LOOPBACK_11435,
        "expected_model_id": model_id,
        "active_runtime_unit_sha256": active_runtime_unit_sha256,
        "endpoint_liveness_proves_identity": False,
        "runtime_specific_activation_binding_reviewed": False,
        "runtime_specific_identity_probe_reviewed": False,
        "activation_command_materialized": False,
        "service_action_materialized": False,
        "ready_probe_materialized": False,
        "requirements": {
            "endpoint_must_be_loopback": True,
            "active_model_identity_must_match": True,
            "runtime_unit_identity_must_match": True,
            "translation_surface_must_remain_reviewed": True,
            "host_validation_unchanged": True,
        },
        "blockers": [
            f"{snapshot_label}_ACTIVATION_BINDING_NOT_REVIEWED",
            f"{snapshot_label}_ACTIVE_MODEL_IDENTITY_PROBE_NOT_REVIEWED",
            RUNTIME_AUTHORITY_BLOCKER,
        ],
    }


def activation_descriptor(snapshot_id: str) -> dict[str, Any]:
    """Return one exact non-executing activation requirement."""
    runtimes = _runtime_index()
    _require(snapshot_id in runtimes, f"unknown snapshot id: {snapshot_id!r}")
    realization = runtimes[snapshot_id]
    identity = realization["identity"]

    common = {
        "schema": ACTIVATION_DESCRIPTOR_SCHEMA,
        "snapshot_id": snapshot_id,
        "snapshot_sha256": realization["snapshot_sha256"],
        "runtime_class": realization["runtime_class"],
        "realization_sha256": realization["realization_sha256"],
        "runtime_surface_realized": True,
        "activation_proven": False,
        "selection_performed": False,
        "activation_performed": False,
        "runtime_started": False,
        "eligible": False,
        "authority": _authority(),
    }

    if snapshot_id == V14:
        details = _external_loopback_descriptor(
            realization,
            model_id=V14_MODEL_ID,
            active_runtime_unit_sha256=V14_ACTIVE_RUNTIME_UNIT_SHA256,
            snapshot_label="V14",
        )

    elif snapshot_id == V10:
        details = _external_loopback_descriptor(
            realization,
            model_id=V10_MODEL_ID,
            active_runtime_unit_sha256=V10_ACTIVE_RUNTIME_UNIT_SHA256,
            snapshot_label="V10",
        )

    elif snapshot_id == V2R13:
        _require(
            identity.get("model_alias") == V2R13_MODEL_ALIAS,
            "V2R13 model alias drift",
        )
        _require(
            identity.get("model_digest") == V2R13_MODEL_DIGEST,
            "V2R13 model digest drift",
        )
        _require(
            identity.get("chat_completions_url") == LOOPBACK_11434,
            "V2R13 endpoint drift",
        )
        _require(
            identity.get("frozen_war_college_commit")
            == V2R13_FROZEN_WAR_COLLEGE_COMMIT,
            "V2R13 frozen source commit drift",
        )
        _require(
            identity.get("frozen_war_college_tree")
            == V2R13_FROZEN_WAR_COLLEGE_TREE,
            "V2R13 frozen source tree drift",
        )
        _require(
            identity.get("engine_commit") == V2R13_FROZEN_ENGINE_COMMIT,
            "V2R13 engine commit drift",
        )
        _require(
            identity.get("runtime_image_id") == V2R13_RUNTIME_IMAGE_ID,
            "V2R13 runtime image drift",
        )

        details = {
            "activation_kind": "external_legacy_ollama_openai_runtime",
            "chat_completions_url": LOOPBACK_11434,
            "expected_model_alias": V2R13_MODEL_ALIAS,
            "expected_model_digest": V2R13_MODEL_DIGEST,
            "runtime_image_id": V2R13_RUNTIME_IMAGE_ID,
            "endpoint_liveness_proves_identity": False,
            "runtime_specific_activation_binding_reviewed": False,
            "runtime_specific_identity_probe_reviewed": False,
            "activation_command_materialized": False,
            "service_action_materialized": False,
            "ready_probe_materialized": False,
            "portable_checkout": {
                "source_materialization": "detached_git_worktree",
                "frozen_war_college_commit": V2R13_FROZEN_WAR_COLLEGE_COMMIT,
                "frozen_war_college_tree": V2R13_FROZEN_WAR_COLLEGE_TREE,
                "frozen_engine_commit": V2R13_FROZEN_ENGINE_COMMIT,
                "source_worktree_path_bound": False,
                "engine_worktree_path_bound": False,
                "worktree_materialization_implemented": False,
                "portable_runner_binding_install_performed": False,
                "canonical_checkout_mutation_required": False,
                "cleanup_required": True,
            },
            "requirements": {
                "endpoint_must_be_loopback": True,
                "active_model_alias_must_match": True,
                "active_model_digest_must_match": True,
                "runtime_image_identity_must_match": True,
                "frozen_source_worktree_must_be_exact": True,
                "exact_engine_worktree_must_be_exact": True,
                "host_validation_unchanged": True,
            },
            "blockers": [
                "V2R13_ACTIVATION_BINDING_NOT_REVIEWED",
                "V2R13_ACTIVE_MODEL_DIGEST_PROBE_NOT_REVIEWED",
                "V2R13_FROZEN_WORKTREE_MATERIALIZER_NOT_REVIEWED",
                RUNTIME_AUTHORITY_BLOCKER,
            ],
        }

    elif snapshot_id == V8:
        _require(
            identity.get("tool_runtime_source_sha256")
            == V8_TOOL_RUNTIME_SOURCE_SHA256,
            "V8 tool-runtime source SHA drift",
        )
        _require(
            identity.get("tool_runtime_contract_sha256")
            == V8_TOOL_RUNTIME_CONTRACT_SHA256,
            "V8 tool-runtime contract SHA drift",
        )
        _require(
            identity.get("base_model_revision") == V8_BASE_MODEL_REVISION,
            "V8 base-model revision drift",
        )
        _require(
            identity.get("base_model_config_sha256") == V8_BASE_MODEL_CONFIG_SHA256,
            "V8 base-model config SHA drift",
        )
        _require(
            identity.get("base_model_shard1_sha256") == V8_BASE_MODEL_SHARD1_SHA256,
            "V8 base-model shard1 SHA drift",
        )
        _require(
            identity.get("base_model_shard2_sha256") == V8_BASE_MODEL_SHARD2_SHA256,
            "V8 base-model shard2 SHA drift",
        )
        _require(
            identity.get("chat_template_sha256") == V8_CHAT_TEMPLATE_SHA256,
            "V8 chat-template SHA drift",
        )
        _require(
            identity.get("tokenizer_json_sha256") == V8_TOKENIZER_JSON_SHA256,
            "V8 tokenizer JSON SHA drift",
        )

        details = {
            "activation_kind": "inprocess_accepted_v8_runtime",
            "chat_completions_url": None,
            "tool_runtime_source_sha256": V8_TOOL_RUNTIME_SOURCE_SHA256,
            "tool_runtime_contract_sha256": V8_TOOL_RUNTIME_CONTRACT_SHA256,
            "runtime_specific_activation_binding_reviewed": False,
            "runtime_specific_identity_probe_reviewed": False,
            "load_call_materialized": False,
            "model_weights_loaded": False,
            "model_dir_path_bound": False,
            "adapter_dir_path_bound": False,
            "requirements": {
                "model_dir_required": True,
                "adapter_dir_required": True,
                "base_model_revision": V8_BASE_MODEL_REVISION,
                "base_model_config_sha256": V8_BASE_MODEL_CONFIG_SHA256,
                "base_model_shard1_sha256": V8_BASE_MODEL_SHARD1_SHA256,
                "base_model_shard2_sha256": V8_BASE_MODEL_SHARD2_SHA256,
                "chat_template_sha256": V8_CHAT_TEMPLATE_SHA256,
                "tokenizer_json_sha256": V8_TOKENIZER_JSON_SHA256,
                "runtime_assets_hash_verified_before_load": True,
                "runtime_environment_live_pip_freeze_match_required": True,
                "offline_only_model_load": True,
                "host_validation_unchanged": True,
            },
            "blockers": [
                "V8_MODEL_DIR_BINDING_NOT_REVIEWED",
                "V8_ADAPTER_DIR_BINDING_NOT_REVIEWED",
                "V8_LOAD_CALL_BINDING_NOT_REVIEWED",
                RUNTIME_AUTHORITY_BLOCKER,
            ],
        }

    else:
        raise RuntimeActivationHold(f"unhandled snapshot id: {snapshot_id}")

    return {**common, **details}


def activation_contract() -> dict[str, Any]:
    """Return the full four-runtime non-executing activation contract."""
    descriptors = [
        activation_descriptor(snapshot_id)
        for snapshot_id in (V14, V10, V2R13, V8)
    ]

    return {
        "schema": CONTRACT_SCHEMA,
        "runtime_realization_set_sha256": RUNTIME_REALIZATION_SET_SHA256,
        "strict_execution_surface_audit_sha256":
            STRICT_EXECUTION_SURFACE_AUDIT_SHA256,
        "legacy_run_identity_audit_sha256":
            LEGACY_RUN_IDENTITY_AUDIT_SHA256,
        "runtime_count": 4,
        "descriptors": descriptors,
        "native_run_namespace": deepcopy(NATIVE_RUN_NAMESPACE),
        "cross_control_activation_implementation_present": False,
        "runtime_selection_implementation_present": False,
        "activation_commands_materialized": False,
        "service_actions_materialized": False,
        "ready_probes_materialized": False,
        "runtime_execution_authorized": False,
        "authority": _authority(),
    }


def arm_runtime_activation_plan(
    *,
    pair_slot: int,
    arm: str,
) -> dict[str, Any]:
    """Bind one canonical arm descriptor to its exact runtime requirement."""
    arm_descriptor = execution_descriptor(pair_slot=pair_slot, arm=arm)
    opponent = arm_descriptor["apollyon_opponent"]
    _require(
        opponent.get("selection_boundary")
        == "EXTERNAL_PRELAUNCH_REVIEWED_RUNTIME_REALIZATION",
        "arm runtime-selection boundary drift",
    )
    _require(
        opponent.get("selection_performed") is False,
        "arm unexpectedly reports runtime selection",
    )
    _require(
        opponent.get("runtime_started") is False,
        "arm unexpectedly reports runtime start",
    )

    activation = activation_descriptor(opponent["snapshot_id"])
    _require(
        activation["snapshot_sha256"] == opponent["snapshot_sha256"],
        "arm/runtime snapshot SHA mismatch",
    )
    _require(
        activation["runtime_class"]
        == opponent["runtime_realization"]["runtime_class"],
        "arm/runtime class mismatch",
    )

    return {
        "schema": ARM_ACTIVATION_PLAN_SCHEMA,
        "pair_slot": pair_slot,
        "arm": arm,
        "execution_index": arm_descriptor["execution_index"],
        "held_out": arm_descriptor["held_out"],
        "opponent_snapshot_id": opponent["snapshot_id"],
        "activation": activation,
        "native_run_namespace": deepcopy(NATIVE_RUN_NAMESPACE),
        "activation_implementation_present": False,
        "runtime_selection_performed": False,
        "runtime_started": False,
        "command_materialized": False,
        "eligible": False,
        "reasons": list(activation["blockers"]),
        "authority": _authority(),
    }


def all_arm_runtime_activation_plans() -> list[dict[str, Any]]:
    """Return all 36 non-executing arm/runtime plans in canonical order."""
    plans: list[dict[str, Any]] = []
    for pair_slot in range(1, 19):
        for arm in ("baseline", "candidate"):
            plans.append(
                arm_runtime_activation_plan(
                    pair_slot=pair_slot,
                    arm=arm,
                )
            )
    _require(len(plans) == 36, "arm/runtime plan count drift")
    return plans


def activate_runtime(*args: Any, **kwargs: Any) -> None:
    """Always hold: runtime activation is deliberately not implemented."""
    raise RuntimeActivationHold(
        "RUNTIME_ACTIVATION_IMPLEMENTATION_NOT_PRESENT: "
        "Generation-2 runtime activation contract is non-executing"
    )
