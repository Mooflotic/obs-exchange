# OBS-O24 — OBS-MAPPA-SPLIT-DISCLOSURE (0.10.92)

```
wave: O24
branch: feature/obs-currency
base_dichiarata_O23: c880f36f68852a15a8a737abb2da19aa0d375d14
VERSION: 0.10.92
commit_principale: b6ae53084ce8485741950d9c0dbbb6774297ca4f
nota_0.2: il commit di sola pubblicazione di questo report NON può autocertificarsi (docs/PROCESS_NOTES.md)
api_health_observed: 0.10.82 (web-only deploy; coerente)
frontend_deployed: 0.10.92 (bundle index-Bdnrv2si.js)
auth_provenance: session mint TTL 180s, token non pubblicato
esito: D applicata · V5/A11y/drift verdi · V4 PASS_REDUCTION@768/390 · INVALID_CENSUS@1280 dichiarato · G3/G4 PASS
```

---

## 1. Elenco file toccati

| path | ruolo |
|------|--------|
| `web/src/views/Topology.vue` | split A/B, `<details>` FDB, marker `data-o24` |
| `scripts/evidence_gate.py` | marker O24 `data-o24="list-split"` |
| `VERSION` / `web/package.json` / `CHANGELOG.md` | bump 0.10.92 |
| `docs/PROCESS_NOTES.md` | regola permanente hash report (0.2) |
| `docs/KNOWN_DEBT.md` | DEBT-O23-ANOMALY…; chiusura MAPPA-GROWTH + DISCLOSURE-NOT-APPLICABLE |
| `docs/obs-o24-*.json|txt` | M/V5/A11y/drift/V/G3/G4 |
| `docs/o24-captures/*` | PNG V6 + G4 |

---

## 2. Blocco 0

### 0.1 Conferma hash finale O23 (integrale)

```
===== 0.1 git log --oneline -8 feature/obs-currency =====
c880f36 docs(observatory): allinea tip §9 O23 a HEAD/origin 65375c9
65375c9 docs(observatory): registra tip commit §9 O23
f856c27 docs(observatory): §9 O23 con hash HEAD/origin verificato 9a0758e
9a0758e docs(observatory): registra tip push O23 in §9
8ed633e docs(observatory): §9 O23 con tip HEAD esplicito
4f2d7a9 docs(observatory): completa §9 hash O23 STOP
8fec661 docs(observatory): conferma push hash O23 STOP in report G5
54add8d docs(observatory): O23 STOP — gate M majority FDB su lista Topology

===== git rev-parse HEAD =====
c880f36f68852a15a8a737abb2da19aa0d375d14

===== git rev-parse origin/feature/obs-currency =====
c880f36f68852a15a8a737abb2da19aa0d375d14

===== ancestor 986b8e0? =====
YES
```

**Verdetto 0.1:** HEAD = origin = `c880f36f68852a15a8a737abb2da19aa0d375d14`; antenato `986b8e0` (O22) = YES. GATE BLOCCO 0 PASS.

### 0.2 Regola permanente formalizzata

Scritta una sola volta in `docs/PROCESS_NOTES.md`:

```
# Note di processo (permanenti)

Regole operative accettate e non da ri-litigare ogni ondata. Non sono debiti aperti.

## Hash del report ≠ hash del commit che lo pubblica

Un report **non può** contenere l’hash del commit che lo pubblica: l’hash dipende dal
contenuto del tree, e il contenuto dipenderebbe dall’hash — impossibilità strutturale di git.

**Metodo corretto (da O21 in poi):** ogni ondata, nel Blocco 0.1, conferma con `git log` /
`git rev-parse` dal vivo l’hash finale **reale** dell’ondata precedente. Il lag di un’ondata
è **permanente e accettato**. Non va «risolto» con amend ricorsivi, tip auto-referenziali,
né registrato di nuovo come debito a ogni ondata.

Nel report finale (G5) si pubblica l’hash del commit **principale** (codice/D o misura+STOP),
con nota esplicita a questa regola per l’eventuale commit successivo di sola pubblicazione
documentale.
```

### 0.3 Debito revisore

`DEBT-O23-ANOMALY-DEFINITION-FLAWED` registrato in KNOWN_DEBT (attribuito al REVISORE): criterio «FDB = anomalia» del gate M O23 confondeva I5 con incidente.

---

## 3. M1/M2 (pre-D)

Riuso `docs/obs-o23-M-topology-list.json` + lettura live di stabilità `edge_relation`. Hash artefatto M: vedi digest sotto. Integrale:

```json
{
  "wave": "O24-M-split",
  "auth_provenance": "session mint TTL 180s, token non pubblicato",
  "reuses": "docs/obs-o23-M-topology-list.json",
  "o23_sha256": "7c1e25df5066797be943a8c852563bf03dfa752494d220f84353643c2afda331",
  "stability_live_1280": {
    "by": {
      "none": 1,
      "confirmed": 9,
      "fdb": 40
    },
    "A": 10,
    "B": 40,
    "rows_n": 50,
    "aH": 781.328125,
    "bH": 3201.25,
    "page": 7193,
    "A_share_of_page": 0.1086,
    "matches_o23_AB_counts": false,
    "o23_A": 12,
    "o23_B": 18
  },
  "groups_from_o23": {
    "1280": {
      "rows_n": 30,
      "len_rows_asserted": 30,
      "A_none_plus_confirmed": 12,
      "len_A_asserted": 12,
      "B_fdb": 18,
      "len_B_asserted": 18,
      "by_relation": {
        "none": 2,
        "confirmed": 10,
        "fdb": 18
      },
      "list_h": 2694,
      "h_pagina": 5645,
      "est_A_h": 1077.6,
      "est_A_share_of_page": 0.1909
    },
    "768": {
      "rows_n": 30,
      "len_rows_asserted": 30,
      "A_none_plus_confirmed": 12,
      "len_A_asserted": 12,
      "B_fdb": 18,
      "len_B_asserted": 18,
      "by_relation": {
        "none": 2,
        "confirmed": 10,
        "fdb": 18
      },
      "list_h": 2722,
      "h_pagina": 6444,
      "est_A_h": 1088.8,
      "est_A_share_of_page": 0.169
    },
    "390": {
      "rows_n": 50,
      "len_rows_asserted": 50,
      "A_none_plus_confirmed": 11,
      "len_A_asserted": 11,
      "B_fdb": 39,
      "len_B_asserted": 39,
      "by_relation": {
        "none": 1,
        "confirmed": 10,
        "fdb": 39
      },
      "list_h": 4524,
      "h_pagina": 10320,
      "est_A_h": 995.3,
      "est_A_share_of_page": 0.0964
    }
  },
  "conflicts": {
    "ok": true,
    "status": 200,
    "count": 0,
    "sample_n": 0
  },
  "gate_M": {
    "decision": "D_JUSTIFIED",
    "A_share_live_1280": 0.1086,
    "threshold_note": "se sola altezza gruppo A ≥0.35 della pagina → problema più profondo dello split FDB",
    "stability_AB_counts_match_o23": false,
    "conflicts_count": 0,
    "group_C_needed": false,
    "d1_390_recommendation": "closed_default",
    "rationale": "Gruppo A compatto (est share <<0.35); B=fdb in details + conteggio; non dipende da ratio anomalie",
    "come_potrebbe_fallire": "API topology non-idempotente cambia A/B; conflitti 403 maschera I3"
  },
  "stability_note": "Lettura live @1280: rows_n=50 A=10 B=40 (API topology non-idempotente vs O23@1280 rows=30 A=12 B=18). Struttura edge_relation stabile; Gruppo A resta piccolo (A_share_live=0.1086 <<0.35). Conteggi O23 riusati come baseline di design; live conferma gate A ok."
}
```

Digest: `docs/obs-o24-M-split.digest.json`.

### 4. Gate M

`gate_M.decision = D_JUSTIFIED` — A_share_live_1280≈0.1086 ≪ 0.35; conflitti API count=0 → nessun gruppo C; 390: `closed_default`.

---

## 5. D applicata

- Gruppo A (`edge_relation` ∈ {none, confirmed}): sezione inline «Confermati / diretti».
- Gruppo B (`fdb`): `<details data-o24="group-b">` **chiuso di default** a 1280/768/**390** (motivicazione: B ancora maggioranza a 390; conteggio nel summary = segnale).
- Summary: `{n} dispositivi visti solo tramite FDB — mostra dettagli`; `aria-expanded` / `aria-controls`.
- Ordine interno invariato (solo split). Canvas SVG invariato. Vocabolario «visto passare» invariato.

---

## 6. Previsioni vs osservati

| atteso | osservato | causa dominante |
|--------|-----------|-----------------|
| Δh grande negativo con B chiuso | @768/−3439, @390/−3440 `PASS_REDUCTION` | disclosure FDB |
| census match stesso payload API | @1280 V4 `INVALID_CENSUS` (49→29) | DEBT-TOPOLOGY-API-NONIDEMPOTENT |
| G4 local≈deployed | Δh=0 ×3 PASS | stesso codice 0.10.92 |

---

## 7. V1–V6 / A11y / drift / G (integrali)

### A/B + a11y (step 2, @1280)

```json
{
  "wave": "O24-AB-A11Y",
  "width": 1280,
  "pass": true,
  "pre_rows": 49,
  "post_rows": 49,
  "only_pre_sample": [],
  "only_post_sample": [],
  "summaryContrast": {
    "fg": "rgb(152, 162, 179)",
    "bg": "rgb(15, 19, 25)",
    "ratio": 7.232,
    "thr": 4.5,
    "fonte": "WCAG 2.2 SC 1.4.3 Contrast (Minimum) AA testo normale",
    "pass": true
  },
  "keyboard": {
    "after_open": {
      "open": true,
      "aria": "true"
    },
    "after_close": {
      "open": false,
      "aria": "false"
    }
  },
  "checks": {
    "V1_keys_equal": true,
    "len_only_pre_asserted": 0,
    "len_only_post_asserted": 0,
    "summary_bucket": "39 dispositivi visti solo tramite FDB — mostra dettagli",
    "has_split_marker": true,
    "has_group_a": true,
    "A_n": 10,
    "B_n": 39,
    "A_plus_B_eq_rows": true,
    "details_closed_default": true,
    "aria_expanded_closed": true,
    "aria_controls_set": true,
    "b_aria_hidden_zero": true,
    "b_display_none_zero": true,
    "keyboard_opens": true,
    "keyboard_closes": true,
    "contrast_pass": true,
    "frontend_post": "0.10.92",
    "paths_svg_pre": 48,
    "paths_svg_post": 48
  },
  "fail": []
}
```

### Drift repo↔NAS RO (step 3)

```json
{
  "phase": "pre_deploy_readonly",
  "NAS_count": 80,
  "repo_count": 79,
  "solo_NAS": [
    "scripts/_w4a_measure.py"
  ],
  "solo_repo_n": 0,
  "solo_repo": [],
  "orphans": [],
  "expected": {
    "solo_NAS": [
      "scripts/_w4a_measure.py"
    ],
    "solo_repo": []
  },
  "ssh_rc": 0,
  "DRIFT_OK": true,
  "method": "ssh find scripts/*.py RO vs local find scripts/*.py (incl. untracked); no NAS mutation",
  "note_git_tracked_only": "git ls-files undercounts (52); drift storico usa filesystem locale"
}
```

### V5 gates (step 1, integrale)

```
===== O24 V5 LOCAL GATES (integrale) =====

----- /tmp/o24-v5-w8.txt -----
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

----- /tmp/o24-v5-specificity.txt -----
EXIT:1
(vuoto + EXIT:1 da grep = nessun match = PASS atteso)

----- /tmp/o24-v5-color.txt -----
=== color_literal_gate.py --self-test ===
SELFTEST vue inject detected: (2, '#ff00aa', '.x { color: #ff00aa; /* O13D_COLOR_GATE_INJECT */ }')
SELFTEST matrix rule inject detected: (956, '#ff00aa', '.o14fix-gate-inject { color: #ff00aa; /* O14FIX_COLOR_GATE_INJECT */ }')
SELFTEST PASS: inject fails (vue+matrix rule), remove passes
EXIT_SELF:0

=== color_literal_gate.py ===
PASS: no hard-coded color literals outside allowlist; matrix.css decls-only
  token_file=assets/matrix.css (literals only in --custom-property decls)
  allowlist_count=16
EXIT:0

----- /tmp/o24-v5-contrast.txt -----
=== contrast_gate.py --self-test ===
SELFTEST inject detected: {'fg': '--inference-edge', 'bg': '--bg-1', 'fg_hex': '#220033', 'bg_hex': '#161b23', 'ratio': 1.089, 'threshold': 3.0, 'fonte': 'WCAG 2.2 SC 1.4.11 Non-text Contrast AA', 'ruolo': 'non_text', 'pass': False}
SELFTEST PASS: inject fails, remove passes
EXIT_SELF:0

=== contrast_gate.py ===
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

----- /tmp/o24-v5-evidence.txt -----
=== evidence_gate.py --self-test ===
SELFTEST ownership inject detected: views/_o20_evidence_gate_inject_tmp.vue:2: /collegato\s+a/ — asserisce ownership di link; FDB prova solo passaggio MAC (I5 rango 60) | <template><span class='edge-fdb'>collegato a switch</span></template>
SELFTEST i2 inject detected: views/Monitoring.vue:930: placeholder senza data-i2-condition/I2 vocab — dichiarare una di ('sorgente_non_disponibile', 'dispositivo_assente', 'misurato_a_zero', 'disabilitato_dall_operatore', 'limite_strutturale') | <span class="muted">—</span>
SELFTEST i2 after remove hits=0
SELFTEST marker_errs_after_inject=0 ownership_hits=0
SELFTEST marker_errs_after_stronger=1
SELFTEST marker inject detected: views/Topology.vue: marker /visto passare/ count=0 < 1 — vocabolario FDB O19 obbligatorio sulla Mappa
SELFTEST PASS: inject fails (ownership+marker+i2), remove passes
EXIT_SELF:0

=== evidence_gate.py ===
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

===== SUMMARY =====
w8: PASS
specificity: PASS (0 match)
color: PASS (+self-test)
contrast: PASS (+self-test, 1 allowlisted)
evidence: PASS (+self-test)
```

### V4/V6 (step 4)

```json
{
  "wave": "O24-V46",
  "auth_provenance": "session mint TTL 180s, token non pubblicato",
  "R_height": 320,
  "verdict_policy": "INVALID_CENSUS | FAIL_HEIGHT(dh>R) | PASS_REDUCTION(closed & dh<-R) | PASS(|dh|<=R)",
  "routes": {
    "topology": {
      "1280": {
        "try": 0,
        "census_match": false,
        "census_pre": {
          "h_pagina": 7184,
          "paths_svg": 48,
          "list_rows": 49,
          "list_parents": 48
        },
        "census_post": {
          "h_pagina": 3967,
          "paths_svg": 27,
          "list_rows": 29,
          "list_parents": 27
        },
        "h_pre": 7184,
        "h_post": 3967,
        "delta_h": -3217,
        "verdict": "INVALID_CENSUS",
        "details_open": false,
        "summary_text": "18 dispositivi visti solo tramite FDB — mostra dettagli",
        "summary_aria_expanded": "false",
        "A_n_post": 11,
        "B_n_post": 18,
        "len_only_pre_asserted": 19,
        "len_only_post_asserted": 1,
        "only_pre": [
          "Allsky 3|fdb|↳ visto passare da GS308EP",
          "Amazon Plug|fdb|↳ visto passare da GS308EP",
          "BMS Honeyw…— Boschetti|fdb|↳ visto passare da GS308EP",
          "DVR Hikvision|fdb|↳ visto passare da GS308EP",
          "Echo Biblioteca|fdb|↳ visto passare da GS308EP",
          "Echo Cabina Armadio|fdb|↳ visto passare da GS308EP",
          "Echo Cucina|fdb|↳ visto passare da GS308EP",
          "Echo Lavanderia|fdb|↳ visto passare da GS308EP",
          "Echo Salottino|fdb|↳ visto passare da GS308EP",
          "Echo — Cucina|fdb|↳ visto passare da GS308EP",
          "Echo — SalaPC|fdb|↳ visto passare da GS308EP",
          "GS308EP|fdb|↳ visto passare da GS308EP",
          "GS308EP|fdb|↳ visto passare da LGS310C",
          "Hub Tapo H100|fdb|↳ visto passare da GS308EP",
          "LGS328C|fdb|↳ visto passare da GS308EP",
          "Lavastoviglie Gaggenau|fdb|↳ visto passare da GS308EP",
          "Piano Indu…ne Gaggenau|fdb|↳ visto passare da GS308EP",
          "Sky|fdb|↳ visto passare da GS308EP",
          "Xiaomi Air…ina Armadio|fdb|↳ visto passare da GS308EP"
        ],
        "only_post": [
          "GS308EP|none|"
        ],
        "b_nodes_aria_hidden": 0,
        "b_nodes_display_none": 0,
        "frontend_post": "0.10.92"
      },
      "768": {
        "try": 0,
        "census_match": true,
        "census_pre": {
          "h_pagina": 7838,
          "paths_svg": 48,
          "list_rows": 49,
          "list_parents": 48
        },
        "census_post": {
          "h_pagina": 4399,
          "paths_svg": 48,
          "list_rows": 49,
          "list_parents": 48
        },
        "h_pre": 7838,
        "h_post": 4399,
        "delta_h": -3439,
        "verdict": "PASS_REDUCTION",
        "details_open": false,
        "summary_text": "39 dispositivi visti solo tramite FDB — mostra dettagli",
        "summary_aria_expanded": "false",
        "A_n_post": 10,
        "B_n_post": 39,
        "len_only_pre_asserted": 0,
        "len_only_post_asserted": 0,
        "only_pre": [],
        "only_post": [],
        "b_nodes_aria_hidden": 0,
        "b_nodes_display_none": 0,
        "frontend_post": "0.10.92"
      },
      "390": {
        "try": 0,
        "census_match": true,
        "census_pre": {
          "h_pagina": 10299,
          "paths_svg": 48,
          "list_rows": 49,
          "list_parents": 48
        },
        "census_post": {
          "h_pagina": 6859,
          "paths_svg": 48,
          "list_rows": 49,
          "list_parents": 48
        },
        "h_pre": 10299,
        "h_post": 6859,
        "delta_h": -3440,
        "verdict": "PASS_REDUCTION",
        "details_open": false,
        "summary_text": "39 dispositivi visti solo tramite FDB — mostra dettagli",
        "summary_aria_expanded": "false",
        "A_n_post": 10,
        "B_n_post": 39,
        "len_only_pre_asserted": 0,
        "len_only_post_asserted": 0,
        "only_pre": [],
        "only_post": [],
        "b_nodes_aria_hidden": 0,
        "b_nodes_display_none": 0,
        "frontend_post": "0.10.92"
      }
    }
  },
  "captures": {
    "1280": {
      "png": "docs/o24-captures/obs-o24-topology-1280.png",
      "png_w": 1280,
      "png_h": 3761,
      "sha256": "8d65bc6fe632d0d2e445163f5091a690e952a568744043f3f49f9241ca82aa67",
      "state": "details_closed"
    },
    "768": {
      "png": "docs/o24-captures/obs-o24-topology-768.png",
      "png_w": 768,
      "png_h": 4399,
      "sha256": "49288896b43a43a078fb66368f1fec2f3665f8b3f8186d453c4b225b132d00c2",
      "state": "details_closed"
    },
    "390": {
      "png": "docs/o24-captures/obs-o24-topology-390.png",
      "png_w": 390,
      "png_h": 7393,
      "sha256": "ea324e2d3e4e9b03e865a8c20d9bad5adf81c4c9f1173868c4eb25171a96fdfb",
      "state": "details_closed"
    }
  },
  "png_asserts": [
    {
      "pair": "1280x768",
      "rc": 0,
      "out": "obs-o24-topology-1280.png: 1280x3761 sha256=8d65bc6fe632d0d2e445163f5091a690e952a568744043f3f49f9241ca82aa67\nobs-o24-topology-768.png: 768x4399 sha256=49288896b43a43a078fb66368f1fec2f3665f8b3f8186d453c4b225b132d00c2\nPASS pair distinct widths\n"
    },
    {
      "pair": "1280x390",
      "rc": 0,
      "out": "obs-o24-topology-1280.png: 1280x3761 sha256=8d65bc6fe632d0d2e445163f5091a690e952a568744043f3f49f9241ca82aa67\nobs-o24-topology-390.png: 390x7393 sha256=ea324e2d3e4e9b03e865a8c20d9bad5adf81c4c9f1173868c4eb25171a96fdfb\nPASS pair distinct widths\n"
    }
  ],
  "open_capture": {
    "png": "docs/o24-captures/obs-o24-topology-1280-open.png",
    "png_w": 1280,
    "png_h": 7016,
    "sha256": "0b26b5abfe828ec1a482041c35781f407f9ecc96db0f7b88a3c617692b06b4b8",
    "state": "details_open",
    "rows_n": 48,
    "B_n": 38,
    "details_open": true,
    "h_open": 7016,
    "h_pre_ref": 7184,
    "delta_h_open_vs_pre": -168,
    "census_match_open_vs_pre": false,
    "verdict_open_vs_pre": "INVALID_CENSUS",
    "b_aria_hidden": 0,
    "b_display_none": 0
  },
  "criteria": {
    "V4_heights": {
      "1280": "INVALID_CENSUS",
      "768": "PASS_REDUCTION",
      "390": "PASS_REDUCTION"
    },
    "V4_any_fail_height": false,
    "V4_any_invalid_census": true,
    "V6_png_all_pass": true,
    "open_vs_pre": "INVALID_CENSUS"
  }
}
```

PNG sha256:

```
5bea42a7b4dd1d8466ad869a2860f5b8a4a5ae2be24a59ee7750bc4e2d3ffd2e  obs-o24-g4-topology-1280.png
da25a84a372d67d8737ed6933b5a15a25ea063c583acd1bd75904a8bbe60b8d0  obs-o24-g4-topology-390.png
dcd4d1dcaddbb83556dbb1a2efaa37f6e3cdfd8a6d94878b3fdf370a0b459dcc  obs-o24-g4-topology-768.png
0b26b5abfe828ec1a482041c35781f407f9ecc96db0f7b88a3c617692b06b4b8  obs-o24-topology-1280-open.png
8d65bc6fe632d0d2e445163f5091a690e952a568744043f3f49f9241ca82aa67  obs-o24-topology-1280.png
ea324e2d3e4e9b03e865a8c20d9bad5adf81c4c9f1173868c4eb25171a96fdfb  obs-o24-topology-390.png
49288896b43a43a078fb66368f1fec2f3665f8b3f8186d453c4b225b132d00c2  obs-o24-topology-768.png
```

### G3 deployed

```json
{
  "assets": [
    {
      "path": "/assets/index-Bdnrv2si.js",
      "sha256": "5136911d9267bef659268dc8c0009af67a8bf4f50b01030c9622da8480f9d5e0",
      "nbytes": 477714,
      "markers": {
        "0.10.92": true,
        "data-o24": true,
        "list-split": true,
        "visti solo tramite FDB": true,
        "group-b": true
      }
    },
    {
      "path": "/assets/index-G7DJ2F1e.css",
      "sha256": "05d7f2da6186d381a8ac52166dd242e7315b90f829bd8992bc7a30d5d9babad7",
      "nbytes": 144417,
      "markers": {
        "0.10.92": false,
        "data-o24": false,
        "list-split": false,
        "visti solo tramite FDB": false,
        "group-b": true
      }
    }
  ],
  "api_health_version": "0.10.82",
  "html_frontend_attr": null,
  "frontend_bundle_version": "0.10.92"
}
```

### G4 local POST ↔ deployed

```json
{
  "wave": "O24-G4",
  "R_height": 320,
  "policy": "one attempt; INVALID_CENSUS if census diverge; no absorb under R; no retry",
  "routes": {
    "1280": {
      "try": 0,
      "census_match": true,
      "census_local": {
        "paths_svg": 47,
        "list_rows": 48,
        "list_parents": 47
      },
      "census_deployed": {
        "paths_svg": 47,
        "list_rows": 48,
        "list_parents": 47
      },
      "h_local": 3763,
      "h_deployed": 3763,
      "delta_h": 0,
      "verdict": "PASS",
      "A_local": 10,
      "B_local": 38,
      "A_deployed": 10,
      "B_deployed": 38,
      "details_open_deployed": false,
      "summary_deployed": "38 dispositivi visti solo tramite FDB — mostra dettagli",
      "frontend_local": "0.10.92",
      "frontend_deployed": "0.10.92",
      "script_deployed": "/assets/index-Bdnrv2si.js"
    },
    "768": {
      "try": 0,
      "census_match": true,
      "census_local": {
        "paths_svg": 47,
        "list_rows": 48,
        "list_parents": 47
      },
      "census_deployed": {
        "paths_svg": 47,
        "list_rows": 48,
        "list_parents": 47
      },
      "h_local": 4480,
      "h_deployed": 4480,
      "delta_h": 0,
      "verdict": "PASS",
      "A_local": 10,
      "B_local": 38,
      "A_deployed": 10,
      "B_deployed": 38,
      "details_open_deployed": false,
      "summary_deployed": "38 dispositivi visti solo tramite FDB — mostra dettagli",
      "frontend_local": "0.10.92",
      "frontend_deployed": "0.10.92",
      "script_deployed": "/assets/index-Bdnrv2si.js"
    },
    "390": {
      "try": 0,
      "census_match": true,
      "census_local": {
        "paths_svg": 47,
        "list_rows": 48,
        "list_parents": 47
      },
      "census_deployed": {
        "paths_svg": 47,
        "list_rows": 48,
        "list_parents": 47
      },
      "h_local": 6909,
      "h_deployed": 6909,
      "delta_h": 0,
      "verdict": "PASS",
      "A_local": 10,
      "B_local": 38,
      "A_deployed": 10,
      "B_deployed": 38,
      "details_open_deployed": false,
      "summary_deployed": "38 dispositivi visti solo tramite FDB — mostra dettagli",
      "frontend_local": "0.10.92",
      "frontend_deployed": "0.10.92",
      "script_deployed": "/assets/index-Bdnrv2si.js"
    }
  },
  "captures_deployed": {
    "1280": {
      "png": "docs/o24-captures/obs-o24-g4-topology-1280.png",
      "png_w": 1280,
      "png_h": 3763,
      "sha256": "5bea42a7b4dd1d8466ad869a2860f5b8a4a5ae2be24a59ee7750bc4e2d3ffd2e"
    },
    "768": {
      "png": "docs/o24-captures/obs-o24-g4-topology-768.png",
      "png_w": 768,
      "png_h": 4480,
      "sha256": "dcd4d1dcaddbb83556dbb1a2efaa37f6e3cdfd8a6d94878b3fdf370a0b459dcc"
    },
    "390": {
      "png": "docs/o24-captures/obs-o24-g4-topology-390.png",
      "png_w": 390,
      "png_h": 6909,
      "sha256": "da25a84a372d67d8737ed6933b5a15a25ea063c583acd1bd75904a8bbe60b8d0"
    }
  },
  "criteria": {
    "verdicts": {
      "1280": "PASS",
      "768": "PASS",
      "390": "PASS"
    },
    "any_fail_height": false,
    "any_invalid_census": false,
    "closed": true,
    "note": "INVALID_CENSUS dichiarato senza retry (policy O22/O23)"
  }
}
```

---

## 8. Debiti

**Chiusi O24**
- `DEBT-O19-MAPPA-DESKTOP-GROWTH` — riduzione con B chiuso + G4 Δh=0.
- `DEBT-O23-MAPPA-DISCLOSURE-NOT-APPLICABLE` — superseded dallo split (wrapping totale resta non applicabile).

**Aperti / note**
- `DEBT-O23-ANOMALY-DEFINITION-FLAWED` — nota di metodo, attribuito al REVISORE.
- `DEBT-TOPOLOGY-API-NONIDEMPOTENT-ROOT-CAUSE` — V4@1280 INVALID_CENSUS (dichiarato, no retry).

---

## 9. Hash commit principale

`b6ae53084ce8485741950d9c0dbbb6774297ca4f` — contiene codice D Topology + bump 0.10.92 + artefatti M/V/G.

Per regola 0.2 (`PROCESS_NOTES.md`): l’eventuale commit successivo di sola pubblicazione di questo report **non** può contenere il proprio hash; O25 confermerà il tip reale in Blocco 0.1.

---

## 10. Cosa NON hai fatto

- Nessun tocco a T7, OBS-CURRENCY resolver, FA251, `_w4a_measure.py`, favicon, grano egress, `--inference` / `--inference-edge`.
- Nessuna modifica canvas SVG Topology; nessuna altra rotta; nessuna matrice O15.
- Nessun merge/tag/force su main; nessun cablaggio `/ai`.
- Nessuno script one-shot residuo in repo (harness solo `/tmp/o24_*.py`).
- Mint `.bak` non sovrascritto.
