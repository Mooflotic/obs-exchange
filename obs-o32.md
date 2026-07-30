# OBS-O32 — OGGI ORDINATA PER RISCHIO + DECLUTTER + RIMOZIONE MATRIX

```
wave: O32
branch: feature/obs-currency
base_dichiarata: 855913b41fa8551474d8d567f93741a0f2362c24 (O31)
VERSION: 0.10.97
deploy: api+web (Cassiopea) — reale
esito: PASS (D1.2 dangerous_exclusions=0; coda flat live verificata)
```

---

## 1. R0 — motore scoring / ordine / controlli

### R0.1 `scoreSpecificity` ≠ scala P1–P7

- `web/src/triageRules.js` → `scoreSpecificity`: specificità **nomi** 1–5 (igiene proposte), **non** la scala difensiva.
- Scala **P1–P7**: `web/src/oggiPriority.js` (`priorityFor*`, `DEFENSE_PRIORITY_LEGEND`).
- Pre-O32: P-tier usato soprattutto come **etichetta/sort locale per sezione**, non come coda globale unica.
- O32 (I6): qualify/ordine in `oggiRiskScore.js`, **re-export** da `triageRules.js` (nessuna duplicazione in `api/`).

### R0.2 Ordine pre-O32

Sezioni per famiglia (FDB / coverage / behavior / secondary / …), sort `compareDefensePriority` **dentro** la sezione — non una lista globale per rischio.

### R0.3 `material_new`

Flag O26 sulle **disposizioni chiuse**, non sulle card aperte. Per S-C O32 espone `baseline_quality` / `baseline_at` da API; FE: baseline `verified|reconstructed` ⇒ non material (solo-L2 stabile escluso).

### R0.4 Controlli «? / + / −»

| Simbolo | Dove | Natura |
|---------|------|--------|
| `?` `+` `−` / `—` | `OggiDecisionMatrix.vue` (matrice O15) | Celle evidenza/azione — **invariate** (non rumore) |
| `?` aiuto | `PageHeader` / toggle O32 `.oggi-help-toggle` | Apre legenda P1–P7 + domande rapide **su richiesta** |

---

## 2. D1.2 — qualificati / esclusi (gate assoluto)

Ricostruzione payload live + secondary allineata al DOM (`docs/obs-o32-d12.json`):

| Metrica | Valore |
|---------|--------|
| candidati | 56 |
| qualificati (partizione) | 16 |
| **qualificati live UI @1280** | **17** |
| esclusi | 40 |
| di cui `solo_l2_stable_baseline` | 9 |
| di cui `p7_hygiene` | 31 |
| **dangerous_exclusions** | **0** |

STOP legittimo: **non attivato**. Nessun escluso con conflitto attivo; nessun `material_new` non-P7 escluso. P7 escluso a prescindere dalla freschezza (mandato).

Hotfix deploy: shadowing `baseline_quality` in `fdb_defense.py` (500 su `/api/fdb-defense/signals`) → variabile `sc_baseline_quality`.

---

## 3. Prime 5 righe live (deployed 0.10.97)

Ordine verificato su `http://192.168.1.3:8080/oggi` (badge = tier):

1. **P1** · Solo L2 · `70:50:AF:FB:86:FA` · fdb · `baseline_quality=absent` (material)
2. **P1** · Solo L2 · `38:A6:CE:40:A7:76` · fdb · absent
3. **P1** · Solo L2 · `62:5A:C6:B6:6D:53` · fdb · absent
4. **P1** · `02:AA:3A:FF:48:33` · secondary (nuovo da conoscere)
5. **P1** · `BE:C7:6A:B4:E7:98` · secondary

Poi: altri P1 secondary → P3 MAC-move (2) → P4 coverage cieca (3) + monitor (3) → P6 behavior. **Nessun `P?`.** Badge monitor: `priorityForMonitor` → P4.

Coda live: **17** righe; famiglie `{fdb:5, secondary:8, coverage:3, behavior:1}`.

---

## 4. Screenshot PRIMA/DOPO (PNG reali + share pin)

Magic `\x89PNG` verificato su tutti; sha256 in `docs/obs-o32-V.json` / `docs/obs-o32-png-assert.json`.

| Breakpoint | PRE | POST full | POST fold |
|------------|-----|-----------|-----------|
| 1280 | `obs-o32-pre-oggi-1280.png` | `obs-o32-post-oggi-1280.png` | `obs-o32-post-oggi-fold-1280.png` |
| 768 | `obs-o32-pre-oggi-768.png` | `obs-o32-post-oggi-768.png` | `obs-o32-post-oggi-fold-768.png` |
| 390 | `obs-o32-pre-oggi-390.png` | `obs-o32-post-oggi-390.png` | `obs-o32-post-oggi-fold-390.png` |

POST @1280: `sha256=4ecf0b4f88700e6b086304ca7ab50d35a48869fc62458159ba1f8570731c0804` · 1280×2043 · no orphan / no mac_move banner / no MatrixRain / scanline off / help `?` / igiene `<details>`.

URL raw **commit-pinned** (tabella compilata dopo `share.sh` + push): vedi § Share sotto.

---

## 5. D2–D4 (prodotto)

- **D2:** lista flat `.oggi-risk-list`; sintesi + badge; bande complete in `<details>` nativo O24; banner FA251/mac_move scartati fuori default; legenda/quick → `? Aiuto`.
- **D3:** niente simboli muti aggiunti; matrice O15 etichettata come prima; monitor non più `P?`.
- **D4:** `MatrixRain.vue` **eliminato**; `.scanline` spento sitewide; sfondo token `--bg-*`; allowlist color = solo Plant.

---

## 6. Gate (integrali in `docs/_o32_gate_*.txt`)

| Gate | Esito |
|------|-------|
| color_literal (+self) | PASS (allowlist=1 Plant) |
| contrast (+self) | PASS (1 allowlisted `--text-3`) |
| evidence | PASS |
| w8_currency | PASS |

---

## 7. Deploy / commit

- Health API: `0.10.97`
- Bundle FE: `0.10.97`, coda `.oggi-risk-row`, no canvas matrix
- Commit principale: **`611fca2ce01fafab081bd8485d91081e57e52a6e`**
- Base: `855913b`

---

## 8. Cosa NON ho fatto

- Nessun tocco a T7, OBS-CURRENCY, `api/app/facts/`, resolver, FDB≠ownership, I1/I5, semantica tre vie O15.
- Nessuna cancellazione dati: solo filtri/ordine vista default.
- Mock «quiet» non riproposto.
- Disposizioni create: ancora 0 (fuori scope).
- Egress novelty: non in coda live (nessuna card E-N aperta nel payload al momento della cattura).

---

## Share (obs-exchange, pin ≠ main)

Compilato nello step share: URL `https://raw.githubusercontent.com/Mooflotic/obs-exchange/<PIN>/…` + doppio sha256 + curl 200.
