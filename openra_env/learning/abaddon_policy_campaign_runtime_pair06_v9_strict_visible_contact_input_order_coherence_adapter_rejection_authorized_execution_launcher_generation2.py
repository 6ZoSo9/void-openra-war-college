"""Explicit one-shot launcher for the authorized Pair-06 V9 adapter-rejection run.

This module is the final host-side wrapper before the reviewed fresh-lineage
adapter-rejection operator. Import and contract inspection are inert.

Operational invocation requires an exact launcher confirmation token. Before it
delegates to the reviewed operator it verifies:
* the reviewed four-gate authorization acceptance is canonical;
* current checkout is canonical main with no tracked-source drift;
* exact acceptance, acceptance review, request review, operator, and operator
  review Git blobs are present in current HEAD;
* the operator source SHA-256 is derived from those exact canonical bytes.

The launcher creates no independent retry path. It passes the already-reviewed
single-use authorizations and four exact confirmation tokens to the operator,
which owns fresh worktree materialization, CUDA:0 admission, create-only
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
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_fresh_execution_authorization_acceptance_source_binding_review_generation2
    as acceptance_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_fresh_lineage_operator_generation2
    as operator,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-authorized-execution-launcher-contract.v1"
)

PAIR_SLOT = 6
ARM = "baseline"
POLICY_ID = "pair06-v9-strict-visible-contact-envelope-v1"
INTERVENTION_ID = "pair06-v9-input-order-coherence-adapter-rejection-retry-v1"

LAUNCH_CONFIRM_TOKEN = (
    "VOID_PAIR06_V9_INPUT_ORDER_ADAPTER_REJECTION_AUTHORIZED_EXECUTE_ONCE"
)

ACCEPTANCE_GIT_BLOB = "75c6557a534123e5ac332682356a76dd7c7c58c6"
ACCEPTANCE_REVIEW_GIT_BLOB = "fb39902b28fbc33dc7d364a050d03bebb63843eb"
REQUEST_REVIEW_GIT_BLOB = "ef9e2b2c638cd358c383235ca1c07845830ca421"
OPERATOR_GIT_BLOB = "666834c004652f56c3fa8bf1fdaa67e1d87576d3"
OPERATOR_REVIEW_GIT_BLOB = "c6b22f43c92dcf3d6868361b0a1e82dd182cb053"

ACCEPTANCE_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "fresh_execution_authorization_acceptance_generation2.py"
)
ACCEPTANCE_REVIEW_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "fresh_execution_authorization_acceptance_source_binding_review_generation2.py"
)
REQUEST_REVIEW_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "fresh_execution_authorization_request_source_binding_review_generation2.py"
)
OPERATOR_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "fresh_lineage_operator_generation2.py"
)
OPERATOR_REVIEW_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "fresh_lineage_operator_source_binding_review_generation2.py"
)

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_AUTHORIZED_HOST_EXECUTION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "runtime_single_pair06_v9_input_order_adapter_rejection_attempt"
)


class Pair06V9AdapterRejectionAuthorizedExecutionLauncherHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9AdapterRejectionAuthorizedExecutionLauncherHold(message)


def _authorization() -> dict[str, Any]:
    out = (
        acceptance_review
        .pair06_v9_adapter_rejection_fresh_execution_authorization_acceptance_review_contract()
    )

    _require(
        out.get(
            "pair06_v9_adapter_rejection_fresh_execution_authorization_acceptance_reviewed"
        )
        is True,
        "PAIR06_V9_ADAPTER_REJECTION_AUTHORIZATION_ACCEPTANCE_NOT_REVIEWED",
    )
    _require(
        out.get("pair_slot") == PAIR_SLOT
        and out.get("arm") == ARM
        and out.get("policy_id") == POLICY_ID
        and out.get("intervention_id") == INTERVENTION_ID,
        "PAIR06_V9_ADAPTER_REJECTION_AUTHORIZED_IDENTITY_DRIFT",
    )
    _require(
        out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0
        and out.get("automatic_retry") is False,
        "PAIR06_V9_ADAPTER_REJECTION_AUTHORIZED_ATTEMPT_BOUND_DRIFT",
    )
    _require(
        out.get("execution_authorization_accepted") is True
        and out.get("policy_activation_authorization_accepted") is True
        and out.get("order_coherence_activation_authorization_accepted") is True
        and out.get("repair_activation_authorization_accepted") is True,
        "PAIR06_V9_ADAPTER_REJECTION_AUTHORIZATION_NOT_ACCEPTED",
    )
    _require(
        out.get("fresh_preclaim_gpu_observation_required") is True
        and out.get(
            "fresh_preclaim_gpu_observation_precedes_attempt_marker"
        )
        is True
        and out.get("zero_foreign_cuda0_compute_processes_required") is True
        and out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "PAIR06_V9_ADAPTER_REJECTION_AUTHORIZED_GPU_POLICY_DRIFT",
    )
    _require(
        out.get("fresh_adapter_rejection_evidence_namespace_required") is True,
        "PAIR06_V9_ADAPTER_REJECTION_AUTHORIZED_NAMESPACE_DRIFT",
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
        is False
        and out.get(
            "repair_activation_authorization_reusable_after_attempt_claim"
        )
        is False,
        "PAIR06_V9_ADAPTER_REJECTION_AUTHORIZATION_REUSE_DRIFT",
    )

    for field in (
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ):
        _require(
            out.get(field) is False,
            "PAIR06_V9_ADAPTER_REJECTION_EXTRA_AUTHORITY_DRIFT:" + field,
        )

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
            "ADAPTER_REJECTION_AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED"
        ),
        "PAIR06_V9_ADAPTER_REJECTION_AUTHORIZATION_NEXT_GATE_DRIFT",
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
            "PAIR06_V9_ADAPTER_REJECTION_CANONICAL_BLOB_DRIFT:" + path,
        )
        observed[path] = blob

    operator_source = Path(operator.SOURCE_ROOT) / operator.SELF_PATH
    _require(
        operator_source.is_file(),
        "PAIR06_V9_ADAPTER_REJECTION_OPERATOR_SOURCE_MISSING",
    )
    operator_sha256 = hashlib.sha256(operator_source.read_bytes()).hexdigest()
    _require(
        len(operator_sha256) == 64,
        "PAIR06_V9_ADAPTER_REJECTION_OPERATOR_SHA256_INVALID",
    )

    return {
        "main_head": head,
        "operator_source_sha256": operator_sha256,
        **{"blob:" + path: blob for path, blob in observed.items()},
    }


def execute_authorized_pair06_v9_adapter_rejection_once(
    *,
    launcher_confirm: str,
) -> dict[str, Any]:
    """Execute exactly the reviewed one-shot lane when all runtime gates pass."""
    _require(
        type(launcher_confirm) is str
        and launcher_confirm == LAUNCH_CONFIRM_TOKEN,
        "PAIR06_V9_ADAPTER_REJECTION_LAUNCH_CONFIRMATION_REQUIRED",
    )

    authorization = _authorization()
    identity = _runtime_identity()

    result = (
        operator
        .execute_pair06_v9_input_order_adapter_rejection_fresh_lineage_baseline_game(
            expected_main_head=identity["main_head"],
            expected_operator_source_sha256=identity["operator_source_sha256"],
            execution_authorization_accepted=True,
            policy_activation_authorization_accepted=True,
            order_coherence_activation_authorization_accepted=True,
            repair_activation_authorization_accepted=True,
            execution_confirm=operator.EXECUTION_CONFIRM_TOKEN,
            policy_confirm=operator.POLICY_CONFIRM_TOKEN,
            order_confirm=operator.ORDER_CONFIRM_TOKEN,
            repair_confirm=operator.REPAIR_CONFIRM_TOKEN,
        )
    )
    _require(
        isinstance(result, Mapping),
        "PAIR06_V9_ADAPTER_REJECTION_OPERATOR_RESULT_MISSING",
    )
    _require(
        result.get("pair_slot") == PAIR_SLOT
        and result.get("arm") == ARM
        and result.get("policy_id") == POLICY_ID,
        "PAIR06_V9_ADAPTER_REJECTION_OPERATOR_RESULT_SCOPE_DRIFT",
    )
    _require(
        result.get("v9_adapter_rejection_operator_integration_used") is True
        and result.get("v9_adapter_rejection_activation_performed") is True,
        "PAIR06_V9_ADAPTER_REJECTION_OPERATOR_RESULT_INTERVENTION_DRIFT",
    )
    _require(
        result.get("automatic_retry") is False,
        "PAIR06_V9_ADAPTER_REJECTION_OPERATOR_RESULT_RETRY_DRIFT",
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
        "authorization_reusable_after_attempt_claim": False,
    }


def pair06_v9_adapter_rejection_authorized_execution_launcher_contract() -> dict[str, Any]:
    authorization = _authorization()

    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v9_adapter_rejection_authorized_execution_launcher_implemented": True,
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
        "fresh_adapter_rejection_evidence_namespace_required": True,
        "execution_authorization_accepted": True,
        "policy_activation_authorization_accepted": True,
        "order_coherence_activation_authorization_accepted": True,
        "repair_activation_authorization_accepted": True,
        "authorization_reusable_after_attempt_claim": False,
        "contract_inspection_performs_host_io": False,
        "contract_inspection_creates_attempt_marker": False,
        "contract_inspection_loads_model": False,
        "contract_inspection_runs_inference": False,
        "contract_inspection_executes_game": False,
        "training_authorized": False,
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
            "fresh_create_only_adapter_rejection_attempt_marker",
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
    result = execute_authorized_pair06_v9_adapter_rejection_once(
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
