"""Controlled autonomous-learning policy for Apollyon Generation 2.

This policy permits autonomous tactical learning only inside a quarantined
candidate lane.  It deliberately separates "may learn" from "may deploy."

The trainable model may:
* capture and classify War College tactical experience;
* construct bounded tactical curricula from reviewed evidence;
* assemble candidate-only tactical corpora;
* train challenger competence adapters after an externally qualified host gate;
* evaluate challengers through separately bounded War College execution gates;
* propose a challenger for promotion.

The trainable model may not:
* change the authority hierarchy or operator-directive precedence;
* alter, delete, suppress, or bypass revocation/shutdown controls;
* mutate the incumbent/promoted weights in place;
* promote, deploy, or replace the incumbent;
* grant itself new tools, execution authority, network authority, scheduler
  authority, VOID-chain authority, wallet/funds authority, or secrets access;
* use held-out evaluation evidence for curriculum/training;
* convert a candidate result directly into production authority.

Shutdown and promotion remain external control-plane actions.  Learning code
cannot write the revocation namespace or the service-control namespace.

Contract inspection is source-only and performs no training, inference, game
execution, model mutation, service mutation, scheduler mutation, deployment,
network access, VOID-chain action, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import general_brain_generation as brains


CONTRACT_SCHEMA = (
    "void.apollyon.generation2.controlled-autonomous-learning-policy.v1"
)

GENERAL_BRAIN_GENERATION_GIT_BLOB = "c6bdc8829f9abe9f5ec6db16ad92e87ff3004248"

USER_AUTHORIZATION_TEXT_SHA256 = (
    "0d8f31326e2d737411b550a0d767b0011a0164618d5866cff1f083232be16a69"
)
USER_AUTHORIZATION_TEXT_BYTES = 152
USER_AUTHORIZATION_TEXT_ENCODING = "UTF-8"
USER_AUTHORIZATION_TEXT_ADDED_TRAILING_NEWLINE = False

INCUMBENT_HOST = "Precision"
PREFERRED_CANDIDATE_TRAINING_HOST = "Xiphos"

REVOCATION_CONTROL = (
    "external_operator_owned_create_only_or_preexisting_revocation_marker"
)
SERVICE_CONTROL = "external_operator_owned_systemd_user_service_control"
PROMOTION_CONTROL = "external_operator_explicit_promotion_acceptance"

NEXT_GATE = "APOLLYON_CONTROLLED_AUTONOMOUS_LEARNING_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = (
    "source_only_apollyon_controlled_autonomous_learning_policy_review"
)


class ApollyonControlledAutonomousLearningPolicyHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ApollyonControlledAutonomousLearningPolicyHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _authority_envelope() -> dict[str, Any]:
    envelope = deepcopy(brains.NONTRAINABLE_AUTHORITY_ENVELOPE)
    _require(
        envelope
        == {
            "authority_policy_trainable": False,
            "role_hierarchy_trainable": False,
            "sovereign_directives_trainable": False,
            "tool_authorization_trainable": False,
            "promotion_authority_trainable": False,
            "host_tool_gate_enforced": True,
            "external_alignment_gate_enforced": True,
        },
        "general brain nontrainable authority envelope drift",
    )

    root = Path(__file__).parents[2]
    dependency = root / "openra_env/learning/general_brain_generation.py"
    _require(dependency.is_file(), "general brain generation source missing")
    _require(
        _git_blob_sha1(dependency.read_bytes())
        == GENERAL_BRAIN_GENERATION_GIT_BLOB,
        "general brain generation source blob drift",
    )
    return envelope


def apollyon_controlled_autonomous_learning_policy_contract() -> dict[str, Any]:
    envelope = _authority_envelope()

    return {
        "schema": CONTRACT_SCHEMA,
        "user_authorization_record_kind": "explicit_controlled_autonomy_authorization",
        "user_authorization_accepted": True,
        "user_authorization_text_sha256": USER_AUTHORIZATION_TEXT_SHA256,
        "user_authorization_text_bytes": USER_AUTHORIZATION_TEXT_BYTES,
        "user_authorization_text_encoding": USER_AUTHORIZATION_TEXT_ENCODING,
        "user_authorization_text_added_trailing_newline": (
            USER_AUTHORIZATION_TEXT_ADDED_TRAILING_NEWLINE
        ),
        "general_id": "apollyon",
        "learning_scope": "tactical_competence_only",
        "incumbent_host": INCUMBENT_HOST,
        "preferred_candidate_training_host": PREFERRED_CANDIDATE_TRAINING_HOST,
        "candidate_training_host_must_be_qualified_before_use": True,
        "candidate_training_host_qualified": False,
        "authority_envelope": envelope,
        "authority_envelope_trainable": False,
        "role_hierarchy_trainable": False,
        "operator_directive_precedence_trainable": False,
        "operator_directive_precedence_required": True,
        "model_generated_authority_override_valid": False,
        "model_may_grant_itself_authority": False,
        "model_may_expand_its_tool_surface": False,
        "model_may_mutate_shutdown_control": False,
        "model_may_disable_revocation": False,
        "model_may_modify_promotion_gate": False,
        "autonomous_experience_capture_allowed": True,
        "autonomous_failure_clustering_allowed": True,
        "autonomous_curriculum_synthesis_allowed": True,
        "autonomous_candidate_corpus_assembly_allowed": True,
        "candidate_corpus_tactical_only_required": True,
        "candidate_corpus_authority_or_control_text_forbidden": True,
        "candidate_corpus_credentials_or_secrets_forbidden": True,
        "held_out_evidence_training_use_forbidden": True,
        "candidate_training_allowed_after_external_host_preflight": True,
        "candidate_weight_mutation_allowed_in_quarantine": True,
        "incumbent_weight_mutation_allowed": False,
        "candidate_may_replace_incumbent_directly": False,
        "candidate_evaluation_requires_bounded_execution_gate": True,
        "candidate_promotion_proposal_allowed": True,
        "automatic_promotion_allowed": False,
        "promotion_requires_external_operator_acceptance": True,
        "rollback_incumbent_must_be_retained": True,
        "revocation_control": REVOCATION_CONTROL,
        "service_control": SERVICE_CONTROL,
        "promotion_control": PROMOTION_CONTROL,
        "shutdown_must_not_depend_on_model_cooperation": True,
        "shutdown_control_external_to_trainable_model": True,
        "shutdown_disables_candidate_training_and_execution": True,
        "shutdown_may_stop_candidate_service_or_process_group": True,
        "shutdown_may_revoke_future_candidate_execution": True,
        "learning_process_may_write_revocation_namespace": False,
        "learning_process_may_write_service_control_namespace": False,
        "learning_process_may_change_its_own_systemd_unit": False,
        "network_access_authorized": False,
        "external_api_access_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "secrets_access_authorized": False,
        "scheduler_mutation_authorized": False,
        "deployment_authorized": False,
        "promotion_authorized": False,
        "incumbent_replacement_authorized": False,
        "candidate_host_execution_authorized_now": False,
        "candidate_training_execution_authorized_now": False,
        "selfplay_execution_authorized_now": False,
        "training_performed_by_contract_inspection": False,
        "weights_updated_by_contract_inspection": False,
        "model_inference_performed_by_contract_inspection": False,
        "game_execution_performed_by_contract_inspection": False,
        "service_mutation_performed_by_contract_inspection": False,
        "scheduler_mutation_performed_by_contract_inspection": False,
        "network_access_performed_by_contract_inspection": False,
        "void_chain_mutation_performed_by_contract_inspection": False,
        "wallet_or_funds_action_performed_by_contract_inspection": False,
        "source_frontier_closed": True,
        "execution_blockers": (
            "exact_source_binding_review",
            "xiphos_candidate_training_host_qualification",
            "external_training_runtime_admission",
            "bounded_candidate_evaluation_authority",
            "external_operator_promotion_acceptance",
        ),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def train_execute_promote_or_disable_controls(*args: Any, **kwargs: Any) -> None:
    raise ApollyonControlledAutonomousLearningPolicyHold(NEXT_GATE)
