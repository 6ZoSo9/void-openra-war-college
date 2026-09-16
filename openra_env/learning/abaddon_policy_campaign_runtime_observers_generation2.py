"""Read-only observer implementations for Abaddon Generation-2 runtime evidence.

This module implements two *dormant* observer surfaces:

1. Strong V8 asset observation:
   - explicit caller-supplied V8 model/adapter roots,
   - final component opened with O_NOFOLLOW,
   - regular-file requirement,
   - explicit per-file byte bound,
   - same descriptor used for read/hash,
   - fstat identity compared before/after,
   - exact reviewed SHA-256 required for all 17 assets,
   - no model load or inference.

2. Exact V2R13 Git observation:
   - explicit caller-supplied pre-existing source/engine roots,
   - strict resolved-path identity,
   - source HEAD commit + HEAD^{tree},
   - full source worktree cleanliness,
   - source detached HEAD,
   - exact engine HEAD commit,
   - full engine worktree cleanliness,
   - no worktree creation or checkout mutation.

Important: neither observer can run accidentally.  Public observation entry points
require `observation_authorized=True` *and* an explicitly supplied backend/runner.
The host backend factories are provided for a future reviewed collector, but this
module never selects or invokes them automatically.

No endpoint/systemd probe, pip freeze, model load, runtime start, game execution,
training, weight update, promotion, deployment, VOID-chain mutation, or funds
action is performed by importing or inspecting this module.
"""

from __future__ import annotations

import hashlib
import os
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Protocol

from openra_env.learning.apollyon_v2r13_portable_checkout import (
    FROZEN_ENGINE_COMMIT,
    FROZEN_WAR_COLLEGE_COMMIT,
    FROZEN_WAR_COLLEGE_TREE,
)
from openra_env.learning.apollyon_v8_campaign_runtime import (
    ADDED_TOKENS_SHA256,
    BASE_MODEL_CONFIG_SHA256,
    BASE_MODEL_INDEX_SHA256,
    BASE_MODEL_SHARD1_SHA256,
    BASE_MODEL_SHARD2_SHA256,
    CHAT_TEMPLATE_SHA256,
    MERGES_SHA256,
    PROCESSOR_CONFIG_SHA256,
    SPECIAL_TOKENS_MAP_SHA256,
    TOKENIZER_CONFIG_SHA256,
    TOKENIZER_JSON_SHA256,
    V8_ADAPTER_CONFIG_SHA256,
    V8_ADAPTER_SHA256,
    V8_ADAPTER_TOKENIZER_CONFIG_SHA256,
    VOCAB_SHA256,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_observation_primitive_review_generation2
    as primitive_review,
)
from openra_env.learning.abaddon_policy_campaign_runtime_path_inputs_generation2 import (
    V2R13,
    V8,
    validate_explicit_path_inputs,
)

CONTRACT_SCHEMA = "void.abaddon.generation2.runtime-observers.v1"
FILE_OBSERVATION_SCHEMA = "void.abaddon.generation2.strong-file-observation.v1"
V8_OBSERVATION_SCHEMA = "void.abaddon.generation2.v8-asset-observation.v1"
V2R13_OBSERVATION_SCHEMA = "void.abaddon.generation2.v2r13-git-observation.v1"

PRIMITIVE_REVIEW_SOURCE_SHA256 = (
    "c0123c2f06fc7a6fcb28449eaa9691afc3e128242ba577da291f15c23ba60086"
)

# Generous hard bounds that prevent unbounded reads while remaining above the
# expected size class of the frozen V8 4B model assets.
MAX_SMALL_ASSET_BYTES = 128 * 1024 * 1024
MAX_MODEL_SHARD_BYTES = 16 * 1024 * 1024 * 1024
MAX_ADAPTER_WEIGHT_BYTES = 8 * 1024 * 1024 * 1024

FILE_IDENTITY_FIELDS = (
    "st_dev",
    "st_ino",
    "st_size",
    "st_mtime_ns",
    "st_ctime_ns",
    "st_mode",
    "st_nlink",
)

COMMON_AUTHORITY = {
    "observation_authorized_by_contract": False,
    "runtime_execution_authorized": False,
    "model_execution_authorized": False,
    "game_execution_authorized": False,
    "worktree_creation_authorized": False,
    "checkout_mutation_authorized": False,
    "pip_freeze_authorized": False,
    "endpoint_probe_authorized": False,
    "systemd_query_authorized": False,
    "model_weights_load_authorized": False,
    "training_authorized": False,
    "weights_update_authorized": False,
    "automatic_policy_promotion_authorized": False,
}


class RuntimeObserverHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeObserverHold(message)


def _require_observation_authority(observation_authorized: bool) -> None:
    _require(
        observation_authorized is True,
        "GENERATION2_READ_ONLY_OBSERVATION_NOT_AUTHORIZED",
    )


def _require_sha256(value: Any, label: str) -> str:
    _require(type(value) is str and len(value) == 64, f"{label} must be SHA-256 hex")
    _require(
        all(char in "0123456789abcdef" for char in value),
        f"{label} must be lowercase SHA-256 hex",
    )
    return value


def _identity_from_stat(value: Any) -> tuple[int, int, int, int, int, int, int]:
    return tuple(int(getattr(value, field)) for field in FILE_IDENTITY_FIELDS)


@dataclass(frozen=True)
class FileObservationBackend:
    open_file: Callable[[str, int], int]
    fstat: Callable[[int], Any]
    read: Callable[[int, int], bytes]
    close: Callable[[int], None]


def host_file_observation_backend() -> FileObservationBackend:
    """Return the real host backend.  Merely constructing it performs no I/O."""
    return FileObservationBackend(
        open_file=lambda path, flags: os.open(path, flags),
        fstat=os.fstat,
        read=os.read,
        close=os.close,
    )


@dataclass(frozen=True)
class V8AssetSpec:
    root_field: str
    relative_path: str
    expected_sha256: str
    label: str
    maximum_bytes: int


V8_ASSET_SPECS = (
    V8AssetSpec(
        "model_dir",
        "config.json",
        BASE_MODEL_CONFIG_SHA256,
        "base config",
        MAX_SMALL_ASSET_BYTES,
    ),
    V8AssetSpec(
        "model_dir",
        "model.safetensors-00001-of-00002.safetensors",
        BASE_MODEL_SHARD1_SHA256,
        "base shard 1",
        MAX_MODEL_SHARD_BYTES,
    ),
    V8AssetSpec(
        "model_dir",
        "model.safetensors-00002-of-00002.safetensors",
        BASE_MODEL_SHARD2_SHA256,
        "base shard 2",
        MAX_MODEL_SHARD_BYTES,
    ),
    V8AssetSpec(
        "model_dir",
        "model.safetensors.index.json",
        BASE_MODEL_INDEX_SHA256,
        "base index",
        MAX_SMALL_ASSET_BYTES,
    ),
    V8AssetSpec(
        "model_dir",
        "chat_template.jinja",
        CHAT_TEMPLATE_SHA256,
        "base chat template",
        MAX_SMALL_ASSET_BYTES,
    ),
    V8AssetSpec(
        "model_dir",
        "tokenizer.json",
        TOKENIZER_JSON_SHA256,
        "base tokenizer",
        MAX_SMALL_ASSET_BYTES,
    ),
    V8AssetSpec(
        "model_dir",
        "tokenizer_config.json",
        TOKENIZER_CONFIG_SHA256,
        "base tokenizer config",
        MAX_SMALL_ASSET_BYTES,
    ),
    V8AssetSpec(
        "model_dir",
        "merges.txt",
        MERGES_SHA256,
        "base merges",
        MAX_SMALL_ASSET_BYTES,
    ),
    V8AssetSpec(
        "model_dir",
        "vocab.json",
        VOCAB_SHA256,
        "base vocab",
        MAX_SMALL_ASSET_BYTES,
    ),
    V8AssetSpec(
        "model_dir",
        "added_tokens.json",
        ADDED_TOKENS_SHA256,
        "base added tokens",
        MAX_SMALL_ASSET_BYTES,
    ),
    V8AssetSpec(
        "model_dir",
        "special_tokens_map.json",
        SPECIAL_TOKENS_MAP_SHA256,
        "base special tokens",
        MAX_SMALL_ASSET_BYTES,
    ),
    V8AssetSpec(
        "model_dir",
        "processor_config.json",
        PROCESSOR_CONFIG_SHA256,
        "base processor config",
        MAX_SMALL_ASSET_BYTES,
    ),
    V8AssetSpec(
        "adapter_dir",
        "adapter_config.json",
        V8_ADAPTER_CONFIG_SHA256,
        "V8 adapter config",
        MAX_SMALL_ASSET_BYTES,
    ),
    V8AssetSpec(
        "adapter_dir",
        "adapter_model.safetensors",
        V8_ADAPTER_SHA256,
        "V8 adapter weights",
        MAX_ADAPTER_WEIGHT_BYTES,
    ),
    V8AssetSpec(
        "adapter_dir",
        "chat_template.jinja",
        CHAT_TEMPLATE_SHA256,
        "V8 adapter chat template",
        MAX_SMALL_ASSET_BYTES,
    ),
    V8AssetSpec(
        "adapter_dir",
        "tokenizer.json",
        TOKENIZER_JSON_SHA256,
        "V8 adapter tokenizer",
        MAX_SMALL_ASSET_BYTES,
    ),
    V8AssetSpec(
        "adapter_dir",
        "tokenizer_config.json",
        V8_ADAPTER_TOKENIZER_CONFIG_SHA256,
        "V8 adapter tokenizer config",
        MAX_SMALL_ASSET_BYTES,
    ),
)


def runtime_observer_contract() -> dict[str, Any]:
    file_req = primitive_review.future_file_observer_requirements()
    git_req = primitive_review.future_v2r13_git_observer_requirements()
    return {
        "schema": CONTRACT_SCHEMA,
        "primitive_review_source_sha256": PRIMITIVE_REVIEW_SOURCE_SHA256,
        "strong_file_observer_implemented": True,
        "v8_asset_observer_implemented": True,
        "v2r13_git_observer_implemented": True,
        "v8_asset_count": len(V8_ASSET_SPECS),
        "strong_file_requirements": dict(file_req),
        "v2r13_git_requirements": dict(git_req),
        "automatic_host_backend_selection": False,
        "observation_requires_explicit_authority": True,
        "observation_performed": False,
        "runtime_execution_authorized": False,
        "model_execution_authorized": False,
        "game_execution_authorized": False,
        "worktree_creation_authorized": False,
        "checkout_mutation_authorized": False,
        "authority": dict(COMMON_AUTHORITY),
    }


def observe_exact_regular_file(
    path: str,
    *,
    expected_sha256: str,
    maximum_bytes: int,
    observation_authorized: bool,
    backend: FileObservationBackend,
) -> dict[str, Any]:
    """Read/hash one exact regular-file generation through one no-follow fd."""
    _require_observation_authority(observation_authorized)
    _require(type(path) is str and path.startswith("/"), "file path must be absolute")
    expected = _require_sha256(expected_sha256, "expected_sha256")
    _require(
        type(maximum_bytes) is int and maximum_bytes > 0,
        "maximum_bytes must be positive integer",
    )
    _require(isinstance(backend, FileObservationBackend), "file backend required")

    flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )
    try:
        fd = backend.open_file(path, flags)
    except OSError as error:
        raise RuntimeObserverHold(
            f"STRONG_FILE_OPEN_FAILED:{type(error).__name__}"
        ) from error

    try:
        before = backend.fstat(fd)
        _require(stat.S_ISREG(before.st_mode), "STRONG_FILE_NOT_REGULAR")
        _require(before.st_size >= 0, "STRONG_FILE_NEGATIVE_SIZE")
        _require(before.st_size <= maximum_bytes, "STRONG_FILE_EXCEEDS_BOUND")

        digest = hashlib.sha256()
        total = 0
        while True:
            remaining = maximum_bytes + 1 - total
            _require(remaining > 0, "STRONG_FILE_EXCEEDS_BOUND")
            chunk = backend.read(fd, min(1024 * 1024, remaining))
            _require(isinstance(chunk, bytes), "STRONG_FILE_READ_TYPE")
            if not chunk:
                break
            digest.update(chunk)
            total += len(chunk)
            _require(total <= maximum_bytes, "STRONG_FILE_EXCEEDS_BOUND")

        after = backend.fstat(fd)
        _require(
            _identity_from_stat(before) == _identity_from_stat(after),
            "STRONG_FILE_GENERATION_CHANGED",
        )
        _require(total == before.st_size, "STRONG_FILE_SIZE_CHANGED")
        actual = digest.hexdigest()
        _require(actual == expected, "STRONG_FILE_SHA256_DRIFT")

        return {
            "schema": FILE_OBSERVATION_SCHEMA,
            "path": path,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "byte_count": total,
            "maximum_bytes": maximum_bytes,
            "identity": {
                field: int(getattr(before, field))
                for field in FILE_IDENTITY_FIELDS
            },
            "generation_stable": True,
            "regular_file": True,
            "symlink_followed": False,
            "runtime_execution_performed": False,
            "model_execution_performed": False,
        }
    finally:
        backend.close(fd)


def observe_v8_assets(
    record: Mapping[str, Any],
    *,
    observation_authorized: bool,
    backend: FileObservationBackend,
) -> dict[str, Any]:
    """Observe all 17 reviewed V8 assets without loading model weights."""
    _require_observation_authority(observation_authorized)
    validated = validate_explicit_path_inputs(V8, record)
    paths = validated["paths"]

    observations = []
    for spec in V8_ASSET_SPECS:
        root = paths[spec.root_field]
        path = f"{root}/{spec.relative_path}"
        observations.append(
            {
                "label": spec.label,
                "root_field": spec.root_field,
                "relative_path": spec.relative_path,
                "observation": observe_exact_regular_file(
                    path,
                    expected_sha256=spec.expected_sha256,
                    maximum_bytes=spec.maximum_bytes,
                    observation_authorized=True,
                    backend=backend,
                ),
            }
        )

    _require(len(observations) == 17, "V8_ASSET_OBSERVATION_COUNT_DRIFT")
    return {
        "schema": V8_OBSERVATION_SCHEMA,
        "snapshot_id": V8,
        "asset_count": len(observations),
        "assets": observations,
        "all_assets_verified": True,
        "model_weights_loaded": False,
        "runtime_started": False,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_execution_performed": False,
    }


@dataclass(frozen=True)
class GitCommandResult:
    returncode: int
    stdout: str
    stderr: str = ""


class GitRunner(Protocol):
    def __call__(self, repo: str, *args: str) -> GitCommandResult:
        ...


class PathResolver(Protocol):
    def __call__(self, path: str) -> str:
        ...


def host_path_resolver(path: str) -> str:
    """Resolve one existing path.  This function is never called automatically."""
    return str(Path(path).resolve(strict=True))


def host_git_runner(repo: str, *args: str) -> GitCommandResult:
    """Run one read-only Git command.  This function is never called automatically."""
    completed = subprocess.run(
        ["/usr/bin/git", "-C", repo, *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env={
            "HOME": str(Path.home()),
            "LANG": "C",
            "LC_ALL": "C",
            "PATH": "/usr/bin:/bin",
        },
    )
    return GitCommandResult(
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def _git_scalar(
    repo: str,
    args: tuple[str, ...],
    *,
    run_git: GitRunner,
    label: str,
    allow_nonzero: bool = False,
) -> GitCommandResult:
    result = run_git(repo, *args)
    _require(isinstance(result, GitCommandResult), f"{label}: invalid Git result")
    if not allow_nonzero:
        _require(result.returncode == 0, f"{label}: Git command failed")
    return result


def observe_v2r13_git_identity(
    record: Mapping[str, Any],
    *,
    observation_authorized: bool,
    run_git: GitRunner,
    resolve_path: PathResolver,
) -> dict[str, Any]:
    """Observe exact V2R13 pre-existing source/engine Git identity read-only."""
    _require_observation_authority(observation_authorized)
    validated = validate_explicit_path_inputs(V2R13, record)
    paths = validated["paths"]
    source = paths["frozen_source_root"]
    engine = paths["exact_engine_root"]

    _require(resolve_path(source) == source, "V2R13_SOURCE_PATH_IDENTITY")
    _require(resolve_path(engine) == engine, "V2R13_ENGINE_PATH_IDENTITY")

    source_head = _git_scalar(
        source,
        ("rev-parse", "HEAD"),
        run_git=run_git,
        label="V2R13_SOURCE_HEAD",
    ).stdout.strip()
    source_tree = _git_scalar(
        source,
        ("rev-parse", "HEAD^{tree}"),
        run_git=run_git,
        label="V2R13_SOURCE_TREE",
    ).stdout.strip()
    source_status = _git_scalar(
        source,
        ("status", "--porcelain", "--untracked-files=all"),
        run_git=run_git,
        label="V2R13_SOURCE_STATUS",
    ).stdout
    source_symbolic = _git_scalar(
        source,
        ("symbolic-ref", "-q", "HEAD"),
        run_git=run_git,
        label="V2R13_SOURCE_SYMBOLIC_REF",
        allow_nonzero=True,
    )

    _require(source_head == FROZEN_WAR_COLLEGE_COMMIT, "V2R13_SOURCE_HEAD_DRIFT")
    _require(source_tree == FROZEN_WAR_COLLEGE_TREE, "V2R13_SOURCE_TREE_DRIFT")
    _require(source_status.strip() == "", "V2R13_SOURCE_WORKTREE_DIRTY")
    _require(
        source_symbolic.returncode == 1 and source_symbolic.stdout.strip() == "",
        "V2R13_SOURCE_NOT_DETACHED",
    )

    engine_head = _git_scalar(
        engine,
        ("rev-parse", "HEAD"),
        run_git=run_git,
        label="V2R13_ENGINE_HEAD",
    ).stdout.strip()
    engine_status = _git_scalar(
        engine,
        ("status", "--porcelain", "--untracked-files=all"),
        run_git=run_git,
        label="V2R13_ENGINE_STATUS",
    ).stdout

    _require(engine_head == FROZEN_ENGINE_COMMIT, "V2R13_ENGINE_HEAD_DRIFT")
    _require(engine_status.strip() == "", "V2R13_ENGINE_WORKTREE_DIRTY")

    return {
        "schema": V2R13_OBSERVATION_SCHEMA,
        "snapshot_id": V2R13,
        "source_root": source,
        "engine_root": engine,
        "source_head_commit": source_head,
        "source_head_tree": source_tree,
        "source_worktree_clean": True,
        "source_detached_head": True,
        "engine_head_commit": engine_head,
        "engine_worktree_clean": True,
        "worktree_created": False,
        "checkout_mutation_performed": False,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_execution_performed": False,
    }
