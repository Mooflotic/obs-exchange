# OBS-O30 — OBS-COLORE-OMOGENEITA (0.10.96)

```
wave: O30
branch: feature/obs-currency
base_dichiarata: 5e72dd23d436ec3fef2f7b0ba2555116124502f5
VERSION: 0.10.96 (web)
deploy: ./scripts/deploy.sh web (api non richiesto)
```

---

## 1. File toccati

| Path | Ruolo |
|------|--------|
| `docs/COLOR_SEMANTICS.md` | M1 registro semantico |
| `docs/obs-o30-M.json` | artefatto M |
| `docs/obs-o30.md` | questo report |
| `docs/obs-o30-b0.txt` | Blocco 0.1 |
| `docs/obs-o30-V2-captures.json` | meta catture |
| `docs/obs-o30-{pre,v}-topology-*.png` | V2 PRE/POST Topology |
| `docs/KNOWN_DEBT.md` | debiti O30 + canvas gap |
| `CHANGELOG.md`, `VERSION`, `web/package.json` | bump 0.10.96 |
| `scripts/color_literal_gate.py` | allowlist 15→2 |
| `web/src/views/Topology.vue` | D1 Michele B |
| `web/src/views/{Actions,Dashboard,Dossier,Inventory,Monitoring,Oggi,Suggestions,Timeline}.vue` | D2 letterali→token |
| `web/src/components/{AssetHabits,Branch308Card,CalibrationBadge,SensorHealth,SpanSensorCard}.vue` | D2 |

---

## 2. Blocco 0.1 (integrale)

```
===== 0.1 git log --oneline -8 feature/obs-currency =====
5e72dd2 feat(observatory): O29 GS308 token realign + mappa inventory (0.10.95)
76fabaa feat(observatory): O28 a11y dialogo disposition + chrome N=0 (0.10.94)
b251a43 docs(observatory): O27 chiusura UX lifecycle — test E1.2 + catture (no prodotto)
ffd85ae docs(observatory): report O26 (principale 3f9ab1f)
3f9ab1f feat(observatory): O26 Oggi lifecycle dispositions (0.10.93)
638d115 docs(observatory): report O25 (principale 4571e45)
4571e45 docs(observatory): O25 M0 discovery + P lifecycle policy (no D)
18d1489 docs(observatory): report O24 split disclosure (principale b6ae530)

===== git rev-parse HEAD =====
5e72dd23d436ec3fef2f7b0ba2555116124502f5

===== git fetch origin && git rev-parse origin/feature/obs-currency =====
5e72dd23d436ec3fef2f7b0ba2555116124502f5

===== HEAD == 5e72dd23d436ec3fef2f7b0ba2555116124502f5? =====
YES

===== HEAD == origin? =====
YES
```

GATE BLOCCO 0: PASS. (O29-FIX senza commit — tip resta O29.)

---

## 3. Fase M

### M1 — `docs/COLOR_SEMANTICS.md`

Registro canonico (ruolo + esempio): `--bg-0/1/2`, `--border*`, `--text-1/2/3`, `--ok`, `--attn`/`--warn`, `--alert`/`--danger`, `--accent`/`--data-out`, `--data-in`, `--inference*`, `--space-1…4`, plus badge/drawer già in matrix. Nessun token nuovo.

### M2 — allowlist enumerata (`len=15` pre-D)

| i | file | class | azione |
|---|------|-------|--------|
| 1–3,5–12,14–15 | AssetHabits…Timeline (13) | `candidate_resolve_gs308_schema` | D2 |
| 4 | MatrixRain.vue | intentional (canvas template rgba) | keep |
| 13 | Plant.vue | (b) categorical | keep |

`assert len(ALLOWLIST_pre)==15`.

### M3 — letterali sito intero

Gate scansiona tutto `web/src` (`SCAN_SUFFIXES`). Pre-D: PASS, letterali solo in allowlist. Nessun FAIL fuori allowlist → **già pulito** oltre allowlist.

### M4 — coerenza di ruolo

| cat | reperto |
|-----|---------|
| **(a)** | Topology `grid_bg` / `depth_border` / `endpoint` tint su `--ok` decorativo → D1 |
| **(b)** | MatrixRain `--ok` ambient cyber; Plant hex categoriali ruoli |
| ok_aligned | ToggleSwitch ON=`--ok` |

### M5 → D1

Decisione Michele **B** (già nota O29): griglia/depth/endpoint → `--border`/`--text-3`; `edge-confirmed` resta `--ok`.

Artefatto: `docs/obs-o30-M.json` (hash proprio pre-D).

---

## 4. Fase D — prima/dopo

### D1 Topology (Michele B)

| selettore | prima | dopo |
|-----------|-------|------|
| `.topology-scroll` grid | `var(--ok) 3%` | `var(--border) 55%` |
| `.depth-column` border | `var(--ok) 7%` | `var(--border) 70%` |
| `.network-node.endpoint` | `var(--ok) 6%` | `var(--text-3) 10%` |
| `.edge-confirmed` stroke | `var(--ok)` | **invariato** |

### D2 allowlist 13 file (schema GS308)

Esempi:

- `Branch308Card`: `rgba(60,140,90,0.18)` → `color-mix(… var(--ok) 18%)`; `#9ab0e0` → `var(--inference-fg)`; `var(--muted,#aaa)` → `var(--text-3)`.
- `Actions`: `rgba(61,255,138,0.12)` glow → `color-mix(… var(--ok) 12%)`; fondo banner → `var(--bg-0)`.
- `Dossier`: chip/fallback letterali → token; `rgb(from var(--inference)…)` → `color-mix(… var(--inference) …)` (gate vede `rgb()`).

Allowlist post: **2** — MatrixRain, Plant.

### D3

Assorbito in D2 (letterali = hit allowlist).

### D4 (a)

Solo Topology (D1). Nessun altro (a).

### D5–D6

Nessuna nuova funzione/token. `--inference` fill e `--inference-edge` invariati (contrast_gate).

---

## 5. Reperti (b) — domanda fattuale (nessuna applicazione)

1. **MatrixRain** usa `--ok` per pioggia ambient. Alternative: (A) lasciare (prodotto cyber); (B) nuovo token ambient; (C) `--text-3`/`--border` (perde “verde matrix”). **Non applicato.**
2. **Plant** hex per ruoli AP/switch/… Alternative: (A) lasciare + debito; (B) famiglia `--plant-role-*`; (C) comprimere su `--ok`/`--attn` (perde distinzione). **Non applicato** → `DEBT-O30-PLANT-CATEGORICAL-HUES`.

---

## 6. Fase V

### V1 — stringhe informative

14 file template toccati: set token testuali template PRE==POST. `len=14`, `all_equal=True`. Solo colore in `<style>`.

### V2 — catture Topology (unica rotta con Δ visivo D1)

PRE = copia O29-V Topology (CSS Topology invariato in O29 D). POST = deployed post-O30.

| file | W×H | sha256 |
|------|-----|--------|
| `obs-o30-pre-topology-bclosed-1280.png` | 1280×4136 | `ec70e3937aff80fbfd534ceb92d8731ffcde6baaf8966765e2162c924310d957` |
| `obs-o30-pre-topology-bclosed-768.png` | 768×4847 | `f93e2aec518ee407c777d1cb4e43114fccbce5ee60e4b6973ac64ce0317633d2` |
| `obs-o30-pre-topology-bclosed-390.png` | 390×7275 | `8bf1103d9629e24a441905a5794d4226efe8704d3ebf4c3b466602b399bcb86b` |
| `obs-o30-pre-topology-bopen-1280.png` | 1280×7390 | `0f0a36b0bb89bdffbec5f63412351d500d0472fa5294c128e6070d6aee030198` |
| `obs-o30-pre-topology-bopen-768.png` | 768×8101 | `6f121aca4e9d9655bfd8e5a42fce103d656628d02d8950c95da9e602c683da80` |
| `obs-o30-pre-topology-bopen-390.png` | 390×10528 | `5f441d5494269379280e7b471f29fd719c12812dc0a0db9a0f7f2166a38cfca8` |
| `obs-o30-v-topology-bclosed-1280.png` | 1280×4464 | `99fec593e2422de33ac241f5002193a9aba655853cad4fe9f32ec421a05e56b4` |
| `obs-o30-v-topology-bclosed-768.png` | 768×5171 | `799ad88106c78af368b245e4b19f9f3e58208e2cc26ea1e6f05bf63d99cb2096` |
| `obs-o30-v-topology-bclosed-390.png` | 390×7708 | `e5d4a3865290bbc4757adf0bc60f304e6509657cf9a5dac75632de3d8115ae38` |
| `obs-o30-v-topology-bopen-1280.png` | 1280×7461 | `bf9ba9858b60ba2268d74c36d3a09d77587ac705262df0260aa98c62910997bc` |
| `obs-o30-v-topology-bopen-768.png` | 768×8168 | `895a0e6fc6fd065ebdbd56a3cc3f2cec623d4ad149d8d2504f2ee70d10095434` |
| `obs-o30-v-topology-bopen-390.png` | 390×9227 | `12a6fa2e91a1192aa27760f7a8c510ae644939aced80d8e7a8b3cfd5f4b97f40` |

`len(png)=12`. Auth: session mint TTL 180s (token non pubblicato). Altezze PRE/POST possono divergere per drift census API (`DEBT-TOPOLOGY-API-NONIDEMPOTENT`) — non criterio colore.

Altre rotte D2: solo token CSS; nessuna cattura extra (Δ non layout).

### V3 — proprietà O19/O20

**Non serve:** `--inference` / `--inference-edge` non ritoccati; archi confirmed restano `--ok`.

### V4 — gate (integrale)

**color_literal_gate --self-test**
```
SELFTEST vue inject detected: (2, '#ff00aa', '.x { color: #ff00aa; /* O13D_COLOR_GATE_INJECT */ }')
SELFTEST matrix rule inject detected: (956, '#ff00aa', '.o14fix-gate-inject { color: #ff00aa; /* O14FIX_COLOR_GATE_INJECT */ }')
SELFTEST PASS: inject fails (vue+matrix rule), remove passes
```

**color_literal_gate**
```
PASS: no hard-coded color literals outside allowlist; matrix.css decls-only
  token_file=assets/matrix.css (literals only in --custom-property decls)
  allowlist_count=2
```

**contrast_gate --self-test**
```
SELFTEST inject detected: {'fg': '--inference-edge', 'bg': '--bg-1', 'fg_hex': '#220033', 'bg_hex': '#161b23', 'ratio': 1.089, 'threshold': 3.0, 'fonte': 'WCAG 2.2 SC 1.4.11 Non-text Contrast AA', 'ruolo': 'non_text', 'pass': False}
SELFTEST PASS: inject fails, remove passes
```

**contrast_gate**
```
=== contrast_gate ===
token_file=web/src/assets/matrix.css
pairs_checked=9
allowlist_entries=1
  PASS --text-1=#e8ebf0 on --bg-0=#0f1319 ratio=15.586 thr=4.5 [text_normal] WCAG 2.2 SC 1.4.3 Contrast (Minimum) AA testo normale
  PASS --text-2=#98a2b3 on --bg-0=#0f1319 ratio=7.232 thr=4.5 [text_normal] WCAG 2.2 SC 1.4.3 Contrast (Minimum) AA testo normale
  FAIL --text-3=#667085 on --bg-0=#0f1319 ratio=3.744 thr=4.5 [text_normal] WCAG 2.2 SC 1.4.3 Contrast (Minimum) AA testo normale
  PASS --ok=#4fb477 on --bg-0=#0f1319 ratio=7.208 thr=3.0 [non_text] WCAG 2.2 SC 1.4.11 Non-text Contrast AA
  PASS --warn=#d9a441 on --bg-0=#0f1319 ratio=8.281 thr=3.0 [non_text] WCAG 2.2 SC 1.4.11 Non-text Contrast AA
  PASS --danger=#e06b52 on --bg-0=#0f1319 ratio=5.671 thr=3.0 [non_text] WCAG 2.2 SC 1.4.11 Non-text Contrast AA
  PASS --inference=#9b7bd4 on --bg-0=#0f1319 ratio=5.479 thr=3.0 [non_text] WCAG 2.2 SC 1.4.11 Non-text Contrast AA (riempimento; non toccare in O20)
  PASS --inference-edge=#7656b0 on --bg-1=#161b23 ratio=3.068 thr=3.0 [non_text] WCAG 2.2 SC 1.4.11 Non-text Contrast AA
  PASS --inference-edge=#7656b0 on --bg-0=#0f1319 ratio=3.307 thr=3.0 [non_text] WCAG 2.2 SC 1.4.11 Non-text Contrast AA
ALLOWLISTED_FAILS=1
  TEMP --text-3 on --bg-0 ratio=3.744 debt=DEBT-NO-CONTRAST-PRESIDIO | testo terziario mute (#667085) spesso <4.5:1 su bg-0; etichette via/odm già in DEBT-NO-CONTRAST-PRES
PASS: contrast pairs within threshold or allowlisted with debt
```

**evidence_gate** (regressione; vocabolario non toccato)
```
=== evidence_gate ===
forbidden_ownership_terms=4
  /collegato\s+a/ — asserisce ownership di link; FDB prova solo passaggio MAC (I5 rango 60)
  /attaccat[oa]\s+a/ — sinonimo ownership fisico; vietato su FDB
  /assegnat[oa]\s+(alla|alla porta|a porta)/ — asserisce assegnazione porta; FDB non è LLDP/manual
  /appartiene\s+a/ — asserisce appartenenza; FDB non è identità
i2_conditions=['sorgente_non_disponibile', 'dispositivo_assente', 'misurato_a_zero', 'disabilitato_dall_operatore', 'limite_strutturale']
ownership_hits=0
marker_errors=0
i2_placeholder_errors=0
PASS: no FDB+ownership vocabulary; required evidence markers present; I2 placeholders declared
```

**w8/drift:** SKIP — nessun file backend toccato (come O28/O29).

**Allowlist finale (`len=2`):**
1. `components/MatrixRain.vue` — canvas rgba da token (DEBT-COLOR-LITERAL-GATE-JS-CANVAS-GAP)
2. `views/Plant.vue` — hue categoriali (b) / DEBT-O30-PLANT-CATEGORICAL-HUES

Eccezioni contrasto: `--text-3` TEMP debitata; `wp_gate` non toccato.

### V5 — `o9_png_assert.py --pair`

4 coppie POST breakpoint distinti: bclosed 1280×768, 1280×390; bopen 1280×768, 1280×390 → **PASS** tutte.

---

## 7. Debiti

| debito | stato |
|--------|--------|
| Allowlist 13 candidate | **chiuso** (tokenizzati) |
| `DEBT-COLOR-LITERAL-GATE-JS-CANVAS-GAP` | aperto (MatrixRain; O30 nota allowlist=2) |
| `DEBT-O30-PLANT-CATEGORICAL-HUES` | **aperto** (b) |
| `DEBT-NO-CONTRAST-PRESIDIO` (`--text-3`) | invariato |
| Gap JS letterali | nessun nuovo letterale JS/canvas fuori scope oltre debito già noto |

---

## 8. Fase G

- **G1** VERSION web `0.10.96`
- **G2** `./scripts/deploy.sh web` → ok; **api non necessario**
- **G3** assets `index-DX8TQyxB.js` / `index-knOJnpXT.css`; `0.10.96` in JS; `has_old_ok_grid_3pct=false`, `has_old_ok_depth_7pct=false`; endpoint=`color-mix(…var(--text-3) 10%,…)`; `edge-confirmed` stroke `--ok`; `has_old_rgba_60_140_90=false`, `has_old_9ab0e0=false`; unico `#6ecf8f` = fallback Plant allowlist
- **G4** catture V2 = post-deploy (stessa sessione)
- **G5** commit hash sotto (tip report non autocertifica — O31 Blocco 0.1)
- **G6** one-shot solo `/tmp/o30_v_capture.py` (non in git); `git ls-files` senza script o30 one-shot

---

## 9. Hash commit principale

_(compitato in G5 — vedi `git log -1` dopo push)_

---

## 10. Cosa NON ho fatto

- Nessun deploy api; nessun tocco `api/app/facts/`, T7, OBS-CURRENCY, FA251, FDB vocab, O15, disclosure A/B logica, layout posizioni, `--inference` fill / `--inference-edge` valori
- Nessun token nuovo (`--grid-line` no)
- Nessuna correzione Plant/MatrixRain (b)
- Nessuna cattura extra rotte D2-only
- Nessun main/merge/tag/force
