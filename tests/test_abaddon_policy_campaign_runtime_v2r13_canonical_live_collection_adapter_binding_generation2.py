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
    "abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_adapter_binding_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_adapter_binding_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "55d85737e0c0ee55199505b20e5628e8e6f7cc171dba9210cd67c753ec03458c"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    repo = "/home/zoso/dev/openra-rl-war-college"
    if repo not in sys.path:
        sys.path.insert(0, repo)
    spec = importlib.util.spec_from_file_location(
        "_void_g2_v2r13_canonical_adapter_binding",
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
    req = m.activation_evidence.evidence_requirement(m.V2R13)
    expected = req["expected"]
    observer = m.worktree_adapter.worktree_observer
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
    p = m.portable_attestation
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


def _candidate(m):
    http_calls = []
    docker_calls = []
    candidate = m.adapter.collect_v2r13_live_collection_adapter_candidate(
        collection_authorized=True,
        observation_authorized=True,
        http_get=_fake_http_backend(m, http_calls),
        run_command=_fake_docker_backend(m, docker_calls),
        worktree_receipt=_worktree_receipt(m),
        portable_binding_attestation=_portable_receipt(m),
    )
    return candidate, http_calls, docker_calls


def _validate(m, candidate):
    return m.validate_bound_canonical_live_collection_adapter_candidate(
        candidate,
        adapter_source_sha256=m.ADAPTER_SOURCE_SHA256,
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
    out = m.v2r13_canonical_live_collection_adapter_binding_contract()
    assert out["schema"] == (
        "void.abaddon.generation2."
        "v2r13-canonical-live-collection-adapter-binding-contract.v1"
    )
    assert out["snapshot_id"] == m.V2R13


def test_adapter_identity_is_pinned_exactly():
    m = _load()
    out = m.v2r13_canonical_live_collection_adapter_binding_contract()
    assert out["adapter_git_blob"] == "29c4bfa11a841359b6c4f4083659c78c474d94ba"
    assert out["adapter_source_sha256"] == (
        "a4236e3c727fcf6eee915ee9e3b44d2ba2e2666e8ac52499c9b342fd71935afb"
    )


def test_binding_is_separate_and_non_self_referential():
    m = _load()
    out = m.v2r13_canonical_live_collection_adapter_binding_contract()
    assert out["separate_binding_instrument"] is True
    assert out["adapter_source_is_not_self_bound"] is True
    assert out["canonical_live_collection_adapter_source_binding_present"] is True


def test_dependency_adapter_remains_unbound_in_its_own_source():
    m = _load()
    out = m.v2r13_canonical_live_collection_adapter_binding_contract()
    adapter_contract = out["dependency_contracts"]["adapter"]
    assert adapter_contract["canonical_live_collection_adapter_source_binding_present"] is False
    assert adapter_contract["canonical_collection_enabled"] is False


def test_binding_preserves_explicit_authority_requirements():
    m = _load()
    out = m.v2r13_canonical_live_collection_adapter_binding_contract()
    assert out["adapter_collection_requires_explicit_authority"] is True
    assert out["adapter_observation_requires_explicit_authority"] is True
    assert out["explicit_http_backend_injection_required"] is True
    assert out["explicit_docker_command_backend_injection_required"] is True
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


def test_binding_never_invokes_adapter_collection_entrypoint():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    forbidden = {
        "adapter.collect_v2r13_live_collection_adapter_candidate",
        "adapter.live_backend.ollama_observer.host_http_get",
        "adapter.live_backend.docker_backend.host_readonly_command_runner",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            assert _dotted(node.func) not in forbidden


def test_provider_frontier_remains_16_of_16():
    m = _load()
    out = m.v2r13_canonical_live_collection_adapter_binding_contract()
    assert out["provider_capability_supported_primitive_count"] == 16
    assert out["provider_capability_remaining_unresolved_primitive_count"] == 0
    assert out["provider_capability_complete"] is True


def test_exact_fake_candidate_is_admitted_by_binding():
    m = _load()
    candidate, _, _ = _candidate(m)
    out = _validate(m, candidate)
    assert out["bound_adapter_candidate_valid"] is True
    assert out["canonical_live_collection_adapter_source_binding_present"] is True


def test_bound_validation_preserves_candidate_readiness_admission():
    m = _load()
    candidate, _, _ = _candidate(m)
    out = _validate(m, candidate)
    assert out["collector_identity_admitted"] is True
    assert out["runtime_readiness_admitted"] is True
    assert out["runtime_execution_authorized"] is False


def test_bound_validation_revalidates_supplied_live_observation():
    m = _load()
    candidate, _, _ = _candidate(m)
    out = _validate(m, candidate)
    assert out["supplied_live_observation_validated"] is True
    assert out["supplied_live_observation_performed"] is True
    assert out["binding_live_observation_performed"] is False
    assert out["binding_adapter_invocation_performed"] is False


def test_bound_validation_recomputes_collector_candidate_exactly():
    m = _load()
    candidate, _, _ = _candidate(m)
    out = _validate(m, candidate)
    assert out["collector_candidate"] == candidate["collector_candidate"]


def test_bound_validation_recomputes_admission_exactly():
    m = _load()
    candidate, _, _ = _candidate(m)
    out = _validate(m, candidate)
    assert out["activation_evidence_admission"] == (
        candidate["activation_evidence_admission"]
    )


def test_source_sha_mismatch_is_rejected():
    m = _load()
    candidate, _, _ = _candidate(m)
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionAdapterBindingHold,
        "source SHA mismatch",
        lambda: m.validate_bound_canonical_live_collection_adapter_candidate(
            candidate,
            adapter_source_sha256="0" * 64,
        ),
    )


def test_tampered_field_set_is_rejected():
    m = _load()
    candidate, _, _ = _candidate(m)
    candidate = deepcopy(candidate)
    candidate["unexpected"] = True
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionAdapterBindingHold,
        "field-set drift",
        lambda: _validate(m, candidate),
    )


def test_tampered_action_boolean_is_rejected():
    m = _load()
    candidate, _, _ = _candidate(m)
    candidate = deepcopy(candidate)
    candidate["runtime_start_performed"] = True
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionAdapterBindingHold,
        "crossed boundary",
        lambda: _validate(m, candidate),
    )


def test_tampered_hold_set_is_rejected():
    m = _load()
    candidate, _, _ = _candidate(m)
    candidate = deepcopy(candidate)
    candidate["holds"] = list(reversed(candidate["holds"]))
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionAdapterBindingHold,
        "hold set drift",
        lambda: _validate(m, candidate),
    )


def test_tampered_primitive_receipt_is_rejected():
    m = _load()
    candidate, _, _ = _candidate(m)
    candidate = deepcopy(candidate)
    candidate["collector_candidate"]["primitive_receipts"][0]["source_sha256"] = "0" * 64
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionAdapterBindingHold,
        "primitive source binding mismatch",
        lambda: _validate(m, candidate),
    )


def test_tampered_activation_evidence_is_rejected():
    m = _load()
    candidate, _, _ = _candidate(m)
    candidate = deepcopy(candidate)
    candidate["activation_evidence"]["endpoint_liveness"] = False
    try:
        _validate(m, candidate)
    except Exception:
        pass
    else:
        raise AssertionError("tampered activation evidence must be rejected")


def test_tampered_live_backend_candidate_is_rejected():
    m = _load()
    candidate, _, _ = _candidate(m)
    candidate = deepcopy(candidate)
    candidate["live_backend_candidate"]["model_identity_verified"] = False
    try:
        _validate(m, candidate)
    except Exception:
        pass
    else:
        raise AssertionError("tampered live backend candidate must be rejected")


def test_tampered_portable_validation_receipt_is_rejected():
    m = _load()
    candidate, _, _ = _candidate(m)
    candidate = deepcopy(candidate)
    candidate["portable_binding_validation"]["validated_receipt"]["attestation_sha256"] = (
        "0" * 64
    )
    try:
        _validate(m, candidate)
    except Exception:
        pass
    else:
        raise AssertionError("tampered portable validation must be rejected")


def test_tampered_worktree_validation_is_rejected():
    m = _load()
    candidate, _, _ = _candidate(m)
    candidate = deepcopy(candidate)
    candidate["worktree_validation"]["git_identity_complete"] = False
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionAdapterBindingHold,
        "worktree validation drift",
        lambda: _validate(m, candidate),
    )


def test_canonical_collection_remains_closed_after_source_binding():
    m = _load()
    out = m.v2r13_canonical_live_collection_adapter_binding_contract()
    assert out["canonical_live_collection_path_complete"] is False
    assert out["canonical_collection_enabled"] is False
    assert out["runtime_execution_authorized"] is False


def test_next_gate_is_bound_collection_entrypoint():
    m = _load()
    out = m.v2r13_canonical_live_collection_adapter_binding_contract()
    assert out["next_gate"] == "V2R13_CANONICAL_LIVE_COLLECTION_ENTRYPOINT_REQUIRED"
    assert out["next_change_class"] == (
        "explicit_authority_bound_canonical_live_collection_entrypoint"
    )


def test_collect_bound_canonical_live_collection_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionAdapterBindingHold,
        "BOUND_CANONICAL_LIVE_COLLECTION_ENTRYPOINT_NOT_IMPLEMENTED",
        lambda: m.collect_bound_canonical_live_collection(),
    )


def test_enable_canonical_live_collection_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionAdapterBindingHold,
        "V2R13_CANONICAL_LIVE_COLLECTION_ENTRYPOINT_REQUIRED",
        lambda: m.enable_canonical_live_collection(),
    )


def test_authorize_runtime_execution_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionAdapterBindingHold,
        "CANONICAL_COLLECTION_ENTRYPOINT_AND_RUNTIME_ACTIVATION_GAPS_REMAIN",
        lambda: m.authorize_runtime_execution(),
    )
