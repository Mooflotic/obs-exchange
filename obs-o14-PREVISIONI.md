# O14 — PREVISIONI (dichiarate prima del deploy)

| id | previsione |
|----|------------|
| Viola esatto | `#9b7bd4` = `rgb(155, 123, 212)` — fonte: `AiInferenceLabel.vue` (border/bg color-mix) e `Dossier.vue` blocco `.inference` / `.tag.infer` (`rgba(155, 123, 212, *)`) |
| Punti d'uso del literal base | **5** occorrenze dirette del base (`#9b7bd4` ×2 in AiInferenceLabel; `rgba(155,123,212,*)` ×3 in Dossier). Famiglia AI/AP correlata (stesso ruolo semantico, hex già in produzione): AiInferenceLabel, AssetDecide, Dossier, Inventory, Suggestions, VisualBadge, TopologyBranch, Topology |
| Allowlist prima | **21** |
| Allowlist dopo | **16** (cadono le voci che restano senza literal fuori token: AiInferenceLabel, AssetDecide, TopologyBranch, VisualBadge, Topology). Restano Dossier/Inventory/Suggestions se ancora hanno literal non-AI (warn/rgba) — motivazioni aggiornate |
| Contrasto testo/bordo INFERENZA IA | **identico** prima/dopo (stesso valore cromatico; solo indirezione `var(--inference)` / `rgb(from …)` / color-mix equivalente) |
| Durata mint | `SESSION_HOURS` da config/env (default **168** in `api/app/config.py` / `.env.example`) — parametro esistente; nessuna durata a gusto |
| Deploy | **sì** — CSS/runtime web cambia (`matrix.css` + componenti + marker) → bump **0.10.83**, deploy `web` |
