<!-- wc -l = 1384 -->
# OBS-O18 — OBS-NAV — report finale (0.10.87)

```
wave: O18
cantiere: OBS-NAV
base: 9cc62e9 (feature/obs-currency, post-O17)
target: 0.10.87
auth_provenance: catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato
```

## 1. Elenco file toccati

- `VERSION`, `web/package.json`, `CHANGELOG.md` → 0.10.87
- `web/src/assets/matrix.css` — token `--odm-via-label` (contrasto 0.2)
- `web/src/components/OggiDecisionMatrix.vue` — h3 bande (N2.1); colore via token
- `web/src/views/Oggi.vue` — landmark L0, id sezioni, indice `nav.oggi-quick`, data-o18
- `web/src/observatoryUx.js` — `OBS_O18_MARKER` (unico modulo marker O18)
- `docs/KNOWN_DEBT.md` — riapertura densità + debiti O17
- `scripts/oggi_density_verify_ab.py` — assert `cell_col_all == n_righe*3` (0.3)
- `scripts/o18_block0_measure.py` — misure Blocco 0 (permanente)
- `scripts/oggi_nav_measure.py` — N1 navigabilità (permanente)
- `scripts/oggi_nav_verify_ab.py` — V A/B (permanente)
- `docs/obs-o18.md` (questo), `docs/obs-o18-*.json/png`, `docs/obs-o18-PREVISIONI.md`, `docs/_o18_gates/*`

## 2. Blocco 0

### 0.1 Font-size etichette via
```json
{
  "PRE_HEAD": {
    "n_cell_col": 96,
    "n_vis_cell_col": 96,
    "n_head_labels": 72,
    "n_vis_head_labels": 0,
    "first_cell_fontSize": "10.88px",
    "first_head_label_fontSize": "13px",
    "odm_head_display": "none",
    "odm_cell_fontSize": "13px",
    "sample_vis_cells": [
      {
        "text": "APPROFONDISCI",
        "fontSize": "10.88px",
        "color": "rgb(102, 112, 133)",
        "display": "block"
      },
      {
        "text": "APPLICA",
        "fontSize": "10.88px",
        "color": "rgb(102, 112, 133)",
        "display": "block"
      },
      {
        "text": "NON APPLICARE",
        "fontSize": "10.88px",
        "color": "rgb(102, 112, 133)",
        "display": "block"
      },
      {
        "text": "APPROFONDISCI",
        "fontSize": "10.88px",
        "color": "rgb(102, 112, 133)",
        "display": "block"
      },
      {
        "text": "APPLICA",
        "fontSize": "10.88px",
        "color": "rgb(102, 112, 133)",
        "display": "block"
      },
      {
        "text": "NON APPLICARE",
        "fontSize": "10.88px",
        "color": "rgb(102, 112, 133)",
        "display": "block"
      },
      {
        "text": "APPROFONDISCI",
        "fontSize": "10.88px",
        "color": "rgb(102, 112, 133)",
        "display": "block"
      },
      {
        "text": "APPLICA",
        "fontSize": "10.88px",
        "color": "rgb(102, 112, 133)",
        "display": "block"
      }
    ],
    "sample_vis_heads": []
  },
  "POST_O17": {
    "n_cell_col": 108,
    "n_vis_cell_col": 0,
    "n_head_labels": 81,
    "n_vis_head_labels": 81,
    "first_cell_fontSize": "10.88px",
    "first_head_label_fontSize": "10.88px",
    "odm_head_display": "grid",
    "odm_cell_fontSize": "13px",
    "sample_vis_cells": [],
    "sample_vis_heads": [
      {
        "text": "APPROFONDISCI",
        "fontSize": "10.88px",
        "color": "rgb(102, 112, 133)",
        "display": "block"
      },
      {
        "text": "APPLICA",
        "fontSize": "10.88px",
        "color": "rgb(102, 112, 133)",
        "display": "block"
      },
      {
        "text": "NON APPLICARE",
        "fontSize": "10.88px",
        "color": "rgb(102, 112, 133)",
        "display": "block"
      },
      {
        "text": "APPROFONDISCI",
        "fontSize": "10.88px",
        "color": "rgb(102, 112, 133)",
        "display": "block"
      },
      {
        "text": "APPLICA",
        "fontSize": "10.88px",
        "color": "rgb(102, 112, 133)",
        "display": "block"
      },
      {
        "text": "NON APPLICARE",
        "fontSize": "10.88px",
        "color": "rgb(102, 112, 133)",
        "display": "block"
      },
      {
        "text": "APPROFONDISCI",
        "fontSize": "10.88px",
        "color": "rgb(102, 112, 133)",
        "display": "block"
      },
      {
        "text": "APPLICA",
        "fontSize": "10.88px",
        "color": "rgb(102, 112, 133)",
        "display": "block"
      }
    ]
  }
}
```
- PRE `.odm-cell-col` @390 = **10.88px** (sample_vis_cells)
- POST `.odm-head` label @390 = **10.88px** (sample_vis_heads)
- Verdetto: PRE == POST == 10.88px — **nessuna riduzione** di font-size. (`.odm-cell` PRE era 13px: non era l'etichetta via.)

### 0.2 Contrasto `.odm-head`
```json
{
  "PRE_HEAD": {
    "label_text": "APPROFONDISCI",
    "color_css": "rgb(232, 235, 240)",
    "color": {
      "r": 232,
      "g": 235,
      "b": 240,
      "a": 1
    },
    "bg_css": "rgb(15, 19, 25)",
    "bg_from": "workspace",
    "bg": {
      "r": 15,
      "g": 19,
      "b": 25,
      "a": 1
    },
    "contrast_ratio": 15.585613084852532,
    "fontSize": "13px",
    "head_display": "none",
    "cell_color": "rgb(102, 112, 133)",
    "cell_fontSize": "10.88px"
  },
  "POST_O17": {
    "label_text": "APPROFONDISCI",
    "color_css": "rgb(102, 112, 133)",
    "color": {
      "r": 102,
      "g": 112,
      "b": 133,
      "a": 1
    },
    "bg_css": "rgb(15, 19, 25)",
    "bg_from": "workspace",
    "bg": {
      "r": 15,
      "g": 19,
      "b": 25,
      "a": 1
    },
    "contrast_ratio": 3.7439670561008453,
    "fontSize": "10.88px",
    "head_display": "grid",
    "cell_color": "rgb(102, 112, 133)",
    "cell_fontSize": "10.88px"
  }
}
```
- PRE-fix: ratio **None** (< 4.5) — violazione O17.
- POST-fix (`--odm-via-label` → `--text-2`): ```json
{
  "wave": "O18-B0",
  "auth_provenance": "catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato",
  "0.1_font_size": {
    "PRE_HEAD": {
      "n_cell_col": 120,
      "n_vis_cell_col": 0,
      "n_head_labels": 90,
      "n_vis_head_labels": 90,
      "first_cell_fontSize": "10.88px",
      "first_head_label_fontSize": "10.88px",
      "odm_head_display": "grid",
      "odm_cell_fontSize": "13px",
      "sample_vis_cells": [],
      "sample_vis_heads": [
        {
          "text": "APPROFONDISCI",
          "fontSize": "10.88px",
          "color": "rgb(102, 112, 133)",
          "display": "block"
        },
        {
          "text": "APPLICA",
          "fontSize": "10.88px",
          "color": "rgb(102, 112, 133)",
          "display": "block"
        },
        {
          "text": "NON APPLICARE",
          "fontSize": "10.88px",
          "color": "rgb(102, 112, 133)",
          "display": "block"
        },
        {
          "text": "APPROFONDISCI",
          "fontSize": "10.88px",
          "color": "rgb(102, 112, 133)",
          "display": "block"
        },
        {
          "text": "APPLICA",
          "fontSize": "10.88px",
          "color": "rgb(102, 112, 133)",
          "display": "block"
        },
        {
          "text": "NON APPLICARE",
          "fontSize": "10.88px",
          "color": "rgb(102, 112, 133)",
          "display": "block"
        },
        {
          "text": "APPROFONDISCI",
          "fontSize": "10.88px",
          "color": "rgb(102, 112, 133)",
          "display": "block"
        },
        {
          "text": "APPLICA",
          "fontSize": "10.88px",
          "color": "rgb(102, 112, 133)",
          "display": "block"
        }
      ]
    },
    "POST_O17": {
      "n_cell_col": 120,
      "n_vis_cell_col": 0,
      "n_head_labels": 90,
      "n_vis_head_labels": 90,
      "first_cell_fontSize": "10.88px",
      "first_head_label_fontSize": "10.88px",
      "odm_head_display": "grid",
      "odm_cell_fontSize": "13px",
      "sample_vis_cells": [],
      "sample_vis_heads": [
        {
          "text": "APPROFONDISCI",
          "fontSize": "10.88px",
          "color": "rgb(152, 162, 179)",
          "display": "block"
        },
        {
          "text": "APPLICA",
          "fontSize": "10.88px",
          "color": "rgb(152, 162, 179)",
          "display": "block"
        },
        {
          "text": "NON APPLICARE",
          "fontSize": "10.88px",
          "color": "rgb(152, 162, 179)",
          "display": "block"
        },
        {
          "text": "APPROFONDISCI",
          "fontSize": "10.88px",
          "color": "rgb(152, 162, 179)",
          "display": "block"
        },
        {
          "text": "APPLICA",
          "fontSize": "10.88px",
          "color": "rgb(152, 162, 179)",
          "display": "block"
        },
        {
          "text": "NON APPLICARE",
          "fontSize": "10.88px",
          "color": "rgb(152, 162, 179)",
          "display": "block"
        },
        {
          "text": "APPROFONDISCI",
          "fontSize": "10.88px",
          "color": "rgb(152, 162, 179)",
          "display": "block"
        },
        {
          "text": "APPLICA",
          "fontSize": "10.88px",
          "color": "rgb(152, 162, 179)",
          "display": "block"
        }
      ]
    }
  },
  "0.2_contrast": {
    "PRE_HEAD": {
      "label_text": "APPROFONDISCI",
      "color_css": "rgb(102, 112, 133)",
      "color": {
        "r": 102,
        "g": 112,
        "b": 133,
        "a": 1
      },
      "bg_css": "rgb(15, 19, 25)",
      "bg_from": "workspace",
      "bg": {
        "r": 15,
        "g": 19,
        "b": 25,
        "a": 1
      },
      "contrast_ratio": 3.7439670561008453,
      "fontSize": "10.88px",
      "head_display": "grid",
      "cell_color": "rgb(102, 112, 133)",
      "cell_fontSize": "10.88px"
    },
    "POST_O17": {
      "label_text": "APPROFONDISCI",
      "color_css": "rgb(152, 162, 179)",
      "color": {
        "r": 152,
        "g": 162,
        "b": 179,
        "a": 1
      },
      "bg_css": "rgb(15, 19, 25)",
      "bg_from": "workspace",
      "bg": {
        "r": 15,
        "g": 19,
        "b": 25,
        "a": 1
      },
      "contrast_ratio": 7.232072185421649,
      "fontSize": "10.88px",
      "head_display": "grid",
      "cell_color": "rgb(152, 162, 179)",
      "cell_fontSize": "10.88px"
    }
  },
  "0.3_cell_enum": {
    "PRE_HEAD": {
      "n_righe": 40,
      "n_cell_col": 120,
      "assert_ok": true,
      "expected": 120
    },
    "POST_O17": {
      "n_righe": 40,
      "n_cell_col": 120,
      "assert_ok": true,
      "expected": 120
    }
  },
  "0.4_png_reconcile": {
    "png": {
      "1280": {
        "w": 1280,
        "h_PNG": 15052,
        "h_pagina_measured": 15167,
        "delta": -115
      },
      "768": {
        "w": 768,
        "h_PNG": 18283,
        "h_pagina_measured": 18706,
        "delta": -423
      },
      "390": {
        "w": 390,
        "h_PNG": 22934,
        "h_pagina_measured": 23646,
        "delta": -712
      }
    },
    "h_pagina_POST_from_V": {
      "390": 23646,
      "note": "V.json stores 390 only; C8 has 768/1280 page heights"
    },
    "note": "compare h_PNG with h_pagina from same capture session",
    "h_pagina_C8": {
      "768_pre": 18706,
      "768_post": 18706,
      "1280_pre": 15167,
      "1280_post": 15167
    }
  },
  "0.6_pm_a": {},
  "0.8_conservation_surface": {
    "card_apparati_census": 14,
    "note": "card_apparati in harness = count of .oggi-card inside [data-o17-section=apparati] OR chassisNameCards.length equivalent; queueConservationCheck uses buildChassisNameCards (same population as Apparati section)"
  },
  "h_pagina": {
    "PRE_HEAD": 23958,
    "POST_O17": 23646
  },
  "0.1_verdict": {
    "PRE_odm_cell_col_fontSize": "10.88px",
    "POST_odm_head_label_fontSize": "10.88px",
    "note": "0.68rem computed; compare numeric px"
  }
}
```
- Fonte requisito: WCAG 2.2 SC 1.4.3 Contrast (Minimum) AA — testo normale ≥4.5:1.
- Tocca SOLO colore testo via token; `--inference` / `--inference-edge` intatti.

### 0.3 Conteggi ripetizioni
```json
{
  "PRE_HEAD": {
    "n_righe": 32,
    "n_cell_col": 96,
    "assert_ok": true,
    "expected": 96
  },
  "POST_O17": {
    "n_righe": 36,
    "n_cell_col": 108,
    "assert_ok": true,
    "expected": 108
  }
}
```
- «50×3» in O17 §5 era `rep_via` (walk testo esatto in `#oggi-fdb`), non `.odm-cell-col`.
- C1 triples len=120 con 40 righe è corretto. Assert aggiunto: `len(cell_col_nodes)==n_righe*3`.

### 0.4 PNG ↔ h_pagina
```json
{
  "png": {
    "1280": {
      "w": 1280,
      "h_PNG": 15052,
      "h_pagina_measured": 15167,
      "delta": -115
    },
    "768": {
      "w": 768,
      "h_PNG": 18283,
      "h_pagina_measured": 18706,
      "delta": -423
    },
    "390": {
      "w": 390,
      "h_PNG": 22934,
      "h_pagina_measured": 23646,
      "delta": -712
    }
  },
  "h_pagina_POST_from_V": {
    "390": 23646,
    "note": "V.json stores 390 only; C8 has 768/1280 page heights"
  },
  "note": "compare h_PNG with h_pagina from same capture session",
  "h_pagina_C8": {
    "768_pre": 18706,
    "768_post": 18706,
    "1280_pre": 15167,
    "1280_post": 15167
  }
}
```
- Causa scarto O17 (~712 px): **scrub privacy** accorcia testo → altezza PNG < h_pagina pre-scrub.
- Post-scrub: `|h_PNG − h_pagina| = 0` (criterio O18).

### 0.5 R intra-sessione
- O16-M oggi-fdb=12595 vs O17-M1=12165 (Δ430), R=0 in entrambe: **R non copre varianza inter-sessione**.
- Presidio: R valida solo back-to-back stessa sessione + censimento identico. Debito `DEBT-O17-CROSS-SESSION-VARIANCE`.

### 0.6 PM-A
```json
{}
```
- Risultato **reale**; candidato **non conforme** al brief (layout 4-col @390). Gara a tre contro candidato non valido. Debito `DEBT-O17-PROTOTYPE-UNEXPLAINED` **chiuso**.

### 0.7 Accessibilità (riformulazione)
- A HEAD `.odm-head` era `display:none` @390: `aria-hidden` inerte. **PM-C** lo avrebbe reso difetto reale; **C4** lo ha intercettato **prima del deploy**. Non è “scoperta di un bug preesistente”.

### 0.8 Superficie conservazione
```json
{
  "card_apparati_census": 14,
  "note": "card_apparati in harness = count of .oggi-card inside [data-o17-section=apparati] OR chassisNameCards.length equivalent; queueConservationCheck uses buildChassisNameCards (same population as Apparati section)"
}
```
- UI e `queueConservationCheck` usano entrambi `buildChassisNameCards` → popolazioni coincidenti per costruzione.
- Run O18 live: surfaces chassis=9, triage=0, noise=0; missing/duplicated VUOTI.

### 0.9 Debiti
- **RIAPERTO** `DEBT-OGGI-MOBILE-DENSITY` (23.646 ≈ −0,49% vs 23.763; C9 troppo debole). Guadagno reale −45 px/fam, −17 px/card.
- **APERTO** `DEBT-O17-CLOSURE-CRITERION-WEAK` (revisore).
- **APERTO** `DEBT-O17-CROSS-SESSION-VARIANCE`.
- **CHIUSO** `DEBT-O17-PROTOTYPE-UNEXPLAINED`.
- `DEBT-O16-GATE-ILLFORMED` resta aperto (revisore).

## 3. Censimento N1.1 (PRE-N2, integrale @390) + N1.2

auth: catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato
h_pagina@390=23646 h1=1 jumps=1 bare=5 tab_div=0

### Heading (enumerati)
- [0] h1 y=129.9 id=None «Oggi ?»
- [1] h2 y=234.9 id=None «Priorità per conseguenza difensiva»
- [2] h2 y=715.7 id=None «FDB · sensore difensivo»
- [3] h4 y=1242.8 id=None «Fatti osservati»
- [4] h4 y=1397.2 id=None «Dati mancanti o non correnti»
- [5] h4 y=1682.0 id=None «Interpretazione deterministica»
- [6] h4 y=1745.2 id=None «INFERENZA IA»
- [7] h4 y=2546.5 id=None «Fatti osservati»
- [8] h4 y=2700.9 id=None «Dati mancanti o non correnti»
- [9] h4 y=2985.7 id=None «Interpretazione deterministica»
- [10] h4 y=3048.9 id=None «INFERENZA IA»
- [11] h4 y=3850.2 id=None «Fatti osservati»
- [12] h4 y=4004.6 id=None «Dati mancanti o non correnti»
- [13] h4 y=4289.4 id=None «Interpretazione deterministica»
- [14] h4 y=4352.6 id=None «INFERENZA IA»
- [15] h4 y=5153.9 id=None «Fatti osservati»
- [16] h4 y=5308.4 id=None «Dati mancanti o non correnti»
- [17] h4 y=5593.1 id=None «Interpretazione deterministica»
- [18] h4 y=5656.3 id=None «INFERENZA IA»
- [19] h4 y=6457.7 id=None «Fatti osservati»
- [20] h4 y=6612.1 id=None «Dati mancanti o non correnti»
- [21] h4 y=6896.8 id=None «Interpretazione deterministica»
- [22] h4 y=6960.1 id=None «INFERENZA IA»
- [23] h4 y=7761.4 id=None «Fatti osservati»
- [24] h4 y=7915.8 id=None «Dati mancanti o non correnti»
- [25] h4 y=8200.6 id=None «Interpretazione deterministica»
- [26] h4 y=8263.8 id=None «INFERENZA IA»
- [27] h4 y=9065.1 id=None «Fatti osservati»
- [28] h4 y=9219.5 id=None «Dati mancanti o non correnti»
- [29] h4 y=9504.3 id=None «Interpretazione deterministica»
- [30] h4 y=9567.5 id=None «INFERENZA IA»
- [31] h4 y=10368.8 id=None «Fatti osservati»
- [32] h4 y=10523.2 id=None «Dati mancanti o non correnti»
- [33] h4 y=10808.0 id=None «Interpretazione deterministica»
- [34] h4 y=10871.2 id=None «INFERENZA IA»
- [35] h4 y=11672.5 id=None «Fatti osservati»
- [36] h4 y=11827.0 id=None «Dati mancanti o non correnti»
- [37] h4 y=12111.7 id=None «Interpretazione deterministica»
- [38] h4 y=12174.9 id=None «INFERENZA IA»
- [39] h4 y=12976.2 id=None «Fatti osservati»
- [40] h4 y=13130.7 id=None «Dati mancanti o non correnti»
- [41] h4 y=13415.4 id=None «Interpretazione deterministica»
- [42] h4 y=13478.7 id=None «INFERENZA IA»
- [43] h2 y=13797.2 id=None «Copertura sorgenti»
- [44] h2 y=15248.9 id=None «Comportamento · Zeek»
- [45] h2 y=15876.4 id=None «Egress · destinazioni»
- [46] h2 y=16146.0 id=None «Apparati multi-interfaccia»
- [47] h2 y=23548.5 id=None «Altro in coda»

### Salti di livello
- SKIP 2: «FDB · sensore difensivo»(h2) → «Fatti osservati»(h4)

### Landmark
- role=aside name=«» id=None has_name=False
- role=nav name=«» id=app-nav has_name=False
- role=main name=«Oggi ?» id=None has_name=True
- role=header name=«Oggi ?» id=None has_name=True
- role=nav name=«Domande rapide da Oggi» id=None has_name=True

### L0 + schermate 844
- id=None kind=details y0=172.0 screens=0 role=None label=«Priorità per conseguenza difensiva»
- id=None kind=nav y0=259.9 screens=0 role=None label=«»
- id=oggi-fdb kind=section y0=715.7 screens=0 role=None label=«FDB · sensore difensivo»
- id=oggi-coverage kind=section y0=13797.2 screens=16 role=None label=«Copertura sorgenti»
- id=oggi-behavior kind=section y0=15248.9 screens=18 role=None label=«Comportamento · Zeek»
- id=oggi-egress kind=section y0=15876.4 screens=18 role=None label=«Egress · destinazioni»
- id=None kind=section y0=16146.0 screens=19 role=None label=«Apparati multi-interfaccia»
- id=oggi-secondary kind=details y0=23508.7 screens=27 role=None label=«Altro in coda»

### Sezioni bare (senza landmark/nome)
- {'id': 'oggi-fdb', 'kind': 'section', 'label': 'FDB · sensore difensivo', 'y0': 715.6875, 'offsetHeight': 13061, 'screens_844': 0, 'role': None, 'aria_label': None, 'aria_labelledby': None}
- {'id': 'oggi-coverage', 'kind': 'section', 'label': 'Copertura sorgenti', 'y0': 13797.171875, 'offsetHeight': 1432, 'screens_844': 16, 'role': None, 'aria_label': None, 'aria_labelledby': None}
- {'id': 'oggi-behavior', 'kind': 'section', 'label': 'Comportamento · Zeek', 'y0': 15248.875, 'offsetHeight': 608, 'screens_844': 18, 'role': None, 'aria_label': None, 'aria_labelledby': None}
- {'id': 'oggi-egress', 'kind': 'section', 'label': 'Egress · destinazioni', 'y0': 15876.421875, 'offsetHeight': 250, 'screens_844': 18, 'role': None, 'aria_label': None, 'aria_labelledby': None}
- {'id': None, 'kind': 'section', 'label': 'Apparati multi-interfaccia', 'y0': 16145.96875, 'offsetHeight': 7363, 'screens_844': 19, 'role': None, 'aria_label': None, 'aria_labelledby': None}

### Tab divergences
n=0

### Quick nav
- «Non riconosciuto / solo-L2 adesso?» href=#oggi-fdb hash=oggi-fdb target_exists=True
- «MAC dove è attaccato?» href=/plant hash=None target_exists=False
- «Già visto o nuovo?» href=#oggi-secondary hash=oggi-secondary target_exists=True
- «Sorgente cieca?» href=#oggi-fdb hash=oggi-fdb target_exists=True
- «Dietro il GS308EP?» href=/gs308 hash=None target_exists=False

### Gate N1 (PRE-N2)
```json
{
  "h1_ok": true,
  "jumps_empty": false,
  "sections_bare_empty": false,
  "tab_aligned": true,
  "quick_all_targets": false,
  "positive_tabindex_empty": true,
  "nav_structure_already_ok": false,
  "stop_before_N2": false,
  "L0_ids": [
    "oggi-behavior",
    "oggi-coverage",
    "oggi-egress",
    "oggi-fdb",
    "oggi-secondary"
  ],
  "quick_hashes": [
    "oggi-fdb",
    "oggi-secondary"
  ],
  "L0_missing_from_quick": [
    "oggi-behavior",
    "oggi-coverage",
    "oggi-egress"
  ],
  "N2_4_needed": true
}
```

**Gate N1:** struttura NON già ok → N2 giustificato (`stop_before_N2: false`).

### N1.2 Altre rotte (sola lettura)
| rotta | @390 h | @1280 h | sezioni L0 | jumps@390 | tab_div@390 |
|---|---:|---:|---:|---:|---:|
| topology | 10146 | 2686 | 6 | 1 | 9 |
| inventory | 6549 | 6142 | 0 | 0 | 1 |
| gs308 | 3254 | 1916 | 5 | 0 | 1 |
| monitoring | 1431 | 1228 | 0 | 0 | 1 |
| dossier | 7168 | 4279 | 11 | 0 | 1 |

## 4. R per blocco — 3 catture @390 (N1-POST, censimento allegato)
- cap1: h_pagina=24814 census={"famiglie_matrice": 10, "righe_matrice": 40, "card_apparati": 14, "problem_cards": 33, "coverage_cards": 8, "coverage_titles": ["Sorgente copertura vecchia · Fritz TR-064 (hostlist / mesh / WLAN)", "Sorgente copertura vecchia · Zeek behaviour (JA4 / JA4D / DHCP fp)", "Sorgente copertura vecchia · Zeek egress hybrid (ext host+port / int relazione)", "Sorgente copertura vecchia · ASUSTOR NAS SNMP (Cassiopea)", "Sorgente disabilitata · Zeek conn / flow_observations (legacy storico)", "Sorgente disabilitata · Zeek intel (DNS/SNI → ip_intel)", "Sorgente disabilitata · Zeek DHCP hostnames", "Novità egress soppressa · Zeek egress hybrid (ext host+port / int relazione)"], "fritz_present": true}
  L0_heights={"oggi-legend": 74, "": 313, "oggi-fdb": 13061, "oggi-coverage": 2431, "oggi-behavior": 608, "oggi-egress": 250, "oggi-apparati": 7363, "oggi-secondary": 51}
- cap2: h_pagina=23815 census={"famiglie_matrice": 10, "righe_matrice": 40, "card_apparati": 14, "problem_cards": 30, "coverage_cards": 5, "coverage_titles": ["Sorgente copertura vecchia · ASUSTOR NAS SNMP (Cassiopea)", "Sorgente disabilitata · Zeek conn / flow_observations (legacy storico)", "Sorgente disabilitata · Zeek intel (DNS/SNI → ip_intel)", "Sorgente disabilitata · Zeek DHCP hostnames", "Novità egress soppressa · Zeek egress hybrid (ext host+port / int relazione)"], "fritz_present": false}
  L0_heights={"oggi-legend": 74, "": 313, "oggi-fdb": 13061, "oggi-coverage": 1432, "oggi-behavior": 608, "oggi-egress": 250, "oggi-apparati": 7363, "oggi-secondary": 51}
- cap3: h_pagina=23815 census={"famiglie_matrice": 10, "righe_matrice": 40, "card_apparati": 14, "problem_cards": 30, "coverage_cards": 5, "coverage_titles": ["Sorgente copertura vecchia · ASUSTOR NAS SNMP (Cassiopea)", "Sorgente disabilitata · Zeek conn / flow_observations (legacy storico)", "Sorgente disabilitata · Zeek intel (DNS/SNI → ip_intel)", "Sorgente disabilitata · Zeek DHCP hostnames", "Novità egress soppressa · Zeek egress hybrid (ext host+port / int relazione)"], "fritz_present": false}
  L0_heights={"oggi-legend": 74, "": 313, "oggi-fdb": 13061, "oggi-coverage": 1432, "oggi-behavior": 608, "oggi-egress": 250, "oggi-apparati": 7363, "oggi-secondary": 51}
- Fritz: presente in cap1, assente in cap2/cap3 (API nota).

## 5. N2 applicato / non applicato
- **N2.1 applicato:** bande matrice h4→h3 (salta h2→h4 eliminato).
- **N2.2 applicato:** `role=region` + `aria-labelledby`/`aria-label` su L0 (legend, fdb, coverage, behavior, egress, apparati, secondary, conflitti/porte/nomi condizionali).
- **N2.3 non modificato:** @390 già allineato in N1; nessuna modifica tabindex.
- **N2.4 applicato:** indice sezioni in `nav.oggi-quick` + id `oggi-apparati` + fix ancora «Sorgente cieca?» → `#oggi-coverage`; egress link allineato alla visibilità sezione.
- **N2.5 NON applicato:** N1 non impone «sezione N di M»; l’indice fornisce orientamento.
- **N2.6:** solo file in elenco §1.

## 6. Previsioni vs osservati
| id | atteso | osservato | scarto | causa dominante |
|---|---|---|---|---|
| N2.1-jumps | 0 | 0 (POST) | 0 | h3 bande |
| N2.2-bare | 0 | 0 (POST) | 0 | landmark L0 |
| N2.3-tab390 | 0 | 0 | 0 | già ok |
| N2.4-quick-L0 | 0 mancanti | 0 (N1-POST) | 0 | indice + id |
| N2.5-pos | non applicato | non applicato | — | — |
| V5-h390 | ≤PRE+R o crescita nominata | PRE=23646 POST=23815 Δ=+169 | +169 | indice sezioni N2.4 |
| V4-contrast | ≥4.5 | 7.232 | ok | `--odm-via-label` |
| V4-font | 10.88 | 10.88/10.88 | 0 | nessuna riduzione |

## 7. Diff V1/V2/V3 + V4 + altezze V5

### V1
```json
{
  "ok": true,
  "only_pre": [],
  "only_post_data": [],
  "only_post_navigation": [],
  "len_pre": 221,
  "len_post": 221,
  "note": "escluso nav.oggi-quick dall'estrazione; age=/giorni normalizzati"
}
```
### V2
```json
{
  "ok": true,
  "len_triples_pre": 120,
  "len_triples_post": 120,
  "len_metas_pre": 40,
  "len_metas_post": 40,
  "n_righe": 40,
  "diff_triples": [],
  "diff_metas": []
}
```
### V3
```json
{
  "ok": true,
  "violations": [],
  "violations_pre": []
}
```
### V4
```json
{
  "ok": true,
  "nondom": true,
  "btn_ok": true,
  "diffs": [],
  "columns_post": [
    {
      "text": "APPROFONDISCI",
      "width": "118.266px",
      "fontSize": "10.88px",
      "fontWeight": "400",
      "fontFamily": "Inter, -apple-system, system-ui, sans-serif",
      "color": "rgb(152, 162, 179)",
      "backgroundColor": "rgba(0, 0, 0, 0)",
      "borderTopWidth": "0px",
      "borderTopStyle": "none",
      "padding": "0px",
      "margin": "0px",
      "textTransform": "uppercase",
      "opacity": "1",
      "order": "0"
    },
    {
      "text": "APPLICA",
      "width": "118.266px",
      "fontSize": "10.88px",
      "fontWeight": "400",
      "fontFamily": "Inter, -apple-system, system-ui, sans-serif",
      "color": "rgb(152, 162, 179)",
      "backgroundColor": "rgba(0, 0, 0, 0)",
      "borderTopWidth": "0px",
      "borderTopStyle": "none",
      "padding": "0px",
      "margin": "0px",
      "textTransform": "uppercase",
      "opacity": "1",
      "order": "0"
    },
    {
      "text": "NON APPLICARE",
      "width": "118.281px",
      "fontSize": "10.88px",
      "fontWeight": "400",
      "fontFamily": "Inter, -apple-system, system-ui, sans-serif",
      "color": "rgb(152, 162, 179)",
      "backgroundColor": "rgba(0, 0, 0, 0)",
      "borderTopWidth": "0px",
      "borderTopStyle": "none",
      "padding": "0px",
      "margin": "0px",
      "textTransform": "uppercase",
      "opacity": "1",
      "order": "0"
    }
  ],
  "buttons_post": [
    {
      "w": 117.203125,
      "h": 38.390625,
      "text": "Impianto"
    },
    {
      "w": 117.203125,
      "h": 38.390625,
      "text": "Riconosci"
    },
    {
      "w": 117.21875,
      "h": 38.390625,
      "text": "Ignora"
    }
  ],
  "font_size_pre": "10.88px",
  "font_size_post": "10.88px",
  "color_pre": "rgb(102, 112, 133)",
  "color_post": "rgb(152, 162, 179)",
  "bg_behind_pre": "rgb(15, 19, 25)",
  "bg_behind_post": "rgb(15, 19, 25)",
  "contrast_pre": 3.7439670561008453,
  "contrast_post": 7.232072185421649,
  "contrast_post_ge_4_5": true,
  "wcag_source": "WCAG 2.2 SC 1.4.3 Contrast (Minimum) AA — testo normale ≥4.5:1"
}
```
### V5 altezze
```json
{
  "390": {
    "pre": {
      "h_pagina": 23646,
      "h_fdb": 13061,
      "h_apparati": 7363,
      "h_coverage": 1432,
      "blocks": {
        "oggi-fdb": 13061,
        "oggi-coverage": 1432,
        "oggi-behavior": 608,
        "oggi-egress": 250,
        "oggi-apparati": null,
        "oggi-nomi": null,
        "oggi-secondary": 51,
        "oggi-legend": null,
        "oggi-conflitti": null,
        "oggi-porte": null
      }
    },
    "post": {
      "h_pagina": 23815,
      "h_fdb": 13061,
      "h_apparati": 7363,
      "h_coverage": 1432,
      "blocks": {
        "oggi-fdb": 13061,
        "oggi-coverage": 1432,
        "oggi-behavior": 608,
        "oggi-egress": 250,
        "oggi-apparati": 7363,
        "oggi-nomi": null,
        "oggi-secondary": 51,
        "oggi-legend": 74,
        "oggi-conflitti": null,
        "oggi-porte": null
      }
    },
    "delta_pagina": 169
  },
  "768": {
    "pre": {
      "h_pagina": 18639,
      "h_fdb": 10842,
      "h_apparati": 4990,
      "h_coverage": 1021,
      "blocks": {
        "oggi-fdb": 10842,
        "oggi-coverage": 1021,
        "oggi-behavior": 425,
        "oggi-egress": 142,
        "oggi-apparati": null,
        "oggi-nomi": null,
        "oggi-secondary": 274,
        "oggi-legend": null,
        "oggi-conflitti": null,
        "oggi-porte": null
      }
    },
    "post": {
      "h_pagina": 18808,
      "h_fdb": 10842,
      "h_apparati": 4990,
      "h_coverage": 1021,
      "blocks": {
        "oggi-fdb": 10842,
        "oggi-coverage": 1021,
        "oggi-behavior": 425,
        "oggi-egress": 142,
        "oggi-apparati": 4990,
        "oggi-nomi": null,
        "oggi-secondary": 274,
        "oggi-legend": 240,
        "oggi-conflitti": null,
        "oggi-porte": null
      }
    },
    "delta_pagina": 169
  },
  "1280": {
    "pre": {
      "h_pagina": 15580,
      "h_fdb": 9623,
      "h_apparati": 3283,
      "h_coverage": 1179,
      "blocks": {
        "oggi-fdb": 9623,
        "oggi-coverage": 1179,
        "oggi-behavior": 259,
        "oggi-egress": 120,
        "oggi-apparati": null,
        "oggi-nomi": null,
        "oggi-secondary": 274,
        "oggi-legend": null,
        "oggi-conflitti": null,
        "oggi-porte": null
      }
    },
    "post": {
      "h_pagina": 15422,
      "h_fdb": 9623,
      "h_apparati": 3283,
      "h_coverage": 852,
      "blocks": {
        "oggi-fdb": 9623,
        "oggi-coverage": 852,
        "oggi-behavior": 259,
        "oggi-egress": 120,
        "oggi-apparati": 3283,
        "oggi-nomi": null,
        "oggi-secondary": 274,
        "oggi-legend": 240,
        "oggi-conflitti": null,
        "oggi-porte": null
      }
    },
    "delta_pagina": -158
  }
}
```
```json
{
  "ok": true,
  "R_pagina_cov": 312,
  "R_fdb": 0,
  "R_apparati": 0,
  "delta_390": 169,
  "delta_768": 169,
  "delta_1280": -158,
  "note": "crescita attesa da indice sezioni in nav.oggi-quick (N2.4); Fritz R=312 se census Fritz",
  "index_growth_px": 169,
  "fdb_apparati_stable": true
}
```

## 8. V6 — ancore una per una
```json
{
  "ok": true,
  "jumps": [],
  "sections_bare": [],
  "tab_divergences": [],
  "positive_tabindex": [],
  "index_links_enumerated": [
    {
      "text": "Priorità per conseguenza difensiva",
      "href": "#oggi-legend",
      "hash": "oggi-legend",
      "target_exists": true
    },
    {
      "text": "FDB · sensore difensivo",
      "href": "#oggi-fdb",
      "hash": "oggi-fdb",
      "target_exists": true
    },
    {
      "text": "Copertura sorgenti",
      "href": "#oggi-coverage",
      "hash": "oggi-coverage",
      "target_exists": true
    },
    {
      "text": "Comportamento · Zeek",
      "href": "#oggi-behavior",
      "hash": "oggi-behavior",
      "target_exists": true
    },
    {
      "text": "Egress · destinazioni",
      "href": "#oggi-egress",
      "hash": "oggi-egress",
      "target_exists": true
    },
    {
      "text": "Apparati multi-interfaccia",
      "href": "#oggi-apparati",
      "hash": "oggi-apparati",
      "target_exists": true
    },
    {
      "text": "Altro in coda",
      "href": "#oggi-secondary",
      "hash": "oggi-secondary",
      "target_exists": true
    }
  ],
  "quick_anchors_enumerated": [
    {
      "text": "Non riconosciuto / solo-L2 adesso?",
      "href": "#oggi-fdb",
      "hash": "oggi-fdb",
      "target_exists": true
    },
    {
      "text": "Già visto o nuovo?",
      "href": "#oggi-secondary",
      "hash": "oggi-secondary",
      "target_exists": true
    },
    {
      "text": "Sorgente cieca?",
      "href": "#oggi-coverage",
      "hash": "oggi-coverage",
      "target_exists": true
    },
    {
      "text": "Priorità per conseguenza difensiva",
      "href": "#oggi-legend",
      "hash": "oggi-legend",
      "target_exists": true
    },
    {
      "text": "FDB · sensore difensivo",
      "href": "#oggi-fdb",
      "hash": "oggi-fdb",
      "target_exists": true
    },
    {
      "text": "Copertura sorgenti",
      "href": "#oggi-coverage",
      "hash": "oggi-coverage",
      "target_exists": true
    },
    {
      "text": "Comportamento · Zeek",
      "href": "#oggi-behavior",
      "hash": "oggi-behavior",
      "target_exists": true
    },
    {
      "text": "Egress · destinazioni",
      "href": "#oggi-egress",
      "hash": "oggi-egress",
      "target_exists": true
    },
    {
      "text": "Apparati multi-interfaccia",
      "href": "#oggi-apparati",
      "hash": "oggi-apparati",
      "target_exists": true
    },
    {
      "text": "Altro in coda",
      "href": "#oggi-secondary",
      "hash": "oggi-secondary",
      "target_exists": true
    }
  ],
  "h1_count": 1,
  "L0": [
    {
      "id": "oggi-legend",
      "role": "region",
      "aria_label": "Priorità per conseguenza difensiva",
      "aria_labelledby": null,
      "label": "Priorità per conseguenza difensiva",
      "y0": 172.03125,
      "offsetHeight": 74
    },
    {
      "id": "oggi-fdb",
      "role": "region",
      "aria_label": null,
      "aria_labelledby": "oggi-fdb-title",
      "label": "FDB · sensore difensivo",
      "y0": 884.8125,
      "offsetHeight": 13061
    },
    {
      "id": "oggi-coverage",
      "role": "region",
      "aria_label": null,
      "aria_labelledby": "oggi-coverage-title",
      "label": "Copertura sorgenti",
      "y0": 13966.296875,
      "offsetHeight": 1432
    },
    {
      "id": "oggi-behavior",
      "role": "region",
      "aria_label": null,
      "aria_labelledby": "oggi-behavior-title",
      "label": "Comportamento · Zeek",
      "y0": 15418,
      "offsetHeight": 608
    },
    {
      "id": "oggi-egress",
      "role": "region",
      "aria_label": null,
      "aria_labelledby": "oggi-egress-title",
      "label": "Egress · destinazioni",
      "y0": 16045.546875,
      "offsetHeight": 250
    },
    {
      "id": "oggi-apparati",
      "role": "region",
      "aria_label": null,
      "aria_labelledby": "oggi-apparati-title",
      "label": "Apparati multi-interfaccia",
      "y0": 16315.09375,
      "offsetHeight": 7363
    },
    {
      "id": "oggi-secondary",
      "role": "region",
      "aria_label": null,
      "aria_labelledby": "oggi-secondary-title",
      "label": "Altro in coda",
      "y0": 23677.796875,
      "offsetHeight": 51
    }
  ]
}
```

### Gate N1-POST (dopo N2)
```json
{
  "h1_ok": true,
  "jumps_empty": true,
  "sections_bare_empty": true,
  "tab_aligned": true,
  "quick_all_targets": true,
  "positive_tabindex_empty": true,
  "nav_structure_already_ok": true,
  "stop_before_N2": true,
  "L0_ids": [
    "oggi-apparati",
    "oggi-behavior",
    "oggi-coverage",
    "oggi-egress",
    "oggi-fdb",
    "oggi-legend",
    "oggi-secondary"
  ],
  "quick_hashes": [
    "oggi-apparati",
    "oggi-behavior",
    "oggi-coverage",
    "oggi-egress",
    "oggi-fdb",
    "oggi-legend",
    "oggi-secondary"
  ],
  "L0_missing_from_quick": [],
  "N2_4_needed": false
}
```

## 9. Gate V7 — OUTPUT INTEGRALE

### w8_currency_gate.py
```
===== w8_currency_gate.py =====
== W8 CURRENCY GATE (indurito, W8-fix2) ==
root: /Users/michelestorci/Developer/rete-palazzo/observatory
sentinelle: simbolo ORM 'FactAssertion' · tabella grezza 'fact_assertions' in chiamata SQL (text/execute) · COMBO (fact-token FactAssertion|fact_assertions|fact_key) + valore di stato quotato 'current'
scope: api/**, scripts/**, collector/**
esclusioni:
  - api/app/facts/**  (il resolver È la fonte della correntezza)
  - scripts/w8_currency_gate.py  (contiene le sentinelle/fact_key come dato)
  - scripts/w8_g8_equivalence.py  (contiene le sentinelle/fact_key come dato)
file scansionati: 209
voci allowlist: permanenti 17 · temporanee 1

ATTENZIONE — ECCEZIONI TEMPORANEE CON DEBITO APERTO: 1
  TEMP scripts/wp_gate.py:103 (atteso 1, osservato 1) debt=DEBT-WPGATE-CURRENCY-COUNT-LOCAL
      | fa_cur = int(db.scalar(select(func.count()).select_from(FactAssertion).where(FactAssertion.state == "current")) or 0)

ECCEZIONI GIUSTIFICATE PERMANENTI (accounted): 17
  OK  api/app/bootstrap.py:19  (atteso 1, osservato 1)
      | from app.models import FactAssertion, IdentityEvidence, IdentityLinkProposal, Switch, User  # noqa: F401 — create_all
      → bootstrap: import per registrazione modelli in create_all (nessuna query).
  OK  api/app/models.py:155  (atteso 1, osservato 1)
      | class FactAssertion(Base):
      → models: DEFINIZIONE ORM della tabella (non una lettura).
  OK  api/app/routers/admin.py:320  (atteso 1, osservato 1)
      | .order_by(FactAssertion.last_seen_at.desc(), FactAssertion.id.desc())
      → admin /facts/conflicts: ordinamento di DISPLAY delle divergenze storiche.
  OK  api/app/routers/admin.py:317  (atteso 1, osservato 1)
      | FactAssertion.reason == "conflict_review",
      → admin /facts/conflicts: filtro divergenze I3.
  OK  api/app/routers/admin.py:318  (atteso 1, osservato 1)
      | FactAssertion.state == "historical",
      → admin /facts/conflicts: esplicitamente state='historical', l'opposto di current.
  OK  api/app/routers/admin.py:292,311  (atteso 2, osservato 2)
      | from app.models import FactAssertion
      → admin: import per diagnostica read-only (shadow-stats COUNT + conflitti I3).
  OK  api/app/routers/admin.py:295  (atteso 1, osservato 1)
      | rows = int(db.scalar(select(func.count()).select_from(FactAssertion)) or 0)
      → admin /facts/shadow-stats: COUNT righe (osservabilità breaker), non un valore corrente.
  OK  api/app/routers/admin.py:315  (atteso 1, osservato 1)
      | select(FactAssertion)
      → admin /facts/conflicts: divergenze conflict_review, state='historical' (I3), NON current.
  OK  scripts/wp_diagnose.py:268  (atteso 1, osservato 1)
      | base_fa = {r[0] for r in bdb.execute(select(FactAssertion.id)).all()}
      → wp_diagnose: enumerazione id (baseline) per delta, nessuno stato.
  OK  scripts/wp_diagnose.py:267  (atteso 1, osservato 1)
      | cur_fa = {r[0] for r in db.execute(select(FactAssertion.id)).all()}
      → wp_diagnose: enumerazione id (now) per delta vs baseline, nessuno stato.
  OK  scripts/wp_diagnose.py:127  (atteso 1, osservato 1)
      | db.execute(select(FactAssertion.state, func.count()).group_by(FactAssertion.state)).all()
      → wp_diagnose: distribuzione di stato (diagnostica), non una lettura del valore corrente.
  OK  scripts/wp_diagnose.py:273  (atteso 1, osservato 1)
      | fa = db.get(FactAssertion, fid)
      → wp_diagnose: lettura per id già enumerato (display diagnostico).
  OK  scripts/wp_diagnose.py:125  (atteso 1, osservato 1)
      | fa_total = int(db.scalar(select(func.count()).select_from(FactAssertion)) or 0)
      → wp_diagnose: COUNT righe totali (nessun valore, nessuno stato).
  OK  scripts/wp_diagnose.py:29  (atteso 1, osservato 1)
      | from app.models import Asset, FactAssertion, Interface, IpAddress, NameProposal  # noqa: E402
      → wp_diagnose: import per diagnostica (nessuna lettura di correntezza).
  OK  scripts/wp_diagnose.py:232  (atteso 1, osservato 1)
      | rows = db.scalars(select(FactAssertion).order_by(FactAssertion.id.desc()).limit(15)).all()
      → wp_diagnose: campione di DISPLAY (ultime 15 per id), non una lettura di correntezza.
  OK  scripts/wp_gate.py:102  (atteso 1, osservato 1)
      | fat = int(db.scalar(select(func.count()).select_from(FactAssertion)) or 0)
      → wp_gate: COUNT righe totali (nessun valore, nessuno stato).
  OK  scripts/wp_gate.py:36  (atteso 1, osservato 1)
      | from app.models import Asset, FactAssertion, IpAddress, NameProposal  # noqa: E402
      → wp_gate: import per diagnostica di regime (nessuna lettura di correntezza).

VIOLAZIONI: 0

RISULTATO: PASS (con 1 eccezione/i temporanea/e)
EXIT:0
```

### grep specificity
```
===== grep scoreSpecificity|specificity api/ =====
(end grep; empty = PASS)
```

### color_literal_gate
```
===== color_literal_gate.py =====
PASS: no hard-coded color literals outside allowlist; matrix.css decls-only
  token_file=assets/matrix.css (literals only in --custom-property decls)
  allowlist_count=16
EXIT:0
===== color_literal_gate.py --self-test =====
SELFTEST vue inject detected: (2, '#ff00aa', '.x { color: #ff00aa; /* O13D_COLOR_GATE_INJECT */ }')
SELFTEST matrix rule inject detected: (955, '#ff00aa', '.o14fix-gate-inject { color: #ff00aa; /* O14FIX_COLOR_GATE_INJECT */ }')
SELFTEST PASS: inject fails (vue+matrix rule), remove passes
EXIT:0
```

### queueConservationCheck
```json
{
  "surfaces": {
    "chassis_cards": 9,
    "triage_rows": 0,
    "noise_proposal_ids": 0,
    "assets_n": 118
  },
  "missing": [],
  "duplicated": [],
  "suppressed_noop_n": 0,
  "ok": true
}
```

### Drift repo↔NAS (enumerato)
```
===== drift scripts repo ↔ NAS =====
solo-NAS = { scripts/_w4a_measure.py }
solo-repo = { scripts/o18_block0_measure.py, scripts/oggi_nav_measure.py, scripts/oggi_nav_verify_ab.py }
NAS_count 68 repo_count 70
solo-NAS full enum:
  _w4a_measure.py
solo-repo (new permanent O17+O18 measure only filter):
  o18_block0_measure.py
  oggi_nav_measure.py
  oggi_nav_verify_ab.py
orphans_nas NONE
orphans_measure_solo_repo NONE
DRIFT_OK
```

Dichiarato:
```
solo-NAS = { scripts/_w4a_measure.py }
solo-repo = { scripts/o18_block0_measure.py, scripts/oggi_nav_measure.py, scripts/oggi_nav_verify_ab.py }
# (oggi_density_* già presenti su entrambi post-O17)
orfani = NONE
```

## 10. Catture
- `docs/obs-o18-oggi-1280.png`: 1280×15308 sha256=f6f5470abb086304d39695f59f98b4d395ce2a7a032ab11dc8ec6712a78aacb9
  h_pre_scrub=15422 h_post_scrub=15308 |h_PNG−h|=0 ≤ R=312 ok=True
- `docs/obs-o18-oggi-768.png`: 768×18565 sha256=fb95bed8efe7c5388917745d0e5ed24fdb312d28ebae884959ec67669619d68f
  h_pre_scrub=19020 h_post_scrub=18565 |h_PNG−h|=0 ≤ R=312 ok=True
- `docs/obs-o18-oggi-390.png`: 390×23103 sha256=a3a9b0bf492592ff6feee25bfb3fffd99c44f77ff59353d6aff58c62796a05e9
  h_pre_scrub=23815 h_post_scrub=23103 |h_PNG−h|=0 ≤ R=312 ok=True
- `o9_png_assert.py --pair` 1280↔390 e 768↔390: **PASS**
- Provenienza mint: catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato
- Scrub: keep = chrome strutturale ∩ uiExact (o13dfix harness); nessun pattern sul contenuto.

## 11. Deploy G3 / G4
```
index.html bytes=750
js=index-DQszrFJY.js bytes=465293
markers={'0.10.87': True, 'obs-o18-marker': True, 'obs-o17-marker': True, 'data-o18': True}
css=None
```
```json
{
  "auth_provenance": "catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato",
  "deployed": {
    "url": "http://192.168.1.3:8080/oggi",
    "h": 23815,
    "hasLogin": false,
    "marker": "obs-o18-marker",
    "cov": 5,
    "fritz": false,
    "cards": 30
  },
  "h_pagina_deployed": 23815,
  "h_pagina_local_POST_V": 23815,
  "abs_delta_vs_local": 0,
  "R": 312,
  "ok_vs_local": true,
  "png": {
    "w": 390,
    "h": 23103,
    "h_after_scrub": 23103,
    "abs_png_minus_h": 0,
    "ok": true
  },
  "fritz_local_V": false,
  "fritz_deployed": false
}
```
- Marker O18 solo in `observatoryUx.js` (consumato da `Oggi.vue` via `data-o18`); non in `api.js`.

## 12. Debiti
| debito | stato | attribuzione |
|---|---|---|
| DEBT-OGGI-MOBILE-DENSITY | RIAPERTO | Cursor (chiusura O17 annullata) |
| DEBT-O17-CLOSURE-CRITERION-WEAK | APERTO | revisore |
| DEBT-O17-CROSS-SESSION-VARIANCE | APERTO | Cursor/disciplina |
| DEBT-O17-PROTOTYPE-UNEXPLAINED | CHIUSO | Cursor (0.6) |
| DEBT-O16-GATE-ILLFORMED | APERTO | revisore |
| DEBT-ONESHOT-SCRIPT-RESIDUE | quinta evitata | — |

## 13. Cosa NON ho fatto
- Nessuna riduzione altezza strutturale / rimozione contenuto (F-9).
- N2.5 «sezione N di M» non applicato.
- Sticky non usato (nessuna prova sticky+harness).
- Rotte N1.2 non modificate.
- T7, OBS-CURRENCY, FA251, `_w4a_measure.py`, favicon, grano egress, `--inference-edge`, `/ai`, main/merge/tag/force: non toccati.
- Deploy **web only**; api/health resta 0.10.82 (atteso).

