from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_capability_generation2
    as capability,
)


def test_contract_binds_exact_pair06_v8_capability():
    out = capability.pair06_v8_runtime_capability_contract()
    assert out["allocation_review_git_blob"] == (
        "5dd312086df8d2a6c205badb3feb71560c519990"
    )
    assert out["allocation_review_source_sha256"] == (
        "695c9ff074a21a7ff6002d30a50852e7a9a746c5735a078f985b80a6a22dfe0a"
    )
    assert out["v8_runtime_git_blob"] == (
        "fd0e72767ba199e88af9e9eb2455c03ace027a14"
    )
    assert out["v8_runtime_source_sha256"] == (
        "faf4b64ea4755fabdbdfc778f3df534a87f056a638763aa1560c7965c482b5af"
    )
    assert out["runtime_activation_git_blob"] == (
        "a3acb42280c334daa24a3b830105a04666fd603b"
    )
    assert out["runtime_activation_source_sha256"] == (
        "dc4c90175dee00f23ab28bc362cec41245a069345c0154d519215e3cb8150a3c"
    )


def test_contract_routes_pair06_to_accepted_v8_without_loading():
    out = capability.pair06_v8_runtime_capability_contract()
    assert out["pair06_v8_runtime_capability_implemented"] is True
    assert out["pair06_v8_runtime_capability_reviewed"] is False
    assert out["pair_slot"] == 6
    assert out["arms"] == ("baseline", "candidate")
    assert out["held_out"] is False
    assert out["runtime_selection_key"] == (
        "apollyon-v3-v8-accepted-model-control"
    )
    assert out["activation_kind"] == "inprocess_accepted_v8_runtime"
    assert out["model_dir_path_bound"] is False
    assert out["adapter_dir_path_bound"] is False
    assert out["runtime_loader_callable_bound"] is True
    assert out["runtime_load_authorized"] is False
    assert out["runtime_load_performed"] is False
    assert out["model_weights_loaded"] is False
    assert out["model_inference_performed"] is False
    assert out["game_execution_performed"] is False
    assert out["game_mutation_performed"] is False


def test_contract_preserves_v8_preload_safety_requirements():
    out = capability.pair06_v8_runtime_capability_contract()
    assert out["runtime_environment_verification_required_before_load"] is True
    assert out["runtime_assets_hash_verification_required_before_load"] is True
    assert out["offline_only_model_load_required"] is True
    runtime = out["accepted_v8_runtime_contract"]
    assert runtime["local_runtime_loader_implemented"] is True
    assert runtime["runtime_assets_hash_verified_before_load"] is True
    assert runtime["offline_only_model_load"] is True
    assert runtime["runtime_execution_performed"] is False
    assert runtime["model_execution_performed"] is False
    assert runtime["game_started"] is False
    assert runtime["game_mutation_performed"] is False


def test_activation_plans_remain_inert_and_unbound():
    out = capability.pair06_v8_runtime_capability_contract()
    expected_reasons = [
        "V8_MODEL_DIR_BINDING_NOT_REVIEWED",
        "V8_ADAPTER_DIR_BINDING_NOT_REVIEWED",
        "V8_LOAD_CALL_BINDING_NOT_REVIEWED",
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
    ]
    for arm in ("baseline", "candidate"):
        plan = out["activation_plans"][arm]
        assert plan["pair_slot"] == 6
        assert plan["arm"] == arm
        assert plan["held_out"] is False
        assert plan["opponent_snapshot_id"] == (
            "apollyon-v3-v8-accepted-model-control"
        )
        assert plan["activation"]["activation_kind"] == (
            "inprocess_accepted_v8_runtime"
        )
        assert plan["activation"]["model_dir_path_bound"] is False
        assert plan["activation"]["adapter_dir_path_bound"] is False
        assert plan["activation"]["load_call_materialized"] is False
        assert plan["activation"]["model_weights_loaded"] is False
        assert plan["runtime_started"] is False
        assert plan["reasons"] == expected_reasons
        assert plan["authority"]["runtime_execution_authorized"] is False


@pytest.mark.parametrize(
    ("pair_slot", "arm", "authorized"),
    [
        (3, "baseline", True),
        (9, "candidate", True),
        (15, "baseline", True),
        (6, "heldout", True),
        (6, "baseline", False),
    ],
)
def test_load_rejects_wrong_scope_or_missing_authority(
    monkeypatch,
    pair_slot,
    arm,
    authorized,
):
    called = []

    def fake_load(*, model_dir, adapter_dir):
        called.append((model_dir, adapter_dir))
        return object()

    monkeypatch.setattr(
        capability.v8_runtime.FrozenV8LocalToolRuntime,
        "load",
        fake_load,
    )

    with pytest.raises(capability.Pair06V8RuntimeCapabilityHold):
        capability.load_pair06_v8_runtime(
            pair_slot=pair_slot,
            arm=arm,
            model_dir="/tmp/model",
            adapter_dir="/tmp/adapter",
            runtime_load_authorized=authorized,
            authority_check=lambda slot, requested_arm: True,
        )
    assert called == []


def test_load_rejects_revoked_authority_without_calling_loader(monkeypatch):
    called = []

    def fake_load(*, model_dir, adapter_dir):
        called.append((model_dir, adapter_dir))
        return object()

    monkeypatch.setattr(
        capability.v8_runtime.FrozenV8LocalToolRuntime,
        "load",
        fake_load,
    )

    with pytest.raises(
        capability.Pair06V8RuntimeCapabilityHold,
        match="PAIR06_V8_RUNTIME_LOAD_AUTHORITY_REVOKED",
    ):
        capability.load_pair06_v8_runtime(
            pair_slot=6,
            arm="baseline",
            model_dir="/tmp/model",
            adapter_dir="/tmp/adapter",
            runtime_load_authorized=True,
            authority_check=lambda slot, requested_arm: False,
        )
    assert called == []


def test_mocked_authorized_load_binds_exact_paths_without_real_model_load(monkeypatch):
    sentinel = object()
    called = []

    def fake_load(*, model_dir, adapter_dir):
        called.append((str(model_dir), str(adapter_dir)))
        return sentinel

    monkeypatch.setattr(
        capability.v8_runtime.FrozenV8LocalToolRuntime,
        "load",
        fake_load,
    )

    observed = capability.load_pair06_v8_runtime(
        pair_slot=6,
        arm="candidate",
        model_dir="/tmp/pair06-v8-model",
        adapter_dir="/tmp/pair06-v8-adapter",
        runtime_load_authorized=True,
        authority_check=lambda slot, requested_arm: (
            slot == 6 and requested_arm == "candidate"
        ),
    )
    assert observed is sentinel
    assert called == [
        ("/tmp/pair06-v8-model", "/tmp/pair06-v8-adapter")
    ]


def test_contract_keeps_execution_and_mutation_authority_closed():
    out = capability.pair06_v8_runtime_capability_contract()
    assert out["automatic_retry"] is False
    assert out["pair15_execution_authorized"] is False
    assert out["pair03_replay_authorized"] is False
    assert out["pair09_replay_authorized"] is False
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_contract_advances_only_to_source_binding_review():
    out = capability.pair06_v8_runtime_capability_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_RUNTIME_CAPABILITY_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_RUNTIME_CAPABILITY_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_game_pair15_and_promotion_entrypoints_hold():
    for fn, message in (
        (
            capability.execute_pair06_game,
            "PAIR06_V8_GAME_EXECUTION_NOT_IMPLEMENTED",
        ),
        (
            capability.execute_pair15,
            "PAIR15_HELD_OUT_EXECUTION_NOT_AUTHORIZED",
        ),
        (
            capability.promote_or_train_candidate,
            "CANDIDATE_PROMOTION_AND_TRAINING_NOT_AUTHORIZED",
        ),
    ):
        with pytest.raises(
            capability.Pair06V8RuntimeCapabilityHold,
            match=message,
        ):
            fn()
