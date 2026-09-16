from __future__ import annotations

import ast
import hashlib
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_path_inputs_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/abaddon_policy_campaign_runtime_path_inputs_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "94a2d25fdcd76e9d789a6fbdb8d7b20c80d260c0f118dbc82c5a7d430c7c9899"

FORBIDDEN_IMPORT_ROOTS = {
    "os",
    "subprocess",
    "socket",
    "requests",
    "urllib",
    "http",
    "httpx",
    "asyncio",
    "multiprocessing",
    "ctypes",
    "glob",
}
FORBIDDEN_CALLS = {
    "subprocess.run",
    "subprocess.Popen",
    "subprocess.call",
    "subprocess.check_call",
    "subprocess.check_output",
    "os.getenv",
    "os.system",
    "os.popen",
    "Path.exists",
    "Path.is_file",
    "Path.is_dir",
    "Path.resolve",
    "Path.expanduser",
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
        "_void_abaddon_g2_runtime_path_inputs",
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


def _v2_record(m):
    return {
        "schema": m.RECORD_SCHEMA,
        "snapshot_id": m.V2R13,
        "source_kind": m.SOURCE_KIND,
        "frozen_source_root": "/srv/void/g2/v2r13/source",
        "exact_engine_root": "/srv/void/g2/v2r13/engine",
    }


def _v8_record(m):
    return {
        "schema": m.RECORD_SCHEMA,
        "snapshot_id": m.V8,
        "source_kind": m.SOURCE_KIND,
        "model_dir": "/srv/void/g2/v8/model",
        "adapter_dir": "/srv/void/g2/v8/adapter",
    }


def test_static_source_has_no_discovery_or_filesystem_observation_surface():
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


def test_contract_freezes_zero_tracked_sources_and_four_external_paths():
    m = _load()
    out = m.path_input_contract()
    assert out["runtime_count"] == 4
    assert out["tracked_source_defined_path_source_count"] == 0
    assert out["explicit_external_input_runtime_count"] == 2
    assert out["explicit_external_input_path_count"] == 4
    assert out["path_defaults_implemented"] is False
    assert out["path_autodiscovery_implemented"] is False
    assert out["filesystem_observation_implemented"] is False
    assert out["collector_implementation_ready"] is False
    assert out["runtime_execution_authorized"] is False


def test_v14_v10_have_no_generation2_path_input_surface():
    m = _load()
    for snapshot in (m.V14, m.V10):
        req = m.path_input_requirement(snapshot)
        assert req["path_fields"] == ()
        assert req["source_kind"] is None
        assert req["caller_must_supply_all_paths"] is False
        assert req["runtime_readiness_claimed"] is False


def test_v2r13_requires_exact_two_explicit_roots():
    m = _load()
    req = m.path_input_requirement(m.V2R13)
    assert req["source_kind"] == "explicit_external_input"
    assert req["path_fields"] == ("frozen_source_root", "exact_engine_root")
    assert req["tracked_source_defined_default"] is False
    assert req["tracked_source_defined_autodiscovery"] is False
    assert req["caller_must_supply_all_paths"] is True
    assert req["canonical_consumers"] == (
        "openra_env.learning.apollyon_v2r13_portable_checkout.reviewed_path_binding",
        "openra_env.learning.apollyon_v2r13_portable_checkout.PortableRunnerBinding.__init__",
    )


def test_v8_requires_exact_model_and_adapter_paths():
    m = _load()
    req = m.path_input_requirement(m.V8)
    assert req["source_kind"] == "explicit_external_input"
    assert req["path_fields"] == ("model_dir", "adapter_dir")
    assert req["tracked_source_defined_default"] is False
    assert req["tracked_source_defined_autodiscovery"] is False
    assert req["canonical_consumers"] == (
        "openra_env.learning.apollyon_v8_campaign_runtime.verify_v8_runtime_assets",
        "openra_env.learning.apollyon_v8_campaign_runtime.FrozenV8LocalToolRuntime.load",
    )


def test_valid_v2r13_paths_are_shape_valid_but_not_observed():
    m = _load()
    out = m.validate_explicit_path_inputs(m.V2R13, _v2_record(m))
    assert out["path_input_shape_valid"] is True
    assert out["path_source_semantics_admitted"] is True
    assert out["path_existence_verified"] is False
    assert out["path_identity_verified"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False
    assert "PATH_EXISTENCE_NOT_VERIFIED" in out["holds"]


def test_valid_v8_paths_are_shape_valid_but_not_observed():
    m = _load()
    out = m.validate_explicit_path_inputs(m.V8, _v8_record(m))
    assert out["path_input_shape_valid"] is True
    assert out["path_source_semantics_admitted"] is True
    assert out["path_existence_verified"] is False
    assert out["path_identity_verified"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["authority"]["model_weights_loaded"] is False


def test_builder_requires_every_path_and_adds_no_defaults():
    m = _load()
    record = m.build_path_input_record(
        m.V8,
        model_dir="/srv/void/g2/v8/model",
        adapter_dir="/srv/void/g2/v8/adapter",
    )
    assert record == _v8_record(m)
    _expect_hold(
        m.RuntimePathInputHold,
        "caller must supply exactly every required path",
        lambda: m.build_path_input_record(
            m.V8,
            model_dir="/srv/void/g2/v8/model",
        ),
    )


def test_relative_path_holds():
    m = _load()
    record = _v8_record(m)
    record["model_dir"] = "relative/model"
    _expect_hold(
        m.RuntimePathInputHold,
        "model_dir must be absolute",
        lambda: m.validate_explicit_path_inputs(m.V8, record),
    )


def test_tilde_path_holds_without_expansion():
    m = _load()
    record = _v8_record(m)
    record["model_dir"] = "~/models/v8"
    _expect_hold(
        m.RuntimePathInputHold,
        "model_dir may not use tilde expansion",
        lambda: m.validate_explicit_path_inputs(m.V8, record),
    )


def test_parent_traversal_holds():
    m = _load()
    record = _v2_record(m)
    record["frozen_source_root"] = "/srv/void/g2/../source"
    _expect_hold(
        m.RuntimePathInputHold,
        "frozen_source_root may not contain parent traversal",
        lambda: m.validate_explicit_path_inputs(m.V2R13, record),
    )


def test_non_normalized_or_root_path_holds():
    m = _load()
    record = _v8_record(m)
    record["model_dir"] = "/srv//void/g2/v8/model"
    _expect_hold(
        m.RuntimePathInputHold,
        "model_dir must already be lexically normalized",
        lambda: m.validate_explicit_path_inputs(m.V8, record),
    )
    record = _v8_record(m)
    record["model_dir"] = "/"
    _expect_hold(
        m.RuntimePathInputHold,
        "model_dir may not be filesystem root",
        lambda: m.validate_explicit_path_inputs(m.V8, record),
    )


def test_duplicate_runtime_paths_hold():
    m = _load()
    record = _v2_record(m)
    record["exact_engine_root"] = record["frozen_source_root"]
    _expect_hold(
        m.RuntimePathInputHold,
        "runtime path inputs must be distinct",
        lambda: m.validate_explicit_path_inputs(m.V2R13, record),
    )


def test_extra_or_missing_fields_hold():
    m = _load()
    record = _v8_record(m)
    record["extra"] = "/tmp/extra"
    _expect_hold(
        m.RuntimePathInputHold,
        "path-input field set drift",
        lambda: m.validate_explicit_path_inputs(m.V8, record),
    )
    record = _v2_record(m)
    del record["exact_engine_root"]
    _expect_hold(
        m.RuntimePathInputHold,
        "path-input field set drift",
        lambda: m.validate_explicit_path_inputs(m.V2R13, record),
    )


def test_invalid_snapshot_or_promoted_runtime_record_holds():
    m = _load()
    _expect_hold(
        m.RuntimePathInputHold,
        "unsupported reviewed snapshot",
        lambda: m.path_input_requirement("not-reviewed"),
    )
    _expect_hold(
        m.RuntimePathInputHold,
        "runtime does not accept Generation-2 path inputs",
        lambda: m.validate_explicit_path_inputs(
            m.V14,
            {
                "schema": m.RECORD_SCHEMA,
                "snapshot_id": m.V14,
                "source_kind": m.SOURCE_KIND,
            },
        ),
    )


def test_autodiscovery_and_observation_always_hold():
    m = _load()
    _expect_hold(
        m.RuntimePathInputHold,
        "RUNTIME_PATH_AUTODISCOVERY_NOT_IMPLEMENTED",
        lambda: m.discover_path_inputs(),
    )
    _expect_hold(
        m.RuntimePathInputHold,
        "RUNTIME_PATH_OBSERVATION_NOT_IMPLEMENTED",
        lambda: m.observe_path_inputs(),
    )
