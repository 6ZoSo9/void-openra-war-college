from __future__ import annotations

import ast
import hashlib
import importlib.util
import sys
from pathlib import Path

import pytest


REPO = Path(__file__).resolve().parents[1]
HISTORICAL = REPO / "fixtures/learning/scout-missions-v1/warm_start_runner_v1_4.py"
DERIVED = REPO / "fixtures/learning/scout-missions-v1/scout_repair_canary_derived_runner_v1.py"

HISTORICAL_GIT_BLOB = "132a5b2df3c3dbc82df7c0ebc6d457e5b77ffb51"
HISTORICAL_SHA256 = (
    "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
)
DERIVED_GIT_BLOB = "166fccd460387b1228702f0032639e99fe4d7f18"

PRESERVED_FUNCTIONS = (
    "find_mcv",
    "building_count",
    "choose_available",
    "combat_units",
    "visible_count",
    "military_damage_signature",
    "base_cell",
    "append_jsonl",
    "reconcile_pending",
    "assert_no_stale_pending",
    "host_step",
    "wait_for",
    "queue_structure",
    "queue_infantry",
    "stage_to_contact",
    "_safe_tool_suffix",
    "apollyon_tools_typed",
    "decision_to_commands_typed",
)

PRESERVED_CONSTANTS = (
    "BASE_RUNNER_SHA",
    "GENERATION",
    "IMAGE_ID",
    "ENGINE_COMMIT",
    "JOINT_ATTESTATION_SHA",
    "CURRICULUM_ID",
    "PREFERRED_INFANTRY",
    "INFANTRY_PRODUCTION",
    "PRODUCTION_NONUNIT_BLOCKLIST",
    "WARMSTART_UNSUPPORTED_STRUCTURES",
)


def _git_blob(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def _tree(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _functions(tree: ast.Module) -> dict[str, ast.FunctionDef]:
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }


def _constants(tree: ast.Module) -> dict[str, object]:
    result: dict[str, object] = {}
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
        ):
            try:
                result[node.targets[0].id] = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                pass
    return result


def _load():
    name = "_void_scout_repair_canary_derived_runner_v1"
    spec = importlib.util.spec_from_file_location(name, DERIVED)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_exact_historical_and_derived_source_identities() -> None:
    historical = HISTORICAL.read_bytes()
    derived = DERIVED.read_bytes()
    assert _git_blob(historical) == HISTORICAL_GIT_BLOB
    assert hashlib.sha256(historical).hexdigest() == HISTORICAL_SHA256
    assert _git_blob(derived) == DERIVED_GIT_BLOB


def test_warm_start_and_typed_host_validation_functions_are_byte_semantically_preserved() -> None:
    historical = _functions(_tree(HISTORICAL))
    derived = _functions(_tree(DERIVED))
    for name in PRESERVED_FUNCTIONS:
        assert name in historical
        assert name in derived
        assert ast.dump(historical[name], include_attributes=False) == ast.dump(
            derived[name],
            include_attributes=False,
        ), name


def test_runtime_engine_identity_constants_are_preserved() -> None:
    historical = _constants(_tree(HISTORICAL))
    derived = _constants(_tree(DERIVED))
    for name in PRESERVED_CONSTANTS:
        assert historical[name] == derived[name], name


def test_model_helper_and_model_inference_surface_is_removed() -> None:
    source = DERIVED.read_text(encoding="utf-8")
    for forbidden in (
        "helper.ollama_tool_call",
        "helper.start_ollama",
        "helper.cleanup",
        "base.APOLLYON_RUNNER",
        "base.APOLLYON_MODEL",
        "apollyon_decision_typed(",
        "systemctl",
        "import subprocess",
    ):
        assert forbidden not in source


def test_all_canary_training_labels_are_false() -> None:
    source = DERIVED.read_text(encoding="utf-8")
    assert '"training_candidate": True' not in source
    assert '"controller_rows_training_candidate": True' not in source
    assert '"agent_training_rows_begin_here": True' not in source
    assert '"training_candidate": False' in source
    assert '"controller_rows_training_candidate": False' in source
    assert '"agent_training_rows_begin_here": False' in source


def test_no_false_actual_apollyon_or_model_runtime_start_claim() -> None:
    source = DERIVED.read_text(encoding="utf-8")
    assert 'print("actual_apollyon=true")' not in source
    assert "apollyon_runtime_started_at_handoff=true" not in source
    assert 'print("actual_apollyon=false")' in source
    assert 'print("deterministic_non_model_opponent=true")' in source
    assert 'print("model_service_start_performed=false")' in source
    assert 'print("model_service_cleanup_performed=false")' in source


def test_canary_scope_is_fixed() -> None:
    module = _load()
    args = module.parse_args([])
    assert module.EXPERIMENT_NAMESPACE == "abaddon-scout-repair-canary-v1"
    assert module.CANARY_SEED == 1100292357
    assert args.seed == module.CANARY_SEED
    assert args.doctrine == "FEINTER"


def test_direct_execution_always_holds() -> None:
    module = _load()
    with pytest.raises(RuntimeError, match=module.NEXT_GATE):
        module.main()


def test_bound_runner_requires_launcher_authority_before_any_host_action() -> None:
    module = _load()
    with pytest.raises(RuntimeError, match=module.NEXT_GATE):
        module.run_bound_canary(
            launcher_authorized=False,
            accepted_war_college_commit="0" * 40,
            argv=[],
        )


def test_bound_runner_rejects_malformed_main_binding_before_host_action() -> None:
    module = _load()
    with pytest.raises(RuntimeError, match="lowercase 40-hex"):
        module.run_bound_canary(
            launcher_authorized=True,
            accepted_war_college_commit="not-a-commit",
            argv=[],
        )


def test_deterministic_adapter_is_the_only_controller_opponent_decision_call() -> None:
    tree = _tree(DERIVED)
    calls = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        target = node.func
        if isinstance(target, ast.Name):
            calls.append(target.id)
        elif isinstance(target, ast.Attribute):
            calls.append(target.attr)
    assert calls.count("deterministic_canary_decision") == 1
    assert "ollama_tool_call" not in calls


def test_direct_main_does_not_call_bound_runner() -> None:
    functions = _functions(_tree(DERIVED))
    direct = functions["main"]
    names = {
        node.func.id
        for node in ast.walk(direct)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert "run_bound_canary" not in names


def test_derived_runner_records_external_dormancy_as_unverified() -> None:
    source = DERIVED.read_text(encoding="utf-8")
    assert '"independent_post_run_dormancy_verified": False' in source
    assert "model_service_preflight_delegated_to_reviewed_launcher=true" in source


def test_source_does_not_mutate_training_or_policy_authority() -> None:
    source = DERIVED.read_text(encoding="utf-8")
    assert 'print("automatic_corpus_admission=false")' in source
    assert 'print("automatic_apollyon_weight_mutation=false")' in source
    assert 'print("automatic_abaddon_policy_promotion=false")' in source
    assert '"automatic_corpus_admission": False' in source
    assert '"automatic_apollyon_weight_mutation": False' in source
    assert '"automatic_abaddon_policy_promotion": False' in source
