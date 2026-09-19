from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_additional_retry_invocation_generation2
    as retry,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair03_baseline_additional_retry_invocation_generation2.py"
)
CLI = (
    REPO
    / "tools/"
    "abaddon_policy_campaign_runtime_v2r13_precision_pair03_baseline_additional_retry_generation2.py"
)


def test_contract_is_retry_index_two_pair03_baseline_only():
    out = retry.v2r13_pair03_baseline_additional_retry_invocation_contract()
    assert out["pair_slot"] == 3
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["retry_index"] == 2
    assert out["max_additional_retry_executions"] == 1
    assert out["total_retry_executions_authorized"] == 2
    assert out["additional_retry_execution_authorized"] is True
    assert out["additional_retry_execution_performed_by_contract_inspection"] is False


def test_contract_requires_both_failed_attempt_archives():
    out = retry.v2r13_pair03_baseline_additional_retry_invocation_contract()
    assert out["live_preserved_history_recheck_required"] is True
    assert out["first_failed_attempt_archive_recheck_required"] is True
    assert out["retry1_failed_attempt_archive_recheck_required"] is True
    assert out["retry1_preservation_receipt_sha256"] == (
        "833fb5bde1bbb96d6e2ceedff615fd86bf3b2522d21687d900355cbe705a0f15"
    )
    assert out["retry1_preservation_receipt_file_sha256"] == (
        "007127f4834e3b2c772316f2f65a3b355c308a7a451eca996ad00c21f3f7cd28"
    )
    assert out["retry1_preserved_warm_start_sha256"] == (
        "0d01cc86255842b4ad3eb5d754c59362dcbfb00d5697a9bbf2897457f03ff798"
    )


def test_contract_requires_repaired_readiness_path():
    out = retry.v2r13_pair03_baseline_additional_retry_invocation_contract()
    assert out["repaired_first_baseline_executor_reused"] is True
    assert out["worktree_readiness_repair_review_required"] is True
    assert out["model_preload_repair_review_required"] is True
    assert out["exact_v2r13_model_preload_before_readiness_required"] is True
    assert out["model_preload_inference_forbidden"] is True


def test_contract_has_no_automatic_or_recursive_retry():
    out = retry.v2r13_pair03_baseline_additional_retry_invocation_contract()
    assert out["automatic_retry"] is False
    assert out["recursive_retry_implemented"] is False
    assert out["remaining_additional_retry_executions_before_invocation"] == 1


def test_contract_preserves_nontraining_nonpromotion_scope():
    out = retry.v2r13_pair03_baseline_additional_retry_invocation_contract()
    for field in (
        "candidate_arm_implemented_by_this_source",
        "held_out_arm_implemented_by_this_source",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_exact_confirmation_token_is_required(monkeypatch):
    calls = []

    def bomb(**kwargs):
        calls.append(kwargs)
        raise AssertionError("underlying executor must not run")

    monkeypatch.setattr(retry.first_baseline, "execute_first_baseline", bomb)
    with pytest.raises(
        retry.V2R13Pair03BaselineAdditionalRetryInvocationHold,
        match="PAIR03_BASELINE_ADDITIONAL_RETRY_CONFIRMATION_REQUIRED",
    ):
        retry.execute_pair03_baseline_additional_retry(confirm="wrong")
    assert calls == []


def test_source_calls_first_baseline_exactly_once():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "execute_first_baseline"
    ]
    assert len(calls) == 1


def test_source_does_not_call_itself_or_old_retry():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    called = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                called.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                called.add(node.func.attr)
    assert "execute_pair03_baseline_additional_retry" not in called
    assert "execute_pair03_baseline_retry" not in called


def test_cli_is_fixed_to_confirmation_only():
    text = CLI.read_text(encoding="utf-8")
    assert "--confirm" in text
    assert "--pair-slot" not in text
    assert "--arm" not in text
    assert "retry_index=2" in text
    assert "automatic_retry=false" in text
    assert "recursive_retry=false" in text


def test_next_gate_is_execution_evidence_acceptance():
    assert retry.NEXT_GATE == (
        "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_EXECUTION_EVIDENCE_ACCEPTANCE_REQUIRED"
    )
