# OBS-EGRESS O13 — STOP E1 (budget volume)

**VERSION prod:** 0.10.78 (invariata — nessun bump, nessun deploy, nessun ripristino `.env`)  
**Ramo:** `feature/obs-currency`  
**Esito:** **STOP autorizzato** per E1(e): anche l’aggregato dichiarato supera il budget. **Nessun ingest abilitato.**

FA 251 intatto. Nessun merge su main. Non avviare percorsi IA. `asustor_nas_snmp` non toccato.

---

## PREVISIONI (dichiarate prima di ogni abilitazione)

| voce | previsione |
|------|------------|
| E1 conn.log /60m | ordine 10⁴ righe (misura da fare) |
| E1 conn.log /24h | ordine 10⁵–10⁶ |
| Fattore log→DB | già aggregato orario in `zeek_conn` (non 1:1) |
| Proiezione oraria attuale | ≫ 2 000 righe/giorno |
| Scelta | se day-aggregate ancora > 2 000 → **STOP, non abilitare** |
| E2 chiavi | non ripristinate se STOP E1 |
| `zeek_conn_flow` | resta `disabilitata` |
| Card E6 | 0 (nessun ingest) |
| Deploy 0.10.79 | **non** se STOP E1 |

---

## E1 — Misura reale (Cassiopea, 2026-07-29)

### a) `conn.log` produzione

| metrica | valore |
|---------|--------|
| path | `/volume1/Docker/observatory/data/zeek` |
| formato | JSON lines, campo `ts` |
| `conn.log` size | ≈ 4.1–4.3 MiB (cresce in tempo reale) |
| `conn.log` righe | ≈ 9 1xx–9 5xx |
| righe ultimi **60 min** (ts) | **18 888** |
| righe ultime **24 h** (ts) | **631 194** |
| rotazione | **oraria** (mediana Δ ≈ 3600 s); 72 file ruotati + current |
| volume tutti `conn*` | ≈ **662 MiB** |

### b) Fattore riga-log → riga-DB (dal codice, non ipotizzato)

Pipeline esistente (`collector/adapters/zeek_conn.py` → `POST /api/ingest/flows`):

1. **Collector:** aggrega in bucket **`(src, dst, dport, proto, hour_start)`**, somma byte; posta solo ore chiuse; skip se `src_ip` non risolve a esattamente 1 asset.
2. **API:** upsert su `dedup_key` (finestra `obs_dedup_window_s`, tipicamente 60 s) — con `observed_at = hour_start` il grano effettivo resta **orario**.

**Non** è 1 riga DB per riga `conn.log`.

Misura unique su ultime 24 h (filtro `ts`):

| grano | unique |
|-------|-------:|
| `(src,dst,dport,proto,hour)` | **35 841** |
| `(src,dst,dport,proto,day)` UTC | **14 499** |
| `(src,dst,dport,proto)` 24 h | **12 724** |
| linee scansionate | **638 546** |

Fattore osservato (ora chiusa esempio `conn.2026-07-29-03-00-00.log`): **19 685** conn → **1 817** bucket → ≈ **10.8** conn/bucket.

### c) Proiezione a regime

| scena | righe/giorno | MiB/giorno (@≈200 B/riga) |
|-------|-------------:|--------------------------:|
| grano **orario** (codice attuale) | **≈35 841** | ≈ **6.8** |
| grano **giorno** (aggregato E1d richiesto) | **≈14 499** | ≈ **2.8** |
| senza porta (solo dest) | non misurato — fuori dalla specifica E1d |

Retention riusabile: `obs_ttl_raw_days` = **7** (vocabolario esistente) oppure `FLOW_OBSERVATION_RETENTION_DAYS` = **30** (default API). Anche a 7 gg: steady-state ≈ 14 499×7 ≈ **101 k** righe se abilitassimo il day-aggregate — oltre il tetto totale **20 000**.

### d–e) Budget e scelta

**Budget dichiarato (tetti già in uso, non inventati):**  
≤ **2 000** righe/giorno · ≤ **50 MiB** tabella · ≤ **20 000** righe totali.

| opzione | vs budget |
|---------|-----------|
| Ingest «grezzo» orario attuale | **14× oltre** 2 000/giorno → vietato |
| Aggregato dispositivo×destinazione×porta×**giorno** | **≈14 499/giorno** → **ancora 7× oltre** 2 000/giorno |
| MiB/giorno aggregato | sotto 50 MiB/giorno — **non** salva: il vincolo che scatta è le **righe/giorno** |

**Scelta motivata:** **NON abilitare**. E1(e): anche l’aggregato supera il budget → **FERMATI**.

Stato DB attuale: **1 892 810 752** byte = **1805.125 MiB** (`DEBT-DB-SIZE-OBSERVED`).  
`flow_observations` residue: **COUNT=69 794**, `MAX(observed_at)=2026-07-25 12:00:00` (pre-blackout).

---

## Cosa NON è stato fatto (dichiarato)

- Nessuna modifica a `.env` (nessuna copia E2a)
- Nessun `FLOW_INGEST_ENABLED` / `ZEEK_PROVIDER_ENABLED` ripristinato
- Nessun deploy 0.10.79
- Nessun rollback da provare (niente da riapplicare)
- Nessun diff ingest/egress/segnale (nessun codice runtime)
- Nessuno screenshot O13
- `zeek_intel` / `zeek_dhcp_names` / IA / `asustor_nas_snmp` intatti

---

## Copertura (E7) — osservata, non dedotta

`zeek_conn_flow`: **`disabilitata`**  
- `enable_flag=flow_ingest_enabled`, `enabled=false`  
- `last_success_at=2026-07-25T12:00:00Z`  
- segnali non osservabili: destinazioni / flow_observations  

Invariato rispetto al pre-O13 (nessun ripristino).

---

## Drift (controllo permanente)

| | repo | NAS |
|--|-----:|----:|
| file scansionati | **198** | **199** |
| delta | | **+1** |

File solo NAS: **`scripts/_w4a_measure.py`** (enumerato).  
Conforme all’atteso. Non toccato.

---

## Gate — output INTEGRALE

### Repo

```
== W8 CURRENCY GATE (indurito, W8-FIX2) ==
root: /Users/michelestorci/Developer/rete-palazzo/observatory
sentinelle: simbolo ORM 'FactAssertion' · tabella grezza 'fact_assertions' in chiamata SQL (text/execute) · COMBO (fact-token FactAssertion|fact_assertions|fact_key) + valore di stato quotato 'current'
scope: api/**, scripts/**, collector/**
esclusioni:
  - api/app/facts/**  (il resolver È la fonte della correntezza)
  - scripts/w8_currency_gate.py  (contiene le sentinelle/fact_key come dato)
  - scripts/w8_g8_equivalence.py  (contiene le sentinelle/fact_key come dato)
file scansionati: 198
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

### NAS

Identico salvo `root: /volume1/Docker/observatory` e `file scansionati: 199`.  
`VIOLAZIONI: 0` · `PASS (con 1 eccezione/i temporanea/e)`.

### I6

`grep -RInE 'scoreSpecificity|specificity' api/` → **vuoto**.

---

## FA 251 (invariato)

`id=251` · `subject_type=chassis` · `subject_id=24` · `fact_key=asset.name` · `value_norm=LGS310C` · `source=manual` · `state=current` · `authority=100`

---

## OSSERVATI vs previsioni

| voce | previsto | osservato | scarto |
|------|----------|-----------|--------|
| STOP E1 se day > 2k | sì | sì (14 499) | — |
| `.env` intatto | sì | `FLOW_INGEST_ENABLED` ABSENT | — |
| `zeek_conn_flow` | `disabilitata` | `disabilitata` | — |
| deploy | no | no | — |
| drift | 1 = `_w4a` | 1 = `_w4a_measure.py` | — |

---

## Debito da registrare (scrittura)

**`DEBT-FLOW-VOLUME-OVER-BUDGET`** (alta, bloccante egress):  
conn.log ≈ 631 k righe/24 h; aggregato giorno × porta ≈ **14 499** righe/giorno vs tetto **2 000**. Per riaprire O13/egress serve un grano più grosso **deciso da Michele** (es. senza porta, campionamento, solo egress esterno, o tetto alzato con decisione esplicita — vietato alzarlo in silenzio). Annotato in `KNOWN_DEBT.md`.

---

## Criteri di fallimento (rilevanti allo STOP)

| criterio | esito |
|----------|-------|
| ingest senza misura/budget | **evitato** (STOP) |
| proiezione oltre budget e abilitato | **evitato** |
| `.env` modificato | **no** |
| allowlist ampliata | **no** |
| FA 251 | **invariato** |
| drift ≠ 1 o file ≠ `_w4a` | **conforme** |
| lavoro boot/DB/`_w4a`/T7 | **no** |

Criteri T1–T8 / E2–E8: **non applicabili** — ondata fermata a E1 prima di abilitare.

---

## Diff / screenshot

- `obs-o13-ingest.diff.txt` — **non prodotto** (nessun codice)
- `obs-o13-egress.diff.txt` — **non prodotto**
- `obs-o13-segnale.diff.txt` — **non prodotto**
- screenshot — **non prodotti**

---

## STOP

O13 non può procedere all’abilitazione flow/conn senza violare il budget dichiarato (E1).  
Attende decisione esclusiva di Michele sul grano/tetto. Cantiere aperto. Nessun merge.
