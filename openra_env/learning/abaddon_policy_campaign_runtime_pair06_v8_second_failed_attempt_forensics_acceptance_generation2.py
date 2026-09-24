"""Source-only acceptance of the second consumed pair-06 V8 baseline failure.

Binds the exact read-only Precision observer captured after the repaired
pair-06 baseline attempt failed during the first controller inference inside
Qwen3.5 GatedDeltaNet / Triton. No cleanup, retry, runtime action, model
action, game action, training, deployment, VOID-chain mutation, or wallet/funds
action occurs here.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-second-failed-attempt-forensics-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-second-failed-attempt-forensics-acceptance.v1"
)

OBSERVER_SHA256 = (
    "1bd19d363cf23265ea0142f9ae161c0da6ff80cd517f308f204975be2f1942be"
)
FAILED_MAIN_HEAD = "cb022ce0d32455c2f94f3ff2460bb88d3fb5c08c"
FAILED_MAIN_TREE = "ca34c9350d9f10876df8332299a40bb5306d2b05"
ATTEMPT_MARKER_SHA256 = (
    "446d8f924f50cf5a293336031c3963f3c5b106f0e8aa204726469df5df65f8d1"
)
PRIOR_ATTEMPT_MARKER_SHA256 = (
    "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
)
INVOCATION_SOURCE_SHA256 = (
    "58fa705393c4f0fe4b1c50c004d020b0682ada2a4f7d8cafe89d76c28e13fdb7"
)
MATERIALIZATION_SHA256 = (
    "7733a01d9d60b70232f91b7ab123513efbc1c01345adc6fbcea2f53dc4a32b74"
)

FROZEN_SOURCE_COMMIT = "973802ef0a614e5afa782ff20e231e18966ae3e5"
FROZEN_SOURCE_TREE = "d8a2af418af00e95ca0f203a2f0264851f2308c6"
ENGINE_COMMIT = "1607a7a6501d42a47638393ecef8b22831064932"
ENGINE_TREE = "bf562078c53edda3e6545f501b73ba1273c5df49"

RUN_DIRECTORY = (
    "warmstart-apollyon-vs-abaddon-20260923T235031Z-feinter-s208354846"
)
WARM_START_SHA256 = (
    "2266fb31a1b78b9dee950bcc1ce2eb77ebf961856e2df4b257a3c83309ee10e5"
)
WARM_START_BYTES = 229255
TRAJECTORY_SHA256 = (
    "955545e7b29377362da2e0f6cd58a113a802aba2ade3a0a32532066944a9d897"
)
TRAJECTORY_BYTES = 1027

PRIOR_ARCHIVE_PATH = (
    "/home/zoso/dev/void-war-college-execution/"
    "v8-generation2/generation2/pair-06/failed-attempts/"
    "baseline-20260923T221259Z-56c02591"
)
PRIOR_PRESERVATION_RECEIPT_FILE_SHA256 = (
    "d32cc7779fb1570ac2085031e296817059ce51d35de43ca3875becf9d032ccff"
)

EXPECTED_EVIDENCE = {
    "observer_sha256": OBSERVER_SHA256,
    "repo_main_head": FAILED_MAIN_HEAD,
    "repo_main_tree": FAILED_MAIN_TREE,
    "pair_slot": 6,
    "arm": "baseline",
    "held_out": False,
    "doctrine": "FEINTER",
    "seed": 208354846,
    "attempt_marker_present": True,
    "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
    "prior_attempt_marker_sha256": PRIOR_ATTEMPT_MARKER_SHA256,
    "distinct_from_prior_attempt": True,
    "result_present": False,
    "closeout_present": False,
    "revocation_present": False,
    "automatic_retry": False,
    "attempt_consumed": True,
    "invocation_source_sha256": INVOCATION_SOURCE_SHA256,
    "materialization_sha256": MATERIALIZATION_SHA256,
    "frozen_source_present": True,
    "frozen_source_clean": True,
    "frozen_source_detached": True,
    "frozen_source_commit": FROZEN_SOURCE_COMMIT,
    "frozen_source_tree": FROZEN_SOURCE_TREE,
    "engine_present": True,
    "engine_clean": True,
    "engine_detached": True,
    "engine_commit": ENGINE_COMMIT,
    "engine_tree": ENGINE_TREE,
    "run_directory": RUN_DIRECTORY,
    "warm_start_present": True,
    "warm_start_sha256": WARM_START_SHA256,
    "warm_start_bytes": WARM_START_BYTES,
    "trajectory_present": True,
    "trajectory_sha256": TRAJECTORY_SHA256,
    "trajectory_bytes": TRAJECTORY_BYTES,
    "summary_present": False,
    "warm_start_completed": True,
    "controller_handoff_reached": True,
    "first_controller_inference_failed": True,
    "failure_class": "qwen35_gated_delta_triton_cpu_pointer",
    "successful_game_result_present": False,
    "prior_archive_present": True,
    "prior_archive_path": PRIOR_ARCHIVE_PATH,
    "prior_preservation_receipt_file_sha256": (
        PRIOR_PRESERVATION_RECEIPT_FILE_SHA256
    ),
    "prior_attempt_reused": False,
    "runtime_retry_authorized": False,
}

EXPECTED_EVIDENCE_SHA256 = hashlib.sha256(
    json.dumps(
        EXPECTED_EVIDENCE,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
).hexdigest()

NEXT_GATE = "PAIR06_V8_SECOND_FAILED_ATTEMPT_PRESERVATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_second_failed_attempt_preservation"


class Pair06V8SecondFailedAttemptForensicsAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8SecondFailedAttemptForensicsAcceptanceHold(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


def accept_pair06_v8_second_failed_attempt_forensics(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    _require(
        isinstance(evidence, Mapping),
        "second failed-attempt evidence must be object",
    )
    supplied = dict(evidence)
    _require(
        set(supplied) == set(EXPECTED_EVIDENCE),
        "second failed-attempt evidence field-set drift",
    )
    for field, expected in EXPECTED_EVIDENCE.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"second failed-attempt evidence drift: {field}",
        )
    _require(
        _digest(supplied) == EXPECTED_EVIDENCE_SHA256,
        "second failed-attempt evidence digest drift",
    )
    return {
        "schema": ACCEPTANCE_SCHEMA,
        "pair06_v8_second_failed_attempt_forensics_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "observer_sha256": OBSERVER_SHA256,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "prior_attempt_marker_sha256": PRIOR_ATTEMPT_MARKER_SHA256,
        "attempt_distinct_from_prior": True,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "attempt_consumed": True,
        "automatic_retry": False,
        "warm_start_completed": True,
        "controller_handoff_reached": True,
        "first_controller_inference_failed": True,
        "failure_class": "qwen35_gated_delta_triton_cpu_pointer",
        "successful_game_result_present": False,
        "residual_frozen_worktrees_present": True,
        "warm_start_preserved": True,
        "trajectory_preserved": True,
        "summary_present": False,
        "prior_archive_preserved": True,
        "prior_attempt_reused": False,
        "runtime_retry_authorized": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "second_failed_attempt_preservation_required": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "evidence": deepcopy(supplied),
    }


def pair06_v8_second_failed_attempt_forensics_acceptance_contract() -> dict[str, Any]:
    accepted = accept_pair06_v8_second_failed_attempt_forensics(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v8_second_failed_attempt_forensics_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "prior_attempt_marker_sha256": PRIOR_ATTEMPT_MARKER_SHA256,
        "attempt_distinct_from_prior": True,
        "attempt_consumed": True,
        "successful_game_result_present": False,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "second_failed_attempt_preservation_required": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_evidence": accepted,
    }


def preserve_or_retry(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8SecondFailedAttemptForensicsAcceptanceHold(NEXT_GATE)
