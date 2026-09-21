"""Static source review for the bounded injected scout post-run observer.

This review binds the exact observer contract and adapter implementation sources.
It performs no host observation and does not accept result evidence.
"""

from __future__ import annotations

from typing import Any


REVIEW_SCHEMA = "void.abaddon.scout-post-run-observer-source-review.v1"
MAIN_HEAD = "9a151da589f93454d31a475b29297ea8a3d35442"

OBSERVER_CONTRACT_PATH = (
    "openra_env/learning/abaddon_scout_post_run_observer_contract_v1.py"
)
OBSERVER_CONTRACT_GIT_BLOB = "fd71ac745c10349047d49f753ecfce1aab712648"

OBSERVER_IMPLEMENTATION_PATH = (
    "openra_env/learning/abaddon_scout_post_run_observer_v1.py"
)
OBSERVER_IMPLEMENTATION_GIT_BLOB = "11dfa40a861e6772258178bbc32840c670e47f9f"

NEXT_GATE = "SCOUT_POST_RUN_OBSERVER_BACKEND_BINDING_REQUIRED"

FALSE_AUTHORITY_FIELDS = (
    "repository_bytes_verified_by_this_module",
    "host_backend_bound",
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


class ScoutPostRunObserverSourceReviewHold(ValueError):
    """Effectful host backend binding remains a separate gate."""


def post_run_observer_source_review_contract() -> dict[str, Any]:
    return {
        "schema": REVIEW_SCHEMA,
        "main_head": MAIN_HEAD,
        "source_references": {
            OBSERVER_CONTRACT_PATH: OBSERVER_CONTRACT_GIT_BLOB,
            OBSERVER_IMPLEMENTATION_PATH: OBSERVER_IMPLEMENTATION_GIT_BLOB,
        },
        "review_kind": "source_binding_expectation_not_host_backend_binding",
        "observer_contract_source_identity_recorded": True,
        "observer_implementation_source_identity_recorded": True,
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "next_gate": NEXT_GATE,
    }


def bind_host_backend(*args: Any, **kwargs: Any) -> None:
    raise ScoutPostRunObserverSourceReviewHold(NEXT_GATE)


def observe_host_state(*args: Any, **kwargs: Any) -> None:
    raise ScoutPostRunObserverSourceReviewHold(NEXT_GATE)


def accept_result(*args: Any, **kwargs: Any) -> None:
    raise ScoutPostRunObserverSourceReviewHold(NEXT_GATE)
