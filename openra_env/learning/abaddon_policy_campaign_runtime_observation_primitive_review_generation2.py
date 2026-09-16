"""Semantic review contract for Generation-2 runtime observation primitives.

This module classifies existing canonical post-PR89 primitives discovered by the
static observation-primitive census.  It performs no observation.

The review deliberately distinguishes:

* a pure supplied-fact validator that can be reused without collecting anything;
* existing read-only verification functions whose semantics are useful but do
  not yet satisfy the stronger Generation-2 evidence requirements;
* private/general helpers that are design references only;
* generic designated-host discovery that is not Apollyon runtime identity proof.

No primitive in this source performs filesystem I/O, Git commands, subprocess
execution, HTTP/systemd probing, model loading, worktree creation, or runtime
execution.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    RUNTIME_AUTHORITY_BLOCKER,
    V10,
    V14,
    V2R13,
    V8,
)
from openra_env.learning.abaddon_policy_campaign_runtime_observation_mechanics_generation2 import (
    observation_mechanics,
)
from openra_env.learning.abaddon_policy_campaign_runtime_path_inputs_generation2 import (
    path_input_requirement,
)

CONTRACT_SCHEMA = "void.abaddon.generation2.runtime-observation-primitive-review.v1"
PRIMITIVE_SCHEMA = "void.abaddon.generation2.runtime-observation-primitive.v1"

OBSERVATION_PRIMITIVE_CENSUS_SHA256 = (
    "6e5ad372c5b2edf758c8cb5bd9c0e815fc5c4cf5804d96c2ab5ebb34e223432f"
)

V8_RUNTIME_GIT_BLOB = "fd0e72767ba199e88af9e9eb2455c03ace027a14"
SPAR_CONTRACT_GIT_BLOB = "9a7cabeb7578a40745e344c32f27845bf1659097"
DESIGNATED_DISCOVERY_GIT_BLOB = "aadcc32fbba9a11d9f4d53f2410a7321c46c0131"

V8_ENVIRONMENT_VALIDATOR = (
    "openra_env.learning.apollyon_v8_campaign_runtime."
    "validate_v8_runtime_environment"
)
V8_ENVIRONMENT_LIVE_VERIFIER = (
    "openra_env.learning.apollyon_v8_campaign_runtime."
    "verify_v8_runtime_environment"
)
V8_ASSET_VERIFIER = (
    "openra_env.learning.apollyon_v8_campaign_runtime."
    "verify_v8_runtime_assets"
)
SPAR_UNCHANGED_READ = "openra_env.analysis._spar_contract._read"
GENERIC_ARTIFACT_RECORD = (
    "scripts.discover_designated_host_execution_binding_runtime_v1."
    "artifact_record"
)
GENERIC_RUNTIME_SNAPSHOT = (
    "scripts.discover_designated_host_execution_binding_runtime_v1."
    "runtime_snapshot"
)

COMMON_AUTHORITY = {
    "filesystem_observation_performed": False,
    "git_query_performed": False,
    "subprocess_execution_performed": False,
    "pip_freeze_performed": False,
    "endpoint_probe_performed": False,
    "systemd_query_performed": False,
    "worktree_created": False,
    "model_weights_loaded": False,
    "runtime_selection_performed": False,
    "runtime_started": False,
    "runtime_execution_authorized": False,
    "game_execution": False,
    "model_execution": False,
    "training": False,
    "weights_updated": False,
    "automatic_policy_promotion": False,
}


class RuntimeObservationPrimitiveReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeObservationPrimitiveReviewHold(message)


def primitive_review(primitive_id: str) -> dict[str, Any]:
    """Return the exact semantic review for one known canonical primitive."""

    if primitive_id == "v8_environment_pure_validator":
        return {
            "schema": PRIMITIVE_SCHEMA,
            "primitive_id": primitive_id,
            "canonical_function": V8_ENVIRONMENT_VALIDATOR,
            "canonical_git_blob": V8_RUNTIME_GIT_BLOB,
            "classification": "admitted_pure_supplied_fact_validator",
            "direct_generation2_reuse_admitted": True,
            "performs_collection": False,
            "performs_filesystem_io": False,
            "performs_subprocess": False,
            "inputs": ("python_major_minor", "pip_freeze_sha256"),
            "claims": (
                "supplied interpreter major/minor equals reviewed V8 identity",
                "supplied pip-freeze SHA-256 equals reviewed V8 identity",
            ),
            "does_not_claim": (
                "how supplied facts were collected",
                "live host identity",
                "runtime readiness",
                "runtime execution authority",
            ),
            "holds": (RUNTIME_AUTHORITY_BLOCKER,),
            "authority": deepcopy(COMMON_AUTHORITY),
        }

    if primitive_id == "v8_environment_live_verifier":
        return {
            "schema": PRIMITIVE_SCHEMA,
            "primitive_id": primitive_id,
            "canonical_function": V8_ENVIRONMENT_LIVE_VERIFIER,
            "canonical_git_blob": V8_RUNTIME_GIT_BLOB,
            "classification": "collection_boundary_not_admitted",
            "direct_generation2_reuse_admitted": False,
            "performs_collection": True,
            "performs_filesystem_io": False,
            "performs_subprocess": True,
            "collection_detail": "executes python -m pip freeze",
            "reason":
                "live subprocess collection requires separate reviewed collector semantics",
            "holds": (
                "V8_LIVE_ENVIRONMENT_COLLECTION_NOT_REVIEWED",
                RUNTIME_AUTHORITY_BLOCKER,
            ),
            "authority": deepcopy(COMMON_AUTHORITY),
        }

    if primitive_id == "v8_asset_runtime_preload_verifier":
        return {
            "schema": PRIMITIVE_SCHEMA,
            "primitive_id": primitive_id,
            "canonical_function": V8_ASSET_VERIFIER,
            "canonical_git_blob": V8_RUNTIME_GIT_BLOB,
            "classification": "runtime_preload_verifier_not_strong_evidence_primitive",
            "direct_generation2_reuse_admitted": False,
            "performs_collection": True,
            "performs_filesystem_io": True,
            "performs_subprocess": False,
            "verified_file_count": 17,
            "loads_model_weights": False,
            "known_strengths": (
                "requires expected file names",
                "rejects symlink at pre-open path check",
                "compares exact SHA-256 for all reviewed files",
                "does not load model weights",
            ),
            "evidence_gaps": (
                "file open does not use O_NOFOLLOW",
                "path check and file open are separate operations",
                "no same-descriptor fstat generation check before and after hashing",
                "no explicit per-file read bound",
            ),
            "reason":
                "retain as existing runtime pre-load verifier but do not use as Generation-2 evidence collector",
            "holds": (
                "V8_STRONG_ASSET_OBSERVER_NOT_REVIEWED",
                RUNTIME_AUTHORITY_BLOCKER,
            ),
            "authority": deepcopy(COMMON_AUTHORITY),
        }

    if primitive_id == "secure_unchanged_regular_file_read_pattern":
        return {
            "schema": PRIMITIVE_SCHEMA,
            "primitive_id": primitive_id,
            "canonical_function": SPAR_UNCHANGED_READ,
            "canonical_git_blob": SPAR_CONTRACT_GIT_BLOB,
            "classification": "admitted_design_reference_only",
            "direct_generation2_reuse_admitted": False,
            "performs_collection": True,
            "performs_filesystem_io": True,
            "performs_subprocess": False,
            "known_strengths": (
                "opens with O_NOFOLLOW",
                "requires bounded regular file",
                "uses same open descriptor for read",
                "fstat identity checked before and after read",
                "rejects changed generation",
            ),
            "limitations": (
                "private helper outside Generation-2 runtime surface",
                "returns bytes rather than a Generation-2 evidence record",
                "does not itself bind an expected SHA-256",
            ),
            "future_design_requirement":
                "Generation-2 strong file observer should preserve this no-follow same-descriptor generation-stability pattern",
            "holds": (
                "GENERATION2_STRONG_FILE_OBSERVER_NOT_IMPLEMENTED",
                RUNTIME_AUTHORITY_BLOCKER,
            ),
            "authority": deepcopy(COMMON_AUTHORITY),
        }

    if primitive_id == "generic_designated_host_artifact_record":
        return {
            "schema": PRIMITIVE_SCHEMA,
            "primitive_id": primitive_id,
            "canonical_function": GENERIC_ARTIFACT_RECORD,
            "canonical_git_blob": DESIGNATED_DISCOVERY_GIT_BLOB,
            "classification": "generic_pattern_not_admitted",
            "direct_generation2_reuse_admitted": False,
            "performs_collection": True,
            "performs_filesystem_io": True,
            "performs_subprocess": False,
            "known_strengths": (
                "lstat before open",
                "rejects symlink",
                "opens with O_NOFOLLOW",
                "compares named path to opened descriptor",
                "hashes opened regular-file descriptor",
            ),
            "evidence_gaps": (
                "no explicit fstat generation comparison after descriptor hashing",
                "generic designated-host semantics are not Generation-2 runtime identity semantics",
            ),
            "holds": (
                "GENERATION2_STRONG_FILE_OBSERVER_NOT_IMPLEMENTED",
                RUNTIME_AUTHORITY_BLOCKER,
            ),
            "authority": deepcopy(COMMON_AUTHORITY),
        }

    if primitive_id == "generic_designated_host_runtime_snapshot":
        return {
            "schema": PRIMITIVE_SCHEMA,
            "primitive_id": primitive_id,
            "canonical_function": GENERIC_RUNTIME_SNAPSHOT,
            "canonical_git_blob": DESIGNATED_DISCOVERY_GIT_BLOB,
            "classification": "partial_git_observation_pattern_not_admitted",
            "direct_generation2_reuse_admitted": False,
            "performs_collection": True,
            "performs_filesystem_io": True,
            "performs_subprocess": True,
            "known_strengths": (
                "requires resolved repository path identity",
                "collects HEAD commit",
                "collects full worktree dirty status",
                "supports exact tracked blob queries",
                "Git runner is injectable for tests",
            ),
            "v2r13_gaps": (
                "does not collect HEAD^{tree}",
                "does not prove frozen source detached HEAD",
                "generic binding shape is not V2R13 evidence schema",
            ),
            "holds": (
                "V2R13_GIT_METADATA_OBSERVER_NOT_IMPLEMENTED",
                RUNTIME_AUTHORITY_BLOCKER,
            ),
            "authority": deepcopy(COMMON_AUTHORITY),
        }

    raise RuntimeObservationPrimitiveReviewHold(
        f"unknown observation primitive: {primitive_id!r}"
    )


def observation_primitive_review_contract() -> dict[str, Any]:
    """Return the reviewed candidate set and exact admission boundary."""
    ids = (
        "v8_environment_pure_validator",
        "v8_environment_live_verifier",
        "v8_asset_runtime_preload_verifier",
        "secure_unchanged_regular_file_read_pattern",
        "generic_designated_host_artifact_record",
        "generic_designated_host_runtime_snapshot",
    )
    reviews = [primitive_review(value) for value in ids]

    v8_paths = path_input_requirement(V8)
    v2_paths = path_input_requirement(V2R13)
    _require(
        v8_paths["source_kind"] == "explicit_external_input",
        "V8 path-input source drift",
    )
    _require(
        v2_paths["source_kind"] == "explicit_external_input",
        "V2R13 path-input source drift",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "observation_primitive_census_sha256":
            OBSERVATION_PRIMITIVE_CENSUS_SHA256,
        "review_count": len(reviews),
        "reviews": reviews,
        "direct_generation2_reuse_admitted": (
            "v8_environment_pure_validator",
        ),
        "design_reference_only": (
            "secure_unchanged_regular_file_read_pattern",
        ),
        "collection_boundary_unadmitted": (
            "v8_environment_live_verifier",
            "v8_asset_runtime_preload_verifier",
            "generic_designated_host_artifact_record",
            "generic_designated_host_runtime_snapshot",
        ),
        "v14_identity_observation_still_unresolved":
            not observation_mechanics(V14)["collector_implementation_ready"],
        "v10_identity_observation_still_unresolved":
            not observation_mechanics(V10)["collector_implementation_ready"],
        "v2r13_git_observer_implemented": False,
        "v8_strong_asset_observer_implemented": False,
        "collector_implementation_ready": False,
        "runtime_execution_authorized": False,
        "authority": deepcopy(COMMON_AUTHORITY),
    }


def future_file_observer_requirements() -> dict[str, Any]:
    """Define semantic requirements only; do not implement a file observer."""
    return {
        "open_final_component_with_no_follow": True,
        "require_regular_file": True,
        "same_descriptor_read_and_hash": True,
        "fstat_before_read": True,
        "fstat_after_read": True,
        "generation_identity_stable": True,
        "explicit_maximum_bytes": True,
        "compare_expected_sha256": True,
        "symlink_acceptance": False,
        "model_load_permitted": False,
        "implemented": False,
    }


def future_v2r13_git_observer_requirements() -> dict[str, Any]:
    """Define exact V2R13 Git facts required from explicit pre-existing roots."""
    return {
        "explicit_external_roots_only": True,
        "resolve_strict_and_reject_alias_or_symlink": True,
        "source_head_commit": True,
        "source_head_tree": True,
        "source_clean_full_worktree": True,
        "source_detached_head": True,
        "engine_head_commit": True,
        "engine_clean_full_worktree": True,
        "worktree_creation_permitted": False,
        "canonical_checkout_mutation_permitted": False,
        "implemented": False,
    }


def execute_observation_primitive(*args: Any, **kwargs: Any) -> None:
    """Always hold: this semantic-review contract performs no collection."""
    raise RuntimeObservationPrimitiveReviewHold(
        "GENERATION2_OBSERVATION_PRIMITIVE_EXECUTION_NOT_IMPLEMENTED: "
        "semantic review is source-only"
    )
