# F0 — Verifica ripristino Fritz (senza bump VERSION)

**Data:** 2026-07-27 · **Corrente:** 0.10.51 · **Esito: VERDE**

Zero segreti in questo documento. Solo booleani di presenza e esiti.

---

## F0.1 Baseline pre-riavvio

### F0.1.1 Chiavi `.env` (disco)

| Chiave | Presente e non vuota |
|---|---|
| `FRITZ_HOST` | **True** |
| `FRITZ_USERNAME` | **True** |
| `FRITZ_PASSWORD` | **True** |

### F0.1.2 Contatori

| Metrica | Valore |
|---|---|
| assets | 151 |
| ip_current | 100 |
| name_proposals totale / pending | 409 / 78 |
| fact_assertions | 253 |
| AD (24h) | 62 |
| breaker | closed |
| unknown_source | 0 |

### F0.1.3 Candidati quarantena / stale

**ops ∈ {fritz_historical, stale_unlocated}** (42 id):  
83, 84, 85, 86, 92, 95, 106, 109, 110, 116, 117, 118, 119, 120, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 151  

Inclusi gli attesi 116, 136, 140, 145, 148.

**trust_level = fritz_historical** (26 id):  
83, 84, 86, 92, 95, 106, 109, 116, 117, 118, 119, 120, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 141

### F0.1.4 Snapshot anti-resurrezione

| Check | Stato |
|---|---|
| asset 4 | `.1.8` current · `.3.20` non current |
| asset 3 | `.1.7` current · `.2.161` non current · manual `LGS310C` |
| asset 5 | `.1.3` current |
| asset 6 | `.3.24` current (`.1.3` non current su questa NIC) |
| asset 98, 150 | nome assente · no `field_sources.name=manual` |
| nomi manual | **30** id (misurato; non 31): 3,5,12,15,19,20,28,30,31,32,34,37,38,42,45,46,48,49,60,64,68,76,82,88,108,112,114,115,121,135 |
| NameProposal fritz rejected | **80** |

### F0.1.5 Snapshot DB

`data/backups/pre-fritz-restore-20260727-190716.db` · protetti intatti.

---

## F0.2 Riavvio

1. `docker compose restart collector` — **insufficiente**: chiavi su disco True, nel container `USERNAME`/`PASSWORD` **False** (len=0). Hostlist/mesh → 401 / `credentials_invalid`.
2. `docker compose up -d --force-recreate --no-deps collector` (solo collector) — dopo: chiavi container True (len user=11, pass=20). **Nessun** 401 successivo (conteggio log post-recreate = **0**).

Atteso un ciclo naturale: discovery ~15 min; hostlist è sul path topology 60s. Il job `run_topology_cycle` risulta spesso **bloccato** dopo il post Fritz (probabile FDB; pre-esistente «max instances»). Verifica path Fritz eseguita con le stesse funzioni del ciclo (conteggi). Tempo dall’inizio recreate al post osservazioni: ~8–11 min di wall-clock osservato.

---

## F0.3 Verifica

| Check | Esito |
|---|---|
| F0.3.1 401 / credentials_invalid **dopo recreate** | **NO** (0 occorrenze). Prima del recreate: SÌ (hostlist 401, mesh credentials_invalid). |
| F0.3.2 hostlist | **94** host (poi 93 su seconda misura) |
| F0.3.2 mesh | status=`available`, **6** associazioni |
| F0.3.3 copertura corrente | **88** asset con `discovery.fritz.last_observed_at` ≥ recreate (id: 1–14,16–72,79,82,85,88,98,108,109,112,119,120,124,125,133–137) |
| F0.3.4 lift | **solo id 109**: trust `fritz_historical`→**`known`**, ops→`active`. **Non** `confirmed_present`. |
| F0.3.5 ancora in quarantena/stale | 41 id (lista sotto) |

### F0.3.5 Ancora `fritz_historical` / `stale_unlocated` (perché)

- **Fresh ma `active=False`** (Fritz li vede inattivi → nessun lift): 85, 119, 120, 124, 125, 133, 134, 137  
- **Fresh `active=True` ma resta `stale_unlocated`**: **136** — `lift_fritz_quarantine_on_active` esce solo da `fritz_historical`, non da `stale_unlocated` (DEBT-PRESENCE-SOURCE-OUTAGE; trust layer non corretto in F0).  
- **Non fresh / non sollevati** (Fritz non li riporta attivi o non in hostlist corrente): resto della lista 83,84,86,92,95,106,110,116–118,122,123,126–132,138–151 ecc.

---

## F0.4 Gate anti-resurrezione

| Voce | Esito |
|---|---|
| F0.4.1 `.3.20` non current; `.1.8` current | **OK** |
| F0.4.2 `.2.161` non current; `.1.7` current | **OK** |
| F0.4.3 Cassiopea `.1.3`@5 e `.3.24`@6 current | **OK** |
| F0.4.4 insieme manual invariato (30 id, stessi valori) | **OK** |
| F0.4.5 asset 98/150 nome ancora assente | **OK** |
| F0.4.6 fritz rejected ancora 80; proposte nuove = **[]** | **OK** |
| F0.4.7 riammissioni IP storiche | **nessuna**. Demotion: asset **43** `192.168.2.101` current→non (Fritz `active=False`) — ip_current 100→**99** |
| F0.4.8 unknown_source | **0** |
| F0.4.9 breaker | **closed**. fact_assertions 253→**260** (Δ+7, tutti `asset.iface_ip` current nuovi: iface 70,6,5,40,34,42,36) — crescita per cambiamento, non ballooning |

---

## F0.5 Esito

**VERDE** — credenziali valide dopo recreate; hostlist+mesh ok; copertura enumerata; F0.4 rispettato; breaker closed.

- **DEBT-FRITZ-TR064-CREDENTIALS** → **CHIUSO** (misura: recreate necessario; `restart` non ricarica `.env`).
- **DEBT-PRESENCE-SOURCE-OUTAGE** resta **APERTO**; rientrati in evidenza Fritz (sottoinsieme): vedi F0.3.3; lift trust solo **109**; **136** ancora `stale_unlocated` con active=True.

Nota operativa: `run_topology_cycle` può appendersi su FDB dopo il post Fritz → job topology «max instances». Non è un fallimento credenziali.

---

## F0.6 Previsione boot1 api (0.10.52)

Dry-run `reconcile_trust_history` **ora** (writer quiet lato api):

| Campo | Atteso boot1 0.10.52 |
|---|---|
| `needs_apply` | **true** |
| `T_backup` | **> 0** (true) |
| `structural` | **1** |
| id | **[109]** — ops/trust ora `active`/`known` (lift live) → plan atteso `fritz_historical` / `fritz_historical` |

Gate binario di regime: dopo apply+secondo boot, `needs_apply=false` · `T_backup=0` · `structural=0`.
