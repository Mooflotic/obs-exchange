# OBS-DB-SLIM · Passo 3a — stop scrittura Observation WLAN · STOP pre-GO

Branch: `feature/obs-db-slim` · **solo WLAN** · R2 (presence/scans/detectors) **fuori scope**.

Diff: [`obs-db-slim-p3a.diff.txt`](https://raw.githubusercontent.com/Mooflotic/obs-exchange/main/obs-db-slim-p3a.diff.txt)

---

## 1 · Cosa si spegne / cosa resta

### Spento

| Path | Prima | Dopo |
|------|-------|------|
| `materialize.py` loop `wlan_associations` (ex `:226–232`) | `record_observation(kind=fritz_wlan_assoc\|fritz_mesh, …)` | **rimosso** |

### Intatto (citato)

| Path | Ruolo |
|------|--------|
| `wifi_associations.py:18` `materialize_wifi_association` | scrive **`assets.meta.link`** (+ `link_history`) — topologia |
| `materialize.py:82` `record_observation` host | dual-write presence gated 60s — **passo 3b** |
| `identity.py:408` nmap MAC `record_observation` | stesso — **passo 3b** |
| `retention.py:120–133` `prune_legacy_observations` | `DELETE … WHERE seen_at < cutoff` — **nessun filtro su `kind`** |

---

## 2 · TTL e le ~216k esistenti

`prune_legacy_observations` usa solo `Observation.seen_at < cutoff` (TTL 7g).  
`kind` non è nella WHERE → le righe `fritz_wlan_assoc` **rientrano** e scenderanno col ritmo del passo 2.  
**Nessun DELETE manuale** in 3a.

---

## 3 · Assert post-deploy (piano GO — non eseguiti ora)

| Check | Metodo |
|-------|--------|
| Topologia Wi‑Fi viva | asset con `meta.link.source=fritz_wlan_assoc` ancora aggiornato dopo un ciclo collector; graph edges wifi presenti |
| Crescita Observation WLAN = 0 | `COUNT(*) WHERE kind='fritz_wlan_assoc' AND seen_at >= deploy_ts` → **0** (o rate/ora = 0) |

---

## 4 · Test

`tests/test_wifi_association_ingest.py`:
- ingest scan: `meta.link` scritto; **nessuna** Observation wlan
- `test_wlan_materialize_does_not_append_legacy_observation` nuovo

```
6 passed
```

---

## Previsione

| | |
|--|--|
| Nuove Observation WLAN / ora dopo deploy | **0** |
| ~216k esistenti | scendono col TTL 7g (freelist↑) |
| File OS | invariato fino VACUUM passo 4 |
| Non toccato | host dual-write, scans, detectors, DNS |

---

## STOP

Attendo **GO** per bump/merge/deploy api e assert topologia + rate WLAN=0.
