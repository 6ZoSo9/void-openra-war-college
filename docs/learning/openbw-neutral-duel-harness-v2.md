# OpenBW neutral dual harness v2

This lane replaces the historical stacked neutral-duel PR #185 with a
current-main source surface that matches the runtime topology already qualified
by the merged OpenBW S1 builder.

## Adopted source identity

The committed neutral bot source is the exact source used by the accepted merged
builder dual runtime:

- `integrations/openbw/neutral_smoke_bot.cpp`
- Git blob `3bc58999d2506ee8d5e130b834e4288ea55e909e`

The CMake source is unchanged from the original compile-only harness:

- `integrations/openbw/CMakeLists.txt`
- Git blob `39ca02f5bde4dc42a949846433fd59285b47ffff`

Role A remains passive and requests leave at frame 480. Role B ignores anonymous
startup `PlayerLeft` events, waits until at least frame 360, recognizes the
named `VOID-A` departure, and requests its own clean leave.

Neither role enables CompleteMapInformation or UserInput, issues unit commands,
uses a model, trains, performs its own filesystem/network I/O, or claims an
Apollyon/Abaddon identity.

## Qualified topology

The accepted runtime topology is now:

- two OpenBW/BWAPI processes;
- `OPENBW_LAN_MODE=LOCAL_FD`;
- one preconnected AF_UNIX socketpair;
- pinned `MapTest.scx` bytes;
- CASC-backed S1 data through the merged production builder;
- CASC downloads disabled;
- zero cache growth;
- A bounded leave at frame 480;
- B bounded follow-up leave after the named A departure.

This supersedes #185's unproven pathname-`LOCAL` design and its legacy MPQ
asset assumptions.

## Fixture-only lobby adaptation

The pinned BWAPI test map has one open-human and one computer slot. The accepted
dual runtime therefore used a temporary isolated-checkout adaptation that
promoted exactly one computer slot to open-human under explicit pre/postcondition
checks.

That adaptation is not part of the merged production builder and is not part of
the committed neutral bot source. It remains test-harness plumbing only.

## Evidence

The merged runtime qualification is recorded in:

`config/war-college/openbw-s1-merged-builder-runtime-qualification-v1.json`

The accepted dual verifier SHA-256 is:

`65f3dfa73c5addfe5e5acce1ad48ee49a9cba0da65b79cc635b317c68d420d48`

The run proved two-instance local synchronization, named peer-departure
propagation, bounded follow-up exit, clean `[0, 0]` launcher return codes and
zero cache growth.

## Authority boundary

This source adoption creates no new execution permit. It records the neutral
harness that has already been qualified and leaves any future agent/model
binding behind a separate review gate.

No Apollyon/Abaddon binding, model execution, training, policy promotion,
deployment, VOID mutation, wallet, transaction or funds action is authorized by
this source lane.
