#!/usr/bin/env python3
"""Fail-closed designated-host wrapper for Conditional Engagement Candidate V2.

The proven warm-start duel runner and its frozen War College worktree remain
untouched. This wrapper loads the reviewed V2 policy/session source from a
separate exact-commit worktree, decorates Apollyon's existing typed-tool prompt,
and binds the coaching decision plus accepted-tool receipt into the legacy
trajectory before its SHA-256 is finalized.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
import types
from pathlib import Path
from typing import Any, Mapping, Sequence

LEGACY_RUNNER = Path.home() / "Downloads" / "void-actual-apollyon-vs-abaddon-warm-start-combat-spar-v1_4.py"
LEGACY_RUNNER_SHA256 = "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
V2_SOURCE_COMMIT = "69ad16ed4db3e59a457d0125138de43f78a8fe39"
V2_CANDIDATE_SHA256 = "27f28a6a46f63a055f8f35c021bafae1035084c444ba7e2009161109ec3efdd6"
V2_FIXTURE = Path("fixtures/training/conditional_engagement_candidate_v2.json")
OVERLAY_PACKAGE = "void_wc_conditional_v2_overlay"


class WrapperError(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise WrapperError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(source_dir: Path, *args: str) -> str:
    cp = subprocess.run(
        ["git", "-C", str(source_dir), *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if cp.returncode != 0:
        raise WrapperError(
            f"git {' '.join(args)} failed in {source_dir}: {(cp.stderr or '').strip()}"
        )
    return (cp.stdout or "").strip()


def validate_v2_source(source_dir: Path) -> dict[str, str]:
    source_dir = source_dir.expanduser().resolve()
    _require(source_dir.is_dir(), f"V2 source dir missing: {source_dir}")
    head = _git(source_dir, "rev-parse", "HEAD")
    _require(head == V2_SOURCE_COMMIT, f"V2 source head drift: expected={V2_SOURCE_COMMIT} actual={head}")
    dirty = _git(source_dir, "status", "--porcelain", "--untracked-files=no")
    _require(not dirty, "V2 source tracked worktree must be clean")

    fixture = source_dir / V2_FIXTURE
    policy = source_dir / "openra_env/coaching/conditional_engagement_v2.py"
    session = source_dir / "openra_env/coaching/conditional_engagement_session_v2.py"
    for label, path in (("candidate fixture", fixture), ("policy module", policy), ("session module", session)):
        _require(path.is_file(), f"missing V2 {label}: {path}")

    fixture_sha = sha256(fixture)
    _require(
        fixture_sha == V2_CANDIDATE_SHA256,
        f"V2 candidate fixture hash drift: expected={V2_CANDIDATE_SHA256} actual={fixture_sha}",
    )
    return {
        "source_dir": str(source_dir),
        "source_commit": head,
        "candidate_sha256": fixture_sha,
        "policy_sha256": sha256(policy),
        "session_sha256": sha256(session),
    }


def load_v2_overlay(source_dir: Path):
    """Load only the two coaching modules into an isolated synthetic package."""
    source_dir = source_dir.expanduser().resolve()
    coaching_dir = source_dir / "openra_env" / "coaching"
    package_name = OVERLAY_PACKAGE
    _require(package_name not in sys.modules, "V2 overlay package already loaded")

    package = types.ModuleType(package_name)
    package.__path__ = [str(coaching_dir)]  # type: ignore[attr-defined]
    package.__package__ = package_name
    sys.modules[package_name] = package

    loaded: list[str] = [package_name]
    try:
        for basename in ("conditional_engagement_v2", "conditional_engagement_session_v2"):
            name = f"{package_name}.{basename}"
            path = coaching_dir / f"{basename}.py"
            spec = importlib.util.spec_from_file_location(name, path)
            _require(spec is not None and spec.loader is not None, f"cannot load V2 module {path}")
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            loaded.append(name)
            spec.loader.exec_module(module)
        policy = sys.modules[f"{package_name}.conditional_engagement_v2"]
        session = sys.modules[f"{package_name}.conditional_engagement_session_v2"]
        return policy, session
    except Exception:
        for name in reversed(loaded):
            sys.modules.pop(name, None)
        raise


def load_legacy_runner(path: Path = LEGACY_RUNNER):
    path = path.expanduser().resolve()
    _require(path.is_file(), f"legacy runner missing: {path}")
    actual = sha256(path)
    _require(
        actual == LEGACY_RUNNER_SHA256,
        f"legacy runner hash drift: expected={LEGACY_RUNNER_SHA256} actual={actual}",
    )
    name = "void_actual_apollyon_abaddon_warmstart_v14_conditional_v2_host"
    spec = importlib.util.spec_from_file_location(name, path)
    _require(spec is not None and spec.loader is not None, "cannot import legacy runner")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _same_names(left: Sequence[str], right: Sequence[str]) -> bool:
    return list(left) == list(right)


class ConditionalV2Hooks:
    """Patch a reviewed legacy runner without changing its world-transition code."""

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
        _require(not self._installed, "V2 hooks already installed")
        self.legacy.apollyon_decision_typed = self._wrapped_decision
        self.legacy.append_jsonl = self._wrapped_append_jsonl
        self._installed = True

    def restore(self) -> None:
        if self._installed:
            self.legacy.apollyon_decision_typed = self._original_decision
            self.legacy.append_jsonl = self._original_append
            self._installed = False

    def _wrapped_decision(self, base, helper, state, pending, pb2, doctrine, round_no):
        # Derive the exact current tool vocabulary before the model is called.
        _, pre_contract = self.legacy.apollyon_tools_typed(base, state, pending)
        offered_names = list(pre_contract["offered_tool_names"])
        prepared = self.session.prepare_round(
            state,
            round_no=round_no,
            allowed_tool_names=offered_names,
        )

        original_tool_call = helper.ollama_tool_call

        def coached_tool_call(system, user, tools):
            # The legacy runner already appends retry feedback after invalid
            # attempts. V2 coaching is therefore appended to every attempt while
            # the world remains unchanged.
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
            _same_names(actual_names, offered_names),
            "offered tool surface changed between V2 preparation and host acceptance",
        )
        receipt = self.session.commit_accepted_tool(name)
        self._round_evidence[int(round_no)] = {
            "prepared": prepared,
            "accepted": receipt,
        }
        return name, args, commands, attempts, contract

    def _wrapped_append_jsonl(self, path: Path, row: dict[str, Any]):
        event = row.get("event")
        output = dict(row)
        if event == "run_header":
            output["conditional_engagement_v2"] = {
                "schema": "void.apollyon.conditional-engagement-run-binding.v2",
                "candidate_only": True,
                "source_commit": self.provenance["source_commit"],
                "candidate_sha256": self.provenance["candidate_sha256"],
                "policy_sha256": self.provenance["policy_sha256"],
                "session_sha256": self.provenance["session_sha256"],
                "wrapper_sha256": self.wrapper_sha256,
                "automatic_apollyon_weight_mutation": False,
                "automatic_abaddon_policy_promotion": False,
                "automatic_corpus_admission": False,
            }
        elif event == "joint_decision":
            round_no = int(row.get("round", 0))
            evidence = self._round_evidence.pop(round_no, None)
            _require(evidence is not None, f"missing V2 evidence for joint_decision round {round_no}")
            output["conditional_engagement_v2"] = evidence
        self._original_append(path, output)


def load_candidate(policy_module: Any, source_dir: Path) -> Mapping[str, Any]:
    fixture = source_dir.expanduser().resolve() / V2_FIXTURE
    candidate = json.loads(fixture.read_text(encoding="utf-8"))
    policy_module.validate_candidate(candidate)
    actual = policy_module.candidate_sha256(candidate)
    _require(actual == V2_CANDIDATE_SHA256, f"V2 candidate semantic digest drift: {actual}")
    return candidate


def parse_wrapper_args(argv: Sequence[str]) -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--v2-source-dir", required=True)
    namespace, remaining = parser.parse_known_args(list(argv))
    return namespace, remaining


def main(argv: Sequence[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    wrapper_args, legacy_args = parse_wrapper_args(argv)
    source_dir = Path(wrapper_args.v2_source_dir)

    provenance = validate_v2_source(source_dir)
    policy_module, session_module = load_v2_overlay(source_dir)
    candidate = load_candidate(policy_module, source_dir)
    coaching_session = session_module.ConditionalEngagementSessionV2(candidate)
    legacy = load_legacy_runner()

    frozen_rl = Path(getattr(legacy, "RL")).expanduser().resolve()
    _require(
        source_dir.expanduser().resolve() != frozen_rl,
        "V2 source must be a separate worktree; refusing to use the frozen legacy War College worktree",
    )

    wrapper_sha = sha256(Path(__file__).resolve())
    hooks = ConditionalV2Hooks(legacy, coaching_session, provenance, wrapper_sha)

    print("=== VOID CONDITIONAL ENGAGEMENT V2 DUEL WRAPPER ===")
    print(f"legacy_runner_sha256={LEGACY_RUNNER_SHA256}")
    print(f"v2_source_commit={provenance['source_commit']}")
    print(f"v2_candidate_sha256={provenance['candidate_sha256']}")
    print(f"v2_policy_sha256={provenance['policy_sha256']}")
    print(f"v2_session_sha256={provenance['session_sha256']}")
    print(f"wrapper_sha256={wrapper_sha}")
    print("frozen_legacy_worktree_mutation=false")
    print("candidate_only=true")
    print("automatic_apollyon_weight_mutation=false")
    print("automatic_abaddon_policy_promotion=false")
    print("automatic_corpus_admission=false")
    print("fail_closed=true")

    old_argv = sys.argv
    hooks.install()
    try:
        sys.argv = [str(LEGACY_RUNNER), *legacy_args]
        legacy.main()
    finally:
        hooks.restore()
        sys.argv = old_argv
    return 0


def cli(argv: Sequence[str] | None = None) -> int:
    try:
        return main(argv)
    except WrapperError as error:
        print("VOID_CONDITIONAL_ENGAGEMENT_V2_WRAPPER_HOLD", file=sys.stderr)
        print(f"blocker={error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(cli())
