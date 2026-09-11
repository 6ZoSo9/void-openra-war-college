from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / "openra_env/agent.py"


def _namespace() -> dict:
    tree = ast.parse(AGENT.read_text(encoding="utf-8"))
    wanted = {"_mutation_turn_execution_mask", "_mutation_turn_hold_result"}
    body: list[ast.stmt] = []

    for node in tree.body:
        if (
            isinstance(node, ast.ImportFrom)
            and node.module == "openra_env.learning.g2_runtime_tool_classification"
        ):
            body.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name in wanted:
            body.append(node)

    assert {node.name for node in body if isinstance(node, ast.FunctionDef)} == wanted
    ns: dict = {}
    exec(compile(ast.Module(body=body, type_ignores=[]), str(AGENT), "exec"), ns)
    return ns


def _call(name: str) -> dict:
    return {
        "id": "call-" + name,
        "type": "function",
        "function": {"name": name, "arguments": "{}"},
    }


def test_observation_calls_remain_executable_in_same_response():
    ns = _namespace()
    mask = ns["_mutation_turn_execution_mask"](
        [_call("get_game_state"), _call("get_map_analysis"), _call("lookup_building")]
    )
    assert mask == (True, True, True)


def test_only_first_mutation_executes_but_later_observations_still_run():
    ns = _namespace()
    mask = ns["_mutation_turn_execution_mask"](
        [
            _call("deploy_unit"),
            _call("advance"),
            _call("get_game_state"),
            _call("build_and_place"),
            _call("get_production"),
        ]
    )
    assert mask == (True, False, True, False, True)


def test_batch_and_plan_consume_the_single_mutation_slot():
    ns = _namespace()
    assert ns["_mutation_turn_execution_mask"](
        [_call("batch"), _call("plan"), _call("advance")]
    ) == (True, False, False)


def test_hold_result_is_nonexecuting_and_not_a_fake_error():
    ns = _namespace()
    result = ns["_mutation_turn_hold_result"]("build_and_place")
    assert result["mutation_turn_hold"] is True
    assert result["executed"] is False
    assert result["held_tool"] == "build_and_place"
    assert "previous mutation-capable tool call" in result["reason"]
    assert "new assistant response" in result["next_step"]
    assert "error" not in result


def test_gameplay_loop_wires_hold_before_g2_prepare_and_world_call():
    source = AGENT.read_text(encoding="utf-8")
    start = source.index(
        "# Execute each tool call. Later mutation-capable calls from the"
    )
    end = source.index("# Detect game connection lost", start)
    gameplay_execution = source[start:end]

    pins = [
        "tool_execution_mask = _mutation_turn_execution_mask(tool_calls)",
        "result = _mutation_turn_hold_result(fn_name)",
        "prepared_tool_call = await g2_frontier.prepare_call(",
        "result = await env.call_tool(fn_name, **fn_args)",
    ]
    for pin in pins:
        assert gameplay_execution.count(pin) == 1

    positions = [gameplay_execution.index(pin) for pin in pins]
    assert positions == sorted(positions)


def test_held_mutation_branch_cannot_prepare_or_call_environment():
    tree = ast.parse(AGENT.read_text(encoding="utf-8"))
    run_agent = next(
        node
        for node in tree.body
        if isinstance(node, ast.AsyncFunctionDef) and node.name == "run_agent"
    )
    holds = [
        node
        for node in ast.walk(run_agent)
        if isinstance(node, ast.If) and ast.unparse(node.test) == "not execute_tool_call"
    ]
    assert len(holds) == 1
    hold = holds[0]
    body = ast.unparse(ast.Module(body=hold.body, type_ignores=[]))
    other = ast.unparse(ast.Module(body=hold.orelse, type_ignores=[]))
    assert "_mutation_turn_hold_result(fn_name)" in body
    assert "g2_frontier.prepare_call" not in body
    assert "env.call_tool" not in body
    assert "g2_frontier.prepare_call" in other
    assert "env.call_tool" in other
