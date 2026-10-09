#!/usr/bin/env python3
"""Apply ONLY an exact, verified fast-forward of Precision's War College main.

Modes:
  --plan                Read-only verification; does not fetch or update.
  --apply-fast-forward  Repeat all checks, then Git merge --ff-only exact SHA.

No reset, force, checkout, fetch, GPU signal, service changes or game execution.
The one-use Pair-06 V3 attempt is not claimed or launched by this script.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import pwd
import re
import socket
import stat
import subprocess
import sys
from typing import Any

ROOT = Path('/home/zoso/dev/openra-rl-war-college')
HOST = 'zoso-Precision-Tower-7810'
REMOTE = 'void-private'
BASE_HEAD = '0ee0d6df2ef617bc4c49cc4c73205a2f75f5ad31'
BASE_TREE = '2dd40a6fcc537401315181728183720e094be445'
PIN_HEAD = 'e983220f85e35c024bcc0da8dec418bcd8342e03'
PIN_TREE = 'f44100ba7b2508412042cb6b8cbd3bbd63afd400'
ARM_ROOT = Path('/home/zoso/dev/void-war-college-execution/v8-generation2/generation2/pair-06/baseline')
CLAIMS = ARM_ROOT / 'claims-v1'
V3_RUNS = ARM_ROOT / 'runs-v9-strict-visible-contact-input-order-coherence-adapter-rejection-actionable-feedback-v3-v1'
V3_EVIDENCE_NAMES = (
    'pair06-v9-strict-visible-contact-input-order-coherence-adapter-rejection-actionable-feedback-v3-baseline-game-attempt-v1.json',
    'pair06-v9-strict-visible-contact-input-order-coherence-adapter-rejection-actionable-feedback-v3-baseline-game-result-v1.json',
    'pair06-v9-strict-visible-contact-input-order-coherence-adapter-rejection-actionable-feedback-v3-baseline-game-closeout-v1.json',
)
GIT = '/usr/bin/git'
ENV = {
    'PATH': '/usr/bin:/bin',
    'HOME': '/home/zoso',
    'LC_ALL': 'C',
    'LANG': 'C',
    'GIT_CONFIG_NOSYSTEM': '1',
    'GIT_CONFIG_GLOBAL': '/dev/null',
    'GIT_NO_REPLACE_OBJECTS': '1',
    'GIT_NO_LAZY_FETCH': '1',
    'GIT_TERMINAL_PROMPT': '0',
    'GIT_OPTIONAL_LOCKS': '0',
    'GIT_SSH_COMMAND': (
        '/usr/bin/ssh -o BatchMode=yes -o StrictHostKeyChecking=yes '
        '-o ConnectTimeout=8 -o ConnectionAttempts=1'
    ),
}


class Hold(RuntimeError):
    """A fail-closed source-alignment safety hold."""


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise Hold(reason)


def run(argv: list[str], timeout: int = 45, *, mutation: bool = False,
        allow_false: bool = False) -> tuple[int, str]:
    env = dict(ENV)
    if mutation:
        env['GIT_OPTIONAL_LOCKS'] = '1'
    try:
        proc = subprocess.run(
            argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, check=False, timeout=timeout,
            env=env, cwd='/', text=True, encoding='utf-8', errors='replace',
        )
    except (OSError, ValueError, subprocess.TimeoutExpired) as e:
        raise Hold('COMMAND_UNAVAILABLE:' + Path(argv[0]).name + ':' + type(e).__name__) from None
    if proc.returncode and not allow_false:
        # Never print command stderr, which can include credential-bearing URLs.
        raise Hold('COMMAND_FAILED:' + Path(argv[0]).name + ':exit_' + str(proc.returncode))
    return proc.returncode, proc.stdout.strip()


def git(*args: str, timeout: int = 45) -> str:
    return run([GIT, '-C', str(ROOT), *args], timeout=timeout)[1]


def official_remote_url(url: str) -> bool:
    return re.fullmatch(
        r'(?:git@github\.com:|ssh://git@github\.com/)'
        r'6ZoSo9/void-openra-war-college(?:\.git)?/?',
        url.strip(), flags=re.IGNORECASE,
    ) is not None


def verify_dir_if_present(path: Path) -> bool:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return False
    require(stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode),
            'EVIDENCE_DIRECTORY_NOT_REAL:' + path.name)
    return True


def v3_unconsumed() -> None:
    if verify_dir_if_present(CLAIMS):
        require(all(not (CLAIMS / n).exists() and not (CLAIMS / n).is_symlink()
                    for n in V3_EVIDENCE_NAMES), 'V3_ATTEMPT_EVIDENCE_ALREADY_PRESENT')
    if verify_dir_if_present(V3_RUNS):
        require(not any(V3_RUNS.iterdir()), 'V3_RUN_NAMESPACE_NOT_EMPTY')


def local_identity(out: dict[str, Any]) -> str:
    require(os.geteuid() != 0 and pwd.getpwuid(os.geteuid()).pw_name == 'zoso',
            'USER_NOT_ZOSO')
    require(socket.gethostname().split('.')[0] == HOST, 'HOST_IDENTITY_DRIFT')
    require(ROOT.is_dir() and not ROOT.is_symlink() and ROOT.resolve() == ROOT,
            'SOURCE_ROOT_NOT_REAL_DIRECTORY')
    require(git('rev-parse', '--show-toplevel') == str(ROOT), 'SOURCE_REPO_IDENTITY_DRIFT')
    require(git('symbolic-ref', '-q', 'HEAD') == 'refs/heads/main', 'NOT_ON_MAIN')
    head, tree = git('rev-parse', 'HEAD'), git('rev-parse', 'HEAD^{tree}')
    out['observed_head_before'] = head
    out['observed_tree_before'] = tree
    if head == BASE_HEAD:
        require(tree == BASE_TREE, 'BASE_TREE_DRIFT')
        out['alignment_state'] = 'BASELINE_BEHIND_PIN'
    elif head == PIN_HEAD:
        require(tree == PIN_TREE, 'PIN_TREE_DRIFT')
        out['alignment_state'] = 'ALREADY_PINNED'
    else:
        raise Hold('UNEXPECTED_LOCAL_HEAD_NO_RESET_OR_REBASE_ALLOWED')
    require(git('status', '--porcelain', '--untracked-files=no') == '',
            'TRACKED_WORKTREE_NOT_CLEAN')
    out['tracked_worktree_clean'] = True
    require(official_remote_url(git('remote', 'get-url', REMOTE)),
            'VOID_PRIVATE_REMOTE_NOT_OFFICIAL')
    out['remote_identity'] = 'GREEN'
    v3_unconsumed()
    out['fresh_v3_attempt_namespace'] = 'GREEN'
    return head


def verify_target_and_remote(out: dict[str, Any], head: str) -> None:
    # Keep the alignment bound to the exact fetched Git object, not a branch name.
    require(git('rev-parse', '--verify', PIN_HEAD + '^{commit}') == PIN_HEAD,
            'PIN_COMMIT_NOT_FETCHED')
    require(git('rev-parse', '--verify', PIN_HEAD + '^{tree}') == PIN_TREE,
            'PIN_TREE_NOT_PRESENT')
    if head == BASE_HEAD:
        require(git('rev-parse', '--verify', 'FETCH_HEAD^{commit}') == PIN_HEAD,
                'FETCH_HEAD_CHANGED_SINCE_GUARDED_STAGE')
        require(git('rev-parse', '--verify', 'FETCH_HEAD^{tree}') == PIN_TREE,
                'FETCH_HEAD_TREE_DRIFT')
        code, _ = run([GIT, '-C', str(ROOT), 'merge-base', '--is-ancestor',
                       BASE_HEAD, PIN_HEAD], allow_false=True)
        require(code == 0, 'FAST_FORWARD_ANCESTRY_NOT_PROVEN')
        out['fast_forward_ancestry_proven'] = True
        out['commits_to_advance'] = int(git('rev-list', '--count', BASE_HEAD + '..' + PIN_HEAD))
        require(out['commits_to_advance'] == 53, 'UNEXPECTED_COMMIT_COUNT_DRIFT')
    # One final independent, read-only check of current official main; no fetch.
    live = git('ls-remote', '--heads', REMOTE, 'main', timeout=45)
    match = re.fullmatch(r'([0-9a-f]{40})\s+refs/heads/main', live)
    require(match is not None, 'REMOTE_MAIN_RESPONSE_SHAPE_DRIFT')
    require(match.group(1) == PIN_HEAD, 'OFFICIAL_REMOTE_MAIN_CHANGED')
    out['official_live_main'] = 'GREEN_EXACT_PIN'
    out['pinned_commit'] = PIN_HEAD
    out['pinned_tree'] = PIN_TREE


def fast_forward(out: dict[str, Any]) -> None:
    # A normal fast-forward merge is the ONLY permitted checkout mutation.
    # Do not perform a hard reset, checkout, pull, fetch, force, or branch switch.
    command = [GIT,
               '-c', 'core.hooksPath=/dev/null',
               '-c', 'core.fsmonitor=false',
               '-c', 'gc.auto=0',
               '-c', 'maintenance.auto=false',
               '-c', 'submodule.recurse=false',
               '-C', str(ROOT),
               'merge', '--ff-only', '--no-stat', '--no-edit', PIN_HEAD]
    out['fast_forward_attempted'] = True
    try:
        run(command, timeout=180, mutation=True)
    except Hold:
        # No automatic repair, reset, or second merge. Distinguish an earlier
        # rejection from any partial checkout update without modifying state.
        out['mutation_result'] = 'FAILED_NO_AUTOMATIC_RECOVERY'
        out['manual_checkout_census_required'] = True
        try:
            observed = git('rev-parse', 'HEAD')
            out['head_after_failed_merge'] = observed
            if observed == PIN_HEAD:
                out['branch_advanced'] = True
                out['checkout_changed'] = True
        except Hold:
            out['head_after_failed_merge'] = 'UNAVAILABLE'
        raise
    out['branch_advanced'] = True
    out['checkout_changed'] = True
    require(git('symbolic-ref', '-q', 'HEAD') == 'refs/heads/main',
            'POST_FAST_FORWARD_BRANCH_DRIFT')
    require(git('rev-parse', 'HEAD') == PIN_HEAD,
            'POST_FAST_FORWARD_HEAD_DRIFT')
    require(git('rev-parse', 'HEAD^{tree}') == PIN_TREE,
            'POST_FAST_FORWARD_TREE_DRIFT')
    require(git('status', '--porcelain', '--untracked-files=no') == '',
            'POST_FAST_FORWARD_TRACKED_DIRTY')
    v3_unconsumed()
    out['post_alignment_verification'] = 'GREEN'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    options = parser.add_mutually_exclusive_group(required=True)
    options.add_argument('--plan', action='store_true')
    options.add_argument('--apply-fast-forward', action='store_true')
    args = parser.parse_args()
    mode = '--apply-fast-forward' if args.apply_fast_forward else '--plan'
    out: dict[str, Any] = {
        'schema': 'void.pair06-v9-v3-precision-pinned-main-ff.v1',
        'mode': mode,
        'host': HOST,
        'repository': str(ROOT),
        'expected_baseline_head': BASE_HEAD,
        'expected_pinned_main': PIN_HEAD,
        'expected_pinned_tree': PIN_TREE,
        'git_fetch': False, 'git_reset': False,
        'git_force': False, 'branch_advanced': False,
        'checkout_changed': False,
        'attempt_created': False, 'game_executed': False,
        'automatic_retry': False, 'gpu_process_signaled': False,
        'gpu_service_mutated': False,
        'gpu_admission': 'NOT_CHECKED_STILL_BLOCKED_UNTIL_SEPARATE_PREFLIGHT',
    }
    try:
        head = local_identity(out)
        verify_target_and_remote(out, head)
        if head == PIN_HEAD:
            out['status'] = 'ALREADY_PINNED_NO_CHANGES'
        elif args.plan:
            out['status'] = 'FAST_FORWARD_PLAN_GREEN'
        else:
            # Revalidate local identity immediately before source mutation.
            require(local_identity(out) == BASE_HEAD,
                    'MAIN_MOVED_BEFORE_FAST_FORWARD')
            fast_forward(out)
            out['status'] = 'FAST_FORWARD_APPLIED_GREEN'
    except Hold as err:
        out['status'] = 'HOLD'
        out['hold_reason'] = str(err)
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as err:
        out['status'] = 'HOLD'
        out['hold_reason'] = 'UNEXPECTED_VERIFICATION_FAILURE:' + type(err).__name__
    print('VOID_PAIR06_V9_V3_GUARDED_FAST_FORWARD_V1')
    print(json.dumps(out, sort_keys=True, indent=2))
    print('NO_FETCH_NO_RESET_NO_GPU_SIGNAL_NO_SERVICE_MUTATION_NO_GAME')
    return 1 if out['status'] == 'HOLD' else 0


if __name__ == '__main__':
    sys.exit(main())
