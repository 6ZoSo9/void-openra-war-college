"""Source-only tests for the external scout result-binding declaration."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_external_result_binding_v1 as binding


ROOT = Path(__file__).resolve().parents[1]
HOLD = binding.ScoutExternalResultBindingHold
EXPERIMENT = "abaddon-scout-source-bound-v1-attempt-001"
ATTEMPT = "a" * 64
TRAJECTORY = "b" * 64
RESULT = "c" * 64
POST = "d" * 64


def _build(**overrides):
    values = {
        "experiment_id": EXPERIMENT,
        "attempt_marker_sha256": ATTEMPT,
        "trajectory_sha256": TRAJECTORY,
        "result_payload_sha256": RESULT,
        "post_run_state_sha256": POST,
    }
    values.update(overrides)
    return binding.build_scout_result_binding(**values), values


def _git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def test_canonical_binding_is_stable_and_non_authorizing():
    payload, values = _build()
    record = json.loads(payload)

    assert payload.endswith(b"\n") and not payload.endswith(b"\n\n")
    assert 0 < len(payload) <= binding.MAX_BINDING_BYTES
    assert record["record_kind"] == "declared_identities_not_verified_evidence"
    assert record["experiment_id"] == EXPERIMENT
    assert record["declared_digests"] == {
        "attempt_marker_sha256": ATTEMPT,
        "trajectory_sha256": TRAJECTORY,
        "result_payload_sha256": RESULT,
        "post_run_state_sha256": POST,
    }
    assert record["pair03_attempt_reuse_allowed"] is False
    assert record["pair03_attempt_reset_allowed"] is False
    assert record["automatic_retry"] is False
    assert record["declared_digest_is_self_authenticating"] is False
    assert record["callback_return_proves_shutdown"] is False
    assert record["historical_cleanup_prints_prove_shutdown"] is False

    validated = binding.validate_scout_result_binding(payload, **values)
    assert validated["binding_bytes_valid"] is True
    assert validated["binding_sha256"] == hashlib.sha256(payload).hexdigest()
    assert validated["binding_bytes"] == len(payload)
    assert validated["next_gate"] == binding.NEXT_GATE


def test_verification_and_authority_fields_remain_false():
    payload, values = _build()
    record = json.loads(payload)
    validated = binding.validate_scout_result_binding(payload, **values)

    assert set(record["verification"]) == set(binding.FALSE_VERIFICATION_FIELDS)
    assert set(validated["verification"]) == set(binding.FALSE_VERIFICATION_FIELDS)
    assert all(value is False for value in record["verification"].values())
    assert all(value is False for value in validated["verification"].values())

    assert set(record["authority"]) == set(binding.FALSE_AUTHORITY_FIELDS)
    assert set(validated["authority"]) == set(binding.FALSE_AUTHORITY_FIELDS)
    assert all(value is False for value in record["authority"].values())
    assert all(value is False for value in validated["authority"].values())


def test_exact_reviewed_source_inventory_matches_current_branch_bytes():
    assert len(binding.SOURCE_REFERENCES) == 12
    assert len(dict(binding.SOURCE_REFERENCES)) == 12
    for relative, expected_blob in binding.SOURCE_REFERENCES:
        path = ROOT / relative
        assert path.is_file() and not path.is_symlink(), relative
        assert _git_blob(path.read_bytes()) == expected_blob, relative


@pytest.mark.parametrize(
    "override",
    [
        {"experiment_id": ""},
        {"experiment_id": "pair03"},
        {"experiment_id": "abaddon-scout-pair03-reuse"},
        {"experiment_id": "Abaddon-scout-upper"},
        {"experiment_id": "x" * 129},
        {"attempt_marker_sha256": "A" * 64},
        {"attempt_marker_sha256": "a" * 63},
        {"trajectory_sha256": "g" * 64},
        {"result_payload_sha256": True},
        {"post_run_state_sha256": ""},
    ],
)
def test_invalid_identity_inputs_fail_before_binding(override):
    with pytest.raises(HOLD):
        _build(**override)


def test_payload_mutation_or_declaration_mismatch_fails_closed():
    payload, values = _build()

    changed = json.loads(payload)
    changed["verification"]["post_run_state_verified"] = True
    mutated = (
        json.dumps(changed, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("ascii")
    with pytest.raises(HOLD, match="BYTES_DRIFT"):
        binding.validate_scout_result_binding(mutated, **values)

    with pytest.raises(HOLD, match="BYTES_DRIFT"):
        binding.validate_scout_result_binding(
            payload,
            **{**values, "trajectory_sha256": "e" * 64},
        )

    with pytest.raises(HOLD, match="EXACT_BYTES"):
        binding.validate_scout_result_binding(bytearray(payload), **values)


def test_public_payload_mutation_cannot_change_future_bindings():
    payload, values = _build()
    changed = json.loads(payload)
    changed["source_references"].clear()
    changed["authority"]["scout_execution_authorized"] = True
    changed["verification"]["result_evidence_verified"] = True

    later = json.loads(binding.build_scout_result_binding(**values))
    assert len(later["source_references"]) == 12
    assert later["authority"]["scout_execution_authorized"] is False
    assert later["verification"]["result_evidence_verified"] is False


@pytest.mark.parametrize(
    ("entrypoint", "kwargs"),
    [
        (binding.accept_result_as_verified, {}),
        (binding.accept_result_as_verified, {"verified": True}),
        (binding.authorize_or_execute, {}),
        (binding.authorize_or_execute, {"authorized": True}),
    ],
)
def test_result_acceptance_and_execution_entrypoints_always_hold(entrypoint, kwargs):
    with pytest.raises(HOLD, match=binding.NEXT_GATE):
        entrypoint(**kwargs)


def test_source_has_no_filesystem_network_runtime_or_local_imports():
    path = ROOT / "openra_env/learning/abaddon_scout_external_result_binding_v1.py"
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.add(node.module)

    assert modules == {"__future__", "hashlib", "json", "typing"}
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
