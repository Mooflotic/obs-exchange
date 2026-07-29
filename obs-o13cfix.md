# OBS-EGRESS O13C-FIX — baseline prematura (0.10.80)

Correzione chiusura baseline su `deferred==0`, criteri B2 misurati (O13B M1), switch novità distinto da ingest, emissioni su ready falso marcate e ripescabili. Ramo lavoro locale; STOP per review; nessun merge su main; FA 251 intatto; `FLOW_INGEST` / `ZEEK_PROVIDER` non toccati.

**VERSION:** 0.10.80  
**Deploy:** `./scripts/deploy.sh api web collector` + `force-recreate --no-deps collector api`  
**Diff tematici:** `obs-o13cfix-baseline.diff.txt`, `obs-o13cfix-rollback.diff.txt`

---

## PREVISIONI

| id | previsione |
|----|------------|
| B1 | baseline riaperta `in_costruzione`; `premature_baseline_ready_at_was` annotato; 246 emissioni marcate `emitted_on_invalid_baseline`, non cancellate |
| B2 | ready solo se copertura ≥3d **e** serie novità ≥3 giorni UTC completi; `deferred==0` vietato |
| B3 | rollback → meta resta, status `in_costruzione`, mai ready per assenza storia |
| Q4 | ingest cresce; card N5 = 0 finché non pronta |
| Q7 | `EGRESS_NOVELTY_SIGNALS_ENABLED=false` → 0 card; ingest indipendente `true` |
| UI | readiness mancante + conteggio invalid + nota novità sospesa; `data-o13cfix="baseline"` |
| marker | `obs-o13c-fix-marker` nel bundle JS servito |
| gate | VIOLAZIONI 0 · PASS (1 TEMP `wp_gate.py:103`) repo+NAS |
| FA251 / DB | invariati |

---

## OSSERVATI (prod post-deploy)

### Settings (booleani)

| flag | valore |
|------|--------|
| `EGRESS_INGEST_ENABLED` | **true** |
| `EGRESS_NOVELTY_SIGNALS_ENABLED` | **false** |
| `FLOW_INGEST` | non true (untouched) |
| `ZEEK_PROVIDER` | untouched |

### Baseline

| campo | valore |
|-------|--------|
| status | **in_costruzione** |
| baseline_ready | **false** |
| criteria_ready (B2) | **false** |
| coverage_days | ~0.024 (≪ 3) |
| novelty_series_have | 0 / 3 |
| premature_baseline_ready_at_was | `2026-07-29T09:59:03.948740Z` |
| forbidden_criterion | `deferred==0` |
| o13cfix_marker | `obs-o13c-fix` |

**Nota B1 race:** dopo invalidate iniziale (`10:23:22Z`), il codice O13C *pre-fix* ancora in esecuzione ha ri-chiuso ready a `10:25:05Z` con reason `ciclo completo con deferred_creates==0 — baseline ready (auto)`. Post-deploy 0.10.80: re-apply `invalidate_premature_baseline` → `in_costruzione` stabile; il path `deferred==0` **non esiste più** nel codice.

### Store (aggregati, no IP)

| scope | n |
|-------|--:|
| `_baseline` | 1 |
| `ext` | 408 |
| `int` | 252 |

### Signals

| metrica | valore |
|---------|-------:|
| cards N5 | **0** |
| novelty_signals_enabled | false |
| invalid_baseline_emissions_count | **246** |
| note | presente (copertura/serie + novità sospesa + invalid) |

### Health / bundle

| check | esito |
|-------|-------|
| `/api/health` | `{"ok":true,"version":"0.10.80"}` |
| JS | `/usr/share/nginx/html/assets/index-BLN0tvdu.js` |
| sha256 | `dc7aef48ee81ed85785d25142a5542f91a9633739a2f6cdf55f610119be60e40` |
| bytes | 442 399 |
| `obs-o13c-fix-marker` count | **1** |
| `obs-o13c-marker` count | **1** |
| `data-o13cfix` count | **2** |

### FA 251

`id=251` · `subject_type=chassis` · `subject_id=24` · `fact_key=asset.name` · `value_norm=LGS310C` · `source=manual` · `state=current` · `authority=100` — **invariato**.

### DB size

`1892810752` bytes · **1805.125 MiB** (invariato; SQLite non restringe).

### Drift organico

| metrica | n |
|---------|--:|
| `fact_assertions` total | 2219 |
| `fact_assertions` current | 212 |

---

## B1 — enumerazione emissioni invalide

- **count:** 246  
- **id range:** 327 … 584  
- **sample (10):** 327, 328, 329, 330, 331, 332, 333, 334, 335, 336  
- **all marked:** true  
- **all recoverable:** true  
- **cancellate:** 0  

Endpoint: `GET /api/egress/invalid-baseline-emissions` (aggregato id/scope/first_seen — no dst in report).

---

## Criteri B2 (fonte O13B M1)

| costante | valore | fonte |
|----------|-------:|-------|
| `MIN_BASELINE_COVERAGE_DAYS` | 3 | O13B M1 copertura reale misurata |
| `MIN_NOVELTY_SERIES_DAYS` | 3 | O13B M1 curva novità a 3 punti (non soglia sul tasso) |

`maybe_close_baseline_after_cycle` registra `deferred` solo per N3 visibilità; **non** chiude su `deferred==0`.  
`mark_baseline_ready` rifiuta se criteri non soddisfatti (`refused: true`).

---

## Errata O13C (821 vs 4292)

Annotato in `docs/obs-o13c.md` con **[Corretto in O13C-FIX]**:

- Causa dominante dello scarto volume: finestra **~1 h** / **30 175** conn vs **631 194**/day O13B (ratio ≈ **20.9**).
- **Non** hybrid key collapse come causa primaria.
- Chiusura baseline same-cycle su `deferred_creates==0` = difetto corretto qui.

Debito: `DEBT-O13C-PREMATURE-BASELINE` (KNOWN_DEBT) — chiuso in 0.10.80.

---

## Test

```
python3 -m pytest tests/test_o13cfix_baseline.py tests/test_o13c_egress.py -q --tb=short
..................                                                       [100%]
18 passed in ~1.6s
```

---

## Gate W8 — FULL (repo + NAS)

### Repo (`python3 scripts/w8_currency_gate.py`)

```
== W8 CURRENCY GATE (indurito, W8-fix2) ==
root: /Users/michelestorci/Developer/rete-palazzo/observatory
sentinelle: simbolo ORM 'FactAssertion' · tabella grezza 'fact_assertions' in chiamata SQL (text/execute) · COMBO (fact-token FactAssertion|fact_assertions|fact_key) + valore di stato quotato 'current'
scope: api/**, scripts/**, collector/**
esclusioni:
  - api/app/facts/**  (il resolver È la fonte della correntezza)
  - scripts/w8_currency_gate.py  (contiene le sentinelle/fact_key come dato)
  - scripts/w8_g8_equivalence.py  (contiene le sentinelle/fact_key come dato)
file scansionati: 201
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

### NAS (`python3 scripts/w8_currency_gate.py` su Cassiopea)

```
== W8 CURRENCY GATE (indurito, W8-fix2) ==
root: /volume1/Docker/observatory
sentinelle: simbolo ORM 'FactAssertion' · tabella grezza 'fact_assertions' in chiamata SQL (text/execute) · COMBO (fact-token FactAssertion|fact_assertions|fact_key) + valore di stato quotato 'current'
scope: api/**, scripts/**, collector/**
esclusioni:
  - api/app/facts/**  (il resolver È la fonte della correntezza)
  - scripts/w8_currency_gate.py  (contiene le sentinelle/fact_key come dato)
  - scripts/w8_g8_equivalence.py  (contiene le sentinelle/fact_key come dato)
file scansionati: 202
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

### Drift

| | |
|--|--:|
| repo_scanned | 201 |
| nas_scanned | 202 |
| NAS−repo | **1** |
| solo NAS | `scripts/_w4a_measure.py` |
| solo repo | *(nessuno)* |

### I6

`grep -RInE 'scoreSpecificity|specificity' api/` → **vuoto**.

Copia sessione (non in share): `docs/_o13cfix_gate_repo_integral.txt`, `docs/_o13cfix_gate_nas_integral.txt`.

---

## Privacy screenshot O13C (6 PNG preesistenti)

Ispezione binaria (nessun IP/host embedded) + lettura visuale:

| file | dst IP / SNI / hostname pubblico | UI LAN |
|------|----------------------------------|--------|
| `obs-o13c-oggi-{1280,768,390}.png` | **no** | MAC L2 `F0:B0:14:90:87:96` |
| `obs-o13c-dossier-{1280,768,390}.png` | **no** | IP `192.168.1.44`, MAC `A8:5E:45:12:3A:26`, nome Kraken |

Per canale pubblicato: servono versioni **redatte** (blur IP/MAC UI). Nessun dst egress/SNI da redarre nei sei PNG.

### Screenshot O13C-FIX

Harness O9 (`Page.captureScreenshot` + `dsf=1`) **non eseguito in questa sessione** (login UI non automatizzato qui). Documentato: preferire catture privacy-safe post-login manuale su `/oggi` con sezione egress `data-o13cfix=baseline` visibile.

---

## Elenco file (comportamento)

| Tema | File |
|------|------|
| B1/B2/B3 + novelty | `api/app/services/egress.py` |
| settings | `api/app/config.py`, `.env.example` |
| API | `api/app/routers/egress.py` |
| test | `tests/test_o13cfix_baseline.py`, `tests/test_o13c_egress.py` |
| UI | `web/src/views/Oggi.vue`, `web/src/api.js`, `web/src/observatoryUx.js` |
| meta | `VERSION`, `web/package.json`, `CHANGELOG.md`, `KNOWN_DEBT.md`, `obs-o13c.md` |

---

## Checklist Q1–Q7 (prod)

| id | criterio | esito |
|----|----------|-------|
| Q1 | B1 annotate + reopen | **OK** (re-apply post race old-code) |
| Q2 | finestra corta + deferred=0 → non pronta | **OK** (coverage≈0.02d, criteria_ready=false) |
| Q3 | ready solo entrambe le condizioni | **OK** in test; prod non ancora eleggibile |
| Q4 | no N5 in costruzione; ingest cresce | **OK** (cards=0; store ext+int popolato) |
| Q5 | invalid marked not deleted | **OK** (246, recoverable) |
| Q6 | rollback reopen | **OK** in test |
| Q7 | novelty off / ingest on | **OK** (settings + cards=0) |

---

## Diff tematici (share)

- `obs-o13cfix-baseline.diff.txt` — criteri B2, invalidate, refuse mark, test, VERSION/CHANGELOG/debt/errata
- `obs-o13cfix-rollback.diff.txt` — Oggi readiness/UI marker, api.js endpoint, observatoryUx, package.json

| deliverable | sha256 | wc -l | commit | URL |
|-------------|--------|------:|--------|-----|
| obs-o13cfix.md | `d3e15597757ab91c2350ea076aa8d78be30158d77ec917df465912d5f599fb45` | 388 | `pending-share` | [raw](https://raw.githubusercontent.com/Mooflotic/obs-exchange/pending-share/obs-o13cfix.md) |
| obs-o13cfix-baseline.diff.txt | `6c4ef6db7c7c7e302927d52b2dc76ac19a44fd8b50ec92768fd36e850d933811` | 2411 | `423e0c10bb2f9a442a02ff490a6cdb6559c93a8b` | [raw](https://raw.githubusercontent.com/Mooflotic/obs-exchange/423e0c10bb2f9a442a02ff490a6cdb6559c93a8b/obs-o13cfix-baseline.diff.txt) |
| obs-o13cfix-rollback.diff.txt | `9fbb6a2e68382faea93add069f055bd976128fbc0028a2607ec71547e2c5b994` | 2171 | `f89c0013abb3cf85553649e21a2f29dd72631e87` | [raw](https://raw.githubusercontent.com/Mooflotic/obs-exchange/f89c0013abb3cf85553649e21a2f29dd72631e87/obs-o13cfix-rollback.diff.txt) |
| [obs-o13c.md](https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-o13c.md) (errata) | — | — | raw |
| [obs-o13cfix-CHANGELOG.md](https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-o13cfix-CHANGELOG.md) | — | — | raw |
| [obs-o13cfix-KNOWN_DEBT.md](https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-o13cfix-KNOWN_DEBT.md) | — | — | raw |

### Screenshot O13C-FIX

Harness O9 / Playwright **non disponibile** in questa sessione (`playwright not installed`). Login UI non automatizzato. Preferire catture privacy-safe post-login manuale su `/oggi` con sezione egress `data-o13cfix=baseline`.

---

## Cosa NON è stato fatto

- Nessun raise di tetti
- Nessun ripristino `FLOW_INGEST` / `ZEEK_PROVIDER`
- Nessuna modifica a `scripts/_w4a_measure.py`
- Nessun IP destinazione in report o assert stampati
- Nessun merge su main
