"""Source-only binding for the reviewed Generation-2 V2R13 collector implementation.

The collector implementation was merged before this file exists. This separate
binding instrument pins that implementation without self-reference by both
canonical Git blob and reviewed source SHA-256.

It also closes the enumerated per-primitive source-binding gap by mapping the
collector's exact 16 V2R13 primitive names to already-reviewed provider or
validator source identities.

This source does not invoke a provider, collect evidence, select a host backend,
perform live observation, enable canonical collection, admit collector identity,
admit runtime readiness, or authorize runtime execution.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_activation_evidence_generation2
    as activation_evidence,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_collector_contract_generation2
    as collector_contract,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_collector_implementation_generation2
    as collector_implementation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_primitive_provider_source_only_generation2
    as source_only_provider,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_worktree_provider_adapter_generation2
    as worktree_provider,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_portable_binding_attestation_generation2
    as portable_attestation,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_rootless_docker_image_backend_binding_generation2
    as runtime_image_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_ollama_observer_binding_generation2
    as ollama_binding,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_collector_reconciliation_generation2
    as reconciliation,
)
from openra_env.learning.abaddon_policy_campaign_runtime_activation_contract_generation2 import (
    V2R13,
)

CONTRACT_SCHEMA = (
    'void.abaddon.generation2.v2r13-collector-implementation-binding-contract.v1'
)

ACTIVATION_EVIDENCE_GIT_BLOB = 'aac7964d9e80633535003b9f27066cac1bb4bac2'
COLLECTOR_CONTRACT_GIT_BLOB = '8014431ad5329137e5ce12334d19d37c877a0b52'
COLLECTOR_IMPLEMENTATION_GIT_BLOB = '0003c24390194a4f621f13c6077e0604b9abcd98'
SOURCE_ONLY_PROVIDER_GIT_BLOB = 'f3b48e624172aeed81e28a6e24508533b7b13661'
WORKTREE_PROVIDER_GIT_BLOB = '7e6f628c64fe02db42bd6adee67d3965e6b1ae92'
PORTABLE_ATTESTATION_GIT_BLOB = 'afdc0421958565e713795dfd0d3c4c683041cc37'
RUNTIME_IMAGE_BINDING_GIT_BLOB = '7075ded7a19454239b95a09e7b4630413124a796'
OLLAMA_BINDING_GIT_BLOB = '58364a1d5d71aead9df6dc0fc61661a557131508'
RECONCILIATION_GIT_BLOB = '6c7dee5f94d32623cd7158868690fe0ac1d0c0c0'

COLLECTOR_IMPLEMENTATION_SOURCE_SHA256 = '91e094c71b838ad8116dced00fbc50b3e8a8bd138f75dfb5ae86b9bf5c97a8dc'
SOURCE_ONLY_PROVIDER_SOURCE_SHA256 = 'daa038f17d3103cd0644303d40fd37a060ec51d1a6c68ac5d91555897eeb1a81'
WORKTREE_PROVIDER_SOURCE_SHA256 = '172dbb3acc3d9f34a64acd68f3bee58ae30336ad2802fd1dfbf9597bf8105522'
PORTABLE_ATTESTATION_SOURCE_SHA256 = 'c480af5b439b4c68b24f5bb68bdce1948f215eda3e847e8631a43e8eacbac818'
RUNTIME_IMAGE_BINDING_SOURCE_SHA256 = '74acc7248ee19d2d141aa4ec36fc3ce1c6068c56ca1801719c3287cd2c774f52'
OLLAMA_BINDING_SOURCE_SHA256 = 'c6b0bb746d017326e600f401a2d07a29fba79aced401687c4eb5238084ee9335'
RECONCILIATION_SOURCE_SHA256 = 'f1c6009735be69a86d77bf1c9ac2fe911bbac97c06076395c6656ce94fa76b86'

COMMON_PRIMITIVES = (
    'observation_mode',
    'mutation_performed',
    'service_action_performed',
    'runtime_start_performed',
    'game_execution_performed',
    'model_inference_performed',
)
OLLAMA_PRIMITIVES = ('endpoint_liveness', 'model_identity_verified')
RUNTIME_IMAGE_PRIMITIVES = ('runtime_image_identity_verified',)
WORKTREE_PRIMITIVES = (
    'frozen_source_worktree.exists',
    'frozen_source_worktree.is_directory',
    'frozen_source_worktree.is_symlink',
    'engine_worktree.exists',
    'engine_worktree.is_directory',
    'engine_worktree.is_symlink',
)
PORTABLE_PRIMITIVES = ('portable_binding_attested',)

PRIMITIVE_SOURCE_BINDINGS = {
    **{name: SOURCE_ONLY_PROVIDER_SOURCE_SHA256 for name in COMMON_PRIMITIVES},
    **{name: OLLAMA_BINDING_SOURCE_SHA256 for name in OLLAMA_PRIMITIVES},
    **{name: RUNTIME_IMAGE_BINDING_SOURCE_SHA256 for name in RUNTIME_IMAGE_PRIMITIVES},
    **{name: WORKTREE_PROVIDER_SOURCE_SHA256 for name in WORKTREE_PRIMITIVES},
    **{name: PORTABLE_ATTESTATION_SOURCE_SHA256 for name in PORTABLE_PRIMITIVES},
}


class RuntimeV2R13CollectorImplementationBindingHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13CollectorImplementationBindingHold(message)


def _validate_dependencies() -> dict[str, Any]:
    historical = collector_contract.validate_collector_contract()
    implementation = collector_implementation.collector_implementation_contract()
    source_only = source_only_provider.source_only_provider_contract()
    worktree = worktree_provider.v2r13_worktree_provider_adapter_contract()
    portable = portable_attestation.v2r13_portable_binding_attestation_contract()
    image = runtime_image_binding.v2r13_rootless_docker_image_backend_binding_contract()
    ollama = ollama_binding.v2r13_ollama_observer_binding_contract()
    reconciled = reconciliation.v2r13_collector_reconciliation_contract()

    _require(
        historical.get('implementation_source_binding_required_before_activation') is True,
        'collector implementation source-binding requirement lost',
    )
    _require(
        historical.get('implementation_source_sha256') is None,
        'historical collector contract unexpectedly self-pins implementation',
    )
    _require(
        implementation.get('injected_primitive_orchestration_implemented') is True,
        'collector injected primitive orchestration missing',
    )
    _require(
        implementation.get('primitive_receipt_source_binding_enforced') is True,
        'collector primitive source-binding enforcement missing',
    )
    _require(
        implementation.get('canonical_primitive_source_bindings_present') is False,
        'collector implementation unexpectedly self-binds primitive sources',
    )

    required = tuple(collector_implementation.required_primitive_names(V2R13))
    _require(
        required == tuple(PRIMITIVE_SOURCE_BINDINGS),
        'collector required primitive ordering/source-binding map drift',
    )
    _require(
        len(required) == 16 and len(set(required)) == 16,
        'collector required primitive set is not exact 16',
    )

    _require(
        source_only.get('common_self_audit_provider_implemented') is True,
        'source-only common provider missing',
    )
    _require(
        worktree.get('six_worktree_primitives_implemented') is True,
        'worktree provider does not implement six collector leaves',
    )
    _require(
        portable.get('supplied_attestation_validator_implemented') is True,
        'portable attestation validator missing',
    )
    _require(
        image.get('runtime_image_identity_provider_primitive_implemented') is True,
        'runtime-image provider primitive missing',
    )
    _require(
        ollama.get('endpoint_liveness_provider_primitive_implemented') is True,
        'endpoint-liveness provider primitive missing',
    )
    _require(
        ollama.get('model_identity_provider_primitive_implemented') is True,
        'model-identity provider primitive missing',
    )
    _require(
        ollama.get('supported_primitive_count_after_binding') == 16,
        'V2R13 provider supported count drift',
    )
    _require(
        ollama.get('remaining_unresolved_primitive_count') == 0,
        'V2R13 provider unresolved count drift',
    )
    _require(
        reconciled.get('historical_future_provider_gap_closed') is True,
        'V2R13 reconciliation no longer closes historical provider gap',
    )
    _require(
        reconciled.get('collector_implementation_source_binding_present') is False,
        'reconciliation unexpectedly claims collector implementation binding',
    )
    _require(
        activation_evidence.REVIEWED_COLLECTOR_BINDING_PRESENT is False,
        'activation evidence collector binding unexpectedly active',
    )

    for contract_name, contract in (
        ('implementation', implementation),
        ('source_only', source_only),
        ('worktree', worktree),
        ('portable', portable),
        ('image', image),
        ('ollama', ollama),
        ('reconciliation', reconciled),
    ):
        _require(
            contract.get('runtime_execution_authorized') is False,
            f'{contract_name} dependency unexpectedly authorizes runtime',
        )
        if 'canonical_collection_enabled' in contract:
            _require(
                contract.get('canonical_collection_enabled') is False,
                f'{contract_name} dependency unexpectedly enables collection',
            )

    return {
        'historical_collector_contract': deepcopy(historical),
        'collector_implementation': deepcopy(implementation),
        'source_only_provider': deepcopy(source_only),
        'worktree_provider': deepcopy(worktree),
        'portable_attestation': deepcopy(portable),
        'runtime_image_binding': deepcopy(image),
        'ollama_binding': deepcopy(ollama),
        'reconciliation': deepcopy(reconciled),
    }


def reviewed_v2r13_primitive_source_bindings() -> dict[str, str]:
    _validate_dependencies()
    return deepcopy(PRIMITIVE_SOURCE_BINDINGS)


def v2r13_collector_implementation_binding_contract() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    bindings = reviewed_v2r13_primitive_source_bindings()
    return {
        'schema': CONTRACT_SCHEMA,
        'snapshot_id': V2R13,
        'activation_evidence_git_blob': ACTIVATION_EVIDENCE_GIT_BLOB,
        'collector_contract_git_blob': COLLECTOR_CONTRACT_GIT_BLOB,
        'collector_implementation_git_blob': COLLECTOR_IMPLEMENTATION_GIT_BLOB,
        'collector_implementation_source_sha256': COLLECTOR_IMPLEMENTATION_SOURCE_SHA256,
        'collector_implementation_source_binding_present': True,
        'collector_implementation_source_identity_pinned_by_git_blob': True,
        'collector_implementation_source_identity_pinned_by_sha256': True,
        'collector_implementation_source_is_not_self_bound': True,
        'primitive_source_bindings': bindings,
        'primitive_source_binding_count': len(bindings),
        'primitive_source_binding_names': tuple(bindings),
        'canonical_primitive_source_bindings_present': True,
        'source_only_provider_git_blob': SOURCE_ONLY_PROVIDER_GIT_BLOB,
        'worktree_provider_git_blob': WORKTREE_PROVIDER_GIT_BLOB,
        'portable_attestation_git_blob': PORTABLE_ATTESTATION_GIT_BLOB,
        'runtime_image_binding_git_blob': RUNTIME_IMAGE_BINDING_GIT_BLOB,
        'ollama_binding_git_blob': OLLAMA_BINDING_GIT_BLOB,
        'reconciliation_git_blob': RECONCILIATION_GIT_BLOB,
        'reviewed_collector_binding_present': False,
        'collector_implementation_source_pinned_by_activation_contract': False,
        'canonical_provider_binding_present': False,
        'canonical_collection_enabled': False,
        'collector_identity_admitted': False,
        'runtime_readiness_admitted': False,
        'runtime_execution_authorized': False,
        'binding_live_observation_implemented': False,
        'binding_filesystem_observation_implemented': False,
        'binding_git_query_implemented': False,
        'binding_subprocess_execution_implemented': False,
        'binding_network_request_implemented': False,
        'binding_ollama_request_implemented': False,
        'binding_docker_command_implemented': False,
        'binding_service_action_implemented': False,
        'binding_model_load_implemented': False,
        'binding_model_inference_implemented': False,
        'binding_game_execution_implemented': False,
        'binding_training_implemented': False,
        'binding_deployment_implemented': False,
        'binding_void_chain_mutation_implemented': False,
        'binding_wallet_or_funds_action_implemented': False,
        'dependency_contracts': dependencies,
    }


def enable_canonical_collection(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13CollectorImplementationBindingHold(
        'V2R13_COLLECTOR_IMPLEMENTATION_BOUND_BUT_ACTIVATION_BINDING_NOT_PRESENT'
    )
