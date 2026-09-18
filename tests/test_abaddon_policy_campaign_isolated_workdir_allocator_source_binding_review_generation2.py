from __future__ import annotations

import ast
import hashlib
import importlib.util
from pathlib import Path


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "openra_env"
    / "learning"
    / "abaddon_policy_campaign_isolated_workdir_allocator_source_binding_review_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "3985b0fbc74a25e29d44ae09d9c52c051ebb9044058d1bdd93ba6c9d1cca5761"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_g2_isolated_workdir_allocator_source_binding_review_test",
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


def test_contract_pins_exact_accepted_allocator_source_and_test():
    m = _load()
    out = m.isolated_workdir_allocator_source_binding_review_contract()
    assert out["allocator_git_blob"] == "0890fb1e037ab21aa8312ab863e34cfc704e9ea2"
    assert out["allocator_source_sha256"] == (
        "7683a3e244f7d7a661816c48aef773abbbe2b805dc2cf95391ad1ab28ff986fb"
    )
    assert out["allocator_test_git_blob"] == "8eb3fcc0657211cf599388e132487bc45e2785ea"
    assert out["allocator_test_sha256"] == (
        "3d8eb684c6644901dbb7eb1c53cf04f5fb9bcf714fbd6ce072ae26d5cd459e6f"
    )


def test_review_is_separate_and_allocator_does_not_self_review():
    m = _load()
    accepted = m.allocator.isolated_workdir_allocator_contract()
    reviewed = m.isolated_workdir_allocator_source_binding_review_contract()
    assert accepted["isolated_workdir_allocator_reviewed"] is False
    assert reviewed["isolated_workdir_allocator_reviewed"] is True
    assert reviewed["allocator_source_is_not_self_bound"] is True
    assert reviewed["separate_review_instrument"] is True


def test_dependency_cache_is_stable():
    m = _load()
    first = m._validate_dependencies_cached()
    second = m._validate_dependencies_cached()
    assert first is second
    assert first["allocation_receipt_count"] == 36


def test_all_36_allocation_receipts_are_validated():
    m = _load()
    out = m._validate_dependencies()
    assert len(out["allocations"]) == 36
    assert out["allocation_receipt_count"] == 36


def test_exact_18_matched_pairs_are_validated():
    m = _load()
    out = m._validate_dependencies()
    rows = out["allocations"]
    assert out["matched_pair_count"] == 18
    assert len({row["pair_slot"] for row in rows}) == 18
    for pair_slot in range(1, 19):
        arms = {row["arm"] for row in rows if row["pair_slot"] == pair_slot}
        assert arms == {"baseline", "candidate"}


def test_exact_baseline_candidate_counts():
    m = _load()
    out = m._validate_dependencies()
    assert out["baseline_allocation_count"] == 18
    assert out["candidate_allocation_count"] == 18


def test_all_namespaces_are_unique():
    m = _load()
    out = m._validate_dependencies()
    rows = out["allocations"]
    assert out["unique_namespace_count"] == 36
    assert len({row["namespace_key"] for row in rows}) == 36


def test_all_path_templates_are_unique():
    m = _load()
    out = m._validate_dependencies()
    rows = out["allocations"]
    assert out["unique_path_template_count"] == 36
    assert len({row["workdir_path_template"] for row in rows}) == 36


def test_all_allocation_digests_are_unique():
    m = _load()
    out = m._validate_dependencies()
    rows = out["allocations"]
    assert out["unique_allocation_digest_count"] == 36
    assert len({row["allocation_sha256"] for row in rows}) == 36


def test_root_token_remains_unresolved():
    m = _load()
    out = m.isolated_workdir_allocator_source_binding_review_contract()
    assert out["workdir_root_token"] == "<GENERATION2_ISOLATED_WORKDIR_ROOT>"
    assert out["unresolved_root_token_preserved"] is True
    assert out["host_path_resolved"] is False
    assert out["filesystem_path_resolved"] is False


def test_workdir_tokens_and_templates_are_canonical():
    m = _load()
    for row in m._validate_dependencies()["allocations"]:
        token = f"generation2/pair-{row['pair_slot']:02d}/{row['arm']}"
        assert row["workdir_token"] == token
        assert row["workdir_path_template"] == (
            "<GENERATION2_ISOLATED_WORKDIR_ROOT>/" + token
        )


def test_matched_pair_roots_are_shared_but_workdirs_are_isolated():
    m = _load()
    rows = m._validate_dependencies()["allocations"]
    for pair_slot in range(1, 19):
        pair = {row["arm"]: row for row in rows if row["pair_slot"] == pair_slot}
        assert pair["baseline"]["pair_root_template"] == pair["candidate"]["pair_root_template"]
        assert pair["baseline"]["workdir_path_template"] != pair["candidate"]["workdir_path_template"]
        assert pair["baseline"]["namespace_key"] != pair["candidate"]["namespace_key"]


def test_matched_pair_runtime_identity_is_preserved():
    m = _load()
    rows = m._validate_dependencies()["allocations"]
    for pair_slot in range(1, 19):
        pair = {row["arm"]: row for row in rows if row["pair_slot"] == pair_slot}
        assert pair["baseline"]["runtime_selection_key"] == pair["candidate"]["runtime_selection_key"]
        assert pair["baseline"]["runtime_realization_sha256"] == pair["candidate"]["runtime_realization_sha256"]


def test_exact_four_runtime_controls_remain_represented():
    m = _load()
    rows = m._validate_dependencies()["allocations"]
    assert {row["opponent_snapshot_id"] for row in rows} == {
        "apollyon-v13-v14-promoted",
        "apollyon-v13-v10-promoted",
        "apollyon-v2r13-qualified-predecessor",
        "apollyon-v3-v8-accepted-model-control",
    }


def test_source_frontier_is_closed_after_review():
    m = _load()
    out = m.isolated_workdir_allocator_source_binding_review_contract()
    assert tuple(out["execution_materialization_source_blockers"]) == ()
    assert out["source_frontier_closed"] is True


def test_runtime_authority_is_the_only_execution_blocker():
    m = _load()
    out = m.isolated_workdir_allocator_source_binding_review_contract()
    assert tuple(out["execution_materialization_blockers"]) == (
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
    )


def test_next_gate_is_runtime_execution_authorization():
    m = _load()
    out = m.isolated_workdir_allocator_source_binding_review_contract()
    assert out["next_gate"] == "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED"


def test_next_change_class_is_runtime_execution_authorization():
    m = _load()
    out = m.isolated_workdir_allocator_source_binding_review_contract()
    assert out["next_change_class"] == "runtime_execution_authorization"


def test_review_performs_no_filesystem_or_workdir_action():
    m = _load()
    out = m.isolated_workdir_allocator_source_binding_review_contract()
    for field in (
        "host_path_resolved",
        "filesystem_path_resolved",
        "path_bindings_resolved",
        "workdir_materialized",
        "workdir_created",
        "filesystem_action_performed",
        "directory_creation_implemented",
        "review_filesystem_observation_implemented",
    ):
        assert out[field] is False, field


def test_review_performs_no_runtime_or_command_action():
    m = _load()
    out = m.isolated_workdir_allocator_source_binding_review_contract()
    for field in (
        "runtime_execution_authorized",
        "runtime_started",
        "process_spawn_implemented",
        "command_execution_performed",
        "review_subprocess_execution_implemented",
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
        assert out[field] is False, field


def test_review_performs_no_live_network_git_or_container_observation():
    m = _load()
    out = m.isolated_workdir_allocator_source_binding_review_contract()
    for field in (
        "review_live_observation_implemented",
        "review_git_query_implemented",
        "review_network_request_implemented",
        "review_ollama_request_implemented",
        "review_docker_command_implemented",
    ):
        assert out[field] is False, field


def test_runtime_entrypoints_remain_authority_held():
    m = _load()
    for fn in (
        m.advance_execution_materialization,
        m.create_isolated_workdir,
        m.execute_materialized_command,
        m.start_runtime,
        m.authorize_runtime_execution,
    ):
        _expect_hold(
            m.IsolatedWorkdirAllocatorSourceBindingReviewHold,
            "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
            fn,
        )


def test_review_does_not_rewrite_allocator_contract():
    m = _load()
    before = m.allocator.isolated_workdir_allocator_contract()
    m.isolated_workdir_allocator_source_binding_review_contract()
    after = m.allocator.isolated_workdir_allocator_contract()
    assert before == after
    assert after["isolated_workdir_allocator_reviewed"] is False


def test_review_is_deterministic():
    m = _load()
    assert (
        m.isolated_workdir_allocator_source_binding_review_contract()
        == m.isolated_workdir_allocator_source_binding_review_contract()
    )


def test_review_dependency_copy_does_not_mutate_cache():
    m = _load()
    first = m._validate_dependencies()
    first["allocations"][0]["pair_slot"] = 999
    second = m._validate_dependencies()
    assert second["allocations"][0]["pair_slot"] != 999


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
