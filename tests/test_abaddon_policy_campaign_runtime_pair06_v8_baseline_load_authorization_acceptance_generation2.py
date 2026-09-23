from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_load_authorization_acceptance_generation2
    as authorization,
)


def test_authorization_is_exactly_one_pair06_baseline_v8_load_attempt():
    out = authorization.pair06_v8_baseline_load_authorization_acceptance_contract()
    assert out["authorization_accepted"] is True
    assert out["authorization_scope"] == "single_pair06_baseline_v8_runtime_load"
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["baseline_first"] is True
    assert out["runtime_load_authorized"] is True
    assert out["maximum_runtime_load_attempts"] == 1
    assert out["automatic_retry"] is False


def test_authorization_is_repository_attestation_not_crypto_proof():
    out = authorization.pair06_v8_baseline_load_authorization_acceptance_contract()
    assert out["authorization_repository_attestation"] is True
    assert out["authorization_cryptographic_proof"] is False
    assert (
        authorization.AUTHORIZATION_ATTESTATION[
            "cryptographic_operator_signature_present"
        ]
        is False
    )


def test_load_is_authorized_but_not_implemented_or_performed():
    out = authorization.pair06_v8_baseline_load_authorization_acceptance_contract()
    assert out["runtime_load_authorized"] is True
    assert out["runtime_load_invocation_implemented"] is False
    assert out["runtime_load_performed"] is False
    assert out["model_weights_loaded"] is False
    assert out["load_attempt_consumption_required"] is True
    assert out["create_only_load_attempt_marker_required"] is True


def test_preload_safety_gates_remain_required():
    out = authorization.pair06_v8_baseline_load_authorization_acceptance_contract()
    assert out["fresh_runtime_environment_verification_required_before_load"] is True
    assert out["runtime_asset_hash_verification_required_before_load"] is True
    assert out["offline_only_model_load_required"] is True
    assert out["authority_callback_required_at_load"] is True


def test_authorization_does_not_expand_into_candidate_game_training_or_external_actions():
    out = authorization.pair06_v8_baseline_load_authorization_acceptance_contract()
    for field in (
        "candidate_runtime_load_authorized",
        "pair15_execution_authorized",
        "model_inference_authorized",
        "model_inference_performed",
        "game_execution_authorized",
        "game_execution_performed",
        "training_authorized",
        "training_performed",
        "weights_update_authorized",
        "weights_updated",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "deployment_performed",
        "void_chain_mutation_authorized",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_authorized",
        "wallet_or_funds_action_performed",
    ):
        assert out[field] is False


def test_exact_embedded_authorization_is_accepted():
    out = authorization.accept_pair06_v8_baseline_load_authorization(
        authorization.AUTHORIZATION_ATTESTATION
    )
    assert out["authorization_accepted"] is True
    assert out["runtime_load_authorized"] is True


def test_tampered_scope_is_rejected():
    value = deepcopy(authorization.AUTHORIZATION_ATTESTATION)
    value["authorization_scope"] = "all_pair06_runtime_actions"
    with pytest.raises(
        authorization.Pair06V8BaselineLoadAuthorizationAcceptanceHold,
        match="authorization drift: authorization_scope",
    ):
        authorization.accept_pair06_v8_baseline_load_authorization(value)


def test_tampered_arm_is_rejected():
    value = deepcopy(authorization.AUTHORIZATION_ATTESTATION)
    value["arm"] = "candidate"
    with pytest.raises(
        authorization.Pair06V8BaselineLoadAuthorizationAcceptanceHold,
        match="authorization drift: arm",
    ):
        authorization.accept_pair06_v8_baseline_load_authorization(value)


def test_field_set_expansion_is_rejected():
    value = deepcopy(authorization.AUTHORIZATION_ATTESTATION)
    value["unexpected_authority_field"] = True
    with pytest.raises(
        authorization.Pair06V8BaselineLoadAuthorizationAcceptanceHold,
        match="authorization field-set drift",
    ):
        authorization.accept_pair06_v8_baseline_load_authorization(value)


def test_next_gate_is_bounded_runtime_load_invocation_implementation():
    out = authorization.pair06_v8_baseline_load_authorization_acceptance_contract()
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_RUNTIME_LOAD_INVOCATION_IMPLEMENTATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_RUNTIME_LOAD_INVOCATION_IMPLEMENTATION_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_pair06_v8_baseline_runtime_load_invocation"
    )


def test_runtime_candidate_and_game_entrypoints_still_hold():
    with pytest.raises(
        authorization.Pair06V8BaselineLoadAuthorizationAcceptanceHold,
        match="PAIR06_V8_BASELINE_RUNTIME_LOAD_INVOCATION_IMPLEMENTATION_REQUIRED",
    ):
        authorization.invoke_runtime_load()
    with pytest.raises(
        authorization.Pair06V8BaselineLoadAuthorizationAcceptanceHold,
        match="PAIR06_V8_CANDIDATE_RUNTIME_LOAD_NOT_AUTHORIZED",
    ):
        authorization.authorize_candidate_runtime_load()
    with pytest.raises(
        authorization.Pair06V8BaselineLoadAuthorizationAcceptanceHold,
        match="PAIR06_V8_GAME_EXECUTION_NOT_AUTHORIZED",
    ):
        authorization.execute_game()
