"""Source-binding tests for the external scout launcher contract."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_external_launcher_contract_review_v1 as review
from openra_env.learning import abaddon_scout_external_launcher_contract_v1 as contract


ROOT = Path(__file__).resolve().parents[1]
HOLD = review.ScoutExternalLauncherSourceReviewHold


def _git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def test_review_manifest_binds_exact_contract_source_and_request():
    path = ROOT / review.CONTRACT_PATH
    assert path.is_file() and not path.is_symlink()
    data = path.read_bytes()

    assert _git_blob(data) == review.CONTRACT_GIT_BLOB
    assert review.CONTRACT_GIT_BLOB == "1f7ee7057c27946f488afe26501482ea4f4fc53d"
    assert contract.REQUEST_SHA256 == review.CONTRACT_REQUEST_SHA256
    assert hashlib.sha256(contract.build_scout_launcher_request()).hexdigest() == (
        review.CONTRACT_REQUEST_SHA256
    )

    receipt = review.source_binding_review_contract()
    assert receipt["bound_main_head"] == "9a151da589f93454d31a475b29297ea8a3d35442"
    assert receipt["contract_path"] == review.CONTRACT_PATH
    assert receipt["contract_git_blob"] == review.CONTRACT_GIT_BLOB
    assert receipt["contract_request_sha256"] == review.CONTRACT_REQUEST_SHA256
    assert receipt["next_gate"] == "SCOUT_FRESH_DURABLE_ATTEMPT_GUARD_REQUIRED"


def test_source_review_remains_non_authorizing():
    receipt = review.source_binding_review_contract()
    assert receipt["review_kind"] == "source_binding_expectation_not_runtime_authority"
    assert receipt["source_identity_expectation_recorded"] is True
    assert receipt["pair03_attempt_reuse_allowed"] is False
    assert receipt["automatic_retry"] is False
    assert receipt["automatic_training_admission"] is False
    assert receipt["automatic_policy_promotion"] is False
    assert len(receipt["authority"]) == len(review.FALSE_AUTHORITY_FIELDS)
    assert set(receipt["authority"]) == set(review.FALSE_AUTHORITY_FIELDS)
    assert all(value is False for value in receipt["authority"].values())


@pytest.mark.parametrize(
    ("entrypoint", "kwargs"),
    [
        (review.authorize_or_execute, {}),
        (review.authorize_or_execute, {"authorized": True}),
        (review.consume_attempt, {}),
        (review.consume_attempt, {"confirm": "CONSUME"}),
        (review.accept_result, {}),
        (review.accept_result, {"verified": True}),
    ],
)
def test_all_effect_or_acceptance_entrypoints_hold(entrypoint, kwargs):
    with pytest.raises(HOLD, match=review.NEXT_GATE):
        entrypoint(**kwargs)


def test_public_review_snapshot_is_fresh():
    first = review.source_binding_review_contract()
    first["authority"]["scout_execution_authorized"] = True
    first["pair03_attempt_reuse_allowed"] = True

    later = review.source_binding_review_contract()
    assert later["authority"]["scout_execution_authorized"] is False
    assert later["pair03_attempt_reuse_allowed"] is False


def test_review_module_has_no_runtime_filesystem_network_or_local_imports():
    path = ROOT / "openra_env/learning/abaddon_scout_external_launcher_contract_review_v1.py"
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.add(node.module)

    assert modules == {"__future__", "typing"}
    for forbidden in (
        "subprocess",
        "socket",
        "requests",
        "httpx",
        "pathlib",
        "importlib",
        "hashlib",
        "open(",
        "os.",
        "run_main_once(",
    ):
        assert forbidden not in source
    assert 'if __name__ ==' not in source
