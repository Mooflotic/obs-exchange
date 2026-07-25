# OBS-PORTALE — Ondata 2 (0.10.32)

**Tag:** `v0.10.32` = `f534536` · live health `0.10.32`

## Criteri

| Decisione | Criterio |
|----------|----------|
| OUI floor | NameProposal OUI solo se conf ≥ **0.7** (= floor VENDOR_HINTS). Raw IEEE 0.4 escluso: 2 pending deboli + 1 Unknown@0.6 archiviati. |
| SSDP | Banner ≠ nome; strip `Host UPnP/…` → host; altrimenti archivia. |
| Digit-run | **0** hit sui nomi attuali → regex `triageRules.js` **invariata**. |
| OS equiv | Solo troncamento nmap (`rest` `^-\d`); no edition upgrade. |
| Sky | Nomi adottati **invariati**; `name_ambiguity` in API/UI; OUI bare collidenti senza IP → archivio `oui_bare_ambiguous`. |

## Gate equivalenza (PRIMA → DOPO)

- **Nomi adottati modificati: 0** (W6 PASS)
- NP: 0 added/removed, **17** changed (tutte enumerate sotto)
- ssdp pending: **10 → 4** (previsto: 4 Fritz strip + 6 banner archive)
- oui pending conf&lt;0.7: **3 → 0**

### Differenze NP

| id | asset | delta |
|----|-------|-------|
| 4 | 2 | oui Switch Linksys 0.4 → archived `oui_below_min_conf` |
| 116–119 | 24/22/21/23 | ssdp Fritz-* UPnP… → `Fritz-*` pending `ssdp_banner_stripped` |
| 126 | 47 | KnOS… → archived `ssdp_banner_not_name` |
| 139 | 47 | GP Electronics 0.4 → archived |
| 366,369,389,391 | 136/137/149/150 | oui Sky bare → archived `oui_bare_ambiguous` |
| 367,368,383,386,394 | … | MR/GW/Linux SSDP banners → archived |
| 388 | 89 | oui Unknown 0.6 → archived |

### Casi limite SSDP (nessun legittimo perso)

- `Fritz-Cucina UPnP/…` → **tenuto** come `Fritz-Cucina`
- `MR-Device` / `GW-Device` / `KnOS` / `Linux/…SDK` → archivio
- `LivingRoom-TV` / hostname corto senza UPnP → tenuto (test)

## Assert

| ID | Esito | Evidenza |
|----|-------|----------|
| W1 | PASS | health 0.10.32 |
| W2 | PASS | regime T_total=**8.897**s needs_apply=false T_backup=0 |
| W5 | PASS | ssdp pending 10→4; Fritz legittimi preservati |
| W6 | PASS | 0 cambi nome adottato |

Primo boot post-deploy: structural=1 / T_backup≈82s (una tantum). Curl health+web 200.
