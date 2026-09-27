from __future__ import annotations

import ast
from pathlib import Path

import pytest

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v8_combat_action_priority_contract_coherence_repair_v2_execution_success_artifact_evidence_audit_generation2
    as audit,
)


EXPECTED = {
    "attempt_marker": (
        "a64faf60c8f548efb5d869374f437de20f7165b1b53ea978332225f68efc7207"
    ),
    "result": (
        "b205421d468d2c02eb73649dc6cffa10084f58cc55c64950ab3d23d5ea21cee4"
    ),
    "closeout": (
        "181bdd2fd818a5e6376f4a58d0bcfae3ae986f96f9298acee0c9e92f818c43d1"
    ),
    "trajectory": (
        "afc57351991c90dc21e4d2316ddd23fce8b01b9132a3435a9252de7227001ddc"
    ),
    "summary": (
        "a5d72287487849164e727836eee82dd5821ddb46f5803b995b1d67cc289075ab"
    ),
    "warm_start": (
        "f36f2717d34e028d02d1b7076d7de1cff65dce1ffed59710110f2adbf4ad700d"
    ),
}


def test_execution_closure_is_preserved_but_artifact_evidence_frontier_is_open():
    out = audit.pair06_v8_coherent_v2_artifact_evidence_audit_contract()

    assert out["execution_lineage_closed"] is True
    assert out["attempt_consumed"] is True
    assert out["attempt_reusable"] is False
    assert out["authorization_reusable"] is False
    assert out["automatic_retry"] is False
    assert out["new_execution_request_opened"] is False

    assert out["prior_source_frontier_closed_claim"] is True
    assert out["repo_side_local_artifact_rehash_performed"] is False
    assert out["artifact_bytes_verified_by_this_audit"] is False
    assert out["public_safe_artifact_manifest_bound"] is False
    assert out["artifact_byte_drift_regression_bound"] is False
    assert out["source_artifact_evidence_frontier_closed"] is False
    assert out["source_frontier_closed"] is False


def test_all_six_runtime_artifact_digests_are_carried_only_as_expected_identities():
    out = audit.pair06_v8_coherent_v2_artifact_evidence_audit_contract()
    assert out["expected_artifact_sha256"] == EXPECTED
    assert set(out["expected_artifact_sha256"]) == {
        "attempt_marker",
        "result",
        "closeout",
        "trajectory",
        "summary",
        "warm_start",
    }


def test_post_close_audit_grants_no_follow_on_authority():
    out = audit.pair06_v8_coherent_v2_artifact_evidence_audit_contract()
    for field in (
        "retry_authorized",
        "replay_authorized",
        "training_authorized",
        "promotion_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        assert out[field] is False


def test_manifest_binding_stays_fail_closed_until_real_byte_evidence_exists():
    out = audit.pair06_v8_coherent_v2_artifact_evidence_audit_contract()
    assert out["next_gate"] == "PAIR06_V8_COHERENT_V2_ARTIFACT_MANIFEST_REQUIRED"
    assert out["next_change_class"] == (
        "source_only_public_safe_artifact_manifest_binding"
    )

    with pytest.raises(
        audit.Pair06V8CoherentV2ArtifactEvidenceAuditHold,
        match="ARTIFACT_MANIFEST_REQUIRED",
    ):
        audit.bind_artifact_manifest({})


def test_execution_lineage_cannot_be_reopened_by_audit_layer():
    with pytest.raises(
        audit.Pair06V8CoherentV2ArtifactEvidenceAuditHold,
        match="EXECUTION_LINEAGE_CLOSED",
    ):
        audit.execute_or_reopen()


def test_audit_source_has_no_host_io_process_network_or_execution_backend():
    path = (
        Path(__file__).parents[1]
        / "openra_env/learning/"
        "abaddon_policy_campaign_runtime_pair06_v8_"
        "combat_action_priority_contract_coherence_repair_v2_"
        "execution_success_artifact_evidence_audit_generation2.py"
    )
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports = {
        node.names[0].name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
    }
    imports.update(
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    )
    assert not imports.intersection(
        {"os", "pathlib", "subprocess", "socket", "urllib", "requests"}
    )
    assert 'if __name__ ==' not in source
    for forbidden in (
        "open(",
        "Popen(",
        "subprocess.",
        "systemctl",
        "docker ",
        "start_ollama",
        "execute_pair06",
        "consume_attempt",
        "unlink(",
        "write_text(",
        "write_bytes(",
    ):
        assert forbidden not in source
