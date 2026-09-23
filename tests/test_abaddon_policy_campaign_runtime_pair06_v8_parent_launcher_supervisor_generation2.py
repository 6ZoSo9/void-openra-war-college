from __future__ import annotations

from types import SimpleNamespace

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_generation2
    as supervisor,
)


def test_contract_implements_parent_supervision_but_remains_inert():
    out = supervisor.pair06_v8_parent_launcher_supervisor_contract()
    assert out["pair06_v8_parent_launcher_supervisor_implemented"] is True
    assert out["pair06_v8_parent_launcher_supervisor_reviewed"] is False
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["socketpair_creation_implemented"] is True
    assert out["child_spawn_with_inherited_fd_implemented"] is True
    assert out["child_private_process_group_implemented"] is True
    assert out["hello_ready_handshake_implemented"] is True
    assert out["parent_decision_service_loop_implemented"] is True
    assert out["authority_check_before_load_implemented"] is True
    assert out["authority_check_before_each_inference_implemented"] is True
    assert out["natural_exit_verification_implemented"] is True
    assert out["term_then_kill_retirement_implemented"] is True
    assert out["v8_reference_release_in_finally_implemented"] is True
    assert out["execution_authorized_by_contract_inspection"] is False
    assert out["subprocess_spawn_performed_by_contract_inspection"] is False
    assert out["model_load_performed_by_contract_inspection"] is False
    assert out["model_inference_performed_by_contract_inspection"] is False
    assert out["game_execution_performed_by_contract_inspection"] is False


def test_contract_leaves_claim_and_worktree_preparation_to_later_gate():
    out = supervisor.pair06_v8_parent_launcher_supervisor_contract()
    assert out["attempt_claim_required_but_not_implemented"] is True
    assert out["worktree_materialization_required_but_not_implemented"] is True
    assert out["isolated_runs_root_required_but_not_created"] is True


def test_decision_response_checks_authority_and_preserves_host_mutation_boundary():
    class Runtime:
        def decide_campaign_turn(self, **kwargs):
            return {
                "host_mutation_performed": False,
                "campaign_action": {"tool": "advance", "arguments": {}},
            }

    request = {
        "attempt_id": "a" * 64,
        "round_no": 1,
        "attempt_no": 1,
        "state": {"tick": 50},
        "typed_tools": [],
        "tool_contract": {},
        "doctrine": "FEINTER",
        "feedback": "",
    }
    out = supervisor._decision_response(
        Runtime(),
        request,
        seq=2,
        authority_check=lambda pair_slot, arm: pair_slot == 6 and arm == "baseline",
    )
    assert out["type"] == "DECIDE_RESPONSE"
    assert out["seq"] == 2
    assert out["campaign_action"] == {"tool": "advance", "arguments": {}}
    assert out["host_mutation_performed"] is False


def test_decision_response_fails_closed_on_revocation():
    with pytest.raises(
        supervisor.Pair06V8ParentSupervisorHold,
        match="REVOKED_BEFORE_INFERENCE",
    ):
        supervisor._decision_response(
            SimpleNamespace(decide_campaign_turn=lambda **kwargs: {}),
            {
                "attempt_id": "a" * 64,
                "round_no": 1,
                "attempt_no": 1,
                "state": {},
                "typed_tools": [],
                "tool_contract": {},
                "doctrine": "FEINTER",
                "feedback": "",
            },
            seq=2,
            authority_check=lambda pair_slot, arm: False,
        )


def test_contract_preserves_non_escalation_boundaries():
    out = supervisor.pair06_v8_parent_launcher_supervisor_contract()
    for field in (
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False
    assert out["automatic_retry"] is False


def test_supervisor_advances_only_to_separate_source_review():
    out = supervisor.pair06_v8_parent_launcher_supervisor_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PARENT_LAUNCHER_SUPERVISOR_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PARENT_LAUNCHER_SUPERVISOR_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_authorization_entrypoint_holds():
    with pytest.raises(
        supervisor.Pair06V8ParentSupervisorHold,
        match="PAIR06_V8_PARENT_LAUNCHER_SUPERVISOR_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        supervisor.authorize_or_claim()
