# Chiusura parti aperte — FASE A (sola ricognizione)

**2026-07-25 ~01:52 CEST** · live **0.10.24** · **nessuna scrittura / nessun deploy**  
Metodo: PRAGMA + COUNT SQLite RO, log collector/api 24h, triageRules.js offline su export pending, KNOWN_DEBT + branch git.

---

## A · Passo 2 a regime (TTL legacy 7g)

### A1 — Giri retention dopo 0.10.23

| Evidenza | Valore |
|----------|--------|
| Deploy TTL legacy | **0.10.23** · merge/deploy ~2026-07-25 01:07 CEST |
| Log collector 24h `retention=200` | **23** |
| Log collector 24h `retention=500` | **1** (lock transient, già noto) |
| Body JSON nei log | **assente** (solo status code) |

**Unico body misurato** (GO p2, forzato):

```json
"legacy_observations_pruned": 39,
"before.observations": 986244,
"after.observations": 986206
```

I giri orari successivi risultano **200** ma senza payload → non ricostruibili i pruned per giro.  
`metric_snapshots.store` **non** include chiave `observations` (solo `observations_raw`).

**Stato:** APERTO (telemetria body insufficiente) · prune misurato max noto = **39**, non regime.

### A2 — Tabella `observations` ora

| Metrica | Valore |
|---------|--------|
| COUNT | **989 219** |
| min(seen_at) | `2026-07-17 23:22:44` |
| max(seen_at) | `2026-07-24 23:51:41` |
| COUNT `seen_at < now-7d` | **117** ← prossimo prune |

Per giorno (righe residue):  
17→156 · 18→1369 · 20→219 708 · 21→163 282 · 22→198 513 · 23→211 909 · 24→194 282.

### A3 — Verdetto temporale regime ~180–220k/g

| | |
|--|--|
| Prune ≫0 a regime **già osservato?** | **NO** (max noto 39) |
| Perché | Giorni “grassi” partono dal **20/07**; cutoff 7g su Jul 20 ≈ **2026-07-27 00:00 UTC** |
| Stima inizio volumi pieni | **~2026-07-27** (quando Jul 20 esce dalla finestra; ~220k/giorno) |
| Fino ad allora | prune piccoli (Jul 17–18: centinaia–migliaia) |

**Stato:** BLOCCATO-FINO-A-**2026-07-27** (assert regime). Non forzare prune.

### A4 — Integrità reader

| Check | Evidenza |
|-------|----------|
| EXPLAIN presence `mac + seen_at≥24h` | `SEARCH observations USING INDEX ix_observations_mac (mac=?)` |
| Detectors | `detectors_enabled=''` (vuoto) → **non attivi** |
| Log api 6h `database is locked` | **6** occorrenze (contesa SQLite, non presence-specific) |
| Errori dedicati inventory/presence/detector/DNS | **nessuno** nei grep 6h oltre lock generici |
| Health | `0.10.24` ok |

**Stato:** APERTO-con-rumore-lock (operativo); reader presence path indice OK. Nessun crash presence dedicato osservato.

---

## B · Passo 3a a regime (WLAN)

### B1 — Observation WLAN post-0.10.24

| | |
|--|--|
| deploy_ts (API healthy) | `2026-07-24 23:28:26` UTC |
| COUNT kind∈{fritz_wlan_assoc,fritz_mesh} ∧ seen_at≥deploy_ts | **0** (ancora, multi-ciclo) |
| max(seen_at) WLAN | `2026-07-24 23:24:50` (**prima** del deploy_ts) |

**Stato:** CHIUSO (scrittura spenta confermata).

### B2 — meta.link / topologia

| | |
|--|--|
| Asset con wifi link | **43** |
| Link `observed_at` nell’ultima ora | **37** |
| Edge `kind=wifi` in `build_topology` | **36** |

**Stato:** CHIUSO (ciclo vivo).

### B3 — Storiche ~216k

| | |
|--|--|
| COUNT WLAN totale | **216 471** |
| min → max seen_at | `2026-07-20 01:12:46` → `2026-07-24 23:24:50` |
| COUNT WLAN `seen_at < now-7d` | **0** |

Non ancora toccate dal TTL (stesso motivo A3: dati dal 20/07). Scenderanno da **~27/07**.

**Stato:** APERTO / BLOCCATO-FINO-A-**2026-07-27** (calo TTL).

---

## C · Gesti manuali pendenti

### C1 — Coda Oggi / «Archivia rumore (N)»

Ricostruzione offline (`triageRules.js` + pending **shown** da `split_name_proposals`, senza sessione UI):

| | |
|--|--|
| Intestazione griglia | **10 adotta · 33 verifica · 11 rumore** |
| `noiseProposalIds` (N bottone massa, su proposals shown) | **37** (era 7 in assert 033A) |
| Pending DB totali | 133 · shown 131 · hidden **2** (1 asset) |

**Stato:** APERTO (massa non eseguita; N=37). Non eseguita qui.

### C2 — Asset 5 Cassiopea `os_guess`

| | |
|--|--|
| `meta.os_guess` | **null** (non `ADM-Free-OS-028b`) |
| `field_sources.os_guess` | stamp manual `2026-07-23T21:08:28Z` (chiave presente, valore assente) |
| FingerprintFact `os` | `Linux Cassiopea`, `Linux 6.6.x`, … |
| Stringa `ADM-Free-OS-028b` in facts/proposals asset 5 | **0** |

**Stato:** CHIUSO di fatto per l’artefatto test (stringa assente). Residuo cosmetico: stamp `field_sources.os_guess` senza valore.

---

## D · Debiti tracciati

### D1 — Fingerbank 027

| | |
|--|--|
| Branch `feature/obs-fingerbank-027` | tip `d20313e`, **non** in `main` |
| Merge / decisione | assente |
| Prerequisito DHCP lease corto + ciclo radio | non evidenziato come fatto in main |

**Stato:** APERTO (branch isolato).

### D2 — DEBT-NO-RECREATION-GUARD

| | |
|--|--|
| Tuple `(asset_id,value)` con pending **e** rejected stesso value | **6** (asset 10,34,36,60,64,88) |
| OBS-033 B3 diceva 0 ricreazioni post-reject | ora **6 coesistenze** → guardia ancora assente |

**Stato:** APERTO (peggiorato vs “0 osservate”).

### D3 — DEBT-PROPOSALS-HIDDEN-FROM-API

| | |
|--|--|
| Pending nascoste da `split_name_proposals` | **2** su **1** asset (era ~24/13) |
| Flag `all_proposals` | **non** implementato (KNOWN_DEBT invariato) |

**Stato:** APERTO (debito strutturale; volume nascosto ridotto).

### D4 — Backup rotation

| Tipo | N | Rotazione keep-3 deploy.sh |
|------|--:|----------------------------|
| `pre-deploy-*.db` | **3** | **sì** |
| `observatory-*.db` (create_backup) | **3** | **no** |
| `pre-db-slim-p1-*.db` | **1** | **no** |
| `data/backups` totale | **17.4G** | |
| Volume1 libero | **5.2T** / 7.3T | |

**Stato:** APERTO (`observatory-*` fuori rotazione).

### D5 — `observations_raw` TTL 7g

| | |
|--|--|
| COUNT | **777 182** |
| min → max observed_at | `2026-07-20 01:12:46` → `2026-07-24 23:50:58` |
| COUNT `observed_at < now-7d` | **0** |
| Snapshots orari: raw in crescita | 744k→774k (24/07) — **nessun morso** ancora |

**Stato:** BLOCCATO-FINO-A-**~2026-07-27** (stesso cancello del legacy grasso).

---

## E · Prerequisiti prossimi cantieri

### E1 — 3b (presence/scans/detectors / stop dual-write host)

| | |
|--|--|
| `scoring_calibrated` | **False** |
| `drift_shadow_mode` | **True** |
| Calibrazione | **active day 5 / 14** · started `2026-07-20T01:12:46Z` |
| `detectors_enabled` | `''` → **nessun detector acceso** |
| Findings / drifts in DB | **0 / 0** |

Toccare ora la fonte Observation dei detectors: **non inquina verdetti live** (detector off, shadow, zero findings).  
Calibrazione scoring/drift **ancora in corso** (giorno 5/14) — 3b su presence/scans resta delicato ma **non** bloccato da detector attivi.

**Stato:** 3b **APRIBILE con cautela**; detectors non sono il cancello. Calibrazione shadow day 5/14 = contesto.

### E2 — 4a/4b VACUUM

| | |
|--|--|
| `auto_vacuum` | **0** |
| `freelist_count` | **20 000** pagine ≈ **78.1 MiB** (riuso writer dopo i ~98.9 MiB del passo 1) |
| OS DB | **2 677 227 520** B (~2.49 GiB) |
| Libero volume1 | **5.2T** ≫ 2× DB → **VACUUM INTO ok** |
| Writer SQLite | **`api`** (RW su `./data`). **`collector`** monta `./data` ma path DB tipicamente via API; Zeek state RO. Fermare almeno **api** (+ collector per evitare POST) durante VACUUM |

**Stato:** prerequisiti spazio/pragma **OK**; esecuzione solo in manutenzione (STOP writer).

---

## Sintesi decisioni (numeri → prossimi passi)

| Parte | Stato | Cancello |
|-------|-------|----------|
| P2 regime prune | BLOCCATO | **~2026-07-27** |
| P3a WLAN write | **CHIUSO** | — |
| P3a WLAN storico TTL | BLOCCATO | **~2026-07-27** |
| C1 Archivia rumore | APERTO | gesto manuale (N≈**37**) |
| C2 ADM artefatto | **CHIUSO** di fatto | — |
| D1 Fingerbank | APERTO | decisione branch |
| D2 recreation | APERTO | 6 tuple |
| D3 hidden API | APERTO | flag assente (hidden=2) |
| D4 observatory-* rotation | APERTO | keep-3 solo pre-deploy |
| D5 raw TTL | BLOCCATO | **~2026-07-27** |
| 3b | APRIBILE (detector off) | calibrazione day 5/14 |
| 4 VACUUM | pronto spazio | freelist 78 MiB; stop api |

Nessuna modifica effettuata in questa FASE A.
