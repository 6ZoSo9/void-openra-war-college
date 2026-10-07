from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_structured_correction_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_source_and_tests_to_exact_bytes():
    out = (
        review
        .pair06_v9_actionable_feedback_v3_structured_correction_review_contract()
    )

    assert out["source_path"] == review.SOURCE_PATH
    assert out["source_git_blob"] == review.SOURCE_GIT_BLOB
    assert out["test_path"] == review.TEST_PATH
    assert out["test_git_blob"] == review.TEST_GIT_BLOB

    assert _git_blob_sha1((ROOT / review.SOURCE_PATH).read_bytes()) == (
        review.SOURCE_GIT_BLOB
    )
    assert _git_blob_sha1((ROOT / review.TEST_PATH).read_bytes()) == (
        review.TEST_GIT_BLOB
    )


def test_review_binds_exact_trigger_and_structured_feedback():
    out = (
        review
        .pair06_v9_actionable_feedback_v3_structured_correction_review_contract()
    )

    assert out[
        "pair06_v9_actionable_feedback_v3_structured_correction_reviewed"
    ] is True
    assert out["exact_v2_trigger"].startswith("function_not_offered:")
    assert out["move_units_unit_ids_required_json_type"] == "string"
    assert isinstance(out["structured_feedback_sha256"], str)
    assert len(out["structured_feedback_sha256"]) == 64


def test_review_requires_transfer_prompt_and_preserves_fail_closed_runtime():
    out = (
        review
        .pair06_v9_actionable_feedback_v3_structured_correction_review_contract()
    )

    assert out["preserve_transfer_system_prompt_required"] is True
    assert out["legacy_prompt_fallback_for_v3_correction_forbidden"] is True

    for field in (
        "frozen_v8_tool_schema_modified",
        "frozen_v8_parser_modified",
        "frozen_v8_translator_modified",
        "host_validator_modified",
        "six_attempt_bound_modified",
        "malformed_unit_ids_coerced",
        "malformed_unit_ids_accepted",
        "runtime_execution_authorized",
        "automatic_retry",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_v3_runtime_integration():
    out = (
        review
        .pair06_v9_actionable_feedback_v3_structured_correction_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V3_STRUCTURED_CORRECTION_RUNTIME_INTEGRATION_REQUIRED"
    )

    with pytest.raises(
        review.Pair06V9ActionableFeedbackV3StructuredCorrectionReviewHold,
        match="STRUCTURED_CORRECTION_RUNTIME_INTEGRATION_REQUIRED",
    ):
        review.integrate_or_execute()
