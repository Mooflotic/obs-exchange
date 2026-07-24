# OBS-032 + D5-bis · GO — micro-fix + previsione + deploy

**Branch:** `feature/obs-032-d5bis`  
**VERSION:** **0.10.20** (invariata)  
**Micro-fix commit:** a sé (12-hex `\b` + `DEBT-MAC-REGEX-DIGIT-RUN`)  
**Diff micro-fix:** `obs-exchange/main/obs-032-d5bis-microfix.diff.txt`

---

## 1 · Micro-fix

- `scoreSpecificity`: `/\b[0-9a-f]{12}\b/i` (word boundary). Target C3X/GAGGENAU/garmin restano rank 1; `pref68A40E40A69Asuff` **≠1**.
- `KNOWN_DEBT`: **DEBT-MAC-REGEX-DIGIT-RUN**
- Dump 030 pin: **invariato** 48/9/2/10/46
- Suite: node **107 pass**; pytest ignore-m6 **479 pass / 9 fail noti**

---

## 2 · Previsione (sola lettura, PRIMA del deploy)

Metodo: dump live `_serialize` + `list_chassis_payload`, poi `triageRules` **0.10.20** (con `\b`) in locale.

### 2a — Chassis dopo la massa → **10**

Membri chassis con ≥1 pending **non-rumore** esposta in API (sopravvivono all’archivio massa):

| asset | nome attuale | proposta che resta (top conf tra non-rumore) | fonte | conf |
|------:|--------------|-----------------------------------------------|-------|-----:|
| 2 | LGS328C | Switch Linksys | oui | 0.4 |
| 3 | LGS310C | Switch Linksys | oui | 0.85 |
| 43 | Sky | MR-Device/1.0.0 (Sky, EM150, ) | ssdp | 0.55 |
| 58 | Sky | GW-Device/1.0.0 (Sky, ES240, ) | ssdp | 0.55 |
| 61 | Sky | MR-Device/1.0.0 (Sky, EM150, ) | ssdp | 0.55 |
| 136 | *(anonimo)* | Sky | oui | 0.85 |
| 137 | *(anonimo)* | Sky | oui | 0.85 |
| 147 | *(anonimo)* | Switch Linksys | oui | 0.85 |
| 149 | *(anonimo)* | Sky | oui | 0.85 |
| 151 | *(anonimo)* | Switch Linksys | oui | 0.85 |

Pre-massa il sottogruppo UI resta **chassis(21)** (15 top-rumore + 6 già non-rumore).

### 2b — Tabella assert (corretta)

| Voce | Vecchia stima | **Dichiarato** |
|------|---------------|----------------|
| Archivia rumore (N) | ≈62 | **60** |
| chassis Verifica **pre-massa** (assert deploy) | 21 | **21** |
| chassis Verifica **post-massa** (Michele) | ≈0–2 | **10** |
| top diversa (max-conf vs max-score) | →0 | **8** (invariato; casi non-MAC) |

### 2c — `#135` Sky TV

| Campo | Valore |
|-------|--------|
| Nome attuale | **`Sky TV`** |
| Proposta adottata | id **416** `ai` / `Sky TV` / conf 0.62 → `archived` (22:51:50), reason OUI/hostname |
| Pending residua | id 363 `oui` / `Sky` / 0.85 |
| Asset con nome esatto `Sky` | **5** (#43, #58, #61, #82, #88) — **#135 non c’è** |
| Collisione «Sky» salita? | **No** per questo adopt (nome scritto = `Sky TV`, non `Sky`) |

---

## 3 · Deploy + osservato

| Voce | Dichiarato | Osservato | Δ |
|------|------------|-----------|---|
| API `/api/health` version | 0.10.20 | **0.10.20** | ok |
| UI sidebar | 0.10.20 | **v0.10.20 · 24/07** | ok |
| Archivia rumore (N) | **60** | **60** (UI + `noiseProposalIds`) | ok |
| chassis Verifica | **21** | **21** | ok |
| Confirm adotta chassis → Annulla | dialogo sì | testo chassis/sibling; `confirm` → false (nessuna adozione) | ok |

Massa: **non eseguita** (Michele). Post-massa atteso: chassis **10** (elenco §2a).

### Merge / tag

- Merge no-ff → `main` (`db99ac9`)
- Tag **`v0.10.20`** pushato
- `./scripts/deploy.sh api web` → ok (bootstrap trust lento ~minuti, poi healthy)

### Suite micro-fix

- `node --test src/*.test.js` → **107 pass**
- `pytest --ignore=tests/test_m6_m8_detectors_flow.py` → **479 pass / 9 fail noti**
- Dump 030 pin: **invariato** 48/9/2/10/46
