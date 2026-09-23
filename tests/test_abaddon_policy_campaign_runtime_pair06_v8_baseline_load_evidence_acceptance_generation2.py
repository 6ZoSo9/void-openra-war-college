from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_load_evidence_acceptance_generation2
    as acceptance,
)


def test_acceptance_pins_exact_precision_load_receipts():
    out = acceptance.pair06_v8_baseline_load_evidence_acceptance_contract()
    assert out["launcher_sha256"] == (
        "1d2b787f0ca5dd89701e4f9862088d8b458dce872034a870e36f73a5ef177246"
    )
    assert out["execution_main_head"] == (
        "cdafee828fe3066651089e43cef88e4668d680ee"
    )
    accepted = out["accepted_evidence"]
    assert accepted["execution_main_tree"] == (
        "796e6ab771bbae3b9f82a74108ce8038713322a7"
    )
    assert accepted["invocation_source_sha256"] == (
        "864e830cf2d62d3776321b75665f07b58f0b548d6a3dc114b0b9cd84eb9a2ea4"
    )
    assert accepted["authorization_attestation_sha256"] == (
        "1a498a1e596c03985f3c9f861df1d2182a7698acac9bd12cffe520f09a9502cc"
    )
    assert accepted["attempt_marker_sha256"] == (
        "59018bdfbd3058b2bd54b79797de19f60e47bfb5da20cab2779cbb974ec92b7d"
    )
    assert accepted["result_file_sha256"] == (
        "aa5e05327460961df4239532b6c78599fc9340bb975e29f12691b64effd5f774"
    )


def test_acceptance_records_exact_single_baseline_load():
    out = acceptance.pair06_v8_baseline_load_evidence_acceptance_contract()
    accepted = out["accepted_evidence"]
    assert accepted["pair_slot"] == 6
    assert accepted["arm"] == "baseline"
    assert accepted["held_out"] is False
    assert accepted["attempt_consumed"] is True
    assert accepted["maximum_attempts"] == 1
    assert accepted["automatic_retry"] is False
    assert accepted["runtime_load_authorized"] is True
    assert accepted["runtime_load_performed"] is True
    assert accepted["model_weights_loaded"] is True
    assert accepted["another_baseline_load_authorized"] is False


def test_acceptance_records_fresh_environment_and_17_assets():
    accepted = (
        acceptance
        .pair06_v8_baseline_load_evidence_acceptance_contract()["accepted_evidence"]
    )
    assert accepted["runtime_environment_verified"] is True
    assert accepted["runtime_assets_verified"] is True
    assert accepted["verified_asset_count"] == 17


def test_acceptance_does_not_expand_into_inference_game_candidate_or_heldout():
    accepted = (
        acceptance
        .pair06_v8_baseline_load_evidence_acceptance_contract()["accepted_evidence"]
    )
    for field in (
        "candidate_runtime_load_authorized",
        "model_inference_authorized",
        "model_inference_performed",
        "game_execution_authorized",
        "game_execution_performed",
        "pair15_execution_authorized",
        "pair15_execution_performed",
    ):
        assert accepted[field] is False


def test_acceptance_preserves_training_deployment_chain_and_funds_boundaries():
    accepted = (
        acceptance
        .pair06_v8_baseline_load_evidence_acceptance_contract()["accepted_evidence"]
    )
    for field in (
        "training_authorized",
        "training_performed",
        "weights_update_authorized",
        "weights_updated",
        "automatic_policy_promotion_authorized",
        "automatic_policy_promotion",
        "deployment_authorized",
        "deployment_performed",
        "void_chain_mutation_authorized",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_authorized",
        "wallet_or_funds_action_performed",
    ):
        assert accepted[field] is False


def test_exact_evidence_accepts_and_tampering_fails_closed():
    accepted = acceptance.accept_pair06_v8_baseline_load_evidence(
        acceptance.EXPECTED_EVIDENCE
    )
    assert accepted["pair06_v8_baseline_load_evidence_accepted"] is True

    value = deepcopy(acceptance.EXPECTED_EVIDENCE)
    value["game_execution_authorized"] = True
    with pytest.raises(
        acceptance.Pair06V8BaselineLoadEvidenceAcceptanceHold,
        match="evidence drift: game_execution_authorized",
    ):
        acceptance.accept_pair06_v8_baseline_load_evidence(value)


def test_field_set_expansion_is_rejected():
    value = deepcopy(acceptance.EXPECTED_EVIDENCE)
    value["unexpected"] = True
    with pytest.raises(
        acceptance.Pair06V8BaselineLoadEvidenceAcceptanceHold,
        match="field-set drift",
    ):
        acceptance.accept_pair06_v8_baseline_load_evidence(value)


def test_acceptance_advances_only_to_separate_evidence_review():
    out = acceptance.pair06_v8_baseline_load_evidence_acceptance_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_LOAD_EVIDENCE_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_LOAD_EVIDENCE_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_follow_on_execution_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8BaselineLoadEvidenceAcceptanceHold,
        match="PAIR06_V8_BASELINE_LOAD_EVIDENCE_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        acceptance.authorize_follow_on_execution()
