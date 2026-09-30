from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_runtime_integration_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_runtime_integration_and_tests_to_repository_bytes():
    out = (
        review
        .pair06_v9_strict_visible_contact_runtime_integration_review_contract()
    )

    assert out["integration_path"] == review.INTEGRATION_PATH
    assert out["integration_git_blob"] == review.INTEGRATION_GIT_BLOB
    assert out["integration_test_path"] == review.INTEGRATION_TEST_PATH
    assert (
        out["integration_test_git_blob"]
        == review.INTEGRATION_TEST_GIT_BLOB
    )

    assert (
        _git_blob_sha1((ROOT / review.INTEGRATION_PATH).read_bytes())
        == review.INTEGRATION_GIT_BLOB
    )
    assert (
        _git_blob_sha1((ROOT / review.INTEGRATION_TEST_PATH).read_bytes())
        == review.INTEGRATION_TEST_GIT_BLOB
    )


def test_one_byte_runtime_integration_drift_breaks_blob_identity():
    raw = (ROOT / review.INTEGRATION_PATH).read_bytes()
    assert _git_blob_sha1(raw) == review.INTEGRATION_GIT_BLOB

    mutated = raw[:-1] + bytes([raw[-1] ^ 1])
    assert _git_blob_sha1(mutated) != review.INTEGRATION_GIT_BLOB


def test_review_closes_only_decision_hook_integration_frontier():
    out = (
        review
        .pair06_v9_strict_visible_contact_runtime_integration_review_contract()
    )

    assert (
        out["pair06_v9_strict_visible_contact_runtime_integration_reviewed"]
        is True
    )
    assert out["decision_hook_runtime_integration_implemented"] is True
    assert out["coherent_filtered_surface_reviewed"] is True
    assert out["unchanged_legacy_host_validator_reviewed"] is True
    assert out["six_attempt_fail_closed_retry_reviewed"] is True
    assert out["frozen_compact_state_reuse_reviewed"] is True
    assert out["proto_game_child_wiring_implemented"] is False
    assert out["parent_supervisor_wiring_implemented"] is False
    assert out["operator_invocation_implemented"] is False
    assert out["new_execution_request_opened"] is False


@pytest.mark.parametrize(
    "field",
    (
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
    ),
)
def test_review_grants_no_effect_authority(field):
    out = (
        review
        .pair06_v9_strict_visible_contact_runtime_integration_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_proto_child_wiring():
    out = (
        review
        .pair06_v9_strict_visible_contact_runtime_integration_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_PROTO_CHILD_WIRING_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_PROTO_CHILD_WIRING_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_pair06_v9_strict_visible_contact_proto_child_wiring"
    )


def test_wire_or_execute_holds():
    with pytest.raises(
        review.Pair06V9StrictVisibleContactRuntimeIntegrationReviewHold,
        match="PROTO_CHILD_WIRING_REQUIRED",
    ):
        review.wire_or_execute()
