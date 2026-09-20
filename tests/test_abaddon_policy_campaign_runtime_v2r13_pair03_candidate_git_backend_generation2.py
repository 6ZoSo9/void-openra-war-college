"""Actual temporary Git worktrees; no Precision, model or game execution."""

from __future__ import annotations

import ast
from pathlib import Path
import os
import subprocess
import sys
import time

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_git_backend_generation2 as backend,
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_authorization_request_generation2 as request,
)

HOLD = backend.CandidateGitHold


def git(root, *args):
    return subprocess.run(
        ["/usr/bin/git", "-C", str(root), *args], env=backend._environment(),
        stdin=subprocess.DEVNULL, capture_output=True, text=True, check=True, timeout=10,
    ).stdout.strip()


@pytest.fixture
def repositories(tmp_path, monkeypatch):
    rows = []
    arm = tmp_path / "generation2/pair-03/candidate"
    arm.mkdir(parents=True)
    baseline = arm.parent / "baseline"
    baseline.mkdir()
    (baseline / "comparison.json").write_bytes(b"preserved-baseline-evidence\n")
    for label, leaf in (("source", "frozen-source"), ("engine", "engine")):
        root = tmp_path / label
        root.mkdir()
        git(root, "init", "--initial-branch=main")
        (root / "tracked.txt").write_text(label + " frozen content\n")
        git(root, "add", "tracked.txt")
        git(root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
            "-c", "commit.gpgsign=false", "commit", "-m", "inert fixture")
        frozen = git(root, "rev-parse", "HEAD")
        rows.append((str(root), str(arm / leaf), frozen))
    monkeypatch.setattr(backend, "_BINDINGS", tuple(rows))
    return rows, baseline


def new_backend():
    return backend.CandidateGitBackend(confirm=backend.CONFIRM_TOKEN)


def test_exact_production_destinations_and_commits_match_accepted_request():
    reference = request.candidate_authorization_request_contract()["request"]["runtime_reference"]
    first, second = backend._BINDINGS
    assert first[0] == "/home/zoso/dev/openra-rl-war-college"
    assert second[0] == first[0] + "/OpenRA"
    expected = "/home/zoso/dev/void-war-college-execution/v2r13-generation2/generation2/pair-03/candidate/"
    assert first[1] == expected + "frozen-source"
    assert second[1] == expected + "engine"
    assert first[2] == reference["frozen_war_college_commit"]
    assert second[2] == reference["frozen_engine_commit"]


def test_real_two_worktree_materializer_command_sequence_and_cleanup(repositories):
    rows, baseline = repositories
    runner = new_backend()
    before = {root: (git(root, "rev-parse", "HEAD"), git(root, "status", "--porcelain"),
                     git(root, "branch", "--show-current")) for root, _, _ in rows}
    for root, destination, commit in rows:
        assert runner.path_exists(root) is True
        assert runner.path_exists(destination) is False
        for args in (("rev-parse", "--show-toplevel"), ("rev-parse", "HEAD"),
                     ("rev-parse", "HEAD^{tree}"), ("status", "--porcelain", "--untracked-files=all"),
                     ("rev-parse", "--verify", commit + "^{commit}"),
                     ("rev-parse", commit + "^{tree}"), ("worktree", "list", "--porcelain")):
            assert runner.run_git(root, *args).returncode == 0
        runner.run_git(root, "worktree", "add", "--detach", destination, commit)
        assert runner.path_exists(destination) is True
        assert runner.run_git(destination, "rev-parse", "HEAD").stdout.strip() == commit
        assert runner.run_git(destination, "rev-parse", "--show-toplevel").stdout.strip() == destination
        assert runner.run_git(destination, "rev-parse", "HEAD^{tree}").stdout.strip() == git(root, "rev-parse", commit + "^{tree}")
        assert runner.run_git(destination, "status", "--porcelain", "--untracked-files=all").stdout == ""
        assert runner.run_git(destination, "symbolic-ref", "-q", "HEAD").returncode == 1
        assert destination in runner.run_git(root, "worktree", "list", "--porcelain").stdout
    for root, destination, _ in reversed(rows):
        runner.run_git(root, "worktree", "remove", destination)
        assert runner.path_exists(destination) is False
        assert destination not in runner.run_git(root, "worktree", "list", "--porcelain").stdout
    assert before == {root: (git(root, "rev-parse", "HEAD"), git(root, "status", "--porcelain"),
                            git(root, "branch", "--show-current")) for root, _, _ in rows}
    assert (baseline / "comparison.json").read_bytes() == b"preserved-baseline-evidence\n"
    assert all(git(root, "branch", "--list").strip() == "* main" for root, _, _ in rows)


@pytest.mark.parametrize("confirmation", [None, True, "", "VOID_ABADDON_GENERATION2_V2R13_EXECUTE_PAIR03_BASELINE"])
def test_wrong_confirmation_performs_no_observation_or_command(monkeypatch, confirmation):
    def forbidden(*args):
        raise AssertionError("host access")
    monkeypatch.setattr(backend, "_directory", forbidden)
    monkeypatch.setattr(backend, "_capture", forbidden)
    with pytest.raises(HOLD, match="CONFIRMATION_REQUIRED"):
        backend.CandidateGitBackend(confirm=confirmation)


@pytest.mark.parametrize("kind", [
    "baseline", "held_out", "other_pair", "traversal", "dot", "slash", "suffix", "root",
    "relative", "nul", "wrong_repository", "swap_destinations", "swap_commits", "head_alias",
    "branch_alias", "uppercase_commit", "force_add", "force_remove", "canonical_remove",
    "fetch", "reset", "checkout", "clean", "config", "prune", "empty", "non_string", "leading_option",
])
def test_out_of_scope_commands_reject_before_subprocess(repositories, monkeypatch, kind):
    rows, _ = repositories
    root, destination, commit = rows[0]
    args = ("worktree", "add", "--detach", destination, commit)
    replacements = {
        "baseline": destination.replace("/candidate/", "/baseline/"),
        "held_out": destination.replace("/pair-03/", "/pair-15/"),
        "other_pair": destination.replace("/pair-03/", "/pair-09/"),
        "traversal": destination + "/../engine", "dot": destination + "/.",
        "slash": destination + "/", "suffix": destination + "-other", "root": "/",
        "relative": "candidate/frozen-source", "nul": destination + "\x00",
    }
    if kind in replacements:
        args = ("worktree", "add", "--detach", replacements[kind], commit)
    elif kind == "wrong_repository": root = rows[1][0]
    elif kind == "swap_destinations": args = ("worktree", "add", "--detach", rows[1][1], commit)
    elif kind == "swap_commits": args = ("worktree", "add", "--detach", destination, rows[1][2])
    elif kind in {"head_alias", "branch_alias", "uppercase_commit"}:
        ref = {"head_alias": "HEAD", "branch_alias": "main", "uppercase_commit": commit.upper()}[kind]
        args = ("worktree", "add", "--detach", destination, ref)
    elif kind == "force_add": args = ("worktree", "add", "--force", destination, commit)
    elif kind == "force_remove": args = ("worktree", "remove", "--force", destination)
    elif kind == "canonical_remove": args = ("worktree", "remove", root)
    elif kind == "fetch": args = ("fetch", "origin")
    elif kind == "reset": args = ("reset", "--hard", commit)
    elif kind == "checkout": args = ("checkout", commit)
    elif kind == "clean": args = ("clean", "-fd")
    elif kind == "config": args = ("config", "--list")
    elif kind == "prune": args = ("worktree", "prune")
    elif kind == "empty": args = ()
    elif kind == "non_string": args = ("rev-parse", True)
    elif kind == "leading_option": args = ("-c", "core.hooksPath=other", "status")
    def forbidden(*args):
        raise AssertionError("forbidden subprocess reached")
    monkeypatch.setattr(backend, "_capture", forbidden)
    with pytest.raises(HOLD): new_backend().run_git(root, *args)


@pytest.mark.parametrize("mutation", ["unknown", "slash", "relative", "wrong_type"])
def test_path_query_is_exactly_scoped(repositories, mutation):
    rows, _ = repositories
    path = {"unknown": str(Path(rows[0][1]).parent.parent / "baseline"),
            "slash": rows[0][0] + "/", "relative": "source", "wrong_type": Path(rows[0][0])}[mutation]
    with pytest.raises(HOLD, match="PATH_NOT_ALLOWED"): new_backend().path_exists(path)


@pytest.mark.parametrize("kind", ["directory", "file", "dangling", "ancestor_link"])
def test_existing_or_linked_destination_is_preserved(repositories, monkeypatch, kind):
    rows, _ = repositories
    root, destination, commit = rows[0]
    path = Path(destination)
    if kind == "directory": path.mkdir()
    elif kind == "file": path.write_bytes(b"foreign")
    elif kind == "dangling": path.symlink_to(path.parent / "absent")
    else:
        actual = path.parent.with_name("retained-candidate")
        path.parent.rename(actual)
        path.parent.symlink_to(actual, target_is_directory=True)
    def forbidden(*args): raise AssertionError("unexpected command")
    monkeypatch.setattr(backend, "_capture", forbidden)
    with pytest.raises(HOLD): new_backend().run_git(root, "worktree", "add", "--detach", destination, commit)
    assert path.lstat() if kind != "ancestor_link" else path.parent.is_symlink()


def test_missing_parent_is_not_created(repositories):
    rows, _ = repositories
    root, destination, commit = rows[0]
    parent = Path(destination).parent
    parent.rmdir()
    with pytest.raises(HOLD, match="PARENT_MISSING"):
        new_backend().run_git(root, "worktree", "add", "--detach", destination, commit)
    assert not parent.exists()


def test_only_instance_created_inode_can_be_removed(repositories):
    rows, _ = repositories
    root, destination, commit = rows[0]
    first = new_backend()
    first.run_git(root, "worktree", "add", "--detach", destination, commit)
    with pytest.raises(HOLD, match="CLEANUP_NOT_OWNED"):
        new_backend().run_git(root, "worktree", "remove", destination)
    original = Path(destination)
    retained = original.with_name("retained-original")
    original.rename(retained)
    original.mkdir()
    with pytest.raises(HOLD, match="CLEANUP_NOT_OWNED"):
        first.run_git(root, "worktree", "remove", destination)
    assert retained.is_dir() and original.is_dir()


def test_dirty_worktree_cleanup_refuses_without_force(repositories):
    rows, baseline = repositories
    root, destination, commit = rows[0]
    runner = new_backend()
    runner.run_git(root, "worktree", "add", "--detach", destination, commit)
    (Path(destination) / "untracked.txt").write_bytes(b"retain this evidence")
    with pytest.raises(HOLD, match="COMMAND_FAILED"):
        runner.run_git(root, "worktree", "remove", destination)
    assert (Path(destination) / "untracked.txt").read_bytes() == b"retain this evidence"
    assert (baseline / "comparison.json").is_file()


def test_add_cannot_repeat_even_after_successful_cleanup(repositories):
    rows, _ = repositories
    root, destination, commit = rows[0]
    runner = new_backend()
    runner.run_git(root, "worktree", "add", "--detach", destination, commit)
    runner.run_git(root, "worktree", "remove", destination)
    with pytest.raises(HOLD, match="ADD_ALREADY_ATTEMPTED"):
        runner.run_git(root, "worktree", "add", "--detach", destination, commit)


def test_ambiguous_add_is_not_adopted_or_retried(repositories, monkeypatch):
    rows, _ = repositories
    root, destination, commit = rows[0]
    runner = new_backend()
    calls = []
    def partial(argv):
        calls.append(argv)
        Path(destination).mkdir()
        (Path(destination) / "residue").write_bytes(b"uncertain")
        raise HOLD("CANDIDATE_GIT_TIMEOUT")
    monkeypatch.setattr(backend, "_capture", partial)
    with pytest.raises(HOLD, match="TIMEOUT"):
        runner.run_git(root, "worktree", "add", "--detach", destination, commit)
    with pytest.raises(HOLD, match="ADD_ALREADY_ATTEMPTED"):
        runner.run_git(root, "worktree", "add", "--detach", destination, commit)
    with pytest.raises(HOLD, match="CLEANUP_NOT_OWNED"):
        runner.run_git(root, "worktree", "remove", destination)
    assert len(calls) == 1 and (Path(destination) / "residue").read_bytes() == b"uncertain"


def test_ambient_git_settings_and_checkout_hook_are_not_used(repositories, monkeypatch, tmp_path):
    rows, _ = repositories
    root, destination, commit = rows[0]
    hook_dir = tmp_path / "fixture-hooks"
    hook_dir.mkdir()
    signal_file = tmp_path / "hook-ran"
    hook = hook_dir / "post-checkout"
    hook.write_text("#!/bin/sh\nprintf ran > '" + str(signal_file) + "'\n")
    hook.chmod(0o755)
    git(root, "config", "core.hooksPath", str(hook_dir))
    monkeypatch.setenv("GIT_DIR", str(Path(rows[1][0]) / ".git"))
    monkeypatch.setenv("GIT_WORK_TREE", rows[1][0])
    monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
    monkeypatch.setenv("GIT_CONFIG_KEY_0", "core.hooksPath")
    monkeypatch.setenv("GIT_CONFIG_VALUE_0", str(hook_dir))
    runner = new_backend()
    assert runner.run_git(root, "rev-parse", "--show-toplevel").stdout.strip() == root
    runner.run_git(root, "worktree", "add", "--detach", destination, commit)
    assert not signal_file.exists()
    runner.run_git(root, "worktree", "remove", destination)


@pytest.mark.parametrize("exit_code", [1, 2, 128])
def test_nonzero_result_is_only_allowed_for_detached_probe(repositories, monkeypatch, exit_code):
    root = repositories[0][0][0]
    monkeypatch.setattr(backend, "_capture", lambda argv: subprocess.CompletedProcess(argv, exit_code, "", "fixture"))
    runner = new_backend()
    with pytest.raises(HOLD, match="COMMAND_FAILED"): runner.run_git(root, "rev-parse", "HEAD")
    if exit_code == 1:
        assert runner.run_git(root, "symbolic-ref", "-q", "HEAD").returncode == 1
    else:
        with pytest.raises(HOLD): runner.run_git(root, "symbolic-ref", "-q", "HEAD")


def test_capture_preserves_both_streams():
    out = backend._capture([sys.executable, "-I", "-S", "-B", "-c", "import sys; print('out'); print('err',file=sys.stderr)"])
    assert out.stdout == "out\n" and out.stderr == "err\n" and out.returncode == 0


@pytest.mark.parametrize("fault", ["timeout", "stdout", "stderr", "invalid_utf8"])
def test_capture_bounds_and_closes_owned_descriptors(monkeypatch, fault):
    before = len(list(Path("/proc/self/fd").iterdir()))
    monkeypatch.setattr(backend, "COMMAND_TIMEOUT_SECONDS", 0.2 if fault == "timeout" else 5.0)
    monkeypatch.setattr(backend, "MAX_OUTPUT_BYTES", 1024)
    programs = {
        "timeout": "import time; time.sleep(30)",
        "stdout": "import os; os.write(1, b'x'*4096)",
        "stderr": "import os; os.write(2, b'x'*4096)",
        "invalid_utf8": "import os; os.write(1,b'\\xff')",
    }
    started = time.monotonic()
    expected = "TIMEOUT" if fault == "timeout" else "TRANSPORT_HOLD" if fault == "invalid_utf8" else "OUTPUT_BOUND"
    with pytest.raises(HOLD, match=expected):
        backend._capture([sys.executable, "-I", "-S", "-B", "-c", programs[fault]])
    assert time.monotonic() - started < 3
    assert len(list(Path("/proc/self/fd").iterdir())) == before
    monkeypatch.setattr(backend, "COMMAND_TIMEOUT_SECONDS", 5.0)
    assert backend._capture([sys.executable, "-I", "-S", "-B", "-c", "print('recovered')"]).stdout == "recovered\n"


def test_import_has_no_runtime_dependencies_or_cli():
    source = Path(backend.__file__).read_text()
    tree = ast.parse(source)
    imports = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}
    imports.update(alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names)
    assert imports == {"__future__", "os", "pathlib", "selectors", "signal", "stat", "subprocess", "time"}
    assert 'if __name__ ==' not in source
    assert "execute_v2r13_arm(" not in source and "consume_candidate_attempt(" not in source


@pytest.mark.parametrize("scenario", ["normal", "dirty_engine", "engine_add_failure"])
def test_complete_checkout_actual_materializer_integration(repositories, monkeypatch, scenario):
    # Execute the existing operational materializer and cleanup, with only its
    # static authority/path admission and frozen identities replaced for the
    # two synthetic repositories. This is not production authority validation.
    from types import SimpleNamespace
    from openra_env.learning import (
        abaddon_policy_campaign_runtime_v2r13_frozen_worktree_materializer_generation2 as materializer,
    )
    rows, baseline = repositories
    source, engine = rows
    paths = {"frozen_source_root": source[1], "exact_engine_root": engine[1]}
    path_record = {"fixture_only": True, "paths": paths}
    monkeypatch.setattr(materializer, "_validate_dependencies", lambda: {})
    monkeypatch.setattr(materializer, "portable_checkout", SimpleNamespace(
        FROZEN_WAR_COLLEGE_COMMIT=source[2],
        FROZEN_WAR_COLLEGE_TREE=git(source[0], "rev-parse", source[2] + "^{tree}"),
        FROZEN_ENGINE_COMMIT=engine[2],
    ))
    monkeypatch.setattr(materializer, "path_inputs", SimpleNamespace(
        V2R13="synthetic-materializer-composition",
        validate_explicit_path_inputs=lambda key, record: {"paths": record["paths"]},
    ))
    runner = new_backend()
    original_capture = backend._capture
    if scenario == "engine_add_failure":
        def fail_engine_add(argv):
            if argv[-5:] == ["worktree", "add", "--detach", engine[1], engine[2]]:
                raise HOLD("SYNTHETIC_ENGINE_ADD_FAILURE")
            return original_capture(argv)
        monkeypatch.setattr(backend, "_capture", fail_engine_add)
        with pytest.raises(HOLD, match="SYNTHETIC_ENGINE_ADD_FAILURE"):
            materializer.materialize_v2r13_frozen_worktrees(
                path_record, source_repository_root=source[0], engine_repository_root=engine[0],
                materialization_authorized=True, path_exists=runner.path_exists, run_git=runner.run_git,
            )
        assert not Path(source[1]).exists() and not Path(engine[1]).exists()
    else:
        receipt = materializer.materialize_v2r13_frozen_worktrees(
            path_record, source_repository_root=source[0], engine_repository_root=engine[0],
            materialization_authorized=True, path_exists=runner.path_exists, run_git=runner.run_git,
        )
        assert receipt["materialization_performed"] is True
        assert receipt["canonical_source_checkout_unchanged"] is True
        assert receipt["canonical_engine_checkout_unchanged"] is True
        assert receipt["runtime_execution_authorized"] is False
        if scenario == "dirty_engine":
            (Path(engine[1]) / "retain.txt").write_text("preserved fixture")
            with pytest.raises(materializer.RuntimeV2R13FrozenWorktreeMaterializerHold, match="not clean"):
                materializer.cleanup_v2r13_frozen_worktrees(
                    receipt, cleanup_authorized=True, path_exists=runner.path_exists, run_git=runner.run_git,
                )
            assert Path(source[1]).is_dir() and Path(engine[1]).is_dir()
        else:
            for _ in range(2):  # Existing cleanup remains idempotent after absence.
                materializer.cleanup_v2r13_frozen_worktrees(
                    receipt, cleanup_authorized=True, path_exists=runner.path_exists, run_git=runner.run_git,
                )
            assert not Path(source[1]).exists() and not Path(engine[1]).exists()
    assert (baseline / "comparison.json").read_bytes() == b"preserved-baseline-evidence\n"
