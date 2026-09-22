"""Pair-09-candidate-only Git callbacks for the V2R13 materializer.

Construction confirms only bounded worktree mechanics, never runtime authority.
Exactly two repository/commit/destination associations are accepted for the
pair-09 candidate arm. There is no CLI, discovery, fetch, canonical checkout,
force removal, arm-root deletion, or runtime call.

Only this backend instance's successfully created inode may be removed by it.
Same-instance retries after any attempted add are forbidden.
"""

from __future__ import annotations

import os
from pathlib import Path
import selectors
import signal
import stat
import subprocess
import time

CONFIRM_TOKEN = (
    "VOID_ABADDON_GENERATION2_V2R13_PREPARE_PAIR09_CANDIDATE_WORKTREES"
)
_SOURCE = "/home/zoso/dev/openra-rl-war-college"
_ARM = (
    "/home/zoso/dev/void-war-college-execution/v2r13-generation2/"
    "generation2/pair-09/candidate"
)
_BINDINGS = (
    (
        _SOURCE,
        _ARM + "/frozen-source",
        "973802ef0a614e5afa782ff20e231e18966ae3e5",
    ),
    (
        _SOURCE + "/OpenRA",
        _ARM + "/engine",
        "1607a7a6501d42a47638393ecef8b22831064932",
    ),
)

GIT_EXECUTABLE = "/usr/bin/git"
COMMAND_TIMEOUT_SECONDS = 30.0
MAX_OUTPUT_BYTES = 1024 * 1024

_READS = frozenset(
    {
        ("rev-parse", "--show-toplevel"),
        ("rev-parse", "HEAD"),
        ("rev-parse", "HEAD^{tree}"),
        ("status", "--porcelain", "--untracked-files=all"),
        ("symbolic-ref", "-q", "HEAD"),
    }
)

NEXT_GATE = "V2R13_PAIR09_CANDIDATE_GIT_BACKEND_SOURCE_BINDING_REVIEW_REQUIRED"
NEXT_CHANGE_CLASS = (
    "source_only_v2r13_pair09_candidate_git_backend_source_binding_review"
)


class V2R13Pair09CandidateGitHold(RuntimeError):
    pass


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise V2R13Pair09CandidateGitHold(code)


def _environment() -> dict[str, str]:
    return {
        "PATH": "/usr/bin:/bin",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_OPTIONAL_LOCKS": "0",
    }


def _capture(argv: list[str]) -> subprocess.CompletedProcess[str]:
    process = None
    finished = False
    try:
        process = subprocess.Popen(
            argv,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=_environment(),
            cwd="/",
            start_new_session=True,
            close_fds=True,
        )
        deadline = time.monotonic() + COMMAND_TIMEOUT_SECONDS
        output = {"stdout": bytearray(), "stderr": bytearray()}
        total = 0
        with selectors.DefaultSelector() as poller:
            for label in output:
                pipe = getattr(process, label)
                os.set_blocking(pipe.fileno(), False)
                poller.register(pipe, selectors.EVENT_READ, label)

            while poller.get_map():
                remaining = deadline - time.monotonic()
                _require(
                    remaining > 0,
                    "PAIR09_CANDIDATE_GIT_TIMEOUT",
                )
                for key, _ in poller.select(remaining):
                    chunk = os.read(key.fileobj.fileno(), 65536)
                    if not chunk:
                        poller.unregister(key.fileobj)
                        continue
                    total += len(chunk)
                    _require(
                        total <= MAX_OUTPUT_BYTES,
                        "PAIR09_CANDIDATE_GIT_OUTPUT_BOUND",
                    )
                    output[key.data].extend(chunk)

            remaining = deadline - time.monotonic()
            _require(
                remaining > 0,
                "PAIR09_CANDIDATE_GIT_TIMEOUT",
            )
            code = process.wait(timeout=remaining)
            finished = True

        return subprocess.CompletedProcess(
            argv,
            code,
            output["stdout"].decode("utf-8", "strict"),
            output["stderr"].decode("utf-8", "strict"),
        )
    except subprocess.TimeoutExpired:
        raise V2R13Pair09CandidateGitHold(
            "PAIR09_CANDIDATE_GIT_TIMEOUT"
        ) from None
    except (OSError, UnicodeError):
        raise V2R13Pair09CandidateGitHold(
            "PAIR09_CANDIDATE_GIT_TRANSPORT_HOLD"
        ) from None
    finally:
        if process is not None:
            if not finished:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            try:
                process.wait(timeout=2)
            finally:
                for pipe in (process.stdout, process.stderr):
                    if pipe is not None:
                        pipe.close()


def _directory(path: str) -> os.stat_result | None:
    current = Path("/")
    last = current.lstat()
    for part in Path(path).parts[1:]:
        current = current / part
        try:
            last = current.lstat()
        except FileNotFoundError:
            return None
        _require(
            stat.S_ISDIR(last.st_mode),
            "PAIR09_CANDIDATE_GIT_PATH_NOT_REAL_DIRECTORY",
        )
    return last


class Pair09CandidateGitBackend:
    def __init__(self, *, confirm: str):
        _require(
            type(confirm) is str and confirm == CONFIRM_TOKEN,
            "PAIR09_CANDIDATE_GIT_CONFIRMATION_REQUIRED",
        )
        _require(
            os.name == "posix",
            "PAIR09_CANDIDATE_GIT_PLATFORM_UNSUPPORTED",
        )
        self._bindings = _BINDINGS
        self._created: dict[str, tuple[int, int]] = {}
        self._attempted: set[str] = set()

    def _binding(self, path: str) -> tuple[str, str, str]:
        _require(
            type(path) is str,
            "PAIR09_CANDIDATE_GIT_PATH_NOT_ALLOWED",
        )
        for row in self._bindings:
            if path in row[:2]:
                return row
        raise V2R13Pair09CandidateGitHold(
            "PAIR09_CANDIDATE_GIT_PATH_NOT_ALLOWED"
        )

    def path_exists(self, path: str) -> bool:
        self._binding(path)
        try:
            return _directory(path) is not None
        except OSError:
            raise V2R13Pair09CandidateGitHold(
                "PAIR09_CANDIDATE_GIT_PATH_OBSERVATION_HOLD"
            ) from None

    def run_git(
        self,
        repository_root: str,
        *args: str,
    ) -> subprocess.CompletedProcess[str]:
        canonical, destination, commit = self._binding(repository_root)
        _require(
            len(args) <= 5 and all(type(arg) is str for arg in args),
            "PAIR09_CANDIDATE_GIT_COMMAND_NOT_ALLOWED",
        )

        extra_reads = {
            ("rev-parse", "--verify", commit + "^{commit}"),
            ("rev-parse", commit + "^{tree}"),
            ("worktree", "list", "--porcelain"),
        }
        adding = (
            repository_root == canonical
            and args
            == (
                "worktree",
                "add",
                "--detach",
                destination,
                commit,
            )
        )
        removing = (
            repository_root == canonical
            and args == ("worktree", "remove", destination)
        )
        readable = (
            args in _READS
            or (
                repository_root == canonical
                and args in extra_reads
            )
        )
        _require(
            adding or removing or readable,
            "PAIR09_CANDIDATE_GIT_COMMAND_NOT_ALLOWED",
        )

        try:
            _require(
                _directory(repository_root) is not None,
                "PAIR09_CANDIDATE_GIT_REPOSITORY_MISSING",
            )
            if adding:
                _require(
                    destination not in self._attempted,
                    "PAIR09_CANDIDATE_GIT_ADD_ALREADY_ATTEMPTED",
                )
                _require(
                    _directory(str(Path(destination).parent))
                    is not None,
                    "PAIR09_CANDIDATE_GIT_PARENT_MISSING",
                )
                _require(
                    _directory(destination) is None,
                    "PAIR09_CANDIDATE_GIT_DESTINATION_EXISTS",
                )
                self._attempted.add(destination)

            if removing:
                observed = _directory(destination)
                _require(
                    observed is not None
                    and destination in self._created
                    and self._created[destination]
                    == (observed.st_dev, observed.st_ino),
                    "PAIR09_CANDIDATE_GIT_CLEANUP_NOT_OWNED",
                )

            argv = [
                GIT_EXECUTABLE,
                "--no-replace-objects",
                "-c",
                "core.hooksPath=/dev/null",
                "-c",
                "core.fsmonitor=false",
                "-c",
                "core.attributesFile=/dev/null",
                "-c",
                "submodule.recurse=false",
                "-c",
                "protocol.allow=never",
                "-c",
                "gc.auto=0",
                "-c",
                "maintenance.auto=false",
                "-C",
                repository_root,
                *args,
            ]
            result = _capture(argv)
            allowed_codes = (
                (0, 1)
                if args == ("symbolic-ref", "-q", "HEAD")
                else (0,)
            )
            _require(
                result.returncode in allowed_codes,
                "PAIR09_CANDIDATE_GIT_COMMAND_FAILED",
            )

            if adding:
                created = _directory(destination)
                _require(
                    created is not None,
                    "PAIR09_CANDIDATE_GIT_CREATED_PATH_MISSING",
                )
                self._created[destination] = (
                    created.st_dev,
                    created.st_ino,
                )

            if removing:
                _require(
                    _directory(destination) is None,
                    "PAIR09_CANDIDATE_GIT_CLEANUP_INCOMPLETE",
                )
                del self._created[destination]

            return result
        except OSError:
            raise V2R13Pair09CandidateGitHold(
                "PAIR09_CANDIDATE_GIT_PATH_OBSERVATION_HOLD"
            ) from None


def pair09_candidate_git_backend_contract() -> dict[str, object]:
    return {
        "schema": (
            "void.abaddon.generation2."
            "v2r13-pair09-candidate-git-backend-contract.v1"
        ),
        "pair09_candidate_git_backend_implemented": True,
        "pair09_candidate_git_backend_reviewed": False,
        "pair_slot": 9,
        "arm": "candidate",
        "held_out": False,
        "binding_count": 2,
        "frozen_source_commit": _BINDINGS[0][2],
        "frozen_engine_commit": _BINDINGS[1][2],
        "fetch_implemented": False,
        "canonical_checkout_implemented": False,
        "force_remove_implemented": False,
        "reset_implemented": False,
        "clean_implemented": False,
        "config_implemented": False,
        "prune_implemented": False,
        "runtime_execution_authorized": False,
        "runtime_execution_performed": False,
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
    }
