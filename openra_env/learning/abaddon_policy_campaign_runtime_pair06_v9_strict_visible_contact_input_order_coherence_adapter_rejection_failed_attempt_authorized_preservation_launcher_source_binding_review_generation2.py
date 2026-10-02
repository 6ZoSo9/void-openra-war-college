"""Exact-blob review of the authorized failed-attempt preservation launcher.

Pins the authorized launcher and focused tests. The review confirms exact
authorization binding, exact reviewed preservation source identities, exact
current-main/source requirements, one-shot confirmation, and delegation only to
the reviewed preservation operation.

No preservation is performed by review. Runtime retry and all game/runtime
authority remain false.
"""

from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import hashlib
from pathlib import Path
from typing import Any

from openra_env.learning import (
    abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_input_order_coherence_adapter_rejection_failed_attempt_authorized_preservation_launcher_generation2
    as launcher,
)


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-input-order-adapter-rejection-failed-attempt-"
    "authorized-preservation-launcher-review-contract.v1"
)

ACCEPTED_BASE_HEAD = "b62300044bebf6048a38af2e6cdbc2200d87417b"

LAUNCHER_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "failed_attempt_authorized_preservation_launcher_generation2.py"
)
LAUNCHER_GIT_BLOB = "e89c18b6c9b66a35fab3ad250586e6f2c5978614"

LAUNCHER_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_"
    "strict_visible_contact_input_order_coherence_adapter_rejection_"
    "failed_attempt_authorized_preservation_launcher_generation2.py"
)
LAUNCHER_TEST_GIT_BLOB = "182fea2d9fa887f0c70939578d01da580614391f"

NEXT_GATE = (
    "PAIR06_V9_STRICT_VISIBLE_CONTACT_INPUT_ORDER_COHERENCE_"
    "ADAPTER_REJECTION_FAILED_ATTEMPT_AUTHORIZED_HOST_PRESERVATION_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "authorized_pair06_v9_input_order_adapter_rejection_"
    "failed_attempt_host_preservation"
)


class Pair06V9AdapterRejectionAuthorizedPreservationLauncherReviewHold(
    ValueError
):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9AdapterRejectionAuthorizedPreservationLauncherReviewHold(
            message
        )


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    out = (
        launcher
        .pair06_v9_adapter_rejection_authorized_preservation_launcher_contract()
    )

    _require(
        out.get("authorized_preservation_launcher_implemented") is True,
        "authorized preservation launcher missing",
    )
    _require(
        out.get("attempt_marker_sha256")
        == "78e3008f427b743fb99664a34da7bcc77baaceff884259cab72bd34dfc2f1c2d",
        "authorized preservation launcher marker drift",
    )
    _require(
        out.get("authorization_text_sha256")
        == "5a622d4487d3f93a054a930c5921f3e1879fb2c3e68ea68f9e2d0535dc9e4ab2"
        and out.get("authorization_text_bytes") == 35,
        "authorized preservation launcher authorization binding drift",
    )

    for field in (
        "exact_current_main_required",
        "exact_launcher_source_sha256_required",
        "explicit_launcher_confirmation_token_required",
        "reviewed_preservation_authorization_required",
        "reviewed_preservation_implementation_required",
        "preservation_delegation_exactly_once",
        "non_force_worktree_removal_required",
        "atomic_archive_rename_required",
        "create_only_preservation_receipt_required",
    ):
        _require(
            out.get(field) is True,
            "authorized preservation launcher invariant drift: " + field,
        )

    for field in (
        "runtime_retry_authorized",
        "automatic_retry",
        "execution_request_opened",
        "runtime_execution_authorized",
        "game_execution_authorized",
        "training_authorized",
        "deployment_authorized",
        "void_chain_mutation_authorized",
        "wallet_or_funds_action_authorized",
        "scheduler_mutation_authorized",
        "preservation_performed_by_contract_inspection",
        "host_io_performed_by_contract_inspection",
        "authorization_reusable_after_preservation",
    ):
        _require(
            out.get(field) is False,
            "authorized preservation launcher authority/effect drift: " + field,
        )

    root = Path(__file__).parents[2]
    for rel, expected in (
        (LAUNCHER_PATH, LAUNCHER_GIT_BLOB),
        (LAUNCHER_TEST_PATH, LAUNCHER_TEST_GIT_BLOB),
    ):
        target = root / rel
        _require(target.is_file(), "reviewed source missing: " + rel)
        _require(
            _git_blob_sha1(target.read_bytes()) == expected,
            "reviewed source blob drift: " + rel,
        )

    return deepcopy(out)


def pair06_v9_adapter_rejection_authorized_preservation_launcher_review_contract() -> dict[str, Any]:
    validated = deepcopy(_validated())

    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_base_head": ACCEPTED_BASE_HEAD,
        "launcher_path": LAUNCHER_PATH,
        "launcher_git_blob": LAUNCHER_GIT_BLOB,
        "launcher_test_path": LAUNCHER_TEST_PATH,
        "launcher_test_git_blob": LAUNCHER_TEST_GIT_BLOB,
        "pair06_v9_adapter_rejection_authorized_preservation_launcher_reviewed": True,
        "attempt_marker_sha256": validated["attempt_marker_sha256"],
        "authorization_text_sha256": validated["authorization_text_sha256"],
        "authorization_text_bytes": validated["authorization_text_bytes"],
        "exact_current_main_required": True,
        "exact_launcher_source_sha256_required": True,
        "explicit_launcher_confirmation_token_required": True,
        "preservation_delegation_exactly_once": True,
        "non_force_worktree_removal_required": True,
        "atomic_archive_rename_required": True,
        "create_only_preservation_receipt_required": True,
        "runtime_retry_authorized": False,
        "automatic_retry": False,
        "execution_request_opened": False,
        "runtime_execution_authorized": False,
        "game_execution_authorized": False,
        "training_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "preservation_performed": False,
        "authorization_reusable_after_preservation": False,
        "validated_launcher": validated,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def preserve(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9AdapterRejectionAuthorizedPreservationLauncherReviewHold(
        NEXT_GATE
    )
