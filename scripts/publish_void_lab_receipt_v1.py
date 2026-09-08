#!/usr/bin/env python3
"""Create and publish one exact War College checkout receipt by retained descriptor."""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path
from typing import Callable, TextIO


SLOT = re.compile(r"slot-(?:0[1-9]|1[0-6])")
AT_EMPTY_PATH = 0x1000
MAX_RECEIPT_BYTES = 4 * 1024 * 1024
CutHook = Callable[[str, int], None]


class ReceiptHold(RuntimeError):
    """Fail-closed receipt publication terminal."""


def _fstat_regular_0600(descriptor: int) -> os.stat_result:
    result = os.fstat(descriptor)
    if not stat.S_ISREG(result.st_mode) or stat.S_IMODE(result.st_mode) != 0o600:
        raise ReceiptHold("HOLD_VOID_LAB_RECEIPT_DESCRIPTOR_MODE")
    return result


def _assert_staging_identity(
    directory_descriptor: int,
    staging_name: str,
    witness: os.stat_result,
) -> None:
    try:
        current = os.stat(
            staging_name,
            dir_fd=directory_descriptor,
            follow_symlinks=False,
        )
    except FileNotFoundError as error:
        raise ReceiptHold("HOLD_VOID_LAB_RECEIPT_STAGING_IDENTITY") from error
    if (
        not stat.S_ISREG(current.st_mode)
        or stat.S_IMODE(current.st_mode) != 0o600
        or (current.st_dev, current.st_ino) != (witness.st_dev, witness.st_ino)
    ):
        raise ReceiptHold("HOLD_VOID_LAB_RECEIPT_STAGING_IDENTITY")


def _read_descriptor(descriptor: int) -> bytes:
    os.lseek(descriptor, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    size = 0
    while True:
        chunk = os.read(descriptor, 65536)
        if not chunk:
            break
        size += len(chunk)
        if size > MAX_RECEIPT_BYTES:
            raise ReceiptHold("HOLD_VOID_LAB_RECEIPT_SIZE")
        chunks.append(chunk)
    return b"".join(chunks)


def _validate_receipt(payload: bytes) -> None:
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReceiptHold("HOLD_VOID_LAB_RECEIPT_SCHEMA") from error
    required = {
        "schema_version": 6,
        "generation": "ad1926569b12466c",
        "source_contract": "GREEN",
        "checkout_contract": "GREEN",
        "exact_checkout_evidence": True,
        "runtime_evidence": "PENDING_DESIGNATED_HOST",
    }
    if not isinstance(value, dict) or any(value.get(key) != expected for key, expected in required.items()):
        raise ReceiptHold("HOLD_VOID_LAB_RECEIPT_SCHEMA")


def _link_descriptor_create_only(
    descriptor: int,
    directory_descriptor: int,
    destination_name: str,
) -> None:
    library = ctypes.CDLL(None, use_errno=True)
    linkat = library.linkat
    linkat.argtypes = (
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
    )
    linkat.restype = ctypes.c_int
    if linkat(
        descriptor,
        b"",
        directory_descriptor,
        os.fsencode(destination_name),
        AT_EMPTY_PATH,
    ) != 0:
        error_number = ctypes.get_errno()
        raise OSError(error_number, os.strerror(error_number), destination_name)


def _run_cut(cut_hook: CutHook | None, stage: str, descriptor: int) -> None:
    if cut_hook is not None:
        cut_hook(stage, descriptor)


def publish_receipt(
    repository: Path,
    slot: str,
    *,
    cut_hook: CutHook | None = None,
    output: TextIO = sys.stdout,
    errors: TextIO = sys.stderr,
) -> int:
    if SLOT.fullmatch(slot) is None:
        print("HOLD_VOID_LAB_RECEIPT_SLOTS_EXHAUSTED", file=errors)
        return 72

    repository = Path(repository).resolve(strict=True)
    verifier = repository / "scripts" / "verify_void_lab_checkout_v1.py"
    receipt_directory = repository.parent
    staging_name = f".void-lab-checkout-{slot}.pending"
    final_name = f"void-lab-checkout-c164a7d2-{slot}.json"
    staging_path = receipt_directory / staging_name
    final_path = receipt_directory / final_name
    directory_descriptor = -1
    staging_descriptor = -1
    staging_created = False

    try:
        directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC
        if hasattr(os, "O_NOFOLLOW"):
            directory_flags |= os.O_NOFOLLOW
        directory_descriptor = os.open(receipt_directory, directory_flags)
        staging_flags = os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC
        if hasattr(os, "O_NOFOLLOW"):
            staging_flags |= os.O_NOFOLLOW
        staging_descriptor = os.open(
            staging_name,
            staging_flags,
            0o600,
            dir_fd=directory_descriptor,
        )
        staging_created = True

        completed = subprocess.run(
            [
                sys.executable,
                str(verifier),
                "--repo-root",
                str(repository),
            ],
            stdout=staging_descriptor,
            check=False,
        )
        if completed.returncode != 0:
            raise ReceiptHold("HOLD_VOID_LAB_CHECKOUT_VERIFIER")

        _run_cut(cut_hook, "after_verifier_exit", staging_descriptor)
        witness = _fstat_regular_0600(staging_descriptor)
        _run_cut(cut_hook, "before_identity_admission", staging_descriptor)
        _assert_staging_identity(directory_descriptor, staging_name, witness)

        os.fsync(staging_descriptor)
        witness = _fstat_regular_0600(staging_descriptor)
        _run_cut(cut_hook, "before_json_validation", staging_descriptor)
        _assert_staging_identity(directory_descriptor, staging_name, witness)
        payload = _read_descriptor(staging_descriptor)
        _validate_receipt(payload)
        digest = hashlib.sha256(payload).hexdigest()

        _run_cut(cut_hook, "before_publication", staging_descriptor)
        _assert_staging_identity(directory_descriptor, staging_name, witness)
        _link_descriptor_create_only(
            staging_descriptor,
            directory_descriptor,
            final_name,
        )
        published = os.stat(
            final_name,
            dir_fd=directory_descriptor,
            follow_symlinks=False,
        )
        retained = _fstat_regular_0600(staging_descriptor)
        if (
            not stat.S_ISREG(published.st_mode)
            or stat.S_IMODE(published.st_mode) != 0o600
            or (published.st_dev, published.st_ino)
            != (retained.st_dev, retained.st_ino)
        ):
            raise ReceiptHold("HOLD_VOID_LAB_RECEIPT_FINAL_IDENTITY")
        os.fsync(directory_descriptor)
        published_after_sync = os.stat(
            final_name,
            dir_fd=directory_descriptor,
            follow_symlinks=False,
        )
        if (
            published_after_sync.st_dev,
            published_after_sync.st_ino,
        ) != (retained.st_dev, retained.st_ino):
            raise ReceiptHold("HOLD_VOID_LAB_RECEIPT_FINAL_IDENTITY")

        print(f"receipt_id={slot}", file=output)
        print(f"receipt_path={final_path}", file=output)
        print(f"{digest}  {final_path}", file=output)
        return 0
    except (OSError, ReceiptHold) as error:
        marker = str(error)
        if not marker.startswith("HOLD_"):
            marker = "HOLD_VOID_LAB_RECEIPT_PUBLICATION"
        print(marker, file=errors)
        return 1
    finally:
        if staging_created:
            print(f"receipt_staging_path={staging_path}", file=errors)
            print("pending_retired=false", file=errors)
            print("staging_cleanup=DEFERRED_NO_PATHNAME_DELETE", file=errors)
        if staging_descriptor >= 0:
            os.close(staging_descriptor)
        if directory_descriptor >= 0:
            os.close(directory_descriptor)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--slot", required=True)
    arguments = parser.parse_args()
    return publish_receipt(arguments.repo_root, arguments.slot)


if __name__ == "__main__":
    raise SystemExit(main())
