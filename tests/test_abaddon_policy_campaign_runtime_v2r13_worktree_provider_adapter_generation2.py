from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_v2r13_worktree_provider_adapter_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_worktree_provider_adapter_generation2.py"
)
EXPECTED_SOURCE_SHA256 = (
    "172dbb3acc3d9f34a64acd68f3bee58ae30336ad2802fd1dfbf9597bf8105522"
)

SOURCE_ROOT = "/frozen/source"
ENGINE_ROOT = "/engine/exact"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_v2r13_worktree_provider_adapter",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _valid_receipt(m):
    ro = m.worktree_observer.runtime_observers
    return {
        "schema": m.worktree_observer.OBSERVATION_SCHEMA,
        "snapshot_id": m.V2R13,
        "frozen_source_worktree": {
            "path": SOURCE_ROOT,
            "exists": True,
            "is_directory": True,
            "is_symlink": False,
            "clean": True,
            "detached": True,
            "head_commit": ro.FROZEN_WAR_COLLEGE_COMMIT,
            "tree_sha": ro.FROZEN_WAR_COLLEGE_TREE,
        },
        "engine_worktree": {
            "path": ENGINE_ROOT,
            "exists": True,
            "is_directory": True,
            "is_symlink": False,
            "clean": True,
            "head_commit": ro.FROZEN_ENGINE_COMMIT,
        },
        "source_path_generation_stable": True,
        "engine_path_generation_stable": True,
        "git_observation_schema": ro.V2R13_OBSERVATION_SCHEMA,
        "observation_mode": "read_only",
        "filesystem_observation_performed": True,
        "git_query_performed": True,
        "worktree_created": False,
        "checkout_mutation_performed": False,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_execution_performed": False,
    }


def _expect_hold(exc_type, pattern, fn):
    try:
        fn()
    except exc_type as exc:
        assert pattern in str(exc), (pattern, str(exc))
    else:
        raise AssertionError(f"expected {exc_type.__name__}: {pattern}")


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def test_contract_binds_exact_source_blobs():
    m = _load()
    out = m.v2r13_worktree_provider_adapter_contract()
    assert out["source_only_provider_git_blob"] == (
        "f3b48e624172aeed81e28a6e24508533b7b13661"
    )
    assert out["worktree_observer_git_blob"] == (
        "994f3be5d3344d6ac905c1f5fee9f9490fd4dd3f"
    )


def test_contract_support_counts_are_exact():
    m = _load()
    out = m.v2r13_worktree_provider_adapter_contract()
    assert out["six_worktree_primitives_implemented"] is True
    assert out["combined_source_supported_primitive_count"] == 12
    assert out["remaining_unresolved_primitive_count"] == 4
    assert out["remaining_unresolved_primitive_names"] == (
        "endpoint_liveness",
        "model_identity_verified",
        "runtime_image_identity_verified",
        "portable_binding_attested",
    )


def test_contract_keeps_live_and_admission_surfaces_closed():
    m = _load()
    out = m.v2r13_worktree_provider_adapter_contract()
    assert out["portable_binding_attestation_implemented"] is False
    assert out["adapter_filesystem_observation_implemented"] is False
    assert out["adapter_git_query_implemented"] is False
    assert out["adapter_path_resolution_implemented"] is False
    assert out["adapter_observer_invocation_implemented"] is False
    assert out["adapter_host_backend_invocation_implemented"] is False
    assert out["canonical_provider_binding_present"] is False
    assert out["canonical_collection_enabled"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_exact_six_primitive_names():
    m = _load()
    assert m.V2R13_WORKTREE_PRIMITIVES == (
        "frozen_source_worktree.exists",
        "frozen_source_worktree.is_directory",
        "frozen_source_worktree.is_symlink",
        "engine_worktree.exists",
        "engine_worktree.is_directory",
        "engine_worktree.is_symlink",
    )


def test_valid_receipt_extracts_exact_six_values():
    m = _load()
    values = m.v2r13_worktree_primitive_values(_valid_receipt(m))
    assert values == {
        "frozen_source_worktree.exists": True,
        "frozen_source_worktree.is_directory": True,
        "frozen_source_worktree.is_symlink": False,
        "engine_worktree.exists": True,
        "engine_worktree.is_directory": True,
        "engine_worktree.is_symlink": False,
    }


def test_adapter_combines_six_source_only_plus_six_worktree_values():
    m = _load()
    out = m.adapt_v2r13_worktree_receipt(_valid_receipt(m))
    assert out["primitive_count"] == 6
    assert out["combined_supported_primitive_count"] == 12
    assert len(out["combined_supported_primitive_names"]) == 12
    assert len(set(out["combined_supported_primitive_names"])) == 12
    assert out["remaining_unresolved_primitive_count"] == 4


def test_adapter_preserves_supplied_observation_provenance():
    m = _load()
    out = m.adapt_v2r13_worktree_receipt(_valid_receipt(m))
    assert out["supplied_receipt_reports_filesystem_observation"] is True
    assert out["supplied_receipt_reports_git_query"] is True
    assert out["adapter_filesystem_observation_performed"] is False
    assert out["adapter_external_worktree_git_query_performed"] is False
    assert out["adapter_path_resolution_performed"] is False
    assert out["adapter_observer_invocation_performed"] is False
    assert out["adapter_host_backend_invocation_performed"] is False


def test_adapter_never_claims_completion_portable_binding_or_readiness():
    m = _load()
    out = m.adapt_v2r13_worktree_receipt(_valid_receipt(m))
    assert out["provider_complete"] is False
    assert out["portable_binding_attested"] is False
    assert out["canonical_provider_binding_present"] is False
    assert out["canonical_collection_enabled"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_adapter_does_not_mutate_supplied_receipt():
    m = _load()
    receipt = _valid_receipt(m)
    before = copy.deepcopy(receipt)
    m.adapt_v2r13_worktree_receipt(receipt)
    assert receipt == before


def test_returned_primitive_values_are_copy_isolated():
    m = _load()
    receipt = _valid_receipt(m)
    first = m.adapt_v2r13_worktree_receipt(receipt)
    first["primitive_values"]["engine_worktree.exists"] = False
    second = m.adapt_v2r13_worktree_receipt(receipt)
    assert second["primitive_values"]["engine_worktree.exists"] is True


def test_bad_top_level_schema_is_rejected():
    m = _load()
    receipt = _valid_receipt(m)
    receipt["schema"] = "wrong"
    _expect_hold(
        m.worktree_observer.RuntimeV2R13WorktreeObserverHold,
        "V2R13 receipt schema drift",
        lambda: m.adapt_v2r13_worktree_receipt(receipt),
    )


def test_missing_top_level_field_is_rejected():
    m = _load()
    receipt = _valid_receipt(m)
    del receipt["git_query_performed"]
    _expect_hold(
        m.worktree_observer.RuntimeV2R13WorktreeObserverHold,
        "V2R13 worktree observation field-set drift",
        lambda: m.adapt_v2r13_worktree_receipt(receipt),
    )


def test_source_existence_false_is_rejected():
    m = _load()
    receipt = _valid_receipt(m)
    receipt["frozen_source_worktree"]["exists"] = False
    _expect_hold(
        m.worktree_observer.RuntimeV2R13WorktreeObserverHold,
        "V2R13 source lacks exists",
        lambda: m.adapt_v2r13_worktree_receipt(receipt),
    )


def test_source_symlink_true_is_rejected():
    m = _load()
    receipt = _valid_receipt(m)
    receipt["frozen_source_worktree"]["is_symlink"] = True
    _expect_hold(
        m.worktree_observer.RuntimeV2R13WorktreeObserverHold,
        "V2R13 source is symlink",
        lambda: m.adapt_v2r13_worktree_receipt(receipt),
    )


def test_engine_directory_false_is_rejected():
    m = _load()
    receipt = _valid_receipt(m)
    receipt["engine_worktree"]["is_directory"] = False
    _expect_hold(
        m.worktree_observer.RuntimeV2R13WorktreeObserverHold,
        "V2R13 engine lacks is_directory",
        lambda: m.adapt_v2r13_worktree_receipt(receipt),
    )


def test_source_commit_drift_is_rejected():
    m = _load()
    receipt = _valid_receipt(m)
    receipt["frozen_source_worktree"]["head_commit"] = "0" * 40
    _expect_hold(
        m.worktree_observer.RuntimeV2R13WorktreeObserverHold,
        "V2R13 source commit drift",
        lambda: m.adapt_v2r13_worktree_receipt(receipt),
    )


def test_engine_commit_drift_is_rejected():
    m = _load()
    receipt = _valid_receipt(m)
    receipt["engine_worktree"]["head_commit"] = "0" * 40
    _expect_hold(
        m.worktree_observer.RuntimeV2R13WorktreeObserverHold,
        "V2R13 engine commit drift",
        lambda: m.adapt_v2r13_worktree_receipt(receipt),
    )


def test_runtime_execution_claim_is_rejected():
    m = _load()
    receipt = _valid_receipt(m)
    receipt["runtime_execution_performed"] = True
    _expect_hold(
        m.worktree_observer.RuntimeV2R13WorktreeObserverHold,
        "V2R13 worktree receipt crossed boundary: runtime_execution_performed",
        lambda: m.adapt_v2r13_worktree_receipt(receipt),
    )


def test_remaining_unresolved_set_is_exact():
    m = _load()
    out = m.adapt_v2r13_worktree_receipt(_valid_receipt(m))
    assert out["remaining_unresolved_primitive_names"] == (
        "endpoint_liveness",
        "model_identity_verified",
        "runtime_image_identity_verified",
        "portable_binding_attested",
    )


def test_static_source_has_no_host_io_or_live_observer_calls():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    forbidden_import_roots = {
        "os",
        "subprocess",
        "pathlib",
        "socket",
        "requests",
        "urllib",
        "http",
        "httpx",
    }
    forbidden_calls = {
        "worktree_observer.observe_v2r13_worktrees",
        "worktree_observer.observe_with_host_backend",
        "source_only_provider.provide_live_primitive",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call):
            assert _dotted(node.func) not in forbidden_calls


def test_live_adapter_entrypoint_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13WorktreeProviderAdapterHold,
        "GENERATION2_V2R13_LIVE_WORKTREE_ADAPTER_NOT_IMPLEMENTED",
        lambda: m.adapt_live_worktree_state(),
    )
