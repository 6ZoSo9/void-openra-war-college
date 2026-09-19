from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry_invocation_generation2
    as retry,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry_invocation_generation2.py"
)
CLI = (
    REPO
    / "tools/"
    "abaddon_policy_campaign_runtime_v2r13_precision_pair03_baseline_retry_generation2.py"
)


def test_contract_is_exactly_one_pair03_baseline_retry():
    out = retry.v2r13_pair03_baseline_retry_invocation_contract()
    assert out["pair_slot"] == 3
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["retry_index"] == 1
    assert out["max_retry_executions"] == 1
    assert out["retry_execution_authorized"] is True
    assert out["remaining_retry_executions_before_invocation"] == 1
    assert out["automatic_retry"] is False


def test_retry_contract_requires_live_preservation_recheck():
    out = retry.v2r13_pair03_baseline_retry_invocation_contract()
    assert out["live_preservation_recheck_required"] is True
    assert out["repaired_first_baseline_executor_reused"] is True
    assert out["preservation_receipt_sha256"] == (
        "564be959096b6895aae3158eb3020d6b2062dcfdbf461e04a7969b8cee815dd9"
    )
    assert out["preservation_receipt_file_sha256"] == (
        "bc6ee5394b8526da429d9b95acc5a1a852fde6c2c728f7732e2bebbebb1552b7"
    )


def test_retry_scope_does_not_expand():
    out = retry.v2r13_pair03_baseline_retry_invocation_contract()
    assert out["retry_execution_performed_by_contract_inspection"] is False
    assert out["candidate_arm_implemented_by_this_source"] is False
    assert out["held_out_arm_implemented_by_this_source"] is False
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_exact_retry_confirmation_token_is_required():
    with pytest.raises(
        retry.V2R13Pair03BaselineRetryInvocationHold,
        match="PAIR03_BASELINE_RETRY_CONFIRMATION_REQUIRED",
    ):
        retry.execute_pair03_baseline_retry(confirm="wrong")


def test_retry_calls_repaired_first_baseline_once(monkeypatch):
    calls = []

    monkeypatch.setattr(
        retry,
        "_validate_dependencies",
        lambda: {"authorized": True},
    )
    monkeypatch.setattr(
        retry,
        "_validate_preservation_on_host",
        lambda: {
            "preservation_receipt_sha256": retry.PRESERVATION_RECEIPT_SHA256,
            "preservation_receipt_file_sha256": retry.PRESERVATION_RECEIPT_FILE_SHA256,
            "warm_start_sha256": retry.WARM_START_SHA256,
        },
    )

    def fake_execute_first_baseline(*, confirm):
        calls.append(confirm)
        return {
            "pair_slot": 3,
            "arm": "baseline",
            "held_out": False,
            "runtime_execution_performed": True,
            "fresh_runtime_readiness_admitted": True,
            "runtime_cleanup_completed": True,
            "automatic_retry": False,
            "candidate_arm_executed": False,
            "held_out_arm_executed": False,
            "training_performed": False,
            "weights_updated": False,
            "automatic_policy_promotion": False,
            "deployment_performed": False,
            "void_chain_mutation_performed": False,
            "wallet_or_funds_action_performed": False,
            "invocation_receipt_sha256": "a" * 64,
            "executor_receipt": {"execution_receipt_sha256": "b" * 64},
        }

    monkeypatch.setattr(
        retry.first_baseline,
        "execute_first_baseline",
        fake_execute_first_baseline,
    )

    out = retry.execute_pair03_baseline_retry(confirm=retry.CONFIRM_TOKEN)
    assert calls == [retry.first_baseline.CONFIRM_TOKEN]
    assert out["retry_index"] == 1
    assert out["retry_authorization_consumed"] is True
    assert out["retry_execution_performed"] is True
    assert out["remaining_retry_executions"] == 0
    assert out["automatic_retry"] is False
    assert out["candidate_arm_executed"] is False
    assert out["held_out_arm_executed"] is False


def test_source_contains_no_second_retry_loop():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    loops = [node for node in ast.walk(tree) if isinstance(node, (ast.For, ast.While))]
    assert not loops


def test_source_uses_repaired_first_baseline_executor():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    attrs = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    assert "execute_first_baseline" in attrs


def test_cli_has_no_pair_or_arm_selector():
    text = CLI.read_text(encoding="utf-8")
    assert "--confirm" in text
    assert "--pair-slot" not in text
    assert "--arm" not in text
    assert "retry_index=1" in text
    assert "max_retry_executions=1" in text
    assert "automatic_retry=false" in text


def test_retry_advances_to_execution_evidence_acceptance():
    assert retry.NEXT_GATE == (
        "V2R13_PAIR03_BASELINE_RETRY_EXECUTION_EVIDENCE_ACCEPTANCE_REQUIRED"
    )
    assert retry.NEXT_CHANGE_CLASS == (
        "source_only_v2r13_pair03_baseline_retry_execution_evidence_acceptance"
    )
