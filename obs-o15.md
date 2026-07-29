# OBS-UX O15 — matrice decisionale a tre percorsi in Oggi (0.10.85)

Ramo `feature/obs-currency` @ `a666859` + WT O14/O14-FIX preservato.  
**STOP per review.** Nessun commit/push/merge/tag.

**VERSION:** 0.10.85 (deploy `web` ×2)  
**PREVISIONI:** [`obs-o15-PREVISIONI.md`](obs-o15-PREVISIONI.md)  
**Diff:** `obs-o15-matrice.diff.txt`, `obs-o15-oggi.diff.txt`  
**Provenienza mint (harness):** `catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato`

---

## G1 — Classificazione famiglie (dal codice)

| famiglia | builder | azioni → endpoint | esito | motivo |
|----------|---------|-------------------|-------|--------|
| `proposta_nome` | `buildTriageRows` (`triageRules.js`) → sezioni Proposte/Da verificare in `Oggi.vue` | deepen→router dossier/plant/topology; Adotta→`api.adoptName` / `adoptChassisName`; Ignora→`api.rejectNameProposal` | **decisionale** se `showAdoptButton` | tre vie reali |
| `chassis_nome` | `buildChassisNameCards` (`oggiChassis.js`) | Dossier; Adotta/Conferma/Correggi→`adoptChassisName`/`renameChassis`; Tieni manuale→`rejectNameProposal` | **decisionale solo con `tieni_manuale`** | senza dismiss → layout azioni dirette (F-9) |
| `move` | `moveSuggestions` API + `moveSuggestionFields` | deepen; Conferma→`approveSuggestion`; Rifiuta→`rejectSuggestion` | **decisionale** | tre vie |
| FDB S-A…S-D / P6 | `api.fdbDefenseSignals` + `fdbDefenseFields` | deepen→plant/dossier; Riconosci→`fdbDefenseAck(acknowledge)`; Ignora→`fdbDefenseAck(ignore)` | **decisionale solo con acknowledge+ignore** | S-D / senza ignore → informative |
| behavior B-C/B-I | `behaviorSignals` | dossier/ack | **informativa** | manca apply distinto |
| egress E-N | `egressSignals` | dossier/ack | **informativa** | manca apply distinto |
| coverage | `coverageReport` | plant/ack | **informativa** | manca apply di fatto |
| conflitti R-H | `factConflicts` | solo Dossier | **informativa** | una via |
| `device_nuovo` / monitor | liste in `Oggi.vue` | dossier/ignora/silenzia | **informativa** | non tre alternative |

Rumore nome: resta lista compatta (archivia), non matrice.

---

## G2 — Simboli (unico modulo)

Modulo: `web/src/oggiDecisionMatrix.js` — `SYMBOL_LEGEND` + `symbolsForEvidence(ev)`.

| | APPROFONDISCI | APPLICA | NON APPLICARE |
|--|---------------|---------|---------------|
| **+** | sostiene: c’è qualcosa di verificabile | sostiene adotta/conferma/correggi | sostiene ignora/rifiuta/archivia |
| **–** | contraddice: fatto già saldo | contraddice applicazione | contraddice il non applicare |
| **?** | insufficiente | insufficiente | insufficiente |
| **—** | non pertinente | non pertinente | non pertinente |

Derivazione da proprietà oggettive (tipo, fonte/`proposalSourceRank`, freschezza FRESHNESS, present/divergence/flags). Mai da output AI. Una riga → tre celle; `findDuplicateEvidenceIds` / test: duplicati assenti. Fonte + correntezza (vocabolario `visualVocab.FRESHNESS`) su ogni riga.

---

## G3 — Nessun verdetto implicito

Ordine colonne stabile. Pulsanti `.odm-btn` senza `.primary`. Niente score/count/forza. Sezione «Adotta consigliati» → «Proposte».

---

## G4 — Bande I1

Ordine: fatti osservati · dati mancanti/non correnti · interpretazione deterministica · **INFERENZA IA** (`--inference`). Vuote dichiarate «Nessun elemento in questa banda (I2).». Inferenza: evidenze, confidenza, limiti, azione di verifica; simboli stilizzati; degrada «nessun motore di inferenza configurato».

---

## G5 — Azioni

Tre pulsanti sotto, allineati grid 1fr×3. APPROFONDISCI → destinazione contestuale (`deepenDestinationForRows`). Payload/endpoint invariati. `confirmChassisNameWrite` (DEBT-CHASSIS-SUBJECT-ID-CHURN) ancora su rename/adopt/confirm chassis.

---

## G6 — Responsive

≤768: trasposizione per riga (evidenza + tre celle in linea). Motivazione: confronto senza nascondere alternative. Nessun carosello/tab/accordion. Test `oggiO15Responsive.test.js`.

---

## Previsioni → osservati

| id | previsione | osservato | scarto |
|----|------------|-----------|--------|
| famiglie | vedi PREVISIONI | chassis/FDB solo se tre vie | raffinato da codice (F-9) |
| forma UI | triage+move+fdb+chassis eleggibili | matrice su eleggibili; resto invariato | — |
| simboli | legenda unica | `SYMBOL_LEGEND` + `symbolsForEvidence` | — |
| responsive | trasposizione ≤768 | CSS grid areas c1 c2 c3 | — |
| queue | missing/duplicated [] | **missing=[] duplicated=[]** (118 asset) | — |
| VERSION | 0.10.85 | NAS 0.10.85 | — |

---

## Prova deploy (frontend)

| asset | sha256 | marker |
|-------|--------|--------|
| `/assets/index-w1cwSH0o.js` | `7496541e504147c534be151d3c621b4fb310976cf98c208be409ff1219d1215e` | `obs-o15-marker` True, `APPROFONDISCI` True, `NON APPLICARE` True, `decision-matrix` True |
| `/assets/index-BULonSvm.css` (build prec.) / CSS in bundle post-fix | gate color PASS | `odm-actions` in CSS |

`/api/health` non usato come prova frontend.

---

## Catture (privacy-safe all’origine, harness O9)

| file | dimensioni reali | note |
|------|------------------|------|
| `obs-o15-oggi-1280.png` | 1280×15009 | full-page; matrice + pulsanti Impianto/Riconosci/Ignora |
| `obs-o15-oggi-768.png` | 768×18200 | tre alternative visibili |
| `obs-o15-oggi-390.png` | 390×23526 | trasposizione; tre celle + tre pulsanti |
| `obs-o15-oggi-prima-{1280,768,390}.png` | 1280/768/390 ×900 | pre-deploy 0.10.84 |
| `obs-o15-oggi-dopo-*.png` | = dopo | coppia decisionale |

`o9_png_assert.py --pair` 1280↔390 e 768↔1280: **PASS** (larghezze distinte).  
Allowlist harness estesa per non anonimizzare APPROFONDISCI/APPLICA/NON APPLICARE.

---

## queueConservationCheck

```
missing []
duplicated []
assets_n 118
```

---

## Gate INTEGRALI

Vedi file:
- `docs/_o15_gate_repo_integral.txt`
- `docs/_o15_gate_nas_integral.txt`

Atteso e osservato: W8 VIOLAZIONI 0 PASS + 1 TEMP `wp_gate.py:103` DEBT-WPGATE-CURRENCY-COUNT-LOCAL; I6 vuoto; color PASS + self-test PASS.

**Drift NAS−repo scripts = 1:** `_w4a_measure.py` (solo NAS).

---

## Breaker / DB / FA 251

| voce | osservato |
|------|-----------|
| egress_observations | count 1937 |
| fact_assertions | count 2634 |
| zeek_behavior_evidence | count 656 |
| db_size | 1892810752 (sola lettura; nessun write O15) |
| tetti breaker | non alzati |
| FA 251 | presente id=251; **non letto/non modificato** |

---

## Working tree / Git

- HEAD resta `a666859`; **nessun commit/push/merge/tag**.
- O14/O14-FIX: marker, `--inference`, mint TTL 180, color gate — intatti nel WT.
- O15 aggiunto sopra.

---

## Criteri di accettazione (uno per uno)

1. Classificazione dal codice motivata — **SÌ** (tabella G1)  
2. Simboli unici + funzione dichiarata — **SÌ**  
3. Nessun verdetto implicito — **SÌ**  
4. Quattro bande + inferenza etichettata/degradata — **SÌ**  
5. Tre pulsanti allineati, endpoint invariati — **SÌ**  
6. Avviso churn chassis — **SÌ** (`confirmChassisNameWrite`)  
7. Confronto 390/768 senza nascondere — **SÌ**  
8. Conservazione coda — **SÌ** missing/duplicated []  
9. Gate PASS repo+NAS, drift=1 `_w4a`, breaker/DB/FA/WT — **SÌ**  
10. Nessun commit/push — **SÌ**

## Criteri di fallimento (dichiarati)

Colonna evidenziata / score / simbolo a mano / simbolo da AI / I2 confuso / riga senza fonte / fatti+inferenza misti / banda vuota omessa / matrice su famiglia senza 3 vie / payload cambiato / automazione / Impianto come colonna / hub nuovo / carosello / azione irraggiungibile / churn perso / queue non vuota / secondo vocabolario freschezza / P1–P7 alterata / browser_take_screenshot / PNG stessa larghezza / PII in artefatti / pytest Py3.9 / campagne / DB-boot-T7-FA251 / breaker alzato / IA a pagamento / SNMP SET / gate riassunti / drift≠1 / scoreSpecificity fuori triageRules / FactAssertion fuori facts / deploy senza marker / commit / diff monolitico — **nessuno di questi attivato** (matrice solo se eleggibile; FDB/chassis senza 3 vie restano informative).

---

## Fuori ambito annotato

- Header UI ancora mostra v0.10.82 in chrome (non VERSION O15) — non corretto in questa ondata.  
- PNG full-page molto alti (coda lunga) — accettabile per prova matrice+pulsanti.

---

## STOP

Cantiere aperto per review esterna. Non chiudere. Non aprire altre ondate. Non commit/push/merge/tag.

---
## Appendice — gate REPO INTEGRALE
```
===== W8 REPO =====
== W8 CURRENCY GATE (indurito, W8-fix2) ==
root: /Users/michelestorci/Developer/rete-palazzo/observatory
sentinelle: simbolo ORM 'FactAssertion' · tabella grezza 'fact_assertions' in chiamata SQL (text/execute) · COMBO (fact-token FactAssertion|fact_assertions|fact_key) + valore di stato quotato 'current'
scope: api/**, scripts/**, collector/**
esclusioni:
  - api/app/facts/**  (il resolver È la fonte della correntezza)
  - scripts/w8_currency_gate.py  (contiene le sentinelle/fact_key come dato)
  - scripts/w8_g8_equivalence.py  (contiene le sentinelle/fact_key come dato)
file scansionati: 203
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
===== I6 REPO =====
===== COLOR REPO =====
PASS: no hard-coded color literals outside allowlist; matrix.css decls-only
  token_file=assets/matrix.css (literals only in --custom-property decls)
  allowlist_count=16
===== COLOR SELF =====
SELFTEST vue inject detected: (2, '#ff00aa', '.x { color: #ff00aa; /* O13D_COLOR_GATE_INJECT */ }')
SELFTEST matrix rule inject detected: (944, '#ff00aa', '.o14fix-gate-inject { color: #ff00aa; /* O14FIX_COLOR_GATE_INJECT */ }')
SELFTEST PASS: inject fails (vue+matrix rule), remove passes
```

## Appendice — gate NAS INTEGRALE
```
===== VERSION =====
0.10.85
===== W8 NAS =====
== W8 CURRENCY GATE (indurito, W8-fix2) ==
root: /volume1/Docker/observatory
sentinelle: simbolo ORM 'FactAssertion' · tabella grezza 'fact_assertions' in chiamata SQL (text/execute) · COMBO (fact-token FactAssertion|fact_assertions|fact_key) + valore di stato quotato 'current'
scope: api/**, scripts/**, collector/**
esclusioni:
  - api/app/facts/**  (il resolver È la fonte della correntezza)
  - scripts/w8_currency_gate.py  (contiene le sentinelle/fact_key come dato)
  - scripts/w8_g8_equivalence.py  (contiene le sentinelle/fact_key come dato)
file scansionati: 204
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
===== I6 NAS =====
===== COLOR NAS =====
PASS: no hard-coded color literals outside allowlist; matrix.css decls-only
  token_file=assets/matrix.css (literals only in --custom-property decls)
  allowlist_count=16
===== COLOR SELF NAS =====
SELFTEST vue inject detected: (2, '#ff00aa', '.x { color: #ff00aa; /* O13D_COLOR_GATE_INJECT */ }')
SELFTEST matrix rule inject detected: (944, '#ff00aa', '.o14fix-gate-inject { color: #ff00aa; /* O14FIX_COLOR_GATE_INJECT */ }')
SELFTEST PASS: inject fails (vue+matrix rule), remove passes
===== DRIFT scripts NAS-repo =====
nas_scripts 88
===== BREAKER / DB =====
db_size 1892810752
egress_observations count 1937
fact_assertions count 2634
zeek_behavior_evidence count 656
FA251_present True id 251
```
