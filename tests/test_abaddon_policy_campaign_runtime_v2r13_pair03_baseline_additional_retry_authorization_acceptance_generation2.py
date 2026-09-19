from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_additional_retry_authorization_acceptance_generation2
    as authorization,
)


def test_authorization_is_exactly_one_additional_pair03_baseline_retry():
    out = (
        authorization
        .v2r13_pair03_baseline_additional_retry_authorization_acceptance_contract()
    )
    assert out["pair_slot"] == 3
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["retry_index"] == 2
    assert out["additional_retry_authorization_accepted"] is True
    assert out["authorization_scope"] == (
        "exactly_one_additional_pair03_baseline_retry"
    )
    assert out["max_additional_retry_executions"] == 1
    assert out["total_retry_executions_authorized"] == 2


def test_prior_retry_must_be_consumed_and_preserved():
    out = (
        authorization
        .v2r13_pair03_baseline_additional_retry_authorization_acceptance_contract()
    )
    assert out["prior_retry_authorization_consumed"] is True
    assert out["failed_retry_preservation_evidence_reviewed"] is True
    assert out["canonical_arm_available_only_after_preservation"] is True


def test_authorization_does_not_execute_or_auto_retry():
    out = (
        authorization
        .v2r13_pair03_baseline_additional_retry_authorization_acceptance_contract()
    )
    assert out["automatic_retry"] is False
    assert out["additional_retry_execution_authorized_now"] is False
    assert out["additional_retry_execution_performed"] is False


def test_authorization_does_not_expand_scope():
    out = (
        authorization
        .v2r13_pair03_baseline_additional_retry_authorization_acceptance_contract()
    )
    for field in (
        "candidate_arm_authorized",
        "held_out_arm_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_authorization_advances_only_to_source_binding_review():
    out = (
        authorization
        .v2r13_pair03_baseline_additional_retry_authorization_acceptance_contract()
    )
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_AUTHORIZATION_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_AUTHORIZATION_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        authorization.V2R13Pair03BaselineAdditionalRetryAuthorizationHold,
        match=(
            "V2R13_PAIR03_BASELINE_ADDITIONAL_RETRY_AUTHORIZATION_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
    ):
        authorization.execute_additional_retry()
