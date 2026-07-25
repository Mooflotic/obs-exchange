# OBS-PORTALE — Ondata 1 (0.10.31)

**Branch:** `feature/obs-portale` · **Tag:** `v0.10.31` = `eed5580`  
**Deploy:** 2026-07-25 · live health `0.10.31`

## Cosa

Dichiarare l’assenza al posto di valori plausibili (debiti f, g, h, i):

1. CandidateList: scelta manuale → badge «manuale», non barra 100%
2. Sidebar: senza `health.version` → «versione non disponibile · {buildId}»
3. DirectionBar / Habits: «direzione non disponibile» + colonna `n/d`
4. AssetChassis: `partialWarning` se member/chassis fail (no mono-NIC silenzioso)

## Assert

| ID | Criterio | Esito | Evidenza |
|----|----------|-------|----------|
| W1 | health 0.10.31 | **PASS** | `{"ok":true,"version":"0.10.31"}` |
| W2 | boot regime needs_apply=false, T_backup=0, ~9s | **PASS** | regime restart: T_total=**9.019**s, needs_apply=false, T_backup=0.0 (primo boot post-deploy structural=1 / T_backup=89.5s — atteso una tantum) |
| W3 | quattro assenze dichiarate | **PASS** | dist: `versione non disponibile`, `direzione non disponibile`, `manuale`, `chassis parziale`; test `portaleDeclareAbsence.test.js` |
| W4 | assets 151, NP invariate | **PASS** | assets=151, name_proposals=412, pending=135 |

## Curl

- `GET /api/health` → 200 · version 0.10.31
- `GET /` (web) → 200

## Debiti chiusi

DEBT-MANUAL-CONF-BAR, DEBT-VERSION-SILENT-FALLBACK, DEBT-HABITS-DIR-UNAVAILABLE, DEBT-CHASSIS-PARTIAL-SILENT (CHIUSA in 0.10.31).

## Note

- Primo boot dopo deploy: `structural=1` (trust apply) + backup — non è regressione del regime.
- Docs close marker: commit `d79b26e` (fuori tag, policy).
