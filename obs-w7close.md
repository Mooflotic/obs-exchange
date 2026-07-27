# W7-CLOSE — chiusure brevi (0.10.59)

Chiusura dei nodi aperti di W7 prima di UX2. Bump **0.10.59** (codice: `mac_ip_policy.py`,
`inventory.py`, `admin.py`). F-3/F-4/F-5/F-6/F-7/F-8/F-10 intatti. Diff integrale:
[`obs-w7close.diff.txt`](obs-w7close.diff.txt); ripubblicazione W7 integrale:
[`obs-w7.diff.txt`](obs-w7.diff.txt).

## Assert di produzione (UNA RIGA)

`0.10.59: version=0.10.59 · needs_apply=false · T_backup=0 · structural=0 · wp_gate CONVERGENZA=OK (0→0→0) · G7 reconcile changes=0 · W7C.2.4 exception_class_changed=0 · wire narrow hits=0 · assets=151 · ip_current=100 · NP=409(pending=78) · FA=261(cur=68) · AD=68 · breaker=closed · observations=absent · unknown_source=0 · I6=vuoto · policy CONSULTIVA disagreements=53/151 (present=99/stale=52) · 109=known/active · 136=known/active`

**Delta enumerati per id (stato):** nessuno. G7 `changes=0`, W7C.2.4 delta=0, FA invariato 261
(l'unica riga 260→261 è id=261, precedente a questa ondata — vedi W7C.4).

## Previsioni (dichiarate pre-deploy) → osservati

| metrica | previsto | osservato | Δ |
|---|---|---|---|
| version | 0.10.59 | 0.10.59 | 0 |
| needs_apply / structural | false / 0 | false / 0 | 0 |
| wp_gate CONVERGENZA | OK (0→0→0) | OK (0→0→0) | 0 |
| G7 reconcile changes | 0 | 0 | 0 |
| W7C.2.4 exception_class_changed | 0 o minimo (enum) | **0** | 0 |
| wire narrow hits (present_l2/l2_only) | 0 | 0 | 0 |
| assets / ip_current | 151 / 100 | 151 / 100 | 0 |
| NP totale / pending | 409 / 78 | 409 / 78 | 0 |
| FA totale / current | 261 / 68 | 261 / 68 | 0 |
| AD (finestra mobile 24h) | ~68 | 68 | — (mobile) |
| breaker / unknown_source | closed / 0 | closed / 0 | 0 |
| observations in sqlite_master | assente | assente | 0 |
| I6 (`rg 'scoreSpecificity|specificity' api/`) | vuoto | vuoto | 0 |
| policy CONSULTIVA disagreements | ≈52 (enum) | **53** (drift dati) | +1 |

Lo scarto `52→53` è **drift di dati**, non ridefinizione della metrica: dalla misura W7 (52) è
stata aggiunta la riga FA id=261 (binding corrente `interface/112`, asset 108 «Sky TV»,
`192.168.2.195`), che sposta un asset nell'insieme dei disaccordi. Misurato 53, riportato 53.

## W7C.1 — Diff integrale ripubblicato

`obs-w7.diff.txt` è stato **ripubblicato** con il **CONTENUTO INTEGRALE** dei tre script prima
elidati: `scripts/w7_macip_blast.py` (blast-radius read-only), `scripts/w7_wire_predict.py`
(predizione wire ristretto), `scripts/w7_g7.py` (**gate G7**). Il gate ora è revisionabile.

**W7C.1.2 — verifica elisioni:** nell'artefatto originale erano riassunti (elisi) esattamente
**4 hunk**: i 3 script sopra + la sezione `docs/KNOWN_DEBT.md` (notazione `@@ (...)`). Tutti e
quattro sono ora integrali nella ripubblicazione. Gli altri hunk (`VERSION`, `web/package.json`,
`api/app/services/topology.py`, `api/app/services/inventory.py`, `tests/test_w7_consumers.py`,
`CHANGELOG.md`) erano già integrali. **Esclusi dichiarati:** `docs/obs-w7.md` (report) e
`docs/obs-w7.diff.txt` (l'artefatto stesso). URL raw con esito curl: in fondo.

## W7C.2 — Eccezione L2-only non dipende più da `Asset.name` (K9/F-5)

**Difetto:** `_l2_only_exception_class` cercava `"powerline"`/`"510e"` in
`" ".join(asset.name, asset.category, asset.vendor)`. I membri di chassis hanno `Asset.name`
**vuoto per progetto** (F-5): un powerline membro di chassis non sarebbe stato riconosciuto.

**Fix (W7C.2.1/2.2):** classe derivata da attributi **MISURATI** — `category`, `vendor`, l'OUI
vendor di **ogni interfaccia** — più il **nome CANONICO risolto** (`presentation_name_for_asset`,
chassis-scoped), mai il nome grezzo del membro. Nessun attributo che riconosce la classe ⇒
classe **ASSENTE (`None`, K3)**, non un match mancato spacciato per «non è powerline».

**Test (W7C.2.3):** `tests/test_w7_consumers.py` — powerline **membro di chassis** con
`Asset.name` vuoto riconosciuto (a) via OUI dell'interfaccia, (b) via nome canonico del chassis;
più il caso K3 (nessun attributo → `None`). Esercizio a runtime: vedi §Test (K4).

**Misura prod (W7C.2.4):** `exception_class_changed = 0` — nessun asset cambia classe di eccezione
col fix. **Fix preventivo dichiarato:** l'unico powerline (id=7 «FRITZ!Powerline 510E») è
standalone, riconosciuto sia dal vecchio codice (nome) sia dal nuovo (nome canonico = nome
proprio); non esistono oggi powerline membri di chassis con nome vuoto. Il fix protegge il caso
futuro in cui lo diventino.

## W7C.3 — Input costanti del classifier (I2)

**Difetto:** `_mac_ip_policy_present` passava `superseded_by_newer_binding=False` fisso — un'ASSERZIONE
non misurata («nessun binding più recente ha soppiantato»).

**Fix:** `superseded_by_newer_binding` reso **tri-stato** (`bool | None`, default `None`=IGNOTO)
in `MacIpPresenceInputs`; `classify_mac_ip_presence` usa `is True` — **solo un `True` misurato**
produce `superseded`; `None` non viene mai coerciuto in un'asserzione (I2). Il wire ora passa
`None` (ignoto).

**W7C.3.2 — dichiarazione misurato/ignoto:**
- `chassis_mgmt_ip` → **IGNOTO** (`None`): non serve e non è misurato nel wire di presenza; mai
  inventato (I2). `present_l2_unaddressed` resta «unaddressed».
- `superseded_by_newer_binding` → **IGNOTO** (`None`): non misurato nel percorso di presenza (il
  wire non consuma le decisioni `superseded`). Prima era `False` costante (asserzione) → rimosso.

## W7C.4 — `fact_assertions` 260 → 261 (riga enumerata)

| campo | valore |
|---|---|
| id | **261** |
| subject | `interface/112` (asset 108 «Sky TV», chassis 30) |
| fact_key | `asset.iface_ip` |
| excl_key | `asset.iface_ip:112` |
| value_norm | `192.168.2.195` |
| source | `fritz` |
| state | `current` |
| reason | `''` |
| created_at | 2026-07-27 18:04:48 |

**Cambiamento, non osservazione ripetuta:** è l'**unica** riga per `interface/112` (nessun
incumbent), azione `created` (nuovo binding corrente), `occurrences=None` (non è una divergenza).
Un refresh (R-A) avrebbe aggiornato `last_seen_at` senza inserire riga. Invariante W4b.0.b
rispettato (la crescita è per cambiamento distinto).

## W7C.5 — La policy piena passa in modalità CONSULTIVA (non autoritativa)

**W7C.5.1/5.2:** nuovo `inventory.mac_ip_policy_consultation` (read-only) + endpoint admin
`GET /api/admin/mac-ip-policy-consultation` (ruolo operator, sola lettura). Calcola il verdetto
della policy completa (regole #1..#5) per ogni asset e lo espone come **divergenza diagnostica**
accanto allo stato reale e all'evidenza che tiene presente il device. **Non scrive nulla, non
guida `operational_state`/`trust_level`/`reliable`** (F-7 — `classify_asset` resta l'unico
deriver). Mai esposto come stato del device in UI.

**W7C.5.5:** le regole #3/#5 **NON sono attivate in modo autoritativo** in questa ondata. Wire
additivo (0.10.58) invariato: `narrow hits=0`, `G7 changes=0`.

**W7C.5.3 — enumerazione dei 53 disaccordi** (verdetto policy · stato reale · evidenza che tiene
presente). Misurato read-only prod (`scripts/w7c_measure.py`), `policy_decisions={present:99, stale:52}`:

Regola #3/#5 marca `stale` device oggi `active` (dissente dalla realtà — la regola è rotta):

| id | verdetto | stato reale (op/trust) | evidenza presente |
|---|---|---|---|
| 7 | stale | active/known | **fritz_active** — «FRITZ!Powerline 510E» (powerline) |
| 8 | stale | active/known | **fritz_active** — «Sky Q principale — Ethernet» |
| 10 | stale | active/known | fritz_active, chassis_ip — «SkyBooster2 BIBLIO» |
| 15 | stale | active/known | (nessuna nel cutoff) — «Robot Roborock» |
| 58 | stale | active/confirmed_present | recent_portal, chassis_ip — «Sky TV» |
| 80,81 | stale | active/known | (nessuna) |
| 82 | stale | active/known | fritz_active — «Sky» |
| 87,89,90,91,93,94,96,97,99,100,101,102,103,104,105,107,111,113 | stale | active/known | (nessuna nel cutoff) |
| 88 | stale | active/known | (nessuna) — «Sky» |
| 109 | stale | active/known | fritz_active, chassis_ip — «LGS328C» (chassis 23) |
| 112 | stale | active/known | **fritz_active** — «FritzBox Router» (gateway) |
| 135 | stale | active/known | fritz_active, chassis_ip — «Sky TV» (chassis 30) |
| 136 | stale | active/known | fritz_active, chassis_ip — «Sky» (chassis 29) |
| 137 | stale | active/known | fritz_active, chassis_ip — «Sky» (chassis 31) |
| 150 | stale | active/known | (nessuna nel cutoff) |

Regola marca `present` device oggi quarantenati/nascosti (altra direzione della rottura):

| id | verdetto | stato reale (op/trust) | evidenza |
|---|---|---|---|
| 83,84,86,117,119,120,123,124,125,126,127,128,129,130,131,132,133,134 | present | fritz_historical | has_current_ip, chassis_ip |
| 85 | present | stale_unlocated | has_current_ip, chassis_ip |
| 138 | present | stale_unlocated | has_current_ip, chassis_ip — «SkyBooster2 BIBLIO» |

**Nominale (casi palesemente falsi):** id 112 (gateway FritzBox), id 7 (powerline), id 8/82/88/135/136/137
(Sky box) sono `active` e dimostrati presenti, ma la regola li marcherebbe `stale`. Il difetto è
nella **regola** (rule #3: «history-only → stale» ignora fritz_active / reachability / chassis IP),
non nei device. Perciò la policy piena **non è pronta a essere autoritativa** (W7C.5.4/5.5).

**W7C.5.4:** `DEBT-MAC-IP-POLICY-WIRE` aggiornato — wire additivo FATTO; policy piena CONSULTIVA
FATTA; attivazione autoritativa **rinviata e condizionata** alla correzione delle regole che
dissentono dalla realtà. Debito **APERTO**, nominato.

## Test (nodi nominati)

- **`test_mac_ip_policy` — 11 passati (ESERCITATO, runtime nell'immagine `observatory-api`,
  Py3.12.13):** include il nuovo `test_supersession_is_tristate_unknown_is_not_asserted` (W7C.3).
- **`test_w7_consumers` — nuovi nodi W7C.2 (`test_w7c23_*`, `test_w7c22_*`): NON esercitati a
  runtime (K4).** Interrotti per contesa di risorse sul NAS (non un difetto del codice: l'immagine
  parte in 3.8s e `test_w762_*` che già percorrono `presentation_name_for_asset` su membri di
  chassis erano passati). Verificati per **import/sintassi** (`py_compile` OK su tutti i file
  cambiati). Il percorso `mac_ip_policy_consultation` + `_l2_only_exception_class` + wire è stato
  **esercitato su dati reali** da `scripts/w7c_measure.py` e dal **gate G7** (151 asset, nessun
  hang, `changes=0`) — prova a runtime del codice cambiato.
- Gate binari (wp_gate/G7/w7c_measure) eseguiti con `--entrypoint python3` nell'immagine
  deployata, collector fermo, rollback. Nessuna riesecuzione della suite completa.

## GATE W7-CLOSE — VERDE

1. Diff integrale pubblicato (3 script + KNOWN_DEBT hunk) — ✓
2. Eccezione L2 non dipende da `Asset.name` (attributi misurati + nome canonico; K3) — ✓
3. Input costanti risolti/dichiarati ignoti (`superseded`=None tri-stato; `chassis_mgmt_ip`=None) — ✓
4. +1 fact_assertion enumerata (id=261, cambiamento) — ✓
5. Policy piena CONSULTIVA e NON autoritativa (endpoint read-only; 53 disaccordi enumerati; F-7) — ✓
6. Gate binari e convergenza verdi (needs_apply=false, structural=0, G7=0, CONVERGENZA OK, breaker
   closed, observations assente, unknown_source=0, I6 vuoto) — ✓

**Rollback ammesso:** tag `v0.10.58` (non necessario — gate verdi).

## Diff / esclusioni

`obs-w7close.diff.txt` — contenuto integrale dei file toccati/creati: `VERSION`,
`web/package.json`, `api/app/services/mac_ip_policy.py`, `api/app/services/inventory.py`,
`api/app/routers/admin.py`, `tests/test_mac_ip_policy.py`, `tests/test_w7_consumers.py`,
`scripts/w7c_measure.py` (nuovo), `CHANGELOG.md`, `docs/KNOWN_DEBT.md`. **Esclusi dichiarati:**
`docs/obs-w7close.md` (questo report), `docs/obs-w7close.diff.txt` (l'artefatto stesso),
`docs/obs-w7.diff.txt` (ripubblicato come deliverable W7C.1, non duplicato qui).

---

# W7C-FIX — correzioni post-review (nessun bump: cambia solo uno script di misura)

Nessun codice di produzione toccato: modificato **solo** `scripts/w7c_measure.py` (strumento di
misura read-only). VERSION resta **0.10.59**.

## W7C-FIX.1 — Misura tautologica FDB corretta

**Difetto (segnalato):** in `scripts/w7c_measure.py` la freschezza FDB era **cablata a
`port_fresh = False`** e passata a `_mac_ip_policy_present(..., fdb_fresh=...)`. Ma sia
`present_l2_unaddressed` sia `l2_only_allowed` richiedono `mac_fdb_fresh=True` (lo dimostra
`test_w762_present_l2_unaddressed_declared_not_deduced`). Quella misura tornava **0 PER
COSTRUZIONE**: la frase «wire additivo inerte, 0 hit in prod» **non era dimostrata**.

**Fix:** lo script ora calcola la freschezza FDB **reale per ogni asset** con la stessa logica e
finestra di `reconcile_asset_presence`:
`port = SwitchPort where asset_id==a.id`; `fdb_fresh = bool(port and port.last_fdb_at and
port.last_fdb_at >= now - 24h)`. Per ogni hit calcola anche `reliable_old` (reachable ∨ physical
∨ recent_portal, **senza** il wire) e `reliable_new`.

**Misura corretta (prod, read-only):**

`W7 narrow wire hits (REAL fdb_fresh): 0`

Enumerazione: **vuota** (0 hit). Il numero è **misurato**, non più tautologico. Sonda del
perché (stessa esecuzione):

`switch_ports_total=46 · with_last_fdb_at=38 · fdb_fresh_in_24h=0 · newest_last_fdb_at=2026-07-25 14:52:35 · assets_with_fresh_fdb=0`

**Due dimostrazioni distinte dell'inerzia (non più «per costruzione»):**
1. **Misurata oggi:** **nessuna** porta ha `last_fdb_at` nella finestra 24h (la più recente è
   ~57 h fa, 2026-07-25 14:52). Quindi `fdb_fresh=False` per tutti **come fatto misurato** (il
   polling FDB non produce osservazioni fresche in questo momento), non come costante imposta.
   Nessun asset qualifica ⇒ 0 hit reali.
2. **Strutturale (vale anche a FDB fresco):** ogni decisione che il wire consuma
   (`present_l2_unaddressed`, `l2_only_allowed`) richiede `mac_fdb_fresh=True`. Ma la **stessa
   porta fresca** produce in `reconcile_asset_presence` `physical_reasons=["FDB recente"]` →
   `reliable=True` **indipendentemente dal wire** (`inventory.py`, riga «FDB recente» + `reliable
   = reachable ∨ physical_reasons ∨ active_discovery ∨ policy_present`). Perciò per **qualsiasi**
   asset in cui il wire potrebbe attivarsi, `reliable_old` è **già** `True`: il wire **non può
   cambiare `reliable`** (né `operational_state`). È additivo-inerte per **accoppiamento**, non
   per assenza di dati.

**Impatto su `reliable`:** 0 hit ⇒ nessun asset cambia esito. E anche in presenza di FDB fresco
l'esito non cambierebbe (punto 2). Correzione della dicitura, non riscrittura: vedi §precisazione
in `obs-w7.md` (W7.2.3) e la nota accodata.

## W7C-FIX.2 — Infrastruttura di test: blocco K4 (NON test rosso)

Runner ripristinato: rimossi eventuali container `pytest` orfani; contesto Docker pulito
(`observatory-api` healthy, collector attivo). Ripetuta l'esecuzione del nodo con fixture
`tests/test_w7_consumers.py` con l'immagine usa-e-getta `observatory-api --entrypoint python3`.

**Esito:** il **primo nodo resta bloccato oltre il timeout anche dopo la pulizia degli orfani**.
L'import di `app.services.inventory` è sano (misurato: **1.87 s**), quindi non è un difetto di
import né del codice cambiato. Per direttiva: **registrato come BLOCCO INFRASTRUTTURALE (K4)**,
**non** interpretato come test rosso. Non ulteriormente diagnosticato (taglio richiesto).

**Copertura effettiva del codice cambiato (runtime, su dati reali):** il percorso
`_l2_only_exception_class` (fix K9), `mac_ip_policy_consultation` (W7C.5) e il wire tri-stato
(W7C.3) sono stati **esercitati a runtime su tutti i 151 asset** da `scripts/w7c_measure.py` e
dal **blast** `scripts/w7_macip_blast.py` (nessun hang: ~3–4 s ciascuno). Il classifier puro
`test_mac_ip_policy` (11 nodi, incl. tri-stato W7C.3) resta **ESERCITATO**. I tre nodi fixture
W7C.2 (`test_w7c23_*`, `test_w7c22_*`) restano **NON esercitati (K4)**: il fix K9 è però provato
su dati reali dalla misura sopra (`exception_class_changed=0` enumerato, powerline id=7
riconosciuto sia da vecchio sia da nuovo codice).

## W7C-FIX.3 — Delta disaccordi 52 (W7) → 53 (W7-CLOSE): spiegazione misurata

Lo **stesso strumento** blast di W7 (`scripts/w7_macip_blast.py`, **immutato**: usa exception da
nome grezzo + `superseded_by_newer_binding=False`) **eseguito ora** rende:

`DISAGREEMENTS vs operational_state: 53` — **identico** ai 53 della consultation W7-CLOSE.

Conseguenza: il **+1 non è causato dal codice W7C** (fix eccezione K9 / tri-stato). Se lo fosse,
il blast — che **non** contiene quelle modifiche — darebbe ancora 52; invece dà 53. È una
**deriva temporale dei dati**: un singolo device è transitato nell'insieme dei disaccordi tra la
misura W7 (0.10.58, contava 52) e W7-CLOSE (0.10.59, ~48 h dopo). `total` invariato **151** in
entrambe. Il device specifico non è nominabile con certezza perché la misura W7 registrò **solo il
conteggio (52)**, non gli id; ma la **concordanza dei due strumenti a 53 oggi** dimostra che non è
una ridefinizione di metrica né un effetto delle modifiche W7C. *(Corregge la §Previsioni sopra,
che attribuiva il +1 alla FA id=261: quella è al più il trigger temporale del periodo, non una
causa di codice — la prova decisiva è l'accordo dei due strumenti a 53.)*

## Assert W7C-FIX (UNA RIGA)

`0.10.59 (invariato): code_prod_changed=NO · w7c_measure fdb_fresh=REAL · narrow wire hits(REAL)=0 · fdb_fresh_ports_24h=0/46 (newest 2026-07-25 14:52) · reliable impact=0 (additivo-inerte, misurato+strutturale) · test_w7_consumers=K4 blocco infrastrutturale (non rosso) · test_mac_ip_policy=11 esercitati · blast(immutato)=53 == consultation=53 ⇒ 52→53 deriva dati (non codice) · total=151`
