# Abaddon scout external launcher contract v1

## Purpose

This source-only contract records the exact inputs and remaining gates for a
future Abaddon scout experiment after the scout lifecycle source merged through
PR #181.

It is not a launcher, runtime permit, attempt guard, result verifier, or game
executor. It intentionally has no filesystem, process, network, model, engine,
Precision, wallet, chain, or funds capability.

## Current source binding

The proposal is bound to War College `main`
`9a151da589f93454d31a475b29297ea8a3d35442` and pins these Git blobs:

- scout runner binding: `9e4894b64f0820a53faf8226974d99687066679b`
- scout host bridge: `1fa8ea14c757e46658813dca035037f125e23880`
- scout missions: `12ca91f68f595919061dd6d5f927fb46428c9a58`
- goal/effect core: `0bd626f6733a77a4861d71e5dea093d0a899c878`
- frozen warm-start runner fixture: `132a5b2df3c3dbc82df7c0ebc6d457e5b77ffb51`
- frozen joint-host fixture: `6e751b855da1d9425c4fd2bd5a997ae1c742ae11`
- frozen Abaddon-controller fixture: `938afb496bfe704c5ff75adbf938473d9c431062`
- protocol fixture: `a20e85cf7d9f3b4c1523b1916569942d7b74e694`

The historical fixtures additionally retain their already reviewed SHA-256
identities for the warm-start runner, joint host, and controller.

## Fixed proposal

The canonical request SHA-256 is
`67582949d9cbb6815c59ba9c78e6ac40fc303080320b5d707ad2b9e64e9baf55`.

Matching those bytes does **not** grant execution authority.

The proposal fixes:

- one future scout experiment attempt;
- zero automatic retries;
- no reuse of the consumed pair-03 attempt;
- no reset of the consumed pair-03 attempt;
- no automatic training admission;
- no automatic policy promotion;
- no deployment, VOID mutation, wallet, or funds authority.

All authority fields remain false in this module.

## Source-binding review layer

The companion `abaddon_scout_external_launcher_contract_review_v1.py` pins this
contract at Git blob `1f7ee7057c27946f488afe26501482ea4f4fc53d` and pins the
canonical request digest above. Its regression test recomputes both identities
from the checkout.

That review layer still grants no execution authority. It deliberately reports
`repository_bytes_verified_by_this_module = false`: repository-byte
verification belongs to tests/review tooling, not to import-time host effects.

Its next gate is `SCOUT_FRESH_DURABLE_ATTEMPT_GUARD_REQUIRED`.

## Required next gates

A future implementation still must independently establish:

1. exact admitted source inventory;
3. a fresh experiment identity;
4. a fresh durable single-use attempt guard;
5. explicit non-reuse of the consumed pair-03 slot;
6. current operation authority immediately before effects;
7. fresh runtime readiness;
8. independent post-run runtime/service/container/source observations; and
9. result and trajectory binding to the admitted source inventory.

The existing scout binding cannot satisfy these gates merely by being
constructed or by returning successfully. Its own snapshots correctly record
that source identity is not verified by the binding.

## Fresh durable attempt guard

The companion `abaddon_scout_external_attempt_guard_v1.py` implements the next
bounded prerequisite without adding runtime authority.

It accepts only the canonical launcher request, the reviewed launcher-contract
Git blob, a lowercase scout experiment identity, the exact caller-admitted
private directory identity, and the explicit state-write confirmation token.

The guard then:

- duplicates the caller's directory descriptor without taking ownership of it;
- requires a private `0700` same-user directory;
- uses one fixed marker name with `O_CREAT|O_EXCL|O_NOFOLLOW|O_CLOEXEC`;
- writes a private `0600` marker with bounded partial-I/O loops;
- fsyncs the file and directory;
- reads the exact marker bytes back;
- rechecks the inode through both descriptor and directory lookup; and
- returns only a consumption receipt whose execution/training/promotion fields
  remain false.

Any existing marker—including empty, junk, symlink, hardlink, directory, valid,
or uncertain crash residue—HOLDs. The guard never deletes, renames, resets, or
reuses a marker. Changing the experiment name cannot reopen the fixed slot.

Regression coverage includes concurrent threads, independent processes, partial
read/write failures, short I/O, fsync failure, close failure, process loss before
the first write, process loss after file fsync, and a completed claim followed
by a fresh-process retry. No test starts a model or game.

Successful marker creation is **attempt consumption only**. It remains false for
scout execution authorization, execution performed, training authorization,
automatic retry, and automatic policy promotion.

## Reviewed attempt/result chain

The durable attempt guard is itself pinned by
`abaddon_scout_external_attempt_guard_review_v1.py`. That review binds the
launcher contract, launcher review, and attempt guard source identities and
advances only to `SCOUT_EXTERNAL_RESULT_BINDING_REQUIRED`.

The result layer is split deliberately:

- `abaddon_scout_external_result_binding_v1.py` constructs a canonical record
  containing a fresh scout experiment ID plus **declared** SHA-256 values for
  the attempt marker, trajectory, result payload, and independent post-run-state
  evidence.
- It also binds the twelve reviewed source identities spanning the original
  scout source/fixtures and the external launcher/attempt chain.
- Every verification and authority field remains false. A caller-supplied digest
  is explicitly not self-authenticating.
- `abaddon_scout_external_result_binding_review_v1.py` pins the exact result
  binding source and advances only to
  `SCOUT_EXTERNAL_RESULT_EVIDENCE_REVIEW_REQUIRED`.

No result declaration is accepted as evidence by either layer.

## Result boundary

`scout_result_requirements()` only describes the evidence a future result
binder must require. This module accepts no caller-supplied result as verified.

In particular:

- callback return is not shutdown proof;
- historical cleanup output is not shutdown proof;
- a trajectory must have an exact digest;
- the result record must have an exact digest;
- the result must identify the fresh attempt;
- post-run state must be independently observed; and
- result evidence cannot create training or promotion authority.

## Tests

The dedicated tests are source-only. They verify:

- canonical proposal bytes and pinned digest;
- all authority fields remain false;
- pair-03 reuse/reset remain false;
- every current source Git blob matches the checkout;
- historical fixture SHA-256 values match the checkout;
- mutated requests fail closed;
- public snapshots cannot mutate future contract values;
- execution and result-acceptance entrypoints always HOLD; and
- the module imports only `hashlib`, `json`, `typing`, and
  `__future__`, with no runtime/filesystem/network/local execution imports.

## Non-goals

This work does not execute a model or game, consume an attempt, create a runtime
permit, touch OpenBW, operate on Precision, change a scheduler, admit training
data, promote a policy, deploy anything, or move funds.

The next implementation step after source review is a separately reviewed,
durable fresh-attempt guard and external invocation boundary. Actual experiment
execution remains a separate explicit decision.
