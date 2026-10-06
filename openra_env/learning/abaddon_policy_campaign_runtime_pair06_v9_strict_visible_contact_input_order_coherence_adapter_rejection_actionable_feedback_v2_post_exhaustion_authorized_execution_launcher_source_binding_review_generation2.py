"""Exact-blob review of the post-exhaustion authorized actionable-feedback V2 launcher.

Pins the launcher and focused tests. The review confirms the exact accepted
authorization lineage, one-attempt zero-auto-retry cardinality, fresh CUDA:0
preclaim gating, exact canonical source identities, and delegation to the
already-reviewed V2 operator. No host execution is performed by review.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v2_post_exhaustion_authorized_execution_launcher_generation2
    as launcher,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v2-"
    "post-exhaustion-authorized-execution-launcher-review.v1"
)

ACCEPTED_BASE_HEAD = "a16441e2025f5152374ad044903472276b4ca3e6"

LAUNCHER_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_post_exhaustion_authorized_execution_"
    "launcher_generation2.py"
)
LAUNCHER_GIT_BLOB = "df786745690c619901211a0e8683163dbdbfd6ba"

LAUNCHER_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v2_post_exhaustion_authorized_execution_"
    "launcher_generation2.py"
)
LAUNCHER_TEST_GIT_BLOB = "68a3a01e2167ebf82dbd870d4a1677d2016c2e2b"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V2_POST_EXHAUSTION_"
    "AUTHORIZED_HOST_EXECUTION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "runtime_single_pair06_v9_input_order_adapter_rejection_"
    "actionable_feedback_v2_post_exhaustion_attempt"
)


class Pair06V9ActionableFeedbackV2PostExhaustionAuthorizedLauncherReviewHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV2PostExhaustionAuthorizedLauncherReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        launcher
        .pair06_v9_actionable_feedback_v2_post_exhaustion_authorized_execution_launcher_contract()
    )

    _require(
        out.get(
            "pair06_v9_actionable_feedback_v2_post_exhaustion_authorized_execution_launcher_implemented"
        )
        is True,
        "post-exhaustion authorized launcher missing",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("policy_id") == "pair06-v9-strict-visible-contact-envelope-v1"
        and out.get("intervention_id")
        == "pair06-v9-input-order-coherence-adapter-rejection-actionable-feedback-v2",
        "post-exhaustion launcher scope drift",
    )
    _require(
        out.get("acceptance_git_blob")
        == "241856d4c7e1207a7ffcebe98b5140f969dbd3d7"
        and out.get("acceptance_review_git_blob")
        == "a05196722a1076f824f9e78715ceaeefa56b8c90"
        and out.get("request_review_git_blob")
        == "c3ae2c1117ad87851769b3999ae35a475c68b3e8"
        and out.get("requirements_review_git_blob")
        == "def228081606c604e785ef057a3ac33fde026a5c"
        and out.get("operator_git_blob")
        == "84132f0ba96cff24dc88ea2ef7259a850162e41a"
        and out.get("operator_review_git_blob")
        == "c74c221202e8ec35c96a458e2d9849743b1c0b41",
        "post-exhaustion launcher source lineage drift",
    )

    for field in (
        "exact_canonical_blobs_required_before_execution",
        "current_main_required_before_execution",
        "tracked_source_clean_required_before_execution",
        "operator_sha256_derived_from_canonical_source",
        "explicit_launcher_confirmation_required",
        "fresh_preclaim_gpu_observation_required",
        "fresh_preclaim_gpu_observation_precedes_attempt_marker",
        "zero_foreign_cuda0_compute_processes_required",
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "actionable_feedback_v2_activation_authorization_accepted",
        "reviewed_operator_source_reuse_only",
    ):
        _require(
            out.get(field) is True,
            "post-exhaustion launcher invariant drift: " + field,
        )

    _require(
        out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0
        and out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "post-exhaustion launcher cardinality/GPU drift",
    )
    _require(
        out.get("prior_v2_attempt_marker_sha256")
        == "35b7582352e10f3677976eb7a11a7253933006c50154fde93c3f43fb1ca03425"
        and out.get("prior_v2_preservation_receipt_sha256")
        == "5dc48dc877a41271694e1e74a4d0e3731c3b7c6fa985bffa4e538ddf8b3d6a3e"
        and out.get("prior_execution_authorization_reusable") is False
        and out.get("prior_preservation_authorization_reusable") is False,
        "post-exhaustion launcher spent-lineage drift",
    )

    for field in (
        "authorization_reusable_after_attempt_claim",
        "contract_inspection_performs_host_io",
        "contract_inspection_creates_attempt_marker",
        "contract_inspection_loads_model",
        "contract_inspection_runs_inference",
        "contract_inspection_executes_game",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
    ):
        _require(
            out.get(field) is False,
            "post-exhaustion launcher boundary drift: " + field,
        )

    _require(
        out.get("source_frontier_closed") is True
        and out.get("next_gate") == NEXT_GATE,
        "post-exhaustion launcher frontier drift",
    )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (LAUNCHER_PATH, LAUNCHER_GIT_BLOB),
        (LAUNCHER_TEST_PATH, LAUNCHER_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_actionable_feedback_v2_post_exhaustion_authorized_execution_launcher_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "launcher_path": LAUNCHER_PATH,
        "launcher_git_blob": LAUNCHER_GIT_BLOB,
        "launcher_test_path": LAUNCHER_TEST_PATH,
        "launcher_test_git_blob": LAUNCHER_TEST_GIT_BLOB,
        "pair06_v9_actionable_feedback_v2_post_exhaustion_authorized_execution_launcher_reviewed": True,
        "pair_slot": validated["pair_slot"],
        "arm": validated["arm"],
        "policy_id": validated["policy_id"],
        "intervention_id": validated["intervention_id"],
        "acceptance_git_blob": validated["acceptance_git_blob"],
        "acceptance_review_git_blob": validated["acceptance_review_git_blob"],
        "request_review_git_blob": validated["request_review_git_blob"],
        "requirements_review_git_blob": validated["requirements_review_git_blob"],
        "operator_git_blob": validated["operator_git_blob"],
        "operator_review_git_blob": validated["operator_review_git_blob"],
        "prior_v2_attempt_marker_sha256": validated[
            "prior_v2_attempt_marker_sha256"
        ],
        "prior_v2_preservation_receipt_sha256": validated[
            "prior_v2_preservation_receipt_sha256"
        ],
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "execution_authorization_accepted": True,
        "policy_activation_authorization_accepted": True,
        "order_coherence_activation_authorization_accepted": True,
        "repair_activation_authorization_accepted": True,
        "actionable_feedback_v2_activation_authorization_accepted": True,
        "explicit_launcher_confirmation_required": True,
        "reviewed_operator_source_reuse_only": True,
        "prior_execution_authorization_reusable": False,
        "prior_preservation_authorization_reusable": False,
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
        "validated_launcher": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV2PostExhaustionAuthorizedLauncherReviewHold(
        NEXT_GATE
    )
