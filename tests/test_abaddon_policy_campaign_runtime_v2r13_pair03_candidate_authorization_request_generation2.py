"""A well-formed candidate proposal must never turn into execution authority."""

from __future__ import annotations

import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair03_candidate_authorization_request_generation2
    as request,
)

REPO = Path(__file__).resolve().parents[1]
PAYLOAD = request.build_candidate_authorization_request()
RECORD = json.loads(PAYLOAD)
HOLD = request.V2R13Pair03CandidateAuthorizationRequestHold


def _encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _leaves(value, path=()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _leaves(child, (*path, key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _leaves(child, (*path, index))
    else:
        yield path, value


def _parent(value, path):
    for part in path[:-1]:
        value = value[part]
    return value, path[-1]


def test_canonical_request_and_pinned_digest_vector():
    assert 0 < len(PAYLOAD) <= request.MAX_REQUEST_BYTES == 16384
    assert PAYLOAD == _encode(RECORD)
    assert PAYLOAD.endswith(b"\n") and not PAYLOAD.endswith(b"\n\n")
    result = request.validate_candidate_authorization_request(PAYLOAD)
    assert result["request_bytes_valid"] is True
    assert result["request_sha256"] == hashlib.sha256(PAYLOAD).hexdigest()
    assert result["request_sha256"] == "5025174efdf945f206119c1f25cb3a5d07bcb87ed3de8ccd93e3d9b1e3354a87"
    assert result["request_byte_length"] == len(PAYLOAD)
    assert result["next_gate"] == "V2R13_PAIR03_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"


def test_scope_is_one_proposed_candidate_attempt_not_baseline_or_held_out():
    assert RECORD["record_kind"] == "proposal_only_not_authorization"
    assert RECORD["proposed_scope"] == {
        "pair_slot": 3,
        "arm": "candidate",
        "held_out": False,
        "maximum_candidate_attempts": 1,
        "maximum_automatic_retries": 0,
        "other_pair_slots_included": False,
        "baseline_rerun_included": False,
    }
    assert RECORD["baseline_reference"]["recorded_rounds_completed"] == 36
    assert RECORD["baseline_reference"]["recorded_outcome"] == "DRAW_OR_UNFINISHED"
    assert RECORD["baseline_reference"]["recorded_outcome_decisive"] is False


def test_all_authority_and_verification_claims_remain_false():
    result = request.validate_candidate_authorization_request(PAYLOAD)
    for value in (RECORD, result):
        assert len(value["authority"]) == 20
        assert all(flag is False for flag in value["authority"].values())
    assert RECORD["legacy_six_arm_authorization_sufficient"] is False
    assert RECORD["matching_request_digest_grants_authority"] is False
    assert RECORD["runtime_gates_enforced_by_this_module"] is False
    assert len(RECORD["required_runtime_gates"]) == 11
    assert "create_only_single_use_attempt_consumption" in RECORD["required_runtime_gates"]


@pytest.mark.parametrize("path,value", list(_leaves(RECORD)))
def test_every_scalar_change_rejects_even_with_new_valid_encoding_and_digest(path, value):
    changed = deepcopy(RECORD)
    parent, key = _parent(changed, path)
    if type(value) is bool:
        parent[key] = not value
    elif type(value) is int:
        parent[key] = value + 1
    else:
        parent[key] = value + "-changed"
    encoded = _encode(changed)
    assert hashlib.sha256(encoded).hexdigest() != hashlib.sha256(PAYLOAD).hexdigest()
    with pytest.raises(HOLD, match="fixed proposal"):
        request.validate_candidate_authorization_request(encoded)


@pytest.mark.parametrize("path,value", list(_leaves(RECORD)))
def test_missing_nested_member_rejects(path, value):
    changed = deepcopy(RECORD)
    parent, key = _parent(changed, path)
    del parent[key]
    with pytest.raises(HOLD):
        request.validate_candidate_authorization_request(_encode(changed))


@pytest.mark.parametrize("section", [None, "authority", "proposed_scope", "candidate_reference"])
def test_unknown_members_reject(section):
    changed = deepcopy(RECORD)
    target = changed if section is None else changed[section]
    target["operator_approved"] = True
    with pytest.raises(HOLD):
        request.validate_candidate_authorization_request(_encode(changed))


@pytest.mark.parametrize("value", [True, 3.0, "3", None])
def test_integer_aliases_do_not_pass_scope_validation(value):
    changed = deepcopy(RECORD)
    changed["proposed_scope"]["pair_slot"] = value
    with pytest.raises(HOLD):
        request.validate_candidate_authorization_request(_encode(changed))


@pytest.mark.parametrize("payload", [
    b"", b"x" * 16385, b"[]", b"null", b"NaN", b"\xff", b"\xef\xbb\xbf" + PAYLOAD,
    PAYLOAD[:-1], PAYLOAD + b"\n", PAYLOAD + b"garbage", b" " + PAYLOAD,
    PAYLOAD.replace(b'"pair_slot":3', b'"pair_slot":3,"pair_slot":3'),
    PAYLOAD.replace(b'"arm":"candidate"', b'"arm":"candid\\u0061te"'),
    PAYLOAD.replace(b"false", b"0", 1),
    b"[" * 4000 + b"]" * 4000,
    json.dumps(RECORD, indent=2).encode(),
    json.dumps(dict(reversed(list(RECORD.items()))), separators=(",", ":")).encode() + b"\n",
])
def test_malformed_alternate_or_oversized_bytes_reject_without_parsing(payload):
    with pytest.raises(HOLD):
        request.validate_candidate_authorization_request(payload)


@pytest.mark.parametrize("payload", [None, {}, [], 1, True, "text", bytearray(PAYLOAD), memoryview(PAYLOAD)])
def test_nonbytes_inputs_reject(payload):
    with pytest.raises(HOLD, match="exact bytes"):
        request.validate_candidate_authorization_request(payload)


def test_nonbytes_hooks_are_not_invoked():
    class Hooks:
        def __bytes__(self):
            raise AssertionError("bytes coercion")

        def __len__(self):
            raise AssertionError("length coercion")

        def __eq__(self, other):
            raise AssertionError("equality coercion")

        def __repr__(self):
            raise AssertionError("error formatting")

    class BytesSubclass(bytes):
        def __len__(self):
            raise AssertionError("subclass length")

        def __eq__(self, other):
            raise AssertionError("subclass equality")

    for payload in (Hooks(), BytesSubclass(PAYLOAD)):
        with pytest.raises(HOLD, match="exact bytes"):
            request.validate_candidate_authorization_request(payload)


def test_no_caller_json_parser_or_rejected_payload_hasher_runs(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("unexpected parser or hasher call")

    monkeypatch.setattr(request.json, "loads", forbidden)
    assert request.validate_candidate_authorization_request(PAYLOAD)["request_bytes_valid"] is True
    monkeypatch.setattr(request.hashlib, "sha256", forbidden)
    with pytest.raises(HOLD):
        request.validate_candidate_authorization_request(PAYLOAD.replace(b'"pair_slot":3', b'"pair_slot":9'))


def test_public_snapshots_are_independent_and_repetition_never_consumes_authority():
    first = request.candidate_authorization_request_contract()
    first["authority"]["candidate_execution_authorized"] = True
    first["request"]["authority"]["candidate_execution_authorized"] = True
    first["request"]["required_runtime_gates"].clear()
    first["request"]["source_references"].clear()
    first["request"]["proposed_scope"]["maximum_candidate_attempts"] = 999
    for _ in range(3):
        later = request.candidate_authorization_request_contract()
        assert later["request"] == RECORD
        assert later["authority"]["candidate_execution_authorized"] is False
        assert later["authority"]["authorization_consumed"] is False
        assert request.build_candidate_authorization_request() == PAYLOAD


@pytest.mark.parametrize("kwargs", [
    {}, {"payload": PAYLOAD}, {"authorized": True},
    {"authorization": {"authorized_pair_slots": [3, 9, 15], "authorized_arms": ["baseline", "candidate"]}},
    {"confirmation": "VOID_ABADDON_GENERATION2_V2R13_EXECUTE_PAIR03_BASELINE"},
])
def test_execution_entrypoint_always_holds(kwargs):
    with pytest.raises(HOLD, match=request.NEXT_GATE):
        request.authorize_or_execute_candidate(**kwargs)


def test_source_has_only_standard_library_data_imports():
    tree = ast.parse(Path(request.__file__).read_text(encoding="utf-8"))
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.add(node.module)
    assert modules == {"__future__", "hashlib", "json", "typing"}


def test_repository_source_references_match_actual_bytes():
    # CI runs this on the complete checkout, without importing runtime modules.
    assert len(request.SOURCE_REFERENCES) == 8
    assert len(dict(request.SOURCE_REFERENCES)) == 8
    for relative, expected_blob in request.SOURCE_REFERENCES:
        path = REPO / relative
        assert path.is_file() and not path.is_symlink(), relative
        data = path.read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert actual == expected_blob, relative
