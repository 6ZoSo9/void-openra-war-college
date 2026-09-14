"""Manual-review admission gate for symmetric Abaddon policy-candidate evidence."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from typing import Any

from openra_env.analysis.spar_abaddon_policy_candidate_pair import PAIR_SCHEMA

ELIGIBILITY_SCHEMA = "void.general-brain-training-eligibility.v1"
REVIEW_SCHEMA = "void.abaddon.policy-candidate-review.v1"

# One symmetric pair is useful diagnostic evidence, but the recovered Abaddon
# refiner requires a reviewed campaign before policy/training admission:
# >=12 reviewed matches, >=6 seeds, >=2 Apollyon snapshots, zero infra failures.
PAIR_LEVEL_ADMISSION_DISABLED_REASON = "ABADDON_REVIEWED_CAMPAIGN_REQUIRED"


def stable_json_bytes(value: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def pair_sha256(pair: Mapping[str, Any]) -> str:
    return hashlib.sha256(stable_json_bytes(pair)).hexdigest()


def _sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value)
    )


def classify_abaddon_policy_candidate_pair_for_training(
    pair: Mapping[str, Any] | None,
    *,
    review: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate one pair for diagnostics, but never admit it by itself."""
    reasons: list[str] = []

    if not isinstance(pair, Mapping):
        reasons.append("ABADDON_PAIR_REQUIRED")
    elif pair.get("schema") != PAIR_SCHEMA:
        reasons.append("ABADDON_PAIR_SCHEMA_MISMATCH")
    else:
        if pair.get("candidate_only") is not True:
            reasons.append("ABADDON_PAIR_NOT_CANDIDATE_ONLY")
        if pair.get("review_required") is not True:
            reasons.append("ABADDON_PAIR_REVIEW_WALL_MISSING")

        comparison = pair.get("comparison")
        candidate = pair.get("candidate")
        authority = pair.get("authority")

        if not isinstance(comparison, Mapping):
            reasons.append("ABADDON_COMPARISON_MISSING")
        else:
            if comparison.get("verdict") != "BETTER":
                reasons.append("ABADDON_NOT_BETTER")
            for key, reason in (
                ("force_preservation_pass", "ABADDON_FORCE_PRESERVATION_FAILED"),
                ("protocol_clean", "ABADDON_PROTOCOL_NOT_CLEAN"),
                ("productive_contact_pass", "ABADDON_PRODUCTIVE_CONTACT_FAILED"),
                ("host_acceptance_pass", "ABADDON_HOST_ACCEPTANCE_FAILED"),
                ("review_candidate_pass", "ABADDON_REVIEW_CANDIDATE_FAILED"),
            ):
                if comparison.get(key) is not True:
                    reasons.append(reason)

        if not isinstance(candidate, Mapping):
            reasons.append("ABADDON_CANDIDATE_IDENTITY_MISSING")
        else:
            for key in (
                "trajectory_sha256",
                "candidate_genome_sha256",
                "candidate_file_sha256",
                "wrapper_sha256",
                "legacy_runner_sha256",
                "abaddon_controller_sha256",
                "abaddon_refiner_sha256",
            ):
                if not _sha256(candidate.get(key)):
                    reasons.append(f"ABADDON_{key.upper()}_INVALID")

        if not isinstance(authority, Mapping):
            reasons.append("ABADDON_AUTHORITY_WALL_MISSING")
        else:
            for key in (
                "training_performed",
                "weights_updated",
                "automatic_corpus_admission",
                "automatic_weight_mutation",
                "automatic_promotion",
            ):
                if authority.get(key) is not False:
                    reasons.append(f"ABADDON_AUTHORITY_DRIFT_{key.upper()}")

    if review is None:
        reasons.append("ABADDON_REVIEW_REQUIRED")
    elif not isinstance(review, Mapping):
        reasons.append("ABADDON_REVIEW_MALFORMED")
    else:
        if review.get("schema") != REVIEW_SCHEMA:
            reasons.append("ABADDON_REVIEW_SCHEMA_MISMATCH")
        if review.get("general_id") != "abaddon":
            reasons.append("ABADDON_REVIEW_GENERAL_MISMATCH")
        reviewer = review.get("reviewer")
        if not isinstance(reviewer, str) or not reviewer.strip():
            reasons.append("ABADDON_REVIEWER_REQUIRED")
        for key, reason in (
            ("review_complete", "ABADDON_REVIEW_INCOMPLETE"),
            ("candidate_identity_reviewed", "ABADDON_IDENTITY_NOT_REVIEWED"),
            ("comparison_reviewed", "ABADDON_COMPARISON_NOT_REVIEWED"),
            ("training_use_approved", "ABADDON_TRAINING_USE_NOT_APPROVED"),
        ):
            if review.get(key) is not True:
                reasons.append(reason)

        if isinstance(pair, Mapping):
            expected_pair_sha = pair_sha256(pair)
            if review.get("pair_sha256") != expected_pair_sha:
                reasons.append("ABADDON_REVIEW_PAIR_SHA_MISMATCH")

    # Critical fail-closed correction: no single pair can satisfy the recovered
    # Abaddon campaign/refiner review requirements.
    if PAIR_LEVEL_ADMISSION_DISABLED_REASON not in reasons:
        reasons.append(PAIR_LEVEL_ADMISSION_DISABLED_REASON)

    return {
        "schema": ELIGIBILITY_SCHEMA,
        "general_id": "abaddon",
        "eligible": False,
        "training_role": "diagnostic_only",
        "candidate_trajectory_sha256": None,
        "candidate_genome_sha256": None,
        "reviewed_pair_sha256": None,
        "reasons": reasons,
        "authority_envelope_trainable": False,
        "automatic_corpus_admission": False,
        "automatic_weight_mutation": False,
        "automatic_promotion": False,
    }
