"""Fixed, non-executable request to design a fresh scout-repair experiment.

This module records the next design gate after the pair-03 scouting defect was
reproduced and the bounded lifecycle repair was source-reviewed. It deliberately
does not select a campaign slot, seed, opponent, runtime, attempt directory, or
execution confirmation. It cannot authorize, launch, retry, promote, train, or
mutate anything.

The pair-03 candidate attempt is already consumed. Historical pair-03 evidence is
reference material only and is not a reusable execution permit or live control.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

REQUEST_SCHEMA = "void.abaddon.scout-repair-experiment-design-request.v1"
VALIDATION_SCHEMA = "void.abaddon.scout-repair-experiment-design-validation.v1"
NEXT_GATE = "SCOUT_REPAIR_EXPERIMENT_DESIGN_REVIEW_REQUIRED"
MAX_REQUEST_BYTES = 32768

PR181_HEAD = "dae97247b47dbbef48cec533ab403c20b5278bae"
PR181_TREE = "004ea893b529d297944000bff690da974a9dba71"
PAIR03_EVIDENCE_ARCHIVE_SHA256 = "f5f0a1229e278aef770806a625c32aa190ecb22ad97623aa62edd6c5a7333b00"
PAIR03_BASELINE_TRAJECTORY_SHA256 = "27741699e08e367e66177d8bcd6bc2244d2c21b804fe250101b8ef0b6c7165b9"
PAIR03_BASELINE_SUMMARY_SHA256 = "d37ab54fa8dbb2269a5ac61ca0880f7ae189188f0eea144031e484815bcdf7d6"
PAIR03_CANDIDATE_TRAJECTORY_SHA256 = "2880cb09bd9afd15d8dbb7436bcc7831191821f5a0be6badeece72e264645d65"
PAIR03_CANDIDATE_SUMMARY_SHA256 = "0819a0714a40dffb79208e5d35e01723143fe9a36eaf2a6feb988fcb4e76a5a0"

REPAIR_SOURCES = (
    ("openra_env/learning/abaddon_scout_missions_v1.py",
     "12ca91f68f595919061dd6d5f927fb46428c9a58",
     "09bb0a403cdb61fcbcae3e4690bf87a2c0aea4e65f4dcc1c755331492ff33571"),
    ("openra_env/learning/abaddon_scout_host_bridge_v1.py",
     "1fa8ea14c757e46658813dca035037f125e23880",
     "573d471c59a972a1f1fa6ec2537b484eef63c13a2102fac51a58de9b33df1d64"),
    ("openra_env/learning/abaddon_scout_runner_binding_v1.py",
     "9e4894b64f0820a53faf8226974d99687066679b",
     "5d8113072e904d59fde6145c73b2e9399772c46bcb1650bf9a687a46839cc9e6"),
    ("openra_env/learning/goal_effect_core_v1.py",
     "0bd626f6733a77a4861d71e5dea093d0a899c878",
     "eaa344512cd8895dff9c21011f6cee34cdeabdd85118e59a4e172334cf39661e"),
)

REQUIRED_DESIGN_DECISIONS = (
    "accepted_main_contains_exact_repair_sources",
    "fresh_non_held_out_experiment_namespace_selected",
    "fresh_seed_selected_without_reusing_pair03_consumed_slot",
    "opponent_runtime_identity_selected_and_source_bound",
    "live_control_requirement_decided",
    "maximum_attempt_count_fixed",
    "automatic_retry_count_fixed_at_zero",
    "durable_create_only_attempt_guard_designed",
    "fresh_host_preflight_and_readiness_required",
    "operation_time_revocation_check_required",
    "independent_post_run_cleanup_observation_required",
    "result_record_and_evidence_review_contract_designed",
)

FALSE_AUTHORITY_FIELDS = (
    "experiment_design_accepted",
    "experiment_slot_selected",
    "seed_selected",
    "opponent_selected",
    "live_control_authorized",
    "scout_repair_execution_authorized",
    "scout_repair_execution_performed",
    "attempt_guard_implemented",
    "attempt_consumed",
    "automatic_retry",
    "training_authorized",
    "training_performed",
    "weights_update_authorized",
    "weights_updated",
    "automatic_policy_promotion_authorized",
    "automatic_policy_promotion",
    "deployment_authorized",
    "deployment_performed",
    "void_chain_mutation_authorized",
    "void_chain_mutation_performed",
    "wallet_or_funds_action_authorized",
    "wallet_or_funds_action_performed",
)


class ScoutRepairExperimentRequestHold(ValueError):
    """The request changed, or an operational action was requested."""


def _record() -> dict[str, Any]:
    return {
        "schema": REQUEST_SCHEMA,
        "record_kind": "proposal_only_not_authorization",
        "repair_source_review": {
            "pr_number": 181,
            "reviewed_head": PR181_HEAD,
            "reviewed_tree": PR181_TREE,
            "must_be_accepted_on_main_before_experiment_acceptance": True,
            "repair_sources": {
                path: {"git_blob": blob, "sha256": sha256}
                for path, blob, sha256 in REPAIR_SOURCES
            },
        },
        "historical_evidence_reference": {
            "pair03_evidence_archive_sha256": PAIR03_EVIDENCE_ARCHIVE_SHA256,
            "baseline_trajectory_sha256": PAIR03_BASELINE_TRAJECTORY_SHA256,
            "baseline_summary_sha256": PAIR03_BASELINE_SUMMARY_SHA256,
            "candidate_trajectory_sha256": PAIR03_CANDIDATE_TRAJECTORY_SHA256,
            "candidate_summary_sha256": PAIR03_CANDIDATE_SUMMARY_SHA256,
            "shared_scouting_defect_reproduced": True,
            "candidate_252_superiority_established": False,
            "historical_evidence_is_reusable_execution_authority": False,
        },
        "proposed_experiment": {
            "purpose": "evaluate_bounded_scout_mission_lifecycle_without_candidate252_policy_mutations",
            "abaddon_doctrine": "FEINTER",
            "treatment": "controller_defaults_plus_abaddon_scout_missions_v1",
            "candidate252_policy_mutations_included": False,
            "campaign_pair_slot": None,
            "seed": None,
            "opponent_runtime_identity": None,
            "live_control_required": None,
            "maximum_attempts": None,
            "maximum_automatic_retries": 0,
            "reuse_pair03_attempt_marker": False,
            "reuse_pair03_execution_result": False,
            "reuse_v2r13_six_arm_authorization": False,
            "held_out_campaign_space_authorized": False,
        },
        "required_design_decisions": list(REQUIRED_DESIGN_DECISIONS),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "matching_request_digest_grants_authority": False,
        "runtime_gates_enforced_by_this_module": False,
        "next_gate": NEXT_GATE,
    }


def build_scout_repair_experiment_request() -> bytes:
    """Return one canonical request with one terminal LF."""
    return (json.dumps(
        _record(), sort_keys=True, separators=(",", ":"),
        ensure_ascii=True, allow_nan=False,
    ) + "\n").encode("utf-8")


def validate_scout_repair_experiment_request(payload: bytes) -> dict[str, Any]:
    """Validate exact proposal bytes; success conveys no execution authority."""
    if type(payload) is not bytes:
        raise ScoutRepairExperimentRequestHold("request must be exact bytes")
    if not 0 < len(payload) <= MAX_REQUEST_BYTES:
        raise ScoutRepairExperimentRequestHold("request byte limit")
    if payload != build_scout_repair_experiment_request():
        raise ScoutRepairExperimentRequestHold("request bytes differ from fixed proposal")
    return {
        "schema": VALIDATION_SCHEMA,
        "request_bytes_valid": True,
        "request_sha256": hashlib.sha256(payload).hexdigest(),
        "request_byte_length": len(payload),
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "next_gate": NEXT_GATE,
    }


def scout_repair_experiment_request_contract() -> dict[str, Any]:
    result = validate_scout_repair_experiment_request(build_scout_repair_experiment_request())
    result["request"] = _record()
    return result


def authorize_or_execute_scout_repair(*args: Any, **kwargs: Any) -> None:
    """Always HOLD: experiment design and authority are deliberately unresolved."""
    raise ScoutRepairExperimentRequestHold(NEXT_GATE)
