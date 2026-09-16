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
    "abaddon_policy_campaign_runtime_v2r13_live_collection_backend_binding_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_live_collection_backend_binding_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "9899e2024f7233aab72b05465ee9d89dfcdea059eacde18e9f5573300110f119"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    repo = "/home/zoso/dev/openra-rl-war-college"
    if repo not in sys.path:
        sys.path.insert(0, repo)
    spec = importlib.util.spec_from_file_location(
        "_void_g2_v2r13_live_collection_backend_binding",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _expect_hold(exc_type, pattern, fn):
    try:
        fn()
    except exc_type as exc:
        assert pattern in str(exc), (pattern, str(exc))
    else:
        raise AssertionError(f"expected {exc_type.__name__}: {pattern}")


def _fake_http_backend(m):
    def http_get(url, *, timeout_seconds, maximum_bytes):
        assert timeout_seconds == m.live_backend.ollama_observer.DEFAULT_TIMEOUT_SECONDS
        assert maximum_bytes == m.live_backend.ollama_observer.MAX_RESPONSE_BYTES
        assert url in {
            m.live_backend.ollama_observer.OLLAMA_TAGS_URL,
            m.live_backend.ollama_observer.OLLAMA_PS_URL,
        }
        body = json.dumps(
            {
                "models": [
                    {
                        "name": m.live_backend.ollama_observer.activation_contract.V2R13_MODEL_ALIAS,
                        "model": m.live_backend.ollama_observer.activation_contract.V2R13_MODEL_ALIAS,
                        "digest": m.live_backend.ollama_observer.activation_contract.V2R13_MODEL_DIGEST,
                    }
                ]
            },
            sort_keys=True,
        ).encode("utf-8")
        return m.live_backend.ollama_observer.HttpGetResult(
            status=200,
            body=body,
            content_type="application/json",
        )

    return http_get


def _fake_docker_backend(m):
    def run_command(args):
        command = tuple(args)
        backend = m.live_backend.docker_backend
        if command == backend.CONTEXT_COMMAND:
            value = [
                {
                    "Name": backend.CONTEXT_NAME,
                    "Endpoints": {
                        "docker": {
                            "Host": backend.EXPECTED_CONTEXT_HOST,
                            "SkipTLSVerify": False,
                        }
                    },
                }
            ]
        elif command == backend.INFO_COMMAND:
            value = {
                "SecurityOptions": ["name=rootless"],
                "DockerRootDir": backend.EXPECTED_DOCKER_ROOT_DIR,
                "OSType": "linux",
            }
        elif command == backend.IMAGE_INSPECT_COMMAND:
            value = [
                {
                    "Id": backend.activation_contract.V2R13_RUNTIME_IMAGE_ID,
                    "RepoTags": [backend.EXPECTED_IMAGE_TAG],
                    "RepoDigests": [backend.EXPECTED_IMAGE_REPO_DIGEST],
                    "Config": {
                        "Labels": {
                            "void.openra.generation": backend.EXPECTED_GENERATION_LABEL,
                            "void.openra.purpose": backend.EXPECTED_PURPOSE_LABEL,
                        },
                        "WorkingDir": backend.EXPECTED_WORKING_DIR,
                        "Entrypoint": list(backend.EXPECTED_ENTRYPOINT_PREFIX),
                    },
                }
            ]
        else:
            raise AssertionError(f"unexpected Docker command: {command!r}")
        return {
            "returncode": 0,
            "stdout": json.dumps(value, sort_keys=True),
            "stderr": "",
        }

    return run_command


def _candidate(m):
    return m.live_backend.collect_v2r13_live_identity_candidate(
        observation_authorized=True,
        http_get=_fake_http_backend(m),
        run_command=_fake_docker_backend(m),
    )


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def test_source_sha_is_exact():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SOURCE_SHA256


def test_contract_schema_and_snapshot_are_exact():
    m = _load()
    out = m.v2r13_live_collection_backend_binding_contract()
    assert out["schema"] == (
        "void.abaddon.generation2.v2r13-live-collection-backend-binding-contract.v1"
    )
    assert out["snapshot_id"] == m.V2R13


def test_backend_identity_is_pinned_exactly():
    m = _load()
    out = m.v2r13_live_collection_backend_binding_contract()
    assert out["live_collection_backend_git_blob"] == (
        "ee78726c7538aeb985ef00140d58792ec75fdcf3"
    )
    assert out["live_collection_backend_source_sha256"] == (
        "1f8dacce44d355f2948359ff59c29b79d50c68e21a648814689ba6a85cce2c94"
    )


def test_binding_is_separate_and_non_self_referential():
    m = _load()
    out = m.v2r13_live_collection_backend_binding_contract()
    assert out["separate_binding_instrument"] is True
    assert out["backend_source_identity_pinned_by_git_blob"] is True
    assert out["backend_source_identity_pinned_by_sha256"] is True
    assert out["backend_source_is_not_self_bound"] is True


def test_dependency_backend_remains_explicit_authority_only():
    m = _load()
    out = m.v2r13_live_collection_backend_binding_contract()
    dep = out["dependency_contracts"]["live_collection_backend"]
    assert dep["live_collection_backend_requires_explicit_authority"] is True
    assert dep["explicit_http_backend_injection_required"] is True
    assert dep["explicit_docker_command_backend_injection_required"] is True
    assert dep["automatic_host_backend_selection"] is False


def test_provider_frontier_remains_16_of_16():
    m = _load()
    out = m.v2r13_live_collection_backend_binding_contract()
    assert out["provider_capability_supported_primitive_count"] == 16
    assert out["provider_capability_remaining_unresolved_primitive_count"] == 0
    assert out["provider_capability_complete"] is True


def test_source_sha_mismatch_is_rejected():
    m = _load()
    candidate = _candidate(m)
    _expect_hold(
        m.RuntimeV2R13LiveCollectionBackendBindingHold,
        "source SHA mismatch",
        lambda: m.validate_bound_live_collection_candidate(
            candidate,
            backend_source_sha256="0" * 64,
        ),
    )


def test_exact_fake_candidate_is_admitted_by_binding():
    m = _load()
    result = m.validate_bound_live_collection_candidate(
        _candidate(m),
        backend_source_sha256=m.LIVE_COLLECTION_BACKEND_SOURCE_SHA256,
    )
    assert result["bound_live_collection_candidate_valid"] is True
    assert result["supplied_live_observation_validated"] is True


def test_bound_validation_marks_source_binding_present():
    m = _load()
    result = m.validate_bound_live_collection_candidate(
        _candidate(m),
        backend_source_sha256=m.LIVE_COLLECTION_BACKEND_SOURCE_SHA256,
    )
    assert result["canonical_live_collection_backend_source_binding_present"] is True


def test_binding_does_not_claim_live_observation_itself():
    m = _load()
    result = m.validate_bound_live_collection_candidate(
        _candidate(m),
        backend_source_sha256=m.LIVE_COLLECTION_BACKEND_SOURCE_SHA256,
    )
    assert result["supplied_live_observation_performed"] is True
    assert result["binding_live_observation_performed"] is False
    assert result["binding_http_request_performed"] is False
    assert result["binding_ollama_request_performed"] is False
    assert result["binding_docker_command_performed"] is False


def test_canonical_collection_remains_closed_after_source_binding():
    m = _load()
    out = m.v2r13_live_collection_backend_binding_contract()
    assert out["canonical_live_collection_backend_source_binding_present"] is True
    assert out["canonical_live_collection_path_complete"] is False
    assert out["canonical_collection_enabled"] is False


def test_bound_candidate_does_not_admit_identity_readiness_or_execution():
    m = _load()
    result = m.validate_bound_live_collection_candidate(
        _candidate(m),
        backend_source_sha256=m.LIVE_COLLECTION_BACKEND_SOURCE_SHA256,
    )
    assert result["collector_identity_admitted"] is False
    assert result["runtime_readiness_admitted"] is False
    assert result["runtime_execution_authorized"] is False


def test_primitive_receipts_use_exact_reviewed_source_bindings():
    m = _load()
    result = m.validate_bound_live_collection_candidate(
        _candidate(m),
        backend_source_sha256=m.LIVE_COLLECTION_BACKEND_SOURCE_SHA256,
    )
    bindings = m.collector_binding.reviewed_v2r13_primitive_source_bindings()
    for name, receipt in result["validated_primitive_receipts"].items():
        assert receipt["source_sha256"] == bindings[name]
        assert receipt["value"] is True


def test_tampered_primitive_receipt_is_rejected():
    m = _load()
    candidate = deepcopy(_candidate(m))
    candidate["primitive_receipts"]["endpoint_liveness"]["source_sha256"] = "0" * 64
    _expect_hold(
        m.RuntimeV2R13LiveCollectionBackendBindingHold,
        "source binding mismatch",
        lambda: m.validate_bound_live_collection_candidate(
            candidate,
            backend_source_sha256=m.LIVE_COLLECTION_BACKEND_SOURCE_SHA256,
        ),
    )


def test_tampered_action_boolean_is_rejected():
    m = _load()
    candidate = deepcopy(_candidate(m))
    candidate["model_inference_performed"] = True
    _expect_hold(
        m.RuntimeV2R13LiveCollectionBackendBindingHold,
        "crossed boundary: model_inference_performed",
        lambda: m.validate_bound_live_collection_candidate(
            candidate,
            backend_source_sha256=m.LIVE_COLLECTION_BACKEND_SOURCE_SHA256,
        ),
    )


def test_tampered_hold_set_is_rejected():
    m = _load()
    candidate = deepcopy(_candidate(m))
    candidate["holds"] = []
    _expect_hold(
        m.RuntimeV2R13LiveCollectionBackendBindingHold,
        "hold set drift",
        lambda: m.validate_bound_live_collection_candidate(
            candidate,
            backend_source_sha256=m.LIVE_COLLECTION_BACKEND_SOURCE_SHA256,
        ),
    )


def test_tampered_field_set_is_rejected():
    m = _load()
    candidate = deepcopy(_candidate(m))
    candidate["unexpected"] = True
    _expect_hold(
        m.RuntimeV2R13LiveCollectionBackendBindingHold,
        "field-set drift",
        lambda: m.validate_bound_live_collection_candidate(
            candidate,
            backend_source_sha256=m.LIVE_COLLECTION_BACKEND_SOURCE_SHA256,
        ),
    )


def test_automatic_host_backend_selection_remains_false():
    m = _load()
    out = m.v2r13_live_collection_backend_binding_contract()
    assert out["automatic_host_backend_selection"] is False


def test_binding_source_has_no_direct_host_io_imports():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    forbidden = {
        "os", "subprocess", "pathlib", "socket", "urllib", "http",
        "requests", "httpx", "docker", "asyncio", "multiprocessing", "ctypes",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden


def test_binding_never_invokes_live_backend_collector():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    forbidden = {
        "live_backend.collect_v2r13_live_identity_candidate",
        "live_backend.ollama_observer.host_http_get",
        "live_backend.docker_backend.host_readonly_command_runner",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            assert _dotted(node.func) not in forbidden


def test_next_gate_is_canonical_adapter():
    m = _load()
    out = m.v2r13_live_collection_backend_binding_contract()
    assert out["next_gate"] == "V2R13_CANONICAL_LIVE_COLLECTION_ADAPTER_REQUIRED"
    assert out["next_change_class"] == (
        "explicit_authority_canonical_live_collection_adapter"
    )


def test_collect_bound_live_identity_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13LiveCollectionBackendBindingHold,
        "BOUND_LIVE_COLLECTION_ADAPTER_NOT_IMPLEMENTED",
        lambda: m.collect_bound_live_identity(),
    )


def test_enable_canonical_live_collection_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13LiveCollectionBackendBindingHold,
        "V2R13_CANONICAL_LIVE_COLLECTION_ADAPTER_REQUIRED",
        lambda: m.enable_canonical_live_collection(),
    )


def test_authorize_runtime_execution_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13LiveCollectionBackendBindingHold,
        "LIVE_COLLECTION_ADAPTER_AND_RUNTIME_ACTIVATION_GAPS_REMAIN",
        lambda: m.authorize_runtime_execution(),
    )
