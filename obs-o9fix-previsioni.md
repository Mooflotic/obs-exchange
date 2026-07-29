# OBS-UX O9-FIX — bozza previsioni (PRIMA delle catture batch)

**Stato runtime:** 0.10.72 (nessun bump finché non ci sono correzioni (a) runtime).

## Previsioni difetti per le 11 rotte Y2 (prima di catturare)

| Rotta | (a) rotto atteso | (b) | (c) | (d) | (e) | Note previsione |
|---|---|---|---|---|---|---|
| `/dossier/:id` (solo-L2 112 + noto 3) | possibile azioni tagliate a 390 | densità sezioni | — | provenance badge vs testo | densità | azioni in viewport a 390 già viste su 112 → (a) improbabile |
| `/inventory` | overflow tabella orizzontale a 390/768 | densità | filtri multi-step | — | — | tabelle dense tipiche |
| `/monitoring` | overflow / controlli fuori viewport a 390 | densità | — | — | — | |
| `/timeline` | overflow eventi/timestamp a 390 | densità | — | — | — | |
| `/actions` | possibili CTA fuori riga a 390 | — | — | — | — | |
| `/dashboard` | slot vuoti non = rotto | — | — | slot ready vs live | estetico | DEBT-DASHBOARD-READY-SLOTS |
| `/findings` | — | — | confluenza Oggi | doppia superficie | — | DEBT-FINDINGS |
| `/osservatorio` | — | — | — | — | minore | statica |
| `/come-funziona` | — | — | — | — | minore | statica |
| `/incidents` | possibile layout stretto | — | — | — | — | |
| `/runbook` | possibile layout stretto | — | — | — | — | |

**Correzioni (a) previste:** solo se overflow/oob/testo tagliato/azione irraggiungibile misurati in audit; altrimenti nessuna correzione runtime → **nessun bump 0.10.73 / nessun deploy**.

**Rinvio O10 (già noto + previsti):** densità mobile plant#6 / oggi#8; (b)(c)(d)(e) di questa ondata.

## Larghezze PNG attese

| Breakpoint | Larghezza reale PNG | Altezza (viewport) |
|---|---|---|
| 1280 | **1280** | 900 |
| 768 | **768** | 900 |
| 390 | **390** | 900 |

Requisito prova: due BP diversi → larghezze PNG diverse; `o9_png_assert.py --pair`.
