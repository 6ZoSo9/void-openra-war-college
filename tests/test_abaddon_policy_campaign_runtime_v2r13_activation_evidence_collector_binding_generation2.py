from __future__ import annotations

import ast
import hashlib
import importlib.util
import sys
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_v2r13_activation_evidence_collector_binding_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_activation_evidence_collector_binding_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "57b45d106f5d4f2e2531a445669910d925c2e0e4bfad725333714703a75b616e"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    repo = "/home/zoso/dev/openra-rl-war-college"
    if repo not in sys.path:
        sys.path.insert(0, repo)
    spec = importlib.util.spec_from_file_location(
        "_void_g2_v2r13_activation_evidence_collector_binding",
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


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def _record(m):
    req = m.activation_evidence.evidence_requirement(m.V2R13)
    expected = req["expected"]
    return {
        "schema": m.activation_evidence.EVIDENCE_SCHEMA,
        "snapshot_id": m.V2R13,
        "snapshot_sha256": req["snapshot_sha256"],
        "runtime_class": req["runtime_class"],
        "evidence_kind": req["evidence_kind"],
        "collector_contract_sha256": m.COLLECTOR_SEMANTIC_SHA256,
        "observation_mode": "read_only",
        "mutation_performed": False,
        "service_action_performed": False,
        "runtime_start_performed": False,
        "game_execution_performed": False,
        "model_inference_performed": False,
        "endpoint_url": expected["endpoint_url"],
        "endpoint_loopback": True,
        "endpoint_liveness": True,
        "active_model_alias": expected["active_model_alias"],
        "active_model_digest": expected["active_model_digest"],
        "model_identity_verified": True,
        "runtime_image_id": expected["runtime_image_id"],
        "runtime_image_identity_verified": True,
        "frozen_source_worktree": {
            "path": "/tmp/void-g2-v2r13-bound-source",
            "exists": True,
            "is_directory": True,
            "is_symlink": False,
            "clean": True,
            "detached": True,
            "head_commit": expected["frozen_war_college_commit"],
            "tree_sha": expected["frozen_war_college_tree"],
        },
        "engine_worktree": {
            "path": "/tmp/void-g2-v2r13-bound-engine",
            "exists": True,
            "is_directory": True,
            "is_symlink": False,
            "clean": True,
            "head_commit": expected["frozen_engine_commit"],
        },
        "portable_binding_attested": True,
    }


def test_source_sha_is_exact():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SOURCE_SHA256


def test_contract_schema_and_snapshot_are_exact():
    m = _load()
    out = m.v2r13_activation_evidence_collector_binding_contract()
    assert out["schema"] == (
        "void.abaddon.generation2."
        "v2r13-activation-evidence-collector-binding-contract.v1"
    )
    assert out["snapshot_id"] == m.V2R13


def test_exact_source_identities_are_pinned():
    m = _load()
    out = m.v2r13_activation_evidence_collector_binding_contract()
    assert out["activation_evidence_git_blob"] == (
        "aac7964d9e80633535003b9f27066cac1bb4bac2"
    )
    assert out["activation_evidence_source_sha256"] == (
        "c08a53842000343544f7ba63e8ae3bc4d24cb7f771294073caf4ab4a5ddc19a0"
    )
    assert out["collector_implementation_git_blob"] == (
        "0003c24390194a4f621f13c6077e0604b9abcd98"
    )
    assert out["collector_binding_git_blob"] == (
        "bcc12598161a9516cb002d6e1c4eead7e914a425"
    )
    assert out["collector_binding_source_sha256"] == (
        "af4a51207a0ad1477eedd18c325ee1df2231b6ad990bbb6f4f8ba53ef5bffc1d"
    )


def test_collector_semantic_identity_is_exact():
    m = _load()
    out = m.v2r13_activation_evidence_collector_binding_contract()
    assert out["collector_semantic_sha256"] == (
        "d11e45cabc10b42e09ab5e328e1e63721b633c7cdcfd7492038ec286b7f3e657"
    )


def test_prior_collector_binding_is_complete():
    m = _load()
    out = m.v2r13_activation_evidence_collector_binding_contract()
    assert out["canonical_primitive_source_bindings_present"] is True
    assert out["primitive_source_binding_count"] == 16


def test_separate_reviewed_collector_binding_is_present():
    m = _load()
    out = m.v2r13_activation_evidence_collector_binding_contract()
    assert out["reviewed_collector_binding_present"] is True
    assert out["collector_identity_admission_implemented"] is True
    assert out["runtime_readiness_admission_implemented"] is True


def test_base_activation_evidence_source_remains_unmodified_and_closed():
    m = _load()
    out = m.v2r13_activation_evidence_collector_binding_contract()
    dep = out["dependency_contracts"]["activation_evidence_contract"]
    assert m.activation_evidence.REVIEWED_COLLECTOR_BINDING_PRESENT is False
    assert dep["reviewed_collector_binding_present"] is False
    assert dep["runtime_execution_authorized"] is False


def test_contract_does_not_admit_without_evidence():
    m = _load()
    out = m.v2r13_activation_evidence_collector_binding_contract()
    assert out["collector_identity_admitted_without_evidence"] is False
    assert out["runtime_readiness_admitted_without_evidence"] is False


def test_valid_bound_v2r13_evidence_is_admitted():
    m = _load()
    out = m.admit_bound_v2r13_evidence(_record(m))
    assert out["evidence_shape_valid"] is True
    assert out["reviewed_collector_binding_present"] is True
    assert out["collector_identity_admitted"] is True
    assert out["runtime_readiness_admitted"] is True
    assert out["runtime_execution_authorized"] is False


def test_bound_admission_leaves_only_runtime_authority_hold():
    m = _load()
    out = m.admit_bound_v2r13_evidence(_record(m))
    assert out["holds"] == [m.RUNTIME_AUTHORITY_BLOCKER]
    assert len(out["superseded_base_shape_holds"]) >= 1


def test_binding_admits_v2r13_only():
    m = _load()
    record = _record(m)
    record["snapshot_id"] = m.activation_evidence.V14
    _expect_hold(
        m.RuntimeV2R13ActivationEvidenceCollectorBindingHold,
        "admits V2R13 only",
        lambda: m.admit_bound_v2r13_evidence(record),
    )


def test_wrong_collector_semantic_sha_is_rejected():
    m = _load()
    record = _record(m)
    record["collector_contract_sha256"] = "0" * 64
    _expect_hold(
        m.RuntimeV2R13ActivationEvidenceCollectorBindingHold,
        "collector semantic SHA mismatch",
        lambda: m.admit_bound_v2r13_evidence(record),
    )


def test_mutation_claim_is_rejected_by_base_shape_validator():
    m = _load()
    record = _record(m)
    record["mutation_performed"] = True
    _expect_hold(
        m.activation_evidence.RuntimeActivationEvidenceHold,
        "crossed authority boundary",
        lambda: m.admit_bound_v2r13_evidence(record),
    )


def test_evidence_field_set_drift_is_rejected():
    m = _load()
    record = _record(m)
    record["unexpected"] = True
    _expect_hold(
        m.activation_evidence.RuntimeActivationEvidenceHold,
        "evidence field set drift",
        lambda: m.admit_bound_v2r13_evidence(record),
    )


def test_input_evidence_is_not_mutated():
    m = _load()
    record = _record(m)
    before = deepcopy(record)
    m.admit_bound_v2r13_evidence(record)
    assert record == before


def test_returned_evidence_is_copy_isolated():
    m = _load()
    record = _record(m)
    out = m.admit_bound_v2r13_evidence(record)
    out["validated_evidence"]["endpoint_liveness"] = False
    assert record["endpoint_liveness"] is True


def test_canonical_collection_and_provider_selection_remain_closed():
    m = _load()
    out = m.admit_bound_v2r13_evidence(_record(m))
    assert out["canonical_provider_binding_present"] is False
    assert out["canonical_collection_enabled"] is False


def test_admission_claims_zero_live_actions():
    m = _load()
    out = m.admit_bound_v2r13_evidence(_record(m))
    for field in (
        "evidence_collected_by_binding",
        "live_observation_performed",
        "filesystem_observation_performed",
        "git_query_performed",
        "subprocess_execution_performed",
        "network_request_performed",
        "ollama_request_performed",
        "docker_command_executed",
        "service_action_performed",
        "runtime_start_performed",
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


def test_static_source_has_no_host_io_imports_or_calls():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    forbidden_import_roots = {
        "os", "subprocess", "pathlib", "socket", "urllib", "http", "requests",
        "httpx", "docker", "asyncio", "multiprocessing", "ctypes",
    }
    forbidden_call_prefixes = (
        "os.", "subprocess.", "pathlib.", "socket.", "urllib.", "http.",
        "requests.", "httpx.", "docker.",
        "collector_implementation.collect_candidate_with_provider",
    )
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call):
            name = _dotted(node.func)
            assert not name.startswith(forbidden_call_prefixes)


def test_runtime_execution_authorization_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13ActivationEvidenceCollectorBindingHold,
        "RUNTIME_EXECUTION_NOT_AUTHORIZED",
        lambda: m.authorize_runtime_execution(),
    )
