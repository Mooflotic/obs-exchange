# OBS-OUI-TEST-RESTORE-DIFF-029

## Summary

Ripristina `test_oui_parse_ieee_and_lookup` in `tests/test_asset_identity.py` com’era a `main` @ 0.10.15 (`673b50b`): parse IEEE (hex + base16 + commenti + tab) → `upsert_oui` → `lookup_oui_vendor` su MAC completo con `reliable=True`.

Import già presenti su main post-028; nessun adattamento necessario. Nessun bump VERSION / nessun deploy.

## Suite

`pytest observatory/tests/test_asset_identity.py` → **16 passed**.

## Commit collaterale (stesso branch)

Documentazione: `DEBT-MANUAL-CONF-BAR` in `KNOWN_DEBT.md`; regola igiene assert in `docs/RELEASE_CHECKLIST.md` §7 (+ puntatore in header `scripts/deploy.sh`).

## Base

`main` post OBS-028. Fingerbank 027 non toccato.

**STOP:** merge/push main solo dopo GO.
