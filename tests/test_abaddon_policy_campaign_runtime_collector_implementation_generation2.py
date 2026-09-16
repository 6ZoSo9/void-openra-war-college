from __future__ import annotations

import ast
import hashlib
import importlib.util
import sys
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_collector_implementation_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_collector_implementation_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "91e094c71b838ad8116dced00fbc50b3e8a8bd138f75dfb5ae86b9bf5c97a8dc"


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
        "_void_abaddon_g2_collector_implementation",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _source_sha(name):
    return hashlib.sha256(("primitive:" + name).encode("utf-8")).hexdigest()


def _bindings(m, snapshot_id, *, supplied_environment_identity=True):
    return {
        name: _source_sha(name)
        for name in m.required_primitive_names(
            snapshot_id,
            supplied_environment_identity=supplied_environment_identity,
        )
    }


def _primitive_value(name):
    if name == "observation_mode":
        return "read_only"
    if name in {
        "mutation_performed",
        "service_action_performed",
        "runtime_start_performed",
        "game_execution_performed",
        "model_inference_performed",
        "load_call_performed",
    }:
        return False
    if name.endswith(".is_symlink"):
        return False
    if name in {
        "endpoint_liveness",
        "model_identity_verified",
        "runtime_unit_identity_verified",
        "runtime_image_identity_verified",
        "portable_binding_attested",
        "runtime_environment_verified",
        "offline_only_verified",
    }:
        return True
    if name.endswith(".exists") or name.endswith(".is_directory"):
        return True
    raise AssertionError(f"unhandled primitive {name}")


def _provider(bindings, *, mutation_override=None):
    def provider(snapshot_id, primitive_name):
        source_sha = bindings[primitive_name]
        record = {
            "schema": (
                "void.abaddon.generation2.runtime-collector-primitive-receipt.v1"
            ),
            "snapshot_id": snapshot_id,
            "primitive_name": primitive_name,
            "source_sha256": source_sha,
            "observation_mode": "read_only",
            "value": _primitive_value(primitive_name),
            "mutation_performed": False,
            "service_action_performed": False,
            "runtime_start_performed": False,
            "game_execution_performed": False,
            "model_inference_performed": False,
        }
        if mutation_override is not None and primitive_name == mutation_override:
            record["mutation_performed"] = True
        return record
    return provider


def _base(m, snapshot_id, *, supplied_environment_identity=True):
    req = m.activation_evidence.evidence_requirement(snapshot_id)
    expected = req["expected"]
    base = {
        "schema": m.activation_evidence.EVIDENCE_SCHEMA,
        "snapshot_id": req["snapshot_id"],
        "snapshot_sha256": req["snapshot_sha256"],
        "runtime_class": req["runtime_class"],
        "evidence_kind": req["evidence_kind"],
    }

    if snapshot_id in {m.V14, m.V10}:
        base.update(
            {
                "endpoint_url": expected["endpoint_url"],
                "endpoint_loopback": True,
                "active_model_id": expected["active_model_id"],
                "active_runtime_unit_sha256": expected[
                    "active_runtime_unit_sha256"
                ],
            }
        )
        return base

    if snapshot_id == m.V2R13:
        base.update(
            {
                "endpoint_url": expected["endpoint_url"],
                "endpoint_loopback": True,
                "active_model_alias": expected["active_model_alias"],
                "active_model_digest": expected["active_model_digest"],
                "runtime_image_id": expected["runtime_image_id"],
                "frozen_source_worktree": {
                    "path": "/srv/void/g2/v2r13/source",
                    "clean": True,
                    "detached": True,
                    "head_commit": expected["frozen_war_college_commit"],
                    "tree_sha": expected["frozen_war_college_tree"],
                },
                "engine_worktree": {
                    "path": "/srv/void/g2/v2r13/engine",
                    "clean": True,
                    "head_commit": expected["frozen_engine_commit"],
                },
            }
        )
        return base

    assert snapshot_id == m.V8
    base.update(
        {
            "model_dir": "/srv/void/g2/v8/model",
            "adapter_dir": "/srv/void/g2/v8/adapter",
            "model_dir_bound": True,
            "adapter_dir_bound": True,
            "tool_runtime_source_sha256": expected[
                "tool_runtime_source_sha256"
            ],
            "tool_runtime_contract_sha256": expected[
                "tool_runtime_contract_sha256"
            ],
            "base_model_revision": expected["base_model_revision"],
            "base_model_config_sha256": expected[
                "base_model_config_sha256"
            ],
            "base_model_shard1_sha256": expected[
                "base_model_shard1_sha256"
            ],
            "base_model_shard2_sha256": expected[
                "base_model_shard2_sha256"
            ],
            "chat_template_sha256": expected["chat_template_sha256"],
            "tokenizer_json_sha256": expected["tokenizer_json_sha256"],
            "runtime_assets_verified": True,
            "model_weights_loaded": False,
        }
    )
    if supplied_environment_identity:
        base["runtime_environment_verified"] = True
    return base


def _collect(m, snapshot_id, *, supplied_environment_identity=True):
    bindings = _bindings(
        m,
        snapshot_id,
        supplied_environment_identity=supplied_environment_identity,
    )
    return m.collect_candidate_with_provider(
        snapshot_id,
        _base(
            m,
            snapshot_id,
            supplied_environment_identity=supplied_environment_identity,
        ),
        primitive_provider=_provider(bindings),
        reviewed_primitive_source_bindings=bindings,
        collection_authorized=True,
        supplied_environment_identity=supplied_environment_identity,
    )


def test_contract_stays_canonical_collection_disabled():
    m = _load()
    out = m.collector_implementation_contract()
    assert out["supported_snapshot_ids"] == (m.V14, m.V10, m.V2R13, m.V8)
    assert out["injected_primitive_orchestration_implemented"] is True
    assert out["primitive_receipt_source_binding_enforced"] is True
    assert out["primitive_receipt_read_only_boundary_enforced"] is True
    assert out["candidate_shape_validation_implemented"] is True
    assert out["automatic_host_backend_selection"] is False
    assert out["canonical_primitive_source_bindings_present"] is False
    assert out["canonical_collection_enabled"] is False
    assert out[
        "collector_implementation_source_pinned_by_activation_contract"
    ] is False
    assert out["reviewed_collector_binding_present"] is False
    assert out["collector_identity_admission_implemented"] is False
    assert out["runtime_readiness_admission_implemented"] is False
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
        "host_file_observation_backend",
        "host_git_runner",
        "host_path_resolver",
        "observe_v8_assets",
        "observe_v2r13_git_identity",
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


def test_collector_contract_binding_is_exact():
    m = _load()
    assert m.COLLECTOR_CONTRACT_SOURCE_SHA256 == (
        "c48ad0871d4ea25e45efcde36e59622d1bb6b2a2fc4a4ed1f25988b543c2038f"
    )
    assert m.COLLECTOR_CONTRACT_GIT_BLOB == (
        "8014431ad5329137e5ce12334d19d37c877a0b52"
    )
    assert m.COLLECTOR_SEMANTIC_SHA256 == (
        "d11e45cabc10b42e09ab5e328e1e63721b633c7cdcfd7492038ec286b7f3e657"
    )


def test_v14_required_primitive_count_is_nine():
    m = _load()
    names = m.required_primitive_names(m.V14)
    assert len(names) == 9
    assert "endpoint_liveness" in names
    assert "model_identity_verified" in names
    assert "runtime_unit_identity_verified" in names


def test_v10_required_primitive_count_is_nine():
    m = _load()
    names = m.required_primitive_names(m.V10)
    assert len(names) == 9
    assert "endpoint_liveness" in names
    assert "model_identity_verified" in names
    assert "runtime_unit_identity_verified" in names


def test_v2r13_required_primitive_count_is_sixteen():
    m = _load()
    names = m.required_primitive_names(m.V2R13)
    assert len(names) == 16
    assert "endpoint_liveness" in names
    assert "portable_binding_attested" in names
    assert "frozen_source_worktree.exists" in names
    assert "engine_worktree.is_symlink" in names


def test_v8_with_environment_required_primitive_count_is_eight():
    m = _load()
    names = m.required_primitive_names(
        m.V8,
        supplied_environment_identity=True,
    )
    assert len(names) == 8
    assert "runtime_environment_verified" not in names
    assert "offline_only_verified" in names
    assert "load_call_performed" in names


def test_v8_without_environment_required_primitive_count_is_nine():
    m = _load()
    names = m.required_primitive_names(
        m.V8,
        supplied_environment_identity=False,
    )
    assert len(names) == 9
    assert "runtime_environment_verified" in names
    assert "offline_only_verified" in names
    assert "load_call_performed" in names


def test_v14_candidate_shape_valid_but_not_admitted():
    m = _load()
    out = _collect(m, m.V14)
    assert out["activation_evidence_shape_valid"] is True
    assert out["primitive_receipt_count"] == 9
    assert out["collector_implementation_source_binding_admitted"] is False
    assert out["collector_identity_admitted"] is False
    assert out["runtime_readiness_admitted"] is False
    assert out["canonical_collection_path"] is False
    assert out["runtime_execution_authorized"] is False


def test_v10_candidate_shape_valid_but_not_admitted():
    m = _load()
    out = _collect(m, m.V10)
    assert out["activation_evidence_shape_valid"] is True
    assert out["primitive_receipt_count"] == 9
    assert out["collector_identity_admitted"] is False
    assert out["runtime_readiness_admitted"] is False


def test_v2r13_candidate_shape_valid_but_not_admitted():
    m = _load()
    out = _collect(m, m.V2R13)
    assert out["activation_evidence_shape_valid"] is True
    assert out["primitive_receipt_count"] == 16
    evidence = out["activation_evidence_candidate"]
    assert evidence["frozen_source_worktree"]["exists"] is True
    assert evidence["frozen_source_worktree"]["is_symlink"] is False
    assert evidence["engine_worktree"]["is_directory"] is True
    assert evidence["portable_binding_attested"] is True
    assert out["runtime_readiness_admitted"] is False


def test_v8_with_environment_candidate_shape_valid_but_not_admitted():
    m = _load()
    out = _collect(m, m.V8)
    assert out["activation_evidence_shape_valid"] is True
    assert out["primitive_receipt_count"] == 8
    evidence = out["activation_evidence_candidate"]
    assert evidence["runtime_environment_verified"] is True
    assert evidence["offline_only_verified"] is True
    assert evidence["load_call_performed"] is False
    assert out["runtime_readiness_admitted"] is False


def test_v8_without_environment_candidate_shape_valid_but_not_admitted():
    m = _load()
    out = _collect(
        m,
        m.V8,
        supplied_environment_identity=False,
    )
    assert out["activation_evidence_shape_valid"] is True
    assert out["primitive_receipt_count"] == 9
    evidence = out["activation_evidence_candidate"]
    assert evidence["runtime_environment_verified"] is True
    assert evidence["offline_only_verified"] is True
    assert out["runtime_readiness_admitted"] is False


def test_candidate_injects_exact_semantic_collector_sha():
    m = _load()
    out = _collect(m, m.V14)
    evidence = out["activation_evidence_candidate"]
    assert evidence["collector_contract_sha256"] == m.COLLECTOR_SEMANTIC_SHA256


def test_collection_requires_explicit_authority():
    m = _load()
    bindings = _bindings(m, m.V14)
    _expect_hold(
        m.RuntimeCollectorImplementationHold,
        "GENERATION2_COLLECTOR_CANDIDATE_COLLECTION_NOT_AUTHORIZED",
        lambda: m.collect_candidate_with_provider(
            m.V14,
            _base(m, m.V14),
            primitive_provider=_provider(bindings),
            reviewed_primitive_source_bindings=bindings,
            collection_authorized=False,
        ),
    )


def test_primitive_binding_set_must_be_exact():
    m = _load()
    bindings = _bindings(m, m.V14)
    bindings.pop(next(iter(bindings)))
    _expect_hold(
        m.RuntimeCollectorImplementationHold,
        "reviewed primitive source binding set drift",
        lambda: m.collect_candidate_with_provider(
            m.V14,
            _base(m, m.V14),
            primitive_provider=_provider(bindings),
            reviewed_primitive_source_bindings=bindings,
            collection_authorized=True,
        ),
    )


def test_primitive_source_binding_mismatch_is_rejected():
    m = _load()
    bindings = _bindings(m, m.V14)
    wrong_name = next(iter(bindings))

    def provider(snapshot_id, primitive_name):
        record = _provider(bindings)(snapshot_id, primitive_name)
        if primitive_name == wrong_name:
            record = dict(record)
            record["source_sha256"] = "0" * 64
        return record

    _expect_hold(
        m.RuntimeCollectorImplementationHold,
        "primitive source binding mismatch",
        lambda: m.collect_candidate_with_provider(
            m.V14,
            _base(m, m.V14),
            primitive_provider=provider,
            reviewed_primitive_source_bindings=bindings,
            collection_authorized=True,
        ),
    )


def test_primitive_authority_crossing_is_rejected():
    m = _load()
    bindings = _bindings(m, m.V14)
    target = next(iter(bindings))
    _expect_hold(
        m.RuntimeCollectorImplementationHold,
        "primitive crossed authority boundary",
        lambda: m.collect_candidate_with_provider(
            m.V14,
            _base(m, m.V14),
            primitive_provider=_provider(
                bindings,
                mutation_override=target,
            ),
            reviewed_primitive_source_bindings=bindings,
            collection_authorized=True,
        ),
    )


def test_primitive_receipt_field_set_drift_is_rejected():
    m = _load()
    bindings = _bindings(m, m.V14)

    def provider(snapshot_id, primitive_name):
        record = dict(_provider(bindings)(snapshot_id, primitive_name))
        record["extra"] = True
        return record

    _expect_hold(
        m.RuntimeCollectorImplementationHold,
        "primitive receipt field-set drift",
        lambda: m.collect_candidate_with_provider(
            m.V14,
            _base(m, m.V14),
            primitive_provider=provider,
            reviewed_primitive_source_bindings=bindings,
            collection_authorized=True,
        ),
    )


def test_base_non_required_field_is_rejected():
    m = _load()
    bindings = _bindings(m, m.V14)
    base = _base(m, m.V14)
    base["not_required"] = True
    _expect_hold(
        m.RuntimeCollectorImplementationHold,
        "base evidence contains non-required fields",
        lambda: m.collect_candidate_with_provider(
            m.V14,
            base,
            primitive_provider=_provider(bindings),
            reviewed_primitive_source_bindings=bindings,
            collection_authorized=True,
        ),
    )


def test_candidate_conflict_is_rejected():
    m = _load()
    bindings = _bindings(m, m.V14)
    base = _base(m, m.V14)
    base["endpoint_liveness"] = False
    _expect_hold(
        m.RuntimeCollectorImplementationHold,
        "collector candidate field conflict: endpoint_liveness",
        lambda: m.collect_candidate_with_provider(
            m.V14,
            base,
            primitive_provider=_provider(bindings),
            reviewed_primitive_source_bindings=bindings,
            collection_authorized=True,
        ),
    )


def test_shape_validation_rejects_wrong_primitive_value():
    m = _load()
    bindings = _bindings(m, m.V14)

    def provider(snapshot_id, primitive_name):
        record = dict(_provider(bindings)(snapshot_id, primitive_name))
        if primitive_name == "endpoint_liveness":
            record["value"] = False
        return record

    _expect_hold(
        m.activation_evidence.RuntimeActivationEvidenceHold,
        "activation evidence lacks true field: endpoint_liveness",
        lambda: m.collect_candidate_with_provider(
            m.V14,
            _base(m, m.V14),
            primitive_provider=provider,
            reviewed_primitive_source_bindings=bindings,
            collection_authorized=True,
        ),
    )


def test_canonical_collection_entrypoint_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeCollectorImplementationHold,
        "GENERATION2_CANONICAL_PRIMITIVE_SOURCE_BINDINGS_NOT_PRESENT",
        lambda: m.collect_activation_evidence(),
    )


def test_reviewed_activation_binding_remains_false():
    m = _load()
    assert m.activation_evidence.REVIEWED_COLLECTOR_BINDING_PRESENT is False


def test_candidates_never_select_live_host_backend_automatically():
    m = _load()
    for snapshot_id in (m.V14, m.V10, m.V2R13, m.V8):
        out = _collect(m, snapshot_id)
        assert out["live_host_backend_selected_automatically"] is False


def test_candidate_holds_include_source_and_admission_gates():
    m = _load()
    out = _collect(m, m.V2R13)
    assert "CANONICAL_PRIMITIVE_SOURCE_BINDINGS_NOT_PRESENT" in out["holds"]
    assert (
        "COLLECTOR_IMPLEMENTATION_SOURCE_NOT_PINNED_BY_ACTIVATION_CONTRACT"
        in out["holds"]
    )
    assert (
        "ACTIVATION_EVIDENCE_COLLECTOR_IDENTITY_NOT_ADMITTED"
        in out["holds"]
    )
