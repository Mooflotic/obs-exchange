# OBS-OGGI-TRIAGE-031 — Report B1 (regole pure)

**Branch:** `feature/oggi-triage-031`  
**Commit:** `182290d` — `feat(oggi): regole pure triage nome (B1, OBS-031)`  
**Scope:** SOLO `observatory/web/src/triageRules.js` + `triageRules.test.js`  
**VERSION:** non bumpata (0.10.19 solo al commit finale del pacchetto)  
**Deploy:** nessuno (attende GO)

## File exchange

| Artefatto | Path |
|---|---|
| Diff B1 | `obs-oggi-triage-031-b1.diff.txt` |
| Questo report | `obs-oggi-triage-031-b1-report.md` |

Raw attesi:

- https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-oggi-triage-031-b1.diff.txt
- https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-oggi-triage-031-b1-report.md

## Modulo

Funzioni pure (D1, nessuna API):

- `normalizeName` — lower + spazi collassati (D7)
- `scoreSpecificity` — scala **1..5** da tabella A3; **PC 108** e **PC-68-13-…** entrambi rank **1** (sintetici; corregge bozza 40 vs 20)
- `countCollisions(proposto, assets, excludeId?)` — uguaglianza normalizzata esatta
- `buildTriageRows(assets, chassisPayload)` — griglia + verdetto + azione + `chassis_member` / `mass_eligible`
- `summarizeTriage(rows)` — conteggi

### Verdetto / azione (D3–D8)

| Condizione | verdict | recommended_action |
|---|---|---|
| membro chassis (≥2) | `chassis` | `verifica` (mass esclusa, D5) |
| `score(prop) ≤ score(cur)` | `rumore` | `archivia` |
| collisioni > 0 | `collide` | `verifica` (mai adotta, D7) |
| nome manual + più specifica | `upgrade` | `verifica` (D4) |
| più specifica ∧ coll=0 ∧ conf≥0.75 ∧ non-manual | `upgrade` | `adotta` (D8) |
| altrimenti upgrade | `upgrade` | `verifica` |

## Test

```text
node --test src/triageRules.test.js
→ 12 pass / 0 fail
```

Casi ambigui 030 pinati:

| # | Caso | Esito |
|---|---|---|
| 1 | Allsky/Pi → Raspberry Pi | rumore |
| 2 | AQM → Echo Cucina | collide |
| 3 | Cassiopea NIC 1/2 | chassis |
| 5 | LGS328C → Switch | rumore (parità) |
| 7 | Sky manual → PC CabinaArmadio | verifica (D4) |

(+ D8 adotta / conf&lt;0.75 → verifica)

## Dump 030 — conteggi regole definitive

Fixture: appendice JSON di `docs/obs-oggi-fasea-030.md` (65 proposte).

| Metrica | Bozza A1 (`<`) | **Definitivo D3 (`≤`, parità inclusa)** |
|---|---:|---:|
| Righe | 65 | **65** |
| Rumore | 26 | **48** (+22 dalla parità e dal riallineamento rank 1..5) |
| Adotta consigliati | — | **9** |
| Verifica (azione) | — | 10 (include 2 chassis) |
| Chassis members | — | 2 |
| Mass-eligible (rumore non-chassis) | — | 46 |
| Collide | — | 6 |

Output test:

```json
{"dump_rows":65,"bozza_rumore_lt":26,"definitivo_rumore_le":48,"adotta_consigliati":9,"verifica":10,"chassis_members":2,"mass_eligible":46,"collide":6}
```

Nota: nel dump `field_sources` è vuoto → `#82 Sky→PC CabinaArmadio` conta come **adotta** (D8). Nel caso unitario 7 con `manual` → **verifica** (D4).

## STOP

B1 pronto per review. **Non partire B2** senza GO esplicito.
