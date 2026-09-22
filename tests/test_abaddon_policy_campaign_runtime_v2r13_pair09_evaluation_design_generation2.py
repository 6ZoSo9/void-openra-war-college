from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_evaluation_design_generation2
    as design,
)


def test_pair09_design_pins_exact_upstream_disposition_and_capabilities():
    out = design.v2r13_pair09_evaluation_design_contract()
    assert out["disposition_review_git_blob"] == (
        "ff606911ce35499b0fd6d25eb10591fc80b0c338"
    )
    assert out["disposition_review_source_sha256"] == (
        "ab7fbc0be7b6f4a960d2a7f75f1ceeb6e111c6737a546e672098c74bb8c33fb9"
    )
    assert out["command_materializer_git_blob"] == (
        "4836360e0d284454f815a2a2e32078d2565e6dea"
    )
    assert out["bounded_executor_git_blob"] == (
        "c7e20c1157e0bcf7f65036631aad47fb82c7aefd"
    )


def test_pair09_is_nonheld_matched_baseline_candidate_design():
    out = design.v2r13_pair09_evaluation_design_contract()
    assert out["pair09_evaluation_design_implemented"] is True
    assert out["pair09_evaluation_design_reviewed"] is False
    assert out["pair_slot"] == 9
    assert out["arms"] == ("baseline", "candidate")
    assert out["held_out"] is False
    assert out["baseline_first"] is True
    assert out["baseline_must_complete_before_candidate"] is True
    assert out["matched_pair_runner_argv_required"] is True
    assert tuple(out["baseline_command"]["runner_argv"]) == tuple(
        out["candidate_command"]["runner_argv"]
    )
    assert tuple(out["matched_pair_runner_argv"]) == tuple(
        out["baseline_command"]["runner_argv"]
    )


@pytest.mark.parametrize("arm", ["baseline", "candidate"])
def test_pair09_commands_remain_source_only_and_nonexecuting(arm):
    command = design.v2r13_pair09_evaluation_design_contract()[f"{arm}_command"]
    assert command["pair_slot"] == 9
    assert command["arm"] == arm
    assert command["workdir_token"] == f"generation2/pair-09/{arm}"
    assert command["runtime_selection_key"] == "apollyon-v2r13-qualified-predecessor"
    assert command["argv_materialized"] is True
    assert command["path_bindings_resolved"] is False
    assert command["process_spawn_implemented"] is False
    assert command["command_execution_performed"] is False
    assert command["workdir_materialized"] is False
    assert command["workdir_created"] is False
    assert command["runtime_execution_authorized"] is False
    assert command["runtime_started"] is False
    assert command["model_inference_performed"] is False
    assert command["game_execution_performed"] is False
    assert command["training_performed"] is False
    assert command["weights_updated"] is False


def test_legacy_broad_capability_is_not_pair09_policy_authority():
    out = design.v2r13_pair09_evaluation_design_contract()
    assert out["historical_bounded_executor_capability_reusable"] is True
    assert out["legacy_six_arm_authorization_sufficient_for_pair09"] is False
    assert out["pair09_baseline_execution_authorized"] is False
    assert out["pair09_candidate_execution_authorized"] is False
    assert out["pair09_execution_performed"] is False


def test_pair03_candidate_is_preserved_without_promotion_or_rejection():
    out = design.v2r13_pair09_evaluation_design_contract()
    assert out["candidate_policy_preserved_from_pair03"] is True
    assert out["candidate_policy_promoted"] is False
    assert out["candidate_policy_rejected"] is False
    assert out["candidate_replay_permitted"] is False


def test_pair09_design_grants_no_heldout_training_promotion_or_external_authority():
    out = design.v2r13_pair09_evaluation_design_contract()
    assert out["held_out_execution_authorized"] is False
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_pair09_design_requires_separate_source_binding_review():
    out = design.v2r13_pair09_evaluation_design_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR09_EVALUATION_DESIGN_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR09_EVALUATION_DESIGN_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_all_execution_entrypoints_hold():
    with pytest.raises(
        design.V2R13Pair09EvaluationDesignHold,
        match="V2R13_PAIR09_BASELINE_EXECUTION_NOT_AUTHORIZED",
    ):
        design.execute_pair09_baseline()

    with pytest.raises(
        design.V2R13Pair09EvaluationDesignHold,
        match="V2R13_PAIR09_CANDIDATE_EXECUTION_NOT_AUTHORIZED",
    ):
        design.execute_pair09_candidate()

    with pytest.raises(
        design.V2R13Pair09EvaluationDesignHold,
        match="V2R13_HELD_OUT_EXECUTION_NOT_AUTHORIZED",
    ):
        design.execute_held_out_pair()
