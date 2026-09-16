from __future__ import annotations

import ast
import hashlib
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    'abaddon_policy_campaign_runtime_v2r13_collector_implementation_binding_generation2.py'
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / 'openra_env/learning/'
    'abaddon_policy_campaign_runtime_v2r13_collector_implementation_binding_generation2.py'
)
EXPECTED_SOURCE_SHA256 = 'af4a51207a0ad1477eedd18c325ee1df2231b6ad990bbb6f4f8ba53ef5bffc1d'

COMMON = (
    'observation_mode',
    'mutation_performed',
    'service_action_performed',
    'runtime_start_performed',
    'game_execution_performed',
    'model_inference_performed',
)
WORKTREE = (
    'frozen_source_worktree.exists',
    'frozen_source_worktree.is_directory',
    'frozen_source_worktree.is_symlink',
    'engine_worktree.exists',
    'engine_worktree.is_directory',
    'engine_worktree.is_symlink',
)


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    repo = '/home/zoso/dev/openra-rl-war-college'
    if repo not in sys.path:
        sys.path.insert(0, repo)
    spec = importlib.util.spec_from_file_location(
        '_void_g2_v2r13_collector_implementation_binding',
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _expect_hold(exc_type, pattern, fn):
    try:
        fn()
    except exc_type as exc:
        assert pattern in str(exc), (pattern, str(exc))
    else:
        raise AssertionError(f'expected {exc_type.__name__}: {pattern}')


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f'{base}.{node.attr}' if base else node.attr
    return ''


def test_source_sha_is_exact():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SOURCE_SHA256


def test_contract_schema_and_snapshot_are_exact():
    m = _load()
    out = m.v2r13_collector_implementation_binding_contract()
    assert out['schema'] == 'void.abaddon.generation2.v2r13-collector-implementation-binding-contract.v1'
    assert out['snapshot_id'] == m.V2R13


def test_collector_implementation_identity_is_exact():
    m = _load()
    out = m.v2r13_collector_implementation_binding_contract()
    assert out['collector_implementation_git_blob'] == '0003c24390194a4f621f13c6077e0604b9abcd98'
    assert out['collector_implementation_source_sha256'] == '91e094c71b838ad8116dced00fbc50b3e8a8bd138f75dfb5ae86b9bf5c97a8dc'
    assert out['collector_implementation_source_binding_present'] is True
    assert out['collector_implementation_source_identity_pinned_by_git_blob'] is True
    assert out['collector_implementation_source_identity_pinned_by_sha256'] is True
    assert out['collector_implementation_source_is_not_self_bound'] is True


def test_binding_map_has_exact_sixteen_names():
    m = _load()
    bindings = m.reviewed_v2r13_primitive_source_bindings()
    assert len(bindings) == 16
    assert len(set(bindings)) == 16
    assert tuple(bindings) == tuple(m.collector_implementation.required_primitive_names(m.V2R13))


def test_common_primitives_bind_to_source_only_provider():
    m = _load()
    bindings = m.reviewed_v2r13_primitive_source_bindings()
    assert tuple(bindings)[:6] == COMMON
    for name in COMMON:
        assert bindings[name] == 'daa038f17d3103cd0644303d40fd37a060ec51d1a6c68ac5d91555897eeb1a81'


def test_worktree_primitives_bind_to_worktree_adapter():
    m = _load()
    bindings = m.reviewed_v2r13_primitive_source_bindings()
    for name in WORKTREE:
        assert bindings[name] == '172dbb3acc3d9f34a64acd68f3bee58ae30336ad2802fd1dfbf9597bf8105522'


def test_portable_primitive_binds_to_attestation_validator():
    m = _load()
    bindings = m.reviewed_v2r13_primitive_source_bindings()
    assert bindings['portable_binding_attested'] == 'c480af5b439b4c68b24f5bb68bdce1948f215eda3e847e8631a43e8eacbac818'


def test_runtime_image_primitive_binds_to_bound_image_provider():
    m = _load()
    bindings = m.reviewed_v2r13_primitive_source_bindings()
    assert bindings['runtime_image_identity_verified'] == '74acc7248ee19d2d141aa4ec36fc3ce1c6068c56ca1801719c3287cd2c774f52'


def test_endpoint_and_model_bind_to_bound_ollama_provider():
    m = _load()
    bindings = m.reviewed_v2r13_primitive_source_bindings()
    assert bindings['endpoint_liveness'] == 'c6b0bb746d017326e600f401a2d07a29fba79aced401687c4eb5238084ee9335'
    assert bindings['model_identity_verified'] == 'c6b0bb746d017326e600f401a2d07a29fba79aced401687c4eb5238084ee9335'


def test_dependency_git_blobs_are_exact():
    m = _load()
    out = m.v2r13_collector_implementation_binding_contract()
    assert out['source_only_provider_git_blob'] == 'f3b48e624172aeed81e28a6e24508533b7b13661'
    assert out['worktree_provider_git_blob'] == '7e6f628c64fe02db42bd6adee67d3965e6b1ae92'
    assert out['portable_attestation_git_blob'] == 'afdc0421958565e713795dfd0d3c4c683041cc37'
    assert out['runtime_image_binding_git_blob'] == '7075ded7a19454239b95a09e7b4630413124a796'
    assert out['ollama_binding_git_blob'] == '58364a1d5d71aead9df6dc0fc61661a557131508'
    assert out['reconciliation_git_blob'] == '6c7dee5f94d32623cd7158868690fe0ac1d0c0c0'


def test_canonical_primitive_source_bindings_are_present():
    m = _load()
    out = m.v2r13_collector_implementation_binding_contract()
    assert out['canonical_primitive_source_bindings_present'] is True
    assert out['primitive_source_binding_count'] == 16


def test_activation_evidence_binding_stays_absent():
    m = _load()
    out = m.v2r13_collector_implementation_binding_contract()
    assert out['reviewed_collector_binding_present'] is False
    assert out['collector_implementation_source_pinned_by_activation_contract'] is False
    assert m.activation_evidence.REVIEWED_COLLECTOR_BINDING_PRESENT is False


def test_collection_identity_and_readiness_stay_closed():
    m = _load()
    out = m.v2r13_collector_implementation_binding_contract()
    assert out['canonical_provider_binding_present'] is False
    assert out['canonical_collection_enabled'] is False
    assert out['collector_identity_admitted'] is False
    assert out['runtime_readiness_admitted'] is False
    assert out['runtime_execution_authorized'] is False


def test_provider_frontier_dependency_is_complete():
    m = _load()
    out = m.v2r13_collector_implementation_binding_contract()
    ollama = out['dependency_contracts']['ollama_binding']
    assert ollama['supported_primitive_count_after_binding'] == 16
    assert ollama['remaining_unresolved_primitive_count'] == 0
    assert ollama['all_v2r13_provider_primitives_implemented'] is True


def test_reconciliation_dependency_closes_historical_provider_gap():
    m = _load()
    out = m.v2r13_collector_implementation_binding_contract()
    recon = out['dependency_contracts']['reconciliation']
    assert recon['historical_future_provider_gap_closed'] is True
    assert recon['collector_implementation_source_binding_present'] is False


def test_returned_binding_map_is_copy_isolated():
    m = _load()
    first = m.reviewed_v2r13_primitive_source_bindings()
    first['endpoint_liveness'] = '0' * 64
    second = m.reviewed_v2r13_primitive_source_bindings()
    assert second['endpoint_liveness'] == 'c6b0bb746d017326e600f401a2d07a29fba79aced401687c4eb5238084ee9335'


def test_returned_dependency_contracts_are_copy_isolated():
    m = _load()
    first = m.v2r13_collector_implementation_binding_contract()
    first['dependency_contracts']['reconciliation']['historical_future_provider_gap_closed'] = False
    second = m.v2r13_collector_implementation_binding_contract()
    assert second['dependency_contracts']['reconciliation']['historical_future_provider_gap_closed'] is True


def test_static_source_has_no_host_io_imports_or_calls():
    source = SOURCE.read_text(encoding='utf-8')
    tree = ast.parse(source, filename=str(SOURCE))
    forbidden_import_roots = {
        'os', 'subprocess', 'pathlib', 'socket', 'urllib', 'http', 'requests',
        'httpx', 'docker', 'asyncio', 'multiprocessing', 'ctypes',
    }
    forbidden_call_prefixes = (
        'os.', 'subprocess.', 'pathlib.', 'socket.', 'urllib.', 'http.',
        'requests.', 'httpx.', 'docker.',
        'ollama_binding.ollama_observer.host_http_get',
        'ollama_binding.ollama_observer.observe_v2r13_ollama_readonly',
        'collector_implementation.collect_candidate_with_provider',
    )
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split('.', 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or '').split('.', 1)[0] not in forbidden_import_roots
        elif isinstance(node, ast.Call):
            name = _dotted(node.func)
            assert not name.startswith(forbidden_call_prefixes)


def test_binding_contract_claims_zero_live_actions():
    m = _load()
    out = m.v2r13_collector_implementation_binding_contract()
    for field in (
        'binding_live_observation_implemented',
        'binding_filesystem_observation_implemented',
        'binding_git_query_implemented',
        'binding_subprocess_execution_implemented',
        'binding_network_request_implemented',
        'binding_ollama_request_implemented',
        'binding_docker_command_implemented',
        'binding_service_action_implemented',
        'binding_model_load_implemented',
        'binding_model_inference_implemented',
        'binding_game_execution_implemented',
        'binding_training_implemented',
        'binding_deployment_implemented',
        'binding_void_chain_mutation_implemented',
        'binding_wallet_or_funds_action_implemented',
    ):
        assert out[field] is False


def test_enable_canonical_collection_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13CollectorImplementationBindingHold,
        'V2R13_COLLECTOR_IMPLEMENTATION_BOUND_BUT_ACTIVATION_BINDING_NOT_PRESENT',
        lambda: m.enable_canonical_collection(),
    )
