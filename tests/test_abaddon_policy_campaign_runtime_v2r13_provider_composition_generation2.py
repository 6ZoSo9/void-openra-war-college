from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_v2r13_provider_composition_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_provider_composition_generation2.py"
)
EXPECTED_SOURCE_SHA256 = (
    "3a3bde2ba3fa9d08b60a9864057968940a67125efc53c4ae7ba1a076db9b4b2a"
)

SOURCE_ROOT = "/frozen/source"
ENGINE_ROOT = "/engine/exact"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_v2r13_provider_composition",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _stable_sha(value):
    raw = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _worktree_receipt(m):
    observer = m.worktree_provider.worktree_observer
    ro = observer.runtime_observers
    return {
        "schema": observer.OBSERVATION_SCHEMA,
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


def _portable_receipt(m):
    binding = m.portable_binding_attestation.portable_checkout
    body = {
        "schema": binding.BINDING_SCHEMA,
        "legacy_source_root_bound": True,
        "legacy_engine_root_bound": True,
        "base_loaded_and_bound": True,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_started": False,
    }
    return {
        **body,
        "attestation_sha256": _stable_sha(body),
    }


def _compose(m, worktree=None, portable=None):
    return m.compose_v2r13_provider(
        worktree_receipt=worktree or _worktree_receipt(m),
        portable_binding_attestation_receipt=portable or _portable_receipt(m),
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


def test_contract_binds_exact_canonical_blobs():
    m = _load()
    out = m.v2r13_provider_composition_contract()
    assert out["source_only_provider_git_blob"] == (
        "f3b48e624172aeed81e28a6e24508533b7b13661"
    )
    assert out["worktree_provider_git_blob"] == (
        "7e6f628c64fe02db42bd6adee67d3965e6b1ae92"
    )
    assert out["portable_attestation_git_blob"] == (
        "afdc0421958565e713795dfd0d3c4c683041cc37"
    )


def test_contract_counts_are_exact():
    m = _load()
    out = m.v2r13_provider_composition_contract()
    assert out["source_only_primitive_count"] == 6
    assert out["worktree_primitive_count"] == 6
    assert out["portable_binding_primitive_count"] == 1
    assert out["combined_supported_primitive_count"] == 13
    assert out["remaining_unresolved_primitive_count"] == 3


def test_contract_remaining_unresolved_set_is_exact():
    m = _load()
    out = m.v2r13_provider_composition_contract()
    assert out["remaining_unresolved_primitive_names"] == (
        "endpoint_liveness",
        "model_identity_verified",
        "runtime_image_identity_verified",
    )


def test_contract_integrates_portable_primitive_only():
    m = _load()
    out = m.v2r13_provider_composition_contract()
    assert out["portable_binding_provider_primitive_implemented"] is True
    assert out["live_endpoint_liveness_provider_implemented"] is False
    assert out["live_model_identity_provider_implemented"] is False
    assert out["live_runtime_image_provider_implemented"] is False


def test_contract_keeps_live_and_admission_surfaces_closed():
    m = _load()
    out = m.v2r13_provider_composition_contract()
    for field in (
        "composition_filesystem_observation_implemented",
        "composition_git_query_implemented",
        "composition_path_resolution_implemented",
        "composition_binding_install_implemented",
        "composition_base_load_implemented",
        "composition_observer_invocation_implemented",
        "composition_host_backend_invocation_implemented",
        "canonical_provider_binding_present",
        "canonical_collection_enabled",
        "runtime_readiness_admitted",
        "runtime_execution_authorized",
    ):
        assert out[field] is False


def test_happy_path_supports_exactly_13_primitives():
    m = _load()
    out = _compose(m)
    assert out["supported_primitive_count"] == 13
    assert len(out["supported_primitive_names"]) == 13
    assert len(set(out["supported_primitive_names"])) == 13


def test_happy_path_adds_portable_binding_as_13th_primitive():
    m = _load()
    out = _compose(m)
    assert out["supported_primitive_names"][-1] == "portable_binding_attested"
    assert out["primitive_values"]["portable_binding_attested"] is True


def test_happy_path_has_exact_three_remaining_unresolved():
    m = _load()
    out = _compose(m)
    assert out["remaining_unresolved_primitive_names"] == (
        "endpoint_liveness",
        "model_identity_verified",
        "runtime_image_identity_verified",
    )
    assert out["remaining_unresolved_primitive_count"] == 3


def test_happy_path_preserves_source_only_self_audits():
    m = _load()
    out = _compose(m)
    assert out["primitive_values"]["observation_mode"] == "read_only"
    assert out["primitive_values"]["mutation_performed"] is False
    assert out["primitive_values"]["service_action_performed"] is False
    assert out["primitive_values"]["runtime_start_performed"] is False
    assert out["primitive_values"]["game_execution_performed"] is False
    assert out["primitive_values"]["model_inference_performed"] is False


def test_happy_path_preserves_six_worktree_primitives():
    m = _load()
    out = _compose(m)
    assert out["primitive_values"]["frozen_source_worktree.exists"] is True
    assert out["primitive_values"]["frozen_source_worktree.is_directory"] is True
    assert out["primitive_values"]["frozen_source_worktree.is_symlink"] is False
    assert out["primitive_values"]["engine_worktree.exists"] is True
    assert out["primitive_values"]["engine_worktree.is_directory"] is True
    assert out["primitive_values"]["engine_worktree.is_symlink"] is False


def test_happy_path_preserves_worktree_observation_provenance():
    m = _load()
    out = _compose(m)
    assert out["worktree_receipt_reports_filesystem_observation"] is True
    assert out["worktree_receipt_reports_git_query"] is True
    assert out["composition_filesystem_observation_performed"] is False
    assert out["composition_external_worktree_git_query_performed"] is False


def test_happy_path_preserves_portable_attestation_identity():
    m = _load()
    out = _compose(m)
    assert out["portable_attestation_sha256"] == (
        "2235940543056b6c9154989c6d124362a524c3702de07b75f1654922525203f5"
    )
    assert out["supplied_portable_attestation_validated"] is True


def test_happy_path_never_claims_provider_complete_or_readiness():
    m = _load()
    out = _compose(m)
    assert out["provider_complete"] is False
    assert out["canonical_provider_binding_present"] is False
    assert out["canonical_collection_enabled"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_composition_does_not_mutate_supplied_inputs():
    m = _load()
    worktree = _worktree_receipt(m)
    portable = _portable_receipt(m)
    worktree_before = copy.deepcopy(worktree)
    portable_before = copy.deepcopy(portable)
    _compose(m, worktree=worktree, portable=portable)
    assert worktree == worktree_before
    assert portable == portable_before


def test_returned_nested_results_are_copy_isolated():
    m = _load()
    worktree = _worktree_receipt(m)
    portable = _portable_receipt(m)
    first = _compose(m, worktree=worktree, portable=portable)
    first["worktree_adapter_result"]["primitive_values"][
        "engine_worktree.exists"
    ] = False
    first["portable_attestation_validation"]["base_loaded_and_bound"] = False
    second = _compose(m, worktree=worktree, portable=portable)
    assert second["worktree_adapter_result"]["primitive_values"][
        "engine_worktree.exists"
    ] is True
    assert second["portable_attestation_validation"]["base_loaded_and_bound"] is True


def test_bad_worktree_receipt_is_rejected():
    m = _load()
    receipt = _worktree_receipt(m)
    receipt["engine_worktree"]["clean"] = False
    _expect_hold(
        m.worktree_provider.worktree_observer.RuntimeV2R13WorktreeObserverHold,
        "V2R13 engine lacks clean",
        lambda: _compose(m, worktree=receipt),
    )


def test_worktree_runtime_execution_claim_is_rejected():
    m = _load()
    receipt = _worktree_receipt(m)
    receipt["runtime_execution_performed"] = True
    _expect_hold(
        m.worktree_provider.worktree_observer.RuntimeV2R13WorktreeObserverHold,
        "runtime_execution_performed",
        lambda: _compose(m, worktree=receipt),
    )


def test_pre_base_load_portable_attestation_is_rejected():
    m = _load()
    receipt = _portable_receipt(m)
    receipt["base_loaded_and_bound"] = False
    body = {
        key: receipt[key]
        for key in m.portable_binding_attestation.ATTESTATION_BODY_FIELDS
    }
    receipt["attestation_sha256"] = _stable_sha(body)
    _expect_hold(
        m.portable_binding_attestation.RuntimeV2R13PortableBindingAttestationHold,
        "base runner not loaded and bound",
        lambda: _compose(m, portable=receipt),
    )


def test_bad_portable_attestation_sha_is_rejected():
    m = _load()
    receipt = _portable_receipt(m)
    receipt["attestation_sha256"] = "0" * 64
    _expect_hold(
        m.portable_binding_attestation.RuntimeV2R13PortableBindingAttestationHold,
        "attestation SHA mismatch",
        lambda: _compose(m, portable=receipt),
    )


def test_portable_runtime_execution_claim_is_rejected():
    m = _load()
    receipt = _portable_receipt(m)
    receipt["runtime_execution_performed"] = True
    _expect_hold(
        m.portable_binding_attestation.RuntimeV2R13PortableBindingAttestationHold,
        "runtime_execution_performed",
        lambda: _compose(m, portable=receipt),
    )


def test_static_source_has_no_host_io_or_live_provider_calls():
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
        "worktree_provider.adapt_live_worktree_state",
        "portable_binding_attestation.validate_live_binding_state",
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


def test_live_composition_entrypoint_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13ProviderCompositionHold,
        "GENERATION2_V2R13_LIVE_PROVIDER_COMPOSITION_NOT_IMPLEMENTED",
        lambda: m.compose_live_v2r13_provider(),
    )
