# OBS-DB-SLIM — FASE A (sola lettura)

Censimento live Cassiopea · `observatory.db` · **nessuna cancellazione / nessun VACUUM / nessun fix**.
Snapshot: **2026-07-24 ~21:45 UTC** · API **0.10.21**.

Obiettivo dichiarato (fasi successive, non questa): file più piccolo su disco **con VACUUM**, dopo mappa writer/reader. Qui solo la mappa.

---

## 0 · File e pragma

| Voce | Valore |
|------|--------|
| Path | `/data/db/observatory.db` (volume1 HDD md1) |
| `OS_SIZE` | **2 668 638 208** B ≈ **2.49 GiB** |
| `page_size` | 4096 |
| `page_count` | 651 526 → `page_count×page_size` = 2 668 650 496 |
| `journal_mode` | **wal** |
| `auto_vacuum` | **0** (none) |
| `synchronous` | 2 (FULL) |
| `wal_autocheckpoint` | 1000 |
| WAL sidecar | **12 116 952** B ≈ **11.6 MiB** |
| SHM | 32 768 B |
| Volume1 libero | **5.2 T** / 7.3 T (29% used) |

---

## 1 · Anatomia (A1–A3)

### A1 — Peso completo (dbstat, ordinato)

Somma dbstat ≈ file intero. Top contributor (tabella + indici correlati):

| MiB | Tipo | Nome | Note |
|----:|------|------|------|
| **1313.8** | table | `observations_raw` | 768 268 righe · **1793 B/riga** medi |
| **781.3** | table | `observations` | 978 532 righe · **837 B/riga** |
| 61.2 | index | `sqlite_autoindex_observations_raw_1` | UNIQUE dedup (implicito) |
| 61.2 | index | `ix_observations_raw_dedup_key` | **duplicato** del precedente |
| 49.5 | index | `ix_obsraw_entity_ts` | (entity_key, observed_at) |
| 37.5 | index | `ix_observations_seen_at` | seen_at |
| 37.5 | index | `ix_obs_seen` | **duplicato** seen_at |
| 34.4 | index | `ix_obsraw_source_ts` | (source, observed_at) |
| 29.4 | index | `ix_observations_raw_observed_at` | observed_at |
| 27.3 | index | `ix_observations_raw_entity_key` | entity_key (prefisso del composito?) |
| 27.0 | index | `ix_observations_mac` | |
| **21.4** | table | `flow_observations` | 52 446 righe · 427 B/riga |
| 16.8 | index | `ix_observations_ip` | |
| **15.2** | table | `heartbeats` | 74 074 righe · 215 B/riga |
| 11.7 | index | `ix_observations_raw_source` | source (prefisso del composito?) |
| 2.9 | index | `ix_hb_mon_ts` | |
| 2.8 | table | `scan_runs` | 1 261 |
| 2.7 | index | `ix_flow_observations_dedup_key` | |
| 2.3 | table | `sensor_runs` | 7 756 |
| 2.0 | index | `ix_flow_ts` | |
| 1.5 | table | `incidents` | 2 294 |
| 1.4 | table | `ip_intel` | 4 888 |
| 1.3 | table | `events` | 2 661 |
| 0.8 | table | `assets` | 151 |
| … | … | resto | ciascuno ≤ 0.4 MiB |

**Copertura 2.49 GiB:** le due tabelle osservazioni da sole ≈ **2.10 GiB** (84%). Con i loro indici ≈ **2.45 GiB** (~98%). Tutto il resto del sistema è rumore rispetto al file.

Righe complete: vedi dump `_tmp_db_slim_out.txt` (sessione) / sezione INDEXES sotto.

### A2 — Dati vs indici · ridondanze

| | Byte | % file |
|--|-----:|-------:|
| Tabelle (dbstat) | 2 246 447 104 | **84.2%** |
| Indici | 422 146 048 | **15.8%** |
| sqlite_schema | 40 960 | ~0 |

**Indici duplicati evidenti (stessa colonna / stesso UNIQUE):**

| Coppia | MiB ciascuno | Totale sprecabile |
|--------|-------------:|------------------:|
| `sqlite_autoindex_observations_raw_1` + `ix_observations_raw_dedup_key` | 61.2 + 61.2 | **~122 MiB** |
| `ix_observations_seen_at` + `ix_obs_seen` | 37.5 + 37.5 | **~75 MiB** |
| `ix_metric_snapshots_taken_at` + `ix_metric_snapshots_ts` | 4 KiB + 4 KiB | irrilevante |

Causa legacy: modello SQLAlchemy `index=True` su colonna **e** `Index(...)` / Alembic `ix_observations_seen_at` + `ix_obs_seen` in `models.py`. Su raw: `UniqueConstraint(dedup_key)` **e** `unique=True, index=True` su `dedup_key`.

**Possibile ridondanza (non “mai usato”, ma ricopribile dal composito leftmost):**

- `ix_observations_raw_entity_key` (~27 MiB) ⊆ prefisso di `ix_obsraw_entity_ts`
- `ix_observations_raw_source` (~12 MiB) ⊆ prefisso di `ix_obsraw_source_ts`

SQLite non espone “unused index” senza `sqlite_stat` + workload; non c’è telemetria query-plan in produzione. Verdetto: **duplicati certi ~197 MiB**; compositi-prefisso **candidati** ulteriori ~39 MiB.

### A3 — Spazio libero interno (freelist)

```
freelist_count = 3
FREELIST_BYTES = 3 × 4096 = 12 288 B ≈ 12 KiB
```

**VACUUM senza DELETE recupererebbe ~0 del file.** Le pagine sono piene; il file è “compatto” rispetto al contenuto attuale. Per calare su disco servono **DELETE (o drop indici) + VACUUM**.

---

## 2 · Chi scrive (B1–B3)

### B1 — `observations` vs `observations_raw`

#### Writer

| Path | File:riga | Cosa scrive |
|------|-----------|-------------|
| Upsert raw | `observations_store.py:113` `upsert_observation_raw` | unica scrittura raw (ingest v2) |
| Gate dual-write | `materialize.py:275+` `write_and_materialize` | raw sempre; legacy solo se `created=True` (nuovo dedup bucket) |
| Legacy host | `materialize.py:82` → `identity.record_observation:1438` | kind host (fritz/nmap/…) |
| Legacy nmap MAC | `identity.py:408` | nmap con MAC |
| **WLAN-only legacy** | `materialize.py:226` | `fritz_wlan_assoc` / `fritz_mesh` — **mai in raw** |

Dedup raw: `obs_dedup_window_s=60` (`config.py:81`). Collapse → niente nuova riga legacy per lo stesso bucket.

#### Frequenza reale (live)

| Finestra | `observations` | `observations_raw` |
|----------|---------------:|-------------------:|
| 10 min | 1608 → **160.8 /min** | 1197 → **119.7 /min** |
| 60 min | 7818 → **130.3 /min** | 6133 → **102.2 /min** |
| ultime 24h | ~198k (giorno) | **155 268** |

Legacy > raw perché **`fritz_wlan_assoc` non passa dal raw** (~43.8k /24h) + eventuali path storici.

#### Differenza di contenuto (esatta)

| | `observations` (legacy) | `observations_raw` |
|--|-------------------------|---------------------|
| Schema | id, kind, mac, ip, hostname, vendor, payload, scan_run_id, seen_at | id, dedup_key, sensor_id, source, kind, entity_key, observed_at, received_at, first_seen, last_seen, hit_count, confidence, ttl, payload, sensor_run_id |
| Semantica | **append-only** 1 riga / evento materializzato | **upsert** per `dedup_key`; hit_count++ / last_seen |
| Payload medio | ~664 B | ~1195 B (envelope v2 più ricco) |
| Kind/source top | fritz 735k · **fritz_wlan_assoc 214k** · nmap 28k · fritz_mesh 163 | fritz 734k · nmap 28k · ssdp 5k · scan-batch… · printer — **zero wlan_assoc** |
| Span live | 2026-07-17 → 07-24 (~7g) | 2026-07-20 → 07-24 (~5g) |

**Cosa fa la legacy che il raw non fa:** (1) storico association Wi‑Fi (`fritz_wlan_assoc`); (2) evidence table flat MAC/IP/hostname per presence/trust/scans/detectors che ancora interrogano `Observation`; (3) densità temporale più fine (append vs collapse 60s).

### B2 — Altre tabelle pesanti

| Tabella | MiB | Writer | Cadenza | Bound? |
|---------|----:|--------|---------|--------|
| `flow_observations` | 21.4 | `evolution.py` ingest flow / Zeek | oraria (closed hour) | **Sì** — prune 30g in `run_retention` (live: sì) |
| `heartbeats` | 15.2 | `monitoring.py` / internet_health | per check monitor | **Sì** — prune 30g |
| `scan_runs` | 2.8 | scan workflow | per job | **No prune** — cresce lento |
| `sensor_runs` | 2.3 | `observations_store.create_sensor_run` | ogni ciclo provider | **No prune** |
| `incidents` | 1.5 | monitoring | eventi | lifecycle open/resolve; no TTL file |
| `ip_intel` | 1.4 | upsert batch / AI context | rare | bounded da IP unici |
| `events` | 1.3 | identity/trust/… | eventi | no TTL |
| `metric_snapshots` | 0.2 | `reliability_metrics.snapshot_*` | retention-run / job | no prune dedicato |
| `observations_aggregate` | 0 | rollup raw | dopo TTL raw | vuota finché TTL non morde |

### B3 — Retention esistente (job V2)

Collector → `POST /api/ingest/retention-run` orario (`collector/main.py` `_run_retention`).

**Live 0.10.21 — cosa TOCCA:**

| Azione | TTL config | Stato live |
|--------|------------|------------|
| Rollup+delete `observations_raw` | `obs_ttl_raw_days=7` | **no-op**: `raw <7d` = **0** righe |
| Prune `heartbeats` | 30g | no-op (span ~7g) |
| Prune `flow_observations` | 30g | no-op (span ~3g) |

**Live — cosa NON tocca:**

- **`observations` legacy** — `HAS_LEGACY_PRUNE=False` su immagine 0.10.21
- assets, events, sensor_runs, scan_runs, ip_intel, incidents, metric_snapshots, indici
- **nessun VACUUM**

(Branch `feature/obs-deploy-01` aggiunge `prune_legacy_observations` default 3g — **non deployato**.)

#### TTL raw 7g: proiezione a 30 giorni

- Ingest raw ~**155k righe/giorno** (media ultimi giorni; payload ~1.2 KB → ~180–220 MiB/giorno grezzi + indici).
- **Con TTL 7g attivo** (steady state): ≈ `7 × 155k` ≈ **1.09M righe** (oggi 0.77M in 5g → coerente). File raw+indici stabilizza ~**1.8–2.2 GiB** (ordine di grandezza attuale), non esplode.
- **Senza TTL a 30g:** ≈ `30 × 155k` ≈ **4.7M righe** → raw table sola ~**6–8 GiB** + indici ~+25–30%.
- Quando il TTL “morderà” (prima volta ~2026-07-27 se continuo dal 20): delete giornaliero ≈ una giornata di raw → **freelist cresce**, file **non cala** finché non c’è VACUUM.

Legacy senza prune: +~180–210k righe/giorno → a 30g da oggi ordine **+~5–6M** → tabella legacy multi‑GiB.

---

## 3 · Chi legge (C1–C3)

### C1 — Query di lettura e finestra massima

#### `observations` (legacy)

| Consumatore | File:riga | Finestra |
|-------------|-----------|----------|
| Presence | `inventory.py:180–184` `reconcile_asset_presence` | **`ASSET_STALE_AFTER_HOURS` default 24h** |
| Trust backfill portal MIN/MAX | `trust.py:322–344` `_prefetch_portal_first_last_by_mac` | **nessuna** (full history portal kinds) — usata se manca `asset.portal_*` |
| Trust N+1 legacy | `trust.py:386–388`, `666–668` | full history (solo path test / `use_prefetch=False`) |
| Scan targets | `scans.py:82–88` | **`TARGET_MAX_AGE` = 24h** |
| Detector DHCP/DNS | `detectors/__init__.py:86–89` | **24h** |
| Detector noise proto | `detectors/__init__.py:116–119` | **24h** |
| DNS hysteresis | `identity.py:1375–1378` | **1h** |

Nota: presence filtra con `is_portal_evidence` (`trust.py:17–28`) — **fritz / fritz_wlan_assoc non contano** come portal; restano peso su disco ma non sono il pavimento presence.

#### `observations_raw`

| Consumatore | File:riga | Finestra |
|-------------|-----------|----------|
| Fingerprint SSDP | `fingerprint_facts.py:1201–1205` | ultimi **800** per `source=ssdp` (ordine desc; di fatto “recente”) |
| Reliability counts | `reliability_metrics.py` | count totale / sensor window `measure_window_days=14` su SensorRun |
| Retention rollup | `retention.py:43–45` | cutoff TTL |

Nessun reader presence/habits/dossier su raw oggi.

#### Altre candidate

| Tabella | Reader | Finestra max |
|---------|--------|--------------|
| `flow_observations` | `habits.py:313–314` | default **7g**, max **30g** |
| `flow_observations` | `flows_summary.py:182+` | ore (UI), non mesi |
| `heartbeats` | `monitors.py:71–76` | **24h** (history UI) |
| `heartbeats` | `monitoring.py:862–865` flap | `flap_window_minutes` (minuti) |
| `heartbeats` | `monitoring.py:1063` up_ratio | **24h** |
| `sensor_runs` | `dashboard.py:253`, `scan_readiness.py:101` | dashboard **24h**; readiness ultimi N |
| `metric_snapshots` | `dashboard.py` latest | 1 riga |

### C2 — Pavimento retention (verdetto)

| Tabella | Pavimento sicuro sotto cui un consumatore vivo perde dati | Note |
|---------|----------------------------------------------------------|------|
| **`observations`** | **≥ 24h** (presence + scans + detectors) | Trust full-history è **solo backfill** se `portal_first_seen` assente; dopo backfill/observe_portal i campi su `assets` bastano. Pavimento operativo: **24h**; margine consigliato **≥ 3g** (come default branch deploy-01). |
| **`observations_raw`** | **≥ max(TTL usi fingerprint SSDP “recenti”, misura)** | Nessun presence. TTL **7g** già ≥ bisogni noti; scendere sotto ~2–3g rischia solo enrichment SSDP “vecchio”. |
| **`flow_observations`** | **≥ 30g** se habits MAX_DAYS=30 usato in UI | Default habits 7g; API permette 30 → allinea prune 30g. |
| **`heartbeats`** | **≥ 24h** UI; flap minuti | Prune 30g >> pavimento. |
| `sensor_runs` / `scan_runs` | non tagliare in Fase B senza audit | piccoli |

### C3 — Migrare presence sul raw → legacy sola-lettura → DROP?

**Cosa fa la legacy che il raw non fa (oltre lo schema):** alimenta i reader C1; contiene **214k `fritz_wlan_assoc`** assenti dal raw; densità append vs upsert 60s.

**Fattibilità presence → raw (o via asset):**

1. **Via `asset.portal_last_seen` / `observe_portal` (preferibile):** già aggiornati in materialize; `reconcile_asset_presence` già usa portal + FDB + reachability; le Observation portal entro 24h sono **evidenza aggiuntiva**. Migrare presence a “non leggere Observation” è fattibile se si garantisce che ogni source portal aggiorni `portal_*` (già vero per path materialize).
2. **Via raw:** possibile filtrare `observations_raw` per source∈PORTAL_EVIDENCE e `observed_at≥cutoff`, ma entity_key/MAC mapping ≠ colonna `mac` flat — più fragile.
3. **WLAN assoc:** oggi solo legacy + `materialize_wifi_association` su asset.meta.link — per DROP legacy non serve storicizzare le Observation assoc se il link sull’asset resta aggiornato.

**Rischi:** trust backfill full-history se asset senza `portal_first_seen`; scans/detectors ancora su `Observation`; dual-write gate `created` — smettere di scrivere legacy richiede switch esplicito dei reader + periodo shadow. **Non DROP in questa fase.** Percorso naturale: (a) reader → portal fields / raw, (b) stop write legacy, (c) TTL aggressivo / truncate, (d) VACUUM, (e) DROP tabella.

---

## 4 · VACUUM (D1–D3)

### D1 — VACUUM offline sul NAS

| Voce | Stima |
|------|--------|
| Tempo su **2.5 GiB HDD** | ordine **15–40 min** (riscrittura sequenziale ~1–3× dimensione; Seagate md1 non SSD) |
| Spazio transitorio | SQLite VACUUM classico riscrive in-place con journal/temp ≈ **fino a ~+2.5 GiB** peak |
| Libero volume1 | **5.2 T** — **sì, c’è spazio** |
| Downtime | API/collector **stop** obbligatorio (file lock); finestra manutenzione |
| `auto_vacuum` | **0** — niente reclaim automatico post-DELETE |

**Importante:** oggi freelist≈0 → VACUUM **senza** DELETE/DROP indici **non riduce** il file.

### D2 — `VACUUM INTO '…/observatory.db.new'`

- Compatta su file nuovo senza distruggere l’originale finché non si swap-a.
- Fattibile: stop writer → `VACUUM INTO` → verifica integrity → swap path/mount → restart.
- Rischi: dimenticare WAL/SHM vecchi; permessi UID container; brief inconsistenza se writer riparte sul vecchio path; tempo simile al VACUUM pieno + spazio **+2.5 GiB** (qui ok).
- Preferibile al VACUUM in-place per rollback (si tiene il `.db` vecchio finché health OK).

### D3 — page_size / WAL / checkpoint

| | |
|--|--|
| `page_size` | 4096 (ok; cambiare richiede VACUUM e non è priorità) |
| WAL attuale | **~11.6 MiB** |
| Checkpoint aggressivo | recupera **al più ~11 MiB** subito — irrilevante vs 2.5 GiB |
| Dopo DELETE massivi | WAL/freelist crescono; solo VACUUM (o vacuum into) stringe il file |

---

## Sintesi per le fasi successive (non eseguire ora)

1. **~98% del file** = `observations_raw` + `observations` + i loro indici.
2. **Freelist nulla** → prune senza VACUUM = file invariato su disco.
3. **Duplicati indici certi ~197 MiB** recuperabili con DROP INDEX + VACUUM (basso rischio, fuori scope Fase A).
4. **Pavimento TTL:** legacy **≥24h** (consigliato 3g); raw **7g** già allineato; flows **30g**; heartbeats **30g**.
5. **Live 0.10.21:** raw TTL ancora no-op; **legacy non prunata**; wlan_assoc solo legacy.
6. **Presence→DROP legacy:** fattibile via campi asset + stop dual-write, non via “solo raw” ingenuo; richiede migrazione reader scans/detectors/trust.

Prossimi tagli da progettare in review: TTL legacy calibrato su C2, dedupe indici, migra-presence, poi **VACUUM INTO** in manutenzione.

---

*Metodo: `CREATE VIRTUAL TABLE temp.stat USING dbstat` in container `api`; PRAGMA; COUNT/AVG; grep writer/reader nel repo `observatory/` (branch lavoro + live 0.10.21 dove indicato).*
