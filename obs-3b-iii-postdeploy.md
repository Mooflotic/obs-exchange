# OBS-DB-SLIM 3b-iii — post-deploy 0.10.27

**Branch:** `feature/obs-db-slim` · **Live:** 0.10.27 · **Data:** 2026-07-25  
**STOP:** PASSO 6 = **deriva** (B2). Reset calibrazione **non** eseguito. 4b non iniziato.

---

## Decisione PASSO 1 — epoch calibrazione: **RIMUOVI e RIMANDA**

### Q1–Q5 (evidenza codice)

| Q | Risposta |
|---|----------|
| **Q1** | **Sì.** Day-clock = `min(MIN(MetricSnapshot.taken_at), MIN(SensorRun.started_at))` in `build_calibration_status` (`reliability_metrics.py`). |
| **Q2** | **Sì.** Azzerarlo senza epoch richiede DELETE/TRUNCATE di `sensor_runs` (dati reali; 8637+ righe live) e/o snapshot. |
| **Q3** | Proposta: `settings` key `calibration_started_at` JSON `{"at":…}` — campo esistente, **nessuna** migrazione Alembic. |
| **Q4** | Con epoch assente la proposta **ricadeva** su SensorRun/snapshot → day **plausibile** (es. 6/14). **Non** dichiarazione di indisponibilità. |
| **Q5** | `SCORING_CALIBRATED` è **solo env** (`settings.scoring_calibrated`). Findings/drift leggono quel flag (`findings.py`, `drift.py`), **non** il day-clock. Completare i 14 giorni UI non accende lo scoring. |

### K1–K5

| K | Esito |
|---|--------|
| K1 Q2=Sì | **PASS** |
| K2 campo esistente | **PASS** |
| K3 epoch assente → indisponibilità esplicita | **FAIL** (numero plausibile = barra muta) |
| K4 solo day-clock | non valutato (K3 già falsa) |
| K5 non accende scoring | **PASS** (env only) |

**Decisione:** RIMUOVI. `reliability_metrics.py` ripristinato a `1f1775f`. Script deferito in `docs/_deferred/reset_calibration_once.py.deferred`. Aperto **DEBT-CALIB-EPOCH**. Diff pubblicato: [obs-3b-iii-calib.diff.txt](https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-3b-iii-calib.diff.txt).

**4 righe spostate** (path day-clock unconditional → else): `first_snapshot` / `first_sensor` / `candidates` / `started_at=min(...)` — calcolavano l’ancora day-clock da MetricSnapshot+SensorRun.

PASSO 7 reset: **saltato** (non fallimento deploy).

---

## Preflight (PASSO 4)

| Voce | Valore |
|------|--------|
| health | 0.10.26 proxy+diretto · servizi healthy |
| DB | 2854432768 B · WAL 9294752 B |
| libero /volume1 | 5703005077504 B |
| observations | 1066959 |
| asset / ip_current | 151 / 99 |
| structural log | 53 (boot 13:21) |

---

## A1–A13 osservato vs previsto

| # | Previsto | Osservato | Esito |
|---|----------|-----------|--------|
| **A1** | health 0.10.27 | proxy+diretto `0.10.27` | **PASS** |
| **A2 F1** | T_prefetch_obs null/assente | `"T_prefetch_obs":{"s":null}` | **PASS** |
| **A3 F2** | T_dry_run &lt; 2 s | **0.086 s** (prosa 0.1s) | **PASS** |
| **A4** | Δ obs/10min = 0 | T0=**1067155** T1=**1067155** Δ=**0** | **PASS** |
| **A5** | 0 evidence reads | codice 3b-iii + dual-write off; retention DELETE/COUNT ammessa | **PASS** |
| **A6** | scans 67 id = preflight | **67**, insieme identico | **PASS** |
| **A7** | AD ⊇63, atteso 82 | **82**, A\B=∅, = expected 82 | **PASS** |
| **A8** | 151 / 99 | **151 / 99** | **PASS** |
| **A9** | structural ~53, &gt;100 STOP | boot1 **structural=53** | **PASS** |
| **A10** | T_backup ≈ invariato | **155.3 s** vs baseline 307.9 s — **ANOMALIA** | vedi sotto |
| **A11 F3** | guadagno ~15–25 s su ~348 | T_total **174.1 s** (needs_apply=true) vs 347.9; intervallo non usabile come metro (A10 confonde) | indicativo |
| **A12 F4** | stesso needs_apply | entrambi boot `needs_apply=true` `needs_backup=true` | ok |
| **A13** | throughput serie | pre-deploy 2854445056 B @14:51; trust 2855002112 B @14:52 T_backup=155.3 → **18.38 MB/s**; deploy wall **INFERITO** ~108 s | aggiornato |

### A10 anomalia (non usata per bloccare A1–A9)

T_backup dimezzato con file ancora caldo dopo snapshot deploy (14:50→14:52). Allineato a **DEBT-BACKUP-ASYMMETRY** (varianza throughput già nota). Non è guadagno funzionale di 3b-iii.

### Cross-check JSON ↔ prosa (boot 1)

| | JSON | prosa |
|--|------|-------|
| dry_run | 0.086 | 0.1s |
| backup | 155.3 | 155.3s |
| apply | 3.648 | 3.6s |
| structural | (report) | 53 |

**Coerenti** (arrotondamento prosa).

---

## PASSO 6 — convergenza: **FAIL (B2 deriva)**

| Boot | structural | timestamp_refresh | needs_apply | T_backup |
|------|------------|-------------------|-------------|----------|
| 1° (deploy) | **53** | 5 | true | 155.3 s |
| 2° (restart) | **53** | 0 | true | 129.3 s |

**Atteso:** structural 2° ≪ 1°. **Osservato:** identico ordine (53=53) → **non convergenza, deriva**.

### Scomposizione structural (dry_run post-boot2, n=53)

| level (piano) | expected_state | n | esempio asset_id |
|---------------|----------------|---|------------------|
| fritz_historical | fritz_historical | 24 | 83,84,86,… |
| known | active | 23 | 71,80,81,87,… |
| stale_unlocated | stale_unlocated | 6 | … |

Pattern tipico (sample): `trust_level=known`, `operational_state=stale_unlocated`, `inventory_hidden_auto=True`.  
Apply trust *dovrebbe* riportare `operational_state=active` se `inventory_hidden_auto` e level∈{known,confirmed_present}, ma al boot successivo lo stato è di nuovo mismatch — **ipotesi guida:** `reconcile_asset_presence` (collector) re-marca `stale_unlocated` dopo l’apply bootstrap → oscillazione. **Non fixato in produzione (B2 STOP).**

**Stato scritto già presente:** apply ha eseguito su entrambi i boot (trust_level/portal_*). Rollback codice ≠ undo scritture.

**PASSO 7:** non eseguito (RIMANDA + B2).

---

## Insiemi funzionali

| | Baseline / atteso | Post-deploy |
|--|-------------------|-------------|
| AD | 82 (63+19) | **82** id identici |
| scans | 67 | **67** id identici |
| asset / ip | 151 / 99 | 151 / 99 |

---

## Serie throughput (DEBT-BACKUP-ASYMMETRY)

| Punto | Size B | T_backup s | MB/s | Note |
|-------|--------|------------|------|------|
| storico | … | … | 10.37 → 9.22 → 9.15 | trust |
| 2026-07-25 14:52 | 2855002112 | 155.3 | **18.38** | post-snapshot caldo; ANOMALIA |
| pre-deploy 14:51 | 2854445056 | (wall deploy INFERITO ≤108 s) | ≥~26 MB/s INFERITO | |

---

## Chiusura 3b-iii

- Dual-write spento · prefetch Observation eliminato · AD/DNS/detectors stub · GATE R1 extent documentato  
- **Aperto:** deriva structural trust↔inventory (B2) — debt da aprire se non già coperto  
- **Rinviato:** DEBT-CALIB-EPOCH  
- **Congelato:** 4b / DROP / retention DELETE·COUNT blocker  
- **Prossimo:** diagnosi ballooning §13 nella finestra di drenaggio legacy (~0 righe ~2026-08-01)

**3b-iii chiuso con riserva B2** (deploy 0.10.27 in live; convergenza apply non dimostrata).
