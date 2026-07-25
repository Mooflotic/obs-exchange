# OBS-DB-SLIM 3b-iii — baseline pre-spegnimento (PASSO 1)

**Host:** Cassiopea · live al momento della misura: **0.10.26**  
**Branch:** `feature/obs-db-slim` · target VERSION: **0.10.27**  
**Misura T0:** 2026-07-25T11:33:37Z · **T1:** +10 min

## 1.1 Dual-write baseline (assert 8.6)

| Istante | `COUNT(*)` su `observations` |
|---------|------------------------------|
| T0 | **1 056 265** |
| T1 (+10 min) | **1 057 730** |
| **Δ 10 min** | **+1 465** |

Questo Δ è il metro per l’assert post-deploy «nuove righe / 10 min = 0». Non usare il vecchio «~1700».

## 1.2 Censimento tabella / file

| Voce | Valore |
|------|--------|
| Righe totali `observations` (T0) | **1 056 265** |
| Righe `seen_at` > 7g (`OBS_LT7D`) | **0** (tutte within 7d) |
| Size DB (byte) | **2 819 690 496** (sessione passo 1) |
| Size WAL (byte) | **7 556 112** |

## 1.3 Insiemi asset (liste)

### `active_discovery` = True (logica legacy Observation@MAC, 24h portal) — **63** id

```
[1, 2, 3, 4, 9, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]
```

### `scans` candidati (già su `presence_sources` da 3b-i) — **67** id

```
[1, 2, 3, 4, 5, 6, 9, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 85, 98]
```

## Verifica semantica PASSO 3 (pre-deploy, logica nuova vs 1.3)

Logica nuova AD: `presence_sources` portal kinds freschi &lt;24h (stesso pattern scans).

| Confronto | Esito |
|-----------|--------|
| A \ B (legacy − nuovo) | **[]** — nessun asset perso (GATE A\B=0) |
| B \ A (nuovo − legacy) | **19** id: `5,6,7,8,10,70,82,85,88,98,112,135,136,137,140,145,148,149,151` |
| Multi-IP nel delta | **[]** — nessun STOP |

**Scomposizione B\A (ogni id):** tutti e 19 hanno `presence_sources["fdb"]` fresco; **nessuno** ha Observation portal by-MAC nelle 24h (`legacy_obs_portal_24h=false`). Cause tipiche:

- FDB scritto via `observe_portal("fdb")` → `presence_sources`, mentre la legacy AD leggeva solo `Observation` by MAC (kind fdb assente o non linkato).
- In `reconcile_asset_presence`, FDB recente entrava già in `physical_reasons` (`SwitchPort.last_fdb_at`); il booleano `active_discovery` diventa True in più, ma `reliable` era già spesso True.

Scans: insieme 1.3 invariato dalla migrazione AD (già su presence_sources).

## Previsioni post-deploy (dichiarate PRIMA del GO)

| # | Assert | Previsto |
|---|--------|----------|
| 8.1 | health | **0.10.27** |
| 8.2 F1 | `T_prefetch_obs` | **assente o `null`** (non ≈0) |
| 8.3 F2 | `T_dry_run` | **&lt; 2 s** |
| 8.4 | `T_backup` | ≈ invariato (4b non fatto); calo = ANOMALIA |
| 8.5 | letture runtime evidence | **0** |
| 8.6 | Δ `observations` / 10 min | **0** (vs baseline **+1465**) |
| 8.7 | AD / scans | AD: set post = presence_sources (A\B=0 + B\A documentato); scans = lista 1.3 |
| 8.8 F3 | guadagno `T_total` | intervallo ~**15–25 s** su ~348 s (indicativo) |
| 8.9 F4 | confronti | solo stesso `needs_apply` |
| 8.10 | throughput backup | solo osservazione → DEBT-BACKUP-ASYMMETRY |
