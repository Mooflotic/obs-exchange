# OBS-EGRESS O13C — hybrid grain (finish / deploy)

**VERSION prod:** 0.10.79  
**Ramo:** `feature/obs-currency`  
**Natura:** abilitazione controllata `EGRESS_INGEST_ENABLED` + deploy `api`/`web`/`collector`.  
**FA 251:** intatto. **FLOW_INGEST / ZEEK_PROVIDER:** non riattivati.  
Nessun IP di destinazione / hostname / SNI in questo artefatto (solo aggregati).

---

## PREVISIONI (dichiarate PRIMA del deploy; riferimento misure O13B)

- creazioni al primo giorno: attese **4.292** (3.068 ext + 1.224 int), quindi cap attivo e baseline differita su ~3 giorni;
- creazioni/giorno a regime: attese **1.083** (841 ext + 242 int) — sotto 2.000;
- insieme attivo a 3 giorni: atteso **7.048**; proiezione 7 giorni **11.380** — sotto 20.000;
- MiB attesi: ≈2,9 a 3 giorni, ≈4,7 a 7 giorni — sotto 50;
- quota attesa di associazioni `uncertain` e `unresolved`, per dispositivo;
- card N5 attese al primo ciclo: **0** (baseline in costruzione);
- stato atteso della nuova sorgente in copertura dopo il primo ciclo.

**Se le creazioni osservate superano materialmente la previsione: kill switch, riporta, FERMATI.**

---

## Ambiente e deploy

| voce | valore |
|------|--------|
| WAVE_START_ISO | `2026-07-29T09:46:48Z` |
| `.env` backup (path only) | `.env.pre-o13c-20260729-114648` (mode `0644`) |
| chiavi aggiunte | solo `EGRESS_INGEST_ENABLED` (len 4=`true`) e `EGRESS_INGEST_INTERVAL_SEC` (len 3=`300`) |
| chiavi non toccate | `FLOW_INGEST_*`, `ZEEK_PROVIDER_*`, `ZEEK_BEHAVIOR_*` (len invariate; FLOW/PROVIDER assenti prima e dopo) |
| snapshot pre-deploy | `data/backups/pre-deploy-20260729-1146.db` |
| deploy | `./scripts/deploy.sh api web collector` + `force-recreate --no-deps collector`; web marker fix con `--no-cache` |

### Test pre-deploy

| suite | esito |
|-------|-------|
| `pytest tests/test_o13c_egress.py` | **9 passed** |
| `node --test src/oggiPriority.test.js` | **4 passed** (O13C P6 ext/int) |

---

## OSSERVATI

### Dimensione DB

| | byte | MiB |
|--|-----:|----:|
| BEFORE | 1 892 810 752 | 1805.125 |
| AFTER | 1 892 810 752 | 1805.125 |
| delta file | **0** (SQLite non restringe; crescita logica in tabella) |

### FA 251

`id=251` · `subject_type=chassis` · `subject_id=24` · `fact_key=asset.name` · `value_norm=LGS310C` · `source=manual` · `state=current` · `authority=100` — **invariato** a ogni checkpoint.

### Primo ciclo (trigger manuale post-enable)

| metrica | valore |
|---------|-------:|
| conn_rows | 30 175 |
| unique_keys posted | 1 791 |
| righe `egress_observations` dopo ciclo | **822** (ext **493** + int **328** + `_baseline` **1**) |
| create ext+int | **821** |
| vs previsione primo giorno 4 292 | **sotto** (−80 % circa) — **nessun kill switch** |
| cap 2 000/giorno | non raggiunto (`deferred=0`) |
| baseline | **ready** nello stesso ciclo (`deferred_creates==0`) — scarto vs «differita ~3 giorni» **[Corretto in O13C-FIX]** |
| card N5 / signals | **0** (novità solo `first_seen` *dopo* `baseline_ready_at`) — allineato alla previsione «0 al primo ciclo» sul piano novità post-baseline |
| breaker | **chiuso** |
| approx_bytes tabella | ~146 KiB ≪ 50 MiB |

**Scarto volume 821 vs 4292 [Corretto in O13C-FIX]:** causa dominante = finestra ~1 h / **30 175** conn vs **631 194**/day O13B (ratio ≈ **20.9**), **non** hybrid key collapse. Il grano ibrido contribuisce secondariamente; il corpus del primo ciclo era un pezzo del giorno O13B, non un collasso di chiavi.

### Associazione (aggregati, no IP)

| assoc_reason (post-crescita) | n |
|------------------------------|--:|
| fatto `asset.iface_ip` current copre observed_at | 408 |
| nessun fatto `asset.iface_ip` per questo IP | 79 |

| peer interni | n |
|--------------|--:|
| resolved_peer | 119 |
| unresolved_peer_ip_kept | 78 |

### Coverage (dopo primo ciclo)

| name | enabled | state | note |
|------|---------|-------|------|
| `zeek_egress` | true | **coperta_fresca** | flag `egress_ingest_enabled` |
| `zeek_conn_flow` | false | **disabilitata** | legacy; FLOW non riattivato |
| `zeek_behavior` | true | coperta_vecchia (age>cadenza al sample) | indipendente |

### SensorRun `zeek_egress`

Cicli OK osservati (counts aggregati): 1791 → 600 (post-P9) → 538 → 352 posted.

### Breaker (dopo cicli successivi)

`evaluate_egress_breaker` → **open=false**. Tetti invariati: 20 000 / 2 000 / 50 MiB.  
Tabella al momento del report (post-cicli schedulati): **rows_total≈423–488**, rows_today sotto 2 000, bytes ≪ 50 MiB.

### Contatori correlati (non O13C)

| | |
|--|--:|
| `fact_assertions` total / current | 2151 / 213 (drift organico live) |
| `zeek_behavior_evidence` | 520 |

---

## Rollback counts (P8 / P9)

### P8 — kill switch

| step | osservato |
|------|-----------|
| set `EGRESS_INGEST_ENABLED=false` + force-recreate collector | `egress_enabled=False`, `would_register_job=False` |
| COUNT T0 | **822** · SensorRun max id **11562** |
| COUNT T+120s | **822** · stesso max id — **invariato** |
| log `zeek_egress` post-recreate | assente |
| re-enable + recreate | `egress_enabled=True`, job registrabile |

### P9 — rollback dati + riapplicazione

| step | total | by scope |
|------|------:|----------|
| prima delete | 822 | `_baseline` 1, ext 493, int 328 |
| dopo delete (`evidence LIKE '%obs-o13c%'` OR ext/int ≥ WAVE_START) | **0** | *(vuoto — anche meta baseline eliminata perché marcata o13c)* |
| dopo re-enable + 1 ciclo | **324** | `_baseline` 1, ext 172, int 151 |
| crescita | **sì** | |

---

## Gate INTEGRAL

### Repo (`scripts/w8_currency_gate.py`)

```
file scansionati: 201
VIOLAZIONI: 0
RISULTATO: PASS (con 1 eccezione/i temporanea/e)
```

(eccezione temporanea `DEBT-WPGATE-CURRENCY-COUNT-LOCAL` — invariata rispetto a ondate precedenti)

### NAS

```
file scansionati: 202
VIOLAZIONI: 0
RISULTATO: PASS (con 1 eccezione/i temporanea/e)
```

Output integrale salvato in sessione: `docs/_o13c_gate_repo_integral.txt`, `docs/_o13c_gate_nas_integral.txt` (non in share).

---

## Drift

| | |
|--|--:|
| repo_scanned | 201 |
| nas_scanned | 202 |
| NAS−repo | **1** |
| solo NAS | `scripts/_w4a_measure.py` |
| solo repo | *(nessuno)* |

Allineato al pattern O13B (file misura NAS-only, non toccato).

---

## Markers proof (web :8080)

| voce | valore |
|------|--------|
| index asset | `/assets/index-C0zefVzT.js` |
| sha256 | `660c9eeaea036846f17f38a086d9d385285914420edfc53b61564d4864f562bb` |
| bytes | 441 312 |
| `obs-o13c-marker` count | **1** (proprietà live su `api`; commenti/`void` eliminati dal minify) |
| `data-o13c` count | **8** |
| health | `{"ok":true,"version":"0.10.79"}` |

---

## Screenshot

Harness Playwright viewport `dsf=1` (procedura O9; non `browser_take_screenshot`).  
`o9_png_assert.py --pair` **PASS** su tutte le coppie.

| file | WxH |
|------|-----|
| `obs-o13c-oggi-1280.png` | 1280×900 |
| `obs-o13c-oggi-768.png` | 768×900 |
| `obs-o13c-oggi-390.png` | 390×900 |
| `obs-o13c-dossier-1280.png` | 1280×900 |
| `obs-o13c-dossier-768.png` | 768×900 |
| `obs-o13c-dossier-390.png` | 390×900 |

Dossier: asset id **28** (membro chassis con traffico egress; nessun IP stampato).

---

## Criteria checklist

| id | criterio | esito |
|----|----------|-------|
| P1 | dispositivo noto → destinazioni ext host/porta/proto, freschezza, qualità assoc | **OK** (store+Dossier; qualità via `assoc_reason` aggregata) |
| P2 | relazione int `A↔B` senza porta | **OK** (grano int; 197 relazioni a regime report) |
| P3 | peer unresolved → IP conservato, no soggetto inventato | **OK** (78 unresolved_peer_ip_kept) |
| P4 | assoc non corrente / valid_from → uncertain | **OK** in test; prod: 79 senza fatto iface_ip |
| P5 | baseline in costruzione → no card N5 | **OK** (signals=0; baseline chiusa subito per deferred=0) |
| P6 | cap differisce senza perdita | **OK** in test; prod: cap non morso (821≪2000) |
| P7 | breaker ferma scrittura | **OK** in test; prod: breaker chiuso, sotto tetti |
| P8 | kill switch osservato in prod | **OK** (job assente, 822 invariato 120s) |
| P9 | rollback → 0 poi riapplicazione cresce | **OK** (822→0→324) |
| P10 | novità post-baseline → card | **OK** in test; prod: 0 card subito dopo ready (atteso: novità solo post-ready) |
| N2 cap≠breaker | funzioni e contatori separati | **OK** |
| N3 baseline visibile | data inizio + seen/created/deferred | **OK** API/UI marker |
| N4 Dossier Cosa fa | ext+int, freschezza, no hub nuovo | **OK** (`data-o13c`) |
| volume vs previsione | non superare materialmente 4292/1083 | **OK** (sotto; nessun STOP) |

---

## Diff tematici (share)

- `obs-o13c-store.diff.txt` — store/ingest/collector/retention/config/test/VERSION/CHANGELOG
- `obs-o13c-egress.diff.txt` — Dossier / behaviour / api.js / observatoryUx
- `obs-o13c-segnale.diff.txt` — novelty/signals / Oggi / oggiPriority / coverage

---

## Cosa NON è stato fatto

- Nessun raise di tetti
- Nessun ripristino `FLOW_INGEST_ENABLED` / `ZEEK_PROVIDER_ENABLED`
- Nessuna modifica a `scripts/_w4a_measure.py`
- Nessun IP destinazione in report o assert stampati
