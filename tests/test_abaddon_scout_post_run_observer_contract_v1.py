"""Tests for the pure scout post-run observer contract."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_post_run_observer_contract_v1 as contract


ROOT = Path(__file__).resolve().parents[1]
HOLD = contract.ScoutPostRunObserverContractHold


def test_contract_requires_independent_observation_and_no_shutdown_shortcuts():
    receipt = contract.post_run_observer_contract()

    assert receipt["evidence_schema"] == "void.abaddon.scout-post-run-state-evidence.v1"
    assert tuple(receipt["required_observations"]) == contract.REQUIRED_OBSERVATIONS
    assert tuple(receipt["false_claims"]) == contract.FALSE_CLAIMS
    assert receipt["independent_observation_required"] is True
    assert receipt["callback_return_is_shutdown_proof"] is False
    assert receipt["historical_cleanup_print_is_shutdown_proof"] is False
    assert receipt["next_gate"] == "SCOUT_POST_RUN_OBSERVER_IMPLEMENTATION_REVIEW_REQUIRED"

    assert set(receipt["authority"]) == set(contract.FALSE_AUTHORITY_FIELDS)
    assert all(value is False for value in receipt["authority"].values())


def test_contract_snapshot_is_fresh():
    first = contract.post_run_observer_contract()
    first["required_observations"].clear()
    first["authority"]["post_run_state_verified"] = True

    later = contract.post_run_observer_contract()
    assert tuple(later["required_observations"]) == contract.REQUIRED_OBSERVATIONS
    assert later["authority"]["post_run_state_verified"] is False


@pytest.mark.parametrize(
    ("entrypoint", "kwargs"),
    [
        (contract.observe_host_state, {}),
        (contract.observe_host_state, {"read_only": True}),
        (contract.accept_result, {}),
        (contract.accept_result, {"verified": True}),
        (contract.authorize_or_execute, {}),
        (contract.authorize_or_execute, {"authorized": True}),
    ],
)
def test_effectful_acceptance_and_execution_entrypoints_hold(entrypoint, kwargs):
    with pytest.raises(HOLD, match=contract.NEXT_GATE):
        entrypoint(**kwargs)


def test_contract_source_has_no_host_observation_or_runtime_imports():
    path = ROOT / "openra_env/learning/abaddon_scout_post_run_observer_contract_v1.py"
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
        "pathlib",
        "hashlib",
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
