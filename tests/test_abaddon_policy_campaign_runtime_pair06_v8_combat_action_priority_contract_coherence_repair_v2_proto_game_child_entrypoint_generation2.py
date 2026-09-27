from __future__ import annotations

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_proto_game_child_entrypoint_generation2
    as entrypoint,
)


def _argv(*, confirm: str, policy_confirm: str) -> list[str]:
    return [
        "--fd", "9",
        "--attempt-id", "a" * 64,
        "--runs-root", "/runs",
        "--frozen-source-root", "/source",
        "--exact-engine-root", "/engine",
        "--confirm", confirm,
        "--policy-confirm", policy_confirm,
    ]


def test_contract_binds_v2_child_and_consumed_lineage():
    out = entrypoint.pair06_v8_combat_priority_coherent_v2_child_entrypoint_contract()
    assert out[
        "pair06_v8_combat_priority_coherent_v2_child_entrypoint_implemented"
    ] is True
    assert out["v2_proto_child_wiring_reviewed"] is True
    assert out["translator_legal_building_mapping_coherent"] is True
    assert out["translator_legal_unit_mapping_coherent"] is True
    assert out["consumed_attempt_marker_sha256"] == (
        "bbc0134e3ab9dd4a60f14e292f278316151105106d3f627e7769d4f0a7337885"
    )
    assert out["consumed_attempt_reusable"] is False
    assert out["prior_authorization_reusable"] is False


def test_wrong_execution_token_holds_before_socket_creation():
    with pytest.raises(
        entrypoint.Pair06V8CombatPriorityCoherentV2ChildEntrypointHold,
        match="execution confirmation token required",
    ):
        entrypoint.main(
            _argv(
                confirm="WRONG",
                policy_confirm=entrypoint.POLICY_CONFIRM_TOKEN,
            )
        )


def test_wrong_policy_token_holds_before_socket_creation():
    with pytest.raises(
        entrypoint.Pair06V8CombatPriorityCoherentV2ChildEntrypointHold,
        match="policy activation token required",
    ):
        entrypoint.main(
            _argv(
                confirm=entrypoint.CONFIRM_TOKEN,
                policy_confirm="WRONG",
            )
        )


def test_contract_grants_no_runtime_authority():
    out = entrypoint.pair06_v8_combat_priority_coherent_v2_child_entrypoint_contract()
    for field in (
        "attempt_retry_authorized",
        "execution_performed_by_contract_inspection",
        "runtime_activation_authorized_by_contract_inspection",
        "automatic_retry",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False
