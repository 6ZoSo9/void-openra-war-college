"""Source-only review of the explicit one-shot pair-03 candidate invocation.

This separate instrument pins the exact candidate invocation implementation and
its adversarial test surface.  It validates the fixed pair/arm scope, source
dependencies, single-use attempt requirement and request-side runtime gates
without collecting host state or invoking the candidate.

This review is not operator authentication and is not execution authority.
After it closes the source-review requirement, the candidate remains held at
the explicit pair-03 candidate execution authorization gate.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_authorization_request_generation2
    as request,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_invocation_generation2
    as invocation,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-candidate-invocation-source-binding-review-contract.v1"
)
REVIEW_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-candidate-invocation-source-binding-review.v1"
)

INVOCATION_GIT_BLOB = "a790b5b1568b42b1a629a525387366d2bb499128"
INVOCATION_SOURCE_SHA256 = (
    "1df36c53c6e7d1f6ff07f732e792e6fdcaab7a8d0d5b9d8249851b78e11202c0"
)
INVOCATION_TEST_GIT_BLOB = "4823d4cbb6824dcd8b0628b70d611a321c12bc10"
INVOCATION_TEST_SHA256 = (
    "24330d7aeb436926e27d875abf9532164a35c2d17080e6f8d3d63791f01309ac"
)
REQUEST_GIT_BLOB = "07516a24553b2516b859bebca21818c0bd0bf01e"
ATTEMPT_GUARD_GIT_BLOB = "b47a2befd6d7181aa5a00805ae20e66293625d45"
HOST_PREFLIGHT_GIT_BLOB = "32c27cacdcd850022bd3de358f82554112c6fd7b"
GIT_BACKEND_GIT_BLOB = "fe578c66b14e08c64e9281a808064b8c8d5e739a"
BOUNDED_EXECUTOR_GIT_BLOB = "c7e20c1157e0bcf7f65036631aad47fb82c7aefd"
FIRST_BASELINE_INVOCATION_GIT_BLOB = "5b790efaf4085deb15eaef538635fd11f5cad9a5"

PAIR_SLOT = 3
ARM = "candidate"
HELD_OUT = False
CONFIRM_TOKEN = "VOID_ABADDON_GENERATION2_V2R13_EXECUTE_PAIR03_CANDIDATE_ONCE"
NEXT_GATE = "V2R13_PAIR03_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
NEXT_CHANGE_CLASS = "trusted_operator_v2r13_pair03_candidate_execution_authorization"

EXPECTED_PINNED_SOURCES = {
    "openra_env/learning/abaddon_policy_campaign_runtime_v2r13_pair03_candidate_authorization_request_generation2.py":
        REQUEST_GIT_BLOB,
    "openra_env/learning/abaddon_policy_campaign_runtime_v2r13_pair03_candidate_attempt_guard_generation2.py":
        ATTEMPT_GUARD_GIT_BLOB,
    "openra_env/learning/abaddon_policy_campaign_runtime_v2r13_pair03_candidate_host_preflight_generation2.py":
        HOST_PREFLIGHT_GIT_BLOB,
    "openra_env/learning/abaddon_policy_campaign_runtime_v2r13_pair03_candidate_git_backend_generation2.py":
        GIT_BACKEND_GIT_BLOB,
    "openra_env/learning/abaddon_policy_campaign_runtime_v2r13_host_preflight_generation2.py":
        "0ae27981a08b27083b235ae4807705c88da259a1",
    "tools/abaddon_policy_campaign_runtime_v2r13_precision_host_preflight_generation2.py":
        "62d8a906ea41138b5443ba3bf96799b6e430b5be",
}

REQUIRED_REQUEST_GATES = {
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
}


class V2R13Pair03CandidateInvocationSourceBindingReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03CandidateInvocationSourceBindingReviewHold(message)


@lru_cache(maxsize=1)
def _validate_dependencies_cached() -> dict[str, Any]:
    proposal = request.candidate_authorization_request_contract()

    _require(invocation.CONFIRM_TOKEN == CONFIRM_TOKEN, "candidate confirmation token drift")
    _require(str(invocation.SOURCE_ROOT) == "/home/zoso/dev/openra-rl-war-college", "candidate source root drift")
    _require(
        str(invocation.ISOLATED_ROOT)
        == "/home/zoso/dev/void-war-college-execution/v2r13-generation2",
        "candidate isolated root drift",
    )
    _require(
        str(invocation.CANDIDATE_ROOT)
        == (
            "/home/zoso/dev/void-war-college-execution/v2r13-generation2/"
            "generation2/pair-03/candidate"
        ),
        "candidate arm root drift",
    )
    _require(invocation.CLAIMS_NAME == "pair03-candidate-claims-v1", "candidate claim namespace drift")
    _require(
        invocation.RESULT_NAME == "pair-03-candidate-execution-result-v1.json",
        "candidate result name drift",
    )
    _require(invocation.REVOCATION_NAME == "REVOKE_V2R13", "candidate revocation sentinel drift")
    _require(callable(invocation.execute_pair03_candidate), "candidate invocation entrypoint missing")

    observed_pins = dict(invocation.PINNED_SOURCES)
    for path, blob in EXPECTED_PINNED_SOURCES.items():
        _require(observed_pins.get(path) == blob, f"candidate pinned dependency drift: {path}")
    _require(
        set(observed_pins) == set(EXPECTED_PINNED_SOURCES),
        "candidate pinned dependency field-set drift",
    )

    _require(proposal.get("next_gate") == NEXT_GATE, "candidate request frontier drift")
    request_record = proposal.get("request")
    _require(isinstance(request_record, dict), "candidate request record missing")
    _require(
        set(request_record.get("required_runtime_gates", ())) == REQUIRED_REQUEST_GATES,
        "candidate request runtime-gate set drift",
    )
    scope = request_record.get("proposed_scope")
    _require(isinstance(scope, dict), "candidate request scope missing")
    _require(scope.get("pair_slot") == PAIR_SLOT, "candidate request pair-slot drift")
    _require(scope.get("arm") == ARM, "candidate request arm drift")
    _require(scope.get("held_out") is HELD_OUT, "candidate request held-out drift")
    _require(scope.get("maximum_candidate_attempts") == 1, "candidate attempt bound drift")
    _require(scope.get("maximum_automatic_retries") == 0, "candidate retry bound drift")

    authority = request_record.get("authority")
    _require(isinstance(authority, dict), "candidate request authority record missing")
    _require(authority and all(value is False for value in authority.values()), "candidate request already carries authority")
    _require(
        request_record.get("legacy_six_arm_authorization_sufficient") is False,
        "legacy broad authority became sufficient",
    )
    _require(
        request_record.get("matching_request_digest_grants_authority") is False,
        "request digest unexpectedly grants authority",
    )

    return {
        "candidate_authorization_request": deepcopy(proposal),
        "candidate_invocation_pinned_sources": deepcopy(observed_pins),
    }


def _validate_dependencies() -> dict[str, Any]:
    return deepcopy(_validate_dependencies_cached())


def v2r13_pair03_candidate_invocation_source_binding_review() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    return {
        "schema": REVIEW_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "candidate_invocation_implemented": True,
        "candidate_invocation_source_binding_present": True,
        "candidate_invocation_reviewed": True,
        "candidate_invocation_source_identity_pinned_by_git_blob": True,
        "candidate_invocation_source_identity_pinned_by_sha256": True,
        "candidate_invocation_test_identity_pinned_by_git_blob": True,
        "candidate_invocation_test_identity_pinned_by_sha256": True,
        "candidate_invocation_source_is_not_self_bound": True,
        "separate_review_instrument": True,
        "candidate_specific_confirmation_required": True,
        "candidate_specific_operator_authorization_accepted": False,
        "operator_authenticated": False,
        "single_use_attempt_required": True,
        "fresh_current_main_preflight_required": True,
        "cached_sudo_required": True,
        "live_revocation_sentinel_absent_required": True,
        "isolated_grpc_python_required": True,
        "exact_model_preload_before_readiness_without_inference_required": True,
        "canonical_worktree_observation_required": True,
        "fresh_canonical_live_readiness_before_inference_required": True,
        "exact_baseline_evidence_reverification_required": True,
        "create_only_attempt_consumption_required": True,
        "completed_baseline_preservation_required": True,
        "result_create_only_required": True,
        "runtime_execution_authorized": False,
        "runtime_execution_invoked_by_review": False,
        "candidate_execution_performed_by_review": False,
        "model_inference_performed_by_review": False,
        "game_execution_performed_by_review": False,
        "automatic_retry": False,
        "held_out_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "dependencies": dependencies,
    }


def v2r13_pair03_candidate_invocation_source_binding_review_contract() -> dict[str, Any]:
    review = v2r13_pair03_candidate_invocation_source_binding_review()
    return {
        "schema": CONTRACT_SCHEMA,
        "invocation_git_blob": INVOCATION_GIT_BLOB,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "invocation_test_git_blob": INVOCATION_TEST_GIT_BLOB,
        "invocation_test_sha256": INVOCATION_TEST_SHA256,
        "request_git_blob": REQUEST_GIT_BLOB,
        "attempt_guard_git_blob": ATTEMPT_GUARD_GIT_BLOB,
        "host_preflight_git_blob": HOST_PREFLIGHT_GIT_BLOB,
        "git_backend_git_blob": GIT_BACKEND_GIT_BLOB,
        "bounded_executor_git_blob": BOUNDED_EXECUTOR_GIT_BLOB,
        "first_baseline_invocation_git_blob": FIRST_BASELINE_INVOCATION_GIT_BLOB,
        "candidate_invocation_source_identity_pinned_by_git_blob": True,
        "candidate_invocation_source_identity_pinned_by_sha256": True,
        "candidate_invocation_test_identity_pinned_by_git_blob": True,
        "candidate_invocation_test_identity_pinned_by_sha256": True,
        "candidate_invocation_source_is_not_self_bound": True,
        "separate_review_instrument": True,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "candidate_invocation_implemented": True,
        "candidate_invocation_source_binding_present": True,
        "candidate_invocation_reviewed": True,
        "candidate_specific_operator_authorization_accepted": False,
        "operator_authenticated": False,
        "runtime_execution_authorized": False,
        "runtime_execution_invoked_by_review": False,
        "candidate_execution_performed_by_review": False,
        "review_host_observation_implemented": False,
        "review_filesystem_mutation_implemented": False,
        "review_git_query_implemented": False,
        "review_subprocess_execution_implemented": False,
        "review_network_request_implemented": False,
        "review_ollama_request_implemented": False,
        "review_docker_command_implemented": False,
        "review_service_action_implemented": False,
        "review_model_load_implemented": False,
        "review_model_inference_implemented": False,
        "review_game_execution_implemented": False,
        "review_training_implemented": False,
        "review_deployment_implemented": False,
        "review_void_chain_mutation_implemented": False,
        "review_wallet_or_funds_action_implemented": False,
        "automatic_retry": False,
        "held_out_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "review": deepcopy(review),
    }


def authorize_or_execute_candidate(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03CandidateInvocationSourceBindingReviewHold(NEXT_GATE)
