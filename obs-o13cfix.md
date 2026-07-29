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

Entrambi:

```
VIOLAZIONI: 0
RISULTATO: PASS (con 1 eccezione/i temporanea/e)
TEMP scripts/wp_gate.py:103 … debt=DEBT-WPGATE-CURRENCY-COUNT-LOCAL
```

Integrali: `docs/_o13cfix_gate_repo_integral.txt`, `docs/_o13cfix_gate_nas_integral.txt` (non in share).

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

| deliverable | sha256 | wc -l | URL |
|-------------|--------|------:|-----|
| [obs-o13cfix.md](https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-o13cfix.md) | *(vedi tabella finale agente)* | — | raw main |
| [obs-o13cfix-baseline.diff.txt](https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-o13cfix-baseline.diff.txt) | `6c4ef6db7c7c7e302927d52b2dc76ac19a44fd8b50ec92768fd36e850d933811` | 2411 | raw |
| [obs-o13cfix-rollback.diff.txt](https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-o13cfix-rollback.diff.txt) | `9fbb6a2e68382faea93add069f055bd976128fbc0028a2607ec71547e2c5b994` | 2171 | raw |
| [obs-o13c.md](https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-o13c.md) (errata) | — | — | raw |
| [obs-o13cfix-CHANGELOG.md](https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-o13cfix-CHANGELOG.md) | — | — | raw |
| [obs-o13cfix-KNOWN_DEBT.md](https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-o13cfix-KNOWN_DEBT.md) | — | — | raw |

### Screenshot O13C-FIX

Harness O9 / Playwright **non disponibile** in questa sessione (`playwright not installed`). Login UI non automatizzato. Preferire catture privacy-safe post-login manuale su `/oggi` con sezione egress `data-o13cfix=baseline`.

- Nessun raise di tetti
- Nessun ripristino `FLOW_INGEST` / `ZEEK_PROVIDER`
- Nessuna modifica a `scripts/_w4a_measure.py`
- Nessun IP destinazione in report o assert stampati
- Nessun merge su main
