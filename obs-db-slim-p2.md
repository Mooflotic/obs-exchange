# OBS-DB-SLIM · Passo 2 — TTL legacy 7g · STOP pre-GO

Branch: `feature/obs-db-slim` · dopo passo 1 (freelist ~99 MiB indici).  
**Nessun deploy / nessun prune live finché non arriva GO.**

Diff: [`obs-db-slim-p2.diff.txt`](https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-db-slim-p2.diff.txt)

---

## 1 · Agancio al job retention esistente

Stesso percorso orario già vivo:

| Layer | File:riga |
|-------|-----------|
| Collector trigger | `collector/collector/main.py:489–494` → `POST /api/ingest/retention-run` |
| Endpoint | `api/app/routers/ingest.py:522–540` `ingest_retention_run` |
| Orchestrator | `api/app/services/retention.py` `run_retention` |
| **Nuovo** pruner | `retention.py` `prune_legacy_observations` (riusa pattern di `prune_heartbeats` / `prune_flow_observations`) |
| Config | `api/app/config.py` `obs_ttl_legacy_days: int = 7` |
| Wire | `ingest_retention_run` passa `legacy_observation_retention_days=settings.obs_ttl_legacy_days` |

Job esistente tocca già: raw TTL **7g** · heartbeats **30g** · flows **30g**.  
Legacy entra **nello stesso** `run_retention` / stesso commit DB — non un job nuovo.

`store_counts` espone anche `observations` (before/after nel JSON di risposta).

Test: `test_retention_prunes_legacy_observations` in `tests/test_m1_observation_store.py`.

---

## 2 · TTL 7g vs pavimento C2 (reader legacy)

| Reader | Finestra max | 7g copre? |
|--------|--------------|-----------|
| Presence `inventory.py:180–184` | **24h** (`ASSET_STALE_AFTER_HOURS`) | sì (≫) |
| Scans `scans.py:82–88` | **24h** | sì |
| Detectors `detectors/__init__.py:86–119` | **24h** | sì |
| DNS hysteresis `identity.py:1375–1378` | **1h** | sì |
| Trust backfill MIN/MAX `trust.py:322–344` | full history (solo se manca `portal_*`) | **non** dipende dal TTL operativo a regime: `observe_portal` scrive sui campi asset |

**Verdetto:** 7g non taglia sotto nessun reader vivo. Allineato a `obs_ttl_raw_days=7`. Margine vs pavimento 24h: **×7**, vs “minimo consigliato 3g”: più sicuro senza costo apprezzabile (vedi previsione).

---

## 3 · Previsione (live 2026-07-24 ~22:40 UTC)

| Metrica | Valore |
|---------|--------|
| Righe `observations` **ora** | **983 788** |
| `seen_at < now-7d` | **0** |
| Span | 2026-07-17 23:06 → 2026-07-24 22:39 (~**6g 23h**) |
| Tabella (dbstat) | ~785 MiB · ~837 B/riga |
| Freelist attuale (post passo 1) | ~23k pagine (~95 MiB residuo dopo riuso writer) |

### Primo giro dopo deploy

| | |
|--|--|
| Righe prima | ~984k |
| Righe dopo (atteso) | **~984k** (`legacy_observations_pruned` ≈ **0**) |
| Spazio logico liberato al primo giro | **~0** |

Motivo: tutto lo storico legacy è ancora **dentro** i 7 giorni. Comportamento corretto (come raw TTL ancora no-op finché non “morde”).

### Quando inizia a mordere

| Orizzonte | Taglio stimato | Logico (~837 B/riga) |
|-----------|----------------|----------------------|
| Tra poche ore (Jul 17 esce) | ~195 | ~0.2 MiB |
| +1 giorno (Jul 17–18) | ~1.6k | ~1 MiB |
| A regime (finestra scorrevole) | ~**180–220k / giorno** entrano ed escono | steady ~7g di dati |
| Se si fosse usato TTL **3g** oggi | ~375k subito | ~300 MiB logici — **scartato** (troppo vicino al pavimento) |

**File OS:** **non cala** fino al VACUUM passo 4. I DELETE aumentano la **freelist** (riusabile dalle scritture successive). Dichiarato.

---

## Piano GO (deploy normale)

1. Snapshot pre-op (deploy api già fa `pre-deploy-*.db` se `api` nei servizi).
2. Bump VERSION + merge/deploy **api** (collector già chiama retention-run — nessuna modifica collector).
3. Osservare primo `POST /api/ingest/retention-run` (log collector o trigger manuale interno): campo `legacy_observations_pruned` + `before.observations` / `after.observations`.
4. Niente VACUUM qui.

---

## STOP

Attendo **GO** per commit/merge/bump/deploy e osservazione del primo prune.
