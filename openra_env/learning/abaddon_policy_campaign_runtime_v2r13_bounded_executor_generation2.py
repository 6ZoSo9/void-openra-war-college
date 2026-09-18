"""Bounded Generation-2 V2R13 runtime execution implementation.

This module composes already-reviewed source primitives into one executable
V2R13 arm path. It is deliberately limited to the six externally authorized
V2R13 arms (pair slots 3, 9, and 15; baseline/candidate).

The implementation does not run on import. Execution requires an explicit
per-call authority flag, a revocation callback, explicit host roots, and a
fresh-readiness provider. The fresh-readiness check is inserted immediately
after the exact legacy runner starts V2R13 and before the runner can perform
its first model decision. If readiness or the second revocation check fails,
the newly started runtime is cleaned up before the hold is raised.

No other runtime lane, training, weight update, automatic promotion,
deployment, VOID-chain mutation, or wallet/funds action is authorized here.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from copy import deepcopy
from functools import lru_cache
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Protocol

from openra_env.learning import (
    abaddon_policy_campaign_command_materializer_generation2 as command_materializer,
)
from openra_env.learning import (
    abaddon_policy_campaign_isolated_workdir_allocator_generation2 as allocator,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_activation_evidence_collector_binding_generation2
    as readiness_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_execution_authorization_acceptance_generation2
    as execution_authorization,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_frozen_worktree_materializer_generation2
    as worktree_materializer,
)
from openra_env.learning import apollyon_v2r13_portable_checkout as portable_checkout
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    V2R13,
)
from openra_env.learning.abaddon_policy_campaign_runtime_path_inputs_generation2 import (
    build_path_input_record,
)
from tools import abaddon_policy_candidate_duel_wrapper as candidate_wrapper

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-bounded-runtime-executor-contract.v1"
)
PLAN_SCHEMA = "void.abaddon.generation2.v2r13-bounded-runtime-execution-plan.v1"
RECEIPT_SCHEMA = "void.abaddon.generation2.v2r13-bounded-runtime-execution-receipt.v1"

AUTHORIZATION_SOURCE_GIT_BLOB = "2501d48ae889b9ed17cdf42acef033023f7d3886"
AUTHORIZATION_ATTESTATION_SHA256 = (
    "34ad7143e876b91056f730de37ab470b6fd8a5f99d84aadefb178cabf87a2031"
)
WORKTREE_MATERIALIZER_REVIEW_GIT_BLOB = "3dcc325c431ec451a737b6e228c365ce1acb4f98"
PORTABLE_CHECKOUT_GIT_BLOB = "077fbf5a2847d85113eb8fcba3904b02343ebfef"
COMMAND_MATERIALIZER_GIT_BLOB = "4836360e0d284454f815a2a2e32078d2565e6dea"
CANDIDATE_WRAPPER_GIT_BLOB = "61eaefee39ebd90df0ddd8c649d9f0f9b64b1776"
CANDIDATE_FIXTURE_GIT_BLOB = "20091bff54edbb567127722fae81e5a5308737d2"

LEGACY_RUNNER_SHA256 = command_materializer.LEGACY_RUNNER_SHA256
CANDIDATE_WRAPPER_SHA256 = command_materializer.CANDIDATE_WRAPPER_SOURCE_SHA256
CANDIDATE_FIXTURE_SHA256 = command_materializer.CANDIDATE_FIXTURE_SHA256
CANDIDATE_GENOME_SHA256 = command_materializer.CANDIDATE_GENOME_SHA256

AUTHORIZED_PAIR_SLOTS = (3, 9, 15)
HELD_OUT_PAIR_SLOTS = (15,)
AUTHORIZED_ARMS = ("baseline", "candidate")
AUTHORIZED_EXECUTION_ARM_COUNT = 6

NEXT_GATE = "V2R13_RUNTIME_EXECUTION_IMPLEMENTATION_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = (
    "source_only_v2r13_runtime_execution_implementation_source_binding_review"
)


class V2R13BoundedRuntimeExecutorHold(RuntimeError):
    pass


class AuthorityCheck(Protocol):
    def __call__(self, pair_slot: int, arm: str) -> bool:
        ...


class FreshReadinessProvider(Protocol):
    def __call__(self, context: Mapping[str, Any]) -> Mapping[str, Any]:
        ...


class GitRunner(Protocol):
    def __call__(self, repository_root: str, *args: str) -> Any:
        ...


class PathExists(Protocol):
    def __call__(self, path: str) -> bool:
        ...


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13BoundedRuntimeExecutorHold(message)


def _stable_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
        default=str,
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_stable_bytes(value)).hexdigest()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _absolute_normalized_path(value: str, label: str) -> Path:
    _require(type(value) is str and bool(value), f"{label} must be non-empty string")
    _require("\x00" not in value, f"{label} contains NUL")
    _require(not value.startswith("~"), f"{label} may not use tilde expansion")
    pure = PurePosixPath(value)
    _require(pure.is_absolute(), f"{label} must be absolute")
    _require(".." not in pure.parts, f"{label} may not contain parent traversal")
    _require(str(pure) == value, f"{label} must already be lexically normalized")
    _require(value != "/", f"{label} may not be filesystem root")
    return Path(value)


def _load_exact_module(path: Path, expected_sha256: str, module_name: str):
    resolved = path.expanduser().resolve()
    _require(resolved.is_file(), f"exact source missing: {resolved}")
    _require(not resolved.is_symlink(), f"exact source may not be symlink: {resolved}")
    actual = _sha256_file(resolved)
    _require(
        actual == expected_sha256,
        f"exact source hash drift: path={resolved} expected={expected_sha256} actual={actual}",
    )
    spec = importlib.util.spec_from_file_location(module_name, resolved)
    _require(
        spec is not None and spec.loader is not None,
        f"cannot import exact source: {resolved}",
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def _authorization_contract_cached() -> dict[str, Any]:
    contract = execution_authorization.v2r13_runtime_execution_authorization_contract()
    _require(
        contract.get("authorization_accepted") is True,
        "V2R13 authorization not accepted",
    )
    _require(
        contract.get("authorization_scope") == "v2r13_lane_only",
        "authorization scope drift",
    )
    _require(
        contract.get("authorized_runtime_selection_key") == V2R13,
        "runtime selection scope drift",
    )
    _require(
        tuple(contract.get("authorized_pair_slots", ())) == AUTHORIZED_PAIR_SLOTS,
        "pair-slot authority drift",
    )
    _require(
        tuple(contract.get("authorized_arms", ())) == AUTHORIZED_ARMS,
        "arm authority drift",
    )
    _require(
        contract.get("authorized_execution_arm_count") == AUTHORIZED_EXECUTION_ARM_COUNT,
        "authorized arm count drift",
    )
    _require(
        contract.get("runtime_execution_authorized") is True,
        "runtime execution not authorized",
    )
    _require(
        contract.get("other_runtime_lanes_authorized") is False,
        "other runtime lane authority present",
    )
    _require(
        contract.get("authorization_attestation_sha256")
        == AUTHORIZATION_ATTESTATION_SHA256,
        "authorization attestation drift",
    )
    _require(
        contract.get("fresh_runtime_readiness_required_before_each_execution") is True,
        "fresh readiness requirement lost",
    )
    _require(
        contract.get("revocation_check_required_before_each_execution") is True,
        "revocation requirement lost",
    )
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(contract.get(field) is False, f"forbidden authority drift: {field}")
    return contract


def _authorization_contract() -> dict[str, Any]:
    return deepcopy(_authorization_contract_cached())


def _authorized_allocation(pair_slot: int, arm: str) -> dict[str, Any]:
    _require(
        pair_slot in AUTHORIZED_PAIR_SLOTS,
        f"pair slot not authorized for V2R13: {pair_slot}",
    )
    _require(arm in AUTHORIZED_ARMS, f"arm not authorized: {arm}")
    contract = _authorization_contract()
    rows = contract.get("authorized_allocations")
    _require(isinstance(rows, list), "authorized allocation ledger missing")
    matches = [
        deepcopy(row)
        for row in rows
        if isinstance(row, Mapping)
        and row.get("pair_slot") == pair_slot
        and row.get("arm") == arm
    ]
    _require(len(matches) == 1, "authorized allocation identity not unique")
    row = matches[0]
    _require(
        row.get("runtime_selection_key") == V2R13,
        "authorized allocation is not V2R13",
    )
    _require(
        row.get("runtime_execution_authorized") is True,
        "allocation authority missing",
    )
    _require(
        tuple(row.get("remaining_blockers", ()))
        == ("V2R13_RUNTIME_EXECUTION_IMPLEMENTATION_REQUIRED",),
        "authorization blocker frontier drift",
    )
    _require(
        tuple(row.get("remaining_source_blockers", ())) == (),
        "source blocker reappeared",
    )
    return row


def execution_plan(*, pair_slot: int, arm: str) -> dict[str, Any]:
    authorized = _authorized_allocation(pair_slot, arm)
    command = command_materializer.materialize_command(pair_slot=pair_slot, arm=arm)
    allocation = allocator.allocate_isolated_workdir(pair_slot=pair_slot, arm=arm)
    _require(
        command.get("runtime_selection_key") == V2R13,
        "command runtime selection drift",
    )
    _require(
        allocation.get("runtime_selection_key") == V2R13,
        "allocation runtime selection drift",
    )
    _require(
        allocation.get("command_sha256") == command.get("command_sha256"),
        "command/allocation binding drift",
    )
    _require(
        allocation.get("allocation_sha256") == authorized.get("allocation_sha256"),
        "authorization/allocation binding drift",
    )
    body = {
        "schema": PLAN_SCHEMA,
        "pair_slot": pair_slot,
        "arm": arm,
        "execution_index": authorized["execution_index"],
        "held_out": pair_slot in HELD_OUT_PAIR_SLOTS,
        "runtime_selection_key": V2R13,
        "authorization_attestation_sha256": AUTHORIZATION_ATTESTATION_SHA256,
        "command_sha256": command["command_sha256"],
        "allocation_sha256": allocation["allocation_sha256"],
        "workdir_token": allocation["workdir_token"],
        "runner_argv": tuple(command["runner_argv"]),
        "runtime_execution_authorized": True,
        "fresh_runtime_readiness_required": True,
        "revocation_check_required": True,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
    }
    return {**body, "plan_sha256": _digest(body)}


def _arm_paths(
    isolated_workdir_root: str,
    plan: Mapping[str, Any],
) -> dict[str, Path]:
    root = _absolute_normalized_path(isolated_workdir_root, "isolated_workdir_root")
    token = str(plan["workdir_token"])
    expected = f"generation2/pair-{int(plan['pair_slot']):02d}/{plan['arm']}"
    _require(token == expected, "workdir token drift")
    arm_root = root.joinpath(*token.split("/"))
    return {
        "root": root,
        "arm_root": arm_root,
        "source": arm_root / "frozen-source",
        "engine": arm_root / "engine",
        "runs": arm_root / "runs",
    }


class _FreshReadinessHooks:
    def __init__(
        self,
        legacy: Any,
        portable: portable_checkout.PortableRunnerBinding,
        *,
        pair_slot: int,
        arm: str,
        materialization_receipt: Mapping[str, Any],
        readiness_provider: FreshReadinessProvider,
        authority_check: AuthorityCheck,
    ) -> None:
        self.legacy = legacy
        self.portable = portable
        self.pair_slot = pair_slot
        self.arm = arm
        self.materialization_receipt = deepcopy(dict(materialization_receipt))
        self.readiness_provider = readiness_provider
        self.authority_check = authority_check
        self._original_load_base = legacy.load_base
        self._base: Any | None = None
        self._original_base_load_module: Any | None = None
        self._helper: Any | None = None
        self._original_helper_start: Any | None = None
        self._original_helper_cleanup: Any | None = None
        self._installed = False
        self.readiness_evidence: dict[str, Any] | None = None
        self.readiness_admission: dict[str, Any] | None = None
        self.runtime_started = False
        self.runtime_cleanup_attempted = False
        self.runtime_cleanup_completed = False
        self.runtime_cleanup_after_hold = False

    def install(self) -> None:
        _require(not self._installed, "fresh-readiness hooks already installed")
        self.legacy.load_base = self._wrapped_load_base
        self._installed = True

    def restore(self) -> None:
        if self._helper is not None:
            if self._original_helper_start is not None:
                self._helper.start_ollama = self._original_helper_start
            if self._original_helper_cleanup is not None:
                self._helper.cleanup = self._original_helper_cleanup
        if self._base is not None and self._original_base_load_module is not None:
            self._base.load_module = self._original_base_load_module
        if self._installed:
            self.legacy.load_base = self._original_load_base
        self._helper = None
        self._original_helper_start = None
        self._original_helper_cleanup = None
        self._base = None
        self._original_base_load_module = None
        self._installed = False

    def _wrapped_load_base(self):
        base = self._original_load_base()
        self._base = base
        original_load_module = base.load_module
        self._original_base_load_module = original_load_module
        expected_runner = Path(base.APOLLYON_RUNNER).expanduser().resolve()

        def load_module(path: Path, name: str):
            module = original_load_module(path, name)
            if Path(path).expanduser().resolve() != expected_runner:
                return module
            original_start = module.start_ollama
            original_cleanup = module.cleanup
            _require(callable(original_start), "V2R13 runtime start hook missing")
            _require(callable(original_cleanup), "V2R13 runtime cleanup hook missing")
            self._helper = module
            self._original_helper_start = original_start
            self._original_helper_cleanup = original_cleanup

            def recorded_cleanup():
                self.runtime_cleanup_attempted = True
                original_cleanup()
                self.runtime_cleanup_completed = True

            def guarded_start():
                _require(
                    self.authority_check(self.pair_slot, self.arm) is True,
                    "V2R13 runtime execution authorization revoked before runtime start",
                )
                original_start()
                self.runtime_started = True
                try:
                    portable_attestation = self.portable.attestation()
                    context = {
                        "pair_slot": self.pair_slot,
                        "arm": self.arm,
                        "runtime_selection_key": V2R13,
                        "materialization_receipt": deepcopy(
                            self.materialization_receipt
                        ),
                        "portable_binding_attestation": deepcopy(
                            portable_attestation
                        ),
                    }
                    evidence = self.readiness_provider(context)
                    _require(
                        isinstance(evidence, Mapping),
                        "fresh V2R13 readiness provider returned non-object",
                    )
                    admission = readiness_binding.admit_bound_v2r13_evidence(evidence)
                    _require(
                        admission.get("runtime_readiness_admitted") is True,
                        "fresh V2R13 readiness not admitted",
                    )
                    _require(
                        admission.get("collector_identity_admitted") is True,
                        "fresh collector identity not admitted",
                    )
                    _require(
                        admission.get("runtime_execution_authorized") is False,
                        "readiness evidence unexpectedly carries authority",
                    )
                    _require(
                        self.authority_check(self.pair_slot, self.arm) is True,
                        "V2R13 runtime execution authorization revoked after readiness",
                    )
                    self.readiness_evidence = deepcopy(dict(evidence))
                    self.readiness_admission = deepcopy(admission)
                except Exception:
                    recorded_cleanup()
                    self.runtime_cleanup_after_hold = True
                    raise

            module.start_ollama = guarded_start
            module.cleanup = recorded_cleanup
            return module

        base.load_module = load_module
        return base


def _ensure_dojo_import_root() -> tuple[Path, bool]:
    dojo_root = candidate_wrapper.DOJO.expanduser().resolve()
    _require(dojo_root.is_dir(), f"candidate dojo root missing: {dojo_root}")
    value = str(dojo_root)
    inserted = value not in sys.path
    if inserted:
        sys.path.insert(0, value)
    return dojo_root, inserted


def _candidate_hooks(
    legacy: Any,
    *,
    candidate_genome_path: Path,
):
    _require(
        candidate_wrapper.wrapper_source_sha256() == CANDIDATE_WRAPPER_SHA256,
        "candidate wrapper source identity drift",
    )
    refiner = candidate_wrapper.load_exact_refiner()
    candidate, candidate_binding = candidate_wrapper.load_candidate_genome(
        candidate_genome_path,
        expected_file_sha256=CANDIDATE_FIXTURE_SHA256,
        refiner=refiner,
    )
    _require(
        candidate_binding.get("candidate_genome_sha256") == CANDIDATE_GENOME_SHA256,
        "candidate semantic genome identity drift",
    )
    binding = {
        **candidate_binding,
        "wrapper_sha256": CANDIDATE_WRAPPER_SHA256,
        "legacy_runner_sha256": LEGACY_RUNNER_SHA256,
        "abaddon_controller_sha256": candidate_wrapper.ABADDON_CONTROLLER_SHA256,
        "abaddon_refiner_sha256": candidate_wrapper.ABADDON_REFINER_SHA256,
    }
    hooks = candidate_wrapper.AbaddonCandidateHooks(
        legacy,
        refiner,
        candidate,
        binding,
    )
    return hooks, binding


def _restore_dojo_import_root(
    dojo_root: Path | None,
    inserted: bool,
) -> None:
    if dojo_root is not None and inserted:
        value = str(dojo_root)
        if value in sys.path:
            sys.path.remove(value)


def _run_artifact_receipt(runs_root: Path) -> dict[str, Any]:
    _require(runs_root.is_dir(), "isolated run root missing after execution")
    run_dirs = sorted(path for path in runs_root.iterdir() if path.is_dir())
    _require(
        len(run_dirs) == 1,
        f"expected exactly one run directory, found {len(run_dirs)}",
    )
    run_dir = run_dirs[0]
    warm = run_dir / "warm-start.jsonl"
    trajectory = run_dir / "trajectory.jsonl"
    summary = run_dir / "summary.json"
    for path, label in (
        (warm, "warm-start"),
        (trajectory, "trajectory"),
        (summary, "summary"),
    ):
        _require(
            path.is_file() and not path.is_symlink(),
            f"{label} artifact missing",
        )
    try:
        summary_obj = json.loads(summary.read_text(encoding="utf-8"))
    except Exception as error:
        raise V2R13BoundedRuntimeExecutorHold(
            f"summary JSON invalid: {error}"
        ) from error
    _require(isinstance(summary_obj, dict), "summary artifact must be object")
    return {
        "run_dir": str(run_dir),
        "run_id": run_dir.name,
        "warm_start_sha256": _sha256_file(warm),
        "trajectory_sha256": _sha256_file(trajectory),
        "summary_sha256": _sha256_file(summary),
        "summary": summary_obj,
    }


def execute_v2r13_arm(
    *,
    pair_slot: int,
    arm: str,
    isolated_workdir_root: str,
    source_repository_root: str,
    engine_repository_root: str,
    legacy_runner_path: str,
    candidate_genome_path: str | None,
    execution_authorized: bool,
    authority_check: AuthorityCheck,
    readiness_provider: FreshReadinessProvider,
    path_exists: PathExists,
    run_git: GitRunner,
) -> dict[str, Any]:
    """Execute one exact authorized V2R13 arm; no retry and no promotion."""
    _require(
        execution_authorized is True,
        "V2R13 runtime execution call not explicitly authorized",
    )
    _require(callable(authority_check), "authority_check must be callable")
    _require(callable(readiness_provider), "readiness_provider must be callable")
    _require(callable(path_exists), "path_exists backend must be callable")
    _require(callable(run_git), "run_git backend must be callable")

    plan = execution_plan(pair_slot=pair_slot, arm=arm)
    _require(
        authority_check(pair_slot, arm) is True,
        "V2R13 runtime execution authorization revoked",
    )

    source_repo = _absolute_normalized_path(
        source_repository_root,
        "source_repository_root",
    )
    engine_repo = _absolute_normalized_path(
        engine_repository_root,
        "engine_repository_root",
    )
    runner_path = _absolute_normalized_path(
        legacy_runner_path,
        "legacy_runner_path",
    )
    _require(source_repo.is_dir(), "source repository root missing")
    _require(engine_repo.is_dir(), "engine repository root missing")
    _require(
        runner_path.is_file() and not runner_path.is_symlink(),
        "legacy runner path invalid",
    )
    _require(
        _sha256_file(runner_path) == LEGACY_RUNNER_SHA256,
        "legacy runner SHA-256 drift",
    )

    paths = _arm_paths(isolated_workdir_root, plan)
    root = paths["root"]
    _require(
        root.is_dir() and not root.is_symlink(),
        "isolated workdir root must pre-exist as real directory",
    )
    _require(
        not paths["arm_root"].exists(),
        "authorized arm workdir already exists; automatic retry forbidden",
    )
    paths["arm_root"].mkdir(parents=True, exist_ok=False)
    paths["runs"].mkdir(exist_ok=False)

    path_record = build_path_input_record(
        V2R13,
        frozen_source_root=str(paths["source"]),
        exact_engine_root=str(paths["engine"]),
    )

    materialization_receipt: dict[str, Any] | None = None
    portable: portable_checkout.PortableRunnerBinding | None = None
    readiness_hooks: _FreshReadinessHooks | None = None
    candidate_hooks: Any | None = None
    dojo_root: Path | None = None
    dojo_inserted = False
    original_runs_dir: Any | None = None
    old_argv = sys.argv
    original_dont_write_bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True

    try:
        materialization_receipt = (
            worktree_materializer.materialize_v2r13_frozen_worktrees(
                path_record,
                source_repository_root=str(source_repo),
                engine_repository_root=str(engine_repo),
                materialization_authorized=True,
                path_exists=path_exists,
                run_git=run_git,
            )
        )
        _require(
            materialization_receipt.get("materialization_performed") is True,
            "V2R13 frozen worktree materialization did not complete",
        )

        dojo_root, dojo_inserted = _ensure_dojo_import_root()
        legacy = _load_exact_module(
            runner_path,
            LEGACY_RUNNER_SHA256,
            f"void_wc_g2_v2r13_pair_{pair_slot:02d}_{arm}",
        )
        original_runs_dir = legacy.RUNS_DIR
        legacy.RUNS_DIR = paths["runs"]

        portable = portable_checkout.PortableRunnerBinding(
            legacy,
            frozen_source_root=paths["source"],
            exact_engine_root=paths["engine"],
        )
        portable.install()

        readiness_hooks = _FreshReadinessHooks(
            legacy,
            portable,
            pair_slot=pair_slot,
            arm=arm,
            materialization_receipt=materialization_receipt,
            readiness_provider=readiness_provider,
            authority_check=authority_check,
        )
        readiness_hooks.install()

        candidate_binding: dict[str, Any] | None = None
        if arm == "candidate":
            _require(
                candidate_genome_path is not None,
                "candidate genome path required",
            )
            candidate_path = _absolute_normalized_path(
                candidate_genome_path,
                "candidate_genome_path",
            )
            candidate_hooks, candidate_binding = _candidate_hooks(
                legacy,
                candidate_genome_path=candidate_path,
            )
            candidate_hooks.install()
        else:
            _require(
                candidate_genome_path is None,
                "baseline arm must not receive candidate genome path",
            )

        sys.argv = [str(runner_path), *tuple(plan["runner_argv"])]
        legacy.main()

        _require(
            readiness_hooks.runtime_started is True,
            "V2R13 runtime start hook was not reached",
        )
        _require(
            readiness_hooks.readiness_admission is not None,
            "fresh V2R13 readiness was not admitted",
        )
        _require(
            readiness_hooks.runtime_cleanup_completed is True,
            "legacy V2R13 runtime cleanup was not observed",
        )
        artifact = _run_artifact_receipt(paths["runs"])
        body = {
            "schema": RECEIPT_SCHEMA,
            "pair_slot": pair_slot,
            "arm": arm,
            "execution_index": plan["execution_index"],
            "held_out": plan["held_out"],
            "plan_sha256": plan["plan_sha256"],
            "authorization_attestation_sha256": AUTHORIZATION_ATTESTATION_SHA256,
            "runtime_selection_key": V2R13,
            "runtime_execution_authorized": True,
            "runtime_execution_performed": True,
            "runtime_started": True,
            "runtime_cleanup_attempted": True,
            "runtime_cleanup_completed": True,
            "fresh_runtime_readiness_admitted": True,
            "fresh_readiness_admission_sha256": _digest(
                readiness_hooks.readiness_admission
            ),
            "fresh_readiness_evidence_sha256": _digest(
                readiness_hooks.readiness_evidence
            ),
            "revocation_checked_before_materialization": True,
            "revocation_checked_before_inference": True,
            "automatic_retry": False,
            "candidate_binding": deepcopy(candidate_binding),
            "run_artifact": artifact,
            "training_performed": False,
            "weights_updated": False,
            "automatic_policy_promotion": False,
            "deployment_performed": False,
            "void_chain_mutation_performed": False,
            "wallet_or_funds_action_performed": False,
        }
        return {**body, "execution_receipt_sha256": _digest(body)}
    finally:
        sys.argv = old_argv
        sys.dont_write_bytecode = original_dont_write_bytecode
        if candidate_hooks is not None:
            candidate_hooks.restore()
        _restore_dojo_import_root(dojo_root, dojo_inserted)
        if readiness_hooks is not None:
            readiness_hooks.restore()
        if portable is not None:
            portable.restore()
        if "legacy" in locals() and original_runs_dir is not None:
            legacy.RUNS_DIR = original_runs_dir
        if materialization_receipt is not None:
            worktree_materializer.cleanup_v2r13_frozen_worktrees(
                materialization_receipt,
                cleanup_authorized=True,
                path_exists=path_exists,
                run_git=run_git,
            )


def bounded_v2r13_runtime_executor_contract() -> dict[str, Any]:
    authorization = _authorization_contract()
    plans = [
        execution_plan(pair_slot=pair_slot, arm=arm)
        for pair_slot in AUTHORIZED_PAIR_SLOTS
        for arm in AUTHORIZED_ARMS
    ]
    return {
        "schema": CONTRACT_SCHEMA,
        "authorization_source_git_blob": AUTHORIZATION_SOURCE_GIT_BLOB,
        "authorization_attestation_sha256": AUTHORIZATION_ATTESTATION_SHA256,
        "worktree_materializer_review_git_blob": (
            WORKTREE_MATERIALIZER_REVIEW_GIT_BLOB
        ),
        "portable_checkout_git_blob": PORTABLE_CHECKOUT_GIT_BLOB,
        "command_materializer_git_blob": COMMAND_MATERIALIZER_GIT_BLOB,
        "candidate_wrapper_git_blob": CANDIDATE_WRAPPER_GIT_BLOB,
        "candidate_fixture_git_blob": CANDIDATE_FIXTURE_GIT_BLOB,
        "legacy_runner_sha256": LEGACY_RUNNER_SHA256,
        "candidate_wrapper_sha256": CANDIDATE_WRAPPER_SHA256,
        "candidate_fixture_sha256": CANDIDATE_FIXTURE_SHA256,
        "candidate_genome_sha256": CANDIDATE_GENOME_SHA256,
        "bounded_v2r13_runtime_executor_implemented": True,
        "bounded_v2r13_runtime_executor_reviewed": False,
        "authorized_pair_slots": AUTHORIZED_PAIR_SLOTS,
        "held_out_pair_slots": HELD_OUT_PAIR_SLOTS,
        "authorized_arms": AUTHORIZED_ARMS,
        "authorized_execution_arm_count": len(plans),
        "execution_plans": plans,
        "other_runtime_lanes_implemented_by_this_source": False,
        "fresh_readiness_hook_after_runtime_start_before_inference": True,
        "readiness_failure_runtime_cleanup_implemented": True,
        "successful_runtime_cleanup_observation_implemented": True,
        "revocation_check_before_materialization_implemented": True,
        "revocation_check_before_inference_implemented": True,
        "detached_frozen_worktree_composition_implemented": True,
        "portable_runner_binding_composition_implemented": True,
        "candidate_policy_hook_composition_implemented": True,
        "isolated_output_root_implemented": True,
        "automatic_retry": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "runtime_execution_performed_by_contract_inspection": False,
        "model_inference_performed_by_contract_inspection": False,
        "game_execution_performed_by_contract_inspection": False,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "authorization": authorization,
    }


def execute_other_runtime_lane(*args: Any, **kwargs: Any) -> None:
    raise V2R13BoundedRuntimeExecutorHold("AUTHORIZATION_SCOPE_V2R13_ONLY")
