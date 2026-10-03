from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_generation2
    as v2,
)


def _request() -> dict:
    return {
        "attempt_id": "a" * 64,
        "round_no": 6,
        "attempt_no": 2,
    }


def _response(tool: str) -> dict:
    return {
        "type": "DECIDE_RESPONSE",
        "seq": 9,
        "protocol_version": 1,
        "pair_slot": 6,
        "arm": "baseline",
        "attempt_id": "a" * 64,
        "round_no": 6,
        "attempt_no": 2,
        "campaign_action": {
            "tool": tool,
            "arguments": {},
        },
        "host_mutation_performed": False,
    }


def test_contract_encodes_exact_wire_format_correction_without_relaxation():
    out = v2.pair06_v9_adapter_rejection_actionable_feedback_v2_contract()

    assert out["actionable_feedback_v2_implemented"] is True
    assert out["v1_sentinel_tool"] == (
        "__v8_adapter_rejected_unit_ids_invalid__"
    )
    assert out["v2_sentinel_tool"] == (
        "__v8_adapter_rejected_move_units_unit_ids_must_be_quoted_string_"
        "not_json_array_or_bare_integer__"
    )
    assert out["expected_child_feedback"] == (
        "function_not_offered:"
        "__v8_adapter_rejected_move_units_unit_ids_must_be_quoted_string_"
        "not_json_array_or_bare_integer__"
    )
    assert out["quoted_string_example_single"] == '"123"'
    assert out["quoted_string_example_multiple"] == '"123,456"'
    assert out["invalid_json_array_example"] == "[123,456]"
    assert out["invalid_bare_integer_example"] == "123"

    assert out["frozen_v8_parser_modified"] is False
    assert out["frozen_v8_translator_modified"] is False
    assert out["malformed_unit_ids_coerced"] is False
    assert out["malformed_unit_ids_accepted"] is False
    assert out["six_attempt_decision_bound_modified"] is False
    assert out["host_validation_modified"] is False


def test_non_sentinel_v1_response_passes_through_by_identity(monkeypatch):
    expected = _response("advance")
    monkeypatch.setattr(
        v2,
        "ORIGINAL_V1_RESPONSE",
        lambda runtime, request, *, seq, authority_check: expected,
    )

    out = v2.decision_response_with_actionable_adapter_rejection_feedback(
        object(),
        _request(),
        seq=9,
        authority_check=lambda pair_slot, arm: True,
    )

    assert out is expected


def test_exact_v1_sentinel_is_rewritten_to_actionable_v2_sentinel(monkeypatch):
    original = _response(v2.V1_SENTINEL_TOOL)
    monkeypatch.setattr(
        v2,
        "ORIGINAL_V1_RESPONSE",
        lambda runtime, request, *, seq, authority_check: original,
    )

    out = v2.decision_response_with_actionable_adapter_rejection_feedback(
        object(),
        _request(),
        seq=9,
        authority_check=lambda pair_slot, arm: (
            pair_slot == 6 and arm == "baseline"
        ),
    )

    assert out is not original
    assert original["campaign_action"]["tool"] == v2.V1_SENTINEL_TOOL
    assert out["campaign_action"]["tool"] == v2.V2_SENTINEL_TOOL
    assert out["campaign_action"]["arguments"] == {}
    assert out["host_mutation_performed"] is False


def test_v2_rechecks_authority_before_rewriting_v1_sentinel(monkeypatch):
    monkeypatch.setattr(
        v2,
        "ORIGINAL_V1_RESPONSE",
        lambda runtime, request, *, seq, authority_check: _response(
            v2.V1_SENTINEL_TOOL
        ),
    )

    with pytest.raises(
        v2.Pair06V9AdapterRejectionActionableFeedbackV2Hold,
        match="AUTHORITY_REVOKED_AFTER_V1_SENTINEL",
    ):
        v2.decision_response_with_actionable_adapter_rejection_feedback(
            object(),
            _request(),
            seq=9,
            authority_check=lambda pair_slot, arm: False,
        )


@pytest.mark.parametrize(
    "field",
    (
        "v1_source_modified",
        "frozen_v8_parser_modified",
        "frozen_v8_translator_modified",
        "malformed_unit_ids_coerced",
        "malformed_unit_ids_accepted",
        "six_attempt_decision_bound_modified",
        "host_validation_modified",
        "world_mutation_before_child_validation",
        "consumed_attempt_retry_authorized",
        "new_execution_request_opened",
        "attempt_claim_created",
        "attempt_created",
        "runtime_execution_authorized",
        "automatic_retry",
        "replay_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_contract_grants_no_runtime_or_follow_on_authority(field):
    out = v2.pair06_v9_adapter_rejection_actionable_feedback_v2_contract()
    assert out[field] is False


def test_review_or_execute_holds():
    with pytest.raises(
        v2.Pair06V9AdapterRejectionActionableFeedbackV2Hold,
        match="ACTIONABLE_FEEDBACK_V2_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        v2.review_or_execute()
