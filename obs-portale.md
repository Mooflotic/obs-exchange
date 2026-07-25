# OBS-PORTALE — report chiusura

**Branch:** `feature/obs-portale` · **Ultimo bump:** `v0.10.33` = `71322ec`  
**Live:** health `0.10.33` · regime T_total ≈ 8.8–9.0 s · `needs_apply=false` · `T_backup=0`  
**Data:** 2026-07-25

---

## Prossimo cantiere (in testa)

1. **Verifica prune raw 0a.1** — atteso ~**2026-07-27**. Predizione falsificabile: ~173 530 righe cancellate, freelist 0.30–0.37 GiB. Confrontare `store.before/after` + log `[retention]` con previsto. (Oggi 2026-07-25: non ancora avvenuto.)
2. **Gesto manuale Michele — «Archivia rumore»** con **N = 41** (rimisurato post-0.10.33 con `all_proposals=true`; il ≈39/2 storici sono obsoleti). **Non eseguito** in questo cantiere.
3. **Audit UX (handoff sotto)** — redesign / rimozione dump grezzo Dossier / unificazione switch / Oggi come coda unica; **dopo** review, un cantiere alla volta (grafica ≠ hot/cold).
4. **Debiti ancora aperti** (dopo PORTALE): `DEBT-AGGREGATE-NO-RETENTION`, `DEBT-FINGERBANK-027` (rimandato ≥2026-08-15), `DEBT-AUTOVACUUM-NOT-SET` (criterio residuo post-prune), `DEBT-BACKUP-ALL-OR-NOTHING`, `DEBT-PRIVACY-MAC-CHURN`, `DEBT-PYTEST-COLLECTION-PY39`, `DEBT-MAC-REGEX-DIGIT-RUN` (verificata 0 hit — regex invariata), rename chassis (residuo adopt).
5. **STOP** funzionale PORTALE: nessun redesign improvvisato qui.

---

## FASE 0a / 0b

Vedi `docs/obs-portale-triage.md`. Sintesi: prune non ancora; AUTOVACUUM soglia residuo >512 MiB×7g post-48h; aggregate senza retention (debito); Δ file **1 024 393 216**; E8 +1 asset 43 Sky + scan anonimi 85/98.

Ordine ondate **confermato dai numeri** (j=0 → verify-only).

---

## Ondata 1 — 0.10.31 (`eed5580` / tag `v0.10.31`)

| Assert | Esito |
|--------|-------|
| W1 health 0.10.31 | PASS |
| W2 regime ~9s, needs_apply=false, T_backup=0 | PASS (9.019 s) |
| W3 quattro assenze dichiarate | PASS |
| W4 assets 151, NP 412 | PASS |

Chiusi: MANUAL-CONF-BAR, VERSION-SILENT-FALLBACK, HABITS-DIR-UNAVAILABLE, CHASSIS-PARTIAL-SILENT.  
Report: `obs-portale-w1.md` (curl 200).

---

## Ondata 2 — 0.10.32 (`f534536` / tag `v0.10.32`)

| Assert | Esito |
|--------|-------|
| W1/W2 | PASS (regime 8.897 s) |
| W5 ssdp pending 10→4 | PASS (4 Fritz strip + 6 banner archive) |
| W6 nomi adottati invariati | PASS (0 cambi) |

Gate equivalenza: 17 NP changed (enumerate in `obs-portale-w2.md`); OUI floor ≥0.7; OS equiv solo nmap; Sky `name_ambiguity`; digit-run 0 hit → regex invariata.  
Report: `obs-portale-w2.md` (curl 200).

---

## Ondata 3 — 0.10.33 (`71322ec` / tag `v0.10.33`)

| Assert | Esito |
|--------|-------|
| W1/W2 | PASS (regime 8.833 s) |
| W7 coda Oggi + N massa | PASS — pending mostrate **118**; **Archivia rumore N = 41** |
| W8 no scoreSpecificity in Python | PASS (`grep` api/ vuoto) |

Move FDB uplink: **19→0** pending (`target_not_access_port`). Adopt chassis → 409. Anti-ricreazione rejected.

---

## Ondata 4 — decisioni

### 4.1 Fingerbank 027
**Rimandare** (non integrare ora). Branch `feature/obs-fingerbank-027` tip `d20313e` (~1.1k LOC: client + cache + DHCP opt55). Costo alto (secret, API, Zeek wire). Cantiere dedicato **non prima del 2026-08-15**. Debito: `DEBT-FINGERBANK-027`.

### 4.2 DNS hysteresis
**Rimuovere / già rimossa.** Il gate Observation dns è stato tolto in 3b-iii; il codice `endpoint.missing` non consulta più DNS. Dichiarato morto: `DEBT-DNS-HYST-LEGACY-NOOP` **CHIUSA**. Nuova isteresi solo con sorgente calda misurabile.

### 4.3 KNOWN_DEBT
Chiuse in PORTALE: presentazione (f/g/h/i), OS-PREFIX, PROPOSALS-HIDDEN, ADOPT-CHASSIS, NO-RECREATION, DNS-HYST.  
Verificata: MAC-DIGIT-RUN (0 hit).  
Aperte/rimandate: AGGREGATE-NO-RETENTION, FINGERBANK-027, AUTOVACUUM (criterio nuovo), ecc.

---

## Verifica prune 0a.1

**Non ancora** (misura 2026-07-25; atteso ~2026-07-27). Resto come punto 1 del prossimo cantiere.

---

## Merge / tag / produzione

- Merge `feature/obs-portale` → `main`
- Tag di produzione = ultimo bump VERSION: **`v0.10.33`** = `71322ec`
- Evidenza: `GET /api/health` → `0.10.33` · curl web/health 200

---

## Handoff UX obbligatorio (sola lettura — nessun redesign in PORTALE)

**Vincolo:** il cantiere funzionale è chiuso. Qui solo misura e documentazione per il **prossimo prompt UX Claude** (audit completo). Nessuna telemetria inventata; ogni conclusione non certa = **inferenza AI** con evidenze e confidenza.

### Vincoli per il prompt UX

1. Mental model switch: **Impianto = edit**, **Topologia = dove**, **Monitor = salute** — non tre “home” dello stesso oggetto; GS308 = scheda ramo opaco, non faux-SNMP.
2. **Oggi = unica coda operativa**: naming + (futuro) move FDB + chassis come *problemi/azioni*, non percorsi autonomi / pagine separate.
3. Deprecare/nascondere `/suggestions` dopo migrazione azioni in Oggi/Dossier.
4. **Rimuovere** «Dossier → Mostra dettagli tecnici» (dump JSON grezzo) — richiesta esplicita utente (`AssetIdentity.vue` L309–314 → `api.assetIdentity(id, technical=true)`).
5. Non inventare telemetria porte sul 308; solo upstream FDB, ping, mappa manuale, endpoint del ramo.

---

### (1) Strutture legacy residue — focus vista switch

**Routes** (`web/src/router.js`):

| Path | View | In nav? | Ruolo |
|------|------|---------|-------|
| `/oggi` | Oggi | RADAR | Coda triage |
| `/dossier/:id` | Dossier | RADAR | Scheda device |
| `/inventory` | Inventory | MAPPA | Lista |
| `/plant` | Plant | MAPPA «Impianto» | Porte/patch + edit |
| `/topology` | Topology | MAPPA | Grafo |
| `/monitoring` | Monitoring | MAPPA «Monitor» | Ping + pannello SNMP switch |
| `/suggestions` | Suggestions | **No (orfana)** | Coda `Suggestion` (move/rename) |

**Tre superfici sullo stesso `Switch` (sovrapposizione):**

| Vista | API | Cosa | Stato |
|-------|-----|------|-------|
| Impianto | `GET /api/switches`, `PATCH /api/ports/{id}` | Griglia porte, FDB, chip GS308, drawer | Corrente edit |
| Topologia | `GET /api/topology` | Albero, ramo opaco 308 | Corrente “dove” |
| Monitor · Switch | stessi switches | Aggregati SNMP; 308 → «non disponibile» | Duplicato parziale salute |

**API/models:** `Switch`/`SwitchPort` canonici; `Suggestion(kind=move)` vs `NameProposal` (Oggi) = due code “proposta”; `PatchPanel`/`PatchPort` solo DB senza UI. Move generate in `topology.py` `_ensure_move_suggestion` (post-0.10.33: 19→0 pending uplink).

**Legacy raggiungibili fuori nav primaria:** Suggestions, Dashboard/Incidents/Ai/Runbook; ingest `POST /fdb` etichettato legacy nel poll_id.

---

### (2) Caso «308» (GS308EP) — senza SNMP

**Fatto dichiarato in codice:** `switch_capabilities` → `snmp_supported=false`, `fdb_supported=false`, `poll_method=manual_upstream`. Asset **4**; IP mgmt `.1.8` (ping); `.3.20` inventariale (KNOWN_DEBT drift). Topology: `inferred_branch`, «porta interna non rilevabile».

| Dato | Affidabile senza SNMP? | Evidenza |
|------|------------------------|----------|
| Nome/modello GS308EP | Sì | riga switches + asset |
| Reachability `.1.8` | Sì | monitor ping |
| Mappa porte **manuale** Plant | Sì se curata | `source=manual` |
| MAC ramo su uplink a monte (FDB core) | Sì come “dietro il 308” | confidenza codice **0.65** |
| Porta **interna** sul 308 | **No** (salvo override) | README + Topology |
| LLDP lato core verso 308 | Sì sul core | `port_roles` |
| Contatori porte / PoE / NSDP | **No** | capabilities |
| Traffico switch-locale rx/tx | **No** | Monitor vuoto |
| MAC/OUI/fingerprint endpoint *dietro* | Sì se visti altrove | pipeline asset |
| Flows SPAN del ramo | Possibile | **Inferenza AI** (conf. bassa): carico “del ramo” ≠ telemetria del 308; serve aggregazione MAC/IP ∩ uplink non esposta oggi |
| Flapping porte sul 308 | **No** | senza SNMP |

**Sintesi UX derivabili (non inventate):** scheda ramo (N endpoint su uplink + freschezza FDB); salute = solo ping + freschezza edit Plant; inventario ramo via `inferred_branch`; gap esplicito porta interna.  
**Inferenza da non presentare come fatto:** PoE/load, porte interne da pattern, “traffico del 308” da SPAN senza join esplicito.

---

### (3) Vista Oggi — chassis / upgrade / FDB

**Conferma architetturale:** chassis, upgrade nome e overhaul/move FDB **non** sono percorsi operativi centrali autonomi; sono **problemi/azioni della vista Oggi** da rendere leggibili, contestualizzati e risolvibili lì (o nel Dossier collegato).

| Tema | In Oggi oggi? | Come |
|------|---------------|------|
| Proposte nome (adotta/verifica/rumore) | Sì | `triageRules` + `all_proposals` |
| Chassis (naming multi-NIC) | Sì · Verifica | `verdict=chassis`; adopt 409; **nessun rename chassis** |
| Upgrade nome | Sì | `verdict=upgrade` / `manual-upgrade` |
| Nuovi + monitor down | Sì · «Altro» | deep-link Monitoring |
| Suggestion `move` / FDB | **No** | resta `/suggestions` orfana + Plant |

**Gap per audit UX:** jargon Verifica (`collide`, `sotto-soglia`); chassis apre Dossier senza spiegare multi-NIC; nessuna card «porta da confermare»; NameProposal vs Suggestion; N massa rumore = **41** (fragile da spiegare); manca azione «apri Impianto/Topologia» dalla riga.

**Use case futuri (dipendenze):** adopt/reject NP; bulk rumore; `GET /api/chassis`; suggestions move + Plant; Topology `?asset_id=`; monitors.

---

### STOP

Misura e handoff sopra sono il deliverable. **Nessun redesign** in questo follow-up. Il prossimo prompt UX implementa l’audit completo (inclusa rimozione dump grezzo Dossier).
