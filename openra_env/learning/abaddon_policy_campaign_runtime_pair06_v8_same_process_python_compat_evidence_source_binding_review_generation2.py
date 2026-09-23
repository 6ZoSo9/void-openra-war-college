"""Source-only review of pair-06 V8/proto Python compatibility evidence."""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_same_process_python_compat_evidence_acceptance_generation2
    as acceptance,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-same-process-python-compat-evidence-review-contract.v1"
)

ACCEPTANCE_SOURCE_GIT_BLOB = "69cbd7574d7b88e83b9169619a2873ab03d08e3a"
ACCEPTANCE_SOURCE_SHA256 = (
    "1de621378882ba4722629c8ac8b01de82000f899e88ef27d45582a0eca31bc14"
)
ACCEPTANCE_TEST_GIT_BLOB = "059b0da800b618c9a0467469e82a5460032906f8"
ACCEPTANCE_TEST_SHA256 = (
    "ac5f185049abfb38f4d530c022fe4453da2c2fc0feb71a53bc04f2cec25535ef"
)

NEXT_GATE = "PAIR06_V8_PARENT_CHILD_RUNTIME_SPLIT_DESIGN_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_parent_child_runtime_split_design"


class Pair06V8PythonCompatEvidenceReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8PythonCompatEvidenceReviewHold(message)


@lru_cache(maxsize=1)
def _validate_acceptance_cached() -> dict[str, Any]:
    contract = acceptance.pair06_v8_python_compat_evidence_acceptance_contract()
    _require(
        contract.get("pair06_v8_same_process_python_compat_evidence_accepted") is True,
        "pair06 Python compatibility evidence acceptance missing",
    )
    _require(contract.get("same_system_python_binary") is True, "system Python identity drift")
    _require(
        contract.get("separate_virtualenv_site_packages") is True,
        "separate venv package boundary missing",
    )
    _require(
        contract.get("same_process_legacy_game_path_compatible") is False,
        "same-process legacy game path unexpectedly compatible",
    )
    _require(
        contract.get("parent_child_runtime_split_required") is True,
        "parent-child split requirement missing",
    )
    _require(
        contract.get("package_install_into_v8_authorized") is False,
        "package installation unexpectedly authorized",
    )
    _require(
        contract.get("cross_venv_site_packages_injection_authorized") is False,
        "cross-venv injection unexpectedly authorized",
    )

    accepted = contract.get("accepted_evidence")
    _require(isinstance(accepted, dict), "accepted compatibility evidence missing")
    _require(accepted.get("pair_slot") == 6, "pair06 compatibility slot drift")
    _require(accepted.get("arm") == "baseline", "pair06 compatibility arm drift")
    _require(accepted.get("held_out") is False, "pair06 compatibility became held-out")
    _require(
        accepted.get("resolved_python") == "/usr/bin/python3.12",
        "resolved Python identity drift",
    )
    _require(
        accepted.get("v8_has_legacy_grpc_proto_dependencies") is False,
        "V8 environment unexpectedly contains legacy game dependencies",
    )
    _require(
        accepted.get("same_process_legacy_game_path_compatible") is False,
        "same-process compatibility evidence drift",
    )
    _require(
        accepted.get("parent_child_runtime_split_required") is True,
        "accepted parent-child split requirement missing",
    )
    for field in (
        "package_install_into_v8_authorized",
        "cross_venv_site_packages_injection_authorized",
        "model_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(accepted.get(field) is False, f"compatibility scope expanded: {field}")
    _require(accepted.get("automatic_retry") is False, "automatic retry enabled")

    _require(
        contract.get("next_gate") == NEXT_GATE,
        "pair06 compatibility review frontier drift",
    )
    return deepcopy(contract)


def pair06_v8_python_compat_evidence_review_contract() -> dict[str, Any]:
    validated = _validate_acceptance_cached()
    accepted = validated["accepted_evidence"]
    return {
        "schema": CONTRACT_SCHEMA,
        "acceptance_source_git_blob": ACCEPTANCE_SOURCE_GIT_BLOB,
        "acceptance_source_sha256": ACCEPTANCE_SOURCE_SHA256,
        "acceptance_test_git_blob": ACCEPTANCE_TEST_GIT_BLOB,
        "acceptance_test_sha256": ACCEPTANCE_TEST_SHA256,
        "pair06_v8_same_process_python_compat_evidence_source_binding_present": True,
        "pair06_v8_same_process_python_compat_evidence_reviewed": True,
        "pair_slot": 6,
        "arm": "baseline",
        "held_out": False,
        "observer_sha256": accepted["observer_sha256"],
        "execution_main_head": accepted["execution_main_head"],
        "v8_python": accepted["v8_python"],
        "proto_python": accepted["proto_python"],
        "resolved_python": accepted["resolved_python"],
        "same_system_python_binary": True,
        "separate_virtualenv_site_packages": True,
        "v8_has_legacy_grpc_proto_dependencies": False,
        "same_process_legacy_game_path_compatible": False,
        "parent_child_runtime_split_required": True,
        "package_install_into_v8_authorized": False,
        "cross_venv_site_packages_injection_authorized": False,
        "model_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "validated_acceptance": deepcopy(validated),
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_or_install(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8PythonCompatEvidenceReviewHold(NEXT_GATE)
