# OBS — W8-fix2b · completamento T7: controllo negativo corretto + handoff NAS

Ramo `feature/obs-currency` · prod **0.10.63** (nessun bump, nessun deploy, nessun
tocco a `api/app/**`/`web/src/**`). Read-only. Previsioni **già pinnate** in
`obs-w8fix2.md` §T5 (NON modificate): qui si citano.

**DIVIETO OUTPUT NON-ESEGUITO rispettato:** ogni campo che richiede il NAS è
`<non eseguito>`. Nessun blocco NAS è ricostruito.

## Conteggio righe artefatti (wc -l)

| Artefatto | righe |
|---|---|
| `obs-w8fix2b.md` | 189 |
| `w8fix2b_g8_equivalence.py` | 233 |
| `KNOWN_DEBT.md` | 447 |
| `obs-w8fix2.md` | 248 |

---

## T7.1 — Dichiarazione di accesso

**RAMO B — NON ho accesso al NAS.**

```
STOP-PRODUZIONE-NON-DISPONIBILE: T7 non eseguibile da me; comandi pronti per Michele.
```
Completo T7.0 (in mio potere) e mi fermo. I campi NAS restano `<non eseguito>` fino
al paste di Michele (T7.5).

---

## T7.0 — Correzione del controllo negativo (eseguita)

**a) Rimosso il caso speciale tautologico** in `_classify`: eliminate le due righe
`if consumer == MUTATE_SENTINEL: return "DIVERGE"`. La classificazione ora deriva
**solo** dal confronto `r`/`consumer`:
- `r!=None e consumer==r` → RESOLVER
- `r==None e consumer!=None` → FALLBACK
- `r==None e consumer==None` → ABSENT
- altrimenti (r!=None, consumer!=r) → DIVERGE

Nel probe il monkeypatch fa restituire alla presentazione la sentinella (consumer≠R),
quindi il DIVERGE nasce dal confronto reale, non da un caso speciale.

**b) Pre-condizione esplicita del probe** (prima di iterare gli asset): risolve
`R = current(db, *subject_of("asset.name", asset<id>), "asset.name")`. Se `R is None`
stampa `MUTATE-PROBE NON VALIDO: … non ha asset.name corrente …` ed **esce 2**; se
`R!=None` stampa `MUTATE-PROBE pre-condizione OK: id=<id> R=<valore>` e prosegue.

**c)** Nessun altro cambiamento: `run_fact`, le tre leg, gli import, la gestione della
transazione (`db.rollback()` finale) sono invariati.

**d)** Aggiunto `DEBT-G8-ENDPOINT-LEG-UNEXERCISED` in `KNOWN_DEBT.md`: la leg endpoint
resta SKIP (token = credenziale di sessione, STOP legittimo); su prod la discriminazione
di G8 poggia sul solo mutate-probe (leg `asset.name` tautologica T1, leg `os.guess`
prevista vacua T5a). Vietato dichiarare G8 «copertura completa».

**e)** Aggiunta la riga **K4** in `obs-w8fix2.md` §T6: SELFTEST/2 verifica `validate_temp`
su dizionari sintetici e **non** esercita il ramo `return 1` di `run_repo`.

`py_compile` su `scripts/w8_g8_equivalence.py`: **OK**. Il controllo negativo end-to-end
(probe che produce DIVERGE=1) si esercita **sul NAS** (dati reali): `<non eseguito>` in
RAMO B.

### Riesecuzione locale del currency-gate (in mio potere, output reale)

`python3 scripts/w8_currency_gate.py --selftest`
```
SELFTEST/1 corpus principale: atteso 3 violazioni ['file2_rawsql.py', 'file3_filterby.py', 'file4_count.py'] + 1 accounted
SELFTEST/1 osservato: 3 violazioni ['file2_rawsql.py', 'file3_filterby.py', 'file4_count.py'] + 1 accounted + 0 temporanee
SELFTEST/1: PASS
SELFTEST/2 config-check temporanee: atteso 1 errore (debt vuoto) + 0 (debt valido)
SELFTEST/2 osservato: 1 errore(i) debt-vuoto + 0 debt-valido
SELFTEST/2: PASS

SELFTEST: PASS (il gate sa fallire e valida le temporanee)
```
exit=0.

`python3 scripts/w8_currency_gate.py` (repo)
```
file scansionati: 175
voci allowlist: permanenti 17 · temporanee 1

ATTENZIONE — ECCEZIONI TEMPORANEE CON DEBITO APERTO: 1
  TEMP scripts/wp_gate.py:103 (atteso 1, osservato 1) debt=DEBT-WPGATE-CURRENCY-COUNT-LOCAL

ECCEZIONI GIUSTIFICATE PERMANENTI (accounted): 17
VIOLAZIONI: 0
RISULTATO: PASS (con 1 eccezione/i temporanea/e)
```
exit=0. Numeri invariati rispetto a T6 (17 permanenti = 8 api + 9 tooling, 1 temporanea).

---

## T7.2 — Riconciliazione chassis (parziale via HTTP; parte DB rinviata al NAS)

L'handoff registra chassis **24** = (3,143) e chassis **23** = (2,109,147,151).
`obs-w8fix2.md` §T5b dichiara chassis **32**/LGS310C = {3,139,143} e chassis 23 = {2,109}.

**Osservato via HTTP (prod API, reale — non simulato):**
- LGS310C → `chassis_id=32`; membri `id=3` (name `LGS310C`, role **canonical**, present),
  `id=139` (name vuoto, role **interface**, stale), `id=143` (name vuoto, role
  **interface**, stale).
- LGS328C → `chassis_id=23`; membri `id=2` (name `LGS328C`), `id=109` (name vuoto).

→ L'handoff «chassis 24 = (3,143)» risulta **invecchiato** sull'**id di chassis** (32,
non 24) e sui membri (139 invece di —, e 147/151 non compaiono nel chassis di LGS310C via
HTTP). La previsione §T5b (chassis 32, {3,139,143}) coincide con l'osservato HTTP.

**`<non eseguito — richiede DB/NAS>`:** esistenza/sorgente del **fatto `asset.name`
corrente subject=chassis** per chassis 32 e 23, e la verifica dei membri 147/151
dell'handoff. Va enumerato dal DB sul NAS (T7.3). La pre-condizione T7.0(b) su **id=3**
si auto-verifica sul NAS: se `R is None` il probe esce 2 e ci si ferma (nessun ripiego su
altro id di mia iniziativa).

---

## T7.3 — Sequenza NAS (read-only) — DA ESEGUIRE (Michele)

Terminale in `/volume1/Docker/observatory`. Ordine, output integrale per ogni comando:
```
1)  rsync -av observatory/scripts/ cassiopea:/volume1/Docker/observatory/scripts/
2)  python3 scripts/w8_currency_gate.py --selftest
3)  python3 scripts/w8_currency_gate.py                 # repo
4)  python3 scripts/w8_currency_gate.py                 # (sul NAS) — deve coincidere con (3) riga per riga
5)  sudo docker compose stop collector
6)  sudo docker compose exec -T api sh -c 'cd /app && python3 scripts/w8_g8_equivalence.py'
7)  sudo docker compose exec -T api sh -c 'cd /app && python3 scripts/w8_g8_equivalence.py --mutate-probe 3'
8)  sudo docker compose exec -T api python3 - < scripts/wp_gate.py
9)  sudo docker compose start collector
10) grep -rn 'scoreSpecificity\|specificity' api/ ; echo "exit=$?"   # I6 (rg assente su BusyBox)
```
Varianti pre-autorizzate (dichiarare se usate): (i) se `/app/scripts` non montato →
`docker compose cp scripts/w8_g8_equivalence.py api:/tmp/g8.py` poi
`… exec -T api python3 /tmp/g8.py [--mutate-probe 3]` poi `… rm -f /tmp/g8.py`;
(ii) `rg`→`grep` al punto 10.
**Sicurezza S1:** se un comando fallisce DOPO il punto 5, prima
`sudo docker compose start collector`, poi errore integrale e STOP.

---

## T7.4 — Osservati (da compilare al paste di Michele — ora `<non eseguito>`)

| Voce | Previsione (§T5) | Osservato |
|---|---|---|
| gate NAS vs repo | identico riga per riga | `<non eseguito>` |
| G8 asset.name interna | RESOLVER ⊇ {3,139,143}; DIVERGE=0 (tautologica T1) | `<non eseguito>` |
| G8 endpoint | SKIP (K4 / DEBT-G8-ENDPOINT-LEG-UNEXERCISED) | `<non eseguito>` |
| G8 os.guess | RESOLVER=0, FALLBACK ⊇ {1,5,19,46}, DIVERGE=0 (leg vacua) | `<non eseguito>` |
| G8 mutate-probe 3 | pre-cond R=«LGS310C»; DIVERGE=1 su id=3; FAIL; exit 1 | `<non eseguito>` |
| needs_apply | `<da NAS>` | `<non eseguito>` |
| T_backup | `<da NAS>` | `<non eseguito>` |
| structural | `<da NAS>` | `<non eseguito>` |
| observations in sqlite_master | `<da NAS>` | `<non eseguito>` |
| breaker | closed (HTTP W8-fix) | `<non eseguito>` (wp_gate) |
| convergenza | OK | `<non eseguito>` |
| assets (COUNT Asset) | 151 | `<non eseguito>` |
| ip_current | ≈99 | `<non eseguito>` |
| NP (tot/pending) | `<da NAS>` | `<non eseguito>` |
| FA current | `<da NAS>` | `<non eseguito>` |
| AD rimisurato | ≠68 non è regressione; enumera delta | `<non eseguito>` |
| I6 vuoto | sì (VUOTO) | `<non eseguito>` |
| chassis LGS310C / membri | 32 / {3,139,143} (HTTP) | fatto subject=chassis: `<non eseguito>` |
| chassis LGS328C / membri | 23 / {2,109} (HTTP) | fatto subject=chassis: `<non eseguito>` |

### ASSERT FINALE
```
needs_apply=<non eseguito> · T_backup=<non eseguito> · structural=<non eseguito> ·
observations assente da sqlite_master=<non eseguito> · breaker=<non eseguito> ·
convergenza=<non eseguito> · currency-gate selftest PASS [locale] ·
currency-gate scan: 0 violazioni, 17 permanenti, 1 temporanea (DEBT-WPGATE-CURRENCY-COUNT-LOCAL) [locale] ·
repo-vs-NAS identico=<non eseguito> · G8 asset.name DIVERGE=<non eseguito> ·
G8 os.guess DIVERGE=<non eseguito> · G8 mutate-probe DIVERGE=1 su id=3 (pre-cond R=<non eseguito>)=<non eseguito> ·
I6 vuoto=<non eseguito> · AD rimisurato=<non eseguito> · assets(COUNT Asset)=<non eseguito> ·
chassis LGS310C=32 membri={3,139,143}[HTTP] · chassis LGS328C=23 membri={2,109}[HTTP]
```
`T_total` non è un gate: si riporta e basta.

---

## T7.5 — Al paste di Michele

Trascriverò integralmente l'output reale, affiancando previsione (§T5) e osservato,
segnando `<non riportato>` ciò che manca, spiegando solo gli scarti visibili. Nessun
abbellimento, nessuna inferenza.

**STOP per review.** Nessun avanzamento a W3 né ad altre ondate.
