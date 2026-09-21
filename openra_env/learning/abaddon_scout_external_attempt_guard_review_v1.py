"""Static source review for the durable scout attempt guard.

This manifest binds the exact reviewed launcher contract, launcher source-review
manifest, and durable attempt-guard source. It performs no repository I/O and
grants no execution, attempt-consumption, result, training, deployment, chain,
wallet, or funds authority.
"""

from __future__ import annotations

from typing import Any


REVIEW_SCHEMA = "void.abaddon.scout-external-attempt-guard-source-review.v1"
MAIN_HEAD = "9a151da589f93454d31a475b29297ea8a3d35442"

LAUNCHER_CONTRACT_PATH = (
    "openra_env/learning/abaddon_scout_external_launcher_contract_v1.py"
)
LAUNCHER_CONTRACT_GIT_BLOB = "1f7ee7057c27946f488afe26501482ea4f4fc53d"

LAUNCHER_REVIEW_PATH = (
    "openra_env/learning/abaddon_scout_external_launcher_contract_review_v1.py"
)
LAUNCHER_REVIEW_GIT_BLOB = "3b6281b6a7bcaa9d5b3d9300728103883a810a6c"

ATTEMPT_GUARD_PATH = (
    "openra_env/learning/abaddon_scout_external_attempt_guard_v1.py"
)
ATTEMPT_GUARD_GIT_BLOB = "043225a7ff6528b9ae7f80994fe17480ad36ed3e"

REQUEST_SHA256 = "67582949d9cbb6815c59ba9c78e6ac40fc303080320b5d707ad2b9e64e9baf55"
NEXT_GATE = "SCOUT_EXTERNAL_RESULT_BINDING_REQUIRED"

FALSE_AUTHORITY_FIELDS = (
    "repository_bytes_verified_by_this_module",
    "operator_authenticated",
    "fresh_attempt_consumed_by_this_module",
    "runtime_readiness_verified",
    "scout_experiment_authorized",
    "scout_execution_authorized",
    "scout_execution_performed",
    "result_evidence_verified",
    "post_run_state_verified",
    "training_authorized",
    "automatic_corpus_admission",
    "weights_update_authorized",
    "automatic_policy_promotion_authorized",
    "deployment_authorized",
    "void_chain_mutation_authorized",
    "wallet_or_funds_action_authorized",
)


class ScoutExternalAttemptGuardReviewHold(ValueError):
    """Effectful or result actions remain outside this source review."""


def attempt_guard_source_review_contract() -> dict[str, Any]:
    return {
        "schema": REVIEW_SCHEMA,
        "main_head": MAIN_HEAD,
        "source_references": {
            LAUNCHER_CONTRACT_PATH: LAUNCHER_CONTRACT_GIT_BLOB,
            LAUNCHER_REVIEW_PATH: LAUNCHER_REVIEW_GIT_BLOB,
            ATTEMPT_GUARD_PATH: ATTEMPT_GUARD_GIT_BLOB,
        },
        "request_sha256": REQUEST_SHA256,
        "review_kind": "source_binding_expectation_not_runtime_authority",
        "attempt_guard_source_identity_recorded": True,
        "pair03_attempt_reuse_allowed": False,
        "pair03_attempt_reset_allowed": False,
        "automatic_retry": False,
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "next_gate": NEXT_GATE,
    }


def consume_attempt(*args: Any, **kwargs: Any) -> None:
    raise ScoutExternalAttemptGuardReviewHold(NEXT_GATE)


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise ScoutExternalAttemptGuardReviewHold(NEXT_GATE)


def accept_result(*args: Any, **kwargs: Any) -> None:
    raise ScoutExternalAttemptGuardReviewHold(NEXT_GATE)
