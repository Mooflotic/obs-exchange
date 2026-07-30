# OBS-O28 — a11y dialogo + chrome «0 casi chiusi» (0.10.94)

```
wave: O28
branch: feature/obs-currency
base_dichiarata: ffd85ae9ed974ccfc37537d0cba4aaf8b73c1558
tip_O27_confermato_0.1: b251a43194f339fde4aa64ddecebce1b0c999ca2
VERSION: 0.10.94 (web; api/health resta 0.10.93 finché non si rebuilda api — atteso)
deploy: web only (api non toccata)
esito: D1–D5 OK · V1 4/4 PASS · V3 N=0 assente · gates color/contrast/evidence PASS · w8/drift SKIP
```

---

## 1. Elenco file toccati

| path | ruolo |
|------|--------|
| `web/src/components/DispositionCloseDialog.vue` | D1–D4 a11y APG |
| `web/src/views/Oggi.vue` | D5 `v-if` N>0 |
| `web/src/oggiClosedChrome.test.js` | V3 isolato (mock predicato + template) |
| `VERSION` / `web/package.json` / `CHANGELOG.md` | 0.10.94 |
| `docs/KNOWN_DEBT.md` | chiude DEBT-O27-DISPOSITION-DIALOG-A11Y |
| `docs/obs-o28*` | report + artefatti V/gates |

**Nessun file `api/app/**`.**

---

## 2. Blocco 0

### 0.1 (integrale)

```
===== 0.1 git log --oneline -8 feature/obs-currency =====
b251a43 docs(observatory): O27 chiusura UX lifecycle — test E1.2 + catture (no prodotto)
ffd85ae docs(observatory): report O26 (principale 3f9ab1f)
3f9ab1f feat(observatory): O26 Oggi lifecycle dispositions (0.10.93)
638d115 docs(observatory): report O25 (principale 4571e45)
4571e45 docs(observatory): O25 M0 discovery + P lifecycle policy (no D)
18d1489 docs(observatory): report O24 split disclosure (principale b6ae530)
b6ae530 feat(observatory): O24 Topology split A/B disclosure FDB (0.10.92)
c880f36 docs(observatory): allinea tip §9 O23 a HEAD/origin 65375c9

===== git rev-parse HEAD =====
b251a43194f339fde4aa64ddecebce1b0c999ca2

===== git fetch origin && git rev-parse origin/feature/obs-currency =====
b251a43194f339fde4aa64ddecebce1b0c999ca2

===== HEAD == b251a43194f339fde4aa64ddecebce1b0c999ca2? =====
YES

===== ancestor ffd85ae9ed974ccfc37537d0cba4aaf8b73c1558 (base O27)? =====
YES

===== HEAD == origin? =====
YES
```

GATE BLOCCO 0: **PASS**.

### 0.2 harness O27

- Path usato in O27: `/tmp/o27_e2_capture.py` (filesystem locale, **non** tracciato in git).
- Classificazione: **RESIDUO ONE-SHOT** (PREFIX `obs-o27`, stati hard-coded O27, non riusabile senza riscrittura).
- Azione: **RIMOSSO** (`rm /tmp/o27_e2_capture.py`). Nessun altro untracked toccato.
- Harness O28 V (`/tmp/o28_v_capture.py`): one-shot analogo → **rimosso in G6**.

---

## 3. D1–D6

Fonte nel codice: WAI-ARIA APG Dialog (Modal) — https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/

| ID | Cosa | Dove |
|----|------|------|
| D1 | All’open: salva `document.activeElement` come opener; `nextTick` → focus sul primo `input[name=disp-esito]`; dialog `tabindex="-1"` fallback | `DispositionCloseDialog.vue` |
| D2 | `keydown` capture su `window`: Tab/Shift+Tab ciclano tra focusabili del dialog | idem |
| D3 | Esc → `onCancel` (stesso emit di Annulla); nessun POST | idem |
| D4 | Alla chiusura (`open→false`): `previouslyFocused.focus()` | idem |
| D5 | `v-if="!loading && closedDispositionCount > 0"` — assente dal DOM a N=0 | `Oggi.vue` |
| D6 | Nessun tocco a disposition logic / altre rotte / inference / resolver | — |

---

## 4. V1–V6

### V1 — a11y PRIMA (O27) / DOPO (O28 deployed)

| Controllo | PRIMA (O27 E2.3) | DOPO (O28 V1) |
|-----------|------------------|---------------|
| Focus iniziale nel dialog | **FAIL** — `active=BUTTON.odm-btn`, `active_inside_dialog=false` | **PASS** — `active=INPUT name=disp-esito type=radio`, `active_inside_dialog=true` |
| Focus trap Tab/Shift+Tab | **FAIL** — 4° Tab → `SUMMARY.oggi-collapse-sum` | **PASS** — 14 Tab senza fuga; Shift+Tab dal primo → `BUTTON.primary` dentro dialog |
| Esc chiude senza inviare | **FAIL** — `esc_closes=false` | **PASS** — dialog chiuso; GET dispositions `count=0` invariato |
| Focus torna al trigger | **FAIL** — dopo Annulla `active=BODY` | **PASS** — Esc e Annulla → `BUTTON.odm-btn` con `data-o28-opener=1` |

Dettaglio tecnico DOPO: `docs/obs-o28-e2.json`. Nessun Conferma cliccato; `post_dispositions.count=0`.

### V2 — ricattura dialog (stessi 3 stati)

| stato | file | sha256 | nota |
|-------|------|--------|------|
| iniziale | `obs-o28-dialog-initial-1280.png` | `fb1feded64408c81d853a0ee4fdb75fb7dd69a32777db96c672a10dd368db5b0` | invariato visivamente |
| esito + motivo vuoto | `obs-o28-dialog-esito-no-motivo-1280.png` | `e5fd2823952185fd40342ebf491f27c9641e484cdb8dd69496400f96c73cd028` | alert «Motivazione obbligatoria.» |
| pronto | `obs-o28-dialog-ready-1280.png` | `4d21196956321965d80930af16218240baafadd36467f34f9721715e6519205e` | senza Conferma |

### V3 — chrome N=0 / N>0

**Deployed NAS (N=0 operativo):** `[data-o26=closed-count]` **assente** (`in_dom=false`, `height=0`). Cattura `obs-o28-oggi-n0-no-chrome-1280.png` sha256=`2fc17092ca95dabc698a56bcdb2f4f2f66622647d5dce7a319cb325bca6d5ed1`.

**Isolato (no NAS):** `web/src/oggiClosedChrome.test.js` — predicato `!loading && closedCount > 0`; template assert `v-if="!loading && closedDispositionCount > 0"` + link `/timeline?disposizioni=1`. **3/3 PASS**.

Bundle minificato conferma: `!n.value&&P.value>0?(… "casi chiusi — consulta Timeline" …)`.

### V4 — pytest -v integrale (17)

```
tests/test_disposition_o26.py::test_disposition_key_chassis_asset PASSED
tests/test_disposition_o26.py::test_disposition_key_fdb_row_granularity PASSED
tests/test_disposition_o26.py::test_material_new_sa_signal_absent_from_fingerprint PASSED
tests/test_disposition_o26.py::test_material_new_sb_mac_move_new PASSED
tests/test_disposition_o26.py::test_material_new_i3_conflict_new PASSED
tests/test_disposition_o26.py::test_material_new_name_kind_changed PASSED
tests/test_disposition_o26.py::test_material_new_i2_absent_flip PASSED
tests/test_disposition_o26.py::test_material_new_exclusion_same_signal_only_last_seen PASSED
tests/test_disposition_o26.py::test_material_new_exclusion_source_fdb_alone PASSED
tests/test_disposition_o26.py::test_material_new_exclusion_soft_no_delta PASSED
tests/test_disposition_api_o26.py::test_v4_rejects_empty_motivation_and_bad_esito PASSED
tests/test_disposition_api_o26.py::test_v1_close_and_v5_reopen_keeps_both_events PASSED
tests/test_disposition_api_o26.py::test_v3_row_granularity_keys_distinct PASSED
tests/test_disposition_api_o26.py::test_v0_empty_table_means_no_closed_keys PASSED
tests/test_disposition_api_o26.py::test_e12_mixed_fdb_rows_filter_hides_only_closed_key PASSED
tests/test_disposition_api_o26.py::test_e12_fdb_and_chassis_keys_do_not_collide PASSED
tests/test_disposition_api_o26.py::test_e12_http_post_rejects_empty_or_bad_esito_writes_nothing PASSED
============================== 17 passed in 0.96s ==============================
```

### V5 — contrasto

**Nessun colore/token modificato** da D1–D5 (solo focus/keydown/`v-if`). Tabella O27 non ripetuta.

### V6 — gate frontend (integrali)

**color_literal_gate.py --self-test:** `SELFTEST PASS: inject fails (vue+matrix rule), remove passes`  
**color_literal_gate.py:** `PASS: no hard-coded color literals outside allowlist; matrix.css decls-only`

**contrast_gate.py --self-test:** `SELFTEST PASS: inject fails, remove passes`  
**contrast_gate.py:** `PASS: contrast pairs within threshold or allowlisted with debt` (ALLOWLISTED_FAILS=1 `--text-3` / DEBT-NO-CONTRAST-PRESIDIO — preesistente)

**evidence_gate.py --self-test:** `SELFTEST PASS: inject fails (ownership+marker+i2), remove passes`  
**evidence_gate.py:** `PASS: no FDB+ownership vocabulary; required evidence markers present; I2 placeholders declared`

**w8 / drift: NON eseguiti** — motivazione: nessun file backend toccato; ondata solo Vue/CSS dialog+chrome Oggi.

---

## 5. Debiti

`DEBT-O27-DISPOSITION-DIALOG-A11Y` → **CHIUSO O28** (V1 4/4 PASS).

---

## 6. Fase G

- **G1:** VERSION + `web/package.json` → **0.10.94**
- **G2:** `./scripts/deploy.sh web` — snapshot DB saltato; **api non rebuildato** (nessuna modifica `api/app/**`)
- **G3:** asset servito `/assets/index-BFZN3CqU.js` sha256=`301412f80f26c715bb54bf06d9b28880f27d82e1093fb467a5097f73e3bcb09d`; marker `o28-first-focus`, `Escape`, `disp-esito`, condizione compilata `P.value>0` + testo «casi chiusi». `api/health.version`=`0.10.93` (container api non aggiornato — atteso).
- **G4:** ricatture V1/V3 sopra.
- **G5:** commit principale (hash sotto; tip report non autocertifica — O29 in 0.1).
- **G6:** harness `/tmp/o27_e2_capture.py` e `/tmp/o28_v_capture.py` rimossi (one-shot).

---

## 7. Cosa NON hai fatto

- Nessuna scrittura disposizione sul NAS.
- Nessun deploy `api` / collector.
- Nessun w8/drift.
- Nessun tocco a T7, OBS-CURRENCY, `api/app/facts/`, Topology, O15, `material_new`/reopen logic.
- Nessun cablaggio `/ai`.
