"""Evidence-preserving archival gate for the failed V2R13 pair-03 baseline.

This module implements only preservation of the already-consumed failed attempt.
It never starts runtime and never retries the arm.  The preservation action is
explicit, fail-closed, and requires the exact confirmation token.

The failed arm directory is atomically renamed to a deterministic sibling under
`pair-03/failed-attempts/`.  The surviving warm-start artifact is verified
before and after the rename, and a preservation receipt is written outside the
archived attempt so the archived tree itself remains unchanged.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_attempt_forensics_acceptance_generation2
    as forensics_acceptance,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-failed-attempt-preservation-contract.v1"
)
RECEIPT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-baseline-failed-attempt-preservation-receipt.v1"
)

ROOT = Path(
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2/generation2/pair-03"
)
FAILED_ARM = ROOT / "baseline"
ARCHIVE_PARENT = ROOT / "failed-attempts"
ARCHIVE_NAME = "baseline-20260918T233630Z-98773549"
ARCHIVE_ROOT = ARCHIVE_PARENT / ARCHIVE_NAME
RUN_REL = Path(
    "runs/warmstart-apollyon-vs-abaddon-20260918T233630Z-feinter-s1990061685"
)
WARM_REL = RUN_REL / "warm-start.jsonl"
WARM_SHA256 = (
    "88e36aad38a92269046e3439fb6e94c5918395f93e5147f15a6c0f6dcf244f28"
)
WARM_BYTES = 223319
FORENSICS_SHA256 = (
    "98773549a75d9567202879b49db1e6e1afaaa2cae38b8c7077882bc6e4949d6d"
)
CONFIRM_TOKEN = (
    "VOID_ABADDON_GENERATION2_V2R13_PRESERVE_FAILED_PAIR03_BASELINE_98773549"
)
PRESERVATION_RECEIPT = (
    ARCHIVE_PARENT / f"{ARCHIVE_NAME}-preservation-receipt.json"
)

NEXT_GATE = "V2R13_PAIR03_BASELINE_RETRY_AUTHORIZATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair03_baseline_retry_authorization"


class V2R13Pair03BaselineFailedAttemptPreservationHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03BaselineFailedAttemptPreservationHold(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


def _file_sha256(path: Path) -> str:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        before = os.fstat(fd)
        _require(stat.S_ISREG(before.st_mode), "warm-start artifact is not regular")
        _require(before.st_size == WARM_BYTES, "warm-start byte count drift")
        digest = hashlib.sha256()
        total = 0
        while True:
            chunk = os.read(fd, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            _require(total <= WARM_BYTES, "warm-start grew during hash")
            digest.update(chunk)
        after = os.fstat(fd)
        _require(total == WARM_BYTES, "warm-start byte count changed")
        _require(
            (
                before.st_dev,
                before.st_ino,
                before.st_mode,
                before.st_size,
                before.st_mtime_ns,
                before.st_ctime_ns,
            )
            == (
                after.st_dev,
                after.st_ino,
                after.st_mode,
                after.st_size,
                after.st_mtime_ns,
                after.st_ctime_ns,
            ),
            "warm-start generation changed during hash",
        )
        return digest.hexdigest()
    finally:
        os.close(fd)


def _exact_failed_tree(root: Path) -> None:
    _require(root.is_dir() and not root.is_symlink(), "failed arm root invalid")
    expected = {
        Path("."),
        Path("runs"),
        RUN_REL,
        WARM_REL,
    }
    actual = {Path(".")}
    for path in root.rglob("*"):
        actual.add(path.relative_to(root))
    _require(actual == expected, "failed arm tree drift")
    _require((root / "runs").is_dir(), "runs directory missing")
    _require(not (root / "runs").is_symlink(), "runs directory symlinked")
    _require((root / RUN_REL).is_dir(), "failed run directory missing")
    _require(not (root / RUN_REL).is_symlink(), "failed run directory symlinked")
    _require((root / WARM_REL).is_file(), "warm-start artifact missing")
    _require(not (root / WARM_REL).is_symlink(), "warm-start artifact symlinked")


def _identity(path: Path) -> tuple[int, int]:
    st = path.lstat()
    return int(st.st_dev), int(st.st_ino)


def _write_receipt(receipt: Mapping[str, Any]) -> None:
    _require(
        PRESERVATION_RECEIPT.exists() is False,
        "preservation receipt already exists",
    )
    raw = (
        json.dumps(
            receipt,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")
    fd = os.open(
        PRESERVATION_RECEIPT,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
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


def preserve_failed_pair03_baseline(*, confirm: str) -> dict[str, Any]:
    _require(confirm == CONFIRM_TOKEN, "FAILED_ATTEMPT_PRESERVATION_CONFIRMATION_REQUIRED")

    accepted = (
        forensics_acceptance
        .v2r13_pair03_baseline_failed_attempt_forensics_acceptance_contract()
    )
    _require(
        accepted.get("failed_attempt_forensics_accepted") is True,
        "failed-attempt forensics not accepted",
    )
    _require(
        accepted.get("forensics_sha256") == FORENSICS_SHA256,
        "failed-attempt forensic identity drift",
    )
    _require(
        accepted.get("retry_authorized") is False,
        "forensic acceptance unexpectedly authorizes retry",
    )

    _require(FAILED_ARM.exists(), "failed arm root missing")
    _require(ARCHIVE_ROOT.exists() is False, "archive destination already exists")
    _require(
        PRESERVATION_RECEIPT.exists() is False,
        "preservation receipt already exists",
    )
    _exact_failed_tree(FAILED_ARM)

    warm_before = FAILED_ARM / WARM_REL
    _require(_file_sha256(warm_before) == WARM_SHA256, "warm-start SHA-256 drift")
    arm_identity_before = _identity(FAILED_ARM)
    warm_identity_before = _identity(warm_before)

    ARCHIVE_PARENT.mkdir(parents=False, exist_ok=True)
    _require(
        ARCHIVE_PARENT.is_dir() and not ARCHIVE_PARENT.is_symlink(),
        "archive parent invalid",
    )

    os.rename(FAILED_ARM, ARCHIVE_ROOT)

    _require(FAILED_ARM.exists() is False, "failed arm path remained after archive")
    _exact_failed_tree(ARCHIVE_ROOT)
    warm_after = ARCHIVE_ROOT / WARM_REL
    _require(_file_sha256(warm_after) == WARM_SHA256, "archived warm-start SHA drift")
    _require(
        _identity(ARCHIVE_ROOT) == arm_identity_before,
        "archive root inode identity changed",
    )
    _require(
        _identity(warm_after) == warm_identity_before,
        "warm-start inode identity changed",
    )

    body = {
        "schema": RECEIPT_SCHEMA,
        "pair_slot": 3,
        "arm": "baseline",
        "forensics_sha256": FORENSICS_SHA256,
        "source_path": str(FAILED_ARM),
        "archive_path": str(ARCHIVE_ROOT),
        "archive_name": ARCHIVE_NAME,
        "warm_start_relative_path": str(WARM_REL),
        "warm_start_sha256": WARM_SHA256,
        "warm_start_bytes": WARM_BYTES,
        "atomic_rename_performed": True,
        "source_path_absent_after_preservation": True,
        "archive_path_present_after_preservation": True,
        "arm_root_inode_preserved": True,
        "warm_start_inode_preserved": True,
        "archived_tree_unchanged": True,
        "failed_attempt_deleted": False,
        "runtime_retry_performed": False,
        "runtime_retry_authorized": False,
        "runtime_start_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }
    receipt = {**body, "preservation_receipt_sha256": _digest(body)}
    _write_receipt(receipt)
    return receipt


def v2r13_pair03_baseline_failed_attempt_preservation_contract() -> dict[str, Any]:
    accepted = (
        forensics_acceptance
        .v2r13_pair03_baseline_failed_attempt_forensics_acceptance_contract()
    )
    return {
        "schema": CONTRACT_SCHEMA,
        "forensics_sha256": FORENSICS_SHA256,
        "confirm_token": CONFIRM_TOKEN,
        "failed_arm_path": str(FAILED_ARM),
        "archive_parent": str(ARCHIVE_PARENT),
        "archive_name": ARCHIVE_NAME,
        "archive_path": str(ARCHIVE_ROOT),
        "preservation_receipt_path": str(PRESERVATION_RECEIPT),
        "warm_start_sha256": WARM_SHA256,
        "warm_start_bytes": WARM_BYTES,
        "exact_failed_tree_required": True,
        "atomic_same_filesystem_rename_implemented": True,
        "inode_identity_preservation_checked": True,
        "archived_tree_mutation_after_rename": False,
        "failed_attempt_deletion_implemented": False,
        "runtime_retry_implemented_by_this_source": False,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "runtime_start_implemented": False,
        "model_inference_implemented": False,
        "game_execution_implemented": False,
        "training_implemented": False,
        "weights_update_implemented": False,
        "automatic_policy_promotion_implemented": False,
        "deployment_implemented": False,
        "void_chain_mutation_implemented": False,
        "wallet_or_funds_action_implemented": False,
        "next_gate": "V2R13_PAIR03_BASELINE_FAILED_ATTEMPT_PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
        "next_change_class": (
            "source_only_v2r13_pair03_baseline_failed_attempt_preservation_review"
        ),
        "accepted_forensics": accepted,
    }


def authorize_retry(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03BaselineFailedAttemptPreservationHold(
        "V2R13_PAIR03_BASELINE_RETRY_NOT_YET_AUTHORIZED"
    )
