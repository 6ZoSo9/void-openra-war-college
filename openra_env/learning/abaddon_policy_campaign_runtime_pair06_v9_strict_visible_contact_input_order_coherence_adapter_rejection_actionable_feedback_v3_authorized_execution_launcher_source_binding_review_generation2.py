"""Exact-blob review of the authorized actionable-feedback V3 launcher.

Pins the launcher and focused tests. The review confirms exact canonical
acceptance/operator identities, explicit launcher confirmation, one-attempt
zero-auto-retry cardinality, fresh GPU preclaim admission, and delegation to
the reviewed fresh-lineage V2 operator with all five accepted authorization
gates.

No host execution is performed by review.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_actionable_feedback_v3_authorized_execution_launcher_generation2
    as launcher,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-actionable-feedback-v3-"
    "authorized-execution-launcher-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "0c6f93b6512e6e37b34b288cdcef0c75c5345624"

LAUNCHER_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v3_authorized_execution_launcher_generation2.py"
)
LAUNCHER_GIT_BLOB = "fe43f9a6cbe39a959581dd295fddb7092c28cf8a"

LAUNCHER_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "actionable_feedback_v3_authorized_execution_launcher_generation2.py"
)
LAUNCHER_TEST_GIT_BLOB = "70d1e0a5f7188160cc35ed4514124379af4944c9"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_ACTIONABLE_FEEDBACK_V3_AUTHORIZED_HOST_EXECUTION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "runtime_single_pair06_v9_input_order_adapter_rejection_"
    "actionable_feedback_v3_attempt"
)


class Pair06V9ActionableFeedbackV3AuthorizedExecutionLauncherReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9ActionableFeedbackV3AuthorizedExecutionLauncherReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        launcher
        .pair06_v9_actionable_feedback_v3_authorized_execution_launcher_contract()
    )

    _require(
        out.get(
            "pair06_v9_actionable_feedback_v3_authorized_execution_launcher_implemented"
        )
        is True,
        "authorized actionable-feedback V3 launcher missing",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1"
        and out.get("intervention_id")
        == "pair06-v9-input-order-coherence-adapter-rejection-actionable-feedback-v3",
        "authorized actionable-feedback V3 launcher scope drift",
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
        "fresh_actionable_feedback_v3_evidence_namespace_required",
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
        "repair_activation_authorization_accepted",
        "actionable_feedback_v3_activation_authorization_accepted",
    ):
        _require(
            out.get(field) is True,
            "authorized actionable-feedback V3 launcher invariant drift: " + field,
        )

    authorization = out.get("authorization")
    _require(
        isinstance(authorization, dict)
        and authorization.get("authorization_text_sha256")
        == launcher.EXACT_AUTHORIZATION_TEXT_SHA256
        and authorization.get("authorization_text_bytes")
        == launcher.EXACT_AUTHORIZATION_TEXT_BYTES
        and authorization.get("authorized_request_sha256")
        == launcher.EXACT_REQUEST_SHA256
        and authorization.get("authorized_request_bytes")
        == launcher.EXACT_REQUEST_BYTES
        and authorization.get("authorized_main_head")
        == launcher.AUTHORIZED_MAIN_AT_AUTHORIZATION_HEAD
        and authorization.get("authorized_main_tree")
        == launcher.AUTHORIZED_MAIN_AT_AUTHORIZATION_TREE
        and authorization.get("prior_attempt_marker_sha256")
        == launcher.CONSUMED_V2_ATTEMPT_MARKER_SHA256
        and authorization.get("preservation_receipt_sha256")
        == launcher.V2_PRESERVATION_RECEIPT_SHA256,
        "authorized V3 launcher exact-identity or consumed-lineage drift",
    )

    _require(
        out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0
        and out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "authorized actionable-feedback V3 launcher cardinality/GPU drift",
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
            "authorized actionable-feedback V3 launcher boundary drift: " + field,
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


def pair06_v9_actionable_feedback_v3_authorized_execution_launcher_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "launcher_path": LAUNCHER_PATH,
        "launcher_git_blob": LAUNCHER_GIT_BLOB,
        "launcher_test_path": LAUNCHER_TEST_PATH,
        "launcher_test_git_blob": LAUNCHER_TEST_GIT_BLOB,
        "pair06_v9_actionable_feedback_v3_authorized_execution_launcher_reviewed": True,
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
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "fresh_actionable_feedback_v3_evidence_namespace_required": True,
        "execution_authorization_accepted": True,
        "policy_activation_authorization_accepted": True,
        "order_coherence_activation_authorization_accepted": True,
        "repair_activation_authorization_accepted": True,
        "actionable_feedback_v3_activation_authorization_accepted": True,
        "explicit_launcher_confirmation_required": True,
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
        "authorization_text_sha256": validated["authorization"][
            "authorization_text_sha256"
        ],
        "authorization_text_bytes": validated["authorization"][
            "authorization_text_bytes"
        ],
        "authorized_request_sha256": validated["authorization"][
            "authorized_request_sha256"
        ],
        "authorized_main_at_authorization_head": validated["authorization"][
            "authorized_main_head"
        ],
        "consumed_v2_attempt_marker_sha256": validated["authorization"][
            "prior_attempt_marker_sha256"
        ],
        "v2_preservation_receipt_sha256": validated["authorization"][
            "preservation_receipt_sha256"
        ],
        "validated_launcher": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9ActionableFeedbackV3AuthorizedExecutionLauncherReviewHold(
        NEXT_GATE
    )
