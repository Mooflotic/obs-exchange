# OBS-UX — Casi d'uso (specifica vincolante)

**Versione specifica:** 2026-07-25 · Baseline prodotto 0.10.33  
**GATE 2:** ogni caso ha tempo attuale (Fase 1.1) e tempo obiettivo.  
Correzioni alla specifica vanno dichiarate, non implementate in silenzio.

---

## Convenzioni tempo

- **Attuale:** click dalla landing `/` + viste (misura 1.1). Tempo umano stimato ≈ 5–15 s/click + lettura.
- **Obiettivo:** percorso primario ≤ click dichiarati; risposta leggibile senza gergo.

---

### CU-01 — Cos'è questo dispositivo nuovo

| Campo | Contenuto |
|-------|-----------|
| **Chi** | Operatore; vuole etichettare uno sconosciuto |
| **Domanda** | «Cos'è questo dispositivo nuovo?» |
| **Evidenze oggi** | MAC/OUI, IP, proposte nome, fingerprint facts, porte/servizi se scan |
| **Risposta attesa** | Identità + fonti + freschezza + cosa manca; azione adotta/verifica |
| **Tempo** | Attuale **2–3 click** (Oggi→Dossier). Obiettivo **≤2** (scheda in Oggi + Dossier 1 click) |
| **Azione** | Adotta nome / ignora / apri Dossier |
| **Esito** | Nome adottato o in verifica; nessun campo autorevole da AI senza adopt |
| **Stato oggi** | **Parziale** |

### CU-02 — Cosa è cambiato oggi

| Campo | Contenuto |
|-------|-----------|
| **Chi** | Operatore al mattino |
| **Domanda** | «Cosa è cambiato oggi?» |
| **Evidenze** | Coda Oggi (proposte, nuovi, monitor); eventi Timeline (non scoped) |
| **Risposta** | Elenco problemi prioritizzati in Oggi (nomi, chassis, porte, assenze, monitor) |
| **Tempo** | Attuale **non ottenibile** come delta. Obiettivo **1 click** (solo Oggi) |
| **Azione** | Aprire/risolvere dalla coda |
| **Esito** | Coda aggiornata |
| **Stato oggi** | **Per niente** (semantico) → ondata A |

### CU-03 — Perché risulta assente

| Campo | Contenuto |
|-------|-----------|
| **Chi** | Operatore su device «non presente» |
| **Domanda** | «Perché questo apparato risulta assente?» |
| **Evidenze** | presence_state, last_seen, fritz, FDB, monitor |
| **Risposta** | Causa in italiano + evidenza + freschezza (I2/I3) |
| **Tempo** | Attuale 2–4. Obiettivo **≤2** da Oggi se in coda |
| **Azione** | Verifica reachability / apri Dossier |
| **Stato oggi** | **Parziale** |

### CU-04 — Dove è attaccato fisicamente

| Campo | Contenuto |
|-------|-----------|
| **Chi** | Operatore in cabina |
| **Domanda** | «Dove è attaccato fisicamente?» |
| **Evidenze** | SwitchPort bind, patch_code, Topology path, FDB |
| **Risposta** | Switch:porta + patch se noto; altrimenti «non rilevato» |
| **Tempo** | Attuale 2–4. Obiettivo **≤2** (link da Oggi/Dossier) |
| **Stato oggi** | **Parziale** |

### CU-05 — Cosa c'è dietro il 308

| Campo | Contenuto |
|-------|-----------|
| **Chi** | Operatore sul ramo opaco |
| **Domanda** | «Cosa c'è dietro il 308?» |
| **Evidenze** | Ping `.1.8`, porte manuali, MAC su uplink FDB (conf 0.65), LLDP core, endpoint visti altrove. **Non** SNMP/PoE/contatori (I7) |
| **Risposta** | Scheda ramo: fatti vs inferenze etichettate; buchi dichiarati |
| **Tempo** | Attuale 1–2 (Plant/Topology). Obiettivo **1** (scheda dedicata raggiungibile) |
| **Stato oggi** | **Parziale** → ondata C |

### CU-06 — Questo nome è affidabile

| Campo | Contenuto |
|-------|-----------|
| **Chi** | Operatore in triage |
| **Domanda** | «Questo nome è affidabile?» |
| **Evidenze** | source, confidence, scoreSpecificity (client), collisioni, manual override |
| **Risposta** | Fonte + certezza + confronto col nome attuale |
| **Tempo** | Attuale 2–4. Obiettivo **1** in card Oggi |
| **Stato oggi** | **Parziale** → A |

### CU-07 — Questi due sono lo stesso apparato

| Campo | Contenuto |
|-------|-----------|
| **Chi** | Operatore su multi-NIC / omonimi |
| **Domanda** | «Questi due sono lo stesso apparato?» |
| **Evidenze** | chassis_id, MAC sibling, name_ambiguity |
| **Risposta** | Sì chassis / omonimi dichiarati / incerto |
| **Tempo** | Attuale 2–3. Obiettivo **≤2** da card chassis in Oggi |
| **Stato oggi** | **Parziale** (adopt 409; manca rename chassis) |

### CU-08 — Cosa fare per primo adesso

| Campo | Contenuto |
|-------|-----------|
| **Chi** | Operatore |
| **Domanda** | «Cosa devo fare per primo adesso?» |
| **Evidenze** | Coda Oggi ordinata |
| **Risposta** | Problema #1 con priorità, causa, azione, certezza |
| **Tempo** | Attuale **1 click**. Obiettivo **1 click** + card A.1 completa |
| **Stato oggi** | **Sì** (struttura) → A migliora leggibilità |

### CU-09 — Anomalia reale o rumore

| Campo | Contenuto |
|-------|-----------|
| **Chi** | Operatore sul bottone massa |
| **Domanda** | «Questa anomalia è reale o è rumore?» |
| **Evidenze** | Regole D12/D13/D3; N=41 scomposto |
| **Risposta** | Elenco cosa/perché prima di archiviare (senza eseguire) |
| **Tempo** | Attuale 1–2 ma **non spiegato**. Obiettivo **1** con anteprima motivata |
| **Stato oggi** | **Parziale** → A.5 |

### CU-10 — Porta da riconfermare (FDB move)

| Campo | Contenuto |
|-------|-----------|
| **Chi** | Operatore dopo FDB vs bind manuale |
| **Domanda** | «Devo spostare questo device di porta?» |
| **Evidenze** | Suggestion kind=move (oggi 0 pending; 19 rejected uplink) |
| **Risposta** | Card in Oggi: da→a, evidenza FDB, confidenza; approva/rifiuta |
| **Tempo** | Attuale: solo `/suggestions` orfana. Obiettivo **1** in Oggi |
| **Stato oggi** | **Per niente** in Oggi → A |

---

## Correzioni alla specifica

*(nessuna al momento della stesura)*
