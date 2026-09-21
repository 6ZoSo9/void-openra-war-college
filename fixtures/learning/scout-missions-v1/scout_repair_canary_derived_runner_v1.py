#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import socket
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

from openra_env.learning.abaddon_scout_repair_canary_runner_adapter_v1 import (
    DeterministicCanaryOpponentAdapter,
)

HOME = Path.home()
DOWNLOADS = HOME / "Downloads"
DOJO = HOME / "dev" / "void-apollyon-dojo"
RL = HOME / "dev" / "openra-rl-war-college"
OPENRA = RL / "OpenRA"

BASE_RUNNER = DOWNLOADS / "void-actual-apollyon-vs-abaddon-joint-sparring-batch-v1_2.py"
BASE_RUNNER_SHA = "c59faac3833ce4bffeb20e3d60625bcb3c63ecc520658660e19a8deefd2db615"

GENERATION = "ad1926569b12466c"
IMAGE = f"void-openra-joint-duel:{GENERATION}"
IMAGE_ID = "sha256:79f2f6800382489a2a648839fc0d58e546384938439378aeea06461363de25f5"
ENGINE_COMMIT = "1607a7a6501d42a47638393ecef8b22831064932"
HISTORICAL_WAR_COLLEGE_COMMIT = "973802ef0a614e5afa782ff20e231e18966ae3e5"
EXPERIMENT_NAMESPACE = "abaddon-scout-repair-canary-v1"
CANARY_SEED = 1100292357
NEXT_GATE = "SCOUT_REPAIR_CANARY_DERIVED_RUNNER_SOURCE_BINDING_AND_LAUNCHER_REQUIRED"
JOINT_ATTESTATION = DOJO / "provenance" / "joint-duel-training-eligibility-v1.json"
JOINT_ATTESTATION_SHA = "1368c737d0f7acae8aabfa539d5e9f51cd87a987bd2d4a03e0cde32d8d0378dd"

CURRICULUM_ID = "symmetric-contact-warm-start-v1"
RUNS_DIR = DOJO / "war-college" / "joint-duels"

PREFERRED_INFANTRY = ("e1", "e3", "e2", "dog")
INFANTRY_PRODUCTION = ("barr", "tent")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_base():
    if not BASE_RUNNER.is_file():
        raise RuntimeError(f"base joint runner missing: {BASE_RUNNER}")
    actual = sha(BASE_RUNNER)
    if actual != BASE_RUNNER_SHA:
        raise RuntimeError(
            f"base runner hash drift: expected={BASE_RUNNER_SHA} actual={actual}"
        )
    name = "void_actual_joint_spar_v12"
    spec = importlib.util.spec_from_file_location(name, BASE_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import base runner")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Actual Apollyon vs actual Abaddon symmetric combat warm-start curriculum"
    )
    p.add_argument("--seed", type=int, default=CANARY_SEED)
    p.add_argument("--doctrine", default="FEINTER")
    p.add_argument("--rounds", type=int, default=36)
    p.add_argument("--ticks-per-round", type=int, default=25)
    p.add_argument("--starter-infantry", type=int, default=4)
    p.add_argument("--staging-max-ticks", type=int, default=800)
    return p.parse_args(argv)


def find_mcv(state):
    rows = [
        u for u in state["units_summary"]
        if u["type"] in {"mcv", "amcv"}
    ]
    if not rows:
        raise RuntimeError("warm-start MCV missing")
    return sorted(rows, key=lambda x: x["id"])[0]["id"]


def building_count(state, btype):
    return sum(1 for b in state["buildings_summary"] if b["type"] == btype)


def choose_available(state, choices):
    avail = set(state["available_production"])
    for x in choices:
        if x in avail:
            return x
    return ""


def combat_units(state):
    return [u for u in state["units_summary"] if u["can_attack"]]


def visible_count(state):
    return len(state["enemy_summary"]) + len(state["enemy_buildings_summary"])


def military_damage_signature(state):
    m = state["military"]
    return (
        int(m["units_killed"]),
        int(m["units_lost"]),
        int(m["buildings_killed"]),
        int(m["buildings_lost"]),
        int(m["kills_cost"]),
        int(m["deaths_cost"]),
    )


def base_cell(state):
    fact = next(
        (b for b in state["buildings_summary"] if b["type"] == "fact"),
        None,
    )
    if fact is None:
        raise RuntimeError("Construction Yard missing")
    return int(fact["cell_x"]), int(fact["cell_y"])


def append_jsonl(path: Path, row: dict[str, Any]):
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
        f.flush()
        os.fsync(f.fileno())


def reconcile_pending(base, states, pending, label):
    """Clear host-side placement bookkeeping for structures already present.

    The runtime-proven game state is authoritative. A completed building must
    not remain as a synthetic host-side pending reservation and block a later
    controller decision.
    """
    cleared = []
    for player in ("Multi0", "Multi1"):
        for btype in list(pending[player]):
            ent = pending[player][btype]
            baseline = int(ent.get("baseline_count", 0))
            actual = building_count(states[player], btype)
            if actual > baseline:
                pending[player].pop(btype, None)
                cleared.append(
                    {
                        "player": player,
                        "building_type": btype,
                        "baseline_count": baseline,
                        "actual_count": actual,
                    }
                )

    if cleared:
        print(
            f"pending_reconcile={label}:"
            + json.dumps(cleared, sort_keys=True, separators=(",", ":"))
        )
    return cleared


def assert_no_stale_pending(states, pending, label):
    stale = []
    for player in ("Multi0", "Multi1"):
        for btype, ent in pending[player].items():
            baseline = int(ent.get("baseline_count", 0))
            actual = building_count(states[player], btype)
            if actual > baseline:
                stale.append(
                    {
                        "player": player,
                        "building_type": btype,
                        "baseline_count": baseline,
                        "actual_count": actual,
                    }
                )
    if stale:
        raise RuntimeError(
            f"{label}: stale completed pending entries remain: "
            + json.dumps(stale, sort_keys=True)
        )


def host_step(base, stub, pb2, sid, states, ticks, commands, warm_log, label):
    start = states["Multi0"]["tick"]
    if states["Multi1"]["tick"] != start:
        raise RuntimeError("warm-start player tick mismatch")
    resp, obs_by = base.joint_advance(stub, pb2, sid, ticks, commands)
    states = {p: base.state_from_obs(o) for p, o in obs_by.items()}
    append_jsonl(warm_log, {
        "event": "warm_start_step",
        "curriculum_id": CURRICULUM_ID,
        "label": label,
        "start_tick": int(resp.start_tick),
        "end_tick": int(resp.end_tick),
        "commands": {
            p: [
                {
                    "action": int(c.action),
                    "actor_id": int(c.actor_id),
                    "target_actor_id": int(c.target_actor_id),
                    "target_x": int(c.target_x),
                    "target_y": int(c.target_y),
                    "item_type": c.item_type,
                }
                for c in commands.get(p, [])
            ]
            for p in ("Multi0", "Multi1")
        },
        "state": {
            "Multi0": base.compact_state(states["Multi0"]),
            "Multi1": base.compact_state(states["Multi1"]),
        },
        "controller_authored": False,
        "training_candidate": False,
    })
    print(
        f"warm_start={label} tick={resp.start_tick}->{resp.end_tick} "
        f"buildings={states['Multi0']['own_buildings']}/{states['Multi1']['own_buildings']} "
        f"combat={len(combat_units(states['Multi0']))}/{len(combat_units(states['Multi1']))} "
        f"visible={visible_count(states['Multi0'])}/{visible_count(states['Multi1'])}"
    )
    return states


def wait_for(base, stub, pb2, sid, states, warm_log, predicate, label, max_ticks=2000, step=50, pending=None):
    elapsed = 0
    pending = pending or {"Multi0": {}, "Multi1": {}}
    while elapsed < max_ticks:
        if predicate(states):
            reconcile_pending(base, states, pending, f"{label}:success")
            assert_no_stale_pending(states, pending, f"{label}:success")
            return states
        commands = {}
        notes = {}
        for player in ("Multi0", "Multi1"):
            cmds, ns = base.placement_commands(
                player, states[player], pending[player], pb2
            )
            commands[player] = cmds
            notes[player] = ns
        states = host_step(
            base, stub, pb2, sid, states, step, commands, warm_log,
            f"{label}:{elapsed+step}"
        )
        if any(notes.values()):
            append_jsonl(warm_log, {
                "event": "warm_start_placement_notes",
                "label": label,
                "tick": states["Multi0"]["tick"],
                "notes": notes,
                "controller_authored": False,
                "training_candidate": False,
            })
        elapsed += step
    raise RuntimeError(f"warm-start timeout waiting for {label}")


def queue_structure(base, stub, pb2, sid, states, warm_log, pending, choices, label):
    selected = {}
    commands = {}
    for player in ("Multi0", "Multi1"):
        btype = choose_available(states[player], choices)
        if not btype:
            raise RuntimeError(
                f"{label}: no available structure for {player}; "
                f"available={states[player]['available_production']}"
            )
        selected[player] = btype
        baseline = building_count(states[player], btype)
        pending[player][btype] = {
            "baseline_count": baseline,
            "attempt": 0,
            "cell_x": 0,
            "cell_y": 0,
        }
        commands[player] = [pb2.Command(action=pb2.BUILD, item_type=btype)]

    states = host_step(
        base, stub, pb2, sid, states, 50, commands, warm_log,
        f"queue_{label}"
    )

    def done(s):
        return all(
            building_count(s[player], selected[player]) >
            pending[player].get(selected[player], {"baseline_count": -1})["baseline_count"]
            if selected[player] in pending[player]
            else building_count(s[player], selected[player]) >= 1
            for player in ("Multi0", "Multi1")
        )

    # Use explicit initial baselines because the pending entry disappears after confirmation.
    baselines = {
        p: building_count(states[p], selected[p]) - (
            1 if building_count(states[p], selected[p]) > 0
            and selected[p] not in pending[p] else 0
        )
        for p in ("Multi0", "Multi1")
    }
    # Correct baselines from pre-queue state are zero for first copies in this curriculum.
    # For robustness, use target counts captured from pending when still present.
    targets = {}
    for p in ("Multi0", "Multi1"):
        ent = pending[p].get(selected[p])
        targets[p] = (ent["baseline_count"] + 1) if ent else max(1, building_count(states[p], selected[p]))

    states = wait_for(
        base, stub, pb2, sid, states, warm_log,
        lambda s: all(building_count(s[p], selected[p]) >= targets[p] for p in ("Multi0", "Multi1")),
        f"place_{label}",
        max_ticks=2200,
        step=50,
        pending=pending,
    )
    print(f"warm_structure_{label}={selected}")
    return states, selected


def queue_infantry(base, stub, pb2, sid, states, warm_log, count):
    types = {}
    commands = {}
    baseline_combat = {
        p: len(combat_units(states[p])) for p in ("Multi0", "Multi1")
    }
    for player in ("Multi0", "Multi1"):
        unit = choose_available(states[player], PREFERRED_INFANTRY)
        if not unit:
            candidates = [
                x for x in states[player]["available_production"]
                if x not in base.BUILDING_TYPES
            ]
            if not candidates:
                raise RuntimeError(
                    f"no trainable starter unit for {player}: "
                    f"{states[player]['available_production']}"
                )
            unit = sorted(candidates)[0]
        types[player] = unit
        commands[player] = [
            pb2.Command(action=pb2.TRAIN, item_type=unit)
            for _ in range(count)
        ]

    states = host_step(
        base, stub, pb2, sid, states, 25, commands, warm_log,
        "queue_starter_infantry"
    )
    states = wait_for(
        base, stub, pb2, sid, states, warm_log,
        lambda s: all(
            len(combat_units(s[p])) >= baseline_combat[p] + count
            for p in ("Multi0", "Multi1")
        ),
        "train_starter_infantry",
        max_ticks=1800,
        step=25,
    )
    print(f"starter_infantry_types={types}")
    return states, types


def stage_to_contact(base, stub, pb2, sid, states, warm_log, max_ticks):
    before_damage = {
        p: military_damage_signature(states[p]) for p in ("Multi0", "Multi1")
    }

    commands = {}
    targets = {}
    for player in ("Multi0", "Multi1"):
        units = combat_units(states[player])
        if not units:
            raise RuntimeError(f"no combat units to stage for {player}")
        bx, by = base_cell(states[player])
        w = int(states[player]["map"]["width"])
        h = int(states[player]["map"]["height"])
        cx, cy = w // 2, h // 2
        # Move 70% from base toward map center. If contact is still absent,
        # a later host step moves the same squad to center.
        tx = round(bx + 0.70 * (cx - bx))
        ty = round(by + 0.70 * (cy - by))
        targets[player] = (tx, ty)
        commands[player] = [
            pb2.Command(
                action=pb2.MOVE,
                actor_id=int(u["id"]),
                target_x=tx,
                target_y=ty,
            )
            for u in units
        ]

    states = host_step(
        base, stub, pb2, sid, states, 25, commands, warm_log,
        "stage_squads_toward_center"
    )

    elapsed = 25
    center_commands_sent = False
    while elapsed < max_ticks:
        if visible_count(states["Multi0"]) > 0 or visible_count(states["Multi1"]) > 0:
            break

        commands = {"Multi0": [], "Multi1": []}
        if elapsed >= max_ticks // 2 and not center_commands_sent:
            for player in ("Multi0", "Multi1"):
                w = int(states[player]["map"]["width"])
                h = int(states[player]["map"]["height"])
                commands[player] = [
                    pb2.Command(
                        action=pb2.MOVE,
                        actor_id=int(u["id"]),
                        target_x=w // 2,
                        target_y=h // 2,
                    )
                    for u in combat_units(states[player])
                ]
            center_commands_sent = True
            label = "stage_squads_to_center"
        else:
            label = "stage_advance"

        states = host_step(
            base, stub, pb2, sid, states, 25, commands, warm_log, label
        )
        elapsed += 25

    after_damage = {
        p: military_damage_signature(states[p]) for p in ("Multi0", "Multi1")
    }
    if after_damage != before_damage:
        raise RuntimeError(
            "warm-start staging caused combat before controller handoff; "
            f"before={before_damage} after={after_damage}"
        )

    contact = {
        "tick": states["Multi0"]["tick"],
        "Multi0_visible": visible_count(states["Multi0"]),
        "Multi1_visible": visible_count(states["Multi1"]),
        "staging_ticks": elapsed,
        "contact_achieved": (
            visible_count(states["Multi0"]) > 0
            or visible_count(states["Multi1"]) > 0
        ),
    }
    print("warm_start_handoff=" + json.dumps(contact, sort_keys=True))
    return states, contact



def _safe_tool_suffix(value):
    return "".join(ch if ch.isalnum() else "_" for ch in str(value))


# These are production entries exposed by the RA rules but not supported by
# the current host-side structure placement contract. They must never leak
# into the unit-training surface merely because the base runner's compact
# BUILDING_TYPES set does not classify them.
PRODUCTION_NONUNIT_BLOCKLIST = {"brik", "fenc", "sbag", "kenn"}

# Naval structures are mechanically valid structures, but this warm-start
# curriculum has no terrain-aware host placement proof for them. Exclude them
# rather than create a placement-dependent contamination source.
WARMSTART_UNSUPPORTED_STRUCTURES = {"spen", "syrd"}


def apollyon_tools_typed(base, state, pending):
    """Expose production choices as distinct functions, not enum arguments.

    Ollama may ignore JSON enum constraints inside tool arguments. A production
    choice is therefore represented by the function identity itself:
      build_structure_powr()
      train_unit_e1(count=...)
    Pending/queued structures simply have no function in this decision.
    """
    original = base.apollyon_tools(state)

    pending_types = set(pending)
    queued_structure_types = {
        str(p.get("item", ""))
        for p in state.get("production", [])
        if p.get("queue_type") in {"Building", "Defense"}
    }

    generic_build_choices = []
    generic_unit_choices = []
    retained = []

    for tool in original:
        fn = tool.get("function", {})
        name = fn.get("name")
        if name == "build_and_place":
            generic_build_choices = list(
                fn.get("parameters", {})
                .get("properties", {})
                .get("building_type", {})
                .get("enum", [])
            )
            continue
        if name == "build_unit":
            generic_unit_choices = list(
                fn.get("parameters", {})
                .get("properties", {})
                .get("unit_type", {})
                .get("enum", [])
            )
            continue
        retained.append(tool)

    legal_buildings = sorted(
        b for b in generic_build_choices
        if b not in pending_types
        and b not in queued_structure_types
        and b not in WARMSTART_UNSUPPORTED_STRUCTURES
    )

    legal_units = sorted(
        u for u in generic_unit_choices
        if u not in PRODUCTION_NONUNIT_BLOCKLIST
    )

    function_to_action = {}

    for btype in legal_buildings:
        fname = f"build_structure_{_safe_tool_suffix(btype)}"
        function_to_action[fname] = {
            "kind": "build_and_place",
            "building_type": btype,
        }
        retained.append({
            "type": "function",
            "function": {
                "name": fname,
                "description": (
                    f"Queue the currently legal structure '{btype}'. "
                    "Host performs deterministic placement when construction completes."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False,
                },
            },
        })

    for utype in legal_units:
        fname = f"train_unit_{_safe_tool_suffix(utype)}"
        function_to_action[fname] = {
            "kind": "build_unit",
            "unit_type": utype,
        }
        retained.append({
            "type": "function",
            "function": {
                "name": fname,
                "description": (
                    f"Queue one to three currently legal '{utype}' units."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "count": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 3,
                        },
                    },
                    "additionalProperties": False,
                },
            },
        })

    offered_names = {
        t.get("function", {}).get("name", "")
        for t in retained
    }
    if "build_and_place" in offered_names or "build_unit" in offered_names:
        raise RuntimeError("generic enum-dependent production tool leaked")

    contract = {
        "production_contract_version": "typed-production-functions-v1",
        "pending_buildings": sorted(pending_types),
        "queued_structure_buildings": sorted(queued_structure_types),
        "unsupported_structures": sorted(WARMSTART_UNSUPPORTED_STRUCTURES),
        "nonunit_blocklist": sorted(PRODUCTION_NONUNIT_BLOCKLIST),
        "legal_buildings": legal_buildings,
        "legal_units": legal_units,
        "production_functions": dict(sorted(function_to_action.items())),
        "offered_tool_names": sorted(x for x in offered_names if x),
    }

    return retained, contract


def decision_to_commands_typed(
    base,
    name,
    args,
    state,
    pending,
    pb2,
    contract,
):
    """Translate typed production function identity into the base host command."""
    action = (contract.get("production_functions") or {}).get(name)
    if action:
        if action["kind"] == "build_and_place":
            if args not in ({}, None):
                # Zero-argument structure tools must not smuggle a different type.
                unexpected = {
                    k: v for k, v in (args or {}).items()
                    if k not in ()
                }
                if unexpected:
                    return False, "typed_structure_tool_unexpected_arguments", []
            return base.decision_to_commands(
                "build_and_place",
                {"building_type": action["building_type"]},
                state,
                pending,
                pb2,
            )

        if action["kind"] == "build_unit":
            count = int((args or {}).get("count", 1) or 1)
            return base.decision_to_commands(
                "build_unit",
                {
                    "unit_type": action["unit_type"],
                    "count": count,
                },
                state,
                pending,
                pb2,
            )

        return False, f"unknown_typed_production_kind:{action['kind']}", []

    # All non-production tools retain the reviewed base conversion.
    return base.decision_to_commands(
        name,
        args,
        state,
        pending,
        pb2,
    )


def deterministic_canary_decision(
    adapter,
    base,
    state,
    pending,
    pb2,
    doctrine,
    round_no,
):
    """Delegate exactly once to the reviewed non-model canary opponent adapter."""
    if not isinstance(adapter, DeterministicCanaryOpponentAdapter):
        raise RuntimeError("reviewed deterministic canary adapter required")
    return adapter.decide(
        base,
        None,
        state,
        pending,
        pb2,
        doctrine,
        round_no,
    )


def run_bound_canary(
    *,
    launcher_authorized: bool,
    accepted_war_college_commit: str,
    argv=None,
):
    if launcher_authorized is not True:
        raise RuntimeError(NEXT_GATE)
    if (
        type(accepted_war_college_commit) is not str
        or len(accepted_war_college_commit) != 40
        or any(c not in "0123456789abcdef" for c in accepted_war_college_commit)
    ):
        raise RuntimeError("accepted War College commit must be lowercase 40-hex")
    args = parse_args(argv)
    if args.doctrine != "FEINTER":
        raise RuntimeError("canary doctrine must be exact FEINTER")
    if args.seed != CANARY_SEED:
        raise RuntimeError("canary seed drift")
    if args.rounds < 1 or args.rounds > 200:
        raise RuntimeError("--rounds must be 1..200")
    if args.ticks_per_round < 1 or args.ticks_per_round > 100:
        raise RuntimeError("--ticks-per-round must be 1..100")
    if args.starter_infantry < 2 or args.starter_infantry > 8:
        raise RuntimeError("--starter-infantry must be 2..8")

    print("=== VOID SCOUT-REPAIR CANARY DERIVED RUNNER V1 ===")
    print(f"curriculum_id={CURRICULUM_ID}")
    print("actual_apollyon=false")
    print("deterministic_non_model_opponent=true")
    print("actual_abaddon=true")
    print("proxy_bot=false")
    print("warm_start_scripted=true")
    print("warm_start_symmetric=true")
    print("warm_start_uses_game_legal_commands=true")
    print("warm_start_rows_training_candidate=false")
    print("controller_rows_training_candidate=false")
    print("completed_placement_pending_reconciliation=true")
    print("controller_handoff_requires_empty_pending=true")
    print("apollyon_production_tools_typed_by_function_identity=true")
    print("generic_build_and_place_tool_absent=true")
    print("generic_build_unit_tool_absent=true")
    print("pending_or_queued_structure_function_absent=true")
    print("unsupported_wall_and_kennel_unit_leak_blocked=true")
    print("concrete_stale_tool_examples_removed=true")
    print("current_allowed_tool_names_explicit_each_round=true")
    print("protocol_invalid_output_never_becomes_advance=true")
    print("automatic_opponent_retry=false")
    print("rejected_deterministic_proposal_aborts_bout=true")
    print(f"generation_id={GENERATION}")
    print(f"seed={args.seed}")
    print(f"abaddon_doctrine={args.doctrine}")
    print(f"round_limit={args.rounds}")
    print(f"ticks_per_round={args.ticks_per_round}")
    print("automatic_corpus_admission=false")
    print("automatic_apollyon_weight_mutation=false")
    print("automatic_abaddon_policy_promotion=false")
    print("git_mutation=false")
    print("void_chain_mutation=false")
    print("wallet_or_funds_action=false")
    print("fail_closed=true")

    base = load_base()
    print("base_joint_runner_hash_green=true")

    # Reuse all exact baseline/provenance checks from the known runner.
    if socket.gethostname() != base.HOST:
        raise RuntimeError(f"run on {base.HOST}")
    if Path(sys.executable).resolve() != base.PROTO_PY.resolve():
        raise RuntimeError(f"run with {base.PROTO_PY}")
    if base.out(["git", "rev-parse", "HEAD"], cwd=OPENRA) != ENGINE_COMMIT:
        raise RuntimeError("OpenRA not at frozen commit")
    if base.out(["git", "rev-parse", "HEAD"], cwd=RL) != accepted_war_college_commit:
        raise RuntimeError("War College not at accepted canary commit")
    if base.out(["git", "status", "--porcelain", "--untracked-files=no"], cwd=OPENRA):
        raise RuntimeError("OpenRA tracked worktree dirty")
    if base.out(["git", "status", "--porcelain", "--untracked-files=no"], cwd=RL):
        raise RuntimeError("War College tracked worktree dirty")
    base.verify_runtime_report()
    if base.out(["docker", "image", "inspect", "-f", "{{.Id}}", IMAGE]) != IMAGE_ID:
        raise RuntimeError("runtime image identity drift")
    if base.out(["docker", "context", "show"]) != "rootless":
        raise RuntimeError("rootless Docker context required")
    base.exact_file(base.ABADDON_CONTROLLER, base.ABADDON_CONTROLLER_SHA, "Abaddon controller")
    base.exact_file(
        JOINT_ATTESTATION,
        JOINT_ATTESTATION_SHA,
        "historical joint runtime attestation reference",
    )
    print("historical_runtime_boundary_reference_green=true")

    canary_opponent = DeterministicCanaryOpponentAdapter(
        tool_contract_builder=apollyon_tools_typed,
        typed_host_validator=decision_to_commands_typed,
    )
    opponent_source = canary_opponent.review_snapshot()["opponent_source_identity"]
    if (
        type(opponent_source) is not dict
        or type(opponent_source.get("sha256")) is not str
        or len(opponent_source["sha256"]) != 64
    ):
        raise RuntimeError("deterministic opponent source identity missing")
    print(f"deterministic_opponent_source_sha256={opponent_source['sha256']}")
    print("model_helper_loaded=false")
    print("model_service_preflight_delegated_to_reviewed_launcher=true")

    abaddon_mod = base.load_module(base.ABADDON_CONTROLLER, "void_abaddon_warmstart")
    controller = abaddon_mod.AbaddonController(
        doctrine=args.doctrine,
        seed=args.seed,
    )
    print("actual_abaddon_controller_loaded=true")

    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    run_id = (
        f"scout-repair-canary-{stamp}-"
        f"{args.doctrine.lower()}-s{args.seed}"
    )
    run_dir = RUNS_DIR / run_id
    if run_dir.exists():
        raise RuntimeError(f"run dir collision: {run_dir}")
    run_dir.mkdir(parents=True)
    warm_log = run_dir / "warm-start.jsonl"
    traj = run_dir / "trajectory.jsonl"
    summary_path = run_dir / "summary.json"
    runner_sha = sha(Path(__file__))

    append_jsonl(warm_log, {
        "event": "warm_start_header",
        "run_id": run_id,
        "curriculum_id": CURRICULUM_ID,
        "generation_id": GENERATION,
        "runner_sha256": runner_sha,
        "base_runner_sha256": BASE_RUNNER_SHA,
        "joint_training_attestation_sha256": JOINT_ATTESTATION_SHA,
        "seed": args.seed,
        "controller_authored": False,
        "training_candidate": False,
    })

    import grpc
    container_name = f"void-warmstart-spar-{os.getpid()}"
    port = base.free_port()
    channel = None
    stub = None
    sid = ""
    destroyed = False
    pending = {"Multi0": {}, "Multi1": {}}
    completed_rounds = 0
    winner = ""
    status = "unfinished"

    with tempfile.TemporaryDirectory(prefix="void-warmstart-spar.") as td:
        pb2, pb2_grpc = base.generate_proto(Path(td))
        try:
            base.run([
                "docker", "run", "-d", "--rm",
                "--name", container_name,
                "-p", f"127.0.0.1:{port}:9999",
                IMAGE,
            ], quiet=True)
            print(f"engine_loopback_grpc_port={port}")
            print("engine_container_started=true")

            channel = grpc.insecure_channel(
                f"127.0.0.1:{port}",
                options=[
                    ("grpc.max_receive_message_length", 64 * 1024 * 1024),
                    ("grpc.max_send_message_length", 16 * 1024 * 1024),
                ],
            )
            stub = pb2_grpc.RLBridgeStub(channel)
            base.wait_daemon(stub, pb2, container_name)
            print("engine_daemon_ready=true")

            created = stub.CreateSession(
                pb2.CreateSessionRequest(
                    map_name="singles.oramap",
                    bots="Multi0:rl-agent,Multi1:rl-agent",
                    seed=args.seed,
                ),
                timeout=30.0,
            )
            sid = created.session_id
            base.wait_players(stub, pb2, sid)
            print(f"session_id={sid}")

            _, obs_by = base.joint_advance(
                stub, pb2, sid, 1, {"Multi0": [], "Multi1": []}
            )
            states = {p: base.state_from_obs(o) for p, o in obs_by.items()}
            print(f"warm_start_initial_tick={states['Multi0']['tick']}")

            # 1) Symmetric legal MCV deployment.
            deploy_cmds = {}
            for p in ("Multi0", "Multi1"):
                deploy_cmds[p] = [
                    pb2.Command(action=pb2.DEPLOY, actor_id=find_mcv(states[p]))
                ]
            states = host_step(
                base, stub, pb2, sid, states, 50, deploy_cmds, warm_log,
                "deploy_mcv"
            )
            states = wait_for(
                base, stub, pb2, sid, states, warm_log,
                lambda s: all(building_count(s[p], "fact") >= 1 for p in ("Multi0", "Multi1")),
                "construction_yard",
                max_ticks=500,
                step=25,
                pending=pending,
            )
            print("warm_start_fact_green=true")

            # 2) Symmetric baseline economy.
            states, _ = queue_structure(
                base, stub, pb2, sid, states, warm_log, pending,
                ("powr", "apwr"), "power"
            )
            states, _ = queue_structure(
                base, stub, pb2, sid, states, warm_log, pending,
                ("proc",), "refinery"
            )
            states = wait_for(
                base, stub, pb2, sid, states, warm_log,
                lambda s: all(
                    int(s[p]["economy"]["harvester_count"]) >= 1
                    for p in ("Multi0", "Multi1")
                ),
                "harvester_spawn",
                max_ticks=600,
                step=25,
                pending=pending,
            )
            print("warm_start_economy_green=true")

            # 3) Symmetric infantry production and starter squads.
            states, prod_types = queue_structure(
                base, stub, pb2, sid, states, warm_log, pending,
                INFANTRY_PRODUCTION, "infantry_production"
            )
            states, unit_types = queue_infantry(
                base, stub, pb2, sid, states, warm_log,
                args.starter_infantry
            )
            print("warm_start_starter_armies_green=true")

            # 4) Stage squads toward center until first visual contact, with no
            # host-authored combat orders and zero warm-start combat allowed.
            states, handoff = stage_to_contact(
                base, stub, pb2, sid, states, warm_log, args.staging_max_ticks
            )

            warm_sha = sha(warm_log)
            print(f"warm_start_sha256={warm_sha}")
            print("warm_start_complete=true")

            reconciled_at_handoff = reconcile_pending(
                base, states, pending, "controller_handoff"
            )
            assert_no_stale_pending(
                states, pending, "controller_handoff"
            )
            if pending["Multi0"] or pending["Multi1"]:
                raise RuntimeError(
                    "warm-start handoff requires empty host pending state; "
                    f"Multi0={pending['Multi0']} Multi1={pending['Multi1']}"
                )
            print(
                f"warm_start_handoff_pending_reconciled="
                f"{len(reconciled_at_handoff)}"
            )
            print("warm_start_handoff_pending_empty=true")
            print("controller_handoff_now=true")

            # The canary opponent is deterministic and non-model. Service state is
            # independently checked by the reviewed launcher/backend, never mutated here.
            print("model_service_start_performed=false")
            print("model_inference_performed=false")

            append_jsonl(traj, {
                "event": "run_header",
                "run_id": run_id,
                "curriculum_id": CURRICULUM_ID,
                "generation_id": GENERATION,
                "runtime_image_id": IMAGE_ID,
                "engine_commit": ENGINE_COMMIT,
                "war_college_commit": accepted_war_college_commit,
                "joint_training_attestation_sha256": JOINT_ATTESTATION_SHA,
                "warm_start_sha256": warm_sha,
                "warm_start_handoff": handoff,
                "experiment_namespace": EXPERIMENT_NAMESPACE,
                "opponent_source_sha256": opponent_source["sha256"],
                "opponent_model_backed": False,
                "abaddon_controller_sha256": base.ABADDON_CONTROLLER_SHA,
                "abaddon_doctrine": args.doctrine,
                "seed": args.seed,
                "round_limit": args.rounds,
                "ticks_per_round": args.ticks_per_round,
                "candidate_only": True,
                "review_required": True,
                "agent_training_rows_begin_here": False,
                "controller_rows_training_candidate": False,
            })

            for round_no in range(1, args.rounds + 1):
                start_tick = states["Multi0"]["tick"]
                if states["Multi1"]["tick"] != start_tick:
                    raise RuntimeError("controller handoff tick disagreement")

                reconcile_pending(
                    base, states, pending, f"controller_round_{round_no}"
                )
                assert_no_stale_pending(
                    states, pending, f"controller_round_{round_no}"
                )

                mech = {}
                placement_notes = {}
                for p in ("Multi0", "Multi1"):
                    mech[p], placement_notes[p] = base.placement_commands(
                        p, states[p], pending[p], pb2
                    )

                (
                    a_name,
                    a_args,
                    a_cmds,
                    a_attempts,
                    a_tool_contract,
                ) = deterministic_canary_decision(
                    canary_opponent,
                    base,
                    states["Multi0"],
                    pending["Multi0"],
                    pb2,
                    args.doctrine,
                    round_no,
                )

                if a_name not in set(a_tool_contract["offered_tool_names"]):
                    raise RuntimeError(
                        f"accepted Apollyon tool was not offered: {a_name}"
                    )
                print(
                    f"apollyon_tool_contract_round={round_no} "
                    f"accepted={a_name} "
                    f"attempts={len(a_attempts)} "
                    f"offered_count={len(a_tool_contract['offered_tool_names'])}"
                )

                ab_decision = controller.decide(states["Multi1"])
                ab_action = ab_decision.get("action") or {}
                b_name = str(ab_action.get("tool", "advance"))
                b_args = ab_action.get("arguments") or {}
                b_ok, b_reason, b_cmds = base.decision_to_commands(
                    b_name, b_args, states["Multi1"], pending["Multi1"], pb2
                )
                if not b_ok:
                    b_cmds = []

                commands = {
                    "Multi0": mech["Multi0"] + a_cmds,
                    "Multi1": mech["Multi1"] + b_cmds,
                }

                append_jsonl(traj, {
                    "event": "joint_decision",
                    "run_id": run_id,
                    "curriculum_id": CURRICULUM_ID,
                    "round": round_no,
                    "start_tick": start_tick,
                    "apollyon_state": base.compact_state(states["Multi0"]),
                    "abaddon_state": base.compact_state(states["Multi1"]),
                    "deterministic_opponent": {
                        "tool": a_name,
                        "arguments": a_args,
                        "attempts": a_attempts,
                        "command_count": len(a_cmds),
                        "tool_contract": a_tool_contract,
                    },
                    "abaddon": {
                        "decision": ab_decision,
                        "accepted": b_ok,
                        "host_reason": b_reason,
                        "command_count": len(b_cmds),
                    },
                    "mechanical_placement": placement_notes,
                    "controller_authored": True,
                    "training_candidate": False,
                    "canary_only": True,
                    "candidate_only": True,
                })

                resp, obs_by = base.joint_advance(
                    stub, pb2, sid, args.ticks_per_round, commands
                )
                states = {p: base.state_from_obs(o) for p, o in obs_by.items()}
                completed_rounds = round_no

                gs = stub.GetState(
                    pb2.StateRequest(session_id=sid, player="Multi0"),
                    timeout=3.0,
                )
                winner = gs.winner or ""
                phase = gs.phase or ""

                append_jsonl(traj, {
                    "event": "joint_result",
                    "run_id": run_id,
                    "curriculum_id": CURRICULUM_ID,
                    "round": round_no,
                    "start_tick": int(resp.start_tick),
                    "end_tick": int(resp.end_tick),
                    "phase": phase,
                    "winner": winner,
                    "apollyon_after": base.compact_state(states["Multi0"]),
                    "abaddon_after": base.compact_state(states["Multi1"]),
                    "controller_authored": True,
                    "training_candidate": False,
                    "canary_only": True,
                    "candidate_only": True,
                })

                print(
                    f"combat_round={round_no} tick={resp.start_tick}->{resp.end_tick} "
                    f"deterministic_opponent={a_name} abaddon={b_name} "
                    f"ap_legal_builds={','.join(a_tool_contract['legal_buildings']) or '-'} "
                    f"visible={visible_count(states['Multi0'])}/"
                    f"{visible_count(states['Multi1'])} "
                    f"combat={len(combat_units(states['Multi0']))}/"
                    f"{len(combat_units(states['Multi1']))} "
                    f"kills={states['Multi0']['military']['kills_cost']}/"
                    f"{states['Multi1']['military']['kills_cost']} "
                    f"phase={phase or 'playing'} winner={winner or '-'}"
                )

                if phase == "game_over" or states["Multi0"]["done"] or states["Multi1"]["done"]:
                    status = "game_over"
                    break

            if status != "game_over":
                status = "round_limit"

            outcome = (
                "APOLLYON_WIN" if winner == "Multi0"
                else "ABADDON_WIN" if winner == "Multi1"
                else "DRAW_OR_UNFINISHED"
            )

            traj_sha = sha(traj)
            summary = {
                "schema": "void.abaddon.scout-repair-canary-runner-summary.v1",
                "experiment_namespace": EXPERIMENT_NAMESPACE,
                "run_id": run_id,
                "curriculum_id": CURRICULUM_ID,
                "generation_id": GENERATION,
                "runtime_image_id": IMAGE_ID,
                "warm_start_sha256": warm_sha,
                "warm_start_handoff": handoff,
                "trajectory_sha256": traj_sha,
                "seed": args.seed,
                "abaddon_doctrine": args.doctrine,
                "rounds_completed": completed_rounds,
                "ticks_per_round": args.ticks_per_round,
                "final_tick": states["Multi0"]["tick"],
                "status": status,
                "winner": winner,
                "outcome": outcome,
                "deterministic_opponent_final": base.compact_state(states["Multi0"]),
                "abaddon_final": base.compact_state(states["Multi1"]),
                "candidate_only": True,
                "warm_start_rows_training_candidate": False,
                "controller_rows_training_candidate": False,
                "opponent_source_sha256": opponent_source["sha256"],
                "opponent_model_backed": False,
                "independent_post_run_dormancy_verified": False,
                "automatic_corpus_admission": False,
                "automatic_apollyon_weight_mutation": False,
                "automatic_abaddon_policy_promotion": False,
            }
            summary_path.write_text(
                json.dumps(summary, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

            print("=== WARM-START SPAR VERDICT ===")
            print(f"run_id={run_id}")
            print(f"warm_start_handoff_tick={handoff['tick']}")
            print(f"warm_start_contact_achieved={str(handoff['contact_achieved']).lower()}")
            print(f"rounds_completed={completed_rounds}")
            print(f"final_tick={states['Multi0']['tick']}")
            print(f"outcome={outcome}")
            print(f"trajectory_sha256={traj_sha}")
            print(f"summary_sha256={sha(summary_path)}")
            print(f"run_dir={run_dir}")
            print("deterministic_opponent_vs_actual_abaddon=true")
            print("controller_rows_joint_same_tick=true")
            print("warm_start_rows_excluded_from_agent_training=true")
            print("candidate_only=true")
            print("automatic_corpus_admission=false")
            print("automatic_apollyon_weight_mutation=false")
            print("automatic_abaddon_policy_promotion=false")
            print("next_step=review_combat_utility_and_rejection_diagnostic")
            print("VOID_ACTUAL_APOLLYON_VS_ABADDON_WARM_START_COMBAT_SPAR_V1_4_GREEN")

            stub.DestroySession(
                pb2.DestroySessionRequest(session_id=sid),
                timeout=10.0,
            )
            destroyed = True
            print("session_destroyed=true")

        finally:
            if sid and stub is not None and not destroyed:
                try:
                    stub.DestroySession(
                        pb2.DestroySessionRequest(session_id=sid),
                        timeout=3.0,
                    )
                except Exception:
                    pass
            if channel is not None:
                try:
                    channel.close()
                except Exception:
                    pass
            inspect = base.run(["docker", "inspect", container_name], check=False, quiet=True)
            if inspect.returncode == 0:
                base.run(["docker", "rm", "-f", container_name], check=False, quiet=True)
            print("engine_container_removed=true")
            print("model_service_cleanup_performed=false")
            print("engine_cleanup_callback_complete=true")

    if base.out(["git", "status", "--porcelain", "--untracked-files=no"], cwd=OPENRA):
        raise RuntimeError("OpenRA tracked worktree changed")
    if base.out(["git", "status", "--porcelain", "--untracked-files=no"], cwd=RL):
        raise RuntimeError("War College tracked worktree changed")
    print("post_run_frozen_worktrees_green=true")


def main():
    """Direct execution is unavailable until a separate reviewed launcher binds authority."""
    raise RuntimeError(NEXT_GATE)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR={exc}", file=sys.stderr)
        print(
            "VOID_ACTUAL_APOLLYON_VS_ABADDON_WARM_START_COMBAT_SPAR_V1_4_RED",
            file=sys.stderr,
        )
        raise
