from __future__ import annotations

from types import FunctionType

import pytest

from openra_env.learning import apollyon_v8_campaign_runtime as v8_runtime
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v4_runtime_integration_generation2
    as integration,
)


def _request(feedback: str) -> dict:
    return {
        "attempt_id": "a" * 64,
        "round_no": 6,
        "attempt_no": 2,
        "state": {
            "units_summary": [
                {"id": 201, "type": "e1", "idle": True, "can_attack": True,
                 "cell_x": 20, "cell_y": 20},
                {"id": 202, "type": "e1", "idle": True, "can_attack": True,
                 "cell_x": 21, "cell_y": 20},
            ]
        },
        "typed_tools": [],
        "tool_contract": {},
        "doctrine": "FEINTER",
        "feedback": feedback,
    }


def test_nonmatching_feedback_delegates_to_v3_response_unchanged(monkeypatch):
    seen = []

    def delegate(runtime, request, *, seq, authority_check):
        seen.append((runtime, request, seq, authority_check))
        return {"type": "DECIDE_RESPONSE", "campaign_action": {"tool": "stop_units"}}

    monkeypatch.setattr(integration, "ORIGINAL_V3_DECISION_RESPONSE", delegate)
    monkeypatch.setattr(integration, "_dependencies", lambda: {})
    runtime = object()
    authority = lambda pair, arm: True
    request = _request("other")

    out = integration.decision_response_with_v4_unit_ids_canonicalization(
        runtime, request, seq=3, authority_check=authority
    )
    assert out["campaign_action"]["tool"] == "stop_units"
    assert seen == [(runtime, request, 3, authority)]


def test_proxy_repairs_only_exact_unit_ids_invalid_and_revalidates(monkeypatch):
    raw = (
        "<tool_call><function=move_units>"
        "<parameter=unit_ids>[201,202]</parameter>"
        "<parameter=target_x>25</parameter>"
        "<parameter=target_y>26</parameter>"
        "</function></tool_call>"
    )

    class Runtime:
        def generate(self, *, messages, tools):
            return raw

    monkeypatch.setattr(
        integration.v3_runtime,
        "_build_v3_runtime_turn",
        lambda **kwargs: {
            "messages": [{"role": "system", "content": "x"},
                         {"role": "user", "content": "y"}],
            "tools": [{"type": "function", "function": {"name": "move_units"}}],
        },
    )

    calls = []

    def translate(*, text, runtime_tools, tool_contract):
        calls.append(text)
        if text == raw:
            raise v8_runtime.V8CampaignRuntimeError("unit_ids invalid")
        return {
            "tool": "move_units",
            "arguments": {"unit_ids": "201,202", "target_x": 25, "target_y": 26},
        }

    monkeypatch.setattr(
        integration.v8_runtime, "translate_v8_output_to_campaign", translate
    )
    monkeypatch.setattr(
        integration.v4_repair,
        "canonicalize_move_units_unit_ids",
        lambda **kwargs: {
            "canonicalization_applied": True,
            "canonical_raw_model_output": "CANONICAL",
            "canonical_unit_ids": "201,202",
        },
    )

    proxy = integration._V4RuntimeProxy(Runtime())
    out = proxy.decide_campaign_turn(
        state=_request(integration.TRIGGER)["state"],
        typed_tools=[],
        tool_contract={},
        doctrine="FEINTER",
        round_no=6,
        feedback=integration.TRIGGER,
    )

    assert calls == [raw, "CANONICAL"]
    assert out["raw_model_output"] == raw
    assert out["translated_model_output"] == "CANONICAL"
    assert out["v4_unit_ids_canonicalization"]["canonicalization_applied"] is True
    assert out["campaign_action"]["arguments"]["unit_ids"] == "201,202"
    assert out["host_mutation_performed"] is False


def test_proxy_does_not_repair_other_translator_errors(monkeypatch):
    class Runtime:
        def generate(self, *, messages, tools):
            return "RAW"

    monkeypatch.setattr(
        integration.v3_runtime,
        "_build_v3_runtime_turn",
        lambda **kwargs: {"messages": [], "tools": []},
    )
    monkeypatch.setattr(
        integration.v8_runtime,
        "translate_v8_output_to_campaign",
        lambda **kwargs: (_ for _ in ()).throw(
            v8_runtime.V8CampaignRuntimeError("movement coordinates invalid")
        ),
    )
    monkeypatch.setattr(
        integration.v4_repair,
        "canonicalize_move_units_unit_ids",
        lambda **kwargs: (_ for _ in ()).throw(AssertionError("must not repair")),
    )

    with pytest.raises(v8_runtime.V8CampaignRuntimeError, match="movement coordinates"):
        integration._V4RuntimeProxy(Runtime()).decide_campaign_turn(
            state={}, typed_tools=[], tool_contract={},
            doctrine="FEINTER", round_no=6, feedback=integration.TRIGGER
        )


def test_exact_trigger_requires_authority_before_v4_proxy(monkeypatch):
    monkeypatch.setattr(integration, "_dependencies", lambda: {})
    with pytest.raises(
        integration.Pair06V9ActionableFeedbackV4RuntimeIntegrationHold,
        match="AUTHORITY_REVOKED",
    ):
        integration.decision_response_with_v4_unit_ids_canonicalization(
            object(),
            _request(integration.TRIGGER),
            seq=1,
            authority_check=lambda pair, arm: False,
        )


def test_parent_builder_is_call_scoped_and_preserves_child_binding(monkeypatch):
    monkeypatch.setattr(integration, "_dependencies", lambda: {})
    original_child = object()

    def parent(*args, **kwargs):
        return None

    scoped = FunctionType(
        parent.__code__,
        {
            **parent.__globals__,
            "_decision_response": integration.ORIGINAL_V3_DECISION_RESPONSE,
            "_child_command": original_child,
        },
        parent.__name__,
        parent.__defaults__,
        parent.__closure__,
    )
    monkeypatch.setattr(integration, "ORIGINAL_V3_PARENT_BUILD", lambda: scoped)
    monkeypatch.setattr(
        integration.v3_runtime,
        "build_pair06_v9_actionable_feedback_v3_parent_run",
        integration.ORIGINAL_V3_PARENT_BUILD,
    )
    monkeypatch.setattr(
        integration.v3_runtime,
        "decision_response_with_v3_structured_correction",
        integration.ORIGINAL_V3_DECISION_RESPONSE,
    )

    out = integration.build_pair06_v9_actionable_feedback_v4_parent_run()
    assert isinstance(out, FunctionType)
    assert out.__globals__["_decision_response"] is (
        integration.decision_response_with_v4_unit_ids_canonicalization
    )
    assert out.__globals__["_child_command"] is original_child


@pytest.mark.parametrize(
    "field",
    (
        "frozen_v8_runtime_source_modified",
        "frozen_v8_parser_modified",
        "frozen_v8_translator_modified",
        "host_validator_modified",
        "host_validator_bypassed",
        "six_attempt_bound_modified",
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
        "consumed_v3_attempt_retry_authorized",
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
    out = integration.pair06_v9_actionable_feedback_v4_runtime_integration_contract()
    assert out[field] is False


def test_contract_stops_at_source_binding_review():
    out = integration.pair06_v9_actionable_feedback_v4_runtime_integration_contract()
    assert out["source_frontier_closed"] is True
    assert out["next_gate"].endswith("SOURCE_BINDING_REVIEW_REQUIRED")
