"""Accept exact durable evidence for the completed V2R13 pair-09 candidate.

This source binds the single authorized pair-09 candidate execution completed
on Precision. It records exact attempt/result identities, run artifact hashes,
candidate policy binding, readiness/receipt identities, preserved predecessor
evidence, and post-run cleanup state.

Import or contract inspection performs no host action. This module grants no
replay, held-out, training, promotion, deployment, VOID-chain, wallet, or funds
authority.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_invocation_source_binding_review_generation2
    as invocation_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-candidate-execution-evidence-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-pair09-candidate-execution-evidence-acceptance.v1"
)

INVOCATION_REVIEW_GIT_BLOB = "97120289508d7baff306ef8c9b3a3f320d011180"
INVOCATION_REVIEW_SOURCE_SHA256 = (
    "f86db879a7d3c2971a5c88a0ff5fb293bc2c3f22a8738c12102da14b3533fd72"
)

LAUNCHER_SHA256 = (
    "0705afdb696da7e2c3208f981a13a4e179548e9c526352475728001486137d94"
)
EXECUTION_MAIN_HEAD = "7d5bf4c41c8a210a05fd9948f898c6cd8e5702d5"
EXECUTION_MAIN_TREE = "80f162601437c6701658eb6ef7cbb1dde7d2dfbd"
INVOCATION_SOURCE_SHA256 = (
    "4858f3fe148829d050604746cd64fa426963370a71029f95d7cc40bb71b5ba7c"
)
SOURCE_BINDINGS_SHA256 = (
    "d9a0226529c241f7af21c8fb2018c3297afc3000af12a397cc02e4d70c7b6232"
)

ATTEMPT_MARKER_SHA256 = (
    "b7bd2dc0ac29bfe1095fe1d03e117708184a97499832859a9b068ecde13d5ce9"
)
RESULT_FILE_SHA256 = (
    "68d86cea4a9806fca60a0bff765dce1227962acb923d6e4da3b5f7b1ab5ccb74"
)
REQUEST_SHA256 = (
    "88cfb23ca671c6d4572e50611b875b4b5329d06ba447f6ee1aa7d69c63aeb12d"
)

RUN_ID = "warmstart-apollyon-vs-abaddon-20260923T115438Z-feinter-s1496195137"
RUN_DIR = (
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2/"
    "generation2/pair-09/candidate/runs/" + RUN_ID
)
SEED = 1496195137
OUTCOME = "DRAW_OR_UNFINISHED"
ROUNDS_COMPLETED = 36
FINAL_TICK = 3551
WARM_START_HANDOFF_TICK = 2651
WARM_START_SHA256 = (
    "e6f648dbf6710766869b5e5a3b0ec79c60e856d7c959e78cd93b1df8cfb3f1f8"
)
TRAJECTORY_SHA256 = (
    "d8de375133687e1296ff0f740bd9901eee24c65332ae8600ab03f724edcd0eae"
)
SUMMARY_SHA256 = (
    "15f4e21c8b2d9988c26f90a9fd3021ff017faef2ac1f6b289d0582cd6748f7e3"
)

EXECUTOR_RECEIPT_SHA256 = (
    "c45315944d5d195b904d56ed31eba9929088f626a9c53b0bdf40858002371b98"
)
AUTHORIZATION_ATTESTATION_SHA256 = (
    "34ad7143e876b91056f730de37ab470b6fd8a5f99d84aadefb178cabf87a2031"
)
PLAN_SHA256 = (
    "48d856e467dde996fa119a7ff801f5649ab7b5e1774b1a093dbf3be0d4014bf7"
)
FRESH_READINESS_ADMISSION_SHA256 = (
    "668073cb385b0a711cc53e2a65ecb1267e897f95c8a34287c281073fb637864f"
)
FRESH_READINESS_EVIDENCE_SHA256 = (
    "d2fcaa4580f74c6d2ae41fd4879ba94be06018af4a328f9a91efcd1a749c6677"
)
HOST_PREFLIGHT_SNAPSHOT_SHA256 = (
    "7cccc5291890801b2a435acfaf3fd85b5c65771180bc7963ceccaf359ec2bd2e"
)

CANDIDATE_FILE_SHA256 = (
    "3fabbe9bc9b44830ee8e13e748d84ada881c6a3604f40c27609a953cabfd7768"
)
CANDIDATE_GENOME_SHA256 = (
    "8253ea5f1b3a709c8d64fb0432d13ac1c52ee82678e2f3b0ec730fe23d603089"
)
CANDIDATE_WRAPPER_SHA256 = (
    "686f88836e73acf9c78bfc1417db735b11100c07c34ce8da291047edd99eea9f"
)
ABADDON_CONTROLLER_SHA256 = (
    "b235d4cff3e3953ed7c511de52c76ada7e1a47046295e104353b61ef09e11103"
)
ABADDON_REFINER_SHA256 = (
    "5c5c4e7260cebcc5afbe9e9bd4744846593b44658ed0088f2eddbcaffc43910b"
)
LEGACY_RUNNER_SHA256 = (
    "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
)

EXPECTED_EVIDENCE = {
    "launcher_sha256": LAUNCHER_SHA256,
    "execution_main_head": EXECUTION_MAIN_HEAD,
    "execution_main_tree": EXECUTION_MAIN_TREE,
    "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
    "source_bindings_sha256": SOURCE_BINDINGS_SHA256,
    "pair_slot": 9,
    "arm": "candidate",
    "held_out": False,
    "maximum_attempts": 1,
    "automatic_retry": False,
    "baseline_rerun": False,
    "attempt_consumed": True,
    "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
    "request_sha256": REQUEST_SHA256,
    "result_present": True,
    "result_file_sha256": RESULT_FILE_SHA256,
    "run_id": RUN_ID,
    "run_dir": RUN_DIR,
    "seed": SEED,
    "outcome": OUTCOME,
    "rounds_completed": ROUNDS_COMPLETED,
    "final_tick": FINAL_TICK,
    "warm_start_handoff_tick": WARM_START_HANDOFF_TICK,
    "warm_start_contact_achieved": False,
    "warm_start_sha256": WARM_START_SHA256,
    "trajectory_sha256": TRAJECTORY_SHA256,
    "summary_sha256": SUMMARY_SHA256,
    "actual_apollyon_vs_actual_abaddon": True,
    "controller_rows_joint_same_tick": True,
    "warm_start_rows_excluded_from_agent_training": True,
    "candidate_only": True,
    "automatic_corpus_admission": False,
    "automatic_apollyon_weight_mutation": False,
    "automatic_abaddon_policy_promotion": False,
    "candidate_file_sha256": CANDIDATE_FILE_SHA256,
    "candidate_genome_sha256": CANDIDATE_GENOME_SHA256,
    "wrapper_sha256": CANDIDATE_WRAPPER_SHA256,
    "legacy_runner_sha256": LEGACY_RUNNER_SHA256,
    "abaddon_controller_sha256": ABADDON_CONTROLLER_SHA256,
    "abaddon_refiner_sha256": ABADDON_REFINER_SHA256,
    "runtime_execution_authorized": True,
    "runtime_execution_performed": True,
    "runtime_started": True,
    "runtime_cleanup_attempted": True,
    "runtime_cleanup_completed": True,
    "fresh_runtime_readiness_admitted": True,
    "revocation_checked_before_materialization": True,
    "revocation_checked_before_inference": True,
    "executor_receipt_sha256": EXECUTOR_RECEIPT_SHA256,
    "authorization_attestation_sha256": AUTHORIZATION_ATTESTATION_SHA256,
    "plan_sha256": PLAN_SHA256,
    "fresh_readiness_admission_sha256": FRESH_READINESS_ADMISSION_SHA256,
    "fresh_readiness_evidence_sha256": FRESH_READINESS_EVIDENCE_SHA256,
    "host_preflight_snapshot_sha256": HOST_PREFLIGHT_SNAPSHOT_SHA256,
    "pair03_baseline_preserved": True,
    "pair03_candidate_preserved": True,
    "pair09_baseline_preserved": True,
    "held_out_execution_performed": False,
    "training_performed": False,
    "weights_updated": False,
    "automatic_policy_promotion": False,
    "deployment_performed": False,
    "void_chain_mutation_performed": False,
    "wallet_or_funds_action_performed": False,
    "ollama_active_after": "inactive",
    "ollama_enabled_after": "disabled",
    "activation_permit_present_after": False,
}

NEXT_GATE = (
    "V2R13_PAIR09_CANDIDATE_EXECUTION_EVIDENCE_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_v2r13_pair09_candidate_execution_evidence_review"
)


class V2R13Pair09CandidateExecutionEvidenceAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13Pair09CandidateExecutionEvidenceAcceptanceHold(message)


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
        .v2r13_pair09_candidate_invocation_review_contract()
    )
    _require(
        reviewed.get("pair09_candidate_invocation_source_binding_present") is True,
        "pair09 candidate invocation source binding missing",
    )
    _require(
        reviewed.get("pair09_candidate_invocation_reviewed") is True,
        "pair09 candidate invocation not reviewed",
    )
    _require(reviewed.get("precision_cli_reviewed") is True, "pair09 candidate CLI not reviewed")
    _require(reviewed.get("pair_slot") == 9, "pair09 candidate slot drift")
    _require(reviewed.get("arm") == "candidate", "pair09 candidate arm drift")
    _require(reviewed.get("held_out") is False, "pair09 candidate held-out drift")
    _require(reviewed.get("single_use_attempt") is True, "pair09 candidate one-shot drift")
    _require(reviewed.get("automatic_retry") is False, "pair09 candidate automatic retry enabled")
    _require(
        reviewed.get("pair09_candidate_execution_performed") is False,
        "source review unexpectedly records runtime execution",
    )
    _require(
        reviewed.get("next_gate")
        == "V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
        "pair09 candidate pre-execution frontier drift",
    )
    return deepcopy(reviewed)


def accept_pair09_candidate_execution_evidence(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    dependency = _validate_dependency()
    _require(isinstance(evidence, Mapping), "pair09 candidate evidence must be object")
    supplied = dict(evidence)
    _require(
        set(supplied) == set(EXPECTED_EVIDENCE),
        "pair09 candidate evidence field-set drift",
    )
    for field, expected in EXPECTED_EVIDENCE.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"pair09 candidate evidence drift: {field}",
        )
    _require(
        _digest(supplied) == EXPECTED_EVIDENCE_SHA256,
        "pair09 candidate evidence digest drift",
    )

    return {
        "schema": ACCEPTANCE_SCHEMA,
        "pair09_candidate_execution_evidence_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "launcher_sha256": LAUNCHER_SHA256,
        "execution_main_head": EXECUTION_MAIN_HEAD,
        "execution_main_tree": EXECUTION_MAIN_TREE,
        "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
        "attempt_consumed": True,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "result_file_sha256": RESULT_FILE_SHA256,
        "pair_slot": 9,
        "arm": "candidate",
        "held_out": False,
        "maximum_attempts": 1,
        "runtime_execution_performed": True,
        "fresh_runtime_readiness_admitted": True,
        "runtime_cleanup_completed": True,
        "run_id": RUN_ID,
        "seed": SEED,
        "outcome": OUTCOME,
        "rounds_completed": ROUNDS_COMPLETED,
        "final_tick": FINAL_TICK,
        "warm_start_sha256": WARM_START_SHA256,
        "trajectory_sha256": TRAJECTORY_SHA256,
        "summary_sha256": SUMMARY_SHA256,
        "candidate_file_sha256": CANDIDATE_FILE_SHA256,
        "candidate_genome_sha256": CANDIDATE_GENOME_SHA256,
        "wrapper_sha256": CANDIDATE_WRAPPER_SHA256,
        "pair03_baseline_preserved": True,
        "pair03_candidate_preserved": True,
        "pair09_baseline_preserved": True,
        "automatic_retry": False,
        "baseline_rerun": False,
        "candidate_execution_replay_permitted": False,
        "another_candidate_execution_authorized": False,
        "held_out_execution_authorized": False,
        "held_out_execution_performed": False,
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
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "evidence": deepcopy(supplied),
        "dependency_review": dependency,
    }


def v2r13_pair09_candidate_execution_evidence_acceptance_contract() -> dict[str, Any]:
    accepted = accept_pair09_candidate_execution_evidence(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "invocation_review_git_blob": INVOCATION_REVIEW_GIT_BLOB,
        "invocation_review_source_sha256": INVOCATION_REVIEW_SOURCE_SHA256,
        "pair09_candidate_execution_evidence_accepted": True,
        "launcher_sha256": LAUNCHER_SHA256,
        "execution_main_head": EXECUTION_MAIN_HEAD,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "attempt_consumed": True,
        "maximum_attempts": 1,
        "candidate_execution_replay_permitted": False,
        "another_candidate_execution_authorized": False,
        "held_out_execution_authorized": False,
        "automatic_retry": False,
        "candidate_result_review_required": True,
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_evidence": accepted,
    }


def authorize_follow_on_execution(*args: Any, **kwargs: Any) -> None:
    raise V2R13Pair09CandidateExecutionEvidenceAcceptanceHold(NEXT_GATE)
