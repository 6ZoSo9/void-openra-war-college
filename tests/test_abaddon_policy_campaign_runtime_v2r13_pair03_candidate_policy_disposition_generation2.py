from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_policy_disposition_generation2
    as disposition,
)


def test_disposition_pins_exact_result_review_source():
    out = disposition.v2r13_pair03_candidate_policy_disposition_contract()
    assert out["result_review_git_blob"] == "1078ff9771b6ba8ba3957b8005e5689d65d41709"
    assert out["result_review_source_sha256"] == (
        "c3b3f9141c5e5ecfeb21b201b978c7739b2ca656b4ae4ea5e35749208ceed6f2"
    )


def test_pair03_disposition_preserves_inconclusive_candidate():
    out = disposition.v2r13_pair03_candidate_policy_disposition_contract()
    assert out["policy_disposition_made"] is True
    assert out["policy_disposition"] == (
        "PRESERVE_PENDING_ADDITIONAL_BOUNDED_EVALUATION"
    )
    assert out["pair03_measurement_conclusive"] is False
    assert out["candidate_preserved_as_evidence"] is True
    assert out["candidate_promoted"] is False
    assert out["candidate_rejected"] is False


def test_disposition_basis_matches_reviewed_pair03_measurement():
    out = disposition.v2r13_pair03_candidate_policy_disposition_contract()
    assert out["disposition_basis"] == {
        "baseline_outcome": "DRAW_OR_UNFINISHED",
        "candidate_outcome": "DRAW_OR_UNFINISHED",
        "rounds_completed": 36,
        "same_seed": True,
        "same_final_tick": True,
        "decisive_candidate_advantage_observed": False,
        "mixed_metric_deltas_observed": True,
    }
    assert out["observed_pairwise_deltas"] == disposition.EXPECTED_DELTAS


def test_additional_evaluation_is_required_but_not_authorized_for_execution():
    out = disposition.v2r13_pair03_candidate_policy_disposition_contract()
    assert out["additional_bounded_evaluation_required"] is True
    assert out["pair09_evaluation_design_required"] is True
    assert out["pair09_execution_authorized"] is False
    assert out["held_out_execution_authorized"] is False
    assert out["candidate_replay_permitted"] is False
    assert out["another_candidate_execution_authorized"] is False


def test_disposition_grants_no_training_promotion_or_external_authority():
    out = disposition.v2r13_pair03_candidate_policy_disposition_contract()
    for field in (
        "training_authorized",
        "training_performed",
        "weights_update_authorized",
        "weights_updated",
        "automatic_policy_promotion_authorized",
        "automatic_policy_promotion",
        "deployment_authorized",
        "deployment_performed",
        "void_chain_mutation_authorized",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_authorized",
        "wallet_or_funds_action_performed",
    ):
        assert out[field] is False


def test_disposition_requires_separate_source_binding_review():
    out = disposition.v2r13_pair03_candidate_policy_disposition_contract()
    assert out["source_binding_reviewed"] is False
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_CANDIDATE_POLICY_DISPOSITION_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR03_CANDIDATE_POLICY_DISPOSITION_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_all_execution_or_promotion_entrypoints_hold():
    with pytest.raises(
        disposition.V2R13Pair03CandidatePolicyDispositionHold,
        match="V2R13_PAIR09_EXECUTION_NOT_AUTHORIZED",
    ):
        disposition.authorize_pair09_execution()

    with pytest.raises(
        disposition.V2R13Pair03CandidatePolicyDispositionHold,
        match="V2R13_HELD_OUT_EXECUTION_NOT_AUTHORIZED",
    ):
        disposition.authorize_held_out_execution()

    with pytest.raises(
        disposition.V2R13Pair03CandidatePolicyDispositionHold,
        match="V2R13_CANDIDATE_PROMOTION_AND_TRAINING_NOT_AUTHORIZED",
    ):
        disposition.promote_or_train_candidate()
