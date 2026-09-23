"""Source-only review of accepted pair-06 V8 Precision environment evidence."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_precision_environment_observation_acceptance_generation2
    as acceptance,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-precision-runtime-environment-observation-source-binding-review-contract.v1"
)

ACCEPTANCE_GIT_BLOB = "3d054bdc04497da10f718141b357eaa35192cbc7"
ACCEPTANCE_SOURCE_SHA256 = (
    "3e50e5a1735bd755b127705e1dabd7facbeed4baf0ce934d1b1b77652f6a79b7"
)
ACCEPTANCE_TEST_GIT_BLOB = "ca51273f9018b87801b7ae4b1bddc4944f03cb6e"
ACCEPTANCE_TEST_SHA256 = (
    "9c8232a32029bfdd6288c3f8add3987b21ebb509bb15f498a76ae71f359c1266"
)

NEXT_GATE = "PAIR06_V8_RUNTIME_ENVIRONMENT_PATH_BINDING_SOURCE_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_runtime_environment_path_binding"


class Pair06V8PrecisionEnvironmentObservationReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PrecisionEnvironmentObservationReviewHold(message)


@lru_cache(maxsize=1)
def _validate_acceptance_cached() -> dict[str, Any]:
    contract = (
        acceptance
        .pair06_v8_precision_environment_observation_acceptance_contract()
    )
    _require(
        contract.get("pair06_v8_precision_environment_observation_accepted") is True,
        "pair06 V8 Precision environment acceptance missing",
    )
    _require(
        contract.get("observer_sha256")
        == "371995496abafd6fda7f562aa4d2bbceb8c7b107d7345cfb5c2a1b5e069dafff",
        "pair06 V8 environment observer SHA drift",
    )
    _require(
        contract.get("accepted_python")
        == "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/venv/bin/python3.12",
        "pair06 V8 accepted interpreter drift",
    )
    _require(
        tuple(contract.get("accepted_python_major_minor", ())) == (3, 12),
        "pair06 V8 accepted Python version drift",
    )
    _require(
        contract.get("accepted_pip_freeze_sha256")
        == "7799387d3ef2780f8d25b93169297d73984d44b1d8264566bd238ee6fdfc3f77",
        "pair06 V8 accepted pip-freeze drift",
    )
    _require(
        contract.get("runtime_environment_admitted") is True,
        "pair06 V8 runtime environment not admitted",
    )
    _require(
        contract.get("runtime_environment_path_binding_eligible") is True,
        "pair06 V8 runtime environment not path-binding eligible",
    )
    _require(
        contract.get("runtime_environment_path_bound") is False,
        "pair06 V8 runtime environment path already bound",
    )
    _require(
        contract.get("runtime_load_authorized") is False
        and contract.get("runtime_load_performed") is False,
        "pair06 V8 runtime load unexpectedly authorized/performed",
    )
    _require(
        contract.get("model_inference_performed") is False
        and contract.get("game_execution_performed") is False,
        "pair06 V8 observation unexpectedly executed model/game",
    )
    _require(
        contract.get("next_gate")
        == "PAIR06_V8_PRECISION_RUNTIME_ENVIRONMENT_OBSERVATION_SOURCE_BINDING_REVIEW_REQUIRED",
        "pair06 V8 environment review frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_precision_environment_observation_review_contract() -> dict[str, Any]:
    reviewed = _validate_acceptance_cached()
    accepted = reviewed["accepted_observation"]
    return {
        "schema": CONTRACT_SCHEMA,
        "acceptance_git_blob": ACCEPTANCE_GIT_BLOB,
        "acceptance_source_sha256": ACCEPTANCE_SOURCE_SHA256,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "acceptance_test_sha256": ACCEPTANCE_TEST_SHA256,
        "separate_review_instrument": True,
        "observation_source_identity_pinned_by_git_blob": True,
        "observation_source_identity_pinned_by_sha256": True,
        "observation_test_identity_pinned_by_git_blob": True,
        "observation_test_identity_pinned_by_sha256": True,
        "pair06_v8_precision_environment_observation_reviewed": True,
        "pair_slot": 6,
        "held_out": False,
        "work_root": accepted["work_root"],
        "accepted_python": accepted["accepted_python"],
        "accepted_python_major_minor": accepted["accepted_python_major_minor"],
        "accepted_pip_freeze_sha256": accepted["accepted_pip_freeze_sha256"],
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
        "reviewed_acceptance": deepcopy(reviewed),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def bind_environment_path(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PrecisionEnvironmentObservationReviewHold(NEXT_GATE)


def load_runtime(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PrecisionEnvironmentObservationReviewHold(
        "PAIR06_V8_RUNTIME_LOAD_NOT_AUTHORIZED"
    )
