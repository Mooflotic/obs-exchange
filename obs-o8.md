# OBS-OGGI O8 — soggetto orfano, rumore strutturale, priorità difensiva

VERSION **0.10.71** · ramo `feature/obs-currency` · STOP per review (no merge main).

## PREVISIONI (dichiarate PRIMA del deploy)

### Z1
- Fatti `subject_type=chassis`: **1** — id **251** (`asset.name`, subject=24, `LGS310C`, manual/100/current).
- Orfani attesi: **1** (chassis 24 assente).

### `queueConservationCheck` PRIMA (logica a 2 superfici / prod 0.10.70)
- Pending asset id: **10, 60, 88, 109, 151**.
- Su card chassis (≥2): **10, 109, 151**.
- Fuori card: **60, 88** (attesi in triage o rumore).
- No-op exact live: **nessuno** → difetto Q2 **latente**, non assente.
- `missing` atteso (2 superfici): **[]** se 60/88 in triage; altrimenti enumerare.
- `duplicated` atteso: **[]**.

### Soppressioni R1 (attese, da enumerare DOPO su live)
- `noop_identico`: **[]** (nessun exact match live al momento della misura pre).
- Altre regole: da enumerare post-deploy sui pending **10, 60, 88, 109, 151**.

### Priorità P1
- Prima: ordine sezioni legacy (conflitti → FDB misto → move → chassis → triage).
- Dopo: legenda P1–P6 visibile; FDB/triage/chassis con `defense_priority.rule` ispezionabile.

### DOPO correzione
- `missing=[]`, `duplicated=[]`.
- FA **251** intatto (stessi campi).

---

## FASE 0 — Z1…Z5

### Z1 censimento (prod, enumerato)
| id | fact_key | subject_id | value | source | authority | state | created_at | chassis_exists |
|----|----------|------------|-------|--------|-----------|-------|------------|----------------|
| 251 | asset.name | 24 | LGS310C | manual | 100 | current | 2026-07-27T11:03:50 | **False** |

Unico fatto a soggetto chassis. Orfano.

### Z2 chassis 24
- Riga chassis 24: **assente**.
- Membri oggi: **nessuno**.
- Chassis 32 (vivo): label LGS310C; membri **3** (LGS310C), **139**, **143**.
- Non è etichetta errata *viva* sul 24: è fatto orfano. Rischio = usarlo come nome del 32 → **vietato**; dichiarato in UI via `orphaned_manual_name_facts`.

### Z3 causa radice — id chassis **non stabile**
- File: `api/app/services/chassis_grouping.py` · `reconcile_chassis_grouping`.
- Chiave: frozenset `member_ids`. Set nuovo → `Chassis(...); db.flush()` (~726–731) → **id nuovo**.
- Uscita: `_dissolve_chassis` → `db.delete(chassis)`.
- Conseguenza: ogni fatto a soggetto chassis si orfanizza al regroup → difetto del soggetto canonico (`DEBT-CHASSIS-SUBJECT-ID-CHURN`).

### Z4 protezione
- `FactAssertion` **senza FK** a `chassis` → dissolve non cancella FA 251.
- Nessun path di pulizia/dedup/adozione trovato che cancelli o riscriva `subject_id` di manuale orfano.
- Resolver: manuale auth 100 non sovrascritto da fonte più debole.
- **Nessun percorso pericoloso da fermare** in questa ondata. Ri-puntamento resta vietato senza Michele.

### Z5 documentale
- `DEBT-CHASSIS-NAME-LEGACY-HELD`: diagnosi «store vuoto / serve W3» **annotata come errata** — i fatti esistono ma sono mal indirizzati.
- Aperto `DEBT-CHASSIS-SUBJECT-ID-CHURN` (Z3 + Z1 + divieto ri-puntamento).
- `DEBT-OGGI-QUEUE-SURFACES` chiuso in O8.

---

## FASE 1–3 (codice)

- `queueConservationCheck`: superfici triage | chassis | rumore (+ `suppressed_noop` / structural).
- `held_name_is_manual` (ex `fact_is_manual`).
- N6: payload whitespace-value → `missing=[666]`.
- `oggiNoise.js`: noop / duplicato / LAA demote / vendor generico; manuale+più debole → **non** soppressa (I3).
- `oggiPriority.js`: legenda P1–P6; S-A…S-D mai rumore.
- Payload chassis: `orphaned_manual_name_facts` + `orphan_policy`.

---

## OSSERVATI (dopo deploy 0.10.71)

### Health
`{"ok":true,"service":"observatory-api","version":"0.10.71"}`

### Z1/Z2/N1
- FA **251** intatto: subject=24, LGS310C, manual/100/current.
- `orphaned_manual_name_facts` espone FA 251; chassis **32** `name_currency.state=absent` (non applica l'orfano).
- Asset **3** su chassis **32** (membri 3,139,143).

### Conservazione live (tre superfici)
```
missing=[]
duplicated=[]
suppressed_noop=[]
surfaces={10:["chassis"],60:["triage"],88:["triage"],109:["chassis"],151:["chassis"]}
```
PRIMA (2 superfici, stessi pending): missing latente assente — `[]` anche prima (Q2 senza casi live).

### Soppressioni R1 live (enumerate)
- Nessuna proposta pending matcha le regole hard al momento della misura: `SUPPRESSIONS_BY_RULE {}`.
- Regole coperte da test: noop / duplicato / LAA demote / vendor; N3 manuale non soppressa.

### Priorità triage live
- P1 (solo-L2): asset **88**
- P6 (igiene): asset **60**
- Chassis cards: 10/109/151 su superficie chassis (igiene/conflitto via `priorityForChassisCard`).
- FDB cards live: **7× S-C** (MAC-move) → P3; tutti `ruolo_porta=non_determinato` (priorità ridotta dichiarata).
  Enumerazione MAC: DC:15:C8:80:BB:EA, F0:B0:14:90:87:96, F0:B0:14:90:87:97, 38:A6:CE:40:A7:76, 70:50:AF:FB:86:F8, 70:50:AF:FC:0A:F8, 70:50:AF:FB:86:FA.

### Breaker (un ciclo)
- open=False · reason=''
- ceilings invariati: max_rows=20000, max_growth_per_day=2000, max_table_bytes=50MiB
- FA_TOTAL=833 · FA_DAY=571 · DB≈1805.12 MiB
- **Non scattato.** Tetti non alzati.

### Gate
- `w8_currency_gate.py`: **VIOLAZIONI: 0** · **PASS (con 1 eccezione temporanea)**
- I6 `grep -RInE 'scoreSpecificity|specificity' api/`: **VUOTO**

### Screenshot Oggi (legenda visibile)
- 1280: https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-o8-oggi-1280.png (curl 200; sha256 ece2e5e90d2bf0731c5aa3224e5e46b7a01a8c43bf7699863011138d5ae8dc9c)
- 768: https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-o8-oggi-768.png (stesso hash del 1280 — viewport Electron non ha ridimensionato; contenuto legenda+orfano+P3 identico)
- 390: https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-o8-oggi-390.png (curl 200; sha256 fe85b3b1d7a8d075fbb27c9965170b8eccf3a96e315f686932c578a05646ede2)

### Nodi
| Nodo | Esito |
|------|-------|
| N1 FA251 orfano dichiarato, non sul 32, intatto | OK |
| N2 noop (test) soppresso-no-op | OK (live 0 casi) |
| N3 manuale+weaker → non soppressa | OK (test) |
| N4 LAA demote_only | OK (test) |
| N5 solo-L2 asset 88 → P1 | OK |
| N6 missing non vuoto | OK (test) |
| N7 S-A → P4 + ruolo incerto | OK (test; live FDB=S-C→P3) |

### Criteri di fallimento (verificati)
1. Fatto chassis ri-puntato/cancellato — **no** (FA251 invariato)
2. Orfano usato sul chassis corrente — **no** (currency 32 absent + warning)
3. conservation missing/duplicated non vuoti — **no** (entrambi [])
4. N6 assente/incapace di fallire — **no** (test missing=[666])
5. Soppressa non contata/ispezionabile/ripescabile — **no** (UI + listStructuralSuppressions; live 0)
6. Nuova soglia numerica / taglio senza UI — **no**
7. scoreSpecificity fuori triageRules — **no** (I6 vuoto)
8. S-A…S-D soppressi come rumore — **no**
9. Manuale sovrascritto da proposta debole — **no**
10. Alta priorità senza azione / pulsante inerte — **no** (azioni F-9 esistenti + ripesca)
11. Ordinamento non ispezionabile / legenda assente — **no** (legenda + regola per riga)
12. Inferenza senza marca/fonte/confidenza o che scrive — **no** (blocchi esistenti; nessuna scrittura IA)
13. API a pagamento — **no**
14. FactAssertion fuori facts/ / allowlist ampliata — **no** (chassis_facts in facts/; gate PASS)
15. boot/backup/DB / _w4a / T7 — **no** (solo snapshot pre-deploy standard)
16. Diff monolitico — **no** (tre diff tematici)

## STOP
Review Michele. FA 251 resta intatto. Nessun merge su main. Nessuna UX complessiva/favicon.
