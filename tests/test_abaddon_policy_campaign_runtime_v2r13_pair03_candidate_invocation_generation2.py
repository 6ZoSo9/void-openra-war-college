"""Candidate wiring with real temporary evidence/claims; no real host runtime."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_invocation_generation2 as invocation,
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_host_preflight_generation2 as preflight,
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_attempt_guard_generation2 as attempt,
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_git_backend_generation2 as git,
)

HEAD = "a" * 40
TREE = "b" * 40
SELF_SHA = "c" * 64
HOLD = invocation.CandidateInvocationHold
REPO = Path(__file__).resolve().parents[1]


def invoke(**overrides):
    return invocation.execute_pair03_candidate(**{
        "expected_main_head": HEAD, "expected_invocation_source_sha256": SELF_SHA,
        "confirm": invocation.CONFIRM_TOKEN, **overrides,
    })


def valid_receipt(root):
    out = {
        "schema": "void.abaddon.generation2.v2r13-bounded-runtime-execution-receipt.v1",
        "pair_slot": 3, "arm": "candidate", "held_out": False,
        "candidate_binding": invocation._expected_candidate_binding(),
        "run_artifact": {"run_id": "inert-candidate-fixture", "run_dir": str(root / "runs/inert-candidate-fixture"),
                         "warm_start_sha256": "d" * 64, "trajectory_sha256": "e" * 64,
                         "summary_sha256": "f" * 64, "summary": {"fixture_only": True}},
    }
    out.update({field: True for field in (
        "runtime_execution_authorized", "runtime_execution_performed", "runtime_started",
        "runtime_cleanup_attempted", "runtime_cleanup_completed", "fresh_runtime_readiness_admitted",
        "revocation_checked_before_materialization", "revocation_checked_before_inference",
    )})
    out.update({field: False for field in (
        "automatic_retry", "training_performed", "weights_updated", "automatic_policy_promotion",
        "deployment_performed", "void_chain_mutation_performed", "wallet_or_funds_action_performed",
    )})
    return {**out, "execution_receipt_sha256": invocation._digest(out)}


@pytest.fixture
def env(tmp_path, monkeypatch):
    root = tmp_path / "execution"
    baseline = root / preflight.BASELINE_RUN_REL
    baseline.mkdir(parents=True)
    data = {"trajectory.jsonl": b'{"fixture":"baseline"}\n', "summary.json": b'{"fixture":true}\n'}
    for name, raw in data.items(): (baseline / name).write_bytes(raw)
    monkeypatch.setattr(preflight, "ISOLATED_ROOT", root)
    monkeypatch.setattr(preflight, "BASELINE_FILES", tuple(
        (name, hashlib.sha256(raw).hexdigest(), 4096) for name, raw in data.items()))
    monkeypatch.setattr(invocation, "ISOLATED_ROOT", root)
    monkeypatch.setattr(invocation, "CANDIDATE_ROOT", root / "generation2/pair-03/candidate")
    events = []
    state = SimpleNamespace(root=root, baseline=baseline, data=data, events=events, executor_calls=[],
                            failure=None, revoke_after_readiness=False, head=HEAD, source_ok=True,
                            preflight_mutation=None, receipt_mutation=None)
    def check_python(): events.append("python")
    def verify(parts, self_sha):
        events.append("sources")
        if not state.source_ok: raise HOLD("inert-source-change")
        return {"inert-source": "7" * 40}
    def current(backend, head):
        events.append("main")
        if head != state.head: raise HOLD("inert-head-change")
        return {"head": head, "tree": TREE}
    def sudo():
        events.append("sudo")
        return state.failure != "sudo"
    def collect(**kwargs):
        events.append("preflight")
        if state.failure == "preflight": raise HOLD("inert-preflight-refusal")
        snap = {"fixture": True, "expected_main_head": kwargs["expected_main_head"]}
        result = {"candidate_host_conditions_validated": True, "expected_main_head": HEAD,
                  "completed_baseline_preserved": True, "legacy_runtime_authority_inherited": False,
                  "candidate_execution_authorized": False, "single_use_attempt_consumed": False,
                  "observed_host_snapshot": snap, "observed_host_snapshot_sha256": invocation._digest(snap),
                  "baseline_files": invocation._baseline_files(preflight)}
        if state.preflight_mutation: state.preflight_mutation(result)
        return result
    def ready(context):
        events.append("readiness")
        if state.failure == "readiness": raise HOLD("inert-readiness-refusal")
        if state.revoke_after_readiness: (root / invocation.REVOCATION_NAME).write_bytes(b"revoked")
        return {"fixture": "readiness-only"}
    def execute(**kwargs):
        events.append("executor")
        state.executor_calls.append(kwargs)
        assert (root / invocation.CLAIMS_NAME / attempt.MARKER_NAME).is_file()
        assert kwargs["pair_slot"] == 3 and kwargs["arm"] == "candidate"
        assert kwargs["candidate_genome_path"] == str(invocation.SOURCE_ROOT / invocation.CANDIDATE_FIXTURE)
        assert kwargs["isolated_workdir_root"] == str(root)
        assert kwargs["execution_authorized"] is True
        assert kwargs["run_git"].__self__ is kwargs["path_exists"].__self__
        assert isinstance(kwargs["run_git"].__self__, git.CandidateGitBackend)
        assert kwargs["authority_check"](3, "candidate") is True
        assert kwargs["authority_check"](3, "baseline") is False
        assert kwargs["authority_check"](15, "candidate") is False
        if state.failure == "executor": raise HOLD("inert-executor-refusal")
        events.append("runtime-start-fixture")
        try:
            kwargs["readiness_provider"]({"pair_slot": 3, "arm": "candidate",
                "runtime_selection_key": "apollyon-v2r13-qualified-predecessor"})
            if not kwargs["authority_check"](3, "candidate"): raise HOLD("inert-revoked-after-readiness")
        finally:
            events.append("runtime-cleanup-fixture")
        result = valid_receipt(invocation.CANDIDATE_ROOT)
        if state.receipt_mutation: state.receipt_mutation(result)
        return result
    parts = SimpleNamespace(attempt=attempt, preflight=preflight, git=git,
                            baseline=SimpleNamespace(_sudo_cache_ready=sudo, _fresh_readiness_provider=ready),
                            executor=SimpleNamespace(execute_v2r13_arm=execute))
    state.parts = parts
    monkeypatch.setattr(invocation, "_check_python", check_python)
    monkeypatch.setattr(invocation, "_components", lambda: parts)
    monkeypatch.setattr(invocation, "_verify_sources", verify)
    monkeypatch.setattr(invocation, "_current_main", current)
    monkeypatch.setattr(preflight, "collect_pair03_candidate_host_preflight", collect)
    return state


def test_one_shot_composes_real_claims_baseline_reads_and_result(env):
    out = invoke()
    assert len(env.executor_calls) == 1
    assert env.events.index("preflight") < env.events.index("executor") < env.events.index("readiness")
    assert env.events.count("runtime-cleanup-fixture") == 1
    marker = env.root / invocation.CLAIMS_NAME / attempt.MARKER_NAME
    stored = env.root / invocation.CLAIMS_NAME / invocation.RESULT_NAME
    assert set(p.name for p in stored.parent.iterdir()) == {attempt.MARKER_NAME, invocation.RESULT_NAME}
    assert out["result_file_sha256"] == hashlib.sha256(stored.read_bytes()).hexdigest()
    assert json.loads(marker.read_bytes())["candidate_execution_authorized"] is False
    assert out["candidate_execution_performed"] is True  # Simulated dispatcher only.
    assert out["operator_authenticated"] is False
    assert out["policy_promotion_performed"] is False
    assert out["executor_receipt"]["candidate_binding"] == invocation._expected_candidate_binding()
    assert {name: (env.baseline / name).read_bytes() for name in env.data} == env.data
    before = stored.read_bytes(), marker.read_bytes()
    with pytest.raises(HOLD, match="PRIOR_RESULT_PRESENT"): invoke()
    assert len(env.executor_calls) == 1
    assert (stored.read_bytes(), marker.read_bytes()) == before


@pytest.mark.parametrize("overrides", [
    {"confirm": None}, {"confirm": True}, {"confirm": ""},
    {"confirm": "VOID_ABADDON_GENERATION2_V2R13_EXECUTE_PAIR03_BASELINE"},
    {"confirm": attempt.CLAIM_CONFIRMATION}, {"confirm": preflight.CONFIRM_TOKEN},
    {"confirm": git.CONFIRM_TOKEN}, {"expected_main_head": "A" * 40},
    {"expected_main_head": 3}, {"expected_invocation_source_sha256": "x" * 64},
    {"expected_invocation_source_sha256": "a" * 63},
])
def test_invalid_inputs_stop_before_components_or_host_access(monkeypatch, overrides):
    def forbidden(): raise AssertionError("host access")
    monkeypatch.setattr(invocation, "_components", forbidden)
    monkeypatch.setattr(invocation, "_check_python", forbidden)
    with pytest.raises(HOLD): invoke(**overrides)


def test_caller_cannot_supply_broad_authority_callbacks_paths_or_old_permits():
    for key in ("execution_authorized", "authority_check", "source_root", "authorization", "preflight", "pair_slot"):
        with pytest.raises(TypeError): invoke(**{key: True})


@pytest.mark.parametrize("failure", ["sudo", "preflight", "source", "head", "revocation"])
def test_preclaim_failures_never_consume_or_dispatch(env, failure):
    if failure in {"sudo", "preflight"}: env.failure = failure
    elif failure == "source": env.source_ok = False
    elif failure == "head": env.head = "d" * 40
    else: (env.root / invocation.REVOCATION_NAME).symlink_to(env.root / "missing")
    with pytest.raises(HOLD): invoke()
    assert env.executor_calls == []
    assert not (env.root / invocation.CLAIMS_NAME).exists()


@pytest.mark.parametrize("field,value", [
    ("candidate_host_conditions_validated", False), ("expected_main_head", "e" * 40),
    ("completed_baseline_preserved", False), ("legacy_runtime_authority_inherited", True),
    ("candidate_execution_authorized", True), ("single_use_attempt_consumed", True),
    ("observed_host_snapshot_sha256", "0" * 64), ("baseline_files", {}),
])
def test_bad_preflight_receipt_is_not_accepted(env, field, value):
    env.preflight_mutation = lambda row: row.update({field: value})
    with pytest.raises(HOLD): invoke()
    assert env.executor_calls == []
    assert not (env.root / invocation.CLAIMS_NAME).exists()


@pytest.mark.parametrize("failure", ["executor", "readiness", "revoked"])
def test_postclaim_failure_preserves_slot_and_never_retries(env, failure):
    if failure == "revoked": env.revoke_after_readiness = True
    else: env.failure = failure
    with pytest.raises(HOLD): invoke()
    marker = env.root / invocation.CLAIMS_NAME / attempt.MARKER_NAME
    assert marker.is_file()
    before = marker.read_bytes()
    assert not (marker.parent / invocation.RESULT_NAME).exists()
    env.failure = None
    env.revoke_after_readiness = False
    sentinel = env.root / invocation.REVOCATION_NAME
    if sentinel.exists(): sentinel.unlink()  # Fixture recovery does not reset marker.
    with pytest.raises(attempt.CandidateAttemptHold, match="ALREADY_EXISTS"): invoke()
    assert len(env.executor_calls) == 1 and marker.read_bytes() == before


@pytest.mark.parametrize("field,value", [
    ("pair_slot", True), ("pair_slot", 15), ("arm", "baseline"), ("held_out", True),
    ("runtime_execution_performed", False), ("runtime_started", False),
    ("runtime_cleanup_completed", False), ("fresh_runtime_readiness_admitted", False),
    ("revocation_checked_before_inference", False), ("automatic_retry", True),
    ("training_performed", True), ("weights_updated", True),
    ("automatic_policy_promotion", True), ("wallet_or_funds_action_performed", True),
    ("candidate_binding", {}), ("execution_receipt_sha256", "0" * 64),
])
def test_wrong_executor_results_cannot_publish_success(env, field, value):
    def mutation(row):
        row[field] = value
        if field != "execution_receipt_sha256":
            row["execution_receipt_sha256"] = invocation._digest({k: v for k, v in row.items() if k != "execution_receipt_sha256"})
    env.receipt_mutation = mutation
    with pytest.raises(HOLD): invoke()
    assert len(env.executor_calls) == 1
    assert (env.root / invocation.CLAIMS_NAME / attempt.MARKER_NAME).is_file()
    assert not (env.root / invocation.CLAIMS_NAME / invocation.RESULT_NAME).exists()


@pytest.mark.parametrize("kind", ["permissive", "symlink", "file"])
def test_claim_namespace_does_not_adopt_unsafe_paths(env, kind):
    path = env.root / invocation.CLAIMS_NAME
    if kind == "permissive": path.mkdir(mode=0o755)
    elif kind == "symlink": path.symlink_to(env.baseline, target_is_directory=True)
    else: path.write_bytes(b"preserve")
    with pytest.raises((HOLD, OSError)): invoke()
    assert env.executor_calls == []
    assert not (env.baseline / attempt.MARKER_NAME).exists()


def test_baseline_change_after_executor_preserves_claim_and_refuses_result(env):
    previous = env.parts.executor.execute_v2r13_arm
    def changed(**kwargs):
        result = previous(**kwargs)
        (env.baseline / "summary.json").write_bytes(b"changed-after-execution")
        return result
    env.parts.executor.execute_v2r13_arm = changed
    with pytest.raises(preflight.CandidateHostPreflightHold): invoke()
    assert (env.root / invocation.CLAIMS_NAME / attempt.MARKER_NAME).is_file()
    assert not (env.root / invocation.CLAIMS_NAME / invocation.RESULT_NAME).exists()


def test_readiness_callback_rejects_wrong_context_before_preload(env):
    def wrong(**kwargs):
        for key, val in (("pair_slot", True), ("pair_slot", 9), ("arm", "baseline"), ("runtime_selection_key", "other")):
            context = {"pair_slot": 3, "arm": "candidate", "runtime_selection_key": "apollyon-v2r13-qualified-predecessor"}
            context[key] = val
            with pytest.raises(HOLD, match="CONTEXT"): kwargs["readiness_provider"](context)
        raise HOLD("inert-test-complete")
    env.parts.executor.execute_v2r13_arm = wrong
    with pytest.raises(HOLD, match="test-complete"): invoke()
    assert "readiness" not in env.events


def test_revocation_immediately_after_claim_prevents_dispatch(env, monkeypatch):
    original = attempt.consume_candidate_attempt
    def revoke(**kwargs):
        result = original(**kwargs)
        (env.root / invocation.REVOCATION_NAME).write_bytes(b"revoke")
        return result
    monkeypatch.setattr(attempt, "consume_candidate_attempt", revoke)
    with pytest.raises(HOLD, match="AFTER_CONSUMPTION"): invoke()
    assert env.executor_calls == []
    assert (env.root / invocation.CLAIMS_NAME / attempt.MARKER_NAME).is_file()


@pytest.mark.parametrize("fault", ["partial", "write_error", "sync_error", "existing"])
def test_result_write_is_create_only_and_retains_uncertain_bytes(tmp_path, monkeypatch, fault):
    tmp_path.chmod(0o700)
    with preflight._open_directory(tmp_path) as fd:
        path = tmp_path / invocation.RESULT_NAME
        if fault == "existing": path.write_bytes(b"preserve-existing")
        write, sync = os.write, os.fsync
        if fault == "partial": monkeypatch.setattr(invocation.os, "write", lambda d, raw: write(d, raw[:3]))
        elif fault == "write_error":
            def fail(*args): raise OSError("inert-write")
            monkeypatch.setattr(invocation.os, "write", fail)
        elif fault == "sync_error":
            def fail(*args): raise OSError("inert-sync")
            monkeypatch.setattr(invocation.os, "fsync", fail)
        if fault == "partial":
            digest = invocation._write_result(fd, {"fixture": True}, preflight)
            assert digest == hashlib.sha256(path.read_bytes()).hexdigest()
        else:
            with pytest.raises(OSError): invocation._write_result(fd, {"fixture": True}, preflight)
            assert path.is_file()
            if fault == "existing": assert path.read_bytes() == b"preserve-existing"
        monkeypatch.setattr(invocation.os, "write", write)
        monkeypatch.setattr(invocation.os, "fsync", sync)
        before = path.read_bytes()
        with pytest.raises(FileExistsError): invocation._write_result(fd, {"fixture": False}, preflight)
        assert path.read_bytes() == before


def test_source_reader_checks_actual_bytes_bounds_and_symlinks(tmp_path):
    path = tmp_path / "source.py"
    path.write_bytes(b"inert source\n")
    assert invocation._read_file(path, 100, preflight) == b"inert source\n"
    with pytest.raises(HOLD, match="SHAPE"): invocation._read_file(path, 3, preflight)
    link = tmp_path / "linked.py"
    link.symlink_to(path)
    with pytest.raises(OSError): invocation._read_file(link, 100, preflight)


@pytest.mark.parametrize("status,accepted", [("", True), ("?? cache/file\n", True), (" M tracked.py\n", False), ("?? cache\nM  source.py\n", False)])
def test_current_main_uses_tracked_clean_policy_only(status, accepted):
    class Queries:
        def run_git(self, root, *args):
            values = {("symbolic-ref", "-q", "HEAD"): "refs/heads/main\n", ("rev-parse", "HEAD"): HEAD + "\n",
                      ("rev-parse", "HEAD^{tree}"): TREE + "\n", ("status", "--porcelain", "--untracked-files=all"): status}
            return SimpleNamespace(returncode=0, stdout=values[args])
    if accepted: assert invocation._current_main(Queries(), HEAD) == {"head": HEAD, "tree": TREE}
    else:
        with pytest.raises(HOLD, match="DIRTY"): invocation._current_main(Queries(), HEAD)


def test_descriptors_are_closed_after_success_and_failure(env):
    before = len(list(Path("/proc/self/fd").iterdir()))
    invoke()
    assert len(list(Path("/proc/self/fd").iterdir())) == before
    with pytest.raises(HOLD, match="PRIOR_RESULT_PRESENT"): invoke()
    assert len(list(Path("/proc/self/fd").iterdir())) == before


# Full-checkout integration: actual accepted executor and its actual readiness
# hooks; inert legacy runner, worktree/model adapters and static plan are fixtures.
@pytest.mark.parametrize("failure", [None, "readiness", "revoked"])
def test_complete_repository_actual_executor_control_flow(env, monkeypatch, failure):
    from openra_env.learning import abaddon_policy_campaign_runtime_v2r13_bounded_executor_generation2 as executor
    env.parts.executor = executor
    env.failure = failure if failure == "readiness" else None
    env.revoke_after_readiness = failure == "revoked"
    events = env.events
    runner = env.root / "inert-legacy.py"
    runner.write_bytes(b"# never executed\n")
    monkeypatch.setattr(invocation, "LEGACY_RUNNER", runner)
    monkeypatch.setattr(executor, "LEGACY_RUNNER_SHA256", hashlib.sha256(runner.read_bytes()).hexdigest())
    plan = {"pair_slot": 3, "arm": "candidate", "held_out": False, "workdir_token": "generation2/pair-03/candidate",
            "execution_index": 1, "plan_sha256": "a" * 64, "runner_argv": ()}
    monkeypatch.setattr(executor, "execution_plan", lambda **kw: deepcopy(plan))
    source = env.root / "source"
    source.mkdir()
    (source / "OpenRA").mkdir()
    monkeypatch.setattr(invocation, "SOURCE_ROOT", source)
    helper = SimpleNamespace(start_ollama=lambda: events.append("actual-hook-inert-start"),
                             cleanup=lambda: events.append("actual-hook-inert-cleanup"))
    helper_path = env.root / "inert-helper.py"
    class Base:
        APOLLYON_RUNNER = helper_path
        def load_module(self, path, name): return helper
    legacy = SimpleNamespace(RUNS_DIR=env.root / "prior", load_base=lambda: Base())
    def main():
        loaded = legacy.load_base().load_module(helper_path, "inert-helper")
        loaded.start_ollama()
        events.append("inert-decision")
        run = legacy.RUNS_DIR / "actual-executor-inert-fixture"
        run.mkdir()
        for name in ("warm-start.jsonl", "trajectory.jsonl", "summary.json"): (run / name).write_text('{"fixture":true}\n')
        loaded.cleanup()
    legacy.main = main
    monkeypatch.setattr(executor, "_load_exact_module", lambda *args: legacy)
    monkeypatch.setattr(executor, "_ensure_dojo_import_root", lambda: (env.root, False))
    class Portable:
        def __init__(self, *args, **kwargs): pass
        def install(self): events.append("portable-install")
        def restore(self): events.append("portable-restore")
        def attestation(self): return {"fixture": True}
    monkeypatch.setattr(executor.portable_checkout, "PortableRunnerBinding", Portable)
    monkeypatch.setattr(executor.worktree_materializer, "materialize_v2r13_frozen_worktrees",
                        lambda *args, **kwargs: {"materialization_performed": True, "path_input_record": {"fixture": True}})
    monkeypatch.setattr(executor.worktree_materializer, "cleanup_v2r13_frozen_worktrees",
                        lambda *args, **kwargs: events.append("worktree-cleanup-fixture"))
    monkeypatch.setattr(executor, "_candidate_hooks", lambda *args, **kwargs: (
        SimpleNamespace(install=lambda: events.append("candidate-install"), restore=lambda: events.append("candidate-restore")),
        invocation._expected_candidate_binding()))
    monkeypatch.setattr(executor.readiness_binding, "admit_bound_v2r13_evidence", lambda evidence: {
        "runtime_readiness_admitted": True, "collector_identity_admitted": True, "runtime_execution_authorized": False})
    if failure:
        with pytest.raises((HOLD, executor.V2R13BoundedRuntimeExecutorHold)): invoke()
        assert "inert-decision" not in events
    else:
        result = invoke()
        assert result["candidate_execution_performed"] is True
        assert events.index("actual-hook-inert-start") < events.index("readiness") < events.index("inert-decision")
    assert events.count("actual-hook-inert-start") == events.count("actual-hook-inert-cleanup") == 1
    assert events.count("candidate-restore") == events.count("portable-restore") == events.count("worktree-cleanup-fixture") == 1
    assert (env.root / invocation.CLAIMS_NAME / attempt.MARKER_NAME).is_file()


def test_complete_repository_dependency_bytes_and_origins():
    parts = invocation._components()
    for relative, expected_blob in (*invocation.request.SOURCE_REFERENCES, *invocation.PINNED_SOURCES):
        raw = (REPO / relative).read_bytes()
        assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == expected_blob
    assert parts.baseline.ARM == "baseline"  # No global rebinding to candidate.
    assert parts.executor.execute_v2r13_arm.__module__ == parts.executor.__name__


@pytest.mark.parametrize("kind", ["file", "dangling_symlink"])
def test_prior_result_without_marker_is_not_a_fresh_attempt(env, kind):
    directory = env.root / invocation.CLAIMS_NAME
    directory.mkdir(mode=0o700)
    result = directory / invocation.RESULT_NAME
    if kind == "file": result.write_bytes(b"existing-result")
    else: result.symlink_to(directory / "missing")
    with pytest.raises(HOLD, match="PRIOR_RESULT_PRESENT"): invoke()
    assert env.executor_calls == []
    assert not (directory / attempt.MARKER_NAME).exists()


def test_actual_source_verifier_rejects_origin_and_byte_drift(tmp_path, monkeypatch):
    source = tmp_path / "source"
    own = source / invocation.SELF_PATH
    own.parent.mkdir(parents=True)
    own.write_bytes(b"# fixture invocation\n")
    monkeypatch.setattr(invocation, "SOURCE_ROOT", source)
    monkeypatch.setattr(invocation, "__file__", str(own))
    own_sha = hashlib.sha256(own.read_bytes()).hexdigest()
    suffixes = {
        "attempt": "pair03_candidate_attempt_guard_generation2.py",
        "preflight": "pair03_candidate_host_preflight_generation2.py",
        "git": "pair03_candidate_git_backend_generation2.py",
        "baseline": "first_baseline_invocation_generation2.py",
        "executor": "bounded_executor_generation2.py",
    }
    parts = SimpleNamespace(**{name: SimpleNamespace(__file__=str(source / (invocation.PREFIX + suffix)))
                              for name, suffix in suffixes.items()})
    parts.preflight._open_directory = preflight._open_directory
    parts.preflight._identity = preflight._identity
    request_file = source / (invocation.PREFIX + "pair03_candidate_authorization_request_generation2.py")
    request_file.write_bytes(b"# fixture dependency\n")
    raw = request_file.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    relative = request_file.relative_to(source).as_posix()
    monkeypatch.setattr(invocation, "request", SimpleNamespace(__file__=str(request_file), SOURCE_REFERENCES=((relative, blob),)))
    monkeypatch.setattr(invocation, "PINNED_SOURCES", ())
    assert invocation._verify_sources(parts, own_sha) == {relative: blob}
    with pytest.raises(HOLD, match="INVOCATION_SOURCE_DRIFT"): invocation._verify_sources(parts, "0" * 64)
    request_file.write_bytes(b"# changed dependency\n")
    with pytest.raises(HOLD, match="DEPENDENCY_SOURCE_DRIFT"): invocation._verify_sources(parts, own_sha)
    parts.baseline.__file__ = str(source / "unexpected-baseline.py")
    with pytest.raises(HOLD, match="DEPENDENCY_ORIGIN_HOLD"): invocation._verify_sources(parts, own_sha)


@pytest.mark.parametrize("fault", [None, "system_interpreter", "wrong_prefix", "not_venv", "bytecode"])
def test_interpreter_check_requires_the_actual_designated_venv(monkeypatch, fault):
    monkeypatch.setattr(invocation.sys, "executable", str(invocation.PROTO_PYTHON))
    monkeypatch.setattr(invocation.sys, "prefix", str(invocation.PROTO_PYTHON.parent.parent))
    monkeypatch.setattr(invocation.sys, "base_prefix", "/usr")
    monkeypatch.setattr(invocation.sys, "dont_write_bytecode", True)
    if fault == "system_interpreter": monkeypatch.setattr(invocation.sys, "executable", "/usr/bin/python3")
    elif fault == "wrong_prefix": monkeypatch.setattr(invocation.sys, "prefix", "/tmp/another-venv")
    elif fault == "not_venv": monkeypatch.setattr(invocation.sys, "base_prefix", invocation.sys.prefix)
    elif fault == "bytecode": monkeypatch.setattr(invocation.sys, "dont_write_bytecode", False)
    if fault:
        with pytest.raises(HOLD): invocation._check_python()
    else: invocation._check_python()
