"""Real temporary-filesystem tests; no game, model or operator host access."""

from __future__ import annotations

import ast
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import threading

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_attempt_guard_generation2 as guard,
)

REQUEST = guard.request.build_candidate_authorization_request()
SOURCE = "a" * 64
HOLD = guard.CandidateAttemptHold
ROOT = str(Path(__file__).resolve().parents[1])


@pytest.fixture
def namespace(tmp_path):
    directory = tmp_path / "claims"
    directory.mkdir(mode=0o700)
    directory.chmod(0o700)
    fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    info = os.fstat(fd)
    yield directory, fd, (info.st_dev, info.st_ino)
    os.close(fd)


def consume(namespace, **overrides):
    _, fd, identity = namespace
    arguments = dict(
        directory_fd=fd, expected_directory_identity=identity, request_bytes=REQUEST,
        invocation_source_sha256=SOURCE, confirm=guard.CLAIM_CONFIRMATION,
    )
    arguments.update(overrides)
    return guard.consume_candidate_attempt(**arguments)


def test_real_marker_is_synced_read_back_private_and_not_execution_authority(namespace, monkeypatch):
    directory, fd, identity = namespace
    syncs = []
    original = os.fsync

    def observe(descriptor):
        syncs.append("directory" if stat.S_ISDIR(os.fstat(descriptor).st_mode) else "file")
        return original(descriptor)

    monkeypatch.setattr(guard.os, "fsync", observe)
    result = consume(namespace)
    marker = directory / guard.MARKER_NAME
    raw = marker.read_bytes()
    recorded = json.loads(raw)
    assert syncs == ["directory", "file", "directory"]
    assert result["single_use_slot_consumed"] is True
    assert result["directory_identity"] == identity
    assert result["marker_sha256"] == hashlib.sha256(raw).hexdigest()
    assert result["marker_bytes"] == len(raw) <= guard.MAX_MARKER_BYTES
    assert stat.S_IMODE(marker.stat().st_mode) == 0o600
    assert marker.stat().st_nlink == 1
    assert recorded["record_kind"] == "attempt_consumed_not_execution_evidence"
    assert recorded["request_sha256"] == guard.REQUEST_SHA256
    assert recorded["invocation_source_sha256"] == SOURCE
    assert recorded["arm"] == "candidate" and recorded["pair_slot"] == 3
    for key in ("candidate_execution_authorized", "candidate_execution_performed",
                "reusable_execution_permit", "automatic_retry", "held_out"):
        assert result[key] is False and recorded[key] is False
    assert os.fstat(fd).st_ino == identity[1]  # Borrowed descriptor remains open.


@pytest.mark.parametrize("override", [
    {"confirm": ""}, {"confirm": True},
    {"confirm": "VOID_ABADDON_GENERATION2_V2R13_EXECUTE_PAIR03_BASELINE"},
    {"request_bytes": b"{}"}, {"request_bytes": bytearray(REQUEST)},
    {"request_bytes": REQUEST + b"\n"}, {"request_bytes": b"x" * 16385},
    {"invocation_source_sha256": "A" * 64}, {"invocation_source_sha256": "a" * 63},
    {"invocation_source_sha256": "g" * 64}, {"invocation_source_sha256": True},
    {"directory_fd": True}, {"directory_fd": -1},
    {"expected_directory_identity": [1, 2]}, {"expected_directory_identity": (True, 2)},
    {"expected_directory_identity": (-1, 2)},
])
def test_invalid_inputs_stop_before_filesystem_access(namespace, monkeypatch, override):
    def forbidden(*args, **kwargs):
        raise AssertionError("filesystem access before admission")

    monkeypatch.setattr(guard.os, "dup", forbidden)
    with pytest.raises(HOLD) as caught:
        consume(namespace, **override)
    assert caught.value.marker_may_exist is False
    assert list(namespace[0].iterdir()) == []


@pytest.mark.parametrize("mode", [0o755, 0o770, 0o777])
def test_nonprivate_directory_refuses_before_consumption(namespace, mode):
    namespace[0].chmod(mode)
    with pytest.raises(HOLD, match="DIRECTORY_HOLD") as caught:
        consume(namespace)
    assert caught.value.marker_may_exist is False
    assert list(namespace[0].iterdir()) == []


def test_wrong_admitted_directory_identity_refuses(namespace):
    dev, ino = namespace[2]
    with pytest.raises(HOLD, match="DIRECTORY_HOLD"):
        consume(namespace, expected_directory_identity=(dev, ino + 1))
    assert list(namespace[0].iterdir()) == []


def test_regular_file_descriptor_refuses(namespace, tmp_path):
    path = tmp_path / "not-a-directory"
    path.write_bytes(b"unrelated")
    fd = os.open(path, os.O_RDONLY)
    info = os.fstat(fd)
    try:
        with pytest.raises(HOLD, match="DIRECTORY_HOLD"):
            consume(namespace, directory_fd=fd, expected_directory_identity=(info.st_dev, info.st_ino))
        assert os.fstat(fd).st_ino == info.st_ino
    finally:
        os.close(fd)
    assert path.read_bytes() == b"unrelated"


@pytest.mark.parametrize("kind", ["empty", "junk", "valid", "directory", "symlink", "dangling", "fifo", "hardlink"])
def test_every_existing_marker_holds_without_reading_or_replacing_it(namespace, tmp_path, monkeypatch, kind):
    marker = namespace[0] / guard.MARKER_NAME
    foreign = tmp_path / "foreign"
    foreign.write_bytes(b"preserve-foreign")
    if kind == "valid":
        consume(namespace)
    elif kind == "directory":
        marker.mkdir()
    elif kind in {"symlink", "dangling"}:
        marker.symlink_to(foreign if kind == "symlink" else tmp_path / "missing")
    elif kind == "fifo":
        os.mkfifo(marker)
    elif kind == "hardlink":
        os.link(foreign, marker)
    else:
        marker.write_bytes(b"" if kind == "empty" else b"not-json")
    mode = marker.lstat().st_mode
    bytes_before = marker.read_bytes() if stat.S_ISREG(mode) else None
    before = marker.lstat()  # Capture after our own read can update atime.

    def forbidden(*args, **kwargs):
        raise AssertionError("existing marker must not be read or rewritten")

    with monkeypatch.context() as patch:
        patch.setattr(guard.os, "read", forbidden)
        patch.setattr(guard.os, "write", forbidden)
        with pytest.raises(HOLD, match="ALREADY_EXISTS") as caught:
            consume(namespace)
        assert caught.value.marker_may_exist is True
    assert marker.lstat() == before
    if bytes_before is not None:
        assert marker.read_bytes() == bytes_before
    assert foreign.read_bytes() == b"preserve-foreign"


def test_different_source_hash_and_mutated_result_cannot_open_a_second_slot(namespace):
    first = consume(namespace)
    first["candidate_execution_authorized"] = True
    first["single_use_slot_consumed"] = False
    for source in (SOURCE, "b" * 64):
        with pytest.raises(HOLD, match="ALREADY_EXISTS"):
            consume(namespace, invocation_source_sha256=source)
    assert len(list(namespace[0].iterdir())) == 1


@pytest.mark.parametrize("which", [1, 2, 3])
def test_sync_failure_never_returns_success_or_removes_uncertain_marker(namespace, monkeypatch, which):
    original = os.fsync
    count = 0

    def fault(fd):
        nonlocal count
        count += 1
        if count == which:
            raise OSError("fixture sync failure")
        return original(fd)

    with monkeypatch.context() as patch:
        patch.setattr(guard.os, "fsync", fault)
        with pytest.raises(HOLD, match="IO_HOLD") as caught:
            consume(namespace)
    exists = (namespace[0] / guard.MARKER_NAME).exists()
    assert exists is (which != 1)
    assert caught.value.marker_may_exist is exists
    if exists:
        with pytest.raises(HOLD, match="ALREADY_EXISTS"):
            consume(namespace)
    else:
        assert consume(namespace)["single_use_slot_consumed"] is True


@pytest.mark.parametrize("operation", ["write_error", "zero_write", "tiny_writes", "read_error", "empty_read", "tiny_reads"])
def test_partial_io_is_bounded_preserved_and_cannot_retry(namespace, monkeypatch, operation):
    write, read = os.write, os.read
    calls = 0

    def fault_write(fd, data):
        nonlocal calls
        calls += 1
        if operation == "write_error":
            raise OSError("fixture write")
        if operation == "zero_write":
            return 0
        return write(fd, data[:1])

    def fault_read(fd, count):
        nonlocal calls
        calls += 1
        if operation == "read_error":
            raise OSError("fixture read")
        if operation == "empty_read":
            return b""
        return read(fd, min(1, count))

    with monkeypatch.context() as patch:
        patch.setattr(guard.os, "write" if "write" in operation else "read",
                      fault_write if "write" in operation else fault_read)
        with pytest.raises(HOLD) as caught:
            consume(namespace)
    assert caught.value.marker_may_exist is True
    assert calls <= guard.MAX_IO_CALLS
    marker = namespace[0] / guard.MARKER_NAME
    before = marker.read_bytes()
    with pytest.raises(HOLD, match="ALREADY_EXISTS"):
        consume(namespace)
    assert marker.read_bytes() == before


def test_short_reads_and_writes_can_complete_without_retrying_the_attempt(namespace, monkeypatch):
    write, read = os.write, os.read
    monkeypatch.setattr(guard.os, "write", lambda fd, data: write(fd, data[:31]))
    monkeypatch.setattr(guard.os, "read", lambda fd, count: read(fd, min(count, 29)))
    assert consume(namespace)["single_use_slot_consumed"] is True


def test_final_namespace_replacement_holds_and_preserves_both_inodes(namespace, monkeypatch):
    marker = namespace[0] / guard.MARKER_NAME
    retained = namespace[0] / "fixture-retained-original"
    original = os.stat

    def replacement(path, *args, **kwargs):
        if path == guard.MARKER_NAME:
            marker.rename(retained)
            marker.write_bytes(b"foreign-replacement")
        return original(path, *args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(guard.os, "stat", replacement)
        with pytest.raises(HOLD, match="FILE_CHANGED"):
            consume(namespace)
    assert marker.read_bytes() == b"foreign-replacement"
    assert json.loads(retained.read_bytes())["request_sha256"] == guard.REQUEST_SHA256


def test_close_error_holds_without_retrying_close_or_losing_borrowed_fd(namespace, monkeypatch):
    original = os.close
    closed = []

    def fault(fd):
        closed.append(fd)
        original(fd)
        if len(closed) == 1:
            raise OSError("fixture close returned an error after closing")

    with monkeypatch.context() as patch:
        patch.setattr(guard.os, "close", fault)
        with pytest.raises(HOLD, match="CLOSE_HOLD"):
            consume(namespace)
    assert len(closed) == len(set(closed)) == 2
    assert os.fstat(namespace[1]).st_ino == namespace[2][1]
    with pytest.raises(HOLD, match="ALREADY_EXISTS"):
        consume(namespace)


def test_concurrent_callers_produce_exactly_one_consumption(namespace):
    gate = threading.Barrier(8, timeout=10)

    def attempt(_):
        gate.wait()
        try:
            return consume(namespace)["single_use_slot_consumed"]
        except HOLD as error:
            return str(error)

    with ThreadPoolExecutor(max_workers=8) as pool:
        outcomes = list(pool.map(attempt, range(8)))
    assert outcomes.count(True) == 1
    assert outcomes.count("CANDIDATE_ATTEMPT_ALREADY_EXISTS") == 7


CHILD = r'''
import os, sys
from openra_env.learning import abaddon_policy_campaign_runtime_v2r13_pair03_candidate_attempt_guard_generation2 as g
fd = os.open(sys.argv[1], os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
s = os.fstat(fd)
mode = sys.argv[2]
if mode == "before_write":
    def crash(*args): os._exit(91)
    g.os.write = crash
elif mode == "after_file_sync":
    original = os.fsync
    count = 0
    def crash(descriptor):
        global count
        count += 1
        original(descriptor)
        if count == 2: os._exit(92)
    g.os.fsync = crash
if mode == "race":
    print("READY", flush=True)
    sys.stdin.buffer.read(1)
try:
    g.consume_candidate_attempt(directory_fd=fd, expected_directory_identity=(s.st_dev,s.st_ino),
        request_bytes=g.request.build_candidate_authorization_request(),
        invocation_source_sha256="a"*64, confirm=g.CLAIM_CONFIRMATION)
except g.CandidateAttemptHold as error:
    print(str(error), flush=True)
    sys.exit(2)
else:
    print("CONSUMED", flush=True)
finally:
    os.close(fd)
'''


def child(namespace, mode):
    return subprocess.run(
        [sys.executable, "-c", CHILD, str(namespace[0]), mode],
        env={"PYTHONPATH": ROOT}, stdin=subprocess.DEVNULL,
        capture_output=True, text=True, timeout=15, check=False,
    )


@pytest.mark.parametrize("cut,exit_code", [("before_write", 91), ("after_file_sync", 92), ("normal", 0)])
def test_fresh_process_refuses_after_process_loss_or_completed_consumption(namespace, cut, exit_code):
    first = child(namespace, cut)
    assert first.returncode == exit_code, first.stderr
    marker = namespace[0] / guard.MARKER_NAME
    before = marker.read_bytes()
    restarted = child(namespace, "normal")
    assert restarted.returncode == 2, restarted.stderr
    assert restarted.stdout.strip() == "CANDIDATE_ATTEMPT_ALREADY_EXISTS"
    assert marker.read_bytes() == before
    if cut == "before_write":
        assert len(before) == 0
    else:
        assert len(before) > 0


def test_independent_processes_cannot_both_consume(namespace):
    processes = [subprocess.Popen(
        [sys.executable, "-c", CHILD, str(namespace[0]), "race"],
        env={"PYTHONPATH": ROOT}, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True,
    ) for _ in range(4)]
    try:
        # Send to every process before collecting results; each performs its own
        # import, directory open and create-only attempt with no shared Python state.
        for process in processes:
            process.stdin.write("x")
            process.stdin.flush()
        results = [process.communicate(timeout=15) for process in processes]
        assert [p.returncode for p in processes].count(0) == 1, results
        assert [p.returncode for p in processes].count(2) == 3, results
        assert sum("CONSUMED" in out for out, _ in results) == 1
        assert sum("ALREADY_EXISTS" in out for out, _ in results) == 3
    finally:
        for process in processes:
            if process.poll() is None:
                process.kill()
                process.wait(timeout=5)


def test_source_exposes_no_runtime_or_reset_entrypoint():
    source = Path(guard.__file__).read_text()
    tree = ast.parse(source)
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.add(node.module)
    assert modules == {"__future__", "hashlib", "json", "os", "stat", "typing", "openra_env.learning"}
    assert "os.unlink(" not in source and "os.remove(" not in source
    assert "os.replace(" not in source and "os.rename(" not in source
    assert "execute_v2r13_arm(" not in source
    assert 'if __name__ ==' not in source
    assert guard.request.validate_candidate_authorization_request(REQUEST)["authority"]["candidate_execution_authorized"] is False


def test_accepted_request_source_bytes_remain_exact():
    data = Path(guard.request.__file__).read_bytes()
    assert hashlib.sha256(data).hexdigest() == (
        "f719a55ea50ec2923251a22bc3daf8ea8f3579e109b6cb5fabebae8430644fd6"
    )
