from __future__ import annotations

from types import SimpleNamespace

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_proto_game_child_generation2
    as child,
)


class FakeLegacy:
    def __init__(self):
        self.APOLLYON_RUNNER = "/tmp/apollyon.py"
        self.apollyon_decision_typed = lambda *a, **k: None
        self.apollyon_tools_typed = lambda *a, **k: ([], {})
        self.decision_to_commands_typed = lambda *a, **k: (True, "ok", [])
        self._helper = SimpleNamespace(
            start_ollama=lambda: (_ for _ in ()).throw(AssertionError("ollama start")),
            cleanup=lambda: (_ for _ in ()).throw(AssertionError("ollama cleanup")),
        )

    def load_base(self):
        base = SimpleNamespace()
        base.APOLLYON_RUNNER = self.APOLLYON_RUNNER
        base.load_module = lambda path, name: self._helper
        return base


def test_contract_binds_exact_pair06_child_scope_and_stays_unauthorized():
    out = child.pair06_v8_proto_game_child_contract()
    assert out["pair06_v8_proto_game_child_implemented"] is True
    assert out["pair06_v8_proto_game_child_reviewed"] is False
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["doctrine"] == "FEINTER"
    assert out["seed"] == 208354846
    assert out["rounds"] == 36
    assert out["ticks_per_round"] == 25
    assert out["starter_infantry"] == 4
    assert out["staging_max_ticks"] == 800
    assert out["legacy_runner_sha256"] == (
        "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
    )
    assert out["game_execution_authorized"] is False
    assert out["subprocess_spawn_authorized"] is False


def test_helper_lifecycle_is_replaced_without_calling_original_ollama(monkeypatch):
    legacy = FakeLegacy()

    class FakeDecisionHooks:
        def __init__(self, legacy, decider):
            self.legacy = legacy
            self.decider = decider

        def install(self):
            pass

        def restore(self):
            pass

    monkeypatch.setattr(
        child.decision_adapter,
        "Pair06V8ApollyonDecisionHooks",
        FakeDecisionHooks,
    )
    monkeypatch.setattr(child, "_dependencies", lambda: {})

    hooks = child.Pair06V8ProtoChildHooks(legacy, object(), "a" * 64)
    hooks.install()
    try:
        base = legacy.load_base()
        helper = base.load_module(legacy.APOLLYON_RUNNER, "helper")
        helper.start_ollama()
        helper.cleanup()
    finally:
        hooks.restore()

    assert hooks.legacy_ollama_start_calls == 1
    assert hooks.legacy_ollama_cleanup_calls == 1


def test_contract_preserves_parent_and_later_launcher_boundaries():
    out = child.pair06_v8_proto_game_child_contract()
    assert out["socketpair_creation_implemented_by_this_source"] is False
    assert out["child_spawn_implemented_by_this_source"] is False
    assert out["worktree_materialization_implemented_by_this_source"] is False
    assert out["durable_attempt_claim_implemented_by_this_source"] is False
    assert out["v8_model_load_implemented_by_this_source"] is False
    assert out["v8_model_inference_implemented_by_this_source"] is False
    assert out["legacy_ollama_service_start_performed"] is False
    assert out["legacy_ollama_network_contact_performed"] is False


def test_contract_preserves_candidate_heldout_training_and_external_boundaries():
    out = child.pair06_v8_proto_game_child_contract()
    for field in (
        "game_execution_authorized",
        "subprocess_spawn_authorized",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False
    assert out["automatic_retry"] is False


def test_child_advances_only_to_separate_source_review():
    out = child.pair06_v8_proto_game_child_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PROTO_GAME_CHILD_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PROTO_GAME_CHILD_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_spawn_entrypoint_holds():
    with pytest.raises(
        child.Pair06V8ProtoGameChildHold,
        match="PAIR06_V8_PROTO_GAME_CHILD_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        child.spawn_child()
