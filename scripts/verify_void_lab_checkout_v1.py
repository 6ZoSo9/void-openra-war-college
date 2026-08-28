#!/usr/bin/env python3
"""Fail-closed source/checkout verifier for the VOID OpenRA lab.

The source-only mode is safe for CI without private-submodule credentials.  It
verifies committed/tracked composition, but explicitly does not assert exact
worktree composition.  The default mode additionally requires both worktrees
to be exact and clean, including the absence of untracked runtime inputs,
before a designated-host build or benchmark is attempted.
"""

from __future__ import annotations

import argparse
import configparser
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence


MARKER = "VOID_WAR_COLLEGE_LAB_CHECKOUT_CONTRACT_V1"
SCHEMA_VERSION = 2
WAR_COLLEGE_FROZEN_COMMIT = "973802ef0a614e5afa782ff20e231e18966ae3e5"
ENGINE_FROZEN_COMMIT = "1607a7a6501d42a47638393ecef8b22831064932"
GENERATION = "ad1926569b12466c"
ENGINE_SUBMODULE_PATH = "OpenRA"
ENGINE_REPOSITORY_URL = "https://github.com/6ZoSo9/void-openra-engine.git"


class VerificationError(RuntimeError):
    """Raised when repository evidence cannot be obtained unambiguously."""


@dataclass(frozen=True)
class Probe:
    war_college_head: str
    war_college_frozen_is_ancestor: bool
    engine_gitlink_commit: str
    engine_repository_url: str
    engine_checkout_present: bool
    engine_checkout_head: str | None
    engine_tracked_checkout_clean: bool | None
    engine_exact_checkout_clean: bool | None
    war_college_tracked_checkout_clean: bool
    war_college_exact_checkout_clean: bool


def _run_git(root: Path, args: Sequence[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown git error"
        raise VerificationError(f"git {' '.join(args)} failed: {detail}")
    return result


def git_checkout_clean(
    root: Path, *, include_untracked: bool, ignore_submodules: bool = False
) -> bool:
    """Return exact git cleanliness under the requested explicit policy."""
    args = [
        "status",
        "--porcelain",
        "--untracked-files=all" if include_untracked else "--untracked-files=no",
    ]
    if ignore_submodules:
        args.append("--ignore-submodules=all")
    return not bool(_run_git(root, args).stdout.strip())


def parse_engine_gitlink(raw: str) -> str:
    lines = [line for line in raw.splitlines() if line.strip()]
    if len(lines) != 1:
        raise VerificationError("OpenRA gitlink must resolve to exactly one tree entry")
    metadata, separator, path = lines[0].partition("\t")
    fields = metadata.split()
    if separator != "\t" or path != ENGINE_SUBMODULE_PATH or len(fields) != 3:
        raise VerificationError("OpenRA gitlink tree entry is malformed")
    mode, object_type, commit = fields
    if mode != "160000" or object_type != "commit":
        raise VerificationError("OpenRA must be a mode-160000 gitlink")
    if len(commit) != 40 or any(ch not in "0123456789abcdef" for ch in commit):
        raise VerificationError("OpenRA gitlink commit is not canonical lowercase SHA-1")
    return commit


def read_engine_repository_url(root: Path) -> str:
    modules = root / ".gitmodules"
    try:
        content = modules.read_text(encoding="utf-8")
    except OSError as error:
        raise VerificationError(f"cannot read .gitmodules: {error}") from error
    parser = configparser.ConfigParser(interpolation=None)
    try:
        parser.read_string(content)
        return parser['submodule "OpenRA"']["url"].strip()
    except (configparser.Error, KeyError) as error:
        raise VerificationError(".gitmodules lacks the exact OpenRA URL") from error


def _is_ancestor(root: Path, ancestor: str, descendant: str) -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    detail = result.stderr.strip() or result.stdout.strip() or "unknown git error"
    raise VerificationError(f"cannot prove frozen War College ancestry: {detail}")


def collect_probe(root: Path) -> Probe:
    repository_root = Path(_run_git(root, ["rev-parse", "--show-toplevel"]).stdout.strip())
    if repository_root.resolve() != root.resolve():
        raise VerificationError("--repo-root is not the War College repository root")

    head = _run_git(root, ["rev-parse", "HEAD"]).stdout.strip()
    gitlink = parse_engine_gitlink(
        _run_git(root, ["ls-tree", "HEAD", "--", ENGINE_SUBMODULE_PATH]).stdout
    )
    parent_tracked_clean = git_checkout_clean(
        root, include_untracked=False, ignore_submodules=True
    )
    parent_exact_clean = git_checkout_clean(
        root, include_untracked=True, ignore_submodules=True
    )

    engine_root = root / ENGINE_SUBMODULE_PATH
    engine_present = (engine_root / ".git").exists()
    engine_head: str | None = None
    engine_tracked_clean: bool | None = None
    engine_exact_clean: bool | None = None
    if engine_present:
        engine_head = _run_git(
            engine_root, ["rev-parse", "HEAD"]
        ).stdout.strip()
        engine_tracked_clean = git_checkout_clean(
            engine_root, include_untracked=False
        )
        engine_exact_clean = git_checkout_clean(
            engine_root, include_untracked=True
        )

    return Probe(
        war_college_head=head,
        war_college_frozen_is_ancestor=_is_ancestor(
            root, WAR_COLLEGE_FROZEN_COMMIT, head
        ),
        engine_gitlink_commit=gitlink,
        engine_repository_url=read_engine_repository_url(root),
        engine_checkout_present=engine_present,
        engine_checkout_head=engine_head,
        engine_tracked_checkout_clean=engine_tracked_clean,
        engine_exact_checkout_clean=engine_exact_clean,
        war_college_tracked_checkout_clean=parent_tracked_clean,
        war_college_exact_checkout_clean=parent_exact_clean,
    )


def evaluate_probe(probe: Probe, *, source_only: bool = False) -> dict[str, object]:
    checks = {
        "war_college_frozen_is_ancestor": probe.war_college_frozen_is_ancestor,
        "engine_gitlink_is_frozen": probe.engine_gitlink_commit == ENGINE_FROZEN_COMMIT,
        "engine_repository_url_is_exact": probe.engine_repository_url
        == ENGINE_REPOSITORY_URL,
        "war_college_tracked_checkout_clean": probe.war_college_tracked_checkout_clean,
        "war_college_exact_checkout_clean": probe.war_college_exact_checkout_clean,
        "engine_checkout_present": probe.engine_checkout_present,
        "engine_checkout_matches_gitlink": probe.engine_checkout_present
        and probe.engine_checkout_head == probe.engine_gitlink_commit,
        "engine_checkout_is_frozen": probe.engine_checkout_present
        and probe.engine_checkout_head == ENGINE_FROZEN_COMMIT,
        "engine_tracked_checkout_clean": probe.engine_tracked_checkout_clean is True,
        "engine_exact_checkout_clean": probe.engine_exact_checkout_clean is True,
    }
    source_keys = (
        "war_college_frozen_is_ancestor",
        "engine_gitlink_is_frozen",
        "engine_repository_url_is_exact",
        "war_college_tracked_checkout_clean",
    )
    checkout_keys = source_keys + (
        "war_college_exact_checkout_clean",
        "engine_checkout_present",
        "engine_checkout_matches_gitlink",
        "engine_checkout_is_frozen",
        "engine_tracked_checkout_clean",
        "engine_exact_checkout_clean",
    )
    source_green = all(checks[key] for key in source_keys)
    checkout_green = all(checks[key] for key in checkout_keys)
    holds = [name for name, passed in checks.items() if not passed]
    return {
        "schema_version": SCHEMA_VERSION,
        "marker": MARKER,
        "generation": GENERATION,
        "preserved_baseline": {
            "war_college_commit": WAR_COLLEGE_FROZEN_COMMIT,
            "engine_commit": ENGINE_FROZEN_COMMIT,
        },
        "observed": {
            "war_college_head": probe.war_college_head,
            "engine_gitlink_commit": probe.engine_gitlink_commit,
            "engine_repository_url": probe.engine_repository_url,
            "engine_checkout_head": probe.engine_checkout_head,
        },
        "checks": checks,
        "requested_contract": (
            "COMMITTED_TRACKED_COMPOSITION_ONLY"
            if source_only
            else "EXACT_WORKTREE_COMPOSITION_INCLUDING_UNTRACKED"
        ),
        "source_only_limitation": (
            "DOES_NOT_ASSERT_EXACT_DESIGNATED_HOST_COMPOSITION"
            if source_only
            else None
        ),
        "exact_checkout_evidence": checkout_green,
        "source_contract": "GREEN" if source_green else "HOLD",
        "checkout_contract": (
            "GREEN"
            if checkout_green
            else "PENDING_ENGINE_CHECKOUT"
            if source_green and not probe.engine_checkout_present
            else "HOLD"
        ),
        "runtime_evidence": "PENDING_DESIGNATED_HOST",
        "holds": holds,
    }


def canonical_json(report: dict[str, object]) -> str:
    return json.dumps(report, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="War College repository root (default: current directory)",
    )
    parser.add_argument(
        "--source-only",
        action="store_true",
        help="Allow an absent engine checkout while still verifying the committed gitlink",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = evaluate_probe(
            collect_probe(args.repo_root.resolve()), source_only=args.source_only
        )
    except VerificationError as error:
        report = {
            "schema_version": SCHEMA_VERSION,
            "marker": MARKER,
            "generation": GENERATION,
            "source_contract": "HOLD",
            "checkout_contract": "HOLD",
            "runtime_evidence": "PENDING_DESIGNATED_HOST",
            "requested_contract": (
                "COMMITTED_TRACKED_COMPOSITION_ONLY"
                if args.source_only
                else "EXACT_WORKTREE_COMPOSITION_INCLUDING_UNTRACKED"
            ),
            "source_only_limitation": (
                "DOES_NOT_ASSERT_EXACT_DESIGNATED_HOST_COMPOSITION"
                if args.source_only
                else None
            ),
            "exact_checkout_evidence": False,
            "holds": [str(error)],
        }
    print(canonical_json(report))
    if report.get("source_contract") != "GREEN":
        return 1
    if args.source_only:
        return 0
    return 0 if report.get("checkout_contract") == "GREEN" else 1


if __name__ == "__main__":
    sys.exit(main())
