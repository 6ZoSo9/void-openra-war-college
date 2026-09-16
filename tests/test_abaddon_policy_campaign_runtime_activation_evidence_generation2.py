from __future__ import annotations

import ast
import hashlib
import importlib.util
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_activation_evidence_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/abaddon_policy_campaign_runtime_activation_evidence_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "c08a53842000343544f7ba63e8ae3bc4d24cb7f771294073caf4ab4a5ddc19a0"
COLLECTOR_SHA = "a" * 64

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
        "_void_abaddon_g2_runtime_activation_evidence",
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


def _common_record(m, snapshot_id):
    req = m.evidence_requirement(snapshot_id)
    return {
        "schema": m.EVIDENCE_SCHEMA,
        "snapshot_id": snapshot_id,
        "snapshot_sha256": req["snapshot_sha256"],
        "runtime_class": req["runtime_class"],
        "evidence_kind": req["evidence_kind"],
        "collector_contract_sha256": COLLECTOR_SHA,
        "observation_mode": "read_only",
        "mutation_performed": False,
        "service_action_performed": False,
        "runtime_start_performed": False,
        "game_execution_performed": False,
        "model_inference_performed": False,
    }


def _external_record(m, snapshot_id):
    req = m.evidence_requirement(snapshot_id)
    expected = req["expected"]
    return {
        **_common_record(m, snapshot_id),
        "endpoint_url": expected["endpoint_url"],
        "endpoint_loopback": True,
        "endpoint_liveness": True,
        "active_model_id": expected["active_model_id"],
        "model_identity_verified": True,
        "active_runtime_unit_sha256": expected["active_runtime_unit_sha256"],
        "runtime_unit_identity_verified": True,
    }


def _v2r13_record(m):
    req = m.evidence_requirement(m.V2R13)
    expected = req["expected"]
    return {
        **_common_record(m, m.V2R13),
        "endpoint_url": expected["endpoint_url"],
        "endpoint_loopback": True,
        "endpoint_liveness": True,
        "active_model_alias": expected["active_model_alias"],
        "active_model_digest": expected["active_model_digest"],
        "model_identity_verified": True,
        "runtime_image_id": expected["runtime_image_id"],
        "runtime_image_identity_verified": True,
        "frozen_source_worktree": {
            "path": "/tmp/void-g2-v2r13-source",
            "exists": True,
            "is_directory": True,
            "is_symlink": False,
            "clean": True,
            "detached": True,
            "head_commit": expected["frozen_war_college_commit"],
            "tree_sha": expected["frozen_war_college_tree"],
        },
        "engine_worktree": {
            "path": "/tmp/void-g2-v2r13-engine",
            "exists": True,
            "is_directory": True,
            "is_symlink": False,
            "clean": True,
            "head_commit": expected["frozen_engine_commit"],
        },
        "portable_binding_attested": True,
    }


def _v8_record(m):
    req = m.evidence_requirement(m.V8)
    expected = req["expected"]
    return {
        **_common_record(m, m.V8),
        "model_dir": "/tmp/void-g2-v8-model",
        "adapter_dir": "/tmp/void-g2-v8-adapter",
        "model_dir_bound": True,
        "adapter_dir_bound": True,
        "tool_runtime_source_sha256": expected["tool_runtime_source_sha256"],
        "tool_runtime_contract_sha256": expected["tool_runtime_contract_sha256"],
        "base_model_revision": expected["base_model_revision"],
        "base_model_config_sha256": expected["base_model_config_sha256"],
        "base_model_shard1_sha256": expected["base_model_shard1_sha256"],
        "base_model_shard2_sha256": expected["base_model_shard2_sha256"],
        "chat_template_sha256": expected["chat_template_sha256"],
        "tokenizer_json_sha256": expected["tokenizer_json_sha256"],
        "runtime_assets_verified": True,
        "runtime_environment_verified": True,
        "offline_only_verified": True,
        "model_weights_loaded": False,
        "load_call_performed": False,
    }


def test_static_source_has_no_direct_collection_or_execution_surface():
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


def test_contract_is_four_runtime_and_collector_absent():
    m = _load()
    out = m.evidence_contract()
    assert out["runtime_count"] == 4
    assert [row["snapshot_id"] for row in out["requirements"]] == [
        m.V14,
        m.V10,
        m.V2R13,
        m.V8,
    ]
    assert out["reviewed_collector_binding_present"] is False
    assert out["collector_implementation_present"] is False
    assert out["endpoint_probe_implemented"] is False
    assert out["service_query_implemented"] is False
    assert out["worktree_discovery_implemented"] is False
    assert out["v8_path_discovery_implemented"] is False
    assert out["runtime_execution_authorized"] is False


def test_v14_v10_evidence_requirements_share_endpoint_but_not_identity():
    m = _load()
    v14 = m.evidence_requirement(m.V14)
    v10 = m.evidence_requirement(m.V10)
    assert v14["expected"]["endpoint_url"] == v10["expected"]["endpoint_url"]
    assert v14["expected"]["active_model_id"] != v10["expected"]["active_model_id"]
    assert (
        v14["expected"]["active_runtime_unit_sha256"]
        != v10["expected"]["active_runtime_unit_sha256"]
    )
    assert v14["collector_binding_reviewed"] is False
    assert v10["collector_binding_reviewed"] is False


def test_valid_v14_shape_is_not_admitted():
    m = _load()
    out = m.validate_evidence_shape(_external_record(m, m.V14))
    assert out["evidence_shape_valid"] is True
    assert out["collector_identity_admitted"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False
    assert "V14_READONLY_ENDPOINT_PROBE_COLLECTOR_NOT_REVIEWED" in out["holds"]


def test_v10_wrong_model_id_holds():
    m = _load()
    record = _external_record(m, m.V10)
    record["active_model_id"] = "wrong-model"
    _expect_hold(
        m.RuntimeActivationEvidenceHold,
        "active model ID drift",
        lambda: m.validate_evidence_shape(record),
    )


def test_external_extra_field_holds():
    m = _load()
    record = _external_record(m, m.V14)
    record["unreviewed_extra"] = True
    _expect_hold(
        m.RuntimeActivationEvidenceHold,
        "evidence field set drift",
        lambda: m.validate_evidence_shape(record),
    )


def test_mutation_claim_holds():
    m = _load()
    record = _external_record(m, m.V14)
    record["mutation_performed"] = True
    _expect_hold(
        m.RuntimeActivationEvidenceHold,
        "crossed authority boundary",
        lambda: m.validate_evidence_shape(record),
    )


def test_v2r13_exact_worktree_shape_is_valid_but_not_admitted():
    m = _load()
    record = _v2r13_record(m)
    out = m.validate_evidence_shape(record)
    assert out["evidence_shape_valid"] is True
    assert out["runtime_readiness_admitted"] is False
    assert "V2R13_FROZEN_WORKTREE_DISCOVERY_COLLECTOR_NOT_REVIEWED" in out["holds"]


def test_v2r13_symlinked_source_holds():
    m = _load()
    record = _v2r13_record(m)
    record["frozen_source_worktree"]["is_symlink"] = True
    _expect_hold(
        m.RuntimeActivationEvidenceHold,
        "frozen source worktree is symlinked",
        lambda: m.validate_evidence_shape(record),
    )


def test_v2r13_source_engine_paths_must_differ():
    m = _load()
    record = _v2r13_record(m)
    record["engine_worktree"]["path"] = record["frozen_source_worktree"]["path"]
    _expect_hold(
        m.RuntimeActivationEvidenceHold,
        "source/engine worktrees must differ",
        lambda: m.validate_evidence_shape(record),
    )


def test_v8_preload_readiness_shape_is_valid_without_loading_weights():
    m = _load()
    record = _v8_record(m)
    out = m.validate_evidence_shape(record)
    assert out["evidence_shape_valid"] is True
    assert out["runtime_readiness_admitted"] is False
    assert record["model_weights_loaded"] is False
    assert record["load_call_performed"] is False
    assert "V8_ASSET_IDENTITY_COLLECTOR_NOT_REVIEWED" in out["holds"]


def test_v8_identity_hash_drift_holds():
    m = _load()
    record = _v8_record(m)
    record["tokenizer_json_sha256"] = "0" * 64
    _expect_hold(
        m.RuntimeActivationEvidenceHold,
        "V8 readiness identity drift: tokenizer_json_sha256",
        lambda: m.validate_evidence_shape(record),
    )


def test_supplied_collector_sha_cannot_bypass_missing_canonical_binding():
    m = _load()
    record = _external_record(m, m.V14)
    _expect_hold(
        m.RuntimeActivationEvidenceHold,
        "no canonical reviewed collector binding is present",
        lambda: m.admit_evidence(
            record,
            reviewed_collector_contract_sha256=COLLECTOR_SHA,
        ),
    )


def test_all_36_arm_requirements_match_runtime_distribution():
    m = _load()
    rows = [
        m.arm_evidence_requirement(pair_slot=slot, arm=arm)
        for slot in range(1, 19)
        for arm in ("baseline", "candidate")
    ]
    assert len(rows) == 36
    assert [row["execution_index"] for row in rows] == list(range(1, 37))
    counts = Counter(row["opponent_snapshot_id"] for row in rows)
    assert counts == {
        m.V14: 12,
        m.V10: 12,
        m.V2R13: 6,
        m.V8: 6,
    }
    assert all(row["evidence_collected"] is False for row in rows)
    assert all(row["evidence_admitted"] is False for row in rows)
    assert all(row["runtime_started"] is False for row in rows)


def test_invalid_snapshot_holds():
    m = _load()
    _expect_hold(
        Exception,
        "unknown snapshot id",
        lambda: m.evidence_requirement("not-reviewed"),
    )


def test_collect_activation_evidence_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeActivationEvidenceHold,
        "ACTIVATION_EVIDENCE_COLLECTOR_NOT_IMPLEMENTED",
        lambda: m.collect_activation_evidence(),
    )
