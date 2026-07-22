<!-- BLOCK-ID: OBS-BEHAV-W1-FASEA-003 -->

# BEHAVIOURAL WAVE 1 — FASE A: ricognizione flow per-device (RO)

**Scope:** solo lettura · nessun detector · STOP FASE A  
**Live (Cassiopea, 2026-07-22):** `flow_observations` ≈ **9237** righe; finestra `2026-07-21 19:00` → `2026-07-22 16:00` (~1 giorno su retention 30gg); ASN/country **sempre vuoti**.

---

## 1) MAKE-OR-BREAK — link asset ↔ flow nel tempo

### Esiste `resolve_asset_by_ip_at`?
Sì — `api/app/services/identity.py`. Usato da:
- top talkers in `flows_summary.flow_summary` (`resolve` su `src_ip` all’inizio dell’ora chiusa);
- mirror RO nel collector Zeek (`resolve_asset_by_ip_at_sqlite`) **prima** del POST: se None/tie → **skip** (niente flow orfani / niente asset nuovi).

### Come funziona
Dato `(ip, observed_at=T)`:
1. cerca binding in `ip_addresses` con `first_seen ≤ T`;
2. tiene righe **current** (`is_current`) oppure storiche con `last_seen ≥ T`;
3. esclude MAC sintetici `FE:…:00`;
4. se **più di un asset** candidato → **`None` (tie)** — non attribuisce.

### Flow di un device con IP multipli nella settimana?
Ricostruibili **solo** aggregando gli IP del device **risolti a T = `observed_at` di ogni riga** (o bucket orario), non con `is_current` di oggi. Pattern:
```
per ogni flow row:
  asset = resolve_asset_by_ip_at(src_ip, row.observed_at)  # e/o dst se LAN
  se asset.id == target → includi
```
Alternativa equivalente: enumerare storici `ip_addresses` dell’asset e filtrare flow dove `src_ip` ∈ set e `observed_at` ∈ `[first_seen, last_seen]` del binding — stessa semantica se i bound sono coerenti.

### Gate anti-attribuzione-sbagliata (obbligatorio)
| Regola | Perché |
|--------|--------|
| **Sempre** `resolve_asset_by_ip_at(ip, observed_at)` — mai IP→asset “ora” | DHCP / privacy MAC |
| **Tie → escludi** (già nel codice) | due device sullo stesso IP nella finestra |
| Non sommare IP storici **senza** intervallo temporale | IP riusato da altro device |
| Preferire `src_ip` come “chi parla” (Zeek `id.orig_h`); dst LAN solo se serve peer | coerenza con ingest attuale |
| Dichiarare coverage: flow solo se resolve ≠ None | trasparenza |

Senza questo gate il Dossier behavioural **mente**.

---

## 2) Destinazioni (ultima settimana)

- **Estraibili:** sì — `GROUP BY dst_ip` (e proto/port) filtrando flow il cui `src_ip` resolve all’asset@T.
- **Hostname / org:** colonne `dst_asn` / `dst_country` **esistono ma live = 0 riempite**. Payload ingest non arricchisce. Top esterni live = IP grezzi (Google/GCP-like, ecc.) — **nessun** nome `amazonaws`/`roborock`.
- **Arricchimento:** necessario per Wave 1 “leggibile” (DNS passivo da Zeek se disponibile, o lookup offline/ASN). Non in FASE A.

## 3) Direzione inbound / outbound

Zeek `conn.log` ha `orig_bytes` / `resp_bytes`.  
**Ma** `zeek_conn.parse_conn_line` fa `bytes = orig + resp` e **non persiste** orig/resp in `flow_observations` (solo `bytes` totale). Payload live: `samples`, `hour_start`, niente split.

→ **Oggi non si distingue** “MB scaricati sull’IoT” vs upload dal DB.  
Per Wave 1 direzione: **serve schema/provider** (es. `orig_bytes`/`resp_bytes` o `bytes_out`/`bytes_in` nel POST) — altrimenti solo volume totale.

## 4) Volume

- Aggregabile per destinazione: `SUM(bytes)`.
- Risoluzione temporale ingest: **bucket orario** (pre-aggregato provider). Non mezz’ora fine-grained nei dati salvati.
- Dedup API su finestra ~60s ma provider posta già orario.

## 5) Orari

- Timestamp = **inizio ora UTC** del bucket.
- Raggruppabile in fasce orarie sì; mezz’ore **no** con i dati attuali.
- Retention: `FLOW_OBSERVATION_RETENTION_DAYS=30`. Live ancora ~1 giorno di storia.

## 6) Porte / servizi

- Ci sono: `dst_port`, `proto` (live: udp≈4903, tcp≈3994, icmp≈340; top 443/80/53/123/1900…).
- Nome servizio: **non in DB**; risolvibile a presentazione con mappa locale / `getservbyport` (best-effort, porte alte = numerico).

## 7) Punti ciechi SPAN

Mirror su uplink/core: **non** vede WiFi↔WiFi stesso AP né molto east-west dietro lo stesso switch senza SPAN.

Live grezzo: ~47 asset con meta link wifi; ~105 asset con IP current; solo **51** compaiono come `src_ip` in qualche flow (match current IP — sottostima se IP cambiato). Device WiFi / mesh / solo-Fritz spesso **incompleti o assenti**.

Dossier deve dichiarare es.  
«Traffico **parziale**: segmento non interamente osservato (SPAN). Assenza ≠ silenzio.»

---

## Proposta carta — sezione Dossier «Abitudini» (Wave 1 descrittivo)

**Gate:** ogni riga flow → `asset_id = resolve_asset_by_ip_at(src_ip, observed_at)`; solo match univoco.

**UI (priorità):**
1. **Con chi parla** — top destinazioni (IP; label se arricchito) ultima 7g  
2. **Direzione** — out/in **solo dopo** persistenza orig/resp; finché no → volume unico + nota «direzione non disponibile»  
3. **Quanto / quando** — barre ore (bucket 1h), totale bytes  
4. **Porte** — collassate / “mostra dettagli”  
5. **Coverage** — badge parziale se wifi/meta o zero flow con IP noto

**Fuori Wave 1:** anomalie, baseline, detector (`EXPERIMENTAL_FLOW_DETECTORS`).

**STOP FASE A.**
