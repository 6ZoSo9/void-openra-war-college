"""Source binding review for the scout post-run read-only backend.

This review pins the concrete backend and its regression tests to the already
reviewed observer contract/adapter/review and the current canary derived runner.

It performs no host observation and creates no scout execution authority.
Actual live observation and any future canary execution remain separate explicit
operator decisions.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning import abaddon_scout_post_run_backend_v1 as backend
from openra_env.learning import abaddon_scout_post_run_observer_review_v1 as observer_review


REVIEW_SCHEMA = "void.abaddon.scout-post-run-backend-source-binding-review.v1"
ACCEPTED_MAIN_HEAD = "0487be81964ef92459f17920418fe0abe8b2a3e5"

BACKEND_PATH = "openra_env/learning/abaddon_scout_post_run_backend_v1.py"
BACKEND_GIT_BLOB = "40eb707a7215324fd9b794da9430427f059fea3a"
BACKEND_TEST_PATH = "tests/test_abaddon_scout_post_run_backend_v1.py"
BACKEND_TEST_GIT_BLOB = "124a0bd061ce45bebecf86ce7f9db39d657f6f59"

OBSERVER_CONTRACT_PATH = observer_review.OBSERVER_CONTRACT_PATH
OBSERVER_CONTRACT_GIT_BLOB = observer_review.OBSERVER_CONTRACT_GIT_BLOB
OBSERVER_IMPLEMENTATION_PATH = observer_review.OBSERVER_IMPLEMENTATION_PATH
OBSERVER_IMPLEMENTATION_GIT_BLOB = observer_review.OBSERVER_IMPLEMENTATION_GIT_BLOB
OBSERVER_REVIEW_PATH = "openra_env/learning/abaddon_scout_post_run_observer_review_v1.py"
OBSERVER_REVIEW_GIT_BLOB = "d8059f351ac31e5df19f7fef58c5737f31fdcf14"

DERIVED_RUNNER_PATH = (
    "fixtures/learning/scout-missions-v1/scout_repair_canary_derived_runner_v1.py"
)
DERIVED_RUNNER_GIT_BLOB = "40030e2ee61d17fd94abd1df733d3ea22650512b"

NEXT_GATE = "SCOUT_POST_RUN_LIVE_OBSERVATION_REQUIRES_SEPARATE_AUTHORIZATION"
NEXT_CHANGE_CLASS = "future_launcher_or_live_observation_only"

FALSE_AUTHORITY_FIELDS = (
    "repository_bytes_verified_by_this_module",
    "host_observation_performed",
    "post_run_state_verified",
    "result_evidence_verified",
    "operator_authenticated",
    "scout_execution_authorized",
    "scout_execution_performed",
    "automatic_retry",
    "training_authorized",
    "automatic_corpus_admission",
    "weights_update_authorized",
    "automatic_policy_promotion_authorized",
    "deployment_authorized",
    "void_chain_mutation_authorized",
    "wallet_or_funds_action_authorized",
)


class ScoutPostRunBackendSourceBindingReviewHold(ValueError):
    pass


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ScoutPostRunBackendSourceBindingReviewHold(code)


def scout_post_run_backend_source_binding_review_contract() -> dict[str, Any]:
    prior = observer_review.post_run_observer_source_review_contract()
    candidate = backend.scout_post_run_backend_contract()

    _require(
        prior.get("next_gate") == "SCOUT_POST_RUN_OBSERVER_BACKEND_BINDING_REQUIRED",
        "SCOUT_BACKEND_PRIOR_GATE_DRIFT",
    )
    _require(
        all(value is False for value in prior["authority"].values()),
        "SCOUT_BACKEND_PRIOR_AUTHORITY_DRIFT",
    )
    _require(
        candidate.get("required_observations")
        == [
            "attempt_marker_present",
            "runtime_service_inactive",
            "engine_container_absent",
            "model_process_absent",
            "source_checkout_clean",
        ],
        "SCOUT_BACKEND_OBSERVATION_SET_DRIFT",
    )
    _require(
        candidate.get("derived_canary_runner_git_blob") == DERIVED_RUNNER_GIT_BLOB,
        "SCOUT_BACKEND_DERIVED_RUNNER_DRIFT",
    )
    _require(
        candidate.get("automatic_host_backend_selection") is False
        and candidate.get("observation_requires_explicit_authority") is True,
        "SCOUT_BACKEND_AUTHORITY_GATE_DRIFT",
    )
    _require(
        candidate.get("git_optional_locks_disabled") is True,
        "SCOUT_BACKEND_GIT_OPTIONAL_LOCKS_DRIFT",
    )
    for field in (
        "host_observation_performed",
        "post_run_state_verified",
        "result_evidence_verified",
        "scout_execution_authorized",
        "automatic_retry",
        "training_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(candidate.get(field) is False, "SCOUT_BACKEND_BOUNDARY_DRIFT:" + field)

    return {
        "schema": REVIEW_SCHEMA,
        "accepted_main_head": ACCEPTED_MAIN_HEAD,
        "source_references": {
            BACKEND_PATH: BACKEND_GIT_BLOB,
            BACKEND_TEST_PATH: BACKEND_TEST_GIT_BLOB,
            OBSERVER_CONTRACT_PATH: OBSERVER_CONTRACT_GIT_BLOB,
            OBSERVER_IMPLEMENTATION_PATH: OBSERVER_IMPLEMENTATION_GIT_BLOB,
            OBSERVER_REVIEW_PATH: OBSERVER_REVIEW_GIT_BLOB,
            DERIVED_RUNNER_PATH: DERIVED_RUNNER_GIT_BLOB,
        },
        "backend_source_binding_present": True,
        "backend_regression_binding_present": True,
        "observer_contract_binding_preserved": True,
        "observer_adapter_binding_preserved": True,
        "observer_review_binding_preserved": True,
        "derived_canary_runner_binding_present": True,
        "all_five_post_run_probe_mechanics_implemented": True,
        "marker_byte_identity_probe_implemented": True,
        "marker_directory_identity_binding_implemented": True,
        "service_inactive_probe_implemented": True,
        "container_absence_probe_implemented": True,
        "model_process_absence_probe_implemented": True,
        "source_and_engine_cleanliness_probe_implemented": True,
        "git_optional_locks_disabled": True,
        "revocation_recheck_delegated_to_observer_adapter": True,
        "automatic_backend_selection": False,
        "actual_host_observation_required_for_future_result_acceptance": True,
        "actual_host_observation_performed": False,
        "actual_scout_execution_authorized": False,
        "actual_scout_execution_performed": False,
        "source_only_backend_gap_closed": True,
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "backend_contract": deepcopy(candidate),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def observe_live_host(*args: Any, **kwargs: Any) -> None:
    raise ScoutPostRunBackendSourceBindingReviewHold(NEXT_GATE)


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise ScoutPostRunBackendSourceBindingReviewHold(NEXT_GATE)


def accept_result(*args: Any, **kwargs: Any) -> None:
    raise ScoutPostRunBackendSourceBindingReviewHold(NEXT_GATE)
