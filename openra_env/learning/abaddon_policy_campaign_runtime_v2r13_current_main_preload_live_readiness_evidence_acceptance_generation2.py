"""Source-only acceptance of exact current-main V2R13 live-readiness evidence.

This instrument accepts one externally completed V2R13 model-only preload plus
canonical read-only live collection that was bound to the exact current
Generation-2 main head/tree.  It pins the complete evidence summary and its
canonical SHA-256, reconciles that fresh readiness with the already accepted
execution-materialization source frontier, and advances only the V2R13 lane to
the explicit runtime-execution authorization gate.

This source performs no preload, model load, live observation, HTTP request,
Docker command, filesystem/Git observation, service action, inference, game
execution, training, deployment, VOID-chain mutation, or funds action.
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_isolated_workdir_allocator_source_binding_review_generation2
    as allocator_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_entrypoint_binding_generation2
    as entrypoint_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_invocation_acceptance_generation2
    as prior_acceptance,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    RUNTIME_AUTHORITY_BLOCKER,
    V2R13,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-current-main-preload-live-readiness-evidence-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-current-main-preload-live-readiness-evidence-acceptance.v1"
)

CURRENT_MAIN_HEAD = "138b121419328d3db79b080dbd9300a4227f3e99"
CURRENT_MAIN_TREE = "200b88ede3913218208ada4171db6d444c97cf28"

ENTRYPOINT_BINDING_GIT_BLOB = "3950bbdd68f2fdc089f596f8159d480699af9982"
ENTRYPOINT_BINDING_SOURCE_SHA256 = (
    "06c5a110401b05631eb64496cee7b2d7e56378a9376c9d0c4fd1db015c6308f1"
)
PRIOR_ACCEPTANCE_GIT_BLOB = "1ced66b86edbda59b33bdc25a185842d7bd71418"
PRIOR_ACCEPTANCE_SOURCE_SHA256 = (
    "2a883510806ac6123c7e8bb6a2289f6d3d0dd501bb5aed0e738c435e7eda3045"
)
ALLOCATOR_REVIEW_GIT_BLOB = "a1fb192ce13030f814da74d12bc930968e77d765"
ALLOCATOR_REVIEW_SOURCE_SHA256 = (
    "3985b0fbc74a25e29d44ae09d9c52c051ebb9044058d1bdd93ba6c9d1cca5761"
)

PRIOR_ACCEPTED_EVIDENCE_SHA256 = (
    "68465b443ab483a1b00db6f947dc87b51231fe1f9ce8434a105e6a0416e5d788"
)
ACCEPTED_EVIDENCE_SHA256 = (
    "ee5c9c555323fc0a0b6550953700ec033ad2f4bb9d8b8763c5f59bfdb9bf91d2"
)
EXPECTED_ACCEPTED_EVIDENCE = {'bound_live_receipt_validation_green': True, 'bound_validation_sha256': 'afda05a169f0848ab94900283935caf1a367a9f1719884fee5b18514815ab6e9', 'canonical_collection_enabled': False, 'canonical_live_collection_path_complete': True, 'canonical_main_head': '138b121419328d3db79b080dbd9300a4227f3e99', 'canonical_main_tree': '200b88ede3913218208ada4171db6d444c97cf28', 'canonical_receipt_model_load_performed': False, 'chat_completions_request_performed': False, 'collector_identity_admitted': True, 'deployment_performed': False, 'docker_context_stdout_sha256': '107f714d1bab1ecae968808edfe5f6570b07c717da8ced0e42fb5eaad832a818', 'docker_image_inspect_stdout_sha256': 'cb147df77f290ebfce9b997496a1d725e6851ee37ae728f7cecc52dbf1177fba', 'docker_info_stdout_sha256': '17b5a2caeb80a253b74fc7ec3d978c949cd10fe09a73bfec022ed62b2a0e0008', 'docker_mutating_command_performed': False, 'entrypoint_receipt_sha256': '41948e77f3b2f937959acfb4a8215f2dd69f5f167f7ac33d3c84ad436fa07f09', 'exact_model_preload_green': True, 'exact_three_docker_metadata_commands_green': True, 'exact_two_ollama_gets_green': True, 'game_execution_performed': False, 'launcher_model_load_performed': True, 'launcher_sha256': 'a76f0542c01de015a2f838e119f1bcb461fd17c063725c7cfd123a5271fa8d82', 'live_observation_performed': True, 'model_inference_performed': False, 'ollama_ps_body_sha256': '0e1723538f8c987908136cc882a43b53ba22569a1546f227fa2f13e455785c52', 'ollama_tags_body_sha256': '119d0ca767aa571ddf514dcfdf4a400e755e28543b1d54e541949ca07bc92a8b', 'preload_body_sha256': '1ddc04745c6310fa1a4ae71dd4a46a3d21c9157a795669b89646a662881c07ef', 'preload_generated_response_text_observed': False, 'preload_prompt_supplied': False, 'provider_capability_remaining_unresolved': 0, 'provider_capability_supported_primitives': 16, 'runtime_execution_authorized': False, 'runtime_readiness_admitted': True, 'training_performed': False, 'void_chain_mutation_performed': False, 'wallet_or_funds_action_performed': False, 'weights_updated': False}
EXPECTED_ACCEPTED_EVIDENCE_FIELDS = frozenset(EXPECTED_ACCEPTED_EVIDENCE)

FUTURE_COLLECTION_GATE = (
    "V2R13_CANONICAL_LIVE_COLLECTION_INVOCATION_AUTHORIZATION_REQUIRED"
)
NEXT_GATE = RUNTIME_AUTHORITY_BLOCKER
NEXT_GATE_SCOPE = "v2r13_lane_only"


class RuntimeV2R13CurrentMainLiveReadinessEvidenceAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13CurrentMainLiveReadinessEvidenceAcceptanceHold(message)


def _canonical_sha256(value: Any) -> str:
    raw = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _validate_dependencies() -> dict[str, Any]:
    bound = (
        entrypoint_binding
        .v2r13_canonical_live_collection_entrypoint_binding_contract()
    )
    prior = (
        prior_acceptance
        .v2r13_canonical_live_collection_invocation_acceptance_contract()
    )
    execution = (
        allocator_review
        .isolated_workdir_allocator_source_binding_review_contract()
    )

    _require(
        bound.get("canonical_live_collection_entrypoint_source_binding_present")
        is True,
        "V2R13 entrypoint source binding missing",
    )
    _require(
        bound.get("canonical_live_collection_path_complete") is True,
        "V2R13 canonical live-collection path incomplete",
    )
    _require(
        bound.get("canonical_collection_enabled") is False,
        "V2R13 canonical collection unexpectedly enabled",
    )
    _require(
        bound.get("runtime_execution_authorized") is False,
        "V2R13 entrypoint unexpectedly authorizes runtime execution",
    )
    _require(
        bound.get("next_gate") == FUTURE_COLLECTION_GATE,
        "V2R13 entrypoint binding next-gate drift",
    )

    _require(
        prior.get("canonical_live_collection_invocation_accepted") is True,
        "prior V2R13 accepted invocation missing",
    )
    _require(
        prior.get("accepted_evidence_sha256") == PRIOR_ACCEPTED_EVIDENCE_SHA256,
        "prior accepted evidence identity drift",
    )
    _require(
        prior.get("runtime_readiness_admitted") is True,
        "prior V2R13 readiness admission missing",
    )
    _require(
        prior.get("future_live_collection_requires_fresh_explicit_authorization")
        is True,
        "fresh collection authority requirement lost",
    )
    _require(
        prior.get("runtime_execution_authorized") is False,
        "prior acceptance unexpectedly authorizes runtime",
    )

    _require(
        execution.get("source_frontier_closed") is True,
        "execution materialization source frontier reopened",
    )
    _require(
        tuple(execution.get("execution_materialization_source_blockers", ())) == (),
        "execution materialization source blocker drift",
    )
    _require(
        tuple(execution.get("execution_materialization_blockers", ()))
        == (RUNTIME_AUTHORITY_BLOCKER,),
        "execution materialization blocker frontier drift",
    )
    _require(
        execution.get("next_gate") == RUNTIME_AUTHORITY_BLOCKER,
        "execution materialization next-gate drift",
    )
    _require(
        execution.get("runtime_execution_authorized") is False,
        "execution materialization unexpectedly authorizes runtime",
    )

    return {
        "entrypoint_binding": deepcopy(bound),
        "prior_live_invocation_acceptance": deepcopy(prior),
        "execution_materialization_review": deepcopy(execution),
    }


def _validate_exact_evidence(evidence: Mapping[str, Any]) -> dict[str, Any]:
    _require(
        isinstance(evidence, Mapping),
        "current-main V2R13 readiness evidence must be object",
    )
    _require(
        set(evidence) == EXPECTED_ACCEPTED_EVIDENCE_FIELDS,
        "current-main V2R13 readiness evidence field-set drift",
    )
    for field, expected in EXPECTED_ACCEPTED_EVIDENCE.items():
        actual = evidence.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"current-main V2R13 readiness evidence drift: {field}",
        )

    copied = deepcopy(dict(evidence))
    _require(
        _canonical_sha256(copied) == ACCEPTED_EVIDENCE_SHA256,
        "current-main V2R13 readiness evidence SHA drift",
    )
    return copied


def accept_current_main_v2r13_live_readiness_evidence(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    """Accept exact supplied evidence without performing any live action."""
    dependencies = _validate_dependencies()
    accepted = _validate_exact_evidence(evidence)

    return {
        "schema": ACCEPTANCE_SCHEMA,
        "snapshot_id": V2R13,
        "current_main_head": CURRENT_MAIN_HEAD,
        "current_main_tree": CURRENT_MAIN_TREE,
        "current_main_preload_live_readiness_evidence_accepted": True,
        "accepted_evidence_sha256": ACCEPTED_EVIDENCE_SHA256,
        "evidence_bound_to_current_main": True,
        "accepted_current_main_live_invocation_count": 1,
        "prior_accepted_live_invocation_count": 1,
        "total_accepted_live_invocation_count": 2,
        "live_observation_evidence_pinned": True,
        "external_launcher_model_load_performed": True,
        "accepted_preload_prompt_supplied": False,
        "accepted_preload_generated_response_text_observed": False,
        "provider_capability_supported_primitive_count": 16,
        "provider_capability_remaining_unresolved_primitive_count": 0,
        "provider_capability_complete": True,
        "collector_identity_admitted": True,
        "runtime_readiness_admitted": True,
        "execution_materialization_source_frontier_closed": True,
        "canonical_live_collection_path_complete": True,
        "canonical_collection_enabled": False,
        "automatic_canonical_collection_enabled": False,
        "future_live_collection_requires_fresh_explicit_authorization": True,
        "acceptance_performs_model_load": False,
        "acceptance_performs_live_observation": False,
        "acceptance_performs_http_request": False,
        "acceptance_performs_ollama_request": False,
        "acceptance_performs_docker_command": False,
        "acceptance_performs_git_query": False,
        "acceptance_performs_filesystem_observation": False,
        "acceptance_performs_systemd_action": False,
        "runtime_activation_performed": False,
        "runtime_execution_authorized": False,
        "runtime_execution_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "policy_promotion_performed": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "runtime_execution_authorization_scope": NEXT_GATE_SCOPE,
        "other_runtime_lanes_readiness_implied": False,
        "next_gate": NEXT_GATE,
        "future_collection_gate": FUTURE_COLLECTION_GATE,
        "holds": [NEXT_GATE],
        "accepted_evidence": accepted,
        "dependencies": dependencies,
    }


def current_main_v2r13_live_readiness_evidence_acceptance_contract() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    _require(
        _canonical_sha256(EXPECTED_ACCEPTED_EVIDENCE) == ACCEPTED_EVIDENCE_SHA256,
        "embedded current-main evidence SHA drift",
    )

    return {
        "schema": CONTRACT_SCHEMA,
        "snapshot_id": V2R13,
        "current_main_head": CURRENT_MAIN_HEAD,
        "current_main_tree": CURRENT_MAIN_TREE,
        "entrypoint_binding_git_blob": ENTRYPOINT_BINDING_GIT_BLOB,
        "entrypoint_binding_source_sha256": ENTRYPOINT_BINDING_SOURCE_SHA256,
        "prior_acceptance_git_blob": PRIOR_ACCEPTANCE_GIT_BLOB,
        "prior_acceptance_source_sha256": PRIOR_ACCEPTANCE_SOURCE_SHA256,
        "allocator_review_git_blob": ALLOCATOR_REVIEW_GIT_BLOB,
        "allocator_review_source_sha256": ALLOCATOR_REVIEW_SOURCE_SHA256,
        "prior_accepted_evidence_sha256": PRIOR_ACCEPTED_EVIDENCE_SHA256,
        "accepted_evidence_sha256": ACCEPTED_EVIDENCE_SHA256,
        "expected_accepted_evidence": deepcopy(EXPECTED_ACCEPTED_EVIDENCE),
        "current_main_preload_live_readiness_evidence_accepted": True,
        "evidence_bound_to_current_main": True,
        "accepted_current_main_live_invocation_count": 1,
        "prior_accepted_live_invocation_count": 1,
        "total_accepted_live_invocation_count": 2,
        "acceptance_validator_implemented": True,
        "acceptance_performs_model_load": False,
        "acceptance_performs_live_observation": False,
        "acceptance_performs_http_request": False,
        "acceptance_performs_ollama_request": False,
        "acceptance_performs_docker_command": False,
        "acceptance_performs_git_query": False,
        "acceptance_performs_filesystem_observation": False,
        "acceptance_performs_systemd_action": False,
        "external_launcher_model_load_performed": True,
        "accepted_preload_prompt_supplied": False,
        "accepted_preload_generated_response_text_observed": False,
        "provider_capability_supported_primitive_count": 16,
        "provider_capability_remaining_unresolved_primitive_count": 0,
        "provider_capability_complete": True,
        "collector_identity_admitted": True,
        "runtime_readiness_admitted": True,
        "execution_materialization_source_frontier_closed": True,
        "canonical_live_collection_path_complete": True,
        "canonical_collection_enabled": False,
        "automatic_canonical_collection_enabled": False,
        "future_live_collection_requires_fresh_explicit_authorization": True,
        "runtime_activation_performed": False,
        "runtime_execution_authorized": False,
        "runtime_execution_performed": False,
        "model_inference_implemented": False,
        "game_execution_implemented": False,
        "training_implemented": False,
        "deployment_implemented": False,
        "void_chain_mutation_implemented": False,
        "wallet_or_funds_action_implemented": False,
        "runtime_execution_authorization_scope": NEXT_GATE_SCOPE,
        "other_runtime_lanes_readiness_implied": False,
        "next_gate": NEXT_GATE,
        "future_collection_gate": FUTURE_COLLECTION_GATE,
        "holds": [NEXT_GATE],
        "dependencies": dependencies,
    }


def request_additional_live_collection(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13CurrentMainLiveReadinessEvidenceAcceptanceHold(
        FUTURE_COLLECTION_GATE
    )


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13CurrentMainLiveReadinessEvidenceAcceptanceHold(NEXT_GATE)
