from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]
SOURCE = (
    ROOT
    / "tools/"
    "void_pair06_v8_coherent_v2_success_artifact_rehash_precision_v1.py"
)
SPEC = importlib.util.spec_from_file_location("pair06_success_rehash", SOURCE)
assert SPEC is not None and SPEC.loader is not None
rehash = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rehash)


def test_exact_six_artifact_paths_and_recorded_digests():
    assert set(rehash.ARTIFACTS) == {
        "attempt_marker",
        "result",
        "closeout",
        "trajectory",
        "summary",
        "warm_start",
    }
    assert rehash.RUN_DIR == Path(
        "/home/zoso/dev/void-war-college-execution/v8-generation2/generation2/"
        "pair-06/baseline/runs-combat-priority-coherent-v2-v1/"
        "warmstart-apollyon-vs-abaddon-20260927T183337Z-feinter-s208354846"
    )
    assert rehash.ARTIFACTS["trajectory"]["path"].name == "trajectory.jsonl"
    assert rehash.ARTIFACTS["summary"]["path"].name == "summary.json"
    assert rehash.ARTIFACTS["warm_start"]["path"].name == "warm-start.jsonl"


def test_read_primitive_verifies_real_bytes_and_rejects_one_byte_drift(tmp_path):
    path = tmp_path / "artifact.bin"
    raw = b"pair06-success-artifact\n"
    path.write_bytes(raw)
    expected = hashlib.sha256(raw).hexdigest()

    observed, receipt = rehash._read_exact_regular_file(
        path,
        expected_sha256=expected,
        maximum_bytes=4096,
    )
    assert observed == raw
    assert receipt["sha256"] == expected
    assert receipt["generation_stable"] is True

    path.write_bytes(raw + b"x")
    with pytest.raises(rehash.ArtifactRehashHold, match="ARTIFACT_SHA256_DRIFT"):
        rehash._read_exact_regular_file(
            path,
            expected_sha256=expected,
            maximum_bytes=4096,
        )


def test_read_primitive_rejects_symlink(tmp_path):
    target = tmp_path / "target.bin"
    target.write_bytes(b"x")
    link = tmp_path / "link.bin"
    link.symlink_to(target)
    with pytest.raises(rehash.ArtifactRehashHold, match="PATH_RESOLUTION_DRIFT"):
        rehash._read_exact_regular_file(
            link,
            expected_sha256=hashlib.sha256(b"x").hexdigest(),
            maximum_bytes=4096,
        )


def test_confirmation_is_required_before_any_artifact_open(monkeypatch):
    calls = []

    def forbidden(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError("artifact open should not be reached")

    monkeypatch.setattr(rehash, "_read_exact_regular_file", forbidden)
    with pytest.raises(
        rehash.ArtifactRehashHold,
        match="READ_ONLY_REHASH_CONFIRMATION_REQUIRED",
    ):
        rehash.collect_success_artifact_rehash_manifest(confirm="wrong")
    assert calls == []


def test_source_has_no_process_network_or_filesystem_mutation_backend():
    source = SOURCE.read_text(encoding="utf-8")
    for forbidden in (
        "subprocess",
        "socket",
        "urllib",
        "requests",
        "O_CREAT",
        "O_TRUNC",
        "O_WRONLY",
        "O_RDWR",
        ".unlink(",
        ".rename(",
        ".replace(",
        ".write_text(",
        ".write_bytes(",
        "os.remove(",
        "os.mkdir(",
        "os.makedirs(",
        "systemctl",
        "docker",
        "start_ollama",
    ):
        assert forbidden not in source
    assert "os.O_RDONLY" in source
    assert "os.read(" in source
    assert "os.fstat(" in source
    assert "hashlib.sha256()" in source
