# OBS-3b-recon — chiusura a costo zero + ricognizione mirata 3b

**Data:** 2026-07-25 · **Live:** 0.10.24 · **Scope:** Parti 1–2 azioni sicure; Parte 3 sola lettura  
**STOP:** nessuna riscrittura reader · nessun deploy · decisione 3b dopo review

---

## Parte 1 · Pulizia working tree

### 1a · `_tmp_chiusura_census.py`

| Check | Esito |
|-------|-------|
| File presente (locale / NAS) | **NO** — già assente |
| `rg '_tmp_chiusura_census'` su repo | **0 match** (nessun import / riferimento) |
| Azione | Nessuna cancellazione / nessun commit (già orfano e rimosso) |

### 1b · `git status`

Branch: `main` (allineato a `origin/main`).

**Nessun file spuri di tipo `_tmp_*`.** Restano solo untracked in `observatory/docs/`:

| File | Nota |
|------|------|
| `obs-chiusura-fasea.md` | OK lasciare (report chiusura) |
| `obs-db-slim-p2-go.md` | report GO passo 2 |
| `obs-db-slim-p3-fasea.md` | report 3 FASE A |
| `obs-db-slim-p3a-go.md` | report 3a GO |
| `obs-deploy-01-go.md` | report deploy-01 |

Tree “pulito” rispetto a diagnostici temporanei; i docs di cantiere restano untracked (non commit obbligatorio qui).

---

## Parte 2 · Gesti manuali (Michele)

### 2a · Asset 5

**CHIUSO di fatto — nessuna azione.**

- Asset id=5: `Cassiopea — NIC 1`, status `noto`
- Conteggio asset nome `ADM-Free-OS-028b`: **0**

### 2b · «Archivia rumore» — NON eseguito (sola lettura)

Live `noiseProposalIds` (stessa funzione UI `triageRules.js`): **39** (era ≈37 in chiusura; delta = nuove pending).

Scomposizione (priorità: chassis → D13 → D12 → altro):

| Bucket | N | Significato |
|--------|---|-------------|
| **chassis** (D5-bis, inclusi in massa) | **6** | membri chassis ≥2 con proposta rumore |
| **D13** (normalizeName uguale) | **20** | proposta ≡ nome attuale |
| **D12** (rank 1 sintetico) | **12** | `PC-…` / MAC / IP sintetici |
| **secondo livello** | **0** | nessuno fuori dalle regole sopra |
| **D3 rank** (parità, non D12/D13) | **1** | `Apparato ASUS` vs `MacBookhristian` (id proposta **360**) |
| **Totale** | **39** | = somma |

**Chassis (6):** 242 (asset 10), 268 (109), 270/272/269/271 (110).

**D13 (20):** doppietti dns+fritz su Broadlink / iPad / LGwebOSTV×2 / Mac×2 / MacBookhristian / Somneo / Spazio / garmin-fenix8…

**D12 (12):** 224, 236, 196/195, 198/197, 202/201, 212, 221, 229, 259 — tutti `PC-*` sintetici.

**IDs completi (39):**  
`242, 224, 236, 153, 113, 169, 120, 173, 123, 174, 124, 179, 128, 178, 129, 180, 360, 196, 195, 198, 197, 202, 201, 212, 221, 229, 259, 268, 270, 272, 269, 271, 292, 291, 294, 293, 317, 316`

Massa = click UI Michele. Cursor non archivia.

---

## Parte 3 · Ricognizione 3b (sola lettura)

### 3a · Cosa significa «detectors off» oggi

**Non girano.** Non è “scrivono solo shadow”: con lista vuota **non eseguono**.

| Pezzo | Dove | Effetto |
|-------|------|---------|
| Flag | `detectors_enabled: str = ""` · `config.py:108` | env `DETECTORS_ENABLED` |
| Lista | `detector_list` · `config.py:130-131` | split CSV |
| Gate | `_enabled` · `detectors/__init__.py:19-21` | `return name in detector_list` — **default OFF** |
| Live | `detectors_enabled=''` → `detector_list=[]` | findings=0, drifts=0 |

Se si abilitassero: i detector M6 tipici usano `upsert_deterministic_finding` → **`shadowed=False`** (verdetti reali, non shadow). Solo path compositi/drift usano shadow:

- `finding_from_drifts` · `findings.py:90,118` — shadow se `not scoring_calibrated` o `drift_shadow_mode`
- `drift.py:104` — `shadow = drift_shadow_mode or not scoring_calibrated`
- Live: `scoring_calibrated=False`, `drift_shadow_mode=True`

**Flickering:** non c’è un detector “flickering” attivabile; l’isteresi trusted scan (DNS) è in `identity.py`, indipendente da `DETECTORS_ENABLED`.

### 3b · Calibrazione day 5/14 — cosa accumula

Live: `active=True`, **day 5/14**, `started_at=2026-07-20T01:12:46Z`, fine finestra ~**2026-08-02/03** (day 14), non 08-05/06.

| Cosa | Tabella / campo | Sorgente dati | Legge Observation legacy? |
|------|-----------------|---------------|---------------------------|
| Orologio giorno N/14 | min(`MetricSnapshot.taken_at`, `SensorRun.started_at`) | `build_calibration_status` · `reliability_metrics.py:165-190` | **NO** |
| Snapshot metriche | `metric_snapshots` (109 righe live) | `snapshot_reliability_metrics` · `:149-157` | **NO** |
| Contenuto metriche | `Asset.presence_state`, `Event` 24h, **count** `ObservationRaw`/`ObservationAggregate`, `SensorRun` | `compute_reliability_metrics` · `:80-146` | **NO** (solo count raw, non legacy) |

**Conclusione:** la calibrazione **non legge** Observation legacy né il contenuto di `observations_raw`. Accumula stato derivato (presence/events) + conteggi store + clock su snapshot/sensor.

### 3c · I tre reader — finestra e legame calibrazione

| Reader | File:riga | Finestra legacy | Alimenta calibrazione? |
|--------|-----------|-----------------|------------------------|
| `inventory.active_discovery` | `inventory.py:180-194` | Observation per MAC, `seen_at ≥ cutoff` (`ASSET_STALE_AFTER_HOURS`, default **24h**); filtra `is_portal_evidence(kind)` | **Indiretto:** cambia `operational_state` / hidden → può influenzare `presence_state` contati in MetricSnapshot |
| `scans._fresh_portal_sources_by_ip` | `scans.py:82-98` | Observation `kind ∈ PORTAL_EVIDENCE`, IP current, **&lt;24h** (`TARGET_MAX_AGE`); già OR con IpAddress | **NO diretto** (non entra in reliability metrics) |
| detectors M6 | es. `detectors/__init__.py:86-90`, `:116-119` | Observation **24h** (dhcp/dns_server / llmnr…) | **NO** finché off; se on → findings (non clock calib) |
| DNS hysteresis | `identity.py:1373-1378` | Observation `kind=dns`, MAC, **&lt;1h** | **Indiretto se cambia:** blocca/consente `endpoint.missing` → `presence_flap_24h` in snapshot |

### 3d · VERDETTO ESPLICITO (una riga)

| Reader | Tocca calibrazione? | Perché |
|--------|---------------------|--------|
| migrare **active_discovery** | **SI** (indiretto) | può cambiare chi è stale/active → `presence_state` → coverage negli snapshot |
| migrare **scans** | **NO** | solo gating target scan; non alimenta MetricSnapshot / clock |
| migrare **detectors/DNS** | detectors **NO** (off); DNS hysteresis **SI** (indiretto) | DNS può variare `endpoint.missing` → flap metrics |

**Quindi 3b NON parte intero.** Spezzare:

| Ora (safe-ish) | Rimandare fino a fine calib (~day 14) o dopo assert |
|----------------|------------------------------------------------------|
| **scans** (se destinazione popolata — vedi 3e) | **active_discovery** (effetto presence) |
| detectors (restano off; migrazione irrilevante) | **DNS hysteresis** (effetto eventi flap) |

### 3e · Destinazione post-migrazione + evidenza equivalenza

| Reader | Destinazione candidata | Dato equivalente già presente? | Migrabile ora? |
|--------|------------------------|--------------------------------|----------------|
| active_discovery | `asset.portal_last_seen` e/o `presence_sources[portal_kind]` (come `observe_portal` · `trust.py:40-57`) | **SI** — live: `portal_last_seen` 24h ≈84; `presence_sources`: nmap=66, fdb=99, fritz_hostlist=148 (ISO timestamp) | Dato OK; **rimandare per 3d** (tocca calib) |
| scans | `IpAddress` source ∈ `PORTAL_EVIDENCE` + `last_seen` &lt;24h | **NO equivalenza** — current IpAddress: solo `fritz`/`mgmt` (fritz **non** portal); nmap su IpAddress rarissimo/non current; Observation portal 24h = **nmap 5665** ancora necessario | **NON migrabile** finché dual-write/materialize non popola `IpAddress.source` portal (o si ridefinisce il gate su `presence_sources`+IP current — cambio semantico) |
| detectors | Observation → raw/Endpoint già per certi detector | N/A mentre `DETECTORS_ENABLED=""` | skip |
| DNS hysteresis | `presence_sources["dns"]` | **NO** — live `assets_with_dns_ps=0`; `dns_obs_1h=0` (anche legacy vuota ora) | **NON migrabile** finché `observe_portal(..., "dns")` non popola; rimandare anche per 3d |

Parallelo 3a (`meta.link`): WLAN aveva già destinazione piena → stop scrittura OK. Qui **scans** e **DNS** non hanno ancora lo stesso livello di equivalenza su tabella destinazione.

---

## Raccomandazione per la review (STOP)

**3b spezzato, non intero, non tutto rimandato.**

1. **Ora:** nessuna riscrittura (questo report). Opzionale: pianificare solo **scans** *dopo* aver popolato IpAddress portal (o dopo design gate su `presence_sources`).
2. **Dopo calibrazione** (`scoring_calibrated` o fine day 14 ~2026-08-02/03): **active_discovery** → `portal_last_seen` / `presence_sources`.
3. **DNS hysteresis:** dopo popolamento `presence_sources.dns` **e** fuori finestra calib (o con baseline flap accettata).
4. Detectors: restano off; non bloccano 3b.

**Non fare in questo cantiere:** deploy, Archivia rumore, stop dual-write host, VACUUM, rewrite reader.
