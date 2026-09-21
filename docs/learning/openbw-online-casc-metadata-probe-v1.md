# OpenBW online StarCraft CASC metadata probe V1

## Purpose

Replace the Battle.net-UI dependency with a direct, read-only metadata query to
Blizzard's official StarCraft CASC CDN.

The current Battle.net UI remained invisible under both stock Wine and
GE-Proton even though the Blizzard Agent reached the network. This probe avoids
that UI entirely.

## Upstream identities

CascLib is pinned to:

- repository: `ladislav-zezula/CascLib`
- commit: `2a280f5a231966dc5d1b534978dd9f9f04a374cd`
- license: MIT
- LICENSE blob: `3b17df3d9bc1d17b55b61024baec95bfb1f264ea`
- `src/CascLib.h` blob: `39e9d3bdf360940e165f7793c95acac5fe00a8ca`
- `src/CascOpenStorage.cpp` blob: `80458a45ee6bc193472002c5e7196fdabd684ea6`

## Parameter-parser correction

The pinned CascLib source contains stale public comments that show colon-delimited
examples for online storage. The actual parser does **not** use colons. Its
compile-time `CASC_PARAM_SEPARATOR` is `*`, and `ParseOpenParams` explicitly
parses:

`local_cache_path[*cdn_url]*code_name*region`

The first Precision probe used the stale commented colon form, so
`<cache>:s1:us` was treated as one literal local path and failed immediately
with `ERROR_FILE_NOT_FOUND` before any CDN request.

V1 now avoids the string parser entirely. It calls `CascOpenStorageEx` with a
structured `CASC_OPEN_STORAGE_ARGS`:

- `szLocalPath = <private-cache>`
- `szCodeName = "s1"`
- `szRegion = "us"`
- `dwLocaleMask = CASC_LOCALE_ENUS`
- `dwFlags = CASC_FEATURE_ALLOW_DOWNLOAD`
- `bOnlineStorage = true`

The pinned CascLib implementation requires `CASC_FEATURE_ALLOW_DOWNLOAD` to fetch
missing internal ENCODING/ROOT manifests when a fresh online cache is opened.
This does **not** give this probe a game-payload path: the executable deliberately
contains and links no `CascOpenFile` or `CascReadFile` symbol. The flag is therefore
bounded to internal metadata/manifests in this gate.

This removes delimiter ambiguity from the gate.

Current Lutris service metadata likewise maps Battle.net `s1` to StarCraft /
StarCraft Remastered.

## Metadata-only behavior

The executable:

1. opens Blizzard's online StarCraft CASC storage through structured args;
2. records product/build/features/total-file-count metadata;
3. enumerates the root namespace with a hard cap of 1,000,000 entries;
4. normalizes case and slash direction;
5. reports names whose suffixes match classic OpenBW inputs.

The first suffix set includes:

- `arr/units.dat`
- `arr/weapons.dat`
- `arr/flingy.dat`
- `arr/sprites.dat`
- `arr/images.dat`
- `arr/orders.dat`
- `arr/techdata.dat`
- `arr/upgrades.dat`
- `arr/sfxdata.dat`
- `arr/sfxdata.tbl`
- Badlands `.cv5/.vf4/.vx4/.vr4/.wpe` tileset files.

The executable deliberately contains no `CascOpenFile` or `CascReadFile`
call. Therefore this gate can fetch online CASC metadata/config/root structures,
but cannot request a game asset payload.

## Why namespace discovery comes first

Pristine OpenBW expects classic MPQ-era relative names. Modern StarCraft CASC
may expose those names with an additional prefix. Matching by normalized suffix
lets the probe discover the actual current namespace without guessing.

## Next gate

If the metadata probe proves the critical names exist, a separate payload gate
may open and hash a very small approved subset from Blizzard's CDN.

That later payload gate remains separate from game execution and from any
Battle.net account/login flow.
