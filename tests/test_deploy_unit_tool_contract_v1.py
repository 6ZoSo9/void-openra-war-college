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


def test_deploy_unit_contract_exposes_delayed_completion():
    node = _function("deploy_unit")
    doc = ast.get_docstring(node) or ""

    assert "Deployment is not instantaneous." in doc
    assert "call advance() as a separate" in doc
    assert "verify the Construction Yard exists" in doc
    assert "same tool-call response or plan" in doc


def test_deploy_unit_returns_pending_completion_feedback():
    node = _function("deploy_unit")

    result_from_execute = False
    note_assignment = False

    for stmt in ast.walk(node):
        if not isinstance(stmt, ast.Assign):
            continue

        if (
            len(stmt.targets) == 1
            and isinstance(stmt.targets[0], ast.Name)
            and stmt.targets[0].id == "result"
            and isinstance(stmt.value, ast.Call)
            and isinstance(stmt.value.func, ast.Attribute)
            and stmt.value.func.attr == "_execute_commands"
        ):
            result_from_execute = True

        for target in stmt.targets:
            if (
                isinstance(target, ast.Subscript)
                and isinstance(target.value, ast.Name)
                and target.value.id == "result"
                and isinstance(target.slice, ast.Constant)
                and target.slice.value == "note"
            ):
                note_assignment = True

    assert result_from_execute
    assert note_assignment

    returns = [
        stmt.value.id
        for stmt in ast.walk(node)
        if isinstance(stmt, ast.Return)
        and isinstance(stmt.value, ast.Name)
    ]
    assert "result" in returns


def test_deploy_unit_does_not_gain_automatic_advance_semantics():
    node = _function("deploy_unit")
    called_names: list[str] = []
    called_attrs: list[str] = []

    for call in [
        item for item in ast.walk(node) if isinstance(item, ast.Call)
    ]:
        if isinstance(call.func, ast.Name):
            called_names.append(call.func.id)
        elif isinstance(call.func, ast.Attribute):
            called_attrs.append(call.func.attr)

    assert "advance" not in called_names
    assert "fast_advance_unary" not in called_attrs
    assert called_attrs.count("_execute_commands") == 1


def test_plan_contract_no_longer_teaches_deploy_then_build_without_time():
    node = _function("plan")
    doc = ast.get_docstring(node) or ""

    assert "plan does NOT advance game time between steps" in doc
    assert "Do not use plan to chain deploy_unit() directly" in doc
    assert "call deploy_unit() separately" in doc
    assert "call advance() separately" in doc
    assert "Example — deploy then build:" not in doc
