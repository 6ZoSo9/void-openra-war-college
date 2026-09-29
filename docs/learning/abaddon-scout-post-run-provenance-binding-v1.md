# Scout post-run provenance binding v1

## Purpose

The reviewed scout post-run backend proves more than the historical v1 evidence
record serializes.

The backend receives an exact admitted War College commit, the frozen OpenRA
commit, a single canary container identity, and the exact durable-attempt
context. Its source-cleanliness probe verifies those identities before returning
true. The v1 evidence record then collapses that result to
`source_checkout_clean=true`.

That is sufficient for the old structural schema, but it leaves a provenance
ambiguity: later evidence review cannot recover which War College commit and
engine context were actually supplied to the backend call.

This change closes that source-only gap without rewriting the historical v1
evidence format.

## Binding record

`abaddon_scout_post_run_provenance_bundle_v1.py` produces a second canonical
record after validating canonical v1 state evidence.

The record binds:

- experiment identity;
- exact attempt-marker SHA-256;
- SHA-256 commitment to the absolute marker path without publishing the path;
- SHA-256 commitment to the admitted directory device/inode identity without
  publishing those raw local values;
- exact canary container name;
- exact admitted War College commit;
- frozen OpenRA commit;
- SHA-256 of the canonical v1 post-run state bytes;
- the reviewed observer-contract identity; and
- the pinned backend, backend-review, observer, and observer-contract source
  blobs.

The same `ScoutPostRunBackendInputs` object is passed to the reviewed backend
collector and then to the binding builder. This makes the serialized provenance
context correspond to the inputs used for that collection call.

## What this does not claim

This layer does not select the real host backend automatically. It does not claim
that a live Precision observation occurred merely because a binding record
exists.

It also does not:

- authorize a scout run;
- create or reset an attempt;
- start or stop a service;
- create or remove a container;
- load a model;
- execute inference or a game;
- train or update weights;
- admit data to a corpus;
- promote or deploy a policy;
- mutate VOID chain state;
- access wallets or signers; or
- perform transactions or funds movement.

The historical v1 state schema remains unchanged.

## Validation

The companion regression tests cover:

- exact War College and OpenRA identity serialization;
- exact state-evidence digest binding;
- canonical v1 state-byte enforcement;
- experiment and attempt-digest mismatch rejection;
- rejection when any required observation is false;
- path and directory commitments without raw local-value publication;
- distinct binding bytes for distinct admitted War College commits;
- one backend collection feeding one binding from the same inputs;
- malformed marker context rejection; and
- permanent refusal of execution authority.

## Exact-blob source review

The companion
`abaddon_scout_post_run_provenance_bundle_source_binding_review_v1.py`
pins the provenance module and its regression test to their exact Git blob
identities. Its regression suite recomputes Git blob SHA-1 from checkout bytes
and includes a one-byte drift negative control.

The review also requires the prior backend source review to remain closed,
requires every provenance authority field to remain false, preserves the
historical v1 evidence schema, and performs no host observation.

## Next gate

`SCOUT_POST_RUN_PROVENANCE_AWARE_LIVE_OBSERVATION_REQUIRES_SEPARATE_AUTHORIZATION`

Any live observation must be a separate explicit step using the reviewed
read-only backend and provenance-aware bundle. This source review does not
authorize that observation, a new scout attempt, or final result acceptance.
