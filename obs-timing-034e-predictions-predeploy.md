# OBS-TIMING-034e — previsioni F1 (SCRITTE PRIMA DEL DEPLOY)

**Scritto:** 2026-07-25, prima di `./scripts/deploy.sh api web`  
**VERSION target:** 0.10.26  
**Baseline live pre-deploy:** 0.10.25

## F0 snapshot (misurato)

| Voce | Valore |
|------|--------|
| observatory.db | **2816573440** B |
| WAL | **9335952** B |
| SHM | **32768** B |
| `/volume1` libero | **5.2T** (df) |
| assets_total | **151** |
| ip_addresses is_current=1 | **99** |
| observations (legacy) | **1055284** |
| presence_sources | **tabella assente** su live 0.10.25 (registrato) |
| /tmp fragment | `MARKER_034c_1784973625` |

**Quarto file (ipotesi delta):** CONFERMATO da `ls` completo — `pre-db-slim-p1-20260724-221514.db` = **2676768768 B** = **2.493 GiB**. Residual directory dopo pre+obs+p1 ≈ 1.9 MiB (json/log).

## Previsioni (immutabili dopo questo punto)

| ID | Previsione |
|----|------------|
| P1 | Snapshot pre-deploy ~2.8 GiB, tempo **280–330 s** @ ~9–10 MB/s |
| P2 | Primo boot 0.10.26: **T_prefetch_obs ≥ 40 s** (banda alta). Se **&lt;20 s** → ipotesi cache **FALSIFICATA**, STOP |
| P3 | `/api/health` = **0.10.26** (proxy + diretto) |
| P4 | Una riga `[timing] {json}`; needs_apply/needs_backup **non null**; no stale/missing |
| P5 | `/tmp/obs_boot_timing.json` non più MARKER; fragment JSON con epoch_start = riga timing |
| P6 | needs_apply True o False: **nessuno** è anomalia — solo registrare |
| P7 | assets=151, ip_current=99, observations≈1055284 (tolleranza: observations può crescere leggermente durante deploy; asset/ip_current identici) |
| P8 | `uvicorn` è **PID 1** nel container (`ps`) |
