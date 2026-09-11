#!/usr/bin/env python3
"""Compatibility facade for the reviewed JointAdvance benchmark core.

The full reviewed source is retained byte-for-byte in
``bench_joint_advance_core.py``.  It is executed into this module namespace so
existing imports, monkeypatch-based falsifiers, and function globals keep the
same behavior.  This facade owns two narrow boundaries around that preserved core: local
evidence publication keeps the durable receipt as an irreversible commit point,
and designated-host execution runs inside a spawned process group so detached
cancellation-resistant work cannot hang top-level process retirement.
"""

import multiprocessing as _BootstrapMultiprocessing
import signal as _BootstrapSignal
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
    check and deletion. Until an atomic generation-conditional removal
    primitive exists, leave the alias or replacement intact for explicit
    reconciliation instead of risking deletion of foreign state.
    """
    del parent_descriptor, staging_name
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


# Preserve the exact reviewed coroutine for direct source-only tests. Runtime
# entry through main() is wrapped below in a separate spawned process group.
_CORE_EXECUTE_RUNTIME = execute_runtime
_RUNTIME_CHILD_START_TIMEOUT_S = SUPERVISOR_START_TIMEOUT_S
_RUNTIME_CHILD_NATURAL_RETIREMENT_S = 5.0
_RUNTIME_CHILD_SIGNAL_GRACE_S = 5.0
_RUNTIME_CONTAINMENT_MIN_MARGIN_S = SUPERVISOR_CONTAINMENT_MIN_MARGIN_S


def _runtime_process_deadline_s(parameters: dict[str, Any]) -> float:
    return _supervisor_outer_timeout_s(parameters)


def _process_group_exists(pgid: int) -> bool:
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except PermissionError as error:
        raise ContractError(
            f"cannot verify runtime process-group retirement for pgid={pgid}: {error}"
        ) from error
    return True


def _wait_process_group_absent(pgid: int, timeout_s: float) -> bool:
    deadline = time.monotonic() + timeout_s
    while True:
        if not _process_group_exists(pgid):
            return True
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return False
        time.sleep(min(0.01, remaining))


def _signal_process_group(pgid: int, signal_number: int) -> None:
    try:
        os.killpg(pgid, signal_number)
    except ProcessLookupError:
        return


def _runtime_retirement_remaining(deadline_s: float) -> float:
    """Return the nonnegative remainder of one monotonic retirement budget."""
    return max(0.0, deadline_s - time.monotonic())


def _retire_runtime_process_group(
    process: Any,
    pgid: int,
    *,
    natural_grace_s: float = _RUNTIME_CHILD_NATURAL_RETIREMENT_S,
    signal_grace_s: float = _RUNTIME_CHILD_SIGNAL_GRACE_S,
) -> str:
    """Retire one process group without multiplying phase-local wait budgets."""
    for label, value in (
        ("natural_grace_s", natural_grace_s),
        ("signal_grace_s", signal_grace_s),
    ):
        if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
            raise ContractError(
                f"{label} must be finite nonnegative seconds"
            )

    started_at = time.monotonic()
    natural_deadline = started_at + natural_grace_s
    term_deadline = natural_deadline + signal_grace_s
    kill_deadline = term_deadline + signal_grace_s
    if not all(
        math.isfinite(value)
        for value in (started_at, natural_deadline, term_deadline, kill_deadline)
    ):
        raise ContractError("derived runtime retirement deadlines must be finite")
    if pgid != process.pid:
        raise ContractError("runtime process-group identity is not bound to child PID")

    process.join(_runtime_retirement_remaining(natural_deadline))
    if not process.is_alive() and not _process_group_exists(pgid):
        return "natural_exit"

    _signal_process_group(pgid, _BootstrapSignal.SIGTERM)
    process.join(_runtime_retirement_remaining(term_deadline))
    if (
        not process.is_alive()
        and _wait_process_group_absent(
            pgid, _runtime_retirement_remaining(term_deadline)
        )
    ):
        return "sigterm_retired"

    _signal_process_group(pgid, _BootstrapSignal.SIGKILL)
    process.join(_runtime_retirement_remaining(kill_deadline))
    if process.is_alive() or not _wait_process_group_absent(
        pgid, _runtime_retirement_remaining(kill_deadline)
    ):
        raise ContractError(
            f"runtime process-group containment failed to retire pgid={pgid}"
        )
    return "sigkill_retired"


def _retire_unbound_runtime_child(
    process: Any,
    *,
    signal_grace_s: float = _RUNTIME_CHILD_SIGNAL_GRACE_S,
) -> None:
    """Retire an unbound child within one monotonic TERM/KILL budget."""
    if (
        type(signal_grace_s) not in (int, float)
        or not math.isfinite(signal_grace_s)
        or signal_grace_s < 0
    ):
        raise ContractError(
            "unbound runtime child signal grace must be finite nonnegative seconds"
        )

    started_at = time.monotonic()
    term_deadline = started_at + signal_grace_s
    kill_deadline = term_deadline + signal_grace_s
    if not all(
        math.isfinite(value)
        for value in (started_at, term_deadline, kill_deadline)
    ):
        raise ContractError(
            "derived unbound runtime child retirement deadlines must be finite"
        )

    process.join(0)
    if not process.is_alive():
        return
    process.terminate()
    process.join(_runtime_retirement_remaining(term_deadline))
    if process.is_alive():
        process.kill()
        process.join(_runtime_retirement_remaining(kill_deadline))
    if process.is_alive():
        raise ContractError("unbound runtime child could not be retired")


def _runtime_child_entry(
    sender: Any,
    args: argparse.Namespace,
    parameters: dict[str, Any],
    expected_provenance: dict[str, str],
) -> None:
    """Run the reviewed async attempt inside a new session/process group.

    The result is sent from inside the root coroutine, before ``asyncio.run``
    begins pending-task shutdown. The parent can therefore obtain the closed
    evidence outcome and still force-retire this process if a cancellation-
    resistant detached task would otherwise hang event-loop shutdown.
    """
    try:
        os.setsid()
        child_pid = os.getpid()
        child_pgid = os.getpgrp()
        if child_pgid != child_pid:
            raise ContractError("runtime child failed to establish a private process group")
        sender.send(("STARTED", child_pid, child_pgid))

        async def attempt() -> None:
            outcome = await _CORE_EXECUTE_RUNTIME(
                args, parameters, expected_provenance,
            )
            sender.send(("OUTCOME", outcome))

        asyncio.run(attempt())
    except BaseException as error:
        try:
            sender.send(("ERROR", type(error).__name__, str(error)))
        except (BrokenPipeError, EOFError, OSError):
            pass
    finally:
        sender.close()


# Make the spawn target importable by its stable public module name even when
# the facade itself is invoked as a script.
_runtime_child_entry.__module__ = _CORE_EXEC_MODULE



def _build_parent_supervisor_record(
    *,
    args: argparse.Namespace,
    process: Any,
    pgid: int,
    outer_execution_timeout_s: float,
    retirement_terminal: str,
    expected_provenance: dict[str, str],
    parameters: dict[str, Any],
) -> dict[str, Any]:
    operation = operation_descriptor(
        expected_provenance,
        parameters,
        designated_hostname=args.designated_hostname,
        openra_dir=Path(args.openra_dir),
    )
    return {
        "schema": SUPERVISOR_SCHEMA,
        "owner": "parent_process",
        "parent_pid": os.getpid(),
        "child_pid": process.pid,
        "child_pgid": pgid,
        "authorization_boundary": {
            "mode": "run",
            "execute_designated_host": True,
            "designated_hostname": args.designated_hostname,
            "operation_sha256": operation["sha256"],
        },
        "start_timeout_s": _RUNTIME_CHILD_START_TIMEOUT_S,
        "outer_execution_timeout_s": outer_execution_timeout_s,
        "terminal_source": "child_outcome",
        "containment": {
            "process_group_bound": True,
            "retirement_attempted": True,
            "retirement_terminal": retirement_terminal,
        },
    }


def _execute_runtime_contained(
    args: argparse.Namespace,
    parameters: dict[str, Any],
    expected_provenance: dict[str, str],
) -> dict[str, Any]:
    """Own one runtime attempt in a spawned, killable process group."""
    if (
        getattr(args, "mode", None) != "run"
        or getattr(args, "execute_designated_host", None) is not True
        or not isinstance(getattr(args, "designated_hostname", None), str)
        or not args.designated_hostname
        or not getattr(args, "openra_dir", None)
    ):
        raise ContractError(
            "runtime containment requires explicit designated-host run authorization"
        )
    if (
        os.name != "posix"
        or not hasattr(os, "setsid")
        or not hasattr(os, "killpg")
    ):
        raise ContractError(
            "designated-host runtime requires POSIX process-group containment"
        )

    context = _BootstrapMultiprocessing.get_context("spawn")
    receiver, sender = context.Pipe(duplex=False)
    process = context.Process(
        target=_runtime_child_entry,
        args=(sender, args, parameters, expected_provenance),
        name="void-war-college-runtime",
    )
    process.start()
    sender.close()

    pgid: int | None = None
    outcome: dict[str, Any] | None = None
    child_error: str | None = None
    deadline = time.monotonic() + _RUNTIME_CHILD_START_TIMEOUT_S
    runtime_started = False
    outer_execution_timeout_s: float | None = None
    retirement_terminal: str | None = None

    try:
        while outcome is None and child_error is None:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                child_error = (
                    "runtime child start deadline exceeded"
                    if not runtime_started
                    else "runtime child outer execution deadline exceeded"
                )
                break

            if receiver.poll(min(0.1, remaining)):
                try:
                    message = receiver.recv()
                except EOFError:
                    child_error = "runtime child pipe closed without a terminal message"
                    break
                if not isinstance(message, tuple) or not message:
                    child_error = "runtime child emitted an invalid control message"
                    break

                kind = message[0]
                if kind == "STARTED":
                    if (
                        runtime_started
                        or len(message) != 3
                        or message[1] != process.pid
                        or message[2] != process.pid
                    ):
                        child_error = "runtime child process-group binding is invalid"
                        break
                    runtime_started = True
                    pgid = message[2]
                    outer_execution_timeout_s = _runtime_process_deadline_s(parameters)
                    deadline = time.monotonic() + outer_execution_timeout_s
                elif kind == "OUTCOME":
                    if not runtime_started or len(message) != 2:
                        child_error = "runtime child outcome arrived before process-group binding"
                        break
                    if not isinstance(message[1], dict):
                        child_error = "runtime child outcome is not a structured object"
                        break
                    if set(message[1]) != {"cells", "run", "host"}:
                        child_error = "runtime child outcome fields are not exact"
                        break
                    outcome = message[1]
                elif kind == "ERROR":
                    if len(message) != 3:
                        child_error = "runtime child error message is malformed"
                    else:
                        child_error = f"{message[1]}:{message[2]}"
                else:
                    child_error = f"runtime child emitted unsupported message type: {kind}"
            elif not process.is_alive():
                child_error = (
                    f"runtime child exited before outcome: exitcode={process.exitcode}"
                )
                break
    finally:
        receiver.close()
        if pgid is None:
            _retire_unbound_runtime_child(process)
        else:
            retirement_terminal = _retire_runtime_process_group(process, pgid)

    if outcome is None:
        raise ContractError(child_error or "runtime child produced no outcome")
    if pgid is None or outer_execution_timeout_s is None or retirement_terminal is None:
        raise ContractError("runtime child outcome lacks a closed parent supervisor terminal")
    return {
        **outcome,
        "supervisor": _build_parent_supervisor_record(
            args=args,
            process=process,
            pgid=pgid,
            outer_execution_timeout_s=outer_execution_timeout_s,
            retirement_terminal=retirement_terminal,
            expected_provenance=expected_provenance,
            parameters=parameters,
        ),
    }


def _run_runtime_from_main(
    args: argparse.Namespace,
    parameters: dict[str, Any],
    provenance: dict[str, str],
) -> dict[str, Any]:
    """Use containment in production while preserving monkeypatch-based unit tests."""
    if execute_runtime is not _CORE_EXECUTE_RUNTIME:
        return asyncio.run(execute_runtime(args, parameters, provenance))
    return _execute_runtime_contained(args, parameters, provenance)


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        provenance = validate_provenance(
            args.engine_sha,
            args.war_college_sha,
            args.benchmark_source_sha,
            args.generation,
        )
        parameters = normalized_args(args)
        if args.mode == "run":
            if not args.execute_designated_host:
                raise ContractError("run requires --execute-designated-host")
            if not args.openra_dir or not args.output or not args.designated_hostname:
                raise ContractError(
                    "run requires --openra-dir, --output, and --designated-hostname"
                )
            operation = operation_descriptor(
                provenance,
                parameters,
                designated_hostname=args.designated_hostname,
                openra_dir=Path(args.openra_dir),
            )
            # A pre-positioned report is not designated-host authority. Refuse
            # it before runtime contact; the spawned runtime child never owns
            # these retained publication descriptors.
            reservation = reserve_evidence_namespace(Path(args.output))
            try:
                outcome = _run_runtime_from_main(args, parameters, provenance)
                report = build_report(
                    provenance=provenance,
                    parameters=parameters,
                    cells=outcome["cells"],
                    executed_designated_host=True,
                    generated_at_utc=utc_now(),
                    command=sys.argv if argv is None else [Path(sys.argv[0]).name, *argv],
                    run=outcome["run"],
                    host=outcome["host"],
                    operation=operation,
                    supervisor=outcome["supervisor"],
                )
                try:
                    payload = stable_json(report).encode("utf-8")
                    publication = publish_evidence_create_only(
                        Path(args.output), payload, reservation=reservation,
                    )
                    if not publication["payload_matches_request"]:
                        report = _validate_recoverable_evidence(
                            _read_regular_read_only(Path(args.output).resolve())
                        )
                except (OSError, ContractError) as error:
                    report["run"].update({
                        "terminal": "output_error",
                        "stage": "evidence_publication",
                        "error_type": type(error).__name__,
                        "error": str(error),
                    })
                    report = json.loads(json.dumps(report, allow_nan=False))
                    # The same retained inode that held the attempted completed
                    # report must carry the process's authoritative failure
                    # terminal. Otherwise explicit reconciliation could count a
                    # durable `completed` artifact after canonical publication
                    # failed and stdout truthfully reported `output_error`.
                    try:
                        _write_reserved_payload(
                            reservation,
                            stable_json(report).encode("utf-8"),
                        )
                    except (OSError, ContractError) as persistence_error:
                        report["run"]["publication_terminal_persistence_error"] = (
                            f"{type(persistence_error).__name__}:{persistence_error}"
                        )
                        report = json.loads(json.dumps(report, allow_nan=False))
            finally:
                reservation.close()
            print(human_summary(report), file=sys.stderr)
        else:
            if args.execute_designated_host:
                raise ContractError("plan must not use --execute-designated-host")
            report = build_report(
                provenance=provenance,
                parameters=parameters,
                cells=[],
                executed_designated_host=False,
                generated_at_utc=utc_now(),
                command=sys.argv if argv is None else [Path(sys.argv[0]).name, *argv],
            )
        print(json.dumps(report, indent=2, sort_keys=True))
        return terminal_exit_code(report) if args.mode == "run" else 0
    except (ContractError, OSError) as error:
        print(f"contract error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
