from __future__ import annotations

from pathlib import Path
import subprocess

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_git_backend_generation2
    as backend,
)

HOLD = backend.V2R13Pair09CandidateGitHold


def git(root, *args):
    return subprocess.run(
        ["/usr/bin/git", "-C", str(root), *args],
        env=backend._environment(),
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    ).stdout.strip()


@pytest.fixture
def repositories(tmp_path, monkeypatch):
    rows = []
    arm = tmp_path / "generation2/pair-09/candidate"
    arm.mkdir(parents=True)
    baseline = arm.parent / "baseline"
    baseline.mkdir()
    (baseline / "comparison.json").write_bytes(
        b"preserved-pair09-baseline-evidence\n"
    )

    for label, leaf in (("source", "frozen-source"), ("engine", "engine")):
        root = tmp_path / label
        root.mkdir()
        git(root, "init", "--initial-branch=main")
        (root / "tracked.txt").write_text(label + " frozen content\n")
        git(root, "add", "tracked.txt")
        git(
            root,
            "-c", "user.name=Fixture",
            "-c", "user.email=fixture@example.invalid",
            "-c", "commit.gpgsign=false",
            "commit", "-m", "inert fixture",
        )
        frozen = git(root, "rev-parse", "HEAD")
        rows.append((str(root), str(arm / leaf), frozen))

    monkeypatch.setattr(backend, "_BINDINGS", tuple(rows))
    return rows, baseline


def new_backend():
    return backend.Pair09CandidateGitBackend(confirm=backend.CONFIRM_TOKEN)


def test_production_bindings_are_exact_pair09_candidate():
    first, second = backend._BINDINGS
    expected = (
        "/home/zoso/dev/void-war-college-execution/v2r13-generation2/"
        "generation2/pair-09/candidate/"
    )
    assert first == (
        "/home/zoso/dev/openra-rl-war-college",
        expected + "frozen-source",
        "973802ef0a614e5afa782ff20e231e18966ae3e5",
    )
    assert second == (
        "/home/zoso/dev/openra-rl-war-college/OpenRA",
        expected + "engine",
        "1607a7a6501d42a47638393ecef8b22831064932",
    )


def test_real_two_worktree_sequence_and_cleanup(repositories):
    rows, baseline = repositories
    runner = new_backend()
    before = {
        root: (
            git(root, "rev-parse", "HEAD"),
            git(root, "status", "--porcelain"),
            git(root, "branch", "--show-current"),
        )
        for root, _, _ in rows
    }

    for root, destination, commit in rows:
        assert runner.path_exists(root) is True
        assert runner.path_exists(destination) is False
        runner.run_git(
            root,
            "worktree", "add", "--detach", destination, commit,
        )
        assert runner.path_exists(destination) is True
        assert (
            runner.run_git(destination, "rev-parse", "HEAD").stdout.strip()
            == commit
        )
        assert (
            runner.run_git(
                destination,
                "status", "--porcelain", "--untracked-files=all",
            ).stdout
            == ""
        )
        assert (
            runner.run_git(destination, "symbolic-ref", "-q", "HEAD").returncode
            == 1
        )

    for root, destination, _ in reversed(rows):
        runner.run_git(root, "worktree", "remove", destination)
        assert runner.path_exists(destination) is False

    after = {
        root: (
            git(root, "rev-parse", "HEAD"),
            git(root, "status", "--porcelain"),
            git(root, "branch", "--show-current"),
        )
        for root, _, _ in rows
    }
    assert after == before
    assert (
        baseline / "comparison.json"
    ).read_bytes() == b"preserved-pair09-baseline-evidence\n"


@pytest.mark.parametrize(
    "confirmation",
    [None, True, "", "VOID_ABADDON_GENERATION2_V2R13_EXECUTE_PAIR09_CANDIDATE_ONCE"],
)
def test_wrong_confirmation_performs_no_observation_or_command(
    monkeypatch,
    confirmation,
):
    def forbidden(*args):
        raise AssertionError("host access")

    monkeypatch.setattr(backend, "_directory", forbidden)
    monkeypatch.setattr(backend, "_capture", forbidden)
    with pytest.raises(HOLD, match="CONFIRMATION_REQUIRED"):
        backend.Pair09CandidateGitBackend(confirm=confirmation)


@pytest.mark.parametrize(
    "args",
    [
        ("fetch", "origin"),
        ("reset", "--hard", "HEAD"),
        ("checkout", "HEAD"),
        ("clean", "-fd"),
        ("config", "--list"),
        ("worktree", "prune"),
    ],
)
def test_forbidden_git_commands_reject_before_subprocess(
    repositories,
    monkeypatch,
    args,
):
    root = repositories[0][0][0]

    def forbidden(*unused):
        raise AssertionError("forbidden subprocess reached")

    monkeypatch.setattr(backend, "_capture", forbidden)
    with pytest.raises(HOLD, match="COMMAND_NOT_ALLOWED"):
        new_backend().run_git(root, *args)


def test_other_pair_destination_is_rejected(repositories, monkeypatch):
    rows, _ = repositories
    root, destination, commit = rows[0]
    other = destination.replace("/pair-09/", "/pair-03/")

    def forbidden(*unused):
        raise AssertionError("forbidden subprocess reached")

    monkeypatch.setattr(backend, "_capture", forbidden)
    with pytest.raises(HOLD):
        new_backend().run_git(
            root,
            "worktree", "add", "--detach", other, commit,
        )


def test_only_same_instance_created_inode_can_be_removed(repositories):
    rows, _ = repositories
    root, destination, commit = rows[0]
    first = new_backend()
    first.run_git(root, "worktree", "add", "--detach", destination, commit)
    with pytest.raises(HOLD, match="CLEANUP_NOT_OWNED"):
        new_backend().run_git(root, "worktree", "remove", destination)


def test_add_cannot_repeat_after_successful_cleanup(repositories):
    rows, _ = repositories
    root, destination, commit = rows[0]
    runner = new_backend()
    runner.run_git(root, "worktree", "add", "--detach", destination, commit)
    runner.run_git(root, "worktree", "remove", destination)
    with pytest.raises(HOLD, match="ADD_ALREADY_ATTEMPTED"):
        runner.run_git(root, "worktree", "add", "--detach", destination, commit)


def test_backend_contract_grants_no_runtime_authority():
    out = backend.pair09_candidate_git_backend_contract()
    assert out["pair09_candidate_git_backend_implemented"] is True
    assert out["pair09_candidate_git_backend_reviewed"] is False
    assert out["pair_slot"] == 9
    assert out["arm"] == "candidate"
    assert out["held_out"] is False
    assert out["binding_count"] == 2
    assert out["fetch_implemented"] is False
    assert out["canonical_checkout_implemented"] is False
    assert out["force_remove_implemented"] is False
    assert out["reset_implemented"] is False
    assert out["clean_implemented"] is False
    assert out["config_implemented"] is False
    assert out["prune_implemented"] is False
    assert out["runtime_execution_authorized"] is False
    assert out["runtime_execution_performed"] is False
    assert out["model_inference_performed"] is False
    assert out["game_execution_performed"] is False
    assert out["training_performed"] is False
    assert out["next_gate"] == (
        "V2R13_PAIR09_CANDIDATE_GIT_BACKEND_SOURCE_BINDING_REVIEW_REQUIRED"
    )
