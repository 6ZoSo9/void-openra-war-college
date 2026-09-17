from __future__ import annotations

import ast
import hashlib
import importlib.util
from pathlib import Path


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "openra_env"
    / "learning"
    / "abaddon_policy_campaign_cross_control_runtime_selector_source_binding_review_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "3a84514c668a5c40f76dd50349a1716e778dcd414f4c1a21d63a6435bfdde334"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_cross_control_selector_source_binding_review_test",
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


def test_contract_pins_exact_accepted_selector_source():
    m = _load()
    out = m.cross_control_runtime_selector_source_binding_review_contract()
    assert out["selector_git_blob"] == "3ddf54f0fe8a37006d1e272bab62d14faa5904c0"
    assert out["selector_source_sha256"] == (
        "19cd2c02e4232cee01e31286eee545237d61d7839542914899a1abf016fe26f4"
    )
    assert out["selector_source_identity_pinned_by_git_blob"] is True
    assert out["selector_source_identity_pinned_by_sha256"] is True


def test_review_is_separate_and_selector_does_not_self_review():
    m = _load()
    deps = m._validate_dependencies()
    impl = deps["selector_contract"]
    out = m.cross_control_runtime_selector_source_binding_review_contract()
    assert impl["cross_control_runtime_selector_reviewed"] is False
    assert out["selector_source_is_not_self_bound"] is True
    assert out["separate_review_instrument"] is True
    assert out["cross_control_runtime_selector_reviewed"] is True


def test_selector_internal_dependency_blobs_remain_exact():
    m = _load()
    impl = m._validate_dependencies()["selector_contract"]
    expected = m.EXPECTED_SELECTOR_INTERNAL_DEPENDENCY_BLOBS
    for field, blob in expected.items():
        assert impl[field] == blob


def test_selector_review_accepts_exact_four_control_semantics():
    m = _load()
    out = m.cross_control_runtime_selector_source_binding_review_contract()
    assert out["selection_key"] == "opponent_snapshot_id"
    assert out["runtime_class_is_not_selection_key"] is True
    assert out["reviewed_runtime_count"] == 4
    assert out["reviewed_runtime_class_count"] == 3


def test_selector_review_accepts_exact_descriptor_and_pair_topology():
    m = _load()
    out = m.cross_control_runtime_selector_source_binding_review_contract()
    assert out["execution_descriptor_count"] == 36
    assert out["matched_pair_count"] == 18
    assert out["selector_accepts_only_canonical_execution_descriptors"] is True
    assert out["selector_preserves_matched_pair_runtime_identity"] is True


def test_all_selected_descriptors_remain_ineligible_and_unauthorized():
    m = _load()
    rows = m._validate_dependencies()["selected_execution_descriptors"]
    assert len(rows) == 36
    assert all(row["eligible"] is False for row in rows)
    assert all(
        row["authority"]["runtime_execution_authorized"] is False
        for row in rows
    )
    assert all(row["runtime"]["started"] is False for row in rows)


def test_each_matched_pair_preserves_one_runtime_identity():
    m = _load()
    rows = m._validate_dependencies()["selected_execution_descriptors"]
    for pair_slot in range(1, 19):
        pair = [row for row in rows if row["pair_slot"] == pair_slot]
        assert len(pair) == 2
        ids = {
            row["runtime"]["selection"]["runtime_realization_sha256"]
            for row in pair
        }
        assert len(ids) == 1


def test_v14_and_v10_same_class_remain_distinct_controls():
    m = _load()
    rows = m._validate_dependencies()["selected_execution_descriptors"]
    v14 = next(
        row["runtime"]["selection"]
        for row in rows
        if row["apollyon_opponent"]["snapshot_id"] == "apollyon-v13-v14-promoted"
    )
    v10 = next(
        row["runtime"]["selection"]
        for row in rows
        if row["apollyon_opponent"]["snapshot_id"] == "apollyon-v13-v10-promoted"
    )
    assert v14["runtime_class"] == v10["runtime_class"]
    assert v14["selection_key"] != v10["selection_key"]
    assert v14["runtime_realization_sha256"] != v10["runtime_realization_sha256"]


def test_review_closes_only_selector_review_frontier():
    m = _load()
    out = m.cross_control_runtime_selector_source_binding_review_contract()
    assert out["cross_control_runtime_selector_implemented"] is True
    assert out["cross_control_runtime_selector_source_binding_present"] is True
    assert out["cross_control_runtime_selector_reviewed"] is True
    assert out["selector_removes_only_its_execution_blocker"] is True


def test_execution_materialization_blockers_are_preserved_after_review():
    m = _load()
    out = m.cross_control_runtime_selector_source_binding_review_contract()
    assert tuple(out["execution_materialization_blockers"]) == (
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
        "COMMAND_MATERIALIZER_NOT_IMPLEMENTED",
        "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
    )
    assert tuple(out["execution_materialization_source_blockers"]) == (
        "COMMAND_MATERIALIZER_NOT_IMPLEMENTED",
        "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
    )
    assert out["execution_materialization_remains_open"] is True


def test_runtime_authority_remains_separate_and_closed():
    m = _load()
    out = m.cross_control_runtime_selector_source_binding_review_contract()
    assert out["runtime_started"] is False
    assert out["runtime_execution_authorized"] is False
    assert out["runtime_selection_performed_by_review"] is False


def test_command_and_workdir_implementations_remain_open():
    m = _load()
    out = m.cross_control_runtime_selector_source_binding_review_contract()
    assert out["command_materializer_implemented"] is False
    assert out["isolated_workdir_allocator_implemented"] is False


def test_next_source_gate_is_command_materializer():
    m = _load()
    out = m.cross_control_runtime_selector_source_binding_review_contract()
    assert out["next_gate"] == "COMMAND_MATERIALIZER_IMPLEMENTATION_REQUIRED"
    assert out["next_change_class"] == "source_only_command_materializer_implementation"


def test_historical_materializer_review_is_retained_not_rewritten():
    m = _load()
    prior = m._validate_dependencies()["historical_materializer_review_contract"]
    assert prior["activation_source_review_frontier_complete"] is True
    assert prior["runtime_authority_is_only_remaining_activation_gap"] is True
    assert prior["runtime_execution_authorized"] is False
    assert prior["next_gate"] == "CROSS_CONTROL_RUNTIME_SELECTOR_IMPLEMENTATION_REQUIRED"


def test_review_contract_performs_no_live_or_runtime_action():
    m = _load()
    out = m.cross_control_runtime_selector_source_binding_review_contract()
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
        "review_deployment_implemented",
        "review_void_chain_mutation_implemented",
        "review_wallet_or_funds_action_implemented",
    ):
        assert out[field] is False


def test_command_materializer_entrypoint_holds_at_next_gate():
    m = _load()
    _expect_hold(
        m.CrossControlRuntimeSelectorSourceBindingReviewHold,
        "COMMAND_MATERIALIZER_IMPLEMENTATION_REQUIRED",
        m.materialize_command,
    )


def test_workdir_allocator_cannot_skip_command_materializer_gate():
    m = _load()
    _expect_hold(
        m.CrossControlRuntimeSelectorSourceBindingReviewHold,
        "COMMAND_MATERIALIZER_IMPLEMENTATION_REQUIRED",
        m.allocate_isolated_workdir,
    )


def test_execution_advance_holds_at_next_gate():
    m = _load()
    _expect_hold(
        m.CrossControlRuntimeSelectorSourceBindingReviewHold,
        "COMMAND_MATERIALIZER_IMPLEMENTATION_REQUIRED",
        m.advance_execution_materialization,
    )


def test_runtime_start_and_authorization_always_hold():
    m = _load()
    for fn in (m.start_runtime, m.authorize_runtime_execution):
        _expect_hold(
            m.CrossControlRuntimeSelectorSourceBindingReviewHold,
            "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
            fn,
        )


def test_review_does_not_rewrite_selector_contract():
    m = _load()
    before = m.selector.cross_control_runtime_selector_contract()
    m.cross_control_runtime_selector_source_binding_review_contract()
    after = m.selector.cross_control_runtime_selector_contract()
    assert before == after
    assert after["cross_control_runtime_selector_reviewed"] is False


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
