# OBS-FDB O4 — FDB come sensore difensivo (0.10.67)

**Ramo:** `feature/obs-currency` · **prod:** 0.10.67 · **STOP per review** · no merge · no Mappa/308/Dossier/UX

---

## O4.1 — Misura preliminare (prima di abilitare scrittura)

| Voce | Valore |
|------|--------|
| `port.fdb_mac` assertion | **0** (totale / current / per switch) |
| `FACT_SHADOW_WRITERS_ENABLED` | **True** |
| Breaker | **closed** · FA totali **262** · created_today **0** · table ≈106 KiB |
| Tetti | 20.000 / 2.000/giorno / 50 MiB — **non alzati** |
| Poll interval | `TOPOLOGY_POLL_INTERVAL_SEC` unset → default codice **60 s** |
| Binding in `observed_macs` | **58** unici port↔MAC (non 135: 75+60 erano entries poll) |

### Previsione volume (dichiarata PRIMA)

- Binding stabili → refresh (`last_seen_at`), **0 insert/giorno a regime**.
- Bootstrap: ≈ **58** create (≪ 2.000/giorno) → **abilitazione OK**.
- Scarto post-deploy: vedi §Scarti.

---

## Previsioni pre-deploy (enumerate)

### `ruolo_porta`
| port_id | switch:port | atteso | regola |
|---------|-------------|--------|--------|
| **36** | 310c:8 | `uplink` | `link_to_port_id→21` (G1) |
| **21** | 328c:21 | `uplink` | `link_to_port_id→36` |
| altre con MAC | — | `non_determinato` | nessuna evidenza strutturale |
| `accesso` | — | **mai** (nessuna evidenza positiva di accesso senza soglia) | I2 |

### Baseline / LAA / solo L2
- Baseline attesi: tutti i MAC del primo populate porta (~58) marcati `baseline`.
- LAA (bit U/L): `76:47:64:FE:41:8B`, `DA:24:DD:18:75:E2`, `DA:24:DD:18:C4:D3`, `DA:24:DD:19:7A:D3`, `DA:24:DD:97:0B:DF` (+ eventuali nuovi LAA post-O3).
- Solo L2 attesi (no IP current): `38:A6:CE:3E:9C:A8`, `38:A6:CE:3E:9C:AE`, `38:A6:CE:40:A7:76`, `70:50:AF:FB:86:F8`, `70:50:AF:FC:0A:F8`, `D4:52:EE:C3:25:16`, `D4:52:EE:C3:25:17`, `D8:EC:5E:CC:1C:14`.

### Card primo ciclo
- S-A: **0** (bootstrap = baseline, non «nuovo»).
- S-B: **0** (G3: presenza multipla uplink↔accesso ≠ move).
- S-C: fino a ~8 (solo L2 non-uplink).
- S-D: **0** (poll fresco).

---

## Implementazione

- Fact `port.fdb_mac` (subject **port**, excl MAC-centrico) via `safe_shadow_port_fdb_snapshot` in `facts/shadow.py`; hook in `apply_fdb_observation`.
- Baseline in `value_json.baseline` + `baseline_at`; refresh **non** cancella baseline.
- MAC-move = supersession **solo se** l’altra porta **non** elenca più il MAC (presenza concorrente ≠ move) — fix hotfix stesso bump.
- Letture currency: `facts/port_fdb.py` (mai `FactAssertion` fuori da `facts/`).
- Segnali: `services/fdb_defense.py` + `GET/POST /api/fdb-defense/*`; Oggi sezione FDB + blocco INFERENZA; slot LLM `/ai` **disattivato**.
- Debiti: `DEBT-ENV-NO-INTEGRITY-CHECK`; precisazione data in `obs-o3.md`; nota O4 su `DEBT-PRIVACY-MAC-CHURN`.

---

## Osservati post-deploy

### Breaker / volume
| Istante | FA tot | created_today | port.fdb_mac | current | mac_move | breaker | fact_assertions MiB |
|---------|--------|---------------|--------------|---------|----------|---------|---------------------|
| pre | 262 | 0 | 0 | 0 | 0 | closed | ~0.1 |
| dopo 1° ciclo (bug move) | 510 | 248 | 248 | 76 | 172 | closed | — |
| T0 post-fix | 734 | 472 | 472 | 76 | 396 | closed | — |
| T1 (~2') | 794 | 532 | 532 | **135** | **396** | closed | — |
| T2 (+130 s) | **794** | **532** | **532** | **135** | **396** | closed | **0.285** |

Regime dopo fix: **Δ create = 0** su due cicli poll; tetti non superati; tetti **non alzati**.

### G1–G6
| Nodo | Esito | Grezzo |
|------|-------|--------|
| G1 | **PASS** | port **36** `uplink` rule=`link_to_port_id→21`; port **21** `uplink` rule=`link_to_port_id→36`; **mai** per conteggio MAC |
| G2 | **PASS** (test) | baseline refresh → no S-A |
| G3 | **PASS** | presenza multipla; dopo fix MOVES stabili; S-B assente su uplink |
| G4 | **PASS** | S-C enumerati sotto |
| G5 | **PASS** (test+cap) | GS308EP `fdb_supported=false` → no S-D inventato |
| G6 | **PASS** (test) | S-D `sorgente_non_disponibile` + errore Timeout reale |

### Card osservate (T1)
S-C media (non_determinato):  
`DC:15:C8:80:BB:EA` 328c:2 · `F0:B0:14:90:87:96` 328c:2 · `F0:B0:14:90:87:97` 328c:2 · `38:A6:CE:3E:9C:A8` 328c:6 · `38:A6:CE:40:A7:76` 328c:9 · `70:50:AF:FB:86:F8` 328c:12 · `70:50:AF:FC:0A:F8` 328c:14 · `38:A6:CE:3E:9C:AE` 328c:16 · `D4:52:EE:C3:25:16` 310c:5 · `D4:52:EE:C3:25:17` 310c:5  

S-A/S-B/S-D: **0**.

### LAA current (value_json.randomized)
`0A:53:5E:59:F6:A8`, `6E:4C:CE:84:8E:1D`, `76:47:64:FE:41:8B`, `DA:24:DD:18:75:E2`, `DA:24:DD:18:C4:D3`, `DA:24:DD:19:7A:D3`, `DA:24:DD:97:0B:DF` — priorità non alta.

### Baseline
`CUR_BASELINE 49 of 135` — scarto vs previsione 58: churn pre-fix ha ricreato binding senza flag baseline; i 49 restano marcati; UI mostra `baseline_at` dove presente. Nuovi MAC post-baseline → S-A (corretto).

---

## Scarti previsione ↔ osservato

1. **Bootstrap create ≫ 58:** bug iniziale «ogni presenza duale = mac_move» → centinaia di create. **Fix:** supersession solo se l’altra porta non elenca più il MAC. Post-fix: create=0/ciclo.
2. **current 135 ≠ 58:** corretto dopo fix — un MAC può essere current su **più porte** (unique slot per subject); i ~58 multi-port O3 diventano doppi binding.
3. **`accesso` mai emesso:** algoritmo O4.3 passo 3 → solo `non_determinato`; segnali su non-uplink a priorità ridotta (I2: non inventiamo accesso).
4. **S-C 10 vs 8:** due MAC aggiuntivi / porte 310c:5 dopo dual-current.

---

## Gate

```
python3 scripts/w8_currency_gate.py
→ VIOLAZIONI: 0 · PASS (con 1 eccezione temporanea)

grep -RInE 'scoreSpecificity|specificity' api/
→ VUOTO (I6)
```

Test: `tests/test_o4_fdb_defense.py` **8 passed**; FE `oggiProblems.test.js` fdbDefenseFields **ok**.

---

## Criteri di fallimento (verificati uno a uno)

| Criterio | Esito |
|----------|-------|
| uplink per conteggio MAC | **no** — solo link_to_port_id |
| soglia numerica inventata | **no** |
| MAC bootstrap come «nuovo» difensivo | **no** S-A a regime; baseline esplicita |
| data baseline non in UI | **no** — `baseline_at` in card/meta |
| inferenza senza etichetta/fonte/confidenza o azione auto | **no** — blocco INFERENZA; llm_slot disabled |
| API a pagamento | **no** |
| card alta senza azione | **no** — ogni card ha actions |
| sorgente_non_disponibile ≈ assente/zero | **no** (G6 test) |
| FactAssertion fuori facts/ / allowlist | **no** — helper in `facts/port_fdb.py` |
| breaker / tetti alzati | **no** — closed, 0.285 MiB, tetti invariati |
| LAA → priorità alta | **no** |
| SNMP SET / config apparati | **no** |

---

## Deploy

`./scripts/deploy.sh api web` → 0.10.67; hotfix `api` solo (fix concurrent move). Collector non ricreato (env invariato).

---

## STOP

Review. Non avviare Mappa / 308 / Dossier / UX / favicon. Non chiudere cantiere. Non merge su main.
