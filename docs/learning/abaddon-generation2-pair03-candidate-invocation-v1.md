# Pair-03 candidate invocation

This module connects the candidate request, single-use attempt guard,
preserved-baseline preflight and restricted Git backend to the existing
`execute_v2r13_arm()` implementation. It is the operational composition, not
another request/receipt-only gate. Neither importing it nor publishing this
source authorizes or performs a real candidate run.

## Explicit operational interface

`execute_pair03_candidate()` takes an expected full main commit SHA, the expected
SHA-256 of this invocation source, and the dedicated candidate-once confirmation.
There is no default confirmation, generic authority boolean, old six-arm permit,
caller-provided evidence, callback, path override, alternative pair or retry flag.
The state-write, read-only preflight and Git-only confirmations do not satisfy
this invocation's confirmation. There is no CLI or import-time dispatch.

The confirmation represents an explicit decision by the trusted local operator;
it is not a password, secret, signature or cryptographic authentication. The
operator must first accept the exact source generation and separately authorize
the actual candidate operation. This change does not record that future decision
as already accepted, and leaves the historical request's authority flags intact.

## Operation sequence

The invocation first requires disabled bytecode writes, the exact designated
virtual-environment executable and its matching `sys.prefix`. Resolving a Python
symlink to the same binary as the system interpreter is not sufficient. It then
checks the invocation and direct dependency origins/bytes, expected current main,
tracked cleanliness, revocation and cached sudo authority.

The preflight preserves the baseline, verifies its comparison files, and checks
the existing host/runtime prerequisites. Its actual snapshot digest and narrow
non-authorizing result are checked rather than inheriting historical six-arm
authority. Baseline bytes are read again and must match that observation.

The candidate-only Git backend supplies the existing executor's worktree
callbacks. A closure rechecks the exact main/source state, baseline evidence and
revocation, and accepts only integer pair slot 3 and the candidate arm.

After the initial gates, the invocation creates or reopens the one fixed private
`pair03-candidate-claims-v1` directory under the isolated execution root, outside
all arm directories. It never removes or resets that directory. Any existing
result, including a dangling link, refuses before claiming another attempt. The
accepted #177 helper then exclusively creates and synchronizes its fixed marker.
A further authority check follows consumption. Any later failure leaves the slot
consumed; there is no automatic retry, even when no model decision occurred.

There is exactly one call to the existing bounded executor, always with pair 3,
arm `candidate`, the fixed genome and canonical roots. The inherited executor
checks the supplied authority closure before materialization and runtime start,
then runs the existing preload/readiness provider before its first model decision
and checks authority again after readiness. The new wrapper also checks the
candidate context before that provider can preload. It does not rebind the
baseline wrapper's globals or call its baseline execution entrypoint. Existing
executor cleanup and failure-preservation behavior remains in force.

On return, the invocation requires the candidate scope and exact policy binding,
completed readiness and cleanup, preserved authority boundaries, valid executor
receipt digest, and a candidate-local artifact directory. It does not interpret
a draw/unfinished result as a win or promote a policy. It rechecks the baseline
before exclusively writing the completion record into the claims directory.

The completion record is bounded to 1 MiB, synchronized, read back on the same
descriptor, and checked against the final named inode. Partial/uncertain records
are retained, never overwritten or resumed. A failed completion write can occur
after the game finished; its consumed attempt marker still forbids automatic
re-entry. The returned digest identifies the actual stored completion bytes.

## Source and runtime boundaries

The eight accepted request references and six additional dependency references
are verified against actual file bytes. The invocation file is bound by the
caller's expected SHA-256. Direct imported module origins are checked. These are
cooperative-host observations, not a full transitive import inventory, an atomic
snapshot or proof of immutable in-memory code custody. The Python import
environment, OS/Git, local repository configuration and same-UID namespace remain
trusted. The function is not a sandbox for a malicious local operator.

Deleting or rolling back the fixed claims directory, swapping namespaces after
observations, or storage misreporting synchronization remains outside the
underlying attempt guard's guarantee. No physical-power-loss guarantee is made.
The inherited preflight/model/executor command behavior remains; source and result
I/O limits are byte/call bounds, not whole-game or kernel-operation deadlines.

Only the existing candidate runtime may execute when this function is explicitly
called on the admitted host. Baseline/held-out execution, automatic retraining,
weight updates, policy promotion, deployment, VOID changes, wallet/signing or
funds movement are not dispatched. The result explicitly does not claim operator
authentication. No actual Precision or game operation occurred in source tests.

## Verification

The new file contains 73 tests: 69 focused cases and four complete-checkout cases.
Focused tests use real temporary baseline files, the unchanged attempt guard,
real private claims/result files and descriptor handling, with simulated host
preflight, main/source admission and executor dispatch. The direct file/origin
verifier and designated-venv checks also have standalone fixture tests. Scope,
revocation, altered receipts, prior results, uncertain writes and post-consumption
failures must refuse without an automatic second dispatch.

Three complete-checkout cases exercise the actual accepted executor and its
actual readiness hooks, using inert legacy/model/worktree/plan fixtures for
successful flow, readiness failure and post-readiness revocation. They check
cleanup and that no fixture decision occurs after a failed readiness boundary.
The fourth checks all dependency bytes and confirms the baseline module remains
baseline-scoped. These cases are not skipped in committed CI.

Local isolated Python execution cannot replace the complete repository, supported
Python 3.10/3.11/3.12 matrix, exact-head source review or a later explicitly
authorized Precision run. This integration branch carries the unchanged #178 and
#179 prerequisites for joint CI without modifying their separate branches.
