# OBS-OGGI-TRIAGE-031 — Ricognizione PRE-PURGA (sola lettura)

**Data:** 2026-07-24 · live Cassiopea · nessuna modifica, nessun deploy, purga NON eseguita  
**Branch/tag live:** main `v0.10.19`

---

## Q1 — Valori ESATTI a schermo (vista Oggi, lettura DOM)

| Elemento | Valore a schermo |
|----------|------------------|
| Intestazione | **`0 adotta · 28 verifica · 35 rumore`** |
| collide | **(2)** |
| chassis | **(21)** |
| manual-upgrade | **(5)** |
| sotto-soglia | **assente** (N=0 → `v-if` nasconde il blocco) |
| Pulsante massa | **`Archivia rumore (163)`** |
| Toggle rumore | `35 proposte filtrate come rumore` |

**Numero vero di verifica: 28.**  
Sotto-gruppi visibili: `2 + 21 + 5 = 28` — partizione coerente.

### Sul «29» del report assert precedente

`splitVerifica` è esaustivo: somma sotto-gruppi ≡ `|verifica|`.  
Il report post-deploy aveva mescolato due letture non atomiche (conteggio header `28` vs h4 `3+21+5=29`, o due refresh consecutivi). **Non** è un bug di `splitVerifica`. Ora header e h4 coincidono su **28**.

---

## Q2 — Delta sulla stessa fotografia (dump live)

Fotografia: serialize di tutti gli asset + dump grezzo `name_proposals` (stesso istante nel container API).

### a) Lato DB (tutte le pending grezze)

| Metrica | Valore |
|---------|-------:|
| Pending totali `status=pending` | **373** |
| `noiseProposalIds` (D10 su grezzo) | **194** id / **67** asset |
| (B2-ter report era 192/67 — drift minore post-deploy) | |

Triage top-per-asset sul grezzo (solo riferimento): adotta 3 · verifica 49 · rumore griglia 38.

### b) Lato API (`_serialize` → campo `proposals`)

| Metrica | Valore |
|---------|-------:|
| Pending esposte in `proposals` | **268** |
| Delta DB − API | **105** |
| Asset con pending a DB | 141 |
| Asset con pending in API | 88 |
| Asset con pending DB ma `proposals=[]` | **53** (94 pending azzerate) |

Su payload API: `noiseProposalIds` → **165** (UI mostra **163** — scarto 2, drift tra dump e refresh browser).

---

## Q3 — Causa (file:riga)

### Payload: **non** tutte le pending

1. **`split_name_proposals`** — [`event_maintenance.py:116–145`](observatory/api/app/services/event_maintenance.py)  
   Docstring: *«una sola evidenza corrente per fonte»*.  
   Per ogni `source`, dopo sort (pending preferito, poi data), solo `index == 0` va in `current`; le altre → `historical` (`:132–142`).  
   **Cap: 1 proposta per fonte**, non per confidenza globale né età globale.

2. **`_serialize`** — [`assets.py:106–119`](observatory/api/app/routers/assets.py)  
   - Filtra via le `fritz` sintetiche (`:107–116`).  
   - Se `presence_state ∈ {fritz_only, stale}` **oppure** `_is_historical(asset)` (`:117–119`): sposta tutto in `proposal_history` e **`proposals = []`**.  
   `_is_historical` (`:67–73`): bucket `fritz_historical` / `stale_unlocated`, `inventory_hidden`, o `operational_state != active`.

### Asset a DB assenti / svuotati nel payload

53 asset con pending a DB ma `proposals` vuoto, di cui (conteggi):

| Motivo `_serialize` | Asset |
|---------------------|------:|
| historical + fritz_only/stale | 37 |
| solo fritz_only/stale | 9 |
| solo historical | 7 |

Esempi: Broadlink/iPad/TV/Mac in `fritz_only`; molti `nuovo`/`ignorato` in bucket `fritz_historical`.  
Il list `include_historical=true` **include** l’asset nella lista, ma `_serialize` ne azzera comunque le proposte correnti.

In più: ~9 pending «ombra» stesso-source scartate da `split_name_proposals` anche su asset ancora esposti.

---

## Q4 — Conseguenza D10 (una riga)

Dopo una purga UI da **163**, il gruppo rumore **visibile** si svuota (o quasi) delle top esposte; **restano ~29 pending rumore invisibili** (DB 194 − API 165, su ~16 asset: secondi livelli stesso-source + asset `fritz_only`/`historical` con `proposals=[]`) — la coda può ripopolarsi quando quei record tornano in `proposals` o cambia la top per fonte.

---

## STOP

Nessun fix. Purga: Michele da UI dopo review. Eventuale allineamento API↔D10 (esporre tutte le pending / non azzerare historical in triage) = decisione successiva.
