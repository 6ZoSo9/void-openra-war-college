"""Pure contract for a future independent scout post-run host observer.

This module defines what must be observed after a future scout attempt. It does
not inspect systemd, processes, containers, Git, files, models, engines, or the
network. The effectful observer implementation remains a separate review gate.
"""

from __future__ import annotations

from typing import Any


CONTRACT_SCHEMA = "void.abaddon.scout-post-run-observer-contract.v1"
EVIDENCE_SCHEMA = "void.abaddon.scout-post-run-state-evidence.v1"
NEXT_GATE = "SCOUT_POST_RUN_OBSERVER_IMPLEMENTATION_REVIEW_REQUIRED"

REQUIRED_OBSERVATIONS = (
    "attempt_marker_present",
    "runtime_service_inactive",
    "engine_container_absent",
    "model_process_absent",
    "source_checkout_clean",
)

FALSE_CLAIMS = (
    "callback_return_used_as_shutdown_proof",
    "historical_cleanup_print_used_as_shutdown_proof",
    "automatic_retry",
    "pair03_attempt_reused",
    "pair03_attempt_reset",
)

FALSE_AUTHORITY_FIELDS = (
    "host_observation_implemented",
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


class ScoutPostRunObserverContractHold(ValueError):
    """Host observation is intentionally unavailable in this pure contract."""


def post_run_observer_contract() -> dict[str, Any]:
    return {
        "schema": CONTRACT_SCHEMA,
        "evidence_schema": EVIDENCE_SCHEMA,
        "required_observations": list(REQUIRED_OBSERVATIONS),
        "false_claims": list(FALSE_CLAIMS),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "independent_observation_required": True,
        "callback_return_is_shutdown_proof": False,
        "historical_cleanup_print_is_shutdown_proof": False,
        "next_gate": NEXT_GATE,
    }


def observe_host_state(*args: Any, **kwargs: Any) -> None:
    """The effectful implementation must be separately reviewed."""
    raise ScoutPostRunObserverContractHold(NEXT_GATE)


def accept_result(*args: Any, **kwargs: Any) -> None:
    raise ScoutPostRunObserverContractHold(NEXT_GATE)


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise ScoutPostRunObserverContractHold(NEXT_GATE)
