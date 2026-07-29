249
# OBS-O17 — OBS-DENSITY (0.10.86)

```
wave: O17
head_base: b2979407e6be513201e3b789d2b4118e1109e1ed
branch: feature/obs-currency
VERSION: 0.10.86
api_upstream: http://192.168.1.3:8080 RO (stack NAS non mutato in M/P/V)
api_health_observed: 0.10.82 (coerente: ultimo deploy api = O13D-FIX era; O14–O17 = web-only)
auth_provenance: catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato
esito: V C1–C12 VERDI · G deploy web OK · G4 scarto 0 su fdb/apparati/pagina
```

---

## 1. Elenco file toccati

| path | ruolo |
|------|--------|
| `web/src/assets/matrix.css` | `--space-1..4`, `--target-min: 24px` (WCAG 2.2 SC 2.5.8) |
| `web/src/components/OggiDecisionMatrix.vue` | PM-C @≤390; `data-o17="pm-c"`; `.odm-head` senza `aria-hidden` |
| `web/src/views/Oggi.vue` | PA-1 ≤640; `data-o17-section="apparati"` `data-o17="pa-1"` |
| `web/src/api.js` | `obs-o17-marker` + `obs-o17-version: __APP_VERSION__` |
| `web/src/observatoryUx.js` | export marker/version O17 |
| `web/package.json` | 0.10.86 |
| `VERSION` | 0.10.86 |
| `CHANGELOG.md` | voce 0.10.86 |
| `docs/KNOWN_DEBT.md` | chiude densità + O16; oneshot attic |
| `scripts/oggi_density_partition_measure.py` | misura permanente M1 |
| `scripts/oggi_density_prototype_measure.py` | misura permanente P |
| `scripts/oggi_density_verify_ab.py` | misura permanente V A/B |
| `_attic/o16_measure_m.py` | oneshot O16 archiviato |
| `_attic/o15_scrub_subset_proof.py` | oneshot scrub-proof archiviato |
| `docs/obs-o16-M.md`, `docs/obs-o16-M-measure.json` | evidenza storica O16-M (annotata, non cancellata) |
| `docs/obs-o17-*.md/json/png`, `docs/_o17_*` | artefatti ondata |

---

## 2. Partizione M1.A (integrale → JSON)

Strumento: `scripts/oggi_density_partition_measure.py`  
Integrale: [`obs-o17-M1-partition.json`](obs-o17-M1-partition.json) · sintesi [`obs-o17-M1.md`](obs-o17-M1.md)

**Gate partizione:** residue_pct = **0** (≤3%) su R1–R3.  
**Residuo nominato:** `gap_before` / `gap_after_last` fra blocchi L0 (margin/padding workspace non in `offsetHeight` sezioni) + subpixel; `residue_what` nel JSON.

**L0 @390 (R1, h_pagina=23304):** sezioni/chrome disgiunti — legend, nav quick, orphan banner, discarded moves, **oggi-fdb (12165)**, oggi-coverage, behavior, egress, **Apparati multi-interfaccia (7605)**, secondary. Somma L0 + gap = h_pagina.

**L1 oggi-fdb:** per famiglia {intestazione, corpo matrice, banda azioni, legenda} + contenuto NON-matrice enumerato voce per voce (JSON `L1_fdb`).  
**L1 Apparati:** 14 card, ciascuna con sottoblocchi nominati (JSON `L1_apparati`).

---

## 3. R per blocco (3 catture) + causa instabilità

| blocco | min | max | R_blocco |
|--------|----:|----:|--------:|
| oggi-fdb | 12165 | 12165 | **0** |
| Apparati multi-interfaccia | 7605 | 7605 | **0** |
| oggi-coverage | 1432 | 1744 | **312** |
| __h_pagina__ | 22992 | 23304 | **312** |
| oggi-behavior / egress / chrome | = | = | **0** |

**Causa oggi-coverage Δ312:** card `coverage_source_blind` **Fritz TR-064** (h≈308) presente solo in R1; assente R2/R3. Delta coverage = intero R_pagina. **Non** jitter banner.  
**Causa problem_cards 30→29:** stessa card (fingerprint coverage Fritz). Causa: **payload API** (freshness/age oltre cadenza). Nodo responsabile enumerato in `stability.coverage_instability`.

---

## 4. Enumerazione M3(b) — 36 righe

Asserzione script: `len(meta_per_row) == rows_checked` (exit errore se fallisce).  
In M1: **36/36**. Integrale in `obs-o17-M1-partition.json` → `meta_per_row`.  
(In V sessione finale: 40 righe / 10 famiglie — stato API esteso; len triples=120, len meta=40, asseriti dinamici.)

---

## 5. Inventario ripetizioni PRE → POST

**PRE (via labels in celle):** APPROFONDISCI / APPLICA / NON APPLICARE ≈ 3×N_righe (V: 50×3 con conteggio nodi testo; cell_col_visible = N_righe×3).  
**POST @390:** cell_col_visible = **0**; odm_head_visible = **3×famiglie** (V: 30). Ripetizioni rimosse = etichette di via in cella (non info unica).  
Inventario stringhe uniche fdb/apparati: **invariato** (C3 diff vuoto).

---

## 6. Tabella prototipi P

Regola (dichiarata **prima**): min h@390 fra candidati con (i) unique invariate (ii) h@768/@1280 entro R_blocco HEAD=0 (iii) nessuna leva vietata; tie → min DOM.

| id | h_fdb@390 | h_app@390 | h_fdb@768 | h_fdb@1280 | h_app@768 | h_app@1280 | DOM fdb/app | unique | ridotto@390 |
|----|----------:|----------:|----------:|-----------:|----------:|-----------:|------------:|-------:|:-----------:|
| HEAD | 12165 | 7605 | 9760 | 8663 | 4990 | 3283 | 1596/581 | 76/96 | — |
| PM-A | **16457** | 7605 | 9760 | 8663 | 4990 | 3283 | 1596/581 | 76/96 | no |
| PM-B | **13975** | 7605 | 9760 | 8663 | 4990 | 3283 | 1596/581 | 76/96 | no |
| **PM-C** | **11758** | 7605 | 9760 | 8663 | 4990 | 3283 | 1596/581 | 76/96 | **sì** |
| **PA-1** | 12165 | **7363** | 9760 | 8663 | 4990 | 3283 | 1596/581 | 76/96 | **sì** |
| PA-2 | 12165 | 8053 | 9760 | 8663 | **5438** | **3731** | 1596/581 | 76/96 | no (desk fuori R) |

**Vincitori: PM-C + PA-1.**  
PA-1 rimozione dichiarata: pila `dt`/`dd` → griglia affiancata (ripetizione strutturale di altezza, etichette restano).  
PM-C rimozione: 108 etichette via in cella → 3 head/famiglia.

---

## 7. Previsioni vs osservati

Fonte dichiarata: [`obs-o17-PREVISIONI.md`](obs-o17-PREVISIONI.md). Sessione V finale (censimento 10 fam / 40 righe):

| id | previsto | osservato | scarto | causa dominante |
|----|----------|-----------|-------:|-----------------|
| P-fdb-390 | 11758 (9 fam) | **13061** (10 fam) | +1303 | **contenuto API** (+1 famiglia matrice vs baseline P) |
| P-app-390 | 7363 | **7363** | 0 | — |
| P-pagina-390 | ~22343–22576 | **23646** | ~+1.1k | stessa famiglia extra + coverage stabile 1432 |
| P-fdb-768/1280 | invariati | invariati PRE=POST | 0 | PM solo ≤390 |
| P-app-768/1280 | invariati | invariati | 0 | PA-1 già 2-col a 768 |
| P-via-labels | 0 cell / 27 head | 0 cell / **30** head | +3 head | 10 famiglie×3 |
| P-unique | invariate | C3 ok | 0 | — |

Deployed@390 riconciliato con POST V: fdb/app/pagina **delta 0**.

---

## 8. Gate C10 + C11 (integrali)

### C10

- `python3 scripts/w8_currency_gate.py` → **VIOLAZIONI 0 · PASS (1 TEMP)** — [`_o17_gate_repo_integral.txt`](_o17_gate_repo_integral.txt)  
- NAS stesso → [`_o17_gate_nas_integral.txt`](_o17_gate_nas_integral.txt)  
- `grep -RInE 'scoreSpecificity|specificity' api/` → **VUOTO** (repo+NAS)  
- `color_literal_gate.py` → **PASS**; `--self-test` → **PASS** (repo+NAS)

### queueConservationCheck

```
triage_n = 0
rumore_noise_proposal_ids_n = 0
chassis_cards_n = 14  (superficie Apparati / V census)
missing = []
duplicated = []
```

**Nota:** triage=0 e rumore=0 sono **stato API**, non errore di selettore; un check su insieme vuoto non è prova di popolazione — cardinalità dichiarata sopra.

### C11 — insiemi enumerati

```
solo-NAS = { scripts/_w4a_measure.py }
  motivazione: decisione Michele; resta sul NAS; non analizzare.

solo-repo = {
  scripts/oggi_density_partition_measure.py,
  scripts/oggi_density_prototype_measure.py,
  scripts/oggi_density_verify_ab.py
}
  motivazione: suite misura densità O17 (partizione, prototipi, A/B); gira in locale, non sul NAS.
```

**Orfani:** nessuno (oneshot `o16_measure_m` + `o15_scrub_subset_proof` → `_attic/`).

---

## 9. Diff C1 / C2 / C3 + audit C4

Da [`obs-o17-V.json`](obs-o17-V.json):

- **C1** triples PRE=POST, len=120, **diff=[]**  
- **C2** meta PRE=POST, len=40, **diff=[]**  
- **C3** unique fdb/app only_pre/only_post **[]**; ripetizioni via: PRE cell labels → POST heads  
- **C4** violations **[]**

---

## 10. Tabella C5 (computed style)

Tre intestazioni via (POST @390) — unica differenza ammessa = testo etichetta:

| prop | APPROFONDISCI | APPLICA | NON APPLICARE |
|------|---------------|---------|---------------|
| width | 118.266px | 118.266px | 118.281px |
| font-size | 10.88px | 10.88px | 10.88px |
| font-weight | 400 | 400 | 400 |
| font-family | Inter, … | Inter, … | Inter, … |
| color | rgb(102,112,133) | idem | idem |
| background | transparent | idem | idem |
| border | none | idem | idem |
| padding/margin | 0 | 0 | 0 |
| text-transform | uppercase | idem | idem |
| opacity | 1 | 1 | 1 |
| order | 0 | 0 | 0 |

Bottoni Impianto/Riconosci/Ignora ≈ 117.2×38.4 ≥ 24×24. **nondom=true, btn_ok=true.**

---

## 11. Altezze PRE/POST, censimento, catture

| | PRE@390 | POST@390 | deployed@390 |
|--|--------:|---------:|-------------:|
| h_pagina | 24341 | 23646 | 23646 |
| h_fdb | 13514 | 13061 | 13061 |
| h_apparati | 7605 | 7363 | 7363 |

Censimento allineato PRE=POST: famiglie_matrice=10, righe=40, card_apparati=14, problem_cards=30, informative_without_matrix=20, coverage=5, triage=0, rumore=0.

**PNG scrub** (Page.screenshot dsf=1, keep=chrome∩uiExact):

| file | W×H | sha256 |
|------|-----|--------|
| obs-o17-oggi-1280.png | 1280×15052 | 38c58e82…45cacd |
| obs-o17-oggi-768.png | 768×18283 | dee90283…00f933 |
| obs-o17-oggi-390.png | 390×22934 | d4c57c61…f142a0 |

`o9_png_assert.py --pair` 1280↔768 e 768↔390: **PASS** (larghezze distinte).

---

## 12. Deploy G3 + G4

**G3 servito:**

- `/assets/index-DeRwHSMJ.js` sha256 `417efd2ee99b8b9ebe4040457488aa37601983ec5396402340bc1bb2c0d16005`  
  - `0.10.86` True · `obs-o17-marker` True · `pm-c` True · `pa-1` True  
- `/assets/index-B8usGG7q.css` · `--space-1` True · `--target-min` True  
- NAS `VERSION` file = **0.10.86**  
- `/api/health` = **0.10.82** — coerente con ultimo deploy **api** (O13D-FIX); O14–O17 web-only. Nessun cantiere.

**G4:** deployed vs POST locale, stesso censimento: Δfdb=0, Δapp=0, Δpagina=0 ≤ R_blocco.

---

## 13. Debiti

| debito | stato |
|--------|--------|
| DEBT-OGGI-MOBILE-DENSITY | **CHIUSO** (C9 stretto fdb+apparati+pagina) |
| DEBT-O16-GATE-ILLFORMED | **APERTO** (revisore) — documentale |
| DEBT-O16-M-PARTIAL-ENUM | **CHIUSO** in M1 |
| DEBT-O16-R-MISATTRIBUTED | **CHIUSO** in M1 |
| DEBT-O16-CENSUS-UNSTABLE | **CHIUSO** in M1.C |
| DEBT-ONESHOT-SCRIPT-RESIDUE | quinta evitata (attic o16/o15_scrub) |

---

## 14. Cosa NON ho fatto (e perché)

- Nessuna trasposizione/fusione famiglie matrice (decisione esclusiva Michele).  
- Nessuna leva vietata (tab/accordion/clamp/virtualizzazione/font-size/…).  
- Nessun deploy api; T7 / OBS-CURRENCY / FA251 / `_w4a_measure.py` / favicon / egress / `/ai` / main/merge/tag/force — **non toccati**.  
- Nessuna modifica intenzionale 768/1280 (PM/PA scopati a ≤390 / ≤640).  
- Browser MCP `browser_take_screenshot` — non usato.
