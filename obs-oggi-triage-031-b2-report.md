# OBS-OGGI-TRIAGE-031 — Report B2

**Branch:** `feature/oggi-triage-031`  
**Commit:** `33520d6` — `feat(oggi): triage griglia + reject NameProposal (B2, 0.10.19)`  
**Base B1-bis:** `0e803fb` (diff separato)  
**VERSION:** **0.10.19**  
**Deploy:** nessuno — STOP pre-deploy, attendi GO

## Motivazione endpoint

Endpoint dedicato `POST /api/assets/{id}/reject-name-proposal` (non parametro su adopt-name): adopt applica il nome; reject solo archivia la `NameProposal` (`status=rejected`) senza toccare `assets.status` / `name`.

Massa: `POST /api/name-proposals/reject-bulk` `{ids:[…]}` (PK `name_proposals`), solo `pending` → conteggi `rejected` / `skipped_non_pending` / `not_found`.

## Exchange

| Artefatto | URL |
|---|---|
| Diff B2 | https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-oggi-triage-031-b2.diff.txt |
| Report | https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-oggi-triage-031-b2-report.md |

## Test

```text
python3 -m pytest tests/test_reject_name_proposal.py -q
→ 4 passed

node --test src/triageRules.test.js src/oggiTriage.test.js src/versionDisplay.test.js
→ 20 pass / 0 fail  (triageRules 13 + oggiTriage 5 + version 2)
```

## Conteggi griglia: fixture vs live

Gruppi UI = `groupTriageRows` (`adotta` / `verifica` / `rumore`=azione archivia).  
I pin nei test dump usano `summarizeTriage` (adotta/verifica azione + `is_noise`); i gruppi rumore sono i soli `recommended_action=archivia` (chassis noise resta in **verifica**).

| Scenario | Adotta | Verifica | Rumore (gruppo) | Note |
|---|---:|---:|---:|---|
| **Fixture dump 030** (test pin, 0 manual) | **9** | **10** | **46** | pin B1/B1-bis; `is_noise`=48 include 2 chassis |
| **Dump 030 + manual live** (sim) | **5** | **14** | **46** | 18 asset manual; flip D4 #64,#42,#68,#82 |
| **Live Cassiopea ora** (DB, sola lettura) | **5** | **53** | **36** | 94 righe pending attuali (coda cresciuta vs 65 del dump) |

**Perché fixture 9/10 ≠ live ~5/14:** i test pinano il dump 030 **senza** `field_sources.name` manual. Sul DB reale 18/65 della coda dump sono manual → D4 sposta 4 adotta→verifica (9→5). Non è regressione: stesso codice, input diverso. La coda live odierna ha più pending (94) quindi verifica/rumore assoluti divergono anche dal dump.

Campioni live **adotta (5):** GS308EP→Switch Netgear; Robot Roborock→roborock-vacuum-a70; anonimo→Raspberry Pi; anonimo→iPhone di Chris; anonimo→Switch Linksys.

## Descrizione griglia renderizzata

```
Oggi
├─ Proposte nome · 5 adotta · 53 verifica · 36 rumore
│  ├─ Adotta consigliati
│  │    [anonimo|nome] → proposto · MAC · IP · porta|— · presenza · FONTE·conf% · badge
│  │    [adotta] [ignora] [apri]
│  ├─ Verifica  (collide / chassis / manual-upgrade / sotto-soglia)
│  │    stesso layout · [verifica] [adotta] [ignora]
│  └─ ▸ N proposte filtrate come rumore   [Archivia rumore (M)]  +C chassis esclusi
│       (espandibile: archivia / adotta / apri)
└─ Altro in coda
   device nuovi + monitor (invariati, solo sotto)
```

Stati: `caricamento…` / errore `role=alert` / vuoto «Niente in coda…». Primitivi: DenseRow, StatusBadge.

## File toccati (B2)

- API: `assets.py` (+`proposals_router`), `main.py`, `event_maintenance.py` (`id` in proposal)
- Web: `Oggi.vue`, `api.js`, `oggiTriage.js`+test, `triageRules.js` (`proposal_id`)
- `VERSION` / `CHANGELOG` / `package.json` → 0.10.19
- `tests/test_reject_name_proposal.py`

## STOP pre-deploy

Review del diff B2, poi **GO** esplicito per sync/deploy. Nessun rename chassis / with_path / Fingerbank / detector.
