from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_v2r13_ollama_readonly_observer_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_ollama_readonly_observer_generation2.py"
)

EXPECTED_SOURCE_SHA256 = "c770d08621ff1d32996e64962bd539c783bd4ba5c259687d1a348a2db775a7ff"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_v2r13_ollama_readonly_observer",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _json_result(m, value, status=200):
    return m.HttpGetResult(
        status=status,
        body=json.dumps(value, sort_keys=True).encode("utf-8"),
        content_type="application/json",
    )


def _model_row(m):
    return {
        "name": m.activation_contract.V2R13_MODEL_ALIAS,
        "model": m.activation_contract.V2R13_MODEL_ALIAS,
        "digest": m.activation_contract.V2R13_MODEL_DIGEST,
        "size": 123,
    }


class FakeBackend:
    def __init__(self, m, *, tags=None, ps=None, tags_status=200, ps_status=200):
        self.m = m
        self.calls = []
        self.tags = tags if tags is not None else {"models": [_model_row(m)]}
        self.ps = ps if ps is not None else {"models": [_model_row(m)]}
        self.tags_status = tags_status
        self.ps_status = ps_status

    def __call__(self, url, *, timeout_seconds, maximum_bytes):
        self.calls.append((url, timeout_seconds, maximum_bytes))
        if url == self.m.OLLAMA_TAGS_URL:
            return _json_result(self.m, self.tags, self.tags_status)
        if url == self.m.OLLAMA_PS_URL:
            return _json_result(self.m, self.ps, self.ps_status)
        raise AssertionError(f"unexpected URL: {url}")


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


def test_contract_binds_exact_semantic_contract():
    m = _load()
    out = m.v2r13_ollama_readonly_observer_contract()
    assert out["live_identity_collector_contract_git_blob"] == (
        "db9fbb58f3d5870c77a796641afb1014acc19ee4"
    )
    assert out["live_identity_collector_semantic_sha256"] == (
        "0bda63a4d82be7f38e604c15fe63f659051cc42527bc9281317df167f6145219"
    )
    assert out["semantic_contract_valid"] is True


def test_contract_routes_are_exact_get_only_nonchat():
    m = _load()
    out = m.v2r13_ollama_readonly_observer_contract()
    assert out["tags_route"] == "/api/tags"
    assert out["ps_route"] == "/api/ps"
    assert out["tags_method"] == "GET"
    assert out["ps_method"] == "GET"
    assert out["chat_completions_route"] == "/v1/chat/completions"
    assert out["chat_completions_forbidden"] is True


def test_contract_candidate_mechanics_do_not_advance_frontier():
    m = _load()
    out = m.v2r13_ollama_readonly_observer_contract()
    assert out["endpoint_liveness_observer_candidate_implemented"] is True
    assert out["running_model_identity_observer_candidate_implemented"] is True
    assert out["runtime_image_identity_observer_implemented"] is False
    assert out["candidate_observation_does_not_admit_collector_identity"] is True
    assert out["candidate_observation_does_not_advance_primitive_frontier"] is True
    assert out["supported_primitive_count_remains"] == 13
    assert out["remaining_unresolved_primitive_count_remains"] == 3


def test_contract_requires_authority_and_no_auto_backend():
    m = _load()
    out = m.v2r13_ollama_readonly_observer_contract()
    assert out["host_http_backend_factory_present"] is True
    assert out["automatic_host_backend_selection"] is False
    assert out["observation_requires_explicit_authority"] is True


def test_contract_keeps_execution_boundaries_closed():
    m = _load()
    out = m.v2r13_ollama_readonly_observer_contract()
    for field in (
        "service_action_implemented",
        "runtime_start_stop_reload_implemented",
        "model_load_implemented",
        "model_inference_implemented",
        "runtime_readiness_admitted",
        "runtime_execution_authorized",
    ):
        assert out[field] is False


def test_observation_requires_explicit_authority():
    m = _load()
    backend = FakeBackend(m)
    _expect_hold(
        m.RuntimeV2R13OllamaObserverHold,
        "OBSERVATION_NOT_AUTHORIZED",
        lambda: m.observe_v2r13_ollama_readonly(
            observation_authorized=False,
            http_get=backend,
        ),
    )
    assert backend.calls == []


def test_valid_fake_observation_uses_exact_two_get_routes():
    m = _load()
    backend = FakeBackend(m)
    out = m.observe_v2r13_ollama_readonly(
        observation_authorized=True,
        http_get=backend,
    )
    assert [call[0] for call in backend.calls] == [
        m.OLLAMA_TAGS_URL,
        m.OLLAMA_PS_URL,
    ]
    assert all(call[1] == m.DEFAULT_TIMEOUT_SECONDS for call in backend.calls)
    assert all(call[2] == m.MAX_RESPONSE_BYTES for call in backend.calls)
    assert out["endpoint_liveness_observed"] is True


def test_valid_fake_observation_matches_expected_model_identity():
    m = _load()
    out = m.observe_v2r13_ollama_readonly(
        observation_authorized=True,
        http_get=FakeBackend(m),
    )
    assert out["catalog_model_alias"] == m.activation_contract.V2R13_MODEL_ALIAS
    assert out["catalog_model_digest"] == m.activation_contract.V2R13_MODEL_DIGEST
    assert out["running_model_alias"] == m.activation_contract.V2R13_MODEL_ALIAS
    assert out["running_model_digest"] == m.activation_contract.V2R13_MODEL_DIGEST
    assert out["model_catalog_identity_matches_expected"] is True
    assert out["running_model_identity_matches_expected"] is True


def test_valid_fake_observation_never_claims_runtime_image_identity():
    m = _load()
    out = m.observe_v2r13_ollama_readonly(
        observation_authorized=True,
        http_get=FakeBackend(m),
    )
    assert out["runtime_image_identity_observation_performed"] is False
    assert out["runtime_image_id"] is None
    assert out["runtime_image_identity_verified"] is False


def test_valid_fake_observation_reports_no_chat_or_inference():
    m = _load()
    out = m.observe_v2r13_ollama_readonly(
        observation_authorized=True,
        http_get=FakeBackend(m),
    )
    assert out["chat_completions_url"] == m.FORBIDDEN_CHAT_COMPLETIONS_URL
    assert out["chat_completions_request_performed"] is False
    assert out["model_inference_performed"] is False
    assert out["model_load_performed"] is False


def test_valid_fake_observation_admits_nothing():
    m = _load()
    out = m.observe_v2r13_ollama_readonly(
        observation_authorized=True,
        http_get=FakeBackend(m),
    )
    assert out["collector_identity_admitted"] is False
    assert out["canonical_provider_binding_present"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_valid_fake_observation_reports_no_service_or_runtime_actions():
    m = _load()
    out = m.observe_v2r13_ollama_readonly(
        observation_authorized=True,
        http_get=FakeBackend(m),
    )
    for field in (
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "runtime_stop_performed",
        "runtime_reload_performed",
        "game_execution_performed",
    ):
        assert out[field] is False


def test_tags_http_failure_is_rejected():
    m = _load()
    backend = FakeBackend(m, tags_status=503)
    _expect_hold(
        m.RuntimeV2R13OllamaObserverHold,
        "TAGS: HTTP status drift",
        lambda: m.observe_v2r13_ollama_readonly(
            observation_authorized=True,
            http_get=backend,
        ),
    )


def test_ps_http_failure_is_rejected():
    m = _load()
    backend = FakeBackend(m, ps_status=503)
    _expect_hold(
        m.RuntimeV2R13OllamaObserverHold,
        "PS: HTTP status drift",
        lambda: m.observe_v2r13_ollama_readonly(
            observation_authorized=True,
            http_get=backend,
        ),
    )


def test_tags_missing_models_is_rejected():
    m = _load()
    backend = FakeBackend(m, tags={})
    _expect_hold(
        m.RuntimeV2R13OllamaObserverHold,
        "TAGS: models must be list",
        lambda: m.observe_v2r13_ollama_readonly(
            observation_authorized=True,
            http_get=backend,
        ),
    )


def test_ps_missing_models_is_rejected():
    m = _load()
    backend = FakeBackend(m, ps={})
    _expect_hold(
        m.RuntimeV2R13OllamaObserverHold,
        "PS: models must be list",
        lambda: m.observe_v2r13_ollama_readonly(
            observation_authorized=True,
            http_get=backend,
        ),
    )


def test_tags_missing_expected_alias_is_rejected():
    m = _load()
    backend = FakeBackend(
        m,
        tags={"models": [{"name": "other:latest", "model": "other:latest", "digest": "0" * 64}]},
    )
    _expect_hold(
        m.RuntimeV2R13OllamaObserverHold,
        "TAGS: exact model alias match count drift",
        lambda: m.observe_v2r13_ollama_readonly(
            observation_authorized=True,
            http_get=backend,
        ),
    )


def test_ps_missing_expected_alias_is_rejected():
    m = _load()
    backend = FakeBackend(
        m,
        ps={"models": [{"name": "other:latest", "model": "other:latest", "digest": "0" * 64}]},
    )
    _expect_hold(
        m.RuntimeV2R13OllamaObserverHold,
        "PS: exact model alias match count drift",
        lambda: m.observe_v2r13_ollama_readonly(
            observation_authorized=True,
            http_get=backend,
        ),
    )


def test_tags_digest_drift_is_rejected():
    m = _load()
    bad = _model_row(m)
    bad["digest"] = "0" * 64
    backend = FakeBackend(m, tags={"models": [bad]})
    _expect_hold(
        m.RuntimeV2R13OllamaObserverHold,
        "TAGS: exact model digest drift",
        lambda: m.observe_v2r13_ollama_readonly(
            observation_authorized=True,
            http_get=backend,
        ),
    )


def test_ps_digest_drift_is_rejected():
    m = _load()
    bad = _model_row(m)
    bad["digest"] = "0" * 64
    backend = FakeBackend(m, ps={"models": [bad]})
    _expect_hold(
        m.RuntimeV2R13OllamaObserverHold,
        "PS: exact model digest drift",
        lambda: m.observe_v2r13_ollama_readonly(
            observation_authorized=True,
            http_get=backend,
        ),
    )


def test_duplicate_expected_alias_is_rejected():
    m = _load()
    row = _model_row(m)
    backend = FakeBackend(m, tags={"models": [row, dict(row)]})
    _expect_hold(
        m.RuntimeV2R13OllamaObserverHold,
        "TAGS: exact model alias match count drift",
        lambda: m.observe_v2r13_ollama_readonly(
            observation_authorized=True,
            http_get=backend,
        ),
    )


def test_host_backend_rejects_unreviewed_url_before_network():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13OllamaObserverHold,
        "HOST_BACKEND_URL_NOT_REVIEWED",
        lambda: m.host_http_get(
            "http://127.0.0.1:11434/v1/chat/completions",
            timeout_seconds=1.0,
            maximum_bytes=1024,
        ),
    )


def test_host_backend_rejects_excessive_timeout_before_network():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13OllamaObserverHold,
        "timeout_seconds outside reviewed bound",
        lambda: m.host_http_get(
            m.OLLAMA_TAGS_URL,
            timeout_seconds=11.0,
            maximum_bytes=1024,
        ),
    )


def test_host_backend_rejects_excessive_byte_bound_before_network():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13OllamaObserverHold,
        "maximum_bytes outside reviewed bound",
        lambda: m.host_http_get(
            m.OLLAMA_TAGS_URL,
            timeout_seconds=1.0,
            maximum_bytes=m.MAX_RESPONSE_BYTES + 1,
        ),
    )


def test_static_source_has_no_chat_completion_invocation():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    forbidden_strings = [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and "/v1/chat/completions" in node.value
    ]
    assert forbidden_strings
    calls = [_dotted(node.func) for node in ast.walk(tree) if isinstance(node, ast.Call)]
    assert "urllib.request.urlopen" in calls
    assert "observe_v2r13_ollama_readonly" not in calls


def test_import_does_not_perform_network_observation():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    top_level_calls = []
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            top_level_calls.append(_dotted(node.value.func))
    assert "urllib.request.urlopen" not in top_level_calls
    assert "observe_v2r13_ollama_readonly" not in top_level_calls
