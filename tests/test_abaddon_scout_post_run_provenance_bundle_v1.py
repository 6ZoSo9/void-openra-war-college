import hashlib
import json

import pytest

from openra_env.learning import abaddon_scout_post_run_backend_v1 as backend
from openra_env.learning import abaddon_scout_post_run_observer_v1 as observer
from openra_env.learning import abaddon_scout_post_run_provenance_bundle_v1 as bundle


def _inputs(
    *,
    accepted_war_college_commit: str = "a" * 40,
) -> backend.ScoutPostRunBackendInputs:
    return backend.ScoutPostRunBackendInputs(
        experiment_id="abaddon-scout-provenance-v1",
        attempt_marker_path=f"/tmp/scout/{backend.attempt_guard.MARKER_NAME}",
        attempt_marker_sha256="1" * 64,
        attempt_directory_identity=(123, 456),
        engine_container_name="void-scout-repair-canary-4242",
        accepted_war_college_commit=accepted_war_college_commit,
    )


def _state_evidence(
    inputs: backend.ScoutPostRunBackendInputs,
    *,
    experiment_id: str | None = None,
    attempt_marker_sha256: str | None = None,
    source_checkout_clean: bool = True,
) -> bytes:
    record = {
        "schema": observer.EVIDENCE_SCHEMA,
        "record_kind": "independent_post_run_state_declaration",
        "experiment_id": experiment_id or inputs.experiment_id,
        "attempt_marker_sha256": (
            attempt_marker_sha256 or inputs.attempt_marker_sha256
        ),
        "observer_contract_git_blob": observer.OBSERVER_CONTRACT_GIT_BLOB,
        "observations": {
            name: (
                source_checkout_clean
                if name == "source_checkout_clean"
                else True
            )
            for name in observer.REQUIRED_OBSERVATIONS
        },
        "claims": {
            field: False
            for field in observer.FALSE_CLAIMS
        },
    }
    return (
        json.dumps(
            record,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")


def _binding_record(
    inputs: backend.ScoutPostRunBackendInputs,
) -> dict:
    raw = bundle.build_scout_post_run_provenance_binding(
        inputs=inputs,
        state_evidence=_state_evidence(inputs),
    )
    return json.loads(raw)


def test_binding_serializes_exact_source_and_runtime_context():
    inputs = _inputs()
    state = _state_evidence(inputs)
    raw = bundle.build_scout_post_run_provenance_binding(
        inputs=inputs,
        state_evidence=state,
    )
    record = json.loads(raw)

    assert record["schema"] == bundle.BINDING_SCHEMA
    assert record["record_kind"] == bundle.RECORD_KIND
    assert record["experiment_id"] == inputs.experiment_id
    assert record["attempt_marker_sha256"] == inputs.attempt_marker_sha256
    assert (
        record["accepted_war_college_commit"]
        == inputs.accepted_war_college_commit
    )
    assert (
        record["expected_engine_commit"]
        == backend.EXPECTED_ENGINE_COMMIT
    )
    assert record["engine_container_name"] == inputs.engine_container_name
    assert record["post_run_state_sha256"] == hashlib.sha256(state).hexdigest()
    assert (
        record["observer_contract_git_blob"]
        == observer.OBSERVER_CONTRACT_GIT_BLOB
    )
    assert record["source_references"] == {
        bundle.BACKEND_PATH: bundle.BACKEND_GIT_BLOB,
        bundle.BACKEND_REVIEW_PATH: bundle.BACKEND_REVIEW_GIT_BLOB,
        bundle.OBSERVER_PATH: bundle.OBSERVER_GIT_BLOB,
        bundle.OBSERVER_CONTRACT_PATH: bundle.OBSERVER_CONTRACT_GIT_BLOB,
    }
    assert all(value is False for value in record["authority"].values())
    assert raw.endswith(b"\n")


def test_binding_commits_local_marker_context_without_publishing_raw_values():
    inputs = _inputs()
    record = _binding_record(inputs)

    assert "attempt_marker_path" not in record
    assert "attempt_directory_identity" not in record
    assert inputs.attempt_marker_path not in json.dumps(record)
    assert record["attempt_marker_path_sha256"] == hashlib.sha256(
        inputs.attempt_marker_path.encode("utf-8")
    ).hexdigest()

    expected_directory_digest = hashlib.sha256(
        json.dumps(
            {"st_dev": 123, "st_ino": 456},
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("ascii")
    ).hexdigest()
    assert (
        record["attempt_directory_identity_sha256"]
        == expected_directory_digest
    )


def test_state_evidence_must_be_canonical_and_match_bound_inputs():
    inputs = _inputs()
    valid = _state_evidence(inputs)

    with pytest.raises(
        bundle.ScoutPostRunProvenanceBundleHold,
        match="STATE_NONCANONICAL",
    ):
        bundle.build_scout_post_run_provenance_binding(
            inputs=inputs,
            state_evidence=valid[:-1] + b" \n",
        )

    with pytest.raises(
        bundle.ScoutPostRunProvenanceBundleHold,
        match="STATE_EXPERIMENT_DRIFT",
    ):
        bundle.build_scout_post_run_provenance_binding(
            inputs=inputs,
            state_evidence=_state_evidence(
                inputs,
                experiment_id="abaddon-scout-other-v1",
            ),
        )

    with pytest.raises(
        bundle.ScoutPostRunProvenanceBundleHold,
        match="STATE_ATTEMPT_DRIFT",
    ):
        bundle.build_scout_post_run_provenance_binding(
            inputs=inputs,
            state_evidence=_state_evidence(
                inputs,
                attempt_marker_sha256="2" * 64,
            ),
        )

    with pytest.raises(
        bundle.ScoutPostRunProvenanceBundleHold,
        match="OBSERVATION_REQUIRED:source_checkout_clean",
    ):
        bundle.build_scout_post_run_provenance_binding(
            inputs=inputs,
            state_evidence=_state_evidence(
                inputs,
                source_checkout_clean=False,
            ),
        )


def test_different_admitted_war_college_commit_changes_binding_bytes():
    inputs_a = _inputs(accepted_war_college_commit="a" * 40)
    inputs_b = _inputs(accepted_war_college_commit="b" * 40)
    state_a = _state_evidence(inputs_a)
    state_b = _state_evidence(inputs_b)

    binding_a = bundle.build_scout_post_run_provenance_binding(
        inputs=inputs_a,
        state_evidence=state_a,
    )
    binding_b = bundle.build_scout_post_run_provenance_binding(
        inputs=inputs_b,
        state_evidence=state_b,
    )

    assert binding_a != binding_b
    assert json.loads(binding_a)["accepted_war_college_commit"] == "a" * 40
    assert json.loads(binding_b)["accepted_war_college_commit"] == "b" * 40


def test_collect_composes_backend_evidence_and_binding_from_same_inputs(monkeypatch):
    inputs = _inputs()
    expected_state = _state_evidence(inputs)
    calls = []

    def fake_collect(
        observed_inputs,
        *,
        observation_authorized,
        read_authority_check,
        run_command,
        file_backend,
        lstat_path,
        resolve_path,
    ):
        calls.append(
            {
                "inputs": observed_inputs,
                "observation_authorized": observation_authorized,
                "read_authority_check": read_authority_check,
                "run_command": run_command,
                "file_backend": file_backend,
                "lstat_path": lstat_path,
                "resolve_path": resolve_path,
            }
        )
        return expected_state

    monkeypatch.setattr(
        bundle.backend,
        "collect_bound_scout_post_run_evidence",
        fake_collect,
    )

    authority = lambda: True
    runner = object()
    file_backend = object()
    lstat_path = object()
    resolve_path = object()

    out = bundle.collect_scout_post_run_provenance_bundle(
        inputs,
        observation_authorized=True,
        read_authority_check=authority,
        run_command=runner,
        file_backend=file_backend,
        lstat_path=lstat_path,
        resolve_path=resolve_path,
    )

    assert len(calls) == 1
    assert calls[0] == {
        "inputs": inputs,
        "observation_authorized": True,
        "read_authority_check": authority,
        "run_command": runner,
        "file_backend": file_backend,
        "lstat_path": lstat_path,
        "resolve_path": resolve_path,
    }
    assert out.state_evidence == expected_state
    binding_record = json.loads(out.provenance_binding)
    assert (
        binding_record["accepted_war_college_commit"]
        == inputs.accepted_war_college_commit
    )
    assert (
        binding_record["post_run_state_sha256"]
        == hashlib.sha256(expected_state).hexdigest()
    )


def test_contract_is_source_only_and_non_authorizing():
    contract = bundle.scout_post_run_provenance_bundle_contract()

    assert contract["accepted_war_college_commit_serialized"] is True
    assert contract["expected_engine_commit_serialized"] is True
    assert contract["engine_container_name_serialized"] is True
    assert contract["attempt_marker_path_raw_publication"] is False
    assert contract["attempt_directory_identity_raw_publication"] is False
    assert contract["post_run_state_digest_bound"] is True
    assert contract["backend_collection_and_binding_share_same_inputs"] is True
    assert contract["automatic_host_backend_selection"] is False
    assert contract["contract_call_performs_host_observation"] is False
    assert contract["historical_v1_schema_rewritten"] is False
    assert contract["final_result_acceptance"] is False
    assert all(value is False for value in contract["authority"].values())
    assert (
        contract["next_gate"]
        == "SCOUT_POST_RUN_PROVENANCE_BINDING_SOURCE_REVIEW_REQUIRED"
    )


def test_invalid_context_fails_before_binding():
    bad_inputs = backend.ScoutPostRunBackendInputs(
        experiment_id="abaddon-scout-provenance-v1",
        attempt_marker_path="/tmp/scout/wrong-name.json",
        attempt_marker_sha256="1" * 64,
        attempt_directory_identity=(123, 456),
        engine_container_name="void-scout-repair-canary-4242",
        accepted_war_college_commit="a" * 40,
    )

    with pytest.raises(
        bundle.ScoutPostRunProvenanceBundleHold,
        match="MARKER_NAME_DRIFT",
    ):
        bundle.build_scout_post_run_provenance_binding(
            inputs=bad_inputs,
            state_evidence=_state_evidence(bad_inputs),
        )


def test_authorize_or_execute_always_holds():
    with pytest.raises(
        bundle.ScoutPostRunProvenanceBundleHold,
        match="EXECUTION_AUTHORITY_UNAVAILABLE",
    ):
        bundle.authorize_or_execute()
