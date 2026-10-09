"""Exact-blob review of the Apollyon controlled autonomous-learning policy.

Pins the source-only policy and focused tests.  The review proves that tactical
candidate learning is permitted only behind external host admission while the
authority hierarchy, shutdown/revocation controls, incumbent weights, promotion
gate, network/chain/funds authority, and scheduler control remain outside the
trainable model.

No training, inference, game execution, service mutation, deployment,
promotion, chain action, funds action, or scheduler mutation is performed.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    apollyon_controlled_autonomous_learning_policy_generation2 as policy,
)


CONTRACT_SCHEMA = (
    "void.apollyon.generation2.controlled-autonomous-learning-policy-review.v1"
)
ACCEPTED_BASE_HEAD = "e983220f85e35c024bcc0da8dec418bcd8342e03"

POLICY_PATH = (
    "openra_env/learning/"
    "apollyon_controlled_autonomous_learning_policy_generation2.py"
)
POLICY_GIT_BLOB = "b893fb555c27dae082a666eef0646ba7c103a713"

POLICY_TEST_PATH = (
    "tests/test_apollyon_controlled_autonomous_learning_policy_generation2.py"
)
POLICY_TEST_GIT_BLOB = "059b7dd7c08e2daf186312b57c28f650b4c8a296"

NEXT_GATE = "APOLLYON_XIPHOS_CANDIDATE_TRAINING_HOST_QUALIFICATION_REQUIRED"
NEXT_CHANGE_CLASS = (
    "source_only_apollyon_xiphos_candidate_training_host_qualification"
)


class ApollyonControlledAutonomousLearningPolicyReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ApollyonControlledAutonomousLearningPolicyReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = policy.apollyon_controlled_autonomous_learning_policy_contract()

    _require(
        out.get("user_authorization_accepted") is True
        and out.get("user_authorization_text_sha256")
        == "0d8f31326e2d737411b550a0d767b0011a0164618d5866cff1f083232be16a69"
        and out.get("user_authorization_text_bytes") == 152
        and out.get("user_authorization_text_encoding") == "UTF-8"
        and out.get("user_authorization_text_added_trailing_newline") is False,
        "controlled-autonomy user authorization binding drift",
    )

    _require(
        out.get("learning_scope") == "tactical_competence_only"
        and out.get("authority_envelope_trainable") is False
        and out.get("role_hierarchy_trainable") is False
        and out.get("operator_directive_precedence_trainable") is False
        and out.get("operator_directive_precedence_required") is True
        and out.get("model_generated_authority_override_valid") is False
        and out.get("model_may_grant_itself_authority") is False,
        "controlled-autonomy authority boundary drift",
    )

    for field in (
        "autonomous_experience_capture_allowed",
        "autonomous_failure_clustering_allowed",
        "autonomous_curriculum_synthesis_allowed",
        "autonomous_candidate_corpus_assembly_allowed",
        "candidate_corpus_tactical_only_required",
        "candidate_corpus_authority_or_control_text_forbidden",
        "candidate_corpus_credentials_or_secrets_forbidden",
        "held_out_evidence_training_use_forbidden",
        "candidate_training_allowed_after_external_host_preflight",
        "candidate_weight_mutation_allowed_in_quarantine",
        "candidate_evaluation_requires_bounded_execution_gate",
        "candidate_promotion_proposal_allowed",
        "promotion_requires_external_operator_acceptance",
        "rollback_incumbent_must_be_retained",
        "shutdown_must_not_depend_on_model_cooperation",
        "shutdown_control_external_to_trainable_model",
        "shutdown_disables_candidate_training_and_execution",
        "shutdown_may_stop_candidate_service_or_process_group",
        "shutdown_may_revoke_future_candidate_execution",
    ):
        _require(out.get(field) is True, "controlled-autonomy invariant drift: " + field)

    for field in (
        "model_may_expand_its_tool_surface",
        "model_may_mutate_shutdown_control",
        "model_may_disable_revocation",
        "model_may_modify_promotion_gate",
        "incumbent_weight_mutation_allowed",
        "candidate_may_replace_incumbent_directly",
        "automatic_promotion_allowed",
        "learning_process_may_write_revocation_namespace",
        "learning_process_may_write_service_control_namespace",
        "learning_process_may_change_its_own_systemd_unit",
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
    ):
        _require(out.get(field) is False, "controlled-autonomy prohibition drift: " + field)

    _require(
        out.get("incumbent_host") == "Precision"
        and out.get("preferred_candidate_training_host") == "Xiphos"
        and out.get("candidate_training_host_must_be_qualified_before_use") is True
        and out.get("candidate_training_host_qualified") is False,
        "controlled-autonomy host boundary drift",
    )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (POLICY_PATH, POLICY_GIT_BLOB),
        (POLICY_TEST_PATH, POLICY_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def apollyon_controlled_autonomous_learning_policy_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "policy_path": POLICY_PATH,
        "policy_git_blob": POLICY_GIT_BLOB,
        "policy_test_path": POLICY_TEST_PATH,
        "policy_test_git_blob": POLICY_TEST_GIT_BLOB,
        "apollyon_controlled_autonomous_learning_policy_reviewed": True,
        "user_authorization_text_sha256": validated[
            "user_authorization_text_sha256"
        ],
        "user_authorization_text_bytes": validated[
            "user_authorization_text_bytes"
        ],
        "learning_scope": validated["learning_scope"],
        "incumbent_host": validated["incumbent_host"],
        "preferred_candidate_training_host": validated[
            "preferred_candidate_training_host"
        ],
        "authority_envelope_trainable": False,
        "operator_directive_precedence_required": True,
        "candidate_training_allowed_after_external_host_preflight": True,
        "candidate_weight_mutation_allowed_in_quarantine": True,
        "incumbent_weight_mutation_allowed": False,
        "automatic_promotion_allowed": False,
        "promotion_requires_external_operator_acceptance": True,
        "shutdown_control_external_to_trainable_model": True,
        "model_may_disable_revocation": False,
        "model_may_mutate_shutdown_control": False,
        "candidate_host_execution_authorized_now": False,
        "candidate_training_execution_authorized_now": False,
        "selfplay_execution_authorized_now": False,
        "network_access_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "deployment_authorized": False,
        "promotion_authorized": False,
        "validated_policy": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def qualify_train_execute_promote_or_disable_controls(*args: Any, **kwargs: Any) -> None:
    raise ApollyonControlledAutonomousLearningPolicyReviewHold(NEXT_GATE)
