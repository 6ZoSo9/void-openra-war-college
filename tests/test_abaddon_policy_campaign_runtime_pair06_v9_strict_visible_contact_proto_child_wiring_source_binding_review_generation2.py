from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_proto_child_wiring_source_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def test_review_pins_wiring_and_tests_to_repository_bytes():
    out = (
        review
        .pair06_v9_strict_visible_contact_proto_child_wiring_review_contract()
    )

    assert out["wiring_path"] == review.WIRING_PATH
    assert out["wiring_git_blob"] == review.WIRING_GIT_BLOB
    assert out["wiring_test_path"] == review.WIRING_TEST_PATH
    assert out["wiring_test_git_blob"] == review.WIRING_TEST_GIT_BLOB

    assert (
        _git_blob_sha1((ROOT / review.WIRING_PATH).read_bytes())
        == review.WIRING_GIT_BLOB
    )
    assert (
        _git_blob_sha1((ROOT / review.WIRING_TEST_PATH).read_bytes())
        == review.WIRING_TEST_GIT_BLOB
    )


def test_one_byte_wiring_drift_breaks_blob_identity():
    raw = (ROOT / review.WIRING_PATH).read_bytes()
    assert _git_blob_sha1(raw) == review.WIRING_GIT_BLOB

    mutated = raw[:-1] + bytes([raw[-1] ^ 1])
    assert _git_blob_sha1(mutated) != review.WIRING_GIT_BLOB


def test_review_closes_only_proto_child_wiring_frontier():
    out = (
        review
        .pair06_v9_strict_visible_contact_proto_child_wiring_review_contract()
    )

    assert (
        out["pair06_v9_strict_visible_contact_proto_child_wiring_reviewed"]
        is True
    )
    assert out["existing_proto_child_source_modified"] is False
    assert out["v9_proto_child_hook_subclass_reviewed"] is True
    assert out["hook_factory_substitution_scoped_to_single_call"] is True
    assert out["hook_factory_restored_in_finally"] is True
    assert out["original_child_execution_authorization_gate_preserved"] is True
    assert out["additional_v9_policy_activation_gate_required"] is True
    assert out["coherent_v9_tool_contract_path_preserved"] is True
    assert out["parent_supervisor_wiring_implemented"] is False
    assert out["operator_entrypoint_wiring_implemented"] is False
    assert out["new_execution_request_opened"] is False
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
        .pair06_v9_strict_visible_contact_proto_child_wiring_review_contract()
    )
    assert out[field] is False


def test_review_advances_only_to_parent_supervisor_wiring():
    out = (
        review
        .pair06_v9_strict_visible_contact_proto_child_wiring_review_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_PARENT_SUPERVISOR_WIRING_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_PARENT_SUPERVISOR_WIRING_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_pair06_v9_strict_visible_contact_parent_supervisor_wiring"
    )


def test_wire_parent_or_execute_holds():
    with pytest.raises(
        review.Pair06V9StrictVisibleContactProtoChildWiringReviewHold,
        match="PARENT_SUPERVISOR_WIRING_REQUIRED",
    ):
        review.wire_parent_or_execute()
