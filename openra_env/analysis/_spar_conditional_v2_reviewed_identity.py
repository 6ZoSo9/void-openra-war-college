"""Exact reviewed implementation identity for Conditional Engagement V2.

These constants are authority-grade comparison points, not values learned from
runtime evidence. A trajectory may claim these identities, but the analyzer
must independently require equality with this bundle before reporting reviewed
V2 evidence as verified.
"""
from __future__ import annotations

REVIEWED_V2_SOURCE_COMMIT = "69ad16ed4db3e59a457d0125138de43f78a8fe39"
REVIEWED_V2_CANDIDATE_SHA256 = "27f28a6a46f63a055f8f35c021bafae1035084c444ba7e2009161109ec3efdd6"
REVIEWED_V2_POLICY_SHA256 = "a84bdab79fd731c76c8476cc0d58bbb0a09a984f44deeb0b4fc85d49705c6246"
REVIEWED_V2_SESSION_SHA256 = "2aec4188f8c9158dfb93fa46cdeed36e6e2a84a03f5049e65f94a1278d796fda"
REVIEWED_V2_WRAPPER_SHA256 = "591c52512aefdd3c49e8441e332c793eaeba807100137e813e55aad5721bdc26"

REVIEWED_V2_IDENTITY = {
    "source_commit": REVIEWED_V2_SOURCE_COMMIT,
    "candidate_sha256": REVIEWED_V2_CANDIDATE_SHA256,
    "policy_sha256": REVIEWED_V2_POLICY_SHA256,
    "session_sha256": REVIEWED_V2_SESSION_SHA256,
    "wrapper_sha256": REVIEWED_V2_WRAPPER_SHA256,
}

__all__ = [
    "REVIEWED_V2_SOURCE_COMMIT",
    "REVIEWED_V2_CANDIDATE_SHA256",
    "REVIEWED_V2_POLICY_SHA256",
    "REVIEWED_V2_SESSION_SHA256",
    "REVIEWED_V2_WRAPPER_SHA256",
    "REVIEWED_V2_IDENTITY",
]
