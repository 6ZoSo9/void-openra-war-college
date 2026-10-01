from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_repair_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_repair_and_tests_to_repository_bytes():
    out = review.pair06_v9_input_order_coherence_repair_review_contract()

    assert out["repair_path"] == review.REPAIR_PATH
    assert out["repair_git_blob"] == review.REPAIR_GIT_BLOB
    assert out["repair_test_path"] == review.REPAIR_TEST_PATH
    assert out["repair_test_git_blob"] == review.REPAIR_TEST_GIT_BLOB

    assert (
        _git_blob_sha1((ROOT / review.REPAIR_PATH).read_bytes())
        == review.REPAIR_GIT_BLOB
    )
    assert (
        _git_blob_sha1((ROOT / review.REPAIR_TEST_PATH).read_bytes())
        == review.REPAIR_TEST_GIT_BLOB
    )


def test_one_byte_repair_drift_breaks_blob_identity():
    raw = (ROOT / review.REPAIR_PATH).read_bytes()
    assert _git_blob_sha1(raw) == review.REPAIR_GIT_BLOB

    mutated = raw[:-1] + bytes([raw[-1] ^ 1])
    assert _git_blob_sha1(mutated) != review.REPAIR_GIT_BLOB


def test_review_preserves_historical_failure_and_narrow_repair_boundary():
    out = review.pair06_v9_input_order_coherence_repair_review_contract()

    assert out["pair06_v9_input_order_coherence_repair_reviewed"] is True
    assert out["runtime_failure_signature"] == (
        "typed tools and offered_tool_names order or membership disagree"
    )
    assert out["historical_v9_policy_source_modified"] is False
    assert out["typed_tool_membership_exact_match_required"] is True
    assert out["typed_tool_order_may_differ_on_input"] is True
    assert out["typed_tool_order_canonicalized_to_offered_order"] is True
    assert out["membership_drift_still_fail_closed"] is True
    assert out["historical_policy_called_after_canonicalization"] is True


@pytest.mark.parametrize(
    "field",
    (
        "consumed_v9_attempt_retry_authorized",
        "new_execution_request_opened",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_review_grants_no_retry_or_effect_authority(field):
    out = review.pair06_v9_input_order_coherence_repair_review_contract()
    assert out[field] is False


def test_review_advances_only_to_runtime_integration():
    out = review.pair06_v9_input_order_coherence_repair_review_contract()

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "RUNTIME_INTEGRATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "RUNTIME_INTEGRATION_REQUIRED"
    )


def test_integrate_or_execute_holds():
    with pytest.raises(
        review.Pair06V9InputOrderCoherenceRepairReviewHold,
        match="INPUT_ORDER_COHERENCE_RUNTIME_INTEGRATION_REQUIRED",
    ):
        review.integrate_or_execute()
