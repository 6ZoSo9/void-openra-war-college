from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_v2r13_runtime_image_readonly_observer_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_runtime_image_readonly_observer_generation2.py"
)

EXPECTED_SOURCE_SHA256 = "70718ab3f5387342cee874ab14603fc0831e0a713919825b747ff5f2f4c2c595"
BACKEND_SOURCE_SHA = "b" * 64


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_v2r13_runtime_image_readonly_observer",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _receipt(m):
    return {
        "schema": m.BACKEND_RECEIPT_SCHEMA,
        "snapshot_id": m.activation_contract.V2R13,
        "primitive_name": "runtime_image_identity_verified",
        "source_sha256": BACKEND_SOURCE_SHA,
        "backend_kind": "synthetic-reviewed-readonly-backend",
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


class FakeBackend:
    def __init__(self, receipt):
        self.receipt = receipt
        self.calls = 0

    def __call__(self):
        self.calls += 1
        return copy.deepcopy(self.receipt)


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


def test_contract_binds_exact_canonical_sources_and_semantic_sha():
    m = _load()
    out = m.v2r13_runtime_image_readonly_observer_contract()
    assert out["live_identity_collector_contract_git_blob"] == (
        "db9fbb58f3d5870c77a796641afb1014acc19ee4"
    )
    assert out["activation_contract_git_blob"] == (
        "a3acb42280c334daa24a3b830105a04666fd603b"
    )
    assert out["live_identity_collector_semantic_sha256"] == (
        "0bda63a4d82be7f38e604c15fe63f659051cc42527bc9281317df167f6145219"
    )
    assert out["semantic_contract_valid"] is True


def test_contract_binds_exact_expected_runtime_image_id():
    m = _load()
    out = m.v2r13_runtime_image_readonly_observer_contract()
    assert out["expected_runtime_image_id"] == (
        "sha256:79f2f6800382489a2a648839fc0d58e546384938439378aeea06461363de25f5"
    )
    assert out["expected_runtime_image_id"] == m.activation_contract.V2R13_RUNTIME_IMAGE_ID


def test_contract_implements_only_backend_agnostic_interface():
    m = _load()
    out = m.v2r13_runtime_image_readonly_observer_contract()
    assert out["runtime_image_backend_protocol_implemented"] is True
    assert out["supplied_backend_receipt_validator_implemented"] is True
    assert out["reviewed_backend_source_binding_required"] is True
    assert out["canonical_backend_source_binding_present"] is False


def test_contract_keeps_all_concrete_host_backends_absent():
    m = _load()
    out = m.v2r13_runtime_image_readonly_observer_contract()
    for field in (
        "docker_backend_implemented",
        "podman_backend_implemented",
        "containerd_backend_implemented",
        "systemd_backend_implemented",
        "process_backend_implemented",
        "filesystem_backend_implemented",
        "network_backend_implemented",
        "subprocess_backend_implemented",
    ):
        assert out[field] is False


def test_contract_requires_explicit_authority_and_no_auto_backend():
    m = _load()
    out = m.v2r13_runtime_image_readonly_observer_contract()
    assert out["automatic_backend_selection"] is False
    assert out["observation_requires_explicit_authority"] is True


def test_contract_preserves_exact_13_3_frontier():
    m = _load()
    out = m.v2r13_runtime_image_readonly_observer_contract()
    assert out["runtime_image_identity_provider_primitive_implemented"] is False
    assert out["candidate_observation_does_not_advance_primitive_frontier"] is True
    assert out["supported_primitive_count_remains"] == 13
    assert out["remaining_unresolved_primitive_count_remains"] == 3
    assert out["remaining_unresolved_primitive_names"] == (
        "endpoint_liveness",
        "model_identity_verified",
        "runtime_image_identity_verified",
    )


def test_contract_keeps_admission_and_execution_closed():
    m = _load()
    out = m.v2r13_runtime_image_readonly_observer_contract()
    assert out["candidate_observation_does_not_admit_collector_identity"] is True
    for field in (
        "service_action_implemented",
        "runtime_start_stop_reload_implemented",
        "model_load_implemented",
        "model_inference_implemented",
        "canonical_provider_binding_present",
        "runtime_readiness_admitted",
        "runtime_execution_authorized",
    ):
        assert out[field] is False


def test_observation_requires_explicit_authority_before_backend_call():
    m = _load()
    backend = FakeBackend(_receipt(m))
    _expect_hold(
        m.RuntimeV2R13RuntimeImageObserverHold,
        "OBSERVATION_NOT_AUTHORIZED",
        lambda: m.observe_v2r13_runtime_image_readonly(
            observation_authorized=False,
            backend=backend,
            reviewed_backend_source_sha256=BACKEND_SOURCE_SHA,
        ),
    )
    assert backend.calls == 0


def test_malformed_reviewed_source_sha_rejected_before_backend_call():
    m = _load()
    backend = FakeBackend(_receipt(m))
    _expect_hold(
        m.RuntimeV2R13RuntimeImageObserverHold,
        "backend source SHA malformed",
        lambda: m.observe_v2r13_runtime_image_readonly(
            observation_authorized=True,
            backend=backend,
            reviewed_backend_source_sha256="not-a-sha",
        ),
    )
    assert backend.calls == 0


def test_noncallable_backend_is_rejected():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13RuntimeImageObserverHold,
        "backend required",
        lambda: m.observe_v2r13_runtime_image_readonly(
            observation_authorized=True,
            backend=None,
            reviewed_backend_source_sha256=BACKEND_SOURCE_SHA,
        ),
    )


def test_valid_fake_backend_called_exactly_once():
    m = _load()
    backend = FakeBackend(_receipt(m))
    out = m.observe_v2r13_runtime_image_readonly(
        observation_authorized=True,
        backend=backend,
        reviewed_backend_source_sha256=BACKEND_SOURCE_SHA,
    )
    assert backend.calls == 1
    assert out["runtime_image_identity_observed"] is True


def test_valid_fake_observation_matches_expected_but_is_not_verified():
    m = _load()
    out = m.observe_v2r13_runtime_image_readonly(
        observation_authorized=True,
        backend=FakeBackend(_receipt(m)),
        reviewed_backend_source_sha256=BACKEND_SOURCE_SHA,
    )
    assert out["runtime_image_identity_matches_expected"] is True
    assert out["runtime_image_id"] == m.activation_contract.V2R13_RUNTIME_IMAGE_ID
    assert out["runtime_image_identity_verified"] is False


def test_valid_fake_observation_admits_nothing():
    m = _load()
    out = m.observe_v2r13_runtime_image_readonly(
        observation_authorized=True,
        backend=FakeBackend(_receipt(m)),
        reviewed_backend_source_sha256=BACKEND_SOURCE_SHA,
    )
    assert out["canonical_backend_source_binding_present"] is False
    assert out["collector_identity_admitted"] is False
    assert out["canonical_provider_binding_present"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_valid_fake_observation_preserves_13_3_frontier():
    m = _load()
    out = m.observe_v2r13_runtime_image_readonly(
        observation_authorized=True,
        backend=FakeBackend(_receipt(m)),
        reviewed_backend_source_sha256=BACKEND_SOURCE_SHA,
    )
    assert out["supported_primitive_count_remains"] == 13
    assert out["remaining_unresolved_primitive_count_remains"] == 3
    assert out["remaining_unresolved_primitive_names"] == (
        "endpoint_liveness",
        "model_identity_verified",
        "runtime_image_identity_verified",
    )


def test_source_binding_mismatch_is_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["source_sha256"] = "c" * 64
    _expect_hold(
        m.RuntimeV2R13RuntimeImageObserverHold,
        "source binding mismatch",
        lambda: m.observe_v2r13_runtime_image_readonly(
            observation_authorized=True,
            backend=FakeBackend(receipt),
            reviewed_backend_source_sha256=BACKEND_SOURCE_SHA,
        ),
    )


def test_runtime_image_identity_drift_is_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["runtime_image_id"] = "sha256:" + "0" * 64
    _expect_hold(
        m.RuntimeV2R13RuntimeImageObserverHold,
        "runtime-image identity drift",
        lambda: m.observe_v2r13_runtime_image_readonly(
            observation_authorized=True,
            backend=FakeBackend(receipt),
            reviewed_backend_source_sha256=BACKEND_SOURCE_SHA,
        ),
    )


def test_missing_receipt_field_is_rejected():
    m = _load()
    receipt = _receipt(m)
    del receipt["runtime_reload_performed"]
    _expect_hold(
        m.RuntimeV2R13RuntimeImageObserverHold,
        "field-set drift",
        lambda: m.observe_v2r13_runtime_image_readonly(
            observation_authorized=True,
            backend=FakeBackend(receipt),
            reviewed_backend_source_sha256=BACKEND_SOURCE_SHA,
        ),
    )


def test_receipt_schema_drift_is_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["schema"] = "wrong"
    _expect_hold(
        m.RuntimeV2R13RuntimeImageObserverHold,
        "schema drift",
        lambda: m.observe_v2r13_runtime_image_readonly(
            observation_authorized=True,
            backend=FakeBackend(receipt),
            reviewed_backend_source_sha256=BACKEND_SOURCE_SHA,
        ),
    )


def test_primitive_name_drift_is_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["primitive_name"] = "model_identity_verified"
    _expect_hold(
        m.RuntimeV2R13RuntimeImageObserverHold,
        "primitive-name drift",
        lambda: m.observe_v2r13_runtime_image_readonly(
            observation_authorized=True,
            backend=FakeBackend(receipt),
            reviewed_backend_source_sha256=BACKEND_SOURCE_SHA,
        ),
    )


def test_empty_backend_kind_is_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["backend_kind"] = ""
    _expect_hold(
        m.RuntimeV2R13RuntimeImageObserverHold,
        "backend kind missing",
        lambda: m.observe_v2r13_runtime_image_readonly(
            observation_authorized=True,
            backend=FakeBackend(receipt),
            reviewed_backend_source_sha256=BACKEND_SOURCE_SHA,
        ),
    )


def test_observation_false_claim_is_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["runtime_image_identity_observation_performed"] = False
    _expect_hold(
        m.RuntimeV2R13RuntimeImageObserverHold,
        "observation not performed",
        lambda: m.observe_v2r13_runtime_image_readonly(
            observation_authorized=True,
            backend=FakeBackend(receipt),
            reviewed_backend_source_sha256=BACKEND_SOURCE_SHA,
        ),
    )


def test_mutation_claim_is_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["mutation_performed"] = True
    _expect_hold(
        m.RuntimeV2R13RuntimeImageObserverHold,
        "mutation_performed",
        lambda: m.observe_v2r13_runtime_image_readonly(
            observation_authorized=True,
            backend=FakeBackend(receipt),
            reviewed_backend_source_sha256=BACKEND_SOURCE_SHA,
        ),
    )


def test_service_action_claim_is_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["service_action_performed"] = True
    _expect_hold(
        m.RuntimeV2R13RuntimeImageObserverHold,
        "service_action_performed",
        lambda: m.observe_v2r13_runtime_image_readonly(
            observation_authorized=True,
            backend=FakeBackend(receipt),
            reviewed_backend_source_sha256=BACKEND_SOURCE_SHA,
        ),
    )


def test_runtime_start_claim_is_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["runtime_start_performed"] = True
    _expect_hold(
        m.RuntimeV2R13RuntimeImageObserverHold,
        "runtime_start_performed",
        lambda: m.observe_v2r13_runtime_image_readonly(
            observation_authorized=True,
            backend=FakeBackend(receipt),
            reviewed_backend_source_sha256=BACKEND_SOURCE_SHA,
        ),
    )


def test_model_inference_claim_is_rejected():
    m = _load()
    receipt = _receipt(m)
    receipt["model_inference_performed"] = True
    _expect_hold(
        m.RuntimeV2R13RuntimeImageObserverHold,
        "model_inference_performed",
        lambda: m.observe_v2r13_runtime_image_readonly(
            observation_authorized=True,
            backend=FakeBackend(receipt),
            reviewed_backend_source_sha256=BACKEND_SOURCE_SHA,
        ),
    )


def test_inputs_are_not_mutated_and_nested_output_is_copy_isolated():
    m = _load()
    receipt = _receipt(m)
    before = copy.deepcopy(receipt)
    out = m.observe_v2r13_runtime_image_readonly(
        observation_authorized=True,
        backend=FakeBackend(receipt),
        reviewed_backend_source_sha256=BACKEND_SOURCE_SHA,
    )
    assert receipt == before
    out["backend_receipt_validation"]["validated_receipt"]["runtime_image_id"] = "changed"
    assert receipt["runtime_image_id"] == m.activation_contract.V2R13_RUNTIME_IMAGE_ID


def test_static_source_has_no_concrete_host_backend_imports_or_calls():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    forbidden_import_roots = {
        "os",
        "subprocess",
        "pathlib",
        "socket",
        "urllib",
        "http",
        "requests",
        "httpx",
        "docker",
        "podman",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots

    calls = [_dotted(node.func) for node in ast.walk(tree) if isinstance(node, ast.Call)]
    forbidden_call_tokens = (
        "subprocess.",
        "os.",
        "urllib.",
        "requests.",
        "httpx.",
        "docker.",
        "podman.",
    )
    assert not any(
        call.startswith(token)
        for call in calls
        for token in forbidden_call_tokens
    )
