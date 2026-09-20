"""Game-neutral observation of goals and expected effects; no execution authority.

This module does not infer a goal from an action name. Clocks, units, intent,
and effect windows must be supplied explicitly by a game adapter/planner.
An observed goal outcome is NOT proof that the last action caused the outcome.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from typing import Any


class ContractError(ValueError):
    """Missing, inconsistent, or out-of-order evidence."""


def text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 240:
        raise ContractError(f"invalid_text:{label}")
    return value


def number(value: Any, label: str, minimum: float | None = None) -> float:
    if type(value) not in (int, float):
        raise ContractError(f"invalid_finite_number:{label}")
    try:
        converted = float(value)
    except (OverflowError, ValueError):
        raise ContractError(f"invalid_finite_number:{label}") from None
    if not math.isfinite(converted):
        raise ContractError(f"invalid_finite_number:{label}")
    if minimum is not None and converted < minimum:
        raise ContractError(f"number_below_minimum:{label}")
    return converted


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False).encode()).hexdigest()


@dataclass(frozen=True)
class Scope:
    run_id: str
    general_id: str
    world_revision: str
    clock_unit: str

    def __post_init__(self):
        for key, value in asdict(self).items():
            text(value, key)
        if self.general_id not in ("apollyon", "abaddon"):
            raise ContractError("unknown_general")


@dataclass(frozen=True)
class Goal:
    goal_id: str
    metric: str
    unit: str
    mode: str  # achieve or maintain
    relation: str  # at_least or at_most
    target: float
    tolerance: float = 0.0
    intent_source: str = "explicit_operator_or_planner"

    def __post_init__(self):
        for key in ("goal_id", "metric", "unit"):
            text(getattr(self, key), key)
        if self.mode not in ("achieve", "maintain"):
            raise ContractError("unknown_goal_mode")
        if self.relation not in ("at_least", "at_most"):
            raise ContractError("unknown_relation")
        if self.intent_source not in ("explicit_operator_or_planner", "synthetic_task_rules"):
            raise ContractError("explicit_goal_required")
        number(self.target, "target")
        number(self.tolerance, "tolerance", 0)

    @property
    def identity(self) -> str:
        return digest(asdict(self))

    def gap(self, value: float) -> float:
        value = number(value, "goal_value")
        signed = self.target - value if self.relation == "at_least" else value - self.target
        return max(0.0, signed - self.tolerance)


@dataclass(frozen=True)
class Observation:
    scope: Scope
    time: float
    metric: str
    unit: str
    value: float | None
    evidence_id: str
    observed: bool = True
    execution: str = "settled"  # settled, pending, unknown

    def __post_init__(self):
        if not isinstance(self.scope, Scope):
            raise ContractError("scope_required")
        number(self.time, "time", 0)
        for key in ("metric", "unit", "evidence_id"):
            text(getattr(self, key), key)
        if type(self.observed) is not bool:
            raise ContractError("observed_flag_not_boolean")
        if self.value is not None:
            number(self.value, "value")
        if self.observed != (self.value is not None):
            raise ContractError("value_observation_flag_conflict")
        if self.execution not in ("settled", "pending", "unknown"):
            raise ContractError("unknown_execution_state")


@dataclass(frozen=True)
class Expectation:
    scope: Scope
    goal_identity: str
    hypothesis_id: str
    issued_at: float
    not_before: float
    review_at: float
    window_source: str  # rules, prior_observations, planner_prediction

    def __post_init__(self):
        if not isinstance(self.scope, Scope):
            raise ContractError("scope_required")
        text(self.goal_identity, "goal_identity")
        text(self.hypothesis_id, "hypothesis_id")
        for key in ("issued_at", "not_before", "review_at"):
            number(getattr(self, key), key, 0)
        if not self.issued_at <= self.not_before <= self.review_at:
            raise ContractError("invalid_effect_window")
        if self.review_at <= self.issued_at:
            raise ContractError("empty_effect_window")
        if self.window_source not in ("rules", "prior_observations", "planner_prediction"):
            raise ContractError("effect_window_source_required")


@dataclass(frozen=True)
class Feedback:
    status: str
    reason: str
    scope: Scope
    goal_identity: str
    hypothesis_id: str
    evidence_id: str
    time: float
    goal_gap: float | None
    goal_observed_satisfied: bool | None
    window_closed: bool
    outcome_usable: bool
    execution_authorized: bool = False
    causal_credit_established: bool = False

    def as_dict(self) -> dict:
        return asdict(self)


class GoalEffectMonitor:
    """One expectation per monitor, with independent run/general/goal binding.

    Only the specified metric can establish progress. A satisfied maintain goal
    is useful even without motion. Sampling never proves uninterrupted safety.
    Review time is a reason to reconsider, NOT proof of a pathfinding failure.
    """
    def __init__(self, goal: Goal, expectation: Expectation, initial: Observation):
        if not isinstance(goal, Goal) or not isinstance(expectation, Expectation):
            raise ContractError("typed_goal_and_expectation_required")
        self.goal, self.expectation = goal, expectation
        if expectation.goal_identity != goal.identity:
            raise ContractError("goal_binding_mismatch")
        self._check(initial)
        if initial.time != expectation.issued_at:
            raise ContractError("initial_time_must_match_issue")
        self._last_time = initial.time
        self._seen = {initial.evidence_id}
        self._best_gap = goal.gap(initial.value) if initial.observed else None
        self._closed = False
        self._maintain_breach = bool(goal.mode == "maintain" and initial.observed
                                     and goal.gap(initial.value) > 0)

    def _check(self, obs: Observation):
        if not isinstance(obs, Observation):
            raise ContractError("typed_observation_required")
        if obs.scope != self.expectation.scope:
            raise ContractError("scope_or_clock_or_revision_mismatch")
        if (obs.metric, obs.unit) != (self.goal.metric, self.goal.unit):
            raise ContractError("unrelated_metric_or_unit")

    def observe(self, obs: Observation) -> Feedback:
        self._check(obs)
        if self._closed:
            raise ContractError("expectation_already_closed")
        if obs.evidence_id in self._seen or obs.time <= self._last_time:
            raise ContractError("duplicate_or_nonadvancing_evidence")
        if len(self._seen) >= 4096:
            raise ContractError("observation_capacity_exhausted")
        e, g = self.expectation, self.goal
        gap = g.gap(obs.value) if obs.observed else None
        satisfied = gap == 0 if gap is not None else None
        improved = gap is not None and self._best_gap is not None and gap < self._best_gap
        breach = self._maintain_breach or bool(g.mode == "maintain" and gap is not None and gap > 0)
        closed = False
        usable = False
        if not obs.observed:
            status, reason = "NEED_OBSERVATION", "missing_metric_is_not_failure"
        elif g.mode == "maintain" and breach:
            status, reason = "RECONSIDER", "observed_invariant_breach"
            # A later recovery cannot erase the earlier observed breach.
            closed, usable = obs.time >= e.review_at, obs.time >= e.review_at
        elif g.mode == "maintain":
            status, reason = "MAINTAINING", "sampled_invariant_intact"
            if obs.time >= e.review_at:
                status, closed, usable = "MAINTAINED_AT_SAMPLES", True, True
        elif satisfied:
            status, reason = "GOAL_OBSERVED", "goal_satisfied_not_action_causation"
            closed, usable = True, True
        elif obs.time < e.not_before:
            status, reason = "WAIT", "expected_effect_not_due"
        elif obs.execution == "unknown":
            status, reason = "NEED_OBSERVATION", "execution_status_unknown"
        elif obs.execution == "pending":
            if obs.time <= e.review_at:
                status, reason = "WAIT", "declared_effect_in_flight"
            else:
                status, reason = "RECONSIDER", "overdue_pending_not_proven_failure"
        elif obs.time < e.review_at:
            status, reason = ("PROGRESS", "goal_metric_improved") if improved else ("WAIT", "review_window_open")
        else:
            status, reason = "RECONSIDER", "goal_unmet_after_review_window"
            closed, usable = True, True
        if g.mode == "maintain" and breach:
            satisfied = False
        result = Feedback(status, reason, obs.scope, g.identity, e.hypothesis_id,
                          obs.evidence_id, obs.time, gap, satisfied, closed, usable)
        self._last_time = obs.time
        self._seen.add(obs.evidence_id)
        self._closed = closed
        self._maintain_breach = breach
        if gap is not None:
            self._best_gap = gap if self._best_gap is None else min(self._best_gap, gap)
        return result
