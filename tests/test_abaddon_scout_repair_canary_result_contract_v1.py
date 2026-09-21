from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_canary_opponent_source_binding_review_v1 as opponent_review
from openra_env.learning import abaddon_scout_repair_canary_result_contract_v1 as result_contract
from openra_env.learning import abaddon_scout_repair_canary_source_design_v1 as source_design


def run(arm, *, suffix, metrics=None):
    seed = source_design.scout_repair_canary_source_design()["seed_derivation"]["seed"]
    opponent = opponent_review.scout_repair_opponent_source_binding_review()["opponent"]["source_identity"]
    base_metrics = {
        "scout_missions_issued": 2,
        "scout_missions_completed": 1,
        "scout_missions_failed": 0,
        "scout_missions_interrupted": 1,
        "unique_observed_scout_arrivals": 1,
        "accepted_shared_clock_noops": 10,
        "idle_combat_units_during_noops": 8,
        "explored_percent": 15.0,
        "contact_response_actions": 2,
        "units_killed": 3,
        "units_lost": 2,
        "kills_cost": 300,
        "deaths_cost": 200,
        "command_rejections": 0,
    }
    if metrics:
        base_metrics.update(metrics)
    return {
        "schema": result_contract.RUN_SCHEMA,
        "experiment_namespace": source_design.NAMESPACE,
        "arm": arm,
        "run_id": f"scout-canary-{arm}-{suffix}",
        "seed": seed,
        "opponent_source_sha256": opponent["sha256"],
        "opponent_model_backed": False,
        "controller_rows_training_candidate": False,
        "automatic_corpus_admission": False,
        "automatic_policy_promotion": False,
        "outcome": "DRAW_OR_UNFINISHED",
        "rounds_completed": 36,
        "ticks_per_round": 25,
        "warm_start_sha256": "1" * 64,
        "trajectory_sha256": ("2" if arm == "legacy_control" else "3") * 64,
        "summary_sha256": ("4" if arm == "legacy_control" else "5") * 64,
        "runtime_image_sha256": "6" * 64,
        "engine_commit": "7" * 40,
        "war_college_commit": "8" * 40,
        "cleanup": {
            "independent_post_run_observation": True,
            "service_active": "inactive",
            "service_enabled": "disabled",
            "activation_permit_present": False,
            "stale_container_count": 0,
            "source_and_baseline_preserved": True,
        },
        "metrics": base_metrics,
    }


def test_valid_run_requires_independent_cleanup_and_nontraining_boundaries():
    out = result_contract.validate_canary_run_result(run("legacy_control", suffix="a"))
    assert out["cleanup"]["independent_post_run_observation"] is True
    assert out["controller_rows_training_candidate"] is False
    assert out["opponent_model_backed"] is False


def test_descriptive_comparison_has_deltas_but_never_a_winner_or_authority():
    control = run("legacy_control", suffix="a")
    treatment = run("scout_repair_treatment", suffix="b", metrics={
        "unique_observed_scout_arrivals": 2,
        "scout_missions_completed": 2,
        "accepted_shared_clock_noops": 3,
        "idle_combat_units_during_noops": 1,
        "explored_percent": 20.5,
    })
    out = result_contract.compare_canary_results(control, treatment)
    d = out["metric_deltas_treatment_minus_control"]
    assert d["unique_observed_scout_arrivals"] == 1
    assert d["accepted_shared_clock_noops"] == -7
    assert d["idle_combat_units_during_noops"] == -7
    assert d["explored_percent"] == 5.5
    assert out["descriptive_comparison_complete"] is True
    assert out["general_performance_superiority_established"] is False
    assert out["causal_generalization_established"] is False
    assert out["automatic_retry_authorized"] is False
    assert out["automatic_policy_promotion_authorized"] is False
    assert out["additional_game_execution_authorized"] is False


def test_canonical_seed_and_opponent_drift_reject_before_pair_comparison():
    control = run("legacy_control", suffix="a")
    treatment = run("scout_repair_treatment", suffix="b")
    changed = deepcopy(treatment)
    changed["seed"] += 1
    with pytest.raises(result_contract.ScoutRepairCanaryResultHold, match="seed_drift"):
        result_contract.compare_canary_results(control, changed)
    changed = deepcopy(treatment)
    changed["opponent_source_sha256"] = "f" * 64
    with pytest.raises(result_contract.ScoutRepairCanaryResultHold, match="opponent_identity_drift"):
        result_contract.compare_canary_results(control, changed)


def test_pair_identity_mismatch_rejects_after_individual_run_validation():
    control = run("legacy_control", suffix="a")
    treatment = run("scout_repair_treatment", suffix="b")
    for field, value in (
        ("warm_start_sha256", "a" * 64),
        ("runtime_image_sha256", "b" * 64),
        ("engine_commit", "c" * 40),
        ("war_college_commit", "d" * 40),
        ("ticks_per_round", 50),
    ):
        changed = deepcopy(treatment)
        changed[field] = value
        with pytest.raises(result_contract.ScoutRepairCanaryResultHold, match="pair_binding_drift"):
            result_contract.compare_canary_results(control, changed)


def test_bad_cleanup_or_training_or_model_backing_rejects():
    base = run("legacy_control", suffix="a")
    changes = [
        ("controller_rows_training_candidate", True),
        ("opponent_model_backed", True),
        ("automatic_corpus_admission", True),
        ("automatic_policy_promotion", True),
    ]
    for field, value in changes:
        changed = deepcopy(base); changed[field] = value
        with pytest.raises(result_contract.ScoutRepairCanaryResultHold):
            result_contract.validate_canary_run_result(changed)
    for field, value in (
        ("independent_post_run_observation", False),
        ("service_active", "active"),
        ("service_enabled", "enabled"),
        ("activation_permit_present", True),
        ("stale_container_count", 1),
        ("source_and_baseline_preserved", False),
    ):
        changed = deepcopy(base); changed["cleanup"][field] = value
        with pytest.raises(result_contract.ScoutRepairCanaryResultHold):
            result_contract.validate_canary_run_result(changed)


def test_metric_consistency_rejects_impossible_counts():
    changed = run("legacy_control", suffix="a", metrics={"scout_missions_issued": 1, "scout_missions_completed": 2})
    with pytest.raises(result_contract.ScoutRepairCanaryResultHold, match="completed_exceeds_issued"):
        result_contract.validate_canary_run_result(changed)
    changed = run("legacy_control", suffix="a", metrics={"scout_missions_completed": 1, "unique_observed_scout_arrivals": 2})
    with pytest.raises(result_contract.ScoutRepairCanaryResultHold, match="unique_arrivals_exceed_completed"):
        result_contract.validate_canary_run_result(changed)


def test_public_validation_returns_copy():
    original = run("legacy_control", suffix="a")
    out = result_contract.validate_canary_run_result(original)
    out["metrics"]["command_rejections"] = 99
    assert original["metrics"]["command_rejections"] == 0


def test_more_execution_or_promotion_entrypoint_always_holds():
    with pytest.raises(result_contract.ScoutRepairCanaryResultHold, match=result_contract.NEXT_GATE):
        result_contract.authorize_promote_or_execute_more(authorized=True)


def test_source_only_import_surface():
    tree = ast.parse(Path(result_contract.__file__).read_text(encoding="utf-8"))
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.add(node.module)
    assert modules == {"__future__", "copy", "typing", "openra_env.learning"}
