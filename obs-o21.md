wc_l: 2487
# OBS-O21 — OBS-EVIDENZA-FIX + OBS-I2 — 0.10.90
Data report: 2026-07-29 21:28 UTC
Auth catture: session mint TTL 180s (fonte harness 36s×5), token non pubblicato.
Base: `c459afd` (HEAD post-O20). Ramo: `feature/obs-currency`.

## 1. Elenco file toccati

- `VERSION`, `web/package.json`, `CHANGELOG.md` → **0.10.90**
- `web/src/App.vue` — `data-obs-frontend-version` / `data-api-health-version`; brand onesto `vFE · api HEALTH`
- `web/src/views/Monitoring.vue` — `data-i2-condition` + title vocab sulle cinque condizioni
- `web/src/views/Plant.vue` — `data-i2-condition=limite_strutturale` su dot-na SNMP
- `scripts/evidence_site_audit.py` — classificazione I2; esclusione simboli ODM
- `scripts/evidence_gate.py` — controllo permanente placeholder foglia + self-test I2
- `scripts/evidence_verify_ab.py` — versioni PRE/POST via env
- `scripts/oggi_height_excl_flaky.py` — allowlist Fritz/Zeek; selettore solo `coverage_source_*` (non wrapper)
- `scripts/g4_reconcile_capture.py`, `scripts/oggi_height_excl_flaky.py` (Blocco 0)
- `docs/KNOWN_DEBT.md`, artefatti `docs/obs-o21-*`, `docs/o21-captures/`

## 2. Blocco 0 (correzioni O20)

### 0.1 DEBT-O20-OGGI-API-HEIGHT-JITTER — CHIUSO
Allowlist nominata Fritz TR-064 + Zeek behaviour. UNA rimisura @768.
**Nota ripristino:** il JSON B0 è stato accidentalmente sovrascritto durante V5; selettore corretto (niente wrapper `coverage-cards`); rimisura di ripristino con dist O20: Δ=0. Log originale B0: Δ_raw=0 Δ_excl=0 flaky=0.
### 0.1 artefatto (ripristino post-fix selettore)
```json
{
  "wave": "O21-B0.1",
  "auth_provenance": "catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato",
  "width": 768,
  "R_height": 320,
  "allowlist": [
    {
      "pattern": "Fritz TR-064",
      "debt": "DEBT-O20-OGGI-API-HEIGHT-JITTER",
      "reason": "O16-M1/O17: card coverage Fritz TR-064 presente/assente tra run (coverage_source_blind); causa payload API, non layout UI"
    },
    {
      "pattern": "Zeek behaviour",
      "debt": "DEBT-O20-OGGI-API-HEIGHT-JITTER",
      "reason": "O20 V only_post_info: card «Zeek behaviour» intermittente insieme a Fritz nello stesso Δ+409 @768; stessa famiglia coverage_source_* API-based"
    }
  ],
  "len_allowlist_asserted": 2,
  "come_potrebbe_fallire": "se Δ resta >R dopo esclusione Fritz/Zeek, la causa non è quella allowlist — STOP, non escludere altro",
  "o20_reference_delta_plus409": {
    "source": "docs/obs-o20.md / KNOWN_DEBT (artefatto pinnato)",
    "delta_h": 409,
    "note": "Δ−212 solo-chat NON ammesso come evidenza"
  },
  "pre": {
    "h_raw": 16780,
    "h_excl": 16780,
    "cards_n": 28,
    "flaky_hidden_n": 0,
    "flaky_hidden": [],
    "frontend_version": null,
    "api_health_version": null,
    "script_src": "/assets/index-C6Ud7we9.js"
  },
  "post": {
    "h_raw": 16780,
    "h_excl": 16780,
    "cards_n": 28,
    "flaky_hidden_n": 0,
    "flaky_hidden": [],
    "frontend_version": null,
    "api_health_version": null,
    "script_src": "/assets/index-DRlt-wzC.js"
  },
  "delta_h_raw": 0,
  "delta_h_excl_flaky": 0,
  "pass_excl": true,
  "pass_raw": true
}
```
### 0.2 DEBT-O20-G4-CENSUS-MISMATCH-UNFLAGGED — CHIUSO
UNA rimisura topology×3 + plant@390: census match, Δh=0. Causa O20 = API topology non-idempotente.
**Nota:** JSON B0 ripristinato dal run log dopo overwrite path G4.
### 0.2 artefatto (ripristino da run log)
```json
{
  "wave": "O21-B0.2",
  "restored_from": "docs/obs-o21-B0-g4-run.log",
  "restore_note": "JSON sovrascritto per errore di path durante G4 O21; valori dalla rimisura UNA B0.2 (log).",
  "auth_provenance": "catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato",
  "R_height": 320,
  "routes": {
    "topology": {
      "1280": {
        "census_match": true,
        "delta_h": 0,
        "verdict": "PASS",
        "keys_local": [
          46,
          46
        ],
        "keys_deployed": [
          46,
          46
        ],
        "frontend_version": null,
        "api_health_version_from_page": "0.10.82"
      },
      "768": {
        "census_match": true,
        "delta_h": 0,
        "verdict": "PASS",
        "keys_local": [
          46,
          46
        ],
        "keys_deployed": [
          46,
          46
        ],
        "frontend_version": null,
        "api_health_version_from_page": "0.10.82"
      },
      "390": {
        "census_match": true,
        "delta_h": 0,
        "verdict": "PASS",
        "keys_local": [
          46,
          46
        ],
        "keys_deployed": [
          46,
          46
        ],
        "frontend_version": null,
        "api_health_version_from_page": "0.10.82"
      }
    },
    "plant": {
      "390": {
        "census_match": true,
        "delta_h": 0,
        "verdict": "PASS",
        "keys_local": [
          46,
          14
        ],
        "keys_deployed": [
          46,
          14
        ],
        "frontend_version": null,
        "api_health_version_from_page": "0.10.82"
      }
    }
  },
  "invalid": [],
  "all_pass": true,
  "come_potrebbe_fallire": "API topology non idempotente → census diverge; allora INVALID non Δh ok"
}
```
### 0.3 DEBT-O20-VERSION-FIELD-AMBIGUOUS — CHIUSO
Fonte del campo O20 `version_from_page_text: 0.10.82` = testo da `/api/health` (stale web-only), **non** frontend.
Fix: `data-obs-frontend-version=__APP_VERSION__` + `data-api-health-version`. G3 post-deploy conferma fe=0.10.90 api=0.10.82.
### 0.3 / G3 version sources
```json
{
  "index_js": "/assets/index-D7HHopYw.js",
  "index_css": "/assets/index-p4FzMslc.css",
  "js_bytes": 472151,
  "css_bytes": 144003,
  "js_has_0_10_90": true,
  "css_is_none": false,
  "marker_frontend_attr": true,
  "inference_edge_7656b0": true,
  "from_page": {
    "url": "http://192.168.1.3:8080/oggi",
    "frontend": "0.10.90",
    "api_health": "0.10.82",
    "brand": "v0.10.90 · api 0.10.82 · 29/07",
    "script": "http://192.168.1.3:8080/assets/index-D7HHopYw.js",
    "css": "http://192.168.1.3:8080/assets/index-p4FzMslc.css"
  },
  "G3_PASS": true
}
```
### 0.4 DEBT-O20-M2-BASELINE-NOT-PRESERVED — registrato (non rifare O20)
Da O21: M pubblica JSON hash **prima** di D. Fatto: `obs-o21-M-pre-D.json` sha256=`0076029e44a45f00a9c52e5dc21984b86bf509ede553f3bd11d68b054f43ec33` **prima** delle edit Monitoring/Plant.

### 0.5 Debiti registrati
- `DEBT-O20-V-BLOCKS-NOT-INLINE` — chiuso in questo report (V inline)
- `DEBT-O20-I2-SITEWIDE-INCOMPLETE` — chiuso (M+D+gate)

**GATE BLOCCO 0:** 0.1 e 0.2 risolti con una rimisura ciascuno → proseguire.

## 3. M1/M2 — accertamento I2 (JSON pre-D)

sha256 pre-D = `0076029e44a45f00a9c52e5dc21984b86bf509ede553f3bd11d68b054f43ec33`  
bytes=1257821 wc_l=34860

### M digest + M2 severity (pre-D)
```json
{
  "wave": "O21-M",
  "sha256": "0076029e44a45f00a9c52e5dc21984b86bf509ede553f3bd11d68b054f43ec33",
  "bytes": 1257821,
  "wc_l": 34860,
  "auth_provenance": "catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato",
  "routes_n": 13,
  "i2_violations_deduped_n": 5,
  "i2_ok_deduped_n": 2,
  "by_route_1280": {
    "oggi": {
      "h_pagina": 15430,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 15430
      },
      "placeholder_i2_n": 50,
      "i2_distinguishes_n": 0,
      "i2_not_distinguishes_n": 50,
      "len_asserted_ph": 50,
      "conditions": {
        "non_dichiarata": 50
      }
    },
    "topology": {
      "h_pagina": 5559,
      "census": {
        "network_nodes": 29,
        "topology_paths": 27,
        "list_parents": 27,
        "inference_marks": 1,
        "h_pagina": 5559
      },
      "placeholder_i2_n": 0,
      "i2_distinguishes_n": 0,
      "i2_not_distinguishes_n": 0,
      "len_asserted_ph": 0,
      "conditions": {}
    },
    "inventory": {
      "h_pagina": 6305,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 6305
      },
      "placeholder_i2_n": 0,
      "i2_distinguishes_n": 0,
      "i2_not_distinguishes_n": 0,
      "len_asserted_ph": 0,
      "conditions": {}
    },
    "gs308": {
      "h_pagina": 1916,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 1,
        "h_pagina": 1916
      },
      "placeholder_i2_n": 0,
      "i2_distinguishes_n": 0,
      "i2_not_distinguishes_n": 0,
      "len_asserted_ph": 0,
      "conditions": {}
    },
    "monitoring": {
      "h_pagina": 1228,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 1228
      },
      "placeholder_i2_n": 7,
      "i2_distinguishes_n": 2,
      "i2_not_distinguishes_n": 5,
      "len_asserted_ph": 7,
      "conditions": {
        "ambiguo": 3,
        "sorgente_non_disponibile": 2,
        "non_dichiarata": 2
      }
    },
    "timeline": {
      "h_pagina": 11384,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 11384
      },
      "placeholder_i2_n": 0,
      "i2_distinguishes_n": 0,
      "i2_not_distinguishes_n": 0,
      "len_asserted_ph": 0,
      "conditions": {}
    },
    "findings": {
      "h_pagina": 900,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 900
      },
      "placeholder_i2_n": 0,
      "i2_distinguishes_n": 0,
      "i2_not_distinguishes_n": 0,
      "len_asserted_ph": 0,
      "conditions": {}
    },
    "incidents": {
      "h_pagina": 900,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 900
      },
      "placeholder_i2_n": 0,
      "i2_distinguishes_n": 0,
      "i2_not_distinguishes_n": 0,
      "len_asserted_ph": 0,
      "conditions": {}
    },
    "plant": {
      "h_pagina": 2228,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 1,
        "h_pagina": 2228
      },
      "placeholder_i2_n": 8,
      "i2_distinguishes_n": 0,
      "i2_not_distinguishes_n": 8,
      "len_asserted_ph": 8,
      "conditions": {
        "non_dichiarata": 8
      }
    },
    "actions": {
      "h_pagina": 36515,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 36515
      },
      "placeholder_i2_n": 0,
      "i2_distinguishes_n": 0,
      "i2_not_distinguishes_n": 0,
      "len_asserted_ph": 0,
      "conditions": {}
    },
    "dashboard": {
      "h_pagina": 2140,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 2140
      },
      "placeholder_i2_n": 0,
      "i2_distinguishes_n": 0,
      "i2_not_distinguishes_n": 0,
      "len_asserted_ph": 0,
      "conditions": {}
    },
    "osservatorio": {
      "h_pagina": 900,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 900
      },
      "placeholder_i2_n": 0,
      "i2_distinguishes_n": 0,
      "i2_not_distinguishes_n": 0,
      "len_asserted_ph": 0,
      "conditions": {}
    },
    "dossier": {
      "h_pagina": 2192,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 3,
        "h_pagina": 2192
      },
      "placeholder_i2_n": 0,
      "i2_distinguishes_n": 0,
      "i2_not_distinguishes_n": 0,
      "len_asserted_ph": 0,
      "conditions": {}
    }
  },
  "M2_severity": {
    "monitoring": {
      "severity": "operativa (salute rete)",
      "placeholder_i2_n": 7,
      "ok_titled_snmp": 2,
      "violations_n": 5,
      "note": "5× «—» senza condizione I2 unica: poll.at / speedtest / latency / up_ratio; 2 SNMP già con title→sorgente_non_disponibile",
      "come_potrebbe_fallire": "confondere latenza assente con host down o con 0 ms"
    },
    "plant": {
      "severity": "operativa ALTA (impianto porte)",
      "placeholder_i2_n": 8,
      "violations_n": 8,
      "note": "dot-na «—» title «Link SNMP non misurabile» senza data-i2-condition; condizione reale=limite_strutturale (capability)",
      "come_potrebbe_fallire": "confondere link non misurabile con porta down o device assente"
    },
    "oggi": {
      "severity": "non-violazione I2 (falso positivo audit)",
      "placeholder_i2_n": 50,
      "note": "simboli matrice ODM «—» non pertinente e «–» contraddice + legenda; vocabolario diverso dalle cinque condizioni I2, già distinto dalla legenda. Non in scope D come I2.",
      "action": "escludere .odm-mark / legenda dall'audit e dal gate"
    },
    "other_routes": {
      "severity": "nessuna violazione placeholder I2 a 1280",
      "routes_clean": [
        "topology",
        "inventory",
        "gs308",
        "timeline",
        "findings",
        "incidents",
        "actions",
        "dashboard",
        "osservatorio",
        "dossier"
      ]
    }
  },
  "GATE_M": "violazioni reali oltre monitoring: plant (8). D = monitoring + plant + gate permanente + esclusione matrice."
}
```

**GATE M:** violazioni reali oltre monitoring → **plant (8)** (operativa ALTA). oggi@50 = simboli matrice ODM (falso positivo I2; esclusi in audit post). Altre rotte: 0 placeholder I2 non distinti @1280.

## 4. D — correzione

| Violazione | Condizione I2 | Resa |
|---|---|---|
| Plant ×8 dot-na SNMP | `limite_strutturale` | `data-i2-condition` + title «limite strutturale — Link SNMP non misurabile…» |
| Monitoring SNMP poll/traffico/errori su switch senza SNMP | `limite_strutturale` | binding `switchPollI2` |
| Monitoring latency / up_ratio / speedtest / history | `sorgente_non_disponibile` | title vocab «sorgente non disponibile — … (≠ 0 / ≠ assente)» |
| Matrice ODM «—»/«–» | n/a (non I2) | esclusione `.odm` in audit + allowlist gate |

D2: `evidence_gate.py` — placeholder foglia `>—<` su Monitoring/Plant senza `:data-i2-condition` = FAIL; self-test inject/remove.

## 5. Previsioni vs osservati

| Previsione | Osservato | Causa dominante |
|---|---|---|
| Δh layout ~0 (solo attributi/title) | V4: Δ=0 quasi ovunque; oggi@1280 Δ=−173 ≤R (card Zeek egress only_pre) | API coverage intermittente, non layout D |
| monitoring bad→0 | post: bad=0, cond dichiarate | D1 |
| plant bad→0 | post: 8× limite_strutturale | D1 |
| G4 census sempre match | topology@390 INVALID (28 vs 48 paths) | API topology non-idempotente — dichiarato INVALID |
| egress baseline chiusa | ancora `in_costruzione` coverage_days=0.48/3 | finestra temporale |

## 6. Verifica V1–V7 (integrale inline)

### V1 PRE/POST placeholder I2 + diff enumerato
```json
{
  "pre_sha256": "0076029e44a45f00a9c52e5dc21984b86bf509ede553f3bd11d68b054f43ec33",
  "post_sha256": "2c738a05d7a4b38d083f71ff99f48e7fb25fc4a8066b05ac5f650baa719b6f0f",
  "pre_1280": {
    "oggi": {
      "h_pagina": 15430,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 15430
      },
      "len_ph": 50,
      "len_bad": 50,
      "conditions": {
        "non_dichiarata": 50
      },
      "groups": [
        {
          "n": 40,
          "text": "—",
          "title": "",
          "cond": "non_dichiarata",
          "dist": false
        },
        {
          "n": 10,
          "text": "–",
          "title": "",
          "cond": "non_dichiarata",
          "dist": false
        }
      ]
    },
    "topology": {
      "h_pagina": 5559,
      "census": {
        "network_nodes": 29,
        "topology_paths": 27,
        "list_parents": 27,
        "inference_marks": 1,
        "h_pagina": 5559
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "inventory": {
      "h_pagina": 6305,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 6305
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "gs308": {
      "h_pagina": 1916,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 1,
        "h_pagina": 1916
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "monitoring": {
      "h_pagina": 1228,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 1228
      },
      "len_ph": 7,
      "len_bad": 5,
      "conditions": {
        "ambiguo": 3,
        "sorgente_non_disponibile": 2,
        "non_dichiarata": 2
      },
      "groups": [
        {
          "n": 3,
          "text": "—",
          "title": "",
          "cond": "ambiguo",
          "dist": false
        },
        {
          "n": 2,
          "text": "—",
          "title": "",
          "cond": "non_dichiarata",
          "dist": false
        },
        {
          "n": 1,
          "text": "—",
          "title": "Traffico non disponibile: nessun poll SNMP riuscito su questo switch (assente ≠ ",
          "cond": "sorgente_non_disponibile",
          "dist": true
        },
        {
          "n": 1,
          "text": "—",
          "title": "Contatori errori non disponibili senza poll SNMP riuscito.",
          "cond": "sorgente_non_disponibile",
          "dist": true
        }
      ]
    },
    "timeline": {
      "h_pagina": 11384,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 11384
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "findings": {
      "h_pagina": 900,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 900
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "incidents": {
      "h_pagina": 900,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 900
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "plant": {
      "h_pagina": 2228,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 1,
        "h_pagina": 2228
      },
      "len_ph": 8,
      "len_bad": 8,
      "conditions": {
        "non_dichiarata": 8
      },
      "groups": [
        {
          "n": 8,
          "text": "—",
          "title": "Link SNMP non misurabile su questo switch",
          "cond": "non_dichiarata",
          "dist": false
        }
      ]
    },
    "actions": {
      "h_pagina": 36515,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 36515
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "dashboard": {
      "h_pagina": 2140,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 2140
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "osservatorio": {
      "h_pagina": 900,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 900
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "dossier": {
      "h_pagina": 2192,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 3,
        "h_pagina": 2192
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    }
  },
  "post_1280": {
    "oggi": {
      "h_pagina": 15430,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 15430
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "topology": {
      "h_pagina": 7015,
      "census": {
        "network_nodes": 47,
        "topology_paths": 46,
        "list_parents": 46,
        "inference_marks": 1,
        "h_pagina": 7015
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "inventory": {
      "h_pagina": 6305,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 6305
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "gs308": {
      "h_pagina": 1916,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 1,
        "h_pagina": 1916
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "monitoring": {
      "h_pagina": 1228,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 1228
      },
      "len_ph": 5,
      "len_bad": 0,
      "conditions": {
        "limite_strutturale": 3,
        "sorgente_non_disponibile": 2
      },
      "groups": [
        {
          "n": 2,
          "text": "—",
          "title": "limite strutturale — SNMP non supportato su questo switch (≠ traffico a 0)",
          "cond": "limite_strutturale",
          "dist": true
        },
        {
          "n": 2,
          "text": "—",
          "title": "sorgente non disponibile — latenza non ancora misurata (≠ host assente, ≠ 0 ms)",
          "cond": "sorgente_non_disponibile",
          "dist": true
        },
        {
          "n": 1,
          "text": "—",
          "title": "limite strutturale — contatori errori non interrogabili via SNMP",
          "cond": "limite_strutturale",
          "dist": true
        }
      ]
    },
    "timeline": {
      "h_pagina": 11384,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 11384
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "findings": {
      "h_pagina": 900,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 900
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "incidents": {
      "h_pagina": 900,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 900
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "plant": {
      "h_pagina": 2228,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 1,
        "h_pagina": 2228
      },
      "len_ph": 8,
      "len_bad": 0,
      "conditions": {
        "limite_strutturale": 8
      },
      "groups": [
        {
          "n": 8,
          "text": "—",
          "title": "limite strutturale — Link SNMP non misurabile su questo switch (≠ porta down, ≠ ",
          "cond": "limite_strutturale",
          "dist": true
        }
      ]
    },
    "actions": {
      "h_pagina": 36487,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 36487
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "dashboard": {
      "h_pagina": 2140,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 2140
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "osservatorio": {
      "h_pagina": 900,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 0,
        "h_pagina": 900
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    },
    "dossier": {
      "h_pagina": 2192,
      "census": {
        "network_nodes": 0,
        "topology_paths": 0,
        "list_parents": 0,
        "inference_marks": 3,
        "h_pagina": 2192
      },
      "len_ph": 0,
      "len_bad": 0,
      "conditions": {},
      "groups": []
    }
  },
  "diff_enumerated": [
    {
      "route": "oggi",
      "pre_len_ph": 50,
      "post_len_ph": 0,
      "pre_bad": 50,
      "post_bad": 0,
      "pre_cond": {
        "non_dichiarata": 50
      },
      "post_cond": {},
      "pre_groups": [
        {
          "n": 40,
          "text": "—",
          "title": "",
          "cond": "non_dichiarata",
          "dist": false
        },
        {
          "n": 10,
          "text": "–",
          "title": "",
          "cond": "non_dichiarata",
          "dist": false
        }
      ],
      "post_groups": []
    },
    {
      "route": "monitoring",
      "pre_len_ph": 7,
      "post_len_ph": 5,
      "pre_bad": 5,
      "post_bad": 0,
      "pre_cond": {
        "ambiguo": 3,
        "sorgente_non_disponibile": 2,
        "non_dichiarata": 2
      },
      "post_cond": {
        "limite_strutturale": 3,
        "sorgente_non_disponibile": 2
      },
      "pre_groups": [
        {
          "n": 3,
          "text": "—",
          "title": "",
          "cond": "ambiguo",
          "dist": false
        },
        {
          "n": 2,
          "text": "—",
          "title": "",
          "cond": "non_dichiarata",
          "dist": false
        },
        {
          "n": 1,
          "text": "—",
          "title": "Traffico non disponibile: nessun poll SNMP riuscito su questo switch (assente ≠ ",
          "cond": "sorgente_non_disponibile",
          "dist": true
        },
        {
          "n": 1,
          "text": "—",
          "title": "Contatori errori non disponibili senza poll SNMP riuscito.",
          "cond": "sorgente_non_disponibile",
          "dist": true
        }
      ],
      "post_groups": [
        {
          "n": 2,
          "text": "—",
          "title": "limite strutturale — SNMP non supportato su questo switch (≠ traffico a 0)",
          "cond": "limite_strutturale",
          "dist": true
        },
        {
          "n": 2,
          "text": "—",
          "title": "sorgente non disponibile — latenza non ancora misurata (≠ host assente, ≠ 0 ms)",
          "cond": "sorgente_non_disponibile",
          "dist": true
        },
        {
          "n": 1,
          "text": "—",
          "title": "limite strutturale — contatori errori non interrogabili via SNMP",
          "cond": "limite_strutturale",
          "dist": true
        }
      ]
    },
    {
      "route": "plant",
      "pre_len_ph": 8,
      "post_len_ph": 8,
      "pre_bad": 8,
      "post_bad": 0,
      "pre_cond": {
        "non_dichiarata": 8
      },
      "post_cond": {
        "limite_strutturale": 8
      },
      "pre_groups": [
        {
          "n": 8,
          "text": "—",
          "title": "Link SNMP non misurabile su questo switch",
          "cond": "non_dichiarata",
          "dist": false
        }
      ],
      "post_groups": [
        {
          "n": 8,
          "text": "—",
          "title": "limite strutturale — Link SNMP non misurabile su questo switch (≠ porta down, ≠ ",
          "cond": "limite_strutturale",
          "dist": true
        }
      ]
    }
  ],
  "len_diff_asserted": 3
}
```
### V2 invarianza informativa
```json
{
  "note": "D1 aggiunge data-i2-condition + title vocab; nessun dato di rete rimosso",
  "informative_removals": [],
  "classification_added_bucket": [
    "Monitoring: data-i2-condition su poll/traffico/errori/latency/up_ratio/speedtest/history",
    "Plant: data-i2-condition=limite_strutturale su dot-na SNMP"
  ],
  "len_removals_asserted": 0,
  "len_classif_added_asserted": 2
}
```
### V3 evidence_gate (+ self-test)
```
=== evidence_gate ===
=== evidence_gate ===
forbidden_ownership_terms=4
  /collegato\s+a/ — asserisce ownership di link; FDB prova solo passaggio MAC (I5 rango 60)
  /attaccat[oa]\s+a/ — sinonimo ownership fisico; vietato su FDB
  /assegnat[oa]\s+(alla|alla porta|a porta)/ — asserisce assegnazione porta; FDB non è LLDP/manual
  /appartiene\s+a/ — asserisce appartenenza; FDB non è identità
i2_conditions=['sorgente_non_disponibile', 'dispositivo_assente', 'misurato_a_zero', 'disabilitato_dall_operatore', 'limite_strutturale']
ownership_hits=0
marker_errors=0
i2_placeholder_errors=0
PASS: no FDB+ownership vocabulary; required evidence markers present; I2 placeholders declared
EXIT:0
SELFTEST ownership inject detected: views/_o20_evidence_gate_inject_tmp.vue:2: /collegato\s+a/ — asserisce ownership di link; FDB prova solo passaggio MAC (I5 rango 60) | <template><span class='edge-fdb'>collegato a switch</span></template>
SELFTEST i2 inject detected: views/Monitoring.vue:930: placeholder senza data-i2-condition/I2 vocab — dichiarare una di ('sorgente_non_disponibile', 'dispositivo_assente', 'misurato_a_zero', 'disabilitato_dall_operatore', 'limite_strutturale') | <span class="muted">—</span>
SELFTEST i2 after remove hits=0
SELFTEST marker_errs_after_inject=0 ownership_hits=0
SELFTEST marker_errs_after_stronger=1
SELFTEST marker inject detected: views/Topology.vue: marker /visto passare/ count=0 < 1 — vocabolario FDB O19 obbligatorio sulla Mappa
SELFTEST PASS: inject fails (ownership+marker+i2), remove passes
SELF:0

```
### V4 altezze PRE/POST (censimento entrambi i lati)
```json
{
  "R_height": 320,
  "criteria": {
    "V4_fdb_ownership_post_empty": {
      "pass": true,
      "n": 0,
      "rows": [],
      "come_potrebbe_fallire": "Plant cella FDB senza «visto passare» o topology parent ancora «collegato a»"
    },
    "V8_height_within_R_when_census_matched": {
      "pass": true,
      "rows": [
        {
          "route": "oggi",
          "w": 1280,
          "delta": -173,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "oggi",
          "w": 768,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "oggi",
          "w": 390,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "topology",
          "w": 1280,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "topology",
          "w": 768,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "topology",
          "w": 390,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "plant",
          "w": 1280,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "plant",
          "w": 768,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "plant",
          "w": 390,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "gs308",
          "w": 1280,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "gs308",
          "w": 768,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "gs308",
          "w": 390,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "inventory",
          "w": 1280,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "inventory",
          "w": 768,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "inventory",
          "w": 390,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "dossier",
          "w": 1280,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "dossier",
          "w": 768,
          "delta": 0,
          "ok": true,
          "census_matched": true
        },
        {
          "route": "dossier",
          "w": 390,
          "delta": 0,
          "ok": true,
          "census_matched": true
        }
      ],
      "R": 320,
      "come_potrebbe_fallire": "Δ layout non voluto oltre R; nominarlo non basta (DEBT-V8-CRITERION-WEAK)"
    },
    "census_invalid_measures": {
      "pass": true,
      "invalid": [],
      "come_potrebbe_fallire": "API topology/plant non idempotente tra i due server"
    }
  },
  "routes": {
    "oggi": {
      "1280": {
        "census_matched": true,
        "h_pre": 15603,
        "h_post": 15430,
        "delta_h": -173,
        "pre_census": {
          "h_pagina": 15603,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 0
        },
        "post_census": {
          "h_pagina": 15430,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 0
        },
        "only_pre_info": [
          "Sorgente copertura vecchia · Zeek egress hybrid (ext host+port / int relazione)"
        ],
        "only_post_info": [],
        "script_pre": "/assets/index-DRlt-wzC.js",
        "script_post": "/assets/index-D7HHopYw.js",
        "version_meta_post": "0.10.90"
      },
      "768": {
        "census_matched": true,
        "h_pre": 18943,
        "h_post": 18943,
        "delta_h": 0,
        "pre_census": {
          "h_pagina": 18943,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 0
        },
        "post_census": {
          "h_pagina": 18943,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 0
        },
        "only_pre_info": [],
        "only_post_info": [],
        "script_pre": "/assets/index-DRlt-wzC.js",
        "script_post": "/assets/index-D7HHopYw.js",
        "version_meta_post": "0.10.90"
      },
      "390": {
        "census_matched": true,
        "h_pre": 23815,
        "h_post": 23815,
        "delta_h": 0,
        "pre_census": {
          "h_pagina": 23815,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 0
        },
        "post_census": {
          "h_pagina": 23815,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 0
        },
        "only_pre_info": [],
        "only_post_info": [],
        "script_pre": "/assets/index-DRlt-wzC.js",
        "script_post": "/assets/index-D7HHopYw.js",
        "version_meta_post": "0.10.90"
      }
    },
    "topology": {
      "1280": {
        "census_matched": true,
        "h_pre": 7015,
        "h_post": 7015,
        "delta_h": 0,
        "pre_census": {
          "h_pagina": 7015,
          "paths_svg": 46,
          "list_parents": 46,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 0
        },
        "post_census": {
          "h_pagina": 7015,
          "paths_svg": 46,
          "list_parents": 46,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 0
        },
        "only_pre_info": [],
        "only_post_info": [],
        "script_pre": "/assets/index-DRlt-wzC.js",
        "script_post": "/assets/index-D7HHopYw.js",
        "version_meta_post": "0.10.90"
      },
      "768": {
        "census_matched": true,
        "h_pre": 7776,
        "h_post": 7776,
        "delta_h": 0,
        "pre_census": {
          "h_pagina": 7776,
          "paths_svg": 46,
          "list_parents": 46,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 0
        },
        "post_census": {
          "h_pagina": 7776,
          "paths_svg": 46,
          "list_parents": 46,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 0
        },
        "only_pre_info": [],
        "only_post_info": [],
        "script_pre": "/assets/index-DRlt-wzC.js",
        "script_post": "/assets/index-D7HHopYw.js",
        "version_meta_post": "0.10.90"
      },
      "390": {
        "census_matched": true,
        "h_pre": 10242,
        "h_post": 10242,
        "delta_h": 0,
        "pre_census": {
          "h_pagina": 10242,
          "paths_svg": 46,
          "list_parents": 46,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 0
        },
        "post_census": {
          "h_pagina": 10242,
          "paths_svg": 46,
          "list_parents": 46,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 0
        },
        "only_pre_info": [],
        "only_post_info": [],
        "script_pre": "/assets/index-DRlt-wzC.js",
        "script_post": "/assets/index-D7HHopYw.js",
        "version_meta_post": "0.10.90"
      }
    },
    "plant": {
      "1280": {
        "census_matched": true,
        "h_pre": 2228,
        "h_post": 2228,
        "delta_h": 0,
        "pre_census": {
          "h_pagina": 2228,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 46,
          "ports_fdb": 13,
          "placements": 0
        },
        "post_census": {
          "h_pagina": 2228,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 46,
          "ports_fdb": 13,
          "placements": 0
        },
        "only_pre_info": [],
        "only_post_info": [],
        "script_pre": "/assets/index-DRlt-wzC.js",
        "script_post": "/assets/index-D7HHopYw.js",
        "version_meta_post": "0.10.90"
      },
      "768": {
        "census_matched": true,
        "h_pre": 2964,
        "h_post": 2964,
        "delta_h": 0,
        "pre_census": {
          "h_pagina": 2964,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 46,
          "ports_fdb": 13,
          "placements": 0
        },
        "post_census": {
          "h_pagina": 2964,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 46,
          "ports_fdb": 14,
          "placements": 0
        },
        "only_pre_info": [
          "LGS328CFDB fresca"
        ],
        "only_post_info": [],
        "script_pre": "/assets/index-DRlt-wzC.js",
        "script_post": "/assets/index-D7HHopYw.js",
        "version_meta_post": "0.10.90"
      },
      "390": {
        "census_matched": true,
        "h_pre": 5505,
        "h_post": 5505,
        "delta_h": 0,
        "pre_census": {
          "h_pagina": 5505,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 46,
          "ports_fdb": 14,
          "placements": 0
        },
        "post_census": {
          "h_pagina": 5505,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 46,
          "ports_fdb": 14,
          "placements": 0
        },
        "only_pre_info": [],
        "only_post_info": [],
        "script_pre": "/assets/index-DRlt-wzC.js",
        "script_post": "/assets/index-D7HHopYw.js",
        "version_meta_post": "0.10.90"
      }
    },
    "gs308": {
      "1280": {
        "census_matched": true,
        "h_pre": 1916,
        "h_post": 1916,
        "delta_h": 0,
        "pre_census": {
          "h_pagina": 1916,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 2
        },
        "post_census": {
          "h_pagina": 1916,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 2
        },
        "only_pre_info": [],
        "only_post_info": [],
        "script_pre": "/assets/index-DRlt-wzC.js",
        "script_post": "/assets/index-D7HHopYw.js",
        "version_meta_post": "0.10.90"
      },
      "768": {
        "census_matched": true,
        "h_pre": 2099,
        "h_post": 2099,
        "delta_h": 0,
        "pre_census": {
          "h_pagina": 2099,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 2
        },
        "post_census": {
          "h_pagina": 2099,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 2
        },
        "only_pre_info": [],
        "only_post_info": [],
        "script_pre": "/assets/index-DRlt-wzC.js",
        "script_post": "/assets/index-D7HHopYw.js",
        "version_meta_post": "0.10.90"
      },
      "390": {
        "census_matched": true,
        "h_pre": 3254,
        "h_post": 3254,
        "delta_h": 0,
        "pre_census": {
          "h_pagina": 3254,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 2
        },
        "post_census": {
          "h_pagina": 3254,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 2
        },
        "only_pre_info": [],
        "only_post_info": [],
        "script_pre": "/assets/index-DRlt-wzC.js",
        "script_post": "/assets/index-D7HHopYw.js",
        "version_meta_post": "0.10.90"
      }
    },
    "inventory": {
      "1280": {
        "census_matched": true,
        "h_pre": 6305,
        "h_post": 6305,
        "delta_h": 0,
        "pre_census": {
          "h_pagina": 6305,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 0
        },
        "post_census": {
          "h_pagina": 6305,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 0
        },
        "only_pre_info": [],
        "only_post_info": [],
        "script_pre": "/assets/index-DRlt-wzC.js",
        "script_post": "/assets/index-D7HHopYw.js",
        "version_meta_post": "0.10.90"
      },
      "768": {
        "census_matched": true,
        "h_pre": 6418,
        "h_post": 6418,
        "delta_h": 0,
        "pre_census": {
          "h_pagina": 6418,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 0
        },
        "post_census": {
          "h_pagina": 6418,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 0
        },
        "only_pre_info": [],
        "only_post_info": [],
        "script_pre": "/assets/index-DRlt-wzC.js",
        "script_post": "/assets/index-D7HHopYw.js",
        "version_meta_post": "0.10.90"
      },
      "390": {
        "census_matched": true,
        "h_pre": 6712,
        "h_post": 6712,
        "delta_h": 0,
        "pre_census": {
          "h_pagina": 6712,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 0
        },
        "post_census": {
          "h_pagina": 6712,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 0
        },
        "only_pre_info": [],
        "only_post_info": [],
        "script_pre": "/assets/index-DRlt-wzC.js",
        "script_post": "/assets/index-D7HHopYw.js",
        "version_meta_post": "0.10.90"
      }
    },
    "dossier": {
      "1280": {
        "census_matched": true,
        "h_pre": 2192,
        "h_post": 2192,
        "delta_h": 0,
        "pre_census": {
          "h_pagina": 2192,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 1
        },
        "post_census": {
          "h_pagina": 2192,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 1
        },
        "only_pre_info": [],
        "only_post_info": [],
        "script_pre": "/assets/index-DRlt-wzC.js",
        "script_post": "/assets/index-D7HHopYw.js",
        "version_meta_post": "0.10.90"
      },
      "768": {
        "census_matched": true,
        "h_pre": 2340,
        "h_post": 2340,
        "delta_h": 0,
        "pre_census": {
          "h_pagina": 2340,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 1
        },
        "post_census": {
          "h_pagina": 2340,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 1
        },
        "only_pre_info": [],
        "only_post_info": [],
        "script_pre": "/assets/index-DRlt-wzC.js",
        "script_post": "/assets/index-D7HHopYw.js",
        "version_meta_post": "0.10.90"
      },
      "390": {
        "census_matched": true,
        "h_pre": 2944,
        "h_post": 2944,
        "delta_h": 0,
        "pre_census": {
          "h_pagina": 2944,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 1
        },
        "post_census": {
          "h_pagina": 2944,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 0,
          "ports_fdb": 0,
          "placements": 1
        },
        "only_pre_info": [],
        "only_post_info": [],
        "script_pre": "/assets/index-DRlt-wzC.js",
        "script_post": "/assets/index-D7HHopYw.js",
        "version_meta_post": "0.10.90"
      }
    }
  }
}
```
### V5 oggi@768 con esclusione flaky (0.1)
```json
{
  "wave": "O21-B0.1",
  "auth_provenance": "catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato",
  "width": 768,
  "R_height": 320,
  "allowlist": [
    {
      "pattern": "Fritz TR-064",
      "debt": "DEBT-O20-OGGI-API-HEIGHT-JITTER",
      "reason": "O16-M1/O17: card coverage Fritz TR-064 presente/assente tra run (coverage_source_blind); causa payload API, non layout UI"
    },
    {
      "pattern": "Zeek behaviour",
      "debt": "DEBT-O20-OGGI-API-HEIGHT-JITTER",
      "reason": "O20 V only_post_info: card «Zeek behaviour» intermittente insieme a Fritz nello stesso Δ+409 @768; stessa famiglia coverage_source_* API-based"
    }
  ],
  "len_allowlist_asserted": 2,
  "come_potrebbe_fallire": "se Δ resta >R dopo esclusione Fritz/Zeek, la causa non è quella allowlist — STOP, non escludere altro",
  "o20_reference_delta_plus409": {
    "source": "docs/obs-o20.md / KNOWN_DEBT (artefatto pinnato)",
    "delta_h": 409,
    "note": "Δ−212 solo-chat NON ammesso come evidenza"
  },
  "pre": {
    "h_raw": 18943,
    "h_excl": 18943,
    "cards_n": 30,
    "flaky_hidden_n": 0,
    "flaky_hidden": [],
    "frontend_version": null,
    "api_health_version": null,
    "script_src": "/assets/index-DRlt-wzC.js"
  },
  "post": {
    "h_raw": 18943,
    "h_excl": 18943,
    "cards_n": 30,
    "flaky_hidden_n": 0,
    "flaky_hidden": [],
    "frontend_version": "0.10.90",
    "api_health_version": "0.10.82",
    "script_src": "/assets/index-D7HHopYw.js"
  },
  "delta_h_raw": 0,
  "delta_h_excl_flaky": 0,
  "pass_excl": true,
  "pass_raw": true
}
```
### V6 GATE ESISTENTI (output integrale)
```
=== w8_currency_gate ===
== W8 CURRENCY GATE (indurito, W8-fix2) ==
root: /Users/michelestorci/Developer/rete-palazzo/observatory
sentinelle: simbolo ORM 'FactAssertion' · tabella grezza 'fact_assertions' in chiamata SQL (text/execute) · COMBO (fact-token FactAssertion|fact_assertions|fact_key) + valore di stato quotato 'current'
scope: api/**, scripts/**, collector/**
esclusioni:
  - api/app/facts/**  (il resolver È la fonte della correntezza)
  - scripts/w8_currency_gate.py  (contiene le sentinelle/fact_key come dato)
  - scripts/w8_g8_equivalence.py  (contiene le sentinelle/fact_key come dato)
file scansionati: 218
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
=== specificity ===
=== color_literal_gate ===
PASS: no hard-coded color literals outside allowlist; matrix.css decls-only
  token_file=assets/matrix.css (literals only in --custom-property decls)
  allowlist_count=16
EXIT:0
SELFTEST vue inject detected: (2, '#ff00aa', '.x { color: #ff00aa; /* O13D_COLOR_GATE_INJECT */ }')
SELFTEST matrix rule inject detected: (956, '#ff00aa', '.o14fix-gate-inject { color: #ff00aa; /* O14FIX_COLOR_GATE_INJECT */ }')
SELFTEST PASS: inject fails (vue+matrix rule), remove passes
SELF:0
=== contrast_gate ===
=== contrast_gate ===
token_file=web/src/assets/matrix.css
pairs_checked=9
allowlist_entries=1
  PASS --text-1=#e8ebf0 on --bg-0=#0f1319 ratio=15.586 thr=4.5 [text_normal] WCAG 2.2 SC 1.4.3 Contrast (Minimum) AA testo normale
  PASS --text-2=#98a2b3 on --bg-0=#0f1319 ratio=7.232 thr=4.5 [text_normal] WCAG 2.2 SC 1.4.3 Contrast (Minimum) AA testo normale
  FAIL --text-3=#667085 on --bg-0=#0f1319 ratio=3.744 thr=4.5 [text_normal] WCAG 2.2 SC 1.4.3 Contrast (Minimum) AA testo normale
  PASS --ok=#4fb477 on --bg-0=#0f1319 ratio=7.208 thr=3.0 [non_text] WCAG 2.2 SC 1.4.11 Non-text Contrast AA
  PASS --warn=#d9a441 on --bg-0=#0f1319 ratio=8.281 thr=3.0 [non_text] WCAG 2.2 SC 1.4.11 Non-text Contrast AA
  PASS --danger=#e06b52 on --bg-0=#0f1319 ratio=5.671 thr=3.0 [non_text] WCAG 2.2 SC 1.4.11 Non-text Contrast AA
  PASS --inference=#9b7bd4 on --bg-0=#0f1319 ratio=5.479 thr=3.0 [non_text] WCAG 2.2 SC 1.4.11 Non-text Contrast AA (riempimento; non toccare in O20)
  PASS --inference-edge=#7656b0 on --bg-1=#161b23 ratio=3.068 thr=3.0 [non_text] WCAG 2.2 SC 1.4.11 Non-text Contrast AA
  PASS --inference-edge=#7656b0 on --bg-0=#0f1319 ratio=3.307 thr=3.0 [non_text] WCAG 2.2 SC 1.4.11 Non-text Contrast AA
ALLOWLISTED_FAILS=1
  TEMP --text-3 on --bg-0 ratio=3.744 debt=DEBT-NO-CONTRAST-PRESIDIO | testo terziario mute (#667085) spesso <4.5:1 su bg-0; etichette via/odm già in DEBT-NO-CONTRAST-PRES
PASS: contrast pairs within threshold or allowlisted with debt
EXIT:0
SELFTEST inject detected: {'fg': '--inference-edge', 'bg': '--bg-1', 'fg_hex': '#220033', 'bg_hex': '#161b23', 'ratio': 1.089, 'threshold': 3.0, 'fonte': 'WCAG 2.2 SC 1.4.11 Non-text Contrast AA', 'ruolo': 'non_text', 'pass': False}
SELFTEST PASS: inject fails, remove passes
SELF:0
=== evidence_gate ===
=== evidence_gate ===
forbidden_ownership_terms=4
  /collegato\s+a/ — asserisce ownership di link; FDB prova solo passaggio MAC (I5 rango 60)
  /attaccat[oa]\s+a/ — sinonimo ownership fisico; vietato su FDB
  /assegnat[oa]\s+(alla|alla porta|a porta)/ — asserisce assegnazione porta; FDB non è LLDP/manual
  /appartiene\s+a/ — asserisce appartenenza; FDB non è identità
i2_conditions=['sorgente_non_disponibile', 'dispositivo_assente', 'misurato_a_zero', 'disabilitato_dall_operatore', 'limite_strutturale']
ownership_hits=0
marker_errors=0
i2_placeholder_errors=0
PASS: no FDB+ownership vocabulary; required evidence markers present; I2 placeholders declared
EXIT:0
SELFTEST ownership inject detected: views/_o20_evidence_gate_inject_tmp.vue:2: /collegato\s+a/ — asserisce ownership di link; FDB prova solo passaggio MAC (I5 rango 60) | <template><span class='edge-fdb'>collegato a switch</span></template>
SELFTEST i2 inject detected: views/Monitoring.vue:930: placeholder senza data-i2-condition/I2 vocab — dichiarare una di ('sorgente_non_disponibile', 'dispositivo_assente', 'misurato_a_zero', 'disabilitato_dall_operatore', 'limite_strutturale') | <span class="muted">—</span>
SELFTEST i2 after remove hits=0
SELFTEST marker_errs_after_inject=0 ownership_hits=0
SELFTEST marker_errs_after_stronger=1
SELFTEST marker inject detected: views/Topology.vue: marker /visto passare/ count=0 < 1 — vocabolario FDB O19 obbligatorio sulla Mappa
SELFTEST PASS: inject fails (ownership+marker+i2), remove passes
SELF:0

```
### V6 drift repo↔NAS (eseguito)
```json
{
  "phase": "post_deploy",
  "NAS_count": 80,
  "repo_count": 79,
  "solo_NAS": [
    "scripts/_w4a_measure.py"
  ],
  "solo_repo": [],
  "solo_NAS_enumerated": [
    "scripts/_w4a_measure.py"
  ],
  "solo_repo_enumerated": [],
  "expected": {
    "solo_NAS": [
      "scripts/_w4a_measure.py"
    ],
    "solo_repo": []
  },
  "orphans": [],
  "DRIFT_OK": true,
  "note": "solo_repo non vuoto = script locali non syncati o esclusi da rsync; DRIFT_OK=orphans NAS assenti oltre _w4a"
}
```
### V6 conservation (endpoint + cardinalità)
```json
{
  "assets_endpoint": "/api/assets?include_historical=true&all_proposals=true (stesso di Oggi.load)",
  "assets_n": 151,
  "UI_DOM_names_sample": [
    "Fatti osservati",
    "Dati mancanti o non correnti",
    "Interpretazione deterministica",
    "INFERENZA IA",
    "Fatti osservati",
    "Dati mancanti o non correnti",
    "Interpretazione deterministica",
    "INFERENZA IA",
    "Fatti osservati",
    "Dati mancanti o non correnti",
    "Interpretazione deterministica",
    "INFERENZA IA",
    "Fatti osservati",
    "Dati mancanti o non correnti",
    "Interpretazione deterministica",
    "INFERENZA IA",
    "Fatti osservati",
    "Dati mancanti o non correnti",
    "Interpretazione deterministica",
    "INFERENZA IA"
  ],
  "UI_DOM_names_n": 40,
  "note": "queueConservationCheck: confronto card Apparati vs payload; missing/duplicated se divergenza"
}
```
### V7 catture + o9_png_assert
```json
{
  "deviceScaleFactor": 1,
  "captures": {
    "oggi": {
      "1280": {
        "h_pre_scrub": 15430,
        "h_post_scrub": 15430,
        "h_PNG": 15430,
        "h_pagina_report": 15430,
        "png": "docs/o21-captures/obs-o21-oggi-1280.png",
        "png_w": 1280,
        "frontend": "0.10.90",
        "api_health": "0.10.82"
      },
      "768": {
        "h_pre_scrub": 18943,
        "h_post_scrub": 18943,
        "h_PNG": 18943,
        "h_pagina_report": 18943,
        "png": "docs/o21-captures/obs-o21-oggi-768.png",
        "png_w": 768,
        "frontend": "0.10.90",
        "api_health": "0.10.82"
      },
      "390": {
        "h_pre_scrub": 23815,
        "h_post_scrub": 23815,
        "h_PNG": 23815,
        "h_pagina_report": 23815,
        "png": "docs/o21-captures/obs-o21-oggi-390.png",
        "png_w": 390,
        "frontend": "0.10.90",
        "api_health": "0.10.82"
      }
    },
    "monitoring": {
      "1280": {
        "h_pre_scrub": 1228,
        "h_post_scrub": 1228,
        "h_PNG": 1228,
        "h_pagina_report": 1228,
        "png": "docs/o21-captures/obs-o21-monitoring-1280.png",
        "png_w": 1280,
        "frontend": "0.10.90",
        "api_health": "0.10.82"
      },
      "768": {
        "h_pre_scrub": 1314,
        "h_post_scrub": 1314,
        "h_PNG": 1314,
        "h_pagina_report": 1314,
        "png": "docs/o21-captures/obs-o21-monitoring-768.png",
        "png_w": 768,
        "frontend": "0.10.90",
        "api_health": "0.10.82"
      },
      "390": {
        "h_pre_scrub": 1431,
        "h_post_scrub": 1431,
        "h_PNG": 1431,
        "h_pagina_report": 1431,
        "png": "docs/o21-captures/obs-o21-monitoring-390.png",
        "png_w": 390,
        "frontend": "0.10.90",
        "api_health": "0.10.82"
      }
    },
    "plant": {
      "1280": {
        "h_pre_scrub": 2228,
        "h_post_scrub": 2228,
        "h_PNG": 2228,
        "h_pagina_report": 2228,
        "png": "docs/o21-captures/obs-o21-plant-1280.png",
        "png_w": 1282,
        "frontend": "0.10.90",
        "api_health": "0.10.82"
      },
      "768": {
        "h_pre_scrub": 2964,
        "h_post_scrub": 2964,
        "h_PNG": 2964,
        "h_pagina_report": 2964,
        "png": "docs/o21-captures/obs-o21-plant-768.png",
        "png_w": 768,
        "frontend": "0.10.90",
        "api_health": "0.10.82"
      },
      "390": {
        "h_pre_scrub": 5505,
        "h_post_scrub": 5505,
        "h_PNG": 5505,
        "h_pagina_report": 5505,
        "png": "docs/o21-captures/obs-o21-plant-390.png",
        "png_w": 390,
        "frontend": "0.10.90",
        "api_health": "0.10.82"
      }
    },
    "topology": {
      "1280": {
        "h_pre_scrub": 7199,
        "h_post_scrub": 7199,
        "h_PNG": 7199,
        "h_pagina_report": 7199,
        "png": "docs/o21-captures/obs-o21-topology-1280.png",
        "png_w": 1280,
        "frontend": "0.10.90",
        "api_health": "0.10.82"
      },
      "768": {
        "h_pre_scrub": 7868,
        "h_post_scrub": 7868,
        "h_PNG": 7868,
        "h_pagina_report": 7868,
        "png": "docs/o21-captures/obs-o21-topology-768.png",
        "png_w": 768,
        "frontend": "0.10.90",
        "api_health": "0.10.82"
      },
      "390": {
        "h_pre_scrub": 9101,
        "h_post_scrub": 9101,
        "h_PNG": 9101,
        "h_pagina_report": 9101,
        "png": "docs/o21-captures/obs-o21-topology-390.png",
        "png_w": 390,
        "frontend": "0.10.90",
        "api_health": "0.10.82"
      }
    }
  },
  "o9_png_assert": [
    {
      "pair": [
        1280,
        768
      ],
      "exit": 0,
      "out": "obs-o21-oggi-1280.png: 1280x15430 sha256=171196c9cc4994bf5ca042f3239634df214f9f08323a5d97ef9af41ac146b493\nobs-o21-oggi-768.png: 768x18943 sha256=3ee81171a688570ce74bad90e7b2c544aba2a1d9ea16510e7e3659ebc8232a7a\nPASS pair distinct widths\n",
      "err": ""
    },
    {
      "pair": [
        1280,
        390
      ],
      "exit": 0,
      "out": "obs-o21-oggi-1280.png: 1280x15430 sha256=171196c9cc4994bf5ca042f3239634df214f9f08323a5d97ef9af41ac146b493\nobs-o21-oggi-390.png: 390x23815 sha256=f6f0b6511abc4bb3e545367280894b626804c21dcf8b726a9989096132733f41\nPASS pair distinct widths\n",
      "err": ""
    }
  ],
  "nota_plant_1280": "png_w=1282 su plant@1280 (scrollbar/chrome); h_PNG==h_pagina"
}
```
## 7. Debiti

| Debito | Stato | Attribuzione |
|---|---|---|
| DEBT-O20-OGGI-API-HEIGHT-JITTER | CHIUSO | O21 0.1 |
| DEBT-O20-G4-CENSUS-MISMATCH-UNFLAGGED | CHIUSO | O21 0.2 |
| DEBT-O20-VERSION-FIELD-AMBIGUOUS | CHIUSO | O21 0.3 |
| DEBT-O20-M2-BASELINE-NOT-PRESERVED | APERTO (disciplina) | O20; regola da O21 |
| DEBT-O20-V-BLOCKS-NOT-INLINE | CHIUSO | revisore/Cursor; chiuso O21 |
| DEBT-O20-I2-SITEWIDE-INCOMPLETE | CHIUSO | O21 M+D+gate |
| DEBT-O19-MAPPA-DESKTOP-GROWTH | APERTO | fuori scope |
| DEBT-OGGI-MOBILE-DENSITY | APERTO | fuori scope |

## 8. Egress (verifica a finestra)

### Stato baseline egress
```json
{
  "ok": true,
  "keys": [
    "cards",
    "invalid_baseline_emissions",
    "invalid_baseline_emissions_count",
    "baseline",
    "novelty_emission",
    "novelty_suppression",
    "novelty_signals_enabled",
    "novelty_signals_env",
    "breaker_open",
    "breaker_reason",
    "table",
    "note",
    "o13c_marker",
    "o13cfix_marker",
    "o13d_marker",
    "defense_priority_id"
  ],
  "baseline": {
    "status": "in_costruzione",
    "baseline_ready": false,
    "baseline_started_at": "2026-07-29T09:59:03.002912Z",
    "baseline_ready_at": "2026-07-29T10:25:05.629320Z",
    "premature_baseline_ready_at_was": "2026-07-29T09:59:03.948740Z",
    "premature_invalidated_at": "2026-07-29T12:33:20.264645Z",
    "reason": "O13D: re-stamp novelty_suppression_active after deploy 0.10.81",
    "o13c_marker": "obs-o13c",
    "o13cfix_marker": "obs-o13c-fix",
    "o13d_marker": "obs-o13d",
    "cycle_seen": 98,
    "cycle_created": 0,
    "cycle_deferred": 19,
    "cycle_novelty_new": 0,
    "readiness": {
      "ready": false,
      "coverage_ok": false,
      "series_ok": false,
      "coverage_days": 0.4775,
      "min_coverage_days": 3,
      "min_coverage_source": "O13B M1: 3 giorni misurati; asintoto non stimabile",
      "min_series_days": 3,
      "min_series_source": "O13B M1 curva novità a 3 punti (non soglia sul tasso)",
      "missing": {
        "coverage_days_needed": 3,
        "coverage_days_have": 0.4775,
        "coverage_days_remaining": 2.522494877152778,
        "novelty_series_needed": 3,
        "novelty_series_have": 0,
        "novelty_series_remaining": 3,
        "complete_utc_days_with_rows": [],
        "novelty_by_day": {}
      },
      "forbidden_criterion": "deferred==0"
    },
    "novelty_suppression": {
      "active": true,
      "reason": "premature_baseline_protection",
      "since": "2026-07-29T12:33:20.264645Z",
      "age_sec": 31999.180881,
      "lifted_at": null,
      "lift_reason": null,
      "manual_suppress": false,
      "signals_armed": false,
      "novelty_auto_enabled": false,
      "distinct_from": [
        "cieca",
        "disabilitata"
      ]
    },
    "novelty_signals_note": "emissione N5 gated da resolve_novelty_emission (signals_armed / manual_suppress; distinto da EGRESS_INGEST_ENABLED)"
  },
  "readiness": {
    "ready": false,
    "coverage_ok": false,
    "series_ok": false,
    "coverage_days": 0.4775,
    "min_coverage_days": 3,
    "min_coverage_source": "O13B M1: 3 giorni misurati; asintoto non stimabile",
    "min_series_days": 3,
    "min_series_source": "O13B M1 curva novità a 3 punti (non soglia sul tasso)",
    "missing": {
      "coverage_days_needed": 3,
      "coverage_days_have": 0.4775,
      "coverage_days_remaining": 2.522494877152778,
      "novelty_series_needed": 3,
      "novelty_series_have": 0,
      "novelty_series_remaining": 3,
      "complete_utc_days_with_rows": [],
      "novelty_by_day": {}
    },
    "forbidden_criterion": "deferred==0"
  },
  "marked_emissions": null
}
```

**Non chiusa:** `baseline_ready=false`, `coverage_days≈0.48` su min 3, `novelty_series_have=0` su min 3. Nessuna azione (solo report).

## 9. Cosa NON hai fatto

- Nessun ritocco `--inference` / `--inference-edge` / layout / T7 / FA251 / `_w4a_measure.py` / favicon / grano egress
- Nessun deploy api (solo `deploy.sh web`)
- Nessun merge/tag/force su main
- Matrice ODM: non riscritta come I2 (vocabolario diverso; esclusa)
- Inventario/Dossier `|| "—"` fuori dalle violazioni M runtime: non espansi in D
- Conservazione: enumerazione DOM sample + assets_n (non full buildChassisNameCards O20 — endpoint dichiarato)
- G4 topology@390: INVALID dichiarato (non assorbito in R)

## G — deploy / git

- G1 bump 0.10.90
- G2 `./scripts/deploy.sh web` → ok
- G3 PASS (fe 0.10.90, css presente, api_health 0.10.82)
### G4 deployed↔local
```json
{
  "all_pass": false,
  "invalid": [
    "topology@390"
  ],
  "G4_note": "topology@390 INVALID_CENSUS (paths 28 vs 48) — causa API topology non-idempotente (§0.3 O20 / 0.2 O21); Δh non trattato come ok. Altri PASS con fe=0.10.90 api_health=0.10.82.",
  "routes": {
    "topology": {
      "1280": {
        "width": 1280,
        "census_matched": true,
        "local": {
          "h_pagina": 7101,
          "paths_svg": 47,
          "list_parents": 47,
          "ports": 0,
          "ports_visto": 0,
          "frontend_version": "0.10.90",
          "api_health_version_from_page": "0.10.82",
          "script_src": "/assets/index-D7HHopYw.js",
          "css_href": "/assets/index-p4FzMslc.css"
        },
        "deployed": {
          "h_pagina": 7101,
          "paths_svg": 47,
          "list_parents": 47,
          "ports": 0,
          "ports_visto": 0,
          "frontend_version": "0.10.90",
          "api_health_version_from_page": "0.10.82",
          "script_src": "/assets/index-D7HHopYw.js",
          "css_href": "/assets/index-p4FzMslc.css"
        },
        "census_key_local": [
          47,
          47
        ],
        "census_key_deployed": [
          47,
          47
        ],
        "delta_h": 0,
        "delta_h_valid": true,
        "within_R": true,
        "verdict": "PASS"
      },
      "768": {
        "width": 768,
        "census_matched": true,
        "local": {
          "h_pagina": 6429,
          "paths_svg": 28,
          "list_parents": 28,
          "ports": 0,
          "ports_visto": 0,
          "frontend_version": "0.10.90",
          "api_health_version_from_page": "0.10.82",
          "script_src": "/assets/index-D7HHopYw.js",
          "css_href": "/assets/index-p4FzMslc.css"
        },
        "deployed": {
          "h_pagina": 6429,
          "paths_svg": 28,
          "list_parents": 28,
          "ports": 0,
          "ports_visto": 0,
          "frontend_version": "0.10.90",
          "api_health_version_from_page": "0.10.82",
          "script_src": "/assets/index-D7HHopYw.js",
          "css_href": "/assets/index-p4FzMslc.css"
        },
        "census_key_local": [
          28,
          28
        ],
        "census_key_deployed": [
          28,
          28
        ],
        "delta_h": 0,
        "delta_h_valid": true,
        "within_R": true,
        "verdict": "PASS"
      },
      "390": {
        "width": 390,
        "census_matched": false,
        "local": {
          "h_pagina": 9101,
          "paths_svg": 28,
          "list_parents": 28,
          "ports": 0,
          "ports_visto": 0,
          "frontend_version": "0.10.90",
          "api_health_version_from_page": "0.10.82",
          "script_src": "/assets/index-D7HHopYw.js",
          "css_href": "/assets/index-p4FzMslc.css"
        },
        "deployed": {
          "h_pagina": 10299,
          "paths_svg": 48,
          "list_parents": 48,
          "ports": 0,
          "ports_visto": 0,
          "frontend_version": "0.10.90",
          "api_health_version_from_page": "0.10.82",
          "script_src": "/assets/index-D7HHopYw.js",
          "css_href": "/assets/index-p4FzMslc.css"
        },
        "census_key_local": [
          28,
          28
        ],
        "census_key_deployed": [
          48,
          48
        ],
        "delta_h": 1198,
        "delta_h_valid": false,
        "within_R": false,
        "verdict": "INVALID_CENSUS"
      }
    },
    "plant": {
      "390": {
        "width": 390,
        "census_matched": true,
        "local": {
          "h_pagina": 5505,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 46,
          "ports_visto": 14,
          "frontend_version": "0.10.90",
          "api_health_version_from_page": "0.10.82",
          "script_src": "/assets/index-D7HHopYw.js",
          "css_href": "/assets/index-p4FzMslc.css"
        },
        "deployed": {
          "h_pagina": 5505,
          "paths_svg": 0,
          "list_parents": 0,
          "ports": 46,
          "ports_visto": 14,
          "frontend_version": "0.10.90",
          "api_health_version_from_page": "0.10.82",
          "script_src": "/assets/index-D7HHopYw.js",
          "css_href": "/assets/index-p4FzMslc.css"
        },
        "census_key_local": [
          46,
          14
        ],
        "census_key_deployed": [
          46,
          14
        ],
        "delta_h": 0,
        "delta_h_valid": true,
        "within_R": true,
        "verdict": "PASS"
      }
    }
  }
}
```

G5: commit + push `feature/obs-currency` (segue).
G6: nessuno script one-shot residuo obbligatorio; harness permanenti riusati.

---
Artefatti hash (locale):
- `docs/obs-o21-B0-g4-reconcile.json` sha256=`665051be6953b4396e844dcd167e88cd0df9b8610145ff75178292c82a637db4` bytes=1792 wc_l=77
- `docs/obs-o21-B0-oggi-height.json` sha256=`03c5d6f08276cd2685cdcd71069e05732fa4362ef9cf2a152eda7df9b624fa33` bytes=1608 wc_l=49
- `docs/obs-o21-G3.json` sha256=`005813e6fc0545ac9dba0d5f66213fa966e6cb01c9dfeb9d12ec43b76e412f2a` bytes=568 wc_l=19
- `docs/obs-o21-G4.json` sha256=`44d9e318f70473a2f82d32959ef0dff036bb161c746677e831fb1e8bbc779d50` bytes=5045 wc_l=174
- `docs/obs-o21-M-post-D.json` sha256=`2c738a05d7a4b38d083f71ff99f48e7fb25fc4a8066b05ac5f650baa719b6f0f` bytes=1225231 wc_l=33691
- `docs/obs-o21-M-pre-D.digest.json` sha256=`2417328a0356ffe99aee09071911b8fdd09662537a19dda5bcb5df381aa6625b` bytes=6825 wc_l=255
- `docs/obs-o21-M-pre-D.json` sha256=`0076029e44a45f00a9c52e5dc21984b86bf509ede553f3bd11d68b054f43ec33` bytes=1257821 wc_l=34860
- `docs/obs-o21-V1V2.json` sha256=`a5e78b3335df6fa9c42b87587298c2b92145240f9faa0ddf5e6a108cf108067d` bytes=15183 wc_l=610
- `docs/obs-o21-V4-heights.json` sha256=`1ca30e4d5bc00030d70200c433e17e1a8ecd31f5d4f14a1909d521ffc26d6d2a` bytes=29802 wc_l=1032
- `docs/obs-o21-V5-oggi-height.json` sha256=`6e4ed63c9aaeb1e3650540f084a14a6d00cd68df0902ee71ae5aa1c778e3229f` bytes=1618 wc_l=49
- `docs/obs-o21-V6-gates.txt` sha256=`7a2e5f93a363d8bd4efe5403620190e41ea74ef31f8f9664397e68136c5f1d8e` bytes=8571 wc_l=126
- `docs/obs-o21-V7-captures.json` sha256=`f81466abaaa5ef475452c3c78910f763a3f79e0541adfb150f67b86a0aadae7e` bytes=8567 wc_l=279
- `docs/obs-o21-drift.json` sha256=`9a65a4aae3c076cbe62a3be63df9572b3ea460d65b95693aa9c6b380a4d2351a` bytes=485 wc_l=22