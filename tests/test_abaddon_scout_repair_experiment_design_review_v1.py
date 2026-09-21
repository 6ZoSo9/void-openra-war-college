from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_repair_experiment_design_review_v1 as review


def test_review_selects_fresh_two_arm_canary_outside_generation2_campaign():
    out = review.scout_repair_experiment_design_review()
    assert out["experiment_namespace"] == "abaddon-scout-repair-canary-v1"
    assert out["stage"] == "initial_causal_canary"
    assert out["arm_count"] == 2
    assert out["generation2_candidate_campaign_slot_reused"] is False
    assert out["pair03_attempt_or_result_reused"] is False
    assert out["held_out_campaign_space_used"] is False
    assert [arm["arm"] for arm in out["arms"]] == ["legacy_control", "scout_repair_treatment"]
    assert all(arm["candidate252_policy_mutations_included"] is False for arm in out["arms"])
    assert out["arms"][0]["scout_mission_lifecycle_enabled"] is False
    assert out["arms"][1]["scout_mission_lifecycle_enabled"] is True


def test_initial_canary_requires_same_pair_inputs_and_deterministic_opponent():
    out = review.scout_repair_experiment_design_review()
    assert all(out["pair_binding_requirements"].values())
    opponent = out["opponent_requirements"]
    assert opponent["initial_canary_model_backed_opponent_allowed"] is False
    assert opponent["deterministic_source_bound_opponent_required"] is True
    assert opponent["specific_opponent_selected"] is False
    assert opponent["later_model_backed_validation_is_separate_gate"] is True
    assert "pair03_first_action_divergence" in opponent["reason"]


def test_initial_canary_runner_cannot_inherit_model_or_training_labels():
    out = review.scout_repair_experiment_design_review()
    requirements = out["runner_requirements"]
    assert requirements == {
        "scripted_warm_start_reused": True,
        "unchanged_host_validator_reused": True,
        "unchanged_joint_advance_reused": True,
        "model_service_start_allowed": False,
        "model_inference_allowed": False,
        "explicit_deterministic_opponent_identity_required": True,
        "historical_actual_apollyon_label_accepted": False,
        "controller_rows_training_candidate": False,
        "warm_start_rows_training_candidate": False,
        "automatic_corpus_admission": False,
        "canary_result_schema_must_be_distinct_from_pair03": True,
    }


def test_canary_is_exactly_one_pair_without_automatic_retry_or_promotion():
    out = review.scout_repair_experiment_design_review()
    limits = out["canary_limits"]
    assert limits == {
        "live_control_runs": 1,
        "live_treatment_runs": 1,
        "maximum_total_game_runs": 2,
        "maximum_automatic_retries": 0,
        "retry_after_consumption_requires_new_explicit_review": True,
        "automatic_training": False,
        "automatic_policy_promotion": False,
    }


def test_evidence_and_causal_limits_remain_explicit():
    out = review.scout_repair_experiment_design_review()
    evidence = set(out["evidence_to_compare"])
    for key in (
        "observed_scout_missions_issued_completed_failed_interrupted",
        "unique_observed_scout_arrivals",
        "accepted_shared_clock_noop_decisions",
        "idle_combat_capable_units_during_noop",
        "command_rejections",
        "runtime_cleanup_and_post_run_dormancy",
    ):
        assert key in evidence
    assert all(value is False for value in out["causal_claim_limits"].values())


def test_operational_inputs_and_all_authority_remain_unresolved():
    out = review.scout_repair_experiment_design_review()
    assert all(value is None for value in out["unresolved"].values())
    assert all(value is False for value in out["authority"].values())
    assert out["execution_authorized"] is False
    assert out["execution_performed"] is False
    assert out["next_gate"] == review.NEXT_GATE


def test_public_results_are_independent():
    first = review.scout_repair_experiment_design_review()
    first["arms"][0]["candidate252_policy_mutations_included"] = True
    first["unresolved"]["fresh_seed"] = 1
    first["authority"]["scout_repair_execution_authorized"] = True
    later = review.scout_repair_experiment_design_review()
    assert later["arms"][0]["candidate252_policy_mutations_included"] is False
    assert later["unresolved"]["fresh_seed"] is None
    assert later["authority"]["scout_repair_execution_authorized"] is False


def test_execution_entrypoint_always_holds():
    for kwargs in ({}, {"authorized": True}, {"seed": 1}, {"confirm": "yes"}):
        with pytest.raises(review.ScoutRepairExperimentDesignHold, match=review.NEXT_GATE):
            review.authorize_or_execute_canary(**kwargs)


def test_source_only_import_surface():
    tree = ast.parse(Path(review.__file__).read_text(encoding="utf-8"))
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.add(node.module)
    assert modules == {
        "__future__", "copy", "typing",
        "openra_env.learning",
    }
