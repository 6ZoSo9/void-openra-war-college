from __future__ import annotations

import pytest

from openra_env.learning import apollyon_v8_campaign_runtime as v8_runtime
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_response_generation2
    as shim,
)


def _request() -> dict:
    return {
        "attempt_id": "a" * 64,
        "round_no": 6,
        "attempt_no": 1,
    }


def test_contract_is_source_only_and_does_not_relax_unit_ids_validation():
    out = shim.pair06_v9_input_order_adapter_rejection_response_contract()

    assert out["adapter_rejection_response_shim_implemented"] is True
    assert out["observed_retryable_error"] == "unit_ids invalid"
    assert out["only_exact_observed_adapter_error_is_retryable"] is True
    assert out["other_v8_adapter_errors_still_propagate"] is True
    assert out["malformed_unit_ids_coerced"] is False
    assert out["malformed_unit_ids_accepted"] is False
    assert out["frozen_v8_runtime_source_modified"] is False
    assert out["historical_parent_source_modified"] is False
    assert out["runtime_execution_authorized"] is False
    assert out["automatic_retry"] is False
    assert out["consumed_input_order_attempt_retry_authorized"] is False


def test_historical_success_response_passes_through_unchanged(monkeypatch):
    expected = {
        "type": "DECIDE_RESPONSE",
        "seq": 7,
        "protocol_version": 1,
        "pair_slot": 6,
        "arm": "baseline",
        "attempt_id": "a" * 64,
        "round_no": 6,
        "attempt_no": 1,
        "campaign_action": {
            "tool": "advance",
            "arguments": {"ticks": 50},
        },
        "host_mutation_performed": False,
    }

    monkeypatch.setattr(
        shim,
        "ORIGINAL_DECISION_RESPONSE",
        lambda runtime, request, *, seq, authority_check: expected,
    )

    out = shim.decision_response_with_observed_adapter_rejection(
        object(),
        _request(),
        seq=7,
        authority_check=lambda pair_slot, arm: True,
    )
    assert out is expected


def test_exact_unit_ids_adapter_error_becomes_unavailable_sentinel(monkeypatch):
    def fail(runtime, request, *, seq, authority_check):
        raise v8_runtime.V8CampaignRuntimeError("unit_ids invalid")

    monkeypatch.setattr(shim, "ORIGINAL_DECISION_RESPONSE", fail)

    out = shim.decision_response_with_observed_adapter_rejection(
        object(),
        _request(),
        seq=9,
        authority_check=lambda pair_slot, arm: (
            pair_slot == 6 and arm == "baseline"
        ),
    )

    assert out == {
        "type": "DECIDE_RESPONSE",
        "seq": 9,
        "protocol_version": 1,
        "pair_slot": 6,
        "arm": "baseline",
        "attempt_id": "a" * 64,
        "round_no": 6,
        "attempt_no": 1,
        "campaign_action": {
            "tool": "__v8_adapter_rejected_unit_ids_invalid__",
            "arguments": {},
        },
        "host_mutation_performed": False,
    }


def test_other_v8_adapter_error_still_propagates(monkeypatch):
    def fail(runtime, request, *, seq, authority_check):
        raise v8_runtime.V8CampaignRuntimeError("movement coordinates invalid")

    monkeypatch.setattr(shim, "ORIGINAL_DECISION_RESPONSE", fail)

    with pytest.raises(
        v8_runtime.V8CampaignRuntimeError,
        match="movement coordinates invalid",
    ):
        shim.decision_response_with_observed_adapter_rejection(
            object(),
            _request(),
            seq=3,
            authority_check=lambda pair_slot, arm: True,
        )


def test_authority_revocation_after_exact_adapter_error_still_holds(monkeypatch):
    def fail(runtime, request, *, seq, authority_check):
        raise v8_runtime.V8CampaignRuntimeError("unit_ids invalid")

    monkeypatch.setattr(shim, "ORIGINAL_DECISION_RESPONSE", fail)

    with pytest.raises(
        shim.Pair06V9InputOrderAdapterRejectionResponseHold,
        match="AUTHORITY_REVOKED_AFTER_ADAPTER_REJECTION",
    ):
        shim.decision_response_with_observed_adapter_rejection(
            object(),
            _request(),
            seq=4,
            authority_check=lambda pair_slot, arm: False,
        )


def test_contract_advances_only_to_exact_blob_review():
    out = shim.pair06_v9_input_order_adapter_rejection_response_contract()

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_RESPONSE_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_review_or_execute_holds():
    with pytest.raises(
        shim.Pair06V9InputOrderAdapterRejectionResponseHold,
        match="ADAPTER_REJECTION_RESPONSE_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        shim.review_or_execute()
