# OBS-PORTALE — report chiusura

**Branch:** `feature/obs-portale` · **Ultimo bump:** `v0.10.33` = `71322ec`  
**Live:** health `0.10.33` · regime T_total ≈ 8.8–9.0 s · `needs_apply=false` · `T_backup=0`  
**Data:** 2026-07-25

---

## Prossimo cantiere (in testa)

1. **Verifica prune raw 0a.1** — atteso ~**2026-07-27**. Predizione falsificabile: ~173 530 righe cancellate, freelist 0.30–0.37 GiB. Confrontare `store.before/after` + log `[retention]` con previsto. (Oggi 2026-07-25: non ancora avvenuto.)
2. **Gesto manuale Michele — «Archivia rumore»** con **N = 41** (rimisurato post-0.10.33 con `all_proposals=true`; il ≈39/2 storici sono obsoleti). **Non eseguito** in questo cantiere.
3. **Debiti ancora aperti** (dopo PORTALE): `DEBT-AGGREGATE-NO-RETENTION`, `DEBT-FINGERBANK-027` (rimandato ≥2026-08-15), `DEBT-AUTOVACUUM-NOT-SET` (criterio residuo post-prune), `DEBT-BACKUP-ALL-OR-NOTHING`, `DEBT-PRIVACY-MAC-CHURN`, `DEBT-PYTEST-COLLECTION-PY39`, `DEBT-MAC-REGEX-DIGIT-RUN` (verificata 0 hit — regex invariata), rename chassis (residuo adopt).
4. **STOP qui** per PORTALE: revisione grafica e hot/cold **uno alla volta**, dopo review.

---

## FASE 0a / 0b

Vedi `docs/obs-portale-triage.md`. Sintesi: prune non ancora; AUTOVACUUM soglia residuo >512 MiB×7g post-48h; aggregate senza retention (debito); Δ file **1 024 393 216**; E8 +1 asset 43 Sky + scan anonimi 85/98.

Ordine ondate **confermato dai numeri** (j=0 → verify-only).

---

## Ondata 1 — 0.10.31 (`eed5580` / tag `v0.10.31`)

| Assert | Esito |
|--------|-------|
| W1 health 0.10.31 | PASS |
| W2 regime ~9s, needs_apply=false, T_backup=0 | PASS (9.019 s) |
| W3 quattro assenze dichiarate | PASS |
| W4 assets 151, NP 412 | PASS |

Chiusi: MANUAL-CONF-BAR, VERSION-SILENT-FALLBACK, HABITS-DIR-UNAVAILABLE, CHASSIS-PARTIAL-SILENT.  
Report: `obs-portale-w1.md` (curl 200).

---

## Ondata 2 — 0.10.32 (`f534536` / tag `v0.10.32`)

| Assert | Esito |
|--------|-------|
| W1/W2 | PASS (regime 8.897 s) |
| W5 ssdp pending 10→4 | PASS (4 Fritz strip + 6 banner archive) |
| W6 nomi adottati invariati | PASS (0 cambi) |

Gate equivalenza: 17 NP changed (enumerate in `obs-portale-w2.md`); OUI floor ≥0.7; OS equiv solo nmap; Sky `name_ambiguity`; digit-run 0 hit → regex invariata.  
Report: `obs-portale-w2.md` (curl 200).

---

## Ondata 3 — 0.10.33 (`71322ec` / tag `v0.10.33`)

| Assert | Esito |
|--------|-------|
| W1/W2 | PASS (regime 8.833 s) |
| W7 coda Oggi + N massa | PASS — pending mostrate **118**; **Archivia rumore N = 41** |
| W8 no scoreSpecificity in Python | PASS (`grep` api/ vuoto) |

Move FDB uplink: **19→0** pending (`target_not_access_port`). Adopt chassis → 409. Anti-ricreazione rejected.

---

## Ondata 4 — decisioni

### 4.1 Fingerbank 027
**Rimandare** (non integrare ora). Branch `feature/obs-fingerbank-027` tip `d20313e` (~1.1k LOC: client + cache + DHCP opt55). Costo alto (secret, API, Zeek wire). Cantiere dedicato **non prima del 2026-08-15**. Debito: `DEBT-FINGERBANK-027`.

### 4.2 DNS hysteresis
**Rimuovere / già rimossa.** Il gate Observation dns è stato tolto in 3b-iii; il codice `endpoint.missing` non consulta più DNS. Dichiarato morto: `DEBT-DNS-HYST-LEGACY-NOOP` **CHIUSA**. Nuova isteresi solo con sorgente calda misurabile.

### 4.3 KNOWN_DEBT
Chiuse in PORTALE: presentazione (f/g/h/i), OS-PREFIX, PROPOSALS-HIDDEN, ADOPT-CHASSIS, NO-RECREATION, DNS-HYST.  
Verificata: MAC-DIGIT-RUN (0 hit).  
Aperte/rimandate: AGGREGATE-NO-RETENTION, FINGERBANK-027, AUTOVACUUM (criterio nuovo), ecc.

---

## Verifica prune 0a.1

**Non ancora** (misura 2026-07-25; atteso ~2026-07-27). Resto come punto 1 del prossimo cantiere.

---

## Merge / tag / produzione

- Merge `feature/obs-portale` → `main`
- Tag di produzione = ultimo bump VERSION: **`v0.10.33`** = `71322ec`
- Evidenza: `GET /api/health` → `0.10.33` · curl web/health 200
