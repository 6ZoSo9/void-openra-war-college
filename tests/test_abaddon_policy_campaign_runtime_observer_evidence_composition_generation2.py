from __future__ import annotations

import ast
import hashlib
import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_observer_evidence_composition_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_observer_evidence_composition_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "dbadd47bd5bf7354754220505857e881b9dea52989569d65669d90415cff0d9d"


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
        "_void_abaddon_g2_observer_evidence_composition",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _v8_paths(m):
    return {
        "schema": "void.abaddon.generation2.runtime-path-input-record.v1",
        "snapshot_id": m.V8,
        "source_kind": "explicit_external_input",
        "model_dir": "/srv/void/g2/v8/model",
        "adapter_dir": "/srv/void/g2/v8/adapter",
    }


def _v2_paths(m):
    return {
        "schema": "void.abaddon.generation2.runtime-path-input-record.v1",
        "snapshot_id": m.V2R13,
        "source_kind": "explicit_external_input",
        "frozen_source_root": "/srv/void/g2/v2r13/source",
        "exact_engine_root": "/srv/void/g2/v2r13/engine",
    }


def _identity(m, size):
    return {
        "st_dev": 2050,
        "st_ino": 11,
        "st_size": size,
        "st_mtime_ns": 13,
        "st_ctime_ns": 17,
        "st_mode": 0o100400,
        "st_nlink": 1,
    }


def _v8_receipt(m):
    paths = _v8_paths(m)
    assets = []
    for index, spec in enumerate(m.observers.V8_ASSET_SPECS, start=1):
        size = index
        root = paths[spec.root_field]
        assets.append(
            {
                "label": spec.label,
                "root_field": spec.root_field,
                "relative_path": spec.relative_path,
                "observation": {
                    "schema": m.observers.FILE_OBSERVATION_SCHEMA,
                    "path": f"{root}/{spec.relative_path}",
                    "expected_sha256": spec.expected_sha256,
                    "actual_sha256": spec.expected_sha256,
                    "byte_count": size,
                    "maximum_bytes": spec.maximum_bytes,
                    "identity": _identity(m, size),
                    "generation_stable": True,
                    "regular_file": True,
                    "symlink_followed": False,
                    "runtime_execution_performed": False,
                    "model_execution_performed": False,
                },
            }
        )
    return {
        "schema": m.observers.V8_OBSERVATION_SCHEMA,
        "snapshot_id": m.V8,
        "asset_count": 17,
        "assets": assets,
        "all_assets_verified": True,
        "model_weights_loaded": False,
        "runtime_started": False,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_execution_performed": False,
    }


def _v2_receipt(m):
    paths = _v2_paths(m)
    return {
        "schema": m.observers.V2R13_OBSERVATION_SCHEMA,
        "snapshot_id": m.V2R13,
        "source_root": paths["frozen_source_root"],
        "engine_root": paths["exact_engine_root"],
        "source_head_commit": m.observers.FROZEN_WAR_COLLEGE_COMMIT,
        "source_head_tree": m.observers.FROZEN_WAR_COLLEGE_TREE,
        "source_worktree_clean": True,
        "source_detached_head": True,
        "engine_head_commit": m.observers.FROZEN_ENGINE_COMMIT,
        "engine_worktree_clean": True,
        "worktree_created": False,
        "checkout_mutation_performed": False,
        "runtime_execution_performed": False,
        "model_execution_performed": False,
        "game_execution_performed": False,
    }


def test_contract_is_pure_partial_composition_only():
    m = _load()
    out = m.observer_evidence_composition_contract()
    assert out["supported_snapshot_ids"] == (m.V2R13, m.V8)
    assert out["promoted_loopback_snapshot_ids_unresolved"] == (m.V14, m.V10)
    assert out["observer_record_validation_implemented"] is True
    assert out["partial_fragment_composition_implemented"] is True
    assert out["final_activation_evidence_shape_composition_implemented"] is False
    assert out["collector_identity_admission_implemented"] is False
    assert out["live_observation_performed"] is False
    assert out["runtime_execution_authorized"] is False


def test_static_source_has_no_collection_or_host_backend_calls():
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
    }
    forbidden_calls = {
        "observers.observe_v8_assets",
        "observers.observe_v2r13_git_identity",
        "observers.observe_exact_regular_file",
        "observers.host_file_observation_backend",
        "observers.host_git_runner",
        "observers.host_path_resolver",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call):
            assert _dotted(node.func) not in forbidden_calls


def test_v8_valid_receipt_is_shape_valid_but_not_admitted():
    m = _load()
    out = m.validate_v8_asset_observer_record(
        _v8_receipt(m),
        path_input_record=_v8_paths(m),
    )
    assert out["observer_record_valid"] is True
    assert out["path_binding_verified"] is True
    assert out["asset_identity_verified"] is True
    assert out["asset_count"] == 17
    assert out["observation_performed_by_validator"] is False
    assert out["collector_identity_admitted"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_v8_fragment_is_partial_and_does_not_invent_environment_evidence():
    m = _load()
    out = m.compose_observer_evidence_fragment(
        m.V8,
        _v8_receipt(m),
        path_input_record=_v8_paths(m),
    )
    fields = out["supported_activation_evidence_fields"]
    assert fields == {
        "model_dir": "/srv/void/g2/v8/model",
        "adapter_dir": "/srv/void/g2/v8/adapter",
        "model_dir_bound": True,
        "adapter_dir_bound": True,
        "runtime_assets_verified": True,
        "model_weights_loaded": False,
    }
    assert "runtime_environment_verified" in out["unresolved_activation_evidence_fields"]
    assert "offline_only_verified" in out["unresolved_activation_evidence_fields"]
    assert "load_call_performed" in out["unresolved_activation_evidence_fields"]
    assert out["activation_evidence_shape_complete"] is False
    assert out["runtime_readiness_admitted"] is False


def test_v8_rejects_asset_count_drift():
    m = _load()
    record = _v8_receipt(m)
    record["asset_count"] = 16
    _expect_hold(
        m.RuntimeObserverEvidenceCompositionHold,
        "V8 observer asset count drift",
        lambda: m.validate_v8_asset_observer_record(
            record,
            path_input_record=_v8_paths(m),
        ),
    )


def test_v8_rejects_asset_path_binding_drift():
    m = _load()
    record = _v8_receipt(m)
    record["assets"][0]["observation"]["path"] = "/wrong/config.json"
    _expect_hold(
        m.RuntimeObserverEvidenceCompositionHold,
        "V8 file path binding drift",
        lambda: m.validate_v8_asset_observer_record(
            record,
            path_input_record=_v8_paths(m),
        ),
    )


def test_v8_rejects_hash_drift():
    m = _load()
    record = _v8_receipt(m)
    record["assets"][0]["observation"]["actual_sha256"] = "0" * 64
    _expect_hold(
        m.RuntimeObserverEvidenceCompositionHold,
        "V8 actual SHA-256 drift",
        lambda: m.validate_v8_asset_observer_record(
            record,
            path_input_record=_v8_paths(m),
        ),
    )


def test_v8_rejects_generation_or_symlink_drift():
    m = _load()
    record = _v8_receipt(m)
    record["assets"][0]["observation"]["generation_stable"] = False
    _expect_hold(
        m.RuntimeObserverEvidenceCompositionHold,
        "V8 file generation unstable",
        lambda: m.validate_v8_asset_observer_record(
            record,
            path_input_record=_v8_paths(m),
        ),
    )

    record = _v8_receipt(m)
    record["assets"][0]["observation"]["symlink_followed"] = True
    _expect_hold(
        m.RuntimeObserverEvidenceCompositionHold,
        "V8 asset followed symlink",
        lambda: m.validate_v8_asset_observer_record(
            record,
            path_input_record=_v8_paths(m),
        ),
    )


def test_v8_rejects_identity_size_drift():
    m = _load()
    record = _v8_receipt(m)
    record["assets"][0]["observation"]["identity"]["st_size"] += 1
    _expect_hold(
        m.RuntimeObserverEvidenceCompositionHold,
        "V8 file identity size/byte_count drift",
        lambda: m.validate_v8_asset_observer_record(
            record,
            path_input_record=_v8_paths(m),
        ),
    )


def test_v8_rejects_authority_boundary_crossing():
    m = _load()
    record = _v8_receipt(m)
    record["model_weights_loaded"] = True
    _expect_hold(
        m.RuntimeObserverEvidenceCompositionHold,
        "observer record crossed authority boundary: model_weights_loaded",
        lambda: m.validate_v8_asset_observer_record(
            record,
            path_input_record=_v8_paths(m),
        ),
    )


def test_v2r13_valid_receipt_is_shape_valid_but_not_admitted():
    m = _load()
    out = m.validate_v2r13_git_observer_record(
        _v2_receipt(m),
        path_input_record=_v2_paths(m),
    )
    assert out["observer_record_valid"] is True
    assert out["path_binding_verified"] is True
    assert out["git_identity_verified"] is True
    assert out["observation_performed_by_validator"] is False
    assert out["collector_identity_admitted"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["runtime_execution_authorized"] is False


def test_v2r13_fragment_is_partial_and_does_not_invent_path_classification():
    m = _load()
    out = m.compose_observer_evidence_fragment(
        m.V2R13,
        _v2_receipt(m),
        path_input_record=_v2_paths(m),
    )
    fields = out["supported_activation_evidence_fields"]
    assert fields["frozen_source_worktree"] == {
        "path": "/srv/void/g2/v2r13/source",
        "clean": True,
        "detached": True,
        "head_commit": m.observers.FROZEN_WAR_COLLEGE_COMMIT,
        "tree_sha": m.observers.FROZEN_WAR_COLLEGE_TREE,
    }
    assert fields["engine_worktree"] == {
        "path": "/srv/void/g2/v2r13/engine",
        "clean": True,
        "head_commit": m.observers.FROZEN_ENGINE_COMMIT,
    }
    unresolved = out["unresolved_activation_evidence_fields"]
    assert "frozen_source_worktree.exists" in unresolved
    assert "frozen_source_worktree.is_directory" in unresolved
    assert "frozen_source_worktree.is_symlink" in unresolved
    assert "engine_worktree.exists" in unresolved
    assert out["activation_evidence_shape_complete"] is False


def test_v2r13_rejects_path_binding_drift():
    m = _load()
    record = _v2_receipt(m)
    record["source_root"] = "/wrong/source"
    _expect_hold(
        m.RuntimeObserverEvidenceCompositionHold,
        "V2R13 source path binding drift",
        lambda: m.validate_v2r13_git_observer_record(
            record,
            path_input_record=_v2_paths(m),
        ),
    )


def test_v2r13_rejects_source_commit_or_tree_drift():
    m = _load()
    record = _v2_receipt(m)
    record["source_head_commit"] = "0" * 40
    _expect_hold(
        m.RuntimeObserverEvidenceCompositionHold,
        "V2R13 source HEAD drift",
        lambda: m.validate_v2r13_git_observer_record(
            record,
            path_input_record=_v2_paths(m),
        ),
    )

    record = _v2_receipt(m)
    record["source_head_tree"] = "0" * 40
    _expect_hold(
        m.RuntimeObserverEvidenceCompositionHold,
        "V2R13 source tree drift",
        lambda: m.validate_v2r13_git_observer_record(
            record,
            path_input_record=_v2_paths(m),
        ),
    )


def test_v2r13_rejects_dirty_or_attached_source():
    m = _load()
    record = _v2_receipt(m)
    record["source_worktree_clean"] = False
    _expect_hold(
        m.RuntimeObserverEvidenceCompositionHold,
        "V2R13 source worktree dirty",
        lambda: m.validate_v2r13_git_observer_record(
            record,
            path_input_record=_v2_paths(m),
        ),
    )

    record = _v2_receipt(m)
    record["source_detached_head"] = False
    _expect_hold(
        m.RuntimeObserverEvidenceCompositionHold,
        "V2R13 source HEAD is not detached",
        lambda: m.validate_v2r13_git_observer_record(
            record,
            path_input_record=_v2_paths(m),
        ),
    )


def test_v2r13_rejects_engine_identity_drift():
    m = _load()
    record = _v2_receipt(m)
    record["engine_head_commit"] = "0" * 40
    _expect_hold(
        m.RuntimeObserverEvidenceCompositionHold,
        "V2R13 engine HEAD drift",
        lambda: m.validate_v2r13_git_observer_record(
            record,
            path_input_record=_v2_paths(m),
        ),
    )


def test_v2r13_rejects_authority_boundary_crossing():
    m = _load()
    record = _v2_receipt(m)
    record["checkout_mutation_performed"] = True
    _expect_hold(
        m.RuntimeObserverEvidenceCompositionHold,
        "observer record crossed authority boundary: checkout_mutation_performed",
        lambda: m.validate_v2r13_git_observer_record(
            record,
            path_input_record=_v2_paths(m),
        ),
    )


def test_promoted_loopback_snapshots_remain_unimplemented():
    m = _load()
    for snapshot_id in (m.V14, m.V10):
        _expect_hold(
            m.RuntimeObserverEvidenceCompositionHold,
            "GENERATION2_PROMOTED_LOOPBACK_OBSERVER_NOT_IMPLEMENTED",
            lambda snapshot_id=snapshot_id: m.validate_observer_record(
                snapshot_id,
                {},
                path_input_record={},
            ),
        )


def test_collection_entrypoint_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeObserverEvidenceCompositionHold,
        "GENERATION2_OBSERVER_EVIDENCE_COLLECTION_NOT_IMPLEMENTED",
        lambda: m.collect_or_observe_runtime_evidence(),
    )


def test_fragments_never_claim_collector_or_runtime_admission():
    m = _load()
    cases = (
        (m.V8, _v8_receipt(m), _v8_paths(m)),
        (m.V2R13, _v2_receipt(m), _v2_paths(m)),
    )
    for snapshot_id, record, paths in cases:
        out = m.compose_observer_evidence_fragment(
            snapshot_id,
            record,
            path_input_record=paths,
        )
        assert out["collector_identity_admitted"] is False
        assert out["runtime_readiness_admitted"] is False
        assert out["observation_performed_by_composer"] is False
        assert out["runtime_selection_performed"] is False
        assert out["runtime_started"] is False
        assert out["runtime_execution_authorized"] is False
