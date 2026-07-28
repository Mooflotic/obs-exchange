# OBS-308 O6 — GS308EP punto cieco operativo (0.10.69)

## FASE 0 — chiusura O5

### V1 — delta 135→132
Percorso: **supersession `reason=left_port`** (design atteso; non TTL/`stale`). Nessun percorso imprevisto → non STOP.

| port_id | MAC | state attuale | reason |
|--------:|-----|---------------|--------|
| 36 | `44:00:49:72:F4:93` | superseded (FA id 766) | `left_port` |
| 36 | `50:99:5A:6E:EA:37` | superseded (FA id 768) | `left_port` |
| 36 | `70:2C:09:EA:22:3A` | superseded (FA id 777) | `left_port` |

### V2 — copy S-A
Corretto: mai «mai visto». Stringa risultante (template):

- baseline ricostruita: `{MAC} · OUI {oui}[ · randomizzato (LAA)] · non presente alla ricostruzione della baseline del {baseline_at}`
- baseline verificata: `{MAC} · OUI {oui}[ · randomizzato (LAA)] · non presente alla baseline verificata del {baseline_at}`

Al ciclo post-deploy: **0 card S-A** in coda (nessun MAC nuovo fuori baseline) — copy verificata nei test `test_o6_sa_body_no_mai_visto`.

---

## PREVISIONI (prima del deploy)

| voce | previsione |
|------|------------|
| Porta attestazione | `328c` port_id **24** / number **24** · regola FDB MAC `54:07:7D:1E:4F:B9` · non uplink gestito |
| Dietro il 308 | `DC:A6:32:9C:A7:62` · OUI `DC:A6:32` · nome **allsky3** · IP `192.168.2.138` |
| Porte 39..46 | tutte **sconosciuta** (0 assegnata / 0 proposta / 0 vuota_dichiarata / 8 sconosciuta) |
| Card P6 primo ciclo | **0** (MAC dietro già in baseline / non «nuovo») |

---

## OSSERVATI (dopo deploy 0.10.69)

| voce | osservato | scarto |
|------|-----------|--------|
| Attestazione | `determinata` · `328c` · port_id **24** · number **24** · rule `FDB corrente contiene MAC del GS308EP gestito (54:07:7D:1E:4F:B9) · non uplink tra apparati gestiti` | = previsione |
| Dietro | `DC:A6:32:9C:A7:62` · allsky3 · `192.168.2.138` · placement «dietro il 308; porta esatta non determinabile dall'apparato» · source=fdb auth=60 | = previsione |
| Porte id 39..46 | state=`sconosciuta` tutte; `telemetry=null` `fdb=null` (I7) | = previsione |
| Counts | assegnata 0 · proposta 0 · vuota_dichiarata 0 · sconosciuta 8 | = |
| P6 | `[]` | = previsione |
| Proposals | 1 (allsky3, INFERENZA, suggested_port=null, llm off) | atteso |
| Conflicts | 0 | atteso |

---

## Breaker (un ciclo post-deploy)

| metrica | valore |
|---------|--------|
| FA totali | 814 |
| FA `port.fdb_mac` current | 137 |
| FA `port.assigned_mac` current | 0 |
| FA create oggi (UTC date) | 552 |
| DB file | 1805.12 MiB (`/data/db/observatory.db`) |
| breaker_open | **False** |
| ceilings | max_rows 20000 · max_growth_per_day 2000 · max_table_bytes 52428800 |
| stato | **OK — tetti non alzati** |

---

## Gate

```
python3 scripts/w8_currency_gate.py
→ VIOLAZIONI: 0
→ RISULTATO: PASS (con 1 eccezione/i temporanea/e)
→ TEMP: scripts/wp_gate.py DEBT-WPGATE-CURRENCY-COUNT-LOCAL

grep -RInE 'scoreSpecificity|specificity' api/
→ VUOTO (I6)
```

Test locali: `pytest tests/test_o6_gs308.py` → **7 passed**; `node --test web/src/gs308.test.js web/src/plantFdb.test.js` → **6 passed**.

---

## T1–T6

| nodo | esito |
|------|-------|
| T1 attestazione + regola | PASS — 328c:24, regola FDB MAC 308 |
| T2 dietro ≠ assegnato a porta 308 | PASS — placement esplicito; porte senza assigned_mac |
| T3 assign manuale reversibile + I3 | PASS (test) — `port.assigned_mac` source=manual; clear → sconosciuta; doppio assign → conflitto |
| T4 inferenza separata | PASS — blocco INFERENZA, fonte+confidenza, llm off, zero scritture |
| T5 porte 39..46 no telemetria | PASS — fdb/telemetry null; switch fdb_supported=false |
| T6 P6 nuovo MAC (test) | PASS — card «porta ignota», azioni, no «mai visto» |

---

## Criteri di fallimento (uno per uno)

| criterio | esito |
|----------|-------|
| Telemetria/FDB/conteggio inventato sul GS308EP (I7) | **no** — `telemetry=null` `fdb=null` |
| Dietro presentato come assegnato a porta senza manuale | **no** |
| Assegnazione senza conferma | **no** — API richiede `confirm:true` + UI `window.confirm` |
| Manuale sovrascritto da proposta debole | **no** — proposte non scrivono; I3 su divergenza |
| Inferenza senza etichetta/fonte/confidenza o azione autonoma | **no** |
| API a pagamento | **no** — `/ai` off |
| Attestazione da conteggio/soglia | **no** — solo FDB MAC + non-uplink |
| Quattro stati confondibili | **no** — label distinte + data-state |
| Punti ciechi assenti/nascosti | **no** — sezione in vista |
| Card alta priorità senza azione | **no** — P6 con 4 azioni (0 card al ciclo) |
| Pulsante inerte | **no** — assign/empty/clear/dossier cablati |
| FactAssertion fuori da `facts/` / allowlist ampliata | **no** — gate PASS |
| Diff monolitico | **no** — backend + view spezzati |

---

## Superficie

- API: `GET /api/gs308/view`, `POST /api/gs308/assign`
- Vista: `/gs308` (link da Impianto, Dossier, Branch308Card, Oggi P6→assign)
- Fact: `port.assigned_mac` (manual, rank 100) via `facts/gs308.py` + shadow

## Screenshot

- `obs-o6-308-desktop.png`
- `obs-o6-308-tablet.png`
- `obs-o6-308-mobile.png`

## Diff

- `obs-o6-backend.diff.txt` — derivazione dietro-308, assign, S-A V2, test
- `obs-o6-view.diff.txt` — vista 308 + wiring ricerca/nav

**STOP per review.** Non Dossier/rumore/UX/favicon · non merge main · cantiere aperto.
