"""Fail-closed non-executing activation-evidence contract for Generation-2.

This module defines the exact read-only evidence shape required to prove that
one reviewed Apollyon opponent runtime is ready for an Abaddon Generation-2 arm.

It deliberately does not implement evidence collection.  In particular it does
not:
  * start/stop/reload a service,
  * probe an endpoint,
  * create or mutate a Git worktree,
  * load V8 model weights,
  * launch OpenRA,
  * launch the legacy runner or candidate wrapper,
  * train/update/promote anything.

Evidence shape and evidence admission are separate:

  * validate_evidence_shape() proves that a supplied object has the exact
    expected values for the selected reviewed runtime.
  * admit_evidence() additionally requires a separately reviewed collector
    binding.  There is no canonical collector binding in this source, so callers
    cannot turn self-reported evidence into an admitted runtime proof.

The contract therefore closes evidence semantics without crossing the runtime
execution boundary.
"""

from __future__ import annotations

import re
from copy import deepcopy
from pathlib import PurePath
from typing import Any, Mapping

from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    RUNTIME_AUTHORITY_BLOCKER,
    V10,
    V14,
    V2R13,
    V8,
    activation_descriptor,
    arm_runtime_activation_plan,
)

CONTRACT_SCHEMA = "void.abaddon.generation2.runtime-activation-evidence-contract.v1"
REQUIREMENT_SCHEMA = "void.abaddon.generation2.runtime-activation-evidence-requirement.v1"
EVIDENCE_SCHEMA = "void.abaddon.generation2.runtime-activation-evidence.v1"
ADMISSION_SCHEMA = "void.abaddon.generation2.runtime-activation-evidence-admission.v1"

ACTIVATION_BINDING_CENSUS_SHA256 = (
    "96261e01c4c3fdb16875f8391ca47adfc6c87b279abfc894d5ac7aa1b2526d33"
)

SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")

V14_EVIDENCE_KIND = "external-loopback-openai-runtime-readiness"
V10_EVIDENCE_KIND = "external-loopback-openai-runtime-readiness"
V2R13_EVIDENCE_KIND = "external-legacy-ollama-openai-runtime-readiness"
V8_EVIDENCE_KIND = "inprocess-v8-preload-readiness"

COMMON_FIELDS = (
    "schema",
    "snapshot_id",
    "snapshot_sha256",
    "runtime_class",
    "evidence_kind",
    "collector_contract_sha256",
    "observation_mode",
    "mutation_performed",
    "service_action_performed",
    "runtime_start_performed",
    "game_execution_performed",
    "model_inference_performed",
)

EXTERNAL_LOOPBACK_FIELDS = COMMON_FIELDS + (
    "endpoint_url",
    "endpoint_loopback",
    "endpoint_liveness",
    "active_model_id",
    "model_identity_verified",
    "active_runtime_unit_sha256",
    "runtime_unit_identity_verified",
)

V2R13_FIELDS = COMMON_FIELDS + (
    "endpoint_url",
    "endpoint_loopback",
    "endpoint_liveness",
    "active_model_alias",
    "active_model_digest",
    "model_identity_verified",
    "runtime_image_id",
    "runtime_image_identity_verified",
    "frozen_source_worktree",
    "engine_worktree",
    "portable_binding_attested",
)

V8_FIELDS = COMMON_FIELDS + (
    "model_dir",
    "adapter_dir",
    "model_dir_bound",
    "adapter_dir_bound",
    "tool_runtime_source_sha256",
    "tool_runtime_contract_sha256",
    "base_model_revision",
    "base_model_config_sha256",
    "base_model_shard1_sha256",
    "base_model_shard2_sha256",
    "chat_template_sha256",
    "tokenizer_json_sha256",
    "runtime_assets_verified",
    "runtime_environment_verified",
    "offline_only_verified",
    "model_weights_loaded",
    "load_call_performed",
)

COMMON_REQUIRED_FALSE = (
    "mutation_performed",
    "service_action_performed",
    "runtime_start_performed",
    "game_execution_performed",
    "model_inference_performed",
)

REVIEWED_COLLECTOR_BINDING_PRESENT = False


class RuntimeActivationEvidenceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeActivationEvidenceHold(message)


def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and SHA256_RE.fullmatch(value) is not None


def _require_exact_fields(record: Mapping[str, Any], fields: tuple[str, ...]) -> None:
    actual = set(record)
    expected = set(fields)
    _require(
        actual == expected,
        "evidence field set drift: "
        f"missing={sorted(expected - actual)!r} extra={sorted(actual - expected)!r}",
    )


def _require_absolute_nonnormalized_path(value: Any, label: str) -> str:
    _require(isinstance(value, str) and bool(value), f"{label} missing")
    path = PurePath(value)
    _require(path.is_absolute(), f"{label} must be absolute")
    _require(".." not in path.parts, f"{label} may not contain parent traversal")
    return value


def _common_requirement(snapshot_id: str) -> dict[str, Any]:
    activation = activation_descriptor(snapshot_id)
    return {
        "schema": REQUIREMENT_SCHEMA,
        "snapshot_id": activation["snapshot_id"],
        "snapshot_sha256": activation["snapshot_sha256"],
        "runtime_class": activation["runtime_class"],
        "activation_proven_before_collection": activation["activation_proven"],
        "runtime_execution_authorized": False,
        "collector_binding_reviewed": False,
        "collector_may_mutate": False,
        "collector_may_start_runtime": False,
        "collector_may_execute_game": False,
        "collector_may_run_model_inference": False,
    }


def evidence_requirement(snapshot_id: str) -> dict[str, Any]:
    """Return the exact read-only evidence requirements for one snapshot."""
    activation = activation_descriptor(snapshot_id)
    common = _common_requirement(snapshot_id)

    if snapshot_id in {V14, V10}:
        label = "V14" if snapshot_id == V14 else "V10"
        return {
            **common,
            "evidence_kind": (
                V14_EVIDENCE_KIND if snapshot_id == V14 else V10_EVIDENCE_KIND
            ),
            "required_fields": EXTERNAL_LOOPBACK_FIELDS,
            "expected": {
                "endpoint_url": activation["chat_completions_url"],
                "endpoint_loopback": True,
                "active_model_id": activation["expected_model_id"],
                "active_runtime_unit_sha256":
                    activation["active_runtime_unit_sha256"],
            },
            "required_true": (
                "endpoint_liveness",
                "model_identity_verified",
                "runtime_unit_identity_verified",
            ),
            "required_false": COMMON_REQUIRED_FALSE,
            "unresolved_collector_blockers": (
                f"{label}_READONLY_ENDPOINT_PROBE_COLLECTOR_NOT_REVIEWED",
                f"{label}_ACTIVE_MODEL_IDENTITY_COLLECTOR_NOT_REVIEWED",
                f"{label}_RUNTIME_UNIT_IDENTITY_COLLECTOR_NOT_REVIEWED",
                RUNTIME_AUTHORITY_BLOCKER,
            ),
        }

    if snapshot_id == V2R13:
        portable = activation["portable_checkout"]
        return {
            **common,
            "evidence_kind": V2R13_EVIDENCE_KIND,
            "required_fields": V2R13_FIELDS,
            "expected": {
                "endpoint_url": activation["chat_completions_url"],
                "endpoint_loopback": True,
                "active_model_alias": activation["expected_model_alias"],
                "active_model_digest": activation["expected_model_digest"],
                "runtime_image_id": activation["runtime_image_id"],
                "frozen_war_college_commit":
                    portable["frozen_war_college_commit"],
                "frozen_war_college_tree":
                    portable["frozen_war_college_tree"],
                "frozen_engine_commit":
                    portable["frozen_engine_commit"],
            },
            "required_true": (
                "endpoint_liveness",
                "model_identity_verified",
                "runtime_image_identity_verified",
                "portable_binding_attested",
            ),
            "required_false": COMMON_REQUIRED_FALSE,
            "frozen_source_worktree_fields": (
                "path",
                "exists",
                "is_directory",
                "is_symlink",
                "clean",
                "detached",
                "head_commit",
                "tree_sha",
            ),
            "engine_worktree_fields": (
                "path",
                "exists",
                "is_directory",
                "is_symlink",
                "clean",
                "head_commit",
            ),
            "unresolved_collector_blockers": (
                "V2R13_READONLY_ENDPOINT_PROBE_COLLECTOR_NOT_REVIEWED",
                "V2R13_ACTIVE_MODEL_DIGEST_COLLECTOR_NOT_REVIEWED",
                "V2R13_RUNTIME_IMAGE_IDENTITY_COLLECTOR_NOT_REVIEWED",
                "V2R13_FROZEN_WORKTREE_DISCOVERY_COLLECTOR_NOT_REVIEWED",
                RUNTIME_AUTHORITY_BLOCKER,
            ),
        }

    if snapshot_id == V8:
        req = activation["requirements"]
        return {
            **common,
            "evidence_kind": V8_EVIDENCE_KIND,
            "required_fields": V8_FIELDS,
            "expected": {
                "tool_runtime_source_sha256":
                    activation["tool_runtime_source_sha256"],
                "tool_runtime_contract_sha256":
                    activation["tool_runtime_contract_sha256"],
                "base_model_revision": req["base_model_revision"],
                "base_model_config_sha256": req["base_model_config_sha256"],
                "base_model_shard1_sha256": req["base_model_shard1_sha256"],
                "base_model_shard2_sha256": req["base_model_shard2_sha256"],
                "chat_template_sha256": req["chat_template_sha256"],
                "tokenizer_json_sha256": req["tokenizer_json_sha256"],
            },
            "required_true": (
                "model_dir_bound",
                "adapter_dir_bound",
                "runtime_assets_verified",
                "runtime_environment_verified",
                "offline_only_verified",
            ),
            "required_false": COMMON_REQUIRED_FALSE + (
                "model_weights_loaded",
                "load_call_performed",
            ),
            "unresolved_collector_blockers": (
                "V8_MODEL_DIR_DISCOVERY_COLLECTOR_NOT_REVIEWED",
                "V8_ADAPTER_DIR_DISCOVERY_COLLECTOR_NOT_REVIEWED",
                "V8_ASSET_IDENTITY_COLLECTOR_NOT_REVIEWED",
                "V8_RUNTIME_ENVIRONMENT_COLLECTOR_NOT_REVIEWED",
                RUNTIME_AUTHORITY_BLOCKER,
            ),
        }

    raise RuntimeActivationEvidenceHold(f"unsupported reviewed snapshot: {snapshot_id}")


def evidence_contract() -> dict[str, Any]:
    """Return the full non-executing evidence contract."""
    rows = [
        evidence_requirement(snapshot_id)
        for snapshot_id in (V14, V10, V2R13, V8)
    ]
    return {
        "schema": CONTRACT_SCHEMA,
        "activation_binding_census_sha256": ACTIVATION_BINDING_CENSUS_SHA256,
        "runtime_count": 4,
        "requirements": rows,
        "reviewed_collector_binding_present": False,
        "collector_implementation_present": False,
        "endpoint_probe_implemented": False,
        "service_query_implemented": False,
        "worktree_discovery_implemented": False,
        "v8_path_discovery_implemented": False,
        "runtime_execution_authorized": False,
    }


def _validate_common(
    record: Mapping[str, Any],
    requirement: Mapping[str, Any],
) -> None:
    _require(
        record.get("schema") == EVIDENCE_SCHEMA,
        "activation evidence schema drift",
    )
    for key in ("snapshot_id", "snapshot_sha256", "runtime_class", "evidence_kind"):
        _require(
            record.get(key) == requirement.get(key),
            f"activation evidence identity drift: {key}",
        )
    _require(
        _is_sha256(record.get("collector_contract_sha256")),
        "collector contract SHA malformed",
    )
    _require(
        record.get("observation_mode") == "read_only",
        "activation evidence observation mode must be read_only",
    )
    for key in requirement["required_true"]:
        _require(record.get(key) is True, f"activation evidence lacks true field: {key}")
    for key in requirement["required_false"]:
        _require(record.get(key) is False, f"activation evidence crossed authority boundary: {key}")


def _validate_external_loopback(
    record: Mapping[str, Any],
    requirement: Mapping[str, Any],
) -> None:
    expected = requirement["expected"]
    _require(
        record.get("endpoint_url") == expected["endpoint_url"],
        "loopback endpoint drift",
    )
    _require(record.get("endpoint_loopback") is True, "endpoint is not loopback")
    _require(
        record.get("active_model_id") == expected["active_model_id"],
        "active model ID drift",
    )
    _require(
        record.get("active_runtime_unit_sha256")
        == expected["active_runtime_unit_sha256"],
        "active runtime unit SHA drift",
    )
    _require(
        _is_sha256(record.get("active_runtime_unit_sha256")),
        "active runtime unit SHA malformed",
    )


def _validate_v2r13(
    record: Mapping[str, Any],
    requirement: Mapping[str, Any],
) -> None:
    expected = requirement["expected"]
    _require(
        record.get("endpoint_url") == expected["endpoint_url"],
        "V2R13 endpoint drift",
    )
    _require(record.get("endpoint_loopback") is True, "V2R13 endpoint not loopback")
    _require(
        record.get("active_model_alias") == expected["active_model_alias"],
        "V2R13 model alias drift",
    )
    _require(
        record.get("active_model_digest") == expected["active_model_digest"],
        "V2R13 model digest drift",
    )
    _require(
        record.get("runtime_image_id") == expected["runtime_image_id"],
        "V2R13 runtime image drift",
    )

    source = record.get("frozen_source_worktree")
    engine = record.get("engine_worktree")
    _require(isinstance(source, Mapping), "V2R13 frozen source worktree missing")
    _require(isinstance(engine, Mapping), "V2R13 engine worktree missing")

    _require_exact_fields(
        source,
        requirement["frozen_source_worktree_fields"],
    )
    _require_exact_fields(
        engine,
        requirement["engine_worktree_fields"],
    )

    _require_absolute_nonnormalized_path(source.get("path"), "frozen source path")
    _require_absolute_nonnormalized_path(engine.get("path"), "engine worktree path")
    _require(source.get("path") != engine.get("path"), "source/engine worktrees must differ")

    for key in ("exists", "is_directory", "clean", "detached"):
        _require(source.get(key) is True, f"frozen source worktree lacks {key}")
    _require(source.get("is_symlink") is False, "frozen source worktree is symlinked")
    _require(
        source.get("head_commit") == expected["frozen_war_college_commit"],
        "frozen source commit drift",
    )
    _require(
        source.get("tree_sha") == expected["frozen_war_college_tree"],
        "frozen source tree drift",
    )

    for key in ("exists", "is_directory", "clean"):
        _require(engine.get(key) is True, f"engine worktree lacks {key}")
    _require(engine.get("is_symlink") is False, "engine worktree is symlinked")
    _require(
        engine.get("head_commit") == expected["frozen_engine_commit"],
        "engine commit drift",
    )


def _validate_v8(
    record: Mapping[str, Any],
    requirement: Mapping[str, Any],
) -> None:
    model_dir = _require_absolute_nonnormalized_path(
        record.get("model_dir"),
        "V8 model_dir",
    )
    adapter_dir = _require_absolute_nonnormalized_path(
        record.get("adapter_dir"),
        "V8 adapter_dir",
    )
    _require(model_dir != adapter_dir, "V8 model_dir and adapter_dir must differ")
    expected = requirement["expected"]
    for key in (
        "tool_runtime_source_sha256",
        "tool_runtime_contract_sha256",
        "base_model_revision",
        "base_model_config_sha256",
        "base_model_shard1_sha256",
        "base_model_shard2_sha256",
        "chat_template_sha256",
        "tokenizer_json_sha256",
    ):
        _require(
            record.get(key) == expected[key],
            f"V8 readiness identity drift: {key}",
        )


def validate_evidence_shape(record: Mapping[str, Any]) -> dict[str, Any]:
    """Validate exact evidence values without admitting collector authority."""
    _require(isinstance(record, Mapping), "activation evidence must be object")
    snapshot_id = record.get("snapshot_id")
    _require(
        snapshot_id in {V14, V10, V2R13, V8},
        "activation evidence snapshot is not reviewed",
    )
    requirement = evidence_requirement(str(snapshot_id))
    _require_exact_fields(record, requirement["required_fields"])
    _validate_common(record, requirement)

    if snapshot_id in {V14, V10}:
        _validate_external_loopback(record, requirement)
    elif snapshot_id == V2R13:
        _validate_v2r13(record, requirement)
    elif snapshot_id == V8:
        _validate_v8(record, requirement)
    else:
        raise RuntimeActivationEvidenceHold("unreachable evidence runtime")

    return {
        "schema": ADMISSION_SCHEMA,
        "snapshot_id": snapshot_id,
        "evidence_shape_valid": True,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "holds": list(requirement["unresolved_collector_blockers"]),
    }


def admit_evidence(
    record: Mapping[str, Any],
    *,
    reviewed_collector_contract_sha256: str | None = None,
) -> dict[str, Any]:
    """Fail closed until a separately reviewed collector binding is supplied."""
    shape = validate_evidence_shape(record)
    requirement = evidence_requirement(str(record["snapshot_id"]))

    if reviewed_collector_contract_sha256 is None:
        return shape

    _require(
        REVIEWED_COLLECTOR_BINDING_PRESENT is True,
        "no canonical reviewed collector binding is present",
    )
    _require(
        _is_sha256(reviewed_collector_contract_sha256),
        "reviewed collector SHA malformed",
    )
    _require(
        record["collector_contract_sha256"] == reviewed_collector_contract_sha256,
        "collector contract SHA mismatch",
    )

    # This branch is deliberately unreachable in v1 until a future source
    # revision pins a reviewed collector contract.
    return {
        "schema": ADMISSION_SCHEMA,
        "snapshot_id": record["snapshot_id"],
        "evidence_shape_valid": True,
        "collector_identity_admitted": True,
        "runtime_readiness_admitted": True,
        "runtime_execution_authorized": False,
        "holds": [RUNTIME_AUTHORITY_BLOCKER],
        "requirement": deepcopy(requirement),
    }


def arm_evidence_requirement(*, pair_slot: int, arm: str) -> dict[str, Any]:
    """Bind one canonical arm to the exact readiness-evidence requirement."""
    plan = arm_runtime_activation_plan(pair_slot=pair_slot, arm=arm)
    requirement = evidence_requirement(plan["opponent_snapshot_id"])
    return {
        "pair_slot": pair_slot,
        "arm": arm,
        "execution_index": plan["execution_index"],
        "held_out": plan["held_out"],
        "opponent_snapshot_id": plan["opponent_snapshot_id"],
        "requirement": requirement,
        "evidence_collected": False,
        "evidence_admitted": False,
        "runtime_selection_performed": False,
        "runtime_started": False,
        "runtime_execution_authorized": False,
    }


def collect_activation_evidence(*args: Any, **kwargs: Any) -> None:
    """Always hold: evidence collection is deliberately not implemented."""
    raise RuntimeActivationEvidenceHold(
        "ACTIVATION_EVIDENCE_COLLECTOR_NOT_IMPLEMENTED: "
        "Generation-2 evidence contract is read-only schema/admission logic only"
    )
