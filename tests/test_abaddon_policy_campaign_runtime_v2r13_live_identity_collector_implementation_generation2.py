from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_v2r13_live_identity_collector_implementation_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_live_identity_collector_implementation_generation2.py"
)

EXPECTED_SOURCE_SHA256 = "8c415a0f3690a96a95c051a365691d3dad501e5656b438b0bf57a502311db9c8"
SEMANTIC_SHA = "0bda63a4d82be7f38e604c15fe63f659051cc42527bc9281317df167f6145219"
ENDPOINT_SOURCE_SHA = "e" * 64


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_v2r13_live_identity_collector_implementation",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _endpoint_receipt(m):
    return {
        "schema": m.ENDPOINT_RECEIPT_SCHEMA,
        "snapshot_id": m.activation_contract.V2R13,
        "primitive_name": "endpoint_liveness",
        "source_sha256": ENDPOINT_SOURCE_SHA,
        "observation_mode": "read_only",
        "endpoint_url": m.activation_contract.LOOPBACK_11434,
        "endpoint_loopback": True,
        "endpoint_liveness": True,
        "mutation_performed": False,
        "service_action_performed": False,
        "runtime_start_performed": False,
        "runtime_stop_performed": False,
        "runtime_reload_performed": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
    }


def _identity_receipt(m):
    v = m.identity_receipt_validator
    return {
        "schema": v.RECEIPT_SCHEMA,
        "snapshot_id": m.activation_contract.V2R13,
        "observation_mode": "read_only",
        "collector_contract_sha256": SEMANTIC_SHA,
        "active_model_alias": m.activation_contract.V2R13_MODEL_ALIAS,
        "active_model_digest": m.activation_contract.V2R13_MODEL_DIGEST,
        "runtime_image_id": m.activation_contract.V2R13_RUNTIME_IMAGE_ID,
        "model_identity_observation_performed": True,
        "runtime_image_identity_observation_performed": True,
        "mutation_performed": False,
        "service_action_performed": False,
        "runtime_start_performed": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "deployment_performed": False,
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


def test_contract_binds_exact_canonical_blobs():
    m = _load()
    out = m.v2r13_live_identity_collector_implementation_contract()
    assert out["live_identity_collector_contract_git_blob"] == (
        "db9fbb58f3d5870c77a796641afb1014acc19ee4"
    )
    assert out["identity_receipt_validator_git_blob"] == (
        "d1586ba032d78296e200d5016560682b82ee599d"
    )
    assert out["activation_contract_git_blob"] == (
        "a3acb42280c334daa24a3b830105a04666fd603b"
    )


def test_contract_binds_exact_semantic_sha():
    m = _load()
    out = m.v2r13_live_identity_collector_implementation_contract()
    assert out["live_identity_collector_semantic_sha256"] == SEMANTIC_SHA
    assert out["semantic_contract_valid"] is True


def test_contract_implements_only_supplied_receipt_composition():
    m = _load()
    out = m.v2r13_live_identity_collector_implementation_contract()
    assert out["supplied_endpoint_receipt_validator_implemented"] is True
    assert out["supplied_identity_receipt_validator_reused"] is True
    assert out["supplied_receipt_composition_implemented"] is True
    assert out["endpoint_receipt_source_binding_enforced"] is True
    assert out["identity_receipt_semantic_contract_binding_enforced"] is True


def test_contract_keeps_all_live_backends_absent():
    m = _load()
    out = m.v2r13_live_identity_collector_implementation_contract()
    for field in (
        "automatic_host_backend_selection",
        "host_backend_implementation_present",
        "live_collection_implemented",
        "canonical_implementation_source_binding_present",
        "canonical_collection_enabled",
        "collector_identity_admission_implemented",
        "filesystem_observation_implemented",
        "external_git_query_implemented",
        "path_resolution_implemented",
        "subprocess_execution_implemented",
        "http_request_implemented",
        "endpoint_probe_implemented",
        "systemd_query_implemented",
        "service_action_implemented",
        "runtime_start_stop_reload_implemented",
        "model_load_implemented",
        "model_inference_implemented",
        "canonical_provider_binding_present",
        "runtime_readiness_admitted",
        "runtime_execution_authorized",
    ):
        assert out[field] is False


def test_contract_preserves_exact_13_3_frontier():
    m = _load()
    out = m.v2r13_live_identity_collector_implementation_contract()
    assert out["supported_primitive_count_remains"] == 13
    assert out["remaining_unresolved_primitive_count_remains"] == 3
    assert out["remaining_unresolved_primitive_names"] == (
        "endpoint_liveness",
        "model_identity_verified",
        "runtime_image_identity_verified",
    )
    assert out["endpoint_liveness_provider_primitive_implemented"] is False
    assert out["model_identity_provider_primitive_implemented"] is False
    assert out["runtime_image_provider_primitive_implemented"] is False


def test_valid_endpoint_receipt_observed_but_not_verified():
    m = _load()
    out = m.validate_endpoint_liveness_receipt(
        _endpoint_receipt(m),
        expected_source_sha256=ENDPOINT_SOURCE_SHA,
    )
    assert out["endpoint_receipt_valid"] is True
    assert out["supplied_endpoint_liveness_observed"] is True
    assert out["collector_identity_admitted"] is False
    assert out["endpoint_liveness_verified"] is False


def test_endpoint_source_binding_mismatch_is_rejected():
    m = _load()
    receipt = _endpoint_receipt(m)
    _expect_hold(
        m.RuntimeV2R13LiveIdentityCollectorImplementationHold,
        "source binding mismatch",
        lambda: m.validate_endpoint_liveness_receipt(
            receipt,
            expected_source_sha256="f" * 64,
        ),
    )


def test_endpoint_bad_url_is_rejected():
    m = _load()
    receipt = _endpoint_receipt(m)
    receipt["endpoint_url"] = "http://127.0.0.1:9999/nope"
    _expect_hold(
        m.RuntimeV2R13LiveIdentityCollectorImplementationHold,
        "URL drift",
        lambda: m.validate_endpoint_liveness_receipt(
            receipt,
            expected_source_sha256=ENDPOINT_SOURCE_SHA,
        ),
    )


def test_endpoint_nonloopback_claim_is_rejected():
    m = _load()
    receipt = _endpoint_receipt(m)
    receipt["endpoint_loopback"] = False
    _expect_hold(
        m.RuntimeV2R13LiveIdentityCollectorImplementationHold,
        "not loopback",
        lambda: m.validate_endpoint_liveness_receipt(
            receipt,
            expected_source_sha256=ENDPOINT_SOURCE_SHA,
        ),
    )


def test_endpoint_false_liveness_is_rejected():
    m = _load()
    receipt = _endpoint_receipt(m)
    receipt["endpoint_liveness"] = False
    _expect_hold(
        m.RuntimeV2R13LiveIdentityCollectorImplementationHold,
        "liveness=true",
        lambda: m.validate_endpoint_liveness_receipt(
            receipt,
            expected_source_sha256=ENDPOINT_SOURCE_SHA,
        ),
    )


def test_endpoint_model_inference_claim_is_rejected():
    m = _load()
    receipt = _endpoint_receipt(m)
    receipt["model_inference_performed"] = True
    _expect_hold(
        m.RuntimeV2R13LiveIdentityCollectorImplementationHold,
        "model_inference_performed",
        lambda: m.validate_endpoint_liveness_receipt(
            receipt,
            expected_source_sha256=ENDPOINT_SOURCE_SHA,
        ),
    )


def test_endpoint_service_action_claim_is_rejected():
    m = _load()
    receipt = _endpoint_receipt(m)
    receipt["service_action_performed"] = True
    _expect_hold(
        m.RuntimeV2R13LiveIdentityCollectorImplementationHold,
        "service_action_performed",
        lambda: m.validate_endpoint_liveness_receipt(
            receipt,
            expected_source_sha256=ENDPOINT_SOURCE_SHA,
        ),
    )


def test_endpoint_missing_field_is_rejected():
    m = _load()
    receipt = _endpoint_receipt(m)
    del receipt["runtime_reload_performed"]
    _expect_hold(
        m.RuntimeV2R13LiveIdentityCollectorImplementationHold,
        "field-set drift",
        lambda: m.validate_endpoint_liveness_receipt(
            receipt,
            expected_source_sha256=ENDPOINT_SOURCE_SHA,
        ),
    )


def test_valid_bundle_matches_supplied_facts_but_admits_nothing():
    m = _load()
    out = m.assemble_candidate_from_supplied_receipts(
        endpoint_receipt=_endpoint_receipt(m),
        endpoint_source_sha256=ENDPOINT_SOURCE_SHA,
        identity_receipt=_identity_receipt(m),
    )
    assert out["semantic_contract_valid"] is True
    assert out["supplied_endpoint_liveness_observed"] is True
    assert out["supplied_identity_values_match"] is True
    assert out["collector_implementation_source_binding_admitted"] is False
    assert out["collector_identity_admitted"] is False
    assert out["endpoint_liveness_verified"] is False
    assert out["model_identity_verified"] is False
    assert out["runtime_image_identity_verified"] is False


def test_valid_bundle_preserves_exact_expected_identity():
    m = _load()
    out = m.assemble_candidate_from_supplied_receipts(
        endpoint_receipt=_endpoint_receipt(m),
        endpoint_source_sha256=ENDPOINT_SOURCE_SHA,
        identity_receipt=_identity_receipt(m),
    )
    assert out["collector_contract_sha256"] == SEMANTIC_SHA
    assert out["identity_receipt_collector_contract_sha256"] == SEMANTIC_SHA
    assert out["expected_model_alias"] == m.activation_contract.V2R13_MODEL_ALIAS
    assert out["expected_model_digest"] == m.activation_contract.V2R13_MODEL_DIGEST
    assert out["expected_runtime_image_id"] == m.activation_contract.V2R13_RUNTIME_IMAGE_ID


def test_valid_bundle_preserves_13_3_frontier():
    m = _load()
    out = m.assemble_candidate_from_supplied_receipts(
        endpoint_receipt=_endpoint_receipt(m),
        endpoint_source_sha256=ENDPOINT_SOURCE_SHA,
        identity_receipt=_identity_receipt(m),
    )
    assert out["supported_primitive_count_remains"] == 13
    assert out["remaining_unresolved_primitive_count_remains"] == 3
    assert out["remaining_unresolved_primitive_names"] == (
        "endpoint_liveness",
        "model_identity_verified",
        "runtime_image_identity_verified",
    )
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_identity_semantic_contract_binding_mismatch_is_rejected():
    m = _load()
    receipt = _identity_receipt(m)
    receipt["collector_contract_sha256"] = "a" * 64
    _expect_hold(
        m.RuntimeV2R13LiveIdentityCollectorImplementationHold,
        "semantic collector-contract binding mismatch",
        lambda: m.assemble_candidate_from_supplied_receipts(
            endpoint_receipt=_endpoint_receipt(m),
            endpoint_source_sha256=ENDPOINT_SOURCE_SHA,
            identity_receipt=receipt,
        ),
    )


def test_identity_digest_drift_is_rejected_by_canonical_validator():
    m = _load()
    receipt = _identity_receipt(m)
    receipt["active_model_digest"] = "0" * 64
    _expect_hold(
        m.identity_receipt_validator.RuntimeV2R13IdentityReceiptValidatorHold,
        "active model digest drift",
        lambda: m.assemble_candidate_from_supplied_receipts(
            endpoint_receipt=_endpoint_receipt(m),
            endpoint_source_sha256=ENDPOINT_SOURCE_SHA,
            identity_receipt=receipt,
        ),
    )


def test_identity_runtime_image_drift_is_rejected_by_canonical_validator():
    m = _load()
    receipt = _identity_receipt(m)
    receipt["runtime_image_id"] = "sha256:" + "0" * 64
    _expect_hold(
        m.identity_receipt_validator.RuntimeV2R13IdentityReceiptValidatorHold,
        "runtime image identity drift",
        lambda: m.assemble_candidate_from_supplied_receipts(
            endpoint_receipt=_endpoint_receipt(m),
            endpoint_source_sha256=ENDPOINT_SOURCE_SHA,
            identity_receipt=receipt,
        ),
    )


def test_identity_inference_claim_is_rejected_by_canonical_validator():
    m = _load()
    receipt = _identity_receipt(m)
    receipt["model_inference_performed"] = True
    _expect_hold(
        m.identity_receipt_validator.RuntimeV2R13IdentityReceiptValidatorHold,
        "model_inference_performed",
        lambda: m.assemble_candidate_from_supplied_receipts(
            endpoint_receipt=_endpoint_receipt(m),
            endpoint_source_sha256=ENDPOINT_SOURCE_SHA,
            identity_receipt=receipt,
        ),
    )


def test_inputs_are_not_mutated_and_nested_outputs_are_copy_isolated():
    m = _load()
    endpoint = _endpoint_receipt(m)
    identity = _identity_receipt(m)
    endpoint_before = copy.deepcopy(endpoint)
    identity_before = copy.deepcopy(identity)
    out = m.assemble_candidate_from_supplied_receipts(
        endpoint_receipt=endpoint,
        endpoint_source_sha256=ENDPOINT_SOURCE_SHA,
        identity_receipt=identity,
    )
    assert endpoint == endpoint_before
    assert identity == identity_before
    out["endpoint_receipt_validation"]["validated_receipt"]["endpoint_liveness"] = False
    out["identity_receipt_validation"]["validated_receipt"]["active_model_digest"] = "0" * 64
    assert endpoint["endpoint_liveness"] is True
    assert identity["active_model_digest"] == m.activation_contract.V2R13_MODEL_DIGEST


def test_candidate_reports_no_live_actions():
    m = _load()
    out = m.assemble_candidate_from_supplied_receipts(
        endpoint_receipt=_endpoint_receipt(m),
        endpoint_source_sha256=ENDPOINT_SOURCE_SHA,
        identity_receipt=_identity_receipt(m),
    )
    for field in (
        "live_observation_performed",
        "host_backend_invoked",
        "http_request_performed",
        "systemd_query_performed",
        "subprocess_execution_performed",
        "model_inference_performed",
        "canonical_provider_binding_present",
        "canonical_collection_enabled",
        "runtime_readiness_admitted",
        "runtime_execution_authorized",
    ):
        assert out[field] is False


def test_static_source_has_no_host_io_or_live_calls():
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
        "live_identity_contract.collect_v2r13_live_identity",
        "identity_receipt_validator.collect_live_v2r13_runtime_identity",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call):
            assert _dotted(node.func) not in forbidden_calls


def test_live_collection_entrypoint_always_holds_without_canonical_binding():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13LiveIdentityCollectorImplementationHold,
        "GENERATION2_V2R13_CANONICAL_IMPLEMENTATION_SOURCE_BINDING_NOT_PRESENT",
        lambda: m.collect_v2r13_live_identity(),
    )
