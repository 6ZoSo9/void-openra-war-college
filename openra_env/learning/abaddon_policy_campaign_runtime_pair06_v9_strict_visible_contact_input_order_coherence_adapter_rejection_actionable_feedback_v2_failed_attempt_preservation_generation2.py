"""Evidence-preserving archival gate for the consumed Pair-06 V9 actionable-feedback V2 failure.

The consumed attempt passed fresh CUDA admission, created its durable attempt
marker, entered live combat, and then failed closed at round 6 after exhausting
six strict-contact decision attempts. The terminal feedback was:

function_not_offered:
__v8_adapter_rejected_move_units_unit_ids_must_be_quoted_string_
not_json_array_or_bare_integer__

This module preserves that exact failed attempt before any later repair-lineage
execution request may be opened.

When separately authorized it:
1. validates the exact consumed marker and exact observed run artifacts;
2. validates the exact source/engine worktrees are registered once, detached,
   clean, and pinned to the reviewed frozen commits/trees;
3. removes only those two worktrees using non-force git worktree remove;
4. inventories every remaining regular evidence file under the baseline root;
5. atomically renames the remaining baseline tree into a unique failed-attempt
   archive namespace; and
6. writes a create-only preservation receipt outside the archived tree.

The marker and run artifacts are preserved byte-for-byte and inode-for-inode
through the atomic rename. No retry, model load, inference, game execution,
training, promotion, deployment, VOID-chain mutation, wallet/funds action, or
scheduler mutation is implemented.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
from typing import Any


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "failed-attempt-preservation-contract.v1"
)
RECEIPT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "failed-attempt-preservation-receipt.v1"
)

PAIR_ROOT = Path(
    "/home/zoso/dev/void-war-college-execution/"
    "v8-generation2/generation2/pair-06"
)
FAILED_ARM = PAIR_ROOT / "baseline"
ARCHIVE_PARENT = PAIR_ROOT / "failed-attempts"
ARCHIVE_NAME = (
    "baseline-v9-input-order-adapter-rejection-actionable-feedback-v2-35b75823"
)
ARCHIVE_ROOT = ARCHIVE_PARENT / ARCHIVE_NAME
PRESERVATION_RECEIPT = (
    ARCHIVE_PARENT / f"{ARCHIVE_NAME}-preservation-receipt.json"
)

SOURCE_REPOSITORY = Path("/home/zoso/dev/openra-rl-war-college")
ENGINE_REPOSITORY = SOURCE_REPOSITORY / "OpenRA"

FROZEN_SOURCE_REL = Path("frozen-source")
ENGINE_REL = Path("engine")
CLAIMS_REL = Path("claims-v1")
RUNS_REL = Path(
    "runs-v9-strict-visible-contact-input-order-coherence-"
    "adapter-rejection-actionable-feedback-v2-v1"
)

MARKER_REL = (
    CLAIMS_REL
    / "pair06-v9-strict-visible-contact-input-order-coherence-"
      "adapter-rejection-actionable-feedback-v2-baseline-game-attempt-v1.json"
)
RESULT_REL = (
    CLAIMS_REL
    / "pair06-v9-strict-visible-contact-input-order-coherence-"
      "adapter-rejection-actionable-feedback-v2-baseline-game-result-v1.json"
)
CLOSEOUT_REL = (
    CLAIMS_REL
    / "pair06-v9-strict-visible-contact-input-order-coherence-"
      "adapter-rejection-actionable-feedback-v2-baseline-game-closeout-v1.json"
)

RUN_NAME = (
    "warmstart-apollyon-vs-abaddon-"
    "20261005T014439Z-feinter-s208354846"
)
RUN_REL = RUNS_REL / RUN_NAME
WARM_REL = RUN_REL / "warm-start.jsonl"
TRAJECTORY_REL = RUN_REL / "trajectory.jsonl"
SUMMARY_REL = RUN_REL / "summary.json"

ATTEMPT_MARKER_SHA256 = (
    "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
)
ATTEMPT_MARKER_BYTES = 2208
WARM_START_SHA256 = (
    "422894c30a385eadd997e741bed84b92c5ffb4af35de1170f0f7bce6805964d5"
)
WARM_START_BYTES = 229255
TRAJECTORY_SHA256 = (
    "3302536e3faecb6d5f99da6922ba028929dec26180360ed3dcc63242bab77c6f"
)
TRAJECTORY_BYTES = 58075

AUTHORIZED_ATTEMPT_MAIN_HEAD = "63a5077ba247a974d2696c479972efdf4cd0f6e8"
AUTHORIZED_ATTEMPT_MAIN_TREE = "e9a6bdf0423e739f97519515f62bd24ef65cf1a3"
OPERATOR_SOURCE_SHA256 = (
    "fcc662cbaaa482651004523b73deb906947a73b296356cc291bb9150dddfc179"
)

FROZEN_SOURCE_COMMIT = "973802ef0a614e5afa782ff20e231e18966ae3e5"
FROZEN_SOURCE_TREE = "d8a2af418af00e95ca0f203a2f0264851f2308c6"
ENGINE_COMMIT = "1607a7a6501d42a47638393ecef8b22831064932"
ENGINE_TREE = "bf562078c53edda3e6545f501b73ba1273c5df49"

FAILURE_CLASS = "strict_contact_actionable_feedback_v2_exhausted"
FAILURE_ROUND = 6
MAX_DECISION_ATTEMPTS = 6
TERMINAL_FEEDBACK = (
    "function_not_offered:"
    "__v8_adapter_rejected_move_units_unit_ids_must_be_quoted_string_"
    "not_json_array_or_bare_integer__"
)

CONFIRM_TOKEN = (
    "VOID_PAIR06_V9_PRESERVE_ACTIONABLE_FEEDBACK_V2_FAILED_ATTEMPT_35B75823"
)

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FAILED_ATTEMPT_"
    "PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "adapter_rejection_actionable_feedback_v2_failed_attempt_preservation_review"
)


class Pair06V9ActionableFeedbackV2FailedAttemptPreservationHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2FailedAttemptPreservationHold(message)


def _stable_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")


def _digest(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


def _file_identity(path: Path) -> tuple[int, int]:
    st = path.lstat()
    _require(stat.S_ISREG(st.st_mode), f"not regular file: {path}")
    _require(not stat.S_ISLNK(st.st_mode), f"symlink refused: {path}")
    return int(st.st_dev), int(st.st_ino)


def _sha256_regular(path: Path) -> str:
    _file_identity(path)
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _plain_file(path: Path, *, size: int | None, sha256: str) -> dict[str, Any]:
    st = path.lstat()
    _require(stat.S_ISREG(st.st_mode), f"not regular file: {path}")
    _require(not stat.S_ISLNK(st.st_mode), f"symlink refused: {path}")
    if size is not None:
        _require(st.st_size == size, f"file size drift: {path}")
    actual = _sha256_regular(path)
    _require(actual == sha256, f"file SHA drift: {path}")
    return {
        "path": str(path),
        "bytes": int(st.st_size),
        "sha256": actual,
        "dev": int(st.st_dev),
        "inode": int(st.st_ino),
    }


def _git(
    repository: Path,
    *args: str,
    allowed: tuple[int, ...] = (0,),
) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        [
            "/usr/bin/git",
            "--no-replace-objects",
            "-c", "core.hooksPath=/dev/null",
            "-c", "core.fsmonitor=false",
            "-c", "core.attributesFile=/dev/null",
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
        proc.returncode in allowed,
        f"git command failed: {repository}: {' '.join(args)}",
    )
    return proc


def _worktree_registration_count(repository: Path, path: Path) -> int:
    text = _git(repository, "worktree", "list", "--porcelain").stdout
    return sum(
        1
        for line in text.splitlines()
        if line == f"worktree {path}"
    )


def _validate_worktree(
    *,
    repository: Path,
    path: Path,
    commit: str,
    tree: str,
) -> dict[str, Any]:
    _require(path.is_dir() and not path.is_symlink(), f"worktree missing: {path}")
    _require(
        _worktree_registration_count(repository, path) == 1,
        f"worktree registration drift: {path}",
    )
    top = _git(path, "rev-parse", "--show-toplevel").stdout.strip()
    head = _git(path, "rev-parse", "HEAD").stdout.strip()
    actual_tree = _git(path, "rev-parse", "HEAD^{tree}").stdout.strip()
    status = _git(path, "status", "--porcelain", "--untracked-files=all").stdout

    _require(top == str(path), f"worktree toplevel drift: {path}")
    _require(head == commit, f"worktree commit drift: {path}")
    _require(actual_tree == tree, f"worktree tree drift: {path}")
    _require(status == "", f"worktree dirty: {path}")

    symbolic = _git(path, "symbolic-ref", "-q", "HEAD", allowed=(0, 1))
    _require(symbolic.returncode != 0, f"worktree unexpectedly attached: {path}")

    return {
        "path": str(path),
        "repository": str(repository),
        "head": head,
        "tree": actual_tree,
        "clean": True,
        "detached": True,
        "registered_once": True,
    }


def _remove_worktree(repository: Path, path: Path) -> None:
    _git(repository, "worktree", "remove", str(path))
    _require(not path.exists(), f"worktree path remained: {path}")
    _require(
        _worktree_registration_count(repository, path) == 0,
        f"worktree remained registered: {path}",
    )


def _evidence_manifest(root: Path) -> tuple[dict[str, Any], ...]:
    _require(root.is_dir() and not root.is_symlink(), "evidence root missing")
    rows: list[dict[str, Any]] = []

    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(dirs):
            p = current_path / name
            st = p.lstat()
            _require(
                stat.S_ISDIR(st.st_mode) and not stat.S_ISLNK(st.st_mode),
                f"evidence directory type drift: {p}",
            )
        for name in sorted(files):
            p = current_path / name
            st = p.lstat()
            _require(
                stat.S_ISREG(st.st_mode) and not stat.S_ISLNK(st.st_mode),
                f"evidence file type drift: {p}",
            )
            rows.append(
                {
                    "relative_path": str(p.relative_to(root)),
                    "bytes": int(st.st_size),
                    "sha256": _sha256_regular(p),
                    "dev": int(st.st_dev),
                    "inode": int(st.st_ino),
                }
            )

    rows.sort(key=lambda row: row["relative_path"])
    return tuple(rows)


def _write_create_only(path: Path, payload: dict[str, Any]) -> str:
    raw = _stable_bytes(payload)
    fd = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
        0o600,
    )
    try:
        written = 0
        while written < len(raw):
            n = os.write(fd, raw[written:])
            _require(n > 0, "preservation receipt short write")
            written += n
        os.fsync(fd)
    finally:
        os.close(fd)
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    _require(actual == hashlib.sha256(raw).hexdigest(), "receipt write drift")
    return actual


def _validate_failed_state() -> dict[str, Any]:
    _require(FAILED_ARM.is_dir() and not FAILED_ARM.is_symlink(), "baseline missing")
    _require(
        ARCHIVE_PARENT.is_dir() and not ARCHIVE_PARENT.is_symlink(),
        "failed-attempt archive parent missing",
    )
    _require(not ARCHIVE_ROOT.exists(), "failed-attempt archive already exists")
    _require(
        not PRESERVATION_RECEIPT.exists(),
        "failed-attempt preservation receipt already exists",
    )

    marker = _plain_file(
        FAILED_ARM / MARKER_REL,
        size=ATTEMPT_MARKER_BYTES,
        sha256=ATTEMPT_MARKER_SHA256,
    )
    warm = _plain_file(
        FAILED_ARM / WARM_REL,
        size=WARM_START_BYTES,
        sha256=WARM_START_SHA256,
    )
    trajectory = _plain_file(
        FAILED_ARM / TRAJECTORY_REL,
        size=TRAJECTORY_BYTES,
        sha256=TRAJECTORY_SHA256,
    )

    _require(not (FAILED_ARM / RESULT_REL).exists(), "unexpected result present")
    _require(not (FAILED_ARM / CLOSEOUT_REL).exists(), "unexpected closeout present")
    _require(not (FAILED_ARM / SUMMARY_REL).exists(), "unexpected summary present")

    run_root = FAILED_ARM / RUNS_REL
    _require(run_root.is_dir() and not run_root.is_symlink(), "runs root missing")
    run_dirs = sorted(p.name for p in run_root.iterdir() if p.is_dir())
    _require(run_dirs == [RUN_NAME], "failed-attempt run directory drift")
    run_files = sorted(
        str(p.relative_to(run_root))
        for p in run_root.rglob("*")
        if p.is_file()
    )
    _require(
        run_files
        == [
            f"{RUN_NAME}/trajectory.jsonl",
            f"{RUN_NAME}/warm-start.jsonl",
        ],
        "failed-attempt run artifact set drift",
    )

    source = _validate_worktree(
        repository=SOURCE_REPOSITORY,
        path=FAILED_ARM / FROZEN_SOURCE_REL,
        commit=FROZEN_SOURCE_COMMIT,
        tree=FROZEN_SOURCE_TREE,
    )
    engine = _validate_worktree(
        repository=ENGINE_REPOSITORY,
        path=FAILED_ARM / ENGINE_REL,
        commit=ENGINE_COMMIT,
        tree=ENGINE_TREE,
    )

    return {
        "marker": marker,
        "warm_start": warm,
        "trajectory": trajectory,
        "source_worktree": source,
        "engine_worktree": engine,
    }


def preserve_pair06_v9_actionable_feedback_v2_failed_attempt(
    *,
    preservation_authorized: bool,
    confirm: str,
) -> dict[str, Any]:
    """Preserve the exact consumed V2 failed attempt without retrying runtime."""
    _require(
        preservation_authorized is True,
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_PRESERVATION_AUTHORIZATION_REQUIRED",
    )
    _require(
        type(confirm) is str and confirm == CONFIRM_TOKEN,
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_PRESERVATION_CONFIRMATION_REQUIRED",
    )

    before = _validate_failed_state()

    marker_identity = (
        before["marker"]["dev"],
        before["marker"]["inode"],
    )
    warm_identity = (
        before["warm_start"]["dev"],
        before["warm_start"]["inode"],
    )
    trajectory_identity = (
        before["trajectory"]["dev"],
        before["trajectory"]["inode"],
    )

    # Preserve reviewed cleanup ordering: engine first, source second.
    _remove_worktree(ENGINE_REPOSITORY, FAILED_ARM / ENGINE_REL)
    _remove_worktree(SOURCE_REPOSITORY, FAILED_ARM / FROZEN_SOURCE_REL)

    manifest_before = _evidence_manifest(FAILED_ARM)
    _require(
        any(
            row["relative_path"] == str(MARKER_REL)
            and row["sha256"] == ATTEMPT_MARKER_SHA256
            for row in manifest_before
        ),
        "attempt marker missing from pre-archive manifest",
    )

    os.rename(FAILED_ARM, ARCHIVE_ROOT)
    _require(not FAILED_ARM.exists(), "baseline path remained after archive rename")
    _require(
        ARCHIVE_ROOT.is_dir() and not ARCHIVE_ROOT.is_symlink(),
        "archive root missing after rename",
    )

    archived_marker = _plain_file(
        ARCHIVE_ROOT / MARKER_REL,
        size=ATTEMPT_MARKER_BYTES,
        sha256=ATTEMPT_MARKER_SHA256,
    )
    archived_warm = _plain_file(
        ARCHIVE_ROOT / WARM_REL,
        size=WARM_START_BYTES,
        sha256=WARM_START_SHA256,
    )
    archived_trajectory = _plain_file(
        ARCHIVE_ROOT / TRAJECTORY_REL,
        size=TRAJECTORY_BYTES,
        sha256=TRAJECTORY_SHA256,
    )

    _require(
        (archived_marker["dev"], archived_marker["inode"]) == marker_identity,
        "attempt marker inode identity changed during archive rename",
    )
    _require(
        (archived_warm["dev"], archived_warm["inode"]) == warm_identity,
        "warm-start inode identity changed during archive rename",
    )
    _require(
        (archived_trajectory["dev"], archived_trajectory["inode"])
        == trajectory_identity,
        "trajectory inode identity changed during archive rename",
    )

    manifest_after = _evidence_manifest(ARCHIVE_ROOT)
    _require(
        manifest_after == manifest_before,
        "archived evidence manifest changed during rename",
    )

    payload = {
        "schema": RECEIPT_SCHEMA,
        "record_kind": "failed_attempt_preservation_receipt",
        "pair_slot": 6,
        "arm": "baseline",
        "policy_id": "pair06-v9-strict-visible-contact-envelope-v1",
        "failure_class": FAILURE_CLASS,
        "failure_round": FAILURE_ROUND,
        "maximum_decision_attempts": MAX_DECISION_ATTEMPTS,
        "terminal_feedback": TERMINAL_FEEDBACK,
        "attempt_consumed": True,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "attempt_marker_bytes": ATTEMPT_MARKER_BYTES,
        "authorized_attempt_main_head": AUTHORIZED_ATTEMPT_MAIN_HEAD,
        "authorized_attempt_main_tree": AUTHORIZED_ATTEMPT_MAIN_TREE,
        "operator_source_sha256": OPERATOR_SOURCE_SHA256,
        "result_present": False,
        "closeout_present": False,
        "summary_present": False,
        "warm_start_sha256": WARM_START_SHA256,
        "warm_start_bytes": WARM_START_BYTES,
        "trajectory_sha256": TRAJECTORY_SHA256,
        "trajectory_bytes": TRAJECTORY_BYTES,
        "source_worktree_removed_non_force": True,
        "engine_worktree_removed_non_force": True,
        "archive_name": ARCHIVE_NAME,
        "archive_path": str(ARCHIVE_ROOT),
        "archive_atomic_rename_performed": True,
        "attempt_marker_inode_preserved": True,
        "warm_start_inode_preserved": True,
        "trajectory_inode_preserved": True,
        "evidence_manifest": [deepcopy(row) for row in manifest_after],
        "evidence_manifest_sha256": _digest(
            {"files": [deepcopy(row) for row in manifest_after]}
        ),
        "automatic_retry": False,
        "runtime_retry_authorized": False,
        "new_execution_request_opened": False,
        "runtime_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "scheduler_mutation_performed": False,
    }
    receipt_sha256 = _write_create_only(PRESERVATION_RECEIPT, payload)

    return {
        **deepcopy(payload),
        "preservation_receipt": str(PRESERVATION_RECEIPT),
        "preservation_receipt_sha256": receipt_sha256,
    }


def pair06_v9_actionable_feedback_v2_failed_attempt_preservation_contract() -> dict[str, Any]:
    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": 6,
        "arm": "baseline",
        "policy_id": "pair06-v9-strict-visible-contact-envelope-v1",
        "failure_class": FAILURE_CLASS,
        "failure_round": FAILURE_ROUND,
        "maximum_decision_attempts": MAX_DECISION_ATTEMPTS,
        "terminal_feedback": TERMINAL_FEEDBACK,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "attempt_marker_bytes": ATTEMPT_MARKER_BYTES,
        "authorized_attempt_main_head": AUTHORIZED_ATTEMPT_MAIN_HEAD,
        "authorized_attempt_main_tree": AUTHORIZED_ATTEMPT_MAIN_TREE,
        "operator_source_sha256": OPERATOR_SOURCE_SHA256,
        "warm_start_sha256": WARM_START_SHA256,
        "warm_start_bytes": WARM_START_BYTES,
        "trajectory_sha256": TRAJECTORY_SHA256,
        "trajectory_bytes": TRAJECTORY_BYTES,
        "source_worktree_commit": FROZEN_SOURCE_COMMIT,
        "source_worktree_tree": FROZEN_SOURCE_TREE,
        "engine_worktree_commit": ENGINE_COMMIT,
        "engine_worktree_tree": ENGINE_TREE,
        "archive_name": ARCHIVE_NAME,
        "archive_path": str(ARCHIVE_ROOT),
        "preservation_receipt_path": str(PRESERVATION_RECEIPT),
        "exact_consumed_marker_required": True,
        "exact_run_artifacts_required": True,
        "result_must_be_absent": True,
        "closeout_must_be_absent": True,
        "summary_must_be_absent": True,
        "exact_clean_detached_registered_worktrees_required": True,
        "non_force_worktree_removal_only": True,
        "engine_removed_before_source": True,
        "remaining_evidence_manifest_hashed": True,
        "atomic_baseline_archive_rename_implemented": True,
        "attempt_marker_inode_preserved": True,
        "run_artifact_inode_preserved": True,
        "create_only_preservation_receipt_implemented": True,
        "preservation_requires_explicit_authority": True,
        "preservation_confirmation_token_required": True,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "new_execution_request_opened": False,
        "runtime_execution_authorized": False,
        "game_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "host_io_performed_by_contract_inspection": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def review_or_preserve(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV2FailedAttemptPreservationHold(NEXT_GATE)
