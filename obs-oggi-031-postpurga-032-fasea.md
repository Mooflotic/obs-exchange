# OBS-031 POST-PURGA + OBS-032 FASE A (+ D5-bis + Sky)

Sola lettura · live Cassiopea · 2026-07-24 ~01:05 UTC+2 · nessun fix/deploy/codice  
Marcatore massa: `rejected_bulk_oggi` · notice utente: **«Archiviate 165»**

---

## A · MISURA POST-PURGA

### M0 — DB con marcatore corretto

| Metrica | Prima (PRE-PURGA) | Dopo |
|---------|------------------:|-----:|
| Pending `status=pending` | **373** | **205** |
| `rejected_bulk_oggi` | 0 | **165** |
| `rejected_from_oggi` (singoli) | 4 | **6** |
| Delta pending | | **−168** (165 bulk + drift altri) |

`rejected_from_oggi` **non** è il marcatore della massa (`assets.py:859` bulk vs `:812` singolo).

### M0b — 163 (pulsante) vs 165 (Archiviate)

| Cosa | Dove | Cosa conta |
|------|------|------------|
| Pulsante | `Oggi.vue:430` `Archivia rumore ({{ noiseIds.length }})` | lunghezza `noiseProposalIds` al render |
| Notice | `formatArchiveNotice` `oggiTriage.js:24–28` | **`res.rejected`** dall’API, non `ids.length` |
| API | `reject_name_proposals_bulk` `assets.py:832–881` | `rejected` = pending effettivamente flippate; espone anche `requested` / `skipped_*` |

Il test `test_reject_bulk_counts` (`tests/test_reject_name_proposal.py:133–156`) **non** asserisce `rejected == len(ids)`: con `[pending, archived, missing]` aspetta `rejected==1`, `skipped_non_pending==1`, `not_found==1`.

Spiegazione 163↔165: in PRE-PURGA il dump API dava già `noiseProposalIds=165` mentre la UI mostrava **163** (drift 2, documentato). Il notice **«Archiviate 165»** coincide con `rejected_bulk_oggi=165` a DB → al click sono stati rifiutati 165 pending; il **163** era etichetta di un render precedente/stale, non il conteggio API.

### M1 — Stato coda (DOM live post-refresh)

| Elemento | Valore |
|----------|--------|
| Intestazione | **`0 adotta · 38 verifica · 2 rumore`** |
| collide | assente (0) |
| chassis | **(21)** |
| manual-upgrade | **(8)** |
| sotto-soglia | **(9)** |
| 21+8+9 | **= 38** verifica ✓ |
| Toggle rumore | **`2 proposte filtrate come rumore`** |
| Pulsante | **`Archivia rumore (5)`** |
| Notice «Archiviate…» | assente (dopo reload) |

**Residuo rumore 2:** non è zoccolo. Griglia=2 asset, massa=**5** id (3 proposte di secondo livello sullo stesso filtro D10). Una **seconda passata** archivia i 5 e svuota il gruppo rumore visibile. Dopo, resta solo il residuo **invisibile** (M2).

### M2 — Residuo invisibile (stima PRE ~29/16 → corretta)

**24** pending rumore nascoste su **13** asset (score≤nome, non in `proposals` API, esclusi chassis/ignorato).

| id | nome | bucket | n nascoste |
|---:|------|--------|----------:|
| 34 | Petkit - Distributore Cibo Gatto | shadow (non in API proposals) | 1 |
| 60 | Nintendo Switch | shadow | 1 |
| 71 | Broadlink-Outlet-T1-79-7b-bc | `fritz_only` + proposals cleared | 2 |
| 72 | Ipad-di-Vale | fritz_only cleared | 2 |
| 74 | LGwebOSTV | fritz_only cleared | 2 |
| 75 | LGwebOSTV | fritz_only cleared | 2 |
| 77 | Mac | fritz_only cleared | 2 |
| 78 | Mac | fritz_only cleared | 2 |
| 79 | MacBookhristian | fritz_only cleared | 3 |
| 88 | Sky | shadow | 1 |
| 114 | Somneo | fritz_only cleared | 2 |
| 115 | Spazio | fritz_only cleared | 2 |
| 121 | garmin-fenix8-51mm-11b8d0080342 | fritz_only cleared | 2 |

Causa invariata: `_serialize` azzera `proposals` su `fritz_only`/`stale`/historical (`assets.py:117–119`) + `split_name_proposals` 1/fonte (`event_maintenance.py:116–145`).

### M3 — S1 post-purga (max-conf vs specificità)

Picker attuale: `topPendingProposal` = **max confidence** (`triageRules.js:191–198`).

| | max-conf | per-specificità |
|--|----------:|----------------:|
| Righe con top diversa | **8** | |
| Adotta consigliati | **0** | **0** |
| Flip adotta conf↔spec | **0** | |

Esempi (5):

| asset | nome | max-conf (rank) | spec (rank) |
|------:|------|-----------------|-------------|
| 2 | LGS328C | Switch dns 0.6 (**2**) | Switch Linksys oui 0.4 (**3**) |
| 11 | SkyBooster2 BIBLIO — mesh | Sky oui 0.85 (**2**) | SkyBooster2 dhcp 0.75 (**3**) |
| 43 | Sky | Sky oui 0.85 (**2**) | MR-Device/… ssdp 0.55 (**3**) |
| 49 | Hub Tapo H100 | TP-Link oui 0.85 (**2**) | H100 dns 0.6 (**3**) |
| 50 | ROCK | PC oui 0.85 (**1**) | ROCK dns 0.6 (**2**) |

**D11:** con adotta=0 su entrambi i picker, **non riapre** un cantiere adotta; resta materiale di **qualità della top** in Verifica (OUI generico batte hostname più specifico). D11 può restare in coda bassa, non bloccante post-purga.

### M4 — DEBT-PROPOSALS-HIDDEN-FROM-API (testo da copiare in KNOWN_DEBT)

- **Priorità:** media (post OBS-031) — blocca D10 “una passata = coda pulita”
- **Cosa:** `GET /api/assets` espone in `proposals` un sottoinsieme delle `NameProposal` pending. DB post-purga 205 pending; rumore nascosto misurato **24**/13 asset; UI rumore massa 5 vs griglia 2.
- **Perché:** (1) `split_name_proposals` → 1 corrente/fonte; (2) `_serialize` sposta tutto in history se `fritz_only`/`stale`/`_is_historical`.
- **Fix previsto:** flag query scoped tipo `all_proposals=1` (solo triage/Oggi), che restituisce le pending grezze **senza** azzerare historical e **senza** cap per-fonte *oppure* con cap esplicito documentato. La specificità resta **solo** in `triageRules.js` — **vietato** duplicare `scoreSpecificity` in Python.
- **Vietato:** far girare D10 server-side con regole di rank; mute presence per “far vedere” le proposte.

---

## B · OBS-032 FASE A — sintetici con MAC incapsulato

### A1 — Pending il cui `value` contiene MAC (regex `AA:BB:…` / `AA-BB-…` / 12 hex)

**27** proposte (alcune multi-fonte sullo stesso valore). Rank attuale = `scoreSpecificity` oggi.

Sintesi azioni: **0** in ADOTTA CONSIGLIATI · 15 verifica · 12 già rumore (rank 1).

Casi critici (rank alto nonostante MAC nel nome):

| id | nome attuale | proposta | rank | fonte | conf | azione |
|---:|--------------|----------|-----:|-------|-----:|--------|
| 14 | Citofono BTicino C3X | `C3X-00-03-50-96-82-2c-45123` | **5** | dns | 0.6 | verifica (top) |
| 37 | Lavastoviglie Gaggenau | `GAGGENAU-DF480162-68A40E40A69A` | **5** | dns | 0.6 | verifica (top) |
| 38 | Piano Induzione Gaggenau | `GAGGENAU-CI292102-68A40E872A7D` | **5** | dns | 0.6 | verifica (top) |
| 121 | garmin-fenix8-51mm-11b8d0080342 | stesso hostname | 5 | dns/fritz | 0.6 | rumore (parità) |

Altri: `PC-…` rank 1 (già rumore o verifica su anonimi).

### A2 — Quante finirebbero in ADOTTA CONSIGLIATI?

**0.** Nessuna proposta MAC-incapsulata è top-conf con conf≥0.75, more-specific, non-manual, non-chassis.  
Rischio reale = **verifica/adotta manuale** su Citofono/Gaggenau (rank 5 oggi), non il gruppo Adotta automatico.

### A3 — Citofono `#14`

| Campo | Valore |
|-------|--------|
| Nome | `Citofono BTicino C3X` |
| `field_sources.name` | **assente** (`{}`) |
| `manual_overrides` | assente → `isManualName` = **false** |
| Provenienza nome | **import legacy** (`mappa`: `00:03:50:96:82:2C` → stesso nome; `runbook.md`; creato col bootstrap `2026-07-17`) |
| Fritz hostname | `C3X-00-03-50-96-82-2c-45123` (discovery, non applicato come `Asset.name`) |
| Pending vive | dns/fritz con hostname MAC; oui `BTicino` già `rejected_bulk_oggi` |

### A4 — Impatto stimato fix (MAC incapsulato → rank 1)

Simulazione client: se `MAC_RE` → rank 1.

| | ora | con fix |
|--|----:|--------:|
| adotta | 0 | **0** |
| rumore massa (noiseIds) | 5 | **5** (+0 netti su massa; 3 top passano a rumore ma restano fuori massa se già in verifica) |
| flipped top (verifica→archivia) | — | **3**: Citofono `#14`, Gaggenau `#37`, `#38` |

Pin dump 030: Citofono era rumore su OUI `BTicino` (già purgato); il rischio 032 è la **proposta dns/fritz hostname** rank 5. Allsky→Raspberry Pi non toccato dal fix MAC.

---

## C · D5-bis — esclusione chassis

### A5 — Pending chassis con score(proposta) ≤ score(nome)

Pending su membri chassis (≥2): **75** (invariato rispetto ricognizione C5).  
Di cui rumore (score≤): **57** — sarebbero in `noiseProposalIds` se D5 non escludesse i chassis.

Prime 20 (una riga/asset):

| id | nome → proposta |
|---:|-----------------|
| 2 | LGS328C → Switch |
| 3 | LGS310C → LGS310C |
| 5 | Cassiopea — NIC 1 → Cassiopea |
| 6 | Cassiopea — NIC 2 → Cassiopea |
| 10 | SkyBooster2 BIBLIO — Ethernet → PC-70-50-AF-FC-0A-F8 |
| 11 | SkyBooster2 BIBLIO — mesh → SkyBooster2 |
| 28 | Kraken → Kraken |
| 30 | Allsky 3 → allsky3 |
| 33 | Echo Salone → Echo Media |
| 35 | Echo Camera Beatrice → Amazon |
| 43 | Sky → PC-192-168-2-101 |
| 49 | Hub Tapo H100 → H100 |
| 50 | ROCK → ROCK |
| 51 | allsky3 → allsky3 |
| 55 | Echo Cucina → amazon-5b5bf3c111c404ae |
| 58 | Sky → PC-192-168-2-195 |
| 61 | Sky → PC-192-168-2-254 |
| 108 | Sky TV → PC 108 |
| 135 | Sky TV → Sky |

### A6 — Adozione e protezione chassis

**Non si può confermare** che l’esclusione “solo in `noiseProposalIds`” basti a proteggere l’adozione.

| Percorso | Check chassis? | Dove |
|----------|----------------|------|
| Massa **archivia** rumore | **Sì** (skip membri) | `noiseProposalIds` `triageRules.js:312–318`; `mass_eligible` `:289` |
| Massa **adotta** | non esiste | — |
| Adotta **singola** UI (anche su riga chassis in Verifica) | **No** hard gate | bottone `adoptRow` su verifica `Oggi.vue:389–395` |
| API `POST …/adopt-name` | **No** | `assets.py:708–771` — nessun `chassis_id` |
| Verdict chassis → non entra nel gruppo Adotta | soft only | `buildTriageRows` `:244–247` (`recommended_action=verifica`) |

Quindi D5 oggi protegge la **purga di massa**, non l’adozione: un click «adotta» su riga chassis chiama l’API senza vincolo.

---

## D · Chassis «Sky»

### A7 — Tre chassis distinti, stessa label

Sì. Tre gruppi `label=Sky`, id diversi:

| chassis id | membri | primary (`pickPrimary`) | confirmations | regola |
|-----------:|--------|-------------------------|---------------|--------|
| **6** | #61 `38:A6:CE:79:D4:FD` (.2.254) + #137 L2 | #61 | **C4** | L2-only peer |
| **21** | #108 U/L `D6:A9:77:61:25:17`, #58 `D4:52:EE:…17/1A`, #135 `D4:52:EE:…16` | **#58** (noto+universale+IP) | **C1+C3+R1** | IP condiviso + FDB + flip-bit0 |
| **22** | #43 `38:A6:CE:3E:9C:AA/AE` (.2.101) + #136 + #149 L2 | #43 | **C4** | L2-only peers |

I tre «mgmt» della tabella C1 erano i bearer IP di **tre chassis omonimi**, non un solo gruppo.

### A8 — `#108` U/L e rotazione MAC

Correzione: **primary live = `#58`**, non `#108`.  
`#108` è `status=nuovo`, solo U/L → `pickPrimary` lo pospone (`inventoryDevices.js:24–52`: named non-nuovo, poi universale, poi IP).

Se il MAC U/L di `#108` ruota:
- l’arco **R1** (`D6:A9…` flip→`D4` + last2 `25:17` ↔ `#58`) **si spezza** (evidenza attuale: flip e last2 matchano);
- `#58`+`#135` restano uniti da **C1** (IP `.2.195`) e **C3** (FDB co-obs);
- `#108` rischia di uscire dal componente / diventare orfano U/L (privacy churn), a meno di nuovo match R1 o IP.

### A9 — `#135` (D4:52:EE) ↔ `#108` (D6:A9:77)

Non R2 (OUI diversi; Sky fuori `SWITCH_OUI_ALLOWLIST`).

Catena in `chassis 21` meta.evidence:
1. **R1** `#108` U/L ↔ `#58` univ (`chassis_grouping.py` R1 / evidence `R1.links`)
2. **C3** FDB porta switch_id=2 port=5 su MAC `D4:52:EE:C3:25:16`+`…17` → asset `#135`+`#58` (`_confirmation_c3` ~422–451)
3. **C1** shared IP `192.168.2.195`

`#135` entra nel gruppo di `#108` per **connettività di componente** (R1+C3+C1), non per OUI diretto.

---

## Numeri chiave

| Voce | N |
|------|--:|
| Pending DB | 205 (−168 da 373) |
| `rejected_bulk_oggi` | 165 |
| UI | 0 / 38 / 2 · Archivia (5) |
| Hidden rumore | 24 / 13 asset |
| S1 flip adotta | 0 (D11 non urgente) |
| MAC→ADOTTA | 0; fix rank1 flip 3 verifica→rumore |
| Chassis pending rumore se no D5 | 57 / 75 |
| Sky omonimi | 3 chassis |

Nessuna proposta di codice oltre il testo DEBT in M4.
