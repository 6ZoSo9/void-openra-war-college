# Abaddon scout-repair canary derived runner v1

## Purpose

`scout_repair_canary_derived_runner_v1.py` is a source-only derivative of the
exact frozen warm-start runner reviewed by the preceding full-runner composition
gate.

It removes the historical model-service/inference behavior and training labels
while preserving the warm-start, typed tool, host validation, game transport,
and same-tick joint mechanics needed by a later explicitly authorized canary
launcher.

This source is **not directly executable**. Its `main()` always raises:

`SCOUT_REPAIR_CANARY_DERIVED_RUNNER_SOURCE_BINDING_AND_LAUNCHER_REQUIRED`.

## Frozen source ancestry

Historical source:

`fixtures/learning/scout-missions-v1/warm_start_runner_v1_4.py`

Historical Git blob:

`132a5b2df3c3dbc82df7c0ebc6d457e5b77ffb51`

Historical SHA-256:

`ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901`

Derived source:

`fixtures/learning/scout-missions-v1/scout_repair_canary_derived_runner_v1.py`

Derived Git blob at this review head:

`166fccd460387b1228702f0032639e99fe4d7f18`

The focused proof computes both Git blob identities from bytes.

## Preserved mechanics

The proof compares these function ASTs directly against the historical runner:

- warm-start state helpers;
- pending reconciliation;
- host-step/wait helpers;
- structure and infantry setup;
- contact staging;
- typed current-turn tool construction; and
- typed host command validation.

The frozen runtime image ID, engine commit, base-runner digest, runtime
attestation digest, curriculum identity and warm-start production constants are
also preserved.

## Model capability removal

The derived source contains no:

- `helper.ollama_tool_call`;
- `helper.start_ollama`;
- `helper.cleanup`;
- `base.APOLLYON_RUNNER`;
- `base.APOLLYON_MODEL`;
- historical model-backed `apollyon_decision_typed` call; or
- systemd model-service command.

Instead, one `DeterministicCanaryOpponentAdapter` is created and each
controller round delegates exactly once through
`deterministic_canary_decision`. The adapter still passes its proposal through
the unchanged typed host validator.

The source emits no claim that a model service was started or cleaned up.

## Non-training boundary

Every canary controller trajectory row is explicitly:

`training_candidate=false`.

The run header fixes:

- `agent_training_rows_begin_here=false`;
- `controller_rows_training_candidate=false`;
- exact canary namespace; and
- deterministic opponent source identity.

The raw runner summary also records
`controller_rows_training_candidate=false` and explicitly says independent
post-run dormancy is not yet verified.

No raw runner summary is a final accepted canary result.

## Accepted-main binding remains external

The historical fixed War College commit cannot be reused for the new canary
because it predates the reviewed repair/launcher chain.

Therefore `run_bound_canary()` requires a lowercase 40-hex
`accepted_war_college_commit` from a later reviewed launcher and compares the
live checkout against it before game setup.

The source itself does not decide which future `main` is accepted.

## Arm selection remains external

This runner is the shared execution substrate for both canary arms.

A later source-bound launcher must:

- use this runner without scout binding for `legacy_control`;
- install the already-reviewed `ScoutMissionRunnerBinding` for
  `scout_repair_treatment`;
- prove the treatment binding is actually installed before invoking the
  runner;
- bind the same seed/runtime image/engine/main/tick parameters across both
  arms;
- create a separate create-only attempt marker for each arm; and
- prevent pair-03 or prior campaign authority reuse.

The runner does not self-label an arm, preventing a caller from claiming
treatment while accidentally running the control path.

## Dormancy and result acceptance remain external

The runner may eventually start the reviewed OpenRA engine container when a
future launcher grants execution. It does not start a model service.

After game teardown, independent post-run evidence must still establish:

- model/runtime service inactive;
- service disabled;
- activation permit absent;
- stale engine container count zero;
- source/baseline preservation; and
- attempt marker/result/evidence binding.

Only then may the separate canary result contract admit a completed arm result.

## Authority boundary

At this stage:

- direct execution is held;
- no accepted current-main commit is selected;
- no arm is selected;
- no treatment binding is installed;
- no attempt is consumed;
- no host observation is performed;
- no game/model execution occurs;
- no training/promotion/deployment/VOID mutation occurs; and
- no wallet or funds action occurs.

Next gate:

`SCOUT_REPAIR_CANARY_DERIVED_RUNNER_SOURCE_BINDING_AND_LAUNCHER_REQUIRED`.
