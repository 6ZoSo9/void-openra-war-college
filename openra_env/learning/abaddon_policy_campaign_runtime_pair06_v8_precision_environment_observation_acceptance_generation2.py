"""Source-only acceptance of exact Precision pair-06 V8 runtime-environment evidence.

The evidence was produced by a bounded read-only observer pinned to canonical
main. It discovered exactly one accepted Python environment under the known V8
work root, proved Python 3.12, matched the exact accepted pip-freeze SHA-256,
and passed the accepted V8 environment validator.

Importing or inspecting this source performs no host scan, subprocess action,
model load, inference, game execution, training, promotion, deployment,
VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_environment_observation_request_source_binding_review_generation2
    as request_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-precision-runtime-environment-observation-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-precision-runtime-environment-observation-acceptance.v1"
)

REQUEST_REVIEW_GIT_BLOB = "dab5691881a42f23e7b84bc59853b527b326aca7"
REQUEST_REVIEW_SOURCE_SHA256 = (
    "bcbc2d29580365662c23b5ae53d6e66222d4ab0c2510c5d15e389576dea59b15"
)

OBSERVER_SHA256 = (
    "371995496abafd6fda7f562aa4d2bbceb8c7b107d7345cfb5c2a1b5e069dafff"
)
CANONICAL_MAIN_HEAD = "0da2b7bd026dcda2a449393424ca7cb6e736bc8a"
WORK_ROOT = "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1"
ACCEPTED_PYTHON = WORK_ROOT + "/venv/bin/python3.12"
ACCEPTED_PYTHON_MAJOR_MINOR = (3, 12)
ACCEPTED_PIP_FREEZE_SHA256 = (
    "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77"
)

EXPECTED_EVIDENCE = {
    "observer_sha256": OBSERVER_SHA256,
    "canonical_main_head": CANONICAL_MAIN_HEAD,
    "pair_slot": 6,
    "arm_scope": ("baseline", "candidate"),
    "held_out": False,
    "work_root": WORK_ROOT,
    "interpreter_discovery_scope": "bounded_known_v8_work_root",
    "filesystem_scan_read_only": True,
    "pip_freeze_observation_read_only": True,
    "python_bin_directory_count": 1,
    "accepted_interpreter_candidate_count": 1,
    "accepted_python": ACCEPTED_PYTHON,
    "accepted_python_major_minor": ACCEPTED_PYTHON_MAJOR_MINOR,
    "accepted_pip_freeze_sha256": ACCEPTED_PIP_FREEZE_SHA256,
    "accepted_v8_runtime_environment_validator_green": True,
    "runtime_execution_performed": False,
    "model_execution_performed": False,
    "runtime_environment_observed": True,
    "runtime_environment_admitted": True,
    "runtime_environment_path_bound": False,
    "model_load": False,
    "model_weights_loaded": False,
    "model_inference": False,
    "game_execution": False,
    "training": False,
    "policy_promotion": False,
    "pair15_execution": False,
    "observation_result_ready_for_source_acceptance": True,
}

NEXT_GATE = (
    "PAIR06_V8_PRECISION_RUNTIME_ENVIRONMENT_OBSERVATION_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_precision_runtime_environment_observation_source_binding_review"
)


class Pair06V8PrecisionEnvironmentObservationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PrecisionEnvironmentObservationAcceptanceHold(message)


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


def _validate_request_review() -> dict[str, Any]:
    reviewed = request_review.pair06_v8_environment_observation_request_review_contract()
    _require(
        reviewed.get("pair06_v8_environment_observation_request_reviewed") is True,
        "pair06 V8 environment observation request not reviewed",
    )
    _require(reviewed.get("pair_slot") == 6, "pair06 environment request slot drift")
    _require(reviewed.get("held_out") is False, "pair06 environment request became held-out")
    _require(
        reviewed.get("work_root") == WORK_ROOT,
        "pair06 environment request work-root drift",
    )
    _require(
        reviewed.get("interpreter_discovery_scope") == "bounded_known_v8_work_root",
        "pair06 interpreter discovery scope drift",
    )
    _require(
        tuple(reviewed.get("expected_python_major_minor", ()))
        == ACCEPTED_PYTHON_MAJOR_MINOR,
        "pair06 expected Python drift",
    )
    _require(
        reviewed.get("expected_pip_freeze_sha256") == ACCEPTED_PIP_FREEZE_SHA256,
        "pair06 expected pip-freeze drift",
    )
    _require(
        reviewed.get("exactly_one_accepted_interpreter_required") is True,
        "pair06 interpreter uniqueness requirement missing",
    )
    _require(
        reviewed.get("pip_freeze_observation_read_only") is True,
        "pair06 pip-freeze observation no longer read-only",
    )
    _require(
        reviewed.get("runtime_environment_observed") is False
        and reviewed.get("runtime_environment_admitted") is False
        and reviewed.get("runtime_environment_path_bound") is False,
        "source request unexpectedly records environment observation",
    )
    _require(
        reviewed.get("runtime_load_authorized") is False
        and reviewed.get("runtime_load_performed") is False,
        "source request unexpectedly authorizes/performs runtime load",
    )
    _require(
        reviewed.get("next_gate")
        == "PAIR06_V8_PRECISION_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED",
        "pair06 environment observation frontier drift",
    )
    return deepcopy(reviewed)


def accept_pair06_v8_precision_environment_observation(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    reviewed = _validate_request_review()
    _require(isinstance(evidence, Mapping), "pair06 V8 environment evidence must be object")
    supplied = dict(evidence)
    _require(
        set(supplied) == set(EXPECTED_EVIDENCE),
        "pair06 V8 environment evidence field-set drift",
    )
    for field, expected in EXPECTED_EVIDENCE.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"pair06 V8 environment evidence drift: {field}",
        )
    _require(
        _digest(supplied) == EXPECTED_EVIDENCE_SHA256,
        "pair06 V8 environment evidence digest drift",
    )
    _require(
        ACCEPTED_PYTHON.startswith(WORK_ROOT + "/"),
        "accepted interpreter escaped bounded work root",
    )

    return {
        "schema": ACCEPTANCE_SCHEMA,
        "pair06_v8_precision_environment_observation_accepted": True,
        "accepted_evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "observer_sha256": OBSERVER_SHA256,
        "canonical_main_head": CANONICAL_MAIN_HEAD,
        "pair_slot": 6,
        "held_out": False,
        "work_root": WORK_ROOT,
        "accepted_python": ACCEPTED_PYTHON,
        "accepted_python_major_minor": ACCEPTED_PYTHON_MAJOR_MINOR,
        "accepted_pip_freeze_sha256": ACCEPTED_PIP_FREEZE_SHA256,
        "python_bin_directory_count": 1,
        "accepted_interpreter_candidate_count": 1,
        "runtime_environment_observed": True,
        "runtime_environment_admitted": True,
        "runtime_environment_path_binding_eligible": True,
        "runtime_environment_path_bound": False,
        "filesystem_scan_read_only": True,
        "pip_freeze_observation_read_only": True,
        "runtime_load_authorized": False,
        "runtime_load_performed": False,
        "model_weights_loaded": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "reviewed_request": reviewed,
        "accepted_evidence": deepcopy(supplied),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def pair06_v8_precision_environment_observation_acceptance_contract() -> dict[str, Any]:
    accepted = accept_pair06_v8_precision_environment_observation(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "request_review_source_sha256": REQUEST_REVIEW_SOURCE_SHA256,
        "pair06_v8_precision_environment_observation_accepted": True,
        "accepted_evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "observer_sha256": OBSERVER_SHA256,
        "accepted_python": ACCEPTED_PYTHON,
        "accepted_python_major_minor": ACCEPTED_PYTHON_MAJOR_MINOR,
        "accepted_pip_freeze_sha256": ACCEPTED_PIP_FREEZE_SHA256,
        "runtime_environment_admitted": True,
        "runtime_environment_path_binding_eligible": True,
        "runtime_environment_path_bound": False,
        "runtime_load_authorized": False,
        "runtime_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_observation": accepted,
    }


def bind_environment_path(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PrecisionEnvironmentObservationAcceptanceHold(NEXT_GATE)


def load_runtime(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PrecisionEnvironmentObservationAcceptanceHold(
        "PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED"
    )
