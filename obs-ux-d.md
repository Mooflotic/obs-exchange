<!-- BLOCK-ID: OBS-UX-D -->

# OBS-UX — Ondata D (0.10.37)

**Tag:** `v0.10.37` = `a53c660` · Live health `0.10.37`

## Boot

| Boot | Esito |
|------|-------|
| 1 post-deploy | T_total=93.371s needs_apply=true T_backup=83.42s (apply strutturale) |
| 2 restart | **PASS regime** T_total=**8.971**s needs_apply=false T_backup=0 |

Conti: assets 151 · name_proposals 412 · AD 82 · ip_current 100 · observations assente.

## Assert

| Assert | Esito |
|--------|-------|
| D-a nessun dump JSON grezzo dal Dossier | PASS — toggle tecnico rimosso; sintesi contestuale |
| D-b CU «cos’è» / «nome affidabile» | PASS — Sintesi identità (saputo/fonti/fresco/incerto/manca) |
| `?technical=1` API | KEEP secondario (score/grezzo), non esposto UI |
