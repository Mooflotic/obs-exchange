# OBS-O31 — SCOPERTA + PROPOSTA (nessun codice prodotto, nessun deploy)

```
wave: O31
branch: feature/obs-currency
base_dichiarata: 3b7690f8b258d923dad4e7563dcb42189c0ea694 (O30 principale)
tip_0.1: c6f5aca1b1784dd1771e75ec6ec11fd5ced58f66 (report O30)
esito: SOLO A/B/C — nessuna fase D, nessun bump VERSION, nessun deploy
```

---

## 1. Blocco 0 (integrale)

### 0.1

```
===== 0.1 git log --oneline -8 feature/obs-currency =====
c6f5aca docs(observatory): report O30 (principale 3b7690f8b258d923dad4e7563dcb42189c0ea694)
3b7690f feat(observatory): O30 omogeneità colori + Topology B (0.10.96)
5e72dd2 feat(observatory): O29 GS308 token realign + mappa inventory (0.10.95)
76fabaa feat(observatory): O28 a11y dialogo disposition + chrome N=0 (0.10.94)
b251a43 docs(observatory): O27 chiusura UX lifecycle — test E1.2 + catture (no prodotto)
ffd85ae docs(observatory): report O26 (principale 3f9ab1f)
3f9ab1f feat(observatory): O26 Oggi lifecycle dispositions (0.10.93)
638d115 docs(observatory): report O25 (principale 4571e45)

===== git rev-parse HEAD =====
c6f5aca1b1784dd1771e75ec6ec11fd5ced58f66

===== git fetch origin && git rev-parse origin/feature/obs-currency =====
c6f5aca1b1784dd1771e75ec6ec11fd5ced58f66

===== discendenza da 3b7690f8b258d923dad4e7563dcb42189c0ea694? =====
YES
```

GATE 0.1: **PASS**.

### 0.2 Housekeeping commit-pinned O30

| Artefatto | Commit rete-palazzo (stato) | Commit obs-exchange | URL raw PINNED | local==raw | main vs pin |
|-----------|----------------------------|---------------------|----------------|------------|-------------|
| `COLOR_SEMANTICS.md` | `3b7690f` (invariato tip) sha256 `3051ccbb…b5bc64` wc=42 | `344a2a144616377dcda79ad20c290226a2d3e205` | [pin](https://raw.githubusercontent.com/Mooflotic/obs-exchange/344a2a144616377dcda79ad20c290226a2d3e205/COLOR_SEMANTICS.md) | YES curl 200 | **identico** |
| `obs-o30.md` (con cite hash) | `c6f5aca` sha256 `6bd5a381…a7a5f4` wc=279 | `625b25320de92936d526348c63cc6f7809bbfc0c` | [pin](https://raw.githubusercontent.com/Mooflotic/obs-exchange/625b25320de92936d526348c63cc6f7809bbfc0c/obs-o30.md) | YES curl 200 | **identico** al momento O31 |

**Divergenza dichiarata:** `obs-o30.md` @ `3b7690f` ≠ @ `c6f5aca` (1 riga: § hash commit principale). Lo stato «riportato» O30 è quello con cite = `c6f5aca` / pin `625b253…`.

Regola permanente aggiornata in `docs/PROCESS_NOTES.md`: URL raw **sempre** commit-pinned, mai `main`.

---

## 2. Fase A — inventario Matrix (branding)

### A1 — `len=4` (asserito)

| # | Elemento | Visibile ora? | Rotte | Ruolo |
|---|----------|---------------|-------|-------|
| 1 | `MatrixRain.vue` (canvas katakana) | **NO** (`display:none` dal 10e93f12 / OBS-025) | globale App | Decorativo ambient; **non** stato; CSS lo spegne ma il componente resta montato |
| 2 | classe `.matrix-bg` | no | globale | Hook stile; naming tematico |
| 3 | `.scanline` | **SÌ** (opacity 0.25) | globale | Decorativo CRT/cyber; **non** stato |
| 4 | `--scanline-stripe` | sì (via scanline) | globale | Supporto effetto |

Nessun copy UI con la parola «Matrix».  
**Esclusi da A1 (non branding):** matrice O15 / `OggiDecisionMatrix`, filename `matrix.css` (A2).

### A2

- O15: **non toccata** (nemmeno in proposta applicativa).
- Rename `matrix.css`: solo nota igiene interna — **non fatto**.

### A3 — alternative ambientali (mock locali, CSS inject, no deploy)

Rotta di prova: `/topology` @1280 (niente O15). Baseline = produzione (scanline on, rain off).

| ID | Idea | PNG |
|----|------|-----|
| baseline | Stato attuale | `obs-o31-a3-baseline-1280.png` |
| a_neutral | Zero effetti | `obs-o31-a3-a_neutral-1280.png` |
| b_accent | Radial soft `--accent` / `--data-out` | `obs-o31-a3-b_accent-1280.png` |
| c_structure | Gradiente `--bg-1`→`--bg-0` | `obs-o31-a3-c_structure-1280.png` |

Artefatto: `docs/obs-o31-A.json`.

---

## 3. Fase B — fatti Oggi / disposizioni

### B1 — disposizioni NAS (sola lettura)

Query esatte (cookie sessione; nessuna write):

```
GET /api/oggi/dispositions
GET /api/oggi/dispositions?state=all
GET /api/oggi/dispositions?state=closed
GET /api/oggi/dispositions?state=reopened
GET /api/oggi/dispositions?evaluate_material=false
```

**Risultato uniforme:** `count=0`, `closed_count=0`, `closed_keys=[]`, `items=[]`.

→ **Zero** disposizioni create, **zero** chiuse, **zero** riaperte da quando il meccanismo è live (O26).

### B2 — censimento Oggi produzione (2026-07-30)

| | 1280 | 768 | 390 |
|--|------|-----|-----|
| `scrollHeight` | 18634 | 22726 | 28627 |
| card `.oggi-problem` | 36 | 36 | 36 |
| closed chrome (`data-o26`) | assente | assente | assente |
| legend `open` | true | true | false |
| rain display | none | none | none |
| scanline | block / 0.25 | idem | idem |

- **open (disposition):** tutte le 36 card (nessuna chiave chiusa).
- **closed:** 0.
- Con `closed_count=0` il link «N casi chiusi» **non è nel DOM** (O28): contributo altezza disposition chrome = **0**. L’altezza pagina è dominata da FDB (~11788 px @1280 sul solo `#oggi-fdb`) + altre code — coerente con «quasi come prima di O25/O26» per la parte lifecycle UI; il carico verticale resta il contenuto operativo (non introdotto dalle disposizioni).

### B3 — catture Oggi

| file | W×H | sha256 |
|------|-----|--------|
| `obs-o31-b-oggi-1280.png` | 1280×18497 | `bcd7af08227e894dc57bad97500191d81507c7e48b4525726aee6bbaaa705450` |
| `obs-o31-b-oggi-768.png` | 768×22246 | `fcce9469ae9824f3e7e2b5028f19c62170236a40517d59b53053fac4b49f7db3` |
| `obs-o31-b-oggi-390.png` | 390×27800 | `acae172c7fe44fe0620a36a148b0a3069888efdf55a709065e9634a797948697` |

Meta: `docs/obs-o31-measure.json`. Auth: session mint TTL (token non pubblicato).

---

## 4. Fase C — prima vista

### C1 — cosa rende fuorviante la piega @1280

Ordine osservato sopra ~900px (produzione):

1. **Header** `Oggi` (~26px) — titolo minimo, help non espanso in census.
2. **Legenda P1–P7 aperta** (~240px) — spiega il sistema, non dà lavoro.
3. **Domande rapide + indice sezioni** (~335px) — orientamento/ancore.
4. Banner **FA251 orfano** + **396 mac_move scartati** — debito/meta, non coda primaria.
5. Solo a ~top 858 inizia **`#oggi-fdb`** (lavoro reale).

Verdict: la prima viewport insegna l’ontologia (priorità, domande, debiti) **prima** di mostrare un caso da decidere.

Catture piega: `obs-o31-c1-oggi-fold-{1280,768,390}.png`.

### C2 — documento (non applicato)

`docs/obs-o31-design-language.md` — tipografia, `--space-*`, sopra/sotto piega, disclosure; **senza** conflitti con O15 / fatti-vs-inferenze / segnale discreto.

### C3 — mock locali solo intestazione/chrome (no deploy, no commit prodotto)

| Variante | Idea | PNG |
|----------|------|-----|
| `c3_v1_quiet` | Titolo più grande + aria; legenda/quick restano | `obs-o31-c3_v1_quiet-fold-1280.png` |
| `c3_v2_workfirst` | Legenda forzata chiusa (mock) | `obs-o31-c3_v2_workfirst-fold-1280.png` |

Confronto vs `obs-o31-c1-oggi-fold-1280.png`.

---

## 5. Domande aperte per Michele

1. **Matrix ambient:** rimuovere solo `.scanline`, o anche smontare `MatrixRain` (già invisibile)? Preferisci A3-a / A3-b / A3-c?
2. **Prima vista Oggi:** quiet header (C3-v1) o work-first (C3-v2: legenda chiusa + quick dopo il lavoro)?
3. I banner **FA251 orfano** e **mac_move scartati** restano sopra FDB o vanno sotto disclosure (senza toccare FA251/logica)?
4. Con **0 disposizioni** live: priorità a far usare il lifecycle, o prima ripulire la piega?

---

## 6. Cosa NON ho fatto

- Nessun commit di codice prodotto, nessun deploy, nessun bump VERSION.
- Nessun tocco O15, T7, OBS-CURRENCY, resolver, FA251, backend, disposition write.
- Mock solo via CSS inject Playwright (non persistiti in `web/src`).
- One-shot `/tmp/o31_capture.py` non in git.

## 7. Share O31 (commit-pinned)

Tutti curl 200 + local==raw al pin indicato. Inventario completo: `obs-o31-share-proof.json`.

| file | exchange commit | URL pin |
|------|-----------------|--------|
| `obs-o31.md` (questo testo, pin pre-cite) | `8e53b80ee9ef8e5dbfe2efef3dfed8be24f99df1` | [raw](https://raw.githubusercontent.com/Mooflotic/obs-exchange/8e53b80ee9ef8e5dbfe2efef3dfed8be24f99df1/obs-o31.md) |
| `obs-o31-A.json` | `4f8e59ac8ca476bcd34694a63d07262160980281` | [raw](https://raw.githubusercontent.com/Mooflotic/obs-exchange/4f8e59ac8ca476bcd34694a63d07262160980281/obs-o31-A.json) |
| `obs-o31-design-language.md` | `b14f8a8df40985f080d3f78df49577268b570dd0` | [raw](https://raw.githubusercontent.com/Mooflotic/obs-exchange/b14f8a8df40985f080d3f78df49577268b570dd0/obs-o31-design-language.md) |
| `obs-o31-b-oggi-1280.png` | `1de58bb3409a69129f14b7094866c4c0d03d0a62` | [raw](https://raw.githubusercontent.com/Mooflotic/obs-exchange/1de58bb3409a69129f14b7094866c4c0d03d0a62/obs-o31-b-oggi-1280.png) |
| `obs-o31-a3-a_neutral-1280.png` | `e642e4acb13d24161f8b325ce93c9dea6b699dbf` | [raw](https://raw.githubusercontent.com/Mooflotic/obs-exchange/e642e4acb13d24161f8b325ce93c9dea6b699dbf/obs-o31-a3-a_neutral-1280.png) |
| `obs-o31-c1-oggi-fold-1280.png` | `9aba857a8d866218f3adc7c22bff189c0579676d` | [raw](https://raw.githubusercontent.com/Mooflotic/obs-exchange/9aba857a8d866218f3adc7c22bff189c0579676d/obs-o31-c1-oggi-fold-1280.png) |
| `obs-o31-c3_v2_workfirst-fold-1280.png` | `a2a578ef192559666838594e84edc21689251f6f` | [raw](https://raw.githubusercontent.com/Mooflotic/obs-exchange/a2a578ef192559666838594e84edc21689251f6f/obs-o31-c3_v2_workfirst-fold-1280.png) |

Il tip di sola pubblicazione del report su exchange può avanzare di un commit rispetto alla riga sopra (lag PROCESS_NOTES); O32 conferma in Blocco 0.1.