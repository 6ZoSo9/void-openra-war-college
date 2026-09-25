"""Source-only review of the third pair-06 preservation result.

This review closes the failed-attempt preservation lineage and re-establishes
the execution frontier for the already accepted one-shot GPU-gated pair-06
authorization. It does not create a new authorization and performs no host I/O,
attempt claim, model load, inference, game execution, training, deployment,
VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_third_failed_attempt_preservation_result_acceptance_generation2
    as preservation_result,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_preclaim_gpu_execution_authorization_acceptance_generation2
    as authorization,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-third-failed-attempt-preservation-result-review-contract.v1"
)

ACCEPTANCE_GIT_BLOB = "cf6b70a34704c9a7b19d0abf59ecad64ab663daf"
ACCEPTANCE_SOURCE_SHA256 = (
    "fe8bbf57daa7613e1ab474b1fb268b97a93acef923c1a6651ef407cfe76a5816"
)
ACCEPTANCE_TEST_GIT_BLOB = "8d5e61467a6346cf7c9dfeee5d87908d02314000"
ACCEPTANCE_TEST_SHA256 = (
    "c94a979e42c72560f0925c9ea7566304a95728e4b837efd0d662cdbf5fbc3a06"
)

AUTHORIZED_REQUEST_SHA256 = (
    "16f28e4df242c8ba8adb44061fe6d6793763e798f5115f876a3dbcf1b84838b2"
)
AUTHORIZED_MAIN_HEAD = "bcf0e38ac2e583b63e592ba1c0dc4446e05d2590"
AUTHORIZATION_ACCEPTANCE_GIT_BLOB = (
    "b1767053c72d53c3f713a986503d0806cdc9decc"
)
AUTHORIZATION_ACCEPTANCE_SOURCE_SHA256 = (
    "2465ced181f1dd3f44f1f4a04b892678258d0ddbb8eb011e9ae4e398d9de1932"
)

ATTEMPT_MARKER_SHA256 = (
    "3ad564f9102291516726e9a029d6c1b501efb82eaec407a02922b9501c85c0f3"
)
PRESERVATION_RECEIPT_LOGICAL_SHA256 = (
    "9a7ec01af0f80d7a0d0333c91fd5c07d9ae24e04eaf87455fb143385ec76070b"
)
PRESERVATION_RECEIPT_FILE_SHA256 = (
    "12a2da73143db442f5620065f8c270ef8026a641da2afa938203e51ceeaa43f4"
)
PRESERVATION_RECEIPT_BYTES = 3130

NEXT_GATE = "PAIR06_V8_RECEIPT_BOUND_PRECLAIM_GPU_PRECISION_EXECUTION_REQUIRED"
NEXT_CHANGE_CLASS = "trusted_operator_pair06_v8_receipt_bound_preclaim_gpu_execution"


class Pair06V8ThirdPreservationResultReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8ThirdPreservationResultReviewHold(message)


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    preserved = (
        preservation_result
        .pair06_v8_third_preservation_result_acceptance_contract()
    )
    authorized = (
        authorization
        .pair06_v8_preclaim_gpu_execution_authorization_acceptance_contract()
    )

    _require(
        preserved.get("pair06_v8_third_preservation_result_accepted") is True,
        "third preservation result not accepted",
    )
    _require(
        preserved.get("attempt_marker_sha256") == ATTEMPT_MARKER_SHA256,
        "third preserved marker drift",
    )
    _require(
        preserved.get("archive_name") == "baseline-3ad564f9"
        and preserved.get("third_failed_attempt_archived") is True
        and preserved.get("third_failed_attempt_deleted") is False,
        "third preservation archive state drift",
    )
    _require(
        preserved.get("prior_failed_attempt_archives_unchanged") is True,
        "prior pair06 archives changed",
    )
    _require(
        preserved.get("fresh_baseline_arm_root_available") is True,
        "fresh pair06 baseline root unavailable",
    )
    _require(
        preserved.get("authorized_execution_head_preserved")
        == AUTHORIZED_MAIN_HEAD,
        "authorized execution head preservation drift",
    )
    _require(
        preserved.get("runtime_retry_authorized") is False
        and preserved.get("automatic_retry") is False,
        "preservation unexpectedly authorizes retry",
    )
    _require(
        preserved.get("next_gate")
        == (
            "PAIR06_V8_THIRD_FAILED_ATTEMPT_PRESERVATION_RESULT_"
            "SOURCE_BINDING_REVIEW_REQUIRED"
        ),
        "third preservation result frontier drift",
    )

    evidence = preserved.get("accepted_evidence")
    _require(isinstance(evidence, dict), "third preservation evidence missing")
    _require(
        evidence.get("preservation_receipt_logical_sha256")
        == PRESERVATION_RECEIPT_LOGICAL_SHA256
        and evidence.get("preservation_receipt_file_sha256")
        == PRESERVATION_RECEIPT_FILE_SHA256
        and evidence.get("preservation_receipt_bytes")
        == PRESERVATION_RECEIPT_BYTES,
        "third preservation receipt identity drift",
    )

    _require(
        authorized.get("authorization_accepted") is True,
        "GPU-gated execution authorization not accepted",
    )
    _require(
        authorized.get("authorized_request_sha256")
        == AUTHORIZED_REQUEST_SHA256,
        "GPU-gated authorized request drift",
    )
    _require(
        authorized.get("authorized_main_head") == AUTHORIZED_MAIN_HEAD,
        "GPU-gated authorized main drift",
    )
    _require(
        authorized.get("maximum_attempts") == 1
        and authorized.get("automatic_retry") is False,
        "GPU-gated authorization cardinality drift",
    )
    _require(
        authorized.get("fresh_preclaim_gpu_observation_required") is True
        and authorized.get(
            "fresh_preclaim_gpu_observation_precedes_attempt_marker"
        )
        is True
        and authorized.get("zero_foreign_cuda0_compute_processes_required")
        is True,
        "GPU-gated authorization admission policy drift",
    )
    _require(
        authorized.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and authorized.get("minimum_cuda0_free_memory_fraction_denominator")
        == 10,
        "GPU-gated authorization threshold drift",
    )
    _require(
        authorized.get("receipt_bound_preclaim_gpu_execution_authorized")
        is True,
        "GPU-gated execution authority missing",
    )
    _require(
        authorized.get("authorization_reusable_after_attempt_claim") is False,
        "GPU-gated authorization post-claim reuse drift",
    )

    return {
        "preservation_result": deepcopy(preserved),
        "authorization": deepcopy(authorized),
    }


def pair06_v8_third_preservation_result_review_contract() -> dict[str, Any]:
    validated = _validated()
    return {
        "schema": CONTRACT_SCHEMA,
        "acceptance_git_blob": ACCEPTANCE_GIT_BLOB,
        "acceptance_source_sha256": ACCEPTANCE_SOURCE_SHA256,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "acceptance_test_sha256": ACCEPTANCE_TEST_SHA256,
        "authorization_acceptance_git_blob": (
            AUTHORIZATION_ACCEPTANCE_GIT_BLOB
        ),
        "authorization_acceptance_source_sha256": (
            AUTHORIZATION_ACCEPTANCE_SOURCE_SHA256
        ),
        "pair06_v8_third_preservation_result_reviewed": True,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "third_failed_attempt_archived": True,
        "third_failed_attempt_deleted": False,
        "fresh_baseline_arm_root_available": True,
        "preservation_receipt_logical_sha256": (
            PRESERVATION_RECEIPT_LOGICAL_SHA256
        ),
        "preservation_receipt_file_sha256": (
            PRESERVATION_RECEIPT_FILE_SHA256
        ),
        "preservation_receipt_bytes": PRESERVATION_RECEIPT_BYTES,
        "authorized_request_sha256": AUTHORIZED_REQUEST_SHA256,
        "authorized_main_head": AUTHORIZED_MAIN_HEAD,
        "existing_gpu_gated_authorization_accepted": True,
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "pair03_replay_authorized": False,
        "pair09_replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "host_io_performed_by_review": False,
        "validated": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8ThirdPreservationResultReviewHold(NEXT_GATE)
