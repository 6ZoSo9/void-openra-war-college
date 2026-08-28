#!/usr/bin/env python3
"""Fail-closed designated-host wrapper for Conditional Engagement Candidate V2.1."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import types
from pathlib import Path
from typing import Any, Mapping, Sequence

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools import conditional_engagement_v2_duel_wrapper as parent

V21_SOURCE_COMMIT = "bf4f5640e7a99cbac5cbda6e5ce33769237de069"
V21_CANDIDATE_SHA256 = "a0b08f7a7ea807de53416f589790059e2540404f680d6b470395bdbdc067f460"
V21_FIXTURE = Path("fixtures/training/conditional_engagement_candidate_v2_1.json")
OVERLAY_PACKAGE = "void_wc_conditional_v2_1_overlay"
RUN_SCHEMA = "void.apollyon.conditional-engagement-run-binding.v2.1"
TRAJECTORY_KEY = "conditional_engagement_v2_1"


class WrapperError(parent.WrapperError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise WrapperError(message)


def validate_v21_source(source_dir: Path) -> dict[str, str]:
    source_dir = source_dir.expanduser().resolve()
    _require(source_dir.is_dir(), f"V2.1 source dir missing: {source_dir}")
    head = parent._git(source_dir, "rev-parse", "HEAD")
    _require(
        head == V21_SOURCE_COMMIT,
        f"V2.1 source head drift: expected={V21_SOURCE_COMMIT} actual={head}",
    )
    dirty = parent._git(source_dir, "status", "--porcelain", "--untracked-files=no")
    _require(not dirty, "V2.1 source tracked worktree must be clean")

    fixture = source_dir / V21_FIXTURE
    policy = source_dir / "openra_env/coaching/conditional_engagement_v2_1.py"
    session = source_dir / "openra_env/coaching/conditional_engagement_session_v2_1.py"
    for label, path in (
        ("candidate fixture", fixture),
        ("policy module", policy),
        ("session module", session),
    ):
        _require(path.is_file(), f"missing V2.1 {label}: {path}")

    fixture_sha = parent.sha256(fixture)
    _require(
        fixture_sha == V21_CANDIDATE_SHA256,
        f"V2.1 candidate fixture hash drift: expected={V21_CANDIDATE_SHA256} actual={fixture_sha}",
    )
    return {
        "source_dir": str(source_dir),
        "source_commit": head,
        "candidate_sha256": fixture_sha,
        "policy_sha256": parent.sha256(policy),
        "session_sha256": parent.sha256(session),
    }


def load_v21_overlay(source_dir: Path):
    source_dir = source_dir.expanduser().resolve()
    coaching_dir = source_dir / "openra_env" / "coaching"
    package_name = OVERLAY_PACKAGE
    _require(package_name not in sys.modules, "V2.1 overlay package already loaded")

    package = types.ModuleType(package_name)
    package.__path__ = [str(coaching_dir)]  # type: ignore[attr-defined]
    package.__package__ = package_name
    sys.modules[package_name] = package
    loaded = [package_name]
    try:
        for basename in (
            "conditional_engagement_v2_1",
            "conditional_engagement_session_v2_1",
        ):
            name = f"{package_name}.{basename}"
            path = coaching_dir / f"{basename}.py"
            spec = importlib.util.spec_from_file_location(name, path)
            _require(spec is not None and spec.loader is not None, f"cannot load V2.1 module {path}")
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            loaded.append(name)
            spec.loader.exec_module(module)
        return (
            sys.modules[f"{package_name}.conditional_engagement_v2_1"],
            sys.modules[f"{package_name}.conditional_engagement_session_v2_1"],
        )
    except Exception:
        for name in reversed(loaded):
            sys.modules.pop(name, None)
        raise


def load_candidate(policy_module: Any, source_dir: Path) -> Mapping[str, Any]:
    fixture = source_dir.expanduser().resolve() / V21_FIXTURE
    candidate = json.loads(fixture.read_text(encoding="utf-8"))
    policy_module.validate_candidate(candidate)
    actual = policy_module.candidate_sha256(candidate)
    _require(actual == V21_CANDIDATE_SHA256, f"V2.1 candidate semantic digest drift: {actual}")
    return candidate


class ConditionalV21Hooks:
    """Decorate Apollyon's typed-tool decision path without owning world mutation."""

    def __init__(self, legacy: Any, session: Any, provenance: Mapping[str, str], wrapper_sha256: str):
        self.legacy = legacy
        self.session = session
        self.provenance = dict(provenance)
        self.wrapper_sha256 = wrapper_sha256
        self._original_decision = legacy.apollyon_decision_typed
        self._original_append = legacy.append_jsonl
        self._round_evidence: dict[int, dict[str, Any]] = {}
        self._installed = False

    def install(self) -> None:
        _require(not self._installed, "V2.1 hooks already installed")
        self.legacy.apollyon_decision_typed = self._wrapped_decision
        self.legacy.append_jsonl = self._wrapped_append_jsonl
        self._installed = True

    def restore(self) -> None:
        if self._installed:
            self.legacy.apollyon_decision_typed = self._original_decision
            self.legacy.append_jsonl = self._original_append
            self._installed = False

    def _wrapped_decision(self, base, helper, state, pending, pb2, doctrine, round_no):
        _, pre_contract = self.legacy.apollyon_tools_typed(base, state, pending)
        offered_names = list(pre_contract["offered_tool_names"])
        prepared = self.session.prepare_round(
            state,
            round_no=round_no,
            allowed_tool_names=offered_names,
        )

        original_tool_call = helper.ollama_tool_call

        def coached_tool_call(system, user, tools):
            return original_tool_call(system, user + "\n" + prepared["coaching"], tools)

        helper.ollama_tool_call = coached_tool_call
        try:
            result = self._original_decision(
                base, helper, state, pending, pb2, doctrine, round_no
            )
        finally:
            helper.ollama_tool_call = original_tool_call

        name, args, commands, attempts, contract = result
        actual_names = list(contract["offered_tool_names"])
        _require(
            actual_names == offered_names,
            "offered tool surface changed between V2.1 preparation and host acceptance",
        )
        receipt = self.session.commit_accepted_tool(name)
        self._round_evidence[int(round_no)] = {
            "prepared": prepared,
            "accepted": receipt,
        }
        return name, args, commands, attempts, contract

    def _wrapped_append_jsonl(self, path: Path, row: dict[str, Any]):
        output = dict(row)
        event = row.get("event")
        if event == "run_header":
            output[TRAJECTORY_KEY] = {
                "schema": RUN_SCHEMA,
                "candidate_only": True,
                "source_commit": self.provenance["source_commit"],
                "candidate_sha256": self.provenance["candidate_sha256"],
                "policy_sha256": self.provenance["policy_sha256"],
                "session_sha256": self.provenance["session_sha256"],
                "wrapper_sha256": self.wrapper_sha256,
                "parent_v2_candidate_sha256": "27f28a6a46f63a055f8f35c021bafae1035084c444ba7e2009161109ec3efdd6",
                "automatic_apollyon_weight_mutation": False,
                "automatic_abaddon_policy_promotion": False,
                "automatic_corpus_admission": False,
            }
        elif event == "joint_decision":
            round_no = int(row.get("round", 0))
            evidence = self._round_evidence.pop(round_no, None)
            _require(
                evidence is not None,
                f"missing V2.1 evidence for joint_decision round {round_no}",
            )
            output[TRAJECTORY_KEY] = evidence
        self._original_append(path, output)


def parse_wrapper_args(argv: Sequence[str]) -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--v2-1-source-dir", required=True)
    namespace, remaining = parser.parse_known_args(list(argv))
    return namespace, remaining


def main(argv: Sequence[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    wrapper_args, legacy_args = parse_wrapper_args(argv)
    source_dir = Path(wrapper_args.v2_1_source_dir)

    provenance = validate_v21_source(source_dir)
    policy_module, session_module = load_v21_overlay(source_dir)
    candidate = load_candidate(policy_module, source_dir)
    coaching_session = session_module.ConditionalEngagementSessionV21(candidate)
    legacy = parent.load_legacy_runner()

    frozen_rl = Path(getattr(legacy, "RL")).expanduser().resolve()
    _require(
        source_dir.expanduser().resolve() != frozen_rl,
        "V2.1 source must be a separate worktree; refusing frozen legacy worktree",
    )

    wrapper_sha = parent.sha256(SCRIPT_PATH)
    hooks = ConditionalV21Hooks(legacy, coaching_session, provenance, wrapper_sha)

    print("=== VOID CONDITIONAL ENGAGEMENT V2.1 DUEL WRAPPER ===")
    print(f"legacy_runner_sha256={parent.LEGACY_RUNNER_SHA256}")
    print(f"v2_1_source_commit={provenance['source_commit']}")
    print(f"v2_1_candidate_sha256={provenance['candidate_sha256']}")
    print(f"v2_1_policy_sha256={provenance['policy_sha256']}")
    print(f"v2_1_session_sha256={provenance['session_sha256']}")
    print(f"v2_1_wrapper_sha256={wrapper_sha}")
    print("frozen_legacy_worktree_mutation=false")
    print("candidate_only=true")
    print("automatic_apollyon_weight_mutation=false")
    print("automatic_abaddon_policy_promotion=false")
    print("automatic_corpus_admission=false")
    print("fail_closed=true")

    old_argv = sys.argv
    hooks.install()
    try:
        sys.argv = [str(parent.LEGACY_RUNNER), *legacy_args]
        legacy.main()
    finally:
        hooks.restore()
        sys.argv = old_argv
    return 0


def cli(argv: Sequence[str] | None = None) -> int:
    try:
        return main(argv)
    except parent.WrapperError as error:
        print("VOID_CONDITIONAL_ENGAGEMENT_V2_1_WRAPPER_HOLD", file=sys.stderr)
        print(f"blocker={error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(cli())
