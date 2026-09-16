from __future__ import annotations

import ast
import hashlib
import importlib.util
import sys
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_evidence_shape_progress_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_evidence_shape_progress_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "c6bdef2213ebbebe479ce37eeaa93c6634634942054ded1efb188c1d024a427f"


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
        "_void_abaddon_g2_runtime_evidence_shape_progress",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _v8_fact(m):
    return {
        "schema": m.FACT_SCHEMA,
        "snapshot_id": m.V8,
        "fact_kind": m.V8_ENVIRONMENT_FACT_KIND,
        "python_major_minor": list(m.v8_runtime.RUNTIME_PYTHON_MAJOR_MINOR),
        "pip_freeze_sha256": m.v8_runtime.RUNTIME_PIP_FREEZE_SHA256,
        "fact_source": m.FACT_SOURCE,
        "live_collection_performed": False,
        "collector_identity_admitted": False,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
    }


def _v2_fact(m):
    return {
        "schema": m.FACT_SCHEMA,
        "snapshot_id": m.V2R13,
        "fact_kind": m.V2R13_PORTABLE_CONTRACT_FACT_KIND,
        "binding_contract": m.v2_portable.portable_binding_contract(),
        "fact_source": m.FACT_SOURCE,
        "live_binding_installation_attested": False,
        "collector_identity_admitted": False,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_execution_performed": False,
    }


def test_contract_preserves_no_collection_and_no_admission():
    m = _load()
    out = m.evidence_shape_progress_contract()
    assert out["v8_static_identity_shape_composition_implemented"] is True
    assert out["v8_supplied_environment_fact_validation_implemented"] is True
    assert out["v8_live_environment_collection_implemented"] is False
    assert out["v8_environment_collector_provenance_admitted"] is False
    assert out["v2r13_portable_contract_identity_validation_implemented"] is True
    assert out["v2r13_live_portable_binding_attestation_implemented"] is False
    assert out["final_activation_evidence_shape_composition_implemented"] is False
    assert out["collector_identity_admission_implemented"] is False
    assert out["runtime_readiness_admission_implemented"] is False
    assert out["live_observation_performed"] is False
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
        "v8_runtime.verify_v8_runtime_environment",
        "v8_runtime.verify_v8_runtime_assets",
        "v8_runtime.FrozenV8LocalToolRuntime.load",
        "v2_portable.PortableRunnerBinding",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call):
            assert _dotted(node.func) not in forbidden_calls


def test_v8_valid_supplied_environment_fact_uses_pure_validator():
    m = _load()
    out = m.validate_v8_environment_fact(_v8_fact(m))
    assert out["supplied_fact_shape_valid"] is True
    assert out["canonical_pure_validator_applied"] is True
    assert out["environment_identity_values_valid"] is True
    assert out["live_environment_collection_proven"] is False
    assert out["collector_identity_admitted"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False
    assert out["activation_evidence_shape_field_support"] == {
        "runtime_environment_verified": True,
    }


def test_v8_rejects_python_identity_drift():
    m = _load()
    record = _v8_fact(m)
    record["python_major_minor"] = [3, 11]
    _expect_hold(
        Exception,
        "V8 runtime Python major/minor drift",
        lambda: m.validate_v8_environment_fact(record),
    )


def test_v8_rejects_package_identity_drift():
    m = _load()
    record = _v8_fact(m)
    record["pip_freeze_sha256"] = "0" * 64
    _expect_hold(
        Exception,
        "V8 runtime pip-freeze SHA-256 drift",
        lambda: m.validate_v8_environment_fact(record),
    )


def test_v8_rejects_authority_boundary_crossing():
    m = _load()
    for field in (
        "live_collection_performed",
        "collector_identity_admitted",
        "runtime_execution_performed",
        "model_execution_performed",
    ):
        record = _v8_fact(m)
        record[field] = True
        _expect_hold(
            m.RuntimeEvidenceShapeProgressHold,
            f"supplied fact crossed authority boundary: {field}",
            lambda record=record: m.validate_v8_environment_fact(record),
        )


def test_v8_progress_without_environment_fact_keeps_environment_unresolved():
    m = _load()
    out = m.v8_evidence_shape_progress()
    assert out["source_static_activation_evidence_fields"] == dict(
        m.evidence_requirement(m.V8)["expected"]
    )
    assert out["supplied_fact_activation_evidence_fields"] == {}
    assert "runtime_environment_verified" in out["unresolved_activation_evidence_fields"]
    assert out["activation_evidence_shape_complete"] is False
    assert out["collector_identity_admitted"] is False
    assert out["runtime_readiness_admitted"] is False


def test_v8_progress_with_environment_fact_closes_shape_value_only():
    m = _load()
    out = m.v8_evidence_shape_progress(_v8_fact(m))
    assert out["supplied_fact_activation_evidence_fields"] == {
        "runtime_environment_verified": True,
    }
    assert "runtime_environment_verified" not in out["unresolved_activation_evidence_fields"]
    assert "offline_only_verified" in out["unresolved_activation_evidence_fields"]
    assert "load_call_performed" in out["unresolved_activation_evidence_fields"]
    assert out["activation_evidence_shape_complete"] is False
    assert out["collector_identity_admitted"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["pip_freeze_performed"] is False


def test_v8_progress_does_not_claim_asset_or_path_evidence():
    m = _load()
    out = m.v8_evidence_shape_progress(_v8_fact(m))
    unresolved = out["unresolved_activation_evidence_fields"]
    for field in (
        "model_dir",
        "adapter_dir",
        "model_dir_bound",
        "adapter_dir_bound",
        "runtime_assets_verified",
        "model_weights_loaded",
    ):
        assert field in unresolved


def test_v2r13_valid_portable_contract_fact_is_identity_only():
    m = _load()
    out = m.validate_v2r13_portable_contract_fact(_v2_fact(m))
    assert out["supplied_fact_shape_valid"] is True
    assert out["canonical_pure_contract_applied"] is True
    assert out["portable_contract_identity_valid"] is True
    assert out["live_binding_installation_attested"] is False
    assert out["activation_evidence_shape_field_support"] == {}
    assert out["collector_identity_admitted"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_v2r13_rejects_portable_contract_identity_drift():
    m = _load()
    record = _v2_fact(m)
    record["binding_contract"] = deepcopy(record["binding_contract"])
    record["binding_contract"]["frozen_engine_commit"] = "0" * 40
    _expect_hold(
        m.RuntimeEvidenceShapeProgressHold,
        "V2R13 portable binding contract identity drift",
        lambda: m.validate_v2r13_portable_contract_fact(record),
    )


def test_v2r13_rejects_live_binding_or_execution_claims():
    m = _load()
    for field in (
        "live_binding_installation_attested",
        "collector_identity_admitted",
        "runtime_execution_performed",
        "model_execution_performed",
        "game_execution_performed",
    ):
        record = _v2_fact(m)
        record[field] = True
        _expect_hold(
            m.RuntimeEvidenceShapeProgressHold,
            f"supplied fact crossed authority boundary: {field}",
            lambda record=record: m.validate_v2r13_portable_contract_fact(record),
        )


def test_v2r13_progress_without_fact_remains_unattested():
    m = _load()
    out = m.v2r13_evidence_shape_progress()
    assert out["portable_contract_identity_valid"] is False
    assert out["portable_binding_attested"] is False
    assert out["supported_activation_evidence_fields"] == {}
    assert out["activation_evidence_shape_complete"] is False
    assert out["collector_identity_admitted"] is False
    assert out["runtime_readiness_admitted"] is False


def test_v2r13_progress_with_fact_binds_contract_but_not_live_attestation():
    m = _load()
    out = m.v2r13_evidence_shape_progress(_v2_fact(m))
    assert out["portable_contract_identity_valid"] is True
    assert out["portable_binding_attested"] is False
    assert out["supported_activation_evidence_fields"] == {}
    assert "portable_binding_attested" in out["unresolved_activation_evidence_fields"]
    assert out["activation_evidence_shape_complete"] is False
    assert out["runtime_readiness_admitted"] is False


def test_v2r13_static_expected_references_match_activation_requirement():
    m = _load()
    out = m.v2r13_evidence_shape_progress(_v2_fact(m))
    assert out["expected_static_reference_fields"] == dict(
        m.evidence_requirement(m.V2R13)["expected"]
    )


def test_collection_entrypoint_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeEvidenceShapeProgressHold,
        "GENERATION2_EVIDENCE_SHAPE_PROGRESS_COLLECTION_NOT_IMPLEMENTED",
        lambda: m.collect_evidence_shape_progress(),
    )


def test_no_progress_path_admits_runtime_authority():
    m = _load()
    results = (
        m.v8_evidence_shape_progress(),
        m.v8_evidence_shape_progress(_v8_fact(m)),
        m.v2r13_evidence_shape_progress(),
        m.v2r13_evidence_shape_progress(_v2_fact(m)),
    )
    for out in results:
        assert out["activation_evidence_shape_complete"] is False
        assert out["collector_identity_admitted"] is False
        assert out["runtime_readiness_admitted"] is False
        assert out["live_observation_performed"] is False
        assert out["runtime_execution_authorized"] is False
