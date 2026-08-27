"""Runtime-neutral session adapter for Conditional Engagement Candidate V2.1."""
from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from typing import Any

from .conditional_engagement_v2_1 import (
    PolicyError,
    candidate_sha256,
    canonical_json_bytes,
    format_coaching,
    select_mode,
    snapshot_from_state,
    validate_candidate,
)

PREPARED_SCHEMA = "void.apollyon.conditional-engagement-prepared-round.v2.1"
COMMIT_SCHEMA = "void.apollyon.conditional-engagement-accepted-round.v2.1"


class SessionError(PolicyError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SessionError(message)


def _allowed_tool_names(value: Sequence[str]) -> tuple[str, ...]:
    _require(isinstance(value, Sequence) and not isinstance(value, (str, bytes)), "allowed_tool_names must be a sequence")
    names = tuple(value)
    _require(bool(names), "allowed_tool_names must not be empty")
    _require(all(isinstance(name, str) and name for name in names), "allowed_tool_names must contain nonempty text")
    _require(len(names) == len(set(names)), "allowed_tool_names contains duplicates")
    return names


def _copy(value: Any) -> Any:
    return json.loads(json.dumps(value, sort_keys=True, separators=(",", ":")))


class ConditionalEngagementSessionV21:
    def __init__(self, candidate: Mapping[str, Any]):
        validate_candidate(candidate)
        self._candidate = json.loads(canonical_json_bytes(candidate).decode("utf-8"))
        validate_candidate(self._candidate)
        self._candidate_sha256 = candidate_sha256(self._candidate)
        self._history: list[dict[str, Any]] = []
        self._pending: dict[str, Any] | None = None

    @property
    def candidate_sha256(self) -> str:
        return self._candidate_sha256

    @property
    def history(self) -> list[dict[str, Any]]:
        return _copy(self._history)

    @property
    def pending_round(self) -> int | None:
        return None if self._pending is None else int(self._pending["round"])

    def prepare_round(self, state: Mapping[str, Any], *, round_no: int, allowed_tool_names: Sequence[str]) -> dict[str, Any]:
        _require(self._pending is None, "previous prepared round is still pending")
        _require(type(round_no) is int and round_no >= 1, "round_no must be integer >= 1")
        names = _allowed_tool_names(allowed_tool_names)
        expected = 1 if not self._history else self._history[-1]["round"] + 1
        _require(round_no == expected, f"expected round {expected}, got {round_no}")
        current = snapshot_from_state(state, round_no=round_no)
        decision = select_mode(self._candidate, current, self._history)
        self._pending = {
            "round": round_no,
            "snapshot": current,
            "allowed_tool_names": names,
            "mode": decision["mode"],
            "reasons": list(decision["reasons"]),
        }
        return {
            "schema": PREPARED_SCHEMA,
            "round": round_no,
            "candidate_sha256": self._candidate_sha256,
            "current_allowed_tool_names": list(names),
            "decision": _copy(decision),
            "coaching": format_coaching(decision),
            "history_committed": False,
        }

    def commit_accepted_tool(self, selected_tool: str) -> dict[str, Any]:
        _require(self._pending is not None, "no prepared round to commit")
        _require(isinstance(selected_tool, str) and selected_tool, "selected_tool must be nonempty text")
        _require(selected_tool in set(self._pending["allowed_tool_names"]), "selected_tool was not offered for this round")
        snapshot = dict(self._pending["snapshot"])
        snapshot["selected_tool"] = selected_tool
        self._history.append(snapshot)
        window = int(self._candidate["thresholds"]["history_window_rounds"])
        if len(self._history) > window:
            self._history = self._history[-window:]
        receipt = {
            "schema": COMMIT_SCHEMA,
            "round": self._pending["round"],
            "candidate_sha256": self._candidate_sha256,
            "mode": self._pending["mode"],
            "reasons": list(self._pending["reasons"]),
            "selected_tool": selected_tool,
            "function_was_offered": True,
            "history_size": len(self._history),
        }
        self._pending = None
        return receipt