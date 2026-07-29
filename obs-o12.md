# OBS-COVERAGE O12 — nessuna sorgente muore in silenzio

**VERSION:** 0.10.77  
**Ramo:** `feature/obs-currency`  
**Deploy:** api + web (collector invariato — nessuna nuova env obbligatoria)  
**STOP:** review. Non avviare O13. FA 251 intatto.

---

## Elenco file (comportamento)

| Area | File |
|------|------|
| C1–C3 modello | `api/app/services/source_coverage.py` |
| API | `api/app/routers/coverage.py`, `api/app/main.py` |
| Settings cadenze/flag | `api/app/config.py` |
| Test C5 R1–R6 | `tests/test_o12_coverage.py` |
| Oggi / priorità | `web/src/views/Oggi.vue`, `web/src/oggiPriority.js` |
| Impianto | `web/src/views/Plant.vue` |
| Client API | `web/src/api.js` |
| Debiti | `docs/KNOWN_DEBT.md` |
| Versione | `VERSION`, `web/package.json`, `CHANGELOG.md` |

Diff tematici: `obs-o12-copertura.diff.txt`, `obs-o12-oggi.diff.txt`.

---

## PREVISIONI (dichiarate prima del deploy)

| sorgente | stato atteso |
|----------|--------------|
| `fdb_snmp` | `coperta_fresca` |
| `fritz_tr064` | `coperta_fresca` |
| `nmap_discovery` | `coperta_fresca` |
| `arp_icmp` | `coperta_fresca` (alias nmap, `card_eligible=false`) |
| `portal_presence` | `coperta_fresca` |
| `ssdp` | `coperta_fresca` |
| `printer_mdns_ipp` | `coperta_fresca` |
| `zeek_behavior` | `coperta_fresca` |
| `zeek_conn_flow` | `disabilitata` |
| `zeek_intel` | `disabilitata` |
| `zeek_dhcp_names` | `disabilitata` |
| `internet_probe` | `coperta_fresca` o `coperta_vecchia` |
| `asustor_nas_snmp` | `coperta_fresca` o `cieca` se meta assente |
| `gs308ep_structural` | `limite_strutturale` |

- `cieca` attese: nessuna (salvo registro vuoto su nas/internet)
- `disabilitata`: `zeek_conn_flow`, `zeek_intel`, `zeek_dhcp_names`
- `cadenza_non_nota`: nessuna
- Card C4: **0** C-S; **3** C-D
- C6: `FLOW_INGEST_ENABLED` **ABSENT** → default false → `disabilitata`; chiave era True in `.env.bak-0910`, assente da `.env.bak.20260727` (stesso evento SNMP_V3_* empty)

---

## C1 — Censimento enumerato

| nome | job/endpoint | feeds | flag | cadenza (attr → sec effettivi) | ultimo successo / errore |
|------|--------------|-------|------|--------------------------------|--------------------------|
| `fdb_snmp` | topology → `/api/ingest/fdb-switch` | FDB porte, `fdb_poll` | always-on | `topology_poll_interval_sec` → 60 | ok fresco; GS308 escluso (I7) |
| `fritz_tr064` | topology → observations `fritz` | `sensor_runs:fritz` | always-on | topology 60 | SensorRun ok |
| `nmap_discovery` | discovery → `nmap` | SensorRun nmap, portal | always-on | `collector_interval_sec` → 900 | SensorRun ok |
| `arp_icmp` | **stesso job nmap** (non provider separato) | kinds arp\|icmp | always-on | 900 | stesso SensorRun nmap |
| `portal_presence` | `observe_portal` → `asset.portal_*` | portal watermark | always-on | 900 | MAX(`portal_last_seen`) |
| `ssdp` | discovery → `ssdp` | SensorRun ssdp | always-on | 900 | SensorRun ok |
| `printer_mdns_ipp` | discovery → `printer` | SensorRun printer | always-on | 900 | SensorRun ok |
| `zeek_behavior` | `zeek-behavior` → `/api/ingest/zeek-behavior` | `zeek_behavior_evidence` | `zeek_behavior_enabled` | 300 | MAX(`last_seen`); **errori ciclo non in SensorRun** (difetto di registro dichiarato) |
| `zeek_conn_flow` | `zeek-conn` → `/api/ingest/flows` | `flow_observations` | `flow_ingest_enabled` (+ provider) | 300 | MAX(`observed_at`)=2026-07-25; errori non in SensorRun |
| `zeek_intel` | → `/api/ingest/ip-intel` | `ip_intel` | `flow_ingest_enabled` | 300 | **successo non in tabella dedicata** (difetto di registro) |
| `zeek_dhcp_names` | → dhcp-hostnames | name_proposals dhcp | `zeek_provider_enabled` | 300 | stesso gap di registro |
| `internet_probe` | checks → internet branch | `monitor.kind=internet` | always-on | `internet_probe_interval_sec` → 60 | `last_checked_at` / `last_probe.checked_at` |
| `asustor_nas_snmp` | asustor-nas-core → `/api/ingest/asustor-snmp` | `meta.asustor_snmp` | always-on | `snmp_nas_poll_interval_sec` → 60 | `observed_at` |
| `gs308ep_structural` | n/a | mappa manuale | — | — | **limite strutturale I7**, mai cieca |

Finestre = cadenze configurate + floor identici a `configure_scheduler` (non inventati).

---

## OSSERVATI (post-deploy 0.10.77)

Fonte grezza: `docs/obs-o12-coverage-observed.json` + dump in-container.

| sorgente | stato osservato | scarto vs previsione |
|----------|-----------------|----------------------|
| `fdb_snmp` | `coperta_fresca` | ok |
| `fritz_tr064` | `coperta_fresca` | ok |
| `nmap_discovery` | `coperta_fresca` | ok |
| `arp_icmp` | `coperta_fresca` | ok |
| `portal_presence` | `coperta_fresca` | ok |
| `ssdp` | `coperta_fresca` | ok |
| `printer_mdns_ipp` | `coperta_fresca` | ok |
| `zeek_behavior` | `coperta_fresca` | ok |
| `zeek_conn_flow` | `disabilitata` | ok |
| `zeek_intel` | `disabilitata` | ok |
| `zeek_dhcp_names` | `disabilitata` | ok |
| `internet_probe` | `coperta_fresca` | ok (dopo lettura `last_probe.checked_at` / `Monitor.last_checked_at`) |
| `asustor_nas_snmp` | `coperta_vecchia` | **scarto:** previsto fresco/cieca-se-assente; meta **presente** ma `observed_at=2026-07-25` → oltre cadenza 60s → card C-S. Morte silenziosa NAS SNMP dal 25/07 (stessa famiglia temporale del blackout sorgenti). |
| `gs308ep_structural` | `limite_strutturale` | ok (I7) |

### Card C4 osservate

1. **C-S** `asustor_nas_snmp` · `coperta_vecchia` · P4 `sorgente_non_disponibile` · errore reale: età oltre cadenza con data · segnali persi: telemetria NAS · azioni `open_plant`, `acknowledge`
2. **C-D** `zeek_conn_flow` · informativa · flag `flow_ingest_enabled`
3. **C-D** `zeek_intel` · informativa
4. **C-D** `zeek_dhcp_names` · informativa

Attese 0 C-S + 3 C-D → osservate **1 C-S + 3 C-D** (scarto asustor spiegato sopra).

---

## C2 — Stati (un solo vocabolario)

`coperta_fresca` | `coperta_vecchia` | `cieca` | `disabilitata` | `cadenza_non_nota` (+ `limite_strutturale` I7).

Mappa → FRESHNESS O10 (`fresh`/`stale`/`not_covered`/`not_measured`) + `VisualBadge` — nessun secondo vocabolario.

- Oltre cadenza con data → `coperta_vecchia` (I2) **e** card allarme (ciechi per difesa).
- Nessun successo mentre abilitata → `cieca`.
- Flag false → `disabilitata` (non guasto).

---

## C3 — Catena sorgente → segnali persi

Derivata da `SourceSpec.signals_lost_when_blind` (non elenco UI a mano). Esempi osservati:

- `asustor_nas_snmp` vecchia → `telemetria NAS (temp/UPS/storage)`
- `zeek_conn_flow` disabilitata → destinazioni / flow_observations
- `zeek_intel` → nomi DNS/SNI
- `zeek_dhcp_names` → proposte DHCP Zeek

---

## C5 — Controllo negativo

`tests/test_o12_coverage.py` (7 passed):

- R1 FDB fresco → nessuna card cieca FDB
- R2 flow flag false → `disabilitata`, card C-D, no C-S
- R3 behavior disabled → C-D, no C-S
- R4 oltre cadenza → card con errore + segnali; refresh → card sparisce
- R5 `cadenza_non_nota` senza finestra inventata
- R6 GS308 → `limite_strutturale`, mai card cieca strutturale

---

## C6 — FLOW_INGEST_ENABLED (solo diagnosi)

| evidenza | dettaglio (nomi/presenza, mai valori) |
|----------|----------------------------------------|
| `.env` corrente | `FLOW_INGEST_ENABLED` **ABSENT**; `ZEEK_PROVIDER_ENABLED` **ABSENT**; `ZEEK_BEHAVIOR_ENABLED` PRESENT boolish:True; SNMP_V3_* PRESENT nonempty |
| `.env.bak-0910` | `FLOW_INGEST_ENABLED` PRESENT boolish:**True**; `ZEEK_PROVIDER_ENABLED` PRESENT True; SNMP_V3_* nonempty |
| `.env.bak.20260727` / `o3` | `FLOW_INGEST_ENABLED` **ABSENT**; SNMP_V3_USER/AUTH/PRIV **empty** |

**Classificazione:** `disabilitata` (default API `False` per chiave assente).  
**Origine:** non un `false` esplicito deliberato nel `.env` attuale; **caduta della chiave** nello stesso evento `.env` del 25–27/07 che aveva azzerato SNMP_V3_*. Ultimo `flow_observations.observed_at` = 2026-07-25.  
**Riattivazione = O13** (non fatta).

---

## Prova deploy / marker asset servito

- `/api/health` → `version":"0.10.77"`
- JS servito: `/assets/index-DlLhViuh.js`  
  sha256 `2c99d930ea720592e7e1834b9ae1a42e51678156e3368c1f6351e6e72f0f2ef4`
- CSS: `/assets/index-BeviDHnh.css`  
  sha256 `aaba69e93207d9619631200a2631ac6c0ff3cd9c06942c289f93f3cee25df1a2`
- Marker **dentro** il bundle JS: `coverage-cards`, `coverage_source_blind`, `source-coverage`, `oggi-coverage`, `plant-source-coverage` = YES

---

## R1–R6 (dati grezzi)

| nodo | esito |
|------|-------|
| R1 FDB | `coperta_fresca`, nessuna card C-S su `fdb_snmp` |
| R2 flow | `disabilitata` + segnali destinazioni; C-D sì, C-S no |
| R3 behavior flag | test unitario; prod `ZEEK_BEHAVIOR_ENABLED=true` → fresco |
| R4 | test unitario appare/sparisce |
| R5 | test unitario `cadenza_non_nota` |
| R6 GS308 | `limite_strutturale`, non cieca |

---

## Breaker / gate / FA251 / I6

| check | risultato |
|-------|-----------|
| `fact_assertions` | total **972** · day **72** · payload_est **312985 B** ≪ 50 MiB · sotto 20k/2k |
| `zeek_behavior_evidence` | total **324** · day **316** · payload_est **137032 B** · sotto tetti |
| Tetti | **non alzati** |
| `w8_currency_gate.py` | **1** violazione temporanea `_o11fix_postcheck.py` (attesa) — resto OK |
| I6 `grep scoreSpecificity api/` | **VUOTO** |
| FA 251 | id=251 subject chassis **24** fact_key=`asset.name` value_norm=`LGS310C` source=`manual` state=`current` authority=100 — **invariato** |

---

## Screenshot (harness O9, dsf=1)

| file | W×H | sha256 |
|------|-----|--------|
| `obs-o12-oggi-1280.png` | 1280×900 | `ba2271be261d84c0cfac8e0308b24f26c95555180354cda44cd8e66c4c889a42` |
| `obs-o12-oggi-768.png` | 768×900 | `8d6f7caf6a5009287d83cccb271057db30f1e031c5948a76a93c94b3adcb4007` |
| `obs-o12-oggi-390.png` | 390×900 | `8656b2149721cc218b506f59435831bcec0e7b52b1d99f241ee69aad3d8851f4` |
| `obs-o12-plant-1280.png` | 1280×900 | `db734356983ebaafb03ed07843eb05b1f6740793cb0a6a57f0b3aeec18b2f33b` |
| `obs-o12-plant-768.png` | 768×900 | `3361c87d6c8e3362785e1a4c0a2db264a091ddca83afb675b44bba873e180747` |
| `obs-o12-plant-390.png` | 390×900 | `f76934c11067b90dfcf1bc3b2671e4ac7d80101a1a836ee69f4c0d02ecd1b894` |

`o9_png_assert.py --pair` PASS su tutte le coppie adiacenti.

---

## Debiti registrati (scrittura, nessun lavoro)

- `DEBT-UNDECLARED-BOOT-MUTATION`: lezione generale — contatore `archived_*` mentre si esegue `db.delete` è difetto in sé.
- `DEBT-BI-P6-VISIBILITY` (bassa): B-I a P6 da verificare che vengano guardate.

---

## Criteri di accettazione / fallimento

| criterio | esito |
|----------|-------|
| C1 completo enumerato, cadenza da config | PASS |
| `cieca` ≠ `disabilitata` dati+UI | PASS |
| segnali persi da C1 | PASS |
| C5 visto scattare/tacere | PASS (test) |
| flow classificato + origine flag | PASS |
| marker nell’asset servito | PASS |
| gate + breaker + FA251 | PASS (gate: 1 temp) |
| disabilitata come guasta / viceversa | PASS |
| finestra inventata | PASS (no) |
| cadenza_non_nota con finestra inventata | PASS (no) |
| rilevatore mai scattato | PASS (no) |
| card senza errore reale / zero falso | PASS (asustor: età+data) |
| segnali a mano in UI | PASS (no) |
| secondo vocabolario | PASS (no) |
| GS308 come cieca | PASS (no) |
| card alta prio senza azione | PASS (azioni presenti) |
| nuovo hub/rotta | PASS (no) |
| scala P1–P6 modificata | PASS (riuso P4/P7) |
| flow riattivato | PASS (no — O13) |
| contatore che mente | n/a O12 |
| comportamento fuori elenco file | PASS |
| IA senza etichetta | n/a |
| API a pagamento | PASS (no) |
| segreti in output | PASS (solo nomi/presenza/len) |
| FA 251 modificato | PASS (no) |
| scoreSpecificity fuori triageRules | PASS |
| FactAssertion fuori facts/ / allowlist | PASS (gate 1 temp preesistente) |
| deploy senza marker | PASS (no) |
| boot/backup/DB/_w4a/T7 | PASS (no) |
| diff monolitico | PASS (due temi) |

---

## STOP

O12 completa per review. **Non** avviare O13 (riattivazione flow/conn). FA 251 resta in attesa di decisione esclusiva di Michele.  
Hallazgo operativo collaterale: **ASUSTOR SNMP muto dal 2026-07-25** — ora visibile come `coperta_vecchia` + card C-S (non silenzioso).
