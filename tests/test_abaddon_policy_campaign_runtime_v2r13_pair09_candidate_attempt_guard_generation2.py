from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import stat
import threading

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_attempt_guard_generation2
    as guard,
)

REQUEST = guard.request.build_pair09_candidate_authorization_request()
SOURCE = "a" * 64
HOLD = guard.V2R13Pair09CandidateAttemptHold


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
    args = {
        "directory_fd": fd,
        "expected_directory_identity": identity,
        "request_bytes": REQUEST,
        "invocation_source_sha256": SOURCE,
        "confirm": guard.CLAIM_CONFIRMATION,
    }
    args.update(overrides)
    return guard.consume_pair09_candidate_attempt(**args)


def test_real_marker_is_private_synced_and_not_execution_authority(namespace):
    directory, _, identity = namespace
    out = consume(namespace)
    marker = directory / guard.MARKER_NAME
    raw = marker.read_bytes()
    record = json.loads(raw)
    assert out["single_use_slot_consumed"] is True
    assert out["directory_identity"] == identity
    assert out["marker_sha256"] == hashlib.sha256(raw).hexdigest()
    assert out["marker_bytes"] == len(raw) <= guard.MAX_MARKER_BYTES
    assert stat.S_IMODE(marker.stat().st_mode) == 0o600
    assert marker.stat().st_nlink == 1
    assert record["record_kind"] == "attempt_consumed_not_execution_evidence"
    assert record["pair_slot"] == 9
    assert record["arm"] == "candidate"
    assert record["held_out"] is False
    assert record["request_sha256"] == out["request_sha256"]
    assert record["invocation_source_sha256"] == SOURCE
    assert record["pair09_candidate_specific_authorization_accepted"] is False
    assert record["pair09_candidate_execution_authorized"] is False
    assert record["pair09_candidate_execution_performed"] is False
    assert record["reusable_execution_permit"] is False
    assert record["automatic_retry"] is False


@pytest.mark.parametrize(
    "override",
    [
        {"confirm": ""},
        {"confirm": True},
        {"request_bytes": b"{}"},
        {"request_bytes": bytearray(REQUEST)},
        {"invocation_source_sha256": "A" * 64},
        {"invocation_source_sha256": "a" * 63},
        {"invocation_source_sha256": True},
        {"directory_fd": True},
        {"directory_fd": -1},
        {"expected_directory_identity": [1, 2]},
        {"expected_directory_identity": (True, 2)},
    ],
)
def test_invalid_inputs_refuse_without_consuming(namespace, override):
    with pytest.raises(HOLD):
        consume(namespace, **override)
    assert list(namespace[0].iterdir()) == []


@pytest.mark.parametrize("mode", [0o755, 0o770, 0o777])
def test_nonprivate_directory_refuses_before_consumption(namespace, mode):
    namespace[0].chmod(mode)
    with pytest.raises(HOLD, match="DIRECTORY_HOLD") as caught:
        consume(namespace)
    assert caught.value.marker_may_exist is False
    assert list(namespace[0].iterdir()) == []


def test_existing_marker_is_terminal_and_preserved(namespace):
    first = consume(namespace)
    marker = namespace[0] / guard.MARKER_NAME
    before = marker.read_bytes()
    with pytest.raises(HOLD, match="ALREADY_EXISTS") as caught:
        consume(namespace, invocation_source_sha256="b" * 64)
    assert caught.value.marker_may_exist is True
    assert marker.read_bytes() == before
    assert first["single_use_slot_consumed"] is True


def test_concurrent_callers_produce_exactly_one_consumption(namespace):
    barrier = threading.Barrier(8, timeout=10)

    def attempt(_):
        barrier.wait()
        try:
            return consume(namespace)["single_use_slot_consumed"]
        except HOLD as error:
            return str(error)

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(attempt, range(8)))
    assert results.count(True) == 1
    assert results.count("PAIR09_CANDIDATE_ATTEMPT_ALREADY_EXISTS") == 7


def test_sync_failure_after_creation_preserves_terminal_marker(namespace, monkeypatch):
    original = os.fsync
    count = 0

    def fault(fd):
        nonlocal count
        count += 1
        if count == 2:
            raise OSError("fixture sync failure")
        return original(fd)

    monkeypatch.setattr(guard.os, "fsync", fault)
    with pytest.raises(HOLD, match="IO_HOLD") as caught:
        consume(namespace)
    marker = namespace[0] / guard.MARKER_NAME
    assert marker.exists()
    assert caught.value.marker_may_exist is True


def test_guard_contract_is_non_authorizing_and_no_reset_surface():
    out = guard.pair09_candidate_attempt_guard_contract()
    assert out["pair09_candidate_attempt_guard_implemented"] is True
    assert out["pair09_candidate_attempt_guard_reviewed"] is False
    assert out["pair_slot"] == 9
    assert out["arm"] == "candidate"
    assert out["held_out"] is False
    assert out["create_only_marker"] is True
    assert out["single_use_attempt"] is True
    assert out["maximum_attempts"] == 1
    assert out["automatic_retry"] is False
    assert out["reset_api_present"] is False
    assert out["delete_api_present"] is False
    assert out["resume_api_present"] is False
    assert out["marker_is_execution_authority"] is False
    assert out["pair09_candidate_execution_authorized"] is False
    assert out["pair09_candidate_execution_performed"] is False
    assert out["next_gate"] == (
        "V2R13_PAIR09_CANDIDATE_ATTEMPT_GUARD_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_source_has_no_delete_or_runtime_entrypoint():
    source = Path(guard.__file__).read_text(encoding="utf-8")
    assert "os.unlink(" not in source
    assert "os.remove(" not in source
    assert "os.replace(" not in source
    assert "execute_v2r13_arm(" not in source
    assert 'if __name__ ==' not in source
