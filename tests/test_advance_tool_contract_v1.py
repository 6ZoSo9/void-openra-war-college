from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "openra_env/server/openra_environment.py"


def _tree() -> ast.Module:
    return ast.parse(SERVER.read_text(encoding="utf-8"))


def _function(name: str) -> ast.FunctionDef:
    nodes = [
        node
        for node in ast.walk(_tree())
        if isinstance(node, ast.FunctionDef) and node.name == name
    ]
    assert len(nodes) == 1
    return nodes[0]


def test_advance_contract_advertises_real_per_call_bound_and_repetition():
    node = _function("advance")
    doc = ast.get_docstring(node) or ""

    assert "clamped to 1-50 ticks per call" in doc
    assert "call advance() repeatedly" in doc
    assert "prerequisite is present" in doc
    assert "500 ticks (max per call)" not in doc


def test_advance_preserves_intentional_fifty_tick_runtime_cap():
    node = _function("advance")
    matching_caps = []

    for call in [item for item in ast.walk(node) if isinstance(item, ast.Call)]:
        if not (isinstance(call.func, ast.Name) and call.func.id == "min"):
            continue
        names = [arg.id for arg in call.args if isinstance(arg, ast.Name)]
        constants = [arg.value for arg in call.args if isinstance(arg, ast.Constant)]
        if "ticks" in names and 50 in constants:
            matching_caps.append(call)

    assert len(matching_caps) == 1


def test_advance_reports_requested_effective_and_actual_ticks_truthfully():
    node = _function("advance")
    source = ast.unparse(node)

    assert "requested_ticks" in source
    assert "effective_ticks" in source
    assert "actual_ticks_advanced" in source
    assert "requested != ticks" in source
    assert "allowed range: 1-50" in source
    assert "Call advance() again if more game time is needed." in source
    assert "500 ticks (max per call)" not in source


def test_advance_keeps_one_bounded_bridge_call_and_no_recursive_auto_repeat():
    node = _function("advance")
    bridge_calls = []
    recursive_calls = []

    for call in [item for item in ast.walk(node) if isinstance(item, ast.Call)]:
        if isinstance(call.func, ast.Attribute) and call.func.attr == "fast_advance_unary":
            bridge_calls.append(call)
        if isinstance(call.func, ast.Name) and call.func.id == "advance":
            recursive_calls.append(call)

    assert len(bridge_calls) == 1
    assert recursive_calls == []
