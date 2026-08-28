from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_v22_wrapper_executes_by_absolute_path_from_foreign_cwd(tmp_path):
    wrapper = Path(__file__).parents[1] / "tools/conditional_engagement_v2_2_duel_wrapper.py"
    completed = subprocess.run(
        [sys.executable, str(wrapper), "--v2-2-source-dir", str(tmp_path / "missing")],
        cwd=tmp_path,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert completed.returncode == 2
    assert "VOID_CONDITIONAL_ENGAGEMENT_V2_2_WRAPPER_HOLD" in completed.stderr
    assert "V2.2 source dir missing" in completed.stderr
    assert "ModuleNotFoundError" not in completed.stderr
