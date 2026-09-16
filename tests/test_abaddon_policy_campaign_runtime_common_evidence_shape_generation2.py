from __future__ import annotations

import ast
import hashlib
import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_common_evidence_shape_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_common_evidence_shape_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "d41f7ed063c858dd2c977df17badc1585c151d8ada7cd0b07f8a9843f0186aa0"


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
        "_void_abaddon_g2_common_evidence_shape",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_contract_is_source_identity_only():
    m = _load()
    out = m.common_evidence_shape_contract()
    assert out["supported_snapshot_ids"] == (m.V2R13, m.V8)
    assert out["static_identity_fields"] == m.STATIC_IDENTITY_FIELDS
    assert out["operational_common_fields"] == m.OPERATIONAL_COMMON_FIELDS
    assert out["static_identity_shape_composition_implemented"] is True
    assert out["operational_observation_evidence_implemented"] is False
    assert out["collector_contract_identity_support_implemented"] is False
    assert out["activation_evidence_shape_completion_implemented"] is False
    assert out["collector_identity_admission_implemented"] is False
    assert out["runtime_readiness_admission_implemented"] is False
    assert out["live_observation_performed"] is False
    assert out["collector_execution_performed"] is False
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
    forbidden_call_fragments = {
        "observe",
        "verify_v8_runtime_environment",
        "verify_v8_runtime_assets",
        "host_file_observation_backend",
        "host_git_runner",
        "host_path_resolver",
        "PortableRunnerBinding",
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


def test_v8_supported_fields_are_exact_five_static_identity_fields():
    m = _load()
    out = m.compose_common_evidence_shape(m.V8)
    supported = out["supported_activation_evidence_fields"]
    assert tuple(supported) == m.STATIC_IDENTITY_FIELDS
    assert len(supported) == 5
    assert out["supported_static_identity_field_count"] == 5


def test_v2r13_supported_fields_are_exact_five_static_identity_fields():
    m = _load()
    out = m.compose_common_evidence_shape(m.V2R13)
    supported = out["supported_activation_evidence_fields"]
    assert tuple(supported) == m.STATIC_IDENTITY_FIELDS
    assert len(supported) == 5
    assert out["supported_static_identity_field_count"] == 5


def test_v8_static_identity_values_match_canonical_requirement():
    m = _load()
    out = m.compose_common_evidence_shape(m.V8)
    req = m.activation_evidence.evidence_requirement(m.V8)
    supported = out["supported_activation_evidence_fields"]
    assert supported["schema"] == m.activation_evidence.EVIDENCE_SCHEMA
    assert supported["snapshot_id"] == req["snapshot_id"]
    assert supported["snapshot_sha256"] == req["snapshot_sha256"]
    assert supported["runtime_class"] == req["runtime_class"]
    assert supported["evidence_kind"] == req["evidence_kind"]


def test_v2r13_static_identity_values_match_canonical_requirement():
    m = _load()
    out = m.compose_common_evidence_shape(m.V2R13)
    req = m.activation_evidence.evidence_requirement(m.V2R13)
    supported = out["supported_activation_evidence_fields"]
    assert supported["schema"] == m.activation_evidence.EVIDENCE_SCHEMA
    assert supported["snapshot_id"] == req["snapshot_id"]
    assert supported["snapshot_sha256"] == req["snapshot_sha256"]
    assert supported["runtime_class"] == req["runtime_class"]
    assert supported["evidence_kind"] == req["evidence_kind"]


def test_operational_common_fields_are_exact_six_and_unresolved():
    m = _load()
    expected = (
        "observation_mode",
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "game_execution_performed",
        "model_inference_performed",
    )
    assert m.OPERATIONAL_COMMON_FIELDS == expected
    for snapshot_id in (m.V8, m.V2R13):
        out = m.compose_common_evidence_shape(snapshot_id)
        assert out["unresolved_activation_evidence_fields"] == expected
        assert out["unresolved_operational_field_count"] == 6


def test_operational_fields_are_never_reported_as_supported():
    m = _load()
    for snapshot_id in (m.V8, m.V2R13):
        out = m.compose_common_evidence_shape(snapshot_id)
        supported = out["supported_activation_evidence_fields"]
        assert not (set(supported) & set(m.OPERATIONAL_COMMON_FIELDS))
        assert out["operational_requirements_supported_as_evidence"] is False


def test_collector_contract_identity_is_not_inferred():
    m = _load()
    for snapshot_id in (m.V8, m.V2R13):
        out = m.compose_common_evidence_shape(snapshot_id)
        assert "collector_contract_sha256" not in out["supported_activation_evidence_fields"]
        assert out["collector_contract_sha256_supported"] is False


def test_v8_required_false_contract_contains_all_common_operational_false_fields():
    m = _load()
    req = m.activation_evidence.evidence_requirement(m.V8)
    for field in m.activation_evidence.COMMON_REQUIRED_FALSE:
        assert field in req["required_false"]


def test_v2r13_required_false_contract_is_exact_common_operational_false_fields():
    m = _load()
    req = m.activation_evidence.evidence_requirement(m.V2R13)
    assert req["required_false"] == m.activation_evidence.COMMON_REQUIRED_FALSE


def test_all_common_identity_and_operational_paths_are_required_fields():
    m = _load()
    for snapshot_id in (m.V8, m.V2R13):
        req = m.activation_evidence.evidence_requirement(snapshot_id)
        required = set(req["required_fields"])
        assert set(m.STATIC_IDENTITY_FIELDS).issubset(required)
        assert set(m.OPERATIONAL_COMMON_FIELDS).issubset(required)


def test_unsupported_promoted_loopback_snapshot_is_rejected():
    m = _load()
    _expect_hold(
        m.RuntimeCommonEvidenceShapeHold,
        "unsupported common-evidence-shape snapshot",
        lambda: m.compose_common_evidence_shape("not-reviewed"),
    )


def test_common_shape_never_claims_completion_admission_or_execution():
    m = _load()
    for snapshot_id in (m.V8, m.V2R13):
        out = m.compose_common_evidence_shape(snapshot_id)
        assert out["activation_evidence_shape_complete"] is False
        assert out["collector_identity_admitted"] is False
        assert out["runtime_readiness_admitted"] is False
        assert out["live_observation_performed"] is False
        assert out["collector_executed"] is False
        assert out["runtime_execution_authorized"] is False


def test_collection_or_admission_entrypoint_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeCommonEvidenceShapeHold,
        "GENERATION2_COMMON_EVIDENCE_COLLECTION_OR_ADMISSION_NOT_IMPLEMENTED",
        lambda: m.collect_or_admit_common_evidence(),
    )
