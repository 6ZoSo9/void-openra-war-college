# OpenBW S1 merged-builder runtime qualification v1

This record closes the first post-merge runtime qualification of the OpenBW S1
compatibility builder merged as commit
`6ffee13a6b8b26ed70cbb55aed3df5e9d7d20c73`.

The qualification is deliberately split into two bounded stages. Both use the
merged production builder blob
`7f815991a4537c03a18d1f740b44d4999addd706` and the same pinned upstream
OpenBW/BWAPI/CascLib commits accepted by the source contract.

## Single-instance stage

The single-instance verifier used pinned `testmap1.scm`, opened the real S1
CASC storage with downloads disabled, loaded the neutral BWAPI module, observed
frames 120, 240 and 360, requested leave at frame 480 and received `onEnd` at
frame 481. The launcher returned zero.

The cache stayed exactly at 856,728,018 bytes during the run. Complete map
information and user input remained disabled. No model or training execution
occurred.

## Dual LOCAL_FD stage

The dual verifier used pinned `MapTest.scx`, two neutral BWAPI modules, a
preconnected AF_UNIX socketpair and OpenBW `LOCAL_FD` transport. Both clients
reached frames 120, 240 and 360.

Role A requested leave at frame 480 and ended at frame 481. Role B observed the
named `VOID-A` peer departure at frame 483, requested its own bounded leave on
that observation, and ended at frame 484. Both launchers returned zero.

The dual run proves:

- two-instance local synchronization;
- named peer-departure propagation;
- bounded peer-followup exit;
- bounded dual lifecycle completion; and
- zero cache growth with CASC download disabled.

## Test-only lobby adaptation

All 11 pinned BWAPI test maps contain only one raw open-human slot. The dual
qualification therefore applies one temporary source adaptation in the isolated
test checkout: exactly one computer-preferred lobby slot is promoted to
open-human under explicit pre/postcondition guards.

That adaptation is **not** present in the merged production source builder. The
qualification receipt and regression test both preserve this distinction. The
runtime proof therefore validates the merged CASC/VX4 builder while treating
the fixture-specific slot promotion as harness-only compatibility plumbing.

## Evidence binding

The machine-readable receipt is:

`config/war-college/openbw-s1-merged-builder-runtime-qualification-v1.json`

It binds the merged commit, builder blob, exact upstream pins, verifier SHA-256
values, map Git blobs, frame/lifecycle observations, zero-growth assertions and
runtime boundaries. Its `evidence_payload_sha256` is the SHA-256 of canonical
JSON after removing that digest field itself.

The associated test verifies the payload digest, builder Git-blob identity,
runtime invariants, zero-growth boundaries and absence of the test lobby
promotion from the production builder.

## Boundaries

This qualification does not execute the StarCraft retail binary, Battle.net,
models, training, policy promotion, deployment, VOID mutation or wallet/funds
actions. It does not mutate the checked-out War College source tree.

Future production work can now treat the merged OpenBW S1 builder as qualified
for both bounded single-instance and bounded two-instance local runtime use under
the exact accepted pins. Broader map coverage, persistent runtime packaging and
agent/model integration remain separate gates.
