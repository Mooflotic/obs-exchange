# OBS-DB-SLIM · Passo 2 — GO deploy 0.10.23

**2026-07-25 ~01:14 CEST** · merge `8fc53c4` · tag `v0.10.23` · deploy `api`+`web`

---

## Assert immediati

### a) Health

```json
{"ok":true,"service":"observatory-api","version":"0.10.23"}
```

### b) Retention-run forzato (collector → `POST /api/ingest/retention-run`)

Primo tentativo: **500** `database is locked` su `DELETE heartbeats` (contesa transient post-bootstrap) — **non** regressione legacy. Retry OK:

```json
{
  "ok": true,
  "result": {
    "compressed": 0,
    "aggregates": 0,
    "deleted": 0,
    "heartbeats_pruned": 0,
    "flow_observations_pruned": 0,
    "legacy_observations_pruned": 39
  },
  "before": {
    "observations_raw": 774387,
    "observations_aggregate": 0,
    "observations": 986244,
    "heartbeats": 74972,
    "flow_observations": 54772
  },
  "after": {
    "observations_raw": 774388,
    "observations_aggregate": 0,
    "observations": 986206,
    "heartbeats": 74972,
    "flow_observations": 54772
  }
}
```

| Check | Atteso (report STOP) | Osservato |
|-------|----------------------|-----------|
| Campo `before/after.observations` | presente | **sì** — aggancio OK |
| `legacy_observations_pruned` | ~0 | **39** (prime righe Jul 17 appena oltre 7g) |
| delta observations | ~0 | 986244 → 986206 (−38; −39 prune + scritture concurrenti) |
| `older_7d` post-run | 0 | **0** |
| `min(seen_at)` | — | avanzato a `2026-07-17 23:22:…` |

Il bite da 39 è coerente col passaggio del cutoff a ~7g esatti; non è ancora il regime 180–220k/giorno.

### c) Reader

- Presence EXPLAIN: ancora `USING INDEX ix_observations_mac` (no full scan).
- `/api/health` 200 · UI inventory risponde 401 (auth, atteso).
- Nessun errore presence/scans nei log post-run.

Snapshot pre-deploy: `data/backups/pre-deploy-20260725-0107.db` (rotazione keep-3 OK).

---

## NON chiuso — assert a +~24h (domani)

Segnare follow-up:

1. `legacy_observations_pruned` **> 0** in modo sostanziale (ordine **~180–220k**/giorno a regime, non decine).
2. `observations` scende rispetto al plateau di crescita; **freelist** sale (ora ~22k pagine post-run; writer riusano).
3. Presence / scans / detectors ancora integri dopo il primo prune grosso.

Stanotte: deploy + hook verificati. Il vero collaudo del TTL è **domani**.
