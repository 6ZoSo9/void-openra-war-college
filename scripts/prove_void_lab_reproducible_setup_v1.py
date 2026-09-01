#!/usr/bin/env python3
"""Falsify destructive or mode-ambiguous War College receipt publication."""

from __future__ import annotations

import hashlib
import os
import re
import stat
import tempfile
from pathlib import Path


MARKER = "VOID_LAB_REPRODUCIBLE_SETUP_PROOF_V1"
DOCUMENT = Path(__file__).parents[1] / "VOID_LAB_REPRODUCIBLE_SETUP_V1.md"
KNOWN_BYTES = b"preserved-prior-receipt\n"
ATTEMPT_ID = re.compile(r"[a-z0-9][a-z0-9_-]{0,63}")
RUNTIME_PATH_EXECUTED = False


def receipt_destination(root: Path, attempt_id: str) -> Path:
    if ATTEMPT_ID.fullmatch(attempt_id) is None:
        raise ValueError("invalid receipt attempt identifier")
    return root / f"void-lab-checkout-c164a7d2-{attempt_id}.json"


def publish_create_only(temp: Path, destination: Path) -> None:
    temp_stat = temp.lstat()
    if not stat.S_ISREG(temp_stat.st_mode) or stat.S_IMODE(temp_stat.st_mode) != 0o600:
        raise RuntimeError("temporary receipt must be one regular mode-0600 file")
    os.link(temp, destination, follow_symlinks=False)
    final_stat = destination.lstat()
    if (
        not stat.S_ISREG(final_stat.st_mode)
        or stat.S_IMODE(final_stat.st_mode) != 0o600
        or (final_stat.st_dev, final_stat.st_ino)
        != (temp_stat.st_dev, temp_stat.st_ino)
    ):
        raise RuntimeError("published receipt identity or mode changed")


def cleanup_owned_generation(
    path: Path,
    witness: os.stat_result,
    *,
    unlink=os.unlink,
) -> bool:
    try:
        current = path.lstat()
    except FileNotFoundError:
        return False
    if (
        stat.S_ISLNK(current.st_mode)
        or (current.st_dev, current.st_ino) != (witness.st_dev, witness.st_ino)
    ):
        return False
    try:
        unlink(path)
    except OSError:
        return False
    return True


def classify_published_receipt(destination: Path, witness: os.stat_result) -> str:
    published = destination.lstat()
    if (
        stat.S_ISREG(published.st_mode)
        and stat.S_IMODE(published.st_mode) == 0o600
        and (published.st_dev, published.st_ino)
        == (witness.st_dev, witness.st_ino)
    ):
        return "COMMITTED"
    return "HOLD"


def prove_document_contract() -> None:
    text = DOCUMENT.read_text(encoding="utf-8")
    required = (
        'void_publish_lab_receipt() (',
        'VOID_LAB_RECEIPT_ID="$1"',
        '[a-z0-9][a-z0-9_-]{0,63}',
        'void-lab-checkout-c164a7d2-$VOID_LAB_RECEIPT_ID.json',
        'test ! -e "$VOID_LAB_RECEIPT"',
        'test ! -L "$VOID_LAB_RECEIPT"',
        'mktemp "$VOID_LAB_RECEIPT_DIR/.void-lab-checkout.XXXXXX"',
        'VOID_LAB_RECEIPT_TEMP_ID="$(stat -c \'%d:%i\' "$VOID_LAB_RECEIPT_TEMP")"',
        'cleanup_owned_temp() {',
        'stat -c \'%a\' "$VOID_LAB_RECEIPT_TEMP"',
        'ln -- "$VOID_LAB_RECEIPT_TEMP" "$VOID_LAB_RECEIPT"',
        'stat -c \'%d:%i\' "$VOID_LAB_RECEIPT"',
        'cleanup_owned_temp',
        'sync -f "$VOID_LAB_RECEIPT_DIR"',
        'void_publish_lab_receipt setup-001',
        'void_publish_lab_receipt prebuild-001',
    )
    for fragment in required:
        if fragment not in text:
            raise RuntimeError(f"documentation omits receipt guard: {fragment}")
    if '> "$VOID_LAB_RECEIPT"' in text:
        raise RuntimeError("documentation directly redirects over final receipt")


def prove_existing_receipt_is_unchanged() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        destination = root / "receipt.json"
        destination.write_bytes(KNOWN_BYTES)
        destination.chmod(0o644)
        before = destination.lstat()
        temp = root / ".candidate"
        temp.write_bytes(b"replacement\n")
        temp.chmod(0o600)
        try:
            publish_create_only(temp, destination)
        except FileExistsError:
            pass
        else:
            raise RuntimeError("pre-existing receipt was not rejected")
        after = destination.lstat()
        if destination.read_bytes() != KNOWN_BYTES:
            raise RuntimeError("pre-existing receipt bytes changed")
        if (after.st_dev, after.st_ino) != (before.st_dev, before.st_ino):
            raise RuntimeError("pre-existing receipt identity changed")
        if stat.S_IMODE(after.st_mode) != 0o644:
            raise RuntimeError("pre-existing receipt mode changed")


def prove_absent_path_publishes_mode_0600() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        destination = root / "receipt.json"
        temp = root / ".candidate"
        temp.write_bytes(b"validated\n")
        temp.chmod(0o600)
        publish_create_only(temp, destination)
        published = destination.lstat()
        candidate = temp.lstat()
        if destination.read_bytes() != b"validated\n":
            raise RuntimeError("published receipt bytes changed")
        if stat.S_IMODE(published.st_mode) != 0o600:
            raise RuntimeError("published receipt is not mode 0600")
        if (published.st_dev, published.st_ino) != (
            candidate.st_dev,
            candidate.st_ino,
        ):
            raise RuntimeError("publication did not retain exact candidate identity")


def prove_repeat_verification_preserves_both_receipts() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        first = receipt_destination(root, "setup-001")
        second = receipt_destination(root, "prebuild-001")
        first_temp = root / ".first-candidate"
        second_temp = root / ".second-candidate"
        first_temp.write_bytes(b'{"attempt":"setup-001"}\n')
        second_temp.write_bytes(b'{"attempt":"prebuild-001"}\n')
        first_temp.chmod(0o600)
        second_temp.chmod(0o600)

        publish_create_only(first_temp, first)
        first_before = first.lstat()
        first_bytes = first.read_bytes()
        first_digest = hashlib.sha256(first_bytes).hexdigest()

        publish_create_only(second_temp, second)
        first_after = first.lstat()
        second_stat = second.lstat()
        second_bytes = second.read_bytes()
        second_digest = hashlib.sha256(second_bytes).hexdigest()

        if first.read_bytes() != first_bytes:
            raise RuntimeError("repeat verification changed the first receipt bytes")
        if (first_after.st_dev, first_after.st_ino) != (
            first_before.st_dev,
            first_before.st_ino,
        ):
            raise RuntimeError("repeat verification changed the first receipt identity")
        if stat.S_IMODE(first_after.st_mode) != 0o600:
            raise RuntimeError("repeat verification changed the first receipt mode")
        if (
            not stat.S_ISREG(second_stat.st_mode)
            or stat.S_IMODE(second_stat.st_mode) != 0o600
        ):
            raise RuntimeError("second receipt is not one regular mode-0600 file")
        if (first_after.st_dev, first_after.st_ino) == (
            second_stat.st_dev,
            second_stat.st_ino,
        ):
            raise RuntimeError("repeat verification reused the first receipt identity")
        if first_digest == second_digest:
            raise RuntimeError("repeat verification did not bind a distinct receipt digest")
        if RUNTIME_PATH_EXECUTED:
            raise RuntimeError("source-only proof reached a runtime path")


def prove_postpublication_cleanup_is_terminal_monotone() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        destination = root / "receipt.json"
        temp = root / ".candidate"
        temp.write_bytes(b"validated\n")
        temp.chmod(0o600)
        witness = temp.lstat()
        publish_create_only(temp, destination)

        temp.unlink()
        temp.write_bytes(b"foreign-generation\n")
        temp.chmod(0o600)
        foreign_before = temp.lstat()
        if cleanup_owned_generation(temp, witness):
            raise RuntimeError("replacement generation was reported as cleaned")
        foreign_after = temp.lstat()
        if temp.read_bytes() != b"foreign-generation\n":
            raise RuntimeError("replacement generation bytes changed")
        if (foreign_after.st_dev, foreign_after.st_ino) != (
            foreign_before.st_dev,
            foreign_before.st_ino,
        ):
            raise RuntimeError("replacement generation identity changed")
        if classify_published_receipt(destination, witness) != "COMMITTED":
            raise RuntimeError("replacement cleanup changed committed terminal")

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        destination = root / "receipt.json"
        temp = root / ".candidate"
        temp.write_bytes(b"validated\n")
        temp.chmod(0o600)
        witness = temp.lstat()
        publish_create_only(temp, destination)

        def fail_unlink(_: os.PathLike[str] | str) -> None:
            raise PermissionError("injected cleanup failure")

        if cleanup_owned_generation(temp, witness, unlink=fail_unlink):
            raise RuntimeError("injected cleanup failure was reported as cleaned")
        if classify_published_receipt(destination, witness) != "COMMITTED":
            raise RuntimeError("cleanup failure reversed committed terminal")
        if destination.read_bytes() != b"validated\n":
            raise RuntimeError("cleanup failure changed committed receipt bytes")


def main() -> int:
    prove_document_contract()
    prove_existing_receipt_is_unchanged()
    prove_absent_path_publishes_mode_0600()
    prove_repeat_verification_preserves_both_receipts()
    prove_postpublication_cleanup_is_terminal_monotone()
    print(f"{MARKER} PASS")
    print("preexisting_receipt_unchanged=true")
    print("absent_path_mode_0600=true")
    print("repeat_verification_distinct_receipts=true")
    print("prior_receipt_preserved=true")
    print("replacement_generation_preserved=true")
    print("cleanup_failure_terminal=COMMITTED")
    print("runtime_path_executed=false")
    print("runtime_evidence=PENDING_DESIGNATED_HOST")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
