<!-- BLOCK-ID: OBS-CHASSIS-W0-IDENTITA -->

# OBS-CHASSIS — W0 Identità (prerequisito W4)

**Live 2026-07-25 · 0.10.40 · RO**

---

## 0.8 Modello chassis

| Voce | Misura |
|------|--------|
| Tabella | `chassis` + `assets.chassis_id` (presentation only) |
| Popolo | `reconcile_chassis_grouping()` — bootstrap + ingest |
| Righe chassis | **15** |
| Asset con chassis_id | **35** |
| Gruppi ≥2 membri | **15** |
| Gruppi ≥2 con ≥1 nome manuale (`manual_overrides`⊇name) | **5** |
| Gruppi ≥2 con >1 nome manuale distinto | **0** |

### Gruppi ≥2 (asset_id → nome)

| ch | label | membri |
|----|-------|--------|
| 1 | Cassiopea — NIC 1 | 5 «Cassiopea — NIC 1», 6 «Cassiopea — NIC 2» |
| 3 | Allsky 3 | 30, 51 |
| 6 | Sky | 61, 137 |
| 9 | (none) | 110, 142 |
| 14 | SkyBooster2 BIBLIO | 10, 11, 138 |
| 15 | Kraken | 28, 140 |
| 16–22 | Echo/Tapo/ROCK/Sky… | (vedi diagnosi) |
| **23** | **LGS328C** | **2 LGS328C, 109, 147, 151** |
| **24** | **LGS310C** | **3 LGS310C, 143** |

---

## Caso di riferimento utente (tre card)

| MAC | asset | nome | chassis_id | NP pending |
|-----|------:|------|------------|------------|
| D8:EC:5E:CC:1C:05 | 147 | (vuoto) | **23** | id **387** oui «Switch Linksys» 0.85 |
| D8:EC:5E:CC:1C:08 | 151 | (vuoto) | **23** | id **393** oui «Switch Linksys» 0.85 |
| D8:EC:5E:C5:7E:C7 | 3 | LGS310C | **24** | id **6** oui «Switch Linksys» 0.85 |

Terzo pending sullo stesso valore chassis 23: asset **109** NP id **266**.

**AMBIGUA (STOP-5):** DB **non** raggruppa i tre MAC come un solo apparato LGS310C. Due NIC sono sibling di **LGS328C** (C4+R2). Non consolidare in W4 senza conferma Michele.

---

## 0.9 NameProposal — candidati soppressione W4

### A) Dup stesso (chassis, value) pending

| gruppo | proposal_ids |
|--------|--------------|
| ch23 \| switch linksys | **266, 387, 393** |

Cardinalità proposte in gruppo dup: **3** · quota su 412: **3/412 = 0.73%**

### B) Pending su chassis con membro manuale

**N = 0** (con definizione stretta `manual_overrides` contiene `name`).

### C) Pending su asset già named (qualsiasi origine nome)

**N = 18** ids:  
`6, 46, 53, 68, 73, 98, 149, 150, 212, 224, 236, 242, 286, 353, 355, 372, 395, 400`

Di cui caso switch: **id 6** su asset 3 LGS310C (nome presente, overrides name **assente**).

### D) Genesi (codice)

Soggetto creazione: **sempre `asset_id`**, mai chassis (`create_name_proposal` in `identity.py`).  
AI naming aggrega chassis ma scrive sul primary asset.

---

## 0.10 Guardia 409

`POST .../adopt-name` (`assets.py`): se `chassis_id` e `COUNT(siblings)≥2` → **409** «rename chassis non implementato».

Esito sul caso: **409 corretto sul soggetto sbagliato** (blocca membro; manca endpoint chassis). Non è un 409 «difettoso» come predicato, è un’azione assente.

---

## 0.11 K1 — reconcile vs `asset.name`

Campi confrontati/riscritti da trust/inventory reconcile:

- `trust_level`, `presence_state`, `portal_*`, `meta.operational_state`, `inventory_hidden*`
- NameProposal deboli fritz → archive

**`asset.name` NON è fra questi campi.**

→ Scrivere canonical name **solo** in `fact_assertion` (W1+) **non** produce da solo structural mismatch / backup 1.85 GiB.  
→ Scrivere `Asset.name` in questo cantiere resta **vietato** per policy esplicita del prompt (anche se K1 lo permetterebbe tecnicamente).

---

## 0.12 Alias interfaccia

**Assente** come naming layer. Esiste solo `Interface.label` (es. `"management"`). Da registrare come `iface.alias` in W1 senza inventare UI ora.

---

## 0.13 Contraddizione semantica

| Voce | N |
|------|--:|
| Asset con nome manuale (lista overrides) | **29** |
| Con `os_guess` non vuoto (claim confrontabile OS) | **3** |
| Contraddizioni family tipizzate (Android↔Windows…) | **0** |
| Non misurabili (no evidenza tipizzata OS) | **26** → available=false |

OUI vs nome modello: **non misurato** senza euristica inventata (K3).

---

## I6

`grep scoreSpecificity\|specificity api/` → **vuoto** (specificità solo `web/src/triageRules.js`).
