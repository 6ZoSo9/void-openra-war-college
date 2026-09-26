"""One-shot combat-priority pair-06 V8 baseline invocation.

This source composes the already-reviewed receipt-bound/no-offload/fresh
preclaim-GPU invocation helpers with the reviewed combat-priority parent
supervisor wiring.

It intentionally uses a new create-only marker/result/closeout namespace and a
new runs root so the previously consumed baseline attempt and preserved run
artifacts cannot be reused or overwritten.

Execution remains impossible without all of:
* exact current main;
* exact invocation-source SHA-256;
* explicit pair-06 execution authorization;
* explicit combat-priority policy activation authorization;
* exact execution confirmation token;
* exact policy activation confirmation token;
* fresh preclaim CUDA:0 admission;
* a fresh create-only combat-priority attempt marker.

Maximum attempts is one. Automatic retry is forbidden.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_generation2
    as base_invocation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_source_binding_review_generation2
    as base_invocation_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_parent_supervisor_wiring_generation2
    as combat_parent,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_parent_supervisor_wiring_source_binding_review_generation2
    as combat_parent_review,
)


SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-priority-baseline-game-attempt-invocation-"
    "receipt-bound-no-offload-preclaim-gpu.v1"
)
CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-priority-baseline-attempt-invocation-"
    "receipt-bound-no-offload-preclaim-gpu-contract.v1"
)

PAIR_SLOT = 6
ARM = "baseline"
HELD_OUT = False

SOURCE_ROOT = Path(base_invocation.SOURCE_ROOT)
ARM_ROOT = Path(base_invocation.ARM_ROOT)
CLAIMS_ROOT = Path(base_invocation.CLAIMS_ROOT)
FROZEN_SOURCE_ROOT = Path(base_invocation.FROZEN_SOURCE_ROOT)
EXACT_ENGINE_ROOT = Path(base_invocation.EXACT_ENGINE_ROOT)
RUNS_ROOT = ARM_ROOT / "runs-combat-priority-v1"

MARKER_NAME = "pair06-v8-combat-priority-baseline-game-attempt-v1.json"
RESULT_NAME = "pair06-v8-combat-priority-baseline-game-result-v1.json"
CLOSEOUT_NAME = "pair06-v8-combat-priority-baseline-game-closeout-v1.json"
REVOCATION_NAME = "REVOKE_PAIR06_V8_COMBAT_PRIORITY_GAME"

SELF_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v8_"
    "combat_action_priority_baseline_attempt_invocation_"
    "receipt_bound_no_offload_preclaim_gpu_generation2.py"
)

V8_PYTHON = Path(base_invocation.V8_PYTHON)

EXECUTION_CONFIRM_TOKEN = (
    "VOID_PAIR06_V8_COMBAT_PRIORITY_RECEIPT_BOUND_NO_OFFLOAD_"
    "PRECLAIM_GPU_EXECUTE_ONCE"
)
POLICY_CONFIRM_TOKEN = (
    "VOID_PAIR06_V8_COMBAT_PRIORITY_POLICY_ACTIVATE_ONCE"
)

PARENT_WIRING_REVIEW_MAIN_HEAD = (
    "beda5d24ad1e457d295ca4a28f3b49beba5e3f2f"
)
PARENT_WIRING_REVIEW_GIT_BLOB = (
    "0e39c82eb1ba93ada017f7118da45318fd8ad84e"
)
PARENT_WIRING_REVIEW_SOURCE_SHA256 = (
    "3a7e605f10670c1c5797706725a0097e8d5cd2a891fe52a899abe75ed7a551ed"
)

BASE_PRECLAIM_GPU_REVIEW_GIT_BLOB = (
    "77dbac309565beb804ac1c2936799574efe5de82"
)
BASE_PRECLAIM_GPU_REVIEW_SOURCE_SHA256 = (
    "beec87bea767fdb0c13c14ed7072d49b8fb18db08f6745c22172931ce8843cce"
)

NEXT_GATE = (
    "PAIR06_V8_COMBAT_ACTION_PRIORITY_BASELINE_ATTEMPT_INVOCATION_"
    "RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v8_combat_action_priority_baseline_attempt_invocation_"
    "receipt_bound_no_offload_preclaim_gpu_review"
)


class Pair06V8CombatPriorityInvocationHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CombatPriorityInvocationHold(message)


def _dependency_contracts() -> dict[str, Any]:
    parent = (
        combat_parent_review
        .pair06_v8_combat_priority_parent_supervisor_wiring_review_contract()
    )
    base = (
        base_invocation_review
        .pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_review_contract()
    )

    _require(
        parent.get(
            "pair06_v8_combat_priority_parent_supervisor_wiring_reviewed"
        )
        is True,
        "PAIR06_V8_COMBAT_PRIORITY_PARENT_WIRING_NOT_REVIEWED",
    )
    _require(
        parent.get("canonical_invocation_lane")
        == "receipt_bound_no_offload_fresh_preclaim_gpu",
        "PAIR06_V8_COMBAT_PRIORITY_INVOCATION_LANE_DRIFT",
    )
    _require(
        parent.get("maximum_attempts_required") == 1
        and parent.get("automatic_retry_required") is False,
        "PAIR06_V8_COMBAT_PRIORITY_ATTEMPT_BOUND_DRIFT",
    )
    _require(
        parent.get("fresh_preclaim_gpu_observation_required") is True
        and parent.get(
            "fresh_preclaim_gpu_observation_must_precede_attempt_marker"
        )
        is True
        and parent.get("durable_create_only_attempt_marker_required") is True
        and parent.get(
            "attempt_marker_must_precede_model_load_and_child_spawn"
        )
        is True,
        "PAIR06_V8_COMBAT_PRIORITY_PRECLAIM_ORDER_DRIFT",
    )
    _require(
        parent.get("attempt_marker_creation_authorized") is False
        and parent.get("runtime_execution_authorized") is False,
        "PAIR06_V8_COMBAT_PRIORITY_PARENT_REVIEW_AUTHORITY_DRIFT",
    )
    _require(
        parent.get("next_gate")
        == (
            "PAIR06_V8_COMBAT_ACTION_PRIORITY_BASELINE_ATTEMPT_INVOCATION_"
            "RECEIPT_BOUND_NO_OFFLOAD_PRECLAIM_GPU_REQUIRED"
        ),
        "PAIR06_V8_COMBAT_PRIORITY_PARENT_FRONTIER_DRIFT",
    )

    _require(
        base.get(
            "pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_"
            "preclaim_gpu_reviewed"
        )
        is True,
        "PAIR06_V8_BASE_PRECLAIM_GPU_INVOCATION_NOT_REVIEWED",
    )
    _require(
        base.get("maximum_attempts") == 1
        and base.get("maximum_automatic_retries") == 0,
        "PAIR06_V8_BASE_PRECLAIM_GPU_ATTEMPT_BOUND_DRIFT",
    )
    _require(
        base.get("fresh_preclaim_gpu_observation_required") is True
        and base.get(
            "fresh_preclaim_gpu_observation_precedes_attempt_marker"
        )
        is True
        and base.get("zero_foreign_cuda0_compute_processes_required") is True
        and base.get("minimum_cuda0_free_memory_fraction_numerator") == 9
        and base.get("minimum_cuda0_free_memory_fraction_denominator") == 10,
        "PAIR06_V8_BASE_PRECLAIM_GPU_ADMISSION_DRIFT",
    )
    _require(
        base.get("historical_gpu_observation_reusable") is False
        and base.get("spent_receipt_bound_request_reusable") is False
        and base.get("spent_oom_attempt_reusable") is False,
        "PAIR06_V8_BASE_PRECLAIM_GPU_REUSE_DRIFT",
    )
    _require(
        base.get("attempt_marker_creation_authorized") is False
        and base.get("game_execution_authorized") is False,
        "PAIR06_V8_BASE_PRECLAIM_GPU_REVIEW_AUTHORITY_DRIFT",
    )

    return {
        "combat_priority_parent_wiring_review": deepcopy(parent),
        "base_preclaim_gpu_invocation_review": deepcopy(base),
    }


def _verify_self(expected_source_sha256: str) -> str:
    source = SOURCE_ROOT / SELF_PATH
    _require(
        Path(__file__) == source,
        "PAIR06_V8_COMBAT_PRIORITY_INVOCATION_ORIGIN_HOLD",
    )
    actual = hashlib.sha256(source.read_bytes()).hexdigest()
    _require(
        actual == expected_source_sha256,
        "PAIR06_V8_COMBAT_PRIORITY_INVOCATION_SOURCE_DRIFT",
    )
    return actual


def _not_revoked() -> None:
    if (CLAIMS_ROOT / REVOCATION_NAME).exists():
        raise Pair06V8CombatPriorityInvocationHold(
            "PAIR06_V8_COMBAT_PRIORITY_INVOCATION_REVOKED"
        )
    if (CLAIMS_ROOT / base_invocation.REVOCATION_NAME).exists():
        raise Pair06V8CombatPriorityInvocationHold(
            "PAIR06_V8_BASELINE_INVOCATION_REVOKED"
        )


def _prepare_directories() -> None:
    base_invocation._ensure_private_dir(ARM_ROOT)
    base_invocation._ensure_private_dir(CLAIMS_ROOT)
    base_invocation._require_empty_directory(RUNS_ROOT)


def _cleanup_preclaim(
    materialization: Mapping[str, Any],
    backend: Any,
) -> None:
    try:
        base_invocation.materializer.cleanup_v2r13_frozen_worktrees(
            materialization,
            cleanup_authorized=True,
            path_exists=backend.path_exists,
            run_git=backend.run_git,
        )
    except BaseException as cleanup_error:
        raise Pair06V8CombatPriorityInvocationHold(
            "PAIR06_V8_COMBAT_PRIORITY_PRECLAIM_CLEANUP_FAILED"
        ) from cleanup_error


def execute_pair06_v8_combat_priority_baseline_game(
    *,
    expected_main_head: str,
    expected_invocation_source_sha256: str,
    execution_authorization_accepted: bool,
    policy_activation_authorization_accepted: bool,
    execution_confirm: str,
    policy_confirm: str,
) -> dict[str, Any]:
    """Execute one combat-priority pair-06 baseline attempt when authorized."""

    _require(
        base_invocation._hex(expected_main_head, 40),
        "PAIR06_V8_COMBAT_PRIORITY_EXPECTED_MAIN_REQUIRED",
    )
    _require(
        base_invocation._hex(expected_invocation_source_sha256, 64),
        "PAIR06_V8_COMBAT_PRIORITY_EXPECTED_SOURCE_REQUIRED",
    )
    _require(
        execution_authorization_accepted is True,
        "PAIR06_V8_COMBAT_PRIORITY_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    _require(
        policy_activation_authorization_accepted is True,
        "PAIR06_V8_COMBAT_PRIORITY_POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
    )
    _require(
        type(execution_confirm) is str
        and execution_confirm == EXECUTION_CONFIRM_TOKEN,
        "PAIR06_V8_COMBAT_PRIORITY_EXECUTION_CONFIRMATION_REQUIRED",
    )
    _require(
        type(policy_confirm) is str
        and policy_confirm == POLICY_CONFIRM_TOKEN,
        "PAIR06_V8_COMBAT_PRIORITY_POLICY_CONFIRMATION_REQUIRED",
    )

    _dependency_contracts()
    base_invocation._check_python()
    source_sha = _verify_self(expected_invocation_source_sha256)
    main = base_invocation._current_main(expected_main_head)
    _prepare_directories()
    _not_revoked()
    preflight = base_invocation._fresh_preflight()

    marker_path = CLAIMS_ROOT / MARKER_NAME
    result_path = CLAIMS_ROOT / RESULT_NAME
    closeout_path = CLAIMS_ROOT / CLOSEOUT_NAME

    for path, code in (
        (marker_path, "PAIR06_V8_COMBAT_PRIORITY_PRIOR_ATTEMPT_PRESENT"),
        (result_path, "PAIR06_V8_COMBAT_PRIORITY_PRIOR_RESULT_PRESENT"),
        (closeout_path, "PAIR06_V8_COMBAT_PRIORITY_PRIOR_CLOSEOUT_PRESENT"),
    ):
        _require(not path.exists(), code)

    backend = base_invocation.git_backend.Pair06V8BaselineGitBackend(
        confirm=base_invocation.git_backend.CONFIRM_TOKEN
    )
    materialization = None
    try:
        materialization = base_invocation._materialize(backend)

        base_invocation._current_main(expected_main_head)
        _verify_self(expected_invocation_source_sha256)
        _not_revoked()
        base_invocation._fresh_preflight()

        gpu_preclaim = base_invocation._fresh_preclaim_gpu_observation()
    except BaseException:
        if materialization is not None:
            _cleanup_preclaim(materialization, backend)
        raise

    marker_payload = {
        "schema": (
            "void.abaddon.generation2."
            "pair06-v8-combat-priority-baseline-game-attempt.v1"
        ),
        "record_kind": "attempt_consumed_not_execution_evidence",
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "expected_main_head": expected_main_head,
        "main_tree": main["tree"],
        "invocation_source_sha256": source_sha,
        "parent_wiring_review_source_sha256": (
            PARENT_WIRING_REVIEW_SOURCE_SHA256
        ),
        "base_preclaim_gpu_review_source_sha256": (
            BASE_PRECLAIM_GPU_REVIEW_SOURCE_SHA256
        ),
        "materialization_sha256": base_invocation._digest(materialization),
        "preclaim_gpu_observation_sha256": base_invocation._digest(
            gpu_preclaim["observation"]
        ),
        "preclaim_gpu_free_memory_bytes": (
            gpu_preclaim["observation"]["free_memory_bytes"]
        ),
        "preclaim_gpu_total_memory_bytes": (
            gpu_preclaim["observation"]["total_memory_bytes"]
        ),
        "preclaim_gpu_compute_process_count": len(
            gpu_preclaim["observation"]["compute_processes"]
        ),
        "fresh_preclaim_gpu_admitted": True,
        "maximum_attempts": 1,
        "automatic_retry": False,
        "pair06_combat_priority_execution_authorization_accepted": True,
        "pair06_combat_priority_policy_activation_accepted": True,
        "runtime_load_authorized": True,
        "model_inference_authorized": True,
        "game_execution_authorized": True,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
    }
    marker_sha256 = base_invocation._write_create_only(
        marker_path,
        marker_payload,
    )
    attempt_id = marker_sha256

    def authority_check(pair_slot: int, arm: str) -> bool:
        if pair_slot != PAIR_SLOT or arm != ARM:
            return False
        try:
            _not_revoked()
            if base_invocation._current_main(expected_main_head) != main:
                return False
            if _verify_self(expected_invocation_source_sha256) != source_sha:
                return False
            if base_invocation._file_sha256(marker_path) != marker_sha256:
                return False
            return True
        except Exception:
            return False

    _require(
        authority_check(PAIR_SLOT, ARM) is True,
        "PAIR06_V8_COMBAT_PRIORITY_REVOKED_AFTER_CLAIM",
    )

    receipt = (
        combat_parent
        .execute_pair06_v8_combat_priority_parent_supervisor_no_offload(
            attempt_id=attempt_id,
            attempt_claimed=True,
            runs_root=str(RUNS_ROOT),
            frozen_source_root=str(FROZEN_SOURCE_ROOT),
            exact_engine_root=str(EXACT_ENGINE_ROOT),
            policy_activation_authorized=True,
            execution_authorized=True,
            authority_check=authority_check,
        )
    )
    receipt = base_invocation._validate_supervisor_receipt(
        receipt,
        attempt_id=attempt_id,
    )

    result_payload = {
        "schema": (
            "void.abaddon.generation2."
            "pair06-v8-combat-priority-baseline-game-result-no-offload.v1"
        ),
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "main_head": expected_main_head,
        "main_tree": main["tree"],
        "invocation_source_sha256": source_sha,
        "attempt_marker_sha256": marker_sha256,
        "attempt_id": attempt_id,
        "materialization": deepcopy(materialization),
        "preflight": deepcopy(preflight),
        "fresh_preclaim_gpu": deepcopy(gpu_preclaim),
        "supervisor_receipt": deepcopy(receipt),
        "combat_priority_parent_wiring_used": True,
        "combat_priority_policy_activation_performed": True,
        "pair06_baseline_execution_performed": True,
        "automatic_retry": False,
        "candidate_execution_performed": False,
        "pair15_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "automatic_policy_promotion": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
    }
    result_sha256 = base_invocation._write_create_only(
        result_path,
        result_payload,
    )

    cleanup = base_invocation.materializer.cleanup_v2r13_frozen_worktrees(
        materialization,
        cleanup_authorized=True,
        path_exists=backend.path_exists,
        run_git=backend.run_git,
    )
    _require(
        cleanup.get("source_worktree_removed") is True
        and cleanup.get("engine_worktree_removed") is True
        and cleanup.get("removed_worktree_count") == 2,
        "PAIR06_V8_COMBAT_PRIORITY_WORKTREE_CLEANUP_HOLD",
    )

    closeout_payload = {
        "schema": (
            "void.abaddon.generation2."
            "pair06-v8-combat-priority-baseline-game-closeout-no-offload.v1"
        ),
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "attempt_id": attempt_id,
        "attempt_marker_sha256": marker_sha256,
        "result_file_sha256": result_sha256,
        "worktree_cleanup": deepcopy(cleanup),
        "worktree_cleanup_completed": True,
        "runs_preserved": True,
        "automatic_retry": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
    }
    closeout_sha256 = base_invocation._write_create_only(
        closeout_path,
        closeout_payload,
    )

    return {
        **deepcopy(result_payload),
        "result_file": str(result_path),
        "result_file_sha256": result_sha256,
        "closeout_file": str(closeout_path),
        "closeout_file_sha256": closeout_sha256,
        "attempt_marker_file": str(marker_path),
        "attempt_marker_sha256": marker_sha256,
    }


def pair06_v8_combat_priority_baseline_attempt_invocation_contract() -> dict[str, Any]:
    dependencies = _dependency_contracts()
    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v8_combat_priority_baseline_attempt_invocation_implemented": True,
        "pair06_v8_combat_priority_baseline_attempt_invocation_reviewed": False,
        "parent_wiring_review_main_head": PARENT_WIRING_REVIEW_MAIN_HEAD,
        "parent_wiring_review_git_blob": PARENT_WIRING_REVIEW_GIT_BLOB,
        "parent_wiring_review_source_sha256": (
            PARENT_WIRING_REVIEW_SOURCE_SHA256
        ),
        "base_preclaim_gpu_review_git_blob": (
            BASE_PRECLAIM_GPU_REVIEW_GIT_BLOB
        ),
        "base_preclaim_gpu_review_source_sha256": (
            BASE_PRECLAIM_GPU_REVIEW_SOURCE_SHA256
        ),
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "exact_v8_python_required": True,
        "exact_current_main_required": True,
        "exact_invocation_source_sha256_required": True,
        "fresh_v8_environment_and_assets_required": True,
        "reviewed_base_preclaim_gpu_helpers_reused": True,
        "reviewed_worktree_materializer_reused": True,
        "preclaim_worktree_materialization_implemented": True,
        "preclaim_materialization_cleanup_on_hold_implemented": True,
        "fresh_preclaim_gpu_observation_implemented": True,
        "fresh_preclaim_gpu_admission_required": True,
        "fresh_preclaim_gpu_observation_precedes_attempt_marker": True,
        "zero_foreign_cuda0_compute_processes_required": True,
        "minimum_cuda0_free_memory_fraction_numerator": 9,
        "minimum_cuda0_free_memory_fraction_denominator": 10,
        "durable_create_only_attempt_marker_implemented": True,
        "combat_priority_marker_namespace_distinct_from_legacy": (
            MARKER_NAME != base_invocation.MARKER_NAME
        ),
        "combat_priority_result_namespace_distinct_from_legacy": (
            RESULT_NAME != base_invocation.RESULT_NAME
        ),
        "combat_priority_closeout_namespace_distinct_from_legacy": (
            CLOSEOUT_NAME != base_invocation.CLOSEOUT_NAME
        ),
        "combat_priority_runs_root_distinct_from_legacy": (
            RUNS_ROOT != Path(base_invocation.RUNS_ROOT)
        ),
        "marker_deletion_api_implemented": False,
        "reset_api_implemented": False,
        "resume_api_implemented": False,
        "attempt_marker_precedes_model_load_and_child_spawn": True,
        "marker_sha256_is_attempt_id": True,
        "authority_rechecked_after_claim": True,
        "authority_rechecked_before_each_inference_by_supervisor": True,
        "reviewed_combat_priority_parent_wiring_used": True,
        "no_offload_parent_receipt_schema_required": True,
        "inference_safe_placement_receipt_required": True,
        "durable_execution_result_before_cleanup_implemented": True,
        "success_only_worktree_cleanup_implemented": True,
        "durable_cleanup_closeout_implemented": True,
        "runs_preserved_after_success": True,
        "maximum_attempts": 1,
        "automatic_retry": False,
        "explicit_execution_authorization_boolean_required": True,
        "explicit_policy_activation_authorization_boolean_required": True,
        "explicit_execution_confirmation_token_required": True,
        "explicit_policy_confirmation_token_required": True,
        "execution_and_policy_confirmation_tokens_distinct": (
            EXECUTION_CONFIRM_TOKEN != POLICY_CONFIRM_TOKEN
        ),
        "execution_authorization_accepted": False,
        "policy_activation_authorization_accepted": False,
        "attempt_consumed": False,
        "attempt_marker_creation_authorized": False,
        "runtime_load_authorized": False,
        "model_inference_authorized": False,
        "game_execution_authorized": False,
        "game_execution_performed": False,
        "candidate_execution_authorized": False,
        "pair15_execution_authorized": False,
        "training_authorized": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "host_io_performed_by_contract_inspection": False,
        "dependencies": dependencies,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CombatPriorityInvocationHold(NEXT_GATE)
