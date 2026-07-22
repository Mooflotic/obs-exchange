<!-- BLOCK-ID: OBS-BEHAV-W1A-P2-DIFF-007 -->

# OBS-BEHAV-W1A-P2-DIFF-007 — 2A backend `/habits`

Scope: solo API + service + test + DEBT-MIRROR-SOURCES. **Niente UI (2B).**

- `GET /api/assets/{id}/habits?days=7`
- Gate SQL set-based (binding + tie→escludi)
- Coverage 3 stati; mirror sources hardcoded `p1/p21/p24` → sink `p22` (`DEBT-MIRROR-SOURCES`)
- Ore: `hours[].hour` in **UTC** + `timezone: "Europe/Rome"` + `hours_basis: "utc"`
- Mix-aware: `SUM(bytes_out)` → NULL se tutte NULL
- Test: `9 passed` (`tests/test_habits.py`)

```diff
diff --git a/observatory/api/app/services/habits.py b/observatory/api/app/services/habits.py
new file mode 100644
--- /dev/null
+++ b/observatory/api/app/services/habits.py
+++ b/observatory/api/app/services/habits.py
@@ -0,0 +1,377 @@
+"""Asset habits (Wave 1a): flow rollup gated by IP binding history."""
+
+from __future__ import annotations
+
+import re
+from datetime import datetime, timedelta, timezone
+from typing import Any, Optional
+
+from sqlalchemy import select, text
+from sqlalchemy.orm import Session, joinedload
+
+from app.models import Asset, SwitchPort
+from app.services.macutil import is_synthetic_ip_mac, normalize_mac
+from app.services.topology import path_to_asset
+
+HABITS_TIMEZONE = "Europe/Rome"
+DEFAULT_DAYS = 7
+MAX_DAYS = 30
+TOP_DESTINATIONS = 8
+TOP_PORTS = 5
+THIN_SAMPLE_MAX = 4  # samples in window → thin_sample (honest “campione sottile”)
+
+# MIRROR_SOURCE_PORTS: config nota (runbook), TODO codificare in DB
+# — DEBT-MIRROR-SOURCES
+MIRROR_SWITCH_CODE = "328c"
+MIRROR_SOURCE_PORTS = frozenset({1, 21, 24})
+MIRROR_SINK_PORT = 22  # Cassiopea eth1 — sink, not a traffic source
+
+_UPLINK_EDGE_RE = re.compile(
+    r"^uplink:([^:]+):(\d+)-([^:]+):(\d+)$",
+    re.IGNORECASE,
+)
+
+
+def _utc_now() -> datetime:
+    return datetime.now(timezone.utc).replace(tzinfo=None)
+
+
+def _asset_link(asset: Asset) -> dict[str, Any]:
+    meta = asset.meta or {}
+    link = meta.get("link")
+    return dict(link) if isinstance(link, dict) else {}
+
+
+def classify_flow_coverage(db: Session, asset: Asset) -> dict[str, str]:
+    """3-state SPAN coverage from topology (not from flow absence)."""
+    link = _asset_link(asset)
+    if str(link.get("media") or "").lower() == "wifi":
+        return {
+            "state": "parziale",
+            "label": "Traffico: copertura parziale",
+            "reason": "WiFi↔WiFi sullo stesso AP non passa dallo SPAN.",
+        }
+
+    if _asset_on_mirror_source_port(db, asset):
+        return {
+            "state": "completo",
+            "label": "Traffico: copertura completa",
+            "reason": (
+                "Path wired su ramo uplink mirrorato (SPAN). "
+                "Assenza di flow = silenzio osservato."
+            ),
+        }
+
+    path = path_to_asset(db, asset.id)
+    if _path_crosses_mirror_sources(path):
+        return {
+            "state": "completo",
+            "label": "Traffico: copertura completa",
+            "reason": (
+                "Path wired su ramo uplink mirrorato (SPAN). "
+                "Assenza di flow = silenzio osservato."
+            ),
+        }
+
+    if path.get("mapped"):
+        return {
+            "state": "parziale",
+            "label": "Traffico: copertura parziale",
+            "reason": (
+                "Porta/ramo non tra le sorgenti mirror "
+                f"(LGS328C p{', p'.join(str(p) for p in sorted(MIRROR_SOURCE_PORTS))}). "
+                "East-west o uplink non mirrorato possono restare invisibili."
+            ),
+        }
+
+    return {
+        "state": "sconosciuto",
+        "label": "Traffico: copertura sconosciuta",
+        "reason": (
+            "Topologia/porta/link non abbastanza chiari per giudicare "
+            "cosa lo SPAN vede."
+        ),
+    }
+
+
+def _asset_on_mirror_source_port(db: Session, asset: Asset) -> bool:
+    macs = {
+        normalize_mac(iface.mac)
+        for iface in (asset.interfaces or [])
+        if iface.mac and not is_synthetic_ip_mac(iface.mac)
+    }
+    ports = db.scalars(
+        select(SwitchPort).options(joinedload(SwitchPort.switch))
+    ).unique().all()
+    for port in ports:
+        sw = port.switch
+        if not sw or sw.code != MIRROR_SWITCH_CODE:
+            continue
+        if int(port.number) not in MIRROR_SOURCE_PORTS:
+            continue
+        if port.asset_id == asset.id:
+            return True
+        observed = {normalize_mac(m) for m in (port.observed_macs or []) if m}
+        if macs & observed:
+            return True
+    return False
+
+
+def _path_crosses_mirror_sources(path: dict[str, Any]) -> bool:
+    for eid in path.get("highlight_edges") or []:
+        match = _UPLINK_EDGE_RE.match(str(eid).strip())
+        if not match:
+            continue
+        left_sw, left_p, right_sw, right_p = (
+            match.group(1).lower(),
+            int(match.group(2)),
+            match.group(3).lower(),
+            int(match.group(4)),
+        )
+        if left_sw == MIRROR_SWITCH_CODE and left_p in MIRROR_SOURCE_PORTS:
+            return True
+        if right_sw == MIRROR_SWITCH_CODE and right_p in MIRROR_SOURCE_PORTS:
+            return True
+    return False
+
+
+def _empty_kind(
+    *,
+    samples: int,
+    coverage_state: str,
+) -> Optional[str]:
+    if samples == 0:
+        if coverage_state == "completo":
+            return "silence_observed"
+        if coverage_state == "parziale":
+            return "maybe_unmirrored"
+        return "unknown_gap"
+    if samples <= THIN_SAMPLE_MAX:
+        return "thin_sample"
+    return None
+
+
+def _mine_flow_ids_sql() -> str:
+    """Set-based gate: binding history + tie → exclude (HAVING COUNT=1)."""
+    return """
+    WITH candidates AS (
+      SELECT
+        f.id AS flow_id,
+        a.id AS asset_id
+      FROM flow_observations f
+      JOIN ip_addresses ip
+        ON ip.ip = f.src_ip
+       AND ip.first_seen <= f.observed_at
+      JOIN interfaces i ON i.id = ip.interface_id
+      JOIN assets a ON a.id = i.asset_id
+      WHERE f.observed_at >= :since
+        AND NOT (
+          UPPER(i.mac) LIKE 'FE:%'
+          AND LENGTH(i.mac) = 17
+          AND substr(i.mac, 16, 2) = '00'
+        )
+        AND (
+          ip.is_current = 1
+          OR (ip.last_seen IS NOT NULL AND ip.last_seen >= f.observed_at)
+        )
+    ),
+    resolved AS (
+      SELECT flow_id, MIN(asset_id) AS asset_id
+      FROM candidates
+      GROUP BY flow_id
+      HAVING COUNT(DISTINCT asset_id) = 1
+    ),
+    mine AS (
+      SELECT f.*
+      FROM flow_observations f
+      JOIN resolved r ON r.flow_id = f.id
+      WHERE r.asset_id = :asset_id
+    )
+    """
+
+
+def asset_habits(
+    db: Session,
+    asset_id: int,
+    *,
+    days: int = DEFAULT_DAYS,
+    now: Optional[datetime] = None,
+    top_destinations: int = TOP_DESTINATIONS,
+    top_ports: int = TOP_PORTS,
+) -> Optional[dict[str, Any]]:
+    """Return habits payload for one asset, or None if asset missing."""
+    asset = db.scalar(
+        select(Asset)
+        .where(Asset.id == asset_id)
+        .options(joinedload(Asset.interfaces))
+    )
+    if not asset:
+        return None
+
+    now = now or _utc_now()
+    days = max(1, min(MAX_DAYS, int(days or DEFAULT_DAYS)))
+    since = now - timedelta(days=days)
+    coverage = classify_flow_coverage(db, asset)
+
+    mine_cte = _mine_flow_ids_sql()
+    params = {"asset_id": asset_id, "since": since}
+
+    totals_row = db.execute(
+        text(
+            mine_cte
+            + """
+            SELECT
+              COUNT(*) AS samples,
+              COALESCE(SUM(bytes), 0) AS bytes_total,
+              SUM(bytes_out) AS bytes_out_sum,
+              SUM(bytes_in) AS bytes_in_sum,
+              SUM(CASE WHEN bytes_out IS NOT NULL THEN 1 ELSE 0 END) AS samples_with_dir,
+              MIN(CASE WHEN bytes_out IS NOT NULL THEN observed_at END) AS dir_first_at
+            FROM mine
+            """
+        ),
+        params,
+    ).mappings().one()
+
+    samples = int(totals_row["samples"] or 0)
+    samples_with_dir = int(totals_row["samples_with_dir"] or 0)
+    bytes_total = int(totals_row["bytes_total"] or 0)
+    # SQL SUM already yields NULL when all NULL; keep as None.
+    bytes_out = (
+        int(totals_row["bytes_out_sum"])
+        if totals_row["bytes_out_sum"] is not None
+        else None
+    )
+    bytes_in = (
+        int(totals_row["bytes_in_sum"])
+        if totals_row["bytes_in_sum"] is not None
+        else None
+    )
+    dir_first = totals_row["dir_first_at"]
+    if isinstance(dir_first, str):
+        try:
+            dir_first = datetime.fromisoformat(dir_first.replace("Z", ""))
+        except ValueError:
+            dir_first = None
+
+    dest_rows = db.execute(
+        text(
+            mine_cte
+            + """
+            SELECT
+              dst_ip,
+              COUNT(*) AS samples,
+              COALESCE(SUM(bytes), 0) AS bytes_total,
+              SUM(bytes_out) AS bytes_out_sum,
+              SUM(bytes_in) AS bytes_in_sum,
+              SUM(CASE WHEN bytes_out IS NOT NULL THEN 1 ELSE 0 END) AS samples_with_dir
+            FROM mine
+            GROUP BY dst_ip
+            ORDER BY bytes_total DESC
+            LIMIT :lim
+            """
+        ),
+        {**params, "lim": max(1, int(top_destinations))},
+    ).mappings().all()
+
+    port_rows = db.execute(
+        text(
+            mine_cte
+            + """
+            SELECT
+              dst_port AS port,
+              proto,
+              COUNT(*) AS samples,
+              COALESCE(SUM(bytes), 0) AS bytes_total
+            FROM mine
+            GROUP BY dst_port, proto
+            ORDER BY bytes_total DESC
+            LIMIT :lim
+            """
+        ),
+        {**params, "lim": max(1, int(top_ports))},
+    ).mappings().all()
+
+    hour_rows = db.execute(
+        text(
+            mine_cte
+            + """
+            SELECT
+              CAST(strftime('%H', observed_at) AS INTEGER) AS hour,
+              COUNT(*) AS samples,
+              COALESCE(SUM(bytes), 0) AS bytes_total
+            FROM mine
+            GROUP BY hour
+            ORDER BY hour
+            """
+        ),
+        params,
+    ).mappings().all()
+
+    destinations = [
+        {
+            "dst_ip": (row["dst_ip"] or "").strip(),
+            "dst_name": None,  # Wave 1b
+            "bytes": int(row["bytes_total"] or 0),
+            "bytes_out": (
+                int(row["bytes_out_sum"]) if row["bytes_out_sum"] is not None else None
+            ),
+            "bytes_in": (
+                int(row["bytes_in_sum"]) if row["bytes_in_sum"] is not None else None
+            ),
+            "samples": int(row["samples"] or 0),
+            "samples_with_direction": int(row["samples_with_dir"] or 0),
+        }
+        for row in dest_rows
+        if (row["dst_ip"] or "").strip()
+    ]
+
+    ports = [
+        {
+            "port": int(row["port"] or 0),
+            "proto": (row["proto"] or "").strip() or "tcp",
+            "bytes": int(row["bytes_total"] or 0),
+            "samples": int(row["samples"] or 0),
+        }
+        for row in port_rows
+    ]
+
+    # Dense 0–23 UTC hours (missing bins → 0) for sparkline-friendly payload.
+    by_hour = {
+        int(row["hour"]): {
+            "hour": int(row["hour"]),
+            "bytes": int(row["bytes_total"] or 0),
+            "samples": int(row["samples"] or 0),
+        }
+        for row in hour_rows
+        if row["hour"] is not None
+    }
+    hours = [
+        by_hour.get(h, {"hour": h, "bytes": 0, "samples": 0}) for h in range(24)
+    ]
+
+    empty_kind = _empty_kind(samples=samples, coverage_state=coverage["state"])
+    ratio = (samples_with_dir / samples) if samples else 0.0
+
+    return {
+        "asset_id": asset_id,
+        "window_days": days,
+        "timezone": HABITS_TIMEZONE,
+        "hours_basis": "utc",
+        "coverage": coverage,
+        "direction_since": (
+            dir_first.isoformat() + "Z" if isinstance(dir_first, datetime) else None
+        ),
+        "direction_sample_ratio": round(ratio, 4),
+        "totals": {
+            "bytes": bytes_total,
+            "bytes_out": bytes_out,
+            "bytes_in": bytes_in,
+            "samples": samples,
+            "samples_with_direction": samples_with_dir,
+        },
+        "destinations": destinations,
+        "ports": ports,
+        "hours": hours,
+        "empty_kind": empty_kind,
+    }
diff --git a/observatory/tests/test_habits.py b/observatory/tests/test_habits.py
new file mode 100644
--- /dev/null
+++ b/observatory/tests/test_habits.py
+++ b/observatory/tests/test_habits.py
@@ -0,0 +1,317 @@
+"""GET /api/assets/{id}/habits — Wave 1a gate + coverage + mix-aware."""
+
+from __future__ import annotations
+
+import sys
+import uuid
+from datetime import datetime, timedelta
+from pathlib import Path
+
+import pytest
+from sqlalchemy import create_engine
+from sqlalchemy.orm import sessionmaker
+
+sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "api"))
+
+from app.db import Base
+from app.models import Asset, FlowObservation, Interface, IpAddress, Switch, SwitchPort
+from app.services.habits import (
+    MIRROR_SOURCE_PORTS,
+    asset_habits,
+    classify_flow_coverage,
+)
+from app.services.identity import upsert_observation_asset
+
+
+@pytest.fixture()
+def db(tmp_path):
+    eng = create_engine(f"sqlite:///{tmp_path / 'habits.db'}")
+    Base.metadata.create_all(eng)
+    Session = sessionmaker(bind=eng)
+    session = Session()
+    yield session
+    session.close()
+
+
+def _flow(
+    *,
+    dedup: str,
+    src: str,
+    dst: str,
+    at: datetime,
+    bytes_n: int = 100,
+    bytes_out=None,
+    bytes_in=None,
+    port: int = 443,
+    proto: str = "tcp",
+):
+    return FlowObservation(
+        dedup_key=dedup,
+        sensor_id="zeek-span",
+        src_ip=src,
+        dst_ip=dst,
+        dst_port=port,
+        proto=proto,
+        bytes=bytes_n,
+        bytes_out=bytes_out,
+        bytes_in=bytes_in,
+        byte_layer="app" if bytes_out is not None else None,
+        observed_at=at,
+    )
+
+
+def test_habits_tie_excludes_ambiguous_ip(db):
+    """Two assets share IP at T → flow excluded (HAVING COUNT=1)."""
+    now = datetime(2026, 7, 22, 12, 0, 0)
+    hour = datetime(2026, 7, 22, 10, 0, 0)
+
+    a = upsert_observation_asset(db, mac="AA:BB:CC:DD:01:01", ip="10.0.0.50", source="nmap")
+    b = upsert_observation_asset(db, mac="AA:BB:CC:DD:02:02", ip="10.0.0.99", source="nmap")
+    db.flush()
+
+    # Give B the same IP overlapping the flow hour (tie).
+    iface_b = b.interfaces[0]
+    db.add(
+        IpAddress(
+            interface_id=iface_b.id,
+            ip="10.0.0.50",
+            is_current=False,
+            first_seen=hour - timedelta(days=1),
+            last_seen=hour + timedelta(hours=2),
+            source="nmap",
+        )
+    )
+    # A's binding covers the hour
+    for iface in a.interfaces:
+        for addr in iface.addresses:
+            if addr.ip == "10.0.0.50":
+                addr.first_seen = hour - timedelta(days=2)
+                addr.is_current = True
+    db.add(
+        _flow(
+            dedup="tie1",
+            src="10.0.0.50",
+            dst="8.8.8.8",
+            at=hour,
+            bytes_n=500,
+            bytes_out=400,
+            bytes_in=100,
+        )
+    )
+    db.commit()
+
+    habits_a = asset_habits(db, a.id, days=7, now=now)
+    habits_b = asset_habits(db, b.id, days=7, now=now)
+    assert habits_a is not None and habits_b is not None
+    assert habits_a["totals"]["samples"] == 0
+    assert habits_b["totals"]["samples"] == 0
+    assert habits_a["empty_kind"] in {
+        "silence_observed",
+        "maybe_unmirrored",
+        "unknown_gap",
+    }
+
+
+def test_habits_unique_binding_includes_flow(db):
+    now = datetime(2026, 7, 22, 12, 0, 0)
+    hour = datetime(2026, 7, 22, 10, 0, 0)
+    asset = upsert_observation_asset(
+        db, mac="AA:BB:CC:DD:03:03", ip="10.0.0.10", source="nmap"
+    )
+    db.flush()
+    for iface in asset.interfaces:
+        for addr in iface.addresses:
+            addr.first_seen = hour - timedelta(days=1)
+            addr.is_current = True
+    db.add(
+        _flow(
+            dedup="ok1",
+            src="10.0.0.10",
+            dst="1.1.1.1",
+            at=hour,
+            bytes_n=90,
+            bytes_out=60,
+            bytes_in=30,
+        )
+    )
+    db.add(
+        _flow(
+            dedup="ok2",
+            src="10.0.0.10",
+            dst="8.8.8.8",
+            at=hour,
+            bytes_n=50,
+            bytes_out=50,
+            bytes_in=0,
+            port=53,
+            proto="udp",
+        )
+    )
+    db.commit()
+
+    habits = asset_habits(db, asset.id, days=7, now=now)
+    assert habits["totals"]["samples"] == 2
+    assert habits["totals"]["bytes"] == 140
+    assert habits["totals"]["bytes_out"] == 110
+    assert habits["totals"]["bytes_in"] == 30
+    assert habits["direction_since"] is not None
+    assert habits["timezone"] == "Europe/Rome"
+    assert habits["hours_basis"] == "utc"
+    assert len(habits["hours"]) == 24
+    assert habits["hours"][10]["bytes"] == 140
+    assert len(habits["destinations"]) == 2
+    assert habits["destinations"][0]["dst_name"] is None
+    # 2 samples ≤ THIN_SAMPLE_MAX(4) → thin_sample
+    assert habits["empty_kind"] == "thin_sample"
+
+
+def test_habits_mix_aware_null_direction(db):
+    """Legacy NULL out/in must not become 0; mix with directional rows."""
+    now = datetime(2026, 7, 22, 12, 0, 0)
+    hour = datetime(2026, 7, 22, 9, 0, 0)
+    asset = upsert_observation_asset(
+        db, mac="AA:BB:CC:DD:04:04", ip="10.0.0.20", source="nmap"
+    )
+    db.flush()
+    for iface in asset.interfaces:
+        for addr in iface.addresses:
+            addr.first_seen = hour - timedelta(days=1)
+            addr.is_current = True
+    db.add(
+        _flow(
+            dedup="leg",
+            src="10.0.0.20",
+            dst="9.9.9.9",
+            at=hour,
+            bytes_n=1000,
+            bytes_out=None,
+            bytes_in=None,
+        )
+    )
+    db.add(
+        _flow(
+            dedup="new",
+            src="10.0.0.20",
+            dst="9.9.9.9",
+            at=hour + timedelta(hours=1),
+            bytes_n=100,
+            bytes_out=70,
+            bytes_in=30,
+        )
+    )
+    db.commit()
+
+    habits = asset_habits(db, asset.id, days=7, now=now)
+    assert habits["totals"]["bytes"] == 1100
+    assert habits["totals"]["bytes_out"] == 70
+    assert habits["totals"]["bytes_in"] == 30
+    assert habits["totals"]["samples_with_direction"] == 1
+    dest = habits["destinations"][0]
+    assert dest["bytes"] == 1100
+    assert dest["bytes_out"] == 70
+    assert dest["bytes_in"] == 30
+
+
+def test_habits_all_null_direction_stays_null(db):
+    now = datetime(2026, 7, 22, 12, 0, 0)
+    hour = datetime(2026, 7, 22, 8, 0, 0)
+    asset = upsert_observation_asset(
+        db, mac="AA:BB:CC:DD:05:05", ip="10.0.0.30", source="nmap"
+    )
+    db.flush()
+    for iface in asset.interfaces:
+        for addr in iface.addresses:
+            addr.first_seen = hour - timedelta(days=1)
+            addr.is_current = True
+    for i in range(5):
+        db.add(
+            _flow(
+                dedup=f"n{i}",
+                src="10.0.0.30",
+                dst=f"8.8.8.{i}",
+                at=hour,
+                bytes_n=10,
+                bytes_out=None,
+                bytes_in=None,
+            )
+        )
+    db.commit()
+    habits = asset_habits(db, asset.id, days=7, now=now)
+    assert habits["totals"]["samples"] == 5
+    assert habits["totals"]["bytes"] == 50
+    assert habits["totals"]["bytes_out"] is None
+    assert habits["totals"]["bytes_in"] is None
+    assert habits["direction_since"] is None
+    assert habits["empty_kind"] is None  # 5 > thin threshold
+
+
+def test_coverage_wifi_partial(db):
+    asset = Asset(uid=str(uuid.uuid4()), name="wifi-cam", meta={"link": {"media": "wifi"}})
+    db.add(asset)
+    db.flush()
+    db.add(Interface(asset_id=asset.id, mac="AA:BB:CC:10:00:01"))
+    db.commit()
+    cov = classify_flow_coverage(db, asset)
+    assert cov["state"] == "parziale"
+    assert "WiFi" in cov["reason"]
+
+
+def test_coverage_mirror_source_completo(db):
+    assert 21 in MIRROR_SOURCE_PORTS
+    core = Switch(code="328c", name="LGS328C", model="LGS328C", role="core", port_count=28)
+    db.add(core)
+    db.flush()
+    asset = Asset(uid=str(uuid.uuid4()), name="on-p21", meta={"link": {"media": "ethernet"}})
+    db.add(asset)
+    db.flush()
+    db.add(Interface(asset_id=asset.id, mac="AA:BB:CC:10:00:21"))
+    port = SwitchPort(
+        switch_id=core.id,
+        number=21,
+        asset_id=asset.id,
+        observed_macs=["AA:BB:CC:10:00:21"],
+    )
+    db.add(port)
+    db.commit()
+    asset = db.get(Asset, asset.id)
+    cov = classify_flow_coverage(db, asset)
+    assert cov["state"] == "completo"
+
+
+def test_coverage_unknown_without_path(db):
+    asset = Asset(uid=str(uuid.uuid4()), name="orphan", meta={})
+    db.add(asset)
+    db.flush()
+    db.add(Interface(asset_id=asset.id, mac="AA:BB:CC:10:00:99"))
+    db.commit()
+    cov = classify_flow_coverage(db, asset)
+    assert cov["state"] == "sconosciuto"
+
+
+def test_empty_kind_silence_vs_unmirrored(db):
+    now = datetime(2026, 7, 22, 12, 0, 0)
+    # completo + no flows
+    core = Switch(code="328c", name="LGS328C", model="LGS328C", role="core", port_count=28)
+    db.add(core)
+    db.flush()
+    wired = Asset(uid=str(uuid.uuid4()), name="quiet", meta={"link": {"media": "ethernet"}})
+    db.add(wired)
+    db.flush()
+    db.add(Interface(asset_id=wired.id, mac="AA:BB:CC:10:01:01"))
+    db.add(SwitchPort(switch_id=core.id, number=1, asset_id=wired.id))
+    wifi = Asset(uid=str(uuid.uuid4()), name="quiet-wifi", meta={"link": {"media": "wifi"}})
+    db.add(wifi)
+    db.flush()
+    db.add(Interface(asset_id=wifi.id, mac="AA:BB:CC:10:01:02"))
+    db.commit()
+
+    h_w = asset_habits(db, wired.id, days=7, now=now)
+    h_f = asset_habits(db, wifi.id, days=7, now=now)
+    assert h_w["coverage"]["state"] == "completo"
+    assert h_w["empty_kind"] == "silence_observed"
+    assert h_f["coverage"]["state"] == "parziale"
+    assert h_f["empty_kind"] == "maybe_unmirrored"
+
+
+def test_habits_404_missing_asset(db):
+    assert asset_habits(db, 99999, days=7) is None
diff --git a/observatory/api/app/routers/assets.py b/observatory/api/app/routers/assets.py
index 7c25024..4d0d2cf 100644
--- a/observatory/api/app/routers/assets.py
+++ b/observatory/api/app/routers/assets.py
@@ -10,11 +10,10 @@ from sqlalchemy.orm import Session, joinedload
 from app.auth import audit, check_csrf, require_role, require_user
 from app.config import Settings, get_settings
 from app.db import get_db
 from app.models import Asset, InternetAccessControl, Interface, IpAddress, Monitor, SwitchPort, User
 from app.schemas import AssetOut, AssetUpdate
-from app.services.identity import score_identity
 from app.services.event_maintenance import split_name_proposals
 from app.services.inventory import (
     current_ip,
     is_synthetic_fritz_name,
     ping_ip,
@@ -488,15 +487,90 @@ def get_asset(asset_id: int, db: Session = Depends(get_db), user: User = Depends
         raise HTTPException(404, "Asset non trovato")
     return _serialize(db, asset, with_path=True)
 
 
 @router.get("/{asset_id}/identity")
-def identity(asset_id: int, db: Session = Depends(get_db), user: User = Depends(require_user)):
-    asset = db.get(Asset, asset_id)
+def identity(
+    asset_id: int,
+    technical: bool = Query(False, description="Includi grezzi fingerprint/proposals"),
+    db: Session = Depends(get_db),
+    user: User = Depends(require_user),
+):
+    """Fatti puliti «Chi sei» (+ score/grezzi se technical=1)."""
+    from app.services.asset_identity import build_asset_identity, load_asset_for_identity
+
+    asset = load_asset_for_identity(db, asset_id)
+    if not asset:
+        raise HTTPException(404, "Asset non trovato")
+    return build_asset_identity(db, asset, include_technical=technical)
+
+
+@router.get("/{asset_id}/habits")
+def habits(
+    asset_id: int,
+    days: int = Query(7, ge=1, le=30),
+    db: Session = Depends(get_db),
+    user: User = Depends(require_user),
+):
+    """Wave 1a: abitudini di traffico (descrittivo, gate resolve IP@t)."""
+    from app.services.habits import asset_habits
+
+    payload = asset_habits(db, asset_id, days=days)
+    if payload is None:
+        raise HTTPException(404, "Asset non trovato")
+    return payload
+
+
+@router.post("/{asset_id}/scan-os")
+def scan_os(
+    asset_id: int,
+    request: Request,
+    db: Session = Depends(get_db),
+    settings: Settings = Depends(get_settings),
+    user: User = Depends(require_role("operator")),
+):
+    """On-demand OS fingerprint (nmap -O via profilo os_fingerprint). Mai nel discovery."""
+    from app.services.scans import enqueue_on_demand_os_fingerprint
+    from sqlalchemy.orm import joinedload
+
+    check_csrf(request, settings)
+    asset = db.scalar(
+        select(Asset)
+        .where(Asset.id == asset_id)
+        .options(
+            joinedload(Asset.interfaces).joinedload(Interface.addresses),
+            joinedload(Asset.name_proposals),
+        )
+    )
     if not asset:
         raise HTTPException(404, "Asset non trovato")
-    return score_identity(asset)
+    result = enqueue_on_demand_os_fingerprint(
+        db, asset, settings=settings, user_id=user.id
+    )
+    if result.get("excluded"):
+        raise HTTPException(409, result.get("message") or "device escluso da OS scan per fragilità")
+    if result.get("unavailable"):
+        raise HTTPException(
+            503, result.get("message") or "OS non disponibile, scanner non privilegiato"
+        )
+    if not result.get("ok"):
+        raise HTTPException(400, result.get("message") or "Impossibile avviare OS scan")
+    from app.services.asset_identity import latest_os_mac_mismatch_attribution
+
+    attribution = latest_os_mac_mismatch_attribution(db, asset_id)
+    if attribution:
+        result["os_attribution"] = attribution
+    audit(
+        db,
+        user=user,
+        action="scan.os_ondemand",
+        entity="asset",
+        entity_id=str(asset_id),
+        detail={"scan_id": result.get("scan_id"), "target": result.get("target")},
+    )
+    db.commit()
+    return result
 
 
 @router.patch("/{asset_id}", response_model=AssetOut)
 def update_asset(
     asset_id: int,
@@ -510,10 +584,11 @@ def update_asset(
     asset = db.get(Asset, asset_id)
     if not asset:
         raise HTTPException(404, "Asset non trovato")
     data = body.model_dump(exclude_unset=True)
     watch_flag = data.pop("watch_fingerprint", None)
+    os_opt_out = data.pop("os_fingerprint_opt_out", None)
     old_crit, old_cat = asset.is_critical, asset.category
     for k, v in data.items():
         setattr(asset, k, v)
     if watch_flag is True:
         from app.services.watch import enable_watch
@@ -525,18 +600,25 @@ def update_asset(
         )
     elif watch_flag is False:
         from app.services.watch import disable_watch
 
         disable_watch(asset)
+    if os_opt_out is not None:
+        from app.services.os_scan_guard import set_os_fingerprint_opt_out
+
+        set_os_fingerprint_opt_out(asset, bool(os_opt_out))
     touch_monitor = ("is_critical" in data and asset.is_critical != old_crit) or (
         "category" in data and asset.category != old_cat
     )
     meta = dict(asset.meta or {})
     overrides = set(meta.get("manual_overrides") or [])
     overrides.update(data)
     if watch_flag is not None:
         overrides.add("watch_fingerprint")
+    if os_opt_out is not None:
+        overrides.add("os_fingerprint_opt_out")
+        meta["os_fingerprint_opt_out"] = bool(os_opt_out)
     meta["manual_overrides"] = sorted(overrides)
     sources = dict(meta.get("field_sources") or {})
     now = datetime.utcnow()
     for field in data:
         sources[field] = {
@@ -548,15 +630,26 @@ def update_asset(
         sources["watch_fingerprint"] = {
             "source": "manuale",
             "confidence": 1.0,
             "last_seen": now.isoformat() + "Z",
         }
+    if os_opt_out is not None:
+        sources["os_fingerprint_opt_out"] = {
+            "source": "manuale",
+            "confidence": 1.0,
+            "last_seen": now.isoformat() + "Z",
+        }
     meta["field_sources"] = sources
     # Re-read watch keys into meta after enable/disable mutated asset.meta
     watch_meta = dict((asset.meta or {}).get("watch") or {})
     if watch_meta:
         meta["watch"] = watch_meta
+    # Keep opt-out if set earlier on asset.meta (watch path may have replaced meta)
+    if os_opt_out is not None:
+        meta["os_fingerprint_opt_out"] = bool(os_opt_out)
+    elif "os_fingerprint_opt_out" in (asset.meta or {}):
+        meta["os_fingerprint_opt_out"] = bool((asset.meta or {}).get("os_fingerprint_opt_out"))
     asset.meta = meta
     asset.updated_at = now
     if touch_monitor:
         from app.services.monitoring import reconcile_asset_monitor
 
@@ -569,11 +662,19 @@ def update_asset(
         db,
         user=user,
         action="asset.update",
         entity="asset",
         entity_id=str(asset.id),
-        detail={**data, **({"watch_fingerprint": watch_flag} if watch_flag is not None else {})},
+        detail={
+            **data,
+            **({"watch_fingerprint": watch_flag} if watch_flag is not None else {}),
+            **(
+                {"os_fingerprint_opt_out": os_opt_out}
+                if os_opt_out is not None
+                else {}
+            ),
+        },
         ip=request.client.host if request.client else "",
     )
     db.commit()
     db.refresh(asset)
     return _serialize(db, asset)
diff --git a/observatory/docs/KNOWN_DEBT.md b/observatory/docs/KNOWN_DEBT.md
index ce545d0..6367f14 100644
--- a/observatory/docs/KNOWN_DEBT.md
+++ b/observatory/docs/KNOWN_DEBT.md
@@ -1,9 +1,17 @@
 # Debito noto (bassa priorità)
 
 Voci consapevoli, non in coda di fix immediata. Non “dimenticate”: esplicite e fuori scope finché non riprese.
 
+## DEBT-MIRROR-SOURCES
+
+- **Priorità:** bassa (Wave 1a behavioural) — config nota, non modellata in DB
+- **Cosa:** le porte **sorgente** del port-mirror sul LGS328C (`p1`, `p21`, `p24` → sink `p22` / Cassiopea eth1) sono una **costante** in `api/app/services/habits.py` (`MIRROR_SOURCE_PORTS`) usata per il badge coverage «Abitudini».
+- **Perché debito:** oggi è runbook/hardcode; uno spostamento fisico del mirror senza aggiornare il codice mentirebbe sulla coverage.
+- **Fix quando servirà:** tabella/config persistita (es. `switch_ports.role=span_source` o meta switch) + bootstrap da doc; togliere la costante.
+- **Vietato:** inferire le sorgenti mirror dalla sola assenza di flow; confondere sink `p22` con sorgente.
+
 ## DEBT-GROUPING-VIRTUAL-MAC
 
 - **Priorità:** FASE B **deployata** (RULE_VERSION=2) + hotfix presentazione (`pickPrimary` / KPI chassis-aware). Residuo noto sotto.
 - **Origine:** verifica L2 «Nuovi» 2026-07-21 (`docs/verifica-nuovi-l2-20260721.txt`); ricognizione FASE A 2026-07-21.
 - **Regole (rule_version=2):**
@@ -84,5 +92,13 @@ Voci consapevoli, non in coda di fix immediata. Non “dimenticate”: esplicite
 - **Priorità:** bassa / policy da progettare
 - **Sintomo:** dopo triage stale FASE 2, resta la classe (d) `local_mac_con_ip` (MAC locally-administered con IP): a ogni rotazione privacy Wi‑Fi rifà apparire stale one-shot.
 - **Origine:** MAC privacy (bit U/L) visti con IP in finestra breve; non ignorabili alla cieca come la classe (a) senza IP.
 - **Fix quando servirà:** policy TTL auto-ignore (es. local MAC + no curation + inactivity N giorni) — non ora.
 - **Vietato ora:** bulk ignorato della (d); DELETE asset; merge/fusion ad hoc.
+
+## DEBT-COLLECTOR-PRIVILEGED
+
+- **Stato:** **RISOLTO PER RIMOZIONE** in codice 0.9.10 (pre-deploy review).
+- **Cosa è cambiato:** nmap installato nell’immagine collector; esecuzione diretta; **eliminati** mount `docker.sock` e `privileged: true`. Restano `cap_add: NET_RAW, NET_ADMIN`.
+- **Gate operativo:** `SCANNER_PRIVILEGED` resta `false` finché staging non conferma: (1) discovery `-sn` con MAC/ARP, (2) un `os_fingerprint` con flag true produce `osmatch`. Solo allora alzare il flag sul NAS.
+- **Residuo:** `run_deep_scan` API non usa più docker nested — richiede `nmap` nell’immagine API o la coda Azioni (`full_tcp`). Fuori dal vettore sock.
+- **Vietato:** reintrodurre docker.sock sul collector; `privileged: true` “per sicurezza”; alzare `SCANNER_PRIVILEGED` senza smoke ARP/-O.
```
