"""Static binding for the scout evidence-review and observer contract sources.

This manifest proves only expected source identities. It performs no host
observation and grants no evidence acceptance or execution authority.
"""

from __future__ import annotations

from typing import Any


REVIEW_SCHEMA = "void.abaddon.scout-result-evidence-review-source-binding.v1"
MAIN_HEAD = "9a151da589f93454d31a475b29297ea8a3d35442"

EVIDENCE_REVIEW_PATH = (
    "openra_env/learning/abaddon_scout_external_result_evidence_review_v1.py"
)
EVIDENCE_REVIEW_GIT_BLOB = "3c703599877c4bf18aeabcf848b85e9b5a517e95"

OBSERVER_CONTRACT_PATH = (
    "openra_env/learning/abaddon_scout_post_run_observer_contract_v1.py"
)
OBSERVER_CONTRACT_GIT_BLOB = "fd71ac745c10349047d49f753ecfce1aab712648"

NEXT_GATE = "SCOUT_POST_RUN_OBSERVER_IMPLEMENTATION_REVIEW_REQUIRED"

FALSE_AUTHORITY_FIELDS = (
    "repository_bytes_verified_by_this_module",
    "host_observer_implemented",
    "host_observer_source_verified",
    "host_observation_performed",
    "post_run_state_verified",
    "result_evidence_verified",
    "operator_authenticated",
    "scout_execution_authorized",
    "training_authorized",
    "automatic_corpus_admission",
    "weights_update_authorized",
    "automatic_policy_promotion_authorized",
    "deployment_authorized",
    "void_chain_mutation_authorized",
    "wallet_or_funds_action_authorized",
)


class ScoutResultEvidenceReviewSourceBindingHold(ValueError):
    """Host observer implementation remains outside this source-only manifest."""


def result_evidence_review_source_binding_contract() -> dict[str, Any]:
    return {
        "schema": REVIEW_SCHEMA,
        "main_head": MAIN_HEAD,
        "source_references": {
            EVIDENCE_REVIEW_PATH: EVIDENCE_REVIEW_GIT_BLOB,
            OBSERVER_CONTRACT_PATH: OBSERVER_CONTRACT_GIT_BLOB,
        },
        "review_kind": "source_binding_expectation_not_host_observation",
        "observer_contract_source_identity_recorded": True,
        "evidence_review_source_identity_recorded": True,
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "next_gate": NEXT_GATE,
    }


def observe_host_state(*args: Any, **kwargs: Any) -> None:
    raise ScoutResultEvidenceReviewSourceBindingHold(NEXT_GATE)


def accept_result(*args: Any, **kwargs: Any) -> None:
    raise ScoutResultEvidenceReviewSourceBindingHold(NEXT_GATE)


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise ScoutResultEvidenceReviewSourceBindingHold(NEXT_GATE)
