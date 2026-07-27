# W4c — Correzioni post-review (0.10.50)

**Esito:** W4c.1/2/3 chiuse · gate binari verdi · **STOP FASE 1 → FASE 2 (F2)**.

**Rollback:** tag `v0.10.49` · kill switch `FACT_SHADOW_WRITERS_ENABLED=false` se solo shadow.

**Rinumerazione:** W4c → **0.10.50** · F2 ondate 0.10.51+ · W5 dopo F2.

Diff: [`docs/obs-w4c.diff.txt`](obs-w4c.diff.txt) — integrale.  
**Esclusione:** il file diff non include sé stesso.

---

## W4c.1 — Un solo nome canonico (VERDE)

### Scelta detentore (W4c.1.1)

**(b) assertion `asset.name` con `subject=chassis`** — già nel registro e nello store  
(`api/app/facts/registry.py` FactSpec `asset.name`; scrittura via `apply_observation` in  
`api/app/services/chassis_rename.py` `adopt_name_on_chassis`).  
Nessun campo `Chassis.canonical_name` aggiunto: una sola copia.

### Comportamento

- `adopt_name_on_chassis` **non** assegna `member.name` né `manual_overrides` ai sibling.
- Il membro che già portava il nome scelto resta invariato; gli altri restano interfacce.
- Presentazione: `chassis_canonical_presentation` legge il fact chassis;  
  `triageRules.js` salta `chassis_role === "interface"` **senza** richiedere nome vuoto.

### Test

- `test_w4c_1_6_rename_four_members_one_canonical` — **PASS** (sostituisce il vuoto di copertura di `test_w4b_5_5` single-member).
- `test_w4b_5_3` aggiornato: dichiara invariante nuovo (membri non rinominati; fact = canonico).

---

## W4c.2 — Bonifica cutoff (VERDE)

- Cutoff dichiarato: **`2026-07-27T11:00:00Z`** (`PROVENANCE_BONIFY_CUTOFF` in `api/app/facts/shadow.py`).
- Fuori dal boot (`bootstrap.py`).
- Script una-tantum: `scripts/unmark_post_cutoff_provenance.py` (no bump VERSION dedicato).

### Misura pre-deploy

| Voce | n |
|------|---|
| `provenance_unreliable` totali | 189 |
| pre-cutoff | 189 |
| **post-cutoff (erronei)** | **0** (ids: nessuno) |

Nessuna rimozione necessaria. Test `test_w4c_2_4` PASS.

---

## W4c.3 — mark_lgs310c fuori boot (VERDE)

Rimossa chiamata da bootstrap. Helper resta in `chassis_rename.py` (one-shot).  
Asset 3: `manual_overrides=['name']` + `field_sources.name.source=manual` · valore `LGS310C` invariato.  
Reversibilità: rimuovere `name` da overrides + field_sources.

---

## W4c.4 — Sorgenti rifiutate (una lettura)

`GET` shadow-stats (in-process api, una volta):

```
unknown_source=0
counters={}
breaker_open=false
```

`safe_shadow_iface_ip` riceve `elected.source` da `IpAddress` (fritz/nmap/mgmt/…).  
**ssdp / mdns / portal non producono IP di interfaccia** per questo writer (usati per nomi/fingerprint).  
Non aggiunti a `asset.iface_ip.sources`. Nessuna traduzione.

---

## W4c.5 — DEBT-PRESENCE-SOURCE-OUTAGE

Aperto in `KNOWN_DEBT.md`. Trust **non** corretto. UI in F2.

---

## W4c.6 — Previsioni (PRIMA del deploy)

Baseline misurata: NP **409** · FA **253** (251→253 da shadow quiet post-W4b; non collasso) · assets **151** · ip_current **100** · AD **62** · trust dry_run `needs_apply=false` · post-cutoff unreliable **0**.

| Metrica | Atteso |
|---------|--------|
| name_proposals | **409** (Δ 0) |
| fact_assertions | **253** (Δ 0) |
| provenance_unreliable rimossi | **0** |
| nomi valore modificato | **0** |
| assets / ip_current | 151 / 100 |
| needs_apply / T_backup / structural | false / 0 / 0 |
| breaker | closed |
| unknown_source | 0 |
| AD | **62** (snapshot finestra) |
| boot1 structural | **0 atteso** (asset 136/140/145/148 già riconciliati; dry_run pre-deploy clean) |

---

## W4c.7 — Test nominati

W4c.1.6/1.7/2.4/3.2 + w4b_chassis + facts_resolver + shadow_w2 + m1 + trust + mac_ip + T-b/e/f + identity + w4a + web oggi: **PASS** (sottoinsieme; non «suite verde»).  
I6: `rg 'scoreSpecificity|specificity' api/` → **vuoto**.

---

## W4c.8 — Assert post-deploy

`boot1 0.10.50: needs_apply=false T_backup=0 structural=0 · NP=409 (Δ0) · assets=151 ip_cur=100 AD=62 · fact_assertions=253 (Δ0) · breaker=closed · unknown_source=0 · observations=absent · provenance_cleared=0 · adopted_names_changed=0 · W4c.1/2/3=verdi · asset3=manual LGS310C`

Previsioni tutte confermate. GATE W4c **VERDE** → FASE 2.
