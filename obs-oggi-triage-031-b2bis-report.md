# OBS-OGGI-TRIAGE-031 — B2-bis + ricognizioni

**Branch:** `feature/oggi-triage-031`  
**Commit:** `d5c7da9` — fix(oggi): notice massa + sort fallback reject (B2-bis)  
**VERSION:** 0.10.19 (invariata)  
**Deploy:** no (STOP review)

Diff: `obs-exchange/main/obs-oggi-triage-031-b2bis.diff.txt`

---

## R1 — Proposte multiple (DB live, sola lettura)

| Metrica | Valore |
|---------|--------|
| NameProposal pending TOTALI | **379** |
| Asset distinti con ≥1 pending | **141** |
| Asset con 1 pending | **34** |
| Asset con 2 pending | **30** |
| Asset con 3+ pending | **77** |

Gruppo rumore UI (36 righe):

| | |
|--|--|
| Asset rumore con >1 pending | **35** / 36 |
| 2ª proposta ancora rumore (solo D3 score) | **27** |
| 2ª proposta non-rumore | **8** |
| mass_eligible | **36** |
| rumore senza proposal_id | **0** |

**Implicazione:** «Archivia rumore (N)» rifiuta solo la top proposal. Molte 2ª pending rientrano in coda; **8** di quelle non-rumore possono uscire dal gruppo rumore. Archivia massa **non** svuota definitivamente il gruppo finché restano altre pending sullo stesso asset.

D9 (sotto-gruppi Verifica): in attesa decisione Michele — non implementato in B2-bis.

---

## R2 — Direzione Abitudini (raspberrypi.org, sola lettura)

Destinazioni: `raspbian.raspberrypi.org`, `archive.raspberrypi.org`.  
Asset «Raspberry Pi» per nome esatto: nessuno (simili: Openhab Pi, Allsky, ropieee). Flussi verso quelle host: **2**, entrambi **prima del 2026-07-23**, `byte_layer=null`, senza `bytes_out`/`bytes_in`.

Dopo cutoff globale: layer `app` / `ip` / `mixed` hanno lo split direzione valorizzato.

**Verdetto: (a) solo storico pre-pipeline** — non (b) ramo `byte_layer='ip'` che perde lo split. Nessuna correzione.

---

## B2-bis — Emendamento (E1–E4)

| ID | Cosa |
|----|------|
| E1 | `notice` distinto da `error`; non azzerato da `load()`; `role=status` tono neutro; sempre «Archiviate N» (+ saltate / non trovate) |
| E2 | Se massEligible < rumore: «N senza id proposta, escluse» accanto al pulsante |
| E3 | `newest_name_proposal`: date None → `datetime.min` + tie-break `id` |
| E4 | Test web (notice sopravvive a load) + API sort fallback |
| D9 | Non toccato |

### Test

```
pytest tests/test_reject_name_proposal.py → 5 passed
node --test oggiTriage + triageRules → 21 pass / 0 fail
```

### File toccati

- `web/src/views/Oggi.vue`
- `web/src/oggiTriage.js` / `.test.js`
- `api/app/routers/assets.py` (`newest_name_proposal`)
- `tests/test_reject_name_proposal.py`

---

## STOP

Review → GO esplicito per merge/deploy. Nessun bump VERSION, nessun deploy.
