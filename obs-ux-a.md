# OBS-UX — Ondata A (0.10.34)

**Tag:** `v0.10.34` = bump commit su `feature/obs-ux`

## Previsto vs osservato
| Assert | Esito |
|--------|-------|
| W1 health 0.10.34 | PASS |
| W2 regime needs_apply=false T_backup=0 ~9s | PASS · T_total=**8.823**s needs_apply=false T_backup=0 |
| A-a CU-08/CU-02 in Oggi | PASS — coda unica con 6 campi; CU-02 = problemi prioritizzati (non Timeline delta) |
| A-b no hub separato; `/suggestions` redirect `/oggi` | PASS |
| A-c sei campi su ogni problema nome/move | PASS |
| I6 no scoreSpecificity Python | PASS |

## Note
- Modelli NameProposal e Suggestion restano distinti in backend; presentazione unificata in Oggi.
- Archivia rumore: anteprima D12/D13/D3; **non eseguita**.
- N rumore live ancora ~41 (anteprima spiega).
