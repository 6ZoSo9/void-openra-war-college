from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_host_preflight_evidence_acceptance_generation2
    as acceptance,
)


def test_exact_external_preflight_evidence_is_accepted():
    out = acceptance.v2r13_host_preflight_evidence_acceptance_contract()
    assert out["host_preflight_evidence_accepted"] is True
    assert out["host_preflight_completed"] is True
    assert out["host_preflight_green"] is True
    assert out["host_preflight_snapshot_sha256"] == (
        "9a15a64e62e7f06cb0444f6e0dc830ddae9d9c262378f7f1f705d273aab7e364"
    )
    assert out["guarded_preflight_wrapper_sha256"] == (
        "12fb1d872be25eaf2583632d085db0ec025d92eda1bc053538e18534177442cd"
    )


def test_runtime_authority_is_preserved_without_execution():
    out = acceptance.v2r13_host_preflight_evidence_acceptance_contract()
    assert out["runtime_execution_authorization_accepted"] is True
    assert out["runtime_execution_implemented"] is True
    assert out["runtime_execution_authorized"] is True
    assert out["runtime_execution_performed"] is False
    assert out["fresh_readiness_still_required_before_inference"] is True
    assert out["automatic_retry"] is False


def test_no_training_promotion_deployment_void_or_funds_action_is_admitted():
    out = acceptance.v2r13_host_preflight_evidence_acceptance_contract()
    for field in (
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "automatic_policy_promotion",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        assert out[field] is False


def test_outer_service_stop_is_recorded_separately_from_read_only_collector():
    out = acceptance.v2r13_host_preflight_evidence_acceptance_contract()
    assert out["outer_environment_correction_service_stop_performed"] is True
    assert out["preflight_collector_service_action_performed"] is False


def test_authorized_execution_surface_remains_exactly_six_v2r13_arms():
    out = acceptance.v2r13_host_preflight_evidence_acceptance_contract()
    accepted = out["accepted_evidence"]
    assert accepted["authorized_pair_slots"] == (3, 9, 15)
    assert accepted["authorized_arms"] == ("baseline", "candidate")
    assert accepted["held_out_pair_slots"] == (15,)


def test_evidence_main_and_engine_identities_are_exact():
    evidence = acceptance.EXPECTED_EVIDENCE
    assert evidence["canonical_main_head"] == (
        "7a39699ab83f1706221afe638fe717783e466f87"
    )
    assert evidence["canonical_main_tree"] == (
        "10b14c64bef3e6b3f0d0f1fbf2204d0f16157632"
    )
    assert evidence["frozen_engine_head"] == (
        "1607a7a6501d42a47638393ecef8b22831064932"
    )
    assert evidence["frozen_engine_tree"] == (
        "bf562078c53edda3e6545f501b73ba1273c5df49"
    )


def test_evidence_preserves_dormant_ollama_boundary():
    evidence = acceptance.EXPECTED_EVIDENCE
    assert evidence["ollama_active"] == "inactive"
    assert evidence["ollama_enabled"] == "disabled"
    assert evidence["activation_permit_present"] is False
    assert evidence["dormant_fuse_present"] is False
    assert evidence["dormant_condition_present"] is False


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("host_preflight_green", False),
        ("runtime_execution_performed", True),
        ("model_inference_performed", True),
        ("game_execution_performed", True),
        ("training_performed", True),
        ("automatic_policy_promotion", True),
        ("activation_permit_present", True),
        ("all_authorized_arm_paths_absent", False),
        ("outer_environment_correction_service_stop_performed", False),
        ("preflight_collector_service_action_performed", True),
    ],
)
def test_tampered_preflight_evidence_is_rejected(field, value):
    evidence = deepcopy(acceptance.EXPECTED_EVIDENCE)
    evidence[field] = value
    with pytest.raises(
        acceptance.V2R13HostPreflightEvidenceAcceptanceHold,
        match=f"host preflight evidence drift: {field}",
    ):
        acceptance.accept_v2r13_host_preflight_evidence(evidence)


def test_evidence_field_set_expansion_is_rejected():
    evidence = deepcopy(acceptance.EXPECTED_EVIDENCE)
    evidence["other_runtime_lane_authorized"] = True
    with pytest.raises(
        acceptance.V2R13HostPreflightEvidenceAcceptanceHold,
        match="host preflight evidence field-set drift",
    ):
        acceptance.accept_v2r13_host_preflight_evidence(evidence)


def test_acceptance_advances_only_to_explicit_runtime_invocation():
    out = acceptance.v2r13_host_preflight_evidence_acceptance_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_source_blockers"] == ()
    assert out["execution_blockers"] == (
        "V2R13_RUNTIME_EXECUTION_INVOCATION_REQUIRED",
    )
    assert out["next_gate"] == "V2R13_RUNTIME_EXECUTION_INVOCATION_REQUIRED"
    assert out["next_change_class"] == (
        "precision_v2r13_runtime_execution_invocation"
    )


def test_runtime_invocation_entrypoint_still_holds():
    with pytest.raises(
        acceptance.V2R13HostPreflightEvidenceAcceptanceHold,
        match="V2R13_RUNTIME_EXECUTION_INVOCATION_REQUIRED",
    ):
        acceptance.invoke_v2r13_runtime()
