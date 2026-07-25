<!-- BLOCK-ID: OBS-IDENTITY-W15-REVIEW -->
# OBS-IDENTITY-EVIDENCE W1.5 — Fase 1 Review (pre-correzione)
**VERSION tree:** 0.10.42 predisposta NON deployata · **Base W1 chiusa:** 0.10.41

**Rinumerazione confermata:** W1.5 = `0.10.42` (identity-evidence, questa wave · pending deploy), W2 = `0.10.43` (shadow writers ENTITY/Bridge/LLDP, rinviata) — cfr. `CHANGELOG.md:3-5` e `VERSION`.

**Codice ispezionato:**
- `api/app/identity_evidence/{classes,store,linker,presence,__init__}.py`
- `api/app/models.py:197-255` (`IdentityEvidence`, `IdentityLinkProposal`)
- `api/app/alembic/versions/n4e5f6a7b8c9_identity_evidence.py`
- `api/app/bootstrap.py:19` (import per `create_all`)
- `tools/obs_identity_presence_probe.py`
- `tests/test_identity_evidence.py` (6 test, 14 assertion)
- `docs/obs-currency-identity-evidence.md`

---

## Verdetti D1..D18

### D1 — H1 non omogeneo (serial/UUID vs bridge MAC/LACP/LLDP)
**PRESENTE.**
- `classes.py:17` → `H1: 1.0` (peso unico per classe intera).
- `linker.py:37-39` → `weight = EVIDENCE_WEIGHTS.get(row.evidence_class, 0.0)`: nessuna partizione per `evidence_key`/sotto‑tipo.
- Design doc (`docs/obs-currency-identity-evidence.md:66`) mette esplicitamente nella stessa riga «serial ENTITY, UUID, bridge base MAC dichiarato, LLDP chassis ID» → una singola H1 basta per superare `PROPOSE_SCORE_THRESHOLD=0.75` (`classes.py:33`).
- Conseguenza: due membri di uno stack che espongono lo stesso **bridge MAC** (o VC‑MAC) sarebbero fusi come se avessero lo stesso **serial** fisico.

### D2 — LLDP chassis ID senza subtype
**PRESENTE.**
- Schema `IdentityEvidence` (`models.py:214-237`): non c'è colonna `subtype` per il TLV LLDP chassis ID (RFC 802.1AB chassis‑id‑subtype 1..7: chassisComponent, ifAlias, portComponent, macAddress, networkAddress, ifName, local).
- `evidence_key: Mapped[str] = mapped_column(String(128), default="")` (`models.py:218`) è testo libero — nessun vincolo/enum.
- Test convivono con `evidence_key="entity.serial"` (`tests/test_identity_evidence.py:131,139`) senza mai includere una prova LLDP → il subtype non è né rappresentato né richiesto.

### D3 — Tier da solo `fact_type` vs `(fact_type, acquisition_method, source, subtype)`
**PRESENTE.**
- `classes.py:16-22`: `EVIDENCE_WEIGHTS` è indicizzato **esclusivamente** da `evidence_class` (H1..H5).
- `linker.py:27-39` `score_link` usa solo `row.evidence_class` e `row.confidence`; **ignora** `row.source`, `row.authority`, `row.evidence_key`, `row.provenance` ai fini di pesatura.
- Il campo `source` è persistito (`models.py:221`) ma mai letto in fase di scoring; `authority` idem. Nessun modificatore tier per acquisition_method.

### D4 — Bridge MAC dedotto da FDB
**ASSENTE (in questa wave).**
- Non c'è nessun writer/ingest attivo nel pacchetto: `identity_evidence/__init__.py:1-16` espone solo `upsert_evidence`, `refresh_evidence`, `decay_stale_evidence`, `score_and_propose_links`, `classify_mac_presence`.
- Nessun modulo (ENTITY/Bridge/LLDP collectors) chiama `upsert_evidence` con `evidence_class=H1` derivato da FDB — verificato con grep dell'import: solo i test lo usano.
- Design (`docs/obs-currency-identity-evidence.md:92,137`) dichiara shadow writers **spenti** e rinviati a W2 (0.10.43).
- Rischio residuo: schema non blocca l'operazione, ma **oggi il percorso non esiste**.

### D5 — Circolarità
**Verdetti separati (a…d):**

**(a) chassis_id come evidenza di se stesso — PRESENTE (design).**
- Il linker usa come chiavi ref `f"chassis:{ch_a.id}"` / `f"chassis:{ch_b.id}"` (tests: righe 108-109, 254-255) e `subject_hint_type="chassis"` (store.py:36-44).
- Nulla vieta che `value_norm` contenga un `chassis_id` → non c'è guardia contro tautologie tipo `subject=chassis:42, value=chassis-id:42`. Nessuna validazione in `EvidenceUpsert` (`store.py:17-28`) né in `upsert_evidence` (`store.py:47-91`).

**(b) transitività automatica / union‑find — ASSENTE.**
- `score_and_propose_links` (`linker.py:42-85`) itera `candidates` come lista piatta; nessuna chiusura transitiva A‑B∧B‑C ⇒ A‑C.
- `IdentityLinkProposal` (`models.py:240-255`) è una relazione a coppie, senza componenti connesse né tabella di equivalenza.

**(c) evidenza da stato post‑merge — ASSENTE.**
- Il linker non fonde (`linker.py:1` "never mutates chassis_id or Asset.name"); il natural‑key (`store.py:35-44`) è ancorato al `subject_hint_id` pre‑merge → non esiste stato "post‑merge" da riletturare.
- Nessuna re‑classificazione automatica del `subject_hint_id` verso un rappresentante di gruppo.

**(d) euristiche storiche riciclate — ASSENTE (nel pacchetto).**
- `identity_evidence/*.py` non importa nulla da `services/identity.py` (nessun uso di `OUI_HINTS`, `classify_oui`, `VENDOR_HINTS`).
- Il probe `tools/obs_identity_presence_probe.py:19-20` importa solo `presence` e `macutil.normalize_mac`; non riusa scoring legacy.

### D6 — H3 co‑observation senza qualifier (access‑port / MAC‑count / simultaneità)
**PRESENTE.**
- Nessun controllo su ruolo porta (access vs uplink/trunk), n° MAC osservati su ifIndex, o finestra di simultaneità: `classes.py:44-84` guarda solo la presenza di `H3` in `classes_present`.
- Il test `test_h2_h3_pair_can_propose_without_h1` (righe 268-319) usa `evidence_key="port.coobs"` con `value="328c:5"` e confidence=0.95 → punteggio ≈ (0.75 + 0.5)·0.95 = 1.1875 → clampato a 1.0, ben oltre 0.75. Nessuna verifica che la porta non sia uplink (rischio di co‑osservazione su trunk che raggruppa tutto).

### D7 — H2 memoria inventariale vs risposta agente live
**PRESENTE.**
- `classes.py` non differenzia H2 "vivo" da H2 "cache/inventory". Il decay per H2 è `168h` (`DECAY_TTL_HOURS[H2]=168`, `classes.py:27`) → un'inventario SNMP di una settimana fa vale quanto una risposta di 5 minuti fa.
- Nessuna proprietà "liveness" nello schema evidence (`models.py:214-237`): `observed_at`/`last_seen_at` esistono ma non entrano nello score, solo nel decay tutto‑o‑niente.

### D8 — H2∧H3 soglia consente consolidamento o solo proposta?
**ASSENTE (solo proposta).**
- `linker.py:75-82` scrive `IdentityLinkProposal(..., status="proposed")` senza alcuna `status="accepted"` code‑path.
- Nessun writer applica `chassis_id`/`Asset.chassis_id` — verificato dal test `test_linker_never_mutates_chassis_id` (righe 222-265) che passa.
- `apply` è azione umana per design (`docs/obs-currency-identity-evidence.md:88` "Writer umano per accept").

### D9 — Consolidamento automatico su H1
**ASSENTE.**
- Come D8: `linker.py:80` fissa `status="proposed"`; nessun ramo scrive `accepted` o modifica `Asset.chassis_id`.
- Il test `test_h1_agree_proposal_proposed` (righe 118-155) verifica solo che venga creata una **proposta**, mai un merge.

### D10 — Evidenza + decisione fuse in un'unica FSM; decay retrae link confermati
**Fusione FSM: ASSENTE.**
- Due macchine a stati **separate**:
  - Evidence (`models.py:228-230`): `current | stale | superseded | retracted`.
  - Proposal (`models.py:251-253`): `proposed | accepted | rejected | expired`.

**Decay retrae link confermati: ASSENTE ma con debito.**
- `decay_stale_evidence` (`store.py:122-139`) opera solo su `IdentityEvidence.state`, non tocca `IdentityLinkProposal.status`. Nessun percorso porta `accepted → expired` in automatico.
- Debito latente: se in W2/W3 arriveranno "accepted", il decay evidenze **non** ha effetto retroattivo → il proposal accettato resta "accepted" anche a fronte di evidenze tutte stale. Nessun test copre questo scenario.

### D11 — Manca proven_same / proven_different / unresolved (default unresolved)
**PRESENTE.**
- Non esiste ternario semantico. Il modello evidence ha `manual_review: bool` (`models.py:235`) e `contradicts_id` (`models.py:232-234`), ma:
  - Nessun campo `judgement ∈ {proven_same, proven_different, unresolved}`.
  - Il "proven_different" non è rappresentabile: `flag_h1_contradiction` (`store.py:108-119`) alza solo `manual_review=True` sulla **stessa** riga in mutazione; non produce un'evidenza negativa autonoma.
- Il proposal state `rejected` copre l'esito umano ma non la **prova** di diversità (perché non è auto‑generabile).

### D12 — Manca absent_measured / absent_unmeasured
**PRESENTE.**
- `presence.py:9` `PresenceClass = Literal["direct", "fdb_fresh", "historical_only", "absent"]` — **quattro** valori, con `absent` singolo bucket.
- `presence.py:38-64`: nel ramo finale `return "absent"` non si distingue:
  - poll SNMP eseguito e MAC assente (misurazione negativa),
  - poll non eseguito / fallito (nessuna misurazione).
- Il tool `obs_identity_presence_probe.py:64` deriva `poll_ok` euristicamente da `last_fdb_at` recente; `poll_ok=False` produce automaticamente `historical_only` o `absent` senza registrare **perché** manca la misura.

### D13 — MAC localmente amministrati (U/L bit) usati come evidenza
**PRESENTE.**
- Nessun filtro sul bit U/L nella pipeline `identity_evidence`. Ricerca esaustiva: `classes.py`, `store.py`, `linker.py`, `presence.py` non chiamano mai `is_locally_administered` (che invece esiste in `services/identity.py:361-362` ed è usato solo per la classificazione OUI legacy).
- Conseguenza: un MAC LAA (bit 41=1) — tipico di **VM cloni**, **randomizzati Wi‑Fi**, **VRRP/HSRP virtuali** — può essere upsertato come H1 (evidence_key libero) e contribuire al merge con peso 1.0.

### D14 — Predicato adiacenza blocchi MAC
**ASSENTE.**
- Nessuna funzione controlla adiacenza numerica dei MAC (offset ±k). L'unica "vicinanza" è OUI24 in H5 (test `test_h5_only_no_link_proposal:92,101`, `evidence_key="oui24"`, `value="D8:EC:5E"`).
- Il design lo esclude esplicitamente: `docs/obs-currency-identity-evidence.md:53` "Contiguità MAC non usata come prova" e `:119` "Contiguità MAC solo H5". La regola `can_propose_link` blocca H5‑only (`classes.py:73-74`).

### D15 — LAG/stack/VM: LACP system ID come fisico? OUI promuove tier?
**PRESENTE (parziale).**
- **LACP system ID:** nessuna categoria dedicata. Se ingerito come H1 con `evidence_key` arbitrario (es. "lacp.sysid"), viene trattato come identifier fisico con peso 1.0 (`classes.py:17`) — stesso rischio di D1.
- **OUI promuove tier:** ASSENTE. `classes.py` fissa H5=0.1 e `is_corroborating_only(H5)` è True (`classes.py:36-37`); nessun ramo lo eleva a H1/H2. Regola `can_propose_link` scarta H5‑only (`classes.py:73`).
- Verdetto complessivo: PRESENTE per LACP (mancata separazione), ASSENTE per la parte OUI‑promuove‑tier.

### D16 — Irreversibilità: merge fonde righe vs LINK; `member_id` su assertion chassis‑scoped
**PRESENTE.**
- **Nessun member_id.** `IdentityEvidence` (`models.py:214-237`) ha solo `subject_hint_type/subject_hint_id`. Nessuna colonna `member_index` / `stack_slot` che consenta di ancorare un'evidenza al **singolo membro fisico** di uno stack chassis‑scoped.
- **Merge (quando arriverà) fonderà righe, non LINK.** Il modello attuale non ha una tabella "link" persistente separata da IdentityLinkProposal. Se W2/W3 introdurranno l'apply, dovranno decidere se: (i) riscrivere `subject_hint_id` (fusione righe → irreversibile senza soft‑delete) oppure (ii) tenere le righe e materializzare un LINK. Oggi la strada (i) è quella suggerita dallo schema piatto → rischio di irreversibilità implicita.

### D17 — Parity Alembic dichiarata ma non provata vs create_all
**PRESENTE.**
- Migration `n4e5f6a7b8c9_identity_evidence.py:7` dichiara esplicitamente: `"Prod uses create_all; this migration keeps alembic parity only."`
- Bootstrap (`bootstrap.py:85`) esegue `Base.metadata.create_all(bind=engine)`; l'import a riga 19 include `IdentityEvidence, IdentityLinkProposal` per farli creare da `create_all`.
- **Nessun test** confronta lo schema generato da `create_all` con quello prodotto da `alembic upgrade`: né in `tests/test_identity_evidence.py` (che usa `Base.metadata.create_all(engine)` a riga 30), né altrove. Nessun `assert_alembic_matches_metadata` o simile.
- Divergenze potenziali non catturate: indici composti `ix_identity_evidence_natural_key`/`_subject_state`/`_class_state` sono dichiarati sia in `models.py:202-212` sia nella migration (righe 49-63) → ridondanza tipica ma non verificata.

### D18 — Copertura test negativi (assertion‑by‑assertion)

**Enumerazione delle 14 assertion nei 6 test (`tests/test_identity_evidence.py`):**

| # | Test | Riga | Assertion | Cosa prova |
|---|------|------|-----------|-----------|
| 1 | `test_h5_only_no_link_proposal` | 114 | `assert proposals == []` | H5‑only non genera proposta (positivo: non merge) |
| 2 | ” | 115 | `assert not can_propose_link(rows, score=0.2)` | Regola pura: H5‑only rifiutata |
| 3 | `test_h1_agree_proposal_proposed` | 153 | `assert len(proposals) == 1` | H1+H1 concordi → 1 proposta |
| 4 | ” | 154 | `assert proposals[0].status == "proposed"` | Status corretto (mai accepted) |
| 5 | ” | 155 | `assert proposals[0].score >= 0.75` | Soglia raggiunta |
| 6 | `test_h1_contradict_manual_review_no_proposal` | 180 | `assert row.manual_review is True` | Contraddizione H1 alza flag |
| 7 | ” | 203 | `assert proposals == []` | Contraddizione blocca proposta |
| 8 | ” | 204 | `assert not can_propose_link([row, peer], score=0.95)` | Regola pura rifiuta anche con score alto |
| 9 | `test_historical_fdb_presence_class` | 219 | `assert result == "historical_only"` | Stale FDB → historical_only |
| 10 | `test_linker_never_mutates_chassis_id` | 263 | `assert asset_a.chassis_id == before_a` | Nessuna mutazione lato A |
| 11 | ” | 264 | `assert asset_b.chassis_id == before_b` | Nessuna mutazione lato B |
| 12 | ” | 265 | `assert db.scalars(select(IdentityLinkProposal)).all()` | Almeno una proposta esiste comunque |
| 13 | `test_h2_h3_pair_can_propose_without_h1` | 317 | `assert len(proposals) == 1` | H2∧H3 senza H1 → 1 proposta |
| 14 | ” | 318 | `assert proposals[0].status == "proposed"` | Status corretto |

**Casi non‑merge coperti (positivi):**
- H5‑only rifiutato (1, 2)
- H1 contraddizione blocca (6, 7, 8)
- `chassis_id` immutato (10, 11)

**Casi non‑merge / negativi MANCANTI:**
1. **H2 sola** (senza H3) → no proposta — non testato.
2. **H3 sola** (senza H2) → no proposta — non testato.
3. **H4 sola** → no proposta — non testato.
4. **H2+H5 / H3+H5 / H4+H5** (H5 corroborante ma senza asse hard) → non testati.
5. **H1 con score sotto soglia** (confidence bassa forzata) → non testato.
6. **Evidenze `state="stale"`** ignorate dal linker → non testato (nessun test invoca `decay_stale_evidence`).
7. **`decay_stale_evidence` transizione** (age > TTL) → non testato: 0 chiamate al simbolo nei test.
8. **`refresh_evidence`** → non testato: 0 chiamate.
9. **Presenza `direct` / `fdb_fresh` / `absent`** → non testati (solo `historical_only` a riga 219).
10. **Idempotenza upsert**: seconda `upsert_evidence` con stesso natural‑key aggiorna `last_seen_at` senza creare duplicati → non asserito (il test contraddizione mostra la mutazione ma non verifica `id` invariato né conteggio righe).
11. **Ramo `existing` in `score_and_propose_links` (linker.py:68-73)**: seconda esecuzione con stessa coppia deve aggiornare `score`/`evidence_ids` senza duplicare — non testato (`assert len(proposals) == 1` dopo doppia esecuzione).
12. **Chiave naturale con `subject_hint_id=None`** → non testato.
13. **`manual_review` per contraddizione lascia intatte le altre righe** (isolamento) → non testato.
14. **Bit U/L su MAC LAA** (cfr. D13) → non testato.
15. **Contiguità MAC ≠ H5**: nessun test verifica che un H5 con `evidence_key` diverso da OUI24 non sia trattato come H1.

**Verdetto D18: PRESENTE.** La suite dimostra i 3 tratti "safety" chiave (no merge auto, no chassis mutation, H5‑only rifiutato) ma **non** i tratti "robustness" (idempotenza, decay, gate parziali, presenza multi‑classe, guardie U/L). Copertura ~40 % delle regole enunciate in `classes.py` e `store.py`.

---

## Sintesi

| Difetto | Verdetto |
|---|---|
| D1  H1 non omogeneo | **PRESENTE** |
| D2  LLDP subtype | **PRESENTE** |
| D3  Tier da fact_type solo | **PRESENTE** |
| D4  Bridge MAC da FDB | ASSENTE |
| D5a chassis_id come propria evidenza | **PRESENTE** (design) |
| D5b transitività/union‑find | ASSENTE |
| D5c evidenza post‑merge | ASSENTE |
| D5d euristiche storiche riciclate | ASSENTE |
| D6  H3 senza qualifier | **PRESENTE** |
| D7  H2 inventory vs live | **PRESENTE** |
| D8  H2∧H3 consolida | ASSENTE (solo proposta) |
| D9  Consolidamento auto H1 | ASSENTE |
| D10 FSM fusa / decay retrae confermati | ASSENTE (con debito) |
| D11 proven_same/different/unresolved | **PRESENTE** |
| D12 absent_measured/unmeasured | **PRESENTE** |
| D13 MAC LAA come evidenza | **PRESENTE** |
| D14 Adiacenza MAC | ASSENTE |
| D15 LACP fisico / OUI→tier | **PRESENTE** (LACP), ASSENTE (OUI) |
| D16 Irreversibilità / member_id | **PRESENTE** |
| D17 Alembic parity non provata | **PRESENTE** |
| D18 Copertura negativa | **PRESENTE** |

**Totale PRESENTE:** 12 · **ASSENTE:** 8 (+ 1 split D5/D15) · **NON APPLICABILE:** 0.

Nessun deploy. Nessuna modifica di codice apportata in questa fase.
