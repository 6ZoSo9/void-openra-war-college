#!/usr/bin/env python3
"""Destination-safe runtime guard for the reviewed General Brain G1 challenger."""
from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from typing import Any

from tools import conditional_engagement_v2_2_g1_duel_wrapper as g1


def _required_argument_names(tools: Any, tool_name: str | None) -> list[str]:
    """Read required argument names from the exact current host tool schema."""
    if not tool_name or not isinstance(tools, Sequence) or isinstance(tools, (str, bytes)):
        return []
    for raw in tools:
        if not isinstance(raw, Mapping):
            continue
        function = raw.get("function") if isinstance(raw.get("function"), Mapping) else raw
        if not isinstance(function, Mapping) or function.get("name") != tool_name:
            continue
        parameters = function.get("parameters")
        if not isinstance(parameters, Mapping):
            continue
        required = parameters.get("required", [])
        if not isinstance(required, Sequence) or isinstance(required, (str, bytes)):
            return []
        names = [value for value in required if isinstance(value, str) and value]
        return names if len(names) == len(required) and len(names) == len(set(names)) else []
    return []


def _destination_guard_text(preferred_tool: str | None, required: Sequence[str]) -> str:
    if preferred_tool != "move_units":
        return ""
    required_text = ",".join(required) if required else "host_schema_required_fields"
    return "\n".join(
        (
            f"LEARNED_TOOL_REQUIRED_ARGUMENTS={required_text}",
            "LEARNED_MOVE_UNITS_ARGUMENT_POLICY=Use unit_ids=\"all_combat\" and supply every other required move_units argument from the exact current tool schema and current observation.",
            "LEARNED_MOVE_UNITS_DESTINATION_POLICY=Any destination/target coordinates must be explicitly grounded in the current observation and must be in bounds; never omit them and never use -1, sentinel, remembered, or invented coordinates.",
            "LEARNED_PREFERENCE_BACKOFF=If you cannot ground every required move_units argument to a valid in-bounds current-observation value, do not choose move_units this turn; choose another currently offered host-authorized tool.",
        )
    )


class DestinationGuardHooks(g1.GeneralBrainOverlayHooks):
    """Apply learned preference only with exact current-schema argument guidance."""

    def _wrapped_decision(self, base, helper, state, pending, pb2, doctrine, round_no):
        _, contract = self.legacy.apollyon_tools_typed(base, state, pending)
        offered_names = list(contract["offered_tool_names"])
        prepared = self.session.prepare_round(
            state,
            round_no=round_no,
            allowed_tool_names=offered_names,
        )
        mode = prepared["decision"]["mode"]
        overlay = g1.tactical_overlay(
            self.binding,
            mode=mode,
            offered_tool_names=offered_names,
        )

        original_tool_call = helper.ollama_tool_call
        schema_required: list[str] = []
        if overlay["prompt_injected"]:
            g1._require(bool(overlay["coaching"]), "applied General Brain preference has empty coaching")

            def brain_tool_call(system, user, tools):
                nonlocal schema_required
                schema_required = _required_argument_names(tools, overlay["preferred_tool"])
                guard = _destination_guard_text(overlay["preferred_tool"], schema_required)
                coaching = overlay["coaching"] + (("\n" + guard) if guard else "")
                return original_tool_call(system, user + "\n" + coaching, tools)

            helper.ollama_tool_call = brain_tool_call
            try:
                result = self._original_decision(
                    base, helper, state, pending, pb2, doctrine, round_no
                )
            finally:
                helper.ollama_tool_call = original_tool_call
        else:
            g1._require(
                overlay["preference_applied"] is False and overlay["coaching"] == "",
                "silent General Brain round unexpectedly carries prompt coaching",
            )
            result = self._original_decision(
                base, helper, state, pending, pb2, doctrine, round_no
            )

        name, args, commands, attempts, accepted_contract = result
        actual_names = list(accepted_contract["offered_tool_names"])
        g1._require(
            actual_names == offered_names,
            "General Brain observation changed the host tool surface",
        )
        accepted = self.session.commit_accepted_tool(name)
        g1._require(
            accepted["mode"] == mode,
            "General Brain parallel V2.2 session mode drift",
        )
        self._round_evidence[int(round_no)] = {
            **{key: value for key, value in overlay.items() if key != "coaching"},
            "tool_schema_required_arguments": schema_required,
            "destination_guard_active": overlay["preferred_tool"] == "move_units",
            "selected_tool": name,
            "selected_preferred_tool": (
                overlay["preferred_tool"] is not None
                and name == overlay["preferred_tool"]
            ),
            "selected_arguments": dict(args) if isinstance(args, Mapping) else {},
            "v2_2_parallel_session_committed": True,
        }
        return name, args, commands, attempts, accepted_contract


def main(argv: Sequence[str] | None = None) -> int:
    old = g1.GeneralBrainOverlayHooks
    g1.GeneralBrainOverlayHooks = DestinationGuardHooks
    try:
        print("general_brain_destination_guard=true")
        print("general_brain_destination_sentinel_forbidden=true")
        print("general_brain_destination_backoff=true")
        return g1.main(list(sys.argv[1:] if argv is None else argv))
    finally:
        g1.GeneralBrainOverlayHooks = old


if __name__ == "__main__":
    raise SystemExit(main())
