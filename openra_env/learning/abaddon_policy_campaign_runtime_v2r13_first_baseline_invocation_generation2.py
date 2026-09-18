"""Bounded Precision invocation for the first Generation-2 V2R13 arm.

The only executable arm implemented here is pair slot 03 baseline.  Importing
or inspecting this module performs no host action.  A caller must explicitly
supply the exact confirmation token to the invocation function.

Before runtime execution, the invocation re-runs the merged full Precision host
preflight against the CURRENT local main HEAD, requires cached sudo authority
for the reviewed legacy runner, requires the revocation sentinel to be absent,
and verifies the accepted historical preflight evidence contract.

During runtime startup the already-reviewed bounded executor injects fresh
canonical V2R13 readiness collection after Ollama/model startup and before the
first model decision.  The authority callback is checked again after readiness.

No candidate arm, held-out arm, training, weight update, automatic promotion,
deployment, VOID-chain mutation, or wallet/funds action is implemented here.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_bounded_executor_generation2 as executor,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_entrypoint_binding_generation2
    as live_entrypoint_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_entrypoint_generation2
    as live_entrypoint,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_host_preflight_evidence_acceptance_generation2
    as preflight_acceptance,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_host_preflight_generation2 as host_preflight,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_ollama_readonly_observer_generation2
    as ollama_observer,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_rootless_docker_image_backend_generation2
    as docker_backend,
)
from tools import (
    abaddon_policy_campaign_runtime_v2r13_precision_host_preflight_generation2
    as precision_preflight,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-first-baseline-runtime-invocation-contract.v1"
)
INVOCATION_RECEIPT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-first-baseline-runtime-invocation-receipt.v1"
)

PAIR_SLOT = 3
ARM = "baseline"
HELD_OUT = False
CONFIRM_TOKEN = "VOID_ABADDON_GENERATION2_V2R13_EXECUTE_PAIR03_BASELINE"

SOURCE_ROOT = Path("/home/zoso/dev/openra-rl-war-college")
ENGINE_ROOT = SOURCE_ROOT / "OpenRA"
ISOLATED_ROOT = Path(
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2"
)
LEGACY_RUNNER = Path(
    "/home/zoso/Downloads/"
    "void-actual-apollyon-vs-abaddon-warm-start-combat-spar-v1_4.py"
)
PROTO_PYTHON = Path(
    "/home/zoso/.local/share/void-tools/openra-bridge-proto-v1/venv/bin/python"
)
REVOCATION_SENTINEL = ISOLATED_ROOT / "REVOKE_V2R13"
ARM_ROOT = ISOLATED_ROOT / "generation2" / "pair-03" / "baseline"
INVOCATION_RECEIPT_PATH = ARM_ROOT / "execution-receipt-generation2.json"

HISTORICAL_PREFLIGHT_SNAPSHOT_SHA256 = (
    "9a15a64e62e7f06cb0444f6e0dc830ddae9d9c262378f7f1f705d273aab7e364"
)
AUTHORIZATION_ATTESTATION_SHA256 = (
    "34ad7143e876b91056f730de37ab470b6fd8a5f99d84aadefb178cabf87a2031"
)

NEXT_GATE = "V2R13_PAIR03_BASELINE_EXECUTION_EVIDENCE_ACCEPTANCE_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_v2r13_pair03_baseline_execution_evidence_acceptance"


class V2R13FirstBaselineInvocationHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise V2R13FirstBaselineInvocationHold(message)


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


def _run_capture(
    argv: list[str],
    *,
    cwd: Path | None = None,
    allowed_returncodes: tuple[int, ...] = (0,),
) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(
        argv,
        cwd=str(cwd) if cwd is not None else None,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
    )
    _require(
        cp.returncode in allowed_returncodes,
        f"command failed rc={cp.returncode}: {argv!r}",
    )
    return cp


def _git_query(*args: str) -> str:
    return _run_capture(["git", "-C", str(SOURCE_ROOT), *args]).stdout.strip()


def _validate_git_args(args: tuple[str, ...]) -> None:
    """Restrict the injected Git backend to reviewed materializer operations."""
    _require(bool(args), "empty Git command")
    command = args[0]

    if command == "rev-parse":
        _require(len(args) in {2, 3}, "unsupported rev-parse shape")
        return

    if command == "status":
        _require(
            args == ("status", "--porcelain", "--untracked-files=all"),
            "unsupported status shape",
        )
        return

    if command == "symbolic-ref":
        _require(
            args == ("symbolic-ref", "-q", "HEAD"),
            "unsupported symbolic-ref shape",
        )
        return

    if command == "worktree":
        _require(len(args) >= 2, "malformed worktree command")
        if args[1:] == ("list", "--porcelain"):
            return
        if len(args) == 5 and args[1] == "add" and args[2] == "--detach":
            destination = Path(args[3])
            _require(destination.is_absolute(), "worktree destination must be absolute")
            _require(
                str(destination).startswith(str(ARM_ROOT) + "/"),
                "worktree add destination escaped pair-03 baseline root",
            )
            return
        if len(args) == 3 and args[1] == "remove":
            destination = Path(args[2])
            _require(destination.is_absolute(), "worktree removal target must be absolute")
            _require(
                str(destination).startswith(str(ARM_ROOT) + "/"),
                "worktree remove target escaped pair-03 baseline root",
            )
            return
        raise V2R13FirstBaselineInvocationHold("unsupported worktree command")

    raise V2R13FirstBaselineInvocationHold(
        f"Git command not allowed for bounded invocation: {command}"
    )


def reviewed_git_runner(
    repository_root: str,
    *args: str,
) -> subprocess.CompletedProcess[str]:
    """Run only the exact Git operations required by the reviewed materializer."""
    root = Path(repository_root)
    _require(root.is_absolute(), "Git repository root must be absolute")
    _validate_git_args(tuple(args))
    return _run_capture(
        ["git", "-C", str(root), *args],
        allowed_returncodes=(0, 1),
    )


def reviewed_path_exists(path: str) -> bool:
    value = Path(path)
    _require(value.is_absolute(), "path-existence query must be absolute")
    return value.exists()


def _validate_confirmation(confirm: str) -> None:
    _require(confirm == CONFIRM_TOKEN, "FIRST_BASELINE_EXECUTION_CONFIRMATION_REQUIRED")


def _accepted_authority_contract() -> dict[str, Any]:
    accepted = preflight_acceptance.v2r13_host_preflight_evidence_acceptance_contract()
    _require(
        accepted.get("host_preflight_evidence_accepted") is True,
        "host preflight evidence acceptance missing",
    )
    _require(
        accepted.get("host_preflight_snapshot_sha256")
        == HISTORICAL_PREFLIGHT_SNAPSHOT_SHA256,
        "historical host-preflight snapshot identity drift",
    )
    _require(
        accepted.get("runtime_execution_authorized") is True,
        "runtime execution authority missing",
    )
    _require(
        accepted.get("runtime_execution_performed") is False,
        "runtime already marked executed before first invocation",
    )
    _require(
        accepted.get("fresh_readiness_still_required_before_inference") is True,
        "fresh readiness requirement lost",
    )
    _require(accepted.get("automatic_retry") is False, "automatic retry enabled")
    return accepted


def _current_repo_identity() -> dict[str, str]:
    _require(SOURCE_ROOT.is_dir(), "source root missing")
    branch = _git_query("branch", "--show-current")
    head = _git_query("rev-parse", "HEAD")
    tree = _git_query("rev-parse", "HEAD^{tree}")
    tracked = _run_capture(
        [
            "git",
            "-C",
            str(SOURCE_ROOT),
            "status",
            "--porcelain",
            "--untracked-files=no",
        ]
    ).stdout.strip()
    _require(branch == "main", "execution requires current checkout on main")
    _require(tracked == "", "execution requires tracked-clean current main")
    return {"branch": branch, "head": head, "tree": tree}


def _current_host_preflight(head: str) -> dict[str, Any]:
    args = SimpleNamespace(
        expected_main_head=head,
        source_repository_root=str(SOURCE_ROOT),
        engine_repository_root=str(ENGINE_ROOT),
        isolated_workdir_root=str(ISOLATED_ROOT),
    )
    snapshot = precision_preflight.collect(args)
    admission = host_preflight.validate_host_preflight_snapshot(snapshot)
    _require(admission.get("host_preflight_green") is True, "fresh host preflight not green")
    _require(
        admission.get("runtime_execution_authorized") is True,
        "fresh host preflight lost runtime authority",
    )
    _require(
        admission.get("runtime_execution_performed") is False,
        "fresh host preflight unexpectedly executed runtime",
    )
    return {
        "snapshot": snapshot,
        "admission": admission,
    }


def _sudo_cache_ready() -> bool:
    cp = subprocess.run(
        ["sudo", "-n", "true"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return cp.returncode == 0


def _authority_check_factory(expected_head: str):
    accepted = _accepted_authority_contract()

    def authority_check(pair_slot: int, arm: str) -> bool:
        if pair_slot != PAIR_SLOT or arm != ARM:
            return False
        if REVOCATION_SENTINEL.exists():
            return False
        try:
            current = _current_repo_identity()
        except Exception:
            return False
        if current["head"] != expected_head:
            return False
        if accepted.get("runtime_execution_authorized") is not True:
            return False
        return True

    return authority_check


def _fresh_readiness_provider(context: Mapping[str, Any]) -> Mapping[str, Any]:
    _require(isinstance(context, Mapping), "fresh readiness context missing")
    receipt = live_entrypoint.collect_v2r13_canonical_live_collection(
        collection_authorized=True,
        observation_authorized=True,
        http_get=ollama_observer.host_http_get,
        run_command=docker_backend.host_readonly_command_runner,
        worktree_receipt=context["materialization_receipt"],
        portable_binding_attestation=context["portable_binding_attestation"],
    )
    validation = (
        live_entrypoint_binding
        .validate_bound_canonical_live_collection_entrypoint_receipt(
            receipt,
            entrypoint_source_sha256=live_entrypoint_binding.ENTRYPOINT_SOURCE_SHA256,
        )
    )
    _require(
        validation.get("bound_entrypoint_receipt_valid") is True,
        "fresh canonical live-readiness receipt invalid",
    )
    _require(
        validation.get("canonical_live_collection_path_complete") is True,
        "fresh canonical live-readiness path incomplete",
    )
    _require(
        validation.get("runtime_readiness_admitted") is True,
        "fresh runtime readiness not admitted",
    )
    _require(
        validation.get("runtime_execution_authorized") is False,
        "fresh readiness receipt unexpectedly carries runtime authority",
    )
    return dict(receipt["activation_evidence"])


def _write_invocation_receipt(receipt: Mapping[str, Any]) -> None:
    _require(ARM_ROOT.is_dir(), "pair-03 baseline arm root missing after execution")
    _require(
        INVOCATION_RECEIPT_PATH.exists() is False,
        "invocation receipt already exists; automatic retry forbidden",
    )
    raw = (
        json.dumps(
            receipt,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
            default=str,
        )
        + "\n"
    ).encode("utf-8")
    fd = os.open(
        INVOCATION_RECEIPT_PATH,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
        0o600,
    )
    try:
        with os.fdopen(fd, "wb", closefd=True) as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        raise


def execute_first_baseline(*, confirm: str) -> dict[str, Any]:
    """Execute exactly pair-03 baseline once after all reviewed gates pass."""
    _validate_confirmation(confirm)
    _require(Path(os.path.realpath(sys.executable)) == PROTO_PYTHON.resolve(), (
        f"execution requires isolated gRPC Python: {PROTO_PYTHON}"
    ))
    _accepted_authority_contract()

    _require(ISOLATED_ROOT.is_dir(), "isolated execution root missing")
    _require(not ISOLATED_ROOT.is_symlink(), "isolated execution root is symlink")
    _require(ARM_ROOT.exists() is False, "pair-03 baseline already materialized")
    _require(REVOCATION_SENTINEL.exists() is False, "V2R13 execution revoked")
    _require(_sudo_cache_ready(), "CACHED_SUDO_AUTHORITY_REQUIRED")

    repo_identity = _current_repo_identity()
    fresh_preflight = _current_host_preflight(repo_identity["head"])
    authority_check = _authority_check_factory(repo_identity["head"])

    execution_receipt = executor.execute_v2r13_arm(
        pair_slot=PAIR_SLOT,
        arm=ARM,
        isolated_workdir_root=str(ISOLATED_ROOT),
        source_repository_root=str(SOURCE_ROOT),
        engine_repository_root=str(ENGINE_ROOT),
        legacy_runner_path=str(LEGACY_RUNNER),
        candidate_genome_path=None,
        execution_authorized=True,
        authority_check=authority_check,
        readiness_provider=_fresh_readiness_provider,
        path_exists=reviewed_path_exists,
        run_git=reviewed_git_runner,
    )

    _require(execution_receipt.get("pair_slot") == PAIR_SLOT, "execution pair-slot drift")
    _require(execution_receipt.get("arm") == ARM, "execution arm drift")
    _require(execution_receipt.get("held_out") is False, "baseline unexpectedly held-out")
    _require(
        execution_receipt.get("runtime_execution_performed") is True,
        "pair-03 baseline execution not completed",
    )
    _require(
        execution_receipt.get("runtime_cleanup_completed") is True,
        "pair-03 baseline runtime cleanup not completed",
    )
    _require(
        execution_receipt.get("fresh_runtime_readiness_admitted") is True,
        "pair-03 baseline fresh readiness not admitted",
    )
    for field in (
        "training_performed",
        "weights_updated",
        "automatic_policy_promotion",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        _require(execution_receipt.get(field) is False, f"execution boundary drift: {field}")

    body = {
        "schema": INVOCATION_RECEIPT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "confirmation_token": CONFIRM_TOKEN,
        "historical_preflight_snapshot_sha256": HISTORICAL_PREFLIGHT_SNAPSHOT_SHA256,
        "current_main_head": repo_identity["head"],
        "current_main_tree": repo_identity["tree"],
        "fresh_host_preflight_snapshot_sha256": (
            fresh_preflight["admission"]["snapshot_sha256"]
        ),
        "authorization_attestation_sha256": AUTHORIZATION_ATTESTATION_SHA256,
        "runtime_execution_performed": True,
        "fresh_runtime_readiness_admitted": True,
        "runtime_cleanup_completed": True,
        "automatic_retry": False,
        "candidate_arm_executed": False,
        "held_out_arm_executed": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "executor_receipt": execution_receipt,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }
    receipt = {**body, "invocation_receipt_sha256": _digest(body)}
    _write_invocation_receipt(receipt)
    return receipt


def first_baseline_invocation_contract() -> dict[str, Any]:
    """Return source-only capabilities; never execute runtime."""
    accepted = _accepted_authority_contract()
    return {
        "schema": CONTRACT_SCHEMA,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "confirm_token": CONFIRM_TOKEN,
        "historical_preflight_snapshot_sha256": HISTORICAL_PREFLIGHT_SNAPSHOT_SHA256,
        "execution_requires_current_main_preflight": True,
        "execution_requires_cached_sudo_authority": True,
        "execution_requires_revocation_sentinel_absent": True,
        "revocation_sentinel": str(REVOCATION_SENTINEL),
        "execution_requires_isolated_grpc_python": True,
        "isolated_grpc_python": str(PROTO_PYTHON),
        "restricted_git_worktree_backend_implemented": True,
        "fresh_canonical_live_readiness_before_inference_implemented": True,
        "fresh_readiness_uses_reviewed_ollama_http_backend": True,
        "fresh_readiness_uses_reviewed_rootless_docker_backend": True,
        "candidate_arm_implemented_by_this_source": False,
        "held_out_arm_implemented_by_this_source": False,
        "automatic_retry": False,
        "runtime_execution_authorized": True,
        "runtime_execution_performed_by_contract_inspection": False,
        "model_inference_performed_by_contract_inspection": False,
        "game_execution_performed_by_contract_inspection": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "next_gate": "V2R13_FIRST_BASELINE_INVOCATION_SOURCE_BINDING_REVIEW_REQUIRED",
        "next_change_class": (
            "source_only_v2r13_first_baseline_invocation_source_binding_review"
        ),
        "accepted_preflight_evidence_contract": accepted,
    }
