# OBS-OGGI-TRIAGE-031 — Ricognizione chassis (sola lettura)

Misura live Cassiopea · 2026-07-24 · nessun fix · nessun deploy  
Fonte dati: DB API container + codice `rule_version=2` (`chassis_grouping.RULE_VERSION`)

---

## C1 — Sottogruppo Oggi `chassis(21)`

Criterio riga (come UI): asset in chassis ≥2 membri, non `ignorato`, con proposta nome pending diversa dal nome attuale (serialize API).

| asset | MAC | nome attuale | proposta (src) | chassis | mgmt (label bearer) |
|------:|-----|--------------|----------------|---------|---------------------|
| 30 | `DC:A6:32:9C:A7:63` | Allsky 3 | Raspberry Pi (oui) | Allsky 3 | `#51` `DC:A6:32:9C:A7:62` / `192.168.2.138` |
| 51 | `DC:A6:32:9C:A7:62` | allsky3 | Raspberry Pi (oui) | Allsky 3 | `#51` `DC:A6:32:9C:A7:62` / `192.168.2.138` |
| 5 | `24:4B:FE:84:6A:01` | Cassiopea — NIC 1 | Cassiopea (ASUSTOR) (oui) | Cassiopea — NIC 1 | `#5` `24:4B:FE:84:6A:01` / `192.168.1.3` |
| 6 | `24:4B:FE:84:6A:02` | Cassiopea — NIC 2 | Cassiopea (ASUSTOR) (oui) | Cassiopea — NIC 1 | `#5` `24:4B:FE:84:6A:01` / `192.168.1.3` |
| 35 | `6C:99:9D:08:8E:1D` | Echo Camera Beatrice | Amazon (oui) | Echo Camera Beatrice | `#35` … / `192.168.2.76` |
| 55 | `40:89:C6:B6:2F:6C` | Echo Cucina | amazon-5b5bf3c111c404ae (dns) | Echo Cucina | `#55` … / `192.168.2.176` |
| 33 | `08:A6:BC:B2:F6:A8` | Echo Salone | Echo Media (ai) | Echo Salone | `#33` … / `192.168.2.70` |
| 49 | `E0:D3:62:ED:BE:9D` | Hub Tapo H100 | TP-Link (oui) | Hub Tapo H100 | `#49` … / `192.168.2.124` |
| 28 | `A8:5E:45:12:3A:26` | Kraken | Apparato ASUS (oui) | Kraken | `#28` … / `192.168.1.44` |
| 3 | `D8:EC:5E:C5:7E:C7` | LGS310C | Switch Linksys (oui) | LGS310C | `#3` … / `192.168.1.7` |
| 2 | `C8:54:4B:F4:71:D5` (+ `D8:EC:5E:CC:1B:FF`) | LGS328C | Switch (dns) | LGS328C | `#2` IP `192.168.1.2` (entrambe le iface) |
| 147 | `D8:EC:5E:CC:1C:05` | *(vuoto)* | Switch Linksys (oui) | LGS328C | `#2` / `192.168.1.2` |
| 151 | `D8:EC:5E:CC:1C:08` | *(vuoto)* | Switch Linksys (oui) | LGS328C | `#2` / `192.168.1.2` |
| 50 | `1C:69:7A:A6:FA:47` | ROCK | PC (oui) | ROCK | `#50` … / `192.168.2.126` |
| 108 | `D6:A9:77:61:25:17` | Sky TV | PC 108 (ai) | Sky | `#108` … / `192.168.2.195` |
| 135 | `D4:52:EE:C3:25:16` | Sky TV | Sky (oui) | Sky | `#108` … / `192.168.2.195` |
| 136 | `38:A6:CE:3E:9C:A8` | *(vuoto)* | Sky (oui) | Sky | `38:A6:CE:3E:9C:AA` / `192.168.2.101` |
| 137 | `38:A6:CE:79:D4:FE` | *(vuoto)* | Sky (oui) | Sky | `38:A6:CE:79:D4:FD` / `192.168.2.254` |
| 149 | `38:A6:CE:3E:9C:AB` | *(vuoto)* | Sky (oui) | Sky | `38:A6:CE:3E:9C:AA` / `192.168.2.101` |
| 10 | `70:50:AF:FC:0A:F8` | SkyBooster2 BIBLIO — Ethernet | Sky (oui) | SkyBooster2 BIBLIO — Ethernet | `#11` `70:50:AF:FC:0A:F9` / `192.168.2.108` |
| 11 | `70:50:AF:FC:0A:F9` | SkyBooster2 BIBLIO — mesh | Sky (oui) | SkyBooster2 BIBLIO — Ethernet | `#11` … / `192.168.2.108` |

**MAC di porta di uno switch tra le 21:** **2 / 21**  
Definizione usata: membro di chassis switch-like (`LGS*` / `GS*` / `SWITCH` nel label) **senza IP current** (L2-only) → `#147`, `#151` sul chassis LGS328C.  
Nota: esiste anche `#109` `D8:EC:5E:CC:1C:01` (stesso profilo, L2-only su LGS328C) ma **non** è nelle 21 perché non ha proposta pending “azioneabile” in Oggi.

(Non confondere con `SwitchPort.asset_id`: quello è l’endpoint *legato* a una porta FDB, non il MAC della porta dello switch.)

---

## C2 — Chassis LGS328C (id=23)

Label: `LGS328C` · origin `auto` · `rule_version=2` · confirmations persistite: **`["C4","R2"]`**  
Creato `2026-07-23T01:49:40Z` · last_confirmed `2026-07-23T22:55:54Z`

| asset | MAC | IP current | first_seen (UTC) | evidenza di unione al gruppo |
|------:|-----|------------|------------------|------------------------------|
| **2** | `D8:EC:5E:CC:1B:FF` + `C8:54:4B:F4:71:D5` | `192.168.1.2` (×2 iface) | `2026-07-18T01:26:08Z` | **Primary** del gruppo. Arco **R2** verso i peer L2 (MAC `D8:EC:5E:CC:1B:FF`). `C8:54:…` è sullo stesso asset per merge infrastruttura IP (vedi C3), **non** per R2. |
| 109 | `D8:EC:5E:CC:1C:01` | — | `2026-07-18T01:26:08Z` | **R2** link `[2,109]` macs `…1B:FF`↔`…1C:01` + **C4** (`l2_only_members`) |
| 147 | `D8:EC:5E:CC:1C:05` | — | `2026-07-21T08:32:05Z` | **R2** link `[2,147]` + **C4** |
| 151 | `D8:EC:5E:CC:1C:08` | — | `2026-07-23T01:47:27Z` | **R2** link `[2,151]` + **C4** |

Evidenza grezza in `chassis.meta.evidence`:

```json
{
  "rule_version": "2",
  "C4": {"primary_asset_id": 2, "l2_only_members": [109, 147, 151]},
  "R2": {
    "links": [
      {"asset_ids": [2, 109], "macs": ["D8:EC:5E:CC:1B:FF", "D8:EC:5E:CC:1C:01"], "oui3": "D8:EC:5E"},
      {"asset_ids": [2, 147], "macs": ["D8:EC:5E:CC:1B:FF", "D8:EC:5E:CC:1C:05"], "oui3": "D8:EC:5E"},
      {"asset_ids": [2, 151], "macs": ["D8:EC:5E:CC:1B:FF", "D8:EC:5E:CC:1C:08"], "oui3": "D8:EC:5E"}
    ],
    "oui_allowlist": ["D8:EC:5E"]
  }
}
```

**Regole citate (file:riga):**

| codice | cosa fa | dove |
|--------|---------|------|
| **R2** | stesso OUI3 allowlist + `\|Δo4\|≤1` + `\|Δo5\|≤1` (prefix5 allentato), non LLDP | `api/app/services/chassis_grouping.py:36` (`SWITCH_OUI_ALLOWLIST`), `:240–251` (`_prefix5_relaxed_adjacent`), `:359–375` (arco R2), `:539–542` (conferma) |
| **C4** | primary + peer **L2-only veri** (no IP e no porta dedicata) | `chassis_grouping.py:454–474` |
| SAFE legacy | stesso prefix5 + `\|Δ last\|≤8` | `chassis_grouping.py:297+` — **non** usata qui (prefix5 diversi: `…CC:1B` vs `…CC:1C`) |
| C3 co-FDB / LLDP | — | **assenti** da `confirmations` / `evidence` di questo chassis |

---

## C3 — Perché `C8:54:4B:F4:71:D5` è nel chassis LGS328C con OUI diverso

**Non è un merge chassis su OUI `C8:54:4B`.**

1. Il MAC sta su **asset `#2`** insieme a `D8:EC:5E:CC:1B:FF` (due `interfaces`, IP current entrambi `192.168.1.2`).
2. Provenienza del secondo MAC: asset **`#116`** (Fritz host “Switch” su `192.168.1.2`) → assorbito nel canonico switch via `reconcile_known_infrastructure` / `_merge_switch_duplicate` (stesso IP di management dello `Switch` `328c`).  
   - Traccia: `#2.meta.merged_asset_ids = [116]`, `#116.meta.canonical_asset_id = 2`, `reconciled_switch_id = 1`.  
   - Interface `C8:54:…` creata `2026-07-18T01:26:08Z` (ex `#116`); `D8:EC:…` esisteva da `2026-07-17T23:06:25Z`.
3. Il **chassis** unisce `#2` ai peer L2 `#109/#147/#151` solo tramite **R2 sull’OUI Linksys `D8:EC:5E`** (+ C4). Nessun link R2/C3 cita `C8:54:4B`.

**Verdetto:** regge come **merge infrastruttura per IP esatto** (`identity.py` `reconcile_known_infrastructure` ~825–908, `_merge_switch_duplicate` ~489–564), non come falso positivo dell’euristica chassis OUI. L’OUI diverso è atteso: Fritz ha visto un MAC, SNMP/seed lo switch un altro, stesso `192.168.1.2`.

---

## C4 — Due «Prima volta» (21/07 10:32 vs 18/07 03:26)

Fuso orario UI Europe/Rome = UTC+2 (luglio):

| UI | ora locale | UTC DB | campo | livello |
|----|------------|--------|-------|---------|
| **Chi sei** | 21/07 **10:32** | `2026-07-21T08:32:05Z` | `Asset.first_seen` dell’asset in URL | **asset-level** |
| **Come sei connesso** | 18/07 **03:26** | `2026-07-18T01:26:08Z` | `device.first_seen` dopo resolve chassis = **`primary.first_seen`** | **chassis-level (primary)** |

Match live: `#147.first_seen = 2026-07-21T08:32:05Z` · `#2.first_seen = 2026-07-18T01:26:08Z`.

**Campi / codice:**

- Chi sei → `identity.first_seen` = `asset.first_seen || portal_first_seen || created_at`  
  `api/app/services/asset_identity.py:423` · UI `AssetIdentity.vue` (“Prima volta”).
- Come sei connesso → `device?.first_seen || asset?.first_seen`  
  `web/src/components/AssetChassis.vue:22–24,139–140`.  
  Con chassis ≥2, `loadChassisScoped` → `composeDevices` imposta `first_seen: primary.first_seen`  
  `web/src/inventoryDevices.js:199` (**non** `min(membri)`).

Quindi lo scarto compare aprendo un **membro non-primary** (es. `#147`): Chi sei parla dell’asset, Come sei connesso della faccia chassis (primary `#2`).

---

## C5 — Proposte nome su membri chassis / MAC di porta

**Filtro che impedisce di generarle per MAC di porta: non esiste.**

Verificato su `suggest.py`, `identity.py` (NameProposal), `dhcp_names.py`, `ai_naming.py`: nessuno salta L2-only di chassis né MAC contigui switch. `ai_naming._pick_primary` sceglie solo il contesto AI, non blocca proposte sugli altri membri.

| metrica | n |
|---------|--:|
| membri in chassis ≥2 | 35 |
| NameProposal **totali** su quei membri | **78** |
| di cui **pending** | **75** |
| totali su membri L2-only (proxy “porta/radio senza IP”) | 23 |
| pending su L2-only | 21 |
| pending su chassis per source | oui 24 · dns 20 · fritz 18 · ssdp 5 · ai 4 · dhcp 4 |

Nelle sole 21 righe Oggi-chassis, le proposte sui due MAC di porta LGS sono `#147` e `#151` → «Switch Linksys» (oui).

---

## Numeri utili per dimensionare il cantiere

- Oggi chassis rows: **21**
- Di cui MAC di porta switch (L2-only su chassis switch): **2** (+1 `#109` fuori Oggi)
- Chassis LGS328C: **4** membri · conferma **R2+C4** · zero FDB/LLDP in evidence
- `C8:54:4B:…`: stesso asset del mgmt via **reconcile IP**, non R2
- Proposte su membri chassis: **78** totali / **75** pending · **nessun filtro** porta

Nessuna proposta di codice in questo report.
