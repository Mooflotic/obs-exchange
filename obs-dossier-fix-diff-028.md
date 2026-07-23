# OBS-DOSSIER-FIX-DIFF-028 (rigenerato)

## Summary — SOLO i 4 fix

1. **CandidateList** — collassa dopo scelta + «cambia»; placeholder neutro «nessuna di queste? scrivila»
2. **Ordine Dossier** — Chi sei → Come sei connesso (§6)
3. **AssetChassis** — niente `api.assets()` full inventory; errore/vuoto; **chassis-scoped**: `api.chassis()` + fetch solo dei member (perché `GET /api/assets/{id}` non include NIC sibling)
4. **os_divergence** — confronto normalizzato (`Linux 4.15` ≡ `Linux 4.15 - 5.19`)

## Base

Diff contro `reconcile/live-base` @ **v0.10.17** (sync Cassiopea live).  
Fingerbank **027 non incluso** (`feature/obs-fingerbank-027`).

## File nel pacchetto

- `web/src/components/ui/CandidateList.vue`
- `web/src/components/AssetChassis.vue`
- `web/src/components/AssetIdentity.vue` (startCollapsed)
- `web/src/views/Dossier.vue` (ordine sezioni)
- `api/app/services/asset_identity.py` (os_labels_equivalent)
- `tests/test_asset_identity.py` (solo test truncation)
- `web/src/components/ui/uiPrimitives.test.js`
- `VERSION` / `CHANGELOG.md`

**Non incluso:** `api.js`, `field_sources_vocab.py`, Fingerbank, test migrate vocab.

## test_oui_parse_ieee_and_lookup

**Non cancellato dal 028.** Assente già su live 0.10.17 (e sul tree riconciliato). Presente solo a git `main` @ 0.10.15. Il pacchetto 028 precedente lo mostrava come delete perché il diff era contro HEAD 0.10.15, non contro live.

## Chassis siblings

`GET /api/assets/{id}` → solo interfacce di **quel** asset. I sibling chassis sono asset distinti. Il fix AssetChassis usa `GET /api/chassis` + `GET /api/assets/{member}` per i soli membri del gruppo.

**STOP pre-deploy.** Nessun merge su main senza review.
