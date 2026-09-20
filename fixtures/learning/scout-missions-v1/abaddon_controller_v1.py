"""VOID-side deterministic Abaddon controller V1.

Consumes canonical OpenRA-RL game-state dictionaries and emits one neutral tool
decision. Imports no OpenRA/OpenRA-RL implementation modules.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
import hashlib
import json
import re
from typing import Any

SCHEMA = "void.abaddon.decision.v1"
DOCTRINES = (
    "RUSHER","TURTLE","FLANKER","FEINTER","COUNTERPUNCHER",
    "ECONOMIST","AMBUSHER","ATTRITION","MOBILE_DEFENSE","FORTRESS",
)
INFANTRY = {"e1","e2","e3","e4","e6"}

@dataclass
class Memory:
    doctrine: str
    seed: int
    turn: int = 0
    scout_targets: list[list[int]] = field(default_factory=list)
    pressure_actions: int = 0
    last_action_sha256: str = ""

PROFILES = {
    "RUSHER":          dict(inf=5, veh=1, group=4, defensive=False, static=False, scout=False),
    "TURTLE":          dict(inf=5, veh=2, group=5, defensive=True,  static=True,  scout=True),
    "FLANKER":         dict(inf=5, veh=2, group=4, defensive=False, static=False, scout=True),
    "FEINTER":         dict(inf=6, veh=2, group=4, defensive=False, static=False, scout=True),
    "COUNTERPUNCHER":  dict(inf=5, veh=2, group=4, defensive=True,  static=False, scout=True),
    "ECONOMIST":       dict(inf=4, veh=1, group=4, defensive=True,  static=False, scout=True),
    "AMBUSHER":        dict(inf=5, veh=1, group=4, defensive=True,  static=False, scout=True),
    "ATTRITION":       dict(inf=6, veh=2, group=4, defensive=False, static=False, scout=True),
    "MOBILE_DEFENSE":  dict(inf=5, veh=3, group=4, defensive=True,  static=False, scout=True),
    "FORTRESS":        dict(inf=6, veh=3, group=6, defensive=True,  static=True,  scout=True),
}

TUNABLE_DEFAULTS = {
    "power_margin_min": 35,
    "weap_power_min": 50,
    "scout_current_min": 10,
    "scout_history_min": 16,
    "advance_ticks": 50,
}
TUNABLE_BOUNDS = {
    "inf": (3, 10),
    "veh": (0, 5),
    "group": (2, 10),
    "power_margin_min": (20, 100),
    "weap_power_min": (30, 140),
    "scout_current_min": (8, 24),
    "scout_history_min": (12, 40),
    "advance_ticks": (25, 100),
}
for _profile in PROFILES.values():
    for _k, _v in TUNABLE_DEFAULTS.items():
        _profile.setdefault(_k, _v)

def _i(v, d=0):
    try: return int(v)
    except Exception: return d

def _id(x):
    try: return int(x.get("id"))
    except Exception: return None

def _units(o): return [x for x in (o.get("units_summary") or []) if isinstance(x, dict)]
def _buildings(o): return [x for x in (o.get("buildings_summary") or []) if isinstance(x, dict)]
def _enemies(o): return [x for x in (o.get("enemy_summary") or []) if isinstance(x, dict)]
def _enemy_buildings(o): return [x for x in (o.get("enemy_buildings_summary") or []) if isinstance(x, dict)]
def _combat(o): return [x for x in _units(o) if bool(x.get("can_attack"))]
def _inf(o): return [x for x in _combat(o) if str(x.get("type")) in INFANTRY]
def _veh(o): return [x for x in _combat(o) if str(x.get("type")) not in INFANTRY]
def _harv(o): return [x for x in _units(o) if str(x.get("type")) == "harv"]
def _ids(xs): return sorted(x for x in (_id(v) for v in xs) if x is not None)
def _has(o, types): return any(str(x.get("type")) in types for x in _buildings(o))
def _queued(o, t): return any(str(x).startswith(t+"@") for x in (o.get("production_items") or []))
def _avail(o, t): return t in set(map(str, o.get("available_production") or []))

def _power(o):
    if "power_balance" in o: return _i(o.get("power_balance"))
    e=o.get("economy") or {}
    return _i(e.get("power_provided"))-_i(e.get("power_drained"))

def _liquid(o):
    e=o.get("economy") or {}
    return _i(e.get("cash"))+_i(e.get("ore"))

def _pos(x):
    try: return int(x.get("cell_x")), int(x.get("cell_y"))
    except Exception: return None

def _map(o):
    m=o.get("map") or {}
    return max(1,_i(m.get("width"),112)), max(1,_i(m.get("height"),54))

def _base(o):
    for t in ("fact","proc","tent","weap","powr"):
        for b in _buildings(o):
            if str(b.get("type"))==t and _pos(b): return _pos(b)
    w,h=_map(o); return (w//2,h//2)

def _dist(a,b): return abs(a[0]-b[0])+abs(a[1]-b[1])

def _digest(v):
    return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def _minimap_targets(o):
    text=str(o.get("minimap") or "")
    lines=text.splitlines()
    if not lines: return []
    m=re.match(r"Map \((\d+)x(\d+), 1cell=(\d+)x(\d+)\):",lines[0].strip())
    if not m: return []
    gw,gh,sx,sy=map(int,m.groups())
    out=[]
    for gy,row in enumerate(lines[1:1+gh]):
        for gx,ch in enumerate(row[:gw]):
            if ch=="#": out.append((gx*sx+sx//2,gy*sy+sy//2))
    return out

def _scout_target(o, mem, scout_id, current_min=10, history_min=16):
    scout=next((u for u in _units(o) if _id(u)==scout_id),None)
    origin=_pos(scout or {}) or _base(o)
    history=[tuple(p) for p in mem.scout_targets]
    candidates=_minimap_targets(o)
    if not candidates:
        w,h=_map(o)
        candidates=[(10,10),(w-11,10),(w-11,h-11),(10,h-11),(w//2,10),(w//2,h-11)]
    viable=[]
    for t in candidates:
        if _dist(origin,t)<int(current_min): continue
        if history and min(_dist(t,p) for p in history)<int(history_min): continue
        viable.append(t)
    if not viable: return None
    return max(viable,key=lambda t:(_dist(origin,t),min((_dist(t,p) for p in history),default=10**6),t[0],t[1]))

def _decision(mem,o,reasons,tool,args):
    action={"tool":tool,"arguments":args}
    mem.turn+=1
    mem.last_action_sha256=_digest(action)
    return {
        "schema":SCHEMA,"identity":"Abaddon","controller_version":1,
        "deterministic":True,"llm":False,"doctrine":mem.doctrine,
        "seed":mem.seed,"tick":_i(o.get("tick")),"turn":mem.turn,
        "reason_codes":reasons,"action":action,"memory":asdict(mem),
    }

class AbaddonController:
    def __init__(self, doctrine: str, seed: int=2050, policy: dict[str, Any] | None=None):
        doctrine=str(doctrine).upper()
        if doctrine not in PROFILES: raise ValueError(f"unsupported doctrine: {doctrine}")
        self.profile=dict(PROFILES[doctrine])
        if policy:
            for key, value in policy.items():
                if key not in TUNABLE_BOUNDS:
                    raise ValueError(f"unsupported tunable policy key: {key}")
                lo, hi=TUNABLE_BOUNDS[key]
                iv=_i(value, lo-1)
                if iv<lo or iv>hi:
                    raise ValueError(f"policy {key} outside bounds {lo}..{hi}: {value}")
                self.profile[key]=iv
        self.memory=Memory(doctrine=doctrine,seed=int(seed))

    def decide(self, observation: dict[str,Any]) -> dict[str,Any]:
        o=observation if isinstance(observation,dict) else {}
        p=self.profile; m=self.memory
        avail=set(map(str,o.get("available_production") or []))
        combat=_combat(o); infantry=_inf(o); vehicles=_veh(o); enemies=_enemies(o)
        power=_power(o); liquid=_liquid(o)

        if not _has(o,{"fact"}):
            mcvs=_ids([u for u in _units(o) if str(u.get("type")) in {"mcv","amcv"}])
            if mcvs: return _decision(m,o,["DEPLOY_MCV"],"deploy_unit",{"unit_id":mcvs[0]})

        # Hard invariant learned from the overnight soak: never expand optional
        # production while power-tight.
        if power<p["power_margin_min"] and "powr" in avail and not _queued(o,"powr"):
            return _decision(m,o,["POWER_MARGIN_LOW","BUILD_POWER_BEFORE_EXPANSION"],
                             "build_and_place",{"building_type":"powr"})

        e=o.get("economy") or {}
        if (not _has(o,{"proc"}) or _i(e.get("harvester_count"))<1) and "proc" in avail and not _queued(o,"proc"):
            return _decision(m,o,["ESTABLISH_REFINERY_HARVESTER"],
                             "build_and_place",{"building_type":"proc"})

        if not _has(o,{"tent","barr"}):
            b="tent" if "tent" in avail else ("barr" if "barr" in avail else None)
            if b and not _queued(o,b):
                return _decision(m,o,["ESTABLISH_INFANTRY_PRODUCTION"],
                                 "build_and_place",{"building_type":b})

        if len(infantry)<p["inf"] and "e1" in avail and not _queued(o,"e1"):
            count=max(1,min(3,p["inf"]-len(infantry)))
            return _decision(m,o,["INFANTRY_SCREEN_BELOW_TARGET"],
                             "build_unit",{"unit_type":"e1","count":count})

        if p["veh"]>0 and not _has(o,{"weap"}) and "weap" in avail and not _queued(o,"weap"):
            if power<p["weap_power_min"] and "powr" in avail and not _queued(o,"powr"):
                return _decision(m,o,["VEHICLE_TECH_DESIRED","POWER_HEADROOM_REQUIRED"],
                                 "build_and_place",{"building_type":"powr"})
            if power>=p["weap_power_min"] and liquid>=2200:
                return _decision(m,o,["VEHICLE_TECH_DESIRED","POWER_HEADROOM_GREEN"],
                                 "build_and_place",{"building_type":"weap"})

        if _has(o,{"weap"}) and len(vehicles)<p["veh"]:
            v=next((x for x in ("1tnk","jeep") if x in avail and not _queued(o,x)),None)
            if v: return _decision(m,o,["VEHICLE_FORCE_BELOW_TARGET"],
                                   "build_unit",{"unit_type":v,"count":1})

        if enemies:
            bx,by=_base(o)
            target=min(enemies,key=lambda x:(_dist(_pos(x) or (999999,999999),(bx,by)),_id(x) or 999999))
            tid=_id(target)
            harvs=_ids(_harv(o))
            if p["defensive"] and harvs and combat:
                return _decision(m,o,["CONTACT_VISIBLE","PROTECT_ECONOMIC_CORE"],
                                 "guard_target",{"target_actor_id":harvs[0],"unit_ids":"all_combat"})
            if tid is not None and len(combat)>=p["group"]:
                m.pressure_actions+=1
                return _decision(m,o,["CONTACT_VISIBLE","CONCENTRATED_RESPONSE"],
                                 "attack_target",{"target_actor_id":tid,"unit_ids":"all_combat"})
            if harvs and combat:
                return _decision(m,o,["CONTACT_VISIBLE","FORCE_NOT_CONCENTRATED","PRESERVE_FORCE"],
                                 "guard_target",{"target_actor_id":harvs[0],"unit_ids":"all_combat"})

        enemy_buildings=_enemy_buildings(o)
        if enemy_buildings and len(combat)>=p["group"]:
            target=sorted(enemy_buildings,key=lambda x:(0 if str(x.get("type")) in {"fact","proc"} else 1,_id(x) or 999999))[0]
            tid=_id(target)
            if tid is not None:
                m.pressure_actions+=1
                return _decision(m,o,["ENEMY_BASE_VISIBLE","CONCENTRATED_PRESSURE"],
                                 "attack_target",{"target_actor_id":tid,"unit_ids":"all_combat"})

        if p["static"] and power>=50 and liquid>=1800 and not _has(o,{"pbox","hbox","gun"}):
            d=next((x for x in ("pbox","gun","hbox") if x in avail and not _queued(o,x)),None)
            if d: return _decision(m,o,["FORTIFY_CORE","POWER_HEADROOM_GREEN"],
                                   "build_and_place",{"building_type":d})

        scout_ids=_ids(infantry)
        if scout_ids and not enemies and not enemy_buildings and (p["scout"] or _i(o.get("explored_percent"))<35):
            sid=scout_ids[0]
            t=_scout_target(o,m,sid,p["scout_current_min"],p["scout_history_min"])
            if t:
                m.scout_targets.append([t[0],t[1]])
                return _decision(m,o,["INTELLIGENCE_GAP","SYSTEMATIC_NEW_SCOUT_SECTOR"],
                                 "move_units",{"unit_ids":str(sid),"target_x":t[0],"target_y":t[1]})

        if m.doctrine=="RUSHER" and len(combat)>=p["group"]:
            w,h=_map(o); bx,by=_base(o)
            tx=10 if bx>w//2 else w-11; ty=10 if by>h//2 else h-11
            m.pressure_actions+=1
            return _decision(m,o,["RUSH_WINDOW","GROUPED_ATTACK_MOVE"],
                             "attack_move",{"unit_ids":"all_combat","target_x":tx,"target_y":ty})

        if m.doctrine=="ECONOMIST" and power>=60 and liquid>=3500 and "silo" in avail and not _has(o,{"silo"}) and not _queued(o,"silo"):
            return _decision(m,o,["ECONOMIC_SURPLUS","ADD_STORAGE"],
                             "build_and_place",{"building_type":"silo"})

        return _decision(m,o,["NO_HIGHER_PRIORITY_ACTION"],"advance",{"ticks":p["advance_ticks"]})

class AbaddonDirector:
    PROXY={
        "RUSHER":("rush","rush-defense"),"TURTLE":("turtle","turtle-breaker"),
        "FLANKER":("normal","fog-hunt"),"FEINTER":("normal","fog-hunt"),
        "COUNTERPUNCHER":("rush","rush-defense"),"ECONOMIST":("rush","economy-under-fire"),
        "AMBUSHER":("normal","fog-hunt"),"ATTRITION":("rush","rush-defense"),
        "MOBILE_DEFENSE":("normal","rush-defense"),"FORTRESS":("turtle","turtle-breaker"),
    }
    def __init__(self, seed_base:int=2050): self.seed_base=int(seed_base)

    @staticmethod
    def flags(history):
        blob=json.dumps(history,sort_keys=True).lower()
        return {
            "power_failure": int("power_nonnegative" in blob and "false" in blob or "low power" in blob),
            "recon_failure": int("gate_6" in blob or "stale" in blob or "recon" in blob and "failure" in blob),
            "contact_nonresponse": int("post_contact" in blob and ("response_actions\": 0" in blob or "response_actions': 0" in blob)),
        }

    def choose(self, history, match_index:int):
        f=self.flags(history)
        if f["power_failure"]: cycle=("RUSHER","ATTRITION","COUNTERPUNCHER")
        elif f["recon_failure"]: cycle=("TURTLE","FORTRESS","AMBUSHER","FLANKER")
        elif f["contact_nonresponse"]: cycle=("RUSHER","COUNTERPUNCHER","MOBILE_DEFENSE")
        else: cycle=("FEINTER","ATTRITION","FORTRESS","ECONOMIST","FLANKER")
        doctrine=cycle[int(match_index)%len(cycle)]
        bot,scenario=self.PROXY[doctrine]
        seed=(self.seed_base+(int(match_index)+1)*7919)%2147483647
        return {
            "schema":"void.abaddon.director-match-plan.v1","identity":"Abaddon",
            "doctrine":doctrine,"seed":seed,"scenario":scenario,
            "proxy_bot_until_second_player_bridge":bot,
            "execution_mode":"DIRECTOR_PROXY_UNTIL_SECOND_PLAYER_BRIDGE",
            "full_abaddon_controller_active":False,"history_flags":f,
        }
