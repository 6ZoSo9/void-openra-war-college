"""Tests for the scout post-run observer source review."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_post_run_observer_review_v1 as review


ROOT = Path(__file__).resolve().parents[1]
HOLD = review.ScoutPostRunObserverSourceReviewHold


def _git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def test_review_binds_exact_observer_contract_and_adapter_sources():
    expected = {
        review.OBSERVER_CONTRACT_PATH: review.OBSERVER_CONTRACT_GIT_BLOB,
        review.OBSERVER_IMPLEMENTATION_PATH: review.OBSERVER_IMPLEMENTATION_GIT_BLOB,
    }
    assert expected == {
        "openra_env/learning/abaddon_scout_post_run_observer_contract_v1.py":
            "fd71ac745c10349047d49f753ecfce1aab712648",
        "openra_env/learning/abaddon_scout_post_run_observer_v1.py":
            "11dfa40a861e6772258178bbc32840c670e47f9f",
    }

    for relative, expected_blob in expected.items():
        path = ROOT / relative
        assert path.is_file() and not path.is_symlink()
        assert _git_blob(path.read_bytes()) == expected_blob


def test_review_keeps_effectful_backend_binding_closed():
    receipt = review.post_run_observer_source_review_contract()

    assert receipt["main_head"] == "9a151da589f93454d31a475b29297ea8a3d35442"
    assert receipt["review_kind"] == "source_binding_expectation_not_host_backend_binding"
    assert receipt["observer_contract_source_identity_recorded"] is True
    assert receipt["observer_implementation_source_identity_recorded"] is True
    assert receipt["next_gate"] == "SCOUT_POST_RUN_OBSERVER_BACKEND_BINDING_REQUIRED"

    assert set(receipt["authority"]) == set(review.FALSE_AUTHORITY_FIELDS)
    assert all(value is False for value in receipt["authority"].values())


@pytest.mark.parametrize(
    ("entrypoint", "kwargs"),
    [
        (review.bind_host_backend, {}),
        (review.bind_host_backend, {"read_only": True}),
        (review.observe_host_state, {}),
        (review.observe_host_state, {"authorized": True}),
        (review.accept_result, {}),
        (review.accept_result, {"verified": True}),
    ],
)
def test_backend_observation_and_acceptance_entrypoints_hold(entrypoint, kwargs):
    with pytest.raises(HOLD, match=review.NEXT_GATE):
        entrypoint(**kwargs)


def test_review_snapshot_is_fresh():
    first = review.post_run_observer_source_review_contract()
    first["source_references"].clear()
    first["authority"]["host_backend_bound"] = True

    later = review.post_run_observer_source_review_contract()
    assert len(later["source_references"]) == 2
    assert later["authority"]["host_backend_bound"] is False


def test_review_source_has_no_host_backend_or_runtime_imports():
    path = ROOT / "openra_env/learning/abaddon_scout_post_run_observer_review_v1.py"
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
        "systemctl",
        "docker",
        "git ",
        "open(",
    ):
        assert forbidden not in source
    assert 'if __name__ ==' not in source
