<!-- BLOCK-ID: OBS-UX-H-MISURA-FINALE -->

# OBS-UX — Fase H: misura finale vs casi d'uso

**Data:** 2026-07-25 · **Branch:** `feature/obs-ux` · **Baseline iniziale:** `obs-ux-misura.md` (0.10.33) · **Baseline specifica:** `obs-ux-casidiuso.md`

---

## Metodo

**Non è stata eseguita remisura live con click cronometrati** su Cassiopea in questo ambiente.

La colonna «tempo finale» deriva da **analisi code-path UI** post-ondate A–F (0.10.34–0.10.39): conteggio click dalla landing post-login (`/` Dashboard → nav) fino alla prima risposta leggibile, come in Fase 1.1. Stima umana ≈ 5–15 s/click + lettura.

Fonti codice: `Oggi.vue`, `Dossier.vue`, `Plant.vue`, `Topology.vue`, `Branch308Card.vue`, `AssetIdentity.vue`, `oggiProblems.js`, router redirect `/suggestions` → `/oggi`.

---

## Tabella casi d'uso

| Caso | Tempo iniziale (1.1) | Obiettivo (casidiuso) | Tempo finale (stimato) | Raggiunto? |
|------|----------------------|------------------------|-------------------------|------------|
| **CU-01** Cos'è questo dispositivo nuovo | 2–3 click (Oggi→Dossier) | ≤2 | **1–2** — sezione «Nuovi» in Oggi (0 click extra) + «apri» Dossier (1); sintesi identità in scheda (D) | **Parziale→Sì** — card Oggi + Dossier 1 click; identità anche nel pannello Inventario resta 2 click |
| **CU-02** Cosa è cambiato oggi | Non ottenibile (semantico) | 1 click (solo Oggi) | **1 click** nav Oggi, ma risposta = **coda operativa**, non delta giornaliero | **No** — struttura OK, semantica «changelog» assente (debito prodotto) |
| **CU-03** Perché risulta assente | 2–4 | ≤2 da Oggi se in coda | **1–2** — presenza umanizzata (`humanPresenceState`) in Dossier; monitor assenti in coda Oggi | **Parziale** — causa in italiano migliorata, evidenza FDB/monitor non sempre in card Oggi |
| **CU-04** Dove è attaccato fisicamente | 2–4 | ≤2 | **1–2** — link Impianto/Topologia da card Oggi (A); sezione chassis in Dossier | **Parziale→Sì** — patch_code in Plant, no PatchPanel UI |
| **CU-05** Cosa c'è dietro il 308 | 1–2 | 1 | **1** — `Branch308Card` in Topologia/Impianto/Dossier asset 4 (C) | **Sì** |
| **CU-06** Questo nome è affidabile | 2–4 | 1 in card Oggi | **1** — card 6 campi + confidenza/fonte; AI etichettata (E) | **Sì** |
| **CU-07** Questi due sono lo stesso apparato | 2–3 | ≤2 da card chassis | **1–2** — blocco chassis in Oggi con spiegazione 409; rename chassis **non** disponibile | **Parziale** — triage sì, azione rename chassis no |
| **CU-08** Cosa fare per primo adesso | 1 | 1 + card completa | **1** — Oggi ordinato Adotta→Verifica→rumore; card A.1 | **Sì** |
| **CU-09** Anomalia reale o rumore | 1–2 (non spiegato) | 1 con anteprima | **1** — anteprima `noiseArchivePreview` con bucket D12/D13/D3 (A.5) | **Sì** — esecuzione massa N=41 resta gesto manuale Michele |
| **CU-10** Porta da riconfermare (FDB move) | Solo `/suggestions` orfana | 1 in Oggi | **1** — sezione «Porte da confermare» in Oggi; redirect `/suggestions` (A). Live: **0 pending** (19 rejected) | **Sì** (struttura); contenuto vuoto finché non nasce pending |

---

## Sintesi obiettivi

| Esito | N | Casi |
|-------|--:|------|
| **Sì** | 4 | CU-05, CU-06, CU-08, CU-09 |
| **Parziale** | 4 | CU-01, CU-03, CU-04, CU-07 |
| **No** | 1 | CU-02 |
| **Sì (struttura, dati vuoti)** | 1 | CU-10 |

**7/10** raggiunti pienamente o con struttura pronta; **3/10** parziali per gap dati/semantica/backend, non solo presentazione.

---

## Delta rispetto a misura 1.2 (stati UI)

| Vista | 1.2 → finale |
|-------|----------------|
| Oggi | partial/stale WEAK → **OK** (ViewStateBanner F) |
| Dossier | partial MISSING → **migliorato** (sintesi D; partial pagina ancora debole su asset mancante) |
| Inventory | error MISSING → **OK error** (B/F) |
| Plant / Topology | error MISSING → **OK error**; partial WEAK → **partial esplicito** |
| Monitoring | stale MISSING → **stale/partial** parziali |
| Findings | — → error/loading OK; empty ancora WEAK |

---

## Onestà limiti

- Nessun cronometro reale; numeri click da grafo nav + handler `router.push`.
- CU-02 richiede feature «delta giornaliero» fuori scope OBS-UX.
- CU-10 non verificabile end-to-end finché `move_pending=0`.
- Gesto «Archivia rumore N=41» **non eseguito** — anteprima sola.
