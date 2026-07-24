# OBS-DB-SLIM · Passo 3a — GO 0.10.24

**2026-07-25** · merge `ebe01a0` · tag `v0.10.24` · deploy `api`+`web`

---

## Assert

### a) Health

```json
{"ok":true,"service":"observatory-api","version":"0.10.24"}
```

### b) Dopo ciclo WiFi (deploy_ts = API healthy UTC `2026-07-24 23:28:26`, poi **+150s**)

| Check | Risultato |
|-------|-----------|
| `COUNT(*) … kind IN (fritz_wlan_assoc,fritz_mesh) AND seen_at >= deploy_ts` | **0** |
| Asset con `meta.link` aggiornato **dopo** deploy_ts | **36** (es. observed_at `2026-07-24T23:28:56Z`) |
| `ASSETS_WITH_WIFI_LINK` | 43 |
| Totale Observation WLAN (storico TTL) | **216 471** (non toccate a mano) |

Scan avvenuto + zero Observation scritte → **entrambi OK**.

### c) Topologia

| | |
|--|--|
| `WIFI_EDGES` | **36** (`kind=wifi`, `source_name=radio AP`) |
| `wifi_association_notice` | (none) |

---

## Note

- Le ~216k righe WLAN restano; scenderanno col TTL 7g (passo 2).
- File invariato fino al VACUUM (passo 4).
- Dual-write host / R2 invariati (passo 3b).
