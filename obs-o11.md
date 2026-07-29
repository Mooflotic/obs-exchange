# OBS-O11 — dal «chi c'è» al «cosa fa»

**VERSION:** 0.10.75 · ramo `feature/obs-currency` · **STOP per review** · FA 251 intatto  
**Deploy:** api + web + collector · prova asset `assets/index-BC1r8ELR.js` sha256 `d33b485749161650078572804d7c6987b0b49be125a197db6e230f012f921069` · health `0.10.75`

---

## PREVISIONI (dichiarate PRIMA del deploy)

### A1–A4

| Voce | Previsione |
|------|------------|
| A3 sonda | **VIVA** |
| A1 SQLite pre-O11 | nessuna colonna JA4; flow stale dal 2026-07-25 (`FLOW_INGEST_ENABLED=false`) |
| A4 | ssl* disco ~3g; baseline **in costruzione** |
| Motore IA | `ai_enabled=False`, `ai_api_key` assente → degradazione Z6 |

### A2 — 10 MAC solo-L2 × Zeek

| MAC | Atteso |
|-----|--------|
| `DC:15:C8:80:BB:EA` | NO |
| `F0:B0:14:90:87:96` | NO |
| `F0:B0:14:90:87:97` | NO |
| `38:A6:CE:3E:9C:A8` | NO |
| `38:A6:CE:40:A7:76` | NO |
| `70:50:AF:FB:86:F8` | NO |
| `70:50:AF:FC:0A:F8` | NO (hostname DHCP su MAC vicino `…:F9`, non questo) |
| `38:A6:CE:3E:9C:AE` | NO |
| `D4:52:EE:C3:25:16` | NO diretto; post-O11 evidenza via **chassis 30** (B3) |
| `D4:52:EE:C3:25:17` | **SÌ** ja4d+ja4; IP `192.168.2.195` `is_current=0` → parte **incerta** |

### C4 card

| Tipo | P | Attese |
|------|---|--------|
| B-C | P5 | **0** (baseline in costruzione) |
| B-I | P1 | ≥0 |

---

## A — CENSIMENTO (misura 2026-07-29T00:38Z)

### A1
- Disco: `ssl.log` ja4/ja4s (2312 rows, 2242 ja4, age≈0); `dhcp.log`/`ja4d.log` freschi; rotated ssl* dal 2026-07-26.
- SQLite pre: no JA4. Post: `zeek_behavior_evidence`.
- `flow_observations` max 2026-07-25. `observations_raw` TTL 7g senza source zeek.

### A2 (disco, pre-ingest) — enumerato come previsione; solo `D4:52:EE:C3:25:17` con evidenza diretta.

### A3 **VIVA** — zeek Up; ssl/conn aggiornati.

### A4 Profondità intenzionale insufficiente → baseline in costruzione da primo ingest O11.

### A5 Habits/flow esistenti; Dossier «Cosa fa» esteso (non hub nuovo).

### B1 `api/app/facts/ip_association.py` (dichiarato: unico percorso FA per IP↔MAC in O11).

---

## OSSERVATI (post-deploy)

### Ingest
- Job collector `zeek-behavior` indipendente da `zeek_provider_enabled`.
- Primo ciclo current logs: posted 5764 grezzi → **212** righe dedup (incl. baseline + seed Z1).
- Breaker: rows_total=212 / today=204 / ≈40 KiB — **sotto** 20k / 2k / 50 MiB · `breaker_open=false`.

### A2 copertura post-ingest (enumerata)

| MAC | Evidenza in `zeek_behavior_evidence` |
|-----|--------------------------------------|
| `DC:15:C8:80:BB:EA` | no → Z2 |
| `F0:B0:14:90:87:96` | no |
| `F0:B0:14:90:87:97` | no |
| `38:A6:CE:3E:9C:A8` | no |
| `38:A6:CE:40:A7:76` | no |
| `70:50:AF:FB:86:F8` | no |
| `70:50:AF:FC:0A:F8` | sì (dhcp_hostname/ja4/ja4d via inventorio post-ingest) |
| `38:A6:CE:3E:9C:AE` | no |
| `D4:52:EE:C3:25:16` | via chassis 30 (B3) |
| `D4:52:EE:C3:25:17` | sì — 8 FP (ja4d mac_direct + ja4; **1 uncertain**) |

**Scarto A2:** `70:50:AF:FC:0A:F8` aveva previsione NO (solo disco su MAC) ma post-ingest corrente ha evidenza — scarto dovuto a traffico/associazioni live dopo go-live, non a falsificazione.

### Z1–Z6

| Nodo | Esito | Grezzo |
|------|-------|--------|
| Z1 `D4:52:EE:C3:25:17` asset 58 | **PASS** | `evidence_available=true` n=8; fonte zeek-span; età/stato freshness; INFERENZA «nessun motore…»; proposal=null |
| Z2 `DC:15:C8:80:BB:EA` | **PASS** | `nessuna evidenza disponibile (I2)` n=0 |
| Z3 | **PASS** | 1× ja4 `association=uncertain` su 192.168.2.195 |
| Z4 | **PASS (test)** | `tests/test_o11_behaviour.py::test_z4_*` — card B-C con azione dopo `mark_baseline_ready`; P5 |
| Z5 | **PASS** | baseline `in_costruzione` dal `2026-07-29T00:48:52.861742Z`; B-C live **0** |
| Z6 | **PASS** | status «proposta non disponibile: nessun motore di inferenza configurato»; evidenze mostrate |

### C4 card osservate
- B-C: **0** (come previsto)
- B-I: **7** (una per soggetto chassis/asset — B3), priorità `non_riconosciuto_o_solo_l2` = P1  
  Enumerati uid: `beh:id:chassis:28`, `:30`, `:15`, `:20`, `:16`, `:19`, `:17`

### FA 251
`id=251 subject=chassis/24 fact_key=asset.name value=LGS310C source=manual authority=100 state=current` — **invariato**.

### Gate
```
python3 scripts/w8_currency_gate.py
→ VIOLAZIONI: 0 · PASS (con 1 eccezione temporanea)

grep -RInE 'scoreSpecificity|specificity' api/
→ VUOTO (I6)
```

### Prova asset servito
- `GET /` → `assets/index-BC1r8ELR.js`
- sha256 JS: `d33b485749161650078572804d7c6987b0b49be125a197db6e230f012f921069`
- marker `data-o11` presente; `/api/health` version `0.10.75`
- favicon: Opzione A + `--text-2` `#98a2b3` (O11-D)

### Screenshot (harness O9, dsf=1)
| File | W×H |
|------|-----|
| obs-o11-oggi-{1280,768,390}.png | 1280/768/390 ×900 |
| obs-o11-dossier-z1-*.png | idem |
| obs-o11-dossier-z2-*.png | idem |
| `o9_png_assert.py --pair` | PASS |

### D Favicon
Eseguita **dopo** A/B/C verdi: armonizzazione Opzione A con `--text-2` (`#98a2b3` sul mark-alt). Diff: `obs-o11-favicon.diff.txt`.

### Debito registrato
`DEBT-OGGI-MOBILE-DENSITY` in `KNOWN_DEBT.md` (nessun lavoro densità in O11).

---

## Diff tematici
- `obs-o11-evidenze.diff.txt` — correlazione + ingest + test
- `obs-o11-segnali.diff.txt` — cambio carattere / Oggi / priorità
- `obs-o11-inferenza.diff.txt` — blocco INFERENZA + degradazione
- `obs-o11-favicon.diff.txt` — D

---

## Criteri di accettazione (checklist)

- [x] A completo, sonda viva
- [x] evidenze con fonte, età, freschezza vocabolario esistente
- [x] IP↔MAC non corrente → incerta
- [x] INFERENZA IA + evidenze + confidenza N/A + limiti + azione verifica
- [x] nessuna proposta simulata
- [x] card C4 con azione; priorità coerente P1/P5
- [x] deploy provato su asset servito
- [x] gate + breaker verdi; FA 251 invariato

## Criteri di fallimento (dichiarati)

- funzionalità su sensore muto → **non applicabile** (A3 viva)
- output IA senza etichetta/evidenze/limiti/azione → **evitato**
- proposta simulata → **evitato**
- inferenza che scrive fatti → **evitato**
- API a pagamento / `/ai` cablato → **evitato** (`ai_enabled` forzato false nel percorso O11)
- attribuzione senza incertezza → **evitato** (Z3)
- fingerprint vecchio come corrente → freshness `stale` dichiarata
- secondo vocabolario → riuso FDB_STALE_HOURS / FRESHNESS
- soglia inventata cambio carattere → strutturale + gate baseline
- segnale su storia insufficiente → **B-C=0** + data inizio
- N schede multi-NIC → dedupe chassis (B3)
- card alta priorità senza azione → azioni open_dossier/ack
- priorità diverse stesse condizioni → `priorityForBehaviorCard` unico
- nuovo hub → no
- credenziali in chat → no (solo nomi/len)
- FA 251 modificato → no
- favicon con A/B/C rossi → D solo a verde
- scoreSpecificity fuori triageRules → I6 vuoto
- FactAssertion fuori facts / allowlist ampliata → gate PASS; bootstrap import FA riga invariata
- deploy senza prova asset → prova hash JS
- boot/DB/_w4a/T7 → non toccati
- diff monolitico → tematici

---

**STOP per review. Nessun merge su main. FA 251 in attesa di decisione esclusiva di Michele.**
