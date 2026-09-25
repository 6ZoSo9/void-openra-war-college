"""Evidence-preserving archival gate for the third consumed pair-06 V8 attempt.

This source preserves the exact marker-only residual OOM tree accepted by the
third-attempt forensic contract. It removes only the two exact clean detached
Git worktrees with non-force `git worktree remove`, then atomically renames
the remaining baseline tree into the failed-attempt archive namespace.

The consumed marker is preserved byte-for-byte and inode-for-inode. The runs
directory is required to be empty. Result, closeout, and revocation must remain
absent. Prior failed-attempt archives and their receipts are revalidated before
and after archival.

No retry, model load, inference, game execution, training, promotion,
deployment, VOID-chain mutation, wallet action, or funds action is implemented.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_third_failed_attempt_forensics_acceptance_generation2
    as forensics_acceptance,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-third-failed-attempt-preservation-contract.v1"
)
RECEIPT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-third-failed-attempt-preservation-receipt.v1"
)

FORENSICS_ACCEPTANCE_GIT_BLOB = "053e311c286a904b26e3ef407e76e46b565d3c81"
FORENSICS_ACCEPTANCE_SOURCE_SHA256 = (
    "75a11e237915dd22eb15f6cf0347ad44bfe1644e667e1562e0827e9d57b15f0e"
)

PAIR_ROOT = Path(
    "/home/zoso/dev/void-war-college-execution/"
    "v8-generation2/generation2/pair-06"
)
FAILED_ARM = PAIR_ROOT / "baseline"
ARCHIVE_PARENT = PAIR_ROOT / "failed-attempts"
ARCHIVE_NAME = "baseline-3ad564f9"
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

ATTEMPT_MARKER_SHA256 = (
    "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
)
ATTEMPT_MARKER_BYTES = 974
ATTEMPT_MARKER_DEV = 2050
ATTEMPT_MARKER_INODE = 209756174

FROZEN_SOURCE_COMMIT = "973802ef0a614e5afa782ff20e231e18966ae3e5"
FROZEN_SOURCE_TREE = "d8a2af418af00e95ca0f203a2f0264851f2308c6"
ENGINE_COMMIT = "1607a7a6501d42a47638393ecef8b22831064932"
ENGINE_TREE = "bf562078c53edda3e6545f501b73ba1273c5df49"

PRIOR_ARCHIVES = (
    (
        "baseline-20260923T221259Z-56c02591",
        "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930",
        "d32cc7779fb1570ac2085031e296817059ce51d35de43ca3875becf9d032ccff",
    ),
    (
        "baseline-20260923T235031Z-446d8f92",
        "446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1",
        "bb0bbfe5c7441706ce61924a718c4055a8e2c991c117f699ad5aa0c7863339b4",
    ),
)

CONFIRM_TOKEN = "VOID_PAIR06_V8_PRESERVE_THIRD_FAILED_ATTEMPT_3AD564F9"

NEXT_GATE = (
    "PAIR06_V8_THIRD_FAILED_ATTEMPT_PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_third_failed_attempt_preservation_review"
)


class Pair06V8ThirdFailedAttemptPreservationHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8ThirdFailedAttemptPreservationHold(message)


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


def _sha256_plain_file(path: Path) -> str:
    st = path.lstat()
    _require(stat.S_ISREG(st.st_mode), f"not regular file: {path}")
    _require(not stat.S_ISLNK(st.st_mode), f"symlink refused: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_prior_archives() -> tuple[dict[str, Any], ...]:
    rows = []
    for name, marker_sha256, receipt_sha256 in PRIOR_ARCHIVES:
        root = ARCHIVE_PARENT / name
        marker = root / MARKER_REL
        receipt = ARCHIVE_PARENT / f"{name}-preservation-receipt.json"
        _require(root.is_dir() and not root.is_symlink(), f"prior archive missing: {name}")
        _require(
            _sha256_plain_file(marker) == marker_sha256,
            f"prior archive marker drift: {name}",
        )
        _require(
            _sha256_plain_file(receipt) == receipt_sha256,
            f"prior archive receipt drift: {name}",
        )
        rows.append(
            {
                "archive_name": name,
                "archive_path": str(root),
                "marker_sha256": marker_sha256,
                "preservation_receipt_file_sha256": receipt_sha256,
                "unchanged": True,
            }
        )
    return tuple(rows)


def _marker(path: Path) -> dict[str, Any]:
    st = path.lstat()
    _require(stat.S_ISREG(st.st_mode), "attempt marker is not regular")
    _require(not stat.S_ISLNK(st.st_mode), "attempt marker is symlinked")
    _require(st.st_size == ATTEMPT_MARKER_BYTES, "attempt marker size drift")
    _require(int(st.st_dev) == ATTEMPT_MARKER_DEV, "attempt marker device drift")
    _require(int(st.st_ino) == ATTEMPT_MARKER_INODE, "attempt marker inode drift")
    raw = path.read_bytes()
    _require(
        hashlib.sha256(raw).hexdigest() == ATTEMPT_MARKER_SHA256,
        "attempt marker SHA drift",
    )
    try:
        value = json.loads(raw)
    except Exception as exc:
        raise Pair06V8ThirdFailedAttemptPreservationHold(
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
        row for row in _worktree_entries(repository)
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
        row for row in _worktree_entries(repository)
        if row.get("worktree") == str(path)
    ]
    _require(not matches, f"worktree remains registered after removal: {path}")


def _expected_tree(root: Path, *, include_worktrees: bool) -> None:
    expected_top = {"claims-v1", "runs-v1"}
    if include_worktrees:
        expected_top.update({"frozen-source", "engine"})
    actual_top = {entry.name for entry in root.iterdir()}
    _require(actual_top == expected_top, "third failed-attempt top-level tree drift")

    claims = root / CLAIMS_REL
    runs = root / RUNS_REL
    _require(claims.is_dir() and not claims.is_symlink(), "claims directory drift")
    _require(runs.is_dir() and not runs.is_symlink(), "runs directory drift")
    _require(
        {entry.name for entry in claims.iterdir()} == {MARKER_REL.name},
        "claims tree drift",
    )
    _require(not any(runs.iterdir()), "runs tree must be empty")

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


def preserve_third_failed_pair06_v8_attempt(*, confirm: str) -> dict[str, Any]:
    _require(
        confirm == CONFIRM_TOKEN,
        "PAIR06_V8_THIRD_FAILED_ATTEMPT_PRESERVATION_CONFIRMATION_REQUIRED",
    )
    accepted = (
        forensics_acceptance
        .pair06_v8_third_failed_attempt_forensics_acceptance_contract()
    )
    _require(
        accepted.get("pair06_v8_third_failed_attempt_forensics_accepted") is True,
        "pair06 third failed-attempt forensics not accepted",
    )
    _require(
        accepted.get("attempt_marker_sha256") == ATTEMPT_MARKER_SHA256,
        "pair06 third failed-attempt marker identity drift",
    )
    _require(
        accepted.get("runtime_retry_authorized") is False,
        "pair06 third forensic acceptance unexpectedly authorizes retry",
    )

    _require(FAILED_ARM.is_dir() and not FAILED_ARM.is_symlink(), "failed arm root invalid")
    _require(not ARCHIVE_ROOT.exists(), "archive destination already exists")
    _require(not PRESERVATION_RECEIPT.exists(), "preservation receipt already exists")
    prior_archives = _validate_prior_archives()

    _expected_tree(FAILED_ARM, include_worktrees=True)
    marker = FAILED_ARM / MARKER_REL
    _marker(marker)

    failed_arm_identity = _file_identity(FAILED_ARM)
    marker_identity = _file_identity(marker)

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

    _require(
        ARCHIVE_PARENT.is_dir() and not ARCHIVE_PARENT.is_symlink(),
        "archive parent invalid",
    )
    os.rename(FAILED_ARM, ARCHIVE_ROOT)

    _require(not FAILED_ARM.exists(), "failed arm source path remains after archive")
    _expected_tree(ARCHIVE_ROOT, include_worktrees=False)

    archived_marker = ARCHIVE_ROOT / MARKER_REL
    _marker(archived_marker)

    _require(
        _file_identity(ARCHIVE_ROOT) == failed_arm_identity,
        "failed arm inode changed during archive",
    )
    _require(
        _file_identity(archived_marker) == marker_identity,
        "attempt marker inode changed during archive",
    )
    _require(
        _validate_prior_archives() == prior_archives,
        "prior failed-attempt archives changed during third preservation",
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
        "runs_empty": True,
        "prior_failed_attempt_archives": prior_archives,
        "prior_failed_attempt_archives_unchanged": True,
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


def pair06_v8_third_failed_attempt_preservation_contract() -> dict[str, Any]:
    accepted = (
        forensics_acceptance
        .pair06_v8_third_failed_attempt_forensics_acceptance_contract()
    )
    return {
        "schema": CONTRACT_SCHEMA,
        "forensics_acceptance_git_blob": FORENSICS_ACCEPTANCE_GIT_BLOB,
        "forensics_acceptance_source_sha256": (
            FORENSICS_ACCEPTANCE_SOURCE_SHA256
        ),
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "confirm_token": CONFIRM_TOKEN,
        "failed_arm_path": str(FAILED_ARM),
        "archive_parent": str(ARCHIVE_PARENT),
        "archive_name": ARCHIVE_NAME,
        "archive_path": str(ARCHIVE_ROOT),
        "preservation_receipt_path": str(PRESERVATION_RECEIPT),
        "marker_only_claims_required": True,
        "empty_runs_required": True,
        "exact_registered_clean_detached_worktrees_required": True,
        "non_force_worktree_removal_implemented": True,
        "atomic_same_filesystem_rename_implemented": True,
        "inode_identity_preservation_checked": True,
        "marker_rehashed_after_archive": True,
        "both_prior_failed_attempt_archives_revalidated_before_and_after": True,
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
        "accepted_forensics": deepcopy(accepted),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_retry(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8ThirdFailedAttemptPreservationHold(
        "PAIR06_V8_THIRD_FAILED_ATTEMPT_RETRY_NOT_AUTHORIZED"
    )
