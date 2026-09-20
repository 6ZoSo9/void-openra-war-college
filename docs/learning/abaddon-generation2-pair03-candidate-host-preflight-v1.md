# Pair-03 candidate preflight with a retained baseline

The existing first-baseline host validator requires all six V2R13 arm paths to
be absent. That is appropriate before the first arm, but cannot admit the next
candidate while the completed baseline remains at its accepted location. Deleting
or temporarily moving the baseline to pass that check would discard or disguise
required comparison evidence. This adapter removes neither evidence nor checks.

## Read-only operation

`collect_pair03_candidate_host_preflight(expected_main_head=..., confirm=...)`
requires an exact lowercase full main SHA and the dedicated read-only confirmation
constant. It accepts no caller-supplied snapshot, alternate root, baseline path,
hash override or execution switch. There is no CLI or import-time collection.

It calls the existing Precision host collector with the canonical source, engine
and isolated-workdir roots. The actual snapshot must report exactly the accepted
pair-03 baseline as present and the candidate and remaining four arms as absent.
A separate no-follow filesystem census rejects dangling symlinks, non-directories,
unexpected arms and missing baseline directories rather than relying on
`Path.exists()` alone.

The two comparison files are read only from the accepted retry-2 run:

`generation2/pair-03/baseline/runs/warmstart-apollyon-vs-abaddon-20260919T203512Z-feinter-s1990061685`

Their required SHA-256 identities are:

- trajectory: `27741699e08e367e66177d8bcd6bc2244d2c21b804fe250101b8ef0b6c7165b9`
- summary: `d37ab54fa8dbb2269a5ac61ca0880f7ae189188f0eea144031e484815bcdf7d6`

Both identities must also match the accepted candidate request. The reader opens
an absolute no-follow directory-descriptor chain and a read-only, nonblocking,
no-follow leaf. It requires a nonempty regular single-link file, enforces a
64 MiB trajectory / 1 MiB summary ceiling, hashes in at most 1 MiB chunks, checks
EOF and compares descriptor/name identity and modification metadata before
admitting the digest. At most `maximum // 1 MiB + 1024` content reads and one EOF
probe occur per file. All descriptors are closed; no create, write, unlink,
rename, permission change, or attempt consumption is implemented. Access-time
updates caused by ordinary reads are not claimed absent.

## Reusing the historical host checks honestly

After the actual baseline layout and bytes are observed, a private deep copy of
the snapshot changes exactly one field:

`isolated_workdir.authorized_arm_paths["3:baseline"].exists: true -> false`

That copy is a **structural compatibility projection**, not another observation
of the machine. The unchanged historical validator then checks all its original
host, source/main, engine, dependency, Docker, Ollama, authority and other-arm
predicates. Its successful return and exact projection digest are required. The
original host snapshot is never changed or passed off as an all-empty snapshot.

The returned candidate result includes the complete original snapshot and its
own digest, the baseline observations, and a separately named projection digest.
`legacy_structural_projection_is_host_observation=false` and
`legacy_runtime_authority_inherited=false` are explicit. The broad historical
runtime-authorization result is discarded, not copied into candidate permission.
A final filesystem arm census checks the expected layout again.

This is a narrow adapter for the existing preflight, not a second host-validator
implementation or a generic completed-arm exemption. The historical collector,
validator, baseline acceptance and request sources remain unchanged; a full-checkout
regression binds their four Git blob identities.

## Remaining execution boundary

Successful collection means the sampled candidate host conditions passed. It
does not authenticate an operator or host, certify executed-source custody,
authorize the candidate, consume #177's attempt marker, preload a model or start
a game. Every execution flag returned here remains false. The existing candidate
authorization gate is unchanged.

The dedicated candidate invocation still needs to compose this read-only operation
with an explicit candidate decision, the fixed persistent attempt guard, its own
candidate-only Git worktree allowlist, and the accepted preload/readiness/revocation
path. No Precision command or actual candidate launch is supplied by this change.

Host collection is sequential, not atomic, and remains dependent on the existing
collector's trusted OS/operator/tooling assumptions and command behavior. The new
byte/call ceilings are not kernel-I/O deadlines or physical-power-loss guarantees.
The no-follow checks do not promise permanent custody against hostile same-UID
mutation or coordinated rollback. No new live host observation was made during
source development or CI.

## Verification scope

The new test file has 61 cases. Forty-nine run in the isolated local workspace:
real temporary baseline reads, preservation, exact one-field projection,
non-inherited authority, layout/schema/type mismatches, symlinks/FIFOs/hardlinks,
missing/empty/oversized/wrong bytes, short-read behavior and bounds, I/O failure,
mutation/replacement detection, late layout change and descriptor cleanup.
Those tests substitute the host collector and legacy-validator response and use
explicitly synthetic baseline hashes; they do not exercise the full legacy import
graph or inspect Precision.

Eleven additional cases in the complete checkout execute the actual unchanged
legacy validator using its existing synthetic host fixture: its original
baseline-present refusal is reproduced, the candidate adapter passes a valid
fixture, and ten independent host/source/runtime drift cases still reject.
A twelfth case verifies the four unchanged dependency Git blobs. These twelve
cases are not skipped in the committed tests or normal CI. Local runs without
the complete checkout deselect them explicitly and report that limitation.

The existing full CI runs the complete test file on Python 3.10, 3.11 and 3.12,
then lint. Source acceptance, the dependent invocation and any operation-bound
Precision run remain separately unproven until their actual evidence exists.
