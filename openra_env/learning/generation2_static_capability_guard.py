"""Static, source-only guard for reviewed Generation-2 capability boundaries.

The guard reads committed Python source as bytes and parses it with ``ast``.
It never imports the reviewed module and never executes its code.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


class CapabilityGuardError(ValueError):
    """Raised when a reviewed capability boundary fails closed."""


@dataclass(frozen=True)
class TargetSpec:
    path: str
    sha256: str
    contract_function: str
    gate_name: str
    gate_value: str
    hold_exception: str
    protected_false_fields: tuple[str, ...]
    held_entrypoints: tuple[str, ...]


PROTECTED_FALSE_FIELDS = (
    "host_path_resolved",
    "filesystem_path_resolved",
    "path_bindings_resolved",
    "workdir_materialized",
    "workdir_created",
    "filesystem_action_performed",
    "directory_creation_implemented",
    "runtime_execution_authorized",
    "runtime_started",
    "process_spawn_implemented",
    "command_execution_performed",
    "review_live_observation_implemented",
    "review_filesystem_observation_implemented",
    "review_git_query_implemented",
    "review_subprocess_execution_implemented",
    "review_network_request_implemented",
    "review_ollama_request_implemented",
    "review_docker_command_implemented",
    "review_service_action_implemented",
    "review_model_load_implemented",
    "review_model_inference_implemented",
    "review_game_execution_implemented",
    "review_training_implemented",
    "review_weights_update_implemented",
    "review_deployment_implemented",
    "review_void_chain_mutation_implemented",
    "review_wallet_or_funds_action_implemented",
)

HELD_ENTRYPOINTS = (
    "advance_execution_materialization",
    "create_isolated_workdir",
    "execute_materialized_command",
    "start_runtime",
    "authorize_runtime_execution",
)

TARGETS = (
    TargetSpec(
        path=(
            "openra_env/learning/"
            "abaddon_policy_campaign_isolated_workdir_allocator_"
            "source_binding_review_generation2.py"
        ),
        sha256="3985b0fbc74a25e29d44ae09d9c52c051ebb9044058d1bdd93ba6c9d1cca5761",
        contract_function="isolated_workdir_allocator_source_binding_review_contract",
        gate_name="NEXT_GATE",
        gate_value="RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
        hold_exception="IsolatedWorkdirAllocatorSourceBindingReviewHold",
        protected_false_fields=PROTECTED_FALSE_FIELDS,
        held_entrypoints=HELD_ENTRYPOINTS,
    ),
)

FORBIDDEN_IMPORT_ROOTS = {
    "asyncio",
    "ctypes",
    "http",
    "httpx",
    "multiprocessing",
    "os",
    "requests",
    "socket",
    "subprocess",
    "urllib",
}

FORBIDDEN_DIRECT_CALLS = {"__import__", "compile", "eval", "exec", "open"}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise CapabilityGuardError(message)


def _named_functions(tree: ast.Module) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    functions: dict[str, ast.FunctionDef | ast.AsyncFunctionDef] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            _require(node.name not in functions, f"duplicate function: {node.name}")
            functions[node.name] = node
    return functions


def _string_constants(tree: ast.Module) -> dict[str, str]:
    constants: dict[str, str] = {}
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        if isinstance(node, ast.Assign):
            if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
                continue
            name = node.targets[0].id
            value = node.value
        else:
            if not isinstance(node.target, ast.Name):
                continue
            name = node.target.id
            value = node.value
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            constants[name] = value.value
    return constants


def _contract_mapping(
    function: ast.FunctionDef | ast.AsyncFunctionDef,
) -> dict[str, ast.expr]:
    returns = [node for node in function.body if isinstance(node, ast.Return)]
    _require(len(returns) == 1, f"{function.name}: expected one direct return")
    value = returns[0].value
    _require(isinstance(value, ast.Dict), f"{function.name}: return must be a dict literal")

    mapping: dict[str, ast.expr] = {}
    assert isinstance(value, ast.Dict)
    for key, item in zip(value.keys, value.values, strict=True):
        if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
            continue
        _require(key.value not in mapping, f"{function.name}: duplicate key {key.value}")
        mapping[key.value] = item
    return mapping


def _verify_static_surface(tree: ast.Module, label: str) -> None:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                _require(root not in FORBIDDEN_IMPORT_ROOTS, f"{label}: forbidden import {root}")
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".", 1)[0]
            _require(root not in FORBIDDEN_IMPORT_ROOTS, f"{label}: forbidden import {root}")
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            _require(
                node.func.id not in FORBIDDEN_DIRECT_CALLS,
                f"{label}: forbidden direct call {node.func.id}",
            )


def _verify_held_entrypoint(
    function: ast.FunctionDef | ast.AsyncFunctionDef,
    spec: TargetSpec,
) -> None:
    _require(not isinstance(function, ast.AsyncFunctionDef), f"{function.name}: async entrypoint")
    _require(len(function.body) == 1, f"{function.name}: executable body expanded")
    statement = function.body[0]
    _require(isinstance(statement, ast.Raise), f"{function.name}: must raise authority hold")
    assert isinstance(statement, ast.Raise)
    raised = statement.exc
    _require(isinstance(raised, ast.Call), f"{function.name}: hold must be constructed")
    assert isinstance(raised, ast.Call)
    _require(
        isinstance(raised.func, ast.Name) and raised.func.id == spec.hold_exception,
        f"{function.name}: hold exception drift",
    )
    _require(len(raised.args) == 1 and not raised.keywords, f"{function.name}: hold arguments drift")
    argument = raised.args[0]
    _require(
        isinstance(argument, ast.Name) and argument.id == spec.gate_name,
        f"{function.name}: gate binding drift",
    )


def audit_source(source: bytes, spec: TargetSpec, *, label: str | None = None) -> dict[str, object]:
    target = label or spec.path
    digest = hashlib.sha256(source).hexdigest()
    _require(digest == spec.sha256, f"{target}: SHA-256 drift: {digest}")

    try:
        tree = ast.parse(source, filename=target)
    except (SyntaxError, UnicodeDecodeError) as exc:
        raise CapabilityGuardError(f"{target}: unreadable Python source: {exc}") from exc

    _verify_static_surface(tree, target)
    constants = _string_constants(tree)
    _require(constants.get(spec.gate_name) == spec.gate_value, f"{target}: next gate drift")

    functions = _named_functions(tree)
    _require(spec.contract_function in functions, f"{target}: contract function missing")
    mapping = _contract_mapping(functions[spec.contract_function])

    for field in spec.protected_false_fields:
        _require(field in mapping, f"{target}: protected field missing: {field}")
        value = mapping[field]
        _require(
            isinstance(value, ast.Constant) and value.value is False,
            f"{target}: protected field not literal false: {field}",
        )

    for entrypoint in spec.held_entrypoints:
        _require(entrypoint in functions, f"{target}: held entrypoint missing: {entrypoint}")
        _verify_held_entrypoint(functions[entrypoint], spec)

    return {
        "path": spec.path,
        "sha256": digest,
        "next_gate": spec.gate_value,
        "protected_false_field_count": len(spec.protected_false_fields),
        "held_entrypoint_count": len(spec.held_entrypoints),
        "module_imported": False,
        "runtime_execution": False,
    }


def audit_repository(root: Path, targets: Sequence[TargetSpec] = TARGETS) -> dict[str, object]:
    _require(bool(targets), "target census is empty")
    repository_root = root.resolve(strict=True)
    receipts: list[dict[str, object]] = []

    for spec in targets:
        relative = Path(spec.path)
        _require(not relative.is_absolute() and ".." not in relative.parts, f"unsafe target path: {spec.path}")
        candidate = repository_root / relative
        _require(not candidate.is_symlink(), f"symlink target rejected: {spec.path}")
        _require(candidate.is_file(), f"target missing: {spec.path}")
        _require(candidate.resolve().is_relative_to(repository_root), f"target escapes repository: {spec.path}")
        receipts.append(audit_source(candidate.read_bytes(), spec))

    return {
        "schema": "void.war-college.generation2-static-capability-guard.v1",
        "target_count": len(receipts),
        "targets": receipts,
        "source_only": True,
        "module_imports": 0,
        "runtime_execution": False,
        "training": False,
        "weights_update": False,
        "deployment": False,
        "void_mutation": False,
        "wallet_or_funds_action": False,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    receipt = audit_repository(args.repo_root)
    print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
