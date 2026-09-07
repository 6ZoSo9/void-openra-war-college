#!/usr/bin/env python3
"""Bind controller evidence to durable currentness and trusted VOID-node producer authentication."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import verify_controller_evidence_isolation_v1 as structural
from scripts import verify_controller_evidence_producer_auth_v1 as producer_auth
from scripts import war_college_designated_producer_trust_root_v1 as designated_root
from scripts.controller_attempt_admission_store_v1 import (
    AdmissionHold,
    AttemptIdentity,
    consume_joint_evidence,
    load_attempt,
)

MARKER = "VOID_WAR_COLLEGE_CONTROLLER_DURABLE_CURRENTNESS_INTEGRATION_V1"
RUNTIME_EVIDENCE = "PENDING_DESIGNATED_HOST"
STORE_WAR_COLLEGE_SOURCE_BASE = "f57c561f3a4c742e34d820933be40dd7d4253951"
STORE_RELATIVE_PATH = Path("war_college/controller_attempt_admission_v3.sqlite3")


def canonical_store_path() -> Path:
    raw = os.environ.get("VOID_DATA_DIR")
    if not raw:
        raise AdmissionHold("HOLD_VOID_DATA_DIR_REQUIRED")
    root = Path(raw)
    if not root.is_absolute():
        raise AdmissionHold("HOLD_VOID_DATA_DIR_NOT_ABSOLUTE")
    return root.resolve(strict=False) / STORE_RELATIVE_PATH


def _identity_bindings(identity: AttemptIdentity | None) -> list[dict[str, str]]:
    if identity is None:
        return []
    return sorted(
        [
            {
                "controller_id": identity.controller_a_id,
                "player_id": identity.controller_a_player_id,
            },
            {
                "controller_id": identity.controller_b_id,
                "player_id": identity.controller_b_player_id,
            },
        ],
        key=lambda item: (item["controller_id"], item["player_id"]),
    )


def _report(
    *,
    contract: str,
    holds: list[str],
    phase: str,
    identity: AttemptIdentity | None = None,
    session_generation: int | None = None,
    joint_evidence_sha256: str | None = None,
    consumption_sha256: str | None = None,
    structural_report: dict[str, Any] | None = None,
    producer_auth_report: dict[str, Any] | None = None,
    designated_root_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    producer_signature_green = (
        isinstance(producer_auth_report, dict)
        and producer_auth_report.get("contract") == "GREEN"
    )
    trust_root_green = (
        isinstance(designated_root_report, dict)
        and designated_root_report.get("contract") == "GREEN"
    )
    return {
        "attempt_id": identity.attempt_id if identity is not None else None,
        "canonical_store_relative_path": str(STORE_RELATIVE_PATH),
        "consumption_sha256": consumption_sha256,
        "contract": contract,
        "controller_player_bindings": _identity_bindings(identity),
        "designated_host_label": (
            designated_root_report.get("designated_host_label")
            if isinstance(designated_root_report, dict)
            else None
        ),
        "designated_producer_trust_root_green": trust_root_green,
        "designated_producer_trust_root_id": (
            designated_root_report.get("trust_root_id")
            if isinstance(designated_root_report, dict)
            else designated_root.PRODUCTION_TRUST_ROOT.root_id
        ),
        "holds": sorted(set(holds)),
        "joint_evidence_sha256": joint_evidence_sha256,
        "marker": MARKER,
        "phase": phase,
        "producer_auth_transcript_sha256": (
            producer_auth_report.get("transcript_sha256")
            if isinstance(producer_auth_report, dict)
            else None
        ),
        "producer_id": identity.producer_id if identity is not None else None,
        "producer_public_key_sha256": (
            identity.producer_public_key_sha256 if identity is not None else None
        ),
        "producer_signature_authentication_green": producer_signature_green,
        "runtime_evidence": RUNTIME_EVIDENCE,
        "session_generation": session_generation,
        "structural_contract": (
            structural_report.get("contract")
            if isinstance(structural_report, dict)
            else None
        ),
        "structural_holds": (
            list(structural_report.get("holds", []))
            if isinstance(structural_report, dict)
            else []
        ),
        "trusted_producer_authentication_green": (
            producer_signature_green and trust_root_green
        ),
    }


def _store_source_hold(identity: AttemptIdentity) -> str | None:
    if identity.source_generation != structural.GENERATION:
        return "HOLD_STORE_SOURCE_GENERATION_MISMATCH"
    if identity.war_college_commit != STORE_WAR_COLLEGE_SOURCE_BASE:
        return "HOLD_STORE_WAR_COLLEGE_SOURCE_BASE_MISMATCH"
    if identity.engine_commit != structural.ENGINE_FROZEN_COMMIT:
        return "HOLD_STORE_ENGINE_COMMIT_MISMATCH"
    return None


def _observed_controller_player_bindings(
    evidence: dict[str, Any],
) -> set[tuple[str, str]] | None:
    controllers = evidence.get("controllers")
    if type(controllers) is not list or len(controllers) != 2:
        return None
    bindings: set[tuple[str, str]] = set()
    for record in controllers:
        if type(record) is not dict:
            return None
        controller_id = record.get("controller_id")
        player_id = record.get("player_id")
        if type(controller_id) is not str or type(player_id) is not str:
            return None
        bindings.add((controller_id, player_id))
    if len(bindings) != 2:
        return None
    return bindings


def verify_and_consume_evidence(
    evidence: Any,
    producer_auth_record: Any,
) -> dict[str, Any]:
    if type(evidence) is not dict:
        return _report(
            contract="HOLD",
            holds=["HOLD_EVIDENCE_NOT_OBJECT"],
            phase="attempt_lookup",
        )

    attempt_id = evidence.get("attempt_id")
    try:
        store_path = canonical_store_path()
        identity, current_generation = load_attempt(store_path, attempt_id)
    except AdmissionHold as error:
        return _report(
            contract="HOLD",
            holds=[str(error)],
            phase="attempt_lookup",
        )

    source_hold = _store_source_hold(identity)
    if source_hold is not None:
        return _report(
            contract="HOLD",
            holds=[source_hold],
            phase="store_source_binding",
            identity=identity,
            session_generation=current_generation,
        )

    structural_report = structural.verify_evidence(
        evidence,
        expected_attempt_id=identity.attempt_id,
        expected_controller_session_generation=current_generation,
    )
    if structural_report.get("contract") != "GREEN":
        return _report(
            contract="HOLD",
            holds=list(structural_report.get("holds", [])),
            phase="structural_verification",
            identity=identity,
            session_generation=current_generation,
            structural_report=structural_report,
        )

    observed = _observed_controller_player_bindings(evidence)
    expected = {
        (identity.controller_a_id, identity.controller_a_player_id),
        (identity.controller_b_id, identity.controller_b_player_id),
    }
    if observed != expected:
        return _report(
            contract="HOLD",
            holds=["HOLD_DURABLE_CONTROLLER_PLAYER_MAPPING_MISMATCH"],
            phase="durable_controller_player_binding",
            identity=identity,
            session_generation=current_generation,
            structural_report=structural_report,
        )

    joint_digest = structural_report.get("admitted_joint_evidence_sha256")
    if type(joint_digest) is not str:
        return _report(
            contract="HOLD",
            holds=["HOLD_STRUCTURAL_JOINT_DIGEST_NOT_ADMITTED"],
            phase="pre_auth",
            identity=identity,
            session_generation=current_generation,
            structural_report=structural_report,
        )

    auth_report = producer_auth.verify_producer_auth(
        producer_auth_record,
        identity=identity,
        session_generation=current_generation,
        joint_evidence_sha256=joint_digest,
        evidence_generation=structural.GENERATION,
        war_college_frozen_commit=structural.WAR_COLLEGE_FROZEN_COMMIT,
        engine_frozen_commit=structural.ENGINE_FROZEN_COMMIT,
    )
    if auth_report.get("contract") != "GREEN":
        return _report(
            contract="HOLD",
            holds=list(auth_report.get("holds", [])),
            phase="producer_authentication",
            identity=identity,
            session_generation=current_generation,
            joint_evidence_sha256=joint_digest,
            structural_report=structural_report,
            producer_auth_report=auth_report,
        )

    root_report = designated_root.verify_designated_producer_trust_v1(
        identity=identity,
        producer_auth_record=producer_auth_record,
    )
    if root_report.get("contract") != "GREEN":
        return _report(
            contract="HOLD",
            holds=list(root_report.get("holds", [])),
            phase="designated_producer_trust_root",
            identity=identity,
            session_generation=current_generation,
            joint_evidence_sha256=joint_digest,
            structural_report=structural_report,
            producer_auth_report=auth_report,
            designated_root_report=root_report,
        )

    try:
        consumption = consume_joint_evidence(
            store_path,
            identity,
            session_generation=current_generation,
            joint_evidence_sha256=joint_digest,
        )
    except AdmissionHold as error:
        return _report(
            contract="HOLD",
            holds=[str(error)],
            phase="durable_consume",
            identity=identity,
            session_generation=current_generation,
            joint_evidence_sha256=joint_digest,
            structural_report=structural_report,
            producer_auth_report=auth_report,
            designated_root_report=root_report,
        )

    return _report(
        contract="GREEN",
        holds=[],
        phase="consumed",
        identity=identity,
        session_generation=current_generation,
        joint_evidence_sha256=joint_digest,
        consumption_sha256=str(consumption["consumption_sha256"]),
        structural_report=structural_report,
        producer_auth_report=auth_report,
        designated_root_report=root_report,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("producer_auth", type=Path)
    args = parser.parse_args(argv)

    try:
        evidence = structural._read_evidence_file(args.evidence)
        auth_record = producer_auth.read_producer_auth_file(args.producer_auth)
        report = verify_and_consume_evidence(evidence, auth_record)
    except structural.AdmissionError as error:
        report = _report(
            contract="HOLD",
            holds=[str(error)],
            phase="evidence_read",
        )
    except producer_auth.ProducerAuthAdmissionError as error:
        report = _report(
            contract="HOLD",
            holds=[str(error)],
            phase="producer_auth_read",
        )
    except (OSError, ValueError, RecursionError) as error:
        report = _report(
            contract="HOLD",
            holds=[f"HOLD_INTEGRATION_FAILURE:{type(error).__name__}"],
            phase="integration_failure",
        )

    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["contract"] == "GREEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
