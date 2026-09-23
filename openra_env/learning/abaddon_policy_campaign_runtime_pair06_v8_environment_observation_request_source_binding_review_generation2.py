"""Source-only review of the pair-06 V8 runtime-environment observation request."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_environment_observation_request_generation2
    as request,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-runtime-environment-observation-request-source-binding-review-contract.v1"
)

REQUEST_GIT_BLOB = "840c518d9d8f21ae09390fde42fcc376125076d6"
REQUEST_SOURCE_SHA256 = (
    "6c4ad1b99e7de071da4d29edfe9b7e5c378b72839e96701dde1e26d10217f2d8"
)
REQUEST_TEST_GIT_BLOB = "5e5a588d625af6fc1ce224878845b4948fb78eb5"
REQUEST_TEST_SHA256 = (
    "4223801ceca584499956efdbe0d991f8c450475739cfaced76bf9daffb8d2339"
)

NEXT_GATE = "PAIR06_V8_PRECISION_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED"
NEXT_CHANGE_CLASS = "trusted_operator_pair06_v8_precision_runtime_environment_observation"


class Pair06V8EnvironmentObservationRequestReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8EnvironmentObservationRequestReviewHold(message)


@lru_cache(maxsize=1)
def _validate_request_cached() -> dict[str, Any]:
    contract = request.pair06_v8_environment_observation_request_contract()
    _require(
        contract.get("pair06_v8_environment_observation_request_implemented") is True,
        "pair06 V8 environment observation request missing",
    )
    _require(
        contract.get("pair06_v8_environment_observation_request_reviewed") is False,
        "pair06 V8 environment observation request unexpectedly self-reviewed",
    )
    _require(contract.get("pair_slot") == 6, "pair06 environment request slot drift")
    _require(contract.get("held_out") is False, "pair06 environment request became held-out")
    _require(
        contract.get("work_root")
        == "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1",
        "pair06 V8 work-root drift",
    )
    _require(
        contract.get("interpreter_discovery_scope")
        == "bounded_known_v8_work_root",
        "pair06 V8 interpreter discovery scope drift",
    )
    _require(
        tuple(contract.get("expected_python_major_minor", ())) == (3, 12),
        "pair06 V8 expected Python drift",
    )
    _require(
        contract.get("expected_pip_freeze_sha256")
        == "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77",
        "pair06 V8 expected pip-freeze drift",
    )
    _require(
        contract.get("exactly_one_accepted_interpreter_required") is True,
        "pair06 V8 interpreter uniqueness requirement missing",
    )
    _require(
        contract.get("pip_freeze_observation_read_only") is True,
        "pair06 V8 pip-freeze observation not read-only",
    )
    _require(
        contract.get("runtime_environment_observed") is False
        and contract.get("runtime_environment_admitted") is False
        and contract.get("runtime_environment_path_bound") is False,
        "pair06 V8 runtime environment already observed/admitted/bound",
    )
    for field in (
        "runtime_load_authorized",
        "runtime_load_performed",
        "model_weights_loaded",
        "model_inference_performed",
        "game_execution_performed",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"pair06 environment request authority drift: {field}")
    _require(
        contract.get("next_gate")
        == "PAIR06_V8_PRECISION_RUNTIME_ENVIRONMENT_OBSERVATION_REQUIRED",
        "pair06 environment request frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_environment_observation_request_review_contract() -> dict[str, Any]:
    reviewed = _validate_request_cached()
    return {
        "schema": CONTRACT_SCHEMA,
        "request_git_blob": REQUEST_GIT_BLOB,
        "request_source_sha256": REQUEST_SOURCE_SHA256,
        "request_test_git_blob": REQUEST_TEST_GIT_BLOB,
        "request_test_sha256": REQUEST_TEST_SHA256,
        "separate_review_instrument": True,
        "request_source_identity_pinned_by_git_blob": True,
        "request_source_identity_pinned_by_sha256": True,
        "request_test_identity_pinned_by_git_blob": True,
        "request_test_identity_pinned_by_sha256": True,
        "pair06_v8_environment_observation_request_reviewed": True,
        "pair_slot": 6,
        "held_out": False,
        "work_root": reviewed["work_root"],
        "interpreter_discovery_scope": reviewed["interpreter_discovery_scope"],
        "expected_python_major_minor": (3, 12),
        "expected_pip_freeze_sha256": (
            "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77"
        ),
        "exactly_one_accepted_interpreter_required": True,
        "pip_freeze_observation_read_only": True,
        "runtime_environment_observed": False,
        "runtime_environment_admitted": False,
        "runtime_environment_path_bound": False,
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
        "reviewed_request": deepcopy(reviewed),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def observe_precision_environment(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8EnvironmentObservationRequestReviewHold(NEXT_GATE)


def load_runtime(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8EnvironmentObservationRequestReviewHold(
        "PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED"
    )
