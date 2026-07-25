# OBS-3b-i — migrazione scans → presence_sources portal (C2=d)

**Branch:** `feature/obs-db-slim` · **Commit code:** `62733c0` · **Docs:** `26b0f72`  
**Data:** 2026-07-25 · **STOP pre-deploy** — review → GO

Scelta: **(d)** — reader scans su `presence_sources` portal + IP current.  
NON (c). Sticky rank / `IpAddress.source` invariato. Dual-write host **resta acceso**.

---

## Parte 1 · Docs

Commit `26b0f72` — `docs: report sessione OBS-DB-SLIM`

File versionati:
- `obs-chiusura-fasea.md`
- `obs-3b-recon.md`
- `obs-3b-i-gap.md`
- `obs-db-slim-p2-go.md`
- `obs-db-slim-p3-fasea.md`
- `obs-db-slim-p3a-go.md`
- `obs-deploy-01-go.md`

**Fuori dal repo:** nessuno lasciato untracked di sessione.  
`git status` post-commit (dopo anche il commit code): branch pulito su `feature/obs-db-slim`.

---

## Parte 2 · Gate di copertura (sola lettura live)

### 2a · Insieme A (legacy Observation branch — 60)

| asset_id | IP |
|---------:|----|
| 1 | 192.168.1.1 |
| 2 | 192.168.1.2 |
| 3 | 192.168.1.7 |
| 4 | 192.168.1.8 |
| 9 | 192.168.2.107 |
| 11 | 192.168.2.108 |
| 12 | 192.168.1.250 |
| 13 | 192.168.2.109 |
| 14 | 192.168.2.68 |
| 16 | 192.168.2.149 |
| 17 | 192.168.3.5 |
| 18 | 192.168.2.190 |
| 19 | 192.168.1.20 |
| 20 | 192.168.2.125 |
| 21 | 192.168.1.10 |
| 22 | 192.168.1.11 |
| 23 | 192.168.1.12 |
| 24 | 192.168.1.13 |
| 25 | 192.168.1.35 |
| 26 | 192.168.1.45 |
| 27 | 192.168.1.46 |
| 28 | 192.168.1.44 |
| 29 | 192.168.1.50 |
| 30 | 192.168.1.117 |
| 31 | 192.168.2.50 |
| 32 | 192.168.2.62 |
| 33 | 192.168.2.70 |
| 34 | 192.168.2.74 |
| 35 | 192.168.2.76 |
| 36 | 192.168.2.80 |
| 37 | 192.168.2.81 |
| 38 | 192.168.2.82 |
| 39 | 192.168.2.93 |
| 40 | 192.168.2.96 |
| 41 | 192.168.2.98 |
| 42 | 192.168.2.99 |
| 44 | 192.168.2.105 |
| 45 | 192.168.2.106 |
| 46 | 192.168.2.110 |
| 47 | 192.168.2.115 |
| 48 | 192.168.2.117 |
| 49 | 192.168.2.124 |
| 50 | 192.168.2.126 |
| 51 | 192.168.2.138 |
| 52 | 192.168.2.148 |
| 53 | 192.168.2.167 |
| 54 | 192.168.2.173 |
| 55 | 192.168.2.176 |
| 56 | 192.168.2.186 |
| 57 | 192.168.2.189 |
| 59 | 192.168.2.203 |
| 60 | 192.168.2.206 |
| 62 | 192.168.3.32 |
| 63 | 192.168.3.38 |
| 64 | 192.168.3.45 |
| 65 | 192.168.3.46 |
| 66 | 192.168.3.47 |
| 67 | 192.168.3.49 |
| 68 | 192.168.2.94 |
| 69 | 192.168.2.122 |

### 2b · Insieme B (presence_sources portal fresco + IP current)

**84** asset con almeno un kind portal fresco in `presence_sources`; **65** coppie (asset, IP current).

Oltre alle 60 di A, B include anche (B\A = 5):
- 5 · 192.168.1.3
- 6 · 192.168.3.24
- 70 · 192.168.2.193
- 85 · 192.168.2.85
- 98 · 192.168.2.88

### 2c–2d · GATE

| Metrica | Valore |
|---------|-------:|
| \|A\| | 60 |
| \|B\| pairs | 65 |
| **A \ B** | **0** |
| GATE | **PASS** → Parte 3 eseguita |

---

## Parte 3 · Implementazione

### 3a · Reader

`_fresh_portal_sources_by_ip` in `scans.py`:
- **Rimosso** `select(Observation)` (ex `:82-98`)
- **Aggiunto** lettura `asset.presence_sources` (kind portal + ts &lt;24h) applicata a ogni IP `is_current`
- Branch IpAddress portal source **invariato** (sticky rank non toccato)
- `active_discovery` / DNS hysteresis: **diff 0** su `inventory.py` / `identity.py`

### 3b · Dual-write host

Non toccato (passo 3b-iii futuro). Solo LETTURA scans.

### 3c · Test (22 passed)

- `test_scan_target_cross_row_fritz_current_plus_nmap_evidence` — sticky fritz + `presence_sources.nmap`
- `test_scan_target_accepts_presence_sources_portal_with_sticky_fritz`
- `test_scan_target_legacy_observation_alone_no_longer_qualifies` — Observation sola non basta più
- `test_scan_target_fritz_or_import_alone_fails` — fritz_hostlist non-portal non apre il gate
- scanning workflow invariato (nmap su IpAddress ancora ok)

### 3d · Previsione pre-deploy (sim live DB)

| | Asset con ≥1 candidato | IP candidati |
|--|----------------------:|-------------:|
| **PRIMA** (Observation + IpAddress portal) | **60** | 61 |
| **DOPO** (presence_sources + IpAddress portal) | **65** | 66 |
| Delta | **+5** | +5 |

Atteso ≥ confermato: recupera i 5 coperti-solo-portal che lo sticky rank nascondeva sul branch IpAddress.

---

## STOP

Nessun deploy. Review → GO deploy su Cassiopea.

---

## Diff (`62733c0`)

```diff
diff --git a/observatory/api/app/services/scans.py b/observatory/api/app/services/scans.py
index bacd448..fcf84c4 100644
--- a/observatory/api/app/services/scans.py
+++ b/observatory/api/app/services/scans.py
@@ -8,7 +8,7 @@ from sqlalchemy import select
 from sqlalchemy.orm import Session
 
 from app.config import Settings
-from app.models import Asset, Observation, ScanRun
+from app.models import Asset, ScanRun
 from app.services.identity import classify_oui
 from app.services.macutil import normalize_mac, oui_prefix
 from app.services.scan_profiles import (
@@ -17,7 +17,7 @@ from app.services.scan_profiles import (
     validate_discovery_network,
     validate_scan_target,
 )
-from app.services.trust import PORTAL_EVIDENCE, is_portal_evidence
+from app.services.trust import is_portal_evidence
 
 ACTIVE_STATUSES = {"queued", "running"}
 TERMINAL_STATUSES = {"done", "failed", "cancelled"}
@@ -42,6 +42,35 @@ SOURCE_CONFIDENCE = {
 }
 
 
+def _parse_presence_ts(raw: object) -> datetime | None:
+    if raw is None:
+        return None
+    if isinstance(raw, datetime):
+        return raw.replace(tzinfo=None) if raw.tzinfo else raw
+    text = str(raw).strip()
+    if not text:
+        return None
+    try:
+        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
+    except ValueError:
+        return None
+    return parsed.replace(tzinfo=None) if parsed.tzinfo else parsed
+
+
+def _fresh_portal_kinds_from_presence(asset: Asset, *, now: datetime) -> list[str]:
+    """Portal kinds with presence_sources timestamp inside TARGET_MAX_AGE."""
+    since = now - TARGET_MAX_AGE
+    kinds: list[str] = []
+    for kind, ts in dict(asset.presence_sources or {}).items():
+        if not is_portal_evidence(kind):
+            continue
+        seen = _parse_presence_ts(ts)
+        if seen is None or seen < since:
+            continue
+        kinds.append(str(kind or "").lower())
+    return kinds
+
+
 def _fresh_portal_sources_by_ip(
     asset: Asset,
     settings: Settings,
@@ -49,7 +78,17 @@ def _fresh_portal_sources_by_ip(
     now: datetime,
     db: Session | None = None,
 ) -> dict[str, list[str]]:
-    """Map IP → portal evidence sources (<24h), from IpAddress rows and/or Observations."""
+    """Map IP → portal evidence sources (<24h).
+
+    Sources (OBS-DB-SLIM 3b-i):
+    - IpAddress rows whose ``source`` is portal evidence (rare when sticky rank
+      keeps ``fritz``/``mgmt`` on the current binding);
+    - asset ``presence_sources`` portal kinds (written by ``observe_portal``),
+      applied to every current LAN IP on the asset.
+
+    Does not read Observation legacy. ``db`` kept for call-site compatibility.
+    """
+    _ = db
     found: dict[str, list[str]] = {}
     for iface in asset.interfaces:
         for address in iface.addresses:
@@ -63,38 +102,20 @@ def _fresh_portal_sources_by_ip(
                 continue
             found.setdefault(safe_ip, []).append(str(address.source or "").lower())
 
-    if db is None:
+    portal_kinds = _fresh_portal_kinds_from_presence(asset, now=now)
+    if not portal_kinds:
         return found
 
-    current_ips: set[str] = set()
-    macs = {normalize_mac(iface.mac) for iface in asset.interfaces if iface.mac}
     for iface in asset.interfaces:
         for address in iface.addresses:
             if not address.is_current:
                 continue
             try:
-                current_ips.add(validate_scan_target(address.ip, settings.network_cidr))
+                safe_ip = validate_scan_target(address.ip, settings.network_cidr)
             except ValueError:
                 continue
-    if not current_ips:
-        return found
-
-    since = now - TARGET_MAX_AGE
-    observations = db.scalars(
-        select(Observation).where(
-            Observation.seen_at >= since,
-            Observation.ip.in_(sorted(current_ips)),
-            Observation.kind.in_(sorted(PORTAL_EVIDENCE)),
-        )
-    ).all()
-    for obs in observations:
-        if obs.mac and macs and normalize_mac(obs.mac) not in macs:
-            continue
-        try:
-            safe_ip = validate_scan_target(obs.ip, settings.network_cidr)
-        except ValueError:
-            continue
-        found.setdefault(safe_ip, []).append(str(obs.kind or "").lower())
+            for kind in portal_kinds:
+                found.setdefault(safe_ip, []).append(kind)
     return found
 
 
@@ -109,8 +130,8 @@ def scan_target_candidates(
 
     An IP qualifies when:
     - there is an ``is_current`` binding on the asset, and
-    - the same asset+IP has a <24h IpAddress/Observation row whose source is in
-      ``PORTAL_EVIDENCE`` (fritz/import* alone do not qualify).
+    - the same asset has fresh portal evidence via IpAddress.source and/or
+      ``presence_sources`` (fritz/import* alone do not qualify).
     """
     now = now or datetime.utcnow()
     if not asset.portal_last_seen:
diff --git a/observatory/tests/test_backend_filo_f2_f28.py b/observatory/tests/test_backend_filo_f2_f28.py
index 5bc8ebf..86e4618 100644
--- a/observatory/tests/test_backend_filo_f2_f28.py
+++ b/observatory/tests/test_backend_filo_f2_f28.py
@@ -92,11 +92,14 @@ def test_purge_placeholder_name_proposals(tmp_path):
 
 
 def test_scan_target_cross_row_fritz_current_plus_nmap_evidence(tmp_path):
+    """Sticky fritz on IpAddress + portal presence_sources (replaces dual IpAddress row)."""
     db = _db(tmp_path)
+    now = datetime.utcnow()
     asset = Asset(
         uid="xrow",
-        portal_first_seen=datetime.utcnow(),
-        portal_last_seen=datetime.utcnow(),
+        portal_first_seen=now,
+        portal_last_seen=now,
+        presence_sources={"nmap": now.isoformat() + "Z"},
     )
     db.add(asset)
     db.flush()
@@ -109,16 +112,7 @@ def test_scan_target_cross_row_fritz_current_plus_nmap_evidence(tmp_path):
             ip="192.168.1.20",
             is_current=True,
             source="fritz",
-            last_seen=datetime.utcnow(),
-        )
-    )
-    db.add(
-        IpAddress(
-            interface_id=iface.id,
-            ip="192.168.1.20",
-            is_current=False,
-            source="nmap",
-            last_seen=datetime.utcnow(),
+            last_seen=now,
         )
     )
     db.flush()
@@ -135,6 +129,7 @@ def test_scan_target_fritz_or_import_alone_fails(tmp_path):
         uid="fritz-only",
         portal_first_seen=datetime.utcnow(),
         portal_last_seen=datetime.utcnow(),
+        presence_sources={"fritz_hostlist": datetime.utcnow().isoformat() + "Z"},
     )
     db.add(asset)
     db.flush()
@@ -150,28 +145,48 @@ def test_scan_target_fritz_or_import_alone_fails(tmp_path):
             last_seen=datetime.utcnow(),
         )
     )
+    db.flush()
+    settings = Settings(network_cidr="192.168.0.0/22")
+    cands, reason = scan_target_candidates(asset, settings, db=db)
+    assert cands == []
+    assert "Nessun IP attuale verificato" in reason
+
+    # import alone also fails (non-portal source, empty presence portal)
+    asset2 = Asset(
+        uid="import-only",
+        portal_first_seen=datetime.utcnow(),
+        portal_last_seen=datetime.utcnow(),
+        presence_sources={},
+    )
+    db.add(asset2)
+    db.flush()
+    iface2 = Interface(asset_id=asset2.id, mac="AA:BB:CC:DD:EE:14")
+    db.add(iface2)
+    db.flush()
     db.add(
         IpAddress(
-            interface_id=iface.id,
-            ip="192.168.1.21",
+            interface_id=iface2.id,
+            ip="192.168.1.24",
             is_current=True,
             source="import",
             last_seen=datetime.utcnow(),
         )
     )
     db.flush()
-    settings = Settings(network_cidr="192.168.0.0/22")
-    cands, reason = scan_target_candidates(asset, settings, db=db)
-    assert cands == []
-    assert "Nessun IP attuale verificato" in reason
+    cands2, reason2 = scan_target_candidates(asset2, settings, db=db)
+    assert cands2 == []
+    assert "Nessun IP attuale verificato" in reason2
 
 
-def test_scan_target_accepts_fresh_observation_evidence(tmp_path):
+def test_scan_target_accepts_presence_sources_portal_with_sticky_fritz(tmp_path):
+    """OBS-DB-SLIM 3b-i: fritz sticky source + presence_sources.nmap → eligible."""
     db = _db(tmp_path)
+    now = datetime.utcnow()
     asset = Asset(
-        uid="obs",
-        portal_first_seen=datetime.utcnow(),
-        portal_last_seen=datetime.utcnow(),
+        uid="sticky-fritz",
+        portal_first_seen=now,
+        portal_last_seen=now,
+        presence_sources={"nmap": now.isoformat() + "Z", "fritz_hostlist": now.isoformat() + "Z"},
     )
     db.add(asset)
     db.flush()
@@ -183,22 +198,55 @@ def test_scan_target_accepts_fresh_observation_evidence(tmp_path):
             interface_id=iface.id,
             ip="192.168.1.22",
             is_current=True,
+            source="fritz",
+            last_seen=now,
+        )
+    )
+    db.flush()
+    settings = Settings(network_cidr="192.168.0.0/22")
+    cands, reason = scan_target_candidates(asset, settings, db=db)
+    assert reason == ""
+    assert [c["ip"] for c in cands] == ["192.168.1.22"]
+    assert "nmap" in cands[0]["sources"]
+
+
+def test_scan_target_legacy_observation_alone_no_longer_qualifies(tmp_path):
+    """Observation legacy without presence_sources must not gate scans (3b-i)."""
+    db = _db(tmp_path)
+    now = datetime.utcnow()
+    asset = Asset(
+        uid="obs-only",
+        portal_first_seen=now,
+        portal_last_seen=now,
+        presence_sources={},
+    )
+    db.add(asset)
+    db.flush()
+    iface = Interface(asset_id=asset.id, mac="AA:BB:CC:DD:EE:13")
+    db.add(iface)
+    db.flush()
+    db.add(
+        IpAddress(
+            interface_id=iface.id,
+            ip="192.168.1.23",
+            is_current=True,
             source="import",
-            last_seen=datetime.utcnow(),
+            last_seen=now,
         )
     )
     db.add(
         Observation(
             kind="nmap",
-            mac="AA:BB:CC:DD:EE:12",
-            ip="192.168.1.22",
-            seen_at=datetime.utcnow(),
+            mac="AA:BB:CC:DD:EE:13",
+            ip="192.168.1.23",
+            seen_at=now,
         )
     )
     db.flush()
     settings = Settings(network_cidr="192.168.0.0/22")
-    cands, _ = scan_target_candidates(asset, settings, db=db)
-    assert [c["ip"] for c in cands] == ["192.168.1.22"]
+    cands, reason = scan_target_candidates(asset, settings, db=db)
+    assert cands == []
+    assert "Nessun IP attuale verificato" in reason
 
 
 def test_speed_and_band_labels():
diff --git a/observatory/tests/test_scanning_workflow.py b/observatory/tests/test_scanning_workflow.py
index 5bf0137..ecb6eb5 100644
--- a/observatory/tests/test_scanning_workflow.py
+++ b/observatory/tests/test_scanning_workflow.py
@@ -134,10 +134,13 @@ def test_duplicate_identical_current_ip_is_one_eligible_candidate(tmp_path):
     db = _db(tmp_path)
     asset = _observed_asset(db)
     asset.name = "ArcherBE3600"
-    iface = asset.interfaces[0]
+    # Second interface claiming the same LAN IP — still one scan candidate.
+    second = Interface(asset_id=asset.id, mac="AA:BB:CC:DD:EE:99")
+    db.add(second)
+    db.flush()
     db.add(
         IpAddress(
-            interface_id=iface.id,
+            interface_id=second.id,
             ip="192.168.1.8",
             is_current=True,
             source="dns",

```
