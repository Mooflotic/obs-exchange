<!-- BLOCK-ID: OBS-UX-PROPOSTE -->

# OBS-UX — Proposte future (solo idee)

**Data:** 2026-07-25 · **Scope:** idee per cantiere **successivo** — **nessun codice** qui.  
**Confine:** tutto ciò implementato in ondate A–F (0.10.34–0.10.39) + fix G (0.10.40) è **fuori** da questo documento.

Riferimento implementato: [`obs-ux.md`](obs-ux.md) · specifica vincolante: [`obs-ux-casidiuso.md`](obs-ux-casidiuso.md).

---

## Semantica e dati

| ID | Proposta | Perché | Dipende da |
|----|----------|--------|------------|
| P-01 | **Delta «cosa è cambiato oggi»** — timeline scoped 24h/48h o digest in Oggi | CU-02 non raggiunto: Oggi = coda, non changelog | Backend eventi aggregati; non solo UI |
| P-02 | **Rename chassis** end-to-end | CU-07 parziale: adopt singola NIC → 409 | API + UI Dossier/chassis |
| P-03 | **Undo** adopt/reject/archivia massa (soft, 30s) | Misura 1.6: tutte azioni irreversibili senza undo | Modello audit o tombstone proposte |
| P-04 | **Ownership IP `.3.20`** — workflow conferma/respinta binding Fritz | I3 operativo aperto | Verifica RO Michele + eventuale adopt manuale |
| P-05 | **Ruoli IP secondari** in UI (primario/vpn/mgmt/servizi) | DEBT-TOPO-IP-CONTEXTUAL backend fatto; UI secondari = FASE C mai chiusa | Design card IP multipli |

---

## Presentazione e grafica

| ID | Proposta | Perché |
|----|----------|--------|
| P-10 | **Allineamento canvas Topologia** ai token blu-ardesia | Residuo G-4: ~15 hex verde in `Topology.vue` |
| P-11 | **Empty state Findings** con `ViewStateBanner` | G-5: tabella vuota senza messaggio |
| P-12 | **Patch panel UI** (schema DB esiste, 0 UI) | CU-04: patch_code solo in Plant edit |
| P-13 | **Focus trap completo** dialog Inventario + `role=switch` toggle | Debito a11y 1.5 |
| P-14 | **Sidebar strumenti** — Dashboard, Incidents, Ai, Runbook discoverable | Route orfane fuori nav principale |

---

## Operatività rete

| ID | Proposta | Perché |
|----|----------|--------|
| P-20 | **SNMP/PoE/contatori GS308EP** se mai disponibili | I7: oggi dichiarato «non rilevato» — non inventare |
| P-21 | **Fingerbank 027** integrazione DHCP opt55 | DEBT-FINGERBANK-027 rimandato ≥2026-08-15 |
| P-22 | **Move FDB** — ripopolare pending quando regole uplink cambiano | 19 rejected uplink; 0 pending live |
| P-23 | **Confronto A↔B** multi-NIC / omonimi side-by-side | CU-07: oggi solo spiegazione testuale |

---

## AI e findings

| ID | Proposta | Perché |
|----|----------|--------|
| P-30 | **Findings in Oggi** quando `scoring.calibrated=true` | Oggi = coda unica; Findings resta vista separata |
| P-31 | **Citazioni cliccabili** da AiConsole verso Dossier/Plant | Riduce click post-risposta AI |
| P-32 | **Feedback «AI sbagliata»** su proposta (non adopt) | Migliora calibrazione senza scrivere DB autorevole |

---

## Infrastruttura / debito collegato

| ID | Proposta | Nota |
|----|----------|------|
| P-40 | Verifica **prune raw 0a.1** post ~2026-07-27 | Non UX; blocca metriche DB |
| P-41 | **AUTovacuum** post-prune se freelist >512 MiB×7g | DEBT-AUTOVACUUM-NOT-SET |
| P-42 | Drop route `/suggestions` dopo periodo di redirect | Oggi redirect attivo; tenere finché bookmark esterni |

---

## Esplicitamente fuori scope prossimo UX

- Redesign completo Dashboard come home operativa (Oggi resta hub triage).
- Telemetria inventata su porte 308.
- Merge identity / chassis grouping (regole R1/R2 intoccabili).
- Esecuzione automatica «Archivia rumore N=41» senza conferma umana.
