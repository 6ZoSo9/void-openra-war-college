from __future__ import annotations

import ast
import hashlib
import importlib.util
from pathlib import Path


HERE = Path(__file__).resolve()
LOCAL_SOURCE = HERE.with_name(
    "abaddon_policy_campaign_runtime_observation_primitive_review_generation2.py"
)
SOURCE = (
    LOCAL_SOURCE
    if LOCAL_SOURCE.is_file()
    else HERE.parents[1]
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_observation_primitive_review_generation2.py"
)
EXPECTED_SOURCE_SHA256 = "c0123c2f06fc7a6fcb28449eaa9691afc3e128242ba577da291f15c23ba60086"

FORBIDDEN_IMPORT_ROOTS = {
    "os",
    "subprocess",
    "socket",
    "requests",
    "urllib",
    "http",
    "httpx",
    "asyncio",
    "multiprocessing",
    "ctypes",
    "glob",
}
FORBIDDEN_CALLS = {
    "subprocess.run",
    "subprocess.Popen",
    "subprocess.call",
    "subprocess.check_call",
    "subprocess.check_output",
    "os.system",
    "os.popen",
    "os.getenv",
}


def _expect_hold(exc_type, pattern, fn):
    try:
        fn()
    except exc_type as exc:
        assert pattern in str(exc), (pattern, str(exc))
    else:
        raise AssertionError(f"expected {exc_type.__name__}: {pattern}")


def _load():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED_SOURCE_SHA256
    spec = importlib.util.spec_from_file_location(
        "_void_abaddon_g2_observation_primitive_review",
        SOURCE,
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def test_static_source_has_no_collection_or_execution_surface():
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in FORBIDDEN_IMPORT_ROOTS
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".", 1)[0]
            assert root not in FORBIDDEN_IMPORT_ROOTS
        elif isinstance(node, ast.Call):
            assert _dotted(node.func) not in FORBIDDEN_CALLS


def test_contract_reviews_exact_six_candidates():
    m = _load()
    out = m.observation_primitive_review_contract()
    assert out["review_count"] == 6
    assert [row["primitive_id"] for row in out["reviews"]] == [
        "v8_environment_pure_validator",
        "v8_environment_live_verifier",
        "v8_asset_runtime_preload_verifier",
        "secure_unchanged_regular_file_read_pattern",
        "generic_designated_host_artifact_record",
        "generic_designated_host_runtime_snapshot",
    ]


def test_only_pure_v8_environment_validator_is_directly_admitted():
    m = _load()
    out = m.observation_primitive_review_contract()
    assert out["direct_generation2_reuse_admitted"] == (
        "v8_environment_pure_validator",
    )
    rows = {row["primitive_id"]: row for row in out["reviews"]}
    assert rows["v8_environment_pure_validator"]["direct_generation2_reuse_admitted"] is True
    for key, row in rows.items():
        if key != "v8_environment_pure_validator":
            assert row["direct_generation2_reuse_admitted"] is False


def test_v8_environment_pure_validator_is_supplied_fact_only():
    m = _load()
    row = m.primitive_review("v8_environment_pure_validator")
    assert row["canonical_function"] == m.V8_ENVIRONMENT_VALIDATOR
    assert row["classification"] == "admitted_pure_supplied_fact_validator"
    assert row["performs_collection"] is False
    assert row["performs_filesystem_io"] is False
    assert row["performs_subprocess"] is False
    assert row["inputs"] == ("python_major_minor", "pip_freeze_sha256")


def test_v8_live_environment_verifier_remains_collection_boundary():
    m = _load()
    row = m.primitive_review("v8_environment_live_verifier")
    assert row["canonical_function"] == m.V8_ENVIRONMENT_LIVE_VERIFIER
    assert row["classification"] == "collection_boundary_not_admitted"
    assert row["performs_collection"] is True
    assert row["performs_subprocess"] is True
    assert "pip freeze" in row["collection_detail"]
    assert "V8_LIVE_ENVIRONMENT_COLLECTION_NOT_REVIEWED" in row["holds"]


def test_v8_asset_verifier_remains_preload_not_evidence_primitive():
    m = _load()
    row = m.primitive_review("v8_asset_runtime_preload_verifier")
    assert row["canonical_function"] == m.V8_ASSET_VERIFIER
    assert row["verified_file_count"] == 17
    assert row["loads_model_weights"] is False
    assert row["direct_generation2_reuse_admitted"] is False
    assert "file open does not use O_NOFOLLOW" in row["evidence_gaps"]
    assert (
        "no same-descriptor fstat generation check before and after hashing"
        in row["evidence_gaps"]
    )


def test_secure_unchanged_read_is_design_reference_only():
    m = _load()
    row = m.primitive_review("secure_unchanged_regular_file_read_pattern")
    assert row["canonical_function"] == m.SPAR_UNCHANGED_READ
    assert row["classification"] == "admitted_design_reference_only"
    assert row["direct_generation2_reuse_admitted"] is False
    assert "opens with O_NOFOLLOW" in row["known_strengths"]
    assert "fstat identity checked before and after read" in row["known_strengths"]
    assert "private helper outside Generation-2 runtime surface" in row["limitations"]


def test_generic_artifact_record_is_not_strong_generation2_evidence():
    m = _load()
    row = m.primitive_review("generic_designated_host_artifact_record")
    assert row["canonical_function"] == m.GENERIC_ARTIFACT_RECORD
    assert row["classification"] == "generic_pattern_not_admitted"
    assert row["direct_generation2_reuse_admitted"] is False
    assert "opens with O_NOFOLLOW" in row["known_strengths"]
    assert (
        "no explicit fstat generation comparison after descriptor hashing"
        in row["evidence_gaps"]
    )


def test_generic_runtime_snapshot_is_partial_for_v2r13():
    m = _load()
    row = m.primitive_review("generic_designated_host_runtime_snapshot")
    assert row["canonical_function"] == m.GENERIC_RUNTIME_SNAPSHOT
    assert row["classification"] == "partial_git_observation_pattern_not_admitted"
    assert "collects HEAD commit" in row["known_strengths"]
    assert "collects full worktree dirty status" in row["known_strengths"]
    assert "does not collect HEAD^{tree}" in row["v2r13_gaps"]
    assert "does not prove frozen source detached HEAD" in row["v2r13_gaps"]


def test_future_file_observer_requirements_preserve_generation_stability():
    m = _load()
    req = m.future_file_observer_requirements()
    assert req == {
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


def test_future_v2r13_git_observer_requires_tree_clean_and_detached_source():
    m = _load()
    req = m.future_v2r13_git_observer_requirements()
    assert req["explicit_external_roots_only"] is True
    assert req["source_head_commit"] is True
    assert req["source_head_tree"] is True
    assert req["source_clean_full_worktree"] is True
    assert req["source_detached_head"] is True
    assert req["engine_head_commit"] is True
    assert req["engine_clean_full_worktree"] is True
    assert req["worktree_creation_permitted"] is False
    assert req["implemented"] is False


def test_v14_v10_identity_channels_remain_unresolved():
    m = _load()
    out = m.observation_primitive_review_contract()
    assert out["v14_identity_observation_still_unresolved"] is True
    assert out["v10_identity_observation_still_unresolved"] is True


def test_path_inputs_remain_explicit_external_inputs():
    m = _load()
    v8 = m.path_input_requirement(m.V8)
    v2 = m.path_input_requirement(m.V2R13)
    assert v8["source_kind"] == "explicit_external_input"
    assert v2["source_kind"] == "explicit_external_input"
    assert v8["caller_must_supply_all_paths"] is True
    assert v2["caller_must_supply_all_paths"] is True
    assert v8["tracked_source_defined_autodiscovery"] is False
    assert v2["tracked_source_defined_autodiscovery"] is False


def test_collection_boundary_set_is_exact():
    m = _load()
    out = m.observation_primitive_review_contract()
    assert out["collection_boundary_unadmitted"] == (
        "v8_environment_live_verifier",
        "v8_asset_runtime_preload_verifier",
        "generic_designated_host_artifact_record",
        "generic_designated_host_runtime_snapshot",
    )
    assert out["design_reference_only"] == (
        "secure_unchanged_regular_file_read_pattern",
    )


def test_all_review_rows_preserve_runtime_authority_false():
    m = _load()
    for row in m.observation_primitive_review_contract()["reviews"]:
        assert row["authority"]["filesystem_observation_performed"] is False
        assert row["authority"]["git_query_performed"] is False
        assert row["authority"]["subprocess_execution_performed"] is False
        assert row["authority"]["model_weights_loaded"] is False
        assert row["authority"]["runtime_started"] is False
        assert row["authority"]["runtime_execution_authorized"] is False


def test_unknown_primitive_holds():
    m = _load()
    _expect_hold(
        m.RuntimeObservationPrimitiveReviewHold,
        "unknown observation primitive",
        lambda: m.primitive_review("not-reviewed"),
    )


def test_execute_observation_primitive_always_holds():
    m = _load()
    _expect_hold(
        m.RuntimeObservationPrimitiveReviewHold,
        "GENERATION2_OBSERVATION_PRIMITIVE_EXECUTION_NOT_IMPLEMENTED",
        lambda: m.execute_observation_primitive(),
    )
