"""Real temporary-filesystem tests for the fresh scout attempt guard."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import stat
import threading

import pytest

from openra_env.learning import abaddon_scout_external_attempt_guard_v1 as guard


REQUEST = guard.contract.build_scout_launcher_request()
EXPERIMENT = "abaddon-scout-source-bound-v1-attempt-001"
HOLD = guard.ScoutExternalAttemptHold
ROOT = Path(__file__).resolve().parents[1]


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
    arguments = {
        "directory_fd": fd,
        "expected_directory_identity": identity,
        "request_bytes": REQUEST,
        "experiment_id": EXPERIMENT,
        "launcher_contract_git_blob": guard.review.CONTRACT_GIT_BLOB,
        "confirm": guard.CLAIM_CONFIRMATION,
    }
    arguments.update(overrides)
    return guard.consume_scout_attempt(**arguments)


def test_real_marker_is_private_synced_and_non_authorizing(namespace, monkeypatch):
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
    assert recorded["experiment_id"] == EXPERIMENT
    assert recorded["request_sha256"] == guard.contract.REQUEST_SHA256
    assert recorded["launcher_contract_git_blob"] == guard.review.CONTRACT_GIT_BLOB

    for key in (
        "pair03_attempt_reused",
        "pair03_attempt_reset",
        "scout_execution_authorized",
        "scout_execution_performed",
        "reusable_execution_permit",
        "automatic_retry",
        "training_authorized",
        "automatic_policy_promotion",
    ):
        assert result[key] is False
        assert recorded[key] is False

    assert os.fstat(fd).st_ino == identity[1]


@pytest.mark.parametrize(
    "override",
    [
        {"confirm": ""},
        {"confirm": True},
        {"confirm": "EXECUTE"},
        {"request_bytes": b"{}"},
        {"request_bytes": bytearray(REQUEST)},
        {"request_bytes": REQUEST + b"\n"},
        {"experiment_id": "pair03"},
        {"experiment_id": "abaddon-scout-pair03-reuse"},
        {"experiment_id": "Abaddon-scout-upper"},
        {"experiment_id": ""},
        {"experiment_id": "x" * 129},
        {"launcher_contract_git_blob": "0" * 40},
        {"launcher_contract_git_blob": True},
        {"directory_fd": True},
        {"directory_fd": -1},
        {"expected_directory_identity": [1, 2]},
        {"expected_directory_identity": (True, 2)},
        {"expected_directory_identity": (-1, 2)},
    ],
)
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


def test_wrong_directory_identity_refuses(namespace):
    dev, ino = namespace[2]
    with pytest.raises(HOLD, match="DIRECTORY_HOLD"):
        consume(namespace, expected_directory_identity=(dev, ino + 1))
    assert list(namespace[0].iterdir()) == []


@pytest.mark.parametrize("kind", ["empty", "junk", "valid", "directory", "symlink", "hardlink"])
def test_every_existing_marker_holds_without_replacing_it(namespace, tmp_path, kind):
    marker = namespace[0] / guard.MARKER_NAME
    foreign = tmp_path / "foreign"
    foreign.write_bytes(b"preserve-foreign")

    if kind == "valid":
        consume(namespace)
    elif kind == "directory":
        marker.mkdir()
    elif kind == "symlink":
        marker.symlink_to(foreign)
    elif kind == "hardlink":
        os.link(foreign, marker)
    else:
        marker.write_bytes(b"" if kind == "empty" else b"not-json")

    before = marker.lstat()
    bytes_before = marker.read_bytes() if stat.S_ISREG(before.st_mode) else None

    with pytest.raises(HOLD, match="ALREADY_EXISTS") as caught:
        consume(namespace)
    assert caught.value.marker_may_exist is True
    assert marker.lstat() == before
    if bytes_before is not None:
        assert marker.read_bytes() == bytes_before
    assert foreign.read_bytes() == b"preserve-foreign"


def test_new_experiment_name_cannot_reopen_consumed_slot(namespace):
    first = consume(namespace)
    assert first["single_use_slot_consumed"] is True

    for experiment in (
        EXPERIMENT,
        "abaddon-scout-source-bound-v1-attempt-002",
        "abaddon-scout-another-fresh-name",
    ):
        with pytest.raises(HOLD, match="ALREADY_EXISTS"):
            consume(namespace, experiment_id=experiment)

    assert len(list(namespace[0].iterdir())) == 1


@pytest.mark.parametrize("which", [1, 2, 3])
def test_sync_failure_never_returns_success_or_removes_uncertain_marker(
    namespace, monkeypatch, which
):
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
    assert outcomes.count("SCOUT_ATTEMPT_ALREADY_EXISTS") == 7


def test_source_exposes_no_execution_reset_or_marker_deletion_api():
    source = (ROOT / "openra_env/learning/abaddon_scout_external_attempt_guard_v1.py").read_text()

    for forbidden in (
        "os.unlink(",
        "os.remove(",
        "os.replace(",
        "os.rename(",
        "subprocess",
        "socket",
        "run_main_once(",
        "authorize_or_execute",
        "execute_pair03",
        "reset_attempt",
        "resume_attempt",
    ):
        assert forbidden not in source

    assert 'if __name__ ==' not in source
    assert guard.contract.validate_scout_launcher_request(REQUEST)[
        "authority"
    ]["scout_execution_authorized"] is False
