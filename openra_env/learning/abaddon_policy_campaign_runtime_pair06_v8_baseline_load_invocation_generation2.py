"""Guarded one-shot pair-06 baseline V8 runtime-load invocation.

Import and contract inspection perform no host observation and do not load
weights. Operational invocation requires:
* the exact reviewed one-load authorization acceptance;
* an explicit per-call authorization_accepted=True decision;
* the exact confirmation token;
* the designated Python 3.12 environment;
* exact current canonical main;
* exact invocation source bytes;
* fresh accepted V8 environment and 17-file asset verification;
* no revocation sentinel;
* create-only single-use attempt consumption before model load.

The invocation loads weights only. It never calls model inference, starts a
War College game, authorizes the candidate arm, touches held-out pair 15,
trains, promotes, deploys, mutates VOID-chain state, or touches wallets/funds.
A post-claim failure is never automatically retried or reset.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_load_authorization_acceptance_source_binding_review_generation2
    as authorization_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_capability_generation2
    as capability,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_capability_source_binding_review_generation2
    as capability_review,
)

SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-baseline-runtime-load-invocation.v1"
)

AUTHORIZATION_REVIEW_GIT_BLOB = "138aa48ab95d15bd7a4c4ab7b6b87ebce096b409"
AUTHORIZATION_REVIEW_SOURCE_SHA256 = (
    "d050c11375335a2cd4df2018a0cb5edabeb383ca958402afdab6589badf90915"
)
CAPABILITY_REVIEW_GIT_BLOB = "8e405b4d03a7a7310dbedd9fae0edbe9976b4637"
CAPABILITY_REVIEW_SOURCE_SHA256 = (
    "5c4836135629ea47e5e38f6aff0bc61201f754b8354152768e9fbf89c5e000fb"
)

PAIR_SLOT = 6
ARM = "baseline"
HELD_OUT = False
MODEL_DIR = Path(
    "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/model"
)
ADAPTER_DIR = Path(
    "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/adapter-v8"
)
PYTHON_PATH = Path(
    "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/venv/bin/python3.12"
)
SOURCE_ROOT = Path("/home/zoso/dev/openra-rl-war-college")
SELF_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v8_baseline_load_invocation_generation2.py"
)
ATTEMPT_ROOT = Path(
    "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/"
    "pair06-v8-baseline-load-claims-v1"
)
MARKER_NAME = "pair06-v8-baseline-load-attempt-v1.json"
RESULT_NAME = "pair06-v8-baseline-load-result-v1.json"
REVOCATION_NAME = "REVOKE_PAIR06_V8_BASELINE_LOAD"

CONFIRM_TOKEN = "VOID_ABADDON_GENERATION2_PAIR06_V8_LOAD_BASELINE_ONCE"

NEXT_GATE = "PAIR06_V8_BASELINE_RUNTIME_LOAD_INVOCATION_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_pair06_v8_baseline_runtime_load_invocation_review"


class Pair06V8BaselineLoadInvocationHold(RuntimeError):
    """Bounded refusal; claimed attempts are never reset automatically."""


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise Pair06V8BaselineLoadInvocationHold(code)


def _hex(value: Any, size: int) -> bool:
    return (
        type(value) is str
        and len(value) == size
        and all(c in "0123456789abcdef" for c in value)
    )


def _bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
            default=str,
        )
        + "\n"
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_bytes(value)).hexdigest()


def _dependency_contracts() -> dict[str, dict[str, Any]]:
    authorization = (
        authorization_review
        .pair06_v8_baseline_load_authorization_acceptance_review_contract()
    )
    reviewed_capability = (
        capability_review
        .pair06_v8_runtime_capability_review_contract()
    )

    _require(
        authorization.get(
            "pair06_v8_baseline_load_authorization_acceptance_reviewed"
        )
        is True,
        "PAIR06_LOAD_INVOCATION_AUTHORIZATION_REVIEW_HOLD",
    )
    _require(
        authorization.get("authorization_accepted") is True
        and authorization.get("runtime_load_authorized") is True,
        "PAIR06_LOAD_INVOCATION_AUTHORIZATION_HOLD",
    )
    _require(
        authorization.get("pair_slot") == PAIR_SLOT
        and authorization.get("arm") == ARM
        and authorization.get("held_out") is False,
        "PAIR06_LOAD_INVOCATION_AUTHORIZATION_SCOPE_HOLD",
    )
    _require(
        authorization.get("maximum_runtime_load_attempts") == 1
        and authorization.get("automatic_retry") is False,
        "PAIR06_LOAD_INVOCATION_ATTEMPT_BOUND_HOLD",
    )
    _require(
        authorization.get("load_attempt_consumption_required") is True
        and authorization.get("create_only_load_attempt_marker_required") is True,
        "PAIR06_LOAD_INVOCATION_CONSUMPTION_HOLD",
    )
    reviewed_authorization = authorization.get("reviewed_authorization")
    _require(
        isinstance(reviewed_authorization, dict),
        "PAIR06_LOAD_INVOCATION_REVIEWED_AUTHORIZATION_HOLD",
    )
    reviewed_request = reviewed_authorization.get("reviewed_request")
    _require(
        isinstance(reviewed_request, dict)
        and reviewed_request.get("model_dir") == str(MODEL_DIR)
        and reviewed_request.get("adapter_dir") == str(ADAPTER_DIR)
        and reviewed_request.get("python_path") == str(PYTHON_PATH),
        "PAIR06_LOAD_INVOCATION_PATH_BINDING_HOLD",
    )

    _require(
        reviewed_capability.get("pair06_v8_runtime_capability_reviewed") is True,
        "PAIR06_LOAD_INVOCATION_CAPABILITY_REVIEW_HOLD",
    )
    _require(
        reviewed_capability.get("runtime_loader_callable_bound") is True,
        "PAIR06_LOAD_INVOCATION_LOADER_BINDING_HOLD",
    )
    _require(
        reviewed_capability.get("runtime_environment_verification_required_before_load")
        is True
        and reviewed_capability.get(
            "runtime_assets_hash_verification_required_before_load"
        )
        is True
        and reviewed_capability.get("offline_only_model_load_required") is True,
        "PAIR06_LOAD_INVOCATION_PRELOAD_BOUNDARY_HOLD",
    )
    _require(
        reviewed_capability.get("authority_callback_required") is True,
        "PAIR06_LOAD_INVOCATION_AUTHORITY_CALLBACK_HOLD",
    )
    return {
        "authorization_review": deepcopy(authorization),
        "capability_review": deepcopy(reviewed_capability),
    }


def pair06_v8_baseline_load_invocation_contract() -> dict[str, Any]:
    dependencies = _dependency_contracts()
    return {
        "schema": SCHEMA,
        "authorization_review_git_blob": AUTHORIZATION_REVIEW_GIT_BLOB,
        "authorization_review_source_sha256": AUTHORIZATION_REVIEW_SOURCE_SHA256,
        "capability_review_git_blob": CAPABILITY_REVIEW_GIT_BLOB,
        "capability_review_source_sha256": CAPABILITY_REVIEW_SOURCE_SHA256,
        "pair06_v8_baseline_load_invocation_implemented": True,
        "pair06_v8_baseline_load_invocation_reviewed": False,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "runtime_load_authorized_by_reviewed_dependency": True,
        "explicit_authorization_boolean_required": True,
        "explicit_confirmation_token_required": True,
        "exact_current_main_required": True,
        "exact_invocation_source_sha256_required": True,
        "designated_python_required": True,
        "fresh_runtime_environment_verification_required": True,
        "runtime_asset_hash_verification_required": True,
        "offline_only_model_load_required": True,
        "revocation_check_required_before_claim": True,
        "revocation_check_required_after_claim": True,
        "single_use_attempt_consumption_required": True,
        "single_use_attempt_consumed": False,
        "automatic_retry": False,
        "runtime_load_performed": False,
        "model_weights_loaded": False,
        "candidate_runtime_load_authorized": False,
        "model_inference_authorized": False,
        "model_inference_performed": False,
        "game_execution_authorized": False,
        "game_execution_performed": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "dependencies": dependencies,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def _check_python() -> None:
    _require(
        sys.dont_write_bytecode is True,
        "PAIR06_LOAD_INVOCATION_BYTECODE_DISABLED_REQUIRED",
    )
    _require(
        Path(sys.executable) == PYTHON_PATH
        and (sys.version_info.major, sys.version_info.minor) == (3, 12),
        "PAIR06_LOAD_INVOCATION_DESIGNATED_PYTHON_REQUIRED",
    )


def _verify_self(expected_invocation_source_sha256: str) -> str:
    source = SOURCE_ROOT / SELF_PATH
    _require(
        Path(__file__) == source,
        "PAIR06_LOAD_INVOCATION_ORIGIN_HOLD",
    )
    raw = source.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    _require(
        actual == expected_invocation_source_sha256,
        "PAIR06_LOAD_INVOCATION_SOURCE_DRIFT",
    )
    return actual


def _git(*args: str) -> str:
    proc = subprocess.run(
        ["/usr/bin/git", "-C", str(SOURCE_ROOT), *args],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
        env={
            "PATH": "/usr/bin:/bin",
            "LC_ALL": "C",
            "LANG": "C",
        },
    )
    _require(proc.returncode == 0, "PAIR06_LOAD_INVOCATION_GIT_QUERY_HOLD")
    return proc.stdout.strip()


def _current_main(expected_main_head: str) -> dict[str, str]:
    _require(
        _git("symbolic-ref", "-q", "HEAD") == "refs/heads/main",
        "PAIR06_LOAD_INVOCATION_MAIN_BRANCH_HOLD",
    )
    head = _git("rev-parse", "HEAD")
    tree = _git("rev-parse", "HEAD^{tree}")
    _require(
        head == expected_main_head and _hex(tree, 40),
        "PAIR06_LOAD_INVOCATION_MAIN_IDENTITY_HOLD",
    )
    rows = _git(
        "status",
        "--porcelain",
        "--untracked-files=all",
    ).splitlines()
    _require(
        all(row.startswith("?? ") for row in rows),
        "PAIR06_LOAD_INVOCATION_TRACKED_SOURCE_DIRTY",
    )
    return {"head": head, "tree": tree}


def _not_revoked() -> None:
    if (ATTEMPT_ROOT / REVOCATION_NAME).exists():
        raise Pair06V8BaselineLoadInvocationHold(
            "PAIR06_LOAD_INVOCATION_REVOKED"
        )


def _fresh_preflight() -> dict[str, Any]:
    from openra_env.learning import apollyon_v8_campaign_runtime as v8_runtime

    environment = v8_runtime.verify_v8_runtime_environment()
    assets = v8_runtime.verify_v8_runtime_assets(
        model_dir=MODEL_DIR,
        adapter_dir=ADAPTER_DIR,
    )
    _require(
        assets.get("verified_file_count") == 17,
        "PAIR06_LOAD_INVOCATION_ASSET_COUNT_HOLD",
    )
    _require(
        assets.get("runtime_execution_performed") is False
        and assets.get("model_execution_performed") is False,
        "PAIR06_LOAD_INVOCATION_PREFLIGHT_EXECUTION_HOLD",
    )
    return {
        "runtime_environment": deepcopy(environment),
        "runtime_assets": {
            **deepcopy(assets),
            "model_dir": str(assets["model_dir"]),
            "adapter_dir": str(assets["adapter_dir"]),
        },
    }


def _claims_root() -> Path:
    ATTEMPT_ROOT.mkdir(parents=True, exist_ok=True, mode=0o700)
    observed = ATTEMPT_ROOT.lstat()
    _require(
        stat.S_ISDIR(observed.st_mode)
        and not stat.S_ISLNK(observed.st_mode)
        and observed.st_uid == os.geteuid(),
        "PAIR06_LOAD_INVOCATION_CLAIMS_ROOT_HOLD",
    )
    os.chmod(ATTEMPT_ROOT, 0o700)
    return ATTEMPT_ROOT


def _write_create_only(path: Path, value: dict[str, Any]) -> str:
    raw = _bytes(value)
    flags = (
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL
        | os.O_NOFOLLOW
        | os.O_CLOEXEC
    )
    try:
        fd = os.open(path, flags, 0o600)
    except FileExistsError as exc:
        raise Pair06V8BaselineLoadInvocationHold(
            "PAIR06_LOAD_INVOCATION_CREATE_ONLY_COLLISION"
        ) from exc
    try:
        os.fchmod(fd, 0o600)
        offset = 0
        while offset < len(raw):
            count = os.write(fd, raw[offset:])
            _require(count > 0, "PAIR06_LOAD_INVOCATION_WRITE_HOLD")
            offset += count
        os.fsync(fd)
        observed = os.fstat(fd)
        _require(
            stat.S_ISREG(observed.st_mode)
            and observed.st_nlink == 1
            and observed.st_size == len(raw),
            "PAIR06_LOAD_INVOCATION_FILE_SHAPE_HOLD",
        )
    finally:
        os.close(fd)
    return hashlib.sha256(raw).hexdigest()


def execute_pair06_baseline_load(
    *,
    expected_main_head: str,
    expected_invocation_source_sha256: str,
    authorization_accepted: bool,
    confirm: str,
) -> dict[str, Any]:
    _require(
        _hex(expected_main_head, 40),
        "PAIR06_LOAD_INVOCATION_EXPECTED_MAIN_HEAD_REQUIRED",
    )
    _require(
        _hex(expected_invocation_source_sha256, 64),
        "PAIR06_LOAD_INVOCATION_EXPECTED_SOURCE_SHA_REQUIRED",
    )
    _require(
        type(authorization_accepted) is bool and authorization_accepted is True,
        "PAIR06_LOAD_INVOCATION_EXPLICIT_AUTHORIZATION_REQUIRED",
    )
    _require(
        type(confirm) is str and confirm == CONFIRM_TOKEN,
        "PAIR06_LOAD_INVOCATION_CONFIRMATION_REQUIRED",
    )

    dependencies = _dependency_contracts()
    _check_python()
    actual_source_sha256 = _verify_self(expected_invocation_source_sha256)
    main_before = _current_main(expected_main_head)
    _not_revoked()
    preflight = _fresh_preflight()

    root = _claims_root()
    marker = root / MARKER_NAME
    result_path = root / RESULT_NAME
    _require(
        not result_path.exists(),
        "PAIR06_LOAD_INVOCATION_PRIOR_RESULT_PRESENT",
    )
    _require(
        not marker.exists(),
        "PAIR06_LOAD_INVOCATION_PRIOR_ATTEMPT_PRESENT",
    )

    authorization = dependencies["authorization_review"]
    marker_payload = {
        "schema": (
            "void.abaddon.generation2."
            "pair06-v8-baseline-runtime-load-attempt.v1"
        ),
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "expected_main_head": expected_main_head,
        "main_tree": main_before["tree"],
        "invocation_source_sha256": actual_source_sha256,
        "authorization_attestation_sha256": authorization[
            "authorization_attestation_sha256"
        ],
        "runtime_load_authorized": True,
        "runtime_load_performed": False,
        "model_weights_loaded": False,
        "automatic_retry": False,
        "candidate_runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
    }
    marker_sha256 = _write_create_only(marker, marker_payload)

    _current_main(expected_main_head)
    _not_revoked()

    def authority_check(pair_slot: int, arm: str) -> bool:
        if pair_slot != PAIR_SLOT or arm != ARM:
            return False
        if (ATTEMPT_ROOT / REVOCATION_NAME).exists():
            return False
        return True

    runtime = capability.load_pair06_v8_runtime(
        pair_slot=PAIR_SLOT,
        arm=ARM,
        model_dir=str(MODEL_DIR),
        adapter_dir=str(ADAPTER_DIR),
        runtime_load_authorized=True,
        authority_check=authority_check,
    )
    _require(
        getattr(runtime, "model", None) is not None
        and getattr(runtime, "tokenizer", None) is not None,
        "PAIR06_LOAD_INVOCATION_RUNTIME_OBJECT_HOLD",
    )

    result_payload = {
        "schema": (
            "void.abaddon.generation2."
            "pair06-v8-baseline-runtime-load-result.v1"
        ),
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "main_head": expected_main_head,
        "main_tree": main_before["tree"],
        "invocation_source_sha256": actual_source_sha256,
        "authorization_attestation_sha256": authorization[
            "authorization_attestation_sha256"
        ],
        "attempt_marker_sha256": marker_sha256,
        "runtime_load_authorized": True,
        "runtime_load_performed": True,
        "model_weights_loaded": True,
        "automatic_retry": False,
        "candidate_runtime_load_authorized": False,
        "model_inference_authorized": False,
        "model_inference_performed": False,
        "game_execution_authorized": False,
        "game_execution_performed": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "training_performed": False,
        "weights_update_authorized": False,
        "weights_updated": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "deployment_performed": False,
        "void_chain_mutation_authorized": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_authorized": False,
        "wallet_or_funds_action_performed": False,
        "preflight": preflight,
    }
    result_sha256 = _write_create_only(result_path, result_payload)
    return {
        **deepcopy(result_payload),
        "result_file": str(result_path),
        "result_file_sha256": result_sha256,
    }
