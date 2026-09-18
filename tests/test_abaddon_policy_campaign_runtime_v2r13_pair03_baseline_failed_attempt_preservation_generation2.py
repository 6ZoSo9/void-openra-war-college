from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_attempt_preservation_generation2
    as preservation,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_attempt_preservation_generation2.py"
)
CLI = (
    REPO
    / "tools/"
    "abaddon_policy_campaign_runtime_v2r13_precision_preserve_failed_pair03_baseline_generation2.py"
)


def test_contract_preserves_failed_attempt_without_retry():
    out = preservation.v2r13_pair03_baseline_failed_attempt_preservation_contract()
    assert out["exact_failed_tree_required"] is True
    assert out["atomic_same_filesystem_rename_implemented"] is True
    assert out["inode_identity_preservation_checked"] is True
    assert out["archived_tree_mutation_after_rename"] is False
    assert out["failed_attempt_deletion_implemented"] is False
    assert out["runtime_retry_implemented_by_this_source"] is False
    assert out["runtime_retry_authorized"] is False
    assert out["automatic_retry"] is False


def test_contract_pins_exact_failed_attempt_identity():
    out = preservation.v2r13_pair03_baseline_failed_attempt_preservation_contract()
    assert out["forensics_sha256"] == (
        "98773549a75d9567202879b49db1e6e1afaaa2cae38b8c7077882bc6e4949d6d"
    )
    assert out["warm_start_sha256"] == (
        "88e36aad38a92269046e3439fb6e94c5918395f93e5147f15a6c0f6dcf244f28"
    )
    assert out["warm_start_bytes"] == 223319
    assert out["archive_name"] == "baseline-20260918T233630Z-98773549"


def test_exact_confirmation_token_is_required():
    with pytest.raises(
        preservation.V2R13Pair03BaselineFailedAttemptPreservationHold,
        match="FAILED_ATTEMPT_PRESERVATION_CONFIRMATION_REQUIRED",
    ):
        preservation.preserve_failed_pair03_baseline(confirm="wrong")


def test_source_has_atomic_rename_but_no_delete_calls():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
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


def test_source_does_not_implement_runtime_retry_or_training_calls():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    called = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                called.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                called.add(node.func.attr)
    forbidden = {
        "execute_v2r13_arm",
        "start_ollama",
        "train",
        "fit",
        "backward",
        "optimizer_step",
        "promote",
        "deploy",
        "broadcast_transaction",
    }
    assert not (called & forbidden)


def test_cli_is_preservation_only():
    text = CLI.read_text(encoding="utf-8")
    assert "--confirm" in text
    assert "--pair-slot" not in text
    assert "--arm" not in text
    assert "runtime_retry=false" in text
    assert "runtime_start=false" in text
    assert "model_inference=false" in text


def test_retry_entrypoint_remains_closed():
    with pytest.raises(
        preservation.V2R13Pair03BaselineFailedAttemptPreservationHold,
        match="V2R13_PAIR03_BASELINE_RETRY_NOT_YET_AUTHORIZED",
    ):
        preservation.authorize_retry()


def test_preservation_advances_only_to_retry_authorization():
    out = preservation.v2r13_pair03_baseline_failed_attempt_preservation_contract()
    assert out["next_gate"] == (
        "V2R13_PAIR03_BASELINE_FAILED_ATTEMPT_PRESERVATION_SOURCE_BINDING_REVIEW_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_v2r13_pair03_baseline_failed_attempt_preservation_review"
    )
