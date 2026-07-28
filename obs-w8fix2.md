# OBS — W8-fix2 · chiusura: ri-pubblicazione verificabile, ruling applicato, doc allineata

Ramo `feature/obs-currency` · prod **0.10.63** (nessun bump, nessun deploy, nessun
tocco a `api/app/**` o `web/src/**`). Verifiche read-only.

Questo report **non incorpora sorgente runtime**: i tre allegati T1 (resolver,
name_proposal_chassis, chassis_rename) restano in `obs-w8fix.md` §Allegati T1 e si
citano per riferimento. Il sorgente dei due script d'ondata è in
`obs-w8fix2-scripts.diff.txt` (solo quello).

## Conteggio righe degli artefatti pubblicati (T2d — troncatura in lettura = rilevabile)

| Artefatto | righe (`wc -l`) |
|---|---|
| `obs-w8fix2.md` | 242 |
| `obs-w8fix2-scripts.diff.txt` | 574 |
| `w8fix2_currency_gate.py` | 343 |
| `w8fix2_g8_equivalence.py` | 219 |
| `obs-design-spec-025.md` | 619 |
| `KNOWN_DEBT.md` | 439 |
| `obs-w8fix.md` | 956 |

---

## R1 — perché i file «sembravano» W8 e come è verificabile ora

Al publish di W8-fix il gate misurava **12018 B** (versione indurita, non i ~5 KB di
W8) e `curl` restituiva 200: il contenuto pubblicato ERA quello indurito. La
collisione era sul **nome piatto** (`w8_currency_gate.py`), con cache CDN di
`raw.githubusercontent` sull'URL già esistente. W8-fix2 pubblica con **nomi nuovi**
(`w8fix2_*`) e allega il **doppio sha256** (locale vs `curl`): non più verificabile a
occhio, verificabile per hash.

---

## T1 — Ruling sui 10 accessi (applicato esattamente)

**9 righe → allowlist PERMANENTE** `(file, snippet, N)`, motivazione individuale
(stile `admin.py`). Numeri di riga **verificati, nessuno scarto**:

| riga | motivazione |
|---|---|
| `scripts/wp_gate.py:36` | import per diagnostica di regime |
| `scripts/wp_diagnose.py:29` | import per diagnostica |
| `scripts/wp_gate.py:102` | COUNT righe totali (nessun valore) |
| `scripts/wp_diagnose.py:125` | COUNT righe totali (nessun valore) |
| `scripts/wp_diagnose.py:127` | distribuzione di stato (diagnostica) |
| `scripts/wp_diagnose.py:232` | campione di display (ultime 15) |
| `scripts/wp_diagnose.py:267` | enumerazione id (now) per delta |
| `scripts/wp_diagnose.py:268` | enumerazione id (baseline) per delta |
| `scripts/wp_diagnose.py:273` | lettura per id già enumerato |

**10ª riga NON sanata** — `scripts/wp_gate.py:103`
(`COUNT(FactAssertion WHERE state=="current")`): **seconda definizione di «corrente»**
nello strumento che certifica la produzione (il resolver applica TTL/`_maybe_stale`/R-E;
da questa riga nasce «FA current» della baseline). Azioni eseguite:
- aperto **`DEBT-WPGATE-CURRENCY-COUNT-LOCAL`** (priorità media) in `KNOWN_DEBT.md`:
  cosa, perché è un secondo autore di correntezza, chi lo consuma (baseline FA current),
  risoluzione = helper di conteggio in `api/app/facts/` (micro-ondata runtime, non ora),
  clausola «vietato chiuderlo allowlistandolo in permanenza»;
- introdotta nel gate la sezione **`TEMPORARY_ALLOWLIST`** `(file, snippet, N, debt)`
  con `debt` OBBLIGATORIO (voce senza debt → exit 1 per errore di configurazione);
  contiene SOLO `wp_gate.py:103`;
- output: sezione TEMPORANEE **in testa**, formato
  `TEMP scripts/wp_gate.py:103 (atteso 1, osservato 1) debt=DEBT-WPGATE-CURRENCY-COUNT-LOCAL`;
- RISULTATO resta PASS senza violazioni ma riporta **`PASS (con 1 eccezione temporanea)`**.

**Nessuna esclusione per path** di `wp_gate.py`/`wp_diagnose.py` (più permissiva di un
pattern generico, vietata). Criterio registrato in `obs-design-spec-025.md` §12:
`api/app/facts/**` escluso perché è la FONTE; ogni altro consumatore si allowlista riga
per riga come `admin.py`.

---

## T6 — Riesecuzione locale del gate dopo il ruling (output integrale)

### `python3 scripts/w8_currency_gate.py --selftest`
```
SELFTEST/1 corpus principale: atteso 3 violazioni ['file2_rawsql.py', 'file3_filterby.py', 'file4_count.py'] + 1 accounted
SELFTEST/1 osservato: 3 violazioni ['file2_rawsql.py', 'file3_filterby.py', 'file4_count.py'] + 1 accounted + 0 temporanee
SELFTEST/1: PASS
SELFTEST/2 config-check temporanee: atteso 1 errore (debt vuoto) + 0 (debt valido)
SELFTEST/2 osservato: 1 errore(i) debt-vuoto + 0 debt-valido
SELFTEST/2: PASS

SELFTEST: PASS (il gate sa fallire e valida le temporanee)
```
Il quinto file sintetico (`file5_temp.py`) alimenta il config-check: una voce
temporanea **senza `debt`** viene rilevata come errore di configurazione (1), una con
`debt` valido no (0).

### `python3 scripts/w8_currency_gate.py` (repo reale)
```
== W8 CURRENCY GATE (indurito, W8-fix2) ==
file scansionati: 175
voci allowlist: permanenti 17 · temporanee 1

ATTENZIONE — ECCEZIONI TEMPORANEE CON DEBITO APERTO: 1
  TEMP scripts/wp_gate.py:103 (atteso 1, osservato 1) debt=DEBT-WPGATE-CURRENCY-COUNT-LOCAL
      | fa_cur = int(db.scalar(select(func.count()).select_from(FactAssertion).where(FactAssertion.state == "current")) or 0)

ECCEZIONI GIUSTIFICATE PERMANENTI (accounted): 17
  OK  api/app/bootstrap.py:19             (atteso 1, osservato 1)  import create_all
  OK  api/app/models.py:155               (atteso 1, osservato 1)  class FactAssertion(Base)
  OK  api/app/routers/admin.py:292,311    (atteso 2, osservato 2)  import diagnostica
  OK  api/app/routers/admin.py:295        (atteso 1, osservato 1)  shadow-stats COUNT
  OK  api/app/routers/admin.py:315        (atteso 1, osservato 1)  conflicts select
  OK  api/app/routers/admin.py:317        (atteso 1, osservato 1)  conflicts reason
  OK  api/app/routers/admin.py:318        (atteso 1, osservato 1)  conflicts state='historical'
  OK  api/app/routers/admin.py:320        (atteso 1, osservato 1)  conflicts order_by
  OK  scripts/wp_gate.py:36               (atteso 1, osservato 1)  import diagnostica regime
  OK  scripts/wp_gate.py:102              (atteso 1, osservato 1)  COUNT totale
  OK  scripts/wp_diagnose.py:29           (atteso 1, osservato 1)  import diagnostica
  OK  scripts/wp_diagnose.py:125          (atteso 1, osservato 1)  COUNT totale
  OK  scripts/wp_diagnose.py:127          (atteso 1, osservato 1)  distribuzione di stato
  OK  scripts/wp_diagnose.py:232          (atteso 1, osservato 1)  campione display (15)
  OK  scripts/wp_diagnose.py:267          (atteso 1, osservato 1)  enum id (now)
  OK  scripts/wp_diagnose.py:268          (atteso 1, osservato 1)  enum id (baseline)
  OK  scripts/wp_diagnose.py:273          (atteso 1, osservato 1)  get per id

VIOLAZIONI: 0

RISULTATO: PASS (con 1 eccezione/i temporanea/e)
```
Previsione T6 (**17 permanenti = 8 api + 9 tooling, 1 temporanea, 0 violazioni**):
**confermata**, exit 0. Selftest exit 0.

---

## T5 — Previsioni pinnate PRIMA dell'esecuzione NAS

### T5a — leg `os.guess`
- **Mappatura fatto→colonna (dichiarata ora):** `os.guess` (fact, subject=**asset**,
  `subject_ref_asset`, cardinality single, sources `{manual, nmap}`, `ttl_window=None`)
  ↔ colonna derivata `Asset.os_guess`. **Normalizzazione:** solo whitespace-collapse
  (`_norm_value`), **nessun** lowercase / trim-vendor / prefisso. Perciò un `DIVERGE`
  con differenza di case o vendor È un divergere reale: **non** lo riclassificherò come
  «normalizzazione legittima» a posteriori.
- **Previsione classi (prod):** i writer shadow scrivono SOLO `asset.iface_ip`
  (shadow-stats counters); `os_fingerprint` notturno è OFF ⇒ **os.guess facts current ≈ 0**.
  Quindi: **RESOLVER=0 · DIVERGE=0**. **FALLBACK** = asset con `os_guess` colonna non
  vuota e senza fatto: via HTTP (lista default) sono **4** → id **{1, 5, 19, 46}**
  (`Linux 4.15 - 5.19`, `ADM-Free-OS-028b`, `Linux 5.6.3`, `Linux 5.6.3`); tra gli
  storici potrebbero essercene pochi altri. **ABSENT** = tutti gli altri. **La leg sarà
  quasi vacua: è un'informazione, non un difetto.**

### T5b — leg `asset.name` (subject=chassis)
- **RESOLVER attesi (id):** membri del **chassis 32 / LGS310C** (fatto manuale, F-1):
  **{3, 139, 143}** (3 canonical/present, 139+143 interface/stale — G8 itera TUTTE le
  righe Asset, storici inclusi). Altri chassis compaiono in RESOLVER **solo se** hanno
  un `asset.name` adottato (fatto): non visibile via HTTP → da enumerare sul NAS.
- **FALLBACK attesi:** **chassis 23 / LGS328C** = **{2, 109}** — il nome «LGS328C» è
  derivato (asset 2, `guess_source: oui`, F-2 NON confermato manuale): resolver=None,
  presentazione=«LGS328C» dal membro → FALLBACK. Più gli altri chassis/singleton con
  nome derivato.
- **ABSENT:** asset senza alcun nome.
- **DIVERGE atteso: 0.**

### T5c — id per `--mutate-probe`
**id = 3** (asset 3, chassis 32). Motivo: ha `asset.name` **corrente dal resolver**
(«LGS310C» manuale) → la mutazione della presentazione produce un DIVERGE pulito contro
`R="LGS310C"`. Atteso: **DIVERGE=1 su id=3, RISULTATO FAIL**.

### T5d — `assets` (due definizioni distinte, NON la stessa metrica)
- **wp_gate:** `COUNT(Asset)` = **tutte le righe**, **nessun filtro** (verificato in
  `wp_gate.py:98`). Previsione **151**. ⚠️ La label «no-historical» del task è imprecisa:
  wp_gate **non** esclude gli storici; lo dichiaro dalla sorgente, non lo adatto.
- **HTTP lista default** (no `include_historical`): **112** (filtro della lista).
- **HTTP `include_historical=true`:** **151**.
- Quindi `wp_gate (151) == HTTP include_historical (151) ≠ HTTP default (112)`. Non
  dichiaro «= baseline» tra metriche a definizione diversa.

### T5e — AD (finestra mobile 24h)
Sarà **letto da `wp_gate` sul NAS**. Un valore **≠ 68 NON è una regressione** (finestra
mobile, tempo trascorso). Se differisce, enumererò gli id in delta (device_counters).

---

## T7 — Esecuzione sul NAS (read-only) — comandi + previsioni (handoff)

Nel terminale già aperto in `/volume1/Docker/observatory`. Previsioni T5 sopra.
Durante G8 **nessuna azione va innescata sull'api** (sole letture; `db.rollback()`).

```
rsync -av observatory/scripts/ cassiopea:/volume1/Docker/observatory/scripts/
python3 scripts/w8_currency_gate.py --selftest        # atteso: SELFTEST PASS
python3 scripts/w8_currency_gate.py                    # (repo) atteso: PASS (con 1 eccezione temporanea)
# sul NAS, stessa cosa: output IDENTICO riga per riga. Se diverge → repo != prod: FERMATI.
sudo docker compose stop collector
sudo docker compose exec -T api sh -c 'cd /app && python3 scripts/w8_g8_equivalence.py'
sudo docker compose exec -T api sh -c 'cd /app && python3 scripts/w8_g8_equivalence.py --mutate-probe 3'
sudo docker compose exec -T api python3 - < scripts/wp_gate.py
sudo docker compose start collector
rg 'scoreSpecificity|specificity' api/                 # I6: atteso VUOTO
```
Note: `python3 - < file` non passa gli argv → per il mutate-probe usa la forma
`sh -c 'cd /app && python3 scripts/... --mutate-probe 3'`. Se `/app/scripts` non è
montato, copia il file nel container e dichiara come. Se un comando fallisce: errore
integrale e **STOP**, nessuna variante non dichiarata.

**Previsioni numeriche NAS:**
- gate NAS = gate repo (`PASS (con 1 eccezione temporanea)`);
- G8 `asset.name` DIVERGE=0 (RESOLVER ⊇ {3,139,143}); `os.guess` DIVERGE=0 (RESOLVER 0,
  FALLBACK ⊇ {1,5,19,46}); `--mutate-probe 3` DIVERGE=1 su id=3, FAIL;
- wp_gate: convergenza OK, breaker closed, assets=151, ip_current≈99, AD=<da wp_gate>;
- I6 VUOTO.

---

## ASSERT FINALE (osservati; `<da NAS>` dove non misurato in QUESTA ondata)

```
needs_apply=<da NAS> · T_backup=<da NAS> · structural=<da NAS> ·
observations assente da sqlite_master=<da NAS> · breaker=<da NAS (HTTP W8-fix: closed)> ·
convergenza=<da NAS> ·
currency-gate selftest PASS (3 attese + config-check debt) [osservato locale] ·
currency-gate scan: 0 violazioni, 17 permanenti, 1 temporanea (DEBT-WPGATE-CURRENCY-COUNT-LOCAL),
  PASS (con 1 eccezione temporanea) [osservato locale] ·
repo-vs-NAS output identico=<da NAS> ·
G8 asset.name DIVERGE=0 (enumerazione classi per id)=<da NAS> ·
G8 os.guess DIVERGE=0 (previsione T5a: RESOLVER=0/FALLBACK≈{1,5,19,46})=<da NAS> ·
G8 mutate-probe DIVERGE=1 su id=3=<da NAS> ·
I6 vuoto=<da NAS> (osservato locale sul repo: VUOTO) ·
AD rimisurato=<da NAS> · assets(wp_gate, COUNT tutte)=<da NAS, previsto 151> ·
assets(HTTP, include_historical)=151 [osservato] · assets(HTTP default)=112 [osservato]
```
`T_total` non è un gate: si riporta e basta.

---

## Sintesi bug della review W8-fix (R1–R6)

| Review | Esito W8-fix2 |
|---|---|
| **R1** file pubblicati = W8 | Nomi nuovi `w8fix2_*` + **doppio sha256** (locale vs curl). |
| **R2** diff con report/sorgente incorporato | `obs-w8fix2-scripts.diff.txt` contiene **solo i due script**; il report non incorpora sorgente runtime. |
| **R3** doc descrive gate vecchio | §12 e `PRESIDIO-CURRENCY-GATE` riscritti (scope, 3 sentinelle, allowlist N + temporanee, stato reale, G8 tx). |
| **R4** assert con gate mai misurati | assert onesto: `<da NAS>` per needs_apply/T_backup/structural/observations; corretto anche in `obs-w8fix.md`. |
| **R5** B4 «Rimisurato» ma rinviato | Sintesi: **rinviato al NAS**; corretto anche in `obs-w8fix.md`. |
| **R6** B1(i) «chiuso» | Dichiarato **MITIGATO, non chiuso** (SQL multi-riga concatenato sfugge) in §12, KNOWN_DEBT e `obs-w8fix.md`. |

**STOP per review.** Nessun avanzamento a W3 né ad altre ondate.
