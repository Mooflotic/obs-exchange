# OBS-O19 — OBS-MAPPA — 0.10.88

Base: `af98330` (post-O18). Ramo: `feature/obs-currency`.
Auth catture: session mint TTL 180s (fonte harness 36s×5), token non pubblicato.

## 1. File toccati

- `web/src/views/Topology.vue` — D1/D2/D4 (tratto, FDB≠ownership, lista DOM, h2, tab)
- `web/src/App.vue` — Schermo intero in sidebar-foot, non fixed
- `scripts/topology_audit_measure.py` — Fase M (nuovo permanente)
- `scripts/topology_verify_ab.py` — Fase V A/B (nuovo permanente)
- `scripts/oggi_nav_measure.py` — generalizzato `OBS_ROUTE`
- `docs/KNOWN_DEBT.md`, `CHANGELOG.md`, `VERSION`, `web/package.json`
- artefatti: `docs/obs-o19-*.json`, `docs/_o19_gate_*.txt`, questo report

## 2. Blocco 0

### 0.1 CSS deploy 0.10.87 — PASS
Dato: `docs/obs-o19-B0-css-deploy.json`
```
{
  "url": "http://192.168.1.3:8080/oggi",
  "auth_provenance": "catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato",
  "measure": {
    "text": "APPROFONDISCI",
    "fontSize": "10.88px",
    "color": "rgb(152, 162, 179)",
    "bg_behind": "rgb(15, 19, 25)",
    "bg_from": "workspace",
    "contrast_ratio": 7.232072185421649,
    "odm_head_display": "grid",
    "n_visible_heads": 30,
    "marker_o18": "obs-o18-marker",
    "version_meta": null
  },
  "wcag": "WCAG 2.2 SC 1.4.3 Contrast (Minimum) AA — testo normale ≥4.5:1",
  "ok": true,
  "css_token_served": {
    "--odm-via-label": "var(--text-2)",
    "--text-2": "#98a2b3"
  }
}
```
`css=None` = FAIL da O19 in poi. Contrasto `.odm-head` deployed ≥4.5:1.

### 0.2 DEBT-O17-PROTOTYPE-UNEXPLAINED — CHIUSO con misura
Dato: `docs/obs-o19-B0-pma.json` — PM-A 4-col, `ev_w` 106.9 vs HEAD 366, `mean_row_h` 238.8 vs 146.2. Causa: wrap evidenza in colonna stretta (brief chiedeva full-width).

### 0.3 Attribuzione contrasto + DEBT-NO-CONTRAST-PRESIDIO
Violazione AA 3.744:1 su `.odm-cell-col` = **O15**, non O17. Attribuzione errata originata dal **revisore** (prompt O18); dati in mano a Cursor non usati. Aperto `DEBT-NO-CONTRAST-PRESIDIO` (gate literal ≠ contrasto).

### 0.4 PNG de-tautologizzato + DEBT-SCRUB-ALTERS-LAYOUT
Criterio: riportare h_pre_scrub, h_post_scrub, h_PNG, h_pagina_report. Scarti O18 vs pre_scrub: 712@390, 455@768, 114@1280. PNG non è documento fedele dell'altezza.

### 0.5–0.6 Censimento
Ogni cattura/breakpoint; PRE=POST identico o misura invalida; un censimento per blocco.

### 0.7 Δ768 19020 vs 18808
Dato: `docs/obs-o19-B0-768.json`
```
{
  "wave": "O19",
  "point": "0.7",
  "question": "h_pre_scrub@768=19020 (O18 §10/captures) vs h_pagina post V5@768=18808 — Δ212 stessa sessione?",
  "data_same_block": {
    "captures.768.h_pagina_pre_scrub": 19020,
    "captures.768.h_pagina_post_scrub": 18565,
    "captures.768.png_h": 18565,
    "heights.768.post.h_pagina": 18808,
    "heights.768.pre.h_pagina": 18639,
    "delta_pre_scrub_minus_V5_post": 212,
    "delta_V5_post_minus_post_scrub": 243
  },
  "verdict": "causa_non_determinata_al_100_senza_riproduzione",
  "ipotesi_dominante": "due misure su navigazioni distinte nella stessa sessione O18 (V5 heights vs pipeline cattura): settle/timing diverso; scrub non spiega il 212 (scrub porta 19020→18565). O18 non allegava censimento @768 alle catture, quindi non si può escludere drift di popolazione.",
  "come_potrebbe_fallire_questa_ipotesi": "se V5 e capture usassero lo stesso page object senza reload e lo stesso istante, Δ212 resterebbe inspiegato — i log O18 non lo provano."
}
```

### 0.8 Conservazione — PASS (14=14)
Dato: `docs/obs-o19-B0-conservation.json` — con `include_historical=true&all_proposals=true`. Falso allarme 9 vs 14 = endpoint sbagliato in O18.
```
{
  "auth_provenance": "catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato",
  "assets_endpoint": "/api/assets?include_historical=true&all_proposals=true (stesso di Oggi.load)",
  "false_alarm_O18": {
    "note": "O18 §0.8 e V9 usarono /api/assets senza include_historical → 118 asset, 5 chassis esclusi (members mancanti), chassis_cards=9 vs UI 14",
    "plain_assets_n": 118,
    "full_assets_n": 151
  },
  "surfaces": {
    "chassis_cards": 14,
    "triage_rows": 0,
    "noise_proposal_ids": 0,
    "chassis_groups_raw": 14,
    "assets_n": 151
  },
  "queueConservationCheck": {
    "missing": [],
    "duplicated": []
  },
  "UI_DOM_names_ordered": [
    "Echo Cucina",
    "LGS328C → Switch Linksys",
    "SkyBooster2 BIBLIO — Ethernet",
    "Sky",
    "Sky",
    "Cassiopea — NIC 1",
    "Allsky 3",
    "Kraken",
    "Echo Salone",
    "Echo Camera Beatrice",
    "Hub Tapo H100",
    "ROCK",
    "Sky TV",
    "LGS310C"
  ],
  "buildChassisNameCards_enum": [
    {
      "chassis_id": 20,
      "key": "chassis-name-20",
      "display_name": "Echo Cucina",
      "member_asset_ids": [
        55,
        141
      ]
    },
    {
      "chassis_id": 23,
      "key": "chassis-name-23",
      "display_name": "LGS328C",
      "member_asset_ids": [
        2,
        109,
        147,
        151
      ]
    },
    {
      "chassis_id": 28,
      "key": "chassis-name-28",
      "display_name": "SkyBooster2 BIBLIO — Ethernet",
      "member_asset_ids": [
        10,
        11,
        138
      ]
    },
    {
      "chassis_id": 31,
      "key": "chassis-name-31",
      "display_name": "Sky",
      "member_asset_ids": [
        61,
        137
      ]
    },
    {
      "chassis_id": 33,
      "key": "chassis-name-33",
      "display_name": "Sky",
      "member_asset_ids": [
        43,
        136,
        149
      ]
    },
    {
      "chassis_id": 1,
      "key": "chassis-name-1",
      "display_name": "Cassiopea — NIC 1",

```

### 0.9 V1 navigazione
`only_post_navigation` obbligatorio; normalizzazioni = limiti del test.

### 0.10 Debiti aperti (non risolti in O19)
- `DEBT-O18-HEADING-UNIQUENESS` (revisore)
- `DEBT-O18-FIELD-NAME-LIES`
- registrato h1 «Oggi ?» / «Topologia ?»

## 3–7. Fase M (pre-D)

Partizione POST-stabile @390 residuo 1.27% ≤3%. Censimento: nodes=155 edges=50 fritz=True.

Crescita 390 vs 1280 (PRE list hidden @1280): dominante **topology-list** (~4500px) + **unresolved** più alto su mobile. Canvas `max-height` viewport limita h@1280.

**M2:** SVG `.topology-edges` `aria-hidden=true` — archi solo-canvas. Equivalente DOM: lista relazioni (ora sempre `display:block`). Scrub: `node_labels_changed=true`; SVG text default vuoti → PNG pubblicabili solo post-scrub.

**M3 PRE:** stroke uniforme `var(--ok)` — FAIL I1 → priorità D1.
**M4 PRE:** 39 archi FDB + «collegato a» — FAIL FDB≠identità → D1.
**M5 PRE:** 1 salto h1→h4; tab divergences (poi risolte in D2).

## 8. Fase P

Non aperta per riduzione h@390: M1 individuava list+unresolved, ma priorità gate = M3+M4. Dopo D, Δh@390 = **+160** (leggenda/testi relazione nominati). Nessun candidato layout applicato.

## 9. Fase D — applicato

| id | cosa | perché |
|----|------|--------|
| D1 | `edge-confirmed/fdb/inferred` stroke-dasharray; legenda a tratto; «visto passare» / ramo inferito | I1 + WCAG 2.2 SC 1.4.1; FDB≠ownership |
| D2 | h2 livelli; canvas tabindex=-1; list sort by y; hidden-zone/branch order:3; Schermo in sidebar static | M5 tab/heading |
| D4 | `.topology-list { display:block }` sempre | I2: testo unico non display:none |
| — | P height candidates | non applicati |
| — | /oggi /inventory /… | vietati |

## 10. Previsioni vs osservati

| id | previsto | osservato | causa dominante |
|----|----------|-----------|-----------------|
| P-h390 | ≈ stabile o +legend | Δ=+160 | testi legenda + frasi relazione |
| P-h1280 | +lista (~4.5k) | Δ=+4421 | lista sempre visibile (D4) |
| V3 | dash FDB≠confirmed | True, dash `7px, 5px` vs `none` | D1 |
| V4 | 0 «collegato a» su FDB | visto=39, lies=[] | D1 |
| V7 jumps | 0 | 0 | h2 |
| V7 tab | 0 in main | 0 | D2 |

## 11. V1–V8

Censimento identico all widths (retry su drift 29↔50).
- V1: diff archi/nodi vuoto, len asseriti in `obs-o19-V.json`
- V2: intentional_re su testi FDB/legenda; nav in bucket separato
- V3: rel counts fdb/confirmed; secondo canale = dasharray
- V4: lies=[]
- V5: hidden=[]
- V6: tratto non-text ≥3:1 via `--ok` su bg (stesso token PRE); `--inference-edge` escluso. Testo etichette introdotte: `--text-*` / muted esistenti
- V7: jumps=0; tabdiv in-main=0 (shell aside→main escluso come debito chrome)
- V8: altezze sopra; crescita @1280 nominata D4

## 12. Gate V9 — OUTPUT INTEGRALE

### w8_currency_gate.py
```
== W8 CURRENCY GATE (indurito, W8-fix2) ==
root: /Users/michelestorci/Developer/rete-palazzo/observatory
sentinelle: simbolo ORM 'FactAssertion' · tabella grezza 'fact_assertions' in chiamata SQL (text/execute) · COMBO (fact-token FactAssertion|fact_assertions|fact_key) + valore di stato quotato 'current'
scope: api/**, scripts/**, collector/**
esclusioni:
  - api/app/facts/**  (il resolver È la fonte della correntezza)
  - scripts/w8_currency_gate.py  (contiene le sentinelle/fact_key come dato)
  - scripts/w8_g8_equivalence.py  (contiene le sentinelle/fact_key come dato)
file scansionati: 211
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

```

### grep specificity
```
(vuoto — nessun match)

```

### color_literal_gate.py
```
PASS: no hard-coded color literals outside allowlist; matrix.css decls-only
  token_file=assets/matrix.css (literals only in --custom-property decls)
  allowlist_count=16

```

### color_literal_gate.py --self-test
```
SELFTEST vue inject detected: (2, '#ff00aa', '.x { color: #ff00aa; /* O13D_COLOR_GATE_INJECT */ }')
SELFTEST matrix rule inject detected: (955, '#ff00aa', '.o14fix-gate-inject { color: #ff00aa; /* O14FIX_COLOR_GATE_INJECT */ }')
SELFTEST PASS: inject fails (vue+matrix rule), remove passes

```

### queueConservationCheck
Vedi Blocco 0.8: UI Apparati 14, check 14, missing=[], duplicated=[] con assets `include_historical=true&all_proposals=true`. Cardinalità 14.

### Drift repo↔NAS (insiemi)
```
solo-NAS  = { scripts/_w4a_measure.py }
solo-repo = {
  scripts/oggi_density_partition_measure.py,
  scripts/oggi_density_prototype_measure.py,
  scripts/oggi_density_verify_ab.py,
  scripts/oggi_nav_measure.py,
  scripts/oggi_nav_verify_ab.py,
  scripts/o18_block0_measure.py,
  scripts/topology_audit_measure.py,
  scripts/topology_verify_ab.py
}
```
(Verifica NAS da eseguire sul terminale Cassiopea se la lista locale diverge.)

## 13. Catture G4 (deployed)

Auth: catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato.
PNG non è documento fedele dell'altezza (scrub altera layout). Page.captureScreenshot dsf=1.
R_pagina=320 (come può fallire: |Δ| > R con censimento identico e senza causa nominata → FAIL).

Artefatti: `docs/obs-o19-topology-{1280,768,390}.png`, `docs/obs-o19-G4.json`.
Script: `scripts/topology_g4_capture.py`.

```
{
  "wave": "O19-G4",
  "base": "http://192.168.1.3:8080",
  "auth_provenance": "catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato",
  "R_pagina": 320,
  "png_not_faithful_height": true,
  "captures": {
    "1280": {
      "file": "obs-o19-topology-1280.png",
      "png_w": 1280,
      "png_h": 7216,
      "h_pre_scrub": 7101,
      "h_post_scrub": 7216,
      "h_PNG": 7216,
      "h_pagina_report": 7101,
      "abs_png_minus_pre": 115,
      "abs_png_minus_post": 0,
      "census": {
        "nodes_n": 155,
        "edges_n": 48,
        "fritz_present": true,
        "sources": [
          "manual",
          "LLDP",
          "FDB",
          "radio AP"
        ],
        "kinds": [
          "ethernet",
          "wifi",
          "inferred_branch"
        ],
        "fdb_n": 38,
        "list_display": "block",
        "visto_n": 38,
        "edge_fdb_paths": 38,
        "paths_n": 47
      },
      "note": "PNG non è documento fedele di h_pagina (scrub altera layout)"
    },
    "768": {
      "file": "obs-o19-topology-768.png",
      "png_w": 768,
      "png_h": 7930,
      "h_pre_scrub": 7819,
      "h_post_scrub": 7930,
      "h_PNG": 7930,
      "h_pagina_report": 7819,
      "abs_png_minus_pre": 111,
      "abs_png_minus_post": 0,
      "census": {
        "nodes_n": 155,
        "edges_n": 48,
        "fritz_present": true,
        "sources": [
          "manual",
          "LLDP",
          "FDB",
          "radio AP"
        ],
        "kinds": [
          "ethernet",
          "wifi",
          "inferred_branch"
        ],
        "fdb_n": 38,
        "list_display": "block",
        "visto_n": 38,
        "edge_fdb_paths": 38,
        "paths_n": 47
      },
      "note": "PNG non è documento fedele di h_pagina (scrub altera layout)"
    },
    "390": {
      "file": "obs-o19-topology-390.png",
      "png_w": 390,
      "png_h": 10199,
      "h_pre_scrub": 10248,
      "h_post_scrub": 10199,
      "h_PNG": 10199,
      "h_pagina_report": 10248,
      "abs_png_minus_pre": 49,
      "abs_png_minus_post": 0,
      "census": {
        "nodes_n": 155,
        "edges_n": 48,
        "fritz_present": true,
        "sources": [
          "manual",
          "LLDP",
          "FDB",
          "radio AP"
        ],
        "kinds": [
          "ethernet",
          "wifi",
          "inferred_branch"
        ],
        "fdb_n": 38,
        "list_display": "block",
        "visto_n": 38,
        "edge_fdb_paths": 38,
        "paths_n": 47
      },
      "note": "PNG non è documento fedele di h_pagina (scrub altera layout)"
    }
  },
  "reconcile": {
    "1280": {
      "h_post_local": 7199,
      "h_deployed_pre_scrub": 7101,
      "delta": -98,
      "R_pagina": 320,
      "ok": true,
      "census": {
        "nodes_n": 155,
        "edges_n": 48,
        "fritz_present": true,
        "sources": [
          "manual",
          "LLDP",
          "FDB",
          "radio AP"
        ],
        "kinds": [
          "ethernet",
          "wifi",
          "inferred_branch"
        ],
        "fdb_n": 38,
        "list_display": "block",
        "visto_n": 38,
        "edge_fdb_paths": 38,
        "paths_n": 47
      }
    },
    "768": {
      "h_post_local": 7838,
      "h_deployed_pre_scrub": 7819,
      "delta": -19,
      "R_pagina": 320,
      "ok": true,
      "census": {
        "nodes_n": 155,
        "edges_n": 48,
        "fritz_present": true,
        "sources": [
          "manual",
          "LLDP",
          "FDB",
          "radio AP"
        ],
        "kinds": [
          "ethernet",
          "wifi",
          "inferred_branch"
        ],
        "fdb_n": 38,
        "list_display": "block",
        "visto_n": 38,
        "edge_fdb_paths": 38,
        "paths_n": 47
      }
    },
    "390": {
      "h_post_local": 10284,
      "h_deployed_pre_scrub": 10248,
      "delta": -36,
      "R_pagina": 320,
      "ok": true,
      "census": {
        "nodes_n": 155,
        "edges_n": 48,
        "fritz_present": true,
        "sources": [
          "manual",
          "LLDP",
          "FDB",
          "radio AP"
        ],
        "kinds": [
          "ethernet",
          "wifi",
          "inferred_branch"
        ],
        "fdb_n": 38,
        "list_display": "block",
        "visto_n": 38,
        "edge_fdb_paths": 38,
        "paths_n": 47
      }
    }
  },
  "verdict": "PASS",
  "png_assert_pair_1280_768": {
    "rc": 0,
    "out": "obs-o19-topology-1280.png: 1280x7216 sha256=52b9568f6a1ac81b841d2bf90fe6b2f7f0e7a423b8a4d7a7c2d1f9b6ffa75960\nobs-o19-topology-768.png: 768x7930 sha256=c2b2ddd96808d8adf01529b8d7663798258d637c9afc0b613b3e3c44456fa930\nPASS pair distinct widths"
  },
  "png_assert_pair_1280_390": {
    "rc": 0,
    "out": "obs-o19-topology-1280.png: 1280x7216 sha256=52b9568f6a1ac81b841d2bf90fe6b2f7f0e7a423b8a4d7a7c2d1f9b6ffa75960\nobs-o19-topology-390.png: 390x10199 sha256=9e59930c20b3199fa81c0bac632542eea0f9737738d7e7aa49a14007e6b145e4\nPASS pair distinct widths"
  }
}
```

## 14. Deploy G3 — PASS

`./scripts/deploy.sh web` → ok. Indice + ogni asset JS/CSS scaricati (css=None = FAIL).

```
{
  "base": "http://192.168.1.3:8080",
  "js_refs": [
    "/assets/index-C6Ud7we9.js"
  ],
  "css_refs": [
    "/assets/index-CuofypE0.css"
  ],
  "css_none_is_fail": true,
  "assets": {
    "/assets/index-C6Ud7we9.js": {
      "bytes": 467747,
      "sha256": "5db92b511e081b84a9b1070ae7f69431ba14ea8dba466888b15490b036197a1e",
      "has_0_10_88": true,
      "has_edge_fdb": true,
      "has_visto_passare": true
    },
    "/assets/index-CuofypE0.css": {
      "bytes": 143977,
      "sha256": "5c28c06cbc7d42d9fb73e4643f659ac5a47c6e439a0b330a2c301db18731c6fe",
      "has_0_10_88": false,
      "has_edge_fdb": true,
      "has_visto_passare": false
    }
  },
  "markers": {
    "0.10.88": true,
    "edge-fdb": true,
    "visto passare": true
  },
  "verdict": "PASS"
}
```

Marker nel bundle JS: `0.10.88`, `edge-fdb`, `visto passare`. CSS: `edge-fdb`.

## 15. Debiti

| debito | stato | attribuzione |
|--------|-------|--------------|
| DEBT-O17-PROTOTYPE-UNEXPLAINED | CHIUSO O19 | misura Cursor |
| DEBT-NO-CONTRAST-PRESIDIO | APERTO | disciplina |
| DEBT-SCRUB-ALTERS-LAYOUT | APERTO | harness |
| DEBT-O18-HEADING-UNIQUENESS | APERTO | revisore |
| DEBT-O18-FIELD-NAME-LIES | APERTO | naming O18 |
| --inference-edge 2.609:1 | invariato | preesistente |

## 16. Cosa NON fatto
- Gate contrasto sito-wide (vietato O19)
- P prototipi densità @390 (priorità semantica; Δh390 già +160)
- Equivalenti DOM aggiuntivi oltre lista (lista copre relazioni)
- Toccare /oggi, inventory, gs308, monitoring, dossier, T7, FA251, `_w4a`, `--inference-edge`, /ai
- Catture topology non ancora ricatturate sul deployed (G4 dopo deploy utente)
