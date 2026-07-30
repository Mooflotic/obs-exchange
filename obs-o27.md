# OBS-O27 — Blocco 0 + chiusura visiva/UX OBS-OGGI-LIFECYCLE

```
wave: O27
branch: feature/obs-currency
base_dichiarata_O26_principale: 3f9ab1fa5f46f304ae063f328122b88046dd780e
tip_confermato_0.1: ffd85ae9ed974ccfc37537d0cba4aaf8b73c1558
VERSION: 0.10.93 (invariata — nessun codice prodotto)
deploy: nessuno
esito: E1 PASS (17) · E2 catture+contrasto OK · E3 nessuna correzione codice · a11y dialogo = reperti
```

---

## 1. Elenco file toccati

**Nessuna riga di prodotto (api/web) modificata.** Solo test + docs/artefatti:

| path | ruolo |
|------|--------|
| `tests/test_disposition_api_o26.py` | +3 test E1.2 (filtro misto, chiavi FDB≠chassis, POST 400 zero-write) |
| `docs/obs-o27.md` | questo report |
| `docs/obs-o27-b0.txt` | Blocco 0.1 integrale |
| `docs/obs-o27-e1-pytest.txt` | pytest -v integrale |
| `docs/obs-o27-e2.json` | misure E2 (contrasto/a11y) |
| `docs/obs-o27-*.png` | catture 1280/768/390 + dialog |
| `docs/KNOWN_DEBT.md` | DEBT-O27-DISPOSITION-DIALOG-A11Y |

**E3:** nessuna correzione di codice. **G:** non applicata (no bump, no deploy, no gate w8/color/…).

---

## 2. Blocco 0.1 (integrale)

```
===== 0.1 git log --oneline -8 feature/obs-currency =====
ffd85ae docs(observatory): report O26 (principale 3f9ab1f)
3f9ab1f feat(observatory): O26 Oggi lifecycle dispositions (0.10.93)
638d115 docs(observatory): report O25 (principale 4571e45)
4571e45 docs(observatory): O25 M0 discovery + P lifecycle policy (no D)
18d1489 docs(observatory): report O24 split disclosure (principale b6ae530)
b6ae530 feat(observatory): O24 Topology split A/B disclosure FDB (0.10.92)
c880f36 docs(observatory): allinea tip §9 O23 a HEAD/origin 65375c9
65375c9 docs(observatory): registra tip commit §9 O23

===== git rev-parse HEAD =====
ffd85ae9ed974ccfc37537d0cba4aaf8b73c1558

===== git fetch origin && git rev-parse origin/feature/obs-currency =====
ffd85ae9ed974ccfc37537d0cba4aaf8b73c1558

===== ancestor 3f9ab1fa5f46f304ae063f328122b88046dd780e (O26 principale)? =====
YES

===== HEAD == origin? =====
YES
```

HEAD=origin discende da `3f9ab1fa5f46f304ae063f328122b88046dd780e` = **YES**.
Il tip `ffd85ae…` è il commit di sola pubblicazione report O26 (non autocertifica); il principale O26 resta `3f9ab1f…`.

GATE BLOCCO 0: **PASS**.

---

## 3. E1

### E1.1 — `pytest -v` integrale (SQLite tmp_path / app minimale; NON NAS)

```
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.3.4, pluggy-1.6.0 -- observatory/.venv/bin/python3
cachedir: .pytest_cache
rootdir: observatory
plugins: anyio-4.12.1, asyncio-0.24.0
asyncio: mode=strict, default_loop_scope=None
collecting ... collected 17 items

tests/test_disposition_o26.py::test_disposition_key_chassis_asset PASSED [  5%]
tests/test_disposition_o26.py::test_disposition_key_fdb_row_granularity PASSED [ 11%]
tests/test_disposition_o26.py::test_material_new_sa_signal_absent_from_fingerprint PASSED [ 17%]
tests/test_disposition_o26.py::test_material_new_sb_mac_move_new PASSED  [ 23%]
tests/test_disposition_o26.py::test_material_new_i3_conflict_new PASSED  [ 29%]
tests/test_disposition_o26.py::test_material_new_name_kind_changed PASSED [ 35%]
tests/test_disposition_o26.py::test_material_new_i2_absent_flip PASSED   [ 41%]
tests/test_disposition_o26.py::test_material_new_exclusion_same_signal_only_last_seen PASSED [ 47%]
tests/test_disposition_o26.py::test_material_new_exclusion_source_fdb_alone PASSED [ 52%]
tests/test_disposition_o26.py::test_material_new_exclusion_soft_no_delta PASSED [ 58%]
tests/test_disposition_api_o26.py::test_v4_rejects_empty_motivation_and_bad_esito PASSED [ 64%]
tests/test_disposition_api_o26.py::test_v1_close_and_v5_reopen_keeps_both_events PASSED [ 70%]
tests/test_disposition_api_o26.py::test_v3_row_granularity_keys_distinct PASSED [ 76%]
tests/test_disposition_api_o26.py::test_v0_empty_table_means_no_closed_keys PASSED [ 82%]
tests/test_disposition_api_o26.py::test_e12_mixed_fdb_rows_filter_hides_only_closed_key PASSED [ 88%]
tests/test_disposition_api_o26.py::test_e12_fdb_and_chassis_keys_do_not_collide PASSED [ 94%]
tests/test_disposition_api_o26.py::test_e12_http_post_rejects_empty_or_bad_esito_writes_nothing PASSED [100%]

============================== 17 passed in 0.90s ==============================
```

Artefatto: `docs/obs-o27-e1-pytest.txt`.

### E1.2 — mappatura comportamento → test

| Comportamento | Test (nome esatto) | Note |
|---|---|---|
| `reopen` ≠ `close`; chiusura resta in storico (P6) | `test_v1_close_and_v5_reopen_keeps_both_events` | già O26 |
| Granularità riga mista (una closed, una open → solo closed filtrata) | `test_e12_mixed_fdb_rows_filter_hides_only_closed_key` | **aggiunto O27** (V3 O26 solo chiavi distinte) |
| POST motivazione vuota / esito invalido → 400/422, zero eventi | `test_e12_http_post_rejects_empty_or_bad_esito_writes_nothing` | **aggiunto O27** (HTTP su app minimale; V4 restava solo ValueError helper) |
| Chiave FDB ≠ Apparati stesso chassis numerico | `test_e12_fdb_and_chassis_keys_do_not_collide` | **aggiunto O27** |

### E1.3 — bulk `archiveNoiseMass` fuori da Oggi?

**Sì.** Meccanismo di dominio esistente, indipendente dalle disposizioni:

1. FE: `archiveNoiseMass` → `api.rejectNameProposalsBulk(ids)` (`web/src/views/Oggi.vue` ~1027–1046).
2. API: `prop.status = "rejected"`, `status_reason = "rejected_bulk_oggi"` (`api/app/routers/assets.py` ~912–913).
3. FE triage: `noiseProposalIds` include solo `(p.status || "pending") === "pending"` (`web/src/triageRules.js` ~374–376).

Dopo il bulk le proposte non sono più pending → escono da `noiseIds` / coda rumore Oggi senza write disposition (M1/O26).

---

## 4. E2 — visivo deployed (nessun POST disposizione)

Auth: session mint, TTL 180s; token non pubblicato.  
`Page.screenshot` Playwright (CDP `Page.captureScreenshot`), `deviceScaleFactor:1`.  
Post-E2 GET `/api/oggi/dispositions`: `count=0`, `closed_count=0` (nessuna scrittura).

### E2.1 catture vuoto + o9_png_assert

| file | WxH | sha256 |
|------|-----|--------|
| `obs-o27-oggi-1280.png` | 1280×16313 | `da37e5843597ed6923949d4984671dd99f240bc1d7c13a64a501456f011d31de` |
| `obs-o27-oggi-768.png` | 768×19679 | `c6a89c09390de47a72bd10276ba53fd82dc9c76550cc66060dc6e2be06fa8f5a` |
| `obs-o27-oggi-390.png` | 390×25261 | `3a3bab722c642c032de55faf9eeb8a4f43504653c40468fc546ae8b04b6c4cd1` |
| `obs-o27-timeline-disp-1280.png` | 1280×11917 | `ea38fc81a61173c6c58e212e83864c35d51a5c266810b6012957a63500402d5f` |
| `obs-o27-timeline-disp-768.png` | 768×11985 | `c79e4f3070e212388f4d1e077bc950e296a601ed498127407b134c07dd5c5576` |
| `obs-o27-timeline-disp-390.png` | 390×14498 | `a3c57a22f13412a8b3e82979e236362eac5b88cd0b421f9417595f9aab68956b` |

`o9_png_assert.py --pair`: PASS su tutte e 4 le coppie oggi/timeline.

### E2.2 dialogo (SENZA Conferma / SENZA POST)

Trigger: `button:has-text("Ignora")` → apre `DispositionCloseDialog`.

| stato | file | sha256 | fatto UI |
|-------|------|--------|----------|
| iniziale (nessun esito, motivazione vuota) | `obs-o27-dialog-initial-1280.png` | `be15945d1cd7f68eee98541ccd0b2ae201f86b4af97f5febf18cdb880e2543bb` | dialog aperto |
| esito selezionato + motivazione vuota + click Conferma | `obs-o27-dialog-esito-no-motivo-1280.png` | `4e377ca6d8f5b0a7b9cc4a9095b0a8bfcc2611629ab55196ff0b9b81eba94568` | alert visibile: **«Motivazione obbligatoria.»** (client-side; nessun POST) |
| esito + motivazione compilati, pronto | `obs-o27-dialog-ready-1280.png` | `986ab129cd7fc461ba015b5d6c8f76915e552467b9bc4d6b3276be63e77702c7` | non cliccato Conferma |

Stato «inviato con successo»: **non** verificato sul NAS (vincolo); coperto da E1 isolato (`test_v1_close_and_v5_reopen_keeps_both_events`).

### E2.3 a11y + contrasto (deployed, senza invio)

| check | esito |
|-------|--------|
| Focus iniziale entra nel dialog | **NO** — all’apertura `activeElement` resta il bottone opener (`BUTTON.odm-btn`), fuori dal dialog |
| Focus trap (Tab) | **ASSENTE** — dopo Tab su textarea → Annulla → Conferma, il 4° Tab esce su `SUMMARY.oggi-collapse-sum` |
| Esc chiude senza inviare | **NO** — Esc non chiude (`esc_closes=false`; nessun handler) |
| Focus ritorna all’opener dopo Annulla | **NO** — dopo Annulla `activeElement` = `BODY` (nessun restore nel componente) |

**Reperti (scelta di design → non auto-fix in E3):** registrati come `DEBT-O27-DISPOSITION-DIALOG-A11Y`.

Contrasto elementi nuovi del dialogo (WCAG 2.1 relative luminance, `(L1+0.05)/(L2+0.05)`):

| elemento | fg | bg | ratio | AA normal (≥4.5) |
|----------|----|----|-------|------------------|
| titolo `#disp-dialog-title` | `#e8ebf0` | `#161b23` | **14.46** | PASS |
| hint `.disp-dialog__hint` (`--text-2`) | `#98a2b3` | `#161b23` | **6.71** | PASS |
| legend Esito | `#e8ebf0` | `#161b23` | **14.46** | PASS |
| label radio esito | `#e8ebf0` | `#161b23` | **14.46** | PASS |
| label Motivazione | `#e8ebf0` | `#161b23` | **14.46** | PASS |
| textarea testo | `#e8ebf0` | `#0f1319` | **15.59** | PASS |
| placeholder motivazione | *assente nel markup* (`textarea` senza `placeholder`) | — | n/a | n/a |
| errore `[role=alert]` | `#e06b52` (`--danger`) | `#161b23` | **5.26** | PASS |
| Conferma `.primary` | `#0f1319` su `#6bc5db` | — | **9.43** | PASS |
| Annulla `.ghost` | `#98a2b3` | `#161b23` | **6.71** | PASS |

Fonte: formula contrasto WCAG 2.1 §1.4.3 (relative luminance). Misure in `docs/obs-o27-e2.json`.

### E2.4 — conteggio «0 casi chiusi» (fatti)

- Testo: `0 casi chiusi — consulta Timeline` (link a `/timeline?disposizioni=1`).
- Sempre presente se `!loading` (`v-if="!loading"`, non condizionato a `N>0`).
- Geometria @1280: `display:block`, `13px`, altezza **19 px**, larghezza **1012 px**, `top≈62`, `left≈244` (sotto header/banner).
- Colore link: `--text-2` `#98a2b3` su `#0f1319` → ratio **7.23**.
- CSS: `.oggi-closed-signal` in `Oggi.vue`.

(Valutazione rumore/invasività: decisione Michele — non modificato.)

---

## 5. E3 / G

**E3 non ha applicato alcuna correzione di codice.**  
Reperti a11y dichiarati come debito (non ambiguità estetico sul conteggio a 0).  
Contrasto elementi nuovi: tutti ≥4.5 — nessun fix contrasto.

**G non eseguita** (nessun bump VERSION, nessun deploy, nessun gate w8/color/contrast/evidence/drift, nessun commit di prodotto).

---

## 6. Debiti

- **Nuovo:** `DEBT-O27-DISPOSITION-DIALOG-A11Y` — focus iniziale / trap / Esc / restore opener assenti sul dialogo chiusura.
- Nessun altro debito nuovo da E1 (bulk OK) o da contrasto.

---

## 7. Cosa NON hai fatto

- Nessun POST/reopen disposizione sul NAS; nessuna scrittura operativa.
- Nessun bump/deploy/merge/tag/force.
- Nessun ri-run gate w8/color/contrast/evidence/drift (codice prodotto invariato).
- Nessun fix focus-trap/Esc (reperto design).
- Nessuna modifica a T7, OBS-CURRENCY, `api/app/facts/`, FA251, Topology, `--inference*`, altre rotte.
- Nessun cablaggio `/ai`.
