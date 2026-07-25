# OBS-TRUST-CONVERGE — gerarchia `operational_state` + fix ping-pong

**VERSION:** 0.10.28 · **Branch:** `feature/obs-db-slim` · **Data:** 2026-07-25  
**Premessa:** `structural=53` è **preesistente** (0.10.25 / 0.10.26 / 0.10.27). Non è regressione 3b-iii.

---

## FASE A — Diagnosi (sola lettura)

### A.1 Writer di `operational_state`

| Writer | file:riga | Regola | Quando |
|--------|-----------|--------|--------|
| `observe_portal` | `trust.py:69` | se `inventory_hidden_auto` → `active` + unhide | ingest portal (ciclo collector / materialize) |
| `_apply_trust_plan` | `trust.py:565` | level=`fritz_historical` → op=`fritz_historical` + hide | bootstrap trust apply |
| `_apply_trust_plan` | `trust.py:576` | level=`stale_unlocated` → op=`stale_unlocated` + hide | bootstrap trust apply |
| `_apply_trust_plan` | `trust.py:587` | level∈{known,confirmed_present} e `inventory_hidden_auto` → `active` + unhide | bootstrap trust apply |
| `reconcile_asset_presence` | `inventory.py:252/273` | evidenza → `stale_unlocated` o `active` (ora gated) | collector `/fdb-reconcile`, materialize, UI assets |
| merge infra | `identity.py:557` | duplicato → `archived` | reconcile infrastruttura |

Letture sole: `assets.py`, `dashboard.py`, `topology.py`, `monitoring.py`, `ai.py`.

### A.2 I 53 asset (id espliciti)

| Gruppo | n | ids |
|--------|---|-----|
| known → expected active | 23 | 71, 80, 81, 87, 89, 90, 91, 93, 94, 96, 97, 99, 100, 101, 102, 103, 104, 105, 107, 108, 111, 113, 150 |
| fritz_historical → fritz_historical | 24 | 83, 84, 86, 92, 95, 106, 116, 117, 118, 119, 120, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134 |
| stale_unlocated → stale_unlocated | 6 | 138, 139, 142, 143, 144, 146 |

Pattern live: `trust_level` **già** uguale a `level` del piano (`trust_eq_false=0`); mismatch **solo** su `operational_state` (`state_eq_false=53`). Ultimo writer effettivo sul DB live = **inventory** (stato post-ciclo collector).

### A.3 Decisione: **(a) PING-PONG REALE**

Prova nested (rollback, zero commit) su API live 0.10.27:

| Step | Risultato |
|------|-----------|
| t0 live | 53 mismatch op_state |
| t1 dopo `_apply_trust_plan` | **53/53** allineati a expected; `identical_rewrite=0` → **non (b)** |
| t2 dopo `reconcile_asset_presence` | **53/53** di nuovo mismatch; `inventory_undid_count=53` |

Undo patterns:
- known: active → stale_unlocated (23)
- fritz_historical: fritz_historical → stale_unlocated (23) o active (1)
- stale_unlocated: stale_unlocated → active (6)

**Implicazione:** ogni boot rifà apply + backup (~155 s); churn WAL su `assets.meta` ogni ciclo presence.

### A.4 Premio

Da boot1 0.10.27: `T_total=174.1`, `T_backup=155.3`, `T_apply=3.648`, `T_dry_run=0.086`.

Con `structural=0` → `needs_apply=false` → backup saltato → apply saltato:

`T_total_atteso ≈ 174.1 − 155.3 − 3.65 ≈ **15 s**` (ordine ~20 s con residuo bootstrap).

### A.5 Ipotesi A10 / pressione scrittura — **REGGE**

- `obs` ultimi 10 min: **0** insert (dual-write spento); baseline pre-3b-iii Δ=+1465/10min ≈ **2.4 righe/s** sulla tabella dominante.
- `Connection.backup()` senza `pages=` (backup.py:96) ricopia pagine sporcate dai writer concorrenti.
- Con observations quasi ferma, meno ricopie → T_backup 307.9 → 155.3 → 129.3 non è «page cache» (già falsificato a P2): è **minore pressione di scrittura**.
- Guadagno reale 3b-iii su boot con needs_apply: **T_total ~174 s vs ~348 s** (~174 s), non i soli ~20 s del prefetch.

---

## FASE B — Gerarchia (forma richiesta)

```
archived (identity merge) >
  trust_quarantine (op_state=fritz_historical | trust_level=stale_unlocated) >
    trust_protected (known | confirmed_present) >
      inventory_presence (active ↔ stale_unlocated)
```

Implementazione: `inventory_may_set_operational_state` in `inventory.py`. Inventory **cede** quando la scrittura annullerebbe il verdetto trust; non inventa stati.

Vietato (non fatto): V1 filtrare contatore, V2 skip apply, V3 default plausibile, V4 AD/scans/dual-write, V5 Alembic.

---

## FASE C — Gate equivalenza C.1

Stato live PRIMA → DOPO fix (valore corretto per gerarchia). Tutte le 53 differenze ammesse:

| id | trust | op prima | op dopo (fix) | causa |
|----|-------|----------|----------------|-------|
| 71,80,81,87,89,90,91,93,94,96,97,99–105,107,108,111,113,150 | known | stale_unlocated | **active** | trust_protected: known resta visibile |
| 83,84,86,92,95,106,117–134 | fritz_historical | stale_unlocated | **fritz_historical** | trust_quarantine: no smash inventory |
| 116 | fritz_historical | active | **fritz_historical** | trust apply riallinea label |
| 138,139,142,143,144,146 | stale_unlocated | active | **stale_unlocated** | trust_quarantine hide; no auto-unhide |

Nessun asset resta congelato nello stato sbagliato rispetto alla gerarchia.

### Test (py3.9 locale `.venv`)

`pytest tests/test_trust_converge.py tests/test_inventory_reachability.py` → **15 passed**.  
Suite completa: non dichiarata verde (DEBT-PYTEST-COLLECTION-PY39 possibile su collection ampia). Eseguito sottoinsieme converge+inventory.

### C.3 Rollback

Snapshot pre-deploy di `deploy.sh`: `data/backups/pre-deploy-<ts>.db`.

```bash
# integrity_check sola lettura
sqlite3 data/backups/pre-deploy-YYYYMMDD-HHMM.db 'PRAGMA integrity_check;'
# ripristino (FERMA api prima; non eseguito qui)
# cp data/backups/pre-deploy-….db data/db/observatory.db
```

---

## Previsioni pre-deploy 0.10.28 (immutabili dopo il lancio)

| ID | Previsto | Bloccante |
|----|----------|-----------|
| D1 | health 0.10.28 | sì |
| D2 | structural boot1 < 53 | sì |
| D3 | boot2 e boot3 structural ≈ 0, stabili | sì |
| D4 | structural=0 → needs_apply=false → T_backup≈0, T_total~15–25 s | sì |
| D5 | AD=82, scans=67, asset=151, ip=99 | sì |
| D6 | Δ observations/10min = 0 | sì |
| D7 | T_prefetch_obs null, T_dry_run < 2 s | sì |
| D8 | nessun op_state peggiore vs C.1 | sì |
| D9 | serie throughput aggiornata | no |
