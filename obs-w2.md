# W2 — Shadow writers `fact_assertion` (0.10.47)

**Esito:** W2.0.a chiusa · writer `asset.iface_ip` collegati · W2.5.3 / W2.5.6 verdi · assert W2.6 rispettato (con scarto `T_total` spiegato) · **STOP prima di W4a**.

**Rollback:** tag `v0.10.46` · kill switch `FACT_SHADOW_WRITERS_ENABLED=false` prima del rollback se il problema è solo nelle scritture shadow.

---

## W2.0.a — Discrepanza diff / sommario T-e/T-f

| | |
|--|--|
| Codice **deployato** 0.10.46 | `elect_interface_primary`: alla demotion `was_current and not is_current` → `last_seen = now` **PRESENTE** |
| Diff W-D-fix | Non includeva `identity.py` → **filtrato**, non assente |
| Gate W2 | **OK** — writers accesi |

---

## W2.0.b — Memoria `DEBT-TOPO-IP-CONTEXTUAL`

Ripristinate da history le voci perse (nessun bump per questa sola voce):

- `_resolve_ap_asset` usa `is_current` (0 client Wi‑Fi IP-only / 41) — **consumatore di correntezza → migrare in W5/W7**
- GS308EP asset 4: ownership binding storico `.3.20` stesso MAC
- Fritz asset 1: ×223 `ip_change`/24h documentati poi silenziati
- `DEBT-LAG-CASSIOPEA` chiuso 21/07 + `docs/obs-ux-ip-308-verifica.md`
- Invariante raw multi-IP + ripristino 0.10.46 mantenuti

---

## W2.1 — Inventario (dichiarato, non assunto)

### `api/app/facts/registry.py` — esiste

| fact_key | subject_scope | cardinality | excl_key | sources (authority via I5 rank) | ttl | consumers |
|----------|---------------|-------------|----------|----------------------------------|-----|-----------|
| `asset.name` | chassis | single | `name` | manual,ai,dhcp,fritz,oui,dns,mdns,ssdp | — | oggi,dossier,… |
| `iface.alias` | asset | single | `alias` | manual | — | dossier,plant |
| `asset.iface_ip` | **interface** (W2) | single | `asset.iface_ip:{iface_id}` | mgmt,dhcp,fritz,nmap,manual | 2h | **()** shadow only |
| `asset.mgmt_ip` | asset | single | `mgmt_ip` | mgmt,manual,fritz,nmap | 2h | monitoring,plant |
| `presence.portal` | asset | single | `presence` | portal | 24h | trust,inventory |
| `port.fdb_mac` | port | scoped | fdb:… | fdb | — | topology,presence |
| `rel.physical_link` | relation | scoped | physical_link | manual,auto | — | plant,topology |
| `os.guess` | asset | single | `os` | manual,nmap | — | dossier |
| `name_proposal` | chassis | multi | proposal:… | ai,dhcp,fritz,… | — | oggi |

### `api/app/facts/resolver.py` — R-A…R-H

| Regola | Stato |
|--------|--------|
| R-A refresh (stesso value+source → `last_seen`, `valid_from` invariato) | implementata |
| R-B supersession atomica (demote poi insert) | implementata |
| R-C weak_evidence (authority inferiore) | implementata |
| R-D manual pinned | implementata |
| R-E TTL / stale | implementata (`expire_stale_facts`) |
| R-F readmission cooldown 4h | implementata |
| R-G absent → None (I2) | implementata (`current`) |
| R-H semantic contradiction / conflict_review | implementata |

Nessuna regola necessaria a W2 mancante.

### `fact_assertions` in prod (pre-writer)

- Tabella + indici: `uq_fact_assertions_current_slot` (partial unique `state='current'`), `ix_fact_assertions_subject_state`, `ix_fact_assertions_fact_state`
- Righe pre-deploy: **0**

---

## W2.2 — Classi collegate / rinviate

| Classe | Decisione |
|--------|-----------|
| `asset.iface_ip` (iface IP) | **COLLEGATA** — soggetto=`interface`, excl_key=`asset.iface_ip:{id}`; scrive solo l’IP **eletto** post-`elect_interface_primary` |
| `asset.name` | **RINVIATA** a W4a/W4b (soggetto chassis) — non dimenticata |
| `os.guess` / hostname / altre | **NON collegate** — K3 / fuori perimetro W2 |

---

## W2.3 — Isolamento S1

| Meccanismo | Dove |
|------------|------|
| Barriera try/except su ogni apply | `facts/shadow.py` `safe_shadow_iface_ip` |
| SAVEPOINT (`begin_nested`) | stessa sessione ingest — rollback assertion ≠ rollback osservazione |
| Kill switch a caldo | `FACT_SHADOW_WRITERS_ENABLED` / `Settings.fact_shadow_writers_enabled` (default true; `false` spegne senza redeploy) |
| Circuit breaker | righe `<20000` · crescita `<2000/giorno` · tabella+indici `<50 MiB`; latch + log `top_groups` |
| K1 | nessuna scrittura su colonne Asset / campi reconcile |

---

## W2.4 — Osservabilità

`GET /api/admin/facts/shadow-stats` (operator): contatori per `(fact_key|source)`, `breaker_*`, `fact_assertions`. Nessuna UI.

---

## W2.5 — Test (nodi nominati)

| Nodo | Esito |
|------|-------|
| W2.5.1 idempotenza R-A | PASS |
| W2.5.2 supersession R-B | PASS |
| W2.5.3 Cassiopea dual-iface entrambe current | PASS |
| W2.5.4 GS308EP `.3.20`→`.1.8` | PASS |
| W2.5.5 fritz ≱ manual | PASS |
| W2.5.6 S1 IntegrityError isolato | PASS |
| W2.5.7 circuit breaker | PASS |
| `test_facts_resolver` (W1) | PASS |
| `test_m1_observation_store` | PASS |
| `test_trust_converge` | PASS |
| `test_mac_ip_policy` | PASS |
| T-b / T-e / T-f | PASS |
| identity (`test_asset_identity`, `test_m3_identity_presence`, `test_identity_evidence`, `test_migrate_identity`) | PASS |

Nessuna suite completa. Nessuna temporizzazione.

---

## W2.6 — Deploy 0.10.47

### Previsioni (dichiarate pre-deploy)

| Metrica | Previsto |
|---------|----------|
| boot1 structural | 0 |
| needs_apply | false |
| T_backup | 0 |
| T_total | 8.8–9.2 s |
| assets / ip_current / NP | 151 / 100 / 412 |
| identity_evidence / link_proposals | 0 / 0 (tabella assente) |
| `observations` in sqlite_master | assente |
| AD_devices_active | **69** (snapshot finestra 24h) |
| fact_assertions avvio | 0 |
| fact_assertions post 1° ciclo | **O(10²) ≈ ip_current (100)** — una assertion per binding primario eletto rinfrescato, non per osservazione raw |

Snapshot pre-op: `data/backups/pre-w2-20260726-014717.db` (+ `pre-deploy-20260726-0147.db`). Protetti intatti.

### Osservato

| Metrica | Osservato | vs previsto |
|---------|-----------|-------------|
| VERSION | 0.10.47 | ok |
| structural | 0 (`changed_assets` trust / conflitti=0) | ok |
| needs_apply | false | ok |
| T_backup | 0.0 | ok |
| T_total | **9.263 s** | **+0.063 s** oltre banda 9.2 — scarto: passo chassis 0.9 s + jitter uvicorn post-rebuild; nessun `needs_apply`/backup; **non** ridefinita la metrica |
| assets / ip_cur / NP | 151 / 100 / 412 | ok |
| ie / link_proposals | 0 / assente | ok |
| observations | assente | ok |
| AD_devices_active | 69 | ok |
| fact_assertions @boot | 0 | ok |
| fact_assertions post ciclo | **56** (tutte `current`, subject=`interface`) | stesso ordine di grandezza di ~100; sotto perché Fritz hostlist **401** e il ciclo ha rinfrescato un sottoinsieme (nmap/ssdp/mgmt); crescita per osservazione eletta, non per raw |
| breaker | **closed** | ok |
| errori shadow isolati | 0 (processo API) | ok |

**Assert one-liner:**

`boot1 0.10.47: structural=0 needs_apply=false T_backup=0 T_total=9.263 · NP=412 assets=151 ip_cur=100 ie/ilp=0/0 observations=absent · AD_devices_active=69 · fact_assertions=56 · breaker=closed`

---

## W2.7 — Verifica successiva (una volta, non serie)

Alla prossima occasione naturale: leggere `fact_assertions`, `breaker`, contatori shadow-stats. Se breaker open → quello è il report.

---

## Rinviate esplicitamente

- **W4a** (soggetto NameProposal / chassis) — STOP qui; arriva dopo review del diff
- Consumatori live di `fact_assertions` (W5/W7), incluso `_resolve_ap_asset`
- Collasso doppi-current IP (W3)
- `asset.name` shadow

## Diff

[`docs/obs-w2.diff.txt`](obs-w2.diff.txt)
