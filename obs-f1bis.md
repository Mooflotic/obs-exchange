# F1-bis — Riqualifica gate F1 + correzioni minime

**Data:** 2026-07-26 · **VERSION deploy:** `0.10.44` · **Ramo:** `feature/obs-currency`  
**STOP F1:** **REVOCATO** (criterio F1.2/F1.3 mal specificato; non rimesso in discussione).  
**W2:** non eseguito (gate T-b / T-e / T-f aperti).

## Rinumerazione ondate

| Ondata | VERSION |
|--------|---------|
| W-C (questo) | **0.10.44** |
| W2 | 0.10.45 |
| W4a | 0.10.46 |
| W4b | 0.10.47 |
| W5 | 0.10.48 |
| W6 | 0.10.49 |
| W7 | 0.10.50 |
| W8 | 0.10.51 |

---

## W-A — Riqualifica (read-only)

### A.1 NameProposal fritz `pending` — violazione = evidenza non-current

Lista esaminata (26 id): 46, 53, 68, 73, 98, 212, 224, 236, 242, 299, 301, 303, 308, 318, 320, 322, 324, 326, 328, 330, 332, 334, 336, 338, 340, 342.

Criterio: assenza di IP fritz `is_current=1` sull’asset **e** `discovery.fritz.active` non vero (evidenza Fritz non più viva). `name_proposals` non ha colonna evidence: supporto = IP fritz current e/o discovery fritz attivo.

| Set | Count | id |
|-----|-------|-----|
| **Violazione (evidenza non-current)** | **3** | **212** (asset 88), **301** (asset 118, IP storico `.2.55`), **318** (asset 122, IP storico `.2.225`) |
| Legittime (sorgente viva) | 23 | resto della lista (es. **242** asset 10: `fritz.active=true`, hostname allineato) |

Set piccolo e giustificato (Fritz inattivo / IP storicizzati). Nessuna azione ora (W4a: soppressione alla generazione).

### A.2 IP fritz `is_current=1` — violazione = supersedibile non eletto

Stessa interfaccia: riga più recente con autorità ≥ fritz che avrebbe dovuto soppiantare il current fritz.

| Set | Count |
|-----|-------|
| **Violazione** | **0** |

**Asset 4 (caso fondativo CHIUSO):** `192.168.3.20` storico · `192.168.1.8` corrente (mgmt).  
**Asset 3:** `192.168.2.161` storico · `192.168.1.7` corrente (mgmt).

### A.3 Controllo inverso — `n_iface > n_ip_current`

**54** asset. Molti sono L2-only / privacy (0 IP current, atteso). Candidati ad alto valore (hanno IP **storicizzati** e potrebbero essere concurrent erronei):

| asset_id | n_iface | n_cur | iface MAC | IP current | IP storici (id / ip / source / last_seen) |
|----------|---------|-------|-----------|------------|-------------------------------------------|
| 3 | 2 | 1 | D8:EC:5E:C5:7E:C7, …:CF | 5 / `.1.7` mgmt | 856 / `.2.161` fritz / 2026-07-23 |
| 6 | 1 | 1 | 24:4B:FE:84:6A:02 | 855 / `.3.24` fritz | 11 / `.1.3` fritz — **vedi B.1** (non in A.3 numerico: 1=1) |
| 82 | 2 | 0 | 38:A6:CE:40:A7:72/76 | — | 143 / `.2.120` fritz |
| 91 | 1 | 0 | 3A:D3:67:3C:D4:FD | — | 852 / `.2.254` fritz |
| 89 | 1 | 0 | 3A:53:67:1F:9C:AA | — | 854 / `.2.101` fritz |
| 99 | 1 | 0 | 72:A8:57:FD:86:F9 | — | 851 / `.2.107` fritz |
| 106 | 1 | 0 | CA:C3:F2:A0:30:09 | — | 150 / `.2.204` fritz |
| 108 | 1 | 0 | D6:A9:77:61:25:17 | — | 227 / `.2.195` fritz |
| 118 | 1 | 0 | 5E:55:DB:65:72:1F | — | 155 / `.2.55` fritz |
| 122 | 1 | 0 | A6:EF:8A:16:89:E8 | — | 159 / `.2.225` fritz |
| 95 | 1 | 0 | 5C:0C:E6:EE:4C:85 | — | 148 / `.2.58` fritz |

Lista completa dei 54 id: 3, 7, 8, 10, 15, 43, 58, 80, 81, 82, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 118, 122, 135, 136, 137, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151.

### A.4 Esito W-A

**Purge CONFERMATO PULITO. STOP resta revocato.**

---

## W-B — Tre difetti

### B.1 Cassiopea asset 6 — DEBT-IP-CURRENT-SCOPE-PER-ASSET

| Voce | Fatto |
|------|--------|
| DB | iface unica id=6 MAC `24:4B:FE:84:6A:02`; IP **11** `.1.3` fritz `is_current=0`; IP **855** `.3.24` fritz `is_current=1` |
| Asset 5 | NIC1 MAC `:01` già tiene `.1.3` **current** (id 9) |
| B.1.a ping da `api` | `.1.3` ok · `.3.24` **100% loss** → `available=false` (K3), non dedotto |
| B.1.b vincolo | applicativo **per interfaccia**: `elect_current` / «Elect a single is_current primary per interface» in `api/app/services/identity.py` ~874–924. Nessun UNIQUE SQL per-asset |
| B.1.c | **Nessuna patch dati.** Registrato **DEBT-IP-CURRENT-SCOPE-PER-ASSET** (`KNOWN_DEBT.md`). Chiusura in W1/W2 quando scope interfaccia + modeling NIC2. Test di non-regressione obbligatorio |
| UI | finché aperto: `.1.3` su asset 6 resta storico; non forzare doppio current |

### B.2 Righe IP duplicate — solo enumerazione

**Coppia `(asset_id, ip)` con >1 riga (stesso asset):**

| asset_id | ip | id righe | is_current | source |
|----------|-----|----------|------------|--------|
| 2 | 192.168.1.2 | 3, 153 | 1, 1 | mgmt, fritz |

**Stesso IP su asset diversi** (sintomo DEBT-ENTITY-KEY-MAC-IP / refresh-as-transition; non collassare):

| ip | id / asset / current |
|----|----------------------|
| 192.168.2.254 | 113/a61 cur=1 · 852/a91 cur=0 |
| 192.168.2.195 | 108/a58 cur=1 · 227/a108 cur=0 |
| 192.168.1.3 | 9/a5 cur=1 · 11/a6 cur=0 |
| 192.168.2.101 | 78/a43 cur=1 · 854/a89 cur=0 |
| 192.168.2.107 | 13/a9 cur=1 · 851/a99 cur=0 |
| 192.168.2.108 | 15/a11 cur=1 · 853/a138 cur=1 |
| 192.168.1.117 | 51/a30 cur=1 · 394/a51 cur=0 |

Collegato a **DEBT-ENTITY-KEY-MAC-IP** (T-b) — blocca W2.

### B.3 Nomi manuali vuoti — unica scrittura W-B

**PREVISIONE (prima dell’esecuzione):** `name_proposals = 412` (lo script non crea NP; nessun writer).

| | Valore |
|--|--------|
| Snapshot | `data/backups/pre-b3-empty-manual-names-20260725-230605.db` |
| Modificati | asset **98**, **150** — rimosso `field_sources.name` manual + `name` da `manual_overrides`; `name` resta `''` (assenza) |
| Audit | `audit_log.action=f1bis.b3.normalize_empty_manual_name` |
| `name_proposals` dopo | **412** |
| Nuove NP (per id) | **[]** |
| 2ª esecuzione | `modified=0` (idempotente) |
| Backup protetti | non toccati |

UI: assenza → presentazione esistente «Device senza nome» / italic unnamed (non stringa vuota grezza). Nessun nome inventato.

---

## W-C — DEBT-RECONCILE-CHURN-1 → 0.10.44

### C.2 Diagnosi (limitata)

Ramo: `reconcile_asset_presence` → `reliable=True` (qui: `reachability.status=reachable` su asset **116**, **0 interfacce**) → desidera `active`.

Buco: `inventory_may_set_operational_state` permetteva `fritz_historical`→`active` se `reliable=True` (`api/app/services/inventory.py`, pre-fix ~168–171).

Gerarchia dichiarata: `archived > trust_quarantine > trust_protected > inventory_presence`. Inventory non deve sollevare `trust_quarantine`.

### C.3 Fix (classe)

`inventory_may_set_operational_state`: se `current_state` o `trust_level` è `fritz_historical`, rifiuta `desired ∈ {active, stale_unlocated}`.

Test: `tests/test_trust_converge.py::test_quarantine_zero_interfaces_inventory_cannot_set_active` (+ matrice aggiornata). Locale: **6 passed**.

### C.5 Previsioni PRE-DEPLOY (dichiarate prima)

| Metrica | Previsto |
|---------|----------|
| boot1 structural | 0 |
| boot1 needs_apply | false |
| boot1 T_backup | 0 |
| regime T_total | 8.8–9.0 s |
| assets / AD / ip_current / NP | 151 / 82 / 100 / **412** |
| identity_evidence / link_proposals | 0 / 0 |
| tabella `observations` | assente |

### C.6 Assert post-deploy (una riga)

`boot1 0.10.44: structural=1 needs_apply=true T_backup=119.244 T_total=128.734 · NP=412 assets=151 ip_cur=100 ie/ilp=0/0 observations=absent · AD_devices_active=69 (≠82, finestra 24h)`

**C.5 NON rispettato su boot1** (structural/needs_apply/T_backup).

**Scarto spiegato (non riformula la metrica boot1):** all’ingresso del container il DB aveva ancora il mismatch pre-fix (116: `trust=fritz_historical`, `op=active`). Boot1 ha *sanato* (apply structural=1 + backup). Post-apply:

| Check | Osservato |
|-------|-----------|
| asset 116 op_state | `fritz_historical` |
| `may_set(...→active, reliable=True)` | `False` |
| `reconcile_asset_presence` | resta `fritz_historical` |
| dry_run trust post-boot | `needs_apply=false`, `structural_actions=[]` |

Il fix di **classe** tiene; il boot1 ha pagato il debito residuo pre-deploy. Rollback ammesso: tag `v0.10.43`. Nessun secondo boot misurato (vietata campagna).

Debito **DEBT-RECONCILE-CHURN-1** marcato CHIUSO in codice; conferma operativa regime = prossimo boot naturale senza campagna.

---

## Gate W2 (invariato, non eseguito)

W2 writers **non partono** finché **DEBT-ENTITY-KEY-MAC-IP** (T-b) e **DEBT-IP-MIGRATION-NONETYPE** (T-e/T-f) non risolti o esentati per iscritto.

## Debiti aggiornati

| Debito | Stato |
|--------|--------|
| DEBT-RECONCILE-CHURN-1 | chiuso in codice 0.10.44 (boot1 ha ancora sanato residuo) |
| DEBT-IP-CURRENT-SCOPE-PER-ASSET | **aperto** (asset 6) |
| DEBT-ENTITY-KEY-MAC-IP | aperto, bloccante W2 (+ enum B.2) |
| DEBT-IP-MIGRATION-NONETYPE | aperto, bloccante W2 |

## Igiene tree

- Report: `docs/obs-f1bis.md`
- Script una-tantum: `scripts/normalize_empty_manual_names.py` (copia operativa NAS: `data/db/normalize_empty_manual_names.py`)
- Nessun bump per B.3; bump solo W-C → `VERSION` / `web/package.json` / `CHANGELOG` = **0.10.44**

## Esito

| Blocco | Esito |
|--------|--------|
| W-A | pulito — purge OK, STOP revocato |
| W-B | eseguito (B.1 debito · B.2 enum · B.3 normalizzato) |
| W-C | fix codice deployato; **FERMA su C.5** (boot1 ≠ previsione) |

**Non si prosegue a W2 / implementazione funzionale / F2** finché Michele non decide sul boot1 (accettare sanata one-shot + dry_run verde post-boot, oppure rollback `v0.10.43`, oppure un boot2 naturale fuori campagna).
