from __future__ import annotations

import ast
import hashlib
import importlib.util
import sys
from copy import deepcopy
from functools import lru_cache
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_v2r13_activation_binding_review_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_activation_binding_review_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "7785cae74baeb5c4a1bfb541b95037019efc6e75134ffc58db4ffbdee041515f"

FORBIDDEN_IMPORT_ROOTS = {
    "subprocess",
    "socket",
    "requests",
    "urllib",
    "http",
    "httpx",
    "asyncio",
    "multiprocessing",
    "ctypes",
}
FORBIDDEN_CALLS = {
    "subprocess.run",
    "subprocess.Popen",
    "subprocess.call",
    "subprocess.check_call",
    "subprocess.check_output",
    "os.system",
    "os.popen",
}


@lru_cache(maxsize=1)
def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_v2r13_activation_binding_review",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def _contract_cached():
    return _load().v2r13_activation_binding_review_contract()


def _contract():
    return deepcopy(_contract_cached())


def _review():
    return deepcopy(_contract_cached()["review"])


def _expect_hold(exc_type, pattern, fn):
    try:
        fn()
    except exc_type as exc:
        assert pattern in str(exc), (pattern, str(exc))
    else:
        raise AssertionError(f"expected {exc_type.__name__}: {pattern}")


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def test_source_sha_is_exact():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SOURCE_SHA256


def test_static_source_has_no_direct_host_io_or_execution_surface():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in FORBIDDEN_IMPORT_ROOTS
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".", 1)[0]
            assert root not in FORBIDDEN_IMPORT_ROOTS
        elif isinstance(node, ast.Call):
            assert _dotted(node.func) not in FORBIDDEN_CALLS


def test_cached_review_matches_fresh_review_and_is_copy_isolated():
    m = _load()
    fresh = m.v2r13_activation_binding_review()
    cached = _review()
    assert cached == fresh

    cached["activation_binding_reviewed"] = False
    later = _review()
    assert later == fresh
    assert later["activation_binding_reviewed"] is True


def test_contract_pins_exact_reviewed_dependency_identities():
    out = _contract()
    assert out["activation_contract_git_blob"] == (
        "a3acb42280c334daa24a3b830105a04666fd603b"
    )
    assert out["activation_contract_source_sha256"] == (
        "dc4c90175dee00f23ab28bc362cec41245a069345c0154d519215e3cb8150a3c"
    )
    assert out["invocation_acceptance_git_blob"] == (
        "1ced66b86edbda59b33bdc25a185842d7bd71418"
    )
    assert out["invocation_acceptance_source_sha256"] == (
        "2a883510806ac6123c7e8bb6a2289f6d3d0dd501bb5aed0e738c435e7eda3045"
    )
    assert out["ollama_binding_git_blob"] == (
        "58364a1d5d71aead9df6dc0fc61661a557131508"
    )
    assert out["ollama_binding_source_sha256"] == (
        "c6b0bb746d017326e600f401a2d07a29fba79aced401687c4eb5238084ee9335"
    )
    assert out["worktree_observer_git_blob"] == (
        "994f3be5d3344d6ac905c1f5fee9f9490fd4dd3f"
    )
    assert out["worktree_observer_source_sha256"] == (
        "ad2544600833e3f88388e68df5e289a7f69b55f4e8c32f89e8899338e195aacf"
    )


def test_historical_activation_contract_is_retained_not_rewritten():
    m = _load()
    out = _contract()
    assert out["historical_activation_contract_retained"] is True
    assert out["historical_activation_blockers"] == (
        "V2R13_ACTIVATION_BINDING_NOT_REVIEWED",
        "V2R13_ACTIVE_MODEL_DIGEST_PROBE_NOT_REVIEWED",
        "V2R13_FROZEN_WORKTREE_MATERIALIZER_NOT_REVIEWED",
        m.activation_contract.RUNTIME_AUTHORITY_BLOCKER,
    )


def test_activation_binding_and_model_digest_review_close_semantically():
    out = _review()
    assert out["activation_binding_reviewed"] is True
    assert out["active_model_digest_probe_reviewed"] is True
    assert out["accepted_live_invocation_present"] is True
    assert out["accepted_live_invocation_count"] == 1
    assert out["provider_capability_complete"] is True
    assert out["provider_supported_primitive_count"] == 16
    assert out["provider_remaining_unresolved_primitive_count"] == 0


def test_worktree_observer_is_reviewed_but_materializer_remains_open():
    out = _review()
    assert out["frozen_worktree_observer_reviewed"] is True
    assert out["frozen_worktree_materializer_reviewed"] is False
    worktree = out["dependencies"]["worktree_observer_contract"]
    assert worktree["six_path_classification_leaves_implemented"] is True
    assert worktree["activation_worktree_shape_composition_implemented"] is True
    assert worktree["real_host_backend_implemented"] is False
    assert worktree["automatic_host_backend_selection"] is False


def test_remaining_activation_blockers_are_exact():
    m = _load()
    out = _review()
    assert out["remaining_activation_blockers"] == (
        "V2R13_FROZEN_WORKTREE_MATERIALIZER_NOT_REVIEWED",
        m.activation_contract.RUNTIME_AUTHORITY_BLOCKER,
    )
    assert out["remaining_activation_blocker_count"] == 2


def test_activation_is_not_claimed_proven_or_complete():
    out = _review()
    assert out["activation_proven"] is False
    assert out["runtime_activation_performed"] is False
    assert out["runtime_activation_path_complete"] is False
    assert out["runtime_execution_authorized"] is False


def test_accepted_collection_does_not_enable_automatic_collection():
    out = _review()
    assert out["canonical_collection_enabled"] is False
    accepted = out["dependencies"]["accepted_live_invocation_contract"]
    assert accepted["canonical_live_collection_invocation_accepted"] is True
    assert accepted["canonical_collection_enabled"] is False
    assert (
        accepted["future_live_collection_requires_fresh_explicit_authorization"]
        is True
    )


def test_model_identity_review_is_grounded_in_canonical_ollama_binding():
    out = _review()
    ollama = out["dependencies"]["ollama_observer_binding_contract"]
    assert ollama["canonical_observer_source_binding_present"] is True
    assert ollama["endpoint_liveness_provider_primitive_implemented"] is True
    assert ollama["model_identity_provider_primitive_implemented"] is True
    assert ollama["supported_primitive_count_after_binding"] == 16
    assert ollama["remaining_unresolved_primitive_count"] == 0
    assert ollama["binding_live_observation_implemented"] is False


def test_execution_materialization_remains_independently_open():
    out = _review()
    assert out["execution_materialization_remains_open"] is True
    assert out["execution_materialization_blockers"] == (
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
        "CROSS_CONTROL_RUNTIME_SELECTOR_NOT_IMPLEMENTED",
        "COMMAND_MATERIALIZER_NOT_IMPLEMENTED",
        "ISOLATED_WORKDIR_ALLOCATOR_NOT_IMPLEMENTED",
    )
    rows = out["dependencies"]["v2r13_execution_descriptors"]
    assert len(rows) == 6
    assert all(row["eligible"] is False for row in rows)


def test_next_gate_is_frozen_worktree_materializer_implementation():
    out = _contract()
    assert out["next_gate"] == (
        "V2R13_FROZEN_WORKTREE_MATERIALIZER_IMPLEMENTATION_REQUIRED"
    )
    assert out["next_change_class"] == (
        "source_only_frozen_worktree_materializer_implementation"
    )
    assert out["runtime_authority_is_not_only_remaining_gap"] is True


def test_review_contract_requires_no_live_or_runtime_action():
    out = _contract()
    for field in (
        "live_observation_required_for_this_change",
        "filesystem_observation_required_for_this_change",
        "git_query_required_for_this_change",
        "runtime_action_required_for_this_change",
        "model_load_required_for_this_change",
        "model_inference_required_for_this_change",
        "game_execution_required_for_this_change",
        "training_required_for_this_change",
        "deployment_required_for_this_change",
        "void_chain_mutation_required_for_this_change",
        "funds_action_required_for_this_change",
        "review_live_observation_implemented",
        "review_filesystem_observation_implemented",
        "review_git_query_implemented",
        "review_subprocess_execution_implemented",
        "review_network_request_implemented",
        "review_ollama_request_implemented",
        "review_docker_command_implemented",
        "review_service_action_implemented",
        "review_model_load_implemented",
        "review_model_inference_implemented",
        "review_game_execution_implemented",
        "review_training_implemented",
        "review_deployment_implemented",
        "review_void_chain_mutation_implemented",
        "review_wallet_or_funds_action_implemented",
    ):
        assert out[field] is False, field


def test_materializer_call_always_holds_at_next_gate():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13ActivationBindingReviewHold,
        "V2R13_FROZEN_WORKTREE_MATERIALIZER_IMPLEMENTATION_REQUIRED",
        lambda: m.materialize_frozen_worktrees(),
    )


def test_runtime_authorization_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13ActivationBindingReviewHold,
        m.activation_contract.RUNTIME_AUTHORITY_BLOCKER,
        lambda: m.authorize_runtime_execution(),
    )
