"""Pair-09 candidate invocation wiring with inert runtime simulation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_invocation_generation2
    as invocation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_host_preflight_generation2
    as preflight,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_attempt_guard_generation2
    as attempt,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_git_backend_generation2
    as git,
)

HEAD = "a" * 40
TREE = "b" * 40
SELF_SHA = "c" * 64
HOLD = invocation.V2R13Pair09CandidateInvocationHold


def invoke(**overrides):
    return invocation.execute_pair09_candidate(
        **{
            "expected_main_head": HEAD,
            "expected_invocation_source_sha256": SELF_SHA,
            "authorization_accepted": True,
            "confirm": invocation.CONFIRM_TOKEN,
            **overrides,
        }
    )


def valid_receipt(root):
    out = {
        "schema": (
            "void.abaddon.generation2."
            "v2r13-bounded-runtime-execution-receipt.v1"
        ),
        "pair_slot": 9,
        "arm": "candidate",
        "held_out": False,
        "candidate_binding": invocation._expected_candidate_binding(),
        "run_artifact": {
            "run_id": "inert-pair09-candidate-fixture",
            "run_dir": str(
                root / "runs/inert-pair09-candidate-fixture"
            ),
            "warm_start_sha256": "d" * 64,
            "trajectory_sha256": "e" * 64,
            "summary_sha256": "f" * 64,
            "summary": {"fixture_only": True},
        },
    }
    out.update(
        {
            field: True
            for field in (
                "runtime_execution_authorized",
                "runtime_execution_performed",
                "runtime_started",
                "runtime_cleanup_attempted",
                "runtime_cleanup_completed",
                "fresh_runtime_readiness_admitted",
                "revocation_checked_before_materialization",
                "revocation_checked_before_inference",
            )
        }
    )
    out.update(
        {
            field: False
            for field in (
                "automatic_retry",
                "training_performed",
                "weights_updated",
                "automatic_policy_promotion",
                "deployment_performed",
                "void_chain_mutation_performed",
                "wallet_or_funds_action_performed",
            )
        }
    )
    return {
        **out,
        "execution_receipt_sha256": invocation._digest(out),
    }


@pytest.fixture
def env(tmp_path, monkeypatch):
    root = tmp_path / "execution"
    root.mkdir()
    root.chmod(0o700)

    preserved_rel = Path("pair09-baseline-claims-v1/evidence.json")
    preserved = root / preserved_rel
    preserved.parent.mkdir(parents=True)
    preserved.write_bytes(b'{"pair09_baseline":"preserved"}\n')
    preserved_sha = hashlib.sha256(preserved.read_bytes()).hexdigest()

    monkeypatch.setattr(preflight, "ISOLATED_ROOT", root)
    monkeypatch.setattr(
        preflight,
        "PRESERVED_FILES",
        ((preserved_rel, preserved_sha, 4096),),
    )
    monkeypatch.setattr(invocation, "ISOLATED_ROOT", root)
    monkeypatch.setattr(
        invocation,
        "CANDIDATE_ROOT",
        root / "generation2/pair-09/candidate",
    )
    monkeypatch.setattr(
        invocation,
        "SOURCE_ROOT",
        tmp_path / "source-root",
    )

    events = []
    state = SimpleNamespace(
        root=root,
        preserved=preserved,
        preserved_bytes=preserved.read_bytes(),
        events=events,
        executor_calls=[],
        failure=None,
        revoke_after_readiness=False,
        head=HEAD,
        source_ok=True,
        preflight_mutation=None,
        receipt_mutation=None,
    )

    def check_python():
        events.append("python")

    def source_chain(parts):
        events.append("source-chain")

    def verify(parts, self_sha):
        events.append("sources")
        if not state.source_ok:
            raise HOLD("inert-source-change")
        return {"inert-source": "7" * 40}

    def current(backend, head):
        events.append("main")
        if head != state.head:
            raise HOLD("inert-head-change")
        return {"head": head, "tree": TREE}

    def sudo():
        events.append("sudo")
        return state.failure != "sudo"

    def collect(**kwargs):
        events.append("preflight")
        if state.failure == "preflight":
            raise HOLD("inert-preflight-refusal")
        snap = {
            "fixture": True,
            "expected_main_head": kwargs["expected_main_head"],
        }
        preserved_rows = invocation._preserved_evidence(preflight)
        result = {
            "pair09_candidate_host_conditions_validated": True,
            "expected_main_head": HEAD,
            "pair03_baseline_preserved": True,
            "pair03_candidate_preserved": True,
            "pair09_baseline_preserved": True,
            "pair09_candidate_absent": True,
            "held_out_pair15_absent": True,
            "legacy_runtime_authority_inherited": False,
            "single_use_attempt_consumed": False,
            "pair09_candidate_execution_authorized": False,
            "observed_host_snapshot": snap,
            "observed_host_snapshot_sha256": invocation._digest(snap),
            "preserved_evidence": preserved_rows,
        }
        if state.preflight_mutation:
            state.preflight_mutation(result)
        return result

    def ready(context):
        events.append("readiness")
        if state.failure == "readiness":
            raise HOLD("inert-readiness-refusal")
        if state.revoke_after_readiness:
            (root / invocation.REVOCATION_NAME).write_bytes(b"revoked")
        return {"fixture": "readiness-only"}

    def execute(**kwargs):
        events.append("executor")
        state.executor_calls.append(kwargs)
        marker = root / invocation.CLAIMS_NAME / attempt.MARKER_NAME
        assert marker.is_file()
        assert kwargs["pair_slot"] == 9
        assert kwargs["arm"] == "candidate"
        assert kwargs["candidate_genome_path"] == str(
            invocation.SOURCE_ROOT / invocation.CANDIDATE_FIXTURE
        )
        assert kwargs["isolated_workdir_root"] == str(root)
        assert kwargs["execution_authorized"] is True
        assert kwargs["run_git"].__self__ is kwargs["path_exists"].__self__
        assert isinstance(
            kwargs["run_git"].__self__,
            git.Pair09CandidateGitBackend,
        )
        assert kwargs["authority_check"](9, "candidate") is True
        assert kwargs["authority_check"](9, "baseline") is False
        assert kwargs["authority_check"](15, "candidate") is False

        if state.failure == "executor":
            raise HOLD("inert-executor-refusal")

        events.append("runtime-start-fixture")
        try:
            kwargs["readiness_provider"](
                {
                    "pair_slot": 9,
                    "arm": "candidate",
                    "runtime_selection_key": (
                        "apollyon-v2r13-qualified-predecessor"
                    ),
                }
            )
            if not kwargs["authority_check"](9, "candidate"):
                raise HOLD("inert-revoked-after-readiness")
        finally:
            events.append("runtime-cleanup-fixture")

        result = valid_receipt(invocation.CANDIDATE_ROOT)
        if state.receipt_mutation:
            state.receipt_mutation(result)
        return result

    parts = SimpleNamespace(
        attempt=attempt,
        preflight=preflight,
        git=git,
        baseline=SimpleNamespace(
            _sudo_cache_ready=sudo,
            _fresh_readiness_provider=ready,
        ),
        executor=SimpleNamespace(execute_v2r13_arm=execute),
    )
    state.parts = parts

    monkeypatch.setattr(invocation, "_check_python", check_python)
    monkeypatch.setattr(invocation, "_components", lambda: parts)
    monkeypatch.setattr(invocation, "_validate_source_chain", source_chain)
    monkeypatch.setattr(invocation, "_verify_sources", verify)
    monkeypatch.setattr(invocation, "_current_main", current)
    monkeypatch.setattr(
        preflight,
        "collect_pair09_candidate_host_preflight",
        collect,
    )
    return state


def test_contract_is_implemented_but_non_authorizing():
    out = invocation.pair09_candidate_invocation_contract()
    assert out["pair09_candidate_invocation_implemented"] is True
    assert out["pair09_candidate_invocation_reviewed"] is False
    assert out["pair_slot"] == 9
    assert out["arm"] == "candidate"
    assert out["held_out"] is False
    assert out["explicit_authorization_boolean_required"] is True
    assert out["explicit_confirmation_token_required"] is True
    assert out["pair09_candidate_specific_authorization_accepted"] is False
    assert out["single_use_attempt_consumed"] is False
    assert out["pair09_candidate_execution_authorized"] is False
    assert out["pair09_candidate_execution_performed"] is False
    assert out["pair09_baseline_rerun_authorized"] is False
    assert out["runtime_execution_performed_by_contract_inspection"] is False


def test_one_shot_simulation_consumes_before_executor_and_writes_result(env):
    out = invoke()
    assert len(env.executor_calls) == 1
    assert env.events.index("preflight") < env.events.index("executor")
    assert env.events.index("executor") < env.events.index("readiness")
    assert env.events.count("runtime-cleanup-fixture") == 1

    marker = env.root / invocation.CLAIMS_NAME / attempt.MARKER_NAME
    stored = env.root / invocation.CLAIMS_NAME / invocation.RESULT_NAME
    assert marker.is_file()
    assert stored.is_file()
    assert out["result_file_sha256"] == hashlib.sha256(
        stored.read_bytes()
    ).hexdigest()
    record = json.loads(marker.read_bytes())
    assert record["pair09_candidate_execution_authorized"] is False
    assert out["pair09_candidate_execution_performed"] is True
    assert out["operator_authenticated"] is False
    assert out["policy_promotion_performed"] is False
    assert env.preserved.read_bytes() == env.preserved_bytes

    before = (stored.read_bytes(), marker.read_bytes())
    with pytest.raises(HOLD, match="PRIOR_RESULT_PRESENT"):
        invoke()
    assert len(env.executor_calls) == 1
    assert (stored.read_bytes(), marker.read_bytes()) == before


@pytest.mark.parametrize(
    "overrides",
    [
        {"authorization_accepted": False},
        {"authorization_accepted": 1},
        {"confirm": None},
        {"confirm": True},
        {"confirm": ""},
        {"confirm": attempt.CLAIM_CONFIRMATION},
        {"confirm": preflight.CONFIRM_TOKEN},
        {"confirm": git.CONFIRM_TOKEN},
        {"expected_main_head": "A" * 40},
        {"expected_main_head": 3},
        {"expected_invocation_source_sha256": "x" * 64},
        {"expected_invocation_source_sha256": "a" * 63},
    ],
)
def test_invalid_inputs_stop_before_components(monkeypatch, overrides):
    def forbidden():
        raise AssertionError("host access")

    monkeypatch.setattr(invocation, "_components", forbidden)
    monkeypatch.setattr(invocation, "_check_python", forbidden)
    with pytest.raises(HOLD):
        invoke(**overrides)


@pytest.mark.parametrize(
    "failure",
    ["sudo", "preflight", "source", "head", "revocation"],
)
def test_preclaim_failures_never_consume_or_dispatch(env, failure):
    if failure in {"sudo", "preflight"}:
        env.failure = failure
    elif failure == "source":
        env.source_ok = False
    elif failure == "head":
        env.head = "d" * 40
    else:
        (env.root / invocation.REVOCATION_NAME).write_bytes(b"revoke")

    with pytest.raises(HOLD):
        invoke()
    assert env.executor_calls == []
    assert not (env.root / invocation.CLAIMS_NAME).exists()


@pytest.mark.parametrize(
    "field,value",
    [
        ("pair09_candidate_host_conditions_validated", False),
        ("expected_main_head", "e" * 40),
        ("pair03_baseline_preserved", False),
        ("pair03_candidate_preserved", False),
        ("pair09_baseline_preserved", False),
        ("pair09_candidate_absent", False),
        ("held_out_pair15_absent", False),
        ("legacy_runtime_authority_inherited", True),
        ("single_use_attempt_consumed", True),
        ("pair09_candidate_execution_authorized", True),
        ("observed_host_snapshot_sha256", "0" * 64),
        ("preserved_evidence", {}),
    ],
)
def test_bad_preflight_receipt_cannot_consume_attempt(
    env,
    field,
    value,
):
    env.preflight_mutation = lambda row: row.update({field: value})
    with pytest.raises(HOLD):
        invoke()
    assert env.executor_calls == []
    assert not (env.root / invocation.CLAIMS_NAME).exists()


@pytest.mark.parametrize("failure", ["executor", "readiness", "revoked"])
def test_postclaim_failures_preserve_marker_and_never_retry(env, failure):
    if failure == "revoked":
        env.revoke_after_readiness = True
    else:
        env.failure = failure

    with pytest.raises(HOLD):
        invoke()

    marker = env.root / invocation.CLAIMS_NAME / attempt.MARKER_NAME
    assert marker.is_file()
    before = marker.read_bytes()
    assert not (marker.parent / invocation.RESULT_NAME).exists()

    env.failure = None
    env.revoke_after_readiness = False
    sentinel = env.root / invocation.REVOCATION_NAME
    if sentinel.exists():
        sentinel.unlink()

    with pytest.raises(
        attempt.V2R13Pair09CandidateAttemptHold,
        match="ALREADY_EXISTS",
    ):
        invoke()
    assert len(env.executor_calls) == 1
    assert marker.read_bytes() == before


@pytest.mark.parametrize(
    "field,value",
    [
        ("pair_slot", 15),
        ("arm", "baseline"),
        ("held_out", True),
        ("runtime_execution_performed", False),
        ("runtime_cleanup_completed", False),
        ("fresh_runtime_readiness_admitted", False),
        ("revocation_checked_before_inference", False),
        ("automatic_retry", True),
        ("training_performed", True),
        ("weights_updated", True),
        ("automatic_policy_promotion", True),
        ("candidate_binding", {}),
        ("execution_receipt_sha256", "0" * 64),
    ],
)
def test_wrong_executor_results_cannot_publish_success(env, field, value):
    def mutation(row):
        row[field] = value
        if field != "execution_receipt_sha256":
            row["execution_receipt_sha256"] = invocation._digest(
                {
                    k: v
                    for k, v in row.items()
                    if k != "execution_receipt_sha256"
                }
            )

    env.receipt_mutation = mutation
    with pytest.raises(HOLD):
        invoke()

    assert len(env.executor_calls) == 1
    assert (
        env.root / invocation.CLAIMS_NAME / attempt.MARKER_NAME
    ).is_file()
    assert not (
        env.root / invocation.CLAIMS_NAME / invocation.RESULT_NAME
    ).exists()


def test_preserved_evidence_change_after_executor_refuses_result(env):
    previous = env.parts.executor.execute_v2r13_arm

    def changed(**kwargs):
        result = previous(**kwargs)
        env.preserved.write_bytes(b"changed-after-execution")
        return result

    env.parts.executor.execute_v2r13_arm = changed
    with pytest.raises(
        preflight.V2R13Pair09CandidateHostPreflightHold
    ):
        invoke()

    assert (
        env.root / invocation.CLAIMS_NAME / attempt.MARKER_NAME
    ).is_file()
    assert not (
        env.root / invocation.CLAIMS_NAME / invocation.RESULT_NAME
    ).exists()


def test_source_chain_distinguishes_git_capability_from_candidate_authority(
    monkeypatch,
):
    parts = invocation._components()
    git_review = (
        parts.git_review
        .v2r13_pair09_candidate_git_backend_review_contract()
    )
    assert "pair09_candidate_execution_authorized" not in git_review
    assert git_review["runtime_execution_authorized"] is False

    invocation._validate_source_chain(parts)

    def elevated_git_review():
        return {**git_review, "runtime_execution_authorized": True}

    monkeypatch.setattr(
        parts.git_review,
        "v2r13_pair09_candidate_git_backend_review_contract",
        elevated_git_review,
    )
    with pytest.raises(
        HOLD,
        match="PAIR09_CANDIDATE_INVOCATION_PREMATURE_RUNTIME_AUTHORITY",
    ):
        invocation._validate_source_chain(parts)


def test_invocation_advances_only_to_source_binding_review():
    out = invocation.pair09_candidate_invocation_contract()
    assert out["next_gate"] == (
        "V2R13_PAIR09_CANDIDATE_INVOCATION_"
        "SOURCE_BINDING_REVIEW_REQUIRED"
    )
