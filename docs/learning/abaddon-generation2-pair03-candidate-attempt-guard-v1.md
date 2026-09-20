# Pair-03 candidate single-use attempt guard

The accepted request specifies one candidate attempt and no automatic retry.
This change implements its missing create-only consumption prerequisite, not
another authorization packet and not the candidate invocation itself.

## Implemented boundary

`consume_candidate_attempt()` receives a borrowed directory descriptor, its
independently admitted `(device, inode)` identity, the exact #176 request bytes,
the expected invocation-source SHA-256 and a confirmation for this state write.
The directory must be an existing, current-user-owned private 0700 directory.
The function duplicates the descriptor; it never closes the caller's copy.

After input and directory validation and a pre-creation directory sync, it
creates exactly `pair-03-candidate-attempt-v1.json` with exclusive, no-follow
creation. The filename is independent of the source digest: changing a digest
cannot select a fresh slot. It sets only that new inode to 0600, completes bounded
writes, syncs the file and parent directory, reads back the same descriptor and
checks that the final name still identifies the same unchanged single-link inode.
All owned descriptors close before a successful result reaches the caller.

The record is at most 2 KiB. At most 64 write calls and 64 content-read calls plus
one EOF probe occur. These are operation/byte bounds, not kernel I/O deadlines.
Any existing marker is a terminal HOLD, including an empty/torn file, an exact
previous record, a directory, FIFO, hard link or dangling symlink. Existing marker
contents are never opened, parsed, overwritten, deleted, resumed or accepted as
permission. Failures after creation preserve the marker and stop before success.
A pre-creation failure performs no consumption; an ambiguous create error reports
`marker_may_exist=true`. A close failure cannot turn into success or mask the
original failure. Close is not retried against a potentially reused descriptor.

## Integration that still must be completed

There is no CLI and no game/runtime callback. No existing executor, preflight,
authorization request, baseline result, failed-run archive, or designated-host
controller-evidence admission store is changed. The latter stores signed-producer
attempt/session and joint-evidence identities; it is not repurposed as launch
permission or expanded to invent a producer identity for this candidate.

The future dedicated candidate invocation must admit ONE fixed persistent claims
directory, outside the baseline/candidate arm materialization paths, and enforce
operator authorization, exact invocation/source/baseline identities, preflight
and revocation before consumption. A failure after consumption never automatically
reopens the slot. Preload, fresh readiness, and the second live revocation check
must still run at their reviewed positions before model decisions. The guard does
not implement or independently attest any of those surrounding host gates.

The confirmation string authorizes only an explicit local state write. The result
and marker both retain `candidate_execution_authorized=false`,
`candidate_execution_performed=false` and `reusable_execution_permit=false`.
Neither a successful call nor a matching digest is operator authentication,
source-custody proof or a transferable execution permit.

## Trust and durability limits

This is a cooperative local-filesystem boundary. Every caller must use the same
admitted persistent directory. Namespace deletion/replacement by a hostile same-UID
process, a different directory, coordinated rollback, arbitrary remote filesystem
semantics and storage that lies about successful fsync are outside the claim.
The final identity comparison is an observation, not permanent writer exclusion.
Process-exit tests are not physical power-loss or designated-Precision evidence.
No production directory is created, opened or consumed by source inspection or CI.

## Verification

The focused pytest file has 50 cases using real temporary files and inert fault
injection: exact private marker/descriptor preservation; invalid inputs and
identities; every existing entry type; source-digest changes; partial writes and
reads; all three sync-failure positions; final-name replacement; close failure;
eight-thread contention; four separate-process contenders; and fresh-interpreter
refusal after a crash before writing, after file sync, or after completed
consumption. The accepted #176 request-source hash is checked; its tests remain unchanged.

The normal repository CI discovers these tests on Python 3.10, 3.11 and 3.12.
A local Python 3.13 run is not that supported-version matrix. Exact-head hosted
checks, source review, dedicated invocation wiring and a separately authorized
Precision run remain required before claiming actual candidate execution.
