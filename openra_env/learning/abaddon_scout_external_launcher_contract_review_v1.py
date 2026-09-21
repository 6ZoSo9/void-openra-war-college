"""Static source-binding manifest for the scout external launcher contract.

This module records the exact reviewed contract blob and request digest. It does
not read repository files, authenticate an operator, consume an attempt, start a
runtime, execute a game, or accept result evidence.
"""

from __future__ import annotations

from typing import Any


REVIEW_SCHEMA = "void.abaddon.scout-external-launcher-source-binding-review.v1"
CONTRACT_PATH = "openra_env/learning/abaddon_scout_external_launcher_contract_v1.py"
CONTRACT_GIT_BLOB = "1f7ee7057c27946f488afe26501482ea4f4fc53d"
CONTRACT_REQUEST_SHA256 = (
    "67582949d9cbb6815c59ba9c78e6ac40fc303080320b5d707ad2b9e64e9baf55"
)
BOUND_MAIN_HEAD = "9a151da589f93454d31a475b29297ea8a3d35442"
NEXT_GATE = "SCOUT_FRESH_DURABLE_ATTEMPT_GUARD_REQUIRED"

FALSE_AUTHORITY_FIELDS = (
    "repository_bytes_verified_by_this_module",
    "operator_authenticated",
    "fresh_attempt_guard_bound",
    "fresh_attempt_consumed",
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


class ScoutExternalLauncherSourceReviewHold(ValueError):
    """Runtime and result authority remain outside this review manifest."""


def source_binding_review_contract() -> dict[str, Any]:
    """Return source expectations and an explicitly non-authorizing boundary."""
    return {
        "schema": REVIEW_SCHEMA,
        "bound_main_head": BOUND_MAIN_HEAD,
        "contract_path": CONTRACT_PATH,
        "contract_git_blob": CONTRACT_GIT_BLOB,
        "contract_request_sha256": CONTRACT_REQUEST_SHA256,
        "review_kind": "source_binding_expectation_not_runtime_authority",
        "source_identity_expectation_recorded": True,
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "pair03_attempt_reuse_allowed": False,
        "automatic_retry": False,
        "automatic_training_admission": False,
        "automatic_policy_promotion": False,
        "next_gate": NEXT_GATE,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    """No execution authority exists in the source-review layer."""
    raise ScoutExternalLauncherSourceReviewHold(NEXT_GATE)


def consume_attempt(*args: Any, **kwargs: Any) -> None:
    """Attempt consumption requires a separate reviewed durable guard."""
    raise ScoutExternalLauncherSourceReviewHold(NEXT_GATE)


def accept_result(*args: Any, **kwargs: Any) -> None:
    """Result acceptance requires a separate reviewed result binder."""
    raise ScoutExternalLauncherSourceReviewHold(NEXT_GATE)
