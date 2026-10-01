"""Exact-blob review of the authorized Pair-06 V9 input-order launcher.

Pins the final host-side launcher and focused tests. The review confirms that
the launcher is inert by inspection, verifies exact canonical authorization and
operator blobs before runtime delegation, derives the operator SHA-256 from
canonical bytes, and preserves the reviewed single-attempt/fresh-GPU boundary.

This review performs no host I/O, GPU observation, attempt claim, model load,
inference, game execution, replay, training, promotion, deployment, chain,
wallet/funds, or scheduler action.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_authorized_execution_launcher_generation2
    as launcher,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-"
    "authorized-execution-launcher-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "fb99e3ca9171a0d454b9044e2d1fa41f5ee38565"

LAUNCHER_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "authorized_execution_launcher_generation2.py"
)
LAUNCHER_GIT_BLOB = "8035b99cc3698891555802c59ba401c29c7653b0"

LAUNCHER_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "authorized_execution_launcher_generation2.py"
)
LAUNCHER_TEST_GIT_BLOB = "9e85e85d6b9af5d2b371ce325203d5aae4e40145"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "HOST_EXECUTION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "runtime_single_pair06_v9_strict_visible_contact_input_order_coherence_"
    "attempt"
)


class Pair06V9InputOrderCoherenceAuthorizedExecutionLauncherReviewHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderCoherenceAuthorizedExecutionLauncherReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = launcher.pair06_v9_input_order_authorized_execution_launcher_contract()

    _require(
        out.get(
            "pair06_v9_input_order_authorized_execution_launcher_implemented"
        )
        is True,
        "V9 input-order authorized launcher missing",
    )
    _require(
        out.get("pair_slot") == 6
        and out.get("arm") == "baseline"
        and out.get("policy_id")
        == "pair06-v9-strict-visible-contact-envelope-v1"
        and out.get("intervention_id")
        == "pair06-v9-input-order-coherence-repair-v1",
        "V9 input-order launcher scope drift",
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
        "fresh_order_evidence_namespace_required",
        "execution_authorization_accepted",
        "policy_activation_authorization_accepted",
        "order_coherence_activation_authorization_accepted",
    ):
        _require(
            out.get(field) is True,
            "V9 input-order launcher invariant drift: " + field,
        )
    _require(
        out.get("maximum_attempts") == 1
        and out.get("maximum_automatic_retries") == 0,
        "V9 input-order launcher attempt cardinality drift",
    )
    _require(
        out.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "V9 input-order launcher GPU threshold drift",
    )
    _require(
        out.get("authorization_reusable_after_attempt_claim") is False,
        "V9 input-order launcher authorization reuse drift",
    )
    for field in (
        "contract_inspection_performs_host_io",
        "contract_inspection_creates_attempt_marker",
        "contract_inspection_loads_model",
        "contract_inspection_runs_inference",
        "contract_inspection_executes_game",
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
            "V9 input-order launcher boundary drift: " + field,
        )
    _require(
        out.get("next_gate") == NEXT_GATE,
        "V9 input-order launcher host-execution frontier drift",
    )

    auth = out.get("authorization")
    _require(
        isinstance(auth, dict),
        "V9 input-order launcher authorization missing",
    )
    _require(
        auth.get(
            "pair06_v9_input_order_execution_authorization_acceptance_reviewed"
        )
        is True,
        "V9 input-order launcher authorization review missing",
    )
    _require(
        auth.get("authorization_text_sha256")
        == "ad1edd0797e2ec6d95d0a4346a09d1a6d02e7f47ba32029cd6d80ec48c532af3",
        "V9 input-order launcher authorization text binding drift",
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


def pair06_v9_input_order_authorized_execution_launcher_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "launcher_path": LAUNCHER_PATH,
        "launcher_git_blob": LAUNCHER_GIT_BLOB,
        "launcher_test_path": LAUNCHER_TEST_PATH,
        "launcher_test_git_blob": LAUNCHER_TEST_GIT_BLOB,
        "pair06_v9_input_order_authorized_execution_launcher_reviewed": True,
        "policy_id": validated["policy_id"],
        "intervention_id": validated["intervention_id"],
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "fresh_preclaim_gpu_observation_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "fresh_order_evidence_namespace_required": True,
        "exact_canonical_blobs_required_before_execution": True,
        "explicit_launcher_confirmation_required": True,
        "authorization_reusable_after_attempt_claim": False,
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
        "validated_launcher": validated,
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


def execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9InputOrderCoherenceAuthorizedExecutionLauncherReviewHold(
        NEXT_GATE
    )
