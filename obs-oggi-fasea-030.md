# OBS-OGGI-FASEA-030

FASE A sola lettura — fotografia coda triage **Oggi** + contratto dati.
Zero codice, zero deploy. Dump live Cassiopea **2026-07-23 ~23:18 UTC+2**.

---

## Parte 1 — chiusura 029 (conferma)

| Voce | Valore |
|---|---|
| Merge | no-squash `fix/oui-test-restore-029` → `main` |
| Hash | `0196abf6eab7256903e89991315f4f3f224f2908` |
| Messaggio | `Merge branch 'fix/oui-test-restore-029'` |
| Push | `1d3ad4c..0196abf  main -> main` **ok** |
| Tag / VERSION | nessuno / resta **0.10.18** |
| Asset 5 / Fingerbank 027 | non toccati |

---

## A1 — Fotografia della coda

### Da dove pesca Oggi

| Cosa | Dettaglio |
|---|---|
| Vista | `observatory/web/src/views/Oggi.vue` |
| Load | `Promise.all([api.assets({include_historical:"true"}), api.chassis(), api.monitors()])` — **:96–107** |
| Proposte nome | client-side su `asset.proposals` pending, top per `confidence`; skip se `status===ignorato` o `name===top.value` — **:23–48** |
| Device nuovi | `composeDevices` + `isNuovoDaConoscere` — **:51–63** + `inventoryDevices.js:316–317` |
| Monitor | non archiviati + `condition===flapping` **o** `last_status∈{down,degraded}` — **:66–84** |
| Ordine | `proposta_nome` → `device_nuovo` → `monitor`, poi età — **:87–94** |
| **Non** usa | `GET /api/suggestions` |

Endpoint:

- `GET /api/assets?include_historical=true` — `routers/assets.py:247+`, serialize `_serialize` con `name_proposals`
- `GET /api/chassis` — solo per compose nuovi
- `GET /api/monitors`

### Conti live (dump)

| Voce | N |
|---|---|
| Proposte nome in coda (logica Oggi) | **65** |
| Di cui «proposta meno specifica del nome attuale» (euristica A1) | **26** |
| Asset `status=nuovo` grezzi | **45** (UI Oggi filtra con `isNuovoDaConoscere` → sottoinsieme; non ricalcolato qui 1:1) |
| Monitor degradati/flapping | **3** |
| Totale grezzo somma | **113** (sovrastima rispetto alla UI per i «nuovi») |

Esempio sintomo: **8** proposte `Sky` (OUI 0.85) — 4 su asset già nominati (`Sky Q…`, `SkyBooster…`) = rumore less-specific; 4 su `nuovo` senza nome attuale.

### Proposte nome — campi per riga

Vedi appendice JSON (`proposte_nome[]`): `asset_id`, `mac`/`macs`, `ip`/`ips`, `nome_attuale`, `nome_proposto`, `fonte`, `confidenza`, `updated_at`, più `presence_state`, `port_label`, flag rumore.

---

## A2 — Contratto dati per la griglia

Campi richiesti vs `GET /api/assets` (payload attuale usato da Oggi):

| Campo | In endpoint attuale? | Dove vive se no / costo |
|---|---|---|
| Nome attuale | **Sì** (`AssetOut.name`) — Oggi **non lo mostra** | `assets.name` |
| Nome proposto | **Sì** (`proposals[].value`) | `name_proposals.value` |
| MAC | **Sì** (`macs[]`) | `interfaces.mac` (già joined) |
| IP corrente | **Sì** (`ips[]`, `ip_bindings`) | `ip_addresses` via interface |
| Porta switch | **Sì** (`port`, `port_label`, `patch`) | meta/path già in serialize list |
| AP WiFi | **Parziale** (`link.ap_*` se presente) | enrich pieno solo con `with_path=True` — oggi list **senza**; costo: join/path per asset o flag query |
| Presenza | **Sì** (`presence_state`, `portal_last_seen`) | già in AssetOut |
| Fonte | **Sì** (`proposals[].source`) | `name_proposals.source` |
| Confidenza | **Sì** (`proposals[].confidence`) | `name_proposals.confidence` |
| Collisioni (N asset con stesso proposto) | **No** | **campo mancante**: conteggio client su lista assets **O** endpoint dedicato `GROUP BY`; costo O(n) in-memory sulla stessa fetch (già caricata) — **zero join** se calcolato in UI/API wrapper |

Conclusione: per la griglia **quasi tutto è già nel JSON**; manca solo **collisioni** (derivabile) e AP affidabile senza `with_path`. Il problema Oggi è di **presentazione**, non di assenza dati base.

---

## A3 — Specificità (bozza regole, non codice)

### Pattern osservati (coda + inventario)

| Classe | Esempi reali |
|---|---|
| Hostname parlanti / modello | `AmazonAQM-008G`, `ROMO-A3021K`, `Loewe-bild-7.77`, `roborock-vacuum-a70`, `Fritz-Cucina` |
| Nomi umani curati | `Echo Cabina Armadio`, `Sky Q principale — Ethernet`, `Cassiopea — NIC 1`, `BMS Honeywell — Boschetti` |
| Brand / tipo generico (OUI) | `Sky`, `Amazon`, `BTicino`, `TP-Link`, `Gaggenau`, `Raspberry Pi`, `Switch Linksys`, `Unknown` |
| Sintetici | `PC-68-13-F3-E7-D2-B2`, `amazon-5b5bf3c111c404ae`, `PC 108`, `PC-192-168-2-*` (nuovi) |
| AI misto | `Echo Cucina`, `Echo Sala`, `Echo Media`, `PC CabinaArmadio`, `Gateway AVM` |

### Tabella criteri di specificità (bozza ordinabile, alto → basso)

| Rank | Criterio | 10 esempi classati dal dump |
|---|---|---|
| 5 | Nome+modello / hostname parlante univoco | `ROMO-A3021K` ← Robot DJI ROMO; `AmazonAQM-008G` ← AQM 2; `Loewe-bild-7.77` ← Loewe bild 7.77; `roborock-vacuum-a70` |
| 4 | Nome umano con stanza/ruolo | `Echo Cabina Armadio`, `SkyBooster2 BIBLIO — mesh`, `Cassiopea — NIC 1` |
| 3 | Tipo+brand non univoco | `Raspberry Pi` (4 in coda), `Switch Linksys` (3), `BMS Honeywell` (2), `Echo Amazon` (2) |
| 2 | Brand nudo / generico | `Sky` (8 in coda), `Amazon` (6), `BTicino`, `TP-Link`, `Gaggenau` |
| 1 | Sintetico / Unknown | `amazon-5b5bf3c…` su Echo Cucina; `PC-68-13-…`; `Unknown` su Echo Bagno; `PC` su ROCK |

**Regola «meno specifica = rumore» (euristica A1):** score(proposto) < score(attuale) → **26/65** filtrate. Esempi: `Sky Q principale — Ethernet`→`Sky`; `Echo Biblioteca`→`Amazon`; `AppleTV-5`→`Dispositivo Apple`; `BTicino F454`→`BTicino`.

### Casi ambigui (non risolti)

1. `Allsky 3` / `allsky3` / `Openhab Pi` / `ropieee` → tutti `Raspberry Pi` (OUI): upgrade o downgrade di specificità?
2. `Amazon Air Quality Monitor` → AI `Echo Cucina` (0.93): collisiona con asset 55 già `Echo Cucina`.
3. `Cassiopea — NIC 1/2` → `Cassiopea (ASUSTOR)`: più «prodotto», meno «ruolo NIC» — rename asset-level vs chassis.
4. `Echo — Cucina` → `Echo Amazon` vs `Echo Cucina` → `amazon-<hex>`: direzioni opposte.
5. `LGS328C` → `Switch` (dns 0.6) vs `LGS310C` → `Switch Linksys`: stessa famiglia, confidenze diverse.
6. `Robot Roborock` (nome) ↔ proposta `roborock-vacuum-a70` e inversa `#15 Roborock`→`Robot Roborock`.
7. Asset `#82` nome `Sky` → AI `PC CabinaArmadio`: upgrade da generico, ma rischio falso positivo.

---

## A4 — Collisioni

### In coda (stesso `nome_proposto`)

| Proposto | Righe in coda |
|---|---|
| Sky | **8** |
| Amazon | **6** |
| Raspberry Pi | **4** |
| Switch Linksys / BTicino | **3** ciascuno |
| BMS Honeywell, Cassiopea (ASUSTOR), Echo Amazon, Gaggenau, TP-Link, Unknown | **2** |

### Inventario: asset che **hanno già** quel nome (norm)

| Proposto | Asset con nome esatto/norm | IDs |
|---|---|---|
| **Sky** | **5** | 43, 58, 61, 82, 88 |
| LGwebOSTV | 2 | 74, 75 |
| Amazon | 1 | 53 |
| Echo Cucina | 1 | 55 |
| Robot Roborock | 1 | 36 |

Adottare «Sky» su un altro asset **aumenta** la collisione (già 5 omonimi).

---

## A5 — Vincoli esistenti

### Accetta proposta (Oggi `[adotta]`)

- UI: `api.adoptName(assetId, source)` — `Oggi.vue:124–133`
- API: `POST /api/assets/{id}/adopt-name?source=…` — `assets.py:692–755`
- Effetti:
  - `assets.name = proposal.value`
  - proposal `status=archived`
  - `meta.manual_overrides` += `name`
  - `meta.field_sources.name` = `manual (proposta {source})` conf 1.0
  - se `status==nuovo` → `noto`
  - se source=ai: Suggestion rename → approved
  - **nessuna scrittura su tabella chassis / member labels**

### Rifiuta / ignora (Oggi `[ignora]` su proposta o nuovo)

- `PATCH /api/assets/{id}` `{status:"ignorato"}` — **non** archivia la NameProposal; nasconde l’asset dalla coda (filtro status). Debito UX: proposta pending resta nel DB.

### Monitor

- `POST /api/monitors/{id}/silences` — silenzia flapping; non tocca nomi.

### Debito noto: nome sul chassis vs asset

- Spec **025 §** «Il nome vive sul chassis» (`obs-design-spec-025.md:395–397`): rename Dossier dovrebbe scrivere sul chassis.
- Oggi **adopt-name** scrive solo `assets.name`.
- **Incrocio cantiere Oggi:** un’azione di massa «adotta» su radio Sky / NIC Cassiopea rinomina **asset singoli**, non il device fisico chassis → omonimi moltiplicati, sibling non allineati. Solo segnalazione; fix fuori FASE A.

---

## STOP

FASE A chiusa. Design griglia + regole verdetto → **review**, poi FASE B su diff.
Nessun bump VERSION, nessun deploy.

---

## Appendice — dump JSON live

```json
{
  "ts": "2026-07-23T21:18:48.307953+00:00",
  "counts": {
    "proposte_nome": 65,
    "proposte_rumore_meno_specifiche": 26,
    "device_nuovi_status_nuovo": 45,
    "monitor_degradati": 3,
    "totale_coda_approx": 113
  },
  "nota_nuovi": "device_nuovi_status_nuovo=45 conta status=nuovo grezzo; Oggi UI usa isNuovoDaConoscere (portal≤24h + anti-U/L) → sottoinsieme",
  "proposte_nome": [
    {
      "kind": "proposta_nome",
      "asset_id": 98,
      "mac": "68:13:F3:E7:D2:B2",
      "macs": [
        "68:13:F3:E7:D2:B2"
      ],
      "ip": "192.168.2.88",
      "ips": [
        "192.168.2.88"
      ],
      "nome_attuale": null,
      "nome_proposto": "PC-68-13-F3-E7-D2-B2",
      "fonte": "dns",
      "fonte_label": "DNS",
      "confidenza": 0.6,
      "confidenza_pct": 60,
      "updated_at": "2026-07-18T01:26:08.657373Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "nuovo",
      "less_specific_noise": false,
      "score_attuale": 0,
      "score_proposto": 20,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 108,
      "mac": "D6:A9:77:61:25:17",
      "macs": [
        "D6:A9:77:61:25:17"
      ],
      "ip": "192.168.2.195",
      "ips": [
        "192.168.2.195"
      ],
      "nome_attuale": null,
      "nome_proposto": "PC 108",
      "fonte": "ai",
      "fonte_label": "AI",
      "confidenza": 0.62,
      "confidenza_pct": 62,
      "updated_at": "2026-07-20T14:42:28.763421Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "nuovo",
      "less_specific_noise": false,
      "score_attuale": 0,
      "score_proposto": 40,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 135,
      "mac": "D4:52:EE:C3:25:16",
      "macs": [
        "D4:52:EE:C3:25:16"
      ],
      "ip": null,
      "ips": [],
      "nome_attuale": null,
      "nome_proposto": "Sky",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-20T03:02:07.333175Z",
      "presence_state": "present",
      "port": "310c:5",
      "port_label": "LGS310C · porta 5",
      "status": "nuovo",
      "less_specific_noise": false,
      "score_attuale": 0,
      "score_proposto": 10,
      "collisioni_stesso_proposto": 8
    },
    {
      "kind": "proposta_nome",
      "asset_id": 136,
      "mac": "38:A6:CE:3E:9C:A8",
      "macs": [
        "38:A6:CE:3E:9C:A8"
      ],
      "ip": null,
      "ips": [],
      "nome_attuale": null,
      "nome_proposto": "Sky",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-20T03:18:07.546180Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "nuovo",
      "less_specific_noise": false,
      "score_attuale": 0,
      "score_proposto": 10,
      "collisioni_stesso_proposto": 8
    },
    {
      "kind": "proposta_nome",
      "asset_id": 137,
      "mac": "38:A6:CE:79:D4:FE",
      "macs": [
        "38:A6:CE:79:D4:FE"
      ],
      "ip": null,
      "ips": [],
      "nome_attuale": null,
      "nome_proposto": "Sky",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-20T06:19:09.608809Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "nuovo",
      "less_specific_noise": false,
      "score_attuale": 0,
      "score_proposto": 10,
      "collisioni_stesso_proposto": 8
    },
    {
      "kind": "proposta_nome",
      "asset_id": 147,
      "mac": "D8:EC:5E:CC:1C:05",
      "macs": [
        "D8:EC:5E:CC:1C:05"
      ],
      "ip": null,
      "ips": [],
      "nome_attuale": null,
      "nome_proposto": "Switch Linksys",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-21T08:32:21.671817Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "nuovo",
      "less_specific_noise": false,
      "score_attuale": 0,
      "score_proposto": 55,
      "collisioni_stesso_proposto": 3
    },
    {
      "kind": "proposta_nome",
      "asset_id": 149,
      "mac": "38:A6:CE:3E:9C:AB",
      "macs": [
        "38:A6:CE:3E:9C:AB"
      ],
      "ip": null,
      "ips": [],
      "nome_attuale": null,
      "nome_proposto": "Sky",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-22T03:19:26.893944Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "nuovo",
      "less_specific_noise": false,
      "score_attuale": 0,
      "score_proposto": 10,
      "collisioni_stesso_proposto": 8
    },
    {
      "kind": "proposta_nome",
      "asset_id": 151,
      "mac": "D8:EC:5E:CC:1C:08",
      "macs": [
        "D8:EC:5E:CC:1C:08"
      ],
      "ip": null,
      "ips": [],
      "nome_attuale": null,
      "nome_proposto": "Switch Linksys",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-23T01:47:50.965438Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "nuovo",
      "less_specific_noise": false,
      "score_attuale": 0,
      "score_proposto": 55,
      "collisioni_stesso_proposto": 3
    },
    {
      "kind": "proposta_nome",
      "asset_id": 30,
      "mac": "DC:A6:32:9C:A7:63",
      "macs": [
        "DC:A6:32:9C:A7:63"
      ],
      "ip": "192.168.1.117",
      "ips": [
        "192.168.1.117"
      ],
      "nome_attuale": "Allsky 3",
      "nome_proposto": "Raspberry Pi",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.835339Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 40,
      "score_proposto": 55,
      "collisioni_stesso_proposto": 4
    },
    {
      "kind": "proposta_nome",
      "asset_id": 48,
      "mac": "A4:02:B7:66:80:0F",
      "macs": [
        "A4:02:B7:66:80:0F"
      ],
      "ip": "192.168.2.117",
      "ips": [
        "192.168.2.117"
      ],
      "nome_attuale": "Amazon Air Quality Monitor",
      "nome_proposto": "Echo Cucina",
      "fonte": "ai",
      "fonte_label": "AI",
      "confidenza": 0.93,
      "confidenza_pct": 93,
      "updated_at": "2026-07-20T14:32:28.712785Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 55,
      "score_proposto": 60,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 64,
      "mac": "54:2B:1C:6B:AD:2D",
      "macs": [
        "54:2B:1C:6B:AD:2D"
      ],
      "ip": "192.168.3.45",
      "ips": [
        "192.168.3.45"
      ],
      "nome_attuale": "Amazon Air Quality Monitor 2",
      "nome_proposto": "AmazonAQM-008G",
      "fonte": "dhcp",
      "fonte_label": "DHCP",
      "confidenza": 0.92,
      "confidenza_pct": 92,
      "updated_at": "2026-07-23T16:31:44.594557Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 55,
      "score_proposto": 80,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 32,
      "mac": "8C:BF:EA:34:90:2C",
      "macs": [
        "8C:BF:EA:34:90:2C"
      ],
      "ip": "192.168.2.62",
      "ips": [
        "192.168.2.62"
      ],
      "nome_attuale": "Amazon Plug",
      "nome_proposto": "Sensore o presa IoT (chip ESP)",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.835345Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 55,
      "score_proposto": 55,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 70,
      "mac": "58:55:CA:3E:9E:D4",
      "macs": [
        "58:55:CA:3E:9E:D4"
      ],
      "ip": "192.168.2.193",
      "ips": [
        "192.168.2.193"
      ],
      "nome_attuale": "AppleTV-5",
      "nome_proposto": "Dispositivo Apple",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:06:57.985894Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 80,
      "score_proposto": 60,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 59,
      "mac": "68:7F:F0:17:70:AD",
      "macs": [
        "68:7F:F0:17:70:AD"
      ],
      "ip": "192.168.2.203",
      "ips": [
        "192.168.2.203"
      ],
      "nome_attuale": "ArcherBE3600",
      "nome_proposto": "TP-Link",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.837012Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 55,
      "score_proposto": 40,
      "collisioni_stesso_proposto": 2
    },
    {
      "kind": "proposta_nome",
      "asset_id": 26,
      "mac": "00:30:AF:20:E9:64",
      "macs": [
        "00:30:AF:20:E9:64"
      ],
      "ip": "192.168.1.45",
      "ips": [
        "192.168.1.45"
      ],
      "nome_attuale": "BMS Honeywell — Boschetti",
      "nome_proposto": "BMS Honeywell",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.835325Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 55,
      "score_proposto": 55,
      "collisioni_stesso_proposto": 2
    },
    {
      "kind": "proposta_nome",
      "asset_id": 27,
      "mac": "00:30:AF:20:DC:16",
      "macs": [
        "00:30:AF:20:DC:16"
      ],
      "ip": "192.168.1.46",
      "ips": [
        "192.168.1.46"
      ],
      "nome_attuale": "BMS Honeywell — Sant'Agostino",
      "nome_proposto": "BMS Honeywell",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.835328Z",
      "presence_state": "present",
      "port": "328c:3",
      "port_label": "LGS328C · porta 3",
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 55,
      "score_proposto": 55,
      "collisioni_stesso_proposto": 2
    },
    {
      "kind": "proposta_nome",
      "asset_id": 25,
      "mac": "00:03:50:8F:10:38",
      "macs": [
        "00:03:50:8F:10:38"
      ],
      "ip": "192.168.1.35",
      "ips": [
        "192.168.1.35"
      ],
      "nome_attuale": "BTicino F454",
      "nome_proposto": "BTicino",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.835321Z",
      "presence_state": "present",
      "port": "328c:2",
      "port_label": "LGS328C · porta 2",
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 55,
      "score_proposto": 40,
      "collisioni_stesso_proposto": 3
    },
    {
      "kind": "proposta_nome",
      "asset_id": 5,
      "mac": "24:4B:FE:84:6A:01",
      "macs": [
        "24:4B:FE:84:6A:01"
      ],
      "ip": "192.168.1.3",
      "ips": [
        "192.168.1.3"
      ],
      "nome_attuale": "Cassiopea — NIC 1",
      "nome_proposto": "Cassiopea (ASUSTOR)",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.838340Z",
      "presence_state": "present",
      "port": "328c:8",
      "port_label": "LGS328C · porta 8",
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 55,
      "score_proposto": 60,
      "collisioni_stesso_proposto": 2
    },
    {
      "kind": "proposta_nome",
      "asset_id": 6,
      "mac": "24:4B:FE:84:6A:02",
      "macs": [
        "24:4B:FE:84:6A:02"
      ],
      "ip": "192.168.3.24",
      "ips": [
        "192.168.3.24"
      ],
      "nome_attuale": "Cassiopea — NIC 2",
      "nome_proposto": "Cassiopea (ASUSTOR)",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.838348Z",
      "presence_state": "present",
      "port": "328c:22",
      "port_label": "LGS328C · porta 22",
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 55,
      "score_proposto": 60,
      "collisioni_stesso_proposto": 2
    },
    {
      "kind": "proposta_nome",
      "asset_id": 14,
      "mac": "00:03:50:96:82:2C",
      "macs": [
        "00:03:50:96:82:2C"
      ],
      "ip": "192.168.2.68",
      "ips": [
        "192.168.2.68"
      ],
      "nome_attuale": "Citofono BTicino C3X",
      "nome_proposto": "BTicino",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.835287Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 55,
      "score_proposto": 40,
      "collisioni_stesso_proposto": 3
    },
    {
      "kind": "proposta_nome",
      "asset_id": 12,
      "mac": "C0:56:E3:5E:48:5F",
      "macs": [
        "C0:56:E3:5E:48:5F"
      ],
      "ip": "192.168.1.250",
      "ips": [
        "192.168.1.250"
      ],
      "nome_attuale": "DVR Hikvision",
      "nome_proposto": "Telecamera Hikvision",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.835280Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 55,
      "score_proposto": 55,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 67,
      "mac": "50:99:5A:8A:2B:9B",
      "macs": [
        "50:99:5A:8A:2B:9B"
      ],
      "ip": "192.168.3.49",
      "ips": [
        "192.168.3.49"
      ],
      "nome_attuale": "Echo Bagno Etnico",
      "nome_proposto": "Unknown",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.7,
      "confidenza_pct": 70,
      "updated_at": "2026-07-22T15:08:00.959784Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 60,
      "score_proposto": 10,
      "collisioni_stesso_proposto": 2
    },
    {
      "kind": "proposta_nome",
      "asset_id": 66,
      "mac": "44:00:49:72:F4:93",
      "macs": [
        "44:00:49:72:F4:93"
      ],
      "ip": "192.168.3.47",
      "ips": [
        "192.168.3.47"
      ],
      "nome_attuale": "Echo Bagno Padronale",
      "nome_proposto": "Amazon",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.837035Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 60,
      "score_proposto": 10,
      "collisioni_stesso_proposto": 6
    },
    {
      "kind": "proposta_nome",
      "asset_id": 57,
      "mac": "F4:03:2A:5D:4D:9E",
      "macs": [
        "F4:03:2A:5D:4D:9E"
      ],
      "ip": "192.168.2.189",
      "ips": [
        "192.168.2.189"
      ],
      "nome_attuale": "Echo Biblioteca",
      "nome_proposto": "Amazon",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.837005Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 60,
      "score_proposto": 10,
      "collisioni_stesso_proposto": 6
    },
    {
      "kind": "proposta_nome",
      "asset_id": 62,
      "mac": "1C:12:B0:B4:57:A9",
      "macs": [
        "1C:12:B0:B4:57:A9"
      ],
      "ip": "192.168.3.32",
      "ips": [
        "192.168.3.32"
      ],
      "nome_attuale": "Echo Cabina Armadio",
      "nome_proposto": "Amazon",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.837022Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 60,
      "score_proposto": 10,
      "collisioni_stesso_proposto": 6
    },
    {
      "kind": "proposta_nome",
      "asset_id": 35,
      "mac": "6C:99:9D:08:8E:1D",
      "macs": [
        "6C:99:9D:08:8E:1D"
      ],
      "ip": "192.168.2.76",
      "ips": [
        "192.168.2.76"
      ],
      "nome_attuale": "Echo Camera Beatrice",
      "nome_proposto": "Amazon",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.836936Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 60,
      "score_proposto": 10,
      "collisioni_stesso_proposto": 6
    },
    {
      "kind": "proposta_nome",
      "asset_id": 63,
      "mac": "08:C2:24:DC:54:8B",
      "macs": [
        "08:C2:24:DC:54:8B"
      ],
      "ip": "192.168.3.38",
      "ips": [
        "192.168.3.38"
      ],
      "nome_attuale": "Echo Camera Ospiti",
      "nome_proposto": "Amazon",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.7,
      "confidenza_pct": 70,
      "updated_at": "2026-07-17T23:40:43.837025Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 60,
      "score_proposto": 10,
      "collisioni_stesso_proposto": 6
    },
    {
      "kind": "proposta_nome",
      "asset_id": 55,
      "mac": "40:89:C6:B6:2F:6C",
      "macs": [
        "40:89:C6:B6:2F:6C"
      ],
      "ip": "192.168.2.176",
      "ips": [
        "192.168.2.176"
      ],
      "nome_attuale": "Echo Cucina",
      "nome_proposto": "amazon-5b5bf3c111c404ae",
      "fonte": "dns",
      "fonte_label": "DNS",
      "confidenza": 0.6,
      "confidenza_pct": 60,
      "updated_at": "2026-07-18T01:26:08.971444Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 60,
      "score_proposto": 20,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 56,
      "mac": "50:99:5A:6E:EA:37",
      "macs": [
        "50:99:5A:6E:EA:37"
      ],
      "ip": "192.168.2.186",
      "ips": [
        "192.168.2.186"
      ],
      "nome_attuale": "Echo Lavanderia",
      "nome_proposto": "Unknown",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.7,
      "confidenza_pct": 70,
      "updated_at": "2026-07-22T15:08:00.959784Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 60,
      "score_proposto": 10,
      "collisioni_stesso_proposto": 2
    },
    {
      "kind": "proposta_nome",
      "asset_id": 39,
      "mac": "CC:9E:A2:8F:9C:E2",
      "macs": [
        "CC:9E:A2:8F:9C:E2"
      ],
      "ip": "192.168.2.93",
      "ips": [
        "192.168.2.93"
      ],
      "nome_attuale": "Echo Sala TV",
      "nome_proposto": "Echo Sala",
      "fonte": "ai",
      "fonte_label": "AI",
      "confidenza": 0.92,
      "confidenza_pct": 92,
      "updated_at": "2026-07-20T14:32:30.076167Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 60,
      "score_proposto": 60,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 33,
      "mac": "08:A6:BC:B2:F6:A8",
      "macs": [
        "08:A6:BC:B2:F6:A8"
      ],
      "ip": "192.168.2.70",
      "ips": [
        "192.168.2.70"
      ],
      "nome_attuale": "Echo Salone",
      "nome_proposto": "Echo Media",
      "fonte": "ai",
      "fonte_label": "AI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-20T14:31:19.156212Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 60,
      "score_proposto": 60,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 52,
      "mac": "18:0B:1B:03:60:D0",
      "macs": [
        "18:0B:1B:03:60:D0"
      ],
      "ip": "192.168.2.148",
      "ips": [
        "192.168.2.148"
      ],
      "nome_attuale": "Echo Salottino",
      "nome_proposto": "Amazon",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.836990Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 60,
      "score_proposto": 10,
      "collisioni_stesso_proposto": 6
    },
    {
      "kind": "proposta_nome",
      "asset_id": 17,
      "mac": "7C:2C:67:2B:24:18",
      "macs": [
        "7C:2C:67:2B:24:18"
      ],
      "ip": "192.168.3.5",
      "ips": [
        "192.168.3.5"
      ],
      "nome_attuale": "Echo — Cucina",
      "nome_proposto": "Echo Amazon",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.835294Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 60,
      "score_proposto": 60,
      "collisioni_stesso_proposto": 2
    },
    {
      "kind": "proposta_nome",
      "asset_id": 18,
      "mac": "7C:2C:67:2B:43:30",
      "macs": [
        "7C:2C:67:2B:43:30"
      ],
      "ip": "192.168.2.190",
      "ips": [
        "192.168.2.190"
      ],
      "nome_attuale": "Echo — SalaPC",
      "nome_proposto": "Echo Amazon",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.835297Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 60,
      "score_proposto": 60,
      "collisioni_stesso_proposto": 2
    },
    {
      "kind": "proposta_nome",
      "asset_id": 1,
      "mac": "60:B5:8D:6C:6D:53",
      "macs": [
        "60:B5:8D:6C:6D:53"
      ],
      "ip": "192.168.1.1",
      "ips": [
        "192.168.1.1"
      ],
      "nome_attuale": "FRITZ!Box 5690 Pro",
      "nome_proposto": "FRITZ!Box",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.835255Z",
      "presence_state": "present",
      "port": "328c:1",
      "port_label": "LGS328C · porta 1",
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 80,
      "score_proposto": 60,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 7,
      "mac": "F0:B0:14:90:87:96",
      "macs": [
        "F0:B0:14:90:87:96",
        "F0:B0:14:90:87:97"
      ],
      "ip": null,
      "ips": [],
      "nome_attuale": "FRITZ!Powerline 510E",
      "nome_proposto": "FRITZ!Powerline",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.838354Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 80,
      "score_proposto": 60,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 24,
      "mac": "DA:24:DD:97:0B:DF",
      "macs": [
        "DA:24:DD:97:0B:DF"
      ],
      "ip": "192.168.1.13",
      "ips": [
        "192.168.1.13"
      ],
      "nome_attuale": "FRITZ!Repeater CabinaArmadio",
      "nome_proposto": "Fritz-CabinaArmadio",
      "fonte": "dns",
      "fonte_label": "DNS",
      "confidenza": 0.6,
      "confidenza_pct": 60,
      "updated_at": "2026-07-18T00:14:21.028753Z",
      "presence_state": "present",
      "port": "328c:9",
      "port_label": "LGS328C · porta 9",
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 60,
      "score_proposto": 80,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 22,
      "mac": "DA:24:DD:19:7A:D3",
      "macs": [
        "DA:24:DD:19:7A:D3"
      ],
      "ip": "192.168.1.11",
      "ips": [
        "192.168.1.11"
      ],
      "nome_attuale": "FRITZ!Repeater Cucina",
      "nome_proposto": "Fritz-Cucina",
      "fonte": "dns",
      "fonte_label": "DNS",
      "confidenza": 0.6,
      "confidenza_pct": 60,
      "updated_at": "2026-07-18T00:14:21.028760Z",
      "presence_state": "present",
      "port": "328c:16",
      "port_label": "LGS328C · porta 16",
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 60,
      "score_proposto": 80,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 21,
      "mac": "DA:24:DD:18:75:E2",
      "macs": [
        "DA:24:DD:18:75:E2"
      ],
      "ip": "192.168.1.10",
      "ips": [
        "192.168.1.10"
      ],
      "nome_attuale": "FRITZ!Repeater SalaPC",
      "nome_proposto": "Fritz-SalaPC",
      "fonte": "dns",
      "fonte_label": "DNS",
      "confidenza": 0.6,
      "confidenza_pct": 60,
      "updated_at": "2026-07-18T00:14:21.028772Z",
      "presence_state": "present",
      "port": "310c:2",
      "port_label": "LGS310C · porta 2",
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 60,
      "score_proposto": 80,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 23,
      "mac": "DA:24:DD:18:C4:D3",
      "macs": [
        "DA:24:DD:18:C4:D3"
      ],
      "ip": "192.168.1.12",
      "ips": [
        "192.168.1.12"
      ],
      "nome_attuale": "FRITZ!Repeater SalettaTV",
      "nome_proposto": "Fritz-SalettaTV",
      "fonte": "dns",
      "fonte_label": "DNS",
      "confidenza": 0.6,
      "confidenza_pct": 60,
      "updated_at": "2026-07-18T00:14:21.028779Z",
      "presence_state": "present",
      "port": "328c:6",
      "port_label": "LGS328C · porta 6",
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 60,
      "score_proposto": 80,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 112,
      "mac": "DC:15:C8:80:BB:EA",
      "macs": [
        "DC:15:C8:80:BB:EA"
      ],
      "ip": null,
      "ips": [],
      "nome_attuale": "FritzBox Router",
      "nome_proposto": "Gateway AVM",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-18T01:26:08.824984Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 60,
      "score_proposto": 55,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 4,
      "mac": "54:07:7D:1E:4F:B9",
      "macs": [
        "54:07:7D:1E:4F:B9"
      ],
      "ip": "192.168.1.8",
      "ips": [
        "192.168.1.8"
      ],
      "nome_attuale": "GS308EP",
      "nome_proposto": "Switch Netgear",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.835270Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 40,
      "score_proposto": 55,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 49,
      "mac": "E0:D3:62:ED:BE:9D",
      "macs": [
        "E0:D3:62:ED:BE:9D"
      ],
      "ip": "192.168.2.124",
      "ips": [
        "192.168.2.124"
      ],
      "nome_attuale": "Hub Tapo H100",
      "nome_proposto": "TP-Link",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.836980Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 55,
      "score_proposto": 40,
      "collisioni_stesso_proposto": 2
    },
    {
      "kind": "proposta_nome",
      "asset_id": 28,
      "mac": "A8:5E:45:12:3A:26",
      "macs": [
        "A8:5E:45:12:3A:26"
      ],
      "ip": "192.168.1.44",
      "ips": [
        "192.168.1.44"
      ],
      "nome_attuale": "Kraken",
      "nome_proposto": "Apparato ASUS",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.835332Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 40,
      "score_proposto": 55,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 3,
      "mac": "D8:EC:5E:C5:7E:C7",
      "macs": [
        "D8:EC:5E:C5:7E:C7",
        "D8:EC:5E:C5:7E:CF"
      ],
      "ip": "192.168.1.7",
      "ips": [
        "192.168.1.7"
      ],
      "nome_attuale": "LGS310C",
      "nome_proposto": "Switch Linksys",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.835266Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 40,
      "score_proposto": 55,
      "collisioni_stesso_proposto": 3
    },
    {
      "kind": "proposta_nome",
      "asset_id": 2,
      "mac": "C8:54:4B:F4:71:D5",
      "macs": [
        "C8:54:4B:F4:71:D5",
        "D8:EC:5E:CC:1B:FF"
      ],
      "ip": "192.168.1.2",
      "ips": [
        "192.168.1.2",
        "192.168.1.2"
      ],
      "nome_attuale": "LGS328C",
      "nome_proposto": "Switch",
      "fonte": "dns",
      "fonte_label": "DNS",
      "confidenza": 0.6,
      "confidenza_pct": 60,
      "updated_at": "2026-07-20T01:08:20.422800Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 40,
      "score_proposto": 40,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 37,
      "mac": "68:A4:0E:40:A6:9A",
      "macs": [
        "68:A4:0E:40:A6:9A"
      ],
      "ip": "192.168.2.81",
      "ips": [
        "192.168.2.81"
      ],
      "nome_attuale": "Lavastoviglie Gaggenau",
      "nome_proposto": "Gaggenau",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.836946Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 55,
      "score_proposto": 40,
      "collisioni_stesso_proposto": 2
    },
    {
      "kind": "proposta_nome",
      "asset_id": 42,
      "mac": "70:C9:4E:83:D7:DC",
      "macs": [
        "70:C9:4E:83:D7:DC"
      ],
      "ip": "192.168.2.99",
      "ips": [
        "192.168.2.99"
      ],
      "nome_attuale": "Loewe bild 7.77",
      "nome_proposto": "Loewe-bild-7.77",
      "fonte": "dhcp",
      "fonte_label": "DHCP",
      "confidenza": 0.92,
      "confidenza_pct": 92,
      "updated_at": "2026-07-23T16:31:44.594522Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 80,
      "score_proposto": 80,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 19,
      "mac": "E4:5F:01:2F:3F:05",
      "macs": [
        "E4:5F:01:2F:3F:05"
      ],
      "ip": "192.168.1.20",
      "ips": [
        "192.168.1.20"
      ],
      "nome_attuale": "Openhab Pi",
      "nome_proposto": "Raspberry Pi",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.835301Z",
      "presence_state": "present",
      "port": "328c:17",
      "port_label": "LGS328C · porta 17",
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 55,
      "score_proposto": 55,
      "collisioni_stesso_proposto": 4
    },
    {
      "kind": "proposta_nome",
      "asset_id": 34,
      "mac": "4C:24:CE:51:70:AE",
      "macs": [
        "4C:24:CE:51:70:AE"
      ],
      "ip": "192.168.2.74",
      "ips": [
        "192.168.2.74"
      ],
      "nome_attuale": "Petkit - Distributore Cibo Gatto",
      "nome_proposto": "Presa o sensore Wi-Fi",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.836302Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 70,
      "score_proposto": 70,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 13,
      "mac": "00:17:88:A8:89:EC",
      "macs": [
        "00:17:88:A8:89:EC"
      ],
      "ip": "192.168.2.109",
      "ips": [
        "192.168.2.109"
      ],
      "nome_attuale": "Philips Hue Bridge",
      "nome_proposto": "Philips Hue",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.835283Z",
      "presence_state": "present",
      "port": "310c:4",
      "port_label": "LGS310C · porta 4",
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 55,
      "score_proposto": 55,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 38,
      "mac": "68:A4:0E:87:2A:7D",
      "macs": [
        "68:A4:0E:87:2A:7D"
      ],
      "ip": "192.168.2.82",
      "ips": [
        "192.168.2.82"
      ],
      "nome_attuale": "Piano Induzione Gaggenau",
      "nome_proposto": "Gaggenau",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.836949Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 55,
      "score_proposto": 40,
      "collisioni_stesso_proposto": 2
    },
    {
      "kind": "proposta_nome",
      "asset_id": 50,
      "mac": "1C:69:7A:A6:FA:47",
      "macs": [
        "1C:69:7A:A6:FA:47"
      ],
      "ip": "192.168.2.126",
      "ips": [
        "192.168.2.126"
      ],
      "nome_attuale": "ROCK",
      "nome_proposto": "PC",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.836983Z",
      "presence_state": "present",
      "port": "328c:15",
      "port_label": "LGS328C · porta 15",
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 15,
      "score_proposto": 10,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 15,
      "mac": "B0:4A:39:XX:XX:XX",
      "macs": [
        "B0:4A:39:XX:XX:XX"
      ],
      "ip": null,
      "ips": [],
      "nome_attuale": "Roborock",
      "nome_proposto": "Robot Roborock",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.838374Z",
      "presence_state": "unknown",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 40,
      "score_proposto": 55,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 68,
      "mac": "0C:9A:E6:B4:D6:E8",
      "macs": [
        "0C:9A:E6:B4:D6:E8"
      ],
      "ip": "192.168.2.94",
      "ips": [
        "192.168.2.94"
      ],
      "nome_attuale": "Robot DJI ROMO",
      "nome_proposto": "ROMO-A3021K",
      "fonte": "dhcp",
      "fonte_label": "DHCP",
      "confidenza": 0.92,
      "confidenza_pct": 92,
      "updated_at": "2026-07-23T16:31:44.594491Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 60,
      "score_proposto": 80,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 36,
      "mac": "B0:4A:39:92:49:57",
      "macs": [
        "B0:4A:39:92:49:57"
      ],
      "ip": "192.168.2.80",
      "ips": [
        "192.168.2.80"
      ],
      "nome_attuale": "Robot Roborock",
      "nome_proposto": "roborock-vacuum-a70",
      "fonte": "dhcp",
      "fonte_label": "DHCP",
      "confidenza": 0.92,
      "confidenza_pct": 92,
      "updated_at": "2026-07-23T16:31:44.594471Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 55,
      "score_proposto": 70,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 82,
      "mac": "38:A6:CE:40:A7:72",
      "macs": [
        "38:A6:CE:40:A7:72",
        "38:A6:CE:40:A7:76"
      ],
      "ip": "192.168.2.120",
      "ips": [
        "192.168.2.120"
      ],
      "nome_attuale": "Sky",
      "nome_proposto": "PC CabinaArmadio",
      "fonte": "ai",
      "fonte_label": "AI",
      "confidenza": 0.88,
      "confidenza_pct": 88,
      "updated_at": "2026-07-20T14:48:52.499200Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 10,
      "score_proposto": 55,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 8,
      "mac": "70:50:AF:FB:86:F8",
      "macs": [
        "70:50:AF:FB:86:F8",
        "70:50:AF:FB:86:FA"
      ],
      "ip": null,
      "ips": [],
      "nome_attuale": "Sky Q principale — Ethernet",
      "nome_proposto": "Sky",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.838361Z",
      "presence_state": "present",
      "port": "328c:12",
      "port_label": "LGS328C · porta 12",
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 55,
      "score_proposto": 10,
      "collisioni_stesso_proposto": 8
    },
    {
      "kind": "proposta_nome",
      "asset_id": 9,
      "mac": "70:50:AF:FB:86:F9",
      "macs": [
        "70:50:AF:FB:86:F9"
      ],
      "ip": "192.168.2.107",
      "ips": [
        "192.168.2.107"
      ],
      "nome_attuale": "SkyBooster1 TECNICO — mesh",
      "nome_proposto": "Sky",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.835273Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 55,
      "score_proposto": 10,
      "collisioni_stesso_proposto": 8
    },
    {
      "kind": "proposta_nome",
      "asset_id": 10,
      "mac": "70:50:AF:FC:0A:F8",
      "macs": [
        "70:50:AF:FC:0A:F8"
      ],
      "ip": null,
      "ips": [],
      "nome_attuale": "SkyBooster2 BIBLIO — Ethernet",
      "nome_proposto": "Sky",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.838367Z",
      "presence_state": "present",
      "port": "328c:14",
      "port_label": "LGS328C · porta 14",
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 55,
      "score_proposto": 10,
      "collisioni_stesso_proposto": 8
    },
    {
      "kind": "proposta_nome",
      "asset_id": 11,
      "mac": "70:50:AF:FC:0A:F9",
      "macs": [
        "70:50:AF:FC:0A:F9"
      ],
      "ip": "192.168.2.108",
      "ips": [
        "192.168.2.108"
      ],
      "nome_attuale": "SkyBooster2 BIBLIO — mesh",
      "nome_proposto": "Sky",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.835276Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 55,
      "score_proposto": 10,
      "collisioni_stesso_proposto": 8
    },
    {
      "kind": "proposta_nome",
      "asset_id": 76,
      "mac": "64:CB:E9:B5:37:26",
      "macs": [
        "64:CB:E9:B5:37:26"
      ],
      "ip": "192.168.2.128",
      "ips": [
        "192.168.2.128"
      ],
      "nome_attuale": "TV LG Saletta TV",
      "nome_proposto": "LGwebOSTV",
      "fonte": "dns",
      "fonte_label": "DNS",
      "confidenza": 0.6,
      "confidenza_pct": 60,
      "updated_at": "2026-07-18T00:14:21.028854Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 55,
      "score_proposto": 40,
      "collisioni_stesso_proposto": 1
    },
    {
      "kind": "proposta_nome",
      "asset_id": 29,
      "mac": "00:03:50:00:88:FA",
      "macs": [
        "00:03:50:00:88:FA"
      ],
      "ip": "192.168.1.50",
      "ips": [
        "192.168.1.50"
      ],
      "nome_attuale": "TouchBTicino",
      "nome_proposto": "BTicino",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.835335Z",
      "presence_state": "present",
      "port": null,
      "port_label": null,
      "status": "noto",
      "less_specific_noise": true,
      "score_attuale": 55,
      "score_proposto": 40,
      "collisioni_stesso_proposto": 3
    },
    {
      "kind": "proposta_nome",
      "asset_id": 51,
      "mac": "DC:A6:32:9C:A7:62",
      "macs": [
        "DC:A6:32:9C:A7:62"
      ],
      "ip": "192.168.2.138",
      "ips": [
        "192.168.2.138"
      ],
      "nome_attuale": "allsky3",
      "nome_proposto": "Raspberry Pi",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.836987Z",
      "presence_state": "present",
      "port": "328c:24",
      "port_label": "LGS328C · porta 24",
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 40,
      "score_proposto": 55,
      "collisioni_stesso_proposto": 4
    },
    {
      "kind": "proposta_nome",
      "asset_id": 46,
      "mac": "D8:3A:DD:51:1E:21",
      "macs": [
        "D8:3A:DD:51:1E:21"
      ],
      "ip": "192.168.2.110",
      "ips": [
        "192.168.2.110"
      ],
      "nome_attuale": "ropieee",
      "nome_proposto": "Raspberry Pi",
      "fonte": "oui",
      "fonte_label": "OUI",
      "confidenza": 0.85,
      "confidenza_pct": 85,
      "updated_at": "2026-07-17T23:40:43.836973Z",
      "presence_state": "present",
      "port": "310c:6",
      "port_label": "LGS310C · porta 6",
      "status": "noto",
      "less_specific_noise": false,
      "score_attuale": 40,
      "score_proposto": 55,
      "collisioni_stesso_proposto": 4
    }
  ],
  "device_nuovi": [
    {
      "kind": "device_nuovo",
      "asset_id": 83,
      "name": "PC-192-168-2-200",
      "mac": "E8:DA:20:C8:49:44",
      "ip": "192.168.2.200",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 84,
      "name": "PC-192-168-2-71",
      "mac": "B0:F7:C4:C2:EE:D7",
      "ip": "192.168.2.71",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 85,
      "name": "PC-192-168-2-85",
      "mac": "4A:77:B9:A5:31:F7",
      "ip": "192.168.2.85",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 86,
      "name": "PC-192-168-2-90",
      "mac": "02:EF:4B:D8:13:65",
      "ip": "192.168.2.90",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 92,
      "name": "PC-3C-55-76-94-0C-FD",
      "mac": "3C:55:76:94:0C:FD",
      "ip": null,
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 95,
      "name": "PC-5C-0C-E6-EE-4C-85",
      "mac": "5C:0C:E6:EE:4C:85",
      "ip": "192.168.2.58",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 98,
      "name": "Amazon Echo/Fire (OUI 2023+)",
      "mac": "68:13:F3:E7:D2:B2",
      "ip": "192.168.2.88",
      "status": "nuovo",
      "presence_state": "present"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 106,
      "name": "PC-CA-C3-F2-A0-30-09",
      "mac": "CA:C3:F2:A0:30:09",
      "ip": "192.168.2.204",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 108,
      "name": "PC-D6-A9-77-61-25-17",
      "mac": "D6:A9:77:61:25:17",
      "ip": "192.168.2.195",
      "status": "nuovo",
      "presence_state": "present"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 109,
      "name": "Switch Linksys",
      "mac": "D8:EC:5E:CC:1C:01",
      "ip": null,
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 110,
      "name": "PC-DA-76-2F-66-1C-14",
      "mac": "DA:76:2F:66:1C:0B",
      "ip": null,
      "status": "nuovo",
      "presence_state": "recent"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 116,
      "name": "c9529b75-66ef-4852-8b08-4c41f6396654",
      "mac": null,
      "ip": null,
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 117,
      "name": "WINC-00-00",
      "mac": "B4:C2:6A:1E:DB:3A",
      "ip": "192.168.2.61",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 118,
      "name": "Watch",
      "mac": "5E:55:DB:65:72:1F",
      "ip": "192.168.2.55",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 119,
      "name": "Xiaomi-Gateway",
      "mac": "04:CF:8C:AC:48:74",
      "ip": "192.168.1.96",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 120,
      "name": "Raspberry Pi",
      "mac": "D8:3A:DD:F4:42:78",
      "ip": "192.168.2.179",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 122,
      "name": "iPad",
      "mac": "A6:EF:8A:16:89:E8",
      "ip": "192.168.2.225",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 123,
      "name": "iPad-2",
      "mac": "44:C6:5D:49:EF:AB",
      "ip": "192.168.2.156",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 124,
      "name": "iPadPro-di-MS",
      "mac": "CC:44:63:97:18:46",
      "ip": "192.168.1.85",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 125,
      "name": "iPaddiChristian",
      "mac": "4C:56:9D:46:2F:63",
      "ip": "192.168.1.61",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 126,
      "name": "iPhone",
      "mac": "4A:C9:89:89:92:C2",
      "ip": "192.168.2.242",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 127,
      "name": "iPhone",
      "mac": "1A:68:68:01:03:E4",
      "ip": "192.168.2.131",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 128,
      "name": "iPhone",
      "mac": "02:AA:3A:FF:48:33",
      "ip": "192.168.3.41",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 129,
      "name": "iPhone",
      "mac": "22:83:8E:76:59:01",
      "ip": "192.168.2.243",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 130,
      "name": "iPhone",
      "mac": "BE:C7:6A:B4:E7:98",
      "ip": "192.168.2.245",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 131,
      "name": "iPhone",
      "mac": "E2:76:2D:4C:0D:E3",
      "ip": "192.168.2.130",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 132,
      "name": "iPhone",
      "mac": "E2:07:F6:A6:50:D3",
      "ip": "192.168.2.198",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 133,
      "name": "iPhoneXdiChris",
      "mac": "40:9C:28:56:5A:DA",
      "ip": "192.168.1.54",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 134,
      "name": "iPhoneXdiChris",
      "mac": "94:16:25:9E:7A:DA",
      "ip": "192.168.1.63",
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 135,
      "name": "Sky",
      "mac": "D4:52:EE:C3:25:16",
      "ip": null,
      "status": "nuovo",
      "presence_state": "present"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 136,
      "name": "Sky",
      "mac": "38:A6:CE:3E:9C:A8",
      "ip": null,
      "status": "nuovo",
      "presence_state": "present"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 137,
      "name": "Sky",
      "mac": "38:A6:CE:79:D4:FE",
      "ip": null,
      "status": "nuovo",
      "presence_state": "present"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 138,
      "name": "72:28:57:FE:0A:F9",
      "mac": "72:28:57:FE:0A:F9",
      "ip": "192.168.2.108",
      "status": "nuovo",
      "presence_state": "recent"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 139,
      "name": "Switch Linksys",
      "mac": "D8:EC:5E:C5:7E:C9",
      "ip": null,
      "status": "nuovo",
      "presence_state": "recent"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 140,
      "name": "AA:2F:22:89:3A:26",
      "mac": "AA:2F:22:89:3A:26",
      "ip": null,
      "status": "nuovo",
      "presence_state": "present"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 141,
      "name": "42:44:E3:5B:2F:6C",
      "mac": "42:44:E3:5B:2F:6C",
      "ip": null,
      "status": "nuovo",
      "presence_state": "fritz_only"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 142,
      "name": "DA:76:2F:66:1C:0D",
      "mac": "DA:76:2F:66:1C:0D",
      "ip": null,
      "status": "nuovo",
      "presence_state": "recent"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 143,
      "name": "DA:F6:2F:62:7E:CF",
      "mac": "DA:F6:2F:62:7E:CF",
      "ip": null,
      "status": "nuovo",
      "presence_state": "recent"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 144,
      "name": "E2:E9:B1:76:BE:9D",
      "mac": "E2:E9:B1:76:BE:9D",
      "ip": null,
      "status": "nuovo",
      "presence_state": "recent"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 145,
      "name": "0A:53:5E:59:F6:A8",
      "mac": "0A:53:5E:59:F6:A8",
      "ip": null,
      "status": "nuovo",
      "presence_state": "present"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 146,
      "name": "1E:34:BD:53:FA:47",
      "mac": "1E:34:BD:53:FA:47",
      "ip": null,
      "status": "nuovo",
      "presence_state": "present"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 147,
      "name": "Switch Linksys",
      "mac": "D8:EC:5E:CC:1C:05",
      "ip": null,
      "status": "nuovo",
      "presence_state": "present"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 148,
      "name": "6E:4C:CE:84:8E:1D",
      "mac": "6E:4C:CE:84:8E:1D",
      "ip": null,
      "status": "nuovo",
      "presence_state": "present"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 149,
      "name": "Sky",
      "mac": "38:A6:CE:3E:9C:AB",
      "ip": null,
      "status": "nuovo",
      "presence_state": "present"
    },
    {
      "kind": "device_nuovo",
      "asset_id": 151,
      "name": "Switch Linksys",
      "mac": "D8:EC:5E:CC:1C:08",
      "ip": null,
      "status": "nuovo",
      "presence_state": "present"
    }
  ],
  "monitor_degradati": [
    {
      "kind": "monitor",
      "monitor_id": 25,
      "name": "Cassiopea — NIC 2",
      "target": "192.168.3.24",
      "asset_id": 6,
      "last_status": "down",
      "condition": "",
      "flap_count": 0
    },
    {
      "kind": "monitor",
      "monitor_id": 29,
      "name": "DVR Hikvision",
      "target": "192.168.1.250",
      "asset_id": 12,
      "last_status": "up",
      "condition": "flapping",
      "flap_count": 4
    },
    {
      "kind": "monitor",
      "monitor_id": 30,
      "name": "Nintendo Switch",
      "target": "192.168.2.206",
      "asset_id": 60,
      "last_status": "down",
      "condition": "",
      "flap_count": 0
    }
  ],
  "collisioni_inventario_top": [
    {
      "proposto": "Sky",
      "in_coda": 8,
      "asset_con_nome_esatto": 5,
      "asset_ids_esatto": [
        43,
        58,
        61,
        82,
        88
      ],
      "asset_con_nome_norm": 5,
      "asset_ids_norm": [
        43,
        58,
        61,
        82,
        88
      ],
      "esempi_norm": [
        "Sky",
        "Sky",
        "Sky",
        "Sky",
        "Sky"
      ]
    },
    {
      "proposto": "LGwebOSTV",
      "in_coda": 1,
      "asset_con_nome_esatto": 2,
      "asset_ids_esatto": [
        74,
        75
      ],
      "asset_con_nome_norm": 2,
      "asset_ids_norm": [
        74,
        75
      ],
      "esempi_norm": [
        "LGwebOSTV",
        "LGwebOSTV"
      ]
    },
    {
      "proposto": "Amazon",
      "in_coda": 6,
      "asset_con_nome_esatto": 1,
      "asset_ids_esatto": [
        53
      ],
      "asset_con_nome_norm": 1,
      "asset_ids_norm": [
        53
      ],
      "esempi_norm": [
        "Amazon"
      ]
    },
    {
      "proposto": "Echo Cucina",
      "in_coda": 1,
      "asset_con_nome_esatto": 1,
      "asset_ids_esatto": [
        55
      ],
      "asset_con_nome_norm": 1,
      "asset_ids_norm": [
        55
      ],
      "esempi_norm": [
        "Echo Cucina"
      ]
    },
    {
      "proposto": "Robot Roborock",
      "in_coda": 1,
      "asset_con_nome_esatto": 1,
      "asset_ids_esatto": [
        36
      ],
      "asset_con_nome_norm": 1,
      "asset_ids_norm": [
        36
      ],
      "esempi_norm": [
        "Robot Roborock"
      ]
    },
    {
      "proposto": "Sensore o presa IoT (chip ESP)",
      "in_coda": 1,
      "asset_con_nome_esatto": 1,
      "asset_ids_esatto": [
        54
      ],
      "asset_con_nome_norm": 1,
      "asset_ids_norm": [
        54
      ],
      "esempi_norm": [
        "Sensore o presa IoT (chip ESP)"
      ]
    },
    {
      "proposto": "Raspberry Pi",
      "in_coda": 4,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    },
    {
      "proposto": "BTicino",
      "in_coda": 3,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    },
    {
      "proposto": "Switch Linksys",
      "in_coda": 3,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    },
    {
      "proposto": "BMS Honeywell",
      "in_coda": 2,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    },
    {
      "proposto": "Cassiopea (ASUSTOR)",
      "in_coda": 2,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    },
    {
      "proposto": "Echo Amazon",
      "in_coda": 2,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    },
    {
      "proposto": "Gaggenau",
      "in_coda": 2,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    },
    {
      "proposto": "TP-Link",
      "in_coda": 2,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    },
    {
      "proposto": "Unknown",
      "in_coda": 2,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    },
    {
      "proposto": "amazon-5b5bf3c111c404ae",
      "in_coda": 1,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    },
    {
      "proposto": "AmazonAQM-008G",
      "in_coda": 1,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    },
    {
      "proposto": "Apparato ASUS",
      "in_coda": 1,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    },
    {
      "proposto": "Dispositivo Apple",
      "in_coda": 1,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    },
    {
      "proposto": "Echo Media",
      "in_coda": 1,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    },
    {
      "proposto": "Echo Sala",
      "in_coda": 1,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    },
    {
      "proposto": "FRITZ!Box",
      "in_coda": 1,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    },
    {
      "proposto": "FRITZ!Powerline",
      "in_coda": 1,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    },
    {
      "proposto": "Fritz-CabinaArmadio",
      "in_coda": 1,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    },
    {
      "proposto": "Fritz-Cucina",
      "in_coda": 1,
      "asset_con_nome_esatto": 0,
      "asset_ids_esatto": [],
      "asset_con_nome_norm": 0,
      "asset_ids_norm": [],
      "esempi_norm": []
    }
  ],
  "collisioni_sky": [
    {
      "proposto": "Sky",
      "in_coda": 8,
      "asset_con_nome_esatto": 5,
      "asset_ids_esatto": [
        43,
        58,
        61,
        82,
        88
      ],
      "asset_con_nome_norm": 5,
      "asset_ids_norm": [
        43,
        58,
        61,
        82,
        88
      ],
      "esempi_norm": [
        "Sky",
        "Sky",
        "Sky",
        "Sky",
        "Sky"
      ]
    }
  ]
}
```
