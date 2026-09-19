from __future__ import annotations

import ast
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_execution_authorization_acceptance_generation2
    as authorization,
)

REPO = Path(__file__).resolve().parents[1]
SOURCE = (
    REPO
    / "openra_env/learning/"
    "abaddon_policy_campaign_runtime_v2r13_execution_authorization_acceptance_generation2.py"
)


@lru_cache(maxsize=1)
def _contract_cached():
    return authorization.v2r13_runtime_execution_authorization_contract()


def _contract():
    return deepcopy(_contract_cached())


def _expect_hold(message: str, fn) -> None:
    try:
        fn()
    except authorization.V2R13RuntimeExecutionAuthorizationHold as exc:
        assert message in str(exc)
    else:
        raise AssertionError("expected authorization hold")


def test_authorization_scope_is_exactly_v2r13_only():
    out = _contract()
    assert out["authorization_scope"] == "v2r13_lane_only"
    assert out["authorized_runtime_selection_key"] == (
        "apollyon-v2r13-qualified-predecessor"
    )
    assert out["other_runtime_lanes_authorized"] is False


def test_authorized_pair_slots_and_arms_are_exact():
    out = _contract()
    assert out["authorized_pair_slots"] == (3, 9, 15)
    assert out["authorized_arms"] == ("baseline", "candidate")
    assert out["authorized_execution_arm_count"] == 6


def test_authorized_allocations_are_exactly_six_v2r13_arms():
    out = _contract()
    rows = out["authorized_allocations"]
    assert len(rows) == 6
    assert {(row["pair_slot"], row["arm"]) for row in rows} == {
        (3, "baseline"),
        (3, "candidate"),
        (9, "baseline"),
        (9, "candidate"),
        (15, "baseline"),
        (15, "candidate"),
    }
    assert {
        row["runtime_selection_key"]
        for row in rows
    } == {"apollyon-v2r13-qualified-predecessor"}


def test_authorized_allocations_advance_only_the_authorization_blocker():
    out = _contract()
    for row in out["authorized_allocations"]:
        assert row["runtime_execution_authorized"] is True
        assert row["remaining_source_blockers"] == ()
        assert row["remaining_blockers"] == (
            "V2R13_RUNTIME_EXECUTION_IMPLEMENTATION_REQUIRED",
        )
        assert row["runtime_started"] is False
        assert row["command_execution_performed"] is False


def test_authorization_remains_nonexecuting():
    out = _contract()
    for field in (
        "runtime_execution_implemented",
        "runtime_execution_performed",
        "runtime_started",
        "model_inference_performed",
        "game_execution_performed",
    ):
        assert out[field] is False


def test_training_promotion_deployment_void_and_funds_remain_unauthorized():
    out = _contract()
    for field in (
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_fresh_readiness_and_revocation_checks_remain_required():
    out = _contract()
    assert out["fresh_runtime_readiness_required_before_each_execution"] is True
    assert out["revocation_check_required_before_each_execution"] is True


def test_authorization_is_repository_attestation_not_crypto_proof():
    out = _contract()
    assert out["authorization_repository_attestation"] is True
    assert out["authorization_cryptographic_proof"] is False
    assert (
        authorization.AUTHORIZATION_ATTESTATION[
            "cryptographic_operator_signature_present"
        ]
        is False
    )


def test_embedded_authorization_accepts_exactly():
    out = authorization.accept_v2r13_runtime_execution_authorization(
        authorization.AUTHORIZATION_ATTESTATION
    )
    assert out["authorization_accepted"] is True
    assert out["runtime_execution_authorized"] is True
    assert out["authorized_execution_arm_count"] == 6


def test_tampered_scope_is_rejected():
    value = deepcopy(authorization.AUTHORIZATION_ATTESTATION)
    value["authorization_scope"] = "all_runtime_lanes"
    _expect_hold(
        "authorization drift: authorization_scope",
        lambda: authorization.accept_v2r13_runtime_execution_authorization(value),
    )


def test_tampered_pair_slots_are_rejected():
    value = deepcopy(authorization.AUTHORIZATION_ATTESTATION)
    value["authorized_pair_slots"] = (3, 6, 9, 12, 15, 18)
    _expect_hold(
        "authorization drift: authorized_pair_slots",
        lambda: authorization.accept_v2r13_runtime_execution_authorization(value),
    )


def test_tampered_execution_count_is_rejected():
    value = deepcopy(authorization.AUTHORIZATION_ATTESTATION)
    value["authorized_execution_arm_count"] = 36
    _expect_hold(
        "authorization drift: authorized_execution_arm_count",
        lambda: authorization.accept_v2r13_runtime_execution_authorization(value),
    )


def test_training_authority_cannot_be_smuggled_in():
    value = deepcopy(authorization.AUTHORIZATION_ATTESTATION)
    value["training_authorized"] = True
    _expect_hold(
        "authorization drift: training_authorized",
        lambda: authorization.accept_v2r13_runtime_execution_authorization(value),
    )


def test_field_set_expansion_is_rejected():
    value = deepcopy(authorization.AUTHORIZATION_ATTESTATION)
    value["v14_authorized"] = True
    _expect_hold(
        "authorization field-set drift",
        lambda: authorization.accept_v2r13_runtime_execution_authorization(value),
    )


def test_memoized_contract_is_copy_isolated():
    out = _contract()
    out["authorized_allocations"].clear()
    assert len(_contract()["authorized_allocations"]) == 6
    assert _contract()["authorization_scope"] == "v2r13_lane_only"


def test_source_has_no_direct_execution_or_host_io_imports():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"), filename=str(SOURCE))
    forbidden = {
        "asyncio",
        "ctypes",
        "http",
        "httpx",
        "multiprocessing",
        "os",
        "pathlib",
        "requests",
        "shutil",
        "socket",
        "subprocess",
        "urllib",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".", 1)[0] not in forbidden
        elif isinstance(node, ast.ImportFrom):
            assert (node.module or "").split(".", 1)[0] not in forbidden


def test_next_gate_is_bounded_v2r13_execution_implementation():
    out = _contract()
    assert out["next_gate"] == "V2R13_RUNTIME_EXECUTION_IMPLEMENTATION_REQUIRED"
    assert out["next_change_class"] == (
        "v2r13_bounded_runtime_execution_implementation"
    )


def test_execution_entrypoint_still_holds_until_implementation_exists():
    _expect_hold(
        "V2R13_RUNTIME_EXECUTION_IMPLEMENTATION_REQUIRED",
        lambda: authorization.execute_authorized_v2r13_runtime(),
    )


def test_other_runtime_lane_entrypoint_holds():
    _expect_hold(
        "AUTHORIZATION_SCOPE_V2R13_ONLY",
        lambda: authorization.authorize_other_runtime_lane(),
    )
