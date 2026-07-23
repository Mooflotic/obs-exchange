# OBS-OGGI-TRIAGE-031 — B2-ter (D9 + D10 + S1)

**Branch:**   
**Commit:**  ()`feature/oggi-triage-031`  
**VERSION:** 0.10.19 (invariata)  
**Deploy:** no — STOP review

Diff: `obs-exchange/main/obs-oggi-triage-031-b2ter.diff.txt`

---

## S1 — Simulazione selezione (sola lettura, selezione NON cambiata)

Picker attuale: `topPending` = max confidenza.  
Alternativa simulata: max `scoreSpecificity`, a parità max confidenza.

| | adotta | verifica | rumore | righe |
|--|-------:|---------:|-------:|------:|
| **Attuale** | 5 | 53 | 36 | 94 |
| **Simulata** | 6 | 67 | 25 | 98 |

- Righe/asset che cambiano proposta o azione: **28**
- Direzioni (azione attuale → simulata):
  - archivia→verifica **7**
  - archivia→adotta **1**
  - archivia→archivia (stesso gruppo, nome diverso) **3**
  - verifica→verifica **5**
  - (assente)→verifica **8** (alt più specifica apre riga dove top=nome attuale)
  - archivia→(assente) **3** / verifica→(assente) **1** (alt coincide col nome → riga sparisce)

### 10 esempi (nome attuale → top conf → alternativa più specifica)

1. LGS328C → Switch [dns 0.6 s2] → Switch Linksys [oui 0.4 s3]
2. SkyBooster1 TECNICO — mesh → Sky [oui 0.85 s2] → SkyBooster2 [dhcp 0.75 s3]
3. AppleTV Sala → AppleTV Sala [ai 0.92 s4] → Sala-TV-1p [dhcp 0.75 s5]
4. LSX → LSX [dhcp 0.75 s2] → KnOS/3.2 UPnP… [ssdp 0.6 s3]
5. Amazon Air Quality Monitor → Echo Cucina [ai 0.93 s4] → AmazonAQM-003Q [dhcp 0.92 s5]
6. FRITZ!Box 5690 Pro → FRITZ!Box [oui 0.85 s4] → Fritz-Master UPnP…5690… [ssdp 0.55 s5]
7. SkyBooster2 BIBLIO — mesh → Sky [oui 0.85 s2] → SkyBooster2 [dhcp 0.75 s3]
8. Citofono BTicino C3X → BTicino [oui 0.85 s2] → C3X-00-03-50… [dhcp 0.75 s5]
9. FRITZ!Repeater SalaPC → Fritz-SalaPC [dns 0.6 s2] → Fritz-SalaPC UPnP…6000… [ssdp 0.6 s5]
10. FRITZ!Repeater Cucina → Fritz-Cucina [dns 0.6 s4] → Fritz-Cucina UPnP…6000… [ssdp 0.6 s5]

**Materiale per D11** — nessuna modifica al picker in codice.

---

## Griglia live aggiornata (post B2-ter, dati dump live)

| Gruppo | N |
|--------|--:|
| adotta | **5** |
| verifica | **53** |
| · collide | **3** |
| · chassis | **23** |
| · manual-upgrade | **4** |
| · sotto-soglia | **23** |
| rumore (righe griglia = top) | **36** |
| **massa Archivia rumore (tutte le pending ≤ score)** | **192** |

Confirm se 192 > 36: «Archiviare 192 proposte su 67 asset (include proposte di secondo livello non visibili in griglia)?»

---

## Codice B2-ter

| ID | Cosa |
|----|------|
| D10 | `noiseProposalIds(assets, chassisPayload)` — tutte pending rumore; esclude chassis + ignorato |
| D9 | `splitVerifica` — collide / chassis / manual-upgrade / sotto-soglia |
| minor | notice azzerato su adopt/reject/archiveNoiseMass |
| debt | `DEBT-HABITS-DIR-UNAVAILABLE` in KNOWN_DEBT.md |

---

## Suite

```
node --test src/*.test.js     → 103 pass / 0 fail
pytest (ignore test_m6_m8*)   → 479 passed, 9 failed (preesistenti, fuori scope)
pytest collection full        → ERROR test_m6_m8_detectors_flow.py (int|None su py3.9, preesistente)
pytest test_reject_name_proposal.py → 5 passed
VERSION                       → 0.10.19
```

Fail pytest preesistenti (es. SSDP/printer alembic backup, IP unique, nmap dedup) — non introdotti da B2-ter.

---

## STOP

Review → GO esplicito per merge + deploy. Nessun bump VERSION.
