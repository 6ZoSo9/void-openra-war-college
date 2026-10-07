from __future__ import annotations

from types import FunctionType

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_structured_correction_runtime_integration_generation2
    as integration,
)


def _minimal_request(feedback: str) -> dict:
    return {
        "attempt_id": "a" * 64,
        "round_no": 6,
        "attempt_no": 2,
        "state": {"tick": 1},
        "typed_tools": [{"function": {"name": "move_units"}}],
        "tool_contract": {},
        "doctrine": "FEINTER",
        "feedback": feedback,
    }


def test_v3_turn_preserves_transfer_prompt_and_injects_structured_feedback(monkeypatch):
    seen = {}

    def translate(**kwargs):
        seen["translate_feedback"] = kwargs["feedback"]
        return {
            "schema": "test",
            "messages": [
                {"role": "system", "content": "transfer"},
                {"role": "user", "content": "baseline"},
            ],
            "tools": [{"type": "function", "function": {"name": "move_units"}}],
            "binding": {
                "system_prompt_family": "transfer",
                "runtime_tool_names": ["move_units"],
            },
            "runtime_input_sha256": "0" * 64,
        }

    def prompt(**kwargs):
        seen["prompt_feedback"] = kwargs["feedback"]
        return "CURRENT STATE: corrected"

    monkeypatch.setattr(integration.v8_runtime, "translate_campaign_turn_for_v8", translate)
    monkeypatch.setattr(integration.v8_runtime, "_v8_current_state_prompt", prompt)
    monkeypatch.setattr(integration.v8_runtime, "_sha256", lambda value: "f" * 64)

    out = integration._build_v3_runtime_turn(
        state={"tick": 1},
        typed_tools=[{"function": {"name": "move_units"}}],
        tool_contract={},
        doctrine="FEINTER",
        round_no=6,
        feedback=integration.v3_correction.V2_TRIGGER,
    )

    assert seen["translate_feedback"] == ""
    assert seen["prompt_feedback"].startswith(integration.v3_correction.V3_FEEDBACK_PREFIX)
    assert out["messages"][0] == {
        "role": "system",
        "content": integration.v8_runtime.TRANSFER_SYSTEM_PROMPT,
    }
    assert out["messages"][1]["content"] == "CURRENT STATE: corrected"
    assert out["binding"]["system_prompt_family"] == "transfer"
    assert out["binding"]["v3_structured_correction_applied"] is True
    assert out["binding"]["legacy_prompt_fallback_used"] is False
    assert out["runtime_input_sha256"] == "f" * 64


def test_runtime_proxy_delegates_nonmatching_feedback_unchanged():
    calls = []

    class Runtime:
        def decide_campaign_turn(self, **kwargs):
            calls.append(kwargs)
            return {"campaign_action": {"tool": "stop_units", "arguments": {}}}

    proxy = integration._V3RuntimeProxy(Runtime())
    out = proxy.decide_campaign_turn(
        state={},
        typed_tools=[],
        tool_contract={},
        doctrine="FEINTER",
        round_no=1,
        feedback="other",
    )

    assert out["campaign_action"]["tool"] == "stop_units"
    assert calls == [{
        "state": {},
        "typed_tools": [],
        "tool_contract": {},
        "doctrine": "FEINTER",
        "round_no": 1,
        "feedback": "other",
    }]


def test_runtime_proxy_exact_trigger_uses_structured_turn_and_frozen_translator(monkeypatch):
    generated = []
    translated = []

    class Runtime:
        def generate(self, *, messages, tools):
            generated.append((messages, tools))
            return "RAW"

    monkeypatch.setattr(
        integration,
        "_build_v3_runtime_turn",
        lambda **kwargs: {
            "messages": [
                {"role": "system", "content": "transfer"},
                {"role": "user", "content": "corrected"},
            ],
            "tools": [{"type": "function", "function": {"name": "move_units"}}],
            "binding": {"system_prompt_family": "transfer"},
            "runtime_input_sha256": "a" * 64,
        },
    )

    def translate(**kwargs):
        translated.append(kwargs)
        return {
            "tool": "move_units",
            "arguments": {
                "unit_ids": "135",
                "target_x": 1,
                "target_y": 2,
                "queued": False,
            },
        }

    monkeypatch.setattr(
        integration.v8_runtime,
        "translate_v8_output_to_campaign",
        translate,
    )

    proxy = integration._V3RuntimeProxy(Runtime())
    out = proxy.decide_campaign_turn(
        state={},
        typed_tools=[],
        tool_contract={"legal_units": []},
        doctrine="FEINTER",
        round_no=6,
        feedback=integration.v3_correction.V2_TRIGGER,
    )

    assert len(generated) == 1
    assert translated[0]["text"] == "RAW"
    assert out["raw_model_output"] == "RAW"
    assert out["campaign_action"]["arguments"]["unit_ids"] == "135"
    assert out["host_mutation_performed"] is False


def test_v3_decision_response_wraps_runtime_only_for_exact_trigger(monkeypatch):
    seen = []

    def v2_response(runtime, request, *, seq, authority_check):
        seen.append(runtime)
        return {
            "type": "DECIDE_RESPONSE",
            "seq": seq,
            "campaign_action": {"tool": "move_units", "arguments": {}},
        }

    monkeypatch.setattr(integration, "ORIGINAL_V2_DECISION_RESPONSE", v2_response)
    monkeypatch.setattr(integration, "_dependencies", lambda: {})
    authority = lambda pair, arm: True
    runtime = object()

    integration.decision_response_with_v3_structured_correction(
        runtime,
        _minimal_request("other"),
        seq=2,
        authority_check=authority,
    )
    assert seen[-1] is runtime

    integration.decision_response_with_v3_structured_correction(
        runtime,
        _minimal_request(integration.v3_correction.V2_TRIGGER),
        seq=3,
        authority_check=authority,
    )
    assert isinstance(seen[-1], integration._V3RuntimeProxy)
    assert seen[-1].runtime is runtime


def test_parent_builder_is_call_scoped_and_preserves_child_binding():
    scoped = integration.build_pair06_v9_actionable_feedback_v3_parent_run()
    assert isinstance(scoped, FunctionType)
    assert scoped.__globals__["_decision_response"] is (
        integration.decision_response_with_v3_structured_correction
    )
    assert integration.v2_parent.build_pair06_v9_actionable_feedback_v2_parent_run is (
        integration.ORIGINAL_V2_PARENT_BUILD
    )
    assert integration.v2_parent.ORIGINAL_V2_DECISION_RESPONSE is (
        integration.ORIGINAL_V2_DECISION_RESPONSE
    )


@pytest.mark.parametrize(
    "field",
    (
        "frozen_v8_tool_schema_modified",
        "frozen_v8_parser_modified",
        "frozen_v8_translator_modified",
        "host_validator_modified",
        "six_attempt_bound_modified",
        "malformed_unit_ids_coerced",
        "malformed_unit_ids_accepted",
        "process_global_parent_run_function_mutated",
        "process_global_child_command_builder_mutated",
        "process_global_decision_response_mutated",
        "process_global_runtime_method_mutated",
        "builder_executes_parent",
        "builder_performs_host_io",
        "builder_loads_model",
        "builder_runs_inference",
        "builder_spawns_child",
        "builder_executes_game",
        "consumed_v2_attempt_retry_authorized",
        "new_execution_request_opened",
        "attempt_claim_created",
        "attempt_created",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "automatic_retry",
        "replay_authorized",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ),
)
def test_contract_grants_no_runtime_or_extra_authority(field):
    out = integration.pair06_v9_actionable_feedback_v3_runtime_integration_contract()
    assert out[field] is False


def test_contract_stops_at_exact_blob_review():
    out = integration.pair06_v9_actionable_feedback_v3_runtime_integration_contract()
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V3_STRUCTURED_CORRECTION_"
        "RUNTIME_INTEGRATION_SOURCE_BINDING_REVIEW_REQUIRED"
    )
