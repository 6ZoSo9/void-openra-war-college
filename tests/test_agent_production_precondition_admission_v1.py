from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / "openra_env/agent.py"


def _helper():
    tree = ast.parse(AGENT.read_text(encoding="utf-8"))
    nodes = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "_known_production_precondition_hold"
    ]
    assert len(nodes) == 1
    namespace: dict = {}
    exec(
        compile(
            ast.Module(body=nodes, type_ignores=[]),
            str(AGENT),
            "exec",
        ),
        namespace,
    )
    return namespace["_known_production_precondition_hold"]


def test_available_production_is_admitted():
    guard = _helper()
    state = {"tick": 55, "available_production": ["powr", "tent"]}
    assert guard("build_and_place", {"building_type": "powr"}, state) is None
    assert guard("build_structure", {"building_type": "tent"}, state) is None


def test_known_unavailable_build_is_held_without_environment_error():
    guard = _helper()
    result = guard(
        "build_and_place",
        {"building_type": "powr"},
        {"tick": 4, "available_production": []},
    )

    assert result["production_precondition_hold"] is True
    assert result["executed"] is False
    assert result["held_tool"] == "build_and_place"
    assert result["requested_item"] == "powr"
    assert result["tick"] == 4
    assert result["available_production"] == []
    assert "known-invalid" in result["reason"]
    assert "call advance()" in result["next_step"]
    assert "error" not in result


def test_known_unavailable_unit_is_held():
    guard = _helper()
    result = guard(
        "build_unit",
        {"unit_type": "e1"},
        {"tick": 100, "available_production": ["powr", "tent"]},
    )
    assert result is not None
    assert result["held_tool"] == "build_unit"
    assert result["requested_item"] == "e1"


def test_unknown_availability_fails_open_to_existing_server_validation():
    guard = _helper()
    assert guard(
        "build_and_place",
        {"building_type": "powr"},
        {"tick": 4},
    ) is None
    assert guard(
        "build_unit",
        {"unit_type": "e1"},
        {},
    ) is None


def test_nonproduction_mutations_are_out_of_scope():
    guard = _helper()
    state = {"tick": 4, "available_production": []}
    assert guard("deploy_unit", {"unit_id": 120}, state) is None
    assert guard("advance", {"ticks": 50}, state) is None
    assert guard("attack_move", {"unit_ids": "all", "target_x": 1, "target_y": 1}, state) is None


def test_agent_tracks_exact_pre_response_state_and_guards_before_g2():
    source = AGENT.read_text(encoding="utf-8")

    initial = "latest_game_state = state if isinstance(state, dict) else {}"
    refresh = "latest_game_state = briefing_state"
    guard = "precondition_hold = _known_production_precondition_hold("
    g2 = "prepared_tool_call = await g2_frontier.prepare_call("

    assert source.count(initial) == 1
    assert source.count(refresh) == 1
    assert source.count(guard) == 1

    execution_start = source.index(
        "# Execute each tool call. Later mutation-capable calls from the"
    )
    execution_end = source.index("# Detect game connection lost", execution_start)
    execution = source[execution_start:execution_end]

    assert execution.count(guard) == 1
    assert execution.count(g2) == 1
    assert execution.index(guard) < execution.index(g2)


def test_precondition_hold_branch_does_not_reach_g2_or_environment():
    tree = ast.parse(AGENT.read_text(encoding="utf-8"))
    run_agent = next(
        node
        for node in tree.body
        if isinstance(node, ast.AsyncFunctionDef) and node.name == "run_agent"
    )

    branches = [
        node
        for node in ast.walk(run_agent)
        if isinstance(node, ast.If)
        and ast.unparse(node.test) == "precondition_hold is not None"
    ]
    assert len(branches) == 1

    branch = branches[0]
    body = ast.unparse(ast.Module(body=branch.body, type_ignores=[]))
    other = ast.unparse(ast.Module(body=branch.orelse, type_ignores=[]))

    assert "result = precondition_hold" in body
    assert "g2_frontier.prepare_call" not in body
    assert "env.call_tool" not in body
    assert "g2_frontier.prepare_call" in other
    assert "env.call_tool" in other

def test_later_turn_snapshot_is_cleared_before_fresh_state_read():
    source = AGENT.read_text(encoding="utf-8")
    loop = source.index("if total_api_calls > 0:")
    refresh = source.index(
        'briefing_state = await env.call_tool("get_game_state")',
        loop,
    )
    clear = source.index("latest_game_state = {}", loop, refresh)

    assert loop < clear < refresh

    # The broad refresh exception remains below this assignment. Therefore a
    # failed refresh leaves the guard with an empty snapshot, which the helper
    # already proves fails open to the environment's validation path.
    refresh_try_end = source.index("# Call LLM with retry for rate limits", refresh)
    exception = source.index("except Exception:", refresh, refresh_try_end)
    assert clear < refresh < exception
