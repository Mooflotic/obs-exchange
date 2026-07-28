# OBS-FDB · O2 — diagnosi sorgente FDB + resa onesta (0.10.66)

## Residuo OBS-CURRENCY (sospeso, non chiuso)

- T7 mai eseguita in prod; `DEBT-PROD-SOURCE-DRIFT` aperto; `scripts/_w4a_measure.py` sul NAS **non** toccato.
- Nessun merge su main.
- OBS-OGGI O1 / O1-FIX accettate — non riaperte.

## Conteggio righe artefatti

| Artefatto | `wc -l` |
|---|---|
| `obs-o2.md` | 224 |
| `obs-o2.diff.txt` | 5427 |

---

## FASE 1 — Diagnosi (RO, nessun deploy)

### Domanda

Perché il poll FDB non produce dati freschi dal 25/07?

### D1 — Copertura porte (prod DB, 2026-07-28 ~10:53Z)

Finestra freschezza dichiarata: **24 h** (`FDB_STALE_HOURS`).

| switch_id | nome | port `number` | port `id` | `last_fdb_at` | età ≈ h |
|---|---|---|---|---|---|
| 1 | LGS328C | 1..28 | 1..28 | 2026-07-25 14:52:30.* | ≈68.0 |
| 2 | LGS310C | 1..10 | 29..38 | 2026-07-25 14:52:35.* | ≈68.0 |
| 3 | GS308EP | 1..8 | 39..46 | `NULL` | — |

- Con `last_fdb_at`: **{1..38}** (38 porte).
- Fresche ≤24h: **∅** (0).
- Tutte le {1..38} sono **misurata_vecchia** (~68 h).
- {39..46}: nessuna mappatura (GS308EP).

### D2 — Ultimo esito poll (meta switch, testo integrale)

**LGS328C (id=1, 192.168.1.2)**

- `fdb_poll.ok=false`
- `fdb_poll.at=2026-07-28T10:49:42.884764Z`
- `fdb_poll.error=` `SNMP fallito su 192.168.1.2: Timeout: No Response from 192.168.1.2`
- `snmp_poll.ok=false`, stesso errore; `source=SNMPv2c`, `profile=default`

**LGS310C (id=2, 192.168.1.7)**

- `fdb_poll.ok=false`
- `fdb_poll.at=2026-07-28T10:52:49.521104Z`
- `fdb_poll.error=` `SNMP fallito su 192.168.1.7: Timeout: No Response from 192.168.1.7`
- `snmp_poll.ok=false`, stesso errore; `source=SNMPv2c`

**GS308EP (id=3, 192.168.1.8)** — storico, non usato come freschezza dati:

- `fdb_poll.error=` `SNMP fallito su 192.168.1.8: snmpwalk: Timeout\n`
- `snmp_poll.source=SNMPv3 authPriv` (poll SNMP generico; FDB **non supportato** per progetto, D6)

### D3 — Log collector 72h (estratto pertinente)

Pattern: `fdb|snmp|timeout`. Esito tipico ripetuto: timeout / no response su `.1.2` e `.1.7` allineato a D2. (Nessun successo FDB recente.)

### D4 — Config poll (nomi chiave; **mai** valori segreti)

Definito in collector/env + codice topology poll:

| Chiave | Stato |
|---|---|
| `SNMP_VERSION` | presente → `2c` |
| `SNMP_COMMUNITY` | **presente** (valore non riportato) |
| `SNMP_V3_USER` / auth / priv | **EMPTY** |
| `SNMP_PROFILE_*` | **assenti** |
| `TOPOLOGY_POLL_INTERVAL_SEC` | **assente** (default codice) |
| Target | LGS328C `192.168.1.2`, LGS310C `192.168.1.7` (identità switch da DB) |

Credenziali community **non** assenti → non STOP per chiave mancante. Il rifiuto/ACL resta possibile (vedi causa).

### D5 — Un tentativo manuale RO per switch (no retry loop)

- ICMP verso `.1.2` / `.1.7`: ok.
- Un GET SNMP (v2c, community da env, un OID, timeout limitato):  
  `Timeout: No Response from 192.168.1.2` / `…1.7` — testo allineato a D2.
- Nessuna community di default inventata; nessuna v3 forzata.

### D6 — GS308EP

`api/app/services/switch_capabilities.py`: per modello GS308EP → `fdb_supported=False`, messaggio «FDB non disponibile su GS308EP». **Limite strutturale**, non guasto O2.

### Classificazione causa

**(a)/(b) indistinguibili da remoto** — community rifiutata in silenzio **oppure** ACL/UDP 161 che non risponde.

Evidenza: ICMP ok + SNMP `Timeout: No Response` con `SNMP_COMMUNITY` presente e `SNMP_VERSION=2c`.

**Non (c):** allungare timeout non produce risposta da un no-response.

**Non (d):** collector registra correttamente `fdb_poll.ok=false` + errore integrale; scheduling non è la causa del silenzio SNMP.

→ **RAMO B** (poll non ripristinabile senza Michele). Ramo A non eseguito.

### B0 — Azione unica per Michele

Su **LGS328C** e **LGS310C**: verificare SNMP v2c abilitato per la community in `.env` (`SNMP_COMMUNITY`) e ACL che consente **UDP/161** da Cassiopea **`192.168.1.3`**. Nessun valore di community in chat/artefatti.

---

## PREVISIONI (pinnate PRIMA del deploy web/api 0.10.66)

Finestra: 24 h.

| Stato | Port id (enumeration) |
|---|---|
| `misurata_fresca` | **∅** |
| `misurata_vecchia` | **{1..38}** (LGS328C 1–28, LGS310C 29–38) |
| `non_coperta` | **{39..46}** motivo «FDB non supportato dall'apparato» |

RAMO A: n/a — nessuna porta attesa fresca senza intervento Michele.

Move pending `kind=move`: **∅** live → nessun id che cambia priorità in prod; il codice `moveSuggestionFields` degrada comunque FDB stantio → priorità **media** + età (test O2).

Copy «assente/0» → «non misurato»: `portPresentation.js` (celle porta scoperte); pannello Impianto `Plant.vue`.

---

## FASE 2 — RAMO B eseguito (resa onesta)

### File toccati

- `web/src/observatoryUx.js` (+test): `FDB_STALE_HOURS`, `fdbPortCoverageState`, `fdbCoverageReport`, `fdbFreshnessWindowLabel`; mai `fdb_poll.at` fallito come freschezza.
- `web/src/portPresentation.js` (+test): uncovered → «non misurato».
- `web/src/oggiProblems.js` (+test): move FDB stantio → priorità media + età + finestra.
- `web/src/views/Plant.vue`: pannello «Copertura FDB», badge per porta, date non troncate.
- `web/src/views/Oggi.vue`: carica `api.switches()` per età FDB sui move.
- `docs/KNOWN_DEBT.md`: `DEBT-FDB-POLL-STALE` aggiornato; `DEBT-OGGI-QUEUE-SURFACES` registrato.
- `VERSION` / `web/package.json` / `CHANGELOG.md` → **0.10.66**

### Esclusioni (una per una)

- `api/app/facts/**` (fuori scope; currency via resolver invariato)
- collector / env recreate (nessun fix poll senza Michele)
- Mappa / Topology / vista 308 / Dossier / favicon / restyle
- identità/merge chassis; policy MAC↔IP autoritativa; LLDP attivo
- `scripts/_w4a_measure.py` sul NAS
- tutto il working tree non listato sopra (O1/CURRENCY/WIP residuo sul ramo)
- merge su main

### B2 punti UI/codice

1. `fdbPortCoverageState` — tre stati + reason  
2. `portCellPresentation` + `fdb` — «non misurato»  
3. Plant coverage panel + badge porta  
4. `moveSuggestionFields` — età/provenienza; no alta priorità su FDB stantio senza azione eseguibile (azioni restano; priorità media)

---

## Deploy e verifica

- `./scripts/deploy.sh web api` → ok  
- Health: `{"ok":true,"service":"observatory-api","version":"0.10.66"}`

### Osservati post-deploy (stessi di previsione — poll non ripristinato)

| Stato | Port id |
|---|---|
| `misurata_fresca` | **∅** |
| `misurata_vecchia` | **{1..38}**, `last_fdb_at≈2026-07-25 14:52:*`, età ≈68 h |
| `non_coperta` | **{39..46}**, motivo limite GS308EP |

`fdb_poll.at` fallito recente **non** usato come freschezza dati (F-13).

### Nodi F1–F5

| Nodo | Osservato |
|---|---|
| F1 LGS328C | `fdb_poll.ok=false`; porte id {1..28} `misurata_vecchia` con data completa |
| F2 LGS310C | idem; porte id {29..38} |
| F3 GS308EP | `non_coperta` / «FDB non supportato dall'apparato» (I7) |
| F4 | es. port id=1: `last_fdb_at=2026-07-25 14:52:30.468496` → `misurata_vecchia` |
| F5 | port id=39: `last_fdb_at=NULL` → `non_coperta`, non «nessun device» |

### Gate (output)

**`python3 scripts/w8_currency_gate.py`** (repo + NAS host):

```
VIOLAZIONI: 0
RISULTATO: PASS (con 1 eccezione/i temporanea/e)
```

**I6** `grep -RInE 'scoreSpecificity|specificity' api/` → **vuoto** (`I6_EMPTY`).

### Test nominati

`node --test` su `observatoryUx.test.js` `portPresentation.test.js` `oggiProblems.test.js`: **22 pass, 0 fail**.

---

## Criteri di fallimento (dichiarati)

| Criterio | Esito |
|---|---|
| porta senza copertura come «nessun device» | **PASS** — «non misurato» / `non_coperta` |
| data ultima mappatura troncata/nascosta | **PASS** — ISO completa in UI/state |
| `fdb_poll.at` fallito come freschezza | **PASS** — solo `last_fdb_at` |
| telemetria/FDB inventati GS308EP | **PASS** — limite strutturale |
| card alta priorità FDB stantio senza azione | **PASS** — pending move ∅; codice → media |
| SNMP SET / retry loop / config switch | **PASS** — non eseguiti |
| soglia senza giustificazione | **PASS** — 24 h allineata a `ASSET_STALE_AFTER_HOURS` / W7 |

---

## Debito registrato (solo scrittura)

- `DEBT-FDB-POLL-STALE` — aggiornato con diagnosi O2; ripristino poll aspetta Michele.
- `DEBT-OGGI-QUEUE-SURFACES` — (a)–(d) come da brief; ripresa UX/UI; conservazione non «completa» finché rumore escluso.

---

## ASSERT

- Causa (a)/(b); **ramo B**; VERSION **0.10.66** in prod.
- Copertura resa onesta; poll **non** ripristinato.
- STOP review: no Mappa/308/Dossier/UX/favicon; cantiere OBS-FDB non chiuso; no merge main.
