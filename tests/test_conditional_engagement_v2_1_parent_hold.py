from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from tools import conditional_engagement_v2_1_duel_wrapper as wrapper_module


def test_parent_wrapper_error_receives_v21_terminal_hold(monkeypatch, capsys):
    def fail(_argv=None):
        raise wrapper_module.parent.WrapperError("parent loader failed")

    monkeypatch.setattr(wrapper_module, "main", fail)
    assert wrapper_module.cli([]) == 2
    captured = capsys.readouterr()
    assert "VOID_CONDITIONAL_ENGAGEMENT_V2_1_WRAPPER_HOLD" in captured.err
    assert "blocker=parent loader failed" in captured.err


def test_direct_path_execution_from_foreign_cwd_loads_repo_parent(tmp_path):
    wrapper = Path(wrapper_module.__file__).resolve()
    result = subprocess.run(
        [
            sys.executable,
            str(wrapper),
            "--v2-1-source-dir",
            str(tmp_path / "missing-source"),
        ],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 2
    assert "VOID_CONDITIONAL_ENGAGEMENT_V2_1_WRAPPER_HOLD" in result.stderr
    assert "V2.1 source dir missing" in result.stderr
    assert "ModuleNotFoundError" not in result.stderr
