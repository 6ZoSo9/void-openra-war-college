#!/usr/bin/env python3
"""Apply one reviewed General Brain challenger adapter outside V2.2 host authority."""
from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from openra_env.learning.general_brain_runtime import (
    BRAIN_RUN_SCHEMA,
    load_challenger_binding,
    tactical_overlay,
)
from tools import conditional_engagement_v2_2_duel_wrapper as v22

BRAIN_TRAJECTORY_KEY = "general_brain_generation_1"


class ChallengerWrapperError(v22.WrapperError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ChallengerWrapperError(message)


class GeneralBrainOverlayHooks:
    """Sit beneath the reviewed V2.2 hook without changing its tool surface."""

    def __init__(self, legacy: Any, session: Any, binding: Mapping[str, Any]):
        self.legacy = legacy
        self.session = session
        self.binding = dict(binding)
        self._original_decision = legacy.apollyon_decision_typed
        self._original_append = legacy.append_jsonl
        self._round_evidence: dict[int, dict[str, Any]] = {}
        self._installed = False

    def install(self) -> None:
        _require(not self._installed, "General Brain overlay already installed")
        self.legacy.apollyon_decision_typed = self._wrapped_decision
        self.legacy.append_jsonl = self._wrapped_append_jsonl
        self._installed = True

    def restore(self) -> None:
        if self._installed:
            self.legacy.apollyon_decision_typed = self._original_decision
            self.legacy.append_jsonl = self._original_append
            self._installed = False

    def _wrapped_decision(self, base, helper, state, pending, pb2, doctrine, round_no):
        _, contract = self.legacy.apollyon_tools_typed(base, state, pending)
        offered_names = list(contract["offered_tool_names"])
        prepared = self.session.prepare_round(
            state,
            round_no=round_no,
            allowed_tool_names=offered_names,
        )
        mode = prepared["decision"]["mode"]
        overlay = tactical_overlay(
            self.binding,
            mode=mode,
            offered_tool_names=offered_names,
        )

        original_tool_call = helper.ollama_tool_call
        if overlay["prompt_injected"]:
            _require(bool(overlay["coaching"]), "applied General Brain preference has empty coaching")

            def brain_tool_call(system, user, tools):
                return original_tool_call(system, user + "\n" + overlay["coaching"], tools)

            helper.ollama_tool_call = brain_tool_call
            try:
                result = self._original_decision(
                    base, helper, state, pending, pb2, doctrine, round_no
                )
            finally:
                helper.ollama_tool_call = original_tool_call
        else:
            _require(
                overlay["preference_applied"] is False and overlay["coaching"] == "",
                "silent General Brain round unexpectedly carries prompt coaching",
            )
            # Do not wrap helper.ollama_tool_call at all. This keeps the model
            # prompt behaviorally untouched when this generation has learned no
            # applicable positive preference for the current tactical mode.
            result = self._original_decision(
                base, helper, state, pending, pb2, doctrine, round_no
            )

        name, args, commands, attempts, accepted_contract = result
        actual_names = list(accepted_contract["offered_tool_names"])
        _require(
            actual_names == offered_names,
            "General Brain observation changed the host tool surface",
        )
        accepted = self.session.commit_accepted_tool(name)
        _require(
            accepted["mode"] == mode,
            "General Brain parallel V2.2 session mode drift",
        )
        self._round_evidence[int(round_no)] = {
            **{key: value for key, value in overlay.items() if key != "coaching"},
            "selected_tool": name,
            "selected_preferred_tool": (
                overlay["preferred_tool"] is not None
                and name == overlay["preferred_tool"]
            ),
            "selected_arguments": dict(args) if isinstance(args, Mapping) else {},
            "v2_2_parallel_session_committed": True,
        }
        return name, args, commands, attempts, accepted_contract

    def _wrapped_append_jsonl(self, path: Path, row: dict[str, Any]):
        output = dict(row)
        event = row.get("event")
        if event == "run_header":
            output[BRAIN_TRAJECTORY_KEY] = {
                "schema": BRAIN_RUN_SCHEMA,
                "general_id": "apollyon",
                "generation": 1,
                "challenger_only": True,
                "adapter_sha256": self.binding["adapter_sha256"],
                "adapter_file_sha256": self.binding["adapter_file_sha256"],
                "challenger_manifest_sha256": self.binding["challenger_manifest_sha256"],
                "challenger_manifest_file_sha256": self.binding[
                    "challenger_manifest_file_sha256"
                ],
                "authority_envelope_trainable": False,
                "sovereign_directives_trainable": False,
                "tool_authorization_trainable": False,
                "automatic_weight_install": False,
                "automatic_promotion": False,
                "review_required": True,
            }
        elif event == "joint_decision":
            round_no = int(row.get("round", 0))
            evidence = self._round_evidence.pop(round_no, None)
            _require(
                evidence is not None,
                f"missing General Brain evidence for round {round_no}",
            )
            output[BRAIN_TRAJECTORY_KEY] = evidence
        self._original_append(path, output)


def parse_args(argv: Sequence[str]) -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--v2-2-source-dir", required=True)
    parser.add_argument("--general-brain-adapter", required=True)
    parser.add_argument("--general-brain-adapter-sha256", required=True)
    parser.add_argument("--general-brain-challenger-manifest", required=True)
    parser.add_argument("--general-brain-challenger-manifest-sha256", required=True)
    namespace, remaining = parser.parse_known_args(list(argv))
    return namespace, remaining


def main(argv: Sequence[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    args, legacy_args = parse_args(argv)
    source_dir = Path(args.v2_2_source_dir)

    provenance = v22.validate_v22_source(source_dir)
    policy_module, session_module = v22.load_v22_overlay(source_dir)
    candidate = v22.load_candidate(policy_module, source_dir)
    reviewed_session = session_module.ConditionalEngagementSessionV22(candidate)
    brain_parallel_session = session_module.ConditionalEngagementSessionV22(candidate)
    legacy = v22.parent.load_legacy_runner()

    binding = load_challenger_binding(
        adapter_path=Path(args.general_brain_adapter),
        challenger_manifest_path=Path(args.general_brain_challenger_manifest),
        expected_adapter_sha256=args.general_brain_adapter_sha256,
        expected_challenger_file_sha256=args.general_brain_challenger_manifest_sha256,
    )

    frozen_rl = Path(getattr(legacy, "RL")).expanduser().resolve()
    _require(
        source_dir.expanduser().resolve() != frozen_rl,
        "V2.2 source must remain a separate reviewed worktree",
    )

    brain_hooks = GeneralBrainOverlayHooks(legacy, brain_parallel_session, binding)
    brain_hooks.install()
    reviewed_wrapper_sha = v22.parent.sha256(v22.SCRIPT_PATH)
    v22_hooks = v22.ConditionalV22Hooks(
        legacy,
        reviewed_session,
        provenance,
        reviewed_wrapper_sha,
    )
    v22_hooks.install()

    print("=== VOID CONDITIONAL ENGAGEMENT V2.2 + GENERAL BRAIN G1 CHALLENGER ===")
    print(f"v2_2_source_commit={provenance['source_commit']}")
    print(f"v2_2_candidate_sha256={provenance['candidate_sha256']}")
    print(f"v2_2_reviewed_wrapper_sha256={reviewed_wrapper_sha}")
    print(f"general_brain_adapter_sha256={binding['adapter_sha256']}")
    print(
        "general_brain_challenger_manifest_sha256="
        + binding["challenger_manifest_sha256"]
    )
    print("general_brain_generation=1")
    print("challenger_only=true")
    print("tool_surface_filtering=false")
    print("unlearned_mode_prompt_injection=false")
    print("authority_envelope_trainable=false")
    print("sovereign_directives_trainable=false")
    print("tool_authorization_trainable=false")
    print("automatic_weight_install=false")
    print("automatic_promotion=false")
    print("fail_closed=true")

    old_argv = sys.argv
    try:
        sys.argv = [str(v22.parent.LEGACY_RUNNER), *legacy_args]
        legacy.main()
    finally:
        try:
            v22_hooks.restore()
        finally:
            brain_hooks.restore()
            sys.argv = old_argv
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
