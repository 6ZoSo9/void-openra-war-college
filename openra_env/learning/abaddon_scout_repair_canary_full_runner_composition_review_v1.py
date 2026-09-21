"""Source-only full-runner composition review for the scout-repair canary.

This review binds the exact frozen historical runner plus the already-reviewed
deterministic canary opponent adapter and canary runner requirements. It performs
no import or execution of those sources and no host I/O.

The purpose is deliberately negative and precise: prove that the frozen runner
cannot be used unchanged for the canary because it still starts/cleans the model
service and labels controller rows as training candidates, while identifying the
exact source obligations for a derived runner implementation.

Passing this review grants no game, model, runtime, training, deployment, VOID,
wallet, or funds authority.
"""

from __future__ import annotations

import ast
import hashlib
from typing import Any


SCHEMA = "void.abaddon.scout-repair-canary-full-runner-composition-review.v1"

HISTORICAL_RUNNER_PATH = (
    "fixtures/learning/scout-missions-v1/warm_start_runner_v1_4.py"
)
HISTORICAL_RUNNER_GIT_BLOB = "132a5b2df3c3dbc82df7c0ebc6d457e5b77ffb51"
HISTORICAL_RUNNER_SHA256 = (
    "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901"
)

CANARY_ADAPTER_PATH = (
    "openra_env/learning/abaddon_scout_repair_canary_runner_adapter_v1.py"
)
CANARY_ADAPTER_GIT_BLOB = "509f7651d36e83a182b7a485c88029dee537f633"

CANARY_REQUIREMENTS_PATH = (
    "openra_env/learning/abaddon_scout_repair_canary_runner_requirements_v1.py"
)
CANARY_REQUIREMENTS_GIT_BLOB = "b14175483877b4c35afc44d6c0f720ce07e68506"

NEXT_GATE = "SCOUT_REPAIR_CANARY_DERIVED_RUNNER_IMPLEMENTATION_REQUIRED"

HISTORICAL_BLOCKERS = (
    "historical_runner_starts_ollama_service",
    "historical_runner_cleanup_invokes_model_service_cleanup",
    "historical_runner_uses_model_backed_apollyon_decision",
    "historical_controller_rows_are_training_candidates",
    "historical_summary_marks_controller_rows_training_candidate",
    "historical_run_header_marks_agent_training_rows_begin_here",
    "historical_stdout_claims_model_runtime_started",
)

DERIVED_RUNNER_OBLIGATIONS = (
    "preserve_exact_warm_start_and_host_validation_semantics",
    "replace_apollyon_decision_with_reviewed_deterministic_canary_adapter",
    "never_dereference_model_helper_for_decision",
    "do_not_start_ollama_or_any_model_service",
    "do_not_invoke_model_inference",
    "do_not_invoke_model_service_cleanup_when_no_service_was_started",
    "emit_no_false_model_runtime_started_claim",
    "mark_all_canary_controller_rows_training_candidate_false",
    "mark_canary_summary_controller_rows_training_candidate_false",
    "mark_agent_training_rows_begin_here_false_or_omit_the_field",
    "log_exact_deterministic_opponent_source_identity",
    "retain_one_host_validation_per_controller_round",
    "retain_zero_automatic_retry",
    "retain_same_tick_joint_commit_semantics",
    "retain_source_checkout_clean_post_run_requirement",
    "require_independent_post_run_runtime_and_container_dormancy_evidence",
    "create_no_execution_authority_in_source_review",
)


class ScoutRepairCanaryFullRunnerReviewHold(ValueError):
    """Exact source binding or full-runner review requirement failed."""


def _require(value: bool, reason: str) -> None:
    if not value:
        raise ScoutRepairCanaryFullRunnerReviewHold(reason)


def _git_blob_sha1(raw: bytes) -> str:
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _decode_python(raw: bytes, label: str) -> str:
    _require(type(raw) is bytes and len(raw) > 0, f"{label}_exact_bytes_required")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ScoutRepairCanaryFullRunnerReviewHold(
            f"{label}_utf8_required"
        ) from exc


def _dotted(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def _call_count(tree: ast.AST, dotted_name: str) -> int:
    return sum(
        1
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and _dotted(node.func) == dotted_name
    )


def _dict_literal_bool_count(
    tree: ast.AST,
    *,
    key_name: str,
    value: bool,
) -> int:
    count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for key, item in zip(node.keys, node.values):
            if (
                isinstance(key, ast.Constant)
                and key.value == key_name
                and isinstance(item, ast.Constant)
                and item.value is value
            ):
                count += 1
    return count


def _string_literal_count(tree: ast.AST, value: str) -> int:
    return sum(
        1
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and node.value == value
    )


def review_full_runner_composition(
    *,
    historical_runner_bytes: bytes,
    canary_adapter_bytes: bytes,
    canary_requirements_bytes: bytes,
) -> dict[str, Any]:
    """Review exact source bytes without importing or executing them."""

    runner_text = _decode_python(historical_runner_bytes, "historical_runner")
    adapter_text = _decode_python(canary_adapter_bytes, "canary_adapter")
    requirements_text = _decode_python(
        canary_requirements_bytes,
        "canary_requirements",
    )

    _require(
        _git_blob_sha1(historical_runner_bytes) == HISTORICAL_RUNNER_GIT_BLOB,
        "historical_runner_git_blob_drift",
    )
    _require(
        _sha256(historical_runner_bytes) == HISTORICAL_RUNNER_SHA256,
        "historical_runner_sha256_drift",
    )
    _require(
        _git_blob_sha1(canary_adapter_bytes) == CANARY_ADAPTER_GIT_BLOB,
        "canary_adapter_git_blob_drift",
    )
    _require(
        _git_blob_sha1(canary_requirements_bytes)
        == CANARY_REQUIREMENTS_GIT_BLOB,
        "canary_requirements_git_blob_drift",
    )

    try:
        runner_tree = ast.parse(runner_text, filename=HISTORICAL_RUNNER_PATH)
        adapter_tree = ast.parse(adapter_text, filename=CANARY_ADAPTER_PATH)
        requirements_tree = ast.parse(
            requirements_text,
            filename=CANARY_REQUIREMENTS_PATH,
        )
    except SyntaxError as exc:
        raise ScoutRepairCanaryFullRunnerReviewHold(
            "reviewed_python_source_invalid"
        ) from exc

    start_ollama_calls = _call_count(runner_tree, "helper.start_ollama")
    cleanup_calls = _call_count(runner_tree, "helper.cleanup")
    historical_model_decision_calls = _call_count(
        runner_tree,
        "apollyon_decision_typed",
    )
    controller_training_true = _dict_literal_bool_count(
        runner_tree,
        key_name="training_candidate",
        value=True,
    )
    summary_training_true = _dict_literal_bool_count(
        runner_tree,
        key_name="controller_rows_training_candidate",
        value=True,
    )
    header_training_begin_true = _dict_literal_bool_count(
        runner_tree,
        key_name="agent_training_rows_begin_here",
        value=True,
    )
    runtime_started_claims = _string_literal_count(
        runner_tree,
        "apollyon_runtime_started_at_handoff=true",
    )

    _require(start_ollama_calls == 1, "historical_start_ollama_shape_drift")
    _require(cleanup_calls == 1, "historical_cleanup_shape_drift")
    _require(
        historical_model_decision_calls == 1,
        "historical_apollyon_decision_call_shape_drift",
    )
    _require(
        controller_training_true == 2,
        "historical_controller_training_row_shape_drift",
    )
    _require(
        summary_training_true == 1,
        "historical_summary_training_label_shape_drift",
    )
    _require(
        header_training_begin_true == 1,
        "historical_training_begin_shape_drift",
    )
    _require(
        runtime_started_claims == 1,
        "historical_runtime_started_claim_shape_drift",
    )

    _require(
        "class DeterministicCanaryOpponentAdapter" in adapter_text,
        "canary_adapter_class_missing",
    )
    _require(
        "helper_dereferenced" in adapter_text
        and "model_service_start_implemented" in adapter_text
        and "model_inference_implemented" in adapter_text
        and "adapter_review_rows_nontraining" in adapter_text,
        "canary_adapter_review_contract_drift",
    )
    _require(
        _call_count(adapter_tree, "helper.ollama_tool_call") == 0,
        "canary_adapter_model_helper_call_forbidden",
    )

    _require(
        "model_service_start_forbidden" in requirements_text
        and "model_inference_forbidden" in requirements_text
        and "controller_rows_training_candidate" in requirements_text
        and "independent_runtime_dormancy_observation_required"
        in requirements_text,
        "canary_requirements_contract_drift",
    )
    _require(
        _call_count(requirements_tree, "subprocess.run") == 0,
        "canary_requirements_host_execution_forbidden",
    )

    return {
        "schema": SCHEMA,
        "source_bindings": {
            HISTORICAL_RUNNER_PATH: {
                "git_blob": HISTORICAL_RUNNER_GIT_BLOB,
                "sha256": HISTORICAL_RUNNER_SHA256,
            },
            CANARY_ADAPTER_PATH: {
                "git_blob": CANARY_ADAPTER_GIT_BLOB,
            },
            CANARY_REQUIREMENTS_PATH: {
                "git_blob": CANARY_REQUIREMENTS_GIT_BLOB,
            },
        },
        "historical_runner_observations": {
            "start_ollama_call_count": start_ollama_calls,
            "cleanup_call_count": cleanup_calls,
            "model_backed_apollyon_decision_call_count": (
                historical_model_decision_calls
            ),
            "controller_training_candidate_true_row_count": (
                controller_training_true
            ),
            "summary_controller_training_candidate_true_count": (
                summary_training_true
            ),
            "run_header_agent_training_rows_begin_here_true_count": (
                header_training_begin_true
            ),
            "model_runtime_started_stdout_claim_count": runtime_started_claims,
        },
        "historical_runner_admissible_without_derivation": False,
        "historical_blockers": HISTORICAL_BLOCKERS,
        "derived_runner_obligations": DERIVED_RUNNER_OBLIGATIONS,
        "derived_runner_implementation_required": True,
        "source_review_performed": True,
        "source_import_or_execution_performed": False,
        "host_observation_performed": False,
        "game_execution_performed": False,
        "model_service_action_performed": False,
        "model_inference_performed": False,
        "attempt_consumed": False,
        "training_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "execution_authorized": False,
        "next_gate": NEXT_GATE,
    }


def authorize_install_or_execute(*args: Any, **kwargs: Any) -> None:
    raise ScoutRepairCanaryFullRunnerReviewHold(NEXT_GATE)
