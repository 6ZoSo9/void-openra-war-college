#!/usr/bin/env python3
"""Fail-closed training-utility metrics for JointAdvance spar trajectories."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from ._spar_analyzer import analyze_trajectory as _analyze_trajectory_base
from ._spar_conditional_v2 import validate_conditional_v2_evidence
from ._spar_conditional_v2_1 import validate_conditional_v21_evidence
from ._spar_conditional_v2_2 import validate_conditional_v22_evidence
from ._spar_contract import ContractError
from ._spar_metrics import (
    contact_episodes as contact_episodes,
    trade_ratio as trade_ratio,
    visible_count as visible_count,
)
from .spar_v22_conversion_utility import analyze_conversion_productivity


def analyze_trajectory(
    trajectory_path: Path,
    *,
    summary_path: Path | None = None,
    expected_trajectory_sha256: str | None = None,
    expected_summary_sha256: str | None = None,
) -> dict[str, Any]:
    """Run base analysis, then verify one optional Conditional Engagement generation."""
    report = _analyze_trajectory_base(
        trajectory_path,
        summary_path=summary_path,
        expected_trajectory_sha256=expected_trajectory_sha256,
        expected_summary_sha256=expected_summary_sha256,
    )
    trajectory_sha = report["provenance"]["trajectory_sha256"]
    v2 = validate_conditional_v2_evidence(
        trajectory_path,
        expected_trajectory_sha256=trajectory_sha,
    )
    v21 = validate_conditional_v21_evidence(
        trajectory_path,
        expected_trajectory_sha256=trajectory_sha,
    )
    v22 = validate_conditional_v22_evidence(
        trajectory_path,
        expected_trajectory_sha256=trajectory_sha,
    )
    present_count = sum(
        generation.get("present") is True
        for generation in (v2, v21, v22)
    )
    if present_count > 1:
        raise ContractError("trajectory contains multiple Conditional Engagement generations")

    conversion: dict[str, Any] = {"present": False}
    if v22.get("present") is True:
        conversion = {
            "present": True,
            **analyze_conversion_productivity(
                trajectory_path,
                expected_trajectory_sha256=trajectory_sha,
            ),
        }

    report["conditional_engagement_v2"] = v2
    report["conditional_engagement_v2_1"] = v21
    report["conditional_engagement_v2_2"] = v22
    report["conditional_engagement_v2_2_conversion_utility"] = conversion
    return report


def stable_json(value: dict[str, Any]) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    ) + "\n"


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    try:
        with temporary.open("x", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if temporary.exists():
            temporary.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trajectory", required=True)
    parser.add_argument("--summary")
    parser.add_argument("--trajectory-sha256")
    parser.add_argument("--summary-sha256")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    try:
        report = analyze_trajectory(
            Path(args.trajectory),
            summary_path=Path(args.summary) if args.summary else None,
            expected_trajectory_sha256=args.trajectory_sha256,
            expected_summary_sha256=args.summary_sha256,
        )
        encoded = stable_json(report)
        atomic_write(Path(args.output), encoded) if args.output else sys.stdout.write(encoded)
        return 0
    except (ContractError, OSError) as error:
        print(f"contract error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
