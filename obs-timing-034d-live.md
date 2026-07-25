# OBS-TIMING-034d — live D0 (pre-code)

**Data:** 2026-07-25 ~12:11 CEST  
**GATE D0:** **PASS** (`/api/health` 200, version `0.10.25`)

---

## D0.1 — `docker compose ps`

```text
NAME                      IMAGE                       COMMAND                  SERVICE     CREATED        STATUS                    PORTS
observatory-api-1         observatory-api             "/entrypoint.sh"         api         2 hours ago    Up 11 minutes (healthy)   0.0.0.0:18000->8000/tcp
observatory-collector-1   observatory-collector       "python -m collector…"   collector   41 hours ago   Up 41 hours               
observatory-proxy-1       caddy:2.8-alpine            "caddy run --config …"   proxy       3 days ago     Up 3 days                 443/tcp, 2019/tcp, 443/udp, 0.0.0.0:8080->80/tcp
observatory-web-1         observatory-web             "/docker-entrypoint.…"   web         3 hours ago    Up 3 hours                80/tcp
observatory-zeek-1        observatory-zeek-ja4:prod   "/bin/sh /opt/observ…"   zeek        42 hours ago   Up 42 hours               
```

---

## D0.2 — health

```text
--- via Mac proxy :8080 ---
{"ok":true,"service":"observatory-api","version":"0.10.25"}
HTTP 200

--- via NAS 127.0.0.1:8080 (proxy) ---
{"ok":true,"service":"observatory-api","version":"0.10.25"}
HTTP 200

--- via NAS api diretto :18000 ---
{"ok":true,"service":"observatory-api","version":"0.10.25"}
HTTP 200
```

---

## D0.3 — bootstrap del restart C1.4 (righe, non riassunto)

Ultime 80 righe grezze erano solo traffico ingest (api già up). Bootstrap del boot `epoch=1784973635` (post stop+start C1.4):

```text
[timing] entrypoint_start epoch=1784973635 nesting=T_total_host contains T_import+T_bootstrap+T_uvicorn
[timing] T_import=0s (disgiunto: pre-bootstrap only; nested_in T_total=yes)
[bootstrap] step 1 schema: 0.2s
[bootstrap] step 2 snmp_cleanup: 0.0s
[bootstrap] utente admin già presente
[bootstrap] step 3 admin_user: 0.0s
[bootstrap] step 4 purge_placeholders: 0.0s
[bootstrap] skip import legacy
[bootstrap] step 5 legacy_import: 0.0s
[bootstrap] backup saltato (nessuna modifica infrastruttura)
[bootstrap] infrastruttura già riconciliata; conflitti=0
[bootstrap] step 6 infrastructure: 0.1s
[bootstrap] override ruolo SPAN già presenti
[bootstrap] step 7 span_overrides: 0.0s
[timing] T_trust start nesting=T_trust contains (T_dry_run[T_prefetch_obs+T_prefetch_fdb+T_plan_loop]+T_backup+T_apply); T_backup nested_in T_trust=yes
[timing] T_dry_run=5.3s (nested_in T_trust=yes) T_prefetch_obs=5.2s T_prefetch_fdb=0.0s T_plan_loop=0.1s T_dry_residuo=0.0s mode=prefetch queries=200
[bootstrap] trust dry_run: 5.3s mode=prefetch queries=200
[bootstrap] trust backup: 302.3s
[timing] T_backup=302.3s (nested_in T_trust=yes, after T_dry_run, needs_backup=True)
[bootstrap] trust apply: 3.8s
[timing] T_apply=3.8s (nested_in T_trust=yes, after T_backup)
[bootstrap] trust v0.4: confermati=80 noti=35 quarantena=26 proposte_archiviate=0 structural=53 timestamp_refresh=7 backup=/data/backups/observatory-20260725-120044-164566.db
[timing] T_trust=311.5s = T_dry_run 5.3 + T_backup 302.3 + T_apply 3.8 + T_residuo 0.1s
[timing] HYPOTHESIS T_trust≈T_backup+T_prefetch_obs+residuo → 302.3+5.2+4.0=311.5 (residuo_legacy includes fdb+plan+apply+wrap; T_residuo_trust_wrap=0.1s)
[bootstrap] step 8 trust: 311.5s
[bootstrap] backup saltato (nessuna modifica monitor)
[bootstrap] monitor già riconciliati
[bootstrap] step 9 monitors: 0.8s
[bootstrap] Cassiopea NIC 2 ritirati: archiviati=1 già=1
[bootstrap] step 10 nic2_retire: 0.1s
[bootstrap] chassis auto=15 changes=0 rule=2
[bootstrap] step 11 chassis: 2.3s
[timing] T_bootstrap_wall=327s (nested_in T_total=yes; contains T_trust)
[timing] entrypoint_exec_uvicorn elapsed_so_far=327s
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Lettura path (dai log):** `needs_backup=True` (riga T_backup); apply eseguito (`structural=53`); backup **non** saltato; durata trust **311.5 s** (di cui backup **302.3 s**).

---

## D0.4 — copia `observatory-*.db` di questo bootstrap

```text
-rw-r--r-- 1 root root 2786009088 Jul 25 12:01 data/backups/observatory-20260725-120044-164566.db
```

Nome coincide col path nel log trust. Size **2786009088** B (~2.60 GiB). Non cancellata.

Altre due presenti (keep-3):

```text
observatory-20260725-101810-501030.db  2747191296
observatory-20260725-093650-416110.db  2733641728
```

---

## D0.5 — `/tmp/obs_boot_timing.json`

```text
-rw-r--r-- 1 root root 23 Jul 25 12:00 /tmp/obs_boot_timing.json
CONTENTS:
MARKER_034c_1784973625
```

Il marker C1.4 **è ancora presente** (non sovrascritto dal bootstrap live: la strumentazione intermedia su 0.10.25 non scriveva il fragment JSON 034b/c). Non cancellato a mano — evidenza S2; il `rm -f` pre-bootstrap di 034c/d lo rimuoverà al prossimo boot deployato.

---

## Verifica `date +%s%N` (D3.1, container live)

```text
date +%s%N → 1784974328480027463   (supportato)
date +%s   → 1784974328
python time.time() → 1784974328.509522
```

Entrypoint 034d usa `python -c "… time.time() …"` per float diretto (2–3 spawn/boot).

---

## D4.2 — dichiarazione esecuzione test

- **Dove:** locale Mac, `/usr/bin/python3` → **Python 3.9.6** (non container api py3.12)
- **Comando:** `PYTHONPATH=api python3 -m pytest tests/test_boot_timing.py -v`
- **Collection:** 4 test in `tests/test_boot_timing.py` (file intero)
- **Esito:** **4 passed** in 0.06s
- **Non eseguita:** suite completa del repo (solo questo file). Non dichiarare «suite verde».
