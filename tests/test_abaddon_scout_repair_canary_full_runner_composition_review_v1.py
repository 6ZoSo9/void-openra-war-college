from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_scout_repair_canary_full_runner_composition_review_v1 as review,
)


REPO = Path(__file__).resolve().parents[1]
RUNNER = REPO / review.HISTORICAL_RUNNER_PATH
ADAPTER = REPO / review.CANARY_ADAPTER_PATH
REQUIREMENTS = REPO / review.CANARY_REQUIREMENTS_PATH
REVIEW_SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_scout_repair_canary_full_runner_composition_review_v1.py"
)


def _git_blob(raw: bytes) -> str:
    return hashlib.sha1(
        f"blob {len(raw)}\0".encode("ascii") + raw
    ).hexdigest()


def _review() -> dict:
    return review.review_full_runner_composition(
        historical_runner_bytes=RUNNER.read_bytes(),
        canary_adapter_bytes=ADAPTER.read_bytes(),
        canary_requirements_bytes=REQUIREMENTS.read_bytes(),
    )


def test_exact_source_bindings_match_checkout() -> None:
    assert _git_blob(RUNNER.read_bytes()) == review.HISTORICAL_RUNNER_GIT_BLOB
    assert (
        hashlib.sha256(RUNNER.read_bytes()).hexdigest()
        == review.HISTORICAL_RUNNER_SHA256
    )
    assert _git_blob(ADAPTER.read_bytes()) == review.CANARY_ADAPTER_GIT_BLOB
    assert (
        _git_blob(REQUIREMENTS.read_bytes())
        == review.CANARY_REQUIREMENTS_GIT_BLOB
    )


def test_historical_runner_is_explicitly_not_admissible_unchanged() -> None:
    out = _review()
    assert out["historical_runner_admissible_without_derivation"] is False
    assert out["derived_runner_implementation_required"] is True
    assert out["historical_blockers"] == review.HISTORICAL_BLOCKERS
    assert out["derived_runner_obligations"] == review.DERIVED_RUNNER_OBLIGATIONS
    assert out["next_gate"] == (
        "SCOUT_REPAIR_CANARY_DERIVED_RUNNER_IMPLEMENTATION_REQUIRED"
    )


def test_historical_incompatibility_counts_are_exact() -> None:
    obs = _review()["historical_runner_observations"]
    assert obs == {
        "start_ollama_call_count": 1,
        "cleanup_call_count": 1,
        "model_backed_apollyon_decision_call_count": 1,
        "controller_training_candidate_true_row_count": 2,
        "summary_controller_training_candidate_true_count": 1,
        "run_header_agent_training_rows_begin_here_true_count": 1,
        "model_runtime_started_stdout_claim_count": 1,
    }


def test_review_grants_no_operational_authority() -> None:
    out = _review()
    for field in (
        "source_import_or_execution_performed",
        "host_observation_performed",
        "game_execution_performed",
        "model_service_action_performed",
        "model_inference_performed",
        "attempt_consumed",
        "training_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "execution_authorized",
    ):
        assert out[field] is False
    assert out["source_review_performed"] is True


def test_model_service_suppression_and_nontraining_are_required() -> None:
    obligations = set(_review()["derived_runner_obligations"])
    assert "do_not_start_ollama_or_any_model_service" in obligations
    assert "do_not_invoke_model_inference" in obligations
    assert (
        "mark_all_canary_controller_rows_training_candidate_false"
        in obligations
    )
    assert (
        "mark_canary_summary_controller_rows_training_candidate_false"
        in obligations
    )
    assert (
        "require_independent_post_run_runtime_and_container_dormancy_evidence"
        in obligations
    )


def test_runner_byte_drift_fails_closed_before_semantic_reinterpretation() -> None:
    raw = RUNNER.read_bytes()
    mutated = raw.replace(
        b"helper.start_ollama()",
        b"helper.start_ollama( )",
        1,
    )
    assert mutated != raw
    with pytest.raises(
        review.ScoutRepairCanaryFullRunnerReviewHold,
        match="historical_runner_git_blob_drift",
    ):
        review.review_full_runner_composition(
            historical_runner_bytes=mutated,
            canary_adapter_bytes=ADAPTER.read_bytes(),
            canary_requirements_bytes=REQUIREMENTS.read_bytes(),
        )


@pytest.mark.parametrize(
    ("path", "keyword"),
    (
        (ADAPTER, "canary_adapter_git_blob_drift"),
        (REQUIREMENTS, "canary_requirements_git_blob_drift"),
    ),
)
def test_dependency_byte_drift_fails_closed(
    path: Path,
    keyword: str,
) -> None:
    raw = path.read_bytes()
    mutated = raw + b"\n"
    kwargs = {
        "historical_runner_bytes": RUNNER.read_bytes(),
        "canary_adapter_bytes": ADAPTER.read_bytes(),
        "canary_requirements_bytes": REQUIREMENTS.read_bytes(),
    }
    if path == ADAPTER:
        kwargs["canary_adapter_bytes"] = mutated
    else:
        kwargs["canary_requirements_bytes"] = mutated
    with pytest.raises(
        review.ScoutRepairCanaryFullRunnerReviewHold,
        match=keyword,
    ):
        review.review_full_runner_composition(**kwargs)


def test_reviewer_source_has_no_host_or_execution_imports() -> None:
    tree = ast.parse(
        REVIEW_SOURCE.read_text(encoding="utf-8"),
        filename=str(REVIEW_SOURCE),
    )
    forbidden = {
        "asyncio",
        "ctypes",
        "docker",
        "http",
        "httpx",
        "multiprocessing",
        "os",
        "pathlib",
        "requests",
        "shutil",
        "socket",
        "subprocess",
        "urllib",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden


def test_reviewer_does_not_import_reviewed_runtime_sources() -> None:
    source = REVIEW_SOURCE.read_text(encoding="utf-8")
    assert "from openra_env" not in source
    assert "import openra_env" not in source


def test_operational_entrypoint_always_holds() -> None:
    with pytest.raises(
        review.ScoutRepairCanaryFullRunnerReviewHold,
        match=review.NEXT_GATE,
    ):
        review.authorize_install_or_execute()
