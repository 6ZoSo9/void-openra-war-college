from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_additional_retry_invocation_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
REVIEW_SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair03_baseline_additional_retry_invocation_source_binding_review_generation2.py"
)


def test_exact_invocation_identities_are_pinned():
    out = review.v2r13_pair03_baseline_additional_retry_invocation_review_contract()
    assert out["invocation_git_blob"] == (
        "a00a5b0a206203298386121b79f30234465a4c16"
    )
    assert out["invocation_source_sha256"] == (
        "29e31bfe025ca9c1d57081e59d16c11373e5d9550757b872b9467e87e8975104"
    )
    assert out["precision_cli_git_blob"] == (
        "5556ad98ff2c82bd8792ae79aa092f16334f4db4"
    )
    assert out["precision_cli_source_sha256"] == (
        "2ffd9a916752e0587e156180d796d6b299d47dec93130f9da2f9bce754b6c2e8"
    )
    assert out["invocation_test_git_blob"] == (
        "01b272ba4d58f8698489c7873532c856757d25f2"
    )
    assert out["invocation_test_sha256"] == (
        "c5597ee7f6577733c99824ad328fe569b5d335dd104a0c6c8568a57b87807d4e"
    )


def test_review_binds_exact_retry_index_two_invocation():
    out = review.v2r13_pair03_baseline_additional_retry_invocation_review_contract()
    assert out["invocation_source_binding_present"] is True
    assert out["invocation_reviewed"] is True
    assert out["pair_slot"] == 3
    assert out["arm"] == "baseline"
    assert out["retry_index"] == 2
    assert out["single_additional_retry_invocation_reviewed"] is True


def test_review_requires_preserved_history_and_repaired_readiness():
    out = review.v2r13_pair03_baseline_additional_retry_invocation_review_contract()
    assert out["live_preserved_history_recheck_reviewed"] is True
    assert out["first_failed_attempt_archive_recheck_reviewed"] is True
    assert out["retry1_failed_attempt_archive_recheck_reviewed"] is True
    assert out["repaired_readiness_path_reviewed"] is True


def test_review_keeps_execution_unperformed_and_nonrecursive():
    out = review.v2r13_pair03_baseline_additional_retry_invocation_review_contract()
    assert out["automatic_retry"] is False
    assert out["recursive_retry"] is False
    assert out["runtime_execution_invoked"] is False
    assert out["runtime_execution_performed"] is False


def test_review_does_not_expand_scope():
    out = review.v2r13_pair03_baseline_additional_retry_invocation_review_contract()
    for field in (
        "candidate_arm_authorized",
        "held_out_arm_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_source_is_host_action_free():
    tree = ast.parse(
        REVIEW_SOURCE.read_text(encoding="utf-8"),
        filename=str(REVIEW_SOURCE),
    )
    forbidden = {
        "os",
        "pathlib",
        "socket",
        "subprocess",
        "urllib",
        "requests",
        "httpx",
    }
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".", 1)[0])
    assert not (imported & forbidden)


def test_review_advances_to_precision_invocation():
    out = review.v2r13_pair03_baseline_additional_retry_invocation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_INVOCATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_INVOCATION_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.V2R13Pair03BaselineAdditionalRetryInvocationReviewHold,
        match="V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_INVOCATION_REQUIRED",
    ):
        review.execute_additional_retry()
