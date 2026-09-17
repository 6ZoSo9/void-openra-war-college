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
    "abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_entrypoint_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_entrypoint_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "e1cf2acb9fec1fec1d4282312fd26443979f72bda93a3244d1caa5556136d6fa"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    repo = "/home/zoso/dev/openra-rl-war-college"
    if repo not in sys.path:
        sys.path.insert(0, repo)
    spec = importlib.util.spec_from_file_location(
        "_void_g2_v2r13_canonical_live_collection_entrypoint",
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


def _fake_http_backend(m, calls):
    def http_get(url, *, timeout_seconds, maximum_bytes):
        calls.append(url)
        observer = m.adapter.live_backend.ollama_observer
        assert timeout_seconds == observer.DEFAULT_TIMEOUT_SECONDS
        assert maximum_bytes == observer.MAX_RESPONSE_BYTES
        assert url in {observer.OLLAMA_TAGS_URL, observer.OLLAMA_PS_URL}
        body = json.dumps(
            {
                "models": [
                    {
                        "name": observer.activation_contract.V2R13_MODEL_ALIAS,
                        "model": observer.activation_contract.V2R13_MODEL_ALIAS,
                        "digest": observer.activation_contract.V2R13_MODEL_DIGEST,
                    }
                ]
            },
            sort_keys=True,
        ).encode("utf-8")
        return observer.HttpGetResult(
            status=200,
            body=body,
            content_type="application/json",
        )
    return http_get


def _fake_docker_backend(m, calls):
    def run_command(args):
        backend = m.adapter.live_backend.docker_backend
        command = tuple(args)
        calls.append(command)
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


def _worktree_receipt(m):
    req = m.adapter.activation_evidence.evidence_requirement(m.V2R13)
    expected = req["expected"]
    observer = m.adapter.worktree_adapter.worktree_observer
    return {
        "schema": observer.OBSERVATION_SCHEMA,
        "snapshot_id": m.V2R13,
        "frozen_source_worktree": {
            "path": "/tmp/void-v2r13-frozen-source",
            "exists": True,
            "is_directory": True,
            "is_symlink": False,
            "clean": True,
            "detached": True,
            "head_commit": expected["frozen_war_college_commit"],
            "tree_sha": expected["frozen_war_college_tree"],
        },
        "engine_worktree": {
            "path": "/tmp/void-v2r13-engine",
            "exists": True,
            "is_directory": True,
            "is_symlink": False,
            "clean": True,
            "head_commit": expected["frozen_engine_commit"],
        },
        "source_path_generation_stable": True,
        "engine_path_generation_stable": True,
        "git_observation_schema": (
            observer.runtime_observers.V2R13_OBSERVATION_SCHEMA
        ),
        "observation_mode": "read_only",
        "filesystem_observation_performed": True,
        "git_query_performed": True,
        "worktree_created": False,
        "checkout_mutation_performed": False,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_execution_performed": False,
    }


def _portable_receipt(m):
    p = m.adapter.portable_attestation
    return {
        "schema": p.portable_checkout.BINDING_SCHEMA,
        "legacy_source_root_bound": True,
        "legacy_engine_root_bound": True,
        "base_loaded_and_bound": True,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_started": False,
        "attestation_sha256": p.FULLY_BOUND_ATTESTATION_SHA256,
    }


def _collect(m):
    http_calls = []
    docker_calls = []
    out = m.collect_v2r13_canonical_live_collection(
        collection_authorized=True,
        observation_authorized=True,
        http_get=_fake_http_backend(m, http_calls),
        run_command=_fake_docker_backend(m, docker_calls),
        worktree_receipt=_worktree_receipt(m),
        portable_binding_attestation=_portable_receipt(m),
    )
    return out, http_calls, docker_calls


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
    out = m.v2r13_canonical_live_collection_entrypoint_contract()
    assert out["schema"] == (
        "void.abaddon.generation2."
        "v2r13-canonical-live-collection-entrypoint-contract.v1"
    )
    assert out["snapshot_id"] == m.V2R13


def test_dependency_binding_identity_is_exact():
    m = _load()
    out = m.v2r13_canonical_live_collection_entrypoint_contract()
    assert out["adapter_binding_git_blob"] == (
        "4945f98a5dc12cff282c767013f81cac091e32e8"
    )
    assert out["adapter_binding_source_sha256"] == (
        "55d85737e0c0ee55199505b20e5628e8e6f7cc171dba9210cd67c753ec03458c"
    )


def test_adapter_identity_is_exact():
    m = _load()
    out = m.v2r13_canonical_live_collection_entrypoint_contract()
    assert out["adapter_git_blob"] == "29c4bfa11a841359b6c4f4083659c78c474d94ba"
    assert out["adapter_source_sha256"] == (
        "a4236e3c727fcf6eee915ee9e3b44d2ba2e2666e8ac52499c9b342fd71935afb"
    )


def test_entrypoint_implementation_present_but_unbound():
    m = _load()
    out = m.v2r13_canonical_live_collection_entrypoint_contract()
    assert out["canonical_live_collection_entrypoint_implementation_present"] is True
    assert out["entrypoint_composition_implemented"] is True
    assert out["canonical_live_collection_entrypoint_source_binding_present"] is False
    assert out["canonical_live_collection_path_complete"] is False
    assert out["canonical_collection_enabled"] is False


def test_explicit_authority_and_backend_injection_are_required():
    m = _load()
    out = m.v2r13_canonical_live_collection_entrypoint_contract()
    assert out["entrypoint_collection_requires_explicit_authority"] is True
    assert out["entrypoint_observation_requires_explicit_authority"] is True
    assert out["explicit_http_backend_injection_required"] is True
    assert out["explicit_docker_command_backend_injection_required"] is True
    assert out["automatic_host_backend_selection"] is False


def test_unauthorized_collection_holds_before_adapter_invocation():
    m = _load()
    calls = []
    def bomb(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError("adapter/backend must not be invoked")
    original = m.adapter.collect_v2r13_live_collection_adapter_candidate
    m.adapter.collect_v2r13_live_collection_adapter_candidate = bomb
    try:
        _expect_hold(
            m.RuntimeV2R13CanonicalLiveCollectionEntrypointHold,
            "CANONICAL_COLLECTION_NOT_AUTHORIZED",
            lambda: m.collect_v2r13_canonical_live_collection(
                collection_authorized=False,
                observation_authorized=True,
                http_get=lambda *a, **k: None,
                run_command=lambda *a, **k: None,
                worktree_receipt=_worktree_receipt(m),
                portable_binding_attestation=_portable_receipt(m),
            ),
        )
    finally:
        m.adapter.collect_v2r13_live_collection_adapter_candidate = original
    assert calls == []


def test_unauthorized_observation_holds_before_adapter_invocation():
    m = _load()
    calls = []
    def bomb(*args, **kwargs):
        calls.append((args, kwargs))
        raise AssertionError("adapter/backend must not be invoked")
    original = m.adapter.collect_v2r13_live_collection_adapter_candidate
    m.adapter.collect_v2r13_live_collection_adapter_candidate = bomb
    try:
        _expect_hold(
            m.RuntimeV2R13CanonicalLiveCollectionEntrypointHold,
            "CANONICAL_OBSERVATION_NOT_AUTHORIZED",
            lambda: m.collect_v2r13_canonical_live_collection(
                collection_authorized=True,
                observation_authorized=False,
                http_get=lambda *a, **k: None,
                run_command=lambda *a, **k: None,
                worktree_receipt=_worktree_receipt(m),
                portable_binding_attestation=_portable_receipt(m),
            ),
        )
    finally:
        m.adapter.collect_v2r13_live_collection_adapter_candidate = original
    assert calls == []


def test_missing_http_backend_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionEntrypointHold,
        "HTTP GET backend required",
        lambda: m.collect_v2r13_canonical_live_collection(
            collection_authorized=True,
            observation_authorized=True,
            http_get=None,
            run_command=lambda args: None,
            worktree_receipt=_worktree_receipt(m),
            portable_binding_attestation=_portable_receipt(m),
        ),
    )


def test_missing_docker_backend_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionEntrypointHold,
        "Docker command backend required",
        lambda: m.collect_v2r13_canonical_live_collection(
            collection_authorized=True,
            observation_authorized=True,
            http_get=lambda *a, **k: None,
            run_command=None,
            worktree_receipt=_worktree_receipt(m),
            portable_binding_attestation=_portable_receipt(m),
        ),
    )


def test_fake_entrypoint_invokes_adapter_and_binding_validation():
    m = _load()
    out, _, _ = _collect(m)
    assert out["entrypoint_invocation_performed"] is True
    assert out["adapter_invocation_performed"] is True
    assert out["adapter_binding_validation_performed"] is True
    assert out["adapter_bound_validation"]["bound_adapter_candidate_valid"] is True


def test_fake_entrypoint_reaches_16_of_16():
    m = _load()
    out, _, _ = _collect(m)
    assert out["provider_capability_supported_primitive_count"] == 16
    assert out["provider_capability_remaining_unresolved_primitive_count"] == 0
    assert out["provider_capability_complete"] is True


def test_fake_entrypoint_admits_identity_and_readiness():
    m = _load()
    out, _, _ = _collect(m)
    assert out["collector_identity_admitted"] is True
    assert out["runtime_readiness_admitted"] is True


def test_fake_entrypoint_never_authorizes_runtime_execution():
    m = _load()
    out, _, _ = _collect(m)
    assert out["runtime_execution_authorized"] is False
    assert out["adapter_bound_validation"]["runtime_execution_authorized"] is False


def test_fake_entrypoint_uses_two_ollama_metadata_routes_only():
    m = _load()
    out, calls, _ = _collect(m)
    observer = m.adapter.live_backend.ollama_observer
    assert calls == [observer.OLLAMA_TAGS_URL, observer.OLLAMA_PS_URL]
    assert out["chat_completions_request_performed"] is False


def test_fake_entrypoint_uses_three_docker_metadata_commands_only():
    m = _load()
    out, _, calls = _collect(m)
    backend = m.adapter.live_backend.docker_backend
    assert calls == [
        backend.CONTEXT_COMMAND,
        backend.INFO_COMMAND,
        backend.IMAGE_INSPECT_COMMAND,
    ]
    assert out["docker_metadata_command_count"] == 3
    assert out["docker_mutating_command_performed"] is False


def test_supplied_nonlive_receipts_are_not_collected_by_entrypoint():
    m = _load()
    out, _, _ = _collect(m)
    assert out["worktree_observation_performed_by_entrypoint"] is False
    assert out["portable_binding_install_performed_by_entrypoint"] is False


def test_entrypoint_preserves_activation_evidence_identity():
    m = _load()
    out, _, _ = _collect(m)
    assert out["activation_evidence"] == out["adapter_candidate"]["activation_evidence"]
    assert out["activation_evidence_admission"] == (
        out["adapter_candidate"]["activation_evidence_admission"]
    )


def test_entrypoint_preserves_no_mutation_or_execution_actions():
    m = _load()
    out, _, _ = _collect(m)
    for field in (
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
        assert out[field] is False


def test_entrypoint_source_has_no_direct_host_io_imports():
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


def test_entrypoint_never_selects_host_factories_automatically():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    forbidden = {
        "adapter.live_backend.ollama_observer.host_http_get",
        "adapter.live_backend.docker_backend.host_readonly_command_runner",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            assert _dotted(node.func) not in forbidden


def test_entrypoint_calls_only_reviewed_adapter_and_binding_surfaces():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    calls = {
        _dotted(node.func)
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
    }
    assert "adapter.collect_v2r13_live_collection_adapter_candidate" in calls
    assert (
        "adapter_binding.validate_bound_canonical_live_collection_adapter_candidate"
        in calls
    )


def test_entrypoint_candidate_hold_set_is_exact():
    m = _load()
    out, _, _ = _collect(m)
    assert out["holds"] == [
        "V2R13_CANONICAL_LIVE_COLLECTION_ENTRYPOINT_SOURCE_BINDING_REQUIRED",
        m.RUNTIME_AUTHORITY_BLOCKER,
    ]


def test_entrypoint_source_binding_remains_false_in_receipt():
    m = _load()
    out, _, _ = _collect(m)
    assert out["canonical_live_collection_entrypoint_source_binding_present"] is False
    assert out["canonical_live_collection_path_complete"] is False
    assert out["canonical_collection_enabled"] is False


def test_next_gate_is_entrypoint_source_binding():
    m = _load()
    out = m.v2r13_canonical_live_collection_entrypoint_contract()
    assert out["next_gate"] == (
        "V2R13_CANONICAL_LIVE_COLLECTION_ENTRYPOINT_SOURCE_BINDING_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_canonical_live_collection_entrypoint_binding"
    )


def test_enable_canonical_live_collection_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionEntrypointHold,
        "V2R13_CANONICAL_LIVE_COLLECTION_ENTRYPOINT_SOURCE_BINDING_REQUIRED",
        lambda: m.enable_canonical_live_collection(),
    )


def test_authorize_runtime_execution_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionEntrypointHold,
        "ENTRYPOINT_SOURCE_BINDING_AND_RUNTIME_ACTIVATION_GAPS_REMAIN",
        lambda: m.authorize_runtime_execution(),
    )


def test_tampered_worktree_receipt_is_rejected():
    m = _load()
    receipt = deepcopy(_worktree_receipt(m))
    receipt["frozen_source_worktree"]["head_commit"] = "0" * 40
    try:
        m.collect_v2r13_canonical_live_collection(
            collection_authorized=True,
            observation_authorized=True,
            http_get=_fake_http_backend(m, []),
            run_command=_fake_docker_backend(m, []),
            worktree_receipt=receipt,
            portable_binding_attestation=_portable_receipt(m),
        )
    except Exception:
        pass
    else:
        raise AssertionError("tampered worktree receipt must be rejected")


def test_tampered_portable_receipt_is_rejected():
    m = _load()
    receipt = deepcopy(_portable_receipt(m))
    receipt["attestation_sha256"] = "0" * 64
    try:
        m.collect_v2r13_canonical_live_collection(
            collection_authorized=True,
            observation_authorized=True,
            http_get=_fake_http_backend(m, []),
            run_command=_fake_docker_backend(m, []),
            worktree_receipt=_worktree_receipt(m),
            portable_binding_attestation=receipt,
        )
    except Exception:
        pass
    else:
        raise AssertionError("tampered portable receipt must be rejected")
