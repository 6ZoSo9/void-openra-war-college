"""Exact accepted-comparator gate for G2 runtime frontier integration.

Default mode is OFF.  Source availability alone cannot activate runtime
installation, shadow evaluation, or enforcement.  A later operator/runtime
authorization must set an active mode and provide exact comparator/evidence
material.  Shadow mode never replaces the proposed action.
"""

from __future__ import annotations

import hashlib
import json
import os
import types
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from openra_env.learning.g2_runtime_capability_projection import (
    project_live_game_state,
)
from openra_env.learning.g2_runtime_candidate_frontier import (
    action_identity_sha256,
    build_candidate_frontier,
    canonical_action,
)
from openra_env.learning.g2_runtime_tool_classification import (
    MUTATION_CAPABLE,
    classify_tool,
    validate_discovered_tool_surface,
)

EXPECTED_COMPARATOR_SHA256 = (
    "0ec2a0c6be7ac4bd08cf90379428a9e5a7acc8b85c90a94df739a82f08aa695c"
)
ACCEPTED_CANDIDATE_MANIFEST_INTERNAL_SHA256 = (
    "8a98cab8cc2c2a23e13079c326c5ba3305bba6676ae64ddf85a2a8edd6c94952"
)
PROMOTION_RECEIPT_INTERNAL_SHA256 = (
    "f5f72c494c671f9f51d3d78c5f7269317194e555edec851c5e4e89a4eedfb622"
)
MODE_ENV = "VOID_G2_RUNTIME_FRONTIER_MODE"
COMPARATOR_PATH_ENV = "VOID_G2_RUNTIME_FRONTIER_COMPARATOR_PATH"
EVIDENCE_PATH_ENV = "VOID_G2_RUNTIME_FRONTIER_EVIDENCE_PATH"
MODES = ("off", "shadow", "enforce")
EXPECTED_FEATURES = {
    "restorative_available": (
        "restorative_for_current_deficit",
        "projected_min_capability",
        "deficit_total_effect",
        "projected_total_capability",
    ),
    "fallback_no_restorative": (
        "projected_min_capability",
        "projected_deficient_capability",
        "projected_total_capability",
    ),
}


class G2RuntimeFrontierHold(RuntimeError):
    """Fail-closed active frontier gate error."""


def _load_json(path: Path) -> dict:
    if path.is_symlink() or not path.is_file():
        raise G2RuntimeFrontierHold("evidence_missing_or_symlinked")
    try:
        value = json.loads(path.read_bytes())
    except (OSError, json.JSONDecodeError) as exc:
        raise G2RuntimeFrontierHold("evidence_json") from exc
    if not isinstance(value, dict):
        raise G2RuntimeFrontierHold("evidence_not_object")
    return value


def load_accepted_comparator(path: Path):
    if path.is_symlink() or not path.is_file():
        raise G2RuntimeFrontierHold("comparator_missing_or_symlinked")
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise G2RuntimeFrontierHold("comparator_read") from exc
    actual = hashlib.sha256(raw).hexdigest()
    if actual != EXPECTED_COMPARATOR_SHA256:
        raise G2RuntimeFrontierHold(
            "comparator_sha256:expected="
            + EXPECTED_COMPARATOR_SHA256
            + ":actual="
            + actual
        )

    # Execute exactly the source bytes that passed the SHA-256 check.  Do not
    # hand the path to importlib after hashing: a second path-based load could
    # consume a timestamp-valid cached .pyc or observe path replacement.
    module = types.ModuleType(
        "void_g2_runtime_accepted_compiled_comparator_v1"
    )
    module.__file__ = str(path)
    try:
        code = compile(raw, str(path), "exec", dont_inherit=True)
        exec(code, module.__dict__)
    except Exception as exc:
        raise G2RuntimeFrontierHold(
            "comparator_verified_bytes_execution"
        ) from exc

    if getattr(module, "CANDIDATE_ID", None) != (
        "apollyon-g2-compiled-lexicographic-comparator-v1"
    ):
        raise G2RuntimeFrontierHold("comparator_candidate_id")
    if getattr(module, "COMPARISON", None) != (
        "lexicographic_maximize_left_to_right"
    ):
        raise G2RuntimeFrontierHold("comparator_comparison")
    features = getattr(module, "BRANCH_FEATURES", None)
    if not isinstance(features, dict):
        raise G2RuntimeFrontierHold("comparator_branch_features")
    for branch, expected in EXPECTED_FEATURES.items():
        if tuple(features.get(branch, ())) != expected:
            raise G2RuntimeFrontierHold(
                "comparator_feature_order:" + branch
            )
    return module


def apply_compiled_comparator_gate(
    *,
    projection: object,
    proposed_action: object,
    evidence: object,
    comparator_path: Path,
) -> dict:
    frontier = build_candidate_frontier(
        projection, proposed_action, evidence
    )
    comparator = load_accepted_comparator(comparator_path)
    try:
        adapted = comparator.adapt(
            frontier["branch"],
            frontier["proposed_action_key"],
            frontier["action_to_tuple"],
        )
    except Exception as exc:
        raise G2RuntimeFrontierHold("comparator_execution") from exc

    executed_key = adapted.get("executed_action")
    candidates = frontier["candidate_actions_by_key"]
    if executed_key not in candidates:
        raise G2RuntimeFrontierHold("comparator_selected_unknown_candidate")
    executed = canonical_action(candidates[executed_key])
    proposed = canonical_action(proposed_action)
    overridden = adapted.get("overridden")
    if overridden not in (True, False):
        raise G2RuntimeFrontierHold("comparator_override_flag")
    if adapted.get("world_mutated_before_adapter_validation") is not False:
        raise G2RuntimeFrontierHold("comparator_prevalidation_boundary")

    result = {
        "schema": "void.generals.g2-runtime-compiled-comparator-gate.result.v1",
        "candidate_id": "apollyon-g2-compiled-lexicographic-comparator-v1",
        "accepted_candidate_manifest_internal_sha256": (
            ACCEPTED_CANDIDATE_MANIFEST_INTERNAL_SHA256
        ),
        "promotion_receipt_internal_sha256": PROMOTION_RECEIPT_INTERNAL_SHA256,
        "compiled_comparator_source_sha256": EXPECTED_COMPARATOR_SHA256,
        "branch": frontier["branch"],
        "proposed_action": proposed,
        "proposed_action_identity_sha256": action_identity_sha256(proposed),
        "executed_action": executed,
        "executed_action_identity_sha256": action_identity_sha256(executed),
        "overridden": overridden,
        "override_reason": adapted.get("override_reason"),
        "maximum_policy_tuple": adapted.get("maximum_policy_tuple"),
        "frontier_member_keys": adapted.get("frontier_members"),
        "world_mutated_before_adapter_validation": False,
        "host_prevalidation_required": True,
        "all_candidates_host_prevalidated": True,
        "model_or_provider_called_by_gate": False,
        "comparator_grants_execution_authority": False,
        "runtime_install_authorized_by_source": False,
        "deployment_authorized_by_source": False,
        "training_data_admitted": False,
        "neural_weights_updated": False,
    }
    return result


@dataclass(frozen=True)
class PreparedToolCall:
    tool_name: str
    arguments: object
    record: dict | None


class RuntimeFrontierController:
    """Per-agent in-memory controller; source defaults to mode=off."""

    def __init__(
        self,
        *,
        mode: str,
        discovered_tools: Iterable[object],
        comparator_path: Path | None = None,
        evidence_path: Path | None = None,
    ):
        if mode not in MODES:
            raise G2RuntimeFrontierHold("invalid_mode:" + str(mode))
        self.mode = mode
        self.comparator_path = comparator_path
        self.evidence_path = evidence_path
        tools = tuple(discovered_tools)
        self.discovered_tool_names = tuple(
            getattr(t, "name", t.get("name") if isinstance(t, dict) else t)
            for t in tools
        )
        self.discovery_hold: str | None = None
        if mode != "off":
            try:
                validate_discovered_tool_surface(tools)
            except Exception as exc:
                if mode == "enforce":
                    raise G2RuntimeFrontierHold(str(exc)) from exc
                self.discovery_hold = str(exc)

    @classmethod
    def from_environment(cls, discovered_tools: Iterable[object]):
        mode = os.environ.get(MODE_ENV, "off").strip().lower() or "off"
        comparator = os.environ.get(COMPARATOR_PATH_ENV, "").strip()
        evidence = os.environ.get(EVIDENCE_PATH_ENV, "").strip()
        return cls(
            mode=mode,
            discovered_tools=discovered_tools,
            comparator_path=Path(comparator) if comparator else None,
            evidence_path=Path(evidence) if evidence else None,
        )

    async def prepare_call(
        self, env, tool_name: str, arguments: object
    ) -> PreparedToolCall:
        # OFF is deliberately behavior-transparent: do not canonicalize, inspect
        # state, classify, or otherwise reshape the pre-existing tool call.
        if self.mode == "off":
            return PreparedToolCall(
                tool_name=tool_name,
                arguments=arguments,
                record=None,
            )

        proposed = canonical_action(
            {"tool": tool_name, "arguments": arguments}
        )
        try:
            classification = classify_tool(proposed["tool"])
        except Exception as exc:
            if self.mode == "enforce":
                raise G2RuntimeFrontierHold(str(exc)) from exc
            return PreparedToolCall(
                tool_name=proposed["tool"],
                arguments=proposed["arguments"],
                record={
                    "schema": "void.generals.g2-runtime-frontier-call.v1",
                    "mode": "shadow",
                    "classification": "unclassified",
                    "proposed_action": proposed,
                    "would_execute_action": None,
                    "actual_action": proposed,
                    "gated": True,
                    "gate_hold": str(exc),
                    "shadow_does_not_replace_or_block": True,
                    "world_mutated_before_adapter_validation": False,
                },
            )
        if classification != MUTATION_CAPABLE:
            return PreparedToolCall(
                tool_name=proposed["tool"],
                arguments=proposed["arguments"],
                record={
                    "schema": "void.generals.g2-runtime-frontier-call.v1",
                    "mode": self.mode,
                    "classification": classification,
                    "proposed_action": proposed,
                    "would_execute_action": proposed,
                    "actual_action": proposed,
                    "gated": False,
                    "observation_or_control_passthrough": True,
                    "world_mutated_before_adapter_validation": False,
                },
            )

        # Fresh observation before every mutation-capable tool call, including
        # later calls in the same assistant response.
        state = await env.call_tool("get_game_state")
        projection = project_live_game_state(state)

        try:
            if self.discovery_hold is not None:
                raise G2RuntimeFrontierHold(
                    "runtime_tool_surface:" + self.discovery_hold
                )
            if self.comparator_path is None:
                raise G2RuntimeFrontierHold("comparator_path_not_configured")
            if self.evidence_path is None:
                raise G2RuntimeFrontierHold("evidence_path_not_configured")
            evidence = _load_json(self.evidence_path)
            gate = apply_compiled_comparator_gate(
                projection=projection,
                proposed_action=proposed,
                evidence=evidence,
                comparator_path=self.comparator_path,
            )
        except Exception as exc:
            if isinstance(exc, G2RuntimeFrontierHold):
                hold = exc
            else:
                hold = G2RuntimeFrontierHold(
                    type(exc).__name__ + ":" + str(exc)
                )
            if self.mode == "enforce":
                raise hold
            # Shadow mode is observational only and cannot replace/block actions.
            return PreparedToolCall(
                tool_name=proposed["tool"],
                arguments=proposed["arguments"],
                record={
                    "schema": "void.generals.g2-runtime-frontier-call.v1",
                    "mode": "shadow",
                    "classification": classification,
                    "proposed_action": proposed,
                    "would_execute_action": None,
                    "actual_action": proposed,
                    "gated": True,
                    "gate_hold": str(hold),
                    "shadow_does_not_replace_or_block": True,
                    "world_mutated_before_adapter_validation": False,
                },
            )

        would_execute = gate["executed_action"]
        actual = proposed if self.mode == "shadow" else would_execute
        return PreparedToolCall(
            tool_name=actual["tool"],
            arguments=actual["arguments"],
            record={
                "schema": "void.generals.g2-runtime-frontier-call.v1",
                "mode": self.mode,
                "classification": classification,
                "proposed_action": proposed,
                "would_execute_action": would_execute,
                "actual_action": actual,
                "gated": True,
                "gate": gate,
                "shadow_does_not_replace_or_block": self.mode == "shadow",
                "world_mutated_before_adapter_validation": False,
            },
        )
