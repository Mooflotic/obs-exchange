# OBS-DOSSIER-FIX-DIFF-028b (emendamento post-review)

Delta su `fix/obs-dossier-028` dopo GO condizionato. **VERSION resta 0.10.18.**  
Base: commit 028 (`44f43bb`) + questo emendamento. **Non** merge/main/deploy finché GO finale.

## Cosa cambia

1. **CandidateList** — riga collassata su testo libero: se `modelValue` non è in `candidates`, mostra `modelValue` come nome (niente barra confidenza, **niente** fallback su `normalized[0]`).
2. **KNOWN_DEBT** — `DEBT-OS-LABELS-PREFIX-EQUIV`, `DEBT-CHASSIS-PARTIAL-SILENT`.
3. **Pulizia** — `os_labels_equivalent`: rimossi separatori unicode morti e `rest.startswith(" ")` post-normalize.

## File

- `web/src/components/ui/CandidateList.vue`
- `web/src/components/ui/uiPrimitives.test.js`
- `docs/KNOWN_DEBT.md`
- `api/app/services/asset_identity.py` (solo cleanup morto)

## Fuori scope (post GO finale)

Merge → main, push tag `v0.10.16`/`v0.10.17`/`v0.10.18`, deploy, assert live, ripristino `test_oui_parse` (cantiere separato).
