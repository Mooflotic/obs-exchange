# OBS-3b-iii-prefetch — baseline avvio + ricognizione trust prefetch

**Data:** 2026-07-25 · **Live:** 0.10.25 · **Scope:** sola lettura  
**STOP:** nessuna modifica · nessuno spegnimento · nessun deploy

---

## Parte 0 · Pulizia tree

Commit `856ecc4` — `docs: report sessione OBS-DB-SLIM`  
File versionati: `obs-4a-plan.md`, `obs-3b-iii-recon.md` (già su obs-exchange).  
`git status` pulito su `main` (allineato a origin dopo push).

---

## Parte 1 · BASELINE 0.10.25 (numeri reali)

Fonte: deploy api+web del 2026-07-25 (tag `v0.10.25`), log timestampati container `observatory-api-1`.

### 1a · Bootstrap API (container start → health)

| Evento | UTC | Δ da start |
|--------|-----|------------|
| Container `StartedAt` | 07:36:09.413Z | 0 |
| `[bootstrap] step 1 schema` (0.3s) | 07:36:15.194Z | +5.8 s |
| `trust dry_run` **35.1s** (prefetch) | 07:36:50.416Z | +41.0 s |
| `trust backup` **198.0s** | 07:40:08.452Z | +239.0 s |
| `trust apply` 1.8s · `step 8 trust` **234.9s** | 07:40:10.282Z | +240.9 s |
| steps 9–11 (monitor/nic2/chassis) | ~07:40:11 | +242 s |
| `Application startup complete` / Uvicorn | 07:40:16.379Z | **+247 s** |
| **Primo `GET /api/health` 200** | 07:40:44.870Z | **+275 s (~4.6 min)** |

Scomposizione step 8 trust (234.9s):

| Sottofase | Tempo | % dello step trust | % fino a Uvicorn (~247s) |
|-----------|------:|-------------------:|-------------------------:|
| **dry_run = prefetch + piano** | **35.1 s** | 15% | **14%** |
| backup SQLite (structural apply) | **198.0 s** | 84% | **80%** |
| apply piano | 1.8 s | &lt;1% | &lt;1% |
| steps 1–7 + 9–11 | ~7 s | — | ~3% |

**Peso prefetch Observation:** **35.1 s** certi (mode=prefetch, queries=200).  
Il collo di bottiglia dell’avvio con apply strutturale è il **backup 198 s**, non il prefetch. Eliminare/migrare il prefetch taglia ~35 s; eliminare backup non necessari (già saltato se solo timestamp_refresh) taglia di più quando `needs_backup=false`.

### 1b · Deploy api completo (fasi)

Deploy `./scripts/deploy.sh api web` (wall agent ≈ **128 s** fino a `deploy ok` = container avviati, **non** healthy).

| Fase | Misura | Tempo |
|------|--------|------:|
| **1. Snapshot** pre-deploy | file `pre-deploy-20260725-0934.db` mtime 09:34:30 CEST; proxy `sqlite3.backup` stesso volume oggi **32.7 s** | **~33–60 s** |
| **2. rsync + build + recreate** | da fine snapshot a `StartedAt` 09:36:09 CEST (Δ file→start **99 s** include fine snap+build) | **~60–90 s** |
| **3. up → health** | `StartedAt` → primo health 200 | **275 s** |
| **Totale “usabile”** (deploy start → health) | snap+build+bootstrap | **~6.5–8 min** |

### 1c · BASELINE 0.10.25 (conservare)

```
BASELINE_0.10.25:
  container_start_to_uvicorn_s: 247
  container_start_to_health_s:  275
  trust_step_s:                 234.9
  trust_dry_run_prefetch_s:      35.1
  trust_backup_s:               198.0
  trust_apply_s:                  1.8
  deploy_sh_to_container_start_s: ~128  (agent wall)
  snapshot_proxy_s:              32.7
  prefetch_portal_obs_rows:     30576
  prefetch_distinct_macs:          66
```

---

## Parte 2 · trust prefetch

### 2a · Dove e cosa

| Pezzo | File:riga |
|-------|-----------|
| Prefetch | `trust.py:322-344` `_prefetch_portal_first_last_by_mac` |
| Uso nel piano | `trust.py:418-431` in `_build_trust_plan` |
| Bootstrap | `bootstrap.py:164` `reconcile_trust_history(dry_run=True)` → apply con `plan` |

**Query:** una aggregate  
`SELECT mac, MIN(seen_at), MAX(seen_at) FROM observations WHERE lower(kind) IN PORTAL_EVIDENCE GROUP BY mac`  
- **Nessuna finestra temporale** (intera storia legacy portal)  
- Live: **30 576** righe portal → **66** MAC distinti  
- Risultato: **dict in memoria** `{mac: (first, last)}` — non scrive tabelle derivate  
- Affiancato da `_prefetch_fdb_last_by_asset` (SwitchPort, non Observation)

### 2b · Consumo runtime / dipendenza

- Consumato **solo** da `reconcile_trust_history` → bootstrap (e test equivalence).  
- **Non** c’è cache usata dalle request HTTP dopo Uvicorn.  
- Se assente: l’API **parte lo stesso**; il piano trust userebbe N+1 (`use_prefetch=False`) o, se si elimina la lettura Observation, i soli campi asset/FDB.  
- È **warmup/reconcile di bootstrap**, non dipendenza request-path. Funzionale per: riempire `portal_first/last` mancanti, `timestamp_refresh`, quarantine FRITZ-only.

### 2c · GATE equivalenza

Dato già altrove:

| Bisogno trust | Destinazione calda | Live |
|---------------|-------------------|------|
| `portal_first` / `portal_last` | `assets.portal_first_seen` / `portal_last_seen` | `need_obs_fill_portal_first` = **0** |
| freschezza aggiuntiva | `presence_sources[portal]` + `SwitchPort.last_fdb_at` | tutti i 66 asset con obs portal hanno già asset/FDB/ps |
| “refresh” che Observation darebbe oltre asset fields | — | **7** asset con `derived > portal_last_seen`; di cui **5** coperti da FDB senza Observation; **2** (LGS328C/LGS310C) solo ~**3 s** di nmap Observation più fresco di `portal_last`/`ps` |

**VERDETTO 2c: GATE PASS** (con nota micro-lag 2 switch ~3s, irrilevante).  
Il prefetch può ripuntare su `portal_*` + FDB + `presence_sources` **oppure** essere eliminato.  
Backfill / finestra TTL ~27/07: **non necessaria** per il gate (campi asset già pieni).

### 2d · Disaccoppiamento / eliminazione (obiettivo avvio)

| Opzione | Effetto avvio | Rischio |
|---------|---------------|---------|
| **A. Eliminare lettura Observation** dal piano trust; usare solo `portal_*` + FDB (+ opz. max `presence_sources`) | −**~35 s** dry_run; queries aggregate Observation spariscono | Micro-lag `portal_last` su pochi asset finché arriva `observe_portal`; test equivalence da aggiornare |
| **B. Lazy / on-demand** (reconcile trust fuori bootstrap) | −**~35 s** (+ eventuale −198 s se si evita apply+backup all’avvio) | Cambia semantica “trust all’avvio”; serve job/admin esplicito |
| **C. Solo ripuntare prefetch** su destinazione calda (stessa struttura dict) | −tempo I/O Observation (query più leggera su 151 asset) | Conserva forma bootstrap |

**Raccomandazione ricognizione:** **A o C** — Observation non è necessaria al bootstrap; eliminarla accorcia l’avvio **e** toglie un reader legacy. Il guadagno maggiore sull’avvio resta evitare **backup 198 s** quando non c’è lavoro strutturale (già previsto in codice se `needs_backup=false`).

---

## Parte 3 · Inventario esaustivo reader `Observation` legacy

`rg` su `observatory/api` (esclusi commenti-only / modelli / raw/aggregate/flow):

| # | File:riga | Tipo | Stato 3b-iii |
|---|-----------|------|----------------|
| 1 | `scans.py` | reader (rimosso; solo docstring) | **già migrato** 3b-i |
| 2 | `inventory.py:182-194` | reader `active_discovery` | **GATE PASS** |
| 3 | `identity.py:1375-1378` | reader DNS hysteresis | **no-op** (0/0) |
| 4 | `trust.py:322-344` | reader prefetch MIN/MAX | **da trattare** (questo report: PASS eliminabile) |
| 5 | `trust.py:386-390` | reader N+1 `_portal_extent_nplus1` | solo `use_prefetch=False` / test |
| 6 | `trust.py:661-670` | `latest_portal_observation` | **helper non referenziato** altrove in api (morto per runtime) |
| 7 | `detectors/__init__.py:89,119` | reader 24h | **OFF** (`DETECTORS_ENABLED=""`); blocco se si accende |
| 8 | `retention.py:131` | **DELETE** prune TTL | manutenzione, non reader prodotto |
| 9 | `identity.py:1438-1460` / `materialize.py:82` / `identity.py:408` | **WRITE** `record_observation` | dual-write (spegnimento dopo reader) |

**Nessun quinto reader prodotto non mappato.**  
Unici residui oltre AD/DNS/prefetch: detectors (off), helper morto, path test N+1, retention delete.

### 3b · Riepilogo

| Reader | Classificazione |
|--------|-----------------|
| scans | migrato |
| active_discovery | GATE PASS |
| DNS | no-op documentato |
| trust prefetch | **GATE PASS → eliminabile/ripuntabile** |
| detectors | off; non migrare finché off |
| latest_portal_observation | morto; rimuovere in cleanup |
| N+1 trust | solo test |

---

## Parte 4 · Vincolo cold storage

| Destinazione | Caldo vs freddo | Segnale |
|--------------|-----------------|--------|
| `presence_sources` / `portal_*` su Asset | **solo caldo** (ultimo visto) | OK split: lo storico resta in raw/aggregate/cold; non mescola anni di timeline nell’asset |
| `IpAddress.source` sticky | caldo (binding corrente) | OK; non usare come archivio eventi |
| Prefetch → stessi campi asset/FDB | caldo | OK; **non** materializzare MIN/MAX storici Observation in una nuova tabella “calda” lunga |
| Tenere Observation come archivio | diventerebbe cold | Dopo DROP: storico solo via `observations_raw` / aggregate / backup |

**Non-regressione:** migrare reader su `presence_sources`/`portal_*` **aiuta** lo split hot/cold (stato vivo piccolo). Evitare di copiare l’intera history Observation in JSON asset.

---

## Sintesi per implementazione 3b-iii (passi successivi)

1. **active_discovery** → `presence_sources` / `portal_last_seen`  
2. **DNS** → `presence_sources["dns"]` (no-op)  
3. **trust prefetch** → **eliminare** (o ripuntare senza Observation) — guadagno baseline **−35 s** dry_run  
4. Assert inventario reader  
5. Spegnere dual-write  
6. Reset calibrazione  

**STOP** — nessuna implementazione in questo prompt.
