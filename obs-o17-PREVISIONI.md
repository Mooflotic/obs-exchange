34
# OBS-O17 — PREVISIONI (dichiarate prima di cablare D)

Regola P già applicata: vincitori **PM-C** + **PA-1**.

Baseline HEAD (ultima misura P, stato coverage senza Fritz blind dove possibile):

| id | metrica | PRE (HEAD) | atteso POST | base |
|----|---------|----------:|------------:|------|
| P-fdb-390 | h(oggi-fdb)@390 | 12165 | **11758** | misura PM-C |
| P-app-390 | h(Apparati)@390 | 7605 | **7363** | misura PA-1 |
| P-pagina-390 | h_pagina@390 | ~22992–23225 | PRE − 407 − 242 ≈ **22343–22576** | somma delta (coverage R=312 può spostare) |
| P-fdb-768 | h(oggi-fdb)@768 | 9760 | **9760** | PM solo ≤390 |
| P-fdb-1280 | h(oggi-fdb)@1280 | 8663 | **8663** | invariato |
| P-app-768 | h(Apparati)@768 | 4990 | **4990** | PA-1 solo ≤640; a 768 già 2-col |
| P-app-1280 | h(Apparati)@1280 | 3283 | **3283** | invariato |
| P-via-labels-390 | .odm-cell-col visibili | 108 | **0** | PM-C |
| P-via-heads-390 | .odm-head visibili | 0 | **27** (9×3 bande) | riuso head |
| P-unique-fdb | stringhe uniche | 76 | **76** | invariate |
| P-unique-app | stringhe uniche | 96 | **96** | invariate |

Scarti in V: causa dominante per prima.

## Osservati (V finale, censimento 10 fam / 40 righe)

| id | osservato | scarto vs atteso | causa dominante |
|----|----------:|-----------------:|-----------------|
| P-fdb-390 | 13061 | +1303 vs 11758 | +1 famiglia matrice nello stato API della sessione V |
| P-app-390 | 7363 | 0 | — |
| P-pagina-390 | 23646 | ~+1.1k | stessa famiglia extra |
| P-fdb-768/1280 | PRE=POST | 0 | — |
| P-app-768/1280 | PRE=POST | 0 | — |
| P-via | cell=0 head=30 | head +3 vs 27 | 10×3 |
| G4 deployed | = POST | 0 | stesso censimento |

