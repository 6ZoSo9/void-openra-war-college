from __future__ import annotations

import json

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_pair09_baseline_authorization_request_generation2
    as request,
)


def test_canonical_request_validates_exactly():
    payload = request.build_pair09_baseline_authorization_request()
    out = request.validate_pair09_baseline_authorization_request(payload)
    assert out["request_bytes_valid"] is True
    assert len(out["request_sha256"]) == 64
    assert out["request_byte_length"] == len(payload)
    assert out["next_gate"] == (
        "V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"
    )


def test_request_scope_is_exact_pair09_baseline_one_shot():
    out = request.pair09_baseline_authorization_request_contract()
    record = out["request"]
    assert record["record_kind"] == "proposal_only_not_authorization"
    assert record["proposed_scope"] == {
        "pair_slot": 9,
        "arm": "baseline",
        "held_out": False,
        "maximum_baseline_attempts": 1,
        "maximum_automatic_retries": 0,
        "candidate_arm_included": False,
        "held_out_arm_included": False,
        "pair03_replay_included": False,
    }
    assert record["evaluation_order"] == {
        "baseline_first": True,
        "candidate_must_wait_for_baseline_result_review": True,
    }


def test_request_pins_exact_reviewed_source_chain():
    out = request.pair09_baseline_authorization_request_contract()
    refs = out["request"]["source_references"]
    assert refs == {
        "openra_env/learning/abaddon_policy_campaign_runtime_v2r13_pair09_baseline_execution_preparation_review_generation2.py":
            "f5242afc9947d52b26c0f89e1f1fe5906c3fa29f",
        "openra_env/learning/abaddon_policy_campaign_runtime_v2r13_pair09_evaluation_design_source_binding_review_generation2.py":
            "08a1a20a16dcceb2feb183d402edaff96f0cadfa",
        "openra_env/learning/abaddon_policy_campaign_runtime_v2r13_bounded_executor_generation2.py":
            "c7e20c1157e0bcf7f65036631aad47fb82c7aefd",
        "openra_env/learning/abaddon_policy_campaign_runtime_v2r13_first_baseline_invocation_generation2.py":
            "5b790efaf4085deb15eaef538635fd11f5cad9a5",
        "openra_env/learning/abaddon_policy_campaign_command_materializer_generation2.py":
            "4836360e0d284454f815a2a2e32078d2565e6dea",
    }


def test_request_requires_operation_time_gates():
    gates = set(
        request.pair09_baseline_authorization_request_contract()
        ["request"]["required_runtime_gates"]
    )
    assert gates == {
        "pair09_baseline_specific_operator_authorization_accepted",
        "exact_pair09_baseline_invocation_source_reviewed",
        "fresh_current_main_host_preflight",
        "cached_sudo_authority",
        "live_revocation_sentinel_absent",
        "isolated_grpc_python",
        "exact_model_preload_before_readiness_without_inference",
        "canonical_worktree_observation",
        "fresh_canonical_live_readiness_before_inference",
        "create_only_pair09_baseline_attempt_consumption",
    }


def test_request_carries_no_authority():
    out = request.pair09_baseline_authorization_request_contract()
    record = out["request"]
    assert record["historical_pair03_runtime_authority_sufficient"] is False
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
        lambda row: row["proposed_scope"].update(arm="candidate"),
        lambda row: row["proposed_scope"].update(held_out=True),
        lambda row: row["proposed_scope"].update(maximum_baseline_attempts=2),
        lambda row: row["proposed_scope"].update(maximum_automatic_retries=1),
        lambda row: row["evaluation_order"].update(baseline_first=False),
        lambda row: row.update(legacy_six_arm_authorization_sufficient=True),
        lambda row: row.update(matching_request_digest_grants_authority=True),
    ],
)
def test_modified_request_bytes_are_rejected(mutation):
    row = request.pair09_baseline_authorization_request_contract()["request"]
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
    ).encode()
    with pytest.raises(
        request.V2R13Pair09BaselineAuthorizationRequestHold,
        match="request bytes differ from fixed proposal",
    ):
        request.validate_pair09_baseline_authorization_request(payload)


def test_wrong_type_and_byte_limit_are_rejected():
    with pytest.raises(
        request.V2R13Pair09BaselineAuthorizationRequestHold,
        match="exact bytes",
    ):
        request.validate_pair09_baseline_authorization_request("not-bytes")

    with pytest.raises(
        request.V2R13Pair09BaselineAuthorizationRequestHold,
        match="byte limit",
    ):
        request.validate_pair09_baseline_authorization_request(b"")


def test_authorize_or_execute_entrypoint_holds():
    with pytest.raises(
        request.V2R13Pair09BaselineAuthorizationRequestHold,
        match="V2R13_PAIR09_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        request.authorize_or_execute_pair09_baseline()
