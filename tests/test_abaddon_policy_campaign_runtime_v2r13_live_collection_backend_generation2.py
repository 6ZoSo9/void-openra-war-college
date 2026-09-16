from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_v2r13_live_collection_backend_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_live_collection_backend_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "fe41c893b95ad80035c6d9f25798555fa5b6ec24421424384569a338660843e2"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    repo = "/home/zoso/dev/openra-rl-war-college"
    if repo not in sys.path:
        sys.path.insert(0, repo)
    spec = importlib.util.spec_from_file_location(
        "_void_g2_v2r13_live_collection_backend",
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


def _fake_http_backend(m, *, bad_digest=False):
    calls = []

    def http_get(url, *, timeout_seconds, maximum_bytes):
        calls.append(url)
        assert timeout_seconds == m.ollama_observer.DEFAULT_TIMEOUT_SECONDS
        assert maximum_bytes == m.ollama_observer.MAX_RESPONSE_BYTES
        digest = (
            "0" * 64
            if bad_digest
            else m.ollama_observer.activation_contract.V2R13_MODEL_DIGEST
        )
        body = json.dumps(
            {
                "models": [
                    {
                        "name": m.ollama_observer.activation_contract.V2R13_MODEL_ALIAS,
                        "model": m.ollama_observer.activation_contract.V2R13_MODEL_ALIAS,
                        "digest": digest,
                    }
                ]
            },
            sort_keys=True,
        ).encode("utf-8")
        return m.ollama_observer.HttpGetResult(
            status=200,
            body=body,
            content_type="application/json",
        )

    return http_get, calls


def _fake_docker_backend(m, *, bad_image=False):
    calls = []

    def run_command(args):
        command = tuple(args)
        calls.append(command)
        if command == m.docker_backend.CONTEXT_COMMAND:
            value = [
                {
                    "Name": m.docker_backend.CONTEXT_NAME,
                    "Endpoints": {
                        "docker": {
                            "Host": m.docker_backend.EXPECTED_CONTEXT_HOST,
                            "SkipTLSVerify": False,
                        }
                    },
                }
            ]
        elif command == m.docker_backend.INFO_COMMAND:
            value = {
                "SecurityOptions": ["name=rootless"],
                "DockerRootDir": m.docker_backend.EXPECTED_DOCKER_ROOT_DIR,
                "OSType": "linux",
            }
        elif command == m.docker_backend.IMAGE_INSPECT_COMMAND:
            image_id = (
                "sha256:" + "0" * 64
                if bad_image
                else m.docker_backend.activation_contract.V2R13_RUNTIME_IMAGE_ID
            )
            value = [
                {
                    "Id": image_id,
                    "RepoTags": [m.docker_backend.EXPECTED_IMAGE_TAG],
                    "RepoDigests": [m.docker_backend.EXPECTED_IMAGE_REPO_DIGEST],
                    "Config": {
                        "Labels": {
                            "void.openra.generation": (
                                m.docker_backend.EXPECTED_GENERATION_LABEL
                            ),
                            "void.openra.purpose": (
                                m.docker_backend.EXPECTED_PURPOSE_LABEL
                            ),
                        },
                        "WorkingDir": m.docker_backend.EXPECTED_WORKING_DIR,
                        "Entrypoint": list(
                            m.docker_backend.EXPECTED_ENTRYPOINT_PREFIX
                        ),
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

    return run_command, calls


def _collect(m):
    http_get, http_calls = _fake_http_backend(m)
    run_command, docker_calls = _fake_docker_backend(m)
    result = m.collect_v2r13_live_identity_candidate(
        observation_authorized=True,
        http_get=http_get,
        run_command=run_command,
    )
    return result, http_calls, docker_calls


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
    out = m.v2r13_live_collection_backend_contract()
    assert out["schema"] == (
        "void.abaddon.generation2.v2r13-live-collection-backend-contract.v1"
    )
    assert out["snapshot_id"] == m.V2R13


def test_post117_reconciliation_gate_is_exact():
    m = _load()
    out = m.v2r13_live_collection_backend_contract()
    dep = out["dependency_contracts"]["post_admission_reconciliation"]
    assert dep["next_gate"] == "V2R13_LIVE_COLLECTION_BACKEND_IMPLEMENTATION_REQUIRED"
    assert dep["canonical_live_collection_path_complete"] is False


def test_live_backend_implementation_is_present_but_not_canonical():
    m = _load()
    out = m.v2r13_live_collection_backend_contract()
    assert out["live_collection_backend_implementation_present"] is True
    assert out["live_collection_backend_composition_implemented"] is True
    assert out["live_collection_backend_source_binding_present"] is False
    assert out["canonical_live_collection_path_complete"] is False
    assert out["canonical_collection_enabled"] is False


def test_explicit_authority_and_backend_injection_are_required():
    m = _load()
    out = m.v2r13_live_collection_backend_contract()
    assert out["live_collection_backend_requires_explicit_authority"] is True
    assert out["explicit_http_backend_injection_required"] is True
    assert out["explicit_docker_command_backend_injection_required"] is True
    assert out["automatic_host_backend_selection"] is False


def test_ollama_observer_source_identity_is_exact():
    m = _load()
    out = m.v2r13_live_collection_backend_contract()
    assert out["ollama_observer_git_blob"] == "9b859e91b8833260a1af7e189ec5cd30d92d9451"
    assert out["ollama_observer_source_sha256"] == (
        "c770d08621ff1d32996e64962bd539c783bd4ba5c259687d1a348a2db775a7ff"
    )


def test_rootless_docker_backend_source_identity_is_exact():
    m = _load()
    out = m.v2r13_live_collection_backend_contract()
    assert out["rootless_docker_backend_git_blob"] == (
        "488497f723ad5bc5ca63b3b2d69cece26bddaaa5"
    )
    assert out["rootless_docker_backend_source_sha256"] == (
        "25e8f41dcea700860ec1b97726b321a99c2622e00ddba12433246c7b121b11f6"
    )


def test_final_three_collector_source_bindings_are_exact():
    m = _load()
    bindings = m.collector_binding.reviewed_v2r13_primitive_source_bindings()
    assert bindings["endpoint_liveness"] == m.OLLAMA_BINDING_SOURCE_SHA256
    assert bindings["model_identity_verified"] == m.OLLAMA_BINDING_SOURCE_SHA256
    assert (
        bindings["runtime_image_identity_verified"]
        == m.ROOTLESS_DOCKER_BINDING_SOURCE_SHA256
    )


def test_unauthorized_collection_holds_before_backend_invocation():
    m = _load()
    calls = []

    def bomb(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError("backend must not be invoked")

    _expect_hold(
        m.RuntimeV2R13LiveCollectionBackendHold,
        "GENERATION2_V2R13_LIVE_COLLECTION_NOT_AUTHORIZED",
        lambda: m.collect_v2r13_live_identity_candidate(
            observation_authorized=False,
            http_get=bomb,
            run_command=bomb,
        ),
    )
    assert calls == []


def test_missing_http_backend_holds_without_docker_invocation():
    m = _load()
    docker_calls = []

    def docker_bomb(*args, **kwargs):
        docker_calls.append((args, kwargs))
        raise AssertionError("Docker backend must not be invoked")

    _expect_hold(
        m.RuntimeV2R13LiveCollectionBackendHold,
        "explicit V2R13 HTTP GET backend required",
        lambda: m.collect_v2r13_live_identity_candidate(
            observation_authorized=True,
            http_get=None,
            run_command=docker_bomb,
        ),
    )
    assert docker_calls == []


def test_fake_collection_verifies_exact_three_live_primitives():
    m = _load()
    result, _, _ = _collect(m)
    assert result["primitive_values"] == {
        "endpoint_liveness": True,
        "model_identity_verified": True,
        "runtime_image_identity_verified": True,
    }
    assert result["live_primitive_count"] == 3


def test_fake_collection_reaches_16_of_16_provider_capability():
    m = _load()
    result, _, _ = _collect(m)
    assert result["provider_capability_supported_primitive_count"] == 16
    assert result["provider_capability_remaining_unresolved_primitive_count"] == 0
    assert result["provider_capability_complete"] is True


def test_fake_collection_uses_only_two_reviewed_ollama_get_routes():
    m = _load()
    _, calls, _ = _collect(m)
    assert calls == [
        m.ollama_observer.OLLAMA_TAGS_URL,
        m.ollama_observer.OLLAMA_PS_URL,
    ]
    assert m.ollama_observer.FORBIDDEN_CHAT_COMPLETIONS_URL not in calls


def test_fake_collection_uses_only_three_reviewed_docker_metadata_commands():
    m = _load()
    result, _, calls = _collect(m)
    assert calls == [
        m.docker_backend.CONTEXT_COMMAND,
        m.docker_backend.INFO_COMMAND,
        m.docker_backend.IMAGE_INSPECT_COMMAND,
    ]
    assert set(result["runtime_image_receipt"]) == set(
        m.docker_binding.runtime_image_interface.BACKEND_RECEIPT_FIELDS
    )
    assert "_candidate_metadata" not in result["runtime_image_receipt"]
    assert result["runtime_image_candidate_metadata"]["rootless_security"] is True


def test_fake_collection_reports_no_mutation_or_execution_actions():
    m = _load()
    result, _, _ = _collect(m)
    for field in (
        "docker_mutating_command_performed",
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "runtime_stop_performed",
        "runtime_reload_performed",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "policy_promotion_performed",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        assert result[field] is False


def test_primitive_receipts_match_collector_receipt_schema_and_bindings():
    m = _load()
    result, _, _ = _collect(m)
    receipts = result["primitive_receipts"]
    assert set(receipts) == set(m.LIVE_PRIMITIVES)
    for name, receipt in receipts.items():
        assert receipt["schema"] == m.collector_implementation.PRIMITIVE_RECEIPT_SCHEMA
        assert receipt["snapshot_id"] == m.V2R13
        assert receipt["primitive_name"] == name
        assert receipt["observation_mode"] == "read_only"
        assert receipt["value"] is True
        if name in {"endpoint_liveness", "model_identity_verified"}:
            assert receipt["source_sha256"] == m.OLLAMA_BINDING_SOURCE_SHA256
        else:
            assert receipt["source_sha256"] == m.ROOTLESS_DOCKER_BINDING_SOURCE_SHA256


def test_collection_candidate_does_not_self_admit_or_enable_canonical_collection():
    m = _load()
    result, _, _ = _collect(m)
    assert result["live_collection_backend_source_binding_present"] is False
    assert result["canonical_live_collection_path_complete"] is False
    assert result["canonical_collection_enabled"] is False
    assert result["collector_identity_admitted_by_backend"] is False
    assert result["runtime_readiness_admitted_by_backend"] is False
    assert result["runtime_execution_authorized"] is False


def test_collection_candidate_holds_are_exact():
    m = _load()
    result, _, _ = _collect(m)
    assert result["holds"] == [
        "V2R13_LIVE_COLLECTION_BACKEND_SOURCE_BINDING_REQUIRED",
        "V2R13_CANONICAL_COLLECTION_NOT_ENABLED",
        m.RUNTIME_AUTHORITY_BLOCKER,
    ]


def test_bad_ollama_digest_is_rejected():
    m = _load()
    http_get, _ = _fake_http_backend(m, bad_digest=True)
    run_command, _ = _fake_docker_backend(m)
    try:
        m.collect_v2r13_live_identity_candidate(
            observation_authorized=True,
            http_get=http_get,
            run_command=run_command,
        )
    except m.ollama_observer.RuntimeV2R13OllamaObserverHold:
        pass
    else:
        raise AssertionError("bad Ollama digest must be rejected")


def test_bad_runtime_image_id_is_rejected():
    m = _load()
    http_get, _ = _fake_http_backend(m)
    run_command, _ = _fake_docker_backend(m, bad_image=True)
    try:
        m.collect_v2r13_live_identity_candidate(
            observation_authorized=True,
            http_get=http_get,
            run_command=run_command,
        )
    except m.docker_backend.RuntimeV2R13RootlessDockerImageBackendHold:
        pass
    else:
        raise AssertionError("bad runtime image ID must be rejected")


def test_chat_completions_remains_forbidden_in_contract():
    m = _load()
    out = m.v2r13_live_collection_backend_contract()
    assert out["chat_completions_forbidden"] is True
    dep = out["dependency_contracts"]["ollama_observer"]
    assert dep["chat_completions_forbidden"] is True


def test_backend_never_selects_host_factories_automatically():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    forbidden = {
        "ollama_observer.host_http_get",
        "docker_backend.host_readonly_command_runner",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            assert _dotted(node.func) not in forbidden


def test_static_source_has_no_direct_host_io_imports():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    forbidden_roots = {
        "os", "subprocess", "pathlib", "socket", "urllib", "http",
        "requests", "httpx", "docker", "asyncio", "multiprocessing", "ctypes",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_roots


def test_next_gate_is_separate_source_binding():
    m = _load()
    out = m.v2r13_live_collection_backend_contract()
    assert out["next_gate"] == "V2R13_LIVE_COLLECTION_BACKEND_SOURCE_BINDING_REQUIRED"
    assert out["next_change_class"] == "source_only_live_collection_backend_binding"


def test_enable_canonical_live_collection_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13LiveCollectionBackendHold,
        "V2R13_LIVE_COLLECTION_BACKEND_SOURCE_BINDING_REQUIRED",
        lambda: m.enable_canonical_live_collection(),
    )


def test_authorize_runtime_execution_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13LiveCollectionBackendHold,
        "V2R13_LIVE_COLLECTION_SOURCE_BINDING_AND_RUNTIME_ACTIVATION_GAPS_REMAIN",
        lambda: m.authorize_runtime_execution(),
    )
