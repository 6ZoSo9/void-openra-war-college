"""Opt-in scout feedback bridge to the existing two-player joint host functions.

Nothing is installed on import or construction. The caller supplies the trusted
controller, unchanged host functions, protocol classes and existing authority
check. Only ``dispatch_joint`` can call that supplied joint function, once per
prepared round, after the supplied authority check. There is no loader, CLI,
model call, independent clock step, persistence, reset, retry, or promotion.

A successful host call establishes submission in a completed shared-clock step,
not per-command engine acceptance, arrival, or combat utility. The caller's
session, callbacks, OS and single-threaded integration are trust assumptions;
this in-memory bridge is not the durable execution-attempt gate.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

from openra_env.learning.abaddon_scout_missions_v1 import ScoutMissionController
from openra_env.learning.goal_effect_core_v1 import Scope

MAX_COMMANDS = 4096
MAX_COMMAND_BYTES = 65536
MAX_BATCH_BYTES = 1024 * 1024
PLAYERS = ("Multi0", "Multi1")


class ScoutHostHold(RuntimeError):
    """No further proposal or submission is allowed on this bridge after failure."""


def _require(condition: bool, reason: str) -> None:
    if not condition:
        raise ScoutHostHold(reason)


def _integer(value: Any, low: int, high: int) -> bool:
    return type(value) is int and low <= value <= high


class ScoutMissionHostBridge:
    """Prepare via the original validator; acknowledge only after joint success.

    ``prepare`` returns legacy-shaped decision/validation fields and copied
    commands. Preserve the existing host's assembly order:
    ``Multi1 = mechanical_placement + abaddon_commands``. ``dispatch_joint``
    checks that exact suffix, permits only placement/cancellation in the prefix,
    and passes both complete batches unchanged to the original joint function.

    Apollyon remains outside this controller. An advance proposal contributes
    zero commands; it never makes an additional clock call. Exceptions after
    dispatch begins mean possible world effects and permanently hold this object.
    No partial result is converted to an acknowledgement or retried.
    """
    def __init__(self, controller: ScoutMissionController, *, scope: Scope,
                 pb2: Any, decision_to_commands: Callable, joint_advance: Callable,
                 authority_check: Callable, session_id: str, ticks_per_round: int):
        _require(type(controller) is ScoutMissionController and type(scope) is Scope
                 and controller.scope == scope, "controller_scope_mismatch")
        _require(controller.snapshot()["pending_host_result"] is False,
                 "unresolved_controller_proposal")
        _require(all(callable(f) for f in (decision_to_commands, joint_advance, authority_check)),
                 "original_host_callbacks_required")
        _require(type(session_id) is str and 0 < len(session_id) <= 240
                 and all(32 <= ord(c) < 127 for c in session_id), "session_id_required")
        _require(_integer(ticks_per_round, 1, 250), "round_tick_bound")
        self._controller, self._scope, self._pb2 = controller, scope, pb2
        self._gate, self._joint, self._authority = decision_to_commands, joint_advance, authority_check
        self._session, self._ticks = session_id, ticks_per_round
        self._pending = None
        self._phase = "IDLE"
        self._next_tick = None
        self._last_feedback = None
        self._dispatch_calls = 0
        self._runtime_effects_possible = False
        self._hold_reason = None

    def _admit(self, phase: str) -> None:
        _require(self._phase == phase, "bridge_phase_" + self._phase)
        _require(self._authority(self._scope) is True, "existing_authority_not_current")

    def _held(self, phase: str) -> None:
        self._phase = "HELD"
        self._hold_reason = phase  # No arbitrary exception text in public state.

    def _command_bytes(self, commands: list) -> tuple[bytes, ...]:
        _require(type(commands) is list and len(commands) <= MAX_COMMANDS, "command_list_bound")
        data, total = [], 0
        for command in commands:
            _require(type(command) is self._pb2.Command, "protocol_command_type_required")
            raw = command.SerializeToString(deterministic=True)
            _require(type(raw) is bytes and len(raw) <= MAX_COMMAND_BYTES, "command_byte_bound")
            total += len(raw)
            _require(total <= MAX_BATCH_BYTES, "batch_byte_bound")
            data.append(raw)
        return tuple(data)

    def _copies(self, data: tuple[bytes, ...]) -> list:
        output = []
        for raw in data:
            command = self._pb2.Command()
            command.ParseFromString(raw)
            output.append(command)
        return output

    def propose(self, observation: dict, *, evidence_id: str) -> dict:
        """Select once; retain the full observation until the original gate runs.

        This split interface matches the frozen runner's existing decide/gate
        sequence. It has no gate, dispatch, or acknowledgement side effect.
        """
        try:
            self._admit("IDLE")
            _require(type(observation) is dict, "host_state_objects_required")
            tick = observation.get("tick")
            _require(_integer(tick, 0, 2**53 - 1), "host_start_tick_required")
            _require(self._next_tick is None or tick == self._next_tick, "previous_joint_end_tick_required")
            proposal = self._controller.decide(deepcopy(observation), scope=self._scope, evidence_id=evidence_id)
            self._pending = {"proposal_id": proposal["proposal_id"], "decision": deepcopy(proposal["decision"]),
                             "tick": tick, "observation": deepcopy(observation)}
            self._phase = "PROPOSED"
            return {"proposal_id": proposal["proposal_id"], "decision": deepcopy(proposal["decision"]),
                    "validation_observed": False, "dispatch_observed": False,
                    "mission": self._controller_view()}
        except BaseException:
            self._held("proposal_failed_no_joint_call")
            raise

    def validate_proposal(self, proposal_id: str, pending_buildings: dict) -> dict:
        """Validate the retained decision/state once without acknowledging dispatch.

        Pending building state is caller-owned. The original gate's bookkeeping
        is retained even if validation subsequently fails; no rollback is guessed.
        """
        try:
            self._admit("PROPOSED")
            _require(type(proposal_id) is str and proposal_id == self._pending["proposal_id"],
                     "proposed_identity_required")
            _require(type(pending_buildings) is dict, "host_state_objects_required")
            pending = self._pending
            decision = pending["decision"]
            action = decision["action"]
            result = self._gate(action["tool"], deepcopy(action["arguments"]),
                                deepcopy(pending["observation"]), pending_buildings, self._pb2)
            _require(type(result) is tuple and len(result) == 3, "host_validation_result_shape")
            accepted, reason, commands = result
            _require(type(accepted) is bool and type(reason) is str and len(reason) <= 4096,
                     "host_validation_result_types")
            encoded = self._command_bytes(commands)
            _require(accepted or not encoded, "rejected_gate_returned_commands")
            if action["tool"] == "advance":
                _require(not encoded, "advance_must_remain_shared_clock_noop")
            if decision["reason_codes"] == ["SCOUT_MISSION_PROPOSED_NOT_ISSUED"] and accepted:
                args = action["arguments"]
                _require(len(commands) == 1, "scout_requires_one_concrete_move")
                expected = self._pb2.Command(action=self._pb2.MOVE, actor_id=int(args["unit_ids"]),
                                             target_x=args["target_x"], target_y=args["target_y"], queued=False)
                _require(encoded == self._command_bytes([expected]), "scout_move_differs_from_proposal")
            self._pending = {"proposal_id": proposal_id, "decision": deepcopy(decision),
                             "tick": pending["tick"], "accepted": accepted, "host_reason": reason,
                             "commands": encoded}
            self._phase = "PREPARED"
            return {"proposal_id": proposal_id, "decision": deepcopy(decision),
                    "accepted": accepted, "host_reason": reason, "command_count": len(encoded),
                    "commands": self._copies(encoded), "dispatch_observed": False,
                    "mission": self._controller_view()}
        except BaseException:
            self._held("validation_failed_no_joint_call")
            raise

    def prepare(self, observation: dict, pending_buildings: dict, *, evidence_id: str) -> dict:
        """Compatibility convenience: propose once, then use the original gate."""
        try:
            _require(type(pending_buildings) is dict, "host_state_objects_required")
            proposal = self.propose(observation, evidence_id=evidence_id)
            return self.validate_proposal(proposal["proposal_id"], pending_buildings)
        except BaseException:
            self._held("prepare_failed_no_joint_call_from_prepare")
            raise

    def dispatch_joint(self, stub: Any, *, proposal_id: str, commands_by_player: dict) -> tuple:
        """Use one authorized original joint call and then acknowledge its result.

        This method can reach the caller's transport when deliberately integrated.
        Offline tests must supply an inert stub. No runtime installation or
        authority is provided by creating this bridge or reviewing its source.
        """
        try:
            self._admit("PREPARED")
            pending = self._pending
            _require(type(proposal_id) is str and proposal_id == pending["proposal_id"], "prepared_proposal_required")
            _require(type(commands_by_player) is dict and set(commands_by_player) == set(PLAYERS),
                     "exact_two_player_batches_required")
            batches = {p: self._command_bytes(commands_by_player[p]) for p in PLAYERS}
            count = len(pending["commands"])
            b_batch = batches["Multi1"]
            _require(len(b_batch) >= count and (not count or b_batch[-count:] == pending["commands"]),
                     "validated_abaddon_batch_changed")
            prefix = self._copies(b_batch[:-count] if count else b_batch)
            _require(all(c.action in (self._pb2.PLACE_BUILDING, self._pb2.CANCEL_PRODUCTION) for c in prefix),
                     "unreviewed_abaddon_prefix_commands")
            # Check again immediately before crossing the supplied transport boundary.
            _require(self._authority(self._scope) is True, "existing_authority_revoked_before_joint")
            self._phase = "DISPATCHING"
            self._dispatch_calls += 1
            self._runtime_effects_possible = True
            result = self._joint(stub, self._pb2, self._session, self._ticks,
                                  {p: self._copies(batches[p]) for p in PLAYERS})
            _require(type(result) is tuple and len(result) == 2, "joint_return_shape")
            response, observations = result
            _require(getattr(response, "session_id", None) == self._session, "joint_response_session_mismatch")
            response_rows = list(getattr(response, "player_observations", ()))
            _require(len(response_rows) == 2 and {getattr(row, "player", None) for row in response_rows} == set(PLAYERS),
                     "joint_response_player_rows_mismatch")
            start, end = getattr(response, "start_tick", None), getattr(response, "end_tick", None)
            _require(_integer(start, 0, 2**53 - 1) and _integer(end, 0, 2**53 - 1)
                     and start == pending["tick"] and end == start + self._ticks,
                     "joint_response_clock_mismatch")
            _require(type(observations) is dict and set(observations) == set(PLAYERS), "joint_player_observations_mismatch")
            _require(all(type(getattr(o, "tick", None)) is int and o.tick == end for o in observations.values()),
                     "joint_observation_tick_mismatch")
            # Prepared command count alone never reaches this acknowledgement.
            self._controller.acknowledge(pending["proposal_id"],
                accepted=pending["accepted"], command_count=count)
            mission = self._controller_view()
            self._last_feedback = {"proposal_id": pending["proposal_id"], "start_tick": start,
                                   "end_tick": end, "host_accepted": pending["accepted"],
                                   "submitted_controller_command_count": count,
                                   "shared_clock_step_completed": True,
                                   "per_command_engine_acceptance_established": False,
                                   "arrival_established_by_dispatch": False,
                                   "mission": mission}
            self._pending = None
            self._next_tick = end
            self._phase = "IDLE"
            return response, observations
        except BaseException:
            self._held("joint_submission_or_acknowledgement_failed")
            raise

    def _controller_view(self) -> dict:
        view = self._controller.snapshot()
        # The pure adapter cannot observe whether its caller is wired to a live
        # transport. Do not forward its source-only false as a live status claim.
        view.pop("runtime_integration_active", None)
        view["runtime_integration_status_observed_by_controller"] = False
        return view

    def snapshot(self) -> dict:
        return {"phase": self._phase, "hold_reason": self._hold_reason,
                "dispatch_call_count": self._dispatch_calls,
                "runtime_effects_possible": self._runtime_effects_possible,
                "automatic_retry": False, "runtime_hooks_installed": False,
                "last_feedback": deepcopy(self._last_feedback),
                "controller": self._controller_view()}
