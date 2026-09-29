"""Exact-blob source review for scout post-run provenance binding v1.

This review pins the provenance bundle and its regression tests to repository
bytes and checks that the prior reviewed read-only backend remains the only
possible source of host observations.

It performs no host observation and grants no scout execution or final result
acceptance authority.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning import abaddon_scout_post_run_backend_source_binding_review_v1 as backend_review
from openra_env.learning import abaddon_scout_post_run_provenance_bundle_v1 as bundle


REVIEW_SCHEMA = "void.abaddon.scout-post-run-provenance-binding-source-review.v1"
ACCEPTED_BASE_MAIN_HEAD = "8201ea345ec5e48eae71ee0e51d018676629aa77"

BUNDLE_PATH = "openra_env/learning/abaddon_scout_post_run_provenance_bundle_v1.py"
BUNDLE_GIT_BLOB = "74755251b902f43e569a7a954152cb2e869f39c1"
BUNDLE_TEST_PATH = "tests/test_abaddon_scout_post_run_provenance_bundle_v1.py"
BUNDLE_TEST_GIT_BLOB = "cf487c7a2d1050177128d4571a720c22cc994103"

BACKEND_REVIEW_PATH = (
    "openra_env/learning/abaddon_scout_post_run_backend_source_binding_review_v1.py"
)
BACKEND_REVIEW_GIT_BLOB = "06b8ce51d6101e0d1ec0d39c6b6a057d91ae8974"

NEXT_GATE = (
    "SCOUT_POST_RUN_PROVENANCE_AWARE_LIVE_OBSERVATION_REQUIRES_SEPARATE_AUTHORIZATION"
)
NEXT_CHANGE_CLASS = "future_live_observation_launcher_or_result_acceptance_only"

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


class ScoutPostRunProvenanceSourceReviewHold(ValueError):
    """The source chain drifted or an effectful action was requested."""


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ScoutPostRunProvenanceSourceReviewHold(code)


def scout_post_run_provenance_source_review_contract() -> dict[str, Any]:
    prior = backend_review.scout_post_run_backend_source_binding_review_contract()
    candidate = bundle.scout_post_run_provenance_bundle_contract()

    _require(
        prior.get("next_gate")
        == "SCOUT_POST_RUN_LIVE_OBSERVATION_REQUIRES_SEPARATE_AUTHORIZATION",
        "SCOUT_PROVENANCE_PRIOR_GATE_DRIFT",
    )
    _require(
        prior.get("source_only_backend_gap_closed") is True,
        "SCOUT_PROVENANCE_BACKEND_REVIEW_INCOMPLETE",
    )
    _require(
        prior.get("actual_host_observation_performed") is False,
        "SCOUT_PROVENANCE_PRIOR_HOST_OBSERVATION_DRIFT",
    )
    _require(
        all(value is False for value in prior["authority"].values()),
        "SCOUT_PROVENANCE_PRIOR_AUTHORITY_DRIFT",
    )

    _require(
        candidate.get("accepted_war_college_commit_serialized") is True,
        "SCOUT_PROVENANCE_WAR_COLLEGE_BINDING_MISSING",
    )
    _require(
        candidate.get("expected_engine_commit_serialized") is True,
        "SCOUT_PROVENANCE_ENGINE_BINDING_MISSING",
    )
    _require(
        candidate.get("engine_container_name_serialized") is True,
        "SCOUT_PROVENANCE_CONTAINER_BINDING_MISSING",
    )
    _require(
        candidate.get("post_run_state_digest_bound") is True,
        "SCOUT_PROVENANCE_STATE_DIGEST_BINDING_MISSING",
    )
    _require(
        candidate.get("backend_collection_and_binding_share_same_inputs") is True,
        "SCOUT_PROVENANCE_INPUT_COHERENCE_MISSING",
    )
    _require(
        candidate.get("attempt_marker_path_raw_publication") is False
        and candidate.get("attempt_directory_identity_raw_publication") is False,
        "SCOUT_PROVENANCE_LOCAL_IDENTITY_PUBLICATION_DRIFT",
    )
    _require(
        candidate.get("automatic_host_backend_selection") is False
        and candidate.get("contract_call_performs_host_observation") is False,
        "SCOUT_PROVENANCE_HOST_BOUNDARY_DRIFT",
    )
    _require(
        candidate.get("historical_v1_schema_rewritten") is False,
        "SCOUT_PROVENANCE_HISTORICAL_SCHEMA_DRIFT",
    )
    _require(
        candidate.get("final_result_acceptance") is False,
        "SCOUT_PROVENANCE_FINAL_ACCEPTANCE_DRIFT",
    )
    _require(
        candidate.get("next_gate")
        == "SCOUT_POST_RUN_PROVENANCE_BINDING_SOURCE_REVIEW_REQUIRED",
        "SCOUT_PROVENANCE_CANDIDATE_GATE_DRIFT",
    )
    _require(
        candidate.get("source_references")
        == {
            bundle.BACKEND_PATH: bundle.BACKEND_GIT_BLOB,
            bundle.BACKEND_REVIEW_PATH: bundle.BACKEND_REVIEW_GIT_BLOB,
            bundle.OBSERVER_PATH: bundle.OBSERVER_GIT_BLOB,
            bundle.OBSERVER_CONTRACT_PATH: bundle.OBSERVER_CONTRACT_GIT_BLOB,
        },
        "SCOUT_PROVENANCE_UPSTREAM_SOURCE_BINDING_DRIFT",
    )
    _require(
        all(value is False for value in candidate["authority"].values()),
        "SCOUT_PROVENANCE_CANDIDATE_AUTHORITY_DRIFT",
    )

    return {
        "schema": REVIEW_SCHEMA,
        "accepted_base_main_head": ACCEPTED_BASE_MAIN_HEAD,
        "source_references": {
            BUNDLE_PATH: BUNDLE_GIT_BLOB,
            BUNDLE_TEST_PATH: BUNDLE_TEST_GIT_BLOB,
            BACKEND_REVIEW_PATH: BACKEND_REVIEW_GIT_BLOB,
        },
        "provenance_bundle_source_binding_present": True,
        "provenance_bundle_regression_binding_present": True,
        "backend_review_binding_preserved": True,
        "historical_v1_state_schema_preserved": True,
        "accepted_war_college_commit_bound": True,
        "expected_engine_commit_bound": True,
        "engine_container_name_bound": True,
        "post_run_state_digest_bound": True,
        "local_marker_path_raw_publication": False,
        "local_directory_identity_raw_publication": False,
        "automatic_backend_selection": False,
        "actual_host_observation_performed": False,
        "actual_scout_execution_authorized": False,
        "actual_scout_execution_performed": False,
        "final_result_acceptance": False,
        "source_only_provenance_gap_closed": True,
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "provenance_contract": deepcopy(candidate),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def observe_live_host(*args: Any, **kwargs: Any) -> None:
    raise ScoutPostRunProvenanceSourceReviewHold(NEXT_GATE)


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise ScoutPostRunProvenanceSourceReviewHold(NEXT_GATE)


def accept_result(*args: Any, **kwargs: Any) -> None:
    raise ScoutPostRunProvenanceSourceReviewHold(NEXT_GATE)
