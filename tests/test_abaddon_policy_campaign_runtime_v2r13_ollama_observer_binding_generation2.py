from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_v2r13_ollama_observer_binding_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_ollama_observer_binding_generation2.py"
)

EXPECTED_SOURCE_SHA256 = "c6b0bb746d017326e600f401a2d07a29fba79aced401687c4eb5238084ee9335"
REVIEWED_OBSERVER_SOURCE_SHA = (
    "c770d08621ff1d32996e64962bd539c783bd4ba5c259687d1a348a2db775a7ff"
)


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_v2r13_ollama_observer_binding",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _observation(m):
    return {
        "schema": m.ollama_observer.OBSERVATION_SCHEMA,
        "snapshot_id": m.activation_contract.V2R13,
        "observation_mode": "read_only",
        "tags_url": m.ollama_observer.OLLAMA_TAGS_URL,
        "ps_url": m.ollama_observer.OLLAMA_PS_URL,
        "chat_completions_url": m.ollama_observer.FORBIDDEN_CHAT_COMPLETIONS_URL,
        "chat_completions_request_performed": False,
        "endpoint_liveness_observed": True,
        "catalog_model_alias": m.activation_contract.V2R13_MODEL_ALIAS,
        "catalog_model_digest": m.activation_contract.V2R13_MODEL_DIGEST,
        "running_model_alias": m.activation_contract.V2R13_MODEL_ALIAS,
        "running_model_digest": m.activation_contract.V2R13_MODEL_DIGEST,
        "model_catalog_identity_matches_expected": True,
        "running_model_identity_matches_expected": True,
        "model_identity_observation_performed": True,
        "runtime_image_identity_observation_performed": False,
        "runtime_image_id": None,
        "runtime_image_identity_verified": False,
        "collector_identity_admitted": False,
        "canonical_provider_binding_present": False,
        "runtime_readiness_admitted": False,
        "runtime_execution_authorized": False,
        "mutation_performed": False,
        "service_action_performed": False,
        "runtime_start_performed": False,
        "runtime_stop_performed": False,
        "runtime_reload_performed": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
    }


def _validate(m, observation=None, source_sha=REVIEWED_OBSERVER_SOURCE_SHA):
    if observation is None:
        observation = _observation(m)
    return m.validate_bound_ollama_observation(
        observation,
        observer_source_sha256=source_sha,
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


def test_contract_pins_exact_observer_source_identities():
    m = _load()
    out = m.v2r13_ollama_observer_binding_contract()
    assert out["ollama_observer_git_blob"] == (
        "9b859e91b8833260a1af7e189ec5cd30d92d9451"
    )
    assert out["ollama_observer_source_sha256"] == REVIEWED_OBSERVER_SOURCE_SHA
    assert out["observer_source_identity_pinned_by_git_blob"] is True
    assert out["observer_source_identity_pinned_by_sha256"] is True


def test_contract_pins_runtime_image_binding_identity():
    m = _load()
    out = m.v2r13_ollama_observer_binding_contract()
    assert out["runtime_image_binding_git_blob"] == (
        "7075ded7a19454239b95a09e7b4630413124a796"
    )
    assert out["runtime_image_binding_source_sha256"] == (
        "74acc7248ee19d2d141aa4ec36fc3ce1c6068c56ca1801719c3287cd2c774f52"
    )


def test_contract_is_separate_non_self_binding_instrument():
    m = _load()
    out = m.v2r13_ollama_observer_binding_contract()
    assert out["separate_binding_instrument"] is True
    assert out["observer_source_is_not_self_bound"] is True
    assert out["canonical_observer_source_binding_present"] is True


def test_contract_implements_exact_two_remaining_primitives():
    m = _load()
    out = m.v2r13_ollama_observer_binding_contract()
    assert out["endpoint_liveness_provider_primitive_implemented"] is True
    assert out["model_identity_provider_primitive_implemented"] is True
    assert out["runtime_image_identity_provider_already_implemented"] is True


def test_contract_advances_exact_14_2_to_16_0_frontier():
    m = _load()
    out = m.v2r13_ollama_observer_binding_contract()
    assert out["baseline_supported_primitive_count"] == 14
    assert out["supported_primitive_count_after_binding"] == 16
    assert out["remaining_unresolved_primitive_count"] == 0
    assert out["remaining_unresolved_primitive_names"] == ()
    assert out["all_v2r13_provider_primitives_implemented"] is True


def test_contract_keeps_provider_readiness_execution_closed():
    m = _load()
    out = m.v2r13_ollama_observer_binding_contract()
    assert out["full_collector_identity_admitted"] is False
    assert out["canonical_provider_binding_present"] is False
    assert out["canonical_collection_enabled"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_contract_has_zero_live_observation_surface():
    m = _load()
    out = m.v2r13_ollama_observer_binding_contract()
    for field in (
        "automatic_host_backend_selection",
        "binding_live_observation_implemented",
        "binding_http_request_implemented",
        "binding_host_backend_invocation_implemented",
        "binding_filesystem_observation_implemented",
        "binding_git_query_implemented",
        "binding_subprocess_execution_implemented",
        "binding_model_inference_implemented",
        "binding_game_execution_implemented",
    ):
        assert out[field] is False


def test_live_collection_entrypoint_hard_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "BOUND_OLLAMA_LIVE_COLLECTION_NOT_IMPLEMENTED",
        lambda: m.collect_bound_ollama_identity(),
    )


def test_valid_bound_observation_verifies_endpoint_and_model():
    m = _load()
    out = _validate(m)
    assert out["canonical_observer_source_binding_present"] is True
    assert out["endpoint_liveness_verified"] is True
    assert out["model_identity_verified"] is True
    assert out["runtime_image_identity_provider_already_canonical"] is True


def test_valid_bound_observation_pins_observer_identity():
    m = _load()
    out = _validate(m)
    assert out["reviewed_observer_source_sha256"] == REVIEWED_OBSERVER_SOURCE_SHA
    assert out["reviewed_observer_git_blob"] == (
        "9b859e91b8833260a1af7e189ec5cd30d92d9451"
    )


def test_valid_bound_observation_has_exact_primitive_values():
    m = _load()
    out = _validate(m)
    assert out["primitive_values"] == {
        "endpoint_liveness": True,
        "model_identity_verified": True,
    }


def test_valid_bound_observation_reaches_16_0_capability_coverage():
    m = _load()
    out = _validate(m)
    assert out["supported_primitive_count_after_binding"] == 16
    assert out["remaining_unresolved_primitive_count"] == 0
    assert out["remaining_unresolved_primitive_names"] == ()
    assert out["all_v2r13_provider_primitives_implemented"] is True


def test_valid_bound_observation_does_not_admit_provider_or_readiness():
    m = _load()
    out = _validate(m)
    assert out["full_collector_identity_admitted"] is False
    assert out["canonical_provider_binding_present"] is False
    assert out["canonical_collection_enabled"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_valid_bound_observation_reports_zero_binding_io():
    m = _load()
    out = _validate(m)
    for field in (
        "binding_http_request_performed",
        "binding_host_backend_invocation_performed",
        "binding_filesystem_observation_performed",
        "binding_git_query_performed",
        "binding_subprocess_execution_performed",
        "binding_model_inference_performed",
        "binding_game_execution_performed",
    ):
        assert out[field] is False


def test_inputs_are_not_mutated_and_output_is_copy_isolated():
    m = _load()
    observation = _observation(m)
    before = copy.deepcopy(observation)
    out = _validate(m, observation)
    assert observation == before
    out["validated_observation"]["catalog_model_alias"] = "changed"
    assert observation["catalog_model_alias"] == m.activation_contract.V2R13_MODEL_ALIAS


def test_source_sha_drift_rejected():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "observer source SHA mismatch",
        lambda: _validate(m, source_sha="0" * 64),
    )


def test_extra_observation_field_rejected():
    m = _load()
    value = _observation(m)
    value["extra"] = True
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "field-set drift",
        lambda: _validate(m, value),
    )


def test_missing_observation_field_rejected():
    m = _load()
    value = _observation(m)
    del value["runtime_reload_performed"]
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "field-set drift",
        lambda: _validate(m, value),
    )


def test_observation_schema_drift_rejected():
    m = _load()
    value = _observation(m)
    value["schema"] = "wrong"
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "schema drift",
        lambda: _validate(m, value),
    )


def test_snapshot_drift_rejected():
    m = _load()
    value = _observation(m)
    value["snapshot_id"] = "wrong"
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "snapshot drift",
        lambda: _validate(m, value),
    )


def test_observation_mode_drift_rejected():
    m = _load()
    value = _observation(m)
    value["observation_mode"] = "read_write"
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "observation mode must be read_only",
        lambda: _validate(m, value),
    )


def test_tags_url_drift_rejected():
    m = _load()
    value = _observation(m)
    value["tags_url"] = "http://127.0.0.1:11434/wrong"
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "tags URL drift",
        lambda: _validate(m, value),
    )


def test_ps_url_drift_rejected():
    m = _load()
    value = _observation(m)
    value["ps_url"] = "http://127.0.0.1:11434/wrong"
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "ps URL drift",
        lambda: _validate(m, value),
    )


def test_chat_completions_request_claim_rejected():
    m = _load()
    value = _observation(m)
    value["chat_completions_request_performed"] = True
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "chat-completions request performed",
        lambda: _validate(m, value),
    )


def test_endpoint_liveness_false_rejected():
    m = _load()
    value = _observation(m)
    value["endpoint_liveness_observed"] = False
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "endpoint liveness not observed",
        lambda: _validate(m, value),
    )


def test_catalog_alias_drift_rejected():
    m = _load()
    value = _observation(m)
    value["catalog_model_alias"] = "wrong"
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "catalog model alias drift",
        lambda: _validate(m, value),
    )


def test_catalog_digest_drift_rejected():
    m = _load()
    value = _observation(m)
    value["catalog_model_digest"] = "0" * 64
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "catalog model digest drift",
        lambda: _validate(m, value),
    )


def test_running_alias_drift_rejected():
    m = _load()
    value = _observation(m)
    value["running_model_alias"] = "wrong"
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "running model alias drift",
        lambda: _validate(m, value),
    )


def test_running_digest_drift_rejected():
    m = _load()
    value = _observation(m)
    value["running_model_digest"] = "0" * 64
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "running model digest drift",
        lambda: _validate(m, value),
    )


def test_catalog_identity_false_rejected():
    m = _load()
    value = _observation(m)
    value["model_catalog_identity_matches_expected"] = False
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "catalog identity mismatch",
        lambda: _validate(m, value),
    )


def test_running_identity_false_rejected():
    m = _load()
    value = _observation(m)
    value["running_model_identity_matches_expected"] = False
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "running identity mismatch",
        lambda: _validate(m, value),
    )


def test_model_identity_observation_false_rejected():
    m = _load()
    value = _observation(m)
    value["model_identity_observation_performed"] = False
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "model identity observation missing",
        lambda: _validate(m, value),
    )


def test_ollama_runtime_image_observation_claim_rejected():
    m = _load()
    value = _observation(m)
    value["runtime_image_identity_observation_performed"] = True
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "crossed into runtime-image observation",
        lambda: _validate(m, value),
    )


def test_ollama_runtime_image_id_claim_rejected():
    m = _load()
    value = _observation(m)
    value["runtime_image_id"] = m.activation_contract.V2R13_RUNTIME_IMAGE_ID
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "unexpectedly reports runtime-image ID",
        lambda: _validate(m, value),
    )


def test_mutation_claim_rejected():
    m = _load()
    value = _observation(m)
    value["mutation_performed"] = True
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "mutation_performed",
        lambda: _validate(m, value),
    )


def test_model_inference_claim_rejected():
    m = _load()
    value = _observation(m)
    value["model_inference_performed"] = True
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "model_inference_performed",
        lambda: _validate(m, value),
    )


def test_game_execution_claim_rejected():
    m = _load()
    value = _observation(m)
    value["game_execution_performed"] = True
    _expect_hold(
        m.RuntimeV2R13OllamaObserverBindingHold,
        "game_execution_performed",
        lambda: _validate(m, value),
    )


def test_observer_dependency_drift_fails_closed():
    m = _load()
    original = m.ollama_observer.v2r13_ollama_readonly_observer_contract
    baseline = original()

    def drifted():
        value = copy.deepcopy(baseline)
        value["chat_completions_forbidden"] = False
        return value

    m.ollama_observer.v2r13_ollama_readonly_observer_contract = drifted
    try:
        _expect_hold(
            m.RuntimeV2R13OllamaObserverBindingHold,
            "chat-completions prohibition lost",
            lambda: m.v2r13_ollama_observer_binding_contract(),
        )
    finally:
        m.ollama_observer.v2r13_ollama_readonly_observer_contract = original


def test_runtime_image_binding_dependency_drift_fails_closed():
    m = _load()
    original = (
        m.runtime_image_binding.v2r13_rootless_docker_image_backend_binding_contract
    )
    baseline = original()

    def drifted():
        value = copy.deepcopy(baseline)
        value["supported_primitive_count_after_binding"] = 13
        return value

    m.runtime_image_binding.v2r13_rootless_docker_image_backend_binding_contract = drifted
    try:
        _expect_hold(
            m.RuntimeV2R13OllamaObserverBindingHold,
            "post-image-binding supported count drift",
            lambda: m.v2r13_ollama_observer_binding_contract(),
        )
    finally:
        m.runtime_image_binding.v2r13_rootless_docker_image_backend_binding_contract = original


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
        "ollama_observer.host_http_get",
        "ollama_observer.observe_v2r13_ollama_readonly",
    )
    assert not any(
        call.startswith(prefix)
        for call in calls
        for prefix in forbidden_call_prefixes
    )
