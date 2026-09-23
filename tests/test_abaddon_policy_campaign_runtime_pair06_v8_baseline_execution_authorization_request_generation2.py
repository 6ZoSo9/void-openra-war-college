from __future__ import annotations

from copy import deepcopy
import json

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_baseline_execution_authorization_request_generation2
    as request,
)


def test_request_binds_exact_pair06_baseline_scope():
    out = request.pair06_v8_baseline_execution_authorization_request_contract()
    scope = out["request"]["proposed_scope"]
    assert scope["pair_slot"] == 6
    assert scope["arm"] == "baseline"
    assert scope["held_out"] is False
    assert scope["doctrine"] == "FEINTER"
    assert scope["seed"] == 208354846
    assert scope["rounds"] == 36
    assert scope["ticks_per_round"] == 25
    assert scope["starter_infantry"] == 4
    assert scope["staging_max_ticks"] == 800
    assert scope["runtime_selection_key"] == "apollyon-v3-v8-accepted-model-control"
    assert scope["maximum_attempts"] == 1
    assert scope["maximum_automatic_retries"] == 0
    assert scope["candidate_arm_included"] is False
    assert scope["held_out_pair15_included"] is False


def test_request_binds_parent_child_architecture_and_evidence_order():
    out = request.pair06_v8_baseline_execution_authorization_request_contract()
    architecture = out["request"]["runtime_architecture"]
    assert architecture["v8_parent_process"] is True
    assert architecture["proto_grpc_game_child_process"] is True
    assert architecture["separate_virtualenv_site_packages_preserved"] is True
    assert architecture["inherited_unix_socketpair_only"] is True
    assert architecture["private_child_process_group"] is True
    assert architecture["legacy_ollama_started"] is False
    assert architecture["legacy_ollama_contacted"] is False

    order = out["request"]["evidence_order"]
    assert order["preclaim_preparation_first"] is True
    assert order["durable_attempt_marker_before_model_load_or_child_spawn"] is True
    assert order["durable_execution_result_before_worktree_cleanup"] is True
    assert order["durable_cleanup_closeout_after_successful_cleanup"] is True
    assert order["runs_preserved"] is True


def test_request_is_proposal_only_and_grants_no_authority():
    out = request.pair06_v8_baseline_execution_authorization_request_contract()
    assert out["matching_request_digest_grants_authority"] is False
    assert out["pair06_baseline_specific_authorization_accepted"] is False
    assert out["pair06_baseline_execution_authorized"] is False
    assert out["pair06_baseline_execution_performed"] is False
    assert all(value is False for value in out["authority"].values())
    assert out["next_gate"] == "PAIR06_V8_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED"


def test_request_bytes_are_fixed_and_tampering_fails():
    payload = request.build_pair06_v8_baseline_execution_authorization_request()
    result = request.validate_pair06_v8_baseline_execution_authorization_request(
        payload
    )
    assert result["request_bytes_valid"] is True
    assert len(result["request_sha256"]) == 64

    body = json.loads(payload)
    body["proposed_scope"]["pair_slot"] = 15
    tampered = (
        json.dumps(body, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode()
    with pytest.raises(
        request.Pair06V8BaselineExecutionAuthorizationRequestHold,
        match="request bytes differ",
    ):
        request.validate_pair06_v8_baseline_execution_authorization_request(
            tampered
        )


def test_execution_entrypoint_holds_for_explicit_authorization():
    with pytest.raises(
        request.Pair06V8BaselineExecutionAuthorizationRequestHold,
        match="PAIR06_V8_BASELINE_EXECUTION_AUTHORIZATION_REQUIRED",
    ):
        request.authorize_or_execute()
