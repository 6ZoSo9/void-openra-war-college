from __future__ import annotations

import ast
from copy import deepcopy
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_host_preflight_generation2 as preflight,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_host_preflight_source_binding_review_generation2
    as review,
)

REPO = Path(__file__).resolve().parents[1]
REVIEW_SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_host_preflight_source_binding_review_generation2.py"
)


def test_exact_preflight_identities_are_pinned():
    out = review.v2r13_host_preflight_source_binding_review_contract()
    assert out["preflight_git_blob"] == "0ae27981a08b27083b235ae4807705c88da259a1"
    assert out["preflight_source_sha256"] == (
        "22620f890efdcfa81882a2e3869dcd88188932ee0417b6aeb4994c7b5829873a"
    )
    assert out["precision_collector_git_blob"] == (
        "62d8a906ea41138b5443ba3bf96799b6e430b5be"
    )
    assert out["precision_collector_source_sha256"] == (
        "0501126c442fe58c8fce296e15146bd7c2eb6d36ac22d423681e1bae92edcc3c"
    )
    assert out["preflight_test_git_blob"] == (
        "c16e514dc0675c56dc6c98575d7b184935eacd3a"
    )
    assert out["preflight_test_sha256"] == (
        "4c7ee1e4c5e0b84ddb0ec24295b64d73b3e8a598337b909bc8f43fb6855bb991"
    )


def test_review_accepts_read_only_preflight_surface():
    out = review.v2r13_host_preflight_source_binding_review()
    assert out["host_preflight_validator_implemented"] is True
    assert out["precision_read_only_collector_implemented"] is True
    assert out["host_preflight_source_binding_present"] is True
    assert out["host_preflight_reviewed"] is True
    assert out["host_preflight_invoked"] is False
    assert out["host_preflight_completed"] is False


def test_review_preserves_runtime_boundaries():
    out = review.v2r13_host_preflight_source_binding_review()
    assert out["runtime_execution_authorization_accepted"] is True
    assert out["runtime_execution_implemented"] is True
    assert out["runtime_execution_authorized"] is True
    assert out["runtime_execution_performed"] is False
    assert out["fresh_readiness_still_required_before_inference"] is True
    assert out["automatic_retry"] is False
    assert out["model_inference_performed"] is False
    assert out["game_execution_performed"] is False
    assert out["training_performed"] is False
    assert out["weights_updated"] is False
    assert out["automatic_policy_promotion"] is False
    assert out["deployment_performed"] is False
    assert out["void_chain_mutation_performed"] is False
    assert out["wallet_or_funds_action_performed"] is False


def test_review_advances_only_to_precision_invocation():
    out = review.v2r13_host_preflight_source_binding_review_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_source_blockers"] == ()
    assert out["execution_blockers"] == (
        "V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_INVOCATION_REQUIRED",
    )
    assert out["next_gate"] == (
        "V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_INVOCATION_REQUIRED"
    )
    assert out["next_change_class"] == "precision_v2r13_host_preflight_invocation"


def test_manifest_identity_is_preserved():
    out = review.v2r13_host_preflight_source_binding_review()
    validated = out["validated_preflight_contract"]
    assert validated["tracked_blobs"] == preflight.TRACKED_BLOBS
    assert validated["external_files"] == preflight.EXTERNAL_FILES
    assert validated["authorized_pair_slots"] == (3, 9, 15)
    assert validated["authorized_arms"] == ("baseline", "candidate")


def test_tampered_preflight_contract_is_rejected(monkeypatch):
    original = preflight.host_preflight_contract

    def tampered():
        value = deepcopy(original())
        value["runtime_execution_performed"] = True
        return value

    review._validate_preflight_cached.cache_clear()
    monkeypatch.setattr(preflight, "host_preflight_contract", tampered)
    try:
        with pytest.raises(
            review.V2R13HostPreflightSourceBindingReviewHold,
            match="unexpectedly executed runtime",
        ):
            review.v2r13_host_preflight_source_binding_review()
    finally:
        review._validate_preflight_cached.cache_clear()


def test_review_source_has_no_host_io_imports():
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


def test_host_preflight_invocation_entrypoint_holds():
    with pytest.raises(
        review.V2R13HostPreflightSourceBindingReviewHold,
        match="V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_INVOCATION_REQUIRED",
    ):
        review.invoke_host_preflight()


def test_runtime_execution_entrypoint_holds_until_preflight_invoked():
    with pytest.raises(
        review.V2R13HostPreflightSourceBindingReviewHold,
        match="V2R13_RUNTIME_EXECUTION_HOST_PREFLIGHT_NOT_YET_INVOKED",
    ):
        review.execute_v2r13_runtime()
