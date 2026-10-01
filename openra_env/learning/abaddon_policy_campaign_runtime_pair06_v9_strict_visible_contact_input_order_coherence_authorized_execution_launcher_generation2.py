"""Explicit one-shot launcher for the authorized Pair-06 V9 input-order run.

This module is the final host-side wrapper before the reviewed order-coherence
operator. Import and contract inspection are inert.

Operational invocation requires an exact launcher confirmation token. Before it
delegates to the reviewed operator it verifies:
* the reviewed authorization acceptance is canonical and authorizes exactly one
  Pair-06 baseline attempt after fresh CUDA:0 preclaim admission;
* strict-contact policy activation and input-order-coherence activation are both
  authorized for that one attempt;
* current checkout is canonical main with no tracked-source drift;
* the exact operator, operator review, request review, authorization acceptance,
  and authorization review Git blobs are present in current HEAD;
* the operator source SHA-256 is derived from those exact canonical bytes.

The launcher creates no independent retry path. It passes the already reviewed
single-use authorizations and three exact confirmation tokens to the operator,
which still owns fresh worktree materialization, CUDA:0 admission, create-only
attempt-marker creation, execution, durable result, cleanup, and closeout.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_execution_authorization_acceptance_source_binding_review_generation2
    as acceptance_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_operator_entrypoint_generation2
    as operator,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "authorized-execution-launcher-contract.v1"
)

PAIR_SLOT = 6
ARM = "baseline"
POLICY_ID = "pair06-v9-strict-visible-contact-envelope-v1"
INTERVENTION_ID = "pair06-v9-input-order-coherence-repair-v1"

LAUNCH_CONFIRM_TOKEN = (
    "VOID_PAIR06_V9_INPUT_ORDER_COHERENCE_AUTHORIZED_EXECUTE_ONCE"
)

ACCEPTANCE_GIT_BLOB = "f3d978c18f8793f6a91fdb0ec507d2a17ed5852f"
ACCEPTANCE_REVIEW_GIT_BLOB = "b0e65e4b752fae9aecde6304a17244301c4180d5"
REQUEST_REVIEW_GIT_BLOB = "19afaae0a30ddebb22e37ba7b5004d370fb97517"
OPERATOR_GIT_BLOB = "2a1e9d04b0a877ad4afb4f99f831b7824c5fb59a"
OPERATOR_REVIEW_GIT_BLOB = "2538f3c191e7a9826df0415583cac1021783a659"

ACCEPTANCE_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "execution_authorization_acceptance_generation2.py"
)
ACCEPTANCE_REVIEW_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "execution_authorization_acceptance_source_binding_review_generation2.py"
)
REQUEST_REVIEW_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "execution_authorization_request_source_binding_review_generation2.py"
)
OPERATOR_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "operator_entrypoint_generation2.py"
)
OPERATOR_REVIEW_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "operator_entrypoint_source_binding_review_generation2.py"
)

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "HOST_EXECUTION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "runtime_single_pair06_v9_strict_visible_contact_input_order_coherence_"
    "attempt"
)


class Pair06V9InputOrderCoherenceAuthorizedExecutionLauncherHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderCoherenceAuthorizedExecutionLauncherHold(
            message
        )


def _authorization() -> dict[str, Any]:
    out = (
        acceptance_review
        .pair06_v9_input_order_execution_authorization_acceptance_review_contract()
    )

    _require(
        out.get(
            "pair06_v9_input_order_execution_authorization_acceptance_reviewed"
        )
        is True,
        "PAIR06_V9_INPUT_ORDER_AUTHORIZATION_ACCEPTANCE_NOT_REVIEWED",
    )
    _require(
        out.get("policy_id") == POLICY_ID
        and out.get("intervention_id") == INTERVENTION_ID,
        "PAIR06_V9_INPUT_ORDER_AUTHORIZED_IDENTITY_DRIFT",
    )
    _require(
        out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0,
        "PAIR06_V9_INPUT_ORDER_AUTHORIZED_ATTEMPT_BOUND_DRIFT",
    )
    _require(
        out.get("receipt_bound_preclaim_gpu_execution_authorized") is True
        and out.get("v9_policy_activation_authorized") is True
        and out.get("v9_order_coherence_activation_authorized") is True,
        "PAIR06_V9_INPUT_ORDER_AUTHORIZATION_NOT_ACCEPTED",
    )
    _require(
        out.get("fresh_preclaim_gpu_observation_required") is True
        and out.get(
            "fresh_preclaim_gpu_observation_precedes_attempt_marker"
        )
        is True
        and out.get("zero_foreign_cuda0_compute_processes_required") is True,
        "PAIR06_V9_INPUT_ORDER_AUTHORIZED_GPU_POLICY_DRIFT",
    )
    _require(
        out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "PAIR06_V9_INPUT_ORDER_AUTHORIZED_GPU_THRESHOLD_DRIFT",
    )
    _require(
        out.get("fresh_order_evidence_namespace_required") is True,
        "PAIR06_V9_INPUT_ORDER_AUTHORIZED_EVIDENCE_NAMESPACE_DRIFT",
    )
    _require(
        out.get("execution_authorization_reusable_after_attempt_claim") is False
        and out.get(
            "policy_activation_authorization_reusable_after_attempt_claim"
        )
        is False
        and out.get(
            "order_coherence_activation_authorization_reusable_after_attempt_claim"
        )
        is False,
        "PAIR06_V9_INPUT_ORDER_AUTHORIZATION_REUSE_DRIFT",
    )

    for field in (
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "pair03_replay_authorized",
        "pair09_replay_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ):
        _require(
            out.get(field) is False,
            "PAIR06_V9_INPUT_ORDER_EXTRA_AUTHORITY_DRIFT:" + field,
        )

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
            "AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED"
        ),
        "PAIR06_V9_INPUT_ORDER_AUTHORIZATION_NEXT_GATE_DRIFT",
    )
    return deepcopy(out)


def _git(*args: str) -> str:
    return operator.base_invocation._git(*args)


def _runtime_identity() -> dict[str, str]:
    head = _git("rev-parse", "HEAD")
    operator.base_invocation._current_main(head)

    expected_blobs = {
        ACCEPTANCE_PATH: ACCEPTANCE_GIT_BLOB,
        ACCEPTANCE_REVIEW_PATH: ACCEPTANCE_REVIEW_GIT_BLOB,
        REQUEST_REVIEW_PATH: REQUEST_REVIEW_GIT_BLOB,
        OPERATOR_PATH: OPERATOR_GIT_BLOB,
        OPERATOR_REVIEW_PATH: OPERATOR_REVIEW_GIT_BLOB,
    }
    observed: dict[str, str] = {}
    for path, expected in expected_blobs.items():
        blob = _git("rev-parse", "HEAD:" + path)
        _require(
            blob == expected,
            "PAIR06_V9_INPUT_ORDER_CANONICAL_BLOB_DRIFT:" + path,
        )
        observed[path] = blob

    operator_source = Path(operator.SOURCE_ROOT) / operator.SELF_PATH
    _require(
        operator_source.is_file(),
        "PAIR06_V9_INPUT_ORDER_OPERATOR_SOURCE_MISSING",
    )
    operator_sha256 = hashlib.sha256(operator_source.read_bytes()).hexdigest()
    _require(
        len(operator_sha256) == 64,
        "PAIR06_V9_INPUT_ORDER_OPERATOR_SHA256_INVALID",
    )

    return {
        "main_head": head,
        "operator_source_sha256": operator_sha256,
        **{"blob:" + path: blob for path, blob in observed.items()},
    }


def execute_authorized_pair06_v9_input_order_once(
    *,
    launcher_confirm: str,
) -> dict[str, Any]:
    """Execute exactly the reviewed one-shot lane when all runtime gates pass."""
    _require(
        type(launcher_confirm) is str
        and launcher_confirm == LAUNCH_CONFIRM_TOKEN,
        "PAIR06_V9_INPUT_ORDER_LAUNCH_CONFIRMATION_REQUIRED",
    )

    authorization = _authorization()
    identity = _runtime_identity()

    result = (
        operator
        .execute_pair06_v9_input_order_coherence_baseline_game(
            expected_main_head=identity["main_head"],
            expected_operator_source_sha256=identity["operator_source_sha256"],
            execution_authorization_accepted=True,
            policy_activation_authorization_accepted=True,
            order_coherence_activation_authorization_accepted=True,
            execution_confirm=operator.EXECUTION_CONFIRM_TOKEN,
            policy_confirm=operator.POLICY_CONFIRM_TOKEN,
            order_confirm=operator.ORDER_CONFIRM_TOKEN,
        )
    )
    _require(
        isinstance(result, Mapping),
        "PAIR06_V9_INPUT_ORDER_OPERATOR_RESULT_MISSING",
    )
    _require(
        result.get("pair_slot") == PAIR_SLOT
        and result.get("arm") == ARM
        and result.get("policy_id") == POLICY_ID,
        "PAIR06_V9_INPUT_ORDER_OPERATOR_RESULT_SCOPE_DRIFT",
    )
    _require(
        result.get("v9_input_order_coherence_parent_wiring_used") is True
        and result.get("v9_input_order_coherence_activation_performed")
        is True,
        "PAIR06_V9_INPUT_ORDER_OPERATOR_RESULT_INTERVENTION_DRIFT",
    )
    _require(
        result.get("automatic_retry") is False,
        "PAIR06_V9_INPUT_ORDER_OPERATOR_RESULT_RETRY_DRIFT",
    )

    return {
        **deepcopy(dict(result)),
        "launcher_contract_schema": CONTRACT_SCHEMA,
        "launcher_main_head": identity["main_head"],
        "authorization_text_sha256": (
            authorization["authorization_text_sha256"]
        ),
        "authorization_text_bytes": authorization["authorization_text_bytes"],
        "single_authorized_attempt_consumed": True,
    }


def pair06_v9_input_order_authorized_execution_launcher_contract() -> dict[str, Any]:
    authorization = _authorization()

    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v9_input_order_authorized_execution_launcher_implemented": True,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "policy_id": POLICY_ID,
        "intervention_id": INTERVENTION_ID,
        "acceptance_git_blob": ACCEPTANCE_GIT_BLOB,
        "acceptance_review_git_blob": ACCEPTANCE_REVIEW_GIT_BLOB,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "operator_git_blob": OPERATOR_GIT_BLOB,
        "operator_review_git_blob": OPERATOR_REVIEW_GIT_BLOB,
        "exact_canonical_blobs_required_before_execution": True,
        "current_main_required_before_execution": True,
        "tracked_source_clean_required_before_execution": True,
        "operator_sha256_derived_from_canonical_source": True,
        "explicit_launcher_confirmation_required": True,
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "fresh_order_evidence_namespace_required": True,
        "execution_authorization_accepted": True,
        "policy_activation_authorization_accepted": True,
        "order_coherence_activation_authorization_accepted": True,
        "authorization_reusable_after_attempt_claim": False,
        "contract_inspection_performs_host_io": False,
        "contract_inspection_creates_attempt_marker": False,
        "contract_inspection_loads_model": False,
        "contract_inspection_runs_inference": False,
        "contract_inspection_executes_game": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "pair03_replay_authorized": False,
        "pair09_replay_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "authorization": authorization,
        "source_frontier_closed": True,
        "execution_blockers": (
            "explicit_launcher_confirmation",
            "exact_current_main_and_canonical_blobs",
            "fresh_preclaim_gpu_admission",
            "fresh_create_only_order_coherence_attempt_marker",
        ),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(add_help=False)
    value.add_argument("--confirm", required=True)
    return value


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    result = execute_authorized_pair06_v9_input_order_once(
        launcher_confirm=args.confirm,
    )
    print(
        json.dumps(
            result,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
