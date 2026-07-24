# OBS-DB-SLIM · Passo 1 — indici duplicati · STOP pre-esecuzione

Branch: `feature/obs-db-slim` · live oggi **0.10.22** · file **~2.49 GiB** · freelist ≈ 12 KiB · `auto_vacuum=0`.

**Nessun DROP eseguito.** Review → **GO** per lanciare lo script.

Script: [`obs_db_slim_p1_drop_dup_indexes.py`](https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs_db_slim_p1_drop_dup_indexes.py)  
(anche in repo: `observatory/scripts/obs_db_slim_p1_drop_dup_indexes.py`)

---

## 1 · Coppie ridondanti (FASE A)

### Coppia A — `observations_raw.dedup_key` (UNIQUE ×2)

| Indice | CREATE / origine | Colonne |
|--------|------------------|---------|
| **`sqlite_autoindex_observations_raw_1`** | implicito da `CONSTRAINT uq_observation_raw_dedup UNIQUE (dedup_key)` | `(dedup_key)` UNIQUE |
| **`ix_observations_raw_dedup_key`** | `CREATE UNIQUE INDEX ix_observations_raw_dedup_key ON observations_raw (dedup_key)` | `(dedup_key)` UNIQUE |

Stesso prefisso (identici). Causa modello: `UniqueConstraint(...)` **e** `dedup_key = mapped_column(..., unique=True, index=True)`.

**Drop:** `ix_observations_raw_dedup_key`  
**Keep:** `sqlite_autoindex_observations_raw_1` (non droppabile senza togliere il UNIQUE)

Peso live: **61.30 MiB** ciascuno.

### Coppia B — `observations.seen_at` (INDEX ×2)

| Indice | CREATE | Colonne |
|--------|--------|---------|
| **`ix_obs_seen`** | `CREATE INDEX ix_obs_seen ON observations (seen_at)` | `(seen_at)` |
| **`ix_observations_seen_at`** | `CREATE INDEX ix_observations_seen_at ON observations (seen_at)` | `(seen_at)` |

Identici. Causa: `Index("ix_obs_seen", "seen_at")` **e** `seen_at = mapped_column(..., index=True)` → Alembic `ix_observations_seen_at`.

**Drop:** `ix_observations_seen_at`  
**Keep:** `ix_obs_seen` (già preferito dal planner sulle range query)

Peso live: **37.57 MiB** ciascuno.

### Micro (stesso pattern, irrilevante per GiB)

| Drop | Keep | Peso |
|------|------|------|
| `ix_metric_snapshots_taken_at` | `ix_metric_snapshots_ts` | 4 KiB ×2 |

Incluso nello script per igiene.

**Fuori scope passo 1:** indici “prefisso del composito” (`ix_observations_raw_entity_key` ⊆ `ix_obsraw_entity_ts`, ecc.) — non duplicati esatti; eventuale passo successivo.

---

## 2 · EXPLAIN QUERY PLAN — PRIMA (live, RO)

### Dedup

```
EXPLAIN … SELECT * FROM observations_raw WHERE dedup_key=?
→ SEARCH observations_raw USING INDEX ix_observations_raw_dedup_key (dedup_key=?)
```

### Presence (`mac` + `seen_at ≥ 24h`)

```
→ SEARCH observations USING INDEX ix_observations_mac (mac=?)
```

I due indici `seen_at` **non** sono scelti qui (filtro dominante = MAC).

### Range / retention-like su `seen_at`

```
SELECT id FROM observations WHERE seen_at < datetime('now','-3 days')
→ SEARCH … USING COVERING INDEX ix_obs_seen (seen_at<?)

SELECT COUNT(*) … seen_at >= -24h
→ SEARCH … USING COVERING INDEX ix_obs_seen (seen_at>?)
```

Quindi `ix_observations_seen_at` è **già inutilizzato** dal planner sulle query tipiche.

---

## 3–4 · Piano DROP + EXPLAIN dopo (nello script)

Ordine allo **GO**:

1. Snapshot `data/backups/pre-db-slim-p1-YYYYmmdd-HHMMSS.db` (API `sqlite3.Connection.backup`)
2. `DROP INDEX IF EXISTS` sui tre candidati sopra
3. **Niente VACUUM**
4. Stessi EXPLAIN: assert
   - dedup → `sqlite_autoindex_observations_raw_1` (o comunque INDEX, no SCAN)
   - `seen_at` range → `ix_obs_seen`
   - presence → ancora INDEX (`mac` o equivalente), no full scan nuovo

---

## 5 · Esecuzione (dopo GO)

Una-tantum, **non** passa da `deploy.sh` / rebuild.

```bash
# dal Mac (sync script)
scp observatory/scripts/obs_db_slim_p1_drop_dup_indexes.py \
  mooflo@192.168.1.3:/volume1/Docker/observatory/data/db/

# su Cassiopea (terminale già aperto in /volume1/Docker/observatory):
# opzionale dry-run:
sudo docker compose exec -T -e DRY_RUN=1 -e PYTHONPATH=/app api \
  python /data/db/obs_db_slim_p1_drop_dup_indexes.py

# esecuzione reale:
sudo docker compose exec -T -e PYTHONPATH=/app api \
  python /data/db/obs_db_slim_p1_drop_dup_indexes.py
```

Writer API/collector possono restare su: `DROP INDEX` è breve; `busy_timeout=60s`. Finestra calma consigliata ma non obbligatoria come per VACUUM.

---

## Previsione spazio

| Voce | Valore |
|------|--------|
| Spazio **logico** indici rimossi | **61.30 + 37.57 + 0.004 ≈ 98.9 MiB** |
| (FASE A citava ~197 MiB = somma **entrambe** le copie; si libera **una** copia per coppia → ~99 MiB) | |
| `freelist` dopo DROP | ≈ +pages degli indici droppati (~25k pagine × 4 KiB) |
| **File su disco** | **resta ~2.49 GiB** finché non arriva **VACUUM (passo 4)** |
| `auto_vacuum` | 0 → nessuno reclaim automatico |

Correzione rispetto al “~197 MiB guadagno certo”: 197 MiB è il peso **totale delle due copie**; dopo un DROP per coppia il guadagno logico è **~99 MiB** (l’altra copia resta). Il file non cala comunque senza VACUUM.

---

## Follow-up codice (non bloccante per lo script)

Per non ricreare i duplicati a un futuro `create_all` / migrazione:

- `Observation.seen_at`: togliere `index=True`, tenere solo `Index("ix_obs_seen", …)`
- `ObservationRaw.dedup_key`: togliere `unique=True, index=True`, tenere solo `UniqueConstraint`
- `MetricSnapshot.taken_at`: un solo indice

Da fare in commit successivo sullo stesso branch **dopo** GO/esito, o insieme al merge — **non** richiesto per il DROP one-shot.

---

## STOP

Attendo **GO** per eseguire snapshot + DROP su Cassiopea. Nessuna modifica schema live finora.
