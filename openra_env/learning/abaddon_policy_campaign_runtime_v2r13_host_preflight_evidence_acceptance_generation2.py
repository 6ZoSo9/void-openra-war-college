"""Source-only acceptance of exact V2R13 Precision host-preflight evidence.

This module records one externally completed, read-only Precision host-preflight
snapshot after a separately authorized Ollama stop restored the reviewed dormant
boundary. It distinguishes the outer environment correction from the collector:
the outer wrapper stopped ollama.service, while the preflight collector itself
performed no service action and no runtime/model/game execution.

Importing or inspecting this source performs no host I/O, service action,
runtime start, model load/inference, game execution, training, deployment,
VOID-chain mutation, or wallet/funds action.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_host_preflight_generation2 as preflight,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_host_preflight_source_binding_review_generation2
    as preflight_review,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-runtime-execution-host-preflight-evidence-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-runtime-execution-host-preflight-evidence-acceptance.v1"
)

PREFLIGHT_GIT_BLOB = "0ae27981a08b27083b235ae4807705c88da259a1"
PRECISION_COLLECTOR_GIT_BLOB = "62d8a906ea41138b5443ba3bf96799b6e430b5be"
PREFLIGHT_REVIEW_GIT_BLOB = "c32bfe20abeef1bae1a130a8ebdb280cc604bf7a"

CANONICAL_MAIN_HEAD = "7a39699ab83f1706221afe638fe717783e466f87"
CANONICAL_MAIN_TREE = "10b14c64bef3e6b3f0d0f1fbf2204d0f16157632"
FROZEN_ENGINE_HEAD = "1607a7a6501d42a47638393ecef8b22831064932"
FROZEN_ENGINE_TREE = "bf562078c53edda3e6545f501b73ba1273c5df49"

GUARDED_PREFLIGHT_WRAPPER_SHA256 = (
    "12fb1d872be25eaf2583632d085db0ec025d92eda1bc053538e18534177442cd"
)
HOST_PREFLIGHT_SNAPSHOT_SHA256 = (
    "9a15a64e62e7f06cb0444f6e0dc830ddae9d9c262378f7f1f705d273aab7e364"
)

AUTHORIZED_PAIR_SLOTS = (3, 9, 15)
AUTHORIZED_ARMS = ("baseline", "candidate")
HELD_OUT_PAIR_SLOTS = (15,)

EXPECTED_EVIDENCE = {
    "wrapper_sha256": GUARDED_PREFLIGHT_WRAPPER_SHA256,
    "snapshot_sha256": HOST_PREFLIGHT_SNAPSHOT_SHA256,
    "canonical_main_head": CANONICAL_MAIN_HEAD,
    "canonical_main_tree": CANONICAL_MAIN_TREE,
    "source_branch": "main",
    "source_tracked_clean": True,
    "frozen_engine_head": FROZEN_ENGINE_HEAD,
    "frozen_engine_tree": FROZEN_ENGINE_TREE,
    "docker_context": "rootless",
    "runtime_image": "void-openra-joint-duel:ad1926569b12466c",
    "runtime_image_id": (
        "sha256:79f2f6800382489a2a648839fc0d58e546384938439378aeea06461363de25f5"
    ),
    "runtime_image_generation": "ad1926569b12466c",
    "ollama_active": "inactive",
    "ollama_enabled": "disabled",
    "activation_permit_present": False,
    "dormant_fuse_present": False,
    "dormant_condition_present": False,
    "authorized_pair_slots": AUTHORIZED_PAIR_SLOTS,
    "authorized_arms": AUTHORIZED_ARMS,
    "held_out_pair_slots": HELD_OUT_PAIR_SLOTS,
    "all_authorized_arm_paths_absent": True,
    "host_preflight_green": True,
    "runtime_execution_authorization_accepted": True,
    "runtime_execution_authorized": True,
    "runtime_execution_implemented": True,
    "runtime_execution_performed": False,
    "fresh_readiness_still_required_before_inference": True,
    "automatic_retry": False,
    "model_inference_performed": False,
    "game_execution_performed": False,
    "training_performed": False,
    "weights_updated": False,
    "automatic_policy_promotion": False,
    "deployment_performed": False,
    "void_chain_mutation_performed": False,
    "wallet_or_funds_action_performed": False,
    "outer_environment_correction_service_stop_performed": True,
    "outer_environment_correction_enable_disable_action": False,
    "outer_environment_correction_daemon_reload": False,
    "preflight_collector_service_action_performed": False,
}

NEXT_GATE = "V2R13_RUNTIME_EXECUTION_INVOCATION_REQUIRED"
NEXT_CHANGE_CLASS = "precision_v2r13_runtime_execution_invocation"


class V2R13HostPreflightEvidenceAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13HostPreflightEvidenceAcceptanceHold(message)


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


def _validate_dependencies() -> dict[str, Any]:
    review = preflight_review.v2r13_host_preflight_source_binding_review_contract()
    implementation = preflight.host_preflight_contract()

    _require(
        review.get("preflight_git_blob") == PREFLIGHT_GIT_BLOB,
        "preflight review validator blob drift",
    )
    _require(
        review.get("precision_collector_git_blob") == PRECISION_COLLECTOR_GIT_BLOB,
        "preflight review collector blob drift",
    )
    _require(
        review.get("host_preflight_source_binding_present") is True,
        "host preflight source binding missing",
    )
    _require(
        review.get("host_preflight_reviewed") is True,
        "host preflight source review missing",
    )
    _require(
        review.get("host_preflight_invoked") is False,
        "source review unexpectedly invokes host preflight",
    )
    _require(
        review.get("host_preflight_completed") is False,
        "source review unexpectedly completes host preflight",
    )
    _require(
        review.get("runtime_execution_authorized") is True,
        "runtime authority missing before evidence acceptance",
    )
    _require(
        review.get("runtime_execution_performed") is False,
        "runtime unexpectedly executed before evidence acceptance",
    )
    _require(
        tuple(review.get("execution_source_blockers", ())) == (),
        "execution source blocker reappeared",
    )
    _require(
        tuple(review.get("execution_blockers", ()))
        == ("V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_INVOCATION_REQUIRED",),
        "preflight invocation frontier drift",
    )

    _require(
        implementation.get("expected_hostname") == "zoso-Precision-Tower-7810",
        "host-preflight Precision hostname drift",
    )
    _require(
        implementation.get("runtime_image") == EXPECTED_EVIDENCE["runtime_image"],
        "host-preflight runtime image drift",
    )
    _require(
        implementation.get("runtime_image_id") == EXPECTED_EVIDENCE["runtime_image_id"],
        "host-preflight runtime image ID drift",
    )
    _require(
        tuple(implementation.get("authorized_pair_slots", ()))
        == AUTHORIZED_PAIR_SLOTS,
        "host-preflight authorized pair-slot drift",
    )
    _require(
        tuple(implementation.get("authorized_arms", ())) == AUTHORIZED_ARMS,
        "host-preflight authorized-arm drift",
    )
    _require(
        implementation.get("runtime_execution_performed") is False,
        "host-preflight contract unexpectedly executes runtime",
    )

    return {
        "preflight_review_contract": deepcopy(review),
        "preflight_contract": deepcopy(implementation),
    }


def accept_v2r13_host_preflight_evidence(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    """Accept exactly the externally completed Precision preflight summary."""
    _validate_dependencies()
    _require(isinstance(evidence, Mapping), "host preflight evidence must be object")
    supplied = dict(evidence)
    _require(
        set(supplied) == set(EXPECTED_EVIDENCE),
        "host preflight evidence field-set drift",
    )
    for field, expected in EXPECTED_EVIDENCE.items():
        actual = supplied.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"host preflight evidence drift: {field}",
        )
    _require(
        _digest(supplied) == EXPECTED_EVIDENCE_SHA256,
        "host preflight evidence digest drift",
    )

    return {
        "schema": ACCEPTANCE_SCHEMA,
        "host_preflight_evidence_accepted": True,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "snapshot_sha256": HOST_PREFLIGHT_SNAPSHOT_SHA256,
        "canonical_main_head": CANONICAL_MAIN_HEAD,
        "canonical_main_tree": CANONICAL_MAIN_TREE,
        "authorized_pair_slots": AUTHORIZED_PAIR_SLOTS,
        "authorized_arms": AUTHORIZED_ARMS,
        "held_out_pair_slots": HELD_OUT_PAIR_SLOTS,
        "host_preflight_completed": True,
        "host_preflight_green": True,
        "runtime_execution_authorization_accepted": True,
        "runtime_execution_implemented": True,
        "runtime_execution_authorized": True,
        "runtime_execution_performed": False,
        "fresh_readiness_still_required_before_inference": True,
        "automatic_retry": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "outer_environment_correction_service_stop_performed": True,
        "preflight_collector_service_action_performed": False,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "evidence": deepcopy(supplied),
    }


def v2r13_host_preflight_evidence_acceptance_contract() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    accepted = accept_v2r13_host_preflight_evidence(EXPECTED_EVIDENCE)
    return {
        "schema": CONTRACT_SCHEMA,
        "preflight_git_blob": PREFLIGHT_GIT_BLOB,
        "precision_collector_git_blob": PRECISION_COLLECTOR_GIT_BLOB,
        "preflight_review_git_blob": PREFLIGHT_REVIEW_GIT_BLOB,
        "guarded_preflight_wrapper_sha256": GUARDED_PREFLIGHT_WRAPPER_SHA256,
        "host_preflight_snapshot_sha256": HOST_PREFLIGHT_SNAPSHOT_SHA256,
        "evidence_sha256": EXPECTED_EVIDENCE_SHA256,
        "host_preflight_evidence_accepted": True,
        "host_preflight_completed": True,
        "host_preflight_green": True,
        "runtime_execution_authorization_accepted": True,
        "runtime_execution_implemented": True,
        "runtime_execution_authorized": True,
        "runtime_execution_performed": False,
        "fresh_readiness_still_required_before_inference": True,
        "automatic_retry": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "outer_environment_correction_service_stop_performed": True,
        "preflight_collector_service_action_performed": False,
        "execution_source_blockers": (),
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "accepted_evidence": accepted,
        "dependencies": dependencies,
    }


def invoke_v2r13_runtime(*args: Any, **kwargs: Any) -> None:
    raise V2R13HostPreflightEvidenceAcceptanceHold(NEXT_GATE)
