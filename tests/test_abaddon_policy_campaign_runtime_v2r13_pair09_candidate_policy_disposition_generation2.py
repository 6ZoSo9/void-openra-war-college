from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_policy_disposition_generation2
    as disposition,
)


def test_disposition_pins_exact_result_review():
    out = disposition.v2r13_pair09_candidate_policy_disposition_contract()
    assert out["result_review_git_blob"] == (
        "372d935810b11e8a5046e21fe7049f3efbfa2f54"
    )
    assert out["result_review_source_sha256"] == (
        "faf47727b5b314d9877fb83f6e5da11ce31ddaeeba34e8faaca5273931c3079d"
    )


def test_pair09_candidate_is_preserved_without_promotion_or_rejection():
    out = disposition.v2r13_pair09_candidate_policy_disposition_contract()
    assert out["pair_slot"] == 9
    assert out["policy_disposition_made"] is True
    assert out["policy_disposition"] == (
        "PRESERVE_PENDING_ADDITIONAL_BOUNDED_EVALUATION"
    )
    assert out["pair09_measurement_conclusive"] is False
    assert out["candidate_preserved_as_evidence"] is True
    assert out["candidate_promoted"] is False
    assert out["candidate_rejected"] is False
    assert out["candidate_replay_permitted"] is False
    assert out["another_candidate_execution_authorized"] is False
    assert out["additional_bounded_evaluation_required"] is True
    assert out["post_pair09_evaluation_design_required"] is True


def test_disposition_preserves_exact_mixed_pairwise_deltas():
    out = disposition.v2r13_pair09_candidate_policy_disposition_contract()
    assert out["observed_pairwise_deltas"] == disposition.EXPECTED_DELTAS
    basis = out["disposition_basis"]
    assert basis["baseline_outcome"] == "DRAW_OR_UNFINISHED"
    assert basis["candidate_outcome"] == "DRAW_OR_UNFINISHED"
    assert basis["rounds_completed"] == 36
    assert basis["same_seed"] is True
    assert basis["same_final_tick"] is True
    assert basis["decisive_candidate_advantage_observed"] is False
    assert basis["mixed_metric_deltas_observed"] is True
    assert basis["held_out_evidence_used"] is False


def test_held_out_and_mutation_authority_remain_closed():
    out = disposition.v2r13_pair09_candidate_policy_disposition_contract()
    assert out["held_out_execution_authorized"] is False
    assert out["held_out_execution_performed"] is False
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


def test_disposition_advances_only_to_separate_source_review():
    out = disposition.v2r13_pair09_candidate_policy_disposition_contract()
    assert out["source_binding_reviewed"] is False
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_CANDIDATE_POLICY_DISPOSITION_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR09_CANDIDATE_POLICY_DISPOSITION_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_prohibited_action_entrypoints_hold():
    for fn, message in (
        (
            disposition.authorize_held_out_execution,
            "V2R13_HELD_OUT_EXECUTION_NOT_AUTHORIZED",
        ),
        (
            disposition.replay_candidate,
            "V2R13_PAIR09_CANDIDATE_REPLAY_NOT_AUTHORIZED",
        ),
        (
            disposition.promote_or_train_candidate,
            "V2R13_CANDIDATE_PROMOTION_AND_TRAINING_NOT_AUTHORIZED",
        ),
    ):
        with pytest.raises(
            disposition.V2R13Pair09CandidatePolicyDispositionHold,
            match=message,
        ):
            fn()
