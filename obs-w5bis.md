# W5-bis — Chiusure prima di W6 (0.10.55)

Gate BLOCCANTE per W6. Migrazione + fix preventivo di correntezza/derivazione, nessuna
seconda gerarchia, nessun secondo autore di `trust_level`/`operational_state` (F-7).
Segreti Fritz mai letti/riportati (F-4). Chassis 23/24 non fusi (F-3). "LGS328C" resta
`unknown_nonempty` (F-2); solo "LGS310C" manuale (F-1).

> **Nota di esecuzione.** Le misure di produzione (W5b.1.1, baseline, boot1/regime,
> gate W5b.6) girano su Cassiopea e sono elencate qui come comandi + **previsioni**;
> vanno eseguite da Michele e i valori OSSERVATI riportati sotto ogni sezione. Il
> codice, gli script e i test sono chiusi e verificati in locale.

---

## W5b.1 — Il mapping livello→stato reso TOTALE

### W5b.1.2 — Verifica del confronto reale (non la ricostruzione)

`_build_trust_plan` (`api/app/services/trust.py`) marca `structural` a:

```519:519:observatory/api/app/services/trust.py
            structural = asset.trust_level != level or current_state != expected_state
```

con `expected_state` calcolato (righe 510-516) come `fritz_historical` / `stale_unlocated`
/ altrimenti **`active`**, e `current_state = (asset.meta or {}).get("operational_state", "active")`
(riga 517). **Il piano confronta `operational_state`.** Quindi il buco è reale: un asset
con livello derivato `known`/`confirmed_present`, `operational_state` ≠ `active` e
`inventory_hidden_auto` falso restava `structural` in perpetuo, perché `_apply_level_meta`
non scriveva `operational_state` in quel ramo. È la stessa forma del difetto dell'asset
109 (W-P.1): lì la divergenza era `trust_level`; qui è il secondo termine del confronto,
`operational_state`, sopravvissuto dietro la condizione `inventory_hidden_auto`.

### W5b.1.1 — Misura PRIMA (read-only) — DA ESEGUIRE

```
sudo docker compose exec -T api python3 - < scripts/w5b_measure.py
```

Enumera gli asset con `inventory_hidden_auto` falso/assente **E** livello derivato in
{known, confirmed_present} **E** `operational_state` ≠ `active`, e fa cross-check con lo
`structural` del piano `dry_run`.

**Previsione: 0.** A 0.10.54 il regime era `structural=0` (obs-w5.md §W5.3): se non
esiste divergenza `operational_state`/livello, la classe W5b.1.1 è vuota. Se la misura
conferma 0 → il fix W5b.1.3 è **PREVENTIVO** (chiude il buco prima che W6 aggiunga altri
scrittori). Se > 0 → enumerare gli id qui e saranno sanati dal boot1 (vedi W5b.4).

**OSSERVATO (0.10.54 prod, read-only):** `W5b.1.1 …: 0` · cross-check `structural (dry_run) = 0 ids=[]` → previsione confermata, fix **preventivo**.

### W5b.1.3 — Fix: mapping totale, scelta dichiarata

`_apply_level_meta` ora copre TUTTI i livelli che riceve (`fritz_historical`,
`stale_unlocated`, `confirmed_present`, `known`): per ogni livello attivo scrive **sempre**
`operational_state="active"`.

- **Scelta dichiarata (esclusione esplicita):** un nascondimento **MANUALE**
  (`inventory_hidden=True`, `inventory_hidden_auto` falso — deciso dall'utente) resta
  rispettato: l'hide non viene revocato. NON diventa `structural` perché il piano
  confronta `operational_state` (portato a `active`), non i flag di hide → nessuna
  oscillazione silenziosa. L'auto-hide (`inventory_hidden_auto=True`) viene invece
  revocato come prima.

### W5b.1.4 — Non si è reso cieco il gate

Il confronto del piano NON è stato allargato, nessun asset è stato escluso dal conteggio,
nessuna soglia toccata. È stato reso **totale il mapping** (l'evidenza→stato), non cieco
il gate. Unico writer del campo confermato (F-7): `_apply_level_meta` / `_write_trust_state`.

### W5b.1.5 — Test comportamentale

`tests/test_wp_presence.py`:
- `test_w5b15_total_mapping_known_without_auto_hide_converges` — livello derivato `known`,
  `inventory_hidden_auto` falso, `operational_state` divergente → apply → **due** build
  consecutivi `structural == []`.
- `test_w5b15_manual_hide_preserved_and_not_structural` — hide manuale: dopo apply
  `operational_state=active`, hide preservato, `structural == []`.

---

## W5b.2 — Il gate di regime dimostra CONVERGENZA, non determinismo

**Difetto:** il vecchio `scripts/wp_gate.py` costruiva due piani `dry_run` sullo stesso
stato con lo **stesso** `now`; un dry-run non applica, quindi i due piani coincidevano per
costruzione — verificava il **determinismo**, non la **convergenza**.

**Riscrittura (opzione a):** piano → **apply** (nella sessione, **mai committato**;
`db.rollback()` finale → il file DB resta invariato) → **ricostruzione** con `now`
**ricalcolato** → `structural == []`; più un terzo build (stabilità). **Snapshot pre-op
OBBLIGATORIO** del file DB in `/data/backups/pre-wpgate-<ts>.db` (W5b.2.1: è una
scrittura, anche se solo in-sessione). `now` ricalcolato a ogni build (W5b.2.3), così una
divergenza dipendente dalla finestra di freschezza 24h può emergere invece di essere
congelata. Esce non-zero se non converge.

**Perché esercita il codice cambiato (K4):** se esistesse un buco di mapping non-totale,
`struct1 > 0` e l'apply NON sanerebbe `operational_state` → `struct2 > 0` → gate RED. Col
fix W5b.1.3 → `struct2 == []`.

**W5b.2.2:** precisazione aggiunta in coda a `obs-wp.md` (storia non riscritta).

---

## W5b.3 — Lista classe-(b) del censimento W4d.1.2, chiusa voce per voce

| # | Voce (W4d.1.2) | Disposizione | Evidenza / ondata |
|---|---|---|---|
| 1 | `trust.py` classify/bucket/actionable | GIÀ CONFORME | `classify_asset` legge la **presenza** del nome come segnale di protezione (`trust.py` ~198-203), non il nome canonico; presenza derivata da evidenza (W-P) |
| 2 | `inventory.py` protection | GIÀ CONFORME | `inventory.py:98` `(asset.name or "").strip()` = segnale di protezione, non display |
| 3 | `suggest.py` / `ai_naming.py` gating | **RINVIATA → W6** | perimetro W6 (inferenze AI + generazione proposte) |
| 4 | `name_proposal_chassis.asset_name_authority` | GIÀ CONFORME | autorità I5 per-membro; `chassis_manual_name`/`chassis_canonical_presentation` usano `current()` resolver (subject=chassis) PRIMA del meta membro (`name_proposal_chassis.py:59-62,125`) |
| 5 | `chassis_rename` enum | GIÀ CONFORME (azione umana, K1 dichiarata) | rename umano esplicito, holder=fact_assertion (W4d.2); non writer automatico |
| 6 | `identity.py` ambiguity/infra | GIÀ CONFORME | risoluzione per mac/ip; fonte contestuale `resolve_asset_by_ip_at` (`identity.py:481`) |
| 7 | `interface_roles` | NON APPLICABILE | alias interfaccia, non nome apparato (classe c) |
| 8 | `fingerprint_facts` match | **RINVIATA → W6** | perimetro W6 (fingerprinting) |
| 9 | `topology` AP heuristics | MIGRATA (label, W4d) + GIÀ CONFORME (euristica) | node label via `presentation_name_for_asset` (`topology.py:565`); fall-through euristico sul nome dichiarato I2 |
| 10 | `port_roles._is_ap_asset` | GIÀ CONFORME | euristica su presenza-nome/categoria (`port_roles.py:432` `_looks_like_ap`), non nome canonico |
| 11 | `detectors` | NON APPLICABILE | mapping ip→asset corrente legittimo (`detectors/__init__.py:63`), non lettura del nome canonico |
| 12 | `wifi_associations` resolve AP | **MIGRATA (W5-bis)** | `resolve_ap_asset` ora `resolve_asset_by_ip_at(ip, observed_at)`; tie→None→fall-through; test `test_w5_consumers` W5b.3 |
| 13 | `chassis_grouping` MemberView/guards | GIÀ CONFORME | presentazione chassis via canon/composeDevices |
| 14 | `composeDevices` singleton/`pickPrimary` (web) | GIÀ CONFORME | consuma `display_name` dell'API (resolver) |
| 15 | `inventorySort.js` | GIÀ CONFORME | ordina su `display_name` (resolver) |
| 16 | `AssetDecide.vue` bind name | NON APPLICABILE | campo di EDIT = colonna grezza per design (input umano) |
| 17 | `_resolve_ap_asset` / `is_current` (topology) | MIGRATA (W5) | `resolve_asset_by_ip_at` (DEBT-TOPO-IP-CONTEXTUAL) |
| 18 | API `_serialize` campo grezzo `name=` | GIÀ CONFORME (dichiarato) | colonna grezza mantenuta; `display_name` via resolver (`assets.py:188-189`) |

**W5b.3.2 — chiusura:** l'unica voce né migrata né conforme nel perimetro di lettura dello
stato corrente era **#12 `wifi_associations` resolve AP** (copia ingest rimasta su
`is_current` dopo che W5 migrò la sola copia di `topology`). **Chiusa in questa ondata**
(equivalenza-preservante: a ingest `observed_at ≈ now`). Le voci #3 e #8 restano RINVIATE
perché ricadono nel perimetro esplicito di W6.

**W5b.3.3 — chiamanti di `presentation_name_for_asset` (nessun `or ""` come surrogato):**

| Chiamante | Gestione del None | Verdetto |
|---|---|---|
| `assets.py:188-189` | `display = presented if presented is not None else guess` | conforme: None → euristica `best_guess`, non `""` |
| `switches.py:151` | `presented or guess or asset.vendor or ""` | conforme: `""` è label terminale di porta, non surrogato di nome canonico |
| `actions.py:96` | `presented or asset.vendor or "Dispositivo"` | conforme: display di ultima istanza |
| `scans.py:252` | `presented or oui_name or asset.vendor or "Dispositivo"` | conforme: display di ultima istanza |
| `topology.py:566` | `presented or (mac or str(id))` | conforme: label nodo di ultima istanza |

Nessun chiamante fa `presentation_name_for_asset(...) or ""`; nessuno scrive stato; il
None non viene mai spacciato per nome canonico. I2 rispettato (`test_w5_consumers`
`test_w541_absent_fact_declares_none` invariato).

**W5b.3.4 — dichiarazione (K4):** il gate G5 di W5 **NON ha esercitato** il path `ap_ip`
(0 associazioni su 62; tutte per `ap_asset_id`/`ap_mac`). La copertura reale della
risoluzione contestuale è nei **test unitari** (`test_w5_consumers`: topology W5.4.6 +
ingest W5b.3). È un fatto, non un difetto.

---

## W5b.4 — Previsioni (PRIMA del deploy)

Baseline di riferimento 0.10.54 (obs-w5.md §W5.3). **Da rimisurare pre-deploy** con:

```
sudo docker compose exec -T api python3 - < scripts/w5b_measure.py   # W5b.1.1 + structural
sudo docker compose stop collector
sudo docker compose exec -T api python3 - < scripts/wp_gate.py       # convergenza
sudo docker compose start collector
```

| Metrica | Previsto (W5-bis) | Origine previsione |
|---|---|---|
| W5b.1.1 (classe buco mapping) | **0** | regime `structural=0` a 0.10.54 ⇒ nessuna divergenza op_state/livello |
| boot1 `structural` (lista per id) | **0** (= W5b.1.1) | nessuno stato memorizzato da sanare; se >0 enumerare gli id qui |
| regime `structural` / `needs_apply` / `T_backup` | **0 / false / 0** | mapping preventivo; ingest = read-migration equivalence-preserving |
| assets | **151** | invariato (nessuna creazione/rimozione) |
| ip_current | mobile (osservazione) | churn elezione multi-IP (W-P.0.1) — non gate |
| name_proposals totale / pending | **409 / mobile** | W5-bis non genera né sopprime proposte |
| fact_assertions | mobile per cambiamento (osservazione) | store cresce per cambiamento |
| AD (finestra 24h) | ~68 (mobile) | finestra mobile — non gate |
| breaker | **closed** | nessun tocco al layer shadow/breaker |
| unknown_source | **0** | invariato |
| observations in sqlite_master | **assente** | invariato |

**Variazioni previste per id:** nessuna (0 attese). Se W5b.1.1 > 0, gli id trovati sono
gli unici attesi al boot1 come `known→active` (op_state), e vanno enumerati DOPO.

### Osservati (0.10.55 prod)

| Metrica | Previsto | Osservato |
|---|---|---|
| W5b.1.1 (pre, 0.10.54) | 0 | **0** ✓ |
| boot1 `structural` / needs_apply / T_backup | 0 / false / 0 | **0 / false / 0** ✓ (T_total=9.234s obs) |
| `wp_gate` convergenza (writer fermi) | OK (0/0/0) | **PIANO1=0 → apply → PIANO2(now ricalc)=0 → PIANO3=0 = OK** ✓ |
| assets | 151 | **151** ✓ |
| ip_current | mobile | 101 (mobile) |
| name_proposals tot/pending | 409 / mobile | **409 / 78** ✓ |
| fact_assertions | mobile | 261 (current=68) |
| AD | ~68 (mobile) | 68 |
| breaker / unknown_source | closed / 0 | **closed / 0** ✓ |
| observations in sqlite_master | assente | **assente** ✓ |
| 109 / 136 | known/active | **known/active · known/active** ✓ |

**Delta enumerati per id:** nessuno (0 variazioni), come previsto.

---

## W5b.5 — Test (solo nodi nominati) — esiti locali

- **Python (176 nodi verdi):** `test_wp_presence` (+ W5b.1.5 nuovi), `test_w5_consumers`
  (+ W5b.3 nuovi), `test_trust_converge`, `test_w4b_chassis`, `test_facts_resolver`,
  `test_facts_shadow_w2`, `test_m1_observation_store`, `test_mac_ip_policy`,
  `test_w4a_chassis_proposals`, identity (`test_identity_evidence`, `test_asset_identity`,
  `test_migrate_identity`, `test_m3_identity_presence`), T-b/T-e/T-f
  (`test_nmap_provider`, `test_ssdp_provider`, `test_topo_ip_contextual`,
  `test_ingest_materialize_equivalence`, `test_wifi_association_ingest`).
- **`test_printer_enrichment` (nodo «printer»):** 5 verdi, **2 ROSSI dichiarati** —
  `test_ipp_precedence_and_human_category_override` (T-c) e
  `test_snmp_enrichment_creates_proposal_without_overwriting_name` (T-d): contratti
  pre-esistenti DEBT-IPP-PRECEDENCE, **perimetro W6.2**, NON addomesticati.
- **JS (39 verdi):** `oggiTriage`, `oggiProblems`, `observatoryUx`, `portPresentation`,
  `topologyLayout`.
- **Gate I6:** `rg 'scoreSpecificity|specificity' api/` → **vuoto** (output mostrato).

Non è dichiarata «suite verde»: eseguiti solo i nodi nominati.

---

## W5b.6 — Deploy e gate — ESEGUITO (VERDE)

Bump **0.10.55** (`VERSION`, `web/package.json`). Deploy via `scripts/deploy.sh api`
(snapshot pre-deploy `data/backups/pre-deploy-*.db` + rsync + backup_rotate + rebuild
image `observatory-api`). `web` rimandato al deploy 0.10.56 di W6 (batch, evita un rebuild
vite ridondante — versione UI allineata a fine W6). Api healthy, `/VERSION`=0.10.55.

Assert post-deploy **in UNA RIGA** (boot1 e regime distinti):

`boot1 0.10.55: structural=0 ids=[] · needs_apply=false · needs_backup=false · T_backup=0 · T_total=9.234s(obs)`
`regime 0.10.55: wp_gate CONVERGENZA=OK (PIANO1=0→apply→PIANO2 now-ricalc=0→PIANO3=0) · structural=0 · needs_apply=false · T_backup=0 · breaker=closed · assets=151 · ip_current=101(mobile) · NP=409(pending=78) · FA=261(cur=68) · AD=68 · unknown_source=0 · observations=absent · I6=vuoto · 109=known/active · 136=known/active`

**GATE W5-bis (tutti VERDI):**
1. mapping livello→stato **totale**, misura W5b.1.1=**0** dichiarata — ✓
2. gate di regime riscritto: **convergenza** dimostrata (apply → rebuild `now` ricalcolato → `structural==[]`), snapshot pre-op `/data/backups/pre-wpgate-20260727-191106.db` — ✓
3. lista classe-(b) chiusa **voce per voce**, nessuna senza disposizione — ✓ (§W5b.3)
4. regime `needs_apply=false · T_backup=0 · structural=0 · breaker=closed` — ✓
5. delta enumerati per id — **0 variazioni** (previsione confermata) — ✓

**Rollback:** revert del bump + deploy tag `v0.10.54`.

---

## Diff

`obs-w5bis.diff.txt` — file toccati (integrale): `api/app/services/trust.py`,
`api/app/services/wifi_associations.py`, `tests/test_wp_presence.py`,
`tests/test_w5_consumers.py`, `scripts/wp_gate.py`, `scripts/w5b_measure.py` (nuovo),
`docs/obs-wp.md`, `VERSION`, `web/package.json`, `CHANGELOG.md`, `docs/KNOWN_DEBT.md`.
**Esclusi dichiarati:** `docs/obs-w5bis.md` (questo report) e `docs/obs-w5bis.diff.txt`
(l'artefatto stesso).
