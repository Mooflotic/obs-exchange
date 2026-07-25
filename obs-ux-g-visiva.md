<!-- BLOCK-ID: OBS-UX-G-VISIVA -->

# OBS-UX — Fase G: revisione visiva

**Data:** 2026-07-25 · **Branch:** `feature/obs-ux` · **Baseline codice:** 0.10.40 (fix CSS post-ispezione)  
**Metodo:** ispezione statica CSS/componenti — **nessuno screenshot live** (tooling browser non disponibile in questo ambiente).

---

## Dichiarazione metodo

Non è stato possibile catturare screenshot reali su Cassiopea. La revisione segue:

1. Lettura `matrix.css` e stili scoped delle viste elencate.
2. Verifica presenza `ViewStateBanner` e pattern truncate/overflow.
3. Contrasto token OBS-DESIGN-SPEC-025 (`--text-*` su `--bg-*`).
4. Responsive `@media (max-width: 800px)` e `(max-width: 640px)`.

---

## Esito per vista

| Vista / componente | Truncate / overflow | Stati UI | Contrasto / token | Spacing / layout | Note |
|--------------------|---------------------|----------|-------------------|------------------|------|
| **Oggi** | OK — `.oggi-grid-main { min-width: 0 }`, azioni `flex-wrap`, card problema `max-width: 16rem` | OK — loading/empty/error/partial via `ViewStateBanner` | OK — token `--text-*`, `--border` | OK — sezioni 1.25rem, bottoni 12px | Anteprima rumore N=41 espandibile; molte azioni ghost su card dense |
| **Inventory** | OK — righe con ellipsis, pannello drawer scroll | OK — error/loading/empty (F) | OK — skin `--inv-*` alias token | OK — densità alta coerente | Dialog: aria-modal presente; focus trap parziale (debito a11y residuo) |
| **Plant** | OK — nomi porta `.dev` con ellipsis | OK — error/loading/empty/partial | OK | OK — griglia porte `minmax(68px)` | GS308: banner citazioni verso Topologia/Monitor |
| **Topology** | OK — `.node-copy strong/small` ellipsis | OK — error/loading/partial/stale | **Residuo** — canvas ancora palette verde legacy (`#07110c`, `#0f1a13`, edge `#318c54`) vs blu-ardesia globale | OK — scrollport `clamp(480px, 68vh, 900px)` | Non bloccante; allineamento token previsto in cantiere grafico dedicato |
| **Monitoring** | OK — `.truncate` + `:title` su nome/target | OK — error/loading/partial | OK | OK — tab sezioni, drawer | Hint SNMP GS308 non inventa dati |
| **Dossier** | OK — titolo head, TOC sticky | OK — hub + scheda error/loading | OK | OK — max-width 980px, TOC blur | Sintesi identità (D) al posto dump JSON |
| **Branch308Card** | OK — liste endpoint flex-wrap | N/A (sezione) | OK — tag Fatto/Inferenza/Da confermare leggibili | OK — block spacing 0.85rem | Copy `.3.20` «da confermare» (E) |
| **AiConsole** | OK — risposta `pre-wrap` | OK — loading + partial se AI off | OK — `AiInferenceLabel` | OK | Disclaimer inferenza visibile |
| **Findings** | OK — titolo `.truncate` 16rem | OK — error/loading; **empty** implicito (tabella vuota senza banner) | OK | OK — `.table-scroll-x` 72vh | Stato empty tabella: debole (solo assenza righe) |

---

## Anomalie trovate e fix applicati (→ 0.10.40)

| ID | Gravità | Descrizione | Fix |
|----|---------|-------------|-----|
| G-1 | **Alta** | `@media (max-width:800px)` — `.workspace { height: calc(100% - auto) }` **CSS invalido** (ignorato dal browser) | `grid-template-rows: auto 1fr` su `.app-shell`; `.workspace { min-height: 0 }` |
| G-2 | Media | Superfici concentrazione dati (`callout`, `seen-meta`, `ai-answer`, `md-body pre/code`, `.topo`) usavano verde legacy `#0a140e` / `#07110c` fuori spec blu-ardesia | Sostituiti con `var(--bg-0|1|2)`, `var(--border)`, `var(--data-idle)` in `matrix.css` |
| G-3 | Bassa | Fallback `@supports not backdrop-filter` card `#0a120c` | `var(--bg-1)` |

**Non fixato in codice (documentato):**

- **G-4** Topologia canvas — palette verde Matrix storica in `Topology.vue` scoped CSS (~15 hex hardcoded). Coerente col grafo ma disallineata dal resto; proposta in `obs-ux-proposte.md`.
- **G-5** Findings — nessun `ViewStateBanner kind=empty` quando tabella vuota (WEAK in misura 1.2).
- **G-6** Toggle Inventario/Dossier senza `role=switch` completo (debito a11y da misura 1.5).

---

## Contrasto matrix.css (token)

| Coppia | Ratio stimato | Esito |
|--------|---------------|-------|
| `--text-1` (#e8ebf0) su `--bg-0` (#0f1319) | ~14:1 | OK |
| `--text-2` (#98a2b3) su `--bg-1` (#161b23) | ~7:1 | OK |
| `--text-3` (#667085) su `--bg-0` | ~4.5:1 | OK per meta/secondario |
| `--accent` (#6bc5db) su `--bg-0` | ~8:1 | OK link/attivo |
| `--alert` (#e06b52) su `--bg-1` | ~5:1 | OK errori |

Nessun testo primario usa opacità al posto dei livelli `--text-*` (conforme spec).

---

## Verdetto fase G

**PASS con riserve.** Nessuna anomalia bloccante in ispezione statica post-fix 0.10.40. Residuo visivo principale: canvas Topologia verde vs tema blu-ardesia (non funzionale).
