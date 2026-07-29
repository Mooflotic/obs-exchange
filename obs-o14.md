# OBS-UX O14 — token `--inference` e session mint (0.10.83)

Ramo lavoro locale `feature/obs-currency` @ `a666859` + WT.  
**STOP per review.** Nessun push/merge/tag. FA 251 intatto. obs-exchange: nessuna cancellazione / cambio visibilità.

**VERSION:** 0.10.83 (CSS/runtime web toccato → bump + deploy `web`)  
**PREVISIONI:** [`obs-o14-PREVISIONI.md`](obs-o14-PREVISIONI.md)  
**Diff:** `obs-o14-token.diff.txt`, `obs-o14-mint.diff.txt`  
**Mint:** [`obs-session-mint.md`](obs-session-mint.md)

**Provenienza catture (emessa dall’harness):**  
`catture autenticate via session mint, scadenza 168h, token non pubblicato`

---

## PREVISIONI → OSSERVATI

| id | previsione | osservato | scarto / causa |
|----|------------|-----------|----------------|
| Viola | `#9b7bd4` = `rgb(155,123,212)` | **confermato** in `AiInferenceLabel`/`Dossier` pre-O14; token `--inference: #9b7bd4` nel CSS servito | nessuno |
| Punti d’uso base | 5 occorrenze base + famiglia AI/AP | base convertito a `var(--inference)` / `rgb(from var(--inference)…)`; chrome correlato relocato in `matrix.css` (stessi hex) | nessuno |
| Allowlist | 21 → 16 | **21 → 16** | nessuno |
| Contrasto | identico | **identico** (stessi hex; PNG prima/dopo **stesso sha256**) | nessuno |
| Durata mint | `SESSION_HOURS` (default 168) | **168h** letto da `.env`; dichiarato in `CAPTURE_PROVENANCE` | nessuno |
| Deploy | sì, web | **sì** `./scripts/deploy.sh web` → 0.10.83 | nessuno |

---

## A — Token `--inference`

### Valore viola (produzione pre-O14)

| dove | valore |
|------|--------|
| `components/AiInferenceLabel.vue` border/bg `color-mix(..., #9b7bd4 …)` | `#9b7bd4` |
| `views/Dossier.vue` `.inference` / `.tag.infer` | `rgba(155, 123, 212, α)` ≡ `#9b7bd4` |

**Token:** `--inference: #9b7bd4` in `assets/matrix.css` (unico token file del color gate). Nessuna variazione di tinta/saturazione/opacità sul valore semantico.

### Punti d’uso convertiti (enumerati)

1. `AiInferenceLabel.vue` — `color-mix(..., var(--inference) …)` su bordo/sfondo blocco; tag chrome → `.obs-inference-tag-chrome`
2. `Dossier.vue` — bordo/sfondo `rgb(from var(--inference) r g b / α)`; testo tag → `.obs-inference-fg-soft`
3. `AssetDecide.vue` — `.obs-inference-well` / `.obs-inference-fg` / `.obs-inference-edge` / `.obs-inference-spin-chrome`
4. `Inventory.vue` — rimossi literal AI residui (UI AI già in `AssetDecide`)
5. `Suggestions.vue` — `sourceClass` aggiunge `.obs-inference-well`
6. `VisualBadge.vue` — `.obs-inference-badge`
7. `TopologyBranch.vue` / `Topology.vue` — AP/group → `.obs-inference-ap` / `.obs-inference-group` (hex produzione invariati in token file)

Chrome secondario già in produzione (`#c4a0ff`, `#6b4aa8`, `#1a1228`, `#c4b0e8`, `#c4b5fd`, `#8b7cf7`, `#9b82e8`, `#775fbd`, `#131323`) **relocato** in `matrix.css` (non nuovi hue).

### Allowlist color gate

| | conteggio |
|--|-----------|
| Prima | **21** |
| Dopo | **16** |

**Voci cadute (5):**  
`components/AiInferenceLabel.vue`, `components/AssetDecide.vue`, `components/TopologyBranch.vue`, `components/ui/VisualBadge.vue`, `views/Topology.vue`

Motivazioni aggiornate su Dossier/Inventory/Suggestions (residui non-AI).

### Contrasto WCAG 2.1 AA (prima ≡ dopo)

Fonte soglia: WCAG 2.1 AA (4.5:1 testo normale, 3:1 large/UI) — già in uso nel progetto.

| superficie | rapporto | AA normale | AA large/UI |
|------------|----------|------------|-------------|
| testo tag `#c4a0ff` / `--bg-1` | **8.081:1** | PASS | PASS |
| testo soft `#c4b0e8` / `--bg-1` | **8.824:1** | PASS | PASS |
| token `#9b7bd4` / `--bg-1` | **5.084:1** | PASS | PASS |
| bordo `#6b4aa8` / `--bg-1` (UI) | **2.609:1** | preesistente sotto 3:1; **invariato** | invariato |

### Non-erosione I1

`--inference` `#9b7bd4` vs `--accent` `#6bc5db` e `--ok` `#4fb477`: hue distinti. Blocco INFERENZA IA resta viola; accenti dati restano cyan/verde.

### Temi

Solo scuro fisso in `matrix.css`; `prefers-reduced-motion` presente; nessun tema chiaro/alto contrasto/stampa introdotto.

### Color gate — output INTEGRALE (repo)

```
PASS: no hard-coded color literals outside token/allowlist files
  token_files=['assets/matrix.css']
  allowlist_count=16
SELFTEST inject detected: (2, '#ff00aa', '.x { color: #ff00aa; /* O13D_COLOR_GATE_INJECT */ }')
SELFTEST PASS: inject fails, remove passes
```

### Color gate — output INTEGRALE (NAS)

```
PASS: no hard-coded color literals outside token/allowlist files
  token_files=['assets/matrix.css']
  allowlist_count=16
SELFTEST inject detected: (2, '#ff00aa', '.x { color: #ff00aa; /* O13D_COLOR_GATE_INJECT */ }')
SELFTEST PASS: inject fails, remove passes
```

---

## B — Session mint

Documentazione: [`obs-session-mint.md`](obs-session-mint.md).

| requisito | stato |
|-----------|--------|
| Solo harness cattura | **sì** — `scripts/o13dfix_capture.py`; rifiuta path mint sotto albero repo |
| Vita breve | **`SESSION_HOURS`** (osservato 168) — parametro esistente |
| Fuori dal repo | `/tmp/obs_session_mint.txt` + `.gitignore` `obs_session_mint.txt` |
| Pulizia a fine cattura | `session_mint_cleared` osservato; file assente dopo run |
| Riga provenienza | `CAPTURE_PROVENANCE	catture autenticate via session mint, scadenza 168h, token non pubblicato` |
| No password/utenti/store/endpoint | **nessuna modifica** |

`DEBT-SCREENSHOT-HARNESS-FRAGILE` aggiornato: auth formalizzata come 4ª occorrenza.

---

## Prove deploy

| asset | sha256 / nota |
|-------|----------------|
| `index.html` | `14a076530c20e22a9b07e55fd34389f551b612f420fad2ef9336579a86d27a32` |
| JS `/assets/index-CcbUj68y.js` | `337ccded59e82c09bd284525e3ac6dba57517516c4c81f4da690b441f9315aff` — `obs-o14-marker` **presente** |
| CSS `/assets/index-BgoCRvQA.css` | `b2d266debd3543acaf5f0745d5bd37fa044473efd42b72f6048ebd089894ba3f` — `--inference: #9b7bd4` **presente** |
| VERSION NAS | `0.10.83` |

**T1:** valore token servito `#9b7bd4` = literal precedente. PNG prima/dopo **identici** (stesso sha256 per breakpoint) → nessuna variazione visiva.

---

## Screenshot (privacy-safe all’origine)

Harness O9 (`o13dfix_capture.py`), scrub DOM prima dello scatto.  
Breakpoint con larghezze reali distinte (assert `--pair` 1280 vs 390 **PASS**).

| file | W×H | ruolo |
|------|-----|-------|
| `obs-o14-dossier-1280.png` | 1280×900 | dopo (= deliverable) |
| `obs-o14-dossier-768.png` | 768×900 | dopo |
| `obs-o14-dossier-390.png` | 390×3304 | dopo |
| `obs-o14-dossier-prima-{1280,768,390}.png` | idem | prima |
| `obs-o14-dossier-dopo-{1280,768,390}.png` | idem | dopo (sha = prima) |

---

## Gate obbligatori

### Currency repo — INTEGRALE

```
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
```

### Currency NAS — INTEGRALE

```
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
```

### I6

Repo: **vuoto**. NAS: **vuoto**.

### Drift

`scripts/` NAS − locale filesystem = **1** file: `scripts/_w4a_measure.py`.

### Breaker / DB

| metrica | valore |
|---------|--------|
| `egress_observations` | 1700 |
| `fact_assertions` | 2407 |
| `zeek_behavior_evidence` | 650 |
| DB MiB | **1805.1** (invariata ~1805) |
| Tetti breaker | **non alzati** |

FA 251: **non letto, non toccato**.

### Test mirati

`tests/test_o14_session_mint.py` + `tests/test_o13d_soppressione.py`: **7 passed**.  
Pytest completo / 9 failure preesistenti: **non eseguiti**.

---

## Criteri di accettazione (uno per uno)

| criterio | esito |
|----------|-------|
| `--inference` = viola produzione, no variazione | **PASS** |
| Punti d’uso enumerati e convertiti; allowlist ridotta | **PASS** (21→16, 5 cadute) |
| Contrasto identico | **PASS** |
| I1 distinto | **PASS** |
| Mint documentato, circoscritto, vita `SESSION_HOURS`, cleanup, provenienza harness | **PASS** |
| No password/utenti/store | **PASS** |
| Gate integrali PASS repo+NAS; drift=1 `_w4a`; breaker; DB | **PASS** |
| Nessun push/merge/tag | **PASS** |

## Criteri di fallimento

Nessuno attivato. In particolare: colore blocco invariato (sha PNG prima=dopo); nessun hue nuovo; allowlist non ampliata; mint non in git; nessun `browser_take_screenshot`; larghezze PNG distinte 1280≠390; nessun segreto/PII in artefatti; FA251 intatto.

---

## Fuori ambito annotato (lasciato stare)

- Bordo `#6b4aa8` su `--bg-1` resta sotto 3:1 (preesistente; non modificato).
- Login form con `ADMIN_*` da `.env` continua a poter fallire 401; mint è il metodo ufficiale.
- Viola AI/AP secondari vivono come classi in `matrix.css` (stessi hex); non introdotti token `--ai`/`--ap` distinti.

**STOP.**
