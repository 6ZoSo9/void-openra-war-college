"""Pure result contract for a future two-arm scout-repair canary.

No files, runtime, model, engine, service, or attempt state are touched. This
module validates caller-supplied completed-run receipts and returns descriptive
paired deltas only. It never selects a winner, recommends promotion, authorizes
another run, or treats callback cleanup as verified dormancy.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import abaddon_scout_canary_opponent_source_binding_review_v1 as opponent_review
from openra_env.learning import abaddon_scout_repair_canary_source_design_v1 as source_design

RUN_SCHEMA = "void.abaddon.scout-repair-canary-run-result.v1"
COMPARISON_SCHEMA = "void.abaddon.scout-repair-canary-paired-review-input.v1"
NEXT_GATE = "SCOUT_REPAIR_HUMAN_CANARY_EVIDENCE_REVIEW_REQUIRED"
ARMS = ("legacy_control", "scout_repair_treatment")
OUTCOMES = ("APOLLYON_WIN", "ABADDON_WIN", "DRAW_OR_UNFINISHED")
HEX = frozenset("0123456789abcdef")


class ScoutRepairCanaryResultHold(ValueError):
    pass


def _require(value: bool, reason: str) -> None:
    if not value:
        raise ScoutRepairCanaryResultHold(reason)


def _sha(value: Any, name: str, length: int = 64) -> str:
    _require(type(value) is str and len(value) == length and set(value) <= HEX, name + "_invalid")
    return value


def _integer(value: Any, name: str, low: int = 0, high: int = 2**53 - 1) -> int:
    _require(type(value) is int and low <= value <= high, name + "_invalid")
    return value


def _number(value: Any, name: str, low: float | None = None) -> float:
    _require(type(value) in (int, float), name + "_invalid")
    out = float(value)
    _require(out == out and out not in (float("inf"), float("-inf")), name + "_nonfinite")
    if low is not None:
        _require(out >= low, name + "_below_minimum")
    return out


def validate_canary_run_result(result: Mapping[str, Any]) -> dict[str, Any]:
    _require(type(result) is dict, "run_result_object_required")
    out = deepcopy(result)
    _require(out.get("schema") == RUN_SCHEMA, "run_schema_drift")
    arm = out.get("arm")
    _require(arm in ARMS, "arm_invalid")
    _require(out.get("experiment_namespace") == source_design.NAMESPACE, "namespace_drift")
    seed = source_design.scout_repair_canary_source_design()["seed_derivation"]["seed"]
    _require(out.get("seed") == seed, "seed_drift")
    opponent = opponent_review.scout_repair_opponent_source_binding_review()["opponent"]["source_identity"]
    _require(out.get("opponent_source_sha256") == opponent["sha256"], "opponent_identity_drift")
    _require(out.get("opponent_model_backed") is False, "model_backed_opponent_forbidden")
    _require(out.get("controller_rows_training_candidate") is False, "canary_training_rows_forbidden")
    _require(out.get("automatic_corpus_admission") is False, "automatic_corpus_admission_forbidden")
    _require(out.get("automatic_policy_promotion") is False, "automatic_promotion_forbidden")
    run_id = out.get("run_id")
    _require(type(run_id) is str and 0 < len(run_id) <= 160 and all(c.isalnum() or c in "-_." for c in run_id),
             "run_id_invalid")
    _require(out.get("outcome") in OUTCOMES, "outcome_invalid")
    _integer(out.get("rounds_completed"), "rounds_completed", 0, 200)
    _integer(out.get("ticks_per_round"), "ticks_per_round", 1, 100)
    for field in ("warm_start_sha256", "trajectory_sha256", "summary_sha256", "runtime_image_sha256"):
        _sha(out.get(field), field)
    for field in ("engine_commit", "war_college_commit"):
        _sha(out.get(field), field, 40)
    cleanup = out.get("cleanup")
    _require(type(cleanup) is dict, "cleanup_object_required")
    _require(cleanup.get("independent_post_run_observation") is True, "independent_cleanup_observation_required")
    _require(cleanup.get("service_active") == "inactive", "service_not_inactive")
    _require(cleanup.get("service_enabled") == "disabled", "service_not_disabled")
    _require(cleanup.get("activation_permit_present") is False, "activation_permit_present")
    _require(cleanup.get("stale_container_count") == 0, "stale_container_present")
    _require(cleanup.get("source_and_baseline_preserved") is True, "source_or_baseline_changed")
    metrics = out.get("metrics")
    _require(type(metrics) is dict, "metrics_object_required")
    for field in (
        "scout_missions_issued", "scout_missions_completed", "scout_missions_failed",
        "scout_missions_interrupted", "unique_observed_scout_arrivals", "accepted_shared_clock_noops",
        "idle_combat_units_during_noops", "contact_response_actions", "units_killed", "units_lost",
        "kills_cost", "deaths_cost", "command_rejections",
    ):
        _integer(metrics.get(field), field, 0)
    _number(metrics.get("explored_percent"), "explored_percent", 0)
    _require(metrics["scout_missions_completed"] <= metrics["scout_missions_issued"], "completed_exceeds_issued")
    _require(metrics["unique_observed_scout_arrivals"] <= metrics["scout_missions_completed"],
             "unique_arrivals_exceed_completed")
    return out


def compare_canary_results(control: Mapping[str, Any], treatment: Mapping[str, Any]) -> dict[str, Any]:
    control = validate_canary_run_result(control)
    treatment = validate_canary_run_result(treatment)
    _require(control["arm"] == "legacy_control" and treatment["arm"] == "scout_repair_treatment",
             "arm_order_or_identity_invalid")
    for field in (
        "experiment_namespace", "seed", "opponent_source_sha256", "opponent_model_backed",
        "warm_start_sha256", "runtime_image_sha256", "engine_commit", "war_college_commit",
        "ticks_per_round",
    ):
        _require(control[field] == treatment[field], "pair_binding_drift:" + field)
    c, t = control["metrics"], treatment["metrics"]
    delta_fields = (
        "scout_missions_issued", "scout_missions_completed", "scout_missions_failed",
        "scout_missions_interrupted", "unique_observed_scout_arrivals", "accepted_shared_clock_noops",
        "idle_combat_units_during_noops", "explored_percent", "contact_response_actions",
        "units_killed", "units_lost", "kills_cost", "deaths_cost", "command_rejections",
    )
    return {
        "schema": COMPARISON_SCHEMA,
        "experiment_namespace": control["experiment_namespace"],
        "seed": control["seed"],
        "control_run_id": control["run_id"],
        "treatment_run_id": treatment["run_id"],
        "control_outcome": control["outcome"],
        "treatment_outcome": treatment["outcome"],
        "control_rounds_completed": control["rounds_completed"],
        "treatment_rounds_completed": treatment["rounds_completed"],
        "metric_deltas_treatment_minus_control": {field: t[field] - c[field] for field in delta_fields},
        "descriptive_comparison_complete": True,
        "general_performance_superiority_established": False,
        "causal_generalization_established": False,
        "automatic_retry_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "additional_game_execution_authorized": False,
        "next_gate": NEXT_GATE,
    }


def authorize_promote_or_execute_more(*args: Any, **kwargs: Any) -> None:
    raise ScoutRepairCanaryResultHold(NEXT_GATE)
