\
"""Dormant V2R13 frozen-worktree materializer implementation for Generation-2.

This module implements the exact Git-worktree materialization mechanics required
by the reviewed V2R13 portable-checkout contract, but deliberately bundles no
real host backend and performs no I/O on import.

Materialization is possible only when a caller:
* supplies the already-reviewed explicit V2R13 destination-path record;
* supplies explicit canonical source- and engine-repository roots;
* supplies a path-existence backend and Git runner;
* grants fresh ``materialization_authorized=True``.

When invoked with authority, the implementation creates exactly two detached Git
worktrees at the frozen War College and engine commits, verifies the frozen source
tree, verifies both materialized worktrees are clean and detached, proves the
canonical source/engine checkout snapshots are unchanged, and rolls back any
partially created worktrees on failure. Cleanup is separately explicit and
idempotent.

This source does not authorize runtime activation or execution, model loading or
inference, game execution, training, deployment, VOID-chain mutation, or funds
movement. A separate source-binding review is still required before the
activation blocker can be considered reviewed.
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import PurePosixPath
from typing import Any, Mapping, Protocol

from openra_env.learning import apollyon_v2r13_portable_checkout as portable_checkout
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_activation_binding_review_generation2
    as activation_review,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_v2r13_worktree_observer_generation2
    as worktree_observer,
)
from openra_env.learning import (
    abaddon_policy_campaign_runtime_path_inputs_generation2 as path_inputs,
)

CONTRACT_SCHEMA = (
    "void.abaddon.generation2.v2r13-frozen-worktree-materializer-contract.v1"
)
MATERIALIZATION_SCHEMA = (
    "void.abaddon.generation2.v2r13-frozen-worktree-materialization.v1"
)
CLEANUP_SCHEMA = (
    "void.abaddon.generation2.v2r13-frozen-worktree-cleanup.v1"
)

ACTIVATION_REVIEW_GIT_BLOB = "9449b871cb745b67a7aa29f0d73de378f119a488"
ACTIVATION_REVIEW_SOURCE_SHA256 = (
    "7785cae74baeb5c4a1bfb541b95037019efc6e75134ffc58db4ffbdee041515f"
)
PORTABLE_CHECKOUT_GIT_BLOB = "077fbf5a2847d85113eb8fcba3904b02343ebfef"
PORTABLE_CHECKOUT_SOURCE_SHA256 = (
    "92e16e281d5a9036d78d900f35d854c6fb9783b2bf156c2acab69408d13a015d"
)
PATH_INPUTS_GIT_BLOB = "f65735c7820da9da0205388f1933b6aa9d6dd737"
PATH_INPUTS_SOURCE_SHA256 = (
    "94a2d25fdcd76e9d789a6fbdb8d7b20c80d260c0f118dbc82c5a7d430c7c9899"
)
WORKTREE_OBSERVER_GIT_BLOB = "994f3be5d3344d6ac905c1f5fee9f9490fd4dd3f"
WORKTREE_OBSERVER_SOURCE_SHA256 = (
    "ad2544600833e3f88388e68df5e289a7f69b55f4e8c32f89e8899338e195aacf"
)

NEXT_GATE = "V2R13_FROZEN_WORKTREE_MATERIALIZER_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = "source_only_frozen_worktree_materializer_source_binding_review"

MATERIALIZATION_RECEIPT_FIELDS = frozenset(
    {
        "schema",
        "snapshot_id",
        "source_repository_root",
        "engine_repository_root",
        "frozen_source_root",
        "exact_engine_root",
        "frozen_source_commit",
        "frozen_source_tree",
        "frozen_engine_commit",
        "source_worktree_created",
        "engine_worktree_created",
        "source_worktree_detached",
        "engine_worktree_detached",
        "source_worktree_clean",
        "engine_worktree_clean",
        "canonical_source_checkout_unchanged",
        "canonical_engine_checkout_unchanged",
        "materialization_performed",
        "filesystem_mutation_performed",
        "git_worktree_admin_mutation_performed",
        "canonical_checkout_working_tree_mutation_performed",
        "runtime_activation_performed",
        "runtime_execution_authorized",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
        "path_input_record",
    }
)


class RuntimeV2R13FrozenWorktreeMaterializerHold(ValueError):
    pass


class GitResult(Protocol):
    returncode: int
    stdout: str
    stderr: str


class GitRunner(Protocol):
    def __call__(self, repository_root: str, *args: str) -> GitResult:
        ...


class PathExists(Protocol):
    def __call__(self, path: str) -> bool:
        ...


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeV2R13FrozenWorktreeMaterializerHold(message)


def _lexical_absolute_path(value: Any, label: str) -> str:
    _require(type(value) is str and bool(value), f"{label} must be non-empty string")
    _require("\x00" not in value, f"{label} contains NUL")
    _require(not value.startswith("~"), f"{label} may not use tilde expansion")
    path = PurePosixPath(value)
    _require(path.is_absolute(), f"{label} must be absolute")
    _require(".." not in path.parts, f"{label} may not contain parent traversal")
    _require(str(path) == value, f"{label} must already be lexically normalized")
    _require(value != "/", f"{label} may not be filesystem root")
    return value


def _run(
    run_git: GitRunner,
    repository_root: str,
    *args: str,
    label: str,
    allowed_returncodes: tuple[int, ...] = (0,),
) -> GitResult:
    _require(callable(run_git), "V2R13 Git runner backend required")
    result = run_git(repository_root, *args)
    _require(
        hasattr(result, "returncode")
        and hasattr(result, "stdout")
        and hasattr(result, "stderr"),
        f"{label}: malformed Git result",
    )
    _require(
        type(result.returncode) is int,
        f"{label}: malformed Git returncode",
    )
    _require(
        type(result.stdout) is str and type(result.stderr) is str,
        f"{label}: malformed Git output",
    )
    _require(
        result.returncode in allowed_returncodes,
        f"{label}: Git command failed rc={result.returncode}",
    )
    return result


def _one_line(result: GitResult, label: str) -> str:
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    _require(len(lines) == 1, f"{label}: expected exactly one output line")
    return lines[0].strip()


def _repo_snapshot(repository_root: str, run_git: GitRunner) -> dict[str, str]:
    toplevel = _one_line(
        _run(
            run_git,
            repository_root,
            "rev-parse",
            "--show-toplevel",
            label="canonical repository toplevel",
        ),
        "canonical repository toplevel",
    )
    _require(
        toplevel == repository_root,
        "canonical repository root identity drift",
    )
    head = _one_line(
        _run(
            run_git,
            repository_root,
            "rev-parse",
            "HEAD",
            label="canonical repository HEAD",
        ),
        "canonical repository HEAD",
    )
    tree = _one_line(
        _run(
            run_git,
            repository_root,
            "rev-parse",
            "HEAD^{tree}",
            label="canonical repository tree",
        ),
        "canonical repository tree",
    )
    status = _run(
        run_git,
        repository_root,
        "status",
        "--porcelain",
        "--untracked-files=all",
        label="canonical repository status",
    ).stdout
    return {
        "toplevel": toplevel,
        "head": head,
        "tree": tree,
        "status": status,
    }


def _verify_available_commit(
    repository_root: str,
    commit: str,
    *,
    run_git: GitRunner,
    expected_tree: str | None = None,
) -> None:
    verified = _one_line(
        _run(
            run_git,
            repository_root,
            "rev-parse",
            "--verify",
            f"{commit}^{{commit}}",
            label="frozen commit verification",
        ),
        "frozen commit verification",
    )
    _require(verified == commit, "frozen commit identity drift")
    if expected_tree is not None:
        tree = _one_line(
            _run(
                run_git,
                repository_root,
                "rev-parse",
                f"{commit}^{{tree}}",
                label="frozen source tree verification",
            ),
            "frozen source tree verification",
        )
        _require(tree == expected_tree, "frozen source tree identity drift")


def _registered_worktrees(repository_root: str, run_git: GitRunner) -> tuple[str, ...]:
    out = _run(
        run_git,
        repository_root,
        "worktree",
        "list",
        "--porcelain",
        label="worktree registry census",
    ).stdout
    paths = []
    for line in out.splitlines():
        if line.startswith("worktree "):
            paths.append(line[len("worktree "):])
    return tuple(paths)


def _verify_materialized_worktree(
    path: str,
    *,
    expected_commit: str,
    expected_tree: str | None,
    path_exists: PathExists,
    run_git: GitRunner,
) -> dict[str, Any]:
    _require(path_exists(path) is True, "materialized worktree path missing")
    toplevel = _one_line(
        _run(
            run_git,
            path,
            "rev-parse",
            "--show-toplevel",
            label="materialized worktree toplevel",
        ),
        "materialized worktree toplevel",
    )
    _require(toplevel == path, "materialized worktree root identity drift")
    head = _one_line(
        _run(
            run_git,
            path,
            "rev-parse",
            "HEAD",
            label="materialized worktree HEAD",
        ),
        "materialized worktree HEAD",
    )
    _require(head == expected_commit, "materialized worktree commit drift")
    tree = _one_line(
        _run(
            run_git,
            path,
            "rev-parse",
            "HEAD^{tree}",
            label="materialized worktree tree",
        ),
        "materialized worktree tree",
    )
    if expected_tree is not None:
        _require(tree == expected_tree, "materialized worktree tree drift")
    status = _run(
        run_git,
        path,
        "status",
        "--porcelain",
        "--untracked-files=all",
        label="materialized worktree status",
    ).stdout
    _require(status == "", "materialized worktree is not clean")
    symbolic = _run(
        run_git,
        path,
        "symbolic-ref",
        "-q",
        "HEAD",
        label="materialized worktree detached-HEAD check",
        allowed_returncodes=(0, 1),
    )
    _require(
        symbolic.returncode != 0,
        "materialized worktree unexpectedly attached to branch",
    )
    return {
        "path": path,
        "head": head,
        "tree": tree,
        "clean": True,
        "detached": True,
    }


def _remove_if_present(
    repository_root: str,
    worktree_path: str,
    *,
    path_exists: PathExists,
    run_git: GitRunner,
    label: str,
) -> bool:
    if path_exists(worktree_path) is not True:
        return False
    _run(
        run_git,
        repository_root,
        "worktree",
        "remove",
        "--force",
        worktree_path,
        label=label,
    )
    _require(
        path_exists(worktree_path) is False,
        f"{label}: worktree path remained after cleanup",
    )
    return True


def _validate_dependencies() -> dict[str, Any]:
    review = activation_review.v2r13_activation_binding_review_contract()
    portable = portable_checkout.portable_binding_contract()
    path_requirement = path_inputs.path_input_requirement(path_inputs.V2R13)
    observer = worktree_observer.v2r13_worktree_observer_contract()

    _require(
        review.get("next_gate")
        == "V2R13_FROZEN_WORKTREE_MATERIALIZER_IMPLEMENTATION_REQUIRED",
        "activation-review next-gate drift",
    )
    _require(
        review.get("frozen_worktree_materializer_reviewed") is False,
        "activation review unexpectedly pre-reviews materializer",
    )
    _require(
        review.get("runtime_execution_authorized") is False,
        "activation review unexpectedly authorizes runtime",
    )

    _require(
        portable.get("source_materialization") == "detached_git_worktree",
        "portable checkout source-materialization drift",
    )
    _require(
        portable.get("frozen_war_college_commit")
        == portable_checkout.FROZEN_WAR_COLLEGE_COMMIT,
        "portable frozen source commit drift",
    )
    _require(
        portable.get("frozen_war_college_tree")
        == portable_checkout.FROZEN_WAR_COLLEGE_TREE,
        "portable frozen source tree drift",
    )
    _require(
        portable.get("frozen_engine_commit")
        == portable_checkout.FROZEN_ENGINE_COMMIT,
        "portable frozen engine commit drift",
    )
    _require(
        portable.get("source_worktree_detached") is True,
        "portable checkout detached-source requirement lost",
    )
    _require(
        portable.get("source_worktree_must_be_clean") is True,
        "portable checkout clean-source requirement lost",
    )
    _require(
        portable.get("worktree_cleanup_required") is True,
        "portable checkout cleanup requirement lost",
    )
    _require(
        portable.get("runtime_execution_performed") is False,
        "portable checkout unexpectedly executes runtime",
    )

    _require(
        tuple(path_requirement.get("path_fields", ()))
        == ("frozen_source_root", "exact_engine_root"),
        "V2R13 path-input field set drift",
    )
    _require(
        path_requirement.get("caller_must_supply_all_paths") is True,
        "V2R13 destination paths no longer explicit",
    )
    _require(
        path_requirement.get("tracked_source_defined_autodiscovery") is False,
        "V2R13 path autodiscovery unexpectedly enabled",
    )

    _require(
        observer.get("six_path_classification_leaves_implemented") is True,
        "V2R13 worktree observer incomplete",
    )
    _require(
        observer.get("real_host_backend_implemented") is False,
        "worktree observer unexpectedly bundles real host backend",
    )
    _require(
        observer.get("runtime_execution_authorized") is False,
        "worktree observer unexpectedly authorizes runtime",
    )

    return {
        "activation_binding_review_contract": deepcopy(review),
        "portable_checkout_contract": deepcopy(portable),
        "path_input_requirement": deepcopy(path_requirement),
        "worktree_observer_contract": deepcopy(observer),
    }


def v2r13_frozen_worktree_materializer_contract() -> dict[str, Any]:
    dependencies = _validate_dependencies()
    return {
        "schema": CONTRACT_SCHEMA,
        "snapshot_id": path_inputs.V2R13,
        "activation_review_git_blob": ACTIVATION_REVIEW_GIT_BLOB,
        "activation_review_source_sha256": ACTIVATION_REVIEW_SOURCE_SHA256,
        "portable_checkout_git_blob": PORTABLE_CHECKOUT_GIT_BLOB,
        "portable_checkout_source_sha256": PORTABLE_CHECKOUT_SOURCE_SHA256,
        "path_inputs_git_blob": PATH_INPUTS_GIT_BLOB,
        "path_inputs_source_sha256": PATH_INPUTS_SOURCE_SHA256,
        "worktree_observer_git_blob": WORKTREE_OBSERVER_GIT_BLOB,
        "worktree_observer_source_sha256": WORKTREE_OBSERVER_SOURCE_SHA256,
        "frozen_source_commit": portable_checkout.FROZEN_WAR_COLLEGE_COMMIT,
        "frozen_source_tree": portable_checkout.FROZEN_WAR_COLLEGE_TREE,
        "frozen_engine_commit": portable_checkout.FROZEN_ENGINE_COMMIT,
        "frozen_worktree_materializer_implemented": True,
        "frozen_worktree_materializer_reviewed": False,
        "source_worktree_add_detached_implemented": True,
        "engine_worktree_add_detached_implemented": True,
        "destination_absence_preflight_implemented": True,
        "canonical_repository_snapshot_guard_implemented": True,
        "frozen_source_tree_verification_implemented": True,
        "materialized_commit_verification_implemented": True,
        "materialized_cleanliness_verification_implemented": True,
        "materialized_detached_head_verification_implemented": True,
        "partial_failure_rollback_implemented": True,
        "cleanup_implemented": True,
        "cleanup_idempotent": True,
        "materialization_requires_explicit_authority": True,
        "cleanup_requires_explicit_authority": True,
        "git_runner_backend_injected": True,
        "path_exists_backend_injected": True,
        "automatic_host_backend_selection": False,
        "real_subprocess_backend_implemented": False,
        "real_filesystem_backend_implemented": False,
        "materialization_performed": False,
        "cleanup_performed": False,
        "filesystem_mutation_performed": False,
        "git_worktree_admin_mutation_performed": False,
        "canonical_checkout_working_tree_mutation_performed": False,
        "activation_proven": False,
        "runtime_activation_performed": False,
        "runtime_execution_authorized": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "next_gate": NEXT_GATE,
        "next_change_class": NEXT_CHANGE_CLASS,
        "dependencies": dependencies,
    }


def materialize_v2r13_frozen_worktrees(
    path_record: Mapping[str, Any],
    *,
    source_repository_root: str,
    engine_repository_root: str,
    materialization_authorized: bool,
    path_exists: PathExists,
    run_git: GitRunner,
) -> dict[str, Any]:
    """Materialize exact detached V2R13 worktrees through injected backends."""
    _validate_dependencies()
    _require(
        materialization_authorized is True,
        "GENERATION2_V2R13_FROZEN_WORKTREE_MATERIALIZATION_NOT_AUTHORIZED",
    )
    _require(callable(path_exists), "V2R13 path-existence backend required")
    _require(callable(run_git), "V2R13 Git runner backend required")

    validated = path_inputs.validate_explicit_path_inputs(
        path_inputs.V2R13,
        path_record,
    )
    destinations = validated["paths"]
    source_destination = destinations["frozen_source_root"]
    engine_destination = destinations["exact_engine_root"]

    source_repository_root = _lexical_absolute_path(
        source_repository_root,
        "source_repository_root",
    )
    engine_repository_root = _lexical_absolute_path(
        engine_repository_root,
        "engine_repository_root",
    )

    all_paths = (
        source_repository_root,
        engine_repository_root,
        source_destination,
        engine_destination,
    )
    _require(
        len(set(all_paths)) == len(all_paths),
        "V2R13 repository roots and worktree destinations must be distinct",
    )
    _require(
        path_exists(source_repository_root) is True,
        "source repository root missing",
    )
    _require(
        path_exists(engine_repository_root) is True,
        "engine repository root missing",
    )
    _require(
        path_exists(source_destination) is False,
        "frozen source destination already exists",
    )
    _require(
        path_exists(engine_destination) is False,
        "exact engine destination already exists",
    )

    source_snapshot_before = _repo_snapshot(source_repository_root, run_git)
    engine_snapshot_before = _repo_snapshot(engine_repository_root, run_git)

    _verify_available_commit(
        source_repository_root,
        portable_checkout.FROZEN_WAR_COLLEGE_COMMIT,
        run_git=run_git,
        expected_tree=portable_checkout.FROZEN_WAR_COLLEGE_TREE,
    )
    _verify_available_commit(
        engine_repository_root,
        portable_checkout.FROZEN_ENGINE_COMMIT,
        run_git=run_git,
    )

    _require(
        source_destination
        not in _registered_worktrees(source_repository_root, run_git),
        "frozen source destination already registered as worktree",
    )
    _require(
        engine_destination
        not in _registered_worktrees(engine_repository_root, run_git),
        "exact engine destination already registered as worktree",
    )

    attempted: list[tuple[str, str, str]] = []
    try:
        attempted.append(
            (source_repository_root, source_destination, "source rollback")
        )
        _run(
            run_git,
            source_repository_root,
            "worktree",
            "add",
            "--detach",
            source_destination,
            portable_checkout.FROZEN_WAR_COLLEGE_COMMIT,
            label="frozen source worktree add",
        )
        source_materialized = _verify_materialized_worktree(
            source_destination,
            expected_commit=portable_checkout.FROZEN_WAR_COLLEGE_COMMIT,
            expected_tree=portable_checkout.FROZEN_WAR_COLLEGE_TREE,
            path_exists=path_exists,
            run_git=run_git,
        )

        attempted.append(
            (engine_repository_root, engine_destination, "engine rollback")
        )
        _run(
            run_git,
            engine_repository_root,
            "worktree",
            "add",
            "--detach",
            engine_destination,
            portable_checkout.FROZEN_ENGINE_COMMIT,
            label="exact engine worktree add",
        )
        engine_materialized = _verify_materialized_worktree(
            engine_destination,
            expected_commit=portable_checkout.FROZEN_ENGINE_COMMIT,
            expected_tree=None,
            path_exists=path_exists,
            run_git=run_git,
        )

        source_snapshot_after = _repo_snapshot(source_repository_root, run_git)
        engine_snapshot_after = _repo_snapshot(engine_repository_root, run_git)
        _require(
            source_snapshot_after == source_snapshot_before,
            "canonical source checkout changed during materialization",
        )
        _require(
            engine_snapshot_after == engine_snapshot_before,
            "canonical engine checkout changed during materialization",
        )

    except Exception as error:
        rollback_errors = []
        for repository_root, destination, label in reversed(attempted):
            if path_exists(destination) is not True:
                continue
            try:
                _remove_if_present(
                    repository_root,
                    destination,
                    path_exists=path_exists,
                    run_git=run_git,
                    label=label,
                )
            except Exception as rollback_error:
                rollback_errors.append(
                    f"{destination}:{type(rollback_error).__name__}:{rollback_error}"
                )
        if rollback_errors:
            raise RuntimeV2R13FrozenWorktreeMaterializerHold(
                "V2R13_FROZEN_WORKTREE_ROLLBACK_FAILED:"
                + "|".join(rollback_errors)
            ) from error
        raise

    return {
        "schema": MATERIALIZATION_SCHEMA,
        "snapshot_id": path_inputs.V2R13,
        "source_repository_root": source_repository_root,
        "engine_repository_root": engine_repository_root,
        "frozen_source_root": source_destination,
        "exact_engine_root": engine_destination,
        "frozen_source_commit": source_materialized["head"],
        "frozen_source_tree": source_materialized["tree"],
        "frozen_engine_commit": engine_materialized["head"],
        "source_worktree_created": True,
        "engine_worktree_created": True,
        "source_worktree_detached": source_materialized["detached"],
        "engine_worktree_detached": engine_materialized["detached"],
        "source_worktree_clean": source_materialized["clean"],
        "engine_worktree_clean": engine_materialized["clean"],
        "canonical_source_checkout_unchanged": True,
        "canonical_engine_checkout_unchanged": True,
        "materialization_performed": True,
        "filesystem_mutation_performed": True,
        "git_worktree_admin_mutation_performed": True,
        "canonical_checkout_working_tree_mutation_performed": False,
        "runtime_activation_performed": False,
        "runtime_execution_authorized": False,
        "model_load_performed": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
        "path_input_record": deepcopy(dict(path_record)),
    }


def cleanup_v2r13_frozen_worktrees(
    receipt: Mapping[str, Any],
    *,
    cleanup_authorized: bool,
    path_exists: PathExists,
    run_git: GitRunner,
) -> dict[str, Any]:
    """Idempotently remove only worktrees named by an exact materializer receipt."""
    _require(
        cleanup_authorized is True,
        "GENERATION2_V2R13_FROZEN_WORKTREE_CLEANUP_NOT_AUTHORIZED",
    )
    _require(callable(path_exists), "V2R13 path-existence backend required")
    _require(callable(run_git), "V2R13 Git runner backend required")
    _require(isinstance(receipt, Mapping), "V2R13 materialization receipt must be object")
    _require(
        set(receipt) == MATERIALIZATION_RECEIPT_FIELDS,
        "V2R13 materialization receipt field-set drift",
    )
    _require(
        receipt.get("schema") == MATERIALIZATION_SCHEMA,
        "V2R13 materialization receipt schema drift",
    )
    _require(
        receipt.get("snapshot_id") == path_inputs.V2R13,
        "V2R13 materialization receipt snapshot drift",
    )
    _require(
        receipt.get("frozen_source_commit")
        == portable_checkout.FROZEN_WAR_COLLEGE_COMMIT,
        "V2R13 materialization source commit drift",
    )
    _require(
        receipt.get("frozen_source_tree")
        == portable_checkout.FROZEN_WAR_COLLEGE_TREE,
        "V2R13 materialization source tree drift",
    )
    _require(
        receipt.get("frozen_engine_commit")
        == portable_checkout.FROZEN_ENGINE_COMMIT,
        "V2R13 materialization engine commit drift",
    )
    for field in (
        "source_worktree_created",
        "engine_worktree_created",
        "source_worktree_detached",
        "engine_worktree_detached",
        "source_worktree_clean",
        "engine_worktree_clean",
        "canonical_source_checkout_unchanged",
        "canonical_engine_checkout_unchanged",
        "materialization_performed",
        "filesystem_mutation_performed",
        "git_worktree_admin_mutation_performed",
    ):
        _require(receipt.get(field) is True, f"V2R13 receipt lacks {field}")
    for field in (
        "canonical_checkout_working_tree_mutation_performed",
        "runtime_activation_performed",
        "runtime_execution_authorized",
        "model_load_performed",
        "model_inference_performed",
        "game_execution_performed",
        "training_performed",
        "weights_updated",
        "deployment_performed",
        "void_chain_mutation_performed",
        "wallet_or_funds_action_performed",
    ):
        _require(receipt.get(field) is False, f"V2R13 receipt crossed boundary: {field}")

    source_repository_root = _lexical_absolute_path(
        receipt.get("source_repository_root"),
        "source_repository_root",
    )
    engine_repository_root = _lexical_absolute_path(
        receipt.get("engine_repository_root"),
        "engine_repository_root",
    )
    source_destination = _lexical_absolute_path(
        receipt.get("frozen_source_root"),
        "frozen_source_root",
    )
    engine_destination = _lexical_absolute_path(
        receipt.get("exact_engine_root"),
        "exact_engine_root",
    )

    engine_removed = _remove_if_present(
        engine_repository_root,
        engine_destination,
        path_exists=path_exists,
        run_git=run_git,
        label="exact engine cleanup",
    )
    source_removed = _remove_if_present(
        source_repository_root,
        source_destination,
        path_exists=path_exists,
        run_git=run_git,
        label="frozen source cleanup",
    )

    return {
        "schema": CLEANUP_SCHEMA,
        "snapshot_id": path_inputs.V2R13,
        "frozen_source_root": source_destination,
        "exact_engine_root": engine_destination,
        "source_worktree_removed": source_removed,
        "engine_worktree_removed": engine_removed,
        "removed_worktree_count": int(source_removed) + int(engine_removed),
        "cleanup_performed": source_removed or engine_removed,
        "cleanup_idempotent": True,
        "runtime_activation_performed": False,
        "runtime_execution_authorized": False,
        "model_inference_performed": False,
        "game_execution_performed": False,
        "training_performed": False,
        "weights_updated": False,
        "deployment_performed": False,
        "void_chain_mutation_performed": False,
        "wallet_or_funds_action_performed": False,
    }


def authorize_runtime_execution(*args: Any, **kwargs: Any) -> None:
    raise RuntimeV2R13FrozenWorktreeMaterializerHold(
        "RUNTIME_EXECUTION_AUTHORIZATION_REQUIRED"
    )
