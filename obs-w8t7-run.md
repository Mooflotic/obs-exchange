# OBS — W8-T7-RUN · esecuzione T7 sul NAS via SSH

Ramo `feature/obs-currency` · prod **0.10.63** · read-only · nessun deploy · nessun bump.

**Canale:** `mooflo@192.168.1.3` con `-i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=8`.
Mai `cassiopea`, mai `192.168.3.24`, mai utente diverso da `mooflo`.

**`<DC>` scelto (P1):** `docker compose` (VARIANTE PRE-AUTORIZZATA: `sudo -n` fallisce con password required; `docker compose version` ok senza sudo).

**Redazione:** nessuna credenziale trovata negli output catturati; nessuna sostituzione `<REDACTED>` necessaria.

**STOP obbligatorio al punto 2:** `file scansionati: 176` ≠ 175 atteso → **repo ≠ produzione**. Sequenza fermata prima del punto 3 (collector **non** fermato).

## Conteggio righe

| Artefatto | `wc -l` |
|---|---|
| `obs-w8t7-run.md` | 216 |

---

## Output integrali (`/tmp/w8out_local/`)

### 00_channel
```
OK_SHELL
mooflo
/volume1/home/mooflo
```

### 00_docker
```
sudo: a password is required
sudo_exit=1
Docker Compose version v2.35.1
docker_exit=0
```

### 00_sha_local
```
80744e430c356f955f635bc7244a814b638b98fc9ef42de56171213187475802  observatory/scripts/w8_currency_gate.py
e440305cf3cdb6d94bed14a688f48ef6ddc2a403944ac725f82aafcddea8ae0e  observatory/scripts/w8_g8_equivalence.py
```

### 00_sha_nas (prima del trasferimento)
```
sha256sum: can't open 'scripts/w8_currency_gate.py': No such file or directory
sha256sum: can't open 'scripts/w8_g8_equivalence.py': No such file or directory
```

**P2:** i due script erano **assenti** sul NAS. Trasferiti uno per uno via `scp` (vietato rsync cartella). Hash dopo trasferimento:

### 00_sha_nas_after
```
80744e430c356f955f635bc7244a814b638b98fc9ef42de56171213187475802  scripts/w8_currency_gate.py
e440305cf3cdb6d94bed14a688f48ef6ddc2a403944ac725f82aafcddea8ae0e  scripts/w8_g8_equivalence.py
```
Locale ≡ remoto dopo scp.

### 01_selftest
```
SELFTEST/1 corpus principale: atteso 3 violazioni ['file2_rawsql.py', 'file3_filterby.py', 'file4_count.py'] + 1 accounted
SELFTEST/1 osservato: 3 violazioni ['file2_rawsql.py', 'file3_filterby.py', 'file4_count.py'] + 1 accounted + 0 temporanee
SELFTEST/1: PASS
SELFTEST/2 config-check temporanee: atteso 1 errore (debt vuoto) + 0 (debt valido)
SELFTEST/2 osservato: 1 errore(i) debt-vuoto + 0 debt-valido
SELFTEST/2: PASS

SELFTEST: PASS (il gate sa fallire e valida le temporanee)
```
exit=0.

### 02_gate_nas
```
== W8 CURRENCY GATE (indurito, W8-fix2) ==
root: /volume1/Docker/observatory
sentinelle: simbolo ORM 'FactAssertion' · tabella grezza 'fact_assertions' in chiamata SQL (text/execute) · COMBO (fact-token FactAssertion|fact_assertions|fact_key) + valore di stato quotato 'current'
scope: api/**, scripts/**, collector/**
esclusioni:
  - api/app/facts/**  (il resolver È la fonte della correntezza)
  - scripts/w8_currency_gate.py  (contiene le sentinelle/fact_key come dato)
  - scripts/w8_g8_equivalence.py  (contiene le sentinelle/fact_key come dato)
file scansionati: 176
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
exit=0.

### 03_stop … 10_chassis
`<non eseguito>` — STOP al controllo immediato del punto 2.

---

## Difetto: repo ≠ produzione (punto 2)

| | Repo (§T6 / locale) | NAS (02_gate_nas) |
|---|---|---|
| `file scansionati` | **175** | **176** |
| esito | PASS (con 1 eccezione temporanea) | PASS (con 1 eccezione temporanea) |
| violazioni | 0 | 0 |
| permanenti / temporanee | 17 / 1 | 17 / 1 |

**Righe divergenti vs gate repo (§T6):**
1. `root:` locale `/Users/…/observatory` vs NAS `/volume1/Docker/observatory` (atteso: path diverso).
2. **`file scansionati: 176`** vs **`175`** ← **difetto bloccante**.

Diagnostica post-STOP (sola lettura, `find … '*.py'`): sul NAS esiste **`scripts/_w4a_measure.py`**, assente dal repo locale. Diff:
```
132a133
> scripts/_w4a_measure.py
```
Nessuna violazione aggiuntiva (il file non tocca `FactAssertion`/sentinelle), ma il conteggio file **non coincide** → protocollo: FERMATI. Non appianato.

---

## Tabella previsione (§T5) → osservato → scarto

| Voce | Previsione (§T5 / T7) | Osservato | Scarto |
|---|---|---|---|
| gate selftest | SELFTEST PASS | SELFTEST PASS | nessuno |
| gate NAS file scansionati | 175 | **176** | **+1** (`scripts/_w4a_measure.py` solo NAS) → STOP |
| gate NAS esito | 0 viol / 17 perm / 1 temp / PASS (con 1 temp) | 0 / 17 / 1 / PASS (con 1 temp) | conteggio file diverge |
| repo-vs-NAS identico | sì riga per riga | **no** | riga `file scansionati` |
| G8 asset.name | DIVERGE=0; RESOLVER ⊇ {3,139,143} | `<non eseguito>` | — |
| G8 endpoint | SKIP | `<non eseguito>` | — |
| G8 os.guess | DIVERGE=0; RESOLVER=0; FALLBACK ⊇ {1,5,19,46} | `<non eseguito>` | — |
| G8 mutate-probe 3 | pre-cond R='LGS310C'; DIVERGE=1; FAIL; exit 1 | `<non eseguito>` | — |
| needs_apply / T_backup / structural / observations | da wp_gate | `<non eseguito>` | — |
| breaker / convergenza | closed / OK | `<non eseguito>` | — |
| assets (COUNT Asset) | 151 | `<non eseguito>` | — |
| ip_current / NP / FA current / AD | da wp_gate; AD≠68 non regressione | `<non eseguito>` | — |
| I6 | vuoto (`grep`) | `<non eseguito>` | — |
| chassis LGS310C / LGS328C | 32/{3,139,143} · 23/{2,109} (HTTP) | fatto DB / 147·151: `<non eseguito>` | — |
| collector | start dopo stop | **non fermato** (STOP prima del p.3) | — |

---

## ASSERT FINALE

```
needs_apply=<non eseguito> · T_backup=<non eseguito> · structural=<non eseguito> ·
observations assente da sqlite_master=<non eseguito> · breaker=<non eseguito> ·
convergenza=<non eseguito> · currency-gate selftest PASS=sì ·
currency-gate scan NAS: violazioni=0, permanenti=17, temporanee=1,
  esito=PASS (con 1 eccezione/i temporanea/e) ·
repo-vs-NAS identico=NO (file scansionati 176≠175; extra scripts/_w4a_measure.py) ·
G8 asset.name DIVERGE=<non eseguito> · G8 os.guess DIVERGE=<non eseguito> ·
G8 mutate-probe DIVERGE=1 su id=3 (pre-cond R=<non eseguito>)=<non eseguito> ·
I6 vuoto=<non eseguito> · AD rimisurato=<non eseguito> · assets(COUNT Asset)=<non eseguito> ·
collector riavviato=n/a (mai fermato) · chassis LGS310C=<non eseguito> ·
chassis LGS328C=<non eseguito>
```
`T_total` non è un gate: si riporta e basta.

**STOP per review.** Nessun avanzamento a W3, nessun merge, VERSION resta 0.10.63.
Collector mai fermato. Decisione su `_w4a_measure.py` (rimuovere dal NAS / portare in repo / escludere) a Michele.
