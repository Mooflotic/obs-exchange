# OBS-COERENZA — chiusura tecnica post-4b

**Live:** 0.10.30 · **main = tag = produzione:** `9003f417a31f2fe25e06dc9a52d24068b7d9b666` (`v0.10.30`) · **Data:** 2026-07-25

---

## GATE 1 — invariante 1

| Evidenza | Valore |
|----------|--------|
| `main` HEAD | `9003f41` |
| `v0.10.30` | `9003f41` (annotated → stesso commit) |
| `/VERSION` host + container | `0.10.30` |
| `GET /api/health` | `version":"0.10.30"` |
| Tree | pulito al tag (report docs sotto) |

**Merge:** `feature/obs-db-slim` → `main` (fast-forward merge `83dac7b`, 24 commit, **0 conflitti**).  
**Tag policy (1.3):** `v0.10.29` resta su **6589e15** (solo codice VERSION); docs `8de356a` fuori tag. **Tag futuri = commit di bump VERSION.** Coerente: `v0.10.30` = bump+codice.

Pre-merge: main era **24 commit** dietro slim; solo ahead = 0.

---

## FASE 2 — data/backups

### 2.1 Misura (2026-07-25 ~16:45, pre-deploy 0.10.30)

| | Byte | File |
|--|-----:|-----:|
| **Totale** | **20 710 430 909** | **33** |
| Inizio sessione (riferimento) | 18 924 423 357 | 7 |
| **Δ sessione** | **+1 786 007 552** (~+1.66 GiB) | **+26** |

Per prefisso (pre-deploy 0.10.30):

| Prefisso | n | Byte |
|----------|--:|-----:|
| pre-deploy | 3 | 8 586 362 880 |
| observatory | 3 | 6 572 019 712 |
| pre-4b-drop | 1 (+sidecars) | 2 873 335 808 |
| pre-db-slim-p1 | 1 | 2 676 768 768 |
| snapshot | 20 | 1 910 701 |
| recheck / other | 3 | ~272 |

### 2.2 Perché 32→33

| Prefisso | Creatore | Rotazione pre-0.10.30 |
|----------|----------|------------------------|
| `pre-deploy-*` | `deploy.sh` | keep-3 **solo** in deploy.sh |
| `observatory-*` | `create_backup` (trust/admin) | keep-3 in `backup.py` |
| `snapshot-*` | `create_backup` JSON | keep-20 |
| `pre-4b-drop-*` | op 4b manuale | **nessuna** |
| `pre-db-slim-p1-*` | script cantiere | **nessuna** |

`DEBT-BACKUP-ROTATION-SPLIT` confermato sui dati: keep-3 deploy solo su `pre-deploy-*`; `observatory-*` ruotati solo quando gira `create_backup`.

### 2.3–2.4 Politica unificata + dry-run

Punto unico: `api/app/services/backup_rotate_core.py` + CLI `scripts/backup_rotate.py`; `deploy.sh` chiama `--apply` **dopo** rsync.

Protetti (mai unlink, per nome):
- `pre-4b-drop-20260725-161330.db`
- `observatory-pre4b.bak`

**Dry-run pre-attivazione (as-is):** nessuna cancellazione.  
**Dry-run simulando +1 pre-deploy:** cancellerebbe solo  
`pre-deploy-20260725-1450.db` · **2 854 445 056 B** · mtime 2026-07-25 14:51.

### 2.5 Bilancio netto sessione (onesto)

| Voce | Byte |
|------|-----:|
| DB liberato (4b Δ file) | **−1 024 389 216** (~−0.95 GiB) |
| Backup Δ vs inizio sessione | **+1 786 007 552** |
| **Netto disco sessione** | **+761 618 336** (~**+0.71 GiB**) |

Dopo rotazione 0.10.30 (−2.85 GiB del pre-deploy vecchio) il netto migliora; vedi E9.

---

## FASE 3 — prune raw

### 3.1 Codice (sola lettura)

- TTL effettivo: `OBS_TTL_RAW_DAYS` default **7**; cutoff = `now − ttl`.
- Rollup: SELECT `observations_raw` con `observed_at < cutoff` → bucket `(source, window)` → upsert `observations_aggregate` → DELETE stesse righe.
- Heartbeats / flow: DELETE diretto con TTL dedicati (30g default).
- Legacy: param ignorato (4b).

### 3.2 Extent live

| | |
|--|--|
| min `observed_at` | 2026-07-20 01:12:46 |
| max | 2026-07-25 14:46:21 |
| righe | ~868 846 → 869 687 (ingest) |

Giorni: 20→173 530, 21→127 571, 22→156 057, 23→167 197, 24→153 502, 25→~91 k.

**Primo prune a volumi pieni:** quando cutoff supera il 20 → **~2026-07-27**.

### 3.3 Predizione (scritta ORA, falsificabile)

Al primo prune efficace (~2026-07-27): circa **173 530** righe (giornata 20) cancellate; freelist attesa ≈ **0.30–0.37 GiB** (≈1790 B/riga tabella + quota indici). Verificare via `store` in retention-run.

### 3.4 Osservazione

`POST /api/ingest/retention-run` ora espone `store.before/after` (`db_bytes`, `freelist_*`) e log  
`[retention] raw_deleted=… db_bytes … freelist_bytes …`.

### 3.5

TTL non modificato; nessun prune artificiale.

---

## FASE 4 — decisioni

| # | Decisione | Motivazione |
|---|-----------|-------------|
| 4.1 AUTOVACUUM | **Accettato** `auto_vacuum=0` | Freelist live = 1–2 pagine; riuso insert. **Cambio idea se** freelist **> 256 MiB** per **≥ 7 giorni** a regime prune. |
| 4.2 ALEMBIC | Migrazione `l2c3d4e5f6a7` `DROP TABLE IF EXISTS` | Idempotente. Live: entrypoint **non** esegue alembic (create_all senza modello → tabella assente, E3). Migration serve install alembic-from-baseline. |
| 4.3 CALIB | Epoch in `settings.calibration_started_at`; assente → `available=false` `day=null` | K3 rispettato. Reset eseguito: day **1/14**. Snapshot `pre-calib-reset-20260725-165514.db` integrity ok. |
| 4.4 Detector | **(a) rimossi dal registro** | Abilitarli impossibile; assenza = fatto. (b) rimandato. |
| 4.5 | Aperto **DEBT-BACKUP-ALL-OR-NOTHING** | Una structural → copia 1.85 GiB / 133 s. |
| 4.6 | Residuo ~28 MB in `obs-4b-postop.md` | Deframmentazione VACUUM. |

---

## E1–E9 osservato vs previsto

| ID | Previsto | Osservato | Esito |
|----|----------|-----------|-------|
| E1 | health 0.10.30 proxy+diretto | 200 / 200 · 0.10.30 | **PASS** |
| E2 | regime ~9 s, needs_apply=false, T_backup=0 | boot1 structural T_total=90.5s; **regime T_total=8.926s**, needs_apply=false, T_backup=0 | **PASS** |
| E3 | observations assente | sqlite_master=0 | **PASS** |
| E4 | assets 151, proposals 412, iface 158, flow 69794, snapshots 122; raw cresce | 151 / 412 / 158 / 69794 / 122; raw **869 687**; sensor_runs 8838; events 3045 (churn) | **PASS** |
| E5 | retention leggibile | ok + `store` freelist; log `[retention]`; deleted=0 (TTL) | **PASS** |
| E6 | delete = dry-run; protetti ok | **ROTATE_DEL** `pre-deploy-20260725-1450.db` 2854445056 (= dry-run); protetti presenti | **PASS** |
| E7 | day 1/14 o indisponibile | pre-reset: available=false day=null; post-reset: **day=1/14** | **PASS** |
| E8 | 82/66/151/98 | **82 / 68 / 151 / 100** — +2 scan eligible, +2 ip_current (churn presence, non regressione) | **PASS*** |
| E9 | size DB + backups | DB **1 868 652 544**; backups **20 591 564 989** (36 file, post-rotate −2.85 GiB + snap calib/pre-deploy) | **PASS** |

\*Scostamento E8 spiegato: IP tornati `is_current` su asset prima esclusi (inverso del churn Sky/43).

---

## Predizione prune (riassunto falsificabile)

| Campo | Valore |
|-------|--------|
| Data attesa primo prune pieno | ~2026-07-27 |
| Righe attese | ~173 530 |
| Freelist attesa | ~0.30–0.37 GiB |

STOP. Cantieri successivi (backlog portale → grafica → hot/cold) uno alla volta dopo review.
