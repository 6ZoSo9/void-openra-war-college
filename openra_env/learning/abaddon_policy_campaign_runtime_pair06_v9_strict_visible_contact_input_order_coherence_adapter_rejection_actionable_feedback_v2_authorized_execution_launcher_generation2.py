"""Explicit one-shot launcher for authorized Pair-06 V9 actionable-feedback V2.

Import and contract inspection are inert. Operational invocation requires an
exact launcher confirmation token. Before delegation to the reviewed fresh-lineage
V2 operator the launcher verifies:

* the reviewed five-gate authorization acceptance is canonical;
* current checkout is canonical main with no tracked-source drift;
* exact acceptance, acceptance review, request review, requirements review,
  operator, and operator review Git blobs are present in current HEAD;
* the operator source SHA-256 is derived from those exact canonical bytes.

The launcher creates no independent retry path. It passes the reviewed
single-use authorizations and five exact confirmation tokens to the operator,
which owns fresh worktree materialization, CUDA:0 admission, create-only attempt
marker creation, execution, durable result, cleanup, and closeout.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_fresh_execution_authorization_acceptance_source_binding_review_generation2
    as acceptance_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_fresh_lineage_operator_generation2
    as operator,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "authorized-execution-launcher-contract.v1"
)

PAIR_SLOT = 6
ARM = "baseline"
POLICY_ID = "pair06-v9-strict-visible-contact-envelope-v1"
INTERVENTION_ID = (
    "pair06-v9-input-order-coherence-adapter-rejection-actionable-feedback-v2"
)

LAUNCH_CONFIRM_TOKEN = (
    "VOID_PAIR06_V9_INPUT_ORDER_ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_"
    "AUTHORIZED_EXECUTE_ONCE"
)

ACCEPTANCE_GIT_BLOB = "30815d85d0b3031b644bfc51abe331a403c9ea4a"
ACCEPTANCE_REVIEW_GIT_BLOB = "acc95f83858bf3056291248074954dd62b52d304"
REQUEST_REVIEW_GIT_BLOB = "5b550b6378e54d8b8b8efe581f34eb7df0a05ceb"
REQUIREMENTS_REVIEW_GIT_BLOB = "541fbacd4ec6d5acbce0cbd2c945f2b45801cfed"
OPERATOR_GIT_BLOB = "84132f0ba96cff24dc88ea2ef7259a850162e41a"
OPERATOR_REVIEW_GIT_BLOB = "c74c221202e8ec35c96a458e2d9849743b1c0b41"

ACCEPTANCE_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_fresh_execution_authorization_"
    "acceptance_generation2.py"
)
ACCEPTANCE_REVIEW_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_fresh_execution_authorization_"
    "acceptance_source_binding_review_generation2.py"
)
REQUEST_REVIEW_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_fresh_execution_authorization_request_"
    "source_binding_review_generation2.py"
)
REQUIREMENTS_REVIEW_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_fresh_execution_authorization_"
    "acceptance_requirements_source_binding_review_generation2.py"
)
OPERATOR_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_fresh_lineage_operator_generation2.py"
)
OPERATOR_REVIEW_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_fresh_lineage_operator_"
    "source_binding_review_generation2.py"
)

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_AUTHORIZED_HOST_EXECUTION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "runtime_single_pair06_v9_input_order_adapter_rejection_"
    "actionable_feedback_v2_attempt"
)


class Pair06V9ActionableFeedbackV2AuthorizedExecutionLauncherHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2AuthorizedExecutionLauncherHold(message)


def _authorization() -> dict[str, Any]:
    out = (
        acceptance_review
        .pair06_v9_actionable_feedback_v2_fresh_execution_authorization_acceptance_review_contract()
    )

    _require(
        out.get(
            "pair06_v9_actionable_feedback_v2_fresh_execution_authorization_acceptance_reviewed"
        )
        is True,
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_AUTHORIZATION_ACCEPTANCE_NOT_REVIEWED",
    )
    _require(
        out.get("pair_slot") == PAIR_SLOT
        and out.get("arm") == ARM
        and out.get("policy_id") == POLICY_ID
        and out.get("intervention_id") == INTERVENTION_ID,
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_AUTHORIZED_IDENTITY_DRIFT",
    )
    _require(
        out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0
        and out.get("automatic_retry") is False,
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_AUTHORIZED_ATTEMPT_BOUND_DRIFT",
    )
    _require(
        out.get("execution_authorization_accepted") is True
        and out.get("policy_activation_authorization_accepted") is True
        and out.get("order_coherence_activation_authorization_accepted") is True
        and out.get("repair_activation_authorization_accepted") is True
        and out.get("actionable_feedback_v2_activation_authorization_accepted")
        is True,
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_AUTHORIZATION_NOT_ACCEPTED",
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
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_AUTHORIZED_GPU_POLICY_DRIFT",
    )
    _require(
        out.get("fresh_actionable_feedback_v2_evidence_namespace_required")
        is True,
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_AUTHORIZED_NAMESPACE_DRIFT",
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
        is False
        and out.get(
            "actionable_feedback_v2_activation_authorization_reusable_after_attempt_claim"
        )
        is False,
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_AUTHORIZATION_REUSE_DRIFT",
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
            "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_EXTRA_AUTHORITY_DRIFT:" + field,
        )

    _require(
        out.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
            "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_"
            "AUTHORIZED_EXECUTION_LAUNCHER_REQUIRED"
        ),
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_AUTHORIZATION_NEXT_GATE_DRIFT",
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
        REQUIREMENTS_REVIEW_PATH: REQUIREMENTS_REVIEW_GIT_BLOB,
        OPERATOR_PATH: OPERATOR_GIT_BLOB,
        OPERATOR_REVIEW_PATH: OPERATOR_REVIEW_GIT_BLOB,
    }
    observed: dict[str, str] = {}
    for path, expected in expected_blobs.items():
        blob = _git("rev-parse", "HEAD:" + path)
        _require(
            blob == expected,
            "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_CANONICAL_BLOB_DRIFT:" + path,
        )
        observed[path] = blob

    operator_source = Path(operator.SOURCE_ROOT) / operator.SELF_PATH
    _require(
        operator_source.is_file(),
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_OPERATOR_SOURCE_MISSING",
    )
    operator_sha256 = hashlib.sha256(operator_source.read_bytes()).hexdigest()
    _require(
        len(operator_sha256) == 64,
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_OPERATOR_SHA256_INVALID",
    )

    return {
        "main_head": head,
        "operator_source_sha256": operator_sha256,
        **{"blob:" + path: blob for path, blob in observed.items()},
    }


def execute_authorized_pair06_v9_actionable_feedback_v2_once(
    *,
    launcher_confirm: str,
) -> dict[str, Any]:
    """Execute exactly the reviewed one-shot V2 lane when all runtime gates pass."""
    _require(
        type(launcher_confirm) is str
        and launcher_confirm == LAUNCH_CONFIRM_TOKEN,
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_LAUNCH_CONFIRMATION_REQUIRED",
    )

    authorization = _authorization()
    identity = _runtime_identity()

    result = (
        operator
        .execute_pair06_v9_input_order_adapter_rejection_actionable_feedback_v2_fresh_lineage_baseline_game(
            expected_main_head=identity["main_head"],
            expected_operator_source_sha256=identity["operator_source_sha256"],
            execution_authorization_accepted=True,
            policy_activation_authorization_accepted=True,
            order_coherence_activation_authorization_accepted=True,
            repair_activation_authorization_accepted=True,
            actionable_feedback_v2_activation_authorization_accepted=True,
            execution_confirm=operator.EXECUTION_CONFIRM_TOKEN,
            policy_confirm=operator.POLICY_CONFIRM_TOKEN,
            order_confirm=operator.ORDER_CONFIRM_TOKEN,
            repair_confirm=operator.REPAIR_CONFIRM_TOKEN,
            feedback_v2_confirm=operator.FEEDBACK_V2_CONFIRM_TOKEN,
        )
    )
    _require(
        isinstance(result, Mapping),
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_OPERATOR_RESULT_MISSING",
    )
    _require(
        result.get("pair_slot") == PAIR_SLOT
        and result.get("arm") == ARM
        and result.get("policy_id") == POLICY_ID,
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_OPERATOR_RESULT_SCOPE_DRIFT",
    )
    _require(
        result.get("v9_adapter_rejection_operator_integration_used") is True
        and result.get("v9_actionable_feedback_v2_operator_integration_used")
        is True
        and result.get("v9_adapter_rejection_activation_performed") is True
        and result.get("v9_actionable_feedback_v2_activation_performed") is True
        and result.get("pair06_baseline_execution_performed") is True,
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_OPERATOR_RESULT_INTERVENTION_DRIFT",
    )
    _require(
        result.get("automatic_retry") is False,
        "PAIR06_V9_ACTIONABLE_FEEDBACK_V2_OPERATOR_RESULT_RETRY_DRIFT",
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


def pair06_v9_actionable_feedback_v2_authorized_execution_launcher_contract() -> dict[str, Any]:
    authorization = _authorization()

    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v9_actionable_feedback_v2_authorized_execution_launcher_implemented": True,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "policy_id": POLICY_ID,
        "intervention_id": INTERVENTION_ID,
        "acceptance_git_blob": ACCEPTANCE_GIT_BLOB,
        "acceptance_review_git_blob": ACCEPTANCE_REVIEW_GIT_BLOB,
        "request_review_git_blob": REQUEST_REVIEW_GIT_BLOB,
        "requirements_review_git_blob": REQUIREMENTS_REVIEW_GIT_BLOB,
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
        "fresh_actionable_feedback_v2_evidence_namespace_required": True,
        "execution_authorization_accepted": True,
        "policy_activation_authorization_accepted": True,
        "order_coherence_activation_authorization_accepted": True,
        "repair_activation_authorization_accepted": True,
        "actionable_feedback_v2_activation_authorization_accepted": True,
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
            "fresh_create_only_actionable_feedback_v2_attempt_marker",
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
    result = execute_authorized_pair06_v9_actionable_feedback_v2_once(
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
