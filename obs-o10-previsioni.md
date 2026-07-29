# OBS-UX O10 — previsioni (PRIMA del deploy)

## W0 — esito atteso e prova

**Atteso: (i)** — le tre correzioni O9-FIX sono nel CSS servito.

**Prova usata (eseguita):**
- `curl /api/health` → version api
- punto codice footer: `App.vue` `refreshRuntimeVersion()` → `api.health()` (runtime, non bundle)
- download `index.html` + `/assets/index-D5IEcFjC.css` serviti
- presenza in CSS servito di:
  - `.timeline-event[data-v-…]{min-width:0;max-width:100%;overflow:hidden;…}`
  - `.md-body{overflow-x:auto;…}`
  - `.md-body table{width:max-content;…}`

Se (ii): STOP, rideploy web only, non iniziare estetico.

## W0-bis

O9-FIX: catture viewport 900px = solo primo schermo; overflow X misurato via `docW` globale. O10 densità = **full-page**.

## W2 — densità (previsioni)

| Rotta | sezioni da collassare di default @390 | height full-page: prima (misura) | dopo (stima, non obiettivo) |
|---|---|---|---|
| `/oggi` | diagnostica secondaria / dettagli non-P1; card P1 restano aperte | ~13582 (O9) | stima: ridotta via collasso (misurare dopo) |
| `/plant` | dettagli porte non critiche | da misurare | stima: ridotta |
| `/inventory` | meta freschezza già inline; panel ok | da misurare | stima: lieve |
| `/monitoring` | drawer/campioni già scroll; filtri | da misurare | stima: lieve |
| `/timeline` | summary già ellissi+title | da misurare | stima: lieve |
| `/runbook` | sezioni md sotto fold / TOC collassabile | da misurare | stima: media |

Ogni collasso dichiara conteggio + priorità max (F-9).

## W3 — contrasto (previsioni)

Misurare PRIMA su elementi (b):
- inventory meta faint (`--inv-faint` / muted)
- monitoring muted labels
- timeline `.event-summary` muted + ellissi
- runbook md cell text

Target: WCAG 2.1 AA — 4.5:1 normale, 3:1 large. Rapporti prima/dopo misurati (non scelti a gusto).

## Difetti #4–#11

| # | azione prevista | motivo |
|---|---|---|
| 4 dossier provenance doppia | **correggere** via W1 | sintomo vocabolario |
| 5 inventory densità/leggibilità | **correggere** W2/W3 | (b) |
| 6 monitoring densità | **correggere** W2/W3 | (b) |
| 7 timeline ellissi | **correggere** W3 title/expand | (b) |
| 8 dashboard ready/live | **correggere** via W1 | sintomo vocabolario |
| 9 findings Salva H-scroll | **fixture test only** W5 | live vuoto, no fake prod |
| 10 incidents | **correggere** W4 dopo W1–W3 | (e) |
| 11 runbook trunc | **correggere** W3 | (b) |
| O9 plant@390 / oggi@390 densità | **correggere** in W2/W4 | già rinviati |

Favicon armonizzazione: **rinviata** (ondata successiva; scelta A bloccata).
