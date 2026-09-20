# Scout mission host-feedback bridge (offline candidate)

## Status

The bridge implementation and its offline integration tests are complete. No
runtime hooks are installed and no new match is authorized by this source.
This update is local and unpublished. The earlier blocked GitHub source-write
attempt has not been retried through another route. There is no new PR, hosted
CI, Precision installation, source synchronization, or policy promotion.

All six repository files from the preceding scout-mission repair are unchanged.
This addition is four files: the bridge, its tests, this document, and a historical
host fixture. The existing goal/effect monitor remains byte-identical. The
frozen controller, original runner, old execution pins and used attempt marker
are not edited.

## Boundary established from original source

The retained joint host source is exactly:
`void-actual-apollyon-vs-abaddon-joint-sparring-batch-v1_2.py`, SHA-256
`c59faac3833ce4bffeb20e3d60625bcb3c63ecc520658660e19a8deefd2db615`.

Its `decision_to_commands` function returns validator acceptance, a reason and
constructed commands. `joint_advance` later copies both players' batches into
one request and calls `stub.JointAdvance`. Constructing a command is not sending
it. The warm-start runner, independently hash-verified at
`ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901`,
logs `command_count` before that joint call. That logged count is not by itself a
post-dispatch acknowledgement.

`ScoutMissionHostBridge` accepts the already trusted mission controller, original
validator and original joint function, protocol classes, scope, session, fixed
ticks per round and the existing caller-supplied authority check. It does not
load those components or authenticate an operator. No callback is installed on
an existing module, and no existing function/global is replaced.

## Prepare, submit, acknowledge

1. `prepare` checks the existing authority, calls the mission controller, then
   calls the original host validator once. It returns the legacy decision,
   actual validation result and copied protocol commands. The mission remains
   unissued and its proposal unresolved. The host's normal pending-building
   dictionary is preserved; its normal production bookkeeping is not bypassed.
2. The caller assembles the same two-player batch as the original host:
   mechanical placement plus each player's controller commands. The bridge
   verifies that Abaddon's suffix exactly matches the serialized commands
   admitted by the validator. Only building-placement/cancellation commands may
   precede that suffix, so a second unreviewed troop order cannot be hidden there.
   Apollyon's complete batch is preserved without being replanned or rewritten.
3. `dispatch_joint` rechecks authority immediately before calling the original
   joint function. There is one call, using the configured session and clock
   interval. It checks the reply's session, exact starting/ending ticks, distinct
   two-player observations and observation ticks.
4. Only after that successful return does it acknowledge the proposal using the
   validator's acceptance flag and submitted controller-command count. It records
   host submission in a completed shared-clock step, not per-command engine
   acceptance, successful movement or arrival. The mission controller alone
   observes later arrival from subsequent game observations.

An accepted `advance` contributes zero commands to the same shared-clock step.
Mechanical placement does not turn it into a scout order, and there is no extra
clock advancement for the scout controller. A rejected proposal contributes no
controller commands and does not create a mission.

A higher-priority contact command interrupts an existing mission only after joint
success. A rejected or failed contact submission cannot falsely cancel that
assignment. Existing mission progress, arrival and cooldown policy is unchanged.

All failure paths hold the bridge instance. A transport error or interruption
means world effects may have occurred: there is no acknowledgement, automatic
retry, reset, new fallback order or claim of no execution. The original pending
proposal and any host bookkeeping remain for review. Reusing the same successful
proposal cannot submit again. The next normal observation must start at the
previous successful joint end tick.

The old pure controller's constant `runtime_integration_active=false` is not
forwarded as a live status claim. The bridge explicitly records that the
controller does not observe integration status, alongside the bridge's own
possible-effects and call-count fields.

## Actual tests and evidence limits

Local Python 3.13.5 verification:

- New bridge file: **51 passed, zero deselected**.
- Bridge plus unchanged mission tests: **96 passed, zero deselected** (51 + 45).
- Original independent evidence-review test file: **29 passed, zero deselected**.

Counts refer to unique cases in their stated suites, not repeated executions.
The first 41 bridge cases passed on the first run; subsequent expansion brought
that file to 51 cases. Earlier and final logs are retained in the package.

Tests import the exact historical fixture but invoke only `decision_to_commands`,
its pure selector, and `joint_advance` with an inert in-process stub. No historical
main, loader, process, service, model, engine or real network stub is called. The
protocol objects are real dynamically constructed protobuf messages using the
Command/JointAdvance fields and enum values inspected in the repository schema.
They are a deliberately small test protocol, not the complete generated bridge
module or an engine compatibility certification.

Coverage includes non-issued prepared orders; exact commands and two-player
assembly; failed/interrupted transport; wrong session and clocks; missing or
duplicate player rows; rejected commands; no-op plus mechanical placement;
contact success/failure; production pending-state preservation; authority expiry;
malformed gate outputs; command bounds; duplicate submission; and acknowledgement
failure after a possible world step.

Four focused cases use exact saved observations: candidate rounds 10, 17 and 33,
and baseline round 33. The original validator has all inputs needed for those
scouting/contact paths. The exported compact observations omit full `production`
state, so no full-host 72-round replay is claimed. Missing required production
state causes a tested HOLD; it is never invented as an empty queue. Replies in
these cases are synthetic tick responses, not alternate world outcomes.

The 29 original evidence tests continue to reproduce the completed experiment
and its shared scouting defect. No claim of improved scouting, combat or winning
follows from the repaired proposals or the synthetic responses.

## Remaining work

Source publication, full-repository tests/lint and supported-version integration
review remain outstanding. This object is not wired into a live runner. A future
reviewed caller must preserve the actual host authority, original command gate,
shared-clock ordering, source identities and a separately admitted experiment.
The existing consumed pair-03 attempt is not reopened.

Callbacks, protocol classes, host session association and single-threaded use are
trusted inputs. The reply checks are exercised with fixtures; no new real engine
reply was collected. This is in-memory round sequencing, not cross-process
exactly-once dispatch, durable crash recovery or a substitute for the existing
one-shot execution guard.
