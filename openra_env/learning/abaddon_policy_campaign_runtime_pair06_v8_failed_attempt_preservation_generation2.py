"""Evidence-preserving archival gate for the consumed pair-06 V8 baseline attempt.

This module never retries runtime. It validates the exact consumed attempt,
removes only the two exact clean detached Git worktrees with non-force
`git worktree remove`, then atomically renames the remaining failed baseline
tree under `pair-06/failed-attempts/`. The marker and run artifacts are
re-hashed before and after archival and their inode identities are preserved.

No model load, inference, game execution, training, promotion, deployment,
VOID-chain mutation, wallet action, or funds action is implemented here.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_failed_attempt_forensics_acceptance_generation2
    as forensics_acceptance,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-failed-attempt-preservation-contract.v1"
)
RECEIPT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-failed-attempt-preservation-receipt.v1"
)

PAIR_ROOT = Path(
    "/home/zoso/dev/void-war-college-execution/"
    "v8-generation2/generation2/pair-06"
)
FAILED_ARM = PAIR_ROOT / "baseline"
ARCHIVE_PARENT = PAIR_ROOT / "failed-attempts"
ARCHIVE_NAME = "baseline-20260923T221259Z-56c02591"
ARCHIVE_ROOT = ARCHIVE_PARENT / ARCHIVE_NAME
PRESERVATION_RECEIPT = (
    ARCHIVE_PARENT / f"{ARCHIVE_NAME}-preservation-receipt.json"
)

SOURCE_REPOSITORY = Path("/home/zoso/dev/openra-rl-war-college")
ENGINE_REPOSITORY = SOURCE_REPOSITORY / "OpenRA"

FROZEN_SOURCE_REL = Path("frozen-source")
ENGINE_REL = Path("engine")
CLAIMS_REL = Path("claims-v1")
RUNS_REL = Path("runs-v1")
MARKER_REL = CLAIMS_REL / "pair06-v8-baseline-game-attempt-v1.json"
RESULT_REL = CLAIMS_REL / "pair06-v8-baseline-game-result-v1.json"
CLOSEOUT_REL = CLAIMS_REL / "pair06-v8-baseline-game-closeout-v1.json"
REVOCATION_REL = CLAIMS_REL / "REVOKE_PAIR06_V8_BASELINE_GAME"
RUN_REL = (
    RUNS_REL
    / "warmstart-apollyon-vs-abaddon-20260923T221259Z-feinter-s208354846"
)
WARM_REL = RUN_REL / "warm-start.jsonl"
TRAJECTORY_REL = RUN_REL / "trajectory.jsonl"
SUMMARY_REL = RUN_REL / "summary.json"

ATTEMPT_MARKER_SHA256 = (
    "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
)
WARM_START_SHA256 = (
    "1a6bbd544aca9f111a0961948771c24f9e2e36eda7559cf78acac1df24411333"
)
WARM_START_BYTES = 229255
TRAJECTORY_SHA256 = (
    "89971bc284dab4424900eb7c27a73504e2acad067a59227dfdf37503475888ca"
)
TRAJECTORY_BYTES = 1027

FROZEN_SOURCE_COMMIT = "973802ef0a614e5afa782ff20e231e18966ae3e5"
FROZEN_SOURCE_TREE = "d8a2af418af00e95ca0f203a2f0264851f2308c6"
ENGINE_COMMIT = "1607a7a6501d42a47638393ecef8b22831064932"
ENGINE_TREE = "bf562078c53edda3e6545f501b73ba1273c5df49"

CONFIRM_TOKEN = "VOID_PAIR06_V8_PRESERVE_FAILED_ATTEMPT_56c02591"

NEXT_GATE = "PAIR06_V8_FAILED_ATTEMPT_PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_failed_attempt_preservation_review"


class Pair06V8FailedAttemptPreservationHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8FailedAttemptPreservationHold(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


def _file_identity(path: Path) -> tuple[int, int]:
    st = path.lstat()
    return int(st.st_dev), int(st.st_ino)


def _plain_file(path: Path, *, size: int, sha256: str) -> None:
    st = path.lstat()
    _require(stat.S_ISREG(st.st_mode), f"not regular file: {path}")
    _require(not stat.S_ISLNK(st.st_mode), f"symlink refused: {path}")
    _require(st.st_size == size, f"file size drift: {path}")
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    _require(actual == sha256, f"file SHA drift: {path}")


def _marker(path: Path) -> dict[str, Any]:
    st = path.lstat()
    _require(stat.S_ISREG(st.st_mode), "attempt marker is not regular")
    _require(not stat.S_ISLNK(st.st_mode), "attempt marker is symlinked")
    raw = path.read_bytes()
    _require(
        hashlib.sha256(raw).hexdigest() == ATTEMPT_MARKER_SHA256,
        "attempt marker SHA drift",
    )
    try:
        value = json.loads(raw)
    except Exception as exc:
        raise Pair06V8FailedAttemptPreservationHold(
            f"attempt marker JSON invalid: {exc}"
        ) from exc
    _require(isinstance(value, dict), "attempt marker must be object")
    _require(value.get("pair_slot") == 6, "attempt marker slot drift")
    _require(value.get("arm") == "baseline", "attempt marker arm drift")
    _require(value.get("held_out") is False, "attempt marker held-out drift")
    _require(value.get("automatic_retry") is False, "attempt marker retry drift")
    _require(value.get("maximum_attempts") == 1, "attempt marker count drift")
    return value


def _git(repository: Path, *args: str) -> str:
    proc = subprocess.run(
        [
            "/usr/bin/git",
            "--no-replace-objects",
            "-c", "core.hooksPath=/dev/null",
            "-c", "core.fsmonitor=false",
            "-c", "submodule.recurse=false",
            "-c", "protocol.allow=never",
            "-c", "gc.auto=0",
            "-c", "maintenance.auto=false",
            "-C", str(repository),
            *args,
        ],
        check=False,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=30,
        env={
            "PATH": "/usr/bin:/bin",
            "LC_ALL": "C",
            "LANG": "C",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_NO_LAZY_FETCH": "1",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_OPTIONAL_LOCKS": "0",
        },
    )
    _require(
        proc.returncode == 0,
        f"git command failed: {repository}: {' '.join(args)}",
    )
    return proc.stdout.strip()


def _worktree_entries(repository: Path) -> list[dict[str, Any]]:
    text = _git(repository, "worktree", "list", "--porcelain")
    entries = []
    current: dict[str, Any] = {}
    for line in text.splitlines() + [""]:
        if not line:
            if current:
                entries.append(current)
                current = {}
            continue
        if line.startswith("worktree "):
            current["worktree"] = line[len("worktree "):]
        elif line.startswith("HEAD "):
            current["HEAD"] = line[len("HEAD "):]
        elif line == "detached":
            current["detached"] = True
        elif line.startswith("branch "):
            current["branch"] = line[len("branch "):]
    return entries


def _validate_worktree(
    *,
    repository: Path,
    path: Path,
    commit: str,
    tree: str,
) -> dict[str, Any]:
    _require(path.is_dir() and not path.is_symlink(), f"worktree missing: {path}")
    _require(_git(path, "rev-parse", "HEAD") == commit, f"worktree commit drift: {path}")
    _require(_git(path, "rev-parse", "HEAD^{tree}") == tree, f"worktree tree drift: {path}")
    _require(
        _git(path, "status", "--porcelain", "--untracked-files=all") == "",
        f"worktree dirty: {path}",
    )
    symbolic = subprocess.run(
        ["/usr/bin/git", "-C", str(path), "symbolic-ref", "-q", "HEAD"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=10,
        env={
            "PATH": "/usr/bin:/bin",
            "LC_ALL": "C",
            "LANG": "C",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_NO_LAZY_FETCH": "1",
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_OPTIONAL_LOCKS": "0",
        },
    )
    _require(symbolic.returncode == 1, f"worktree is not detached: {path}")

    matches = [
        row
        for row in _worktree_entries(repository)
        if row.get("worktree") == str(path)
    ]
    _require(len(matches) == 1, f"worktree registration drift: {path}")
    entry = matches[0]
    _require(entry.get("HEAD") == commit, f"registered worktree HEAD drift: {path}")
    _require(entry.get("detached") is True, f"registered worktree not detached: {path}")
    _require("branch" not in entry, f"registered worktree unexpectedly branched: {path}")
    return {
        "repository": str(repository),
        "path": str(path),
        "commit": commit,
        "tree": tree,
        "clean": True,
        "detached": True,
        "registered": True,
    }


def _remove_worktree(repository: Path, path: Path) -> None:
    _git(repository, "worktree", "remove", str(path))
    _require(not path.exists(), f"worktree path remains after removal: {path}")
    matches = [
        row
        for row in _worktree_entries(repository)
        if row.get("worktree") == str(path)
    ]
    _require(not matches, f"worktree remains registered after removal: {path}")


def _expected_tree(root: Path, *, include_worktrees: bool) -> None:
    expected_top = {"claims-v1", "runs-v1"}
    if include_worktrees:
        expected_top.update({"frozen-source", "engine"})
    actual_top = {entry.name for entry in root.iterdir()}
    _require(actual_top == expected_top, "failed attempt top-level tree drift")

    claims = root / CLAIMS_REL
    runs = root / RUNS_REL
    run = root / RUN_REL
    _require(claims.is_dir() and not claims.is_symlink(), "claims directory drift")
    _require(runs.is_dir() and not runs.is_symlink(), "runs directory drift")
    _require(run.is_dir() and not run.is_symlink(), "run directory drift")

    _require(
        {entry.name for entry in claims.iterdir()} == {MARKER_REL.name},
        "claims tree drift",
    )
    _require(
        {entry.name for entry in runs.iterdir()} == {RUN_REL.name},
        "runs tree drift",
    )
    _require(
        {entry.name for entry in run.iterdir()}
        == {WARM_REL.name, TRAJECTORY_REL.name},
        "run artifact tree drift",
    )

    if include_worktrees:
        for rel in (FROZEN_SOURCE_REL, ENGINE_REL):
            path = root / rel
            _require(
                path.is_dir() and not path.is_symlink(),
                f"worktree directory drift: {path}",
            )
    else:
        _require(not (root / FROZEN_SOURCE_REL).exists(), "frozen source remains")
        _require(not (root / ENGINE_REL).exists(), "engine worktree remains")

    _require(not (root / RESULT_REL).exists(), "result unexpectedly present")
    _require(not (root / CLOSEOUT_REL).exists(), "closeout unexpectedly present")
    _require(not (root / REVOCATION_REL).exists(), "revocation unexpectedly present")
    _require(not (root / SUMMARY_REL).exists(), "summary unexpectedly present")


def _write_receipt(receipt: Mapping[str, Any]) -> None:
    _require(not PRESERVATION_RECEIPT.exists(), "preservation receipt already exists")
    raw = (
        json.dumps(
            receipt,
            sort_keys=True,
            indent=2,
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")
    fd = os.open(
        PRESERVATION_RECEIPT,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
        0o600,
    )
    try:
        with os.fdopen(fd, "wb", closefd=True) as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        raise


def preserve_failed_pair06_v8_attempt(*, confirm: str) -> dict[str, Any]:
    _require(
        confirm == CONFIRM_TOKEN,
        "PAIR06_V8_FAILED_ATTEMPT_PRESERVATION_CONFIRMATION_REQUIRED",
    )
    accepted = (
        forensics_acceptance
        .pair06_v8_failed_attempt_forensics_acceptance_contract()
    )
    _require(
        accepted.get("pair06_v8_failed_attempt_forensics_accepted") is True,
        "pair06 failed-attempt forensics not accepted",
    )
    _require(
        accepted.get("attempt_marker_sha256") == ATTEMPT_MARKER_SHA256,
        "pair06 failed-attempt marker identity drift",
    )
    _require(
        accepted.get("runtime_retry_authorized") is False,
        "pair06 forensic acceptance unexpectedly authorizes retry",
    )

    _require(FAILED_ARM.is_dir() and not FAILED_ARM.is_symlink(), "failed arm root invalid")
    _require(not ARCHIVE_ROOT.exists(), "archive destination already exists")
    _require(not PRESERVATION_RECEIPT.exists(), "preservation receipt already exists")

    _expected_tree(FAILED_ARM, include_worktrees=True)
    marker = FAILED_ARM / MARKER_REL
    warm = FAILED_ARM / WARM_REL
    trajectory = FAILED_ARM / TRAJECTORY_REL

    _marker(marker)
    _plain_file(warm, size=WARM_START_BYTES, sha256=WARM_START_SHA256)
    _plain_file(trajectory, size=TRAJECTORY_BYTES, sha256=TRAJECTORY_SHA256)

    failed_arm_identity = _file_identity(FAILED_ARM)
    marker_identity = _file_identity(marker)
    warm_identity = _file_identity(warm)
    trajectory_identity = _file_identity(trajectory)

    source_info = _validate_worktree(
        repository=SOURCE_REPOSITORY,
        path=FAILED_ARM / FROZEN_SOURCE_REL,
        commit=FROZEN_SOURCE_COMMIT,
        tree=FROZEN_SOURCE_TREE,
    )
    engine_info = _validate_worktree(
        repository=ENGINE_REPOSITORY,
        path=FAILED_ARM / ENGINE_REL,
        commit=ENGINE_COMMIT,
        tree=ENGINE_TREE,
    )

    _remove_worktree(SOURCE_REPOSITORY, FAILED_ARM / FROZEN_SOURCE_REL)
    _remove_worktree(ENGINE_REPOSITORY, FAILED_ARM / ENGINE_REL)

    _expected_tree(FAILED_ARM, include_worktrees=False)
    _marker(marker)
    _plain_file(warm, size=WARM_START_BYTES, sha256=WARM_START_SHA256)
    _plain_file(trajectory, size=TRAJECTORY_BYTES, sha256=TRAJECTORY_SHA256)

    ARCHIVE_PARENT.mkdir(mode=0o700, parents=False, exist_ok=True)
    _require(
        ARCHIVE_PARENT.is_dir() and not ARCHIVE_PARENT.is_symlink(),
        "archive parent invalid",
    )

    os.rename(FAILED_ARM, ARCHIVE_ROOT)

    _require(not FAILED_ARM.exists(), "failed arm source path remains after archive")
    _expected_tree(ARCHIVE_ROOT, include_worktrees=False)

    archived_marker = ARCHIVE_ROOT / MARKER_REL
    archived_warm = ARCHIVE_ROOT / WARM_REL
    archived_trajectory = ARCHIVE_ROOT / TRAJECTORY_REL

    _marker(archived_marker)
    _plain_file(
        archived_warm,
        size=WARM_START_BYTES,
        sha256=WARM_START_SHA256,
    )
    _plain_file(
        archived_trajectory,
        size=TRAJECTORY_BYTES,
        sha256=TRAJECTORY_SHA256,
    )

    _require(
        _file_identity(ARCHIVE_ROOT) == failed_arm_identity,
        "failed arm inode changed during archive",
    )
    _require(
        _file_identity(archived_marker) == marker_identity,
        "attempt marker inode changed during archive",
    )
    _require(
        _file_identity(archived_warm) == warm_identity,
        "warm-start inode changed during archive",
    )
    _require(
        _file_identity(archived_trajectory) == trajectory_identity,
        "trajectory inode changed during archive",
    )

    body = {
        "schema": RECEIPT_SCHEMA,
        "pair_slot": 6,
        "arm": "baseline",
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "source_path": str(FAILED_ARM),
        "archive_path": str(ARCHIVE_ROOT),
        "archive_name": ARCHIVE_NAME,
        "frozen_source_worktree": source_info,
        "engine_worktree": engine_info,
        "frozen_source_worktree_removed_non_force": True,
        "engine_worktree_removed_non_force": True,
        "source_path_absent_after_preservation": True,
        "archive_path_present_after_preservation": True,
        "failed_arm_inode_preserved": True,
        "attempt_marker_inode_preserved": True,
        "warm_start_inode_preserved": True,
        "trajectory_inode_preserved": True,
        "warm_start_sha256": WARM_START_SHA256,
        "warm_start_bytes": WARM_START_BYTES,
        "trajectory_sha256": TRAJECTORY_SHA256,
        "trajectory_bytes": TRAJECTORY_BYTES,
        "failed_attempt_deleted": False,
        "runtime_retry_performed": False,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
    }
    receipt = {
        **body,
        "preservation_receipt_sha256": _digest(body),
    }
    _write_receipt(receipt)
    return receipt


def pair06_v8_failed_attempt_preservation_contract() -> dict[str, Any]:
    accepted = (
        forensics_acceptance
        .pair06_v8_failed_attempt_forensics_acceptance_contract()
    )
    return {
        "schema": CONTRACT_SCHEMA,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "confirm_token": CONFIRM_TOKEN,
        "failed_arm_path": str(FAILED_ARM),
        "archive_parent": str(ARCHIVE_PARENT),
        "archive_name": ARCHIVE_NAME,
        "archive_path": str(ARCHIVE_ROOT),
        "preservation_receipt_path": str(PRESERVATION_RECEIPT),
        "exact_failed_tree_required": True,
        "exact_registered_clean_detached_worktrees_required": True,
        "non_force_worktree_removal_implemented": True,
        "atomic_same_filesystem_rename_implemented": True,
        "inode_identity_preservation_checked": True,
        "marker_warm_start_trajectory_rehashed_after_archive": True,
        "failed_attempt_deletion_implemented": False,
        "runtime_retry_implemented_by_this_source": False,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "runtime_start_implemented": False,
        "model_load_implemented": False,
        "model_inference_implemented": False,
        "game_execution_implemented": False,
        "training_implemented": False,
        "weights_update_implemented": False,
        "automatic_policy_promotion_implemented": False,
        "deployment_implemented": False,
        "void_chain_mutation_implemented": False,
        "wallet_or_funds_action_implemented": False,
        "accepted_forensics": accepted,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_retry(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8FailedAttemptPreservationHold(
        "PAIR06_V8_FAILED_ATTEMPT_RETRY_NOT_AUTHORIZED"
    )
