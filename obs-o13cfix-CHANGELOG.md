# Changelog

## 0.10.80 — OBS-EGRESS O13C-FIX: baseline prematura, criteri B2, switch novità

- **B1:** baseline prematura invalidata (annotata, non cancellata); emissioni N5 su ready falso marcate `emitted_on_invalid_baseline` (246 in prod), ripescabili.
- **B2:** chiusura solo con copertura ≥3d + serie novità ≥3 giorni UTC completi (fonte O13B M1); vietato `deferred==0`.
- **B3:** rollback riapre `in_costruzione` (mai pronta per assenza di storia).
- Switch `EGRESS_NOVELTY_SIGNALS_ENABLED` distinto da ingest; default false. Oggi mostra readiness mancante + conteggio emissioni invalide.
- Marker bundle `obs-o13c-fix-marker`; endpoint `/api/egress/invalid-baseline-emissions`.


## 0.10.79 — OBS-EGRESS O13C: hybrid grain (ext host+port / int relazione)

- **Grano:** `ext` = (subject, dst_ip, dport, proto); `int` = (subject, peer_subject) senza porta/proto.
- **Cap ≠ breaker:** cap 2000 create/giorno (defer, non drop); breaker 20k/2k/50MiB (stop create).
- **Baseline:** `in_costruzione` finché un ciclo chiude con `deferred==0` → auto ready; nessun segnale novità prima.
- Collector `zeek-egress` + `EGRESS_INGEST_ENABLED` (default false); **non** riattiva `FLOW_INGEST` / `flow_observations`.
- Oggi E-N (P6), Dossier Cosa fa + inferenza destinazioni; coverage `zeek_egress`; retention `obs_ttl_raw_days`.


## 0.10.78 — OBS-COVERAGE O12-FIX: gate, attic oneshot, P7, SensorRun Zeek

- **K1/K2:** violazione reale `_o11fix_postcheck.py` (non «temporanea»): archivio recuperabile + `mv` in `_attic/`; gate `VIOLAZIONI: 0`; `DEBT-ONESHOT-SCRIPT-RESIDUE`.
- **K3:** P7 = `igiene_nome` dichiarato in legenda UI P1–P7 (allineamento modulo↔copy).
- **K4:** esiti ciclo `zeek_behavior` / `zeek_conn_flow` / `zeek_intel` / `zeek_dhcp_names` → `SensorRun`; card C-S mostra errore reale o «ultimo errore non registrato».
- **K5:** diagnosi `SNMP_NAS_*` (ABSENT in `.env` corrente; caduta con evento 25–27/07) → annotata in `DEBT-ENV-NO-INTEGRITY-CHECK`; nessuna riattivazione.


## 0.10.77 — OBS-COVERAGE O12: nessuna sorgente muore in silenzio

- **C1–C3:** censimento sorgenti enumerato + modello `coperta_fresca|coperta_vecchia|cieca|disabilitata|cadenza_non_nota`; segnali persi derivati dalle spec.
- **C4:** card Oggi C-S (cieca/vecchia, P4 `sorgente_non_disponibile`) e C-D (disabilitata, informativa P7); pannello Impianto riusa FRESHNESS/VisualBadge.
- **C5:** test negativo R4 (card appare/sparisce) + R3 disabilitata senza allarme.
- **C6:** `flow_observations` classificata (no riattivazione — O13); accertamento flag in report.
- Debiti: lezione contatore `archived_*` vs `db.delete`; `DEBT-BI-P6-VISIBILITY`.


## 0.10.76 — OBS-BEHAVIOUR O11-FIX: kill switch, retention, validità, B-I

- **F8:** rimossa mutazione boot non dichiarata (`reconcile_chassis_name_proposal_suppression`); soft-archive w4a ispezionabile/ripescabile; `DEBT-UNDECLARED-BOOT-MUTATION`.
- **G1–G3:** `ZEEK_BEHAVIOR_ENABLED` + intervallo proprio; docstring cold-start onesta; rotazione log con inode + conteggio.
- **G4:** retention `zeek_behavior_evidence` = `obs_ttl_raw_days` (7).
- **G5–G6:** `certain` vietato su `valid_from` nullo/troncato; MAC multi-interfaccia → incerto deterministico; display B-I su `src_mac` evidenza.
- **G7:** B-I raggruppate; priorità `ignoto_con_evidenze_zeek` (P6) distinta da non-riconosciuto attivo (P1).


## 0.10.75 — OBS-BEHAVIOUR O11: evidenze Zeek, Cosa fa, cambio di carattere

- **A:** censimento sonda SPAN viva (ssl/dhcp/ja4d); JA4 non era in SQLite — ingest nuovo.
- **B:** `zeek_behavior_evidence` + correlazione IP↔MAC via `facts/ip_association` (incerta se non current).
- **C:** Dossier «Cosa fa» + blocco INFERENZA IA degradato (nessun motore); baseline in costruzione; card Oggi B-C/B-I.
- Collector: job `zeek-behavior` indipendente da `FLOW_INGEST` / `zeek_provider_enabled`.
- Debito registrato: `DEBT-OGGI-MOBILE-DENSITY` (nessun lavoro densità in O11).


## 0.10.74 — OBS-UX O10: vocabolario visivo, densità mobile, leggibilità

- **W0:** O9-FIX confermata nel CSS servito (timeline min-width:0, md-body overflow-x, table max-content).
- **W1:** `visualVocab.js` + `VisualBadge` — provenance/freschezza/P1–P6/riconoscimento/slot; fix #4 dossier e #8 ReadySlot.
- **W2:** densità @390 — Oggi legenda/coda collassabili; Timeline già-letti; Plant copertura FDB; height full-page misurate.
- **W3/W5:** contrasto AA (--text-2 per muted/meta); Salva sticky (`col-action`); fixture test findings (K4 live vuoto).
- Diff tematici: vocabolario · densità · leggibilità.



## 0.10.73 — OBS-UX O9-FIX: audit 11 rotte, overflow timeline/runbook

- **Y2/Y4:** catture verificate 1280/768/390 sulle 11 rotte mancanti + dossier solo-L2/noto.
- **(a) timeline@390:** card eventi non espandono più il documento (`min-width:0` / contain nowrap).
- **(a) runbook@768/390:** tabelle markdown in scrollport locale (`.md-body { overflow-x: auto }`).
- Diff: `obs-o9fix-rotto.diff.txt`. Y0/Y1 annotazioni; (b)(c)(d)(e) → O10.


## 0.10.72 — OBS-UX O9: harness screenshot, priorità FDB, overflow, avviso churn

- **X1:** diagnosi O8 (PNG tutti 768×); harness CDP `Emulation`+`Page.captureScreenshot`+`o9_png_assert.py` (deviceScaleFactor=1).
- **X2:** S-C=`fdb_l2_only`→P1 (non P3); S-A→P2, S-B→P3, S-D→P4; test invariante superfici.
- **X3:** confirm pre-scrittura nome chassis (`DEBT-CHASSIS-SUBJECT-ID-CHURN`); FA 251 intatto.
- **Layout:** mitiga `DEBT-OGGI-LAYOUT-OVERFLOW` (scroll documento).
- Diff: fase0 · mappa · ui.


## 0.10.71 — OBS-OGGI O8: orfano chassis, conservazione, rumore, priorità difensiva

- **F0:** censimento fatti `subject_type=chassis` (FA 251 orfano); `orphaned_manual_name_facts` in payload chassis; DEBT diagnostica corretta + `DEBT-CHASSIS-SUBJECT-ID-CHURN`. Nessun ri-puntamento.
- **Q1–Q4:** `queueConservationCheck` a tre superfici + `suppressed_noop` + N6; `held_name_is_manual`; chiude `DEBT-OGGI-QUEUE-SURFACES`.
- **R1–R3 / P1–P4:** soppressioni strutturali ispezionabili/ripesabili; priorità per conseguenza difensiva + legenda; segnali S-A…S-D non soppressi.
- Diff: conservazione · rumore · priorità.

## 0.10.70 — OBS-DOSSIER O7: il Dossier risponde (sei domande)

- **D1:** rimossi dump/sezioni grezze dal percorso decisionale; registro di rimozione in `obs-o7.md`.
- **D2–D6:** `GET /api/assets/{id}/dossier` — Cos'è / Dove / Da quando / Cosa fa / È atteso? / Azioni; storia FDB senza eventi O4 defect (nota + DEBT); freschezza O2/O5; INFERENZA IA offline; blue-team solo-L2.
- Diff tematici: backend · vista. Debito annotato: `DEBT-DB-SIZE-OBSERVED` (nessun lavoro DB).

## 0.10.69 — OBS-308 O6: punto cieco GS308EP operativo

- **F0:** V1 delta 135→132 = supersession `left_port` (atteso); V2 copy S-A senza «mai visto».
- **P1–P2:** attestazione strutturale (FDB MAC 308 a monte) + insieme «dietro il 308» (fonte fdb, porta esatta non determinabile).
- **P3–P5:** assegnazione manuale reversibile (`port.assigned_mac`), inferenza separata, punti ciechi in vista, I7 senza telemetria sul 308.
- **P6–P7:** card Oggi «nuovo dietro il 308, porta ignota»; vista `/gs308` da Impianto/Dossier; ricerca «dietro il 308».

## 0.10.68 — OBS-MAPPA O5: bonifica O4 + Impianto operativo

- **F0:** marcatura 396 supersession spurie (`o4_defect_concurrent_presence_move`, no DELETE); baseline ricostruita distinta; UI conteggio scartati + `DEBT-O4-SPURIOUS-MOVES`.
- **M2–M6:** Impianto consuma verità FDB (ruolo+regola, solo-L2, LAA, baseline quality, tre stati vuoti I2, link `link_to_port_id`, ricerca/filtri/azioni, INFERENZA offline).
- Diff tematici: bonifica · hotfix supersession · mappa.

## 0.10.67 — OBS-FDB O4: FDB come sensore difensivo

- **O4.1–O4.2:** assertion `port.fdb_mac` via shadow (source=fdb, auth 60); baseline esplicita al primo populate porta; LAA = `randomized` (DEBT-PRIVACY-MAC-CHURN).
- **O4.3:** `ruolo_porta` ∈ {accesso, uplink, non_determinato} solo evidenza strutturale (link / inclusione insiemi MAC) — mai soglia numerica.
- **O4.4:** card Oggi S-A/S-B/S-C/S-D con azioni F-9; S-D distingue `sorgente_non_disponibile`.
- **O4.5:** blocco INFERENZA offline (OUI/inventario); slot LLM `/ai` predisposto e disattivato.
- Debiti: `DEBT-ENV-NO-INTEGRITY-CHECK`; precisazione data regressione in `obs-o3.md`.

## 0.10.66 — OBS-FDB O2: diagnosi FDB + resa onesta copertura

- **FASE 1:** SNMP v2c timeout su LGS328C/LGS310C (ICMP ok); causa (a)/(b) → ramo B; GS308EP limite strutturale.
- **B1–B4:** stati porta `misurata_fresca`/`misurata_vecchia`/`non_coperta`; pannello Impianto; «non misurato» ≠ assente; move FDB stantio → priorità media.
- Debiti: `DEBT-FDB-POLL-STALE` aggiornato; `DEBT-OGGI-QUEUE-SURFACES` registrato.

## 0.10.65 — OBS-OGGI O1-FIX: provenienza onesta + conservazione coda

- **T1 — `legacy_manual`:** `name_kind=fact` solo se `name_currency.state===fact`; member-held manual → `legacy_manual` (I1). Conflitto I3/`heldManual` invariati.
- **T2 — conservazione coda:** `buildTriageRows` assorbe via `absorbedChassisAssetIds` (card reali); `queueConservationCheck` enumera `missing`/`duplicated`.
- **T3 — test P1–P4** a forma di produzione. **T4 —** `split(/\s+/)`. Debiti `DEBT-CHASSIS-NAME-LEGACY-HELD`, `DEBT-OGGI-LAYOUT-OVERFLOW`.

## 0.10.64 — OBS-OGGI O1: card chassis e adozione nome in Oggi

- **O1.1 — una card per apparato multi-interfaccia in Oggi.** `buildChassisNameCards` + sezione «Apparati multi-interfaccia»: nome dal resolver (`GET /api/chassis` → `name_currency`), altrimenti inferenza etichettata, altrimenti «nome non noto» (I2). Membri (id, ruolo, IP) in elenco. Provenienza sempre visibile (I1).
- **O1.2 — Adotta/Correggi sul soggetto chassis.** Azioni sulla card → `POST /api/chassis/{id}/rename|adopt-name`. UI risolve sempre al chassis: nessun 409 `chassis_subject_required` grezzo. Conflitto manuale vs proposta più debole → card conflitto (I3). F-9: priorità alta solo con azione.
- **O1.3 — API:** `list_chassis_payload` espone `name_currency` via `resolver.current`. Membri multi-NIC assorbiti da `buildTriageRows` (niente card proposta per-NIC).
- **OBS-CURRENCY sospeso** (non chiuso). Gate: currency PASS (1 temp); I6 vuoto. Deploy: `api` + `web`.

## W8-fix — indurimento del presidio + esecuzione reale dei gate (NESSUN deploy, nessun bump)

- **B1 gate indurito (`scripts/w8_currency_gate.py`).** Sentinelle: simbolo ORM `FactAssertion` **+** tabella grezza `fact_assertions` in chiamata SQL (`text/execute`, B1-i) **+** COMBO (fact-token + valore di stato quotato `'current'`, cattura `state='current'`/`filter_by(state="current")`). Allowlist per **(file, snippet, N)** con conteggio: N+1 = violazione, atteso vs osservato in output (B1-ii). Scope allargato a **`api/**` · `scripts/**` · `collector/**`** (B1-iii). `--selftest` (controllo negativo): corpus sintetico in dir temporanea → **3 violazioni attese (file 2,3,4) + 1 accounted → PASS (il gate sa fallire)**.
- **Esito gate reale (repo):** **FAIL — 10 violazioni** tutte in tooling read-only (`scripts/wp_gate.py`, `scripts/wp_diagnose.py`) che legge `FactAssertion` per metriche di regime, rese visibili SOLO ora dall'allargamento scope. Per regola d'ondata **NON allowlistate**: classificate e **fermate per ruling** (vedi `obs-w8fix.md`).
- **B2/B3 G8 eseguito e discriminante (`scripts/w8_g8_equivalence.py`).** Import-smoke (T4a: `subject_of` vive in `resolver.py`, import corretto), leg **os.guess** (resolver vs colonna derivata `Asset.os_guess` — store diverso, non tautologico), leg **endpoint** `GET /api/assets/{id}` opzionale (T4b), `--mutate-probe <id>` (T4d). Eseguito su DB sintetico: normale **DIVERGE=0 (PASS)**; `--mutate-probe` → **DIVERGE=1 esatto sull'id, FAIL**. Prova che G8 sa fallire.
- **B4** AD rimisurato (finestra mobile 24h). **B5** corretta contraddizione: `resolver.history()` è **senza chiamanti**, nessun `?history=true` esiste → `DEBT-HISTORY-PATH-UNWIRED` (spec §12 + `obs-w8.md` corretti). **B6** JSON grezzo `/api/assets/2` e `/109`: «LGS328C» è il canonico del **chassis 23** (tenuto dall'asset **2**); l'asset **109** è membro con nome PROPRIO vuoto (F-5) e AI guess «Switch Centrale» — etichette corrette in `obs-w8.md`.
- **Nessun tocco a `api/app/**` o `web/src/**`** ⇒ nessun deploy, VERSION resta **0.10.63**.

## W8 — enforcement della correntezza (presidio; NESSUN deploy, nessun bump)

- **W8.1 censimento esaustivo → 0 calcoli locali di correntezza da migrare (classe (a) vuota).** Grep su `api/` e `web/src/`: ogni punto che «decide qual è il valore adesso» è già dentro il resolver (`api/app/facts/`), oppure è (b) legittimo con criterio dichiarato — `ip_addresses.is_current` = elezione IP (F-15, non correntezza), colonne di stato derivate di `Asset` (F-7), evidenza grezza/oggetti di dominio (Event/ScanRun/SpeedTest/Finding/Suggestion/Snapshot/ActionRequest), FE che consuma la correntezza fornita dal server. Nessuna classe (a): la migrazione dei consumatori era già stata completata in W5/W6/W7.
- **W8.3 gate permanente istituito:** `scripts/w8_currency_gate.py` — sentinella su ogni riga che nomina `FactAssertion` fuori da `api/app/facts/`; **fallisce** su accessi nuovi; allowlist per (file, snippet) con motivazione. Eseguito: **9 eccezioni giustificate, 0 violazioni (PASS)**. Da eseguire a ogni ondata futura insieme a I6. Documentato in `docs/obs-design-spec-025.md` §12 e `KNOWN_DEBT.md` (PRESIDIO-CURRENCY-GATE).
- **W8.4 API corrente per default:** già così — `GET /api/assets` con `include_historical=false`/`all_proposals=false`, `resolver.history()` percorso storico sanzionato ma non cablato ad alcun endpoint. **0 contratti cambiati.** Verifica runtime (method A): `ips`/`ip_bindings` vuoti → «assente» (≠ zero); binding non-eletti/duplicati restano visibili (F-15). UI stale/superseded invariata da UX3 (nessun cambio, riferimento agli screenshot UX3).
- **W8.5 G8:** `scripts/w8_g8_equivalence.py` (read-only) — equivalenza correntezza nome resolver↔presentazione; 0 migrazioni ⇒ 0 casi (c) per costruzione; probe da confermare a writer fermi sul NAS.
- **Nessun cambio di codice runtime** ⇒ nessun deploy, VERSION resta 0.10.63. Presidio e doc sono artefatti di repo. Pre-condizioni W3 (IP) restano aperte: `DEBT-DOUBLE-CURRENT-IP`, `DEBT-IFACE-IP-CARDINALITY-ROLE`, `DEBT-LASTSEEN-DUAL-SEMANTICS`.

## 0.10.63 — UX3 ondata 2: architettura superfici (D8 + confluenze)

- **UX3.1.4 / D8 — Dashboard decisa con misura → «Panoramica» in navigazione.** Misura prod (2026-07-28): la Dashboard mostra ciò che nessun'altra vista mostra — stato calibrazione osservatorio (giorno N/14), **salute Internet** (capacità/traffico FRITZ!Box, speedtest NAS, prossimo test), copertura discovery, salute sensori, KPI device+monitor. **Utile e distinta** (opzione a): entra in nav come «Panoramica» (gruppo RADAR). Coerenza con F-9: `/` non è più la Dashboard ma **reindirizza a `/oggi`** (il cardine è la landing); la Dashboard vive su `/dashboard`.
- **UX3.2 — architettura delle superfici (decisioni con dati reali).** `suggestions` → già **CONFLUITA** in Oggi (redirect `/suggestions`→`/oggi`; le 2 proposte pending compaiono in Oggi). `findings` → 0 elementi, 0 drift, in shadow: **tolta dalla nav primaria** (coda parallela vuota, F-9), ma **ancora raggiungibile** dalla Dashboard (ReadySlot + card «Findings shadow») e per URL — nessuna funzione irraggiungibile (UX3.2.4). Debito `DEBT-FINDINGS-OGGI-CONFLUENCE` registrato: confluenza autoritativa in Oggi rinviata a calibrazione/scoring (M4–M5). Le viste con domanda unica **TENGONO**: Oggi (cardine), Dossier (device), Inventario (elenco/ricerca), Impianto (porte/modifica), Topologia (dove), Monitor (salute), Timeline (cronologia), Azioni (scansioni/errori discovery), Panoramica (D8).
- **Nessun dato grezzo rimosso perché non trovato di gravità operativa (UX3.3):** Dossier è strutturato e onesto (identità osservata con ignoti dichiarati, inferenza AI marcata con confidenza+evidenze, GS308EP con `.1.8` corrente/`.3.20` storico) — non un dump. Switch = tre superfici coerenti (Impianto=modifica, Topologia=dove, Monitor=salute), nessuna vista switch legacy autonoma. ReadySlot Dashboard dichiarano l'attesa (I2), non inventano: annotati in `DEBT-DASHBOARD-READY-SLOTS`.
- **Test:** nessun nodo backend toccato; frontend `oggiTriage`, `oggiProblems`, `observatoryUx`, `portPresentation`, `topologyLayout` invariati verdi. F-1..F-14 rispettati; policy MAC↔IP consultiva (F-12); I5/F-8 immutati; favicon A (F-6).

## 0.10.62 — UX3 ondata 1: mobile + Mappa usabili (D3, D4, D7)

- **UX3.1.2 / D3 — navigazione mobile a comparsa:** sotto 800px la sidebar diventava una barra alta ~280px perché gli 11 link andavano a capo su più righe, spingendo il contenuto sotto la piega. Ora (`App.vue` + `matrix.css`) la barra mobile è compatta (brand + hamburger «☰ Menu» + utente/Esci); il menu si apre a comparsa a piena larghezza in colonna, con tocco comodo, e si chiude a ogni cambio rotta. Desktop invariato. Nessun tocco ad auth/ruoli (K10).
- **UX3.1.3 / D4 — Impianto, troncamenti alla radice:** in `Plant.vue` più righe informative usavano `white-space:nowrap`+`overflow:hidden`+ellissi su testo che deve andare a capo (stessa **classe** di causa di D2, qui su testo semplice, non `DenseRow`). Punti condivisi enumerati e corretti: `.fdb-status` (banner copertura FDB — la **data dell'ultima misura non va mai troncata**, F-13: ora va a capo a ogni larghezza), `.switch-role`, `.port-foot .patch` (vanno a capo su mobile). 
- **UX3.1.1 / D7 — Topologia usabile su mobile:** il grafo a coordinate assolute in un contenitore scroll è inutilizzabile sotto 800px (finestrella su una mappa grande). Sotto 800px il grafo è sostituito da una **lista gerarchica per livello** (Radice → Livello 1/2/3) che risponde alla stessa domanda («dove sta un apparato, a cosa è attaccato»): riusa i nodi già posizionati da `layoutTopology` e mostra per ciascun nodo nome canonico, IP/tipo e «↳ collegato a <padre>»; gli endpoint restano toccabili per isolarne il percorso. I controlli zoom (inerti senza grafo) sono nascosti su mobile. Nessun dato inventato.
- **Test:** `topologyLayout`, `portPresentation`, `observatoryUx`, `oggiTriage`, `oggiProblems` (invariati, verdi). Favicon A immutata (F-6), I5/F-8 immutati, nessuna logica identità/currency nel frontend, policy MAC↔IP consultiva (F-12), FDB solo presentazione (F-13).

## 0.10.61 — UX2 ondata 1b: Oggi non tronca su tablet (radice DenseRow)

- **UX2.5 — Oggi, troncamento su tablet risolto alla radice:** su tablet (≈820px) i valori delle card («Causa ed evidenza», «Esito», …) erano **tagliati a metà parola**. Causa: lo slot primario di `DenseRow` porta lo stile generico `white-space:nowrap` + `overflow:hidden`, adatto a righe singole ma non al contenuto **multilinea** delle card di Oggi. Fix in `Oggi.vue`: dentro `.oggi` lo slot primario va a capo e resta visibile a **tutti** i breakpoint (non solo ≤640px). Nessun impatto su desktop (già largo) né sul resto delle viste che usano DenseRow.

## 0.10.60 — UX2 ondata 1: onestà dei dati porta/telemetria + Oggi mobile

- **UX2.2.4 / F-13 — copertura FDB dichiarata in UI (`DEBT-FDB-POLL-STALE`):** la copertura FDB è ferma (RO 2026-07-27: 46 porte, 38 con `last_fdb_at`, 0 fresche nelle 24h; più recente 2026-07-25 14:52). Nuovo helper puro `fdbCoverageStatus()` in `web/src/observatoryUx.js` (con test) calcola la freschezza dalla `last_fdb_at` di porta, **mai** dall'ora del poll fallito. Impianto (`Plant.vue`): banner «copertura FDB non aggiornata: ultima mappatura … (circa N h fa)» e badge per-switch corretto — prima `switchFreshness` spacciava `fdb_poll.at` (tentativo fallito, `ok:false`) come «dati al … (ok)». Solo presentazione: nessuna diagnosi/riavvio del polling (F-13).
- **UX2.5 / I2 / I7 — Monitor: assente ≠ zero:** in «Switch · salute porte» (`Monitoring.vue`) traffico ed errori erano resi `0 b/s` / `0` per switch senza SNMP riuscito (GS308EP non interrogabile, LGS in timeout). Ora sono `—` (non disponibile) quando `snmp_poll.ok≠true`, e l'ultimo poll è marcato «non riuscito». Nessuna telemetria inventata.
- **UX2.1 / UX2.5 — Oggi (il cardine) responsive su mobile:** le card di Oggi troncavano nome/MAC e non impilavano label/valore su schermi stretti (le azioni comprimevano il contenuto). Fix CSS scoped in `Oggi.vue`: sotto 640px la riga densa impila (azioni sotto, allineate a sinistra), i campi vanno a capo, nome/MAC non si troncano.
- **Test:** `observatoryUx` (nuovo caso `fdbCoverageStatus` F-13), `oggiTriage`, `oggiProblems`, `portPresentation`, `topologyLayout` — 40 verdi. Favicon A immutata (F-6), I5/F-8 immutati, nessuna logica di identità/currency nel frontend (F-13 = presentazione di timestamp misurati), policy MAC↔IP resta consultiva (F-12).

## 0.10.59 — W7-CLOSE: eccezione L2 da attributi misurati, ignoto≠falso, policy consultiva

- **W7C.2 (K9/F-5) — eccezione L2-only NON dipende più da `Asset.name`:** `_l2_only_exception_class` (`inventory.py`) derivava la classe powerline/510E da `" ".join(asset.name, asset.category, asset.vendor)`. Dopo W4c.1 i membri di chassis hanno `Asset.name` **vuoto per progetto** (F-5): un powerline membro di chassis non sarebbe stato riconosciuto. Ora la classe è derivata da attributi **MISURATI** — `category`, `vendor`, l'**OUI vendor** di ogni interfaccia — e, quando serve un nome, dal **nome CANONICO risolto** (`presentation_name_for_asset`, chassis-scoped), mai dal nome grezzo del membro. Se nessun attributo misurato riconosce la classe, la classe è **ASSENTE (`None`, K3)**, non un match mancato spacciato per «non è powerline».
- **W7C.3 (I2/K3) — input costanti del classifier risolti:** in `_mac_ip_policy_present` gli input `chassis_mgmt_ip` e `superseded_by_newer_binding` erano passati fissi (`None`, `False`). Il secondo **asseriva** un fatto non misurato («nessun binding più recente ha soppiantato»). Ora `superseded_by_newer_binding` è **tri-stato** (`bool | None`, default `None`=IGNOTO): solo un `True` **misurato** produce il verdetto `superseded`; `None` (ignoto) non viene mai coerciuto in un'asserzione. Il wire passa `None` (ignoto), non più `False`. `chassis_mgmt_ip` resta `None`=IGNOTO (non serve/non misurato qui, mai inventato).
- **W7C.5 — policy PIENA CONSULTIVA (mai autoritativa):** nuovo `inventory.mac_ip_policy_consultation` (read-only) calcola il verdetto della policy completa (regole #1..#5) per ogni asset e lo espone come **divergenza diagnostica** accanto allo stato reale, con l'evidenza che tiene presente il device. Endpoint admin `GET /api/admin/mac-ip-policy-consultation` (sola lettura, ruolo operator). **Non scrive nulla e non guida `operational_state`/`trust_level`/`reliable`** (F-7): le regole #3/#5 restano **NON autoritative** (attivazione autoritativa rinviata e condizionata alla correzione delle regole che dissentono dalla realtà osservabile — `DEBT-MAC-IP-POLICY-WIRE` aperto). Mai esposto come stato del device in UI.
- **Test:** `test_mac_ip_policy` (11, incl. tri-stato supersession) esercitato; nuovi nodi fixture/app W7C.2 verificati per import/sintassi (K4, non esercitati a runtime per contesa risorse NAS). F-7 intatto, I5/F-8 immutati, favicon A immutata (F-6).

## 0.10.58 — W7 (deploy 1/2): T-a uplink→portal + wire mac_ip_policy additivo

- **W7.3 T-a (DEBT-FDB-UPLINK-PORTAL):** `apply_fdb_observation` (`topology.py`) **ricalcolava** `interface.interface_role` per-porta prima della guardia portale, facendo un **downgrade `uplink→endpoint`** su un singolo hit FDB → poi attribuiva `portal_last_seen` a una porta uplink (presenza al posto sbagliato). Fix: un hit FDB per-porta NON declassa più un'interfaccia strutturale (`uplink`/`infra`); i downgrade restano di competenza del reclassify globale (`role_for_interface_global`). Test T-a verde, non indebolito. Il fix NON azzera retroattivamente `portal_last_seen`: nessun effetto su presence/structural al boot (misurato).
- **W7.2 wire `mac_ip_policy` (deploy 1/2 — additivo, F-7 intatto):** il classifier `classify_mac_ip_presence` è ora collegato a `reconcile_asset_presence` come **solo segnale di PRESENZA** (`reliable`), limitato alle lacune che la logica esistente non copre: membro di chassis mantenuto presente dall'IP corrente di chassis (`present_l2_unaddressed`) ed eccezione powerline/510E (`l2_only_allowed`). Il wire **non forza mai `stale`/`superseded`** e non è un secondo autore di `operational_state`/`trust_level` (classify_asset resta l'unico deriver). `present_l2_unaddressed` è **dichiarato** dalla freschezza FDB misurata, mai dedotto dal solo IP di chassis. **Misura pre-deploy (read-only prod):** 0 hit `present_l2_unaddressed`/`l2_only_allowed` correnti ⇒ **0 cambi di `operational_state`** (wire inerte oggi, esercitato dai test unitari `test_w7_consumers` — K4).
- **W7.2.3 split dichiarato:** la riclassificazione AMPIA della policy (regole #3/#5: `stale`/`superseded` che toglierebbero presenza a device correnti) ha blast-radius **alto (52/151 asset**, inclusi FritzBox router, powerline, Sky box) e tocca infrastruttura oggi `active` → **rinviata al deploy 2/2** (decisione di dominio su quali device attivi declassare: Michele). Non fatta qui per non introdurre regressioni (c) né violare «stale/superseded fuori dallo stato corrente».
- **Test:** `test_w7_consumers` (5, wire additivo), `test_m2_discovery` (T-a) verdi; nodi presence/trust/scans nominati verdi (94). Gate I6 vuoto.

## 0.10.57 — W6-REVIEW: rank ipp/snmp riportato al minimo non alterante di I5

- **W6R.1 (DEBT-IPP-PRECEDENCE, correzione soglia non misurata):** W6 aveva collocato `ipp=88`/`snmp=87` **sopra** `dhcp=85`, alterando l'ordinamento dell'invariante di PRODOTTO I5 (`manual > ai > dhcp > fritz > oui`) per far passare due test — stessa classe di difetto della soglia inventata rimossa in W1.5-bis. L'UNICO vincolo MISURATO è `ipp > fritz` (test T-c, fixture fritz(0.9) vs ipp(0.96)); nessun test impone `ipp > dhcp` né alcun ordine per `snmp` (T-d e `test_printer_provider` asseriscono solo creazione/valore della proposta, mai `best_guess`). Rank riportato al minimo non alterante: **`ipp=snmp=81`** (tier «identità auto-dichiarata via management», sopra `fritz=80`, **sotto `dhcp=85`** → I5 intatto; tie ipp/snmp risolto da confidence). La posizione del tier vs `dhcp` è una decisione di dominio lasciata a Michele (STOP-5, K8), tenuta sotto dhcp.
- **W6R.1.3 effetto misurato (read-only prod 0.10.56):** **0 proposte pending `ipp`/`snmp`**, **0 asset vinti** da `ipp`/`snmp`, **0 flip** di `best_guess` abbassando i rank → il fix è **comportamentalmente inerte** in produzione. Le 3 differenze `i5_reorder` (id 109/120/134) sono `ai` (rank 90, non toccato) e **restano**.
- **W6R.2.1 `adopted_names_changed = 0` (misurato):** i 30 nomi adottati (`manual_overrides` include `name`) sono **identici** tra prod 0.10.56, backup pre-deploy W6 e nightly pre-W6 — nessun nome adottato ha cambiato valore.
- **W6R.2.2 asset senza best guess:** 28 asset con `best_guess` vuoto; di questi 9 senza nome canonico (`presented=None`) → la UI dichiara l'assenza («Device senza nome» / MAC, I2), mai un placeholder spacciato per nome. Gli altri mostrano il nome dell'apparato (asset.name o canon chassis).
- **Test:** nodi nominati Python verdi (T-c/T-d verdi con `ipp=snmp=81`); gate I6 `rg 'scoreSpecificity|specificity' api/` vuoto. Nessun test indebolito. Artefatti W6 e W5-bis ripubblicati con URL raw (curl 200).

## 0.10.56 — W6: fingerprinting, inferenze AI, generazione proposte alla correntezza

- **W6.1 correntezza dei consumatori (`suggest.best_guess`, `ai_naming._hostnames`, `fingerprint_facts` backfill hostname):** `best_guess` non filtrava lo stato delle `NameProposal` e sorfava proposte **rejected/superseded/archived** — in prod **51 asset** ricevevano come «best guess» un nome che l'utente aveva rifiutato o che era stato soppiantato. Ora i tre percorsi consumano SOLO proposte `pending`; le altre restano a DB (storia leggibile, `escludere ≠ cancellare`). Fatti `fact_assertions` in stato `superseded/historical` non erano consumati (i percorsi leggono `resolver.current` o `observations_raw`, mai gli stati non correnti) → per quel lato il fix è preventivo (misurato: 0).
- **W6.2 DEBT-IPP-PRECEDENCE (T-c/T-d), gerarchia unica I5:** `best_guess` decideva la precedenza con un **secondo prospetto di pesi** (`SOURCE_WEIGHT`) non coincidente con I5. Rimosso: ora ordina per `authority_for` (registro I5) primario, `confidence` a parità. `ipp`/`snmp` hanno un rank **dichiarato esplicito** in `AUTHORITY_RANK` (ipp=88, snmp=87: identità auto-dichiarata dal device via management, sotto l'AI curata e sopra dhcp/fritz). Root-cause di T-c/T-d: `create_name_proposal` faceva `db.add` senza sincronizzare la relazione `asset.name_proposals` → le proposte create non erano visibili in-sessione; ora `append` alla relazione. T-c → `('Stampante Studio','ipp')`, T-d → proposta `snmp` presente. Test non indeboliti.
- **W6.3 soppressione alla generazione (già conforme):** `should_suppress_proposal` sopprime per **provenienza + soggetto** (chassis-manual blocca sorgenti più deboli; dedup per valore), mai per specificità del nome (I6, K6). Gate `rg 'scoreSpecificity|specificity' api/` **vuoto**.
- **W6.2/6.4 R-D:** un'inferenza AI resta marcata (`source=ai`, `status=pending`) e NON sovrascrive un valore `manual`; `ai` non entra come sorgente hostname fattuale nel payload LLM.
- **W6.4 gate G6 (writer fermi, `now` ricalcolato):** `best_guess` PRE vs DEPLOYED, per id. Baseline pre-deploy `diff=0` (inline-old fedele). Post-deploy: **54 differenze, tutte (a)** — 51 `status_exclusion` (correntezza) + 3 `i5_reorder` (id 109/120/134: `ai` pending ora batte `oui`/`fritz` per I5). Zero (b), zero (c). Fingerprint/AI generation NON esercitati in prod (K4): filtro preventivo + AI = API a pagamento; copertura nei test unitari.
- **W6.6 test (nodi nominati):** Python nominati verdi (incl. `test_w6_consumers` W6.6.1-6.4, T-c/T-d ora verdi) + 39 JS. Gate I6 vuoto.

## 0.10.55 — W5-bis: chiusure prima di W6

- **W5b.1 mapping livello→stato TOTALE (`trust.py` `_apply_level_meta`):** per ogni livello attivo (`known`/`confirmed_present`) `operational_state="active"` viene scritto SEMPRE. Prima, se `inventory_hidden_auto` era falso, `operational_state` restava invariato e `_build_trust_plan` (che confronta `operational_state`) marcava `structural` in perpetuo — stessa forma del difetto 109 dietro una condizione. L'auto-hide viene revocato; un nascondimento MANUALE resta rispettato ed esplicitamente escluso (non è `structural`: il piano confronta `operational_state`, non i flag di hide). Mapping reso totale, gate NON reso cieco (F-7: unico writer del campo).
- **W5b.2 gate di regime = CONVERGENZA (`scripts/wp_gate.py` riscritto):** prima costruiva due piani `dry_run` sullo stesso stato con lo stesso `now` (verificava il determinismo, non la convergenza). Ora: piano → **apply** (in-sessione, mai committato, snapshot pre-op) → ricostruzione con `now` **ricalcolato** → `structural == []`. Precisazione aggiunta a `obs-wp.md` (non riscritta la storia).
- **W5b.3 lista classe-(b) chiusa voce per voce:** copia ingest `wifi_associations.resolve_ap_asset` era rimasta su `is_current` dopo la migrazione W5 di `topology._resolve_ap_asset`; migrata al resolver contestuale `resolve_asset_by_ip_at(ap_ip, observed_at)`, tie → None → fall-through sul nome (I2). Chiamanti di `presentation_name_for_asset` verificati: nessuno annulla il None con `or ""`/placeholder come surrogato di nome canonico (i fallback sono display-di-ultima-istanza, dichiarati). G5 di W5 non ha esercitato il path `ap_ip` (0/62): copertura nei test unitari (dichiarato, non «verificato»).
- **W5b.5 test (nodi nominati):** 176 nodi Python verdi + 39 JS verdi + nuovi W5b.1.5 (mapping totale, hide manuale preservato) e W5b.3 (ingest AP contestuale + tie). T-c/T-d (`test_printer_enrichment`, DEBT-IPP-PRECEDENCE) restano ROSSI: contratti W6, non addomesticati. Gate I6 `rg 'scoreSpecificity|specificity' api/` vuoto.

## 0.10.54 — W5: consumatori dello stato corrente sul resolver

- **W5.0/1 perimetro:** migrazione di LETTURA (nessuna scrittura su colonne Asset). Il nome canonico nelle viste migrate passa già dal resolver (`presentation_name_for_asset` → `current("chassis", …, "asset.name")`, fallback dichiarato I2 quando assente).
- **W5 `_resolve_ap_asset` (DEBT-TOPO-IP-CONTEXTUAL):** il fallback per-IP non usa più `IpAddress.is_current` ma `resolve_asset_by_ip_at(ap_ip, observed_at)`: risolve l'AP che DETENEVA l'IP al momento dell'associazione, non chi lo detiene ora. Tie → None → fall-through all'euristica sul nome (I2, nessun proprietario indovinato).
- **W5.1.3 (IP multi-valore):** `asset.iface_ip` ha `cardinality=single` (solo IP eletto); il resolver NON è fonte esclusiva per gli IP finché il ruolo non entra nella `excl_key` (pre-condizione W3, DEBT-IFACE-IP-CARDINALITY-ROLE). La UI continua a mostrare tutti gli IP reali (multi-IP non collassati).
- **W5.2 gate G5 (writer fermi):** risoluzione AP `is_current` vs contestuale su 62 associazioni Wi-Fi → **0 differenze** (0 associazioni sul path `ap_ip`; tutte risolvono per `ap_asset_id`/`ap_mac`). Nessuna regressione: la migrazione è un fix latente, equivalenza-preservante sui dati correnti.
- **W5.4 test:** `_resolve_ap_asset` contestuale + tie→fall-through (W5.4.6); chassis un nome canonico dal resolver (W5.4.5); fatto assente → None (W5.4.1); resolver stale/superseded esclusi dal corrente, storia leggibile (facts_resolver/shadow_w2).

## 0.10.53 — W-P: presenza con un solo proprietario, stato derivato

- **W-P.1 (misurato):** ipotesi A — Fritz VEDE l'asset 109 (`discovery.fritz.active=True` fresh, MAC `D8:EC:5E:CC:1C:01`). Il lift era legittimo; il difetto era che `classify_asset` non consumava l'evidenza fritz → riderivava `fritz_historical` ≠ stato memorizzato → `structural=1` permanente. Divergenti reali: solo 109.
- **W-P.2:** l'evidenza si scrive, lo stato si deriva. `classify_asset` ora legge l'evidenza fritz-active fresca (`meta.discovery.fritz`, finestra staleness) e deriva `known` (autorità fritz I5 0.90, MAI `confirmed_present`). `lift_fritz_quarantine_on_active` non scrive più lo stato: registra l'evidenza e ri-esegue la derivazione unica. Mapping `livello→stato` estratto in `_apply_level_meta` (un solo writer, condiviso con `_apply_trust_plan`).
- **W-P.3:** round-trip a writer fermi (due piani consecutivi `structural==[]`); fixture 109-like con/senza evidenza fritz; D.0.b (fresh→known, mai confirmed_present) + reversibilità; W-C invariata (inventory non solleva né smasha la quarantena). Gate I6 vuoto.
- **fritz_historical NON assorbente:** un'evidenza fritz-active fresca solleva la quarantena via derivazione; scaduta l'evidenza il piano riporta a `fritz_historical`/`stale_unlocated` senza oscillare.
- **DEBT-PRESENCE-SOURCE-OUTAGE:** migliorato (fritz vivo → `known`, non stale), ma NON chiuso: manca ancora la distinzione «sorgente non disponibile» vs «dispositivo assente» (richiede segnale di copertura sorgente). Resta APERTO.

## 0.10.52 — W4d: census Asset.name, una scrittura rename, UX truth

- **W4d.1:** censimento lettori `Asset.name`; `presentation_name_for_asset` su API display/porte/topologia/scan; lista (b) → input W5.
- **W4d.2:** `adopt_name_on_chassis` / `mark_lgs310c_manual` → sola `apply_observation` (niente doppio shadow).
- **W4d.3:** `obs-ux2.md` matrice «non verificato a runtime» + checklist Michele; LGS via API reali.
- **W4d.4:** favicon opzione B (anello+hub, stessi token) pubblicata; attuale non sostituita.
- **F0:** DEBT-FRITZ-TR064-CREDENTIALS chiuso (recreate collector).

## 0.10.51 — F2: revisione UI/UX portale (presenza, Mappa, favicon)

- **F2.0:** gruppo nav MAPPA = Inventario/Impianto/Topologia/…; mappa porte fisica = `/plant`.
- **F2.1 Plant:** deep-link `?asset=`/`?asset_id=`; pallini SNMP nascosti se non supportati (GS308); limiti I2/I7 in Branch308.
- **F2.2–3:** banner Fritz muto (Oggi/Dashboard/Inventario); `stale_unlocated` → «copertura sorgente non disponibile»; conflitti R-H nel flusso Oggi; dossier/inventario un nome chassis.
- **F2.5:** favicon su token `--bg-0`/`--accent`/`--ok`; SVG+ICO+apple-touch; link versionati.
- **Non toccato:** trust layer (DEBT-PRESENCE-SOURCE-OUTAGE); credenziali Fritz; W5 consumatori.

## 0.10.50 — W4c: rename chassis un-canonico, bonifica una-tantum, boot pulito

- **W4c.1:** `adopt_name_on_chassis` scrive solo `fact_assertions` (subject=chassis); i membri non vengono rinominati né marcati manual; triage sibling su `chassis_role===interface`.
- **W4c.2:** bonifica `provenance_unreliable` con cutoff `2026-07-27T11:00:00Z`, fuori dal boot; script `scripts/unmark_post_cutoff_provenance.py`.
- **W4c.3:** `mark_lgs310c_manual` rimosso dal bootstrap (helper one-shot).
- **W4c.5:** aperto DEBT-PRESENCE-SOURCE-OUTAGE (Fritz muto ≠ device assente).

## 0.10.49 — W4b: provenienza senza traduzione, anti-ballooning, rename chassis

- **W4b.0.a:** shadow writers non traducono più le sorgenti; unknown → rifiuto + `unknown_source`; bonifica `provenance_unreliable` su nmap non ricostruibile.
- **W4b.0.b:** divergenze ripetute (stesso excl_key/value/source) aggiornano `occurrences` invece di nuove righe.
- **W4b.1:** LGS310C (asset 3 / chassis 24) marcato manual (provenienza); LGS328C resta `unknown_nonempty`; UI card dichiara l’apparato di appartenenza.
- **W4b.2:** rename/adopt a soggetto chassis; member → 409 con chassis; conflict-review in Oggi; `asset.name` collegato agli shadow writers.
- **W4b.3:** aperti DEBT-RH-BEFORE-REFRESH; `_table_bytes` non usa più la size del file DB; DEBT-FRITZ resta aperto (credenziali TR-064 assenti).

## 0.10.48 — W4a: soggetto chassis e soppressione proposte a monte

- **W4a:** NameProposal generate/soppresse per soggetto chassis (manual blocca autorità inferiore; dedup `(chassis, valore)`); risolvibilità calcolata; sibling come interfacce.
- **W4a.0:** `facts/shadow.py` tracciato; DEBT-IFACE-IP-CARDINALITY-ROLE; DEBT-FRITZ-TR064-CREDENTIALS (STOP-5); `subject_ref_interface` rifiuta multi-NIC senza primary.
- **Non toccato:** adopt/rename 409 (W4b); shadow `asset.name`.
- Report: [`docs/obs-w4a.md`](docs/obs-w4a.md).

## 0.10.47 — W2: shadow writers fact_assertion

- **W2:** scritture parallele `asset.iface_ip` (soggetto=interfaccia, excl_key=`asset.iface_ip:{iface_id}`); nessun consumatore legge ancora.
- **S1:** barriera + SAVEPOINT; kill switch `FACT_SHADOW_WRITERS_ENABLED`; circuit breaker (20k righe / 2k/giorno / 50 MiB).
- **Non collegato:** `asset.name` (chassis → W4a/W4b). Observability: `GET /api/admin/facts/shadow-stats`.
- Report: [`docs/obs-w2.md`](docs/obs-w2.md).

## 0.10.46 — W-D-fix: discriminante multi-IP sul dedup

- **X.2:** `entity_key` resta MAC-scoped; `compute_dedup_key` ripristina discriminante IP (`fact_discriminant_for`) — DEBT-TOPO-IP-CONTEXTUAL ripristinato.
- **X.4:** lift Fritz → `known` (non `confirmed_present`); decisione in `on_fritz_active_evidence` (trust).
- **Debiti:** DEBT-LASTSEEN-DUAL-SEMANTICS. W2 → **0.10.47**.
- Report: [`docs/obs-wd-fix.md`](docs/obs-wd-fix.md).

## 0.10.45 — W-D: sblocco gate W2 (T-b, T-e, T-f)

- **T-b:** `entity_key_for` MAC-scoped quando MAC noto; IP-only provisional (`identity_provisional`) + DEBT-PROVISIONAL-IDENTITY-MERGE.
- **T-e/T-f:** demotion IP chiude `last_seen=now` → `resolve_asset_by_ip_at` trova il detentore storico.
- **D.0.b:** `lift_fritz_quarantine_on_active` (trust) — quarantena non assorbente; inventory resta bloccata.
- **Debiti:** DEBT-DOUBLE-CURRENT-IP; Cassiopea ri-caratterizzata chassis (W4a/W4b); alembic unificato in DEBT-ALEMBIC-BASELINE-LEGACY-TABLE. W2 writers → **0.10.46** (poi **0.10.47** in W-D-fix).
- Report: [`docs/obs-wd.md`](docs/obs-wd.md).

## 0.10.44 — F1-bis: DEBT-RECONCILE-CHURN-1 + riqualifica gate F1

- **W-C:** `inventory_may_set_operational_state` non solleva/smasha `trust_quarantine` (`fritz_historical`) — chiude DEBT-RECONCILE-CHURN-1 (classe, non asset 116). Test zero-iface obbligatorio.
- **W-B.3:** script una-tantum `scripts/normalize_empty_manual_names.py` (asset 98/150 name manual vuoto → assenza; no bump).
- **Debiti:** DEBT-IP-CURRENT-SCOPE-PER-ASSET (Cassiopea asset 6). W2 slitta a **0.10.45** (poi rinumerato → **0.10.46** in W-D).
- Report: [`docs/obs-f1bis.md`](docs/obs-f1bis.md).

## 0.10.43 — OBS-IDENTITY W1.5-bis gate closure

- **W1.5-bis:** rimossa soglia E3 inventata (`mac_count_threshold` solo se misurata); test limiti E5-physical (D.2); tool RO `obs_identity_linker_dryrun.py`. Nessun writer identity acceso. W2 shadow writers slitta a **0.10.44** (poi rinumerato → **0.10.45** in F1-bis). Debiti: DEBT-RECONCILE-CHURN-1 (asset 116), DEBT-E3-AVAILABLE-FALSE.
- **MAC↔IP (fixture):** classifier puro `mac_ip_policy.py` + 9 test contratto; **non** wired a reconcile/trust (DEBT-MAC-IP-POLICY-WIRE → W7).

## 0.10.42 — W1.5 identity-evidence (deployata)

- **OBS-CURRENCY W1.5 OBS-IDENTITY-EVIDENCE (Fase 3 post-review):** scala evidenze **E0..E5** (`level = f(fact_type, acquisition_method, source, subtype, quals)` — mai `fact_type` da solo) e scala decisioni **D0..D3** (D4 assente per design). Package `api/app/identity_evidence/{classes,store,linker,decisions,presence,mac_guards,circularity}.py`. Modelli aggiornati (`member_id`, `provenance_generation`, `collector_run_id`, stato `absent_measured`/`absent_unmeasured`, FSM `link_state` ortogonale a `evidence.state`, `relation` default `unresolved`, `audit` JSON per confermare/rifiutare/ritrarre). Guardrail: **U/L bit MAC** (LAA → downgrade a E1), **zero adiacenza blocchi MAC** (test statico sul modulo), **K7 circolarità** (chassis_id come propria evidenza rifiutato; provenance che cita il link stesso rifiutata). Linker: solo `link_state=proposed`, mai `chassis_id`/`Asset.name`, no transitività, no fusione. Merge = LINK (reversibile via `retract_link`). Test T1..T21 + schema parity models ↔ `create_all` verdi. W2 shadow writers slittato a **0.10.44** (W1.5-bis).

## 0.10.41 — OBS-CURRENCY W1 (deployata)

- **OBS-CURRENCY W1:** fondamenta `fact_assertion` — registro dichiarativo (`api/app/facts/registry.py`), resolver unico R-A..R-H (`api/app/facts/resolver.py`), modello + indice unico parziale `(subject_type, subject_id, excl_key) WHERE state='current'`, migrazione Alembic di coerenza. Nessun writer ingest, nessun consumatore modificato, nessuna scrittura su colonne Asset. Regime assert: T_total=8.879 · needs_apply=false · T_backup=0 · NP=412.

## 0.10.40 — 2026-07-25

- **OBS-UX fase G (visiva):** allineamento superfici `matrix.css` ai token blu-ardesia (`--bg-*`, `--border`, `--data-idle`); fix responsive invalido `calc(100% - auto)` → `grid-template-rows: auto 1fr` su sidebar mobile.

## 0.10.39 — 2026-07-25

- **OBS-UX ondata F:** `ViewStateBanner` (loading / empty / error / parziale / stale) su Oggi, Inventario, Impianto, Topologia, Monitor, Dossier, Findings; `UX_COPY` per gergo interno; focus-visible su ricerche Inventario/Dossier; messaggio massa «Archivia rumore» con saltate/non trovate.

## 0.10.38 — 2026-07-25

- **OBS-UX ondata E:** etichetta «Inferenza AI» su proposte e Assistente (`AiInferenceLabel`: evidenze, confidenza, «può sbagliare»); rank sorgente `ai` sotto `manual` (I5); AI non entra in «Adotta» automatico; prodotto utilizzabile con `AI_ENABLED=false`; **correzione copy IP .3.20 da confermare** (scheda 308 / I3 — non inventariale, non SPAN).

## 0.10.37 — 2026-07-25

- **OBS-UX ondata D:** Dossier «Chi sei» — sezione Sintesi identità (cosa sappiamo / fonti / freschezza / incerto / manca) al posto del toggle «Mostra dettagli tecnici» e dump JSON; `name_proposals` e `fingerprint_facts` leggeri sempre in GET identity (senza evidence grezzo).

## 0.10.36 — 2026-07-25

- **OBS-UX ondata C:** componente riusabile `Branch308Card` (fatti, gap I7, inferenza SPAN dichiarata) montato in Topologia (nodo/percorso GS308EP), Impianto e Dossier asset 4; helper `branch308*` in `observatoryUx.js`.

## 0.10.35 — 2026-07-25

- **OBS-UX ondata B:** chiariti i tre ruoli switch (Impianto=edit, Topologia=collocazione, Monitor=salute) con PageHeader e banner; sezione SNMP Monitor cita Impianto/Topologia per GS308; divergenza IP asset 4 dichiarata; stati errore su load Inventory/Plant/Topology; decisioni legacy in `docs/obs-ux-deps-b.md`.

## 0.10.34 — 2026-07-25

- **OBS-UX ondata A:** Oggi come cardine unico — card problema (6 campi), porte FDB in coda, anteprima Archivia rumore (N scomposto), link Impianto/Topologia/Dossier, `/suggestions` → redirect `/oggi`. Specifica: `docs/obs-ux-casidiuso.md`.

## 0.10.33 — 2026-07-25

- **OBS-PORTALE ondata 3:** `all_proposals=true` su GET /api/assets (Oggi); guardia anti-ricreazione NameProposal rejected; adopt-name 409 su chassis multi-NIC; reject move FDB verso porte uplink/path (310c:8 / 328c:21).

## 0.10.32 — 2026-07-25

- **OBS-PORTALE ondata 2:** qualità proposte a monte — filtro banner SSDP (`ssdp_name_candidate`); OUI NameProposal ≥0.7; OS equivalenza solo troncamento nmap; Sky omonimi dichiarati (`name_ambiguity`) / OUI bare qualificati con IP. Digit-run: 0 hit sui nomi attuali → regex invariata.

## 0.10.31 — 2026-07-25

- **OBS-PORTALE ondata 1:** dichiara l'assenza — barra confidenza manuale → badge «manuale»; sidebar «versione non disponibile» senza health; DirectionBar testo esplicito; chassis partial warning (no mono-NIC silenzioso).

## 0.10.30 — 2026-07-25

- **OBS-COERENZA:** rotazione backup unificata (`backup_rotate_core` + `deploy.sh` post-rsync); protetti esclusi per nome (`pre-4b-drop-20260725-161330.db`, `observatory-pre4b.bak`).
- Calibrazione K3: day-clock solo da `settings.calibration_started_at`; assente/invalido → `available=false`, `day=null` (mai SensorRun).
- Alembic `l2c3d4e5f6a7`: `DROP TABLE IF EXISTS observations` (idempotente).
- Detector stub `unexpected_dhcp_dns` / `llmnr_nbns_mdns` rimossi dal registro.
- Retention-run: telemetria `store` freelist/bytes + log riga.
- Debiti: chiude ROTATION-SPLIT / ALEMBIC-BASELINE-LEGACY / CALIB-EPOCH (K3); apre `DEBT-BACKUP-ALL-OR-NOTHING`; accetta `DEBT-AUTOVACUUM-NOT-SET` con criterio.

## 0.10.29 — 2026-07-25

- **OBS-DB-SLIM 4b (codice):** rimuove il modello ORM `Observation`, i path retention DELETE/COUNT legacy, e adatta `store_counts` (`observations: null` dichiarato). Dual-write resta spento. Aperto `DEBT-ALEMBIC-BASELINE-LEGACY-TABLE`.
- **OBS-DB-SLIM 4b (DB):** DROP `observations` + `VACUUM INTO`; file ~2.87 → ~1.85 GiB; freelist DROP ≈ 0.93 GiB. Chiude `DEBT-RETENTION-LEGACY-DROP-BLOCKER` e `DEBT-ORM-MODEL-RECREATES-TABLE`. Aperto `DEBT-AUTOVACUUM-NOT-SET`. Report: `docs/obs-4b-postop.md`.

## 0.10.28 — 2026-07-25

- **OBS-TRUST-CONVERGE:** gerarchia ownership di `operational_state` (archived > trust_quarantine > trust_protected > inventory). Chiude il ping-pong preesistente trust apply ↔ `reconcile_asset_presence` (structural=53 stabile da 0.10.25). Premio atteso: needs_apply=false → backup saltato.

## 0.10.27 — 2026-07-25

- **OBS-DB-SLIM 3b-iii:** elimina trust prefetch Observation; `active_discovery` da `presence_sources`; rimuove DNS hysteresis legacy e SELECT detector su `observations`; spegne dual-write (`record_observation` no-op). `T_prefetch_obs` → `null`. Retention/raw intatti. 4b congelato.
- **Post-deploy:** F1/F2/A4–A9 PASS. `structural=53` **preesistente** (già 0.10.25/0.10.26); gate convergenza mal specificato. Epoch calibrazione rimandata (`DEBT-CALIB-EPOCH`). Guadagno T_total (~174 vs ~348 s) via minore pressione scrittura su `observations` durante backup (A.5), non solo prefetch.
- Convergenza trust: cantiere 0.10.28.

## 0.10.25 — 2026-07-25

- **OBS-DB-SLIM 3b-i:** `scans` legge evidenza portal da `presence_sources` + IP current (niente Observation legacy). Sticky rank `IpAddress.source` invariato; dual-write host resta acceso. Verifica pre-GO: +5 asset = solo recupero sticky (mono-IP); nessun cambio semantica multi-IP live.

## 0.10.24 — 2026-07-25

- **OBS-DB-SLIM passo 3a:** stop append `Observation` per `fritz_wlan_assoc`/`fritz_mesh`; `materialize_wifi_association` (meta.link) resta. Dual-write host invariato (3b).

## 0.10.23 — 2026-07-25

- **OBS-DB-SLIM passo 2:** prune tabella legacy `observations` nel job retention orario (`OBS_TTL_LEGACY_DAYS`, default **7**, allineato al raw). Nessun VACUUM — file cala solo al passo 4.

## 0.10.22 — 2026-07-24

- **OBS-DEPLOY-01 (split):** `deploy.sh` — snapshot SQLite pre-deploy solo se `api` è tra i servizi; rotazione keep-3 su `data/backups/pre-deploy-*.db` subito dopo lo snapshot. Nessun prune/TTL su `observations` (materia OBS-DB-SLIM).

## 0.10.21 — 2026-07-24

- **OBS-033A (B2 + D12 + D13):** massa «Archivia rumore» segue `noiseIds` anche con griglia rumore vuota; rank 1 sempre rumore (anche su anonimi); `normalizeName` collassa `-_./spazi` e la parità normalizzata è rumore prima dei rank. Debito: `DEBT-NO-RECREATION-GUARD`, `DEBT-VERSION-SILENT-FALLBACK`.

## 0.10.20 — 2026-07-24

- **OBS-032 + D5-bis:** `scoreSpecificity` tratta i MAC incapsulati (coppie hex o 12 hex) come sintetici rank 1; massa «archivia rumore» include i membri chassis (`noiseProposalIds`); conferma dichiarativa su adotta chassis. Debito: `DEBT-PROPOSALS-HIDDEN-FROM-API`, `DEBT-ADOPT-NO-CHASSIS-GUARD`.

## 0.10.19 — 2026-07-23

- **OBS-OGGI-TRIAGE-031:** coda Oggi con triage proposte nome (`triageRules` D3–D8): gruppi adotta / verifica / rumore collassato; ignora archivia `NameProposal` (`POST …/reject-name-proposal` + `reject-bulk`); massa «archivia rumore» solo `mass_eligible`.

## 0.10.18 — 2026-07-23

- **OBS-DOSSIER-FIX-028:** CandidateList collassa dopo scelta (+ «cambia»); placeholder neutro; ordine Dossier chi sei → connesso; AssetChassis chassis-scoped (no inventario completo) + errore/vuoto; divergenza OS su label normalizzate. Base git riconciliata a live 0.10.17. Fingerbank 027 resta su branch separato.

## 0.10.17 — 2026-07-23

- **OBS-MANUAL-WINS-DIFF-026:** scelta OS umana vince a schermo (`labels.os` / `os_selected`); `os_divergence` quando nmap diverge; `field_sources` uniformato a `manual` (+ migrazione bootstrap); `used_ports` da nmap `<portused>` persistiti in evidence → `os_ports_used`.

## 0.10.16 — 2026-07-23

- **Restyle OBS-DESIGN-SPEC-025 (fasi A–F):** token ardesia + Inter/JetBrains Mono; ESLint `no-undef`; primitivi UI (DenseRow, StatusBadge, DirectionBar, HourlySparkline, CandidateList, SaveIndicator); Dossier con TOC sticky + OS multi-match; note auto-save; Inventario su tipografia sans; vista **Oggi** (coda triage proposte/nuovi/monitor). Spec in `docs/obs-design-spec-025.md`.

## 0.10.15 — 2026-07-23

- **Fix Inventario crash (regressione 0.10.11):** badge infrastruttura chiamava `catLabel()` non definito nello SFC → `ReferenceError` al primo device infra e smontaggio della vista. Ripristinato helper; hardened `matchDeviceFilter`/`sourceLabel(dhcp)`; `AssetDecide`/`AssetNotes` tollerano `assetId` null.

## 0.10.14 — 2026-07-23

- **Hostname DHCP → name_proposals (`source=dhcp`):** collector legge `dhcp.log`/`ja4d.log`, API `POST /api/ingest/dhcp-hostnames`. Confidence alta su hostname parlanti (`AmazonAQM-*`, `ROMO-*`, `*-bild-*`, …); skip rumore (`amazon-<hex>`, `Amazon`, Fritz `PC-MAC`). Solo proposta, mai auto-rinomina. Priorità display: umano > dhcp parlante > fritz sintetico (escluso) > oui.
- **Adozioni:** Amazon AQM 48/64, Loewe bild 7.77 (42) — identificati da hostname DHCP.

## 0.10.13 — 2026-07-23

- **DHCP fingerprint in dhcp.log:** `zeek/dhcp_fingerprint.zeek` estende `DHCP::Info` con `param_list` (opt 55) e `vendor_class` (opt 60); `@load` da `local.zeek` accanto a JA4. Input Fingerbank correlabile a MAC/IP senza package extra. Volume compose: `./zeek` intera.

## 0.10.12 — 2026-07-23

- **Sensore Zeek JA4 in produzione:** image `observatory-zeek-ja4:prod` (base `zeek/zeek:8.2` + package `zeek/foxio/ja4` v0.18.8); `@load ja4` in `zeek/local.zeek`. Impronte TLS (`ssl.log` → `ja4`/`ja4s`) + JA4D DHCP (`ja4d.log`). Prune esteso a `ja4d*`. Spike accettato (~98% ja4, RAM ~121 MiB/768). Rollback: `image: zeek/zeek:8.2` + `docker compose --profile span up -d --force-recreate zeek`.

## 0.10.11 — 2026-07-23

- **Abitudini — contesto AI in UI (OBS-DOSSIER-COMPLETE-022):** `/habits` espone `dst_context` + `dst_category` da `ip_intel`; riga destinazione = descrizione leggibile in evidenza, nome tecnico+IP solo in tooltip (fallback middle-ellipsis se `non_deducibile`).
- **Dossier autosufficiente:** `AssetChassis` / `AssetDecide` / `AssetNotes` estratti; `/dossier/:id` ha interfacce+presenza, Tu decidi (rinomina/adotta/ignora/watch), note editabili, Identity (OS protect) e Habits. Drawer Inventario riusa Decide/Notes (anteprima).
- **Contesto — automazione + confidence (022 addendum):**
  - job notturno `IP_INTEL_CONTEXT_NIGHTLY_*` (default OFF): solo `context IS NULL`, mai ritenta `non_deducibile`; stesso batch/sleep dello script
  - correzione manuale `PATCH /api/ip-intel/context` (`source=manual`, priorità max, ✎ in Abitudini)
  - ritento esplicito script `--retry-non-deducibile` (dopo validazione prompt)
  - UI: conf≥0.7 normale · 0.3–0.7 arancione + «probabile:» · manual tono distinto; tooltip con fonte+conf
  - prompt propositivo (ipotesi su indizi leggibili) — validare con `--preview` su batch misto prima di apply/retry
  - **confidence strutturata (OBS-IP-INTEL-STRUCT-023):** colonne `context_category` / `context_what` / `context_confidence` = fonte di verità; `context` blob solo mirror derivato; backfill one-shot con log fail (`scripts/ip_intel_context_struct_migrate.py`); `/habits` → `dst_category`/`dst_context`/`dst_confidence`/`dst_source`; priorità `manual` > `ai`

## 0.10.10 — 2026-07-23

- **Dossier pagina piena + sidebar RADAR/MAPPA (OBS-DOSSIER-PAGE-021):** `AssetIdentity` / `AssetHabits` estratti (fetch autonomo, OS actions nel componente); `/dossier` hub + `/dossier/:id`; drawer Inventario = anteprima + Tu decidi + «Apri Dossier»; stub onesti Oggi/Osservatorio/Come funziona.

## 0.10.9 — 2026-07-23

- **Abitudini — leggibilità destinazioni (OBS-UI-DEST-READABILITY-019):** label speciali senza query (`broadcast LAN` da `network_cidr`, `broadcast globale`, SSDP/mDNS/multicast); middle-ellipsis sui nomi lunghi (coda = dominio) + tooltip pieno; niente CSS end-clip.
- **Wave 1c live:** contesto AI applicato a ~392 hostname distinti (`ip_intel.context`); script riprendibile, batch 10 sotto TPM Groq.

## 0.10.8 — 2026-07-23

- **Wave 1c — contesto destinazioni (manuale):** colonne `ip_intel.context` / `context_source` / `ai_fetched_at`; classificazione hostname completo via Groq (batch 10–12 sotto TPM, `non_deducibile` valido); script `scripts/ip_intel_context_run.py` (niente job notturno). TTL 90g.

## 0.10.7 — 2026-07-23

- **Wave 1b — nomi destinazioni osservati:** tabella `ip_intel` (DNS A/AAAA + SNI `:443` confermato via `conn.uid`); provider `zeek_intel` → `POST /api/ingest/ip-intel` (cold start: offset EOF, niente backlog); Habits riempie `dst_name` (pubblici da cache, privati da asset locale). Nessun AI context in questo pezzo.
- **Zeek prune:** entrypoint esteso a `ssl*` / `http*` / `files*` (oltre conn/dns/dhcp); niente bare mode.

## 0.10.6 — 2026-07-23

- **Abitudini chassis-aware:** aggregazione per device fisico (`scope=chassis` default se ≥2 membri). Gate `resolve_asset_by_ip_at` invariato + union post-risoluzione; coverage = peggiore dei membri con motivo composto; provenienza per interfaccia (`Traffico da: eth #N · wifi #M`). Stesso quadro da primary o sibling; asset senza chassis invariato.

## 0.10.5 — 2026-07-23

- **Wave 1a completa — sezione «Abitudini» nel Dossier Inventario:** badge coverage (completo/parziale/sconosciuto), destinazioni con direzione out|in (Opzione A), volume 7g + sparkline ore locali (`Europe/Rome`), porte a scomparsa, stati vuoti onesti (`empty_kind`). Descrittivo; reset habits su `closePanel`.

## 0.10.4 — 2026-07-23

- **Bootstrap — trust dry_run prefetch:** 2 aggregati (`MIN`/`MAX` portal `seen_at` per MAC + `MAX(last_fdb_at)` per asset) prima del loop; da ~2N+1 query a ~3. Equivalenza col legacy N+1 coperta da test. Log: `mode=prefetch queries=N`.
- Allinea in tree anche il §5 già live in **0.10.3** (backup trust selettivo: solo strutturali; refresh soli timestamp senza backup; `start_period` 180s).

## 0.10.3 — 2026-07-23

- **Bootstrap — backup trust selettivo:** backup solo su modifiche strutturali (`trust_level` / quarantine / proposte archiviate). I refresh di soli timestamp (`portal_*` / `presence_state`) applicano senza backup (~60s risparmiati sui boot ordinari). `BOOTSTRAP_BACKUP=always` resta scappatoia. Healthcheck api `start_period: 180s`.

## 0.10.2 — 2026-07-23

- **Fix perdita ora chiusa su timeout POST flow:** batch N=100 su `POST /api/ingest/flows`, retry con ack per chunk (pending resta se fail), tetto K=3 / M=3000 con log `[zeek_conn] DROP ora …`, timeout flow 120s, observations post 60s. Non drop silenzioso in `finally`.

## 0.10.1 — 2026-07-23

- **Wave 1a Parte 2A — `GET /api/assets/{id}/habits`:** rollup 7g gate SQL temporale (binding history, tie→escludi), coverage 3 stati da topologia, mix-aware `bytes_out`/`bytes_in`, `empty_kind`, ore UTC + `timezone: Europe/Rome`. Mirror sources hardcoded (`DEBT-MIRROR-SOURCES`). Solo API — UI Abitudini = 2B.

## 0.10.0 — 2026-07-23

- **Wave 1a Parte 1 — pipeline direzione flow:** `bytes_out` / `bytes_in` / `byte_layer` end-to-end (Zeek `conn.log` → aggregate → ingest → `flow_observations` → `flows_summary`). App-layer primario; fallback IP-bytes (`byte_layer=ip`); mai null→0 silenzioso. Migration Alembic `h8e4f5a6b7c8` (+ colonne idempotenti in `schema_migrations`). Storico: out/in NULL. Inizia il filone behavioural.

## 0.9.12 — 2026-07-22

- Attribuzione OS **chassis-aware**: se nmap risponde col MAC di un sibling dello stesso chassis (gate: `origin` ∈ {auto, manuale}, ≥1 di C1/C2/C3, no X1), l’OS va all’**owner** del MAC + mirror sul target dello scan; stats `os_attributed_via_chassis_sibling`. Nessun merge identity; `chassis_grouping` non toccato.

## 0.9.11 — 2026-07-22

- Osservabilità attribuzione OS su MAC mismatch: `fingerprint_stats.mac_mismatches` (+ `os_discarded_mac_mismatch` / messaggio), `scan_run.message` esplicito, Dossier label «OS non attribuito (MAC discordante — vedi dettagli)» con tooltip. Nessuna fusion identity, nessun cambio worker.

## 0.9.10 — 2026-07-22

- **DEBT-COLLECTOR-PRIVILEGED risolto per rimozione:** nmap **in-image** nel collector (`apt install nmap`); `nmap_scan.py` esegue il binario locale (no `docker run` / no `instrumentisto/nmap`).
- Compose collector: **drop** `/var/run/docker.sock`, **drop** `privileged: true` — restano solo `NET_RAW` + `NET_ADMIN` (pattern Zeek).
- `SCANNER_PRIVILEGED` resta **false** al deploy finché staging non conferma ARP (`-sn` con MAC) e un `os_fingerprint` mirato con flag true. Accensione OS = solo dopo quella verifica.

## 0.9.9 — 2026-07-22

- Dossier «Chi sei»: parser identità pulito (`GET /api/assets/{id}/identity`), OUI resident (`oui_vendors` + `scripts/oui_refresh.py` manuale), sezione UI nel pannello Inventario con ignoti dichiarati.
- Opt-out OS per-asset (`meta.os_fingerprint_opt_out`, default per tipo iot/domotica/media — **zero brand** hardcoded); toggle «Proteggi da scansione OS».
- Semaforo `GET /api/system/scan-readiness` (green/yellow/red + motivo) sul bottone «Rileva OS ora».
- OS detection **canale spento**: `SCANNER_PRIVILEGED=false`; `/scan-os` → «OS non disponibile, scanner non privilegiato». Accensione OS = cantiere 0.9.10 (`DEBT-COLLECTOR-PRIVILEGED`: nmap-in-image, drop docker.sock/privileged).

## 0.9.8 — 2026-07-22

- LEVA B SQLite lock: `reconcile_all_asset_presence` solo su `/fdb-reconcile` (collector `reconcile_presence=False` su nmap/ssdp/printer/fritz/scan-batch); anti-burst `PRESENCE_RECONCILE_MIN_INTERVAL_SEC=600` (~1–2 pass/15'). Log `[fdb-reconcile] presence pass|coalesced`.

## 0.9.7 — 2026-07-22

- Ondata 1 audit portale (11 finding UX): badge calibrazione stabile su refresh fallito; Plant chip fonte GS308 + freschezza switch + ruolo `span` (p22 LGS328C); sticky inventario e Monitoring (`.table-scroll-x` scrollport 72vh); middle-ellipsis topologia; empty states; età proposte; form Plant azzerato al close. Solo presentazione — VERSION bump al deploy.

## 0.9.6 — 2026-07-21

- Post-0.9.5: sub-timing trust (`dry_run` / `backup` / `apply`); rotation backup elimina anche sidecar `.db-wal`/`.db-shm`; prune Zeek locale esteso a `dns*`/`dhcp*` (no `-b`); `utcnow` → `datetime.now(timezone.utc)` naive nel codice recente.

## 0.9.5 — 2026-07-21

- Bootstrap speed: timing per-step nei log (`[bootstrap] step N …: X.Xs`); trust single-pass (riuso `plan` del dry_run, assunzione single-writer pre-uvicorn); retention backup `observatory-*.db` keep 3 + `pre-deploy-*.db` keep 3 + `snapshot-*.json` keep 20; `BOOTSTRAP_BACKUP=auto|always|never`; log `backup saltato (nessuna modifica trust)`.

## 0.9.4 — 2026-07-21

- UI SPAN: `GET /api/flows/summary` (RO), card Sensore SPAN + Flussi (beta), etichette present_now 30m vs 24h, collasso flapping (`UI_FLAP_COLLAPSE_MIN=6`), residuo Kuma → «importato».

## 0.9.3 — 2026-07-21

- Zeek SPAN FASE B (wiring inerte): compose profilo `span` (`mem_limit` 768m), policy `conn.log` JSON, provider orario → `/api/ingest/flow`, retention `flow_observations` 30gg, checklist MemAvailable in OPTIONAL_SENSORS.
- Bond Cassiopea sciolto: `DEBT-LAG-CASSIOPEA` CHIUSO; eth0 LAN / eth1 SPAN; ritiro monitor «Cassiopea — NIC 2» (`.3.24`); runbook + script span/smoke.

## 0.9.2 — 2026-07-21

- Chassis grouping virtual-MAC (`RULE_VERSION=2`): **R1** flip-bit0+last2 AUTO se univ `noto` unico; **R2** prefix5 allentato solo OUI switch allowlist (`D8:EC:5E`) con guard nominati. Echo/Sky fuori allowlist non fondono. Chiude rumore card «Nuovi».

## 0.9.1 — 2026-07-21

- Fingerprint B2: profilo `os_fingerprint` (`-O` se privileged), materialize `os_hints`/services → `fingerprint_facts` + Endpoint/Service, guard MAC su `asset_id`.
- Watch governabile da UI (toggle), fingerprint on-sighting priority=0 con cooldown 10′ + dedup coda; Suggestion classify da fact OS + notifica; nightly batch gated OFF (`OS_FINGERPRINT_NIGHTLY_ENABLED=false`).
- Hotfix: timeout coda scan 60s, `--osscan-guess`, tie-break OS a parità accuracy, `disable_watch` rimuove `meta.watch`.

## 0.9.0 — 2026-07-21

- Multi-IP per ruolo: elezione per rango fonte + isteresi (niente last-write-wins), `ip_addresses.role`, sticky source, `ip_bindings` API; `endpoint.ip_change` solo sul primario. Chiude DEBT-TOPO-IP-CONTEXTUAL.
- Bonifica duplicati storici `(iface,ip)` + UNIQUE index; dedup raw L3 = MAC+IP.
- Fingerprint facts B1: `fingerprint_facts`, writer da segnale già in store, fetch SSDP con guard SSRF, classify Conferma/Adotta, `fingerprint_summary` nel naming; fix OS sysDescr (no hostname).
- VERSION runtime da `/api/health` (sidebar) — già in `e3da871`.

## 0.8.3 — 2026-07-21

- Filo backend audit (F2/F13/F14/F28): deny-list + purge placeholder identità (`none`/`none-N`); scan-targets evidenza cross-row portal; unità link topologia normalizzate; KPI monitor = unione problemi con `problem_silenced` separato.

## 0.8.2 — 2026-07-21

- Audit UX Cowork assorbito — ondate 1–4 (F1–F27): timezone unificato (`formatTime` + LocalClock), router/auth/loading, responsive, stati/filtri/microcopy, card Nuovi/Problemi.
- Single-source versione: `observatory/VERSION` (Docker + vite + API); `.dockerignore` per context snello.
- Prompt AI naming: campo `evidence` sempre in italiano, stile telegrafico.
- Debito annotato: `DEBT-TOPO-IP-CONTEXTUAL` in [`docs/KNOWN_DEBT.md`](docs/KNOWN_DEBT.md).

## 0.8.1 — 2026-07-20

- FASE 2 kuma→ping: migrazione selettiva (10 monitor) a ping nativo; 13 `kind=kuma` archiviati (storia conservata); GS308EP pinned su `192.168.1.8`; Cassiopea un solo ping sul bond `.1.3`.
- Hook PATCH asset: cambio reale `is_critical`/`category` → `reconcile_asset_monitor` (unarchive/archive, mai delete).
- Boosters mesh (asset 9/11): categoria `infrastruttura`; `config.retain` solo escape hatch.
- UI: badge calibrazione sidebar contenuto (`max-width: 100%`, giorno sempre visibile).
- Script: [`scripts/migrate_kuma_fase2_to_ping.py`](scripts/migrate_kuma_fase2_to_ping.py); censimento/diff in `docs/kuma-to-ping-fase*.txt`.

## 0.8.0 — 2026-07-20

- FILO 2b: `devices_*` in `/api/dashboard`, KPI Device attivi, link stale; `device_counters` allineato all'inventario (24h, ignorati, chassis).
- Triage stale: 20 MAC privacy residui restore → `status=ignorato` (no delete).
- FILO 3: `services/ai_naming.py` — proposte nome via LLM (Groq), contratto nome/evidenza/room, validazione anti-MAC/IP/vendor/ridondanza, soglia confidence, batch rate-limited, bottone pannello + badge `ai` in Proposte, adozione solo umana.
- DEBT-PRIVACY-MAC-CHURN annotato in [`docs/KNOWN_DEBT.md`](docs/KNOWN_DEBT.md).

## 0.7.1 — 2026-07-20

- Inventario FILO 2: lista device (chassis o singleton) + pannello slide-in; `AssetOut.chassis_id`; compose client-side.
- Fix freshness: `parseSeenMs` tratta ISO naive come UTC (niente skew +2h IT).
- `scripts/deploy.sh`: exclude cablati `data/` e `.env`, snapshot `pre-deploy-*.db`, niente `--delete`.
- `scripts/nightly-backup.sh`: DB + `.env` in `observatory-backups/`, retention 14g (ADM cron 04:00).
- Nota incidente rsync: [`docs/incident-20260720-rsync-delete.md`](docs/incident-20260720-rsync-delete.md).

## 0.7.0 — 2026-07-20

- Chassis grouping layer (FASE B): tabella `chassis` + `assets.chassis_id` (presentation, no merge identity/presence/`is_current`).
- AUTO C1–C4 + guard X1; C4 stretto (others = no dedicated port e no IP); isteresi dissolve; evidenza in `meta`; origin manuale/adottato rispettato.
- API `GET /api/chassis`; `inventory-summary` espone `devices_total` / `devices_active` accanto ai contatori assets_*.
- Hook post `/fdb-reconcile` + backfill bootstrap; dissolve membership via query FK.
- Live: 6 chassis (membership FASE A), presence delta 0, reconcile idempotente.

## 0.6.1 — 2026-07-20

- Cutover nmap: `mark_missing` + `wlan_associations` sul POST `NmapHostsProvider` (una volta/ciclo); batch discovery thin `hosts=[]` / `mark_missing=False`. Ping-only resta raw-only.
- Guardrail: `mark_missing=True` solo se nmap `ok` e lista non vuota — evita missing di massa se nmap fallisce e restano solo wlan.

## 0.6.0 — 2026-07-19

- Nmap #4 chiuso come provider dual: `NmapHostsProvider` → `/observations` (MAC upsert + dedup con `scan-batch:ping`); ping-only resta misura/raw-only (mai FE). Live `/22`: unresolved=1 = Cassiopea (tie ALB).
- Debiti: `DEBT-NMAP-CUTOVER` (cutover batch non urgente); nota ALB su `DEBT-LAG-CASSIOPEA`. 2b materializza-ping-only non serve.

## 0.5.14 — 2026-07-19

- Nmap #4 Fase 2a (misura): `NmapHostsProvider` dual → `/observations` + `SensorRun(source=nmap)`; MAC upsert; ping-only solo contatori (`kept`/`resolved`/`unresolved`), zero scritture Asset / no FE. Batch ping invariato.
- Nmap #4 **chiuso** come provider: live `/22` — dual MAC ok, unresolved=1 = Cassiopea (tie ALB, DEBT-LAG-CASSIOPEA); 2b non serve. Debito: `DEBT-NMAP-CUTOVER` (cutover batch non urgente).

## 0.5.13 — 2026-07-19

- BUG 1: `interface_role` A2 — uplink solo MAC switch su link strutturale; AP→infra; host dietro multi/AP→endpoint. Helper unico + backfill in `/fdb-reconcile` con fingerprint (porte/MAC/link + Switch + asset category/name) e TTL full ogni 20 cicli; skip a regime se invariato.

## 0.5.12 — 2026-07-19

- BUG 5: clear automatico (`import`/`fdb`) di `asset_id` infrastruttura su porte con link strutturale confermato, in `reconcile_physical_links` (O(link)); prevent su import e `_apply_stable_fdb_candidate`. `source=manual` intoccato. 328c:24 fuori scope.
- Debito: DEBT-TOPO-IP-CONTEXTUAL (BUG 3 declassato) in `docs/KNOWN_DEBT.md`.

## 0.5.11 — 2026-07-19

- BUG 4: Percorso rilevato — label uplink solo porta di arrivo (niente ↔) e step Core non duplicato.

## 0.5.10 — 2026-07-19

- LEVA 1-bis (a): collector POST `/fdb-reconcile` sempre a fine poll FDB (anche 0 switch ok / switches-snmp fallito) → ≥1 `reconcile_all`/ciclo garantito.

## 0.5.9 — 2026-07-19

- LEVA 1-bis: `/fdb-switch` non chiama più `reconcile_all_asset_presence`; un solo pass presence a fine poll in `/fdb-reconcile` (binding per-switch restano).

## 0.5.8 — 2026-07-19

- LEVA 1: sul path Fritz topology, `reconcile_all_asset_presence` solo ogni 3 cicli; materialize host resta ogni tick. Flag `reconcile_presence` su `/observations`.

## 0.5.7 — 2026-07-19

- Ripristina il feed Printer al dual approvato (solo host già in discovery batch); rimuove orphan mDNS non approvato.
- Mantiene `docker-cli` nel collector (fix nmap da 0.5.6).

## 0.5.6 — 2026-07-19

- Collector: `docker-cli` nell'immagine (nmap via docker sock).

## 0.5.5 — 2026-07-19

- Printer #3 provider: envelope `kind=printer` / `entity_key=IP` via `/observations` (dual con `enrich_printer_hosts`).
- Anti-ghost / anti ri-categorizzazione: `attach_printer_evidence` resolve per IP@`observed_at`, mai Asset L3-only FE.
- `printer_first_seen` / `printer_last_seen` su Asset; stesso `now` di `meta.printer.last_seen`.
- Alembic `d4b02f8c3159` (batch_alter SQLite): colonne printer — backup pre-upgrade.
- `printer` fuori da `PORTAL_EVIDENCE` (come SSDP).

## 0.5.4 — 2026-07-19

- Sidebar: sotto «LAN Observatory» mostra `vX.Y.Z · build …`; rimossi «rete palazzo» e «offline-first».

## 0.5.3 — 2026-07-19

- SSDP #2 provider: envelope `kind=ssdp` / `entity_key=IP` via `/observations` (dual con proposals nmap).
- Anti-ghost: `attach_ssdp_evidence` resolve per IP@`observed_at`, mai Asset L3-only FE.
- `ssdp_first_seen` / `ssdp_last_seen` su Asset (liveness fuori dalla FSM di presenza).
- Alembic `c3a91e7b2048` (batch_alter SQLite): colonne SSDP — backup pre-upgrade, upgrade/downgrade testati.
- SSDP fuori da `PORTAL_EVIDENCE`; demote IP chiude `last_seen` per storico binding.

## 0.5.2 — 2026-07-19

- Fritz #1 (provider cabling): hostlist Fritz solo via `FritzHostsProvider` (`source=fritz`, ciclo ~60s).
- Discovery 900s (passo B): niente `fetch_host_list` nel merge; `scan-batch:ping` non emette più `kind=fritz`.
- Mesh/WLAN associations e FDB/wlan status restano nel path topology/discovery.
- Dedup raw resta (a): bucket 60s allineato — idempotenza, non conferma multi-fonte.

## 0.5.1 — 2026-07-19

- Path ingest unico: `/observations` materializza lo stato derivato; `scan-batch` è adattatore sottile.
- Dedup cross-source su `ObservationRaw` (`source` fuori dalla chiave) con upsert atomico `ON CONFLICT`.
- Legacy `Observation`: append solo quando il raw crea una riga nuova (`record_legacy=created`), così il cablaggio multi-fonte non gonfia `Finding.occurrence_count`.
- UI calibrazione: Salute sensori, hero calibrazione, favicon LO in stile Matrix.
- Loadtest store: log strutturato `error_records`; gate concurrent senza `other_errors` sul path atomico.

## 0.5.0 — 2026-07-18

- Chiude M1b: soglie gate DB esplicite, `tools/measure_store_gate.py`, cutover Alembic documentato.
- M2: host ping-only/IP-only, match MAC esatto (niente same_device), FDB per-switch, esclusione uplink/virtual da presenza, generic FRITZ allineato (no flicker).
- M3: identity fusion multi-segnale, presenza per-interface, rimozione gate mark_missing >=8/25%, API merge/split con evidence.
- M4–M5: Snapshot/Drift/Finding in shadow-mode; `scoring.calibrated=false` di default (solo alert deterministici).
- M6–M8: detector attivabili, notifiche astratte OFF di default, ingest flow opzionale.
- M9: compose con profili/healthcheck, versione `v0.5.0`, docs sensori e backup.

## Non rilasciato — M1 (fondamenta ingestione/osservabilita)

- Aggiunge il contratto provider (collector) con wrapper timeout/retry/rate-limit e `SensorRun` per ogni esecuzione.
- Introduce l'envelope v2 normalizzato con `dedup_key` idempotente, `l2.mac_type` e `interface_role` (default `unknown`, derivazione in M2).
- Aggiunge lo store osservazioni append-only (`observations_raw`), il rollup (`observations_aggregate`) e le metriche baseline (`metric_snapshots`).
- Endpoint ingest v2 `POST /api/ingest/observations` idempotente; `scan-batch` invariato con dual-write nello store grezzo.
- Retention/rollup al giorno zero con TTL provvisori + pruning heartbeat (`POST /api/ingest/retention-run`).
- Metriche di affidabilita discovery (sez. 13) via `GET /api/reliability` e `GET /api/sensors`.
- Adotta Alembic (batch mode + naming convention, baseline schema); il runtime resta su `create_all` + migrazioni additive fino al cutover documentato.
- Additivo e feature-flag: identity fusion, presenza, drift e findings restano invariati (M2+).

## 0.4.0 — 2026-07-18

- Integra il modello di presenza trusted con timestamp distinti per portale e FRITZ!Box.
- Aggiunge monitor nativi, riepilogo Internet, incidenti aggregati e gestione completa dalla UI.
- Aggiunge scansioni difensive persistenti con approvazione, avanzamento e annullamento.
- Introduce i ruoli operativi delle porte e compatta i dettagli tecnici nei drawer.
- Unifica tutti i filtri e gli stati booleani nel toggle Matrix accessibile, senza checkbox native.
- Rimuove l'integrazione runtime con Kuma e aggiunge la migrazione one-shot con backup.
- Conserva le correzioni post-v0.3 per WLAN repeater, blocco WAN, identità LGS, flapping, speedtest e storico dispositivi.
- Archivia in sicurezza i monitor ping automatici coperti da monitor attivi, anche cross-kind.
- Rende l'ACK degli incidenti atomico e idempotente, con gestione esplicita della contesa SQLite.
- Deduplica e ordina gli IP candidati alle scansioni, consentendo override validati e label OUI leggibili.

## 0.3.0

- Introduce inventario evidence-based, topologia operativa, monitoraggio Internet e azioni difensive controllate.
