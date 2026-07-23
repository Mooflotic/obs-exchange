<!-- BLOCK-ID: OBS-FLOW-INGEST-FIX-DIFF-009 -->

# OBS-FLOW-INGEST-FIX-DIFF-009 — non perdere ora chiusa su timeout

## Parametri scelti
- **batch N=100** → `POST /api/ingest/flows` (`{"flows":[...]}`, max 500)
- **K=3** retry falliti sulla stessa ora → DROP esplicito con log
- **M=3000** pending buckets → DROP ora chiusa più vecchia con log
- **timeout flow=120s**; observations (Fritz/nmap) post **30→60s** (stesso sintomo timed-out)

## Comportamento
1. POST fail → bucket restano, ora NON in `flushed_hours`, `hour_fail_counts++`
2. Chunk ack: rimossi dal pending solo i body POST-ati OK (no inflate su retry)
3. Success → flush ora; tetto → `[zeek_conn] DROP ora <h>: X bucket persi dopo …`

Nota share: header interno redatti come `x_obs_hdr` (guard anti-pattern sul canale).

Test: `13 passed` (`test_zeek_conn_provider`).

STOP pre-deploy.

```diff
diff --git a/observatory/api/app/routers/evolution.py b/observatory/api/app/routers/evolution.py
index 0c5b5a1..c8bacec 100644
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
 
@@ -222,56 +243,92 @@ def ingest_flow(
 ):
     """M8: authenticated normalized flow/conn ingest (feature-flagged)."""
     _check_internal(x_obs_hdr, settings)
     if not settings.flow_ingest_enabled:
         raise HTTPException(503, "flow ingest disabilitato (FLOW_INGEST_ENABLED=false)")
+    result = upsert_flow_observation(db, body, settings)
+    db.commit()
+    return result
+
+
+class FlowBatchIn(BaseModel):
+    flows: list[FlowIn] = Field(default_factory=list)
+
+
+@router.post("/ingest/flows")
+def ingest_flows(
+    body: FlowBatchIn,
+    db: Session = Depends(get_db),
+    settings: Settings = Depends(get_settings),
+    x_obs_hdr: Optional[str] = Header(default=None),
+):
+    """Batch flow ingest (one HTTP round-trip for many buckets)."""
+    _check_internal(x_obs_hdr, settings)
+    if not settings.flow_ingest_enabled:
+        raise HTTPException(503, "flow ingest disabilitato (FLOW_INGEST_ENABLED=false)")
+    flows = list(body.flows or [])
+    if len(flows) > 500:
+        raise HTTPException(400, "max 500 flows per batch")
+    results = [upsert_flow_observation(db, item, settings) for item in flows]
+    db.commit()
+    created = sum(1 for r in results if r.get("created"))
+    return {"ok": True, "count": len(results), "created": created, "results": results}
+
+
+def upsert_flow_observation(db: Session, body: FlowIn, settings: Settings) -> dict[str, Any]:
+    """Insert or add-into dedup window; caller commits."""
     observed = body.observed_at or datetime.utcnow()
     entity = f"{body.src_ip}>{body.dst_ip}:{body.dst_port}/{body.proto}"
     bucket = int(observed.timestamp() // max(1, settings.obs_dedup_window_s))
     dedup = hashlib.sha256(
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
             at=observed,
             bytes_n=int(body.bytes or 0),
             detail="Flow ingest: traffico su IP watched",
             extra={"sensor_id": body.sensor_id, "proto": body.proto, "dst_port": body.dst_port},
         )
-        db.commit()
         return {"ok": True, "created": False, "id": existing.id}
     row = FlowObservation(
         dedup_key=dedup,
         sensor_id=body.sensor_id,
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
     db.add(row)
+    db.flush()
     from app.services.watch import note_traffic_for_ips
 
     note_traffic_for_ips(
         db,
         ips=[body.src_ip, body.dst_ip],
         at=observed,
         bytes_n=int(body.bytes or 0),
         detail="Flow ingest: traffico su IP watched",
         extra={"sensor_id": body.sensor_id, "proto": body.proto, "dst_port": body.dst_port},
     )
-    db.commit()
     return {"ok": True, "created": True, "id": row.id}
 
 
 @router.post("/notifications/test")
 def test_notification(
diff --git a/observatory/collector/collector/adapters/zeek_conn.py b/observatory/collector/collector/adapters/zeek_conn.py
index 74ad49e..a45d2de 100644
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
 
@@ -189,19 +255,22 @@ def resolve_asset_by_ip_at_sqlite(
     return next(iter(candidates.keys()))
 
 
 def load_state(path: Path) -> dict[str, Any]:
     if not path.is_file():
-        return {"flushed_hours": [], "offsets": {}}
+        return {"flushed_hours": [], "offsets": {}, "hour_fail_counts": {}}
     try:
         data = json.loads(path.read_text(encoding="utf-8"))
     except (OSError, json.JSONDecodeError):
-        return {"flushed_hours": [], "offsets": {}}
+        return {"flushed_hours": [], "offsets": {}, "hour_fail_counts": {}}
     if not isinstance(data, dict):
-        return {"flushed_hours": [], "offsets": {}}
+        return {"flushed_hours": [], "offsets": {}, "hour_fail_counts": {}}
     data.setdefault("flushed_hours", [])
     data.setdefault("offsets", {})
+    data.setdefault("hour_fail_counts", {})
+    if not isinstance(data["hour_fail_counts"], dict):
+        data["hour_fail_counts"] = {}
     return data
 
 
 def save_state(
     path: Path,
@@ -212,13 +281,18 @@ def save_state(
     path.parent.mkdir(parents=True, exist_ok=True)
     flushed = list(state.get("flushed_hours") or [])[-48:]
     offsets = dict(state.get("offsets") or {})
     base = log_dir if log_dir is not None else path.parent
     offsets = {k: v for k, v in offsets.items() if (base / k).is_file()}
+    fails = dict(state.get("hour_fail_counts") or {})
+    # Keep fail counts only for hours not yet flushed.
+    flushed_set = set(flushed)
+    fails = {k: int(v) for k, v in fails.items() if k not in flushed_set and int(v) > 0}
     payload = {
         "flushed_hours": flushed,
         "offsets": offsets,
+        "hour_fail_counts": fails,
         "last_cycle_at": state.get("last_cycle_at"),
         "last_stats": dict(state.get("last_stats") or {}),
     }
     path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
 
@@ -286,15 +360,19 @@ def build_flow_bodies(
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
@@ -310,95 +388,201 @@ def _merge_buckets(
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
 
 
 def reset_pending_buckets() -> None:
     """Test helper: clear in-memory hourly state."""
     _pending_buckets.clear()
 
 
+# Batch POST size — ~700 buckets → ~7 requests instead of ~700.
+FLOW_BATCH_SIZE = 100
+# After this many failed cycles on the same closed hour → explicit DROP.
+HOUR_FAIL_MAX = 3
+# Hard cap on in-memory buckets; drop oldest closed hour(s) with log.
+PENDING_BUCKETS_MAX = 3000
+
+
+def _chunked(items: list[Any], size: int) -> list[list[Any]]:
+    n = max(1, int(size))
+    return [items[i : i + n] for i in range(0, len(items), n)]
+
+
+def _drop_hour_buckets(
+    hour: datetime,
+    *,
+    reason: str,
+    fail_counts: dict[str, int],
+) -> int:
+    """Remove all pending buckets for ``hour``; return how many were dropped."""
+    hour_key = hour.isoformat()
+    dropped = 0
+    for key in list(_pending_buckets):
+        if key[4] == hour:
+            del _pending_buckets[key]
+            dropped += 1
+    fail_counts.pop(hour_key, None)
+    print(
+        f"[zeek_conn] DROP ora {hour_key}: {dropped} bucket persi dopo {reason}",
+        flush=True,
+    )
+    return dropped
+
+
 def run_zeek_provider_cycle(
     *,
     log_dir: Path,
     sqlite_path: Path,
-    post_flow: Callable[[dict[str, Any]], Any],
+    post_flows: Optional[Callable[[list[dict[str, Any]]], Any]] = None,
+    post_flow: Optional[Callable[[dict[str, Any]], Any]] = None,
     sensor_id: str = SENSOR_ID,
     now: Optional[datetime] = None,
+    batch_size: int = FLOW_BATCH_SIZE,
+    hour_fail_max: int = HOUR_FAIL_MAX,
+    pending_buckets_max: int = PENDING_BUCKETS_MAX,
 ) -> dict[str, int]:
-    """Read new conn lines into memory; POST closed-hour aggregates via post_flow.
+    """Read new conn lines; POST closed-hour aggregates in batches.
 
-    Offsets are persisted immediately after the read so a failed POST never
-    re-ingests the same conn lines (API dedup would sum bytes). On POST
-    failure, closed-hour pending is still dropped (accept row loss).
+    On POST failure the closed-hour buckets stay pending and the hour is NOT
+    marked flushed (retry next cycle). Drop only after successful POST or the
+    explicit anti-accumulation ceiling (fail count / pending max) with a log.
     """
+    if post_flows is None and post_flow is not None:
+        def post_flows(bodies: list[dict[str, Any]]) -> Any:  # type: ignore[misc]
+            for body in bodies:
+                post_flow(body)
+            return None
+    if post_flows is None:
+        raise TypeError("post_flows or post_flow is required")
+
     now = now or _utc_now()
     state_path = log_dir / STATE_NAME
     state = load_state(state_path)
     records, offsets = iter_new_conn_lines(log_dir, dict(state.get("offsets") or {}))
     state["offsets"] = offsets
     state["last_cycle_at"] = now.isoformat() + "Z"
-    # Persist offsets + heartbeat mtime before any POST — prefer lost rows over byte inflation.
+    # Persist offsets before POST — prefer lost rows over byte inflation on re-read.
     save_state(state_path, state, log_dir=log_dir)
 
     _merge_buckets(_pending_buckets, aggregate_conn_records(records))
     flushed = set(state.get("flushed_hours") or [])
+    fail_counts: dict[str, int] = {
+        str(k): int(v) for k, v in dict(state.get("hour_fail_counts") or {}).items()
+    }
     cutoff = hour_bucket_start(now)
 
     def _resolve(ip: str, at: datetime) -> Optional[int]:
         return resolve_asset_by_ip_at_sqlite(sqlite_path, ip, at)
 
-    closed: dict[tuple[str, str, int, str, datetime], dict[str, Any]] = {}
-    for key, slot in list(_pending_buckets.items()):
-        hour = key[4]
-        hour_key = hour.isoformat()
-        if hour >= cutoff:
-            continue
+    # Discard already-flushed hours still lingering in memory.
+    for key in list(_pending_buckets):
+        hour_key = key[4].isoformat()
         if hour_key in flushed:
             del _pending_buckets[key]
-            continue
-        closed[key] = slot
 
-    bodies = build_flow_bodies(
-        closed,
-        resolve=_resolve,
-        sensor_id=sensor_id,
-        closed_before=cutoff,
-    )
-    skipped = len(closed) - len(bodies)
+    # Ceiling: drop oldest closed hours while over pending max.
+    dropped_ceiling = 0
+    while len(_pending_buckets) > pending_buckets_max:
+        closed_hours = sorted(
+            {key[4] for key in _pending_buckets if key[4] < cutoff}
+        )
+        if not closed_hours:
+            break
+        oldest = closed_hours[0]
+        dropped_ceiling += _drop_hour_buckets(
+            oldest,
+            reason=f"pending>{pending_buckets_max}",
+            fail_counts=fail_counts,
+        )
+        flushed.add(oldest.isoformat())
+
+    closed_hours = sorted({key[4] for key in _pending_buckets if key[4] < cutoff})
     posted = 0
+    skipped = 0
     post_error: Optional[BaseException] = None
-    try:
-        for body in bodies:
-            post_flow(body)
-            posted += 1
-    except BaseException as exc:  # noqa: BLE001 — recorded; closed hour still dropped
-        post_error = exc
-    finally:
-        # Drop closed buckets even on failure (no retry → no API byte sum inflate).
-        hours_done = {key[4].isoformat() for key in closed}
-        for key in list(closed):
-            _pending_buckets.pop(key, None)
-        flushed.update(hours_done)
-        state["flushed_hours"] = sorted(flushed)[-48:]
-        state["last_cycle_at"] = now.isoformat() + "Z"
-        state["last_stats"] = {
-            "records_read": len(records),
-            "buckets_pending": len(_pending_buckets),
-            "posted": posted,
-            "skipped_unresolved": skipped,
+
+    for hour in closed_hours:
+        hour_key = hour.isoformat()
+        hour_slots = {
+            key: slot for key, slot in _pending_buckets.items() if key[4] == hour
         }
-        save_state(state_path, state, log_dir=log_dir)
+        bodies = build_flow_bodies(
+            hour_slots,
+            resolve=_resolve,
+            sensor_id=sensor_id,
+            closed_before=cutoff,
+        )
+        skipped += len(hour_slots) - len(bodies)
+        # Unresolved-only hour: nothing to post — flush empty.
+        if not bodies:
+            for key in list(hour_slots):
+                _pending_buckets.pop(key, None)
+            flushed.add(hour_key)
+            fail_counts.pop(hour_key, None)
+            continue
+        try:
+            for chunk in _chunked(bodies, batch_size):
+                post_flows(chunk)
+                posted += len(chunk)
+                # Ack only what the API accepted — safe retry of the remainder.
+                for body in chunk:
+                    key = (
+                        str(body.get("src_ip") or ""),
+                        str(body.get("dst_ip") or ""),
+                        int(body.get("dst_port") or 0),
+                        str(body.get("proto") or "tcp"),
+                        hour,
+                    )
+                    _pending_buckets.pop(key, None)
+        except BaseException as exc:  # noqa: BLE001
+            post_error = exc
+            fails = int(fail_counts.get(hour_key) or 0) + 1
+            fail_counts[hour_key] = fails
+            if fails >= hour_fail_max:
+                _drop_hour_buckets(
+                    hour,
+                    reason=f"{fails} retry",
+                    fail_counts=fail_counts,
+                )
+                flushed.add(hour_key)
+            # Keep remaining hours for a later cycle; stop this cycle.
+            break
+        else:
+            # All chunks ok — drop unresolved leftovers for this hour.
+            for key in list(hour_slots):
+                _pending_buckets.pop(key, None)
+            flushed.add(hour_key)
+            fail_counts.pop(hour_key, None)
+
+    state["flushed_hours"] = sorted(flushed)[-48:]
+    state["hour_fail_counts"] = fail_counts
+    state["last_cycle_at"] = now.isoformat() + "Z"
+    state["last_stats"] = {
+        "records_read": len(records),
+        "buckets_pending": len(_pending_buckets),
+        "posted": posted,
+        "skipped_unresolved": skipped,
+        "dropped_ceiling": dropped_ceiling,
+        "hour_fail_counts": dict(fail_counts),
+    }
+    save_state(state_path, state, log_dir=log_dir)
 
     if post_error is not None:
         raise post_error
     return {
         "records_read": len(records),
         "buckets_pending": len(_pending_buckets),
         "posted": posted,
         "skipped_unresolved": skipped,
+        "dropped_ceiling": dropped_ceiling,
     }
diff --git a/observatory/collector/collector/main.py b/observatory/collector/collector/main.py
index 214978a..b743ef2 100644
--- a/observatory/collector/collector/main.py
+++ b/observatory/collector/collector/main.py
@@ -499,37 +499,38 @@ def _run_retention(settings: Settings) -> None:
     except Exception as exc:  # noqa: BLE001
         print(f"[collector] retention err: {exc}")
 
 
 def _run_zeek_provider(settings: Settings) -> None:
-    """Optional SPAN conn.log → hourly POST /api/ingest/flow (flag off by default)."""
+    """Optional SPAN conn.log → hourly POST /api/ingest/flows (flag off by default)."""
     if not getattr(settings, "zeek_provider_enabled", False):
         return
     api = settings.api_internal.rstrip("/")
     log_dir = Path(getattr(settings, "zeek_log_dir", "/data/zeek"))
     sqlite_path = Path(
         os.environ.get("SQLITE_PATH")
         or getattr(settings, "sqlite_path", "/data/db/observatory.db")
     )
 
-    def _post(body: dict) -> None:
-        with httpx.Client(timeout=30.0) as client:
+    def _post_flows(bodies: list[dict]) -> None:
+        # 120s: one batch ≤100 rows; sequential /ingest/flow at 30s was the outage.
+        with httpx.Client(timeout=120.0) as client:
             response = client.post(
-                f"{api}/api/ingest/flow",
+                f"{api}/api/ingest/flows",
                 headers=headers(settings),
-                json=body,
+                json={"flows": bodies},
             )
             if response.status_code >= 400:
                 raise RuntimeError(
-                    f"flow ingest {response.status_code}: {response.text[:200]}"
+                    f"flow ingest batch {response.status_code}: {response.text[:200]}"
                 )
 
     try:
         stats = run_zeek_provider_cycle(
             log_dir=log_dir,
             sqlite_path=sqlite_path,
-            post_flow=_post,
+            post_flows=_post_flows,
         )
         print(
             f"[collector] zeek_conn read={stats.get('records_read')} "
             f"pending={stats.get('buckets_pending')} "
             f"posted={stats.get('posted')} "
diff --git a/observatory/collector/collector/providers/base.py b/observatory/collector/collector/providers/base.py
index b4a1455..352dac2 100644
--- a/observatory/collector/collector/providers/base.py
+++ b/observatory/collector/collector/providers/base.py
@@ -158,9 +158,9 @@ def post_provider_result(
         "mark_missing": bool(mark_missing),
     }
     if wlan_associations:
         payload["wlan_associations"] = wlan_associations
     response = client.post(
-        f"{api_base}/api/ingest/observations", json=payload, headers=headers, timeout=30
+        f"{api_base}/api/ingest/observations", json=payload, headers=headers, timeout=60
     )
     response.raise_for_status()
     return response.json()
diff --git a/observatory/tests/test_zeek_conn_provider.py b/observatory/tests/test_zeek_conn_provider.py
index a51ae9e..8db8515 100644
--- a/observatory/tests/test_zeek_conn_provider.py
+++ b/observatory/tests/test_zeek_conn_provider.py
@@ -72,26 +72,125 @@ def test_parse_and_aggregate_hourly():
             }
         ),
     ]
     records = [parse_conn_line(line) for line in lines]
     assert all(records)
+    assert records[0]["bytes_out"] == 100
+    assert records[0]["bytes_in"] == 50
+    assert records[0]["byte_layer"] == "app"
     buckets = aggregate_conn_records(records)
     assert len(buckets) == 2
     key14 = ("10.0.0.1", "8.8.8.8", 443, "tcp", hour_bucket_start(t0))
     assert buckets[key14]["bytes"] == 200
+    assert buckets[key14]["bytes_out"] == 120
+    assert buckets[key14]["bytes_in"] == 80
+    assert buckets[key14]["byte_layer"] == "app"
     assert buckets[key14]["samples"] == 2
 
 
+def test_parse_conn_null_app_falls_back_to_ip_bytes():
+    ts = _utc_ts(datetime(2026, 7, 21, 14, 10, 0))
+    line = json.dumps(
+        {
+            "ts": ts,
+            "id.orig_h": "10.0.0.1",
+            "id.resp_h": "8.8.8.8",
+            "id.resp_p": 443,
+            "proto": "tcp",
+            "orig_bytes": None,
+            "resp_bytes": None,
+            "orig_ip_bytes": 1500,
+            "resp_ip_bytes": 800,
+        }
+    )
+    rec = parse_conn_line(line)
+    assert rec is not None
+    assert rec["bytes_out"] == 1500
+    assert rec["bytes_in"] == 800
+    assert rec["bytes"] == 2300
+    assert rec["byte_layer"] == "ip"
+
+
+def test_parse_conn_one_side_null_one_way_stays_app():
+    """resp_bytes null + no reverse IP traffic → treat as one-way (in=0), layer=app."""
+    ts = _utc_ts(datetime(2026, 7, 21, 14, 10, 0))
+    line = json.dumps(
+        {
+            "ts": ts,
+            "id.orig_h": "10.0.0.1",
+            "id.resp_h": "8.8.8.8",
+            "id.resp_p": 443,
+            "proto": "tcp",
+            "orig_bytes": 42,
+            "resp_bytes": None,
+            "orig_ip_bytes": 60,
+            "resp_ip_bytes": 0,
+        }
+    )
+    rec = parse_conn_line(line)
+    assert rec is not None
+    assert rec["bytes_out"] == 42
+    assert rec["bytes_in"] == 0
+    assert rec["byte_layer"] == "app"
+
+
+def test_parse_conn_one_side_null_with_reverse_ip_uses_ip_layer():
+    """resp_bytes null but resp_ip_bytes>0 → not silent 0; use IP-bytes."""
+    ts = _utc_ts(datetime(2026, 7, 21, 14, 10, 0))
+    line = json.dumps(
+        {
+            "ts": ts,
+            "id.orig_h": "10.0.0.1",
+            "id.resp_h": "8.8.8.8",
+            "id.resp_p": 443,
+            "proto": "tcp",
+            "orig_bytes": 100,
+            "resp_bytes": None,
+            "orig_ip_bytes": 120,
+            "resp_ip_bytes": 900,
+        }
+    )
+    rec = parse_conn_line(line)
+    assert rec is not None
+    assert rec["bytes_out"] == 120
+    assert rec["bytes_in"] == 900
+    assert rec["byte_layer"] == "ip"
+
+
+def test_parse_conn_both_null_no_ip_keeps_direction_unknown():
+    ts = _utc_ts(datetime(2026, 7, 21, 14, 10, 0))
+    line = json.dumps(
+        {
+            "ts": ts,
+            "id.orig_h": "10.0.0.1",
+            "id.resp_h": "8.8.8.8",
+            "id.resp_p": 443,
+            "proto": "tcp",
+            "orig_bytes": None,
+            "resp_bytes": None,
+        }
+    )
+    rec = parse_conn_line(line)
+    assert rec is not None
+    assert rec["bytes_out"] is None
+    assert rec["bytes_in"] is None
+    assert rec["byte_layer"] is None
+    assert rec["bytes"] == 0
+
+
 def test_build_flow_bodies_skips_unresolved_and_open_hour():
     hour = datetime(2026, 7, 21, 14, 0, 0)
     buckets = {
         ("10.0.0.1", "8.8.8.8", 443, "tcp", hour): {
             "src_ip": "10.0.0.1",
             "dst_ip": "8.8.8.8",
             "dst_port": 443,
             "proto": "tcp",
             "bytes": 90,
+            "bytes_out": 60,
+            "bytes_in": 30,
+            "byte_layer": "app",
             "observed_at": hour,
             "samples": 1,
         },
         ("10.0.0.99", "8.8.8.8", 443, "tcp", hour): {
             "src_ip": "10.0.0.99",
@@ -113,10 +212,13 @@ def test_build_flow_bodies_skips_unresolved_and_open_hour():
         closed_before=datetime(2026, 7, 21, 15, 0, 0),
     )
     assert len(bodies) == 1
     assert bodies[0]["src_ip"] == "10.0.0.1"
     assert bodies[0]["bytes"] == 90
+    assert bodies[0]["bytes_out"] == 60
+    assert bodies[0]["bytes_in"] == 30
+    assert bodies[0]["byte_layer"] == "app"
     assert bodies[0]["observed_at"] == hour.isoformat()
 
 
 def test_provider_cycle_posts_closed_hour_only(tmp_path):
     reset_pending_buckets()
@@ -135,19 +237,22 @@ def test_provider_cycle_posts_closed_hour_only(tmp_path):
         }
     )
     (log_dir / "conn.log").write_text(line + "\n", encoding="utf-8")
     posted: list[dict] = []
 
+    def post_flows(bodies: list[dict]) -> None:
+        posted.extend(bodies)
+
     import collector.adapters.zeek_conn as zc
 
     original = zc.resolve_asset_by_ip_at_sqlite
     zc.resolve_asset_by_ip_at_sqlite = lambda db_path, ip, observed_at: 7
     try:
         stats = run_zeek_provider_cycle(
             log_dir=log_dir,
             sqlite_path=tmp_path / "missing.db",
-            post_flow=posted.append,
+            post_flows=post_flows,
             now=datetime(2026, 7, 21, 15, 5, 0),
         )
     finally:
         zc.resolve_asset_by_ip_at_sqlite = original
         reset_pending_buckets()
@@ -155,12 +260,12 @@ def test_provider_cycle_posts_closed_hour_only(tmp_path):
     assert stats["posted"] == 1
     assert posted[0]["observed_at"] == "2026-07-21T14:00:00"
     assert posted[0]["bytes"] == 11
 
 
-def test_post_fail_mid_cycle_does_not_inflate_bytes(tmp_path):
-    """Offsets saved before POST; failed cycle must not re-merge conn lines."""
+def test_post_fail_keeps_pending_and_retries(tmp_path, capsys):
+    """On POST failure: buckets stay, hour not flushed; next cycle retries."""
     reset_pending_buckets()
     log_dir = tmp_path / "zeek"
     log_dir.mkdir()
     closed = datetime(2026, 7, 21, 14, 30, 0)
     lines = [
@@ -187,46 +292,144 @@ def test_post_fail_mid_cycle_does_not_inflate_bytes(tmp_path):
             }
         ),
     ]
     (log_dir / "conn.log").write_text("\n".join(lines) + "\n", encoding="utf-8")
 
-    posted: list[dict] = []
-
-    def post_fail_mid(body: dict) -> None:
-        posted.append(dict(body))
-        if len(posted) >= 2:
-            raise RuntimeError("boom")
-
     import collector.adapters.zeek_conn as zc
 
     original = zc.resolve_asset_by_ip_at_sqlite
     zc.resolve_asset_by_ip_at_sqlite = lambda db_path, ip, observed_at: 7
     try:
         with pytest.raises(RuntimeError, match="boom"):
             run_zeek_provider_cycle(
                 log_dir=log_dir,
                 sqlite_path=tmp_path / "missing.db",
-                post_flow=post_fail_mid,
+                post_flows=lambda bodies: (_ for _ in ()).throw(RuntimeError("boom")),
                 now=datetime(2026, 7, 21, 15, 5, 0),
             )
-        first_total = sum(int(p["bytes"]) for p in posted)
-        assert first_total == 150
+        state = json.loads((log_dir / "zeek_provider_state.json").read_text())
+        assert "2026-07-21T14:00:00" not in state["flushed_hours"]
+        assert state["hour_fail_counts"].get("2026-07-21T14:00:00") == 1
+        assert len(zc._pending_buckets) == 2
 
-        posted_again: list[dict] = []
+        posted: list[dict] = []
         stats = run_zeek_provider_cycle(
             log_dir=log_dir,
             sqlite_path=tmp_path / "missing.db",
-            post_flow=posted_again.append,
+            post_flows=lambda bodies: posted.extend(bodies),
             now=datetime(2026, 7, 21, 15, 5, 0),
         )
         assert stats["records_read"] == 0
-        assert posted_again == []
-        # No second POST → bytes cannot double via API dedup sum.
+        assert stats["posted"] == 2
         assert sum(int(p["bytes"]) for p in posted) == 150
+        state2 = json.loads((log_dir / "zeek_provider_state.json").read_text())
+        assert "2026-07-21T14:00:00" in state2["flushed_hours"]
+        assert not state2.get("hour_fail_counts")
+    finally:
+        zc.resolve_asset_by_ip_at_sqlite = original
+        reset_pending_buckets()
+
+
+def test_hour_fail_ceiling_drops_with_explicit_log(tmp_path, capsys):
+    reset_pending_buckets()
+    log_dir = tmp_path / "zeek"
+    log_dir.mkdir()
+    closed = datetime(2026, 7, 21, 14, 30, 0)
+    line = json.dumps(
+        {
+            "ts": _utc_ts(closed),
+            "id.orig_h": "10.0.0.1",
+            "id.resp_h": "8.8.8.8",
+            "id.resp_p": 443,
+            "proto": "tcp",
+            "orig_bytes": 11,
+            "resp_bytes": 0,
+        }
+    )
+    (log_dir / "conn.log").write_text(line + "\n", encoding="utf-8")
+
+    import collector.adapters.zeek_conn as zc
+
+    original = zc.resolve_asset_by_ip_at_sqlite
+    zc.resolve_asset_by_ip_at_sqlite = lambda db_path, ip, observed_at: 7
+
+    def always_fail(bodies):
+        raise RuntimeError("timeout")
+
+    try:
+        for _ in range(2):
+            with pytest.raises(RuntimeError):
+                run_zeek_provider_cycle(
+                    log_dir=log_dir,
+                    sqlite_path=tmp_path / "missing.db",
+                    post_flows=always_fail,
+                    now=datetime(2026, 7, 21, 15, 5, 0),
+                    hour_fail_max=3,
+                )
+        assert len(zc._pending_buckets) == 1
+        with pytest.raises(RuntimeError):
+            run_zeek_provider_cycle(
+                log_dir=log_dir,
+                sqlite_path=tmp_path / "missing.db",
+                post_flows=always_fail,
+                now=datetime(2026, 7, 21, 15, 5, 0),
+                hour_fail_max=3,
+            )
+        assert len(zc._pending_buckets) == 0
+        state = json.loads((log_dir / "zeek_provider_state.json").read_text())
+        assert "2026-07-21T14:00:00" in state["flushed_hours"]
+        out = capsys.readouterr().out
+        assert "DROP ora 2026-07-21T14:00:00" in out
+        assert "3 retry" in out
+    finally:
+        zc.resolve_asset_by_ip_at_sqlite = original
+        reset_pending_buckets()
+
+
+def test_post_flows_batches(tmp_path):
+    reset_pending_buckets()
+    log_dir = tmp_path / "zeek"
+    log_dir.mkdir()
+    closed = datetime(2026, 7, 21, 14, 10, 0)
+    lines = []
+    for i in range(5):
+        lines.append(
+            json.dumps(
+                {
+                    "ts": _utc_ts(closed),
+                    "id.orig_h": f"10.0.0.{i+1}",
+                    "id.resp_h": "8.8.8.8",
+                    "id.resp_p": 443,
+                    "proto": "tcp",
+                    "orig_bytes": 10,
+                    "resp_bytes": 0,
+                }
+            )
+        )
+    (log_dir / "conn.log").write_text("\n".join(lines) + "\n", encoding="utf-8")
+    batches: list[int] = []
+
+    def post_flows(bodies: list[dict]) -> None:
+        batches.append(len(bodies))
+
+    import collector.adapters.zeek_conn as zc
+
+    original = zc.resolve_asset_by_ip_at_sqlite
+    zc.resolve_asset_by_ip_at_sqlite = lambda db_path, ip, observed_at: 7
+    try:
+        stats = run_zeek_provider_cycle(
+            log_dir=log_dir,
+            sqlite_path=tmp_path / "missing.db",
+            post_flows=post_flows,
+            now=datetime(2026, 7, 21, 15, 0, 0),
+            batch_size=2,
+        )
     finally:
         zc.resolve_asset_by_ip_at_sqlite = original
         reset_pending_buckets()
+    assert stats["posted"] == 5
+    assert batches == [2, 2, 1]
 
 
 def test_save_state_prunes_missing_offset_files(tmp_path):
     from collector.adapters.zeek_conn import save_state
 
```
