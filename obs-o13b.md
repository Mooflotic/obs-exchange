# OBS-EGRESS O13B — misura di decisione (sola lettura)

**VERSION prod:** 0.10.78 (invariata — nessun bump, nessun deploy)  
**Ramo:** `feature/obs-currency`  
**Natura:** **sola lettura**. Nessuna abilitazione, nessuna scrittura su DB/`.env`, nessuna tabella nuova, nessun ingest.

FA 251 intatto. Nessun merge su main. `scripts/_w4a_measure.py` non toccato. Nessun IP di destinazione / hostname / SNI in questo artefatto.

---

## PREVISIONI (dichiarate PRIMA delle misure)

| voce | previsione |
|------|------------|
| Novità giorno 3, grano riferimento `(device,dst,port,proto)` | ordine **10³–10⁴** tuple nuove/giorno |
| Grani vs tetti attuali (2 000/giorno, 20 000 totali, 50 MiB) | full G0 **oltre**; `/24` collassato e secondo livello device×giorno **sotto**; `(device,dst)` **incerto**; external-only forse ancora oltre senza collasso |
| Copertura log | ≈ **3** giorni calendario da ~72 file orari ruotati + `conn.log` corrente (corpus ≈662 MiB) |

**Nessuna scelta di grano. Nessuna proposta di tetto.**

---

## Metodo (dichiarato)

- Log: `/volume1/Docker/observatory/data/zeek` — solo file `conn.YYYY-MM-DD-*.log` dei giorni della finestra.
- DB: `data/db/observatory.db` aperto `mode=ro`.
- Dispositivo: logica `associate_ip_at` in sola lettura su `asset.iface_ip` → interface → asset → `chassis_id` se presente else `asset_id`. Associazione **certain** o **uncertain** → soggetto; **unresolved** → token anonimo stabile `u:`+`sha256(src)[:12]` (nessun IP stampato). Dichiarato: include unresolved nella cardinalità M1–M2.
- Chiavi tuple: digest interno (cardinalità esatta; collisione trascurabile).
- Privato = RFC1918 + link-local + ULA; esterno = resto.
- Byte/riga `flow_observations`: media lunghezze colonne SQLite + 24 B overhead = **436.15 B/riga** (fonte: `sqlite_column_length_avg_plus_24_overhead`; `dbstat` assente).
- Analisi su NAS via `python3 -` / `/tmp`; **nessun file** lasciato sotto `/volume1/Docker/observatory`.

### Copertura temporale reale

| giorno UTC | ruolo | file orari | note |
|------------|-------|----------:|------|
| 2026-07-26 | D1 | 20 | **bordo incompleto** (mancano 00–03 UTC); **incluso con dichiarazione** |
| 2026-07-27 | D2 | 24 | completo |
| 2026-07-28 | D3 | 24 | completo |
| 2026-07-29 | escluso | 4 | giorno corrente parziale |
| `conn.log` corrente | escluso | — | non chiuso |

Righe parse D1–D3: **517 493 / 388 511 / 559 656** (tot **1 465 660**); `PARSE_ERR=0`.  
File usati nella finestra: **68**. Corpus totale su disco (tutti i `conn*`) resta nell’ordine dichiarato in O13 (~662 MiB); il solo `conn.log` corrente è ~MiB singoli, non 662.

---

## M1 — Tasso di novità (grano G0, senza tempo)

G0 = `(dispositivo, dst_ip, porta, proto)` — refresh `last_seen`, non nuova riga per giorno.

| metrica | valore |
|---------|-------:|
| \|D1\| | 5 624 |
| \|D2\| | 7 596 |
| \|D3\| | 10 849 |
| \|D2 ∖ D1\| | 4 640 |
| \|D3 ∖ (D1∪D2)\| | **6 800** |
| \|D1∪D2∪D3\| | 17 064 |
| nucleo stabile (in tutti e 3 i giorni) | **0.1347** (2 298) |
| coda transitoria (in un solo giorno) | **0.7242** (12 357) |

Curva cumulativa: **5 624 → 10 264 → 17 064** (dopo D1, D1∪D2, D1∪D2∪D3).

**Asintoto:** non stimabile — solo 3 giorni di dati; **nessuna estrapolazione**.

---

## M2 — Cardinalità sotto grani alternativi (stessa finestra)

| grano | cum 3d | nuove giorno 3 | \|D1\| | \|D2\| | \|D3\| |
|-------|-------:|---------------:|------:|------:|------:|
| G0 `(dev,dst,port,proto)` | 17 064 | 6 800 | 5 624 | 7 596 | 10 849 |
| G1 `(dev,dst)` | 6 413 | 939 | 4 032 | 4 094 | 3 925 |
| G2 `(dev,dst_/24,port,proto)` | 15 125 | 6 405 | 4 625 | 6 583 | 9 892 |
| G3 `(dev,dst_/24)` | 4 149 | 527 | 2 773 | 2 816 | 2 756 |
| G0_ext | 5 305 | 841 | 3 068 | 3 159 | 3 005 |
| G0_int | 11 759 | 5 959 | 2 556 | 4 437 | 7 844 |
| G1_ext | 4 670 | 697 | 2 808 | 2 874 | 2 761 |
| G1_int | 1 743 | 242 | 1 224 | 1 220 | 1 164 |
| G2_ext | 3 841 | 484 | 2 449 | 2 501 | 2 412 |
| G2_int | 11 284 | 5 921 | 2 176 | 4 082 | 7 480 |
| G3_ext | 3 259 | 361 | 2 207 | 2 243 | 2 184 |
| G3_int | 890 | 166 | 566 | 573 | 572 |

---

## M3 — Composizione

**a)** Dispositivi distinti (soggetto): **444**. Dispositivi che coprono l’80 % delle tuple G0: **19** (Pareto; nessuna destinazione nominata).

**b)** Destinazioni IP distinte: **2 533**. Prefissi `/24` (v4) o `/48` (v6): **1 233**. Indice rotazione IP/prefisso = **2.054**.

**c)** Cardinalità G0 esterna / interna: **5 305 / 11 759** → frazione card esterna **0.3109**. Volume righe conn ext/int: **103 373 / 1 362 287** → frazione righe est **0.0705**.

**d)** Associazione IP↔MAC (`associate_ip_at` RO; `valid_from` nullo/troncato → `uncertain`):

| | certain | uncertain | unresolved |
|--|--------:|----------:|-----------:|
| tuple G0 | 15 737 | 376 | 951 |
| flussi (righe conn) | 1 194 002 | 170 603 | 101 055 |

---

## M4 — Secondo livello (dispositivo × giorno)

| giorno | dispositivi distinti |
|--------|---------------------:|
| 2026-07-26 | 224 |
| 2026-07-27 | 209 |
| 2026-07-28 | 250 |
| **max** | **250** |

Ordine dell’atteso «numero di asset attivi/giorno», non delle tuple destinazione.

---

## M5 — Primo giorno, regime, insieme attivo, MiB vs tetti **attuali**

Tetti di riferimento (già in uso, **non modificati, non proposti**):  
**2 000** righe/giorno · **20 000** totali · **50 MiB**.

Assunto store: dedup+refresh su chiave senza tempo.

- `active_7d` / `active_30d`: **non misurabili** con soli 3 giorni → lower bound = cum3.
- `naive_upper_7d = cum3 + 4×new_day3`: **estrapolazione dichiarata, non misura** (solo confronto).

| grano | create D1 | new/d3 (regime) | cum3 LB | naive7* | MiB cum3 | MiB naive7* | tetto 2k/giorno | tetto 20k tot | tetto 50 MiB |
|-------|----------:|----------------:|--------:|--------:|---------:|------------:|-----------------|---------------|--------------|
| G0 | 5 624 | 6 800 | 17 064 | 44 264 | 7.10 | 18.41 | **no** (D1 e regime) | cum3 sì; naive7 no | cum3 sì |
| G1 | 4 032 | 939 | 6 413 | 10 169 | 2.67 | 4.23 | **no** su D1; **sì** a regime | sì | sì |
| G2 | 4 625 | 6 405 | 15 125 | 40 745 | 6.29 | 16.95 | **no** (D1 e regime) | cum3 sì; naive7 no | cum3 sì |
| G3 | 2 773 | 527 | 4 149 | 6 257 | 1.73 | 2.60 | **no** su D1; **sì** a regime | sì | sì |
| G0_ext | 3 068 | 841 | 5 305 | 8 669 | 2.21 | 3.61 | **no** su D1; **sì** a regime | sì | sì |
| G0_int | 2 556 | 5 959 | 11 759 | 35 595 | 4.89 | 14.81 | **no** (D1 e regime) | cum3 sì; naive7 no | cum3 sì |
| G1_ext | 2 808 | 697 | 4 670 | 7 458 | 1.94 | 3.10 | **no** su D1; **sì** a regime | sì | sì |
| G1_int | 1 224 | 242 | 1 743 | 2 711 | 0.73 | 1.13 | **sì** D1 e regime | sì | sì |
| G2_ext | 2 449 | 484 | 3 841 | 5 777 | 1.60 | 2.40 | **no** su D1; **sì** a regime | sì | sì |
| G2_int | 2 176 | 5 921 | 11 284 | 34 968 | 4.69 | 14.55 | **no** (D1 e regime) | cum3 sì; naive7 no | cum3 sì |
| G3_ext | 2 207 | 361 | 3 259 | 4 703 | 1.36 | 1.96 | **no** su D1; **sì** a regime | sì | sì |
| G3_int | 566 | 166 | 890 | 1 554 | 0.37 | 0.65 | **sì** D1 e regime | sì | sì |

\*naive7 = estrapolazione dichiarata.

---

## M6 — Costo difensivo (prosa; **nessuna scelta**)

**(a) Insieme completo delle destinazioni, con tetto proprio sul negozio flussi**  
Si possono ancora elencare host:porta:proto per dispositivo; se il tetto proprio resta basso rispetto alla novità G0 (~6 800/giorno e coda 72 % monogiorno), il breaker/retention taglia proprio le tuple che un elenco «completo» pretendeva di conservare. Si perde la garanzia di completezza storica oltre il tetto.

**(b) Sole novità rispetto a una baseline compatta**  
Si risponde a «cosa c’è di nuovo?» senza tenere navigabile l’abituale; si perde la domanda «con chi parla di solito?» e ogni buco di baseline si presenta come novità artificiale. Il nucleo stabile (~13 % in tutti e 3 i giorni) resta fuori dal segnale.

**(c) Destinazioni collassate a /24, senza host esatto**  
Si riduce la cardinalità (G3 cum3 4 149; novità 527), ma si perde «quale host nel prefisso»; G2 ( /24+porta+proto) resta costoso in novità interna (~5 921/giorno), quindi collassare il solo indirizzo non elimina da solo il volume se porta/proto restano nella chiave.

---

## OSSERVATI vs previsioni

| previsione | osservato | scarto |
|------------|-----------|--------|
| novità G0 d3 ∈ 10³–10⁴ | **6 800** | ordine confermato |
| G0 oltre tetti | viola **2k/giorno** (D1 e regime); cum3 17 064 < 20k; MiB cum3 < 50 | day sì; tot/MiB a 3d ancora sotto (7d non misura) |
| /24 under | **G3** regime under 2k; **G2** ancora viola regime | solo collasso senza porta under a regime |
| device×giorno under | max **250** | confermato |
| `(dev,dst)` incerto | G1 regime 939 under; **D1=4 032 viola 2k** | empirico: regime ok, primo giorno no |
| external-only probabilmente over | G0_ext regime **841** under; overage da **G0_int** (5 959) | **smentita** sul day a regime per ext |
| ~3 giorni / ~72 file / ~662 MiB | 3 giorni (D1 incompleto); 68 file in finestra; corpus rotato ~662 MiB | giorni ok; non confondere `conn.log` corrente con 662 MiB |

---

## Controlli permanenti

### Dimensione DB

| | byte |
|--|-----:|
| prima misura | 1 892 810 752 |
| dopo misura | 1 892 810 752 |
| identici | **sì** |

(Conteggi riga `fact_assertions` possono muoversi per ingest live parallelo non O13B; la size file è rimasta identica. O13B non ha scritto.)

### Breaker (osservato RO via api container)

```json
{"rows_total": 1059, "breaker_open": false, "reason": "", "bytes": 512000, "zeek_behavior_evidence_rows": 366, "shadow_breaker_open": false, "shadow_breaker_reason": ""}
```

Tetti codice invariati: 20 000 / 2 000 / 50 MiB. **Non alzati.**

### FA 251 (invariato)

`id=251` · `subject_type=chassis` · `subject_id=24` · `fact_key=asset.name` · `value_norm=LGS310C` · `source=manual` · `state=current` · `authority=100`

### Copertura `zeek_conn_flow` (osservata)

```json
{"name": "zeek_conn_flow", "enabled": false, "state": "disabilitata", "last_success_at": "2026-07-25T12:00:00Z"}
```

### Drift

| | |
|--|--:|
| repo file scansionati | 198 |
| NAS file scansionati | 199 |
| delta | **1** |
| solo NAS | `scripts/_w4a_measure.py` |
| solo repo | *(nessuno)* |

### I6

`grep -RInE 'scoreSpecificity|specificity' api/` → **vuoto**.

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

```
== W8 CURRENCY GATE (indurito, W8-FIX2) ==
root: /volume1/Docker/observatory
sentinelle: simbolo ORM 'FactAssertion' · tabella grezza 'fact_assertions' in chiamata SQL (text/execute) · COMBO (fact-token FactAssertion|fact_assertions|fact_key) + valore di stato quotato 'current'
scope: api/**, scripts/**, collector/**
esclusioni:
  - api/app/facts/**  (il resolver È la fonte della correntezza)
  - scripts/w8_currency_gate.py  (contiene le sentinelle/fact_key come dato)
  - scripts/w8_g8_equivalence.py  (contiene le sentinelle/fact_key come dato)
file scansionati: 199
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

---

## Criteri di fallimento (uno per uno)

| criterio | esito |
|----------|-------|
| scrittura DB / `.env` / abilitazione ingest | **evitato** |
| deploy o bump VERSION | **evitato** |
| tetto proposto/modificato/suggerito da Cursor | **evitato** (solo confronto) |
| grano scelto/raccomandato da Cursor | **evitato** |
| IP/hostname/SNI pubblicati | **evitato** |
| stima come misura / estrapolazione non dichiarata | **evitato** (naive7 etichettata; asintoto rifiutato) |
| gate riassunto | **evitato** (integrale sopra) |
| drift ≠ 1 o file ≠ `_w4a_measure.py` | **conforme** |
| FA 251 modificato | **no** |
| percorsi IA / API a pagamento | **no** |
| boot/backup/DB/`_w4a`/T7 | **no** |
| `zeek_conn_flow` ≠ `disabilitata` | **no** (`disabilitata`) |

---

## STOP

O13B produce solo numeri per la decisione esclusiva di Michele (grano ed eventuale tetto proprio del negozio flussi).  
Nessuna abilitazione. Cantiere aperto. Nessun merge.
