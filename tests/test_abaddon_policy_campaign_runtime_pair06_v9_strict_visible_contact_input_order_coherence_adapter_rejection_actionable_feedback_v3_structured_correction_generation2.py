from __future__ import annotations

import json

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_structured_correction_generation2
    as correction,
)


def test_exact_trigger_builds_structured_correction():
    out = correction.build_structured_correction_retry_context(
        feedback=correction.V2_TRIGGER
    )
    assert out["input_feedback"] == correction.V2_TRIGGER
    assert out["structured_feedback"].startswith(correction.V3_FEEDBACK_PREFIX)
    payload = json.loads(
        out["structured_feedback"][len(correction.V3_FEEDBACK_PREFIX):]
    )
    assert payload == out["structured_payload"]
    assert payload["tool"] == "move_units"
    assert payload["argument"] == "unit_ids"
    assert payload["required_json_type"] == "string"
    assert payload["ids_source"] == "CURRENT STATE own_units id values"
    assert payload["valid_single_argument_json"] == '{"unit_ids":"135"}'
    assert payload["valid_multiple_argument_json"] == '{"unit_ids":"135,137"}'
    assert payload["invalid_json_array_argument_json"] == '{"unit_ids":[135,137]}'
    assert payload["invalid_bare_integer_argument_json"] == '{"unit_ids":135}'


@pytest.mark.parametrize(
    "feedback",
    (
        "",
        "unit_ids invalid",
        "function_not_offered:move_units",
    ),
)
def test_non_exact_trigger_is_rejected(feedback):
    with pytest.raises(
        correction.Pair06V9ActionableFeedbackV3StructuredCorrectionHold,
        match="EXACT_V2_TRIGGER_REQUIRED",
    ):
        correction.build_structured_correction_retry_context(feedback=feedback)


def test_transfer_prompt_is_preserved_for_correction():
    out = correction.build_structured_correction_retry_context(
        feedback=correction.V2_TRIGGER
    )
    assert out["system_prompt"] == correction.v8_runtime.TRANSFER_SYSTEM_PROMPT
    assert out["system_prompt_family"] == "transfer"
    assert out["preserve_transfer_system_prompt"] is True
    assert out["legacy_system_prompt_selected"] is False


def test_frozen_runtime_boundaries_remain_unchanged():
    out = correction.pair06_v9_actionable_feedback_v3_structured_correction_contract()

    assert out["structured_correction_v3_implemented"] is True
    assert out["exact_v2_trigger_only"] is True
    assert out["move_units_unit_ids_required_json_type"] == "string"
    assert out["preserve_transfer_system_prompt_required"] is True
    assert out["legacy_prompt_fallback_for_v3_correction_forbidden"] is True
    assert out["reviewed_transfer_acceptance_correct"] == 28
    assert out["reviewed_legacy_acceptance_correct"] == 24

    for field in (
        "frozen_v8_tool_schema_modified",
        "frozen_v8_parser_modified",
        "frozen_v8_translator_modified",
        "host_validator_modified",
        "six_attempt_bound_modified",
        "malformed_unit_ids_coerced",
        "malformed_unit_ids_accepted",
    ):
        assert out[field] is False


@pytest.mark.parametrize(
    "field",
    (
        "consumed_v2_attempt_retry_authorized",
        "new_execution_request_opened",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "automatic_retry",
        "replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "contract_inspection_performs_host_io",
    ),
)
def test_no_runtime_or_follow_on_authority(field):
    out = correction.pair06_v9_actionable_feedback_v3_structured_correction_contract()
    assert out[field] is False


def test_next_gate_is_runtime_integration():
    out = correction.pair06_v9_actionable_feedback_v3_structured_correction_contract()
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V3_STRUCTURED_CORRECTION_RUNTIME_INTEGRATION_REQUIRED"
    )
