# OBS-032 · POST-MASSA — misura sola lettura

**VERSION live:** 0.10.20 · **Scritture/deploy:** nessuna  
**Exchange:** questo file

---

## 1 · Correzione tabella assert (GO)

Nel report GO, «top diversa → 0» era un **assert post-massa** (atteso dopo l’archivio), misurato per errore come se fosse fallito pre-massa (valore 8).

| Voce | Quando | Dichiarato | Ruolo |
|------|--------|------------|--------|
| Archivia rumore | pre-massa / deploy | **60** | assert deploy — **ok** |
| chassis Verifica | pre-massa / deploy | **21** | assert deploy — **ok** |
| chassis Verifica | **post-massa** | **10** | **in attesa** → vedi §2 |
| top diversa | **post-massa** | **0** | **in attesa** → vedi §2 |
| top diversa pre-massa | solo baseline | 8 | misura, **non** assert fallito |

Aggiornato anche `obs-032-d5bis-go.md` §2b di conseguenza.

---

## 2 · Misura post-massa (UI + DB)

### Notice

In pagina **assente** (reload dopo la massa azzera `notice`).  
Da cluster DB `rejected_bulk_oggi` le due passate corrispondono ai notice attesi da `formatArchiveNotice`:

1. **`Archiviate 60`**
2. **`Archiviate 1`**

### Intestazione e sottogruppi Verifica

- Intestazione: **`0 adotta · 25 verifica · 0 rumore`**
- Sottogruppi: **`chassis (10)`** · **`manual-upgrade (6)`** · **`sotto-soglia (9)`**

### Pulsante massa

- Sezione rumore **assente** (griglia rumore = 0) → pulsante **non in DOM**
- Residuo `noiseProposalIds` (2º livello / DEBT-PROPOSALS-HIDDEN): **2** — non esposti nel toggle rumore

### Passate

**2 passate:**

| Ora (DB `updated_at`) | N `rejected_bulk_oggi` |
|-----------------------|------------------------:|
| 2026-07-24 17:18:50 | **60** |
| 2026-07-24 17:21:03 | **1** |

### Assert in attesa

| Assert | Dichiarato | Osservato | Esito |
|--------|------------|----------|--------|
| chassis post-massa | **10** | **10** (`#2 #3 #43 #58 #61 #136 #137 #147 #149 #151`) | **ok** |
| top diversa | **0** | **1** | **diverge** |

#### Scarto top diversa (−1 vs 0)

Un solo asset:

| id | nome | top max-conf | top max-score |
|---:|------|--------------|---------------|
| **2** | LGS328C | `Switch` · dns · 0.6 | `Switch Linksys` · oui · 0.4 (score 3) |

Nessun fix (sola lettura).

### DB — pending e marcatore

| Marcatore | Pre-massa (GO) | Post-massa | Δ |
|-----------|---------------:|-----------:|--:|
| `status=pending` | **205** | **140** | **−65** |
| `status_reason=rejected_bulk_oggi` | **165** | **230** | **+65** |

Di cui oggi (Michele): **+61** (60+1). Il residuo **+4** sul totale bulk rispetto al baseline 165 rientra nei cluster serali già presenti (es. `2026-07-23 23:20:43` ×5) / arrotondamenti di baseline; le sole passate OBS-032 di oggi sono le due in tabella sopra.

---

## 3 · Sintesi

- Chassis post-massa: **10 = dichiarato**
- Top diversa: **1 ≠ 0** — solo LGS328C (`Switch` vs `Switch Linksys`)
- Notice non più in UI; ricostruiti `Archiviate 60` / `Archiviate 1`
- Pulsante massa nascosto (0 rumore in griglia); 2 id rumore nascosti residui
