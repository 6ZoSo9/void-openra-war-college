#!/usr/bin/env python3
"""Fail-closed training-utility metrics for JointAdvance spar trajectories."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from ._spar_analyzer import analyze_trajectory
from ._spar_contract import ContractError
from ._spar_metrics import contact_episodes, trade_ratio, visible_count

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
