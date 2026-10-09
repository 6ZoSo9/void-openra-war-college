"""Exact-blob review of the read-only Xiphos candidate-training preflight.

Pins the preflight implementation and focused tests.  The review confirms that
host observation remains read-only, candidate training is still unauthorized,
and external operator shutdown/promotion boundaries from the controlled
autonomy policy remain intact.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    apollyon_xiphos_candidate_training_host_preflight_generation2 as preflight,
)


CONTRACT_SCHEMA = (
    "void.apollyon.generation2."
    "xiphos-candidate-training-host-preflight-review.v1"
)
ACCEPTED_BASE_HEAD = "3fb793d7f60ac096398574ca660c8bfc499d6fd1"

PREFLIGHT_PATH = (
    "openra_env/learning/"
    "apollyon_xiphos_candidate_training_host_preflight_generation2.py"
)
PREFLIGHT_GIT_BLOB = "e83de4916441f125992e1a55b17e357619b8e429"

PREFLIGHT_TEST_PATH = (
    "tests/test_apollyon_xiphos_candidate_training_host_preflight_generation2.py"
)
PREFLIGHT_TEST_GIT_BLOB = "fe382843ef201c05da792e8e86163de7a2ff72d5"

POLICY_REVIEW_GIT_BLOB = "4a4b9123e6cad52fcf2bb8b1f70dde0bba36ce20"

NEXT_GATE = "APOLLYON_XIPHOS_CANDIDATE_TRAINING_HOST_READONLY_OBSERVATION_REQUIRED"
NEXT_CHANGE_CLASS = (
    "host_readonly_apollyon_xiphos_candidate_training_qualification_observation"
)


class ApollyonXiphosCandidateTrainingHostPreflightReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ApollyonXiphosCandidateTrainingHostPreflightReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = preflight.apollyon_xiphos_candidate_training_host_preflight_contract()

    _require(
        out.get("policy_review_git_blob") == POLICY_REVIEW_GIT_BLOB
        and out.get("policy_reviewed") is True,
        "Xiphos preflight controlled-autonomy policy binding drift",
    )
    _require(
        out.get("preferred_candidate_training_host") == "Xiphos"
        and out.get("expected_host_normalized") == "xiphos",
        "Xiphos preflight host identity drift",
    )
    _require(
        out.get("source_root") == "/home/zoso/dev/openra-rl-war-college"
        and out.get("model_root")
        == "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1"
        and out.get("venv_python")
        == (
            "/home/zoso/Downloads/void-apollyon-v3-qwen35-4b-lora-v1/"
            "venv/bin/python3.12"
        ),
        "Xiphos preflight runtime-path drift",
    )
    _require(
        out.get("minimum_cuda0_free_fraction_numerator") == 9
        and out.get("minimum_cuda0_free_fraction_denominator") == 10,
        "Xiphos preflight GPU admission drift",
    )
    _require(
        out.get("read_only_host_collection_implemented") is True
        and out.get("shutdown_control_external_to_trainable_model") is True
        and out.get("automatic_promotion_allowed") is False,
        "Xiphos preflight control boundary drift",
    )

    for field in (
        "network_access_by_collection",
        "git_fetch_by_collection",
        "git_checkout_by_collection",
        "git_reset_by_collection",
        "directory_creation_by_collection",
        "package_install_by_collection",
        "service_mutation_by_collection",
        "process_signal_by_collection",
        "model_load_by_collection",
        "model_inference_by_collection",
        "game_execution_by_collection",
        "training_by_collection",
        "weights_update_by_collection",
        "candidate_training_execution_authorized",
        "selfplay_execution_authorized",
        "deployment_authorized",
        "promotion_authorized",
        "scheduler_mutation_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
    ):
        _require(out.get(field) is False, "Xiphos preflight boundary drift: " + field)

    root = Path(__file__).parents[2]
    for rel, expected in (
        (PREFLIGHT_PATH, PREFLIGHT_GIT_BLOB),
        (PREFLIGHT_TEST_PATH, PREFLIGHT_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def apollyon_xiphos_candidate_training_host_preflight_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "preflight_path": PREFLIGHT_PATH,
        "preflight_git_blob": PREFLIGHT_GIT_BLOB,
        "preflight_test_path": PREFLIGHT_TEST_PATH,
        "preflight_test_git_blob": PREFLIGHT_TEST_GIT_BLOB,
        "policy_review_git_blob": POLICY_REVIEW_GIT_BLOB,
        "apollyon_xiphos_candidate_training_host_preflight_reviewed": True,
        "preferred_candidate_training_host": "Xiphos",
        "expected_host_normalized": "xiphos",
        "read_only_host_collection_reviewed": True,
        "minimum_cuda0_free_fraction_numerator": 9,
        "minimum_cuda0_free_fraction_denominator": 10,
        "candidate_training_host_qualification_requires_live_observation": True,
        "candidate_training_host_qualified": False,
        "candidate_training_execution_authorized": False,
        "selfplay_execution_authorized": False,
        "training_performed": False,
        "weights_updated": False,
        "deployment_authorized": False,
        "promotion_authorized": False,
        "network_access_authorized": False,
        "scheduler_mutation_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "shutdown_control_external_to_trainable_model": True,
        "validated_preflight": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def qualify_train_execute_or_promote(*args: Any, **kwargs: Any) -> None:
    raise ApollyonXiphosCandidateTrainingHostPreflightReviewHold(NEXT_GATE)
