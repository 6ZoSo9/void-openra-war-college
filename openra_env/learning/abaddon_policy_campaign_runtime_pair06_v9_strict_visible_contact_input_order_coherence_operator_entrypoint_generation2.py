"""One-shot operator entrypoint for Pair-06 V9 input-order coherence.

This source composes the reviewed receipt-bound/no-offload/fresh-preclaim-GPU
baseline helpers with the reviewed input-order-coherent V9 parent-supervisor
wiring.

It uses a fresh create-only order-coherence marker/result/closeout namespace and
fresh runs root, distinct from both V8 and the consumed historical V9 lane.

Operational execution remains impossible without all of:
* exact current main;
* exact operator-source SHA-256;
* explicit execution authorization;
* explicit V9 strict-contact policy activation authorization;
* explicit input-order-coherence activation authorization;
* three exact, distinct confirmation tokens;
* fresh preclaim CUDA:0 admission;
* a fresh create-only order-coherence attempt marker.

Maximum attempts is one. Automatic retry is forbidden. Import and contract
inspection perform no host I/O or execution. This source itself grants no
authorization and does not treat general work authorization as game execution
authorization.
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
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_execution_success_closeout_source_binding_review_generation2
    as prior_success_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_parent_supervisor_wiring_generation2
    as order_parent,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_parent_supervisor_wiring_source_binding_review_generation2
    as order_parent_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_proto_game_child_entrypoint_generation2
    as order_child_entry,
)


SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-baseline-game-attempt-invocation-"
    "receipt-bound-no-offload-preclaim-gpu.v1"
)
CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-strict-visible-contact-input-order-coherence-operator-entrypoint-contract.v1"
)

PAIR_SLOT = 6
ARM = "baseline"
HELD_OUT = False
POLICY_ID = "pair06-v9-strict-visible-contact-envelope-v1"

SOURCE_ROOT = Path(base_invocation.SOURCE_ROOT)
ARM_ROOT = Path(base_invocation.ARM_ROOT)
CLAIMS_ROOT = Path(base_invocation.CLAIMS_ROOT)
FROZEN_SOURCE_ROOT = Path(base_invocation.FROZEN_SOURCE_ROOT)
EXACT_ENGINE_ROOT = Path(base_invocation.EXACT_ENGINE_ROOT)
RUNS_ROOT = ARM_ROOT / "runs-v9-strict-visible-contact-input-order-coherence-v1"

MARKER_NAME = (
    "pair06-v9-strict-visible-contact-input-order-coherence-baseline-game-attempt-v1.json"
)
RESULT_NAME = (
    "pair06-v9-strict-visible-contact-input-order-coherence-baseline-game-result-v1.json"
)
CLOSEOUT_NAME = (
    "pair06-v9-strict-visible-contact-input-order-coherence-baseline-game-closeout-v1.json"
)
REVOCATION_NAME = "REVOKE_PAIR06_V9_INPUT_ORDER_INPUT_ORDER_COHERENCE_GAME"

SELF_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_"
    "operator_entrypoint_generation2.py"
)

V8_PYTHON = Path(base_invocation.V8_PYTHON)

EXECUTION_CONFIRM_TOKEN = (
    "VOID_PAIR06_V9_INPUT_ORDER_INPUT_ORDER_COHERENCE_RECEIPT_BOUND_NO_OFFLOAD_"
    "PRECLAIM_GPU_EXECUTE_ONCE"
)
POLICY_CONFIRM_TOKEN = order_child_entry.POLICY_CONFIRM_TOKEN
ORDER_CONFIRM_TOKEN = order_child_entry.ORDER_CONFIRM_TOKEN

ORDER_PARENT_REVIEW_GIT_BLOB = "34ef81214dc8d56073698ac531e84f23d92b6b6c"
BASE_PRECLAIM_GPU_REVIEW_GIT_BLOB = (
    "77dbac309565beb804ac1c2936799574efe5de82"
)
PRIOR_V8_SUCCESS_REVIEW_GIT_BLOB = (
    "149b04e687d16d797603701089846804a384b7ae"
)

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_INPUT_ORDER_COHERENCE_"
    "OPERATOR_ENTRYPOINT_SOURCE_BINDING_REVIEW_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_strict_visible_contact_input_order_coherence_"
    "operator_entrypoint_review"
)


class Pair06V9InputOrderCoherenceOperatorHold(RuntimeError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9InputOrderCoherenceOperatorHold(message)


def _dependency_contracts() -> dict[str, Any]:
    parent = (
        order_parent_review
        .pair06_v9_input_order_coherence_parent_wiring_review_contract()
    )
    base = (
        base_invocation_review
        .pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_preclaim_gpu_review_contract()
    )
    prior = (
        prior_success_review
        .pair06_v8_combat_priority_coherent_v2_success_review_contract()
    )

    _require(
        parent.get(
            "pair06_v9_input_order_coherence_parent_wiring_reviewed"
        )
        is True,
        "PAIR06_V9_INPUT_ORDER_PARENT_WIRING_NOT_REVIEWED",
    )
    _require(
        parent.get("durable_attempt_claim_prerequisite_preserved") is True
        and parent.get("no_offload_cuda0_parent_path_preserved") is True,
        "PAIR06_V9_INPUT_ORDER_PARENT_RUNTIME_BOUNDARY_DRIFT",
    )
    _require(
        parent.get("execution_confirmation_token_preserved") is True
        and parent.get("historical_v9_policy_activation_token_preserved") is True
        and parent.get("distinct_order_coherence_activation_token_preserved")
        is True,
        "PAIR06_V9_INPUT_ORDER_PARENT_CONFIRMATION_BOUNDARY_DRIFT",
    )
    _require(
        parent.get("execution_request_created") is False
        and parent.get("attempt_claim_created") is False
        and parent.get("attempt_created") is False
        and parent.get("runtime_execution_authorized") is False,
        "PAIR06_V9_INPUT_ORDER_PARENT_AUTHORITY_DRIFT",
    )
    _require(
        parent.get("next_gate")
        == (
            "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
            "OPERATOR_ENTRYPOINT_WIRING_REQUIRED"
        ),
        "PAIR06_V9_INPUT_ORDER_OPERATOR_FRONTIER_DRIFT",
    )

    _require(
        base.get(
            "pair06_v8_baseline_attempt_invocation_receipt_bound_no_offload_"
            "preclaim_gpu_reviewed"
        )
        is True,
        "PAIR06_V9_INPUT_ORDER_BASE_PRECLAIM_GPU_INVOCATION_NOT_REVIEWED",
    )
    _require(
        base.get("maximum_attempts") == 1
        and base.get("maximum_automatic_retries") == 0,
        "PAIR06_V9_INPUT_ORDER_BASE_PRECLAIM_ATTEMPT_BOUND_DRIFT",
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
        "PAIR06_V9_INPUT_ORDER_BASE_PRECLAIM_GPU_POLICY_DRIFT",
    )
    _require(
        base.get("historical_gpu_observation_reusable") is False
        and base.get("spent_receipt_bound_request_reusable") is False
        and base.get("spent_oom_attempt_reusable") is False,
        "PAIR06_V9_INPUT_ORDER_BASE_PRECLAIM_REUSE_DRIFT",
    )
    _require(
        base.get("attempt_marker_creation_authorized") is False
        and base.get("game_execution_authorized") is False,
        "PAIR06_V9_INPUT_ORDER_BASE_PRECLAIM_AUTHORITY_DRIFT",
    )

    _require(
        prior.get(
            "pair06_v8_combat_priority_coherent_v2_success_reviewed"
        )
        is True,
        "PAIR06_V9_INPUT_ORDER_PRIOR_SUCCESS_REVIEW_MISSING",
    )
    _require(
        prior.get("attempt_consumed") is True
        and prior.get("attempt_reusable") is False
        and prior.get("authorization_reusable") is False
        and prior.get("automatic_retry") is False,
        "PAIR06_V9_INPUT_ORDER_PRIOR_SUCCESS_REUSE_DRIFT",
    )
    _require(
        prior.get("new_execution_request_opened") is False
        and prior.get("lineage_closed") is True,
        "PAIR06_V9_INPUT_ORDER_PRIOR_SUCCESS_LINEAGE_DRIFT",
    )

    return {
        "v9_parent_wiring_review": deepcopy(parent),
        "base_preclaim_gpu_invocation_review": deepcopy(base),
        "prior_v8_v2_success_review": deepcopy(prior),
    }


def _verify_self(expected_source_sha256: str) -> str:
    source = SOURCE_ROOT / SELF_PATH
    _require(
        Path(__file__) == source,
        "PAIR06_V9_INPUT_ORDER_OPERATOR_ORIGIN_HOLD",
    )
    actual = hashlib.sha256(source.read_bytes()).hexdigest()
    _require(
        actual == expected_source_sha256,
        "PAIR06_V9_INPUT_ORDER_OPERATOR_SOURCE_DRIFT",
    )
    return actual


def _not_revoked() -> None:
    if (CLAIMS_ROOT / REVOCATION_NAME).exists():
        raise Pair06V9InputOrderCoherenceOperatorHold(
            "PAIR06_V9_INPUT_ORDER_OPERATOR_REVOKED"
        )
    if (CLAIMS_ROOT / base_invocation.REVOCATION_NAME).exists():
        raise Pair06V9InputOrderCoherenceOperatorHold(
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
        raise Pair06V9InputOrderCoherenceOperatorHold(
            "PAIR06_V9_INPUT_ORDER_PRECLAIM_CLEANUP_FAILED"
        ) from cleanup_error


def execute_pair06_v9_input_order_coherence_baseline_game(
    *,
    expected_main_head: str,
    expected_operator_source_sha256: str,
    execution_authorization_accepted: bool,
    policy_activation_authorization_accepted: bool,
    order_coherence_activation_authorization_accepted: bool,
    execution_confirm: str,
    policy_confirm: str,
    order_confirm: str,
) -> dict[str, Any]:
    """Execute one V9 pair-06 baseline attempt when separately authorized."""

    _require(
        base_invocation._hex(expected_main_head, 40),
        "PAIR06_V9_INPUT_ORDER_EXPECTED_MAIN_REQUIRED",
    )
    _require(
        base_invocation._hex(expected_operator_source_sha256, 64),
        "PAIR06_V9_INPUT_ORDER_EXPECTED_SOURCE_REQUIRED",
    )
    _require(
        execution_authorization_accepted is True,
        "PAIR06_V9_INPUT_ORDER_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    _require(
        policy_activation_authorization_accepted is True,
        "PAIR06_V9_INPUT_ORDER_POLICY_ACTIVATION_AUTHORIZATION_REQUIRED",
    )
    _require(
        order_coherence_activation_authorization_accepted is True,
        "PAIR06_V9_INPUT_ORDER_COHERENCE_ACTIVATION_AUTHORIZATION_REQUIRED",
    )
    _require(
        type(execution_confirm) is str
        and execution_confirm == EXECUTION_CONFIRM_TOKEN,
        "PAIR06_V9_INPUT_ORDER_EXECUTION_CONFIRMATION_REQUIRED",
    )
    _require(
        type(policy_confirm) is str
        and policy_confirm == POLICY_CONFIRM_TOKEN,
        "PAIR06_V9_INPUT_ORDER_POLICY_CONFIRMATION_REQUIRED",
    )
    _require(
        type(order_confirm) is str
        and order_confirm == ORDER_CONFIRM_TOKEN,
        "PAIR06_V9_INPUT_ORDER_COHERENCE_CONFIRMATION_REQUIRED",
    )

    dependencies = _dependency_contracts()
    base_invocation._check_python()
    source_sha = _verify_self(expected_operator_source_sha256)
    main = base_invocation._current_main(expected_main_head)
    _prepare_directories()
    _not_revoked()
    preflight = base_invocation._fresh_preflight()

    marker_path = CLAIMS_ROOT / MARKER_NAME
    result_path = CLAIMS_ROOT / RESULT_NAME
    closeout_path = CLAIMS_ROOT / CLOSEOUT_NAME

    for path, code in (
        (marker_path, "PAIR06_V9_INPUT_ORDER_PRIOR_ATTEMPT_PRESENT"),
        (result_path, "PAIR06_V9_INPUT_ORDER_PRIOR_RESULT_PRESENT"),
        (closeout_path, "PAIR06_V9_INPUT_ORDER_PRIOR_CLOSEOUT_PRESENT"),
    ):
        _require(not path.exists(), code)

    backend = base_invocation.git_backend.Pair06V8BaselineGitBackend(
        confirm=base_invocation.git_backend.CONFIRM_TOKEN
    )
    materialization = None
    try:
        materialization = base_invocation._materialize(backend)

        base_invocation._current_main(expected_main_head)
        _verify_self(expected_operator_source_sha256)
        _not_revoked()
        base_invocation._fresh_preflight()

        gpu_preclaim = base_invocation._fresh_preclaim_gpu_observation()
    except BaseException:
        if materialization is not None:
            _cleanup_preclaim(materialization, backend)
        raise

    prior = dependencies["prior_v8_v2_success_review"]
    marker_payload = {
        "schema": (
            "void.abaddon.generation2."
            "pair06-v9-strict-visible-contact-input-order-coherence-baseline-game-attempt.v1"
        ),
        "record_kind": "attempt_consumed_not_execution_evidence",
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "policy_id": POLICY_ID,
        "expected_main_head": expected_main_head,
        "main_tree": main["tree"],
        "operator_source_sha256": source_sha,
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
        "pair06_v9_execution_authorization_accepted": True,
        "pair06_v9_policy_activation_accepted": True,
        "pair06_v9_input_order_coherence_activation_accepted": True,
        "prior_v8_v2_run_id": prior["run_id"],
        "prior_v8_v2_attempt_marker_sha256": prior["attempt_marker_sha256"],
        "prior_v8_v2_attempt_reusable": False,
        "prior_v8_v2_authorization_reusable": False,
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
            if _verify_self(expected_operator_source_sha256) != source_sha:
                return False
            if base_invocation._file_sha256(marker_path) != marker_sha256:
                return False
            return True
        except Exception:
            return False

    _require(
        authority_check(PAIR_SLOT, ARM) is True,
        "PAIR06_V9_INPUT_ORDER_REVOKED_AFTER_CLAIM",
    )

    receipt = (
        order_parent
        .execute_pair06_v9_input_order_coherence_parent_supervisor_no_offload(
            attempt_id=attempt_id,
            attempt_claimed=True,
            runs_root=str(RUNS_ROOT),
            frozen_source_root=str(FROZEN_SOURCE_ROOT),
            exact_engine_root=str(EXACT_ENGINE_ROOT),
            policy_activation_authorized=True,
            order_coherence_activation_authorized=True,
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
            "pair06-v9-strict-visible-contact-input-order-coherence-baseline-game-result-"
            "no-offload.v1"
        ),
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "policy_id": POLICY_ID,
        "main_head": expected_main_head,
        "main_tree": main["tree"],
        "operator_source_sha256": source_sha,
        "attempt_marker_sha256": marker_sha256,
        "attempt_id": attempt_id,
        "materialization": deepcopy(materialization),
        "preflight": deepcopy(preflight),
        "fresh_preclaim_gpu": deepcopy(gpu_preclaim),
        "supervisor_receipt": deepcopy(receipt),
        "v9_parent_wiring_used": True,
        "v9_input_order_coherence_parent_wiring_used": True,
        "v9_policy_activation_performed": True,
        "v9_input_order_coherence_activation_performed": True,
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
        "PAIR06_V9_INPUT_ORDER_WORKTREE_CLEANUP_HOLD",
    )

    closeout_payload = {
        "schema": (
            "void.abaddon.generation2."
            "pair06-v9-strict-visible-contact-input-order-coherence-baseline-game-closeout-"
            "no-offload.v1"
        ),
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "policy_id": POLICY_ID,
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


def pair06_v9_input_order_coherence_operator_contract() -> dict[str, Any]:
    dependencies = _dependency_contracts()
    prior = dependencies["prior_v8_v2_success_review"]

    return {
        "schema": CONTRACT_SCHEMA,
        "pair06_v9_input_order_coherence_operator_entrypoint_implemented": True,
        "pair06_v9_input_order_coherence_operator_entrypoint_reviewed": False,
        "order_parent_review_git_blob": ORDER_PARENT_REVIEW_GIT_BLOB,
        "base_preclaim_gpu_review_git_blob": BASE_PRECLAIM_GPU_REVIEW_GIT_BLOB,
        "prior_v8_success_review_git_blob": PRIOR_V8_SUCCESS_REVIEW_GIT_BLOB,
        "pair_slot": PAIR_SLOT,
        "arm": ARM,
        "held_out": HELD_OUT,
        "policy_id": POLICY_ID,
        "exact_v8_python_required": True,
        "exact_current_main_required": True,
        "exact_operator_source_sha256_required": True,
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
        "marker_deletion_api_implemented": False,
        "reset_api_implemented": False,
        "resume_api_implemented": False,
        "attempt_marker_precedes_model_load_and_child_spawn": True,
        "marker_sha256_is_attempt_id": True,
        "authority_rechecked_after_claim": True,
        "authority_rechecked_before_each_inference_by_parent": True,
        "no_offload_parent_receipt_schema_required": True,
        "inference_safe_placement_receipt_required": True,
        "durable_execution_result_before_cleanup_implemented": True,
        "success_only_worktree_cleanup_implemented": True,
        "durable_cleanup_closeout_implemented": True,
        "runs_preserved_after_success": True,
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "v9_evidence_namespace_distinct_from_v8": True,
        "order_evidence_namespace_distinct_from_historical_v9": True,
        "order_runs_root": str(RUNS_ROOT),
        "order_marker_name": MARKER_NAME,
        "order_result_name": RESULT_NAME,
        "order_closeout_name": CLOSEOUT_NAME,
        "prior_v8_v2_run_id": prior["run_id"],
        "prior_v8_v2_attempt_marker_sha256": prior["attempt_marker_sha256"],
        "prior_v8_v2_attempt_reusable": False,
        "prior_v8_v2_authorization_reusable": False,
        "explicit_execution_authorization_boolean_required": True,
        "explicit_policy_activation_authorization_boolean_required": True,
        "explicit_order_coherence_activation_authorization_boolean_required": True,
        "explicit_execution_confirmation_token_required": True,
        "explicit_policy_confirmation_token_required": True,
        "explicit_order_coherence_confirmation_token_required": True,
        "all_confirmation_tokens_distinct": (
            len({EXECUTION_CONFIRM_TOKEN, POLICY_CONFIRM_TOKEN, ORDER_CONFIRM_TOKEN}) == 3
        ),
        "execution_authorization_accepted": False,
        "policy_activation_authorization_accepted": False,
        "order_coherence_activation_authorization_accepted": False,
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
        "scheduler_mutation_authorized": False,
        "host_io_performed_by_contract_inspection": False,
        "dependencies": dependencies,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9InputOrderCoherenceOperatorHold(NEXT_GATE)
