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
    "abaddon_policy_campaign_runtime_v2r13_"
    "current_main_preload_live_readiness_evidence_acceptance_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_"
    "current_main_preload_live_readiness_evidence_acceptance_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "a91350385ede0e3e6575cbf81fbacf88bc336bd0ea3d37b86035d46d442b0778"


@lru_cache(maxsize=1)
def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    repo = str(HERE.parents[1])
    if repo not in sys.path:
        sys.path.insert(0, repo)
    spec = importlib.util.spec_from_file_location(
        "_void_g2_v2r13_current_main_readiness_acceptance",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    raw_validate_dependencies = module._validate_dependencies

    @lru_cache(maxsize=1)
    def cached_dependencies():
        return raw_validate_dependencies()

    def copy_isolated_dependencies():
        return deepcopy(cached_dependencies())

    module._raw_validate_dependencies_for_test = raw_validate_dependencies
    module._validate_dependencies = copy_isolated_dependencies
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
    out = m.current_main_v2r13_live_readiness_evidence_acceptance_contract()
    assert out["schema"] == (
        "void.abaddon.generation2."
        "v2r13-current-main-preload-live-readiness-evidence-acceptance-contract.v1"
    )
    assert out["snapshot_id"] == m.V2R13


def test_current_main_binding_is_exact():
    m = _load()
    out = m.current_main_v2r13_live_readiness_evidence_acceptance_contract()
    assert out["current_main_head"] == "138b121419328d3db79b080dbd9300a4227f3e99"
    assert out["current_main_tree"] == "200b88ede3913218208ada4171db6d444c97cf28"
    assert out["evidence_bound_to_current_main"] is True


def test_exact_evidence_sha_is_pinned_and_recomputed():
    m = _load()
    assert m.ACCEPTED_EVIDENCE_SHA256 == (
        "ee5c9c555323fc0a0b6550953700ec033ad2f4bb9d8b8763c5f59bfdb9bf91d2"
    )
    assert m._canonical_sha256(_evidence(m)) == m.ACCEPTED_EVIDENCE_SHA256


def test_launcher_and_preload_identity_are_exact():
    m = _load()
    evidence = _evidence(m)
    assert evidence["launcher_sha256"] == (
        "a76f0542c01de015a2f838e119f1bcb461fd17c063725c7cfd123a5271fa8d82"
    )
    assert evidence["preload_body_sha256"] == (
        "1ddc04745c6310fa1a4ae71dd4a46a3d21c9157a795669b89646a662881c07ef"
    )
    assert evidence["exact_model_preload_green"] is True
    assert evidence["launcher_model_load_performed"] is True
    assert evidence["preload_prompt_supplied"] is False
    assert evidence["preload_generated_response_text_observed"] is False


def test_live_metadata_hashes_are_exact():
    m = _load()
    evidence = _evidence(m)
    assert evidence["ollama_tags_body_sha256"] == (
        "119d0ca767aa571ddf514dcfdf4a400e755e28543b1d54e541949ca07bc92a8b"
    )
    assert evidence["ollama_ps_body_sha256"] == (
        "0e1723538f8c987908136cc882a43b53ba22569a1546f227fa2f13e455785c52"
    )
    assert evidence["docker_context_stdout_sha256"] == (
        "107f714d1bab1ecae968808edfe5f6570b07c717da8ced0e42fb5eaad832a818"
    )
    assert evidence["docker_info_stdout_sha256"] == (
        "17b5a2caeb80a253b74fc7ec3d978c949cd10fe09a73bfec022ed62b2a0e0008"
    )
    assert evidence["docker_image_inspect_stdout_sha256"] == (
        "cb147df77f290ebfce9b997496a1d725e6851ee37ae728f7cecc52dbf1177fba"
    )


def test_bound_receipt_hashes_are_exact():
    m = _load()
    evidence = _evidence(m)
    assert evidence["entrypoint_receipt_sha256"] == (
        "41948e77f3b2f937959acfb4a8215f2dd69f5f167f7ac33d3c84ad436fa07f09"
    )
    assert evidence["bound_validation_sha256"] == (
        "afda05a169f0848ab94900283935caf1a367a9f1719884fee5b18514815ab6e9"
    )
    assert evidence["bound_live_receipt_validation_green"] is True


def test_cached_dependency_snapshot_matches_fresh_validation_and_is_copy_isolated():
    m = _load()
    fresh = m._raw_validate_dependencies_for_test()
    cached = m._validate_dependencies()
    assert cached == fresh

    cached["entrypoint_binding"]["canonical_live_collection_path_complete"] = False
    later = m._validate_dependencies()
    assert later == fresh
    assert later["entrypoint_binding"]["canonical_live_collection_path_complete"] is True


def test_exact_evidence_is_accepted():
    m = _load()
    out = m.accept_current_main_v2r13_live_readiness_evidence(_evidence(m))
    assert out["current_main_preload_live_readiness_evidence_accepted"] is True
    assert out["accepted_evidence_sha256"] == m.ACCEPTED_EVIDENCE_SHA256
    assert out["evidence_bound_to_current_main"] is True


def test_acceptance_preserves_readiness_and_provider_completion():
    m = _load()
    out = m.accept_current_main_v2r13_live_readiness_evidence(_evidence(m))
    assert out["provider_capability_supported_primitive_count"] == 16
    assert out["provider_capability_remaining_unresolved_primitive_count"] == 0
    assert out["provider_capability_complete"] is True
    assert out["collector_identity_admitted"] is True
    assert out["runtime_readiness_admitted"] is True


def test_accepted_model_load_is_external_but_acceptance_is_source_only():
    m = _load()
    out = m.accept_current_main_v2r13_live_readiness_evidence(_evidence(m))
    assert out["external_launcher_model_load_performed"] is True
    assert out["acceptance_performs_model_load"] is False
    assert out["accepted_preload_prompt_supplied"] is False
    assert out["accepted_preload_generated_response_text_observed"] is False


def test_execution_materialization_source_frontier_is_closed():
    m = _load()
    out = m.current_main_v2r13_live_readiness_evidence_acceptance_contract()
    assert out["execution_materialization_source_frontier_closed"] is True
    dep = out["dependencies"]["execution_materialization_review"]
    assert dep["source_frontier_closed"] is True
    assert tuple(dep["execution_materialization_source_blockers"]) == ()
    assert tuple(dep["execution_materialization_blockers"]) == (
        m.RUNTIME_AUTHORITY_BLOCKER,
    )


def test_dependency_identities_are_exact():
    m = _load()
    out = m.current_main_v2r13_live_readiness_evidence_acceptance_contract()
    assert out["entrypoint_binding_git_blob"] == "3950bbdd68f2fdc089f596f8159d480699af9982"
    assert out["prior_acceptance_git_blob"] == "1ced66b86edbda59b33bdc25a185842d7bd71418"
    assert out["allocator_review_git_blob"] == "a1fb192ce13030f814da74d12bc930968e77d765"


def test_prior_acceptance_is_retained_and_current_acceptance_is_second():
    m = _load()
    out = m.current_main_v2r13_live_readiness_evidence_acceptance_contract()
    assert out["prior_accepted_evidence_sha256"] == (
        "68465b443ab483a1b00db6f947dc87b51231fe1f9ce8434a105e6a0416e5d788"
    )
    assert out["prior_accepted_live_invocation_count"] == 1
    assert out["accepted_current_main_live_invocation_count"] == 1
    assert out["total_accepted_live_invocation_count"] == 2


def test_runtime_execution_remains_closed_and_lane_scoped():
    m = _load()
    out = m.accept_current_main_v2r13_live_readiness_evidence(_evidence(m))
    assert out["runtime_execution_authorized"] is False
    assert out["runtime_execution_performed"] is False
    assert out["runtime_activation_performed"] is False
    assert out["runtime_execution_authorization_scope"] == "v2r13_lane_only"
    assert out["other_runtime_lanes_readiness_implied"] is False


def test_acceptance_preserves_no_inference_game_training_or_funds_actions():
    m = _load()
    out = m.accept_current_main_v2r13_live_readiness_evidence(_evidence(m))
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


def test_contract_itself_performs_no_live_or_host_actions():
    m = _load()
    out = m.current_main_v2r13_live_readiness_evidence_acceptance_contract()
    for field in (
        "acceptance_performs_model_load",
        "acceptance_performs_live_observation",
        "acceptance_performs_http_request",
        "acceptance_performs_ollama_request",
        "acceptance_performs_docker_command",
        "acceptance_performs_git_query",
        "acceptance_performs_filesystem_observation",
        "acceptance_performs_systemd_action",
    ):
        assert out[field] is False


def test_tampered_field_set_is_rejected():
    m = _load()
    evidence = _evidence(m)
    evidence["unexpected"] = True
    _expect_hold(
        m.RuntimeV2R13CurrentMainLiveReadinessEvidenceAcceptanceHold,
        "field-set drift",
        lambda: m.accept_current_main_v2r13_live_readiness_evidence(evidence),
    )


def test_tampered_main_head_is_rejected():
    m = _load()
    evidence = _evidence(m)
    evidence["canonical_main_head"] = "0" * 40
    _expect_hold(
        m.RuntimeV2R13CurrentMainLiveReadinessEvidenceAcceptanceHold,
        "evidence drift: canonical_main_head",
        lambda: m.accept_current_main_v2r13_live_readiness_evidence(evidence),
    )


def test_tampered_preload_hash_is_rejected():
    m = _load()
    evidence = _evidence(m)
    evidence["preload_body_sha256"] = "0" * 64
    _expect_hold(
        m.RuntimeV2R13CurrentMainLiveReadinessEvidenceAcceptanceHold,
        "evidence drift: preload_body_sha256",
        lambda: m.accept_current_main_v2r13_live_readiness_evidence(evidence),
    )


def test_boolean_integer_type_confusion_is_rejected():
    m = _load()
    evidence = _evidence(m)
    evidence["live_observation_performed"] = 1
    _expect_hold(
        m.RuntimeV2R13CurrentMainLiveReadinessEvidenceAcceptanceHold,
        "evidence drift: live_observation_performed",
        lambda: m.accept_current_main_v2r13_live_readiness_evidence(evidence),
    )


def test_tampered_inference_claim_is_rejected():
    m = _load()
    evidence = _evidence(m)
    evidence["model_inference_performed"] = True
    _expect_hold(
        m.RuntimeV2R13CurrentMainLiveReadinessEvidenceAcceptanceHold,
        "evidence drift: model_inference_performed",
        lambda: m.accept_current_main_v2r13_live_readiness_evidence(evidence),
    )


def test_tampered_runtime_authority_claim_is_rejected():
    m = _load()
    evidence = _evidence(m)
    evidence["runtime_execution_authorized"] = True
    _expect_hold(
        m.RuntimeV2R13CurrentMainLiveReadinessEvidenceAcceptanceHold,
        "evidence drift: runtime_execution_authorized",
        lambda: m.accept_current_main_v2r13_live_readiness_evidence(evidence),
    )


def test_missing_external_model_load_claim_is_rejected():
    m = _load()
    evidence = _evidence(m)
    evidence["launcher_model_load_performed"] = False
    _expect_hold(
        m.RuntimeV2R13CurrentMainLiveReadinessEvidenceAcceptanceHold,
        "evidence drift: launcher_model_load_performed",
        lambda: m.accept_current_main_v2r13_live_readiness_evidence(evidence),
    )


def test_returned_evidence_is_copy_isolated():
    m = _load()
    evidence = _evidence(m)
    out = m.accept_current_main_v2r13_live_readiness_evidence(evidence)
    out["accepted_evidence"]["runtime_readiness_admitted"] = False
    assert evidence["runtime_readiness_admitted"] is True
    second = m.accept_current_main_v2r13_live_readiness_evidence(evidence)
    assert second["accepted_evidence"]["runtime_readiness_admitted"] is True


def test_next_gate_is_runtime_execution_authorization_for_v2r13_only():
    m = _load()
    out = m.current_main_v2r13_live_readiness_evidence_acceptance_contract()
    assert out["next_gate"] == "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED"
    assert out["runtime_execution_authorization_scope"] == "v2r13_lane_only"
    assert out["other_runtime_lanes_readiness_implied"] is False
    assert out["holds"] == ["RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED"]


def test_future_live_collection_still_requires_fresh_authorization():
    m = _load()
    out = m.current_main_v2r13_live_readiness_evidence_acceptance_contract()
    assert out["future_live_collection_requires_fresh_explicit_authorization"] is True
    assert out["future_collection_gate"] == (
        "V2R13_CANONICAL_LIVE_COLLECTION_INVOCATION_AUTHORIZATION_REQUIRED"
    )
    _expect_hold(
        m.RuntimeV2R13CurrentMainLiveReadinessEvidenceAcceptanceHold,
        "V2R13_CANONICAL_LIVE_COLLECTION_INVOCATION_AUTHORIZATION_REQUIRED",
        lambda: m.request_additional_live_collection(),
    )


def test_runtime_execution_entrypoint_still_holds():
    m = _load()
    _expect_hold(
        m.RuntimeV2R13CurrentMainLiveReadinessEvidenceAcceptanceHold,
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED",
        lambda: m.authorize_runtime_execution(),
    )
