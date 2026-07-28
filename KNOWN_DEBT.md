# Debito noto (bassa priorità)

Voci consapevoli, non in coda di fix immediata. Non “dimenticate”: esplicite e fuori scope finché non riprese.

## DEBT-HISTORY-PATH-UNWIRED

- **Priorità:** bassa — aperto W8-fix / 0.10.63 (correzione contraddizione B5 della review W8).
- **Cosa:** `resolver.history()` (`api/app/facts/resolver.py`) esiste ed è esportato (`app/facts/__init__.py`) ma è **senza chiamanti**: nessun router lo invoca e **nessun endpoint espone `?history=true`** (verificato: grep chiamanti + elenco route routers/ — solo `proposal_history`/`warning_history`/monitor history, estranei ai fatti). Il contratto «storico su richiesta esplicita» è **dichiarato ma non cablato**.
- **Conseguenza:** l'API è corrente per default *perché* lo storico non è esposto (non per una scelta di gating). Non è una regressione: è codice previsto e inerte.
- **Ripresa:** quando un consumatore avrà bisogno dello storico dei fatti, cablare `resolver.history()` a un endpoint con `?history=true` (default corrente). Fino ad allora resta inerte.
- **Vietato:** dichiarare `?history=true` come funzionante finché non è cablato; rimuovere `resolver.history()` o riclassificarlo silenziosamente come morto (è la superficie sanzionata per lo storico).

## DEBT-WPGATE-CURRENCY-COUNT-LOCAL

- **Priorità:** media — aperto W8-fix2 / 0.10.63.
- **Cosa:** `scripts/wp_gate.py:103` esegue `COUNT(FactAssertion WHERE state=="current")` — una lettura di correntezza dei fatti **fuori dal resolver**.
- **Perché è un secondo autore di correntezza:** il resolver applica TTL / `_maybe_stale` / R-E per decidere cosa è «corrente adesso»; un `state=="current"` grezzo in SQL **può divergere** dal corrente effettivo del resolver (es. righe scadute non ancora marcate stale). È una **seconda definizione di «corrente»** dentro lo strumento che certifica la produzione.
- **Chi lo consuma:** il valore «FA current» stampato nella riga REGIME di `wp_gate` (baseline dei report d'ondata).
- **Risoluzione prevista:** helper di conteggio corrente in `api/app/facts/` (es. `facts.count_current(...)`) che riusi il resolver; `wp_gate` lo chiama invece dello SQL grezzo. È una **micro-ondata runtime successiva** (tocca `api/app/facts/`), **non ora**.
- **Stato nel gate:** sanato in `TEMPORARY_ALLOWLIST` di `w8_currency_gate.py` con `debt=DEBT-WPGATE-CURRENCY-COUNT-LOCAL` (stampato in testa all'output; l'esito è `PASS (con 1 eccezione temporanea)`).
- **Vietato:** dichiararlo chiuso allowlistandolo in **permanenza**; introdurre altre letture `state=="current"` grezze fuori dal resolver.

## PRESIDIO-CURRENCY-GATE (presidio permanente, non debito)

- **Natura:** presidio, non debito da chiudere — istituito W8 / 0.10.63; indurito W8-fix / W8-fix2.
- **Cosa presidia:** la correntezza dei FATTI si legge SOLO dal resolver (`api/app/facts/`). Nessun altro consumatore può interrogare `FactAssertion` per decidere «qual è il valore adesso» (evidenza si scrive, stato si deriva — F-7).
- **Come (versione consegnata):** `scripts/w8_currency_gate.py` — scope **`api/** · scripts/** · collector/****, esclusi `api/app/facts/**` (fonte protetta) e i due file d'ondata. **Tre sentinelle:** simbolo ORM `FactAssertion`; tabella `fact_assertions` dentro chiamata SQL (`text(`/`.execute(`/`.exec_driver_sql(`); COMBO fact-token + `'current'` quotato. Allowlist **per (file, snippet, N)** con conteggio (N+1 = violazione) + sezione **TEMPORANEA** `(file, snippet, N, debt)` con `debt` obbligatorio (voce senza debt → exit 1). Ha `--selftest`.
- **Criterio del ruling (W8-fix2):** `api/app/facts/**` escluso perché è la fonte; **ogni altro consumatore, tooling compreso, si allowlista riga per riga** (come `admin.py`), MAI per path intero.
- **Stato W8-fix2:** **0 violazioni · 17 eccezioni permanenti** (8 api + 9 tooling `wp_gate`/`wp_diagnose`) · **1 temporanea** (`DEBT-WPGATE-CURRENCY-COUNT-LOCAL`) → **PASS (con 1 eccezione temporanea)**. Selftest **PASS** (3 violazioni attese + config-check debt).
- **Limitazione dichiarata (R6):** B1(i) è **MITIGATO, non chiuso** — una stringa SQL costruita su più righe e concatenata sfugge alle tre sentinelle. Non dichiarare «chiuso».
- **Da eseguire:** a ogni ondata futura, con output completo, **insieme a I6**.
- **Non presidiato (criterio dichiarato):** `ip_addresses.is_current` = elezione IP (F-15), non correntezza dei fatti (pre-condizioni W3: `DEBT-DOUBLE-CURRENT-IP`, `DEBT-IFACE-IP-CARDINALITY-ROLE`, `DEBT-LASTSEEN-DUAL-SEMANTICS`); colonne di stato derivate `Asset` (F-7); evidenza grezza/oggetti di dominio; `resolver.history()` (`DEBT-HISTORY-PATH-UNWIRED`).
- **Equivalenza (G8):** `scripts/w8_g8_equivalence.py` — **read-only sulla TRANSAZIONE DB** (`db.rollback()`, nessun commit; file versionato). Confronta `asset.name` (resolver vs presentazione vs endpoint) e `os.guess` (resolver vs colonna `Asset.os_guess`): `DIVERGE=0` non-regressione. `--mutate-probe <id>` = controllo negativo (`DIVERGE=1` + FAIL).
- **Doc:** [`docs/obs-design-spec-025.md`](obs-design-spec-025.md) §12 · [`docs/obs-w8.md`](obs-w8.md) · [`docs/obs-w8fix.md`](obs-w8fix.md) · [`docs/obs-w8fix2.md`](obs-w8fix2.md)
- **Vietato:** allowlist con pattern generico o esclusione per path di un consumatore; leggere correntezza dei fatti fuori dal resolver; introdurre un secondo autore di stato (F-7).

## DEBT-FINDINGS-OGGI-CONFLUENCE

- **Priorità:** UX (architettura superfici) — aperto UX3 / 0.10.63
- **Cosa:** la route `/findings` è una coda parallela a Oggi (F-9). Misura in prod (2026-07-28): `/api/findings`=0, `/api/drifts`=0 — la superficie è **vuota** ed è in **shadow** finché lo scoring non è calibrato (Dashboard: «Findings restano in shadow»). Per non frammentare la coda operativa, `/findings` è stata **tolta dalla nav primaria** in 0.10.63.
- **Raggiungibilità (UX3.2.4 rispettato):** la route esiste ancora ed è raggiungibile dalla Dashboard (ReadySlot «Findings e severità → Apri Findings (shadow)» e card «Findings (shadow) → Apri») e per URL diretto. Nessuna funzione operativa resa irraggiungibile.
- **Confluenza rinviata:** quando i findings compositi diventeranno autoritativi (scoring calibrato, M4–M5), i loro elementi devono diventare **problemi dentro Oggi** (F-9), non una vista separata. Condizione: calibrazione completata + severità calibrata.
- **Vietato:** ricreare un hub findings separato da Oggi; esporre findings shadow come alert.

## DEBT-DASHBOARD-READY-SLOTS

- **Priorità:** UX (roadmap M3–M5) — annotato UX3 / 0.10.63
- **Cosa:** la Dashboard (ora «Panoramica», in nav) mostra `ReadySlot` placeholder («Presenza», «Findings e severità», «Coda attenzione») che in calibrazione dichiarano onestamente «Disponibile dopo la calibrazione» (I2, nessun dato inventato). Non sono rumore da rimuovere: sono slot di roadmap con etichetta d'attesa.
- **Ripresa:** riempimento a calibrazione conclusa (M3/M4/M5). Nessuna barra muta, nessun valore plausibile.
- **Vietato:** riempirli con valori stimati prima della calibrazione.

## DEBT-RECONCILE-CHURN-1

- **Priorità:** media (bootstrap regime) — **CHIUSO in F1-bis / 0.10.44**; **confermato D.6** sul boot1 di **0.10.45** (`structural=0`)
- **Cosa:** asset **116** aveva `trust_level=fritz_historical` ma `meta.operational_state=active`. Boot1 `needs_apply=true` / `structural=1` / `T_backup≈80s` perché `inventory_may_set_operational_state` permetteva `fritz_historical`→`active` se `reliable=True` (anche con 0 interfacce via reachability).
- **Fix:** inventory non solleva né smasha `trust_quarantine` (`fritz_historical` op_state o trust_level) — gerarchia invariata `archived > trust_quarantine > trust_protected > inventory_presence`. Test `test_quarantine_zero_interfaces_inventory_cannot_set_active`.
- **Vietato (storico):** tollerarlo come “regime ok”; caso speciale su `asset_id=116`.

## DEBT-IP-CURRENT-SCOPE-PER-ASSET → ri-caratterizzato come IDENTITÀ CHASSIS (W-D)

- **Priorità:** W4a/W4b (consolidamento chassis) — riaperto/riscritto F1-bis→W-D 2026-07-26
- **Fatto:** Cassiopea è modellata come **due asset record** — asset **5** «Cassiopea — NIC 1» tiene `192.168.1.3` CURRENT (id 9); asset **6** tiene `192.168.3.24` CURRENT (id 855). L’IP di management non è perso: è sull’altro record. Il ping fallito su `.3.24` dal container api è atteso (lato SPAN), non un sintomo.
- **Test di non-regressione (da chiudere in W4a/W4b):** dopo consolidamento, Cassiopea = **UN** apparato con **DUE** interfacce; entrambi gli IP correnti ciascuno sulla propria interfaccia; un solo nome canonico.
- **Vietato ora:** patch dati che forzi due current sullo stesso asset_id / stessa iface.
- **Doc:** [`docs/obs-f1bis.md`](obs-f1bis.md) · [`docs/obs-wd.md`](obs-wd.md)

## DEBT-DOUBLE-CURRENT-IP

- **Priorità:** pre-condizione **W3** — aperto W-D 2026-07-26
- **Cosa:** stesso IP con >1 riga `is_current=1` (stesso asset o asset diversi). Al backfill W3 collideranno con `uq_fact_assertions_current_slot`.
- **Casi enumerati (live, invariati da X.2):**
  - `192.168.1.2` — id **3** (asset 2, mgmt) + id **153** (asset 2, fritz)
  - `192.168.2.108` — id **15** (asset 11) + id **853** (asset 138)
- **Nota:** W3 richiede una **regola di risoluzione dichiarata PRIMA** del backfill. **NON** collassare ora. Cardinalità non cambiata da X.2 (dedup ≠ `is_current`).
- **Doc:** [`docs/obs-wd.md`](obs-wd.md) · [`docs/obs-wd-fix.md`](obs-wd-fix.md)

## DEBT-PROVISIONAL-IDENTITY-MERGE

- **Priorità:** post W-D (quando MAC sconosciuto → poi scoperto) — aperto W-D 2026-07-26
- **Cosa:** `entity_key` IP-only è marcato `payload.identity_provisional=true`, ma non esiste ancora un percorso di **fusione** quando il MAC viene scoperto in seguito (evitare duplicato).
- **X.2:** invariato — discriminante IP sul dedup non introduce merge. Cardinalità debito invariata.
- **Vietato:** inventare il merge in questa ondata.
- **Doc:** [`docs/obs-wd.md`](obs-wd.md) · [`docs/obs-wd-fix.md`](obs-wd-fix.md)

## DEBT-E3-AVAILABLE-FALSE

- **Priorità:** bloccante per E3 finché SNMP non è misurabile
- **Cosa:** E3-topological richiede access_port + mac_count misurato + soglia **esplicita** + simultaneità. Con poll SNMP in timeout, E3 = **available=false** (degrada a E2). Nessuna soglia inventata.
- **Vincolo:** non promuovere E3 finché `fdb_poll.ok` / misure porta non tornano.
- **Ripresa:** W2+ quando SNMP/LLDP writers misurano; requisiti accesso/poll in **DEBT-FDB-LLDP-PASSIVE**.

## DEBT-FDB-LLDP-PASSIVE

- **Priorità:** wave futura post W1.5-bis (writers SNMP / presenza) — **non** interrompe W1.5-bis
- **Cosa:** implementazione iniziale **passiva/read-only** FDB+LLDP: presenza/posizione L2, **non** identità; FDB ≠ ownership; LLDP/CDP solo corroborante (spoofabile). LGS310C/328C: SNMPv3 authPriv, RO, ACL solo Cassiopea, view Bridge/LLDP/ENTITY, no SET, segreti fuori repo/log, timeout/rate limit; LLDP/CDP non abilitato dove non serve. ObservationRaw: switch_id, port, VLAN/bridge-domain, timestamp, age/last_seen, acquisition_method, failure_state; dedupe per **transizione** non per poll. Alert «nuovo MAC su access» solo dopo classificazione misurata access/trunk/uplink/AP/powerline, inizialmente informativo; **niente** quarantena/shutdown auto. Spoof / MAC move / CAM flood / randomized MAC previsti; assenza alert ≠ sicurezza.
- **Doc:** [`docs/obs-fdb-lldp-passive.md`](obs-fdb-lldp-passive.md)
- **Vietato:** usarlo come scorciatoia identity/merge; SET SNMP; enforcement automatico porte; dichiarare “rete sicura” perché non ci sono alert.

## DEBT-ENTITY-KEY-MAC-IP

- **Priorità:** era bloccante W2 — **CHIUSO in W-D / 0.10.45** (2026-07-26)
- **Fix:** `entity_key_for` → MAC quando MAC noto; IP-only → provisional (`identity_provisional`). Test T-b verde.
- **Residuo correlato (non collassare):** righe IP duplicate / refresh-as-transition — vedi B.2 / DEBT-DOUBLE-CURRENT-IP.
- **Doc:** [`docs/obs-wd.md`](obs-wd.md)

## DEBT-IP-MIGRATION-NONETYPE

- **Priorità:** era bloccante W2 — **CHIUSO in W-D / 0.10.45** (2026-07-26)
- **Causa:** `elect_interface_primary` demoteva senza chiudere `last_seen` → `resolve_asset_by_ip_at` tornava `None` a T intermedio.
- **Fix:** alla demotion, `last_seen = now` se mancante/precedente. T-e / T-f verdi.
- **Doc:** [`docs/obs-wd.md`](obs-wd.md)

## DEBT-ALEMBIC-BASELINE-LEGACY-TABLE

- **Priorità:** bassa (igiene CI; Alembic **non** gira in prod) — unificato W-D 2026-07-26
- **Ex:** DEBT-ALEMBIC-MIGRATION-TESTS + baseline disallineata da tabella `observations` droppata.
- **Sintomi test:** `ix_observations_seen_at`, `assets.chassis_id`, `assets.printer_first_seen` su fixture/alembic.
- **Vietato:** inseguirli come fix runtime; schema prod = `create_all`.
- **Doc:** [`docs/obs-wd.md`](obs-wd.md)

## DEBT-IPP-PRECEDENCE (T-c / T-d) — CHIUSO in W6, rank corretto in W6-REVIEW (0.10.57)

- **Priorità:** media (autorità naming) — registrato W-D 2026-07-26, **chiuso** W6 2026-07-27, rank rivisto W6-REVIEW
- **Test:** `test_ipp_precedence_and_human_category_override` (T-c); `test_snmp_enrichment_creates_proposal_without_overwriting_name` (T-d) — entrambi VERDI
- **Root-cause:** `create_name_proposal` faceva `db.add` senza sincronizzare la relazione `asset.name_proposals` (proposte create invisibili in-sessione) + `best_guess` usava un secondo prospetto di pesi (`SOURCE_WEIGHT`) non coincidente con I5.
- **Fix (W6.2 + W6R.1):** `create_name_proposal` → `append` alla relazione (guardia `has_rejected_name_proposal` invariata, non ricrea rifiutate); `best_guess` ordina per `authority_for` (I5) primario + confidence. **Rank corretto in W6-REVIEW:** `ipp=88`/`snmp=87` (sopra dhcp, alteravano I5) → **`ipp=snmp=81`** — unico vincolo misurato `ipp>fritz` (T-c); sotto `dhcp=85`, I5 di prodotto intatto. Posizione tier vs dhcp = decisione di dominio (Michele, STOP-5). Misurato: 0 flip in prod. Nessuna seconda gerarchia. Test non indeboliti.

## DEBT-FDB-UPLINK-PORTAL (T-a) — CHIUSO in W7 (0.10.58)

- **Priorità:** media — registrato W-D 2026-07-26 (preesistente), **chiuso** W7 2026-07-27
- **Test:** `test_m2_discovery.py::test_fdb_skips_observe_portal_on_uplink_role` — VERDE
- **Osservato:** `portal_last_seen` valorizzato invece di `None` su ruolo uplink.
- **Root-cause:** `apply_fdb_observation` (`topology.py`) ricalcolava `interface_role` per-porta prima della guardia portale, declassando `uplink→endpoint` su un singolo hit FDB.
- **Fix (W7.3):** un hit FDB per-porta non declassa più un'interfaccia strutturale (`uplink`/`infra`); i downgrade restano del reclassify globale. Nessun azzeramento retroattivo di `portal_last_seen`. Test non indebolito.

## DEBT-MAC-IP-POLICY-WIRE — APERTO (wire additivo 0.10.58; policy piena CONSULTIVA 0.10.59; autoritativa rinviata)

- **Priorità:** wave presence — **wire additivo fatto** (0.10.58); **policy piena esposta come CONSULTIVA** (0.10.59); attivazione autoritativa delle regole #3/#5 **rinviata e condizionata**.
- **Cosa:** policy dominio MAC↔IP (chassis ≥1 IP corrente; eccezione powerline/510E; `present_l2_unaddressed`; supersession binding) — classifier `api/app/services/mac_ip_policy.py` + test contratto.
- **Fatto (W7.2, deploy 1/2, 0.10.58):** `classify_mac_ip_presence` collegato a `reconcile_asset_presence` come **solo segnale di presenza** (`present_l2_unaddressed` + `l2_only_allowed` → `reliable`); mai forza `stale`/`superseded` (F-7 intatto, non secondo autore). Misurato 0 cambi in prod.
- **F-14 — il wire è INERTE per costruzione (W7C-FIX, 0.10.59):** ogni decisione consumata dal wire (`present_l2_unaddressed`, `l2_only_allowed`) richiede `mac_fdb_fresh=True`; ma la stessa porta fresca genera in `reconcile_asset_presence` `physical_reasons=["FDB recente"]`, quindi `reliable` era **già** `True` senza il wire. Il wire non fa lavoro su `reliable` a prescindere dalla freschezza FDB. Misura corretta prod (`scripts/w7c_measure.py`, freschezza FDB reale): **0 hit** — vedi `docs/obs-w7close.md` §W7C-FIX.1. Correlato a DEBT-FDB-POLL-STALE (oggi 0 porte fresche).
- **Fatto (W7C.5, 0.10.59) — policy piena CONSULTIVA:** `inventory.mac_ip_policy_consultation` (read-only) + endpoint admin `GET /api/admin/mac-ip-policy-consultation` calcolano il verdetto della policy completa (regole #1..#5) per ogni asset e lo espongono come **divergenza visibile** accanto allo stato reale e all'evidenza che tiene presente il device. **Non scrive, non guida `operational_state`/`trust_level`/`reliable`** (F-7). Le regole #3/#5 **NON sono autoritative**.
- **Rinviato (attivazione autoritativa — decisione dominio Michele + correzione regole):** le regole #3/#5 marcherebbero `stale` device la cui presenza è dimostrata nello stesso istante da altre evidenze (FritzBox router, powerline, Sky box) — dissentono dalla realtà osservabile su una quota rilevante del parco e sbagliano sul gateway. **Il difetto è nella regola, non negli asset.** L'attivazione autoritativa è **condizionata alla correzione** delle regole che dissentono dalla realtà; fino ad allora il verdetto resta consultivo (I3). Blast-radius misurato read-only prod: vedi `docs/obs-w7close.md` (enumerazione per id).
- **Doc:** [`docs/obs-currency-mac-ip-policy.md`](obs-currency-mac-ip-policy.md), [`docs/obs-w7close.md`](obs-w7close.md)
- **Vietato:** attivare #3/#5 in modo autoritativo prima della correzione delle regole; usare la policy come scorciatoia di fusione chassis; inventare management IP.

## DEBT-FDB-POLL-STALE — APERTO (copertura FDB ferma; resa visibile in UI 0.10.60)

- **Priorità:** presentazione fatta (0.10.60); ripristino del polling FDB **fuori scope UX2** (non diagnosticare, F-13).
- **Cosa (misura F-13, RO 2026-07-27):** 46 switch port, **38 con `last_fdb_at`**, **0 freschi nelle 24h**; il più recente è **2026-07-25 14:52** (~57 h). `fdb_poll.ok=false` sui core LGS328C/LGS310C (SNMP timeout); GS308EP senza FDB per progetto.
- **Perché debito:** la mappatura porta→device (FDB) non si aggiorna; i dati di porta mostrati in Impianto/Topologia/Monitor sono la persistenza dell'ultima FDB riuscita. Un dato di porta vecchio di giorni **non va presentato come corrente** (I2/I3).
- **Fatto (UX2.2.4, 0.10.60) — solo presentazione:**
  - `web/src/observatoryUx.js` `fdbCoverageStatus()` (helper puro, test) calcola la freschezza dalla `last_fdb_at` di porta, **mai** dall'ora del poll fallito.
  - Impianto (`web/src/views/Plant.vue`): banner «copertura FDB non aggiornata: ultima mappatura … (circa N h fa)» + badge per-switch corretto (non spaccia più `fdb_poll.at` fallito come «dati al … (ok)»).
  - Monitor (`web/src/views/Monitoring.vue`): traffico/errori resi «—» quando `snmp_poll.ok≠true` (assente ≠ 0); poll marcato «non riuscito».
- **Correlato:** DEBT-PRESENCE-SOURCE-OUTAGE (copertura sorgente presence), DEBT-E3-AVAILABLE-FALSE (SNMP/LLDP non misurati), DEBT-MAC-IP-POLICY-WIRE §F-14 (con 0 porte fresche il wire non ha nulla su cui agire).
- **Vietato:** diagnosticare o riavviare il polling FDB dentro UX2 (F-13); mostrare la data del poll fallito come freschezza del dato; presentare occupazione porte vecchia come corrente.

## DEBT-MIRROR-SOURCES

- **Priorità:** bassa (Wave 1a behavioural) — config nota, non modellata in DB
- **Cosa:** le porte **sorgente** del port-mirror sul LGS328C (`p1`, `p21`, `p24` → sink `p22` / Cassiopea eth1) sono una **costante** in `api/app/services/habits.py` (`MIRROR_SOURCE_PORTS`) usata per il badge coverage «Abitudini».
- **Perché debito:** oggi è runbook/hardcode; uno spostamento fisico del mirror senza aggiornare il codice mentirebbe sulla coverage.
- **Fix quando servirà:** tabella/config persistita (es. `switch_ports.role=span_source` o meta switch) + bootstrap da doc; togliere la costante.
- **Vietato:** inferire le sorgenti mirror dalla sola assenza di flow; confondere sink `p22` con sorgente.

## DEBT-GROUPING-VIRTUAL-MAC

- **Priorità:** FASE B **deployata** (RULE_VERSION=2) + hotfix presentazione (`pickPrimary` / KPI chassis-aware). Residuo noto sotto.
- **Origine:** verifica L2 «Nuovi» 2026-07-21 (`docs/verifica-nuovi-l2-20260721.txt`); ricognizione FASE A 2026-07-21.
- **Regole (rule_version=2):**
  1. **R1 flip-bit0+last2:** AUTO diretto se target univ `noto` **unico**; multi-target → proposal `flip_bit0_last2_ambiguous`. Evidence in `chassis.meta.evidence.R1`.
  2. **R2 prefix5 allentato:** solo OUI in `SWITCH_OUI_ALLOWLIST` (`D8:EC:5E` Linksys); guard ≤1 nominato o stesso `chassis_id`. Echo/Sky OUI fuori → no R2.
- **Fuori R1/R2 (accettato):** radio Sky **universali** adiacenti (es. `38:A6:CE:79:D5:01`) senza cugino U/L e fuori allowlist R2 restano orfane. **Non** forzarle in AUTO grouping (fonderebbe box Sky diversi — rischio G2). Restano candidati **PROPOSTA** (non auto) da C3/C4 co-FDB o adozione manuale. Se la card Nuovi è 2 (asset 98 + una Sky orfana) invece di 1, è **accettabile**: 98 è lo sconosciuto vero; la Sky è radio nota da accorpare a mano o via co-FDB.
- **KPI privacy-churn:** chassis U/L puro (es. DA:76, solo MAC locally-administered, senza padre universale) **non** conta come `new_actionable` — rumore privacy, anche se `pickPrimary` lascia la riga senza nome.
- **Diff:** [`docs/debt-grouping-virtual-mac-fase-b-diff.txt`](debt-grouping-virtual-mac-fase-b-diff.txt); test `tests/test_chassis_virtual_mac.py`.
- **Vietato:** merge identity; toccare `is_current`; AUTO R2 senza allowlist; AUTO su radio Sky universali adiacenti senza C3/C4.
- **Assert live post-deploy:** card Nuovi = 1 (o 2 se Sky universale orfana); chassis assorbono radio R1; LGS328C+#109+#147; Echo Cabina≠Cucina; chassis DA:76 escluso dal KPI; `RULE_VERSION=2` nei chassis nuovi; presence delta 0.

## DEBT-LAG-CASSIOPEA (CHIUSO 21/07/2026)

- **Stato:** **CHIUSO** per rimozione bond 21/07/2026.
- **Topologia attuale:** bond sciolto — `eth0` = LAN `192.168.1.3/22` (LGS328C p8),
  `eth1` = SPAN sink `10.255.255.2/30` (LGS328C p22). Non più ALB / IP condiviso.
- **Cosa resta:** due Asset NIC (`…:01` / `…:02`) possono ancora comparire in inventario
  finché non si rivede il grouping chassis; non è più un problema di bonding.
- **Vietato (storico, non riaprire):** fingere ancora un LAG; rimaterializzare ping su
  `192.168.3.24` (NIC 2 legacy, IP non più esistente).
- **Postcheck / smoke:** [`scripts/span_postcheck.sh`](../scripts/span_postcheck.sh),
  [`scripts/capture_smoke.sh`](../scripts/capture_smoke.sh),
  [`scripts/span_preflight.sh`](../scripts/span_preflight.sh) (pre-scioglimento, storico).

## DEBT-NMAP-CUTOVER

- **Priorità:** chiuso in codice (cutover v0.6.1) — tenere come nota operativa
- **Stato:** fonte unica `NmapHostsProvider` → `/observations` con **`wlan_associations` nello stesso POST**; **`mark_missing=True` solo se nmap ok e non vuoto** (guardrail: nmap fallito/vuoto + solo wlan → mm=False, niente falso missing non-wifi). Batch discovery thin: `hosts=[]`, `wlan=[]`, **`mark_missing=False` esplicito** (mai doppio mm/ciclo). Ping-only resta raw-only.
- **Assert live obbligatorio al deploy:** presence delta 0; wlan assoc count ≠ 0; no missing spike; un solo `mark_missing`/ciclo quando nmap ok (`SensorRun.counts.mark_missing=1`, batch mm=0).
- **Vietato:** riattivare `mark_missing=True` sul batch discovery; mm con nmap vuoto/fallito; post nmap con mm senza wlan quando mm è True; materializzare ping-only/FE.

## DEBT-MONITOR-KUMA

- **Priorità:** chiuso in operatività (FASE 2 v0.8.1) — tenere come nota
- **Stato:** i 13 `kind=kuma` sono **archiviati** (storia conservata, mai delete). Dieci target infra/mesh girano come `kind=ping` nativo; DVR/LUMIN/openhabian restano solo archiviati finché non si attiva il toggle critico.
- **Residuo:** riprendere DVR (#2) / LUMIN / openhabian dal toggle critico se servono; non riattivare Kuma runtime.
- **Vietato:** ripristinare Kuma come dipendenza; delete delle righe kuma archiviate.

## DEBT-TOPO-IP-CONTEXTUAL

- **Priorità:** bassa (latente → perimetro ampliato 2026-07-21; discriminante raw ripristinato 0.10.46) — ex BUG 3 declassato
- **Invariante:** multi-IP sullo stesso MAC **non collassa** nello store raw (fatti distinti).
- **Stato raw:** **violato in 0.10.45** (`dedup_key` usava solo `entity_key` MAC-scoped → 5 IP → 1 riga). **Ripristinato in 0.10.46:** `entity_key` resta MAC; `compute_dedup_key` aggiunge discriminante IP (`fact_discriminant_for`). Identità ≠ dedup. Vedi [`docs/obs-wd-fix.md`](obs-wd-fix.md).
- **Perimetro definitivo:** multi-IP per ruolo (`primario` / `vpn` / `mgmt` / `servizi`). `endpoint.ip_change` **solo sul primario**. Casi noti:
  - **FRITZ!Box** (asset 1): 5 IP contemporanei sullo stesso MAC — `.1.1` primario, `.1.9` VPN LAN, `.1.4`/`.1.5`/`.1.6` (ruolo TBD servizi/altro); ×223 `ip_change`/24h documentati poi silenziati.
  - **GS308EP** (asset 4): `.1.8` mgmt (fatto). `.3.20` = binding Fritz storico sullo stesso MAC, **ownership da confermare** (non inventariale; non SPAN — SPAN=p22/NIC2 `.3.24` / sink `10.255.255.2/30`). Vedi [`docs/obs-ux-ip-308-verifica.md`](obs-ux-ip-308-verifica.md).
  - **Cassiopea (ex-bond):** `DEBT-LAG-CASSIOPEA` **CHIUSO** 21/07/2026 (eth0 LAN / eth1 SPAN).
- **Nota architetturale:** il dedup raw per-MAC scartava le osservazioni L3 multi-IP (sul Fritz 4/5 IP perse nel raw, `hit_count≈5` ma `l3.ip` resta solo `.1.1`) mentre l’upsert legacy scrive comunque i binding e gli `ip_change`: le due pipeline divergevano. Fix 0.10.46: `dedup_key` MAC+IP per L3.
- **Sintomo latente (BUG 3 originale / consumatore di correttezza) — MIGRATO W5 (0.10.54):** [`_resolve_ap_asset`](../api/app/services/topology.py) usa ora `resolve_asset_by_ip_at(ap_ip, observed_at)` (contestuale) invece di `is_current`; tie → None → fall-through sul nome. Gate G5 a writer fermi: 62 associazioni Wi-Fi, 0 sul path `ap_ip` → **0 differenze** (fix latente, equivalenza-preservante). Il facet «consumatore di correntezza» di questo debito è chiuso; la cardinalità/ruolo multi-IP resta tracciata in **DEBT-IFACE-IP-CARDINALITY-ROLE** (pre-condizione W3). Vedi [`docs/obs-w5.md`](obs-w5.md).
- **Copia ingest chiusa — W5-bis (0.10.55):** [`wifi_associations.resolve_ap_asset`](../api/app/services/wifi_associations.py) (risoluzione AP lato ingest Wi-Fi) era rimasta su `is_current` dopo la migrazione W5 della sola copia di `topology`; ora usa `resolve_asset_by_ip_at(ap_ip, observed_at)` con `observed_at` dall'associazione; tie → None → fall-through sul nome (I2). Equivalenza-preservante sui dati correnti (a ingest `observed_at ≈ now`). Copertura: `tests/test_w5_consumers.py` (contestuale + tie). Vedi [`docs/obs-w5bis.md`](obs-w5bis.md).
- **Fix quando servirà:** (1) ruoli IP + `ip_change` solo primario; (2) dedup L3 MAC+IP *(fatto 0.10.46)*; (3) nel solo ramo (b) di `_resolve_ap_asset`, `resolve_asset_by_ip_at` + `observed_at`; tie→None→fall-through. NON toccare `is_current` alla cieca su multi-NIC storiche.
- **Riattivazione:** attribuzione topologia sbagliata su IP DHCP migrato, oppure ripresa del rumore `ip_change` multi-ruolo dopo unmute.
- **Stato FASE B (codice):** elezione + `role` + dedup `mac|ip` + `ip_change` solo primario — in tree. Bonifica storica duplicate `(interface_id, ip)` resta fuori scope. UI secondari = FASE C.
- **Bonifica storica:** eventuali righe duplicate `(interface_id, ip)` pre-FASE-B restano; niente UniqueConstraint finché non c’è purge dedicato (fuori scope).

## DEBT-IFACE-IP-CARDINALITY-ROLE

- **Priorità:** pre-condizione **W3** — aperto W4a 2026-07-26
- **Cosa:** `asset.iface_ip` ha `cardinality=single` per interfaccia e il writer shadow registra **solo l’IP eletto** (`elect_interface_primary`). Sul Fritz (asset 1) esistono cinque IP simultanei (`.1.1` primario, `.1.9` VPN, `.1.4`/`.1.5`/`.1.6` servizi) — i non-eletti **non** compaiono nel layer assertion.
- **I2:** assenza di un IP in `fact_assertions` **non** significa che l’IP non esista.
- **W4b.3.3:** `current()` senza `excl_key` e con più righe `current` su cardinality `single` sceglie in silenzio per authority — collegato a questo debito; non collassare ora.
- **Prima di W3:** `excl_key` deve acquisire il **ruolo** (`fact_key + interface_id + role`), cardinalità `scoped`. NON inventare i ruoli mancanti ora (K3).
- **Vietato in W4a/W4b:** implementare il ruolo nella excl_key; collassare i doppi-current.
- **Doc:** [`docs/obs-w4a.md`](obs-w4a.md) · legato a DEBT-TOPO-IP-CONTEXTUAL

## DEBT-RH-BEFORE-REFRESH

- **Priorità:** media (correttezza resolver) — aperto W4b 2026-07-27
- **Cosa:** `_check_rh_conflict` gira **prima** di R-A refresh. Ogni refresh riesegue la scansione cross-fact; un valore già `current` può diventare `conflict_review` per un cambiamento altrove senza che l’osservazione in ingresso sia nuova.
- **Vietato in W4b:** correggere l’ordine ora.
- **Doc:** [`docs/obs-w4b.md`](obs-w4b.md)

## DEBT-LASTSEEN-DUAL-SEMANTICS

- **Priorità:** pre-condizione **W3** — aperto W-D-fix 2026-07-26
- **Cosa:** `elect_interface_primary` scrive `last_seen = now` alla demotion (chiusura amministrativa di intervallo) nello stesso campo «ultima osservazione».
- **Nota W3:** prima del backfill dichiarare per ogni campo quale semantica porta; le righe con `last_seen` amministrativo daranno `valid_to`, non un’osservazione.
- **Vietato ora:** correggere / biforcare il campo in questa ondata.
- **Doc:** [`docs/obs-wd-fix.md`](obs-wd-fix.md)

## DEBT-FRITZ-TR064-CREDENTIALS

- **Priorità:** operativa — **CHIUSO F0 2026-07-27**
- **Chiusura misurata:** Michele ha ripristinato le chiavi in `.env`. `docker compose restart collector` **non** ricarica env (USERNAME/PASSWORD len=0 nel container → ancora 401). Dopo `up -d --force-recreate --no-deps collector`: chiavi presenti nel container; hostlist **94** host; mesh `available` **6** assoc; **0** occorrenze 401/`credentials_invalid` post-recreate. Valori segreti mai letti/riportati.
- **Doc:** [`docs/obs-fritz-restore.md`](obs-fritz-restore.md)

## DEBT-PRESENCE-SOURCE-OUTAGE

- **Priorità:** alta (I2/I4 + churn boot) — aperto W4c 2026-07-27; **NON corretto in W4c** (W4c.5.2); **resta APERTO** con Fritz vivo (F0)
- **Fatto misurato (W4b boot1):** `structural=4` — asset **136, 140, 145, 148** `meta.operational_state` `active` → `stale_unlocated`. AD finestra 24h sceso 69→62.
- **Meccanismo:** `classify_asset` / `reconcile_trust_history` in [`api/app/services/trust.py`](../api/app/services/trust.py) (~170–189, ~474–489, ~618–621): senza `portal_last_seen` recente e senza protezione → bucket `stale_unlocated`. Con Fritz TR-064 muto i refresh hostlist non aggiornano la presenza → l’assenza della **sorgente** viene trattata come assenza del **dispositivo**.
- **Principio:** quando la sorgente che copriva un device è indisponibile, lo stato corretto è «non misurato» / «copertura sorgente non disponibile», non «assente».
- **F0 (Fritz vivo):** evidenza Fritz corrente su 88 asset; lift live solo **109** → `known` (non `confirmed_present`). **136** ha `discovery.fritz.active=True` ma resta `stale_unlocated` perché `lift_fritz_quarantine_on_active` esce solo da `fritz_historical`. Trust layer non corretto in F0/W4d.
- **Vietato in W4c/F0:** correggere il trust layer. UI (F2 / **0.10.51**): banner Fritz + copy «copertura sorgente non disponibile».
- **W-P (0.10.53) — trust layer corretto, debito NON chiuso:** `classify_asset` ora legge l'evidenza fritz-active fresca e deriva `known` (autorità fritz, mai `confirmed_present`); il lift non scrive più lo stato (evidenza→derivazione). Effetto misurato: 109 converge (fine oscillazione), 136 sollevato a `known`. Questo distingue «fritz vivo→known» da «fritz stale→stale/historical», MA **non** distingue ancora «sorgente non disponibile» (outage TR-064) da «dispositivo assente»: durante un'outage l'evidenza invecchia oltre la finestra e l'asset ridiscende. Serve un segnale di **copertura sorgente** (sensor_run/coverage) per chiudere. **RESTA APERTO** (non chiuso per prossimità, W-P.2.7).
- **Doc:** [`docs/obs-w4c.md`](obs-w4c.md) · [`docs/obs-ux2.md`](obs-ux2.md) · [`docs/obs-fritz-restore.md`](obs-fritz-restore.md) · [`docs/obs-wp.md`](obs-wp.md)

## DEBT-A2-CASCADE-AP

- **Priorità:** bassa (latente) — ex nota di confine BUG 1 / A2
- **Sintomo potenziale:** su porta AP, ogni MAC con `category=infrastruttura` diventa `interface_role=infra` e resta escluso dalla presenza FDB (`observe_portal` skip). Un repeater/powerline in cascata dietro un AP (secondo infra sulla stessa porta) sarebbe escluso da FDB anche se “visto”.
- **Stato oggi:** assente in rete — sulle porte AP c’è un solo MAC infra ed è l’AP bindato; i repeater restano nel path Fritz.
- **Riattivazione:** se un repeater/powerline dietro un AP scompare dalla presenza, valutare regola più stretta (solo l’AP della porta → infra; altri infra dietro AP → endpoint).

## DEBT-WLAN-ASSOC-GHOST

- **Priorità:** bassa (latente) — path assoc senza anti-ghost
- **Sintomo potenziale:** in [`materialize_wifi_association`](../api/app/services/wifi_associations.py), se `client_mac` non ha Asset, si crea via `upsert_observation_asset` (L2-only possibile). Non c’è resolve-o-niente come SSDP/Printer/nmap ping-only.
- **Stato oggi:** innocuo — cutover live: 36/36 wlan agganciano client già noti; 0 Asset creati da quel giro; Asset totali invariati.
- **Riattivazione:** se compare un Asset L2-only nato da `fritz_wlan_assoc` per un client mai visto altrove.
- **Vietato ora:** spegnere la create senza misura; trattarlo come bug attivo senza evidenza.

## DEBT-SKY-RADIO-FUSION

- **Priorità:** bassa / non urgente
- **Sintomo:** MAC consecutivi stesso OUI (es. `38:A6:CE:3E:9C:A8` / `:AB` / `:AE` sullo stesso chassis Sky) restano Asset endpoint distinti; le radio secondarie spesso senza IP (path Fritz hostlist, non wlan del ciclo nmap).
- **Perché non è un bug del cutover:** preesistenti (18–19/07); wlan non li ha creati.
- **Fix quando servirà:** feature identity fusion per-chassis (multi-MAC stesso device wireless), non merge ad hoc.
- **Vietato ora:** merge forzato solo per “pulire” l’inventario.

## DEBT-PRIVACY-MAC-CHURN

- **Priorità:** bassa / policy da progettare
- **Sintomo:** dopo triage stale FASE 2, resta la classe (d) `local_mac_con_ip` (MAC locally-administered con IP): a ogni rotazione privacy Wi‑Fi rifà apparire stale one-shot.
- **Origine:** MAC privacy (bit U/L) visti con IP in finestra breve; non ignorabili alla cieca come la classe (a) senza IP.
- **Fix quando servirà:** policy TTL auto-ignore (es. local MAC + no curation + inactivity N giorni) — non ora.
- **Vietato ora:** bulk ignorato della (d); DELETE asset; merge/fusion ad hoc.

## DEBT-COLLECTOR-PRIVILEGED

- **Stato:** **RISOLTO PER RIMOZIONE** in codice 0.9.10 (pre-deploy review).
- **Cosa è cambiato:** nmap installato nell’immagine collector; esecuzione diretta; **eliminati** mount `docker.sock` e `privileged: true`. Restano `cap_add: NET_RAW, NET_ADMIN`.
- **Gate operativo:** `SCANNER_PRIVILEGED` resta `false` finché staging non conferma: (1) discovery `-sn` con MAC/ARP, (2) un `os_fingerprint` con flag true produce `osmatch`. Solo allora alzare il flag sul NAS.
- **Residuo:** `run_deep_scan` API non usa più docker nested — richiede `nmap` nell’immagine API o la coda Azioni (`full_tcp`). Fuori dal vettore sock.
- **Vietato:** reintrodurre docker.sock sul collector; `privileged: true` “per sicurezza”; alzare `SCANNER_PRIVILEGED` senza smoke ARP/-O.

## DEBT-OS-LABELS-PREFIX-EQUIV (OBS-028)

- **Stato:** **CHIUSA in 0.10.32** — `os_labels_equivalent` solo troncamento nmap (`rest` match `^-\d`); edition upgrade non equivalenti.
- **Cosa (storico):** prefisso generico azzittiva divergenze tipo Windows vs Windows Server.
- **Vietato:** allargare ulteriormente il prefisso senza review.

## DEBT-CHASSIS-PARTIAL-SILENT (OBS-028)

- **Stato:** **CHIUSA in 0.10.31** — `partialWarning` in `AssetChassis.vue`; member/chassis fail dichiarati (no mono-NIC silenzioso).
- **Cosa (storico):** se `api.chassis()` o un fetch member fallivano, AssetChassis degradava in silenzio a vista mono-NIC.
- **Vietato:** ripristinare `api.assets()` full inventory come workaround.

## DEBT-PYTEST-COLLECTION-PY39

- **Priorità:** media (igiene suite locale) — OBS-031 V2
- **Cosa:** in locale (macOS **Python 3.9.6**) `pytest` non completa la collection: `tests/test_m6_m8_detectors_flow.py` importa `create_app` → FastAPI valuta `estimate_sec: int | None` in [`api/app/routers/system.py:23`](../api/app/routers/system.py) e fallisce senza `eval_type_backport`. Produzione API: **Python 3.12.13** (`python:3.12-slim`) — la stessa annotazione è nativa e non rompe.
- **Perché debito:** la suite «intera» non viene mai eseguita sul laptop dell’operatore; si lavora con `--ignore=tests/test_m6_m8_detectors_flow.py` o sottoinsiemi.
- **Fix quando servirà:** allineare la versione Python locale a ≥3.10 (ideale 3.12 come il container), oppure installare `eval_type_backport` nell’env di test, oppure riscrivere le annotazioni endpoint a `Optional[int]` dove FastAPI le valuta a import-time.
- **Vietato:** dichiarare «suite verde» eseguendo solo sottoinsiemi / ignore senza dichiararlo nel report.

## DEBT-HABITS-DIR-UNAVAILABLE

- **Stato:** **CHIUSA in 0.10.31** — DirectionBar testo «direzione non disponibile»; colonna value `n/d` allineata.
- **Cosa (storico):** barra idle silenziosa + totale bytes senza dichiarazione.
- **Vietato:** dedurre una direzione dai totali (`bytes` → inventare out/in).

## DEBT-MANUAL-CONF-BAR (OBS-026/028)

- **Stato:** **CHIUSA in 0.10.31** — CandidateList: badge «manuale» al posto della barra 100% per scelta autorevole.
- **Cosa (storico):** `accuracy: 100` disegnata come inferenza misurata.
- **Vietato:** estendere accuracy sintetiche ad altre fonti; rimuovere il subtitle «scelta manuale».

## DEBT-PROPOSALS-HIDDEN-FROM-API (OBS-031/032)

- **Stato:** **CHIUSA in 0.10.33** — `GET /api/assets?all_proposals=true` espone pending grezze (Oggi); specificità resta in `triageRules.js`.
- **Cosa (storico):** split 1/fonte + svuotamento fritz_only/stale/historical nascondeva la coda.
- **Vietato:** duplicare `scoreSpecificity` in Python.

## DEBT-ADOPT-NO-CHASSIS-GUARD (OBS-032 / D5-bis)

- **Stato:** **CHIUSA in 0.10.33** — `POST …/adopt-name` → 409 se chassis multi-NIC (≥2); Oggi non propone più confirm soft.
- **Residuo:** rename a livello chassis (spec 025) resta cantiere futuro.
- **Vietato:** bypass UI senza vincolo API.

## DEBT-MAC-REGEX-DIGIT-RUN (OBS-032)

- **Stato:** **VERIFICATA in 0.10.32** — 0 nomi attuali con corsa 12+ cifre; regex `triageRules.js` **invariata** (rischio asimmetrico teorico).
- **Cosa:** `\b[0-9a-f]{12}\b` può trattare 12+ cifre decimali come MAC sintetico.
- **Vietato:** allargare ulteriormente il pattern senza review; cambiare la regex senza hit misurati.

## DEBT-NO-RECREATION-GUARD (OBS-033 / B3)

- **Stato:** **CHIUSA in 0.10.33** — `create_name_proposal` / `has_rejected_name_proposal` su identity, OUI, SSDP, DHCP, AI, printer.
- **Cosa (storico):** generatori potevano ricreare pending dopo reject sulla stessa tupla.
- **Vietato:** considerare la purga/massa definitiva senza la guardia.

## DEBT-VERSION-SILENT-FALLBACK (OBS-033 / Q0b)

- **Stato:** **CHIUSA in 0.10.31** — senza `health.version` la sidebar mostra «versione non disponibile · {buildId}».
- **Cosa (storico):** solo `__BUILD_ID__` (gg/mm) sembrava una versione valida.
- **Vietato:** fallback che sembrano un dato valido.

## DEBT-BACKUP-ROTATION-SPLIT

- **Stato:** **CHIUSA in 0.10.30** (OBS-COERENZA) — un solo punto `backup_rotate_core` + `scripts/backup_rotate.py`; `deploy.sh` chiama `--apply` post-rsync. Protetti esclusi per nome. Vedi `docs/obs-coerenza.md`.

## DEBT-BACKUP-ALL-OR-NOTHING

- **Priorità:** media — costo boot/deploy
- **Cosa:** `needs_backup` è tutto-o-niente: una sola azione structural (es. asset 116 in A5 post-4b) produce una copia integrale ~1.85 GiB in ~133 s.
- **Fix futuro:** backup incrementale / skip se solo timestamp / soglia structural count.
- **Vietato ora:** cambiare semantica needs_backup in questo cantiere.

## DEBT-AGGREGATE-NO-RETENTION

- **Priorità:** media — crescita lenta ma monotona
- **Cosa:** `observations_aggregate` è **solo scritto** dal rollup raw (`retention.py` `rollup_raw_observations`); **nessun DELETE/TTL** su questa tabella. Live 2026-07-25: **0 righe** (prune raw non ha ancora prodotto volumi).
- **Stima crescita:** a regime, ~1 riga aggregata per `(source, window)` ogni 6h di raw potata. Con ~150–170k raw/giorno e source dominante `fritz`, ordine di grandezza **decine–centinaia di aggregati/giorno** dopo il 2026-07-27 — payload piccolo vs raw, ma senza TTL cresce senza limite.
- **Fix futuro:** TTL o rollup-of-aggregates dedicato. **Non** in OBS-PORTALE.

## DEBT-DNS-HYST-LEGACY-NOOP

- **Stato:** **CHIUSA in OBS-PORTALE ondata 4 (decisione)** — il gate DNS era già stato rimosso in 3b-iii; resta solo commento. `endpoint.missing` usa cycles / reachability / FDB / mesh, **senza** isteresi DNS. Non reintrodurre finché `observe_portal("dns")` non popola una sorgente calda; allora cantiere nuovo con segnale misurabile.
- **Cosa (storico):** lettura `Observation(kind=dns)` no-op dopo DROP legacy.
- **Vietato:** reintrodurre query runtime su tabella `observations`.

## DEBT-FINGERBANK-027

- **Stato:** **RIMANDATO** — branch `feature/obs-fingerbank-027` (`d20313e`, ~1.1k LOC: client on-demand + cache + DHCP opt55). **Non integrare in PORTALE.**
- **Decisione (2026-07-25):** cantiere dedicato **non prima del 2026-08-15** (dopo review grafica / hot-cold). Costo: API nuove, secret Fingerbank, wire Zeek DHCP, UI dossier.
- **Vietato:** merge silenzioso su main senza cantiere; chiamate cloud senza opt-in.

## DEBT-DETECTOR-OBS-LEGACY

- **Stato:** **CHIUSA in 0.10.30** (scelta **a**): `unexpected_dhcp_dns` e `llmnr_nbns_mdns` **rimossi dal registro** — abilitarli è impossibile. Ripristino solo con reader su `observations_raw` + test occurrence_count (cantiere nuovo).

## DEBT-RETENTION-LEGACY-DROP-BLOCKER

- **Stato:** **CHIUSA** (codice 0.10.29 + finestra DROP 2026-07-25) — DELETE/COUNT legacy rimossi da `retention.py`; risposta 1.1 in `docs/obs-4b-retention-blocker-answer.md`.
- **Evidenza A6:** `POST /api/ingest/retention-run` ok; `observations: null`; nessun raise; prune raw eseguito (`deleted=0` entro TTL). Vedi `docs/obs-4b-postop.md`.

## DEBT-ORM-MODEL-RECREATES-TABLE

- **Stato:** **CHIUSA** (codice 0.10.29 + post-swap) — classe `Observation` rimossa da `models.py`.
- **Evidenza A4:** dopo primo boot post-swap, `sqlite_master` senza tabella `observations`. Vedi `docs/obs-4b-postop.md`.

## DEBT-ALEMBIC-BASELINE-LEGACY-TABLE

- **Stato:** **CHIUSA in 0.10.30** — migrazione `l2c3d4e5f6a7` `DROP TABLE IF EXISTS observations` (idempotente su produzione già senza tabella). Baseline storica non riscritta.

## DEBT-AUTOVACUUM-NOT-SET

- **Stato:** **ACCETTATO** (OBS-COERENZA 4.1; riformulata OBS-PORTALE 0a.2) — `auto_vacuum=0` resta. Freelist live post-4b ≈ 2 pagine; gli insert riusano freelist → il file tende a stabilizzarsi.
- **Perché non «> 256 MiB × 7g» sul picco:** il primo prune raw pieno (~2026-07-27) predice freelist **0.30–0.37 GiB** (307–379 MiB) **immediatamente** dopo DELETE — sopra 256 MiB senza che il file sia “gonfio residuo”. Quella soglia scattava sul picco post-prune, non sul problema reale.
- **Criterio nuovo (residuo a regime):** dopo un prune, attendere **≥ 48 h di ingest** (riuso freelist). Se allora `freelist_bytes` resta **> 512 MiB** per **≥ 7 giorni** consecutivi **e** `db_bytes` non cala rispetto al pre-prune → programmare VACUUM periodico. Il picco entro 48 h dal prune **non** conta.

## DEBT-CALIB-EPOCH

- **Stato:** **CHIUSA in 0.10.30** — day-clock solo da `settings.calibration_started_at`; assente/invalido → `available=false`, `day=null` (K3). Reset via `scripts/reset_calibration_epoch.py` dopo snapshot+integrity.

## DEBT-TRUST-INVENTORY-OSCILLATION

- **Priorità:** chiuso in 0.10.28 (OBS-TRUST-CONVERGE) — **preesistente**, non regressione 3b-iii
- **Evidenza storica:** structural=53 già su 0.10.25 e 0.10.26; stesso insieme deterministico su 0.10.27 boot1/boot2. Il gate «boot2 ≪ boot1» era mal specificato (mai misurato sul codice vecchio).
- **Causa accertata (FASE A):** ping-pong **(a)** — `_apply_trust_plan` allinea i 53 `operational_state`, poi `reconcile_asset_presence` li riscrive (53/53 undid in nested probe). Non (b): apply cambia davvero i valori (`identical_rewrite=0`).
- **Premio (A.4):** con structural=0 → needs_apply=false → backup saltato → `T_total ≈ 15 s` (da 174 con T_backup=155).
- **Fix:** gerarchia esplicita in `inventory_may_set_operational_state` — inventory cede a trust_quarantine / trust_protected. Vedi `docs/obs-trust-converge.md`.

## DEBT-BACKUP-ASYMMETRY

- **Stato:** **CHIUSA in diagnosi** (2026-07-25, §13 / OBS-TRUST-CONVERGE) — nessuna modifica a `deploy.sh`/`backup.py`
- **Due copie/deploy:** confermate (pre-deploy + trust se needs_apply).
- **Throughput:** serie trust 10.37 → 9.22 → 9.15 → 18.38 → 17.3 → **13.88** MB/s (post-4b, file ~1.85 GiB, T_backup=133.2 s su boot structural).
- **Causa del dimezzamento post-3b-iii:** minore pressione di scrittura su `observations` durante `Connection.backup()` (dual-write off) — A.5 confermata; non page-cache.
- **Premio aggiuntivo 0.10.28:** con structural=0 il backup trust è saltato (T_backup=0, T_total≈9 s).
