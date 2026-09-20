from __future__ import annotations

import ast
import hashlib
import importlib.util
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

import pytest

SOURCE = (
    Path(__file__).resolve().parents[1]
    / "openra_env"
    / "learning"
    / "abaddon_policy_campaign_runtime_v2r13_frozen_worktree_materializer_source_binding_review_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "b894b0b109fb943f444cfb3467249b7ed991fc8673967e271456c80d4df503fe"


@lru_cache(maxsize=1)
def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_v2r13_materializer_source_binding_review_test",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def _contract_cached():
    return _load().v2r13_frozen_worktree_materializer_source_binding_review_contract()


def _contract():
    return deepcopy(_contract_cached())


@lru_cache(maxsize=1)
def _dependencies_cached():
    return _load()._validate_dependencies()


def _dependencies():
    return deepcopy(_dependencies_cached())


def _expect_hold(exc_type, pattern, fn):
    try:
        fn()
    except exc_type as exc:
        assert pattern in str(exc)
        return
    raise AssertionError(f"expected hold containing {pattern!r}")


def test_source_sha_is_exact():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SOURCE_SHA256


def test_contract_pins_exact_accepted_materializer_source():
    m = _load()
    out = _contract()
    assert out["materializer_git_blob"] == "8c6fb13480e03f094f63fdb753ec19a0ce223c80"
    assert out["materializer_source_sha256"] == (
        "e1c189775b9b09d043f9e49d143d9f4ecab253ba5ea293fdf69820d0d2d86ff3"
    )
    assert out["materializer_source_identity_pinned_by_git_blob"] is True
    assert out["materializer_source_identity_pinned_by_sha256"] is True


def test_review_is_separate_and_does_not_rewrite_materializer_self_review():
    m = _load()
    deps = _dependencies()
    impl = deps["materializer_contract"]
    out = _contract()
    assert impl["frozen_worktree_materializer_reviewed"] is False
    assert out["materializer_source_is_not_self_bound"] is True
    assert out["separate_review_instrument"] is True
    assert out["frozen_worktree_materializer_reviewed"] is True


def test_review_accepts_exact_materializer_safety_frontier():
    m = _load()
    impl = _dependencies()["materializer_contract"]
    for field in (
        "source_worktree_add_detached_implemented",
        "engine_worktree_add_detached_implemented",
        "canonical_repository_snapshot_guard_implemented",
        "frozen_source_tree_verification_implemented",
        "materialized_commit_verification_implemented",
        "materialized_cleanliness_verification_implemented",
        "materialized_detached_head_verification_implemented",
        "partial_failure_rollback_implemented",
    ):
        assert impl[field] is True


def test_review_accepts_hardened_cleanup_frontier():
    m = _load()
    impl = _dependencies()["materializer_contract"]
    for field in (
        "cleanup_receipt_path_binding_implemented",
        "cleanup_registry_ownership_revalidation_implemented",
        "cleanup_commit_tree_clean_detached_revalidation_implemented",
        "cleanup_all_targets_preflight_before_removal_implemented",
        "cleanup_non_force_removal_implemented",
    ):
        assert impl[field] is True


def test_materialization_and_cleanup_authority_remain_explicit():
    m = _load()
    out = _contract()
    assert out["materialization_requires_explicit_authority"] is True
    assert out["cleanup_requires_explicit_authority"] is True
    assert out["review_materializer_invocation_implemented"] is False
    assert out["review_cleanup_invocation_implemented"] is False


def test_no_real_host_backend_or_auto_selection_is_admitted():
    m = _load()
    out = _contract()
    assert out["materializer_host_backend_bundled"] is False
    assert out["materializer_automatic_host_backend_selection"] is False


def test_materializer_review_closes_only_its_activation_blocker():
    m = _load()
    out = _contract()
    assert tuple(out["remaining_activation_blockers"]) == (
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["remaining_activation_blocker_count"] == 1
    assert out["runtime_authority_is_only_remaining_activation_gap"] is True


def test_activation_is_still_not_claimed_or_performed():
    m = _load()
    out = _contract()
    assert out["activation_source_review_frontier_complete"] is True
    assert out["activation_proven"] is False
    assert out["runtime_activation_performed"] is False
    assert out["runtime_activation_path_complete"] is False
    assert out["runtime_execution_authorized"] is False


def test_execution_materialization_remains_independently_open():
    m = _load()
    out = _contract()
    assert tuple(out["execution_materialization_blockers"]) == (
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
        "CROSS_CONTROL_RUNTIME_SELECTOR_NOT_IMPLEMENTED",
        "COMMAND_MATERIALIZER_NOT_IMPLEMENTED",
        "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
    )
    assert tuple(out["execution_materialization_source_blockers"]) == (
        "CROSS_CONTROL_RUNTIME_SELECTOR_NOT_IMPLEMENTED",
        "COMMAND_MATERIALIZER_NOT_IMPLEMENTED",
        "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
    )
    assert out["execution_materialization_remains_open"] is True


def test_all_v2r13_execution_descriptors_remain_ineligible_and_unauthorized():
    m = _load()
    rows = _dependencies()["v2r13_execution_descriptors"]
    assert len(rows) == 6
    assert all(row["eligible"] is False for row in rows)
    assert all(
        row["authority"]["runtime_execution_authorized"] is False
        for row in rows
    )


def test_next_source_gate_is_cross_control_runtime_selector():
    m = _load()
    out = _contract()
    assert out["next_gate"] == "CROSS_CONTROL_RUNTIME_SELECTOR_IMPLEMENTATION_REQUIRED"
    assert (
        out["next_change_class"]
        == "source_only_cross_control_runtime_selector_implementation"
    )


def test_review_contract_performs_no_live_or_runtime_action():
    m = _load()
    out = _contract()
    for field in (
        "review_materializer_invocation_implemented",
        "review_cleanup_invocation_implemented",
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
        "review_deployment_implemented",
        "review_void_chain_mutation_implemented",
        "review_wallet_or_funds_action_implemented",
    ):
        assert out[field] is False


def test_materialization_entrypoint_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13FrozenWorktreeMaterializerSourceBindingReviewHold,
        "GENERATION2_V2R13_FROZEN_WORKTREE_MATERIALIZATION_NOT_AUTHORIZED",
        lambda: m.materialize_frozen_worktrees(),
    )


def test_runtime_authorization_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13FrozenWorktreeMaterializerSourceBindingReviewHold,
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
        lambda: m.authorize_runtime_execution(),
    )


def test_execution_materialization_advance_holds_at_next_gate():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13FrozenWorktreeMaterializerSourceBindingReviewHold,
        "CROSS_CONTROL_RUNTIME_SELECTOR_IMPLEMENTATION_REQUIRED",
        lambda: m.advance_execution_materialization(),
    )


def test_historical_activation_review_is_retained_not_rewritten():
    m = _load()
    deps = _dependencies()
    prior = deps["historical_activation_review_contract"]
    assert tuple(prior["remaining_activation_blockers"]) == (
        "V2R13_FROZEN_WORKTREE_MATERIALIZER_NOT_REVIEWED",
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert prior["frozen_worktree_materializer_reviewed"] is False


def test_memoized_snapshots_are_copy_isolated():
    contract = _contract()
    contract["materializer_git_blob"] = "mutated"
    assert _contract()["materializer_git_blob"] == "8c6fb13480e03f094f63fdb753ec19a0ce223c80"

    dependencies = _dependencies()
    dependencies["v2r13_execution_descriptors"].clear()
    assert len(_dependencies()["v2r13_execution_descriptors"]) == 6


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
