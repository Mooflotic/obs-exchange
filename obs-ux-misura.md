# OBS-UX — Fase 1 Misura

**Live:** 0.10.33 · **Data:** 2026-07-25 · Branch `feature/obs-ux`  
**Prune 0.1:** non ancora (raw_min `2026-07-20`; atteso ~2026-07-27).  
**Conteggi:** assets 151 · NP 412 · pending 122 · ip_current 100 · move_pending 0 · move_rejected 19 · `observations` assente.

---

## 1.1 Tempo-per-risposta (misurato su codice UI)

Landing post-login = `/` Dashboard. Click = azioni fino alla risposta.

| Domanda | Click | Viste | Ottenibile? | Note |
|---------|------:|-------|-------------|------|
| cos'è questo dispositivo nuovo | 2–3 | Oggi→Dossier·Chi sei | Parziale→sì | Inventario senza Identità nel pannello |
| cosa è cambiato oggi | 1+ | Timeline / Oggi | **No** (semantico) | Nessun delta giornaliero; Oggi=coda non changelog |
| perché risulta assente | 2–4 | Dossier/Impianto | Parziale | Enum presence grezzo; motivi backend non etichettati |
| dove è attaccato fisicamente | 2–4 | Dossier/Plant/Topology | Parziale | `patch_code` su porta; no PatchPanel UI |
| cosa c'è dietro il 308 | 1–2 | Plant/Topology | Parziale | FDB uplink + porte manuali; no SNMP |
| questo nome è affidabile | 2–4 | Oggi/Dossier | Parziale | Confidence + verdict; no score unico |
| questi due sono lo stesso | 2–3 | Chassis/Inventory | Parziale | Nessun confronta A↔B |
| cosa fare per primo | **1** | Oggi | **Sì** | Adotta→Verifica→rumore→Altro |
| anomalia reale o rumore | 1–2 | Oggi | Sì (nomi) | Altrove Findings in calibrazione |

---

## 1.2 Inventario stati (mancanti = difetto)

| Vista | load | empty | error | parziale | forbidden | stale |
|-------|------|-------|-------|----------|-----------|-------|
| Oggi | OK | OK | OK | WEAK | MISSING | WEAK |
| Dossier | OK | WEAK | OK | MISSING pagina | MISSING | WEAK raw |
| Inventory | OK | OK | **MISSING** | MISSING | MISSING | OK |
| Plant | OK | WEAK | **MISSING** | WEAK FDB | MISSING | WEAK |
| Topology | OK | WEAK | **MISSING** | WEAK | MISSING | OK |
| Monitoring | OK | OK | WEAK | WEAK | MISSING | MISSING |
| Suggestions | OK | OK | **MISSING** | MISSING | MISSING | MISSING |
| AssetChassis | OK | OK | OK | **OK** partialWarning | MISSING | OK |
| DirectionBar | — | — | — | — | — | OK «non disponibile» |
| CandidateList | — | WEAK | MISSING | MISSING | MISSING | MISSING |

---

## 1.3 Audit dipendenze (obbligatorio pre-rimozione)

| Target | Chi chiama | Uso reale | Decisione (da ondata B) |
|--------|------------|-----------|-------------------------|
| `/suggestions` | router; UI orfana; Dashboard conteggio senza link | Suggestion pending (move/rename) | **Migrare** move→Oggi; poi route non necessaria |
| `AssetIdentity` technical dump | Solo toggle Dossier → `?technical=1` | Debug JSON | Valutare in D: rimuovere se nessun caso d'uso |
| Suggestion vs NameProposal | Due code parallele | Naming duplicato; move solo Suggestion | Unificare **presentazione** in Oggi; modelli restano distinti |
| PatchPanel/PatchPort | Solo DB/Alembic; 0 UI | Morto | Keep schema o drop in B dopo conferma |
| Dashboard/Incidents/Ai/Runbook | Router; fuori nav (ecc. landing) | Dashboard sì; altri secondari | Keep; link o menu strumenti |
| `POST /fdb` legacy | Solo definizione; collector usa `/fdb-switch` | Escape hatch | Keep deprecato o remove dopo conferma zero client |

---

## 1.4 Audit testi (gergo)

| Label | Problema |
|-------|----------|
| collide | Inglese interno |
| sotto-soglia | Non spiega 0.75 |
| Verifica | Ambiguo |
| chassis / manual-upgrade / upgrade | Jargon |
| rumore / Archivia rumore | OK se spiegato cosa/perché |
| presence_state raw in Dossier | Enum API |
| fritz_historical / stale_unlocated / inventory_hidden_auto | Solo backend/meta |
| Proposte (Suggestions) vs Proposte nome (Oggi) | Collisione lessicale |

---

## 1.5 A11y / responsive (rotto)

- Focus globale OK; molti toggle Inventario/Dossier senza `role=switch`/tastiera.
- Search `outline:none` senza focus-visible forte.
- Dialog Inventario: aria-modal senza focus trap completo.
- Sidebar wrap a 800px: densità/overflow su Oggi actions.
- Route orfane = barriera discoverability.

---

## 1.6 Azioni

| Azione | Confirm | During | After | Partial fail | Undo |
|--------|---------|--------|-------|--------------|------|
| adopt nome | No (chassis blocco 409) | busy | reload | error | **MISSING** |
| reject | No | busy | reload | error | **MISSING** |
| Archivia rumore massa | `window.confirm` | massBusy | notice | saltate in notice | **MISSING** |
| move approve/reject | No | no busy | reload | silent? | **MISSING** |

---

## 1.7 Caso N=41 — scomposizione (live 2026-07-25)

`noiseProposalIds` su `all_proposals=true` → **N = 41**. Regole in `triageRules.js` (`isNoiseProposal`):

| Regola | N | Significato |
|--------|--:|-------------|
| **D13** parità normalizzata | **21** | Proposta ≡ nome attuale (dopo normalize) — ridondante |
| **D12** rank 1 sintetico | **15** | MAC/hex/Unknown/PC sintetico |
| **D3** rank ≤ corrente | **5** | Proposta non più specifica (es. Fritz-* SSDP vs nome parlante) |

Esempi D12: `001788a889ec` (Hue). Esempi D3: `Fritz-SalaPC` su «FRITZ!Repeater SalaPC». Esempi D13: `ROCK`/`ROCK`, doppi dns+fritz su stessi host.

**Difetto UX:** il confirm dice solo il numero; non elenca *cosa* né *perché*. Comando di massa non giustificato all'utente = difetto di esperienza (da chiudere in ondata A senza eseguirlo).
