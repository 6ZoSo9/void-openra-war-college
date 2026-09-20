from __future__ import annotations

import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from openra_env.learning import abaddon_scout_repair_experiment_request_v1 as request

PAYLOAD = request.build_scout_repair_experiment_request()
RECORD = json.loads(PAYLOAD)
HOLD = request.ScoutRepairExperimentRequestHold


def _encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def test_request_is_canonical_and_non_authorizing():
    assert PAYLOAD == _encode(RECORD)
    assert PAYLOAD.endswith(b"\n") and not PAYLOAD.endswith(b"\n\n")
    out = request.validate_scout_repair_experiment_request(PAYLOAD)
    assert out["request_bytes_valid"] is True
    assert out["request_sha256"] == hashlib.sha256(PAYLOAD).hexdigest()
    assert out["next_gate"] == request.NEXT_GATE
    assert all(value is False for value in out["authority"].values())


def test_fresh_experiment_space_is_deliberately_unselected():
    proposed = RECORD["proposed_experiment"]
    assert proposed["campaign_pair_slot"] is None
    assert proposed["seed"] is None
    assert proposed["opponent_runtime_identity"] is None
    assert proposed["live_control_required"] is None
    assert proposed["maximum_attempts"] is None
    assert proposed["maximum_automatic_retries"] == 0
    assert proposed["reuse_pair03_attempt_marker"] is False
    assert proposed["reuse_pair03_execution_result"] is False
    assert proposed["reuse_v2r13_six_arm_authorization"] is False
    assert proposed["held_out_campaign_space_authorized"] is False


def test_treatment_excludes_candidate252_policy_mutations():
    proposed = RECORD["proposed_experiment"]
    assert proposed["abaddon_doctrine"] == "FEINTER"
    assert proposed["treatment"] == "controller_defaults_plus_abaddon_scout_missions_v1"
    assert proposed["candidate252_policy_mutations_included"] is False
    evidence = RECORD["historical_evidence_reference"]
    assert evidence["shared_scouting_defect_reproduced"] is True
    assert evidence["candidate_252_superiority_established"] is False
    assert evidence["historical_evidence_is_reusable_execution_authority"] is False


def test_repair_source_identities_are_exact_review_expectations():
    refs = RECORD["repair_source_review"]["repair_sources"]
    assert RECORD["repair_source_review"]["pr_number"] == 181
    assert RECORD["repair_source_review"]["reviewed_head"] == request.PR181_HEAD
    assert RECORD["repair_source_review"]["reviewed_tree"] == request.PR181_TREE
    assert RECORD["repair_source_review"]["must_be_accepted_on_main_before_experiment_acceptance"] is True
    assert len(refs) == 4
    assert refs["openra_env/learning/abaddon_scout_missions_v1.py"]["sha256"] == "09bb0a403cdb61fcbcae3e4690bf87a2c0aea4e65f4dcc1c755331492ff33571"
    assert refs["openra_env/learning/abaddon_scout_runner_binding_v1.py"]["git_blob"] == "9e4894b64f0820a53faf8226974d99687066679b"


def test_design_decisions_require_new_guard_readiness_and_result_contract():
    decisions = set(RECORD["required_design_decisions"])
    assert decisions == set(request.REQUIRED_DESIGN_DECISIONS)
    for required in (
        "fresh_non_held_out_experiment_namespace_selected",
        "fresh_seed_selected_without_reusing_pair03_consumed_slot",
        "durable_create_only_attempt_guard_designed",
        "fresh_host_preflight_and_readiness_required",
        "operation_time_revocation_check_required",
        "independent_post_run_cleanup_observation_required",
        "result_record_and_evidence_review_contract_designed",
    ):
        assert required in decisions


def test_all_authority_fields_are_false_and_complete():
    assert set(RECORD["authority"]) == set(request.FALSE_AUTHORITY_FIELDS)
    assert len(RECORD["authority"]) == 22
    assert all(value is False for value in RECORD["authority"].values())
    assert RECORD["matching_request_digest_grants_authority"] is False
    assert RECORD["runtime_gates_enforced_by_this_module"] is False


def test_changed_or_malformed_bytes_reject():
    changes = []
    changed = deepcopy(RECORD)
    changed["proposed_experiment"]["campaign_pair_slot"] = 9
    changes.append(_encode(changed))
    changed = deepcopy(RECORD)
    changed["authority"]["scout_repair_execution_authorized"] = True
    changes.append(_encode(changed))
    changed = deepcopy(RECORD)
    changed["proposed_experiment"]["maximum_automatic_retries"] = 1
    changes.append(_encode(changed))
    changes += [b"", PAYLOAD[:-1], PAYLOAD + b"\n", b" " + PAYLOAD, b"{}\n", b"x" * (request.MAX_REQUEST_BYTES + 1)]
    for payload in changes:
        with pytest.raises(HOLD):
            request.validate_scout_repair_experiment_request(payload)


@pytest.mark.parametrize("value", [None, {}, [], 1, True, "text", bytearray(PAYLOAD), memoryview(PAYLOAD)])
def test_nonbytes_reject(value):
    with pytest.raises(HOLD, match="exact bytes"):
        request.validate_scout_repair_experiment_request(value)


def test_public_contract_is_fresh_and_mutation_safe():
    first = request.scout_repair_experiment_request_contract()
    first["authority"]["scout_repair_execution_authorized"] = True
    first["request"]["required_design_decisions"].clear()
    first["request"]["repair_source_review"]["repair_sources"].clear()
    later = request.scout_repair_experiment_request_contract()
    assert later["request"] == RECORD
    assert later["authority"]["scout_repair_execution_authorized"] is False
    assert later["request"]["required_design_decisions"] == list(request.REQUIRED_DESIGN_DECISIONS)


def test_execution_entrypoint_always_holds():
    for kwargs in ({}, {"authorized": True}, {"pair_slot": 9}, {"confirm": "yes"}):
        with pytest.raises(HOLD, match=request.NEXT_GATE):
            request.authorize_or_execute_scout_repair(**kwargs)


def test_source_imports_only_data_standard_library_modules():
    tree = ast.parse(Path(request.__file__).read_text(encoding="utf-8"))
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.add(node.module)
    assert modules == {"__future__", "hashlib", "json", "typing"}
