from __future__ import annotations

import re
from pathlib import Path

from openra_env.server.openra_environment import OpenRAEnvironment


AFFORDANCE = (
    'Interface fact: move_units accepts unit_ids="all_idle" to select '
    "the currently idle combat units; target_x and target_y are map-cell "
    "coordinates and must stay within the reported map width and height. "
    "This describes existing tool syntax only and does not require any "
    "particular action or destination."
)


def _default_prompt() -> str:
    return (
        Path(__file__).resolve().parents[1]
        / "openra_env"
        / "prompts"
        / "default.txt"
    ).read_text(encoding="utf-8")


def test_default_prompt_exposes_exact_factual_all_idle_affordance_once():
    prompt = _default_prompt()

    assert prompt.count(AFFORDANCE) == 1
    assert 'unit_ids="all_idle"' in AFFORDANCE
    assert "target_x" in AFFORDANCE
    assert "target_y" in AFFORDANCE
    assert "reported map width and height" in AFFORDANCE


def test_affordance_does_not_prescribe_scouting_or_destination():
    lower = AFFORDANCE.lower()

    assert "scout" not in lower
    assert "enemy" not in lower
    assert "least-explored" not in lower
    assert "quadrant" not in lower
    assert "move now" not in lower
    assert "you should" not in lower
    assert re.search(r"\btarget_x\b", AFFORDANCE)
    assert re.search(r"\btarget_y\b", AFFORDANCE)
    assert not re.search(r"\(\s*\d+\s*,\s*\d+\s*\)", AFFORDANCE)


def test_all_idle_runtime_selector_means_idle_combat_only():
    env = OpenRAEnvironment.__new__(OpenRAEnvironment)
    obs = {
        "units": [
            {
                "actor_id": 101,
                "type": "e1",
                "can_attack": True,
                "is_idle": True,
            },
            {
                "actor_id": 102,
                "type": "e1",
                "can_attack": True,
                "is_idle": False,
            },
            {
                "actor_id": 103,
                "type": "harv",
                "can_attack": False,
                "is_idle": True,
            },
        ]
    }

    assert env._resolve_unit_ids("all_idle", obs) == [101]
