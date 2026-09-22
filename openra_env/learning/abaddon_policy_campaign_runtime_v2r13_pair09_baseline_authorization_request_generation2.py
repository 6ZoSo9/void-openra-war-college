"""Fixed non-authorizing request for one V2R13 pair-09 baseline execution.

This module creates one canonical proposal for the next bounded evaluation step.
It is not operator authentication, an execution permit, host readiness proof,
or a reusable authority token. Matching bytes never grant execution.

The request binds the reviewed pair-09 design/preparation chain and requires a
future exact invocation source review plus fresh operation-time host gates.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

REQUEST_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-baseline-execution-authorization-request.v1"
)
RESULT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-baseline-execution-authorization-request-validation.v1"
)

NEXT_GATE = "V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
MAX_REQUEST_BYTES = 16384

_PREFIX = "openra_env/learning/abaddon_policy_campaign_"
SOURCE_REFERENCES = (
    (
        _PREFIX
        + "runtime_v2r13_pair09_baseline_execution_preparation_review_generation2.py",
        "f5242afc9947d52b26c0f89e1f1fe5906c3fa29f",
    ),
    (
        _PREFIX
        + "runtime_v2r13_pair09_evaluation_design_source_binding_review_generation2.py",
        "08a1a20a16dcceb2feb183d402edaff96f0cadfa",
    ),
    (
        _PREFIX + "runtime_v2r13_bounded_executor_generation2.py",
        "c7e20c1157e0bcf7f65036631aad47fb82c7aefd",
    ),
    (
        _PREFIX + "runtime_v2r13_first_baseline_invocation_generation2.py",
        "5b790efaf4085deb15eaef538635fd11f5cad9a5",
    ),
    (
        _PREFIX + "command_materializer_generation2.py",
        "4836360e0d284454f815a2a2e32078d2565e6dea",
    ),
)

REQUIRED_RUNTIME_GATES = (
    "pair09_baseline_specific_operator_authorization_accepted",
    "exact_pair09_baseline_invocation_source_reviewed",
    "fresh_current_main_host_preflight",
    "cached_sudo_authority",
    "live_revocation_sentinel_absent",
    "isolated_grpc_python",
    "exact_model_preload_before_readiness_without_inference",
    "canonical_worktree_observation",
    "fresh_canonical_live_readiness_before_inference",
    "create_only_pair09_baseline_attempt_consumption",
)

FALSE_AUTHORITY_FIELDS = (
    "pair09_baseline_specific_authorization_accepted",
    "pair09_baseline_execution_authorized",
    "pair09_baseline_execution_performed",
    "pair09_candidate_execution_authorized",
    "pair09_candidate_execution_performed",
    "held_out_execution_authorized",
    "held_out_execution_performed",
    "operator_authenticated",
    "source_inventory_verified",
    "runtime_readiness_verified",
    "authorization_consumption_implemented",
    "authorization_consumed",
    "automatic_retry",
    "training_authorized",
    "weights_update_authorized",
    "automatic_policy_promotion_authorized",
    "deployment_authorized",
    "void_chain_mutation_authorized",
    "wallet_or_funds_action_authorized",
)


class V2R13Pair09BaselineAuthorizationRequestHold(ValueError):
    pass


def _request_record() -> dict[str, Any]:
    return {
        "schema": REQUEST_SCHEMA,
        "record_kind": "proposal_only_not_authorization",
        "source_references": dict(SOURCE_REFERENCES),
        "proposed_scope": {
            "pair_slot": 9,
            "arm": "baseline",
            "held_out": False,
            "maximum_baseline_attempts": 1,
            "maximum_automatic_retries": 0,
            "candidate_arm_included": False,
            "held_out_arm_included": False,
            "pair03_replay_included": False,
        },
        "evaluation_order": {
            "baseline_first": True,
            "candidate_must_wait_for_baseline_result_review": True,
        },
        "runtime_reference": {
            "selection_key": "apollyon-v2r13-qualified-predecessor",
        },
        "required_runtime_gates": list(REQUIRED_RUNTIME_GATES),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "historical_pair03_runtime_authority_sufficient": False,
        "legacy_six_arm_authorization_sufficient": False,
        "matching_request_digest_grants_authority": False,
        "runtime_gates_enforced_by_this_module": False,
        "next_gate": NEXT_GATE,
    }


def build_pair09_baseline_authorization_request() -> bytes:
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


def validate_pair09_baseline_authorization_request(
    payload: bytes,
) -> dict[str, Any]:
    if type(payload) is not bytes:
        raise V2R13Pair09BaselineAuthorizationRequestHold(
            "request must be exact bytes"
        )
    if not 0 < len(payload) <= MAX_REQUEST_BYTES:
        raise V2R13Pair09BaselineAuthorizationRequestHold(
            "request byte limit"
        )
    if payload != build_pair09_baseline_authorization_request():
        raise V2R13Pair09BaselineAuthorizationRequestHold(
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


def pair09_baseline_authorization_request_contract() -> dict[str, Any]:
    result = validate_pair09_baseline_authorization_request(
        build_pair09_baseline_authorization_request()
    )
    return {**result, "request": _request_record()}


def authorize_or_execute_pair09_baseline(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09BaselineAuthorizationRequestHold(NEXT_GATE)
