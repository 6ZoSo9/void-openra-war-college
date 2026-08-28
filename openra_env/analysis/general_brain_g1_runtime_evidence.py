from __future__ import annotations

import hashlib
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

from openra_env.learning.general_brain_runtime import BRAIN_ROUND_SCHEMA, BRAIN_RUN_SCHEMA

from ._spar_conditional_v2_2 import validate_conditional_v22_evidence
from ._spar_contract import (
    MAX_TRAJECTORY_BYTES,
    SHA256,
    ContractError,
    _arr,
    _bool,
    _int,
    _jsonl,
    _obj,
    _pattern,
    _read,
    _str,
)

TRAJECTORY_KEY = "general_brain_generation_1"


def _text_array(value: Any, label: str) -> list[str]:
    rows = _arr(value, label)
    return [_str(item, f"{label}[{index}]") for index, item in enumerate(rows)]


def _run_binding(header: Mapping[str, Any]) -> dict[str, Any] | None:
    raw = header.get(TRAJECTORY_KEY)
    if raw is None:
        return None
    raw = _obj(raw, f"run_header.{TRAJECTORY_KEY}")
    if _str(raw.get("schema"), "General Brain run schema") != BRAIN_RUN_SCHEMA:
        raise ContractError("General Brain run schema mismatch")
    if _str(raw.get("general_id"), "General Brain general_id") != "apollyon":
        raise ContractError("General Brain runtime must belong to Apollyon")
    if _int(raw.get("generation"), "General Brain generation") != 1:
        raise ContractError("General Brain runtime generation must be 1")
    _bool(raw.get("challenger_only"), "General Brain challenger_only", True)
    adapter_sha = _pattern(raw.get("adapter_sha256"), "General Brain adapter SHA", SHA256)
    adapter_file_sha = _pattern(raw.get("adapter_file_sha256"), "General Brain adapter file SHA", SHA256)
    manifest_sha = _pattern(
        raw.get("challenger_manifest_sha256"),
        "General Brain challenger manifest semantic SHA",
        SHA256,
    )
    manifest_file_sha = _pattern(
        raw.get("challenger_manifest_file_sha256"),
        "General Brain challenger manifest file SHA",
        SHA256,
    )
    if adapter_sha != adapter_file_sha:
        raise ContractError("General Brain adapter semantic/file SHA mismatch")
    # Brain manifests intentionally use a semantic-object SHA while the JSON
    # artifact has its own byte/file SHA. Both are independently bound and
    # therefore MUST NOT be required to equal one another.
    for key in (
        "authority_envelope_trainable",
        "sovereign_directives_trainable",
        "tool_authorization_trainable",
        "automatic_weight_install",
        "automatic_promotion",
    ):
        _bool(raw.get(key), f"General Brain {key}", False)
    _bool(raw.get("review_required"), "General Brain review_required", True)
    return {
        "schema": BRAIN_RUN_SCHEMA,
        "general_id": "apollyon",
        "generation": 1,
        "challenger_only": True,
        "adapter_sha256": adapter_sha,
        "adapter_file_sha256": adapter_file_sha,
        "challenger_manifest_sha256": manifest_sha,
        "challenger_manifest_file_sha256": manifest_file_sha,
        "authority_envelope_trainable": False,
        "sovereign_directives_trainable": False,
        "tool_authorization_trainable": False,
        "automatic_weight_install": False,
        "automatic_promotion": False,
        "review_required": True,
    }


def validate_general_brain_g1_evidence(
    trajectory_path: Path,
    *,
    expected_trajectory_sha256: str,
) -> dict[str, Any]:
    if SHA256.fullmatch(expected_trajectory_sha256) is None:
        raise ContractError("expected trajectory SHA-256 malformed for General Brain validation")
    raw = _read(trajectory_path, "trajectory", MAX_TRAJECTORY_BYTES)
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected_trajectory_sha256:
        raise ContractError("trajectory changed before General Brain validation")
    rows = _jsonl(raw)
    if not rows:
        raise ContractError("trajectory is empty during General Brain validation")

    reviewed_v22 = validate_conditional_v22_evidence(
        trajectory_path,
        expected_trajectory_sha256=actual,
    )
    run = _run_binding(rows[0])
    if run is None:
        return {"present": False, "rounds_verified": 0}
    if reviewed_v22.get("present") is not True or reviewed_v22.get("reviewed_identity_verified") is not True:
        raise ContractError("General Brain challenger is not layered over reviewed V2.2")

    rounds = 0
    preference_applied = 0
    preferred_selected = 0
    preferred_move_units = 0
    mode_counts: Counter[str] = Counter()
    for row in rows[1:]:
        if row.get("event") != "joint_decision":
            continue
        rounds += 1
        raw_brain = _obj(row.get(TRAJECTORY_KEY), f"round {rounds} General Brain evidence")
        if _str(raw_brain.get("schema"), "General Brain round schema") != BRAIN_ROUND_SCHEMA:
            raise ContractError("General Brain round schema mismatch")
        if _str(raw_brain.get("general_id"), "General Brain round general_id") != "apollyon":
            raise ContractError("General Brain round general_id mismatch")
        if _int(raw_brain.get("generation"), "General Brain round generation") != 1:
            raise ContractError("General Brain round generation mismatch")
        if _pattern(raw_brain.get("adapter_sha256"), "General Brain round adapter SHA", SHA256) != run["adapter_sha256"]:
            raise ContractError("General Brain round adapter binding mismatch")
        if _pattern(raw_brain.get("challenger_manifest_sha256"), "General Brain round manifest SHA", SHA256) != run["challenger_manifest_sha256"]:
            raise ContractError("General Brain round manifest binding mismatch")

        v22_evidence = _obj(row.get("conditional_engagement_v2_2"), f"round {rounds} V2.2 evidence")
        prepared = _obj(v22_evidence.get("prepared"), f"round {rounds} V2.2 prepared")
        decision = _obj(prepared.get("decision"), f"round {rounds} V2.2 decision")
        mode = _str(raw_brain.get("mode"), "General Brain mode")
        if mode != _str(decision.get("mode"), "V2.2 mode"):
            raise ContractError("General Brain tactical mode does not match reviewed V2.2 mode")
        mode_counts[mode] += 1

        offered = _text_array(raw_brain.get("offered_tool_names"), "General Brain offered_tool_names")
        prepared_offered = _text_array(prepared.get("current_allowed_tool_names"), "V2.2 prepared tool names")
        if offered != prepared_offered:
            raise ContractError("General Brain observed tool surface differs from reviewed V2.2 surface")
        _bool(raw_brain.get("tool_surface_unchanged"), "General Brain tool_surface_unchanged", True)

        weights = _obj(raw_brain.get("offered_weights"), "General Brain offered_weights")
        for tool, score in weights.items():
            if not isinstance(tool, str) or tool not in offered or type(score) not in (int, float):
                raise ContractError("General Brain offered weight is malformed")

        preferred = raw_brain.get("preferred_tool")
        score = raw_brain.get("preferred_score")
        applied = _bool(raw_brain.get("preference_applied"), "General Brain preference_applied")
        if preferred is None:
            if score is not None or applied:
                raise ContractError("General Brain preference absent but marked applied")
        else:
            preferred = _str(preferred, "General Brain preferred_tool")
            if preferred not in offered or type(score) not in (int, float) or float(score) <= 0 or not applied:
                raise ContractError("General Brain preferred tool binding malformed")
            preference_applied += 1

        arguments = _obj(raw_brain.get("preferred_arguments"), "General Brain preferred_arguments")
        if mode == "FORCE_CONVERSION" and preferred == "move_units":
            if arguments != {"unit_ids": "all_combat"}:
                raise ContractError("General Brain learned move_units selector drift")
            preferred_move_units += 1
        elif arguments:
            raise ContractError("General Brain preferred arguments present without reviewed selector case")

        apollyon = _obj(row.get("apollyon"), "Apollyon decision")
        selected = _str(raw_brain.get("selected_tool"), "General Brain selected_tool")
        if selected != _str(apollyon.get("tool"), "Apollyon tool"):
            raise ContractError("General Brain selected tool does not match trajectory")
        selected_preferred = _bool(
            raw_brain.get("selected_preferred_tool"),
            "General Brain selected_preferred_tool",
        )
        if selected_preferred != (preferred is not None and selected == preferred):
            raise ContractError("General Brain preferred-selection receipt mismatch")
        if selected_preferred:
            preferred_selected += 1
        _bool(raw_brain.get("v2_2_parallel_session_committed"), "General Brain parallel session", True)
        for key in (
            "authority_envelope_trainable",
            "tool_authorization_trainable",
            "automatic_weight_install",
            "automatic_promotion",
        ):
            _bool(raw_brain.get(key), f"General Brain round {key}", False)

    if rounds == 0:
        raise ContractError("General Brain run has no joint_decision rows")
    if rounds != reviewed_v22.get("rounds_verified"):
        raise ContractError("General Brain/V2.2 verified round count mismatch")

    return {
        "present": True,
        **run,
        "rounds_verified": rounds,
        "mode_counts": dict(sorted(mode_counts.items())),
        "preference_applied_rounds": preference_applied,
        "preferred_tool_selected_rounds": preferred_selected,
        "preferred_move_units_rounds": preferred_move_units,
        "preference_follow_fraction": (
            preferred_selected / preference_applied if preference_applied else 1.0
        ),
        "all_round_receipts_verified": True,
        "reviewed_v2_2_identity_verified": True,
    }


__all__ = ["TRAJECTORY_KEY", "validate_general_brain_g1_evidence"]
