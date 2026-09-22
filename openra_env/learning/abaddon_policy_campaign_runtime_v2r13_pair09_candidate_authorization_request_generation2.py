"""Fixed, non-executable authorization request for V2R13 pair-09 candidate.

This is a deterministic proposal, not an authorization record, operator
authentication, runtime permit, or execution receipt. Matching request bytes or
a matching digest never grant execution.

A future invocation must independently reverify the completed pair-09 baseline,
current source identities, host readiness, revocation state, candidate policy
binding, and create-only one-use attempt consumption.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

REQUEST_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-candidate-authorization-request.v1"
)
RESULT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-candidate-request-validation.v1"
)

NEXT_GATE = "V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
MAX_REQUEST_BYTES = 16384

_PREFIX = "openra_env/learning/abaddon_policy_campaign_"
SOURCE_REFERENCES = (
    (
        _PREFIX
        + "runtime_v2r13_pair09_candidate_execution_preparation_review_generation2.py",
        "2bdc9a8acd96fde976fc0e3a4a6d3e356307fc3f",
    ),
    (
        _PREFIX + "runtime_v2r13_pair09_baseline_result_review_generation2.py",
        "e0f663b144aa2036d7dba2a8d001f8f061f2f892",
    ),
    (
        _PREFIX + "runtime_v2r13_bounded_executor_generation2.py",
        "c7e20c1157e0bcf7f65036631aad47fb82c7aefd",
    ),
    (
        _PREFIX + "command_materializer_generation2.py",
        "4836360e0d284454f815a2a2e32078d2565e6dea",
    ),
    (
        "tools/abaddon_policy_candidate_duel_wrapper.py",
        "61eaefee39ebd90df0ddd8c649d9f0f9b64b1776",
    ),
    (
        "fixtures/learning/abaddon-policy-genome-generation-2-candidate-252.json",
        "20091bff54edbb567127722fae81e5a5308737d2",
    ),
)

REQUIRED_RUNTIME_GATES = (
    "pair09_candidate_specific_operator_authorization_accepted",
    "exact_pair09_candidate_invocation_source_reviewed",
    "fresh_current_main_host_preflight",
    "cached_sudo_authority",
    "live_revocation_sentinel_absent",
    "isolated_grpc_python",
    "exact_model_preload_before_readiness_without_inference",
    "canonical_worktree_observation",
    "fresh_canonical_live_readiness_before_inference",
    "exact_pair09_baseline_result_reverified",
    "exact_pair03_preserved_evidence_reverified",
    "exact_candidate_policy_binding_reverified",
    "create_only_pair09_candidate_attempt_consumption",
)

FALSE_AUTHORITY_FIELDS = (
    "pair09_candidate_specific_authorization_accepted",
    "pair09_candidate_execution_authorized",
    "pair09_candidate_execution_performed",
    "pair09_candidate_invocation_implemented",
    "pair09_candidate_invocation_reviewed",
    "operator_authenticated",
    "source_inventory_verified",
    "baseline_evidence_bytes_verified",
    "runtime_readiness_verified",
    "authorization_consumption_implemented",
    "authorization_consumed",
    "pair09_baseline_rerun_authorized",
    "held_out_execution_authorized",
    "automatic_retry",
    "training_authorized",
    "weights_update_authorized",
    "automatic_policy_promotion_authorized",
    "deployment_authorized",
    "void_chain_mutation_authorized",
    "wallet_or_funds_action_authorized",
)


class V2R13Pair09CandidateAuthorizationRequestHold(ValueError):
    pass


def _request_record() -> dict[str, Any]:
    return {
        "schema": REQUEST_SCHEMA,
        "record_kind": "proposal_only_not_authorization",
        "source_references": dict(SOURCE_REFERENCES),
        "preparation_source_sha256": (
            "6f4cea4ff326a4579a98456a6272c7bef6c44b3915446e2b5f20fce9b9d9a8ca"
        ),
        "preparation_test_git_blob": "df189ee056584e6f4dee2efef59248eb6619ce1d",
        "preparation_test_sha256": (
            "5836efff0033563d4b68003373fb5faa9741649bb595eba2bae447c969edd576"
        ),
        "proposed_scope": {
            "pair_slot": 9,
            "arm": "candidate",
            "held_out": False,
            "maximum_candidate_attempts": 1,
            "maximum_automatic_retries": 0,
            "baseline_rerun_included": False,
            "held_out_arm_included": False,
            "other_pair_slots_included": False,
        },
        "baseline_reference": {
            "seed": 1496195137,
            "round_limit": 36,
            "recorded_rounds_completed": 36,
            "recorded_outcome": "DRAW_OR_UNFINISHED",
            "recorded_outcome_decisive": False,
            "trajectory_sha256": (
                "103f4325d9ed91edf0e72982045e4f72e12bf40641e43915beeabb4c9e569700"
            ),
            "summary_sha256": (
                "48e8ce8d0c1a00163b88a5c4b3c23e7b057bcfb5d2b59977c67387c838a8f189"
            ),
            "result_file_sha256": (
                "86b8cf0ce07ff6135d43911b36870e481e028f10a288c26f29f858655dde0ec2"
            ),
            "attempt_marker_sha256": (
                "57f862fe39a8939f3d47d4184fe264e0b9cd3988143f4cdc3adb9973a0e2e41c"
            ),
        },
        "candidate_reference": {
            "wrapper_sha256": (
                "686f88836e73acf9c78bfc1417db735b11100c07c34ce8da291047edd99eea9f"
            ),
            "fixture_sha256": (
                "3fabbe9bc9b44830ee8e13e748d84ada881c6a3604f40c27609a953cabfd7768"
            ),
            "semantic_genome_sha256": (
                "8253ea5f1b3a709c8d64fb0432d13ac1c52ee82678e2f3b0ec730fe23d603089"
            ),
            "controller_sha256": (
                "b235d4cff3e3953ed7c511de52c76ada7e1a47046295e104353b61ef09e11103"
            ),
            "refiner_sha256": (
                "5c5c4e7260cebcc5afbe9e9bd4744846593b44658ed0088f2eddbcaffc43910b"
            ),
        },
        "runtime_reference": {
            "selection_key": "apollyon-v2r13-qualified-predecessor",
            "model_alias": "void-apollyon-candidate-v2r13:latest",
            "model_digest": (
                "b52834ea46c10362e9bb20cd2e721716016bb36f800ddbc62e7fbaa24fb40932"
            ),
            "frozen_war_college_commit": "973802ef0a614e5afa782ff20e231e18966ae3e5",
            "frozen_war_college_tree": "d8a2af418af00e95ca0f203a2f0264851f2308c6",
            "frozen_engine_commit": "1607a7a6501d42a47638393ecef8b22831064932",
            "runtime_image_id": (
                "sha256:79f2f6800382489a2a648839fc0d58e546384938439378aeea06461363de25f5"
            ),
        },
        "required_runtime_gates": list(REQUIRED_RUNTIME_GATES),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "legacy_six_arm_authorization_sufficient": False,
        "matching_request_digest_grants_authority": False,
        "runtime_gates_enforced_by_this_module": False,
        "next_gate": NEXT_GATE,
    }


def build_pair09_candidate_authorization_request() -> bytes:
    return (
        json.dumps(
            _request_record(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def validate_pair09_candidate_authorization_request(
    payload: bytes,
) -> dict[str, Any]:
    if type(payload) is not bytes:
        raise V2R13Pair09CandidateAuthorizationRequestHold(
            "request must be exact bytes"
        )
    if not 0 < len(payload) <= MAX_REQUEST_BYTES:
        raise V2R13Pair09CandidateAuthorizationRequestHold(
            "request byte limit"
        )
    if payload != build_pair09_candidate_authorization_request():
        raise V2R13Pair09CandidateAuthorizationRequestHold(
            "request bytes differ from fixed proposal"
        )
    return {
        "schema": RESULT_SCHEMA,
        "request_bytes_valid": True,
        "request_sha256": hashlib.sha256(payload).hexdigest(),
        "request_byte_length": len(payload),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "next_gate": NEXT_GATE,
    }


def pair09_candidate_authorization_request_contract() -> dict[str, Any]:
    result = validate_pair09_candidate_authorization_request(
        build_pair09_candidate_authorization_request()
    )
    return {**result, "request": _request_record()}


def authorize_or_execute_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09CandidateAuthorizationRequestHold(NEXT_GATE)
