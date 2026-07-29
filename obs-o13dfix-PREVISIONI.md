# O13D-FIX — PREVISIONI (dichiarate prima del deploy / delle catture)

| id | previsione |
|----|------------|
| D0 20 file | 14 tracked (`git diff --stat` 487+/34−) + 6 untracked prodotto O13D: `color_literal_gate.py`, `test_o13d_soppressione.py`, `obs-o13cfix-redatto.md`, `obs-o13d-emissions-246.json`, `obs-o13d-c7-registro.md`, `obs-o13d-screenshot-harness.md` |
| D0 privacy.diff | ~80–150 righe (redatto.md + pointer `obs-o13cfix.md` + dichiarazione PNG binari esclusi dal testo diff) |
| D0 ui.diff | ~20–40 righe (`api.js`, `observatoryUx.js` — web/src non in novelty/color; Oggi/Incidents/Plant già in novelty/color) |
| D0 resto.diff | ~500–700 righe (`.gitignore`, meta già in O13D-meta dove serve ridichiarazione, gate script, test, c7, harness, emissions) — senza ridiffare novelty/color API |
| D0 aritmetica | copertura file = 100% dei 20; scarto vs solo `git diff --stat` atteso (untracked + ridichiarazioni tematiche) |
| D1 chiavi | presenti: `ADMIN_USER`, `ADMIN_PASSWORD`; esito atteso **non** STOP-CREDENZIALI-ASSENTI |
| D1 harness | O9 CDP / Playwright viewport+dsf=1; W×H distinti 1280/768/390; privacy-safe all'origine |
| D2 difetti | attesi alcuni (b) contrasto/troncamento e (d) su mobile; (a) pochi; (c)(e) rinviati enumerati |
| D2 correzioni | (a)(d) + (b) contrasto/troncamento in ondata; (c)(e) rinvio |
| D3 residui | allowlist 22 voci; risolvibili con token esistenti: **2–8** literal verdi non semantici → `--ok`; viola AI **senza token** → FERMO dichiarato (no inventare `--ai`) |
| D3 temi | atteso solo tema scuro fisso; `prefers-reduced-motion` se presente; no light/HC/print |
| D5 | baseline `in_costruzione`, coverage ≪ 3d, N5=0, soppressione `premature_baseline_protection` visibile |
| bump | **0.10.82** se cambia runtime (web/api); solo docs/diff/catture → nessun bump |
