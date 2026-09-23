from __future__ import annotations

from copy import deepcopy

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_same_process_python_compat_evidence_acceptance_generation2
    as acceptance,
)


def test_acceptance_records_exact_observer_and_interpreters():
    out = acceptance.pair06_v8_python_compat_evidence_acceptance_contract()
    accepted = out["accepted_evidence"]
    assert accepted["observer_sha256"] == (
        "98cd66991e9e0a61c009a5ca7d5103d52ae4fd777cad1c83319dd906561ce42f"
    )
    assert accepted["execution_main_head"] == (
        "213fcc39d1ef61455da1564032ccbb5930f0112a"
    )
    assert accepted["v8_python"].endswith("/venv/bin/python3.12")
    assert accepted["proto_python"].endswith("/venv/bin/python")
    assert accepted["resolved_python"] == "/usr/bin/python3.12"


def test_acceptance_records_environment_incompatibility_without_package_mutation():
    out = acceptance.pair06_v8_python_compat_evidence_acceptance_contract()
    accepted = out["accepted_evidence"]
    assert accepted["same_system_python_binary"] is True
    assert accepted["separate_virtualenv_site_packages"] is True
    assert accepted["v8_has_legacy_grpc_proto_dependencies"] is False
    assert accepted["same_process_legacy_game_path_compatible"] is False
    assert accepted["package_install_into_v8_authorized"] is False
    assert accepted["cross_venv_site_packages_injection_authorized"] is False
    assert accepted["parent_child_runtime_split_required"] is True


def test_exact_evidence_accepts_and_tampering_fails_closed():
    out = acceptance.accept_pair06_v8_python_compat_evidence(
        acceptance.EXPECTED_EVIDENCE
    )
    assert out["pair06_v8_same_process_python_compat_evidence_accepted"] is True

    tampered = deepcopy(acceptance.EXPECTED_EVIDENCE)
    tampered["v8_import_grpc"] = True
    with pytest.raises(
        acceptance.Pair06V8PythonCompatEvidenceAcceptanceHold,
        match="evidence drift: v8_import_grpc",
    ):
        acceptance.accept_pair06_v8_python_compat_evidence(tampered)


def test_acceptance_grants_no_execution_or_package_authority():
    accepted = acceptance.pair06_v8_python_compat_evidence_acceptance_contract()[
        "accepted_evidence"
    ]
    for field in (
        "package_install_into_v8_authorized",
        "cross_venv_site_packages_injection_authorized",
        "model_load_authorized",
        "model_inference_authorized",
        "game_execution_authorized",
        "candidate_execution_authorized",
        "pair15_execution_authorized",
        "training_authorized",
        "weights_update_authorized",
        "automatic_policy_promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert accepted[field] is False
    assert accepted["automatic_retry"] is False


def test_acceptance_advances_only_to_parent_child_split_design():
    out = acceptance.pair06_v8_python_compat_evidence_acceptance_contract()
    assert out["source_frontier_closed"] is True
    assert out["execution_blockers"] == (
        "PAIR06_V8_PARENT_CHILD_RUNTIME_SPLIT_DESIGN_REQUIRED",
    )
    assert out["next_gate"] == "PAIR06_V8_PARENT_CHILD_RUNTIME_SPLIT_DESIGN_REQUIRED"


def test_execution_entrypoint_holds():
    with pytest.raises(
        acceptance.Pair06V8PythonCompatEvidenceAcceptanceHold,
        match="PAIR06_V8_PARENT_CHILD_RUNTIME_SPLIT_DESIGN_REQUIRED",
    ):
        acceptance.execute_or_install()
