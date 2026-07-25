# OBS-3b-i-gap — migrazione scans: delta legacy → IpAddress

**Data:** 2026-07-25 · **Live:** 0.10.24 · **Scope:** sola lettura  
**STOP:** nessuna modifica codice/DB/config · nessun deploy

Contesto: tra i reader 3b, solo `scans` non tocca la calibrazione; bloccato perché IpAddress portal «non equivalente». Qui il delta esatto.

---

## A · Cosa legge scans dalla legacy

### A1 · Branch Observation (`scans.py:82-98`)

```82:98:observatory/api/app/services/scans.py
    since = now - TARGET_MAX_AGE
    observations = db.scalars(
        select(Observation).where(
            Observation.seen_at >= since,
            Observation.ip.in_(sorted(current_ips)),
            Observation.kind.in_(sorted(PORTAL_EVIDENCE)),
        )
    ).all()
    for obs in observations:
        if obs.mac and macs and normalize_mac(obs.mac) not in macs:
            continue
        try:
            safe_ip = validate_scan_target(obs.ip, settings.network_cidr)
        except ValueError:
            continue
        found.setdefault(safe_ip, []).append(str(obs.kind or "").lower())
    return found
```

| Aspetto | Dettaglio |
|---------|-----------|
| **Campi letti** | `seen_at`, `ip`, `kind`, `mac` (solo per filtro MAC) — **non** legge `hostname`/`vendor`/`payload` |
| **Filtro kind** | `Observation.kind ∈ PORTAL_EVIDENCE` = `{arp, icmp, dns, mdns, snmp, lldp, fdb, ipp, service, nmap}` (`trust.py:17-29`) |
| **Finestra** | `seen_at ≥ now − TARGET_MAX_AGE` = **24h** (`scans.py:27`) |
| **Scope IP** | solo IP già `is_current` sull’asset (raccolti subito sopra) |
| **Filtro MAC** | se l’obs ha MAC e l’asset ha MAC: deve matchare; altrimenti passa |
| **Output** | arricchisce `found: dict[ip → list[source/kind]]` — stesso map prodotto anche dal branch IpAddress (`:54-64`) |
| **A valle** | `scan_target_candidates` (`:125-138`) tiene solo IP **current** presenti in `found`; costruisce candidati scan (`ip`, `sources`, `best_source`, …). **Non** scrive presence / eventi / metriche |

Pre-condizioni fuori da questo branch (già su Asset): `portal_last_seen` fresco &lt;24h (`:116-119`).

### A2 · Kind reali consumati (live, ultime 24h)

| kind ∈ PORTAL_EVIDENCE | COUNT Observation 24h |
|------------------------|----------------------:|
| **nmap** | **5665** |
| arp, icmp, dns, mdns, snmp, lldp, fdb, ipp, service | **0** |
| **Totale portal** | **5665** |

- IP distinti (CIDR-validi) con evidenza portal in legacy 24h: **67**
- Kind per IP: solo `('nmap',)` su tutti e 67
- Dopo join asset+MAC+`is_current`: **60** coppie `(asset_id, ip)` per cui il branch Observation contribuisce al gate

---

## B · Destinazione IpAddress oggi

### B1 · Schema e writer

Tabella `ip_addresses` (`models.py:119-135`):

| Campo | Tipo | Ruolo per scans |
|-------|------|-----------------|
| `interface_id`, `ip` | FK + str | binding (unique iface+ip) |
| `is_current` | bool | candidato scan |
| `first_seen` / `last_seen` | datetime | freschezza (&lt;24h nel branch portal) |
| `source` | str(32) | **unico** segnale “è portal?” via `is_portal_evidence(source)` |
| `role` | str | irrilevante per scans |

**Chi scrive:** `observe_interface_ip` · `identity.py:720-780`, chiamato da `upsert_observation_asset` · `:1104-1116` (materialize / nmap / fritz / …).

Comportamento critico (`:736-738`, `:761-765`):

- su riga esistente: aggiorna sempre `last_seen`
- aggiorna `source` **solo se** il nuovo source ha rank ≥ vecchio (`IP_SOURCE_RANK`: fritz=80, mgmt=90, **nmap=50**)
- quindi **nmap dopo fritz non promuove `source` a nmap** (by design, anti-demotion election)

Copertura writer: ogni path che passa da `upsert_observation_asset` con IP; nmap mac-host sì. Non crea una seconda riga per lo stesso `(iface, ip)` (unique constraint).

Live `ip_addresses` per source × is_current:

| source | is_current | N |
|--------|------------|--:|
| fritz | true | 94 |
| fritz | false | 16 |
| mgmt | true | 3 |
| **nmap** | **false** | **5** |
| nmap | true | **0** |

Le 5 `source=nmap` sono IP secondari non current (es. 192.168.1.4–6, .9 su asset 1; .117 su 51) — utili solo per *quei* IP nel branch IpAddress, non per i 60 current.

### B2 · Confronto sugli stessi (asset, IP) che la legacy alimenta

Universo: **60** `(asset_id, ip)` con contributo Observation portal &lt;24h.

| Esito vs IpAddress «equivalente»* | N | Note |
|-----------------------------------|--:|------|
| **Equivalente pieno** (`source` portal + `last_seen` &lt;24h + stesso IP current) | **0** | |
| **Parziale** | **60** | riga `is_current` presente; `source` ∈ {fritz, mgmt} (**non** portal) |
| **Mancante** (nessuna riga IP) | **0** | |
| Branch IpAddress portal che già copre la coppia | **0** / 60 | Observation **necessaria** per tutte e 60 |
| Branch IpAddress portal solo (senza obs) | **5** | i 5 nmap non-current |

\*Equivalente = ciò che il branch IpAddress (`scans.py:54-64`) accetterebbe senza Observation.

Current source sulle 60: `fritz`×58 + `mgmt`×3.  
`last_seen` IpAddress è in genere **più fresco** dell’ultimo nmap obs (p50 delta obs−ip ≈ −13 min) — la freschezza c’è; manca il **flag portal su `source`**.

In parallelo: `presence_sources.nmap` fresco &lt;24h su **63** asset — segnale portal a livello asset già popolato da `observe_portal`, ma **non** letto da `scans` oggi.

---

## C · Il delta (cuore)

### C1 · Campo per campo

| Cosa scans prende da Observation | In IpAddress? | Natura del gap |
|----------------------------------|---------------|----------------|
| `kind` portal (oggi quasi solo `nmap`) come evidenza per IP | Campo `source` **esiste** ma resta `fritz`/`mgmt` per sticky rank | **Presente, non popolato come portal** (writer non può/non vuole sovrascrivere) |
| `seen_at` &lt;24h | `last_seen` esiste e di solito è fresco | **Non è un gap di finestra** (stessa 24h; IpAddress trattiene l’ultima vista, non TTL 7g) |
| `ip` | `ip` | OK — 60/60 presenti |
| `mac` (filtro) | via `Interface.mac` | OK |
| Multi-source per stesso IP (fritz + nmap) | **Un solo** `source` per `(iface, ip)` | Limite di modello: election vs portal evidence in conflitto sullo stesso campo |

**Non serve** nuova colonna *obbligatoria* se si cambia il reader; **serve** se si vuole tenere IP-level portal evidence senza toccare `source` sticky.

Schema assente? **No** per i campi che scans usa oggi.  
Finestra più corta su IpAddress? **No**.

### C2 · VERDETTO forma del fix (senza implementare)

**(a) solo ripuntare — NO.** Destinazione non equivalente: 0/60. Il report 3d aveva ragione.

**(b) solo backfill `source=nmap` — NO come fix primario.** Violerebbe lo sticky rank (`nmap` 50 &lt; `fritz` 80); romperebbe l’election IP. Backfill storico di `source` è sbagliato.

**(c) campo/tabella additiva — VIABILE.** Es. `IpAddress.portal_last_seen` (o `portal_kinds` JSON) aggiornato da `observe_portal` / upsert portal **senza** cambiare `source`. Poi reader scans legge quel campo. Schema additivo + writer + backfill 24h.

**(d) altro — VIABILE e spesso preferibile.** Ripuntare il branch Observation su evidenza già derivata:
- `asset.presence_sources[kind]` (nmap già su ~63 asset) **+** binding `IpAddress.is_current`, oppure
- solo `portal_last_seen` asset (già gate `:116-119`) + current IP — più largo, meno fedele al per-IP.

**Verdetto C2:** **(d) oppure (c)** — non (a), non (b) puro.  
Raccomandazione operativa per il prompt di implementazione: partire da **(d)** zero-schema (reader su `presence_sources` portal + IP current), con assert di parità candidati vs branch Observation; se serve granularità per-IP senza demotion → **(c)**.

### C3 · Backfill e finestra TTL 7g

| Domanda | Risposta |
|---------|----------|
| Serve backfill storico profondo? | **No per scans** — gate = **24h**. Non servono i 7 giorni di legacy. |
| Se (d) | Backfill **0** — `presence_sources.nmap` già vivo |
| Se (c) | Backfill ~**60** righe da Observation `kind=nmap` ultime 24h **oppure** da `presence_sources` — non dalla coda TTL |
| Vincolo ~27/07 (prune legacy day-0)? | **Non critico per 3b-i scans**: nmap continua a scrivere ogni ciclo; anche se Jul 20 esce dal TTL, le 24h correnti restano. Nessuna corsa al backfill pre-prune per questo reader |
| Legacy portal tot | ~28.8k righe nmap; min `seen_at` 2026-07-20 — ancora dentro i 7g; older_than 5–7d = 0 al momento del census |

---

## D · Non-interferenza calibrazione

### D1 · scans è isolato?

Evidenza:

1. `scans.py` **non** referenzia `presence_state`, `endpoint.missing`, `MetricSnapshot`, `reconcile_asset_presence`, né DNS hysteresis.
2. `_fresh_portal_sources_by_ip` / `scan_target_candidates` sono usati solo dal flusso scan target / enqueue (`:201`, `:262`) — gating candidati, non stato presence.
3. Calibrazione (`reliability_metrics.py`) legge Asset.presence_state, Event flap, count raw/aggregate, SensorRun — **nessuna** API scans.
4. Reader bloccati fino a fine calib:
   - `inventory.active_discovery` → Observation → operational_state / presence
   - DNS hysteresis `identity.py:1373+` → `endpoint.missing`
   - Migrare **solo** il reader scans (togliere il `select(Observation)` e usare IpAddress/`presence_sources`) **non** esegue quei path.

**Conferma:** sì — scans è isolato; 3b-i non riapre active_discovery né DNS.

---

## Nota pulizia docs (untracked)

I report di sessione in `observatory/docs/` già pubblicati su **obs-exchange** (`obs-3b-recon`, `obs-chiusura-fasea`, `obs-db-slim-*-go`, `obs-deploy-01-go`, …) sono **artefatti di scambio + audit locale**: stessa famiglia dei `obs-db-slim-p1.md` già tracked.

**Scelta:** **versionarli** con commit dedicato `docs: report sessione OBS-DB-SLIM` (inclusi `obs-3b-recon.md` e questo `obs-3b-i-gap.md`), così non restano untracked indefiniti. Non sono “solo scratch”: documentano GO/assert e ricognizioni 3b.

---

## STOP

Nessuna riscrittura. Prossimo passo (prompt implementazione 3b-i): scegliere **C2=(d)** o **(c)**; assert parità candidati; zero deploy finché assert verde.
