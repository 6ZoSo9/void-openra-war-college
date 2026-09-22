"""Accept exact completed Precision evidence for V2R13 pair-03 candidate.

This source binds the already completed one-shot candidate execution and its
preserved baseline reference. It records a valid completed measurement only.
It does not replay execution, authorize another attempt, train, update weights,
promote policy, deploy, mutate VOID, or touch wallets/funds.

Importing or inspecting this module performs no host action.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_invocation_source_binding_review_generation2
    as invocation_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-candidate-execution-evidence-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair03-candidate-execution-evidence-acceptance.v1"
)

EXECUTION_MAIN_HEAD = "ea218d29cf6ae55058754379159d318cd1be71aa"
EXECUTION_MAIN_TREE = "10a8af4cb4b6ef178fbdac656aee951d214d9853"
VALIDATION_MAIN_HEAD = "f32437d2dbbb3a5e702f661494e427c30f6e6136"

INVOCATION_SOURCE_SHA256 = (
    "1df36c53c6e7d1f6ff07f732e792e6fdcaab7a8d0d5b9d8249851b78e11202c0"
)
ATTEMPT_MARKER_SHA256 = (
    "0ab9062efa497457a6e7d42a149e302b3809887f54c7b1e1112b86b5ec2d7f79"
)
RESULT_FILE_SHA256 = (
    "9be2b3a74205cd6102f5839171638431ef25cb4f57db1028033ef2498f740829"
)
EXECUTOR_RECEIPT_SHA256 = (
    "396c9e535ab92ada204aee31e1442fa68841adcbd2b231709d945f72c0bf78f9"
)
REQUEST_SHA256 = (
    "5025174efdf945f206119c1f25cb3a5d07bcb87ed3de8ccd93e3d9b1e3354a87"
)

RUN_ID = "warmstart-apollyon-vs-abaddon-20260920T154029Z-feinter-s1990061685"
RUN_DIR = (
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2/"
    "generation2/pair-03/candidate/runs/" + RUN_ID
)
OUTCOME = "DRAW_OR_UNFINISHED"
ROUNDS_COMPLETED = 36
FINAL_TICK = 3551
SEED = 1990061685
WARM_START_HANDOFF_TICK = 2651
WARM_START_SHA256 = (
    "334846e59a956c1f8e059979f56c1775b39e1d51ef42c172e09fc7ab022a8a3a"
)
TRAJECTORY_SHA256 = (
    "2880cb09bd9afd15d8dbb7436bcc7831191821f5a0be6badeece72e264645d65"
)
SUMMARY_SHA256 = (
    "0819a0714a40dffb79208e5d35e01723143fe9a36eaf2a6feb988fcb4e76a5a0"
)

BASELINE_RUN_ID = "warmstart-apollyon-vs-abaddon-20260919T203512Z-feinter-s1990061685"
BASELINE_TRAJECTORY_SHA256 = (
    "27741699e08e367e66177d8bcd6bc2244d2c21b804fe250101b8ef0b6c7165b9"
)
BASELINE_SUMMARY_SHA256 = (
    "d37ab54fa8db2269a5ac61ca0880f7ae189188f0eea144031e484815bcdf7d6"
)

EXPECTED_EVIDENCE = {
    "execution_main_head": EXECUTION_MAIN_HEAD,
    "execution_main_tree": EXECUTION_MAIN_TREE,
    "validation_main_head": VALIDATION_MAIN_HEAD,
    "execution_main_ancestor_of_validation_main": True,
    "invocation_source_identity_retained": True,
    "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
    "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
    "result_file_sha256": RESULT_FILE_SHA256,
    "request_sha256": REQUEST_SHA256,
    "executor_receipt_sha256": EXECUTOR_RECEIPT_SHA256,
    "pair_slot": 3,
    "arm": "candidate",
    "held_out": False,
    "candidate_specific_call_confirmed": True,
    "operator_authenticated": False,
    "candidate_attempt_consumed": True,
    "candidate_completed_result_present": True,
    "candidate_execution_performed": True,
    "candidate_execution_replay_required": False,
    "candidate_execution_replay_permitted": False,
    "completed_baseline_preserved": True,
    "run_id": RUN_ID,
    "run_dir": RUN_DIR,
    "outcome": OUTCOME,
    "rounds_completed": ROUNDS_COMPLETED,
    "final_tick": FINAL_TICK,
    "seed": SEED,
    "warm_start_handoff_tick": WARM_START_HANDOFF_TICK,
    "warm_start_sha256": WARM_START_SHA256,
    "trajectory_sha256": TRAJECTORY_SHA256,
    "summary_sha256": SUMMARY_SHA256,
    "baseline_run_id": BASELINE_RUN_ID,
    "baseline_trajectory_sha256": BASELINE_TRAJECTORY_SHA256,
    "baseline_summary_sha256": BASELINE_SUMMARY_SHA256,
    "runtime_execution_authorized": True,
    "runtime_execution_performed": True,
    "runtime_started": True,
    "runtime_cleanup_attempted": True,
    "runtime_cleanup_completed": True,
    "fresh_runtime_readiness_admitted": True,
    "revocation_checked_before_materialization": True,
    "revocation_checked_before_inference": True,
    "automatic_retry": False,
    "training_performed": False,
    "weights_updated": False,
    "automatic_policy_promotion": False,
    "deployment_performed": False,
    "void_chain_mutation_performed": False,
    "wallet_or_funds_action_performed": False,
    "automatic_corpus_admission": False,
    "automatic_apollyon_weight_mutation": False,
    "automatic_abaddon_policy_promotion": False,
}

NEXT_GATE = (
    "V2R13_PAIR03_CANDIDATE_EXECUTION_EVIDENCE_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_v2r13_pair03_candidate_execution_evidence_review"
)


class V2R13Pair03CandidateExecutionEvidenceAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair03CandidateExecutionEvidenceAcceptanceHold(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


EXPECTED_EVIDENCE_SHA256 = _digest(EXPECTED_EVIDENCE)


def _validate_dependency() -> dict[str, Any]:
    reviewed = (
        invocation_review
        .v2r13_pair03_candidate_invocation_source_binding_review_contract()
    )
    _require(
        reviewed.get("candidate_invocation_source_binding_present") is True,
        "candidate invocation source binding missing",
    )
    _require(
        reviewed.get("candidate_invocation_reviewed") is True,
        "candidate invocation not reviewed",
    )
    _require(reviewed.get("pair_slot") == 3, "candidate pair-slot drift")
    _require(reviewed.get("arm") == "candidate", "candidate arm drift")
    _require(reviewed.get("held_out") is False, "candidate held-out drift")
    _require(
        reviewed.get("candidate_specific_operator_authorization_accepted") is False,
        "source review unexpectedly carries operator authority",
    )
    _require(
        reviewed.get("runtime_execution_authorized") is False,
        "source review unexpectedly carries runtime authority",
    )
    _require(reviewed.get("automatic_retry") is False, "automatic retry enabled")
    return deepcopy(reviewed)


def accept_pair03_candidate_execution_evidence(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    dependency = _validate_dependency()
    _require(isinstance(evidence, Mapping), "candidate evidence must be object")
    supplied = dict(evidence)
    _require(
        set(supplied) == set(EXPECTED_EVIDENCE),
        "candidate evidence field-set drift",
    )
    for field, expected in EXPECTED_EVIDENCE.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"candidate evidence drift: {field}",
        )
    _require(
        _digest(supplied) == EXPECTED_EVIDENCE_SHA256,
        "candidate evidence digest drift",
    )

    return {
        "schema": ACCEPTANCE_SCHEMA,
        "candidate_execution_evidence_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "execution_main_head": EXECUTION_MAIN_HEAD,
        "validation_main_head": VALIDATION_MAIN_HEAD,
        "pair_slot": 3,
        "arm": "candidate",
        "held_out": False,
        "candidate_attempt_consumed": True,
        "candidate_execution_performed": True,
        "candidate_completed_result_present": True,
        "candidate_execution_replay_required": False,
        "candidate_execution_replay_permitted": False,
        "runtime_cleanup_completed": True,
        "fresh_runtime_readiness_admitted": True,
        "completed_baseline_preserved": True,
        "outcome": OUTCOME,
        "rounds_completed": ROUNDS_COMPLETED,
        "run_id": RUN_ID,
        "trajectory_sha256": TRAJECTORY_SHA256,
        "summary_sha256": SUMMARY_SHA256,
        "baseline_trajectory_sha256": BASELINE_TRAJECTORY_SHA256,
        "baseline_summary_sha256": BASELINE_SUMMARY_SHA256,
        "automatic_retry": False,
        "another_candidate_execution_authorized": False,
        "pair09_execution_authorized": False,
        "held_out_execution_authorized": False,
        "training_authorized": False,
        "training_performed": False,
        "weights_update_authorized": False,
        "weights_updated": False,
        "automatic_policy_promotion_authorized": False,
        "automatic_policy_promotion": False,
        "deployment_authorized": False,
        "deployment_performed": False,
        "void_chain_mutation_authorized": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_authorized": False,
        "wallet_or_funds_action_performed": False,
        "candidate_result_review_required": True,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "evidence": deepcopy(supplied),
        "invocation_review": dependency,
    }


def v2r13_pair03_candidate_execution_evidence_acceptance_contract() -> dict[str, Any]:
    accepted = accept_pair03_candidate_execution_evidence(EXPECTED_EVIDENCE)
    return {
        **accepted,
        "contract_schema": CONTRACT_SCHEMA,
        "accepted_evidence": deepcopy(accepted["evidence"]),
    }


def authorize_follow_on_execution(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair03CandidateExecutionEvidenceAcceptanceHold(NEXT_GATE)
