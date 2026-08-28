from __future__ import annotations

import copy
import hashlib
import json
import statistics
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from openra_env.analysis._spar_conditional_v2_2 import validate_conditional_v22_evidence
from openra_env.analysis._spar_contract import (
    MAX_TRAJECTORY_BYTES,
    _arr,
    _jsonl,
    _obj,
    _pairs,
    _read,
)
from openra_env.analysis._spar_metrics import military, visible_count
from openra_env.learning.general_brain_generation import (
    NONTRAINABLE_AUTHORITY_ENVELOPE,
    manifest_sha256,
    stable_json,
    validate_brain_manifest,
)

POLICY_SNAPSHOT_SCHEMA = "void.general-brain-utility-policy-snapshot.v1"
POLICY_RECORD_SCHEMA = "void.general-brain-utility-policy-record.v1"
POLICY_ADAPTER_SCHEMA = "void.general-brain-tactical-policy-adapter.v1"
POLICY_RECEIPT_SCHEMA = "void.general-brain-policy-training-receipt.v1"
ALGORITHM_ID = "utility_backed_direct_policy_v1"
UTILITY_HORIZON_ROUNDS = 3
MIN_POLICY_EXAMPLES = 3
MILLIS = 1000


class GeneralBrainPolicyError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise GeneralBrainPolicyError(message)


def _sha(value: Any, label: str) -> str:
    _require(
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value),
        f"{label} must be lowercase SHA-256",
    )
    return value


def _canonical_sha(value: Mapping[str, Any]) -> str:
    return hashlib.sha256((stable_json(dict(value)) + "\n").encode("utf-8")).hexdigest()


def _attempt_arguments(attempt: Mapping[str, Any]) -> Mapping[str, Any] | None:
    for key in ("arguments", "args"):
        value = attempt.get(key)
        if isinstance(value, Mapping):
            return value
    return None


def _map_dimensions(state: Mapping[str, Any]) -> tuple[int, int]:
    raw = state.get("map")
    _require(isinstance(raw, Mapping), "state.map missing")
    width, height = raw.get("width"), raw.get("height")
    _require(type(width) is int and width > 1, "map width invalid")
    _require(type(height) is int and height > 1, "map height invalid")
    return width, height


def _normalized_millis(value: int, extent: int) -> int:
    _require(0 <= value < extent, "target coordinate is out of bounds")
    return int(round((value / (extent - 1)) * MILLIS))


def _utility_over_horizon(
    before: Mapping[str, Any],
    horizon_after: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    _require(bool(horizon_after), "utility horizon is empty")
    start = military(dict(before))
    final = military(dict(horizon_after[-1]))
    kills_delta = final["kills_cost"] - start["kills_cost"]
    deaths_delta = final["deaths_cost"] - start["deaths_cost"]
    _require(kills_delta >= 0 and deaths_delta >= 0, "military counters regressed in utility horizon")
    net_delta = kills_delta - deaths_delta
    contact = any(visible_count(dict(state)) > 0 for state in horizon_after)
    damage = kills_delta > 0
    # Contact with no loss is useful scouting/conversion evidence. Damage must
    # be non-regressive on value. Pure legal movement with no tactical effect is
    # intentionally not positive training signal.
    positive = net_delta > 0 or (damage and net_delta >= 0) or (contact and deaths_delta == 0)
    return {
        "contact_observed": contact,
        "damage_inflicted": damage,
        "kills_cost_delta": kills_delta,
        "deaths_cost_delta": deaths_delta,
        "net_kill_cost_delta": net_delta,
        "utility_positive": positive,
    }


def classify_force_conversion_move(
    decision_row: Mapping[str, Any],
    horizon_results: Sequence[Mapping[str, Any]],
    *,
    source_trajectory_sha256: str,
    seed: int,
    round_no: int,
) -> dict[str, Any] | None:
    """Return one utility-backed portable move policy record or None.

    Validity alone is insufficient. The accepted move must be first-attempt,
    exact reviewed FORCE_CONVERSION evidence and produce bounded tactical
    utility within the post-action horizon.
    """

    _sha(source_trajectory_sha256, "source trajectory SHA-256")
    apollyon = _obj(decision_row.get("apollyon"), "apollyon decision")
    attempts = _arr(apollyon.get("attempts"), "apollyon attempts")
    if len(attempts) != 1:
        return None
    attempt = _obj(attempts[0], "apollyon attempt")
    if attempt.get("accepted") is not True or attempt.get("world_mutated_before_validation") is not False:
        return None
    if attempt.get("tool") != "move_units" or apollyon.get("tool") != "move_units":
        return None

    evidence = _obj(decision_row.get("conditional_engagement_v2_2"), "V2.2 evidence")
    prepared = _obj(evidence.get("prepared"), "V2.2 prepared")
    selected = _obj(prepared.get("decision"), "V2.2 prepared decision")
    if selected.get("mode") != "FORCE_CONVERSION":
        return None
    accepted = _obj(evidence.get("accepted"), "V2.2 accepted")
    if accepted.get("selected_tool") != "move_units":
        return None

    arguments = _attempt_arguments(attempt)
    if not isinstance(arguments, Mapping) or arguments.get("unit_ids") != "all_combat":
        return None
    target_x, target_y = arguments.get("target_x"), arguments.get("target_y")
    if type(target_x) is not int or type(target_y) is not int:
        return None

    before = _obj(decision_row.get("apollyon_state"), "apollyon_state")
    width, height = _map_dimensions(before)
    x_millis = _normalized_millis(target_x, width)
    y_millis = _normalized_millis(target_y, height)
    after_states = [
        _obj(row.get("apollyon_after"), f"utility result {index}")
        for index, row in enumerate(horizon_results, 1)
    ]
    utility = _utility_over_horizon(before, after_states)
    if utility["utility_positive"] is not True:
        return None

    return {
        "schema": POLICY_RECORD_SCHEMA,
        "general_id": "apollyon",
        "source_trajectory_sha256": source_trajectory_sha256,
        "source_round": round_no,
        "seed": seed,
        "mode": "FORCE_CONVERSION",
        "tool": "move_units",
        "unit_selector": "all_combat",
        "target_policy": "normalized_map_fraction",
        "target_x_millis": x_millis,
        "target_y_millis": y_millis,
        "utility_horizon_rounds": len(after_states),
        "utility": utility,
        "authority_labels_included": False,
        "automatic_corpus_admission": False,
        "automatic_weight_mutation": False,
        "automatic_promotion": False,
    }


def extract_utility_policy_records(
    trajectory_path: Path,
    *,
    expected_trajectory_sha256: str,
    horizon_rounds: int = UTILITY_HORIZON_ROUNDS,
) -> list[dict[str, Any]]:
    _require(1 <= horizon_rounds <= 6, "utility horizon must be 1..6 rounds")
    path = trajectory_path.expanduser().resolve()
    raw = _read(path, "trajectory", MAX_TRAJECTORY_BYTES)
    actual = hashlib.sha256(raw).hexdigest()
    _require(actual == _sha(expected_trajectory_sha256, "expected trajectory SHA-256"), "trajectory SHA-256 mismatch")
    reviewed = validate_conditional_v22_evidence(path, expected_trajectory_sha256=actual)
    _require(reviewed.get("present") is True, "trajectory is not V2.2 evidence")
    _require(reviewed.get("reviewed_identity_verified") is True, "V2.2 identity is not reviewed")
    _require(reviewed.get("all_round_receipts_verified") is True, "V2.2 receipts incomplete")
    _require(reviewed.get("runtime_seed_branching") is False, "runtime seed branching detected")

    rows = _jsonl(raw)
    _require(bool(rows), "trajectory is empty")
    header = rows[0]
    seed = header.get("seed")
    _require(type(seed) is int, "run_header seed invalid")
    pairs = _pairs(rows[1:])
    records: list[dict[str, Any]] = []
    for offset, (decision, _result) in enumerate(pairs):
        horizon = [
            pairs[index][1]
            for index in range(offset, min(len(pairs), offset + horizon_rounds))
        ]
        record = classify_force_conversion_move(
            decision,
            horizon,
            source_trajectory_sha256=actual,
            seed=seed,
            round_no=offset + 1,
        )
        if record is not None:
            records.append(record)
    return records


def build_policy_snapshot(
    trajectories: Sequence[tuple[Path, str]],
) -> dict[str, Any]:
    _require(bool(trajectories), "at least one trajectory is required")
    records: list[dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()
    sources: set[str] = set()
    for path, digest in trajectories:
        for record in extract_utility_policy_records(
            path,
            expected_trajectory_sha256=digest,
        ):
            key = (record["source_trajectory_sha256"], record["source_round"])
            if key in seen:
                continue
            seen.add(key)
            sources.add(record["source_trajectory_sha256"])
            records.append(record)
    records.sort(key=lambda row: (row["source_trajectory_sha256"], row["source_round"]))
    return {
        "schema": POLICY_SNAPSHOT_SCHEMA,
        "general_id": "apollyon",
        "scope": "tactical_competence_only",
        "record_count": len(records),
        "records": records,
        "source_trajectory_sha256": sorted(sources),
        "utility_horizon_rounds": UTILITY_HORIZON_ROUNDS,
        "validity_only_examples_admitted": False,
        "authority_envelope_trainable": False,
        "automatic_corpus_admission": False,
        "automatic_weight_mutation": False,
        "automatic_promotion": False,
    }


def validate_policy_snapshot(snapshot: Mapping[str, Any]) -> None:
    snapshot = _obj(snapshot, "policy snapshot")
    _require(snapshot.get("schema") == POLICY_SNAPSHOT_SCHEMA, "policy snapshot schema drift")
    _require(snapshot.get("general_id") == "apollyon", "policy snapshot general drift")
    _require(snapshot.get("scope") == "tactical_competence_only", "policy snapshot scope drift")
    records = _arr(snapshot.get("records"), "policy snapshot records")
    _require(snapshot.get("record_count") == len(records), "policy snapshot record_count mismatch")
    _require(snapshot.get("validity_only_examples_admitted") is False, "validity-only examples admitted")
    for key in ("authority_envelope_trainable", "automatic_corpus_admission", "automatic_weight_mutation", "automatic_promotion"):
        _require(snapshot.get(key) is False, f"policy snapshot authority drift: {key}")
    for record in records:
        record = _obj(record, "policy record")
        _require(record.get("schema") == POLICY_RECORD_SCHEMA, "policy record schema drift")
        _require(record.get("mode") == "FORCE_CONVERSION", "policy record mode drift")
        _require(record.get("tool") == "move_units", "policy record tool drift")
        _require(record.get("unit_selector") == "all_combat", "policy record selector drift")
        _require(record.get("target_policy") == "normalized_map_fraction", "policy record target policy drift")
        for field in ("target_x_millis", "target_y_millis"):
            _require(type(record.get(field)) is int and 0 <= record[field] <= MILLIS, f"policy record {field} invalid")
        utility = _obj(record.get("utility"), "policy record utility")
        _require(utility.get("utility_positive") is True, "non-positive policy example admitted")
        _require(record.get("authority_labels_included") is False, "authority labels leaked into policy record")


def policy_snapshot_sha256(snapshot: Mapping[str, Any]) -> str:
    validate_policy_snapshot(snapshot)
    return _canonical_sha(snapshot)


def _validate_rejected_parent_pair(pair: Mapping[str, Any], expected_parent_adapter_sha256: str) -> None:
    pair = _obj(pair, "rejected parent pair")
    _require(pair.get("schema") == "void.general-brain-incumbent-challenger-pair.v1", "rejected pair schema drift")
    _require(pair.get("general_id") == "apollyon", "rejected pair general drift")
    _require(pair.get("adapter_sha256") == _sha(expected_parent_adapter_sha256, "parent adapter SHA-256"), "rejected pair adapter binding mismatch")
    comparison = _obj(pair.get("comparison"), "rejected pair comparison")
    _require(
        comparison.get("verdict") == "WORSE"
        or comparison.get("protocol_clean") is not True
        or comparison.get("behavioral_gates_pass") is not True,
        "parent pair does not prove rejection",
    )


def train_policy_adapter_revision_two(
    parent_challenger_manifest: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    *,
    rejected_parent_pair: Mapping[str, Any],
    rejected_parent_pair_sha256: str,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    validate_brain_manifest(parent_challenger_manifest)
    validate_policy_snapshot(snapshot)
    _require(parent_challenger_manifest.get("general_id") == "apollyon", "parent challenger general drift")
    _require(parent_challenger_manifest.get("generation") == 1, "revision-two parent must be Generation 1")
    competence = _obj(parent_challenger_manifest.get("competence_adapter"), "parent competence adapter")
    _require(competence.get("state") == "challenger", "parent Generation 1 is not challenger")
    parent_adapter_sha = _sha(competence.get("artifact_sha256"), "parent adapter SHA-256")
    _validate_rejected_parent_pair(rejected_parent_pair, parent_adapter_sha)
    rejected_sha = _sha(rejected_parent_pair_sha256, "rejected parent pair file SHA-256")

    records = list(snapshot["records"])
    _require(len(records) >= MIN_POLICY_EXAMPLES, f"need at least {MIN_POLICY_EXAMPLES} utility-positive examples")
    x_millis = int(round(statistics.median(record["target_x_millis"] for record in records)))
    y_millis = int(round(statistics.median(record["target_y_millis"] for record in records)))

    adapter = {
        "schema": POLICY_ADAPTER_SCHEMA,
        "general_id": "apollyon",
        "generation": 1,
        "candidate_revision": 2,
        "scope": "tactical_competence_only",
        "algorithm": ALGORITHM_ID,
        "parent_adapter_sha256": parent_adapter_sha,
        "parent_revision_status": "REJECTED",
        "rejected_parent_pair_sha256": rejected_sha,
        "policy_snapshot_sha256": policy_snapshot_sha256(snapshot),
        "utility_positive_record_count": len(records),
        "flat_tool_weight_retained": False,
        "policies": {
            "FORCE_CONVERSION": {
                "tool": "move_units",
                "application": "mode_entry_only",
                "unit_selector": "all_combat",
                "target_policy": "normalized_map_fraction",
                "target_x_millis": x_millis,
                "target_y_millis": y_millis,
                "queued": False,
            }
        },
        "authority_envelope_embedded": False,
        "tool_authorization_embedded": False,
        "promotion_authority_embedded": False,
        "automatic_weight_install": False,
        "automatic_promotion": False,
    }

    receipt = {
        "schema": POLICY_RECEIPT_SCHEMA,
        "general_id": "apollyon",
        "generation": 1,
        "candidate_revision": 2,
        "algorithm": ALGORITHM_ID,
        "parent_manifest_sha256": manifest_sha256(parent_challenger_manifest),
        "parent_adapter_sha256": parent_adapter_sha,
        "rejected_parent_pair_sha256": rejected_sha,
        "policy_snapshot_sha256": policy_snapshot_sha256(snapshot),
        "policy_adapter_sha256": _canonical_sha(adapter),
        "utility_positive_record_count": len(records),
        "authority_envelope_trainable": False,
        "automatic_weight_install": False,
        "automatic_promotion": False,
    }

    revised_manifest = copy.deepcopy(dict(parent_challenger_manifest))
    revised_manifest["candidate_revision"] = 2
    revised_manifest["competence_adapter"] = {
        "trainable": True,
        "scope": "tactical_competence_only",
        "state": "challenger",
        "artifact_sha256": _canonical_sha(adapter),
    }
    revised_manifest["revision_lineage"] = {
        "parent_challenger_manifest_sha256": manifest_sha256(parent_challenger_manifest),
        "parent_adapter_sha256": parent_adapter_sha,
        "rejected_parent_pair_sha256": rejected_sha,
        "policy_snapshot_sha256": policy_snapshot_sha256(snapshot),
        "policy_training_receipt_sha256": _canonical_sha(receipt),
    }
    _require(
        revised_manifest.get("authority_envelope") == parent_challenger_manifest.get("authority_envelope") == NONTRAINABLE_AUTHORITY_ENVELOPE,
        "revision changed authority envelope",
    )
    validate_brain_manifest(revised_manifest)
    return adapter, receipt, revised_manifest


def validate_policy_adapter(adapter: Mapping[str, Any]) -> None:
    adapter = _obj(adapter, "policy adapter")
    _require(adapter.get("schema") == POLICY_ADAPTER_SCHEMA, "policy adapter schema drift")
    _require(adapter.get("general_id") == "apollyon", "policy adapter general drift")
    _require(adapter.get("generation") == 1 and adapter.get("candidate_revision") == 2, "policy adapter revision drift")
    _require(adapter.get("scope") == "tactical_competence_only", "policy adapter scope drift")
    _require(adapter.get("algorithm") == ALGORITHM_ID, "policy adapter algorithm drift")
    _sha(adapter.get("parent_adapter_sha256"), "policy parent adapter SHA-256")
    _sha(adapter.get("rejected_parent_pair_sha256"), "policy rejected pair SHA-256")
    _sha(adapter.get("policy_snapshot_sha256"), "policy snapshot SHA-256")
    _require(adapter.get("parent_revision_status") == "REJECTED", "parent revision was not rejected")
    _require(adapter.get("flat_tool_weight_retained") is False, "rejected flat tool weight retained")
    policies = _obj(adapter.get("policies"), "policy adapter policies")
    policy = _obj(policies.get("FORCE_CONVERSION"), "FORCE_CONVERSION policy")
    _require(policy.get("tool") == "move_units", "policy tool drift")
    _require(policy.get("application") == "mode_entry_only", "policy application drift")
    _require(policy.get("unit_selector") == "all_combat", "policy selector drift")
    _require(policy.get("target_policy") == "normalized_map_fraction", "policy target drift")
    for field in ("target_x_millis", "target_y_millis"):
        _require(type(policy.get(field)) is int and 0 <= policy[field] <= MILLIS, f"policy {field} invalid")
    for key in ("authority_envelope_embedded", "tool_authorization_embedded", "promotion_authority_embedded", "automatic_weight_install", "automatic_promotion"):
        _require(adapter.get(key) is False, f"policy adapter authority drift: {key}")


def policy_adapter_sha256(adapter: Mapping[str, Any]) -> str:
    validate_policy_adapter(adapter)
    return _canonical_sha(adapter)


def policy_training_receipt_sha256(receipt: Mapping[str, Any]) -> str:
    receipt = _obj(receipt, "policy training receipt")
    _require(receipt.get("schema") == POLICY_RECEIPT_SCHEMA, "policy receipt schema drift")
    for key in ("parent_manifest_sha256", "parent_adapter_sha256", "rejected_parent_pair_sha256", "policy_snapshot_sha256", "policy_adapter_sha256"):
        _sha(receipt.get(key), f"policy receipt {key}")
    _require(receipt.get("authority_envelope_trainable") is False, "policy receipt authority drift")
    _require(receipt.get("automatic_weight_install") is False, "policy receipt auto-install drift")
    _require(receipt.get("automatic_promotion") is False, "policy receipt auto-promotion drift")
    return _canonical_sha(receipt)


__all__ = [
    "ALGORITHM_ID",
    "GeneralBrainPolicyError",
    "MIN_POLICY_EXAMPLES",
    "POLICY_ADAPTER_SCHEMA",
    "POLICY_RECORD_SCHEMA",
    "POLICY_SNAPSHOT_SCHEMA",
    "build_policy_snapshot",
    "classify_force_conversion_move",
    "extract_utility_policy_records",
    "policy_adapter_sha256",
    "policy_snapshot_sha256",
    "policy_training_receipt_sha256",
    "train_policy_adapter_revision_two",
    "validate_policy_adapter",
    "validate_policy_snapshot",
]
