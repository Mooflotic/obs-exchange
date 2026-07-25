# OBS ballooning §13 — diagnosi (sola lettura)

**Live:** 0.10.28 · **DB:** 2 866 352 128 B (**2.669 GiB**) · **Data:** 2026-07-25  
**Metodo:** `dbstat` + COUNT/aggregati SQL in sola lettura. **Nessuna scrittura. 4b non iniziato.**

---

## Bilancio byte (chiude)

| Voce | Byte | GiB | % file |
|------|------|-----|--------|
| `observations_raw` (tabella) | 1 546 641 408 | 1.440 | 54.0% |
| `observations` (legacy) | 902 033 408 | 0.840 | 31.5% |
| Indici su raw+obs (top 6) | ≈233 000 000 | 0.217 | 8.1% |
| `flow_observations` + idx | ≈34 000 000 | 0.032 | 1.2% |
| `heartbeats` + idx | ≈22 000 000 | 0.020 | 0.8% |
| Resto tabelle/idx misurati | ≈55 000 000 | 0.051 | 2.0% |
| **Somma dbstat top** | **2 793 066 496** | **2.601** | **97.4%** |
| **Residuo dichiarato** (file − somma) | **73 285 632** | **0.068** | **2.6%** |
| Freelist | 8 192 (2 pagine) | ≈0 | — |
| WAL | 7 424 272 | 0.007 | — |

`page_count×page_size` = 2 866 356 224 ≈ size file (ok). Residuo ~73 MiB = tabelle/indici fuori dalla top-25 + overhead SQLite — **non nascosto**.

---

## Cause ordinate per peso

### 1. `observations_raw` — 1.44 GiB (54%) — **confermata**
- Righe: **862 525**
- Kind dominante: `fritz` **823 970** righe, payload medio **1221 B**, somma payload **~1.00 GiB**
- Indici correlati: `ix_obsraw_*` / `ix_observations_raw_*` ~**0.17 GiB** aggiuntivi

### 2. `observations` legacy — 0.84 GiB (31%) — **confermata**
- Righe: **1 067 155** (congelate: dual-write off; Δ/10min = 0)
- Kind: `fritz` 819 070 × ~758 B → **~0.58 GiB** solo payload; + `fritz_wlan_assoc` ~0.08 GiB
- Indici `ix_obs_*` ~**0.09 GiB**
- TTL dichiarato **7g** (`OBS_TTL_LEGACY_DAYS`); extent live ~2026-07-20→25 = finestra TTL. Prune **gira** (bordo a 7g). File non cala senza VACUUM/DROP (**4b**).

### 3. Doppia materializzazione raw ↔ legacy — **confermata**
| Fatto | raw | legacy |
|-------|-----|--------|
| fritz rows | 823 970 | 819 070 |
| payload medio | 1221 B | 758 B |
| volume tabella | 1.44 GiB | 0.84 GiB |

Stesso fatto FRITZ (e nmap) in due tabelle. Raw è la copia “grassa”; legacy è storica in drenaggio.

### 4. Indici sproporzionati su serie temporali — **confermata**
48 indici utente; i sei maggiori su obs/raw pesano **~0.22 GiB**. Utili alle query di retention/trust storiche; dopo DROP legacy diversi `ix_obs_*` spariscono con la tabella.

### 5. Duplicati esatti — **falsificata**
`GROUP BY mac,kind,seen_at HAVING COUNT>1` → **0** gruppi, **0** extra. Nessun gonfiore da insert identici.

### 6. Freelist / buco interno — **falsificata come causa primaria**
Freelist = **2** pagine. Lo spazio liberato dal prune viene **riusato**; il file non restringe (comportamento SQLite atteso). Ballooning = contenuto vivo + legacy ancora piena, non freelist.

### 7. Altri store — minori
- `flow_observations` 69 794 righe / ~30 MiB (TTL 30g)
- `heartbeats` 85 206 / ~18 MiB
- `sensor_runs` 8 759 / ~2.7 MiB — **senza TTL dedicato** (candidato post-4b)
- `assets`/`ip`/`events` trascurabili sul totale

---

## F.4 EXPLAIN (query reali)

Retention/legacy e trust non leggono più `observations` a runtime (3b-iii) salvo **DELETE/COUNT** retention (BLOCKER 4b).  
Indici `ix_obs_seen` / `ix_observations_mac` servono al prune legacy; dopo DROP diventano irrilevanti.  
Su raw: `ix_obsraw_entity_ts` / `ix_obsraw_source_ts` giustificati dal rollup TTL.

## F.6 Retention — dichiarato vs reale

| Tabella | TTL dichiarato | Evidenza live |
|---------|----------------|---------------|
| `observations_raw` | rollup+delete (ttl raw, tip. 7g) | extent ~7g; ancora 1.44 GiB (payload grosso) |
| `observations` | 7g | extent 6–7g; 0.84 GiB; **insert fermi** |
| `flow_observations` | 30g | presente |
| `heartbeats` | retention dedicata | presente |
| `sensor_runs` | **nessuno** | 8759 righe accumulate |

## F.7 Job / dedup
- Dual-write host **spento** → niente nuove legacy.
- Dup esatti = 0 → dedup_key / insert path non moltiplicano righe identiche.
- `sensor_runs` cresce con ogni ciclo collector (atteso).

## F.8 Outlier
- Top MAC legacy ~12 1xx righe ciascuno: host sempre presenti nel poll FRITZ (frequenza × giorni), non anomalia di chiave.
- Source raw: `fritz` domina (>95%).

## F.9 Frequenze
- Legacy/giorno pre-stop: ~160–220k/giorno; oggi 78k (mezza giornata + stop dual-write).
- Raw/giorno: ~127–173k; oggi 85k (ancora attivo).

## F.10 Config duplicate
Nessuna evidenza di collector doppio nel perimetro misurato (un `observatory-collector-1`).

## F.11 Cache ricostruibili
`metric_snapshots` 122 righe (~250 KiB) — irrilevante.  
`presence_sources` / `portal_*` su asset = caldo piccolo (corretto per split).

## F.12 DEBT-BACKUP-ASYMMETRY — **chiusa con misura**

| Punto | Misura |
|-------|--------|
| Due copie/deploy | Confermate: `pre-deploy-*` (deploy.sh) + `observatory-*` (trust se needs_apply) |
| Throughput trust vs deploy | Serie trust: 10.37 → 9.22 → 9.15 → 18.38 → **17.3** MB/s (0.10.28 boot1) |
| Dimezzamento post-3b-iii | **Conferma A.5:** con dual-write off, `observations` non riceve ~2.4 insert/s; `Connection.backup()` ricopia meno pagine sporche. Non è page-cache (già falsificato a P2). |
| Premio converge 0.10.28 | Boot3: **T_backup=0**, **T_total=8.869 s** (needs_apply=false) |

Nessuna modifica a `deploy.sh` / `backup.py`.

## F.13 Tre ipotesi extra

| Ipotesi | Esito |
|---------|-------|
| H-A: gonfiore da freelist dopo prune | **Falsificata** (2 pagine) |
| H-B: duplicati esatti observations | **Falsificata** (0) |
| H-C: `flow_observations` o heartbeats dominano il file | **Falsificata** (<2% combinati) |

---

## Contromisure (solo proposte — **non implementare**)

### Prima di 4b
- Lasciar drenare legacy a ~0 righe (~2026-08-01) e **ri-misurare** dbstat.
- Monitorare crescita **solo** `observations_raw` (payload fritz).
- Non riaccendere dual-write.

### Dentro 4b
- DROP `observations` + rimozione modello ORM (blocker `DEBT-ORM-MODEL-RECREATES-TABLE`).
- Rimuovere indici/reader legacy residui.
- Valutare VACUUM **una tantum** post-DROP (file cala solo qui).

### Dopo 4b
- Comprimere/normalizzare payload `fritz` in raw (campi costanti / ridondanze).
- TTL o rollup aggressivo su raw se la crescita giornaliera resta ~150k.
- Retention su `sensor_runs`.
- Unificare backup (una copia/deploy) — cantiere dedicato post-asimmetria chiusa in diagnosi.

---

**STOP.** 4b si apre solo dopo review di questo documento.
