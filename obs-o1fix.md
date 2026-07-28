# OBS-O1-FIX — provenienza onesta + conservazione coda (0.10.65)

## Residuo OBS-CURRENCY (sospeso, non chiuso)

- T7 mai eseguita in prod; `DEBT-PROD-SOURCE-DRIFT` aperto; `_w4a_measure.py` sul NAS **non** toccato.
- Nessun merge su main.

## Conteggio righe artefatti

| Artefatto | `wc -l` |
|---|---|
| `obs-o1fix.md` | 202 |
| `obs-o1fix.diff.txt` | 2314 |

---

## PREVISIONI (pinnate PRIMA del deploy)

### `name_kind` atteso sui 15 chassis (T1)

Misura payload live pre-deploy (`/api/chassis` + assets `include_historical=true`): currency `absent` su tutti.

| `name_kind` | ids chassis |
|---|---|
| `legacy_manual` | **{1, 3, 15, 18, 30, 32}** (6) |
| `inference` | **{16, 17, 19, 20, 23, 28, 31, 33}** (8) |
| `absent` | **{9}** (1) |
| `fact` | **∅** (0) — nessuno ha `name_currency.state=fact` |

### Id che cambiano etichetta rispetto a 0.10.64

**{1, 3, 15, 18, 30, 32}**: da «manuale»/«fatto manuale» spurio → legacy senza «fatto» in `certainty`.

### `queueConservationCheck` PRIMA della correzione T2

Pending non-`ignorato` = **{109, 151}** (entrambi su card 23).

Con builder O1 (`chassisMemberIds` grezzo): **`missing: []`, `duplicated: []`**.

→ D2 **latente** in produzione. **N6 assente** in prod → solo test **P3** (K4).

### DOPO (atteso)

`missing: []`, `duplicated: []`.

### Nodi

| Nodo | Atteso |
|---|---|
| N1 ch32 | `legacy_manual`, certainty senza «fatto», correggi (+ conferma) |
| N2 ch23 | `inference` oui |
| N4 ch1 | `legacy_manual`, una card |
| N6 | solo P3 |

---

## Diff

Vedi `obs-o1fix.diff.txt`.

File toccati: `oggiChassis.js`(+test), `triageRules.js`, `oggiProblems.js`, `Oggi.vue`, `KNOWN_DEBT.md`, `VERSION`, `web/package.json`, `CHANGELOG.md`.

Esclusioni: `api/app/facts/**`; codice runtime API (deploy api solo per VERSION in health); collector; FDB/Mappa/308/Dossier/favicon/restyle; screenshot; `_w4a_measure.py`; merge main.

### T1.d — punti verificati (legacy ≠ fact)

1. assignment `fact` solo da currency fact  
2. `chassisNameFields` branch `legacy_manual`  
3. `chassisProvenanceLabel` branch dedicato  
4. priorità media + verdict `chassis_nome_legacy`  
5. `AiInferenceLabel` non su legacy  
6. I3/`heldManual` invariati; azioni correggi+conferma  

### T4

`split(/\s+/)`. Nessun cambio token su sorgenti reali monotoken.

---

## Deploy

1. `./scripts/deploy.sh web` (codice O1-FIX).  
2. `./scripts/deploy.sh api` solo per allineare `VERSION` in `/api/health` (nessun cambio codice API). Collector intatto.

---

## OSSERVATI (dopo deploy)

### Kinds (15 card)

| kind | ids |
|---|---|
| `legacy_manual` | {1, 3, 15, 18, 30, 32} |
| `inference` | {16, 17, 19, 20, 23, 28, 31, 33} |
| `absent` | {9} |
| `fact` | ∅ |
| `fact` con currency≠fact | ∅ |

Allineato alle previsioni. **Scarti: nessuno.**

### Conservazione

```json
{"missing":[],"duplicated":[]}
```

Pre e post: entrambi vuoti (D2 latente).

### N1 / N2 / N4 — JSON grezzo

**N1 chassis 32:**
```json
{
  "chassis_id": 32,
  "name_kind": "legacy_manual",
  "fact_is_manual": true,
  "name_currency": {"value": null, "source": null, "confidence": null, "authority": null, "state": "absent"},
  "display_name": "LGS310C",
  "name_source": "manual",
  "actions": ["correggi", "conferma_manuale"],
  "conflict": false,
  "member_asset_ids": [3, 139, 143],
  "certainty": "manuale su interfaccia · confidenza 100% · non consolidato",
  "certainty_has_fatto": false
}
```

**N2 chassis 23:**
```json
{
  "chassis_id": 23,
  "name_kind": "inference",
  "fact_is_manual": false,
  "name_currency": {"value": null, "source": null, "confidence": null, "authority": null, "state": "absent"},
  "display_name": "LGS328C",
  "name_source": "oui",
  "actions": ["correggi", "adotta_proposta"],
  "member_asset_ids": [2, 109, 147, 151],
  "certainty": "inferenza oui · confidenza — · I1",
  "certainty_has_fatto": false
}
```

**N4 chassis 1:**
```json
{
  "chassis_id": 1,
  "name_kind": "legacy_manual",
  "fact_is_manual": true,
  "name_currency": {"value": null, "source": null, "confidence": null, "authority": null, "state": "absent"},
  "display_name": "Cassiopea — NIC 1",
  "actions": ["correggi", "conferma_manuale"],
  "member_asset_ids": [5, 6],
  "certainty": "manuale su interfaccia · confidenza 100% · non consolidato",
  "certainty_has_fatto": false
}
```

### UI (Playwright `/oggi`)

- label legacy presente: *manuale, registrato sull'interfaccia — non ancora fatto d'apparato*
- nessun `fatto manuale ·` spurio
- LGS310C / LGS328C+inferenza oui / Cassiopea — NIC 1 / count 15

### N6

Nessun chassis a rischio in prod. **P3** verde in `oggiChassis.test.js`.

### Test FE nominati

`oggiChassis.test.js` + `oggiTriage.test.js` + `oggiProblems.test.js`: **27 pass, 0 fail** (P1–P4 inclusi; nessun test esistente indebolito/rinominato/invertito).

---

## Criteri di fallimento

| Criterio | Esito |
|---|---|
| legacy con «fatto» in certainty | **PASS** (`certainty_has_fatto=false` N1/N4) |
| I3 non scatta su member-held | **PASS** (P2 + test member-held) |
| conservation missing/duplicated ≠ [] | **PASS** (`[]`/`[]`) |
| test esistente indebolito/rinominato/invertito | **PASS** |
| `name_kind=fact` con currency ≠ fact | **PASS** (lista vuota) |

## Gate

```
VIOLAZIONI: 0
RISULTATO: PASS (con 1 eccezione/i temporanea/e)
I6_EMPTY_OK
```

## Debiti registrati (T5)

- `DEBT-CHASSIS-NAME-LEGACY-HELD`
- `DEBT-OGGI-LAYOUT-OVERFLOW`

## ASSERT

T1/T2/T3/T4/T5 soddisfatti. OBS-CURRENCY resta sospeso. STOP per review.

**STOP.** Non avanzare a FDB / Mappa / 308 / Dossier. Nessun merge su main.
