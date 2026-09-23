from __future__ import annotations

from types import SimpleNamespace

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_game_coupled_runtime_generation2
    as runtime_core,
)

HOLD = runtime_core.Pair06V8BaselineGameCoupledRuntimeHold


def test_contract_is_implemented_but_inert_and_unauthorized():
    out = runtime_core.pair06_v8_baseline_game_coupled_runtime_contract()
    assert out["pair06_v8_baseline_game_coupled_runtime_implemented"] is True
    assert out["pair06_v8_baseline_game_coupled_runtime_reviewed"] is False
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["seed"] == 208354846
    assert out["rounds"] == 36
    assert out["same_process_load_and_game_implemented"] is True
    assert out["authority_check_before_load_implemented"] is True
    assert out["authority_check_before_each_inference_implemented"] is True
    assert out["game_runner_adapter_required"] is True
    assert out["game_runner_adapter_implemented_by_this_source"] is False
    assert out["game_coupled_load_authorized"] is False
    assert out["model_inference_authorized"] is False
    assert out["game_execution_authorized"] is False
    assert out["runtime_execution_performed_by_contract_inspection"] is False
    assert out["model_inference_performed_by_contract_inspection"] is False
    assert out["game_execution_performed_by_contract_inspection"] is False


def test_contract_preserves_candidate_heldout_training_and_external_boundaries():
    out = runtime_core.pair06_v8_baseline_game_coupled_runtime_contract()
    for field in (
        "candidate_runtime_load_authorized",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "pair03_replay_authorized",
        "pair09_replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False
    assert out["automatic_retry"] is False


def test_inert_execution_with_mocked_loader_and_runner(monkeypatch):
    decisions = []
    load_calls = []

    class Runtime:
        def decide_campaign_turn(self, **kwargs):
            decisions.append(kwargs)
            return {"campaign_action": {"name": "advance", "arguments": {"ticks": 50}}}

    def load(**kwargs):
        load_calls.append(kwargs)
        assert kwargs["pair_slot"] == 6
        assert kwargs["arm"] == "baseline"
        assert kwargs["runtime_load_authorized"] is True
        assert kwargs["authority_check"](6, "baseline") is True
        return Runtime()

    monkeypatch.setattr(runtime_core.capability, "load_pair06_v8_runtime", load)

    def authority(pair_slot, arm):
        return pair_slot == 6 and arm == "baseline"

    def game_runner(**kwargs):
        assert kwargs["pair_slot"] == 6
        assert kwargs["arm"] == "baseline"
        assert kwargs["seed"] == 208354846
        assert kwargs["rounds"] == 36
        assert kwargs["ticks_per_round"] == 25
        assert kwargs["starter_infantry"] == 4
        assert kwargs["staging_max_ticks"] == 800
        assert kwargs["runtime_selection_key"] == "apollyon-v3-v8-accepted-model-control"
        decision = kwargs["apollyon_decider"](
            state={"tick": 1},
            typed_tools=[],
            tool_contract={},
            doctrine="TEST",
            round_no=1,
        )
        assert decision["campaign_action"]["name"] == "advance"
        return {
            "pair_slot": 6,
            "arm": "baseline",
            "held_out": False,
            "seed": 208354846,
            "rounds_limit": 36,
            "ticks_per_round": 25,
            "starter_infantry": 4,
            "staging_max_ticks": 800,
            "runtime_selection_key": "apollyon-v3-v8-accepted-model-control",
            "runtime_load_performed": True,
            "runtime_started": True,
            "model_inference_performed": True,
            "model_inference_count": 1,
            "game_execution_performed": True,
            "runtime_cleanup_attempted": True,
            "runtime_cleanup_completed": True,
            "automatic_retry": False,
            "candidate_runtime_load_performed": False,
            "candidate_execution_performed": False,
            "held_out_execution_performed": False,
            "training_performed": False,
            "weights_updated": False,
            "automatic_policy_promotion": False,
            "deployment_performed": False,
            "void_chain_mutation_performed": False,
            "wallet_or_funds_action_performed": False,
        }

    out = runtime_core.execute_pair06_baseline_game_coupled_runtime(
        execution_authorized=True,
        authority_check=authority,
        game_runner=game_runner,
    )
    assert len(load_calls) == 1
    assert len(decisions) == 1
    assert out["runtime_load_performed"] is True
    assert out["model_inference_performed"] is True
    assert out["model_inference_count"] == 1
    assert out["game_execution_performed"] is True
    assert out["runtime_cleanup_completed"] is True
    assert out["automatic_retry"] is False
    assert len(out["execution_receipt_sha256"]) == 64


def test_authority_required_before_load(monkeypatch):
    def forbidden(**kwargs):
        raise AssertionError("load must not happen")

    monkeypatch.setattr(runtime_core.capability, "load_pair06_v8_runtime", forbidden)

    with pytest.raises(HOLD, match="AUTHORIZATION_REQUIRED"):
        runtime_core.execute_pair06_baseline_game_coupled_runtime(
            execution_authorized=False,
            authority_check=lambda pair_slot, arm: True,
            game_runner=lambda **kwargs: {},
        )


def test_revocation_before_load_stops_before_loader(monkeypatch):
    def forbidden(**kwargs):
        raise AssertionError("load must not happen")

    monkeypatch.setattr(runtime_core.capability, "load_pair06_v8_runtime", forbidden)

    with pytest.raises(HOLD, match="REVOKED_BEFORE_LOAD"):
        runtime_core.execute_pair06_baseline_game_coupled_runtime(
            execution_authorized=True,
            authority_check=lambda pair_slot, arm: False,
            game_runner=lambda **kwargs: {},
        )


def test_revocation_before_inference_is_enforced(monkeypatch):
    class Runtime:
        def decide_campaign_turn(self, **kwargs):
            raise AssertionError("model inference must not happen after revocation")

    monkeypatch.setattr(
        runtime_core.capability,
        "load_pair06_v8_runtime",
        lambda **kwargs: Runtime(),
    )

    calls = {"count": 0}

    def authority(pair_slot, arm):
        calls["count"] += 1
        return calls["count"] == 1

    def game_runner(**kwargs):
        kwargs["apollyon_decider"](
            state={"tick": 1},
            typed_tools=[],
            tool_contract={},
            doctrine="TEST",
            round_no=1,
        )
        raise AssertionError("unreachable")

    with pytest.raises(HOLD, match="REVOKED_BEFORE_INFERENCE"):
        runtime_core.execute_pair06_baseline_game_coupled_runtime(
            execution_authorized=True,
            authority_check=authority,
            game_runner=game_runner,
        )


def test_receipt_scope_drift_fails_closed(monkeypatch):
    class Runtime:
        def decide_campaign_turn(self, **kwargs):
            return {"campaign_action": {}}

    monkeypatch.setattr(
        runtime_core.capability,
        "load_pair06_v8_runtime",
        lambda **kwargs: Runtime(),
    )

    def runner(**kwargs):
        kwargs["apollyon_decider"](
            state={},
            typed_tools=[],
            tool_contract={},
            doctrine="TEST",
            round_no=1,
        )
        return {
            "pair_slot": 15,
            "arm": "baseline",
            "held_out": False,
            "seed": 208354846,
            "rounds_limit": 36,
            "ticks_per_round": 25,
            "starter_infantry": 4,
            "staging_max_ticks": 800,
            "runtime_selection_key": "apollyon-v3-v8-accepted-model-control",
            "runtime_load_performed": True,
            "runtime_started": True,
            "model_inference_performed": True,
            "model_inference_count": 1,
            "game_execution_performed": True,
            "runtime_cleanup_attempted": True,
            "runtime_cleanup_completed": True,
            "automatic_retry": False,
            "candidate_runtime_load_performed": False,
            "candidate_execution_performed": False,
            "held_out_execution_performed": False,
            "training_performed": False,
            "weights_updated": False,
            "automatic_policy_promotion": False,
            "deployment_performed": False,
            "void_chain_mutation_performed": False,
            "wallet_or_funds_action_performed": False,
        }

    with pytest.raises(HOLD, match="receipt drift: pair_slot"):
        runtime_core.execute_pair06_baseline_game_coupled_runtime(
            execution_authorized=True,
            authority_check=lambda pair_slot, arm: pair_slot == 6 and arm == "baseline",
            game_runner=runner,
        )


def test_contract_advances_only_to_separate_source_review():
    out = runtime_core.pair06_v8_baseline_game_coupled_runtime_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_GAME_COUPLED_RUNTIME_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_GAME_COUPLED_RUNTIME_SOURCE_BINDING_REVIEW_REQUIRED"
    )
