#!/usr/bin/env python3
"""Falsify destructive or mode-ambiguous War College receipt publication."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path


MARKER = "VOID_LAB_REPRODUCIBLE_SETUP_PROOF_V1"
DOCUMENT = Path(__file__).parents[1] / "VOID_LAB_REPRODUCIBLE_SETUP_V1.md"
KNOWN_BYTES = b"preserved-prior-receipt\n"
ATTEMPT_ID = re.compile(r"slot-(?:0[1-9]|1[0-6])")
RUNTIME_PATH_EXECUTED = False
REQUIRED_HOST_COMMANDS = (
    "uname",
    "python3",
    "git",
    "awk",
    "dirname",
    "ln",
    "mktemp",
    "rm",
    "sha256sum",
    "stat",
    "sync",
)


def receipt_destination(root: Path, attempt_id: str) -> Path:
    if ATTEMPT_ID.fullmatch(attempt_id) is None:
        raise ValueError("invalid receipt slot identifier")
    return root / f"void-lab-checkout-c164a7d2-{attempt_id}.json"


def staging_destination(root: Path, attempt_id: str) -> Path:
    if ATTEMPT_ID.fullmatch(attempt_id) is None:
        raise ValueError("invalid receipt slot identifier")
    return root / f".void-lab-checkout-{attempt_id}.pending"


def write_staging_create_only(path: Path, payload: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())


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


def classify_staging_alias(path: Path, witness: os.stat_result) -> str:
    try:
        current = path.lstat()
    except FileNotFoundError:
        return "ABSENT"
    if (
        stat.S_ISLNK(current.st_mode)
        or not stat.S_ISREG(current.st_mode)
        or stat.S_IMODE(current.st_mode) != 0o600
        or (current.st_dev, current.st_ino) != (witness.st_dev, witness.st_ino)
    ):
        return "DEFERRED_FOREIGN"
    return "DEFERRED_OWNED"

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
        '# VOID_LAB_HOST_PREFLIGHT_V1_BEGIN',
        'void_require_lab_setup_host() (',
        'for command in uname python3 git awk dirname ln mktemp rm sha256sum stat sync; do',
        "test \"$(uname -s)\" = 'Linux'",
        'mktemp -d "${TMPDIR:-/tmp}/void-lab-prereq.XXXXXX"',
        'ln -- "$VOID_LAB_PREFLIGHT_DIR/source" "$VOID_LAB_PREFLIGHT_DIR/link"',
        "stat -c '%d:%i' \"$VOID_LAB_PREFLIGHT_DIR/source\"",
        'sync -f "$VOID_LAB_PREFLIGHT_DIR"',
        'HOLD_VOID_LAB_SETUP_HOST_PREREQUISITES',
        '# VOID_LAB_HOST_PREFLIGHT_V1_END',
        'void_publish_lab_receipt() (',
        'VOID_LAB_RECEIPT_ID="$1"',
        'slot-(?:0[1-9]|1[0-6])',
        'HOLD_VOID_LAB_RECEIPT_SLOTS_EXHAUSTED',
        'void-lab-checkout-c164a7d2-$VOID_LAB_RECEIPT_ID.json',
        'test ! -e "$VOID_LAB_RECEIPT"',
        'test ! -L "$VOID_LAB_RECEIPT"',
        'VOID_LAB_RECEIPT_TEMP="$VOID_LAB_RECEIPT_DIR/.void-lab-checkout-$VOID_LAB_RECEIPT_ID.pending"',
        'test ! -e "$VOID_LAB_RECEIPT_TEMP"',
        'set -C',
        'VOID_LAB_RECEIPT_TEMP_ID="$(stat -c \'%d:%i\' "$VOID_LAB_RECEIPT_TEMP")"',
        'report_retained_temp() {',
        'pending_retired=false',
        'staging_cleanup=DEFERRED_NO_PATHNAME_DELETE',
        'trap report_retained_temp EXIT',
        'stat -c \'%a\' "$VOID_LAB_RECEIPT_TEMP"',
        'ln -- "$VOID_LAB_RECEIPT_TEMP" "$VOID_LAB_RECEIPT"',
        'stat -c \'%d:%i\' "$VOID_LAB_RECEIPT"',
        'sync -f "$VOID_LAB_RECEIPT_DIR"',
        'void_publish_lab_receipt slot-01',
        'void_publish_lab_receipt slot-02',
    )
    for fragment in required:
        if fragment not in text:
            raise RuntimeError(f"documentation omits receipt guard: {fragment}")
    if '> "$VOID_LAB_RECEIPT"' in text:
        raise RuntimeError("documentation directly redirects over final receipt")
    receipt_shell = documented_receipt_shell()
    if 'rm ' in receipt_shell or "cleanup_owned_temp" in receipt_shell:
        raise RuntimeError("documented receipt shell retains pathname cleanup authority")
    if "mktemp " in receipt_shell:
        raise RuntimeError("documented receipt shell permits unbounded random staging aliases")


def documented_host_preflight() -> str:
    text = DOCUMENT.read_text(encoding="utf-8")
    begin = "# VOID_LAB_HOST_PREFLIGHT_V1_BEGIN"
    end = "# VOID_LAB_HOST_PREFLIGHT_V1_END"
    start = text.index(begin)
    finish = text.index(end, start) + len(end)
    return text[start:finish] + "\n"


def documented_receipt_shell() -> str:
    text = DOCUMENT.read_text(encoding="utf-8")
    begin = "void_publish_lab_receipt() ("
    end = "void_publish_lab_receipt slot-01"
    start = text.index(begin)
    finish = text.index(end, start) + len(end)
    return text[start:finish] + "\n"


def prove_documented_receipt_shell_syntax() -> None:
    source = documented_receipt_shell()
    control = subprocess.run(
        ["/bin/dash", "-n"],
        input=source,
        text=True,
        capture_output=True,
        check=False,
    )
    if control.returncode != 0:
        raise RuntimeError(
            f"documented receipt shell has invalid dash syntax: {control.stderr}"
        )

    closing = "\n)\nvoid_publish_lab_receipt slot-01"
    if closing not in source:
        raise RuntimeError("receipt shell extraction omitted its exact function close")
    mutant = source.replace(
        closing,
        "\nvoid_publish_lab_receipt slot-01",
        1,
    )
    rejected = subprocess.run(
        ["/bin/dash", "-n"],
        input=mutant,
        text=True,
        capture_output=True,
        check=False,
    )
    if rejected.returncode == 0:
        raise RuntimeError("receipt shell syntax-deletion mutant was accepted")


def run_documented_receipt_shell(root: Path, slot: str) -> subprocess.CompletedProcess[str]:
    repository = root / "checkout"
    scripts = repository / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    verifier = scripts / "verify_void_lab_checkout_v1.py"
    verifier.write_text(
        "print('{\"schema_version\":6,\"generation\":\"ad1926569b12466c\","
        "\"source_contract\":\"GREEN\",\"checkout_contract\":\"GREEN\","
        "\"exact_checkout_evidence\":true,"
        "\"runtime_evidence\":\"PENDING_DESIGNATED_HOST\"}')\n",
        encoding="utf-8",
    )
    source = documented_receipt_shell()
    source = source.replace(
        "void_publish_lab_receipt slot-01",
        f"void_publish_lab_receipt {slot}",
        1,
    )
    environment = dict(os.environ)
    environment["VOID_WAR_COLLEGE_DIR"] = str(repository)
    return subprocess.run(
        ["/bin/dash"],
        input=source,
        text=True,
        capture_output=True,
        env=environment,
        check=False,
    )


def prove_documented_receipt_shell_execution() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        control = run_documented_receipt_shell(root, "slot-01")
        if control.returncode != 0:
            raise RuntimeError(
                f"documented receipt shell control failed: {control.returncode}: "
                f"{control.stderr}"
            )
        staging = root / ".void-lab-checkout-slot-01.pending"
        final = root / "void-lab-checkout-c164a7d2-slot-01.json"
        staged = staging.lstat()
        published = final.lstat()
        if (
            not stat.S_ISREG(staged.st_mode)
            or not stat.S_ISREG(published.st_mode)
            or stat.S_IMODE(staged.st_mode) != 0o600
            or stat.S_IMODE(published.st_mode) != 0o600
            or (staged.st_dev, staged.st_ino)
            != (published.st_dev, published.st_ino)
        ):
            raise RuntimeError("documented shell did not publish one exact mode-0600 inode")
        if "staging_cleanup=DEFERRED_NO_PATHNAME_DELETE" not in control.stderr:
            raise RuntimeError("documented shell omitted deferred-cleanup receipt")
        staging_bytes = staging.read_bytes()
        final_bytes = final.read_bytes()
        staging_before = staging.lstat()
        final_before = final.lstat()

        reused = run_documented_receipt_shell(root, "slot-01")
        if reused.returncode == 0:
            raise RuntimeError("documented shell reused a consumed receipt slot")
        staging_after = staging.lstat()
        final_after = final.lstat()
        if staging.read_bytes() != staging_bytes or final.read_bytes() != final_bytes:
            raise RuntimeError("documented shell slot reuse changed prior bytes")
        if (staging_after.st_dev, staging_after.st_ino) != (
            staging_before.st_dev,
            staging_before.st_ino,
        ):
            raise RuntimeError("documented shell slot reuse changed staging identity")
        if (final_after.st_dev, final_after.st_ino) != (
            final_before.st_dev,
            final_before.st_ino,
        ):
            raise RuntimeError("documented shell slot reuse changed final identity")

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        invalid = run_documented_receipt_shell(root, "slot-17")
        if invalid.returncode != 72:
            raise RuntimeError(
                f"documented shell invalid slot returned {invalid.returncode}, not 72"
            )
        if "HOLD_VOID_LAB_RECEIPT_SLOTS_EXHAUSTED" not in invalid.stderr:
            raise RuntimeError("documented shell invalid slot omitted exhaustion HOLD")
        if list(root.glob("*.json")) or list(root.glob(".*.pending")):
            raise RuntimeError("invalid documented shell slot created receipt state")

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        repository = root / "checkout"
        repository.mkdir()
        foreign = root / ".void-lab-checkout-slot-01.pending"
        foreign.write_bytes(b"foreign-staging-generation\n")
        foreign.chmod(0o600)
        before = foreign.lstat()
        preserved = foreign.read_bytes()
        collision = run_documented_receipt_shell(root, "slot-01")
        if collision.returncode == 0:
            raise RuntimeError("documented shell accepted a foreign staging generation")
        after = foreign.lstat()
        if foreign.read_bytes() != preserved:
            raise RuntimeError("documented shell changed foreign staging bytes")
        if (after.st_dev, after.st_ino) != (before.st_dev, before.st_ino):
            raise RuntimeError("documented shell changed foreign staging identity")
        final = root / "void-lab-checkout-c164a7d2-slot-01.json"
        if final.exists() or final.is_symlink():
            raise RuntimeError("foreign staging collision published a final receipt")


def host_command_paths() -> dict[str, str]:
    paths: dict[str, str] = {}
    for command in REQUIRED_HOST_COMMANDS:
        resolved = shutil.which(command)
        if resolved is None:
            raise RuntimeError(f"proof host lacks required control command: {command}")
        paths[command] = resolved
    return paths


def run_host_preflight(
    root: Path,
    command_paths: dict[str, str],
    *,
    missing: str | None = None,
    substituted: str | None = None,
) -> tuple[subprocess.CompletedProcess[str], Path]:
    bin_dir = root / "bin"
    bin_dir.mkdir(parents=True)
    for command, resolved in command_paths.items():
        target = bin_dir / command
        if command == missing:
            continue
        if command == substituted:
            target.write_text("#!/bin/sh\nexit 88\n", encoding="utf-8")
            target.chmod(0o700)
        else:
            target.symlink_to(resolved)
    marker = root / "downstream-mutation"
    environment = dict(os.environ)
    environment["PATH"] = str(bin_dir)
    environment["TMPDIR"] = str(root)
    environment["VOID_LAB_MUTATION_MARKER"] = str(marker)
    script = documented_host_preflight()
    script += "printf 'mutated\\n' > \"$VOID_LAB_MUTATION_MARKER\"\n"
    result = subprocess.run(
        ["/bin/dash"],
        input=script,
        text=True,
        capture_output=True,
        env=environment,
        check=False,
    )
    return result, marker


def prove_host_preflight_fails_before_downstream_mutation() -> None:
    command_paths = host_command_paths()
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        control, marker = run_host_preflight(root / "control", command_paths)
        if control.returncode != 0 or not marker.is_file():
            raise RuntimeError(
                f"supported host control failed: {control.returncode}: {control.stderr}"
            )
    for command in REQUIRED_HOST_COMMANDS:
        for mode in ("missing", "substituted"):
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                root.mkdir(exist_ok=True)
                kwargs = {mode: command}
                result, marker = run_host_preflight(root, command_paths, **kwargs)
                if result.returncode == 0:
                    raise RuntimeError(f"{mode} {command} did not fail prerequisite wall")
                if marker.exists():
                    raise RuntimeError(
                        f"{mode} {command} reached downstream mutation marker"
                    )


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


def prove_fixed_slots_bound_staging_aliases() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for number in range(1, 17):
            slot = f"slot-{number:02d}"
            staging = staging_destination(root, slot)
            final = receipt_destination(root, slot)
            payload = f'{{"slot":"{slot}"}}\n'.encode()
            write_staging_create_only(staging, payload)
            witness = staging.lstat()
            publish_create_only(staging, final)
            if classify_staging_alias(staging, witness) != "DEFERRED_OWNED":
                raise RuntimeError(f"{slot} staging alias was not retained")
            if classify_published_receipt(final, witness) != "COMMITTED":
                raise RuntimeError(f"{slot} final receipt was not committed")

        entries = list(root.iterdir())
        if len(entries) != 32:
            raise RuntimeError("fixed slot set did not produce exactly 16 aliases and receipts")
        if any(stat.S_IMODE(path.lstat().st_mode) != 0o600 for path in entries):
            raise RuntimeError("fixed slot set contains a non-owner-only path")

        first = staging_destination(root, "slot-01")
        first_before = first.lstat()
        first_bytes = first.read_bytes()
        try:
            write_staging_create_only(first, b"replacement\n")
        except FileExistsError:
            pass
        else:
            raise RuntimeError("consumed staging slot was reusable")
        first_after = first.lstat()
        if first.read_bytes() != first_bytes:
            raise RuntimeError("staging-slot reuse changed prior bytes")
        if (first_after.st_dev, first_after.st_ino) != (
            first_before.st_dev,
            first_before.st_ino,
        ):
            raise RuntimeError("staging-slot reuse changed prior identity")

        for invalid in ("slot-00", "slot-17", "setup-001", "slot-1", "slot-001"):
            try:
                staging_destination(root, invalid)
            except ValueError:
                continue
            raise RuntimeError(f"invalid receipt slot was admitted: {invalid}")


def prove_repeat_verification_preserves_both_receipts() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        first = receipt_destination(root, "slot-01")
        second = receipt_destination(root, "slot-02")
        first_temp = root / ".first-candidate"
        second_temp = root / ".second-candidate"
        first_temp.write_bytes(b'{"attempt":"slot-01"}\n')
        second_temp.write_bytes(b'{"attempt":"slot-02"}\n')
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


def prove_postpublication_staging_retention_has_no_delete_authority() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        destination = root / "receipt.json"
        temp = root / ".candidate"
        temp.write_bytes(b"validated\n")
        temp.chmod(0o600)
        witness = temp.lstat()
        publish_create_only(temp, destination)

        if classify_staging_alias(temp, witness) != "DEFERRED_OWNED":
            raise RuntimeError("owned staging alias was not retained")
        staged = temp.lstat()
        final = destination.lstat()
        if (staged.st_dev, staged.st_ino) != (final.st_dev, final.st_ino):
            raise RuntimeError("retained staging alias lost published identity")

        # Adversarial interleaving at the former validation-to-unlink boundary:
        # observe A, replace it with B, then execute only the non-mutating
        # classification admitted by this generation.
        if classify_staging_alias(temp, witness) != "DEFERRED_OWNED":
            raise RuntimeError("pre-replacement staging observation changed")
        temp.unlink()
        temp.write_bytes(b"foreign-generation\n")
        temp.chmod(0o600)
        foreign_before = temp.lstat()
        if classify_staging_alias(temp, witness) != "DEFERRED_FOREIGN":
            raise RuntimeError("foreign staging generation was not deferred")
        foreign_after = temp.lstat()
        if temp.read_bytes() != b"foreign-generation\n":
            raise RuntimeError("foreign staging generation bytes changed")
        if (foreign_after.st_dev, foreign_after.st_ino) != (
            foreign_before.st_dev,
            foreign_before.st_ino,
        ):
            raise RuntimeError("foreign staging generation identity changed")
        if classify_published_receipt(destination, witness) != "COMMITTED":
            raise RuntimeError("foreign staging replacement changed committed terminal")

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        destination = root / "receipt.json"
        temp = root / ".candidate"
        temp.write_bytes(b"validated\n")
        temp.chmod(0o600)
        witness = temp.lstat()
        publish_create_only(temp, destination)
        temp.unlink()
        if classify_staging_alias(temp, witness) != "ABSENT":
            raise RuntimeError("missing staging alias was not classified absent")
        if classify_published_receipt(destination, witness) != "COMMITTED":
            raise RuntimeError("missing staging alias changed committed terminal")


def main() -> int:
    prove_document_contract()
    prove_documented_receipt_shell_syntax()
    prove_documented_receipt_shell_execution()
    prove_host_preflight_fails_before_downstream_mutation()
    prove_existing_receipt_is_unchanged()
    prove_absent_path_publishes_mode_0600()
    prove_fixed_slots_bound_staging_aliases()
    prove_repeat_verification_preserves_both_receipts()
    prove_postpublication_staging_retention_has_no_delete_authority()
    print(f"{MARKER} PASS")
    print("receipt_shell_dash_syntax=true")
    print("receipt_shell_syntax_mutant_rejected=true")
    print("documented_receipt_shell_execution=true")
    print("documented_receipt_slot_reuse_rejected=true")
    print("documented_receipt_invalid_slot_exit=72")
    print("documented_receipt_foreign_staging_preserved=true")
    print("host_preflight_supported_control=true")
    print(f"host_preflight_missing_command_cases={len(REQUIRED_HOST_COMMANDS)}")
    print(f"host_preflight_substituted_command_cases={len(REQUIRED_HOST_COMMANDS)}")
    print("host_preflight_downstream_mutations=0")
    print("preexisting_receipt_unchanged=true")
    print("absent_path_mode_0600=true")
    print("receipt_slot_limit=16")
    print("staging_alias_cardinality_bound=16")
    print("staging_retry_reuse_rejected=true")
    print("repeat_verification_distinct_receipts=true")
    print("prior_receipt_preserved=true")
    print("staging_alias_retained=true")
    print("replacement_at_retirement_boundary_preserved=true")
    print("staging_cleanup_authority=false")
    print("receipt_commit_terminal=COMMITTED")
    print("runtime_path_executed=false")
    print("runtime_evidence=PENDING_DESIGNATED_HOST")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
