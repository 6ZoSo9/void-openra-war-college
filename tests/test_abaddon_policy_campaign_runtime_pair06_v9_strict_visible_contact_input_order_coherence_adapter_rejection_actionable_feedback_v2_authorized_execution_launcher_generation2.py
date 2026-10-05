from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_authorized_execution_launcher_generation2
    as launcher,
)


def test_contract_is_inert_and_binds_all_five_authorizations():
    out = (
        launcher
        .pair06_v9_actionable_feedback_v2_authorized_execution_launcher_contract()
    )

    assert out[
        "pair06_v9_actionable_feedback_v2_authorized_execution_launcher_implemented"
    ] is True
    assert out["execution_authorization_accepted"] is True
    assert out["policy_activation_authorization_accepted"] is True
    assert out["order_coherence_activation_authorization_accepted"] is True
    assert out["repair_activation_authorization_accepted"] is True
    assert out["actionable_feedback_v2_activation_authorization_accepted"] is True

    assert out["maximum_attempts"] == 1
    assert out["maximum_automatic_retries"] == 0
    assert out["fresh_preclaim_gpu_observation_required"] is True
    assert out["fresh_preclaim_gpu_observation_precedes_attempt_marker"] is True
    assert out["zero_foreign_cuda0_compute_processes_required"] is True
    assert out["fresh_actionable_feedback_v2_evidence_namespace_required"] is True

    assert out["contract_inspection_performs_host_io"] is False
    assert out["contract_inspection_creates_attempt_marker"] is False
    assert out["contract_inspection_loads_model"] is False
    assert out["contract_inspection_runs_inference"] is False
    assert out["contract_inspection_executes_game"] is False


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
        "execute_pair06_v9_input_order_adapter_rejection_actionable_feedback_v2_fresh_lineage_baseline_game",
        lambda **kwargs: called.__setitem__("operator", called["operator"] + 1),
    )

    with pytest.raises(
        launcher.Pair06V9ActionableFeedbackV2AuthorizedExecutionLauncherHold,
        match="ACTIONABLE_FEEDBACK_V2_LAUNCH_CONFIRMATION_REQUIRED",
    ):
        launcher.execute_authorized_pair06_v9_actionable_feedback_v2_once(
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
            "authorization_text_bytes": 435,
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
            "v9_actionable_feedback_v2_operator_integration_used": True,
            "v9_adapter_rejection_activation_performed": True,
            "v9_actionable_feedback_v2_activation_performed": True,
            "pair06_baseline_execution_performed": True,
            "automatic_retry": False,
            "attempt_marker_sha256": "d" * 64,
        }

    monkeypatch.setattr(
        launcher.operator,
        "execute_pair06_v9_input_order_adapter_rejection_actionable_feedback_v2_fresh_lineage_baseline_game",
        execute,
    )

    out = launcher.execute_authorized_pair06_v9_actionable_feedback_v2_once(
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
        "actionable_feedback_v2_activation_authorization_accepted": True,
        "execution_confirm": launcher.operator.EXECUTION_CONFIRM_TOKEN,
        "policy_confirm": launcher.operator.POLICY_CONFIRM_TOKEN,
        "order_confirm": launcher.operator.ORDER_CONFIRM_TOKEN,
        "repair_confirm": launcher.operator.REPAIR_CONFIRM_TOKEN,
        "feedback_v2_confirm": launcher.operator.FEEDBACK_V2_CONFIRM_TOKEN,
    }

    assert out["launcher_main_head"] == "b" * 40
    assert out["authorization_text_sha256"] == "a" * 64
    assert out["authorization_text_bytes"] == 435
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
        .pair06_v9_actionable_feedback_v2_authorized_execution_launcher_contract()
    )
    assert out[field] is False


def test_contract_advances_only_to_authorized_host_execution():
    out = (
        launcher
        .pair06_v9_actionable_feedback_v2_authorized_execution_launcher_contract()
    )

    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
        "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_AUTHORIZED_HOST_EXECUTION_REQUIRED"
    )
