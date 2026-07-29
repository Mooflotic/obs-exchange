# wc-l=117
# OBS-BEHAVIOUR O11-FIX — 0.10.76

Correzione di otto difetti su O11 accettata. Ramo `feature/obs-currency`. STOP per review; nessun merge su main; FA 251 intatto.

## Elenco file (comportamento)

| Tema | File |
|------|------|
| F8 boot | `api/app/bootstrap.py`, `api/app/services/name_proposal_chassis.py`, `api/app/routers/admin.py`, `docs/KNOWN_DEBT.md`, `tests/test_w4a_chassis_proposals.py` |
| G1–G4 ingest | `collector/collector/adapters/zeek_behavior.py`, `collector/collector/config.py`, `collector/collector/main.py`, `api/app/services/retention.py`, `api/app/routers/ingest.py`, `.env.example`, `tests/test_o11fix.py` |
| G5–G6 assoc | `api/app/facts/ip_association.py` (+ nodi Q3–Q5 in `test_o11fix.py`) |
| G7 priorità | `api/app/services/behaviour.py`, `web/src/oggiPriority.js`, `web/src/views/Oggi.vue`, `web/src/oggiO8.test.js` |
| Meta | `VERSION`, `web/package.json`, `CHANGELOG.md` |

## Previsioni (dichiarate pre-deploy) → Osservati

### F8 — boot undeclared
- **Funzione:** `reconcile_chassis_name_proposal_suppression` — set A (chassis con nome manuale + proposta più debole) e set B (dedup valore per chassis). Chiavi `archived_a`/`archived_b` erano **fuorvianti**: fino a O11-FIX faceva `db.delete` (perdita), non soft-archive.
- **Previsione:** dal deploy 0.10.75 → **0 id** archiviati/cancellati (nessun id da enumerare).
- **Osservato:** soft-archive w4a residui = **[]** (nessun id). Scarto: nessuno.
- **Scelta F8(c):** **rimozione** dal boot (non dichiarazione come voluta). Motivazione: mutazione dati a ogni avvio fuori scopo O11 e assente dall’elenco file.
- **F8(b):** soft-archive + `GET /api/admin/name-proposals/w4a-suppressions` + `POST .../restore-w4a` (lista vuota oggi).
- Debito: `DEBT-UNDECLARED-BOOT-MUTATION`.

### G4 — retention
- **Previsione:** TTL = `obs_ttl_raw_days` = **7** (stesso vocabolario di `observations_raw`). Prima purga: deleted≈0 (tutte le evidenze <7g), after≈285–293.
- **Osservato:** `ttl=7`, before=293, pruned=0, after=293.
- **Proiezione a regime:** coda storica oltre 7g di `last_seen` viene rimossa; restano le evidenze ancora “vive” con `first_seen`/`observation_count` intatti. Nessun VACUUM.

### G5 — certain → uncertain
- **Previsione:** flip **0** (i `certain` live hanno `valid_from` non nullo e `valid_from_truncated=0`).
- **Osservato:** `G5_FLIP_IDS []` — nessun evidence id. Scarto: nessuno.
- Nota: colonna `valid_from` è NOT NULL in schema; il ramo `None` è coperto in test via iniezione in-memory (I2).

### G6 — `70:50:AF:FC:0A:F8`
- **Previsione:** **NO misattribuzione di scrittura** — log ed evidenze su **`…:F9`**; la card O11 mostrava F8 perché primo MAC del chassis 28 (display).
- **Osservato:**
  - Evidenze `src_mac=…:F8`: **nessuna** (id []).
  - Evidenze `src_mac=…:F9`: id **88, 89, 202, 203, 204**.
  - Chassis 28 membri: asset 10=`…:F8`, 11=`…:F9`, 138=LAA `72:28:57:FE:0A:F9`.
  - Riga log originale (`dhcp.2026-07-29-02-00-00.log`):
    `{"ts":1785284974.587034,"uids":["Czpno03TNAZlDCPalb"],...,"mac":"70:50:af:fc:0a:f9","host_name":"SkyBooster2",...}`
  - Post-fix member B-I chassis 28: mac **`70:50:AF:FC:0A:F9`** (evidenza, non primo iface).

### G7 — Oggi
- **Previsione:** 1 voce B-I raggruppata, priorità `ignoto_con_evidenze_zeek` (P6), azioni evidenze+nome (non solo ack); B-C invariato se presente.
- **Osservato:** 1 card `beh:id:group`, kind=`behavior_unknown_with_evidence_group`, count=**7**, `defense_priority_id=ignoto_con_evidenze_zeek`, actions=`open_evidences`,`assign_name`,`acknowledge`. Members: chassis 28,30,15,20,16,19,17.

## G1–G3 / Q1–Q7

| Nodo | Esito |
|------|--------|
| Q1 | `ZEEK_BEHAVIOR_ENABLED=false` → `enabled False`, JOBS `[]`, BEFORE=AFTER=293 in 35s; poi restore `true` + recreate |
| Q2 | test rotazione inode: rotations≥1, hostname h2 ingerito |
| Q3–Q4 | `uncertain` + reason inizio/troncato |
| Q5 | collisione → `uncertain`, id ASC display |
| Q6 | old_fp rimosso; new_fp `first_seen`/`observation_count` preservati |
| Q7 | gruppo + P6 ≠ P1; stessa id su member/group; test superfici JS |

**G2 scelta:** cold-start = **lettura intero file corrente** (offset 0), non EOF. Docstring allineata al codice (la dichiarazione EOF era falsa).

**G3:** `file_ids` device:inode; rotazione contata in `stats.rotations`.

## Deploy / prova asset

- VERSION **0.10.76** (`/api/health` ok).
- JS servito: `index-BWh4iIM_.js` sha256 `f2c4608d04005ef665c8d326fb7d8176005d6d290e06a864b44c1a6bb7c769bd`
- Marker bundle: `ignoto_con_evidenze_zeek` True; `behavior_unknown_with_evidence_group` True.
- Collector: `up -d --force-recreate --no-deps collector` dopo env.

## Breaker

- `zeek_behavior_evidence`: rows_total=293, rows_today=285, approx_bytes=55531, breaker_open=False (tetti invariati 20k/2k/50MiB).
- `fact_assertions`: 948 righe.
- **Controllo negativo (test):** breaker forzato open → `skipped_breaker`, conteggio invariato.

## Gate

```
VIOLAZIONI: 0
RISULTATO: PASS (con 1 eccezione/i temporanea/e)
```

I6 `grep -RInE 'scoreSpecificity|specificity' api/` → **vuoto**.

## FA 251

Invariato: id=251, subject chassis 24, `asset.name`=`LGS310C`, source=manual, authority=100, state=current.

## Screenshot

Harness viewport + dsf=1 (mai `browser_take_screenshot`):

| File | WxH | pair |
|------|-----|------|
| `obs-o11fix-oggi-1280.png` | 1280×900 | PASS vs 768 |
| `obs-o11fix-oggi-768.png` | 768×900 | PASS vs 390 |
| `obs-o11fix-oggi-390.png` | 390×900 | |

## Criteri di fallimento (check)

- scrittore senza interruttore → **no** (G1/Q1)
- docstring sicurezza falsa → **no** (G2)
- perdita/rotazione non contata → **no** (G3/Q2)
- tabella senza retention → **no** (G4)
- certain su valid_from nullo/troncato → **no** (G5)
- MAC arbitrario → **no** (G6)
- F8 chiuso senza riga log → **no** (log dhcp citata)
- P1 solo-ack → **no** (G7 azioni utili)
- priorità diverse stessa condizione → **no** (Q7)
- modifica fuori elenco file → **no**
- proposte senza ripesca → **no** (API list/restore; lista vuota)
- FA 251 / I6 / currency / DB maint / `_w4a_measure` / T7 → **no**

## STOP

Cantiere aperto. Review diff tematici. FA 251 in attesa decisione esclusiva di Michele.
