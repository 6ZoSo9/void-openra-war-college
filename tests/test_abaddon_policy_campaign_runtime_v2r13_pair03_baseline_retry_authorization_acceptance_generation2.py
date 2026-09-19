from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_baseline_retry_authorization_acceptance_generation2
    as authorization,
)


def test_retry_authorization_is_exactly_one_pair03_baseline_retry():
    out = authorization.v2r13_pair03_baseline_retry_authorization_acceptance_contract()
    assert out["pair_slot"] == 3
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["retry_authorization_accepted"] is True
    assert out["max_retry_executions"] == 1
    assert out["automatic_retry"] is False


def test_retry_is_not_yet_executable_before_preservation_evidence_acceptance():
    out = authorization.v2r13_pair03_baseline_retry_authorization_acceptance_contract()
    assert out["preservation_must_complete_before_retry"] is True
    assert out["preservation_receipt_must_be_accepted_before_retry"] is True
    assert out["retry_execution_authorized_now"] is False
    assert out["runtime_retry_performed"] is False
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_PRESERVATION_EVIDENCE_ACCEPTANCE_REQUIRED",
    )


def test_retry_authorization_does_not_expand_scope():
    out = authorization.v2r13_pair03_baseline_retry_authorization_acceptance_contract()
    assert out["candidate_arm_authorized"] is False
    assert out["held_out_arm_authorized"] is False
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_retry_entrypoint_holds_until_preservation_evidence_acceptance():
    with pytest.raises(
        authorization.V2R13Pair03BaselineRetryAuthorizationHold,
        match="V2R13_PAIR03_BASELINE_PRESERVATION_EVIDENCE_ACCEPTANCE_REQUIRED",
    ):
        authorization.execute_retry()
