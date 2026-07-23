# OBS-OGGI-TRIAGE-031 — Report B1-bis

**Branch:** `feature/oggi-triage-031`  
**Commit:** `0e803fb8f882730b246c21b160a1d9f96f758c71` (dopo B1 `182290d`)  
**Scope:** solo `triageRules.js` + `triageRules.test.js`  
**VERSION / deploy:** no

## Exchange

| Artefatto | URL |
|---|---|
| Diff | https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-oggi-triage-031-b1bis.diff.txt |
| Report | https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-oggi-triage-031-b1bis-report.md |

## Emendamento

1. **Rank 4 su trattini:** dopo i check rank 5, `isRank4HumanRoom(n)` anche su `n.replace(/-/g, " ")`.
   - `Fritz-Cucina` → **4**, `Echo-Cucina` → **4**
   - invarianti: `PC-68-13-…`=1, `roborock-vacuum-a70`=5, `TP-Link`=2
2. **`is_noise`:** solo `isNoise` (D3); rimossa clausola ridondante `(manual && !moreSpecific)`.
3. **ROOM_RE:** commento — lessico di casa, da curare quando compaiono stanze/dispositivi nuovi.
4. Branch manual D4 semplificato (raggiunto solo se già più specifica).

## Test

```text
node --test src/triageRules.test.js
→ 13 pass / 0 fail
```

## Dump 030 — pin (vecchi B1 → nuovi B1-bis)

I conteggi **fixture** (senza `field_sources` manual) **non cambiano**: i `Fritz-*` in coda sono proposte su asset anonimi (0→4 resta upgrade, non rumore).

| Metrica | B1 | **B1-bis** |
|---|---:|---:|
| Righe | 65 | **65** |
| Rumore | 48 | **48** |
| Adotta | 9 | **9** |
| Verifica (azione) | 10 | **10** |
| Mass-eligible | 46 | **46** |
| Chassis | 2 | **2** |
| Collide | 6 | **6** |

```json
{"dump_rows":65,"bozza_rumore_lt":26,"definitivo_rumore_le":48,"adotta_consigliati":9,"verifica":10,"chassis_members":2,"mass_eligible":46,"collide":6}
```

## Addendum sola lettura — `field_sources.name` manual (DB live Cassiopea)

Query sui **65** `asset_id` della coda dump 030 (meta `field_sources.name` / `manual_overrides`).

| | Valore |
|---|---|
| Asset coda trovati | 65/65 |
| Con nome **manual** | **18** |
| IDs | 5, 12, 19, 28, 30, 32, 34, 37, 38, 42, 46, 48, 49, 64, 68, 76, **82**, 112 |

### Asset #82

| Campo | Valore |
|---|---|
| name | `Sky` |
| `manual_overrides` | `["name"]` |
| `field_sources.name.source` | `manual (proposta oui)` |
| **is_manual_name** | **true** |

Quindi caso 7 in produzione: **verifica** (D4), non adotta — allineato al test unitario B1.

### Tabella: fixture vs atteso col manual reale

Ricalcolo `buildTriageRows` sullo stesso dump, applicando i 18 flag manual live (sola simulazione, non nel codice B1-bis).

| Metrica | Fixture (0 manual) | **Con manual live** |
|---|---:|---:|
| Rumore | 48 | 48 |
| **Adotta** | **9** | **5** |
| **Verifica** | **10** | **14** |
| Mass-eligible | 46 | 46 |

Flip adotta→verifica (D4): `#64` AQM2→AmazonAQM-008G, `#42` Loewe, `#68` ROMO, **`#82` Sky→PC CabinaArmadio**.

## STOP

B1-bis pubblicato. **Ack veloce**, poi si parte B2 (UI + API D6, VERSION 0.10.19).
