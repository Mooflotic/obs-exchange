# W4a — Soggetto chassis e soppressione proposte a monte (0.10.48)

**Esito:** W4a.0.a chiusa · soppressione attiva · LGS310C verificato in prod · delta enumerato · **STOP prima di W4b**.

**Rollback:** tag `v0.10.47` · kill switch shadow `FACT_SHADOW_WRITERS_ENABLED=false` se serve.

---

## W4a.0.a — `facts/shadow.py` nel repo

| | |
|--|--|
| Prima | `??` untracked (violazione igiene; S1 assente dal tree git) |
| Ora | `git add` — tracciato |
| Diff W4a | contenuto **integrale** di `shadow.py` + `resolver.py` + modello `FactAssertion` in appendice di `obs-w4a.diff.txt` |

---

## W4a.0.b — Fritz 401 (STOP-5 credenziali)

| Domanda | Risposta |
|---------|----------|
| (1) Persistente o intermittente? Da quando? | **Persistente** nel buffer log: ogni ciclo `hostlist path fallito: HTTP Error 401: Unauthorized`. Prima occorrenza nel buffer: `2026-07-25T15:02:42Z`; ultima campionata `2026-07-25T23:58:49Z`. Anche `mesh SOAP … credentials_invalid` (28× / 2h). |
| (2) Correlato al purge o indipendente? | **Credenziali assenti**, non rate-limit intermittente. Su Cassiopea `.env`: `FRITZ_HOST` presente; `FRITZ_USERNAME` / `FRITZ_PASSWORD` **ASSENTI**. Codice: `collector/adapters/fritz.py` `_mesh_error` (≈880–884) mappa HTTP 401/403 → `credentials_invalid`. |
| (3) Cosa degrada con Fritz muto? | Hostlist / `discovery.fritz.active` / hostname Fritz / assoc mesh (0). Restano: nmap/ssdp/printer, diagnostica WLAN AP (spesso 200), SNMP. |

**STOP-5:** solo Michele può ripristinare le credenziali TR-064. Nessuna campagna di monitoraggio. Resto W4a proseguito. Debito: **DEBT-FRITZ-TR064-CREDENTIALS**.

---

## W4a.0.c — Cardinalità `asset.iface_ip`

Registro + KNOWN_DEBT: `cardinality=single` = **solo IP eletto**. Assenza in assertion ≠ IP inesistente. Aperto **DEBT-IFACE-IP-CARDINALITY-ROLE** (excl_key + role prima di W3). Ruoli non implementati.

## W4a.0.d — `subject_ref_interface`

Multi-NIC senza `is_primary` → `ValueError` (niente guess). Una sola NIC resta valida. S1 isola l’errore nello shadow path.

---

## W4a.1 — Misura candidati (prod, pre-soppressione)

### 1.1 Chassis

| Metrica | Valore |
|---------|--------|
| gruppi ≥2 membri | **15** |
| gruppi ≥1 nome manuale (meta) | **5** (chassis 1,3,15,18,21) |
| gruppi >1 nome manuale distinto | **0** |

**Caso LGS (MACs utente):**

| chassis_id | asset_id | nome | origin nome | MAC |
|------------|----------|------|-------------|-----|
| 23 | 2 | LGS328C | **unknown_nonempty** (I2: non taggato manual) | …1B:FF / …71:D5 |
| 23 | 109 | (assente) | absent | …1C:01 |
| 23 | 147 | (assente) | absent | …1C:05 |
| 23 | 151 | (assente) | absent | …1C:08 |
| 24 | 3 | LGS310C | **unknown_nonempty** | …7E:C7 / …7E:CF |
| 24 | 143 | (assente) | absent | DA:F6:… |

Le tre card UI non condividono un solo `chassis_id`: 147/151 ∈ 23 (LGS328C); 3 ∈ 24 (LGS310C).

### 1.2–1.5 Set A/B/C (pending)

| Set | \|set\| | quota /412 | ids |
|-----|--------|------------|-----|
| **A** (chassis con nome **manual** + proposta più debole) | **0** | 0% | — |
| **B** (duplicati stesso chassis+valore) | **3** | 0.728% | 266, 387, 393 |
| **C** (multi-NIC → adopt 409) | **7** | 1.699% | 6, 242, 266, 374, 375, 387, 393 |

**A=0 dichiarato:** LGS310C/LGS328C hanno nome nonempty **senza** `manual_overrides` / `field_sources.name=manual` → non autorità ≥ manual (I2).

### 1.6 Intersezione F1 Fritz pending (26 id)

| | ids |
|--|-----|
| ∩ A | — |
| ∩ B | — |
| ∩ C | **242** |

**Evidenza corrente (misurata, non dedotta):** subset con `last_seen` 2026-07-25 (es. 46,53,68,…) ancora `present`; subset `fritz_only` con `last_seen` 2026-07-18 e `source_reported_at=None` (299–342) — evidenza **non corrente** rispetto al mutismo Fritz 401.

---

## W4a.2 — Implementazione

| Punto | Dove |
|-------|------|
| Soppressione generazione (manual chassis + dedup) | `create_name_proposal` + `should_suppress_proposal` |
| Reconcile idempotente delete A ∪ B-extras | bootstrap step 4 |
| Risolvibilità calcolata | `actionable` / `resolvable` / `actionable_reason` su proposals |
| Sibling presentation | `chassis_role` / `chassis_canonical_*` + triage skip interface anonime |
| Adopt/409 | **intatto** (W4b) |
| Shadow `asset.name` | **non collegato** |
| I6 | `rg 'scoreSpecificity\|specificity' api/` → **vuoto** |

---

## W4a.3 — Previsioni (dichiarate pre-deploy) vs osservato

| Metrica | Previsto | Osservato |
|---------|----------|-----------|
| name_proposals | **410** (Δ −2) | **410** |
| soppresse | **266** (B dedup), **387** (B dedup); keep **393** | ids assenti; 393 pending |
| A | nessuna | archived_a=0 |
| nomi adottati modificati | 0 | 0 (LGS310C/LGS328C invariati) |
| assets / ip_current | 151 / 100 | 151 / 100 |
| needs_apply / T_backup / structural | false / 0 / 0 | false / 0 / 0 |
| breaker | closed | closed |
| fact_assertions | **56** (W4a non tocca writers) | **56** |
| AD (finestra) | **69** | **69** |
| T_total | report only | **9.121 s** |

**Assert one-liner:**

`boot1 0.10.48: structural=0 needs_apply=false T_backup=0 · NP=410 (Δ-2: 266,387 B-dedup) · assets=151 ip_cur=100 AD=69 · fact_assertions=56 · breaker=closed · I6=empty · adopted_names_changed=0`

### LGS in prod post-deploy

| asset | ruolo | actionable | card triage attesa |
|-------|-------|------------|-------------------|
| 3 LGS310C | canonical | false (multi-NIC) | ≤1 voce **unresolvable** (prop 6) |
| 147, 151, 109 | interface di LGS328C | false | **saltate** (non apparati anonimi) |

Tre card alta priorità → al massimo una voce non-adotta; zero `adotta` senza azione.

---

## W4a.4 — Test nominati

W4a.4.1–4.3 + facts/m1/trust/mac_ip/T-b/e/f/identity/shadow W2: **PASS** (sottoinsieme nominato; non «suite verde»).

---

## Diff

[`docs/obs-w4a.diff.txt`](obs-w4a.diff.txt) — **integrale** di ogni file toccato/creato + appendice full `shadow.py` / `resolver.py` / `FactAssertion`.

### Esclusioni dichiarate

Nessuna esclusione dei file dell’ondata. Non inclusi: artefatti di altre ondate non toccati (es. `obs-w2.md`), `node_modules`, `data/`.
