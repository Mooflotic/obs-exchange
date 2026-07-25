<!-- BLOCK-ID: OBS-UX -->

# OBS-UX — Report chiusura cantiere

**Branch:** `feature/obs-ux` · **VERSION tree:** 0.10.40 (G fix CSS) · **Data:** 2026-07-25  
**Specifica vincolante:** [`obs-ux-casidiuso.md`](obs-ux-casidiuso.md) · **Misura iniziale:** [`obs-ux-misura.md`](obs-ux-misura.md) · **Misura finale:** [`obs-ux-h-misura-finale.md`](obs-ux-h-misura-finale.md)

---

## Stato deploy

| Assert | Esito |
|--------|-------|
| W1 health | PASS · `0.10.40` |
| W2 regime | PASS · T_total=**8.864**s · needs_apply=false · T_backup=0 |
| Conti | PASS · assets 151 · name_proposals 412 · AD 82 · ip_current 100 · observations assente |
| main = tag = prod | PASS dopo merge — tag `v0.10.40` = bump G |
| Prune 0a.1 | **Non ancora** (~2026-07-27) |

---

## Prune raw 0a.1

**Non ancora avvenuto** (misura 2026-07-25). Atteso ~2026-07-27: ~173 530 righe, freelist 0.30–0.37 GiB. Predizione falsificabile con `store.before/after` + log `[retention]`.

---

## Gesto manuale N=41

**Non eseguito** in questo cantiere. `noiseProposalIds` con `all_proposals=true` → **N = 41** (D13=21, D12=15, D3=5). Anteprima motivata in Oggi (A.5); archiviazione massa resta decisione operatore.

---

## Debiti aperti (post OBS-UX)

| Debito | Nota |
|--------|------|
| CU-02 delta giornaliero | Semantica «cosa è cambiato» — proposta P-01 |
| Rename chassis | CU-07 parziale; adopt 409 |
| IP `.3.20` ownership | Verdetto RO: [`obs-ux-ip-308-verifica.md`](obs-ux-ip-308-verifica.md) |
| DEBT-AGGREGATE-NO-RETENTION | Backend |
| DEBT-FINGERBANK-027 | Rimandato ≥2026-08-15 |
| DEBT-AUTOVACUUM-NOT-SET | Post-prune |
| DEBT-BACKUP-ALL-OR-NOTHING | Operatività |
| DEBT-PRIVACY-MAC-CHURN | Grouping |
| Topologia palette verde | Residuo visivo G-4 |
| A11y toggle/focus trap | Misura 1.5 residuo |

---

## Misura finale (sintesi)

Vedi tabella completa in [`obs-ux-h-misura-finale.md`](obs-ux-h-misura-finale.md).

| Esito | Casi |
|-------|------|
| Sì | CU-05, CU-06, CU-08, CU-09 (+ CU-10 struttura) |
| Parziale | CU-01, CU-03, CU-04, CU-07 |
| No | CU-02 |

**Metodo:** analisi code-path; **no** remisura live click in fase H.

---

## Ondate A–F (outcome)

| Onda | VERSION | Outcome |
|------|---------|---------|
| **A** | 0.10.34 | Oggi hub — card 6 campi, move FDB in coda, anteprima rumore, redirect `/suggestions` |
| **B** | 0.10.35 | Tre ruoli switch (Impianto/Topologia/Monitor), error load, deps [`obs-ux-deps-b.md`](obs-ux-deps-b.md) |
| **C** | 0.10.36 | `Branch308Card` ramo 308 — fatti/gap/inferenze |
| **D** | 0.10.37 | Sintesi identità Dossier; dump JSON rimosso |
| **E** | 0.10.38 | `AiInferenceLabel`; copy IP `.3.20` corretto |
| **F** | 0.10.39 | `ViewStateBanner`; UX_COPY; focus-visible ricerche |

Report dettagliati: [`obs-ux-b.md`](obs-ux-b.md) … [`obs-ux-e.md`](obs-ux-e.md) (+ F in CHANGELOG 0.10.39).

---

## IP GS308EP `.3.20` — verdetto

**Non inventariale; non SPAN.** Binding Fritz storico sul MAC asset 4, stale; SPAN = LGS328C p22 → asset 6 (`.3.24`). UI: «da confermare». RO: [`obs-ux-ip-308-verifica.md`](obs-ux-ip-308-verifica.md). **PASS** intento E/I3.

---

## Revisione visiva (fase G)

Ispezione statica — **no screenshot**. Fix 0.10.40: token blu-ardesia in `matrix.css`, fix CSS invalido mobile. Dettaglio: [`obs-ux-g-visiva.md`](obs-ux-g-visiva.md).

---

## Prossimo cantiere

1. Verifica **prune** ~2026-07-27.
2. Gesto manuale **Archivia rumore N=41** (Michele).
3. Idee non implementate: [`obs-ux-proposte.md`](obs-ux-proposte.md) — priorità suggerita: CU-02 (P-01), rename chassis (P-02), Topologia token (P-10).
4. **STOP** redesign oltre proposte documentate finché non aperto nuovo cantiere.

---

## Tag / merge

- Merge `feature/obs-ux` → `main`: **TBD** parent
- Tag produzione atteso: **`v0.10.40`** (post G)
- Evidenza: `GET /api/health` → **TBD**
