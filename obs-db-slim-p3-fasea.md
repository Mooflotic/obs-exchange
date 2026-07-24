# OBS-DB-SLIM · Passo 3 — FASE A (sola lettura) · STOP

Branch: `feature/obs-db-slim` · live **0.10.23** · **nessuna scrittura / nessun stop dual-write**.

Obiettivo dichiarato: rendere la legacy *droppabile* senza perdere dati vivi.  
Questa FASE A risponde a R1–R3. I punti 4–6 restano **bloccati** finché i gap R2 non hanno destinazione implementata (non solo nominata).

---

## R1 · `fritz_wlan_assoc` — chi legge, dove migra

### Writer (legacy Observation)

| Path | Comportamento |
|------|----------------|
| `materialize.py:224–232` | Per ogni `wlan_associations[]`: **sempre** `record_observation(kind=fritz_wlan_assoc\|fritz_mesh, …)` — **non** passa da raw / non gated da dedup raw |

Live: ~**216k** `fritz_wlan_assoc` + 163 `fritz_mesh` in `observations`. **0** in `observations_raw`.

### Reader runtime (produzione)

| Consumatore | File:riga | Sorgente dati |
|-------------|-----------|---------------|
| Topologia Wi‑Fi edges | `topology.py:355–397`, `620–623` | **`asset.meta["link"]`** (`source`, `ap_*`, `band`, `observed_at` / `updated_at`) |
| Evidence visibility | `topology.py:611–623` | stesso `link` |
| Materialize link | `wifi_associations.py:18–76` | **scrive** `meta.link` (+ `link_history` max 20) |

**Nessuna query di produzione** del tipo `Observation.kind == 'fritz_wlan_assoc'` (solo test + script RO dossier).

Live check: **43** asset con `meta.link.source ∈ {fritz_wlan_assoc,fritz_mesh}`; link `observed_at` fresco (ciclo collector).

### Destinazione (certa)

| Dato vivo | Destinazione |
|-----------|--------------|
| Associazione client→AP corrente | **`assets.meta.link`** (già aggiornata da `materialize_wifi_association`) |
| Handoff recenti | **`assets.meta.link_history`** (già, ultimi 20) |
| Storico 216k Observation | **non serve al runtime** topologia/scans/detector |

**Non** serve tabella dedicata né backfill su raw per *non perdere* le associazioni vive: sono già sull’asset.  
Le 216k righe Observation sono append-only ridondante rispetto a `meta.link`.

### Verdetto R1

Destinazione chiara → **WLAN non blocca il DROP funzionale** della legacy, a condizione di **continuare** `materialize_wifi_association` e **solo** spegnere `record_observation` sul path wlan (`materialize.py:226`).

---

## R2 · Presence / scans / detectors vs `portal_*`

`fritz_wlan_assoc` **non** è `PORTAL_EVIDENCE` (`trust.py:17–28`; contratto test). Non alimenta presence portal né scan targets.

### Cosa `portal_*` copre già

| Uso | Meccanismo |
|-----|------------|
| Gate “ha evidenza recente” | `asset.portal_last_seen` (`scans.py:116–119`, trust classify, dashboard) |
| First/last backfill | `observe_portal` + campi asset; prefetch Observation solo se `portal_*` assente (`trust.py:440+`) |
| Source map | `asset.presence_sources` (aggiornato in `observe_portal`) |

### Campi / path ancora scoperti (leggono ancora `observations`)

| Reader | File:riga | Cosa prende dalla legacy | Copertura `portal_*` oggi |
|--------|-----------|--------------------------|---------------------------|
| Presence `active_discovery` | `inventory.py:180–194` | Observation portal kinds con `seen_at ≥ 24h` | **No** — usa le righe, non solo `portal_last_seen` (che entra come `old`, riga 204) |
| Scans portal-by-IP | `scans.py:82–98` | Observation `PORTAL_EVIDENCE` + IP &lt;24h | **Parziale** — già anche `IpAddress.source` portal &lt;24h (`scans.py:54–64`); Observation è *supplemento* |
| Detectors | `detectors/__init__.py:86–119` | kinds `dhcp` / `dns_server` / `llmnr` / `nbns` / `mdns` / `ssdp` su Observation &lt;24h | **No** — non usano `portal_*` |
| DNS hysteresis | `identity.py:1375–1378` | Observation `kind=dns` &lt;1h | **No** |

### Destinazioni proposte (per chiudere R2 prima dei punti 4–6)

| Gap | Destinazione proposta |
|-----|----------------------|
| Presence `active_discovery` | `portal_last_seen ≥ cutoff` **oppure** `presence_sources[*]` fresco (≥24h) — equivalenza funzionale se ogni portal source continua a chiamare `observe_portal` |
| Scans Observation branch | Affidarsi a `IpAddress` portal (già scritto da `observe_interface_ip`); opzionale: raw `entity_key`/IP — **dopo** verifica che ogni path portal aggiorni `IpAddress.source` |
| Detectors | **`observations_raw`** filtrato per `source`/`kind` &lt;24h **oppure** lasciare detector shadow finché non migrati (oggi spesso flag-off) |
| DNS hysteresis | `presence_sources["dns"]` ISO timestamp **oppure** raw |

### Verdetto R2

`portal_*` **non** copre tutto ciò che i reader vivi prendono dalla legacy.  
**STOP sui punti 4–6** finché presence (+ scans se si toglie Observation, + detectors/dns) non sono migrati a queste destinazioni.

WLAN (R1) è OK; **presence/detectors** no.

---

## R3 · Dual-write: cosa scrive la legacy da preservare altrove

### Writer

| Call site | Gate | Contenuto Observation |
|-----------|------|------------------------|
| `materialize.py:82` → `identity.record_observation:1438` | `record_legacy` (raw `created=True`, dedup 60s) | `kind`, `mac`, `ip`, `hostname`, `vendor`, `payload{proposals,link,fritz_*,…}`, `scan_run_id`, `seen_at=now` |
| `identity.py:408` | stesso gate via nmap MAC | come sopra, kind nmap |
| `materialize.py:226` | **sempre** (wlan) | kind wlan/mesh, mac client, payload `{association:…}` |

### Già preservato altrove (stesso ingest, indipendente da Observation)

| Contenuto | Dove |
|-----------|------|
| Envelope host | `observations_raw` (`write_and_materialize`) |
| Portal first/last + evidence | `observe_portal` → `portal_*`, `presence_sources`, meta.trust |
| Asset / IP / hostname | `upsert_observation_asset` / `observe_interface_ip` |
| Fritz hostlist state | `update_fritz_evidence` / meta.discovery.fritz |
| Wi‑Fi parent | `materialize_wifi_association` → **meta.link** |

### Solo (o principalmente) in legacy Observation oggi

| Contenuto | Impatto se stop write senza migrazione reader |
|-----------|-----------------------------------------------|
| Append storico portal kinds (nmap/icmp/…) | Presence `active_discovery` e scans Observation branch deboli |
| Append `fritz` hostlist (~147k/24h) | **Non** portal evidence; presence non lo usa come discovery; peso solo disco |
| Append wlan | Runtime **OK** via meta.link; storico Observation sacrificabile |
| Append kinds detector (se presenti) | Detectors ciechi |

---

## Previsione (dopo stop dual-write — solo quando GO+gap chiusi)

| Metrica | Atteso |
|---------|--------|
| Righe/min scritte su `observations` | **0** |
| `materialize_wifi_association` | continua (meta.link vivo) |
| Crescita legacy | solo freelist da TTL 7g (passo 2), nessun append |
| File OS | invariato fino VACUUM passo 4 |

---

## Piano 4–6 (NON eseguire — prerequisiti)

Ordine obbligatorio **prima** di spegnere i writer:

1. **Refactor presence** (`inventory.py`): `active_discovery` ← `portal_last_seen` / `presence_sources` (test di equivalenza).
2. **Scans**: assert che `IpAddress` portal basti; rimuovere o rendere opzionale il branch Observation.
3. **Detectors / DNS**: puntare a raw o `presence_sources` (o documentare detector off).
4. Solo allora: togliere `record_observation` da `materialize.py:82`, `:226`, `identity.py:408` (flag `OBS_LEGACY_OBSERVATION_WRITE=0` consigliato per rollback).
5. Backfill: **non** richiesto per wlan (meta.link già). Eventuale one-shot: trust `portal_*` da Observation residuale dove ancora null (già fa reconcile).
6. Legacy sola-lettura → candidata DROP/TRUNCATE al passo 4 + VACUUM. **Niente DROP qui.**

---

## Diff

Nessun diff codice in questa FASE A (sola lettura).  
Report: questo file.

---

## STOP

| Domanda | Esito |
|---------|--------|
| R1 destinazione wlan certa? | **Sì** → `assets.meta.link` |
| R2 presence/scans/detectors coperti solo da portal_*? | **No** — gap elencati |
| Procedere a 4–6? | **No** finché gap R2 non hanno codice+test |

Attendo review: o (A) GO su sotto-passo “presence→portal_* first”, o (B) rivedere destinazioni detectors.
