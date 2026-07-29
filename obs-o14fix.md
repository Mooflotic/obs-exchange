# OBS-UX O14-FIX — token veri in matrix.css, mint TTL breve (0.10.84)

Ramo `feature/obs-currency` @ `a666859` + WT.  
**STOP per review.** Nessun push/merge/tag. FA 251 intatto.

**VERSION:** 0.10.84 · deploy `web`  
**PREVISIONI:** [`obs-o14fix-PREVISIONI.md`](obs-o14fix-PREVISIONI.md)  
**Diff:** `obs-o14fix-token.diff.txt`, `obs-o14fix-mint.diff.txt`  
**Mint:** [`obs-session-mint.md`](obs-session-mint.md)

**Provenienza catture (harness):**  
`catture autenticate via session mint, scadenza 180s (fonte run harness 36s×5), token non pubblicato`

---

## PREVISIONI → OSSERVATI

| id | previsione | osservato | scarto |
|----|------------|-----------|--------|
| Literal fuori custom property | 30 occ / 18 valori | **30→0** in regole; valori in `--*` | nessuno |
| Allowlist | 16→16 | **16→16** | nessuno |
| Run harness | 36 s | **36 s** (dossier×3 bp) | nessuno |
| Mint TTL | 180 s | **180 s** enforced + in provenienza | nessuno |
| Deploy | sì web 0.10.84 | **sì** | nessuno |

---

## E — Token file = solo token

### Enumerazione pre-fix (literal in regole)

30 occorrenze / 18 valori unici. Tra cui i 9 O14 spostati in classi:

| valore | classe (es.) | ruolo | token assegnato |
|--------|--------------|-------|-----------------|
| `#c4a0ff` | `.obs-inference-fg` / well / tag / spin | testo AI brillante | `--inference-fg` |
| `#c4b0e8` | `.obs-inference-fg-soft` | testo AI soft (dossier tag) | `--inference-fg-soft` |
| `#6b4aa8` | `.obs-inference-edge` / well / tag / spin | bordo AI | `--inference-edge` |
| `#1a1228` | `.obs-inference-well` | sfondo pozzo AI | `--inference-well-bg` |
| `#c4b5fd` | `.obs-inference-badge` | testo badge infer | `--inference-badge-fg` |
| `#8b7cf7` | `.obs-inference-badge` | tinta badge infer | `--inference-badge` |
| `#9b82e8` | `.obs-inference-ap` | bordo AP (≠ AI) | `--ap-border` |
| `#775fbd` | `.obs-inference-group` | bordo group | `--group-border` |
| `#131323` | `.obs-inference-group` | sfondo group | `--group-bg` |
| `#6a5520` | `.badge.warn/new/…` | bordo badge attenzione | `--badge-warn-border` |
| `#803333` | `.badge.danger/down` | bordo badge pericolo | `--badge-danger-border` |
| `rgba(230,195,92,0.45)` | `.callout.warn`, `.topo-node.critical` | anello attenzione | `--attn-ring` |
| `rgba(0,0,0,0.25)` | sticky action col | ombra sticky | `--shadow-sticky-action` |
| `rgba(0,0,0,0.45)` | `.drawer-backdrop` | overlay drawer | `--drawer-backdrop` |
| `rgba(0,0,0,0.5)` | `.drawer` | ombra drawer | `--drawer-shadow` |
| `rgba(0,0,0,0.55)` | helptip | ombra helptip | `--helptip-shadow` |
| `rgba(255,107,107,0.35)` | `.spark i.d` | glow spark down | `--spark-down-glow` |
| `rgba(0,0,0,0.05)` | `.scanline` | striscia scanline | `--scanline-stripe` |

AI e AP **non unificati**. Nessun hue nuovo. Valori identici.

### Gate indurito

`matrix.css` scansionato: hex/rgb ammessi **solo** in `--nome: valore`. Self-test: inject in regola **visto fallire**, remove **passa**.

### Allowlist: 16 → 16

Nessuna voce Vue caduta in questa ondata. Motivazioni scritte invariate (residue non-AI).

**Voci cadute in O14 (storico) — esito ora dichiarato:**

| voce | O14 | O14-FIX |
|------|-----|---------|
| AiInferenceLabel, AssetDecide, TopologyBranch, VisualBadge, Topology | **trasferite** (literal in classi matrix.css) | **risolte** (custom property + `var()`) |

### Debito contrasto

`DEBT-INFERENCE-EDGE-CONTRAST`: `--inference-edge` `#6b4aa8` su `--bg-1` = **2.609:1** (< 3:1 WCAG 2.1 AA UI). Preesistente, invariato, non corretto qui.

---

## F — Mint a vita breve

| | |
|--|--|
| Parametro | `CAPTURE_MINT_TTL_SEC` default **180** (solo harness) |
| Fonte | run misurata **36 s** × 5 |
| `SESSION_HOURS` | **non toccato** |
| Enforcement | età `mtime` > TTL → mint rifiutato |
| Cleanup | sì, a fine cattura |
| Path | `/tmp/obs_session_mint.txt` + `.gitignore` |

---

## Prove deploy

| asset | sha256 |
|-------|--------|
| JS `index-CeoI_123.js` | `ce0baefd97e54f7c75f205a08f6ffa70d493d49f9cb0668d51a7ce8894aa80f5` — `obs-o14fix-marker` |
| CSS `index-DdTKFMOH.css` | `5e69d22ce0bbda9fc96a964a07d55a63d44fabf8eb93433c8b7a0949e3370c76` — `--inference-fg`, `--ap-border`, `--group-bg` presenti |
| VERSION NAS | `0.10.84` |

---

## Screenshot (privacy-safe all’origine)

| file | W×H | sha256 |
|------|-----|--------|
| `obs-o14fix-dossier-1280.png` | 1280×900 | `5466acaa…f7c10a` |
| `obs-o14fix-dossier-768.png` | 768×900 | `87a65616…16d33d` |
| `obs-o14fix-dossier-390.png` | 390×3304 | `78619473…858d66` |
| `*-prima-*` / `*-dopo-*` | idem | **identici** per breakpoint (T3) |

`o9_png_assert.py --pair` 1280 vs 390: **PASS**.

---

## Gate — output INTEGRALE

### Currency repo

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

### Currency NAS

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

Repo: vuoto. NAS: vuoto.

### Color + self-test (repo = NAS)

```
PASS: no hard-coded color literals outside allowlist; matrix.css decls-only
  token_file=assets/matrix.css (literals only in --custom-property decls)
  allowlist_count=16
SELFTEST vue inject detected: (2, '#ff00aa', '.x { color: #ff00aa; /* O13D_COLOR_GATE_INJECT */ }')
SELFTEST matrix rule inject detected: (944, '#ff00aa', '.o14fix-gate-inject { color: #ff00aa; /* O14FIX_COLOR_GATE_INJECT */ }')
SELFTEST PASS: inject fails (vue+matrix rule), remove passes
```

### Drift

`scripts/` NAS − locale = **1**: `scripts/_w4a_measure.py`.

### Breaker / DB

| metrica | valore |
|---------|--------|
| egress_observations | 1735 |
| fact_assertions | 2474 |
| zeek_behavior_evidence | 650 |
| DB MiB | **1805.1** |
| Tetti | non alzati |

FA 251: **non letto, non toccato**.

### Test mirati

`test_o14_session_mint.py` + `test_o13d_soppressione.py`: **8 passed**.

---

## Criteri di accettazione

| criterio | esito |
|----------|-------|
| matrix.css solo token in regole | **PASS** |
| nomi semantici; AI≠AP | **PASS** |
| gate scansiona matrix + visto fallire | **PASS** |
| allowlist 16 motivate; O14 cadute trasferite→risolte | **PASS** |
| PNG sha prima=dopo | **PASS** |
| mint TTL proprio 180s da misura 36s | **PASS** |
| no SESSION_HOURS/password/store/endpoint | **PASS** |
| gate PASS, drift=1, breaker, DB, FA251, no push | **PASS** |

## Criteri di fallimento

Nessuno attivato.

**STOP.**
