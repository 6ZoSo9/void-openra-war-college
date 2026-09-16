from __future__ import annotations

import ast
import hashlib
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_v2r13_collector_reconciliation_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_collector_reconciliation_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "f1c6009735be69a86d77bf1c9ac2fe911bbac97c06076395c6656ce94fa76b86"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_v2r13_collector_reconciliation",
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


def test_source_sha_is_exact():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SOURCE_SHA256


def test_contract_schema_and_status_are_exact():
    m = _load()
    out = m.v2r13_collector_reconciliation_contract()
    assert out["schema"] == (
        "void.abaddon.generation2.v2r13-collector-reconciliation-contract.v1"
    )
    assert out["reconciliation_status"] == (
        "provider-capability-complete-collector-binding-still-closed"
    )
    assert out["source_only_reconciliation"] is True


def test_exact_reviewed_source_identities_are_pinned():
    m = _load()
    out = m.v2r13_collector_reconciliation_contract()
    assert out["historical_collector_contract_git_blob"] == (
        "8014431ad5329137e5ce12334d19d37c877a0b52"
    )
    assert out["historical_collector_contract_source_sha256"] == (
        "c48ad0871d4ea25e45efcde36e59622d1bb6b2a2fc4a4ed1f25988b543c2038f"
    )
    assert out["collector_implementation_git_blob"] == (
        "0003c24390194a4f621f13c6077e0604b9abcd98"
    )
    assert out["collector_implementation_source_sha256"] == (
        "91e094c71b838ad8116dced00fbc50b3e8a8bd138f75dfb5ae86b9bf5c97a8dc"
    )
    assert out["v2r13_ollama_binding_git_blob"] == (
        "58364a1d5d71aead9df6dc0fc61661a557131508"
    )
    assert out["v2r13_ollama_binding_source_sha256"] == (
        "c6b0bb746d017326e600f401a2d07a29fba79aced401687c4eb5238084ee9335"
    )


def test_historical_future_provider_list_is_exact():
    m = _load()
    out = m.v2r13_collector_reconciliation_contract()
    assert out["historical_required_future_primitives"] == (
        "read_only_loopback_endpoint_liveness",
        "read_only_active_model_digest_identity",
        "read_only_runtime_image_identity",
        "read_only_worktree_path_classification",
        "portable_binding_attestation",
        "common_operational_action_ledger",
    )
    assert out["historical_required_future_primitive_count"] == 6


def test_provider_frontier_is_exact_16_zero():
    m = _load()
    out = m.v2r13_collector_reconciliation_contract()
    assert out["provider_supported_primitive_count"] == 16
    assert out["provider_remaining_unresolved_primitive_count"] == 0
    assert out["provider_remaining_unresolved_primitive_names"] == ()
    assert out["provider_capability_coverage_complete"] is True


def test_historical_provider_gap_is_closed_but_contract_needs_reconciliation():
    m = _load()
    out = m.v2r13_collector_reconciliation_contract()
    assert out["historical_future_provider_gap_closed"] is True
    assert out["historical_contract_reconciliation_required"] is True


def test_candidate_orchestration_is_present():
    m = _load()
    out = m.v2r13_collector_reconciliation_contract()
    assert out["collector_candidate_orchestration_present"] is True


def test_collector_implementation_source_binding_remains_absent():
    m = _load()
    out = m.v2r13_collector_reconciliation_contract()
    assert out["collector_implementation_source_binding_present"] is False


def test_canonical_primitive_source_bindings_remain_absent():
    m = _load()
    out = m.v2r13_collector_reconciliation_contract()
    assert out["canonical_primitive_source_bindings_present"] is False


def test_reviewed_collector_binding_remains_absent():
    m = _load()
    out = m.v2r13_collector_reconciliation_contract()
    assert out["reviewed_collector_binding_present"] is False


def test_canonical_provider_binding_remains_closed():
    m = _load()
    out = m.v2r13_collector_reconciliation_contract()
    assert out["canonical_provider_binding_present"] is False


def test_canonical_collection_remains_closed():
    m = _load()
    out = m.v2r13_collector_reconciliation_contract()
    assert out["canonical_collection_enabled"] is False


def test_collector_identity_remains_unadmitted():
    m = _load()
    out = m.v2r13_collector_reconciliation_contract()
    assert out["collector_identity_admitted"] is False


def test_runtime_readiness_remains_unadmitted():
    m = _load()
    out = m.v2r13_collector_reconciliation_contract()
    assert out["runtime_readiness_admitted"] is False


def test_runtime_execution_remains_unauthorized():
    m = _load()
    out = m.v2r13_collector_reconciliation_contract()
    assert out["runtime_execution_authorized"] is False


def test_no_live_or_host_actions_are_claimed():
    m = _load()
    out = m.v2r13_collector_reconciliation_contract()
    for field in (
        "live_observation_performed",
        "http_request_performed",
        "host_backend_invoked",
        "ollama_request_performed",
        "docker_command_executed",
        "service_action_performed",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
    ):
        assert out[field] is False


def test_no_training_deploy_chain_or_funds_actions_are_claimed():
    m = _load()
    out = m.v2r13_collector_reconciliation_contract()
    for field in (
        "training_performed",
        "weights_updated",
        "policy_promotion_performed",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        assert out[field] is False


def test_returned_nested_contracts_are_copy_isolated():
    m = _load()
    first = m.v2r13_collector_reconciliation_contract()
    first["historical_collector_contract"]["semantic_contract_valid"] = False
    second = m.v2r13_collector_reconciliation_contract()
    assert second["historical_collector_contract"]["semantic_contract_valid"] is True


def test_source_has_no_host_io_imports_or_calls():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    forbidden_import_roots = {
        "os", "subprocess", "pathlib", "socket", "urllib", "http", "requests",
        "httpx", "docker", "asyncio", "multiprocessing", "ctypes",
    }
    forbidden_call_prefixes = (
        "os.", "subprocess.", "pathlib.", "socket.", "urllib.", "http.",
        "requests.", "httpx.", "docker.",
        "ollama_binding.ollama_observer.host_http_get",
        "ollama_binding.ollama_observer.observe_v2r13_ollama_readonly",
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


def test_enable_canonical_collection_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13CollectorReconciliationHold,
        "V2R13_COLLECTOR_RECONCILIATION_DOES_NOT_AUTHORIZE_CANONICAL_COLLECTION",
        lambda: m.enable_canonical_collection(),
    )
