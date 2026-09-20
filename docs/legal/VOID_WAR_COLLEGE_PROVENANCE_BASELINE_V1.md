# VOID OpenRA War College Provenance Baseline V1

**Baseline date:** 2026-09-20  
**VOID accepted reference:** `9a151da589f93454d31a475b29297ea8a3d35442`  
**VOID tree:** `004ea893b529d297944000bff690da974a9dba71`

## Purpose

This is a dated attribution/provenance baseline for future comparisons.

It is designed to answer a narrow question: **what distinctive downstream War
College material was publicly present in this repository at this point in
time, and what upstream material are we explicitly not claiming?**

Similarity to this baseline is evidence to investigate, not an automatic
finding of copying, infringement, or bad faith.

The machine-readable companion is
`docs/legal/void-war-college-provenance-baseline-v1.json`.

## Fixed comparison references

At baseline creation, the public comparison references were:

- VOID War College: `6ZoSo9/void-openra-war-college`
  - main `9a151da589f93454d31a475b29297ea8a3d35442`
  - tree `004ea893b529d297944000bff690da974a9dba71`
- OpenRA-RL: `yxc20089/OpenRA-RL`
  - main `5dadd449c912ac2d4021cc8ed84fc0b385b1543c`
  - tree `fa92204fdca0c5f647da1d93a14f16821a4532af`
- OpenRA-RL Website: `yxc20089/OpenRA-RL-Website`
  - main `0007f1fed49e954a7706c7c64a6c98894f98cfb1`
  - tree `4f95d8c65eaa1f10804cffc9be4a3c2e1b7727f0`

These exact refs make later comparisons reproducible even after those projects
change.

## Downstream-only path baseline

At those exact refs:

| VOID path prefix | VOID files | Same paths in OpenRA-RL main | Same paths in OpenRA-RL Website main |
| --- | ---: | ---: | ---: |
| `openra_env/learning/` | 112 | 0 | 0 |
| `openra_env/analysis/` | 23 | 0 | 0 |
| `docs/learning/` | 10 | 0 | 0 |
| `fixtures/learning/` | 14 | 0 | 0 |

This is a path-level observation, not a blanket copyright conclusion. Some
files inside downstream-only directories may embed copied fixtures, protocol
definitions, generated material, or other third-party content. The manifest
records fingerprints; ownership still follows actual authorship.

## Dated first-public evidence anchors

| Distinctive system | First public commit | UTC | Recorded author |
| --- | --- | --- | --- |
| normalized warm-start pair binding | `00125bec14aab93b32005e7c037537ca956aad32` | 2026-08-27T20:51:33Z | 6ZoSo9 |
| General Brain generation and corpus gate | `646acd3a3200634c9c2bbd005b938f00f0eca4f5` | 2026-08-28T10:12:54Z | 6ZoSo9 |
| Apollyon brain generation zero | `883ff9de8cc852192b9fc26e6c7e9d437077b81d` | 2026-08-28T10:13:13Z | 6ZoSo9 |
| Abaddon brain generation zero | `d0fe904658277fd22ce2ebe1e84b880e85f2478a` | 2026-08-28T10:13:25Z | 6ZoSo9 |
| reviewed Abaddon campaign contract | `d89f1d978189f9fa0ca93a826f87f113cd812fe3` | 2026-09-14T22:14:31Z | 6ZoSo9 / zoso |
| bounded Abaddon scout mission lifecycle | `dae97247b47dbbef48cec533ab403c20b5278bae` | 2026-09-20T19:36:59Z | 6ZoSo9 / zoso |

Representative anchors:

- **Normalized warm-start pair binding** appeared on 2026-08-27 in
  `openra_env/analysis/spar_pair_binding.py`.
- **General Brain generation/corpus gating**, **Apollyon generation zero**, and
  **Abaddon generation zero** were publicly committed on 2026-08-28.
- The **reviewed Abaddon campaign contract** appears in the September War
  College campaign line.
- The **bounded Abaddon scout mission lifecycle** was published in PR #181 and
  accepted into main on 2026-09-20.

The companion JSON binds these claims to exact commit IDs and every current
Git blob under the four tracked downstream areas.

## Explicit upstream prior-art exclusions

We do **not** claim generic OpenRA-RL leaderboard or multi-session work as
original VOID War College material.

Two concrete examples exist in both repositories with the **same Git commit
hashes**:

- `40d745772153af97dc4a53f91c9065271fc34dd0` — bench
  auto-export/upload and leaderboard submission, authored upstream in February
  2026.
- `0b04233dc756121bab55354cc914990dc40dc417` — multi-session Python client
  and single-daemon architecture, authored upstream in March 2026.

Their identical commit identity demonstrates inherited upstream history. Any
future attribution analysis must exclude that material.

Likewise, generic ideas such as AI agents, benchmarks, leaderboards,
reinforcement-learning curricula, replay verification, or multi-session
execution are weak similarity signals by themselves.

## Distinctive terminology snapshot

At the comparison refs above, GitHub code search returned zero matches in both
OpenRA-RL and OpenRA-RL-Website for:

- `Apollyon`
- `Abaddon`
- `General Brain`
- `warm-start pair`
- `evidence contract`
- `source binding`
- `goal effect`
- `candidate-only`

This search snapshot is supporting evidence only. Search absence does not prove
absence from historical, private, deleted, unindexed, or differently worded
material.

## Public website / Hugging Face boundary

OpenRA-RL's public website and OpenRA-Bench/Hugging Face surfaces predate the
distinctive War College systems above. Those surfaces include generic agent,
benchmark, replay, training, and leaderboard concepts.

This baseline therefore does **not** treat those generic surfaces as VOID-owned
material.

Future concern should focus on later appearance of distinctive War College
expression or implementation: exact/near-exact source, schema names, unusual
contract structures, tests, fixture shapes, documentation language, or several
independent distinctive features appearing together.

## Future comparison protocol

When a potentially similar project appears:

1. Preserve URLs, commit IDs, timestamps, screenshots, and downloadable source.
2. Compare against the fixed blobs in the companion JSON.
3. Separate exact matches from structural similarity and generic ideas.
4. Establish chronology: which expression was publicly committed first.
5. Check whether the material is actually upstream prior art already inherited
   by this repository.
6. Check license/notice preservation.
7. Record access/provenance facts that are publicly supportable; do not infer
   motive from similarity alone.
8. Escalate strong evidence for human/legal review before making a public
   accusation.

### Strong signals

- exact Git blob or byte-for-byte matches of downstream-only files;
- later near-identical implementation of distinctive War College structures;
- reuse of distinctive project/schema names such as Apollyon, Abaddon, General
  Brain, or VOID-specific evidence/source-binding terminology;
- copied comments, documentation wording, tests, fixtures, hashes, or
  reproducibility conventions;
- several independent distinctive similarities occurring together.

### Weak signals

- AI agents;
- leaderboards;
- RL training or curricula;
- replays;
- multi-session runtimes;
- OpenRA/OpenEnv integration patterns.

## Integrity

The companion JSON contains **159 file fingerprints** from:

- `openra_env/learning/`
- `openra_env/analysis/`
- `docs/learning/`
- `fixtures/learning/`

Each record contains path, Git blob SHA-1, byte size, and same-path presence
against the two fixed comparison trees.

This document does not alter the GPL, expand copyright ownership, or declare
that anyone has copied the project. It creates a reproducible baseline so
future attribution questions can be evaluated against evidence.
