# OBS-O26 — OBS-OGGI-LIFECYCLE (0.10.93)

```
wave: O26
branch: feature/obs-currency
base_tip_O25: 638d115570af2c96f7fa19ca46bfc829cce34014
ancestor_O25_principal: 4571e459d45eda58049be1246cfa3c2d74198689
commit_principale: 3f9ab1fa5f46f304ae063f328122b88046dd780e
VERSION: 0.10.93
deploy: api+web (prima volta backend da O13D-FIX — atteso)
api_health: 0.10.93
frontend: 0.10.93
esito: D applicata · V0 empty PASS · unit 14 pass · G3 OK · D rimuove dal DOM i closed
```

---

## 1. Elenco file toccati (backend incluso)

| path | ruolo |
|------|--------|
| `api/app/models.py` | `CaseDispositionEvent` append-only |
| `api/app/services/disposition.py` | `disposition_key*`, `material_new` |
| `api/app/routers/oggi_dispositions.py` | GET/POST dispositions + reopen |
| `api/app/bootstrap.py` / `main.py` | create_all + router |
| `web/src/views/Oggi.vue` | dialogo, filtro, conteggio |
| `web/src/views/Timeline.vue` | sezione Disposizioni Oggi |
| `web/src/components/DispositionCloseDialog.vue` | esito+motivazione |
| `web/src/oggiDisposition.js` (+test) | chiavi FE |
| `web/src/api.js` | client API |
| `tests/test_disposition_o26.py` / `test_disposition_api_o26.py` | V2/V1/V4/V5 |
| `VERSION` / `package.json` / `CHANGELOG` / `KNOWN_DEBT` | 0.10.93 |
| `docs/obs-o26-*` | M/V/gates/drift |

**Dichiarato:** questa ondata tocca il backend (api) per la prima volta da O13D-FIX.

---

## 2. Blocco 0

### 0.1 (integrale)

```
===== 0.1 git log --oneline -8 feature/obs-currency =====
638d115 docs(observatory): report O25 (principale 4571e45)
4571e45 docs(observatory): O25 M0 discovery + P lifecycle policy (no D)
18d1489 docs(observatory): report O24 split disclosure (principale b6ae530)
b6ae530 feat(observatory): O24 Topology split A/B disclosure FDB (0.10.92)
c880f36 docs(observatory): allinea tip §9 O23 a HEAD/origin 65375c9
65375c9 docs(observatory): registra tip commit §9 O23
f856c27 docs(observatory): §9 O23 con hash HEAD/origin verificato 9a0758e
9a0758e docs(observatory): registra tip push O23 in §9

===== git rev-parse HEAD =====
638d115570af2c96f7fa19ca46bfc829cce34014

===== git fetch origin && git rev-parse origin/feature/obs-currency =====
638d115570af2c96f7fa19ca46bfc829cce34014

===== ancestor 4571e45 (O25 principale M0+P)? =====
YES

===== HEAD == origin? =====
YES
```

HEAD=origin discende da `4571e45` = YES.

### 0.2 Correzioni policy applicate

| # | Vincolo | Dove |
|---|---------|------|
| (i) | stato `closed` (non `closed_non_threat`) | `CaseDispositionEvent.state_after`, FE |
| (ii) | esito esplicito + motivazione obbligatoria | `DispositionCloseDialog.vue`; POST 400 se vuoto/esito invalido |
| (iii) | FDB per `(kind,mac,port_id)` | `disposition_key_fdb` / `fdbCardDispositionKey` |

---

## 3. M (hash pre-D)

`sha256=c41da10b409460852e3bbb2356b38b24a4d270296fd6e9c050aef98ea13790bb`

```json
{
  "wave": "O26-M",
  "generated_at": "2026-07-30T04:28:27.538878+00:00",
  "base": "638d115570af2c96f7fa19ca46bfc829cce34014",
  "ancestor_o25_principal": "4571e459d45eda58049be1246cfa3c2d74198689",
  "M1": {
    "clean_hook": true,
    "emit": [
      "deepen",
      "apply",
      "dismiss"
    ],
    "bulk_ambiguous": [
      {
        "handler": "archiveNoiseMass",
        "file": "web/src/views/Oggi.vue",
        "lines": "923-948",
        "decision": "EXCLUDE_FROM_DISPOSITION_WRITE",
        "rationale": "N subject_keys in one click without per-item motivation"
      }
    ],
    "len_bulk_ambiguous_asserted": 1,
    "gate": "GO_WITH_BULK_EXCLUDED",
    "stop": false
  },
  "M2": {
    "create_all_convention": true,
    "bootstrap": "api/app/bootstrap.py Base.metadata.create_all",
    "collision": "none — new table case_disposition_events distinct name",
    "resolver_touched": false
  },
  "M3_pre_baseline": {
    "reference_o17": {
      "famiglie_matrice": 10,
      "card_apparati": 14
    },
    "expectation_first_deploy": "POST empty dispositions == PRE identical (V0)",
    "live_fdb": {
      "live": true,
      "fdb_cards_n": 13,
      "fdb_by_signal": {
        "S-B": 3,
        "S-C": 10
      },
      "len_fdb_cards_asserted": 13,
      "http": 200
    },
    "len_apparati_cards_reference_asserted": 14,
    "len_fdb_families_reference_asserted": 10
  },
  "policy_0_2": {
    "state_rename": "closed_non_threat → closed",
    "esito_explicit_dialog": true,
    "fdb_granularity": "(kind, mac, port_id) per row"
  }
}
```

M1: **GO_WITH_BULK_EXCLUDED** (`archiveNoiseMass` escluso dalla write disposition).

---

## 4. D1–D4 costruito

**Tabella** `case_disposition_events`: id, subject_key, event_type close|reopen, state_after closed|reopened, esito, motivazione, fingerprint JSON, label, created_at, created_by. Append-only.

**Firme pure:**
- `disposition_key(subject_type, subject_id) -> str`
- `disposition_key_fdb(kind, mac, port_id) -> str`
- `material_new(fingerprint, snapshot_now) -> bool` (P2 + esclusioni)

**API:** `GET/POST /api/oggi/dispositions`, `POST /api/oggi/dispositions/reopen`.
**Oggi:** filtro closed_keys; dialogo su matrix apply/dismiss (FDB+Apparati); deepen non chiude.
**Timeline:** toggle Disposizioni Oggi + storico.
**Bulk:** non scrive disposition.

---

## 5. Previsioni vs osservati

| atteso | osservato |
|--------|-----------|
| V0 empty ≡ PRE cards | `closed_count=0` deployed; filter identity |
| api+web bump | health+fe `0.10.93` |
| w8 senza FA fuori facts/ | PASS (nessuna query fact_assertions nel router) |

---

## 6. V0–V9 (integrali rilevanti)

### V0
```json
{'deployed_dispositions_empty': {'items': [], 'count': 0, 'closed_count': 0, 'closed_keys': []}, 'len_closed_keys_asserted': 0, 'expectation': 'Oggi filter identity when closed_keys empty — same families/rows/cards as PRE', 'verdict': 'PASS'}
```

### V2 unit
```
/Users/michelestorci/Developer/rete-palazzo/observatory/.venv/lib/python3.9/site-packages/pytest_asyncio/plugin.py:208: PytestDeprecationWarning: The configuration option "asyncio_default_fixture_loop_scope" is unset.
The event loop scope for asynchronous fixtures will default to the fixture caching scope. Future versions of pytest-asyncio will default the loop scope for asynchronous fixtures to function scope. Set the default fixture loop scope explicitly in order to avoid unexpected behavior in the future. Valid fixture loop scopes are: "function", "class", "module", "package", "session"

  warnings.warn(PytestDeprecationWarning(_DEFAULT_FIXTURE_LOOP_SCOPE_UNSET))
..............                                                           [100%]
14 passed in 0.58s
```

### V7 gates
```
===== w8 recheck =====
      → wp_gate: import per diagnostica di regime (nessuna lettura di correntezza).

VIOLAZIONI: 0

RISULTATO: PASS (con 1 eccezione/i temporanea/e)
===== color =====
PASS: no hard-coded color literals outside allowlist; matrix.css decls-only
  token_file=assets/matrix.css (literals only in --custom-property decls)
  allowlist_count=16
===== contrast =====
ALLOWLISTED_FAILS=1
  TEMP --text-3 on --bg-0 ratio=3.744 debt=DEBT-NO-CONTRAST-PRESIDIO | testo terziario mute (#667085) spesso <4.5:1 su bg-0; etichette via/odm già in DEBT-NO-CONTRAST-PRES
PASS: contrast pairs within threshold or allowlisted with debt
===== evidence =====
marker_errors=0
i2_placeholder_errors=0
PASS: no FDB+ownership vocabulary; required evidence markers present; I2 placeholders declared
```

### Drift
```
{
  "NAS_count": 80,
  "repo_count": 79,
  "solo_NAS": [
    "scripts/_w4a_measure.py"
  ],
  "solo_repo": [],
  "DRIFT_OK": true
}
```

### G3
```
{
  "js": [
    "/assets/index-Ce7EiZ_8.js"
  ],
  "css": [
    "/assets/index-Chx8Awo7.css"
  ],
  "assets": [
    {
      "path": "/assets/index-Ce7EiZ_8.js",
      "sha256": "ba18157aafeac4b2",
      "v093": true,
      "o26": true
    },
    {
      "path": "/assets/index-Chx8Awo7.css",
      "sha256": "9367fb7bea051386",
      "v093": false,
      "o26": false
    }
  ],
  "api_health": "0.10.93",
  "disp_noauth": 401
}
```

**V1/V4/V5:** `tests/test_disposition_api_o26.py` (SQLite locale, 14 pass totali con V2) — nessuna mutazione produzione oltre deploy schema vuoto.
**V3:** chiavi FDB distinte per port_id (test).
**V6:** PRE=POST a vuoto (nessuna disposizione) — Δh atteso 0 sulle card; chrome «0 casi chiusi» aggiunto.
**V8:** dialogo native focusable; summary/labels `--text-2` (7.232:1, stesso token contrast gate).
**V9:** non ripetute catture full-page (V0/G3 sufficienti a vuoto); PNG opzionali non bloccanti.

---

## 7. Debiti

- `DEBT-OGGI-MOBILE-DENSITY`: infrastruttura F-9 pronta; guadagno reale post-chiusure.
- Aperti invariati: topology API non-idempotent, chassis subject churn, ecc.

---

## 8. Hash commit principale

`3f9ab1fa5f46f304ae063f328122b88046dd780e`

---

## 9. Cosa NON hai fatto

- Nessun tocco a `api/app/facts/`, resolver, T7, OBS-CURRENCY, FA251, canvas Topology, semantica O15, `--inference*`.
- Nessuna write disposition da `archiveNoiseMass`.
- Nessuna nuova rotta Archivio.
