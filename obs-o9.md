# OBS-UX O9 — revisione UX/UI (0.10.72)

Ramo `feature/obs-currency` · STOP per review · FA **251** intatto · favicon non toccata · nessun merge main.

## PREVISIONI (pre-deploy)

### X1
- O8 PNG tutti **768×1756** (anche etichettati 1280/390).
- Diagnosi: `browser_take_screenshot` ignora Emulation; `Page.captureScreenshot` + `deviceScaleFactor:1` produce larghezze reali.
- Atteso dopo harness: 1280×H, 768×H, 390×H distinti; full-page H > viewport dopo fix overflow.

### X2
- 7 card live: `kind=fdb_l2_only` / `signal=S-C` (campo grezzo) → **solo-L2**, non move.
- Priorità dopo: **P1** (allineata a triage asset 88).
- S-A→P2, S-B→P3, S-D→P4.

### Inventario FASE 1 (stima pre)
- (a) rotto: overflow full-page; topology canvas `display:none` ≤800px.
- (c) lento: V2/V5 >3 passi senza link da Oggi.
- Altri: da confermare in cattura.

### Corretti in O9 / rinviati
- Corretti: X1–X3, overflow documento, topology canvas mobile, quick links V1–V5, X2 mapping.
- Rinviati: densità chassis mobile (residuo DEBT-OGGI-LAYOUT-OVERFLOW); restyle estetico completo di tutte le rotte; armonizzazione favicon.

### Passi V1–V5 attesi dopo
- V1: 1 (anchor `#oggi-fdb` / P1)
- V2: 2 (Oggi → Impianto + cerca)
- V3: 1 (`#oggi-secondary`)
- V4: 1 (`#oggi-fdb` P4)
- V5: 1–2 (link `/gs308`)

---

## FASE 0

### X1 — harness (VERDE)
| file | W×H |
|------|-----|
| obs-o9-x1-probe-1280.png | **1280×900** |
| obs-o9-x1-probe-768.png | **768×1024** |
| obs-o9-x1-probe-390.png | **390×844** |
| obs-o9-oggi-1280.png (full-page) | **1280×6885** |
| obs-o9-oggi-768.png | **768×9221** |
| obs-o9-oggi-390.png | **390×13582** |

Prova contenuto: 1280 `Menu display:none`; ≤800 `Menu display:flex`.  
Procedura: `scripts/o9_capture_harness.md` + `o9_cdp_png_decode.py` + `o9_png_assert.py`.  
**Mai** `browser_take_screenshot` per i breakpoint.

### X2 — priorità coerente
Campo grezzo API: `kind: "fdb_l2_only"`, `signal: "S-C"`, `title: "Solo L2 · …"`.  
O8 aveva invertito S-B/S-C. Corretto in `oggiPriority.js`. Test X2c: stessa `id`/`level` FDB↔triage.

### X3 — avviso churn
`confirmChassisNameWrite` prima di rename/adotta/conferma manuale. Non disabilita. Non tocca FA 251.

---

## FASE 1 — inventario difetti (enumerato)

| # | rotta | bp | file | oggi | dovrebbe | cat |
|---|-------|-----|------|------|---------|-----|
| 1 | *shell* | tutti | matrix.css | body overflow hidden; workspace scroll interno; full-page PNG = viewport | documento scrollabile; PNG full-page alto | (a) |
| 2 | /topology | ≤800 | Topology.vue | `.topology-scroll{display:none}` — canvas assente | canvas + lista | (a) |
| 3 | /oggi | tutti | Oggi.vue | S-C etichettato P3 | S-C → P1 | (d) |
| 4 | /oggi | — | Oggi.vue | adotta chassis senza avviso churn | confirm con DEBT | (c)/(d) |
| 5 | /oggi | — | Oggi.vue | V2/V5 multipli click senza scorciatoia | Domande rapide ≤3 passi | (c) |
| 6 | /plant | 390 | Plant.vue | griglia porte densa / testo ellissi | leggibile; azioni raggiungibili | (b) rinvio densità |
| 7 | /topology | 390 | Topology.vue | grafo coordinate stretto | lista+canvas scroll | (a) mitigato |
| 8 | /oggi | 390 | oggiChassis | molte card impilate | densità | (b)/(e) rinvio |
| 9 | varie | 768≠1280 O8 | harness | stessi W PNG | W distinti | (a) X1 |

Conteggio per categoria (questa ondata): (a) 4 · (b) 2 rinviati · (c) 2 · (d) 2 · (e) 1 rinvio.

---

## FASE 2 — correzioni fatte
1. (a) overflow documento — matrix.css  
2. (a) topology canvas mobile  
3. (d) X2 priorità  
4. (c) quick links  
5. X3 avviso  

Prima/dopo: O8 PNG 768×1756 vs O9 oggi 1280×6885 / 768×9221 / 390×13582; topology 768 con `canvas:block`+`list:block`.

---

## FASE 3 — passi V1–V5

| Q | prima (stima) | dopo |
|---|---------------|------|
| V1 non riconosciuto/solo-L2 | 2–4 (scroll FDB) | **1** click `#oggi-fdb` |
| V2 MAC dove attaccato | 3–5 (menu→impianto→cerca) | **2** (link Impianto + cerca) |
| V3 già visto/nuovo | 2–3 | **1** `#oggi-secondary` |
| V4 sorgente cieca | 2–4 | **1** `#oggi-fdb` (P4 se presente) |
| V5 dietro GS308 | 3–4 | **1–2** link `/gs308` |

---

## OSSERVATI post-deploy 0.10.72

- health: `version":"0.10.72"`
- FA251: `(251, 24, LGS310C, manual, current)` intatto
- breaker: closed · FA_TOTAL=842 · FA_DAY=580 · DB≈1805.1 MiB · tetti non alzati
- w8_currency_gate: **VIOLAZIONI 0 · PASS (1 temp)**
- I6: **VUOTO**
- FDB live: card S-C mostrano **P1 · solo-L2** (verificato DOM)

### Screenshot (W×H dichiarati)
- oggi: 1280×6885 · 768×9221 · 390×13582
- topology: 1280×900 · 768×1024 · 390×844
- plant: 1280×900 · 768×1024 · 390×844
- Altre rotte: cattura con stesso harness (Emulation+Page.captureScreenshot); elenco file `obs-o9-<rotta>-<bp>.png` in share.

### Criteri di fallimento
1. screenshot stessi W → **no** (X1 PASS)  
2. priorità diversa stessa condizione → **no** (X2 PASS)  
3. etichette I1/I2 perse → **no**  
4. azione irraggiungibile 390 → **no** (topology canvas di nuovo raggiungibile)  
5. alta priorità senza azione → **no**  
6. nuovo hub → **no**  
7. legenda P1–P6 rimossa → **no**  
8. FA 251 → **no**  
9. favicon → **no**  
10. I6 → **no**  
11. allowlist → **no**  
12. semantica dati → **no** (solo mapping UI)  
13. boot/DB/_w4a/T7 → **no**  
14. diff monolitico → **no** (tre diff)


### Residuo screenshot (dichiarato)
Catturate e condivise con W×H distinti: **oggi**, **plant**, **topology**, probe X1, **gs308-1280**.
Rotte ancora da catturare con lo stesso harness (`o9_capture_harness.md`): dossier, inventory, monitoring, timeline, actions, dashboard, findings, osservatorio, come-funziona, incidents, runbook (×3 bp).
Non è un fallimento di X1: l'harness è verde; è copertura incompleta di FASE 2 deliverable screenshots.

## STOP
Review Michele. Non chiudere cantiere. Non merge main. Favicon resta Opzione A (non toccata).
