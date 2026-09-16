"""Dormant V2R13 worktree observer for Abaddon Generation-2.

This module closes the six V2R13 path-classification leaves without inventing
facts from the existing Git observer.

The observer requires explicit caller-supplied backends:

* ``lstat_path`` classifies the exact final path component without following it;
* ``run_git`` is passed to the already-reviewed V2R13 Git observer;
* ``resolve_path`` is passed to that same reviewed observer.

Observation is fail-closed and requires ``observation_authorized=True``.
The exact directory generation is sampled before and after the reviewed Git
observation and must remain stable.  The returned nested worktree objects match
the activation-evidence field sets exactly.

This module deliberately provides NO real host backend and performs no I/O on
import.  It never selects ``os.lstat``, ``host_git_runner``, or
``host_path_resolver`` automatically.

No worktree creation, checkout mutation, endpoint/systemd probe, model load,
runtime/game/model execution, training, promotion, deployment, VOID-chain
mutation, or funds action is authorized.
"""

from __future__ import annotations

import stat
from copy import deepcopy
from typing import Any, Mapping, Protocol

from openra_env.learning import (
    abaddon_policy_campaign_runtime_activation_evidence_generation2
    as activation_evidence,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_observers_generation2
    as runtime_observers,
)
from openra_env.learning.abaddon_policy_campaign_runtime_path_inputs_generation2 import (
    V2R13,
    validate_explicit_path_inputs,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-worktree-observer-contract.v1"
)
OBSERVATION_SCHEMA = (
    "void.abaddon.generation2.v2r13-worktree-observation.v1"
)

RUNTIME_OBSERVERS_GIT_BLOB = "cc4774e6aa934764c189cebd4040cd8ea4870517"
PATH_INPUTS_GIT_BLOB = "f65735c7820da9da0205388f1933b6aa9d6dd737"
ACTIVATION_EVIDENCE_GIT_BLOB = "aac7964d9e80633535003b9f27066cac1bb4bac2"

STAT_IDENTITY_FIELDS = (
    "st_dev",
    "st_ino",
    "st_mode",
    "st_nlink",
    "st_size",
    "st_mtime_ns",
    "st_ctime_ns",
)


class RuntimeV2R13WorktreeObserverHold(ValueError):
    pass


class PathLstat(Protocol):
    def __call__(self, path: str) -> Any:
        ...


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13WorktreeObserverHold(message)


def _require_authority(observation_authorized: bool) -> None:
    _require(
        observation_authorized is True,
        "GENERATION2_V2R13_WORKTREE_OBSERVATION_NOT_AUTHORIZED",
    )


def _stat_identity(value: Any, label: str) -> tuple[int, ...]:
    result: list[int] = []
    for field in STAT_IDENTITY_FIELDS:
        item = getattr(value, field, None)
        _require(
            type(item) is int,
            f"{label}: malformed lstat field {field}",
        )
        result.append(item)
    return tuple(result)


def _classify_directory(
    path: str,
    *,
    label: str,
    lstat_path: PathLstat,
) -> tuple[dict[str, Any], tuple[int, ...]]:
    _require(callable(lstat_path), f"{label}: lstat backend required")
    try:
        observed = lstat_path(path)
    except OSError as error:
        raise RuntimeV2R13WorktreeObserverHold(
            f"{label}: path observation failed:{type(error).__name__}"
        ) from error

    identity = _stat_identity(observed, label)
    mode = identity[STAT_IDENTITY_FIELDS.index("st_mode")]
    is_symlink = stat.S_ISLNK(mode)
    is_directory = stat.S_ISDIR(mode)

    _require(not is_symlink, f"{label}: path is symlink")
    _require(is_directory, f"{label}: path is not directory")

    return (
        {
            "path": path,
            "exists": True,
            "is_directory": True,
            "is_symlink": False,
        },
        identity,
    )


def _validate_git_receipt(
    receipt: Mapping[str, Any],
    *,
    source_path: str,
    engine_path: str,
) -> None:
    _require(isinstance(receipt, Mapping), "V2R13 Git receipt missing")
    _require(
        receipt.get("schema") == runtime_observers.V2R13_OBSERVATION_SCHEMA,
        "V2R13 Git receipt schema drift",
    )
    _require(receipt.get("snapshot_id") == V2R13, "V2R13 Git receipt snapshot drift")
    _require(
        receipt.get("source_root") == source_path,
        "V2R13 Git receipt source path drift",
    )
    _require(
        receipt.get("engine_root") == engine_path,
        "V2R13 Git receipt engine path drift",
    )
    _require(
        receipt.get("source_worktree_clean") is True,
        "V2R13 Git receipt source not clean",
    )
    _require(
        receipt.get("source_detached_head") is True,
        "V2R13 Git receipt source not detached",
    )
    _require(
        receipt.get("engine_worktree_clean") is True,
        "V2R13 Git receipt engine not clean",
    )
    _require(
        receipt.get("worktree_created") is False,
        "V2R13 Git receipt created worktree",
    )
    _require(
        receipt.get("checkout_mutation_performed") is False,
        "V2R13 Git receipt mutated checkout",
    )
    for field in (
        "runtime_execution_performed",
        "model_execution_performed",
        "game_execution_performed",
    ):
        _require(
            receipt.get(field) is False,
            f"V2R13 Git receipt crossed authority boundary: {field}",
        )


def _compose_worktree_objects(
    source_classification: Mapping[str, Any],
    engine_classification: Mapping[str, Any],
    git_receipt: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    requirement = activation_evidence.evidence_requirement(V2R13)

    source = {
        **deepcopy(dict(source_classification)),
        "clean": git_receipt["source_worktree_clean"],
        "detached": git_receipt["source_detached_head"],
        "head_commit": git_receipt["source_head_commit"],
        "tree_sha": git_receipt["source_head_tree"],
    }
    engine = {
        **deepcopy(dict(engine_classification)),
        "clean": git_receipt["engine_worktree_clean"],
        "head_commit": git_receipt["engine_head_commit"],
    }

    _require(
        set(source) == set(requirement["frozen_source_worktree_fields"]),
        "V2R13 source worktree evidence field-set drift",
    )
    _require(
        set(engine) == set(requirement["engine_worktree_fields"]),
        "V2R13 engine worktree evidence field-set drift",
    )
    return source, engine


def observe_v2r13_worktrees(
    record: Mapping[str, Any],
    *,
    observation_authorized: bool,
    lstat_path: PathLstat,
    run_git: runtime_observers.GitRunner,
    resolve_path: runtime_observers.PathResolver,
) -> dict[str, Any]:
    """Observe exact V2R13 worktree classification + reviewed Git identity."""
    _require_authority(observation_authorized)
    _require(callable(lstat_path), "V2R13 lstat backend required")
    _require(callable(run_git), "V2R13 Git runner required")
    _require(callable(resolve_path), "V2R13 path resolver required")

    validated = validate_explicit_path_inputs(V2R13, record)
    paths = validated["paths"]
    source_path = paths["frozen_source_root"]
    engine_path = paths["exact_engine_root"]

    source_before, source_identity_before = _classify_directory(
        source_path,
        label="V2R13_SOURCE_WORKTREE",
        lstat_path=lstat_path,
    )
    engine_before, engine_identity_before = _classify_directory(
        engine_path,
        label="V2R13_ENGINE_WORKTREE",
        lstat_path=lstat_path,
    )

    git_receipt = runtime_observers.observe_v2r13_git_identity(
        record,
        observation_authorized=True,
        run_git=run_git,
        resolve_path=resolve_path,
    )
    _validate_git_receipt(
        git_receipt,
        source_path=source_path,
        engine_path=engine_path,
    )

    source_after, source_identity_after = _classify_directory(
        source_path,
        label="V2R13_SOURCE_WORKTREE",
        lstat_path=lstat_path,
    )
    engine_after, engine_identity_after = _classify_directory(
        engine_path,
        label="V2R13_ENGINE_WORKTREE",
        lstat_path=lstat_path,
    )

    _require(
        source_identity_before == source_identity_after,
        "V2R13_SOURCE_WORKTREE_GENERATION_CHANGED",
    )
    _require(
        engine_identity_before == engine_identity_after,
        "V2R13_ENGINE_WORKTREE_GENERATION_CHANGED",
    )
    _require(
        source_before == source_after,
        "V2R13 source classification changed",
    )
    _require(
        engine_before == engine_after,
        "V2R13 engine classification changed",
    )

    source_worktree, engine_worktree = _compose_worktree_objects(
        source_before,
        engine_before,
        git_receipt,
    )

    return {
        "schema": OBSERVATION_SCHEMA,
        "snapshot_id": V2R13,
        "frozen_source_worktree": source_worktree,
        "engine_worktree": engine_worktree,
        "source_path_generation_stable": True,
        "engine_path_generation_stable": True,
        "git_observation_schema": runtime_observers.V2R13_OBSERVATION_SCHEMA,
        "observation_mode": "read_only",
        "filesystem_observation_performed": True,
        "git_query_performed": True,
        "worktree_created": False,
        "checkout_mutation_performed": False,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_execution_performed": False,
    }


def validate_v2r13_worktree_observation(
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate a supplied composite receipt without performing observation."""
    _require(isinstance(receipt, Mapping), "V2R13 worktree observation missing")
    expected_fields = {
        "schema",
        "snapshot_id",
        "frozen_source_worktree",
        "engine_worktree",
        "source_path_generation_stable",
        "engine_path_generation_stable",
        "git_observation_schema",
        "observation_mode",
        "filesystem_observation_performed",
        "git_query_performed",
        "worktree_created",
        "checkout_mutation_performed",
        "runtime_execution_performed",
        "model_execution_performed",
        "game_execution_performed",
    }
    _require(
        set(receipt) == expected_fields,
        "V2R13 worktree observation field-set drift",
    )
    _require(receipt.get("schema") == OBSERVATION_SCHEMA, "V2R13 receipt schema drift")
    _require(receipt.get("snapshot_id") == V2R13, "V2R13 receipt snapshot drift")
    _require(
        receipt.get("git_observation_schema")
        == runtime_observers.V2R13_OBSERVATION_SCHEMA,
        "V2R13 embedded Git schema drift",
    )
    _require(receipt.get("observation_mode") == "read_only", "V2R13 mode drift")
    _require(
        receipt.get("source_path_generation_stable") is True,
        "V2R13 source generation not stable",
    )
    _require(
        receipt.get("engine_path_generation_stable") is True,
        "V2R13 engine generation not stable",
    )
    _require(
        receipt.get("filesystem_observation_performed") is True,
        "V2R13 filesystem observation claim missing",
    )
    _require(
        receipt.get("git_query_performed") is True,
        "V2R13 Git query claim missing",
    )
    for field in (
        "worktree_created",
        "checkout_mutation_performed",
        "runtime_execution_performed",
        "model_execution_performed",
        "game_execution_performed",
    ):
        _require(
            receipt.get(field) is False,
            f"V2R13 worktree receipt crossed boundary: {field}",
        )

    requirement = activation_evidence.evidence_requirement(V2R13)
    source = receipt.get("frozen_source_worktree")
    engine = receipt.get("engine_worktree")
    _require(isinstance(source, Mapping), "V2R13 source worktree object missing")
    _require(isinstance(engine, Mapping), "V2R13 engine worktree object missing")
    _require(
        set(source) == set(requirement["frozen_source_worktree_fields"]),
        "V2R13 source worktree field-set drift",
    )
    _require(
        set(engine) == set(requirement["engine_worktree_fields"]),
        "V2R13 engine worktree field-set drift",
    )

    for key in ("exists", "is_directory", "clean", "detached"):
        _require(source.get(key) is True, f"V2R13 source lacks {key}")
    _require(source.get("is_symlink") is False, "V2R13 source is symlink")
    for key in ("exists", "is_directory", "clean"):
        _require(engine.get(key) is True, f"V2R13 engine lacks {key}")
    _require(engine.get("is_symlink") is False, "V2R13 engine is symlink")

    expected = requirement["expected"]
    _require(
        source.get("head_commit") == expected["frozen_war_college_commit"],
        "V2R13 source commit drift",
    )
    _require(
        source.get("tree_sha") == expected["frozen_war_college_tree"],
        "V2R13 source tree drift",
    )
    _require(
        engine.get("head_commit") == expected["frozen_engine_commit"],
        "V2R13 engine commit drift",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "receipt_valid": True,
        "path_classification_complete": True,
        "git_identity_complete": True,
        "activation_worktree_shape_complete": True,
        "canonical_provider_binding_present": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
    }


def v2r13_worktree_observer_contract() -> dict[str, Any]:
    return {
        "schema": CONTRACT_SCHEMA,
        "runtime_observers_git_blob": RUNTIME_OBSERVERS_GIT_BLOB,
        "path_inputs_git_blob": PATH_INPUTS_GIT_BLOB,
        "activation_evidence_git_blob": ACTIVATION_EVIDENCE_GIT_BLOB,
        "path_lstat_backend_required": True,
        "git_runner_required": True,
        "path_resolver_required": True,
        "real_host_backend_implemented": False,
        "automatic_host_backend_selection": False,
        "observation_requires_explicit_authority": True,
        "path_generation_stability_check_implemented": True,
        "reviewed_git_observer_composition_implemented": True,
        "six_path_classification_leaves_implemented": True,
        "activation_worktree_shape_composition_implemented": True,
        "observation_performed": False,
        "canonical_provider_binding_present": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
    }


def observe_with_host_backend(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13WorktreeObserverHold(
        "GENERATION2_V2R13_HOST_PATH_BACKEND_NOT_IMPLEMENTED"
    )
