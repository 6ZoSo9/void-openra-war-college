from copy import deepcopy

import pytest

from openra_env.learning import abaddon_scout_repair_canary_runner_requirements_v1 as subject


def test_contract_is_fresh_two_arm_non_model_canary():
    row = subject.scout_repair_canary_runner_requirements()
    assert row["arms"] == ("legacy_control", "scout_repair_treatment")
    assert row["control"]["scout_lifecycle_repair_enabled"] is False
    assert row["treatment"]["scout_lifecycle_repair_enabled"] is True
    assert row["control"]["candidate252_mutations_included"] is False
    assert row["treatment"]["candidate252_mutations_included"] is False
    assert row["opponent_execution_contract"]["model_service_start_forbidden"] is True
    assert row["opponent_execution_contract"]["model_inference_forbidden"] is True
    assert row["execution_authorized"] is False


def test_attempt_budget_is_exactly_one_each_and_no_retry():
    row = subject.scout_repair_canary_runner_requirements()["attempt_contract"]
    assert row == {
        "control_attempts": 1,
        "treatment_attempts": 1,
        "maximum_total_game_runs": 2,
        "automatic_retries": 0,
        "separate_create_only_arm_markers_required": True,
        "shared_marker_between_arms_allowed": False,
        "pair03_marker_reuse_allowed": False,
        "uncertain_or_consumed_arm_may_rerun_without_new_review": False,
    }


def _good_claim():
    row = subject.scout_repair_canary_runner_requirements()
    return {
        "schema": "void.abaddon.scout-repair-canary-runner-implementation-review.v1",
        "experiment_namespace": row["experiment_namespace"],
        "seed": row["seed"],
        "opponent_source_sha256": row["opponent_source_identity"]["sha256"],
        "model_service_start_implemented": False,
        "model_inference_implemented": False,
        "automatic_retry_implemented": False,
        "training_admission_implemented": False,
        "automatic_policy_promotion_implemented": False,
        "execution_authority_created": False,
        "typed_current_turn_tool_contract_used": True,
        "unchanged_host_validator_used": True,
        "deterministic_opponent_identity_logged": True,
        "controller_rows_nontraining": True,
        "separate_arm_attempt_markers_designed": True,
        "independent_post_run_observation_required": True,
    }


def test_source_review_claim_can_validate_without_granting_execution():
    out = subject.validate_runner_implementation_claim(_good_claim())
    assert out["source_review_claim_valid"] is True
    assert out["execution_authorized"] is False


@pytest.mark.parametrize("field", [
    "model_service_start_implemented", "model_inference_implemented",
    "automatic_retry_implemented", "training_admission_implemented",
    "automatic_policy_promotion_implemented", "execution_authority_created",
])
def test_forbidden_capability_claims_hold(field):
    row = _good_claim(); row[field] = True
    with pytest.raises(subject.ScoutRepairCanaryRunnerRequirementsHold):
        subject.validate_runner_implementation_claim(row)


@pytest.mark.parametrize("field", [
    "typed_current_turn_tool_contract_used", "unchanged_host_validator_used",
    "deterministic_opponent_identity_logged", "controller_rows_nontraining",
    "separate_arm_attempt_markers_designed", "independent_post_run_observation_required",
])
def test_missing_required_source_property_holds(field):
    row = _good_claim(); row[field] = False
    with pytest.raises(subject.ScoutRepairCanaryRunnerRequirementsHold):
        subject.validate_runner_implementation_claim(row)


def test_seed_and_opponent_are_source_bound():
    base = _good_claim()
    for field, replacement in (("seed", base["seed"] + 1), ("opponent_source_sha256", "0" * 64)):
        row = deepcopy(base); row[field] = replacement
        with pytest.raises(subject.ScoutRepairCanaryRunnerRequirementsHold):
            subject.validate_runner_implementation_claim(row)


def test_authorize_entrypoint_always_holds():
    with pytest.raises(subject.ScoutRepairCanaryRunnerRequirementsHold):
        subject.authorize_or_execute()
