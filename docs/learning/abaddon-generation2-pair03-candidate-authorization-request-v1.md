# Pair-03 candidate authorization request

This source-only proposal follows merged #174. It does not accept operator
authorization, implement candidate invocation, or change the existing gate:
`V2R13_PAIR03_CANDIDATE_EXECUTION_AUTHORIZATION_REQUIRED`.

## Proposed operation

One Generation-2 V2R13 pair-03 candidate attempt, with no automatic retry,
no baseline rerun, no other pair, and no held-out arm. The packet binds the
reviewed candidate wrapper/fixture/genome, baseline trajectory/summary,
controller/refiner, and frozen runtime identities. Its preparation-main head
is historical provenance, not a claim about current host HEAD or readiness.

The baseline reference records 36 completed rounds and `DRAW_OR_UNFINISHED`;
it does not claim a decisive result. This module reads neither baseline file.

## Data interface

`build_candidate_authorization_request()` returns a fixed canonical UTF-8 JSON
proposal with sorted keys, compact separators, and one terminal LF.
`validate_candidate_authorization_request(payload)` accepts only exact built-in
`bytes`, rejects empty or over-16-KiB input before comparison, and accepts only
byte-for-byte equality with that fixed proposal. There is no caller JSON parser.
Duplicate keys, alternate encodings, extra fields, changed identities, numeric
aliases, broadened scope, and altered authority flags therefore cannot match.
The returned SHA-256 identifies request bytes; it does not identify the operator
or grant any authority. Validation can be repeated: it consumes no attempt.

`candidate_authorization_request_contract()` returns fresh, independently
mutable snapshots. `authorize_or_execute_candidate()` always raises the existing
authorization HOLD, including for valid packets and historical six-arm permits.

## Remaining runtime obligations

A future separately reviewed accepting/invoking implementation must enforce
candidate-specific operator authorization, exact invocation-source review,
fresh current-main host preflight, cached sudo authority, live revocation,
isolated gRPC Python, exact non-inference model preload, canonical worktree
observation, fresh live readiness, baseline-byte reverification, and create-only
single-use attempt consumption. This module implements none of those host gates.
The eight source references are expectations, not a complete transitive inventory.

All operator/source/evidence/readiness/consumption acceptance flags remain false.
Training, weights changes, policy promotion, deployment, VOID and funds actions
remain unauthorized. No runtime module is imported by this request builder.
The tests additionally hash the eight referenced files on the complete checkout;
that repository check does not turn request validation into runtime permission.
