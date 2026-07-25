# OBS-DB-SLIM 3b-iii — PASSO 0 baseline riconciliata (GATE)

**Data misura:** 2026-07-25  
**Host:** Cassiopea `0.10.25` (health verificato)  
**Strumentazione:** timer nidificati in `entrypoint.sh` + `bootstrap.py` + `trust.py`  
(`T_prefetch_obs` = sola lettura Observation portal; codice di misura syncato su api, VERSION invariata)

---

## Nidificazione dichiarata (struttura reale)

```
T_total (host: container StartedAt → primo /api/health 200)
  ├── T_import          DISGIUNTO (pre-bootstrap; ~0 s)
  └── T_bootstrap_wall  NIDIFICATO in T_total
        └── T_trust     NIDIFICATO in T_bootstrap (step 8)
              ├── T_dry_run     NIDIFICATO in T_trust
              │     ├── T_prefetch_obs   NIDIFICATO in dry_run  ← Observation
              │     ├── T_prefetch_fdb   NIDIFICATO in dry_run
              │     └── T_plan_loop      NIDIFICATO in dry_run
              ├── T_backup      NIDIFICATO in T_trust, DOPO dry_run
              └── T_apply       NIDIFICATO in T_trust, DOPO backup
        T_residuo_trust = T_trust − (T_dry_run + T_backup + T_apply)
```

**T_backup è NIDIFICATO dentro T_trust** (non disgiunto).

---

## Previsione da falsificare (dichiarata PRIMA, testo piano)

> ipotesi = il backup è NIDIFICATO dentro T_trust, e  
> T_trust ≈ T_backup + T_prefetch + T_residuo con T_residuo ≈ 1.8 s.

### Verdetto ipotesi

| Parte | Esito |
|-------|--------|
| Backup NIDIFICATO in T_trust | **CONFERMATA** (log espliciti + somma componenti) |
| T_trust ≈ T_backup + T_prefetch_obs + residuo | **CONFERMATA come identità aritmetica** se residuo = tutto ciò che non è backup né prefetch_obs |
| T_residuo ≈ 1.8 s nel senso del report precedente | **FALSIFICATA come etichetta** |

**Struttura reale del “buco” 1.8 s del report precedente:**  
quel report scriveva `trust 234.9 = prefetch 35.1 + backup 198` (somma 233.1) e ometteva **T_apply**.  
Con la strumentazione: `T_residuo_trust` (wrap) ≈ **0.0 s**; i ~1.5–1.8 s sono **T_apply**, componente separata nidificata in T_trust, non “residuo misterioso”.

Forma corretta:

`T_trust = T_dry_run + T_backup + T_apply + T_residuo_trust`  
con `T_dry_run ≈ T_prefetch_obs + T_prefetch_fdb + T_plan_loop` e `T_residuo_trust ≈ 0`.

---

## Misure (solo numeri osservati)

### RUN1 — path strutturale (needs_backup=True, needs_apply=True)

Primo avvio dopo rebuild strumentazione.

| Timer | Valore (s) | Note |
|-------|------------|------|
| T_total | **291** | entrypoint epoch 1784967475 → health epoch 1784967766 |
| T_import | **0** | misurato |
| T_bootstrap_wall | **286** | misurato |
| T_trust | **276.3** | misurato |
| T_dry_run | **11.1** | nested in T_trust |
| T_prefetch_obs | **10.9** | nested in dry_run |
| T_prefetch_fdb | **0.0** | nested in dry_run |
| T_plan_loop | **0.1** | nested in dry_run |
| T_dry_residuo | **0.0** | calcolato: 11.1−(10.9+0.0+0.1) |
| T_backup | **263.7** | nested in T_trust |
| T_apply | **1.5** | nested in T_trust |
| T_residuo_trust | **0.0** | calcolato: 276.3−(11.1+263.7+1.5) |

Somma check livello trust: 11.1+263.7+1.5+0.0 = **276.3** (Δ 0.0 s) → **PASS ±2 s**.

Health: `{"ok":true,"version":"0.10.25"}`.

### RUN2 — path steady (needs_apply=False → backup skip)

Cold `compose stop` + `start`, nessuna modifica funzionale.

| Timer | Valore (s) |
|-------|------------|
| T_total | **60** |
| T_bootstrap_wall | **55** |
| T_trust | **49.0** |
| T_dry_run | **48.9** |
| T_prefetch_obs | **48.3** |
| T_prefetch_fdb | **0.4** |
| T_plan_loop | **0.3** |
| T_dry_residuo | **0.0** |
| T_backup | **0.0** (skip) |
| T_apply | **0.0** (skip) |
| T_residuo_trust | **0.0** |

Somma: 48.9+0+0+0 = 49.0 → **PASS ±2 s**.

### RUN3 — stesso path di RUN2 (terza misura per rumore)

Cold stop/start, nessuna modifica funzionale.

| Timer | Valore (s) |
|-------|------------|
| T_total | **29** |
| T_bootstrap_wall | **23** |
| T_trust | **17.1** |
| T_dry_run | **17.0** |
| T_prefetch_obs | **16.7** |
| T_prefetch_fdb | **0.1** |
| T_plan_loop | **0.3** |
| T_dry_residuo | **0.0** |
| T_backup | **0.0** (skip) |
| T_apply | **0.0** (skip) |
| T_residuo_trust | **0.0** |

Somma: 17.0+0+0+0 = 17.1 → **PASS ±2 s**.

---

## Coerenza run-to-run (GATE 0c)

### Path confrontabile: RUN2 vs RUN3 (entrambi backup=0)

| Metrica | RUN2 | RUN3 | Δ run-to-run |
|---------|------|------|--------------|
| T_prefetch_obs | 48.3 | 16.7 | **31.6 s** |
| T_trust | 49.0 | 17.1 | **31.9 s** |
| T_total | 60 | 29 | **31 s** |

Δ atteso post-fix (rimozione prefetch) citato dal piano: **≈ −35 s**.  
Dispersione misurata sullo stesso path: **≈ 32 s** → **non** “nettamente inferiore” al segnale.

### RUN1 non confrontabile con RUN2/3

RUN1 ha eseguito backup strutturale (**263.7 s**). Dopo l’apply, RUN2/3 hanno `needs_apply=False` → T_backup=0.  
Media RUN1+RUN2 sarebbe un **miscuglio di due path diversi** → non usata come metro.

---

## GATE 0

| Criterio | Esito |
|----------|--------|
| (a) somma componenti = totale livello ±2 s, nidificazione dichiarata | **PASS** (tutte e 3 le run) |
| (b) T_residuo calcolato e spiegato | **PASS** (sempre 0.0 s wrap; il vecchio “1.8” era T_apply) |
| (c) due run coerenti; rumore ≪ 35 s | **FAIL** (Δ prefetch 31.6 s su path steady) |

### GATE 0 = **FAIL**

**STOP.** Nessuna modifica funzionale (passi 1–7 non avviati).  
Nessun metro ufficiale “media di due run” per gli assert del passo 9: la baseline riconciliata **non è certificabile** finché il rumore prefetch non è sotto controllo o l’assert −35 s non viene riformulato (es. assert su `T_prefetch_obs=0` + budget su mediana/IQR di N run).

---

## Nota operativa

- Live resta `0.10.25` con **solo** strumentazione timer (nessun bump VERSION).  
- Per riprodurre: greppare `docker logs` per `[timing]`.  
- Non iniziare 4b. Non DROP tabella `observations`.
