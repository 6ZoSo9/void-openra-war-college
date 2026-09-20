# Abaddon scout mission lifecycle candidate

## Outcome and integration boundary

This is an offline controller repair for the shared scouting defect diagnosed in
pair-03, not a promotion of candidate #252. `ScoutMissionController` composes an
already reviewed frozen Abaddon module. It does not load that module, patch its
globals, replace its source, change the frozen executor, or install runtime hooks.
There is no CLI, dispatcher, model call, filesystem operation, or training step.
The current Precision controller and consumed candidate attempt are unchanged.

The repair changes the scouting branch, not ordinary production/contact priority.
It returns a proposal envelope. A future separately reviewed host integration must
pass only `proposal['decision']` into the existing command validator and then call
`acknowledge(proposal_id, accepted=..., command_count=...)` with that actual gate's
result. Another observation is refused until this acknowledgement arrives. Do not
reuse the old one-shot launch authorization or feed hypothetical acknowledgements
into a live run.

## Reuse, not a competing recovery framework

The earlier `general_destination_recovery_v1.py` (SHA-256
`4f38b082cf44f3de7de0b946a8311b6c63e425f90127924705eef917234645de`)
was inspected. It supplies a movement veto/reselection boundary, not an Abaddon
mission planner; its original documentation explicitly requires a controller
replan interface. It is neither replaced nor silently connected here.

The existing `goal_effect_core_v1.py` is reused byte-for-byte from the retained
`void-prepare-generals-portable-strategy-v1.py` payload: SHA-256
`eaa344512cd8895dff9c21011f6cee34cdeabdd85118e59a4e172334cf39661e`.
Its Scope, Goal, Expectation, Observation and GoalEffectMonitor supply identity,
clock, target-distance progress and observed satisfaction. The installer was
parsed as literals, not executed. No skill learner, policy fitting or training
code is imported. This preserves earlier work instead of inventing another
monitor. Repository packaging is new; live integration is not implied.

## Implemented behavior

- One active `(unit, destination)` mission and one pending host result per scope.
  A proposed move is not issued. A positive host result with at least one
  dispatched command creates `ISSUED`, not a completed visit. Rejection never
  creates an assignment or a visit. A missing or inconsistent result holds.
- New scouts must be owned, living-or-health-unknown, combat-capable infantry
  with explicit consistent idle flags and no nonempty activity. The first
  eligible ID is selected, rather than unconditionally taking the lowest ID.
  The existing `_scout_target` planner chooses the target; coordinates are not
  invented by this adapter. Unknown-idle and busy actors are not commandeered.
- New best sampled Manhattan distance renews the stall review window while the
  same assignment remains active. Construction, cash, movement by another unit,
  and moving away then back to the same best distance cannot renew it. A fixed
  overall mission window prevents endless extensions.
- Only observed proximity within the configured arrival radius produces
  `COMPLETED` history. Missing actors, zero health, changed actor type, or loss
  of combat capability invalidate an assignment without inventing a death or
  completed visit. Lack of observed progress produces `FAILED` review state;
  it is not proof of pathfinding failure or unreachable terrain.
- Production and visible-contact decisions still come from the original
  controller. An accepted, actually dispatched higher-priority order selecting
  the scout interrupts the mission; rejected or zero-command outcomes do not.
- Completed visits and failed/interrupted destinations have separate tick-based
  cooldowns. Neither is permanent target exhaustion. Records are bounded and
  not silently evicted to manufacture eligibility. Duplicate evidence, reversed
  ticks, changed scope/map, malformed unit/contact data and exhausted budgets
  hold before publishing another proposal.
- The returned legacy-shaped decision updates its action hash and memory to the
  actual proposal. The original planner's immediate `scout_targets.append` is
  discarded on the private controller copy. Only completed visits enter that
  compatibility field. Public snapshots and proposal dictionaries are copies.

Defaults are proposed engineering choices, not values optimized or validated in
new games: 300 game ticks without a new best distance; 1,200 maximum mission
ticks; 1,200 completed-visit cooldown; 300 failed/interrupted cooldown; arrival
radius 2 Manhattan cells; 128 retained history entries; 4,096 observations.
The monitor remains bounded even when samples are infrequent. Arrival observed
in a late sample establishes arrival at that sample, not an inferred arrival
time. Scope must identify one run, Abaddon, one world revision, and game ticks.

An `advance` decision while an assignment progresses means no replacement scout
order is proposed. It is not a forged host acceptance or a new independent clock
advance. The existing joint host retains its clock and command semantics.

## Evidence fixtures and tests

`fixtures/learning/scout-missions-v1/abaddon_controller_v1.py` is a **historical
read-only test fixture**, not another selected runtime controller. It is exactly
the executed source SHA-256
`b235d4cff3e3953ed7c511de52c76ada7e1a47046295e104353b61ef09e11103`.
The adapter receives the trusted module from its caller; it does not read this
fixture at runtime. Tests bind the fixture and reused monitor hashes.

`pair03_saved_observations.json` contains ordinary canonical JSON, not executable
code. Its SHA-256 is
`2c88f2a81dababba939fe839a3161e6d26833dee1a634670dc01164859224cff`.
The 34,471 bytes project 13 recorded Abaddon observations and original
decisions: candidate rounds 8 through 18 and 33, plus baseline round 33. Each row
names its original JSONL line. Original trajectory and archive hashes are stored
in the fixture. Apollyon model responses and the private host snapshot are not
included. The uploaded archive itself is unchanged.

The saved-round controls establish that round 10 has no eligible idle infantry,
so the adapter waits instead of retasking busy actor 142. Round 17 has eligible
idle infantry and can propose scouting rather than inheriting six permanently
excluded issued destinations. A recorded-input sequence checks retention and
non-completion, while synthetic transitions establish accepted/rejected issue,
arrival, progression, stall, unavailable actor, contact interruption, expiry,
capacity, scope, acknowledgement and snapshot isolation behavior.

Local verification uses Python 3.13.5 and the complete new test file; no committed
skip or runtime dispatch exists. Additional local replay evaluates both complete
36-observation streams with explicitly **synthetic** host acknowledgements. Its
changed proposals do not generate alternate world states. Therefore neither
that replay nor these tests establish improved exploration, combat results or
live effectiveness. The previous 29-test evidence review remains unchanged.

The normal repository suite must validate this additive source generation on its
supported Python versions and run lint. A separately reviewed constructor/host-
feedback integration and separately authorized new experiment are still required
before using this candidate live. No source sync or Precision command accompanies
this source-only proposal; do not delete or reset either completed run or marker.
