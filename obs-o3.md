# OBS-FDB · O3 — ripristino poll lato nostro (0.10.66, solo config)

O2 / O2-FIX accettati — non riaperti. Nessun bump VERSION (solo `.env`). Nessun merge main.

## Conteggio righe artefatti

| Artefatto | `wc -l` |
|---|---|
| `obs-o3.md` | 171 |
| `obs-o3.diff.txt` | 496 |

---

## S1 — Ricerca credenziali (nomi / lunghezze, mai valori)

### S1a — File candidati

| File | note |
|---|---|
| `.env` | attivo; `env_file` di api+collector |
| `.env.bak-0910` | bak 2026-07-22 |
| `.env.bak-0910-preOS` | bak |
| `.env.bak-099` | bak |
| `.env.bak-prekuma-20260720-1746` | bak |
| `.env.bak.20260727-185852` | bak post-regressione (allineato allo stato vuoto) |
| `.env.example` | template |

Compose: collector/api `env_file: .env`; `environment` solo path/TZ/API (nessun secret inline).

### S1b/c — Chiavi SNMP live `.env` (prima del restore)

| key | commented | len | empty | quote/ws/CR |
|---|---|---|---|---|
| SNMP_DEFAULT_PROFILE | no | 7 | no | clean |
| SNMP_VERSION | no | **2** | no | clean (=`2c` letterale, non stampato oltre la len) |
| SNMP_COMMUNITY | no | 6 | no | clean |
| SNMP_V3_USER | no | **0** | **sì** | |
| SNMP_V3_AUTH_PROTOCOL | no | 3 | no | |
| SNMP_V3_AUTH_PASSWORD | no | **0** | **sì** | |
| SNMP_V3_PRIV_PROTOCOL | no | 3 | no | |
| SNMP_V3_PRIV_PASSWORD | no | **0** | **sì** | |

Nei **bak pre-27/07** (es. `.env.bak-0910`): `SNMP_VERSION` len=**1**; `SNMP_V3_USER` len=**11**; `SNMP_V3_AUTH_PASSWORD` len=**23**; `SNMP_V3_PRIV_PASSWORD` len=**26**; anche `SNMP_NAS_*` presenti (non usati per switch).

### S1d — Processo collector (prima)

Stesse chiavi del live; V3 len=0; VERSION len=2. Nessuna `SNMP_NAS_*` nel processo (assenti dal live `.env`).

### S1e — Diff file vs processo

Chiavi live ↔ processo allineate; il gap era **valori V3 azzerati nel file attivo**, non un `env_file` mancante.

### S1g — Codice

`resolve_snmp_profile` legge `SNMP_VERSION`, `SNMP_V3_*`, `SNMP_COMMUNITY`, oppure `SNMP_PROFILE_<LABEL>_*`. Nomi trovati nei bak = nomi che il codice legge. Nessun alias mancante.

### Esito S1

**Non (v).** Credenziali v3 **valorizzate nei `.env.bak-*`**, azzerate nel `.env` attivo (regressione 2026-07-27) → ripristino S4 da bak (stessi nomi chiave).  
Classificazione operativa: **(i)-restore** — presenti e valorizzate fuori dal processo attivo.

---

## S2 — Source dei poll riusciti 25/07

| Via | Esito |
|---|---|
| S2a `observations_raw` | nessun payload SNMPv/fdb-switch sul 25/07 (ingest FDB non passa da quella tabella) |
| S2b logs collector 100h | 0 righe 25/07 con snmp/fdb (ritenzione log) |
| S2c audit_log | 0 hit |
| S2d backup `pre-4b-drop-20260725-161330.db` | copia RO su volume1, letta, **cancellata**; originale intatto |

**S2d osservato (backup 16:13 del 25/07):**

- LGS328C: `fdb_ok=true`, `snmp_source=SNMPv3 authPriv`, `at≈14:13Z`
- LGS310C: idem `SNMPv3 authPriv`
- GS308EP: fail timeout (invariato)

→ i poll riusciti del 25/07 furono **v3**, non v2c. Le chiavi v3 sono state **perse dal `.env` attivo**, non «community cambiata».

---

## S3 — Previsioni (pinnate PRIMA di S4)

- Dopo restore V3 + `SNMP_VERSION` len=1 + recreate collector: `fdb_poll.ok=true`, `source=SNMPv3 authPriv` su LGS.
- Porte **{1..38}** → `misurata_fresca`.
- GS308EP **{39..46}** restano `non_coperta` (FDB non supportato); SNMP ignorato in log — non peggioramento.

---

## S4 — Ripristino

- **S4a:** copia `.env.bak.o3-20260728-213623` (permessi 0644, non pubblicata).
- **S4b:** da `.env.bak-0910` ripristinate solo le righe  
  `SNMP_VERSION`, `SNMP_V3_USER`, `SNMP_V3_AUTH_PROTOCOL`, `SNMP_V3_AUTH_PASSWORD`, `SNMP_V3_PRIV_PROTOCOL`, `SNMP_V3_PRIV_PASSWORD`.  
  Nessun’altra riga. Nessun valore stampato.
- **S4c:** changed_keys solo  
  `(VERSION 2→1)`, `(USER 0→11)`, `(AUTH_PASSWORD 0→23)`, `(PRIV_PASSWORD 0→26)`.
- **S4d:** `docker compose up -d --force-recreate --no-deps collector`  
  Processo post: VERSION len=1, USER 11, AUTH 23, PRIV 26.
- **S4e:** un ciclo poll naturale (~60s).

Log (integrale, senza secret):

```
snmp: 2 switch da interrogare
snmp 328c@192.168.1.2: 75 MAC, 28 interfacce → 200
snmp 310c@192.168.1.7: 60 MAC, 10 interfacce → 200
308ep: SNMP ignorato (mappa manuale e dati FDB/LLDP dallo switch upstream)
```

---

## S5 — Verifica porte (prima → dopo)

**Prima (O2):** fresca ∅; vecchia {1..38}; non {39..46}.

**Dopo:**

| Stato | port id |
|---|---|
| `misurata_fresca` | **{1..38}** (`last_fdb_at≈2026-07-28 21:37–21:38Z`, età ≈0.01–0.02 h) |
| `misurata_vecchia` | **∅** |
| `non_coperta` | **{39..46}** motivo «FDB non supportato dall'apparato» |

| switch | fdb_poll.ok | at | source | error |
|---|---|---|---|---|
| LGS328C | true | 2026-07-28T21:37:57.609941Z | SNMPv3 authPriv | '' |
| LGS310C | true | 2026-07-28T21:38:14.721168Z | SNMPv3 authPriv | '' |
| GS308EP | false (meta storica) | 2026-07-18… | SNMPv3 authPriv | timeout storico; poll **ignorato** ora |

Ripristino **completo** su LGS; GS308EP invariato per progetto. Resa onesta O2 non toccata.

S6: **non applicabile** (niente timeout residuo su LGS).

---

## S7 — Inventario segnale difensivo (input O4, nessuna implementazione)

| Segnale | Disponibile? | Dove | Cosa manca per farne un segnale |
|---|---|---|---|
| MAC per porta | **sì** | `switch_ports.observed_macs` + `last_fdb_at` | UI/card Oggi tipizzata; soglia età |
| MAC-move fra porte | **parziale** | stesso MAC su >1 porta nello snapshot (58 MAC multi-porta misurati; molti via uplink 310c:8) | storico temporale move; escludere uplink/trunk |
| Solo L2 (no IP) | **sì come dato grezzo** | MAC in FDB senza binding IP corrente | join esplicito + card «L2-only» |
| MAC mai visto | **no come serie** | solo snapshot corrente | baseline/storico first-seen FDB |
| uplink vs accesso | **parziale** | ruoli porta / notes / mac flood su uplink | classificazione porta affidabile + policy alert |

---

## Gate

```
VIOLAZIONI: 0
RISULTATO: PASS (con 1 eccezione/i temporanea/e)
```

I6: vuoto (repo + NAS). Health: `version=0.10.66`.

---

## Diff

Solo `docs/KNOWN_DEBT.md` (chiusura debito). **`.env` escluso**. Nessun file runtime.

## Criteri di fallimento

Tutti **PASS** (nessun secret in artefatti; nessun inspect env; S1 completo; no SET apparati; backup protetto solo copiato/letto/cancellata la copia; `.env` solo righe previste; ripristino LGS completo dichiarato tale; O2 UI non riscritta).

## ASSERT

Poll FDB LGS ripristinato con **SNMPv3 authPriv** da restore `.env` bak. STOP review — no O4/Mappa/308/merge.
