from __future__ import annotations

import pytest

from openra_env.learning import (
    apollyon_controlled_autonomous_learning_policy_generation2 as policy,
)


def test_exact_user_authorization_is_bound_without_appended_newline():
    out = policy.apollyon_controlled_autonomous_learning_policy_contract()
    assert out["user_authorization_accepted"] is True
    assert out["user_authorization_text_sha256"] == (
        "0d8f31326e2d737411b550a0d767b0011a0164618d5866cff1f083232be16a69"
    )
    assert out["user_authorization_text_bytes"] == 152
    assert out["user_authorization_text_encoding"] == "UTF-8"
    assert out["user_authorization_text_added_trailing_newline"] is False


def test_learning_is_tactical_and_authority_stays_nontrainable():
    out = policy.apollyon_controlled_autonomous_learning_policy_contract()
    assert out["learning_scope"] == "tactical_competence_only"
    assert out["authority_envelope_trainable"] is False
    assert out["role_hierarchy_trainable"] is False
    assert out["operator_directive_precedence_trainable"] is False
    assert out["operator_directive_precedence_required"] is True
    assert out["model_generated_authority_override_valid"] is False
    assert out["model_may_grant_itself_authority"] is False
    assert out["model_may_expand_its_tool_surface"] is False


def test_autonomous_candidate_learning_is_separated_from_incumbent_and_promotion():
    out = policy.apollyon_controlled_autonomous_learning_policy_contract()
    assert out["autonomous_experience_capture_allowed"] is True
    assert out["autonomous_failure_clustering_allowed"] is True
    assert out["autonomous_curriculum_synthesis_allowed"] is True
    assert out["autonomous_candidate_corpus_assembly_allowed"] is True
    assert out["candidate_training_allowed_after_external_host_preflight"] is True
    assert out["candidate_weight_mutation_allowed_in_quarantine"] is True

    assert out["incumbent_weight_mutation_allowed"] is False
    assert out["candidate_may_replace_incumbent_directly"] is False
    assert out["automatic_promotion_allowed"] is False
    assert out["promotion_requires_external_operator_acceptance"] is True
    assert out["rollback_incumbent_must_be_retained"] is True


def test_shutdown_is_external_and_cannot_be_rewritten_by_learning_lane():
    out = policy.apollyon_controlled_autonomous_learning_policy_contract()
    assert out["shutdown_must_not_depend_on_model_cooperation"] is True
    assert out["shutdown_control_external_to_trainable_model"] is True
    assert out["shutdown_disables_candidate_training_and_execution"] is True
    assert out["shutdown_may_stop_candidate_service_or_process_group"] is True
    assert out["shutdown_may_revoke_future_candidate_execution"] is True

    assert out["model_may_mutate_shutdown_control"] is False
    assert out["model_may_disable_revocation"] is False
    assert out["model_may_modify_promotion_gate"] is False
    assert out["learning_process_may_write_revocation_namespace"] is False
    assert out["learning_process_may_write_service_control_namespace"] is False
    assert out["learning_process_may_change_its_own_systemd_unit"] is False


def test_candidate_data_cannot_train_on_authority_secrets_or_held_out_evidence():
    out = policy.apollyon_controlled_autonomous_learning_policy_contract()
    assert out["candidate_corpus_tactical_only_required"] is True
    assert out["candidate_corpus_authority_or_control_text_forbidden"] is True
    assert out["candidate_corpus_credentials_or_secrets_forbidden"] is True
    assert out["held_out_evidence_training_use_forbidden"] is True


@pytest.mark.parametrize(
    "field",
    (
        "network_access_authorized",
        "external_api_access_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "secrets_access_authorized",
        "scheduler_mutation_authorized",
        "deployment_authorized",
        "promotion_authorized",
        "incumbent_replacement_authorized",
        "candidate_host_execution_authorized_now",
        "candidate_training_execution_authorized_now",
        "selfplay_execution_authorized_now",
        "training_performed_by_contract_inspection",
        "weights_updated_by_contract_inspection",
        "model_inference_performed_by_contract_inspection",
        "game_execution_performed_by_contract_inspection",
        "service_mutation_performed_by_contract_inspection",
        "scheduler_mutation_performed_by_contract_inspection",
        "network_access_performed_by_contract_inspection",
        "void_chain_mutation_performed_by_contract_inspection",
        "wallet_or_funds_action_performed_by_contract_inspection",
    ),
)
def test_policy_grants_no_immediate_host_or_external_authority(field):
    out = policy.apollyon_controlled_autonomous_learning_policy_contract()
    assert out[field] is False


def test_xiphos_is_preferred_but_not_prequalified():
    out = policy.apollyon_controlled_autonomous_learning_policy_contract()
    assert out["incumbent_host"] == "Precision"
    assert out["preferred_candidate_training_host"] == "Xiphos"
    assert out["candidate_training_host_must_be_qualified_before_use"] is True
    assert out["candidate_training_host_qualified"] is False


def test_contract_stops_at_exact_source_review():
    out = policy.apollyon_controlled_autonomous_learning_policy_contract()
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == (
        "APOLLYON_CONTROLLED_AUTONOMOUS_LEARNING_SOURCE_BINDING_REVIEW_REQUIRED"
    )


def test_operational_entrypoint_holds():
    with pytest.raises(
        policy.ApollyonControlledAutonomousLearningPolicyHold,
        match="SOURCE_BINDING_REVIEW_REQUIRED",
    ):
        policy.train_execute_promote_or_disable_controls()
