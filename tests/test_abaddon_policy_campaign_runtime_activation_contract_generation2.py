from __future__ import annotations

import ast
import hashlib
import importlib.util
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_PROPOSAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_activation_contract_generation2.py"
)
SOURCE = (
    LOCAL_PROPOSAL_SOURCE
    if LOCAL_PROPOSAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/abaddon_policy_campaign_runtime_activation_contract_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "dc4c90175dee00f23ab28bc362cec41245a069345c0154d519215e3cb8150a3c"

FORBIDDEN_IMPORT_ROOTS = {
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
FORBIDDEN_CALLS = {
    "subprocess.run",
    "subprocess.Popen",
    "subprocess.call",
    "subprocess.check_call",
    "subprocess.check_output",
    "os.system",
    "os.popen",
}


def _expect_hold(exc_type, pattern, fn):
    try:
        fn()
    except exc_type as exc:
        assert pattern in str(exc), (pattern, str(exc))
    else:
        raise AssertionError(f"expected {exc_type.__name__}: {pattern}")


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_runtime_activation_contract",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def test_static_source_has_no_direct_execution_surface():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in FORBIDDEN_IMPORT_ROOTS
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".", 1)[0]
            assert root not in FORBIDDEN_IMPORT_ROOTS
        elif isinstance(node, ast.Call):
            assert _dotted(node.func) not in FORBIDDEN_CALLS


def test_activation_contract_is_exact_four_runtime_nonexecuting_set():
    m = _load()
    out = m.activation_contract()
    assert out["runtime_count"] == 4
    assert [row["snapshot_id"] for row in out["descriptors"]] == [
        m.V14,
        m.V10,
        m.V2R13,
        m.V8,
    ]
    assert out["cross_control_activation_implementation_present"] is False
    assert out["runtime_selection_implementation_present"] is False
    assert out["activation_commands_materialized"] is False
    assert out["service_actions_materialized"] is False
    assert out["ready_probes_materialized"] is False
    assert out["runtime_execution_authorized"] is False
    assert all(row["eligible"] is False for row in out["descriptors"])


def test_v14_v10_share_endpoint_but_require_distinct_identity():
    m = _load()
    v14 = m.activation_descriptor(m.V14)
    v10 = m.activation_descriptor(m.V10)
    assert v14["activation_kind"] == "external_loopback_openai_runtime"
    assert v10["activation_kind"] == "external_loopback_openai_runtime"
    assert v14["chat_completions_url"] == v10["chat_completions_url"] == m.LOOPBACK_11435
    assert v14["expected_model_id"] != v10["expected_model_id"]
    assert v14["active_runtime_unit_sha256"] != v10["active_runtime_unit_sha256"]
    assert v14["endpoint_liveness_proves_identity"] is False
    assert v10["endpoint_liveness_proves_identity"] is False
    assert v14["runtime_specific_activation_binding_reviewed"] is False
    assert v10["runtime_specific_activation_binding_reviewed"] is False


def test_v2r13_requires_exact_external_runtime_and_frozen_worktrees():
    m = _load()
    row = m.activation_descriptor(m.V2R13)
    assert row["activation_kind"] == "external_legacy_ollama_openai_runtime"
    assert row["chat_completions_url"] == m.LOOPBACK_11434
    assert row["expected_model_alias"] == m.V2R13_MODEL_ALIAS
    assert row["expected_model_digest"] == m.V2R13_MODEL_DIGEST
    assert row["portable_checkout"]["source_materialization"] == "detached_git_worktree"
    assert row["portable_checkout"]["source_worktree_path_bound"] is False
    assert row["portable_checkout"]["engine_worktree_path_bound"] is False
    assert row["portable_checkout"]["worktree_materialization_implemented"] is False
    assert row["portable_checkout"]["canonical_checkout_mutation_required"] is False
    assert "V2R13_FROZEN_WORKTREE_MATERIALIZER_NOT_REVIEWED" in row["blockers"]


def test_v8_is_inprocess_and_paths_are_deliberately_unbound():
    m = _load()
    row = m.activation_descriptor(m.V8)
    assert row["activation_kind"] == "inprocess_accepted_v8_runtime"
    assert row["chat_completions_url"] is None
    assert row["tool_runtime_source_sha256"] == m.V8_TOOL_RUNTIME_SOURCE_SHA256
    assert row["tool_runtime_contract_sha256"] == m.V8_TOOL_RUNTIME_CONTRACT_SHA256
    assert row["model_dir_path_bound"] is False
    assert row["adapter_dir_path_bound"] is False
    assert row["load_call_materialized"] is False
    assert row["model_weights_loaded"] is False
    assert row["requirements"]["runtime_assets_hash_verified_before_load"] is True
    assert row["requirements"]["runtime_environment_live_pip_freeze_match_required"] is True
    assert row["requirements"]["offline_only_model_load"] is True
    assert "V8_LOAD_CALL_BINDING_NOT_REVIEWED" in row["blockers"]


def test_native_run_namespace_is_overwrite_safe_but_not_unique_guaranteed():
    m = _load()
    ns = m.activation_contract()["native_run_namespace"]
    assert ns["timestamp_granularity"] == "seconds"
    assert ns["primary_outputs"] == (
        "warm-start.jsonl",
        "trajectory.jsonl",
        "summary.json",
    )
    assert ns["primary_outputs_direct_children_of_run_dir"] is True
    assert ns["run_dir_collision_check_present"] is True
    assert ns["run_dir_mkdir_present"] is True
    assert ns["overwrite_safe"] is True
    assert ns["run_id_uniqueness_evidence_present"] is True
    assert ns["run_id_uniqueness_guaranteed"] is False
    assert ns["collision_refusal_required"] is True
    assert ns["additional_outer_workdir_isolation_required"] is False


def test_all_36_arm_plans_match_frozen_runtime_distribution():
    m = _load()
    rows = m.all_arm_runtime_activation_plans()
    assert len(rows) == 36
    assert [row["execution_index"] for row in rows] == list(range(1, 37))
    counts = Counter(row["opponent_snapshot_id"] for row in rows)
    assert counts == {
        m.V14: 12,
        m.V10: 12,
        m.V2R13: 6,
        m.V8: 6,
    }
    assert all(row["eligible"] is False for row in rows)


def test_baseline_candidate_share_same_runtime_requirement_per_pair():
    m = _load()
    for pair_slot in range(1, 19):
        baseline = m.arm_runtime_activation_plan(pair_slot=pair_slot, arm="baseline")
        candidate = m.arm_runtime_activation_plan(pair_slot=pair_slot, arm="candidate")
        assert baseline["opponent_snapshot_id"] == candidate["opponent_snapshot_id"]
        assert baseline["activation"]["snapshot_sha256"] == candidate["activation"]["snapshot_sha256"]
        assert baseline["activation"]["runtime_class"] == candidate["activation"]["runtime_class"]


def test_all_arm_plans_preserve_external_prelaunch_boundary_as_unperformed():
    m = _load()
    for row in m.all_arm_runtime_activation_plans():
        assert row["activation_implementation_present"] is False
        assert row["runtime_selection_performed"] is False
        assert row["runtime_started"] is False
        assert row["command_materialized"] is False
        assert row["authority"]["runtime_execution_authorized"] is False
        assert m.RUNTIME_AUTHORITY_BLOCKER in row["reasons"]


def test_held_out_status_remains_bound_to_canonical_arm_descriptor():
    m = _load()
    rows = m.all_arm_runtime_activation_plans()
    held = [row for row in rows if row["held_out"]]
    assert len(held) == 12
    assert {row["pair_slot"] for row in held} == set(range(13, 19))


def test_unknown_snapshot_holds():
    m = _load()
    _expect_hold(
        m.RuntimeActivationHold,
        "unknown snapshot id",
        lambda: m.activation_descriptor("not-a-reviewed-snapshot"),
    )


def test_invalid_arm_holds_through_canonical_adapter():
    m = _load()
    _expect_hold(
        Exception,
        "unknown Generation-2 arm",
        lambda: m.arm_runtime_activation_plan(pair_slot=1, arm="wrong"),
    )


def test_activate_runtime_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeActivationHold,
        "RUNTIME_ACTIVATION_IMPLEMENTATION_NOT_PRESENT",
        lambda: m.activate_runtime(),
    )
