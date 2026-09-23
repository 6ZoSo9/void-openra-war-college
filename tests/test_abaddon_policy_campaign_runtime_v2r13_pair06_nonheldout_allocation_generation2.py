from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair06_nonheldout_allocation_generation2
    as allocation,
)


def test_allocation_selects_pair06_by_deterministic_rule():
    out = allocation.v2r13_pair06_nonheldout_allocation_contract()
    assert out["new_nonheldout_allocation_selected"] is True
    assert out["selection_rule"] == (
        "lowest_unused_nonheldout_historical_control_pair_slot"
    )
    assert out["completed_nonheldout_pair_slots"] == (3, 9)
    assert out["eligible_unused_historical_control_pair_slots"] == (6, 12)
    assert out["selected_pair_slot"] == 6
    assert out["selected_held_out"] is False


def test_pair06_canonical_binding_is_exact():
    out = allocation.v2r13_pair06_nonheldout_allocation_contract()
    assert out["selected_seed"] == 208354846
    assert out["selected_rounds"] == 36
    assert out["selected_ticks_per_round"] == 25
    assert out["selected_starter_infantry"] == 4
    assert out["selected_staging_max_ticks"] == 800
    assert out["selected_opponent_role"] == "prior_accepted_model_control"
    assert out["selected_opponent_snapshot_id"] == (
        "apollyon-v3-v8-accepted-model-control"
    )
    assert out["selected_opponent_snapshot_sha256"] == (
        "5c51082219530a302ce25b28daba9928f56a436c11d1508ca0bef755f4a86667"
    )


def test_pair06_baseline_and_candidate_are_matched_and_inert():
    out = allocation.v2r13_pair06_nonheldout_allocation_contract()
    baseline = out["baseline_command"]
    candidate = out["candidate_command"]
    assert out["matched_baseline_candidate_required"] is True
    assert tuple(baseline["runner_argv"]) == tuple(candidate["runner_argv"])
    assert baseline["pair_slot"] == 6
    assert candidate["pair_slot"] == 6
    assert baseline["arm"] == "baseline"
    assert candidate["arm"] == "candidate"
    assert baseline["runtime_selection_key"] == (
        "apollyon-v3-v8-accepted-model-control"
    )
    assert candidate["runtime_selection_key"] == (
        "apollyon-v3-v8-accepted-model-control"
    )
    for command in (baseline, candidate):
        assert command["runtime_execution_authorized"] is False
        assert command["runtime_started"] is False
        assert command["command_execution_performed"] is False
        assert command["model_inference_performed"] is False
        assert command["game_execution_performed"] is False
        assert command["training_performed"] is False
        assert command["weights_updated"] is False


def test_pair06_requires_bounded_executor_extension():
    out = allocation.v2r13_pair06_nonheldout_allocation_contract()
    assert out["bounded_executor_current_pair_slots"] == (3, 9, 15)
    assert out["bounded_executor_current_held_out_pair_slots"] == (15,)
    assert out["bounded_executor_extension_required"] is True
    assert out["pair06_runtime_execution_authorized"] is False
    assert out["pair06_runtime_execution_performed"] is False


def test_pair15_and_existing_pair_replays_remain_closed():
    out = allocation.v2r13_pair06_nonheldout_allocation_contract()
    assert out["pair15_execution_authorized"] is False
    assert out["pair15_execution_performed"] is False
    assert out["pair03_replay_authorized"] is False
    assert out["pair09_replay_authorized"] is False


def test_allocation_grants_no_training_promotion_or_external_authority():
    out = allocation.v2r13_pair06_nonheldout_allocation_contract()
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_allocation_frontier_is_capability_extension():
    out = allocation.v2r13_pair06_nonheldout_allocation_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR06_BOUNDED_CAPABILITY_EXTENSION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR06_BOUNDED_CAPABILITY_EXTENSION_REQUIRED"
    )


def test_prohibited_action_entrypoints_hold():
    for fn, message in (
        (
            allocation.execute_pair06,
            "V2R13_PAIR06_RUNTIME_EXECUTION_NOT_AUTHORIZED",
        ),
        (
            allocation.execute_pair15,
            "V2R13_PAIR15_HELD_OUT_EXECUTION_NOT_AUTHORIZED",
        ),
        (
            allocation.promote_or_train_candidate,
            "V2R13_CANDIDATE_PROMOTION_AND_TRAINING_NOT_AUTHORIZED",
        ),
    ):
        with pytest.raises(
            allocation.V2R13Pair06NonheldoutAllocationHold,
            match=message,
        ):
            fn()
