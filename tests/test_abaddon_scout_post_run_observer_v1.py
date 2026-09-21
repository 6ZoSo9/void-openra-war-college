"""Tests for the bounded injected scout post-run observer adapter."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_external_result_binding_v1 as binding
from openra_env.learning import abaddon_scout_external_result_evidence_review_v1 as evidence
from openra_env.learning import abaddon_scout_post_run_observer_v1 as observer


ROOT = Path(__file__).resolve().parents[1]
HOLD = observer.ScoutPostRunObserverHold
EXPERIMENT = "abaddon-scout-source-bound-v1-attempt-001"
ATTEMPT_SHA = "a" * 64


def _probes(events=None, overrides=None):
    events = [] if events is None else events
    overrides = {} if overrides is None else overrides

    def make(name):
        def probe():
            events.append(("probe", name))
            value = overrides.get(name, True)
            if isinstance(value, BaseException):
                raise value
            return value

        return probe

    return {name: make(name) for name in observer.REQUIRED_OBSERVATIONS}


def _authority(events=None, values=None):
    events = [] if events is None else events
    sequence = iter([True] * 100 if values is None else values)

    def check():
        events.append(("authority", len([x for x in events if x[0] == "authority"]) + 1))
        value = next(sequence)
        if isinstance(value, BaseException):
            raise value
        return value

    return check


def _canonical(value):
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("ascii")


def _attempt_marker():
    return _canonical(
        {
            "schema": evidence.ATTEMPT_MARKER_SCHEMA,
            "record_kind": evidence.ATTEMPT_RECORD_KIND,
            "experiment_id": EXPERIMENT,
            "request_sha256": evidence.REQUEST_SHA256,
            "launcher_contract_git_blob": evidence.LAUNCHER_CONTRACT_GIT_BLOB,
            "single_use_scope": True,
            "pair03_attempt_reused": False,
            "pair03_attempt_reset": False,
            "scout_execution_authorized": False,
            "scout_execution_performed": False,
            "reusable_execution_permit": False,
            "automatic_retry": False,
            "training_authorized": False,
            "automatic_policy_promotion": False,
        }
    )


def test_success_calls_each_probe_once_in_fixed_authority_then_probe_order():
    events = []
    raw = observer.observe_post_run_state(
        experiment_id=EXPERIMENT,
        attempt_marker_sha256=ATTEMPT_SHA,
        observer_contract_git_blob=observer.OBSERVER_CONTRACT_GIT_BLOB,
        read_authority_check=_authority(events),
        probes=_probes(events),
    )
    record = json.loads(raw)

    expected = []
    for index, name in enumerate(observer.REQUIRED_OBSERVATIONS, start=1):
        expected.extend([("authority", index), ("probe", name)])
    assert events == expected

    assert record["schema"] == observer.EVIDENCE_SCHEMA
    assert record["record_kind"] == "independent_post_run_state_declaration"
    assert record["experiment_id"] == EXPERIMENT
    assert record["attempt_marker_sha256"] == ATTEMPT_SHA
    assert record["observer_contract_git_blob"] == observer.OBSERVER_CONTRACT_GIT_BLOB
    assert tuple(record["observations"]) == tuple(sorted(observer.REQUIRED_OBSERVATIONS))
    assert all(record["observations"][name] is True for name in observer.REQUIRED_OBSERVATIONS)
    assert set(record["claims"]) == set(observer.FALSE_CLAIMS)
    assert all(value is False for value in record["claims"].values())
    assert raw == _canonical(record)


@pytest.mark.parametrize("stop_index", range(5))
def test_revoked_read_authority_stops_before_corresponding_probe(stop_index):
    events = []
    values = [True] * stop_index + [False]

    with pytest.raises(HOLD, match="AUTHORITY_REQUIRED"):
        observer.observe_post_run_state(
            experiment_id=EXPERIMENT,
            attempt_marker_sha256=ATTEMPT_SHA,
            observer_contract_git_blob=observer.OBSERVER_CONTRACT_GIT_BLOB,
            read_authority_check=_authority(events, values),
            probes=_probes(events),
        )

    assert sum(event[0] == "probe" for event in events) == stop_index


@pytest.mark.parametrize("value", [False, None, 1, "true"])
def test_non_literal_true_probe_result_holds_without_retry(value):
    events = []
    name = observer.REQUIRED_OBSERVATIONS[2]

    with pytest.raises(HOLD, match="POSITIVE_OBSERVATION_REQUIRED"):
        observer.observe_post_run_state(
            experiment_id=EXPERIMENT,
            attempt_marker_sha256=ATTEMPT_SHA,
            observer_contract_git_blob=observer.OBSERVER_CONTRACT_GIT_BLOB,
            read_authority_check=_authority(events),
            probes=_probes(events, {name: value}),
        )

    assert events.count(("probe", name)) == 1


def test_probe_exception_is_sanitized_and_not_retried():
    events = []
    name = observer.REQUIRED_OBSERVATIONS[1]

    with pytest.raises(HOLD, match="PROBE_ERROR:runtime_service_inactive:ValueError"):
        observer.observe_post_run_state(
            experiment_id=EXPERIMENT,
            attempt_marker_sha256=ATTEMPT_SHA,
            observer_contract_git_blob=observer.OBSERVER_CONTRACT_GIT_BLOB,
            read_authority_check=_authority(events),
            probes=_probes(events, {name: ValueError("secret detail")}),
        )

    assert events.count(("probe", name)) == 1


def test_authority_exception_is_sanitized_before_probe():
    events = []
    with pytest.raises(HOLD, match="AUTHORITY_ERROR:RuntimeError"):
        observer.observe_post_run_state(
            experiment_id=EXPERIMENT,
            attempt_marker_sha256=ATTEMPT_SHA,
            observer_contract_git_blob=observer.OBSERVER_CONTRACT_GIT_BLOB,
            read_authority_check=_authority(events, [RuntimeError("secret detail")]),
            probes=_probes(events),
        )
    assert not any(event[0] == "probe" for event in events)


@pytest.mark.parametrize(
    "override",
    [
        {"experiment_id": ""},
        {"experiment_id": "abaddon-scout-pair03-reuse"},
        {"experiment_id": "Abaddon-scout-upper"},
        {"attempt_marker_sha256": "A" * 64},
        {"attempt_marker_sha256": "a" * 63},
        {"observer_contract_git_blob": "0" * 40},
        {"read_authority_check": True},
        {"probes": {}},
    ],
)
def test_invalid_inputs_fail_before_any_probe(override):
    events = []
    args = {
        "experiment_id": EXPERIMENT,
        "attempt_marker_sha256": ATTEMPT_SHA,
        "observer_contract_git_blob": observer.OBSERVER_CONTRACT_GIT_BLOB,
        "read_authority_check": _authority(events),
        "probes": _probes(events),
    }
    args.update(override)

    with pytest.raises(HOLD):
        observer.observe_post_run_state(**args)
    assert not any(event[0] == "probe" for event in events)


def test_observer_output_composes_with_structural_evidence_review():
    marker = _attempt_marker()
    marker_sha = hashlib.sha256(marker).hexdigest()
    trajectory = b'{"synthetic":"trajectory"}\n'
    result_payload = b'{"synthetic":"result"}\n'

    post_run = observer.observe_post_run_state(
        experiment_id=EXPERIMENT,
        attempt_marker_sha256=marker_sha,
        observer_contract_git_blob=observer.OBSERVER_CONTRACT_GIT_BLOB,
        read_authority_check=_authority(),
        probes=_probes(),
    )

    binding_payload = binding.build_scout_result_binding(
        experiment_id=EXPERIMENT,
        attempt_marker_sha256=marker_sha,
        trajectory_sha256=hashlib.sha256(trajectory).hexdigest(),
        result_payload_sha256=hashlib.sha256(result_payload).hexdigest(),
        post_run_state_sha256=hashlib.sha256(post_run).hexdigest(),
    )

    receipt = evidence.review_scout_result_evidence(
        binding_payload=binding_payload,
        experiment_id=EXPERIMENT,
        attempt_marker_bytes=marker,
        trajectory_bytes=trajectory,
        result_payload_bytes=result_payload,
        post_run_state_bytes=post_run,
    )

    assert receipt["post_run_observer_contract_verified"] is True
    assert receipt["post_run_observer_implementation_verified"] is False
    assert receipt["result_evidence_verified"] is False
    assert receipt["next_gate"] == "SCOUT_POST_RUN_OBSERVER_IMPLEMENTATION_REVIEW_REQUIRED"


def test_execution_entrypoint_always_holds():
    with pytest.raises(HOLD, match="EXECUTION_AUTHORITY_UNAVAILABLE"):
        observer.authorize_or_execute(authorized=True)


def test_source_contains_no_direct_host_runtime_or_mutation_backends():
    path = ROOT / "openra_env/learning/abaddon_scout_post_run_observer_v1.py"
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.add(node.module)

    assert modules == {"__future__", "json", "typing"}
    for forbidden in (
        "pathlib",
        "hashlib",
        "os.",
        "subprocess",
        "socket",
        "requests",
        "httpx",
        "systemctl",
        "docker",
        "git ",
        "open(",
        "unlink",
        "remove(",
        "kill(",
    ):
        assert forbidden not in source
    assert 'if __name__ ==' not in source
