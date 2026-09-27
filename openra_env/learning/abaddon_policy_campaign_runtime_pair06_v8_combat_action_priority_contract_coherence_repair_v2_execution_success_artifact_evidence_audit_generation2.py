"""Post-close artifact-evidence audit for pair-06 V8 V2 coherent success.

The execution lineage remains permanently closed: the attempt and authorization
are spent and no retry, replay, training, promotion, deployment, chain, wallet,
or funds authority is created here.

This source corrects a narrower evidence classification.  The merged success
closeout and source-binding review record terminal SHA-256 strings, but neither
module independently rehashed the six durable runtime artifacts.  Therefore
execution closure and artifact-byte provenance are tracked separately until a
public-safe, content-addressed manifest derived from those bytes is reviewed.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_execution_success_closeout_generation2
    as closeout,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_execution_success_closeout_source_binding_review_generation2
    as prior_review,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-priority-coherent-v2-success-artifact-evidence-audit.v1"
)

PRIOR_REVIEW_MAIN_HEAD = "d25c45a4790cad764205adeea2e8e480c1bbb9bf"
PRIOR_REVIEW_GIT_BLOB = "149b04e687d16d797603701089846804a384b7ae"
PRIOR_REVIEW_TEST_GIT_BLOB = "94ed17419854cd91b030048524a72b5895086d05"

EXPECTED_ARTIFACT_SHA256 = {
    "attempt_marker": (
        "a64faf60c8f548efb5d869374f437de20f7165b1b53ea978332225f68efc7207"
    ),
    "result": (
        "b205421d468d2c02eb73649dc6cffa10084f58cc55c64950ab3d23d5ea21cee4"
    ),
    "closeout": (
        "181bdd2fd818a5e6376f4a58d0bcfae3ae986f96f9298acee0c9e92f818c43d1"
    ),
    "trajectory": (
        "afc57351991c90dc21e4d2316ddd23fce8b01b9132a3435a9252de7227001ddc"
    ),
    "summary": (
        "a5d72287487849164e727836eee82dd5821ddb46f5803b995b1d67cc289075ab"
    ),
    "warm_start": (
        "f36f2717d34e028d02d1b7076d7de1cff65dce1ffed59710110f2adbf4ad700d"
    ),
}

NEXT_GATE = "PAIR06_V8_COHERENT_V2_ARTIFACT_MANIFEST_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_public_safe_artifact_manifest_binding"


class Pair06V8CoherentV2ArtifactEvidenceAuditHold(ValueError):
    """Artifact-byte provenance remains open without a reviewed manifest."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V8CoherentV2ArtifactEvidenceAuditHold(message)


def _expected_from_closeout(record: dict[str, Any]) -> dict[str, str]:
    return {
        "attempt_marker": record["attempt_marker_sha256"],
        "result": record["result_file_sha256"],
        "closeout": record["closeout_file_sha256"],
        "trajectory": record["trajectory_sha256"],
        "summary": record["summary_sha256"],
        "warm_start": record["warm_start_sha256"],
    }


def pair06_v8_coherent_v2_artifact_evidence_audit_contract() -> dict[str, Any]:
    """Separate immutable execution closure from still-open artifact proof."""
    closed = prior_review.pair06_v8_combat_priority_coherent_v2_success_review_contract()
    recorded = (
        closeout.pair06_v8_combat_priority_coherent_v2_success_closeout_contract()
    )
    expected = _expected_from_closeout(recorded)

    _require(closed.get("lineage_closed") is True, "prior lineage closure drift")
    _require(
        closed.get("new_execution_request_opened") is False,
        "prior review unexpectedly opened execution",
    )
    _require(
        closed.get("attempt_consumed") is True
        and closed.get("attempt_reusable") is False
        and closed.get("authorization_reusable") is False
        and closed.get("automatic_retry") is False,
        "spent execution boundary drift",
    )
    _require(
        recorded.get("repo_side_local_artifact_rehash_performed") is False,
        "historical closeout rehash classification drift",
    )
    _require(expected == EXPECTED_ARTIFACT_SHA256, "recorded artifact digest drift")

    return {
        "schema": CONTRACT_SCHEMA,
        "record_kind": "source_only_post_close_artifact_evidence_audit",
        "prior_review_main_head": PRIOR_REVIEW_MAIN_HEAD,
        "prior_review_git_blob": PRIOR_REVIEW_GIT_BLOB,
        "prior_review_test_git_blob": PRIOR_REVIEW_TEST_GIT_BLOB,
        "run_id": recorded["run_id"],
        "pair_slot": recorded["pair_slot"],
        "arm": recorded["arm"],
        "rounds_completed": recorded["rounds_completed"],
        "final_tick": recorded["final_tick"],
        "outcome": recorded["outcome"],
        "expected_artifact_sha256": deepcopy(EXPECTED_ARTIFACT_SHA256),
        "execution_lineage_closed": True,
        "attempt_consumed": True,
        "attempt_reusable": False,
        "authorization_reusable": False,
        "automatic_retry": False,
        "new_execution_request_opened": False,
        "prior_source_frontier_closed_claim": closed["source_frontier_closed"],
        "repo_side_local_artifact_rehash_performed": False,
        "artifact_bytes_verified_by_this_audit": False,
        "public_safe_artifact_manifest_bound": False,
        "artifact_byte_drift_regression_bound": False,
        "source_artifact_evidence_frontier_closed": False,
        "source_frontier_closed": False,
        "retry_authorized": False,
        "replay_authorized": False,
        "training_authorized": False,
        "promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def bind_artifact_manifest(*args: Any, **kwargs: Any) -> None:
    """Manifest admission is intentionally unavailable in this audit layer."""
    raise Pair06V8CoherentV2ArtifactEvidenceAuditHold(NEXT_GATE)


def execute_or_reopen(*args: Any, **kwargs: Any) -> None:
    """No post-close audit may reopen the consumed execution lineage."""
    raise Pair06V8CoherentV2ArtifactEvidenceAuditHold(
        "PAIR06_V8_COHERENT_V2_EXECUTION_LINEAGE_CLOSED"
    )
