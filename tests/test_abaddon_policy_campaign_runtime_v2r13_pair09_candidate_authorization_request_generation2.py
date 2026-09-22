from __future__ import annotations

import json

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_candidate_authorization_request_generation2
    as request,
)


def test_canonical_request_validates_exactly():
    payload = request.build_pair09_candidate_authorization_request()
    out = request.validate_pair09_candidate_authorization_request(payload)
    assert out["request_bytes_valid"] is True
    assert len(out["request_sha256"]) == 64
    assert out["request_byte_length"] == len(payload)
    assert out["next_gate"] == (
        "V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def test_request_scope_is_exact_pair09_candidate_one_shot():
    record = request.pair09_candidate_authorization_request_contract()["request"]
    assert record["record_kind"] == "proposal_only_not_authorization"
    assert record["proposed_scope"] == {
        "pair_slot": 9,
        "arm": "candidate",
        "held_out": False,
        "maximum_candidate_attempts": 1,
        "maximum_automatic_retries": 0,
        "baseline_rerun_included": False,
        "held_out_arm_included": False,
        "other_pair_slots_included": False,
    }


def test_request_binds_exact_preparation_and_baseline():
    record = request.pair09_candidate_authorization_request_contract()["request"]
    assert record["preparation_source_sha256"] == (
        "6f4cea4ff326a4579a98456a6272c7bef6c44b3915446e2b5f20fce9b9d9a8ca"
    )
    assert record["preparation_test_git_blob"] == (
        "df189ee056584e6f4dee2efef59248eb6619ce1d"
    )
    assert record["preparation_test_sha256"] == (
        "5836efff0033563d4b68003373fb5faa9741649bb595eba2bae447c969edd576"
    )
    assert record["baseline_reference"] == {
        "seed": 1496195137,
        "round_limit": 36,
        "recorded_rounds_completed": 36,
        "recorded_outcome": "DRAW_OR_UNFINISHED",
        "recorded_outcome_decisive": False,
        "trajectory_sha256": (
            "103f4325d9ed91edf0e72982045e4f72e12bf40641e43915beeabb4c9e569700"
        ),
        "summary_sha256": (
            "48e8ce8d0c1a00163b88a5c4b3c23e7b057bcfb5d2b59977c67387c838a8f189"
        ),
        "result_file_sha256": (
            "86b8cf0ce07ff6135d43911b36870e481e028f10a288c26f29f858655dde0ec2"
        ),
        "attempt_marker_sha256": (
            "57f862fe39a8939f3d47d4184fe264e0b9cd3988143f4cdc3adb9973a0e2e41c"
        ),
    }


def test_request_binds_exact_candidate_policy_and_runtime():
    record = request.pair09_candidate_authorization_request_contract()["request"]
    assert record["candidate_reference"] == {
        "wrapper_sha256": (
            "686f88836e73acf9c78bfc1417db735b11100c07c34ce8da291047edd99eea9f"
        ),
        "fixture_sha256": (
            "3fabbe9bc9b44830ee8e13e748d84ada881c6a3604f40c27609a953cabfd7768"
        ),
        "semantic_genome_sha256": (
            "8253ea5f1b3a709c8d64fb0432d13ac1c52ee82678e2f3b0ec730fe23d603089"
        ),
        "controller_sha256": (
            "b235d4cff3e3953ed7c511de52c76ada7e1a47046295e104353b61ef09e11103"
        ),
        "refiner_sha256": (
            "5c5c4e7260cebcc5afbe9e9bd4744846593b44658ed0088f2eddbcaffc43910b"
        ),
    }
    assert record["runtime_reference"]["selection_key"] == (
        "apollyon-v2r13-qualified-predecessor"
    )
    assert record["runtime_reference"]["model_digest"] == (
        "b52834ea46c10362e9bb20cd2e721716016bb36f800ddbc62e7fbaa24fb40932"
    )


def test_request_requires_all_runtime_gates():
    record = request.pair09_candidate_authorization_request_contract()["request"]
    assert tuple(record["required_runtime_gates"]) == request.REQUIRED_RUNTIME_GATES


def test_request_carries_no_authority():
    out = request.pair09_candidate_authorization_request_contract()
    record = out["request"]
    assert record["legacy_six_arm_authorization_sufficient"] is False
    assert record["matching_request_digest_grants_authority"] is False
    assert record["runtime_gates_enforced_by_this_module"] is False
    assert record["authority"]
    assert all(value is False for value in record["authority"].values())
    assert out["authority"]
    assert all(value is False for value in out["authority"].values())


@pytest.mark.parametrize(
    "mutation",
    [
        lambda row: row["proposed_scope"].update(pair_slot=3),
        lambda row: row["proposed_scope"].update(arm="baseline"),
        lambda row: row["proposed_scope"].update(held_out=True),
        lambda row: row["proposed_scope"].update(maximum_candidate_attempts=2),
        lambda row: row["proposed_scope"].update(maximum_automatic_retries=1),
        lambda row: row["proposed_scope"].update(baseline_rerun_included=True),
        lambda row: row["baseline_reference"].update(seed=1),
        lambda row: row["candidate_reference"].update(
            semantic_genome_sha256="0" * 64
        ),
        lambda row: row.update(legacy_six_arm_authorization_sufficient=True),
        lambda row: row.update(matching_request_digest_grants_authority=True),
    ],
)
def test_modified_request_bytes_are_rejected(mutation):
    row = request.pair09_candidate_authorization_request_contract()["request"]
    mutation(row)
    payload = (
        json.dumps(
            row,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")
    with pytest.raises(
        request.V2R13Pair09CandidateAuthorizationRequestHold,
        match="request bytes differ from fixed proposal",
    ):
        request.validate_pair09_candidate_authorization_request(payload)


def test_wrong_type_and_empty_payload_are_rejected():
    with pytest.raises(
        request.V2R13Pair09CandidateAuthorizationRequestHold,
        match="exact bytes",
    ):
        request.validate_pair09_candidate_authorization_request("not-bytes")
    with pytest.raises(
        request.V2R13Pair09CandidateAuthorizationRequestHold,
        match="byte limit",
    ):
        request.validate_pair09_candidate_authorization_request(b"")


def test_execution_entrypoint_holds():
    with pytest.raises(
        request.V2R13Pair09CandidateAuthorizationRequestHold,
        match="V2R13_PAIR09_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        request.authorize_or_execute_candidate()
