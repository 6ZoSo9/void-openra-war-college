"""Bounded adapter for independent scout post-run read-only probes.

The adapter owns no host-observation backend. A separately reviewed caller
supplies five read-only probe callbacks plus a current read-authority callback.

Each required probe is called at most once, in fixed order, with an authority
recheck immediately before it. False, non-boolean, revoked, or exceptional
observations HOLD. There is no retry, service action, process action, filesystem
mutation, game/model execution, deployment, chain mutation, or funds action.
"""

from __future__ import annotations

import json
from typing import Any, Callable


EVIDENCE_SCHEMA = "void.abaddon.scout-post-run-state-evidence.v1"
OBSERVER_CONTRACT_GIT_BLOB = "fd71ac745c10349047d49f753ecfce1aab712648"
MAX_EVIDENCE_BYTES = 65536

REQUIRED_OBSERVATIONS = (
    "attempt_marker_present",
    "runtime_service_inactive",
    "engine_container_absent",
    "model_process_absent",
    "source_checkout_clean",
)

FALSE_CLAIMS = (
    "callback_return_used_as_shutdown_proof",
    "historical_cleanup_print_used_as_shutdown_proof",
    "automatic_retry",
    "pair03_attempt_reused",
    "pair03_attempt_reset",
)


class ScoutPostRunObserverHold(RuntimeError):
    """A required read-only observation was unavailable or not affirmative."""


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ScoutPostRunObserverHold(code)


def _valid_hex64(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _valid_experiment_id(value: Any) -> bool:
    return (
        type(value) is str
        and 1 <= len(value) <= 128
        and value.startswith("abaddon-scout-")
        and "pair03" not in value
        and all(character in "abcdefghijklmnopqrstuvwxyz0123456789._-" for character in value)
    )


def observe_post_run_state(
    *,
    experiment_id: str,
    attempt_marker_sha256: str,
    observer_contract_git_blob: str,
    read_authority_check: Callable[[], bool],
    probes: dict[str, Callable[[], bool]],
) -> bytes:
    """Call each supplied read-only probe once and emit canonical evidence bytes."""
    _require(_valid_experiment_id(experiment_id), "SCOUT_OBSERVER_EXPERIMENT_ID_INVALID")
    _require(_valid_hex64(attempt_marker_sha256), "SCOUT_OBSERVER_ATTEMPT_DIGEST_INVALID")
    _require(
        type(observer_contract_git_blob) is str
        and observer_contract_git_blob == OBSERVER_CONTRACT_GIT_BLOB,
        "SCOUT_OBSERVER_CONTRACT_SOURCE_DRIFT",
    )
    _require(callable(read_authority_check), "SCOUT_OBSERVER_AUTHORITY_CALLBACK_REQUIRED")
    _require(
        type(probes) is dict and set(probes) == set(REQUIRED_OBSERVATIONS),
        "SCOUT_OBSERVER_PROBE_SET_INVALID",
    )
    for name in REQUIRED_OBSERVATIONS:
        _require(callable(probes[name]), f"SCOUT_OBSERVER_PROBE_NOT_CALLABLE:{name}")

    observations: dict[str, bool] = {}
    for name in REQUIRED_OBSERVATIONS:
        try:
            authority = read_authority_check()
        except Exception as exc:
            raise ScoutPostRunObserverHold(
                f"SCOUT_OBSERVER_AUTHORITY_ERROR:{type(exc).__name__}"
            ) from None
        _require(authority is True, f"SCOUT_OBSERVER_AUTHORITY_REQUIRED:{name}")

        try:
            observed = probes[name]()
        except Exception as exc:
            raise ScoutPostRunObserverHold(
                f"SCOUT_OBSERVER_PROBE_ERROR:{name}:{type(exc).__name__}"
            ) from None
        _require(
            observed is True,
            f"SCOUT_OBSERVER_POSITIVE_OBSERVATION_REQUIRED:{name}",
        )
        observations[name] = True

    record = {
        "schema": EVIDENCE_SCHEMA,
        "record_kind": "independent_post_run_state_declaration",
        "experiment_id": experiment_id,
        "attempt_marker_sha256": attempt_marker_sha256,
        "observer_contract_git_blob": OBSERVER_CONTRACT_GIT_BLOB,
        "observations": observations,
        "claims": {field: False for field in FALSE_CLAIMS},
    }
    raw = (
        json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("ascii")
    _require(len(raw) <= MAX_EVIDENCE_BYTES, "SCOUT_OBSERVER_EVIDENCE_BYTE_LIMIT")
    return raw


def authorize_or_execute(*args: Any, **kwargs: Any) -> None:
    """Post-run observation never creates execution authority."""
    raise ScoutPostRunObserverHold("SCOUT_OBSERVER_EXECUTION_AUTHORITY_UNAVAILABLE")
