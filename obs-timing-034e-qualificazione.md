# OBS-TIMING-034e — qualificazione (STOP su P2)

**Data:** 2026-07-25  
**Commit deployato:** `5fa03d8` + `84cda6f` (F-1 test/docs) su branch `feature/obs-db-slim`  
**Live post-deploy:** `/api/health` → **0.10.26**  
**3b-iii / 4b:** CONGELATI

Previsioni immutabili: [obs-timing-034e-predictions-predeploy.md](https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-timing-034e-predictions-predeploy.md)

---

## F0.2 — quarto file (ipotesi delta)

`ls -la data/backups` completo ha mostrato:

```text
2676768768  pre-db-slim-p1-20260724-221514.db
```

= **2.493 GiB**. L’ipotesi «quarto file ≈ 2.494 GiB» è **CONFERMATA** (prefisso `pre-db-slim-p1-`, non `.bak`). Residual dopo pre+obs+p1 ≈ **1.9 MiB** (json/log). Nessuna cancellazione.

---

## P1–P8 — osservato vs previsto

| ID | Previsto | Osservato | Esito |
|----|----------|-----------|-------|
| P1 | Snapshot ~2.8 GiB in **280–330 s** @ 9–10 MB/s | `pre-deploy-20260725-1319.db` size **2816585728** B; `deploy.sh` wall **112 s** (snapshot+rsync+build+start — **nessun timer dedicato al solo snapshot**). Throughput se si attribuisse tutto lo wall allo snapshot: ~25 MB/s (inferito, non misurato puro). | **DIVERGE** (più veloce del range); non bloccante da solo |
| P2 | T_prefetch_obs **≥ 40 s** | **19.716 s** | **FALSIFICATA** (&lt;20 s) → **STOP** |
| P3 | health **0.10.26** | proxy+diretto `{"ok":true,"version":"0.10.26"}` | **PASS** |
| P4 | 1× `[timing]{json}`; needs_* non null; no stale/missing | Una riga JSON; `needs_apply=true`, `needs_backup=true`; stale/missing assenti | **PASS** |
| P5 | niente MARKER; fragment = boot corrente | Fragment 277 B, `epoch_start=1784978465.819` = riga timing; MARKER assente | **PASS** |
| P6 | needs_apply qualunque | `needs_apply=true` (registrato) | **PASS** (non anomalia) |
| P7 | assets=151, ip_current=99 | assets=**151**, ip_current=**99**; observations 1055284→**1055564** (+280 durante finestra) | **PASS** su asset/IP; obs cresciute (ingest) |
| P8 | uvicorn PID 1 | `/proc/1/cmdline` = `python3.12 … uvicorn app.main:app …` | **PASS** |

### Riga `[timing]` post-deploy (boot D)

```json
{"event":"api_boot","version":"0.10.26","epoch_start":1784978465.819,"epoch_import_end":1784978465.863,"epoch_bootstrap_end":1784978809.591,"epoch_ready":1784978813.762,"needs_backup":true,"needs_apply":true,"t_total_level_check":"identity","timers":{"T_total":{"s":347.943,"parent":null},"T_import":{"s":0.044,"parent":"T_total"},"T_bootstrap_wall":{"s":343.728,"parent":"T_total"},"T_uvicorn_to_ready":{"s":4.171,"parent":"T_total"},"T_trust":{"s":331.275,"parent":"T_bootstrap_wall"},"T_dry_run":{"s":20.079,"parent":"T_trust"},"T_prefetch_obs":{"s":19.716,"parent":"T_dry_run"},"T_prefetch_fdb":{"s":0.196,"parent":"T_dry_run"},"T_plan_loop":{"s":0.166,"parent":"T_dry_run"},"T_dry_residuo":{"s":0.001,"parent":"T_dry_run"},"T_backup":{"s":307.942,"parent":"T_trust"},"T_apply":{"s":3.253,"parent":"T_trust"},"T_residuo_trust":{"s":0.001,"parent":"T_trust"}}}
```

### Cross-check JSON ↔ prosa bootstrap (S2 end-to-end)

| Componente | Prosa `[bootstrap]` | JSON `[timing]` |
|------------|---------------------|-----------------|
| dry_run | 20.1 s | 20.079 s |
| backup | 307.9 s | 307.942 s |
| apply | 3.3 s | 3.253 s |

**Allineati** (arrotondamento prosa a 1 decimale). Merge fragment↔epoch **OK in produzione**.

---

## P2 — ipotesi cache FALSIFICATA

**Previsione:** dopo snapshot integrale pre-deploy, primo boot → T_prefetch_obs ≥ 40 s.  
**Osservato:** **19.716 s** (&lt; 20 s soglia di falsificazione).

**STOP.** Nessun passo G (RUN_A/B/C). Nessuna riformulazione a posteriori.

### Ipotesi alternative candidate (non verificate)

1. **Contesa col writer** — collector/ingest attivi durante il prefetch; I/O non solo sequenziale caldo/freddo.
2. **Stato WAL** — WAL pre-deploy 9.3 MiB; checkpoint/merge durante bootstrap altera il costo di lettura.
3. **Retention / job concorrenti** — prune orario o altri lettori sul DB durante il boot.
4. **Crescita / forma tabella** — `observations` ~1.05M righe; il costo non è dominato solo dalla residenza in page cache del file intero.
5. **Snapshot non ha sfrattato la cache come atteso** — lo snapshot pre-deploy (~2.8 GiB) è più veloce del previsto (wall deploy 112 s): possibile che le pagine restino calde o che il path di copia non invaldi la cache come un `cat` sequenziale freddo.
6. **Prefetch non legge l’intero heap observations** — query aggregata/indice; banda “alta” da run storiche (48 s) non è equivalente a “cold full scan”.

---

## G1–G7 — NON ESEGUITI

Bloccati da P2 FAIL. Tabella storica 0.10.25 resta in `obs-3b-iii-baseline-034.md` / note 034b; bande provvisorie 5.2–48.3 s **non certificate** da questo deploy.

### Serie throughput backup (solo punti noti + questo boot)

| timestamp | size B | T_backup s | MB/s |
|-----------|--------|------------|------|
| (report pre-034) | 2733641728 | 263.7 | **10.37** |
| 2026-07-25 12:00 | 2786009088 | 302.3 | **9.22** |
| 2026-07-25 13:21 (questo deploy) | 2817433600 | 307.942 | **9.15** |

Tendenza: throughput in **lieve calo** (10.37 → 9.22 → 9.15 MB/s) mentre la taglia sale. Fatto registrato; **nessuna conclusione di causa**. Rilevante per l’assunto §9/§11 su 4b.

---

## Metro F1–F4

**Non aggiornato con bande certificate** (G non corso). Restano come da piano 034b:

- **F1** (bloccante, post-3b-iii): `T_prefetch_obs` **assente** come componente
- **F2** (bloccante): `T_dry_run` &lt; 2 s su qualsiasi cache
- **F3** (indicativo): guadagno T_total = intervallo fondo–ceiling — **non certificato**
- **F4**: confrontare solo stesso `needs_apply`

---

## F-1 eseguito pre-deploy

- Commit `84cda6f` — guardie S2 ripristinate; doc `T_import`
- Test: **6 passed**, locale Mac **Python 3.9.6**, solo `tests/test_boot_timing.py`
- Diff: https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-timing-034e-f1.diff.txt

---

## STOP

Ipotesi page-cache per T_prefetch_obs **falsificata** al primo boot 0.10.26.  
Attendere review / GO prima di G o di riaprire 3b-iii. Non iniziare 4b.
