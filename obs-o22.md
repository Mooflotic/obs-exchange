wc_l: 909
# OBS-O22 — Blocco 0 + OBS-CHASSIS-ID + OBS-SUPERSESSIONE-UI — 0.10.91
Data report: 2026-07-29 22:01 UTC
Auth catture: session mint TTL 180s, token non pubblicato.
Base confermata: `dcef325` (= HEAD = origin/feature/obs-currency). Ramo: `feature/obs-currency`.

## Vincolo UX Michele (O22)

NON far crescere l’interfaccia. Prima vista sintetica; niente card/pannelli/testo persistente lungo se basta un disambiguatore compatto. Dettagli in progressive disclosure (`title` / approfondisci già esistente). Segnale discreto solo su sospetto.

Applicazione:
- **Chassis:** solo collisione → `Nome · <ottetto MAC>` (compatto); IP/MAC completi nel `title`. Nessuna collisione → invariato.
- **Supersessione:** etichetta banda **invariata** («Dati mancanti o non correnti»); tre cause solo in `title` + `data-currency-hint`. Nessun layout nuovo.

## 1. Elenco file toccati

- `VERSION`, `web/package.json`, `CHANGELOG.md` → **0.10.91**
- `web/src/oggiChassis.js` (+ test) — `applyChassisDisplayCollisions` / `screen_name`
- `web/src/oggiProblems.js`, `web/src/views/Oggi.vue` — resa `screen_name` + `data-name-collision`
- `web/src/inventoryDevices.js` — collisioni righe `chassis:*`
- `web/src/views/Topology.vue` — select label solo se nome=canon chassis in collisione
- `web/src/oggiDecisionMatrix.js`, `web/src/components/OggiDecisionMatrix.vue` — HINTS/title (label invariata)
- `scripts/oggi_height_excl_flaky.py` — Zeek egress hybrid
- `scripts/evidence_gate.py` — marker O22
- `docs/KNOWN_DEBT.md`, artefatti `docs/obs-o22-*`, `docs/o22-captures/`

Plant: nessuna lista chassis omonimi (porte FDB); altezze verificate invariate. Inventory/Oggi/Topology = rotte nome chassis.

## 2. Blocco 0

### 0.1 Conferma commit dcef325 — CONFERMATA

```
$ git log --oneline -5 feature/obs-currency
dcef325 feat(observatory): I2 placeholder distinguibili e fix evidenza O20 (0.10.90)
c459afd docs(observatory): pubblica report O20 su obs-exchange (commit-pinned)
5f71e0f feat(observatory): evidenza sito-wide e presidi contrasto (0.10.89)
30b65f7 docs(observatory): chiude O19 con deploy G3/G4 e share verificato
45b3453 feat(observatory): mappa onesta su /topology (0.10.88)

$ git log --oneline -1 origin/feature/obs-currency
dcef325 feat(observatory): I2 placeholder distinguibili e fix evidenza O20 (0.10.90)

$ git rev-parse HEAD
dcef3259088d4bd8b922b79bceb74373fb631ffd
$ git rev-parse origin/feature/obs-currency
dcef3259088d4bd8b922b79bceb74373fb631ffd
```

Milestone O21 confermata retroattivamente: HEAD locale = origin = `dcef325`.

### 0.2 Zeek egress hybrid in allowlist

Aggiunta terza voce in `scripts/oggi_height_excl_flaky.py`. Rimisura oggi@1280: Δ_raw=0 Δ_excl=0.
Artefatto: `docs/obs-o22-B0-oggi-height-1280.json` sha256=`b47c9e9b4e19f668bc2b84ac57530c2f609da533498e7ce9d0962f782752fadd`

```json
{
  "wave": "O21-B0.1",
  "auth_provenance": "catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato",
  "width": 1280,
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
    },
    {
      "pattern": "Zeek egress hybrid",
      "debt": "DEBT-O20-OGGI-API-HEIGHT-JITTER",
      "reason": "O21 V4 oggi@1280 only_pre_info: «Sorgente copertura vecchia · Zeek egress hybrid» causò Δh=−173 entro R ma non era in allowlist; terza sorgente coverage API-based intermittente (stessa famiglia Fritz/Zeek behaviour)"
    }
  ],
  "len_allowlist_asserted": 3,
  "come_potrebbe_fallire": "se Δ resta >R dopo esclusione Fritz/Zeek, la causa non è quella allowlist — STOP, non escludere altro",
  "o20_reference_delta_plus409": {
    "source": "docs/obs-o20.md / KNOWN_DEBT (artefatto pinnato)",
    "delta_h": 409,
    "note": "Δ−212 solo-chat NON ammesso come evidenza"
  },
  "pre": {
    "h_raw": 15430,
    "h_excl": 15430,
    "cards_n": 30,
    "flaky_hidden_n": 0,
    "flaky_hidden": [],
    "frontend_version": null,
    "api_health_version": null,
    "script_src": "/assets/index-DRlt-wzC.js"
  },
  "post": {
    "h_raw": 15430,
    "h_excl": 15430,
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

### 0.3 Monitoring 7→5 — spiegato

Confronto `obs-o21-M-pre-D` vs `obs-o21-V1V2`/`M-post-D`: scomparsi (1) up_ratio_24h «—» (dato live), (2) una foglia SNMP/speedtest «—» (poll/dato). Non rimozione da D.
`DEBT-O21-MONITORING-COUNT-UNEXPLAINED` CHIUSO.
Artefatto sha256=`0381524f80fe29ed2625ae0dbd56b99b30a3e6326610503412c732a13a984502`

```json
{
  "debt": "DEBT-O21-MONITORING-COUNT-UNEXPLAINED",
  "sources": [
    "docs/obs-o21-M-pre-D.json",
    "docs/obs-o21-M-post-D.json",
    "docs/obs-o21-V1V2.json"
  ],
  "pre_n": 7,
  "post_n": 5,
  "delta": -2,
  "pre_breakdown": {
    "ambiguo": 3,
    "sorgente_non_disponibile_titled": 2,
    "non_dichiarata": 2
  },
  "post_breakdown": {
    "limite_strutturale": 3,
    "sorgente_non_disponibile_latency": 2
  },
  "disappeared": [
    {
      "element": "up_ratio_24h «—» (non_dichiarata in PRE)",
      "cause": "dato live: in POST non compare placeholder up_ratio ⇒ rapporto 24h campionato nel frattempo",
      "evidence": "POST groups hanno solo latency×2 come sorgente; nessun gruppo up_ratio/—"
    },
    {
      "element": "una foglia SNMP o speedtest «—» (ambiguo/non_dichiarata in PRE)",
      "cause": "dato live più probabile: poll.at o throughput speedtest passato da null a valorizzato; oppure switch con poll fallito ora ok (traffico/errori non più —)",
      "evidence": "PRE aveva traffico+errori titled sorgente + 3 ambiguo; POST ha solo 3 limite su GS308-like (no SNMP) — lo switch con poll fallito/titled non produce più —"
    }
  ],
  "not_cause": "rimozione informativa da D (D aggiunge attributi; non cancella celle)",
  "come_potrebbe_fallire": "se i JSON fossero di sessioni non confrontabili senza censimento; qui stesso inventario di celle tipizzate I2"
}
```

### 0.4 DEBT-TOPOLOGY-API-NONIDEMPOTENT-ROOT-CAUSE

Registrato in KNOWN_DEBT (solo registrazione). Confermato di nuovo in G4 O22 topology@768 INVALID_CENSUS.

## 3. M (pubblicata PRIMA di D)

### M chassis — sha256=`a9d5094139f2ab132f071faf23446941d765e545ad87fed27099622c3b4f710a`

```json
{
  "wave": "O22-M-chassis",
  "auth_provenance": "session mint TTL 180s, token non pubblicato",
  "endpoint_assets": "/api/assets?include_historical=true&all_proposals=true",
  "endpoint_chassis": "/api/chassis",
  "assets_n": 151,
  "chassis_groups_n": 14,
  "all_chassis_rows_n": 14,
  "len_all_chassis_asserted": 14,
  "multi_member_cards_n": 14,
  "len_multi_asserted": 14,
  "collision_groups_all_chassis": [
    {
      "display_name": "Sky",
      "n_chassis": 2,
      "chassis": [
        {
          "chassis_id": 31,
          "members_n": 2,
          "member_ids": [
            61,
            137
          ],
          "display_name": "Sky",
          "name_kind": "member_name",
          "primary_mac": "38:A6:CE:79:D4:FD",
          "primary_ip": "192.168.2.254",
          "mac_last_octet": "FD"
        },
        {
          "chassis_id": 33,
          "members_n": 3,
          "member_ids": [
            43,
            136,
            149
          ],
          "display_name": "Sky",
          "name_kind": "member_name",
          "primary_mac": "38:A6:CE:3E:9C:AA",
          "primary_ip": "192.168.2.101",
          "mac_last_octet": "AA"
        }
      ],
      "len_chassis_asserted": 2
    }
  ],
  "len_collision_groups_all_asserted": 1,
  "collision_groups_buildChassisNameCards_population": [
    {
      "display_name": "Sky",
      "n_chassis": 2,
      "chassis": [
        {
          "chassis_id": 31,
          "members_n": 2,
          "member_ids": [
            61,
            137
          ],
          "display_name": "Sky",
          "name_kind": "member_name",
          "primary_mac": "38:A6:CE:79:D4:FD",
          "primary_ip": "192.168.2.254",
          "mac_last_octet": "FD"
        },
        {
          "chassis_id": 33,
          "members_n": 3,
          "member_ids": [
            43,
            136,
            149
          ],
          "display_name": "Sky",
          "name_kind": "member_name",
          "primary_mac": "38:A6:CE:3E:9C:AA",
          "primary_ip": "192.168.2.101",
          "mac_last_octet": "AA"
        }
      ],
      "len_chassis_asserted": 2
    }
  ],
  "len_collision_groups_cards_asserted": 1,
  "come_potrebbe_fallire": "display_name assente o normalizzazione diversa nasconde collisioni"
}
```

len_collision_groups_asserted=1 (solo Sky 31/33). len_all_chassis=14.

### M supersessione — sha256=`202f5731de174676171274b5c688191fa9348463ddf19d925cb98947b7588130`

Sintesi: `/api/admin/facts/conflicts` status=200 count=0. Violazione: etichetta banda confonde missing/TTL/superseded. gate_M=`D_JUSTIFIED_VOCAB_ONLY`.
Verdict M: `vocab_exists_for_superseded_distinct_from_I1_I2` = false (pre-D).

```json
{
  "admin_facts_conflicts": {
    "status": 200,
    "ok": true,
    "n": 0,
    "sample": [],
    "keys": [
      "conflicts",
      "count"
    ],
    "body_head": "{\"conflicts\":[],\"count\":0}"
  },
  "verdict": {
    "admin_conflicts_reachable": true,
    "admin_conflicts_status": 200,
    "vocab_exists_for_superseded_distinct_from_I1_I2": false,
    "missing_stale_ambiguous": true,
    "missing_stale_note": "Etichetta «Dati mancanti o non correnti» (matrix missing_stale) raggruppa assenza, bassa correntezza e possibili fatti non current senza distinguere: superseded vs TTL-scaduto vs I3 conflitto. Non è un vocabolo FactAssertion.state=historical.",
    "violations": [
      {
        "where": "/oggi matrice banda missing_stale",
        "severity": "media — confusione lessicale non perdita dati",
        "issue": "«non correnti» non dichiara quale delle tre cause (superseded / TTL / conflitto)",
        "distinguishes_superseded_vs_ttl_vs_conflict": false
      }
    ],
    "gate_M": "D_JUSTIFIED_VOCAB_ONLY",
    "markers_present": {
      "superseded_or_historical_word": false,
      "ttl_or_scaduto_word": false,
      "conflitto_word": false
    }
  }
}
```

## 4. D applicata

### Chassis
`applyChassisDisplayCollisions`: solo gruppi con display_name duplicato → `screen_name = Nome · <ottetto MAC>` (fallback IP); `display_name` invariato; `collision_detail` (IP+MAC) nel title. Rotte: Oggi/Apparati, Inventory (`chassis:*`), Topology (select se label=canon).

### Supersessione
Label persistente **non** allungata (UX Michele). Solo `MATRIX_BAND_HINTS` → `title` + `data-currency-hint="missing|ttl_stale|superseded"`.

## 5. Previsioni vs osservati

| Previsione | Osservato | Causa dominante |
|---|---|---|
| Solo Sky 31/33 cambiano resa | only_pre=`Sky` only_post=`Sky · FD`,`Sky · AA` (len 1→2) | collisione display_name |
| Altezze ≈0 / ≤R | tutte PASS dopo census corretto; Δh oggi@1280=−154 ≤R | jitter coverage API + testo compatto |
| Label banda invariata | label_unchanged_compact=true | UX disclosure |
| Topology G4 può INVALID | topology@768 INVALID_CENSUS 27≠47 | DEBT topology API |

## 6. V1–V5 integrali

### V1 invarianza informativa
```json
{
  "only_pre": [
    "Sky"
  ],
  "only_post": [
    "Sky · AA",
    "Sky · FD"
  ],
  "added_text_bucket": [
    "Sky · AA",
    "Sky · FD"
  ],
  "len_only_pre": 1,
  "len_only_post": 2,
  "no_removal_beyond_sky_plain": true
}
```
```json
{
  "sky_pre": [
    "Sky"
  ],
  "sky_post": [
    "Sky · AA",
    "Sky · AAnome inferito",
    "Sky · FD",
    "Sky · FDnome inferito"
  ],
  "collisions_post_n": 2,
  "expect_two_distinct_sky": true
}
```
```json
{
  "missing_stale_labels": [
    "Dati mancanti o non correnti",
    "Dati mancanti o non correnti",
    "Dati mancanti o non correnti",
    "Dati mancanti o non correnti",
    "Dati mancanti o non correnti"
  ],
  "label_unchanged_compact": true,
  "hints_present": true,
  "titles_mention_superseded": true
}
```
Bucket testo aggiunto: solo `Sky · AA` / `Sky · FD`. Nessuna rimozione oltre il plain `Sky` sostituito dal disambiguato.

### V2 strutturale
Chassis 31/33 restano distinti; fatti storici non rimossi; odm_bands 36→36; inventory rows 72→72.

### V3 gate (output integrale)
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
=== specificity grep ===
(nessun match)
=== color_literal_gate --self-test ===
SELFTEST vue inject detected: (2, '#ff00aa', '.x { color: #ff00aa; /* O13D_COLOR_GATE_INJECT */ }')
SELFTEST matrix rule inject detected: (956, '#ff00aa', '.o14fix-gate-inject { color: #ff00aa; /* O14FIX_COLOR_GATE_INJECT */ }')
SELFTEST PASS: inject fails (vue+matrix rule), remove passes
=== color_literal_gate ===
PASS: no hard-coded color literals outside allowlist; matrix.css decls-only
  token_file=assets/matrix.css (literals only in --custom-property decls)
  allowlist_count=16
=== contrast_gate --self-test ===
SELFTEST inject detected: {'fg': '--inference-edge', 'bg': '--bg-1', 'fg_hex': '#220033', 'bg_hex': '#161b23', 'ratio': 1.089, 'threshold': 3.0, 'fonte': 'WCAG 2.2 SC 1.4.11 Non-text Contrast AA', 'ruolo': 'non_text', 'pass': False}
SELFTEST PASS: inject fails, remove passes
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
=== evidence_gate --self-test ===
SELFTEST ownership inject detected: views/_o20_evidence_gate_inject_tmp.vue:2: /collegato\s+a/ — asserisce ownership di link; FDB prova solo passaggio MAC (I5 rango 60) | <template><span class='edge-fdb'>collegato a switch</span></template>
SELFTEST i2 inject detected: views/Monitoring.vue:930: placeholder senza data-i2-condition/I2 vocab — dichiarare una di ('sorgente_non_disponibile', 'dispositivo_assente', 'misurato_a_zero', 'disabilitato_dall_operatore', 'limite_strutturale') | <span class="muted">—</span>
SELFTEST i2 after remove hits=0
SELFTEST marker_errs_after_inject=0 ownership_hits=0
SELFTEST marker_errs_after_stronger=1
SELFTEST marker inject detected: views/Topology.vue: marker /visto passare/ count=0 < 1 — vocabolario FDB O19 obbligatorio sulla Mappa
SELFTEST PASS: inject fails (ownership+marker+i2), remove passes
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

```

### V3 conservation
```json
{
  "wave": "O22-conservation",
  "assets_endpoint": "/api/assets?include_historical=true&all_proposals=true",
  "assets_n": 151,
  "chassis_endpoint": "/api/chassis",
  "chassis_groups_n": 14,
  "queueConservationCheck_note": "P4 unit test oggiChassis.test.js PASS (missing/duplicated empty); population=buildChassisNameCards",
  "len_assets_asserted": 151,
  "len_chassis_asserted": 14
}
```
Unit P4 `queueConservationCheck` → missing/duplicated empty (oggiChassis.test.js 12/12).

### V3 drift repo↔NAS (eseguito)
```json
{
  "phase": "post_deploy",
  "NAS_count": 103,
  "repo_count": 102,
  "solo_NAS": [
    "scripts/_w4a_measure.py"
  ],
  "solo_repo": [],
  "solo_repo_n": 0,
  "solo_NAS_enumerated": [
    "scripts/_w4a_measure.py"
  ],
  "expected": {
    "solo_NAS": [
      "scripts/_w4a_measure.py"
    ]
  },
  "orphans": [],
  "DRIFT_OK": true,
  "ssh_rc": 0,
  "ssh_err": ""
}
```

### V4 altezze
Tutti PASS (oggi: census corretto escludendo collisions_n intenzionale 0→2). Criteri:
```json
{
  "verdicts": [
    "PASS",
    "PASS",
    "PASS",
    "PASS",
    "PASS",
    "PASS",
    "PASS",
    "PASS",
    "PASS",
    "PASS",
    "PASS",
    "PASS"
  ],
  "all_pass_or_invalid_honest": true,
  "any_fail_height": false,
  "oggi_census_correction": [
    "oggi@1280: PASS Δh=-154 bands=36→36",
    "oggi@768: PASS Δh=35 bands=36→36",
    "oggi@390: PASS Δh=17 bands=36→36"
  ]
}
```
Dettaglio rotte (verdict/Δh/census):
```json
{
  "oggi@1280": {
    "verdict": "PASS",
    "delta_h": -154,
    "census_match": true,
    "h_pre": 14624,
    "h_post": 14470
  },
  "oggi@768": {
    "verdict": "PASS",
    "delta_h": 35,
    "census_match": true,
    "h_pre": 17861,
    "h_post": 17896
  },
  "oggi@390": {
    "verdict": "PASS",
    "delta_h": 17,
    "census_match": true,
    "h_pre": 22511,
    "h_post": 22528
  },
  "inventory@1280": {
    "verdict": "PASS",
    "delta_h": 0,
    "census_match": true,
    "h_pre": 6305,
    "h_post": 6305
  },
  "inventory@768": {
    "verdict": "PASS",
    "delta_h": 0,
    "census_match": true,
    "h_pre": 6418,
    "h_post": 6418
  },
  "inventory@390": {
    "verdict": "PASS",
    "delta_h": 0,
    "census_match": true,
    "h_pre": 6712,
    "h_post": 6712
  },
  "topology@1280": {
    "verdict": "PASS",
    "delta_h": 0,
    "census_match": true,
    "h_pre": 5559,
    "h_post": 5559
  },
  "topology@768": {
    "verdict": "PASS",
    "delta_h": 0,
    "census_match": true,
    "h_pre": 7838,
    "h_post": 7838
  },
  "topology@390": {
    "verdict": "PASS",
    "delta_h": 0,
    "census_match": true,
    "h_pre": 10299,
    "h_post": 10299
  },
  "plant@1280": {
    "verdict": "PASS",
    "delta_h": 0,
    "census_match": true,
    "h_pre": 2228,
    "h_post": 2228
  },
  "plant@768": {
    "verdict": "PASS",
    "delta_h": 0,
    "census_match": true,
    "h_pre": 2964,
    "h_post": 2964
  },
  "plant@390": {
    "verdict": "PASS",
    "delta_h": -2,
    "census_match": true,
    "h_pre": 5507,
    "h_post": 5505
  }
}
```

### V5 catture + o9_png_assert
```json
{
  "asserts": [
    {
      "slug": "oggi",
      "pair": "1280x768",
      "rc": 0,
      "out": "obs-o22-oggi-1280.png: 1280x14470 sha256=e1016abf76adff973629db7a889a17f403e45a89366e914ec9c10af1eee5a327\nobs-o22-oggi-768.png: 768x18109 sha256=6afd811d1f965a6548c3dfab2a411d6c8b79e933922bc404032b37f6a826228d\nPASS pair distinct widths\n"
    },
    {
      "slug": "oggi",
      "pair": "1280x390",
      "rc": 0,
      "out": "obs-o22-oggi-1280.png: 1280x14470 sha256=e1016abf76adff973629db7a889a17f403e45a89366e914ec9c10af1eee5a327\nobs-o22-oggi-390.png: 390x22528 sha256=68c8b7a37d0eb2ff408e562e732b794559fe2c2c5b7653a2fcc68a26824fb235\nPASS pair distinct widths\n"
    },
    {
      "slug": "inventory",
      "pair": "1280x768",
      "rc": 0,
      "out": "obs-o22-inventory-1280.png: 1280x6305 sha256=0fbc8d36128cbcafdf966ca312de2a05c47e6bc9051f39f6420b19f9e54c0d41\nobs-o22-inventory-768.png: 768x6418 sha256=0ce95fa408a082f6075843d1a3377c8a2338807c19fd42976102e6d2d2a93e5a\nPASS pair distinct widths\n"
    },
    {
      "slug": "inventory",
      "pair": "1280x390",
      "rc": 0,
      "out": "obs-o22-inventory-1280.png: 1280x6305 sha256=0fbc8d36128cbcafdf966ca312de2a05c47e6bc9051f39f6420b19f9e54c0d41\nobs-o22-inventory-390.png: 390x6712 sha256=3ffcb63a4078d7cfd2f3ef9ecef5516740a73a0a21e4f4ff141633dbe4d8469d\nPASS pair distinct widths\n"
    },
    {
      "slug": "topology",
      "pair": "1280x768",
      "rc": 0,
      "out": "obs-o22-topology-1280.png: 1280x5559 sha256=946dda3f6f145d5f4423f998b7065d0c2769908de59b092e7bcf0e6f55688a6c\nobs-o22-topology-768.png: 768x7838 sha256=f3c2fdc5bb118d25e1a6e7c5f68edb49746bd0c0fc3558623c8476759e44af0f\nPASS pair distinct widths\n"
    },
    {
      "slug": "topology",
      "pair": "1280x390",
      "rc": 0,
      "out": "obs-o22-topology-1280.png: 1280x5559 sha256=946dda3f6f145d5f4423f998b7065d0c2769908de59b092e7bcf0e6f55688a6c\nobs-o22-topology-390.png: 390x10299 sha256=23c618a7da96055c974ca760457e3d1bb0dd2d0a59a6212c279d4931cb9c01d8\nPASS pair distinct widths\n"
    }
  ],
  "all_pass": true
}
```

## 7. G Deploy / prova / git

### G1 bump 0.10.91 — fatto
### G2 `./scripts/deploy.sh web` — ok (log `docs/obs-o22-G2-deploy.log`)
### G3 prova diretta
```json
{
  "wave": "O22-G3",
  "index_html_js": "/assets/index-EKiFcL_r.js",
  "index_html_css": "/assets/index-qABMkN1m.css",
  "js_bytes": 475927,
  "css_bytes": 144003,
  "js_http": 200,
  "css_http": 200,
  "markers": {
    "0.10.91_in_js": true,
    "applyChassisDisplayCollisions": true,
    "superseded_hint": true,
    "short_band": true,
    "long_band_absent": true
  },
  "api_health": {
    "ok": true,
    "service": "observatory-api",
    "version": "0.10.82"
  },
  "page": {
    "frontend": "0.10.91",
    "api_health_attr": "0.10.82",
    "brand": "v0.10.91 · api 0.10.82 · 29/07",
    "script": "http://192.168.1.3:8080/assets/index-EKiFcL_r.js",
    "collisions": [
      {
        "t": "Sky · FD",
        "id": "31"
      },
      {
        "t": "Sky · AA",
        "id": "33"
      }
    ],
    "missing_hint": "missing|ttl_stale|superseded",
    "missing_title": "Dati mancanti o non correnti — tre cause: (1) assente / sorgente non disponibile (I2); (2) scaduto per TTL (bassa correntezza, ancora current); (3) superseded /",
    "missing_label": "Dati mancanti o non correnti"
  },
  "pass": true
}
```
### G4 ricattura deployed
```json
{
  "oggi@1280": {
    "verdict": "PASS",
    "delta_h": 154,
    "census_match": true,
    "census_local": [
      36
    ],
    "census_deployed": [
      36
    ]
  },
  "oggi@768": {
    "verdict": "PASS",
    "delta_h": 0,
    "census_match": true,
    "census_local": [
      36
    ],
    "census_deployed": [
      36
    ]
  },
  "oggi@390": {
    "verdict": "PASS",
    "delta_h": 0,
    "census_match": true,
    "census_local": [
      36
    ],
    "census_deployed": [
      36
    ]
  },
  "inventory@1280": {
    "verdict": "PASS",
    "delta_h": 0,
    "census_match": true,
    "census_local": [
      72
    ],
    "census_deployed": [
      72
    ]
  },
  "inventory@768": {
    "verdict": "PASS",
    "delta_h": 0,
    "census_match": true,
    "census_local": [
      72
    ],
    "census_deployed": [
      72
    ]
  },
  "inventory@390": {
    "verdict": "PASS",
    "delta_h": 0,
    "census_match": true,
    "census_local": [
      72
    ],
    "census_deployed": [
      72
    ]
  },
  "topology@1280": {
    "verdict": "PASS",
    "delta_h": 0,
    "census_match": true,
    "census_local": [
      46,
      46
    ],
    "census_deployed": [
      46,
      46
    ]
  },
  "topology@768": {
    "verdict": "INVALID_CENSUS",
    "delta_h": 1490,
    "census_match": false,
    "census_local": [
      27,
      27
    ],
    "census_deployed": [
      47,
      47
    ]
  },
  "topology@390": {
    "verdict": "PASS",
    "delta_h": 0,
    "census_match": true,
    "census_local": [
      47,
      47
    ],
    "census_deployed": [
      47,
      47
    ]
  },
  "plant@390": {
    "verdict": "PASS",
    "delta_h": 0,
    "census_match": true,
    "census_local": [
      46
    ],
    "census_deployed": [
      46
    ]
  }
}
```
topology@768 **INVALID_CENSUS** onesto (paths 27 vs 47) — DEBT topology API; non forzato sotto R.

### G5 commit/push — vedi §8 (hash effettivi, push confermato)

### G6
Nessuno script one-shot residuo in repo (`/tmp/o22_verify_v.py` non committato).

## 8. Hash commit e push CONFERMATI

```
feature (0.10.91): 76da2a25bbfa0e1382d1417dd7ae3e5b15b772a0
  feat(observatory): chassis disambiguati e vocab supersessione in disclosure (0.10.91)
docs seals:
  9e65fd3443219985c1cf1c844c1ba94bcedfba27  sigilla report O22 con hash commit G5
  6c684f55b1aae06e69de6962dad1c257ab081cd1  conferma push O22 in report G5
HEAD tip (= questo commit report): be427c80fe47be698a9c61f40d87201a4fecd693
origin/feature/obs-currency: be427c80fe47be698a9c61f40d87201a4fecd693 (dopo push)
branch: feature/obs-currency = origin/feature/obs-currency
push: CONFERMATO (dcef325..tip). Vietati main/merge/tag/force/rewrite — non usati.
O21 base confermata: dcef3259088d4bd8b922b79bceb74373fb631ffd
```


## 9. Debiti

| Debito | Stato |
|---|---|
| DEBT-O21-MONITORING-COUNT-UNEXPLAINED | CHIUSO O22 0.3 |
| DEBT-CHASSIS-NAME-COLLISION | CHIUSO O22 (resa) |
| DEBT-O22-SUPERSESSION-VOCAB-DISCLOSURE | CHIUSO O22 (disclosure) |
| DEBT-TOPOLOGY-API-NONIDEMPOTENT-ROOT-CAUSE | APERTO (registrato) |
| DEBT-O20-OGGI-API-HEIGHT-JITTER | già chiuso; allowlist +Zeek egress |

## 10. Cosa NON hai fatto

- Nessun tocco a OBS-CURRENCY / `api/app/facts/` / resolver
- Nessuna fusione/rinomina chassis; nessun layout nuovo; niente card/pannelli
- Nessun main/merge/tag/force; api non rebuild (solo web)
- Plant senza disambiguatore (nessuna lista chassis omonimi)
- Root cause topology API non indagata (fuori scope)
- T7, FA251, favicon, grano egress, --inference*, MAPPA-DESKTOP-GROWTH, OGGI-MOBILE-DENSITY intatti
