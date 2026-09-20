"""Fixed, non-executable authorization request for the pair-03 candidate.

This is a proposal, not an authorization record or a runtime permit. The
validator admits only the exact request bytes built here; it does not parse
caller JSON, authenticate an operator, read evidence/source files, prove host
readiness, consume an attempt, or invoke the existing six-arm executor.

Source references are reviewed identity expectations, not a complete transitive
inventory or a claim that this function verified their current on-disk bytes.
A future accepting/invoking implementation must independently enforce the
listed gates. A matching request digest alone can never authorize execution.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

REQUEST_SCHEMA = "void.abaddon.generation2.v2r13-pair03-candidate-authorization-request.v1"
RESULT_SCHEMA = "void.abaddon.generation2.v2r13-pair03-candidate-request-validation.v1"
NEXT_GATE = "V2R13_PAIR03_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
MAX_REQUEST_BYTES = 16384
PREPARATION_MAIN_HEAD = "1c9683a207c67e74afbc08a9373973c4a9e0bba7"

_PREFIX = "openra_env/learning/abaddon_policy_campaign_"
SOURCE_REFERENCES = (
    (_PREFIX + "runtime_v2r13_pair03_candidate_execution_preparation_review_generation2.py",
     "ac9d21c6c18b8247b06460ea35240f7fbc810625"),
    (_PREFIX + "runtime_v2r13_pair03_baseline_result_review_generation2.py",
     "877c9dd0969b1b2220f5d886da7521aa756a9742"),
    (_PREFIX + "runtime_v2r13_bounded_executor_generation2.py",
     "c7e20c1157e0bcf7f65036631aad47fb82c7aefd"),
    (_PREFIX + "runtime_v2r13_first_baseline_invocation_generation2.py",
     "5b790efaf4085deb15eaef538635fd11f5cad9a5"),
    (_PREFIX + "command_materializer_generation2.py",
     "4836360e0d284454f815a2a2e32078d2565e6dea"),
    (_PREFIX + "runtime_activation_contract_generation2.py",
     "a3acb42280c334daa24a3b830105a04666fd603b"),
    ("tools/abaddon_policy_candidate_duel_wrapper.py",
     "61eaefee39ebd90df0ddd8c649d9f0f9b64b1776"),
    ("fixtures/learning/abaddon-policy-genome-generation-2-candidate-252.json",
     "20091bff54edbb567127722fae81e5a5308737d2"),
)

REQUIRED_RUNTIME_GATES = (
    "candidate_specific_operator_authorization_accepted",
    "exact_candidate_invocation_source_reviewed",
    "fresh_current_main_host_preflight",
    "cached_sudo_authority",
    "live_revocation_sentinel_absent",
    "isolated_grpc_python",
    "exact_model_preload_before_readiness_without_inference",
    "canonical_worktree_observation",
    "fresh_canonical_live_readiness_before_inference",
    "exact_baseline_trajectory_and_summary_reverified",
    "create_only_single_use_attempt_consumption",
)

FALSE_AUTHORITY_FIELDS = (
    "candidate_specific_authorization_accepted",
    "candidate_execution_authorized",
    "candidate_execution_performed",
    "candidate_invocation_implemented",
    "candidate_invocation_reviewed",
    "operator_authenticated",
    "source_inventory_verified",
    "baseline_evidence_bytes_verified",
    "runtime_readiness_verified",
    "authorization_consumption_implemented",
    "authorization_consumed",
    "held_out_execution_authorized",
    "another_baseline_retry_authorized",
    "automatic_retry",
    "training_authorized",
    "weights_update_authorized",
    "automatic_policy_promotion_authorized",
    "deployment_authorized",
    "void_chain_mutation_authorized",
    "wallet_or_funds_action_authorized",
)


class V2R13Pair03CandidateAuthorizationRequestHold(ValueError):
    """The request is not the exact proposal, or execution was requested."""


def _request_record() -> dict[str, Any]:
    # Fresh literals only: callers never receive a shared mutable snapshot.
    return {
        "schema": REQUEST_SCHEMA,
        "record_kind": "proposal_only_not_authorization",
        "preparation_main_head": PREPARATION_MAIN_HEAD,
        "source_references": dict(SOURCE_REFERENCES),
        "proposed_scope": {
            "pair_slot": 3,
            "arm": "candidate",
            "held_out": False,
            "maximum_candidate_attempts": 1,
            "maximum_automatic_retries": 0,
            "other_pair_slots_included": False,
            "baseline_rerun_included": False,
        },
        "baseline_reference": {
            "trajectory_sha256": "27741699e08e367e66177d8bcd6bc2244d2c21b804fe250101b8ef0b6c7165b9",
            "summary_sha256": "d37ab54fa8dbb2269a5ac61ca0880f7ae189188f0eea144031e484815bcdf7d6",
            "recorded_rounds_completed": 36,
            "recorded_outcome": "DRAW_OR_UNFINISHED",
            "recorded_outcome_decisive": False,
        },
        "candidate_reference": {
            "wrapper_sha256": "686f88836e73acf9c78bfc1417db735b11100c07c34ce8da291047edd99eea9f",
            "fixture_sha256": "3fabbe9bc9b44830ee8e13e748d84ada881c6a3604f40c27609a953cabfd7768",
            "semantic_genome_sha256": "8253ea5f1b3a709c8d64fb0432d13ac1c52ee82678e2f3b0ec730fe23d603089",
            "controller_sha256": "b235d4cff3e3953ed7c511de52c76ada7e1a47046295e104353b61ef09e11103",
            "refiner_sha256": "5c5c4e7260cebcc5afbe9e9bd4744846593b44658ed0088f2eddbcaffc43910b",
        },
        "runtime_reference": {
            "selection_key": "apollyon-v2r13-qualified-predecessor",
            "model_alias": "void-apollyon-candidate-v2r13:latest",
            "model_digest": "b52834ea46c10362e9bb20cd2e721716016bb36f800ddbc62e7fbaa24fb40932",
            "frozen_war_college_commit": "973802ef0a614e5afa782ff20e231e18966ae3e5",
            "frozen_war_college_tree": "d8a2af418af00e95ca0f203a2f0264851f2308c6",
            "frozen_engine_commit": "1607a7a6501d42a47638393ecef8b22831064932",
            "runtime_image_id": "sha256:79f2f6800382489a2a648839fc0d58e546384938439378aeea06461363de25f5",
        },
        "required_runtime_gates": list(REQUIRED_RUNTIME_GATES),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "legacy_six_arm_authorization_sufficient": False,
        "matching_request_digest_grants_authority": False,
        "runtime_gates_enforced_by_this_module": False,
        "next_gate": NEXT_GATE,
    }


def build_candidate_authorization_request() -> bytes:
    """Return the one canonical UTF-8 proposal, with one terminal LF."""
    return (json.dumps(
        _request_record(), sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    ) + "\n").encode("utf-8")


def validate_candidate_authorization_request(payload: bytes) -> dict[str, Any]:
    """Validate fixed bytes only; success never means permission to execute."""
    if type(payload) is not bytes:
        raise V2R13Pair03CandidateAuthorizationRequestHold("request must be exact bytes")
    if not 0 < len(payload) <= MAX_REQUEST_BYTES:
        raise V2R13Pair03CandidateAuthorizationRequestHold("request byte limit")
    # No caller-controlled JSON parser, coercion, hash, or runtime import.
    if payload != build_candidate_authorization_request():
        raise V2R13Pair03CandidateAuthorizationRequestHold("request bytes differ from fixed proposal")
    return {
        "schema": RESULT_SCHEMA,
        "request_bytes_valid": True,
        "request_sha256": hashlib.sha256(payload).hexdigest(),
        "request_byte_length": len(payload),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "next_gate": NEXT_GATE,
    }


def candidate_authorization_request_contract() -> dict[str, Any]:
    """Return a fresh proposal and its non-authorizing validation result."""
    result = validate_candidate_authorization_request(build_candidate_authorization_request())
    result["request"] = _request_record()
    return result


def authorize_or_execute_candidate(*args: Any, **kwargs: Any) -> None:
    """Remain closed even when supplied a valid request or historical permit."""
    raise V2R13Pair03CandidateAuthorizationRequestHold(NEXT_GATE)
