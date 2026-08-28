from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping
from typing import Any

BRAIN_MANIFEST_SCHEMA = "void.general-brain-generation.v1"
TRAINING_ELIGIBILITY_SCHEMA = "void.general-brain-training-eligibility.v1"
V22_PAIR_SCHEMA = "void.apollyon.conditional-engagement-v2-2-pair-comparison.v2"
SUPPORTED_GENERALS = ("apollyon", "abaddon")

# These controls are intentionally outside the trainable competence adapter.
# A challenger generation may improve tactics, but it may not learn a new
# authority hierarchy, expand its tools, or acquire its own promotion power.
NONTRAINABLE_AUTHORITY_ENVELOPE = {
    "authority_policy_trainable": False,
    "role_hierarchy_trainable": False,
    "sovereign_directives_trainable": False,
    "tool_authorization_trainable": False,
    "promotion_authority_trainable": False,
    "host_tool_gate_enforced": True,
    "external_alignment_gate_enforced": True,
}


class GeneralBrainContractError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise GeneralBrainContractError(message)


def _obj(value: Any, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), f"{label} must be an object")
    return value


def _sha256(value: Any, label: str) -> str:
    _require(
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value),
        f"{label} must be lowercase SHA-256",
    )
    return value


def stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def manifest_sha256(manifest: Mapping[str, Any]) -> str:
    validate_brain_manifest(manifest)
    return hashlib.sha256(stable_json(manifest).encode("utf-8")).hexdigest()


def validate_brain_manifest(manifest: Mapping[str, Any]) -> None:
    manifest = _obj(manifest, "manifest")
    _require(manifest.get("schema") == BRAIN_MANIFEST_SCHEMA, "brain manifest schema drift")
    general_id = manifest.get("general_id")
    _require(general_id in SUPPORTED_GENERALS, "unsupported general_id")
    generation = manifest.get("generation")
    _require(type(generation) is int and generation >= 0, "generation must be integer >= 0")

    base = _obj(manifest.get("base_model"), "base_model")
    _require(base.get("replaceable") is True, "base model must remain replaceable")
    _require(base.get("identity_boundary") is False, "base model may not become identity boundary")

    adapter = _obj(manifest.get("competence_adapter"), "competence_adapter")
    _require(adapter.get("trainable") is True, "competence adapter must be trainable")
    _require(adapter.get("scope") == "tactical_competence_only", "competence adapter scope drift")
    state = adapter.get("state")
    _require(state in {"untrained", "challenger", "incumbent"}, "competence adapter state invalid")
    artifact_sha = adapter.get("artifact_sha256")
    if state == "untrained":
        _require(artifact_sha is None, "untrained adapter may not claim artifact SHA-256")
    else:
        _sha256(artifact_sha, "competence adapter artifact_sha256")

    authority = dict(_obj(manifest.get("authority_envelope"), "authority_envelope"))
    _require(authority == NONTRAINABLE_AUTHORITY_ENVELOPE, "nontrainable authority envelope drift")

    learning = _obj(manifest.get("learning"), "learning")
    _require(learning.get("automatic_corpus_admission") is False, "automatic corpus admission forbidden")
    _require(learning.get("automatic_weight_mutation") is False, "automatic weight mutation forbidden")
    _require(learning.get("automatic_promotion") is False, "automatic promotion forbidden")
    _require(learning.get("reviewed_evidence_required") is True, "reviewed evidence must be required")
    _require(learning.get("rollback_generation_retained") is True, "rollback generation must be retained")


def make_generation_zero(general_id: str) -> dict[str, Any]:
    _require(general_id in SUPPORTED_GENERALS, "unsupported general_id")
    manifest = {
        "schema": BRAIN_MANIFEST_SCHEMA,
        "general_id": general_id,
        "generation": 0,
        "base_model": {
            "replaceable": True,
            "identity_boundary": False,
            "binding": "external-runtime-model",
        },
        "competence_adapter": {
            "trainable": True,
            "scope": "tactical_competence_only",
            "state": "untrained",
            "artifact_sha256": None,
        },
        "authority_envelope": dict(NONTRAINABLE_AUTHORITY_ENVELOPE),
        "learning": {
            "automatic_corpus_admission": False,
            "automatic_weight_mutation": False,
            "automatic_promotion": False,
            "reviewed_evidence_required": True,
            "rollback_generation_retained": True,
        },
    }
    validate_brain_manifest(manifest)
    return manifest


def classify_apollyon_v22_pair_for_training(pair: Mapping[str, Any]) -> dict[str, Any]:
    """Classify one reviewed V2.2 pair for positive Apollyon competence training.

    This gate intentionally admits only clear improvements. Ties, regressions,
    protocol retries, or behavioral-gate failures remain diagnostic evidence but
    do not become positive training examples.
    """

    pair = _obj(pair, "pair")
    reasons: list[str] = []

    if pair.get("schema") != V22_PAIR_SCHEMA:
        reasons.append("PAIR_SCHEMA_NOT_REVIEWED_V2")
    if pair.get("candidate_only") is not True:
        reasons.append("PAIR_NOT_CANDIDATE_ONLY")

    warm = pair.get("warm_start_binding")
    if not isinstance(warm, Mapping) or warm.get("semantic_match") is not True:
        reasons.append("WARM_START_NOT_SEMANTICALLY_BOUND")

    candidate = pair.get("candidate")
    if not isinstance(candidate, Mapping):
        reasons.append("CANDIDATE_REPORT_MISSING")
        candidate = {}
    elif candidate.get("reviewed_identity_verified") is not True:
        reasons.append("CANDIDATE_IDENTITY_NOT_REVIEWED")

    comparison = pair.get("comparison")
    if not isinstance(comparison, Mapping):
        reasons.append("COMPARISON_MISSING")
        comparison = {}
    else:
        if comparison.get("verdict") != "BETTER":
            reasons.append("PRIMARY_METRIC_NOT_BETTER")
        if comparison.get("protocol_clean") is not True:
            reasons.append("PROTOCOL_NOT_CLEAN")
        if comparison.get("force_preservation_pass") is not True:
            reasons.append("FORCE_PRESERVATION_FAILED")
        if comparison.get("productive_contact_pass") is not True:
            reasons.append("PRODUCTIVE_CONTACT_FAILED")
        if comparison.get("attack_move_reduction_pass") is not True:
            reasons.append("ATTACK_MOVE_BEHAVIOR_GATE_FAILED")

    trajectory_sha = candidate.get("trajectory_sha256")
    if trajectory_sha is not None:
        try:
            _sha256(trajectory_sha, "candidate trajectory_sha256")
        except GeneralBrainContractError:
            reasons.append("CANDIDATE_TRAJECTORY_SHA_INVALID")
    else:
        reasons.append("CANDIDATE_TRAJECTORY_SHA_MISSING")

    eligible = not reasons
    return {
        "schema": TRAINING_ELIGIBILITY_SCHEMA,
        "general_id": "apollyon",
        "eligible": eligible,
        "training_role": "positive_tactical_example" if eligible else "diagnostic_only",
        "candidate_trajectory_sha256": trajectory_sha if eligible else None,
        "reasons": reasons,
        "authority_envelope_trainable": False,
        "automatic_corpus_admission": False,
        "automatic_weight_mutation": False,
        "automatic_promotion": False,
    }


def classify_abaddon_from_apollyon_v22_pair(pair: Mapping[str, Any]) -> dict[str, Any]:
    """Fail closed until Abaddon has its own symmetric challenger evaluator."""

    _obj(pair, "pair")
    return {
        "schema": TRAINING_ELIGIBILITY_SCHEMA,
        "general_id": "abaddon",
        "eligible": False,
        "training_role": "diagnostic_only",
        "candidate_trajectory_sha256": None,
        "reasons": ["ABADDON_REQUIRES_SYMMETRIC_REVIEWED_CHALLENGER_EVIDENCE"],
        "authority_envelope_trainable": False,
        "automatic_corpus_admission": False,
        "automatic_weight_mutation": False,
        "automatic_promotion": False,
    }


def make_challenger_generation(
    parent: Mapping[str, Any],
    *,
    adapter_artifact_sha256: str,
    corpus_snapshot_sha256: str,
    training_receipt_sha256: str,
) -> dict[str, Any]:
    """Create a challenger manifest while preserving the authority envelope exactly."""

    validate_brain_manifest(parent)
    adapter_sha = _sha256(adapter_artifact_sha256, "adapter_artifact_sha256")
    corpus_sha = _sha256(corpus_snapshot_sha256, "corpus_snapshot_sha256")
    receipt_sha = _sha256(training_receipt_sha256, "training_receipt_sha256")

    challenger = copy.deepcopy(dict(parent))
    challenger["generation"] = int(parent["generation"]) + 1
    challenger["competence_adapter"] = {
        "trainable": True,
        "scope": "tactical_competence_only",
        "state": "challenger",
        "artifact_sha256": adapter_sha,
    }
    challenger["training_lineage"] = {
        "parent_manifest_sha256": manifest_sha256(parent),
        "corpus_snapshot_sha256": corpus_sha,
        "training_receipt_sha256": receipt_sha,
    }
    _require(
        challenger["authority_envelope"] == parent["authority_envelope"] == NONTRAINABLE_AUTHORITY_ENVELOPE,
        "challenger authority envelope changed",
    )
    validate_brain_manifest(challenger)
    return challenger
