# OBS-UX O13D — auto-lift novità, soppressione visibile, gate colori (0.10.81)

Ramo lavoro locale; **STOP per review**; nessun push/merge su main. FA 251 intatto; `FLOW_INGEST` / `ZEEK_PROVIDER` non toccati; `EGRESS_INGEST` resta true; novità può restare env=false finché baseline `in_costruzione` (0 card).

**VERSION:** 0.10.81  
**Meccanismo C1:** **(i)** auto-lift alla chiusura baseline B2  
**PREVISIONI:** [`obs-o13d-PREVISIONI.md`](obs-o13d-PREVISIONI.md) (dichiarate prima del deploy — onorate)

**Diff tematici:** `obs-o13d-novelty.diff.txt`, `obs-o13d-color.diff.txt`, `obs-o13d-meta.diff.txt`  
**Emissioni:** [`obs-o13d-emissions-246.json`](obs-o13d-emissions-246.json)  
**Redact share:** [`obs-o13cfix-redatto.md`](obs-o13cfix-redatto.md) + `obs-o13d-redact-o13c-*.png`

---

## PREVISIONI → OSSERVATI

| id | previsione | osservato |
|----|------------|-----------|
| C0 gitignore | `.env` / `.env.*` / `!.env.example` | **già C0** — non modificato oltre |
| C0 5× ux2-assets | leave | **leave** (`docs/obs-ux2-assets/` 5 file) |
| C0 3× measure | leave + debt 4ª | **leave** + `DEBT-ONESHOT-SCRIPT-RESIDUE` 4ª occorrenza |
| C1 meccanismo | (i) auto-lift + env=false post-lift = manuale | **shipped** `resolve_novelty_emission` |
| Baseline post-deploy | `in_costruzione`, coverage ≪ 3d | **OK** coverage ~0.107d / 3d; serie 0/3 |
| Card N5 | 0 | **OK** 0 card; invalid 246 |
| Gap 327…584 | 12 id senza marcatore | **12** id: 342,346–349,385,400–402,418,425,442 — esistono, `first_seen` &lt; ready prematuro → non erano candidati N5 |
| C6 verdi | Incidents/Plant | **fix**; residui canvas/AI in allowlist gate |
| C7 | pochi (a)/(d); (b)(c)(e) rinviati | vedi `obs-o13d-c7-registro.md` |
| marker | `obs-o13d-marker` nel bundle | **OK** in `index-B_irPQUC.js` |
| health | 0.10.81 | **OK** `{"version":"0.10.81"}` |
| novelty_suppression | stamping post-deploy | **OK** `premature_baseline_protection` active |

---

## C0 — classificazione residui

| classe | path | decisione |
|--------|------|-----------|
| ux2-assets ×5 | `docs/obs-ux2-assets/` | **leave** (probe docs) |
| measure ×3 | `scripts/w5b_measure.py`, `w6review_measure.py`, `w7c_measure.py` | **leave** + debt 4ª |
| public channel | — | `DEBT-PUBLIC-CHANNEL-EXPOSURE` (solo obs-exchange; decisione Michele) |
| screenshot harness | — | `DEBT-SCREENSHOT-HARNESS-FRAGILE` |

---

## C1 — novelty emission

- `invalidate_premature_baseline` → `novelty_suppression_active=True`, reason=`premature_baseline_protection`, `o13d_marker`
- `maybe_close_baseline_after_cycle` → ready **solo** B2; lift: `signals_armed=True`, `novelty_auto_enabled=True`, `lift_reason=baseline_closed_b2` + snapshot criteri; **mai** `deferred==0`
- `resolve_novelty_emission` → `{allowed, state, suppression}`
  - allowed iff `baseline_ready ∧ signals_armed ∧ ¬manual_suppress` (con scudo auto post-lift che ignora env=false da B1 finché env non torna true)
  - env=false dopo drop scudo → `novelty_suppressed_manual` **visibile**
- `novelty_egress_cards` / `build_egress_signals` usano resolve; payload `novelty_suppression` / `novelty_emission`
- Coverage `zeek_egress`: `signal_suppression` + card `coverage_novelty_suppressed` (P7 `igiene_nome`); stato **non** cieca/disabilitata

---

## C2 — test

`tests/test_o13d_soppressione.py`: R3 manuale visibile; R4 skip pre-ready + invalid; auto-lift; unmark R6.

```
pytest tests/test_o13d* tests/test_o13c* -q
22 passed
```

---

## C3 — 246 emissioni (NAS RO)

| campo | valore |
|-------|--------|
| count | **246** |
| id range | 327…584 (258 slot) |
| missing | **12** (vedi JSON) |
| extra fuori range | 0 |

Lista completa: [`obs-o13d-emissions-246.json`](obs-o13d-emissions-246.json) (solo `id`,`scope`,`marker` — no IP/MAC/nomi).

**API ripesca:** `POST /api/egress/invalid-baseline-emissions/{id}/unmark` (+ `/remark`).

### Embed riepilogo

```json
{
  "count": 246,
  "id_min": 327,
  "id_max": 584,
  "missing_in_range": [342, 346, 347, 348, 349, 385, 400, 401, 402, 418, 425, 442],
  "gap_explanation": "first_seen before premature ready_at — not N5 candidates"
}
```

---

## C4 — redact

6 PNG pixelati: `obs-o13d-redact-o13c-{oggi,dossier}-{1280,768,390}.png`  
Doc: `obs-o13cfix-redatto.md` — pointer in `obs-o13cfix.md`.

---

## C5 — screenshot

**STOP** — credenziali UI assenti in sessione. Doc: `obs-o13d-screenshot-harness.md`. Debito fragile aperto.

---

## C6 — color gate

- Script: `scripts/color_literal_gate.py` (+ `--self-test` inject/remove)
- Fix: Incidents `rgba(61,255,138,*)` → `color-mix(var(--ok))`; Plant `#47b36b` / `#83c99c` → `var(--ok)`
- Token: `--ok #4fb477`, `--warn`=`--attn`, `--attn`, `--accent` in `matrix.css`
- Residui canvas/AI: allowlist con reason (nessun colore inventato)

```
python3 scripts/color_literal_gate.py → PASS
python3 scripts/color_literal_gate.py --self-test → PASS
```

---

## C7 / C8

- C7: registro `obs-o13d-c7-registro.md` — «Visualizza dati» assente; (b)(c)(e) deferred
- C8: `test_priority_consistency_p6_both_scopes` presente; egress cards hanno `actions`; inference block label `INFERENZA IA`

---

## Marker / VERSION

| artefact | valore |
|----------|--------|
| VERSION | 0.10.81 |
| `api.js` | `obs-o13d-marker` |
| `observatoryUx.js` | `OBS_O13D_MARKER` |

---

## Gate currency (FULL)

### Repo (`python3 scripts/w8_currency_gate.py`)

```
VIOLAZIONI: 0
RISULTATO: PASS (con 1 eccezione/i temporanea/e)
```

Integrale: `docs/_o13d_gate_repo_integral.txt`

### NAS

```
VIOLAZIONI: 0
RISULTATO: PASS (con 1 eccezione/i temporanea/e)
VERSION: 0.10.81
```

Integrale: `docs/_o13d_gate_nas_integral.txt`  
Post-deploy: `invalidate_premature_baseline` re-stamp O13D → `novelty_suppression_active=True`; cards=0; invalid=246.

### Color gate

```
PASS: no hard-coded color literals outside token/allowlist files
SELFTEST PASS: inject fails, remove passes
```

---

## Deploy (Cassiopea)

Da Mac (rsync+ssh via `deploy.sh`), poi sul terminale già aperto in `/volume1/Docker/observatory`:

```bash
sudo docker compose up -d --build --force-recreate --no-deps api web collector
```

Env: `EGRESS_INGEST_ENABLED=true`; `EGRESS_NOVELTY_SIGNALS_ENABLED=false` ok finché `in_costruzione` (0 card N5). Dopo B2 close, auto-lift arma i segnali anche con env false (scudo); successivo env=false = soppressione manuale visibile.

---

## Shipped vs deferred (onesto)

| item | stato |
|------|-------|
| C0 debt + classificazione | **shipped** |
| C1 resolve + auto-lift + coverage note | **shipped** |
| C2 test R3/R4/lift | **shipped** |
| C3 246 JSON + unmark API | **shipped** |
| C4 redact PNG + md | **shipped** |
| C5 screenshot live | **STOP / deferred** (no creds) |
| C6 gate + worst greens | **shipped**; residui canvas/AI allowlisted |
| C7 (a)/(d) light | **shipped** (nessun difetto chiaro); (b)(c)(e) **deferred** |
| C8 spot-check | **shipped** (test priorità già presente) |
| push/merge | **non fatto** |
