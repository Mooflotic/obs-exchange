# FASE A — Docker layers + cronometro deploy + crescita DB

**Data:** 2026-07-24 · **Sola lettura** (misure timed: snapshot rimosso dopo misura; build cache hit; container già Running)  
**Live DB:** ~2.55 GiB · Cassiopea `/volume1` (HDD)

---

## D1 — Dockerfile api (integrale)

```dockerfile
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl iputils-ping \
    && rm -rf /var/lib/apt/lists/*

COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/app ./app
COPY api/alembic.ini ./alembic.ini
COPY api/entrypoint.sh /entrypoint.sh
COPY VERSION /VERSION
RUN chmod +x /entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
```

**Risposta secca:** le dipendenze stanno in un layer **separato e anteriore** (`COPY requirements.txt` → `RUN pip install`, **poi** `COPY api/app`).

Un deploy che cambia **solo** codice Python (requirements invariato) **non** rifà il `pip install`: il layer pip resta `CACHED` (verificato nel build a vuoto sotto). Si invalidano solo i layer da `COPY api/app` in poi.

(Simmetrico sul web: `COPY package.json` → `npm install` → poi `COPY web/`.)

---

## D2 — Cache vs rebuild da zero

| Voce | Valore |
|------|--------|
| `deploy.sh` | `docker compose up -d --build --no-deps …` |
| `--no-cache` | **assente** → usa build cache |
| `docker system prune` / build pulita | **assente** nel flusso |
| `--no-deps` | sì (già noto) |

A vuoto (nessun cambio codice): layer tutti `CACHED`; build wall-clock ~6 s (metadata + export), non pip/npm da zero.

---

## D3 — Cronometro deploy a vuoto (timestamp reali UTC)

Metodo: stesse operazioni di `deploy.sh` a fasi; snapshot di misura **cancellato** subito dopo (no crescita `data/backups`).  
`up --no-build`: immagine invariata → container **già Running** (no bootstrap freddo).

### API

| Fase | Start → End | Durata |
|------|-------------|--------|
| Snapshot DB | `21:20:09` → `21:20:31` | **20.18 s** (`SNAPSHOT_SEC`; size 2 658 127 872 B) |
| Build immagine | `21:20:32` → `21:20:38` | **5.82 s** (`BUILD_ELAPSED`; pip **CACHED**) |
| up + `/api/health` | `21:20:38` → `21:20:44` | **~6 s** (container Running; health `0.10.21`) |

Rsync (fuori dalle tre fasi richieste): ~1 s.

### Web

| Fase | Start → End | Durata |
|------|-------------|--------|
| Snapshot DB | `21:21:00` → `21:21:22` | **21.61 s** |
| Build immagine | `21:21:23` → `21:21:30` | **6.47 s** (npm/build **CACHED**) |
| up + HTTP :8080 | `21:21:30` → `21:21:31` | **~1 s** (200) |

**Snapshot su deploy solo-web = tempo sprecato:** **~22 s** a DB attuale (~2.5 GiB), a fronte di ~7 s di lavoro utile (build+up). Su HDD cresce con la size del DB.

Nota: un deploy api **con** cambio codice / nuova immagine che **ricrea** il container paga anche bootstrap (trust dry_run ecc., minuti) — fuori misura «a vuoto».

---

## D4 — Chi mangia i 2.5 GB

`dbstat` (container api) — top per `pgsize`:

| MiB | Oggetto |
|----:|---------|
| **1308.3** | **`observations_raw`** |
| **778.1** | **`observations`** (legacy) |
| 60.9 | ix `observations_raw` dedup_key |
| 49.3 | ix `obsraw` entity_ts |
| 37.3 | ix `observations` seen_at (×2 nomi) |
| 34.3 | ix `obsraw` source_ts |
| 29.3 | ix `observations_raw` observed_at |
| 27.2 | ix `observations_raw` entity_key |
| 26.9 | ix `observations` mac |
| 21.4 | **`flow_observations`** |

Somma grezza tabelle+indici osservazioni ≈ **~2.3 GiB** del file ~2.55 GiB.

| Tabella | Righe | Finestra | Retention nel codice |
|---------|------:|----------|----------------------|
| `observations_raw` | ~765k | 2026-07-20 → oggi (~5g) | sì: TTL raw **7g** → rollup → delete (`retention.py` / `OBS_TTL_RAW_DAYS`) |
| `observations` | ~975k | 2026-07-17 → oggi (~7g) | **no** — non toccata da `run_retention` |
| `flow_observations` | ~52k | ~3g | sì: 30g |
| `heartbeats` | ~74k | ~7g | sì |
| `ip_intel` | ~5k | — | piccolo |
| `observations_aggregate` | **0** | — | rollup non ha ancora prodotto aggregati (nulla oltre TTL 7g) |

Raw per source (top): **fritz ~731k**, nmap ~28k, ssdp ~5k.

### Da dove il raddoppio 1.2 → 2.5 GB

1. **Doppia scrittura append-heavy:** legacy `observations` (~778 MiB, **senza purge**) + store M1 `observations_raw` (~1.3 GiB, TTL 7g ma ancora tutto dentro la finestra).
2. Indici su entrambe le tabelle (~200+ MiB).
3. `flow_observations` / heartbeats / ip_intel: **non** la causa del raddoppio.
4. Finché `observations` legacy cresce senza retention, **nessuna ottimizzazione di deploy** riduce il DB; al massimo lo snapshot pre-deploy diventa più lento (~20 s oggi, lineare con la size).

---

## Implicazioni (solo lettura — decide dopo)

- Ottimizzare deploy: skip snapshot su `web`/`collector`; layer deps già ok.
- Retention: problema strutturale su **`observations` legacy** (+ raw ancora sotto TTL).
