from __future__ import annotations

import ast
import hashlib
import importlib.util
from pathlib import Path

SOURCE = (
    Path(__file__).resolve().parents[1]
    / "openra_env"
    / "learning"
    / "abaddon_policy_campaign_isolated_workdir_allocator_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "7683a3e244f7d7a661816c48aef773abbbe2b805dc2cf95391ad1ab28ff986fb"

def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_g2_isolated_workdir_allocator_test", SOURCE
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

def test_contract_pins_exact_accepted_review_and_materializer():
    m = _load()
    out = m.isolated_workdir_allocator_contract()
    assert out["materializer_review_git_blob"] == "dee3750ce5d6acce014a45711e515fccac283574"
    assert out["materializer_review_source_sha256"] == (
        "2172c015b77e51d2d44cd1c3e37d1caac58d945daec0f0652594b9969756cc0b"
    )
    assert out["command_materializer_git_blob"] == "4836360e0d284454f815a2a2e32078d2565e6dea"

def test_review_frontier_constants_are_exact():
    m = _load()
    out = m._validate_review_frontier_constants()
    assert out["command_materializer_reviewed_by_separate_accepted_source"] is True
    assert tuple(out["pre_allocator_blockers"]) == (
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
        "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
    )
    assert tuple(out["pre_allocator_source_blockers"]) == (
        "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
    )

def test_exact_36_allocations_and_18_pairs():
    m = _load()
    rows = m.all_isolated_workdir_allocations()
    assert len(rows) == 36
    assert len({row["pair_slot"] for row in rows}) == 18
    assert sum(row["arm"] == "baseline" for row in rows) == 18
    assert sum(row["arm"] == "candidate" for row in rows) == 18

def test_all_allocation_namespaces_are_unique():
    m = _load()
    rows = m.all_isolated_workdir_allocations()
    assert len({row["namespace_key"] for row in rows}) == 36
    assert len({row["workdir_path_template"] for row in rows}) == 36
    assert len({row["allocation_sha256"] for row in rows}) == 36

def test_workdir_token_shape_is_exact_for_all_rows():
    m = _load()
    for row in m.all_isolated_workdir_allocations():
        expected = f"generation2/pair-{row['pair_slot']:02d}/{row['arm']}"
        assert row["workdir_token"] == expected
        assert tuple(row["workdir_token_components"]) == tuple(expected.split("/"))

def test_root_token_remains_unresolved():
    m = _load()
    out = m.isolated_workdir_allocator_contract()
    assert out["workdir_root_token"] == "<GENERATION2_ISOLATED_WORKDIR_ROOT>"
    assert out["unresolved_root_token_required"] is True
    assert out["host_path_resolved"] is False
    assert out["filesystem_path_resolved"] is False

def test_path_templates_are_deterministic_and_tokenized():
    m = _load()
    for row in m.all_isolated_workdir_allocations():
        assert row["workdir_path_template"] == (
            "<GENERATION2_ISOLATED_WORKDIR_ROOT>/" + row["workdir_token"]
        )
        assert row["pair_root_template"] == (
            f"<GENERATION2_ISOLATED_WORKDIR_ROOT>/generation2/pair-{row['pair_slot']:02d}"
        )

def test_matched_pair_shares_pair_root_but_not_workdir_template():
    m = _load()
    for pair_slot in range(1, 19):
        baseline = m.allocate_isolated_workdir(pair_slot=pair_slot, arm="baseline")
        candidate = m.allocate_isolated_workdir(pair_slot=pair_slot, arm="candidate")
        assert baseline["pair_root_template"] == candidate["pair_root_template"]
        assert baseline["workdir_path_template"] != candidate["workdir_path_template"]
        assert baseline["namespace_key"] != candidate["namespace_key"]

def test_allocator_accepts_only_canonical_command_receipts():
    m = _load()
    canonical = m.command_materializer.materialize_command(pair_slot=1, arm="baseline")
    out = m.allocate_from_materialized_command(canonical)
    assert out["pair_slot"] == 1 and out["arm"] == "baseline"
    tampered = dict(canonical)
    tampered["workdir_token"] = "generation2/pair-01/candidate"
    _expect_hold(
        m.IsolatedWorkdirAllocatorHold,
        "not canonical accepted materializer output",
        lambda: m.allocate_from_materialized_command(tampered),
    )

def test_invalid_pair_and_arm_fail_closed():
    m = _load()
    _expect_hold(
        m.IsolatedWorkdirAllocatorHold,
        "canonical accepted command not found",
        lambda: m.allocate_isolated_workdir(pair_slot=19, arm="baseline"),
    )
    _expect_hold(
        m.IsolatedWorkdirAllocatorHold,
        "unsupported arm",
        lambda: m.allocate_isolated_workdir(pair_slot=1, arm="other"),
    )

def test_allocation_receipt_is_source_only_not_filesystem_action():
    m = _load()
    row = m.allocate_isolated_workdir(pair_slot=1, arm="candidate")
    assert row["isolated_workdir_allocator_implemented"] is True
    assert row["allocation_receipt_materialized"] is True
    assert row["allocation_is_source_only"] is True
    assert row["workdir_path_template_materialized"] is True
    assert row["workdir_materialized"] is False
    assert row["workdir_created"] is False
    assert row["filesystem_action_performed"] is False
    assert row["directory_creation_implemented"] is False

def test_command_path_bindings_remain_unresolved_after_allocation():
    m = _load()
    row = m.allocate_isolated_workdir(pair_slot=1, arm="candidate")
    assert row["path_bindings_resolved"] is False
    assert row["host_path_resolved"] is False
    assert row["filesystem_path_resolved"] is False

def test_runtime_selection_is_preserved():
    m = _load()
    for pair_slot in range(1, 19):
        baseline = m.allocate_isolated_workdir(pair_slot=pair_slot, arm="baseline")
        candidate = m.allocate_isolated_workdir(pair_slot=pair_slot, arm="candidate")
        assert baseline["runtime_selection_key"] == candidate["runtime_selection_key"]
        assert baseline["runtime_realization_sha256"] == candidate["runtime_realization_sha256"]
        assert baseline["runtime_selection_preserved"] is True
        assert candidate["runtime_selection_preserved"] is True

def test_all_four_runtime_controls_remain_present():
    m = _load()
    ids = {row["opponent_snapshot_id"] for row in m.all_isolated_workdir_allocations()}
    assert ids == {
        "apollyon-v13-v14-promoted",
        "apollyon-v13-v10-promoted",
        "apollyon-v2r13-qualified-predecessor",
        "apollyon-v3-v8-accepted-model-control",
    }

def test_allocator_removes_only_allocator_execution_blocker():
    m = _load()
    row = m.allocate_isolated_workdir(pair_slot=1, arm="baseline")
    assert tuple(row["remaining_blockers"]) == (
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
    )

def test_allocator_closes_source_blocker_frontier():
    m = _load()
    row = m.allocate_isolated_workdir(pair_slot=1, arm="baseline")
    assert tuple(row["remaining_source_blockers"]) == ()
    assert tuple(m.isolated_workdir_allocator_contract()["post_allocator_source_blockers"]) == ()

def test_runtime_and_command_actions_remain_false():
    m = _load()
    row = m.allocate_isolated_workdir(pair_slot=1, arm="candidate")
    for field in (
        "process_spawn_implemented",
        "command_execution_performed",
        "runtime_started",
        "runtime_execution_authorized",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        assert row[field] is False, field

def test_contract_reports_exact_topology():
    m = _load()
    out = m.isolated_workdir_allocator_contract()
    assert out["execution_descriptor_count"] == 36
    assert out["matched_pair_count"] == 18
    assert out["baseline_allocation_count"] == 18
    assert out["candidate_allocation_count"] == 18
    assert out["unique_namespace_count"] == 36
    assert out["unique_path_template_count"] == 36

def test_contract_boundary_flags_remain_false():
    m = _load()
    out = m.isolated_workdir_allocator_contract()
    for field in (
        "host_path_resolved",
        "filesystem_path_resolved",
        "workdir_materialized",
        "workdir_created",
        "filesystem_action_performed",
        "directory_creation_implemented",
        "path_bindings_resolved",
        "runtime_execution_authorized",
        "runtime_started",
        "process_spawn_implemented",
        "command_execution_performed",
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

def test_next_gate_is_allocator_source_binding_review():
    m = _load()
    out = m.isolated_workdir_allocator_contract()
    assert out["next_gate"] == "ISOLATED_WORKDIR_ALLOCATOR_SOURCE_BINDING_REVIEW_REQUIRED"
    assert out["next_change_class"] == (
        "source_only_isolated_workdir_allocator_source_binding_review"
    )

def test_execution_advance_holds_at_source_review_gate():
    m = _load()
    _expect_hold(
        m.IsolatedWorkdirAllocatorHold,
        "ISOLATED_WORKDIR_ALLOCATOR_SOURCE_BINDING_REVIEW_REQUIRED",
        m.advance_execution_materialization,
    )

def test_directory_creation_and_runtime_entrypoints_remain_authority_held():
    m = _load()
    for fn in (
        m.create_isolated_workdir,
        m.execute_materialized_command,
        m.start_runtime,
        m.authorize_runtime_execution,
    ):
        _expect_hold(
            m.IsolatedWorkdirAllocatorHold,
            "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
            fn,
        )

def test_allocator_contract_does_not_rewrite_command_materializer():
    m = _load()
    before = m.command_materializer.command_materializer_contract()
    m.isolated_workdir_allocator_contract()
    after = m.command_materializer.command_materializer_contract()
    assert before == after
    assert after["isolated_workdir_allocator_implemented"] is False

def test_accepted_command_cache_is_stable():
    m = _load()
    first = m._accepted_commands_cached()
    second = m._accepted_commands_cached()
    assert first is second
    assert len(first) == 36

def test_allocations_are_deterministic():
    m = _load()
    assert m.all_isolated_workdir_allocations() == m.all_isolated_workdir_allocations()

def test_static_source_has_no_direct_host_io_or_execution_surface():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    forbidden_import_roots = {
        "os","subprocess","socket","requests","urllib","http","httpx",
        "asyncio","multiprocessing","ctypes","pathlib",
    }
    forbidden_names = {"open","exec","eval","__import__"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".",1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".",1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_names
