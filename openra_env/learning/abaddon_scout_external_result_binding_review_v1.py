"""Static source review for the scout external result-binding declaration.

This review binds the exact result-binding source and the reviewed launcher /
attempt-guard chain. It performs no repository I/O and cannot turn declared
digests into verified evidence or execution authority.
"""

from __future__ import annotations

from typing import Any


REVIEW_SCHEMA = "void.abaddon.scout-external-result-binding-source-review.v1"
MAIN_HEAD = "9a151da589f93454d31a475b29297ea8a3d35442"

RESULT_BINDING_PATH = (
    "openra_env/learning/abaddon_scout_external_result_binding_v1.py"
)
RESULT_BINDING_GIT_BLOB = "81fbc479ff087e03fc341d2b191b284fb0017803"

ATTEMPT_GUARD_REVIEW_PATH = (
    "openra_env/learning/abaddon_scout_external_attempt_guard_review_v1.py"
)
ATTEMPT_GUARD_REVIEW_GIT_BLOB = "858a218e87b2dc2eee21a9065bd530fcc0523ee2"

ATTEMPT_GUARD_PATH = (
    "openra_env/learning/abaddon_scout_external_attempt_guard_v1.py"
)
ATTEMPT_GUARD_GIT_BLOB = "043225a7ff6528b9ae7f80994fe17480ad36ed3e"

LAUNCHER_CONTRACT_PATH = (
    "openra_env/learning/abaddon_scout_external_launcher_contract_v1.py"
)
LAUNCHER_CONTRACT_GIT_BLOB = "1f7ee7057c27946f488afe26501482ea4f4fc53d"

NEXT_GATE = "SCOUT_EXTERNAL_RESULT_EVIDENCE_REVIEW_REQUIRED"

FALSE_AUTHORITY_FIELDS = (
    "repository_bytes_verified_by_this_module",
    "declared_digests_verified",
    "result_evidence_verified",
    "post_run_state_verified",
    "operator_authenticated",
    "scout_execution_authorized",
    "scout_execution_performed",
    "training_authorized",
    "automatic_corpus_admission",
    "weights_update_authorized",
    "automatic_policy_promotion_authorized",
    "deployment_authorized",
    "void_chain_mutation_authorized",
    "wallet_or_funds_action_authorized",
)


class ScoutExternalResultBindingReviewHold(ValueError):
    """Declared result identities still require independent evidence review."""


def result_binding_source_review_contract() -> dict[str, Any]:
    return {
        "schema": REVIEW_SCHEMA,
        "main_head": MAIN_HEAD,
        "source_references": {
            LAUNCHER_CONTRACT_PATH: LAUNCHER_CONTRACT_GIT_BLOB,
            ATTEMPT_GUARD_PATH: ATTEMPT_GUARD_GIT_BLOB,
            ATTEMPT_GUARD_REVIEW_PATH: ATTEMPT_GUARD_REVIEW_GIT_BLOB,
            RESULT_BINDING_PATH: RESULT_BINDING_GIT_BLOB,
        },
        "review_kind": "source_binding_expectation_not_evidence_acceptance",
        "result_binding_source_identity_recorded": True,
        "pair03_attempt_reuse_allowed": False,
        "automatic_retry": False,
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "next_gate": NEXT_GATE,
    }


def verify_declared_evidence(*args: Any, **kwargs: Any) -> None:
    raise ScoutExternalResultBindingReviewHold(NEXT_GATE)


def accept_result(*args: Any, **kwargs: Any) -> None:
    raise ScoutExternalResultBindingReviewHold(NEXT_GATE)


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise ScoutExternalResultBindingReviewHold(NEXT_GATE)
