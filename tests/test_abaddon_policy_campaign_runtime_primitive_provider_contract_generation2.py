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
    "abaddon_policy_campaign_runtime_primitive_provider_contract_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_primitive_provider_contract_generation2.py"
)
EXPECTED_SOURCE_SHA256 = (
    "d28867393c73ae4a570bc97a78a6d16b634f0026cdded6f567ee89aef47369e6"
)
EXPECTED_PROVIDER_CONTRACT_SHA256 = (
    "58e84a058c332de983ccaef19bd1383a92071966b653e699d032c9e9e86c1114"
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


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_primitive_provider_contract",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_semantic_sha_is_exact_and_stable():
    m = _load()
    assert m.provider_contract_sha256() == EXPECTED_PROVIDER_CONTRACT_SHA256
    out = m.validate_provider_contract()
    assert out["provider_contract_sha256"] == EXPECTED_PROVIDER_CONTRACT_SHA256
    assert out["semantic_contract_valid"] is True


def test_manifest_canonical_roundtrip_matches_semantic_sha():
    m = _load()
    manifest = m.provider_contract_manifest()
    canonical = json.dumps(
        manifest,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")
    assert hashlib.sha256(canonical).hexdigest() == EXPECTED_PROVIDER_CONTRACT_SHA256


def test_manifest_hash_changes_when_semantics_change():
    m = _load()
    manifest = deepcopy(m.provider_contract_manifest())
    manifest["canonical_collection_enabled"] = True
    canonical = json.dumps(
        manifest,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")
    assert hashlib.sha256(canonical).hexdigest() != EXPECTED_PROVIDER_CONTRACT_SHA256


def test_exact_canonical_source_blob_bindings():
    m = _load()
    manifest = m.provider_contract_manifest()
    assert manifest["collector_contract_git_blob"] == (
        "8014431ad5329137e5ce12334d19d37c877a0b52"
    )
    assert manifest["collector_implementation_git_blob"] == (
        "0003c24390194a4f621f13c6077e0604b9abcd98"
    )
    assert manifest["runtime_observers_git_blob"] == (
        "cc4774e6aa934764c189cebd4040cd8ea4870517"
    )
    assert manifest["v8_runtime_git_blob"] == (
        "fd0e72767ba199e88af9e9eb2455c03ace027a14"
    )
    assert manifest["primitive_review_git_blob"] == (
        "97e7b11ec4cb4214e7b9764121ec8059371dab51"
    )
    assert manifest["observation_mechanics_git_blob"] == (
        "5fc94c056d1ad7de41b5d7156bce9b3f500f29ba"
    )


def test_snapshot_primitive_counts_are_exact():
    m = _load()
    rows = m.provider_contract_manifest()["snapshots"]
    assert rows[m.V14]["required_primitive_count"] == 9
    assert rows[m.V10]["required_primitive_count"] == 9
    assert rows[m.V2R13]["required_primitive_count"] == 16
    assert rows[m.V8]["required_primitive_count_with_supplied_environment"] == 8
    assert rows[m.V8]["required_primitive_count_without_supplied_environment"] == 9


def test_common_operational_primitive_set_is_exact_six():
    m = _load()
    common = m.provider_contract_manifest()["common_operational_primitives"]
    assert set(common) == {
        "observation_mode",
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "game_execution_performed",
        "model_inference_performed",
    }


def test_common_operational_primitives_are_source_only_self_audits():
    m = _load()
    common = m.provider_contract_manifest()["common_operational_primitives"]
    for name, row in common.items():
        assert row["class"] == "source_only_collector_self_audit", name
        assert row["host_io_required"] is False


def test_common_expected_values_are_exact():
    m = _load()
    common = m.provider_contract_manifest()["common_operational_primitives"]
    assert common["observation_mode"]["expected_value"] == "read_only"
    for name in (
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "game_execution_performed",
        "model_inference_performed",
    ):
        assert common[name]["expected_value"] is False


def test_v14_live_identity_channels_remain_unresolved():
    m = _load()
    assert m.primitive_contract(m.V14, "endpoint_liveness")[
        "canonical_route_present"
    ] is False
    model = m.primitive_contract(m.V14, "model_identity_verified")
    assert model["canonical_route_present"] is False
    assert model["inference_endpoint_is_identity_probe"] is False
    unit = m.primitive_contract(m.V14, "runtime_unit_identity_verified")
    assert unit["canonical_route_present"] is False
    assert unit["generic_designated_host_discovery_admitted"] is False


def test_v10_live_identity_channels_remain_unresolved():
    m = _load()
    assert m.primitive_contract(m.V10, "endpoint_liveness")[
        "canonical_route_present"
    ] is False
    model = m.primitive_contract(m.V10, "model_identity_verified")
    assert model["canonical_route_present"] is False
    assert model["inference_endpoint_is_identity_probe"] is False
    unit = m.primitive_contract(m.V10, "runtime_unit_identity_verified")
    assert unit["canonical_route_present"] is False


def test_loopback_liveness_contract_forbids_model_inference():
    m = _load()
    for snapshot_id in (m.V14, m.V10, m.V2R13):
        row = m.primitive_contract(snapshot_id, "endpoint_liveness")
        assert row["class"] == "unresolved_read_only_liveness_probe"
        assert row["model_inference_permitted"] is False
        assert row["canonical_route_present"] is False


def test_v2r13_live_model_and_image_identity_remain_unresolved():
    m = _load()
    model = m.primitive_contract(m.V2R13, "model_identity_verified")
    assert model["class"] == "unresolved_live_model_digest_identity_channel"
    assert model["inference_endpoint_is_identity_probe"] is False
    assert model["canonical_route_present"] is False
    image = m.primitive_contract(
        m.V2R13,
        "runtime_image_identity_verified",
    )
    assert image["class"] == "unresolved_runtime_image_identity_channel"
    assert image["canonical_route_present"] is False


def test_v2r13_six_path_leaves_require_reviewed_observer_adapter():
    m = _load()
    leaves = (
        "frozen_source_worktree.exists",
        "frozen_source_worktree.is_directory",
        "frozen_source_worktree.is_symlink",
        "engine_worktree.exists",
        "engine_worktree.is_directory",
        "engine_worktree.is_symlink",
    )
    for leaf in leaves:
        row = m.primitive_contract(m.V2R13, leaf)
        assert row["class"] == "reviewed_v2r13_observer_adapter_required"
        assert row["host_io_required"] is False
        assert row["reviewed_observer_function"] == "observe_v2r13_git_identity"
        assert row["reviewed_observer_git_blob"] == (
            "cc4774e6aa934764c189cebd4040cd8ea4870517"
        )
        assert row["adapter_implementation_present"] is False


def test_v2r13_portable_binding_attestation_stays_unimplemented():
    m = _load()
    row = m.primitive_contract(m.V2R13, "portable_binding_attested")
    assert row["class"] == (
        "unresolved_portable_binding_attestation_composition"
    )
    assert row["host_io_required"] is False
    assert row["reviewed_git_observer_present"] is True
    assert row["reviewed_static_contract_present"] is True
    assert row["attestation_composition_implemented"] is False


def test_v8_environment_pure_validator_is_reusable_only_for_supplied_facts():
    m = _load()
    row = m.primitive_contract(m.V8, "runtime_environment_verified")
    assert row["class"] == (
        "supplied_fact_validator_or_unreviewed_live_collection"
    )
    assert row["pure_validator_function"] == "validate_v8_runtime_environment"
    assert row["pure_validator_git_blob"] == (
        "fd0e72767ba199e88af9e9eb2455c03ace027a14"
    )
    assert row["pure_validator_direct_reuse_admitted"] is True
    assert row["live_collector_function"] == "verify_v8_runtime_environment"
    assert row["live_collection_reviewed"] is False


def test_v8_offline_only_attestation_remains_unresolved():
    m = _load()
    row = m.primitive_contract(m.V8, "offline_only_verified")
    assert row["class"] == "unresolved_offline_only_attestation"
    assert row["host_io_required"] is True
    assert row["canonical_route_present"] is False


def test_v8_load_call_is_source_only_self_audit_false():
    m = _load()
    row = m.primitive_contract(m.V8, "load_call_performed")
    assert row["class"] == "source_only_collector_self_audit"
    assert row["expected_value"] is False
    assert row["host_io_required"] is False
    assert row["model_load_permitted"] is False


def test_canonical_collector_implementation_stays_disabled():
    m = _load()
    out = m.collector_implementation.collector_implementation_contract()
    assert out["canonical_primitive_source_bindings_present"] is False
    assert out["canonical_collection_enabled"] is False
    assert out["reviewed_collector_binding_present"] is False
    assert out["runtime_readiness_admission_implemented"] is False
    assert out["runtime_execution_authorized"] is False


def test_canonical_collector_contract_stays_unadmitted():
    m = _load()
    out = m.collector_contract.validate_collector_contract()
    assert out["reviewed_collector_binding_present"] is False
    assert out["collector_binding_activation"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_validated_provider_contract_never_claims_execution_or_admission():
    m = _load()
    out = m.validate_provider_contract()
    assert out["canonical_provider_bindings_present"] is False
    assert out["canonical_collection_enabled"] is False
    assert out["reviewed_collector_binding_present"] is False
    assert out["runtime_readiness_admission_enabled"] is False
    assert out["live_observation_performed"] is False
    assert out["provider_execution_performed"] is False
    assert out["runtime_execution_authorized"] is False


def test_static_source_has_no_host_io_imports_or_calls():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    forbidden_import_roots = {
        "os",
        "subprocess",
        "socket",
        "requests",
        "urllib",
        "http",
        "httpx",
        "pathlib",
        "asyncio",
        "multiprocessing",
        "ctypes",
    }
    forbidden_call_fragments = {
        "observe_v2r13_git_identity",
        "observe_v8_assets",
        "verify_v8_runtime_environment",
        "host_git_runner",
        "host_file_observation_backend",
        "systemctl",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call):
            name = _dotted(node.func)
            assert not any(fragment in name for fragment in forbidden_call_fragments)


def test_unknown_snapshot_is_rejected():
    m = _load()
    _expect_hold(
        m.RuntimePrimitiveProviderContractHold,
        "unsupported provider snapshot",
        lambda: m.primitive_contract("not-reviewed", "observation_mode"),
    )


def test_unknown_primitive_is_rejected():
    m = _load()
    _expect_hold(
        m.RuntimePrimitiveProviderContractHold,
        "unknown provider primitive",
        lambda: m.primitive_contract(m.V14, "not-a-primitive"),
    )


def test_collection_entrypoint_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimePrimitiveProviderContractHold,
        "GENERATION2_CANONICAL_PRIMITIVE_PROVIDERS_NOT_IMPLEMENTED",
        lambda: m.collect_provider_evidence(),
    )
