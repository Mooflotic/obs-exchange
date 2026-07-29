178
# OBS-O16 — Fase M (MISURA) — STOP

```
wave: O16-M
head: b2979407e6be513201e3b789d2b4118e1109e1ed
branch: feature/obs-currency
VERSION_repo: 0.10.85
dist_locale: /tmp/obs-o16-dist (vite build da HEAD; asset JS index-w1cwSH0o.js = stesso hash O15)
api_upstream: http://192.168.1.3:8080 (sola lettura; stack NAS non toccato)
api_health_version_osservata: 0.10.82
viewport: 390×900 · deviceScaleFactor:1
auth_provenance: catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato
esito: STOP — ipotesi di lavoro FALSA — Fase D/V/G NON avviate
```

---

## VERDETTO GATE M

**Primo contributore M1 (altezza decrescente) = `oggi-fdb` (FDB · sensore difensivo), offsetHeight = 12595 — NON il sottoalbero matrice.**

Per regola ondata: ipotesi «matrice = causa dominante» **falsa**. **STOP obbligatorio. Nessun intervento D.**

### Causa dominante reale (dai dati)

| rank | id stabile | label | offsetHeight |
|------|------------|-------|--------------|
| 1 | `oggi-fdb` | FDB · sensore difensivo | **12595** |
| 2 | `section:Apparati multi-interfaccia` | Apparati multi-interfaccia | **7605** |
| — | AGGREGATO `[data-o15=decision-matrix]` (somma istanze) | sottoalbero matrice | **8127** |
| — | AGGREGATO matrice (bbox unione) | | **11695** |

- Tutte le **9** matrici (36 righe evidenza) stanno **dentro** `oggi-fdb` (evidence id `fdb-*`).
- `Apparati multi-interfaccia` = **7605 px senza alcuna matrice** (14 card informative; chrome matrice = 0).
- Decomposizione FDB: matrice_sum 8127 + non-matrice ≈ 4468 ≈ 12595.
- Pagina R1: **h_pagina = 23734** (allineato all’ordine di grandezza O15 23763).

La densità a 390 non è riducibile trattando **solo** la matrice: il secondo blocco di primo livello è quasi quanto tutte le matrici sommate, e non è matrice.

---

## M1 — Sezioni di primo livello @390 (COMPLETE, per altezza decrescente)

Fonte: `docs/obs-o16-M-measure.json` · capture_R1 · `M1_sections_by_height`.

| # | offsetHeight | ordine flusso | id DOM stabile | label |
|---|-------------:|--------------:|----------------|-------|
| 1 | 12595 | 5 | `oggi-fdb` | FDB · sensore difensivo |
| 2 | 7605 | 9 | `section:Apparati multi-interfaccia` | Apparati multi-interfaccia |
| 3 | 1744 | 6 | `oggi-coverage` | Copertura sorgenti |
| 4 | 608 | 7 | `oggi-behavior` | Comportamento · Zeek |
| 5 | 250 | 8 | `oggi-egress` | Egress · destinazioni |
| 6 | 175 | 3 | `o8-orphan-name-facts` | (orfano FA) |
| 7 | 144 | 2 | `nav.oggi-quick` | Domande rapide |
| 8 | 91 | 4 | `o4-discarded-moves` | (scarti mac_move) |
| 9 | 74 | 1 | `oggi-legend-collapse` | Priorità P1–P7 · legenda … |
| 10 | 51 | 10 | `oggi-secondary-collapse` | Altro in coda · 4 · priorità max P1 |
| 11 | 26 | 11 | `child:page-head page-header` | (chrome pagina) |

Assenti dal DOM in questa cattura (coda vuota): `Nomi da decidere`, `Porte da confermare`, `Conflitti da verificare`.

Somma altezze M1 = 23363 · h_pagina = 23734 (delta ≈ chrome/app shell).

---

## M2 — Sottoalbero matrice per famiglia @390

9 famiglie; ogni istanza: offsetHeight **903**, righe evidenza **4**, legenda sum **36** + details **17** = **53**, header `.odm-head` **visibili = 0** (nodi presenti per banda = 3, tutti `display:none`), row height mediana **136**, **flow_blocks = 4** per riga (`odm-ev` + 3× `odm-cell`).

| # | id famiglia (misura) | righe | h intestazione visibile | h legenda | h/riga (mediana) | blocchi flusso/riga |
|---|---------------------|------:|------------------------:|----------:|-----------------:|--------------------:|
| 1 | matrix#1 | 4 | 0 | 53 | 136 | 4 |
| 2 | matrix#2 | 4 | 0 | 53 | 136 | 4 |
| 3 | matrix#3 | 4 | 0 | 53 | 136 | 4 |
| 4 | matrix#4 | 4 | 0 | 53 | 136 | 4 |
| 5 | matrix#5 | 4 | 0 | 53 | 136 | 4 |
| 6 | matrix#6 | 4 | 0 | 53 | 136 | 4 |
| 7 | matrix#7 | 4 | 0 | 53 | 136 | 4 |
| 8 | matrix#8 | 4 | 0 | 53 | 136 | 4 |
| 9 | matrix#9 | 4 | 0 | 53 | 136 | 4 |

Grid osservato su `.odm-row`:  
`display:grid` · `grid-template-columns: 118.266px 118.266px 118.281px` ·  
`grid-template-areas: "ev ev ev" "c1 c2 c3"`.

---

## M3 — Risposte (dati)

**(a) A 390 la matrice riflua da tabella a pila?**  
**Sì, trasposizione a due bande** (non tabella a 4 colonne): evidenza a tutta larghezza, poi tre celle in linea. Non è una pila verticale di tre celle una sotto l’altra, ma **non** è una tabella vera a 4 colonne (contrasto con obiettivo D1).

**(b) Fonte e correntezza: una volta per riga o per cella?**  
**Una volta per riga.** 36/36 righe: `meta_count=1`, `meta_in_cells=0`.  
⇒ condizione D3 («se e solo se ripetute per cella») **non** scatta.

**(c) Legenda e intestazioni di via: una volta per famiglia o ripetute?**  
- Legenda neutra (`.odm-legend-sum`): **1 per famiglia** (9/9).  
- `.odm-head` (intestazioni via desktop): **0 visibili** @390.  
- Etichette via in cella (`.odm-cell-col`): **108 visibili** = 3 × 36 righe → **ripetute per ogni cella di ogni riga**.

**(d) Famiglie solo informative trascinano cromo di matrice?**  
**No.** `informative_without_matrix=22`, `informative_with_matrix_chrome=0`.

**(e) Padding/gap @390 ereditati da token desktop?**  
Token `--space-*` / `--gap` / `--pad` / `--page-pad` / `--workspace-pad`: **null** (non definiti).  
Valori computed ereditati da rem/CSS scoped O15:

| selettore | computed |
|-----------|----------|
| `.odm-row` gap | 5.6px · padding 7.2px 0 |
| `.odm-cell` padding | 3.2px 5.6px · gap 7.2px |
| `.odm-btn` | padding 7.2px 8px · minHeight 38.4px · 117×38 |
| `.workspace` padding | 14.4px 12px 24px |
| `--radius` | 6px |

Nessun breakpoint dedicato 390 oltre `@media (max-width: 768px)` della trasposizione.

---

## M4 — Ripetibilità R (stesso build, due catture consecutive @390)

| metrica | h1 (R1) | h2 (R2) | R = \|h1−h2\| |
|---------|--------:|--------:|-------------:|
| h_pagina | 23734 | 23422 | **312** |
| h_matrice (somma istanze) | 8127 | 8127 | **0** |
| h_matrice (bbox unione) | 11695 | 11695 | **0** |

R matrice = 0 (stabile). R pagina = 312 (possibile jitter di caricamento coda secondaria / banner; M5 identico nelle due catture).

---

## M5 — Censimento elementi (ripetibile in V)

| voce | R1 | R2 |
|------|---:|---:|
| famiglie matrice | 9 | 9 |
| righe matrice totali | 36 | 36 |
| elementi coda triage | 0 | 0 |
| card chassis | 14 | 14 |
| elementi coda rumore | 0 | 0 |

Nota: sezione «Nomi da decidere» assente → triage/rumore a 0 sono stato API, non errore di selettore.

---

## PREVISIONI post-D (dichiarate, NON eseguite)

D **non avviata**. Previsioni sotto = solo traccia di ciò che D1–D5 avrebbero mirato, derivate da M1–M2; **non** da riconciliare in V.

| id | componente | h osservata (R1) | h attesa post-D (ipotesi strutturale) | base |
|----|------------|-----------------:|--------------------------------------:|------|
| P-matrice-sum | somma 9×`.odm` | 8127 | ~5200–6200 | D1 tabella 4 col → flow_blocks 4→1; D2 head×1/famiglia al posto di 108 cell-col; D4 legenda riga singola (togli details 17×9) |
| P-oggi-fdb | sezione FDB | 12595 | ~9500–11000 | riduce solo sottoalbero matrice interno; resto FDB invariato |
| P-apparati | Apparati multi-interfaccia | 7605 | **7605** | fuori scope D (nessuna matrice) |
| P-pagina | h_pagina | 23734 | ≥ 23734 − (8127−6200) ≈ **≥21800** | floor: Apparati+resto restano |

Anche nello scenario ottimistico, la pagina resterebbe un muro: Apparati soli = 7605.

---

## Cosa NON è stato fatto (e perché)

- Fase D / V / G: **non avviate** — gate M (primo contributore ≠ sottoalbero matrice).
- Deploy, bump 0.10.86, commit, push: **no**.
- Modifica semantica / CSS / Vue: **nessuna** (solo script misura locale `scripts/o16_measure_m.py` + artefatti docs).
- T7, OBS-CURRENCY, FA 251, `_w4a_measure.py`, favicon, grano egress, obs-exchange oltre pubblicazione di questo report: **non toccati**.
- Nessuno script di misura depositato sul NAS.

---

## Artefatti locali

- `docs/obs-o16-M-measure.json` — dump integrale R1/R2
- `docs/obs-o16-M.md` — questo report
- Build: `/tmp/obs-o16-dist` (fuori repo)

JSON grezzo per audit: stesso contenuto di measure.json (M1 enumerato, M2 per famiglia, M3, R, M5).
