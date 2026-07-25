<!-- BLOCK-ID: OBS-IDENTITY-W15 -->

# OBS-IDENTITY-EVIDENCE W1.5 — Report chiusura

**VERSION:** 0.10.42 · **Branch:** `feature/obs-currency` · **Base W1:** 0.10.41 chiusa

---

## Sequenza versioni

| Ondata | VERSION |
|--------|---------|
| W1 contratto/schema/resolver | 0.10.41 (deployata) |
| **W1.5 identity-evidence** | **0.10.42** |
| W2 writer shadow | 0.10.43 |
| W4a / W4b / W5… | 0.10.44+ |

---

## Fase 1 — Review D1–D18

Pubblicato: `obs-identity-w15-review.md` (curl 200).  
Difetti PRESENTE corretti in Fase 3 (E/D, subtype LLDP, U/L, K7, FSM ortogonali, no adjacency, no auto-merge, absent_measured/unmeasured, proven_* / unresolved, member_id, schema parity test).

## Fase 2 — Diagnosi

Pubblicato: `obs-identity-w15-diagnosi.md`.  
`:05`/`:08` = sola storia · SNMP timeout = unmeasured · chassis_id auto **non** evidenza · K1: identity fuori colonne Asset reconcile.

## Fase 3 — Correzione

Package `api/app/identity_evidence/` riscritto su scala E0–E5 / D0–D3.  
Test **T1–T21 + schema parity: 22 passed**.

## Fase 4 — Gate pre-deploy

| Gate | Esito |
|------|-------|
| G1 Review + diff correzione | OK |
| G2 Suite T1–T21 | **22 passed** (asserzioni esplicite, non conteggio) |
| G3 No writer attivo / no adjacency / no chassis self-evidence | OK (confirm solo in `decisions.py` su azione umana) |
| G4 I6 `scoreSpecificity\|specificity` in api/ | **VUOTO** |
| G5 Parità schema create_all | test_schema_parity OK; alembic non gira in prod |
| G6 No write Asset/reconcile fields | OK (store separato) |
| G7 Previsioni (sotto) | dichiarate **prima** del deploy |

### G7 PREDICTIONS (pre-deploy)

| Metrica | Valore esatto atteso |
|---------|----------------------|
| `identity_evidence` rows | **0** |
| `identity_link_proposals` rows | **0** |
| Delta DB | ≈ schema vuoto only |
| `T_total` regime | **8.8–9.0 s** |
| `needs_apply` | **false** |
| `T_backup` | **0** |
| `name_proposals` | **412** (invariato) |
| assets / AD / ip_current | **151 / 82 / 100** |
| `:05`/`:08` proposte consolidabili | **0** |
| fusione ch23/ch24 | **nessuna** |
| LGS310C name | **invariato** (pin manuale non toccato dal codice W1.5) |

## Fase 5 — OBSERVED

_TBD post-deploy._

## Rollback

`git revert` bump + deploy tag `v0.10.41`. Schema identity inerte: non rimuovere in fretta.
