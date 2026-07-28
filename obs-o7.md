# OBS-DOSSIER O7 — il Dossier risponde (0.10.70)

## REGISTRO DI RIMOZIONE (D1 — enumerato)

| campo / blocco | dove stava | destinazione / motivo |
|----------------|------------|------------------------|
| TOC «chi sei / come sei connesso / tu decidi / abitudini / note / ramo 308» | `Dossier.vue` nav | riformulato in toc sei domande (azioni·cos'è·dove·da quando·cosa fa·atteso?·inferenza) |
| Header strip `presenza · IP · MAC` monospazio | `Dossier.vue` `.dossier-sub` | riformulato in **Cos'è** (MAC/IP/solo-L2) + freschezza in **Dove sta** |
| Pulsanti header «Inventario / Topologia» | `Dossier.vue` `.dossier-actions` | riformulato in azioni **Apri Impianto / Apri Topologia** (Q6) |
| `Branch308Card` inline per asset 4 | `Dossier.vue` `#ramo-308` | riformulato: link `/gs308` da **Dove sta** quando `behind_308` o azioni; scheda ramo non più dump in pagina |
| Sezione «Chi sei» (`AssetIdentity` grid Vendor/Tipo/OS) | `AssetIdentity.vue` `.id-grid` | riformulato in **Cos'è** via `GET /dossier` |
| KV Hostname / Servizi / MAC / Prima volta / Presenza | `AssetIdentity.vue` `.inv-identity-kv` | Hostname/Servizi → dettaglio diagnostico chiuso (`identity` endpoint); MAC/Prima volta → **Cos'è** / **Da quando**; Presenza → non più dump header (stato in **È atteso?** + habits) |
| Blocco «Proposte nome (AI)» inline | `AssetIdentity.vue` | riformulato in **INFERENZA IA** (fonte+confidenza) |
| Toggle «Proteggi da scansione OS» + note | `AssetIdentity.vue` | relegato in «Altre decisioni» (`AssetDecide` details) — diagnosi/config, non percorso decisionale |
| Semaforo `scan_readiness` + «Rileva OS ora» + reason | `AssetIdentity.vue` | relegato in **Dettaglio diagnostico** chiuso di default |
| Sezione «Sintesi identità» (Cosa sappiamo / Fonti / Freschezza / Incerto / Cosa manca) | `AssetIdentity.vue` `#sintesi-identita` | riformulato: fatti in Q1–Q5; freschezza O2/O5 in **Dove sta**; incerto in **INFERENZA IA** |
| `CandidateList` OS multipli aperti | `AssetIdentity.vue` | relegato dietro dettaglio diagnostico / altre decisioni |
| Sezione «Come sei connesso» Presenza/Stato/date/Porta | `AssetChassis.vue` | riformulato: porta → **Dove sta** (FDB); date → **Da quando** (catena + label baseline); stato → **È atteso?** |
| Lista «Interfacce» grezza (mac/name/kind/ip per NIC) | `AssetChassis.vue` | rimosso dal percorso decisionale perché privo di valore immediato; raggiungibile via identity/chassis API in dettaglio diagnostico |
| Warning «vista chassis parziale» a pieno schermo | `AssetChassis.vue` | rimosso dalla vista principale (motivo: rumore; chassis resta in API) |
| Form Decide a piena pagina (categoria/OS/watch fingerprint) | `AssetDecide.vue` sopra la piega | riformulato: azioni primarie in Q6; form completo in `<details>Altre decisioni` chiuso di default |
| «Suggerito» + Adotta + Proponi nome (AI) a piena vista | `AssetDecide.vue` | riformulato: proposte in **INFERENZA IA**; adozione solo via azione esplicita Q6 / details |
| Dump grezzo `?technical=1` in UI | mai montato nel Dossier (già `false`) | dichiarato nel dettaglio diagnostico come endpoint, **non** aperto in UI |
| Eventuali residui «Visualizza dati» | assenti nel tree pre-O7 | n/a — confermato assente; vietato reintrodurre |

Nessun campo sopra è sparito senza riga in questo registro.

---

## PREVISIONI (prima del deploy)

### Nodi

| nodo | previsioni |
|------|------------|
| **K1** asset 135 `D4:52:EE:C3:25:16` | solo-L2; Dove=`310c:5`; Cos'è nome legacy/noto; È atteso=atteso ma blue-team per solo-L2; storia: eventi non-defect + **7** esclusi O4; inferenza OUI |
| **K2** asset 51 allsky3 | Dove=`dietro il 308, porta interna non determinabile` + link `/gs308`; azione assign_308_port |
| **K3** asset 3 LGS310C | nome: **atteso manual** su chassis — in DB fact `asset.name` manual è su chassis **24** (orphaned), asset su chassis **32** → previsione aggiornata: **legacy_manual** (I2 onesto) + nessun dump |
| **K4** asset 56 Echo Lavanderia (`50:99:5A:6E:EA:37`) | first_seen kind=`lower_bound_reconstructed`, copy ricostruzione, no storia inventata |
| **K5** asset 4 GS308EP | campi FDB/SNMP → `non misurato` + errore SNMP Timeout reale |
| **K6** = K1 | excluded_defect_count=7, nota DEBT-O4-SPURIOUS-MOVES |

### Campi → non misurato
- `fdb_locale_308`, `snmp_308` su asset 4 (I7 / poll fallito)

---

## OSSERVATI (post 0.10.70)

| nodo | osservato | scarto |
|------|-----------|--------|
| K1 | solo_l2=true; where `310c:5` misurata_fresca; name Sky TV `legacy_manual`; expected atteso+central; events=2; **excluded=7** con nota; INFERENZA IA | ruolo `non_determinato` (non «accesso») — evidenza strutturale roles, non inventato |
| K2 | behind_308 + link `/gs308` + assign_308_port | = |
| K3 | LGS310C `legacy_manual`; where `328c:21` uplink; no grezzi | vs «manual»: fact 251 orphaned chassis 24 ≠ 32 → **scarto spiegato** (I2) |
| K4 | label ricostruzione baseline 2026-07-28T22:22:08Z + storia precedente non disponibile | = |
| K5 | non_measured fdb+snmp con Timeout | = |
| K6 | excluded=7 + nota DEBT | = |

---

## Breaker

| metrica | valore |
|---------|--------|
| FA totali | 819 |
| FA giorno | 557 |
| DB MiB | 1805.12 (annotato `DEBT-DB-SIZE-OBSERVED` — **nessun intervento**) |
| breaker_open | False |
| tetti | invariati |

## Gate

```
w8_currency_gate.py → VIOLAZIONI: 0 · PASS (1 temporanea)
grep specificity api/ → VUOTO (I6)
```

Test: `pytest tests/test_o7_dossier.py` → 6 passed; `dossierO7.test.js` + inventoryDevices → pass.

---

## Criteri di fallimento

| criterio | esito |
|----------|-------|
| Campo rimosso fuori registro | **no** |
| Dump grezzo sopravvissuto | **no** |
| Storia più ricca dell'evidenza | **no** |
| 396 defect in storia / esclusi senza nota | **no** (7 su K1 con nota) |
| Sorgente non fresca come zero/vuoto/corrente | **no** (K5 non misurato) |
| Secondo vocabolario freschezza | **no** (O2/O5) |
| Inferenza senza INFERENZA IA/fonte/conf | **no** |
| Inferenza che scrive | **no** |
| API a pagamento | **no** |
| Pulsante inerte / azione irrev. senza confirm | **no** |
| FactAssertion fuori facts/ / allowlist | **no** |
| Lavoro boot/DB/`_w4a` | **no** |
| Diff monolitico | **no** |

**STOP per review.** Non O8/coda · non UX · non merge main.
