from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_bounded_executor_generation2
    as executor,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_bounded_executor_generation2.py"
)


def test_contract_exposes_exact_six_authorized_v2r13_arms():
    out = executor.bounded_v2r13_runtime_executor_contract()
    assert out["authorized_pair_slots"] == (3, 9, 15)
    assert out["held_out_pair_slots"] == (15,)
    assert out["authorized_arms"] == ("baseline", "candidate")
    assert out["authorized_execution_arm_count"] == 6
    assert len(out["execution_plans"]) == 6
    assert {
        (row["pair_slot"], row["arm"])
        for row in out["execution_plans"]
    } == {
        (3, "baseline"),
        (3, "candidate"),
        (9, "baseline"),
        (9, "candidate"),
        (15, "baseline"),
        (15, "candidate"),
    }


def test_contract_does_not_expand_other_runtime_or_training_authority():
    out = executor.bounded_v2r13_runtime_executor_contract()
    assert out["other_runtime_lanes_implemented_by_this_source"] is False
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


@pytest.mark.parametrize("pair_slot", [3, 9, 15])
@pytest.mark.parametrize("arm", ["baseline", "candidate"])
def test_execution_plan_preserves_exact_v2r13_authorization(pair_slot, arm):
    plan = executor.execution_plan(pair_slot=pair_slot, arm=arm)
    assert plan["pair_slot"] == pair_slot
    assert plan["arm"] == arm
    assert plan["runtime_selection_key"] == "apollyon-v2r13-qualified-predecessor"
    assert plan["runtime_execution_authorized"] is True
    assert plan["held_out"] is (pair_slot == 15)
    assert plan["fresh_runtime_readiness_required"] is True
    assert plan["revocation_check_required"] is True
    assert plan["automatic_retry"] is False
    assert len(plan["plan_sha256"]) == 64


@pytest.mark.parametrize("pair_slot", [1, 2, 4, 6, 12, 18])
def test_non_v2r13_pair_slots_are_rejected(pair_slot):
    with pytest.raises(
        executor.V2R13BoundedRuntimeExecutorHold,
        match="pair slot not authorized",
    ):
        executor.execution_plan(pair_slot=pair_slot, arm="baseline")


def test_unknown_arm_is_rejected():
    with pytest.raises(
        executor.V2R13BoundedRuntimeExecutorHold,
        match="arm not authorized",
    ):
        executor.execution_plan(pair_slot=3, arm="shadow")


def test_path_layout_is_deterministic_and_arm_scoped():
    plan = executor.execution_plan(pair_slot=15, arm="candidate")
    paths = executor._arm_paths("/tmp/void-g2-execution", plan)
    assert str(paths["arm_root"]) == (
        "/tmp/void-g2-execution/generation2/pair-15/candidate"
    )
    assert str(paths["source"]).endswith("/pair-15/candidate/frozen-source")
    assert str(paths["engine"]).endswith("/pair-15/candidate/engine")
    assert str(paths["runs"]).endswith("/pair-15/candidate/runs")


def test_execute_requires_explicit_per_call_authority_before_host_access():
    def forbidden(*args, **kwargs):
        raise AssertionError("host backend must not be reached")

    with pytest.raises(
        executor.V2R13BoundedRuntimeExecutorHold,
        match="not explicitly authorized",
    ):
        executor.execute_v2r13_arm(
            pair_slot=3,
            arm="baseline",
            isolated_workdir_root="/tmp/not-used",
            source_repository_root="/tmp/not-used-source",
            engine_repository_root="/tmp/not-used-engine",
            legacy_runner_path="/tmp/not-used-runner",
            candidate_genome_path=None,
            execution_authorized=False,
            authority_check=forbidden,
            readiness_provider=forbidden,
            path_exists=forbidden,
            run_git=forbidden,
        )


class _FakePortable:
    def attestation(self):
        return {
            "schema": "fake-portable-attestation",
            "legacy_source_root_bound": True,
            "legacy_engine_root_bound": True,
            "base_loaded_and_bound": True,
        }


def _fresh_hook_fixture(monkeypatch, provider, authority):
    calls = {"start": 0, "cleanup": 0}
    helper = SimpleNamespace()

    def start():
        calls["start"] += 1

    def cleanup():
        calls["cleanup"] += 1

    helper.start_ollama = start
    helper.cleanup = cleanup
    runner_path = Path("/tmp/fake-apollyon-runner.py")

    class Base:
        APOLLYON_RUNNER = runner_path

        @staticmethod
        def load_module(path, name):
            assert Path(path) == runner_path
            return helper

    class Legacy:
        @staticmethod
        def load_base():
            return Base()

    monkeypatch.setattr(
        executor.readiness_binding,
        "admit_bound_v2r13_evidence",
        lambda evidence: {
            "collector_identity_admitted": True,
            "runtime_readiness_admitted": True,
            "runtime_execution_authorized": False,
            "validated_evidence": dict(evidence),
        },
    )

    hooks = executor._FreshReadinessHooks(
        Legacy,
        _FakePortable(),
        pair_slot=3,
        arm="baseline",
        materialization_receipt={"schema": "fake-materialization"},
        readiness_provider=provider,
        authority_check=authority,
    )
    return hooks, Legacy, runner_path, calls


def test_fresh_readiness_hook_runs_after_start_and_before_return(monkeypatch):
    events = []

    def provider(context):
        events.append("readiness")
        assert context["pair_slot"] == 3
        assert context["arm"] == "baseline"
        assert context["runtime_selection_key"] == (
            "apollyon-v2r13-qualified-predecessor"
        )
        assert (
            context["portable_binding_attestation"]["base_loaded_and_bound"]
            is True
        )
        return {"schema": "fake-evidence"}

    def authority(pair_slot, arm):
        events.append("authority")
        return True

    hooks, legacy, runner_path, calls = _fresh_hook_fixture(
        monkeypatch,
        provider,
        authority,
    )
    hooks.install()
    try:
        base = legacy.load_base()
        helper = base.load_module(runner_path, "helper")
        helper.start_ollama()
    finally:
        hooks.restore()

    assert calls == {"start": 1, "cleanup": 0}
    assert events == ["authority", "readiness", "authority"]
    assert hooks.runtime_started is True
    assert hooks.runtime_cleanup_attempted is False
    assert hooks.runtime_cleanup_completed is False
    assert hooks.readiness_admission["runtime_readiness_admitted"] is True


def test_fresh_readiness_failure_cleans_started_runtime(monkeypatch):
    def provider(context):
        raise RuntimeError("fresh readiness failed")

    hooks, legacy, runner_path, calls = _fresh_hook_fixture(
        monkeypatch,
        provider,
        lambda pair_slot, arm: True,
    )
    hooks.install()
    try:
        base = legacy.load_base()
        helper = base.load_module(runner_path, "helper")
        with pytest.raises(RuntimeError, match="fresh readiness failed"):
            helper.start_ollama()
    finally:
        hooks.restore()

    assert calls == {"start": 1, "cleanup": 1}
    assert hooks.runtime_started is True
    assert hooks.runtime_cleanup_attempted is True
    assert hooks.runtime_cleanup_completed is True
    assert hooks.runtime_cleanup_after_hold is True


def test_revocation_after_readiness_cleans_started_runtime(monkeypatch):
    checks = iter([True, False])
    hooks, legacy, runner_path, calls = _fresh_hook_fixture(
        monkeypatch,
        lambda context: {"schema": "fake-evidence"},
        lambda pair_slot, arm: next(checks),
    )
    hooks.install()
    try:
        base = legacy.load_base()
        helper = base.load_module(runner_path, "helper")
        with pytest.raises(
            executor.V2R13BoundedRuntimeExecutorHold,
            match="revoked after readiness",
        ):
            helper.start_ollama()
    finally:
        hooks.restore()

    assert calls == {"start": 1, "cleanup": 1}
    assert hooks.runtime_cleanup_attempted is True
    assert hooks.runtime_cleanup_completed is True
    assert hooks.runtime_cleanup_after_hold is True


def test_normal_legacy_cleanup_is_observed_and_restored(monkeypatch):
    hooks, legacy, runner_path, calls = _fresh_hook_fixture(
        monkeypatch,
        lambda context: {"schema": "fake-evidence"},
        lambda pair_slot, arm: True,
    )
    hooks.install()
    base = legacy.load_base()
    helper = base.load_module(runner_path, "helper")
    wrapped_cleanup = helper.cleanup
    helper.start_ollama()
    helper.cleanup()
    assert calls == {"start": 1, "cleanup": 1}
    assert hooks.runtime_cleanup_attempted is True
    assert hooks.runtime_cleanup_completed is True
    hooks.restore()
    assert helper.cleanup is not wrapped_cleanup


def test_contract_advances_to_separate_source_binding_review():
    out = executor.bounded_v2r13_runtime_executor_contract()
    assert out["bounded_v2r13_runtime_executor_implemented"] is True
    assert out["bounded_v2r13_runtime_executor_reviewed"] is False
    assert out["successful_runtime_cleanup_observation_implemented"] is True
    assert out["next_gate"] == (
        "V2R13_RUNTIME_EXECUTION_IMPLEMENTATION_SOURCE_BINDING_REVIEW_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_v2r13_runtime_execution_implementation_source_binding_review"
    )


def test_execution_contract_inspection_performs_no_runtime_action():
    out = executor.bounded_v2r13_runtime_executor_contract()
    assert out["runtime_execution_performed_by_contract_inspection"] is False
    assert out["model_inference_performed_by_contract_inspection"] is False
    assert out["game_execution_performed_by_contract_inspection"] is False


def test_source_does_not_implement_network_or_subprocess_backend():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    forbidden = {"subprocess", "socket", "http", "httpx", "requests", "urllib"}
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(
                alias.name.split(".", 1)[0]
                for alias in node.names
            )
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".", 1)[0])
    assert not (imported & forbidden)


def test_other_runtime_lane_entrypoint_holds():
    with pytest.raises(
        executor.V2R13BoundedRuntimeExecutorHold,
        match="AUTHORIZATION_SCOPE_V2R13_ONLY",
    ):
        executor.execute_other_runtime_lane()
