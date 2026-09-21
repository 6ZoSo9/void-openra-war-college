# Abaddon scout-repair canary full-runner composition review v1

Marker: `void.abaddon.scout-repair-canary-full-runner-composition-review.v1`

## Purpose

This source-only review binds the exact frozen historical warm-start runner to the
already-reviewed deterministic canary opponent adapter and canary runner
requirements.

It does **not** create a runnable canary. Its job is to prove whether the frozen
runner can be reused unchanged and, if not, define the exact obligations for a
derived runner implementation.

## Bound sources

Historical runner:

`fixtures/learning/scout-missions-v1/warm_start_runner_v1_4.py`

- Git blob: `132a5b2df3c3dbc82df7c0ebc6d457e5b77ffb51`
- SHA-256: `ad7655e3ebfee198aed4ec879aa630f1fa4676eb75d8be432e6e5242dbc3d901`

Canary decision adapter:

`openra_env/learning/abaddon_scout_repair_canary_runner_adapter_v1.py`

- Git blob: `509f7651d36e83a182b7a485c88029dee537f633`

Canary runner requirements:

`openra_env/learning/abaddon_scout_repair_canary_runner_requirements_v1.py`

- Git blob: `b14175483877b4c35afc44d6c0f720ce07e68506`

The review computes Git blob identities directly from supplied exact bytes and
does not import or execute any of those sources.

## Why the historical runner is rejected unchanged

The exact frozen runner still has seven canary-incompatible facts:

1. it calls `helper.start_ollama()`;
2. it calls `helper.cleanup()` after marking Ollama started;
3. its controller loop calls the model-backed `apollyon_decision_typed`;
4. both controller trajectory row kinds set `training_candidate=true`;
5. its summary sets `controller_rows_training_candidate=true`;
6. the run header sets `agent_training_rows_begin_here=true`; and
7. stdout claims `apollyon_runtime_started_at_handoff=true`.

The focused review pins the exact AST/source shape for each fact. Any byte drift
fails before semantic reinterpretation.

Therefore:

`historical_runner_admissible_without_derivation=false`

## Derived-runner obligations

A later implementation must preserve the reviewed warm-start, typed tool,
unchanged host-validation, and same-tick joint-commit behavior while changing
only the canary-specific boundaries.

It must:

- replace the model-backed Apollyon decision with the reviewed deterministic
  canary adapter;
- never dereference the model helper for decision making;
- never start Ollama or another model service;
- never perform model inference;
- avoid model-service cleanup when no model service was started;
- emit no false runtime-start claim;
- mark all canary controller trajectory rows non-training;
- mark the canary summary's controller rows non-training;
- set `agent_training_rows_begin_here=false` or omit that field;
- log the exact deterministic-opponent source identity;
- retain one unchanged host validation per controller round;
- retain zero automatic retry;
- retain same-tick joint commit semantics;
- retain post-run clean-source requirements; and
- require independent runtime/container dormancy evidence.

This review intentionally does not prescribe a source-editing mechanism. The
derived runner must itself be separately source-reviewed and pinned.

## Authority boundary

The review performs no:

- source import or execution;
- host observation;
- game/model execution;
- service action;
- attempt consumption;
- training or policy promotion;
- deployment or VOID mutation;
- wallet/transaction/funds action; or
- execution authorization.

The next gate is:

`SCOUT_REPAIR_CANARY_DERIVED_RUNNER_IMPLEMENTATION_REQUIRED`.
