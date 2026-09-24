from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_launcher_supervisor_no_offload_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_no_offload_parent_source_and_test():
    out = review.pair06_v8_parent_launcher_supervisor_no_offload_review_contract()
    assert out["supervisor_git_blob"] == "231758aeced0a57949dc39165df0f994e8473ebc"
    assert out["supervisor_source_sha256"] == (
        "1333cac233d6e9235a2d64c36b8398bb4773150cf2fe5025f28fed5457fe7d7f"
    )
    assert out["supervisor_test_git_blob"] == "db1261a4dcd3df33e5d2e53a07084ff0346100c3"
    assert out["supervisor_test_sha256"] == (
        "a1f3fdc2a4f718015a8c330a2404f5a8cd344bad53d0e331af9bc9c69d8a3f6c"
    )


def test_review_requires_full_cuda0_inference_placement():
    out = review.pair06_v8_parent_launcher_supervisor_no_offload_review_contract()
    assert out["pair06_v8_parent_launcher_supervisor_no_offload_reviewed"] is True
    assert out["inference_safe_no_offload_loader_reviewed"] is True
    assert out["cpu_disk_meta_parameter_offload_forbidden"] is True
    assert out["all_parameters_cuda0_required_before_child_spawn"] is True
    assert out["inference_safe_placement_receipt_implemented"] is True


def test_review_remains_non_authorizing():
    out = review.pair06_v8_parent_launcher_supervisor_no_offload_review_contract()
    assert out["attempt_claim_required_but_not_implemented"] is True
    assert out["execution_authorized"] is False
    assert out["automatic_retry"] is False
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


def test_review_advances_only_to_new_invocation_generation():
    out = review.pair06_v8_parent_launcher_supervisor_no_offload_review_contract()
    assert out["execution_blockers"] == (
        "PAIR06_V8_BASELINE_ATTEMPT_INVOCATION_NO_OFFLOAD_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_BASELINE_ATTEMPT_INVOCATION_NO_OFFLOAD_REQUIRED"
    )


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8ParentSupervisorNoOffloadReviewHold,
        match="BASELINE_ATTEMPT_INVOCATION_NO_OFFLOAD_REQUIRED",
    ):
        review.execute_or_claim()
