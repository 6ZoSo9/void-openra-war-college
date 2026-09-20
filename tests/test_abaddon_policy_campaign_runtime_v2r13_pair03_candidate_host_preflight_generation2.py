"""Candidate preflight: real temporary file reads, inert host/runtime fixtures."""
from __future__ import annotations

import ast
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_host_preflight_generation2 as candidate,
)

HOLD = candidate.CandidateHostPreflightHold
HEAD = "a" * 40
REPO = Path(__file__).resolve().parents[1]


def arm_rows(root):
    return {f"{pair}:{arm}": {
        "path": str(root / "generation2" / f"pair-{pair:02d}" / arm),
        "exists": pair == 3 and arm == "baseline",
    } for pair in (3, 9, 15) for arm in ("baseline", "candidate")}


@pytest.fixture
def layout(tmp_path, monkeypatch):
    root = tmp_path / "isolated"
    run = root / candidate.BASELINE_RUN_REL
    run.mkdir(parents=True)
    fixture_bytes = {"trajectory.jsonl": b'{"fixture":"trajectory"}\n',
                     "summary.json": b'{"outcome":"DRAW_OR_UNFINISHED","fixture":true}\n'}
    files = tuple((name, hashlib.sha256(data).hexdigest(), 4096) for name, data in fixture_bytes.items())
    for name, data in fixture_bytes.items():
        (run / name).write_bytes(data)
    monkeypatch.setattr(candidate, "ISOLATED_ROOT", root)
    monkeypatch.setattr(candidate, "BASELINE_FILES", files)
    monkeypatch.setattr(candidate, "request", SimpleNamespace(candidate_authorization_request_contract=lambda: {
        "request": {"baseline_reference": {
            "trajectory_sha256": files[0][1], "summary_sha256": files[1][1],
        }},
    }))
    snapshot = {"expected_main_head": HEAD, "isolated_workdir": {
        "root": str(root), "authorized_arm_paths": arm_rows(root),
    }, "untouched_fixture": {"identity": "retain", "checks": [1, 2, 3]}}
    received = []

    def legacy_check(projected):
        received.append(deepcopy(projected))
        assert all(row["exists"] is False for row in projected["isolated_workdir"]["authorized_arm_paths"].values())
        return {"host_preflight_green": True, "snapshot_sha256": candidate._digest(projected),
                "runtime_execution_authorized": True}

    monkeypatch.setattr(candidate, "_collect_host_snapshot", lambda head: deepcopy(snapshot))
    monkeypatch.setattr(candidate, "_legacy_validator", lambda: SimpleNamespace(validate_host_preflight_snapshot=legacy_check))
    return SimpleNamespace(root=root, run=run, snapshot=snapshot, received=received, data=fixture_bytes, files=files)


def collect(**overrides):
    return candidate.collect_pair03_candidate_host_preflight(**{
        "expected_main_head": HEAD, "confirm": candidate.CONFIRM_TOKEN, **overrides,
    })


def test_real_baseline_files_remain_present_and_true_snapshot_is_retained(layout):
    before = {name: ((layout.run / name).read_bytes(), (layout.run / name).stat().st_mode) for name in layout.data}
    out = collect()
    assert out["candidate_host_conditions_validated"] is True
    assert out["observed_host_snapshot"] == layout.snapshot
    assert out["observed_host_snapshot"]["isolated_workdir"]["authorized_arm_paths"]["3:baseline"]["exists"] is True
    assert out["observed_host_snapshot_sha256"] == candidate._digest(layout.snapshot)
    projected = deepcopy(layout.snapshot)
    projected["isolated_workdir"]["authorized_arm_paths"]["3:baseline"]["exists"] = False
    assert layout.received == [projected]  # Exactly one changed predicate, no other exemption.
    assert out["legacy_structural_projection_sha256"] == candidate._digest(projected)
    assert out["legacy_structural_projection_sha256"] != out["observed_host_snapshot_sha256"]
    for key in ("legacy_structural_projection_is_host_observation", "legacy_runtime_authority_inherited",
                "candidate_execution_authorized", "candidate_execution_performed", "single_use_attempt_consumed",
                "runtime_started", "model_load_performed", "game_execution_performed",
                "independent_host_attestation", "atomic_host_snapshot"):
        assert out[key] is False
    assert out["completed_baseline_preserved"] is True
    assert {name: ((layout.run / name).read_bytes(), (layout.run / name).stat().st_mode) for name in layout.data} == before
    assert sorted(p.name for p in layout.run.iterdir()) == sorted(layout.data)
    for name, digest, _ in layout.files:
        assert out["baseline_files"][name] == {"path": str(layout.run / name), "sha256": digest,
                                               "bytes": len(layout.data[name])}


def test_results_do_not_share_snapshot_state(layout):
    first = collect()
    first["observed_host_snapshot"]["untouched_fixture"]["checks"].clear()
    first["baseline_files"].clear()
    second = collect()
    assert second["observed_host_snapshot"] == layout.snapshot
    assert len(second["baseline_files"]) == 2


@pytest.mark.parametrize("overrides", [
    {"confirm": None}, {"confirm": True}, {"confirm": ""},
    {"confirm": "VOID_ABADDON_GENERATION2_V2R13_EXECUTE_PAIR03_BASELINE"},
    {"expected_main_head": "A" * 40}, {"expected_main_head": "a" * 39},
    {"expected_main_head": "x" * 40}, {"expected_main_head": 42},
])
def test_invalid_call_does_not_collect_or_touch_files(monkeypatch, overrides):
    def forbidden(*args, **kwargs):
        raise AssertionError("unexpected collection")
    monkeypatch.setattr(candidate, "_collect_host_snapshot", forbidden)
    monkeypatch.setattr(candidate, "_arm_census", forbidden)
    with pytest.raises(HOLD):
        collect(**overrides)


@pytest.mark.parametrize("pair,arm", [(3, "candidate"), (9, "baseline"), (9, "candidate"), (15, "baseline"), (15, "candidate")])
def test_other_existing_arm_is_not_waived(layout, pair, arm):
    (layout.root / "generation2" / f"pair-{pair:02d}" / arm).mkdir(parents=True)
    with pytest.raises(HOLD, match="ARM_LAYOUT"):
        collect()
    assert layout.received == []


@pytest.mark.parametrize("mutation", ["baseline_absent", "baseline_numeric", "candidate_present", "path_drift", "extra_row", "missing_row", "extra_field", "root_drift", "head_drift"])
def test_snapshot_layout_mismatch_is_not_projected_away(layout, mutation):
    rows = layout.snapshot["isolated_workdir"]["authorized_arm_paths"]
    if mutation == "baseline_absent": rows["3:baseline"]["exists"] = False
    elif mutation == "baseline_numeric": rows["3:baseline"]["exists"] = 1
    elif mutation == "candidate_present": rows["3:candidate"]["exists"] = True
    elif mutation == "path_drift": rows["3:baseline"]["path"] += "-wrong"
    elif mutation == "extra_row": rows["30:baseline"] = deepcopy(rows["3:baseline"])
    elif mutation == "missing_row": del rows["15:baseline"]
    elif mutation == "extra_field": rows["3:baseline"]["allow_retry"] = True
    elif mutation == "root_drift": layout.snapshot["isolated_workdir"]["root"] += "-other"
    elif mutation == "head_drift": layout.snapshot["expected_main_head"] = "b" * 40
    with pytest.raises(HOLD):
        collect()
    assert layout.received == []


@pytest.mark.parametrize("kind", ["symlink", "dangling", "file", "fifo"])
def test_candidate_non_directory_is_not_mistaken_for_absence(layout, kind):
    path = layout.root / "generation2/pair-03/candidate"
    if kind == "symlink": path.symlink_to(layout.run, target_is_directory=True)
    elif kind == "dangling": path.symlink_to(layout.root / "missing")
    elif kind == "file": path.write_bytes(b"preserve")
    else: os.mkfifo(path)
    with pytest.raises(HOLD, match="ARM_NOT_DIRECTORY"):
        collect()
    assert path.lstat()


@pytest.mark.parametrize("kind", ["missing", "symlink", "directory", "fifo", "hardlink", "empty", "oversized", "wrong_hash"])
def test_baseline_file_rejections_preserve_evidence(layout, kind):
    path = layout.run / "trajectory.jsonl"
    original = path.read_bytes()
    path.unlink()  # Fixture setup only, never the production collector.
    if kind == "missing": pass
    elif kind == "symlink": path.symlink_to(layout.run / "summary.json")
    elif kind == "directory": path.mkdir()
    elif kind == "fifo": os.mkfifo(path)
    elif kind == "hardlink": os.link(layout.run / "summary.json", path)
    elif kind == "empty": path.write_bytes(b"")
    elif kind == "oversized": path.write_bytes(b"x" * 4097)
    else: path.write_bytes(original.replace(b"fixture", b"changed"))
    with pytest.raises(HOLD):
        collect()
    assert layout.received == []
    assert (layout.run / "summary.json").read_bytes() == layout.data["summary.json"]


def test_symlinked_ancestor_is_not_followed(layout):
    parent = layout.run.parent
    moved = parent.with_name("retained-runs")
    parent.rename(moved)
    parent.symlink_to(moved, target_is_directory=True)
    with pytest.raises(HOLD, match="FILESYSTEM"):
        collect()
    assert (moved / candidate.BASELINE_RUN_ID / "trajectory.jsonl").read_bytes() == layout.data["trajectory.jsonl"]


def test_short_reads_can_complete(layout, monkeypatch):
    original = os.read
    monkeypatch.setattr(candidate.os, "read", lambda fd, count: original(fd, min(3, count)))
    assert collect()["candidate_host_conditions_validated"] is True


@pytest.mark.parametrize("fault", ["empty", "error", "mutate", "replace"])
def test_read_failure_or_identity_change_never_admits(layout, monkeypatch, fault):
    original = os.read
    touched = False
    path = layout.run / "trajectory.jsonl"
    def read(fd, count):
        nonlocal touched
        if fault == "empty": return b""
        if fault == "error": raise OSError("inert fixture I/O")
        data = original(fd, count)
        if not touched:
            touched = True
            if fault == "mutate":
                path.write_bytes(b"changed" * 7)
            else:
                path.rename(layout.run / "retained-original")
                path.write_bytes(layout.data["trajectory.jsonl"])
        return data
    monkeypatch.setattr(candidate.os, "read", read)
    with pytest.raises(HOLD):
        collect()
    assert layout.received == []


def test_read_call_bound_is_enforced(layout, monkeypatch):
    path = layout.run / "trajectory.jsonl"
    path.write_bytes(b"z" * 2048)
    original = os.read
    calls = 0
    def tiny(fd, count):
        nonlocal calls
        calls += 1
        return original(fd, min(count, 1))
    monkeypatch.setattr(candidate.os, "read", tiny)
    with pytest.raises(HOLD, match="READ_BOUND"):
        candidate._read_baseline_file(path.name, hashlib.sha256(path.read_bytes()).hexdigest(), 4096)
    assert calls == 1024


def test_legacy_failure_is_not_turned_into_candidate_success(layout, monkeypatch):
    def refuse(_):
        raise ValueError("inert legacy host finding")
    monkeypatch.setattr(candidate, "_legacy_validator", lambda: SimpleNamespace(validate_host_preflight_snapshot=refuse))
    with pytest.raises(ValueError, match="legacy host finding"):
        collect()


@pytest.mark.parametrize("bad", ["green", "digest"])
def test_malformed_legacy_admission_is_not_used(layout, monkeypatch, bad):
    def result(projection):
        return {"host_preflight_green": bad != "green", "snapshot_sha256": "0" * 64 if bad == "digest" else candidate._digest(projection)}
    monkeypatch.setattr(candidate, "_legacy_validator", lambda: SimpleNamespace(validate_host_preflight_snapshot=result))
    with pytest.raises(HOLD, match="SHARED_CHECKS"):
        collect()


def test_changed_layout_after_hashing_stops_collection(layout, monkeypatch):
    original = candidate._arm_census
    count = 0
    def census():
        nonlocal count
        count += 1
        if count == 2:
            (layout.root / "generation2/pair-03/candidate").mkdir()
        return original()
    monkeypatch.setattr(candidate, "_arm_census", census)
    with pytest.raises(HOLD, match="ARM_LAYOUT"):
        collect()
    assert count == 2


def test_fd_count_returns_to_baseline_after_success_and_failure(layout):
    before = len(list(Path("/proc/self/fd").iterdir()))
    collect()
    assert len(list(Path("/proc/self/fd").iterdir())) == before
    (layout.run / "summary.json").write_bytes(b"bad")
    with pytest.raises(HOLD): collect()
    assert len(list(Path("/proc/self/fd").iterdir())) == before


def test_fixed_canonical_pins_and_no_runtime_mutation_entrypoint():
    baseline = candidate.request.candidate_authorization_request_contract()["request"]["baseline_reference"]
    assert candidate.BASELINE_FILES[0][1] == baseline["trajectory_sha256"]
    assert candidate.BASELINE_FILES[1][1] == baseline["summary_sha256"]
    assert candidate.BASELINE_RUN_ID == "warmstart-apollyon-vs-abaddon-20260919T203512Z-feinter-s1990061685"
    assert str(candidate.ISOLATED_ROOT) == "/home/zoso/dev/void-war-college-execution/v2r13-generation2"
    source = Path(candidate.__file__).read_text()
    tree = ast.parse(source)
    calls = {node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}
    assert not calls.intersection({"mkdir", "unlink", "rename", "replace", "write", "fchmod", "consume_candidate_attempt", "execute_v2r13_arm"})
    assert 'if __name__ ==' not in source


# These tests run normally in unfiltered hosted CI. They require the complete
# checkout/import graph, unavailable in the isolated local source workspace.
@pytest.mark.parametrize("mutation", [None, "hostname", "main", "engine", "image", "rootless", "service", "permit", "external", "tracked", "authority"])
def test_complete_repository_real_legacy_validator_composition(monkeypatch, mutation):
    fixture_path = REPO / "tests/test_abaddon_policy_campaign_runtime_v2r13_host_preflight_generation2.py"
    spec = importlib.util.spec_from_file_location("candidate_preflight_original_test_fixture", fixture_path)
    fixture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixture)
    snapshot = fixture.valid_snapshot()
    snapshot["isolated_workdir"]["root"] = str(candidate.ISOLATED_ROOT)
    snapshot["isolated_workdir"]["path"] = str(candidate.ISOLATED_ROOT)
    snapshot["isolated_workdir"]["authorized_arm_paths"] = arm_rows(candidate.ISOLATED_ROOT)
    legacy = candidate._legacy_validator()
    with pytest.raises(legacy.V2R13HostPreflightHold, match="arm-path already exists: 3:baseline"):
        legacy.validate_host_preflight_snapshot(snapshot)
    if mutation == "hostname": snapshot["hostname"] = "wrong"
    elif mutation == "main": snapshot["source_repository"]["head"] = "f" * 40
    elif mutation == "engine": snapshot["engine_repository"]["tracked_status"] = " M engine"
    elif mutation == "image": snapshot["docker"]["image_id"] = "wrong"
    elif mutation == "rootless": snapshot["docker"]["context"] = "default"
    elif mutation == "service": snapshot["ollama"]["active"] = "active"
    elif mutation == "permit": snapshot["ollama"]["activation_permit_present"] = True
    elif mutation == "external": snapshot["external_files"]["legacy_warm_start_runner"]["sha256"] = "0" * 64
    elif mutation == "tracked": snapshot["source_repository"]["tracked_blobs"]["executor_source"]["blob"] = "0" * 40
    elif mutation == "authority": snapshot["authority"]["runtime_start_performed"] = True
    monkeypatch.setattr(candidate, "_collect_host_snapshot", lambda head: deepcopy(snapshot))
    monkeypatch.setattr(candidate, "_arm_census", lambda: None)
    monkeypatch.setattr(candidate, "_read_baseline_file", lambda name, digest, cap: {
        "path": str(candidate.ISOLATED_ROOT / candidate.BASELINE_RUN_REL / name), "sha256": digest, "bytes": 100,
    })
    if mutation:
        with pytest.raises(legacy.V2R13HostPreflightHold): collect()
    else:
        assert collect()["candidate_execution_authorized"] is False


def test_complete_repository_dependency_blobs_are_preserved():
    for relative, expected in candidate.DEPENDENCY_GIT_BLOBS:
        raw = (REPO / relative).read_bytes()
        assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == expected, relative
