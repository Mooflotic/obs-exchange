# obs-ux3 — Ultima ondata correttiva UI/UX (0.10.62 → 0.10.63)

Chiusura dei quattro difetti rinviati, esecuzione di ciò che UX2 non aveva eseguito,
decisione dell'architettura delle superfici. Metodo: interfaccia **esercitata** (resa reale
headless Playwright/Chromium = **R**; payload API reale di produzione = **A**). Nessun «OK» da
lettura di codice.

Base raw canale: `https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/`.

---

## 0. Ondate e assert di produzione

| Ondata | Versione | Contenuto | Assert (una riga) |
|---|---|---|---|
| 1 | **0.10.62** | D3 nav mobile · D4 troncamenti Impianto · D7 Topologia mobile | `needs_apply=false · structural=0 (piano1/2/3) · convergenza OK · breaker closed · observations=0 · version=0.10.62 · assets=151 ip_current=101 NP=408(77) FA=261(68) AD=68` |
| 2 | **0.10.63** | D8 Dashboard→Panoramica · `/`→`/oggi` · architettura superfici (findings/suggestions) | `needs_apply=false · structural=0 (piano1/2/3) · convergenza OK · breaker closed · observations=0 · I6 vuoto · version=0.10.63 · assets=151 ip_current=99 NP=408(77) FA=261(68) AD=68` |

Rollback ammesso: `v0.10.61` (prima dell'ondata), poi `v0.10.62`.

### Delta enumerati per id (non per conteggio)
- **assets 151 · NP 408 (pending 77) · FA 261 (current 68) · AD 68 · unknown_source 0 · breaker closed**: invariati in entrambe le ondate.
- **ip_current**: 100 (baseline 0.10.61) → **101** (0.10.62) → **99** (0.10.63). Entrambe le ondate toccano **solo frontend** (bundle web + `/VERSION`): nessun writer SQL/DB toccato → il delta **non è attribuibile al deploy**. È presenza Fritz live.
  - Baseline enumerabile congelata a 0.10.62 (101 id): `1,3,5,7,9,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41,43,45,47,49,51,53,55,57,61,65,67,69,73,78,79,81,83,85,87,89,91,93,95,97,99,101,103,105,108,109,111,113,115,117,119,121,123,125,127,129,131,132,134,135,136,137,138,139,140,141,144,145,146,147,149,151,152,153,154,156,157,158,160,161,162,163,164,165,166,167,168,169,170,171,227,853,855,858,859,860,861`.
  - A 0.10.63 **caduti** (baseline→ora): **ip_id 78** (`192.168.2.101`, asset 43, `source=fritz`) e **ip_id 108** (`192.168.2.195`, asset 58, `source=fritz`), entrambi `is_current=False` con `last_seen 2026-07-27 22:41:16` (stesso ciclo di osservazione Fritz). Nessun id aggiunto. Nuova baseline enumerabile per l'ondata successiva = i 99 id (baseline − {78,108}).

---

## 1. UX3.1 — I quattro aperti, chiusi (non in checklist)

### D3 — Navigazione mobile (sidebar ~280px) → **RIPARATO** (R)
- **Causa (frontend):** sotto 800px la sidebar diventava una barra a più righe: gli 11 link andavano a capo, occupando ~280px prima del contenuto.
- **Fix:** `App.vue` + `matrix.css`. Barra mobile compatta (**LAN Observatory · ☰ Menu · admin · Esci**); il menu si apre a comparsa a piena larghezza in colonna, tocco comodo, e si **chiude a ogni cambio rotta**. Desktop invariato. Nessun tocco a auth/ruoli (K10).
- **Verifica (R):** `obs-ux3-oggi-mobile.png` (barra collassata), `obs-ux3-nav-mobile-open.png` (menu aperto: tutte le voci raggiungibili). Test funzionale: hamburger apre il menu e il link Topologia è visibile (`nav_open_ok=true`).

### D4 — Troncamenti in Impianto → **RIPARATO ALLA RADICE** (R)
- **Causa condivisa (stessa *classe* di D2):** `white-space:nowrap` + `overflow:hidden` + ellissi su testo che deve andare a capo. In Impianto è testo semplice (non `DenseRow`).
- **Punti enumerati e corretti** (`Plant.vue`):
  1. `.fdb-status` — banner copertura FDB: **la data dell'ultima misura non va mai troncata** (F-13) → ora va a capo a **ogni** larghezza (`white-space:normal; overflow:visible`).
  2. `.switch-role` — ruolo/posizione switch → a capo su mobile.
  3. `.port-foot .patch` — etichetta patch porta → a capo su mobile.
- **Verifica (R):** `obs-ux3-plant-mobile.png` — banner integrale visibile: «Copertura FDB non aggiornata: ultima mappatura porte da FDB il **25/07/2026, 16:52:35 (circa 55 h fa)**…» senza ellissi.
- **Nota (K4):** `DenseRow` in prod è usato solo in `Oggi.vue` (già gestito, D2) e `AssetHabits.vue` (righe singole, nessun troncamento multilinea osservato). Nessun altro punto condivide la causa su contenuto multilinea.

### D7 — Grafo Topologia su mobile → **RIPARATO con rappresentazione alternativa** (R)
- **Causa (frontend):** il grafo è uno *stage* a coordinate assolute in un contenitore scroll; sotto 800px diventa una finestrella su una mappa grande → inutilizzabile.
- **Fix:** `Topology.vue` — sotto 800px il grafo è sostituito da una **lista gerarchica per livello** (Radice → Livello 1/2/3) che risponde alla stessa domanda («dove sta un apparato, a cosa è attaccato»). Riusa i nodi già posizionati da `layoutTopology`; per ogni nodo: nome canonico, IP/tipo, «↳ collegato a <padre>»; gli endpoint restano toccabili per isolarne il percorso. I controlli zoom (inerti senza grafo) sono nascosti su mobile.
- **Verifica (R):** `obs-ux3-topology-mobile.png` — lista con 46 righe, gerarchia con «↳ collegato a FRITZ 5690 Pro». Desktop invariato (`obs-ux3-topology-desktop.png`): grafo presente, lista nascosta (`desktop_graph_visible=true`, `topo_graph_hidden` su mobile=true).

### D8 — Dashboard fuori dalla navigazione → **DECISO CON LA MISURA ED ESEGUITO** (A+R)
- **Misura (A, `/api/dashboard`):** la Dashboard mostra ciò che **nessun'altra vista** mostra — stato calibrazione osservatorio (giorno **3/14**), **salute Internet** (capacità/traffico FRITZ!Box, speedtest NAS, prossimo test), copertura discovery, salute sensori, KPI device+monitor.
- **Decisione: (a) utile e distinta → entra in navigazione** come **«Panoramica»** (gruppo RADAR). Coerenza con F-9: `/` non è più la Dashboard ma **reindirizza a `/oggi`** (il cardine è la landing); la Dashboard vive su `/dashboard`.
- **Verifica (R):** `obs-ux3-dashboard-desktop.png`; smoke: `/`→`/oggi`, nav contiene «Panoramica», Dashboard raggiungibile con la card Internet.

---

## 2. UX3.2 — Architettura delle superfici (dati reali)

Conteggi di produzione (A, 2026-07-28) e decisione. Overlap = se elementi/azioni compaiono anche in Oggi.

| Route | Domanda | Elementi (prod) | Azioni | Overlap Oggi | Decisione |
|---|---|---|---|---|---|
| `oggi` | Cosa devo fare adesso | coda problemi (nomi 0/24/39, conflitti, chassis, move) | adotta/verifica/ignora + deep-link | — (è il cardine) | **TIENE** |
| `dossier/:id` | Tutto su un device | 1 device (identità, connessione, decidi, abitudini, note) | rinomina, note | apribile da Oggi (1 clic) | **TIENE** |
| `inventory` | Elenco/ricerca device | 113 asset (`/api/assets`) | filtri, apri dossier | no (Oggi è coda, non elenco) | **TIENE** |
| `plant` | Porte e patch (modifica) | switch + porte | modifica patch/ruolo/note | apribile da Oggi (move FDB) | **TIENE** |
| `topology` | Dove/come collegati | 46 nodi | seleziona endpoint | apribile da Oggi | **TIENE** |
| `monitoring` | Salute/reachability | 16 monitor + salute switch | (read-only poll) | apribile da Oggi | **TIENE** |
| `timeline` | Cronologia eventi | 100 eventi | — (storico) | no | **TIENE** |
| `actions` | Scansioni/errori discovery autorizzati | 2 richieste + storico scan | approva/esegui scan | no | **TIENE** |
| `dashboard` | Quadro rete/Internet/calibrazione | KPI + Internet + calibrazione | link a viste | no | **TIENE** (D8: in nav come Panoramica) |
| `suggestions` | Proposte nome | 2 pending | (via Oggi) | **sì** (redirect `/suggestions`→`/oggi`) | **CONFLUITA** (già) |
| `findings` | Findings compositi (shadow) | **0** findings, **0** drift | — | no (vuota, in shadow) | **CONFLUISCE (differita)** → tolta dalla nav |
| `osservatorio` / `come-funziona` | Teaser roadmap datati | 0 (stub) | — | no | **TIENE con riserva** (roadmap, vedi checklist) |

### Esecuzione (cosa spariva, dove ricompare, link aggiornati)
- **`suggestions`**: già confluita (redirect a `/oggi`). Le 2 proposte pending compaiono in Oggi («Nomi da decidere»). Nessuna voce di nav. Nessun link interno rotto.
- **`findings`**: **tolta dalla nav primaria** (`App.vue`). La route esiste ancora ed è **raggiungibile** dalla Dashboard (ReadySlot «Findings e severità → Apri Findings (shadow)» e card «Findings (shadow) → Apri») e per URL diretto — verificato R (`findings_still_reachable=true`). **Nessuna funzione operativa irraggiungibile** (UX3.2.4). Debito `DEBT-FINDINGS-OGGI-CONFLUENCE`: quando i findings diventeranno autoritativi (scoring calibrato, M4–M5) i loro elementi devono diventare problemi **dentro Oggi**, non una vista separata (F-9).
- **`dashboard`**: `/` → `/oggi`; nuova `/dashboard`; nuova voce nav «Panoramica». Nessun link interno a `/` come Dashboard (i KPI puntano a `/inventory`, `/monitoring`, `/incidents`, `/findings`, `/actions`, invariati).

> Route fuori nav non toccate (raggiungibili per URL/drill-down): `incidents` (storico, aperto da Panoramica/Monitor «Da gestire»), `runbook`, `ai` (percorso AI **non esercitato**: consuma API a pagamento — STOP legittimo).

---

## 3. UX3.3 — Ciò che UX2.4 non aveva eseguito (misurato su asset reali)

### 3.1 «Dossier: visualizza dati» (asset 3, 109, 4, 1) — **operativo, non un dump** (R)
Cosa mostra realmente (resa reale):
- **Asset 3 — LGS310C** (`obs-ux3-dossier-3.png`): «Presente ora · 192.168.1.7 · Vendor Switch Linksys · Tipo infrastruttura · **OS non rilevato · Hostname nessuno annunciato · Servizi nessuno osservato**». Nome **LGS310C** (manuale, F-1); **nessuna proposta OUI** su chassis 24 (F-1). Ignoti **dichiarati**, non inventati (I2).
- **Asset 109 — LGS328C** (`obs-ux3-dossier-109.png`): «Visto solo dal FRITZ!Box · **interfaccia di LGS328C** · Hostname Switch Centrale · Proposte nome (AI) «Switch Centrale» **INFERENZA AI · Confidenza 90% · Evidenze usate: vendor Linksys, stable attachment, infrastructure category · Può sbagliare — verifica**». F-5 (membro come interfaccia), F-2 (LGS328C non confermato, mostrato come inferenza non manuale), F-10/I1 (marcata, confidenza+evidenze).
- **Asset 4 — GS308EP** (`obs-ux3-dossier-4.png`): «Ramo GS308EP — **FATTO / Da confermare / inferenze etichettate**. Capacità switch: **SNMP no, FDB no**, poll manual_upstream. **IP gestione corrente 192.168.1.8 (fatto)**. In DB c'è anche 192.168.3.2[0]…». F-11 (`.1.8` corrente, `.3.20` storico), I7 (nessuna telemetria inventata).
- **Asset 1 — FRITZ!Box** (`obs-ux3-dossier-1.png`): «Vendor FRITZ!Box · OS Linux 4.15–5.19 · scelta manuale · Servizi DNS/HTTP/HTTPS/SIP · Presente ora».

**Conclusione:** il Dossier è **informazione operativa strutturata** (identità osservata, connessione, decidi, abitudini, note), non un dump grezzo. Caso d'uso: «tutto su un device, con ignoti dichiarati e inferenze marcate». **Nulla da rimuovere.**

### 3.2 Vista switch e strutture legacy — **modello coerente, nessuna vista legacy** (A+R)
Tre superfici sullo stesso oggetto `Switch`, ciascuna con domanda distinta e coerente:
- **Impianto = modifica** (porte, patch, ruoli).
- **Topologia = dove** (collegamenti/rami).
- **Monitor = salute** (reachability, poll SNMP read-only, «Switch · salute porte»).
Non esiste una route/vista switch **autonoma** superata (nessun `/switches` nel router). Nessun elemento duplicato da rimuovere; i tre insistono sullo stesso oggetto ma con funzioni disgiunte.

### 3.3 Dati grezzi senza valore operativo — **enumerati, nessuno di gravità operativa** (R)
- Dossier: nessun dump grezzo (vedi 3.1).
- Dashboard `ReadySlot` («Presenza», «Findings e severità», «Coda attenzione»): in calibrazione dichiarano **«Disponibile dopo la calibrazione»** — attesa onesta (I2), **non** dati inventati né barre mute. Annotati in `DEBT-DASHBOARD-READY-SLOTS`, non rimossi (slot di roadmap M3–M5).
- `Actions` mostra il valore grezzo di un hint scan (`source · value · confidence`): è diagnostica su una superficie da operatore, non nel flusso principale — lasciata.

---

## 4. UX3.4 — Rapidità (conteggio interazioni da `/oggi`, una volta)

Da `/oggi`, per la domanda tipica di ogni vista che TIENE:

| Vista | Domanda tipica | Sequenza da `/oggi` | Passi |
|---|---|---|---|
| Oggi | Cosa devo fare adesso | (sei già qui) — prima card = prima azione | **0** |
| Dossier(device) | Tutto su questo device | card Oggi → **apri Dossier** (`openDossier`) | **1** |
| Impianto(device) | Dove sta questa porta | card Oggi → **Impianto** (`openPlant ?asset=`) | **1** |
| Topologia(device) | A cosa è attaccato | card Oggi → **Topologia** (`openTopology ?asset_id=`) | **1** |
| Monitor(device) | È in linea? | card Oggi → **Monitor** (`openMonitor ?monitor=`) | **1** |
| Panoramica | Come sta la rete/Internet | nav → **Panoramica** | **1** |
| Inventario | Elenco/ricerca device | nav → **Inventario** | **1** |
| Timeline | Cosa è successo | nav → **Timeline** | **1** |
| Azioni | Scansioni/errori | nav → **Azioni** | **1** |
| Dossier(device non in Oggi) | Tutto su un device qualsiasi | nav → **Dossier** → cerca → apri | **3** |

Tutte ≤ 3 passi; le viste device-centriche sono a **1 clic** grazie ai deep-link già presenti nelle card di Oggi (`openDossier/openPlant/openTopology/openMonitor`, con `?from=oggi`). Nessuna riduzione ulteriore necessaria.

**UX3.4.3 (Oggi senza scroll esplorativo, tutti i breakpoint):** verificato R — la **prima card è la prima azione** su desktop (`obs-ux3-oggi-desktop.png`), tablet (`obs-ux3-oggi-tablet.png`) e mobile (`obs-ux3-oggi-mobile.png`). Su mobile la riga densa impila (label sopra, valore sotto, azioni sotto), niente troncamenti.

---

## 5. UX3.5 — Regressione e coerenza (resa reale)

- **D1 (Oggi mobile)**: risolto — `obs-ux3-oggi-mobile.png` (impila, nome/MAC non troncati).
- **D2 (Oggi tablet)**: risolto — `obs-ux3-oggi-tablet.png` (Causa/Impatto/Azione/Certezza/Esito a capo, leggibili).
- **D5 (copertura FDB Impianto)**: banner corretto con data — `obs-ux3-plant-mobile.png` / `-desktop.png`.
- **D6 (Monitor telemetria)**: `obs-ux3-monitoring-desktop.png` — LGS/GS308EP mostrano Traffico/Errori **«—»** e poll «non riuscito»/«—», nessun `0` inventato (I2/I7).
- **AI marcata (F-10/I1)**: «nome migliore», «MDNS · 60%», «fonte dns · confidenza 60%» in Oggi; «INFERENZA AI · Confidenza 90% · Evidenze usate» nel Dossier.
- **Caso LGS (F-1/F-2/F-3/F-5)**: chassis 23 = LGS328C con membri come interfacce (asset 109 «interfaccia di LGS328C»); chassis 24 = LGS310C manuale, **nessuna proposta OUI**; chassis non fusi.
- **GS308EP (F-11)**: `.1.8` corrente, `.3.20` storico, telemetria assente dichiarata.
- **Banner FDB (F-13)**: presente e corretto; nessun dato di porta presentato come corrente.
- **Nessuna card alta priorità senza azione**; nessun controllo mostrato se non eseguibile (verificato R su Oggi).
- **I6**: `rg 'scoreSpecificity|specificity' api/` → **vuoto** (mostrato in ondata 2).

---

## 6. UX3.6 — Lista di controlli per Michele (solo gusto / impossibilità materiale)

Nessun difetto funzionale (K11): sono già tutti riparati. Restano scelte di gusto e priorità percepita.

1. **Oggi**: la **prima card** in cima è davvero quella su cui agiresti per prima? (priorità percepita)
2. **«Panoramica»** come nome della ex-Dashboard in nav ti è chiaro, o preferisci «Dashboard»/«Rete»? (gusto)
3. **Osservatorio** e **«Come funziona»** sono teaser datati (radar ~30/07, guida ~agosto): tenerli in nav come conto alla rovescia o nasconderli finché non escono? (gusto/roadmap)
4. **Topologia mobile**: la lista gerarchica ti basta, o vuoi anche il pinch-zoom sul grafo? (gusto)
5. **Findings** tolta dalla nav (0 elementi, in shadow, raggiungibile da Panoramica): d'accordo o la rivuoi in nav? (priorità percepita)
6. **Densità/spaziatura** delle card di Oggi su desktop: troppa aria o giusta? (gusto)
7. **Badge inferenza AI** («nome migliore» / confidenza): abbastanza distinto dai fatti misurati a colpo d'occhio? (gusto)
8. **Raggruppamento nav** (RADAR / MAPPA) e ordine delle voci: ti convince? (gusto)

---

## 7. Debiti registrati / invariati
- **`DEBT-FINDINGS-OGGI-CONFLUENCE`** (nuovo): confluenza autoritativa findings in Oggi rinviata a calibrazione/scoring; route raggiungibile nel frattempo.
- **`DEBT-DASHBOARD-READY-SLOTS`** (nuovo): slot roadmap M3–M5 con etichetta d'attesa (I2), non rumore.
- **`DEBT-FDB-POLL-STALE`**, **`DEBT-PRESENCE-SOURCE-OUTAGE`**, **`DEBT-MAC-IP-POLICY-WIRE`**: invariati, aperti.

## 8. Vincoli rispettati
F-1..F-14 · I1..I7 · K1..K11. Nessun secondo autore di stato (F-7); policy MAC↔IP resta consultiva (F-12); I5/F-8 immutati; favicon A (F-6); nessuna logica di identità/currency nel frontend; nessun hub separato (F-9); auth/ruoli/CSRF non toccati (K10); venv Playwright non committato.

**STOP.** Dopo la review arriva **W8** (enforcement).
