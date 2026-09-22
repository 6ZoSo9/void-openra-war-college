from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_attempt_guard_generation2
    as guard,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_authorization_request_generation2
    as request,
)


def _open_private_directory(path: Path) -> tuple[int, tuple[int, int]]:
    path.mkdir()
    path.chmod(0o700)
    fd = os.open(
        path,
        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
    )
    st = os.fstat(fd)
    return fd, (st.st_dev, st.st_ino)


def _consume_once(path: Path, *, source_sha: str = "a" * 64):
    fd, identity = _open_private_directory(path)
    try:
        return guard.consume_pair09_baseline_attempt(
            directory_fd=fd,
            expected_directory_identity=identity,
            request_bytes=request.build_pair09_baseline_authorization_request(),
            invocation_source_sha256=source_sha,
            confirm=guard.CLAIM_CONFIRMATION,
        )
    finally:
        os.close(fd)


def test_contract_is_single_use_non_authorizing_guard():
    out = guard.pair09_baseline_attempt_guard_contract()
    assert out["pair_slot"] == 9
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["single_use_attempt_consumption_implemented"] is True
    assert out["create_only_marker_required"] is True
    assert out["existing_or_uncertain_marker_holds"] is True
    assert out["marker_deletion_api_implemented"] is False
    assert out["reset_api_implemented"] is False
    assert out["resume_api_implemented"] is False
    assert out["automatic_retry"] is False
    assert out["pair09_baseline_specific_authorization_accepted"] is False
    assert out["pair09_baseline_execution_authorized"] is False
    assert out["pair09_baseline_execution_performed"] is False


def test_exact_claim_creates_one_private_marker(tmp_path):
    root = tmp_path / "claims"
    result = _consume_once(root)
    marker = root / guard.MARKER_NAME

    assert result["single_use_slot_consumed"] is True
    assert result["pair_slot"] == 9
    assert result["arm"] == "baseline"
    assert result["held_out"] is False
    assert result["pair09_baseline_specific_authorization_accepted"] is False
    assert result["pair09_baseline_execution_authorized"] is False
    assert result["pair09_baseline_execution_performed"] is False
    assert result["reusable_execution_permit"] is False
    assert result["automatic_retry"] is False
    assert marker.is_file()
    assert not marker.is_symlink()
    assert (marker.stat().st_mode & 0o777) == 0o600

    parsed = json.loads(marker.read_text(encoding="ascii"))
    assert parsed["record_kind"] == "attempt_consumed_not_execution_evidence"
    assert parsed["pair_slot"] == 9
    assert parsed["arm"] == "baseline"
    assert parsed["held_out"] is False
    assert parsed["invocation_source_sha256"] == "a" * 64
    assert parsed["pair09_baseline_specific_authorization_accepted"] is False
    assert parsed["pair09_baseline_execution_authorized"] is False
    assert parsed["pair09_baseline_execution_performed"] is False
    assert parsed["reusable_execution_permit"] is False
    assert parsed["automatic_retry"] is False


def test_second_claim_holds_and_does_not_replace_marker(tmp_path):
    root = tmp_path / "claims"
    first = _consume_once(root)
    marker = root / guard.MARKER_NAME
    first_bytes = marker.read_bytes()
    first_inode = marker.stat().st_ino

    fd = os.open(
        root,
        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
    )
    st = os.fstat(fd)
    try:
        with pytest.raises(
            guard.V2R13Pair09BaselineAttemptHold,
            match="PAIR09_BASELINE_ATTEMPT_ALREADY_EXISTS",
        ) as held:
            guard.consume_pair09_baseline_attempt(
                directory_fd=fd,
                expected_directory_identity=(st.st_dev, st.st_ino),
                request_bytes=request.build_pair09_baseline_authorization_request(),
                invocation_source_sha256="a" * 64,
                confirm=guard.CLAIM_CONFIRMATION,
            )
        assert held.value.marker_may_exist is True
    finally:
        os.close(fd)

    assert marker.read_bytes() == first_bytes
    assert marker.stat().st_ino == first_inode
    assert first["marker_sha256"] == guard.hashlib.sha256(first_bytes).hexdigest()


def test_wrong_confirmation_rejected_before_marker_creation(tmp_path):
    root = tmp_path / "claims"
    fd, identity = _open_private_directory(root)
    try:
        with pytest.raises(
            guard.V2R13Pair09BaselineAttemptHold,
            match="PAIR09_BASELINE_ATTEMPT_CONFIRMATION_REQUIRED",
        ):
            guard.consume_pair09_baseline_attempt(
                directory_fd=fd,
                expected_directory_identity=identity,
                request_bytes=request.build_pair09_baseline_authorization_request(),
                invocation_source_sha256="a" * 64,
                confirm="wrong",
            )
    finally:
        os.close(fd)
    assert not (root / guard.MARKER_NAME).exists()


def test_modified_request_rejected_before_marker_creation(tmp_path):
    root = tmp_path / "claims"
    fd, identity = _open_private_directory(root)
    try:
        payload = request.build_pair09_baseline_authorization_request() + b"x"
        with pytest.raises(
            guard.V2R13Pair09BaselineAttemptHold,
            match="PAIR09_BASELINE_ATTEMPT_REQUEST_INVALID",
        ):
            guard.consume_pair09_baseline_attempt(
                directory_fd=fd,
                expected_directory_identity=identity,
                request_bytes=payload,
                invocation_source_sha256="a" * 64,
                confirm=guard.CLAIM_CONFIRMATION,
            )
    finally:
        os.close(fd)
    assert not (root / guard.MARKER_NAME).exists()


def test_invalid_invocation_source_identity_rejected(tmp_path):
    root = tmp_path / "claims"
    fd, identity = _open_private_directory(root)
    try:
        with pytest.raises(
            guard.V2R13Pair09BaselineAttemptHold,
            match="PAIR09_BASELINE_ATTEMPT_SOURCE_IDENTITY_INVALID",
        ):
            guard.consume_pair09_baseline_attempt(
                directory_fd=fd,
                expected_directory_identity=identity,
                request_bytes=request.build_pair09_baseline_authorization_request(),
                invocation_source_sha256="not-a-sha",
                confirm=guard.CLAIM_CONFIRMATION,
            )
    finally:
        os.close(fd)
    assert not (root / guard.MARKER_NAME).exists()


def test_directory_mode_must_be_private(tmp_path):
    root = tmp_path / "claims"
    root.mkdir()
    root.chmod(0o755)
    fd = os.open(
        root,
        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC,
    )
    st = os.fstat(fd)
    try:
        with pytest.raises(
            guard.V2R13Pair09BaselineAttemptHold,
            match="PAIR09_BASELINE_ATTEMPT_DIRECTORY_HOLD",
        ):
            guard.consume_pair09_baseline_attempt(
                directory_fd=fd,
                expected_directory_identity=(st.st_dev, st.st_ino),
                request_bytes=request.build_pair09_baseline_authorization_request(),
                invocation_source_sha256="a" * 64,
                confirm=guard.CLAIM_CONFIRMATION,
            )
    finally:
        os.close(fd)
    assert not (root / guard.MARKER_NAME).exists()


def test_no_reset_delete_or_resume_api_exists():
    for name in (
        "reset_pair09_baseline_attempt",
        "delete_pair09_baseline_attempt",
        "resume_pair09_baseline_attempt",
        "clear_pair09_baseline_attempt",
    ):
        assert not hasattr(guard, name)


def test_guard_advances_only_to_separate_source_review():
    out = guard.pair09_baseline_attempt_guard_contract()
    assert out["next_gate"] == (
        "V2R13_PAIR09_BASELINE_ATTEMPT_GUARD_"
        "SOURCE_BINDING_REVIEW_REQUIRED"
    )
