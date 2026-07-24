# OBS-033 FASE A — Qualità delle proposte (sola lettura)

**Data:** 2026-07-24 · **VERSION live:** 0.10.20  
**Scritture / codice / deploy:** nessuna  
**Dump:** Cassiopea `_serialize` + `NameProposal` pending (140)

---

## Q0 — Massa post-032

**Sì, eseguita** (Michele).

| Voce | Valore |
|------|--------|
| Passate | **2** (60 @ 17:18:50 + 1 @ 17:21:03) |
| Pulsante massa finale | sezione rumore assente (griglia **0**); residuo `noiseProposalIds` **2** (nascosti) |
| Gruppo chassis | **10** (atteso 10) — **ok** |
| Top diversa | **1** (atteso 0) — diverge: `#2` LGS328C `Switch`/dns 0.6 vs `Switch Linksys`/oui 0.4 |

Dettaglio: `obs-032-postmassa.md`.

---

## Q0b — Sidebar versione «24/07»

**Lettura dello screenshot, non un bug di prodotto.**

Componente (`App.vue`):

```js
versionLabel = ver ? `v${ver} · ${buildId}` : buildId
// ver ← /api/health.version ; buildId = __BUILD_ID__ (solo gg/mm)
```

Misura DOM oggi: **`v0.10.20 · 24/07`**.  
Se health fallisce o non è ancora arrivato, resta solo `24/07` (fallback `buildId`). L’assert post-deploy vedeva già la forma completa.

---

## A1 — SSDP come sorgente nomi

| Metrica | N |
|---------|--:|
| Pending `source=ssdp` | **10** |
| Contengono `/` | **10** |
| Contengono `UPnP` | **6** |
| > 4 parole | **5** |

### Prime 15 (tutte e 10)

| asset | nome attuale | proposta | rank | gruppo top |
|------:|--------------|----------|-----:|------------|
| 21 | FRITZ!Repeater SalaPC | Fritz-SalaPC UPnP/1.0 AVM FRITZ!Repeater 6000 253.08.25 | 5 | verifica |
| 22 | FRITZ!Repeater Cucina | Fritz-Cucina UPnP/1.0 AVM FRITZ!Repeater 6000 253.08.25 | 5 | verifica |
| 23 | FRITZ!Repeater SalettaTV | Fritz-CameraOspiti UPnP/1.0 AVM FRITZ!Repeater 6000 253.08.25 | 5 | verifica |
| 24 | FRITZ!Repeater CabinaArmadio | Fritz-CabinaArmadio UPnP/1.0 AVM FRITZ!Repeater 2400 169.08.25 | 5 | verifica |
| 43 | Sky | MR-Device/1.0.0 (Sky, EM150, ) | 3 | chassis |
| 47 | LSX | KnOS/3.2 UPnP/1.0 DMP/3.5 | 3 | verifica |
| 53 | Amazon | Linux/4.4.162+, UPnP/1.0, Portable SDK for UPnP devices | 3 | verifica |
| 58 | Sky | GW-Device/1.0.0 (Sky, ES240, ) | 3 | chassis |
| 61 | Sky | MR-Device/1.0.0 (Sky, EM150, ) | 3 | chassis |
| 89 | *(vuoto)* | MR-Device/1.0.0 (Sky, EM150, ) | 3 | none (non top-conf) |

### Dove nasce

1. **Collector** `probe_ssdp` — [`collector/adapters/mdns_ssdp.py:35–45`](../collector/collector/adapters/mdns_ssdp.py): header HTTP **`SERVER:`** → campo `vendor`.
2. Envelope — [`collector/providers/ssdp_hosts.py:35`](../collector/collector/providers/ssdp_hosts.py): `raw.proposals.ssdp = vendor[:80]`.
3. Persistenza — [`api/app/services/materialize.py:60–61`](../api/app/services/materialize.py) → [`identity.attach_ssdp_evidence:302–327`](../api/app/services/identity.py): `NameProposal(source="ssdp", value=vendor[:255], confidence=0.55)`.

Campo SSDP usato: **header `SERVER`** (non `LOCATION` / `USN`, che restano in raw).

---

## A2 — Nomi curati senza provenienza

| Metrica | N |
|---------|--:|
| Asset con nome non vuoto e `field_sources.name` assente | **58** |
| Di cui MAC presente in `mappa.json` anagrafica | **48** |
| Di cui stesso nome della mappa | **21** |
| Con ≥1 pending più specifica (upgrade di specificità) | **13** |
| Oggi in gruppo **adotta** (D4 li manderebbe in verifica se `field_sources.name.source=manual`) | **0** |

### Fonte del dato

[`api/app/services/migrate.py:124–148`](../api/app/services/migrate.py) `import_legacy`: da `mappa.json` → `anagrafica[mac].nome` scrive `asset.name` **senza** valorizzare `meta.field_sources.name`.

### Backfill (non eseguito)

- **Tabella/campo:** `assets.meta` (JSON) → chiave `field_sources.name`
- **Valore proposto:** `{ "source": "legacy", "confidence": 1 }` (o `"import"` / `"mappa"`) per asset il cui nome coincide con l’anagrafica legacy  
- **Non** equivale a `manual` → **non** attiva D4 da solo; per protezione D4 servirebbe `source: "manual"` o `manual_overrides`

---

## A3 — Proposte rank 1 (sintetiche) — dimensionamento D12

| Metrica | N |
|---------|--:|
| Pending con `scoreSpecificity=1` | **44** |
| Asset distinti | **35** |
| Su asset con nome vuoto/null | **38** |
| Il cui asset ha top-row **≠ rumore** | **44 / 44** |

Con nome vuoto (score 0) un sintetico rank 1 è *più* specifico → finisce in verifica (sotto-soglia / chassis / …), non in rumore. È il volume rilevante per D12.

---

## A4 — Parità normalizeName vs rank

Coppie (nome attuale, proposta) con `normalizeName` uguale ma rank diversi: **0**.

### Caso richiesto (normalize **diverso** — spazio vs `-`)

| Stringa | Rank | Regola che produce |
|---------|-----:|--------------------|
| `BTicino F454` | **3** | fallback `if (/\s/.test(n)) return 3` (`triageRules.js` ~115) |
| `Bticino-F454` | **5** | hostname `alnum-dash-digit` (`triageRules.js` ~74–78) |

`normalizeName` collassa spazi ma **non** normalizza i trattini → le due stringhe non sono la stessa chiave; non entrano nel conteggio A4.

---

## Pending by source (contesto)

dns 65 · fritz 44 · oui 14 · **ssdp 10** · ai 5 · dhcp 2 · **totale 140**
