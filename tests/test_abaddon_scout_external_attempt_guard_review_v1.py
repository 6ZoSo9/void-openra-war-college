"""Source-binding tests for the durable scout attempt guard review."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_external_attempt_guard_review_v1 as review
from openra_env.learning import abaddon_scout_external_attempt_guard_v1 as guard
from openra_env.learning import abaddon_scout_external_launcher_contract_review_v1 as launcher_review
from openra_env.learning import abaddon_scout_external_launcher_contract_v1 as launcher


ROOT = Path(__file__).resolve().parents[1]
HOLD = review.ScoutExternalAttemptGuardReviewHold


def _git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def test_review_binds_exact_launcher_review_and_attempt_guard_sources():
    expected = {
        review.LAUNCHER_CONTRACT_PATH: review.LAUNCHER_CONTRACT_GIT_BLOB,
        review.LAUNCHER_REVIEW_PATH: review.LAUNCHER_REVIEW_GIT_BLOB,
        review.ATTEMPT_GUARD_PATH: review.ATTEMPT_GUARD_GIT_BLOB,
    }
    assert expected == {
        "openra_env/learning/abaddon_scout_external_launcher_contract_v1.py":
            "1f7ee7057c27946f488afe26501482ea4f4fc53d",
        "openra_env/learning/abaddon_scout_external_launcher_contract_review_v1.py":
            "3b6281b6a7bcaa9d5b3d9300728103883a810a6c",
        "openra_env/learning/abaddon_scout_external_attempt_guard_v1.py":
            "043225a7ff6528b9ae7f80994fe17480ad36ed3e",
    }

    for relative, expected_blob in expected.items():
        path = ROOT / relative
        assert path.is_file() and not path.is_symlink()
        assert _git_blob(path.read_bytes()) == expected_blob

    assert launcher.REQUEST_SHA256 == review.REQUEST_SHA256
    assert launcher_review.CONTRACT_REQUEST_SHA256 == review.REQUEST_SHA256
    assert guard.review.CONTRACT_GIT_BLOB == review.LAUNCHER_CONTRACT_GIT_BLOB


def test_review_contract_is_non_authorizing_and_points_to_result_binding():
    receipt = review.attempt_guard_source_review_contract()

    assert receipt["main_head"] == "9a151da589f93454d31a475b29297ea8a3d35442"
    assert receipt["review_kind"] == "source_binding_expectation_not_runtime_authority"
    assert receipt["attempt_guard_source_identity_recorded"] is True
    assert receipt["pair03_attempt_reuse_allowed"] is False
    assert receipt["pair03_attempt_reset_allowed"] is False
    assert receipt["automatic_retry"] is False
    assert receipt["next_gate"] == "SCOUT_EXTERNAL_RESULT_BINDING_REQUIRED"

    assert len(receipt["authority"]) == len(review.FALSE_AUTHORITY_FIELDS)
    assert set(receipt["authority"]) == set(review.FALSE_AUTHORITY_FIELDS)
    assert all(value is False for value in receipt["authority"].values())


@pytest.mark.parametrize(
    ("entrypoint", "kwargs"),
    [
        (review.consume_attempt, {}),
        (review.consume_attempt, {"confirm": guard.CLAIM_CONFIRMATION}),
        (review.authorize_or_execute, {}),
        (review.authorize_or_execute, {"authorized": True}),
        (review.accept_result, {}),
        (review.accept_result, {"verified": True}),
    ],
)
def test_all_effect_or_result_entrypoints_hold(entrypoint, kwargs):
    with pytest.raises(HOLD, match=review.NEXT_GATE):
        entrypoint(**kwargs)


def test_review_snapshot_is_fresh():
    first = review.attempt_guard_source_review_contract()
    first["source_references"].clear()
    first["authority"]["scout_execution_authorized"] = True

    later = review.attempt_guard_source_review_contract()
    assert len(later["source_references"]) == 3
    assert later["authority"]["scout_execution_authorized"] is False


def test_review_source_has_no_runtime_filesystem_network_or_local_imports():
    path = ROOT / "openra_env/learning/abaddon_scout_external_attempt_guard_review_v1.py"
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
