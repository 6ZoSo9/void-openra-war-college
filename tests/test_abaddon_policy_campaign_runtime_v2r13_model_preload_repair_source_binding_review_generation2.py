from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_model_preload_repair_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
REVIEW_SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_model_preload_repair_source_binding_review_generation2.py"
)


def test_exact_repair_identities_are_pinned():
    out = review.v2r13_model_preload_repair_source_binding_review_contract()
    assert out["repaired_invocation_git_blob"] == (
        "5b790efaf4085deb15eaef538635fd11f5cad9a5"
    )
    assert out["repaired_invocation_source_sha256"] == (
        "3d87705a42156b0603cfa945e455200f0999291b7d70ee57bf65334d8f8c4a40"
    )
    assert out["repaired_test_git_blob"] == (
        "0584426fe3dc10d79c6d535503f453529826dd1b"
    )
    assert out["repaired_test_sha256"] == (
        "4ac3a8dff592c04e315e46e506318559595e7831887dada663705dd870ff8f6c"
    )


def test_review_accepts_model_load_without_inference():
    out = review.v2r13_model_preload_repair_source_binding_review_contract()
    assert out["repair_source_binding_present"] is True
    assert out["repair_reviewed"] is True
    assert out["exact_v2r13_model_preload_reviewed"] is True
    assert out["empty_generate_prompt_reviewed"] is True
    assert out["empty_response_required"] is True
    assert out["token_evaluation_forbidden"] is True
    assert out["model_load_before_readiness_reviewed"] is True
    assert out["model_inference_during_preload"] is False


def test_review_does_not_expand_execution_authority():
    out = review.v2r13_model_preload_repair_source_binding_review_contract()
    assert out["runtime_execution_invoked"] is False
    assert out["runtime_execution_performed"] is False
    assert out["automatic_retry"] is False
    for field in (
        "candidate_arm_authorized",
        "held_out_arm_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_review_advances_only_to_retry_rebind():
    out = review.v2r13_model_preload_repair_source_binding_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "V2R13_PAIR03_BASELINE_RETRY_REBIND_REQUIRED",
    )
    assert out["next_gate"] == "V2R13_PAIR03_BASELINE_RETRY_REBIND_REQUIRED"


def test_review_source_is_host_action_free():
    tree = ast.parse(
        REVIEW_SOURCE.read_text(encoding="utf-8"),
        filename=str(REVIEW_SOURCE),
    )
    forbidden = {
        "os",
        "pathlib",
        "socket",
        "subprocess",
        "urllib",
        "requests",
        "httpx",
    }
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".", 1)[0])
    assert not (imported & forbidden)


def test_execution_entrypoint_remains_closed():
    with pytest.raises(
        review.V2R13ModelPreloadRepairReviewHold,
        match="V2R13_PAIR03_BASELINE_RETRY_REBIND_REQUIRED",
    ):
        review.execute_retry()
