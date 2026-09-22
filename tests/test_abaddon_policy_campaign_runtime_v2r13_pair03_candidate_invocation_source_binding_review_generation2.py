from __future__ import annotations

import ast
import hashlib
from copy import deepcopy
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_invocation_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_pair03_candidate_invocation_source_binding_review_generation2.py"
)
EXPECTED_SOURCE_SHA256 = (
    "4d30eb0ca6e293a02c418b9a8404bac752c7b2316535cc039d01cb63a0aa5c48"
)


def contract():
    return review.v2r13_pair03_candidate_invocation_source_binding_review_contract()


def test_review_source_sha_is_exact():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SOURCE_SHA256


def test_review_pins_exact_invocation_and_adversarial_test_surface():
    out = contract()
    assert out["invocation_git_blob"] == "a790b5b1568b42b1a629a525387366d2bb499128"
    assert out["invocation_source_sha256"] == (
        "1df36c53c6e7d1f6ff07f732e792e6fdcaab7a8d0d5b9d8249851b78e11202c0"
    )
    assert out["invocation_test_git_blob"] == "4823d4cbb6824dcd8b0628b70d611a321c12bc10"
    assert out["invocation_test_sha256"] == (
        "24330d7aeb436926e27d875abf9532164a35c2d17080e6f8d3d63791f01309ac"
    )
    assert out["candidate_invocation_source_identity_pinned_by_git_blob"] is True
    assert out["candidate_invocation_source_identity_pinned_by_sha256"] is True
    assert out["candidate_invocation_test_identity_pinned_by_git_blob"] is True
    assert out["candidate_invocation_test_identity_pinned_by_sha256"] is True
    assert out["precision_cli_git_blob"] == "267a7348ce08ac66d2c46fbc931bb5cf1fb4e8af"
    assert out["precision_cli_source_sha256"] == (
        "516a6192ed45a8596372bf50e087991340508b71d6e0b8b8109e1c4c78079f87"
    )
    assert out["precision_cli_test_git_blob"] == "cdeee21152bd135523d217feb17823fe4acfd994"
    assert out["precision_cli_test_sha256"] == (
        "fadaa3386ff90045f3fee0f4c016dd3786d4fa5ad15fdba3d1c901bd14333aaa"
    )
    assert out["precision_cli_identity_pinned_by_git_blob"] is True
    assert out["precision_cli_identity_pinned_by_sha256"] is True
    assert out["precision_cli_test_identity_pinned_by_git_blob"] is True
    assert out["precision_cli_test_identity_pinned_by_sha256"] is True
    assert out["precision_cli_requires_expected_main_head"] is True
    assert out["precision_cli_pins_reviewed_invocation_source_sha256"] is True
    assert out["precision_cli_requires_explicit_confirmation"] is True


def test_review_is_separate_and_does_not_self_bind_invocation():
    out = contract()
    assert out["candidate_invocation_source_is_not_self_bound"] is True
    assert out["separate_review_instrument"] is True
    assert out["candidate_invocation_implemented"] is True
    assert out["candidate_invocation_source_binding_present"] is True
    assert out["candidate_invocation_reviewed"] is True


def test_exact_candidate_dependency_blobs_remain_pinned():
    out = contract()
    assert out["request_git_blob"] == "07516a24553b2516b859bebca21818c0bd0bf01e"
    assert out["attempt_guard_git_blob"] == "b47a2befd6d7181aa5a00805ae20e66293625d45"
    assert out["host_preflight_git_blob"] == "32c27cacdcd850022bd3de358f82554112c6fd7b"
    assert out["git_backend_git_blob"] == "fe578c66b14e08c64e9281a808064b8c8d5e739a"
    assert out["bounded_executor_git_blob"] == "c7e20c1157e0bcf7f65036631aad47fb82c7aefd"
    assert out["first_baseline_invocation_git_blob"] == (
        "5b790efaf4085deb15eaef538635fd11f5cad9a5"
    )
    pins = out["review"]["dependencies"]["candidate_invocation_pinned_sources"]
    assert pins == review.EXPECTED_PINNED_SOURCES


def test_review_accepts_only_pair03_nonheld_candidate_scope():
    out = contract()
    assert out["pair_slot"] == 3
    assert out["arm"] == "candidate"
    assert out["held_out"] is False
    proposal = out["review"]["dependencies"]["candidate_authorization_request"]["request"]
    assert proposal["proposed_scope"] == {
        "pair_slot": 3,
        "arm": "candidate",
        "held_out": False,
        "maximum_candidate_attempts": 1,
        "maximum_automatic_retries": 0,
        "other_pair_slots_included": False,
        "baseline_rerun_included": False,
    }


def test_authorization_request_requires_this_review_but_review_grants_no_authority():
    out = contract()
    proposal = out["review"]["dependencies"]["candidate_authorization_request"]["request"]
    assert "exact_candidate_invocation_source_reviewed" in proposal["required_runtime_gates"]
    assert "candidate_specific_operator_authorization_accepted" in proposal["required_runtime_gates"]
    assert out["candidate_specific_operator_authorization_accepted"] is False
    assert out["operator_authenticated"] is False
    assert out["runtime_execution_authorized"] is False
    assert out["runtime_execution_invoked_by_review"] is False
    assert out["candidate_execution_performed_by_review"] is False


def test_review_preserves_all_operation_time_gates():
    out = contract()["review"]
    for field in (
        "candidate_specific_confirmation_required",
        "single_use_attempt_required",
        "fresh_current_main_preflight_required",
        "cached_sudo_required",
        "live_revocation_sentinel_absent_required",
        "isolated_grpc_python_required",
        "exact_model_preload_before_readiness_without_inference_required",
        "canonical_worktree_observation_required",
        "fresh_canonical_live_readiness_before_inference_required",
        "exact_baseline_evidence_reverification_required",
        "create_only_attempt_consumption_required",
        "completed_baseline_preservation_required",
        "result_create_only_required",
    ):
        assert out[field] is True


def test_review_does_not_expand_follow_on_authority():
    out = contract()
    assert out["automatic_retry"] is False
    for field in (
        "held_out_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_performs_no_host_or_runtime_action():
    out = contract()
    for field in (
        "review_host_observation_implemented",
        "review_filesystem_mutation_implemented",
        "review_git_query_implemented",
        "review_subprocess_execution_implemented",
        "review_network_request_implemented",
        "review_ollama_request_implemented",
        "review_docker_command_implemented",
        "review_service_action_implemented",
        "review_model_load_implemented",
        "review_model_inference_implemented",
        "review_game_execution_implemented",
        "review_training_implemented",
        "review_deployment_implemented",
        "review_void_chain_mutation_implemented",
        "review_wallet_or_funds_action_implemented",
    ):
        assert out[field] is False


def test_frontier_advances_only_to_explicit_candidate_authorization():
    out = contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_PAIR03_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
    )
    assert out["next_change_class"] == (
        "trusted_operator_v2r13_pair03_candidate_execution_authorization"
    )


def test_authorize_or_execute_entrypoint_always_holds():
    with pytest.raises(
        review.V2R13Pair03CandidateInvocationSourceBindingReviewHold,
        match="V2R13_PAIR03_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        review.authorize_or_execute_candidate()


def test_review_contract_is_copy_isolated():
    first = contract()
    first["review"]["dependencies"]["candidate_invocation_pinned_sources"].clear()
    second = contract()
    assert second["review"]["dependencies"]["candidate_invocation_pinned_sources"] == (
        review.EXPECTED_PINNED_SOURCES
    )


def test_static_review_source_has_no_direct_host_io_or_execution_surface():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    forbidden_import_roots = {
        "asyncio",
        "ctypes",
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
    forbidden_names = {"open", "exec", "eval", "__import__"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in forbidden_names


def test_review_never_calls_candidate_invocation():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))

    def dotted(node):
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            base = dotted(node.value)
            return f"{base}.{node.attr}" if base else node.attr
        return ""

    calls = {
        dotted(node.func)
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
    }
    assert "invocation.execute_pair03_candidate" not in calls


def test_historical_request_remains_non_authorizing_after_review():
    before = review.request.candidate_authorization_request_contract()
    _ = contract()
    after = review.request.candidate_authorization_request_contract()
    assert before == after
    authority = after["request"]["authority"]
    assert authority and all(value is False for value in authority.values())
