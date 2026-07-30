# Color semantics — LAN Observatory

Registro canonico dei token di colore. Un token ha un **ruolo semantico stabile**:
usarlo per un ruolo diverso è incoerenza funzionale, non solo estetica.

Fonte valori: `web/src/assets/matrix.css` (OBS-DESIGN-SPEC-025 + ondate successive).
Metro di paragone per audit di coerenza (O30+).

| Token | Hex / valore | Ruolo semantico | Esempio già in codice |
|-------|--------------|-----------------|------------------------|
| `--bg-0` | `#0f1319` | Superficie di pagina / fondo primario | `body { background: var(--bg-0) }` (`matrix.css`) |
| `--bg-1` | `#161b23` | Pannello / card elevata | `.topology-list__row { background: var(--bg-1) }` |
| `--bg-2` | `#1d242e` | Superficie ulteriormente elevata | alias `--bg-elev` |
| `--border` | `#262e3a` | Cornice / struttura **neutra** (non stato) | bordi card, input, griglia decorativa (O30) |
| `--border-2` | `#323c4a` | Cornice secondaria più marcata | `--data-idle` affine |
| `--text-1` | `#e8ebf0` | Testo primario | `body { color: var(--text-1) }` |
| `--text-2` | `#98a2b3` | Testo secondario / muted leggibile | `.oggi-closed-signal a`, hint dialog |
| `--text-3` | `#667085` | Testo terziario / decorazione muted (contrasto spesso &lt;4.5:1 — vedi debito) | etichette uppercase lista Topology |
| `--ok` | `#4fb477` | **Stato positivo / confermato / sano** | `.badge.ok`, `edge-confirmed` stroke, SaveIndicator saved |
| `--attn` / `--warn` | `#d9a441` | Attenzione / warning (non critico) | `.badge.warn`, CalibrationBadge |
| `--alert` / `--danger` | `#e06b52` | Critico / errore / down | `.error`, `.badge.danger`, ViewStateBanner error |
| `--accent` / `--data-out` | `#6bc5db` | Accento UI / flusso dati out (non stato ok) | link `a`, gateway highlight |
| `--data-in` | `#e0a048` | Flusso dati in (temperatura calda) | sparklines / data chrome |
| `--inference` | `#9b7bd4` | **Contenuto derivato da IA** (fill) — mai fatto | blocco INFERENZA Dossier |
| `--inference-fg` | `#c4a0ff` | Testo/etichetta su superficie inference | `.tag.infer` Gs308 |
| `--inference-edge` | `#7656b0` | Bordo non-testo inference (≥3:1) — **non ritoccare** | archi/edge inference dove previsto |
| `--space-1…4` | `0.25–0.75rem` | Scala spaziatura densità (O17) | gap/padding componenti densità |
| `--badge-warn-border` | `#6a5520` | Bordo badge warning | `.badge.warn` |
| `--attn-ring` | `rgba(230,195,92,0.45)` | Alone/glow attenzione | CalibrationBadge dot |
| `--drawer-backdrop` | `rgba(0,0,0,0.45)` | Overlay drawer | Inventory drawer |
| `--drawer-shadow` | `rgba(0,0,0,0.5)` | Ombra drawer | Inventory |

## Vietato (funzionale)

- Usare `--ok` per decorazione senza stato (griglia, cornici neutre) → usare `--border` / `--text-3`.
- Usare `--inference*` per fatti osservati o chrome generico.
- Inventare letterali hex/rgba al posto di un token già con quel ruolo.

## Eccezioni debitate

- `--text-3` su `--bg-0` &lt;4.5:1 testo normale → `DEBT-NO-CONTRAST-PRESIDIO` (non “risolvere” alzando il token qui senza ondata contrasto).
- Canvas `fillStyle` runtime → `DEBT-COLOR-LITERAL-GATE-JS-CANVAS-GAP`; MatrixRain legge `--ok`/`--bg-0` a runtime.
