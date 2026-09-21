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

CascLib documents online storage parameters as:

`<local_cache_path>:<product_code>:<region>`

The StarCraft product is `s1`, and this probe uses region `us` plus enUS
locale, yielding:

`<private-cache>:s1:us`

Current Lutris service metadata likewise maps Battle.net `s1` to StarCraft /
StarCraft Remastered.

## Metadata-only behavior

The executable:

1. opens Blizzard's online `s1:us` CASC storage;
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
