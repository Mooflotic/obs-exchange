# OBS-033A — B2 + D12 + D13 (STOP pre-deploy)

**Branch:** `feature/obs-033a` · **commit:** `d08cc13` · **VERSION:** **0.10.21**  
**Deploy:** **no** — review → GO per merge + deploy

---

## Cosa cambia

| ID | Effetto |
|----|---------|
| **B2** | «Archivia rumore (N)» su `noiseIds.length > 0`, anche con griglia rumore vuota; etichetta «proposte non visibili in griglia…». Conferma già gestisce `n > gridRows` (anche `gridRows === 0`). |

### Assert B2 post-massa residui `#2`

Archiviando i rumore residui **`297`** + **`3`** (`Switch` dns/fritz su LGS328C): resta solo `Switch Linksys`/oui → **«top diversa» passa da 1 a 0**.
| **D12** | `scoreSpecificity === 1` → rumore sempre (anche nome attuale vuoto) |
| **D13** | `normalizeName` collassa `-_.`; se chiavi uguali → rumore **prima** dei rank |

Dump 030 re-pin: **48/9/2/10/46 → 51/8/2/8/49** (rumore/adotta/chassis/verifica/mass_eligible).

Debito: `DEBT-NO-RECREATION-GUARD`, `DEBT-VERSION-SILENT-FALLBACK`.

---

## 5 · Previsione live (assert post-deploy)

Calcolata su dump Cassiopea `_serialize` + chassis **prima** del deploy (pending 140, VERSION live ancora 0.10.20).

### Baseline → atteso post-deploy

| Voce | Baseline (0.10.20) | **Atteso 0.10.21** |
|------|-------------------:|-------------------:|
| Pulsante `Archivia rumore (N)` | assente (griglia 0; residuo 2 nascosto) | **`Archivia rumore (7)`** |
| Intestazione | `0 adotta · 25 verifica · 0 rumore` | **`0 adotta · 22 verifica · 3 rumore`** |
| Verifica · chassis | 10 | **10** |
| Verifica · manual-upgrade | 6 | **5** |
| Verifica · sotto-soglia | 9 | **7** |
| Verifica · collide | 0 | **0** |

### Righe griglia verifica → rumore

| Effetto | N | Dettaglio |
|---------|--:|-----------|
| **D12** | **2** | `#85` *(vuoto)* → `PC-192-168-2-85`; `#98` *(vuoto)* → `PC-68-13-F3-E7-D2-B2` |
| **D13** | **1** | `#25` `BTicino F454` → `Bticino-F454` |
| **Totale** | **3** | = nuovo gruppo rumore |

### `noiseIds` (massa)

`[297, 3, 154, 36, 200, 199, 235]` → **7**  
(= 2 chassis Switch `#2` + 2× BTicino D13 + 2× `#85` D12 + 1× `#98` D12)

Se dopo deploy questi numeri divergono: **STOP** e report.

Assert B2 (dopo prima massa o archivio mirato di `297`+`3`): **top diversa = 0**.

---

## 6 · Suite

| Suite | Esito |
|-------|--------|
| `node --test src/*.test.js` | **111 pass / 0 fail** |
| `pytest --ignore=tests/test_m6_m8_detectors_flow.py` | **479 passed / 9 failed** (noti, invariati) |

---

## Diff

`obs-033a.diff.txt` (branch vs main, file del cantiere).

---

## STOP

Review → **GO** per merge no-ff + tag `v0.10.21` + deploy `api web` + assert §5.
