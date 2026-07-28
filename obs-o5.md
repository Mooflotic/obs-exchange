# OBS-MAPPA O5 — bonifica O4 + Impianto operativo (0.10.68)

**Ramo:** `feature/obs-currency` · **STOP per review** · no merge · no 308/Dossier/UX

---

## Hotfix cutoff (da deploy, non stimato)

`observatory-api-1` **StartedAt = `2026-07-28T22:01:43.153510797Z`**  
(fonte: `docker inspect`; backup `pre-deploy-20260729-0000.db`; hotfix `./scripts/deploy.sh api`)

Predicato F0.1: `fact_key='port.fdb_mac' AND state='superseded' AND reason='mac_move' AND created_at < 2026-07-28T22:01:43Z`

---

## Previsioni pre-bonifica / pre-deploy

| Voce | Atteso |
|------|--------|
| F0.1 count | **396** · first20 ids `263..282` |
| `port.fdb_mac` pre-O4 | **0** |
| FA total before=after | identico |
| current `port.fdb_mac` | identico (O4 diceva 135; al momento bonifica **132** — scarto poll) |
| F0.4 no-baseline | O4 diceva 86; al momento **83** |
| non_coperta GS308EP | port_id **39..46** |
| solo-L2 (O4 card) | 10 MAC; su mappa anche duali uplink |

---

## F0 — Bonifica (osservati)

**Backup:** `/data/backups/o5-pre-bonifica-20260728-222020.db` · size 1892810752 · `PRAGMA integrity_check=ok`  
(host: `/volume1/Docker/observatory/data/backups/o5-pre-bonifica-20260728-222020.db`)

| Check | Prima | Dopo |
|-------|------:|-----:|
| FA total | 799 | **799** |
| port.fdb_mac current | 132 | **132** |
| marked defect | — | **396** `o4_defect_concurrent_presence_move` |
| baseline_reconstructed | — | **83** |
| baseline verified | 49 | 49 |

First 20 defect ids: `263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282`

**Nessuna DELETE.** Consumatori escludono le marcate e UI mostra conteggio + `DEBT-O4-SPURIOUS-MOVES`.

### Binding ricostruiti (83) — qualità inferiore, non S-A
Elenco completo nel report apply JSON; esempi: port **9** `50:99:5A:6E:EA:37`, port **33**/`21` duali `D4:52:EE:C3:25:16/17`, molti su port **36** (uplink). UI: «presente alla ricostruzione del \<ISO\>; storia precedente non disponibile».

---

## M1 — Diagnosi Impianto / Topologia (pre-fix)

| Difetto | Cosa mostrava | Cosa deve | File |
|---------|---------------|-----------|------|
| Ruolo porta legacy / override | badge ruolo senza regola FDB strutturale | `ruolo_porta` + regola `link_to_port_id` / ⊇ / non_determinato | `Plant.vue`, `fdb_defense.classify_port_roles` |
| MAC solo snapshot `observed_macs` | lista grezza, no solo-L2/LAA/baseline | binding fact + marker | `GET /api/fdb-defense/plant` |
| Stati vuoti confusi | «free» / non_coperta mescolati | tre stati I2 distinti | `plantFdb.js`, Plant |
| Link 36↔21 | meta auto_links / non evidenziato | link fatto disegnato | plant `links[]` |
| Ricerca «dove sta?» | solo `?asset=` | MAC/IP/nome + highlight | Plant ops |
| Topologia | GS308EP card OK; non consuma plant FDB | fuori scope O5 oltre coerenza I7 | `Topology.vue` (non riscritta) |

---

## Osservati mappa (JSON plant)

- **M-T1:** port **21**/**36** `uplink` rule=`link_to_port_id→…`; link `328c:21 ↔ 310c:8`
- **M-T2:** non_coperta ids **39,40,41,42,43,44,45,46**
- **M-T3:** `D4:52:EE:C3:25:16` su port **33** (`310c:5`) solo-L2 + inferenza
- **misurata senza dispositivi:** ids `4,5,7,10,11,13,18,19,20,25,26,27,28,29,37,38` (n=16)
- **non_fresca:** nessuno al ciclo misura
- **discarded_moves.count:** 396

### Solo-L2 (enumerati)
`(2,328c:2,DC:15:C8:80:BB:EA)` `(2,F0:B0:14:90:87:96)` `(2,F0:B0:14:90:87:97)` `(6,38:A6:CE:3E:9C:A8)` `(9,38:A6:CE:40:A7:76)` `(12,70:50:AF:FB:86:F8)` `(14,70:50:AF:FC:0A:F8)` `(16,38:A6:CE:3E:9C:AE)` `(21,… duali uplink)` `(33,310c:5,D4:52:EE:C3:25:16/17)` `(36,uplink mirrored)`

---

## Breaker post-bonifica

FA **799** · defect **396** · current **132** · fact_assertions table ≈0.3 MiB (pre) · breaker **closed** · tetti non alzati.

---

## Gate

```
python3 scripts/w8_currency_gate.py → PASS (1 temporanea), 0 violazioni
grep -RInE 'scoreSpecificity|specificity' api/ → VUOTO
```

Test: `test_o5_bonifica.py` + `test_o4_fdb_defense.py` + `plantFdb.test.js`.

---

## Criteri di fallimento

| Criterio | Esito |
|----------|-------|
| DELETE fact_assertions | **no** |
| FA / current cambiati da bonifica | **no** (799/132) |
| scartati spariti senza spiegazione | **no** — banner 396 + debito |
| reconstructed = verified | **no** |
| non_coperta = senza dispositivi | **no** — label distinte |
| FDB inventato GS308EP | **no** |
| ruolo da conteggio | **no** |
| inferenza senza fonte / azione auto | **no** |
| API a pagamento | **no** |
| azione inerte | **no** — dossier/ack/ignore |
| FactAssertion fuori facts/ / allowlist | **no** — logica in `facts/o5_bonifica.py` |
| diff monolitico | **no** — 3 diff tematici |

---

## Deliverable

- `obs-o5.md` (questo)
- `obs-o5-bonifica.diff.txt`
- `obs-o5-o4hotfix.diff.txt`
- `obs-o5-mappa.diff.txt`
- screenshot `obs-o5-mappa-<breakpoint>.png`

STOP.
