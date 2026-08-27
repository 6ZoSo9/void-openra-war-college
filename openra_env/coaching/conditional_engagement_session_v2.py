"""Runtime-neutral session adapter for Conditional Engagement Candidate V2.

This module intentionally owns no game, model, Ollama, OpenRA, or mutation
capability. It turns already-observed duel state into candidate coaching and
records only a host-accepted tool after the caller proves that tool was offered
for the exact round.
"""
from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from typing import Any

from .conditional_engagement_v2 import (
    PolicyError,
    candidate_sha256,
    canonical_json_bytes,
    format_coaching,
    select_mode,
    snapshot_from_state,
    validate_candidate,
)

PREPARED_SCHEMA = "void.apollyon.conditional-engagement-prepared-round.v2"
COMMIT_SCHEMA = "void.apollyon.conditional-engagement-accepted-round.v2"


class SessionError(PolicyError):
    """Raised when session sequencing or offered-tool evidence is invalid."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SessionError(message)


def _round_number(value: Any) -> int:
    _require(type(value) is int and value >= 1, "round_no must be integer >= 1")
    return value


def _allowed_tool_names(value: Sequence[str]) -> tuple[str, ...]:
    _require(
        isinstance(value, Sequence) and not isinstance(value, (str, bytes)),
        "allowed_tool_names must be a sequence",
    )
    names = tuple(value)
    _require(bool(names), "allowed_tool_names must not be empty")
    _require(
        all(isinstance(name, str) and bool(name) for name in names),
        "allowed_tool_names must contain nonempty text",
    )
    _require(len(names) == len(set(names)), "allowed_tool_names contains duplicates")
    return names


def _json_copy(value: Any) -> Any:
    return json.loads(json.dumps(value, sort_keys=True, separators=(",", ":")))


class ConditionalEngagementSessionV2:
    """Bind one immutable candidate to one sequential duel-side coaching session."""

    def __init__(self, candidate: Mapping[str, Any]):
        validate_candidate(candidate)
        # Freeze the candidate through its canonical JSON representation so an
        # external mutable dict cannot change policy after session creation.
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
        return _json_copy(self._history)

    @property
    def pending_round(self) -> int | None:
        if self._pending is None:
            return None
        return int(self._pending["round"])

    def prepare_round(
        self,
        state: Mapping[str, Any],
        *,
        round_no: int,
        allowed_tool_names: Sequence[str],
    ) -> dict[str, Any]:
        """Derive coaching from observed pre-decision state without committing history."""
        _require(self._pending is None, "previous prepared round is still pending")
        round_no = _round_number(round_no)
        names = _allowed_tool_names(allowed_tool_names)

        expected = 1 if not self._history else self._history[-1]["round"] + 1
        _require(round_no == expected, f"expected round {expected}, got {round_no}")

        current = snapshot_from_state(state, round_no=round_no, selected_tool=None)
        decision = select_mode(self._candidate, current, self._history)
        coaching = format_coaching(decision)

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
            "decision": _json_copy(decision),
            "coaching": coaching,
            "history_committed": False,
        }

    def commit_accepted_tool(self, selected_tool: str) -> dict[str, Any]:
        """Commit only the final host-accepted tool from the currently prepared round."""
        _require(self._pending is not None, "no prepared round to commit")
        _require(
            isinstance(selected_tool, str) and bool(selected_tool),
            "selected_tool must be nonempty text",
        )
        allowed = set(self._pending["allowed_tool_names"])
        _require(selected_tool in allowed, "selected_tool was not offered for this round")

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
