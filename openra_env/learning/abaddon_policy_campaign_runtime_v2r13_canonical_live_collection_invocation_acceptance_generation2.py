"""Source-only acceptance for one exact V2R13 canonical live-collection invocation.

This instrument admits exactly one previously completed, externally supplied
live-collection evidence summary.  It performs no live observation and does not
invoke Ollama, Docker, Git, systemd, model inference, game execution, training,
deployment, VOID-chain mutation, or wallet/funds actions.

Acceptance of this one evidence record does not enable automatic collection and
does not authorize runtime execution.  Any future live collection still requires
fresh explicit authorization.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_canonical_live_collection_entrypoint_binding_generation2
    as entrypoint_binding,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    RUNTIME_AUTHORITY_BLOCKER,
    V2R13,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-canonical-live-collection-invocation-acceptance-contract.v1"
)
ACCEPTANCE_SCHEMA = (
    "void.abaddon.generation2."
    "v2r13-canonical-live-collection-invocation-acceptance.v1"
)

ENTRYPOINT_BINDING_GIT_BLOB = "3950bbdd68f2fdc089f596f8159d480699af9982"
ENTRYPOINT_BINDING_SOURCE_SHA256 = (
    "06c5a110401b05631eb64496cee7b2d7e56378a9376c9d0c4fd1db015c6308f1"
)

ACCEPTED_EVIDENCE_SHA256 = "68465b443ab483a1b00db6f947dc87b51231fe1f9ce8434a105e6a0416e5d788"
EXPECTED_ACCEPTED_EVIDENCE = {'canonical_main_head': '94130a47e3d0f118331c7fbfd8be5b5092d7138c', 'canonical_main_tree': 'ac90ee3652bd170b49122c34de4ae9060c6a57c1', 'launcher_sha256': 'd590039b3274c933ab67af311b17d3394d78f0f36ab44c788a3964831fefc8d2', 'preload_body_sha256': '347ba4f9e512784469fc36522a277ab67d888d105f04412e0a5c6a4947483378', 'ollama_tags_body_sha256': '119d0ca767aa571ddf514dcfdf4a400e755e28543b1d54e541949ca07bc92a8b', 'ollama_ps_body_sha256': '86f32105e624b7486dce6264fdd515789ee3a9e520c7b33704532bafb82662c1', 'docker_context_stdout_sha256': '107f714d1bab1ecae968808edfe5f6570b07c717da8ced0e42fb5eaad832a818', 'docker_info_stdout_sha256': '6f48856a6248ee95e7390ce947f7ec81742503a60359f3ec54d6a45afafea374', 'docker_image_inspect_stdout_sha256': 'cb147df77f290ebfce9b997496a1d725e6851ee37ae728f7cecc52dbf1177fba', 'entrypoint_receipt_sha256': '41948e77f3b2f937959acfb4a8215f2dd69f5f167f7ac33d3c84ad436fa07f09', 'bound_validation_sha256': 'afda05a169f0848ab94900283935caf1a367a9f1719884fee5b18514815ab6e9', 'exact_two_ollama_gets_green': True, 'exact_three_docker_metadata_commands_green': True, 'bound_live_receipt_validation_green': True, 'live_observation_performed': True, 'provider_capability_supported_primitives': 16, 'provider_capability_remaining_unresolved': 0, 'collector_identity_admitted': True, 'runtime_readiness_admitted': True, 'launcher_model_load_performed': True, 'canonical_receipt_model_load_performed': False, 'preload_prompt_supplied': False, 'preload_generated_response_text_observed': False, 'chat_completions_request_performed': False, 'docker_mutating_command_performed': False, 'model_inference_performed': False, 'game_execution_performed': False, 'training_performed': False, 'weights_updated': False, 'deployment_performed': False, 'void_chain_mutation_performed': False, 'wallet_or_funds_action_performed': False, 'canonical_live_collection_path_complete': True, 'canonical_collection_enabled': False, 'runtime_execution_authorized': False, 'post_live_worktree_green': True}
EXPECTED_ACCEPTED_EVIDENCE_FIELDS = frozenset(EXPECTED_ACCEPTED_EVIDENCE)

NEXT_GATE = "V2R13_ACTIVATION_BINDING_REVIEW_REQUIRED"
FUTURE_COLLECTION_GATE = (
    "V2R13_CANONICAL_LIVE_COLLECTION_INVOCATION_AUTHORIZATION_REQUIRED"
)


class RuntimeV2R13CanonicalLiveCollectionInvocationAcceptanceHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13CanonicalLiveCollectionInvocationAcceptanceHold(message)


def _validate_dependency_contract() -> dict[str, Any]:
    bound = (
        entrypoint_binding
        .v2r13_canonical_live_collection_entrypoint_binding_contract()
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
        "V2R13 runtime execution unexpectedly authorized",
    )
    _require(
        bound.get("next_gate") == FUTURE_COLLECTION_GATE,
        "V2R13 entrypoint binding next-gate drift",
    )
    return deepcopy(bound)


def _validate_exact_evidence(evidence: Mapping[str, Any]) -> dict[str, Any]:
    _require(
        isinstance(evidence, Mapping),
        "V2R13 accepted invocation evidence must be object",
    )
    _require(
        set(evidence) == EXPECTED_ACCEPTED_EVIDENCE_FIELDS,
        "V2R13 accepted invocation evidence field-set drift",
    )

    for field, expected in EXPECTED_ACCEPTED_EVIDENCE.items():
        actual = evidence.get(field)
        _require(
            type(actual) is type(expected) and actual == expected,
            f"V2R13 accepted invocation evidence drift: {field}",
        )

    return deepcopy(dict(evidence))


def accept_v2r13_canonical_live_collection_invocation(
    evidence: Mapping[str, Any],
) -> dict[str, Any]:
    """Accept the exact reviewed invocation evidence without re-observation."""
    dependency = _validate_dependency_contract()
    accepted = _validate_exact_evidence(evidence)

    return {
        "schema": ACCEPTANCE_SCHEMA,
        "snapshot_id": V2R13,
        "canonical_live_collection_invocation_accepted": True,
        "accepted_live_invocation_count": 1,
        "accepted_evidence_sha256": ACCEPTED_EVIDENCE_SHA256,
        "live_observation_evidence_pinned": True,
        "provider_capability_supported_primitive_count": 16,
        "provider_capability_remaining_unresolved_primitive_count": 0,
        "provider_capability_complete": True,
        "collector_identity_admitted": True,
        "runtime_readiness_admitted": True,
        "canonical_live_collection_path_complete": True,
        "canonical_collection_enabled": False,
        "automatic_canonical_collection_enabled": False,
        "future_live_collection_requires_fresh_explicit_authorization": True,
        "runtime_execution_authorized": False,
        "runtime_activation_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "policy_promotion_performed": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "next_gate": NEXT_GATE,
        "holds": [NEXT_GATE, RUNTIME_AUTHORITY_BLOCKER],
        "accepted_evidence": accepted,
        "dependency_contract": dependency,
    }


def v2r13_canonical_live_collection_invocation_acceptance_contract() -> dict[str, Any]:
    dependency = _validate_dependency_contract()
    return {
        "schema": CONTRACT_SCHEMA,
        "snapshot_id": V2R13,
        "entrypoint_binding_git_blob": ENTRYPOINT_BINDING_GIT_BLOB,
        "entrypoint_binding_source_sha256": ENTRYPOINT_BINDING_SOURCE_SHA256,
        "accepted_evidence_sha256": ACCEPTED_EVIDENCE_SHA256,
        "expected_accepted_evidence": deepcopy(EXPECTED_ACCEPTED_EVIDENCE),
        "accepted_live_invocation_count": 1,
        "acceptance_validator_implemented": True,
        "acceptance_performs_live_observation": False,
        "acceptance_performs_http_request": False,
        "acceptance_performs_ollama_request": False,
        "acceptance_performs_docker_command": False,
        "acceptance_performs_git_query": False,
        "acceptance_performs_systemd_action": False,
        "canonical_live_collection_invocation_accepted": True,
        "provider_capability_supported_primitive_count": 16,
        "provider_capability_remaining_unresolved_primitive_count": 0,
        "provider_capability_complete": True,
        "collector_identity_admitted": True,
        "runtime_readiness_admitted": True,
        "canonical_live_collection_path_complete": True,
        "canonical_collection_enabled": False,
        "automatic_canonical_collection_enabled": False,
        "future_live_collection_requires_fresh_explicit_authorization": True,
        "runtime_execution_authorized": False,
        "runtime_activation_performed": False,
        "model_inference_implemented": False,
        "game_execution_implemented": False,
        "training_implemented": False,
        "deployment_implemented": False,
        "void_chain_mutation_implemented": False,
        "wallet_or_funds_action_implemented": False,
        "next_gate": NEXT_GATE,
        "future_collection_gate": FUTURE_COLLECTION_GATE,
        "holds": [NEXT_GATE, RUNTIME_AUTHORITY_BLOCKER],
        "dependency_contract": dependency,
    }


def request_additional_live_collection(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13CanonicalLiveCollectionInvocationAcceptanceHold(
        FUTURE_COLLECTION_GATE
    )


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13CanonicalLiveCollectionInvocationAcceptanceHold(
        RUNTIME_AUTHORITY_BLOCKER
    )
