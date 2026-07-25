# OBS-3b-iii-recon — gap active_discovery + DNS hysteresis

**Data:** 2026-07-25 · **Live:** 0.10.25 · **Calib:** day **6**/14 (started 2026-07-20)  
**Scope:** sola lettura · **STOP:** nessuna modifica · nessuno spegnimento dual-write · nessun deploy

Contesto decisione Michele (non eseguita qui): spegnere dual-write host e rifare calibrazione.  
4a rinviato (freelist≈0). Questo report prepara i due reader ancora su legacy.

---

## A · active_discovery (`inventory.py:180-194`)

### A1 · Codice e effetto

```180:238:observatory/api/app/services/inventory.py
    recent_observations = (
        db.scalars(
            select(Observation).where(
                Observation.mac.in_(macs), Observation.seen_at >= cutoff
            )
        ).all()
        if macs
        else []
    )
    ...
    active_discovery = any(
        is_portal_evidence(observation.kind, observation.payload)
        for observation in recent_observations
    )
    reliable = (
        reachability.get("status") == "reachable"
        or bool(physical_reasons)
        or active_discovery
    )
    ...
    stale = bool(negative and not reliable and old)
    ...
    asset.presence_state = presence_state(asset, now=now, recent_hours=hours)
```

| Aspetto | Dettaglio |
|---------|-----------|
| **Campi** | `Observation.mac`, `seen_at`, `kind`, `payload` (payload passato a `is_portal_evidence`, oggi kind-only) |
| **Filtro** | MAC ∈ interfacce asset; `seen_at ≥ cutoff` |
| **Finestra** | `ASSET_STALE_AFTER_HOURS` (default **24h**) |
| **Kind** | quelli in `PORTAL_EVIDENCE` (`trust.py:17-29`): nmap, fdb, dns, mdns, arp, icmp, … — **non** fritz |
| **Output** | booleano `active_discovery` → entra in `reliable` → evita `stale_unlocated` / unhide; poi `presence_state()` da **`portal_last_seen`** (non dal booleano diretto) |
| **Calibrazione** | **indiretto:** `presence_state` e `operational_state` influenzano coverage in `MetricSnapshot` (`reliability_metrics.py:87-106`) |

Live 24h: Observation portal = quasi solo **nmap** (5542).

### A2 · Destinazione dopo

**`asset.presence_sources[portal_kind]`** (timestamp ISO) e/o **`asset.portal_last_seen`**, già scritti da `observe_portal` (`trust.py:40-57`) su upsert portal.

Evidenza live:

| Segnale | Copertura |
|---------|----------:|
| `presence_sources` portal fresco 24h | nmap **63**, fdb **75** asset |
| `portal_last_seen` fresco 24h | **82** asset |
| Set A (legacy active_discovery True) | **63** |
| A \ B (`presence_sources` portal fresco) | **0** |
| A \ B (`ps` ∪ `portal_last_seen`) | **0** |
| B \ A | **19** (solo destinazione — come scans sticky recovery) |

Equivalente (stesso pattern di scans 3b-i): **sì**.

### A3 · Gap / backfill / TTL

- Gap: **nessuno** per il gate corrente.
- Backfill: **non necessario** per migrare il reader.
- Finestra pre-prune ~27/07: **non critica** per AD (dato già in `presence_sources` / `portal_last_seen`).

---

## B · DNS hysteresis (`identity.py:1373-1388` → `endpoint.missing`)

### B1 · Codice e effetto

```1373:1433:observatory/api/app/services/identity.py
        dns_recent = bool(
            db.scalar(
                select(Observation.id).where(
                    Observation.mac == iface.mac,
                    Observation.kind == "dns",
                    Observation.seen_at >= now - timedelta(hours=1),
                )
            )
        )
        if (
            (cycles < 2 and not timed_out)
            or reachability.get("status") != "no_reply"
            or physical_recent
            or fdb_recent
            or dns_recent
        ):
            continue
        ...
        db.add(Event(type="endpoint.missing", ...))
```

| Aspetto | Dettaglio |
|---------|-----------|
| **Campi** | `Observation.id` (esistenza), `mac`, `kind`, `seen_at` |
| **Filtro** | `kind == "dns"`, MAC interfaccia, `seen_at ≥ now−1h` |
| **Output** | se True → **blocca** emissione `endpoint.missing` |
| **Calibrazione** | **indiretto:** eventi `endpoint.missing`/`recovered` → `presence_flap_24h` in MetricSnapshot |

### B2 · Destinazione

Candidata naturale: **`presence_sources["dns"]`** (stesso `observe_portal(..., "dns")`).

Evidenza live:

| Segnale | Valore |
|---------|-------:|
| Observation `kind=dns` 1h / 24h | **0 / 0** |
| Asset con `presence_sources.dns` | **0** |
| Keys `presence_sources` | solo `nmap`, `fritz_hostlist`, `fdb` |

Il dato **non** è popolato nella destinazione — ma **nemmeno** nella legacy oggi. Equivalenza = **assenza su entrambi i lati**.

### B3 · Gap / backfill / TTL

- **Gap strutturale:** nessun writer live produce Observation `dns` né `presence_sources.dns` (grep collector/api: nessun emit `kind=dns` attivo).
- Backfill da legacy: **0 righe** utili.
- TTL ~27/07: **irrilevante** per DNS (vuoto).
- Prima di affidarsi a DNS come isteresi futura: serve che il path hostname/DNS chiami `observe_portal(asset, "dns", …)` (oggi non lo fa in modo osservabile).

---

## C · Gate di equivalenza

### C1 · active_discovery

| | N |
|--|--:|
| A (legacy True) | **63** |
| B (`presence_sources` portal &lt;24h) | **82** |
| **A \ B** | **0** |
| B \ A | 19 |

Lista A\B: **vuota**.

### C2 · DNS hysteresis

| | N |
|--|--:|
| A (asset con dns Observation &lt;1h) | **0** |
| B (`presence_sources.dns` &lt;1h) | **0** |
| **A \ B** | **0** |

Lista A\B: **vuota** (vacua).

### C3 · VERDETTI

| Reader | Gate | Nota |
|--------|------|------|
| **active_discovery** | **PASS** | Migrabile ora → `presence_sources` portal fresco (± `portal_last_seen`). Stesso pattern di scans. |
| **DNS hysteresis** | **PASS (vacuo)** | Comportamento oggi identico (dns mai “recent”). Destinazione vuota: migrare a `presence_sources["dns"]` è ok come no-op; **non** c’è evidenza positiva da preservare. Opzionale: documentare che DNS isteresi è morta finché non si popola `observe_portal("dns")`. |

---

## D · Piano spegnimento dual-write (progetto)

### D1 · Writer legacy da spegnere + inventario reader

**Writer `record_observation` (host dual-write):**

| Sito | Ruolo |
|------|--------|
| `materialize.py:82` | host generici (arp/fritz/…); gated `record_legacy` |
| `identity.py:408` | nmap MAC path in `attach_nmap_evidence`; gated `record_legacy` |
| `identity.py:1438` | definizione `record_observation` |

WLAN già fuori (3a). Spegnimento = `record_legacy=False` / non chiamare più questi path.

**Inventario reader Observation — NON è solo {AD, DNS, scans}:**

| Reader | Stato | Blocca dual-write stop? | Blocca DROP legacy? |
|--------|-------|-------------------------|---------------------|
| **scans** | migrato 3b-i | no | no |
| **active_discovery** | da migrare | **sì** finché non migrato | sì |
| **DNS hysteresis** | da migrare (vacuo) | sì (codice ancora sulla tabella) | sì |
| **`trust._prefetch_portal_first_last_by_mac`** (`trust.py:322-344`) | **LIVE** ogni bootstrap api (`bootstrap.py:164`) | **Parziale:** non richiede *nuove* scritture se `portal_*` restano aggiornati da `observe_portal`; ma **legge ancora** Observation e può rinfrescare `portal_last_seen` da MAX storico | **sì** (DROP rompe bootstrap) |
| **`trust._portal_extent_nplus1` / `latest_portal_observation`** | test / helper | basso | sì se usati |
| **detectors** (`detectors/__init__.py:89,119`) | **OFF** (`DETECTORS_ENABLED=""`) | no finché off | sì se si accendono |
| **retention** DELETE Observation | manutenzione | n/a (è writer delete) | n/a |

**Conclusione D1:** l’assunto «solo tre reader» è **FALSO**.  
Prima dello spegnimento dual-write (e soprattutto prima del DROP): migrare **AD + DNS**; **migrare o disaccoppiare trust prefetch** da Observation (es. usare solo `portal_first/last_seen` + `presence_sources` / FDB). Altrimenti bootstrap continua a dipendere dalla tabella legacy.

### D2 · Reset calibrazione (descrizione, non eseguire)

Stato attuale: `scoring_calibrated=false` (env); day-clock =  
`min(min(MetricSnapshot.taken_at), min(SensorRun.started_at))` → oggi ancorato al **2026-07-20** (`reliability_metrics.py:165-190`).

| Azione | Effetto |
|--------|---------|
| `SCORING_CALIBRATED=false` | già così — scoring resta in learning |
| `DELETE FROM metric_snapshots;` | azzera la **serie** di metriche; **non** basta a rimettere day=1 perché resta `SensorRun` |
| Day-clock a 0/14 pulito | **manca un epoch dedicato** in config oggi. Opzioni future: (a) env `CALIBRATION_STARTED_AT` / `MEASURE_EPOCH` letto da `build_calibration_status`; (b) truncare anche SensorRun (distruttivo, sconsigliato); (c) accettare day alto ma serie metriche nuova |

Comando previsto (solo piano):

```bash
# 1) dopo migrazioni + dual-write off + assert
# 2) backup DB
# 3) SQL: DELETE FROM metric_snapshots;
# 4) env: SCORING_CALIBRATED=false
# 5) IDEALE: aggiungere CALIBRATION_STARTED_AT=<now> e usarlo nel clock
# 6) restart api; verificare calibration.day ≈ 1 e started_at nuovo
```

### D3 · Ordine sicuro (futuro)

```
1. Migra active_discovery → presence_sources (+ test gate A\B=0)
   rollback: revert reader; dual-write ancora ON
2. Migra DNS hysteresis → presence_sources["dns"] (no-op oggi)
   rollback: revert
3. Migra/disaccoppia trust prefetch da Observation
   (obbligatorio prima di DROP; fortemente consigliato prima di stop dual-write)
4. Inventario finale: rg "Observation" nei path runtime → solo retention/admin
5. Spegnere dual-write host (record_legacy=False / no record_observation host)
   assert: 0 nuove Observation post-deploy_ts; portal_*/presence_sources ancora freschi
6. Reset calibrazione (metric_snapshots + epoch)
7. Più tardi: TTL svuota legacy → DROP → VACUUM 4b
```

Gate per passo: assert numerici pre/post; dual-write resta acceso fino al passo 5.

---

## Sintesi decisione

| Voce | Esito |
|------|-------|
| **C3 AD** | PASS → migrabile subito |
| **C3 DNS** | PASS vacuo → migrabile (no-op); destinazione da popolare solo se si vuole DNS vivo in futuro |
| **D1** | **Altri reader:** trust bootstrap (+ detectors se on). **Bloccano** lo spegnimento “pulito” / DROP se non migrati |
| **Forma 3b-iii** | (1) AD + DNS come scans; (2) trust prefetch nello stesso cantiere o subito dopo; (3) solo poi dual-write off + reset calib |

**STOP** — nessuna riscrittura. Su C3 + D1 si decide se 3b-iii include solo AD/DNS o anche trust.
