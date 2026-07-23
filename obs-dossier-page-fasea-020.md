<!-- BLOCK-ID: OBS-DOSSIER-PAGE-FASEA-020 -->

# OBS-DOSSIER-PAGE-FASEA-020 — Dossier pagina piena + sidebar RADAR/MAPPA

**STOP FASE A** — sola lettura · nessun codice/deploy.

Obiettivo: `/dossier/:id` come vista piena nel gruppo **RADAR**. Sidebar riorganizzata in due gruppi (stub per voci non ancora vive).

---

## Target sidebar (FASE B)

| Gruppo | Voci | Stato in questa fase |
|--------|------|----------------------|
| **RADAR** | Oggi · Osservatorio · **Dossier** · Come funziona | stub tranne Dossier (pagina reale) |
| **MAPPA** | Inventario · Impianto · Topologia · Monitor · Timeline · Findings · Azioni | già esistenti (rinominate/riordinate) |

Fuori scope / da decidere in B: Incidenti, Proposte, Runbook, AI (oggi in «Salute/Controllo») — non compaiono nella lista target; o si aggregano sotto MAPPA o restano in un terzo gruppo minimo.

---

## 1. Estrazione componenti

**Oggi:** Chi sei + Abitudini vivono solo nel drawer di `web/src/views/Inventory.vue` (Teleport → `aside.inv-panel`).

### Template / API

| Sezione | ~righe | Fetch |
|---------|--------|-------|
| Chi sei | 751–850 | `GET /api/assets/{id}/identity[?technical=1]` via `loadIdentity` |
| Abitudini | 852–973 | `GET /api/assets/{id}/habits?days=7` via `loadHabits` |

Chiave asset: `device.primaryId` (non la chassis key).

### State intrecciato col pannello

| Stato | Accoppiamento |
|-------|----------------|
| `identity*` / `habits*` / expand | init in `openPanel` → `load*`; azzerati in `closePanel` |
| `panelOpen` + `body.panel-open` | Teleport drawer; Escape / backdrop chiudono |
| `busy` / `msg` | **condivisi** con Tu decidi, adopt, IP role, AI — anche opt-out OS / scan |
| `selected` / `form` | editing; le due sezioni leggono `selected.primaryId` |

### Come estrarre (riuso vero, zero duplicazione UI)

```
AssetIdentity.vue   prop: assetId
  watch → api.assetIdentity; loading/error interni
  azioni OS: emit('changed') oppure solo-lettura sul Dossier

AssetHabits.vue     prop: assetId, days?=7
  watch → api.assetHabits; expand interni; helpers da habitsUi.js

Inventory drawer:  <AssetIdentity :asset-id="…" /> + <AssetHabits … />
Dossier page:      stessi due componenti
```

CSS `.habits-*` / `.inv-chi-sei` oggi scoped in Inventory → spostare col componente (o modulo CSS condiviso).

**Verdict:** si riusa davvero. Non duplicare markup. Costo = move template+state+CSS+load; spezzare dipendenza da `closePanel`/`Teleport`.

---

## 2. Routing

`web/src/router.js`: routes flat, nessun layout nested.

- Guard: `beforeEach` + `auth.check()`; solo `/login` è `meta.public`.
- Aggiungere `/dossier` e `/dossier/:id`: **banale/additivo** (come Inventory).
- Stub RADAR: `/oggi`, `/osservatorio`, `/come-funziona` → stesso componente `Stub.vue` o tre mini-viste «Prossimamente».
- Catch-all `/:pathMatch(.*)*` resta in coda.

---

## 3. Sidebar — oggi e mobile

**Oggi** (`App.vue` ~115–137): tre `.nav-group` (Operativo / Salute / Controllo) + `.nav-label`. CSS già in `matrix.css` (`.nav-group`, `.nav-label::before`).

**RADAR / MAPPA:** refactor **di contenuto** (riordino link + 2 label), **non strutturale** — stesso markup group/label.

**Mobile (`max-width: 800px` in `matrix.css` ~744+; sotto ~430px stessa regola, più stretto):**

- Sidebar diventa barra orizzontale in alto (flex, scroll).
- **`.nav-label { display: none }`** — le intestazioni di gruppo **spariscono**; restano solo i link in fila.
- Con ~11+ voci MAPPA+RADAR la barra sarà affollata: in FASE B valutare truncate / overflow-x (già tipico) o nascondere stub su mobile.

Nessun refactor CSS obbligatorio per introdurre i gruppi; solo attenzione UX mobile (label nascoste = gruppi invisibili).

---

## 4. Ricerca `/dossier` (senza id)

| Opzione | Pro | Contro |
|---------|-----|--------|
| **A. Client-side** — `GET /api/assets?include_historical=true` + filtro locale (come Inventario) | Zero API nuova; ~130–150 asset ok | Scarica tutto |
| **B. Server `?q=`** — già in `list_assets` (name/vendor/notes/status/MAC/IP) | Leggero se cresce | Hostname non nel blob search |

**Proposta FASE B:** **A** per hub Dossier (stesso ordine di grandezza Inventario). Opzionale debounce + `?q=` se la lista cresce. Niente endpoint dedicato.

Placeholder search: nome / IP / MAC (allineato a `matchDeviceSearch`).

---

## 5. Divisione contenuti — drawer vs pagina

Principio: **una sola fonte UI** per Chi sei / Abitudini (i componenti). Drawer = anteprima + azione; pagina = approfondimento.

| | **Drawer Inventario** | **Pagina `/dossier/:id`** |
|--|------------------------|---------------------------|
| Scopo | «È questo? Agisci / correggi» | «Chi è davvero e come si comporta» |
| Anteprima | Presente/stale · IP · nome · vendor/OUI breve | Hero completo (nome, MAC, IP, presence) |
| Chi sei | **snippet** o componente in modalità compact *oppure* solo link | `AssetIdentity` completo (+ technical) |
| Abitudini | **no** (o 1 riga volume 7g) — evita doppio fetch pesante in lista | `AssetHabits` completo |
| Editing | Tu decidi · Note · adopt · IP role · watch | link «Modifica in Inventario» |
| CTA | **`Apri Dossier`** → `router.push(/dossier/${primaryId})` | «Torna all’Inventario» / search hub |

**Evita duplicazione:** non mantenere due markup paralleli di Chi sei/Abitudini. Se il drawer mostra un pezzo di identity, è lo stesso `AssetIdentity` con prop `variant="compact"` **oppure** solo i campi già noti dal device composto (senza secondo fetch) + CTA Dossier.

Raccomandazione FASE B minima:

1. Drawer: head (presente? IP? nome) + Tu decidi + **Apri Dossier** + editing residuo.
2. Dossier: Identity + Habits full.
3. Inventario lista invariata; open panel resta per edit rapido.

---

## FASE B (fuori scope) — pezzi

1. Extract `AssetIdentity` / `AssetHabits`; Inventory li monta (o snellisce).
2. `DossierHub.vue` (`/dossier`) + `Dossier.vue` (`/dossier/:id`).
3. Sidebar RADAR/MAPPA; stub Oggi / Osservatorio / Come funziona.
4. CTA «Apri Dossier» nel drawer.
5. Decisione Incidenti/Proposte/Runbook/AI (terzo gruppo o sotto MAPPA).

**STOP FASE A.**
