"""Concrete-candidate and semantic-frontier construction for G2 runtime use.

Candidate evidence must be bound to the exact visible-state projection and must
carry a positive, non-mutating host-prevalidation receipt before it can enter
the comparator frontier.  Tool schemas alone never satisfy this contract.
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any

from openra_env.learning.g2_runtime_capability_projection import (
    CAPABILITIES,
    canonical_json_bytes,
    verify_projection,
)

SCHEMA = "void.generals.g2-runtime-candidate-frontier.v1"
EVIDENCE_SCHEMA = "void.generals.g2-runtime-frontier-evidence.v1"
MAX_CANDIDATES = 128
MAX_ABS_EFFECT = 1000


class CandidateFrontierHold(RuntimeError):
    """Fail-closed concrete frontier construction error."""


def canonical_action(action: object) -> dict:
    if not isinstance(action, dict):
        raise CandidateFrontierHold("action_not_object")
    if set(action) != {"tool", "arguments"}:
        raise CandidateFrontierHold("action_shape")
    tool = action.get("tool")
    arguments = action.get("arguments")
    if not isinstance(tool, str) or not tool:
        raise CandidateFrontierHold("action_tool")
    if not isinstance(arguments, dict):
        raise CandidateFrontierHold("action_arguments")
    try:
        raw = canonical_json_bytes({"tool": tool, "arguments": arguments})
        normalized = json.loads(raw)
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise CandidateFrontierHold("action_not_canonical_json") from exc
    return normalized


def canonical_action_key(action: object) -> str:
    return canonical_json_bytes(canonical_action(action)).decode("utf-8")


def action_identity_sha256(action: object) -> str:
    return hashlib.sha256(
        canonical_json_bytes(canonical_action(action))
    ).hexdigest()


def _verify_internal_object(value: object, name: str) -> dict:
    if not isinstance(value, dict):
        raise CandidateFrontierHold(name + "_not_object")
    copy = dict(value)
    supplied = copy.pop("sha256", None)
    actual = hashlib.sha256(canonical_json_bytes(copy)).hexdigest()
    if supplied != actual:
        raise CandidateFrontierHold(name + "_internal_hash")
    return value


def _delta(value: object, name: str) -> dict[str, float]:
    if not isinstance(value, dict) or set(value) != set(CAPABILITIES):
        raise CandidateFrontierHold(name + "_shape")
    out: dict[str, float] = {}
    for capability in CAPABILITIES:
        raw = value[capability]
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            raise CandidateFrontierHold(name + "_non_numeric:" + capability)
        number = float(raw)
        if not math.isfinite(number) or abs(number) > MAX_ABS_EFFECT:
            raise CandidateFrontierHold(name + "_out_of_range:" + capability)
        out[capability] = number
    return out


def _candidate_row(
    projection: dict, row: object
) -> tuple[str, dict, dict[str, float]] | None:
    if not isinstance(row, dict):
        raise CandidateFrontierHold("candidate_not_object")
    action = canonical_action(row.get("action"))
    action_id = action_identity_sha256(action)

    host = row.get("host_prevalidation")
    if not isinstance(host, dict):
        raise CandidateFrontierHold("host_prevalidation_missing:" + action_id)
    if host.get("state_projection_sha256") != projection["sha256"]:
        raise CandidateFrontierHold("host_prevalidation_state:" + action_id)
    if host.get("action_identity_sha256") != action_id:
        raise CandidateFrontierHold("host_prevalidation_action:" + action_id)
    if host.get("world_mutated_before_validation") is not False:
        raise CandidateFrontierHold("host_prevalidation_mutation:" + action_id)
    if host.get("execution_authority") is not False:
        raise CandidateFrontierHold("host_prevalidation_authority:" + action_id)

    # Invalid host candidates are excluded, never passed to the comparator.
    if host.get("valid") is not True:
        return None

    effect = row.get("effect_evidence")
    if not isinstance(effect, dict):
        raise CandidateFrontierHold("effect_evidence_missing:" + action_id)
    if effect.get("supported") is not True:
        return None
    support = effect.get("support")
    if isinstance(support, bool) or not isinstance(support, int) or support < 1:
        raise CandidateFrontierHold("effect_support:" + action_id)
    immediate = _delta(
        effect.get("immediate_mean_delta"), "immediate_mean_delta"
    )
    delayed = _delta(
        effect.get("delayed_next_round_mean_delta"),
        "delayed_next_round_mean_delta",
    )
    total = {
        name: immediate[name] + delayed[name] for name in CAPABILITIES
    }
    return canonical_action_key(action), action, total


def _policy_tuple(
    branch: str,
    current: dict[str, int],
    deficient: str,
    total_effect: dict[str, float],
) -> list[float | int]:
    projected = {
        name: current[name] + total_effect[name] for name in CAPABILITIES
    }
    deficit_effect = total_effect[deficient]
    if branch == "restorative_available":
        return [
            1 if deficit_effect > 0 else 0,
            min(projected.values()),
            deficit_effect,
            sum(projected.values()),
        ]
    if branch == "fallback_no_restorative":
        return [
            min(projected.values()),
            projected[deficient],
            sum(projected.values()),
        ]
    raise CandidateFrontierHold("unknown_branch:" + branch)


def build_candidate_frontier(
    projection: object,
    proposed_action: object,
    evidence: object,
) -> dict:
    projection = verify_projection(projection)
    proposed = canonical_action(proposed_action)
    evidence = _verify_internal_object(evidence, "evidence")
    if evidence.get("schema") != EVIDENCE_SCHEMA:
        raise CandidateFrontierHold("evidence_schema")
    if evidence.get("state_projection_sha256") != projection["sha256"]:
        raise CandidateFrontierHold("evidence_state_projection")
    if evidence.get("projection_spec_sha256") != projection[
        "projection_spec_sha256"
    ]:
        raise CandidateFrontierHold("evidence_projection_spec")
    if evidence.get("tool_schema_is_concrete_candidate_action") is not False:
        raise CandidateFrontierHold("schema_candidate_boundary")

    candidates = evidence.get("candidates")
    if not isinstance(candidates, list):
        raise CandidateFrontierHold("candidate_list")
    if not candidates or len(candidates) > MAX_CANDIDATES:
        raise CandidateFrontierHold("candidate_count")

    action_by_key: dict[str, dict] = {}
    effect_by_key: dict[str, dict[str, float]] = {}
    for row in candidates:
        parsed = _candidate_row(projection, row)
        if parsed is None:
            continue
        key, action, total_effect = parsed
        if key in action_by_key:
            raise CandidateFrontierHold("duplicate_candidate:" + key)
        action_by_key[key] = action
        effect_by_key[key] = total_effect

    if not action_by_key:
        raise CandidateFrontierHold("no_host_prevalidated_supported_candidates")

    current = projection["capabilities"]
    deficient = projection["deficient_capability"]
    restorative = [
        key for key in action_by_key
        if effect_by_key[key][deficient] > 0
    ]
    branch = (
        "restorative_available"
        if restorative
        else "fallback_no_restorative"
    )
    policy_keys = restorative or list(action_by_key)
    action_to_tuple = {
        key: _policy_tuple(
            branch, current, deficient, effect_by_key[key]
        )
        for key in policy_keys
    }
    result = {
        "schema": SCHEMA,
        "branch": branch,
        "deficient_capability": deficient,
        "proposed_action": proposed,
        "proposed_action_key": canonical_action_key(proposed),
        "proposed_action_identity_sha256": action_identity_sha256(proposed),
        "candidate_actions_by_key": {
            key: action_by_key[key] for key in sorted(action_to_tuple)
        },
        "action_to_tuple": {
            key: action_to_tuple[key] for key in sorted(action_to_tuple)
        },
        "all_candidates_host_prevalidated": True,
        "world_mutated_before_validation": False,
        "tool_schema_is_concrete_candidate_action": False,
        "model_or_provider_called": False,
        "execution_authority": False,
    }
    result["sha256"] = hashlib.sha256(canonical_json_bytes(result)).hexdigest()
    return result
