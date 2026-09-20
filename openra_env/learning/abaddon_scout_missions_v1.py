"""Offline candidate adapter for the frozen Abaddon controller's scouting branch.

No loader, engine, filesystem, model, or runtime hook is installed here. Supply
an already reviewed, trusted controller module. Its ordinary decision priorities
and target planner are reused, not copied. The caller must retain the original
host validator and acknowledge its actual result before the next observation.

A proposal is not an issued order. A host-accepted order is not an arrived scout.
Only sampled arrival enters completed history. Review deadlines are candidate
policy choices, not proof of terrain failure or improved live performance.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
from types import SimpleNamespace
from typing import Any

from openra_env.learning.goal_effect_core_v1 import (
    Expectation, Goal, GoalEffectMonitor, Observation, Scope, digest, text,
)

SCHEMA = "void.abaddon.scout-mission-proposal.v1"
MAX_OBSERVATIONS = 4096
MAX_UNITS = 4096
MAX_MINIMAP_CHARS = 65536


class ScoutMissionHold(ValueError):
    """Unusable evidence or an unresolved proposal; never a fallback command."""


def _require(value: bool, reason: str) -> None:
    if not value:
        raise ScoutMissionHold(reason)


def _int(value: Any, name: str, low: int = 0, high: int = 2**53 - 1) -> int:
    _require(type(value) is int and low <= value <= high, "invalid_" + name)
    return value


@dataclass(frozen=True)
class MissionPolicy:
    stall_ticks: int = 300
    maximum_mission_ticks: int = 1200
    completed_cooldown_ticks: int = 1200
    failed_cooldown_ticks: int = 300
    arrival_radius: int = 2
    maximum_history: int = 128

    def __post_init__(self) -> None:
        for name in ("stall_ticks", "maximum_mission_ticks", "completed_cooldown_ticks", "failed_cooldown_ticks"):
            _int(getattr(self, name), name, 1, 100000)
        _require(self.maximum_mission_ticks >= self.stall_ticks, "mission_window_shorter_than_stall_window")
        _int(self.arrival_radius, "arrival_radius", 0, 16)
        _int(self.maximum_history, "maximum_history", 1, 4096)


def _state(raw: dict) -> tuple[int, tuple[int, int], dict[int, dict]]:
    _require(type(raw) is dict and type(raw.get("map")) is dict, "observation_map_required")
    tick = _int(raw.get("tick"), "tick")
    shape = tuple(_int(raw["map"].get(k), "map_" + k, 1, 4096) for k in ("width", "height"))
    rows = raw.get("units_summary")
    _require(type(rows) is list and len(rows) <= MAX_UNITS, "owned_unit_census_required")
    units = {}
    for row in rows:
        _require(type(row) is dict, "unit_object_required")
        uid = _int(row.get("id"), "unit_id", 1)
        _require(uid not in units, "duplicate_unit_id")
        _int(row.get("cell_x"), "unit_x", 0, shape[0] - 1)
        _int(row.get("cell_y"), "unit_y", 0, shape[1] - 1)
        _require(type(row.get("type")) is str and 0 < len(row["type"]) <= 64, "unit_type_required")
        _require(type(row.get("can_attack")) is bool, "combat_flag_required")
        flags = [row[k] for k in ("idle", "is_idle") if k in row]
        _require(all(type(v) is bool for v in flags) and len(set(flags)) <= 1, "idle_flags_conflict_or_invalid")
        hp = row.get("hp_percent")
        _require(hp is None or (type(hp) in (int, float) and 0 <= hp <= 1), "invalid_health")
        for k in ("activity", "current_activity"):
            _require(k not in row or (type(row[k]) is str and len(row[k]) <= 256), "invalid_activity")
        units[uid] = {**row, "_idle": bool(flags) and flags[0] is True}
    for key in ("enemy_summary", "enemy_buildings_summary"):
        _require(type(raw.get(key)) is list and len(raw[key]) <= MAX_UNITS
                 and all(type(row) is dict for row in raw[key]), "visible_contact_census_required")
    minimap = raw.get("minimap")
    _require(minimap is None or (type(minimap) is str and len(minimap) <= MAX_MINIMAP_CHARS), "minimap_bound")
    return tick, shape, units


def _distance(unit: dict, target: tuple[int, int]) -> int:
    return abs(unit["cell_x"] - target[0]) + abs(unit["cell_y"] - target[1])


class ScoutMissionController:
    """One scout mission and one unresolved proposal per run/general/revision.

    ``decide`` returns an envelope; send only its ``decision`` through the
    existing host gate. ``acknowledge`` records that gate's accepted flag and
    dispatched command count, not a fabricated execution result. This class
    never dispatches. Missing acknowledgement holds rather than guessing.
    """
    def __init__(self, legacy: Any, *, scope: Scope, doctrine: str, seed: int,
                 policy: dict | None = None, mission_policy: MissionPolicy = MissionPolicy()):
        _require(type(scope) is Scope and scope.general_id == "abaddon" and scope.clock_unit == "game_ticks",
                 "abaddon_game_tick_scope_required")
        _require(type(mission_policy) is MissionPolicy, "mission_policy_required")
        self._legacy, self.scope, self.policy = legacy, scope, mission_policy
        self._base = legacy.AbaddonController(doctrine, seed, policy=deepcopy(policy))
        self._mission = None
        self._history: list[dict] = []
        self._pending = None
        self._last_tick = -1
        self._shape = None
        self._seen: set[str] = set()
        self._last_event = {"status": "UNASSIGNED", "reason": "no_order_issued"}

    def _monitor(self, target: tuple[int, int], unit: dict, tick: int, deadline: int, mission_id: str):
        goal = Goal(mission_id, "scout_target_distance", "manhattan_cells", "achieve", "at_most",
                    self.policy.arrival_radius)
        expectation = Expectation(self.scope, goal.identity, mission_id, tick, tick,
                                  min(tick + self.policy.stall_ticks, deadline), "planner_prediction")
        return GoalEffectMonitor(goal, expectation, Observation(
            self.scope, tick, goal.metric, goal.unit, _distance(unit, target), f"issue:{mission_id}:{tick}"))

    def _finish(self, status: str, reason: str, tick: int) -> None:
        mission = self._mission
        _require(mission is not None, "active_mission_required")
        # Expire only by observed game ticks; unrelated construction cannot clear history.
        _require(len(self._history) < self.policy.maximum_history, "mission_history_capacity")
        ttl = self.policy.completed_cooldown_ticks if status == "COMPLETED" else self.policy.failed_cooldown_ticks
        self._history.append({"target": mission["target"], "status": status, "reason": reason,
                              "observed_tick": tick, "expires_tick": tick + ttl})
        self._last_event = {"status": status, "reason": reason, "unit_id": mission["unit_id"],
                            "target": mission["target"], "observed_tick": tick}
        self._mission = None

    def _observe_mission(self, tick: int, units: dict[int, dict], evidence_id: str) -> None:
        mission = self._mission
        if mission is None:
            return
        unit = units.get(mission["unit_id"])
        if unit is None or unit["type"] != mission["unit_type"] or not unit["can_attack"] or unit.get("hp_percent") == 0:
            self._finish("FAILED", "assigned_actor_unavailable_not_death_proof", tick)
            return
        distance = _distance(unit, mission["target"])
        monitor = mission["monitor"]
        feedback = monitor.observe(Observation(self.scope, tick, monitor.goal.metric, monitor.goal.unit,
                                               distance, evidence_id))
        if feedback.status == "GOAL_OBSERVED":
            self._finish("COMPLETED", "arrival_observed_not_order_causation", tick)
        elif tick >= mission["deadline"]:
            self._finish("FAILED", "maximum_mission_window_elapsed", tick)
        elif distance < mission["best_distance"]:
            # Only a new all-time best distance renews the stall window. Moving
            # away/back, production, other units, or cash cannot renew it.
            mission["best_distance"] = distance
            mission["monitor"] = self._monitor(mission["target"], unit, tick, mission["deadline"], mission["id"])
            mission["status"] = "IN_PROGRESS"
            self._last_event = {"status": "IN_PROGRESS", "reason": "new_best_target_distance"}
        elif feedback.status == "RECONSIDER":
            self._finish("FAILED", "no_progress_review_due_not_path_failure_proof", tick)
        else:
            mission["status"] = "IN_PROGRESS"
            self._last_event = {"status": "IN_PROGRESS", "reason": "retain_assignment_within_review_window"}

    def _apply_decision(self, raw: dict, tick: int, shape: tuple[int, int], units: dict[int, dict]) -> dict:
        completed = [list(row["target"]) for row in self._history if row["status"] == "COMPLETED"]
        self._base.memory.scout_targets = deepcopy(completed)
        decision = self._base.decide(deepcopy(raw))
        _require(decision.get("schema") == "void.abaddon.decision.v1" and decision.get("identity") == "Abaddon",
                 "frozen_controller_decision_required")
        branch = decision.get("reason_codes")
        scouting = branch in (["INTELLIGENCE_GAP", "SYSTEMATIC_NEW_SCOUT_SECTOR"], ["NO_HIGHER_PRIORITY_ACTION"])
        intent = None
        if scouting:
            tool, args = "advance", {"ticks": self._base.profile["advance_ticks"]}
            reason = "SCOUT_MISSION_IN_PROGRESS" if self._mission else "NO_ELIGIBLE_IDLE_SCOUT"
            contact = bool(raw["enemy_summary"] or raw["enemy_buildings_summary"])
            scout_policy = self._base.profile["scout"] or self._legacy._i(raw.get("explored_percent")) < 35
            if not self._mission and not contact and scout_policy:
                eligible = [u for _, u in sorted(units.items()) if u["_idle"] and u["can_attack"]
                            and u["type"] in self._legacy.INFANTRY and u.get("hp_percent") != 0
                            and not u.get("activity", "") and not u.get("current_activity", "")]
                if eligible:
                    unit = eligible[0]
                    memory = SimpleNamespace(scout_targets=[list(row["target"]) for row in self._history])
                    target = self._legacy._scout_target(raw, memory, unit["id"],
                                self._base.profile["scout_current_min"], self._base.profile["scout_history_min"])
                    reason = "SCOUT_TARGETS_UNAVAILABLE_UNTIL_REVIEW"
                    if target is not None:
                        _require(type(target) is tuple and len(target) == 2 and all(type(v) is int for v in target)
                                 and 0 <= target[0] < shape[0] and 0 <= target[1] < shape[1], "planner_target_invalid")
                        _require(len(self._history) < self.policy.maximum_history, "mission_history_capacity")
                        tool = "move_units"
                        args = {"unit_ids": str(unit["id"]), "target_x": target[0], "target_y": target[1]}
                        reason = "SCOUT_MISSION_PROPOSED_NOT_ISSUED"
                        intent = {"unit_id": unit["id"], "unit_type": unit["type"], "target": target,
                                  "initial_unit": deepcopy(unit), "tick": tick}
            elif not self._mission:
                reason = "NO_HIGHER_PRIORITY_ACTION"
            decision["action"] = {"tool": tool, "arguments": args}
            decision["reason_codes"] = [reason]
        # Discard the legacy planner's order-time history append. Only an
        # observed arrival is allowed into this adapter's completed history.
        self._base.memory.scout_targets = deepcopy(completed)
        self._base.memory.last_action_sha256 = digest(decision["action"])
        decision["memory"] = asdict(self._base.memory)
        proposal_id = digest({"scope": asdict(self.scope), "tick": tick, "decision": decision})
        self._pending = {"proposal_id": proposal_id, "decision": deepcopy(decision), "intent": intent, "tick": tick}
        return {"schema": SCHEMA, "proposal_id": proposal_id, "decision": decision,
                "mission": self.snapshot(), "execution_authorized": False, "host_validation_required": True}

    def decide(self, observation: dict, *, scope: Scope, evidence_id: str) -> dict:
        _require(scope == self.scope, "cross_scope_observation")
        text(evidence_id, "evidence_id")
        _require(self._pending is None, "host_acknowledgement_required")
        _require(len(self._seen) < MAX_OBSERVATIONS, "observation_capacity")
        tick, shape, units = _state(observation)
        _require(tick > self._last_tick and evidence_id not in self._seen, "duplicate_or_nonadvancing_observation")
        _require(self._shape is None or self._shape == shape, "map_changed_within_scope")
        # Commit all-or-nothing, including monitor and controller memory. The
        # supplied trusted module remains shared; no global is patched.
        work = object.__new__(type(self))
        work.__dict__ = {k: (v if k == "_legacy" else deepcopy(v)) for k, v in self.__dict__.items()}
        work._history = [row for row in work._history if row["expires_tick"] > tick]
        work._observe_mission(tick, units, evidence_id)
        out = work._apply_decision(observation, tick, shape, units)
        work._last_tick, work._shape = tick, shape
        work._seen.add(evidence_id)
        self.__dict__ = work.__dict__
        return out

    def acknowledge(self, proposal_id: str, *, accepted: bool, command_count: int) -> dict:
        _require(type(proposal_id) is str and self._pending is not None
                 and proposal_id == self._pending["proposal_id"], "pending_proposal_identity_required")
        _require(type(accepted) is bool, "exact_host_accepted_flag_required")
        _int(command_count, "host_command_count", 0, 4096)
        _require(accepted or command_count == 0, "rejected_command_cannot_be_dispatched")
        pending = self._pending
        intent = pending["intent"]
        _require(not (accepted and intent and command_count == 0), "scout_order_not_dispatched")
        if accepted and intent:
            _require(self._mission is None, "mission_already_active")
            deadline = intent["tick"] + self.policy.maximum_mission_ticks
            self._mission = {"id": proposal_id, "unit_id": intent["unit_id"], "unit_type": intent["unit_type"],
                             "target": intent["target"], "issued_tick": intent["tick"], "deadline": deadline,
                             "best_distance": _distance(intent["initial_unit"], intent["target"]), "status": "ISSUED",
                             "monitor": self._monitor(intent["target"], intent["initial_unit"], intent["tick"], deadline, proposal_id)}
            self._last_event = {"status": "ISSUED", "reason": "host_accepted_not_arrival"}
        elif accepted and command_count > 0 and self._mission:
            action = pending["decision"]["action"]
            if action["tool"] in {"attack_target", "attack_move", "guard_target", "move_units", "stop_units"}:
                selector = action["arguments"].get("unit_ids")
                # Frozen controller emits all_combat or one decimal actor ID.
                if selector == "all_combat" or selector == str(self._mission["unit_id"]):
                    self._finish("INTERRUPTED", "accepted_higher_priority_order", pending["tick"])
        elif not accepted:
            self._last_event = {"status": "REJECTED", "reason": "host_rejected_no_mission_issued"}
        self._pending = None
        return self.snapshot()

    def snapshot(self) -> dict:
        mission = ({k: deepcopy(v) for k, v in self._mission.items() if k != "monitor"} if self._mission else None)
        return {"scope": asdict(self.scope), "active": mission, "history": deepcopy(self._history),
                "last_event": deepcopy(self._last_event), "pending_host_result": self._pending is not None,
                "execution_authorized": False, "runtime_integration_active": False}
