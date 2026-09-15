from __future__ import annotations

import hashlib
from pathlib import Path
from types import SimpleNamespace

import pytest

from openra_env.learning.apollyon_v2r13_portable_checkout import (
    APOLLYON_BOUNDARY_RUNNER_SHA256,
    BASE_JOINT_RUNNER_SHA256,
    BROKER_V11_SOAK_V14_SHA256,
    FROZEN_ENGINE_COMMIT,
    FROZEN_WAR_COLLEGE_COMMIT,
    FROZEN_WAR_COLLEGE_TREE,
    JOINT_PROTO_SHA256,
    LEGACY_WARM_START_RUNNER_SHA256,
    MODEL_ALIAS,
    PortableCheckoutBindingError,
    PortableRunnerBinding,
    portable_binding_contract,
    reviewed_path_binding,
)


def _base() -> SimpleNamespace:
    return SimpleNamespace(
        WAR_COLLEGE_COMMIT=FROZEN_WAR_COLLEGE_COMMIT,
        ENGINE_COMMIT=FROZEN_ENGINE_COMMIT,
        IMAGE_ID="sha256:79f2f6800382489a2a648839fc0d58e546384938439378aeea06461363de25f5",
        APOLLYON_RUNNER_SHA=APOLLYON_BOUNDARY_RUNNER_SHA256,
        PROTO_SHA=JOINT_PROTO_SHA256,
        APOLLYON_MODEL=MODEL_ALIAS,
        RL=Path("/old/source"),
        OPENRA=Path("/old/engine"),
        PROTO=Path("/old/source/proto/rl_bridge.proto"),
    )


def _legacy(base: SimpleNamespace | None = None) -> SimpleNamespace:
    base = base or _base()
    return SimpleNamespace(
        BASE_RUNNER_SHA=BASE_JOINT_RUNNER_SHA256,
        WAR_COLLEGE_COMMIT=FROZEN_WAR_COLLEGE_COMMIT,
        ENGINE_COMMIT=FROZEN_ENGINE_COMMIT,
        IMAGE_ID="sha256:79f2f6800382489a2a648839fc0d58e546384938439378aeea06461363de25f5",
        RL=Path("/canonical/source"),
        OPENRA=Path("/canonical/engine"),
        load_base=lambda: base,
    )


def test_contract_binds_exact_frozen_identity_and_stays_nonexecuting():
    result = portable_binding_contract()
    assert result["frozen_war_college_commit"] == FROZEN_WAR_COLLEGE_COMMIT
    assert result["frozen_war_college_tree"] == FROZEN_WAR_COLLEGE_TREE
    assert result["frozen_engine_commit"] == FROZEN_ENGINE_COMMIT
    assert result["legacy_warm_start_runner_sha256"] == LEGACY_WARM_START_RUNNER_SHA256
    assert result["base_joint_runner_sha256"] == BASE_JOINT_RUNNER_SHA256
    assert result["apollyon_boundary_runner_sha256"] == APOLLYON_BOUNDARY_RUNNER_SHA256
    assert result["broker_v11_soak_v14_sha256"] == BROKER_V11_SOAK_V14_SHA256
    assert result["source_materialization"] == "detached_git_worktree"
    assert result["canonical_checkout_mutation_required"] is False
    assert result["current_main_head_independent"] is True
    assert result["runtime_execution_performed"] is False
    assert result["model_execution_performed"] is False
    assert result["game_started"] is False
    assert result["training"] is False
    assert result["weights_updated"] is False
    assert result["binding_contract_sha256"] == (
        "677e503e8d4827a9d8950a177f308ad08982f612d70881f16de2c271e3b10e49"
    )


def test_reviewed_path_binding_keeps_source_engine_and_proto_explicit(tmp_path):
    source = tmp_path / "source"
    engine = tmp_path / "engine"
    result = reviewed_path_binding(
        frozen_source_root=source,
        exact_engine_root=engine,
    )
    assert result["source_root"] == source.resolve()
    assert result["engine_root"] == engine.resolve()
    assert result["proto_path"] == (source / "proto/rl_bridge.proto").resolve()


def test_source_and_engine_roots_must_be_distinct(tmp_path):
    with pytest.raises(PortableCheckoutBindingError, match="must be distinct"):
        reviewed_path_binding(
            frozen_source_root=tmp_path,
            exact_engine_root=tmp_path,
        )


def test_binding_rebinds_legacy_and_loaded_base_then_restores(tmp_path):
    base = _base()
    legacy = _legacy(base)
    old_legacy_rl = legacy.RL
    old_legacy_engine = legacy.OPENRA
    old_base_rl = base.RL
    old_base_engine = base.OPENRA
    old_base_proto = base.PROTO
    source = tmp_path / "frozen-source"
    engine = tmp_path / "engine"

    with PortableRunnerBinding(
        legacy,
        frozen_source_root=source,
        exact_engine_root=engine,
    ) as binding:
        assert legacy.RL == source.resolve()
        assert legacy.OPENRA == engine.resolve()
        loaded = legacy.load_base()
        assert loaded is base
        assert base.RL == source.resolve()
        assert base.OPENRA == engine.resolve()
        assert base.PROTO == (source / "proto/rl_bridge.proto").resolve()
        attestation = binding.attestation()
        assert attestation["legacy_source_root_bound"] is True
        assert attestation["legacy_engine_root_bound"] is True
        assert attestation["base_loaded_and_bound"] is True
        assert attestation["runtime_execution_performed"] is False
        assert attestation["model_execution_performed"] is False
        assert attestation["game_started"] is False

    assert legacy.RL == old_legacy_rl
    assert legacy.OPENRA == old_legacy_engine
    assert base.RL == old_base_rl
    assert base.OPENRA == old_base_engine
    assert base.PROTO == old_base_proto


def test_binding_can_attest_before_base_load_without_claiming_base_bound(tmp_path):
    legacy = _legacy()
    with PortableRunnerBinding(
        legacy,
        frozen_source_root=tmp_path / "source",
        exact_engine_root=tmp_path / "engine",
    ) as binding:
        result = binding.attestation()
        assert result["legacy_source_root_bound"] is True
        assert result["legacy_engine_root_bound"] is True
        assert result["base_loaded_and_bound"] is False


def test_binding_rejects_legacy_commit_drift(tmp_path):
    legacy = _legacy()
    legacy.WAR_COLLEGE_COMMIT = "0" * 40
    with pytest.raises(PortableCheckoutBindingError, match="commit drift"):
        PortableRunnerBinding(
            legacy,
            frozen_source_root=tmp_path / "source",
            exact_engine_root=tmp_path / "engine",
        )


def test_binding_rejects_loaded_base_boundary_drift(tmp_path):
    base = _base()
    base.APOLLYON_RUNNER_SHA = "0" * 64
    legacy = _legacy(base)
    with PortableRunnerBinding(
        legacy,
        frozen_source_root=tmp_path / "source",
        exact_engine_root=tmp_path / "engine",
    ):
        with pytest.raises(PortableCheckoutBindingError, match="boundary SHA drift"):
            legacy.load_base()


def test_source_hash_is_stable_for_runtime_realization_binding():
    path = Path(__file__).parents[1] / (
        "openra_env/learning/apollyon_v2r13_portable_checkout.py"
    )
    assert hashlib.sha256(path.read_bytes()).hexdigest() == (
        "92e16e281d5a9036d78d900f35d854c6fb9783b2bf156c2acab69408d13a015d"
    )
