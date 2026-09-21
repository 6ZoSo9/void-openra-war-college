"""Source-only tests for the external scout launcher/result proposal."""

from __future__ import annotations

import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_external_launcher_contract_v1 as contract


ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = contract.build_scout_launcher_request()
RECORD = json.loads(PAYLOAD)
HOLD = contract.ScoutExternalLauncherContractHold


def _encode(value):
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("ascii")


def _git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def test_canonical_request_digest_and_scope_are_exact():
    assert PAYLOAD == _encode(RECORD)
    assert 0 < len(PAYLOAD) <= contract.MAX_REQUEST_BYTES == 8192
    assert hashlib.sha256(PAYLOAD).hexdigest() == contract.REQUEST_SHA256
    assert contract.REQUEST_SHA256 == (
        "67582949d9cbb6815c59ba9c78e6ac40fc303080320b5d707ad2b9e64e9baf55"
    )

    validation = contract.validate_scout_launcher_request(PAYLOAD)
    assert validation["request_bytes_valid"] is True
    assert validation["request_sha256"] == contract.REQUEST_SHA256
    assert validation["next_gate"] == contract.NEXT_GATE

    assert RECORD["record_kind"] == "proposal_only_not_authorization"
    assert RECORD["main_head"] == "9a151da589f93454d31a475b29297ea8a3d35442"
    assert RECORD["proposed_scope"] == {
        "experiment_family": "abaddon-scout-source-bound-v1",
        "maximum_attempts": 1,
        "maximum_automatic_retries": 0,
        "pair03_attempt_reuse_allowed": False,
        "pair03_attempt_reset_allowed": False,
        "held_out": False,
    }


def test_every_authority_field_remains_literal_false():
    assert len(RECORD["authority"]) == len(contract.FALSE_AUTHORITY_FIELDS)
    assert set(RECORD["authority"]) == set(contract.FALSE_AUTHORITY_FIELDS)
    assert all(value is False for value in RECORD["authority"].values())

    validation = contract.validate_scout_launcher_request(PAYLOAD)
    assert validation["authority"] == RECORD["authority"]

    requirements = contract.scout_result_requirements()
    assert requirements["result_evidence_verified"] is False
    assert requirements["post_run_state_verified"] is False
    assert requirements["automatic_retry"] is False
    assert requirements["automatic_training_admission"] is False
    assert requirements["automatic_policy_promotion"] is False


def test_required_gates_keep_fresh_attempt_and_pair03_separation_explicit():
    assert tuple(RECORD["required_gates"]) == contract.REQUIRED_GATES
    assert "fresh_experiment_identity_accepted" in contract.REQUIRED_GATES
    assert "fresh_durable_single_use_attempt_guard" in contract.REQUIRED_GATES
    assert "consumed_pair03_slot_not_reused" in contract.REQUIRED_GATES
    assert "current_operation_authority_rechecked" in contract.REQUIRED_GATES
    assert "post_run_runtime_state_independently_verified" in contract.REQUIRED_GATES

    claims = RECORD["binding_claims"]
    assert claims == {
        "matching_request_digest_grants_authority": False,
        "source_contract_grants_runtime_authority": False,
        "historical_pair03_authority_reusable": False,
        "callback_return_proves_shutdown": False,
        "historical_cleanup_prints_prove_shutdown": False,
    }


def test_source_inventory_matches_current_repository_bytes():
    assert len(contract.SOURCE_REFERENCES) == 8
    assert len(dict(contract.SOURCE_REFERENCES)) == 8

    for relative, expected_blob in contract.SOURCE_REFERENCES:
        path = ROOT / relative
        assert path.is_file() and not path.is_symlink(), relative
        assert _git_blob(path.read_bytes()) == expected_blob, relative


@pytest.mark.parametrize(
    ("relative", "expected_sha256"),
    [
        (
            "fixtures/learning/scout-missions-v1/warm_start_runner_v1_4.py",
            "ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901",
        ),
        (
            "fixtures/learning/scout-missions-v1/joint_host_v1_2.py",
            "c59faac3833ce4bffeb20e3d60625bcb3c63ecc520658660e19a8deefd2db615",
        ),
        (
            "fixtures/learning/scout-missions-v1/abaddon_controller_v1.py",
            "b235d4cff3e3953ed7c511de52c76ada7e1a47046295e104353b61ef09e11103",
        ),
    ],
)
def test_historical_fixture_sha256_bindings_match_bytes(relative, expected_sha256):
    data = (ROOT / relative).read_bytes()
    assert hashlib.sha256(data).hexdigest() == expected_sha256
    assert contract.HISTORICAL_SHA256[Path(relative).name] == expected_sha256


def test_exact_bytes_only_and_no_payload_parser_on_rejection(monkeypatch):
    class BytesSubclass(bytes):
        def __len__(self):
            raise AssertionError("subclass hooks must not run")

    with pytest.raises(HOLD, match="exact bytes"):
        contract.validate_scout_launcher_request(BytesSubclass(PAYLOAD))

    def forbidden(*args, **kwargs):
        raise AssertionError("rejected payload must not be parsed or hashed")

    monkeypatch.setattr(contract.json, "loads", forbidden)
    monkeypatch.setattr(contract.hashlib, "sha256", forbidden)
    with pytest.raises(HOLD, match="differ"):
        contract.validate_scout_launcher_request(PAYLOAD.replace(b'"maximum_attempts":1', b'"maximum_attempts":2'))


def test_request_mutations_all_fail_closed():
    mutations = []

    changed = deepcopy(RECORD)
    changed["authority"]["scout_execution_authorized"] = True
    mutations.append(changed)

    changed = deepcopy(RECORD)
    changed["proposed_scope"]["pair03_attempt_reuse_allowed"] = True
    mutations.append(changed)

    changed = deepcopy(RECORD)
    changed["proposed_scope"]["maximum_automatic_retries"] = 1
    mutations.append(changed)

    changed = deepcopy(RECORD)
    changed["source_references"][
        "openra_env/learning/abaddon_scout_runner_binding_v1.py"
    ] = "0" * 40
    mutations.append(changed)

    changed = deepcopy(RECORD)
    changed["required_gates"].remove("fresh_durable_single_use_attempt_guard")
    mutations.append(changed)

    for changed in mutations:
        with pytest.raises(HOLD):
            contract.validate_scout_launcher_request(_encode(changed))


def test_public_snapshots_are_fresh_and_cannot_mutate_future_contracts():
    first = contract.scout_launcher_contract()
    first["request"]["source_references"].clear()
    first["request"]["authority"]["scout_execution_authorized"] = True
    first["request"]["required_gates"].clear()
    first["authority"]["scout_execution_authorized"] = True

    result = contract.scout_result_requirements()
    result["source_references"].clear()
    result["pair03_attempt_reuse_allowed"] = True

    later = contract.scout_launcher_contract()
    assert later["request"] == RECORD
    assert later["authority"]["scout_execution_authorized"] is False

    later_result = contract.scout_result_requirements()
    assert len(later_result["source_references"]) == 8
    assert later_result["pair03_attempt_reuse_allowed"] is False


@pytest.mark.parametrize(
    "kwargs",
    [
        {},
        {"payload": PAYLOAD},
        {"authorized": True},
        {"confirm": "EXECUTE"},
        {"pair03_authorization": True},
    ],
)
def test_execution_entrypoint_always_holds(kwargs):
    with pytest.raises(HOLD, match=contract.NEXT_GATE):
        contract.authorize_or_execute_scout(**kwargs)


@pytest.mark.parametrize(
    "kwargs",
    [{}, {"result": {}}, {"verified": True}, {"trajectory_sha256": "a" * 64}],
)
def test_result_acceptance_entrypoint_always_holds(kwargs):
    with pytest.raises(HOLD, match=contract.NEXT_GATE):
        contract.accept_result_as_verified(**kwargs)


def test_contract_source_has_no_runtime_filesystem_network_or_local_imports():
    source_path = ROOT / "openra_env/learning/abaddon_scout_external_launcher_contract_v1.py"
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.add(node.module)

    assert modules == {"__future__", "hashlib", "json", "typing"}
    for forbidden in (
        "subprocess",
        "socket",
        "requests",
        "httpx",
        "pathlib",
        "importlib",
        "open(",
        "os.",
        "execute_pair03",
        "run_main_once(",
    ):
        assert forbidden not in source
    assert 'if __name__ ==' not in source
