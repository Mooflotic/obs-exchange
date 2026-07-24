# OBS-DEPLOY-01 — FASE B (STOP pre-deploy)

**Branch:** `feature/obs-deploy-01` · **VERSION:** invariata (0.10.21) · **Deploy feature:** no

---

## V1 — `observations` legacy: **VIVA**

| Prova | Esito |
|-------|--------|
| `max(seen_at)` vs ora | age **~15 s** (live) |
| Scritture ultime 10 min | **~1700** righe |
| Writer | `identity.record_observation` [`identity.py:1438–1460`](../api/app/services/identity.py) |
| Call sites | `materialize.py:82` (host, gated su raw `created`), `materialize.py:226` (wlan assoc), `identity.py:408` (nmap) |
| Perché non solo-raw | dual-write deliberato: presence/trust leggono ancora legacy `Observation.seen_at` (orizzonte ~24h); commento in `materialize.py:75–80` |

**Non DROP.** Serve job di pruning.

Primo commit che introduce `record_observation`: `9be7dbc` (2026-07-18).

---

## V2 — TTL raw 7g: job **gira**, prune **ancora no-op**

| Vova | Esito |
|------|--------|
| Scheduler | collector `retention` ogni `retention_interval_sec=3600` ([`main.py:633–640`](../collector/collector/main.py)) |
| Endpoint | `POST /api/ingest/retention-run` → **200** (log api) |
| Ultimo giro | `metric_snapshots` **21:19:55** UTC (cadenza oraria); log `retention=200` ripetuti |
| Righe raw >7g | **0** (`min(observed_at)=2026-07-20`, finestra ~5g) |
| `observations_aggregate` | **0** (rollup non ha ancora materiale da comprimere) |

Il TTL è applicato dal job; la crescita odierna è perché **tutto il raw è ancora dentro i 7 giorni**, non perché il pruner sia morto.

---

## Diff FASE B (questo branch)

1. **`deploy.sh`:** snapshot **solo** se `api ∈ servizi`; altrimenti `snapshot DB saltato`.
2. **`deploy.sh`:** dopo snapshot, rotazione **keep-3** su `pre-deploy-*.db` (Python nello stesso SSH).
3. **Retention legacy:** `prune_legacy_observations` in `run_retention` · `OBS_TTL_LEGACY_DAYS` default **3** (presence ≪ 3g).
4. Test: prune legacy + contratto testo `deploy.sh`.

### Smoke (innocuo, già eseguito)

`./scripts/deploy.sh web` → log **`snapshot DB saltato (api non nei servizi: web)`** · `/api/health` **0.10.21** · web **200**.

---

## Previsione (assert al GO / primo deploy api + retention)

Stato oggi: DB file **~2.55 GiB**; `data/backups` **13.7G** (3× pre-deploy + 3× observatory-* + json).

| Voce | Atteso |
|------|--------|
| Righe legacy prune @3g | **~−38%** (~368k / 977k) |
| Spazio logico tabella+indici | **≈ −0.35–0.45 GiB** (stima su dbstat `observations` 778 MiB × frazione) |
| **File DB su disco** | **≈ invariato** finché non si fa **VACUUM offline** (SQLite non restringe il file al DELETE) |
| Dopo VACUUM offline (manuale, fuori job) | ordine **~2.1–2.2 GiB** (se anche gli indici si ricalcolano) |
| `data/backups` post-rotazione | già **3** pre-deploy → liberato **0** subito; keep-3 evita crescita oltre 3 al prossimo snapshot api (~2.5G/cad) |
| Raw @7g | ancora **0** delete finché non passa il 27/07 circa |

---

## STOP

Review → **GO** per merge + deploy **api** (snapshot = rete prima del primo prune operativo) + assert previsione.  
**Non** VACUUM automatico nel job orario.
