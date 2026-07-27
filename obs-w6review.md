# W6-REVIEW — Ripubblicazione + correzione rank ipp/snmp (0.10.57)

Revisione bloccante di W6 (0.10.56). Correzione di codice richiesta solo da W6R.1
(rank) → bump **0.10.57**. Diff integrale: [`obs-w6review.diff.txt`](obs-w6review.diff.txt).
Segreti Fritz mai letti (F-4). Chassis 23/24 non fusi (F-3). Solo "LGS310C" manuale
(F-1); "LGS328C" non marcato (F-2). Ordinamento I5 non alterato senza mandato.

## W6R.0 — Ripubblicazione (URL raw complete, curl 200)

I quattro artefatti erano già presenti nel canale con contenuto identico (nessun commit
nuovo necessario). URL raw **complete** verificate con `curl`:

| Artefatto | HTTP | Bytes | URL RAW |
|---|---|---|---|
| obs-w6.md | **200** | 9081 | `https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-w6.md` |
| obs-w6.diff.txt | **200** | 21739 | `https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-w6.diff.txt` |
| obs-w5bis.md | **200** | 15278 | `https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-w5bis.md` |
| obs-w5bis.diff.txt | **200** | 25972 | `https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-w5bis.diff.txt` |

**W6R.0.2 — completezza del diff W6.** `obs-w6.diff.txt` contiene OGNI file toccato
dall'ondata: `CHANGELOG.md`, `VERSION`, `api/app/facts/registry.py`,
`api/app/services/ai_naming.py`, `api/app/services/fingerprint_facts.py`,
**`api/app/services/identity.py`** (il percorso di scrittura `create_name_proposal`),
`api/app/services/suggest.py`, `docs/KNOWN_DEBT.md`, `scripts/w6_gate.py` (registro rank
esercitato nel gate), `tests/test_dhcp_names.py`, `tests/test_w6_consumers.py`,
`web/package.json`. **Esclusioni dichiarate una per una:** `docs/obs-w6.md` (il report) e
`docs/obs-w6.diff.txt` (l'artefatto stesso).

## W6R.1 — Rank `ipp`/`snmp`: soglia non misurata, riportata al minimo non alterante

**Difetto confermato.** `ipp=88`/`snmp=87` collocavano due sorgenti **sopra `dhcp=85`**,
alterando l'ordinamento dell'invariante di PRODOTTO I5 (`manual > ai > dhcp > fritz > oui`,
F-8) per far passare due test. Stessa classe della soglia inventata rimossa in W1.5-bis
(`mac_count_threshold`).

### W6R.1.1 — Vincolo MISURATO, riga per riga

- **`ipp`:** l'unico test che asserisce `best_guess` con `ipp` è **T-c**
  (`test_ipp_precedence_and_human_category_override`), fixture: proposta `fritz` "HP123"
  (conf 0.9) + enrichment `ipp` "Stampante Studio" (conf 0.96), atteso
  `best_guess[:2]==('Stampante Studio','ipp')`. Vincolo misurato = **`ipp` batte `fritz`
  (rank 80)**. Nessun test impone `ipp > dhcp`.
- **`snmp`:** **NESSUN** test asserisce `snmp` in `best_guess`. T-d
  (`test_snmp_enrichment_creates_proposal_without_overwriting_name`) e
  `test_printer_provider` (`test_r1_...`, `probe_snmp`) asseriscono solo la **creazione e
  il valore** della proposta e che `asset.name` non venga sovrascritto — mai
  l'ordinamento. Vincolo misurato su `snmp` = **nessuno**.
- **Casi reali (prod 0.10.56, read-only):** `PENDING_BY_SOURCE={ai:5, dhcp:2, dns:42,
  fritz:26, oui:3}` → **0 proposte pending `ipp`, 0 `snmp`**. Nessun caso reale impone
  alcun ordine per ipp/snmp.

### W6R.1.2 — Rank minimo non alterante (assegnato)

`ipp=snmp=81`: sopra `fritz`/`mgmt` (80), **sotto `dhcp` (85)** → invariante di prodotto
`dhcp>fritz>oui` intatto. `ipp>80` è il valore **minimo** che T-c richiede; `snmp` senza
vincolo va allo stesso tier (tie risolto da `confidence`: ipp 0.96 > snmp 0.94), senza
inventare un ordine ipp/snmp. **La posizione del tier «management self-declared» rispetto
a `dhcp` non è determinata da alcuna misura: è una decisione di DOMINIO — NON scelta qui
(STOP-5, K8), lasciata a Michele; nel frattempo tenuta sotto `dhcp` (minimo non
alterante).**

### W6R.1.3 — Effetto ri-misurato (per id)

- **FLIPS abbassando ipp/snmp a 81 = 0** (misura read-only su prod 0.10.56, prima del
  deploy). Il fix è **comportamentalmente inerte**: nessun asset cambia best guess.
- Le **3 differenze `i5_reorder` (id 109, 120, 134) RESTANO** — sono `ai` (rank 90, non
  toccato dal fix): id=109 `('Switch Linksys','oui')→('Switch Centrale','ai')`; id=120
  `('Raspberry Pi','oui')→('Allsky Pi','ai')`; id=134 `('iPhoneXdiChris','fritz')→
  ('iPhone di Chris','ai')`. Confermato post-deploy: G6=54 `{status_exclusion:51,
  i5_reorder:3}` invariato.

### W6R.1.4 — T-c/T-d NON modificati

Test invariati; entrambi VERDI con `ipp=snmp=81` (locale, 13 passed nel gruppo printer +
w6_consumers + dhcp_names). Nessuna asserzione riscritta.

## W6R.2 — Tre verifiche

### W6R.2.1 — `adopted_names_changed = 0` (misurato, enumerato)

Confronto dei nomi adottati (`manual_overrides` include `name`) tra **prod 0.10.56**,
**backup pre-deploy W6** (`pre-deploy-20260727-2036.db`) e **nightly pre-W6**
(`observatory-20260727-130350.db`): **30 nomi, id e valori IDENTICI** in tutte e tre le
istantanee. Nessun nome adottato ha cambiato valore. `best_guess` è display/adozione, non
scrive `asset.name`; il deploy non esegue backfill di nomi. **0 → non è uno STOP.**

Id adottati (30): 3, 5, 12, 15, 19, 20, 28, 30, 31, 32, 34, 37, 38, 42, 45, 46, 48, 49,
60, 64, 68, 76, 82, 88, 108, 112, 114, 115, 121, 135.

### W6R.2.2 — Asset rimasti senza best guess (enumerati) + assenza dichiarata (I2)

28 asset con `best_guess` vuoto. Per ciascuno si distingue il nome **presentato** (canon
chassis o `asset.name`, che il display usa quando `best_guess` è vuoto):

- **Mostrano l'assenza (`presented=None`) → UI «Device senza nome» / MAC (I2):**
  **83, 84, 85, 86, 92, 95, 106, 116, 142** (9 asset). Verificato lato frontend:
  `Inventory.vue`/`Dossier.vue` rendono `"Device senza nome"` (classe `unnamed`, corsivo),
  `Topology.vue` cade sul MAC — **mai** vuoto o placeholder spacciato per nome.
- **Mostrano comunque un nome dell'apparato** (`asset.name` o canon chassis, non un best
  guess): 71, 72, 73, 74, 75, 77, 78, 108, 114, 115, 121 (asset.name) e 138, 140, 141,
  143, 144, 145, 146, 148 (canon chassis). Questi non «mostrano vuoto».

Il passaggio a `('','')` per gli id del gate G6 (proposta `rejected` non più sorfata) è la
**scoperta corretta** di W6: chi non ha altra evidenza dichiara l'assenza.

### W6R.2.3 — `create_name_proposal` «sincronizza la relazione»

Diff (W6): `db.add(prop)` → `asset.name_proposals.append(prop)`. **Cosa sincronizza:** il
grafo in-sessione — `best_guess` e i consumatori iterano la collezione
`asset.name_proposals`; con solo `db.add` una proposta creata nella stessa transazione non
era nella collezione già caricata finché non scadeva/ricaricava (root-cause di T-c/T-d).
**Perché necessario:** T-c/T-d creano e poi leggono nella stessa sessione.
**Idempotenza + `was_rejected`:** invariate — la guardia `has_rejected_name_proposal`
(`identity.py:414-417`) precede l'`append` e ritorna `None` se `(asset_id, source, value)`
è già `rejected`; `should_suppress_proposal` (dedup chassis) resta prima dell'append.
`append` è lo stesso oggetto del cascade INSERT: nessun doppio inserimento. La semantica di
dedup è identica a `db.add` — il cambiamento è idempotency-neutral.

## W6R.3 — Copertura dichiarata (K4)

- **W6R.3.1 percorso AI (`propose_name`/batch):** NON esercitato in prod (API Groq a
  pagamento — STOP legittimo). Resta dichiarato **non esercitato dal gate** (K4); coperto
  solo dai test unitari (`test_w6_consumers::test_w663_...`, R-D).
- **W6R.3.2 fingerprint:** il gate G6 esercita **solo** il percorso `best_guess`
  (inferenza di presentazione dai `NameProposal`). NON esercita: la generazione di
  `FingerprintFact` (il filtro di correntezza è preventivo: i fatti a DB non cambiano per
  una modifica di codice), né il backfill hostname→device_class, né la generazione AI.
  «Non esercitato» ≠ «verificato»: quei percorsi hanno copertura nei test unitari
  (`test_w6_consumers` W6.6.1-6.4).

## W6R.4 — Deploy 0.10.57 e gate

Bump `0.10.57` (`VERSION`, `web/package.json`). Deploy `scripts/deploy.sh api` (snapshot
pre-deploy `pre-deploy-20260727-2036.db` + rsync + backup_rotate + rebuild image
`observatory-api`, container ricreato). Solo codice: `api/app/facts/registry.py`.

Assert post-deploy in UNA RIGA (boot1 e regime distinti):

`boot1 0.10.57: structural=0 · needs_apply=false · needs_backup=false · T_backup=0 · T_total=9.411s(obs)`
`regime 0.10.57: wp_gate CONVERGENZA=OK (PIANO1=0→apply→PIANO2 now-ricalc=0→PIANO3=0) · G6=54 {status_exclusion:51,i5_reorder:3} invariato · FLIPS ipp/snmp=0 · IPP_SNMP_WINNERS=[] · needs_apply=false · T_backup=0 · structural=0 · breaker=closed · assets=151 · ip_current=100(mobile) · NP=409(pending=78) · FA=261(cur=68) · AD=68 · unknown_source=0 · observations=absent · I6=vuoto · 109=known/active · 136=known/active · adopted_names_changed=0`

**Delta enumerati per id:** nessuno (0 flip, come previsto).

### GATE W6-REVIEW (tutti VERDI)

1. Artefatti W6 e W5-bis ripubblicati, URL raw complete, **curl 200** — ✓
2. Rank ipp/snmp riportato al minimo non alterante (`ipp=snmp=81`, sotto dhcp; unico
   vincolo misurato `ipp>fritz`; 0 flip) — ✓
3. `adopted_names_changed = 0` misurato ed enumerato (30 identici) — ✓
4. Asset senza best guess enumerati; assenza dichiarata in UI (I2) per i 9 `presented=None` — ✓
5. Gate binari verdi al regime (`needs_apply=false · T_backup=0 · structural=0 ·
   observations assente · breaker=closed`) — ✓

**VERDE. W7 sbloccato.**

**Rollback:** revert del bump + deploy tag `v0.10.56`; kill switch shadow
(`FACT_SHADOW_WRITERS_ENABLED=false`) prima del rollback se il problema fosse nel solo
layer assertion. (Non necessario: gate verdi.)

## Diff

`obs-w6review.diff.txt` — file toccati (integrale): `api/app/facts/registry.py`,
`VERSION`, `web/package.json`, `CHANGELOG.md`, `docs/KNOWN_DEBT.md`,
`scripts/w6review_measure.py` (nuovo), `scripts/adopted_dump.py` (nuovo).
**Esclusi dichiarati:** `docs/obs-w6review.md` (questo report) e `docs/obs-w6review.diff.txt`
(l'artefatto stesso).
