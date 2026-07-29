# OBS-UX O9-FIX — audit 11 rotte + soli difetti (a)

**Runtime:** 0.10.73 · deploy `web` (+ recreate `api` solo remount `/VERSION`) · ramo `feature/obs-currency`  
**Harness:** Playwright Chromium headless = Emulation-equivalent (`viewport` CSS + `deviceScaleFactor:1` + screenshot viewport); assert `o9_png_assert.py`. **Mai** `browser_take_screenshot`.  
**O9 accettata:** X1–X3, overflow documento, topology ≤800, quick links V1–V5 — **non ritoccati**.

---

## Y0 — annotazione retroattiva

- Aperto `DEBT-SCREENSHOT-HARNESS-FALSE-EVIDENCE` in `docs/KNOWN_DEBT.md` (O5–O8: dichiarazione «tre breakpoint» falsa; ondate valide su dati; harness corretto in O9).
- Annotata una riga `[Corretto in O9-FIX]…` in `obs-o5.md`, `obs-o6.md`, `obs-o7.md`, `obs-o8.md` — **senza** riscrivere/cancellare immagini.

## Y1 — stima V1–V5

In `obs-o9.md` FASE 3: colonna «prima» etichettata **stima non misurabile a posteriori**; «dopo» **misurato** su 0.10.72. Nessuna rimisurazione/rollback.

---

## Previsioni (dichiarate PRIMA delle catture batch)

Vedi anche `obs-o9fix-previsioni.md`.

| Rotta | (a) atteso | (b) | (c) | (d) | (e) |
|---|---|---|---|---|---|
| `/dossier/:id` | improbabile | densità | — | badge provenance | densità |
| `/inventory` | overflow tabella 390 | densità | filtri | — | — |
| `/monitoring` | overflow/oob 390 | densità | — | — | — |
| `/timeline` | overflow/CTA 390 | densità | — | — | — |
| `/actions` | CTA fuori riga 390 | — | — | — | — |
| `/dashboard` | no | — | — | slot ready | estetico |
| `/findings` | soft H-scroll Salva | — | confluenza | doppia superficie | — |
| `/osservatorio` | no | — | — | — | minore |
| `/come-funziona` | no | — | — | — | minore |
| `/incidents` | layout stretto? | — | — | — | — |
| `/runbook` | tabelle md clip | — | — | — | — |

**Larghezze PNG attese:** 1280 / 768 / 390 (altezza viewport 900).  
**(a) da correggere:** solo se misurati; altrimenti nessun bump.

---

## Osservati (DOPO catture + audit DOM)

### Inventario rotte Y2 (12 URL = 11 rotte + dossier×2)

| # | Rotta | Caso | 1280 | 768 | 390 | Difetti |
|---|---|---|---|---|---|---|
| 1 | `/dossier/:id` | solo-L2 asset **112** | 1280×900 | 768×900 | 390×900 | #4 (d) |
| 2 | `/dossier/:id` | noto asset **3** LGS310C | 1280×900 | 768×900 | 390×900 | nessun (a) |
| 3 | `/inventory` | — | 1280×900 | 768×900 | 390×900 | #5 (b) |
| 4 | `/monitoring` | — | 1280×900 | 768×900 | 390×900 | #6 (b) |
| 5 | `/timeline` | — | 1280×900 | 768×900 | 390×900 | **#1 (a)** corretto; #7 (b) |
| 6 | `/actions` | — | 1280×900 | 768×900 | 390×900 | nessun difetto rilevato |
| 7 | `/dashboard` | — | 1280×900 | 768×900 | 390×900 | #8 (d/e) |
| 8 | `/findings` | stato vuoto | 1280×900 | 768×900 | 390×900 | #9 (c) — solo se tabelle popolate; oggi vuoto |
| 9 | `/osservatorio` | stub | 1280×900 | 768×900 | 390×900 | nessun difetto rilevato |
| 10 | `/come-funziona` | stub | 1280×900 | 768×900 | 390×900 | nessun difetto rilevato |
| 11 | `/incidents` | — | 1280×900 | 768×900 | 390×900 | #10 (e) |
| 12 | `/runbook` | — | 1280×900 | 768×900 | 390×900 | **#2/#3 (a)** corretti; #11 (b) |

### Tabella difetti (formato O9)

| # | rotta | bp | file/componente | cosa si vede oggi | cosa dovrebbe vedersi | categoria |
|---|---|---|---|---|---|---|
| 1 | `/timeline` | 390 | `Timeline.vue` `.timeline-event` | `docW=726` · card ~697px · bottoni «Silenzia…» OOB (R≈716); testo CTA tagliato; `body overflow-x:hidden` clippa | card ≤ viewport; CTA leggibile/raggiungibile senza overflow documento | **(a) rotto** — **CORRETTO** (`min-width:0` + contain) |
| 2 | `/runbook` | 768 | `matrix.css` `.md-body table` | `docW>vw` · TABLE ~1157px espande documento, clip senza scroll | tabella in scrollport locale | **(a) rotto** — **CORRETTO** |
| 3 | `/runbook` | 390 | idem | come #2 a 390 | idem | **(a) rotto** — **CORRETTO** |
| 4 | `/dossier/112` | 390 | `Dossier.vue` nome | `legacy_manual` badge + testo ripetuto | una sola resa provenance | (d) incoerente → **O10** |
| 5 | `/inventory` | 390 | `Inventory.vue` | lista densa; ellissi nome/MAC | densità leggibile | (b) → **O10** |
| 6 | `/monitoring` | 390 | `Monitoring.vue` | tabelle dense in `.table-scroll-x` | densità | (b) → **O10** |
| 7 | `/timeline` | 390 | `Timeline.vue` summary/h2 | ellissi intenzionale su summary/IP | densità (non overflow) | (b) → **O10** |
| 8 | `/dashboard` | * | `Dashboard.vue` | slot ready vs live | coerenza | (d)/(e) → **O10** |
| 9 | `/findings` | 390/768 | `Findings.vue` tabella | **oggi vuoto** («Nessun finding»); con righe, Salva fuori fold senza H-scroll | azione Salva raggiungibile senza H-scroll obbligatorio | (c) → **O10** (non esercitato su dati vuoti) |
| 10 | `/incidents` | 390 | `Incidents.vue` | layout ok funzionalmente | rifinitura | (e) → **O10** |
| 11 | `/runbook` | 390 | `.md-body` | trunc candidati (celle/ellipsis) post-fix | densità testo | (b) → **O10** |

### Conteggio

| categoria | n | note |
|---|---|---|
| (a) rotto | **3** | tutti corretti in questa ondata |
| (b) illeggibile/densità | 4 | #5 #6 #7 #11 → O10 |
| (c) lento | 1 | #9 → O10 |
| (d) incoerente | 2 | #4 #8 → O10 |
| (e) estetico | 2 | #8 #10 → O10 (+ densità plant/oggi già O9) |

**Scarti vs previsioni:** inventory/monitoring **senza** (a) overflow misurato (previsione troppo pessimista). Timeline e runbook (a) **confermati**. Findings senza dati → (c) non osservabile ora (etichettato, non inventato).

---

## Y3 — correzioni (a)

1. **Timeline:** `.timeline-event` / list / panel `min-width:0` + `overflow:hidden` — blocca min-content da `h2`/`summary` nowrap in CSS grid.  
2. **Runbook:** `.md-body { overflow-x:auto }` + table `width:max-content` — scrollport locale, documento non espande.

Diff: `obs-o9fix-rotto.diff.txt`.  
**Nessun cambio semantica dati.**

### Rinviati O10 (enumerati)

- #4 dossier provenance doppia (d)
- #5 inventory densità 390 (b)
- #6 monitoring densità 390 (b)
- #7 timeline ellissi summary (b)
- #8 dashboard coerenza slot (d/e)
- #9 findings Salva+H-scroll quando popolato (c)
- #10 incidents estetico (e)
- #11 runbook trunc celle (b)
- **già O9:** densità mobile `#6 /plant@390`, `#8 /oggi@390`
- armonizzazione cromatica favicon (scelta A bloccata — non riaprire)

---

## Y4 — PNG · larghezze reali · assert

Tutti i file sotto `docs/o9fix-captures/` (e flat in share). Altezza viewport **900**.

`o9_png_assert.py --pair` (esito):

- dossier-solo-l2 1280↔390 → **PASS**
- timeline 1280↔390 → **PASS**
- inventory 768↔390 → **PASS**
- runbook 768↔390 → **PASS**

Coppie **prima/dopo** (a):

- `obs-o9fix-timeline-390-prima.png` / `-dopo.png`
- `obs-o9fix-runbook-390-prima.png` / `-dopo.png`
- `obs-o9fix-runbook-768-prima.png` / `-dopo.png`

---

## Deploy · breaker · gate · invarianti

- **Bump 0.10.73** (runtime (a) corretto). Deploy `./scripts/deploy.sh web`. Recreate `api` solo per `/VERSION` → health `0.10.73`.
- Breaker (misurato post-ciclo): **FA_TOTAL=906** · **FA_DAY=188** (`date(observed_at)=today`) · **DB=1805.12 MiB** · stato **closed** · tetti non alzati. (`FA_DAY` O9 era 580 su metrica analoga — delta giorno diverso; non è soglia nuova.)
- `w8_currency_gate.py`: **VIOLAZIONI 0 · PASS (1 temporanea)** `DEBT-WPGATE-CURRENCY-COUNT-LOCAL`
- I6 `grep -RInE 'scoreSpecificity|specificity' api/`: **VUOTO**
- **FA 251** invariato: `asset.name` · subject chassis **24** · `LGS310C` · manual/100/current
- Favicon: **non toccata** in questa ondata (opzione A resta)

### Criteri di fallimento (uno per uno)

| Criterio | Esito |
|---|---|
| rotta Y2 non ispezionata/catturata ×3 | **PASS** — 12 URL × 3 |
| due PNG breakpoint stessa larghezza | **PASS** — assert pair |
| (b)(c)(d)(e) corretti invece di rinviati | **PASS** — solo (a) |
| (a) rilevato non corretto | **PASS** — #1–#3 fix |
| stima come misura | **PASS** — Y1 etichettata |
| etichette I1/I2 perse | **PASS** |
| azione irraggiungibile @390 | **PASS** — timeline CTA ripristinata |
| nuovo hub vs Oggi | **PASS** |
| scala P1–P6 rimossa | **PASS** (non toccata) |
| FA 251 modificato | **PASS** |
| favicon/scelta A | **PASS** |
| scoreSpecificity fuori triageRules | **PASS** I6 |
| FactAssertion fuori facts/ / allowlist | **PASS** gate |
| semantica dati | **PASS** |
| Y0/Y1 cancellano report | **PASS** — solo annotate |
| boot/backup/DB/_w4a/T7 | **PASS** |
| diff monolitico | **PASS** — rotto tematico |

---

## STOP

STOP per review. **Non** avviare O10 · **non** chiudere cantiere · **non** merge main. FA 251 intatto in attesa di Michele.
