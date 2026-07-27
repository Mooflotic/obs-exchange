# OBS — W8-fix · indurimento del presidio di correntezza ed esecuzione reale dei gate

Ramo `feature/obs-currency` · prod **0.10.63** (nessun bump, nessun deploy, nessun
tocco a `api/app/**` o `web/src/**`). Tutte le verifiche read-only.

Regola d'ondata rispettata: si revisiona il **diff**; previsioni **prima**, osservati
**dopo**, scarti spiegati; enumerazione per id; ogni gate accompagnato dalla **prova
che sa fallire**; nessun test indebolito/rinominato/invertito.

Cosa è stato eseguito **da me, in locale/HTTP** (osservati reali qui sotto):
gate `--selftest` e scansione repo; G8 (normale + `--mutate-probe`) su **DB
sintetico** in venv temporaneo; import-smoke; I6 grep; JSON grezzo `/api/assets/{2,109}`;
baseline via HTTP (assets, FA totale, unknown_source, breaker).
Cosa resta **handoff sul NAS** (produzione accessibile solo dal terminale di Michele):
G8 su dati reali + `--mutate-probe` reale, `wp_gate` (convergenza + regime), gate su
copia NAS (repo-vs-NAS identico), I6 sul NAS. Previsioni dichiarate in **T8**.

---

## Sintesi degli esiti (una riga per bug della review W8)

| Bug | Esito W8-fix |
|---|---|
| **B1(i)** raw SQL `fact_assertions` sfuggiva | **Chiuso** — sentinella su `fact_assertions` in `text/execute` + COMBO `state='current'`. Provato dal selftest (file 2). |
| **B1(ii)** allowlist senza conteggio riutilizzabile | **Chiuso** — allowlist `(file, snippet, N)`; N+1 = violazione; COMBO cattura `filter_by(state="current")`. Provato dal selftest (file 3 e 4). |
| **B1(iii)** scope più stretto del censimento | **Chiuso** — scope `api/** · scripts/** · collector/**`. Ha fatto emergere **10 violazioni reali** in tooling (ruling, sotto). |
| **B2/B3** G8 mai eseguito / «0 per costruzione» | **Chiuso** — G8 **eseguito**; `--mutate-probe` → **DIVERGE=1 e FAIL**: discrimina. |
| **B4** AD copiato, non rimisurato | **Rimisurato** (T7); enumerazione DB per id = handoff NAS. |
| **B5** contraddizione `?history=true` | **Chiuso** — non esiste; `DEBT-HISTORY-PATH-UNWIRED`, spec §12 + obs-w8.md corretti. |
| **B6** etichette identità errate | **Chiuso** — JSON grezzo pubblicato; etichette corrette (LGS328C = chassis 23, asset 2). |

---

## T1 — Sorgente per la review: `presentation_name_for_asset` è un wrapper?

**Risposta: wrapper del resolver CON fallback allo stato derivato — NON puro.**

`presentation_name_for_asset(db, asset)` → `chassis_canonical_presentation(db, asset)`:
- usa `current(db, "chassis", cid, "asset.name")` (il **resolver**) come nome canonico
  PRIMARIO del chassis (righe 125–136 di `name_proposal_chassis.py`);
- se il fatto è **assente** (o l'asset è singleton / chassis < 2 membri) **ripiega** sul
  nome tenuto dal membro `asset.name` — **stato derivato** (righe 137–166).

Conseguenza per G8: quando il resolver ha un valore `R`, la presentazione lo usa ⇒
`P == R` **per costruzione**. Perciò `DIVERGE` tra funzione interna e resolver sul solo
`asset.name` è **tautologicamente 0**: confermata la critica B2/B3. Correzioni applicate:
1. G8 confronta il nome anche con la **superficie consumer reale** — il campo nome di
   `GET /api/assets/{id}` (leg opzionale, T4b);
2. la **discriminazione** è dimostrata da `--mutate-probe` (T4d) e dalla leg **`os.guess`**
   (resolver vs colonna `Asset.os_guess`: store DIVERSO, confronto **non** tautologico).

Gli allegati integrali dei tre file sono in coda al report (§Allegati T1).

---

## T2 + T3 — Gate indurito e controllo negativo (`--selftest`)

### T3a — `python3 scripts/w8_currency_gate.py --selftest` (osservato reale)

```
== W8 CURRENCY GATE (indurito, W8-fix) ==
root: /var/folders/.../w8gate_selftest_XXXX
sentinelle: simbolo ORM 'FactAssertion' · tabella grezza 'fact_assertions' in chiamata SQL (text/execute) · COMBO (fact-token FactAssertion|fact_assertions|fact_key) + valore di stato quotato 'current'
scope: api/**, scripts/**, collector/**
esclusioni:
  - api/app/facts/**  (il resolver È la fonte della correntezza)
  - scripts/w8_currency_gate.py  (contiene le sentinelle/fact_key come dato)
  - scripts/w8_g8_equivalence.py  (contiene le sentinelle/fact_key come dato)
file scansionati: 4
voci allowlist: 2

ECCEZIONI GIUSTIFICATE (accounted): 1
  OK  api/app/file1_orm.py:1  (atteso 1, osservato 1)
      | class FactAssertion(Base):
      → selftest: ORM def lecita

VIOLAZIONI: 3
  FAIL api/app/file2_rawsql.py:1  (atteso 0, osservato 1)
      | stmt = text("SELECT value_norm FROM fact_assertions WHERE fact_key='asset.name' AND state='current' ORDER BY id DESC LIMIT 1")
      → COMBO fact-token + 'current' (lettura di correntezza)
  FAIL api/app/file3_filterby.py:1  (atteso 0, osservato 1)
      | row = db.scalars(select(FactAssertion).filter_by(fact_key="asset.name", state="current")).first()
      → COMBO fact-token + 'current' (lettura di correntezza)
  FAIL api/app/file4_count.py:1,2  (atteso 1, osservato 2)
      | class FactAssertion(Base):
      → CONTEGGIO: atteso 1, osservato 2 — selftest: autorizzata 1 volta

RISULTATO: FAIL

SELFTEST atteso: 3 violazioni ['file2_rawsql.py', 'file3_filterby.py', 'file4_count.py'] + 1 accounted (file1)
SELFTEST osservato: 3 violazioni ['file2_rawsql.py', 'file3_filterby.py', 'file4_count.py'] + 1 accounted
SELFTEST: PASS (il gate sa fallire)
```
Exit `0`. **Il gate sa fallire**: cattura raw SQL (B1-i), `filter_by(state="current")`
(B1-ii), e conteggio N+1 (B1-ii). File 1 (def ORM lecita) resta accounted.

### T3b — `python3 scripts/w8_currency_gate.py` sul repo reale (osservato reale)

Previsione: emergono accessi in tooling `scripts/**` invisibili prima (scope B1-iii).
Osservato: **175 file scansionati, 8 accounted, 10 violazioni, RISULTATO FAIL**.

Prime iterazioni hanno mostrato **4 falsi positivi** del gate, corretti rendendolo
preciso (non è un indebolimento: mira al selettore reale di correntezza):
- `uq_fact_assertions_current_slot` (nome dell'indice) faceva scattare il COMBO perché
  «current» era **sottostringa di un identificatore** → COMBO ora richiede `'current'`
  **quotato** come valore di stato (`state='current'`);
- `"Canonical name from fact_assertions …"` (docstring) faceva scattare la sentinella
  tabella perché conteneva la parola inglese «from» → la sentinella `fact_assertions`
  ora scatta solo dentro una **chiamata SQL** (`text(`/`.execute(`/`.exec_driver_sql(`).

**8 accounted (api/, giustificate):**
```
  OK  api/app/bootstrap.py:19           (atteso 1)  import per create_all (schema)
  OK  api/app/models.py:155             (atteso 1)  class FactAssertion(Base) — def ORM
  OK  api/app/routers/admin.py:292,311  (atteso 2)  import diagnostica read-only
  OK  api/app/routers/admin.py:295      (atteso 1)  /facts/shadow-stats COUNT righe
  OK  api/app/routers/admin.py:315      (atteso 1)  /facts/conflicts select (state='historical')
  OK  api/app/routers/admin.py:317      (atteso 1)  /facts/conflicts reason=conflict_review
  OK  api/app/routers/admin.py:318      (atteso 1)  /facts/conflicts state='historical' (≠current)
  OK  api/app/routers/admin.py:320      (atteso 1)  /facts/conflicts order_by (display)
```

**10 violazioni reali (tooling read-only, mai viste prima) — NON allowlistate:**
```
  FAIL scripts/wp_gate.py:36       from app.models import ... FactAssertion ...
  FAIL scripts/wp_gate.py:102      fat = COUNT(FactAssertion)
  FAIL scripts/wp_gate.py:103      COUNT(FactAssertion WHERE state == "current")   [COMBO]
  FAIL scripts/wp_diagnose.py:29   import FactAssertion
  FAIL scripts/wp_diagnose.py:125  fa_total = COUNT(FactAssertion)
  FAIL scripts/wp_diagnose.py:127  group_by(FactAssertion.state)
  FAIL scripts/wp_diagnose.py:232  select(FactAssertion).order_by(...).limit(15)
  FAIL scripts/wp_diagnose.py:267  select(FactAssertion.id) [now]
  FAIL scripts/wp_diagnose.py:268  select(FactAssertion.id) [baseline]
  FAIL scripts/wp_diagnose.py:273  db.get(FactAssertion, fid)
```

### Classificazione e RULING (T3 — fermata obbligatoria)

Tutte e 10 sono in **tooling read-only** (`wp_gate.py` = gate di convergenza/regime;
`wp_diagnose.py` = diagnostica W-P). **Non sono consumatori runtime** che ricalcolano
la correntezza: **contano** righe e leggono la **distribuzione di stato** per metriche
di regime — la stessa natura di `/facts/shadow-stats` (che È allowlistato). Nessuna
riga decide «qual è il valore adesso» per servire l'app.

Come da regola, **non le ho aggiunte all'allowlist**. Ruling richiesto a Michele:

- **(A) — raccomandata:** escludere il **tooling read-only di gate/diagnosi** dallo
  scope (aggiungere `scripts/wp_gate.py`, `scripts/wp_diagnose.py` a `EXCLUDE_FILES`
  con motivazione), per parità con `api/app/facts/**` (fonte) e con i due file d'ondata
  già esclusi. Principio: il tooling **misura**, non consuma correntezza a runtime.
- **(B):** allowlist per-riga (verboso, fragile a ogni refactor del tooling).
- **(C):** instradare i conteggi da un helper in `api/app/facts/` — **fuori scope**
  (toccherebbe runtime; vietato in questa ondata).

Finché non c'è ruling, **il gate reale resta FAIL** (onesto: lo scope allargato ha
rivelato che anche il tooling legge FA). Il **selftest PASS** dimostra che il gate
discrimina. Non procedo ad allowlistare né escludere di mia iniziativa.

---

## T4 — G8 eseguibile, discriminante, esteso

### T4a — import-smoke (osservato reale)
`subject_of` vive in `api/app/facts/resolver.py` (riga 44) ed è ri-esportato da
`app/facts/__init__.py`: l'import `from app.facts.resolver import current, subject_of`
è **corretto** (nessuna correzione necessaria; nessun tocco al resolver).
```
== G8 IMPORT-SMOKE ==
  OK  current
  OK  subject_of
  OK  get_settings
  OK  Asset
  OK  npc
IMPORT-SMOKE: PASS
```

### T4 b/c/d — esecuzione reale su DB sintetico (venv temporaneo, poi rimosso)

Non potendo toccare la prod da qui, ho **eseguito G8 davvero** su un DB SQLite
sintetico (3 asset: A1 con fatti `asset.name`+`os.guess` current; A2 solo stato
derivato; A3 nome vuoto) — per **dimostrare che gira e discrimina**, indipendente
dalla produzione. Nessun dato reale toccato; venv e DB rimossi a fine run.

**Normale (osservato):**
```
== G8 asset.name — consumatore: presentation_name_for_asset() [interna] ==
  RESOLVER=1 FALLBACK=1 ABSENT=1 DIVERGE=0
  RESOLVER ids: [1]
  FALLBACK: id=2 resolver=None consumatore='Bar'
  ABSENT ids: [3]
== G8 asset.name — endpoint GET /api/assets/{id} ==
  SKIP (K4): OBS_G8_BASE/OBS_G8_TOKEN non impostati; leg non esercitata a runtime.
== G8 os.guess — consumatore: Asset.os_guess [colonna derivata] ==
  RESOLVER=1 FALLBACK=0 ABSENT=2 DIVERGE=0
  RESOLVER ids: [1]
  ABSENT ids: [2, 3]
RISULTATO G8: PASS
```

**`--mutate-probe 1` (controllo negativo, osservato):**
```
== MUTATE-PROBE attivo su id=1 (sentinella di presentazione) ==
== G8 asset.name — consumatore: presentation_name_for_asset() [interna] ==
  RESOLVER=0 FALLBACK=1 ABSENT=1 DIVERGE=1
  DIVERGE: id=1 resolver='Foo' consumatore='__G8_MUTATE_SENTINEL__'
== G8 os.guess — ... DIVERGE=0
RISULTATO G8: FAIL
MUTATE-PROBE: atteso DIVERGE=1 su id=1 e FAIL — confermato
```
Exit `1`. **G8 sa fallire**: la mutazione della sola funzione di presentazione su un
id produce **DIVERGE=1 esattamente su quell'id** e RISULTATO FAIL. La leg `os.guess`
(store diverso) resta a DIVERGE=0 e mostra RESOLVER=1 → prova che il confronto legge
due fonti indipendenti e concordi (non tautologico).

### T4e — contraddizione docstring risolta
G8 è **read-only sulla TRANSAZIONE DB** (`db.rollback()` finale, nessun commit) ma è un
file **versionato** (repo + obs-exchange). La docstring ora dichiara: «mai commit» =
transazione DB, non versionamento git. Durante G8 **nessuna azione è innescata
sull'api** (solo letture): l'unico writer vivo non riceve scritture.

---

## T5 — B5: ruling su `resolver.history()`

Evidenza (grep chiamanti + elenco route in `api/app/routers/**`):
- `resolver.history()` è definito (`resolver.py:195`) ed esportato (`facts/__init__.py`)
  ma **nessun router lo importa o lo invoca**;
- gli unici «history» nei router sono estranei ai fatti: `proposal_history`
  (`assets.py`, split proposte-nome), `warning_history` (`switches.py`), history di
  stato monitor (`monitors.py`). **Nessun `?history=true` esiste.**

Ruling: il contratto «storico su richiesta esplicita» era **dichiarato ma non cablato**.
Correzioni: `obs-design-spec-025.md` §12 e `obs-w8.md` corretti; aperto
**`DEBT-HISTORY-PATH-UNWIRED`** in `KNOWN_DEBT.md`. Codice non rimosso né riclassificato
come morto (è la superficie sanzionata per lo storico, inerte finché non cablata).

---

## T6 — B6: evidenza grezza di identità (JSON, campi pertinenti)

Troncamento dichiarato: mostrati solo i campi richiesti; omessi timestamp di liveness,
`meta`, `trust_level`, `interfaces`, proposte, ecc. (non pertinenti a identità/IP).

**`GET /api/assets/2`**
```json
{ "id": 2, "display_name": "LGS328C", "name": "LGS328C",
  "chassis_id": 23, "chassis_role": "canonical",
  "chassis_canonical_name": "LGS328C", "chassis_canonical_asset_id": 2,
  "guess": "Switch Linksys", "guess_source": "oui", "os_guess": "",
  "presence_state": "present",
  "ips": ["192.168.1.2", "192.168.1.2"],
  "ip_bindings": [
    {"ip":"192.168.1.2","is_current":true,"role":"mgmt","source":"mgmt","last_seen":"2026-07-27T23:34:34.946316Z"},
    {"ip":"192.168.1.2","is_current":true,"role":"","source":"fritz","last_seen":"2026-07-18T02:55:32.435005Z"}
  ] }
```

**`GET /api/assets/109`**
```json
{ "id": 109, "display_name": "LGS328C", "name": "",
  "chassis_id": 23, "chassis_role": "interface",
  "chassis_canonical_name": "LGS328C", "chassis_canonical_asset_id": 2,
  "guess": "Switch Centrale", "guess_source": "ai", "os_guess": "",
  "presence_state": "fritz_only", "ips": [], "ip_bindings": [] }
```

**Lettura (soggetto CHASSIS del nome, esplicito):**
- «**LGS328C**» è il nome **del chassis 23**, tenuto dall'asset **2** (`chassis_role:
  canonical`, `chassis_canonical_asset_id: 2`); il guess proprio dell'asset 2 è
  «Switch Linksys» (`oui`).
- L'asset **109** è un **membro** del chassis 23 (`chassis_role: interface`): il suo
  nome **proprio è VUOTO** (`name: ""` — F-5); il «LGS328C» che vede l'utente è il
  **canonico del chassis** ereditato, **non** un nome del membro. Il suo AI guess
  proprio è «**Switch Centrale**» (`guess_source: ai`, F-10/I1).

Correzione applicata a `obs-w8.md`: la formulazione W8 «asset 109 (LGS328C, chassis 23)»
attribuiva al membro un nome che ha soggetto chassis; ora esplicitato.
Anche l'asserzione W8 «chassis 23 LGS328C è AI» era imprecisa (l'AI è il guess «Switch
Centrale» dell'asset 109; il nome LGS328C del chassis è tenuto dall'asset 2) — corretta.

Nota IP (F-15): l'asset 2 mostra due binding **entrambi `is_current: true`** sulla
stessa IP `192.168.1.2` con ruoli `mgmt` e `""` (fonti `mgmt` e `fritz`) — è la
**pre-condizione W3** nota (`DEBT-DOUBLE-CURRENT-IP`, `DEBT-IFACE-IP-CARDINALITY-ROLE`):
finché il ruolo non entra nell'`excl_key`, coesistono due «correnti» leciti. Non è
compito di W8-fix.

---

## T7 — Baseline rimisurata (B4)

Misurati **ora** (2026-07-28) via HTTP read-only:

| Metrica | Comando | Osservato | vs 0.10.63 |
|---|---|---|---|
| assets (include_historical) | `GET /api/assets?include_historical=true` → len | **151** | = |
| fact_assertions totale | `GET /api/admin/facts/shadow-stats` → `.fact_assertions` | **261** | = |
| unknown_source | idem → `.unknown_source` | **0** | = |
| breaker | idem → `.breaker_open` | **false (closed)** | = |

DB-only (query esatte per NAS — enumerazione per id come da regola):
```python
# ip_current (enumerazione id), FA current, NP, AD 24h, unknown_source
from sqlalchemy import select, func
from app.models import IpAddress, FactAssertion, NameProposal, Asset
ip_ids = sorted(r for (r,) in db.execute(select(IpAddress.id).where(IpAddress.is_current == True)).all())
fa_cur = db.scalar(select(func.count()).select_from(FactAssertion).where(FactAssertion.state=="current"))
np_tot = db.scalar(select(func.count()).select_from(NameProposal))
np_pend= db.scalar(select(func.count()).select_from(NameProposal).where(NameProposal.status=="pending"))
```
Previsioni (da 0.10.63): `ip_current` = **99** id (i 101 congelati in obs-ux3 §0 meno
{78,108}); `FA current` = **68**; `NP` totale **408** / pending **77**.
**AD (finestra mobile 24h)**: **da rimisurare ora** — per costruzione può differire dal
valore congelato in 0.10.63 (il tempo è passato): non è una regressione, va **letto
dall'output di `wp_gate` sul NAS** (T8) e, se differisce, spiegato enumerando gli id
in delta. Nota metrica: `wp_gate` conta `assets` **senza** `include_historical`; il 151
qui include gli storici — le due misure non vanno confuse.

---

## T8 — Esecuzione reale sul NAS (read-only) — previsioni + comandi (handoff)

Eseguito **da me** (locale/HTTP), osservati sopra: gate `--selftest` (PASS), gate repo
(FAIL 10, ruling), G8 normale+`--mutate-probe` su DB sintetico (PASS / FAIL atteso),
import-smoke (PASS), I6 `rg 'scoreSpecificity|specificity' api/` → **VUOTO (PASS)**.

Resta sul NAS (esegui nel terminale già aperto in `/volume1/Docker/observatory`).
**Previsioni dichiarate PRIMA:**

| Comando | Previsione |
|---|---|
| `rsync -av observatory/scripts/ …/scripts/` | trasferisce `w8_currency_gate.py`, `w8_g8_equivalence.py` aggiornati (nessun restart) |
| `python3 scripts/w8_currency_gate.py --selftest` | identico all'osservato locale: **3 violazioni + 1 accounted, SELFTEST PASS** |
| `python3 scripts/w8_currency_gate.py` (repo E NAS) | **FAIL, 10 violazioni** identiche a repo. **Se repo≠NAS → FERMARSI** (repo≠prod, difetto da dichiarare) |
| `sudo docker compose stop collector` | api resta unico writer |
| `… exec -T api python3 - < scripts/w8_g8_equivalence.py` | **DIVERGE=0** su `asset.name` e `os.guess`, **RISULTATO PASS** (nessuna azione innescata) |
| `… exec -T api python3 - < scripts/w8_g8_equivalence.py --mutate-probe <id>` | **DIVERGE=1** esatto su `<id>`, **FAIL** (usa un id con `asset.name` corrente, es. un membro del chassis 24/LGS310C manuale) |
| `… exec -T api python3 - < scripts/wp_gate.py` | **convergenza OK**, breaker closed; riporta ip_current, NP, FA current, **AD rimisurato** |
| `sudo docker compose start collector` | writer ripristinato |
| `rg 'scoreSpecificity\|specificity' api/` (sul NAS) | **VUOTO** (I6 PASS) |

Nota su `--mutate-probe` via stdin: `python3 - < file` ignora gli argv dopo `-`; se
l'invocazione con `--mutate-probe` non riceve l'id, esegui invece:
`sudo docker compose exec -T api sh -c 'cd /app && python3 scripts/w8_g8_equivalence.py --mutate-probe <id>'`
(il file è già sincronizzato in `/app/scripts` se il volume lo monta; altrimenti copialo).
Se un comando fallisce, **riporta l'errore integrale e fermati** (niente varianti).

**Dichiarazione:** durante G8 nessuna azione viene innescata sull'api — sono sole
letture; `db.rollback()` chiude senza commit.

---

## ASSERT FINALE (valori osservati; NAS = da confermare da Michele)

```
needs_apply=false · T_backup=0 · structural=0 · observations assente da sqlite_master ·
breaker=closed(osservato HTTP) · convergenza=OK(NAS, previsto) ·
currency-gate: selftest PASS (3 violazioni attese OK) · repo-scan FAIL 10 (tooling, RULING) ·
G8 DIVERGE=0 su asset.name e os.guess (DB sintetico; NAS previsto) ·
G8 mutate-probe DIVERGE=1 sull'id atteso (osservato) ·
I6 vuoto (osservato, locale) · AD rimisurato=<da wp_gate NAS> · repo-vs-NAS=<da confermare>
```
`T_total` non è un gate: si riporta e basta. **Nota di onestà:** `currency-gate` sul repo
è **FAIL** (10 violazioni di tooling), non PASS — lo scope allargato (B1-iii) ha
rivelato che anche `wp_gate`/`wp_diagnose` leggono FA. Attende **ruling** (opzione A
raccomandata). Il selftest PASS certifica che il gate discrimina.

---

## Allegati T1 — sorgente integrale (immutato; per la review)

Questi tre file **non sono modificati** da W8-fix (nessun tocco a `api/app/**`);
non compaiono quindi nel diff. Sono pubblicati qui **integralmente** come richiesto.
Simboli esportati da `app/facts/__init__.py`: `AUTHORITY_RANK`, `FACT_REGISTRY`,
`get_fact_spec`, `apply_observation`, `canonical_name_for_entity`, **`current`**,
`current_map`, **`history`**, **`subject_of`**.

### `api/app/facts/resolver.py`

```python
"""Single resolver for fact currency — R-A..R-H live here only.

Invariant (W4b.0.b): the fact store grows by DISTINCT CHANGE (or distinct
divergence), never by repeated observation. Refresh and repeated weak evidence
update last_seen_at / occurrence counters — they do not insert new rows.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.facts.registry import (
    authority_for,
    default_confidence,
    get_fact_spec,
    semantic_contradiction,
)
from app.models import Asset, FactAssertion, Interface, utcnow

READMISSION_COOLDOWN = timedelta(hours=4)

# R-C observability (W2 will expose per fact_key/source).
weak_evidence_count = 0
conflict_review_count = 0


@dataclass
class ApplyResult:
    action: str
    assertion: FactAssertion | None = None
    incumbent: FactAssertion | None = None
    conflict: dict[str, Any] | None = None


def _norm_value(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def subject_of(fact_key: str, entity: Any) -> tuple[str, int]:
    spec = get_fact_spec(fact_key)
    return spec.subject_ref(entity)


def _base_query(subject_type, subject_id, fact_key=None, *, state=None, excl_key=None):
    clauses = [
        FactAssertion.subject_type == subject_type,
        FactAssertion.subject_id == subject_id,
    ]
    if fact_key is not None:
        clauses.append(FactAssertion.fact_key == fact_key)
    if state is not None:
        clauses.append(FactAssertion.state == state)
    if excl_key is not None:
        clauses.append(FactAssertion.excl_key == excl_key)
    return select(FactAssertion).where(and_(*clauses))


def _incumbent_current(db, subject_type, subject_id, fact_key, excl_key):
    return db.scalars(
        _base_query(subject_type, subject_id, fact_key, state="current", excl_key=excl_key)
        .order_by(FactAssertion.id.desc()).limit(1)
    ).first()


def _related_subjects(entity):
    if isinstance(entity, Asset):
        asset = entity
    elif isinstance(entity, Interface):
        asset = entity.asset
    else:
        return []
    subjects = [("asset", int(asset.id))]
    if asset.chassis_id:
        subjects.append(("chassis", int(asset.chassis_id)))
    return subjects


def _cross_fact_incumbents(db, entity, applying_fact_key):
    """Current rows on related subjects for R-H (name vs os, etc.)."""
    seen = set()
    rows = []
    for subject_type, subject_id in _related_subjects(entity):
        for row in db.scalars(
            _base_query(subject_type, subject_id, state="current").order_by(FactAssertion.id.desc())
        ).all():
            if row.fact_key == applying_fact_key:
                continue
            key = (row.subject_type, row.subject_id, row.fact_key, row.excl_key)
            if key in seen:
                continue
            seen.add(key)
            rows.append(row)
    return rows


def current(db, subject_type, subject_id, fact_key, *, excl_key=None, apply_ttl=False):
    """R-G: absent → None (caller must declare I2).

    Without excl_key and cardinality=single with multiple current rows, this
    silently picks highest authority (DEBT-IFACE-IP-CARDINALITY-ROLE / W4b.3.3).
    Callers that need all currents must query explicitly.
    """
    spec = get_fact_spec(fact_key)
    if excl_key is not None:
        row = _incumbent_current(db, subject_type, subject_id, fact_key, excl_key)
        if row and apply_ttl:
            _maybe_stale(db, row, spec)
        return row
    rows = list(db.scalars(
        _base_query(subject_type, subject_id, fact_key, state="current")
        .order_by(FactAssertion.id.desc())
    ).all())
    if not rows:
        return None
    if spec.cardinality == "single" and len(rows) > 1:
        rows.sort(key=lambda r: (r.authority, r.id), reverse=True)
    row = rows[0]
    if apply_ttl:
        _maybe_stale(db, row, spec)
    return row


def current_map(db, subject_type, subject_ids, fact_keys):
    if not subject_ids or not fact_keys:
        return {}
    rows = db.scalars(select(FactAssertion).where(
        FactAssertion.subject_type == subject_type,
        FactAssertion.subject_id.in_(subject_ids),
        FactAssertion.fact_key.in_(fact_keys),
        FactAssertion.state == "current",
    )).all()
    grouped = {}
    for row in rows:
        grouped.setdefault((row.subject_id, row.fact_key), []).append(row)
    out = {}
    for sid in subject_ids:
        for fk in fact_keys:
            bucket = grouped.get((sid, fk))
            if not bucket:
                out[(sid, fk)] = None
                continue
            spec = get_fact_spec(fk)
            if spec.cardinality == "single" and len(bucket) > 1:
                bucket.sort(key=lambda r: (r.authority, r.id), reverse=True)
            out[(sid, fk)] = bucket[0]
    return out


def history(db, subject_type, subject_id, fact_key, *, excl_key=None):
    q = _base_query(subject_type, subject_id, fact_key, excl_key=excl_key).order_by(
        FactAssertion.valid_from.asc(), FactAssertion.id.asc(),
    )
    return list(db.scalars(q).all())


# _maybe_stale / _new_assertion / _upsert_divergence / _check_rh_conflict /
# _within_readmission_cooldown / apply_observation (R-A..R-H) /
# canonical_name_for_entity / expire_stale_facts: invariati dal deploy 0.10.63.
# Il file completo (652 righe) è nel repo; qui sopra current()/subject_of()/
# history()/current_map() + simboli esportati, come richiesto da T1.
```

### `api/app/services/name_proposal_chassis.py` (integrale, 279 righe)

```python
"""W4a — chassis-scoped name proposal generation guards (provenance + subject only)."""

from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.facts.registry import AUTHORITY_RANK, authority_for
from app.models import Asset, NameProposal

MANUAL_AUTHORITY = AUTHORITY_RANK["manual"]


def asset_name_authority(asset: Asset) -> Optional[int]:
    """Return I5 authority rank of asset.name, or None if absent/unknown (I2)."""
    name = (asset.name or "").strip()
    if not name:
        return None
    meta = dict(asset.meta or {})
    overrides = {str(x) for x in (meta.get("manual_overrides") or [])}
    if "name" in overrides or "nome" in overrides:
        return MANUAL_AUTHORITY
    fs = (meta.get("field_sources") or {}).get("name") or {}
    if isinstance(fs, str):
        src = fs.lower().strip()
    else:
        src = str(fs.get("source") or "").lower().strip()
    if src.startswith("manual"):
        return MANUAL_AUTHORITY
    if not src:
        return None
    token = src.split()[0].split("(")[0].strip()
    if token == "manual":
        return MANUAL_AUTHORITY
    return authority_for(token)


def chassis_members(db: Session, chassis_id: int) -> list[Asset]:
    return list(
        db.scalars(
            select(Asset)
            .options(joinedload(Asset.interfaces), joinedload(Asset.name_proposals))
            .where(Asset.chassis_id == int(chassis_id))
        ).unique().all()
    )


def chassis_manual_name(db: Session, chassis_id: int) -> Optional[str]:
    """Canonical manual name: prefer fact_assertions (W4c.1), else member meta."""
    from app.facts.resolver import current

    row = current(db, "chassis", int(chassis_id), "asset.name")
    if row is not None and (row.source or "").lower() == "manual" and (row.value_norm or "").strip():
        return row.value_norm.strip()
    best: Optional[str] = None
    for member in chassis_members(db, chassis_id):
        auth = asset_name_authority(member)
        if auth is not None and auth >= MANUAL_AUTHORITY:
            name = (member.name or "").strip()
            if name:
                return name
            best = best or name
    return best


def chassis_has_manual_name(db: Session, chassis_id: int) -> bool:
    return bool(chassis_manual_name(db, chassis_id))


def chassis_member_count(db: Session, chassis_id: int | None) -> int:
    if not chassis_id:
        return 0
    return int(db.scalar(
        select(func.count()).select_from(Asset).where(Asset.chassis_id == int(chassis_id))
    ) or 0)


def proposal_actionability(db: Session, asset: Asset) -> tuple[bool, str]:
    """Whether adopt/rename is available on this asset row (W4b.2.4: chassis subject)."""
    cid = asset.chassis_id
    if cid is not None:
        return False, "chassis_multi_nic_adopt_blocked"
    return True, ""


def chassis_canonical_presentation(db: Session, asset: Asset) -> dict[str, Any]:
    """Sibling presentation: one apparato name; members are interfaces (W4c.1).

    Canonical name from fact_assertions (subject=chassis) when present; else
    member-held name for presentation only (I2 for authority).
    """
    from app.facts.resolver import current

    cid = asset.chassis_id
    if not cid:
        return {"chassis_role": None, "chassis_canonical_name": None, "chassis_canonical_asset_id": None}
    members = chassis_members(db, cid)
    if len(members) < 2:
        return {"chassis_role": None, "chassis_canonical_name": None, "chassis_canonical_asset_id": None}

    fact = current(db, "chassis", int(cid), "asset.name")     # ← RESOLVER (primario)
    fact_name = (fact.value_norm or "").strip() if fact is not None else ""

    named = [m for m in members if (m.name or "").strip()]
    manual_named = [m for m in named if (asset_name_authority(m) or 0) >= MANUAL_AUTHORITY]

    if fact_name:
        matching = [m for m in members if (m.name or "").strip() == fact_name]
        pool = matching or members
        canon_name = fact_name                                # resolver vince
    else:
        pool = manual_named or named
        if not pool:
            return {"chassis_role": "interface", "chassis_canonical_name": None, "chassis_canonical_asset_id": None}
        canon_name = (sorted(pool, key=lambda m: (m.id or 0))[0].name or "").strip() or None  # ← fallback stato derivato

    canon_asset = sorted(pool, key=lambda m: (m.id or 0))[0]
    role = "canonical" if asset.id == canon_asset.id else "interface"
    return {"chassis_role": role, "chassis_canonical_name": canon_name, "chassis_canonical_asset_id": canon_asset.id}


def presentation_name_for_asset(db: Session, asset: Asset) -> Optional[str]:
    """W4d.1.3 — user-facing apparato name (chassis canon when present).

    Returns None when absent (I2: never "" as a stand-in for missing).
    """
    pres = chassis_canonical_presentation(db, asset)
    canon = (pres.get("chassis_canonical_name") or "").strip()
    if canon:
        return canon
    own = (asset.name or "").strip()                          # ← fallback singleton
    return own or None


def should_suppress_proposal(db: Session, *, asset: Asset, source: str, value: str) -> tuple[bool, str]:
    """Generation gate: provenance + chassis subject (I6 — no name scoring in Python)."""
    text = (value or "").strip()
    if not text:
        return True, "empty"
    src = (source or "").strip().lower()
    prop_auth = authority_for(src)
    cid = asset.chassis_id
    if cid is not None and chassis_has_manual_name(db, cid):
        if prop_auth < MANUAL_AUTHORITY:
            return True, "chassis_manual_blocks_weaker"
    if cid is not None:
        member_ids = [m.id for m in chassis_members(db, cid)]
        if member_ids:
            existing = db.scalars(select(NameProposal).where(
                NameProposal.asset_id.in_(member_ids),
                NameProposal.status == "pending",
                NameProposal.value == text[:255],
            )).first()
            if existing is not None:
                return True, "chassis_value_dedup"
    return False, ""


def reconcile_chassis_name_proposal_suppression(db: Session) -> dict[str, int]:
    """Delete set A (manual chassis + weaker) and B extras (dedup). Idempotent.

    Rows are removed (not merely archived) so ``name_proposals`` count reflects
    the cleaned operational queue — W4a.3 delta gate.
    """
    removed_a = 0
    removed_b = 0
    pending = list(db.scalars(select(NameProposal).where(NameProposal.status == "pending")).all())
    assets = {a.id: a for a in db.scalars(select(Asset)).all()}
    to_delete: list[NameProposal] = []

    for prop in pending:  # Set A
        asset = assets.get(prop.asset_id)
        if not asset or not asset.chassis_id:
            continue
        if not chassis_has_manual_name(db, asset.chassis_id):
            continue
        if authority_for(prop.source) >= MANUAL_AUTHORITY:
            continue
        to_delete.append(prop)
        removed_a += 1

    delete_ids = {p.id for p in to_delete}
    buckets: dict[tuple[int, str], list[NameProposal]] = {}
    for prop in pending:  # Set B extras: keep highest id per (chassis, value)
        if prop.id in delete_ids:
            continue
        asset = assets.get(prop.asset_id)
        if not asset or not asset.chassis_id:
            continue
        key = (int(asset.chassis_id), (prop.value or "").strip().casefold())
        buckets.setdefault(key, []).append(prop)
    for _key, group in buckets.items():
        if len(group) < 2:
            continue
        keep = max(group, key=lambda p: p.id or 0)
        for prop in group:
            if prop.id == keep.id or prop.id in delete_ids:
                continue
            to_delete.append(prop)
            delete_ids.add(prop.id)
            removed_b += 1

    for prop in db.scalars(select(NameProposal).where(
        NameProposal.status_reason.in_(("w4a_chassis_manual_blocks_weaker", "w4a_chassis_value_dedup"))
    )).all():
        if prop.id not in delete_ids:
            to_delete.append(prop)
            delete_ids.add(prop.id)
            if "dedup" in (prop.status_reason or ""):
                removed_b += 1
            else:
                removed_a += 1

    for prop in to_delete:
        db.delete(prop)
    return {"archived_a": removed_a, "archived_b": removed_b}
```

### `api/app/services/chassis_rename.py` (integrale, 277 righe)

```python
"""W4b/W4c — chassis-level rename/adopt + one-shot LGS310C mark helper.

W4c.1: canonical name lives ONLY in fact_assertions (asset.name, subject=chassis).
Rename does NOT copy the name onto every member or mark them manual.
"""

from __future__ import annotations

from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.facts.resolver import apply_observation, current
from app.models import Asset, AuditLog, Chassis, NameProposal, utcnow
from app.services.name_proposal_chassis import chassis_members


class ChassisRenameError(Exception):
    def __init__(self, code: str, message: str, *, chassis_id: int | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.chassis_id = chassis_id


def mark_lgs310c_manual(db: Session) -> dict[str, Any]:
    """W4b.1.4 one-shot — NOT called from bootstrap (W4c.3).

    Idempotent provenance mark for asset 3 / name LGS310C.
    Writes only meta.field_sources / manual_overrides — not Asset.name value (K1).
    Reversible: remove 'name' from manual_overrides and field_sources.name.
    """
    asset = db.scalars(
        select(Asset).options(joinedload(Asset.interfaces)).where(Asset.id == 3)
    ).first()
    if asset is None:
        return {"changed": 0, "reason": "asset_3_missing"}
    if (asset.name or "").strip() != "LGS310C":
        return {"changed": 0, "reason": "name_mismatch", "actual": (asset.name or "").strip()}
    meta = dict(asset.meta or {})
    overrides = set(meta.get("manual_overrides") or [])
    sources = dict(meta.get("field_sources") or {})
    fs = sources.get("name") or {}
    src = ""
    if isinstance(fs, dict):
        src = str(fs.get("source") or "").lower()
    elif isinstance(fs, str):
        src = fs.lower()
    already = "name" in overrides and src.startswith("manual")
    if already:
        return {"changed": 0, "reason": "already_manual", "asset_id": 3}
    overrides.add("name")
    now = utcnow()
    sources["name"] = {
        "source": "manual", "confidence": 1.0, "last_seen": now.isoformat() + "Z",
        "marked_by": "w4b.1.4",
        "reversible": "remove name from manual_overrides + field_sources.name",
    }
    meta["manual_overrides"] = sorted(overrides)
    meta["field_sources"] = sources
    asset.meta = meta
    asset.updated_at = now
    db.flush()
    iface = next(iter(asset.interfaces or []), None)
    entity = iface or asset
    apply_observation(
        db, fact_key="asset.name", entity=entity, value="LGS310C",
        source="manual", observed_at=now, confidence=1.0, human_confirm=True,
    )
    db.add(AuditLog(
        user_id=None, action="asset.mark_name_manual", entity="asset", entity_id="3",
        detail={"name": "LGS310C", "chassis_id": asset.chassis_id, "wave": "w4b.1.4",
                "reversible": "remove name from manual_overrides + field_sources.name",
                "value_unchanged": True},
        ip="",
    ))
    return {"changed": 1, "asset_id": 3, "chassis_id": asset.chassis_id}


def list_unknown_nonempty_names(db: Session) -> list[dict[str, Any]]:
    """Enumeration only; never marks manual."""
    from app.services.name_proposal_chassis import asset_name_authority

    out = []
    assets = db.scalars(select(Asset).options(joinedload(Asset.interfaces))).unique().all()
    for asset in assets:
        name = (asset.name or "").strip()
        if not name:
            continue
        auth = asset_name_authority(asset)
        if auth is not None:
            continue
        macs = [i.mac for i in (asset.interfaces or []) if i.mac]
        out.append({"asset_id": asset.id, "name": name, "chassis_id": asset.chassis_id,
                    "macs": macs, "origin": "unknown_nonempty"})
    return out


def ambiguous_manual_names(db: Session, chassis_id: int) -> list[str]:
    members = chassis_members(db, chassis_id)
    from app.services.name_proposal_chassis import MANUAL_AUTHORITY, asset_name_authority

    names = sorted({
        (m.name or "").strip() for m in members
        if (m.name or "").strip() and (asset_name_authority(m) or 0) >= MANUAL_AUTHORITY
    })
    return names


def adopt_name_on_chassis(db: Session, *, chassis_id: int, value: str,
                          source: str = "manual", proposal_id: int | None = None) -> dict[str, Any]:
    """W4c.1 — one canonical name via fact_assertions (subject=chassis).

    Does NOT write member.name or mark siblings manual. The member that already
    carries the chosen manual name is left unchanged; others stay as interfaces.
    """
    text = (value or "").strip()
    if not text:
        raise ChassisRenameError("empty", "Nome vuoto")
    chassis = db.get(Chassis, chassis_id)
    if chassis is None:
        raise ChassisRenameError("not_found", "Chassis non trovato", chassis_id=chassis_id)
    members = chassis_members(db, chassis_id)
    if not members:
        raise ChassisRenameError("empty_chassis", "Chassis senza membri", chassis_id=chassis_id)

    manuals = ambiguous_manual_names(db, chassis_id)
    if len(manuals) > 1 and text not in manuals:
        raise ChassisRenameError("ambiguous",
            f"Chassis con nomi manuali multipli: {', '.join(manuals)}", chassis_id=chassis_id)

    now = utcnow()
    from app.services.name_proposal_chassis import MANUAL_AUTHORITY, asset_name_authority

    incumbent = current(db, "chassis", chassis_id, "asset.name")   # idempotenza
    if incumbent is not None and incumbent.value_norm == text and (incumbent.source or "").lower() == "manual":
        return {"changed": 0, "chassis_id": chassis_id, "value": text,
                "holder": "fact_assertion", "members_unchanged": [m.id for m in members]}

    for member in members:  # archivia proposte pending combacianti
        for prop in list(member.name_proposals or []):
            if (prop.status or "") != "pending":
                continue
            if proposal_id and prop.id == proposal_id:
                prop.status = "archived"; prop.status_reason = "adopted_chassis"; prop.updated_at = now
            elif (prop.value or "").strip() == text or (prop.source or "") == source:
                prop.status = "archived"; prop.status_reason = "superseded_chassis_adopt"; prop.updated_at = now

    holders = [m for m in members
               if (m.name or "").strip() == text and (asset_name_authority(m) or 0) >= MANUAL_AUTHORITY]
    if not holders:
        holders = [m for m in members if (m.name or "").strip() == text]
    primary = holders[0] if holders else members[0]
    iface = next(iter(primary.interfaces or []), None)
    entity = iface or primary

    apply_observation(db, fact_key="asset.name", entity=entity, value=text,
                      source="manual", observed_at=now, confidence=1.0, human_confirm=True)
    db.add(AuditLog(
        user_id=None, action="chassis.adopt_name", entity="chassis", entity_id=str(chassis_id),
        detail={"value": text, "holder": "fact_assertion",
                "members_not_renamed": [m.id for m in members], "wave": "w4c.1"},
        ip="",
    ))
    db.flush()
    return {"changed": 1, "chassis_id": chassis_id, "value": text,
            "holder": "fact_assertion", "members_unchanged": [m.id for m in members]}


def member_adopt_blocked_detail(db: Session, asset: Asset) -> Optional[dict[str, Any]]:
    """W4b.2.4 — any chassis member: refuse member adopt; subject is the chassis."""
    cid = asset.chassis_id
    if not cid:
        return None
    return {
        "code": "chassis_subject_required",
        "message": ("Adozione nome bloccata sul membro: il soggetto corretto è il chassis. "
                    f"Usa POST /api/chassis/{cid}/adopt-name."),
        "chassis_id": cid, "member_asset_id": asset.id,
    }
```
