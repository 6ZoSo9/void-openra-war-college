from __future__ import annotations

import ast
import hashlib
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_v2r13_post_admission_reconciliation_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_post_admission_reconciliation_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "8548a745b617b46a72faf8b4f8b196916caf3e51c5c924a0dc68b3547a282346"
EXPECTED_LIVE_IMPL_SHA256 = "8c415a0f3690a96a95c051a365691d3dad501e5656b438b0bf57a502311db9c8"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    repo = "/home/zoso/dev/openra-rl-war-college"
    if repo not in sys.path:
        sys.path.insert(0, repo)
    spec = importlib.util.spec_from_file_location(
        "_void_g2_v2r13_post_admission_reconciliation",
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


def test_schema_and_snapshot_are_exact():
    m = _load()
    out = m.v2r13_post_admission_reconciliation_contract()
    assert out["schema"] == (
        "void.abaddon.generation2."
        "v2r13-post-admission-collection-activation-reconciliation.v1"
    )
    assert out["snapshot_id"] == m.activation_contract.V2R13


def test_live_identity_implementation_identity_is_pinned():
    m = _load()
    out = m.v2r13_post_admission_reconciliation_contract()
    assert out["live_identity_implementation_git_blob"] == (
        "49b1044a45cdb92d7077028b9856ef710f07b275"
    )
    assert out["live_identity_implementation_source_sha256"] == (
        EXPECTED_LIVE_IMPL_SHA256
    )
    assert out["live_identity_implementation_source_binding_present"] is True


def test_live_identity_implementation_remains_non_self_bound():
    m = _load()
    out = m.v2r13_post_admission_reconciliation_contract()
    assert out["live_identity_implementation_self_binding_present"] is False
    dep = out["dependency_contracts"]["dormant_live_identity_implementation"]
    assert dep["canonical_implementation_source_binding_present"] is False


def test_post116_readiness_layer_is_complete():
    m = _load()
    out = m.v2r13_post_admission_reconciliation_contract()
    assert out["post_admission_readiness_layer_complete"] is True
    assert out["reviewed_collector_binding_present"] is True
    assert out["collector_identity_admission_implemented"] is True
    assert out["runtime_readiness_admission_implemented"] is True


def test_provider_capability_frontier_is_current_16_of_16():
    m = _load()
    out = m.v2r13_post_admission_reconciliation_contract()
    assert out["provider_capability_frontier_authoritative"] is True
    assert out["current_provider_supported_primitive_count"] == 16
    assert out["current_provider_remaining_unresolved_primitive_count"] == 0
    assert out["current_provider_remaining_unresolved_primitive_names"] == ()
    assert out["provider_capability_complete"] is True


def test_historical_13_3_contract_is_retained_but_not_current_capability():
    m = _load()
    out = m.v2r13_post_admission_reconciliation_contract()
    assert out["historical_live_identity_contract_retained"] is True
    assert out["historical_live_identity_supported_primitive_count"] == 13
    assert out["historical_live_identity_remaining_unresolved_primitive_count"] == 3
    assert out["historical_13_3_not_current_provider_capability"] is True


def test_historical_unresolved_names_are_exact():
    m = _load()
    out = m.v2r13_post_admission_reconciliation_contract()
    assert out["historical_live_identity_remaining_unresolved_primitive_names"] == (
        "endpoint_liveness",
        "model_identity_verified",
        "runtime_image_identity_verified",
    )


def test_supplied_receipt_composition_exists_without_live_backend():
    m = _load()
    out = m.v2r13_post_admission_reconciliation_contract()
    assert out["live_identity_supplied_receipt_composition_implemented"] is True
    assert out["live_collection_backend_implementation_present"] is False


def test_canonical_live_collection_remains_closed():
    m = _load()
    out = m.v2r13_post_admission_reconciliation_contract()
    assert out["canonical_live_collection_path_complete"] is False
    assert out["canonical_collection_enabled"] is False


def test_activation_blockers_are_exact():
    m = _load()
    out = m.v2r13_post_admission_reconciliation_contract()
    assert out["runtime_activation_blockers"] == (
        "V2R13_ACTIVATION_BINDING_NOT_REVIEWED",
        "V2R13_ACTIVE_MODEL_DIGEST_PROBE_NOT_REVIEWED",
        "V2R13_FROZEN_WORKTREE_MATERIALIZER_NOT_REVIEWED",
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["runtime_activation_path_complete"] is False


def test_execution_materialization_blockers_are_exact():
    m = _load()
    out = m.v2r13_post_admission_reconciliation_contract()
    assert out["execution_materialization_blockers"] == (
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
        "CROSS_CONTROL_RUNTIME_SELECTOR_NOT_IMPLEMENTED",
        "COMMAND_MATERIALIZER_NOT_IMPLEMENTED",
        "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
    )
    assert out["execution_materialization_path_complete"] is False


def test_runtime_authority_is_not_only_remaining_gap():
    m = _load()
    out = m.v2r13_post_admission_reconciliation_contract()
    assert out["runtime_execution_authorized"] is False
    assert out["runtime_authority_is_not_only_remaining_gap"] is True


def test_next_gate_is_live_collection_backend_implementation():
    m = _load()
    out = m.v2r13_post_admission_reconciliation_contract()
    assert out["next_gate"] == (
        "V2R13_LIVE_COLLECTION_BACKEND_IMPLEMENTATION_REQUIRED"
    )
    assert out["next_change_class"] == (
        "explicit_authority_read_only_live_collection_backend_composition"
    )


def test_reconciliation_change_requires_no_live_action():
    m = _load()
    out = m.v2r13_post_admission_reconciliation_contract()
    assert out["live_observation_required_for_this_change"] is False
    assert out["runtime_action_required_for_this_change"] is False
    assert out["deployment_required_for_this_change"] is False
    assert out["training_required_for_this_change"] is False
    assert out["funds_action_required_for_this_change"] is False


def test_reconciliation_contract_claims_zero_side_effect_implementations():
    m = _load()
    out = m.v2r13_post_admission_reconciliation_contract()
    for field in (
        "reconciliation_live_observation_implemented",
        "reconciliation_filesystem_observation_implemented",
        "reconciliation_git_query_implemented",
        "reconciliation_subprocess_execution_implemented",
        "reconciliation_network_request_implemented",
        "reconciliation_ollama_request_implemented",
        "reconciliation_docker_command_implemented",
        "reconciliation_service_action_implemented",
        "reconciliation_runtime_start_implemented",
        "reconciliation_model_load_implemented",
        "reconciliation_model_inference_implemented",
        "reconciliation_game_execution_implemented",
        "reconciliation_training_implemented",
        "reconciliation_deployment_implemented",
        "reconciliation_void_chain_mutation_implemented",
        "reconciliation_wallet_or_funds_action_implemented",
    ):
        assert out[field] is False


def test_dependency_activation_descriptor_remains_ineligible():
    m = _load()
    out = m.v2r13_post_admission_reconciliation_contract()
    activation = out["dependency_contracts"]["v2r13_activation_descriptor"]
    assert activation["activation_proven"] is False
    assert activation["eligible"] is False


def test_dependency_execution_descriptors_remain_six_and_ineligible():
    m = _load()
    out = m.v2r13_post_admission_reconciliation_contract()
    rows = out["dependency_contracts"]["v2r13_execution_descriptors"]
    assert len(rows) == 6
    assert all(row["eligible"] is False for row in rows)


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
        "live_identity_implementation.collect_v2r13_live_identity",
        "ollama_binding.collect_bound_ollama_identity",
        "activation_contract.activate_runtime",
    )
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call):
            assert not _dotted(node.func).startswith(forbidden_call_prefixes)


def test_enable_canonical_live_collection_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13PostAdmissionReconciliationHold,
        "V2R13_LIVE_COLLECTION_BACKEND_IMPLEMENTATION_REQUIRED",
        lambda: m.enable_canonical_live_collection(),
    )


def test_authorize_runtime_execution_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13PostAdmissionReconciliationHold,
        "V2R13_COLLECTION_ACTIVATION_AND_EXECUTION_MATERIALIZATION_GAPS_REMAIN",
        lambda: m.authorize_runtime_execution(),
    )
