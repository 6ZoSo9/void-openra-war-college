from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from tools.conditional_engagement_v2_2_g1_destination_guard_duel_wrapper import (
    _destination_guard_text,
    _required_argument_names,
)


def test_required_argument_names_reads_exact_openai_function_schema():
    tools = [
        {
            "type": "function",
            "function": {
                "name": "move_units",
                "parameters": {
                    "type": "object",
                    "required": ["unit_ids", "target_x", "target_y"],
                    "properties": {},
                },
            },
        }
    ]
    assert _required_argument_names(tools, "move_units") == [
        "unit_ids",
        "target_x",
        "target_y",
    ]


def test_required_argument_names_never_invents_missing_schema():
    assert _required_argument_names([], "move_units") == []
    assert _required_argument_names([{"name": "attack_move"}], "move_units") == []


def test_destination_guard_forbids_sentinel_and_allows_backoff():
    text = _destination_guard_text(
        "move_units",
        ["unit_ids", "target_x", "target_y"],
    )
    assert "LEARNED_TOOL_REQUIRED_ARGUMENTS=unit_ids,target_x,target_y" in text
    assert 'unit_ids="all_combat"' in text
    assert "never use -1" in text
    assert "never omit" in text
    assert "current observation" in text
    assert "do not choose move_units" in text
    assert "another currently offered host-authorized tool" in text


def test_destination_guard_is_silent_for_other_tools():
    assert _destination_guard_text("attack_move", ["target_x", "target_y"]) == ""
    assert _destination_guard_text(None, []) == ""


def test_destination_guard_absolute_path_startup_from_foreign_cwd(tmp_path):
    script = (
        Path(__file__).resolve().parents[1]
        / "tools"
        / "conditional_engagement_v2_2_g1_destination_guard_duel_wrapper.py"
    )
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )
    combined = result.stdout + result.stderr
    assert result.returncode == 2
    assert "ModuleNotFoundError" not in combined
    assert "--v2-2-source-dir" in combined
    assert "--general-brain-adapter" in combined
