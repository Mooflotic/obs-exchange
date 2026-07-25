# OBS-TIMING-034c — recon C1 (read-only)

**Data:** 2026-07-25  
**Host:** Cassiopea, container `observatory-api-1`  
**VERSION live al momento della prova:** health/proxy poteva essere 502 (bootstrap in corso dopo stop+start C1.4); file `/VERSION` nel container = `0.10.25`.

---

## C1.1 — path VERSION nell’immagine / live

**Dockerfile** (`api/Dockerfile` riga 16):

```text
COPY VERSION /VERSION
```

**docker-compose.yml** (bind aggiuntivo):

```text
- ./VERSION:/VERSION:ro
```

**Prova live:**

```text
ls -la /VERSION
-rw-r--r-- 1 1001 users 8 Jul 25 09:33 /VERSION

cat /VERSION
0.10.25

find / -name VERSION -type f
/VERSION

mount | grep VERSION
/dev/mapper/md1_c on /VERSION type btrfs (ro,...,subvol=/base)
```

**Esito testuale:** `/VERSION` esiste nel container live e contiene `0.10.25`. È il path reale (unico trovato). Il mount btrfs conferma il bind compose sul file host.

---

## C1.2 — BOOTSTRAP_BACKUP

| Fonte | Valore osservato |
|-------|------------------|
| `docker-compose.yml` | nessun `BOOTSTRAP_BACKUP` (né in `environment:`) |
| `.env` host produzione | riga assente (`BOOTSTRAP_BACKUP not set in .env`) |
| env nel container | `BOOTSTRAP_BACKUP=<unset>`; `env \| grep -i BOOTSTRAP` → vuoto |
| default codice | `settings.bootstrap_backup: str = "auto"` in `config.py` |
| `.env.example` | `BOOTSTRAP_BACKUP=auto` (documentazione, non live) |

**Chi vince:** unset in compose/env → **default codice `auto`**.

**GATE C1:** `BOOTSTRAP_BACKUP=always` **non** osservato → si può procedere a C2.

---

## C1.3 — `data/backups`

| Prefisso | count | total_bytes | total_GiB |
|----------|-------|-------------|-----------|
| `pre-deploy-*.db` | 3 | 8087683072 | 7.532 |
| `observatory-*.db` | 3 | 8158060544 | 7.598 |

Directory intera `data/backups`: **18924423357** bytes (~17.6 GiB).

**5 mtime più recenti `pre-deploy-*.db`** (ne esistono solo 3):

| mtime epoch | size | name |
|-------------|------|------|
| 1784964870 | 2733228032 | pre-deploy-20260725-0934.db |
| 1784935418 | 2677227520 | pre-deploy-20260725-0123.db |
| 1784934452 | 2677227520 | pre-deploy-20260725-0107.db |

**5 mtime più recenti `observatory-*.db`** (ne esistono solo 3):

| mtime epoch | size | name |
|-------------|------|------|
| 1784967519 | 2747191296 | observatory-20260725-101810-501030.db |
| 1784965035 | 2733641728 | observatory-20260725-093650-416110.db |
| 1784935552 | 2677227520 | observatory-20260725-012529-521712.db |

**Nota testuale:** i nomi `observatory-*` hanno timestamp ~10:18 e ~09:36 del 25/07; i `pre-deploy-*` più recenti ~09:34. Non si afferma qui la correlazione restart↔copia (osservazione sola; rotazione fuori perimetro).

---

## C1.4 — sopravvivenza `/tmp/obs_boot_timing.json` a stop+start

**Prima:**

```text
echo MARKER_034c_1784973625 > /tmp/obs_boot_timing.json
# CONTENTS: MARKER_034c_1784973625
```

**Operazione:** `docker compose stop api` poi `docker compose start api` (stesso container, no recreate).

**Dopo start:**

```text
ls -la /tmp/obs_boot_timing.json
-rw-r--r-- 1 root root 23 Jul 25 12:00 /tmp/obs_boot_timing.json

cat /tmp/obs_boot_timing.json
MARKER_034c_1784973625
```

**Esito testuale:** il file **sopravvive** a `compose stop`+`start` con contenuto invariato.

---

## GATE C1

| Check | Esito |
|-------|--------|
| C1.2 ≠ `always` | **PASS** (vince `auto`) |
| Procedere a C2 | **SÌ** |
