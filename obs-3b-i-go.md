# OBS-3b-i-go — verifica semantica + GO 0.10.25

**Data:** 2026-07-25 · **Branch merge:** `feature/obs-db-slim` → `main` (no-squash) · **Tag:** `v0.10.25`  
**Live:** `/api/health` → `0.10.25`

---

## Parte 1 · Granularità per-IP → per-asset (sola lettura)

Census live pre-GO (stesso algoritmo old vs new di `obs-3b-i`):

| | Asset | IP rows |
|--|------:|--------:|
| OLD (Observation + IpAddress portal) | 62 | 62 |
| NEW (presence_sources + IpAddress portal) | 67 | 67 |
| Delta | **+5** | +5 |

(I numeri assoluti sono saliti rispetto al report notturno 60→65; il **+5** è lo stesso insieme di asset.)

### 1a · Classificazione dei +5

**Tutti e 5 = (i) effetto voluto sticky.** Nessuno = (ii) collaterale multi-IP.

| asset_id | Nome | IP current | `IpAddress.source` | presence portal | Obs portal su IP | Classe |
|---------:|------|------------|--------------------|-----------------|------------------|--------|
| **5** | Cassiopea — NIC 1 | 192.168.1.3 | fritz | fdb (+ nmap stale) | no | **(i)** mono-IP sticky |
| **6** | Cassiopea — NIC 2 | 192.168.3.24 | fritz (role secondario) | fdb | no | **(i)** mono-IP sticky |
| **70** | AppleTV-5 | 192.168.2.193 | fritz | fdb | no | **(i)** mono-IP sticky |
| **85** | (anonimo) | 192.168.2.85 | fritz | fdb | no | **(i)** mono-IP sticky |
| **98** | (anonimo) | 192.168.2.88 | fritz | fdb | no | **(i)** mono-IP sticky |

Nessuno dei +5 ha `n_current_ips > 1`.

### 1b · Insieme cambio semantica multi-IP

**VUOTO (0).**

Nessun asset multi-IP ha un IP current che col vecchio codice non avrebbe qualificato e che ora qualifica.

Contesto: live ha essenzialmente **0 device multi-IP distinti** (solo LGS328C con lo stesso IP su due interfacce). Quindi la nuova granularità per-asset non ha ancora un terreno dove divergere.

### 1c · Rischio

**Nessun rischio reale da 1b** (insieme vuoto).  
Esempi non applicabili. La migrazione resta equivalente sul parco attuale: i +5 sono recovery sticky, non allargamento multi-binding.

**Decisione 2a:** 1b vuoto → **pienamente equivalente** → GO senza KNOWN_DEBT.

---

## Parte 2 · GO eseguito

### 2a/2b

- KNOWN_DEBT **non** aggiunto (1b vuoto; niente eccezione 1c).
- Procedura **2c**.

### 2c · Deploy

| Step | Esito |
|------|-------|
| Merge no-squash `feature/obs-db-slim` → `main` | `14fc060` |
| Push `main` + tag `v0.10.25` | ok |
| Bump VERSION / CHANGELOG / web package | **0.10.25** |
| `./scripts/deploy.sh api web` | ok (snapshot `pre-deploy-20260725-0934.db`) |

### Assert post-deploy

| Check | Previsto | Osservato | |
|-------|----------|-----------|---|
| `/api/health` version | 0.10.25 | `{"ok":true,"version":"0.10.25"}` | OK |
| Asset serviti da scans | ≥62, tipicamente 67 | **67** asset / **67** IP | OK (+5 vs old 62) |
| Sticky case asset 5 | servito con source fritz + portal fdb | `sources=['fdb','fritz']`, map `{'192.168.1.3':['fdb']}` | OK |
| PLUS5 {5,6,70,85,98} | tutti serviti | **True** | OK |
| `active_discovery` | ancora su Observation | sì (`inventory.py`) | OK invariato |
| DNS hysteresis | ancora su Observation dns | sì (`identity.py`) | OK invariato |
| scans legge Observation a runtime | no | solo docstring «Does not read Observation legacy»; nessun import/query | OK |
| dual-write host | acceso | `record_observation` + `record_legacy` presenti in `materialize.py` | OK |

Nessun assert divergente → **nessun fix in produzione**.

---

## STOP

3b-i **chiuso in live 0.10.25**. Prossimo cantiere DB-SLIM: active_discovery / DNS dopo calib, oppure 3b-iii stop dual-write host quando i reader restanti saranno migrati.
