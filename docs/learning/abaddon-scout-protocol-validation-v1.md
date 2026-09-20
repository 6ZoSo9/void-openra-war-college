# Scout repair V5 — complete-schema and serialized-message validation

## Outcome

V5 closes the handwritten partial-protocol test gap. All four unpublished runtime
modules are byte-identical to V4: the mission controller, reused goal/effect core,
host bridge and runner binding. No new runtime mechanism or authority is added.
The previous 184 repair cases pass using messages derived from the complete
compiler-produced schema. Twenty-six new wire/schema cases also pass: 210 total,
zero deselections. Publication remains unresolved; no source write was retried.

## Exact protocol basis and compiler

The complete `proto/rl_bridge.proto` was fetched using the connected repository at
`ea218d29cf6ae55058754379159d318cd1be71aa`, then reproduced locally and checked against
Git blob `a20e85cf7d9f3b4c1523b1916569942d7b74e694`. Its 10,331 bytes have SHA-256
`9a48ca90bd525b7fd5502e7426cd8c1bb96b1308c2b18904d4d7af023699eae3`.
It is added only as a historical test fixture, not as a change to the canonical
repository protocol or a substitute runtime bridge.

An existing local protoc binary (libprotoc 3.13.0, distributed with installed
PyTorch) compiled that exact file to a FileDescriptorSet. The descriptor-set
SHA-256 is `a519a53e29d8ed158256b67938e4227ae09423c40757f67d6cee8631655690b4`.
The tests create dynamic protobuf classes from this complete compiler output.
They no longer reconstruct selected fields or enum values by hand.

The descriptor contains all 20 messages, 23 ActionType values, one service and
six RPC signatures. Tests include the streaming flags on GameSession, the unary
FastAdvance signature, the C# namespace option, and previously omitted observation,
production, military and building fields. Actual protobuf integer ranges, unknown
field retention and serialization are exercised.

The test helper normally uses the repository's grpcio-tools dependency. This local
lab lacks grpcio-tools, so it used the explicit absolute SCOUT_TEST_PROTOC override.
There is no silent partial-schema fallback and no automatic package installation.
The compiler is not distributed in this package.

Reference: Protocol Buffers documentation describes `protoc --descriptor_set_out`
as producing a FileDescriptorSet: https://protobuf.dev/programming-guides/techniques/
The distinction from generating gRPC client/server bindings is described at
https://grpc.io/docs/languages/python/basics/ . No generated gRPC client, server,
HTTP/2 transport or OpenRA engine was executed by these tests.

## Serialized joint-step tests

A new in-process test boundary serializes requests using the compiler-derived
request class, decodes them before the synthetic host receives them, then encodes
and decodes replies using the service's declared response class. It opens no socket.
The existing original host command gate and joint-step function are still used.

Tests verify that a mission is not acknowledged before the matching decoded reply,
that malformed reply bytes after a possible step cannot acknowledge or retry the
proposal, and that valid protobuf with wrong sessions, ticks or player sets still
fails the existing checks. Unknown bytes added to an already prepared scout
command are rejected before transport, rather than being silently discarded.

The entire historical main also runs for 1, 3 and 36 controller rounds with
serialized CreateSession, GetState, JointAdvance and DestroySession messages.
These are the existing synthetic world/service/model fixtures, not new games.
The test-world startup continues to update its existing synthetic state object;
only its protocol stub is wrapped. No runtime source change was needed.

The old cleanup snapshots still state `actual_runtime_state_verified=false`.
Protocol correctness does not turn a returned cleanup callback into proof of
service dormancy, container removal, scout arrival or improved gameplay.

## Actual verification

Python 3.13.5 / pytest 9.0.2 / protobuf 6.33.6:

| Suite | Passing cases | Deselected |
| --- | ---: | ---: |
| Existing repair cases, now using complete schema | 184 | 0 |
| New schema/wire cases | 26 | 0 |
| Combined repair package | 210 | 0 |
| Source exporter, independent real temporary Git tests | 20 | 0 |
| Unchanged original pair-03 evidence reviewer | 29 | 0 |

The unchanged evidence archive still hashes to
`f5f0a1229e278aef770806a625c32aa190ecb22ad97623aa62edd6c5a7333b00`.
Clean package extraction repeats the repair and exporter cases; repeated runs are
not extra unique tests. Python-3.10 grammar parsing and in-memory compilation pass;
this is not execution on Python 3.10/3.11/3.12.

Initial new wire tests had 207 passes / 3 failures because the test replaced the
synthetic world's state owner with a transport proxy and checked a nonexistent
`restored` snapshot key. Wrapping only the protocol stub and using the documented
`callbacks_installed` key corrected the harness. No production code or original
assertion was relaxed. Failed and passing logs are included.

The exporter's initial tests exposed an incorrect assumption that ordinary Git
ZIP entries always contain Unix mode bits. Actual Git writes DOS-default metadata
for regular non-executable entries; the check now explicitly admits that form
while still checking every file's committed Git blob and preserving Unix metadata
for symlinks/executables. Its uninitialized-submodule fixture was also corrected.
A subsequent corruption-test harness preserved Git's original ZIP metadata so the
intended content-hash rejection is actually reached. These failed logs are retained.

## Full-repository validation blocker and source-only handoff

The read-only full-source download failed DNS resolution for codeload.github.com.
Connected reads can inspect individual files but the full source archive has not
been obtained in this container. Full-repository tests, Ruff, the supported Python
runtime matrix and hosted CI remain unrun. No claim is made that obtaining an
archive will by itself supply missing Python dependencies or Git-history evidence.

`war_college_accepted_source_export_precision_v1.py` exports the already accepted
commit from Precision, not the unpublished scout candidate. It requires the exact
clean main head/tree, reads the committed file inventory, runs local `git archive`,
and creates one new 0600 ZIP in Downloads. It verifies the archive's commit comment,
member set, CRCs, each file's length and Git blob, source preservation and final
output identity. Missing export-ignored files or changed export-substituted bytes
are a HOLD, not silently accepted as a complete source snapshot.

The export excludes untracked/ignored working files, .git metadata/history,
and engine-submodule contents. Symlink blobs can be archived as data but are not
followed or extracted. Executable source is archived, not executed. It never reads
both completed game directories or the attempt marker. It does not fetch, switch,
install, apply a patch, publish, run tests, import repository code, contact a model,
invoke sudo/Docker/systemd, reset a slot, or start another game. Existing output
is not overwritten; a partial/uncertain output is preserved after failure.

Expected output is
`~/Downloads/war_college_accepted_source_ea218d29_20260920.zip`.
The user controls uploading it. The exporter has passed 20 local temporary-repository
cases and correctly refused this non-Precision host; it has not run on Precision.
It addresses the missing full-source input only, not the separate blocked source
publication. No alternate publication route is supplied.

## Package scope and preserved boundaries

Fourteen of V4's sixteen repository files are unchanged. Two test fixture providers
are updated; four files are added (complete proto fixture, compiler helper, wire
tests and this report). All four runtime modules and all three historical executable
source fixtures remain byte-identical. The handoff and its tests are separate from
the proposed repository overlay.

No source commit, branch, PR, hosted run, Precision source sync/installation,
new game/model execution, baseline retry, training, promotion, funds action,
scheduler change or #153 change occurred. Both completed runs and the consumed
pair-03 marker/result stay unchanged. Live experiment approval and independent
post-run checks remain separate from offline schema validation.
