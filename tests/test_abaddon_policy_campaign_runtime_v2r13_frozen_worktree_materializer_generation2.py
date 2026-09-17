from __future__ import annotations

import ast
import hashlib
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_v2r13_frozen_worktree_materializer_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_frozen_worktree_materializer_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "64e6c5939564d5a861fd18d91716396749d6bd95bdaa779d5d1687c251234417"

SOURCE_REPO = "/repos/war-college"
ENGINE_REPO = "/repos/openra"
SOURCE_DEST = "/materialized/v2r13/source"
ENGINE_DEST = "/materialized/v2r13/engine"

CANONICAL_SOURCE_HEAD = "95f05fa9c1680da91cf3d92de80976f4af83e702"
CANONICAL_SOURCE_TREE = "64a7492d313b2b22beb404097221aff53ebb4c12"
CANONICAL_ENGINE_HEAD = "1111111111111111111111111111111111111111"
CANONICAL_ENGINE_TREE = "2222222222222222222222222222222222222222"
FROZEN_ENGINE_TREE = "3333333333333333333333333333333333333333"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_v2r13_frozen_worktree_materializer",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _expect_hold(exc_type, pattern, fn):
    try:
        fn()
    except exc_type as exc:
        assert pattern in str(exc), (pattern, str(exc))
    else:
        raise AssertionError(f"expected {exc_type.__name__}: {pattern}")


def _record(m):
    return {
        "schema": m.path_inputs.RECORD_SCHEMA,
        "snapshot_id": m.path_inputs.V2R13,
        "source_kind": m.path_inputs.SOURCE_KIND,
        "frozen_source_root": SOURCE_DEST,
        "exact_engine_root": ENGINE_DEST,
    }


class FakeGit:
    def __init__(self, m):
        self.m = m
        self.paths = {SOURCE_REPO, ENGINE_REPO}
        self.worktrees = {}
        self.events = []
        self.fail_engine_add = False
        self.source_attached_after_add = False
        self.source_tree_drift = False
        self.mutate_canonical_source_after_add = False

        self.canonical = {
            SOURCE_REPO: {
                "head": CANONICAL_SOURCE_HEAD,
                "tree": CANONICAL_SOURCE_TREE,
                "status": "",
            },
            ENGINE_REPO: {
                "head": CANONICAL_ENGINE_HEAD,
                "tree": CANONICAL_ENGINE_TREE,
                "status": "",
            },
        }
        self.known = {
            SOURCE_REPO: {
                m.portable_checkout.FROZEN_WAR_COLLEGE_COMMIT:
                    m.portable_checkout.FROZEN_WAR_COLLEGE_TREE,
                CANONICAL_SOURCE_HEAD: CANONICAL_SOURCE_TREE,
            },
            ENGINE_REPO: {
                m.portable_checkout.FROZEN_ENGINE_COMMIT: FROZEN_ENGINE_TREE,
                CANONICAL_ENGINE_HEAD: CANONICAL_ENGINE_TREE,
            },
        }

    def exists(self, path):
        return path in self.paths

    def result(self, rc=0, stdout="", stderr=""):
        return SimpleNamespace(returncode=rc, stdout=stdout, stderr=stderr)

    def _state(self, repo):
        if repo in self.canonical:
            state = dict(self.canonical[repo])
            if (
                repo == SOURCE_REPO
                and self.mutate_canonical_source_after_add
                and SOURCE_DEST in self.worktrees
            ):
                state["head"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            return state
        if repo in self.worktrees:
            return self.worktrees[repo]
        raise AssertionError(("unknown repo", repo))

    def __call__(self, repo, *args):
        key = tuple(args)
        self.events.append((repo, key))

        if key == ("rev-parse", "--show-toplevel"):
            return self.result(stdout=repo + "\n")

        if key == ("rev-parse", "HEAD"):
            return self.result(stdout=self._state(repo)["head"] + "\n")

        if key == ("rev-parse", "HEAD^{tree}"):
            return self.result(stdout=self._state(repo)["tree"] + "\n")

        if len(key) == 3 and key[:2] == ("rev-parse", "--verify"):
            spec = key[2]
            assert spec.endswith("^{commit}")
            commit = spec[:-len("^{commit}")]
            if commit in self.known.get(repo, {}):
                return self.result(stdout=commit + "\n")
            return self.result(rc=1, stderr="unknown commit")

        if len(key) == 2 and key[0] == "rev-parse" and key[1].endswith("^{tree}"):
            commit = key[1][:-len("^{tree}")]
            tree = self.known.get(repo, {}).get(commit)
            if tree is None:
                return self.result(rc=1, stderr="unknown tree")
            if (
                repo == SOURCE_REPO
                and commit == self.m.portable_checkout.FROZEN_WAR_COLLEGE_COMMIT
                and self.source_tree_drift
            ):
                tree = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
            return self.result(stdout=tree + "\n")

        if key == ("status", "--porcelain", "--untracked-files=all"):
            return self.result(stdout=self._state(repo).get("status", ""))

        if key == ("symbolic-ref", "-q", "HEAD"):
            state = self._state(repo)
            if state.get("detached", False):
                return self.result(rc=1)
            return self.result(stdout="refs/heads/main\n")

        if key == ("worktree", "list", "--porcelain"):
            rows = [f"worktree {repo}", ""]
            for path, state in self.worktrees.items():
                if state["owner"] == repo:
                    rows.extend([f"worktree {path}", "detached", ""])
            return self.result(stdout="\n".join(rows))

        if len(key) == 5 and key[:3] == ("worktree", "add", "--detach"):
            destination = key[3]
            commit = key[4]
            if repo == ENGINE_REPO and self.fail_engine_add:
                return self.result(rc=1, stderr="synthetic engine add failure")
            tree = self.known[repo][commit]
            detached = True
            if repo == SOURCE_REPO and self.source_attached_after_add:
                detached = False
            self.paths.add(destination)
            self.worktrees[destination] = {
                "owner": repo,
                "head": commit,
                "tree": tree,
                "status": "",
                "detached": detached,
            }
            return self.result(stdout=f"Preparing worktree {destination}\n")

        if len(key) == 4 and key[:3] == ("worktree", "remove", "--force"):
            destination = key[3]
            state = self.worktrees.get(destination)
            if state is None or state["owner"] != repo:
                return self.result(rc=1, stderr="unknown worktree")
            del self.worktrees[destination]
            self.paths.discard(destination)
            return self.result()

        raise AssertionError((repo, args))


def _materialize(m, fake, **overrides):
    kwargs = {
        "source_repository_root": SOURCE_REPO,
        "engine_repository_root": ENGINE_REPO,
        "materialization_authorized": True,
        "path_exists": fake.exists,
        "run_git": fake,
    }
    kwargs.update(overrides)
    return m.materialize_v2r13_frozen_worktrees(
        _record(m),
        **kwargs,
    )


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def test_source_sha_is_exact():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SOURCE_SHA256


def test_static_source_bundles_no_real_host_backend():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    forbidden_roots = {
        "os",
        "subprocess",
        "socket",
        "requests",
        "urllib",
        "http",
        "httpx",
        "asyncio",
        "multiprocessing",
        "ctypes",
    }
    forbidden_calls = {
        "subprocess.run",
        "subprocess.Popen",
        "subprocess.call",
        "subprocess.check_call",
        "subprocess.check_output",
        "os.system",
        "os.popen",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_roots
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".", 1)[0]
            assert root not in forbidden_roots
        elif isinstance(node, ast.Call):
            assert _dotted(node.func) not in forbidden_calls


def test_contract_pins_exact_dependencies_and_next_review_gate():
    m = _load()
    out = m.v2r13_frozen_worktree_materializer_contract()
    assert out["activation_review_git_blob"] == (
        "9449b871cb745b67a7aa29f0d73de378f119a488"
    )
    assert out["portable_checkout_git_blob"] == (
        "077fbf5a2847d85113eb8fcba3904b02343ebfef"
    )
    assert out["path_inputs_git_blob"] == (
        "f65735c7820da9da0205388f1933b6aa9d6dd737"
    )
    assert out["worktree_observer_git_blob"] == (
        "994f3be5d3344d6ac905c1f5fee9f9490fd4dd3f"
    )
    assert out["next_gate"] == (
        "V2R13_FROZEN_WORKTREE_MATERIALIZER_SOURCE_BINDING_REVIEW_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_frozen_worktree_materializer_source_binding_review"
    )


def test_contract_implements_materializer_without_reviewing_itself():
    m = _load()
    out = m.v2r13_frozen_worktree_materializer_contract()
    assert out["frozen_worktree_materializer_implemented"] is True
    assert out["frozen_worktree_materializer_reviewed"] is False
    assert out["source_worktree_add_detached_implemented"] is True
    assert out["engine_worktree_add_detached_implemented"] is True
    assert out["partial_failure_rollback_implemented"] is True
    assert out["cleanup_implemented"] is True
    assert out["cleanup_idempotent"] is True


def test_contract_preserves_runtime_and_activation_boundary():
    m = _load()
    out = m.v2r13_frozen_worktree_materializer_contract()
    assert out["materialization_performed"] is False
    assert out["cleanup_performed"] is False
    assert out["activation_proven"] is False
    assert out["runtime_activation_performed"] is False
    assert out["runtime_execution_authorized"] is False
    assert out["model_load_performed"] is False
    assert out["model_inference_performed"] is False
    assert out["game_execution_performed"] is False
    assert out["training_performed"] is False
    assert out["deployment_performed"] is False
    assert out["void_chain_mutation_performed"] is False
    assert out["wallet_or_funds_action_performed"] is False


def test_materialization_requires_explicit_authority():
    m = _load()
    fake = FakeGit(m)
    _expect_hold(
        m.RuntimeV2R13FrozenWorktreeMaterializerHold,
        "MATERIALIZATION_NOT_AUTHORIZED",
        lambda: m.materialize_v2r13_frozen_worktrees(
            _record(m),
            source_repository_root=SOURCE_REPO,
            engine_repository_root=ENGINE_REPO,
            materialization_authorized=False,
            path_exists=fake.exists,
            run_git=fake,
        ),
    )
    assert SOURCE_DEST not in fake.paths
    assert ENGINE_DEST not in fake.paths


def test_materialization_requires_injected_backends():
    m = _load()
    fake = FakeGit(m)
    _expect_hold(
        m.RuntimeV2R13FrozenWorktreeMaterializerHold,
        "path-existence backend required",
        lambda: m.materialize_v2r13_frozen_worktrees(
            _record(m),
            source_repository_root=SOURCE_REPO,
            engine_repository_root=ENGINE_REPO,
            materialization_authorized=True,
            path_exists=None,
            run_git=fake,
        ),
    )


def test_materialization_rejects_existing_destination_before_git_mutation():
    m = _load()
    fake = FakeGit(m)
    fake.paths.add(SOURCE_DEST)
    _expect_hold(
        m.RuntimeV2R13FrozenWorktreeMaterializerHold,
        "frozen source destination already exists",
        lambda: _materialize(m, fake),
    )
    assert not any(event[1][:2] == ("worktree", "add") for event in fake.events)


def test_materialization_rejects_repository_destination_overlap():
    m = _load()
    fake = FakeGit(m)
    record = _record(m)
    record["frozen_source_root"] = SOURCE_REPO
    _expect_hold(
        m.RuntimeV2R13FrozenWorktreeMaterializerHold,
        "must be distinct",
        lambda: m.materialize_v2r13_frozen_worktrees(
            record,
            source_repository_root=SOURCE_REPO,
            engine_repository_root=ENGINE_REPO,
            materialization_authorized=True,
            path_exists=fake.exists,
            run_git=fake,
        ),
    )


def test_happy_path_materializes_exact_two_detached_clean_worktrees():
    m = _load()
    fake = FakeGit(m)
    out = _materialize(m, fake)
    assert SOURCE_DEST in fake.paths
    assert ENGINE_DEST in fake.paths
    assert out["source_worktree_created"] is True
    assert out["engine_worktree_created"] is True
    assert out["source_worktree_detached"] is True
    assert out["engine_worktree_detached"] is True
    assert out["source_worktree_clean"] is True
    assert out["engine_worktree_clean"] is True
    assert out["frozen_source_commit"] == m.portable_checkout.FROZEN_WAR_COLLEGE_COMMIT
    assert out["frozen_source_tree"] == m.portable_checkout.FROZEN_WAR_COLLEGE_TREE
    assert out["frozen_engine_commit"] == m.portable_checkout.FROZEN_ENGINE_COMMIT


def test_happy_path_receipt_truthfully_reports_only_materialization_mutation():
    m = _load()
    fake = FakeGit(m)
    out = _materialize(m, fake)
    assert out["materialization_performed"] is True
    assert out["filesystem_mutation_performed"] is True
    assert out["git_worktree_admin_mutation_performed"] is True
    assert out["canonical_checkout_working_tree_mutation_performed"] is False
    assert out["canonical_source_checkout_unchanged"] is True
    assert out["canonical_engine_checkout_unchanged"] is True
    assert out["runtime_activation_performed"] is False
    assert out["runtime_execution_authorized"] is False
    assert out["model_load_performed"] is False
    assert out["model_inference_performed"] is False
    assert out["game_execution_performed"] is False
    assert out["training_performed"] is False
    assert out["weights_updated"] is False
    assert out["deployment_performed"] is False
    assert out["void_chain_mutation_performed"] is False
    assert out["wallet_or_funds_action_performed"] is False


def test_exact_worktree_add_commands_are_bound_to_frozen_commits():
    m = _load()
    fake = FakeGit(m)
    _materialize(m, fake)
    adds = [
        event
        for event in fake.events
        if event[1][:3] == ("worktree", "add", "--detach")
    ]
    assert adds == [
        (
            SOURCE_REPO,
            (
                "worktree",
                "add",
                "--detach",
                SOURCE_DEST,
                m.portable_checkout.FROZEN_WAR_COLLEGE_COMMIT,
            ),
        ),
        (
            ENGINE_REPO,
            (
                "worktree",
                "add",
                "--detach",
                ENGINE_DEST,
                m.portable_checkout.FROZEN_ENGINE_COMMIT,
            ),
        ),
    ]


def test_frozen_source_tree_drift_holds_before_any_creation():
    m = _load()
    fake = FakeGit(m)
    fake.source_tree_drift = True
    _expect_hold(
        m.RuntimeV2R13FrozenWorktreeMaterializerHold,
        "frozen source tree identity drift",
        lambda: _materialize(m, fake),
    )
    assert SOURCE_DEST not in fake.paths
    assert ENGINE_DEST not in fake.paths


def test_engine_add_failure_rolls_back_source_worktree():
    m = _load()
    fake = FakeGit(m)
    fake.fail_engine_add = True
    _expect_hold(
        m.RuntimeV2R13FrozenWorktreeMaterializerHold,
        "exact engine worktree add",
        lambda: _materialize(m, fake),
    )
    assert SOURCE_DEST not in fake.paths
    assert ENGINE_DEST not in fake.paths
    assert (
        SOURCE_REPO,
        ("worktree", "remove", "--force", SOURCE_DEST),
    ) in fake.events


def test_post_creation_detached_check_failure_rolls_back_source():
    m = _load()
    fake = FakeGit(m)
    fake.source_attached_after_add = True
    _expect_hold(
        m.RuntimeV2R13FrozenWorktreeMaterializerHold,
        "unexpectedly attached",
        lambda: _materialize(m, fake),
    )
    assert SOURCE_DEST not in fake.paths
    assert ENGINE_DEST not in fake.paths


def test_canonical_checkout_change_is_detected_and_both_worktrees_rollback():
    m = _load()
    fake = FakeGit(m)
    fake.mutate_canonical_source_after_add = True
    _expect_hold(
        m.RuntimeV2R13FrozenWorktreeMaterializerHold,
        "canonical source checkout changed",
        lambda: _materialize(m, fake),
    )
    assert SOURCE_DEST not in fake.paths
    assert ENGINE_DEST not in fake.paths


def test_cleanup_requires_separate_explicit_authority():
    m = _load()
    fake = FakeGit(m)
    receipt = _materialize(m, fake)
    _expect_hold(
        m.RuntimeV2R13FrozenWorktreeMaterializerHold,
        "CLEANUP_NOT_AUTHORIZED",
        lambda: m.cleanup_v2r13_frozen_worktrees(
            receipt,
            cleanup_authorized=False,
            path_exists=fake.exists,
            run_git=fake,
        ),
    )
    assert SOURCE_DEST in fake.paths
    assert ENGINE_DEST in fake.paths


def test_cleanup_removes_both_worktrees_and_is_idempotent():
    m = _load()
    fake = FakeGit(m)
    receipt = _materialize(m, fake)
    first = m.cleanup_v2r13_frozen_worktrees(
        receipt,
        cleanup_authorized=True,
        path_exists=fake.exists,
        run_git=fake,
    )
    assert first["source_worktree_removed"] is True
    assert first["engine_worktree_removed"] is True
    assert first["removed_worktree_count"] == 2
    assert first["cleanup_performed"] is True
    assert SOURCE_DEST not in fake.paths
    assert ENGINE_DEST not in fake.paths

    second = m.cleanup_v2r13_frozen_worktrees(
        receipt,
        cleanup_authorized=True,
        path_exists=fake.exists,
        run_git=fake,
    )
    assert second["source_worktree_removed"] is False
    assert second["engine_worktree_removed"] is False
    assert second["removed_worktree_count"] == 0
    assert second["cleanup_performed"] is False
    assert second["cleanup_idempotent"] is True


def test_cleanup_preserves_runtime_training_chain_and_funds_boundaries():
    m = _load()
    fake = FakeGit(m)
    receipt = _materialize(m, fake)
    out = m.cleanup_v2r13_frozen_worktrees(
        receipt,
        cleanup_authorized=True,
        path_exists=fake.exists,
        run_git=fake,
    )
    assert out["runtime_activation_performed"] is False
    assert out["runtime_execution_authorized"] is False
    assert out["model_inference_performed"] is False
    assert out["game_execution_performed"] is False
    assert out["training_performed"] is False
    assert out["weights_updated"] is False
    assert out["deployment_performed"] is False
    assert out["void_chain_mutation_performed"] is False
    assert out["wallet_or_funds_action_performed"] is False


def test_tampered_receipt_is_rejected_before_cleanup():
    m = _load()
    fake = FakeGit(m)
    receipt = _materialize(m, fake)
    bad = dict(receipt)
    bad["runtime_execution_authorized"] = True
    _expect_hold(
        m.RuntimeV2R13FrozenWorktreeMaterializerHold,
        "crossed boundary",
        lambda: m.cleanup_v2r13_frozen_worktrees(
            bad,
            cleanup_authorized=True,
            path_exists=fake.exists,
            run_git=fake,
        ),
    )
    assert SOURCE_DEST in fake.paths
    assert ENGINE_DEST in fake.paths


def test_runtime_authorization_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13FrozenWorktreeMaterializerHold,
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
        lambda: m.authorize_runtime_execution(),
    )
