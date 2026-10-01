from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_generation2
    as proto_child,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_proto_child_wiring_generation2
    as wiring,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_runtime_integration_generation2
    as order_integration,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_proto_child_wiring_generation2
    as historical_v9_child,
)


class _Legacy:
    def load_base(self):
        return None

    def apollyon_tools_typed(self, base, state, pending):
        return [], {
            "offered_tool_names": [],
            "production_functions": {},
            "legal_units": [],
            "legal_buildings": [],
        }

    def decision_to_commands_typed(
        self,
        base,
        name,
        args,
        state,
        pending,
        pb2,
        contract,
    ):
        return True, "accepted", []

    def apollyon_decision_typed(self, *args, **kwargs):
        return "original"


def _run_kwargs():
    return {
        "sock": object(),
        "attempt_id": "a" * 64,
        "runs_root": "/runs",
        "frozen_source_root": "/source",
        "exact_engine_root": "/engine",
        "policy_activation_authorized": True,
        "order_coherence_activation_authorized": True,
        "execution_authorized": True,
    }


def test_contract_pins_exact_reviewed_dependencies():
    out = wiring.pair06_v9_input_order_coherence_proto_child_wiring_contract()

    assert out["order_integration_git_blob"] == (
        "166e4e84fd657adcdd752e53c8c6fd8ea555006b"
    )
    assert out["order_integration_review_git_blob"] == (
        "f17cadd048f4437d66792ae76dd1a096b475eba7"
    )
    assert out["historical_v9_child_git_blob"] == (
        "5fc4c66b0c0f23edb8c4932bba1c743fd63b9b12"
    )
    assert out["historical_v9_child_review_git_blob"] == (
        "747dd644fdff569745854f5a3d35758e150e5d2f"
    )
    assert out["v8_proto_child_git_blob"] == (
        "7ea5d27c2d2bb499dfec4c00d2812d7ed043f8bc"
    )
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"


def test_specialized_hooks_advance_only_the_decision_hook():
    legacy = _Legacy()
    hooks = wiring.Pair06V9InputOrderCoherentProtoChildHooks(
        legacy,
        object(),
        "b" * 64,
    )

    assert isinstance(
        hooks,
        historical_v9_child.Pair06V9StrictVisibleContactProtoChildHooks,
    )
    assert type(hooks._decision_hooks) is (
        order_integration.Pair06V9InputOrderCoherentDecisionHooks
    )
    assert hooks.v9_strict_visible_contact_decision_hook_bound is True
    assert hooks.input_order_coherence_decision_hook_bound is True
    assert hooks.legacy is legacy
    assert hooks.attempt_id == "b" * 64


def test_scoped_child_run_binds_factory_without_mutating_module_global():
    original_factory = proto_child.Pair06V8ProtoChildHooks
    original_run = proto_child.run_pair06_v8_proto_game_child

    scoped = wiring._scoped_v8_child_run()

    assert scoped is not original_run
    assert scoped.__code__ is original_run.__code__
    assert scoped.__globals__["Pair06V8ProtoChildHooks"] is (
        wiring.Pair06V9InputOrderCoherentProtoChildHooks
    )
    assert proto_child.Pair06V8ProtoChildHooks is original_factory
    assert proto_child.run_pair06_v8_proto_game_child is original_run


def test_wrapper_requires_historical_v9_policy_activation_gate():
    kwargs = _run_kwargs()
    kwargs["policy_activation_authorized"] = False

    with pytest.raises(
        wiring.Pair06V9InputOrderCoherenceProtoChildWiringHold,
        match="V9_STRICT_VISIBLE_CONTACT_POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
    ):
        wiring.run_pair06_v9_input_order_coherence_proto_game_child(**kwargs)


def test_wrapper_requires_distinct_order_coherence_activation_gate():
    kwargs = _run_kwargs()
    kwargs["order_coherence_activation_authorized"] = False

    with pytest.raises(
        wiring.Pair06V9InputOrderCoherenceProtoChildWiringHold,
        match="V9_INPUT_ORDER_COHERENCE_ACTIVATION_AUTHORIZATION_REQUIRED",
    ):
        wiring.run_pair06_v9_input_order_coherence_proto_game_child(**kwargs)


def test_wrapper_preserves_existing_child_execution_gate():
    kwargs = _run_kwargs()
    kwargs["execution_authorized"] = False

    with pytest.raises(
        wiring.Pair06V9InputOrderCoherenceProtoChildWiringHold,
        match="CHILD_GAME_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        wiring.run_pair06_v9_input_order_coherence_proto_game_child(**kwargs)


def test_wrapper_delegates_without_global_hook_factory_mutation(monkeypatch):
    observed = {}

    def fake_scoped_run(**kwargs):
        observed["factory"] = proto_child.Pair06V8ProtoChildHooks
        observed["run"] = proto_child.run_pair06_v8_proto_game_child
        observed["kwargs"] = kwargs
        return {"fake_child_result": True}

    monkeypatch.setattr(wiring, "_scoped_v8_child_run", lambda: fake_scoped_run)

    result = wiring.run_pair06_v9_input_order_coherence_proto_game_child(
        **_run_kwargs()
    )

    assert result == {"fake_child_result": True}
    assert observed["factory"] is wiring.ORIGINAL_V8_CHILD_HOOKS
    assert observed["run"] is wiring.ORIGINAL_V8_CHILD_RUN
    assert observed["kwargs"]["execution_authorized"] is True
    assert proto_child.Pair06V8ProtoChildHooks is wiring.ORIGINAL_V8_CHILD_HOOKS
    assert proto_child.run_pair06_v8_proto_game_child is wiring.ORIGINAL_V8_CHILD_RUN


def test_wrapper_keeps_globals_original_after_delegate_failure(monkeypatch):
    def fake_scoped_run(**kwargs):
        assert proto_child.Pair06V8ProtoChildHooks is wiring.ORIGINAL_V8_CHILD_HOOKS
        raise RuntimeError("synthetic child failure")

    monkeypatch.setattr(wiring, "_scoped_v8_child_run", lambda: fake_scoped_run)

    with pytest.raises(RuntimeError, match="synthetic child failure"):
        wiring.run_pair06_v9_input_order_coherence_proto_game_child(
            **_run_kwargs()
        )

    assert proto_child.Pair06V8ProtoChildHooks is wiring.ORIGINAL_V8_CHILD_HOOKS
    assert proto_child.run_pair06_v8_proto_game_child is wiring.ORIGINAL_V8_CHILD_RUN


def test_contract_grants_no_retry_or_effect_authority():
    out = wiring.pair06_v9_input_order_coherence_proto_child_wiring_contract()

    for field in (
        "consumed_v9_attempt_retry_authorized",
        "parent_supervisor_repair_wiring_implemented",
        "operator_repair_wiring_implemented",
        "new_execution_request_opened",
        "attempt_created",
        "runtime_activation_authorized",
        "runtime_execution_authorized",
        "replay_authorized",
        "automatic_retry",
        "training_authorized",
        "automatic_corpus_admission",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ):
        assert out[field] is False


def test_contract_records_global_isolation_and_fail_closed_order_boundary():
    out = wiring.pair06_v9_input_order_coherence_proto_child_wiring_contract()

    assert out["historical_v9_proto_child_source_modified"] is False
    assert out["existing_v8_proto_child_source_modified"] is False
    assert out["historical_v8_child_run_code_reused"] is True
    assert out["call_scoped_child_hook_factory_binding_implemented"] is True
    assert out["process_global_child_hook_factory_mutated"] is False
    assert out["process_global_child_run_function_mutated"] is False
    assert out["new_concurrency_scope_leak_introduced"] is False
    assert out["original_child_execution_authorization_gate_preserved"] is True
    assert out["historical_v9_policy_activation_gate_preserved"] is True
    assert out["additional_order_coherence_activation_gate_required"] is True
    assert out["typed_tool_membership_exact_match_required"] is True
    assert out["typed_tool_order_canonicalized_to_offered_order"] is True
    assert out["membership_drift_still_fail_closed"] is True


def test_wiring_advances_only_to_source_review():
    out = wiring.pair06_v9_input_order_coherence_proto_child_wiring_contract()

    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "PROTO_CHILD_WIRING_SOURCE_BINDING_REVIEW_REQUIRED",
    )


def test_entrypoint_holds():
    with pytest.raises(
        wiring.Pair06V9InputOrderCoherenceProtoChildWiringHold,
        match="PROTO_CHILD_WIRING_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        wiring.review_or_execute()
