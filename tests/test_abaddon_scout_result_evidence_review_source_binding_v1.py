"""Tests for scout evidence-review source binding."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_result_evidence_review_source_binding_v1 as review


ROOT = Path(__file__).resolve().parents[1]
HOLD = review.ScoutResultEvidenceReviewSourceBindingHold


def _git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def test_binding_matches_exact_evidence_review_and_observer_contract_sources():
    expected = {
        review.EVIDENCE_REVIEW_PATH: review.EVIDENCE_REVIEW_GIT_BLOB,
        review.OBSERVER_CONTRACT_PATH: review.OBSERVER_CONTRACT_GIT_BLOB,
    }
    assert expected == {
        "openra_env/learning/abaddon_scout_external_result_evidence_review_v1.py":
            "3c703599877c4bf18aeabcf848b85e9b5a517e95",
        "openra_env/learning/abaddon_scout_post_run_observer_contract_v1.py":
            "fd71ac745c10349047d49f753ecfce1aab712648",
    }

    for relative, expected_blob in expected.items():
        path = ROOT / relative
        assert path.is_file() and not path.is_symlink()
        assert _git_blob(path.read_bytes()) == expected_blob


def test_binding_is_source_only_and_points_to_implementation_review():
    receipt = review.result_evidence_review_source_binding_contract()

    assert receipt["main_head"] == "9a151da589f93454d31a475b29297ea8a3d35442"
    assert receipt["review_kind"] == "source_binding_expectation_not_host_observation"
    assert receipt["observer_contract_source_identity_recorded"] is True
    assert receipt["evidence_review_source_identity_recorded"] is True
    assert receipt["next_gate"] == "SCOUT_POST_RUN_OBSERVER_IMPLEMENTATION_REVIEW_REQUIRED"

    assert set(receipt["authority"]) == set(review.FALSE_AUTHORITY_FIELDS)
    assert all(value is False for value in receipt["authority"].values())


@pytest.mark.parametrize(
    ("entrypoint", "kwargs"),
    [
        (review.observe_host_state, {}),
        (review.observe_host_state, {"read_only": True}),
        (review.accept_result, {}),
        (review.accept_result, {"verified": True}),
        (review.authorize_or_execute, {}),
        (review.authorize_or_execute, {"authorized": True}),
    ],
)
def test_host_observation_acceptance_and_execution_entrypoints_hold(entrypoint, kwargs):
    with pytest.raises(HOLD, match=review.NEXT_GATE):
        entrypoint(**kwargs)


def test_binding_snapshot_is_fresh():
    first = review.result_evidence_review_source_binding_contract()
    first["source_references"].clear()
    first["authority"]["host_observer_implemented"] = True

    later = review.result_evidence_review_source_binding_contract()
    assert len(later["source_references"]) == 2
    assert later["authority"]["host_observer_implemented"] is False


def test_source_has_no_host_filesystem_process_network_or_local_imports():
    path = ROOT / "openra_env/learning/abaddon_scout_result_evidence_review_source_binding_v1.py"
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
        "json",
        "os.",
        "subprocess",
        "socket",
        "requests",
        "httpx",
        "open(",
        "systemctl",
        "docker",
    ):
        assert forbidden not in source
    assert 'if __name__ ==' not in source
