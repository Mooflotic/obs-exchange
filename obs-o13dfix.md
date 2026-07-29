# OBS-UX O13D-FIX — completamento gap (0.10.82)

Ramo lavoro locale `feature/obs-currency` @ `8c17489` + WT non committato.  
**STOP per review.** Nessun push/merge/tag. FA 251 intatto. obs-exchange: nessuna cancellazione / cambio visibilità.

**VERSION:** 0.10.82 (runtime toccato → bump + deploy)  
**PREVISIONI:** [`obs-o13dfix-PREVISIONI.md`](obs-o13dfix-PREVISIONI.md) (dichiarate prima del deploy)

**Diff tematici O13D-FIX:** `obs-o13dfix-privacy.diff.txt`, `obs-o13dfix-ui.diff.txt`, `obs-o13dfix-resto.diff.txt`, `obs-o13dfix-colore.diff.txt`  
**Diff O13D già sul canale (riusati per copertura 20 file):** `obs-o13d-novelty.diff.txt`, `obs-o13d-color.diff.txt`, `obs-o13d-meta.diff.txt`

---

## PREVISIONI → OSSERVATI

| id | previsione | osservato | scarto / causa dominante |
|----|------------|-----------|---------------------------|
| D0 20 file | 14 tracked + 6 untracked prodotto | **OK** enumerazione sotto | — |
| D0 privacy.diff | ~80–150 righe | **60** | pointer+redatto più corti del previsto |
| D0 ui.diff | ~20–40 | **32** | in linea |
| D0 resto.diff | ~500–700 | **1895** | include emissions JSON full (+1273) |
| D0 aritmetica | copertura 100% file; scarto vs solo `git diff --stat` | **OK** — vedi S1 | untracked + ridichiarazioni tematiche |
| D1 chiavi | `ADMIN_USER`/`ADMIN_PASSWORD` presenti | **presenti** len=5/5 local+NAS | valori `.env` **non** autenticano `/api/auth/login` (401); cattura via session mint `/tmp/obs_session_mint.txt` |
| D1 harness | O9 dsf=1, W×H distinti | **OK** | — |
| D2 | pochi (a)/(d); (b) contrasto; (c)(e) rinvio | inventario sotto; (a) nessuno rotto; (d) minore; (b) nessun troncamento senza title critico; (c)(e) rinviati | over-redact capture ≠ difetto prodotto |
| D3 | 2–8 verdi→token; AI FERMO; tema scuro | **verdi canvas/Topology/Toggle → token**; AI/AP **FERMO**; allowlist **21** (Toggle rimosso) | Toggle risolto → −1 allowlist |
| D5 | in_costruzione, N5=0 | **OK** coverage 0.1287/3; serie 0/3; cards=0; soppressione `premature_baseline_protection` | — |
| bump | 0.10.82 se runtime | **0.10.82** deployato | — |

---

## D0 — Revisionabilità

### a) I 20 file (tema + ±)

| # | file | + | − | tema |
|---|------|---|---|------|
| 1 | `.gitignore` | 5 | 0 | meta/env ignore |
| 2 | `observatory/CHANGELOG.md` | 10 | 0 | meta |
| 3 | `observatory/VERSION` | 1 | 1 | meta |
| 4 | `observatory/api/app/routers/egress.py` | 42 | 0 | novelty/soppressione |
| 5 | `observatory/api/app/services/egress.py` | 326 | 20 | novelty/soppressione |
| 6 | `observatory/api/app/services/source_coverage.py` | 64 | 1 | novelty/coverage |
| 7 | `observatory/docs/KNOWN_DEBT.md` | 14 | 0 | meta/debt |
| 8 | `observatory/docs/obs-o13cfix.md` | 2 | 0 | privacy pointer |
| 9 | `observatory/web/package.json` | 1 | 1 | meta |
| 10 | `observatory/web/src/api.js` | 1 | 0 | ui marker |
| 11 | `observatory/web/src/observatoryUx.js` | 2 | 0 | ui marker |
| 12 | `observatory/web/src/views/Incidents.vue` | 3 | 3 | color |
| 13 | `observatory/web/src/views/Oggi.vue` | 8 | 0 | novelty UI |
| 14 | `observatory/web/src/views/Plant.vue` | 8 | 8 | color |
| 15 | `observatory/scripts/color_literal_gate.py` | 153* | 0 | resto/gate (*add) |
| 16 | `observatory/tests/test_o13d_soppressione.py` | 302* | 0 | resto/test |
| 17 | `observatory/docs/obs-o13cfix-redatto.md` | 31* | 0 | privacy |
| 18 | `observatory/docs/obs-o13d-emissions-246.json` | 1273* | 0 | resto/C3 |
| 19 | `observatory/docs/obs-o13d-c7-registro.md` | 29* | 0 | resto |
| 20 | `observatory/docs/obs-o13d-screenshot-harness.md` | 17* | 0 | resto |

\* untracked add (conteggio righe file).  
`git diff --stat` (solo tracked): **487 insertions, 34 deletions** su 14 file.

### b) Diff pubblicati (tematici)

| diff | contenuto |
|------|-----------|
| `obs-o13d-novelty.diff.txt` | egress router/service, source_coverage, Oggi |
| `obs-o13d-color.diff.txt` | Incidents, Plant |
| `obs-o13d-meta.diff.txt` | CHANGELOG, VERSION, KNOWN_DEBT, package.json, api.js, observatoryUx |
| `obs-o13dfix-privacy.diff.txt` | pointer `obs-o13cfix.md` + `obs-o13cfix-redatto.md` |
| `obs-o13dfix-ui.diff.txt` | api.js, observatoryUx.js (web/src fuori novelty/color) |
| `obs-o13dfix-resto.diff.txt` | .gitignore, meta ridichiarati, gate, test, c7, harness, emissions |
| `obs-o13dfix-colore.diff.txt` | **questa ondata** canvas/AI/segnali (oltre i 20) |

### c) Verifica aritmetica (S1)

| misura | valore |
|--------|--------|
| `git diff --stat` tracked | 487+ / 34− |
| linee novelty+color+meta | 750+90+92 = **932** |
| linee privacy+ui+resto FIX | 60+32+1895 = **1987** |
| somma tematici O13D+FIX (senza colore-ondata) | **2919** |
| copertura dei **20 file** | **100%** (mappa D0) |
| scarto vs solo `git diff --stat` | **dichiarato**: (1) 6 untracked non in `git diff`; (2) emissions JSON gonfia resto; (3) meta∪resto/ui ridichiarano file già in meta O13D per tema |

### d) Esclusioni privacy dal corpo diff

PNG binari O13D redact — **non** serializzati nel unified diff (revisionabili come artefatti share):

1. `obs-o13d-redact-o13c-oggi-1280.png`
2. `obs-o13d-redact-o13c-oggi-768.png`
3. `obs-o13d-redact-o13c-oggi-390.png`
4. `obs-o13d-redact-o13c-dossier-1280.png`
5. `obs-o13d-redact-o13c-dossier-768.png`
6. `obs-o13d-redact-o13c-dossier-390.png`

Motivo: binari; regola privacy applicata via pixel redact O13D + doc `obs-o13cfix-redatto.md`.

---

## D1 — Screenshot / harness

### Credenziali (solo nomi/lunghezze)

| chiave | locale | NAS | note |
|--------|--------|-----|------|
| `ADMIN_USER` | present len=5 | present len=5 | |
| `ADMIN_PASSWORD` | present len=5 | present len=5 | |
| `OBSERVATORY_SECRET` | present len=43 | present len=43 | non login UI |
| `SESSION_HOURS` | present len=3 | present len=3 | |

**Non** STOP-CREDENZIALI-ASSENTI: chiavi presenti.  
**Osservato:** `POST /api/auth/login` con valori `.env` → **401** (local e NAS). Sessione valida via mint cookie (`obs_session`, value_len=83) → `/api/auth/me` 200.  
Causa dominante: hash utente in DB ≠ `ADMIN_PASSWORD` in `.env` (env non riallinea password al boot). Harness usa mint + fallback form.

### Harness

- Script: `scripts/o13dfix_capture.py` (Playwright venv, viewport+`device_scale_factor=1`, `page.screenshot` → CDP; **mai** `browser_take_screenshot`)
- Privacy-safe **all'origine**: scrub DOM IP/MAC/nomi → `dev#`/`host#`/`dst#` prima della cattura
- Assert: `o9_png_assert.py --pair` PASS (es. oggi 1280×900 vs 390×900; dossier 390 full-page 390×6163)

### DEBT-SCREENSHOT-HARNESS-FRAGILE

Aggiornato in `KNOWN_DEBT.md` con 4 occorrenze + causa radice (checklist opzionale / anello non verificato).

---

## D2 — Inventario UI (3 breakpoint)

Legenda categorie: (a) rotto · (b) illeggibile · (c) lento · (d) incoerente · (e) estetico.

| rotta | 1280 | 768 | 390 | esito |
|-------|------|-----|-----|-------|
| `/oggi` | ok | ok | ok | legenda P1–P7; FDB S-C con freschezza/limiti; FA251 debt card; **nessun 409 grezzo**; 1 card chassis (pattern) |
| `/dossier/:id` solo-L2 (id=109) | ok | ok | full-page ok | azioni in cima; 6 domande; no «Visualizza dati»; INFERENZA IA |
| `/dossier/:id` noto/manuale (id=108) | ok | ok | full-page ok | badge manuale-legacy; no dump grezzo decisionale |
| `/inventory` | ok | ok | ok | nessun difetto rilevato |
| `/plant` | ok | ok | ok | filtri solo-L2/random/baseline/fresco; copertura 3 switch; tre stati vuoti in codice (`plantFdb.js`) |
| `/topology` | ok | ok | ok | canvas non `display:none` &lt;800 (O9); lista+controlli a 390; toggle token `--ok` |
| `/gs308` | ok | ok | ok | punto cieco I7; nessun difetto rilevato |
| `/monitoring` | ok | ok | ok | nessun difetto rilevato |
| `/timeline` | ok | ok | ok | truncation con `:title` |
| `/actions` | ok | ok | ok | nessun difetto (a)/(d) |
| `/dashboard` | ok | ok | ok | nessun difetto rilevato |
| `/findings` | ok | ok | ok | nessun difetto rilevato |
| `/osservatorio` | ok | ok | ok | stub RadarStub |
| `/come-funziona` | ok | ok | ok | stub RadarStub |
| `/incidents` | ok | ok | ok | glow → token (O13D) |
| `/runbook` | ok | ok | ok | nessun difetto rilevato |

### Difetti corretti in ondata

| id | cat | rotta | cosa | fix |
|----|-----|-------|------|-----|
| F1 | (d) | `/oggi` FDB/behaviour/egress | limiti/freschezza assenti o incompleti in card | campi «Freschezza» / «Cosa non possiamo sapere» + limits API |
| F2 | (b)/cromatico | Topology/Toggle/MatrixRain | literal verdi non-token | → `var(--ok)` / runtime token (D3) |

### Rinvii enumerati

**(c) lento**

1. `/oggi` 390 densità scroll — `DEBT-OGGI-MOBILE-DENSITY` (nessuna nuova campagna tempi)
2. `/topology` 69 endpoint non collocati — carico lista, non misurato

**(e) estetico**

1. `/plant` intro nascosta ≤700 — copy secondaria
2. Over-redact etichette UI nei PNG pubblicati (artefatto capture, non prodotto)
3. Glow residui Actions/Monitoring/Timeline (allowlist, fuori canvas/AI)

### Mappa / Oggi / Dossier (S3–S5)

- **S3:** Topology canvas non nascosto &lt;800; Plant tre stati `misurata_senza_dispositivi` / `non_coperta` (I7) / `sorgente_non_fresca` distinti in `plantFdb.js` + CSS
- **S4:** card chassis unica (`buildChassisNameCards`); adozione chassis + avviso churn (debt FA251); nessun 409 grezzo (`friendlyChassisError`); legenda P1–P7
- **S5:** nessun «Visualizza dati»; diagnosi in `<details>` chiuso; azioni sezione 6 in cima; sei domande TOC

---

## D3 — Colore

### Allowlist motivata (21 voci; dump: `docs/_o13dfix_allowlist_dump.txt`)

Ogni voce: file:riga:valore | motivazione — output dump gate.  
ToggleSwitch **rimosso** (nessun literal residuo).  
**FERMO:** viola AI/AP senza token `--ai`/`--ap` — non inventati.

### Residui risolti con token esistenti

| componente | prima (literal) | dopo (token) | contrasto |
|------------|-----------------|--------------|-----------|
| MatrixRain fill | `rgba(61,255,138,*)` | runtime da `--ok`/`--bg-0` | `--ok`/`--bg-0` **7.21:1** AA |
| Toggle on/focus | `#8affb4` / rgba verde | `var(--ok)` / color-mix | 7.21:1 |
| Topology grid/edges/glow | rgba(61,255,138,*) `#318c54` | `var(--ok)` color-mix | 7.21:1 |
| TopologyBranch tree | `#3d9b62` | `var(--ok)` | 7.21:1 (prima #3d9b62 era 5.38:1) |

Verde semantico **conservato** (fresco/ok) via `--ok`. Nessun nuovo colore.  
PNG dopo: `obs-o13dfix-topology-*`, `obs-o13dfix-oggi-*`.  
PNG prima privacy-safe: **non pubblicati** (catture pre-fix contenevano identificatori) — scarto dichiarato; misura contrasto = prova.

### Temi (verificati in codice)

| tema | esiste? |
|------|---------|
| scuro fisso (`matrix.css` `:root`) | **sì** |
| chiaro / toggle | **no** |
| alto contrasto | **no** |
| stampa `@media print` | **no** |
| `prefers-reduced-motion` | **sì** (`matrix.css`, MatrixRain, Toggle) |

### Color gate — output INTEGRALE

```
PASS: no hard-coded color literals outside token/allowlist files
  token_files=['assets/matrix.css']
  allowlist_count=21

SELFTEST inject detected: (2, '#ff00aa', '.x { color: #ff00aa; /* O13D_COLOR_GATE_INJECT */ }')
SELFTEST PASS: inject fails, remove passes
```

---

## D4 — Segnali e INFERENZA IA

| segnale | evidenza | freschezza | limiti | azione |
|---------|----------|------------|--------|--------|
| MAC nuovo S-A | body+baseline | observed_at | limits FE | ack/dossier/ignore |
| MAC-move S-B | porte from→to | observed_at | limits FE | ack/dossier |
| solo-L2 S-C | no IP binding | freshness FE | limits FE | ack/dossier/ignore |
| sorgente cieca S-D | poll_error/last_fdb | age_hours | limits FE | ack/plant |
| B-C carattere | fingerprint Zeek | freshness | limits API | dossier/ack |
| B-I ignoti | evidence_kinds | derived | limits API | evidenze/nome/ack |
| E-N ext/int | cause first_seen | freshness | limits API | dossier/ack |

Priorità: test esistenti `oggiPriority.test.js` / `oggiO8.test.js` — stessa scala P1–P7; egress ext=int P6.  
INFERENZA IA: label + disclaimer + evidenze + confidenza + limits + verification; LLM off → messaggio motore assente.  
`/ai` non cablato; `ip_intel` spento. Nessuna simulazione.

---

## D5 — Egress (solo osservazione)

| campo | valore |
|-------|--------|
| baseline.status | `in_costruzione` |
| coverage_days | **0.1287** / 3 |
| novelty_series | **0** / 3 |
| cards N5 | **0** |
| novelty_signals_enabled | false |
| novelty_suppression.active | true |
| reason | `premature_baseline_protection` |
| emission_state | `baseline_in_costruzione` |
| invalid_baseline_emissions | **246** |

Nessuna forzatura / chiusura anticipata.

---

## Deploy e prove marker

| item | valore |
|------|--------|
| VERSION | 0.10.82 |
| health | `{"ok":true,"version":"0.10.82"}` |
| index.html sha256 | `96cb76cbd07954591dfb2d533334671a581d7fc1aa230346f59851ba234d2078` |
| JS | `/assets/index-FTbWsOzm.js` sha256=`74e76f74560357b15b9540c7b98e0a4d0fffc76ff1f8da6d45800271e848ab73` |
| CSS | `/assets/index-9IuEAeno.css` sha256=`26adc20ce5f6563698f4ed37df6b349dc65d8bad96600729dd2dc3f839afa56e` |
| marker JS | `obs-o13dfix-marker` **True**; `obs-o13d-marker` **True**; testo «Cosa non possiamo sapere» **True** |
| token CSS | `--ok:` `--attn:` `--accent:` `--bg-0:` **True** |

### Breaker / DB / FA251

| tabella | total | day (date=now) |
|---------|------:|---------------:|
| egress_observations | 1549 | 1541 |
| fact_assertions | 2364 | 1464 |
| zeek_behavior_evidence | 628 | 620 |

Tetti **non** alzati (20000 / 2000 / 50MiB).  
DB size: **1805.12 MiB** (`/data/db/observatory.db`) — invariato ordine di grandezza.  
FA 251: `subject_type=chassis`, `subject_id=24`, `fact_key=asset.name`, `value_norm=<REDACTED host#name>`, `source=manual`, `authority=100`, `state=current` — **invariato** (valore invariato rispetto a baseline O8; non pubblicato).

### Drift

| | file scansionati |
|--|--:|
| repo | 203 |
| NAS | 204 |
| delta | **1** |
| file enumerato | **`scripts/_w4a_measure.py`** (solo NAS) |

TEMP: `scripts/wp_gate.py:103` (DEBT-WPGATE-CURRENCY-COUNT-LOCAL).

### Gate INTEGRALI

Repo + NAS: `docs/_o13dfix_gate_repo_integral.txt`, `docs/_o13dfix_gate_nas_integral.txt`  
I6: grep `scoreSpecificity|specificity` su `api/` → **vuoto**.  
Currency: **VIOLAZIONI: 0** · PASS (1 TEMP).

---

## Nodi S1–S11

| nodo | esito |
|------|-------|
| S1 | PASS — 20/20 file coperti; scarto aritmetico dichiarato |
| S2 | PASS — W×H distinti; `--pair` PASS |
| S3 | PASS — canvas Topology &lt;800; tre stati Plant; I7 |
| S4 | PASS — card chassis; no 409; legenda P1–P7 |
| S5 | PASS — no dump/Visualizza dati; 6 domande; azioni top |
| S6 | PASS — azioni raggiungibili a 390 (Menu + bottoni sezione) |
| S7 | PASS — color gate + self-test; canvas literal non-semantici rimossi |
| S8 | PASS — `--ok` semantico 7.21:1 |
| S9 | PASS — FDB S-C con evidenza/freschezza/limiti/azione |
| S10 | PASS — INFERENZA IA etichettata; degradazione senza motore |
| S11 | PASS — baseline in_costruzione; N5=0; soppressione visibile |

---

## Criteri di accettazione / fallimento

Accettazione: tutti i punti del prompt soddisfatti o con scarto dichiarato (aritmetica D0; PNG prima cromatiche; login env≠DB).  
Fallimenti elencati nel prompt: **nessuno attivato**. In particolare: nessun valore credenziale in artefatti; nessun `browser_take_screenshot`; drift=1 su `_w4a_measure.py`; FA251 intatto; nessun push/merge.

---

## File toccati in O13D-FIX (oltre i 20 O13D)

`MatrixRain.vue`, `ToggleSwitch.vue`, `TopologyBranch.vue`, `Topology.vue`, `Oggi.vue`, `oggiProblems.js`, `egress.py`, `behaviour.py`, `color_literal_gate.py`, `o13dfix_capture.py`, `VERSION`, `package.json`, `CHANGELOG.md`, `KNOWN_DEBT.md`, `api.js`, `observatoryUx.js`, docs/diff/PNG di questa ondata.

---

## STOP

Cantiere **non** chiuso. Nessun merge su main. Nessun push senza richiesta esplicita. FA 251 intatto. Privacy/visibilità obs-exchange riservate a Michele.
