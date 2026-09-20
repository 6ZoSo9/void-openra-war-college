# OpenBW neutral two-agent duel harness V1

## Purpose

Prepare the smallest deterministic two-process OpenBW/BWAPI smoke topology
without attaching Apollyon or Abaddon to the new arena and without launching a
game.

This lane depends on the pinned/build-only OpenBW arena probe. It adds
War College-owned neutral bot source and proves that both AI modules compile and
export the BWAPI entry points. Runtime remains separately gated.

## Neutral smoke bots

Both shared libraries are compiled from:

- `integrations/openbw/neutral_smoke_bot.cpp`
- Git blob `2ee1ee850b7b4ef2fb3292305189375f97015f3a`

The integration CMake source is:

- `integrations/openbw/CMakeLists.txt`
- Git blob `39ca02f5bde4dc42a949846433fd59285b47ffff`

Role A is passive except that it calls BWAPI `leaveGame()` at frame **480**.
Role B remains passive. Neither role enables user input or hidden map
information, performs model calls, opens its own files/sockets, trains, or
claims to be Apollyon or Abaddon.

## Future deterministic topology

The data-only launch contract fixes:

- two OpenBW/BWAPI processes;
- local `OPENBW_LAN_MODE=LOCAL` transport;
- one private per-run socket path;
- host process starts first with a non-existing socket path;
- joiner starts only after host socket creation is observed;
- both clients use the same admitted map bytes;
- both races are Terran for the first smoke;
- game type is MELEE;
- host seed override is **2050**;
- joiner does not supply a competing seed override;
- auto-restart is OFF;
- min/max players are both 2;
- shared-memory BWAPI server is OFF;
- UI and sound are OFF.

BWAPI's `Config.cpp` maps configuration to environment variables as
`BWAPI_CONFIG_<SECTION>__<KEY>`; the harness uses that canonical mapping
instead of generating mutable INI files.

## Asset boundary

No StarCraft/Brood War assets are included, downloaded, discovered, or read by
the compile lane.

A later operator admission must provide exact SHA-256 identities for
`Stardat.mpq`, `Broodat.mpq`, `Patch_rt.mpq`, and the exact selected map,
plus an operator review of the license/ownership basis for using those local
assets. Even valid asset evidence does not authorize launching the match.

## Compile gate

The dedicated workflow fetches the exact pinned OpenBW/BWAPI source, applies
only upstream PR #16's exact GCC-13 compatibility patch, builds
`BWAPILauncher` without executing it, builds both War College bot shared
objects, verifies ELF type plus `gameInit` and `newAIModule` exports, and
records hashes.

It never loads either bot or launches the game.

## Later gates

After compile evidence:

1. operator game-data/map hash admission;
2. create-only runtime attempt guard;
3. source-bound dual-process invocation;
4. separate explicit authorization for one smoke match;
5. post-run replay/result/dormancy evidence;
6. only after that, strategy-capable neutral agents;
7. only later, independently reviewed Apollyon/Abaddon bindings.

No runtime authority is created here.
