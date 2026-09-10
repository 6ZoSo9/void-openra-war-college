from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / "openra_env/agent.py"


def _namespace() -> dict:
    tree = ast.parse(AGENT.read_text(encoding="utf-8"))
    wanted = {"_mutation_turn_can_execute", "_mutation_turn_hold_result"}
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
    exec(
        compile(ast.Module(body=body, type_ignores=[]), str(AGENT), "exec"),
        ns,
    )
    return ns


def test_observation_calls_remain_executable_after_mutation_slot_is_reserved():
    ns = _namespace()
    can_execute = ns["_mutation_turn_can_execute"]

    assert can_execute("get_game_state", True) is True
    assert can_execute("get_map_analysis", True) is True
    assert can_execute("lookup_building", True) is True


def test_mutation_can_execute_before_slot_is_reserved_but_not_after():
    ns = _namespace()
    can_execute = ns["_mutation_turn_can_execute"]

    assert can_execute("deploy_unit", False) is True
    assert can_execute("advance", False) is True
    assert can_execute("deploy_unit", True) is False
    assert can_execute("advance", True) is False
    assert can_execute("build_and_place", True) is False


def test_batch_and_plan_remain_mutation_capable_for_slot_purposes():
    ns = _namespace()
    can_execute = ns["_mutation_turn_can_execute"]

    assert can_execute("batch", False) is True
    assert can_execute("plan", False) is True
    assert can_execute("batch", True) is False
    assert can_execute("plan", True) is False


def test_hold_result_is_nonexecuting_and_not_a_fake_error():
    ns = _namespace()
    result = ns["_mutation_turn_hold_result"]("build_and_place")

    assert result["mutation_turn_hold"] is True
    assert result["executed"] is False
    assert result["held_tool"] == "build_and_place"
    assert "previous mutation-capable tool call" in result["reason"]
    assert "new assistant response" in result["next_step"]
    assert "error" not in result


def _gameplay_execution_source() -> str:
    source = AGENT.read_text(encoding="utf-8")
    start = source.index(
        "# Execute each tool call. A host-side non-executing hold does not"
    )
    end = source.index("# Detect game connection lost", start)
    return source[start:end]


def test_gameplay_loop_reserves_only_after_precondition_hold_is_ruled_out():
    execution = _gameplay_execution_source()

    pins = [
        "mutation_execution_reserved = False",
        "for tc in tool_calls:",
        "execute_tool_call = _mutation_turn_can_execute(",
        "precondition_hold = _known_production_precondition_hold(",
        "if precondition_hold is not None:",
        "result = precondition_hold",
        "mutation_execution_reserved = True",
        "prepared_tool_call = await g2_frontier.prepare_call(",
        "result = await env.call_tool(fn_name, **fn_args)",
    ]
    for pin in pins:
        assert execution.count(pin) == 1

    positions = [execution.index(pin) for pin in pins]
    assert positions == sorted(positions)


def test_production_hold_branch_does_not_reserve_mutation_execution_slot():
    tree = ast.parse(AGENT.read_text(encoding="utf-8"))
    run_agent = next(
        node
        for node in tree.body
        if isinstance(node, ast.AsyncFunctionDef) and node.name == "run_agent"
    )

    precondition_branches = [
        node
        for node in ast.walk(run_agent)
        if isinstance(node, ast.If)
        and ast.unparse(node.test) == "precondition_hold is not None"
    ]
    assert len(precondition_branches) == 1
    branch = precondition_branches[0]

    hold_body = ast.unparse(ast.Module(body=branch.body, type_ignores=[]))
    execute_body = ast.unparse(ast.Module(body=branch.orelse, type_ignores=[]))

    assert "result = precondition_hold" in hold_body
    assert "mutation_execution_reserved = True" not in hold_body
    assert "g2_frontier.prepare_call" not in hold_body
    assert "env.call_tool" not in hold_body

    assert "mutation_execution_reserved = True" in execute_body
    assert "g2_frontier.prepare_call" in execute_body
    assert "env.call_tool" in execute_body


def test_later_mutation_hold_branch_cannot_reach_g2_or_environment():
    tree = ast.parse(AGENT.read_text(encoding="utf-8"))
    run_agent = next(
        node
        for node in tree.body
        if isinstance(node, ast.AsyncFunctionDef) and node.name == "run_agent"
    )
    holds = [
        node
        for node in ast.walk(run_agent)
        if isinstance(node, ast.If)
        and ast.unparse(node.test) == "not execute_tool_call"
    ]
    assert len(holds) == 1
    hold = holds[0]

    body = ast.unparse(ast.Module(body=hold.body, type_ignores=[]))
    other = ast.unparse(ast.Module(body=hold.orelse, type_ignores=[]))

    assert "_mutation_turn_hold_result(fn_name)" in body
    assert "g2_frontier.prepare_call" not in body
    assert "env.call_tool" not in body
    assert "_known_production_precondition_hold" in other
    assert "g2_frontier.prepare_call" in other


def test_invalid_production_then_valid_mutation_is_not_structurally_blocked():
    execution = _gameplay_execution_source()

    # The production hold is resolved before the only assignment that reserves
    # the mutation slot. Therefore a known-invalid first production proposal
    # returns without setting the slot, and a later valid mutation in this same
    # response can still enter the execution branch.
    hold = execution.index("result = precondition_hold")
    reserve = execution.index("mutation_execution_reserved = True")
    g2 = execution.index("prepared_tool_call = await g2_frontier.prepare_call(")

    assert hold < reserve < g2
