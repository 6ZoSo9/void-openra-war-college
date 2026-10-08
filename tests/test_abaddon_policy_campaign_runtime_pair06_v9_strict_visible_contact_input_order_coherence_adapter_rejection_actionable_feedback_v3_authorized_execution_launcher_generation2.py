from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_authorized_execution_launcher_generation2
    as launcher,
)


def test_contract_is_inert_and_binds_all_five_authorizations():
    out = (
        launcher
        .pair06_v9_actionable_feedback_v3_authorized_execution_launcher_contract()
    )

    assert out[
        "pair06_v9_actionable_feedback_v3_authorized_execution_launcher_implemented"
    ] is True
    assert out["execution_authorization_accepted"] is True
    assert out["policy_activation_authorization_accepted"] is True
    assert out["order_coherence_activation_authorization_accepted"] is True
    assert out["repair_activation_authorization_accepted"] is True
    assert out["actionable_feedback_v3_activation_authorization_accepted"] is True

    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["fresh_actionable_feedback_v3_evidence_namespace_required"] is True

    assert out["contract_inspection_performs_host_io"] is False
    assert out["contract_inspection_creates_attempt_marker"] is False
    assert out["contract_inspection_loads_model"] is False
    assert out["contract_inspection_runs_inference"] is False
    assert out["contract_inspection_executes_game"] is False


def test_exact_v3_authorization_identity_is_pinned():
    assert launcher.EXACT_AUTHORIZATION_TEXT_SHA256 == (
        "9fa7ed99b41b74f6ccfc161f8b2b20cc1fc76391b4a806e75583c6b3ee0ae932"
    )
    assert launcher.EXACT_AUTHORIZATION_TEXT_BYTES == 624
    assert launcher.EXACT_REQUEST_SHA256 == (
        "b3ff66271cabc9ed4d5be57c0a0fcd5b7e8cc69c65857fc0e35656f0c3464b2f"
    )
    assert launcher.EXACT_REQUEST_BYTES == 3113
    assert launcher.AUTHORIZED_MAIN_AT_AUTHORIZATION_HEAD == (
        "077c26ece41b2272fbf208d8e862df6a57462d39"
    )
    assert launcher.AUTHORIZED_MAIN_AT_AUTHORIZATION_TREE == (
        "0fe0093d6504591eaf94721aea662b3dfe923d05"
    )
    assert launcher.CONSUMED_V2_ATTEMPT_MARKER_SHA256 == (
        "ee1b4fc57605387133409f1d73d71d7a55fd57acfbf657c846dea71fcc821176"
    )
    assert launcher.V2_PRESERVATION_RECEIPT_SHA256 == (
        "f898ffdbc16bfdf0b3658224e545bb05006600b711ff74d3e3591cc813c59021"
    )


def test_authorization_mismatch_fails_before_runtime_identity_or_operator(monkeypatch):
    called = {"identity": 0, "operator": 0}

    # The acceptance review is mocked with a mismatched identity.
    # Even with all five accepted gates, this must fail closed.
    bad = {
        "pair06_v9_actionable_feedback_v3_fresh_execution_authorization_acceptance_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "policy_id": launcher.POLICY_ID,
        "intervention_id": launcher.INTERVENTION_ID,
        "authorization_text_sha256": "0" * 64,
        "authorization_text_bytes": 624,
        "authorized_request_sha256": launcher.EXACT_REQUEST_SHA256,
        "authorized_request_bytes": launcher.EXACT_REQUEST_BYTES,
        "authorized_main_head": launcher.AUTHORIZED_MAIN_AT_AUTHORIZATION_HEAD,
        "authorized_main_tree": launcher.AUTHORIZED_MAIN_AT_AUTHORIZATION_TREE,
    }
    monkeypatch.setattr(
        launcher.acceptance_review,
        "pair06_v9_actionable_feedback_v3_fresh_execution_authorization_acceptance_review_contract",
        lambda: bad,
    )
    monkeypatch.setattr(
        launcher,
        "_runtime_identity",
        lambda: called.__setitem__("identity", called["identity"] + 1),
    )
    monkeypatch.setattr(
        launcher.operator,
        "execute_pair06_v9_input_order_adapter_rejection_actionable_feedback_v3_fresh_lineage_baseline_game",
        lambda **kwargs: called.__setitem__("operator", called["operator"] + 1),
    )
    with pytest.raises(
        launcher.Pair06V9ActionableFeedbackV3AuthorizedExecutionLauncherHold,
        match="AUTHORIZATION_IDENTITY_DRIFT",
    ):
        launcher.execute_authorized_pair06_v9_actionable_feedback_v3_once(
            launcher_confirm=launcher.LAUNCH_CONFIRM_TOKEN,
        )
    assert called == {"identity": 0, "operator": 0}


def test_wrong_launcher_confirmation_fails_before_authorization_or_runtime(monkeypatch):
    called = {"authorization": 0, "identity": 0, "operator": 0}

    monkeypatch.setattr(
        launcher,
        "_authorization",
        lambda: called.__setitem__(
            "authorization", called["authorization"] + 1
        ),
    )
    monkeypatch.setattr(
        launcher,
        "_runtime_identity",
        lambda: called.__setitem__("identity", called["identity"] + 1),
    )
    monkeypatch.setattr(
        launcher.operator,
        "execute_pair06_v9_input_order_adapter_rejection_actionable_feedback_v3_fresh_lineage_baseline_game",
        lambda **kwargs: called.__setitem__("operator", called["operator"] + 1),
    )

    with pytest.raises(
        launcher.Pair06V9ActionableFeedbackV3AuthorizedExecutionLauncherHold,
        match="ACTIONABLE_FEEDBACK_V3_LAUNCH_CONFIRMATION_REQUIRED",
    ):
        launcher.execute_authorized_pair06_v9_actionable_feedback_v3_once(
            launcher_confirm="wrong",
        )

    assert called == {"authorization": 0, "identity": 0, "operator": 0}


def test_successful_launcher_delegates_exactly_once_with_five_gates(monkeypatch):
    calls = []

    monkeypatch.setattr(
        launcher,
        "_authorization",
        lambda: {
            "authorization_text_sha256": "a" * 64,
            "authorization_text_bytes": 624,
        },
    )
    monkeypatch.setattr(
        launcher,
        "_runtime_identity",
        lambda: {
            "main_head": "b" * 40,
            "operator_source_sha256": "c" * 64,
        },
    )

    def execute(**kwargs):
        calls.append(kwargs)
        return {
            "pair_slot": 6,
            "arm": "baseline",
            "policy_id": launcher.POLICY_ID,
            "v9_adapter_rejection_operator_integration_used": True,
            "v9_actionable_feedback_v3_operator_integration_used": True,
            "v9_adapter_rejection_activation_performed": True,
            "v9_actionable_feedback_v3_activation_performed": True,
            "pair06_baseline_execution_performed": True,
            "automatic_retry": False,
            "attempt_marker_sha256": "d" * 64,
        }

    monkeypatch.setattr(
        launcher.operator,
        "execute_pair06_v9_input_order_adapter_rejection_actionable_feedback_v3_fresh_lineage_baseline_game",
        execute,
    )

    out = launcher.execute_authorized_pair06_v9_actionable_feedback_v3_once(
        launcher_confirm=launcher.LAUNCH_CONFIRM_TOKEN,
    )

    assert len(calls) == 1
    assert calls[0] == {
        "expected_main_head": "b" * 40,
        "expected_operator_source_sha256": "c" * 64,
        "execution_authorization_accepted": True,
        "policy_activation_authorization_accepted": True,
        "order_coherence_activation_authorization_accepted": True,
        "repair_activation_authorization_accepted": True,
        "actionable_feedback_v3_activation_authorization_accepted": True,
        "execution_confirm": launcher.operator.EXECUTION_CONFIRM_TOKEN,
        "policy_confirm": launcher.operator.POLICY_CONFIRM_TOKEN,
        "order_confirm": launcher.operator.ORDER_CONFIRM_TOKEN,
        "repair_confirm": launcher.operator.REPAIR_CONFIRM_TOKEN,
        "feedback_v3_confirm": launcher.operator.FEEDBACK_V3_CONFIRM_TOKEN,
    }

    assert out["launcher_main_head"] == "b" * 40
    assert out["authorization_text_sha256"] == "a" * 64
    assert out["authorization_text_bytes"] == 624
    assert out["single_authorized_attempt_consumed"] is True
    assert out["authorization_reusable_after_attempt_claim"] is False


@pytest.mark.parametrize(
    "field",
    (
        "contract_inspection_performs_host_io",
        "contract_inspection_creates_attempt_marker",
        "contract_inspection_loads_model",
        "contract_inspection_runs_inference",
        "contract_inspection_executes_game",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "authorization_reusable_after_attempt_claim",
    ),
)
def test_contract_grants_no_extra_or_inspection_authority(field):
    out = (
        launcher
        .pair06_v9_actionable_feedback_v3_authorized_execution_launcher_contract()
    )
    assert out[field] is False


def test_contract_advances_only_to_authorized_host_execution():
    out = (
        launcher
        .pair06_v9_actionable_feedback_v3_authorized_execution_launcher_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V3_AUTHORIZED_HOST_EXECUTION_REQUIRED"
    )
