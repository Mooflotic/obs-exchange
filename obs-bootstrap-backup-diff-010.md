<!-- BLOCK-ID: OBS-BOOTSTRAP-BACKUP-DIFF-010 -->
=== BOOTSTRAP velocità — chiusura debito ===
Data: 2026-07-23
Scope review:
  1. start_period api 20s → 180s (compose) — zero rischio
  2. §5 backup trust selettivo (structural vs timestamp)
  3. FASE A dry_run N+1 (doc only — no prefetch)
VERSION: invariata (bump solo al deploy)
Test: pytest test_trust_backup_selective + test_v03_operational → 6 passed

Nota: altre hunk sporche in docker-compose.yml (.sock/privileged 0.9.10)
NON fanno parte di questo cantiere — sotto solo start_period.

diff --git a/observatory/docker-compose.yml b/observatory/docker-compose.yml
--- a/observatory/docker-compose.yml
+++ b/observatory/docker-compose.yml
@@ -44,7 +44,7 @@ services:
       interval: 30s
       timeout: 5s
       retries: 5
-      start_period: 20s
+      start_period: 180s
diff --git a/observatory/api/app/bootstrap.py b/observatory/api/app/bootstrap.py
index 024b151..9c6cdb8 100644
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
@@ -157,25 +162,32 @@ def main() -> None:
         t0 = _step_start()
         t_sub = time.perf_counter()
         trust_preview = reconcile_trust_history(db, dry_run=True)
         print(f"[bootstrap] trust dry_run: {time.perf_counter() - t_sub:.1f}s")
         trust_plan = trust_preview.get("plan")
-        has_trust_changes = bool(
-            trust_preview["changed_assets"] or trust_preview["proposals_archived"]
-        )
-        if has_trust_changes:
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
diff --git a/observatory/api/app/services/trust.py b/observatory/api/app/services/trust.py
index 44c97be..5dcc985 100644
--- a/observatory/api/app/services/trust.py
+++ b/observatory/api/app/services/trust.py
@@ -139,24 +139,43 @@ def classify_asset(asset: Asset, *, now: datetime | None = None, stale_hours: in
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
@@ -263,33 +282,53 @@ def _empty_trust_report() -> dict[str, int]:
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
 def _build_trust_plan(db: Session, *, now: datetime) -> dict:
-    """Single O(assets × observations) scan → report + apply actions."""
+    """Single O(assets × observations) scan → report + apply actions.
+
+    Per-asset DB cost today (N+1 — see docs/fase-a-trust-dryrun-nplus1):
+    1× SELECT all assets, then for each asset with MACs: 1× Observation scan
+    + 1× SwitchPort.last_fdb_at → ~2N queries beyond the asset load.
+    """
     report = _empty_trust_report()
     actions: list[dict] = []
     for asset in db.scalars(select(Asset)).all():
         report["assets_total"] += 1
         portal_rows = []
         macs = [interface.mac for interface in asset.interfaces]
         if macs:
+            # N+1: one Observation query per asset (not a single prefetch).
             portal_rows = [
                 row
                 for row in db.scalars(
                     select(Observation)
                     .where(Observation.mac.in_(macs))
                     .order_by(Observation.seen_at)
                 ).all()
                 if is_portal_evidence(row.kind, row.payload)
             ]
         derived_last = portal_rows[-1].seen_at if portal_rows else None
+        # N+1: one FDB max query per asset.
         fdb_at = db.scalar(
             select(SwitchPort.last_fdb_at)
             .where(SwitchPort.asset_id == asset.id, SwitchPort.last_fdb_at.is_not(None))
             .order_by(SwitchPort.last_fdb_at.desc())
             .limit(1)
@@ -324,12 +363,12 @@ def _build_trust_plan(db: Session, *, now: datetime) -> dict:
             else "stale_unlocated"
             if level == "stale_unlocated"
             else "active"
         )
         current_state = (asset.meta or {}).get("operational_state", "active")
-        if asset.trust_level != level or current_state != expected_state:
-            report["changed_assets"] += 1
+        # Structural = trust_level flip or quarantine/stale hide meta (operational_state).
+        structural = asset.trust_level != level or current_state != expected_state
 
         archive_proposal_ids: list[int] = []
         if level == "fritz_historical":
             report["quarantine"] += 1
             mac = asset.interfaces[0].mac if asset.interfaces else ""
@@ -340,20 +379,48 @@ def _build_trust_plan(db: Session, *, now: datetime) -> dict:
                 )
                 if weak and proposal.status == "pending":
                     report["proposals_archived"] += 1
                     archive_proposal_ids.append(proposal.id)
 
+        portal_refresh = bool(
+            (portal_rows and not asset.portal_first_seen)
+            or (
+                derived_last
+                and (not asset.portal_last_seen or derived_last > asset.portal_last_seen)
+            )
+        )
+        eff_portal = asset.portal_last_seen
+        if derived_last and (not eff_portal or derived_last > eff_portal):
+            eff_portal = derived_last
+        expected_presence = _presence_from_clock(
+            portal_last_seen=eff_portal,
+            fritz_last_seen=asset.fritz_last_seen,
+            has_fritz_discovery=bool(
+                dict((asset.meta or {}).get("discovery") or {}).get("fritz")
+            ),
+            now=now,
+        )
+        presence_refresh = (asset.presence_state or "") != expected_presence
+
+        if structural:
+            report["changed_assets"] += 1
+        elif portal_refresh or presence_refresh:
+            report["timestamp_refreshes"] += 1
+
         actions.append(
             {
                 "asset_id": asset.id,
                 "level": level,
                 "expected_state": expected_state,
                 "has_portal_rows": bool(portal_rows),
                 "portal_first": portal_rows[0].seen_at if portal_rows else None,
                 "portal_last": portal_rows[-1].seen_at if portal_rows else None,
                 "derived_last": derived_last,
                 "archive_proposal_ids": archive_proposal_ids,
+                "structural": structural,
+                "timestamp_refresh": (not structural)
+                and (portal_refresh or presence_refresh),
             }
         )
     return {"report": report, "actions": actions, "now": now}
 
 
diff --git a/observatory/.env.example b/observatory/.env.example
--- a/observatory/.env.example
+++ b/observatory/.env.example
@@
-# Bootstrap: auto = backup solo se trust/infra/monitor cambiano; always|never.
+# Bootstrap: auto = backup solo su cambi strutturali (trust_level / quarantine /
+# proposte archiviate / infra / monitor). Refresh soli portal_last_seen /
+# presence_state NON triggerano backup trust. always|never = scappatoie.
 BOOTSTRAP_BACKUP=auto

=== NEW FILE: observatory/tests/test_trust_backup_selective.py ===
diff --git a/observatory/tests/test_trust_backup_selective.py b/observatory/tests/test_trust_backup_selective.py
new file mode 100644
index 0000000..5b56dfb
--- /dev/null
+++ b/observatory/tests/test_trust_backup_selective.py
@@ -0,0 +1,101 @@
+"""§5 backup trust selettivo: structural vs timestamp-only refresh."""
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
+from app.models import Asset, Interface, Observation
+from app.services.trust import (  # noqa: E402
+    reconcile_trust_history,
+    trust_needs_apply,
+    trust_needs_backup,
+)
+
+
+def _session(tmp_path):
+    engine = create_engine(f"sqlite:///{tmp_path / 'trust_sel.db'}")
+    Base.metadata.create_all(engine)
+    return sessionmaker(bind=engine)()
+
+
+def test_trust_needs_backup_helpers():
+    assert trust_needs_backup({"changed_assets": 0, "proposals_archived": 0}) is False
+    assert trust_needs_backup({"changed_assets": 1, "proposals_archived": 0}) is True
+    assert trust_needs_backup({"changed_assets": 0, "proposals_archived": 2}) is True
+    assert trust_needs_apply({"changed_assets": 0, "proposals_archived": 0, "timestamp_refreshes": 0}) is False
+    assert trust_needs_apply({"changed_assets": 0, "proposals_archived": 0, "timestamp_refreshes": 3}) is True
+    assert trust_needs_apply({"changed_assets": 1, "proposals_archived": 0, "timestamp_refreshes": 0}) is True
+
+
+def test_portal_bump_alone_is_timestamp_not_backup(tmp_path):
+    """Newer portal Observation bumps portal_last_seen without trust_level flip → no backup."""
+    db = _session(tmp_path)
+    now = datetime.utcnow().replace(microsecond=0)
+    old = now - timedelta(hours=2)
+    newer = now - timedelta(minutes=5)
+    asset = Asset(
+        uid="portal-bump",
+        status="noto",
+        name="NAS",
+        trust_level="confirmed_present",
+        presence_state="present",
+        portal_first_seen=old,
+        portal_last_seen=old,
+        meta={"operational_state": "active"},
+    )
+    db.add(asset)
+    db.flush()
+    db.add(Interface(asset_id=asset.id, mac="AA:BB:CC:DD:EE:01"))
+    db.add(
+        Observation(
+            kind="icmp",
+            mac="AA:BB:CC:DD:EE:01",
+            seen_at=newer,
+            payload={},
+        )
+    )
+    db.flush()
+
+    preview = reconcile_trust_history(db, dry_run=True, now=now)
+    assert preview["changed_assets"] == 0
+    assert preview["proposals_archived"] == 0
+    assert preview["timestamp_refreshes"] == 1
+    assert trust_needs_backup(preview) is False
+    assert trust_needs_apply(preview) is True
+
+    reconcile_trust_history(db, dry_run=False, plan=preview["plan"], now=now)
+    db.commit()
+    db.refresh(asset)
+    assert asset.portal_last_seen == newer
+    assert asset.trust_level == "confirmed_present"
+
+
+def test_trust_level_flip_is_structural(tmp_path):
+    db = _session(tmp_path)
+    now = datetime.utcnow().replace(microsecond=0)
+    asset = Asset(
+        uid="histo",
+        status="nuovo",
+        trust_level="confirmed_present",
+        presence_state="stale",
+        portal_first_seen=now - timedelta(days=10),
+        portal_last_seen=now - timedelta(days=5),
+        meta={"operational_state": "active"},
+    )
+    db.add(asset)
+    db.flush()
+    db.add(Interface(asset_id=asset.id, mac="AA:BB:CC:DD:EE:02"))
+    db.flush()
+
+    preview = reconcile_trust_history(db, dry_run=True, now=now)
+    assert preview["changed_assets"] >= 1
+    assert preview["timestamp_refreshes"] == 0
+    assert trust_needs_backup(preview) is True

=== NEW FILE: observatory/docs/fase-a-trust-dryrun-nplus1-20260723.txt ===
diff --git a/observatory/docs/fase-a-trust-dryrun-nplus1-20260723.txt b/observatory/docs/fase-a-trust-dryrun-nplus1-20260723.txt
new file mode 100644
index 0000000..6a938e6
--- /dev/null
+++ b/observatory/docs/fase-a-trust-dryrun-nplus1-20260723.txt
@@ -0,0 +1,62 @@
+FASE A — trust dry_run N+1 (sola lettura / conteggio query)
+Data: 2026-07-23
+Scope: analisi. NESSUN prefetch implementato in questa fase.
+
+Contesto misurato (0.9.6): trust dry_run ~28.9s su boot Cassiopea.
+
+========================================================================
+1. LOOP
+========================================================================
+
+File: observatory/api/app/services/trust.py → _build_trust_plan
+
+  1×  SELECT Asset (tutti)
+  for asset in assets:                          # N = assets_total
+      if macs:
+          1× SELECT Observation
+               WHERE mac IN (macs asset)
+               ORDER BY seen_at
+               + filtro Python is_portal_evidence
+      1× SELECT SwitchPort.last_fdb_at
+               WHERE asset_id = ? AND last_fdb_at IS NOT NULL
+               ORDER BY last_fdb_at DESC LIMIT 1
+      # classificazione bucket / trust_level in-process (0 query)
+
+Apply (_apply_trust_plan), se riusa plan: 1× Asset IN (…) + eventuale
+NameProposal IN (…) — non ri-scansiona observations.
+
+========================================================================
+2. CONTEGGIO QUERY (stima)
+========================================================================
+
+  Q_assets = 1
+  Q_obs    = N_con_mac          (tipicamente ≈ N)
+  Q_fdb    = N                  (sempre, anche senza MAC)
+  Totale dry_run ≈ 1 + N_con_mac + N  ≈ 2N + 1
+
+Esempio N=150 → ~301 query round-trip SQLite.
+Il commento nel codice parlava già di O(assets × observations): il costo
+dominante non è solo il numero di query, ma ogni Observation scan che
+rilegge (e filtra in Python) tutte le righe per quei MAC — su DB grandi
+ogni query può essere pesante.
+
+Single-pass bootstrap (0.9.5): dry_run costruisce plan, apply lo riusa
+→ niente secondo giro 2N. I ~29s restano sul dry_run.
+
+========================================================================
+3. PREFETCH (FASE B — NON ora)
+========================================================================
+
+Sostituire il loop con:
+  - 1× Observation WHERE mac IN (tutti i MAC degli asset) ORDER BY seen_at
+    poi group-by mac in memoria / dict asset_id → portal rows
+  - 1× aggregato FDB: MAX(last_fdb_at) GROUP BY asset_id
+→ Q_dry_run ≈ 3 (assets + obs + fdb) indipendente da N.
+
+Rischi da valutare in FASE B:
+  - memoria se observations per tutti i MAC sono enormi (oggi per-asset
+    già materializza tutte le righe MAC comunque)
+  - ordine/filtro is_portal_evidence deve restare identico
+  - test di equivalenza report dry_run pre/post prefetch
+
+STOP FASE A. Prefetch solo dopo OK esplicito.
