from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_parent_supervisor_wiring_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_child_entrypoint_parent_wiring_and_tests():
    out = (
        review
        .pair06_v9_strict_visible_contact_parent_wiring_review_contract()
    )

    assert out["child_entry_git_blob"] == review.CHILD_ENTRY_GIT_BLOB
    assert out["child_entry_test_git_blob"] == review.CHILD_ENTRY_TEST_GIT_BLOB
    assert out["parent_wiring_git_blob"] == review.PARENT_WIRING_GIT_BLOB
    assert (
        out["parent_wiring_test_git_blob"]
        == review.PARENT_WIRING_TEST_GIT_BLOB
    )

    assert (
        _git_blob_sha1((ROOT / review.CHILD_ENTRY_PATH).read_bytes())
        == review.CHILD_ENTRY_GIT_BLOB
    )
    assert (
        _git_blob_sha1((ROOT / review.CHILD_ENTRY_TEST_PATH).read_bytes())
        == review.CHILD_ENTRY_TEST_GIT_BLOB
    )
    assert (
        _git_blob_sha1((ROOT / review.PARENT_WIRING_PATH).read_bytes())
        == review.PARENT_WIRING_GIT_BLOB
    )
    assert (
        _git_blob_sha1((ROOT / review.PARENT_WIRING_TEST_PATH).read_bytes())
        == review.PARENT_WIRING_TEST_GIT_BLOB
    )


def test_one_byte_child_entrypoint_drift_breaks_blob_identity():
    raw = (ROOT / review.CHILD_ENTRY_PATH).read_bytes()
    assert _git_blob_sha1(raw) == review.CHILD_ENTRY_GIT_BLOB
    mutated = raw[:-1] + bytes([raw[-1] ^ 1])
    assert _git_blob_sha1(mutated) != review.CHILD_ENTRY_GIT_BLOB


def test_one_byte_parent_wiring_drift_breaks_blob_identity():
    raw = (ROOT / review.PARENT_WIRING_PATH).read_bytes()
    assert _git_blob_sha1(raw) == review.PARENT_WIRING_GIT_BLOB
    mutated = raw[:-1] + bytes([raw[-1] ^ 1])
    assert _git_blob_sha1(mutated) != review.PARENT_WIRING_GIT_BLOB


def test_review_closes_only_child_entrypoint_and_parent_wiring_frontier():
    out = (
        review
        .pair06_v9_strict_visible_contact_parent_wiring_review_contract()
    )

    assert out[
        "pair06_v9_strict_visible_contact_parent_wiring_reviewed"
    ] is True
    assert out["v9_child_entrypoint_reviewed"] is True
    assert out["existing_no_offload_parent_source_modified"] is False
    assert out["execution_confirmation_token_preserved"] is True
    assert out["distinct_v9_policy_activation_token_preserved"] is True
    assert out["durable_attempt_claim_prerequisite_preserved"] is True
    assert out["no_offload_cuda0_parent_path_preserved"] is True
    assert out["scoped_child_command_substitution_reviewed"] is True
    assert out["child_command_restored_in_finally_reviewed"] is True
    assert out["operator_entrypoint_wiring_implemented"] is False
    assert out["execution_request_created"] is False
    assert out["attempt_claim_created"] is False
    assert out["attempt_created"] is False


@pytest.mark.parametrize(
    "field",
    (
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "automatic_retry",
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
def test_review_grants_no_effect_authority(field):
    out = (
        review
        .pair06_v9_strict_visible_contact_parent_wiring_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_operator_entrypoint_wiring():
    out = (
        review
        .pair06_v9_strict_visible_contact_parent_wiring_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_OPERATOR_ENTRYPOINT_WIRING_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_OPERATOR_ENTRYPOINT_WIRING_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_pair06_v9_strict_visible_contact_operator_entrypoint_wiring"
    )


def test_wire_operator_or_execute_holds():
    with pytest.raises(
        review.Pair06V9StrictVisibleContactParentWiringReviewHold,
        match="OPERATOR_ENTRYPOINT_WIRING_REQUIRED",
    ):
        review.wire_operator_or_execute()
