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
    "abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_entrypoint_binding_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_entrypoint_binding_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "06c5a110401b05631eb64496cee7b2d7e56378a9376c9d0c4fd1db015c6308f1"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    repo = "/home/zoso/dev/openra-rl-war-college"
    if repo not in sys.path:
        sys.path.insert(0, repo)
    spec = importlib.util.spec_from_file_location(
        "_void_g2_v2r13_canonical_live_collection_entrypoint_binding",
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
        observer = m.entrypoint.adapter.live_backend.ollama_observer
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
        backend = m.entrypoint.adapter.live_backend.docker_backend
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
    a = m.entrypoint.adapter
    req = a.activation_evidence.evidence_requirement(m.V2R13)
    expected = req["expected"]
    observer = a.worktree_adapter.worktree_observer
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
        "git_observation_schema": observer.runtime_observers.V2R13_OBSERVATION_SCHEMA,
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
    p = m.entrypoint.adapter.portable_attestation
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


def _receipt(m):
    http_calls = []
    docker_calls = []
    out = m.entrypoint.collect_v2r13_canonical_live_collection(
        collection_authorized=True,
        observation_authorized=True,
        http_get=_fake_http_backend(m, http_calls),
        run_command=_fake_docker_backend(m, docker_calls),
        worktree_receipt=_worktree_receipt(m),
        portable_binding_attestation=_portable_receipt(m),
    )
    return out, http_calls, docker_calls


def _validate(m, receipt):
    return m.validate_bound_canonical_live_collection_entrypoint_receipt(
        receipt,
        entrypoint_source_sha256=m.ENTRYPOINT_SOURCE_SHA256,
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
    out = m.v2r13_canonical_live_collection_entrypoint_binding_contract()
    assert out["schema"] == (
        "void.abaddon.generation2."
        "v2r13-canonical-live-collection-entrypoint-binding-contract.v1"
    )
    assert out["snapshot_id"] == m.V2R13


def test_entrypoint_identity_is_pinned_exactly():
    m = _load()
    out = m.v2r13_canonical_live_collection_entrypoint_binding_contract()
    assert out["entrypoint_git_blob"] == "48e579c5d8ef0c05db93d637777d4882493cbf9d"
    assert out["entrypoint_source_sha256"] == (
        "e1cf2acb9fec1fec1d4282312fd26443979f72bda93a3244d1caa5556136d6fa"
    )


def test_binding_is_separate_and_non_self_referential():
    m = _load()
    out = m.v2r13_canonical_live_collection_entrypoint_binding_contract()
    assert out["separate_binding_instrument"] is True
    assert out["entrypoint_source_is_not_self_bound"] is True
    assert out["canonical_live_collection_entrypoint_source_binding_present"] is True


def test_dependency_entrypoint_remains_unbound_in_its_own_source():
    m = _load()
    out = m.v2r13_canonical_live_collection_entrypoint_binding_contract()
    dep = out["dependency_contracts"]["entrypoint"]
    assert dep["canonical_live_collection_entrypoint_source_binding_present"] is False
    assert dep["canonical_live_collection_path_complete"] is False
    assert dep["canonical_collection_enabled"] is False


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


def test_binding_never_invokes_entrypoint_or_host_factories():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    forbidden = {
        "entrypoint.collect_v2r13_canonical_live_collection",
        "entrypoint.adapter.live_backend.ollama_observer.host_http_get",
        "entrypoint.adapter.live_backend.docker_backend.host_readonly_command_runner",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            assert _dotted(node.func) not in forbidden


def test_exact_fake_receipt_is_admitted_by_binding():
    m = _load()
    receipt, _, _ = _receipt(m)
    out = _validate(m, receipt)
    assert out["bound_entrypoint_receipt_valid"] is True
    assert out["canonical_live_collection_entrypoint_source_binding_present"] is True


def test_binding_validation_marks_path_complete_but_not_enabled():
    m = _load()
    receipt, _, _ = _receipt(m)
    out = _validate(m, receipt)
    assert out["canonical_live_collection_path_complete"] is True
    assert out["canonical_collection_enabled"] is False
    assert out["runtime_execution_authorized"] is False


def test_binding_contract_marks_path_complete_but_not_enabled():
    m = _load()
    out = m.v2r13_canonical_live_collection_entrypoint_binding_contract()
    assert out["canonical_live_collection_path_complete"] is True
    assert out["canonical_collection_enabled"] is False
    assert out["runtime_execution_authorized"] is False


def test_bound_validation_preserves_identity_and_readiness():
    m = _load()
    receipt, _, _ = _receipt(m)
    out = _validate(m, receipt)
    assert out["collector_identity_admitted"] is True
    assert out["runtime_readiness_admitted"] is True


def test_bound_validation_performs_no_entrypoint_or_live_observation():
    m = _load()
    receipt, _, _ = _receipt(m)
    out = _validate(m, receipt)
    assert out["binding_entrypoint_invocation_performed"] is False
    assert out["binding_live_observation_performed"] is False
    assert out["binding_http_request_performed"] is False
    assert out["binding_ollama_request_performed"] is False
    assert out["binding_docker_command_performed"] is False


def test_entrypoint_source_sha_mismatch_is_rejected():
    m = _load()
    receipt, _, _ = _receipt(m)
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionEntrypointBindingHold,
        "source SHA mismatch",
        lambda: m.validate_bound_canonical_live_collection_entrypoint_receipt(
            receipt,
            entrypoint_source_sha256="0" * 64,
        ),
    )


def test_tampered_field_set_is_rejected():
    m = _load()
    receipt, _, _ = _receipt(m)
    receipt = deepcopy(receipt)
    receipt["unexpected"] = True
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionEntrypointBindingHold,
        "field-set drift",
        lambda: _validate(m, receipt),
    )


def test_tampered_runtime_action_is_rejected():
    m = _load()
    receipt, _, _ = _receipt(m)
    receipt = deepcopy(receipt)
    receipt["runtime_start_performed"] = True
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionEntrypointBindingHold,
        "crossed boundary",
        lambda: _validate(m, receipt),
    )


def test_tampered_hold_set_is_rejected():
    m = _load()
    receipt, _, _ = _receipt(m)
    receipt = deepcopy(receipt)
    receipt["holds"] = list(reversed(receipt["holds"]))
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionEntrypointBindingHold,
        "hold set drift",
        lambda: _validate(m, receipt),
    )


def test_tampered_adapter_candidate_is_rejected():
    m = _load()
    receipt, _, _ = _receipt(m)
    receipt = deepcopy(receipt)
    receipt["adapter_candidate"]["runtime_start_performed"] = True
    try:
        _validate(m, receipt)
    except Exception:
        pass
    else:
        raise AssertionError("tampered adapter candidate must be rejected")


def test_tampered_embedded_adapter_validation_is_rejected():
    m = _load()
    receipt, _, _ = _receipt(m)
    receipt = deepcopy(receipt)
    receipt["adapter_bound_validation"]["runtime_readiness_admitted"] = False
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionEntrypointBindingHold,
        "embedded adapter validation mismatch",
        lambda: _validate(m, receipt),
    )


def test_tampered_activation_evidence_identity_is_rejected():
    m = _load()
    receipt, _, _ = _receipt(m)
    receipt = deepcopy(receipt)
    receipt["activation_evidence"]["endpoint_liveness"] = False
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionEntrypointBindingHold,
        "activation evidence identity mismatch",
        lambda: _validate(m, receipt),
    )


def test_tampered_dependency_snapshot_is_rejected():
    m = _load()
    receipt, _, _ = _receipt(m)
    receipt = deepcopy(receipt)
    receipt["dependency_contracts"]["adapter_binding"]["runtime_execution_authorized"] = True
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionEntrypointBindingHold,
        "dependency snapshot drift",
        lambda: _validate(m, receipt),
    )


def test_next_gate_is_explicit_live_collection_authorization():
    m = _load()
    out = m.v2r13_canonical_live_collection_entrypoint_binding_contract()
    assert out["next_gate"] == (
        "V2R13_CANONICAL_LIVE_COLLECTION_INVOCATION_AUTHORIZATION_REQUIRED"
    )
    assert out["next_change_class"] == (
        "explicit_live_collection_authorization_and_invocation"
    )


def test_enable_canonical_live_collection_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionEntrypointBindingHold,
        "V2R13_CANONICAL_LIVE_COLLECTION_INVOCATION_AUTHORIZATION_REQUIRED",
        lambda: m.enable_canonical_live_collection(),
    )


def test_authorize_runtime_execution_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionEntrypointBindingHold,
        "LIVE_INVOCATION_AND_RUNTIME_ACTIVATION_GAPS_REMAIN",
        lambda: m.authorize_runtime_execution(),
    )
