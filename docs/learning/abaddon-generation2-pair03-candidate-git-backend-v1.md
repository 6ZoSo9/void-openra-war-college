# Pair-03 candidate Git backend

The accepted first-baseline Git wrapper restricts worktree destinations to the
baseline arm. It must not be repointed by modifying its globals for a candidate
run. This backend supplies the existing materializer's two callback interfaces,
`run_git(repository_root, *args)` and `path_exists(path)`, for the candidate only.
It does not replace the materializer or add another execution/authorization model.

## Exact allowed operation set

Construction requires `CONFIRM_TOKEN` for worktree operations and performs no
host I/O. Import and construction do not confer game or model execution authority.
The only repository, destination and frozen-commit associations are:

- `/home/zoso/dev/openra-rl-war-college` to the pair-03 candidate `frozen-source`
  at `973802ef0a614e5afa782ff20e231e18966ae3e5`;
- its `OpenRA` repository to the pair-03 candidate `engine` at
  `1607a7a6501d42a47638393ecef8b22831064932`.

Both destinations are inside the fixed
`/home/zoso/dev/void-war-college-execution/v2r13-generation2/generation2/pair-03/candidate`
arm. Roots, destinations and commit spellings are exact, not prefix allowlists.
No caller-provided replacement roots or pins exist in the constructor.

Allowed reads are the materializer's exact toplevel, HEAD/tree, frozen-commit/tree,
cleanliness, detached-HEAD and worktree-registry queries. Only `worktree add
--detach` for the associated frozen commit and non-force `worktree remove` for
the associated destination can mutate Git state. Fetch, reset, canonical checkout,
clean, configuration queries/writes, pruning, force flags, branch/ref aliases,
other arms, traversal and alternate path spellings reject before subprocess use.

Paths are observed component-by-component without accepting symlink components.
The candidate parent must already exist; this adapter creates no arm directory.
One backend instance records each attempted add and the device/inode of each
successful creation. Only that instance's still-matching inode can be removed.
A failed/ambiguous add is not adopted for cleanup and cannot be retried by that
instance. Uncertain residue is preserved for explicit operator review. A newly
constructed instance cannot claim cleanup ownership of existing residue.

The existing materializer remains responsible for source/tree/cleanliness and
registry validation, before/after canonical checkout snapshots, receipt binding,
and preflighting both cleanup targets before removing either. Git's non-force
removal also refuses dirty worktrees. Git administration metadata necessarily
changes when adding/removing linked worktrees; canonical checkout content and
branch state are not intentionally modified by this adapter.

## Process boundary

Commands use `/usr/bin/git`, never a PATH-selected replacement or shell. The
child environment does not inherit caller Git overrides, loader, proxy or
credential settings. System/global Git config, replacement objects, lazy fetch,
prompts and optional locks are disabled; command-level settings disable hooks,
fsmonitor, recursive submodules, protocols and automatic maintenance.

Combined stdout/stderr retention is capped at 1 MiB, with at most one additional
64 KiB read chunk before rejection. A 30-second deadline bounds child/pipe waits
after process creation. Timeout/output overflow terminates the dedicated child
process group, waits up to two seconds for the child and closes pipe descriptors.
Malformed UTF-8 and transport errors refuse. Only the detached-HEAD query may
return 1; other nonzero results cannot be mistaken for success. There are no
subprocess retries or implicit filesystem rollback on uncertain failures.

These are not hostile-host, uninterruptible-kernel-I/O or absolute process-creation
deadline claims. The OS, installed Git, repository-local configuration and tracked
attributes remain trusted. Disabling hooks is not a sandbox against every possible
Git filter or malicious repository configuration. Directory checks are sequential
observations, not permanent exclusion against concurrent same-UID replacement.

## Verification and remaining composition

Fifty-seven focused tests execute locally with two real temporary Git repositories
and synthetic frozen commits. They cover a complete two-worktree callback sequence,
clean/detached state, ordinary cleanup, canonical branch/content preservation,
baseline evidence preservation, rejected commands/paths/refs, linked/existing
paths, foreign cleanup, dirty cleanup, ambiguous creation, repeated adds, ambient
Git overrides, disabled checkout hooks, both output streams, exit-code handling,
output/time/UTF-8 failures and descriptor cleanup. No Precision path is used.

Three additional complete-checkout tests invoke the actual unchanged materializer
and cleanup implementation for normal/idempotent cleanup, dirty-engine refusal
before removing either target, and rollback after an engine-add failure. Only
static authority/path validators and frozen identities are substituted for the
synthetic repositories. These tests do not claim production authorization; they
run normally in hosted CI and were not executed in the isolated local workspace.

The dedicated candidate invocation still must compose this backend with the
accepted single-use guard, the candidate preflight, a fresh candidate-specific
operator decision and the existing preload/readiness/revocation sequence. A new
backend instance is not durable replay protection: all invocations must consume
the same admitted persistent attempt slot. No CLI, runtime call, baseline retry,
training, deployment or funds operation is added here.
