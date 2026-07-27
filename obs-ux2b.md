# obs-ux2b — Revisione UI/UX ESERCITATA (UX2)

Corrente a fine ondata: **0.10.61**. Metodo: interfaccia **esercitata**, non letta.
Deploy in questa ondata: **0.10.60** (onestà dati porta/telemetria + Oggi mobile) e
**0.10.61** (Oggi tablet, radice DenseRow).

Come è stata esercitata (UX2.0.1):
- **(R)** resa reale in browser headless (Playwright/Chromium locale, sessione admin
  legittima) con screenshot allegato al canale. 12 route × 3 breakpoint = **36 screenshot**
  a 0.10.61, 0 errori console, tutte le richieste API 200.
- **(A)** payload API reale di produzione osservato durante la resa (mappa richieste/stati
  per cella) e query mirate read-only.
- **(N)** non verificato a runtime (dichiarato per route).

> Nessuna cella «OK» senza metodo. Non è una matrice tutta OK: i difetti trovati sono
> enumerati (§3), tre risolti e verificati via R, quattro dichiarati aperti/checklist.

---

## 1. Corrispondenza route → viste (App.vue / router.js)

Gruppo nav **RADAR**: `/oggi` (Oggi) · `/osservatorio` (stub) · `/dossier` + `/dossier/:id`
(Dossier) · `/come-funziona` (stub).
Gruppo nav **MAPPA**: `/inventory` (Inventario) · `/plant` (**Impianto = le porte**) ·
`/topology` (Topologia) · `/monitoring` (Monitor) · `/timeline` · `/findings` · `/actions` (Azioni).
Altre: `/` (Dashboard calibrazione/sensori/flussi, **non in nav**) · `/incidents` · `/runbook`
· `/ai`. Redirect: `/suggestions → /oggi`, `/monitor → /monitoring`.

«Mappa» (UX2.2.1) = gruppo nav composito; **le porte sono in `/plant` (Impianto)**.

## 2. Matrice metodo (vista × breakpoint)

R = screenshot allegato (0.10.61) · A = payload reale osservato · N = non verificato.
File screenshot: `obs-ux2b-<route>-<breakpoint>.png` (piatti in root del canale, §7).

| Route | mobile | tablet | desktop | Note sintetica |
|---|---|---|---|---|
| /oggi | R+A | R+A | R+A | cardine; card con azioni; inferenze AI marcate; mobile/tablet **riparati** |
| /dossier/109 (LGS328C) | R+A | R+A | R+A | membro chassis 23; nome canonico, AI «Switch Centrale» marcata |
| /dossier/3 (LGS310C) | R+A | R+A | R+A | chassis 24; manuale (F-1); «Cosa manca» dichiarato |
| /inventory | R+A | R+A | R+A | conteggi + «Non visti · copertura non disponibile» |
| /plant (Impianto) | R+A | R+A | R+A | **banner copertura FDB** (F-13); GS308EP dichiarato |
| /topology | R+A | R+A | R+A | «endpoint non collocati» dichiarato; grafo mobile degradato |
| /monitoring | R+A | R+A | R+A | telemetria assente = «—» (I2/I7) |
| /findings | R+A | R+A | R+A | — |
| /actions | R+A | R+A | R+A | — |
| /timeline | R+A | R+A | R+A | — |
| / (Dashboard) | R+A | R+A | R+A | calibrazione/sensori/flussi; **non in nav** (D8) |
| /osservatorio | R+A | R+A | R+A | stub datato dichiarato |
| /come-funziona | N | N | N | stub datato (stessa natura di /osservatorio) |
| /dossier (senza id) | N | N | N | landing indice; l'operativo è /dossier/:id |
| /incidents /runbook /ai | N | N | N | viste secondarie, non nel giro RADAR/MAPPA |
| /suggestions /monitor | — | — | — | redirect (→/oggi, →/monitoring) |

## 3. Mappa difetti (componente · riproduzione · causa · gravità · origine · esito)

| ID | Componente / riproduzione | Causa | Gravità | Origine | Esito |
|---|---|---|---|---|---|
| D1 | Oggi card @mobile (390): nome/MAC troncati, label/valore non impilati | `DenseRow` flex non impila + `.oggi-fields` colonna fissa `9.5rem 1fr` | rotto | frontend | **RISOLTO 0.10.60** (R) |
| D2 | Oggi card @tablet (820): valori tagliati a metà parola | slot primario `DenseRow` con `white-space:nowrap`+`overflow:hidden` su contenuto multilinea | rotto | frontend | **RISOLTO 0.10.61** (R) |
| D3 | Sidebar resa come blocco in cima @mobile: ~280px prima del contenuto (tutte le route) | layout responsive della sidebar | degradato | frontend | **APERTO** → checklist C7 |
| D4 | Impianto @mobile: helper toggle e riga errore SNMP troncati senza wrap | testo lungo non mandato a capo nell'header switch | cosmetico | frontend | **APERTO** → checklist C8 |
| D5 | Impianto/Topologia/Monitor: dati porta vecchi presentati come correnti; badge switch «dati al …(ok)» = ora del poll **fallito** | `switchFreshness` usava `fdb_poll.at` con `ok:false` | degradato | a monte (copertura ferma, F-13) + presentazione frontend | **RISOLTO presentazione 0.10.60** (banner + badge reale); copertura resta ferma → `DEBT-FDB-POLL-STALE` |
| D6 | Monitor «salute porte»: traffico `0 b/s` ed errori `0` per switch senza SNMP | celle rendevano 0 invece di «—» | degradato (I2/I7) | frontend | **RISOLTO 0.10.60** (R) |
| D7 | Topologia @mobile (390): grafo non chiaramente usabile (canvas parziale) | rendering grafo su viewport stretto | degradato | frontend | **APERTO** → checklist C9 |
| D8 | Dashboard `/` non raggiungibile dalla nav (parte da Oggi) | `/` orfano in nav | cosmetico/navigazione | frontend | **DICHIARATO** (default landing; non in nav) |

## 4. Riparazioni fatte (verificate via R)

- **UX2.2.4 / F-13 — copertura FDB dichiarata (0.10.60).** Helper puro `fdbCoverageStatus()`
  (`observatoryUx.js`, con test) calcola la freschezza dalla `last_fdb_at` di porta, **mai**
  dall'ora del poll fallito. Impianto ora mostra: banner «*Copertura FDB non aggiornata:
  ultima mappatura porte da FDB il 25/07/2026, 16:52:35 (circa 55 h fa). La collocazione delle
  porte mostrata può non essere corrente.*» e badge per-switch «*mappa porte da FDB del
  25/07 — non aggiornata*» (poll fallito mostrato a parte). Solo presentazione: nessuna
  diagnosi/riavvio del polling (F-13). Debito registrato `DEBT-FDB-POLL-STALE`, collegato a
  DEBT-PRESENCE-SOURCE-OUTAGE e DEBT-E3-AVAILABLE-FALSE.
- **UX2.5 / I2 / I7 — Monitor: assente ≠ zero (0.10.60).** In «Switch · salute porte»
  traffico ed errori sono `—` quando `snmp_poll.ok≠true` (LGS328C/LGS310C in timeout, GS308EP
  non interrogabile); ultimo poll marcato «· non riuscito». Nessuna telemetria a 0 finta.
- **UX2.1 / UX2.5 — Oggi responsive (0.10.60 mobile, 0.10.61 tablet).** Le card impilano su
  mobile (azioni sotto, campi label-sopra-valore, nome/MAC a capo) e non troncano più il
  contenuto multilinea su tablet (override dello stile generico di DenseRow dentro `.oggi`).

## 5. Oggi, il cardine — verifica su dati reali (UX2.1)

- **Priorità/azioni:** ogni card dichiara apparato (nome canonico), «Priorità», «Causa ed
  evidenza», «Impatto», «Azione raccomandata», «Certezza», «Esito», con azioni eseguibili
  (adotta/ignora/apri Dossier, + Impianto/Topologia). Non osservate card alta priorità senza
  azione. Sezioni presenti: «Nomi da decidere» (adotta consigliati / da verificare / rumore),
  conflitti R-H come problemi con azione, «Porte da confermare» (ex-suggestions/FDB move dentro
  Oggi, F-9). Chassis/upgrade nome/move FDB vivono in Oggi, nessun hub separato.
- **Inferenze AI marcate (F-10/I1):** verificato su dati reali. In Oggi la proposta «Sky → PC
  CabinaArmadio» porta badge **«INFERENZA AI · Confidenza 88%»** con «Evidenze usate…» e «Può
  sbagliare — verifica…», graficamente distinta dalle proposte da sorgente misurata (es. «fonte
  dns · confidenza 60%», «OUI · 85%»). Nel Dossier 109 l'AI «Switch Centrale» ha badge
  **«INFERENZA AI · Confidenza 90%»** + evidenze + disclaimer.
- **Caso LGS (UX2.1.6), valori ricevuti:**
  - Chassis 23 → **LGS328C**: Dossier del membro 109 mostra titolo «LGS328C», sottotitolo
    «*interfaccia di LGS328C · — · D8:EC:5E:CC:1C:01*», presenza «Visto solo dal FRITZ!Box».
    La resa ha caricato i membri chassis 23 (asset 2, 147, 151, 109). Il nome **grezzo** del
    membro è vuoto (F-5); si mostra il **canonico** «LGS328C», **non marcato manuale** (F-2:
    resta `unknown_nonempty`).
  - Chassis 24 → **LGS310C**: Dossier asset 3 «LGS310C · Presente ora · 192.168.1.7» (manuale
    confermato, F-1). La resa ha caricato i membri chassis 24 (asset 3, 143). **Nessuna
    proposta OUI** emersa per il chassis 24 in Oggi.
  - Nota misurata: la sezione «Adotta consigliati» è passata da 1 a **0** (la proposta OUI
    «Switch Linksys» pending è la riga NP scomparsa, vedi §6). Nessuna card alta priorità senza
    azione.

## 6. Assert di produzione (dopo ogni deploy)

Assert 0.10.61 (una riga):
`v0.10.61 · needs_apply=false · structural=0 · observations_in_sqlite_master=0 ·
breaker=closed · convergenza OK (piano→apply→rebuild, now ricalcolato → structural==[]) ·
assets=151 · ip_current=100 · NP=408(pending=77) · FA=261(current=68) · AD=68`
(`needs_apply=false` ⇒ nessun backup trust pendente; `T_total` non è un gate: al boot 0.10.61
il passo trust ha applicato structural=1 emerso dallo scorrimento della finestra 24h e ha poi
riconvergo — wp_gate post-boot: structural=0.)

**Delta contatori vs baseline 0.10.59 (NP 409/pending 78 → 408/pending 77):** −1 totale **e**
−1 pending ⇒ **rimozione di una riga di proposta pending** (non una transizione di stato: le 5
transizioni non-pending più recenti datano 2026-07-25, nessuna da questi deploy). Coerente con
«Adotta consigliati» passato da 1 a 0 in Oggi: la proposta OUI «Switch Linksys» pending non
c'è più (pruning/manutenzione, non causata da questa ondata solo-frontend). L'id esatto è
**irrecuperabile** per lo stesso motivo del 52→53 (la baseline era un totale, non una lista).
**Baseline enumerabile registrata ora** (77 id pending, per rendere il prossimo delta per id):
`46,53,68,73,98,149,150,185,187,208,212,215,217,219,223,224,227,231,233,236,242,245,247,249,
251,253,255,257,261,274,279,286,299,300,301,302,303,304,307,308,309,318,319,320,321,322,323,
324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,353,355,372,
374,375,381,393,395,400,414`.
`unknown_source`: non rimisurato in questa ondata (nessun codice sorgente-sorgenti toccato);
baseline 0.

Assert 0.10.60 (una riga): `v0.10.60 · needs_apply=false · structural=0 · observations=0 ·
breaker=closed · convergenza OK · assets=151 · ip_current=100 · NP=408(77) · FA=261(68) · AD=68`.

## 7. GS308EP (UX2.3) — misurabile senza inventare

Verificato via R (Impianto/Monitor/Topologia) + A. Presente e dichiarato: nome/modello, IP
gestione **corrente .1.8** (fatto), mappa porte manuale, ramo a valle da FDB/LLDP upstream con
nota, reachability. Dichiarato NON disponibile (I2/I7): FDB proprio, contatori/PoE, traffico
locale — resi come «FDB non disponibile», «SNMP non disponibile», **traffico/errori «—»** in
Monitor (non 0). L'indirizzo storico **.3.20** è marcato come storico/non corrente, con la nota
ownership. Nessuna barra muta, nessun numero finto. F-13 si applica anche alla confidenza del
ramo (FDB core vecchio → banner in Impianto).

## 8. Legacy e rumore (UX2.4)

- **Dossier per-asset:** **operativo, non dump grezzo** — «Chi sei», sintesi identità (Cosa
  sappiamo / Fonti / Freschezza / Incerto/Cosa manca), proposte nome con azioni. Si tiene.
- **Dashboard `/`:** calibrazione + salute sensori + SPAN/flussi (beta). Non ridondante con
  Oggi, ma **non raggiungibile dalla nav** (D8) — dichiarato (default landing).
- **`/osservatorio`, `/come-funziona`:** stub con disponibilità datata dichiarata — placeholder
  accettabili, si tengono dichiarati.
- **SPAN su Dashboard:** contatori grezzi (`flow_observations`, pending) ma etichettati «dati
  descrittivi — baseline in calibrazione». Accettabile in calibrazione; da rivedere alla fine
  della finestra (debito leggero, non rimosso ora).
- Nessuna rimozione in questa ondata (scelte di navigazione/rimozione = giudizio di Michele,
  checklist C10-C12).

## 9. Vincolo architetturale (UX2.6) e gate I6

- Nessuna logica di **identità o correntezza** implementata nel frontend. `fdbCoverageStatus()`
  è **presentazione** di timestamp misurati (`last_fdb_at`), non derivazione di stato/currency;
  la soglia 24h rispecchia `ASSET_STALE_AFTER_HOURS`. La policy MAC↔IP resta **consultiva**
  (F-12), mai esposta come stato del device in UI.
- **Gate I6:** `rg 'scoreSpecificity|specificity' api/` → **output vuoto** (nessun file).

## 10. Test (solo nodi nominati, dopo deploy che tocca quel codice)

`observatoryUx` (nuovo caso `fdbCoverageStatus`, F-13), `oggiTriage`, `oggiProblems`,
`portPresentation`, `topologyLayout` → **40 verdi** (0.10.60); ri-eseguiti `oggiTriage`,
`oggiProblems`, `observatoryUx` → **28 verdi** (0.10.61). Nessuna suite completa, nessun altro
nodo, nessuna temporizzazione.

## 11. Lista di controlli per Michele (UX2.8)

Una riga, risultato atteso — per ciò che solo tu puoi giudicare o non ho potuto esercitare:

1. Apri **/oggi**: la prima card è davvero quella su cui agiresti per prima? (priorità percepita)
2. **/oggi**: le card sono troppe/troppo lunghe? Serve un limite «senza scroll» più stretto?
3. **/oggi** su telefono: nome, testo e pulsanti sono leggibili e toccabili? (atteso: sì, riparato)
4. **/oggi** su tablet: i valori delle card non sono più tagliati? (atteso: sì, riparato)
5. **/plant (Impianto)**: il banner «copertura FDB non aggiornata … 55 h fa» è chiaro e non allarmante oltre il dovuto?
6. **/monitoring**: traffico/errori «—» per gli switch senza SNMP sono comprensibili come «non disponibile»?
7. **Menu laterale su telefono**: occupa troppo spazio prima del contenuto? (D3, non risolto — decidi se comprimerlo)
8. **/plant** su telefono: le righe di stato switch troncate danno fastidio? (D4)
9. **/topology** su telefono: il grafo è usabile o va ripensato per lo schermo stretto? (D7)
10. **/** (Dashboard): la vuoi raggiungibile dal menu o va bene solo come pagina iniziale? (D8)
11. **/osservatorio** e **/come-funziona**: gli stub «disponibile dal …» vanno tenuti o nascosti fino al rilascio?
12. **Dossier**: la sintesi identità è al giusto livello di dettaglio o va alleggerita?

## 12. Dipendenze rinviate / debiti

- `DEBT-FDB-POLL-STALE` (nuovo): copertura FDB ferma, resa visibile; ripristino polling fuori
  scope UX2 (F-13).
- `DEBT-MAC-IP-POLICY-WIRE §F-14`: wire additivo inerte per costruzione (registrato).
- D3/D4/D7/D8: difetti frontend aperti, in checklist per decisione di layout/priorità di Michele.
- Guida d'uso: `obs-guida-uso.md`.

## 13. Screenshot (canale, file piatti in root)

Base: `https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/`. 36 file a 0.10.61:
`obs-ux2b-<route>-<breakpoint>.png` con route ∈ {oggi, dossier-109, dossier-3, inventory,
plant, topology, monitoring, findings, actions, timeline, dashboard, osservatorio} e breakpoint
∈ {mobile, tablet, desktop}. URL raw ed esito curl: vedi risposta di consegna.
