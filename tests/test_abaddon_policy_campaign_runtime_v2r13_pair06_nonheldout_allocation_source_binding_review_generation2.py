from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair06_nonheldout_allocation_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_allocation_source_and_tests():
    out = review.v2r13_pair06_nonheldout_allocation_review_contract()
    assert out["allocation_git_blob"] == (
        "434cd0e7e471b8b176434faf051252482354a1cc"
    )
    assert out["allocation_source_sha256"] == (
        "d5ba7bf9e3431d2f1389a417baab574431198e1f12e3f62a37cfacc689a30adf"
    )
    assert out["allocation_test_git_blob"] == (
        "bcfec926f5a94df4fe744fa29fec6db9630af42f"
    )
    assert out["allocation_test_sha256"] == (
        "12ef48a49ebe02ffcc6de02b03c948aebfd5b236c183d16fc639f9a03df32671"
    )


def test_review_confirms_exact_pair06_allocation():
    out = review.v2r13_pair06_nonheldout_allocation_review_contract()
    assert out["pair06_nonheldout_allocation_reviewed"] is True
    assert out["selected_pair_slot"] == 6
    assert out["selected_seed"] == 208354846
    assert out["selected_held_out"] is False
    assert out["selected_opponent_role"] == "prior_accepted_model_control"
    assert out["selected_opponent_snapshot_id"] == (
        "apollyon-v3-v8-accepted-model-control"
    )
    assert out["selected_opponent_snapshot_sha256"] == (
        "5c51082219530a302ce25b28daba9928f56a436c11d1508ca0bef755f4a86667"
    )


def test_review_routes_pair06_to_v8_capability():
    out = review.v2r13_pair06_nonheldout_allocation_review_contract()
    assert out["v2r13_executor_not_applicable_to_pair06"] is True
    assert out["pair06_v8_runtime_capability_required"] is True
    assert out["pair06_v8_activation_kind"] == "inprocess_accepted_v8_runtime"
    assert out["pair06_v8_model_dir_binding_reviewed"] is False
    assert out["pair06_v8_adapter_dir_binding_reviewed"] is False
    assert out["pair06_v8_load_call_binding_reviewed"] is False
    assert out["pair06_runtime_execution_authorized"] is False
    assert out["pair06_runtime_execution_performed"] is False


def test_review_preserves_pair15_and_existing_evidence():
    out = review.v2r13_pair06_nonheldout_allocation_review_contract()
    assert out["pair15_execution_authorized"] is False
    assert out["pair15_execution_performed"] is False
    assert out["pair03_replay_authorized"] is False
    assert out["pair09_replay_authorized"] is False


def test_review_grants_no_training_promotion_or_external_authority():
    out = review.v2r13_pair06_nonheldout_allocation_review_contract()
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_frontier_is_v8_capability_implementation():
    out = review.v2r13_pair06_nonheldout_allocation_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_RUNTIME_CAPABILITY_IMPLEMENTATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "PAIR06_V8_RUNTIME_CAPABILITY_IMPLEMENTATION_REQUIRED"
    )


def test_prohibited_action_entrypoints_hold():
    for fn, message in (
        (
            review.execute_pair06,
            "V2R13_PAIR06_RUNTIME_EXECUTION_NOT_AUTHORIZED",
        ),
        (
            review.execute_pair15,
            "V2R13_PAIR15_HELD_OUT_EXECUTION_NOT_AUTHORIZED",
        ),
        (
            review.promote_or_train_candidate,
            "V2R13_CANDIDATE_PROMOTION_AND_TRAINING_NOT_AUTHORIZED",
        ),
    ):
        with pytest.raises(
            review.V2R13Pair06NonheldoutAllocationReviewHold,
            match=message,
        ):
            fn()
