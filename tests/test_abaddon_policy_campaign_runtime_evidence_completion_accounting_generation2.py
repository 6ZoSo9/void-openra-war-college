from __future__ import annotations

import ast
import hashlib
import importlib.util
import sys
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_evidence_completion_accounting_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_evidence_completion_accounting_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "4195573dad83c9dee0dc8206c84366b9843b9dc968e865ebac032a457ac07325"


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
        "_void_abaddon_g2_completion_accounting",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _v8_integrated(m, *, with_environment=True):
    expected = dict(m.activation_evidence.evidence_requirement(m.V8)["expected"])
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
        "schema": "void.abaddon.generation2.runtime-evidence-integration.v1",
        "snapshot_id": m.V8,
        "combined_supported_activation_evidence_fields": combined,
        "unresolved_activation_evidence_fields": tuple(unresolved),
        "activation_evidence_shape_complete": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
    }


def _v2_integrated(m):
    req = m.activation_evidence.evidence_requirement(m.V2R13)
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
        "schema": "void.abaddon.generation2.runtime-evidence-integration.v1",
        "snapshot_id": m.V2R13,
        "combined_supported_activation_evidence_fields": combined,
        "unresolved_activation_evidence_fields": unresolved,
        "activation_evidence_shape_complete": False,
        "collector_identity_admitted": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
    }


def test_contract_is_descriptive_only_and_non_admitting():
    m = _load()
    out = m.evidence_completion_accounting_contract()
    assert out["required_leaf_path_accounting_implemented"] is True
    assert out["nested_v2r13_leaf_accounting_implemented"] is True
    assert out["reference_only_field_separation_implemented"] is True
    assert out["supported_unresolved_overlap_rejection_implemented"] is True
    assert out["completion_counts_are_descriptive_only"] is True
    assert out["activation_evidence_shape_completion_implemented"] is False
    assert out["collector_identity_admission_implemented"] is False
    assert out["runtime_readiness_admission_implemented"] is False
    assert out["live_observation_performed"] is False
    assert out["collector_execution_performed"] is False
    assert out["runtime_execution_authorized"] is False


def test_v8_required_leaf_count_is_exact_29():
    m = _load()
    paths = m._required_leaf_paths(m.V8)
    assert len(paths) == 29
    assert len(paths) == len(set(paths))
    assert "collector_contract_sha256" in paths
    assert "runtime_environment_verified" in paths
    assert "offline_only_verified" in paths
    assert "load_call_performed" in paths


def test_v2r13_required_leaf_count_is_exact_35():
    m = _load()
    paths = m._required_leaf_paths(m.V2R13)
    assert len(paths) == 35
    assert len(paths) == len(set(paths))
    assert "frozen_source_worktree.path" in paths
    assert "frozen_source_worktree.exists" in paths
    assert "frozen_source_worktree.tree_sha" in paths
    assert "engine_worktree.path" in paths
    assert "engine_worktree.is_symlink" in paths
    assert "portable_binding_attested" in paths


def test_v8_with_environment_fact_accounts_15_supported_3_unresolved_11_unaccounted():
    m = _load()
    out = m.account_integrated_evidence(m.V8, _v8_integrated(m))
    assert out["required_leaf_count"] == 29
    assert out["supported_leaf_count"] == 15
    assert out["unresolved_leaf_count"] == 3
    assert out["unaccounted_leaf_count"] == 11
    assert out["reference_only_field_count"] == 0
    assert out["all_required_paths_accounted"] is False
    assert out["all_required_paths_resolved"] is False
    assert out["activation_evidence_shape_complete"] is False
    assert out["collector_identity_admitted"] is False
    assert out["runtime_readiness_admitted"] is False


def test_v8_without_environment_fact_accounts_14_supported_4_unresolved_11_unaccounted():
    m = _load()
    out = m.account_integrated_evidence(
        m.V8,
        _v8_integrated(m, with_environment=False),
    )
    assert out["required_leaf_count"] == 29
    assert out["supported_leaf_count"] == 14
    assert out["unresolved_leaf_count"] == 4
    assert out["unaccounted_leaf_count"] == 11
    assert "runtime_environment_verified" in out["unresolved_leaf_paths"]


def test_v8_common_evidence_claims_remain_unaccounted():
    m = _load()
    out = m.account_integrated_evidence(m.V8, _v8_integrated(m))
    for path in (
        "schema",
        "snapshot_id",
        "snapshot_sha256",
        "runtime_class",
        "evidence_kind",
        "observation_mode",
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "game_execution_performed",
        "model_inference_performed",
    ):
        assert path in out["unaccounted_leaf_paths"]


def test_v2r13_accounts_13_supported_11_unresolved_11_unaccounted():
    m = _load()
    out = m.account_integrated_evidence(m.V2R13, _v2_integrated(m))
    assert out["required_leaf_count"] == 35
    assert out["supported_leaf_count"] == 13
    assert out["unresolved_leaf_count"] == 11
    assert out["unaccounted_leaf_count"] == 11
    assert out["all_required_paths_accounted"] is False
    assert out["all_required_paths_resolved"] is False


def test_v2r13_reference_only_static_keys_are_not_counted_as_evidence():
    m = _load()
    out = m.account_integrated_evidence(m.V2R13, _v2_integrated(m))
    assert out["reference_only_field_count"] == 3
    assert set(out["reference_only_fields"]) == {
        "frozen_war_college_commit",
        "frozen_war_college_tree",
        "frozen_engine_commit",
    }
    for key in out["reference_only_fields"]:
        assert key not in out["required_leaf_paths"]
        assert key not in out["supported_leaf_paths"]


def test_v2r13_nested_partial_support_is_leaf_precise():
    m = _load()
    out = m.account_integrated_evidence(m.V2R13, _v2_integrated(m))
    for path in (
        "frozen_source_worktree.path",
        "frozen_source_worktree.clean",
        "frozen_source_worktree.detached",
        "frozen_source_worktree.head_commit",
        "frozen_source_worktree.tree_sha",
        "engine_worktree.path",
        "engine_worktree.clean",
        "engine_worktree.head_commit",
    ):
        assert path in out["supported_leaf_paths"]
    for path in (
        "frozen_source_worktree.exists",
        "frozen_source_worktree.is_directory",
        "frozen_source_worktree.is_symlink",
        "engine_worktree.exists",
        "engine_worktree.is_directory",
        "engine_worktree.is_symlink",
    ):
        assert path in out["unresolved_leaf_paths"]


def test_supported_unresolved_overlap_is_rejected():
    m = _load()
    record = _v8_integrated(m)
    record["unresolved_activation_evidence_fields"] = (
        *record["unresolved_activation_evidence_fields"],
        "runtime_assets_verified",
    )
    _expect_hold(
        m.RuntimeEvidenceCompletionAccountingHold,
        "evidence paths both supported and unresolved",
        lambda: m.account_integrated_evidence(m.V8, record),
    )


def test_unknown_unresolved_path_is_rejected():
    m = _load()
    record = _v8_integrated(m)
    record["unresolved_activation_evidence_fields"] = (
        *record["unresolved_activation_evidence_fields"],
        "not_a_required_field",
    )
    _expect_hold(
        m.RuntimeEvidenceCompletionAccountingHold,
        "unresolved non-required evidence paths",
        lambda: m.account_integrated_evidence(m.V8, record),
    )


def test_unknown_nested_supported_child_is_rejected():
    m = _load()
    record = _v2_integrated(m)
    record = deepcopy(record)
    record["combined_supported_activation_evidence_fields"][
        "frozen_source_worktree"
    ]["invented"] = True
    _expect_hold(
        m.RuntimeEvidenceCompletionAccountingHold,
        "unsupported frozen_source_worktree child fields",
        lambda: m.account_integrated_evidence(m.V2R13, record),
    )


def test_preclaimed_complete_record_is_rejected():
    m = _load()
    record = _v8_integrated(m)
    record["activation_evidence_shape_complete"] = True
    _expect_hold(
        m.RuntimeEvidenceCompletionAccountingHold,
        "refuses pre-claimed complete evidence",
        lambda: m.account_integrated_evidence(m.V8, record),
    )


def test_preadmitted_collector_is_rejected():
    m = _load()
    record = _v8_integrated(m)
    record["collector_identity_admitted"] = True
    _expect_hold(
        m.RuntimeEvidenceCompletionAccountingHold,
        "refuses pre-admitted collector identity",
        lambda: m.account_integrated_evidence(m.V8, record),
    )


def test_preadmitted_readiness_is_rejected():
    m = _load()
    record = _v8_integrated(m)
    record["runtime_readiness_admitted"] = True
    _expect_hold(
        m.RuntimeEvidenceCompletionAccountingHold,
        "refuses pre-admitted runtime readiness",
        lambda: m.account_integrated_evidence(m.V8, record),
    )


def test_runtime_authority_is_rejected():
    m = _load()
    record = _v8_integrated(m)
    record["runtime_execution_authorized"] = True
    _expect_hold(
        m.RuntimeEvidenceCompletionAccountingHold,
        "refuses runtime execution authority",
        lambda: m.account_integrated_evidence(m.V8, record),
    )


def test_integration_schema_drift_is_rejected():
    m = _load()
    record = _v8_integrated(m)
    record["schema"] = "not-the-integration-schema"
    _expect_hold(
        m.RuntimeEvidenceCompletionAccountingHold,
        "integrated evidence schema drift",
        lambda: m.account_integrated_evidence(m.V8, record),
    )


def test_unsupported_snapshot_is_rejected():
    m = _load()
    _expect_hold(
        m.RuntimeEvidenceCompletionAccountingHold,
        "unsupported completion-accounting snapshot",
        lambda: m.account_integrated_evidence("not-reviewed", {}),
    )


def test_collection_or_admission_entrypoint_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeEvidenceCompletionAccountingHold,
        "GENERATION2_COMPLETION_ACCOUNTING_COLLECTION_OR_ADMISSION_NOT_IMPLEMENTED",
        lambda: m.collect_or_admit_completion_evidence(),
    )


def test_accounting_never_claims_execution_or_admission():
    m = _load()
    for snapshot_id, record in (
        (m.V8, _v8_integrated(m)),
        (m.V2R13, _v2_integrated(m)),
    ):
        out = m.account_integrated_evidence(snapshot_id, record)
        assert out["activation_evidence_shape_complete"] is False
        assert out["collector_identity_admitted"] is False
        assert out["runtime_readiness_admitted"] is False
        assert out["live_observation_performed"] is False
        assert out["collector_executed"] is False
        assert out["runtime_execution_authorized"] is False
