from __future__ import annotations

import ast
import hashlib
import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_primitive_provider_source_only_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_primitive_provider_source_only_generation2.py"
)
EXPECTED_SOURCE_SHA256 = (
    "daa038f17d3103cd0644303d40fd37a060ec51d1a6c68ac5d91555897eeb1a81"
)


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_provider_source_only",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _expect_hold(exc_type, pattern, fn):
    try:
        fn()
    except exc_type as exc:
        assert pattern in str(exc), (pattern, str(exc))
    else:
        raise AssertionError(f"expected {exc_type.__name__}: {pattern}")


def _valid_v8_fact(m):
    return {
        "schema": m.V8_SUPPLIED_ENVIRONMENT_SCHEMA,
        "python_major_minor": [3, 12],
        "pip_freeze_sha256": m.v8_runtime.RUNTIME_PIP_FREEZE_SHA256,
        "collection_performed": False,
        "filesystem_observation_performed": False,
        "subprocess_execution_performed": False,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_execution_performed": False,
    }


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def test_contract_binds_exact_provider_contract_and_v8_source():
    m = _load()
    out = m.source_only_provider_contract()
    assert out["provider_contract_git_blob"] == (
        "807335ae5ee2892917d02acfa6434fd65151960f"
    )
    assert out["provider_contract_semantic_sha256"] == (
        "58e84a058c332de983ccaef19bd1383a92071966b653e699d032c9e9e86c1114"
    )
    assert out["v8_runtime_git_blob"] == (
        "fd0e72767ba199e88af9e9eb2455c03ace027a14"
    )


def test_contract_implements_only_zero_io_classes():
    m = _load()
    out = m.source_only_provider_contract()
    assert out["common_self_audit_provider_implemented"] is True
    assert out["v8_load_call_self_audit_implemented"] is True
    assert out["v8_supplied_environment_validator_implemented"] is True
    assert out["v8_live_environment_collector_implemented"] is False
    assert out["v8_offline_only_provider_implemented"] is False
    assert out["v2r13_path_adapter_implemented"] is False
    assert out["v2r13_live_model_identity_provider_implemented"] is False
    assert out["v2r13_runtime_image_provider_implemented"] is False
    assert out["v2r13_portable_attestation_provider_implemented"] is False
    assert out["v14_live_identity_provider_implemented"] is False
    assert out["v10_live_identity_provider_implemented"] is False
    assert out["endpoint_liveness_provider_implemented"] is False


def test_contract_never_claims_collection_readiness_or_execution():
    m = _load()
    out = m.source_only_provider_contract()
    assert out["canonical_provider_binding_present"] is False
    assert out["canonical_collection_enabled"] is False
    assert out["live_observation_performed"] is False
    assert out["provider_host_io_performed"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_common_self_audit_values_are_exact_for_v14_v10_v2():
    m = _load()
    expected = {
        "observation_mode": "read_only",
        "mutation_performed": False,
        "service_action_performed": False,
        "runtime_start_performed": False,
        "game_execution_performed": False,
        "model_inference_performed": False,
    }
    for snapshot_id in (m.V14, m.V10, m.V2R13):
        assert m.source_only_self_audit_values(snapshot_id) == expected


def test_v8_adds_only_load_call_false_to_common_self_audits():
    m = _load()
    out = m.source_only_self_audit_values(m.V8)
    assert out == {
        "observation_mode": "read_only",
        "mutation_performed": False,
        "service_action_performed": False,
        "runtime_start_performed": False,
        "game_execution_performed": False,
        "model_inference_performed": False,
        "load_call_performed": False,
    }


def test_unknown_snapshot_holds():
    m = _load()
    _expect_hold(
        m.RuntimePrimitiveProviderSourceOnlyHold,
        "unsupported source-only provider snapshot",
        lambda: m.source_only_self_audit_values("not-reviewed"),
    )


def test_v14_progress_is_exact_six_supported_three_unresolved():
    m = _load()
    out = m.source_only_provider_progress(m.V14)
    assert out["supported_primitive_count"] == 6
    assert set(out["supported_primitive_names"]) == set(m.COMMON_SELF_AUDIT_VALUES)
    assert out["unresolved_primitive_names"] == m.V14_UNRESOLVED
    assert out["unresolved_primitive_count"] == 3
    assert out["provider_complete"] is False


def test_v10_progress_is_exact_six_supported_three_unresolved():
    m = _load()
    out = m.source_only_provider_progress(m.V10)
    assert out["supported_primitive_count"] == 6
    assert out["unresolved_primitive_names"] == m.V10_UNRESOLVED
    assert out["unresolved_primitive_count"] == 3
    assert out["provider_complete"] is False


def test_v2_progress_is_exact_six_supported_ten_unresolved():
    m = _load()
    out = m.source_only_provider_progress(m.V2R13)
    assert out["supported_primitive_count"] == 6
    assert out["unresolved_primitive_names"] == m.V2R13_UNRESOLVED
    assert out["unresolved_primitive_count"] == 10
    assert out["provider_complete"] is False


def test_v2_path_gap_refuses_to_infer_six_missing_leaves():
    m = _load()
    out = m.v2r13_path_adapter_gap()
    assert out["reviewed_git_observer_present"] is True
    assert out["reviewed_git_observer_git_blob"] == (
        "cc4774e6aa934764c189cebd4040cd8ea4870517"
    )
    assert out["observer_receipt_contains_missing_leaves"] is False
    assert out["adapter_implemented"] is False
    assert out["new_observation_primitive_required"] is True
    assert set(out["missing_activation_leaves"]) == {
        "frozen_source_worktree.exists",
        "frozen_source_worktree.is_directory",
        "frozen_source_worktree.is_symlink",
        "engine_worktree.exists",
        "engine_worktree.is_directory",
        "engine_worktree.is_symlink",
    }


def test_v8_without_supplied_environment_is_seven_supported_two_unresolved():
    m = _load()
    out = m.source_only_provider_progress(m.V8)
    assert out["supported_primitive_count"] == 7
    assert "load_call_performed" in out["supported_primitive_names"]
    assert out["validated_v8_environment_fact"] is None
    assert out["unresolved_primitive_names"] == (
        "runtime_environment_verified",
        "offline_only_verified",
    )
    assert out["unresolved_primitive_count"] == 2


def test_v8_valid_supplied_environment_closes_only_environment_claim():
    m = _load()
    fact = _valid_v8_fact(m)
    out = m.source_only_provider_progress(
        m.V8,
        supplied_v8_environment_fact=fact,
    )
    assert out["supported_primitive_count"] == 8
    assert "runtime_environment_verified" in out["supported_primitive_names"]
    assert out["unresolved_primitive_names"] == ("offline_only_verified",)
    assert out["unresolved_primitive_count"] == 1
    validated = out["validated_v8_environment_fact"]
    assert validated["runtime_environment_verified"] is True
    assert validated["collection_performed"] is False
    assert validated["subprocess_execution_performed"] is False
    assert validated["pure_validator_git_blob"] == (
        "fd0e72767ba199e88af9e9eb2455c03ace027a14"
    )
    assert out["provider_complete"] is False


def test_v8_supplied_environment_rejects_python_drift():
    m = _load()
    fact = _valid_v8_fact(m)
    fact["python_major_minor"] = [3, 11]
    _expect_hold(
        m.v8_runtime.V8CampaignRuntimeError,
        "V8 runtime Python major/minor drift",
        lambda: m.validate_v8_supplied_environment_fact(fact),
    )


def test_v8_supplied_environment_rejects_package_drift():
    m = _load()
    fact = _valid_v8_fact(m)
    fact["pip_freeze_sha256"] = "0" * 64
    _expect_hold(
        m.v8_runtime.V8CampaignRuntimeError,
        "V8 runtime pip-freeze SHA-256 drift",
        lambda: m.validate_v8_supplied_environment_fact(fact),
    )


def test_v8_supplied_environment_rejects_collection_claim():
    m = _load()
    fact = _valid_v8_fact(m)
    fact["subprocess_execution_performed"] = True
    _expect_hold(
        m.RuntimePrimitiveProviderSourceOnlyHold,
        "V8 supplied environment fact crossed boundary",
        lambda: m.validate_v8_supplied_environment_fact(fact),
    )


def test_v8_supplied_environment_rejects_extra_field():
    m = _load()
    fact = _valid_v8_fact(m)
    fact["extra"] = True
    _expect_hold(
        m.RuntimePrimitiveProviderSourceOnlyHold,
        "V8 environment fact field-set drift",
        lambda: m.validate_v8_supplied_environment_fact(fact),
    )


def test_progress_never_claims_host_io_or_runtime_authority():
    m = _load()
    for snapshot_id in (m.V14, m.V10, m.V2R13, m.V8):
        out = m.source_only_provider_progress(snapshot_id)
        assert out["canonical_provider_binding_present"] is False
        assert out["canonical_collection_enabled"] is False
        assert out["live_observation_performed"] is False
        assert out["filesystem_observation_performed"] is False
        assert out["external_worktree_git_query_performed"] is False
        assert out["observer_invocation_performed"] is False
        assert out["provider_host_io_performed"] is False
        assert out["runtime_readiness_admitted"] is False
        assert out["runtime_execution_authorized"] is False


def test_static_source_has_no_host_io_imports_or_calls():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    forbidden_import_roots = {
        "os",
        "subprocess",
        "socket",
        "requests",
        "urllib",
        "http",
        "httpx",
        "pathlib",
        "asyncio",
        "multiprocessing",
        "ctypes",
    }
    forbidden_call_fragments = {
        "verify_v8_runtime_environment",
        "observe_v2r13_git_identity",
        "observe_v8_assets",
        "host_git_runner",
        "host_file_observation_backend",
        "systemctl",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call):
            name = _dotted(node.func)
            assert not any(fragment in name for fragment in forbidden_call_fragments)


def test_live_provider_entrypoint_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimePrimitiveProviderSourceOnlyHold,
        "GENERATION2_LIVE_PRIMITIVE_PROVIDER_NOT_IMPLEMENTED",
        lambda: m.provide_live_primitive(),
    )
