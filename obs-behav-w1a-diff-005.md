<!-- BLOCK-ID: OBS-BEHAV-W1A-DIFF-005 -->

# OBS-BEHAV-W1A-DIFF-005 — Parte 1 pipeline direzione

Scope: dati only (parser → ingest → DB → flows_summary). STOP pre-UI/Dossier.

File: `zeek_conn.py`, `evolution.py` (FlowIn/ingest), `FlowObservation`, Alembic `h8e4f5a6b7c8`, `flows_summary.py`.

Test: `14 passed` (`test_zeek_conn_provider` + `test_flows_summary`).

```diff
diff --git a/observatory/api/app/routers/evolution.py b/observatory/api/app/routers/evolution.py
index 0c5b5a1..2dd71dd 100644
--- a/observatory/api/app/routers/evolution.py
+++ b/observatory/api/app/routers/evolution.py
@@ -29,17 +29,38 @@ class FindingUpdate(BaseModel):
     status: Optional[str] = None
     assignee: Optional[str] = None
     notes: Optional[str] = None
 
 
+def _add_optional_flow_int(existing: Optional[int], incoming: Optional[int]) -> Optional[int]:
+    if incoming is None:
+        return existing
+    if existing is None:
+        return int(incoming)
+    return int(existing) + int(incoming)
+
+
+def _merge_byte_layer(a: Optional[str], b: Optional[str]) -> Optional[str]:
+    if a is None:
+        return b
+    if b is None:
+        return a
+    if a == b:
+        return a
+    return "mixed"
+
+
 class FlowIn(BaseModel):
     sensor_id: str = "remote"
     src_ip: str = ""
     dst_ip: str = ""
     dst_port: int = 0
     proto: str = "tcp"
     bytes: int = 0
+    bytes_out: Optional[int] = None
+    bytes_in: Optional[int] = None
+    byte_layer: Optional[str] = None
     dst_asn: str = ""
     dst_country: str = ""
     observed_at: Optional[datetime] = None
     raw: dict[str, Any] = Field(default_factory=dict)
 
@@ -231,10 +252,13 @@ def ingest_flow(
         f"{body.sensor_id}|flow|{bucket}|{entity}".encode()
     ).hexdigest()[:40]
     existing = db.scalar(select(FlowObservation).where(FlowObservation.dedup_key == dedup))
     if existing:
         existing.bytes = int(existing.bytes or 0) + int(body.bytes or 0)
+        existing.bytes_out = _add_optional_flow_int(existing.bytes_out, body.bytes_out)
+        existing.bytes_in = _add_optional_flow_int(existing.bytes_in, body.bytes_in)
+        existing.byte_layer = _merge_byte_layer(existing.byte_layer, body.byte_layer)
         from app.services.watch import note_traffic_for_ips
 
         note_traffic_for_ips(
             db,
             ips=[body.src_ip, body.dst_ip],
@@ -251,10 +275,13 @@ def ingest_flow(
         src_ip=body.src_ip,
         dst_ip=body.dst_ip,
         dst_port=body.dst_port,
         proto=body.proto,
         bytes=body.bytes,
+        bytes_out=body.bytes_out,
+        bytes_in=body.bytes_in,
+        byte_layer=body.byte_layer,
         dst_asn=body.dst_asn,
         dst_country=body.dst_country,
         observed_at=observed,
         payload=body.raw,
     )
diff --git a/observatory/api/app/services/flows_summary.py b/observatory/api/app/services/flows_summary.py
index ec2bcb3..a91905e 100644
--- a/observatory/api/app/services/flows_summary.py
+++ b/observatory/api/app/services/flows_summary.py
@@ -130,15 +130,21 @@ def flow_summary(
         slot = by_src.get(src)
         if slot is None:
             by_src[src] = {
                 "src_ip": src,
                 "bytes": int(row.bytes or 0),
+                "bytes_out": row.bytes_out,
+                "bytes_in": row.bytes_in,
                 "dsts": {((row.dst_ip or "").strip())},
                 "samples": 1,
             }
         else:
             slot["bytes"] = int(slot["bytes"] or 0) + int(row.bytes or 0)
+            if row.bytes_out is not None:
+                slot["bytes_out"] = int(slot["bytes_out"] or 0) + int(row.bytes_out)
+            if row.bytes_in is not None:
+                slot["bytes_in"] = int(slot["bytes_in"] or 0) + int(row.bytes_in)
             if (row.dst_ip or "").strip():
                 slot["dsts"].add((row.dst_ip or "").strip())
             slot["samples"] = int(slot.get("samples") or 0) + 1
 
     ranked = sorted(by_src.values(), key=lambda s: int(s["bytes"] or 0), reverse=True)[
@@ -153,10 +159,16 @@ def flow_summary(
                 "src_ip": slot["src_ip"],
                 "asset_id": asset.id if asset else None,
                 "asset_name": (asset.name or "").strip() or None if asset else None,
                 "dst_distinct": len(dsts),
                 "bytes": int(slot["bytes"] or 0),
+                "bytes_out": (
+                    int(slot["bytes_out"]) if slot.get("bytes_out") is not None else None
+                ),
+                "bytes_in": (
+                    int(slot["bytes_in"]) if slot.get("bytes_in") is not None else None
+                ),
                 "samples": int(slot.get("samples") or 0),
             }
         )
 
     provider = provider_state_info(zeek_log_dir=zeek_log_dir, now=now)
diff --git a/observatory/collector/collector/adapters/zeek_conn.py b/observatory/collector/collector/adapters/zeek_conn.py
index 74ad49e..634aea3 100644
--- a/observatory/collector/collector/adapters/zeek_conn.py
+++ b/observatory/collector/collector/adapters/zeek_conn.py
@@ -52,10 +52,70 @@ def parse_conn_ts(value: Any) -> Optional[datetime]:
         return dt
     except ValueError:
         return None
 
 
+def _optional_nonneg_int(value: Any) -> Optional[int]:
+    """Parse Zeek byte field; None/missing stay None (never silent null→0)."""
+    if value is None:
+        return None
+    if isinstance(value, str) and not value.strip():
+        return None
+    try:
+        return max(0, int(value))
+    except (TypeError, ValueError):
+        return None
+
+
+def _merge_byte_layer(a: Optional[str], b: Optional[str]) -> Optional[str]:
+    if a is None:
+        return b
+    if b is None:
+        return a
+    if a == b:
+        return a
+    return "mixed"
+
+
+def _add_optional_int(a: Optional[int], b: Optional[int]) -> Optional[int]:
+    if a is None and b is None:
+        return None
+    return int(a or 0) + int(b or 0)
+
+
+def resolve_conn_byte_sides(row: dict[str, Any]) -> tuple[Optional[int], Optional[int], Optional[str]]:
+    """App-layer first; IP-bytes fallback; never silent null→0 without byte_layer.
+
+    Returns (bytes_out, bytes_in, byte_layer) where out=orig, in=resp.
+    """
+    orig_app = _optional_nonneg_int(row.get("orig_bytes"))
+    resp_app = _optional_nonneg_int(row.get("resp_bytes"))
+    orig_ip = _optional_nonneg_int(row.get("orig_ip_bytes"))
+    resp_ip = _optional_nonneg_int(row.get("resp_ip_bytes"))
+
+    if orig_app is not None and resp_app is not None:
+        return orig_app, resp_app, "app"
+
+    if orig_app is not None and resp_app is None:
+        # One-way only if reverse IP confirms no return traffic.
+        if resp_ip is None or resp_ip == 0:
+            return orig_app, 0, "app"
+        out = orig_ip if orig_ip is not None else orig_app
+        return out, resp_ip, "ip"
+
+    if orig_app is None and resp_app is not None:
+        if orig_ip is None or orig_ip == 0:
+            return 0, resp_app, "app"
+        inn = resp_ip if resp_ip is not None else resp_app
+        return orig_ip, inn, "ip"
+
+    if orig_ip is not None or resp_ip is not None:
+        return int(orig_ip or 0), int(resp_ip or 0), "ip"
+
+    return None, None, None
+
+
 def parse_conn_line(line: str) -> Optional[dict[str, Any]]:
     text = (line or "").strip()
     if not text or text.startswith("#"):
         return None
     try:
@@ -71,37 +131,37 @@ def parse_conn_line(line: str) -> Optional[dict[str, Any]]:
     try:
         dport = int(row.get("id.resp_p") or row.get("dst_port") or 0)
     except (TypeError, ValueError):
         dport = 0
     proto = str(row.get("proto") or "tcp").strip().lower() or "tcp"
-    try:
-        orig = int(row.get("orig_bytes") or 0)
-    except (TypeError, ValueError):
-        orig = 0
-    try:
-        resp = int(row.get("resp_bytes") or 0)
-    except (TypeError, ValueError):
-        resp = 0
+    bytes_out, bytes_in, byte_layer = resolve_conn_byte_sides(row)
+    if bytes_out is None and bytes_in is None:
+        total = 0
+    else:
+        total = int(bytes_out or 0) + int(bytes_in or 0)
     ts = parse_conn_ts(row.get("ts"))
     if ts is None:
         return None
     return {
         "ts": ts,
         "src_ip": src,
         "dst_ip": dst,
         "dst_port": dport,
         "proto": proto,
-        "bytes": max(0, orig) + max(0, resp),
+        "bytes": total,
+        "bytes_out": bytes_out,
+        "bytes_in": bytes_in,
+        "byte_layer": byte_layer,
         "orig_l2_addr": str(row.get("orig_l2_addr") or "").strip(),
         "raw": row,
     }
 
 
 def aggregate_conn_records(
     records: Iterable[dict[str, Any]],
 ) -> dict[tuple[str, str, int, str, datetime], dict[str, Any]]:
-    """Bucket by (src, dst, dport, proto, hour_start); sum bytes."""
+    """Bucket by (src, dst, dport, proto, hour_start); sum bytes + out/in."""
     buckets: dict[tuple[str, str, int, str, datetime], dict[str, Any]] = {}
     for rec in records:
         hour = hour_bucket_start(rec["ts"])
         key = (rec["src_ip"], rec["dst_ip"], int(rec["dst_port"]), rec["proto"], hour)
         slot = buckets.get(key)
@@ -110,16 +170,22 @@ def aggregate_conn_records(
                 "src_ip": rec["src_ip"],
                 "dst_ip": rec["dst_ip"],
                 "dst_port": int(rec["dst_port"]),
                 "proto": rec["proto"],
                 "bytes": int(rec.get("bytes") or 0),
+                "bytes_out": rec.get("bytes_out"),
+                "bytes_in": rec.get("bytes_in"),
+                "byte_layer": rec.get("byte_layer"),
                 "observed_at": hour,
                 "orig_l2_addr": rec.get("orig_l2_addr") or "",
                 "samples": 1,
             }
         else:
             slot["bytes"] = int(slot["bytes"] or 0) + int(rec.get("bytes") or 0)
+            slot["bytes_out"] = _add_optional_int(slot.get("bytes_out"), rec.get("bytes_out"))
+            slot["bytes_in"] = _add_optional_int(slot.get("bytes_in"), rec.get("bytes_in"))
+            slot["byte_layer"] = _merge_byte_layer(slot.get("byte_layer"), rec.get("byte_layer"))
             slot["samples"] = int(slot.get("samples") or 0) + 1
             if not slot.get("orig_l2_addr") and rec.get("orig_l2_addr"):
                 slot["orig_l2_addr"] = rec["orig_l2_addr"]
     return buckets
 
@@ -286,15 +352,19 @@ def build_flow_bodies(
                 "src_ip": slot["src_ip"],
                 "dst_ip": slot["dst_ip"],
                 "dst_port": slot["dst_port"],
                 "proto": slot["proto"],
                 "bytes": slot["bytes"],
+                "bytes_out": slot.get("bytes_out"),
+                "bytes_in": slot.get("bytes_in"),
+                "byte_layer": slot.get("byte_layer"),
                 "raw": {
                     "hour_start": hour.isoformat(),
                     "samples": slot.get("samples"),
                     "orig_l2_addr": slot.get("orig_l2_addr") or "",
                     "provider": "zeek_conn",
+                    "byte_layer": slot.get("byte_layer"),
                 },
             },
             sensor_id=sensor_id,
         )
         body["observed_at"] = hour.isoformat()
@@ -310,10 +380,15 @@ def _merge_buckets(
         existing = target.get(key)
         if existing is None:
             target[key] = dict(slot)
             continue
         existing["bytes"] = int(existing.get("bytes") or 0) + int(slot.get("bytes") or 0)
+        existing["bytes_out"] = _add_optional_int(existing.get("bytes_out"), slot.get("bytes_out"))
+        existing["bytes_in"] = _add_optional_int(existing.get("bytes_in"), slot.get("bytes_in"))
+        existing["byte_layer"] = _merge_byte_layer(
+            existing.get("byte_layer"), slot.get("byte_layer")
+        )
         existing["samples"] = int(existing.get("samples") or 0) + int(slot.get("samples") or 0)
         if not existing.get("orig_l2_addr") and slot.get("orig_l2_addr"):
             existing["orig_l2_addr"] = slot["orig_l2_addr"]
 
 
diff --git a/observatory/api/app/models.py b/observatory/api/app/models.py
index 9fbe40b..95a50d2 100644
--- a/observatory/api/app/models.py
+++ b/observatory/api/app/models.py
@@ -812,9 +812,13 @@ class FlowObservation(Base):
     src_ip: Mapped[str] = mapped_column(String(45), default="")
     dst_ip: Mapped[str] = mapped_column(String(45), default="")
     dst_port: Mapped[int] = mapped_column(Integer, default=0)
     proto: Mapped[str] = mapped_column(String(16), default="")
     bytes: Mapped[int] = mapped_column(Integer, default=0)
+    # Directional volume (Wave 1a). NULL = pre-1a / unknown — never treat as 0.
+    bytes_out: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
+    bytes_in: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
+    byte_layer: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
     dst_asn: Mapped[str] = mapped_column(String(32), default="")
     dst_country: Mapped[str] = mapped_column(String(8), default="")
     observed_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
     payload: Mapped[dict] = mapped_column(JSON, default=dict)
diff --git a/observatory/api/app/alembic/versions/h8e4f5a6b7c8_flow_direction_bytes.py b/observatory/api/app/alembic/versions/h8e4f5a6b7c8_flow_direction_bytes.py
new file mode 100644
--- /dev/null
+++ b/observatory/api/app/alembic/versions/h8e4f5a6b7c8_flow_direction_bytes.py
@@ -0,0 +1,30 @@
+"""flow_observations directional bytes (Wave 1a)
+
+Revision ID: h8e4f5a6b7c8
+Revises: g7d3e4f5a6b7
+Create Date: 2026-07-22 22:30:00.000000
+"""
+from __future__ import annotations
+
+from alembic import op
+import sqlalchemy as sa
+
+
+revision = "h8e4f5a6b7c8"
+down_revision = "g7d3e4f5a6b7"
+branch_labels = None
+depends_on = None
+
+
+def upgrade() -> None:
+    with op.batch_alter_table("flow_observations") as batch_op:
+        batch_op.add_column(sa.Column("bytes_out", sa.Integer(), nullable=True))
+        batch_op.add_column(sa.Column("bytes_in", sa.Integer(), nullable=True))
+        batch_op.add_column(sa.Column("byte_layer", sa.String(length=8), nullable=True))
+
+
+def downgrade() -> None:
+    with op.batch_alter_table("flow_observations") as batch_op:
+        batch_op.drop_column("byte_layer")
+        batch_op.drop_column("bytes_in")
+        batch_op.drop_column("bytes_out")
```
