"""Pair-06 proto/gRPC game-child implementation for V8 parent IPC.

This source implements the child-side composition only. Import/contract
inspection are inert.

When later explicitly authorized, the child:
* runs under the accepted proto/gRPC venv;
* receives one HELLO over an inherited socketpair;
* loads the exact legacy warm-start runner;
* rebinds it to already-materialized frozen source/engine worktrees;
* replaces only legacy apollyon_decision_typed via the reviewed V8 decision
  hooks, with the decider implemented as bounded IPC;
* replaces only helper.start_ollama/helper.cleanup with inert compatibility
  functions so the legacy runner never starts or contacts Ollama;
* preserves legacy exact-file and dormant-service preflight checks;
* executes the exact pair-06 baseline FEINTER runner argv;
* emits GAME_RESULT or ERROR over IPC;
* restores every in-memory hook before returning.

This module does not create the socketpair, materialize worktrees, spawn the
child, create the durable game-attempt claim, load V8, or authorize execution.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_apollyon_decision_adapter_generation2
    as decision_adapter,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_apollyon_decision_adapter_source_binding_review_generation2
    as decision_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_child_ipc_bridge_generation2
    as ipc,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_parent_child_ipc_bridge_source_binding_review_generation2
    as ipc_review,
)
from openra_env.learning import apollyon_v2r13_portable_checkout as portable_checkout

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-proto-game-child-contract.v1"
)

IPC_REVIEW_GIT_BLOB = "61c037af43ba0d65995900e087622d917a4b5f58"
IPC_REVIEW_SOURCE_SHA256 = (
    "f19e4235d69fa953571c50c787bbd5aba072ab337e7e6a63de75f34b98d48c27"
)
DECISION_REVIEW_GIT_BLOB = "6b9e4efdd7294392deefd5461a0403daaab3b90b"
DECISION_REVIEW_SOURCE_SHA256 = (
    "56ceee6f4e10edf1c85b9e86df483f7090aa7866616288b167778b2d1f61b377"
)
PORTABLE_CHECKOUT_GIT_BLOB = "077fbf5a2847d85113eb8fcba3904b02343ebfef"
PORTABLE_CHECKOUT_SOURCE_SHA256 = (
    "92e16e281d5a9036d78d900f35d854c6fb9783b2bf156c2acab69408d13a015d"
)

PAIR_SLOT = 6
ARM = "baseline"
HELD_OUT = False
DOCTRINE = "FEINTER"
SEED = 208354846
ROUNDS = 36
TICKS_PER_ROUND = 25
STARTER_INFANTRY = 4
STAGING_MAX_TICKS = 800

PROTO_PYTHON = Path(
    "/home/zoso/.local/share/void-tools/openra-bridge-proto-v1/venv/bin/python"
)
LEGACY_RUNNER = Path(
    "/home/zoso/Downloads/"
    "void-actual-apollyon-vs-abaddon-warm-start-combat-spar-v1_4.py"
)
LEGACY_RUNNER_SHA256 = (
    "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
)

NEXT_GATE = "PAIR06_V8_PROTO_GAME_CHILD_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_proto_game_child_review"


class Pair06V8ProtoGameChildHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8ProtoGameChildHold(message)


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _dependencies() -> dict[str, Any]:
    ipc_contract = ipc_review.pair06_v8_parent_child_ipc_bridge_review_contract()
    decision_contract = decision_review.pair06_v8_apollyon_decision_adapter_review_contract()

    _require(
        ipc_contract.get("pair06_v8_parent_child_ipc_bridge_reviewed") is True,
        "pair06 IPC bridge not reviewed",
    )
    _require(
        ipc_contract.get("next_gate") == "PAIR06_V8_PROTO_GAME_CHILD_IMPLEMENTATION_REQUIRED",
        "pair06 proto-child frontier drift",
    )
    _require(
        decision_contract.get("pair06_v8_apollyon_decision_adapter_reviewed") is True,
        "pair06 V8 decision adapter not reviewed",
    )
    _require(
        decision_contract.get("legacy_hook_symbol") == "apollyon_decision_typed",
        "pair06 legacy decision hook drift",
    )
    _require(
        decision_contract.get("legacy_ollama_tool_call_used") is False,
        "pair06 decision adapter unexpectedly uses Ollama",
    )

    portable = portable_checkout.portable_binding_contract()
    _require(
        portable.get("legacy_warm_start_runner_sha256") == LEGACY_RUNNER_SHA256,
        "legacy warm-start runner identity drift",
    )
    _require(
        portable.get("canonical_checkout_mutation_required") is False,
        "portable checkout unexpectedly requires canonical mutation",
    )
    return {
        "ipc_review": deepcopy(ipc_contract),
        "decision_review": deepcopy(decision_contract),
        "portable_checkout": deepcopy(portable),
    }


def _load_exact_legacy():
    _require(LEGACY_RUNNER.is_file(), "legacy runner missing")
    _require(not LEGACY_RUNNER.is_symlink(), "legacy runner may not be symlink")
    _require(
        _sha256_file(LEGACY_RUNNER) == LEGACY_RUNNER_SHA256,
        "legacy runner SHA drift",
    )
    name = "void_pair06_v8_proto_game_child_legacy"
    spec = importlib.util.spec_from_file_location(name, LEGACY_RUNNER)
    _require(spec is not None and spec.loader is not None, "legacy runner import spec missing")
    module = importlib.util.module_from_spec(spec)
    previous = sys.modules.get(name)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        if previous is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous
        raise
    return module


class Pair06V8ProtoChildHooks:
    """Replace only legacy model transport/decision surfaces in memory."""

    def __init__(self, legacy: Any, sock: Any, attempt_id: str) -> None:
        _dependencies()
        _require(callable(getattr(legacy, "load_base", None)), "legacy load_base missing")
        _require(
            isinstance(attempt_id, str)
            and len(attempt_id) == 64
            and all(ch in "0123456789abcdef" for ch in attempt_id),
            "attempt_id invalid",
        )
        self.legacy = legacy
        self.sock = sock
        self.attempt_id = attempt_id
        self._original_load_base = legacy.load_base
        self._decision_hooks = decision_adapter.Pair06V8ApollyonDecisionHooks(
            legacy,
            self._ipc_decider,
        )
        self._installed = False
        self._helper = None
        self._helper_original_start = None
        self._helper_original_cleanup = None
        self._child_send_seq = 2
        self._parent_recv_seq = 2
        self._last_round = None
        self._attempt_no = 0
        self.legacy_ollama_start_calls = 0
        self.legacy_ollama_cleanup_calls = 0

    @property
    def next_child_send_seq(self) -> int:
        return self._child_send_seq

    def install(self) -> None:
        _require(not self._installed, "proto child hooks already installed")
        self.legacy.load_base = self._wrapped_load_base
        self._decision_hooks.install()
        self._installed = True

    def restore(self) -> None:
        self._decision_hooks.restore()
        if self._helper is not None:
            if self._helper_original_start is not None:
                self._helper.start_ollama = self._helper_original_start
            if self._helper_original_cleanup is not None:
                self._helper.cleanup = self._helper_original_cleanup
        if self._installed:
            self.legacy.load_base = self._original_load_base
        self._helper = None
        self._helper_original_start = None
        self._helper_original_cleanup = None
        self._installed = False

    def _wrapped_load_base(self):
        base = self._original_load_base()
        original_load_module = base.load_module
        expected = Path(base.APOLLYON_RUNNER).expanduser().resolve()

        def load_module(path: Path, name: str):
            helper = original_load_module(path, name)
            if Path(path).expanduser().resolve() != expected:
                return helper
            _require(callable(getattr(helper, "start_ollama", None)), "helper start_ollama missing")
            _require(callable(getattr(helper, "cleanup", None)), "helper cleanup missing")
            self._helper = helper
            self._helper_original_start = helper.start_ollama
            self._helper_original_cleanup = helper.cleanup

            def inert_start_ollama():
                self.legacy_ollama_start_calls += 1

            def inert_cleanup():
                self.legacy_ollama_cleanup_calls += 1

            helper.start_ollama = inert_start_ollama
            helper.cleanup = inert_cleanup
            return helper

        base.load_module = load_module
        return base

    def _ipc_decider(
        self,
        *,
        state: Mapping[str, Any],
        typed_tools: Any,
        tool_contract: Mapping[str, Any],
        doctrine: str,
        round_no: int,
        feedback: str = "",
    ) -> dict[str, Any]:
        if self._last_round != round_no:
            self._last_round = round_no
            self._attempt_no = 1
        else:
            self._attempt_no += 1
        _require(1 <= self._attempt_no <= 6, "decision attempt number exceeded")

        request = {
            "type": "DECIDE_REQUEST",
            "seq": self._child_send_seq,
            "protocol_version": 1,
            "pair_slot": PAIR_SLOT,
            "arm": ARM,
            "attempt_id": self.attempt_id,
            "round_no": round_no,
            "attempt_no": self._attempt_no,
            "state": deepcopy(dict(state)),
            "typed_tools": deepcopy(list(typed_tools)),
            "tool_contract": deepcopy(dict(tool_contract)),
            "doctrine": doctrine,
            "feedback": feedback,
        }
        ipc.send_message(
            self.sock,
            request,
            direction="child_to_parent",
            expected_seq=self._child_send_seq,
            expected_attempt_id=self.attempt_id,
        )
        self._child_send_seq += 1

        response = ipc.recv_message(
            self.sock,
            direction="parent_to_child",
            expected_seq=self._parent_recv_seq,
            expected_attempt_id=self.attempt_id,
        )
        self._parent_recv_seq += 1

        if response["type"] == "ABORT":
            raise Pair06V8ProtoGameChildHold(
                "parent aborted pair06 child: " + response["reason"]
            )
        _require(response["type"] == "DECIDE_RESPONSE", "expected DECIDE_RESPONSE")
        _require(response["round_no"] == round_no, "decision response round drift")
        _require(
            response["attempt_no"] == self._attempt_no,
            "decision response attempt drift",
        )
        return {
            "host_mutation_performed": False,
            "campaign_action": deepcopy(response["campaign_action"]),
        }


def _game_result(runs_root: Path) -> dict[str, Any]:
    run_dirs = sorted(path for path in runs_root.iterdir() if path.is_dir())
    _require(len(run_dirs) == 1, "expected exactly one pair06 run directory")
    run_dir = run_dirs[0]
    warm = run_dir / "warm-start.jsonl"
    trajectory = run_dir / "trajectory.jsonl"
    summary_path = run_dir / "summary.json"
    for path in (warm, trajectory, summary_path):
        _require(path.is_file() and not path.is_symlink(), f"run artifact missing: {path.name}")

    try:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise Pair06V8ProtoGameChildHold(f"summary JSON invalid: {exc}") from exc
    _require(isinstance(summary, dict), "summary must be object")
    _require(summary.get("seed") == SEED, "summary seed drift")
    _require(summary.get("abaddon_doctrine") == DOCTRINE, "summary doctrine drift")
    _require(summary.get("ticks_per_round") == TICKS_PER_ROUND, "summary tick bound drift")
    rounds_completed = summary.get("rounds_completed")
    _require(
        type(rounds_completed) is int and 0 <= rounds_completed <= ROUNDS,
        "summary rounds_completed invalid",
    )
    return {
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "seed": SEED,
        "doctrine": DOCTRINE,
        "rounds_limit": ROUNDS,
        "ticks_per_round": TICKS_PER_ROUND,
        "starter_infantry": STARTER_INFANTRY,
        "staging_max_ticks": STAGING_MAX_TICKS,
        "run_id": run_dir.name,
        "run_dir": str(run_dir),
        "warm_start_sha256": _sha256_file(warm),
        "trajectory_sha256": _sha256_file(trajectory),
        "summary_sha256": _sha256_file(summary_path),
        "summary": deepcopy(summary),
        "legacy_ollama_started": False,
        "legacy_ollama_contacted": False,
        "game_execution_performed": True,
        "game_cleanup_completed": True,
        "candidate_execution_performed": False,
        "held_out_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "automatic_retry": False,
    }


def run_pair06_v8_proto_game_child(
    *,
    sock: Any,
    attempt_id: str,
    runs_root: str,
    frozen_source_root: str,
    exact_engine_root: str,
    execution_authorized: bool,
) -> dict[str, Any]:
    """Run the exact pair-06 baseline legacy game in an already-spawned child."""
    _dependencies()
    _require(execution_authorized is True, "PAIR06_V8_CHILD_GAME_EXECUTION_AUTHORIZATION_REQUIRED")
    _require(
        Path(sys.executable).resolve() == PROTO_PYTHON.resolve(),
        "pair06 child must use accepted proto Python",
    )
    _require(os.getpid() == os.getpgrp(), "pair06 child must lead private process group")

    runs = Path(runs_root)
    _require(runs.is_dir() and not runs.is_symlink(), "runs_root must pre-exist as real directory")
    _require(not any(runs.iterdir()), "runs_root must begin empty")

    hello = ipc.recv_message(
        sock,
        direction="parent_to_child",
        expected_seq=1,
        expected_attempt_id=attempt_id,
    )
    _require(hello["type"] == "HELLO", "pair06 child expected HELLO")

    ipc.send_message(
        sock,
        {
            "type": "READY",
            "seq": 1,
            "protocol_version": 1,
            "pair_slot": PAIR_SLOT,
            "arm": ARM,
            "attempt_id": attempt_id,
            "child_pid": os.getpid(),
            "child_pgid": os.getpgrp(),
        },
        direction="child_to_parent",
        expected_seq=1,
        expected_attempt_id=attempt_id,
    )

    legacy = _load_exact_legacy()
    original_runs_dir = legacy.RUNS_DIR
    old_argv = sys.argv
    hooks = Pair06V8ProtoChildHooks(legacy, sock, attempt_id)

    try:
        legacy.RUNS_DIR = runs
        with portable_checkout.PortableRunnerBinding(
            legacy,
            frozen_source_root=Path(frozen_source_root),
            exact_engine_root=Path(exact_engine_root),
        ):
            hooks.install()
            try:
                sys.argv = [
                    str(LEGACY_RUNNER),
                    "--seed", str(SEED),
                    "--doctrine", DOCTRINE,
                    "--rounds", str(ROUNDS),
                    "--ticks-per-round", str(TICKS_PER_ROUND),
                    "--starter-infantry", str(STARTER_INFANTRY),
                    "--staging-max-ticks", str(STAGING_MAX_TICKS),
                ]
                legacy.main()
            finally:
                hooks.restore()
                sys.argv = old_argv
        result = _game_result(runs)
        _require(
            hooks.legacy_ollama_start_calls == 1,
            "legacy handoff did not reach inert start_ollama exactly once",
        )
        _require(
            hooks.legacy_ollama_cleanup_calls == 1,
            "legacy cleanup did not reach inert cleanup exactly once",
        )
        ipc.send_message(
            sock,
            {
                "type": "GAME_RESULT",
                "seq": hooks.next_child_send_seq,
                "protocol_version": 1,
                "pair_slot": PAIR_SLOT,
                "arm": ARM,
                "attempt_id": attempt_id,
                "result": deepcopy(result),
            },
            direction="child_to_parent",
            expected_seq=hooks.next_child_send_seq,
            expected_attempt_id=attempt_id,
        )
        return result
    except BaseException as exc:
        try:
            ipc.send_message(
                sock,
                {
                    "type": "ERROR",
                    "seq": hooks.next_child_send_seq,
                    "protocol_version": 1,
                    "pair_slot": PAIR_SLOT,
                    "arm": ARM,
                    "attempt_id": attempt_id,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc)[:2048],
                },
                direction="child_to_parent",
                expected_seq=hooks.next_child_send_seq,
                expected_attempt_id=attempt_id,
            )
        except BaseException:
            pass
        raise
    finally:
        hooks.restore()
        legacy.RUNS_DIR = original_runs_dir
        sys.argv = old_argv


def pair06_v8_proto_game_child_contract() -> dict[str, Any]:
    dependencies = _dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "ipc_review_git_blob": IPC_REVIEW_GIT_BLOB,
        "ipc_review_source_sha256": IPC_REVIEW_SOURCE_SHA256,
        "decision_review_git_blob": DECISION_REVIEW_GIT_BLOB,
        "decision_review_source_sha256": DECISION_REVIEW_SOURCE_SHA256,
        "portable_checkout_git_blob": PORTABLE_CHECKOUT_GIT_BLOB,
        "portable_checkout_source_sha256": PORTABLE_CHECKOUT_SOURCE_SHA256,
        "pair06_v8_proto_game_child_implemented": True,
        "pair06_v8_proto_game_child_reviewed": False,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "doctrine": DOCTRINE,
        "seed": SEED,
        "rounds": ROUNDS,
        "ticks_per_round": TICKS_PER_ROUND,
        "starter_infantry": STARTER_INFANTRY,
        "staging_max_ticks": STAGING_MAX_TICKS,
        "proto_python": str(PROTO_PYTHON),
        "legacy_runner": str(LEGACY_RUNNER),
        "legacy_runner_sha256": LEGACY_RUNNER_SHA256,
        "hello_ready_handshake_implemented": True,
        "ipc_decision_loop_implemented": True,
        "reviewed_decision_hook_reused": True,
        "legacy_start_ollama_replaced_in_memory": True,
        "legacy_cleanup_replaced_in_memory": True,
        "legacy_ollama_service_start_performed": False,
        "legacy_ollama_network_contact_performed": False,
        "portable_frozen_worktree_binding_implemented": True,
        "isolated_runs_root_required": True,
        "game_result_hashing_implemented": True,
        "error_terminal_implemented": True,
        "socketpair_creation_implemented_by_this_source": False,
        "child_spawn_implemented_by_this_source": False,
        "worktree_materialization_implemented_by_this_source": False,
        "durable_attempt_claim_implemented_by_this_source": False,
        "v8_model_load_implemented_by_this_source": False,
        "v8_model_inference_implemented_by_this_source": False,
        "game_execution_authorized": False,
        "subprocess_spawn_authorized": False,
        "automatic_retry": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "dependencies": dependencies,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def spawn_child(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8ProtoGameChildHold(NEXT_GATE)
