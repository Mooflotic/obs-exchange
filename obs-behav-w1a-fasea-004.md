<!-- BLOCK-ID: OBS-BEHAV-W1A-FASEA-004 -->

# BEHAVIOURAL WAVE 1a — FASE A tecnica (RO)

**Scope:** sola lettura · nessuna implementazione · STOP FASE A  
**Live:** `data/zeek/conn.log` corrente (~16k righe scansionate), Zeek attivo.

---

## VERIFICA 1 — Direzione: i byte separati esistono?

### 1) Campi reali in conn.log (policy attuale)

I campi **ci sono**. Non sempre popolati.

| Situazione | Evidenza live |
|------------|---------------|
| TCP chiuso (`SF`) | `orig_bytes`/`resp_bytes` numerici + `orig_ip_bytes`/`resp_ip_bytes` |
| TCP half/OTH/S0 | spesso `orig_bytes`/`resp_bytes` = **`null`**, ma `*_ip_bytes` > 0 |
| UDP NTP/DNS ok | a volte entrambi app-layer; spesso `resp_bytes=0` o null |
| UDP S0 / one-way | `orig_bytes`/`resp_bytes` **null**, solo `orig_ip_bytes` |
| ICMP | mix: spesso app-layer numerico; anche null+ip_bytes |

Su ~16.6k righe: ~12.6k con almeno un lato app-layer `>`; ~3.0k con **entrambi null** ma IP-bytes presenti.

**Esempi reali (estratti):**

```text
TCP SF  .2.176→99.81.112.62:443  orig_bytes=1433 resp_bytes=317195  orig_ip=11865 resp_ip=319259
TCP SF  .2.176→15.217.247.169:443 orig_bytes=624  resp_bytes=4633
TCP OTH .1.3→.1.117:22           orig_bytes=null resp_bytes=null  orig_ip=0 resp_ip=44
TCP S0  .3.47→.178.115:55443     orig_bytes=null resp_bytes=null  orig_ip=60 resp_ip=0
UDP SF  .2.203→.1.1:53           orig_bytes=28 resp_bytes=92
UDP S0  .2.99→162.159.200.1:123  orig_bytes=null resp_bytes=null  orig_ip=76 resp_ip=0
UDP S0  .2.80→.3.255:58866       orig_bytes=158 resp_bytes=0
ICMP    fe80…→fe80…              orig_bytes=16 resp_bytes=16 (+ ip_bytes)
```

**Quale coppia usare?**
- **Primaria:** `orig_bytes` / `resp_bytes` (payload applicativo) quando **almeno uno non è null**.
- **Fallback:** `orig_ip_bytes` / `resp_ip_bytes` se entrambi app-layer sono null — altrimenti si perde ~18% delle conn (UDP/S0). Nota: IP-bytes includono header → leggermente gonfi; accettabile per direzione, etichettare `byte_layer=app|ip`.
- **Non affidabile come “silenzio”:** `int(null or 0)` come fa oggi il parser — confonde null con zero.

### 2) `parse_conn_line` oggi + punti da toccare

Oggi (`zeek_conn.py`):
```python
orig = int(row.get("orig_bytes") or 0)   # null → 0
resp = int(row.get("resp_bytes") or 0)
"bytes": orig + resp                      # unica cifra persistita
```
Aggregate somma solo `bytes`; `build_flow_bodies` / `normalize_flow_record` / `FlowIn` / `FlowObservation` hanno solo `bytes`.

**Pipeline da estendere (carta):**
1. `parse_conn_line` → emettere `bytes_out`, `bytes_in`, `byte_layer`, tenere `bytes=out+in`
2. `aggregate_conn_records` → sommare out/in (e samples) per bucket
3. `build_flow_bodies` + `flow_stub.normalize_flow_record`
4. `FlowIn` (`evolution.py`) + `ingest_flow` (add su dedup esistente)
5. Model `FlowObservation` + migration Alembic
6. Test: `test_zeek_conn_provider`, `test_flows_summary`
7. (Wave 1a UI) `flows_summary` / identity dossier — fuori da questa FASE A se solo pipeline

### 3) Migration proposta

Aggiungere colonne nullable:
- `bytes_out INTEGER NULL`
- `bytes_in INTEGER NULL`
- (opz.) `byte_layer VARCHAR(8) NULL` — `app` | `ip`

Tenere **`bytes`** = `COALESCE(bytes_out,0)+COALESCE(bytes_in,0)` in scrittura nuova; storico: `bytes` pieno, **out/in NULL** → UI: «direzione non disponibile per dati pre-1a».

Non rompere top-talkers esistenti.

---

## VERIFICA 2 — Coverage per-device

### 4) Assenza dai flow ≠ “non visto dallo SPAN”

I 51/105 sono solo “src_ip corrente compare in qualche flow”. Cause miste:
- device quiete (no traffico nell’ora);
- IP storico nei flow ma non current (sottostima del match grezzo);
- resolve skip (tie/None) → provider **non posta**;
- segmento non mirrorato (WiFi↔WiFi, east-west).

Serve segnale **strutturale** (dove sta il device), non solo conteggio flow.

### 5) Segnali disponibili → 3 stati

Codice/topologia oggi:
- `meta.link.media/kind` ≈ wifi (~47 asset);
- `SwitchPort.role` / overrides: SPAN sink = **LGS328C p22** (`ensure_known_span_overrides`); uplink/downlink/dedicated da FDB;
- path inventario (`topology`) verso core/gateway;
- **sources del mirror (p1/p21/p24)** non sono modellate come lista formale in DB — vanno trattate come config nota (doc/runbook) o override manuali finché non si codificano.

**Logica proposta (carta):**

| Stato | Condizione |
|-------|------------|
| **completo** | path verso core attraversa uplink mirrorato / traffico WAN tipicamente sullo SPAN; non wifi-only; ha avuto ≥1 flow risolto in finestra *oppure* è wired su ramo uplink |
| **parziale (motivo)** | `link=wifi` → «WiFi↔WiFi stesso AP non osservato»; oppure solo-AP/mesh; oppure east-west su stesso access switch senza passare dall’uplink mirrorato; oppure resolve frequenti None |
| **sconosciuto** | niente path/porta/link affidabile; o mai visto in FDB/Fritz con topologia ambigua |

Badge Dossier: testo corto + motivo. **Assenza di flow + coverage=completo** → «silenzio osservato»; **assenza + parziale** → «può esserci traffico non mirrorato».

---

## Proposta sintesi Wave 1a

1. **Schema:** `bytes_out`/`bytes_in` NULL + `bytes` compat; `byte_layer` opz.  
2. **Parser:** app-bytes se non-null; else IP-bytes; non collassare null→0 senza flag.  
3. **Coverage:** 3 stati da topologia/link, non da sola assenza flow.  
4. **Dossier «Abitudini»:** destinazioni IP grezzo + out/in quando non-NULL + badge coverage. Nomi = Wave 1b.

**STOP FASE A.**
