from __future__ import annotations

import ast
import hashlib
import importlib.util
import stat
import sys
from pathlib import Path
from types import SimpleNamespace


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_v2r13_worktree_observer_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_worktree_observer_generation2.py"
)
EXPECTED_SOURCE_SHA256 = (
    "ad2544600833e3f88388e68df5e289a7f69b55f4e8c32f89e8899338e195aacf"
)

SOURCE_ROOT = "/frozen/source"
ENGINE_ROOT = "/engine/exact"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_v2r13_worktree_observer",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _record(m):
    return {
        "schema": "void.abaddon.generation2.runtime-path-input-record.v1",
        "snapshot_id": m.V2R13,
        "source_kind": "explicit_external_input",
        "frozen_source_root": SOURCE_ROOT,
        "exact_engine_root": ENGINE_ROOT,
    }


def _dir_stat(*, ino, mode=None, mtime_ns=100, ctime_ns=200):
    if mode is None:
        mode = stat.S_IFDIR | 0o755
    return SimpleNamespace(
        st_dev=2050,
        st_ino=ino,
        st_mode=mode,
        st_nlink=2,
        st_size=4096,
        st_mtime_ns=mtime_ns,
        st_ctime_ns=ctime_ns,
    )


def _stable_lstat(path):
    if path == SOURCE_ROOT:
        return _dir_stat(ino=1001)
    if path == ENGINE_ROOT:
        return _dir_stat(ino=2001)
    raise FileNotFoundError(path)


def _git_runner(
    m,
    *,
    source_dirty=False,
    engine_dirty=False,
    source_attached=False,
    source_head=None,
    source_tree=None,
    engine_head=None,
):
    expected_source_head = (
        source_head
        or m.runtime_observers.FROZEN_WAR_COLLEGE_COMMIT
    )
    expected_source_tree = (
        source_tree
        or m.runtime_observers.FROZEN_WAR_COLLEGE_TREE
    )
    expected_engine_head = (
        engine_head
        or m.runtime_observers.FROZEN_ENGINE_COMMIT
    )

    def run(repo, *args):
        key = tuple(args)
        if repo == SOURCE_ROOT:
            if key == ("rev-parse", "HEAD"):
                return m.runtime_observers.GitCommandResult(
                    0,
                    expected_source_head + "\n",
                )
            if key == ("rev-parse", "HEAD^{tree}"):
                return m.runtime_observers.GitCommandResult(
                    0,
                    expected_source_tree + "\n",
                )
            if key == (
                "status",
                "--porcelain",
                "--untracked-files=all",
            ):
                return m.runtime_observers.GitCommandResult(
                    0,
                    " M drift\n" if source_dirty else "",
                )
            if key == ("symbolic-ref", "-q", "HEAD"):
                if source_attached:
                    return m.runtime_observers.GitCommandResult(
                        0,
                        "refs/heads/main\n",
                    )
                return m.runtime_observers.GitCommandResult(1, "")
        if repo == ENGINE_ROOT:
            if key == ("rev-parse", "HEAD"):
                return m.runtime_observers.GitCommandResult(
                    0,
                    expected_engine_head + "\n",
                )
            if key == (
                "status",
                "--porcelain",
                "--untracked-files=all",
            ):
                return m.runtime_observers.GitCommandResult(
                    0,
                    " M drift\n" if engine_dirty else "",
                )
        raise AssertionError((repo, args))

    return run


def _observe(m, **kwargs):
    return m.observe_v2r13_worktrees(
        _record(m),
        observation_authorized=True,
        lstat_path=kwargs.pop("lstat_path", _stable_lstat),
        run_git=kwargs.pop("run_git", _git_runner(m)),
        resolve_path=kwargs.pop("resolve_path", lambda path: path),
        **kwargs,
    )


def _expect_hold(exc_type, pattern, fn):
    try:
        fn()
    except exc_type as exc:
        assert pattern in str(exc), (pattern, str(exc))
    else:
        raise AssertionError(f"expected {exc_type.__name__}: {pattern}")


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def test_contract_binds_exact_canonical_blobs():
    m = _load()
    out = m.v2r13_worktree_observer_contract()
    assert out["runtime_observers_git_blob"] == (
        "cc4774e6aa934764c189cebd4040cd8ea4870517"
    )
    assert out["path_inputs_git_blob"] == (
        "f65735c7820da9da0205388f1933b6aa9d6dd737"
    )
    assert out["activation_evidence_git_blob"] == (
        "aac7964d9e80633535003b9f27066cac1bb4bac2"
    )


def test_contract_is_dormant_and_requires_injected_backends():
    m = _load()
    out = m.v2r13_worktree_observer_contract()
    assert out["path_lstat_backend_required"] is True
    assert out["git_runner_required"] is True
    assert out["path_resolver_required"] is True
    assert out["real_host_backend_implemented"] is False
    assert out["automatic_host_backend_selection"] is False
    assert out["observation_requires_explicit_authority"] is True
    assert out["observation_performed"] is False


def test_contract_implements_path_generation_and_composition_only():
    m = _load()
    out = m.v2r13_worktree_observer_contract()
    assert out["path_generation_stability_check_implemented"] is True
    assert out["reviewed_git_observer_composition_implemented"] is True
    assert out["six_path_classification_leaves_implemented"] is True
    assert out["activation_worktree_shape_composition_implemented"] is True
    assert out["canonical_provider_binding_present"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_observation_requires_explicit_authority():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13WorktreeObserverHold,
        "GENERATION2_V2R13_WORKTREE_OBSERVATION_NOT_AUTHORIZED",
        lambda: m.observe_v2r13_worktrees(
            _record(m),
            observation_authorized=False,
            lstat_path=_stable_lstat,
            run_git=_git_runner(m),
            resolve_path=lambda path: path,
        ),
    )


def test_happy_path_produces_exact_activation_worktree_shapes():
    m = _load()
    out = _observe(m)
    requirement = m.activation_evidence.evidence_requirement(m.V2R13)
    assert set(out["frozen_source_worktree"]) == set(
        requirement["frozen_source_worktree_fields"]
    )
    assert set(out["engine_worktree"]) == set(
        requirement["engine_worktree_fields"]
    )


def test_happy_path_source_values_are_exact():
    m = _load()
    out = _observe(m)
    source = out["frozen_source_worktree"]
    assert source == {
        "path": SOURCE_ROOT,
        "exists": True,
        "is_directory": True,
        "is_symlink": False,
        "clean": True,
        "detached": True,
        "head_commit": m.runtime_observers.FROZEN_WAR_COLLEGE_COMMIT,
        "tree_sha": m.runtime_observers.FROZEN_WAR_COLLEGE_TREE,
    }


def test_happy_path_engine_values_are_exact():
    m = _load()
    out = _observe(m)
    engine = out["engine_worktree"]
    assert engine == {
        "path": ENGINE_ROOT,
        "exists": True,
        "is_directory": True,
        "is_symlink": False,
        "clean": True,
        "head_commit": m.runtime_observers.FROZEN_ENGINE_COMMIT,
    }


def test_happy_path_receipt_boundary_is_exact():
    m = _load()
    out = _observe(m)
    assert out["source_path_generation_stable"] is True
    assert out["engine_path_generation_stable"] is True
    assert out["observation_mode"] == "read_only"
    assert out["filesystem_observation_performed"] is True
    assert out["git_query_performed"] is True
    assert out["worktree_created"] is False
    assert out["checkout_mutation_performed"] is False
    assert out["runtime_execution_performed"] is False
    assert out["model_execution_performed"] is False
    assert out["game_execution_performed"] is False


def test_supplied_receipt_validator_accepts_happy_path():
    m = _load()
    out = m.validate_v2r13_worktree_observation(_observe(m))
    assert out["receipt_valid"] is True
    assert out["path_classification_complete"] is True
    assert out["git_identity_complete"] is True
    assert out["activation_worktree_shape_complete"] is True
    assert out["canonical_provider_binding_present"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_source_symlink_is_rejected():
    m = _load()

    def lstat_path(path):
        if path == SOURCE_ROOT:
            return _dir_stat(
                ino=1001,
                mode=stat.S_IFLNK | 0o777,
            )
        return _stable_lstat(path)

    _expect_hold(
        m.RuntimeV2R13WorktreeObserverHold,
        "V2R13_SOURCE_WORKTREE: path is symlink",
        lambda: _observe(m, lstat_path=lstat_path),
    )


def test_engine_symlink_is_rejected():
    m = _load()

    def lstat_path(path):
        if path == ENGINE_ROOT:
            return _dir_stat(
                ino=2001,
                mode=stat.S_IFLNK | 0o777,
            )
        return _stable_lstat(path)

    _expect_hold(
        m.RuntimeV2R13WorktreeObserverHold,
        "V2R13_ENGINE_WORKTREE: path is symlink",
        lambda: _observe(m, lstat_path=lstat_path),
    )


def test_source_non_directory_is_rejected():
    m = _load()

    def lstat_path(path):
        if path == SOURCE_ROOT:
            return _dir_stat(
                ino=1001,
                mode=stat.S_IFREG | 0o644,
            )
        return _stable_lstat(path)

    _expect_hold(
        m.RuntimeV2R13WorktreeObserverHold,
        "V2R13_SOURCE_WORKTREE: path is not directory",
        lambda: _observe(m, lstat_path=lstat_path),
    )


def test_engine_missing_is_rejected():
    m = _load()

    def lstat_path(path):
        if path == ENGINE_ROOT:
            raise FileNotFoundError(path)
        return _stable_lstat(path)

    _expect_hold(
        m.RuntimeV2R13WorktreeObserverHold,
        "V2R13_ENGINE_WORKTREE: path observation failed:FileNotFoundError",
        lambda: _observe(m, lstat_path=lstat_path),
    )


def test_source_generation_change_is_rejected():
    m = _load()
    calls = {SOURCE_ROOT: 0, ENGINE_ROOT: 0}

    def lstat_path(path):
        calls[path] += 1
        if path == SOURCE_ROOT:
            ino = 1001 if calls[path] == 1 else 1002
            return _dir_stat(ino=ino)
        return _dir_stat(ino=2001)

    _expect_hold(
        m.RuntimeV2R13WorktreeObserverHold,
        "V2R13_SOURCE_WORKTREE_GENERATION_CHANGED",
        lambda: _observe(m, lstat_path=lstat_path),
    )


def test_engine_generation_change_is_rejected():
    m = _load()
    calls = {SOURCE_ROOT: 0, ENGINE_ROOT: 0}

    def lstat_path(path):
        calls[path] += 1
        if path == ENGINE_ROOT:
            ino = 2001 if calls[path] == 1 else 2002
            return _dir_stat(ino=ino)
        return _dir_stat(ino=1001)

    _expect_hold(
        m.RuntimeV2R13WorktreeObserverHold,
        "V2R13_ENGINE_WORKTREE_GENERATION_CHANGED",
        lambda: _observe(m, lstat_path=lstat_path),
    )


def test_source_path_resolution_drift_is_rejected_by_reviewed_git_observer():
    m = _load()
    _expect_hold(
        m.runtime_observers.RuntimeObserverHold,
        "V2R13_SOURCE_PATH_IDENTITY",
        lambda: _observe(
            m,
            resolve_path=lambda path: "/other" if path == SOURCE_ROOT else path,
        ),
    )


def test_source_dirty_is_rejected_by_reviewed_git_observer():
    m = _load()
    _expect_hold(
        m.runtime_observers.RuntimeObserverHold,
        "V2R13_SOURCE_WORKTREE_DIRTY",
        lambda: _observe(
            m,
            run_git=_git_runner(m, source_dirty=True),
        ),
    )


def test_source_attached_is_rejected_by_reviewed_git_observer():
    m = _load()
    _expect_hold(
        m.runtime_observers.RuntimeObserverHold,
        "V2R13_SOURCE_NOT_DETACHED",
        lambda: _observe(
            m,
            run_git=_git_runner(m, source_attached=True),
        ),
    )


def test_engine_dirty_is_rejected_by_reviewed_git_observer():
    m = _load()
    _expect_hold(
        m.runtime_observers.RuntimeObserverHold,
        "V2R13_ENGINE_WORKTREE_DIRTY",
        lambda: _observe(
            m,
            run_git=_git_runner(m, engine_dirty=True),
        ),
    )


def test_source_commit_drift_is_rejected_by_reviewed_git_observer():
    m = _load()
    _expect_hold(
        m.runtime_observers.RuntimeObserverHold,
        "V2R13_SOURCE_HEAD_DRIFT",
        lambda: _observe(
            m,
            run_git=_git_runner(m, source_head="0" * 40),
        ),
    )


def test_malformed_lstat_field_is_rejected():
    m = _load()

    def lstat_path(path):
        value = _stable_lstat(path)
        value.st_ino = "not-int"
        return value

    _expect_hold(
        m.RuntimeV2R13WorktreeObserverHold,
        "malformed lstat field st_ino",
        lambda: _observe(m, lstat_path=lstat_path),
    )


def test_static_source_has_no_real_host_backend_or_auto_selection():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    forbidden_import_roots = {
        "os",
        "subprocess",
        "pathlib",
        "socket",
        "requests",
        "urllib",
        "http",
        "httpx",
    }
    forbidden_calls = {
        "runtime_observers.host_git_runner",
        "runtime_observers.host_path_resolver",
        "os.lstat",
        "Path.resolve",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call):
            assert _dotted(node.func) not in forbidden_calls


def test_host_entrypoint_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13WorktreeObserverHold,
        "GENERATION2_V2R13_HOST_PATH_BACKEND_NOT_IMPLEMENTED",
        lambda: m.observe_with_host_backend(),
    )
