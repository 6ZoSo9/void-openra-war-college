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
    dependency_blobs: tuple[tuple[str, str], ...] = ()


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

DEPENDENCY_BLOBS = (
    ("openra_env/learning/abaddon_policy_campaign_command_materializer_generation2.py", "4836360e0d284454f815a2a2e32078d2565e6dea"),
    ("openra_env/learning/abaddon_policy_campaign_command_materializer_source_binding_review_generation2.py", "dee3750ce5d6acce014a45711e515fccac283574"),
    ("openra_env/learning/abaddon_policy_campaign_cross_control_runtime_selector_generation2.py", "3ddf54f0fe8a37006d1e272bab62d14faa5904c0"),
    ("openra_env/learning/abaddon_policy_campaign_cross_control_runtime_selector_source_binding_review_generation2.py", "63b10239738980873bb26fc4f238b5c3e982a33e"),
    ("openra_env/learning/abaddon_policy_campaign_execution_adapter_generation2.py", "994d44d751c530619649322c72a65edf15f6a8c3"),
    ("openra_env/learning/abaddon_policy_campaign_isolated_workdir_allocator_generation2.py", "0890fb1e037ab21aa8312ab863e34cfc704e9ea2"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_activation_contract_generation2.py", "a3acb42280c334daa24a3b830105a04666fd603b"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_activation_evidence_generation2.py", "aac7964d9e80633535003b9f27066cac1bb4bac2"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_collector_contract_generation2.py", "8014431ad5329137e5ce12334d19d37c877a0b52"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_collector_implementation_generation2.py", "0003c24390194a4f621f13c6077e0604b9abcd98"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_observation_mechanics_generation2.py", "5fc94c056d1ad7de41b5d7156bce9b3f500f29ba"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_observation_primitive_review_generation2.py", "97e7b11ec4cb4214e7b9764121ec8059371dab51"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_observers_generation2.py", "cc4774e6aa934764c189cebd4040cd8ea4870517"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_path_inputs_generation2.py", "f65735c7820da9da0205388f1933b6aa9d6dd737"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_primitive_provider_contract_generation2.py", "807335ae5ee2892917d02acfa6434fd65151960f"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_primitive_provider_source_only_generation2.py", "f3b48e624172aeed81e28a6e24508533b7b13661"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_activation_binding_review_generation2.py", "9449b871cb745b67a7aa29f0d73de378f119a488"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_activation_evidence_collector_binding_generation2.py", "ddda2bac0570f99295b2c15b2000baed8478aa4c"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_adapter_binding_generation2.py", "4945f98a5dc12cff282c767013f81cac091e32e8"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_adapter_generation2.py", "29c4bfa11a841359b6c4f4083659c78c474d94ba"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_entrypoint_binding_generation2.py", "3950bbdd68f2fdc089f596f8159d480699af9982"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_entrypoint_generation2.py", "48e579c5d8ef0c05db93d637777d4882493cbf9d"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_invocation_acceptance_generation2.py", "1ced66b86edbda59b33bdc25a185842d7bd71418"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_collector_implementation_binding_generation2.py", "bcc12598161a9516cb002d6e1c4eead7e914a425"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_collector_reconciliation_generation2.py", "6c7dee5f94d32623cd7158868690fe0ac1d0c0c0"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_frozen_worktree_materializer_generation2.py", "8c6fb13480e03f094f63fdb753ec19a0ce223c80"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_frozen_worktree_materializer_source_binding_review_generation2.py", "3dcc325c431ec451a737b6e228c365ce1acb4f98"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_identity_receipt_validator_generation2.py", "d1586ba032d78296e200d5016560682b82ee599d"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_live_collection_backend_binding_generation2.py", "1a480133382dc878c79e110b8f6d8f30d0d7229d"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_live_collection_backend_generation2.py", "ee78726c7538aeb985ef00140d58792ec75fdcf3"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_live_identity_collector_contract_generation2.py", "db9fbb58f3d5870c77a796641afb1014acc19ee4"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_live_identity_collector_implementation_generation2.py", "49b1044a45cdb92d7077028b9856ef710f07b275"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_ollama_observer_binding_generation2.py", "58364a1d5d71aead9df6dc0fc61661a557131508"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_ollama_readonly_observer_generation2.py", "9b859e91b8833260a1af7e189ec5cd30d92d9451"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_portable_binding_attestation_generation2.py", "afdc0421958565e713795dfd0d3c4c683041cc37"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_post_admission_reconciliation_generation2.py", "fea52c8faf483e85f207ed65a384f34222d4c07a"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_provider_composition_generation2.py", "4efdf74ac7b140af5f29d5539eccde98694f4a3b"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_rootless_docker_image_backend_binding_generation2.py", "7075ded7a19454239b95a09e7b4630413124a796"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_rootless_docker_image_backend_generation2.py", "488497f723ad5bc5ca63b3b2d69cece26bddaaa5"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_runtime_image_readonly_observer_generation2.py", "8bc118684fb085361fa98dd80b6a1ee37edeb523"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_worktree_observer_generation2.py", "994f3be5d3344d6ac905c1f5fee9f9490fd4dd3f"),
    ("openra_env/learning/abaddon_policy_campaign_runtime_v2r13_worktree_provider_adapter_generation2.py", "7e6f628c64fe02db42bd6adee67d3965e6b1ae92"),
    ("openra_env/learning/apollyon_opponent_runtime_realizations.py", "0dbae61b0be96445e5fd6c23a07491a03f18b679"),
    ("openra_env/learning/apollyon_v2r13_portable_checkout.py", "077fbf5a2847d85113eb8fcba3904b02343ebfef"),
    ("openra_env/learning/apollyon_v8_campaign_runtime.py", "fd0e72767ba199e88af9e9eb2455c03ace027a14"),
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
        dependency_blobs=DEPENDENCY_BLOBS,
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


def _git_blob_oid(source: bytes) -> str:
    header = f"blob {len(source)}\0".encode("ascii")
    return hashlib.sha1(header + source).hexdigest()


def _local_dependency_paths(source: bytes, label: str) -> tuple[str, ...]:
    try:
        tree = ast.parse(source, filename=label)
    except (SyntaxError, UnicodeDecodeError) as exc:
        raise CapabilityGuardError(f"{label}: unreadable Python source: {exc}") from exc

    paths: set[str] = set()
    prefix = "openra_env.learning"
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            _require(node.level == 0, f"{label}: relative local import")
            module = node.module or ""
            if module == prefix:
                for alias in node.names:
                    _require(alias.name != "*", f"{label}: wildcard local import")
                    paths.add(f"openra_env/learning/{alias.name}.py")
            elif module.startswith(prefix + "."):
                suffix = module[len(prefix) + 1 :].replace(".", "/")
                paths.add(f"openra_env/learning/{suffix}.py")
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith(prefix + "."):
                    suffix = alias.name[len(prefix) + 1 :].replace(".", "/")
                    paths.add(f"openra_env/learning/{suffix}.py")
    return tuple(sorted(paths))


def _read_repository_source(repository_root: Path, path: str) -> bytes:
    relative = Path(path)
    _require(not relative.is_absolute() and ".." not in relative.parts, f"unsafe source path: {path}")
    candidate = repository_root / relative
    _require(not candidate.is_symlink(), f"symlink source rejected: {path}")
    _require(candidate.is_file(), f"source missing: {path}")
    _require(candidate.resolve().is_relative_to(repository_root), f"source escapes repository: {path}")
    return candidate.read_bytes()


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
        source = _read_repository_source(repository_root, spec.path)
        receipt = audit_source(source, spec)

        expected = dict(spec.dependency_blobs)
        _require(
            len(expected) == len(spec.dependency_blobs),
            f"{spec.path}: duplicate dependency manifest path",
        )
        visited = {spec.path}
        discovered: set[str] = set()
        pending = list(_local_dependency_paths(source, spec.path))

        while pending:
            dependency = pending.pop()
            if dependency in visited:
                continue
            visited.add(dependency)
            _require(
                dependency in expected,
                f"{spec.path}: unbound local dependency: {dependency}",
            )
            dependency_source = _read_repository_source(repository_root, dependency)
            actual_blob = _git_blob_oid(dependency_source)
            _require(
                actual_blob == expected[dependency],
                f"{spec.path}: dependency blob drift: {dependency}: {actual_blob}",
            )
            discovered.add(dependency)
            pending.extend(_local_dependency_paths(dependency_source, dependency))

        unused = sorted(set(expected) - discovered)
        _require(not unused, f"{spec.path}: unused dependency binding: {unused[0]}")
        receipt["dependency_count"] = len(discovered)
        receipt["dependencies"] = [
            {"path": path, "git_blob": expected[path]} for path in sorted(discovered)
        ]
        receipts.append(receipt)

    return {
        "schema": "void.war-college.generation2-static-capability-guard.v1",
        "target_count": len(receipts),
        "dependency_count": sum(int(row["dependency_count"]) for row in receipts),
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
