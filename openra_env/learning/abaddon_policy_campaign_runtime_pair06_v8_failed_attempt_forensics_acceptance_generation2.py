"""Source-only acceptance of the consumed pair-06 V8 baseline failed attempt.

Binds the exact read-only Precision observer captured after the single authorized
pair-06 baseline attempt failed on the first V8 inference. No cleanup, retry,
runtime action, model action, game action, training, deployment, VOID-chain
mutation, or wallet/funds action occurs here.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

OBSERVER_SHA256 = (
    "2b021514e2992dee3df99b41008900ee3098e218a7e29fb8c2594432fd14ca19"
)
FAILED_MAIN_HEAD = "0635e319b811975caec8c60fd6eabedc892dc981"
ATTEMPT_MARKER_SHA256 = (
    "56c02591672542cab905cd05b8061d1e44f4587a46bef925136db856232e5930"
)
INVOCATION_SOURCE_SHA256 = (
    "2eeaf9606e6a1cf173e0453104f3d440da8ab7e169a0bfe163b89c54e8164bd9"
)
MATERIALIZATION_SHA256 = (
    "7733a01d9d60b70232f91b7ab123513efbc1c01345adc6fbcea2f53dc4a32b74"
)
FROZEN_SOURCE_COMMIT = "973802ef0a614e5afa782ff20e231e18966ae3e5"
FROZEN_SOURCE_TREE = "d8a2af418af00e95ca0f203a2f0264851f2308c6"
ENGINE_COMMIT = "1607a7a6501d42a47638393ecef8b22831064932"
ENGINE_TREE = "bf562078c53edda3e6545f501b73ba1273c5df49"
RUN_DIRECTORY = (
    "warmstart-apollyon-vs-abaddon-20260923T221259Z-feinter-s208354846"
)
WARM_START_SHA256 = (
    "1a6bbd544aca9f111a0961948771c24f9e2e36eda7559cf78acac1df24411333"
)
WARM_START_BYTES = 229255
TRAJECTORY_SHA256 = (
    "89971bc284dab4424900eb7c27a73504e2acad067a59227dfdf37503475888ca"
)
TRAJECTORY_BYTES = 1027

EXPECTED_EVIDENCE = {
    "observer_sha256": OBSERVER_SHA256,
    "repo_main_head": FAILED_MAIN_HEAD,
    "pair_slot": 6,
    "arm": "baseline",
    "held_out": False,
    "doctrine": "FEINTER",
    "seed": 208354846,
    "attempt_marker_present": True,
    "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
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
    "first_v8_inference_failed": True,
    "successful_game_result_present": False,
    "runtime_retry_authorized": False,
}

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-failed-attempt-forensics-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-failed-attempt-forensics-acceptance.v1"
)
NEXT_GATE = "PAIR06_V8_FAILED_ATTEMPT_PRESERVATION_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_failed_attempt_preservation"


class Pair06V8FailedAttemptForensicsAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8FailedAttemptForensicsAcceptanceHold(message)


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


EXPECTED_EVIDENCE_SHA256 = _digest(EXPECTED_EVIDENCE)


def accept_pair06_v8_failed_attempt_forensics(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    _require(isinstance(evidence, Mapping), "pair06 failed-attempt evidence must be object")
    supplied = dict(evidence)
    _require(
        set(supplied) == set(EXPECTED_EVIDENCE),
        "pair06 failed-attempt evidence field-set drift",
    )
    for field, expected in EXPECTED_EVIDENCE.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"pair06 failed-attempt evidence drift: {field}",
        )
    _require(
        _digest(supplied) == EXPECTED_EVIDENCE_SHA256,
        "pair06 failed-attempt evidence digest drift",
    )
    return {
        "schema": ACCEPTANCE_SCHEMA,
        "pair06_v8_failed_attempt_forensics_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "observer_sha256": OBSERVER_SHA256,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "attempt_consumed": True,
        "automatic_retry": False,
        "warm_start_completed": True,
        "controller_handoff_reached": True,
        "first_v8_inference_failed": True,
        "successful_game_result_present": False,
        "residual_frozen_worktrees_present": True,
        "warm_start_preserved": True,
        "trajectory_preserved": True,
        "summary_present": False,
        "runtime_retry_authorized": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "failed_attempt_preservation_required": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "evidence": deepcopy(supplied),
    }


def pair06_v8_failed_attempt_forensics_acceptance_contract() -> dict[str, Any]:
    accepted = accept_pair06_v8_failed_attempt_forensics(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v8_failed_attempt_forensics_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "attempt_marker_sha256": ATTEMPT_MARKER_SHA256,
        "attempt_consumed": True,
        "successful_game_result_present": False,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "failed_attempt_preservation_required": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_evidence": accepted,
    }


def preserve_or_retry(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8FailedAttemptForensicsAcceptanceHold(NEXT_GATE)
