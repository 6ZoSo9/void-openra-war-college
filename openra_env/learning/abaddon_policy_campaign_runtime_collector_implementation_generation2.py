"""Dormant, source-only Generation-2 collector implementation scaffold.

This module implements deterministic collector orchestration over explicitly
supplied, source-bound read-only primitive providers.  It does not supply a
canonical host provider and it never selects one automatically.

Two entry points are intentionally separate:

* collect_candidate_with_provider():
  test/review surface requiring explicit collection_authorized=True plus an
  exact per-primitive reviewed source-binding map;
* collect_activation_evidence():
  canonical collection surface, which always hard-holds until a future source
  revision pins reviewed primitive-provider implementations.

The resulting candidate can satisfy the activation-evidence *shape* validator,
but this module never admits collector identity or runtime readiness.  The
canonical activation-evidence binding remains disabled.

No filesystem access, Git command, subprocess, environment read, pip freeze,
endpoint/systemd probe, host-backend selection, model load, worktree creation,
runtime/game/model execution, training, weight update, promotion, deployment,
VOID-chain mutation, or funds action occurs merely by importing this module.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Protocol

from openra_env.learning import (
    abaddon_policy_campaign_runtime_activation_evidence_generation2
    as activation_evidence,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_collector_contract_generation2
    as collector_contract,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    RUNTIME_AUTHORITY_BLOCKER,
    V10,
    V14,
    V2R13,
    V8,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.runtime-collector-implementation-contract.v1"
)
PRIMITIVE_RECEIPT_SCHEMA = (
    "void.abaddon.generation2.runtime-collector-primitive-receipt.v1"
)
CANDIDATE_SCHEMA = (
    "void.abaddon.generation2.runtime-collector-candidate.v1"
)

COLLECTOR_CONTRACT_SOURCE_SHA256 = (
    "c48ad0871d4ea25e45efcde36e59622d1bb6b2a2fc4a4ed1f25988b543c2038f"
)
COLLECTOR_CONTRACT_GIT_BLOB = "8014431ad5329137e5ce12334d19d37c877a0b52"
COLLECTOR_SEMANTIC_SHA256 = (
    "d11e45cabc10b42e09ab5e328e1e63721b633c7cdcfd7492038ec286b7f3e657"
)
ACTIVATION_EVIDENCE_GIT_BLOB = "aac7964d9e80633535003b9f27066cac1bb4bac2"

CANONICAL_PRIMITIVE_SOURCE_BINDINGS_PRESENT = False
CANONICAL_COLLECTION_ENABLED = False

SHA256_HEX = frozenset("0123456789abcdef")


class RuntimeCollectorImplementationHold(ValueError):
    pass


class PrimitiveProvider(Protocol):
    def __call__(
        self,
        snapshot_id: str,
        primitive_name: str,
    ) -> Mapping[str, Any]:
        ...


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeCollectorImplementationHold(message)


def _is_sha256(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(char in SHA256_HEX for char in value)
    )


def _collector_manifest() -> Mapping[str, Any]:
    validated = collector_contract.validate_collector_contract()
    _require(
        validated.get("collector_contract_sha256") == COLLECTOR_SEMANTIC_SHA256,
        "collector semantic SHA drift",
    )
    manifest = validated.get("manifest")
    _require(isinstance(manifest, Mapping), "collector manifest missing")
    return manifest


def collector_owned_evidence_fields(
    snapshot_id: str,
    *,
    supplied_environment_identity: bool = True,
) -> tuple[str, ...]:
    """Return exact evidence leaves owned by the future collector."""
    manifest = _collector_manifest()
    rows = manifest["snapshot_contracts"]
    _require(
        snapshot_id in {V14, V10, V2R13, V8},
        f"unsupported collector snapshot: {snapshot_id!r}",
    )
    row = rows[snapshot_id]

    if snapshot_id == V8:
        key = (
            "collector_owned_evidence_fields_with_supplied_environment"
            if supplied_environment_identity
            else "collector_owned_evidence_fields_without_supplied_environment"
        )
        fields = row[key]
    else:
        fields = row["collector_owned_evidence_fields"]

    _require(isinstance(fields, list), "collector-owned field list malformed")
    _require(
        all(isinstance(value, str) and value for value in fields),
        "collector-owned field must be non-empty string",
    )
    _require(
        len(fields) == len(set(fields)),
        "collector-owned evidence fields contain duplicates",
    )
    return tuple(fields)


def required_primitive_names(
    snapshot_id: str,
    *,
    supplied_environment_identity: bool = True,
) -> tuple[str, ...]:
    """Return primitive names excluding the collector's own semantic identity."""
    fields = collector_owned_evidence_fields(
        snapshot_id,
        supplied_environment_identity=supplied_environment_identity,
    )
    return tuple(
        field
        for field in fields
        if field != "collector_contract_sha256"
    )


def _require_primitive_bindings(
    names: tuple[str, ...],
    bindings: Mapping[str, Any],
) -> dict[str, str]:
    _require(
        isinstance(bindings, Mapping),
        "reviewed primitive source bindings must be object",
    )
    _require(
        set(bindings) == set(names),
        "reviewed primitive source binding set drift",
    )
    result: dict[str, str] = {}
    for name in names:
        value = bindings[name]
        _require(
            _is_sha256(value),
            f"primitive source binding SHA malformed: {name}",
        )
        result[name] = value
    return result


def _validate_primitive_receipt(
    receipt: Mapping[str, Any],
    *,
    snapshot_id: str,
    primitive_name: str,
    expected_source_sha256: str,
) -> Any:
    _require(isinstance(receipt, Mapping), "primitive receipt must be object")
    _require(
        set(receipt)
        == {
            "schema",
            "snapshot_id",
            "primitive_name",
            "source_sha256",
            "observation_mode",
            "value",
            "mutation_performed",
            "service_action_performed",
            "runtime_start_performed",
            "game_execution_performed",
            "model_inference_performed",
        },
        f"primitive receipt field-set drift: {primitive_name}",
    )
    _require(
        receipt.get("schema") == PRIMITIVE_RECEIPT_SCHEMA,
        f"primitive receipt schema drift: {primitive_name}",
    )
    _require(
        receipt.get("snapshot_id") == snapshot_id,
        f"primitive receipt snapshot drift: {primitive_name}",
    )
    _require(
        receipt.get("primitive_name") == primitive_name,
        f"primitive receipt name drift: {primitive_name}",
    )
    _require(
        receipt.get("source_sha256") == expected_source_sha256,
        f"primitive source binding mismatch: {primitive_name}",
    )
    _require(
        receipt.get("observation_mode") == "read_only",
        f"primitive observation mode drift: {primitive_name}",
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
            f"primitive crossed authority boundary: {primitive_name}:{field}",
        )
    return deepcopy(receipt.get("value"))


def _set_leaf(target: dict[str, Any], leaf: str, value: Any) -> None:
    if "." not in leaf:
        _require(
            leaf not in target or target[leaf] == value,
            f"collector candidate field conflict: {leaf}",
        )
        target[leaf] = deepcopy(value)
        return

    parent, child = leaf.split(".", 1)
    _require(
        parent in {"frozen_source_worktree", "engine_worktree"},
        f"unsupported nested collector leaf: {leaf}",
    )
    current = target.get(parent)
    if current is None:
        current = {}
        target[parent] = current
    _require(
        isinstance(current, dict),
        f"nested collector field must be object: {parent}",
    )
    _require(
        child not in current or current[child] == value,
        f"collector candidate nested-field conflict: {leaf}",
    )
    current[child] = deepcopy(value)


def _validate_base_fields(
    snapshot_id: str,
    base_evidence_fields: Mapping[str, Any],
) -> dict[str, Any]:
    _require(
        isinstance(base_evidence_fields, Mapping),
        "base evidence fields must be object",
    )
    requirement = activation_evidence.evidence_requirement(snapshot_id)
    allowed = set(requirement["required_fields"])
    extra = set(base_evidence_fields) - allowed
    _require(
        not extra,
        f"base evidence contains non-required fields: {sorted(extra)!r}",
    )
    return deepcopy(dict(base_evidence_fields))


def collect_candidate_with_provider(
    snapshot_id: str,
    base_evidence_fields: Mapping[str, Any],
    *,
    primitive_provider: PrimitiveProvider,
    reviewed_primitive_source_bindings: Mapping[str, Any],
    collection_authorized: bool,
    supplied_environment_identity: bool = True,
) -> dict[str, Any]:
    """Collect one candidate using only explicitly bound injected primitives."""
    _require(
        collection_authorized is True,
        "GENERATION2_COLLECTOR_CANDIDATE_COLLECTION_NOT_AUTHORIZED",
    )
    _require(
        callable(primitive_provider),
        "collector primitive provider must be callable",
    )
    _require(
        snapshot_id in {V14, V10, V2R13, V8},
        f"unsupported collector snapshot: {snapshot_id!r}",
    )

    candidate = _validate_base_fields(snapshot_id, base_evidence_fields)
    candidate["collector_contract_sha256"] = COLLECTOR_SEMANTIC_SHA256

    primitive_names = required_primitive_names(
        snapshot_id,
        supplied_environment_identity=supplied_environment_identity,
    )
    bindings = _require_primitive_bindings(
        primitive_names,
        reviewed_primitive_source_bindings,
    )

    primitive_receipts: list[dict[str, Any]] = []
    for primitive_name in primitive_names:
        raw = primitive_provider(snapshot_id, primitive_name)
        value = _validate_primitive_receipt(
            raw,
            snapshot_id=snapshot_id,
            primitive_name=primitive_name,
            expected_source_sha256=bindings[primitive_name],
        )
        _set_leaf(candidate, primitive_name, value)
        primitive_receipts.append(deepcopy(dict(raw)))

    requirement = activation_evidence.evidence_requirement(snapshot_id)
    required_fields = set(requirement["required_fields"])
    _require(
        set(candidate) == required_fields,
        "collector candidate evidence field set remains incomplete",
    )

    shape = activation_evidence.validate_evidence_shape(candidate)
    _require(
        shape.get("evidence_shape_valid") is True,
        "collector candidate failed activation-evidence shape validation",
    )
    _require(
        shape.get("collector_identity_admitted") is False,
        "collector candidate unexpectedly admitted collector identity",
    )
    _require(
        shape.get("runtime_readiness_admitted") is False,
        "collector candidate unexpectedly admitted runtime readiness",
    )
    _require(
        shape.get("runtime_execution_authorized") is False,
        "collector candidate unexpectedly gained runtime authority",
    )

    return {
        "schema": CANDIDATE_SCHEMA,
        "snapshot_id": snapshot_id,
        "collector_contract_sha256": COLLECTOR_SEMANTIC_SHA256,
        "primitive_receipt_count": len(primitive_receipts),
        "primitive_receipts": primitive_receipts,
        "activation_evidence_candidate": candidate,
        "activation_evidence_shape_valid": True,
        "collector_implementation_source_binding_admitted": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "canonical_collection_path": False,
        "live_host_backend_selected_automatically": False,
        "runtime_execution_authorized": False,
        "holds": [
            "CANONICAL_PRIMITIVE_SOURCE_BINDINGS_NOT_PRESENT",
            "COLLECTOR_IMPLEMENTATION_SOURCE_NOT_PINNED_BY_ACTIVATION_CONTRACT",
            "ACTIVATION_EVIDENCE_COLLECTOR_IDENTITY_NOT_ADMITTED",
            RUNTIME_AUTHORITY_BLOCKER,
        ],
    }


def collector_implementation_contract() -> dict[str, Any]:
    """Return the exact dormant implementation boundary."""
    collector_contract.validate_collector_contract()
    _require(
        activation_evidence.REVIEWED_COLLECTOR_BINDING_PRESENT is False,
        "activation-evidence collector binding unexpectedly active",
    )
    return {
        "schema": CONTRACT_SCHEMA,
        "collector_contract_source_sha256": COLLECTOR_CONTRACT_SOURCE_SHA256,
        "collector_contract_git_blob": COLLECTOR_CONTRACT_GIT_BLOB,
        "collector_semantic_sha256": COLLECTOR_SEMANTIC_SHA256,
        "activation_evidence_git_blob": ACTIVATION_EVIDENCE_GIT_BLOB,
        "supported_snapshot_ids": (V14, V10, V2R13, V8),
        "injected_primitive_orchestration_implemented": True,
        "primitive_receipt_source_binding_enforced": True,
        "primitive_receipt_read_only_boundary_enforced": True,
        "candidate_shape_validation_implemented": True,
        "automatic_host_backend_selection": False,
        "canonical_primitive_source_bindings_present": False,
        "canonical_collection_enabled": False,
        "collector_implementation_source_pinned_by_activation_contract": False,
        "reviewed_collector_binding_present": False,
        "collector_identity_admission_implemented": False,
        "runtime_readiness_admission_implemented": False,
        "live_observation_performed": False,
        "collector_executed_on_host": False,
        "runtime_execution_authorized": False,
    }


def collect_activation_evidence(*args: Any, **kwargs: Any) -> None:
    """Always hold until canonical primitive implementations are pinned."""
    _require(
        CANONICAL_PRIMITIVE_SOURCE_BINDINGS_PRESENT is True,
        "GENERATION2_CANONICAL_PRIMITIVE_SOURCE_BINDINGS_NOT_PRESENT",
    )
    _require(
        CANONICAL_COLLECTION_ENABLED is True,
        "GENERATION2_CANONICAL_COLLECTION_NOT_ENABLED",
    )
    raise RuntimeCollectorImplementationHold(
        "GENERATION2_CANONICAL_COLLECTOR_ENTRYPOINT_NOT_IMPLEMENTED"
    )
