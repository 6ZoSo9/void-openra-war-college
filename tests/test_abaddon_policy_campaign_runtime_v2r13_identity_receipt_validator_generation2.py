from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_v2r13_identity_receipt_validator_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_identity_receipt_validator_generation2.py"
)
EXPECTED_SOURCE_SHA256 = (
    "fea7eb190d6e44a8980189d2e1d281708508daf0529fb2f7644e898bb9311e74"
)


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_v2r13_identity_receipt_validator",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _receipt(m):
    return {
        "schema": m.RECEIPT_SCHEMA,
        "snapshot_id": m.activation_contract.V2R13,
        "observation_mode": "read_only",
        "collector_contract_sha256": "a" * 64,
        "active_model_alias": m.EXPECTED_MODEL_ALIAS,
        "active_model_digest": m.EXPECTED_MODEL_DIGEST,
        "runtime_image_id": m.EXPECTED_RUNTIME_IMAGE_ID,
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
    out = m.v2r13_runtime_identity_receipt_validator_contract()
    assert out["activation_contract_git_blob"] == (
        "a3acb42280c334daa24a3b830105a04666fd603b"
    )
    assert out["activation_evidence_git_blob"] == (
        "aac7964d9e80633535003b9f27066cac1bb4bac2"
    )
    assert out["runtime_realizations_git_blob"] == (
        "0dbae61b0be96445e5fd6c23a07491a03f18b679"
    )


def test_contract_binds_exact_expected_identity():
    m = _load()
    out = m.v2r13_runtime_identity_receipt_validator_contract()
    assert out["expected_model_alias"] == "void-apollyon-candidate-v2r13:latest"
    assert out["expected_model_digest"] == (
        "b52834ea46c10362e9bb20cd2e721716016bb36f800ddbc62e7fbaa24fb40932"
    )
    assert out["expected_runtime_image_id"] == (
        "sha256:79f2f6800382489a2a648839fc0d58e546384938439378aeea06461363de25f5"
    )


def test_contract_does_not_admit_identity_primitives():
    m = _load()
    out = m.v2r13_runtime_identity_receipt_validator_contract()
    assert out["supplied_receipt_shape_validator_implemented"] is True
    assert out["collector_contract_binding_required_for_identity_admission"] is True
    assert out["self_reported_collector_sha_is_sufficient"] is False
    assert out["model_identity_provider_primitive_implemented"] is False
    assert out["runtime_image_provider_primitive_implemented"] is False


def test_contract_preserves_13_3_frontier():
    m = _load()
    out = m.v2r13_runtime_identity_receipt_validator_contract()
    assert out["supported_primitive_count_remains"] == 13
    assert out["remaining_unresolved_primitive_count_remains"] == 3
    assert out["remaining_unresolved_primitive_names"] == (
        "endpoint_liveness",
        "model_identity_verified",
        "runtime_image_identity_verified",
    )


def test_contract_keeps_live_and_admission_surfaces_closed():
    m = _load()
    out = m.v2r13_runtime_identity_receipt_validator_contract()
    for field in (
        "live_collection_implemented",
        "validator_filesystem_observation_implemented",
        "validator_git_query_implemented",
        "validator_path_resolution_implemented",
        "validator_subprocess_execution_implemented",
        "validator_endpoint_probe_implemented",
        "validator_systemd_query_implemented",
        "canonical_provider_binding_present",
        "canonical_collection_enabled",
        "runtime_readiness_admitted",
        "runtime_execution_authorized",
    ):
        assert out[field] is False


def test_valid_receipt_matches_expected_values_but_is_not_admitted():
    m = _load()
    out = m.validate_v2r13_runtime_identity_receipt(_receipt(m))
    assert out["receipt_shape_valid"] is True
    assert out["expected_identity_values_match"] is True
    assert out["collector_identity_admitted"] is False
    assert out["model_identity_verified"] is False
    assert out["runtime_image_identity_verified"] is False


def test_valid_receipt_preserves_exact_identity_values():
    m = _load()
    out = m.validate_v2r13_runtime_identity_receipt(_receipt(m))
    assert out["active_model_alias"] == m.EXPECTED_MODEL_ALIAS
    assert out["active_model_digest"] == m.EXPECTED_MODEL_DIGEST
    assert out["runtime_image_id"] == m.EXPECTED_RUNTIME_IMAGE_ID


def test_valid_receipt_reports_observation_claims_only():
    m = _load()
    out = m.validate_v2r13_runtime_identity_receipt(_receipt(m))
    assert out["model_identity_observation_claimed"] is True
    assert out["runtime_image_identity_observation_claimed"] is True
    assert out["collector_identity_admitted"] is False


def test_validator_reports_no_collection_of_its_own():
    m = _load()
    out = m.validate_v2r13_runtime_identity_receipt(_receipt(m))
    for field in (
        "validator_collection_performed",
        "validator_filesystem_observation_performed",
        "validator_external_worktree_git_query_performed",
        "validator_path_resolution_performed",
        "validator_subprocess_execution_performed",
        "validator_endpoint_probe_performed",
        "validator_systemd_query_performed",
        "validator_model_load_performed",
        "validator_model_inference_performed",
    ):
        assert out[field] is False


def test_input_is_not_mutated_and_output_receipt_is_copy():
    m = _load()
    receipt = _receipt(m)
    before = copy.deepcopy(receipt)
    out = m.validate_v2r13_runtime_identity_receipt(receipt)
    assert receipt == before
    out["validated_receipt"]["active_model_digest"] = "0" * 64
    assert receipt["active_model_digest"] == m.EXPECTED_MODEL_DIGEST


def test_model_alias_drift_is_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["active_model_alias"] = "wrong"
    _expect_hold(
        m.RuntimeV2R13IdentityReceiptValidatorHold,
        "active model alias drift",
        lambda: m.validate_v2r13_runtime_identity_receipt(receipt),
    )


def test_model_digest_drift_is_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["active_model_digest"] = "0" * 64
    _expect_hold(
        m.RuntimeV2R13IdentityReceiptValidatorHold,
        "active model digest drift",
        lambda: m.validate_v2r13_runtime_identity_receipt(receipt),
    )


def test_runtime_image_drift_is_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["runtime_image_id"] = "sha256:" + "0" * 64
    _expect_hold(
        m.RuntimeV2R13IdentityReceiptValidatorHold,
        "runtime image identity drift",
        lambda: m.validate_v2r13_runtime_identity_receipt(receipt),
    )


def test_model_observation_not_claimed_is_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["model_identity_observation_performed"] = False
    _expect_hold(
        m.RuntimeV2R13IdentityReceiptValidatorHold,
        "model identity observation not claimed",
        lambda: m.validate_v2r13_runtime_identity_receipt(receipt),
    )


def test_runtime_image_observation_not_claimed_is_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["runtime_image_identity_observation_performed"] = False
    _expect_hold(
        m.RuntimeV2R13IdentityReceiptValidatorHold,
        "runtime image observation not claimed",
        lambda: m.validate_v2r13_runtime_identity_receipt(receipt),
    )


def test_collector_sha_malformed_is_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["collector_contract_sha256"] = "not-a-sha"
    _expect_hold(
        m.RuntimeV2R13IdentityReceiptValidatorHold,
        "collector contract SHA malformed",
        lambda: m.validate_v2r13_runtime_identity_receipt(receipt),
    )


def test_model_inference_claim_is_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["model_inference_performed"] = True
    _expect_hold(
        m.RuntimeV2R13IdentityReceiptValidatorHold,
        "model_inference_performed",
        lambda: m.validate_v2r13_runtime_identity_receipt(receipt),
    )


def test_service_action_claim_is_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["service_action_performed"] = True
    _expect_hold(
        m.RuntimeV2R13IdentityReceiptValidatorHold,
        "service_action_performed",
        lambda: m.validate_v2r13_runtime_identity_receipt(receipt),
    )


def test_missing_field_is_rejected():
    m = _load()
    receipt = _receipt(m)
    del receipt["runtime_image_id"]
    _expect_hold(
        m.RuntimeV2R13IdentityReceiptValidatorHold,
        "field-set drift",
        lambda: m.validate_v2r13_runtime_identity_receipt(receipt),
    )


def test_static_source_has_no_host_io_or_collection_calls():
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
        "activation_contract.activation_descriptor",
        "activation_contract.reviewed_opponent_runtime_realizations",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call):
            assert _dotted(node.func) not in forbidden_calls


def test_live_collection_entrypoint_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13IdentityReceiptValidatorHold,
        "GENERATION2_V2R13_LIVE_RUNTIME_IDENTITY_COLLECTION_NOT_IMPLEMENTED",
        lambda: m.collect_live_v2r13_runtime_identity(),
    )
