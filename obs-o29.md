# OBS-O29 — OBS-MAPPA-RIALLINEAMENTO (0.10.95)

```
wave: O29
branch: feature/obs-currency
base_dichiarata: b251a43194f339fde4aa64ddecebce1b0c999ca2
tip_O28_confermato_0.1: 76fabaac65077e49e61175978c16df80174444fa
VERSION: 0.10.95 (web; api/health può restare 0.10.93/94 finché non rebuild api — atteso)
deploy: web only
esito: M gate → D solo Gs308 (a) · Topology (b)/(M4) · V color/contrast/evidence PASS · w8/drift SKIP
```

---

## 1. Elenco file toccati

| path | ruolo |
|------|--------|
| `web/src/views/Gs308.vue` | D1 letterali → token |
| `scripts/color_literal_gate.py` | rimossa allowlist Gs308 |
| `VERSION` / `web/package.json` / `CHANGELOG.md` | 0.10.95 |
| `docs/KNOWN_DEBT.md` | DEBT-COLOR-LITERAL-GATE-JS-CANVAS-GAP |
| `docs/obs-o29*` | M/V/report/catture |

**Topology.vue non modificato.** Nessun `api/app/**`.

---

## 2. Blocco 0.1 (integrale)

```
===== 0.1 git log --oneline -8 feature/obs-currency =====
76fabaa feat(observatory): O28 a11y dialogo disposition + chrome N=0 (0.10.94)
b251a43 docs(observatory): O27 chiusura UX lifecycle — test E1.2 + catture (no prodotto)
ffd85ae docs(observatory): report O26 (principale 3f9ab1f)
3f9ab1f feat(observatory): O26 Oggi lifecycle dispositions (0.10.93)
638d115 docs(observatory): report O25 (principale 4571e45)
4571e45 docs(observatory): O25 M0 discovery + P lifecycle policy (no D)
18d1489 docs(observatory): report O24 split disclosure (principale b6ae530)
b6ae530 feat(observatory): O24 Topology split A/B disclosure FDB (0.10.92)

===== git rev-parse HEAD =====
76fabaac65077e49e61175978c16df80174444fa

===== git fetch origin && git rev-parse origin/feature/obs-currency =====
76fabaac65077e49e61175978c16df80174444fa

===== HEAD == 76fabaac65077e49e61175978c16df80174444fa? =====
YES

===== tip O28 introduce D1-D5 (feat a11y)? =====
feat(observatory): O28 a11y dialogo disposition + chrome N=0 (0.10.94)

===== ancestor b251a43194f339fde4aa64ddecebce1b0c999ca2 (base O28)? =====
YES

===== HEAD == origin? =====
YES
```

GATE BLOCCO 0: **PASS**.

---

## 3. Fase M

### M1 — token di riferimento (`matrix.css`)

| token | hex |
|-------|-----|
| `--bg-0` | `#0f1319` |
| `--bg-1` | `#161b23` |
| `--bg-2` | `#1d242e` |
| `--border` / `--border-2` | `#262e3a` / `#323c4a` |
| `--text-1/2/3` | `#e8ebf0` / `#98a2b3` / `#667085` |
| `--ok` | `#4fb477` |
| `--attn` / `--warn` | `#d9a441` |
| `--alert` / `--danger` | `#e06b52` |
| `--accent` / `--data-out` | `#6bc5db` |
| `--data-in` | `#e0a048` |
| `--inference` | `#9b7bd4` |
| `--inference-fg` | `#c4a0ff` |
| `--inference-edge` | `#7656b0` |
| `--space-1…4` | `0.25/0.35/0.5/0.75rem` |

### M2 — verdi (Topology + GS308)

**Topology @1280 istanze greenish misurate:** `len=47` (quasi tutte path SVG `edge-fdb`/`edge-confirmed` con stroke `rgb(79,180,119)` = `--ok`).

Ruoli unici Topology (`len=7` asserito in `obs-o29-M.json`):

| id | computed | token | ruolo | cat |
|----|----------|-------|-------|-----|
| grid_bg | color-mix(--ok 3%) | `var(--ok)` | griglia decorativa | **(b)** |
| depth_border | color-mix(--ok 7%) | `var(--ok)` | colonna decorativa | **(b)** |
| edge_confirmed / fdb / inferred | `#4fb477` | `var(--ok)` | canale O19 + dash | **M4 exclude** |
| node_endpoint tint | color-mix(--ok 6%) | `var(--ok)` | superficie endpoint | **(b)** dubbio |
| zoom ± | text-2/border | — | **non verde** | n/a |

**Nessuno slider verde** — controlli zoom = bottoni `.ghost`.

**GS308 categoria (a)** `len=5` famiglie:

| letterale | ruolo | fix |
|-----------|-------|-----|
| `rgba(60,140,90,*)` | superfici ok | `color-mix(var(--ok))` |
| `var(--ok,#6ecf8f)` | fallback estraneo | `var(--ok)` |
| `#9ab0e0` / `rgba(100,120,180,*)` | infer/proposta | `--inference*` |
| `var(--warn,#d4b85a)` | warn fallback | `var(--warn)` |
| `var(--muted,#999/#aaa)` | muted fallback | `var(--muted)` |

Fonte CSS (gate); nessun fillStyle JS su Topology/GS308. MatrixRain già tokenizzato (gap gate JS registrato come debito).

### M3 — layout misurato

Screenshot PRE condivisi (obs-exchange): `obs-o29-m-topology-b{closed,open}-{1280,768,390}.png`, `obs-o29-m-gs308-1280.png`, `obs-o29-M.json`.

- `negative_margins=[]` sempre.
- «Overlap» stage↔list/unresolved: **artefatto** `position:absolute` del canvas (bbox alto) vs flusso sotto; a 768 (lista sopra, scroll sotto) `overlaps=[]`.
- Overflow stage w>viewport: **scroll orizzontale intenzionale**.
- **Nessun D2 layout** (nessun (a) oggettivo).

### M4 — esclusioni

- Tratti confirmed/fdb/inferred: tutti `--ok` + dash O19 — **non toccare**.
- `--inference` / `--inference-edge`: non usati come fill tratti Topology — **non toccare**.
- Disclosure A/B O24: struttura invariata.

### GATE M

- **(a) → D:** solo Gs308 letterali.
- **(b):** griglia/depth/endpoint tint Topology su `--ok` (domanda sotto).
- Layout: nessuno (a).

---

## 4. D — correzioni (a)

Solo `Gs308.vue` + rimozione allowlist gate.

| prima | dopo |
|-------|------|
| `rgba(60,140,90,0.18)` fact bg | `color-mix(in srgb, var(--ok) 18%, transparent)` |
| `color: var(--ok, #6ecf8f)` | `color: var(--ok)` |
| `#9ab0e0` infer fg | `var(--inference-fg)` |
| `rgba(100,120,180,*)` infer/proposta | `color-mix(… var(--inference) …)` |
| fallback warn/muted | `var(--warn)` / `var(--muted)` |
| bordi `rgba(255,255,255,*)` | `var(--border)` |
| input `rgba(0,0,0,0.25)` | `var(--bg-0)` |

D2 layout: nessuna. D3 JS canvas Topology: nessuno. D4/D5 rispettati.

POST misurato: `.tag.fact` color `rgb(79,180,119)`; `.tag.infer` color `rgb(196,160,255)` (=`--inference-fg`).

---

## 5. Reperti (b) — domanda per Michele

**Griglia Topology e tint colonne/endpoint usano `--ok` (verde stato) come decorazione neutra.**

| Alternativa | Conseguenza |
|-------------|-------------|
| A — lasciare `--ok` (status quo) | Coerente col tratto confirmed; griglia “tinta rete ok”; rischio: verde stato = decorazione |
| B — passare a `--border` / `--text-3` mix | Griglia neutra; tratti restano `--ok`; allinea “decorazione ≠ stato” |
| C — nuovo token `--grid-line` | Solo se si vuole una voce dedicata (non richiesto ora) |

**Nessuna applicata in O29.**

---

## 6. V1–V5

### V1
- Topology template: **invariato**.
- Gs308 template: **invariato** (solo `<style>`).
- Nessuna rimozione controlli/dati.

### V2 POST (share)
| file | WxH | sha256 |
|------|-----|--------|
| `obs-o29-v-topology-bclosed-1280.png` | 1280×4136 | `ec70e393…d957` |
| `obs-o29-v-topology-bclosed-768.png` | 768×4847 | `f93e2aec…633d2` |
| `obs-o29-v-topology-bclosed-390.png` | 390×7275 | `8bf1103d…cb86b` |
| `obs-o29-v-topology-bopen-1280.png` | 1280×7390 | `0f0a36b0…0198` |
| `obs-o29-v-topology-bopen-768.png` | 768×8101 | `6f121aca…da80` |
| `obs-o29-v-topology-bopen-390.png` | 390×10528 | `5f441d54…cfca8` |
| `obs-o29-v-gs308-1280.png` | 1280×1666 | `19c462b4…87f49` |

### V3
Nessun token tratto Topology toccato → **tabella O19/O20 non ripetuta**.

### V4 gate
- `color_literal_gate --self-test` PASS; gate PASS; `allowlist_count=15` (−1 Gs308).
- `contrast_gate --self-test` PASS; gate PASS (TEMP `--text-3` preesistente).
- `evidence_gate` PASS (regressione; no --self-test: vocabolario non toccato).
- **w8/drift SKIP** — nessun file backend.

### V5
`o9_png_assert.py --pair` PASS su 4 coppie topology V2.

---

## 7. Debiti

- **Nuovo:** `DEBT-COLOR-LITERAL-GATE-JS-CANVAS-GAP` (gate non scansiona JS canvas).
- Topology (b) griglia: domanda aperta, non debito codice.

---

## 8. Fase G

- G1: 0.10.95  
- G2: `./scripts/deploy.sh web` — api non serve  
- G3: `/assets/index-CVzNuM8H.js`; `has_old_6ecf=false`, `has_old_9ab0=false`, `has_inference_fg=true`  
- G4: catture V sopra  
- G5: commit principale (hash sotto; tip report non autocertifica)  
- G6: `/tmp/o29_m_capture.py`, `/tmp/o29_v_capture.py` rimossi  

---

## 9. Cosa NON hai fatto

- Nessuna modifica Topology CSS/layout.
- Nessun cambio `--inference` / `--inference-edge` valori.
- Nessun backend/deploy api; w8/drift; nuova funzione/pannello.
- Nessuna decisione (b) sulla griglia.
- Nessun `/ai`.
