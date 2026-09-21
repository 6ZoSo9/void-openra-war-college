"""Source-binding tests for the scout external result declaration review."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_external_result_binding_review_v1 as review
from openra_env.learning import abaddon_scout_external_result_binding_v1 as binding


ROOT = Path(__file__).resolve().parents[1]
HOLD = review.ScoutExternalResultBindingReviewHold


def _git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def test_review_binds_exact_result_binding_and_attempt_chain():
    expected = {
        review.LAUNCHER_CONTRACT_PATH: review.LAUNCHER_CONTRACT_GIT_BLOB,
        review.ATTEMPT_GUARD_PATH: review.ATTEMPT_GUARD_GIT_BLOB,
        review.ATTEMPT_GUARD_REVIEW_PATH: review.ATTEMPT_GUARD_REVIEW_GIT_BLOB,
        review.RESULT_BINDING_PATH: review.RESULT_BINDING_GIT_BLOB,
    }
    assert expected == {
        "openra_env/learning/abaddon_scout_external_launcher_contract_v1.py":
            "1f7ee7057c27946f488afe26501482ea4f4fc53d",
        "openra_env/learning/abaddon_scout_external_attempt_guard_v1.py":
            "043225a7ff6528b9ae7f80994fe17480ad36ed3e",
        "openra_env/learning/abaddon_scout_external_attempt_guard_review_v1.py":
            "858a218e87b2dc2eee21a9065bd530fcc0523ee2",
        "openra_env/learning/abaddon_scout_external_result_binding_v1.py":
            "81fbc479ff087e03fc341d2b191b284fb0017803",
    }

    for relative, expected_blob in expected.items():
        path = ROOT / relative
        assert path.is_file() and not path.is_symlink()
        assert _git_blob(path.read_bytes()) == expected_blob

    assert binding.NEXT_GATE == review.NEXT_GATE


def test_review_remains_non_authorizing_and_non_verifying():
    receipt = review.result_binding_source_review_contract()

    assert receipt["main_head"] == "9a151da589f93454d31a475b29297ea8a3d35442"
    assert receipt["review_kind"] == "source_binding_expectation_not_evidence_acceptance"
    assert receipt["result_binding_source_identity_recorded"] is True
    assert receipt["pair03_attempt_reuse_allowed"] is False
    assert receipt["automatic_retry"] is False
    assert receipt["next_gate"] == "SCOUT_EXTERNAL_RESULT_EVIDENCE_REVIEW_REQUIRED"

    assert len(receipt["authority"]) == len(review.FALSE_AUTHORITY_FIELDS)
    assert set(receipt["authority"]) == set(review.FALSE_AUTHORITY_FIELDS)
    assert all(value is False for value in receipt["authority"].values())


@pytest.mark.parametrize(
    ("entrypoint", "kwargs"),
    [
        (review.verify_declared_evidence, {}),
        (review.verify_declared_evidence, {"verified": True}),
        (review.accept_result, {}),
        (review.accept_result, {"verified": True}),
        (review.authorize_or_execute, {}),
        (review.authorize_or_execute, {"authorized": True}),
    ],
)
def test_all_verification_acceptance_and_execution_entrypoints_hold(entrypoint, kwargs):
    with pytest.raises(HOLD, match=review.NEXT_GATE):
        entrypoint(**kwargs)


def test_review_snapshot_is_fresh():
    first = review.result_binding_source_review_contract()
    first["source_references"].clear()
    first["authority"]["result_evidence_verified"] = True

    later = review.result_binding_source_review_contract()
    assert len(later["source_references"]) == 4
    assert later["authority"]["result_evidence_verified"] is False


def test_review_source_has_no_runtime_filesystem_network_or_local_imports():
    path = ROOT / "openra_env/learning/abaddon_scout_external_result_binding_review_v1.py"
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.add(node.module)

    assert modules == {"__future__", "typing"}
    for forbidden in (
        "hashlib",
        "pathlib",
        "os.",
        "subprocess",
        "socket",
        "requests",
        "httpx",
        "open(",
        "run_main_once(",
    ):
        assert forbidden not in source
    assert 'if __name__ ==' not in source
