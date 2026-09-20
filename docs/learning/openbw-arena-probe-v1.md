# OpenBW War College arena probe V1

## Goal

Evaluate OpenBW as a **second** War College RTS environment without replacing
the accepted OpenRA lane and without claiming that an OpenBW match has run.

The first gate is deliberately smaller: prove that exact pinned OpenBW/BWAPI
source can be configured and compiled headlessly on hosted Linux CI.

## Pinned upstream source

OpenBW core:

- repository: `OpenBW/openbw`
- branch used for discovery: `master`
- exact commit: `4b046d5f65302b10cb0a745f0fecd37ec85b20a8`
- commit date: 2026-08-13
- current GitHub repository metadata reports no detected license
- the pinned repository root contains no `LICENSE` or `COPYING` file

OpenBW BWAPI fork:

- repository: `OpenBW/bwapi`
- branch: `develop-openbw`
- exact commit: `48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2`
- `LICENSE` Git blob:
  `65c5ca88a67c30becee01c5a8816d964b03862f9`
- that file contains the GNU Lesser General Public License version 3 text

Because OpenBW core's repository-level license is not explicit at the pinned
source state, this V1 probe does **not** vendor or redistribute OpenBW source.
Hosted CI obtains the public source transiently from the upstream repositories
at the exact commits above. Any later redistribution/package design requires a
separate license review.

## Upstream runtime facts

The OpenBW BWAPI README states:

- OpenBW is built as part of the BWAPI CMake build;
- Linux headless builds are supported;
- GUI support is optional and defaults off;
- `BWAPILauncher` is the main executable;
- runtime requires three external StarCraft data archives:
  `Stardat.mpq`, `Broodat.mpq`, and `Patch_rt.mpq`;
- OpenBW has no built-in computer player;
- multiplayer currently supports 1v1.

The repository does not contain or acquire those game assets in this lane.

## Probe

The workflow `.github/workflows/openbw-headless-build-probe-v1.yml`:

1. checks out the War College source;
2. validates this source-only contract;
3. obtains only the two pinned public upstream repositories;
4. verifies their exact commit identities;
5. checks the expected upstream licensing surface;
6. configures BWAPI/OpenBW with UI disabled;
7. builds only the `BWAPILauncher` target;
8. verifies the launcher artifact exists;
9. emits a build-only receipt.

It does **not** run the launcher, read/download StarCraft MPQ data, create a game
session, start a model, train, or promote policy.

## Why this topology

OpenBW has no built-in opponent. A useful future arena therefore needs two
controlled agents. The clean initial design is two local OpenBW processes in
1v1, each driven through the BWAPI surface by an explicitly source-bound
War College adapter.

Apollyon and Abaddon names must not be attached to those adapters until their
actual policy/runtime identity is bound and reviewed. The initial deterministic
smoke bots should use neutral names and produce non-training evidence.

## Gates after a green build

A green V1 build means only that the pinned sources compile headlessly.

Later gates are separate:

1. license/redistribution review for OpenBW core;
2. operator-supplied legitimate game-data admission by exact hashes;
3. inert two-agent harness design;
4. deterministic smoke-bot source identities;
5. replay/state determinism evidence;
6. only then, a separately authorized live smoke match;
7. later still, reviewed Apollyon/Abaddon adapters and cross-arena evaluation.

No live game authority is granted by this document or the build workflow.
