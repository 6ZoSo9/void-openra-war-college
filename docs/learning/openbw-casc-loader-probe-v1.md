# OpenBW current-client CASC loader probe V1

## Purpose

Prove that the pinned OpenBW/BWAPI stack can be compiled against Blizzard's
current CASC storage format without obtaining unofficial legacy MPQ archives.

This is a **compile-only** compatibility experiment. It does not install
Battle.net, install StarCraft, open CASC game data, launch OpenBW, or load a bot.

## Why this lane exists

Precision has no existing StarCraft/Brood War installation and no legacy
`StarDat.mpq`, `BrooDat.mpq`, or `Patch_rt.mpq` files.

The official Blizzard `STARCRAFT` installer endpoint was downloaded
read-only and resolved to:

- `Battle.net-Setup.exe`
- version path `installer/win/1.0.66/Battle.net-Setup.exe`
- 4,896,464 bytes
- SHA-256
  `de5d32d4ea5eed5a9e120027fb68b370976dbfecc8f2a8f91305977f0b87fcaf`

It was not executed.

Current Blizzard data uses CASC rather than pristine OpenBW's hardcoded legacy
MPQ directory loader.

## Architecture evidence

ChkForge demonstrates that an OpenBW-backed application can read StarCraft
content from CASC storage through CascLib. ChkForge's repository does not expose
a clear top-level license, so **none of its modified OpenBW source is copied**.

The War College integration independently implements a narrow C ABI shim
against CascLib's public API. OpenBW includes only that shim's opaque header,
so CascLib's legacy Windows-style typedefs cannot collide with old BWAPI's
compatibility typedefs.

## CascLib

Pinned dependency:

- repository: `ladislav-zezula/CascLib`
- commit: `2a280f5a231966dc5d1b534978dd9f9f04a374cd`
- date: 2026-08-22
- license: MIT
- LICENSE Git blob:
  `3b17df3d9bc1d17b55b61024baec95bfb1f264ea`
- `src/CascLib.h` Git blob:
  `39e9d3bdf360940e165f7793c95acac5fe00a8ca`

CascLib documents Linux CMake builds and provides the exact primitives used by
the probe: `CascOpenStorage`, `CascOpenFile`, `CascGetFileSize64`,
`CascReadFile`, `CascCloseFile`, and `CascCloseStorage`.

## Transient OpenBW transformation

The transformation applies only to a temporary checkout after verifying:

- OpenBW commit
  `4b046d5f65302b10cb0a745f0fecd37ec85b20a8`;
- `data_loading.h` Git blob
  `c8d5a0fd65a1672116189e9c95a7706e81f6671c`;
- BWAPI commit
  `48124ba8ed1b4d52b3dfd52acbaf34afb9a37fe2`;
- `bwapi/OpenBWData/CMakeLists.txt` Git blob
  `4339d2300fefce5005ed57f49522d0ad66038019`.

It replaces only the hardcoded three-MPQ `data_files_loader` implementation
with a loader that calls the War College C ABI shim. The shim alone includes
`CascLib.h` and links against the externally built CascLib shared library.

Pinned War College shim blobs:

- header: `112a6190449127f6c305273a764786085ea179d1`
- source: `81b954aca0b0a5d7ab6975294d567da7f855be78`
- CMake: `b95aa50b7f0703cc38657a4be77fb693eb869739`

No patched OpenBW file is committed to War College.

## Hosted proof

The workflow:

1. fetches exact OpenBW, BWAPI and CascLib commits;
2. verifies the CascLib MIT license blob;
3. builds and installs CascLib to a temporary prefix;
4. builds the War College C ABI shim against CascLib;
5. applies the already reviewed BWAPI GCC-13 `<cstdint>` patch;
6. applies the exact-source CASC loader transformer;
7. configures OpenBW/BWAPI headlessly;
8. builds `BWAPILauncher`;
9. verifies `libOpenBWData.so` depends on the War College shim and that the
   shim resolves `libcasc.so`;
10. never executes the launcher or opens game data.

## Next gate

A green compile proves architecture only.

The next external gate is installing the current official Blizzard StarCraft
data into an isolated local prefix, followed by read-only CASC identity and
filename-availability checks. Actual game execution remains separately
authorized.
