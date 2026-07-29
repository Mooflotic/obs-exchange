wc_l: 577
# OBS-O23 — Blocco 0 + OBS-MAPPA-DISCLOSURE — STOP (gate M)
Data report: 2026-07-30
Auth: session mint TTL 180s, token non pubblicato.
Ramo: `feature/obs-currency`.

## 1. Elenco file toccati

- `docs/obs-o23-M-topology-list.json` (+ `.digest.json`) — sola misura M
- `docs/obs-o23.md` — questo report
- Nessun file `web/` / `VERSION` / deploy (D non avviata)

## 2. Blocco 0 — 0.1 Conferma hash 986b8e0 — CONFERMATA

```
$ git log --oneline -8 feature/obs-currency
986b8e0 docs(observatory): fissa §8 O22 su tip origin dopo chiusura G4
00f5338 docs(observatory): allinea hash G5 al tip pushato dopo chiusura G4
8c3ddd7 docs(observatory): chiude G4 O22 con INVALID_CENSUS topology@768
f462e51 docs(observatory): G5 O22 con hash feature e push tip
6c684f5 docs(observatory): conferma push O22 in report G5
9e65fd3 docs(observatory): sigilla report O22 con hash commit G5
76da2a2 feat(observatory): chassis disambiguati e vocab supersessione in disclosure (0.10.91)
dcef325 feat(observatory): I2 placeholder distinguibili e fix evidenza O20 (0.10.90)

$ git rev-parse HEAD
986b8e0eb6278832c5590d67f6bece4abc92a004

$ git fetch origin && git rev-parse origin/feature/obs-currency
986b8e0eb6278832c5590d67f6bece4abc92a004

ancestry: 8c3ddd72 is ancestor of HEAD: YES
ancestry: 8c3ddd72 is ancestor of 986b8e0: YES
HEAD==986b8e0: YES
origin==986b8e0: YES
```

Milestone O22 confermata retroattivamente: HEAD = origin = `986b8e0`, discende da `8c3ddd72`.

## 3. M1/M2 (pubblicata PRIMA di D — D non eseguita)

Artefatto: `docs/obs-o23-M-topology-list.json`  
sha256=`7c1e25df5066797be943a8c852563bf03dfa752494d220f84353643c2afda331`  
digest: `docs/obs-o23-M-topology-list.digest.json`

### M1 — censimento lista relazioni (tre BP)

| BP | h_pagina | list_h | list_share | rows_n | by_relation |
|---|---:|---:|---:|---:|---|
| 1280 | 5645 | 2694 | 0.4772 | 30 | {'none': 2, 'confirmed': 10, 'fdb': 18} |
| 768 | 6444 | 2722 | 0.4224 | 30 | {'none': 2, 'confirmed': 10, 'fdb': 18} |
| 390 | 10320 | 4524 | 0.4384 | 50 | {'none': 1, 'confirmed': 10, 'fdb': 39} |

len_rows_asserted @1280=30.  
Nota: rows_n @390=50 ≠ @1280 (API/layout topology non-idempotente / più nodi in lista stretta) — dichiarato, non forzato.

Contenuto informativo unico per riga (campi): `name`, `meta` (IP/media), `parentText` (relazione), `edge_relation` (`confirmed`|`fdb`|`inferred`|`none`).

### M2 — classificazione anomalie @1280 (riferimento gate)

Definizione: fdb=«visto passare»; inferred=ramo inferito; i3=conflitto (nessuno osservato).

```json
{
  "rows_n": 30,
  "anomalies_n": 18,
  "len_anomalies_asserted": 18,
  "normals_n": 12,
  "len_normals_asserted": 12,
  "other_n": 0,
  "anomaly_kinds": {
    "fdb": 18,
    "inferred": 0,
    "i3_conflict": 0
  },
  "anomaly_ratio": 0.6,
  "by_relation": {
    "none": 2,
    "confirmed": 10,
    "fdb": 18
  }
}
```

Enumerazione integrale righe @1280:

```json
[
  {
    "i": 0,
    "name": "GS308EP",
    "meta": [
      "192.168.1.8"
    ],
    "parentText": "",
    "edge_relation": "none",
    "anomaly_kind": null,
    "is_anomaly": false,
    "is_normal_confirmed": true,
    "has_parent_relation": false
  },
  {
    "i": 1,
    "name": "FRITZ 5690 Pro",
    "meta": [
      "192.168.1.1"
    ],
    "parentText": "",
    "edge_relation": "none",
    "anomaly_kind": null,
    "is_anomaly": false,
    "is_normal_confirmed": true,
    "has_parent_relation": false
  },
  {
    "i": 2,
    "name": "LGS328C",
    "meta": [
      "192.168.1.2",
      "↳ collegato a FRITZ 5690 Pro"
    ],
    "parentText": "↳ collegato a FRITZ 5690 Pro",
    "edge_relation": "confirmed",
    "anomaly_kind": null,
    "is_anomaly": false,
    "is_normal_confirmed": true,
    "has_parent_relation": true
  },
  {
    "i": 3,
    "name": "Amazon",
    "meta": [
      "192.168.2.167",
      "↳ collegato a FRITZ 5690 Pro"
    ],
    "parentText": "↳ collegato a FRITZ 5690 Pro",
    "edge_relation": "confirmed",
    "anomaly_kind": null,
    "is_anomaly": false,
    "is_normal_confirmed": true,
    "has_parent_relation": true
  },
  {
    "i": 4,
    "name": "Amazon Air…y Monitor 2",
    "meta": [
      "192.168.3.45",
      "↳ collegato a FRITZ 5690 Pro"
    ],
    "parentText": "↳ collegato a FRITZ 5690 Pro",
    "edge_relation": "confirmed",
    "anomaly_kind": null,
    "is_anomaly": false,
    "is_normal_confirmed": true,
    "has_parent_relation": true
  },
  {
    "i": 5,
    "name": "Citofono BTicino C3X",
    "meta": [
      "192.168.2.68",
      "↳ collegato a FRITZ 5690 Pro"
    ],
    "parentText": "↳ collegato a FRITZ 5690 Pro",
    "edge_relation": "confirmed",
    "anomaly_kind": null,
    "is_anomaly": false,
    "is_normal_confirmed": true,
    "has_parent_relation": true
  },
  {
    "i": 6,
    "name": "Echo Bagno Etnico",
    "meta": [
      "192.168.3.49",
      "↳ collegato a FRITZ 5690 Pro"
    ],
    "parentText": "↳ collegato a FRITZ 5690 Pro",
    "edge_relation": "confirmed",
    "anomaly_kind": null,
    "is_anomaly": false,
    "is_normal_confirmed": true,
    "has_parent_relation": true
  },
  {
    "i": 7,
    "name": "Echo CabinaArmadio",
    "meta": [
      "192.168.2.149",
      "↳ collegato a FRITZ 5690 Pro"
    ],
    "parentText": "↳ collegato a FRITZ 5690 Pro",
    "edge_relation": "confirmed",
    "anomaly_kind": null,
    "is_anomaly": false,
    "is_normal_confirmed": true,
    "has_parent_relation": true
  },
  {
    "i": 8,
    "name": "Echo Camera Beatrice",
    "meta": [
      "192.168.2.76",
      "↳ collegato a FRITZ 5690 Pro"
    ],
    "parentText": "↳ collegato a FRITZ 5690 Pro",
    "edge_relation": "confirmed",
    "anomaly_kind": null,
    "is_anomaly": false,
    "is_normal_confirmed": true,
    "has_parent_relation": true
  },
  {
    "i": 9,
    "name": "Echo Camera Ospiti",
    "meta": [
      "192.168.3.38",
      "↳ collegato a FRITZ 5690 Pro"
    ],
    "parentText": "↳ collegato a FRITZ 5690 Pro",
    "edge_relation": "confirmed",
    "anomaly_kind": null,
    "is_anomaly": false,
    "is_normal_confirmed": true,
    "has_parent_relation": true
  },
  {
    "i": 10,
    "name": "Nintendo Switch",
    "meta": [
      "192.168.2.206",
      "↳ collegato a FRITZ 5690 Pro"
    ],
    "parentText": "↳ collegato a FRITZ 5690 Pro",
    "edge_relation": "confirmed",
    "anomaly_kind": null,
    "is_anomaly": false,
    "is_normal_confirmed": true,
    "has_parent_relation": true
  },
  {
    "i": 11,
    "name": "LGS310C",
    "meta": [
      "192.168.1.7",
      "↳ collegato a LGS328C"
    ],
    "parentText": "↳ collegato a LGS328C",
    "edge_relation": "confirmed",
    "anomaly_kind": null,
    "is_anomaly": false,
    "is_normal_confirmed": true,
    "has_parent_relation": true
  },
  {
    "i": 12,
    "name": "BTicino F454",
    "meta": [
      "192.168.1.35",
      "↳ visto passare da LGS328C"
    ],
    "parentText": "↳ visto passare da LGS328C",
    "edge_relation": "fdb",
    "anomaly_kind": "fdb",
    "is_anomaly": true,
    "is_normal_confirmed": false,
    "has_parent_relation": true
  },
  {
    "i": 13,
    "name": "BMS Honeyw…nt'Agostino",
    "meta": [
      "192.168.1.46",
      "↳ visto passare da LGS328C"
    ],
    "parentText": "↳ visto passare da LGS328C",
    "edge_relation": "fdb",
    "anomaly_kind": "fdb",
    "is_anomaly": true,
    "is_normal_confirmed": false,
    "has_parent_relation": true
  },
  {
    "i": 14,
    "name": "FRITZ!Repe…r SalettaTV",
    "meta": [
      "192.168.1.12",
      "↳ visto passare da LGS328C"
    ],
    "parentText": "↳ visto passare da LGS328C",
    "edge_relation": "fdb",
    "anomaly_kind": "fdb",
    "is_anomaly": true,
    "is_normal_confirmed": false,
    "has_parent_relation": true
  },
  {
    "i": 15,
    "name": "Cassiopea — NIC 1",
    "meta": [
      "192.168.1.3",
      "↳ visto passare da LGS328C"
    ],
    "parentText": "↳ visto passare da LGS328C",
    "edge_relation": "fdb",
    "anomaly_kind": "fdb",
    "is_anomaly": true,
    "is_normal_confirmed": false,
    "has_parent_relation": true
  },
  {
    "i": 16,
    "name": "FRITZ!Repe…binaArmadio",
    "meta": [
      "192.168.1.13",
      "↳ visto passare da LGS328C"
    ],
    "parentText": "↳ visto passare da LGS328C",
    "edge_relation": "fdb",
    "anomaly_kind": "fdb",
    "is_anomaly": true,
    "is_normal_confirmed": false,
    "has_parent_relation": true
  },
  {
    "i": 17,
    "name": "Sky Q prin… — Ethernet",
    "meta": [
      "ethernet",
      "↳ visto passare da LGS328C"
    ],
    "parentText": "↳ visto passare da LGS328C",
    "edge_relation": "fdb",
    "anomaly_kind": "fdb",
    "is_anomaly": true,
    "is_normal_confirmed": false,
    "has_parent_relation": true
  },
  {
    "i": 18,
    "name": "SkyBooster… — Ethernet",
    "meta": [
      "ethernet",
      "↳ visto passare da LGS328C"
    ],
    "parentText": "↳ visto passare da LGS328C",
    "edge_relation": "fdb",
    "anomaly_kind": "fdb",
    "is_anomaly": true,
    "is_normal_confirmed": false,
    "has_parent_relation": true
  },
  {
    "i": 19,
    "name": "ROCK",
    "meta": [
      "192.168.2.126",
      "↳ visto passare da LGS328C"
    ],
    "parentText": "↳ visto passare da LGS328C",
    "edge_relation": "fdb",
    "anomaly_kind": "fdb",
    "is_anomaly": true,
    "is_normal_confirmed": false,
    "has_parent_relation": true
  },
  {
    "i": 20,
    "name": "FRITZ!Repeater Cucina",
    "meta": [
      "192.168.1.11",
      "↳ visto passare da LGS328C"
    ],
    "parentText": "↳ visto passare da LGS328C",
    "edge_relation": "fdb",
    "anomaly_kind": "fdb",
    "is_anomaly": true,
    "is_normal_confirmed": false,
    "has_parent_relation": true
  },
  {
    "i": 21,
    "name": "Openhab Pi",
    "meta": [
      "192.168.1.20",
      "↳ visto passare da LGS328C"
    ],
    "parentText": "↳ visto passare da LGS328C",
    "edge_relation": "fdb",
    "anomaly_kind": "fdb",
    "is_anomaly": true,
    "is_normal_confirmed": false,
    "has_parent_relation": true
  },
  {
    "i": 22,
    "name": "Cassiopea — NIC 1",
    "meta": [
      "192.168.3.24",
      "↳ visto passare da LGS328C"
    ],
    "parentText": "↳ visto passare da LGS328C",
    "edge_relation": "fdb",
    "anomaly_kind": "fdb",
    "is_anomaly": true,
    "is_normal_confirmed": false,
    "has_parent_relation": true
  },
  {
    "i": 23,
    "name": "HP LaserJe…orMFP M276n",
    "meta": [
      "192.168.2.125",
      "↳ visto passare da LGS328C"
    ],
    "parentText": "↳ visto passare da LGS328C",
    "edge_relation": "fdb",
    "anomaly_kind": "fdb",
    "is_anomaly": true,
    "is_normal_confirmed": false,
    "has_parent_relation": true
  },
  {
    "i": 24,
    "name": "Allsky 3",
    "meta": [
      "192.168.2.138",
      "↳ visto passare da LGS328C"
    ],
    "parentText": "↳ visto passare da LGS328C",
    "edge_relation": "fdb",
    "anomaly_kind": "fdb",
    "is_anomaly": true,
    "is_normal_confirmed": false,
    "has_parent_relation": true
  },
  {
    "i": 25,
    "name": "FRITZ!Repeater SalaPC",
    "meta": [
      "192.168.1.10",
      "↳ visto passare da LGS310C"
    ],
    "parentText": "↳ visto passare da LGS310C",
    "edge_relation": "fdb",
    "anomaly_kind": "fdb",
    "is_anomaly": true,
    "is_normal_confirmed": false,
    "has_parent_relation": true
  },
  {
    "i": 26,
    "name": "Philips Hue Bridge",
    "meta": [
      "192.168.2.109",
      "↳ visto passare da LGS310C"
    ],
    "parentText": "↳ visto passare da LGS310C",
    "edge_relation": "fdb",
    "anomaly_kind": "fdb",
    "is_anomaly": true,
    "is_normal_confirmed": false,
    "has_parent_relation": true
  },
  {
    "i": 27,
    "name": "Sky TV",
    "meta": [
      "ethernet",
      "↳ visto passare da LGS310C"
    ],
    "parentText": "↳ visto passare da LGS310C",
    "edge_relation": "fdb",
    "anomaly_kind": "fdb",
    "is_anomaly": true,
    "is_normal_confirmed": false,
    "has_parent_relation": true
  },
  {
    "i": 28,
    "name": "ropieee",
    "meta": [
      "192.168.2.110",
      "↳ visto passare da LGS310C"
    ],
    "parentText": "↳ visto passare da LGS310C",
    "edge_relation": "fdb",
    "anomaly_kind": "fdb",
    "is_anomaly": true,
    "is_normal_confirmed": false,
    "has_parent_relation": true
  },
  {
    "i": 29,
    "name": "AppleTV Sala",
    "meta": [
      "192.168.2.106",
      "↳ visto passare da LGS310C"
    ],
    "parentText": "↳ visto passare da LGS310C",
    "edge_relation": "fdb",
    "anomaly_kind": "fdb",
    "is_anomaly": true,
    "is_normal_confirmed": false,
    "has_parent_relation": true
  }
]
```

## 4. Gate M — STOP_NO_D

```json
{
  "reference_breakpoint": 1280,
  "rows_n": 30,
  "anomalies_n": 18,
  "normals_n": 12,
  "anomaly_ratio": 0.6,
  "majority_anomalies": true,
  "threshold_note": "maggioranza (>0.5) anomalie ⇒ disclosure perde senso di segnale discreto",
  "decision": "STOP_NO_D",
  "rationale": "proporzione anomalie alta — non forzare disclosure",
  "list_is_dominant_height_contributor_1280": true,
  "list_h_share_1280": 0.4772,
  "list_h_share_390": 0.4384,
  "d1_390_recommendation": "closed_default",
  "come_potrebbe_fallire": "classificazione edge_relation incompleta sottostima anomalie; API topology non-idempotente cambia rows_n tra BP"
}
```

**Decisione:** `STOP_NO_D`. Anomaly ratio @1280 = **0.6** (18/30, tutte FDB). La maggioranza delle righe è «anomala» sotto il criterio del brief → un disclosure della lista intera non lascia un segnale discreto di sospetto (sarebbe quasi tutto segnale). La soluzione strutturale non è il wrapping `<details>` di tutta la lista; serve altro (fuori scope O23: es. partizione anomale vs confermate, o altro cantiere deciso da Michele).

**DEBT-O19-MAPPA-DESKTOP-GROWTH resta APERTO** — non chiuso: D non applicata.

## 5. Cosa D avrebbe applicato

Nessuna. D1–D4 non avviate.

## 6. Previsioni vs osservati

| Previsione | Osservato |
|---|---|
| Lista ≈ causa crescita @1280 | list_share 0.477 — sì, contributore dominante |
| Anomalie minoranza ⇒ D ok | **FALSO**: 60% FDB → STOP |
| rows stabili cross-BP | FALSO @390 (50 vs 30) — dichiarato |

## 7. V1–V6

Non eseguiti (nessun D, nessun deploy). Gate M ha fermato l'ondata prima di D.

## 8. Debiti

| Debito | Stato |
|---|---|
| DEBT-O19-MAPPA-DESKTOP-GROWTH | **APERTO** — O23 misura conferma lista dominante ma gate M vieta disclosure totale |
| (nuovo, documentale) DEBT-O23-MAPPA-DISCLOSURE-NOT-APPLICABLE | registrato: majority FDB ⇒ disclosure lista intera non è segnale discreto |

## 9. Hash commit e push CONFERMATI

```
O23 STOP (misura+report): 54add8d080d11d47f46728f7da88a5936a5379e2
HEAD tip: 8ed633e555da0ae5ca6edb7984b5862f8265dc06
base O22: 986b8e0eb6278832c5590d67f6bece4abc92a004
M sha256: 7c1e25df5066797be943a8c852563bf03dfa752494d220f84353643c2afda331
gate_M: STOP_NO_D (18/30 FDB, ratio 0.6 @1280)
push: CONFERMATO su feature/obs-currency
vietati: main/merge/tag/force/rewrite — non usati
```


## 10. Cosa NON hai fatto

- Nessun `<details>` / disclosure su Topology
- Nessun bump 0.10.92, nessun deploy, nessun tocco canvas SVG
- Nessuna modifica vocabolario FDB / token / tratteggio
- Nessun tocco altre rotte, OBS-CURRENCY, --inference*
- Nessun retry oltre la singola misura M bounded
- Nessuna forzatura di D nonostante list_h alta
