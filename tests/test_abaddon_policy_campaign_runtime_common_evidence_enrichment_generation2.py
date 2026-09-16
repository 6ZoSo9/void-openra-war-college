from __future__ import annotations

import ast
import hashlib
import importlib.util
import sys
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_common_evidence_enrichment_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_common_evidence_enrichment_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "1ddef9404efe938455cc325dd067f13e78f1f1d101a051ef06b01691ff18970f"


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
        "_void_abaddon_g2_common_evidence_enrichment",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _v8_integrated(m, *, with_environment=True):
    ae = m.completion_accounting.activation_evidence
    expected = dict(ae.evidence_requirement(m.V8)["expected"])
    combined = {
        **expected,
        "model_dir": "/srv/void/g2/v8/model",
        "adapter_dir": "/srv/void/g2/v8/adapter",
        "model_dir_bound": True,
        "adapter_dir_bound": True,
        "runtime_assets_verified": True,
        "model_weights_loaded": False,
    }
    unresolved = [
        "collector_contract_sha256",
        "offline_only_verified",
        "load_call_performed",
    ]
    if with_environment:
        combined["runtime_environment_verified"] = True
    else:
        unresolved.insert(1, "runtime_environment_verified")

    return {
        "schema": m.evidence_integration.INTEGRATION_SCHEMA,
        "snapshot_id": m.V8,
        "combined_supported_activation_evidence_fields": combined,
        "unresolved_activation_evidence_fields": tuple(unresolved),
        "activation_evidence_shape_complete": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "holds": ("BASE_PARTIAL_HOLD",),
    }


def _v2_integrated(m):
    ae = m.completion_accounting.activation_evidence
    req = ae.evidence_requirement(m.V2R13)
    expected = dict(req["expected"])
    combined = {
        **expected,
        "frozen_source_worktree": {
            "path": "/srv/void/g2/v2r13/source",
            "clean": True,
            "detached": True,
            "head_commit": expected["frozen_war_college_commit"],
            "tree_sha": expected["frozen_war_college_tree"],
        },
        "engine_worktree": {
            "path": "/srv/void/g2/v2r13/engine",
            "clean": True,
            "head_commit": expected["frozen_engine_commit"],
        },
    }
    unresolved = (
        "collector_contract_sha256",
        "endpoint_liveness",
        "model_identity_verified",
        "runtime_image_identity_verified",
        "portable_binding_attested",
        "frozen_source_worktree.exists",
        "frozen_source_worktree.is_directory",
        "frozen_source_worktree.is_symlink",
        "engine_worktree.exists",
        "engine_worktree.is_directory",
        "engine_worktree.is_symlink",
    )
    return {
        "schema": m.evidence_integration.INTEGRATION_SCHEMA,
        "snapshot_id": m.V2R13,
        "combined_supported_activation_evidence_fields": combined,
        "unresolved_activation_evidence_fields": unresolved,
        "activation_evidence_shape_complete": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "holds": ("BASE_PARTIAL_HOLD",),
    }


def test_contract_preserves_non_admitting_boundary():
    m = _load()
    out = m.common_evidence_enrichment_contract()
    assert out["preserves_integration_schema"] is True
    assert out["supported_snapshot_ids"] == (m.V2R13, m.V8)
    assert out["common_static_identity_enrichment_implemented"] is True
    assert out["common_operational_hold_propagation_implemented"] is True
    assert out["all_required_leaf_classification_implemented"] is True
    assert out["zero_unaccounted_means_readiness"] is False
    assert out["operational_observation_evidence_implemented"] is False
    assert out["collector_contract_identity_support_implemented"] is False
    assert out["activation_evidence_shape_completion_implemented"] is False
    assert out["collector_identity_admission_implemented"] is False
    assert out["runtime_readiness_admission_implemented"] is False
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
        "observe_v8_assets",
        "observe_v2r13_git_identity",
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
        m.RuntimeCommonEvidenceEnrichmentHold,
        "common enrichment supported-field conflict: a",
        lambda: m._merge_supported_fields({"a": 1}, {"a": 2}),
    )


def test_v8_with_environment_becomes_20_supported_9_unresolved_zero_unaccounted():
    m = _load()
    out = m.enrich_integrated_evidence(_v8_integrated(m))
    assert out["post_enrichment_required_leaf_count"] == 29
    assert out["post_enrichment_supported_leaf_count"] == 20
    assert out["post_enrichment_unresolved_leaf_count"] == 9
    assert out["post_enrichment_unaccounted_leaf_count"] == 0
    assert out["post_enrichment_all_required_paths_accounted"] is True
    assert out["post_enrichment_all_required_paths_resolved"] is False


def test_v8_without_environment_becomes_19_supported_10_unresolved_zero_unaccounted():
    m = _load()
    out = m.enrich_integrated_evidence(
        _v8_integrated(m, with_environment=False)
    )
    assert out["post_enrichment_required_leaf_count"] == 29
    assert out["post_enrichment_supported_leaf_count"] == 19
    assert out["post_enrichment_unresolved_leaf_count"] == 10
    assert out["post_enrichment_unaccounted_leaf_count"] == 0


def test_v2r13_becomes_18_supported_17_unresolved_zero_unaccounted():
    m = _load()
    out = m.enrich_integrated_evidence(_v2_integrated(m))
    assert out["post_enrichment_required_leaf_count"] == 35
    assert out["post_enrichment_supported_leaf_count"] == 18
    assert out["post_enrichment_unresolved_leaf_count"] == 17
    assert out["post_enrichment_unaccounted_leaf_count"] == 0
    assert out["post_enrichment_all_required_paths_accounted"] is True
    assert out["post_enrichment_all_required_paths_resolved"] is False


def test_v8_common_identity_fields_are_added_exactly():
    m = _load()
    out = m.enrich_integrated_evidence(_v8_integrated(m))
    combined = out["combined_supported_activation_evidence_fields"]
    common = m.common_shape.compose_common_evidence_shape(m.V8)
    for key, value in common["supported_activation_evidence_fields"].items():
        assert combined[key] == value
    assert out["common_static_identity_supported_field_count"] == 5


def test_v2r13_common_identity_fields_are_added_exactly():
    m = _load()
    out = m.enrich_integrated_evidence(_v2_integrated(m))
    combined = out["combined_supported_activation_evidence_fields"]
    common = m.common_shape.compose_common_evidence_shape(m.V2R13)
    for key, value in common["supported_activation_evidence_fields"].items():
        assert combined[key] == value
    assert out["common_static_identity_supported_field_count"] == 5


def test_common_operational_fields_are_carried_as_unresolved():
    m = _load()
    for record in (_v8_integrated(m), _v2_integrated(m)):
        out = m.enrich_integrated_evidence(record)
        unresolved = out["unresolved_activation_evidence_fields"]
        for field in m.common_shape.OPERATIONAL_COMMON_FIELDS:
            assert field in unresolved
        assert out["common_operational_unresolved_field_count"] == 6


def test_collector_contract_remains_unresolved():
    m = _load()
    for record in (_v8_integrated(m), _v2_integrated(m)):
        out = m.enrich_integrated_evidence(record)
        assert "collector_contract_sha256" in out[
            "unresolved_activation_evidence_fields"
        ]
        assert "collector_contract_sha256" not in out[
            "combined_supported_activation_evidence_fields"
        ]


def test_zero_unaccounted_never_claims_readiness():
    m = _load()
    for record in (_v8_integrated(m), _v2_integrated(m)):
        out = m.enrich_integrated_evidence(record)
        assert out["post_enrichment_unaccounted_leaf_count"] == 0
        assert out["activation_evidence_shape_complete"] is False
        assert out["collector_identity_admitted"] is False
        assert out["runtime_readiness_admitted"] is False
        assert out["runtime_execution_authorized"] is False


def test_integration_schema_is_preserved():
    m = _load()
    for record in (_v8_integrated(m), _v2_integrated(m)):
        out = m.enrich_integrated_evidence(record)
        assert out["schema"] == m.evidence_integration.INTEGRATION_SCHEMA


def test_preclaimed_complete_record_is_rejected():
    m = _load()
    record = _v8_integrated(m)
    record["activation_evidence_shape_complete"] = True
    _expect_hold(
        m.RuntimeCommonEvidenceEnrichmentHold,
        "refuses pre-claimed complete evidence",
        lambda: m.enrich_integrated_evidence(record),
    )


def test_preadmitted_collector_is_rejected():
    m = _load()
    record = _v8_integrated(m)
    record["collector_identity_admitted"] = True
    _expect_hold(
        m.RuntimeCommonEvidenceEnrichmentHold,
        "refuses pre-admitted collector identity",
        lambda: m.enrich_integrated_evidence(record),
    )


def test_preadmitted_readiness_is_rejected():
    m = _load()
    record = _v8_integrated(m)
    record["runtime_readiness_admitted"] = True
    _expect_hold(
        m.RuntimeCommonEvidenceEnrichmentHold,
        "refuses pre-admitted runtime readiness",
        lambda: m.enrich_integrated_evidence(record),
    )


def test_runtime_authority_is_rejected():
    m = _load()
    record = _v8_integrated(m)
    record["runtime_execution_authorized"] = True
    _expect_hold(
        m.RuntimeCommonEvidenceEnrichmentHold,
        "refuses runtime execution authority",
        lambda: m.enrich_integrated_evidence(record),
    )


def test_integration_schema_drift_is_rejected():
    m = _load()
    record = _v8_integrated(m)
    record["schema"] = "not-the-integration-schema"
    _expect_hold(
        m.RuntimeCommonEvidenceEnrichmentHold,
        "integrated evidence schema drift",
        lambda: m.enrich_integrated_evidence(record),
    )


def test_unsupported_snapshot_is_rejected():
    m = _load()
    record = _v8_integrated(m)
    record["snapshot_id"] = "not-reviewed"
    _expect_hold(
        m.RuntimeCommonEvidenceEnrichmentHold,
        "unsupported common-evidence enrichment snapshot",
        lambda: m.enrich_integrated_evidence(record),
    )


def test_collection_or_admission_entrypoint_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeCommonEvidenceEnrichmentHold,
        "GENERATION2_COMMON_EVIDENCE_ENRICHMENT_COLLECTION_OR_ADMISSION_NOT_IMPLEMENTED",
        lambda: m.collect_or_admit_enriched_evidence(),
    )
