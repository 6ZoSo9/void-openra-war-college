from __future__ import annotations

from pathlib import Path

from openra_env.server.openra_environment import OpenRAEnvironment


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "openra_env/server/openra_environment.py"


def test_building_queue_hold_blocks_later_building_item():
    result = OpenRAEnvironment._placeable_queue_hold(
        "tent",
        [
            {
                "queue_type": "Building",
                "item": "proc",
                "progress": 0.24,
                "remaining_ticks": 638,
                "paused": False,
            }
        ],
        553,
    )

    assert result is not None
    assert result["production_queue_hold"] is True
    assert result["executed"] is False
    assert result["requested_item"] == "tent"
    assert result["queue_type"] == "Building"
    assert result["pending_items"] == ["proc"]
    assert result["tick"] == 553
    assert "advance()" in result["next_step"]


def test_later_building_requests_cannot_overtake_older_building_work():
    production = [
        {"queue_type": "Building", "item": "tent", "progress": 0.0},
        {"queue_type": "Building", "item": "powr", "progress": 0.0},
    ]
    result = OpenRAEnvironment._placeable_queue_hold("syrd", production, 1077)

    assert result is not None
    assert result["pending_items"] == ["tent", "powr"]
    assert "tent, powr" in result["reason"]


def test_defense_queue_remains_independent_from_building_queue():
    production = [{"queue_type": "Building", "item": "proc", "progress": 0.36}]
    assert OpenRAEnvironment._placeable_queue_hold("brik", production, 657) is None


def test_canonical_defense_queue_membership_covers_nonplacement_bias_items():
    defense_items = {
        "mslo", "gap", "iron", "pdox",
        "tsla", "agun", "sam", "pbox", "hbox", "gun", "ftur",
        "silo", "sbag", "fenc", "brik",
    }

    for item in defense_items:
        assert OpenRAEnvironment._placeable_queue_type(item) == "Defense"

    for item in {"powr", "tent", "proc", "weap", "syrd", "dome"}:
        assert OpenRAEnvironment._placeable_queue_type(item) == "Building"


def test_building_queue_remains_independent_from_defense_queue():
    production = [{"queue_type": "Defense", "item": "brik", "progress": 0.4}]
    assert OpenRAEnvironment._placeable_queue_hold("tent", production, 700) is None


def test_ready_but_unplaced_same_queue_item_still_holds():
    result = OpenRAEnvironment._placeable_queue_hold(
        "weap",
        [
            {
                "queue_type": "Building",
                "item": "proc",
                "progress": 1.0,
                "remaining_ticks": 0,
                "paused": False,
            }
        ],
        1200,
    )

    assert result is not None
    assert result["pending_items"] == ["proc"]


def test_malformed_or_same_item_entries_do_not_create_false_hold():
    production = [
        None,
        "bad",
        {"queue_type": "Building", "item": "tent", "progress": 0.5},
        {"queue_type": "Defense", "item": "gun", "progress": 0.3},
        {"queue_type": "Building", "item": ""},
    ]

    assert OpenRAEnvironment._placeable_queue_hold("tent", production, True) is None
    assert OpenRAEnvironment._placeable_queue_hold("tent", None, 5) is None


def test_build_and_place_calls_queue_hold_before_world_command():
    source = SOURCE.read_text(encoding="utf-8")
    start = source.index("def build_and_place(")
    end = source.index("def place_building(", start)
    block = source[start:end]

    hold_call = block.index("queue_hold = env._placeable_queue_hold(")
    execute_call = block.index(
        "commands = [CommandModel(action=ActionType.BUILD, item_type=building_type)]"
    )

    assert hold_call < execute_call
    assert "if queue_hold is not None:" in block
    assert "return queue_hold" in block


def test_build_structure_contract_remains_unchanged():
    source = SOURCE.read_text(encoding="utf-8")
    start = source.index("def build_structure(")
    end = source.index("def build_and_place(", start)
    block = source[start:end]

    assert "queue_hold = env._placeable_queue_hold(" not in block
