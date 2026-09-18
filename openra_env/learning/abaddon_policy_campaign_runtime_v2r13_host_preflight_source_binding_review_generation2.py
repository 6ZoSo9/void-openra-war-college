"""Source-only review of the Generation-2 V2R13 Precision host preflight.

Pins the exact host-preflight validator, real read-only Precision collector, and
tests. This review performs no host I/O and advances only to explicit Precision
preflight invocation. Runtime execution remains closed.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_host_preflight_generation2 as preflight,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-runtime-execution-host-preflight-source-binding-review-contract.v1"
)
REVIEW_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-runtime-execution-host-preflight-source-binding-review.v1"
)

PREFLIGHT_GIT_BLOB = "0ae27981a08b27083b235ae4807705c88da259a1"
PREFLIGHT_SOURCE_SHA256 = (
    "22620f890efdcfa81882a2e3869dcd88188932ee0417b6aeb4994c7b5829873a"
)
PRECISION_COLLECTOR_GIT_BLOB = "62d8a906ea41138b5443ba3bf96799b6e430b5be"
PRECISION_COLLECTOR_SOURCE_SHA256 = (
    "0501126c442fe58c8fce296e15146bd7c2eb6d36ac22d423681e1bae92edcc3c"
)
PREFLIGHT_TEST_GIT_BLOB = "c16e514dc0675c56dc6c98575d7b184935eacd3a"
PREFLIGHT_TEST_SHA256 = (
    "4c7ee1e4c5e0b84ddb0ec24295b64d73b3e8a598337b909bc8f43fb6855bb991"
)

EXECUTOR_REVIEW_GIT_BLOB = "9111f921db54bf58dc8046328f7d05cf319d6ebb"

NEXT_GATE = "V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_INVOCATION_REQUIRED"
NEXT_CHANGE_CLASS = "precision_v2r13_host_preflight_invocation"


class V2R13HostPreflightSourceBindingReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13HostPreflightSourceBindingReviewHold(message)


@lru_cache(maxsize=1)
def _validate_preflight_cached() -> dict[str, Any]:
    _require(
        preflight.EXECUTOR_REVIEW_GIT_BLOB == EXECUTOR_REVIEW_GIT_BLOB,
        "host-preflight executor-review blob drift",
    )
    contract = preflight.host_preflight_contract()

    _require(
        contract.get("executor_review_git_blob") == EXECUTOR_REVIEW_GIT_BLOB,
        "host-preflight contract executor-review blob drift",
    )
    _require(
        contract.get("host_preflight_validator_implemented") is True,
        "host-preflight validator missing",
    )
    _require(
        contract.get("real_host_collector_implemented_by_this_source") is False,
        "validator source unexpectedly performs real host collection",
    )
    _require(
        contract.get("read_only_snapshot_required") is True,
        "host preflight lost read-only requirement",
    )
    _require(
        contract.get("runtime_execution_authorized") is True,
        "accepted runtime authority missing at preflight frontier",
    )
    _require(
        contract.get("runtime_execution_performed") is False,
        "host-preflight contract unexpectedly executed runtime",
    )
    for field in (
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        _require(contract.get(field) is False, f"preflight boundary drift: {field}")

    _require(
        contract.get("expected_hostname") == preflight.EXPECTED_HOSTNAME,
        "expected Precision hostname drift",
    )
    _require(
        contract.get("expected_source_root") == preflight.EXPECTED_SOURCE_ROOT,
        "expected source root drift",
    )
    _require(
        contract.get("expected_engine_root") == preflight.EXPECTED_ENGINE_ROOT,
        "expected engine root drift",
    )
    _require(
        contract.get("expected_proto_python") == preflight.EXPECTED_PROTO_PYTHON,
        "expected proto Python drift",
    )
    _require(
        contract.get("frozen_source_commit") == preflight.FROZEN_SOURCE_COMMIT,
        "frozen source commit drift",
    )
    _require(
        contract.get("frozen_source_tree") == preflight.FROZEN_SOURCE_TREE,
        "frozen source tree drift",
    )
    _require(
        contract.get("frozen_engine_commit") == preflight.FROZEN_ENGINE_COMMIT,
        "frozen engine commit drift",
    )
    _require(
        contract.get("runtime_image") == preflight.RUNTIME_IMAGE,
        "runtime image name drift",
    )
    _require(
        contract.get("runtime_image_id") == preflight.RUNTIME_IMAGE_ID,
        "runtime image identity drift",
    )
    _require(
        tuple(contract.get("authorized_pair_slots", ()))
        == preflight.AUTHORIZED_PAIR_SLOTS,
        "authorized pair-slot drift",
    )
    _require(
        tuple(contract.get("authorized_arms", ())) == preflight.AUTHORIZED_ARMS,
        "authorized-arm drift",
    )

    tracked = contract.get("tracked_blobs")
    external = contract.get("external_files")
    _require(
        isinstance(tracked, dict) and tracked == preflight.TRACKED_BLOBS,
        "tracked blob manifest drift",
    )
    _require(
        isinstance(external, dict) and external == preflight.EXTERNAL_FILES,
        "external dependency manifest drift",
    )

    _require(
        contract.get("next_gate")
        == "V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_SOURCE_BINDING_REVIEW_REQUIRED",
        "host-preflight implementation gate drift",
    )
    _require(
        contract.get("next_change_class")
        == "source_only_v2r13_host_preflight_source_binding_review",
        "host-preflight implementation change-class drift",
    )

    return deepcopy(contract)


def _validate_preflight() -> dict[str, Any]:
    return deepcopy(_validate_preflight_cached())


def v2r13_host_preflight_source_binding_review() -> dict[str, Any]:
    validated = _validate_preflight()
    return {
        "schema": REVIEW_SCHEMA,
        "preflight_git_blob": PREFLIGHT_GIT_BLOB,
        "preflight_source_sha256": PREFLIGHT_SOURCE_SHA256,
        "precision_collector_git_blob": PRECISION_COLLECTOR_GIT_BLOB,
        "precision_collector_source_sha256": PRECISION_COLLECTOR_SOURCE_SHA256,
        "preflight_test_git_blob": PREFLIGHT_TEST_GIT_BLOB,
        "preflight_test_sha256": PREFLIGHT_TEST_SHA256,
        "preflight_source_identity_pinned_by_git_blob": True,
        "preflight_source_identity_pinned_by_sha256": True,
        "precision_collector_identity_pinned_by_git_blob": True,
        "precision_collector_identity_pinned_by_sha256": True,
        "preflight_test_identity_pinned_by_git_blob": True,
        "preflight_test_identity_pinned_by_sha256": True,
        "separate_review_instrument": True,
        "host_preflight_validator_implemented": True,
        "precision_read_only_collector_implemented": True,
        "host_preflight_source_binding_present": True,
        "host_preflight_reviewed": True,
        "host_preflight_invoked": False,
        "host_preflight_completed": False,
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
        "execution_source_blockers": (),
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "validated_preflight_contract": validated,
    }


def v2r13_host_preflight_source_binding_review_contract() -> dict[str, Any]:
    review = v2r13_host_preflight_source_binding_review()
    return {
        "schema": CONTRACT_SCHEMA,
        "preflight_git_blob": PREFLIGHT_GIT_BLOB,
        "preflight_source_sha256": PREFLIGHT_SOURCE_SHA256,
        "precision_collector_git_blob": PRECISION_COLLECTOR_GIT_BLOB,
        "precision_collector_source_sha256": PRECISION_COLLECTOR_SOURCE_SHA256,
        "preflight_test_git_blob": PREFLIGHT_TEST_GIT_BLOB,
        "preflight_test_sha256": PREFLIGHT_TEST_SHA256,
        "host_preflight_source_binding_present": True,
        "host_preflight_reviewed": True,
        "host_preflight_invoked": False,
        "host_preflight_completed": False,
        "runtime_execution_authorized": True,
        "runtime_execution_performed": False,
        "execution_source_blockers": (),
        "execution_blockers": (NEXT_GATE,),
        "source_frontier_closed": True,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "review": review,
    }


def invoke_host_preflight(*args: Any, **kwargs: Any) -> None:
    raise V2R13HostPreflightSourceBindingReviewHold(NEXT_GATE)


def execute_v2r13_runtime(*args: Any, **kwargs: Any) -> None:
    raise V2R13HostPreflightSourceBindingReviewHold(
        "V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_NOT_YET_INVOKED"
    )
