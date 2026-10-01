from __future__ import annotations

import hashlib
import json

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_execution_authorization_request_generation2
    as request,
)


def test_request_contract_is_proposal_only_and_matched_scope():
    out = request.pair06_v9_input_order_execution_authorization_request_contract()

    assert out[
        "pair06_v9_input_order_execution_authorization_request_implemented"
    ] is True
    assert out["policy_id"] == "pair06-v9-strict-visible-contact-envelope-v1"
    assert out["intervention_id"] == "pair06-v9-input-order-coherence-repair-v1"
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["doctrine"] == "FEINTER"
    assert out["seed"] == 208354846
    assert out["rounds"] == 36
    assert out["ticks_per_round"] == 25
    assert out["starter_infantry"] == 4
    assert out["staging_max_ticks"] == 800
    assert out["runtime_selection_key"] == "apollyon-v3-qwen35-4b-lora-v1"
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0


def test_request_binds_reviewed_stack_without_claiming_it_is_main():
    out = request.pair06_v9_input_order_execution_authorization_request_contract()
    binding = out["request"]["source_binding"]

    assert out["reviewed_operator_stack_head"] == (
        "23dabde76ef494e741294bf7c4ed210af5ce45a9"
    )
    assert binding["reviewed_operator_stack_head"] == out[
        "reviewed_operator_stack_head"
    ]
    assert binding["canonical_main_must_be_bound_by_later_authorization"] is True
    assert out["canonical_main_must_be_bound_by_later_authorization"] is True


def test_request_bytes_are_canonical_deterministic_and_exactly_validated():
    first = request.build_pair06_v9_input_order_execution_authorization_request()
    second = request.build_pair06_v9_input_order_execution_authorization_request()

    assert first == second
    assert first.endswith(b"\n")
    parsed = json.loads(first)
    assert parsed["record_kind"] == "proposal_only_not_authorization"

    validated = request.validate_pair06_v9_input_order_execution_authorization_request(
        first
    )
    assert validated["request_bytes_valid"] is True
    assert validated["request_sha256"] == hashlib.sha256(first).hexdigest()
    assert validated["request_byte_length"] == len(first)
    assert validated["matching_request_digest_grants_authority"] is False
    assert validated["fresh_user_authorization_text_required"] is True
    assert (
        validated["general_source_work_authorization_is_execution_authorization"]
        is False
    )


def test_one_byte_request_mutation_fails_closed():
    raw = request.build_pair06_v9_input_order_execution_authorization_request()
    mutated = raw[:-2] + (b" " if raw[-2:-1] != b" " else b"x") + raw[-1:]

    with pytest.raises(
        request.Pair06V9InputOrderCoherenceAuthorizationRequestHold,
        match="request bytes differ from fixed input-order proposal",
    ):
        request.validate_pair06_v9_input_order_execution_authorization_request(
            mutated
        )


def test_controlled_comparison_is_matched_scope_without_causal_claim():
    out = request.pair06_v9_input_order_execution_authorization_request_contract()
    comparison = out["request"]["controlled_comparison"]

    assert comparison["comparator_policy_id"] == (
        "pair06-v8-combat-action-priority-envelope-v1"
    )
    assert comparison["candidate_policy_id"] == out["policy_id"]
    assert comparison["candidate_intervention_id"] == out["intervention_id"]
    for field in (
        "same_pair_slot",
        "same_arm",
        "same_doctrine",
        "same_seed",
        "same_round_budget",
        "same_tick_budget",
        "same_starter_infantry",
        "same_runtime_selection",
    ):
        assert comparison[field] is True
    assert comparison["causal_claim_made"] is False
    assert out["controlled_comparison_causal_claim_made"] is False


def test_predecessor_lineage_is_nonreusable():
    out = request.pair06_v9_input_order_execution_authorization_request_contract()
    lineage = out["request"]["lineage"]
    prior = out["dependencies"]["prior_v8_v2_success_review"]

    assert lineage["prior_v8_v2_run_id"] == prior["run_id"]
    assert lineage["prior_v8_v2_attempt_consumed"] is True
    assert lineage["prior_v8_v2_attempt_reusable"] is False
    assert lineage["prior_v8_v2_authorization_reusable"] is False
    assert lineage["prior_v8_v2_result_reusable_as_authority"] is False
    assert lineage["prior_v8_v2_closeout_reusable_as_authority"] is False
    assert lineage["prior_v8_v2_lineage_closed"] is True
    assert lineage["historical_v9_attempt_reusable"] is False
    assert lineage["historical_v9_authorization_reusable"] is False
    assert out["historical_v9_attempt_reusable"] is False
    assert out["historical_v9_authorization_reusable"] is False


def test_request_preserves_fresh_preclaim_gpu_gate():
    out = request.pair06_v9_input_order_execution_authorization_request_contract()
    gpu = out["request"]["gpu_admission_policy"]

    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert out["minimum_cuda0_free_memory_fraction_denominator"] == 10
    assert gpu["fresh_observation_required"] is True
    assert gpu["historical_gpu_observation_reusable"] is False
    assert gpu["gpu_admission_hold_must_not_consume_attempt"] is True


def test_request_requires_three_fresh_authorizations_beyond_digest():
    out = request.pair06_v9_input_order_execution_authorization_request_contract()
    activation = out["request"]["activation"]

    assert out["fresh_execution_authorization_required"] is True
    assert out["fresh_policy_activation_authorization_required"] is True
    assert out["fresh_order_coherence_activation_authorization_required"] is True
    assert out["fresh_user_authorization_text_required"] is True
    assert out["matching_request_digest_grants_authority"] is False
    assert out["request_digest_reusable_as_authorization"] is False
    assert out["general_source_work_authorization_is_execution_authorization"] is False
    assert activation["separate_policy_activation_authorization_required"] is True
    assert activation[
        "separate_order_coherence_activation_authorization_required"
    ] is True
    assert activation["request_digest_grants_any_activation"] is False


@pytest.mark.parametrize(
    "field",
    request.FALSE_AUTHORITY_FIELDS
    + ("host_io_performed_by_contract_inspection",),
)
def test_request_grants_no_authority(field):
    out = request.pair06_v9_input_order_execution_authorization_request_contract()
    assert out[field] is False


def test_request_advances_only_to_source_binding_review():
    out = request.pair06_v9_input_order_execution_authorization_request_contract()

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "EXECUTION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "EXECUTION_AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_authorize_or_execute_holds():
    with pytest.raises(
        request.Pair06V9InputOrderCoherenceAuthorizationRequestHold,
        match="INPUT_ORDER_COHERENCE_EXECUTION_AUTHORIZATION_REQUEST_"
        "SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        request.authorize_or_execute()
