<!-- BLOCK-ID: OBS-BEHAV-W1A-P2-FASEA-006 -->

# OBS-BEHAV-W1A-P2-FASEA-006 — Dossier «Abitudini» (FASE A design)

**Scope:** sola lettura · design + fattibilità query · **nessun codice** · STOP FASE A  
**Contesto live (2026-07-23 ~00:36):** pipeline direzione 0.10.0 deployata; `bytes_out`/`bytes_in` ancora 0 sulle 13k righe storiche (atteso); accumulo inizia dalle ore chiuse post-deploy.  
**Vincolo Wave 1a:** solo descrittivo — nessun «anomalo/normale».

---

## 0. Premessa architetturale (gate)

«Abitudini di un asset» = flow dove  
`resolve_asset_by_ip_at(src_ip, observed_at) == asset.id`  
(tie → escludi). Spec già in `identity.py` e nel provider Zeek (a ingest le righe non risolte **non** vengono postate).

Il pannello è **per un device**, non per tutta la LAN → budget di costo molto basso.

Evidenza live 7g (`flow_observations`):

| Metrica | Valore |
|---------|--------|
| src distinti | 54 |
| righe/src p50 | ~137 |
| righe/src p90 | ~567 |
| max | ~1880 |
| IP con >1 asset in binding history | 7 (tie rari ma reali) |
| aggregato top-dst + ore su un src busy | ~24–50 ms SQLite |

---

## PARTE TECNICA

### 1. Query concreta — una sola, non iterare per-riga

**Verdetto:** una query SQL set-based basta e resta accettabile. Iterare `resolve_asset_by_ip_at` su ogni riga è **sconsigliato** (N× ORM); se serve fallback Python, risolvere per **chiave distinta `(src_ip, observed_at)`** (bucket orario già tipico) con cache — non per riga grezza.

#### 1a. Join che replica il gate (preferred)

```sql
-- Parametri: :asset_id, :since (UTC, tip. now-7d)
WITH candidates AS (
  SELECT
    f.id AS flow_id,
    a.id AS asset_id
  FROM flow_observations f
  JOIN ip_addresses ip
    ON ip.ip = f.src_ip
   AND ip.first_seen <= f.observed_at
  JOIN interfaces i ON i.id = ip.interface_id
  JOIN assets a ON a.id = i.asset_id
  WHERE f.observed_at >= :since
    -- esclude MAC sintetici FE:…:00 (stesso filtro di resolve_asset_by_ip_at)
    AND NOT (
      UPPER(i.mac) LIKE 'FE:%'
      AND UPPER(i.mac) LIKE '%:00'
      AND LENGTH(i.mac) = 17
    )
    AND (
      ip.is_current = 1
      OR (ip.last_seen IS NOT NULL AND ip.last_seen >= f.observed_at)
    )
),
resolved AS (
  -- tie → escludi (HAVING = 1)
  SELECT flow_id, MIN(asset_id) AS asset_id
  FROM candidates
  GROUP BY flow_id
  HAVING COUNT(DISTINCT asset_id) = 1
),
mine AS (
  SELECT f.*
  FROM flow_observations f
  JOIN resolved r ON r.flow_id = f.id
  WHERE r.asset_id = :asset_id
)

-- (A) top destinazioni + volume + direzione (mix-aware)
SELECT
  dst_ip,
  COUNT(*)                         AS samples,
  SUM(bytes)                       AS bytes_total,
  SUM(bytes_out)                   AS bytes_out_sum,   -- NULL se tutte NULL
  SUM(bytes_in)                    AS bytes_in_sum,
  SUM(CASE WHEN bytes_out IS NOT NULL THEN 1 ELSE 0 END) AS samples_with_dir,
  MIN(CASE WHEN bytes_out IS NOT NULL THEN observed_at END) AS dir_first_at
FROM mine
GROUP BY dst_ip
ORDER BY bytes_total DESC
LIMIT 12;

-- (B) porte (a scomparsa: top N, resto collassato)
SELECT dst_port, proto, SUM(bytes) AS bytes_total, COUNT(*) AS samples
FROM mine
GROUP BY dst_port, proto
ORDER BY bytes_total DESC
LIMIT 8;

-- (C) fasce orarie 0–23 (UTC o locale documentato — proporre locale LAN)
SELECT CAST(strftime('%H', observed_at) AS INTEGER) AS hour,
       SUM(bytes) AS bytes_total,
       COUNT(*) AS samples
FROM mine
GROUP BY hour
ORDER BY hour;
```

Nota SQLite: `SUM(bytes_out)` su mix NULL+valori **ignora** i NULL (ok). Se **tutte** NULL → risultato NULL (non 0) — preservare in API come `null`.

#### 1b. Perché non «solo IP correnti»

Filtrare solo `src_ip = IP current dell’asset` è **sbagliato** se DHCP ha ruotato: perderebbe ore storiche. Il join su binding history è il gate corretto.  
Filtrare `src_ip IN (tutti gli IP mai visti sull’asset)` senza interval check **sovrastimerebbe** se l’IP è stato riassegnato (i 7 tie live lo dimostrano).

#### 1c. Costo per il pannello di UN device

| Approccio | Costo stimato | Note |
|-----------|---------------|------|
| SQL 1a (3 aggregati) | ≪100 ms | preferred; indici utili: `observed_at`, eventualmente `(src_ip, observed_at)` |
| Python: candidati per IP asset + resolve cache per ora | ok su max ~2k righe | fallback / parity test vs SQL |
| Resolve ORM per riga | no | N-query inutile |

Endpoint proposto (carta, non implementare ora):  
`GET /api/assets/{id}/habits?days=7` → payload sotto.

---

### 2. Mix direzione (storico NULL + nuove valorizzate)

**Non** collassare NULL→0 nell’aggregato direzione.

Campi risposta (per destinazione e per totale sezione):

| Campo | Significato |
|-------|-------------|
| `bytes_total` | `SUM(bytes)` — **sempre**, tutto lo storico in finestra |
| `bytes_out` / `bytes_in` | `SUM` solo sulle righe con direzione; se nessuna → `null` |
| `direction_coverage` | `samples_with_dir / samples` (0–1) |
| `direction_since` | `MIN(observed_at)` dove `bytes_out IS NOT NULL` (globale asset) |

**Presentazione volume vs direzione (senza rompere i totali):**

1. **Volume** (barra / cifra primaria) = sempre `bytes_total` (7g).
2. **Direzione** = sottoinsieme; se `direction_since` valorizzato, una riga meta:
   - `Direzione disponibile dal 23 Jul 2026 (UTC) — N% delle osservazioni in finestra`
3. Se `direction_coverage == 0`: niente barre out|in; solo volume + nota «direzione non ancora in accumulo (pre-1a / in attesa ora chiusa)».
4. Se `0 < coverage < 1`: barre out|in calcolate **solo** sul sottoinsieme con direzione; **non** ridistribuire il volume senza direzione sulle barre. Eventuale micro-nota: «barre su M di K osservazioni».

Così l’occhio vede «quanto ha parlato» (totale) e «in che verso» (subset onesto).

---

## PARTE DESIGN — sezione «Abitudini»

Contesto UI: estensione del pannello Inventario, stessa famiglia di **Chi sei** (`inv-p-sec` + `inv-p-seclabel` + purpose one-liner). Non nuova route.

### 3. Struttura proposta (ordine)

```
┌─ Abitudini ─────────────────────────────────────────────┐
│  Chi parla, quanto, quando — solo osservato sullo SPAN  │
│                                                         │
│  [5] BADGE COVERAGE          ← prima di tutto           │
│  [meta] direzione dal … · finestra 7g                   │
│                                                         │
│  [1] Con chi parla           top destinazioni (IP)      │
│  [2] Direzione               out|in per riga top        │
│  [3] Volume + orari          totale 7g + fascia 0–23    │
│  [4] Porte                   chip a scomparsa           │
└─────────────────────────────────────────────────────────┘
```

Densità: max **8–12 destinazioni** visibili; resto «+N altre» collassato. Niente tabella densa 50 colonne. Una riga ≈ destinazione + mini-barra + 1–2 cifre.

#### (1) Con chi parla

```
Con chi parla                          7 giorni
────────────────────────────────────────────────
  13.224.119.231          ████████░░  4.0 MB
  192.168.2.93            ███████░░░  5.0 MB
  8.8.8.8                 ███░░░░░░░  0.9 MB
  … +9 destinazioni
```

- Colonna primaria: **IP grezzo** oggi; spazio riservato a sinistra/sopra per **nome Wave 1b** (stesso slot: oggi IP mono-riga, domani `Nome\nIP` o `Nome · IP`).
- Ordine: `bytes_total` desc.
- Click destinazione (opz. dopo): niente ora — Wave 1a solo lettura statica.

#### (2)+(1) Direzione — legata alla riga destinazione

Vedi §4: la direzione vive **sulla riga**, non in un blocco separato enorme.

#### (3) Volume + orari

```
Volume 7g          124 MB
Attivo tipicamente  ▁▂▁▁▃▇█▇▅▂▁▁▁▁▁▁▁▂▃▅▇█▇▃▁▁  (ore)
                    0        6        12       18    23
```

Una sola riga sparkline 24 celle + totale. Dettaglio ore solo in tooltip (`14:00 → 18 MB`).

#### (4) Porte a scomparsa

```
Porte  [443] [55443] [53]  ·  mostra tutte ▾
```

Default: top 3–5 per volume. Espansione → lista corta `port/proto · volume`. Nessun muro di porte efimere.

#### (5) Badge coverage — in cima

Sempre la prima riga utile della sezione (come semaforo OS in Chi sei). Testo esatto §6.

---

### 4. Direzione in/out — 3 opzioni (sceglierne una in review)

Caso d’uso guida: **IoT che riceve molto** (in ≫ out) deve saltare all’occhio.

#### Opzione A — Barra divisa out|in (consigliata)

```
  13.224.119.231
  out ▐████░░░░░░░░░░░░░░░░▌ in     0.4 | 3.6 MB
       ←── 10% ──→←──── 90% ────→
```

- Segmento sinistro = out, destro = in; proporzioni sul **sottoinsieme con direzione**.
- Colori: out = tono «emesso», in = tono «ricevuto» (nella palette Matrix esistente — no viola AI-default; riuso accent già in app).
- Se `bytes_out/in` null sulla riga: niente barra; solo volume totale + «—».

**Pro:** squilibrio visibile in 200 ms. **Contro:** serve legenda corta una volta («out = verso destinazione · in = dalla destinazione»).

#### Opzione B — Freccia + ratio

```
  13.224.119.231     4.0 MB     in ←────●── out    9∶1
```

**Pro:** esplicito. **Contro:** meno «quanto» assoluto; ratio confonde su volumi piccoli.

#### Opzione C — Due micro-barre affiancate

```
  13.224.119.231
  ↑ out  ██░░░░  0.4 MB
  ↓ in   ████████████  3.6 MB
```

**Pro:** confronto assoluto chiaro. **Contro:** altezza 2× (densità peggiore su 12 righe).

**Proposta default per review:** **A**, con fallback testo se coverage direzione < soglia (es. <20% samples): mostra solo volume + meta «direzione ancora scarsa».

---

### 5. Orari — mock

**Consiglio:** sparkline 24 barre (una per ora UTC→locale LAN documentato in footnote UI: «ore Europe/Rome»), non heatmap 7×24 (troppo denso per Strato 4).

```
Quando è attivo (7g, ora locale)
0  . . . . . . 6  . . . . . .12 . . . . . .18 . . . . . .23
▁  ▁ ▁ ▂ ▃ ▅ ▇ █ ▇ ▅ ▃ ▂ ▁ ▁ ▁ ▂ ▃ ▅ ▇ █ ▇ ▅ ▂ ▁
              └ picco mattina ┘         └ picco sera ┘
```

Tooltip su cella: `mar–dom · 21:00 · 12 MB · 34 oss.`.  
Se tutto piatto/zero: «nessun pattern orario in finestra» (non «dormiente» — giudizio vietato).

---

### 6. Badge coverage — testi esatti

Posizione: **prima riga** sotto il purpose, prima delle destinazioni.

| Stato | Label corta (badge) | Motivo (title / riga secondaria) |
|-------|---------------------|----------------------------------|
| **completo** | `Traffico: copertura completa` | `Path wired su ramo uplink mirrorato (SPAN). Assenza di flow = silenzio osservato.` |
| **parziale** | `Traffico: copertura parziale` | Motivo tipizzato, es. `WiFi↔WiFi sullo stesso AP non passa dallo SPAN.` / `East-west su access switch senza uplink mirrorato.` |
| **sconosciuto** | `Traffico: copertura sconosciuta` | `Topologia/porta/link non abbastanza chiari per giudicare cosa lo SPAN vede.` |

Sorgenti mirror note (config, non ancora tabella DB): **LGS328C p1 / p21 / p24** → sink **p22** (Cassiopea). Usarle nella logica coverage in implementazione; in UI bastano badge+motivo, senza elencare porte a meno che coverage=parziale e il motivo le citi.

Tone: descrittivo, mai «affidabile al 100%» / «cieco = sospetto».

---

### 7. Stati vuoti / parziali (trasparenza sull’ignoto)

#### Device senza flow in finestra

| Coverage | Cosa mostra |
|----------|-------------|
| **completo** | Badge completo + blocco vuoto: `Nessun flusso osservato in 7 giorni. Con copertura completa, questo è silenzio osservato sullo SPAN.` Niente lista destinazioni finta. |
| **parziale** | Badge parziale + motivo + `Nessun flusso in 7 giorni. Può esserci traffico non mirrorato (es. WiFi↔WiFi).` |
| **sconosciuto** | Badge sconosciuto + `Nessun flusso in 7 giorni — non sappiamo se il device è quieto o fuori dallo SPAN.` |

#### Pochi dati (es. 1–3 destinazioni, pochi MB)

Mostrare comunque la struttura completa, con meta onesta:

```
Copertura: parziale — WiFi↔WiFi…
Direzione dal 23 Jul · 2 osservazioni su 2
Con chi parla
  8.8.8.8   …  12 KB
Volume 7g   12 KB   · campione ancora sottile
```

Niente padding con placeholder «in calibrazione» inventati; se campione sottile, dirlo in una riga.

#### Direzione ancora tutta NULL (post-deploy, prima ora chiusa)

```
Volume 7g  124 MB          ← ok, storico
Direzione  non ancora disponibile in questa finestra
           (pipeline attiva; attende ore chiuse post-0.10.0)
```

Barre out|in assenti; lista destinazioni solo volume.

---

## Mock completo (happy path — IoT che riceve)

```
┌─ Abitudini ──────────────────────────────────────────────┐
│  Chi parla, quanto, quando — solo osservato sullo SPAN   │
│                                                          │
│  ● Traffico: copertura completa                          │
│    Path wired su ramo uplink mirrorato (SPAN).           │
│    Direzione dal 23 Jul 2026 · 38% delle oss. in 7g       │
│                                                          │
│  Con chi parla                                           │
│  13.224.119.231   out ▐█░░░░░░░░░░░░░░░░░░░▌ in  0.4│3.6 MB │
│  192.168.2.93     out ▐████████████████████▌ in  4.8│0.2 MB │
│  8.8.8.8          out ▐██████░░░░░░░░░░░░░░▌ in  0.6│0.3 MB │
│  +5 destinazioni                                         │
│                                                          │
│  Volume 7g  124 MB                                       │
│  Quando     ▁▁▂▃▅▇█▇▅▂▁▁▁▁▂▃▅▇█▇▅▂▁▁                     │
│             0      6     12     18     23                │
│                                                          │
│  Porte  [443] [55443] [53]  · mostra tutte               │
└──────────────────────────────────────────────────────────┘
```

(Nella riga 1 lo squilibrio **in≫out** è evidente a colpo d’occhio — Opzione A.)

---

## Contratto API (carta — non implementare)

```json
{
  "asset_id": 55,
  "window_days": 7,
  "coverage": {
    "state": "completo|parziale|sconosciuto",
    "label": "Traffico: copertura …",
    "reason": "…"
  },
  "direction_since": "2026-07-23T00:00:00Z",
  "direction_sample_ratio": 0.38,
  "totals": {
    "bytes": 129931733,
    "bytes_out": 12000000,
    "bytes_in": 48000000,
    "samples": 706,
    "samples_with_direction": 268
  },
  "destinations": [
    {
      "dst_ip": "13.224.119.231",
      "dst_name": null,
      "bytes": 4160324,
      "bytes_out": 400000,
      "bytes_in": 3600000,
      "samples": 17,
      "samples_with_direction": 6
    }
  ],
  "ports": [{"port": 443, "proto": "tcp", "bytes": 9000000, "samples": 40}],
  "hours": [{"hour": 21, "bytes": 12000000, "samples": 34}],
  "empty_kind": null
}
```

`dst_name: null` oggi = posto Wave 1b.  
`empty_kind`: `null` | `silence_observed` | `maybe_unmirrored` | `unknown_gap` | `thin_sample`.

---

## Decisioni da chiudere in review (prima del Vue)

1. **Direzione:** Opzione **A** (barra divisa) vs B vs C?  
2. **Ore:** timezone **locale LAN** (Europe/Rome) vs UTC in UI?  
3. **Limiti default:** top 8 dest / top 5 porte / 7 giorni — ok?  
4. **Coverage:** implementare logica 3 stati in Parte 2 codice insieme alla sezione, o stub `sconosciuto` finché topologia mirror-sources non è config formale?

---

**STOP FASE A.** Nessuna implementazione Vue/API finché la presentazione non è scelta.
