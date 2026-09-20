# Scout-mission runner binding — offline V3

## Outcome

The scout repair now has an explicit callback binding for the historical warm-start
runner's existing controller loop. It is not published, installed on Precision,
or part of an approved new game. The binding does not launch a runner. Its caller
must already possess the reviewed source modules, operation-time authority,
source/host/runtime checks, and a separate durable attempt guard for a NEW
experiment. Do not reuse the completed pair-03 slot or its launcher.

This update modifies the unpublished `abaddon_scout_host_bridge_v1.py` and adds
`abaddon_scout_runner_binding_v1.py`, its tests, this document, and an exact
historical warm-start-runner test fixture. Nine of the ten V2 repository files
are unchanged, including the mission controller and goal/effect core. The old
V1/V2 documents remain historical reports of their corresponding stages.
No accepted repository or Precision source file is changed by this package.

## Concrete integration gap closed

The real runner calls Abaddon `decide`, then `decision_to_commands`, writes a
`joint_decision` record, submits both player batches with `joint_advance`, obtains
the end state, and writes `joint_result`. V2's bridge combined the first two
operations in `prepare`, so directly substituting it for the controller would
not preserve the runner's split call sequence.

The bridge now exposes `propose` and `validate_proposal`. `prepare` remains a
compatibility convenience that calls each once. The proposal retains a copy of
the full observation; the original command gate still runs only once against
that retained state and the caller's actual pending-building dictionary.
Neither stage acknowledges dispatch. The existing joint-success acknowledgement
and its tests are preserved.

## Opt-in callback wiring

`ScoutMissionRunnerBinding` accepts an already loaded runner, expected doctrine,
seed, round count, fixed ticks per round, world revision, mission policy, and the
caller's existing authority callback. Construction has no installation or world
side effect. An explicit `install()` replaces two callbacks on that in-memory
runner, and three on the one base object its unchanged loader returns. It never
rewrites a source file or installs itself globally.

The loader is still the caller's original. A proxy replaces only the Abaddon
constructor on a separate module object; the original controller module/class
is not patched. Other modules, including Apollyon's runtime helper, are returned
unchanged. An already policy-wrapped controller is rejected rather than silently
combining two experimental treatments.

The runner constructs its controller before choosing a run ID. The proxy retains
the expected constructor arguments; the real mission controller/bridge is created
only after the warm-start header, session and controller header are available.
The callback checks the expected seed, doctrine, round/tick bounds and historical
controller-identity field. This is an agreement with trusted supplied modules,
NOT independent byte verification or operator authentication.

During controller rounds:

1. `decide` proposes one repair decision on the full current Abaddon observation.
2. The runner's subsequent gate call must echo the exact action, arguments, state
   and protocol object. The bridge invokes the original validator once.
3. The decision log must match the prepared decision, gate acceptance, reason,
   command count, compact observation, run ID, round and starting tick. The
   appended scout metadata explicitly says dispatch has not been observed.
4. Only after that log succeeds may the original joint callback run. The bridge
   retains its exact command-byte, session, tick and two-player reply checks.
5. A successful reply acknowledges the mission. The following result log includes
   that submission feedback, not a claim of engine acceptance or arrival. An
   additional decision cannot overtake the result log.

Warm-start joint calls pass through the original function; they do not create
scout missions. Both the warm-start and controller paths require the caller's
current operation permission. Apollyon's typed tool selection, mechanical
placement, production bookkeeping, shared clock, state query and outer cleanup
remain their original implementations.

The binding adds a distinct `abaddon_scout_missions_v1` evidence field without
rewriting Apollyon's choice or the original Abaddon decision/gate fields. New
metadata marks training use unapproved and automatic promotion false. The original
runner's summary writer is unchanged: a future admitted experiment must bind the
new repair's source identity and trajectory metadata in its own experiment/result
record. This module does not claim that an old summary or #180 receipt format
already accepts the new treatment. Its incompatibility with the old candidate
wrapper is intentional.

## Error and restoration behavior

A failed decision log stops before joint submission. A failed result log occurs
after a potentially completed world step and cannot undo or reset the issued
mission. A failing external end-state query leaves the binding waiting for its
result log; another decision is rejected. Failed/mismatched/interrupted joint
calls retain the bridge's pending proposal and possible-effects state, without
acknowledgement or retry.

All wrapped callback failures hold this binding. `restore()` only restores
callbacks still identical to its own replacements. A competing replacement
causes a HOLD rather than an overwrite. Restored controller proxies cannot issue
new proposals. The same binding cannot be installed again. Restoration does not
reset missions, authorizations, disk markers, a runtime, or an uncertain world
step. In-memory sequencing is not cross-process exactly-once execution.

## Actual local verification

The new runner test file has **47 cases**. The combined local package has
**143 cases: 47 runner + 51 existing bridge + 45 unchanged mission cases**, all
passing with zero deselections. The independent original pair-03 reviewer also
has **29 passing cases**, run separately on the unchanged uploaded evidence.
These are not additive counts of repeated clean-extraction executions.

Tests hash-check the historical warm-start runner against
`ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901`, then extract
its unique controller `for round_no` loop using AST. Every statement in that loop
is retained unchanged. Its actual typed Apollyon tool gate, pending-building
reconciliation, original command validator and original joint function execute.
The startup/main, real loaders, services, model endpoint, session creation and
outer cleanup are NOT executed. The test loop's initial state is explicitly
synthetic, not a padded or counterfactually simulated historical observation.

The model callback is scripted and the transport is an in-process fake. Command
and joint-response objects use the prior deliberately partial protobuf fixture;
`StateRequest` and returned state-query data are simple test objects. Observation
conversion is a fixture returning explicitly synthetic full states. Thus this
is actual loop-statement integration coverage, NOT full runner-main, full generated
protocol, live engine, performance, or new experiment acceptance.

A 36-round synthetic case verifies exactly 36 controller joint calls, no extra
clock step, and no invented arrival in stationary sampled states. Additional
cases cover drifted gate/log inputs, log failure before/after dispatch, protocol
failure, end-state-query failure, permission loss, round exhaustion, original
production bookkeeping, callback restoration, a real temporary JSONL append,
and proposal-copy isolation. The tests do not certify continuous unit movement.

Local Python is 3.13.5. Source files also pass Python-3.10 grammar parsing and
in-memory compilation; that is not execution on Python 3.10/3.11/3.12. Full
repository tests, Ruff and hosted CI remain unrun. A read-only attempt to fetch
the full accepted repository archive failed DNS resolution in this environment.
The earlier blocked source-publication request was not retried by another route.

The first runner-test run had 20 passes and 14 failures because the extracted-loop
test harness did not initialize its local `states` variable. Passing the initial
state and pending dictionary as function arguments fixed that harness error
without altering any statement of the frozen loop. The original failing output
and subsequent passing logs are retained. An initial existing-suite invocation
from the wrong working directory failed collection; the correctly rooted run
passed all 96 existing cases before the binding tests were introduced.

## Remaining acceptance

Source publication remains unresolved; no branch, PR or hosted validation exists
for V1/V2/V3. A new reviewed launcher/result binding, full-main/runtime-cleanup
composition tests, full-repository validation and a separately authorized new
experiment are still required before any Precision use. No improvement in real
scouting, combat or win rate is claimed. Both historical runs and the consumed
pair-03 attempt must remain untouched.
