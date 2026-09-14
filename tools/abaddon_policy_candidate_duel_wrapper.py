#!/usr/bin/env python3
"""Fail-closed Abaddon policy-candidate wrapper for the frozen warm-start duel.

This wrapper does not train or promote anything. It keeps Apollyon's reviewed
boundary unchanged, verifies the exact deterministic Abaddon controller and
refiner, injects one reviewed candidate policy genome into Abaddon's controller
constructor, and leaves the legacy host decision_to_commands validation path
untouched.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
import types
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

MARK = "VOID_WAR_COLLEGE_ABADDON_POLICY_CANDIDATE_WRAPPER_V1"

HOME = Path.home()
LEGACY_RUNNER = (
    HOME / "Downloads" /
    "void-actual-apollyon-vs-abaddon-warm-start-combat-spar-v1_4.py"
)
LEGACY_RUNNER_SHA256 = (
    "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
)
DOJO = HOME / "dev" / "void-apollyon-dojo"
ABADDON_CONTROLLER = DOJO / "dojo" / "abaddon_controller.py"
ABADDON_CONTROLLER_SHA256 = (
    "b235d4cff3e3953ed7c511de52c76ada7e1a47046295e104353b61ef09e11103"
)
ABADDON_REFINER = DOJO / "dojo" / "abaddon_refiner.py"
ABADDON_REFINER_SHA256 = (
    "5c5c4e7260cebcc5afbe9e9bd4744846593b44658ed0088f2eddbcaffc43910b"
)

EVIDENCE_KEY = "abaddon_policy_candidate_v1"
RUN_SCHEMA = "void.abaddon.policy-candidate-run-binding.v1"
ROUND_SCHEMA = "void.abaddon.policy-candidate-round-binding.v1"


class WrapperError(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise WrapperError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def wrapper_source_sha256() -> str:
    return sha256_file(Path(__file__).resolve())


def _load_exact_module(path: Path, expected_sha256: str, module_name: str):
    path = path.expanduser().resolve()
    _require(path.is_file() and not path.is_symlink(), f"exact source missing: {path}")
    actual = sha256_file(path)
    _require(
        actual == expected_sha256,
        f"exact source hash drift: path={path} expected={expected_sha256} actual={actual}",
    )
    spec = importlib.util.spec_from_file_location(module_name, path)
    _require(spec is not None and spec.loader is not None, f"cannot import exact source: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_exact_legacy_runner():
    return _load_exact_module(
        LEGACY_RUNNER,
        LEGACY_RUNNER_SHA256,
        "void_wc_abaddon_candidate_legacy_v14",
    )


def load_exact_refiner():
    return _load_exact_module(
        ABADDON_REFINER,
        ABADDON_REFINER_SHA256,
        "void_wc_abaddon_candidate_refiner_v1",
    )


def _semantic_genome_sha256(refiner: Any, genome: Mapping[str, Any]) -> str:
    body = copy.deepcopy(dict(genome))
    claimed = body.pop("genome_sha256", None)
    _require(isinstance(claimed, str), "candidate genome_sha256 missing")
    actual = refiner.digest(body)
    _require(
        actual == claimed,
        f"candidate semantic digest mismatch: claimed={claimed} actual={actual}",
    )
    return actual


def load_candidate_genome(
    path: Path,
    *,
    expected_file_sha256: str,
    refiner: Any,
) -> tuple[dict[str, Any], dict[str, str]]:
    path = path.expanduser().resolve()
    _require(path.is_file() and not path.is_symlink(), f"candidate genome missing: {path}")
    raw = path.read_bytes()
    actual_file_sha = sha256_bytes(raw)
    _require(
        actual_file_sha == expected_file_sha256,
        "candidate genome file SHA-256 mismatch: "
        f"expected={expected_file_sha256} actual={actual_file_sha}",
    )
    try:
        candidate = json.loads(raw)
    except json.JSONDecodeError as error:
        raise WrapperError(f"candidate genome JSON invalid: {error}") from error
    _require(isinstance(candidate, dict), "candidate genome must be an object")
    refiner.validate_genome(candidate)
    _require(candidate.get("identity") == "Abaddon", "candidate identity is not Abaddon")
    _require(candidate.get("schema") == refiner.SCHEMA, "candidate genome schema drift")
    semantic_sha = _semantic_genome_sha256(refiner, candidate)
    return candidate, {
        "candidate_file_sha256": actual_file_sha,
        "candidate_genome_sha256": semantic_sha,
    }


def _candidate_controller_module(
    original_module: Any,
    refiner: Any,
    candidate: Mapping[str, Any],
    binding: Mapping[str, str],
):
    original_class = getattr(original_module, "AbaddonController", None)
    _require(callable(original_class), "exact Abaddon controller class missing")

    class CandidateAbaddonController(original_class):
        def __init__(self, doctrine: str, seed: int = 2050, *args: Any, **kwargs: Any):
            _require("policy" not in kwargs, "legacy caller attempted to override candidate policy")
            policy = refiner.policy_for(dict(candidate), doctrine)
            super().__init__(
                doctrine,
                seed,
                *args,
                policy=policy,
                **kwargs,
            )
            self._void_candidate_binding = {
                **dict(binding),
                "doctrine": str(doctrine).upper(),
                "policy": dict(policy),
            }

    proxy = types.ModuleType("void_wc_candidate_abaddon_controller_proxy")
    proxy.__dict__.update(vars(original_module))
    proxy.AbaddonController = CandidateAbaddonController
    proxy.__void_candidate_binding__ = dict(binding)
    return proxy


class AbaddonCandidateHooks:
    """Inject candidate policy at the controller constructor boundary only."""

    def __init__(
        self,
        legacy: Any,
        refiner: Any,
        candidate: Mapping[str, Any],
        binding: Mapping[str, str],
    ) -> None:
        self.legacy = legacy
        self.refiner = refiner
        self.candidate = dict(candidate)
        self.binding = dict(binding)
        self._original_load_base = legacy.load_base
        self._original_append_jsonl = legacy.append_jsonl
        self._installed = False

    def install(self) -> None:
        _require(not self._installed, "Abaddon candidate hooks already installed")
        self.legacy.load_base = self._wrapped_load_base
        self.legacy.append_jsonl = self._wrapped_append_jsonl
        self._installed = True

    def restore(self) -> None:
        if self._installed:
            self.legacy.load_base = self._original_load_base
            self.legacy.append_jsonl = self._original_append_jsonl
            self._installed = False

    def _wrapped_load_base(self):
        base = self._original_load_base()

        controller_path = Path(getattr(base, "ABADDON_CONTROLLER", "")).expanduser().resolve()
        controller_sha = getattr(base, "ABADDON_CONTROLLER_SHA", None)
        _require(
            controller_path == ABADDON_CONTROLLER.resolve(),
            f"legacy Abaddon controller path drift: {controller_path}",
        )
        _require(
            controller_sha == ABADDON_CONTROLLER_SHA256,
            f"legacy Abaddon controller SHA binding drift: {controller_sha}",
        )

        original_load_module = base.load_module

        def load_module(path: Path, name: str):
            resolved = Path(path).expanduser().resolve()
            module = original_load_module(path, name)
            if resolved != controller_path:
                return module
            actual = sha256_file(resolved)
            _require(
                actual == ABADDON_CONTROLLER_SHA256,
                "Abaddon controller bytes changed before candidate injection",
            )
            return _candidate_controller_module(
                module,
                self.refiner,
                self.candidate,
                self.binding,
            )

        base.load_module = load_module
        return base

    def _wrapped_append_jsonl(self, path: Path, row: dict[str, Any]):
        output = dict(row)
        event = row.get("event")
        if event == "run_header":
            _require(
                row.get("abaddon_controller_sha256") == ABADDON_CONTROLLER_SHA256,
                "run header controller binding drift",
            )
            _require(row.get("candidate_only") is True, "run header lost candidate-only boundary")
            output[EVIDENCE_KEY] = {
                "schema": RUN_SCHEMA,
                **self.binding,
                "candidate_only": True,
                "review_required": True,
                "training_use_approved": False,
                "candidate_general": "abaddon",
                "opponent_general": "apollyon",
                "apollyon_policy_mutated": False,
                "host_validation_path": "legacy_base.decision_to_commands",
                "host_validation_unchanged": True,
                "world_mutated_before_host_validation": False,
                "training_performed": False,
                "weights_updated": False,
                "automatic_corpus_admission": False,
                "automatic_abaddon_policy_promotion": False,
            }
        elif event == "joint_decision":
            abaddon = row.get("abaddon")
            _require(isinstance(abaddon, Mapping), "joint decision missing Abaddon result")
            accepted = abaddon.get("accepted")
            _require(isinstance(accepted, bool), "joint decision Abaddon host acceptance missing")
            output[EVIDENCE_KEY] = {
                "schema": ROUND_SCHEMA,
                **self.binding,
                "round": row.get("round"),
                "legacy_host_accepted": accepted,
                "legacy_host_reason": str(abaddon.get("host_reason", "")),
                "host_validation_unchanged": True,
                "world_mutated_before_host_validation": False,
            }
        self._original_append_jsonl(path, output)


def parse_wrapper_args(argv: Sequence[str]) -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--abaddon-candidate-genome", required=True)
    parser.add_argument("--expected-candidate-file-sha256", required=True)
    namespace, remaining = parser.parse_known_args(list(argv))
    return namespace, remaining


def main(argv: Sequence[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    wrapper_args, legacy_args = parse_wrapper_args(argv)

    _require(len(wrapper_args.expected_candidate_file_sha256) == 64, "candidate file SHA-256 malformed")
    _require(
        all(c in "0123456789abcdef" for c in wrapper_args.expected_candidate_file_sha256),
        "candidate file SHA-256 must be lowercase hex",
    )

    legacy = load_exact_legacy_runner()
    refiner = load_exact_refiner()
    candidate, candidate_binding = load_candidate_genome(
        Path(wrapper_args.abaddon_candidate_genome),
        expected_file_sha256=wrapper_args.expected_candidate_file_sha256,
        refiner=refiner,
    )

    binding = {
        **candidate_binding,
        "wrapper_sha256": wrapper_source_sha256(),
        "legacy_runner_sha256": LEGACY_RUNNER_SHA256,
        "abaddon_controller_sha256": ABADDON_CONTROLLER_SHA256,
        "abaddon_refiner_sha256": ABADDON_REFINER_SHA256,
    }

    hooks = AbaddonCandidateHooks(legacy, refiner, candidate, binding)

    print(MARK)
    print(f"wrapper_sha256={binding['wrapper_sha256']}")
    print(f"legacy_runner_sha256={LEGACY_RUNNER_SHA256}")
    print(f"abaddon_controller_sha256={ABADDON_CONTROLLER_SHA256}")
    print(f"abaddon_refiner_sha256={ABADDON_REFINER_SHA256}")
    print(f"candidate_file_sha256={binding['candidate_file_sha256']}")
    print(f"candidate_genome_sha256={binding['candidate_genome_sha256']}")
    print("candidate_general=abaddon")
    print("apollyon_fixed=true")
    print("host_validation_unchanged=true")
    print("training_performed=false")
    print("weights_updated=false")
    print("automatic_corpus_admission=false")
    print("automatic_abaddon_policy_promotion=false")
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
        print("VOID_WAR_COLLEGE_ABADDON_POLICY_CANDIDATE_WRAPPER_V1_HOLD", file=sys.stderr)
        print(f"blocker={error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(cli())
