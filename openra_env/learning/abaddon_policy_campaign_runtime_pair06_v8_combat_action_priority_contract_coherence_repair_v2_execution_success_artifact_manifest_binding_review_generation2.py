"""Bind the public-safe pair-06 V8 V2 coherent success artifact manifest.

The designated Precision observer independently rehashed the six durable
artifacts from the already-closed successful execution.  This source reviews
that public-safe manifest in memory and closes only the artifact-evidence
frontier.

The execution lineage remains permanently closed.  No retry, replay, training,
promotion, deployment, VOID-chain, wallet, transaction, or funds authority is
created by manifest acceptance.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-priority-coherent-v2-success-artifact-manifest-review.v1"
)
MANIFEST_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v8-combat-priority-coherent-v2-success-artifact-rehash-manifest.v1"
)

MANIFEST_PATH = (
    "config/war-college/"
    "pair06-v8-coherent-v2-success-artifact-rehash-manifest-v1.json"
)
MANIFEST_GIT_BLOB = "87f2d5ba1a2fdcfd4d5c12f595a86a193e4097f2"
REHASH_SOURCE_PATH = "tools/void_pair06_v8_coherent_v2_success_artifact_rehash_precision_v1.py"
REHASH_SOURCE_GIT_BLOB = "65134520a1bf0d621b6e63fdceb003dc1f964f59"
REHASH_TEST_PATH = "tests/test_void_pair06_v8_coherent_v2_success_artifact_rehash_precision_v1.py"
REHASH_TEST_GIT_BLOB = "6382f6dc345c91657ac1252db9b7195fdebe3a85"

AUDIT_SOURCE_GIT_BLOB = "99391cdc0493cca4887105fefda5d2569b1401bc"
AUDIT_TEST_GIT_BLOB = "aeaa82d9f59b70ebb9d90743f2ed462b2c39743d"

RUN_ID = "warmstart-apollyon-vs-abaddon-20260927T183337Z-feinter-s208354846"
AUTHORIZED_EXECUTION_MAIN = "d8b16f1c23a74803ac4ace94045fed147c3c69fe"
SOURCE_BASIS_MAIN = "d25c45a4790cad764205adeea2e8e480c1bbb9bf"

EXPECTED_ARTIFACTS = {
    "attempt_marker": {
        "byte_count": 1865,
        "sha256": "a64faf60c8f548efb5d869374f437de20f7165b1b53ea978332225f68efc7207",
    },
    "result": {
        "byte_count": 12584,
        "sha256": "b205421d468d2c02eb73649dc6cffa10084f58cc55c64950ab3d23d5ea21cee4",
    },
    "closeout": {
        "byte_count": 1518,
        "sha256": "181bdd2fd818a5e6376f4a58d0bcfae3ae986f96f9298acee0c9e92f818c43d1",
    },
    "trajectory": {
        "byte_count": 440704,
        "sha256": "afc57351991c90dc21e4d2316ddd23fce8b01b9132a3435a9252de7227001ddc",
    },
    "summary": {
        "byte_count": 9274,
        "sha256": "a5d72287487849164e727836eee82dd5821ddb46f5803b995b1d67cc289075ab",
    },
    "warm_start": {
        "byte_count": 229255,
        "sha256": "f36f2717d34e028d02d1b7076d7de1cff65dce1ffed59710110f2adbf4ad700d",
    },
}

FALSE_AUTHORITY_FIELDS = (
    "retry_authorized",
    "replay_authorized",
    "training_authorized",
    "promotion_authorized",
    "deployment_authorized",
    "void_chain_mutation_authorized",
    "wallet_or_funds_action_authorized",
    "new_execution_request_opened",
)

NEXT_GATE = "PAIR06_V8_COHERENT_V2_SUCCESS_ARTIFACT_EVIDENCE_CLOSED"
NEXT_CHANGE_CLASS = "none"


class Pair06V8CoherentV2ArtifactManifestReviewHold(ValueError):
    pass


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise Pair06V8CoherentV2ArtifactManifestReviewHold(code)


def validate_artifact_rehash_manifest(record: Mapping[str, Any]) -> dict[str, Any]:
    _require(isinstance(record, Mapping), "MANIFEST_OBJECT_REQUIRED")
    value = dict(record)

    _require(value.get("schema") == MANIFEST_SCHEMA, "MANIFEST_SCHEMA_DRIFT")
    _require(
        value.get("run_id") == RUN_ID
        and value.get("pair_slot") == 6
        and value.get("arm") == "baseline",
        "MANIFEST_RUN_SCOPE_DRIFT",
    )
    _require(
        value.get("authorized_execution_main") == AUTHORIZED_EXECUTION_MAIN,
        "MANIFEST_EXECUTION_MAIN_DRIFT",
    )
    _require(
        value.get("source_basis_main") == SOURCE_BASIS_MAIN,
        "MANIFEST_SOURCE_BASIS_DRIFT",
    )
    _require(
        value.get("artifact_count") == 6
        and value.get("artifact_bytes_verified") is True
        and value.get("artifact_cross_file_semantics_verified") is True
        and value.get("repo_side_local_artifact_rehash_performed") is True,
        "MANIFEST_ARTIFACT_VERIFICATION_INCOMPLETE",
    )
    _require(
        value.get("host_observation_performed") is True
        and value.get("host_mutation_performed") is False,
        "MANIFEST_HOST_BOUNDARY_DRIFT",
    )
    _require(
        value.get("execution_lineage_closed") is True
        and value.get("attempt_reusable") is False
        and value.get("authorization_reusable") is False
        and value.get("automatic_retry") is False
        and value.get("new_execution_request_opened") is False,
        "MANIFEST_EXECUTION_CLOSURE_DRIFT",
    )

    for field in (
        "game_execution_performed_by_observer",
        "model_inference_performed_by_observer",
        "training_performed_by_observer",
        "deployment_performed_by_observer",
        "void_chain_mutation_performed_by_observer",
        "wallet_or_funds_action_performed_by_observer",
    ):
        _require(value.get(field) is False, "MANIFEST_OBSERVER_BOUNDARY_DRIFT:" + field)

    artifacts = value.get("artifacts")
    _require(type(artifacts) is dict, "MANIFEST_ARTIFACT_MAP_REQUIRED")
    _require(set(artifacts) == set(EXPECTED_ARTIFACTS), "MANIFEST_ARTIFACT_SET_DRIFT")

    for name, expected in EXPECTED_ARTIFACTS.items():
        observed = artifacts.get(name)
        _require(type(observed) is dict, "MANIFEST_ARTIFACT_RECORD_REQUIRED:" + name)
        _require(
            set(observed)
            == {
                "byte_count",
                "generation_stable",
                "regular_file",
                "sha256",
                "single_link",
                "symlink_followed",
            },
            "MANIFEST_ARTIFACT_FIELD_SET_DRIFT:" + name,
        )
        _require(
            observed.get("byte_count") == expected["byte_count"],
            "MANIFEST_ARTIFACT_BYTE_COUNT_DRIFT:" + name,
        )
        _require(
            observed.get("sha256") == expected["sha256"],
            "MANIFEST_ARTIFACT_SHA256_DRIFT:" + name,
        )
        _require(
            observed.get("generation_stable") is True
            and observed.get("regular_file") is True
            and observed.get("single_link") is True
            and observed.get("symlink_followed") is False,
            "MANIFEST_ARTIFACT_IDENTITY_DRIFT:" + name,
        )

    return deepcopy(value)


def pair06_v8_coherent_v2_artifact_manifest_review_contract(
    manifest: Mapping[str, Any],
) -> dict[str, Any]:
    validated = validate_artifact_rehash_manifest(manifest)
    return {
        "schema": CONTRACT_SCHEMA,
        "manifest_path": MANIFEST_PATH,
        "manifest_git_blob": MANIFEST_GIT_BLOB,
        "rehash_source_path": REHASH_SOURCE_PATH,
        "rehash_source_git_blob": REHASH_SOURCE_GIT_BLOB,
        "rehash_test_path": REHASH_TEST_PATH,
        "rehash_test_git_blob": REHASH_TEST_GIT_BLOB,
        "audit_source_git_blob": AUDIT_SOURCE_GIT_BLOB,
        "audit_test_git_blob": AUDIT_TEST_GIT_BLOB,
        "run_id": RUN_ID,
        "artifact_count": 6,
        "expected_artifacts": deepcopy(EXPECTED_ARTIFACTS),
        "manifest_validated": True,
        "artifact_bytes_verified": True,
        "artifact_cross_file_semantics_verified": True,
        "repo_side_local_artifact_rehash_performed": True,
        "byte_drift_negative_control_present": True,
        "public_safe_artifact_manifest_bound": True,
        "execution_lineage_closed": True,
        "attempt_reusable": False,
        "authorization_reusable": False,
        "automatic_retry": False,
        "artifact_evidence_frontier_closed": True,
        "source_artifact_evidence_frontier_closed": True,
        "source_frontier_closed": True,
        "authority": {field: False for field in FALSE_AUTHORITY_FIELDS},
        "validated_manifest": validated,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def execute_or_reopen(*args: Any, **kwargs: Any) -> None:
    raise Pair06V8CoherentV2ArtifactManifestReviewHold(
        "PAIR06_V8_COHERENT_V2_EXECUTION_LINEAGE_CLOSED"
    )
