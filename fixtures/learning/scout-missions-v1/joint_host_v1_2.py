#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

HOME = Path.home()
DOWNLOADS = HOME / "Downloads"
RL = HOME / "dev" / "openra-rl-war-college"
OPENRA = RL / "OpenRA"
DOJO = HOME / "dev" / "void-apollyon-dojo"

HOST = "zoso-Precision-Tower-7810"

# Runtime-proven dual-controller generation.
GENERATION = "ad1926569b12466c"
IMAGE = f"void-openra-joint-duel:{GENERATION}"
IMAGE_ID = "sha256:79f2f6800382489a2a648839fc0d58e546384938439378aeea06461363de25f5"
ENGINE_COMMIT = "1607a7a6501d42a47638393ecef8b22831064932"
WAR_COLLEGE_COMMIT = "973802ef0a614e5afa782ff20e231e18966ae3e5"
RUNTIME_REPORT = DOWNLOADS / "void-openra-joint-duel-effect-authority-smoke-v1_2-20260827T062507.json"
RUNTIME_REPORT_SHA = "1073b98f938c8095b50ce97812e2fd08557e93ca491de2868b1b0a8250a5355f"
PROTO = RL / "proto" / "rl_bridge.proto"
PROTO_SHA = "9a48ca90bd525b7fd5502e7426cd8c1bb96b1308c2b18904d4d7af023699eae3"

# Frozen Apollyon boundary.
APOLLYON_RUNNER = DOWNLOADS / "void-apollyon-openra-war-college-attested-run-v1_13.py"
APOLLYON_RUNNER_SHA = "72fb0e9909dcdddb6c4a7713a5aa55568d2bef43020e6478945ca69247590abc"
APOLLYON_MODEL = "void-apollyon-candidate-v2r13:latest"

# Frozen Abaddon controller.
ABADDON_CONTROLLER = DOJO / "dojo" / "abaddon_controller.py"
ABADDON_CONTROLLER_SHA = "b235d4cff3e3953ed7c511de52c76ada7e1a47046295e104353b61ef09e11103"
ABADDON_DOCTRINES = (
    "RUSHER", "TURTLE", "FLANKER", "FEINTER", "COUNTERPUNCHER",
    "ECONOMIST", "AMBUSHER", "ATTRITION", "MOBILE_DEFENSE", "FORTRESS",
)

PROTO_PY = HOME / ".local/share/void-tools/openra-bridge-proto-v1/venv/bin/python"
ATTESTATION = DOJO / "provenance" / "joint-duel-training-eligibility-v1.json"
RUNS_DIR = DOJO / "war-college" / "joint-duels"

BUILDING_TYPES = {
    "fact", "powr", "apwr", "proc", "silo", "tent", "barr", "weap",
    "fix", "stek", "atek", "dome", "hpad", "afld", "iron", "pdox",
    "mslo", "sam", "spen", "syrd", "agun", "gun", "ftur", "tsla",
    "pbox", "hbox", "gap",
}
FOOTPRINTS = {
    "fact": (3, 4), "proc": (3, 4),
    "powr": (2, 3), "apwr": (3, 3),
    "barr": (2, 3), "tent": (2, 3),
    "weap": (3, 3), "fix": (3, 3), "stek": (3, 3),
    "dome": (2, 3), "hpad": (2, 3), "afld": (3, 2),
    "iron": (2, 2), "pdox": (2, 2),
    "mslo": (2, 1), "sam": (2, 1),
    "spen": (3, 3), "syrd": (3, 3), "atek": (2, 3),
    "gun": (1, 1), "ftur": (1, 1), "tsla": (1, 1),
    "agun": (1, 1), "pbox": (1, 1), "hbox": (1, 1), "gap": (1, 1),
}
DEFENSE_BUILDINGS = {"gun", "ftur", "tsla", "agun", "pbox", "hbox", "sam", "gap"}
MAX_PLACEMENT_ATTEMPTS = 20


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args, cwd=None, check=True, quiet=False, timeout=None):
    cp = subprocess.run(
        [str(x) for x in args],
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=timeout,
    )
    if cp.stdout and not quiet:
        print(cp.stdout.rstrip())
    if check and cp.returncode != 0:
        raise RuntimeError(
            f"command failed rc={cp.returncode}: {' '.join(map(str, args))}\n"
            f"{(cp.stdout or '')[-5000:]}"
        )
    return cp


def out(args, cwd=None, timeout=None) -> str:
    return run(args, cwd=cwd, quiet=True, timeout=timeout).stdout.strip()


def exact_file(path: Path, expected: str, label: str) -> None:
    if not path.is_file():
        raise RuntimeError(f"{label} missing: {path}")
    actual = sha(path)
    if actual != expected:
        raise RuntimeError(
            f"{label} hash drift\nexpected={expected}\nactual={actual}\npath={path}"
        )


def free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")

    # Dynamic modules containing @dataclass classes must be registered before
    # execution. dataclasses resolves cls.__module__ through sys.modules while
    # the class decorator runs.
    mod = importlib.util.module_from_spec(spec)
    previous = sys.modules.get(name)
    sys.modules[name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        if previous is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous
        raise
    return mod


def verify_runtime_report() -> dict[str, Any]:
    exact_file(RUNTIME_REPORT, RUNTIME_REPORT_SHA, "runtime authority smoke report")
    data = json.loads(RUNTIME_REPORT.read_text(encoding="utf-8"))
    expected = {
        "schema": "void.openra.joint-duel-effect-authority-smoke.v1_2",
        "generation_id": GENERATION,
        "image": IMAGE,
        "image_id": IMAGE_ID,
        "seed": 2050,
        "verdict": "GREEN",
        "training_started": False,
        "evidence_admitted": False,
        "container_removed": True,
    }
    for k, v in expected.items():
        if data.get(k) != v:
            raise RuntimeError(
                f"runtime report mismatch {k}: expected={v!r} actual={data.get(k)!r}"
            )
    if data.get("attack_hashes") != data.get("control_hashes"):
        raise RuntimeError("runtime report does not bind foreign-command zero effect")
    owner = data.get("owner_hashes") or {}
    control = data.get("control_hashes") or {}
    if owner.get("Multi0") == control.get("Multi0"):
        raise RuntimeError("runtime report lacks authorized-command sensitivity")
    if len(set(data.get("sessions_destroyed") or [])) != 3:
        raise RuntimeError("runtime teardown proof incomplete")
    if "FAILED_PRECONDITION" not in str(data.get("legacy_after_joint_status", "")):
        raise RuntimeError("joint/legacy mutual exclusion proof missing")
    return data


def write_joint_attestation() -> str:
    obj = {
        "schema": "void.apollyon-abaddon.joint-duel-training-eligibility.v1",
        "generation_id": GENERATION,
        "purpose": "candidate-only actual Apollyon-vs-Abaddon joint sparring trajectories",
        "engine": {
            "image": IMAGE,
            "image_id": IMAGE_ID,
            "openra_commit": ENGINE_COMMIT,
            "war_college_commit": WAR_COLLEGE_COMMIT,
            "proto_sha256": PROTO_SHA,
        },
        "runtime_proof": {
            "file": RUNTIME_REPORT.name,
            "sha256": RUNTIME_REPORT_SHA,
            "same_tick_joint_advance": True,
            "same_seed_determinism": True,
            "player_perspective_isolation": True,
            "subject_actor_authority_isolation": True,
            "legacy_joint_mutual_exclusion": True,
            "teardown_green": True,
        },
        "apollyon": {
            "model": APOLLYON_MODEL,
            "boundary_runner": APOLLYON_RUNNER.name,
            "boundary_runner_sha256": APOLLYON_RUNNER_SHA,
        },
        "abaddon": {
            "controller": str(ABADDON_CONTROLLER.relative_to(DOJO)),
            "controller_sha256": ABADDON_CONTROLLER_SHA,
            "deterministic": True,
            "llm": False,
        },
        "policy": {
            "joint_sparring_candidate_rows_eligible": True,
            "automatic_corpus_admission": False,
            "automatic_apollyon_weight_mutation": False,
            "automatic_abaddon_policy_promotion": False,
            "review_required_before_training_or_promotion": True,
            "baseline_generation_must_remain_immutable": True,
        },
    }
    raw = (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode()
    ATTESTATION.parent.mkdir(parents=True, exist_ok=True)
    if ATTESTATION.exists() and ATTESTATION.read_bytes() != raw:
        raise RuntimeError(f"joint training attestation drift: {ATTESTATION}")
    if not ATTESTATION.exists():
        ATTESTATION.write_bytes(raw)
    att_sha = sha(ATTESTATION)
    print(f"joint_training_attestation={ATTESTATION}")
    print(f"joint_training_attestation_sha256={att_sha}")
    print("joint_sparring_candidate_rows_eligible=true")
    print("automatic_corpus_admission=false")
    return att_sha


def generate_proto(temp: Path):
    cdir = temp / "grpc"
    cdir.mkdir()
    run(
        [
            sys.executable, "-m", "grpc_tools.protoc",
            f"-I{PROTO.parent}",
            f"--python_out={cdir}",
            f"--grpc_python_out={cdir}",
            str(PROTO),
        ],
        cwd=RL,
        quiet=True,
    )
    sys.path.insert(0, str(cdir))
    import importlib
    pb2 = importlib.import_module("rl_bridge_pb2")
    pb2_grpc = importlib.import_module("rl_bridge_pb2_grpc")
    return pb2, pb2_grpc


def wait_daemon(stub, pb2, name: str, timeout_s=60):
    deadline = time.monotonic() + timeout_s
    last = None
    while time.monotonic() < deadline:
        status = out(["docker", "inspect", "-f", "{{.State.Status}}", name])
        if status != "running":
            logs = out(["docker", "logs", "--tail", "200", name])
            raise RuntimeError(f"engine container stopped: {status}\n{logs}")
        try:
            state = stub.GetState(pb2.StateRequest(), timeout=1.0)
            print(f"daemon_ready_phase={state.phase}")
            return
        except Exception as exc:
            last = exc
            time.sleep(0.25)
    raise RuntimeError(f"engine daemon readiness timeout: {last}")


def wait_players(stub, pb2, sid: str, timeout_s=90):
    deadline = time.monotonic() + timeout_s
    latest = {}
    while time.monotonic() < deadline:
        ok = True
        for player in ("Multi0", "Multi1"):
            try:
                st = stub.GetState(
                    pb2.StateRequest(session_id=sid, player=player),
                    timeout=2.0,
                )
                latest[player] = {
                    "phase": st.phase,
                    "tick": st.tick,
                    "player_internal_name": st.player_internal_name,
                    "winner": st.winner,
                }
                if st.phase != "playing" or st.player_internal_name != player:
                    ok = False
            except Exception as exc:
                latest[player] = {"error": repr(exc)}
                ok = False
        if ok:
            return latest
        time.sleep(0.25)
    raise RuntimeError(f"player routes not ready: {latest}")


def state_from_obs(obs) -> dict[str, Any]:
    eco = {
        "cash": int(obs.economy.cash),
        "ore": int(obs.economy.ore),
        "power_provided": int(obs.economy.power_provided),
        "power_drained": int(obs.economy.power_drained),
        "resource_capacity": int(obs.economy.resource_capacity),
        "harvester_count": int(obs.economy.harvester_count),
    }
    units = []
    for u in obs.units:
        units.append({
            "id": int(u.actor_id),
            "type": u.type,
            "idle": bool(u.is_idle),
            "is_idle": bool(u.is_idle),
            "can_attack": bool(u.can_attack),
            "stance": int(u.stance),
            "cell_x": int(u.cell_x),
            "cell_y": int(u.cell_y),
            "activity": u.current_activity,
            "current_activity": u.current_activity,
            "hp_percent": float(u.hp_percent),
        })
    buildings = []
    for b in obs.buildings:
        buildings.append({
            "id": int(b.actor_id),
            "type": b.type,
            "cell_x": int(b.cell_x),
            "cell_y": int(b.cell_y),
            "hp_percent": float(b.hp_percent),
            "is_powered": bool(b.is_powered),
        })
    enemies = []
    for e in obs.visible_enemies:
        enemies.append({
            "id": int(e.actor_id),
            "type": e.type,
            "cell_x": int(e.cell_x),
            "cell_y": int(e.cell_y),
            "hp_percent": float(e.hp_percent),
            "can_attack": bool(e.can_attack),
            "owner": e.owner,
        })
    enemy_buildings = []
    for b in obs.visible_enemy_buildings:
        enemy_buildings.append({
            "id": int(b.actor_id),
            "type": b.type,
            "cell_x": int(b.cell_x),
            "cell_y": int(b.cell_y),
            "hp_percent": float(b.hp_percent),
            "owner": b.owner,
        })
    prod = []
    prod_items = []
    for p in obs.production:
        row = {
            "queue_type": p.queue_type,
            "item": p.item,
            "progress": float(p.progress),
            "remaining_ticks": int(p.remaining_ticks),
            "paused": bool(p.paused),
        }
        prod.append(row)
        prod_items.append(f"{p.item}@{float(p.progress):.0%}")
    return {
        "tick": int(obs.tick),
        "done": bool(obs.done),
        "result": obs.result,
        "economy": eco,
        "power_balance": eco["power_provided"] - eco["power_drained"],
        "military": {
            "units_killed": int(obs.military.units_killed),
            "units_lost": int(obs.military.units_lost),
            "buildings_killed": int(obs.military.buildings_killed),
            "buildings_lost": int(obs.military.buildings_lost),
            "army_value": int(obs.military.army_value),
            "assets_value": int(obs.military.assets_value),
            "kills_cost": int(obs.military.kills_cost),
            "deaths_cost": int(obs.military.deaths_cost),
        },
        "own_units": len(units),
        "own_buildings": len(buildings),
        "units_summary": units,
        "buildings_summary": buildings,
        "enemy_summary": enemies,
        "enemy_buildings_summary": enemy_buildings,
        "visible_enemy_units": len(enemies),
        "visible_enemy_buildings": len(enemy_buildings),
        "production": prod,
        "production_items": prod_items,
        "available_production": list(obs.available_production),
        "map": {
            "width": int(obs.map_info.width),
            "height": int(obs.map_info.height),
            "map_name": obs.map_info.map_name,
        },
        "explored_percent": float(obs.explored_percent),
        "minimap": "",
    }


def resolve_units(selector: Any, state: dict[str, Any]) -> list[int]:
    units = state["units_summary"]
    living = {u["id"] for u in units}
    if isinstance(selector, int):
        return [selector] if selector in living else []
    if isinstance(selector, list):
        return [int(x) for x in selector if int(x) in living]
    if not isinstance(selector, str):
        return []
    s = selector.strip()
    if s == "all_combat":
        return [u["id"] for u in units if u["can_attack"]]
    if s == "all_idle":
        return [u["id"] for u in units if u["can_attack"] and u["idle"]]
    if s == "all":
        return [u["id"] for u in units]
    if s.startswith("type:"):
        t = s[5:].strip()
        return [u["id"] for u in units if u["type"] == t]
    cleaned = s.strip("[] ")
    if cleaned:
        try:
            vals = [int(x.strip()) for x in cleaned.split(",") if x.strip()]
            return [x for x in vals if x in living]
        except ValueError:
            pass
    return [u["id"] for u in units if u["type"].lower() == s.lower()]


def placement_candidates(building_type: str, state: dict[str, Any]) -> list[tuple[int, int]]:
    buildings = state["buildings_summary"]
    fact = next((b for b in buildings if b["type"] == "fact"), None)
    if fact is None:
        return []
    cx, cy = fact["cell_x"], fact["cell_y"]
    bw, bh = FOOTPRINTS.get(building_type, (2, 2))
    occupied = set()
    for b in buildings:
        fw, fh = FOOTPRINTS.get(b["type"], (2, 2))
        bx, by = b["cell_x"], b["cell_y"]
        for dx in range(-1, fw + 1):
            for dy in range(-1, fh + 1):
                occupied.add((bx + dx, by + dy))
    map_w = max(1, int(state["map"]["width"]))
    map_h = max(1, int(state["map"]["height"]))
    candidates = []
    for dx in range(-15, 16):
        for dy in range(-15, 16):
            dist = abs(dx) + abs(dy)
            if dist < 2 or dist > 15:
                continue
            px, py = cx + dx, cy + dy
            if px < 0 or py < 0 or px + bw > map_w or py + bh > map_h:
                continue
            if any((px + ox, py + oy) in occupied
                   for ox in range(bw) for oy in range(bh)):
                continue
            candidates.append((px, py, dist))
    if building_type in DEFENSE_BUILDINGS:
        ex = map_w - cx
        ey = map_h - cy
        dx0 = ex - cx
        dy0 = ey - cy
        mag = max(abs(dx0), abs(dy0), 1)
        ux, uy = dx0 / mag, dy0 / mag
        candidates.sort(
            key=lambda c: (
                -((c[0] - cx) * ux + (c[1] - cy) * uy),
                abs(c[2] - 5),
                c[0],
                c[1],
            )
        )
    else:
        candidates.sort(key=lambda c: (c[2], c[0], c[1]))
    return [(x, y) for x, y, _ in candidates]


def placement_commands(player: str, state: dict[str, Any], pending: dict[str, dict], pb2):
    commands = []
    notes = []
    counts = {}
    for b in state["buildings_summary"]:
        counts[b["type"]] = counts.get(b["type"], 0) + 1

    for btype in list(pending):
        ent = pending[btype]
        if counts.get(btype, 0) > ent["baseline_count"]:
            notes.append(f"{btype}:placement_confirmed")
            pending.pop(btype, None)
            continue

        ready = any(
            p["item"] == btype and p["queue_type"] in {"Building", "Defense"}
            and p["progress"] >= 0.99
            for p in state["production"]
        )
        queued = any(p["item"] == btype for p in state["production"])

        if not queued and not ready:
            # Production disappeared without a new building: failed/cancelled.
            notes.append(f"{btype}:production_disappeared")
            pending.pop(btype, None)
            continue

        if not ready:
            continue

        candidates = placement_candidates(btype, state)
        idx = int(ent["attempt"])
        if idx >= min(len(candidates), MAX_PLACEMENT_ATTEMPTS):
            commands.append(pb2.Command(
                action=pb2.CANCEL_PRODUCTION,
                item_type=btype,
            ))
            notes.append(f"{btype}:placement_exhausted_cancel")
            pending.pop(btype, None)
            continue

        if idx == 0 and ent.get("cell_x", 0) and ent.get("cell_y", 0):
            x, y = int(ent["cell_x"]), int(ent["cell_y"])
        else:
            x, y = candidates[idx]
        commands.append(pb2.Command(
            action=pb2.PLACE_BUILDING,
            item_type=btype,
            target_x=x,
            target_y=y,
        ))
        ent["attempt"] = idx + 1
        notes.append(f"{btype}:place_attempt_{idx+1}@{x},{y}")

    return commands, notes


def decision_to_commands(
    name: str,
    args: dict[str, Any],
    state: dict[str, Any],
    pending: dict[str, dict],
    pb2,
):
    if not isinstance(args, dict):
        return False, "arguments_not_object", []

    own_units = {u["id"] for u in state["units_summary"]}
    own_actors = own_units | {b["id"] for b in state["buildings_summary"]}
    enemy_actors = (
        {e["id"] for e in state["enemy_summary"]}
        | {b["id"] for b in state["enemy_buildings_summary"]}
    )
    width = max(1, int(state["map"]["width"]))
    height = max(1, int(state["map"]["height"]))

    if name == "advance":
        return True, "shared_clock_noop", []

    if name == "deploy_unit":
        uid = int(args.get("unit_id", 0) or 0)
        if uid not in own_units:
            return False, f"deploy_foreign_or_missing_unit:{uid}", []
        return True, "deploy", [pb2.Command(action=pb2.DEPLOY, actor_id=uid)]

    if name == "build_and_place":
        btype = str(args.get("building_type", ""))
        if btype not in BUILDING_TYPES:
            return False, f"unknown_building:{btype}", []
        if btype not in state["available_production"]:
            return False, f"building_unavailable:{btype}", []
        if btype in pending:
            return False, f"building_already_pending:{btype}", []
        if any(p["item"] == btype for p in state["production"]):
            return False, f"building_already_queued:{btype}", []
        baseline = sum(1 for b in state["buildings_summary"] if b["type"] == btype)
        pending[btype] = {
            "baseline_count": baseline,
            "attempt": 0,
            "cell_x": int(args.get("cell_x", 0) or 0),
            "cell_y": int(args.get("cell_y", 0) or 0),
        }
        return True, "build_and_place", [
            pb2.Command(action=pb2.BUILD, item_type=btype)
        ]

    if name == "build_unit":
        utype = str(args.get("unit_type", ""))
        count = int(args.get("count", 1) or 1)
        if utype in BUILDING_TYPES or utype not in state["available_production"]:
            return False, f"unit_unavailable:{utype}", []
        if count < 1 or count > 3:
            return False, f"unit_count_out_of_bounds:{count}", []
        return True, "build_unit", [
            pb2.Command(action=pb2.TRAIN, item_type=utype)
            for _ in range(count)
        ]

    if name in {"move_units", "attack_move", "stop_units", "set_stance"}:
        ids = resolve_units(args.get("unit_ids", ""), state)
        if not ids:
            return False, "no_owned_units_resolved", []
        if name == "stop_units":
            return True, "stop", [
                pb2.Command(action=pb2.STOP, actor_id=uid) for uid in ids
            ]
        if name == "set_stance":
            stance_map = {
                "hold_fire": 0, "return_fire": 1,
                "defend": 2, "attack_anything": 3,
            }
            stance = str(args.get("stance", "attack_anything")).lower()
            if stance not in stance_map:
                return False, f"invalid_stance:{stance}", []
            return True, "stance", [
                pb2.Command(
                    action=pb2.SET_STANCE,
                    actor_id=uid,
                    target_x=stance_map[stance],
                )
                for uid in ids
            ]
        x = int(args.get("target_x", -1))
        y = int(args.get("target_y", -1))
        if x < 0 or x >= width or y < 0 or y >= height:
            return False, f"target_out_of_bounds:{x},{y}", []
        action = pb2.MOVE if name == "move_units" else pb2.ATTACK_MOVE
        return True, name, [
            pb2.Command(
                action=action,
                actor_id=uid,
                target_x=x,
                target_y=y,
                queued=bool(args.get("queued", False)),
            )
            for uid in ids
        ]

    if name == "attack_target":
        ids = resolve_units(args.get("unit_ids", ""), state)
        tid = int(args.get("target_actor_id", 0) or 0)
        if not ids:
            return False, "no_owned_attackers_resolved", []
        if tid not in enemy_actors:
            return False, f"target_not_visible_enemy:{tid}", []
        return True, "attack_target", [
            pb2.Command(
                action=pb2.ATTACK,
                actor_id=uid,
                target_actor_id=tid,
                queued=bool(args.get("queued", False)),
            )
            for uid in ids
        ]

    if name == "guard_target":
        ids = resolve_units(args.get("unit_ids", ""), state)
        tid = int(args.get("target_actor_id", 0) or 0)
        if not ids:
            return False, "no_owned_guards_resolved", []
        if tid not in own_actors:
            return False, f"guard_target_not_owned:{tid}", []
        return True, "guard_target", [
            pb2.Command(
                action=pb2.GUARD,
                actor_id=uid,
                target_actor_id=tid,
            )
            for uid in ids
        ]

    return False, f"unsupported_tool:{name}", []


def apollyon_tools(state: dict[str, Any]) -> list[dict[str, Any]]:
    width = max(1, int(state["map"]["width"]))
    height = max(1, int(state["map"]["height"]))
    available = list(state["available_production"])
    bchoices = sorted(x for x in available if x in BUILDING_TYPES)
    uchoices = sorted(x for x in available if x not in BUILDING_TYPES)
    mcvs = sorted(
        u["id"] for u in state["units_summary"]
        if u["type"] in {"mcv", "amcv"}
    )
    enemy_ids = sorted(
        [x["id"] for x in state["enemy_summary"]]
        + [x["id"] for x in state["enemy_buildings_summary"]]
    )
    own_actor_ids = sorted(
        [x["id"] for x in state["units_summary"]]
        + [x["id"] for x in state["buildings_summary"]]
    )
    selector_desc = (
        'Owned unit selector: "all_combat", "all_idle", "type:e1", '
        'a comma-separated list of observed own actor IDs, or one observed own type.'
    )

    tools = [{
        "type": "function",
        "function": {
            "name": "advance",
            "description": "Take no command this decision. The host advances the shared duel clock by the fixed round amount.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
    }]

    if mcvs:
        tools.append({
            "type": "function",
            "function": {
                "name": "deploy_unit",
                "description": "Deploy one owned MCV or deployable unit.",
                "parameters": {
                    "type": "object",
                    "properties": {"unit_id": {"type": "integer", "enum": mcvs}},
                    "required": ["unit_id"],
                    "additionalProperties": False,
                },
            },
        })

    if bchoices:
        tools.append({
            "type": "function",
            "function": {
                "name": "build_and_place",
                "description": "Queue one available structure. The host performs deterministic placement once construction is ready.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "building_type": {"type": "string", "enum": bchoices},
                    },
                    "required": ["building_type"],
                    "additionalProperties": False,
                },
            },
        })

    if uchoices:
        tools.append({
            "type": "function",
            "function": {
                "name": "build_unit",
                "description": "Queue one to three available units.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "unit_type": {"type": "string", "enum": uchoices},
                        "count": {"type": "integer", "minimum": 1, "maximum": 3},
                    },
                    "required": ["unit_type"],
                    "additionalProperties": False,
                },
            },
        })

    combat = [u for u in state["units_summary"] if u["can_attack"]]
    if combat:
        for name, desc in (
            ("move_units", "Move owned units to a cell."),
            ("attack_move", "Move owned units toward a cell while fighting encountered enemies."),
        ):
            tools.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": desc,
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "unit_ids": {"type": "string", "description": selector_desc},
                            "target_x": {"type": "integer", "minimum": 0, "maximum": width - 1},
                            "target_y": {"type": "integer", "minimum": 0, "maximum": height - 1},
                            "queued": {"type": "boolean"},
                        },
                        "required": ["unit_ids", "target_x", "target_y"],
                        "additionalProperties": False,
                    },
                },
            })
        tools.append({
            "type": "function",
            "function": {
                "name": "set_stance",
                "description": "Set combat stance for owned units.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "unit_ids": {"type": "string", "description": selector_desc},
                        "stance": {
                            "type": "string",
                            "enum": ["hold_fire", "return_fire", "defend", "attack_anything"],
                        },
                    },
                    "required": ["unit_ids", "stance"],
                    "additionalProperties": False,
                },
            },
        })
        tools.append({
            "type": "function",
            "function": {
                "name": "stop_units",
                "description": "Stop owned units.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "unit_ids": {"type": "string", "description": selector_desc},
                    },
                    "required": ["unit_ids"],
                    "additionalProperties": False,
                },
            },
        })
        if own_actor_ids:
            tools.append({
                "type": "function",
                "function": {
                    "name": "guard_target",
                    "description": "Order owned combat units to guard an owned actor.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "unit_ids": {"type": "string", "description": selector_desc},
                            "target_actor_id": {"type": "integer", "enum": own_actor_ids},
                        },
                        "required": ["unit_ids", "target_actor_id"],
                        "additionalProperties": False,
                    },
                },
            })
        if enemy_ids:
            tools.append({
                "type": "function",
                "function": {
                    "name": "attack_target",
                    "description": "Attack one currently visible enemy actor.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "unit_ids": {"type": "string", "description": selector_desc},
                            "target_actor_id": {"type": "integer", "enum": enemy_ids},
                            "queued": {"type": "boolean"},
                        },
                        "required": ["unit_ids", "target_actor_id"],
                        "additionalProperties": False,
                    },
                },
            })
    return tools


def compact_state(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "tick": state["tick"],
        "economy": state["economy"],
        "power_balance": state["power_balance"],
        "military": state["military"],
        "units_summary": state["units_summary"],
        "buildings_summary": state["buildings_summary"],
        "enemy_summary": state["enemy_summary"],
        "enemy_buildings_summary": state["enemy_buildings_summary"],
        "production_items": state["production_items"],
        "available_production": state["available_production"],
        "map": state["map"],
        "explored_percent": state["explored_percent"],
    }


def apollyon_decision(helper, state, pending, pb2, doctrine: str, round_no: int):
    tools = apollyon_tools(state)
    system = (
        "You are Apollyon, VOID General, in a private deterministic Red Alert duel against "
        "the actual Abaddon controller. Both sides decide from the same frozen world tick and "
        "their command batches are committed before the shared simulation advances. "
        "Call exactly one provided tool. Use only observed own actor IDs and currently visible "
        "enemy IDs. Never invent IDs. Win the duel while preserving a functional economy: "
        "deploy the MCV, maintain power, establish refinery/harvester and production, scout, "
        "respond to contact, and exploit real tactical opportunities. Host-controlled building "
        "placement is mechanical and symmetric. An advance tool means intentionally issue no "
        "command this round. Do not claim hidden information."
    )
    base_user = (
        f"ROUND={round_no}\n"
        f"ABADDON_DOCTRINE_PUBLIC_TRAINING_LABEL={doctrine}\n"
        f"SHARED_TICKS_PER_ROUND_FIXED=true\n"
        f"STATE={json.dumps(compact_state(state), sort_keys=True, separators=(',', ':'))}"
    )
    attempts = []
    feedback = ""
    for attempt in range(1, 3):
        user = base_user
        if feedback:
            user += (
                "\nHOST_REJECTED_PREVIOUS_ATTEMPT=" + feedback
                + "\nChoose one valid tool call using the unchanged frozen state."
            )
        name, args = helper.ollama_tool_call(system, user, tools)
        ok, reason, commands = decision_to_commands(name, args, state, pending, pb2)
        attempts.append({
            "attempt": attempt,
            "tool": name,
            "arguments": args,
            "accepted": ok,
            "host_reason": reason,
        })
        if ok:
            return name, args, commands, attempts
        feedback = reason
    return "advance", {}, [], attempts


def joint_advance(stub, pb2, sid, ticks, commands_by_player):
    req = pb2.JointAdvanceRequest(session_id=sid, ticks=ticks)
    for player in ("Multi0", "Multi1"):
        batch = req.player_actions.add(player=player)
        for cmd in commands_by_player.get(player, []):
            batch.commands.add().CopyFrom(cmd)
    resp = stub.JointAdvance(req, timeout=120.0)
    if resp.end_tick - resp.start_tick != ticks:
        raise RuntimeError(
            f"joint tick delta mismatch: {resp.start_tick}->{resp.end_tick}, expected {ticks}"
        )
    obs_by = {x.player: x.observation for x in resp.player_observations}
    if set(obs_by) != {"Multi0", "Multi1"}:
        raise RuntimeError(f"wrong joint observation set: {set(obs_by)}")
    for player, obs in obs_by.items():
        if obs.tick != resp.end_tick:
            raise RuntimeError(f"{player} observation tick mismatch")
    return resp, obs_by


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
        f.flush()
        os.fsync(f.fileno())


def parse_args():
    p = argparse.ArgumentParser(
        description="Actual Apollyon vs actual Abaddon bounded joint sparring batch"
    )
    p.add_argument("--seed", type=int, default=2050)
    p.add_argument("--rounds", type=int, default=24)
    p.add_argument("--ticks-per-round", type=int, default=50)
    p.add_argument("--doctrine", choices=ABADDON_DOCTRINES, default="RUSHER")
    return p.parse_args()


def main():
    args = parse_args()
    if args.rounds < 1 or args.rounds > 200:
        raise RuntimeError("--rounds must be 1..200")
    if args.ticks_per_round < 1 or args.ticks_per_round > 250:
        raise RuntimeError("--ticks-per-round must be 1..250")

    print("=== VOID ACTUAL APOLLYON VS ABADDON JOINT SPARRING BATCH V1.2 ===")
    print("actual_apollyon=true")
    print("actual_abaddon=true")
    print("proxy_bot=false")
    print(f"generation_id={GENERATION}")
    print(f"image={IMAGE}")
    print(f"seed={args.seed}")
    print(f"abaddon_doctrine={args.doctrine}")
    print(f"round_limit={args.rounds}")
    print(f"ticks_per_round={args.ticks_per_round}")
    print("joint_same_tick_actions=true")
    print("training_candidate_collection=true")
    print("automatic_apollyon_weight_mutation=false")
    print("automatic_abaddon_policy_promotion=false")
    print("automatic_corpus_admission=false")
    print("git_mutation=false")
    print("void_chain_mutation=false")
    print("wallet_or_funds_action=false")
    print("production_runtime_mutation=false")
    print("fail_closed=true")

    if socket.gethostname() != HOST:
        raise RuntimeError(f"run on {HOST}")
    if not PROTO_PY.is_file():
        raise RuntimeError(f"isolated gRPC Python missing: {PROTO_PY}")
    if Path(sys.executable).resolve() != PROTO_PY.resolve():
        raise RuntimeError(
            f"run with isolated gRPC Python: {PROTO_PY}\ncurrent={sys.executable}"
        )

    if out(["git", "rev-parse", "HEAD"], cwd=OPENRA) != ENGINE_COMMIT:
        raise RuntimeError("OpenRA worktree is not at frozen runtime-proven commit")
    if out(["git", "rev-parse", "HEAD"], cwd=RL) != WAR_COLLEGE_COMMIT:
        raise RuntimeError("War College worktree is not at frozen runtime-proven commit")
    if out(["git", "status", "--porcelain", "--untracked-files=no"], cwd=OPENRA):
        raise RuntimeError("OpenRA tracked worktree not clean")
    if out(["git", "status", "--porcelain", "--untracked-files=no"], cwd=RL):
        raise RuntimeError("War College tracked worktree not clean")
    print("frozen_local_worktrees_green=true")

    exact_file(PROTO, PROTO_SHA, "joint proto")
    exact_file(APOLLYON_RUNNER, APOLLYON_RUNNER_SHA, "Apollyon boundary runner")
    exact_file(ABADDON_CONTROLLER, ABADDON_CONTROLLER_SHA, "Abaddon controller")
    verify_runtime_report()
    print("runtime_authority_proof_green=true")

    image_id = out(["docker", "image", "inspect", "-f", "{{.Id}}", IMAGE])
    if image_id != IMAGE_ID:
        raise RuntimeError(f"image drift: expected={IMAGE_ID} actual={image_id}")
    label = out([
        "docker", "image", "inspect", "-f",
        '{{ index .Config.Labels "void.openra.generation" }}', IMAGE,
    ])
    if label != GENERATION:
        raise RuntimeError("runtime image generation label drift")
    if out(["docker", "context", "show"]) != "rootless":
        raise RuntimeError("rootless Docker context required")
    if "rootless" not in out(["docker", "info"]).lower():
        raise RuntimeError("rootless Docker daemon required")
    print("runtime_image_identity_green=true")
    print("docker_rootless=true")

    helper = load_module(APOLLYON_RUNNER, "void_apollyon_v113_boundary")
    if getattr(helper, "MODEL", None) != APOLLYON_MODEL:
        raise RuntimeError("Apollyon model boundary drift")

    # Preserve the local-only/dormant fuse boundary from the reviewed Apollyon runner.
    # systemctl status-query commands use nonzero return codes for expected
    # negative states (e.g. is-active -> rc=3 for "inactive",
    # is-enabled -> rc=1 for "disabled"). Treat stdout as the authority and
    # validate the exact dormant state instead of requiring rc=0.
    active_cp = run(
        ["systemctl", "is-active", helper.SERVICE],
        check=False,
        quiet=True,
    )
    enabled_cp = run(
        ["systemctl", "is-enabled", helper.SERVICE],
        check=False,
        quiet=True,
    )
    active = (active_cp.stdout or "").strip()
    enabled = (enabled_cp.stdout or "").strip()
    print(f"pre_ollama_active={active}")
    print(f"pre_ollama_active_rc={active_cp.returncode}")
    print(f"pre_ollama_enabled={enabled}")
    print(f"pre_ollama_enabled_rc={enabled_cp.returncode}")
    if active != "inactive" or enabled != "disabled":
        raise RuntimeError(
            "Ollama must begin exactly inactive and disabled; "
            f"observed active={active!r}/rc{active_cp.returncode}, "
            f"enabled={enabled!r}/rc{enabled_cp.returncode}"
        )
    print("ollama_dormant_preflight_green=true")
    for label_name, (path, expected) in helper.EXACT.items():
        exact_file(path, expected, label_name)
    exact_file(helper.V14, helper.V14_SHA, "Apollyon V14 boundary")
    print("apollyon_local_only_boundary_green=true")

    abaddon_mod = load_module(ABADDON_CONTROLLER, "void_abaddon_controller")
    print("dynamic_module_registration_green=true")
    controller = abaddon_mod.AbaddonController(
        doctrine=args.doctrine,
        seed=args.seed,
    )
    print("abaddon_controller_loaded=true")
    print("abaddon_deterministic=true")

    att_sha = write_joint_attestation()

    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    run_id = (
        f"actual-apollyon-vs-abaddon-{stamp}-"
        f"{args.doctrine.lower()}-s{args.seed}"
    )
    run_dir = RUNS_DIR / run_id
    if run_dir.exists():
        raise RuntimeError(f"run directory collision: {run_dir}")
    run_dir.mkdir(parents=True)
    corpus = run_dir / "trajectory.jsonl"
    summary_path = run_dir / "summary.json"
    manifest_path = run_dir / "manifest.json"

    runner_sha = sha(Path(__file__))
    append_jsonl(corpus, {
        "event": "run_header",
        "run_id": run_id,
        "generation_id": GENERATION,
        "runtime_image_id": IMAGE_ID,
        "engine_commit": ENGINE_COMMIT,
        "war_college_commit": WAR_COLLEGE_COMMIT,
        "joint_training_attestation_sha256": att_sha,
        "runner_sha256": runner_sha,
        "apollyon_model": APOLLYON_MODEL,
        "abaddon_controller_sha256": ABADDON_CONTROLLER_SHA,
        "abaddon_doctrine": args.doctrine,
        "seed": args.seed,
        "round_limit": args.rounds,
        "ticks_per_round": args.ticks_per_round,
        "candidate_only": True,
        "review_required": True,
    })

    import grpc

    container_name = f"void-actual-joint-spar-{os.getpid()}"
    port = free_port()
    channel = None
    stub = None
    sid = ""
    destroyed = False
    helper_started = False
    pending = {"Multi0": {}, "Multi1": {}}
    final_status = "unfinished"
    winner = ""
    completed_rounds = 0

    with tempfile.TemporaryDirectory(prefix="void-actual-joint-spar.") as td:
        pb2, pb2_grpc = generate_proto(Path(td))
        try:
            helper.start_ollama()
            helper_started = True

            run([
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
            wait_daemon(stub, pb2, container_name)
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
            wait_players(stub, pb2, sid)
            print(f"session_id={sid}")
            print("actual_two_external_players_ready=true")

            # Atomic 1-tick bootstrap produces both first full observations.
            initial_resp, obs_by = joint_advance(
                stub, pb2, sid, 1, {"Multi0": [], "Multi1": []}
            )
            states = {p: state_from_obs(o) for p, o in obs_by.items()}
            print(f"joint_initial_tick={initial_resp.end_tick}")

            for round_no in range(1, args.rounds + 1):
                start_tick = states["Multi0"]["tick"]
                if states["Multi1"]["tick"] != start_tick:
                    raise RuntimeError("player perspectives disagree on start tick")

                # Host-only symmetric building placement is prepared from each player's
                # own observation before either controller decision is converted.
                mech0, placement0 = placement_commands(
                    "Multi0", states["Multi0"], pending["Multi0"], pb2
                )
                mech1, placement1 = placement_commands(
                    "Multi1", states["Multi1"], pending["Multi1"], pb2
                )

                a_name, a_args, a_cmds, a_attempts = apollyon_decision(
                    helper,
                    states["Multi0"],
                    pending["Multi0"],
                    pb2,
                    args.doctrine,
                    round_no,
                )

                ab_decision = controller.decide(states["Multi1"])
                ab_action = ab_decision.get("action") or {}
                b_name = str(ab_action.get("tool", "advance"))
                b_args = ab_action.get("arguments") or {}
                b_ok, b_reason, b_cmds = decision_to_commands(
                    b_name,
                    b_args,
                    states["Multi1"],
                    pending["Multi1"],
                    pb2,
                )
                if not b_ok:
                    b_cmds = []

                commands = {
                    "Multi0": mech0 + a_cmds,
                    "Multi1": mech1 + b_cmds,
                }

                append_jsonl(corpus, {
                    "event": "joint_decision",
                    "run_id": run_id,
                    "round": round_no,
                    "start_tick": start_tick,
                    "apollyon_state": compact_state(states["Multi0"]),
                    "abaddon_state": compact_state(states["Multi1"]),
                    "apollyon": {
                        "tool": a_name,
                        "arguments": a_args,
                        "attempts": a_attempts,
                        "command_count": len(a_cmds),
                    },
                    "abaddon": {
                        "decision": ab_decision,
                        "accepted": b_ok,
                        "host_reason": b_reason,
                        "command_count": len(b_cmds),
                    },
                    "mechanical_placement": {
                        "Multi0": placement0,
                        "Multi1": placement1,
                    },
                    "joint_command_counts": {
                        "Multi0": len(commands["Multi0"]),
                        "Multi1": len(commands["Multi1"]),
                    },
                    "candidate_only": True,
                    "training_candidate": True,
                    "joint_training_attestation_sha256": att_sha,
                })

                resp, obs_by = joint_advance(
                    stub, pb2, sid, args.ticks_per_round, commands
                )
                states = {p: state_from_obs(o) for p, o in obs_by.items()}
                completed_rounds = round_no

                st0 = stub.GetState(
                    pb2.StateRequest(session_id=sid, player="Multi0"),
                    timeout=3.0,
                )
                winner = st0.winner or ""
                phase = st0.phase or ""

                append_jsonl(corpus, {
                    "event": "joint_result",
                    "run_id": run_id,
                    "round": round_no,
                    "start_tick": int(resp.start_tick),
                    "end_tick": int(resp.end_tick),
                    "phase": phase,
                    "winner": winner,
                    "apollyon_after": compact_state(states["Multi0"]),
                    "abaddon_after": compact_state(states["Multi1"]),
                    "candidate_only": True,
                    "training_candidate": True,
                    "joint_training_attestation_sha256": att_sha,
                })

                print(
                    f"round={round_no} tick={resp.start_tick}->{resp.end_tick} "
                    f"apollyon={a_name} abaddon={b_name} "
                    f"visible={states['Multi0']['visible_enemy_units'] + states['Multi0']['visible_enemy_buildings']}/"
                    f"{states['Multi1']['visible_enemy_units'] + states['Multi1']['visible_enemy_buildings']} "
                    f"phase={phase or 'playing'} winner={winner or '-'}"
                )

                if phase == "game_over" or states["Multi0"]["done"] or states["Multi1"]["done"]:
                    final_status = "game_over"
                    break

            if final_status != "game_over":
                final_status = "round_limit"

            if winner == "Multi0":
                outcome = "APOLLYON_WIN"
            elif winner == "Multi1":
                outcome = "ABADDON_WIN"
            elif final_status == "game_over":
                outcome = "DRAW_OR_UNRESOLVED_WINNER"
            else:
                outcome = "UNFINISHED_CANDIDATE"

            summary = {
                "schema": "void.apollyon-abaddon.actual-joint-sparring-summary.v1",
                "run_id": run_id,
                "generation_id": GENERATION,
                "runtime_image_id": IMAGE_ID,
                "engine_commit": ENGINE_COMMIT,
                "war_college_commit": WAR_COLLEGE_COMMIT,
                "runtime_report_sha256": RUNTIME_REPORT_SHA,
                "joint_training_attestation_sha256": att_sha,
                "runner_sha256": runner_sha,
                "seed": args.seed,
                "abaddon_doctrine": args.doctrine,
                "rounds_completed": completed_rounds,
                "ticks_per_round": args.ticks_per_round,
                "final_tick": states["Multi0"]["tick"],
                "status": final_status,
                "winner": winner,
                "outcome": outcome,
                "apollyon_final": compact_state(states["Multi0"]),
                "abaddon_final": compact_state(states["Multi1"]),
                "candidate_only": True,
                "review_required": True,
                "automatic_corpus_admission": False,
                "automatic_apollyon_weight_mutation": False,
                "automatic_abaddon_policy_promotion": False,
            }
            summary_path.write_text(
                json.dumps(summary, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

            corpus_sha = sha(corpus)
            summary_sha = sha(summary_path)
            manifest = {
                "schema": "void.apollyon-abaddon.actual-joint-sparring-manifest.v1",
                "run_id": run_id,
                "trajectory_sha256": corpus_sha,
                "summary_sha256": summary_sha,
                "joint_training_attestation_sha256": att_sha,
                "generation_id": GENERATION,
                "candidate_only": True,
                "review_required": True,
                "admitted": False,
            }
            manifest_path.write_text(
                json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

            print("=== JOINT SPARRING VERDICT ===")
            print(f"run_id={run_id}")
            print(f"rounds_completed={completed_rounds}")
            print(f"final_tick={states['Multi0']['tick']}")
            print(f"outcome={outcome}")
            print(f"winner={winner or 'none'}")
            print(f"trajectory_sha256={corpus_sha}")
            print(f"summary_sha256={summary_sha}")
            print(f"run_dir={run_dir}")
            print("actual_apollyon_vs_actual_abaddon=true")
            print("joint_same_tick_training=true")
            print("candidate_only=true")
            print("automatic_corpus_admission=false")
            print("automatic_apollyon_weight_mutation=false")
            print("automatic_abaddon_policy_promotion=false")
            print("next_step=review_joint_trajectory_and_generate_bounded_refinement_candidates")
            print("VOID_ACTUAL_APOLLYON_VS_ABADDON_JOINT_SPARRING_BATCH_V1_2_GREEN")

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
            inspect = run(["docker", "inspect", container_name], check=False, quiet=True)
            if inspect.returncode == 0:
                run(["docker", "rm", "-f", container_name], check=False, quiet=True)
            print("engine_container_removed=true")

            if helper_started:
                helper.cleanup()
            print("joint_sparring_cleanup_complete=true")

    # No git or production mutation is allowed.
    if out(["git", "status", "--porcelain", "--untracked-files=no"], cwd=OPENRA):
        raise RuntimeError("OpenRA tracked worktree changed during sparring")
    if out(["git", "status", "--porcelain", "--untracked-files=no"], cwd=RL):
        raise RuntimeError("War College tracked worktree changed during sparring")
    print("post_run_frozen_worktrees_green=true")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR={exc}", file=sys.stderr)
        print("VOID_ACTUAL_APOLLYON_VS_ABADDON_JOINT_SPARRING_BATCH_V1_2_RED", file=sys.stderr)
        raise
