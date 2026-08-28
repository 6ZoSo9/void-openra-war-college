from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from openra_env.analysis._spar_conditional_v2_2 import validate_conditional_v22_evidence
from openra_env.analysis._spar_contract import (
    MAX_TRAJECTORY_BYTES,
    ContractError,
    _arr,
    _header,
    _jsonl,
    _obj,
    _pairs,
    _read,
)
from openra_env.learning.general_brain_generation import (
    GeneralBrainContractError,
    NONTRAINABLE_AUTHORITY_ENVELOPE,
    make_challenger_generation,
    manifest_sha256,
    stable_json,
    validate_brain_manifest,
)

CORPUS_SNAPSHOT_SCHEMA = "void.general-brain-reviewed-corpus-snapshot.v1"
PREFERENCE_RECORD_SCHEMA = "void.general-brain-tactical-preference-record.v1"
IMITATION_RECORD_SCHEMA = "void.general-brain-positive-imitation-record.v1"
ADAPTER_SCHEMA = "void.general-brain-tactical-preference-adapter.v1"
TRAINING_RECEIPT_SCHEMA = "void.general-brain-training-receipt.v1"
PROMOTION_EVALUATION_SCHEMA = "void.general-brain-challenger-evaluation.v1"
PROMOTION_DECISION_SCHEMA = "void.general-brain-promotion-decision.v1"
ALGORITHM_ID = "deterministic_pairwise_tool_preference_v1"


class GeneralBrainTrainingError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise GeneralBrainTrainingError(message)


def _sha256(value: Any, label: str) -> str:
    _require(
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value),
        f"{label} must be lowercase SHA-256",
    )
    return value


def _canonical_sha(value: Mapping[str, Any]) -> str:
    return hashlib.sha256((stable_json(dict(value)) + "\n").encode("utf-8")).hexdigest()


def _tool_call(tool: str, arguments: Mapping[str, Any] | None = None) -> dict[str, Any]:
    _require(isinstance(tool, str) and tool, "tool must be nonempty text")
    return {"tool": tool, "arguments": copy.deepcopy(dict(arguments or {}))}


def _attempt_arguments(attempt: Mapping[str, Any]) -> Mapping[str, Any] | None:
    for key in ("arguments", "args"):
        value = attempt.get(key)
        if isinstance(value, Mapping):
            return value
    return None


def _clean_context(prepared: Mapping[str, Any]) -> dict[str, Any]:
    decision = _obj(prepared.get("decision"), "prepared.decision")
    compliance = _obj(prepared.get("action_compliance"), "prepared.action_compliance")
    allowed = _arr(prepared.get("current_allowed_tool_names"), "prepared.current_allowed_tool_names")
    _require(all(isinstance(name, str) and name for name in allowed), "allowed tool names malformed")
    coaching = prepared.get("coaching")
    _require(isinstance(coaching, str) and coaching, "prepared coaching missing")
    reasons = decision.get("reasons")
    _require(isinstance(reasons, list) and all(isinstance(value, str) for value in reasons), "decision reasons malformed")
    return {
        "mode": decision.get("mode"),
        "reasons": list(reasons),
        "coaching": coaching,
        "allowed_tool_names": list(allowed),
        "action_compliance": copy.deepcopy(dict(compliance)),
    }


def extract_apollyon_training_records(
    trajectory_path: Path,
    *,
    expected_trajectory_sha256: str | None = None,
) -> list[dict[str, Any]]:
    """Extract reviewed tactical preference records without importing authority labels.

    A whole bout does not need to be a tactical win for a FORCE_CONVERSION
    mistake/correction record to be useful. The source round itself must still
    be exact-identity V2.2 evidence, first-attempt, and unchanged before host
    validation. Positive imitation is stricter: the accepted preferred action
    must carry the reviewed all_combat selector in the structured attempt.
    """

    path = trajectory_path.expanduser().resolve()
    raw = _read(path, "trajectory", MAX_TRAJECTORY_BYTES)
    trajectory_sha = hashlib.sha256(raw).hexdigest()
    if expected_trajectory_sha256 is not None:
        _require(trajectory_sha == _sha256(expected_trajectory_sha256, "trajectory SHA-256"), "trajectory SHA-256 mismatch")

    rows = _jsonl(raw)
    _require(bool(rows), "trajectory is empty")
    header = _header(rows[0])
    pairs = _pairs(rows[1:])

    reviewed = validate_conditional_v22_evidence(
        path,
        expected_trajectory_sha256=trajectory_sha,
    )
    _require(reviewed.get("present") is True, "trajectory is not reviewed V2.2 evidence")
    _require(reviewed.get("reviewed_identity_verified") is True, "V2.2 reviewed identity is not verified")
    _require(reviewed.get("all_round_receipts_verified") is True, "V2.2 round receipts are not verified")
    _require(reviewed.get("tool_surface_bound") is True, "V2.2 tool surface is not bound")
    _require(reviewed.get("accepted_tool_bound") is True, "V2.2 accepted tool is not bound")
    _require(reviewed.get("runtime_seed_branching") is False, "runtime seed branching detected")

    records: list[dict[str, Any]] = []
    for number, (decision_row, _result_row) in enumerate(pairs, 1):
        apollyon = _obj(decision_row.get("apollyon"), f"round {number} apollyon")
        attempts = _arr(apollyon.get("attempts"), f"round {number} apollyon attempts")
        # Retry rounds are useful diagnostics but are not weight-training input.
        if len(attempts) != 1:
            continue
        attempt = _obj(attempts[0], f"round {number} attempt")
        if attempt.get("accepted") is not True or attempt.get("world_mutated_before_validation") is not False:
            continue

        evidence = _obj(
            decision_row.get("conditional_engagement_v2_2"),
            f"round {number} V2.2 evidence",
        )
        prepared = _obj(evidence.get("prepared"), f"round {number} prepared")
        accepted = _obj(evidence.get("accepted"), f"round {number} accepted")
        context = _clean_context(prepared)
        compliance = _obj(context["action_compliance"], "action_compliance")
        selected = accepted.get("selected_tool")
        _require(isinstance(selected, str) and selected, "accepted selected_tool missing")
        _require(attempt.get("tool") == selected, "structured attempt tool does not match accepted receipt")

        if (
            context["mode"] == "FORCE_CONVERSION"
            and compliance.get("attack_move_discouraged") is True
            and compliance.get("preferred_offered_alternative") == "move_units"
            and "move_units" in context["allowed_tool_names"]
        ):
            coaching = context["coaching"]
            _require('PREFERRED_MOVE_UNITS_SELECTOR=unit_ids="all_combat"' in coaching, "reviewed selector guidance missing")
            _require('unit_ids="all_combat" exactly' in coaching, "selector-integrity rule missing")

            common = {
                "general_id": "apollyon",
                "source_trajectory_sha256": trajectory_sha,
                "source_round": number,
                "seed": header["seed"],
                "candidate_sha256": reviewed["candidate_sha256"],
                "context": context,
                "authority_labels_included": False,
                "automatic_corpus_admission": False,
                "automatic_weight_mutation": False,
                "automatic_promotion": False,
            }

            if selected == "attack_move":
                records.append(
                    {
                        "schema": PREFERENCE_RECORD_SCHEMA,
                        **common,
                        "training_role": "reviewed_counterfactual_preference",
                        "chosen": _tool_call("move_units", {"unit_ids": "all_combat"}),
                        "rejected": _tool_call("attack_move", _attempt_arguments(attempt)),
                        "reason": "FORCE_CONVERSION_REVIEWED_SELECTOR_PREFERRED_OVER_BLIND_ATTACK_MOVE",
                    }
                )
            elif selected == "move_units":
                arguments = _attempt_arguments(attempt)
                if isinstance(arguments, Mapping) and arguments.get("unit_ids") == "all_combat":
                    records.append(
                        {
                            "schema": IMITATION_RECORD_SCHEMA,
                            **common,
                            "training_role": "reviewed_positive_imitation",
                            "chosen": _tool_call("move_units", arguments),
                            "reason": "FORCE_CONVERSION_ACCEPTED_REVIEWED_SELECTOR_FIRST_ATTEMPT",
                        }
                    )

    return records


def build_corpus_snapshot(
    general_id: str,
    trajectories: Sequence[tuple[Path, str | None]],
) -> dict[str, Any]:
    _require(general_id in {"apollyon", "abaddon"}, "unsupported general_id")
    _require(bool(trajectories), "at least one trajectory is required")
    if general_id != "apollyon":
        raise GeneralBrainTrainingError("Abaddon requires its own symmetric reviewed extractor before training")

    records: list[dict[str, Any]] = []
    source_shas: set[str] = set()
    seen: set[tuple[str, int, str]] = set()
    for path, expected_sha in trajectories:
        extracted = extract_apollyon_training_records(path, expected_trajectory_sha256=expected_sha)
        for record in extracted:
            key = (
                str(record["source_trajectory_sha256"]),
                int(record["source_round"]),
                str(record["schema"]),
            )
            if key in seen:
                continue
            seen.add(key)
            source_shas.add(str(record["source_trajectory_sha256"]))
            records.append(record)

    records.sort(key=lambda value: (value["source_trajectory_sha256"], value["source_round"], value["schema"]))
    preference_count = sum(record["schema"] == PREFERENCE_RECORD_SCHEMA for record in records)
    imitation_count = sum(record["schema"] == IMITATION_RECORD_SCHEMA for record in records)
    return {
        "schema": CORPUS_SNAPSHOT_SCHEMA,
        "general_id": general_id,
        "scope": "tactical_competence_only",
        "records": records,
        "record_count": len(records),
        "preference_record_count": preference_count,
        "positive_imitation_record_count": imitation_count,
        "source_trajectory_sha256": sorted(source_shas),
        "excluded_from_training": [
            "authority_envelope",
            "role_hierarchy",
            "sovereign_directives",
            "tool_authorization",
            "promotion_authority",
        ],
        "authority_envelope_trainable": False,
        "automatic_corpus_admission": False,
        "automatic_weight_mutation": False,
        "automatic_promotion": False,
    }


def validate_corpus_snapshot(snapshot: Mapping[str, Any]) -> None:
    snapshot = _obj(snapshot, "corpus snapshot")
    _require(snapshot.get("schema") == CORPUS_SNAPSHOT_SCHEMA, "corpus snapshot schema drift")
    _require(snapshot.get("general_id") in {"apollyon", "abaddon"}, "corpus general_id invalid")
    _require(snapshot.get("scope") == "tactical_competence_only", "corpus scope drift")
    records = _arr(snapshot.get("records"), "corpus records")
    _require(snapshot.get("record_count") == len(records), "corpus record_count mismatch")
    for key in ("authority_envelope_trainable", "automatic_corpus_admission", "automatic_weight_mutation", "automatic_promotion"):
        _require(snapshot.get(key) is False, f"corpus authority drift: {key}")
    forbidden = set(snapshot.get("excluded_from_training", []))
    _require({"authority_envelope", "role_hierarchy", "sovereign_directives", "tool_authorization", "promotion_authority"} <= forbidden, "corpus exclusion wall incomplete")
    for index, record in enumerate(records):
        record = _obj(record, f"record {index}")
        _require(record.get("schema") in {PREFERENCE_RECORD_SCHEMA, IMITATION_RECORD_SCHEMA}, "unsupported training record schema")
        _require(record.get("general_id") == snapshot.get("general_id"), "record general_id mismatch")
        _sha256(record.get("source_trajectory_sha256"), "record trajectory SHA-256")
        _require(type(record.get("source_round")) is int and record["source_round"] >= 1, "record source_round invalid")
        _require(record.get("authority_labels_included") is False, "authority labels leaked into training record")
        for key in ("automatic_corpus_admission", "automatic_weight_mutation", "automatic_promotion"):
            _require(record.get(key) is False, f"training record authority drift: {key}")


def corpus_snapshot_sha256(snapshot: Mapping[str, Any]) -> str:
    validate_corpus_snapshot(snapshot)
    return _canonical_sha(snapshot)


def train_tactical_preference_adapter(
    parent_manifest: Mapping[str, Any],
    corpus_snapshot: Mapping[str, Any],
) -> dict[str, Any]:
    validate_brain_manifest(parent_manifest)
    validate_corpus_snapshot(corpus_snapshot)
    _require(parent_manifest.get("general_id") == corpus_snapshot.get("general_id"), "manifest/corpus general mismatch")
    records = list(corpus_snapshot["records"])
    _require(bool(records), "reviewed corpus has no trainable tactical records")

    weights: dict[str, dict[str, float]] = {}
    for record in records:
        context = _obj(record.get("context"), "record context")
        mode = context.get("mode")
        _require(isinstance(mode, str) and mode, "record mode missing")
        mode_weights = weights.setdefault(mode, {})
        chosen = _obj(record.get("chosen"), "record chosen")
        chosen_tool = chosen.get("tool")
        _require(isinstance(chosen_tool, str) and chosen_tool, "chosen tool missing")
        increment = 1.0 if record["schema"] == PREFERENCE_RECORD_SCHEMA else 0.25
        mode_weights[chosen_tool] = mode_weights.get(chosen_tool, 0.0) + increment
        if record["schema"] == PREFERENCE_RECORD_SCHEMA:
            rejected = _obj(record.get("rejected"), "record rejected")
            rejected_tool = rejected.get("tool")
            _require(isinstance(rejected_tool, str) and rejected_tool, "rejected tool missing")
            mode_weights[rejected_tool] = mode_weights.get(rejected_tool, 0.0) - 1.0

    normalized = {
        mode: {tool: weights[mode][tool] for tool in sorted(weights[mode])}
        for mode in sorted(weights)
    }
    adapter = {
        "schema": ADAPTER_SCHEMA,
        "general_id": parent_manifest["general_id"],
        "scope": "tactical_competence_only",
        "algorithm": ALGORITHM_ID,
        "parent_manifest_sha256": manifest_sha256(parent_manifest),
        "corpus_snapshot_sha256": corpus_snapshot_sha256(corpus_snapshot),
        "record_count": len(records),
        "weights": normalized,
        "authority_envelope_embedded": False,
        "tool_authorization_embedded": False,
        "promotion_authority_embedded": False,
    }
    return adapter


def validate_adapter(adapter: Mapping[str, Any]) -> None:
    adapter = _obj(adapter, "adapter")
    _require(adapter.get("schema") == ADAPTER_SCHEMA, "adapter schema drift")
    _require(adapter.get("general_id") in {"apollyon", "abaddon"}, "adapter general_id invalid")
    _require(adapter.get("scope") == "tactical_competence_only", "adapter scope drift")
    _require(adapter.get("algorithm") == ALGORITHM_ID, "adapter algorithm drift")
    _sha256(adapter.get("parent_manifest_sha256"), "adapter parent manifest SHA-256")
    _sha256(adapter.get("corpus_snapshot_sha256"), "adapter corpus SHA-256")
    _require(type(adapter.get("record_count")) is int and adapter["record_count"] >= 1, "adapter record_count invalid")
    weights = _obj(adapter.get("weights"), "adapter weights")
    _require(bool(weights), "adapter weights are empty")
    for mode, raw in weights.items():
        _require(isinstance(mode, str) and mode, "adapter mode invalid")
        tool_weights = _obj(raw, f"adapter weights {mode}")
        for tool, score in tool_weights.items():
            _require(isinstance(tool, str) and tool, "adapter tool invalid")
            _require(type(score) in (int, float), "adapter weight must be numeric")
    for key in ("authority_envelope_embedded", "tool_authorization_embedded", "promotion_authority_embedded"):
        _require(adapter.get(key) is False, f"adapter authority leakage: {key}")


def adapter_sha256(adapter: Mapping[str, Any]) -> str:
    validate_adapter(adapter)
    return _canonical_sha(adapter)


def make_training_receipt(
    parent_manifest: Mapping[str, Any],
    corpus_snapshot: Mapping[str, Any],
    adapter: Mapping[str, Any],
) -> dict[str, Any]:
    validate_brain_manifest(parent_manifest)
    validate_corpus_snapshot(corpus_snapshot)
    validate_adapter(adapter)
    _require(adapter.get("parent_manifest_sha256") == manifest_sha256(parent_manifest), "adapter parent binding mismatch")
    _require(adapter.get("corpus_snapshot_sha256") == corpus_snapshot_sha256(corpus_snapshot), "adapter corpus binding mismatch")
    return {
        "schema": TRAINING_RECEIPT_SCHEMA,
        "general_id": parent_manifest["general_id"],
        "algorithm": ALGORITHM_ID,
        "parent_manifest_sha256": manifest_sha256(parent_manifest),
        "corpus_snapshot_sha256": corpus_snapshot_sha256(corpus_snapshot),
        "adapter_artifact_sha256": adapter_sha256(adapter),
        "record_count": corpus_snapshot["record_count"],
        "scope": "tactical_competence_only",
        "authority_envelope_sha256": _canonical_sha(NONTRAINABLE_AUTHORITY_ENVELOPE),
        "authority_envelope_trainable": False,
        "automatic_weight_mutation": False,
        "automatic_promotion": False,
    }


def training_receipt_sha256(receipt: Mapping[str, Any]) -> str:
    receipt = _obj(receipt, "training receipt")
    _require(receipt.get("schema") == TRAINING_RECEIPT_SCHEMA, "training receipt schema drift")
    _sha256(receipt.get("parent_manifest_sha256"), "receipt parent manifest SHA-256")
    _sha256(receipt.get("corpus_snapshot_sha256"), "receipt corpus SHA-256")
    _sha256(receipt.get("adapter_artifact_sha256"), "receipt adapter SHA-256")
    _require(receipt.get("scope") == "tactical_competence_only", "training receipt scope drift")
    _require(receipt.get("authority_envelope_trainable") is False, "training receipt authority drift")
    _require(receipt.get("automatic_weight_mutation") is False, "automatic weight mutation forbidden")
    _require(receipt.get("automatic_promotion") is False, "automatic promotion forbidden")
    return _canonical_sha(receipt)


def make_challenger_from_training(
    parent_manifest: Mapping[str, Any],
    corpus_snapshot: Mapping[str, Any],
    adapter: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> dict[str, Any]:
    return make_challenger_generation(
        parent_manifest,
        adapter_artifact_sha256=adapter_sha256(adapter),
        corpus_snapshot_sha256=corpus_snapshot_sha256(corpus_snapshot),
        training_receipt_sha256=training_receipt_sha256(receipt),
    )


def evaluate_promotion(
    incumbent_manifest: Mapping[str, Any],
    challenger_manifest: Mapping[str, Any],
    evaluation: Mapping[str, Any],
) -> dict[str, Any]:
    validate_brain_manifest(incumbent_manifest)
    validate_brain_manifest(challenger_manifest)
    evaluation = _obj(evaluation, "promotion evaluation")
    reasons: list[str] = []

    if evaluation.get("schema") != PROMOTION_EVALUATION_SCHEMA:
        reasons.append("EVALUATION_SCHEMA_INVALID")
    if incumbent_manifest.get("general_id") != challenger_manifest.get("general_id"):
        reasons.append("GENERAL_ID_MISMATCH")
    if challenger_manifest.get("generation") != incumbent_manifest.get("generation") + 1:
        reasons.append("CHALLENGER_GENERATION_NOT_NEXT")
    if incumbent_manifest.get("authority_envelope") != challenger_manifest.get("authority_envelope"):
        reasons.append("AUTHORITY_ENVELOPE_DRIFT")
    if evaluation.get("incumbent_manifest_sha256") != manifest_sha256(incumbent_manifest):
        reasons.append("INCUMBENT_BINDING_MISMATCH")
    if evaluation.get("challenger_manifest_sha256") != manifest_sha256(challenger_manifest):
        reasons.append("CHALLENGER_BINDING_MISMATCH")
    if evaluation.get("authority_envelope_match") is not True:
        reasons.append("AUTHORITY_EVALUATION_FAILED")
    if evaluation.get("all_protocol_clean") is not True:
        reasons.append("PROTOCOL_NOT_CLEAN")
    if evaluation.get("all_behavioral_gates_pass") is not True:
        reasons.append("BEHAVIORAL_GATE_FAILED")

    critical = evaluation.get("critical_seeds")
    if not isinstance(critical, Mapping):
        reasons.append("CRITICAL_SEEDS_MISSING")
        critical = {}
    regression = critical.get("2051") if isinstance(critical, Mapping) else None
    gain = critical.get("2055") if isinstance(critical, Mapping) else None
    if not isinstance(regression, Mapping) or regression.get("complete") is not True or regression.get("median_challenger_minus_incumbent", -1) < 0:
        reasons.append("REGRESSION_SEED_2051_FAILED")
    if not isinstance(gain, Mapping) or gain.get("complete") is not True or gain.get("median_challenger_minus_incumbent", 0) <= 0:
        reasons.append("GAIN_SEED_2055_FAILED")

    heldout = evaluation.get("heldout_seeds")
    if not isinstance(heldout, Mapping) or len(heldout) < 3:
        reasons.append("HELDOUT_COVERAGE_INCOMPLETE")
    else:
        for seed, raw in heldout.items():
            if not isinstance(raw, Mapping) or raw.get("complete") is not True or raw.get("worse_pairs", 99) > 1:
                reasons.append(f"HELDOUT_SEED_{seed}_FAILED")

    eligible = not reasons
    return {
        "schema": PROMOTION_DECISION_SCHEMA,
        "general_id": challenger_manifest.get("general_id"),
        "eligible_for_promotion": eligible,
        "reasons": reasons,
        "authority_envelope_preserved": incumbent_manifest.get("authority_envelope") == challenger_manifest.get("authority_envelope") == NONTRAINABLE_AUTHORITY_ENVELOPE,
        "automatic_promotion": False,
        "review_required": True,
    }


__all__ = [
    "ADAPTER_SCHEMA",
    "CORPUS_SNAPSHOT_SCHEMA",
    "GeneralBrainTrainingError",
    "PROMOTION_EVALUATION_SCHEMA",
    "adapter_sha256",
    "build_corpus_snapshot",
    "corpus_snapshot_sha256",
    "evaluate_promotion",
    "extract_apollyon_training_records",
    "make_challenger_from_training",
    "make_training_receipt",
    "train_tactical_preference_adapter",
    "training_receipt_sha256",
    "validate_adapter",
    "validate_corpus_snapshot",
]
