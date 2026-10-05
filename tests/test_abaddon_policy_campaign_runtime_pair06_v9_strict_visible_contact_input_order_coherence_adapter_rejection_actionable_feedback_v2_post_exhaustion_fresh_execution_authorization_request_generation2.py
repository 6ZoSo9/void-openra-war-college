from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_post_exhaustion_fresh_execution_authorization_request_generation2
    as request,
)


def test_request_binds_closed_v2_failure_lineage():
    out = request.post_exhaustion_fresh_execution_authorization_request()
    record = out["request"]
    lineage = record["lineage"]

    assert record["record_kind"] == "proposal_only_not_authorization"
    assert lineage["prior_v2_attempt_marker_sha256"] == (
        "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
    )
    assert lineage["prior_v2_preservation_receipt_sha256"] == (
        "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
    )
    assert lineage["prior_v2_failure_class"] == (
        "strict_contact_actionable_feedback_v2_exhausted"
    )
    assert lineage["prior_v2_failure_round"] == 6
    assert lineage["prior_v2_attempt_consumed"] is True
    assert lineage["prior_v2_attempt_reusable"] is False
    assert lineage["prior_v2_execution_authorization_reusable"] is False
    assert lineage["prior_v2_preservation_authorization_reusable"] is False
    assert lineage["prior_v2_preservation_lineage_closed"] is True
    assert lineage["reviewed_operator_source_reuse_requested"] is True
    assert lineage["reviewed_operator_authorization_reuse_requested"] is False
    assert lineage["fresh_active_baseline_namespace_required"] is True
    assert lineage["archived_prior_v2_namespace_must_remain_immutable"] is True


def test_request_retains_one_attempt_zero_retry_and_fresh_gpu_gate():
    out = request.post_exhaustion_fresh_execution_authorization_request()
    safety = out["request"]["runtime_safety"]

    assert safety["maximum_attempts"] == 1
    assert safety["maximum_automatic_retries"] == 0
    assert safety["fresh_preclaim_gpu_observation_required"] is True
    assert safety["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert safety["zero_foreign_cuda0_compute_processes_required"] is True
    assert safety["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert safety["minimum_cuda0_free_memory_fraction_denominator"] == 10


def test_request_requires_five_fresh_authorization_gates():
    out = request.post_exhaustion_fresh_execution_authorization_request()
    boundary = out["request"]["authorization_boundary"]

    assert boundary["fresh_execution_authorization_requested"] is True
    assert boundary["fresh_policy_activation_authorization_requested"] is True
    assert boundary[
        "fresh_order_coherence_activation_authorization_requested"
    ] is True
    assert boundary["fresh_repair_activation_authorization_requested"] is True
    assert boundary[
        "fresh_actionable_feedback_v2_activation_authorization_requested"
    ] is True
    assert boundary["five_distinct_confirmation_tokens_required"] is True
    assert boundary["fresh_user_authorization_text_required"] is True
    assert (
        boundary["general_source_work_authorization_is_execution_authorization"]
        is False
    )
    assert boundary["matching_request_digest_grants_authority"] is False
    assert boundary["matching_request_bytes_grant_authority"] is False
    assert boundary["prior_execution_authorization_reusable"] is False
    assert (
        boundary["prior_preservation_authorization_reusable_as_execution_authority"]
        is False
    )


@pytest.mark.parametrize(
    "field",
    (
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "actionable_feedback_v2_activation_authorization_accepted",
        "attempt_marker_creation_authorized",
        "runtime_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "attempt_created",
        "runtime_execution_authorized",
        "replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_request_grants_no_authority(field):
    out = request.post_exhaustion_fresh_execution_authorization_request()
    assert out["request"][field] is False


def test_request_performs_no_host_or_runtime_effects():
    out = request.post_exhaustion_fresh_execution_authorization_request()

    assert out["request_grants_authority"] is False
    assert out["host_io_performed"] is False
    assert out["attempt_marker_created"] is False
    assert out["runtime_load_performed"] is False
    assert out["model_inference_performed"] is False
    assert out["game_execution_performed"] is False
    assert out["training_performed"] is False
    assert out["deployment_performed"] is False
    assert out["void_chain_mutation_performed"] is False
    assert out["wallet_or_funds_action_performed"] is False
    assert out["scheduler_mutation_performed"] is False


def test_request_advances_only_to_source_binding_review():
    out = request.post_exhaustion_fresh_execution_authorization_request()

    assert isinstance(out["request_sha256"], str)
    assert len(out["request_sha256"]) == 64
    assert out["request_bytes"] > 0
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_POST_EXHAUSTION_FRESH_EXECUTION_"
        "AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED"
    )

    with pytest.raises(
        request.Pair06V9ActionableFeedbackV2PostExhaustionFreshExecutionRequestHold,
        match="AUTHORIZATION_REQUEST_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        request.accept_or_execute()
