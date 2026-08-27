"""Optional fail-closed validation for Conditional Engagement V2 evidence."""
from __future__ import annotations

import hashlib
from collections import Counter
from pathlib import Path
from typing import Any

from ._spar_conditional_v2_reviewed_identity import REVIEWED_V2_IDENTITY
from ._spar_contract import (
    MAX_TRAJECTORY_BYTES,
    SHA256,
    SHA40,
    ContractError,
    _arr,
    _bool,
    _int,
    _jsonl,
    _obj,
    _pattern,
    _read,
    _str,
)

RUN_SCHEMA = "void.apollyon.conditional-engagement-run-binding.v2"
PREPARED_SCHEMA = "void.apollyon.conditional-engagement-prepared-round.v2"
ACCEPTED_SCHEMA = "void.apollyon.conditional-engagement-accepted-round.v2"
DECISION_SCHEMA = "void.apollyon.conditional-engagement-decision.v2"
MODES = (
    "REBUILD_FORCE",
    "ATTRITION_BRAKE",
    "CONTACT_RESPONSE",
    "MEASURED_CONTACT",
    "ENGAGEMENT_DEFICIT",
    "BALANCED_SEARCH",
)


def _text_array(value: Any, label: str) -> list[str]:
    rows = _arr(value, label)
    return [_str(item, f"{label}[{index}]") for index, item in enumerate(rows)]


def _run_binding(header: dict[str, Any]) -> dict[str, Any] | None:
    raw = header.get("conditional_engagement_v2")
    if raw is None:
        return None
    raw = _obj(raw, "run_header.conditional_engagement_v2")
    if _str(raw.get("schema"), "V2 run schema") != RUN_SCHEMA:
        raise ContractError("V2 run schema mismatch")
    _bool(raw.get("candidate_only"), "V2 candidate_only", True)
    for key in (
        "automatic_apollyon_weight_mutation",
        "automatic_abaddon_policy_promotion",
        "automatic_corpus_admission",
    ):
        _bool(raw.get(key), f"V2 {key}", False)

    parsed = {
        "source_commit": _pattern(raw.get("source_commit"), "V2 source_commit", SHA40),
        "candidate_sha256": _pattern(raw.get("candidate_sha256"), "V2 candidate SHA", SHA256),
        "policy_sha256": _pattern(raw.get("policy_sha256"), "V2 policy SHA", SHA256),
        "session_sha256": _pattern(raw.get("session_sha256"), "V2 session SHA", SHA256),
        "wrapper_sha256": _pattern(raw.get("wrapper_sha256"), "V2 wrapper SHA", SHA256),
    }
    for key, expected in REVIEWED_V2_IDENTITY.items():
        if parsed[key] != expected:
            raise ContractError(f"V2 reviewed identity mismatch: {key}")

    return {
        "schema": RUN_SCHEMA,
        "candidate_only": True,
        **parsed,
        "reviewed_identity_verified": True,
        "automatic_apollyon_weight_mutation": False,
        "automatic_abaddon_policy_promotion": False,
        "automatic_corpus_admission": False,
    }


def _round_binding(
    row: dict[str, Any],
    *,
    round_number: int,
    run: dict[str, Any] | None,
) -> str | None:
    raw = row.get("conditional_engagement_v2")
    if run is None:
        if raw is not None:
            raise ContractError("V2 round evidence is present without V2 run binding")
        return None
    if raw is None:
        raise ContractError(f"round {round_number} missing V2 evidence")
    raw = _obj(raw, f"round {round_number} V2 evidence")
    prepared = _obj(raw.get("prepared"), f"round {round_number} V2 prepared")
    accepted = _obj(raw.get("accepted"), f"round {round_number} V2 accepted")

    if _str(prepared.get("schema"), "V2 prepared schema") != PREPARED_SCHEMA:
        raise ContractError("V2 prepared schema mismatch")
    if _int(prepared.get("round"), "V2 prepared round", 1) != round_number:
        raise ContractError("V2 prepared round mismatch")
    if _pattern(prepared.get("candidate_sha256"), "V2 prepared candidate SHA", SHA256) != run["candidate_sha256"]:
        raise ContractError("V2 prepared candidate SHA mismatch")
    _bool(prepared.get("history_committed"), "V2 prepared history_committed", False)

    allowed = _text_array(prepared.get("current_allowed_tool_names"), "V2 current_allowed_tool_names")
    if not allowed or len(allowed) != len(set(allowed)):
        raise ContractError("V2 offered tool names must be nonempty and unique")

    apollyon = _obj(row.get("apollyon"), "V2-bound Apollyon decision")
    host_contract = _obj(apollyon.get("tool_contract"), "V2-bound Apollyon tool contract")
    host_allowed = _text_array(host_contract.get("offered_tool_names"), "Apollyon offered_tool_names")
    if allowed != host_allowed:
        raise ContractError("V2 prepared tool surface does not match host tool contract")

    policy_decision = _obj(prepared.get("decision"), "V2 policy decision")
    if _str(policy_decision.get("schema"), "V2 decision schema") != DECISION_SCHEMA:
        raise ContractError("V2 decision schema mismatch")
    mode = _str(policy_decision.get("mode"), "V2 mode")
    if mode not in MODES:
        raise ContractError(f"unsupported V2 mode {mode!r}")
    reasons = _text_array(policy_decision.get("reasons"), "V2 decision reasons")
    if not reasons:
        raise ContractError("V2 decision reasons must not be empty")
    if _pattern(policy_decision.get("candidate_sha256"), "V2 decision candidate SHA", SHA256) != run["candidate_sha256"]:
        raise ContractError("V2 decision candidate SHA mismatch")
    _bool(policy_decision.get("runtime_seed_branching"), "V2 runtime_seed_branching", False)
    evidence = _obj(policy_decision.get("evidence"), "V2 decision evidence")
    if _int(evidence.get("round"), "V2 evidence round", 1) != round_number:
        raise ContractError("V2 evidence round mismatch")
    _str(policy_decision.get("instruction"), "V2 decision instruction")

    coaching = _str(prepared.get("coaching"), "V2 coaching")
    if "CONDITIONAL_ENGAGEMENT_CANDIDATE_V2" not in coaching or f"MODE={mode}" not in coaching:
        raise ContractError("V2 coaching text does not bind the recorded mode")
    if "CURRENT_ALLOWED_TOOL_NAMES" not in coaching or "do not infer hidden state" not in coaching:
        raise ContractError("V2 coaching boundary text is missing")

    if _str(accepted.get("schema"), "V2 accepted schema") != ACCEPTED_SCHEMA:
        raise ContractError("V2 accepted schema mismatch")
    if _int(accepted.get("round"), "V2 accepted round", 1) != round_number:
        raise ContractError("V2 accepted round mismatch")
    if _pattern(accepted.get("candidate_sha256"), "V2 accepted candidate SHA", SHA256) != run["candidate_sha256"]:
        raise ContractError("V2 accepted candidate SHA mismatch")
    if _str(accepted.get("mode"), "V2 accepted mode") != mode:
        raise ContractError("V2 accepted mode mismatch")
    accepted_reasons = _text_array(accepted.get("reasons"), "V2 accepted reasons")
    if accepted_reasons != reasons:
        raise ContractError("V2 accepted reasons do not match prepared decision")
    selected = _str(accepted.get("selected_tool"), "V2 accepted selected_tool")
    if selected != _str(apollyon.get("tool"), "Apollyon accepted tool"):
        raise ContractError("V2 accepted tool does not match Apollyon trajectory tool")
    if selected not in allowed:
        raise ContractError("V2 accepted tool was not in prepared tool surface")
    _bool(accepted.get("function_was_offered"), "V2 function_was_offered", True)
    _int(accepted.get("history_size"), "V2 history_size", 1, 5)
    return mode


def validate_conditional_v2_evidence(
    trajectory_path: Path,
    *,
    expected_trajectory_sha256: str,
) -> dict[str, Any]:
    """Re-read one unchanged generation and verify optional V2 bindings."""
    if SHA256.fullmatch(expected_trajectory_sha256) is None:
        raise ContractError("expected trajectory SHA-256 malformed for V2 validation")
    raw = _read(trajectory_path, "trajectory", MAX_TRAJECTORY_BYTES)
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected_trajectory_sha256:
        raise ContractError("trajectory changed between base and V2 validation")
    rows = _jsonl(raw)
    if not rows:
        raise ContractError("trajectory is empty during V2 validation")
    run = _run_binding(rows[0])
    mode_counts: Counter[str] = Counter()
    rounds = 0
    for row in rows[1:]:
        if row.get("event") != "joint_decision":
            continue
        rounds += 1
        mode = _round_binding(row, round_number=rounds, run=run)
        if mode is not None:
            mode_counts[mode] += 1
    if run is None:
        return {"present": False, "rounds_verified": 0, "mode_counts": {}}
    if rounds == 0:
        raise ContractError("V2 run binding has no joint_decision rows")
    return {
        "present": True,
        **run,
        "rounds_verified": rounds,
        "mode_counts": dict(sorted(mode_counts.items())),
        "all_round_receipts_verified": True,
        "tool_surface_bound": True,
        "accepted_tool_bound": True,
        "runtime_seed_branching": False,
    }
