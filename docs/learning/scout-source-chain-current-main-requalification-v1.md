# Scout source chain current-main requalification v1

This lane consolidates historical draft PRs #191, #192, #193 and #194 onto
current War College main without rewriting any reviewed payload file.

## Exact lineage

The consolidation preserves:

- #191 head `1e9fd02bb8120628e7daf4208fd3ee51f7dd140e` — 23 additive files;
- #192 head `3213b6cbe3fec94f90c0ccb13d10eab8482e2245` — 16 additive files;
- #193 head `2fe34494a35bf5dcfc1aedda3d8096e1b10b9b12` — 4 additive files;
- #194 head `13a4c64783c0380b6f969ce6d10fddd0e18df1e8` — 4 additive files.

All 47 destination Git blobs exactly match their source PR blobs.

## Historical main binding is preserved

#191 intentionally records the original accepted scout proposal against:

`9a151da589f93454d31a475b29297ea8a3d35442`

That historical source binding is **not** rewritten to pretend the proposal was
originally reviewed against a later main.

Instead, this requalification separately proves that the eight dependency blobs
bound by that historical proposal remain byte-identical on the consolidation
base main:

`3703eaddc7e95f917de72747cc3e6248c78fb295`

Those dependencies are the accepted scout runner binding, host bridge, missions,
goal/effect core, frozen warm-start runner, joint-host fixture,
Abaddon-controller fixture and RL bridge protocol.

## Canary stack semantics remain unchanged

#192 remains source/design-only and still leaves
`accepted_main_head_with_repair=None`. #193 remains a source-only review proving
that the frozen historical full runner is not admissible unchanged for the
non-model canary. #194 remains the derived non-model runner implementation and
still requires a later source-bound launcher and explicit authority.

The consolidation does not select a future accepted repaired main, consume an
attempt, run a game/model, start a service, train, promote policy, deploy, mutate
VOID, or touch wallets/funds.

## Machine-readable evidence

`config/war-college/scout-source-chain-current-main-requalification-v1.json`

binds all 47 payload blobs, all eight historical dependency blobs, the four
source PR heads, the current-main requalification base and the no-authority
boundary.

The focused source-contract test recomputes every Git blob identity from the
checked-out bytes and confirms the historical main binding was preserved rather
than rewritten.
