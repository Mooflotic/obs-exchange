# O14-FIX — PREVISIONI (dichiarate prima del deploy)

| id | previsione |
|----|------------|
| Literal in `matrix.css` fuori da custom property | **30 occorrenze** / **18 valori unici** (9 O14 inference/AP + badge/shadow/drawer/scanline preesistenti) |
| Nomi semantici proposti | `--inference-fg`, `--inference-fg-soft`, `--inference-edge`, `--inference-well-bg`, `--inference-badge`, `--inference-badge-fg`, `--ap-border`, `--group-border`, `--group-bg`; badge `--badge-warn-border`, `--badge-danger-border`; `--attn-ring`; `--drawer-backdrop`, `--drawer-shadow`, `--helptip-shadow`, `--shadow-sticky-action`, `--spark-down-glow`, `--scanline-stripe` (ombre/scanline: semantica di ruolo UI, non tinta) |
| Allowlist prima | **16** |
| Allowlist dopo | **16** (nessuna voce Vue risolta da questa ondata; le 5 cadute in O14 restano classificate **trasferite→ora risolte** nel token file) |
| Run harness misurata | **36 s** (`OBS_CAPTURE_ONLY=dossier`, 9 PNG, exit 0) — fonte wall-clock locale 2026-07-29 |
| Scadenza mint | **180 s** (= 36 s × 5, margine per run più lunghe/jitter; ≪ 168 h; indipendente da `SESSION_HOURS`) |
| Deploy | **sì** — `matrix.css` servito cambia → bump **0.10.84**, deploy `web` |
