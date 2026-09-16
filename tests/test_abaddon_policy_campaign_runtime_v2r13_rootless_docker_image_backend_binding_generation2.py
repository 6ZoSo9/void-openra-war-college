from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_v2r13_rootless_docker_image_backend_binding_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_rootless_docker_image_backend_binding_generation2.py"
)

EXPECTED_SOURCE_SHA256 = "74acc7248ee19d2d141aa4ec36fc3ce1c6068c56ca1801719c3287cd2c774f52"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_v2r13_rootless_docker_image_backend_binding",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _receipt(m):
    return {
        "schema": m.runtime_image_interface.BACKEND_RECEIPT_SCHEMA,
        "snapshot_id": m.activation_contract.V2R13,
        "primitive_name": "runtime_image_identity_verified",
        "source_sha256": m.ROOTLESS_DOCKER_BACKEND_SOURCE_SHA256,
        "backend_kind": m.ROOTLESS_DOCKER_BACKEND_KIND,
        "observation_mode": "read_only",
        "runtime_image_id": m.activation_contract.V2R13_RUNTIME_IMAGE_ID,
        "runtime_image_identity_observation_performed": True,
        "mutation_performed": False,
        "service_action_performed": False,
        "runtime_start_performed": False,
        "runtime_stop_performed": False,
        "runtime_reload_performed": False,
        "model_load_performed": False,
        "model_inference_performed": False,
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


def test_contract_pins_exact_backend_source_identities():
    m = _load()
    out = m.v2r13_rootless_docker_image_backend_binding_contract()
    assert out["rootless_docker_backend_git_blob"] == (
        "488497f723ad5bc5ca63b3b2d69cece26bddaaa5"
    )
    assert out["rootless_docker_backend_source_sha256"] == (
        "25e8f41dcea700860ec1b97726b321a99c2622e00ddba12433246c7b121b11f6"
    )
    assert out["backend_source_identity_pinned_by_git_blob"] is True
    assert out["backend_source_identity_pinned_by_sha256"] is True


def test_contract_pins_exact_dependency_blobs():
    m = _load()
    out = m.v2r13_rootless_docker_image_backend_binding_contract()
    assert out["activation_contract_git_blob"] == (
        "a3acb42280c334daa24a3b830105a04666fd603b"
    )
    assert out["provider_composition_git_blob"] == (
        "4efdf74ac7b140af5f29d5539eccde98694f4a3b"
    )
    assert out["runtime_image_interface_git_blob"] == (
        "8bc118684fb085361fa98dd80b6a1ee37edeb523"
    )


def test_contract_is_separate_non_self_binding_instrument():
    m = _load()
    out = m.v2r13_rootless_docker_image_backend_binding_contract()
    assert out["separate_binding_instrument"] is True
    assert out["backend_source_is_not_self_bound"] is True
    assert out["canonical_backend_source_binding_present"] is True


def test_contract_implements_only_runtime_image_provider_primitive():
    m = _load()
    out = m.v2r13_rootless_docker_image_backend_binding_contract()
    assert out["runtime_image_identity_provider_primitive_implemented"] is True
    assert out["runtime_image_identity_can_verify_from_bound_receipt"] is True
    assert out["endpoint_liveness_provider_implemented"] is False
    assert out["model_identity_provider_implemented"] is False


def test_contract_advances_exact_13_3_to_14_2_frontier():
    m = _load()
    out = m.v2r13_rootless_docker_image_backend_binding_contract()
    assert out["baseline_supported_primitive_count"] == 13
    assert out["supported_primitive_count_after_binding"] == 14
    assert out["remaining_unresolved_primitive_count"] == 2
    assert out["remaining_unresolved_primitive_names"] == (
        "endpoint_liveness",
        "model_identity_verified",
    )


def test_contract_keeps_full_collector_provider_readiness_execution_closed():
    m = _load()
    out = m.v2r13_rootless_docker_image_backend_binding_contract()
    assert out["full_collector_identity_admitted"] is False
    assert out["canonical_provider_binding_present"] is False
    assert out["canonical_collection_enabled"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_contract_has_no_live_observation_surface():
    m = _load()
    out = m.v2r13_rootless_docker_image_backend_binding_contract()
    for field in (
        "binding_live_observation_implemented",
        "binding_filesystem_observation_implemented",
        "binding_git_query_implemented",
        "binding_subprocess_execution_implemented",
        "binding_host_backend_invocation_implemented",
        "binding_network_probe_implemented",
        "binding_ollama_http_request_implemented",
        "binding_model_inference_implemented",
        "binding_game_execution_implemented",
    ):
        assert out[field] is False
    assert out["automatic_host_backend_selection"] is False


def test_live_collection_entrypoint_hard_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendBindingHold,
        "BOUND_RUNTIME_IMAGE_LIVE_COLLECTION_NOT_IMPLEMENTED",
        lambda: m.collect_bound_runtime_image_identity(),
    )


def test_valid_bound_receipt_verifies_runtime_image():
    m = _load()
    out = m.validate_bound_runtime_image_receipt(_receipt(m))
    assert out["canonical_backend_source_binding_present"] is True
    assert out["runtime_image_identity_observed"] is True
    assert out["runtime_image_identity_matches_expected"] is True
    assert out["runtime_image_identity_verified"] is True
    assert out["runtime_image_id"] == m.activation_contract.V2R13_RUNTIME_IMAGE_ID


def test_valid_bound_receipt_pins_backend_identity():
    m = _load()
    out = m.validate_bound_runtime_image_receipt(_receipt(m))
    assert out["backend_kind"] == "rootless_docker_local_image_store_v1"
    assert out["reviewed_backend_source_sha256"] == (
        "25e8f41dcea700860ec1b97726b321a99c2622e00ddba12433246c7b121b11f6"
    )
    assert out["reviewed_backend_git_blob"] == (
        "488497f723ad5bc5ca63b3b2d69cece26bddaaa5"
    )


def test_valid_bound_receipt_lifts_only_after_unbound_interface_validation():
    m = _load()
    out = m.validate_bound_runtime_image_receipt(_receipt(m))
    assert out["interface_validation"]["backend_receipt_valid"] is True
    assert out["interface_validation"]["runtime_image_identity_matches_expected"] is True
    assert out["interface_validation"]["runtime_image_identity_verified"] is False
    assert out["runtime_image_identity_verified"] is True


def test_valid_bound_receipt_has_exact_primitive_value():
    m = _load()
    out = m.validate_bound_runtime_image_receipt(_receipt(m))
    assert out["primitive_values"] == {"runtime_image_identity_verified": True}
    assert out["supported_primitive_count_after_binding"] == 14
    assert out["remaining_unresolved_primitive_count"] == 2


def test_valid_bound_receipt_does_not_admit_other_identity_or_readiness():
    m = _load()
    out = m.validate_bound_runtime_image_receipt(_receipt(m))
    assert out["endpoint_liveness_verified"] is False
    assert out["model_identity_verified"] is False
    assert out["full_collector_identity_admitted"] is False
    assert out["canonical_provider_binding_present"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_valid_bound_receipt_reports_zero_binding_io():
    m = _load()
    out = m.validate_bound_runtime_image_receipt(_receipt(m))
    for field in (
        "binding_filesystem_observation_performed",
        "binding_git_query_performed",
        "binding_subprocess_execution_performed",
        "binding_host_backend_invocation_performed",
        "binding_network_probe_performed",
        "binding_ollama_http_request_performed",
        "binding_model_inference_performed",
        "binding_game_execution_performed",
    ):
        assert out[field] is False


def test_inputs_are_not_mutated_and_output_is_copy_isolated():
    m = _load()
    receipt = _receipt(m)
    before = copy.deepcopy(receipt)
    out = m.validate_bound_runtime_image_receipt(receipt)
    assert receipt == before
    out["interface_validation"]["validated_receipt"]["runtime_image_id"] = "changed"
    assert receipt["runtime_image_id"] == m.activation_contract.V2R13_RUNTIME_IMAGE_ID


def test_extra_receipt_field_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["extra"] = True
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendBindingHold,
        "field-set drift",
        lambda: m.validate_bound_runtime_image_receipt(receipt),
    )


def test_missing_receipt_field_rejected():
    m = _load()
    receipt = _receipt(m)
    del receipt["runtime_reload_performed"]
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendBindingHold,
        "field-set drift",
        lambda: m.validate_bound_runtime_image_receipt(receipt),
    )


def test_backend_kind_drift_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["backend_kind"] = "other"
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendBindingHold,
        "backend kind mismatch",
        lambda: m.validate_bound_runtime_image_receipt(receipt),
    )


def test_backend_source_sha_drift_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["source_sha256"] = "0" * 64
    _expect_hold(
        m.RuntimeV2R13RootlessDockerImageBackendBindingHold,
        "backend source SHA mismatch",
        lambda: m.validate_bound_runtime_image_receipt(receipt),
    )


def test_receipt_schema_drift_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["schema"] = "wrong"
    _expect_hold(
        m.runtime_image_interface.RuntimeV2R13RuntimeImageObserverHold,
        "schema drift",
        lambda: m.validate_bound_runtime_image_receipt(receipt),
    )


def test_snapshot_drift_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["snapshot_id"] = "wrong"
    _expect_hold(
        m.runtime_image_interface.RuntimeV2R13RuntimeImageObserverHold,
        "snapshot drift",
        lambda: m.validate_bound_runtime_image_receipt(receipt),
    )


def test_primitive_name_drift_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["primitive_name"] = "model_identity_verified"
    _expect_hold(
        m.runtime_image_interface.RuntimeV2R13RuntimeImageObserverHold,
        "primitive-name drift",
        lambda: m.validate_bound_runtime_image_receipt(receipt),
    )


def test_observation_mode_drift_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["observation_mode"] = "read_write"
    _expect_hold(
        m.runtime_image_interface.RuntimeV2R13RuntimeImageObserverHold,
        "observation mode must be read_only",
        lambda: m.validate_bound_runtime_image_receipt(receipt),
    )


def test_runtime_image_id_drift_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["runtime_image_id"] = "sha256:" + "0" * 64
    _expect_hold(
        m.runtime_image_interface.RuntimeV2R13RuntimeImageObserverHold,
        "runtime-image identity drift",
        lambda: m.validate_bound_runtime_image_receipt(receipt),
    )


def test_observation_false_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["runtime_image_identity_observation_performed"] = False
    _expect_hold(
        m.runtime_image_interface.RuntimeV2R13RuntimeImageObserverHold,
        "observation not performed",
        lambda: m.validate_bound_runtime_image_receipt(receipt),
    )


def test_mutation_claim_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["mutation_performed"] = True
    _expect_hold(
        m.runtime_image_interface.RuntimeV2R13RuntimeImageObserverHold,
        "mutation_performed",
        lambda: m.validate_bound_runtime_image_receipt(receipt),
    )


def test_service_action_claim_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["service_action_performed"] = True
    _expect_hold(
        m.runtime_image_interface.RuntimeV2R13RuntimeImageObserverHold,
        "service_action_performed",
        lambda: m.validate_bound_runtime_image_receipt(receipt),
    )


def test_runtime_start_claim_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["runtime_start_performed"] = True
    _expect_hold(
        m.runtime_image_interface.RuntimeV2R13RuntimeImageObserverHold,
        "runtime_start_performed",
        lambda: m.validate_bound_runtime_image_receipt(receipt),
    )


def test_model_inference_claim_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["model_inference_performed"] = True
    _expect_hold(
        m.runtime_image_interface.RuntimeV2R13RuntimeImageObserverHold,
        "model_inference_performed",
        lambda: m.validate_bound_runtime_image_receipt(receipt),
    )


def test_game_execution_claim_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["game_execution_performed"] = True
    _expect_hold(
        m.runtime_image_interface.RuntimeV2R13RuntimeImageObserverHold,
        "game_execution_performed",
        lambda: m.validate_bound_runtime_image_receipt(receipt),
    )


def test_backend_dependency_drift_fails_closed():
    m = _load()
    original = m.docker_backend.v2r13_rootless_docker_image_backend_contract
    baseline = original()

    def drifted():
        value = copy.deepcopy(baseline)
        value["backend_kind"] = "wrong"
        return value

    m.docker_backend.v2r13_rootless_docker_image_backend_contract = drifted
    try:
        _expect_hold(
            m.RuntimeV2R13RootlessDockerImageBackendBindingHold,
            "backend kind drift",
            lambda: m.v2r13_rootless_docker_image_backend_binding_contract(),
        )
    finally:
        m.docker_backend.v2r13_rootless_docker_image_backend_contract = original


def test_provider_baseline_drift_fails_closed():
    m = _load()
    original = m.provider_composition.v2r13_provider_composition_contract
    baseline = original()

    def drifted():
        value = copy.deepcopy(baseline)
        value["combined_supported_primitive_count"] = 14
        return value

    m.provider_composition.v2r13_provider_composition_contract = drifted
    try:
        _expect_hold(
            m.RuntimeV2R13RootlessDockerImageBackendBindingHold,
            "baseline supported count drift",
            lambda: m.v2r13_rootless_docker_image_backend_binding_contract(),
        )
    finally:
        m.provider_composition.v2r13_provider_composition_contract = original


def test_interface_dependency_drift_fails_closed():
    m = _load()
    original = m.runtime_image_interface.v2r13_runtime_image_readonly_observer_contract
    baseline = original()

    def drifted():
        value = copy.deepcopy(baseline)
        value["supplied_backend_receipt_validator_implemented"] = False
        return value

    m.runtime_image_interface.v2r13_runtime_image_readonly_observer_contract = drifted
    try:
        _expect_hold(
            m.RuntimeV2R13RootlessDockerImageBackendBindingHold,
            "receipt validator missing",
            lambda: m.v2r13_rootless_docker_image_backend_binding_contract(),
        )
    finally:
        m.runtime_image_interface.v2r13_runtime_image_readonly_observer_contract = original


def test_static_binding_source_has_no_host_io_imports_or_calls():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    forbidden_roots = {
        "os",
        "subprocess",
        "pathlib",
        "socket",
        "urllib",
        "http",
        "requests",
        "httpx",
        "docker",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_roots

    calls = [
        _dotted(node.func)
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
    ]
    forbidden_call_prefixes = (
        "os.",
        "subprocess.",
        "pathlib.",
        "socket.",
        "urllib.",
        "http.",
        "requests.",
        "httpx.",
        "docker.",
    )
    assert not any(
        call.startswith(prefix)
        for call in calls
        for prefix in forbidden_call_prefixes
    )
