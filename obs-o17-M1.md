126
# OBS-O17 — Fase M1 (partizione + stabilità)

```
wave: O17-M1
head: b2979407e6be513201e3b789d2b4118e1109e1ed
tool: scripts/oggi_density_partition_measure.py
dist: /tmp/obs-o16-dist (HEAD)
api: http://192.168.1.3:8080 RO
auth_provenance: catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato
gate: PASS (residue 0%; M3b len==36; nodi instabilità identificati)
```

## Gate M1

| criterio | esito |
|----------|-------|
| partizione residue ≤ 3% h_pagina | **PASS** residue_pct=**0** (R1–R3) |
| len(array)==contatore per enum | **PASS** meta_per_row len=36 == rows_checked |
| nodo instabilità identificato | **PASS** (coverage + problem_cards = stessa card) |

Nota: un bug `residue_pct or 99` aveva falsato il gate a 99; corretto nello script (`None`-aware). Catture invariate; gate ricalcolato.

---

## M1.A — Partizione L0 @390 (R1 stabile di riferimento per FDB/Apparati)

h_pagina R1=**23304** · sum_L0_geom+gaps=**23304** · residuo nominato=**gap_before/gap_after** fra blocchi L0 (margin/padding workspace), sum_gaps≈**372**.

| id | h | ruolo |
|----|--:|------|
| oggi-fdb | 12165 | sezione |
| section:Apparati multi-interfaccia | 7605 | sezione |
| oggi-coverage | 1744† | sezione (instabile) |
| oggi-behavior | 608 | sezione |
| oggi-egress | 250 | sezione |
| o8-orphan-name-facts | 175 | banner |
| nav.oggi-quick | 144 | chrome |
| o4-discarded-moves | 91 | banner |
| oggi-legend-collapse | 74 | chrome |
| oggi-secondary-collapse | 51 | sezione |
| page-header | 26 | chrome |

† R2/R3: coverage=1432 (vedi C).

**Dentro oggi-fdb:** 9 famiglie × (parts_non_matrix≈394 + matrix=903) = card 1345; matrix_sum=**8127** (66,8% di 12165); non_matrix_sum enumerato≈**3566** (head+names+meta+fields).

**Dentro Apparati:** 14 card, head=20. Costo dominante = `dl.oggi-fields` (mediana **372** / card ≈543): a ≤640 px le coppie dt/dd sono in **pila** (`grid-template-columns: 1fr`), non affiancate.

---

## M1.B — R per blocco (3 catture)

Solo blocchi con R>0:

| blocco | min | max | R_blocco | valori |
|--------|----:|----:|---------:|--------|
| oggi-coverage | 1432 | 1744 | **312** | 1744, 1432, 1432 |
| __h_pagina__ | 22992 | 23304 | **312** | 23304, 22992, 22992 |

oggi-fdb R=0 · Apparati R=0 · matrice R=0.

---

## M1.C — Causa instabilità (dati, non «jitter»)

**Nodo responsabile:** card coverage  
`Sorgente copertura vecchia · Fritz TR-064 (hostlist / mesh / WLAN)`  
(`kind=coverage_source_blind`, h≈308).

| cattura | API `/api/coverage/sources` | DOM |
|---------|------------------------------|-----|
| R1 16:41:29Z | Fritz presente, last_success_at=2026-07-29T16:40:14.841265Z | card h=308, section 1744, problem_cards=30 |
| R2 16:41:38Z | Fritz **assente** dalla lista cards | section 1432, problem_cards=29 |
| R3 16:41:49Z | Fritz **assente** | idem |

Delta section = 1744−1432 = **312** = intero R_pagina.  
problem_cards 30→29 = **la stessa card** (è un `.oggi-problem` dentro coverage).

Causa: **differenza di payload API** (finestra / classificazione «copertura vecchia» temporale su Fritz). Non rumore di layout.

Per V: baseline PRE/POST sullo stato **senza** Fritz blind (R2/R3), oppure dichiarare coverage fuori dal confronto di riduzione densità se il payload diverge.

---

## M1.D — Censimento esteso (R1; R2/R3: problem_cards−1 = Fritz)

| voce | R1 | R2 | R3 |
|------|---:|---:|---:|
| famiglie matrice | 9 | 9 | 9 |
| righe matrice | 36 | 36 | 36 |
| card chassis / Apparati | 14 | 14 | 14 |
| problem_cards | 30 | 29 | 29 |
| informative_without_matrix | 21 | 20 | 20 |
| coda triage | 0 | 0 | 0 |
| coda rumore | 0 | 0 | 0 |
| unique info oggi-fdb | 77 | — | — |
| unique info Apparati | 96 | — | — |

---

## M1.E — M3(b) enumerazione completa

`rows_checked=36` · `len(meta_per_row)=36` · asserito nello script · `all_rows_have_exactly_one_meta=true` · `meta_in_cells=0` su tutte.  
Include famiglie O16 omesse: `1e247df1`, `54d984b9`, `3e770d0b`, `144fbd79` (e tutte le altre). Dump: `obs-o17-M1-partition.json`.

---

## M1.F — Inventario ripetizioni (carburante P)

**oggi-fdb (top):** APPROFONDISCI/APPLICA/NON APPLICARE ×**45** ciascuno; simboli; `Correntezza: non misurato` ×36; `Fonte: fdb` ×27; etichette campi ×9.

**Apparati (top):** Priorità/Regola/Causa/Impatto/Certezza/Esito/Cosa verificare ×**14**; `correggi nome`/`Dossier` ×14; frasi esito ripetute ×5.

---

## Regola di scelta P (dichiarata PRIMA di misurare)

Vince il candidato con **h@390 minore**, fra quelli che soddisfano:
1. stringhe informative uniche invariate vs HEAD
2. h@768 e h@1280 entro R_blocco di HEAD (FDB R=0, Apparati R=0 ⇒ scarto 0)
3. nessuna leva vietata  

A parità entro R_blocco: meno nodi DOM.  
Se nessuno scende sotto HEAD@390: STOP prima di D.

**PA mirano a `dl.oggi-fields`** (sottoblocco dominante Apparati, mediana 372).
