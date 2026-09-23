from __future__ import annotations

from types import SimpleNamespace

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_git_backend_generation2
    as backend,
)


def test_contract_is_exact_pair06_baseline_and_nonexecuting():
    out = backend.pair06_v8_baseline_git_backend_contract()
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["fixed_source_root"] == (
        "/home/zoso/dev/openra-rl-war-college"
    )
    assert out["fixed_arm_root"].endswith(
        "/v8-generation2/generation2/pair-06/baseline"
    )
    assert out["frozen_source_commit"] == (
        "973802ef0a614e5afa782ff20e231e18966ae3e5"
    )
    assert out["frozen_engine_commit"] == (
        "1607a7a6501d42a47638393ecef8b22831064932"
    )
    assert out["fetch_implemented"] is False
    assert out["force_remove_implemented"] is False
    assert out["network_protocol_allowed"] is False
    assert out["runtime_execution_authorized"] is False
    assert out["runtime_execution_performed"] is False
    assert out["automatic_retry"] is False


def test_backend_requires_exact_confirmation():
    with pytest.raises(
        backend.Pair06V8BaselineGitHold,
        match="PAIR06_V8_GIT_CONFIRMATION_REQUIRED",
    ):
        backend.Pair06V8BaselineGitBackend(confirm="wrong")


def test_binding_allows_only_exact_known_roots_and_destinations():
    value = backend.Pair06V8BaselineGitBackend(
        confirm=backend.CONFIRM_TOKEN
    )
    for row in backend._BINDINGS:
        canonical, destination, _ = row
        assert value._binding(canonical) == row
        assert value._binding(destination) == row

    with pytest.raises(
        backend.Pair06V8BaselineGitHold,
        match="PAIR06_V8_GIT_PATH_NOT_ALLOWED",
    ):
        value._binding("/tmp/not-allowed")


def test_run_git_rejects_unlisted_command(monkeypatch):
    value = backend.Pair06V8BaselineGitBackend(
        confirm=backend.CONFIRM_TOKEN
    )
    monkeypatch.setattr(
        backend,
        "_directory",
        lambda path: SimpleNamespace(st_dev=1, st_ino=2),
    )
    with pytest.raises(
        backend.Pair06V8BaselineGitHold,
        match="PAIR06_V8_GIT_COMMAND_NOT_ALLOWED",
    ):
        value.run_git(
            backend.SOURCE_ROOT,
            "push",
            "origin",
            "main",
        )


def test_environment_disables_network_and_ambient_git_configuration():
    env = backend._environment()
    assert env["GIT_TERMINAL_PROMPT"] == "0"
    assert env["GIT_CONFIG_NOSYSTEM"] == "1"
    assert env["GIT_CONFIG_GLOBAL"] == "/dev/null"
    assert env["GIT_NO_LAZY_FETCH"] == "1"
