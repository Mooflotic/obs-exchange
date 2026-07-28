# OBS-O1 — chassis e adozione nome in Oggi (0.10.64)

## Residuo OBS-CURRENCY (sospeso, non chiuso)

Da registrare, **non** da lavorare in questa ondata:

- T7 **mai** eseguita in produzione: G8 (`asset.name`, `os.guess`, `--mutate-probe`), `wp_gate` (convergenza, `needs_apply`, `T_backup`, structural, breaker, AD rimisurato), I6 su NAS.
- `DEBT-PROD-SOURCE-DRIFT` aperto.
- `scripts/_w4a_measure.py` resta sul NAS dov'è: per direttiva di Michele **NON** va spostato, archiviato, cancellato né ulteriormente analizzato.
- Nessun merge su main da OBS-CURRENCY né da O1.

Registrato anche in `docs/KNOWN_DEBT.md` § «CANTIERE OBS-CURRENCY — SOSPESO».

## Conteggio righe artefatti

| Artefatto | `wc -l` / note |
|---|---|
| `obs-o1.md` | 211 |
| `obs-o1.diff.txt` | 2088 |
| `obs-o1-oggi-desktop.png` | sezione chassis (1100×3000) |
| `obs-o1-oggi-tablet.png` | sezione chassis (720×4350) |
| `obs-o1-oggi-mobile.png` | sezione chassis (366×6680) |

---

## PREVISIONI (pinnate PRIMA del deploy)

### Card in Oggi
- **PRIMA (0.10.63):** 0 card «Apparati multi-interfaccia» (sezione assente). Proposte nome per-NIC: asset **109** (AI «Switch Centrale») e **151** (OUI «Switch Linksys») potevano generare card proprie; altri membri multi-NIC senza pending top → nessuna card nome chassis dedicata.
- **DOPO (atteso):** **15** card chassis (una per ogni multi-member ≥2 visibili con `include_historical=true`):
  ids chassis **{1, 3, 9, 15, 16, 17, 18, 19, 20, 23, 28, 30, 31, 32, 33}**.
- **Id che smettono di generare card proposta propria** (assorbiti): tutti i membri di quei chassis, in particolare **{2, 3, 5, 6, 109, 139, 143, 147, 151, …}**; le pending **109→374** (ai) e **151→393** (oui) compaiono **sulla** card chassis 23, non come card separate.

### N1–N5 (atteso)

| Nodo | Nome mostrato | Provenienza | Azioni | Note |
|---|---|---|---|---|
| N1 chassis **32** membri **{3,139,143}** | `LGS310C` | fatto **manuale** (resolver o field_sources) | correggi | nessuna sovrascrittura da proposta più debole |
| N2 chassis **23** membri **{2,109,147,151}** | `LGS328C` | **INFERENZA** (oui / senza fact) | conferma / adotta / correggi | mai come fatto |
| N3 asset **109** | — | guess AI «Switch Centrale» etichettato nei note membri | — | **nessuna card propria** (assorbito in N2) |
| N4 chassis **1** membri **{5,6}** | `Cassiopea — NIC 1` | **manuale** | correggi | **una sola card**, due interfacce |
| N5 singleton | invariato | — | triage per-asset come prima | nessuna card chassis spuria |

### Conflitti attesi
- Chassis **23**: proposte pending (AI 374 / OUI 393) vs inferenza display — non conflitto I3 (non c'è fatto manuale); azione adotta/conferma.
- Se su chassis **32** compare proposta non-manuale ≠ LGS310C → conflitto I3 (tieni / sostituisci).

---

## Diff e implementazione

Vedi `obs-o1.diff.txt` (integrale file toccati).

File toccati:
- `api/app/services/chassis_grouping.py` — `name_currency` via `resolver.current` (solo)
- `web/src/oggiChassis.js` (+ test) — card builder; fallback membro con etichetta I1/I2; `heldManual` per I3 legacy
- `web/src/triageRules.js` (+ test) — assorbimento multi-NIC da triage per-asset
- `web/src/oggiProblems.js` — `chassisNameFields`
- `web/src/views/Oggi.vue` — sezione UI + azioni chassis; `friendlyChassisError` nasconde 409 grezzo
- `web/src/api.js` — `adoptChassisName` / `renameChassis`
- `web/src/oggiTriage.test.js` — assorbimento O1
- `docs/KNOWN_DEBT.md` — OBS-CURRENCY sospeso
- `VERSION`, `web/package.json`, `CHANGELOG.md`

Esclusioni dichiarate (una per una):
- `api/app/facts/**` — non toccato
- `collector/**` — non toccato
- FDB / Mappa / Topologia / Plant / 308 / Dossier / favicon / restyle
- `scripts/_w4a_measure.py` (NAS) — non toccato
- merge su main — non eseguito

---

## Deploy

1. Bump VERSION → **0.10.64**.
2. `./scripts/deploy.sh api web` (prima), poi `./scripts/deploy.sh web` (fix `heldManual` post-osservazione locale). Collector non toccato.
3. Health post-boot: `{"ok":true,"service":"observatory-api","version":"0.10.64"}` (API in bootstrap ~107s, poi ready).

---

## OSSERVATI (dopo deploy)

### Card in Oggi
- **UI:** `15 · nome a livello apparato` (testo sezione).
- **Builder su payload live** (`/api/assets?include_historical=true&all_proposals=true` + `/api/chassis`): **15** card, ids **{1, 3, 9, 15, 16, 17, 18, 19, 20, 23, 28, 30, 31, 32, 33}** — allineato alla previsione.
- **Assorbiti (nessuna riga triage nome propria):** verificato per **{2,3,5,6,109,139,143}** → 0 hit in `buildTriageRows`.

### JSON grezzo — `name_currency` (API `/api/chassis`)

Chassis **1** (N4):
```json
{"id":1,"label":"Cassiopea — NIC 1","name_currency":{"value":null,"source":null,"confidence":null,"authority":null,"state":"absent"},"members":[{"asset_id":5,"name":"Cassiopea — NIC 1","ips":["192.168.1.3"]},{"asset_id":6,"name":"Cassiopea — NIC 2","ips":["192.168.1.3","192.168.3.24"]}]}
```

Chassis **23** (N2):
```json
{"id":23,"label":"LGS328C","name_currency":{"value":null,"source":null,"confidence":null,"authority":null,"state":"absent"},"members":[{"asset_id":2,"name":"LGS328C","ips":["192.168.1.2"]},{"asset_id":109,"name":"","ips":[]},{"asset_id":147,"name":"","ips":[]},{"asset_id":151,"name":"","ips":[]}]}
```

Chassis **32** (N1):
```json
{"id":32,"label":"LGS310C","name_currency":{"value":null,"source":null,"confidence":null,"authority":null,"state":"absent"},"members":[{"asset_id":3,"name":"LGS310C","ips":["192.168.1.7","192.168.2.161"]},{"asset_id":139,"name":"","ips":[]},{"asset_id":143,"name":"","ips":[]}]}
```

**Nota (scarto currency):** su tutti i 15 chassis `name_currency.state=absent` — i nomi manuali/legacy vivono su `Asset.name` + `field_sources` (W4b), non ancora come fatto chassis nel store. La UI usa il fallback membro **etichettato** (manuale / inferenza / «nome non noto»), senza spacciare un membro come fact del resolver.

### JSON grezzo — campi asset pertinenti

Asset **3** (N1 canonical):
```json
{"id":3,"name":"LGS310C","chassis_id":32,"chassis_role":"canonical","chassis_canonical_name":"LGS310C","guess":"Switch Linksys","guess_source":"oui","field_sources_name":{"source":"manual","confidence":1.0,"last_seen":"2026-07-27T11:03:50.067735Z","marked_by":"w4b.1.4"},"pending":[]}
```

Asset **2** (N2 canonical):
```json
{"id":2,"name":"LGS328C","chassis_id":23,"chassis_role":"canonical","chassis_canonical_name":"LGS328C","guess":"Linksys","guess_source":"oui","field_sources_name":null,"pending":[]}
```

Asset **109** (N3):
```json
{"id":109,"name":"","chassis_id":23,"chassis_role":"interface","chassis_canonical_name":"LGS328C","guess":"Switch Centrale","guess_source":"ai","field_sources_name":null,"pending":[{"id":374,"value":"Switch Centrale","source":"ai","confidence":0.9,"status":"pending"}]}
```

Asset **5** / **6** (N4):
```json
{"id":5,"name":"Cassiopea — NIC 1","chassis_id":1,"chassis_role":"canonical","chassis_canonical_name":"Cassiopea — NIC 1","field_sources_name":{"source":"manual","confidence":1.0},"pending":[]}
{"id":6,"name":"Cassiopea — NIC 2","chassis_id":1,"chassis_role":"interface","chassis_canonical_name":"Cassiopea — NIC 1","ips":["192.168.3.24"],"pending":[]}
```

Asset **151** pending OUI (sulla card N2, non card propria):
```json
{"id":151,"pending":[{"id":393,"source":"oui","value":"Switch Linksys","confidence":0.85,"status":"pending"}]}
```

### N1–N5 osservati (UI + builder)

| Nodo | Nome mostrato | Provenienza UI | Azioni | Esito |
|---|---|---|---|---|
| N1 ch **32** {3,139,143} | `LGS310C` | **manuale** (member-held; currency absent) | `correggi nome` | OK |
| N2 ch **23** {2,109,147,151} | `LGS328C` → proposta `Switch Linksys` | **inferenza oui** + badge «nome inferito»; guess AI #109 in causa | `correggi nome`, `adotta proposta` | OK |
| N3 asset **109** | — | guess «Switch Centrale» (ai) nei note della card 23 | nessuna card propria | OK |
| N4 ch **1** {5,6} | `Cassiopea — NIC 1` | **manuale**; 2 interfacce (#5 .1.3, #6 .3.24) | `correggi nome` | **una sola card** OK |
| N5 singleton es. **53** `Amazon` | triage invariato | — | nessuna card chassis | OK |

### Scarti previsione → osservato
- Conteggio 15/15: **nessuno**.
- Pending top su N2: rank proposte FE (`PROPOSAL_SOURCE_RANK`) mette **oui (35) > ai (10)** → proposta mostrata **393 Switch Linksys**, non 374. Entrambe restano sull’unica card 23; AI resta visibile come guess membro (I1).
- `name_currency` sempre `absent` in prod (legacy): display da member-held, etichette I1/I2 rispettate; conflitto I3 su manuale member-held coperto da `heldManual` (test + deploy web2).

### Conflitti osservati
- Nessuna card `chassis_conflitto` attiva su N1–N5 (N1 senza pending debole live; generazione backend già blocca proposte più deboli su manuale chassis).

---

## Criteri di fallimento (verificati uno per uno)

| Criterio | Esito |
|---|---|
| N4 produce due card | **PASS** — una card chassis 1, membri {5,6} |
| Inferenza senza etichetta di inferenza | **PASS** — N2 «inferenza oui» + AiInferenceLabel / badge nome inferito |
| Nome assente come "" / plausibile | **PASS** — chassis 9 mostra «nome non noto» / «assenza dichiarata» |
| Nome manuale sovrascritto da proposta più debole | **PASS** — N1 manuale; nessuna adotta silenziosa; conflitto I3 se pending debole |
| Card alta priorità senza azione | **PASS** — N2 alta → correggi+adotta; absent alta → correggi |
| 409 `chassis_subject_required` grezzo all’utente | **PASS** — `friendlyChassisError` in Oggi.vue; adozione sempre via `/api/chassis/...` |

---

## Gate (post-deploy, output)

### `python3 scripts/w8_currency_gate.py` (repo e NAS)

```
VIOLAZIONI: 0
RISULTATO: PASS (con 1 eccezione/i temporanea/e)
```

Nessuna violazione nuova da O1. Nessuna allowlist aggiunta.

### I6 — `rg 'scoreSpecificity|specificity' api/`

```
I6_EMPTY_OK
```

(NAS: `rg` assente → stesso check con `grep -RnE`; vuoto.)

### Test FE nominati

`npm test` web: **133 pass, 0 fail** (incluso `oggiChassis.test.js`).

---

## Screenshot

- `obs-o1-oggi-desktop.png` — sezione «Apparati multi-interfaccia» (N1–N4 contenuti nella sezione; count 15)
- `obs-o1-oggi-tablet.png`
- `obs-o1-oggi-mobile.png`

Nota: screenshot = elemento sezione chassis (full-page viewport bloccato da layout overflow); i nodi N1–N4 sono nel testo UI della sezione.

---

## ASSERT

- O1.1: una card per multi-NIC; nome etichettato; membri elencati; assente → «nome non noto».
- O1.2: azioni sul soggetto chassis; niente 409 grezzo; F-9 rispettato.
- O1.3: `name_currency` solo via resolver; `facts/**` non toccato.
- OBS-CURRENCY resta sospeso; nessun merge main; STOP per review.

**STOP per review.** Non avanzare a FDB / Mappa / 308 / Dossier.
