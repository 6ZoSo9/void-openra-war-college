from __future__ import annotations

import ast
import hashlib
import importlib.util
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_observation_mechanics_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/abaddon_policy_campaign_runtime_observation_mechanics_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "c2e97a753152630c20e04e1e435199e1b5b29731f6a68d0c1180a857bd685211"

FORBIDDEN_IMPORT_ROOTS = {
    "subprocess",
    "socket",
    "requests",
    "urllib",
    "http",
    "httpx",
    "asyncio",
    "multiprocessing",
    "ctypes",
}
FORBIDDEN_CALLS = {
    "subprocess.run",
    "subprocess.Popen",
    "subprocess.call",
    "subprocess.check_call",
    "subprocess.check_output",
    "os.system",
    "os.popen",
}


def _expect_hold(exc_type, pattern, fn):
    try:
        fn()
    except exc_type as exc:
        assert pattern in str(exc), (pattern, str(exc))
    else:
        raise AssertionError(f"expected {exc_type.__name__}: {pattern}")


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_runtime_observation_mechanics",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def test_static_source_has_no_direct_observation_or_execution_surface():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in FORBIDDEN_IMPORT_ROOTS
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".", 1)[0]
            assert root not in FORBIDDEN_IMPORT_ROOTS
        elif isinstance(node, ast.Call):
            assert _dotted(node.func) not in FORBIDDEN_CALLS


def test_contract_has_exact_four_runtime_mechanics_and_no_collector():
    m = _load()
    out = m.observation_mechanics_contract()
    assert out["runtime_count"] == 4
    assert [row["snapshot_id"] for row in out["mechanics"]] == [
        m.V14,
        m.V10,
        m.V2R13,
        m.V8,
    ]
    assert out["canonical_source_defined_api_path_count"] == 0
    assert out["chat_completions_urls_are_identity_probe_routes"] is False
    assert out["generic_designated_host_discovery_is_apollyon_identity_proof"] is False
    assert out["collector_implementation_present"] is False
    assert out["collector_implementation_ready"] is False
    assert out["runtime_execution_authorized"] is False


def test_v14_v10_do_not_reinterpret_inference_endpoint_as_identity_probe():
    m = _load()
    v14 = m.observation_mechanics(m.V14)
    v10 = m.observation_mechanics(m.V10)
    assert v14["mechanic_class"] == "unresolved_promoted_loopback_identity_channel"
    assert v10["mechanic_class"] == "unresolved_promoted_loopback_identity_channel"
    assert (
        v14["known_inference_surface"]["chat_completions_url"]
        == v10["known_inference_surface"]["chat_completions_url"]
    )
    assert v14["known_inference_surface"]["identity_probe_route"] is False
    assert v10["known_inference_surface"]["identity_probe_route"] is False
    assert v14["known_inference_surface"]["identity_probe_may_reuse_inference_request"] is False
    assert v10["known_inference_surface"]["identity_probe_may_reuse_inference_request"] is False
    assert v14["canonical_source_defined_identity_route"] is False
    assert v10["canonical_source_defined_identity_route"] is False


def test_v14_v10_preserve_distinct_exact_identities():
    m = _load()
    v14 = m.observation_mechanics(m.V14)
    v10 = m.observation_mechanics(m.V10)
    assert v14["expected_identity"]["model_id"] != v10["expected_identity"]["model_id"]
    assert (
        v14["expected_identity"]["active_runtime_unit_sha256"]
        != v10["expected_identity"]["active_runtime_unit_sha256"]
    )


def test_generic_systemd_discovery_not_admissible_for_v14_v10_identity():
    m = _load()
    for snapshot in (m.V14, m.V10):
        row = m.observation_mechanics(snapshot)
        assert row["generic_designated_host_systemd_discovery_admissible"] is False
        assert row["runtime_specific_service_name_defined"] is False
        assert row["collector_implementation_ready"] is False


def test_v2r13_uses_only_preexisting_explicit_path_binding_surface():
    m = _load()
    row = m.observation_mechanics(m.V2R13)
    binding = row["preexisting_path_binding"]
    assert row["mechanic_class"] == "split_preexisting_path_and_unresolved_live_identity"
    assert binding["canonical_function"] == m.V2R13_PATH_BINDER
    assert binding["canonical_source_sha256"] == m.V2R13_PORTABLE_SOURCE_SHA256
    assert binding["explicit_frozen_source_root_required"] is True
    assert binding["explicit_exact_engine_root_required"] is True
    assert binding["source_engine_roots_must_differ"] is True
    assert binding["creates_worktrees"] is False
    assert binding["mutates_canonical_checkout"] is False


def test_v2r13_live_model_identity_channel_remains_unresolved():
    m = _load()
    row = m.observation_mechanics(m.V2R13)
    live = row["live_runtime_identity"]
    assert live["canonical_source_defined_identity_route"] is False
    assert row["git_metadata_observation_implementation_present"] is False
    assert row["worktree_materializer_present"] is False
    assert row["live_model_identity_observation_implementation_present"] is False
    assert row["collector_implementation_ready"] is False


def test_v8_asset_verifier_is_preload_only():
    m = _load()
    row = m.observation_mechanics(m.V8)
    asset = row["asset_observation"]
    assert row["mechanic_class"] == "local_preload_verification_with_unbound_paths"
    assert asset["canonical_function"] == m.V8_ASSET_VERIFIER
    assert asset["canonical_source_sha256"] == m.V8_RUNTIME_SOURCE_SHA256
    assert asset["model_dir_input_required"] is True
    assert asset["adapter_dir_input_required"] is True
    assert asset["preexisting_paths_required"] is True
    assert asset["exact_file_hash_verification"] is True
    assert asset["verified_file_count"] == 17
    assert asset["loads_model_weights"] is False
    assert asset["performs_model_inference"] is False
    assert asset["collector_invocation_implemented"] is False


def test_v8_environment_pure_validator_separated_from_live_pip_freeze():
    m = _load()
    row = m.observation_mechanics(m.V8)
    env = row["environment_observation"]
    assert env["pure_validator_function"] == m.V8_ENVIRONMENT_VALIDATOR
    assert env["live_verifier_function"] == m.V8_LIVE_ENVIRONMENT_VERIFIER
    assert env["pure_validator_inputs"] == (
        "python_major_minor",
        "pip_freeze_sha256",
    )
    assert env["live_verifier_executes_pip_freeze"] is True
    assert env["live_verifier_collector_invocation_implemented"] is False


def test_v8_model_loader_is_explicitly_outside_readiness_collection():
    m = _load()
    row = m.observation_mechanics(m.V8)
    boundary = row["load_boundary"]
    assert boundary["canonical_function"] == m.V8_MODEL_LOADER
    assert boundary["admissible_for_readiness_collection"] is False
    assert boundary["loads_model_weights"] is True
    assert boundary["must_remain_uninvoked"] is True


def test_v8_path_sources_remain_unresolved():
    m = _load()
    row = m.observation_mechanics(m.V8)
    paths = row["path_binding"]
    assert paths["model_dir_source_defined"] is False
    assert paths["adapter_dir_source_defined"] is False
    assert paths["explicit_preexisting_paths_required"] is True
    assert row["collector_implementation_ready"] is False


def test_all_mechanics_preserve_runtime_authority_false():
    m = _load()
    for row in m.observation_mechanics_contract()["mechanics"]:
        assert row["authority"]["observation_performed"] is False
        assert row["authority"]["endpoint_probe_performed"] is False
        assert row["authority"]["systemd_query_performed"] is False
        assert row["authority"]["subprocess_execution_performed"] is False
        assert row["authority"]["worktree_created"] is False
        assert row["authority"]["model_weights_loaded"] is False
        assert row["authority"]["runtime_started"] is False
        assert row["authority"]["runtime_execution_authorized"] is False


def test_collector_build_requests_all_hold():
    m = _load()
    rows = [m.collector_build_request(s) for s in (m.V14, m.V10, m.V2R13, m.V8)]
    assert len(rows) == 4
    assert all(row["collector_implementation_present"] is False for row in rows)
    assert all(row["collector_implementation_ready"] is False for row in rows)
    assert all(row["eligible"] is False for row in rows)
    assert all(m.RUNTIME_AUTHORITY_BLOCKER in row["reasons"] for row in rows)


def test_mechanic_classes_are_intentionally_split():
    m = _load()
    rows = [m.observation_mechanics(s) for s in (m.V14, m.V10, m.V2R13, m.V8)]
    counts = Counter(row["mechanic_class"] for row in rows)
    assert counts == {
        "unresolved_promoted_loopback_identity_channel": 2,
        "split_preexisting_path_and_unresolved_live_identity": 1,
        "local_preload_verification_with_unbound_paths": 1,
    }


def test_invalid_snapshot_holds():
    m = _load()
    _expect_hold(
        m.RuntimeObservationMechanicsHold,
        "unsupported reviewed snapshot",
        lambda: m.observation_mechanics("not-reviewed"),
    )


def test_collect_runtime_identity_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeObservationMechanicsHold,
        "RUNTIME_IDENTITY_OBSERVATION_NOT_IMPLEMENTED",
        lambda: m.collect_runtime_identity(),
    )
