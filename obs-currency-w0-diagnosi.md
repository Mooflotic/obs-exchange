<!-- BLOCK-ID: OBS-CURRENCY-W0-DIAGNOSI -->

# OBS-CURRENCY — W0 Diagnosi misurata

**Data:** 2026-07-25 · **Live:** 0.10.40 · **Branch:** `feature/obs-currency`  
**Scope:** sola lettura · nessun deploy · nessun bump  
**Prune raw:** NON ancora (raw_min=`2026-07-20 01:12:46` · raw_max=`2026-07-25 16:47:23` · n=**870 279**) — atteso ~2026-07-27

**Baseline assert:** assets **151** · AD **82** · ip_current **100** · name_proposals **412** · `observations` assente · dual-write spento  
**scans 68:** metrica storica non allineata a `scan_runs` live (**1493** totali, **1306** done) — dichiarata **available=false** come assert numerico in questo cantiere finché non ridefinita (non ridefinita a posteriori).

---

## 0.1 Mappa «corrente» (sintesi)

Writer primario IP: `identity.elect_interface_primary` ← `observe_interface_ip` (rank sorgente + fresh 30m).  
Presenza trust: `portal_last_seen` 24h. UI `stale` usa spesso `last_seen` 24h — **due orologi**.

Tabelle complete nel report di ricognizione codice (path principali):

| Area | Criterio |
|------|----------|
| `ip_addresses.is_current` | elezione per interfaccia |
| Fallback display IP | `max(last_seen)` se nessun current (`assets.py`, `topology.py`) |
| Trust / presence | `portal_last_seen` ≤24h / ≤72h |
| FDB | `MAX(last_fdb_at)` |
| Chassis KPI | `max(member.last_seen)` ≤24h |

---

## 0.2 Anatomia `ip_current` (100)

| Voce | Misura |
|------|--------|
| Conteggio | **100** |
| Contiene `192.168.3.20`? | **No** (`is_current=0` su asset 4) |
| Asset con >1 riga current | **1** — asset **2** LGS328C: stesso IP `.1.2` su **due MAC** (`D8:EC:5E:CC:1B:FF` mgmt + `C8:54:4B:F4:71:D5` fritz) |

`.1.8` current asset 4 · `.3.20` non current stesso MAC (classe sequenziale).

Cassiopea: NIC1 asset5 `.1.3` current · NIC2 asset6 `.3.24` current (`.1.3` non current su NIC2) — **concorrente su asset distinti / MAC distinti**, non multi-current sullo stesso MAC.

---

## 0.3 Cardinalità per classe

### IP
| Metrica | N |
|---------|---|
| Righe `ip_addresses` | 118 |
| Asset con >1 IP mai visti | **6** (ids: 1,3,4,6,50,51) |
| Stesso MAC, multi-current | **0** |
| Stesso MAC, sequenziale (>1 IP, ≤1 current) | **6** |
| Asset multi-current IP/MAC distinti | **1** (asset 2, stesso IP due MAC) |

**Classificazione IP (misurata):** sullo stesso MAC i valori sono **mutuamente esclusivi** (sequenziali). Concorrenza legittima = MAC/asset distinti (Cassiopea 5/6).

### MAC↔asset / hostname / chassis
| Classe | Misura |
|--------|--------|
| Interfaces | 158 |
| NameProposal | 412 (pending per source: dns42 fritz26 oui6 ai5 dhcp2) |
| Chassis rows | 15 · asset con `chassis_id` | 35 · gruppi ≥2 | **15** |
| Manual name (`manual_overrides` lista contiene `name`) | **29** asset |
| Chassis ≥2 con ≥1 manuale | **5** |
| Chassis ≥2 con >1 nome manuale distinto | **0** |

### Altre classi
OS/servizi/FDB/relazioni: non ridotti a «corrente singolo» in questo W0 oltre i path già mappati in 0.1; fingerprint non auto-scrive `Asset.os_guess`.

---

## 0.4 Istanze vive difetto classe-`.3.20` (IP sequenziale non current)

Definizione operativa W0: stesso MAC con IP current + ≥1 IP non current (candidato superseded).

**N = 9** (enumerate):

| asset | MAC | current | non-current | source nc |
|------:|-----|---------|-------------|-----------|
| 1 | 60:B5:8D:6C:6D:53 | .1.1 | .1.4 .1.5 .1.6 .1.9 | nmap |
| 3 | D8:EC:5E:C5:7E:C7 | .1.7 | .2.161 | fritz |
| **4** | **54:07:7D:1E:4F:B9** | **.1.8** | **.3.20** | **fritz** |
| 6 | 24:4B:FE:84:6A:02 | .3.24 | .1.3 | fritz |
| 50 | 1C:69:7A:A6:FA:47 | .2.126 | .1.148 | fritz |
| 51 | DC:A6:32:9C:A7:62 | .2.138 | .1.117 | nmap |

Nota: asset 1 ha 4 non-current → 4 delle 9 righe. Non sono tutte «bug UI»: sono storia IP sullo stesso MAC; il difetto prodotto è presentarne una come corrente o inventariale senza stato.

---

## 0.5 Intervalli osservazioni (sample raw)

Finestra osservabile: **TTL 7gg raw** (min 2026-07-20 → max 2026-07-25). Percentili **oltre** quella finestra: **available=false** (K3).

Query: 200 000 righe ordinate · **11.4 s** (HDD) · totale script **16.8 s**.

| source | n_gaps | p50 s | p90 s | p99 s | max s |
|--------|-------:|------:|------:|------:|------:|
| fritz | 185872 | 60.1 | 120.1 | 180.1 | 337434 |
| nmap | 7805 | 45.6 | 247.6 | 939.7 | 3125 |
| ssdp | 5738 | 901 | 1031 | 10491 | 79098 |
| printer | 500 | 901 | 1047 | 1814 | 2703 |
| scan-batch:os_fingerprint | 3 | 50.4 | 191 | 223 | 227 |

TTL proposte (registro): basate su p99 **entro** finestra 7gg; oltre = non misurabile.

---

## 0.6 Costo query

| Step | s |
|------|--:|
| raw window | 0.019 |
| ip card | 0.002 |
| chassis | 0.006 |
| name_proposals | 0.007 |
| contradiction | 0.011 |
| intervals (200k) | **16.665** |
| export | 0.042 |
| **totale** | **16.754** |

Nessuna query >60 s; intervals chunkabile se serve.

---

## 0.7 Calendario prune + export

| Voce | Valore |
|------|--------|
| Prune pieno | **non ancora** (~2026-07-27) |
| Export | `/data/exports/obs-currency-w0-history.jsonl` |
| Linee | **205** |
| Size | **52 397 B (0.05 MiB)** |
| Contenuto | IP da `ip_addresses` + nomi asset (valid_from truncated sui nomi) |

Se prune arriva prima di W3: i `valid_from` raw sotto raw_min corrente restano ricostruibili solo da questo export (IP sì; storia raw extra **no**).

---

## W0.B — rimando

Dettaglio chassis / proposte / K1 / contraddizione: [`obs-chassis-w0-identita.md`](obs-chassis-w0-identita.md).

### Hallucination check caso UI «tre card LGS310C»

LIVE: MAC `…:1C:05` e `…:1C:08` sono **chassis_id=23 (LGS328C)**; MAC `…:C5:7E:C7` LGS310C è **chassis_id=24**.  
→ **Riga AMBIGUA (STOP-5)**: l’apparato fisico «unico» dichiarato in UI non coincide col grouping DB. Non scegliere in W1–W4 su questa fusione finché Michele non conferma.
