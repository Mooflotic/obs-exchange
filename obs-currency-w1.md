<!-- BLOCK-ID: OBS-CURRENCY-W1 -->

# OBS-CURRENCY — W1 Contratto, schema, resolver

**VERSION:** 0.10.41 (deployata · chiusa) · **Branch:** `feature/obs-currency`  
**Scope:** fondamenta only — nessun writer ingest, nessun consumatore, nessuna scrittura Asset.name  
**Sequenza:** W1 → **0.10.41** · W1.5 identity-evidence → **0.10.42** · W2 shadow writers → **0.10.43**

---

## Deliverable

| Componente | Path |
|------------|------|
| Registro fatti | `api/app/facts/registry.py` |
| Resolver R-A..R-H | `api/app/facts/resolver.py` |
| Modello | `FactAssertion` in `api/app/models.py` |
| Alembic (coerenza, non prod) | `m3d4e5f6a7b8_fact_assertions.py` |
| Test | `tests/test_facts_resolver.py` (13 test) |

---

## PREDICTIONS (pre-deploy)

| Metrica | Valore atteso |
|---------|---------------|
| `fact_assertion` rows | **0** |
| Delta dimensione DB | **≈ 0** (solo schema vuoto) |
| `T_total` regime avvio | **8.8–9.0 s** (in banda) |
| `needs_apply` | **false** |
| `T_backup` | **0** |
| `name_proposals` | **412** (invariato — W1 non tocca la coda) |
| assets / AD / ip_current | **151 / 82 / 100** |
| `observations` legacy | **assente** |
| scans | **available=false** (metrica storica 68 ≠ `scan_runs` live; non ridefinita) |

---

## OBSERVED (post-deploy · regime)

**Misura:** 2026-07-25 ~20:03 Europe/Rome · health `0.10.41` · boot dopo settle trust (`needs_apply=false` pre-restart)

| Metrica | Predetto | Osservato | Esito |
|---------|----------|-----------|-------|
| VERSION | 0.10.41 | **0.10.41** | OK |
| `fact_assertions` | 0 | **0** | OK |
| `T_total` | 8.8–9.0 | **8.879** | OK |
| `needs_apply` | false | **false** | OK |
| `T_backup` | 0 | **0.0** | OK |
| `needs_backup` | false | **false** | OK |
| assets | 151 | **151** | OK |
| AD (`trust_level=confirmed_present`) | 82 | **82** | OK |
| ip_current | 100 | **100** | OK |
| name_proposals | 412 | **412** | OK |
| `observations` in sqlite_master | assente | **assente** | OK |
| dual-write | spento | **nessuna setting/env dual-write attiva** | OK |
| indice `uq_fact_assertions_current_slot` | UNIQUE WHERE state=current | **presente** | OK |
| scans | available=false | **available=false** (`scan_runs` live ≠ 68) | OK (non ridefinito) |

**Nota boot1 post-deploy:** primo avvio post-install aveva `needs_apply=true` / `T_backup≈80–83s` / `structural≥1` (settle trust). **Non** è il regime di assert. Regime = restart successivo a dry_run con `needs_apply=false`.

Fragment regime:
```json
{"needs_backup": false, "needs_apply": false, "T_trust": 0.088, "T_backup": 0.0, "T_apply": 0.0}
```
`T_total=8.879` da riga `[timing]` lifespan.

---

## Regole implementate (resolver)

| Regola | Comportamento |
|--------|---------------|
| R-A | Stesso `value_norm` + stessa `excl_key` → refresh `last_seen_at`, nessuna nuova riga |
| R-B | Supersession atomica: incumbent `superseded` poi nuova riga `current` |
| R-C | Evidenza debole → riga `historical`/`reason=weak_evidence`, incumbent invariato |
| R-D | `manual` non sovrascrivibile da sorgenti automatiche |
| R-E | `ttl_window=None` → nessuna scadenza; altrimenti `stale` oltre finestra |
| R-F | Riammissione = nuova riga; cooldown anti-flap 4h |
| R-G | Assente → `None` (I2) |
| R-H | Contraddizione tipizzata (es. Android↔Windows) → `CONFLICT-REVIEW`, current invariato |

---

## Verifica indice parziale (post-boot)

```python
import sqlite3
con = sqlite3.connect("/data/db/observatory.db")
print(con.execute(
    "SELECT sql FROM sqlite_master WHERE name='uq_fact_assertions_current_slot'"
).fetchone()[0])
con.close()
```

Atteso: `UNIQUE ... WHERE state='current'`. **Verificato in prod.**

---

## Test unitari

```bash
python3 -m pytest tests/test_facts_resolver.py -q
```

Risultato: **13 passed** (pre-deploy; invariati).

---

## Chiusura

W1 **CHIUSA**. Prossima ondata: **W1.5 OBS-IDENTITY-EVIDENCE → 0.10.42** (non W2). W2 shadow writers → **0.10.43**.
