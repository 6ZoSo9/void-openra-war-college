from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import sys
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_collector_contract_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_collector_contract_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "c48ad0871d4ea25e45efcde36e59622d1bb6b2a2fc4a4ed1f25988b543c2038f"
EXPECTED_COLLECTOR_CONTRACT_SHA256 = (
    "d11e45cabc10b42e09ab5e328e1e63721b633c7cdcfd7492038ec286b7f3e657"
)


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
        "_void_abaddon_g2_collector_contract",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_contract_semantic_sha_is_exact_and_stable():
    m = _load()
    assert m.collector_contract_sha256() == EXPECTED_COLLECTOR_CONTRACT_SHA256
    out = m.validate_collector_contract()
    assert out["collector_contract_sha256"] == EXPECTED_COLLECTOR_CONTRACT_SHA256
    assert out["semantic_contract_valid"] is True


def test_manifest_canonical_roundtrip_matches_semantic_sha():
    m = _load()
    manifest = m.collector_contract_manifest()
    canonical = json.dumps(
        manifest,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")
    assert hashlib.sha256(canonical).hexdigest() == EXPECTED_COLLECTOR_CONTRACT_SHA256


def test_manifest_hash_changes_when_semantics_change():
    m = _load()
    manifest = deepcopy(m.collector_contract_manifest())
    manifest["collector_may_mutate"] = True
    canonical = json.dumps(
        manifest,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")
    assert hashlib.sha256(canonical).hexdigest() != EXPECTED_COLLECTOR_CONTRACT_SHA256


def test_contract_binds_exact_reviewed_source_blobs():
    m = _load()
    manifest = m.collector_contract_manifest()
    assert manifest["activation_contract_git_blob"] == (
        "a3acb42280c334daa24a3b830105a04666fd603b"
    )
    assert manifest["activation_evidence_git_blob"] == (
        "aac7964d9e80633535003b9f27066cac1bb4bac2"
    )
    assert manifest["runtime_observers_git_blob"] == (
        "cc4774e6aa934764c189cebd4040cd8ea4870517"
    )


def test_activation_evidence_binding_remains_inactive():
    m = _load()
    assert m.activation_evidence.REVIEWED_COLLECTOR_BINDING_PRESENT is False
    out = m.validate_collector_contract()
    assert out["reviewed_collector_binding_present"] is False
    assert out["collector_binding_activation"] is False


def test_implementation_source_binding_is_required_but_absent():
    m = _load()
    manifest = m.collector_contract_manifest()
    assert (
        manifest[
            "collector_implementation_source_binding_required_before_activation"
        ]
        is True
    )
    assert manifest["collector_implementation_source_sha256"] is None
    out = m.validate_collector_contract()
    assert out["implementation_source_binding_required_before_activation"] is True
    assert out["implementation_source_sha256"] is None


def test_collector_authority_is_exact_read_only():
    m = _load()
    manifest = m.collector_contract_manifest()
    assert manifest["observation_mode"] == "read_only"
    assert manifest["automatic_host_backend_selection"] is False
    assert manifest["explicit_observation_authority_required"] is True
    for field in (
        "collector_may_mutate",
        "collector_may_start_runtime",
        "collector_may_execute_game",
        "collector_may_run_model_inference",
        "collector_may_train",
        "collector_may_update_weights",
        "collector_may_promote_policy",
        "collector_may_deploy",
        "collector_may_mutate_void_chain",
        "collector_may_move_funds",
    ):
        assert manifest[field] is False


def test_runtime_observer_contract_keeps_explicit_authority_gate():
    m = _load()
    observer = m.runtime_observers.runtime_observer_contract()
    assert observer["automatic_host_backend_selection"] is False
    assert observer["observation_requires_explicit_authority"] is True
    assert observer["observation_performed"] is False
    assert observer["runtime_execution_authorized"] is False


def test_snapshot_contract_set_is_exact_four_reviewed_snapshots():
    m = _load()
    rows = m.collector_contract_manifest()["snapshot_contracts"]
    assert set(rows) == {m.V14, m.V10, m.V2R13, m.V8}


def test_no_snapshot_claims_full_collector_implementation():
    m = _load()
    rows = m.collector_contract_manifest()["snapshot_contracts"]
    for row in rows.values():
        assert row["full_collector_implemented"] is False
    out = m.validate_collector_contract()
    assert out["full_collector_implemented"] is False


def test_v14_has_no_reviewed_partial_observer_primitive():
    m = _load()
    row = m.collector_contract_manifest()["snapshot_contracts"][m.V14]
    assert row["reviewed_partial_observer_primitives_present"] is False
    assert "read_only_loopback_endpoint_liveness" in row[
        "required_future_primitives"
    ]
    assert "read_only_active_model_identity" in row[
        "required_future_primitives"
    ]
    assert "read_only_runtime_unit_identity" in row[
        "required_future_primitives"
    ]


def test_v10_has_no_reviewed_partial_observer_primitive():
    m = _load()
    row = m.collector_contract_manifest()["snapshot_contracts"][m.V10]
    assert row["reviewed_partial_observer_primitives_present"] is False
    assert "read_only_loopback_endpoint_liveness" in row[
        "required_future_primitives"
    ]
    assert "read_only_active_model_identity" in row[
        "required_future_primitives"
    ]
    assert "read_only_runtime_unit_identity" in row[
        "required_future_primitives"
    ]


def test_v2r13_binds_only_reviewed_git_observer_primitive():
    m = _load()
    row = m.collector_contract_manifest()["snapshot_contracts"][m.V2R13]
    assert row["reviewed_partial_observer_primitives_present"] is True
    assert row["reviewed_partial_observer_primitives"] == [
        "observe_v2r13_git_identity"
    ]


def test_v8_binds_only_reviewed_asset_observer_primitives():
    m = _load()
    row = m.collector_contract_manifest()["snapshot_contracts"][m.V8]
    assert row["reviewed_partial_observer_primitives_present"] is True
    assert row["reviewed_partial_observer_primitives"] == [
        "observe_v8_assets",
        "observe_exact_regular_file",
    ]


def test_v2r13_collector_owned_fields_match_canonical_17_unresolved_leaves():
    m = _load()
    row = m.collector_contract_manifest()["snapshot_contracts"][m.V2R13]
    fields = row["collector_owned_evidence_fields"]
    assert len(fields) == 17
    assert len(fields) == len(set(fields))
    assert "collector_contract_sha256" in fields
    assert "endpoint_liveness" in fields
    assert "model_identity_verified" in fields
    assert "runtime_image_identity_verified" in fields
    assert "portable_binding_attested" in fields
    assert "frozen_source_worktree.exists" in fields
    assert "engine_worktree.is_symlink" in fields


def test_v8_with_environment_collector_owned_fields_match_9_unresolved_leaves():
    m = _load()
    row = m.collector_contract_manifest()["snapshot_contracts"][m.V8]
    fields = row["collector_owned_evidence_fields_with_supplied_environment"]
    assert len(fields) == 9
    assert len(fields) == len(set(fields))
    assert "collector_contract_sha256" in fields
    assert "offline_only_verified" in fields
    assert "load_call_performed" in fields
    assert "runtime_environment_verified" not in fields


def test_v8_without_environment_collector_owned_fields_match_10_unresolved_leaves():
    m = _load()
    row = m.collector_contract_manifest()["snapshot_contracts"][m.V8]
    fields = row["collector_owned_evidence_fields_without_supplied_environment"]
    assert len(fields) == 10
    assert len(fields) == len(set(fields))
    assert "runtime_environment_verified" in fields
    assert "offline_only_verified" in fields
    assert "load_call_performed" in fields


def test_common_operational_fields_are_collector_owned_for_v8_and_v2r13():
    m = _load()
    common = {
        "observation_mode",
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "game_execution_performed",
        "model_inference_performed",
    }
    rows = m.collector_contract_manifest()["snapshot_contracts"]
    assert common.issubset(
        set(rows[m.V2R13]["collector_owned_evidence_fields"])
    )
    assert common.issubset(
        set(rows[m.V8]["collector_owned_evidence_fields_with_supplied_environment"])
    )


def test_collector_contract_identity_never_claims_admission_or_readiness():
    m = _load()
    out = m.collector_contract_identity()
    assert out["collector_contract_sha256"] == EXPECTED_COLLECTOR_CONTRACT_SHA256
    assert out["implementation_source_binding_present"] is False
    assert out["collector_binding_activation"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_static_source_never_invokes_observer_or_host_backend():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    forbidden_calls = {
        "runtime_observers.observe_v8_assets",
        "runtime_observers.observe_exact_regular_file",
        "runtime_observers.observe_v2r13_git_identity",
        "runtime_observers.host_file_observation_backend",
        "runtime_observers.host_git_runner",
        "runtime_observers.host_path_resolver",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            assert _dotted(node.func) not in forbidden_calls


def test_collection_entrypoint_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeCollectorContractHold,
        "GENERATION2_REVIEWED_COLLECTOR_IMPLEMENTATION_NOT_PRESENT",
        lambda: m.collect_activation_evidence(),
    )


def test_validate_contract_never_claims_execution_or_readiness():
    m = _load()
    out = m.validate_collector_contract()
    assert out["live_observation_performed"] is False
    assert out["collector_executed"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False
