"""Explicit, reversible scout binding for the unchanged warm-start runner loop.

No loader, CLI, source write, or standalone host launcher is provided. A
separately reviewed caller supplies the already-loaded runner and its existing
operation permission. ``install`` changes only callbacks on that in-memory
runner, the base object it loads and its runtime helper. ``run_main_once`` is
an explicit OPERATIONAL call to the supplied main, not a read-only check.
Warm-start/production/Apollyon/readiness and cleanup implementations remain the
caller's originals. A failed startup requests the existing helper cleanup before
propagating the original error.

This is opt-in runtime wiring, not new execution permission or durable exactly-
once delivery. Tests use the exact saved runner loop with inert callbacks.
Helper callback completion does not prove a dormant service or removed container.
The caller must verify source bytes, bind a NEW authorized experiment and retain
its attempt guard. Prior pair-03 authority cannot be reused through this class.
"""
from __future__ import annotations

from copy import deepcopy
from types import ModuleType, SimpleNamespace
from typing import Any, Callable

from openra_env.learning.abaddon_scout_host_bridge_v1 import ScoutMissionHostBridge
from openra_env.learning.abaddon_scout_missions_v1 import MissionPolicy, ScoutMissionController
from openra_env.learning.goal_effect_core_v1 import Scope

EVIDENCE_KEY = "abaddon_scout_missions_v1"
CONTROLLER_SHA256 = "b235d4cff3e3953ed7c511de52c76ada7e1a47046295e104353b61ef09e11103"


class ScoutRunnerHold(RuntimeError):
    """Stop this binding. Restoration is not permission to start another attempt."""


def _require(value: bool, reason: str) -> None:
    if not value:
        raise ScoutRunnerHold(reason)


class ScoutMissionRunnerBinding:
    """Bind the existing decide -> gate -> log -> joint -> result-log sequence.

    The unchanged runner constructs Abaddon before it chooses a run ID. The
    constructor proxy therefore records doctrine/seed, while the real mission
    controller is instantiated only after the run header and warm-start session
    are bound. Commands are acknowledged only by the bridge after joint success.
    Caller-owned callbacks, modules, protocol classes, and single-threaded use
    remain trusted. No source hash or operator identity is attested by this class.
    """
    def __init__(self, runner: Any, *, doctrine: str, seed: int, round_limit: int,
                 ticks_per_round: int, world_revision: str, authority_check: Callable,
                 mission_policy: MissionPolicy = MissionPolicy()):
        _require(type(doctrine) is str and doctrine.isupper(), "doctrine_required")
        _require(type(seed) is int and 0 <= seed <= 2**31 - 1, "seed_bound")
        _require(type(round_limit) is int and 1 <= round_limit <= 200, "round_limit_bound")
        _require(type(ticks_per_round) is int and 1 <= ticks_per_round <= 100, "round_ticks_bound")
        _require(type(world_revision) is str and 0 < len(world_revision) <= 240, "world_revision_required")
        _require(callable(authority_check) and type(mission_policy) is MissionPolicy, "caller_authority_and_policy_required")
        _require(callable(getattr(runner, "load_base", None)) and callable(getattr(runner, "append_jsonl", None)),
                 "original_runner_callbacks_required")
        self._runner = runner
        self._load = runner.load_base
        self._append = runner.append_jsonl
        self._doctrine, self._seed, self._round_limit, self._ticks = doctrine, seed, round_limit, ticks_per_round
        self._revision, self._authority, self._policy = world_revision, authority_check, mission_policy
        self._slots = []
        self._installed = False
        self._used = False
        self._held = False
        self._phase = "BEFORE_HEADER"
        self._base = self._controller_module = self._bridge = None
        self._scope = self._session = self._stub = self._pb2 = None
        self._round = 1
        self._constructor_seen = False
        self._run_id = self._observation = self._proposal = self._prepared = self._last_result = None
        self._warm_joint_calls = 0
        self._helper = None
        self._main_entered = False
        self._main_returned = False
        self._main_error_type = None
        self._final_cleanup_error_type = None
        self._restoration_error_type = None
        self._final_cleanup_fallback_attempted = False
        self._runtime_start_attempted = False
        self._runtime_start_returned = False
        self._runtime_start_failed = False
        self._helper_cleanup_attempts = 0
        self._helper_cleanup_returned = False
        self._helper_cleanup_error_type = None
        self._failed_start_cleanup_attempted = False
        self._failed_start_cleanup_error_type = None

    def _wrapped(self, callback: Callable, *, allow_held: bool = False) -> Callable:
        def guarded(*args, **kwargs):
            try:
                _require(self._installed and (allow_held or not self._held), "binding_not_installed_or_already_held")
                return callback(*args, **kwargs)
            except BaseException:
                self._held = True
                raise
        return guarded

    def _slot(self, obj: Any, name: str, callback: Callable, *, allow_held: bool = False) -> None:
        original = getattr(obj, name)
        replacement = self._wrapped(callback, allow_held=allow_held)
        setattr(obj, name, replacement)
        self._slots.append((obj, name, original, replacement))

    def install(self) -> None:
        _require(not self._used, "binding_install_once")
        _require(self._runner.load_base is self._load and self._runner.append_jsonl is self._append,
                 "runner_callbacks_changed_before_install")
        self._used = True
        self._slot(self._runner, "load_base", self._load_base)
        self._slot(self._runner, "append_jsonl", self._append_row)
        self._installed = True

    def run_main_once(self):
        """Explicitly call the supplied main once, then restore our callbacks.

        This is an operational call, NOT preflight-only. There is no source or
        host attestation, durable attempt guard, CLI or permission grant here.
        A reviewed caller must already provide those surrounding boundaries for
        a NEW experiment. Cleanup is not a game retry. No artifact is deleted.
        """
        _require(self._installed and not self._held and not self._main_entered
                 and self._base is None and callable(getattr(self._runner, "main", None)),
                 "fresh_installed_binding_and_original_main_required")
        self._main_entered = True
        result, failure, traceback = None, None, None
        try:
            result = self._runner.main()
            self._main_returned = True
        except BaseException as error:
            self._held = True
            self._main_error_type = type(error).__name__
            failure, traceback = error, error.__traceback__
        finally:
            # The historical finally can itself fail before reaching helper
            # teardown (for example Docker inspection). Independently reach the
            # existing cleanup once if no cleanup through this binding occurred.
            # Never retry an observed failed cleanup; retain its uncertain state.
            if self._runtime_start_attempted and self._helper_cleanup_attempts == 0:
                self._final_cleanup_fallback_attempted = True
                try:
                    self._cleanup_helper()
                except BaseException as error:
                    self._held = True
                    self._final_cleanup_error_type = type(error).__name__
                    if failure is None:
                        failure, traceback = error, error.__traceback__
            try:
                self.restore()
            except BaseException as error:
                self._held = True
                self._restoration_error_type = type(error).__name__
                if failure is None:
                    failure, traceback = error, error.__traceback__
        if failure is not None:
            raise failure.with_traceback(traceback)
        return result

    def restore(self) -> None:
        """Restore only our own still-installed callbacks; never overwrite a rival."""
        if not self._installed:
            return
        if not all(getattr(obj, name) is replacement for obj, name, _, replacement in self._slots):
            self._held = True
            raise ScoutRunnerHold("callback_changed_do_not_overwrite")
        for obj, name, original, _ in reversed(self._slots):
            setattr(obj, name, original)
        self._installed = False

    def _current_authority(self) -> None:
        _require(self._scope is not None and self._authority(self._scope) is True,
                 "existing_operation_authority_required")

    def _load_base(self):
        _require(self._base is None, "one_base_instance_required")
        base = self._load()
        _require(getattr(base, "ABADDON_CONTROLLER_SHA", None) == CONTROLLER_SHA256,
                 "frozen_controller_binding_required")
        _require(all(callable(getattr(base, n, None)) for n in
                     ("load_module", "decision_to_commands", "joint_advance", "compact_state")),
                 "original_base_callbacks_required")
        self._base = base
        self._original_loader, self._original_gate, self._original_joint = (
            base.load_module, base.decision_to_commands, base.joint_advance)
        self._slot(base, "load_module", self._load_module)
        self._slot(base, "decision_to_commands", self._gate)
        self._slot(base, "joint_advance", self._joint)
        return base

    def _load_module(self, path, name):
        module = self._original_loader(path, name)
        if path == getattr(self._base, "APOLLYON_RUNNER", None):
            _require(self._helper is None and all(callable(getattr(module, n, None))
                     for n in ("start_ollama", "cleanup")), "one_original_runtime_helper_required")
            self._helper = module
            self._original_helper_start = module.start_ollama
            self._original_helper_cleanup = module.cleanup
            self._slot(module, "start_ollama", self._start_helper)
            # Teardown must remain callable after a failed gate/log/transport or
            # revoked operation permission. This never restarts or retries a game.
            self._slot(module, "cleanup", self._cleanup_helper, allow_held=True)
            return module
        if path != self._base.ABADDON_CONTROLLER:
            return module
        _require(self._controller_module is None and callable(getattr(module, "AbaddonController", None)),
                 "one_frozen_controller_module_required")
        _require(not hasattr(module, "__void_candidate_binding__"), "separate_policy_treatment_required")
        self._controller_module = module
        proxy = ModuleType("void_scout_mission_constructor_proxy")
        proxy.__dict__.update(vars(module))
        proxy.AbaddonController = self._wrapped(self._constructor)
        return proxy

    def _cleanup_helper(self):
        """Observe the supplied cleanup callback, not actual service-state proof."""
        self._helper_cleanup_attempts += 1
        self._helper_cleanup_returned = False
        self._helper_cleanup_error_type = None
        try:
            result = self._original_helper_cleanup()
        except BaseException as error:
            self._helper_cleanup_error_type = type(error).__name__
            raise
        self._helper_cleanup_returned = True
        return result

    def _start_helper(self):
        """Bound a failed-start cleanup fallback without masking the start error.

        The frozen runner sets its local started flag only after start returns.
        Its outer finally therefore cannot handle a partial failing start alone.
        An observed cleanup during start is not repeated. A supplied startup
        callback may have performed unobservable internal cleanup; in that case
        the one fallback may repeat that teardown. The caller must supply the
        existing idempotent helper, not a new cleanup or dispatch implementation.
        """
        _require(self._phase == "BEFORE_HEADER" and not self._runtime_start_attempted,
                 "runtime_start_once_before_controller_header")
        self._current_authority()
        self._runtime_start_attempted = True
        prior_cleanups = self._helper_cleanup_attempts
        try:
            result = self._original_helper_start()
        except BaseException:
            self._runtime_start_failed = True
            if self._helper_cleanup_attempts == prior_cleanups:
                self._failed_start_cleanup_attempted = True
                try:
                    self._cleanup_helper()
                except BaseException as cleanup_error:
                    # Preserve the primary startup failure, including interrupts.
                    # The secondary cleanup error remains explicit in snapshot().
                    self._failed_start_cleanup_error_type = type(cleanup_error).__name__
            raise
        self._runtime_start_returned = True
        return result

    def _constructor(self, doctrine: str, seed: int = 2050):
        _require(not self._constructor_seen and type(seed) is int and seed == self._seed
                 and type(doctrine) is str and doctrine == self._doctrine, "constructor_scope_mismatch")
        self._constructor_seen = True
        return SimpleNamespace(decide=self._wrapped(self._decide))

    def _decide(self, observation: dict) -> dict:
        _require(self._phase == "ROUND_READY" and self._round <= self._round_limit,
                 "candidate_round_not_ready")
        self._current_authority()
        self._observation = deepcopy(observation)
        self._proposal = self._bridge.propose(observation, evidence_id=f"{self._run_id}:round:{self._round}")
        self._phase = "WAIT_GATE"
        return deepcopy(self._proposal["decision"])

    def _gate(self, name, args, state, pending, pb2):
        if self._phase in {"BEFORE_HEADER", "ROUND_READY"}:
            # Warm-start/Apollyon's already reviewed gate path is untouched.
            return self._original_gate(name, args, state, pending, pb2)
        _require(self._phase == "WAIT_GATE", "unexpected_gate_order")
        self._current_authority()
        action = self._proposal["decision"]["action"]
        _require(pb2 is self._pb2 and name == action["tool"] and args == action["arguments"]
                 and type(state) is dict and state == self._observation, "candidate_gate_echo_changed")
        self._prepared = self._bridge.validate_proposal(self._proposal["proposal_id"], pending)
        self._phase = "WAIT_DECISION_LOG"
        return (self._prepared["accepted"], self._prepared["host_reason"], self._prepared["commands"])

    def _joint(self, stub, pb2, session_id, ticks, commands):
        self._current_authority()
        if self._session is None:
            _require(self._phase == "BEFORE_HEADER" and type(session_id) is str and bool(session_id),
                     "warm_start_session_required")
            self._session, self._stub, self._pb2 = session_id, stub, pb2
        _require(session_id == self._session and stub is self._stub and pb2 is self._pb2,
                 "runner_session_or_protocol_changed")
        if self._phase == "BEFORE_HEADER":
            self._warm_joint_calls += 1
            return self._original_joint(stub, pb2, session_id, ticks, commands)
        _require(self._phase == "WAIT_JOINT" and type(ticks) is int and ticks == self._ticks,
                 "joint_without_logged_validated_round")
        result = self._bridge.dispatch_joint(stub, proposal_id=self._proposal["proposal_id"], commands_by_player=commands)
        self._last_result = {"start_tick": result[0].start_tick, "end_tick": result[0].end_tick}
        self._phase = "WAIT_RESULT_LOG"
        return result

    def _append_row(self, path, row):
        _require(type(row) is dict and EVIDENCE_KEY not in row and "abaddon_policy_candidate_v1" not in row,
                 "unambiguous_scout_evidence_required")
        event = row.get("event")
        if event == "warm_start_header":
            _require(self._run_id is None and self._constructor_seen and type(row.get("seed")) is int and row["seed"] == self._seed,
                     "warm_start_header_scope_mismatch")
            self._scope = Scope(row.get("run_id"), "abaddon", self._revision, "game_ticks")
            self._current_authority()
            self._append(path, deepcopy(row))
            self._run_id = row["run_id"]
            return
        if event == "run_header":
            _require(self._phase == "BEFORE_HEADER" and self._run_id is not None and self._session is not None
                     and row.get("run_id") == self._run_id and type(row.get("seed")) is int and row["seed"] == self._seed
                     and row.get("abaddon_doctrine") == self._doctrine
                     and type(row.get("ticks_per_round")) is int and row["ticks_per_round"] == self._ticks
                     and type(row.get("round_limit")) is int and row["round_limit"] == self._round_limit
                     and row.get("abaddon_controller_sha256") == CONTROLLER_SHA256,
                     "run_header_scope_mismatch")
            self._current_authority()
            controller = ScoutMissionController(self._controller_module, scope=self._scope,
                doctrine=self._doctrine, seed=self._seed, mission_policy=self._policy)
            self._bridge = ScoutMissionHostBridge(controller, scope=self._scope, pb2=self._pb2,
                decision_to_commands=self._original_gate, joint_advance=self._original_joint,
                authority_check=self._authority, session_id=self._session, ticks_per_round=self._ticks)
            metadata = {"schema": "void.abaddon.scout-runner-binding.v1", "repair_applied": True,
                        "new_execution_permission_created": False, "training_use_approved": False,
                        "source_identity_verified_by_binding": False, "automatic_policy_promotion": False}
            self._append(path, {**deepcopy(row), EVIDENCE_KEY: metadata})
            self._phase = "ROUND_READY"
            return
        if event in {"joint_decision", "joint_result"}:
            _require(row.get("run_id") == self._run_id and type(row.get("round")) is int
                     and row["round"] == self._round, "round_log_scope_mismatch")
            if event == "joint_decision":
                _require(self._phase == "WAIT_DECISION_LOG", "decision_log_order")
                actual = row.get("abaddon")
                _require(type(actual) is dict and actual.get("decision") == self._prepared["decision"]
                         and actual.get("accepted") is self._prepared["accepted"]
                         and type(actual.get("command_count")) is int
                         and actual["command_count"] == self._prepared["command_count"]
                         and actual.get("host_reason") == self._prepared["host_reason"]
                         and type(row.get("start_tick")) is int and row["start_tick"] == self._observation["tick"]
                         and row.get("abaddon_state") == self._base.compact_state(self._observation),
                         "decision_log_differs_from_prepared_round")
                metadata = {"proposal_id": self._proposal["proposal_id"], "dispatch_observed": False,
                            "training_use_approved": False}
                self._append(path, {**deepcopy(row), EVIDENCE_KEY: metadata})
                self._phase = "WAIT_JOINT"
            else:
                _require(self._phase == "WAIT_RESULT_LOG" and type(row.get("start_tick")) is int
                         and type(row.get("end_tick")) is int
                         and row["start_tick"] == self._last_result["start_tick"]
                         and row["end_tick"] == self._last_result["end_tick"], "result_log_before_joint_or_clock_drift")
                feedback = self._bridge.snapshot()["last_feedback"]
                self._append(path, {**deepcopy(row), EVIDENCE_KEY: {
                    "submission_feedback": feedback, "training_use_approved": False}})
                self._phase = "ROUND_READY"
                self._round += 1
                self._observation = self._proposal = self._prepared = None
            return
        _require(self._phase == "BEFORE_HEADER", "unexpected_controller_log_event")
        self._append(path, deepcopy(row))

    def snapshot(self) -> dict:
        bridge = self._bridge.snapshot() if self._bridge is not None else None
        if bridge is not None:
            bridge.pop("runtime_hooks_installed", None)
        return {"callbacks_installed": self._installed, "held": self._held, "phase": self._phase,
                "next_round": self._round, "warm_start_joint_call_count": self._warm_joint_calls,
                "bridge": bridge, "execution_permission_created": False, "automatic_retry": False,
                "source_identity_verified_by_binding": False,
                "main_lifecycle": {
                    "entered": self._main_entered,
                    "callback_returned": self._main_returned,
                    "error_type": self._main_error_type,
                    "final_cleanup_fallback_attempted": self._final_cleanup_fallback_attempted,
                    "final_cleanup_error_type": self._final_cleanup_error_type,
                    "restoration_error_type": self._restoration_error_type,
                    "actual_runtime_state_verified": False,
                },
                "helper_lifecycle": {
                    "start_attempted": self._runtime_start_attempted,
                    "start_callback_returned": self._runtime_start_returned,
                    "start_failed": self._runtime_start_failed,
                    "cleanup_callback_attempts": self._helper_cleanup_attempts,
                    "cleanup_callback_returned": self._helper_cleanup_returned,
                    "cleanup_error_type": self._helper_cleanup_error_type,
                    "failed_start_cleanup_attempted": self._failed_start_cleanup_attempted,
                    "failed_start_cleanup_error_type": self._failed_start_cleanup_error_type,
                    "actual_runtime_state_verified": False,
                }}
