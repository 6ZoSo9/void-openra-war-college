from __future__ import annotations

import ast
import hashlib
import importlib.util
import sys
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_v2r13_"
    "canonical_live_collection_invocation_acceptance_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_"
    "canonical_live_collection_invocation_acceptance_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "2a883510806ac6123c7e8bb6a2289f6d3d0dd501bb5aed0e738c435e7eda3045"


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    repo = str(HERE.parents[1])
    if repo not in sys.path:
        sys.path.insert(0, repo)
    spec = importlib.util.spec_from_file_location(
        "_void_g2_v2r13_canonical_live_collection_invocation_acceptance",
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
        raise AssertionError(f"expected {exc_type.__name__}: {pattern}")


def _evidence(m):
    return deepcopy(m.EXPECTED_ACCEPTED_EVIDENCE)


def test_source_sha_is_exact():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SOURCE_SHA256


def test_contract_schema_and_snapshot_are_exact():
    m = _load()
    out = m.v2r13_canonical_live_collection_invocation_acceptance_contract()
    assert out["schema"] == (
        "void.abaddon.generation2."
        "v2r13-canonical-live-collection-invocation-acceptance-contract.v1"
    )
    assert out["snapshot_id"] == m.V2R13


def test_entrypoint_binding_identity_is_pinned_exactly():
    m = _load()
    out = m.v2r13_canonical_live_collection_invocation_acceptance_contract()
    assert out["entrypoint_binding_git_blob"] == (
        "3950bbdd68f2fdc089f596f8159d480699af9982"
    )
    assert out["entrypoint_binding_source_sha256"] == (
        "06c5a110401b05631eb64496cee7b2d7e56378a9376c9d0c4fd1db015c6308f1"
    )


def test_exact_success_evidence_hash_is_pinned():
    m = _load()
    assert m.ACCEPTED_EVIDENCE_SHA256 == "68465b443ab483a1b00db6f947dc87b51231fe1f9ce8434a105e6a0416e5d788"
    evidence = _evidence(m)
    assert evidence["launcher_sha256"] == (
        "d590039b3274c933ab67af311b17d3394d78f0f36ab44c788a3964831fefc8d2"
    )
    assert evidence["entrypoint_receipt_sha256"] == (
        "41948e77f3b2f937959acfb4a8215f2dd69f5f167f7ac33d3c84ad436fa07f09"
    )
    assert evidence["bound_validation_sha256"] == (
        "afda05a169f0848ab94900283935caf1a367a9f1719884fee5b18514815ab6e9"
    )


def test_ollama_and_docker_hashes_are_pinned_exactly():
    m = _load()
    evidence = _evidence(m)
    assert evidence["ollama_tags_body_sha256"] == (
        "119d0ca767aa571ddf514dcfdf4a400e755e28543b1d54e541949ca07bc92a8b"
    )
    assert evidence["ollama_ps_body_sha256"] == (
        "86f32105e624b7486dce6264fdd515789ee3a9e520c7b33704532bafb82662c1"
    )
    assert evidence["docker_context_stdout_sha256"] == (
        "107f714d1bab1ecae968808edfe5f6570b07c717da8ced0e42fb5eaad832a818"
    )
    assert evidence["docker_info_stdout_sha256"] == (
        "6f48856a6248ee95e7390ce947f7ec81742503a60359f3ec54d6a45afafea374"
    )
    assert evidence["docker_image_inspect_stdout_sha256"] == (
        "cb147df77f290ebfce9b997496a1d725e6851ee37ae728f7cecc52dbf1177fba"
    )


def test_exact_evidence_is_accepted_once():
    m = _load()
    out = m.accept_v2r13_canonical_live_collection_invocation(_evidence(m))
    assert out["canonical_live_collection_invocation_accepted"] is True
    assert out["accepted_live_invocation_count"] == 1
    assert out["live_observation_evidence_pinned"] is True


def test_acceptance_preserves_identity_and_readiness():
    m = _load()
    out = m.accept_v2r13_canonical_live_collection_invocation(_evidence(m))
    assert out["provider_capability_complete"] is True
    assert out["provider_capability_supported_primitive_count"] == 16
    assert out["provider_capability_remaining_unresolved_primitive_count"] == 0
    assert out["collector_identity_admitted"] is True
    assert out["runtime_readiness_admitted"] is True


def test_acceptance_does_not_enable_automatic_collection_or_runtime():
    m = _load()
    out = m.accept_v2r13_canonical_live_collection_invocation(_evidence(m))
    assert out["canonical_live_collection_path_complete"] is True
    assert out["canonical_collection_enabled"] is False
    assert out["automatic_canonical_collection_enabled"] is False
    assert out["future_live_collection_requires_fresh_explicit_authorization"] is True
    assert out["runtime_execution_authorized"] is False
    assert out["runtime_activation_performed"] is False


def test_acceptance_preserves_execution_boundaries():
    m = _load()
    out = m.accept_v2r13_canonical_live_collection_invocation(_evidence(m))
    for field in (
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "policy_promotion_performed",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        assert out[field] is False


def test_dependency_contract_remains_source_bound_but_not_enabled():
    m = _load()
    out = m.v2r13_canonical_live_collection_invocation_acceptance_contract()
    dep = out["dependency_contract"]
    assert dep["canonical_live_collection_entrypoint_source_binding_present"] is True
    assert dep["canonical_live_collection_path_complete"] is True
    assert dep["canonical_collection_enabled"] is False
    assert dep["runtime_execution_authorized"] is False


def test_acceptance_source_has_no_direct_host_io_imports():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    forbidden = {
        "os", "subprocess", "pathlib", "socket", "urllib", "http",
        "requests", "httpx", "docker", "asyncio", "multiprocessing", "ctypes",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden


def test_tampered_field_set_is_rejected():
    m = _load()
    evidence = _evidence(m)
    evidence["unexpected"] = True
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionInvocationAcceptanceHold,
        "field-set drift",
        lambda: m.accept_v2r13_canonical_live_collection_invocation(evidence),
    )


def test_tampered_receipt_hash_is_rejected():
    m = _load()
    evidence = _evidence(m)
    evidence["entrypoint_receipt_sha256"] = "0" * 64
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionInvocationAcceptanceHold,
        "evidence drift: entrypoint_receipt_sha256",
        lambda: m.accept_v2r13_canonical_live_collection_invocation(evidence),
    )


def test_tampered_boundary_boolean_is_rejected():
    m = _load()
    evidence = _evidence(m)
    evidence["model_inference_performed"] = True
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionInvocationAcceptanceHold,
        "evidence drift: model_inference_performed",
        lambda: m.accept_v2r13_canonical_live_collection_invocation(evidence),
    )


def test_boolean_integer_type_confusion_is_rejected():
    m = _load()
    evidence = _evidence(m)
    evidence["live_observation_performed"] = 1
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionInvocationAcceptanceHold,
        "evidence drift: live_observation_performed",
        lambda: m.accept_v2r13_canonical_live_collection_invocation(evidence),
    )


def test_contract_marks_exactly_one_invocation_accepted():
    m = _load()
    out = m.v2r13_canonical_live_collection_invocation_acceptance_contract()
    assert out["canonical_live_collection_invocation_accepted"] is True
    assert out["accepted_live_invocation_count"] == 1
    assert out["acceptance_performs_live_observation"] is False
    assert out["acceptance_performs_ollama_request"] is False
    assert out["acceptance_performs_docker_command"] is False


def test_next_gate_is_activation_binding_review():
    m = _load()
    out = m.v2r13_canonical_live_collection_invocation_acceptance_contract()
    assert out["next_gate"] == "V2R13_ACTIVATION_BINDING_REVIEW_REQUIRED"
    assert out["future_collection_gate"] == (
        "V2R13_CANONICAL_LIVE_COLLECTION_INVOCATION_AUTHORIZATION_REQUIRED"
    )


def test_additional_collection_requires_fresh_authorization():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionInvocationAcceptanceHold,
        "V2R13_CANONICAL_LIVE_COLLECTION_INVOCATION_AUTHORIZATION_REQUIRED",
        lambda: m.request_additional_live_collection(),
    )


def test_runtime_execution_remains_closed():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13CanonicalLiveCollectionInvocationAcceptanceHold,
        m.RUNTIME_AUTHORITY_BLOCKER,
        lambda: m.authorize_runtime_execution(),
    )
