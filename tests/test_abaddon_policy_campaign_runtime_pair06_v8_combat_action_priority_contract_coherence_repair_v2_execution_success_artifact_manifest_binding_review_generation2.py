from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_execution_success_artifact_manifest_binding_review_generation2
    as review,
)


ROOT = Path(__file__).parents[1]
MANIFEST = ROOT / review.MANIFEST_PATH


def _git_blob_sha1(raw: bytes) -> str:
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def _load() -> dict:
    raw = MANIFEST.read_bytes()
    assert _git_blob_sha1(raw) == review.MANIFEST_GIT_BLOB
    return json.loads(raw.decode("utf-8"))


def test_manifest_blob_and_observer_sources_are_exactly_pinned():
    out = review.pair06_v8_coherent_v2_artifact_manifest_review_contract(_load())
    assert out["manifest_git_blob"] == "87f2d5ba1a2fdcfd4d5c12f595a86a193e4097f2"

    bindings = {
        review.REHASH_SOURCE_PATH: review.REHASH_SOURCE_GIT_BLOB,
        review.REHASH_TEST_PATH: review.REHASH_TEST_GIT_BLOB,
        review.AUDIT_SOURCE_PATH: review.AUDIT_SOURCE_GIT_BLOB,
        review.AUDIT_TEST_PATH: review.AUDIT_TEST_GIT_BLOB,
    }
    assert bindings == {
        review.REHASH_SOURCE_PATH: "65134520a1bf0d621b6e63fdceb003dc1f964f59",
        review.REHASH_TEST_PATH: "6382f6dc345c91657ac1252db9b7195fdebe3a85",
        review.AUDIT_SOURCE_PATH: "99391cdc0493cca4887105fefda5d2569b1401bc",
        review.AUDIT_TEST_PATH: "4ec4bcf7d39c743c2004030f7fc37a3ed40cc887",
    }

    for relative, expected_blob in bindings.items():
        raw = (ROOT / relative).read_bytes()
        assert _git_blob_sha1(raw) == expected_blob


def test_one_byte_source_drift_breaks_pinned_blob_identity():
    raw = (ROOT / review.REHASH_SOURCE_PATH).read_bytes()
    assert _git_blob_sha1(raw) == review.REHASH_SOURCE_GIT_BLOB
    mutated = raw[:-1] + bytes([raw[-1] ^ 1])
    assert _git_blob_sha1(mutated) != review.REHASH_SOURCE_GIT_BLOB


def test_manifest_closes_only_the_artifact_evidence_frontier():
    out = review.pair06_v8_coherent_v2_artifact_manifest_review_contract(_load())
    assert out["manifest_validated"] is True
    assert out["artifact_bytes_verified"] is True
    assert out["artifact_cross_file_semantics_verified"] is True
    assert out["repo_side_local_artifact_rehash_performed"] is True
    assert out["byte_drift_negative_control_present"] is True
    assert out["public_safe_artifact_manifest_bound"] is True
    assert out["execution_lineage_closed"] is True
    assert out["artifact_evidence_frontier_closed"] is True
    assert out["source_artifact_evidence_frontier_closed"] is True
    assert out["source_frontier_closed"] is True
    assert out["next_gate"] == "PAIR06_V8_COHERENT_V2_SUCCESS_ARTIFACT_EVIDENCE_CLOSED"
    assert out["next_change_class"] == "none"


def test_manifest_preserves_spent_attempt_and_zero_follow_on_authority():
    out = review.pair06_v8_coherent_v2_artifact_manifest_review_contract(_load())
    assert out["attempt_reusable"] is False
    assert out["authorization_reusable"] is False
    assert out["automatic_retry"] is False
    assert set(out["authority"]) == set(review.FALSE_AUTHORITY_FIELDS)
    assert all(value is False for value in out["authority"].values())


@pytest.mark.parametrize("artifact", sorted(review.EXPECTED_ARTIFACTS))
def test_any_artifact_digest_drift_fails_closed(artifact):
    value = _load()
    value["artifacts"][artifact]["sha256"] = "0" * 64
    with pytest.raises(
        review.Pair06V8CoherentV2ArtifactManifestReviewHold,
        match="MANIFEST_ARTIFACT_SHA256_DRIFT",
    ):
        review.validate_artifact_rehash_manifest(value)


@pytest.mark.parametrize(
    "field,value",
    [
        ("artifact_bytes_verified", False),
        ("artifact_cross_file_semantics_verified", False),
        ("repo_side_local_artifact_rehash_performed", False),
        ("host_mutation_performed", True),
        ("attempt_reusable", True),
        ("authorization_reusable", True),
        ("automatic_retry", True),
        ("new_execution_request_opened", True),
    ],
)
def test_manifest_verification_or_authority_drift_fails_closed(field, value):
    manifest = _load()
    manifest[field] = value
    with pytest.raises(review.Pair06V8CoherentV2ArtifactManifestReviewHold):
        review.validate_artifact_rehash_manifest(manifest)



def test_unknown_manifest_field_fails_closed():
    manifest = _load()
    manifest["unexpected"] = "drift"
    with pytest.raises(
        review.Pair06V8CoherentV2ArtifactManifestReviewHold,
        match="MANIFEST_FIELD_SET_DRIFT",
    ):
        review.validate_artifact_rehash_manifest(manifest)

def test_manifest_receipt_is_defensively_copied():
    manifest = _load()
    out = review.pair06_v8_coherent_v2_artifact_manifest_review_contract(manifest)
    manifest["artifacts"]["trajectory"]["sha256"] = "0" * 64
    assert out["validated_manifest"]["artifacts"]["trajectory"]["sha256"] == (
        review.EXPECTED_ARTIFACTS["trajectory"]["sha256"]
    )


def test_review_cannot_reopen_execution():
    with pytest.raises(
        review.Pair06V8CoherentV2ArtifactManifestReviewHold,
        match="EXECUTION_LINEAGE_CLOSED",
    ):
        review.execute_or_reopen()
