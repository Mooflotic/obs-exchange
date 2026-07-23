# OBS-DOSSIER-FIX-DIFF-028

## Summary

1. **CandidateList** collassa sulla riga scelta + link «cambia»; placeholder neutro «nessuna di queste? scrivila».
2. **Dossier** ordine §6: Chi sei → Come sei connesso → …
3. **AssetChassis** non carica più tutto l’inventario (causa spinner infinito); errore / vuoto espliciti.
4. **os_divergence** confronta label normalizzate (`Linux 4.15` ≡ `Linux 4.15 - 5.19`).

Diff unificato (-U5): `obs-dossier-fix-diff-028.diff.txt` (stesso commit di pubblicazione).

**STOP pre-deploy** — nessun deploy in questa fase.

## Versione (live 0.10.17 → dichiarata 0.10.19)

Non è un deploy saltato non tracciato.

| Tag locale | Contenuto | Deploy live | obs-exchange |
|---|---|---|---|
| **0.10.17** | OBS-MANUAL-WINS-026 | sì (live attuale) | `obs-manual-wins-diff-026.md` |
| **0.10.18** | OBS-FINGERBANK-027 (FASE B) | **no** — solo working tree | **non pubblicato** |
| **0.10.19** | OBS-DOSSIER-FIX-028 | **no** — STOP pre-deploy | questo pacchetto |

La **0.10.18** esiste nel tree locale (`VERSION` / `CHANGELOG`) come Fingerbank on-demand, ma non è stata né deployata su Cassiopea né caricata su obs-exchange. Il bump a **0.10.19** per il 028 è quindi numerazione sequenziale sul branch di lavoro, non un buco di release in produzione.
