from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_retry_preservation_generation2
    as contract,
)
from tools import (
    abaddon_policy_campaign_runtime_v2r13_precision_preserve_failed_retry_generation2
    as tool,
)

REPO = Path(__file__).resolve().parents[1]
TOOL_SOURCE = (
    REPO
    / "tools/"
    "abaddon_policy_campaign_runtime_v2r13_precision_preserve_failed_retry_generation2.py"
)


def test_contract_pins_exact_failed_retry_and_original_archive():
    out = contract.v2r13_pair03_baseline_failed_retry_preservation_contract()
    assert out["failed_retry_forensics_sha256"] == (
        "71e90fdcc834e28c7b2fabb22b46bd6e5d133773021c6355ea8dea1bf61f2c6d"
    )
    assert out["failed_retry_warm_start_sha256"] == (
        "0d01cc86255842b4ad3eb5d754c59362dcbfb00d5697a9bbf2897457f03ff798"
    )
    assert out["failed_retry_warm_start_bytes"] == 223319
    assert out["original_warm_start_sha256"] == (
        "88e36aad38a92269046e3439fb6e94c5918395f93e5147f15a6c0f6dcf244f28"
    )
    assert out["original_preservation_receipt_file_sha256"] == (
        "bc6ee5394b8526da429d9b95acc5a1a852fde6c2c728f7732e2bebbebb1552b7"
    )


def test_contract_grants_no_additional_retry_or_runtime_authority():
    out = contract.v2r13_pair03_baseline_failed_retry_preservation_contract()
    assert out["failed_retry_deletion_authorized"] is False
    assert out["additional_retry_authorized"] is False
    assert out["automatic_retry"] is False
    for field in (
        "runtime_start_authorized",
        "model_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_tool_requires_exact_confirmation_before_mutation():
    with pytest.raises(tool.Hold, match="PRESERVATION_CONFIRMATION_REQUIRED"):
        tool.preserve("wrong")


def test_tool_source_has_atomic_rename_and_no_delete_api():
    tree = ast.parse(TOOL_SOURCE.read_text(encoding="utf-8"), filename=str(TOOL_SOURCE))
    attrs = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    assert "rename" in attrs
    forbidden = {
        "unlink",
        "rmdir",
        "remove",
        "removedirs",
        "rmtree",
    }
    assert not (attrs & forbidden)


def test_tool_source_does_not_start_runtime_or_retry():
    tree = ast.parse(TOOL_SOURCE.read_text(encoding="utf-8"), filename=str(TOOL_SOURCE))
    called = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                called.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                called.add(node.func.attr)
    forbidden = {
        "execute_pair03_baseline_retry",
        "execute_first_baseline",
        "execute_v2r13_arm",
        "start_ollama",
        "train",
        "fit",
        "promote",
        "deploy",
        "broadcast_transaction",
    }
    assert not (called & forbidden)


def test_tool_cli_is_fixed_to_preservation_only():
    text = TOOL_SOURCE.read_text(encoding="utf-8")
    assert "--confirm" in text
    assert "--pair-slot" not in text
    assert "--arm" not in text
    assert "additional_retry=false" in text
    assert "runtime_start=false" in text
    assert "model_load=false" in text
    assert "model_inference=false" in text


def test_contract_advances_to_source_binding_review_only():
    out = contract.v2r13_pair03_baseline_failed_retry_preservation_contract()
    assert out["preservation_implemented"] is True
    assert out["precision_preservation_tool_present"] is True
    assert out["precision_preservation_tool_source_binding_present"] is False
    assert out["preservation_invoked"] is False
    assert out["next_gate"] == (
        "V2R13_PAIR03_BASELINE_FAILED_RETRY_PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED"
    )
