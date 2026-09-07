#!/usr/bin/env python3
"""Immutable designated-producer trust root for War College evidence."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from cryptography.hazmat.primitives import serialization

from scripts import verify_controller_evidence_producer_auth_v1 as producer_auth
from scripts.controller_attempt_admission_store_v1 import AttemptIdentity

MARKER = "VOID_WAR_COLLEGE_DESIGNATED_PRODUCER_TRUST_ROOT_V1"
VERSION = 1
AUTHORITY_SCOPE = "war_college_designated_producer_verify"

_NODE_ID_RE = re.compile(r"[0-9a-f]{32}\Z")
_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
_SHA1_RE = re.compile(r"[0-9a-f]{40}\Z")
_GIT_COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")
_ISO_UTC_MS_RE = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z\Z"
)
_ROOT_ID_RE = re.compile(r"voidwcdptr1_[0-9a-f]{64}\Z")


@dataclass(frozen=True)
class DesignatedProducerTrustRootV1:
    marker: str
    version: int
    authority_scope: str
    designated_host_label: str
    source_repository: str
    source_commit: str
    trust_profile_path: str
    trust_profile_blob_sha1: str
    trust_profile_marker: str
    identity_confirmation_path: str
    identity_confirmation_blob_sha1: str
    producer_node_id: str
    public_key_fingerprint_sha256: str
    binding_sha256: str
    expires_at_utc: str
    root_id: str


def _payload(root: DesignatedProducerTrustRootV1) -> dict[str, Any]:
    return {
        "authority_scope": root.authority_scope,
        "binding_sha256": root.binding_sha256,
        "designated_host_label": root.designated_host_label,
        "expires_at_utc": root.expires_at_utc,
        "identity_confirmation_blob_sha1": root.identity_confirmation_blob_sha1,
        "identity_confirmation_path": root.identity_confirmation_path,
        "marker": root.marker,
        "producer_node_id": root.producer_node_id,
        "public_key_fingerprint_sha256": root.public_key_fingerprint_sha256,
        "source_commit": root.source_commit,
        "source_repository": root.source_repository,
        "trust_profile_blob_sha1": root.trust_profile_blob_sha1,
        "trust_profile_marker": root.trust_profile_marker,
        "trust_profile_path": root.trust_profile_path,
        "version": root.version,
    }


def derive_trust_root_id_v1(root: DesignatedProducerTrustRootV1) -> str:
    encoded = json.dumps(
        _payload(root),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")
    return "voidwcdptr1_" + hashlib.sha256(encoded).hexdigest()


def _parse_expiry(value: str) -> datetime:
    if _ISO_UTC_MS_RE.fullmatch(value) is None:
        raise ValueError("trust-root expiry is not canonical UTC milliseconds")
    parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    if parsed.tzinfo is None:
        raise ValueError("trust-root expiry is timezone-naive")
    return parsed.astimezone(timezone.utc)


def validate_trust_root_v1(root: DesignatedProducerTrustRootV1) -> None:
    if root.marker != MARKER:
        raise ValueError("trust-root marker mismatch")
    if root.version != VERSION:
        raise ValueError("trust-root version mismatch")
    if root.authority_scope != AUTHORITY_SCOPE:
        raise ValueError("trust-root authority scope mismatch")
    if root.designated_host_label != "precision":
        raise ValueError("trust-root designated host mismatch")
    if root.source_repository != "6ZoSo9/void-node":
        raise ValueError("trust-root source repository mismatch")
    if _GIT_COMMIT_RE.fullmatch(root.source_commit) is None:
        raise ValueError("trust-root source commit invalid")
    if root.trust_profile_path != "config/void-tor-agent-access-client-v1.json":
        raise ValueError("trust-root profile path mismatch")
    if _SHA1_RE.fullmatch(root.trust_profile_blob_sha1) is None:
        raise ValueError("trust-root profile blob invalid")
    if root.trust_profile_marker != "VOID_TOR_AGENT_ACCESS_CLIENT_PROFILE_V1":
        raise ValueError("trust-root profile marker mismatch")
    if (
        root.identity_confirmation_path
        != "docs/public/local-multibox-nimo-rejoin-operator-runbook-v1.md"
    ):
        raise ValueError("trust-root identity confirmation path mismatch")
    if _SHA1_RE.fullmatch(root.identity_confirmation_blob_sha1) is None:
        raise ValueError("trust-root identity confirmation blob invalid")
    if _NODE_ID_RE.fullmatch(root.producer_node_id) is None:
        raise ValueError("trust-root producer node id invalid")
    if _SHA256_RE.fullmatch(root.public_key_fingerprint_sha256) is None:
        raise ValueError("trust-root public-key fingerprint invalid")
    if _SHA256_RE.fullmatch(root.binding_sha256) is None:
        raise ValueError("trust-root binding digest invalid")
    _parse_expiry(root.expires_at_utc)
    if _ROOT_ID_RE.fullmatch(root.root_id) is None:
        raise ValueError("trust-root id invalid")
    if derive_trust_root_id_v1(root) != root.root_id:
        raise ValueError("trust-root id mismatch")


PRODUCTION_TRUST_ROOT = DesignatedProducerTrustRootV1(
    marker=MARKER,
    version=VERSION,
    authority_scope=AUTHORITY_SCOPE,
    designated_host_label="precision",
    source_repository="6ZoSo9/void-node",
    source_commit="0cb5832f88eab7c9a1678328e546f2a307b71530",
    trust_profile_path="config/void-tor-agent-access-client-v1.json",
    trust_profile_blob_sha1="c181e5872650b2a1c29d0d3cc958676db34043b0",
    trust_profile_marker="VOID_TOR_AGENT_ACCESS_CLIENT_PROFILE_V1",
    identity_confirmation_path=(
        "docs/public/local-multibox-nimo-rejoin-operator-runbook-v1.md"
    ),
    identity_confirmation_blob_sha1="34f88de65129010a2090303028809002981061c8",
    producer_node_id="9d89483769e469e0473b489dc50dba96",
    public_key_fingerprint_sha256=(
        "2f52b928cb00bf309510d1edef299554277fba6d52bfd1ddb52b9b015397c50b"
    ),
    binding_sha256=(
        "f625a192b3f97a29513603b2a433e4acc86f15fb81f9fa536cc44541e5873521"
    ),
    expires_at_utc="2027-01-26T08:39:09.089Z",
    root_id=(
        "voidwcdptr1_"
        "6f5e9ea9e192cae9166c5be293e94437748e5d21d72bd8f27681a61979a29ba9"
    ),
)

validate_trust_root_v1(PRODUCTION_TRUST_ROOT)


def public_key_der_fingerprint_sha256_v1(raw_pem: Any) -> str | None:
    derived = producer_auth.derive_void_node_identity_from_public_pem(raw_pem)
    if derived is None:
        return None
    _node_id, _pem_sha256, key = derived
    der = key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return hashlib.sha256(der).hexdigest()


def verify_designated_producer_trust_v1(
    *,
    identity: AttemptIdentity,
    producer_auth_record: Any,
    root: DesignatedProducerTrustRootV1 = PRODUCTION_TRUST_ROOT,
    now_utc: datetime | None = None,
) -> dict[str, Any]:
    holds: list[str] = []

    try:
        validate_trust_root_v1(root)
    except ValueError:
        holds.append("HOLD_DESIGNATED_PRODUCER_TRUST_ROOT_INVALID")

    now = now_utc or datetime.now(timezone.utc)
    if now.tzinfo is None:
        holds.append("HOLD_DESIGNATED_PRODUCER_TRUST_TIME_NAIVE")
    else:
        now = now.astimezone(timezone.utc)
        try:
            expiry = _parse_expiry(root.expires_at_utc)
        except ValueError:
            holds.append("HOLD_DESIGNATED_PRODUCER_TRUST_ROOT_INVALID")
        else:
            if now >= expiry:
                holds.append("HOLD_DESIGNATED_PRODUCER_TRUST_ROOT_EXPIRED")

    if identity.producer_id != root.producer_node_id:
        holds.append("HOLD_DESIGNATED_PRODUCER_NODE_ID_MISMATCH")

    if type(producer_auth_record) is not dict:
        holds.append("HOLD_DESIGNATED_PRODUCER_AUTH_RECORD_INVALID")
        public_key_pem = None
    else:
        public_key_pem = producer_auth_record.get("producer_public_key_pem")

    derived = producer_auth.derive_void_node_identity_from_public_pem(public_key_pem)
    if derived is None:
        holds.append("HOLD_DESIGNATED_PRODUCER_PUBLIC_KEY_INVALID")
    else:
        derived_node_id, pem_sha256, _key = derived
        if derived_node_id != root.producer_node_id:
            holds.append("HOLD_DESIGNATED_PRODUCER_PUBLIC_KEY_NODE_ID_MISMATCH")
        if identity.producer_public_key_sha256 != pem_sha256:
            holds.append("HOLD_DESIGNATED_PRODUCER_STORE_PUBLIC_KEY_MISMATCH")
        fingerprint = public_key_der_fingerprint_sha256_v1(public_key_pem)
        if fingerprint != root.public_key_fingerprint_sha256:
            holds.append("HOLD_DESIGNATED_PRODUCER_PUBLIC_KEY_FINGERPRINT_MISMATCH")

    if holds:
        return {
            "contract": "HOLD",
            "holds": sorted(set(holds)),
            "trust_root_id": root.root_id,
            "designated_host_label": root.designated_host_label,
            "source_commit": root.source_commit,
            "producer_node_id": root.producer_node_id,
        }

    return {
        "contract": "GREEN",
        "holds": [],
        "trust_root_id": root.root_id,
        "designated_host_label": root.designated_host_label,
        "source_commit": root.source_commit,
        "producer_node_id": root.producer_node_id,
        "public_key_fingerprint_sha256": root.public_key_fingerprint_sha256,
        "binding_sha256": root.binding_sha256,
        "expires_at_utc": root.expires_at_utc,
    }
