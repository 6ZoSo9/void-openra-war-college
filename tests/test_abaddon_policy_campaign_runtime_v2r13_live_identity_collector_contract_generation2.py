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
    "abaddon_policy_campaign_runtime_v2r13_live_identity_collector_contract_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_live_identity_collector_contract_generation2.py"
)

EXPECTED_SOURCE_SHA256 = "907195d559e7489de995b352f2d72d9b4125f32d7d74a19a7004f6067f29f164"
EXPECTED_SEMANTIC_SHA256 = "0bda63a4d82be7f38e604c15fe63f659051cc42527bc9281317df167f6145219"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_v2r13_live_identity_collector_contract",
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
        ensure_ascii=True,
    ).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


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


def test_semantic_sha_is_exact_and_stable():
    m = _load()
    assert m.EXPECTED_COLLECTOR_CONTRACT_SHA256 == EXPECTED_SEMANTIC_SHA256
    assert m.collector_contract_sha256() == EXPECTED_SEMANTIC_SHA256


def test_manifest_canonical_roundtrip_matches_semantic_sha():
    m = _load()
    manifest = m.collector_contract_manifest()
    assert _stable_sha(manifest) == EXPECTED_SEMANTIC_SHA256


def test_manifest_hash_changes_when_semantics_change():
    m = _load()
    manifest = m.collector_contract_manifest()
    manifest["collector_binding_activation"] = True
    assert _stable_sha(manifest) != EXPECTED_SEMANTIC_SHA256


def test_contract_binds_exact_canonical_blobs():
    m = _load()
    out = m.validate_v2r13_live_identity_collector_contract()
    manifest = out["manifest"]
    assert manifest["activation_contract_git_blob"] == (
        "a3acb42280c334daa24a3b830105a04666fd603b"
    )
    assert manifest["observation_mechanics_git_blob"] == (
        "5fc94c056d1ad7de41b5d7156bce9b3f500f29ba"
    )
    assert manifest["identity_receipt_validator_git_blob"] == (
        "d1586ba032d78296e200d5016560682b82ee599d"
    )
    assert manifest["generic_designated_host_readonly_reference_git_blob"] == (
        "aadcc32fbba9a11d9f4d53f2410a7321c46c0131"
    )


def test_contract_binds_exact_v2r13_identity_targets():
    m = _load()
    manifest = m.collector_contract_manifest()
    assert manifest["expected_chat_completions_url"] == (
        "http://127.0.0.1:11434/v1/chat/completions"
    )
    assert manifest["expected_model_alias"] == "void-apollyon-candidate-v2r13:latest"
    assert manifest["expected_model_digest"] == (
        "b52834ea46c10362e9bb20cd2e721716016bb36f800ddbc62e7fbaa24fb40932"
    )
    assert manifest["expected_runtime_image_id"] == (
        "sha256:79f2f6800382489a2a648839fc0d58e546384938439378aeea06461363de25f5"
    )


def test_contract_binds_exact_receipt_schema():
    m = _load()
    manifest = m.collector_contract_manifest()
    assert manifest["receipt_schema"] == m.identity_receipt_validator.RECEIPT_SCHEMA


def test_generic_readonly_reference_is_design_only():
    m = _load()
    manifest = m.collector_contract_manifest()
    assert (
        manifest[
            "generic_designated_host_reference_admitted_as_v2r13_identity_proof"
        ]
        is False
    )
    assert (
        manifest["generic_designated_host_reference_is_design_reference_only"]
        is True
    )


def test_inference_endpoint_cannot_be_reused_as_probe():
    m = _load()
    manifest = m.collector_contract_manifest()
    assert manifest["inference_endpoint_may_be_reused_as_identity_probe"] is False
    assert manifest["chat_completions_request_allowed_for_liveness"] is False
    assert manifest["identity_probe_may_run_model_inference"] is False


def test_channel_set_is_exact_three_unresolved_primitives():
    m = _load()
    channels = m.collector_contract_manifest()["channels"]
    assert set(channels) == {
        "endpoint_liveness",
        "model_identity_verified",
        "runtime_image_identity_verified",
    }


def test_all_three_channels_are_required_but_unimplemented():
    m = _load()
    channels = m.collector_contract_manifest()["channels"]
    for row in channels.values():
        assert row["required"] is True
        assert row["collector_implemented"] is False
        assert row["backend_mechanism"] == "unresolved"


def test_endpoint_liveness_requires_non_inference_route_but_defines_none():
    m = _load()
    endpoint = m.collector_contract_manifest()["channels"]["endpoint_liveness"]
    assert endpoint["expected_loopback_host"] == "127.0.0.1"
    assert endpoint["expected_port"] == 11434
    assert endpoint["non_inference_route_required"] is True
    assert endpoint["canonical_non_inference_probe_route_defined"] is False
    assert endpoint["may_call_chat_completions"] is False
    assert endpoint["may_run_model_inference"] is False


def test_model_identity_channel_is_unresolved_and_noninferential():
    m = _load()
    row = m.collector_contract_manifest()["channels"]["model_identity_verified"]
    assert row["expected_model_alias"] == m.activation_contract.V2R13_MODEL_ALIAS
    assert row["expected_model_digest"] == m.activation_contract.V2R13_MODEL_DIGEST
    assert row["canonical_live_identity_route_defined"] is False
    assert row["may_run_model_inference"] is False


def test_runtime_image_channel_is_unresolved_and_nonmutating():
    m = _load()
    row = m.collector_contract_manifest()["channels"][
        "runtime_image_identity_verified"
    ]
    assert row["expected_runtime_image_id"] == m.activation_contract.V2R13_RUNTIME_IMAGE_ID
    assert row["canonical_live_identity_route_defined"] is False
    assert row["may_start_or_restart_runtime"] is False


def test_contract_requires_separate_implementation_binding():
    m = _load()
    out = m.validate_v2r13_live_identity_collector_contract()
    assert out["implementation_source_binding_required_before_admission"] is True
    assert out["implementation_source_sha256"] is None
    assert out["collector_binding_activation"] is False
    assert out["collector_implementation_present"] is False


def test_contract_requires_explicit_authority_and_no_auto_backend():
    m = _load()
    out = m.validate_v2r13_live_identity_collector_contract()
    assert out["explicit_observation_authority_required"] is True
    assert out["automatic_host_backend_selection"] is False


def test_contract_preserves_identity_validator_trust_boundary():
    m = _load()
    validator = (
        m.identity_receipt_validator.v2r13_runtime_identity_receipt_validator_contract()
    )
    assert validator["collector_contract_binding_required_for_identity_admission"] is True
    assert validator["self_reported_collector_sha_is_sufficient"] is False
    assert validator["model_identity_provider_primitive_implemented"] is False
    assert validator["runtime_image_provider_primitive_implemented"] is False


def test_contract_preserves_exact_13_3_frontier():
    m = _load()
    out = m.validate_v2r13_live_identity_collector_contract()
    assert out["supported_primitive_count_remains"] == 13
    assert out["remaining_unresolved_primitive_count_remains"] == 3
    assert out["model_identity_verified"] is False
    assert out["runtime_image_identity_verified"] is False


def test_contract_grants_no_mutation_execution_or_funds_authority():
    m = _load()
    manifest = m.collector_contract_manifest()
    for field in (
        "collector_may_mutate",
        "collector_may_start_runtime",
        "collector_may_stop_runtime",
        "collector_may_reload_service",
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


def test_validation_never_admits_collector_readiness_or_execution():
    m = _load()
    out = m.validate_v2r13_live_identity_collector_contract()
    assert out["live_observation_performed"] is False
    assert out["collector_executed"] is False
    assert out["collector_identity_admitted"] is False
    assert out["canonical_provider_binding_present"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_contract_identity_is_semantic_only():
    m = _load()
    out = m.collector_contract_identity()
    assert out["collector_contract_sha256"] == EXPECTED_SEMANTIC_SHA256
    assert out["semantic_contract_valid"] is True
    assert out["implementation_source_binding_present"] is False
    assert out["collector_binding_activation"] is False
    assert out["collector_identity_admitted"] is False


def test_manifest_result_is_copy_isolated():
    m = _load()
    first = m.validate_v2r13_live_identity_collector_contract()
    first["manifest"]["channels"]["endpoint_liveness"]["collector_implemented"] = True
    second = m.validate_v2r13_live_identity_collector_contract()
    assert (
        second["manifest"]["channels"]["endpoint_liveness"]["collector_implemented"]
        is False
    )


def test_static_source_has_no_host_io_or_live_probe_calls():
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
        "identity_receipt_validator.collect_live_v2r13_runtime_identity",
        "observation_mechanics.collect_runtime_identity",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call):
            assert _dotted(node.func) not in forbidden_calls


def test_live_collector_entrypoint_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13LiveIdentityCollectorContractHold,
        "GENERATION2_V2R13_LIVE_IDENTITY_COLLECTOR_IMPLEMENTATION_NOT_PRESENT",
        lambda: m.collect_v2r13_live_identity(),
    )
