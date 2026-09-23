from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_post_pair09_evaluation_design_generation2
    as design,
)


def test_design_binds_pair03_pair09_dispositions_and_executor():
    out = design.v2r13_post_pair09_evaluation_design_contract()
    assert out["pair03_disposition_review_git_blob"] == (
        "ff606911ce35499b0fd6d25eb10591fc80b0c338"
    )
    assert out["pair09_disposition_review_git_blob"] == (
        "21e87f2d594544886610cff2b5596c325a743494"
    )
    assert out["bounded_executor_git_blob"] == (
        "c7e20c1157e0bcf7f65036631aad47fb82c7aefd"
    )


def test_existing_nonheldout_v2r13_capacity_is_exhausted():
    out = design.v2r13_post_pair09_evaluation_design_contract()
    assert out["post_pair09_evaluation_design_implemented"] is True
    assert out["post_pair09_evaluation_design_reviewed"] is False
    assert out["authorized_pair_slots"] == (3, 9, 15)
    assert out["held_out_pair_slots"] == (15,)
    assert out["nonheldout_pair_slots"] == (3, 9)
    assert out["completed_nondecisive_nonheldout_pair_slots"] == (3, 9)
    assert out["existing_nonheldout_capacity_exhausted"] is True


def test_pair15_heldout_is_preserved_from_tuning_use():
    out = design.v2r13_post_pair09_evaluation_design_contract()
    assert out["held_out_pair15_preserved"] is True
    assert out["held_out_contamination_prohibited"] is True
    assert out["held_out_use_as_tuning_tiebreaker_allowed"] is False
    assert out["pair15_execution_authorized"] is False
    assert out["pair15_execution_performed"] is False


def test_new_nonheldout_allocation_is_required_but_not_authorized():
    out = design.v2r13_post_pair09_evaluation_design_contract()
    assert out["new_nonheldout_evaluation_allocation_required"] is True
    assert out["new_nonheldout_execution_authorized"] is False
    assert out["pair03_replay_authorized"] is False
    assert out["pair09_replay_authorized"] is False
    assert out["candidate_promoted"] is False
    assert out["candidate_rejected"] is False


def test_design_grants_no_training_promotion_or_external_authority():
    out = design.v2r13_post_pair09_evaluation_design_contract()
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_design_advances_only_to_new_nonheldout_allocation():
    out = design.v2r13_post_pair09_evaluation_design_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_NEW_NONHELDOUT_EVALUATION_ALLOCATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_NEW_NONHELDOUT_EVALUATION_ALLOCATION_REQUIRED"
    )


def test_prohibited_execution_entrypoints_hold():
    for fn, message in (
        (
            design.execute_pair15,
            "V2R13_PAIR15_HELD_OUT_EXECUTION_NOT_AUTHORIZED",
        ),
        (
            design.replay_existing_pair,
            "V2R13_EXISTING_PAIR_REPLAY_NOT_AUTHORIZED",
        ),
        (
            design.promote_or_train_candidate,
            "V2R13_CANDIDATE_PROMOTION_AND_TRAINING_NOT_AUTHORIZED",
        ),
    ):
        with pytest.raises(
            design.V2R13PostPair09EvaluationDesignHold,
            match=message,
        ):
            fn()
