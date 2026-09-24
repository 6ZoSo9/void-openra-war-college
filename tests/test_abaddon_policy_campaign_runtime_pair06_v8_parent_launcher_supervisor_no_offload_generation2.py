from __future__ import annotations

from types import SimpleNamespace

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_no_offload_generation2
    as supervisor,
)


def test_contract_binds_inference_safe_no_offload_parent_generation():
    out = supervisor.pair06_v8_parent_launcher_supervisor_no_offload_contract()
    assert out["pair06_v8_parent_launcher_supervisor_implemented"] is True
    assert out["pair06_v8_parent_launcher_supervisor_reviewed"] is False
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["inference_safe_no_offload_loader_reviewed"] is True
    assert out["inference_safe_loader_bound_before_generate_adapter"] is True
    assert out["cpu_disk_meta_parameter_offload_forbidden"] is True
    assert out["all_parameters_cuda0_required_before_child_spawn"] is True
    assert out["inference_safe_placement_receipt_implemented"] is True
    assert out["offload_safe_generate_adapter_reviewed"] is True
    assert out["offload_safe_generate_bound_after_load_before_child_spawn"] is True
    assert out["hard_coded_cuda_input_transfer_used_by_pair06_parent"] is False


def test_contract_preserves_one_shot_and_non_escalation_boundaries():
    out = supervisor.pair06_v8_parent_launcher_supervisor_no_offload_contract()
    assert out["attempt_claim_required_but_not_implemented"] is True
    assert out["worktree_materialization_required_but_not_implemented"] is True
    assert out["isolated_runs_root_required_but_not_created"] is True
    assert out["automatic_retry"] is False
    for field in (
        "execution_authorized_by_contract_inspection",
        "subprocess_spawn_performed_by_contract_inspection",
        "model_load_performed_by_contract_inspection",
        "model_inference_performed_by_contract_inspection",
        "game_execution_performed_by_contract_inspection",
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


def test_decision_response_still_requires_live_authority():
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
    assert out["host_mutation_performed"] is False

    with pytest.raises(
        supervisor.Pair06V8ParentSupervisorHold,
        match="REVOKED_BEFORE_INFERENCE",
    ):
        supervisor._decision_response(
            SimpleNamespace(decide_campaign_turn=lambda **kwargs: {}),
            request,
            seq=2,
            authority_check=lambda pair_slot, arm: False,
        )


def test_contract_advances_only_to_separate_review():
    out = supervisor.pair06_v8_parent_launcher_supervisor_no_offload_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PARENT_LAUNCHER_SUPERVISOR_NO_OFFLOAD_SOURCE_BINDING_REVIEW_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_PARENT_LAUNCHER_SUPERVISOR_NO_OFFLOAD_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_authorization_entrypoint_holds():
    with pytest.raises(
        supervisor.Pair06V8ParentSupervisorHold,
        match="NO_OFFLOAD_SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        supervisor.authorize_or_claim()
