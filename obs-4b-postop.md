# OBS-DB-SLIM 4b — post-operazione (DROP + VACUUM)

**Live:** 0.10.29 · **Branch:** `feature/obs-db-slim` · **Tag:** `v0.10.29` · **Data:** 2026-07-25  
**Finestra DB:** 2026-07-25 ~16:16–16:23 Europe/Rome

---

## Previsioni P1–P6 (scritte prima; non modificate)

| ID | Previsto | Osservato | Esito |
|----|----------|-----------|-------|
| P1 | freelist post-DROP ≈ 998 000 000 B | **995 205 120 B** (242 970 × 4096) | PASS (~−0.3%) |
| P2 | file post-VACUUM ≈ (size − 0.93 GiB) ± 5% | prima **2 873 942 016**; slim **1 849 548 800**; banda [1 782 144 915, 1 969 739 117] | PASS |
| P3 | integrity ok; conteggi superstiti identici | integrity slim **ok**; gate ricalcolato a writer fermi: tutti OK | PASS* |
| P4 | `observations_raw` COUNT esatto | **865 759 = 865 759** | PASS |
| P5 | downtime 5–12 min | **~7 min** (stop collector/api → api healthy post-swap) | PASS |
| P6 | primo boot: `observations` non ricreata | `sqlite_master` count=**0** | PASS |

\*Gate automatico 2.7 aveva FAIL su `heartbeats` 85592→85594: **falso positivo** — conteggio 2.2 fatto con writer ancora attivi. Ricalcolo a servizi fermi: orig=slim su tutte le tabelle. Scelta: procedere allo swap (nessuna corruzione; originale post-DROP intatto fino allo swap). Documentato sotto.

---

## Snapshot e size

| Artefatto | Path | Byte |
|-----------|------|------|
| Snapshot dedicato pre-op | `data/backups/pre-4b-drop-20260725-161330.db` | 2 873 335 808 |
| Integrity snap (RO) | — | **ok** |
| DB prima (2.2) | `data/db/observatory.db` | 2 873 942 016 |
| WAL prima | | 7 156 472 |
| Libero `/volume1` | | 5 699 476 918 272 |
| Freelist post-DROP | | 995 205 120 |
| Slim (VACUUM INTO) | `observatory-slim.db` → poi live | 1 849 548 800 |
| `.bak` post-swap | `data/db/observatory-pre4b.bak` | 2 873 950 208 |
| Live post-boot (cresce con raw) | `observatory.db` | ~1 85x MB |

Nota: `observatory-pre4b.bak` è il file **post-DROP** (freelist, **senza** tabella `observations`). Il restore «pre-DROP con legacy» è lo snapshot `pre-4b-drop-*.db` (`SNAP_has_observations=1`, integrity **ok**).

---

## Conteggi 2.2 (lista di controllo P3)

Valori «prima» = post-stop truth (heartbeats aggiornato da 85592→**85594** dopo checkpoint).  
«Dopo slim» = gate 2.7 ricalcolato. «Live post» = dopo riavvio collector (churn atteso su heartbeats/raw).

| Tabella | Prima (stop) | Dopo slim | Live post-op |
|---------|-------------:|----------:|-------------:|
| observations | 1 067 155 (poi DROPPATA) | — | **assente** |
| observations_raw | 865 759 | 865 759 | 866 666+ (ingest ripreso) |
| assets | 151 | 151 | 151 |
| name_proposals | 412 | 412 | 412 |
| ip_addresses | 118 | 118 | 118 |
| interfaces | 158 | 158 | 158 |
| flow_observations | 69 794 | 69 794 | 69 794 |
| heartbeats | 85 594 | 85 594 | 85 703+ |
| sensor_runs | 8 798 | 8 798 | 8 798 |
| metric_snapshots | 122 | 122 | 122 |
| events | 3 032 | 3 032 | 3 032 |
| switch_ports | 46 | 46 | 46 |
| findings | 0 | 0 | 0 |
| portal_last non-null (asset) | 103 | — | — |
| presence_sources non-vuoti | 148 | — | — |

---

## Durate passi

| Passo | Durata |
|-------|--------|
| 2.1 snapshot + integrity | ~1.5 min (integrity snap ~84 s) |
| 2.3 stop collector→api | ~few s |
| 2.4 wal_checkpoint(TRUNCATE) | istantaneo → wal=0 |
| 2.5 DROP | ~1–2 min (freelist) |
| 2.6 VACUUM INTO | **34.692 s** |
| 2.7 integrity slim + counts | ~80 s |
| 2.8–2.10 swap + api healthy | **156 s** restart api |
| **Downtime writer** | **~7 min** |

---

## Gate 2.7

1. Prima corsa: FAIL `heartbeats` (+2) → **nessuno swap**.
2. Diagnosi: conteggio pre-stop; a writer fermi orig≡slim.
3. Decisione: **GATE_RECHECK PASS** → swap eseguito.
4. Integrity slim: **ok**. `observations` assente nello slim.

---

## Assert A1–A10

| ID | Criterio | Esito | Note |
|----|----------|-------|------|
| A1 | health 0.10.29 proxy+diretto | **PASS** | `/api/health` → 200 entrambi |
| A2 | size vs P2 | **PASS** | Δ ≈ 1.024 GiB liberati sul file |
| A3 | conteggi 2.2; raw esatto al gate | **PASS** | post-op heartbeats/raw crescono (collector) |
| A4 | `observations` assente dopo boot | **PASS** | sqlite_master=0 |
| A5 | boot regime ~9 s, needs_apply=false, T_backup=0 | **PASS** | boot1 post-swap: apply structural=1 (asset 116 meta) + T_backup=133 s; **boot regime** T_total=**8.817 s**, needs_apply=false, T_backup=0 |
| A6 | retention pota raw senza eccezioni | **PASS** | `POST /api/ingest/retention-run`: ok; `observations: null`; `deleted=0` (entro TTL 7g); nessun raise |
| A7 | AD/scans/asset/ip_current | **PASS** | AD(**confirmed_present**)=**82**, scans(eligible)=**66**, assets=**151**, ip_current=**98**. Asset 43 Sky: IP `192.168.2.101` `is_current=0` (churn già noto D5) |
| A8 | T_prefetch_obs null; T_dry_run &lt; 2 s | **PASS** | null; 0.088 s |
| A9 | T_backup su file più piccolo + serie | **PASS** | post-swap structural backup: 1 849 548 800 B / 133.238 s ≈ **13.88 MB/s**. Serie: 10.37 → 9.22 → 9.15 → 18.38 → 17.3 → **13.88**. Regime: T_backup=0 |
| A10 | nessun delete in `data/backups`; `.bak` leggibile | **PASS** | snap pre-4b presente; bak integrity **ok** (107.5 s); backup_count=32 |

---

## Rollback verificato (disponibile)

`.bak` integrity_check (sola lettura) = **ok** prima di dichiararlo disponibile.

```bash
cd /volume1/Docker/observatory
sudo docker compose stop collector api
mv data/db/observatory.db data/db/observatory-slim-failed.db
mv data/db/observatory-pre4b.bak data/db/observatory.db
sudo docker compose start api
sudo docker compose start collector
```

Restore **con** tabella `observations` (solo emergenza dati storici): usare `data/backups/pre-4b-drop-20260725-161330.db` (integrity ok; ha `observations`). Non cancellare né `.bak` né lo snapshot in questo cantiere.

---

## Debiti

| Debito | Stato |
|--------|-------|
| DEBT-RETENTION-LEGACY-DROP-BLOCKER | **CHIUSA** (A6) |
| DEBT-ORM-MODEL-RECREATES-TABLE | **CHIUSA** (A4) |
| DEBT-ALEMBIC-BASELINE-LEGACY-TABLE | **APERTA** |
| DEBT-AUTOVACUUM-NOT-SET | **APERTA** — `PRAGMA auto_vacuum` resta **0** dopo `INCREMENTAL` senza secondo VACUUM full |

---

## Hot/cold (§11)

Con legacy droppata non esiste più store storico oltre i **7 giorni di `observations_raw`** + i backup.  
Obiettivo hot/cold **APERTO**, non ostacolato: stato caldo (`presence_sources`, `portal_*`) resta piccolo. **Non implementato in 4b.**
