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

Asset SHA (PNG+diff+previsioni): `256f30785d530d32a26697da0b67813572479801`
Base: `https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/`

| file | note | sha256 |
|---|---|---|
| [obs-o10-dashboard-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-dashboard-1280.png) | 1280×900 | `ca2632586c7eb0d8ca00fa1c4e4e1ef8b5d10faaa0e056f0a045c841b167878f` |
| [obs-o10-dashboard-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-dashboard-390.png) | 390×900 | `9a8f1dbe99df42f01eae002504b1087f76c33a7d14bb5a12efda4cbf6d6113cb` |
| [obs-o10-dashboard-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-dashboard-768.png) | 768×900 | `2e13fdf90b0e02a4eb2e2cd961cfd74517b0c173ea2e2938fd5cb216d6fc4933` |
| [obs-o10-densita.diff.txt](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-densita.diff.txt) | 22 lines | `42a2a066968515ce9ac0c252b460b0d6b03337594c432ad07a86057cd6096d56` |
| [obs-o10-dossier-noto-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-dossier-noto-1280.png) | 1280×900 | `93e864925e0f5016c7ca009f3bf524276ca7090786ae340c785943af2fa9ec54` |
| [obs-o10-dossier-noto-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-dossier-noto-390.png) | 390×900 | `9888db004afc3d1f0367552b7bcb8235e2195474fc3292cf2e50cdd174600ac1` |
| [obs-o10-dossier-noto-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-dossier-noto-768.png) | 768×900 | `c8d7befbff33ec76cf49ceb2244c347f7b98fb7f0836f53a30e6e20ec97bdb61` |
| [obs-o10-findings-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-findings-1280.png) | 1280×900 | `9acb961f9c937f1c7ef383ee26e13dbb84e4bb990868d033ecefb1af658d0913` |
| [obs-o10-findings-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-findings-390.png) | 390×900 | `35aaec6d1592ed18c4009788dfa9872934c4341e23635413fc87d7624f57c005` |
| [obs-o10-findings-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-findings-768.png) | 768×900 | `ef0bb5eaf66063916b9dd0dc05b9899ea96f95778429c764cfc0deb0efc33694` |
| [obs-o10-incidents-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-incidents-1280.png) | 1280×900 | `5b3cce53783efcff0893838cb6dbc914e4a3ce272687e8174c74a6e578483a09` |
| [obs-o10-incidents-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-incidents-390.png) | 390×900 | `8fed6e3282ebe51274f9a37e87b4a23fdb8b3504a4adf6e2500c8d8562f877ed` |
| [obs-o10-incidents-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-incidents-768.png) | 768×900 | `25ef3a4adf52f53d89c83506058fe39c8581a4eeaef0635d4858e5b0fec1bff4` |
| [obs-o10-inventory-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-inventory-1280.png) | 1280×900 | `4f1ff804a55be03263b95cb3c0c76ae3712ecfd8fa67670883271779a2c84b58` |
| [obs-o10-inventory-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-inventory-390.png) | 390×6386 | `2ab46780ab51100d6b67ed25316288a62028f342b241fa9bdba49cdb330d6f52` |
| [obs-o10-inventory-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-inventory-768.png) | 768×900 | `6e07b2bd0801e2254a61b791cf1b1ce7295c1da3a9db4ab46a00be803e41c451` |
| [obs-o10-leggibilita.diff.txt](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-leggibilita.diff.txt) | 19 lines | `e909f5ee636ac2c59760057e66a12583be6baca1216fc692ec3e873cf144403b` |
| [obs-o10-monitoring-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-monitoring-1280.png) | 1280×900 | `d4e210dd923d7aa3fb06da3d626a4c06b656199fef60321b020a2c7bd7a31af6` |
| [obs-o10-monitoring-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-monitoring-390.png) | 390×1431 | `e153224db1f02a71bbb2fa832f880a329c8673e0c4e514cada609be15686c4c8` |
| [obs-o10-monitoring-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-monitoring-768.png) | 768×900 | `2f2bc21585bc29bc13d04c347797e056e3463157b2910fe6f2bf841eb0e29d70` |
| [obs-o10-oggi-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-oggi-1280.png) | 1280×900 | `a8b0b34c8fe21e015ccd24f5600e6240d5e2d0dd6a56c9863a03cae186a40b68` |
| [obs-o10-oggi-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-oggi-390.png) | 390×13228 | `9731ebf27aefe5c2bbe5b4f8d54d61c65a5be512bdfe39d3d56d8c09e6fce434` |
| [obs-o10-oggi-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-oggi-768.png) | 768×900 | `5b4ca60ac7afc49583678acd9fdb505de987924db66b5b38560d8fef9ad45643` |
| [obs-o10-plant-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-plant-1280.png) | 1280×900 | `75d8ce4926539a9c514370032dc8e11ff7e160b649afb85cbd0d0949d41f3aa3` |
| [obs-o10-plant-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-plant-390.png) | 390×5442 | `ac29e0039bb997ab9194449a92afe1f1aeb29c215a354cbc2d77b45c80921a76` |
| [obs-o10-plant-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-plant-768.png) | 768×900 | `fad309de40650cfe5a69a78faeed54b601a1a67de2dfe7e7ec8bd7a3ee0bd956` |
| [obs-o10-previsioni.md](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-previsioni.md) | 59 lines | `cf0904084460ea37375cbcc71b87b5095e9850730ba0a78f3de37d160ec3aed8` |
| [obs-o10-runbook-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-runbook-1280.png) | 1280×900 | `653d6b698eb42f2bee1817010233cac3c5202f1954447ac1a346a3d0638a613b` |
| [obs-o10-runbook-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-runbook-390.png) | 390×10780 | `63759b8cb2b7ffd91154a6cd9b6c500017ae817e90d57da4f0441d57268de6ff` |
| [obs-o10-runbook-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-runbook-768.png) | 768×900 | `e0778e9d77612bfc407968a3024b7685069842e5afaa6fd7ec0070aeb44c82e0` |
| [obs-o10-timeline-1280.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-timeline-1280.png) | 1280×900 | `77414333028684c9e5f203cffe0fb62ec7e4ef74fbd4f72ddc1885b8f5fa9a9b` |
| [obs-o10-timeline-390.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-timeline-390.png) | 390×13400 | `f75346dc8edfac813f99823b9357d4faeaf47cce5627aa5dee813a2dd641dd22` |
| [obs-o10-timeline-768.png](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-timeline-768.png) | 768×900 | `f87955e9d7dd722e310ff149db3a55a5d537edb2e345d25b52504e390409e9da` |
| [obs-o10-vocabolario.diff.txt](https://raw.githubusercontent.com/Mooflotic/obs-exchange/256f30785d530d32a26697da0b67813572479801/obs-o10-vocabolario.diff.txt) | 21 lines | `08c932bd5b337810e3f608bf58e91dcb870a6925ca93c5e23f2ec953f2740edd` |
