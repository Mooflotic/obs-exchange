# OBS-DB-SLIM · Passo 1 — GO eseguito

**2026-07-24 22:15 UTC** · live · branch `feature/obs-db-slim` · **nessun deploy** · **nessun VACUUM**

Script: [`obs_db_slim_p1_drop_dup_indexes.py`](https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs_db_slim_p1_drop_dup_indexes.py) (senza `ix_metric_snapshots_*`)

---

## a) DRY_RUN finale

```
DB /data/db/observatory.db size=2676752384 DRY_RUN=True
DROP_CANDIDATE ix_observations_raw_dedup_key bytes=64319488 KEEP sqlite_autoindex_observations_raw_1
DROP_CANDIDATE ix_observations_seen_at bytes=39411712 KEEP ix_obs_seen
LOGICAL_FREE_EST_BYTES 103731200 (98.9 MiB)
FILE_WILL_STAY ~2676752384 until VACUUM (passo 4); freelist_now=2
=== EXPLAIN BEFORE ===
-- dedup_lookup
   SEARCH observations_raw USING INDEX ix_observations_raw_dedup_key (dedup_key=?)
-- presence_mac_seen
   SEARCH observations USING INDEX ix_observations_mac (mac=?)
-- seen_at_range
   SEARCH observations USING COVERING INDEX ix_obs_seen (seen_at<?)
-- seen_at_count_24h
   SEARCH observations USING COVERING INDEX ix_obs_seen (seen_at>?)
DRY_RUN done — nessun DROP
```

## b) Snapshot pre-op

| | |
|--|--|
| Path | `data/backups/pre-db-slim-p1-20260724-221514.db` |
| Size | **2 676 768 768** B ≈ **2.5 GiB** |
| Guard | `SNAPSHOT_OK` (≥ 95% del live) |

## c) DROP + EXPLAIN AFTER

```
DROP INDEX ix_observations_raw_dedup_key
DROP INDEX ix_observations_seen_at
=== EXPLAIN AFTER ===
-- dedup_lookup
   SEARCH observations_raw USING INDEX sqlite_autoindex_observations_raw_1 (dedup_key=?)
-- presence_mac_seen
   SEARCH observations USING INDEX ix_observations_mac (mac=?)
-- seen_at_range
   SEARCH observations USING COVERING INDEX ix_obs_seen (seen_at<?)
-- seen_at_count_24h
   SEARCH observations USING COVERING INDEX ix_obs_seen (seen_at>?)
```

`assert_no_scan` AFTER: **pass**. Nessun restore.

Verifica master: entrambi i DROP **GONE**; keep **PRESENT**; `ix_metric_snapshots_taken_at` intatto (escluso).

## d) Freelist / file OS

| Voce | Prima | Dopo |
|------|------:|-----:|
| `freelist_count` | 2 | **25 327** |
| freelist bytes | ~8 KiB | **103 739 392** ≈ **98.9 MiB** |
| pagine attese | — | 103 731 200 / 4096 ≈ 25 326 ✓ |
| `OS_SIZE` file | 2 676 752 384 | **2 677 227 520** (~invariato; +~0.5 MiB writer concurrenti) |

Comportamento corretto: spazio in freelist riusabile; file non cala senza VACUUM (passo 4).

---

## Follow-up (non fatto)

- Hygiene modelli SQLAlchemy (evitare ricreazione `index=True` duplicato) su merge successivo.
- `ix_metric_snapshots_taken_at` resta; solo con PROBE dedicata.
