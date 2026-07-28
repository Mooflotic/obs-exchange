# OBS-FDB · O2-FIX — chiusura cause nostre + diff revisionabile

Prod: **0.10.66** (nessun bump: FASE 2 non eseguita).  
O2 ramo B (resa onesta) **accettato** — non riaperto.

## Conteggio righe artefatti

| Artefatto | `wc -l` |
|---|---|
| `obs-o2fix.md` | 184 |
| `obs-o2fix-coverage.diff.txt` | 324 |
| `obs-o2fix.diff.txt` | **non prodotto** (FASE 2 non eseguita) |

---

## PREVISIONI (pinnate PRIMA delle prove)

### C1
Atteso: `network_mode: host` → sorgente verso `192.168.1.2` = **192.168.1.3**.

### C2
Atteso: **host** e **collector** → stesso `Timeout: No Response` su `.1.2` e `.1.7` (stesso netns).  
Se host OK e container no → (c1) nostra.  
Predizione: **entrambi falliscono**.

### C3
Atteso: `SNMP_V3_USER` / `_AUTH_PASSWORD` / `_PRIV_PASSWORD` EMPTY → **v3 non testabile**.  
`snmp_poll.source` non è etichetta fissa: deriva da `SnmpCredentials.source`.

### C4
Atteso: `switches.ip` LGS328C=`.1.2`, LGS310C=`.1.7`; doppio `is_current` su `.1.2` noto (`DEBT-DOUBLE-CURRENT-IP`) ma **stesso** IP.

---

## FASE 1 — Misure

### C1 — Da dove parte il poll

| | |
|---|---|
| Servizio | **collector** |
| Funzione | `collector/collector/main.py` → ciclo SNMP/FDB → `collect_switch_snapshot` (`adapters/snmp_lldp.py`) |
| Ingest | POST `/api/ingest/fdb-switch` → `record_fdb_poll` / `record_snmp_poll` (`api/.../topology.py`) |
| Compose | `network_mode: host` (`docker-compose.yml` collector) |
| Inspect | `NetworkMode=host` |
| Host route | `192.168.1.2 dev eth0 src 192.168.1.3` |
| Container (python UDP connect) | dest `.1.2`/`.1.7` → **src 192.168.1.3** |

**Dichiarazione:** il poll esce come **192.168.1.3**, non come IP di bridge Docker.

→ **(c1) esclusa.**

### C2 — Stesso GET, due sorgenti (v2c, un OID, `-t 3 -r 1`, una prova)

OID: `1.3.6.1.2.1.1.1.0` (sysDescr). Community da env (**valore non riportato**).

| Prova | Comando (senza secret) | Esito integrale | ms |
|---|---|---|---|
| LGS328C host | `/usr/builtin/sbin/snmpwalk -v2c -c <REDACTED> -t 3 -r 1 -On 192.168.1.2 …` | `Timeout: No Response from 192.168.1.2` | 6162 |
| LGS310C host | idem `.1.7` | `Timeout: No Response from 192.168.1.7` | 6036 |
| LGS328C collector | `snmpget -v2c -c <REDACTED> -t 3 -r 1 -On 192.168.1.2 …` | `Timeout: No Response from 192.168.1.2.` | 6016 |
| LGS310C collector | idem `.1.7` | `Timeout: No Response from 192.168.1.7.` | 6016 |

Predizione C2 **confermata**. Host e container falliscono entrambi → non (c1).

### C3 — Versione + F3

**F3 — `snmp_poll.source`:**

- Impostato in `collect_switch_snapshot` → `"source": credentials.source` (`snmp_lldp.py`).
- `SnmpCredentials.source` (`collector/config.py`): `SNMPv3 {security_level}` se `version=="3"`, altrimenti `SNMPv2c`.
- **Non** è un’etichetta cablata falsa.
- GS308EP `source=SNMPv3 authPriv` con `at=2026-07-18`: meta **stalà** da quando `SNMP_VERSION` era 3 (backup `.env` storici). Poll LGS correnti: `source=SNMPv2c`.

**Env (solo presenza):**

| Chiave | present |
|---|---|
| `SNMP_VERSION` | sì → letterale **`2c`** |
| `SNMP_COMMUNITY` | sì |
| `SNMP_V3_USER` | **no (EMPTY)** |
| `SNMP_V3_AUTH_PASSWORD` | **no (EMPTY)** |
| `SNMP_V3_PRIV_PASSWORD` | **no (EMPTY)** |
| `SNMP_V3_AUTH_PROTOCOL` / `_PRIV_PROTOCOL` | sì (protocolli, senza secret) |
| `SNMP_PROFILE_*` | **NONE** |

**C3b/c:** «v3 non testabile: credenziali assenti (chiavi: `SNMP_V3_USER`, `SNMP_V3_AUTH_PASSWORD`, `SNMP_V3_PRIV_PASSWORD`)». Nessun tentativo alla cieca.

**C3d:** codice **supporta** profili per switch (`resolve_snmp_profile` + `SNMP_PROFILE_<LABEL>_*`), ma in prod **nessun** profilo è definito → i tre apparati condividono `default`. Registrato `DEBT-SNMP-PROFILE-PER-SWITCH`.

Progetto `docs/obs-fdb-lldp-passive.md` / `DEBT-FDB-LLDP-PASSIVE`: LGS → **SNMPv3 authPriv**. Poll attuale: **v2c**.

→ **(c2) non esclusa** (versione disallineata al progetto; v3 non verificabile senza secret).

### C4 — Bersaglio IP

| switch | `switches.ip` |
|---|---|
| LGS328C (id=1) | `192.168.1.2` |
| LGS310C (id=2) | `192.168.1.7` |

`ip_addresses` (enumerazione):

| id | ip | is_current | source | role | asset_id |
|---|---|---|---|---|---|
| **3** | 192.168.1.2 | 1 | mgmt | mgmt | 2 |
| **153** | 192.168.1.2 | 1 | fritz | '' | 2 |
| **5** | 192.168.1.7 | 1 | mgmt | mgmt | 3 |

Doppio current su `.1.2` = `DEBT-DOUBLE-CURRENT-IP` (stesso indirizzo). Il collector usa `switches.ip` → bersaglio **corretto**.

→ **(c3) esclusa.**

### (d) codice poll

Collector invoca SNMP, registra errore, `source` coerente con versione risolta. Nessun difetto di scheduling/gestione errore che spieghi il silenzio v2c.

→ **(d) esclusa.**

---

## Classificazione finale

**(c2)** — versione SNMP sbagliata rispetto al progetto (poll **v2c**, target documentato **v3 authPriv**); credenziali v3 **assenti** → **non ripristinabile da soli**.

**Non (a/b):** vietato dichiararle finché (c2) non è esclusa; (c2) resta aperta per mancanza di secret.

**FASE 2:** **non eseguita** (nessun deploy, VERSION resta 0.10.66). Resa onesta O2 invariata.

---

## FASE 3 — Diff revisionabile

`obs-o2fix-coverage.diff.txt`: solo estratto helper (`FDB_STALE_HOURS`, `fdbFreshnessWindowLabel`, `_utcMs`, `fdbPortCoverageState`, `fdbCoverageReport`, `fdbCoverageStatus`) + test copertura FDB/O2.  
**Non** ripubblicato `obs-o2.diff.txt`.

Esclusioni del diff corto: Plant, Oggi, portPresentation, oggiProblems, CHANGELOG, VERSION, resto di `observatoryUx.js`, monolite O2.

Test nominati: **2 pass** (`copertura FDB…`, `O2 FDB port states…`).

---

## Gate (output)

```
VIOLAZIONI: 0
RISULTATO: PASS (con 1 eccezione/i temporanea/e)
```

I6 `grep -RInE 'scoreSpecificity|specificity' api/` → **vuoto** (`I6_EMPTY`) — repo e NAS.

---

## Criteri di fallimento

| Criterio | Esito |
|---|---|
| (a/b) senza escludere (c1)(c2)(c3)(d) | **PASS** — (a/b) non dichiarata; (c2) residua |
| modifica config apparati | **PASS** — nessuna |
| SNMP SET / retry loop / community cieche | **PASS** |
| secret in chat/artefatti | **PASS** |
| riscrivere resa O2 | **PASS** |
| diff monolitico | **PASS** — diff corto 324 righe |

---

## RICHIESTA A MICHELE

**Causa residua:** (c2) — il collector interroga LGS328C/LGS310C in **SNMPv2c** mentre il progetto (`DEBT-FDB-LLDP-PASSIVE`) richiede **SNMPv3 authPriv**; le chiavi v3 in `.env` sono vuote quindi la versione corretta **non è testabile**.

**Alternative escluse:**

| Causa | Misura che la esclude |
|---|---|
| (c1) IP sorgente container | `NetworkMode=host`; src **192.168.1.3**; C2 host=collector entrambi timeout |
| (c3) bersaglio IP sbagliato | `switches.ip` `.1.2`/`.1.7`; mgmt `ip_addresses` id **3** e **5** |
| (d) bug codice poll | `source` da credenziali; errori registrati correttamente |
| (a/b) | **non dichiarata** — (c2) non esclusa |

**Singola azione:** nel `.env` su Cassiopea, valorizza `SNMP_V3_USER`, `SNMP_V3_AUTH_PASSWORD`, `SNMP_V3_PRIV_PASSWORD` (account RO già previsto per LGS) e imposta `SNMP_VERSION=3`, poi `docker compose up -d --force-recreate --no-deps collector`.

**Cosa cambierà / verifica:** al poll successivo `fdb_poll.ok=true` su LGS328C/LGS310C e porte id **{1..38}** con `last_fdb_at` entro 24 h (`misurata_fresca`); GS308EP resta `non_coperta` per limite. Se dopo v3 resta timeout, allora si riapre ACL/(a/b) con (c2) ormai esercitata.

Nessun segreto in questo report. Nessuna modifica agli apparati da parte dell’agente.
