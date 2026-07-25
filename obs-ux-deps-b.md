# OBS-UX — Ondata B: dipendenze e decisioni legacy

**Versione:** 0.10.35 · **Branch:** `feature/obs-ux` · **Data:** 2026-07-25

Decisioni pre-rimozione per Wave B. Nessun drop schema in questa ondata.

---

## Tabella dipendenze

| Target | Chi chiama / dove | Uso reale | Decisione B |
|--------|-------------------|-----------|-------------|
| `/suggestions` | `router.js` redirect; API `GET /api/suggestions`; Oggi legge move pending | Route UI orfana; coda move già in Oggi | **KEEP redirect** → `/oggi` (migrato) |
| `Suggestions.vue` | Nessuna route attiva | File legacy non montato | **KEEP** file inutilizzato (no delete) |
| `PatchPanel` / `PatchPort` | Solo `models.py` + Alembic baseline | Schema morto, 0 UI | **KEEP schema**, no UI |
| `Dashboard` | `/` landing post-login | KPI e riepilogo | **KEEP** |
| `Incidents` | Router + nav secondaria | Aggregazione incidenti monitor | **KEEP** |
| `AiConsole` | Router + nav secondaria | Console AI read-only | **KEEP** |
| `Runbook` | Router + nav secondaria | Markdown operativo | **KEEP** |
| `POST /api/ingest/fdb` | Solo definizione API; collector usa `/fdb-switch` | Escape hatch legacy | **KEEP deprecato** (docstring) |
| `AssetIdentity` technical dump | Dossier `?technical=1` | Debug JSON grezzo | **KEEP** fino a ondata D |

---

## Superfici switch (Wave B)

| Vista | Caso d'uso | Non duplicare |
|-------|------------|---------------|
| **Impianto** (`/plant`) | Edit porte: patch, ruoli, note, override | Collocazione, ping |
| **Topologia** (`/topology`) | Dove è collegato (LLDP/FDB/Wi‑Fi) | Edit porte, SNMP health |
| **Monitor** (`/monitoring`) | Salute read-only: ping, SNMP aggregati, Internet/NAS | Mappa porte (→ Impianto), placement (→ Topologia) |

GS308EP: SNMP assente — Monitor cita Impianto per mappa e Topologia per ramo opaco; divergenza IP dichiarata in Impianto/Inventario/Dossier (asset 4).

---

## Fuori scope B (ondate successive)

| Item | Ondata |
|------|--------|
| Scheda ramo 308 completa | C |
| Rimozione dump tecnico `AssetIdentity` | D |
