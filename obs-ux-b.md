<!-- BLOCK-ID: OBS-UX-B -->

# OBS-UX — Ondata B (0.10.35)

**Tag:** `v0.10.35` = `275cbc3` su `feature/obs-ux`  
**Live:** health `0.10.35` · Cassiopea 2026-07-25

## Previsto vs osservato

| Assert | Esito |
|--------|-------|
| W1 health 0.10.35 | PASS |
| W2 regime `needs_apply=false` `T_backup=0` · T_total 8.8–9.0 s | PASS · T_total=**8.802**s · needs_apply=false · T_backup=0 |
| Conti: assets 151 · name_proposals 412 · AD (confirmed_present) 82 · ip_current 100 | PASS |
| `observations` assente da sqlite_master | PASS (0) |
| Dual-write spento | PASS |
| B-a nessuna info con regole diverse su due viste | PASS — Impianto=edit · Topologia=dove · Monitor=salute; citazioni crociate |
| B-b niente rimosso senza riga dipendenze | PASS — tabella in `docs/obs-ux-deps-b.md`; zero drop |
| I3 divergenza IP asset 4 | PASS al deploy B con copy «inventariale» — **poi corretta** (verifica RO): `.1.8` fatto; `.3.20` binding Fritz storico da confermare, non IP del 308; SPAN ≠ `.3.20` → `obs-ux-ip-308-verifica.md` |
| I7 GS308EP | PASS — Monitor non inventa SNMP; rimanda a Impianto/Topologia |

## Decisioni legacy (sintesi)

| Target | Decisione |
|--------|-----------|
| `/suggestions` | KEEP redirect → `/oggi` |
| PatchPanel/Port | KEEP schema, no UI |
| Dashboard/Incidents/Ai/Runbook | KEEP |
| `POST /fdb` | KEEP deprecato |
| Dump tecnico AssetIdentity | KEEP fino a ondata D |

## Note

- `scan_runs` live = 1489 (metrica storica «scans 68» non più allineata a questa tabella; non archiviata come churn asset).
- Scheda ramo 308 completa → ondata C.
