# OBS-UX O10 — vocabolario visivo, densità mobile, leggibilità

**Runtime:** 0.10.74 · deploy `web` (+ recreate `api` remount VERSION) · `feature/obs-currency`  
**Harness:** viewport reale + `deviceScaleFactor:1` + full-page su W2 @390 · **mai** `browser_take_screenshot`.  
**O9 / O9-FIX:** non ritoccate (X1–X3, harness, overflow doc, topology, V1–V5, S-C→P1, (a) timeline/runbook).

---

## W0 — versione realmente servita (bloccante)

| Check | Risultato |
|---|---|
| (a) `GET /api/health` | **0.10.74** (dopo remount; pre-O10 era 0.10.73) |
| (b) Footer versione | **runtime** da `/api/health` — `App.vue` `refreshRuntimeVersion()` → `api.health()` → `versionLabel` = `v${ver} · ${buildId}`. **Non** compilata nel bundle. |
| (c) CSS servito pre-O10 | asset `index-D5IEcFjC.css` conteneva già O9-FIX: `.timeline-event…{min-width:0…}`, `.md-body{overflow-x:auto…}`, `.md-body table{width:max-content…}` |
| (d) hash | prova diretta sulle regole CSS, non sul numero versione |

**Esito W0: (i)** — O9-FIX confermata in produzione. Footer 0.10.72 osservato da Michele = health/api non ancora rimontato o sessione pre-refresh; **non** bundle web stale rispetto alle correzioni (a).

### W0 post-deploy O10
CSS servito nuovo: `index-Ci_sXu7j.css` (sha256 `bf7f5cfd…`) contiene `oggi-collapse`, `timeline-read-collapse`, `col-action` sticky, `status-badge.muted`→`--text-2`, O9-FIX retained.

## W0-bis
O9-FIX: catture viewport 900px = solo primo schermo; overflow X via `docW` globale. **O10 densità = full-page** (PNG @390 con altezza = `scrollHeight`).

---

## Previsioni → osservati

Vedi `obs-o10-previsioni.md`.

### Height full-page @390 (misurate)

| Rotta | prima | dopo | Δ | scarto vs stima |
|---|---|---|---|---|
| `/oggi` | 13680 | 13228 | −452 | collasso legenda/coda; P1 FDB restano → riduzione contenuta |
| `/plant` | 5972 | 5442 | −530 | copertura FDB in `<details>` |
| `/inventory` | 6386 | 6386 | 0 | solo contrasto (previsto lieve) |
| `/monitoring` | 1431 | 1431 | 0 | già compatta |
| `/timeline` | 19210 | 13400 | **−5810** | già-letti collassati |
| `/runbook` | 10780 | 10780 | 0 | wrap celle; no collasso sezioni md (evitato semantic risk) |

### Contrasto WCAG 2.1 AA (misurato)

| Elemento | prima | dopo | AA normal |
|---|---|---|---|
| `--text-3` / `--inv-faint` su `--bg-0` | **3.74:1** | non usato per meta testo | FAIL → evitato |
| `--text-2` / `--inv-mut` / `--muted` su `--bg-0` | 7.23:1 | 7.23:1 | PASS |
| `StatusBadge.muted` | text-3 (~3.47 su bg-1) | **text-2** | PASS |
| Inventory meta/subtitle/empty | inv-faint | **inv-mut** | PASS |

---

## W1 — vocabolario unico

`web/src/visualVocab.js` + `VisualBadge.vue` (StatusBadge + tone `infer`):

- provenienza: manuale · manuale-legacy · inferenza · non nota  
- freschezza: fresco · vecchio(+data) · non misurato(+motivo) · non coperto  
- priorità: P1–P6 (legenda O8)  
- riconoscimento: atteso · non riconosciuto · ignorato  
- slot: waiting · ready · live  

**#4** Dossier: un solo `VisualBadge` (niente chip+label duplicati).  
**#8** ReadySlot: stesso shell card + badge vocabolario (niente dashed/opacity parallela).

---

## Difetti #4–#11

| # | esito | note |
|---|---|---|
| 4 | **corretto** | W1 |
| 5 | **corretto** | contrasto meta inventory |
| 6 | **parziale** | monitoring già muted AA; densità già bassa |
| 7 | **corretto** | title + collapse già-letti |
| 8 | **corretto** | W1 ReadySlot |
| 9 | **layout + fixture test** | sticky `col-action`; **K4 live non esercitato** (vuoto, no fake) |
| 10 | **corretto** | W4 incidents wrap/grid |
| 11 | **corretto** | md cells wrap + title path via overflow-wrap |
| O9 plant/oggi densità | **trattati** in W2 | height misurate sopra |

Favicon armonizzazione: **rinviata**.

---

## Deploy · breaker · gate

- VERSION **0.10.74** · `./scripts/deploy.sh web` · health **0.10.74**
- Breaker: FA_TOTAL=**918** · FA_DAY=**200** · DB=**1805.12 MiB** · closed · tetti non alzati
- `w8_currency_gate.py`: **VIOLAZIONI 0 · PASS (1 temp)**
- I6: **VUOTO**
- FA **251** invariato: chassis 24 · asset.name · LGS310C · manual/100/current
- Favicon: non toccata in questa ondata

### Criteri di fallimento

| Criterio | Esito |
|---|---|
| W0 senza prova CSS servito | **PASS** |
| correzione assente dal bundle | **PASS** (marker CSS verificati) |
| densità nasconde P1 | **PASS** (P1 aperti; già-letti dichiarati) |
| etichette I1/I2 perse | **PASS** |
| collasso senza conteggio/priorità | **PASS** |
| troncamento senza valore intero | **PASS** (title) |
| contrasto sotto AA senza motivo | **PASS** |
| soglia a gusto | **PASS** (solo WCAG / misure) |
| finding fittizi in prod | **PASS** |
| test spacciato per prod | **PASS** (K4 dichiarato) |
| azione irraggiungibile @390 | **PASS** |
| hub vs Oggi | **PASS** |
| legenda P1–P6 rimossa | **PASS** |
| FA 251 / favicon / I6 / currency | **PASS** |
| semantica dati / DB / T7 | **PASS** |
| diff monolitico | **PASS** — tre diff tematici curtati |

---

## STOP

STOP per review. Non avvio armonizzazione favicon. Non chiudo cantiere. Non merge main. FA 251 intatto.

## Share (commit-pinned)

Asset SHA (PNG+diff+previsioni): 
Base: 

| file | note | sha256 |
|---|---|---|
| [obs-o10-dashboard-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-dashboard-1280.png) | 1280×900 |  |
| [obs-o10-dashboard-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-dashboard-390.png) | 390×900 |  |
| [obs-o10-dashboard-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-dashboard-768.png) | 768×900 |  |
| [obs-o10-densita.diff.txt](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-densita.diff.txt) | 22 lines |  |
| [obs-o10-dossier-noto-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-dossier-noto-1280.png) | 1280×900 |  |
| [obs-o10-dossier-noto-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-dossier-noto-390.png) | 390×900 |  |
| [obs-o10-dossier-noto-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-dossier-noto-768.png) | 768×900 |  |
| [obs-o10-findings-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-findings-1280.png) | 1280×900 |  |
| [obs-o10-findings-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-findings-390.png) | 390×900 |  |
| [obs-o10-findings-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-findings-768.png) | 768×900 |  |
| [obs-o10-incidents-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-incidents-1280.png) | 1280×900 |  |
| [obs-o10-incidents-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-incidents-390.png) | 390×900 |  |
| [obs-o10-incidents-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-incidents-768.png) | 768×900 |  |
| [obs-o10-inventory-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-inventory-1280.png) | 1280×900 |  |
| [obs-o10-inventory-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-inventory-390.png) | 390×6386 |  |
| [obs-o10-inventory-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-inventory-768.png) | 768×900 |  |
| [obs-o10-leggibilita.diff.txt](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-leggibilita.diff.txt) | 19 lines |  |
| [obs-o10-monitoring-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-monitoring-1280.png) | 1280×900 |  |
| [obs-o10-monitoring-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-monitoring-390.png) | 390×1431 |  |
| [obs-o10-monitoring-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-monitoring-768.png) | 768×900 |  |
| [obs-o10-oggi-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-oggi-1280.png) | 1280×900 |  |
| [obs-o10-oggi-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-oggi-390.png) | 390×13228 |  |
| [obs-o10-oggi-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-oggi-768.png) | 768×900 |  |
| [obs-o10-plant-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-plant-1280.png) | 1280×900 |  |
| [obs-o10-plant-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-plant-390.png) | 390×5442 |  |
| [obs-o10-plant-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-plant-768.png) | 768×900 |  |
| [obs-o10-previsioni.md](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-previsioni.md) | 59 lines |  |
| [obs-o10-runbook-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-runbook-1280.png) | 1280×900 |  |
| [obs-o10-runbook-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-runbook-390.png) | 390×10780 |  |
| [obs-o10-runbook-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-runbook-768.png) | 768×900 |  |
| [obs-o10-timeline-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-timeline-1280.png) | 1280×900 |  |
| [obs-o10-timeline-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-timeline-390.png) | 390×13400 |  |
| [obs-o10-timeline-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-timeline-768.png) | 768×900 |  |
| [obs-o10-vocabolario.diff.txt](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-vocabolario.diff.txt) | 21 lines |  |
