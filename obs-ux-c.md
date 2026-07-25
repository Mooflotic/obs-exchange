<!-- BLOCK-ID: OBS-UX-C -->

# OBS-UX — Ondata C (0.10.36)

**Tag:** `v0.10.36` = `17b19d4` · Deploy con D in `0.10.37`

## Previsto vs osservato

| Assert | Esito |
|--------|-------|
| C-a nessun dato porta/PoE/contatore per il 308 | PASS — Branch308Card dichiara gap I7 |
| C-b ogni elemento etichettato fatto o inferenza | PASS — tag Fatto / confidenza / Inferenza |
| C-c CU-05 «cosa c’è dietro il 308» | PASS — scheda in Topologia/Impianto/Dossier |
| I7 snmp/fdb false · poll manual_upstream | PASS |

## Correzione post-C (verdetto operativo, ship in 0.10.38)

Copy iniziale B/C trattava `.3.20` come inventariale: **errato**.  
Verifica RO: binding Fritz stale; SPAN ≠ `.3.20`. UI aggiornata a «da confermare» — vedi `obs-ux-ip-308-verifica.md`.
