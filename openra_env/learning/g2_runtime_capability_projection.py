"""Deterministic visible-state capability projection for the G2 frontier.

The projection is a versioned source policy, not a learned model.  It consumes
only fields already returned by get_game_state and never opponent-hidden state.
"""

from __future__ import annotations

import hashlib
import json
import math
from types import MappingProxyType

SCHEMA = "void.generals.g2-runtime-capability-projection.v1"
CAPABILITIES = ("margin", "delivery", "sensing", "continuity")
MIN_CAPABILITY = 0
MAX_CAPABILITY = 1000

PROJECTION_SPEC = MappingProxyType({
    "schema": SCHEMA,
    "capabilities": CAPABILITIES,
    "domain": [MIN_CAPABILITY, MAX_CAPABILITY],
    "margin": "(economy.cash + economy.ore) // 100",
    "delivery": "military.army_value // 100",
    "sensing": "round(explored_percent * 10)",
    "continuity": (
        "own_buildings * 25 + economy.harvester_count * 40 "
        "+ trunc(power_balance / 10)"
    ),
    "hidden_or_unobserved_opponent_state_used": False,
    "model_inference_used": False,
})


class CapabilityProjectionHold(RuntimeError):
    """Fail-closed visible-state projection error."""


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


PROJECTION_SPEC_SHA256 = hashlib.sha256(
    canonical_json_bytes(dict(PROJECTION_SPEC))
).hexdigest()


def _number(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CapabilityProjectionHold("non_numeric:" + name)
    result = float(value)
    if not math.isfinite(result):
        raise CapabilityProjectionHold("non_finite:" + name)
    return result


def _bounded_int(value: float) -> int:
    return max(MIN_CAPABILITY, min(MAX_CAPABILITY, int(value)))


def _nonnegative(value: object, name: str) -> float:
    result = _number(value, name)
    if result < 0:
        raise CapabilityProjectionHold("negative:" + name)
    return result


def project_live_game_state(state: object) -> dict:
    if not isinstance(state, dict):
        raise CapabilityProjectionHold("state_not_object")
    economy = state.get("economy")
    military = state.get("military")
    if not isinstance(economy, dict):
        raise CapabilityProjectionHold("economy_not_object")
    if not isinstance(military, dict):
        raise CapabilityProjectionHold("military_not_object")

    cash = _nonnegative(economy.get("cash"), "economy.cash")
    ore = _nonnegative(economy.get("ore"), "economy.ore")
    harvesters = _nonnegative(
        economy.get("harvester_count"), "economy.harvester_count"
    )
    army_value = _nonnegative(
        military.get("army_value"), "military.army_value"
    )
    explored = _number(state.get("explored_percent"), "explored_percent")
    if explored < 0 or explored > 100:
        raise CapabilityProjectionHold("explored_percent_out_of_range")
    own_buildings = _nonnegative(
        state.get("own_buildings"), "own_buildings"
    )
    power_balance = _number(state.get("power_balance"), "power_balance")

    capabilities = {
        "margin": _bounded_int((cash + ore) // 100),
        "delivery": _bounded_int(army_value // 100),
        "sensing": _bounded_int(round(explored * 10)),
        "continuity": _bounded_int(
            own_buildings * 25
            + harvesters * 40
            + int(power_balance / 10)
        ),
    }
    deficient = min(
        CAPABILITIES,
        key=lambda name: (capabilities[name], CAPABILITIES.index(name)),
    )
    source = {
        "cash": cash,
        "ore": ore,
        "harvester_count": harvesters,
        "army_value": army_value,
        "explored_percent": explored,
        "own_buildings": own_buildings,
        "power_balance": power_balance,
    }
    result = {
        "schema": SCHEMA,
        "projection_spec_sha256": PROJECTION_SPEC_SHA256,
        "capabilities": capabilities,
        "deficient_capability": deficient,
        "visible_source": source,
        "hidden_or_unobserved_opponent_state_used": False,
        "model_inference_used": False,
    }
    result["sha256"] = hashlib.sha256(canonical_json_bytes(result)).hexdigest()
    return result


def verify_projection(projection: object) -> dict:
    if not isinstance(projection, dict):
        raise CapabilityProjectionHold("projection_not_object")
    value = dict(projection)
    supplied = value.pop("sha256", None)
    actual = hashlib.sha256(canonical_json_bytes(value)).hexdigest()
    if supplied != actual:
        raise CapabilityProjectionHold("projection_internal_hash")
    if value.get("schema") != SCHEMA:
        raise CapabilityProjectionHold("projection_schema")
    if value.get("projection_spec_sha256") != PROJECTION_SPEC_SHA256:
        raise CapabilityProjectionHold("projection_spec")
    capabilities = value.get("capabilities")
    if not isinstance(capabilities, dict) or set(capabilities) != set(CAPABILITIES):
        raise CapabilityProjectionHold("capability_vector_shape")
    for name in CAPABILITIES:
        raw = capabilities.get(name)
        if isinstance(raw, bool) or not isinstance(raw, int):
            raise CapabilityProjectionHold("capability_non_integer:" + name)
        if raw < MIN_CAPABILITY or raw > MAX_CAPABILITY:
            raise CapabilityProjectionHold("capability_out_of_range:" + name)
    if value.get("deficient_capability") not in CAPABILITIES:
        raise CapabilityProjectionHold("deficient_capability")
    return projection
