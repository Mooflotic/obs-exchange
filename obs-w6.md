# W6 — Fingerprinting, inferenze AI, generazione proposte alla correntezza (0.10.56)

Gate FASE 1 (W5-bis) verde su tutti e cinque i punti → W6 avviata autonomamente.
Deploy `0.10.56` su Cassiopea via `scripts/deploy.sh api web`. Diff integrale:
[`obs-w6.diff.txt`](obs-w6.diff.txt).

## W6.0 Perimetro

Consumatori resi conformi alla correntezza: **fingerprinting** (`fingerprint_facts`
backfill hostname→device_class), **inferenze AI** (`ai_naming` payload), **generazione
NameProposal** (best_guess / create_name_proposal). Fuori perimetro (dichiarato): presence,
scans, conflitti, wire `mac_ip_policy` (W7); backfill (W3); trust layer (chiuso in W-P).

## W6.1 — stale/superseded non entrano; storia leggibile (escludere ≠ cancellare)

### W6.1.1 misura PRIMA (read-only prod 0.10.55)

Due tipi di «fatto non corrente»:

- **`fact_assertions` in stato `superseded`/`historical`** (osservato: superseded=4,
  historical=189). I tre percorsi **non li leggono**: `chassis_manual_name` /
  `chassis_canonical_presentation` usano `resolver.current` (solo `current`), il resto
  legge `observations_raw` / `meta`. **0 consumati** → per questo lato il fix è preventivo.
- **`NameProposal` non-attive** (`rejected`/`superseded`/`archived`). Osservato:
  `rejected=284 · archived=20 · superseded=27 · pending=78` (tot 409). `best_guess`,
  `_hostnames` (AI) e il loop hostname del backfill iteravano `asset.name_proposals`
  **senza filtro di stato** → consumavano anche le rifiutate. **Misura: 51 asset**
  ricevevano come «best guess» una proposta NON pending (una che l'utente aveva
  **rifiutato** o che era stata soppiantata). NON preventivo: difetto reale.

### Fix

I tre consumatori leggono ora **solo `status == "pending"`**; `rejected/superseded/
archived` restano a DB (storia leggibile) ma non alimentano inferenza/AI/fingerprint.
Nessuna reimplementazione della correntezza: si usa il campo di stato esistente.

## W6.2 — DEBT-IPP-PRECEDENCE (T-c/T-d): gerarchia UNICA I5

### W6.2.1 diagnosi (file:riga)

- La precedenza è decisa da `best_guess` (`api/app/services/suggest.py`), che ordinava per
  `SOURCE_WEIGHT[source] * confidence` — un **secondo prospetto di pesi** (suggest.py, dict
  `SOURCE_WEIGHT`) **non coincidente con I5** (`AUTHORITY_RANK`, `api/app/facts/registry.py`).
- Root-cause immediato di T-c/T-d: `create_name_proposal` (`api/app/services/identity.py`)
  faceva `db.add(prop)` **senza** sincronizzare la relazione `asset.name_proposals`. Le
  proposte create (ipp, snmp) NON erano visibili in-sessione → `best_guess` vedeva solo la
  vecchia collezione in cache (per T-c: solo `fritz` → `('HP123','fritz')`; per T-d: lista
  vuota).

### W6.2.2 correzione con I5 esistente

- `create_name_proposal` → `asset.name_proposals.append(prop)` (grafo in-sessione coerente).
- `best_guess` rimuove `SOURCE_WEIGHT` e ordina per `authority_for` (I5) primario +
  `confidence` a parità. Unica gerarchia.
- `ipp`/`snmp` dichiarati esplicitamente in `AUTHORITY_RANK`: **ipp=88, snmp=87** (identità
  auto-dichiarata dal device via management — IPP printer-name, SNMP make-and-model/sysName —
  sotto l'AI curata `90` e sopra i nomi assegnati dalla rete `dhcp=85`/`fritz=80`). Non
  tradotto, non approssimato.

### W6.2.3/6.2.4 test come contratti

T-c → `best_guess(asset)[:2] == ('Stampante Studio','ipp')` ✓ ; T-d → proposta
`[('snmp','HP LaserJet M404dn')]`, `category='stampante'`, `name` invariato ✓. Test **non**
indeboliti. Correzione isolabile in questa ondata → nessun debito residuo (DEBT-IPP-PRECEDENCE
CHIUSO).

`test_dhcp_names::test_apply_hints_and_best_guess_priority` (fuori dai nodi nominati ma da non
rompere): l'asserzione meta sul costante rimosso `SOURCE_WEIGHT["dhcp"] > SOURCE_WEIGHT["oui"]`
è riallineata alla gerarchia unica → `authority_for("dhcp") > authority_for("oui")`; le
asserzioni comportamentali (`source=="dhcp"`, valore) restano invariate.

## W6.3 — soppressione alla generazione (già conforme) + I6

`should_suppress_proposal` (`name_proposal_chassis.py`) sopprime **alla generazione** per
**provenienza + soggetto**: chassis con nome manuale blocca sorgenti più deboli
(`authority_for < manual`); dedup `(chassis, value)` su pending. **Mai** per specificità del
nome. Gate I6 `rg 'scoreSpecificity|specificity' api/` → **vuoto**.

## W6.4 — R-D (AI marcata, non supersede manual)

`_upsert_ai_proposal` crea la proposta `source=ai`, `status=pending`, non tocca `asset.name`
né alcun valore manual; `ai` non entra come sorgente hostname fattuale nel payload LLM
(`_hostnames`). Coperto da `test_w6_consumers::test_w663_...`.

**Nota AI/costi:** la generazione AI (`propose_name` / batch) consuma un'API a pagamento
(Groq). Resa conforme e testata, ma **NON eseguita** in prod (criterio di STOP del prompt).

## W6.4 — Gate di equivalenza G6 (a writer fermi, `now` ricalcolato)

`scripts/w6_gate.py`: reimplementa INLINE il `best_guess` PRE-W6 (secondo prospetto,
tutti gli stati) e lo confronta per id col `best_guess` DEPLOYED. Collector fermo.

- **Baseline pre-deploy (0.10.55):** `diff=0` → l'inline-old è fedele al comportamento
  corrente (validazione della baseline a writer fermi).
- **Post-deploy (0.10.56):** **54 differenze**, `by_cause={status_exclusion:51, i5_reorder:3}`.

Classificazione (ogni differenza è **(a) difetto atteso corretto**; zero (b), zero (c)):

- **51 `status_exclusion` (a):** il vecchio `best_guess` sorfava una proposta `rejected`/
  `archived`; il nuovo la esclude e ripiega su OUI-vendor / prossima pending / assenza (I2).
  Es. id=71 `('Broadlink…','fritz' rejected)`→`('','')`; id=2 `('Switch','fritz' rejected)`→
  `('Switch Linksys','oui')`; id=20 `('HP LaserJet 200…','snmp' rejected)`→`('Stampante HP','oui')`.
- **3 `i5_reorder` (a):** proposta `ai` **pending** ora batte `oui`/`fritz` per I5 (ai=90):
  - id=109 `('Switch Linksys','oui')` → `('Switch Centrale','ai')`
  - id=120 `('Raspberry Pi','oui')` → `('Allsky Pi','ai')`
  - id=134 `('iPhoneXdiChris','fritz')` → `('iPhone di Chris','ai')`

Fingerprint e AI-generation **NON esercitati** in prod (K4): il fix è un filtro di
correntezza (i `FingerprintFact` a DB non cambiano per una modifica di codice) e l'AI è a
pagamento — copertura nei test unitari (`test_w6_consumers`).

## W6.5 — Previsioni (dichiarate PRIMA) vs osservati

| Metrica | Previsto | Osservato 0.10.56 |
|---|---|---|
| G6 differenze | 54 (51 status + 3 i5), tutte (a) | **54 · {status_exclusion:51, i5_reorder:3}** ✓ |
| G6 regressioni (c) | 0 | **0** ✓ |
| name_proposals tot/pending | 409 / 78 (invariati) | **409 / 78** ✓ |
| fact_assertions | ~261 (cur 68) | 261 (current=68) |
| assets | 151 | **151** ✓ |
| ip_current | ~101 (mobile) | 99 (mobile) |
| AD | ~68 (mobile) | 68 |
| breaker / unknown_source | closed / 0 | **closed / 0** |
| observations in sqlite_master | assente | **assente** ✓ |
| regime needs_apply / T_backup / structural | false / 0 / 0 | **false / 0 / 0** ✓ |

**boot1 (dichiarato prima come possibile «sana stato memorizzato», enumerato dopo):**
`needs_apply=true` per **1 solo `timestamp_refresh`** (`trust v0.4: … structural=0
timestamp_refresh=1`), drift da ~18 min di ingest tra i due deploy — **non strutturale, non
W6**. Il regime (`wp_gate` PIANO1) è `changed=0 · needs_apply=False · structural=0`.

## W6.6 — Test (solo nodi nominati)

Python nominati verdi: `test_wp_presence · test_w5_consumers · test_trust_converge ·
test_w4b_chassis · test_facts_resolver · test_facts_shadow_w2 · test_m1_observation_store ·
test_mac_ip_policy · test_printer_enrichment (T-b/T-c/T-d/T-e/T-f) · test_identity_evidence ·
test_w4a_chassis_proposals · test_w6_consumers · test_dhcp_names` → **129 passed**.
JS: `oggiTriage · oggiProblems · observatoryUx · portPresentation · topologyLayout` →
**39 pass**. Nuovi W6.6.1-6.4 in `test_w6_consumers`. T-c/T-d ora VERDI. Gate I6 vuoto.
Non è stata rieseguita la suite completa; nessuna dichiarazione di «suite verde».

## W6.7 — Deploy e gate

Assert post-deploy in UNA RIGA (boot1 e regime distinti):

`boot1 0.10.56: structural=0 · needs_apply=true(1 timestamp_refresh, ingest, non-W6) · T_backup=0 · T_total=9.476s(obs)`
`regime 0.10.56: wp_gate CONVERGENZA=OK (0/0/0) · G6 diffs=54 tutte(a) {status:51,i5:3} 0 regressioni · needs_apply=false · T_backup=0 · structural=0 · breaker=closed · assets=151 · ip_current=99 · NP=409(pending=78) · FA=261(cur=68) · AD=68 · unknown_source=0 · observations=absent · I6=vuoto · 109=known/active · 136=known/active`

**GATE W6:** (1) currency dei consumatori con misura 51 dichiarata ✓ · (2) I5 gerarchia unica,
T-c/T-d verdi ✓ · (3) soppressione alla generazione + I6 vuoto ✓ · (4) G6 differenze
enumerate per id, 0 regressioni ✓ · (5) delta name_proposals per id = 0 ✓. **VERDE.**

**Rollback:** revert del bump + deploy tag `v0.10.55`; kill switch shadow prima del rollback
se il problema fosse nel solo layer assertion.

STOP: il prompt W7 arriva dopo la review del diff.
