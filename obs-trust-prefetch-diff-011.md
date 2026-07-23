<!-- BLOCK-ID: OBS-TRUST-PREFETCH-DIFF-011 -->
=== TRUST DRY_RUN PREFETCH N+1 → aggregati (FASE B) ===
Data: 2026-07-23
VERSION: invariata (STOP pre-deploy)
Test: pytest test_trust_prefetch_equivalence + test_trust_backup_selective + test_v03_operational → 8 passed

Nota review: `trust.py` / `bootstrap.py` vs git HEAD includono anche §5 backup
selettivo (già live 0.10.3, non ancora commit). Scope di QUESTO cantiere:
  - `_prefetch_portal_first_last_by_mac` / `_prefetch_fdb_last_by_asset`
  - `_build_trust_plan(..., use_prefetch=True|False)` + `scan_stats`
  - log bootstrap `mode=… queries=…`
  - `tests/test_trust_prefetch_equivalence.py`

Equivalenza filtri:
- portal-evidence = lower(kind) IN PORTAL_EVIDENCE (payload inutilizzato in is_portal_evidence)
- nessuna finestra temporale (storia intera), first/last = MIN/MAX seen_at
- multi-MAC: min(firsts)/max(lasts) sui MAC dell'asset ≡ portal_rows[0]/[-1] sul merge ordinato
- asset senza MAC / senza obs: has_portal_rows=False, derived_last solo da FDB se presente
- FDB: MAX(last_fdb_at) GROUP BY asset_id ≡ ORDER BY DESC LIMIT 1

Bootstrap log: `[bootstrap] trust dry_run: Xs mode=prefetch queries=N`

diff --git a/observatory/api/app/services/trust.py b/observatory/api/app/services/trust.py
index 44c97be..1ed2bfa 100644
--- a/observatory/api/app/services/trust.py
+++ b/observatory/api/app/services/trust.py
@@ -1,10 +1,12 @@
 from __future__ import annotations
 
+from contextlib import contextmanager
 from datetime import datetime, timedelta, timezone
+from typing import Iterator
 
-from sqlalchemy import select
+from sqlalchemy import event, func, select
 from sqlalchemy.orm import Session
 
 from app.models import Asset, Event, NameProposal, Observation, SwitchPort
 from app.services.inventory import is_synthetic_fritz_name
 
@@ -139,24 +141,43 @@ def classify_asset(asset: Asset, *, now: datetime | None = None, stale_hours: in
     if asset.portal_last_seen:
         return "stale_unlocated"
     return "fritz_historical"
 
 
-def presence_state(asset: Asset, *, now: datetime | None = None, recent_hours: int = 24) -> str:
-    now = now or _utc_now()
-    if asset.portal_last_seen:
-        age = now - asset.portal_last_seen
+def _presence_from_clock(
+    *,
+    portal_last_seen: datetime | None,
+    fritz_last_seen: datetime | None,
+    has_fritz_discovery: bool,
+    now: datetime,
+    recent_hours: int = 24,
+) -> str:
+    if portal_last_seen:
+        age = now - portal_last_seen
         if age <= timedelta(hours=max(1, recent_hours)):
             return "present"
         if age <= timedelta(hours=max(2, recent_hours * 3)):
             return "recent"
         return "stale"
-    if asset.fritz_last_seen or dict((asset.meta or {}).get("discovery") or {}).get("fritz"):
+    if fritz_last_seen or has_fritz_discovery:
         return "fritz_only"
     return "unknown"
 
 
+def presence_state(asset: Asset, *, now: datetime | None = None, recent_hours: int = 24) -> str:
+    now = now or _utc_now()
+    return _presence_from_clock(
+        portal_last_seen=asset.portal_last_seen,
+        fritz_last_seen=asset.fritz_last_seen,
+        has_fritz_discovery=bool(
+            dict((asset.meta or {}).get("discovery") or {}).get("fritz")
+        ),
+        now=now,
+        recent_hours=recent_hours,
+    )
+
+
 def _asset_macs(asset: Asset) -> list[str]:
     return [interface.mac for interface in (asset.interfaces or []) if interface.mac]
 
 
 def _asset_has_current_ip(asset: Asset) -> bool:
@@ -263,100 +284,258 @@ def _empty_trust_report() -> dict[str, int]:
         "known": 0,
         "new_actionable": 0,
         "quarantine": 0,
         "stale_unlocated": 0,
         "proposals_archived": 0,
+        # Structural: trust_level / quarantine meta / hide — triggers bootstrap backup.
         "changed_assets": 0,
+        # Portal/presence only — apply without backup (BOOTSTRAP_BACKUP=auto).
+        "timestamp_refreshes": 0,
     }
 
 
-def _build_trust_plan(db: Session, *, now: datetime) -> dict:
-    """Single O(assets × observations) scan → report + apply actions."""
-    report = _empty_trust_report()
-    actions: list[dict] = []
-    for asset in db.scalars(select(Asset)).all():
-        report["assets_total"] += 1
-        portal_rows = []
-        macs = [interface.mac for interface in asset.interfaces]
-        if macs:
-            portal_rows = [
-                row
-                for row in db.scalars(
-                    select(Observation)
-                    .where(Observation.mac.in_(macs))
-                    .order_by(Observation.seen_at)
-                ).all()
-                if is_portal_evidence(row.kind, row.payload)
-            ]
-        derived_last = portal_rows[-1].seen_at if portal_rows else None
-        fdb_at = db.scalar(
-            select(SwitchPort.last_fdb_at)
-            .where(SwitchPort.asset_id == asset.id, SwitchPort.last_fdb_at.is_not(None))
-            .order_by(SwitchPort.last_fdb_at.desc())
-            .limit(1)
+def trust_needs_backup(report: dict) -> bool:
+    """True when reconcile would mutate quarantine / trust_level / archived proposals."""
+    return bool(report.get("changed_assets") or report.get("proposals_archived"))
+
+
+def trust_needs_apply(report: dict) -> bool:
+    """True when apply should run (structural and/or reconstructible timestamp refresh)."""
+    return trust_needs_backup(report) or bool(report.get("timestamp_refreshes"))
+
+
+@contextmanager
+def _count_db_queries(db: Session) -> Iterator[dict[str, int]]:
+    """Count SQL statements on this session's bind (incl. lazy-load)."""
+    bind = db.get_bind()
+    stats = {"queries": 0}
+
+    def _before(conn, cursor, statement, parameters, context, executemany):  # noqa: ANN001
+        stats["queries"] += 1
+
+    event.listen(bind, "before_cursor_execute", _before)
+    try:
+        yield stats
+    finally:
+        event.remove(bind, "before_cursor_execute", _before)
+
+
+def _prefetch_portal_first_last_by_mac(
+    db: Session,
+) -> dict[str, tuple[datetime, datetime]]:
+    """One aggregate: MIN/MAX seen_at per MAC for portal-evidence kinds.
+
+    Equivalence with the legacy loop: that loop loads all Observation rows for
+    the asset MACs ordered by seen_at, filters with ``is_portal_evidence``
+    (kind only — payload unused), then takes [0] / [-1]. Across multiple MACs
+    that is global min/max seen_at. Per-MAC MIN/MAX then min/max across the
+    asset's MAC list yields the same first/last. No temporal window in either
+    path (full history).
+    """
+    kinds = sorted(PORTAL_EVIDENCE)
+    rows = db.execute(
+        select(
+            Observation.mac,
+            func.min(Observation.seen_at),
+            func.max(Observation.seen_at),
         )
-        if fdb_at and (not derived_last or fdb_at > derived_last):
-            derived_last = fdb_at
-        if not asset.portal_last_seen and derived_last:
-            recent = derived_last >= now - timedelta(hours=24)
-            if recent:
-                bucket = (
-                    "new_actionable"
-                    if is_nuovo_actionable_asset(asset)
-                    else "confirmed_present"
+        .where(func.lower(Observation.kind).in_(kinds))
+        .group_by(Observation.mac)
+    ).all()
+    return {mac: (first, last) for mac, first, last in rows if mac is not None}
+
+
+def _prefetch_fdb_last_by_asset(db: Session) -> dict[int, datetime]:
+    """One aggregate: MAX(last_fdb_at) per asset_id (non-null only)."""
+    rows = db.execute(
+        select(SwitchPort.asset_id, func.max(SwitchPort.last_fdb_at))
+        .where(
+            SwitchPort.asset_id.is_not(None),
+            SwitchPort.last_fdb_at.is_not(None),
+        )
+        .group_by(SwitchPort.asset_id)
+    ).all()
+    return {int(asset_id): last_at for asset_id, last_at in rows if asset_id is not None}
+
+
+def _portal_extent_from_mac_index(
+    macs: list[str],
+    portal_by_mac: dict[str, tuple[datetime, datetime]],
+) -> tuple[datetime | None, datetime | None, bool]:
+    firsts: list[datetime] = []
+    lasts: list[datetime] = []
+    for mac in macs:
+        extent = portal_by_mac.get(mac)
+        if extent is None:
+            continue
+        firsts.append(extent[0])
+        lasts.append(extent[1])
+    if not firsts:
+        return None, None, False
+    return min(firsts), max(lasts), True
+
+
+def _portal_extent_nplus1(
+    db: Session, macs: list[str]
+) -> tuple[datetime | None, datetime | None, bool]:
+    """Legacy per-asset Observation scan (kept for equivalence tests)."""
+    if not macs:
+        return None, None, False
+    portal_rows = [
+        row
+        for row in db.scalars(
+            select(Observation)
+            .where(Observation.mac.in_(macs))
+            .order_by(Observation.seen_at)
+        ).all()
+        if is_portal_evidence(row.kind, row.payload)
+    ]
+    if not portal_rows:
+        return None, None, False
+    return portal_rows[0].seen_at, portal_rows[-1].seen_at, True
+
+
+def _fdb_last_nplus1(db: Session, asset_id: int) -> datetime | None:
+    return db.scalar(
+        select(SwitchPort.last_fdb_at)
+        .where(SwitchPort.asset_id == asset_id, SwitchPort.last_fdb_at.is_not(None))
+        .order_by(SwitchPort.last_fdb_at.desc())
+        .limit(1)
+    )
+
+
+def _build_trust_plan(
+    db: Session, *, now: datetime, use_prefetch: bool = True
+) -> dict:
+    """Build trust report + apply actions.
+
+    Default: 1× assets + 2× aggregates (portal-by-mac, fdb-by-asset), then a
+    pure in-memory loop. ``use_prefetch=False`` keeps the legacy ~2N Observation
+    / FDB queries for equivalence tests only.
+    """
+    with _count_db_queries(db) as qstats:
+        portal_by_mac: dict[str, tuple[datetime, datetime]] | None = None
+        fdb_by_asset: dict[int, datetime] | None = None
+        if use_prefetch:
+            portal_by_mac = _prefetch_portal_first_last_by_mac(db)
+            fdb_by_asset = _prefetch_fdb_last_by_asset(db)
+
+        report = _empty_trust_report()
+        actions: list[dict] = []
+        for asset in db.scalars(select(Asset)).all():
+            report["assets_total"] += 1
+            macs = [interface.mac for interface in asset.interfaces]
+            if use_prefetch:
+                assert portal_by_mac is not None and fdb_by_asset is not None
+                portal_first, portal_last, has_portal_rows = _portal_extent_from_mac_index(
+                    macs, portal_by_mac
                 )
+                fdb_at = fdb_by_asset.get(asset.id)
+            else:
+                portal_first, portal_last, has_portal_rows = _portal_extent_nplus1(db, macs)
+                fdb_at = _fdb_last_nplus1(db, asset.id)
+
+            derived_last = portal_last
+            if fdb_at and (not derived_last or fdb_at > derived_last):
+                derived_last = fdb_at
+            if not asset.portal_last_seen and derived_last:
+                recent = derived_last >= now - timedelta(hours=24)
+                if recent:
+                    bucket = (
+                        "new_actionable"
+                        if is_nuovo_actionable_asset(asset)
+                        else "confirmed_present"
+                    )
+                else:
+                    protected = bool(
+                        (asset.name or "").strip()
+                        or asset.status == "noto"
+                        or asset.is_critical
+                        or (asset.meta or {}).get("manual_overrides")
+                        or (asset.meta or {}).get("infrastructure_identity")
+                    )
+                    bucket = "known" if protected else "stale_unlocated"
             else:
-                protected = bool(
-                    (asset.name or "").strip()
-                    or asset.status == "noto"
-                    or asset.is_critical
-                    or (asset.meta or {}).get("manual_overrides")
-                    or (asset.meta or {}).get("infrastructure_identity")
+                bucket = operational_bucket(asset, now=now)
+            if bucket != "fritz_historical":
+                report[bucket if bucket in report else "known"] += 1
+            level = "confirmed_present" if bucket == "new_actionable" else bucket
+            expected_state = (
+                "fritz_historical"
+                if level == "fritz_historical"
+                else "stale_unlocated"
+                if level == "stale_unlocated"
+                else "active"
+            )
+            current_state = (asset.meta or {}).get("operational_state", "active")
+            # Structural = trust_level flip or quarantine/stale hide meta (operational_state).
+            structural = asset.trust_level != level or current_state != expected_state
+
+            archive_proposal_ids: list[int] = []
+            if level == "fritz_historical":
+                report["quarantine"] += 1
+                mac = asset.interfaces[0].mac if asset.interfaces else ""
+                for proposal in asset.name_proposals:
+                    weak = proposal.source == "fritz" and (
+                        is_synthetic_fritz_name(proposal.value, mac)
+                        or proposal.value.strip().lower() in {"", "unknown", "sconosciuto"}
+                    )
+                    if weak and proposal.status == "pending":
+                        report["proposals_archived"] += 1
+                        archive_proposal_ids.append(proposal.id)
+
+            portal_refresh = bool(
+                (has_portal_rows and not asset.portal_first_seen)
+                or (
+                    derived_last
+                    and (not asset.portal_last_seen or derived_last > asset.portal_last_seen)
                 )
-                bucket = "known" if protected else "stale_unlocated"
-        else:
-            bucket = operational_bucket(asset, now=now)
-        if bucket != "fritz_historical":
-            report[bucket if bucket in report else "known"] += 1
-        level = "confirmed_present" if bucket == "new_actionable" else bucket
-        expected_state = (
-            "fritz_historical"
-            if level == "fritz_historical"
-            else "stale_unlocated"
-            if level == "stale_unlocated"
-            else "active"
-        )
-        current_state = (asset.meta or {}).get("operational_state", "active")
-        if asset.trust_level != level or current_state != expected_state:
-            report["changed_assets"] += 1
+            )
+            eff_portal = asset.portal_last_seen
+            if derived_last and (not eff_portal or derived_last > eff_portal):
+                eff_portal = derived_last
+            expected_presence = _presence_from_clock(
+                portal_last_seen=eff_portal,
+                fritz_last_seen=asset.fritz_last_seen,
+                has_fritz_discovery=bool(
+                    dict((asset.meta or {}).get("discovery") or {}).get("fritz")
+                ),
+                now=now,
+            )
+            presence_refresh = (asset.presence_state or "") != expected_presence
 
-        archive_proposal_ids: list[int] = []
-        if level == "fritz_historical":
-            report["quarantine"] += 1
-            mac = asset.interfaces[0].mac if asset.interfaces else ""
-            for proposal in asset.name_proposals:
-                weak = proposal.source == "fritz" and (
-                    is_synthetic_fritz_name(proposal.value, mac)
-                    or proposal.value.strip().lower() in {"", "unknown", "sconosciuto"}
-                )
-                if weak and proposal.status == "pending":
-                    report["proposals_archived"] += 1
-                    archive_proposal_ids.append(proposal.id)
+            if structural:
+                report["changed_assets"] += 1
+            elif portal_refresh or presence_refresh:
+                report["timestamp_refreshes"] += 1
 
-        actions.append(
-            {
-                "asset_id": asset.id,
-                "level": level,
-                "expected_state": expected_state,
-                "has_portal_rows": bool(portal_rows),
-                "portal_first": portal_rows[0].seen_at if portal_rows else None,
-                "portal_last": portal_rows[-1].seen_at if portal_rows else None,
-                "derived_last": derived_last,
-                "archive_proposal_ids": archive_proposal_ids,
-            }
-        )
-    return {"report": report, "actions": actions, "now": now}
+            actions.append(
+                {
+                    "asset_id": asset.id,
+                    "level": level,
+                    "expected_state": expected_state,
+                    "has_portal_rows": has_portal_rows,
+                    "portal_first": portal_first,
+                    "portal_last": portal_last,
+                    "derived_last": derived_last,
+                    "archive_proposal_ids": archive_proposal_ids,
+                    "structural": structural,
+                    "timestamp_refresh": (not structural)
+                    and (portal_refresh or presence_refresh),
+                }
+            )
+
+        scan_stats = {
+            "mode": "prefetch" if use_prefetch else "nplus1",
+            "queries": qstats["queries"],
+        }
+    return {
+        "report": report,
+        "actions": actions,
+        "now": now,
+        "scan_stats": scan_stats,
+    }
 
 
 def _apply_trust_plan(db: Session, plan: dict, *, now: datetime) -> dict[str, int]:
     """Apply a previously built plan (no observation re-scan)."""
     actions = plan.get("actions") or []
@@ -448,31 +627,35 @@ def reconcile_trust_history(
     db: Session,
     *,
     dry_run: bool = True,
     now: datetime | None = None,
     plan: dict | None = None,
+    use_prefetch: bool = True,
 ) -> dict:
     """Reversible, idempotent quarantine of historical FRITZ-only records.
 
     Bootstrap assumption: runs single-threaded before uvicorn starts, with no
     concurrent DB writers between dry_run and apply. Reusing ``plan`` from a
-    prior dry_run is therefore safe and avoids a second O(assets × observations)
-    scan. Callers outside bootstrap that pass ``plan`` must uphold the same
+    prior dry_run is therefore safe and avoids a second observation/FDB scan.
+    Callers outside bootstrap that pass ``plan`` must uphold the same
     single-writer window.
+
+    ``use_prefetch=False`` forces the legacy per-asset N+1 scan (tests only).
     """
     now = now or _utc_now()
     if plan is not None:
         payload = plan
         if "actions" not in payload and isinstance(payload.get("plan"), dict):
             payload = payload["plan"]
         apply_now = payload.get("now") if isinstance(payload.get("now"), datetime) else now
         return _apply_trust_plan(db, payload, now=apply_now)
 
-    built = _build_trust_plan(db, now=now)
+    built = _build_trust_plan(db, now=now, use_prefetch=use_prefetch)
     if dry_run:
         report = dict(built["report"])
         report["plan"] = built
+        report["scan_stats"] = built.get("scan_stats") or {}
         return report
     return _apply_trust_plan(db, built, now=now)
 
 
 def latest_portal_observation(db: Session, asset: Asset) -> Observation | None:
diff --git a/observatory/api/app/bootstrap.py b/observatory/api/app/bootstrap.py
index 024b151..722bc13 100644
--- a/observatory/api/app/bootstrap.py
+++ b/observatory/api/app/bootstrap.py
@@ -19,11 +19,15 @@ from app.services.backup import bootstrap_should_backup, create_backup
 from app.services.identity import reconcile_known_infrastructure
 from app.services.migrate import import_legacy
 from app.services.monitoring import reconcile_existing_monitors
 from app.services.port_roles import ensure_known_span_overrides
 from app.services.schema_migrations import apply_sqlite_migrations
-from app.services.trust import reconcile_trust_history
+from app.services.trust import (
+    reconcile_trust_history,
+    trust_needs_apply,
+    trust_needs_backup,
+)
 
 
 def _step_start() -> float:
     return time.perf_counter()
 
@@ -72,10 +76,11 @@ def main() -> None:
     Path(settings.sqlite_path).parent.mkdir(parents=True, exist_ok=True)
 
     t0 = _step_start()
     engine = get_engine()
     Base.metadata.create_all(bind=engine)
+    # New tables (e.g. oui_vendors) land via create_all; column patches via apply_sqlite.
     migrated = apply_sqlite_migrations(engine)
     _step_end(1, "schema", t0)
     if migrated:
         print(f"[bootstrap] migrazione SQLite v0.4: {', '.join(migrated)}")
     SessionLocal = _session_factory()
@@ -155,27 +160,39 @@ def main() -> None:
         # Single-pass trust: dry_run builds the plan; apply reuses it (no second scan).
         # Safe because bootstrap is single-threaded pre-uvicorn (no concurrent writers).
         t0 = _step_start()
         t_sub = time.perf_counter()
         trust_preview = reconcile_trust_history(db, dry_run=True)
-        print(f"[bootstrap] trust dry_run: {time.perf_counter() - t_sub:.1f}s")
-        trust_plan = trust_preview.get("plan")
-        has_trust_changes = bool(
-            trust_preview["changed_assets"] or trust_preview["proposals_archived"]
+        dry_s = time.perf_counter() - t_sub
+        scan = trust_preview.get("scan_stats") or {}
+        print(
+            f"[bootstrap] trust dry_run: {dry_s:.1f}s "
+            f"mode={scan.get('mode', '?')} queries={scan.get('queries', '?')}"
         )
-        if has_trust_changes:
+        trust_plan = trust_preview.get("plan")
+        # Backup only for structural trust work (level/quarantine/proposals).
+        # Portal/presence refresh alone → apply without ~60s SQLite backup.
+        # BOOTSTRAP_BACKUP=always still forces backup via has_changes=False path.
+        needs_backup = trust_needs_backup(trust_preview)
+        needs_apply = trust_needs_apply(trust_preview)
+        if needs_apply:
             t_sub = time.perf_counter()
-            backup = _bootstrap_backup(db, settings, has_changes=True, reason="trust")
+            backup = _bootstrap_backup(
+                db, settings, has_changes=needs_backup, reason="trust"
+            )
             print(f"[bootstrap] trust backup: {time.perf_counter() - t_sub:.1f}s")
             t_sub = time.perf_counter()
             trust_applied = reconcile_trust_history(db, dry_run=False, plan=trust_plan)
             db.commit()
             print(f"[bootstrap] trust apply: {time.perf_counter() - t_sub:.1f}s")
+            ts_n = trust_applied.get("timestamp_refreshes", 0)
             print(
                 f"[bootstrap] trust v0.4: confermati={trust_applied['confirmed_present']} "
                 f"noti={trust_applied['known']} quarantena={trust_applied['quarantine']} "
                 f"proposte_archiviate={trust_applied['proposals_archived']} "
+                f"structural={trust_applied.get('changed_assets', 0)} "
+                f"timestamp_refresh={ts_n} "
                 f"backup={(backup or {}).get('db')}"
             )
         else:
             t_sub = time.perf_counter()
             _bootstrap_backup(db, settings, has_changes=False, reason="trust")

=== NEW FILE: observatory/tests/test_trust_prefetch_equivalence.py ===
diff --git a/observatory/tests/test_trust_prefetch_equivalence.py b/observatory/tests/test_trust_prefetch_equivalence.py
new file mode 100644
index 0000000..0d0f06f
--- /dev/null
+++ b/observatory/tests/test_trust_prefetch_equivalence.py
@@ -0,0 +1,178 @@
+"""Prefetch trust dry_run: equivalence vs legacy N+1 scan."""
+
+from __future__ import annotations
+
+import sys
+from datetime import datetime, timedelta
+from pathlib import Path
+
+from sqlalchemy import create_engine
+from sqlalchemy.orm import sessionmaker
+
+sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "api"))
+
+from app.db import Base
+from app.models import Asset, Interface, NameProposal, Observation, Switch, SwitchPort
+from app.services.trust import _build_trust_plan, reconcile_trust_history
+
+
+def _session(tmp_path):
+    engine = create_engine(f"sqlite:///{tmp_path / 'trust_prefetch.db'}")
+    Base.metadata.create_all(engine)
+    return sessionmaker(bind=engine)()
+
+
+def _action_key(action: dict) -> dict:
+    return {
+        "asset_id": action["asset_id"],
+        "level": action["level"],
+        "expected_state": action["expected_state"],
+        "has_portal_rows": action["has_portal_rows"],
+        "portal_first": action["portal_first"],
+        "portal_last": action["portal_last"],
+        "derived_last": action["derived_last"],
+        "archive_proposal_ids": list(action["archive_proposal_ids"]),
+        "structural": action["structural"],
+        "timestamp_refresh": action["timestamp_refresh"],
+    }
+
+
+def _report_key(report: dict) -> dict:
+    return {
+        k: report[k]
+        for k in (
+            "assets_total",
+            "confirmed_present",
+            "known",
+            "new_actionable",
+            "quarantine",
+            "stale_unlocated",
+            "proposals_archived",
+            "changed_assets",
+            "timestamp_refreshes",
+        )
+    }
+
+
+def test_prefetch_plan_identical_to_nplus1(tmp_path):
+    """Prefetch aggregates must match legacy per-asset Observation/FDB scans."""
+    db = _session(tmp_path)
+    now = datetime.utcnow().replace(microsecond=0)
+    t0 = now - timedelta(days=3)
+    t1 = now - timedelta(hours=6)
+    t2 = now - timedelta(hours=1)
+    t_fdb = now - timedelta(minutes=10)
+
+    # Multi-MAC: portal first on mac-A, last on mac-B; non-portal kinds ignored.
+    multi = Asset(
+        uid="multi",
+        status="noto",
+        name="MultiNIC",
+        trust_level="confirmed_present",
+        presence_state="present",
+        portal_first_seen=t0,
+        portal_last_seen=t1,
+        meta={"operational_state": "active"},
+    )
+    # Quarantine candidate + weak Fritz proposal.
+    histo = Asset(uid="histo", status="nuovo", trust_level=None, presence_state="unknown")
+    # No MAC → no portal rows.
+    bare = Asset(
+        uid="bare",
+        status="noto",
+        name="Bare",
+        trust_level="known",
+        presence_state="unknown",
+        meta={"operational_state": "active"},
+    )
+    # FDB newer than portal last.
+    fdb_asset = Asset(
+        uid="fdb",
+        status="noto",
+        name="FDBBox",
+        trust_level="confirmed_present",
+        presence_state="present",
+        portal_first_seen=t1,
+        portal_last_seen=t1,
+        meta={"operational_state": "active"},
+    )
+    db.add_all([multi, histo, bare, fdb_asset])
+    db.flush()
+
+    db.add_all(
+        [
+            Interface(asset_id=multi.id, mac="AA:BB:CC:DD:EE:01"),
+            Interface(asset_id=multi.id, mac="AA:BB:CC:DD:EE:02"),
+            Interface(asset_id=histo.id, mac="11:22:33:44:55:66"),
+            Interface(asset_id=fdb_asset.id, mac="DE:AD:BE:EF:00:01"),
+        ]
+    )
+    db.add(
+        NameProposal(
+            asset_id=histo.id,
+            source="fritz",
+            value="PC-11-22-33-44-55-66",
+            confidence=0.3,
+            status="pending",
+        )
+    )
+    db.add_all(
+        [
+            Observation(kind="icmp", mac="AA:BB:CC:DD:EE:01", seen_at=t0, payload={}),
+            Observation(kind="nmap", mac="AA:BB:CC:DD:EE:02", seen_at=t2, payload={}),
+            # Must NOT drive portal (ssdp / fritz outside PORTAL_EVIDENCE path for portal).
+            Observation(kind="ssdp", mac="AA:BB:CC:DD:EE:02", seen_at=now, payload={}),
+            Observation(kind="fritz", mac="AA:BB:CC:DD:EE:01", seen_at=now, payload={}),
+            # Uppercase kind still portal via lower().
+            Observation(kind="ICMP", mac="DE:AD:BE:EF:00:01", seen_at=t1, payload={}),
+        ]
+    )
+    sw = Switch(code="sw1", name="sw", ip="192.168.1.8")
+    db.add(sw)
+    db.flush()
+    db.add(
+        SwitchPort(
+            switch_id=sw.id,
+            number=1,
+            asset_id=fdb_asset.id,
+            last_fdb_at=t_fdb,
+            source="fdb",
+        )
+    )
+    db.flush()
+
+    legacy = _build_trust_plan(db, now=now, use_prefetch=False)
+    pref = _build_trust_plan(db, now=now, use_prefetch=True)
+
+    assert _report_key(legacy["report"]) == _report_key(pref["report"])
+    legacy_actions = sorted(
+        (_action_key(a) for a in legacy["actions"]), key=lambda a: a["asset_id"]
+    )
+    pref_actions = sorted(
+        (_action_key(a) for a in pref["actions"]), key=lambda a: a["asset_id"]
+    )
+    assert legacy_actions == pref_actions
+
+    # Multi-MAC first/last span both NICs.
+    multi_action = next(a for a in pref["actions"] if a["asset_id"] == multi.id)
+    assert multi_action["portal_first"] == t0
+    assert multi_action["portal_last"] == t2
+    assert multi_action["has_portal_rows"] is True
+
+    fdb_action = next(a for a in pref["actions"] if a["asset_id"] == fdb_asset.id)
+    assert fdb_action["derived_last"] == t_fdb
+
+    # Query budget: prefetch must beat N+1 on this fixture.
+    assert pref["scan_stats"]["mode"] == "prefetch"
+    assert legacy["scan_stats"]["mode"] == "nplus1"
+    assert pref["scan_stats"]["queries"] < legacy["scan_stats"]["queries"]
+
+
+def test_reconcile_dry_run_exposes_scan_stats(tmp_path):
+    db = _session(tmp_path)
+    db.add(Asset(uid="x", status="nuovo"))
+    db.flush()
+    preview = reconcile_trust_history(db, dry_run=True)
+    assert preview["scan_stats"]["mode"] == "prefetch"
+    assert isinstance(preview["scan_stats"]["queries"], int)
+    assert preview["scan_stats"]["queries"] >= 3
