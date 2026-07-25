# W-D-fix — Discriminante multi-IP + lift proporzionato

**Data:** 2026-07-26 · **VERSION:** `0.10.46` · **Base:** `0.10.45` (no rollback a 0.10.44)  
**W2:** non avviato — stop dopo review diff.

## Rinumerazione

| Ondata | VERSION |
|--------|---------|
| W-D-fix | **0.10.46** |
| W2 | 0.10.47 |
| W4a…W8 | 0.10.48…0.10.53 |

Diff: [`docs/obs-wd-fix.diff.txt`](obs-wd-fix.diff.txt)

---

## X.1 — Impatto produzione 0.10.45 (read-only)

| Voce | Valore |
|------|--------|
| `DEDUP_WINDOW_S` | **60** (`observations_store.py:22`) |
| 0.10.45 live da | **2026-07-25 23:24:35Z** (container `StartedAt`) |

### X.1.2–X.1.3 Collassi post-deploy (entity_key MAC-only + IP in payload + hit_count>1)

| id | entity_key | hit_count | IP nel payload | kind |
|----|------------|-----------|----------------|------|
| **872183** | `60:B5:8D:6C:6D:53` | **5** | `192.168.1.1` | nmap |

| Metrica | Valore esatto |
|---------|----------------|
| Righe | **1** |
| Hit collassati (extra) | **4** (= 5−1) |
| MAC coinvolti | **1** (`60:B5:8D:6C:6D:53`) |

Post-deploy anche **56** righe MAC-only+IP con `hit_count=1` (un IP per MAC — nessun collasso multi-IP). Forma `mac_ip` post-0.10.45: **0**.

### X.1.4 Percorso `ip_addresses`

`write_and_materialize` (`materialize.py` **279–285**): anche con `created=False` (collasso raw) ogni envelope resta in `accepted` e passa a `materialize_host` → `observe_interface_ip` (`identity.py` **1365+**).

**Conclusione:** la scoperta/aggiornamento IP **non** dipende dal fatto che raw crei una riga nuova. Collasso = perdita di **storico raw** (payload tiene solo il first-writer), **non** perdita funzionale di binding: per il MAC collassato restano in `ip_addresses` id 1/172/173/174/175 (`.1.1` current + `.1.4`/`.1.5`/`.1.6`/`.1.9` con `last_seen` aggiornato al ciclo).

### X.1.5 Ricostruibilità

- Dal payload della riga **872183**: solo `.1.1` — gli altri IP **non** sono nel raw collassato.
- Da `ip_addresses` / altri cicli: **sì**, i binding multi-IP dell’asset 1 sono presenti.
- Perdita dichiarata: **storico append-only per quella finestra**, non i binding correnti.

---

## X.2 — Fix identità ≠ discriminante

| Funzione | Ruolo | Comportamento 0.10.46 |
|----------|-------|------------------------|
| `entity_key_for` | CHI | **Invariato:** MAC / endpoint / IP provisional |
| `fact_discriminant_for` | QUALE FATTO | IP (vuoto se già in endpoint key) |
| `compute_dedup_key` | dedup | `sensor\|bucket\|entity_key\|fact\|kind` — **source fuori** |

### Call site

| Consumatore | Impatto |
|-------------|---------|
| `upsert_observation_raw` / `compute_dedup_key` | Multi-IP → fatti distinti; stesso MAC+IP → refresh |
| `ObservationRaw.entity_key` | Resta MAC-scoped |
| T-b / cross-source | `source` fuori chiave — invariato |
| Provider ssdp/printer IP-only | Discriminante = IP (= entity_key); invariato |

**DEBT-TOPO-IP-CONTEXTUAL:** violato in 0.10.45, **ripristinato** in 0.10.46 (invariante: multi-IP stesso MAC non collassa).

---

## X.3 — Test

| Test | Esito |
|------|-------|
| `test_dedup_key_keeps_multi_ip` (5 fatti) | **PASS** |
| `test_entity_key_precedence` (MAC-scoped) | **PASS** (insieme al precedente) |
| `test_dedup_key_same_mac_same_ip_refreshes_in_window` | **PASS** |
| T-b, T-e, T-f | **PASS** |
| `test_m1_observation_store.py` | **PASS** |
| `test_trust_converge.py` | **PASS** |
| `test_mac_ip_policy.py` + identity (`migrate`/`asset`/`m3`/`identity_evidence`) | **PASS** |

Nota: il test errato `test_dedup_key_mac_scoped_collapses_multi_ip` (asserzione invertita in 0.10.45) è stato **rinominato** ripristinando l’asserzione protettiva a 5 fatti — dichiarato qui; invariante dipendente: DEBT-TOPO-IP-CONTEXTUAL.

---

## X.4 — Lift proporzionato

| Prima (0.10.45) | Dopo (0.10.46) |
|-----------------|----------------|
| `trust_level=confirmed_present` | **`known`** (Fritz 0.90, non apex portal) |
| Decisione richiamata da inventory | `on_fritz_active_evidence` in **trust.py**; inventory solo segnala |

**Reversibilità:** dopo lift + `active=False`, `_build_trust_plan` → `fritz_historical` → apply ripristina quarantena. Test aggiornato **PASS**. Portal (`observe_portal`) resta l’unico path a `confirmed_present`.

---

## X.5 — Registrazioni

| Debito | Nota |
|--------|------|
| **DEBT-LASTSEEN-DUAL-SEMANTICS** | Aperto — `last_seen=now` a demotion = chiusura amministrativa; W3 deve dichiarare semantica |
| DEBT-DOUBLE-CURRENT-IP | Cardinalità invariata (id 3+153; 15+853) |
| DEBT-PROVISIONAL-IDENTITY-MERGE | Invariato |

---

## X.6 / X.7 — Deploy

### Previsioni (prima)

| Metrica | Previsto |
|---------|----------|
| structural / needs_apply / T_backup | 0 / false / 0 |
| T_total | 8.8–9.2 s |
| assets / ip_cur / NP | 151 / 100 / 412 |
| ie / ilp / observations | 0 / 0 / assente |
| AD_devices_active | **69** (snapshot finestra) |
| delta contatori dominio | **0** |
| raw multi-IP post-deploy | 5 fatti su `60:B5:8D:…` al ciclo, altrimenti `available=false` |

### Assert (una riga)

`boot1 0.10.46: structural=0 needs_apply=false T_backup=0 T_total=8.933 · assets=151 ip_cur=100 NP=412 AD=69 ie/ilp=0/0 observations=absent · X.7 multi-IP naturale post-deploy=available=false (max raw ancora 872247; X.3.1 sufficiente)`

| X.7 | Esito |
|-----|-------|
| MAC con >1 raw post-deploy e IP diversi | **nessuno** — nessun ingest raw tra deploy e misura (~3 min; collector senza nuovo ciclo observations) |
| | **available=false (K3)** — non forzato traffico artificiale |

---

## Esito

X.2+X.3 verdi (identità MAC + discriminante IP) · X.4 lift `known` reversibile · X.6 assert OK.

**STOP:** non si accendono i writer. Prompt W2 dopo review di questo diff. Rollback ammesso solo a **`v0.10.45`**.
