from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_repaired_baseline_execution_authorization_acceptance_generation2
    as acceptance,
)


def test_acceptance_binds_exact_repaired_request_main_and_user_authorization():
    out = acceptance.pair06_v8_repaired_baseline_execution_authorization_acceptance_contract()
    assert out["pair06_v8_repaired_baseline_execution_authorization_accepted"] is True
    assert out["authorized_request_sha256"] == (
        "31c0069869915eb01221d7ea0aa867c0517df0a702eeff58ca69f70dec07a410"
    )
    assert out["authorized_main_head"] == (
        "cb022ce0d32455c2f94f3ff2460bb88d3fb5c08c"
    )
    assert out["authorization_text_sha256"] == (
        "80a422164e3e1a51194d32ed06a2e15b5396711be7640fd0b03b57dddba6cc55"
    )
    assert out["authorization_text_bytes"] == 692


def test_acceptance_authorizes_only_one_fresh_repaired_pair06_baseline_attempt():
    out = acceptance.pair06_v8_repaired_baseline_execution_authorization_acceptance_contract()
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_attempt_required"] is True
    assert out["offload_safe_generate_binding_required"] is True
    assert out["baseline_execution_authorized"] is True
    assert out["runtime_load_authorized"] is True
    assert out["model_inference_authorized"] is True
    assert out["game_execution_authorized"] is True
    assert out["child_spawn_authorized"] is True
    assert out["automatic_retry"] is False


def test_acceptance_keeps_prior_request_and_attempt_spent():
    out = acceptance.pair06_v8_repaired_baseline_execution_authorization_acceptance_contract()
    assert out["spent_request_sha256"] == (
        "a4a46454130e94ceca137b055e8d0fe38c569fd011a03503697414d90943f4ae"
    )
    assert out["spent_attempt_marker_sha256"] == (
        "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
    )
    assert out["spent_request_reusable"] is False
    assert out["spent_attempt_reusable"] is False


def test_acceptance_preserves_all_explicit_exclusions():
    out = acceptance.pair06_v8_repaired_baseline_execution_authorization_acceptance_contract()
    for field in (
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "pair03_replay_authorized",
        "pair09_replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_acceptance_records_no_new_execution_or_consumption_yet():
    out = acceptance.pair06_v8_repaired_baseline_execution_authorization_acceptance_contract()
    assert out["attempt_consumed"] is False
    assert out["game_execution_performed"] is False
    assert out["next_gate"] == "PAIR06_V8_REPAIRED_BASELINE_AUTHORIZED_INVOCATION_READY"


def test_execution_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8RepairedBaselineExecutionAuthorizationAcceptanceHold,
        match="PAIR06_V8_REPAIRED_BASELINE_AUTHORIZED_INVOCATION_READY",
    ):
        acceptance.execute()
