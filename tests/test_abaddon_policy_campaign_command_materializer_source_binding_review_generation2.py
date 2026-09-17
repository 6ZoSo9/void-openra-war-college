from __future__ import annotations

import ast
import hashlib
import importlib.util
from pathlib import Path


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "openra_env"
    / "learning"
    / "abaddon_policy_campaign_command_materializer_source_binding_review_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "2172c015b77e51d2d44cd1c3e37d1caac58d945daec0f0652594b9969756cc0b"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_command_materializer_source_binding_review_test",
        SOURCE,
    )
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


def test_contract_pins_exact_accepted_materializer_source():
    m = _load()
    out = m.command_materializer_source_binding_review_contract()
    assert out["command_materializer_git_blob"] == (
        "4836360e0d284454f815a2a2e32078d2565e6dea"
    )
    assert out["command_materializer_source_sha256"] == (
        "d02a23e7c0d3e4fc8a9c087e511a66d0d32f72b24e6702c62e9b886fb9dfee5d"
    )
    assert out["materializer_source_identity_pinned_by_git_blob"] is True
    assert out["materializer_source_identity_pinned_by_sha256"] is True


def test_review_is_separate_and_materializer_does_not_self_review():
    m = _load()
    deps = m._validate_dependencies()
    impl = deps["command_materializer_contract"]
    out = m.command_materializer_source_binding_review_contract()
    assert impl["command_materializer_reviewed"] is False
    assert out["materializer_source_is_not_self_bound"] is True
    assert out["separate_review_instrument"] is True
    assert out["command_materializer_reviewed"] is True


def test_historical_selector_review_identity_is_retained_without_census():
    m = _load()
    prior = m._validate_dependencies()["historical_selector_review"]
    assert prior["selector_review_git_blob"] == (
        "63b10239738980873bb26fc4f238b5c3e982a33e"
    )
    assert prior["selector_review_source_sha256"] == (
        "3a84514c668a5c40f76dd50349a1716e778dcd414f4c1a21d63a6435bfdde334"
    )
    assert prior["selector_review_frontier_preserved"] is True


def test_materializer_internal_dependency_blobs_remain_exact():
    m = _load()
    impl = m._validate_dependencies()["command_materializer_contract"]
    for field, blob in m.EXPECTED_MATERIALIZER_INTERNAL_DEPENDENCY_BLOBS.items():
        assert impl[field] == blob


def test_review_accepts_exact_command_and_pair_topology():
    m = _load()
    out = m.command_materializer_source_binding_review_contract()
    assert out["execution_descriptor_count"] == 36
    assert out["matched_pair_count"] == 18
    assert out["baseline_command_count"] == 18
    assert out["candidate_command_count"] == 18
    assert out["runtime_control_count"] == 4


def test_all_36_source_command_receipts_are_validated():
    m = _load()
    rows = m._validate_dependencies()["materialized_commands"]
    assert len(rows) == 36
    assert {row["execution_index"] for row in rows} == set(range(1, 37))
    assert len({row["command_sha256"] for row in rows}) == 36


def test_all_command_receipts_remain_unresolved_and_unexecuted():
    m = _load()
    rows = m._validate_dependencies()["materialized_commands"]
    for row in rows:
        assert row["argv_template_materialized"] is True
        assert row["argv_contains_unresolved_path_tokens"] is True
        assert row["path_bindings_resolved"] is False
        assert row["shell_command_materialized"] is False
        assert row["subprocess_invocation_materialized"] is False
        assert row["process_spawn_implemented"] is False
        assert row["command_execution_performed"] is False
        assert row["workdir_materialized"] is False
        assert row["workdir_created"] is False


def test_matched_pair_runner_argv_remains_identical():
    m = _load()
    rows = m._validate_dependencies()["materialized_commands"]
    for pair_slot in range(1, 19):
        pair = [row for row in rows if row["pair_slot"] == pair_slot]
        assert len(pair) == 2
        baseline = next(row for row in pair if row["arm"] == "baseline")
        candidate = next(row for row in pair if row["arm"] == "candidate")
        assert baseline["runner_argv"] == candidate["runner_argv"]


def test_matched_pair_runtime_identity_remains_identical():
    m = _load()
    rows = m._validate_dependencies()["materialized_commands"]
    for pair_slot in range(1, 19):
        pair = [row for row in rows if row["pair_slot"] == pair_slot]
        assert len(pair) == 2
        assert len({row["runtime_selection_key"] for row in pair}) == 1
        assert len({row["runtime_realization_sha256"] for row in pair}) == 1


def test_exact_four_runtime_controls_remain_represented():
    m = _load()
    rows = m._validate_dependencies()["materialized_commands"]
    assert {row["opponent_snapshot_id"] for row in rows} == m.EXPECTED_RUNTIME_IDS


def test_baseline_command_binding_is_exact_and_unresolved():
    m = _load()
    row = m.command_materializer.materialize_command(pair_slot=1, arm="baseline")
    assert row["argv_template"][:2] == ("python3", "<LEGACY_RUNNER_PATH>")
    binding = row["path_bindings"]["legacy_runner"]
    assert binding["sha256"] == (
        "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
    )
    assert binding["path_resolved"] is False
    assert binding["used_in_argv"] is True


def test_candidate_command_binding_is_exact_and_unresolved():
    m = _load()
    row = m.command_materializer.materialize_command(pair_slot=1, arm="candidate")
    assert row["argv_template"][:6] == (
        "python3",
        "<CANDIDATE_WRAPPER_PATH>",
        "--abaddon-candidate-genome",
        "<CANDIDATE_GENOME_PATH>",
        "--expected-candidate-file-sha256",
        "3fabbe9bc9b44830ee8e13e748d84ada881c6a3604f40c27609a953cabfd7768",
    )
    wrapper = row["path_bindings"]["candidate_wrapper"]
    genome = row["path_bindings"]["candidate_genome"]
    assert wrapper["git_blob"] == "61eaefee39ebd90df0ddd8c649d9f0f9b64b1776"
    assert genome["git_blob"] == "20091bff54edbb567127722fae81e5a5308737d2"
    assert wrapper["path_resolved"] is False
    assert genome["path_resolved"] is False


def test_candidate_wrapper_retains_exact_internal_legacy_runner_dependency():
    m = _load()
    row = m.command_materializer.materialize_command(pair_slot=1, arm="candidate")
    dep = row["path_bindings"]["candidate_wrapper_legacy_runner_dependency"]
    assert dep["consumer"] == "candidate_wrapper_internal_exact_dependency"
    assert dep["used_in_argv"] is False
    assert dep["sha256"] == (
        "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
    )


def test_review_closes_only_command_materializer_review_frontier():
    m = _load()
    out = m.command_materializer_source_binding_review_contract()
    assert out["command_materializer_implemented"] is True
    assert out["command_materializer_source_binding_present"] is True
    assert out["command_materializer_reviewed"] is True
    assert out["command_materializer_removes_only_its_execution_blocker"] is True


def test_execution_blockers_after_review_are_exact():
    m = _load()
    out = m.command_materializer_source_binding_review_contract()
    assert tuple(out["execution_materialization_blockers"]) == (
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
        "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
    )
    assert tuple(out["execution_materialization_source_blockers"]) == (
        "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
    )
    assert out["execution_materialization_remains_open"] is True


def test_workdir_frontier_remains_unimplemented():
    m = _load()
    out = m.command_materializer_source_binding_review_contract()
    assert out["isolated_workdir_allocator_implemented"] is False
    assert out["path_bindings_resolved"] is False


def test_runtime_authority_remains_separate_and_closed():
    m = _load()
    out = m.command_materializer_source_binding_review_contract()
    assert out["runtime_selection_preserved"] is True
    assert out["runtime_execution_authorized"] is False
    assert out["runtime_started"] is False
    assert out["process_spawn_implemented"] is False
    assert out["command_execution_performed"] is False


def test_next_source_gate_is_isolated_workdir_allocator():
    m = _load()
    out = m.command_materializer_source_binding_review_contract()
    assert out["next_gate"] == "ISOLATED_WORKDIR_ALLOCATOR_IMPLEMENTATION_REQUIRED"
    assert out["next_change_class"] == (
        "source_only_isolated_workdir_allocator_implementation"
    )


def test_review_contract_performs_no_live_or_runtime_action():
    m = _load()
    out = m.command_materializer_source_binding_review_contract()
    for field in (
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
    ):
        assert out[field] is False


def test_workdir_allocator_cannot_skip_review_frontier():
    m = _load()
    _expect_hold(
        m.CommandMaterializerSourceBindingReviewHold,
        "ISOLATED_WORKDIR_ALLOCATOR_IMPLEMENTATION_REQUIRED",
        m.allocate_isolated_workdir,
    )


def test_execution_advance_holds_at_next_source_gate():
    m = _load()
    _expect_hold(
        m.CommandMaterializerSourceBindingReviewHold,
        "ISOLATED_WORKDIR_ALLOCATOR_IMPLEMENTATION_REQUIRED",
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
            m.CommandMaterializerSourceBindingReviewHold,
            "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
            fn,
        )


def test_review_does_not_rewrite_materializer_contract():
    m = _load()
    before = m.command_materializer.command_materializer_contract()
    m.command_materializer_source_binding_review_contract()
    after = m.command_materializer.command_materializer_contract()
    assert before == after
    assert after["command_materializer_reviewed"] is False


def test_dependency_validation_cache_is_stable():
    m = _load()
    first = m._validate_dependencies_cached()
    second = m._validate_dependencies_cached()
    assert first is second
    assert len(first["materialized_commands"]) == 36


def test_reviewed_command_receipts_are_deterministic():
    m = _load()
    first = m._validate_dependencies()["materialized_commands"]
    second = m._validate_dependencies()["materialized_commands"]
    assert first == second


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
    forbidden_names = {
        "open",
        "exec",
        "eval",
        "__import__",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_names
