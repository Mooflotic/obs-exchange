# OBS-O25 — Blocco 0 + OBS-OGGI-LIFECYCLE (scoperta + policy, NO D)

```
wave: O25
branch: feature/obs-currency
base_dichiarata_O24: 18d148910e2901c5f067799dea9a3986ce91380f
commit_principale: 4571e459d45eda58049be1246cfa3c2d74198689
nota_0.2: tip di sola pubblicazione non autocertificato; O26 conferma in Blocco 0.1
VERSION: invariata (nessun codice)
esito: GATE 0 PASS · M0 pubblicato · P scritta · P7(c)=vuoto · D rimandata a O26 (sequenza)
```

---

## 1. Elenco file toccati

| path | ruolo |
|------|--------|
| `docs/obs-o25-M0-discovery.json` | scoperta M0.1–M0.8 |
| `docs/obs-o25-P-policy.md` | policy P1–P8 |
| `docs/obs-o25.md` | questo report |

Nessun file di codice.

---

## 2. Blocco 0.1 (integrale)

```
===== 0.1 git log --oneline -8 feature/obs-currency =====
18d1489 docs(observatory): report O24 split disclosure (principale b6ae530)
b6ae530 feat(observatory): O24 Topology split A/B disclosure FDB (0.10.92)
c880f36 docs(observatory): allinea tip §9 O23 a HEAD/origin 65375c9
65375c9 docs(observatory): registra tip commit §9 O23
f856c27 docs(observatory): §9 O23 con hash HEAD/origin verificato 9a0758e
9a0758e docs(observatory): registra tip push O23 in §9
8ed633e docs(observatory): §9 O23 con tip HEAD esplicito
4f2d7a9 docs(observatory): completa §9 hash O23 STOP

===== git rev-parse HEAD =====
18d148910e2901c5f067799dea9a3986ce91380f

===== git fetch origin && git rev-parse origin/feature/obs-currency =====
18d148910e2901c5f067799dea9a3986ce91380f

===== ancestor b6ae530 (O24 principale)? =====
YES

===== HEAD == declared 18d1489? =====
YES
===== HEAD == origin? =====
YES
```

**Verdetto:** HEAD=origin=`18d148910e2901c5f067799dea9a3986ce91380f`; antenato `b6ae530` = YES. GATE BLOCCO 0 PASS.

---

## 3. M0 discovery (integrale)

Hash contenuto (calcolato pre-P e invariato): `sha256=c61da0bba2e732826a89229a56f5c1c1334a1226877f86d686dd092a146b69f2` · `wc_l=335`

```json
{
  "wave": "O25-M0-discovery",
  "mode": "READ_ONLY",
  "auth_provenance": "session mint TTL 180s for M0.7 only; token non pubblicato",
  "generated_at": "2026-07-30T04:18:31.124637+00:00",
  "base_confirmed": "18d148910e2901c5f067799dea9a3986ce91380f",
  "M0_1_routes": {
    "len_routes_asserted": 7,
    "routes": [
      {
        "path": "/actions",
        "view": "web/src/views/Actions.vue",
        "shows": "Coda operativa ActionRequest + ScanRun (WoL/shutdown/scan…)",
        "model": "ActionRequest status pending|approved|running|done|failed|rejected; decided_at; result text",
        "closed_cases_with_outcome_motivation": false,
        "representation": "raw_operational_queue",
        "api": [
          "GET/POST /api/actions",
          "POST /api/actions/{id}/approve|reject",
          "scans*"
        ],
        "exposes": {
          "esito": false,
          "motivazione": false,
          "chiuso": false,
          "riaperto": false
        },
        "priority_verdict": "NON è decision log F-9; è coda di esecuzione"
      },
      {
        "path": "/timeline",
        "view": "web/src/views/Timeline.vue",
        "shows": "Cronologia Event raggruppati; read/mute; toggle Mostra archivio (lifecycle archived/superseded/suppressed)",
        "model": "Event + EventMute + EventRead",
        "closed_cases_with_outcome_motivation": false,
        "representation": "raw_chronology_plus_read_mute_archive_filter",
        "api": [
          "GET /api/events",
          "POST /api/events/read",
          "POST/DELETE /api/events/mutes*"
        ],
        "exposes": {
          "esito": false,
          "motivazione": false,
          "chiuso": false,
          "riaperto": false
        },
        "closest_archivio_note": "toggle 'Mostra archivio' = filtro lifecycle eventi, non Archivio casi F-9"
      },
      {
        "path": "/findings",
        "view": "web/src/views/Findings.vue",
        "shows": "Finding aperti + drift; edit status/assignee/notes",
        "model": "Finding.status open|ack|confirmed|resolved; notes Text",
        "closed_cases_with_outcome_motivation": "partial",
        "representation": "triage_table_status_notes_not_f9_disposition",
        "api": [
          "GET /api/findings",
          "PATCH /api/findings/{id}"
        ],
        "exposes": {
          "esito": "partial_status",
          "motivazione": "partial_notes",
          "chiuso": "partial_resolved",
          "riaperto": false
        }
      },
      {
        "path": "/incidents",
        "view": "web/src/views/Incidents.vue",
        "shows": "Incident monitor; ack/resolve/dismiss/silenzia/archivia",
        "model": "Incident.status open|acked|resolved|dismissed; acked_at/resolved_at/dismissed_at; NO closed_reason",
        "closed_cases_with_outcome_motivation": "partial",
        "representation": "monitor_incident_lifecycle_no_structured_motivation",
        "api": [
          "GET /api/incidents",
          "POST …/ack|dismiss|resolve",
          "POST /api/monitors/{id}/silences"
        ],
        "exposes": {
          "esito": "partial_status",
          "motivazione": false,
          "chiuso": "partial_resolved_dismissed",
          "riaperto": false
        }
      },
      {
        "path": "/osservatorio",
        "view": "web/src/views/RadarStub.vue",
        "shows": "Stub placeholder radar",
        "model": null,
        "closed_cases_with_outcome_motivation": false,
        "representation": "placeholder_stub",
        "api": [],
        "exposes": {
          "esito": false,
          "motivazione": false,
          "chiuso": false,
          "riaperto": false
        }
      },
      {
        "path": "/runbook",
        "view": "web/src/views/Runbook.vue",
        "shows": "Markdown operativo editabile",
        "model": "admin runbook blob",
        "closed_cases_with_outcome_motivation": false,
        "representation": "ops_markdown_doc",
        "api": [
          "GET/PUT /api/admin/runbook"
        ],
        "exposes": {
          "esito": false,
          "motivazione": false,
          "chiuso": false,
          "riaperto": false
        }
      },
      {
        "path": "/dossier|/dossier/:id",
        "view": "web/src/views/Dossier.vue",
        "shows": "O7 sei domande + INFERENZA + diagnosis collapsed",
        "model": "GET /api/assets/{id}/dossier via build_dossier_answer",
        "six_questions_len_asserted": 6,
        "six_questions": [
          "what",
          "where",
          "since",
          "does",
          "expected",
          "actions"
        ],
        "closed_cases_with_outcome_motivation": false,
        "representation": "answer_surface_not_case_archive",
        "api": [
          "GET /api/assets/{id}/dossier",
          "PATCH /api/assets/{id}"
        ],
        "exposes": {
          "esito": false,
          "motivazione": "partial_ignore_motivo_on_Asset.notes",
          "chiuso": false,
          "riaperto": false
        },
        "raw_data_removal_registry": {
          "source": "docs/obs-o7.md REGISTRO DI RIMOZIONE (D1)",
          "entries_count_asserted": 17,
          "nature": "documentale UI — non ledger runtime"
        }
      }
    ],
    "archivio_equivalent": {
      "dedicated_route": null,
      "len_closest_asserted": 3,
      "closest": [
        {
          "where": "/timeline Mostra archivio",
          "meaning": "filtro lifecycle eventi"
        },
        {
          "where": "/monitoring Mostra archivio",
          "meaning": "monitor archiviati"
        },
        {
          "where": "/incidents Archivia",
          "meaning": "dismiss incidente"
        }
      ]
    }
  },
  "M0_2_decision_state": {
    "zero_hits_terms": [
      "disposition",
      "closed_reason",
      "triage_state",
      "snooze"
    ],
    "len_zero_hits_asserted": 4,
    "o15_matrix_path_persistence": {
      "verdict": "NO_MATRIX_PATH_PERSISTENCE",
      "evidence": [
        "web/src/oggiDecisionMatrix.js — MATRIX_COLUMNS binding UI, no fetch",
        "web/src/components/OggiDecisionMatrix.vue — emit deepen|apply|dismiss only",
        "web/src/views/Oggi.vue — deepen=nav; apply/dismiss=effetti dominio (adopt/reject/ack) NON record colonna"
      ],
      "label_esito_ui": "Oggi.vue 'Esito' = testo prognostico oggiProblems.js, non DB disposition"
    },
    "existing_status_surfaces_len_asserted": 6,
    "existing_status_surfaces": [
      "Incident ack/dismiss/resolve",
      "Finding status/notes",
      "NameProposal reject (status_reason fisso)",
      "Suggestion approve/reject",
      "ActionRequest approve/reject",
      "domain ack fdb/egress/behavior/coverage"
    ]
  },
  "M0_3_triage": {
    "client": "web/src/triageRules.js — pure client D1–D13; No API calls (header)",
    "scoreSpecificity": "presente; NON toccato (I6)",
    "accept_persist": "api.adoptName / adoptChassisName — scrive nome, non disposition=accept",
    "dismiss_persist": "POST reject-name-proposal (+bulk) — NameProposal.status=rejected",
    "snooze_persist": false,
    "triageRules_persists": false,
    "closest_to_F9": {
      "candidate": "Oggi triage queue + matrix F-9 landing (router oggi)",
      "rank": "closest_partial",
      "gaps": [
        "Nessuna entità Case/Disposition con esito+motivazione+chiuso/riaperto",
        "Nessuno snooze",
        "Matrice non registra path scelto",
        "/actions non è decision log"
      ]
    }
  },
  "M0_4_subject_identity": {
    "stable_key_available_without_new_identity_logic": true,
    "key_shape": "(subject_type, subject_id) via subject_of / subject_ref_chassis",
    "oggi_card_key": "chassis_id on Apparati cards (oggiChassis.js chassis-name-${cid})",
    "interface_read_only": [
      "api/app/facts/resolver.py subject_of, current, history",
      "api/app/facts/registry.py subject_ref_chassis",
      "api/app/facts/chassis_facts.py list_chassis_subject_assertions"
    ],
    "stability_caveat": "DEBT-CHASSIS-SUBJECT-ID-CHURN — chassis_id cambia al regroup membership; FA orfani marcati non cancellati",
    "resolver_invocation": "none — solo lettura interfacce/docs"
  },
  "M0_5_marked_never_deleted": {
    "len_patterns_asserted": 2,
    "patterns": [
      {
        "id": "O5",
        "what": "396 supersession spurie marcate reason=o4_defect_concurrent_presence_move; mai DELETE",
        "code": [
          "scripts/o5_bonifica.py",
          "api/app/services/port_fdb.py",
          "fdb_defense discarded_moves"
        ],
        "docs": "docs/obs-o5.md; KNOWN_DEBT O4 defect"
      },
      {
        "id": "O7",
        "what": "Registro rimozione Dossier (17 voci) — audit documentale UI, non append-only runtime",
        "docs": "docs/obs-o7.md REGISTRO DI RIMOZIONE"
      }
    ],
    "broader_invariant": "FactAssertion history: superseded never deleted (test_history_never_deleted)"
  },
  "M0_6_mac_move_novelty": {
    "exists": true,
    "correct_suspicion_criterion": "NOT source=fdb; YES novelty vs baseline + true mac_move",
    "signals_len_asserted": 4,
    "signals": [
      {
        "signal": "S-A",
        "kind": "fdb_mac_new",
        "meaning": "NEW post-baseline (current senza baseline flag)"
      },
      {
        "signal": "S-B",
        "kind": "fdb_mac_move",
        "meaning": "CHANGED cross-port mac_move (defect O4 esclusi)"
      },
      {
        "signal": "S-C",
        "kind": "fdb_l2_only",
        "meaning": "solo-L2"
      },
      {
        "signal": "S-D",
        "kind": "fdb_source_stale",
        "meaning": "fonte cieca/stale"
      }
    ],
    "pipeline": "shadow.safe_shadow_port_fdb_snapshot → baseline/mac_move/left_port; read via GET /api/fdb-defense/signals",
    "debt_correction": "sostituisce criterio flawed FDB=anomalia (DEBT-O23-ANOMALY-DEFINITION-FLAWED)"
  },
  "M0_7_conflicts": {
    "endpoint": "GET /api/admin/facts/conflicts",
    "http": 200,
    "count": 0,
    "conflicts_len_asserted": 0,
    "response_shape": {
      "conflicts": "list",
      "count": "int"
    },
    "filter": "reason=conflict_review AND state=historical"
  },
  "M0_8_oggi_census": {
    "reference_session": "docs/obs-o17.md V: famiglie_matrice=10, card_apparati=14",
    "len_fdb_families_asserted": 10,
    "len_apparati_cards_asserted": 14,
    "fdb_section": {
      "anchor": "#oggi-fdb",
      "always_relevant_fields": [
        "signal S-A…S-D + priorità",
        "mac / switch:port / ruolo_porta",
        "baseline_at",
        "ODM bands I1: observed|missing_stale|deterministic|inference",
        "inference block",
        "S-D cieca (I2 narrative)",
        "discarded_moves banner (O5)"
      ],
      "i3_on_fdb": "not typical",
      "mac_move_novelty": "S-A novelty; S-B mac_move; baseline long-stable excluded from S-A"
    },
    "apparati_section": {
      "anchor": "#oggi-apparati",
      "always_relevant_fields": [
        "name_kind fact|legacy_manual|inference|absent (I1/I2)",
        "conflict vs proposta (I3)",
        "AiInferenceLabel",
        "provenienza labels",
        "ODM bands + actions",
        "data-chassis-id disposition key"
      ],
      "mac_move_on_apparati": false
    },
    "i2_formal_quintet_on_oggi": "mostly narrative (absent/cieca); formal data-i2-condition cablato su Monitoring/Plant (O21), non quintetto completo su ogni banda Oggi",
    "len_always_visible_inventory_buckets_asserted": 2
  },
  "bottom_line": {
    "f9_disposition_store_exists": false,
    "actions_is_decision_log": false,
    "o15_persists_path_choice": false,
    "nearest_building_blocks": [
      "NameProposal adopt/reject",
      "Suggestion approve/reject",
      "Incident/Finding status",
      "fdb-defense signals S-A/S-B",
      "Timeline archive filter (not case archive)"
    ],
    "correct_always_visible_criterion": "S-A/S-B novelty+mac_move + I3 conflicts + dati necessari alla via O15 — NOT edge_relation=fdb"
  }
}
```

---

## 4. P policy (integrale)

`sha256=aff1056ea0cb90d336a29a4859f9d58b4c5cef196c8354d14fc02418a89354d2` · `wc_l=243`

```markdown
# OBS-O25 — Policy ciclo di vita Oggi (F-9)

**Modalità:** sola policy scritta. Nessun codice.
**Ancoraggio:** ogni sezione cita un reperto di `docs/obs-o25-M0-discovery.json`
(`sha256=c61da0bba2e732826a89229a56f5c1c1334a1226877f86d686dd092a146b69f2`).
**Vincolo F-9 Michele:** Oggi = pannello decisioni; non minacciosi escono (non solo
collassano); Archivio/equivalente consultabile; Dossier = approfondimenti; auditabilità.

---

## P1. Stati del ciclo di vita

**Ancoraggio M0:** M0.2 (nessun `disposition`/`closed_reason`/`triage_state`/`snooze`);
M0.3 (triage = accept/reject dominio, non case store); bottom_line
`f9_disposition_store_exists=false`.

| Stato | Significato | Evento che lo determina |
|-------|-------------|-------------------------|
| `open` | Caso in Oggi; richiede scelta via O15 o resta sospetto | Comparsa evidenza (vedi P4) senza chiusura attiva |
| `closed_non_threat` | Natura non minacciosa stabilita; **uscito da Oggi**; consultabile in area chiusi | Chiusura esplicita con esito+motivazione (evento scritto) |
| `reopened` | Tornato in Oggi | Nuova evidenza materiale (P2) rispetto al fingerprint di chiusura (P5) |

Transizioni ammesse:

```
open → closed_non_threat   (chiusura esplicita)
closed_non_threat → reopened   (P2 vero)
reopened → closed_non_threat   (nuova chiusura; nuovo fingerprint)
```

Vietato: `open → deleted`; qualsiasi cancellazione di eventi di chiusura/riapertura
(M0.5 pattern «marcato mai cancellato»).

Esiti di chiusura (campo obbligatorio sull’evento, non solo sullo stato):

- `non_threat_known` — classificato non minaccioso con motivo
- `applied` — azione dominio già eseguita (adopt/ack/…) e caso non richiede più Oggi
- `not_applicable` — via NON APPLICARE con motivo; resta consultabile

Nota: questi esiti **non** coincidono con lo status Incident/Finding (M0.1) né con
ActionRequest (M0.1 `/actions`).

---

## P2. Criterio di «nuova evidenza materiale» (riapertura)

**Ancoraggio M0:** M0.6 (S-A/S-B vs baseline); M0.7 (I3 conflicts); M0.8 (tag I1/I2/I3);
correzione DEBT-O23-ANOMALY-DEFINITION-FLAWED (fonte FDB ≠ sospetto).

Una riapertura è **vera** se e solo se vale **almeno una** condizione verificabile:

1. **MAC-move / novelty (M0.6):** per la chiave del caso compare un segnale
   `fdb_mac_new` (S-A) o `fdb_mac_move` (S-B) con `(kind, mac, port_id|switch:port,
   observed_at)` **assente** dal fingerprint di chiusura (P5).
2. **Conflitto I3 (M0.7):** `GET /api/admin/facts/conflicts` restituisce una riga con
   `(fact_key, subject_type, subject_id, excl_key, value, incumbent_value)` non presente
   nel fingerprint (o `count` passa da 0 a >0 sul soggetto).
3. **Cambio di rango/valore di fatto rilevante (I5/I1):** per i campi nel fingerprint
   (nome canonicizzato, conflict flag Apparati, signal kind FDB) il valore corrente da
   API già esistenti differisce dal valore fingerprintato; la fonte ha autorità
   confrontabile via campi già esposti (`source`/`authority` su FA o campi card).
4. **Cambio condizione I2 materialmente diversa:** passaggio tra condizioni narrative
   già in card (es. da `absent`/cieca a fatto osservato, o viceversa su freschezza
   strutturale) rispetto al fingerprint — non un semplice refresh UI.

**Non** è evidenza materiale:

- stesso MAC sulla stessa porta con solo `last_seen` aggiornato senza S-A/S-B;
- `edge_relation=fdb` / `source=fdb` da soli (M0.6 + debito anomaly);
- riapertura «perché sembra cambiato» senza delta fingerprint.

Falsificabile: dato fingerprint F e snapshot S, `material_new(F,S)` è predicato puro.

---

## P3. Dove vivono i casi chiusi

**Ancoraggio M0:** M0.1 `archivio_equivalent.dedicated_route=null`; `/actions` respinto
come decision log; `/timeline` archivio = lifecycle eventi; `/findings`/`/incidents` =
scope monitor/finding; Dossier = answer surface.

**Scelta:** riusare **`/timeline` come superficie di consultazione**, con un **filtro /
sezione dedicata ai soli eventi di disposizione F-9** (chiusura/riapertura), **senza
nuova rotta** in prima battuta.

Motivazione:

- già esiste «Mostra archivio» e il vocabolario di eventi letti/silenziati (M0.1);
- evita un mostro `/archivio` parallelo (F-9: riusa);
- i chiusi **non** restano in Oggi collassati (differenza O24 Topology).

Se in O26 la densità Timeline rende il filtro inutilizzabile, **allora** si valuta una
rotta dedicata — ultima opzione, con giustificazione da misura, non da preferenza.

Dossier resta il luogo degli **approfondimenti/evidenze** (sei domande), non l’archivio
delle decisioni chiuse.

---

## P4. Insieme «sempre visibile in Oggi»

**Ancoraggio M0:** M0.6, M0.7 (`count=0` al momento M0), M0.8 (10 famiglie FDB, 14
Apparati; bande ODM; signal S-A…S-D).

Indipendentemente dallo stato del caso, restano in Oggi (se presenti nei dati):

### Per ogni famiglia FDB (×10, `len_fdb_families_asserted=10`)

| Banda/campo | Perché |
|-------------|--------|
| Signal **S-A** (`fdb_mac_new`) | evento nuovo post-baseline |
| Signal **S-B** (`fdb_mac_move`) | MAC-move vero |
| Signal **S-D** (fonte cieca/stale) se attiva | limite strutturale / I2 narrativo necessario alla scelta |
| Campi strettamente necessari alla via O15 sulla card attiva: mac, switch:port, ruolo_porta, baseline_at, priorità/regola, bande ODM observed/missing_stale/deterministic/inference | «informazioni strettamente necessarie» F-9 |
| Banner `discarded_moves` (conteggio O5) | segnale discreto di debito/interpretazione, non rumore di riga |

**Non** restano «sempre» solo perché FDB: card S-C/solo-L2 **già chiuse** come non
minacciose escono (P1), salvo P2.

### Per ogni card Apparati (×14, `len_apparati_cards_asserted=14`)

| Banda/campo | Perché |
|-------------|--------|
| `conflict` / I3 vs proposta | conflitto |
| `name_kind=absent` o divergenza I3 | scelta nome non liquidata |
| Inference esplicita + provenienza | I1 necessario alla via |
| `data-chassis-id` + campi ODM/actions della card aperta | necessaria alla scelta |

### Globali

| Voce | Perché |
|------|--------|
| Conflitti I3 da `/api/admin/facts/conflicts` se `count>0` sul soggetto | M0.7 |
| Eventi nuovi di dominio già in coda Oggi (name proposal collide/upgrade non archiviati) finché non chiusi | M0.3 |

---

## P5. Regola di deduplicazione

**Ancoraggio M0:** M0.4 chiave `(subject_type, subject_id)` / `chassis_id`; M0.6
fingerprintable signals; M0.8 card keys.

**Stesso caso** = stessa chiave soggetto:

- Apparati / nome: `("chassis", chassis_id)` se presente, altrimenti `("asset", asset_id)`
  (M0.4 `subject_ref_chassis`).
- FDB signal: chiave composta `(kind, mac, port_id)` (o switch:port stabile) — il soggetto
  «caso FDB» non è il chassis, è il segnale.

**Fingerprint di chiusura** (immutabile, scritto sull’evento di chiusura):

```
{
  "subject_key": ["chassis"|"asset"|"fdb_signal", id|composite],
  "closed_at": iso,
  "outcome": "...",
  "motivation": "...",
  "evidence": {
    "signals": [{"kind","mac","port_id","observed_at"}],
    "conflicts": [{"fact_key","subject_type","subject_id","excl_key","value","incumbent_value"}],
    "name_kind": "...",
    "conflict_flag": bool
  }
}
```

**Duplicato (resta fuori da Oggi):** stesso `subject_key` in `closed_non_threat` **e**
`material_new(fingerprint, snapshot_now) == false` (P2).

Caveat M0.4: se `chassis_id` churna (DEBT-CHASSIS-SUBJECT-ID-CHURN), il caso chiuso può
restare orfano sulla vecchia chiave — come i FA; non si «ripara» cancellando; si può
riaprire solo se P2 matcha sulla nuova chiave con evidenza nuova (non silenzioso merge).

---

## P6. Auditabilità

**Ancoraggio M0:** M0.5 O5 mark-never-delete; O7 registro documentale; invariante
`FactAssertion` history never deleted.

Regole:

1. **Nessuna cancellazione** di eventi di disposizione. Mai.
2. Ogni chiusura/riapertura è un **evento append-only** (F-7: l’evidenza si scrive; lo
   stato `open|closed_non_threat|reopened` si **deriva** dall’ultimo evento per chiave).
3. Pattern O5: se un evento risulta spurio, si **marca** (`reason`/`superseded`), non si
   DELETE.
4. Il registro O7 resta modello per «cosa non mostrare in UI» documentato; la disposizione
   F-9 è runtime, non solo markdown.

---

## P7. Superficie di impatto tecnico

**Ancoraggio M0:** M0.1–M0.4; O15 non persiste path (M0.2); nessun disposition store
(M0.2/M0.3).

### (a) Solo frontend, dati/rotte esistenti

- Filtrare da Oggi le card il cui `subject_key` risulta `closed_non_threat` **se** lo
  store disposizione è già leggibile.
- Deep-link a Timeline filtrata / Dossier per consultazione.
- Segnale discreto (conteggio chiusi oggi / link Archivio-equivalente) senza crescere a
  mostro (principio UX O22).
- **Limite:** senza store persistente, un filtro solo-localStorage **non** soddisfa
  auditabilità multi-dispositivo né P6 — quindi (a) da solo non chiude F-9.

### (b) Additivo (endpoint/tabella nuovi) senza toccare il resolver

- Tabella/eventi `CaseDispositionEvent` (o nome equivalente) con fingerprint + esito +
  motivazione + timestamps.
- Endpoint write: chiudi / (riapertura è derivata da job o da lettura a richiesta che
  valuta P2).
- Endpoint read: lista per chiave; Timeline (o FE) li mostra in sezione Archivio-equivalente.
- Lettura **read-only** di: `/api/fdb-defense/signals`, `/api/admin/facts/conflicts`,
  payload Oggi già aggregati, eventuali `FactAssertion` via API admin esistenti —
  **senza** modificare `api/app/facts/` né supersessione.

### (c) Componenti che richiederebbero di modificare il resolver o riaprire T7/OBS-CURRENCY

**Insieme (c): vuoto per l’MVP policy qui descritto.**

Motivazione fattuale: la disposizione è un **overlay** su chiavi già esposte
(`chassis_id`, signal composite) e su API già esistenti; non richiede cambiare
`subject_of`, supersession, o currency gate.

**Fuori MVP / decisione separata (NON in (c) come blocco, ma nominata):** rendere
`chassis_id` immutabile al regroup (`DEBT-CHASSIS-SUBJECT-ID-CHURN`) — toccherebbe
identità/currency. **Non è precondizione** per costruire (b)+(a) in O26; è un rischio di
orfani già accettato per i FA (M0.4/M0.5).

**GATE P:** (c) vuoto → D non bloccata da impossibilità tecnica sul resolver; D resta
**rimandata a O26** per scelta di sequenza (revisione policy P2/P5 = rischio, non solo
tecnica).

---

## P8. Cosa non verrà fatto in questa ondata

- Nessuna modifica a `Oggi.vue`, `Topology.vue`, router, modelli, `api/app/facts/`.
- Nessun bump VERSION, nessun deploy, nessuna nuova tabella/endpoint creati.
- Nessuna modifica alla semantica matrice O15, canvas SVG, `--inference*`.
- Solo artefatti: `docs/obs-o25-M0-discovery.json` (+ digest), questo file, report O25.
```

---

## 5. P7(c)

**Vuoto.** Nessuna componente MVP richiede di modificare il resolver o riaprire T7/OBS-CURRENCY.
Overlay disposizione + lettura RO API esistenti (M0 → P7).

Nessuna domanda bloccante per Michele su (c). Restano da **revisionare** (rischio, non impossibilità):
P2 (evidenza materiale) e P5 (fingerprint/dedup) prima di D in O26.

---

## 6. Sequenza D

P7(c) vuoto: **D è progettabile in O26** previa revisione policy. Questa ondata si chiude senza D per disciplina di sequenza (non per blocco tecnico sul resolver).

---

## 7. Hash commit principale

`4571e459d45eda58049be1246cfa3c2d74198689` — commit che contiene M0+P (codice documentale dell’ondata). Per regola 0.2, l’eventuale commit successivo di sola pubblicazione di questo report non si autocertifica.

---

## 8. Cosa NON hai fatto

- Nessuna modifica a Oggi.vue / Topology / router / modelli / `api/app/facts/`.
- Nessun bump VERSION, nessun deploy, nessuna tabella/endpoint creati.
- Nessuna misura di altezza, nessuno script one-shot in repo.
- Nessun tocco a T7, OBS-CURRENCY, FA251, `_w4a_measure.py`, favicon, egress, `--inference*`, matrice O15 semantica, canvas SVG, visibilità obs-exchange.
