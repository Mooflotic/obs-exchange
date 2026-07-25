# OBS-4a-plan — VACUUM parziale: ricognizione + piano finestra

**Data:** 2026-07-25 · **Live:** 0.10.25 · **Scope:** sola lettura  
**STOP:** nessun VACUUM · nessuno stop container · nessuna modifica · nessun deploy

Contesto: 4a dovrebbe compattare freelist già liberata (indici passo 1 + TTL), **senza** toccare la legacy `observations` (dual-write ancora acceso). Qui il piano e le misure live.

---

## A · Chi scrive sul DB

### A1 · Mappa writer / non-writer

| Servizio | Apre `observatory.db`? | Scrive? | Frequenza | Dove |
|----------|------------------------|---------|-----------|------|
| **api** | Sì (RW, WAL) | **Sì — unico writer SQL** | Continuo: ingest collector + UI | `db.py:25-37` engine; `materialize.py:82` `record_observation`; `ingest.py` POST (observations, fdb, scans, retention-run, reliability-snapshot, …); job retention via `ingest.py:522-540` |
| **collector** | Sì, ma **solo RO** (zeek IP resolve) | **No SQL write** — scrive via HTTP→api | Discovery **900s**; topology **60s**; scan-jobs **3s**; retention trigger **3600s**; checks ~60s; NAS SNMP 300/3600s | POST ingest: `providers/base.py:163`, `main.py` (fritz/fdb/scans/retention…); RO: `zeek_conn.py:202-216` `mode=ro` |
| **zeek** | **No** | No (solo log file `/data/zeek`) | Continuo su eth1 | `docker-compose.yml:116-139` — volume solo `zeek-logs` |
| **web** | **No** | No SQLite — SPA Vue → HTTP api | Su richiesta utente | nginx static; mute/scan/UI passano dall’api |
| **proxy** (Caddy) | **No** | No | Reverse proxy | `8080→api/web` |
| **retention / metric snapshot** | Via **api** | Sì (DELETE/INSERT) | Collector chiama api ogni **~1h** | `collector/main.py:489-497`, `634-638`; `ingest.py:522-552` |
| **postgres / ai** | N/A | spenti (profiles) | — | — |

**Live write proxy (2026-07-25 ~09:47):**

| Finestra | `observations` | `observations_raw` |
|----------|---------------:|-------------------:|
| 10 min | 562 | 562 |
| 60 min | 4660 | 4697 |

≈ **500–700 insert legacy+raw / 10 min** in questo slot (ordine di grandezza allineato al “~1700/10min” di carico alto; qui più basso).

### A2 · Cosa fermare per VACUUM

| Fermare | Perché |
|---------|--------|
| **collector** | Genera tutto il traffico ingest; apre anche SQLite **RO** (può bloccare exclusive lock) |
| **api** | Unico writer; tiene connessioni WAL aperte |
| **Non fermare web** | Solo static/HTTP; non apre il DB |
| **Non fermare proxy** | Idem; UI resta “su” ma api down → errori temporanei |
| **Non fermare zeek** | Non tocca SQLite (solo file log). Opzionale: lasciarlo su evita buco conn.log |

### A3 · Comandi stop/start (ordine)

```bash
# STOP (ordine obbligatorio: prima chi genera carico, poi il holder del DB)
sudo docker compose stop collector
sudo docker compose stop api

# … finestra VACUUM (sez. C) …

# START (api prima: health; poi collector — dipende da api healthy)
sudo docker compose start api
# attendere healthy (healthcheck start_period 180s, di solito molto prima)
sudo docker compose start collector
```

- **Ordine conta:** collector prima in stop (smette di martellare api); api prima in start (collector `depends_on: service_healthy`).
- Nessun flag “pausa scrittura” dedicato: stop container è il gate pulito.
- `restart: unless-stopped` non riavvia da solo dopo `stop` finché non fai `start`/`up`.

---

## B · Dimensione e durata

### B1 · Freelist ATTUALE (guadagno atteso 4a)

| Metrica | Valore live |
|---------|-------------|
| `page_size` | **4096** |
| `freelist_count` | **3** |
| freelist bytes | **12 288** ≈ **0.01 MiB** |
| file OS | **2 735 460 352** ≈ **2.55 GiB** |
| `page_count` | 667 841 |
| WAL | **7.2 MiB** |
| `journal_mode` | wal |

**Verdetto B1 (critico):** il ~**98.9 MiB** di freelist post-passo 1 **non c’è più**. I writer (dual-write + raw, migliaia di insert/ora) hanno **riusato** quelle pagine. Post-p2 la freelist era salita (~22k pagine) e poi di nuovo consumata.  
**Guadagno atteso di un VACUUM OGGI ≈ 0.01 MiB di freelist** — non 78 MiB. Il file resta ~2.55 GiB perché lo spazio “liberato” dagli indici è di nuovo pieno di dati vivi.

4a resta tecnicamente eseguibile (riscrittura + eventuale micro-frammentazione), ma **non è cost-effective** finché la freelist non torna sostanziosa (es. dopo il regime TTL ~180–220k delete/giorno senza riuso immediato, o dopo stop dual-write 3b-iii).

### B2 · Durata stimata VACUUM INTO (~2.55 GiB, HDD md1 RAID1)

| Proxy | Tempo | Note |
|-------|------:|------|
| `sqlite3.backup` stesso volume (misura live oggi) | **32.7 s** | ~80 MiB/s — **lower bound** (copia sequenziale) |
| Trust bootstrap backup (log 0.10.25 deploy) | **198 s** | I/O sotto carico concurrente |
| VACUUM INTO (stima) | **2–8 min** | riscrittura + indici; tipico **3–6 min**; coda **8–12 min** se md1 impegnato |

Range onesto downtime totale (stop→start): **3–12 minuti** (vedi C3).

### B3 · Spazio libero

| Volume | Size | Avail | |
|--------|------|------:|---|
| `/volume1` (md1_c) | 7.3T | **5.2T** | OK ≫ 2.5 GiB per `observatory-slim.db` |

Nota: `/tmp` è **tmpfs 1.9G pieno al 100%** — **non** usare `/tmp` per slim/backup. Solo sotto `data/db/` o `data/backups/`.

---

## C · Sequenza della finestra (piano, NON eseguire)

### C1 · Passi e comandi

Path: `/volume1/Docker/observatory` (terminale già lì).

```bash
# --- 0. precondizione ---
# freelist_count * page_size  >>  1 MiB   altrimenti rinviare (vedi B1/D1)
# df -h /volume1  → Avail ≥ 3G
# nessun altro client sqlite sul file

# --- 1. snapshot pre-op (rete di sicurezza) ---
STAMP=$(date +%Y%m%d-%H%M)
python3 - <<PY
import os, sqlite3
src, dest = "data/db/observatory.db", f"data/backups/pre-vacuum-4a-{os.environ.get('STAMP','manual')}.db"
# meglio: dest con STAMP shell
PY
# Variante pratica (stesso pattern deploy.sh):
python3 - <<'PY'
import os, sqlite3, time
stamp = time.strftime("%Y%m%d-%H%M")
dest = f"data/backups/pre-vacuum-4a-{stamp}.db"
dst = sqlite3.connect(dest)
src = sqlite3.connect("file:data/db/observatory.db?mode=ro", uri=True)
src.backup(dst); dst.close(); src.close()
print("SNAPSHOT", dest, os.path.getsize(dest))
PY

# --- 2. stop writer ---
sudo docker compose stop collector
sudo docker compose stop api

# --- 3. checkpoint WAL (SÌ: confluire prima del VACUUM INTO) ---
sqlite3 data/db/observatory.db 'PRAGMA wal_checkpoint(TRUNCATE);'
# atteso: wal piccolo/azzerato; nessun altro processo agganciato

# --- 4. VACUUM INTO (crea file nuovo; originale intatto) ---
sqlite3 data/db/observatory.db "VACUUM INTO 'data/db/observatory-slim.db';"

# --- 5. verifica PRIMA dello swap (gate hard) ---
sqlite3 data/db/observatory-slim.db 'PRAGMA integrity_check;'
# deve stampare: ok

python3 - <<'PY'
import sqlite3
a = sqlite3.connect("file:data/db/observatory.db?mode=ro", uri=True)
b = sqlite3.connect("file:data/db/observatory-slim.db?mode=ro", uri=True)
tables = ["observations", "observations_raw", "assets", "name_proposals"]
for t in tables:
    ca = a.execute(f"select count(*) from {t}").fetchone()[0]
    cb = b.execute(f"select count(*) from {t}").fetchone()[0]
    print(t, ca, cb, "OK" if ca == cb else "FAIL")
    assert ca == cb, t
print("COUNTS_MATCH")
PY
# se FAIL → STOP qui: rm data/db/observatory-slim.db; restart api+collector; originale intatto

# --- 6. swap ---
mv data/db/observatory.db data/db/observatory-pre-vacuum-4a-${STAMP}.bak
mv data/db/observatory-slim.db data/db/observatory.db
# rimuovere residui wal/shm dell’originale se presenti (dopo checkpoint dovrebbero essere vuoti)
rm -f data/db/observatory.db-wal data/db/observatory.db-shm
# (api in WAL recreerà wal al primo connect)

# --- 7. restart writer ---
sudo docker compose start api
# attendere: curl -sS http://127.0.0.1:18000/api/health → version 0.10.25
sudo docker compose start collector

# --- 8. assert ---
curl -sS http://127.0.0.1:8080/api/health
ls -lah data/db/observatory.db   # size ≤ pre (oggi ≈ uguale se freelist≈0)
# riconteggio tabelle vs snapshot se utile
```

### C2 · Rollback per passo

| Passo | Se fallisce | Originale |
|-------|-------------|-----------|
| 1 snapshot | abort | intatto |
| 2 stop | `start` di nuovo | intatto |
| 3 checkpoint | restart servizi | intatto |
| 4 VACUUM INTO | `rm observatory-slim.db`; restart | **intatto** (INTO non sovrascrive) |
| 5 integrity/conteggi | `rm slim`; restart; **niente swap** | **intatto** |
| 6 swap | ripristino: `mv .bak → observatory.db` | recuperabile da `.bak` + snapshot |
| 7–8 restart/assert | fix servizi; DB già swappato | `.bak` + `pre-vacuum-4a-*.db` |

**Conferma:** fino al passo 5 incluso lo swap non è avvenuto → originale intatto. C2 = sì.

### C3 · Downtime stimato

| Fase | Range |
|------|------:|
| stop collector+api | 10–40 s |
| checkpoint | &lt; 30 s |
| VACUUM INTO | **2–8 min** |
| verify + swap | 30–90 s |
| api healthy + collector up | 30 s – 3 min |
| **Totale writer fermi** | **~3–12 min** |

Michele sceglie la finestra in base a questo range (notte / basso traffico).

---

## D · Interferenza con la calibrazione

### D1 · Verdetto

Live calib: **day 6/14**, `started_at=2026-07-20`, `scoring_calibrated=False`. Clock = giorni da min(MetricSnapshot, SensorRun) — **non** dipende dal freelist. Snapshot metriche ≈ **1/ora** (`metric_snapshots_24h=24`). Detectors **off**.

| Effetto buco N minuti | Impatto calib |
|----------------------|---------------|
| Clock day N/14 | **Nullo** (granularità giorno) |
| 1 snapshot metriche saltato | Buco 1 punto nella serie presence/coverage/flap — **rumore minore** su 14 giorni |
| Presence stale temporanea | Si riallinea al primo ciclo post-restart (~minuti) |
| Detectors shadow | Non girano già |

**Però:** con freelist ≈ **0.01 MiB**, aprire 3–12 min di buco **ora** non compra spazio.  
**Verdetto D1:**  
- **Non conviene fare 4a ORA** solo per “chiudere il cantiere”: costo calib/raccolta > guadagno.  
- **Aspettare** una di: (1) freelist di nuovo ≫ decine di MiB dopo prune TTL a regime (~da **2026-07-27** in poi, quando Jul 20 esce dalla finestra 7g e i delete superano il riuso), oppure (2) post **3b-iii** (stop dual-write) + prune grosso, oppure (3) finestra notturna **solo se** B1 mostra freelist sostanziosa al re-check.  
- Se un giorno B1 ≥ ~50 MiB e serve spazio file OS: 4a **si può** fare anche in calibrazione (buco &lt;15 min accettabile sul day-clock); preferire basso traffico.

---

## Sintesi per la decisione

1. **Writer da fermare:** `collector` + `api`. Web/proxy/zeek no.  
2. **Guadagno oggi:** ≈ **0 MiB** (freelist riusata) — 4a non paga.  
3. **Sequenza C1** pronta; rollback safe fino a pre-swap.  
4. **Downtime:** 3–12 min.  
5. **D1:** rinviare 4a finché freelist non ricresce; non urgente rispetto a calibrazione.

**STOP** — nessuna esecuzione. Sul re-check freelist + D1 Michele sceglie QUANDO aprire la finestra; il prompt successivo sarà l’esecuzione (solo se B1 lo giustifica).
