# OBS-033A GO — assert live vs previsione

**Merge:** `0e21452` (no-ff `feature/obs-033a`) · **tag:** `v0.10.21` · **deploy:** `./scripts/deploy.sh api web`  
**Massa:** non eseguita (Michele)

## Assert (dichiarato → osservato)

| Voce | Dichiarato | Osservato | Esito |
|------|------------|-----------|-------|
| a) `/api/health` | `0.10.21` | `0.10.21` | **ok** |
| a) sidebar | `v0.10.21 · …` (non sola data) | `v0.10.21 · 24/07` | **ok** |
| b) pulsante | **7** | **7** `[297,3,154,36,200,199,235]` | **ok** |
| c) coda | `0 · 22 · 3` | `0 · 22 · 3` | **ok** |
| c) sottogruppi | chassis 10 · manual 5 · sotto-soglia 7 | **10 · 5 · 7** | **ok** |
| d) rumore top | `#25` D13, `#85` D12, `#98` D12 | `#25` Bticino-F454; `#85` PC-192-168-2-85; `#98` PC-68-13-F3-… | **ok** |
| e) massa | non eseguire | non eseguita | **ok** |

`top diversa` pre-massa: ancora **1** (`#2` Switch vs Switch Linksys) — atteso; dopo archivio 297+3 → **0**.

## Atteso post-massa (Michele)

`0 · 22 · 0` · top diversa **0** · `#2` allineato su `Switch Linksys`.
