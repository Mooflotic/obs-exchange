<!-- BLOCK-ID: OBS-W8 -->

# W8 — Enforcement della correntezza

**Esito in una riga.** Il censimento esaustivo trova **0 calcoli locali di
correntezza da migrare** (classe (a) vuota): la correntezza dei fatti è già
letta da un solo posto, il resolver `api/app/facts/`; tutto il resto è (b)
legittimo con criterio dichiarato. Perciò **nessun cambio di codice runtime →
nessun deploy → nessun bump** (VERSION resta **0.10.63**). W8 consegna il
**presidio permanente** (gate + doc) e l'**equivalenza G8**, e conferma che
l'**API è corrente per default**.

> Perché non ci sono migrazioni: i consumatori dei fatti erano già stati portati
> al resolver / allo stato derivato in W5/W6/W7. W8 lo **dimostra** e ci mette un
> presidio che impedisce il ritorno di calcoli locali.

---

## 0. Baseline (0.10.63, invariata — nessun deploy)

assets **151** · ip_current **99** · NP **408** (pending **77**) · FA **261**
(current **68**) · AD **68** (finestra mobile) · unknown_source **0** ·
breaker **closed**. Delta previsto e osservato: **0** (nessuna scrittura, nessun
deploy).

---

## W8.1 — Censimento dei calcoli locali di correntezza (esaustivo)

Grep su `api/**` e `web/src/**` per: `ORDER BY … observed_at/last_seen DESC
LIMIT 1`, `MAX(observed_at/last_seen)`, `is_current == True`, `.first()` su
query ordinate per tempo, `timedelta(hours/days/minutes=…)`, `DISTINCT` su
ip/mac/hostname, «prendi il più recente». Ogni riga ha una disposizione. Nessuna
è (a); nessuna (c) da rimuovere; tutte (b) con criterio dichiarato.

### Criterio di distinzione (W8.1.3)

Un punto è **correntezza dei FATTI** solo se decide il valore corrente di un
fatto del registry (`asset.name`, `iface.alias`, `asset.iface_ip`,
`asset.mgmt_ip`, `presence.portal`, `port.fdb_mac`, `rel.physical_link`,
`os.guess`, `name_proposal`) leggendo `FactAssertion`. Tutto ciò che segue **non
lo è**, e il criterio è dichiarato riga per gruppo:

| Gruppo | Fatto/oggetto | Criterio usato | Dentro `facts/`? | Disp. |
|---|---|---|---|---|
| resolver.py:79,108,146,287,640 · shadow.py:371,401 | correntezza fatti | `state="current"` + order-by id | **Sì** | (b) unica fonte |
| admin.py:292,295 | COUNT righe FA | osservabilità breaker (no valore) | No (allowlist) | (b) |
| admin.py:311,315,317,318,320 | divergenze conflict_review | `state="historical"` (I3), display | No (allowlist) | (b) |
| models.py:155 · bootstrap.py:19 | — | def ORM / import create_all | No (allowlist) | (b) |
| `ip_addresses.is_current` (≈70 punti, vedi sotto) | IP eletto | **elezione** IP, non correntezza fatto (F-15) | No | (b) |
| fingerprint_facts.py:1204 | evidenza grezza | `ObservationRaw.observed_at DESC` (evidenza, non stato) | No | (b) |
| identity/trust/event_maintenance/monitoring (Event.created_at DESC) | eventi | ultimo **evento** di dominio | No | (b) |
| actions.py:239 · asset_identity.py:274 · evolution.py:175 · suggestions.py:24 · drift.py:32 · monitors/dashboard/speedtest (SpeedTestResult) | oggetti di dominio | ultimo scan/azione/finding/suggestion/snapshot/speedtest | No | (b) |
| trust.py:399 (MAX last_fdb_at) · flows_summary.py:97 (MAX observed_at) | aggregati evidenza | max di un timestamp d'evidenza (presenza/flussi) | No | (b) |
| ~30 `timedelta(…)` (retention/monitoring/presence/cooldown) | finestre | freschezza/presenza/retention, **stato derivato da classify_asset** (F-7) | No | (b) |
| habits:246 · admin:223 · reliability:36 · ip_intel_context:123,129 | DISTINCT | dedup/aggregazione, non «prendi l'ultimo» | No | (b) |
| web/src/inventoryDevices.js (is_current, maxLastSeen, canonName) | display | consuma correntezza/elezione/stato **dal server** | No (FE) | (b) |

### `is_current` su `ip_addresses` — falso positivo legittimo (F-15, W8.1.3)

È il **meccanismo di elezione** dell'IP eletto, non un calcolo di correntezza
dei fatti. Distinzione: opera sulla colonna `is_current` della **riga IP**
(elezione prodotta da `identity.elect_interface_primary`, il produttore
dell'elezione), non su `FactAssertion`. Il resolver **non** è fonte esclusiva
per gli IP finché il ruolo non entra nella `excl_key` (pre-condizione W3). Punti
(campione esaustivo): `identity.py` 305/479/508/886–943/1019 (886–943 =
`elect_interface_primary`, il produttore), `actions.py` 153/262/277/536,
`assets.py` 86/98/108/933/951/963, `ingest.py` 231/259, `scans.py`
111/132/151/499, `topology.py` 339/552/668/1068/1557, `inventory.py`
134/135/588, `migrate.py` 155–327, `monitoring.py` 148/267/1204, `ai_naming.py`
213/228, `ai.py` 169, `detectors/__init__.py` 40/63, `ip_intel.py` 298,
`snapshots.py` 30, `asustor_health.py` 20, `reliability_metrics.py` 38,
`watch.py` 233, `admin.py` 221, `switches.py` 167, `trust.py` 262,
`identity_fusion.py` 109, `wifi_associations.py` 116, `mac_ip_policy.py`
121–123, `dashboard.py` 356, `habits.py` 238, `models.py` 129 (def). **Tutti
(b)**.

### Classe (c) — codice morto

Nessuna riga da rimuovere. `resolver.history()` è **senza chiamanti** ma è il
percorso storico **sanzionato** (esposto solo su `?history=true`): non è morto,
è il contratto per lo storico. Mantenuto → (b).

---

## W8.2 — Migrazione classe (a)

**Nulla da migrare (classe (a) vuota).** K12 è soddisfatto in modo vacuo: non si
rimuove alcun calcolo locale, quindi non c'è equivalenza da dimostrare *prima*
di una rimozione. R-G (W8.2.3): dove il resolver restituisce `None`, il
chiamante **dichiara l'assenza** — `presentation_name_for_asset` ritorna `None`
(mai `""`), l'API restituisce `ips: []`/`ip_bindings: []` (assente ≠ zero, vedi
W8.4). F-15 (W8.2.4): gli IP **non** si migrano al resolver come fonte esclusiva
(perderebbero gli IP reali non eletti) → **rinviati a W3**, dichiarato.

---

## W8.3 — Il gate permanente (istituito, eseguito)

`scripts/w8_currency_gate.py`. Sentinella: ogni riga che nomina `FactAssertion`
sotto `api/app/**` escluso `api/app/facts/**`. **Fallisce** su accessi nuovi.
Allowlist **per (file, snippet esatto)** con motivazione — mai pattern generico.

Output completo (eseguito ora):

```
== W8 CURRENCY GATE ==
scope: api/app/**  (escluso api/app/facts/**)
sentinella: righe che nominano `FactAssertion`

ECCEZIONI GIUSTIFICATE (accounted): 9
  OK  api/app/models.py:155           | class FactAssertion(Base):
  OK  api/app/bootstrap.py:19         | from app.models import FactAssertion, IdentityEvidence, ...  # create_all
  OK  api/app/routers/admin.py:292    | from app.models import FactAssertion
  OK  api/app/routers/admin.py:295    | rows = int(db.scalar(select(func.count()).select_from(FactAssertion)) or 0)
  OK  api/app/routers/admin.py:311    | from app.models import FactAssertion
  OK  api/app/routers/admin.py:315    | select(FactAssertion)
  OK  api/app/routers/admin.py:317    | FactAssertion.reason == "conflict_review",
  OK  api/app/routers/admin.py:318    | FactAssertion.state == "historical",
  OK  api/app/routers/admin.py:320    | .order_by(FactAssertion.last_seen_at.desc(), FactAssertion.id.desc())

VIOLAZIONI (accessi nuovi non giustificati): 0

RISULTATO: PASS
```

Da eseguire a ogni ondata futura **insieme a I6**. Documentato in
`docs/obs-design-spec-025.md` §12 e `KNOWN_DEBT.md` (PRESIDIO-CURRENCY-GATE).

---

## W8.4 — Superficie API e UI

**API corrente per default: già così. 0 contratti cambiati.** Enumerazione:

| Endpoint | Default | Storico |
|---|---|---|
| `GET /api/assets` | `include_historical=false`, `all_proposals=false` → solo correnti | `?include_historical=true`, `?all_proposals=true` |
| `GET /api/assets/{id}` | binding correnti + non-eletti visibili (F-15); `proposal_history` = divergenze I3 dichiarate | — |
| `GET /api/suggestions` | filtro `status` | — |
| `GET /api/admin/facts/conflicts` | divergenze `state="historical"` (I3, per costruzione storico/diagnostico) | — |
| `resolver.history()` | non cablato ad alcun endpoint | percorso `?history=true` sanzionato, non usato |

**UI stale/superseded/assente dichiarati — verifica runtime (method A, prod
0.10.63):**

- **assente ≠ zero** — asset **109** (LGS328C, chassis 23): `ips: []`,
  `ip_bindings: []` → l'UI mostra «—», non `0`.
- **non-eletti/duplicati visibili (F-15)** — asset **2**: `192.168.1.2` compare
  in **due** binding (`role=mgmt` source `mgmt`; `role=""` source `fritz`),
  entrambi resi con ruolo/sorgente (DEBT-DOUBLE-CURRENT-IP non collassato).
- **inferenza AI marcata (F-10/I1)** — asset 109: `guess="Switch Centrale"`,
  `guess_source="ai"` accanto al nome, non spacciata per certezza.

**UI invariata da W8** (nessun cambio di codice): le rese `stale/superseded`
già verificate con screenshot in **UX3** (`obs-ux3-*`) restano valide; W8 non le
tocca. Verifica R non ri-esercitata in W8 perché la UI è identica (K4 dichiarato);
la resa reale del **contratto** è esercitata qui via method A. Nessuna card ad
alta priorità senza azione (F-9), policy MAC↔IP resta consultiva (F-12).

---

## W8.5 — Gate di equivalenza G8

`scripts/w8_g8_equivalence.py` (read-only, mai commit). Confronta, per ogni
asset, la correntezza del **nome** dal resolver (`current("asset.name")`) con la
presentazione consumer-facing (`presentation_name_for_asset`). Classi per id:
`RESOLVER` (P==R), `FALLBACK` (R=None → stato derivato, I2 dichiarata),
`ABSENT` (R=None,P=None, I2), `DIVERGE` (R≠None e P≠R → sospetto calcolo locale).

**Previsione:** `DIVERGE=0` (nessun calcolo locale esiste — W8.1). `FALLBACK`
atteso per i chassis/asset senza fatto-nome manuale a livello chassis (es.
chassis 23 «LGS328C» è **AI**, non un `asset.name` manuale corrente → ripiego
sullo stato; chassis 24 «LGS310C» è **manuale** F-1 → `RESOLVER`). Con 0
migrazioni non esiste un before/after: G8 è **conferma**, e per costruzione ha
**0 casi (c)**. Da eseguire a writer fermi sul NAS (comando in §W8.7).

---

## W8.6 — Previsioni

Nessun deploy ⇒ nessuna variazione prevista: assets **151**, ip_current **99**
(id congelati come in `obs-ux3.md` §0), NP **408**/pending **77**, FA
**261**/current **68**, AD ~**68**, unknown_source **0**, breaker **closed**,
**0** endpoint con contratto cambiato. G8: `DIVERGE=0`. Currency gate: PASS.

---

## W8.7 — Gate W8 e chiusura

| # | Requisito | Stato |
|---|---|---|
| 1 | Censimento esaustivo, ogni riga con disposizione | ✅ (0 (a), 0 (c), tutte (b)) |
| 2 | Classe (a) migrata con equivalenza (K12) | ✅ vacuo (0 (a)); IP rinviati a W3 (F-15) |
| 3 | Gate permanente istituito, eseguito, output, eccezioni per file:riga | ✅ PASS (9 ecc., 0 viol.) |
| 4 | API corrente per default; storico solo su richiesta | ✅ già così, 0 contratti cambiati |
| 5 | UI stale/superseded dichiarati, resa reale | ✅ method A (contratto); R invariata da UX3 (K4) |
| 6 | G8 senza (c); gate binari/convergenza verdi; I6 vuoto | ⏳ da confermare sul NAS (comandi sotto; nessun deploy) |
| 7 | Delta enumerati per id | ✅ 0 delta (nessuna scrittura) |

### Comandi di conferma sul NAS (terminale già aperto in `/volume1/Docker/observatory`)

Nessun deploy. Sync degli script nuovi, poi conferma read-only (collector fermo,
`now` ricalcolato). Rollback non pertinente (nessun cambio runtime).

```
# 1) sync repo → NAS (dal tuo host di sviluppo, se serve)
#    rsync -av observatory/scripts/ cassiopea:/volume1/Docker/observatory/scripts/

# 2) presidio correntezza (repo, non tocca prod)
python3 scripts/w8_currency_gate.py      # atteso: RISULTATO: PASS

# 3) equivalenza G8 + convergenza a writer fermi
sudo docker compose stop collector
sudo docker compose exec -T api python3 - < scripts/w8_g8_equivalence.py   # atteso: DIVERGE=0
sudo docker compose exec -T api python3 - < scripts/wp_gate.py             # atteso: CONVERGENZA: OK
sudo docker compose start collector
```

**Assert (una riga, da riportare dopo l'esecuzione):**
`needs_apply=false · T_backup=0 · structural=0 · observations assente · breaker=closed · convergenza OK · G8 DIVERGE=0 · currency-gate PASS · I6 vuoto`.

---

## Lista per Michele (solo scelte di dominio, nessun difetto funzionale)

1. **Attivazione autoritativa** delle regole #3/#5 della policy MAC↔IP: resta
   rinviata (F-12, `DEBT-MAC-IP-POLICY-WIRE`) — decisione di dominio su quali
   device attivi declassare. Nessuna azione richiesta ora.
2. Dopo la review, **W3 (backfill)** resta bloccato dalle tre pre-condizioni IP
   aperte: `DEBT-DOUBLE-CURRENT-IP`, `DEBT-IFACE-IP-CARDINALITY-ROLE`,
   `DEBT-LASTSEEN-DUAL-SEMANTICS`.

---

## STOP

W8 chiuso lato repo (censimento + presidio + doc + G8 pronto). Restano da
**confermare sul NAS** i gate binari/convergenza/G8/I6 (comandi sopra, nessun
deploy). Dopo la review si valuta **W3**, che resta bloccato dalle tre
pre-condizioni IP aperte.
