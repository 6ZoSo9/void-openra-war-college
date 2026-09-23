from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_same_process_python_compat_evidence_source_binding_review_generation2
    as review,
)


def test_review_pins_exact_acceptance_source_and_tests():
    out = review.pair06_v8_python_compat_evidence_review_contract()
    assert out["acceptance_source_git_blob"] == (
        "69cbd7574d7b88e83b9169619a2873ab03d08e3a"
    )
    assert out["acceptance_source_sha256"] == (
        "1de621378882ba4722629c8ac8b01de82000f899e88ef27d45582a0eca31bc14"
    )
    assert out["acceptance_test_git_blob"] == (
        "059b0da800b618c9a0467469e82a5460032906f8"
    )
    assert out["acceptance_test_sha256"] == (
        "ac5f185049abfb38f4d530c022fe4453da2c2fc0feb71a53bc04f2cec25535ef"
    )


def test_review_confirms_parent_child_split_is_required():
    out = review.pair06_v8_python_compat_evidence_review_contract()
    assert out["pair06_v8_same_process_python_compat_evidence_reviewed"] is True
    assert out["pair_slot"] == 6
    assert out["arm"] == "baseline"
    assert out["held_out"] is False
    assert out["same_system_python_binary"] is True
    assert out["separate_virtualenv_site_packages"] is True
    assert out["v8_has_legacy_grpc_proto_dependencies"] is False
    assert out["same_process_legacy_game_path_compatible"] is False
    assert out["parent_child_runtime_split_required"] is True


def test_review_preserves_environment_and_authority_boundaries():
    out = review.pair06_v8_python_compat_evidence_review_contract()
    for field in (
        "package_install_into_v8_authorized",
        "cross_venv_site_packages_injection_authorized",
        "model_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
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


def test_review_advances_only_to_parent_child_split_design():
    out = review.pair06_v8_python_compat_evidence_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PARENT_CHILD_RUNTIME_SPLIT_DESIGN_REQUIRED",
    )
    assert out["next_gate"] == "PAIR06_V8_PARENT_CHILD_RUNTIME_SPLIT_DESIGN_REQUIRED"


def test_execution_entrypoint_holds():
    with pytest.raises(
        review.Pair06V8PythonCompatEvidenceReviewHold,
        match="PAIR06_V8_PARENT_CHILD_RUNTIME_SPLIT_DESIGN_REQUIRED",
    ):
        review.execute_or_install()
