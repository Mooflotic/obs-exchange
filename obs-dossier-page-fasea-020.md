<!-- BLOCK-ID: OBS-DOSSIER-PAGE-FASEA-020 -->

# OBS-DOSSIER-PAGE-FASEA-020 — Dossier pagina piena (ricognizione)

**STOP FASE A** — sola lettura, nessun codice/deploy.

Obiettivo: `/dossier/:id` nel gruppo «Non so cosa cerco»; riusare Chi sei / Abitudini da Inventory, non duplicare.

---

## 1. Estrazione — Inventory.vue oggi

**File:** `web/src/views/Inventory.vue`

### Struttura template (drawer `aside.inv-panel`)

| Blocco | ~righe | Contenuto |
|--------|--------|-----------|
| Head | 680–698 | nome / MAC / IP + close |
| **Tu decidi** | 700–749 | form edit (nome, cat, status, OS, patch, critico, watch) |
| **Chi sei** | 751–850 | identity KV, opt-out OS, scan readiness, «Rileva OS ora», JSON technical |
| **Abitudini** | 852–973 | coverage, provenance, dest out\|in, sparkline, porte |
| Altro drawer | 975–1114 | IP, «Il sistema ha visto», interfacce, percorso, proposte, fingerprint, note, Salva |

### State dedicato alle due sezioni

- **Chi sei:** `identity`, `identityLoading`, `identityTechnicalOpen`, `osScanBusy`, `osScanMsg`
- **Abitudini:** `habits`, `habitsLoading`, `habitsDestExpanded`, `habitsPortsExpanded` + computed (`habitsLocalHours`, `habitsSpark`, `habitsDestView`, …)

### Load API (già per `primaryId`, non chassis key)

| Funzione | Endpoint client | Note |
|----------|-----------------|------|
| `loadIdentity(assetId)` | `GET /api/assets/{id}/identity[?technical=1]` | fail → `msg` |
| `loadHabits(assetId)` | `GET /api/assets/{id}/habits?days=7` | fail soft, non blocca pannello |
| azioni OS | `PATCH` asset opt-out · `POST …/scan-os` · `scanReadiness` | usano `busy`/`msg` condivisi |

Helpers: `habitsUi.js` (presentazione pura); `inventoryDevices.identitySources` / `pathHops` per pezzi adiacenti del panel.

### Accoppiamento col pannello (da spezzare)

```
openPanel(device)
  → selected + form + panelOpen + body.panel-open
  → loadIdentity(primaryId) + loadHabits(primaryId)

closePanel()
  → azzera selected/form/identity/habits/expand + body.panel-open

Escape / backdrop / post-save → closePanel
busy + msg → condivisi con Tu decidi / adopt / IP role / AI
```

**Per `AssetIdentity.vue` / `AssetHabits.vue`:**

- Prop: `assetId: number` (+ opz. `days` per habits).
- Caricano da soli (`onMounted` / `watch assetId`).
- State loading/error **interno**; non dipendere da `panelOpen` / `closePanel`.
- Azioni mutanti (opt-out, scan OS): o restano nel child con emit `changed`, o restano nel drawer Inventario (azioni) e sul dossier solo lettura.
- CSS: ~100 linee `.habits-*` / `.inv-chi-sei` oggi scoped in Inventory → spostare col componente (o foglio condiviso).
- Inventory dopo extract: `<AssetIdentity :asset-id="selected.primaryId" />` + stesso per Habits **oppure** link «Apri dossier» e drawer snellito.

**Verdict estrazione:** fattibile; costo = spostare template+state+CSS+load. Il vincolo reale è `busy`/`msg` e le azioni OS, non le API.

---

## 2. Routing

**File:** `web/src/router.js` — routes flat, **nessun layout nested**.

- Guard unico: `beforeEach` → `auth.check()`; solo `/login` è `meta.public`.
- Inventario già `/inventory`; query `?view=` gestita in-page.

**`/dossier` + `/dossier/:id`:** additivo e banale (due entry come le altre viste). Auth già coperta. Shell `App.vue` + `<router-view>` invariata. Attenzione solo all’ordine: `/dossier/:id` prima del catch-all `/:pathMatch(.*)*`.

---

## 3. Sidebar

**File:** `web/src/App.vue` ~115–137 — già tre `.nav-group` con `.nav-label` («Operativo», «Salute», «Controllo»). CSS pronto in `matrix.css` (`.nav-group` / `.nav-label`).

**«So cosa cerco» / «Non so cosa cerco»:** solo markup additivo (rinominare/riordinare gruppi + link Dossier). Nessun refactor strutturale. Mobile già nasconde le label.

Proposta gruppi (orientativa):

| Gruppo | Voci |
|--------|------|
| So cosa cerco | Inventario, Impianto, Topologia, … |
| Non so cosa cerco | **Dossier**, Dashboard?, Findings? |
| (Salute / Controllo restano o si fondono) | … |

---

## 4. Ricerca

**Backend:** `GET /api/assets?q=` già filtra substring su name, category, vendor, notes, status, MAC, IP (`assets.py` ~288–301). **Nessun campo hostname dedicato** nel blob search.

**Client Inventario oggi:** carica **tutto** (`include_historical=true`) e filtra con `matchDeviceSearch` (nome/vendor/IP/MAC iface) — **non** passa `q` all’API.

**Scala:** ~130–150 device/asset in casa → client-side basta per hub `/dossier`. Alternativa zero-costo: riusare `?q=` server se un giorno cresce.

**Endpoint nuovo:** non necessario in FASE B.

---

## 5. Proposta — drawer vs pagina (niente doppioni)

| **Drawer Inventario** (azione) | **Pagina `/dossier/:id`** (lettura / narrativa) |
|--------------------------------|--------------------------------------------------|
| Lista + search + countbar | Hero: nome, MAC, IP (da `GET /api/assets/{id}`) |
| **Tu decidi** + Salva / Note | **AssetIdentity** (Chi sei) |
| Adotta proposte / AI nome / ruoli IP | **AssetHabits** (Abitudini) |
| Watch / critico | Percorso (+ link Topologia) opzionale |
| CTA «Apri dossier» → `/dossier/:id` | Link «Modifica in Inventario» → `/inventory` + open panel |

**`/dossier` (senza id):** search-first hub («Non so cosa cerco») → pick → naviga a `/:id`. Stesso dataset assets, UI diversa dalla tabella Inventario.

**Regola anti-duplicazione:** le due sezioni vivono **solo** nei componenti estratti; Inventory e Dossier li montano. Contenuto edit resta solo in Inventario.

---

## FASE B (fuori scope) — pezzi previsti

1. Extract `AssetIdentity.vue` + `AssetHabits.vue`; Inventory li riusa.
2. `Dossier.vue` + routes `/dossier`, `/dossier/:id`.
3. Sidebar: due gruppi + link Dossier.
4. Hub search client-side; deep-link da Inventario.

**STOP FASE A.**
