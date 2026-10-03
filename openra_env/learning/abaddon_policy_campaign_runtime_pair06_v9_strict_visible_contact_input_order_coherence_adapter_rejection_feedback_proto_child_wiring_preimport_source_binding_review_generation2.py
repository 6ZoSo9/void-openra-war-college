"""Pre-import exact-source review for Pair-06 V9 adapter-feedback child wiring.

This successor review closes the pre-import provenance gap in the earlier
source-binding review.  It does not import or execute the reviewed wiring or
any of its local learning-module dependencies.

Instead it:
1. reads accepted bytes from ACCEPTED_HEAD via Git objects;
2. recursively discovers the local openra_env.learning import closure from
   those accepted bytes;
3. compares every corresponding worktree file byte-for-byte before parsing any
   worktree source; and
4. performs static assertions only on the already-accepted Git bytes.

Thus a dirty worktree cannot execute reviewed module top-level or contract code
before drift is rejected.

No parent wiring, operator wiring, runtime activation, execution request,
attempt, model/game/GPU run, retry, training, promotion, deployment, chain,
wallet/funds, or scheduler authority is granted.
"""

from __future__ import annotations

import ast
from functools import lru_cache
import hashlib
from pathlib import Path
import subprocess
from typing import Any


CONTRACT_SCHEMA = (
    "void.abaddon.generation2."
    "pair06-v9-adapter-rejection-feedback-"
    "proto-child-preimport-source-review-contract.v1"
)

ACCEPTED_HEAD = "421c99f6962620c854c4671579af1268135eef18"
REPOSITORY_ROOT = Path(__file__).parents[2]

WIRING_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_"
    "input_order_coherence_adapter_rejection_feedback_"
    "proto_child_wiring_generation2.py"
)
WIRING_GIT_BLOB = "64af11733bb384959cc7cc5f11d18dab2d9e2c1c"

WIRING_TEST_PATH = (
    "tests/"
    "test_abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_"
    "input_order_coherence_adapter_rejection_feedback_"
    "proto_child_wiring_generation2.py"
)
WIRING_TEST_GIT_BLOB = "27e7f692117a8d4dde9e0a8cc2271218a26fa22a"

FEEDBACK_OVERLAY_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_"
    "input_order_coherence_adapter_rejection_feedback_"
    "overlay_generation2.py"
)
FEEDBACK_OVERLAY_GIT_BLOB = "f720d70d2f7068eeeb05324d3a89aaf6b86daa84"

HISTORICAL_WIRING_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_"
    "input_order_coherence_proto_child_wiring_generation2.py"
)
HISTORICAL_WIRING_GIT_BLOB = "1b87cb5596c219e6118f4b69845dbecaa29a3ace"

HISTORICAL_WIRING_REVIEW_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_"
    "input_order_coherence_proto_child_wiring_"
    "source_binding_review_generation2.py"
)
HISTORICAL_WIRING_REVIEW_GIT_BLOB = (
    "7e96e32361b64f71ccf5c2cfd3c10a33c15429a1"
)

PREDECESSOR_REVIEW_PATH = (
    "openra_env/learning/"
    "abaddon_policy_campaign_runtime_pair06_v9_strict_visible_contact_"
    "input_order_coherence_adapter_rejection_feedback_"
    "proto_child_wiring_source_binding_review_generation2.py"
)
PREDECESSOR_REVIEW_GIT_BLOB = "1027c91108750f25c8d730dc048e34ad8e6df6e0"

ENTRY_PATHS = (
    WIRING_PATH,
    WIRING_TEST_PATH,
    FEEDBACK_OVERLAY_PATH,
    HISTORICAL_WIRING_PATH,
    HISTORICAL_WIRING_REVIEW_PATH,
)

NEXT_GATE = (
    "PAIR06_V9_ADAPTER_REJECTION_FEEDBACK_"
    "PARENT_SUPERVISOR_WIRING_REQUIRED"
)
NEXT_CHANGE_CLASS = (
    "source_only_pair06_v9_adapter_rejection_feedback_"
    "parent_supervisor_wiring"
)


class Pair06V9AdapterFeedbackPreimportSourceReviewHold(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Pair06V9AdapterFeedbackPreimportSourceReviewHold(message)


def _git_blob_sha1(raw: bytes) -> str:
    prefix = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(prefix + raw).hexdigest()


@lru_cache(maxsize=None)
def _accepted_bytes(path: str) -> bytes:
    try:
        proc = subprocess.run(
            [
                "git",
                "-C",
                str(REPOSITORY_ROOT),
                "show",
                f"{ACCEPTED_HEAD}:{path}",
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise Pair06V9AdapterFeedbackPreimportSourceReviewHold(
            "accepted Git source unavailable: " + path
        ) from exc
    return proc.stdout


def _learning_import_paths(raw: bytes, *, path: str) -> tuple[str, ...]:
    try:
        tree = ast.parse(raw.decode("utf-8"), filename=path)
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise Pair06V9AdapterFeedbackPreimportSourceReviewHold(
            "accepted source parse failed: " + path
        ) from exc

    out: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom):
            continue

        module = node.module or ""
        if module == "openra_env.learning":
            for alias in node.names:
                if alias.name == "*":
                    continue
                out.add(
                    "openra_env/learning/"
                    + alias.name
                    + ".py"
                )
        elif module.startswith("openra_env.learning."):
            out.add(module.replace(".", "/") + ".py")

    return tuple(sorted(out))


def _accepted_path_exists(path: str) -> bool:
    try:
        _accepted_bytes(path)
    except Pair06V9AdapterFeedbackPreimportSourceReviewHold:
        return False
    return True


def _discover_accepted_closure() -> tuple[str, ...]:
    pending = list(ENTRY_PATHS)
    seen: set[str] = set()

    while pending:
        path = pending.pop()
        if path in seen:
            continue

        raw = _accepted_bytes(path)
        seen.add(path)

        for candidate in _learning_import_paths(raw, path=path):
            if candidate in seen:
                continue
            if _accepted_path_exists(candidate):
                pending.append(candidate)

    return tuple(sorted(seen))


def _verify_worktree_before_parse(
    *,
    root: Path = REPOSITORY_ROOT,
) -> dict[str, bytes]:
    verified: dict[str, bytes] = {}

    for path in _discover_accepted_closure():
        expected = _accepted_bytes(path)
        target = root / path
        _require(target.is_file(), "reviewed worktree source missing: " + path)

        # Critical ordering: compare raw bytes first. Do not parse, import,
        # compile, or execute the worktree file before this equality passes.
        actual = target.read_bytes()
        _require(
            actual == expected,
            "pre-import worktree source drift: " + path,
        )
        verified[path] = expected

    return verified


def _static_assertions(sources: dict[str, bytes]) -> None:
    wiring = sources[WIRING_PATH].decode("utf-8")
    overlay = sources[FEEDBACK_OVERLAY_PATH].decode("utf-8")
    historical = sources[HISTORICAL_WIRING_PATH].decode("utf-8")
    historical_review = sources[HISTORICAL_WIRING_REVIEW_PATH].decode("utf-8")

    # Parse only accepted Git bytes after the entire worktree closure has
    # already been byte-verified.
    for path, raw in sources.items():
        try:
            ast.parse(raw.decode("utf-8"), filename=path)
        except (UnicodeDecodeError, SyntaxError) as exc:
            raise Pair06V9AdapterFeedbackPreimportSourceReviewHold(
                "verified accepted source parse failed: " + path
            ) from exc

    for token in (
        "class Pair06V9AdapterFeedbackProtoChildHooks",
        "feedback_overlay.Pair06V9AdapterRejectionFeedbackDecisionHooks(",
        'scoped_globals["Pair06V9InputOrderCoherentProtoChildHooks"]',
        'scoped_globals["_scoped_v8_child_run"]',
        '"consumed_v9_attempt_retry_authorized": False',
        '"runtime_execution_authorized": False',
        '"automatic_retry": False',
    ):
        _require(token in wiring, "verified wiring invariant missing: " + token)

    for token in (
        'if name == "__v8_adapter_rejected_unit_ids_invalid__":',
        'reason = "unit_ids invalid"',
        '"sentinel_accepted": False',
        '"sentinel_host_validation_performed": False',
        '"sentinel_world_mutation_performed": False',
        '"execution_authorized": False',
        '"consumed_attempt_retry_authorized": False',
    ):
        _require(token in overlay, "verified overlay invariant missing: " + token)

    _require(
        "feedback_overlay" not in historical,
        "historical input-order wiring unexpectedly contains feedback overlay",
    )
    _require(
        'WIRING_GIT_BLOB = "'
        + HISTORICAL_WIRING_GIT_BLOB
        + '"' in historical_review,
        "historical input-order review binding drift",
    )

    _require(
        _git_blob_sha1(sources[WIRING_PATH]) == WIRING_GIT_BLOB,
        "accepted wiring blob identity drift",
    )
    _require(
        _git_blob_sha1(sources[WIRING_TEST_PATH]) == WIRING_TEST_GIT_BLOB,
        "accepted wiring-test blob identity drift",
    )
    _require(
        _git_blob_sha1(sources[FEEDBACK_OVERLAY_PATH])
        == FEEDBACK_OVERLAY_GIT_BLOB,
        "accepted feedback-overlay blob identity drift",
    )
    _require(
        _git_blob_sha1(sources[HISTORICAL_WIRING_PATH])
        == HISTORICAL_WIRING_GIT_BLOB,
        "accepted historical wiring blob identity drift",
    )
    _require(
        _git_blob_sha1(sources[HISTORICAL_WIRING_REVIEW_PATH])
        == HISTORICAL_WIRING_REVIEW_GIT_BLOB,
        "accepted historical review blob identity drift",
    )


@lru_cache(maxsize=1)
def _validated() -> dict[str, Any]:
    sources = _verify_worktree_before_parse()
    _static_assertions(sources)

    closure = tuple(sorted(sources))
    return {
        "accepted_head": ACCEPTED_HEAD,
        "verified_closure_paths": closure,
        "verified_closure_count": len(closure),
        "wiring_git_blob": WIRING_GIT_BLOB,
        "wiring_test_git_blob": WIRING_TEST_GIT_BLOB,
        "feedback_overlay_git_blob": FEEDBACK_OVERLAY_GIT_BLOB,
        "historical_wiring_git_blob": HISTORICAL_WIRING_GIT_BLOB,
        "historical_wiring_review_git_blob": HISTORICAL_WIRING_REVIEW_GIT_BLOB,
        "predecessor_review_git_blob": PREDECESSOR_REVIEW_GIT_BLOB,
    }


def pair06_v9_adapter_feedback_preimport_source_review_contract() -> dict[str, Any]:
    validated = dict(_validated())
    return {
        "schema": CONTRACT_SCHEMA,
        "accepted_head": ACCEPTED_HEAD,
        "pair_slot": 6,
        "arm": "baseline",
        "policy_id": "pair06-v9-strict-visible-contact-envelope-v1",
        "preimport_source_review_implemented": True,
        "reviewed_modules_imported_by_review": False,
        "reviewed_modules_executed_by_review": False,
        "worktree_bytes_verified_before_parse": True,
        "accepted_git_bytes_only_static_analysis": True,
        "reachable_local_import_closure_verified": True,
        "preimport_drift_fail_closed": True,
        "top_level_sentinel_execution_possible": False,
        "wiring_git_blob": WIRING_GIT_BLOB,
        "wiring_test_git_blob": WIRING_TEST_GIT_BLOB,
        "feedback_overlay_git_blob": FEEDBACK_OVERLAY_GIT_BLOB,
        "historical_wiring_git_blob": HISTORICAL_WIRING_GIT_BLOB,
        "historical_wiring_review_git_blob": HISTORICAL_WIRING_REVIEW_GIT_BLOB,
        "predecessor_review_git_blob": PREDECESSOR_REVIEW_GIT_BLOB,
        "verified_closure_count": validated["verified_closure_count"],
        "verified_closure_paths": validated["verified_closure_paths"],
        "consumed_v9_attempt_retry_authorized": False,
        "parent_supervisor_wiring_implemented": False,
        "operator_wiring_implemented": False,
        "runtime_activation_authorized": False,
        "runtime_execution_authorized": False,
        "replay_authorized": False,
        "automatic_retry": False,
        "training_authorized": False,
        "automatic_corpus_admission": False,
        "weights_update_authorized": False,
        "automatic_policy_promotion_authorized": False,
        "deployment_authorized": False,
        "void_chain_mutation_authorized": False,
        "wallet_or_funds_action_authorized": False,
        "scheduler_mutation_authorized": False,
        "source_frontier_closed": True,
        "execution_blockers": (NEXT_GATE,),
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
    }


def wire_parent_or_execute(*args: Any, **kwargs: Any) -> None:
    raise Pair06V9AdapterFeedbackPreimportSourceReviewHold(NEXT_GATE)
