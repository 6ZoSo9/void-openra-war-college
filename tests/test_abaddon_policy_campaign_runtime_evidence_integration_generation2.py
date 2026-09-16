from __future__ import annotations

import ast
import hashlib
import importlib.util
import sys
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_evidence_integration_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_evidence_integration_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "0fcbc4375fcc3c8458b06ea92dcd34fdedaa53e50e180169365a64cab30a3b3a"


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


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_runtime_evidence_integration",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _v8_paths(m):
    return {
        "schema": "void.abaddon.generation2.runtime-path-input-record.v1",
        "snapshot_id": m.V8,
        "source_kind": "explicit_external_input",
        "model_dir": "/srv/void/g2/v8/model",
        "adapter_dir": "/srv/void/g2/v8/adapter",
    }


def _v2_paths(m):
    return {
        "schema": "void.abaddon.generation2.runtime-path-input-record.v1",
        "snapshot_id": m.V2R13,
        "source_kind": "explicit_external_input",
        "frozen_source_root": "/srv/void/g2/v2r13/source",
        "exact_engine_root": "/srv/void/g2/v2r13/engine",
    }


def _identity(m, size):
    return {
        "st_dev": 2050,
        "st_ino": 11,
        "st_size": size,
        "st_mtime_ns": 13,
        "st_ctime_ns": 17,
        "st_mode": 0o100400,
        "st_nlink": 1,
    }


def _v8_receipt(m):
    obs = m.observer_composition.observers
    paths = _v8_paths(m)
    assets = []
    for index, spec in enumerate(obs.V8_ASSET_SPECS, start=1):
        root = paths[spec.root_field]
        assets.append(
            {
                "label": spec.label,
                "root_field": spec.root_field,
                "relative_path": spec.relative_path,
                "observation": {
                    "schema": obs.FILE_OBSERVATION_SCHEMA,
                    "path": f"{root}/{spec.relative_path}",
                    "expected_sha256": spec.expected_sha256,
                    "actual_sha256": spec.expected_sha256,
                    "byte_count": index,
                    "maximum_bytes": spec.maximum_bytes,
                    "identity": _identity(m, index),
                    "generation_stable": True,
                    "regular_file": True,
                    "symlink_followed": False,
                    "runtime_execution_performed": False,
                    "model_execution_performed": False,
                },
            }
        )
    return {
        "schema": obs.V8_OBSERVATION_SCHEMA,
        "snapshot_id": m.V8,
        "asset_count": 17,
        "assets": assets,
        "all_assets_verified": True,
        "model_weights_loaded": False,
        "runtime_started": False,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_execution_performed": False,
    }


def _v2_receipt(m):
    obs = m.observer_composition.observers
    paths = _v2_paths(m)
    return {
        "schema": obs.V2R13_OBSERVATION_SCHEMA,
        "snapshot_id": m.V2R13,
        "source_root": paths["frozen_source_root"],
        "engine_root": paths["exact_engine_root"],
        "source_head_commit": obs.FROZEN_WAR_COLLEGE_COMMIT,
        "source_head_tree": obs.FROZEN_WAR_COLLEGE_TREE,
        "source_worktree_clean": True,
        "source_detached_head": True,
        "engine_head_commit": obs.FROZEN_ENGINE_COMMIT,
        "engine_worktree_clean": True,
        "worktree_created": False,
        "checkout_mutation_performed": False,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_execution_performed": False,
    }


def _v8_fact(m):
    sp = m.shape_progress
    return {
        "schema": sp.FACT_SCHEMA,
        "snapshot_id": m.V8,
        "fact_kind": sp.V8_ENVIRONMENT_FACT_KIND,
        "python_major_minor": list(sp.v8_runtime.RUNTIME_PYTHON_MAJOR_MINOR),
        "pip_freeze_sha256": sp.v8_runtime.RUNTIME_PIP_FREEZE_SHA256,
        "fact_source": sp.FACT_SOURCE,
        "live_collection_performed": False,
        "collector_identity_admitted": False,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
    }


def _v2_fact(m):
    sp = m.shape_progress
    return {
        "schema": sp.FACT_SCHEMA,
        "snapshot_id": m.V2R13,
        "fact_kind": sp.V2R13_PORTABLE_CONTRACT_FACT_KIND,
        "binding_contract": sp.v2_portable.portable_binding_contract(),
        "fact_source": sp.FACT_SOURCE,
        "live_binding_installation_attested": False,
        "collector_identity_admitted": False,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_execution_performed": False,
    }


def test_contract_is_partial_source_only_integration():
    m = _load()
    out = m.runtime_evidence_integration_contract()
    assert out["supported_snapshot_ids"] == (m.V2R13, m.V8)
    assert out["partial_evidence_integration_implemented"] is True
    assert out["conflicting_supported_field_rejection_implemented"] is True
    assert out["final_activation_evidence_shape_composition_implemented"] is False
    assert out["collector_identity_admission_implemented"] is False
    assert out["runtime_readiness_admission_implemented"] is False
    assert out["live_observation_performed"] is False
    assert out["external_worktree_git_query_performed"] is False
    assert out["pip_freeze_performed"] is False
    assert out["observer_invocation_performed"] is False
    assert out["runtime_execution_authorized"] is False


def test_static_source_has_no_collection_or_execution_surface():
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
    }
    forbidden_calls = {
        "observer_composition.observers.observe_v8_assets",
        "observer_composition.observers.observe_v2r13_git_identity",
        "shape_progress.v8_runtime.verify_v8_runtime_environment",
        "shape_progress.v8_runtime.verify_v8_runtime_assets",
        "shape_progress.v2_portable.PortableRunnerBinding",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call):
            assert _dotted(node.func) not in forbidden_calls


def test_merge_supported_fields_accepts_disjoint_fields():
    m = _load()
    assert m._merge_supported_fields({"a": 1}, {"b": 2}) == {
        "a": 1,
        "b": 2,
    }


def test_merge_supported_fields_accepts_equal_duplicate():
    m = _load()
    assert m._merge_supported_fields({"a": 1}, {"a": 1}) == {"a": 1}


def test_merge_supported_fields_rejects_conflict():
    m = _load()
    _expect_hold(
        m.RuntimeEvidenceIntegrationHold,
        "conflicting supported activation-evidence field: a",
        lambda: m._merge_supported_fields({"a": 1}, {"a": 2}),
    )


def test_v8_without_environment_fact_remains_partially_unresolved():
    m = _load()
    out = m.integrate_v8_partial_evidence(
        _v8_receipt(m),
        path_input_record=_v8_paths(m),
    )
    unresolved = out["unresolved_activation_evidence_fields"]
    assert "collector_contract_sha256" in unresolved
    assert "runtime_environment_verified" in unresolved
    assert "offline_only_verified" in unresolved
    assert "load_call_performed" in unresolved
    assert out["activation_evidence_shape_complete"] is False
    assert out["collector_identity_admitted"] is False
    assert out["runtime_readiness_admitted"] is False


def test_v8_with_environment_fact_closes_only_environment_shape():
    m = _load()
    out = m.integrate_v8_partial_evidence(
        _v8_receipt(m),
        path_input_record=_v8_paths(m),
        environment_fact=_v8_fact(m),
    )
    combined = out["combined_supported_activation_evidence_fields"]
    unresolved = out["unresolved_activation_evidence_fields"]
    assert combined["runtime_environment_verified"] is True
    assert "runtime_environment_verified" not in unresolved
    assert "collector_contract_sha256" in unresolved
    assert "offline_only_verified" in unresolved
    assert "load_call_performed" in unresolved
    assert out["activation_evidence_shape_complete"] is False
    assert out["collector_identity_admitted"] is False
    assert out["runtime_readiness_admitted"] is False


def test_v8_combines_static_and_observer_fields():
    m = _load()
    out = m.integrate_v8_partial_evidence(
        _v8_receipt(m),
        path_input_record=_v8_paths(m),
        environment_fact=_v8_fact(m),
    )
    combined = out["combined_supported_activation_evidence_fields"]
    requirement = m.shape_progress.evidence_requirement(m.V8)
    for key, value in requirement["expected"].items():
        assert combined[key] == value
    assert combined["model_dir"] == "/srv/void/g2/v8/model"
    assert combined["adapter_dir"] == "/srv/void/g2/v8/adapter"
    assert combined["model_dir_bound"] is True
    assert combined["adapter_dir_bound"] is True
    assert combined["runtime_assets_verified"] is True
    assert combined["model_weights_loaded"] is False


def test_v8_bad_observer_receipt_is_rejected_upstream():
    m = _load()
    record = _v8_receipt(m)
    record["assets"][0]["observation"]["actual_sha256"] = "0" * 64
    _expect_hold(
        Exception,
        "V8 actual SHA-256 drift",
        lambda: m.integrate_v8_partial_evidence(
            record,
            path_input_record=_v8_paths(m),
            environment_fact=_v8_fact(m),
        ),
    )


def test_v8_bad_environment_fact_is_rejected_upstream():
    m = _load()
    fact = _v8_fact(m)
    fact["pip_freeze_sha256"] = "0" * 64
    _expect_hold(
        Exception,
        "V8 runtime pip-freeze SHA-256 drift",
        lambda: m.integrate_v8_partial_evidence(
            _v8_receipt(m),
            path_input_record=_v8_paths(m),
            environment_fact=fact,
        ),
    )


def test_v8_integrator_never_claims_collection_or_execution():
    m = _load()
    out = m.integrate_v8_partial_evidence(
        _v8_receipt(m),
        path_input_record=_v8_paths(m),
        environment_fact=_v8_fact(m),
    )
    assert out["live_observation_performed_by_integrator"] is False
    assert out["pip_freeze_performed_by_integrator"] is False
    assert out["observer_invocation_performed_by_integrator"] is False
    assert out["runtime_selection_performed"] is False
    assert out["runtime_started"] is False
    assert out["runtime_execution_authorized"] is False


def test_v2r13_without_portable_fact_keeps_contract_identity_false():
    m = _load()
    out = m.integrate_v2r13_partial_evidence(
        _v2_receipt(m),
        path_input_record=_v2_paths(m),
    )
    assert out["portable_contract_identity_valid"] is False
    assert out["portable_binding_attested"] is False
    assert out["activation_evidence_shape_complete"] is False
    assert out["runtime_readiness_admitted"] is False


def test_v2r13_with_portable_fact_binds_contract_only():
    m = _load()
    out = m.integrate_v2r13_partial_evidence(
        _v2_receipt(m),
        path_input_record=_v2_paths(m),
        portable_contract_fact=_v2_fact(m),
    )
    assert out["portable_contract_identity_valid"] is True
    assert out["portable_binding_attested"] is False
    assert "portable_binding_attested" in out["unresolved_activation_evidence_fields"]
    assert out["activation_evidence_shape_complete"] is False
    assert out["collector_identity_admitted"] is False
    assert out["runtime_readiness_admitted"] is False


def test_v2r13_combines_static_refs_and_git_fragment():
    m = _load()
    out = m.integrate_v2r13_partial_evidence(
        _v2_receipt(m),
        path_input_record=_v2_paths(m),
        portable_contract_fact=_v2_fact(m),
    )
    combined = out["combined_supported_activation_evidence_fields"]
    requirement = m.shape_progress.evidence_requirement(m.V2R13)
    for key, value in requirement["expected"].items():
        assert combined[key] == value
    assert combined["frozen_source_worktree"]["path"] == "/srv/void/g2/v2r13/source"
    assert combined["frozen_source_worktree"]["clean"] is True
    assert combined["frozen_source_worktree"]["detached"] is True
    assert combined["engine_worktree"]["path"] == "/srv/void/g2/v2r13/engine"
    assert combined["engine_worktree"]["clean"] is True


def test_v2r13_path_classification_remains_unresolved():
    m = _load()
    out = m.integrate_v2r13_partial_evidence(
        _v2_receipt(m),
        path_input_record=_v2_paths(m),
        portable_contract_fact=_v2_fact(m),
    )
    unresolved = out["unresolved_activation_evidence_fields"]
    for field in (
        "frozen_source_worktree.exists",
        "frozen_source_worktree.is_directory",
        "frozen_source_worktree.is_symlink",
        "engine_worktree.exists",
        "engine_worktree.is_directory",
        "engine_worktree.is_symlink",
    ):
        assert field in unresolved


def test_v2r13_live_runtime_identity_fields_remain_unresolved():
    m = _load()
    out = m.integrate_v2r13_partial_evidence(
        _v2_receipt(m),
        path_input_record=_v2_paths(m),
        portable_contract_fact=_v2_fact(m),
    )
    unresolved = out["unresolved_activation_evidence_fields"]
    for field in (
        "collector_contract_sha256",
        "endpoint_liveness",
        "model_identity_verified",
        "runtime_image_identity_verified",
        "portable_binding_attested",
    ):
        assert field in unresolved


def test_v2r13_bad_git_receipt_is_rejected_upstream():
    m = _load()
    record = _v2_receipt(m)
    record["source_head_commit"] = "0" * 40
    _expect_hold(
        Exception,
        "V2R13 source HEAD drift",
        lambda: m.integrate_v2r13_partial_evidence(
            record,
            path_input_record=_v2_paths(m),
            portable_contract_fact=_v2_fact(m),
        ),
    )


def test_v2r13_bad_portable_contract_is_rejected_upstream():
    m = _load()
    fact = _v2_fact(m)
    fact["binding_contract"] = deepcopy(fact["binding_contract"])
    fact["binding_contract"]["frozen_engine_commit"] = "0" * 40
    _expect_hold(
        Exception,
        "V2R13 portable binding contract identity drift",
        lambda: m.integrate_v2r13_partial_evidence(
            _v2_receipt(m),
            path_input_record=_v2_paths(m),
            portable_contract_fact=fact,
        ),
    )


def test_v2r13_integrator_never_claims_live_git_or_execution():
    m = _load()
    out = m.integrate_v2r13_partial_evidence(
        _v2_receipt(m),
        path_input_record=_v2_paths(m),
        portable_contract_fact=_v2_fact(m),
    )
    assert out["live_observation_performed_by_integrator"] is False
    assert out["external_worktree_git_query_performed_by_integrator"] is False
    assert out["observer_invocation_performed_by_integrator"] is False
    assert out["runtime_selection_performed"] is False
    assert out["runtime_started"] is False
    assert out["runtime_execution_authorized"] is False


def test_dispatch_rejects_unsupported_snapshot():
    m = _load()
    _expect_hold(
        m.RuntimeEvidenceIntegrationHold,
        "unsupported partial-evidence integration snapshot",
        lambda: m.integrate_partial_evidence(
            "not-reviewed",
            {},
            path_input_record={},
        ),
    )


def test_collection_or_admission_entrypoint_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeEvidenceIntegrationHold,
        "GENERATION2_INTEGRATED_EVIDENCE_COLLECTION_OR_ADMISSION_NOT_IMPLEMENTED",
        lambda: m.collect_or_admit_integrated_evidence(),
    )
