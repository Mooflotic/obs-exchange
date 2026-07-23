# OBS-032 + D5-bis · FASE B — report implementazione

**Branch:** `feature/obs-032-d5bis` (da `main`)  
**VERSION:** **0.10.20** (bump solo in questo cantiere)  
**Deploy:** **STOP** — review, poi GO per merge/deploy  
**Diff:** `obs-exchange/main/obs-032-d5bis-faseb.diff.txt`

---

## 0 · Domande aperte (sola lettura live)

### Q0 — Proposta DHCP 0.75 su `#14` Citofono

| Campo | Valore |
|-------|--------|
| Proposal id | **408** |
| `source` | `dhcp` |
| `value` | `C3X-00-03-50-96-82-2c-45123` |
| `confidence` | **0.75** |
| `status` | **`rejected`** |
| `status_reason` | **`rejected_from_oggi`** |
| `updated_at` | `2026-07-23 22:58:52` (≈ 00:58 IT) |

Dopo lo screenshot «1 adotta» (~00:52), l’operatore ha archiviato **singolarmente** la DHCP da Oggi. Restano pending dns/fritz (stesso hostname, conf 0.5/0.6) → top dns 0.6 in **verifica**.  
`rejected_from_oggi` 4→6: i due nuovi sono **#408** (Citofono dhcp) e **#127** (LUMIN ssdp, 22:54).

**A2 corretta:** la trappola MAC-incapsulato **ha raggiunto ADOTTA CONSIGLIATI** (documentata dallo screenshot + reject). Non è solo rischio «verifica/adotta manuale».

### Q1 — Pending 373→205 = −168 vs 165+2 = 167

Conti reject: `rejected_bulk_oggi` **165** + delta `rejected_from_oggi` **+2** = **167**.

L’unità mancante (−168) è l’**adozione** (non reject) di proposal **`id=416`** `Sky TV` su asset **`#135`**, `status=archived`, `updated_at=2026-07-23 22:51:50` — subito prima della massa bulk (22:53). Fuori dal conteggio reject → −1 pending in più.

---

## 1 · OBS-032 — MAC incapsulato → rank 1

- `scoreSpecificity`: check rank 1 **prima** dei rank 5 — pattern `(?:[0-9a-f]{2}[-:]){5}[0-9a-f]{2}` **oppure** `[0-9a-f]{12}` in qualunque posizione.
- Fixture: C3X / GAGGENAU / garmin → **1**; ROMO / roborock / Loewe / AmazonAQM / LGS328C / GS308EP → **≠1**.
- Dump 030 re-pin: **invariato**  
  `rumore/adotta/chassis/verifica/mass_eligible`  
  **48 / 9 / 2 / 10 / 46 → 48 / 9 / 2 / 10 / 46**

---

## 2 · D5-bis — chassis in massa + conferma adotta

- `noiseProposalIds` / `noiseProposalsMissingIdCount`: **rimosso** lo skip chassis. Restano esclusi `ignorato` e proposte senza id.
- `Oggi.vue` `adoptRow`: se `chassis_member`, `confirm` dichiarativo (nome su asset singolo; sibling divergenti) — non blocca.
- UI «+N chassis esclusi» rimossa (non più vera).
- **`mass_eligible`:** il `&& !chassisMember` era **già ridondante** (branch chassis non setta mai `massEligible=true`). Semplificato a `mass_eligible: massEligible`. Il campo resta per il conteggio rumore di griglia; **la massa usa solo `noiseProposalIds`** — non escludeva i chassis via `mass_eligible`.
- Test: chassis rumore → id in `noiseProposalIds`; source-test conferma in `Oggi.vue`.

---

## 3 · Documentazione

- `KNOWN_DEBT`: **DEBT-PROPOSALS-HIDDEN-FROM-API**, **DEBT-ADOPT-NO-CHASSIS-GUARD**
- `CHANGELOG` + `VERSION` / `package.json` → **0.10.20**

---

## 4 · Attese post-deploy (assert — non eseguire ora)

Baseline live **0.10.19** post-purga (misura FASE A ~01:05):

| Voce | Baseline | Atteso post **0.10.20** |
|------|----------|-------------------------|
| Pulsante `Archivia rumore (N)` | **5** | **≈ 62** (5 + ~57 rumore chassis) |
| Sottogruppo `chassis(21)` | **21** | **≈ 0–2** dopo 1–2 passate massa (solo non-rumore / upgrade residui) |
| S1 «top diversa» M3 | **8** | **0** (o ≪8) — MAC→rank 1 riallinea top conf vs specificità sui hostname MAC |
| ADOTTA con hostname MAC conf≥0.75 | possibile (Q0) | **0** automatici (rank 1 → rumore/≤, non D8) |

---

## 5 · Suite

| Suite | Esito |
|-------|--------|
| `node --test src/*.test.js` | **107 pass / 0 fail** |
| `pytest --ignore=tests/test_m6_m8_detectors_flow.py` | **479 passed**, **9 failed** (noti, invariati) |

9 fail noti: `test_backend_filo_f2_f28` (2), `test_m2_discovery`, `test_nmap_provider`, `test_printer_alembic`, `test_printer_provider`, `test_scanning_workflow`, `test_ssdp_alembic`, `test_ssdp_provider`.

---

## STOP

Review → **GO** per merge no-ff + deploy Cassiopea + assert §4.
