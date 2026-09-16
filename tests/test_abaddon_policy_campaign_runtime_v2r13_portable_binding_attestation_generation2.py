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
    "abaddon_policy_campaign_runtime_v2r13_portable_binding_attestation_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_portable_binding_attestation_generation2.py"
)
EXPECTED_SOURCE_SHA256 = (
    "c480af5b439b4c68b24f5bb68bdce1948f215eda3e847e8631a43e8eacbac818"
)


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_v2r13_portable_binding_attestation",
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


def _valid_receipt(m):
    body = {
        "schema": m.portable_checkout.BINDING_SCHEMA,
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


def test_contract_binds_exact_portable_source_and_contract():
    m = _load()
    out = m.v2r13_portable_binding_attestation_contract()
    assert out["portable_checkout_git_blob"] == (
        "077fbf5a2847d85113eb8fcba3904b02343ebfef"
    )
    assert out["portable_checkout_source_sha256"] == (
        "92e16e281d5a9036d78d900f35d854c6fb9783b2bf156c2acab69408d13a015d"
    )
    assert out["portable_binding_contract_sha256"] == (
        "677e503e8d4827a9d8950a177f308ad08982f612d70881f16de2c271e3b10e49"
    )


def test_contract_binds_exact_fully_bound_attestation_sha():
    m = _load()
    out = m.v2r13_portable_binding_attestation_contract()
    assert out["fully_bound_attestation_sha256"] == (
        "2235940543056b6c9154989c6d124362a524c3702de07b75f1654922525203f5"
    )


def test_contract_requires_full_base_binding_and_rejects_partial():
    m = _load()
    out = m.v2r13_portable_binding_attestation_contract()
    assert out["full_legacy_source_binding_required"] is True
    assert out["full_legacy_engine_binding_required"] is True
    assert out["full_base_binding_required"] is True
    assert out["pre_base_load_attestation_admitted"] is False


def test_contract_keeps_live_and_admission_surfaces_closed():
    m = _load()
    out = m.v2r13_portable_binding_attestation_contract()
    assert out["live_binding_install_implemented"] is False
    assert out["live_base_load_implemented"] is False
    assert out["validator_filesystem_observation_implemented"] is False
    assert out["validator_git_query_implemented"] is False
    assert out["validator_path_resolution_implemented"] is False
    assert out["validator_observer_invocation_implemented"] is False
    assert out["validator_host_backend_invocation_implemented"] is False
    assert out["canonical_provider_binding_present"] is False
    assert out["canonical_collection_enabled"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_valid_full_attestation_is_accepted():
    m = _load()
    receipt = _valid_receipt(m)
    out = m.validate_v2r13_portable_binding_attestation(receipt)
    assert out["supplied_attestation_valid"] is True
    assert out["portable_binding_fully_attested"] is True
    assert out["legacy_source_root_bound"] is True
    assert out["legacy_engine_root_bound"] is True
    assert out["base_loaded_and_bound"] is True


def test_valid_full_attestation_hash_is_exact():
    m = _load()
    receipt = _valid_receipt(m)
    assert receipt["attestation_sha256"] == m.FULLY_BOUND_ATTESTATION_SHA256
    out = m.validate_v2r13_portable_binding_attestation(receipt)
    assert out["supplied_attestation_sha256"] == (
        m.FULLY_BOUND_ATTESTATION_SHA256
    )


def test_validator_reports_no_actions_of_its_own():
    m = _load()
    out = m.validate_v2r13_portable_binding_attestation(_valid_receipt(m))
    assert out["validator_filesystem_observation_performed"] is False
    assert out["validator_external_worktree_git_query_performed"] is False
    assert out["validator_path_resolution_performed"] is False
    assert out["validator_binding_install_performed"] is False
    assert out["validator_base_load_performed"] is False
    assert out["validator_observer_invocation_performed"] is False
    assert out["validator_host_backend_invocation_performed"] is False


def test_validator_never_admits_provider_readiness_or_execution():
    m = _load()
    out = m.validate_v2r13_portable_binding_attestation(_valid_receipt(m))
    assert out["canonical_provider_binding_present"] is False
    assert out["canonical_collection_enabled"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_pre_base_load_attestation_is_rejected():
    m = _load()
    receipt = _valid_receipt(m)
    receipt["base_loaded_and_bound"] = False
    body = {
        key: receipt[key]
        for key in m.ATTESTATION_BODY_FIELDS
    }
    receipt["attestation_sha256"] = _stable_sha(body)
    _expect_hold(
        m.RuntimeV2R13PortableBindingAttestationHold,
        "portable binding base runner not loaded and bound",
        lambda: m.validate_v2r13_portable_binding_attestation(receipt),
    )


def test_legacy_source_unbound_is_rejected():
    m = _load()
    receipt = _valid_receipt(m)
    receipt["legacy_source_root_bound"] = False
    _expect_hold(
        m.RuntimeV2R13PortableBindingAttestationHold,
        "portable binding legacy source root not bound",
        lambda: m.validate_v2r13_portable_binding_attestation(receipt),
    )


def test_legacy_engine_unbound_is_rejected():
    m = _load()
    receipt = _valid_receipt(m)
    receipt["legacy_engine_root_bound"] = False
    _expect_hold(
        m.RuntimeV2R13PortableBindingAttestationHold,
        "portable binding legacy engine root not bound",
        lambda: m.validate_v2r13_portable_binding_attestation(receipt),
    )


def test_runtime_execution_claim_is_rejected():
    m = _load()
    receipt = _valid_receipt(m)
    receipt["runtime_execution_performed"] = True
    _expect_hold(
        m.RuntimeV2R13PortableBindingAttestationHold,
        "runtime_execution_performed",
        lambda: m.validate_v2r13_portable_binding_attestation(receipt),
    )


def test_model_execution_claim_is_rejected():
    m = _load()
    receipt = _valid_receipt(m)
    receipt["model_execution_performed"] = True
    _expect_hold(
        m.RuntimeV2R13PortableBindingAttestationHold,
        "model_execution_performed",
        lambda: m.validate_v2r13_portable_binding_attestation(receipt),
    )


def test_game_started_claim_is_rejected():
    m = _load()
    receipt = _valid_receipt(m)
    receipt["game_started"] = True
    _expect_hold(
        m.RuntimeV2R13PortableBindingAttestationHold,
        "game_started",
        lambda: m.validate_v2r13_portable_binding_attestation(receipt),
    )


def test_schema_drift_is_rejected():
    m = _load()
    receipt = _valid_receipt(m)
    receipt["schema"] = "wrong"
    _expect_hold(
        m.RuntimeV2R13PortableBindingAttestationHold,
        "portable binding attestation schema drift",
        lambda: m.validate_v2r13_portable_binding_attestation(receipt),
    )


def test_missing_field_is_rejected():
    m = _load()
    receipt = _valid_receipt(m)
    del receipt["game_started"]
    _expect_hold(
        m.RuntimeV2R13PortableBindingAttestationHold,
        "portable binding attestation field-set drift",
        lambda: m.validate_v2r13_portable_binding_attestation(receipt),
    )


def test_extra_field_is_rejected():
    m = _load()
    receipt = _valid_receipt(m)
    receipt["extra"] = False
    _expect_hold(
        m.RuntimeV2R13PortableBindingAttestationHold,
        "portable binding attestation field-set drift",
        lambda: m.validate_v2r13_portable_binding_attestation(receipt),
    )


def test_attestation_sha_mismatch_is_rejected():
    m = _load()
    receipt = _valid_receipt(m)
    receipt["attestation_sha256"] = "0" * 64
    _expect_hold(
        m.RuntimeV2R13PortableBindingAttestationHold,
        "portable binding attestation SHA mismatch",
        lambda: m.validate_v2r13_portable_binding_attestation(receipt),
    )


def test_validator_does_not_mutate_input_and_returns_copy():
    m = _load()
    receipt = _valid_receipt(m)
    before = copy.deepcopy(receipt)
    out = m.validate_v2r13_portable_binding_attestation(receipt)
    assert receipt == before
    out["validated_receipt"]["base_loaded_and_bound"] = False
    assert receipt["base_loaded_and_bound"] is True


def test_static_source_has_no_host_io_or_live_binding_calls():
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
        "portable_checkout.reviewed_path_binding",
        "portable_checkout.PortableRunnerBinding",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call):
            assert _dotted(node.func) not in forbidden_calls


def test_live_binding_validation_entrypoint_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13PortableBindingAttestationHold,
        "GENERATION2_V2R13_LIVE_PORTABLE_BINDING_VALIDATION_NOT_IMPLEMENTED",
        lambda: m.validate_live_binding_state(),
    )
