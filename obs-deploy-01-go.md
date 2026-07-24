# OBS-DEPLOY-01 — split snapshot+rotazione · STOP post-assert

**Versione:** `0.10.22` · tag `v0.10.22` · merge `27c7c35`  
**Scope:** solo le due parti sicure. **Nessun** prune/TTL su `observations`.

---

## Cosa è entrato in main

| File | Cambio |
|------|--------|
| `scripts/deploy.sh` | Snapshot SQLite **solo se** `api` ∈ servizi; dopo snapshot **rotazione keep-3** su `pre-deploy-*.db` |
| `VERSION` / `web/package.json` / `CHANGELOG` | bump **0.10.22** |

**Scartato** (resta materia OBS-DB-SLIM): `prune_legacy_observations`, `obs_ttl_legacy_days`, test retention legacy.

Commit feature: `052d35b` · merge: `27c7c35`.

---

## Assert live

### a) `/api/health` = versione attesa

```json
{"ok":true,"service":"observatory-api","version":"0.10.22"}
```

(OK su `:18000`. Bootstrap trust ~5–7 min post-recreate; compose ha mostrato `unhealthy` durante start_period — endpoint risponde.)

### b) deploy web **non** crea snapshot

Log:

```
==> snapshot DB saltato (api non nei servizi: web)
==> deploy ok
```

### c) deploy api **crea** snapshot + rotazione keep-3

Log:

```
==> pre-deploy snapshot DB su …/observatory
SNAPSHOT data/backups/pre-deploy-20260724-2357.db size 2673618944
ROTATE_DEL pre-deploy-20260724-0026.db
ROTATE_KEEP 3 deleted 1
==> deploy ok
```

File restanti (esattamente **3**):

- `pre-deploy-20260724-1841.db` (2.4G)
- `pre-deploy-20260724-2303.db` (2.5G)
- `pre-deploy-20260724-2357.db` (2.5G) ← nuovo

### d) `data/backups` dopo

| Metrica | Prima | Dopo |
|---------|-------|------|
| `pre-deploy-*.db` | 3 | **3** (rotazione OK) |
| Totale dir `data/backups` | 13.7G | **14.2G** |
| Somma solo `pre-deploy-*` | ~6.9G | **7.3G** |

Nota: in dir restano anche 3× `observatory-*.db` (~2–2.5G cad.) da `create_backup` bootstrap/api — **non** toccati da keep-3 (solo `pre-deploy-*.db`). Crescita netta dir ≈ +0.5G (nuovo snap − vecchio 2.0G + eventuale altro).

---

## STOP · review → GO

Infra deploy OK; prune legacy **non** deployato.  
Attendo **GO** esplicito solo se serve altro (docs/push già fatti). Per OBS-DB-SLIM i TTL restano fuori da questo release.
