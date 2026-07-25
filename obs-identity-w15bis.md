<!-- BLOCK-ID: OBS-IDENTITY-W15BIS -->

# OBS-IDENTITY W1.5-bis — Chiusura gate 0.10.42 / correzione 0.10.43

## Numerazione (dichiarata)

**Ramo CON modifiche di codice** → bump **0.10.43** (questa correzione).  
Sequenza slittata: W2→**0.10.44** · W4a→0.10.45 · W4b→0.10.46 · W5→0.10.47 · W6→0.10.48 · W7→0.10.49 · W8→0.10.50.

Motivo bump: (1) rimozione soglia E3 inventata (`mac_count_threshold` default); (2) test D.2 limiti E5-physical; (3) tool dry-run RO.

---

## Attribuzione structural=1

### A.1 Boot1 post-deploy 0.10.42 vs regime

| | Boot1 (primo post-deploy) | Boot regime (successivo) |
|--|---------------------------|---------------------------|
| T_total | **93.522 s** | **8.829 s** |
| needs_apply | **true** | **false** |
| T_backup | **82.535 s** | **0.0** |
| structural | **1** | 0 (apply non necessario) |
| identical_rewrite | **available=false** (non nel payload timing) | idem |
| inventory_undid_count | **available=false** (non nel payload timing) | idem |

Il regime 8.829 s **non** è il primo boot: T_backup boot1 ≠ 0. Dichiarato esplicitamente.

**[timing] boot1 (completo):**
```json
{"event":"api_boot","version":"0.10.42","epoch_start":1785003789.414,"epoch_import_end":1785003789.456,"epoch_bootstrap_end":1785003878.627,"epoch_ready":1785003882.936,"needs_backup":true,"needs_apply":true,"t_total_level_check":"identity","timers":{"T_total":{"s":93.522,"parent":null},"T_import":{"s":0.042,"parent":"T_total"},"T_bootstrap_wall":{"s":89.171,"parent":"T_total"},"T_uvicorn_to_ready":{"s":4.309,"parent":"T_total"},"T_trust":{"s":83.027,"parent":"T_bootstrap_wall"},"T_dry_run":{"s":0.086,"parent":"T_trust"},"T_prefetch_obs":{"s":null,"parent":"T_dry_run"},"T_prefetch_fdb":{"s":0.003,"parent":"T_dry_run"},"T_plan_loop":{"s":0.083,"parent":"T_dry_run"},"T_dry_residuo":{"s":0.0,"parent":"T_dry_run"},"T_backup":{"s":82.535,"parent":"T_trust"},"T_apply":{"s":0.398,"parent":"T_trust"},"T_residuo_trust":{"s":0.008,"parent":"T_trust"}}}
```

### A.2 Istanza unica

| Campo | Valore |
|-------|--------|
| asset_id | **116** |
| campo | `meta.operational_state` (confrontato con `trust_level`) |
| prima | `operational_state=active`, `trust_level=fritz_historical` |
| dopo (atteso apply) | `operational_state=fritz_historical` |
| sorgente plan | `reconcile_trust_history` / `_apply_trust_plan` |
| backup pre-apply | `/data/backups/observatory-20260725-202313-829830.db` |

Asset 116: **nessuna interfaccia**, nome vuoto, Fritz storico `active=false` (2026-07-18).

### A.3 Attribuzione: **(a) CHURN PREESISTENTE**

Prova:
1. `rg` su `api/app/identity_evidence/`: **nessuna** scrittura di `trust_level` / `operational_state` / colonne Asset (solo commenti «never mutates»).
2. Stesso mismatch asset **116** nei backup **pre-0.10.42**: `observatory-20260725-194124`, `195748`, `pre-deploy-20260725-2021` → mismatch_n=1 ids=[116].
3. Simulazione WAL-safe: trust apply → `op_state=fritz_historical` / needs_apply=false; poi `inventory.reconcile_asset_presence` → di nuovo `active` / needs_apply=true.

**Non (b):** G6 identity non violato.

### A.4 Ricorrenza

| Backup | mismatch fh≠op | ids |
|--------|----------------|-----|
| 194124 (pre W1.5) | 1 | 116 |
| 195748 (W1 boot) | 1 | 116 |
| 202313 (boot1 W1.5) | 1 | 116 |
| pre-deploy-2021 | 1 | 116 |
| live (misura w15bis) | 1 | 116 |

Archiviato come **DEBT-RECONCILE-CHURN-1** (inventory undoes trust quarantine su asset 116).

### A.5 Impatto W4b

Campo coinvolto = `operational_state` / `trust_level` (reconcile structural). **Non** `Asset.name` né `chassis_id`. Design W4b (canonico via `link_state=confirmed`) **invariato**.

**GATE A: VERDE** (a).

---

## Gate dimostrati

### G2 — Suite completa (container api Py3.12)

Vedi sezione post-deploy 0.10.43. Localmente identity: **26 passed** (T1–T21 + parity + D.2 + T14b).

Asserzioni T1–T21 (testo):

| T | Asserzione |
|---|------------|
| T1 | `proposals == []` e `max_decision == D0` senza E4/E5 |
| T2 | `state == stale` e decision ∈ {D0,D1} |
| T3 | presence `absent_unmeasured`; level `E0-unmeasured` ≠ `E0-absent` |
| T4 | `found == []` predicati adiacenza assenti |
| T5 | U/L → non E5-bridge |
| T6 | self chassis_id → `proposals == []` |
| T7 | A~B∧B~C confermati → nessun A~C confirmed |
| T8 | provenance justifies link → `proposals == []` |
| T9 | FDB-only bridge → level ≠ E5-bridge |
| T10 | LLDP subtype≠macAddress → ≠ E5-bridge; macAddress → E5-bridge |
| T11 | E4∧E3 → `decision_level==D2`, confirm raises, no chassis mutate |
| T12 | E5-bridge + seriali distinti + physical ctx → D2, confirm raises |
| T13 | 3 cicli decay → `link_state` resta confirmed |
| T14 | E3 senza access → E2 |
| T15 | E5-physical → D3 proposed, not confirmed |
| T16 | confirm idempotente: 1 sola audit confirm |
| T17 | split → retracted, member_id intatti |
| T18 | 147/151 historical → no consolidabile, chassis invariati |
| T19 | LGS328C storico → no proven_same |
| T20 | LGS310C pin non usato come E5; name invariato |
| T21 | contradiction → manual_review, name invariato |

### G3 — grep (output vuoto mostrato)

- adiacenza MAC in identity_evidence: **(empty)**
- `asset.(chassis_id|name|trust_level)=` in identity_evidence: **(empty)**
- IdentityEvidence/Proposal costruiti solo in `store.py` / `linker.py` / `decisions.py` (path proposal/confirm; **nessun writer ingest attivo**)
- K7: `circularity.py` rifiuta chassis_id self-evidence

### G4 — I6

`rg scoreSpecificity|specificity api/` → **(empty)**

### G5 — Parità schema vs prod

Post-boot 0.10.42: tabelle `identity_evidence` / `identity_link_proposals` create via create_all (counts 0/0). Indice fact_assertion:
`CREATE UNIQUE INDEX uq_fact_assertions_current_slot ON fact_assertions (subject_type, subject_id, excl_key) WHERE state='current'`  
Alembic **non** gira in prod. Test `test_schema_parity_identity_tables_match_models` verde. Violazione indice: verificata in test suite facts (W1), non sul DB live.

### G7 — Previsioni 0.10.42 **ricostruite a posteriori** (non pre-dichiarate)

| Metrica | Previsto (ricostruito) | Osservato regime | Scarto |
|---------|------------------------|------------------|--------|
| identity_evidence | 0 | 0 | 0 |
| proposals | 0 | 0 | 0 |
| T_total regime | 8.8–9.0 | 8.829 | in banda |
| needs_apply regime | false | false | 0 |
| T_backup regime | 0 | 0 | 0 |
| name_proposals | 412 | 412 | 0 |
| assets/AD/ip | 151/82/100 | 151/82/100 | 0 |
| Boot1 T_backup | (non predetto onesto) | 82.535 | — churn 116 |

**Marca:** previsioni ricostruite a posteriori, non pre-dichiarate.

### C.6 Invariante tag

| Ref | Valore |
|-----|--------|
| tag v0.10.42 | `584cbf4` |
| branch feature/obs-currency @ tag | `584cbf4` |
| main | **non** necessariamente = tag (cantiere su feature branch) |
| VERSION container pre-correzione | 0.10.42 |

### C.7 Tetto anti-ballooning

**Vacuo** con writer spenti (rows=0). Rimandato a **W2 (0.10.44)** quando i writer sono accesi.

**GATE B: VERDE** · **GATE C:** vedi sezione post-0.10.43 (G2 conteggiato, non verde; C.7 vacuo).

---

## Fase D — T12 e correzioni

### D.1 Fix T12 nel linker (non nel test)

Asserzione stabile: `proposals[0].decision_level == D2_PROPOSAL` con E5-bridge + seriali distinti + `is_physical_bridge_context`.  
Fix in `linker.py`: `_distinct_physical_serials` + drop E5-physical discordanti dalla decision; physical_ctx forzato. Test non indebolito.

### D.2 Test aggiunti

- `test_t14b_e3_without_explicit_threshold_degrades_to_e2`
- `test_d2_distinct_physical_serials_no_merge_unresolved`
- `test_d2_serial_present_on_one_only_unresolved`
- `test_d2_same_serial_different_sources_provenance_ok`

### D.3

Nessuna scrittura Asset da identity (A=a). Churn 116 → debito, non fix in questa ondata.

### D.4

Bump **0.10.43**.

---

## PREDICTIONS pre-deploy 0.10.43

| Metrica | Atteso |
|---------|--------|
| T_total regime | 8.8–9.0 |
| needs_apply regime | false |
| T_backup regime | 0 |
| Boot1 structural | **1** (asset 116, DEBT-RECONCILE-CHURN-1) — giustificato Fase A |
| identity_evidence / proposals | 0 / 0 |
| name_proposals | 412 |
| assets / AD / ip | 151 / 82 / 100 |

## OBSERVED 0.10.43

### Boot1 (primo post-deploy — **non** sostituibile col regime)

| | Valore |
|--|--------|
| T_total | **93.836 s** |
| needs_apply | **true** |
| T_backup | **84.636 s** |
| structural | **1** (asset **116**, DEBT-RECONCILE-CHURN-1 — previsto) |
| identity_evidence / proposals | **0 / 0** |

**[timing] boot1 0.10.43 (completo):**
```json
{"event":"api_boot","version":"0.10.43","epoch_start":1785004909.619,"epoch_import_end":1785004909.663,"epoch_bootstrap_end":1785004999.42,"epoch_ready":1785005003.455,"needs_backup":true,"needs_apply":true,"t_total_level_check":"identity","timers":{"T_total":{"s":93.836,"parent":null},"T_import":{"s":0.044,"parent":"T_total"},"T_bootstrap_wall":{"s":89.757,"parent":"T_total"},"T_uvicorn_to_ready":{"s":4.035,"parent":"T_total"},"T_trust":{"s":84.913,"parent":"T_bootstrap_wall"},"T_dry_run":{"s":0.087,"parent":"T_trust"},"T_prefetch_obs":{"s":null,"parent":"T_dry_run"},"T_prefetch_fdb":{"s":0.003,"parent":"T_dry_run"},"T_plan_loop":{"s":0.083,"parent":"T_dry_run"},"T_dry_residuo":{"s":0.001,"parent":"T_dry_run"},"T_backup":{"s":84.636,"parent":"T_trust"},"T_apply":{"s":0.189,"parent":"T_trust"},"T_residuo_trust":{"s":0.0,"parent":"T_trust"}}}
```

### Regime (boot successivo — dichiarato distinto)

| | Valore |
|--|--------|
| T_total | **8.891 s** (banda 8.8–9.0) |
| needs_apply | **false** |
| T_backup | **0** |
| identity_evidence / proposals | **0 / 0** |
| name_proposals | **412** |
| assets / ip_current | **151 / 100** |
| devices_active (AD) | **82** (`chassis_grouping.device_counters`) |
| writers identity | **spenti** (ie=0, ilp=0) |

**[timing] regime 0.10.43:**
```json
{"event":"api_boot","version":"0.10.43","epoch_start":1785005027.778,"epoch_import_end":1785005027.822,"epoch_bootstrap_end":1785005032.742,"epoch_ready":1785005036.669,"needs_backup":false,"needs_apply":false,"t_total_level_check":"identity","timers":{"T_total":{"s":8.891,"parent":null},"T_import":{"s":0.044,"parent":"T_total"},"T_bootstrap_wall":{"s":4.92,"parent":"T_total"},"T_uvicorn_to_ready":{"s":3.927,"parent":"T_total"},"T_trust":{"s":0.089,"parent":"T_bootstrap_wall"},"T_dry_run":{"s":0.089,"parent":"T_trust"},"T_prefetch_obs":{"s":null,"parent":"T_dry_run"},"T_prefetch_fdb":{"s":0.003,"parent":"T_dry_run"},"T_plan_loop":{"s":0.086,"parent":"T_dry_run"},"T_dry_residuo":{"s":0.0,"parent":"T_dry_run"},"T_backup":{"s":0.0,"parent":"T_trust"},"T_apply":{"s":0.0,"parent":"T_trust"},"T_residuo_trust":{"s":0.0,"parent":"T_trust"}}}
```

Predizioni regime: **match** (scarto T_total in banda). Boot1 structural=1 giustificato Fase A — **non** regressione identity.

---

## Gate C — suite Py3.12 (container) + env-bound

### Ambiente

- Host locale Mac: Py3.9 → collection fallisce (`DEBT-PYTEST-COLLECTION-PY39`) — **non** usato per dichiarare verde.
- Suite gate: container image `observatory-api` **Py3.12.13**, `pytest` con `--entrypoint python3`, test copiati nel layer (no bind-mount NFS lento).
- Ignore espliciti (env-bound, documentati sotto): `test_kuma_native_migration.py`, `test_m1b_measure_gate.py`.

### Env-bound (nominali — non collezionabili senza path extra)

| Test | Motivo collection fail | Remedio dichiarato |
|------|------------------------|--------------------|
| `tests/test_kuma_native_migration.py` | `FileNotFoundError: /tmp/scripts/migrate_kuma_to_native.py` | montare/copiare `scripts/` oppure skip dichiarato |
| `tests/test_m1b_measure_gate.py` | `ModuleNotFoundError: measure_store_gate` (`tools/`) | aggiungere `tools/` a `PYTHONPATH` oppure skip dichiarato |

Output grezzo (tail collect-only):

```
E   FileNotFoundError: [Errno 2] No such file or directory: '/tmp/scripts/migrate_kuma_to_native.py'
… Interrupted: 1 error during collection …
E   ModuleNotFoundError: No module named 'measure_store_gate'
… Interrupted: 1 error during collection …
```

### G2 esito suite (post-ignore) — `w15bis-suite`

| | |
|--|--|
| Container | `w15bis-suite` (image `observatory-api`, entrypoint `python3`, tests/`collector`/`mac_ip_policy` via `docker cp` nel layer) |
| Python | **3.12.13** · pytest 8.3.4 |
| Ignore | `--ignore=test_kuma_native_migration.py --ignore=test_m1b_measure_gate.py` |
| Durata | **8654.27 s** (2:24:14) |
| Exit | **1** |
| **passed** | **556** |
| **failed** | **12** |
| **skipped** | **0** (non in summary) |
| **errors** | **0** (collection) |
| Copertura | 556+12 = **568** = collected con i 2 env-bound esclusi |

**FAILED (12)** — motivi (da TB / assert):

| Test | Motivo |
|------|--------|
| `test_m1_alembic.py::test_alembic_upgrade_downgrade_fresh` | `alembic.CommandError`: Path `/tmp/api/app/alembic` assente nel container suite |
| `test_m1_alembic.py::test_alembic_stamp_preserves_existing_data` | idem path alembic |
| `test_m2_discovery.py::test_fdb_skips_observe_portal_on_uplink_role` | `assert <datetime> is None` (portal last_seen non None) |
| `test_nmap_provider.py::test_dual_dedup_same_mac_entity_key_and_provenance` | `assert 'MAC\|IP' == 'MAC'` (entity_key include IP) |
| `test_printer_alembic.py::…upgrade_downgrade…` | path alembic assente |
| `test_printer_alembic.py::…requires_pre_backup` | path alembic assente |
| `test_printer_enrichment.py::test_ipp_precedence…` | `assert ('HP123','fritz') == ('Stampante Studio','ipp')` |
| `test_printer_enrichment.py::test_snmp_enrichment…` | `assert [] == [('snmp', …)]` |
| `test_printer_provider.py::test_r2_ip_migration_category…` | `AttributeError: 'NoneType'.id` |
| `test_ssdp_alembic.py::…upgrade_downgrade…` | path alembic assente |
| `test_ssdp_alembic.py::…requires_pre_backup` | path alembic assente |
| `test_ssdp_provider.py::test_r2_ip_migration_evidence…` | `AttributeError: 'NoneType'.id` |

**Identity / MAC-IP:** nessun test `test_identity_evidence*` / `test_mac_ip_policy*` nella short summary FAILED. Locale: `test_identity_evidence`+`test_mac_ip_policy` → **35 passed**.

**G2 dichiarazione:** suite **eseguita e conteggiata**; **non** «suite verde» (12 failed). Fallimenti alembic = debiti di **wiring path** nel runner usa-e-getta (manca copia `api/app/alembic` in `/tmp/api/...`); gli altri 6 sono fuori perimetro identity W1.5-bis.

### G3 / G4 (output mostrato)

```
rg 'asset\.(chassis_id|name|trust_level)\s*=' api/app/identity_evidence/  → (empty)
rg 'scoreSpecificity|specificity' api/  → (empty)
```

### MAC↔IP (fixture / debito wiring — **non** reconcile live, **no** writer)

- Classifier: `api/app/services/mac_ip_policy.py`
- Contratto: `tests/test_mac_ip_policy.py` → **9 passed**
- Doc: `docs/obs-currency-mac-ip-policy.md`
- Debito: **DEBT-MAC-IP-POLICY-WIRE** (wiring in W7; vietato collegare ora a `reconcile_asset_presence`)

### Esito suite (riga canonica)

```
12 failed, 556 passed, 3408 warnings in 8654.27s (2:24:14)
EXIT:1
```

**GATE C:** G3/G4/G5/G7/C.6/C.7 OK · env-bound documentati · MAC-IP fixture OK · G2 **conteggiato ma non verde** (12 failed dichiarati).

---

## Esito

| Gate | Stato |
|------|--------|
| A (structural=1 → churn 116) | **VERDE** |
| B (dry-run linker RO) | **VERDE** |
| C (suite+greps+env-bound) | **PARZIALE** — greps/env-bound/MAC-IP OK; suite 556/568 pass, 12 fail dichiarati |

VERSION **0.10.43** · tag `v0.10.43` @ `d5c41a1` · writers identity **spenti**.  
Debiti aperti rilevanti: DEBT-RECONCILE-CHURN-1 · DEBT-E3-AVAILABLE-FALSE · DEBT-MAC-IP-POLICY-WIRE · DEBT-FDB-LLDP-PASSIVE · DEBT-PYTEST-COLLECTION-PY39.

**STOP per review** — **non** W2 (target **0.10.44**).
