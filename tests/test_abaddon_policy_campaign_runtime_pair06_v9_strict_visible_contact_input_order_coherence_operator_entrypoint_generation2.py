from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_operator_entrypoint_generation2
    as invocation,
)


def _kwargs() -> dict:
    return {
        "expected_main_head": "a" * 40,
        "expected_operator_source_sha256": "b" * 64,
        "execution_authorization_accepted": True,
        "policy_activation_authorization_accepted": True,
        "order_coherence_activation_authorization_accepted": True,
        "execution_confirm": invocation.EXECUTION_CONFIRM_TOKEN,
        "policy_confirm": invocation.POLICY_CONFIRM_TOKEN,
        "order_confirm": invocation.ORDER_CONFIRM_TOKEN,
    }


def test_contract_is_one_shot_order_coherence_operator_lane():
    out = invocation.pair06_v9_input_order_coherence_operator_contract()

    assert out["pair06_v9_input_order_coherence_operator_entrypoint_implemented"] is True
    assert out["pair06_v9_input_order_coherence_operator_entrypoint_reviewed"] is False
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["policy_id"] == "pair06-v9-strict-visible-contact-envelope-v1"
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0


def test_order_evidence_namespace_is_fresh_and_historical_v9_nonreusable():
    out = invocation.pair06_v9_input_order_coherence_operator_contract()

    assert out["v9_evidence_namespace_distinct_from_v8"] is True
    assert out["order_evidence_namespace_distinct_from_historical_v9"] is True
    assert out["historical_v9_attempt_reusable"] is False
    assert out["historical_v9_authorization_reusable"] is False
    assert "input-order-coherence" in out["order_runs_root"]
    assert "input-order-coherence" in out["order_marker_name"]
    assert "input-order-coherence" in out["order_result_name"]
    assert "input-order-coherence" in out["order_closeout_name"]


def test_contract_preserves_preclaim_gpu_and_durable_claim_ordering():
    out = invocation.pair06_v9_input_order_coherence_operator_contract()

    assert out["fresh_preclaim_gpu_observation_implemented"] is True
    assert out["fresh_preclaim_gpu_admission_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    assert out["durable_create_only_attempt_marker_implemented"] is True
    assert out["attempt_marker_precedes_model_load_and_child_spawn"] is True
    assert out["marker_sha256_is_attempt_id"] is True
    assert out["authority_rechecked_after_claim"] is True
    assert out["authority_rechecked_before_each_inference_by_parent"] is True


def test_three_authorization_and_confirmation_gates_are_distinct():
    out = invocation.pair06_v9_input_order_coherence_operator_contract()

    assert out["explicit_execution_authorization_boolean_required"] is True
    assert out["explicit_policy_activation_authorization_boolean_required"] is True
    assert out["explicit_order_coherence_activation_authorization_boolean_required"] is True
    assert out["explicit_execution_confirmation_token_required"] is True
    assert out["explicit_policy_confirmation_token_required"] is True
    assert out["explicit_order_coherence_confirmation_token_required"] is True
    assert out["all_confirmation_tokens_distinct"] is True
    assert len(
        {
            invocation.EXECUTION_CONFIRM_TOKEN,
            invocation.POLICY_CONFIRM_TOKEN,
            invocation.ORDER_CONFIRM_TOKEN,
        }
    ) == 3


@pytest.mark.parametrize(
    ("field", "message"),
    (
        ("execution_authorization_accepted", "EXECUTION_AUTHORIZATION_REQUIRED"),
        ("policy_activation_authorization_accepted", "POLICY_ACTIVATION_AUTHORIZATION_REQUIRED"),
        (
            "order_coherence_activation_authorization_accepted",
            "COHERENCE_ACTIVATION_AUTHORIZATION_REQUIRED",
        ),
    ),
)
def test_authorization_holds_precede_host_io(field, message):
    kwargs = _kwargs()
    kwargs[field] = False

    with pytest.raises(
        invocation.Pair06V9InputOrderCoherenceOperatorHold,
        match=message,
    ):
        invocation.execute_pair06_v9_input_order_coherence_baseline_game(**kwargs)


@pytest.mark.parametrize(
    ("field", "message"),
    (
        ("execution_confirm", "EXECUTION_CONFIRMATION_REQUIRED"),
        ("policy_confirm", "POLICY_CONFIRMATION_REQUIRED"),
        ("order_confirm", "COHERENCE_CONFIRMATION_REQUIRED"),
    ),
)
def test_wrong_confirmation_holds_before_host_io(field, message):
    kwargs = _kwargs()
    kwargs[field] = "wrong"

    with pytest.raises(
        invocation.Pair06V9InputOrderCoherenceOperatorHold,
        match=message,
    ):
        invocation.execute_pair06_v9_input_order_coherence_baseline_game(**kwargs)


@pytest.mark.parametrize(
    "field",
    (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "attempt_consumed",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "game_execution_performed",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "host_io_performed_by_contract_inspection",
    ),
)
def test_contract_grants_no_runtime_or_follow_on_authority(field):
    out = invocation.pair06_v9_input_order_coherence_operator_contract()
    assert out[field] is False


def test_operator_advances_only_to_source_review():
    out = invocation.pair06_v9_input_order_coherence_operator_contract()

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "OPERATOR_ENTRYPOINT_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "OPERATOR_ENTRYPOINT_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_authorize_or_execute_holds():
    with pytest.raises(
        invocation.Pair06V9InputOrderCoherenceOperatorHold,
        match="OPERATOR_ENTRYPOINT_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        invocation.authorize_or_execute()
