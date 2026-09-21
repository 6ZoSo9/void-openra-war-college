"""In-memory tests for structural scout result evidence review."""

from __future__ import annotations

import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_external_result_binding_v1 as binding
from openra_env.learning import abaddon_scout_external_result_evidence_review_v1 as review


ROOT = Path(__file__).resolve().parents[1]
HOLD = review.ScoutExternalResultEvidenceReviewHold
EXPERIMENT = "abaddon-scout-source-bound-v1-attempt-001"
OBSERVER_BLOB = review.POST_RUN_OBSERVER_CONTRACT_GIT_BLOB


def _canonical(value) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("ascii")


def _marker(**overrides):
    record = {
        "schema": review.ATTEMPT_MARKER_SCHEMA,
        "record_kind": review.ATTEMPT_RECORD_KIND,
        "experiment_id": EXPERIMENT,
        "request_sha256": review.REQUEST_SHA256,
        "launcher_contract_git_blob": review.LAUNCHER_CONTRACT_GIT_BLOB,
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
    record.update(overrides)
    return _canonical(record)


def _post_run(marker_sha256, *, observations=None, claims=None, **overrides):
    record = {
        "schema": review.POST_RUN_SCHEMA,
        "record_kind": "independent_post_run_state_declaration",
        "experiment_id": EXPERIMENT,
        "attempt_marker_sha256": marker_sha256,
        "observer_contract_git_blob": OBSERVER_BLOB,
        "observations": {
            field: True for field in review.REQUIRED_POST_RUN_OBSERVATIONS
        },
        "claims": {field: False for field in review.FALSE_POST_RUN_CLAIMS},
    }
    if observations is not None:
        record["observations"] = observations
    if claims is not None:
        record["claims"] = claims
    record.update(overrides)
    return _canonical(record)


def _package(*, marker=None, trajectory=None, result=None, post_run=None):
    marker = _marker() if marker is None else marker
    trajectory = b'{"synthetic":"trajectory"}\n' if trajectory is None else trajectory
    result = b'{"synthetic":"result"}\n' if result is None else result
    marker_sha = hashlib.sha256(marker).hexdigest()
    post_run = _post_run(marker_sha) if post_run is None else post_run

    payload = binding.build_scout_result_binding(
        experiment_id=EXPERIMENT,
        attempt_marker_sha256=marker_sha,
        trajectory_sha256=hashlib.sha256(trajectory).hexdigest(),
        result_payload_sha256=hashlib.sha256(result).hexdigest(),
        post_run_state_sha256=hashlib.sha256(post_run).hexdigest(),
    )
    return {
        "binding_payload": payload,
        "experiment_id": EXPERIMENT,
        "attempt_marker_bytes": marker,
        "trajectory_bytes": trajectory,
        "result_payload_bytes": result,
        "post_run_state_bytes": post_run,
    }


def test_exact_in_memory_package_binds_bytes_but_does_not_verify_final_evidence():
    package = _package()
    receipt = review.review_scout_result_evidence(**package)

    assert receipt["binding_bytes_verified"] is True
    assert receipt["attempt_marker_structure_verified"] is True
    assert receipt["trajectory_digest_verified"] is True
    assert receipt["result_payload_digest_verified"] is True
    assert receipt["post_run_state_structure_verified"] is True
    assert receipt["post_run_observer_contract_git_blob"] == OBSERVER_BLOB
    assert receipt["post_run_observer_contract_verified"] is True
    assert receipt["post_run_observer_implementation_verified"] is False
    assert receipt["result_evidence_verified"] is False
    assert receipt["next_gate"] == review.NEXT_GATE
    assert set(receipt["authority"]) == set(review.FALSE_AUTHORITY_FIELDS)
    assert all(value is False for value in receipt["authority"].values())


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("pair03_attempt_reused", True),
        ("pair03_attempt_reset", True),
        ("scout_execution_authorized", True),
        ("scout_execution_performed", True),
        ("reusable_execution_permit", True),
        ("automatic_retry", True),
        ("training_authorized", True),
        ("automatic_policy_promotion", True),
        ("single_use_scope", False),
    ],
)
def test_attempt_marker_authority_or_reuse_drift_fails_even_with_matching_digest(field, value):
    marker = _marker(**{field: value})
    package = _package(marker=marker)
    with pytest.raises(HOLD):
        review.review_scout_result_evidence(**package)


def test_attempt_marker_wrong_experiment_or_source_identity_fails():
    for marker in (
        _marker(experiment_id="abaddon-scout-other"),
        _marker(request_sha256="0" * 64),
        _marker(launcher_contract_git_blob="0" * 40),
    ):
        with pytest.raises(HOLD):
            review.review_scout_result_evidence(**_package(marker=marker))


@pytest.mark.parametrize("field", review.REQUIRED_POST_RUN_OBSERVATIONS)
def test_every_required_post_run_observation_must_be_true(field):
    observations = {name: True for name in review.REQUIRED_POST_RUN_OBSERVATIONS}
    observations[field] = False

    marker = _marker()
    post_run = _post_run(hashlib.sha256(marker).hexdigest(), observations=observations)
    with pytest.raises(HOLD, match="OBSERVATION_REQUIRED"):
        review.review_scout_result_evidence(
            **_package(marker=marker, post_run=post_run)
        )


@pytest.mark.parametrize("field", review.FALSE_POST_RUN_CLAIMS)
def test_every_forbidden_post_run_claim_must_remain_false(field):
    claims = {name: False for name in review.FALSE_POST_RUN_CLAIMS}
    claims[field] = True

    marker = _marker()
    post_run = _post_run(hashlib.sha256(marker).hexdigest(), claims=claims)
    with pytest.raises(HOLD, match="FALSE_REQUIRED"):
        review.review_scout_result_evidence(
            **_package(marker=marker, post_run=post_run)
        )


def test_post_run_attempt_digest_and_observer_contract_identity_are_bound():
    marker = _marker()
    marker_sha = hashlib.sha256(marker).hexdigest()

    wrong_digest = _post_run("0" * 64)
    with pytest.raises(HOLD, match="ATTEMPT_DIGEST"):
        review.review_scout_result_evidence(
            **_package(marker=marker, post_run=wrong_digest)
        )

    invalid_observer = _post_run(marker_sha, observer_contract_git_blob="0" * 40)
    with pytest.raises(HOLD, match="OBSERVER_CONTRACT_IDENTITY"):
        review.review_scout_result_evidence(
            **_package(marker=marker, post_run=invalid_observer)
        )


def test_noncanonical_or_extended_evidence_fails_closed():
    marker = _marker()
    marker_sha = hashlib.sha256(marker).hexdigest()
    post = json.loads(_post_run(marker_sha))
    post["extra"] = False

    with pytest.raises(HOLD, match="POST_RUN_FIELDS"):
        review.review_scout_result_evidence(
            **_package(marker=marker, post_run=_canonical(post))
        )

    pretty = json.dumps(json.loads(_post_run(marker_sha)), indent=2).encode("ascii")
    with pytest.raises(HOLD, match="NONCANONICAL"):
        review.review_scout_result_evidence(
            **_package(marker=marker, post_run=pretty)
        )


def test_binding_must_match_the_actual_supplied_bytes():
    package = _package()
    original = package["binding_payload"]

    changed_trajectory = b'{"synthetic":"other-trajectory"}\n'
    package["trajectory_bytes"] = changed_trajectory
    package["binding_payload"] = original

    with pytest.raises(binding.ScoutExternalResultBindingHold, match="BYTES_DRIFT"):
        review.review_scout_result_evidence(**package)


def test_byte_type_and_size_limits_fail_before_review():
    package = _package()
    package["trajectory_bytes"] = bytearray(package["trajectory_bytes"])
    with pytest.raises(HOLD, match="EXACT_BYTES_REQUIRED"):
        review.review_scout_result_evidence(**package)

    package = _package()
    package["post_run_state_bytes"] = b"x" * (review.MAX_POST_RUN_STATE_BYTES + 1)
    with pytest.raises(HOLD, match="BYTE_LIMIT"):
        review.review_scout_result_evidence(**package)


@pytest.mark.parametrize(
    ("entrypoint", "kwargs"),
    [
        (review.accept_result_as_verified, {}),
        (review.accept_result_as_verified, {"verified": True}),
        (review.authorize_or_execute, {}),
        (review.authorize_or_execute, {"authorized": True}),
    ],
)
def test_final_acceptance_and_execution_entrypoints_hold(entrypoint, kwargs):
    with pytest.raises(HOLD, match=review.NEXT_GATE):
        entrypoint(**kwargs)


def test_review_source_has_no_filesystem_process_network_or_runtime_calls():
    path = ROOT / "openra_env/learning/abaddon_scout_external_result_evidence_review_v1.py"
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.add(node.module)

    assert modules == {
        "__future__",
        "hashlib",
        "json",
        "typing",
        "openra_env.learning",
    }
    for forbidden in (
        "pathlib",
        "os.",
        "subprocess",
        "socket",
        "requests",
        "httpx",
        "open(",
        "run_main_once(",
        "consume_scout_attempt(",
    ):
        assert forbidden not in source
    assert 'if __name__ ==' not in source
