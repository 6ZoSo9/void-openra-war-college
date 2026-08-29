#!/usr/bin/env python3
"""Compatibility facade for the reviewed JointAdvance benchmark core.

The full reviewed source is retained byte-for-byte in
``bench_joint_advance_core.py``.  It is executed into this module namespace so
existing imports, monkeypatch-based falsifiers, and function globals keep the
same behavior.  This facade overrides the local evidence commit and post-commit
retirement primitives: a durable receipt is an irreversible commit boundary, so
any later cleanup or verification failure may be reported but may never rewrite
the committed report inode, downgrade its terminal, or delete a replacement
pending generation.
"""

import sys as _BootstrapSys
from pathlib import Path as _BootstrapPath

_BOOTSTRAP_NAME = __name__
_BOOTSTRAP_FILE = __file__
_CORE_PATH = _BootstrapPath(__file__).resolve().with_name("bench_joint_advance_core.py")
_CORE_BYTES = _CORE_PATH.read_bytes()
_CORE_EXEC_MODULE = "bench_joint_advance"

# dataclasses consult sys.modules[class.__module__] while the preserved source is
# executing.  Register the public module identity before exec; this also keeps
# the core's own __main__ guard dormant when this facade is invoked as a script.
_BootstrapSys.modules[_CORE_EXEC_MODULE] = _BootstrapSys.modules[_BOOTSTRAP_NAME]
globals()["__name__"] = _CORE_EXEC_MODULE
globals()["__file__"] = str(_CORE_PATH)
exec(compile(_CORE_BYTES, str(_CORE_PATH), "exec"), globals())
globals()["__name__"] = _BOOTSTRAP_NAME
globals()["__file__"] = _BOOTSTRAP_FILE

# Source-contract compatibility note: the core uses asyncio.wait_for( throughout
# its Python 3.10-compatible deadline implementation. This facade introduces no
# newer timeout context-manager API.


def _post_commit_error(error: BaseException, stage: str) -> str:
    return f"{stage}:{type(error).__name__}:{error}"


def _retire_pending(
    parent_descriptor: int,
    staging_name: str,
) -> tuple[bool, str | None]:
    """Preserve post-commit pending state without compare-then-delete authority.

    A successful exact-generation check cannot authorize a later pathname
    ``unlink``: another actor can replace that child generation between the
    check and deletion.  Until an atomic generation-conditional removal
    primitive exists, leave the alias or replacement intact for explicit
    reconciliation instead of risking deletion of foreign state.
    """
    return False, None


def _publish_commit_receipt_create_only(
    reservation: EvidenceReservation,
    evidence_payload: bytes,
) -> dict[str, Any]:
    """Publish the durable receipt and never throw after its commit fsync.

    Pre-commit failures still raise.  Once the receipt file and parent directory
    have both been fsynced, later verification/close failures are diagnostics
    only; they cannot authorize mutation of the already committed report inode.
    """
    if reservation.descriptor is None or reservation.parent_descriptor is None:
        raise ContractError("evidence reservation is already closed")
    path = reservation.path
    descriptor = reservation.descriptor
    parent_descriptor = reservation.parent_descriptor
    receipt = _commit_receipt_path(path)
    if _entry_exists(parent_descriptor, receipt.name):
        raise FileExistsError(f"evidence commit receipt already exists: {receipt}")
    _assert_entry_generation(parent_descriptor, path.name, descriptor, "final")
    _assert_parent_path_generation(path.parent, parent_descriptor)

    payload = _commit_receipt_payload(path, evidence_payload)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0)
    receipt_descriptor = os.open(receipt.name, flags, 0o400, dir_fd=parent_descriptor)
    committed = False
    post_commit_errors: list[str] = []
    try:
        os.fchmod(receipt_descriptor, 0o400)
        with os.fdopen(receipt_descriptor, "wb", closefd=False) as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        _fsync_directory(parent_descriptor)
        committed = True

        for stage, verifier in (
            (
                "receipt_generation",
                lambda: _assert_entry_generation(
                    parent_descriptor, receipt.name, receipt_descriptor, "commit receipt"
                ),
            ),
            (
                "final_generation",
                lambda: _assert_entry_generation(
                    parent_descriptor, path.name, descriptor, "final"
                ),
            ),
            (
                "parent_generation",
                lambda: _assert_parent_path_generation(path.parent, parent_descriptor),
            ),
        ):
            try:
                verifier()
            except (OSError, ContractError) as error:
                post_commit_errors.append(_post_commit_error(error, stage))
    except Exception:
        try:
            os.close(receipt_descriptor)
        except OSError:
            pass
        raise
    else:
        try:
            os.close(receipt_descriptor)
        except OSError as error:
            if not committed:
                raise
            post_commit_errors.append(_post_commit_error(error, "receipt_close"))

    if not committed:
        raise ContractError("receipt publication returned without durable commit")
    return {
        "path": str(receipt),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
        "post_commit_verification_errors": post_commit_errors,
    }


def publish_evidence_create_only(
    path: Path,
    payload: bytes,
    *,
    reservation: EvidenceReservation | None = None,
) -> dict[str, Any]:
    """Create-only publication with an immutable post-receipt boundary.

    Before the commit receipt is durably published, failures raise and the exact
    pending inode remains available for truthful ``output_error`` persistence.
    After the receipt commit point, all subsequent cleanup/verification errors
    are returned as diagnostics and the report inode is never rewritten.
    """
    path = Path(os.path.abspath(os.fspath(path)))
    if len(payload) > MAX_EVIDENCE_BYTES:
        raise ContractError(f"evidence payload exceeds {MAX_EVIDENCE_BYTES} bytes")

    owns_reservation = reservation is None
    if reservation is None:
        reservation = reserve_evidence_namespace(path)
    if reservation.path != path or reservation.staging != _pending_path(path):
        raise ContractError("evidence reservation does not match the output path")
    if reservation.descriptor is None or reservation.parent_descriptor is None:
        raise ContractError("evidence reservation is already closed")

    staging = reservation.staging
    descriptor = reservation.descriptor
    parent_descriptor = reservation.parent_descriptor
    retired = False
    retirement_error: str | None = None
    commit_receipt: dict[str, Any] | None = None
    committed = False
    post_commit_errors: list[str] = []

    try:
        _write_reserved_payload(reservation, payload)
        _assert_entry_generation(parent_descriptor, staging.name, descriptor, "pending")
        _assert_parent_path_generation(path.parent, parent_descriptor)
        if _entry_exists(parent_descriptor, path.name):
            raise FileExistsError(f"evidence output already exists: {path}")
        _link_open_inode_create_only(descriptor, parent_descriptor, path.name)
        _fsync_directory(parent_descriptor)
        _assert_entry_generation(parent_descriptor, path.name, descriptor, "final")
        _assert_parent_path_generation(path.parent, parent_descriptor)

        commit_receipt = _publish_commit_receipt_create_only(reservation, payload)
        committed = True
        post_commit_errors.extend(
            list(commit_receipt.get("post_commit_verification_errors", []))
        )

        try:
            _assert_entry_generation(parent_descriptor, staging.name, descriptor, "pending")
        except (OSError, ContractError) as error:
            retirement_error = _post_commit_error(error, "pending_generation")
            post_commit_errors.append(retirement_error)
        else:
            try:
                retired, retirement_error = _retire_pending(
                    parent_descriptor, staging.name,
                )
            except Exception as error:
                retirement_error = _post_commit_error(error, "pending_retirement")
                post_commit_errors.append(retirement_error)
            else:
                if retirement_error is not None:
                    post_commit_errors.append(
                        f"pending_retirement:{retirement_error}"
                    )

        for stage, verifier in (
            (
                "final_generation_after_commit",
                lambda: _assert_entry_generation(
                    parent_descriptor, path.name, descriptor, "final"
                ),
            ),
            (
                "parent_generation_after_commit",
                lambda: _assert_parent_path_generation(path.parent, parent_descriptor),
            ),
        ):
            try:
                verifier()
            except (OSError, ContractError) as error:
                post_commit_errors.append(_post_commit_error(error, stage))
    except Exception as error:
        if not committed:
            raise
        post_commit_errors.append(_post_commit_error(error, "unexpected_post_commit"))
    finally:
        if owns_reservation or committed:
            reservation.close()

    if not committed or commit_receipt is None:
        raise ContractError("evidence publication returned without durable commit receipt")
    return {
        "path": str(path),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
        "recovered": False,
        "payload_matches_request": True,
        "pending_retired": retired,
        "pending_retirement_error": retirement_error,
        "commit_receipt": commit_receipt,
        "post_commit_verification_errors": post_commit_errors,
        "post_commit_report_mutation": False,
    }


if __name__ == "__main__":
    raise SystemExit(main())
