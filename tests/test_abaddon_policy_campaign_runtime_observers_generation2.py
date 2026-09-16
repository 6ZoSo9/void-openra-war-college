from __future__ import annotations

import ast
import hashlib
import importlib.util
import os
import stat
import sys
from pathlib import Path
from types import SimpleNamespace


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name("abaddon_policy_campaign_runtime_observers_generation2.py")
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/abaddon_policy_campaign_runtime_observers_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "cc02c4894a9fcb81152ca9f9f86c65a60443de4273e0d73282ea0f996469ab52"


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def _expect_hold(exc_type, pattern, fn):
    try:
        fn()
    except exc_type as exc:
        assert pattern in str(exc), (pattern, str(exc))
    else:
        raise AssertionError(f"expected {exc_type.__name__}: {pattern}")


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_runtime_observers",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _stat(size, *, ino=7, mtime=11, ctime=13, mode=None, nlink=1):
    if mode is None:
        mode = stat.S_IFREG | 0o400
    return SimpleNamespace(
        st_dev=2050,
        st_ino=ino,
        st_size=size,
        st_mtime_ns=mtime,
        st_ctime_ns=ctime,
        st_mode=mode,
        st_nlink=nlink,
    )


def _backend_for(m, payload, *, after=None, open_error=None):
    state = {"offset": 0, "flags": None, "closed": False, "fstat_calls": 0}
    before = _stat(len(payload))
    after = before if after is None else after

    def open_file(path, flags):
        if open_error is not None:
            raise open_error
        state["flags"] = flags
        assert path.startswith("/")
        return 9

    def fstat_fn(fd):
        assert fd == 9
        state["fstat_calls"] += 1
        return before if state["fstat_calls"] == 1 else after

    def read_fn(fd, maximum):
        assert fd == 9
        start = state["offset"]
        if start >= len(payload):
            return b""
        chunk = payload[start : start + maximum]
        state["offset"] += len(chunk)
        return chunk

    def close_fn(fd):
        assert fd == 9
        state["closed"] = True

    return m.FileObservationBackend(open_file, fstat_fn, read_fn, close_fn), state


def _v8_record(m):
    return {
        "schema": "void.abaddon.generation2.runtime-path-input-record.v1",
        "snapshot_id": m.V8,
        "source_kind": "explicit_external_input",
        "model_dir": "/srv/void/g2/v8/model",
        "adapter_dir": "/srv/void/g2/v8/adapter",
    }


def _v2_record(m):
    return {
        "schema": "void.abaddon.generation2.runtime-path-input-record.v1",
        "snapshot_id": m.V2R13,
        "source_kind": "explicit_external_input",
        "frozen_source_root": "/srv/void/g2/v2r13/source",
        "exact_engine_root": "/srv/void/g2/v2r13/engine",
    }


def _good_git_runner(m):
    source = "/srv/void/g2/v2r13/source"
    engine = "/srv/void/g2/v2r13/engine"
    calls = []

    def run_git(repo, *args):
        calls.append((repo, args))
        table = {
            (source, ("rev-parse", "HEAD")):
                m.GitCommandResult(0, m.FROZEN_WAR_COLLEGE_COMMIT + "\n"),
            (source, ("rev-parse", "HEAD^{tree}")):
                m.GitCommandResult(0, m.FROZEN_WAR_COLLEGE_TREE + "\n"),
            (source, ("status", "--porcelain", "--untracked-files=all")):
                m.GitCommandResult(0, ""),
            (source, ("symbolic-ref", "-q", "HEAD")):
                m.GitCommandResult(1, ""),
            (engine, ("rev-parse", "HEAD")):
                m.GitCommandResult(0, m.FROZEN_ENGINE_COMMIT + "\n"),
            (engine, ("status", "--porcelain", "--untracked-files=all")):
                m.GitCommandResult(0, ""),
        }
        return table[(repo, args)]

    return run_git, calls


def test_contract_implements_both_dormant_observers():
    m = _load()
    out = m.runtime_observer_contract()
    assert out["strong_file_observer_implemented"] is True
    assert out["v8_asset_observer_implemented"] is True
    assert out["v2r13_git_observer_implemented"] is True
    assert out["v8_asset_count"] == 17
    assert out["automatic_host_backend_selection"] is False
    assert out["observation_requires_explicit_authority"] is True
    assert out["observation_performed"] is False
    assert out["runtime_execution_authorized"] is False


def test_v8_manifest_has_exact_seventeen_unique_paths_and_hashes():
    m = _load()
    specs = m.V8_ASSET_SPECS
    assert len(specs) == 17
    keys = [(s.root_field, s.relative_path) for s in specs]
    assert len(keys) == len(set(keys))
    for spec in specs:
        assert spec.root_field in {"model_dir", "adapter_dir"}
        assert len(spec.expected_sha256) == 64
        int(spec.expected_sha256, 16)
        assert spec.maximum_bytes > 0
    assert specs[0].relative_path == "config.json"
    assert specs[13].relative_path == "adapter_model.safetensors"


def test_strong_file_observer_requires_explicit_authority():
    m = _load()
    backend, _ = _backend_for(m, b"abc")
    _expect_hold(
        m.RuntimeObserverHold,
        "GENERATION2_READ_ONLY_OBSERVATION_NOT_AUTHORIZED",
        lambda: m.observe_exact_regular_file(
            "/tmp/a",
            expected_sha256=hashlib.sha256(b"abc").hexdigest(),
            maximum_bytes=10,
            observation_authorized=False,
            backend=backend,
        ),
    )


def test_strong_file_observer_uses_nofollow_and_same_descriptor_stability():
    m = _load()
    payload = b"abc123"
    backend, state = _backend_for(m, payload)
    out = m.observe_exact_regular_file(
        "/tmp/a",
        expected_sha256=hashlib.sha256(payload).hexdigest(),
        maximum_bytes=1024,
        observation_authorized=True,
        backend=backend,
    )
    assert state["flags"] & getattr(os, "O_NOFOLLOW", 0) == getattr(os, "O_NOFOLLOW", 0)
    assert state["fstat_calls"] == 2
    assert state["closed"] is True
    assert out["generation_stable"] is True
    assert out["byte_count"] == len(payload)
    assert out["actual_sha256"] == hashlib.sha256(payload).hexdigest()
    assert out["runtime_execution_performed"] is False
    assert out["model_execution_performed"] is False


def test_strong_file_observer_rejects_generation_change():
    m = _load()
    payload = b"abc123"
    after = _stat(len(payload), mtime=99, ctime=101)
    backend, state = _backend_for(m, payload, after=after)
    _expect_hold(
        m.RuntimeObserverHold,
        "STRONG_FILE_GENERATION_CHANGED",
        lambda: m.observe_exact_regular_file(
            "/tmp/a",
            expected_sha256=hashlib.sha256(payload).hexdigest(),
            maximum_bytes=1024,
            observation_authorized=True,
            backend=backend,
        ),
    )
    assert state["closed"] is True


def test_strong_file_observer_rejects_nonregular_and_oversize():
    m = _load()
    payload = b"abc"
    backend, _ = _backend_for(
        m,
        payload,
        after=_stat(len(payload), mode=stat.S_IFDIR | 0o500),
    )
    # Nonregular is checked on the first fstat, so build a dedicated backend.
    before = _stat(len(payload), mode=stat.S_IFDIR | 0o500)
    state = {"n": 0}
    bad_backend = m.FileObservationBackend(
        lambda path, flags: 9,
        lambda fd: before,
        lambda fd, n: b"",
        lambda fd: state.__setitem__("n", state["n"] + 1),
    )
    _expect_hold(
        m.RuntimeObserverHold,
        "STRONG_FILE_NOT_REGULAR",
        lambda: m.observe_exact_regular_file(
            "/tmp/a",
            expected_sha256=hashlib.sha256(payload).hexdigest(),
            maximum_bytes=1024,
            observation_authorized=True,
            backend=bad_backend,
        ),
    )
    assert state["n"] == 1

    large_before = _stat(2048)
    large_backend = m.FileObservationBackend(
        lambda path, flags: 9,
        lambda fd: large_before,
        lambda fd, n: b"",
        lambda fd: None,
    )
    _expect_hold(
        m.RuntimeObserverHold,
        "STRONG_FILE_EXCEEDS_BOUND",
        lambda: m.observe_exact_regular_file(
            "/tmp/a",
            expected_sha256=hashlib.sha256(payload).hexdigest(),
            maximum_bytes=1024,
            observation_authorized=True,
            backend=large_backend,
        ),
    )


def test_strong_file_observer_rejects_sha_drift():
    m = _load()
    payload = b"abc123"
    backend, _ = _backend_for(m, payload)
    _expect_hold(
        m.RuntimeObserverHold,
        "STRONG_FILE_SHA256_DRIFT",
        lambda: m.observe_exact_regular_file(
            "/tmp/a",
            expected_sha256="0" * 64,
            maximum_bytes=1024,
            observation_authorized=True,
            backend=backend,
        ),
    )


def test_public_v8_observer_does_not_auto_select_host_backend():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    fn = next(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "observe_v8_assets"
    )
    body = ast.get_source_segment(source, fn)
    assert "host_file_observation_backend(" not in body
    assert "backend: FileObservationBackend" in body
    assert "observe_exact_regular_file(" in body


def test_v2r13_git_observer_requires_explicit_authority():
    m = _load()
    run_git, _ = _good_git_runner(m)
    _expect_hold(
        m.RuntimeObserverHold,
        "GENERATION2_READ_ONLY_OBSERVATION_NOT_AUTHORIZED",
        lambda: m.observe_v2r13_git_identity(
            _v2_record(m),
            observation_authorized=False,
            run_git=run_git,
            resolve_path=lambda value: value,
        ),
    )


def test_v2r13_git_observer_accepts_exact_fake_identity_only():
    m = _load()
    run_git, calls = _good_git_runner(m)
    out = m.observe_v2r13_git_identity(
        _v2_record(m),
        observation_authorized=True,
        run_git=run_git,
        resolve_path=lambda value: value,
    )
    assert out["source_head_commit"] == m.FROZEN_WAR_COLLEGE_COMMIT
    assert out["source_head_tree"] == m.FROZEN_WAR_COLLEGE_TREE
    assert out["source_worktree_clean"] is True
    assert out["source_detached_head"] is True
    assert out["engine_head_commit"] == m.FROZEN_ENGINE_COMMIT
    assert out["engine_worktree_clean"] is True
    assert out["worktree_created"] is False
    assert out["checkout_mutation_performed"] is False
    assert len(calls) == 6


def test_v2r13_git_observer_rejects_source_tree_drift():
    m = _load()
    good, _ = _good_git_runner(m)
    def run_git(repo, *args):
        if args == ("rev-parse", "HEAD^{tree}"):
            return m.GitCommandResult(0, "0" * 40 + "\n")
        return good(repo, *args)
    _expect_hold(
        m.RuntimeObserverHold,
        "V2R13_SOURCE_TREE_DRIFT",
        lambda: m.observe_v2r13_git_identity(
            _v2_record(m),
            observation_authorized=True,
            run_git=run_git,
            resolve_path=lambda value: value,
        ),
    )


def test_v2r13_git_observer_rejects_dirty_source():
    m = _load()
    good, _ = _good_git_runner(m)
    def run_git(repo, *args):
        if repo.endswith("/source") and args == ("status", "--porcelain", "--untracked-files=all"):
            return m.GitCommandResult(0, "?? stray\n")
        return good(repo, *args)
    _expect_hold(
        m.RuntimeObserverHold,
        "V2R13_SOURCE_WORKTREE_DIRTY",
        lambda: m.observe_v2r13_git_identity(
            _v2_record(m),
            observation_authorized=True,
            run_git=run_git,
            resolve_path=lambda value: value,
        ),
    )


def test_v2r13_git_observer_rejects_attached_source():
    m = _load()
    good, _ = _good_git_runner(m)
    def run_git(repo, *args):
        if repo.endswith("/source") and args == ("symbolic-ref", "-q", "HEAD"):
            return m.GitCommandResult(0, "refs/heads/main\n")
        return good(repo, *args)
    _expect_hold(
        m.RuntimeObserverHold,
        "V2R13_SOURCE_NOT_DETACHED",
        lambda: m.observe_v2r13_git_identity(
            _v2_record(m),
            observation_authorized=True,
            run_git=run_git,
            resolve_path=lambda value: value,
        ),
    )


def test_v2r13_git_observer_rejects_engine_commit_drift():
    m = _load()
    good, _ = _good_git_runner(m)
    def run_git(repo, *args):
        if repo.endswith("/engine") and args == ("rev-parse", "HEAD"):
            return m.GitCommandResult(0, "0" * 40 + "\n")
        return good(repo, *args)
    _expect_hold(
        m.RuntimeObserverHold,
        "V2R13_ENGINE_HEAD_DRIFT",
        lambda: m.observe_v2r13_git_identity(
            _v2_record(m),
            observation_authorized=True,
            run_git=run_git,
            resolve_path=lambda value: value,
        ),
    )


def test_v2r13_git_observer_rejects_path_alias_or_symlink_resolution():
    m = _load()
    run_git, calls = _good_git_runner(m)
    _expect_hold(
        m.RuntimeObserverHold,
        "V2R13_SOURCE_PATH_IDENTITY",
        lambda: m.observe_v2r13_git_identity(
            _v2_record(m),
            observation_authorized=True,
            run_git=run_git,
            resolve_path=lambda value: "/different" if value.endswith("/source") else value,
        ),
    )
    assert calls == []


def test_public_v2r13_observer_does_not_auto_select_host_runner_or_resolver():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    fn = next(
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "observe_v2r13_git_identity"
    )
    body = ast.get_source_segment(source, fn)
    assert "host_git_runner(" not in body
    assert "host_path_resolver(" not in body
    assert "run_git: GitRunner" in body
    assert "resolve_path: PathResolver" in body


def test_host_backends_are_defined_but_never_called_at_import():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    top_level_calls = []
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            top_level_calls.append(ast.unparse(node.value.func))
    assert "host_file_observation_backend" not in top_level_calls
    assert "host_git_runner" not in top_level_calls
    assert "host_path_resolver" not in top_level_calls


def test_tests_never_call_real_host_backends():
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(Path(__file__)))
    forbidden = {
        "m.host_file_observation_backend",
        "m.host_git_runner",
        "m.host_path_resolver",
    }
    actual = sorted(
        {
            _dotted(node.func)
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and _dotted(node.func) in forbidden
        }
    )
    assert actual == []


def test_observers_preserve_runtime_authority_false():
    m = _load()
    contract = m.runtime_observer_contract()
    assert contract["authority"]["runtime_execution_authorized"] is False
    assert contract["authority"]["model_execution_authorized"] is False
    assert contract["authority"]["game_execution_authorized"] is False
    assert contract["authority"]["worktree_creation_authorized"] is False
    assert contract["authority"]["checkout_mutation_authorized"] is False
    assert contract["authority"]["model_weights_load_authorized"] is False
