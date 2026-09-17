from __future__ import annotations

import ast
import hashlib
import importlib.util
from pathlib import Path


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "openra_env"
    / "learning"
    / "abaddon_policy_campaign_command_materializer_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "d02a23e7c0d3e4fc8a9c087e511a66d0d32f72b24e6702c62e9b886fb9dfee5d"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location("_void_g2_command_materializer_v3_test", SOURCE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _expect_hold(exc_type, pattern, fn):
    try:
        fn()
    except exc_type as exc:
        assert pattern in str(exc), (pattern, str(exc))
        return
    raise AssertionError(f"expected hold containing {pattern!r}")


def test_source_sha_is_exact():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SOURCE_SHA256


def test_review_frontier_uses_constants_not_expensive_review_census():
    m = _load()
    out = m._validate_review_frontier_constants()
    assert out["selector_reviewed_by_separate_accepted_source"] is True
    assert out["runtime_execution_authorized"] is False


def test_contract_pins_exact_accepted_dependencies():
    m = _load()
    out = m.command_materializer_contract()
    assert out["selector_review_git_blob"] == "63b10239738980873bb26fc4f238b5c3e982a33e"
    assert out["selector_git_blob"] == "3ddf54f0fe8a37006d1e272bab62d14faa5904c0"
    assert out["execution_adapter_git_blob"] == "994d44d751c530619649322c72a65edf15f6a8c3"
    assert out["orchestrator_git_blob"] == "8948b53d002e5d7e48a7aef2ec10ff5d690f5a1c"


def test_contract_pins_exact_wrapper_and_fixture():
    m = _load()
    out = m.command_materializer_contract()
    assert out["candidate_wrapper_git_blob"] == "61eaefee39ebd90df0ddd8c649d9f0f9b64b1776"
    assert out["candidate_wrapper_source_sha256"] == (
        "686f88836e73acf9c78bfc1417db735b11100c07c34ce8da291047edd99eea9f"
    )
    assert out["candidate_fixture_git_blob"] == "20091bff54edbb567127722fae81e5a5308737d2"
    assert out["candidate_fixture_sha256"] == (
        "3fabbe9bc9b44830ee8e13e748d84ada881c6a3604f40c27609a953cabfd7768"
    )


def test_accepted_ledger_is_cached_once():
    m = _load()
    first = m._ledger_index_cached()
    second = m._ledger_index_cached()
    assert first is second
    assert len(first) == 36


def test_exact_36_commands_and_18_pairs():
    m = _load()
    rows = m.all_materialized_commands()
    assert len(rows) == 36
    assert len({row["pair_slot"] for row in rows}) == 18
    assert sum(row["arm"] == "baseline" for row in rows) == 18
    assert sum(row["arm"] == "candidate" for row in rows) == 18


def test_runner_flag_order_is_exact():
    m = _load()
    assert m.RUNNER_FLAGS == (
        "--seed",
        "--doctrine",
        "--rounds",
        "--ticks-per-round",
        "--starter-infantry",
        "--staging-max-ticks",
    )


def test_all_commands_are_deterministic():
    m = _load()
    first = m.all_materialized_commands()
    second = m.all_materialized_commands()
    assert first == second
    assert len({row["command_sha256"] for row in first}) == 36


def test_baseline_uses_legacy_runner_token():
    m = _load()
    out = m.materialize_command(pair_slot=1, arm="baseline")
    assert out["argv_template"][:2] == ("python3", "<LEGACY_RUNNER_PATH>")
    assert out["path_bindings"]["legacy_runner"]["sha256"] == (
        "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
    )


def test_candidate_uses_reviewed_wrapper_prefix():
    m = _load()
    out = m.materialize_command(pair_slot=1, arm="candidate")
    assert out["argv_template"][:6] == (
        "python3",
        "<CANDIDATE_WRAPPER_PATH>",
        "--abaddon-candidate-genome",
        "<CANDIDATE_GENOME_PATH>",
        "--expected-candidate-file-sha256",
        "3fabbe9bc9b44830ee8e13e748d84ada881c6a3604f40c27609a953cabfd7768",
    )


def test_candidate_wrapper_binding_is_exact_and_unresolved():
    m = _load()
    binding = m.materialize_command(pair_slot=1, arm="candidate")["path_bindings"]["candidate_wrapper"]
    assert binding["relative_path"] == "tools/abaddon_policy_candidate_duel_wrapper.py"
    assert binding["git_blob"] == "61eaefee39ebd90df0ddd8c649d9f0f9b64b1776"
    assert binding["path_resolved"] is False


def test_candidate_genome_binding_is_exact_and_unresolved():
    m = _load()
    binding = m.materialize_command(pair_slot=1, arm="candidate")["path_bindings"]["candidate_genome"]
    assert binding["relative_path"] == (
        "fixtures/learning/abaddon-policy-genome-generation-2-candidate-252.json"
    )
    assert binding["git_blob"] == "20091bff54edbb567127722fae81e5a5308737d2"
    assert binding["semantic_genome_sha256"] == (
        "8253ea5f1b3a709c8d64fb0432d13ac1c52ee82678e2f3b0ec730fe23d603089"
    )
    assert binding["path_resolved"] is False


def test_candidate_retains_wrapper_legacy_runner_dependency():
    m = _load()
    binding = (
        m.materialize_command(pair_slot=1, arm="candidate")
        ["path_bindings"]["candidate_wrapper_legacy_runner_dependency"]
    )
    assert binding["used_in_argv"] is False
    assert binding["consumer"] == "candidate_wrapper_internal_exact_dependency"


def test_matched_pair_runner_argv_is_identical():
    m = _load()
    for pair_slot in range(1, 19):
        baseline = m.materialize_command(pair_slot=pair_slot, arm="baseline")
        candidate = m.materialize_command(pair_slot=pair_slot, arm="candidate")
        assert baseline["runner_argv"] == candidate["runner_argv"]


def test_all_four_runtime_controls_remain_present():
    m = _load()
    ids = {row["opponent_snapshot_id"] for row in m.all_materialized_commands()}
    assert ids == {
        "apollyon-v13-v14-promoted",
        "apollyon-v13-v10-promoted",
        "apollyon-v2r13-qualified-predecessor",
        "apollyon-v3-v8-accepted-model-control",
    }


def test_matched_pair_runtime_identity_is_preserved():
    m = _load()
    for pair_slot in range(1, 19):
        baseline = m.materialize_command(pair_slot=pair_slot, arm="baseline")
        candidate = m.materialize_command(pair_slot=pair_slot, arm="candidate")
        assert baseline["runtime_selection_key"] == candidate["runtime_selection_key"]
        assert baseline["runtime_realization_sha256"] == candidate["runtime_realization_sha256"]


def test_runtime_selection_is_preserved_without_runtime_start():
    m = _load()
    out = m.materialize_command(pair_slot=1, arm="candidate")
    assert out["runtime_selection_preserved"] is True
    assert out["runtime_selection_recomputed_by_selector"] is False
    assert out["runtime_started"] is False
    assert out["runtime_execution_authorized"] is False


def test_command_materialization_removes_only_command_blocker():
    m = _load()
    out = m.materialize_command(pair_slot=1, arm="baseline")
    assert tuple(out["remaining_blockers"]) == (
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
        "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
    )
    assert tuple(out["remaining_source_blockers"]) == (
        "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
    )


def test_workdir_remains_unmaterialized():
    m = _load()
    out = m.materialize_command(pair_slot=1, arm="candidate")
    assert out["workdir_materialized"] is False
    assert out["workdir_created"] is False
    assert out["path_bindings_resolved"] is False
    assert out["argv_contains_unresolved_path_tokens"] is True


def test_no_shell_or_subprocess_surface_is_materialized():
    m = _load()
    out = m.materialize_command(pair_slot=1, arm="candidate")
    assert out["shell_command_materialized"] is False
    assert out["subprocess_invocation_materialized"] is False
    assert out["process_spawn_implemented"] is False
    assert out["command_execution_performed"] is False


def test_contract_boundary_flags_remain_false():
    m = _load()
    out = m.command_materializer_contract()
    for field in (
        "runtime_execution_authorized",
        "runtime_started",
        "process_spawn_implemented",
        "command_execution_performed",
        "shell_command_materialized",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        assert out[field] is False, field


def test_invalid_pair_fails_closed():
    m = _load()
    _expect_hold(
        m.CommandMaterializerHold,
        "canonical ledger row not found",
        lambda: m.materialize_command(pair_slot=19, arm="baseline"),
    )


def test_invalid_arm_fails_closed():
    m = _load()
    _expect_hold(
        m.CommandMaterializerHold,
        "unsupported arm",
        lambda: m.materialize_command(pair_slot=1, arm="other"),
    )


def test_next_gate_is_source_binding_review():
    m = _load()
    out = m.command_materializer_contract()
    assert out["next_gate"] == "COMMAND_MATERIALIZER_SOURCE_BINDING_REVIEW_REQUIRED"
    assert out["next_change_class"] == "source_only_command_materializer_source_binding_review"


def test_workdir_allocator_cannot_skip_review():
    m = _load()
    _expect_hold(
        m.CommandMaterializerHold,
        "COMMAND_MATERIALIZER_SOURCE_BINDING_REVIEW_REQUIRED",
        m.allocate_isolated_workdir,
    )
    _expect_hold(
        m.CommandMaterializerHold,
        "COMMAND_MATERIALIZER_SOURCE_BINDING_REVIEW_REQUIRED",
        m.advance_execution_materialization,
    )


def test_runtime_entrypoints_remain_authority_held():
    m = _load()
    for fn in (
        m.execute_materialized_command,
        m.start_runtime,
        m.authorize_runtime_execution,
    ):
        _expect_hold(
            m.CommandMaterializerHold,
            "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
            fn,
        )


def test_static_source_has_no_direct_host_io_or_execution_surface():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    forbidden_import_roots = {
        "os",
        "subprocess",
        "socket",
        "requests",
        "urllib",
        "http",
        "httpx",
        "asyncio",
        "multiprocessing",
        "ctypes",
        "pathlib",
    }
    forbidden_names = {"open", "exec", "eval", "__import__"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_names
