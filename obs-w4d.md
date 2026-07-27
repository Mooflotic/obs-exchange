# W4d — Census Asset.name + una scrittura + verità UX (0.10.52)

**Data:** 2026-07-27 · **Base:** F0 VERDE + 0.10.51 · **Ramo:** `feature/obs-currency`

---

## Assert (UNA RIGA)

`boot1 0.10.52: needs_apply=true T_backup=72.818 structural=1 id=[109] · NP=409/78 · assets=151 ip_cur=99 AD=68 · FA=260 · breaker=closed · unknown_source=0 · observations=absent · display 109/147/151=LGS328C 143=LGS310C`  

`regime: needs_apply=true T_backup>0 structural=[109] — GATE REGIME NON VERDE (oscillazione classify↔lift su 109; vedi sotto). W5 NON avviata.`

### Previsioni → osservati

| Metrica | Previsto | Osservato | Scarto |
|---|---|---|---|
| NP tot/pen | 409/78 | 409/78 | 0 |
| FA | 260 | 260 | 0 |
| assets / ip_cur | 151 / 99 | 151 / 99 | 0 |
| AD | 68 | 68 | 0 |
| breaker / unknown | closed / 0 | closed / 0 | 0 |
| nomi Asset.value | 0 | 0 | 0 |
| boot1 structural | **1 · [109]** (F0.6) | **1 · log structural=1** | 0 |
| boot1 needs_apply / T_backup | true / >0 | true / 72.818s | ok |
| regime needs_apply | false | **true** | **FAIL** — 109 |
| display_name 109/147/151 | LGS328C | LGS328C | ok |
| display_name 143 | LGS310C | LGS310C | ok |

---

## F0 (prerequisito) — sintesi

Report: https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-fritz-restore.md  
DEBT-FRITZ-TR064-CREDENTIALS **CHIUSO**. DEBT-PRESENCE-SOURCE-OUTAGE **APERTO**.

---

## W4d.1 — Censimento lettori `Asset.name`

Tabella esaustiva (sintesi; dettaglio per file nel diff / agent census).  
**Chassis-aware YES** = usa `chassis_canonical_name` / fact_assertions / `composeDevices` chassis / `presentation_name_for_asset`.

### Corretti in W4d (classe a)

| Locus | Scopo | Prima | Dopo |
|---|---|---|---|
| `assets.py` `_serialize` display_name | UI | `asset.name`/`guess` | `presentation_name_for_asset` |
| `switches.py` `asset_name` | Impianto | `asset.name` | presentation |
| `topology.py` node label | grafo | `asset.name` | presentation |
| `scans.py` / `actions.py` display_name | scan picker | `asset.name` | presentation |
| `Dossier.vue` recent | ultimi consultati | raw `name` | `display_name`/canon |
| `triageRules.js` noise* | rumore Oggi | solo `name` | canon/`display_name`/`name` |

### Lista (b) — input W5 (consumatori stato corrente)

`trust.py` classify/bucket/actionable · `inventory.py` protection · `suggest.py` / `ai_naming.py` gating · `name_proposal_chassis.asset_name_authority` · `chassis_rename` enum · `identity.py` ambiguity/infra · `interface_roles` · `fingerprint_facts` match · `topology` AP heuristics · `port_roles._is_ap_asset` · `detectors` · `wifi_associations` resolve AP · `chassis_grouping` MemberView/guards · `composeDevices` singleton/`pickPrimary` · `inventorySort.js` · `AssetDecide.vue` bind name · `_resolve_ap_asset` / `is_current` (DEBT-TOPO-IP-CONTEXTUAL) · API `_serialize` campo grezzo `name=` (colonna) finché W5 non migra la lettura corrente sul resolver.

### Lista (c) — legittimamente per-asset (giustificate)

| Locus | Perché |
|---|---|
| `collectInterfaces` / NIC `i.name` | alias interfaccia, non nome apparato |
| FactSpec registry `asset.name` | schema, non UI |
| log/debug interni | diagnostica per riga DB |
| OS/candidate `.name` non-Asset | non display apparato |

Gate W4d.1.1: tabella pubblicata qui + lista (b) sopra → **input W5**.  
W4d.1.3 verificato in test + prod: membri con `name=""` mostrano canon in `display_name`.

---

## W4d.2 — Doppia scrittura

Percorso umano esplicito: **`apply_observation(..., human_confirm=True)`** (holder=fact_assertion).  
Rimosso `safe_shadow_asset_name` da `adopt_name_on_chassis` e `mark_lgs310c_manual`.  
Test `test_w4d_2_2`: +1 FactAssertion al primo rename, 0 al secondo.

---

## W4d.3 — UX truth

- `obs-ux2.md`: matrice → «non verificato a runtime» + checklist 10 voci.
- **LGS API reali (post-deploy):**

| id | chassis_id | role | canon | name | display_name | pending |
|---|---|---|---|---|---|---|
| 2 | 23 | canonical | LGS328C | LGS328C | LGS328C | 0 |
| 3 | 24 | canonical | LGS310C | LGS310C | LGS310C | 0 |
| 109 | 23 | interface | LGS328C | "" | **LGS328C** | 0 |
| 143 | 24 | interface | LGS310C | "" | **LGS310C** | 0 |
| 147 | 23 | interface | LGS328C | "" | **LGS328C** | 0 |
| 151 | 23 | interface | LGS328C | "" | **LGS328C** | 0 |

LGS328C resta `unknown_nonempty` (F-2): nessuna marcatura manual.

---

## W4d.4 — Favicon opzione B

Token invariati (`--bg-0` `#0f1319`, `--accent` `#6bc5db`, `--ok` `#4fb477`, `--text-1` `#e8ebf0`).  
Opzione B: **anello + hub** (nessuna lettera). **Non sostituita** l’attuale (L+O).  
Pubblicati: `obs-ux2-favicon-optB-16.png` · `optB-32.png` · `optB.svg`. Scelta a Michele.

---

## Gate regime — perché NON verde

F0 lift ha portato **109** a `ops=active` / `trust=known` con evidenza `fritz_active`.  
`classify_asset(109)` → **`fritz_historical`** (presence `fritz_only`, no portal).  
Quindi `reconcile_trust_history` dry_run: `needs_apply=true`, `structural=[109]` in perpetuo, anche a collector fermo.  
Boot1 ha applicato `structural=1` (log), ma lo stato osservato resta `active`/`known` (lift / piano incoerenti).  
**Non è correggibile in W4d** senza toccare il trust layer (DEBT-PRESENCE-SOURCE-OUTAGE).  

→ **GATE W4d FALLITO sul regime** → **W5 non parte**.

---

## Test (nodi nominati)

`test_w4b_chassis` (+ W4d.1.3 / W4d.2.2) · facts_resolver · facts_shadow_w2 · m1_observation_store · trust_converge · mac_ip_policy · w4a_chassis_proposals · migrate_identity · m3_identity · oggiTriage/Problems · observatoryUx · portPresentation · topologyLayout → pass sottoinsieme.  
I6: `rg 'scoreSpecificity|specificity' api/` → **VUOTO**.  
Non dichiarato «suite verde».

---

## Debiti

- DEBT-FRITZ-TR064-CREDENTIALS: **CHIUSO** (F0)
- DEBT-PRESENCE-SOURCE-OUTAGE: **APERTO** (+ oscillazione 109 classify↔lift)
- Lista (b) W5: sopra — **bloccata** finché regime gate non è risolto

---

## Publish

- `obs-w4d.md` · `obs-w4d.diff.txt`
- Favicon B + `obs-ux2.md` aggiornato
- F0 già pubblicato
