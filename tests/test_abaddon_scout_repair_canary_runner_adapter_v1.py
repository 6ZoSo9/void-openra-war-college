from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_canary_opponent_v1 as opponent
from openra_env.learning import abaddon_scout_repair_canary_runner_adapter_v1 as subject


class Base:
    def compact_state(self, state):
        return deepcopy(state)


def state(*, visible=(), combat=4):
    return {
        "map": {"width": 112, "height": 54},
        "units_summary": [
            {"id": 100 + i, "type": "e1", "can_attack": True, "cell_x": 15, "cell_y": 27}
            for i in range(combat)
        ],
        "buildings_summary": [{"id": 10, "type": "fact", "cell_x": 15, "cell_y": 27}],
        "enemy_summary": [{"id": uid, "type": "e1", "cell_x": 70, "cell_y": 27} for uid in visible],
        "enemy_buildings_summary": [],
    }


def builder(_base, _state, _pending):
    names = ["advance", "attack_move", "attack_target", "train_unit_e1"]
    return [{"name": name} for name in names], {"offered_tool_names": names, "legal_buildings": []}


def validator(_base, name, args, _state, _pending, _pb2, contract):
    assert name in contract["offered_tool_names"]
    return True, "accepted", [(name, deepcopy(args))]


def test_adapter_is_one_proposal_one_validation_and_historical_shape(monkeypatch):
    counts = {"proposal": 0, "validator": 0}
    original = opponent.propose_deterministic_pressure_action

    def counted_proposal(*args, **kwargs):
        counts["proposal"] += 1
        return original(*args, **kwargs)

    def counted_validator(*args, **kwargs):
        counts["validator"] += 1
        return validator(*args, **kwargs)

    monkeypatch.setattr(opponent, "propose_deterministic_pressure_action", counted_proposal)
    adapter = subject.DeterministicCanaryOpponentAdapter(
        tool_contract_builder=builder,
        typed_host_validator=counted_validator,
    )
    result = adapter.decide(Base(), object(), state(visible=(900, 700)), {}, object(), "FEINTER", 1)
    assert len(result) == 5
    name, args, commands, attempts, contract = result
    assert name == "attack_target"
    assert args["target_actor_id"] == 700
    assert len(commands) == 1
    assert len(attempts) == 1
    assert contract["offered_tool_names"][0] == "advance"
    assert counts == {"proposal": 1, "validator": 1}
    assert attempts[0]["training_candidate"] is False
    assert attempts[0]["model_backed"] is False


def test_helper_is_never_dereferenced():
    class ExplodingHelper:
        def __getattribute__(self, name):
            raise AssertionError("helper must not be touched")

    adapter = subject.DeterministicCanaryOpponentAdapter(
        tool_contract_builder=builder,
        typed_host_validator=validator,
    )
    adapter.decide(Base(), ExplodingHelper(), state(), {}, object(), "FEINTER", 1)
    snap = adapter.review_snapshot()
    assert snap["helper_dereferenced"] is False
    assert snap["model_service_start_implemented"] is False
    assert snap["model_inference_implemented"] is False
    assert snap["joint_dispatch_implemented"] is False


def test_host_rejection_holds_without_retry_or_advance(monkeypatch):
    counts = {"proposal": 0, "validator": 0}
    original = opponent.propose_deterministic_pressure_action

    def counted_proposal(*args, **kwargs):
        counts["proposal"] += 1
        return original(*args, **kwargs)

    def reject(*args, **kwargs):
        counts["validator"] += 1
        return False, "synthetic_reject", []

    monkeypatch.setattr(opponent, "propose_deterministic_pressure_action", counted_proposal)
    adapter = subject.DeterministicCanaryOpponentAdapter(
        tool_contract_builder=builder,
        typed_host_validator=reject,
    )
    with pytest.raises(subject.ScoutRepairCanaryRunnerAdapterHold, match="synthetic_reject"):
        adapter.decide(Base(), None, state(), {}, object(), "FEINTER", 1)
    assert counts == {"proposal": 1, "validator": 1}
    assert adapter.review_snapshot()["decision_calls"] == 0


def test_review_row_is_explicitly_nontraining_and_source_bound():
    adapter = subject.DeterministicCanaryOpponentAdapter(
        tool_contract_builder=builder,
        typed_host_validator=validator,
    )
    adapter.decide(Base(), None, state(), {}, object(), "FEINTER", 1)
    row = adapter.review_snapshot()["last_review_row"]
    assert row["training_candidate"] is False
    assert row["model_service_used"] is False
    assert row["model_inference_used"] is False
    assert row["proposal_count"] == 1
    assert row["host_validation_count"] == 1
    assert row["automatic_retry"] is False
    assert row["execution_authority"] is False
    assert row["deterministic_opponent_identity"]["sha256"] == "d602ba95d9a079e82ffc87cad22c8e6839ee5fdf1ccc910672018249359be66f"


def test_round_and_doctrine_are_bounded_and_monotonic():
    adapter = subject.DeterministicCanaryOpponentAdapter(
        tool_contract_builder=builder,
        typed_host_validator=validator,
    )
    with pytest.raises(subject.ScoutRepairCanaryRunnerAdapterHold, match="default_feinter"):
        adapter.decide(Base(), None, state(), {}, object(), "RUSHER", 1)
    adapter.decide(Base(), None, state(), {}, object(), "FEINTER", 1)
    with pytest.raises(subject.ScoutRepairCanaryRunnerAdapterHold, match="monotonically"):
        adapter.decide(Base(), None, state(), {}, object(), "FEINTER", 1)


def test_malformed_tool_contract_or_validator_output_holds():
    bad_builders = [
        lambda *_: ([], {}),
        lambda *_: ([], {"offered_tool_names": []}),
        lambda *_: ([], {"offered_tool_names": ["advance", "advance"]}),
    ]
    for bad in bad_builders:
        adapter = subject.DeterministicCanaryOpponentAdapter(
            tool_contract_builder=bad,
            typed_host_validator=validator,
        )
        with pytest.raises(subject.ScoutRepairCanaryRunnerAdapterHold):
            adapter.decide(Base(), None, state(), {}, object(), "FEINTER", 1)

    adapter = subject.DeterministicCanaryOpponentAdapter(
        tool_contract_builder=builder,
        typed_host_validator=lambda *_: (True, "ok"),
    )
    with pytest.raises(subject.ScoutRepairCanaryRunnerAdapterHold, match="result_shape"):
        adapter.decide(Base(), None, state(), {}, object(), "FEINTER", 1)


def test_adapter_review_is_explicitly_not_full_runner_admission():
    out = subject.adapter_review_claim()
    assert out["typed_current_turn_tool_contract_consumed"] is True
    assert out["adapter_review_rows_nontraining"] is True
    assert out["historical_runner_model_service_start_suppressed"] is False
    assert out["historical_runner_cleanup_service_action_suppressed"] is False
    assert out["historical_runner_durable_controller_rows_relabelled_nontraining"] is False
    assert out["full_runner_source_review_claim_valid"] is False
    assert out["execution_authority_created"] is False


def test_adapter_exposes_no_authorizing_entrypoint():
    with pytest.raises(subject.ScoutRepairCanaryRunnerAdapterHold, match="FULL_RUNNER_COMPOSITION"):
        subject.authorize_install_run_or_dispatch(authorized=True)


def test_source_has_no_runtime_or_io_imports_and_no_model_call_token():
    source = Path(subject.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.add(node.module)
    assert not modules & {"os", "pathlib", "subprocess", "socket", "httpx", "requests", "grpc", "docker"}
    assert ".ollama_tool_call(" not in source
    assert "start_ollama(" not in source
    assert "joint_advance(" not in source
    assert "open(" not in source
