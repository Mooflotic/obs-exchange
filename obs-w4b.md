# W4b — Rename/adoption chassis + provenienza + anti-ballooning (0.10.49)

**Esito:** W4b.0.a/b verdi · `asset.name` collegato agli shadow writers · LGS310C manual · deploy 0.10.49 · **STOP prima di W5**.

**Rollback:** tag `v0.10.48` · kill switch `FACT_SHADOW_WRITERS_ENABLED=false` se solo shadow.

**Rinumerazione:** W4b → **0.10.49** · W5→0.10.50 · W6→0.10.51 · W7→0.10.52 · W8→0.10.53

Diff: [`docs/obs-w4b.diff.txt`](obs-w4b.diff.txt)

---

## W4b.0.a — Provenienza non si traduce (VERDE)

### Misura pre-correzione (prod, read-only)

| Sorgente `fact_assertions` | state | n |
|----------------------------|-------|---|
| nmap | historical | 187 |
| fritz | current | 58 |
| mgmt | current | 3 |
| nmap | current | 2 |
| **totale** | | **250** |

`IpAddress` current sources: fritz 93 · mgmt 3 · nmap 4.  
Mismatch `fact_assertions.source` vs `IpAddress.source` sullo stesso IP corrente: **0**.

Sorgenti reali dichiarate nel registro I5 (nessuna seconda gerarchia):  
`asset.iface_ip` → mgmt, dhcp, fritz, nmap, manual, **scan, arp, icmp** (rank 75 come nmap).  
Authority non determinabile → tier `unknown` (10).

### Fix

- Eliminata `_SOURCE_MAP` / default-to-nmap.
- Sorgente non in `FactSpec.sources` → rifiuto, `unknown_source++`, log una volta; S1 isolato.
- Bonifica: righe `asset.iface_ip` con `source=nmap` marcate `provenance_unreliable` (non ricostruibile scan→nmap vs nmap autentico). Idempotente.

### Test W4b.5.1

PASS — unknown source rifiutata, 0 righe, contatore ≥1.

---

## W4b.0.b — Anti-ballooning (VERDE)

- Docstring resolver: lo store cresce per **cambiamento / divergenza distinta**, non per osservazione.
- `_upsert_divergence`: stesso `(excl_key, value_norm, source, reason)` → `last_seen_at` + `occurrences`.
- Ballooning già in prod: 187 historical `nmap`/`weak_evidence` (evidenza del difetto). Non collassati (fuori scope); il fix ferma la crescita futura.

### Test W4b.5.2

PASS — 50 OUI deboli → **1** riga historical, `occurrences=50`.

**Gate W4b.0:** a+b verdi → `asset.name` **collegato** (`safe_shadow_asset_name`).

---

## W4b.0.c — Fritz (non bloccante)

| Check | Esito |
|-------|-------|
| Internet (F-1) | ripristinata (dichiarato Michele) |
| `FRITZ_USERNAME` / `PASSWORD` in `.env` | **ASSENTI** |
| Log collector | ancora `hostlist path fallito: HTTP Error 401` + `mesh SOAP … credentials_invalid` |
| Debito | **DEBT-FRITZ-TR064-CREDENTIALS** resta **APERTO** |

Nessuna campagna, nessuna scrittura, nessuna inferenza compensativa.

---

## W4b.1 — LGS + marcatura

### W4b.1.1 UI

Copy «stesso apparato» → card dichiara l’apparato di appartenenza per nome canonico chassis (`oggiProblems.js`). Chassis 23 ≠ 24: **nessuna fusione**.

### W4b.1.3 `unknown_nonempty` (enumerazione pre-deploy)

Vedi appendice sotto (conteggio misurato in prod). **Nessuno** marcato manual tranne W4b.1.4.

### W4b.1.4 LGS310C (F-2)

- Asset **3**, chassis **24**, valore nome invariato `LGS310C`.
- Solo meta: `manual_overrides` + `field_sources.name=manual` + audit + assertion chassis.
- K1: nessuna scrittura sul valore confrontato oltre la provenienza (valore già LGS310C).
- **LGS328C non toccato** (F-3).

**Soppressione attesa:** NP id **6** (`Switch Linksys` / oui / asset 3) → **DELETE** (set A).

---

## W4b.2 — Rename chassis

- `POST /api/chassis/{id}/adopt-name` e `/rename` — atomici, idempotenti, audit.
- Member adopt → **409** `chassis_subject_required`.
- Alias `iface.alias` excl_key distinta.
- Conflict-review persistito (`reason=conflict_review`) + `GET /api/admin/facts/conflicts` + sezione Oggi.
- W4b.2.9: `unresolvable` → priorità **bassa**; pulsante **adotta** solo se eseguibile (`showAdoptButton`).

---

## W4b.3 — Debiti

| Debito | Azione |
|--------|--------|
| DEBT-RH-BEFORE-REFRESH | **APERTO** (R-H prima di R-A) |
| `_table_bytes` | **FIX** una riga: dbstat fail → 0, non size file DB |
| DEBT-IFACE-IP-CARDINALITY-ROLE | nota su `current()` silent pick |
| DEBT-FRITZ-TR064-CREDENTIALS | confermato APERTO |

---

## W4b.4 — Previsioni (dichiarate PRIMA del deploy)

Baseline pre-deploy misurata: VERSION 0.10.48 · NP **410** · fact_assertions **250** · assets **151** · ip_current **100** · AD **62** (`devices_active` finestra 24h).

| Metrica | Atteso | Delta / note |
|---------|--------|--------------|
| name_proposals | **409** | Δ **−1** · id **6** eliminato (set A post-manual LGS310C) |
| fact_assertions | **251** | Δ **+1** · assertion `asset.name` chassis 24 / LGS310C; bonifica solo `reason` |
| nomi adottati (valore) | **0** | LGS310C cambia **provenienza**, non valore |
| assets | 151 | — |
| ip_current | 100 | — |
| needs_apply | false | — |
| T_backup | 0 | — |
| structural | 0 | — |
| breaker | closed | — |
| unknown_source | 0 | boot quiet |
| AD | **62** | snapshot finestra pre-deploy |

---

## W4b.5 — Test (nodi nominati)

| Nodo | Esito |
|------|-------|
| W4b.5.1–5.10 (`test_w4b_chassis`) | PASS |
| test_facts_resolver | PASS (conflict_review: +1 historical I3) |
| test_m1_observation_store | PASS |
| test_trust_converge | PASS |
| test_mac_ip_policy | PASS |
| T-b / T-e / T-f (nmap dual_dedup, printer/ssdp resolve) | PASS |
| identity (+ evidence, asset, migrate, m3) | PASS |
| test_facts_shadow_w2 + test_m4_m7_shadow | PASS |
| test_w4a_chassis_proposals | PASS |
| web oggiTriage / oggiProblems | PASS |

I6: `rg 'scoreSpecificity|specificity' api/` → **vuoto**.

Non dichiarata «suite verde».

---

## W4b.6 — Assert post-deploy

### Previsioni vs osservati

| Metrica | Previsto | Osservato | Scarto |
|---------|----------|-----------|--------|
| name_proposals | 409 | **409** | 0 · id **6** assente |
| fact_assertions | 251 | **251** | 0 · `asset.name` chassis 24 / LGS310C / manual / current |
| nomi adottati (valore) | 0 | **0** | LGS310C invariato; solo provenienza |
| assets | 151 | 151 | 0 |
| ip_current | 100 | 100 | 0 |
| AD | 62 | **62** | 0 |
| breaker | closed | closed | 0 |
| unknown_source | 0 | 0 | 0 |
| provenance_unreliable marked | (bonifica) | **189** | nmap iface_ip rows |
| observations table | assente | assente | 0 |

### Gate binari

| Gate | boot1 (primo deploy) | boot2 (restart) |
|------|----------------------|-----------------|
| needs_apply | **true** | **false** |
| T_backup | **81.698** | **0** |
| structural | **4** | **0** (apply saltato) |
| breaker | closed | closed |

**boot1 structural=4 — enumerato (non W4b write):** confronto pre-deploy snapshot → current su `meta.operational_state`:

| asset_id | before | after |
|----------|--------|-------|
| 136 | active | stale_unlocated |
| 140 | active | stale_unlocated |
| 145 | active | stale_unlocated |
| 148 | active | stale_unlocated |

Causa: invecchiamento presenza con Fritz TR-064 muto (DEBT-FRITZ). `trust_level` colonne invariate (diff trust_level/presence_state/status = 0). Asset 3: solo aggiunta `manual_overrides=['name']`.

**Regime dopo boot2:** `needs_apply=false · T_backup=0 · structural=0 · breaker=closed`.

### Produzione LGS

| asset | chassis | ruolo | canonico | pending OUI |
|-------|---------|-------|----------|-------------|
| 3 LGS310C | 24 | canonical | LGS310C | **nessuno** |
| 2 LGS328C | 23 | canonical | LGS328C | — |
| 147 | 23 | interface → LGS328C | LGS328C | — |
| 151 | 23 | interface → LGS328C | LGS328C | id 393 «Switch Linksys» (atteso: 328C non manual, F-3) |

I6: `rg 'scoreSpecificity|specificity' api/` → **vuoto**.

### Riga assert

`boot2 0.10.49: needs_apply=false T_backup=0 structural=0 · NP=409 (Δ-1: id 6) · assets=151 ip_cur=100 AD=62 · fact_assertions=251 · breaker=closed · unknown_source=0 · observations=absent · adopted_names_changed=0 · W4b.0.a/b=verdi · asset.name shadow=ON · boot1_structural=4[136,140,145,148] fritz-stale`

---

## Esito / STOP

W4b chiusa su **0.10.49**. Prompt **W5** solo dopo review del diff.

Rollback ammesso: `v0.10.48` · kill switch shadow se solo layer assertion.

---

## Appendice — `unknown_nonempty` pre-deploy

**58** asset (nome valorizzato, provenienza assente). Nessuno marcato manual in questa ondata tranne W4b.1.4 (LGS310C).

| asset_id | name | chassis_id | macs |
|----------|------|------------|------|
| 2 | LGS328C | 23 | D8:EC:5E:CC:1B:FF,… | **NON manual (F-3)** |
| 3 | LGS310C | 24 | D8:EC:5E:C5:7E:C7,… | → marcato manual in W4b.1.4 |
| 1 | FRITZ!Box 5690 Pro | — | 60:B5:8D:6C:6D:53 |
| 4 | GS308EP | — | 54:07:7D:1E:4F:B9 |
| … | (altri 54, elenco completo in misura pre-deploy; non marcati) | | |

Lista completa id: 1,2,3,4,6,7,8,9,10,11,13,14,16,17,18,21,22,23,24,25,26,27,29,33,35,36,39,40,41,43,44,47,50,51,52,53,54,55,56,57,58,59,61,62,63,65,66,67,69,70,71,72,73,74,75,77,78,79.
