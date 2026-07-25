# W-D — Sblocco gate W2 (T-b, T-e, T-f) + chiusure pendenti

**Data:** 2026-07-26 · **VERSION:** `0.10.45` · **Ramo:** `feature/obs-currency`  
**C.5:** STOP **REVOCATO** (non rimesso in discussione). NESSUN rollback a `v0.10.43`.  
**W2 writers:** **non** avviati — stop dopo review diff (prompt W2 separato).

## Rinumerazione

| Ondata | VERSION |
|--------|---------|
| W-D (questo) | **0.10.45** |
| W2 | 0.10.46 |
| W4a | 0.10.47 |
| W4b | 0.10.48 |
| W5 | 0.10.49 |
| W6 | 0.10.50 |
| W7 | 0.10.51 |
| W8 | 0.10.52 |

Diff: [`docs/obs-wd.diff.txt`](obs-wd.diff.txt)

---

## D.0.a — AD 69 vs invariante 82

**Definizione contatore:** `DEVICE_ACTIVE_WINDOW = timedelta(hours=24)` in `api/app/services/chassis_grouping.py` **riga 31**; uso in `device_counters` **righe 860–861** (`last_seen` entro 24h → `devices_active`).

| Domanda | Risposta |
|---------|----------|
| (1) Finestra mobile o conteggio stabile? | **Finestra mobile 24h** — varia per natura con `last_seen` |
| (2) I 13 usciti = i 13 con IP fritz storicizzato? | **No.** Intersezione stale ∩ hist-fritz = **5** id: **95, 106, 108, 118, 122**. Hist-fritz asset: 3,4,6,50,82,89,91,95,99,106,108,118,122 (13). Stale device-counter (42) ≫ 13. |

**Conclusione:** invariante «AD 82» **MAL SPECIFICATA**. Sostituita: assert su **snapshot finestra** (`AD_devices_active` pre-deploy = **69**), non su 82 fisso. Coincidenza Δ=13 ≠ set purge.

---

## D.0.b — Quarantena non assorbente

| Percorso lift (trust) | File:riga |
|----------------------|-----------|
| Portal evidence (nmap/icmp/…) → `observe_portal` set `operational_state=active` se `inventory_hidden_auto` | `trust.py` **66–74** |
| Fritz `active=True` → `lift_fritz_quarantine_on_active` | `trust.py` (nuovo) chiamato da `inventory.update_fritz_evidence` |
| Trust plan apply: level `known`/`confirmed_present` + `inventory_hidden_auto` → active | `trust.py` **584–592** (post-rinumera locale) |

Inventory **non** solleva (`inventory_may_set` rifiuta `fritz_historical`→`active`).

**Test:** `test_fritz_historical_lifts_on_new_fritz_active` — **PASS**.

---

## D.1 — T-b DEBT-ENTITY-KEY-MAC-IP **CHIUSO**

### Call site `entity_key_for` / `entity_key`

| Consumatore | Impatto |
|-------------|---------|
| `observations_store.compute_dedup_key` / `upsert_observation_raw` | Dedup ora MAC-scoped; multi-IP stesso MAC collassa in-window |
| `ObservationRaw.entity_key` colonna | Nuove righe = MAC; storico resta `MAC\|IP` finché non riscritto |
| `test_nmap_provider` T-b | Contratto MAC — verde |
| `fingerprint_facts` (legge entity_key SSDP) | IP-only keys invariate per envelope senza MAC |
| Provider docs ssdp/printer `entity_key=IP` | Invariato (MAC assente → provisional) |

**Fallback:** MAC assente → key=IP + `payload.identity_provisional=true`. Merge post-MAC: **DEBT-PROVISIONAL-IDENTITY-MERGE** (non inventato).

**Produzione (campione id, forma attuale pre-rewrite):** ancora `MAC|IP` sulle raw esistenti (es. id 872171…872157). **Delta contatori atteso dal cambio forma: 0** (nessuna riscrittura storica).

---

## D.2 — T-e / T-f DEBT-IP-MIGRATION-NONETYPE **CHIUSO**

| | |
|--|--|
| Crash | `resolve_asset_by_ip_at(...).id` con return `None` |
| Perché | `elect_interface_primary` demoteva l’IP vecchio lasciando `last_seen` al first_seen → intervallo chiuso non copre T intermedio (`identity.py` pre-fix) |
| Fix | Alla demotion: `last_seen = now` se mancante/precedente (`identity.py` elect loop) — **non** una guardia che inghiotte la migrazione |
| Semantica | Detentore storico conserva categoria/evidenza; nuovo diventa current |

---

## D.3 — Registrazioni (nessuna correzione dati)

### D.3.1 DEBT-DOUBLE-CURRENT-IP

| ip | id / asset / source |
|----|---------------------|
| 192.168.1.2 | **3**/a2 mgmt + **153**/a2 fritz |
| 192.168.2.108 | **15**/a11 + **853**/a138 |

W3: regola di risoluzione **prima** del backfill. Non collassati.

### D.3.2 Cassiopea = debito chassis (W4a/W4b)

Asset 5 = NIC1 `.1.3` current · asset 6 = `.3.24` current. Ping `.3.24` fail = SPAN atteso. Test non-reg: un apparato, due iface, due IP current, un nome.

### D.3.3 Alembic

Unificato in **DEBT-ALEMBIC-BASELINE-LEGACY-TABLE** (observations droppata; alembic non in prod).

---

## D.4 — Test (nodi nominati)

| Nodo | Esito |
|------|-------|
| T-b dual_dedup entity_key | **PASS** |
| T-e printer IP migration | **PASS** |
| T-f ssdp IP migration | **PASS** |
| T-c ipp_precedence | **FAIL** (registrato DEBT-IPP-PRECEDENCE) |
| T-d snmp enrichment proposal | **FAIL** (stesso debito naming) |
| T-a fdb uplink portal | **FAIL** (DEBT-FDB-UPLINK-PORTAL) |
| D.0.b lift fritz active | **PASS** |
| `test_trust_converge.py` | **PASS** (tutti) |
| `test_mac_ip_policy.py` | **PASS** |

T-c/T-d **non** risolti da D.1 — non corretti in questa ondata.

---

## D.5 / D.6 — Deploy 0.10.45

### Previsioni (dichiarate prima)

| Metrica | Previsto |
|---------|----------|
| structural | 0 |
| needs_apply | false |
| T_backup | 0 |
| T_total regime | 8.8–9.0 s |
| assets / ip_current / NP | 151 / 100 / 412 |
| ie / ilp | 0 / 0 |
| observations | assente |
| AD_devices_active | **69** (finestra; non 82) |
| delta contatori da entity_key | **0** |

### Assert post-deploy (una riga)

`boot1 0.10.45: structural=0 needs_apply=false T_backup=0 T_total=9.043 · assets=151 ip_cur=100 NP=412 AD=69 ie/ilp=0/0 observations=absent · 116=fh/fh · entity_key_delta=0`

| Scarto | Spiegazione |
|--------|-------------|
| T_total 9.043 vs banda 8.8–9.0 | +0.043 s oltre il tetto; bootstrap wall 5.0 + uvicorn→ready ~4.0 — non structural/backup |
| AD 69 | coerente con previsione finestra |

**D.6:** `structural=0` → **DEBT-RECONCILE-CHURN-1 confermato CHIUSO**.

---

## Esito

| Gate | Stato |
|------|--------|
| T-b, T-e, T-f | verdi |
| D.0.b non assorbente | sì |
| D.6 structural=0 | sì |
| **Gate W2** | **SBLOCCATO** a livello debito T-b/T-e/T-f |

**STOP di questa ondata:** non si accendono i writer. Il prompt W2 arriva dopo review del diff (`obs-wd.diff.txt`). Motivo: con writers on, una `excl_key` sbagliata diventa dato persistito.

Rollback ammesso solo a **`v0.10.44`** (non 0.10.43).
