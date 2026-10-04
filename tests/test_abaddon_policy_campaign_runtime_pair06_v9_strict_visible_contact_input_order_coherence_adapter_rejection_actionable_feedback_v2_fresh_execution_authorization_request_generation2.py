from __future__ import annotations

import hashlib
import json

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_fresh_execution_authorization_request_generation2
    as request,
)


def test_request_is_deterministic_and_digest_matches_exact_bytes():
    first = request.fresh_execution_authorization_request()
    second = request.fresh_execution_authorization_request()
    assert first == second

    raw = (
        json.dumps(
            first["request"],
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")

    assert first["request_sha256"] == hashlib.sha256(raw).hexdigest()
    assert first["request_bytes"] == len(raw)
    assert first["request_bytes"] <= request.MAX_REQUEST_BYTES


def test_request_binds_closed_failed_lineage_and_fresh_v2_namespace():
    record = request.fresh_execution_authorization_request()["request"]
    lineage = record["lineage"]

    assert lineage["prior_attempt_marker_sha256"] == (
        "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d"
    )
    assert lineage["preservation_receipt_sha256"] == (
        "32c7089433072f8dc85880de911a3b24d68b35a0be71154ddd9a1af5705a0181"
    )
    assert lineage["prior_attempt_consumed"] is True
    assert lineage["prior_attempt_reusable"] is False
    assert lineage["prior_attempt_authorization_reusable"] is False
    assert lineage["preservation_lineage_closed"] is True
    assert lineage["preservation_authorization_reusable"] is False
    assert lineage["fresh_actionable_feedback_v2_evidence_namespace_required"] is True


def test_request_preserves_one_attempt_preclaim_gpu_safety():
    safety = request.fresh_execution_authorization_request()["request"]["runtime_safety"]
    assert safety["maximum_attempts"] == 1
    assert safety["maximum_automatic_retries"] == 0
    assert safety["fresh_preclaim_gpu_observation_required"] is True
    assert safety["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert safety["zero_foreign_cuda0_compute_processes_required"] is True
    assert safety["minimum_cuda0_free_memory_fraction_numerator"] == 9
    assert safety["minimum_cuda0_free_memory_fraction_denominator"] == 10


def test_request_requires_five_fresh_authorization_gates():
    boundary = request.fresh_execution_authorization_request()["request"][
        "authorization_boundary"
    ]

    assert boundary["fresh_execution_authorization_requested"] is True
    assert boundary["fresh_policy_activation_authorization_requested"] is True
    assert boundary["fresh_order_coherence_activation_authorization_requested"] is True
    assert boundary["fresh_repair_activation_authorization_requested"] is True
    assert boundary[
        "fresh_actionable_feedback_v2_activation_authorization_requested"
    ] is True
    assert boundary["five_distinct_confirmation_tokens_required"] is True
    assert boundary["fresh_user_authorization_text_required"] is True

    assert boundary["general_source_work_authorization_is_execution_authorization"] is False
    assert boundary["matching_request_digest_grants_authority"] is False
    assert boundary["matching_request_bytes_grant_authority"] is False
    assert boundary["prior_authorization_text_reusable"] is False
    assert boundary["preservation_authorization_reusable_as_execution_authority"] is False


@pytest.mark.parametrize("field", request.FALSE_AUTHORITY_FIELDS)
def test_request_record_grants_no_authority(field):
    record = request.fresh_execution_authorization_request()["request"]
    assert record[field] is False


@pytest.mark.parametrize(
    "field",
    (
        "request_grants_authority",
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "actionable_feedback_v2_activation_authorization_accepted",
        "host_io_performed",
        "attempt_marker_created",
        "runtime_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
        "scheduler_mutation_performed",
    ),
)
def test_validated_request_remains_non_authorizing(field):
    out = request.fresh_execution_authorization_request()
    assert out[field] is False


def test_request_advances_only_to_source_binding_review():
    out = request.fresh_execution_authorization_request()
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_FRESH_EXECUTION_AUTHORIZATION_REQUEST_"
        "SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_accept_or_execute_holds():
    with pytest.raises(
        request.Pair06V9ActionableFeedbackV2FreshExecutionRequestHold,
        match=(
            "ACTIONABLE_FEEDBACK_V2_FRESH_EXECUTION_AUTHORIZATION_REQUEST_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
    ):
        request.accept_or_execute()
