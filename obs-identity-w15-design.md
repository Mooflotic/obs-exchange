<!-- BLOCK-ID: OBS-IDENTITY-W15-DESIGN -->

# OBS-IDENTITY-EVIDENCE W1.5 — Design corretto (E/D) + IMPLEMENTATION

**VERSION:** 0.10.42 · **Base:** W1 0.10.41 chiusa · **W2 shadow writers:** 0.10.43

---

## Scala EVIDENCE

Livello = f(`fact_type`, `acquisition_method`, `source`, `subtype`, quals). Mai dal solo fact_type.

| Livello | Significato |
|---------|-------------|
| E0-unmeasured | misura non eseguita / fallita |
| E0-absent | misura eseguita, risultato negativo |
| E1-corroborant | OUI/vendor — non alza mai |
| E2-temporal | correlazione temporale / topologia degradata |
| E3-topological | co-osservazione porta **solo se** access misurata ∧ MAC count misurato ≤ soglia ∧ simultaneità |
| E4-mgmt | risposta mgmt-plane live che enumera entrambi |
| E5-bridge | bridge/VC (LLDP chassis-id subtype macAddress, bridge base MAC SNMP, LACP system ID) — **non** fonde membri fisici |
| E5-physical | serial/UUID ENTITY — consolida membri su conferma umana |

Esclusioni: MAC U/L; adiacenza blocco MAC (predicato assente); circolarità K7.

## Scala DECISION

| D | Effetto |
|---|---------|
| D0 | nulla |
| D1 | ipotesi interna |
| D2 | `IdentityLinkProposal(link_state=proposed)` |
| D3 | consolidabile **solo** su conferma umana |
| D4 | **non esiste** |

Mappa: E5-physical → D3; E5-bridge → D3 VC / D2 se contesto membri fisici; E4∧E3 → D2; E3/E2 → D1; E1/E0 → D0.

Link **non** transitivi. Relazione: `proven_same|proven_different|unresolved` (default unresolved).

## FSM ortogonali

- `evidence_state`: current|stale|superseded|absent_measured|absent_unmeasured  
- `link_state`: proposed|confirmed|rejected|retracted  
Decay evidenza **non** retrae `confirmed`.

## IMPLEMENTATION

| Path | Ruolo |
|------|-------|
| `api/app/identity_evidence/classes.py` | classify + max_decision |
| `store.py` | upsert idempotente, decay evidence-only |
| `linker.py` | propose-only, no transitivity, drop discordant physical |
| `decisions.py` | confirm/reject/retract audit |
| `mac_guards.py` | U/L only — zero adjacency |
| `circularity.py` | K7 |
| `presence.py` | direct/fdb_fresh/historical/absent_* |
| `tests/test_identity_evidence.py` | T1–T21 + schema parity |
| Alembic `n4e5f6a7b8c9_*` | parity; prod = create_all |

Writers ingest **spenti**. Nessuna scrittura Asset.
