from __future__ import annotations

import ast
import hashlib
import importlib.util
from pathlib import Path


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "openra_env"
    / "learning"
    / "abaddon_policy_campaign_cross_control_runtime_selector_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "19cd2c02e4232cee01e31286eee545237d61d7839542914899a1abf016fe26f4"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_cross_control_selector_test",
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


def test_contract_pins_exact_accepted_dependencies():
    m = _load()
    out = m.cross_control_runtime_selector_contract()
    assert out["execution_adapter_git_blob"] == "994d44d751c530619649322c72a65edf15f6a8c3"
    assert out["runtime_realizations_git_blob"] == "0dbae61b0be96445e5fd6c23a07491a03f18b679"
    assert out["materializer_review_git_blob"] == "3dcc325c431ec451a737b6e228c365ce1acb4f98"
    assert out["orchestrator_git_blob"] == "8948b53d002e5d7e48a7aef2ec10ff5d690f5a1c"


def test_contract_pins_reviewed_realization_and_snapshot_sets():
    m = _load()
    out = m.cross_control_runtime_selector_contract()
    assert out["runtime_realization_set_sha256"] == (
        "1dbb861a3bc03a4423187846a519f228726cc890f4452c3b1d8607614288a7d8"
    )
    assert out["opponent_snapshot_set_sha256"] == (
        "d7bfce0cb1456ec440f6ab362c781057837c3912c557f865ae95b7ddc6278526"
    )


def test_selector_is_implemented_but_not_self_reviewed():
    m = _load()
    out = m.cross_control_runtime_selector_contract()
    assert out["cross_control_runtime_selector_implemented"] is True
    assert out["cross_control_runtime_selector_reviewed"] is False
    assert out["runtime_selection_performed"] is False


def test_selector_supports_exact_36_descriptors_and_18_pairs():
    m = _load()
    out = m.cross_control_runtime_selector_contract()
    assert out["execution_descriptor_count"] == 36
    assert out["matched_pair_count"] == 18
    assert len(out["dependencies"]["execution_descriptors"]) == 36


def test_selector_supports_exact_four_reviewed_controls():
    m = _load()
    out = m.cross_control_runtime_selector_contract()
    assert out["reviewed_runtime_count"] == 4
    assert set(out["dependencies"]["runtime_index"]) == set(m.EXPECTED_RUNTIME_BINDINGS)


def test_runtime_class_is_not_used_as_cross_control_identity():
    m = _load()
    out = m.cross_control_runtime_selector_contract()
    assert out["selection_key"] == "opponent_snapshot_id"
    assert out["runtime_class_is_not_selection_key"] is True
    assert out["reviewed_runtime_class_count"] == 3


def test_v14_and_v10_same_class_remain_distinct_by_snapshot_identity():
    m = _load()
    v14 = next(
        row
        for row in m.all_selected_execution_descriptors()
        if row["apollyon_opponent"]["snapshot_id"] == "apollyon-v13-v14-promoted"
    )
    v10 = next(
        row
        for row in m.all_selected_execution_descriptors()
        if row["apollyon_opponent"]["snapshot_id"] == "apollyon-v13-v10-promoted"
    )
    s14 = v14["runtime"]["selection"]
    s10 = v10["runtime"]["selection"]
    assert s14["runtime_class"] == s10["runtime_class"]
    assert s14["selection_key"] != s10["selection_key"]
    assert s14["runtime_realization_sha256"] != s10["runtime_realization_sha256"]


def test_all_36_canonical_descriptors_select_deterministically():
    m = _load()
    first = m.all_selected_execution_descriptors()
    second = m.all_selected_execution_descriptors()
    assert first == second
    assert len(first) == 36
    assert all(row["runtime"]["selection_performed"] is True for row in first)


def test_each_matched_pair_uses_identical_runtime_selection():
    m = _load()
    rows = m.all_selected_execution_descriptors()
    for pair_slot in range(1, 19):
        pair = [row for row in rows if row["pair_slot"] == pair_slot]
        assert len(pair) == 2
        identities = {
            row["runtime"]["selection"]["runtime_realization_sha256"]
            for row in pair
        }
        assert len(identities) == 1


def test_selected_descriptor_removes_only_selector_blocker():
    m = _load()
    row = m.selected_execution_descriptor(pair_slot=1, arm="baseline")
    assert tuple(row["reasons"]) == (
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
        "COMMAND_MATERIALIZER_NOT_IMPLEMENTED",
        "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
    )
    assert "CROSS_CONTROL_RUNTIME_SELECTOR_NOT_IMPLEMENTED" not in row["reasons"]


def test_selected_descriptor_remains_ineligible():
    m = _load()
    row = m.selected_execution_descriptor(pair_slot=1, arm="baseline")
    assert row["eligible"] is False
    assert row["authority"]["runtime_execution_authorized"] is False


def test_selection_never_starts_runtime_or_executes_model_game():
    m = _load()
    out = m.select_runtime(pair_slot=1, arm="baseline")
    assert out["selection_performed"] is True
    assert out["selection_is_source_only"] is True
    assert out["runtime_started"] is False
    assert out["runtime_execution_authorized"] is False
    assert out["model_load_performed"] is False
    assert out["model_inference_performed"] is False
    assert out["game_execution_performed"] is False


def test_selection_does_not_materialize_command_or_workdir():
    m = _load()
    out = m.select_runtime(pair_slot=1, arm="candidate")
    assert out["command_materialized"] is False
    assert out["workdir_materialized"] is False


def test_v2r13_runtime_identity_remains_exactly_bound():
    m = _load()
    rows = m.all_selected_execution_descriptors()
    row = next(
        row
        for row in rows
        if row["apollyon_opponent"]["snapshot_id"]
        == "apollyon-v2r13-qualified-predecessor"
    )
    selection = row["runtime"]["selection"]
    assert selection["runtime_class"] == "legacy_warm_start_ollama_openai_tool_runtime"
    assert selection["runtime_identity"]["model_alias"] == "void-apollyon-candidate-v2r13:latest"
    assert selection["runtime_identity"]["model_digest"] == (
        "b52834ea46c10362e9bb20cd2e721716016bb36f800ddbc62e7fbaa24fb40932"
    )
    assert selection["runtime_identity"]["engine_commit"] == (
        "1607a7a6501d42a47638393ecef8b22831064932"
    )


def test_v8_selection_remains_local_frozen_template_runtime_class():
    m = _load()
    rows = m.all_selected_execution_descriptors()
    row = next(
        row
        for row in rows
        if row["apollyon_opponent"]["snapshot_id"]
        == "apollyon-v3-v8-accepted-model-control"
    )
    selection = row["runtime"]["selection"]
    assert selection["runtime_class"] == (
        "accepted_v8_adapter_frozen_chat_template_tool_runtime"
    )
    assert selection["runtime_started"] is False
    assert selection["model_inference_performed"] is False


def test_invalid_pair_slot_is_rejected_fail_closed():
    m = _load()
    _expect_hold(
        Exception,
        "unknown Generation-2 arm",
        lambda: m.select_runtime(pair_slot=0, arm="baseline"),
    )


def test_invalid_arm_is_rejected_fail_closed():
    m = _load()
    _expect_hold(
        Exception,
        "unknown Generation-2 arm",
        lambda: m.select_runtime(pair_slot=1, arm="wrong"),
    )


def test_tampered_snapshot_identity_is_rejected():
    m = _load()
    d = m.execution_adapter.execution_descriptor(pair_slot=1, arm="baseline")
    d["apollyon_opponent"]["snapshot_id"] = "apollyon-v13-v10-promoted"
    _expect_hold(
        m.CrossControlRuntimeSelectorHold,
        "not canonical",
        lambda: m.select_cross_control_runtime(d),
    )


def test_tampered_runtime_realization_is_rejected():
    m = _load()
    d = m.execution_adapter.execution_descriptor(pair_slot=1, arm="baseline")
    d["apollyon_opponent"]["runtime_realization"]["runtime_class"] = "tampered"
    _expect_hold(
        m.CrossControlRuntimeSelectorHold,
        "not canonical",
        lambda: m.select_cross_control_runtime(d),
    )


def test_tampered_preselector_blockers_are_rejected():
    m = _load()
    d = m.execution_adapter.execution_descriptor(pair_slot=1, arm="baseline")
    d["reasons"] = list(d["reasons"][:-1])
    _expect_hold(
        m.CrossControlRuntimeSelectorHold,
        "not canonical",
        lambda: m.select_cross_control_runtime(d),
    )


def test_historical_adapter_remains_unmodified_and_nonselecting():
    m = _load()
    before = m.execution_adapter.execution_descriptor(pair_slot=1, arm="baseline")
    m.select_cross_control_runtime(before)
    after = m.execution_adapter.execution_descriptor(pair_slot=1, arm="baseline")
    assert before == after
    assert after["runtime"]["cross_control_selector_implemented"] is False
    assert after["runtime"]["selection_performed"] is False


def test_materializer_review_frontier_is_retained():
    m = _load()
    deps = m._validate_dependencies()
    review = deps["materializer_review_contract"]
    assert review["frozen_worktree_materializer_reviewed"] is True
    assert review["activation_source_review_frontier_complete"] is True
    assert review["runtime_execution_authorized"] is False


def test_next_gate_is_separate_selector_source_binding_review():
    m = _load()
    out = m.cross_control_runtime_selector_contract()
    assert out["next_gate"] == (
        "CROSS_CONTROL_RUNTIME_SELECTOR_SOURCE_BINDING_REVIEW_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_cross_control_runtime_selector_source_binding_review"
    )


def test_command_and_workdir_advance_hold_at_selector_review_gate():
    m = _load()
    for fn in (m.materialize_command, m.allocate_isolated_workdir):
        _expect_hold(
            m.CrossControlRuntimeSelectorHold,
            "CROSS_CONTROL_RUNTIME_SELECTOR_SOURCE_BINDING_REVIEW_REQUIRED",
            fn,
        )


def test_runtime_start_and_authorization_remain_closed():
    m = _load()
    for fn in (m.start_runtime, m.authorize_runtime_execution):
        _expect_hold(
            m.CrossControlRuntimeSelectorHold,
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
    forbidden_calls = {
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
            assert node.func.id not in forbidden_calls
