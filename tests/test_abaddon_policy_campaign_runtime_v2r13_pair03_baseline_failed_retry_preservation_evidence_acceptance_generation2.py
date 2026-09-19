from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_failed_retry_preservation_evidence_acceptance_generation2
    as acceptance,
)


def test_exact_preservation_evidence_is_accepted():
    out = (
        acceptance
        .v2r13_pair03_failed_retry_preservation_evidence_acceptance_contract()
    )
    assert out["preservation_evidence_accepted"] is True
    assert out["preservation_receipt_sha256"] == (
        "833fb5bde1bbb96d6e2ceedff615fd86bf3b2522d21687d900355cbe705a0f15"
    )
    assert out["preservation_receipt_file_sha256"] == (
        "007127f4834e3b2c772316f2f65a3b355c308a7a451eca996ad00c21f3f7cd28"
    )


def test_acceptance_closes_preservation_without_authorizing_retry():
    out = acceptance.accept_pair03_failed_retry_preservation_evidence(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["pair_slot"] == 3
    assert out["arm"] == "baseline"
    assert out["retry_index"] == 1
    assert out["failed_retry_preserved"] is True
    assert out["canonical_arm_path_available_for_future_authorized_execution"] is True
    assert out["original_first_attempt_archive_preserved"] is True
    assert out["failed_retry_archive_preserved"] is True
    assert out["retry_authorization_consumed"] is True
    assert out["additional_retry_authorized"] is False
    assert out["additional_retry_performed"] is False
    assert out["runtime_execution_authorized_now"] is False
    assert out["automatic_retry"] is False


def test_acceptance_does_not_expand_scope():
    out = acceptance.accept_pair03_failed_retry_preservation_evidence(
        acceptance.EXPECTED_EVIDENCE
    )
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


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("canonical_arm_path_absent_after_preservation", False),
        ("retry_archive_present_after_preservation", False),
        ("retry_preservation_receipt_present", False),
        ("atomic_rename_performed", False),
        ("archive_root_inode_preserved", False),
        ("retry_warm_start_inode_preserved", False),
        ("archived_retry_tree_unchanged", False),
        ("original_first_attempt_archive_preserved", False),
        ("failed_retry_deleted", True),
        ("additional_retry_authorized", True),
        ("additional_retry_performed", True),
        ("runtime_start_performed", True),
        ("model_load_performed", True),
        ("model_inference_performed", True),
        ("game_execution_performed", True),
        ("ollama_active_after", "active"),
    ],
)
def test_tampered_preservation_evidence_is_rejected(field, value):
    evidence = deepcopy(acceptance.EXPECTED_EVIDENCE)
    evidence[field] = value
    with pytest.raises(
        acceptance.V2R13Pair03FailedRetryPreservationEvidenceAcceptanceHold,
        match=f"preservation evidence drift: {field}",
    ):
        acceptance.accept_pair03_failed_retry_preservation_evidence(evidence)


def test_preservation_evidence_field_expansion_is_rejected():
    evidence = deepcopy(acceptance.EXPECTED_EVIDENCE)
    evidence["third_retry_authorized"] = True
    with pytest.raises(
        acceptance.V2R13Pair03FailedRetryPreservationEvidenceAcceptanceHold,
        match="preservation evidence field-set drift",
    ):
        acceptance.accept_pair03_failed_retry_preservation_evidence(evidence)


def test_acceptance_advances_only_to_additional_retry_authorization():
    out = (
        acceptance
        .v2r13_pair03_failed_retry_preservation_evidence_acceptance_contract()
    )
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_AUTHORIZATION_REQUIRED"
    )


def test_additional_retry_entrypoint_holds():
    with pytest.raises(
        acceptance.V2R13Pair03FailedRetryPreservationEvidenceAcceptanceHold,
        match="V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_AUTHORIZATION_REQUIRED",
    ):
        acceptance.authorize_additional_retry()
