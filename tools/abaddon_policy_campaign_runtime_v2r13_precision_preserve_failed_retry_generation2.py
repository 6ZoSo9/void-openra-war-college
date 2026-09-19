#!/usr/bin/env python3
"""Preserve the exact consumed V2R13 pair-03 baseline retry."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_retry_preservation_generation2
    as contract,
)

MARK = "VOID_ABADDON_GENERATION2_V2R13_PRESERVE_FAILED_RETRY1_PAIR03_V1"

PAIR_ROOT = Path(contract.FAILED_RETRY_ARM_PATH).parent
SOURCE = Path(contract.FAILED_RETRY_ARM_PATH)
DEST = Path(contract.RETRY_ARCHIVE_PATH)
RECEIPT = Path(contract.RETRY_PRESERVATION_RECEIPT_PATH)

RETRY_RUN_REL = Path(
    "runs/warmstart-apollyon-vs-abaddon-20260919T121144Z-feinter-s1990061685"
)
RETRY_WARM_REL = RETRY_RUN_REL / "warm-start.jsonl"
ORIGINAL_ARCHIVE = Path(contract.ORIGINAL_ARCHIVE_PATH)
ORIGINAL_WARM_REL = Path(
    "runs/warmstart-apollyon-vs-abaddon-20260918T233630Z-feinter-s1990061685/"
    "warm-start.jsonl"
)
ORIGINAL_RECEIPT = (
    ORIGINAL_ARCHIVE.parent
    / "baseline-20260918T233630Z-98773549-preservation-receipt.json"
)

CONFIRM_TOKEN = (
    "VOID_ABADDON_GENERATION2_V2R13_PRESERVE_FAILED_RETRY1_PAIR03_71E90FDC"
)


class Hold(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Hold(message)


def file_sha256(path: Path, expected_size: int | None = None) -> str:
    require(path.is_file() and not path.is_symlink(), f"invalid file: {path}")
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), f"not regular file: {path}")
    if expected_size is not None:
        require(st.st_size == expected_size, f"file size drift: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact_retry_tree(root: Path) -> None:
    require(root.is_dir() and not root.is_symlink(), "failed retry root invalid")
    expected = {
        Path("."),
        Path("runs"),
        RETRY_RUN_REL,
        RETRY_WARM_REL,
    }
    actual = {Path(".")}
    for path in root.rglob("*"):
        actual.add(path.relative_to(root))
    require(actual == expected, "failed retry tree drift")


def inode(path: Path) -> tuple[int, int]:
    st = path.lstat()
    return int(st.st_dev), int(st.st_ino)


def verify_original_archive() -> None:
    require(ORIGINAL_ARCHIVE.is_dir(), "original archive missing")
    require(not ORIGINAL_ARCHIVE.is_symlink(), "original archive symlinked")
    warm = ORIGINAL_ARCHIVE / ORIGINAL_WARM_REL
    require(
        file_sha256(warm, contract.FAILED_RETRY_WARM_START_BYTES)
        == contract.ORIGINAL_WARM_START_SHA256,
        "original warm-start SHA drift",
    )
    require(
        file_sha256(ORIGINAL_RECEIPT)
        == contract.ORIGINAL_PRESERVATION_RECEIPT_FILE_SHA256,
        "original preservation receipt SHA drift",
    )


def preserve(confirm: str) -> dict:
    require(confirm == CONFIRM_TOKEN, "PRESERVATION_CONFIRMATION_REQUIRED")

    c = contract.v2r13_pair03_baseline_failed_retry_preservation_contract()
    require(c["additional_retry_authorized"] is False, "unexpected retry authority")
    require(c["preservation_implemented"] is False, "contract implementation drift")

    verify_original_archive()
    exact_retry_tree(SOURCE)
    require(not DEST.exists(), "retry archive destination already exists")
    require(not RECEIPT.exists(), "retry preservation receipt already exists")
    require(DEST.parent.is_dir(), "retry archive parent missing")
    require(not DEST.parent.is_symlink(), "retry archive parent symlinked")

    warm_before = SOURCE / RETRY_WARM_REL
    require(
        file_sha256(warm_before, contract.FAILED_RETRY_WARM_START_BYTES)
        == contract.FAILED_RETRY_WARM_START_SHA256,
        "retry warm-start SHA drift",
    )
    root_inode = inode(SOURCE)
    warm_inode = inode(warm_before)

    os.rename(SOURCE, DEST)

    require(not SOURCE.exists(), "source path remained after preservation")
    exact_retry_tree(DEST)
    warm_after = DEST / RETRY_WARM_REL
    require(
        file_sha256(warm_after, contract.FAILED_RETRY_WARM_START_BYTES)
        == contract.FAILED_RETRY_WARM_START_SHA256,
        "archived retry warm-start SHA drift",
    )
    require(inode(DEST) == root_inode, "archive root inode changed")
    require(inode(warm_after) == warm_inode, "retry warm-start inode changed")
    verify_original_archive()

    body = {
        "schema": (
            "void.abaddon.generation2."
            "v2r13-pair03-baseline-failed-retry-preservation-receipt.v1"
        ),
        "pair_slot": 3,
        "arm": "baseline",
        "retry_index": 1,
        "failed_retry_forensics_sha256": contract.FAILED_RETRY_FORENSICS_SHA256,
        "source_path": str(SOURCE),
        "archive_path": str(DEST),
        "retry_warm_start_sha256": contract.FAILED_RETRY_WARM_START_SHA256,
        "retry_warm_start_bytes": contract.FAILED_RETRY_WARM_START_BYTES,
        "atomic_rename_performed": True,
        "source_path_absent_after_preservation": True,
        "archive_path_present_after_preservation": True,
        "archive_root_inode_preserved": True,
        "retry_warm_start_inode_preserved": True,
        "archived_retry_tree_unchanged": True,
        "original_first_attempt_archive_preserved": True,
        "original_warm_start_sha256": contract.ORIGINAL_WARM_START_SHA256,
        "original_preservation_receipt_file_sha256": (
            contract.ORIGINAL_PRESERVATION_RECEIPT_FILE_SHA256
        ),
        "failed_retry_deleted": False,
        "additional_retry_authorized": False,
        "additional_retry_performed": False,
        "runtime_start_performed": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "next_gate": (
            "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_AUTHORIZATION_REQUIRED"
        ),
    }
    semantic_sha = hashlib.sha256(
        json.dumps(
            body,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()
    receipt = {**body, "preservation_receipt_sha256": semantic_sha}

    raw = (json.dumps(receipt, sort_keys=True, indent=2) + "\n").encode("utf-8")
    fd = os.open(RECEIPT, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
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

    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--confirm", required=True)
    args = parser.parse_args(argv)

    print(MARK)
    print("operation=failed_retry_preservation_only")
    print("atomic_rename=true")
    print("failed_retry_delete=false")
    print("additional_retry_authorized=false")
    print("additional_retry=false")
    print("runtime_start=false")
    print("model_load=false")
    print("model_inference=false")
    print("game_execution=false")
    print("training=false")
    print("deployment=false")
    print("void_chain_mutation=false")
    print("wallet_or_funds_action=false")

    try:
        receipt = preserve(args.confirm)
    except Exception as error:
        print(f"{MARK}_HOLD", file=sys.stderr)
        print(f"blocker={type(error).__name__}:{error}", file=sys.stderr)
        return 2

    print(
        "preservation_receipt_json="
        + json.dumps(receipt, sort_keys=True, separators=(",", ":"))
    )
    print(f"preservation_receipt_sha256={receipt['preservation_receipt_sha256']}")
    print(f"next_gate={receipt['next_gate']}")
    print(f"{MARK}_GREEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
