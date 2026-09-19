from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_preservation_evidence_acceptance_generation2
    as acceptance,
)


def test_exact_preservation_evidence_is_accepted():
    out = acceptance.v2r13_pair03_baseline_preservation_evidence_acceptance_contract()
    assert out["preservation_evidence_accepted"] is True
    assert out["preservation_receipt_sha256"] == (
        "564be959096b6895aae3158eb3020d6b2062dcfdbf461e04a7969b8cee815dd9"
    )
    assert out["preservation_receipt_file_sha256"] == (
        "bc6ee5394b8526da429d9b95acc5a1a852fde6c2c728f7732e2bebbebb1552b7"
    )


def test_preservation_acceptance_opens_exactly_one_retry():
    out = acceptance.accept_pair03_baseline_preservation_evidence(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["pair_slot"] == 3
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["failed_attempt_preserved"] is True
    assert out["canonical_arm_path_available_for_retry"] is True
    assert out["retry_authorization_accepted"] is True
    assert out["retry_execution_authorized_now"] is True
    assert out["max_retry_executions"] == 1
    assert out["remaining_retry_executions"] == 1
    assert out["automatic_retry"] is False
    assert out["runtime_retry_performed"] is False


def test_retry_scope_does_not_expand():
    out = acceptance.accept_pair03_baseline_preservation_evidence(
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
        ("archive_path_present_after_preservation", False),
        ("preservation_receipt_present", False),
        ("atomic_rename_performed", False),
        ("archived_tree_unchanged", False),
        ("arm_root_inode_preserved", False),
        ("warm_start_inode_preserved", False),
        ("failed_attempt_deleted", True),
        ("runtime_retry_performed", True),
        ("runtime_start_performed", True),
        ("model_inference_performed", True),
        ("game_execution_performed", True),
        ("training_performed", True),
        ("automatic_policy_promotion", True),
        ("ollama_active_after", "active"),
    ],
)
def test_tampered_preservation_evidence_is_rejected(field, value):
    evidence = deepcopy(acceptance.EXPECTED_EVIDENCE)
    evidence[field] = value
    with pytest.raises(
        acceptance.V2R13Pair03BaselinePreservationEvidenceAcceptanceHold,
        match=f"preservation evidence drift: {field}",
    ):
        acceptance.accept_pair03_baseline_preservation_evidence(evidence)


def test_evidence_field_expansion_is_rejected():
    evidence = deepcopy(acceptance.EXPECTED_EVIDENCE)
    evidence["second_retry_authorized"] = True
    with pytest.raises(
        acceptance.V2R13Pair03BaselinePreservationEvidenceAcceptanceHold,
        match="preservation evidence field-set drift",
    ):
        acceptance.accept_pair03_baseline_preservation_evidence(evidence)


def test_acceptance_advances_only_to_retry_invocation_implementation():
    out = acceptance.v2r13_pair03_baseline_preservation_evidence_acceptance_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_RETRY_INVOCATION_IMPLEMENTATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR03_BASELINE_RETRY_INVOCATION_IMPLEMENTATION_REQUIRED"
    )


def test_direct_retry_entrypoint_remains_closed_until_invocation_source():
    with pytest.raises(
        acceptance.V2R13Pair03BaselinePreservationEvidenceAcceptanceHold,
        match="V2R13_PAIR03_BASELINE_RETRY_INVOCATION_IMPLEMENTATION_REQUIRED",
    ):
        acceptance.execute_retry()
