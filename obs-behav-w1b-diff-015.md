<!-- BLOCK-ID: OBS-BEHAV-W1B-DIFF-015 -->

# OBS-BEHAV-W1B-DIFF-015 — nomi destinazioni (ip_intel) + prune

**VERSION:** 0.10.7 · **Test:** 20 passed (test_ip_intel + test_habits)

## Cosa
- Cold start intel: offset a EOF (no backlog RAM spike)
1. Prune entrypoint: ssl*/http*/files* (no bare mode)
2. ip_intel + ingest + zeek_intel provider (dns primario, ssl:443+uid)
3. Habits dst_name da ip_intel / asset locale privato
4. AI context = pezzo successivo

## Diff

diff --git a/observatory/CHANGELOG.md b/observatory/CHANGELOG.md
index d468cc4..02d85ec 100644
--- a/observatory/CHANGELOG.md
+++ b/observatory/CHANGELOG.md
@@ -1,5 +1,60 @@
 # Changelog
 
+## 0.10.7 — 2026-07-23
+
+- **Wave 1b — nomi destinazioni osservati:** tabella `ip_intel` (DNS A/AAAA + SNI `:443` confermato via `conn.uid`); provider `zeek_intel` → `POST /api/ingest/ip-intel`; Habits riempie `dst_name` (pubblici da cache, privati da asset locale). Nessun AI context in questo pezzo.
+- **Zeek prune:** entrypoint esteso a `ssl*` / `http*` / `files*` (oltre conn/dns/dhcp); niente bare mode.
+
+## 0.10.6 — 2026-07-23
+
+- **Abitudini chassis-aware:** aggregazione per device fisico (`scope=chassis` default se ≥2 membri). Gate `resolve_asset_by_ip_at` invariato + union post-risoluzione; coverage = peggiore dei membri con motivo composto; provenienza per interfaccia (`Traffico da: eth #N · wifi #M`). Stesso quadro da primary o sibling; asset senza chassis invariato.
+
+## 0.10.5 — 2026-07-23
+
+- **Wave 1a completa — sezione «Abitudini» nel Dossier Inventario:** badge coverage (completo/parziale/sconosciuto), destinazioni con direzione out|in (Opzione A), volume 7g + sparkline ore locali (`Europe/Rome`), porte a scomparsa, stati vuoti onesti (`empty_kind`). Descrittivo; reset habits su `closePanel`.
+
+## 0.10.4 — 2026-07-23
+
+- **Bootstrap — trust dry_run prefetch:** 2 aggregati (`MIN`/`MAX` portal `seen_at` per MAC + `MAX(last_fdb_at)` per asset) prima del loop; da ~2N+1 query a ~3. Equivalenza col legacy N+1 coperta da test. Log: `mode=prefetch queries=N`.
+- Allinea in tree anche il §5 già live in **0.10.3** (backup trust selettivo: solo strutturali; refresh soli timestamp senza backup; `start_period` 180s).
+
+## 0.10.3 — 2026-07-23
+
+- **Bootstrap — backup trust selettivo:** backup solo su modifiche strutturali (`trust_level` / quarantine / proposte archiviate). I refresh di soli timestamp (`portal_*` / `presence_state`) applicano senza backup (~60s risparmiati sui boot ordinari). `BOOTSTRAP_BACKUP=always` resta scappatoia. Healthcheck api `start_period: 180s`.
+
+## 0.10.2 — 2026-07-23
+
+- **Fix perdita ora chiusa su timeout POST flow:** batch N=100 su `POST /api/ingest/flows`, retry con ack per chunk (pending resta se fail), tetto K=3 / M=3000 con log `[zeek_conn] DROP ora …`, timeout flow 120s, observations post 60s. Non drop silenzioso in `finally`.
+
+## 0.10.1 — 2026-07-23
+
+- **Wave 1a Parte 2A — `GET /api/assets/{id}/habits`:** rollup 7g gate SQL temporale (binding history, tie→escludi), coverage 3 stati da topologia, mix-aware `bytes_out`/`bytes_in`, `empty_kind`, ore UTC + `timezone: Europe/Rome`. Mirror sources hardcoded (`DEBT-MIRROR-SOURCES`). Solo API — UI Abitudini = 2B.
+
+## 0.10.0 — 2026-07-23
+
+- **Wave 1a Parte 1 — pipeline direzione flow:** `bytes_out` / `bytes_in` / `byte_layer` end-to-end (Zeek `conn.log` → aggregate → ingest → `flow_observations` → `flows_summary`). App-layer primario; fallback IP-bytes (`byte_layer=ip`); mai null→0 silenzioso. Migration Alembic `h8e4f5a6b7c8` (+ colonne idempotenti in `schema_migrations`). Storico: out/in NULL. Inizia il filone behavioural.
+
+## 0.9.12 — 2026-07-22
+
+- Attribuzione OS **chassis-aware**: se nmap risponde col MAC di un sibling dello stesso chassis (gate: `origin` ∈ {auto, manuale}, ≥1 di C1/C2/C3, no X1), l’OS va all’**owner** del MAC + mirror sul target dello scan; stats `os_attributed_via_chassis_sibling`. Nessun merge identity; `chassis_grouping` non toccato.
+
+## 0.9.11 — 2026-07-22
+
+- Osservabilità attribuzione OS su MAC mismatch: `fingerprint_stats.mac_mismatches` (+ `os_discarded_mac_mismatch` / messaggio), `scan_run.message` esplicito, Dossier label «OS non attribuito (MAC discordante — vedi dettagli)» con tooltip. Nessuna fusion identity, nessun cambio worker.
+
+## 0.9.10 — 2026-07-22
+
+- **DEBT-COLLECTOR-PRIVILEGED risolto per rimozione:** nmap **in-image** nel collector (`apt install nmap`); `nmap_scan.py` esegue il binario locale (no `docker run` / no `instrumentisto/nmap`).
+- Compose collector: **drop** `/var/run/docker.sock`, **drop** `privileged: true` — restano solo `NET_RAW` + `NET_ADMIN` (pattern Zeek).
+- `SCANNER_PRIVILEGED` resta **false** al deploy finché staging non conferma ARP (`-sn` con MAC) e un `os_fingerprint` mirato con flag true. Accensione OS = solo dopo quella verifica.
+
+## 0.9.9 — 2026-07-22
+
+- Dossier «Chi sei»: parser identità pulito (`GET /api/assets/{id}/identity`), OUI resident (`oui_vendors` + `scripts/oui_refresh.py` manuale), sezione UI nel pannello Inventario con ignoti dichiarati.
+- Opt-out OS per-asset (`meta.os_fingerprint_opt_out`, default per tipo iot/domotica/media — **zero brand** hardcoded); toggle «Proteggi da scansione OS».
+- Semaforo `GET /api/system/scan-readiness` (green/yellow/red + motivo) sul bottone «Rileva OS ora».
+- OS detection **canale spento**: `SCANNER_PRIVILEGED=false`; `/scan-os` → «OS non disponibile, scanner non privilegiato». Accensione OS = cantiere 0.9.10 (`DEBT-COLLECTOR-PRIVILEGED`: nmap-in-image, drop docker.sock/privileged).
+
 ## 0.9.8 — 2026-07-22
 
 - LEVA B SQLite lock: `reconcile_all_asset_presence` solo su `/fdb-reconcile` (collector `reconcile_presence=False` su nmap/ssdp/printer/fritz/scan-batch); anti-burst `PRESENCE_RECONCILE_MIN_INTERVAL_SEC=600` (~1–2 pass/15'). Log `[fdb-reconcile] presence pass|coalesced`.
diff --git a/observatory/VERSION b/observatory/VERSION
index e3e1807..2d993c4 100644
--- a/observatory/VERSION
+++ b/observatory/VERSION
@@ -1 +1 @@
-0.9.8
+0.10.7
diff --git a/observatory/api/app/models.py b/observatory/api/app/models.py
index 9fbe40b..16d16ac 100644
--- a/observatory/api/app/models.py
+++ b/observatory/api/app/models.py
@@ -176,6 +176,18 @@ class FingerprintFact(Base):
     asset: Mapped[Asset] = relationship(back_populates="fingerprint_facts")
 
 
+class OuiVendor(Base):
+    """Resident OUI→vendor (subset of IEEE for MAC prefixes seen on the LAN)."""
+
+    __tablename__ = "oui_vendors"
+
+    id: Mapped[int] = mapped_column(Integer, primary_key=True)
+    prefix: Mapped[str] = mapped_column(String(8), unique=True, index=True)  # AA:BB:CC
+    vendor: Mapped[str] = mapped_column(String(128), default="")
+    source: Mapped[str] = mapped_column(String(32), default="ieee")  # ieee|seed|manual
+    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
+
+
 class Switch(Base):
     __tablename__ = "switches"
 
@@ -814,7 +826,28 @@ class FlowObservation(Base):
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
+
+
+class IpIntel(Base):
+    """Observed public IP → name (DNS A/AAAA or TLS SNI). Wave 1b.
+
+    AI context columns are a later wave — not here.
+    """
+
+    __tablename__ = "ip_intel"
+    __table_args__ = (Index("ix_ip_intel_last_seen", "last_seen"),)
+
+    ip: Mapped[str] = mapped_column(String(45), primary_key=True)
+    name: Mapped[str] = mapped_column(String(255), default="")
+    source: Mapped[str] = mapped_column(String(16), default="")  # dns|ssl
+    first_seen: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
+    last_seen: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
+    confidence: Mapped[float] = mapped_column(Float, default=0.0)
diff --git a/observatory/api/app/routers/evolution.py b/observatory/api/app/routers/evolution.py
index 0c5b5a1..bd1225a 100644
--- a/observatory/api/app/routers/evolution.py
+++ b/observatory/api/app/routers/evolution.py
@@ -19,6 +19,7 @@ from app.services.detectors import DETECTORS, run_detectors
 from app.services.drift import detect_drift
 from app.services.findings import finding_from_drifts, serialize_finding
 from app.services.flows_summary import flow_summary
+from app.services.ip_intel import upsert_ip_intel_batch
 from app.services.notifications import dispatch_notification
 from app.services.snapshots import confirm_baseline, snapshot_asset
 
@@ -31,6 +32,24 @@ class FindingUpdate(BaseModel):
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
@@ -38,6 +57,9 @@ class FlowIn(BaseModel):
     dst_port: int = 0
     proto: str = "tcp"
     bytes: int = 0
+    bytes_out: Optional[int] = None
+    bytes_in: Optional[int] = None
+    byte_layer: Optional[str] = None
     dst_asn: str = ""
     dst_country: str = ""
     observed_at: Optional[datetime] = None
@@ -224,6 +246,37 @@ def ingest_flow(
     _check_internal(x_obs_token, settings)
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
+    x_obs_token: Optional[str] = Header(default=None),
+):
+    """Batch flow ingest (one HTTP round-trip for many buckets)."""
+    _check_internal(x_obs_token, settings)
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
@@ -233,6 +286,9 @@ def ingest_flow(
     existing = db.scalar(select(FlowObservation).where(FlowObservation.dedup_key == dedup))
     if existing:
         existing.bytes = int(existing.bytes or 0) + int(body.bytes or 0)
+        existing.bytes_out = _add_optional_flow_int(existing.bytes_out, body.bytes_out)
+        existing.bytes_in = _add_optional_flow_int(existing.bytes_in, body.bytes_in)
+        existing.byte_layer = _merge_byte_layer(existing.byte_layer, body.byte_layer)
         from app.services.watch import note_traffic_for_ips
 
         note_traffic_for_ips(
@@ -243,7 +299,6 @@ def ingest_flow(
             detail="Flow ingest: traffico su IP watched",
             extra={"sensor_id": body.sensor_id, "proto": body.proto, "dst_port": body.dst_port},
         )
-        db.commit()
         return {"ok": True, "created": False, "id": existing.id}
     row = FlowObservation(
         dedup_key=dedup,
@@ -253,12 +308,16 @@ def ingest_flow(
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
@@ -269,10 +328,52 @@ def ingest_flow(
         detail="Flow ingest: traffico su IP watched",
         extra={"sensor_id": body.sensor_id, "proto": body.proto, "dst_port": body.dst_port},
     )
-    db.commit()
     return {"ok": True, "created": True, "id": row.id}
 
 
+class IpIntelItemIn(BaseModel):
+    ip: str
+    name: str
+    source: str = Field(description="dns|ssl")
+    confidence: float = 0.8
+    seen_at: Optional[datetime] = None
+
+
+class IpIntelBatchIn(BaseModel):
+    items: list[IpIntelItemIn] = Field(default_factory=list)
+
+
+@router.post("/ingest/ip-intel")
+def ingest_ip_intel(
+    body: IpIntelBatchIn,
+    db: Session = Depends(get_db),
+    settings: Settings = Depends(get_settings),
+    x_obs_token: Optional[str] = Header(default=None),
+):
+    """Batch public IP→name from Zeek dns/ssl (feature-flagged with flow ingest)."""
+    _check_internal(x_obs_token, settings)
+    if not settings.flow_ingest_enabled:
+        raise HTTPException(503, "flow ingest disabilitato (FLOW_INGEST_ENABLED=false)")
+    items = list(body.items or [])
+    if len(items) > 500:
+        raise HTTPException(400, "max 500 items per batch")
+    stats = upsert_ip_intel_batch(
+        db,
+        [
+            {
+                "ip": it.ip,
+                "name": it.name,
+                "source": it.source,
+                "confidence": it.confidence,
+                "seen_at": it.seen_at,
+            }
+            for it in items
+        ],
+    )
+    db.commit()
+    return {"ok": True, **stats}
+
+
 @router.post("/notifications/test")
 def test_notification(
     request: Request,
diff --git a/observatory/collector/collector/main.py b/observatory/collector/collector/main.py
index 214978a..400690b 100644
--- a/observatory/collector/collector/main.py
+++ b/observatory/collector/collector/main.py
@@ -25,6 +25,7 @@ from collector.adapters.printer import discover_printers_mdns, enrich_printer_ho
 from collector.adapters.asustor_snmp import collect_asustor_snapshot, evaluate_health
 from collector.adapters.snmp_lldp import collect_switch_snapshot, group_fdb_by_port
 from collector.adapters.zeek_conn import run_zeek_provider_cycle
+from collector.adapters.zeek_intel import run_zeek_intel_cycle
 from collector.config import Settings
 from collector.scan_jobs import process_scan_queue
 
@@ -501,7 +502,7 @@ def _run_retention(settings: Settings) -> None:
 
 
 def _run_zeek_provider(settings: Settings) -> None:
-    """Optional SPAN conn.log → hourly POST /api/ingest/flow (flag off by default)."""
+    """Optional SPAN conn.log → hourly POST /api/ingest/flows (flag off by default)."""
     if not getattr(settings, "zeek_provider_enabled", False):
         return
     api = settings.api_internal.rstrip("/")
@@ -511,23 +512,24 @@ def _run_zeek_provider(settings: Settings) -> None:
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
@@ -538,6 +540,27 @@ def _run_zeek_provider(settings: Settings) -> None:
     except Exception as exc:  # noqa: BLE001
         print(f"[collector] zeek_conn err: {exc}")
 
+    def _post_intel(items: list[dict]) -> None:
+        with httpx.Client(timeout=60.0) as client:
+            response = client.post(
+                f"{api}/api/ingest/ip-intel",
+                headers=headers(settings),
+                json={"items": items},
+            )
+            if response.status_code >= 400:
+                raise RuntimeError(
+                    f"ip-intel ingest {response.status_code}: {response.text[:200]}"
+                )
+
+    try:
+        intel = run_zeek_intel_cycle(log_dir=log_dir, post_intel=_post_intel)
+        print(
+            f"[collector] zeek_intel dns={intel.get('dns_rows')} "
+            f"ssl={intel.get('ssl_rows')} posted={intel.get('posted')}"
+        )
+    except Exception as exc:  # noqa: BLE001
+        print(f"[collector] zeek_intel err: {exc}")
+
 
 def configure_scheduler(sched: BlockingScheduler, settings: Settings) -> None:
     sched.add_job(
diff --git a/observatory/docs/OPTIONAL_SENSORS.md b/observatory/docs/OPTIONAL_SENSORS.md
index 39d8925..2e49d02 100644
--- a/observatory/docs/OPTIONAL_SENSORS.md
+++ b/observatory/docs/OPTIONAL_SENSORS.md
@@ -59,14 +59,12 @@ intervallo `RETENTION_INTERVAL_SEC`, tipicamente orario — non solo nightly).
 ### Retention locale `data/zeek/` (entrypoint)
 
 Il loop orario in `zeek/entrypoint.sh` cancella file con mtime >2 giorni
-per i pattern `conn*`, `dns*`, `dhcp*` (log correnti e ruotati).
-
-Scelta: **estendere il prune**, non `-b` (bare). La policy
-`local.zeek` carica solo `base/protocols/conn`, ma su disco possono
-restare `dns.log` / `dhcp.log` da run precedenti o da dipendenze Zeek;
-il prune li copre senza cambiare il comportamento del binario. Bare
-mode (`zeek -b`) stringerebbe a “solo conn” in modo letterale — da
-rivalutare solo se la disk budget lo impone.
+per i pattern `conn*`, `dns*`, `dhcp*`, `ssl*`, `http*`, `files*`
+(log correnti e ruotati).
+
+Scelta: **estendere il prune**, non `-b` (bare). Senza bare Zeek scrive
+anche `ssl`/`dns`/`http` (init-default) — servono a `ip_intel` (Wave 1b).
+Bare mode stringerebbe a “solo conn” e toglierebbe i nomi destinazione.
 
 ### Stima righe/giorno (ordine di grandezza)
 
diff --git a/observatory/web/package.json b/observatory/web/package.json
index 06a97cf..4cfc988 100644
--- a/observatory/web/package.json
+++ b/observatory/web/package.json
@@ -1,7 +1,7 @@
 {
   "name": "lan-observatory-web",
   "private": true,
-  "version": "0.9.8",
+  "version": "0.10.7",
   "type": "module",
   "scripts": {
     "dev": "vite",
diff --git a/observatory/zeek/entrypoint.sh b/observatory/zeek/entrypoint.sh
index efc95a6..9d7ebbc 100755
--- a/observatory/zeek/entrypoint.sh
+++ b/observatory/zeek/entrypoint.sh
@@ -2,11 +2,10 @@
 # Zeek SPAN sink — AF_PACKET on ZEEK_IFACE, logs under /zeek-logs.
 # Retention locale 48h (mtime +2). ulimit nofile must be set by compose.
 #
-# Prune: conn* + dns* + dhcp* (rotated). Policy locale carica solo conn, ma
-# dns.log/dhcp.log possono restare da run precedenti o da dipendenze Zeek —
-# li ruotiamo uguale. Non usiamo -b (bare): stringerebbe a solo conn a costo
-# di cambiare il comportamento del binario; rivalutare se la disk budget
-# lo richiede (vedi docs/OPTIONAL_SENSORS.md).
+# Prune: conn* + dns* + dhcp* + ssl* + http* + files* (rotated).
+# Zeek senza -b scrive anche ssl/dns/http/files (init-default); non passare
+# a bare mode — dns.log e ssl.log servono a ip_intel (Wave 1b).
+# Vedi docs/OPTIONAL_SENSORS.md.
 set -eu
 
 IFACE="${ZEEK_IFACE:-eth1}"
@@ -16,13 +15,16 @@ POLICY="${ZEEK_POLICY:-/opt/observatory/zeek/local.zeek}"
 mkdir -p "$LOGDIR"
 cd "$LOGDIR"
 
-# Background prune: keep ~48h of rotated SPAN logs (conn + side dns/dhcp).
+# Background prune: keep ~48h of rotated SPAN logs (conn + naming + side).
 (
   while true; do
     find "$LOGDIR" -type f \( \
       -name 'conn*.log' -o -name 'conn.*.log*' \
       -o -name 'dns*.log' -o -name 'dns.*.log*' \
       -o -name 'dhcp*.log' -o -name 'dhcp.*.log*' \
+      -o -name 'ssl*.log' -o -name 'ssl.*.log*' \
+      -o -name 'http*.log' -o -name 'http.*.log*' \
+      -o -name 'files*.log' -o -name 'files.*.log*' \
     \) -mtime +2 -delete 2>/dev/null || true
     sleep 3600
   done

=== NEW FILE: api/app/alembic/versions/i9f6a7b8c9d0_ip_intel.py ===
"""ip_intel table for observed destination names (Wave 1b)

Revision ID: i9f6a7b8c9d0
Revises: h8e4f5a6b7c8
Create Date: 2026-07-23 14:00:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "i9f6a7b8c9d0"
down_revision = "h8e4f5a6b7c8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ip_intel",
        sa.Column("ip", sa.String(length=45), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("source", sa.String(length=16), nullable=False, server_default=""),
        sa.Column("first_seen", sa.DateTime(), nullable=False),
        sa.Column("last_seen", sa.DateTime(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0"),
    )
    op.create_index("ix_ip_intel_last_seen", "ip_intel", ["last_seen"])


def downgrade() -> None:
    op.drop_index("ix_ip_intel_last_seen", table_name="ip_intel")
    op.drop_table("ip_intel")

=== NEW FILE: api/app/services/ip_intel.py ===
"""Observed public IP → hostname (DNS / TLS SNI). Wave 1b naming.

No AI context here — later wave adds columns on the same table.
"""

from __future__ import annotations

import ipaddress
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Asset, Interface, IpAddress, IpIntel

CONF_DNS = 0.80
CONF_SSL = 0.95
SOURCE_DNS = "dns"
SOURCE_SSL = "ssl"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def is_public_ip(ip: str) -> bool:
    """True for globally routable addresses — never RFC1918 / link-local / etc."""
    try:
        addr = ipaddress.ip_address((ip or "").strip())
    except ValueError:
        return False
    return not (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_multicast
        or addr.is_reserved
        or addr.is_unspecified
    )


def normalize_hostname(name: str) -> str:
    text = (name or "").strip().rstrip(".").lower()
    if not text or len(text) > 253:
        return ""
    # Reject obvious garbage / IP literals as "names".
    try:
        ipaddress.ip_address(text)
        return ""
    except ValueError:
        pass
    return text[:255]


def upsert_ip_intel(
    db: Session,
    *,
    ip: str,
    name: str,
    source: str,
    confidence: float,
    seen_at: Optional[datetime] = None,
) -> dict[str, Any]:
    """Insert or refresh one public IP name. Skips private / invalid. Caller commits."""
    ip = (ip or "").strip()
    name = normalize_hostname(name)
    source = (source or "").strip().lower()
    if not ip or not name or source not in {SOURCE_DNS, SOURCE_SSL}:
        return {"ok": False, "skipped": "invalid"}
    if not is_public_ip(ip):
        return {"ok": False, "skipped": "private"}
    at = seen_at or _utc_now()
    conf = max(0.0, min(1.0, float(confidence)))

    row = db.get(IpIntel, ip)
    if row is None:
        db.add(
            IpIntel(
                ip=ip,
                name=name,
                source=source,
                first_seen=at,
                last_seen=at,
                confidence=conf,
            )
        )
        return {"ok": True, "created": True, "ip": ip}

    if at > row.last_seen:
        row.last_seen = at
    # Prefer higher confidence; SSL wins ties (CDN-quality SNI).
    replace = conf > float(row.confidence or 0)
    if not replace and conf == float(row.confidence or 0):
        replace = source == SOURCE_SSL and row.source != SOURCE_SSL
    if replace or not (row.name or "").strip():
        row.name = name
        row.source = source
        row.confidence = conf
    return {"ok": True, "created": False, "ip": ip}


def upsert_ip_intel_batch(
    db: Session,
    items: Iterable[dict[str, Any]],
) -> dict[str, int]:
    """Upsert many records. Caller commits."""
    created = 0
    updated = 0
    skipped = 0
    for raw in items:
        seen = raw.get("seen_at")
        if isinstance(seen, str) and seen:
            try:
                text = seen[:-1] + "+00:00" if seen.endswith("Z") else seen
                seen_dt = datetime.fromisoformat(text)
                if seen_dt.tzinfo is not None:
                    seen_dt = seen_dt.replace(tzinfo=None) - (
                        seen_dt.utcoffset() or timedelta()
                    )
            except ValueError:
                seen_dt = None
        elif isinstance(seen, datetime):
            seen_dt = seen.replace(tzinfo=None) if seen.tzinfo else seen
        else:
            seen_dt = None
        result = upsert_ip_intel(
            db,
            ip=str(raw.get("ip") or ""),
            name=str(raw.get("name") or ""),
            source=str(raw.get("source") or ""),
            confidence=float(raw.get("confidence") or 0),
            seen_at=seen_dt,
        )
        if not result.get("ok"):
            skipped += 1
        elif result.get("created"):
            created += 1
        else:
            updated += 1
    return {"created": created, "updated": updated, "skipped": skipped}


def names_for_ips(db: Session, ips: Iterable[str]) -> dict[str, str]:
    """Map public IPs → observed name from ip_intel."""
    wanted = sorted({(ip or "").strip() for ip in ips if is_public_ip(ip or "")})
    if not wanted:
        return {}
    rows = db.scalars(select(IpIntel).where(IpIntel.ip.in_(wanted))).all()
    return {row.ip: row.name for row in rows if (row.name or "").strip()}


def local_asset_names_for_ips(db: Session, ips: Iterable[str]) -> dict[str, str]:
    """Private / non-public IPs → current asset display name if uniquely bound."""
    wanted = sorted(
        {(ip or "").strip() for ip in ips if (ip or "").strip() and not is_public_ip(ip or "")}
    )
    if not wanted:
        return {}
    rows = db.execute(
        select(IpAddress.ip, Asset.name, Asset.id)
        .join(Interface, Interface.id == IpAddress.interface_id)
        .join(Asset, Asset.id == Interface.asset_id)
        .where(IpAddress.ip.in_(wanted), IpAddress.is_current.is_(True))
    ).all()
    by_ip: dict[str, set[str]] = {}
    for ip, name, _aid in rows:
        label = (name or "").strip()
        if not label:
            continue
        by_ip.setdefault(str(ip), set()).add(label)
    return {ip: next(iter(names)) for ip, names in by_ip.items() if len(names) == 1}


def enrich_destination_names(db: Session, destinations: list[dict[str, Any]]) -> None:
    """Fill dst_name in-place: ip_intel for public, asset name for private."""
    if not destinations:
        return
    ips = [str(d.get("dst_ip") or "") for d in destinations]
    public_names = names_for_ips(db, ips)
    local_names = local_asset_names_for_ips(db, ips)
    for dest in destinations:
        ip = str(dest.get("dst_ip") or "").strip()
        if not ip:
            continue
        if is_public_ip(ip):
            dest["dst_name"] = public_names.get(ip)
        else:
            dest["dst_name"] = local_names.get(ip)

=== NEW FILE: collector/collector/adapters/zeek_intel.py ===
"""Zeek dns.log + ssl.log → public IP names → POST /api/ingest/ip-intel.

DNS A/AAAA answers are primary coverage; TLS SNI on :443 confirmed via
conn.uid is higher-confidence (CDN multi-tenant). Private IPs never emitted.
"""

from __future__ import annotations

import ipaddress
import json
from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Optional

STATE_NAME = "zeek_intel_state.json"
UID_CACHE_MAX = 30_000
CONF_DNS = 0.80
CONF_SSL = 0.95
INTEL_BATCH_SIZE = 200


def _utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def parse_ts(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return datetime.utcfromtimestamp(float(value))
    text = str(value).strip()
    if not text:
        return None
    try:
        return datetime.utcfromtimestamp(float(text))
    except ValueError:
        pass
    try:
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None) - (dt.utcoffset() or timedelta())
    return dt


def is_public_ip(ip: str) -> bool:
    try:
        addr = ipaddress.ip_address((ip or "").strip())
    except ValueError:
        return False
    return not (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_multicast
        or addr.is_reserved
        or addr.is_unspecified
    )


def normalize_hostname(name: str) -> str:
    text = (name or "").strip().rstrip(".").lower()
    if not text or len(text) > 253:
        return ""
    try:
        ipaddress.ip_address(text)
        return ""
    except ValueError:
        pass
    return text[:255]


def load_state(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"offsets": {}, "uid_cache": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"offsets": {}, "uid_cache": []}
    if not isinstance(data, dict):
        return {"offsets": {}, "uid_cache": []}
    data.setdefault("offsets", {})
    data.setdefault("uid_cache", [])
    return data


def save_state(path: Path, state: dict[str, Any], *, log_dir: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    offsets = dict(state.get("offsets") or {})
    offsets = {k: v for k, v in offsets.items() if (log_dir / k).is_file()}
    # Persist a tail of uid→resp for ssl confirmation across cycles.
    uid_cache = list(state.get("uid_cache") or [])[-UID_CACHE_MAX:]
    payload = {
        "offsets": offsets,
        "uid_cache": uid_cache,
        "last_cycle_at": state.get("last_cycle_at"),
        "last_stats": dict(state.get("last_stats") or {}),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _iter_new_json_lines(
    log_dir: Path,
    offsets: dict[str, int],
    prefixes: tuple[str, ...],
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    rows: list[dict[str, Any]] = []
    new_offsets = dict(offsets)
    if not log_dir.is_dir():
        return rows, new_offsets
    ordered: list[Path] = []
    seen: set[Path] = set()
    for prefix in prefixes:
        for path in sorted(log_dir.glob(f"{prefix}*")):
            if not path.is_file() or path in seen:
                continue
            if path.name.endswith(".json") or "state" in path.name:
                continue
            seen.add(path)
            ordered.append(path)
    for path in ordered:
        key = path.name
        start = int(new_offsets.get(key) or 0)
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size < start:
            start = 0
        try:
            with path.open("r", encoding="utf-8", errors="ignore") as fh:
                fh.seek(start)
                for line in fh:
                    text = line.strip()
                    if not text or text.startswith("#"):
                        continue
                    try:
                        row = json.loads(text)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(row, dict):
                        rows.append(row)
                new_offsets[key] = fh.tell()
        except OSError:
            continue
    return rows, new_offsets


def extract_dns_pairs(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """A/AAAA answers → public answer_ip → query name."""
    out: list[dict[str, Any]] = []
    for row in rows:
        qtype = str(row.get("qtype_name") or "").upper()
        if qtype not in {"A", "AAAA"}:
            continue
        query = normalize_hostname(str(row.get("query") or ""))
        if not query:
            continue
        answers = row.get("answers") or []
        if not isinstance(answers, list):
            continue
        ts = parse_ts(row.get("ts"))
        for ans in answers:
            ip = str(ans or "").strip()
            if not is_public_ip(ip):
                continue
            out.append(
                {
                    "ip": ip,
                    "name": query,
                    "source": "dns",
                    "confidence": CONF_DNS,
                    "seen_at": (ts or _utc_now()).isoformat() + "Z",
                }
            )
    return out


def _uid_map_from_cache(entries: list[Any]) -> OrderedDict[str, str]:
    """uid → resp_ip (ordered for LRU trim)."""
    mapping: OrderedDict[str, str] = OrderedDict()
    for item in entries:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            uid, resp = str(item[0]), str(item[1])
            if uid and resp:
                mapping[uid] = resp
                mapping.move_to_end(uid)
        elif isinstance(item, dict):
            uid = str(item.get("uid") or "")
            resp = str(item.get("resp") or "")
            if uid and resp:
                mapping[uid] = resp
                mapping.move_to_end(uid)
    return mapping


def ingest_conn_uids(
    rows: Iterable[dict[str, Any]],
    uid_map: OrderedDict[str, str],
) -> None:
    for row in rows:
        uid = str(row.get("uid") or "").strip()
        resp = str(row.get("id.resp_h") or "").strip()
        if not uid or not resp:
            continue
        uid_map[uid] = resp
        uid_map.move_to_end(uid)
        while len(uid_map) > UID_CACHE_MAX:
            uid_map.popitem(last=False)


def extract_ssl_pairs(
    rows: Iterable[dict[str, Any]],
    uid_map: OrderedDict[str, str],
) -> list[dict[str, Any]]:
    """SNI on :443 confirmed when ssl.uid maps to same resp_h in recent conn."""
    out: list[dict[str, Any]] = []
    for row in rows:
        try:
            rport = int(row.get("id.resp_p") or 0)
        except (TypeError, ValueError):
            rport = 0
        if rport != 443:
            continue
        sni = normalize_hostname(str(row.get("server_name") or ""))
        if not sni:
            continue
        uid = str(row.get("uid") or "").strip()
        resp = str(row.get("id.resp_h") or "").strip()
        if not uid or not resp:
            continue
        confirmed = uid_map.get(uid)
        if confirmed is None or confirmed != resp:
            continue
        if not is_public_ip(resp):
            continue
        ts = parse_ts(row.get("ts"))
        out.append(
            {
                "ip": resp,
                "name": sni,
                "source": "ssl",
                "confidence": CONF_SSL,
                "seen_at": (ts or _utc_now()).isoformat() + "Z",
            }
        )
    return out


def _collapse_best(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One record per IP: highest confidence; SSL wins ties."""
    best: dict[str, dict[str, Any]] = {}
    for item in items:
        ip = item["ip"]
        prev = best.get(ip)
        if prev is None:
            best[ip] = item
            continue
        if float(item["confidence"]) > float(prev["confidence"]):
            best[ip] = item
        elif float(item["confidence"]) == float(prev["confidence"]) and item[
            "source"
        ] == "ssl" and prev["source"] != "ssl":
            best[ip] = item
        else:
            # refresh seen_at if newer
            if str(item.get("seen_at") or "") > str(prev.get("seen_at") or ""):
                prev["seen_at"] = item["seen_at"]
    return list(best.values())


def run_zeek_intel_cycle(
    *,
    log_dir: Path,
    post_intel: Callable[[list[dict[str, Any]]], Any],
    now: Optional[datetime] = None,
    batch_size: int = INTEL_BATCH_SIZE,
) -> dict[str, int]:
    """Read new dns/ssl/conn lines; POST collapsed public IP names."""
    now = now or _utc_now()
    state_path = log_dir / STATE_NAME
    state = load_state(state_path)
    offsets = dict(state.get("offsets") or {})
    uid_map = _uid_map_from_cache(list(state.get("uid_cache") or []))

    conn_rows, offsets = _iter_new_json_lines(log_dir, offsets, ("conn",))
    ingest_conn_uids(conn_rows, uid_map)

    dns_rows, offsets = _iter_new_json_lines(log_dir, offsets, ("dns",))
    ssl_rows, offsets = _iter_new_json_lines(log_dir, offsets, ("ssl",))

    pairs = extract_dns_pairs(dns_rows) + extract_ssl_pairs(ssl_rows, uid_map)
    collapsed = _collapse_best(pairs)

    posted = 0
    for i in range(0, len(collapsed), max(1, batch_size)):
        chunk = collapsed[i : i + batch_size]
        if chunk:
            post_intel(chunk)
            posted += len(chunk)

    state["offsets"] = offsets
    state["uid_cache"] = [[uid, resp] for uid, resp in uid_map.items()]
    state["last_cycle_at"] = now.isoformat() + "Z"
    state["last_stats"] = {
        "conn_rows": len(conn_rows),
        "dns_rows": len(dns_rows),
        "ssl_rows": len(ssl_rows),
        "pairs": len(pairs),
        "posted": posted,
    }
    save_state(state_path, state, log_dir=log_dir)
    return {
        "conn_rows": len(conn_rows),
        "dns_rows": len(dns_rows),
        "ssl_rows": len(ssl_rows),
        "pairs": len(pairs),
        "posted": posted,
    }

=== NEW FILE: tests/test_ip_intel.py ===
"""Wave 1b — ip_intel from Zeek dns/ssl + habits dst_name."""

from __future__ import annotations

import json
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "api"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "collector"))

from app.db import Base
from app.models import Asset, FlowObservation, Interface, IpAddress, IpIntel
from app.services.habits import asset_habits
from app.services.identity import upsert_observation_asset
from app.services.ip_intel import (
    enrich_destination_names,
    is_public_ip,
    upsert_ip_intel,
    upsert_ip_intel_batch,
)
from collector.adapters.zeek_intel import (
    extract_dns_pairs,
    extract_ssl_pairs,
    ingest_conn_uids,
    run_zeek_intel_cycle,
)
from collections import OrderedDict


@pytest.fixture()
def db(tmp_path):
    eng = create_engine(f"sqlite:///{tmp_path / 'intel.db'}")
    Base.metadata.create_all(eng)
    Session = sessionmaker(bind=eng)
    session = Session()
    yield session
    session.close()


def test_is_public_ip_rejects_private():
    assert is_public_ip("8.8.8.8")
    assert is_public_ip("1.1.1.1")
    assert not is_public_ip("192.168.1.10")
    assert not is_public_ip("10.0.0.1")
    assert not is_public_ip("172.16.5.5")
    assert not is_public_ip("127.0.0.1")
    assert not is_public_ip("not-an-ip")


def test_upsert_skips_private(db):
    result = upsert_ip_intel(
        db,
        ip="192.168.1.1",
        name="gateway.lan",
        source="dns",
        confidence=0.9,
    )
    assert result["skipped"] == "private"
    assert db.get(IpIntel, "192.168.1.1") is None


def test_upsert_ssl_beats_dns(db):
    now = datetime(2026, 7, 23, 12, 0, 0)
    upsert_ip_intel(
        db,
        ip="93.184.216.34",
        name="cdn.example.net",
        source="dns",
        confidence=0.8,
        seen_at=now,
    )
    upsert_ip_intel(
        db,
        ip="93.184.216.34",
        name="www.example.com",
        source="ssl",
        confidence=0.95,
        seen_at=now + timedelta(minutes=1),
    )
    db.commit()
    row = db.get(IpIntel, "93.184.216.34")
    assert row is not None
    assert row.name == "www.example.com"
    assert row.source == "ssl"
    assert row.confidence == pytest.approx(0.95)


def test_extract_dns_pairs_public_only():
    rows = [
        {
            "qtype_name": "A",
            "query": "api.example.com",
            "answers": ["93.184.216.34", "192.168.1.50"],
            "ts": 1784804400.0,
        },
        {"qtype_name": "TXT", "query": "x", "answers": ["v=spf1"], "ts": 1784804400.0},
    ]
    pairs = extract_dns_pairs(rows)
    assert len(pairs) == 1
    assert pairs[0]["ip"] == "93.184.216.34"
    assert pairs[0]["name"] == "api.example.com"
    assert pairs[0]["source"] == "dns"


def test_extract_ssl_requires_uid_confirm():
    uid_map: OrderedDict[str, str] = OrderedDict()
    ingest_conn_uids(
        [{"uid": "Cu1", "id.resp_h": "93.184.216.34", "id.resp_p": 443}],
        uid_map,
    )
    rows = [
        {
            "uid": "Cu1",
            "id.resp_h": "93.184.216.34",
            "id.resp_p": 443,
            "server_name": "www.example.com",
            "ts": 1784804400.0,
        },
        {
            "uid": "missing",
            "id.resp_h": "1.2.3.4",
            "id.resp_p": 443,
            "server_name": "nope.example",
            "ts": 1784804400.0,
        },
        {
            "uid": "Cu1",
            "id.resp_h": "93.184.216.34",
            "id.resp_p": 8443,
            "server_name": "other.example.com",
            "ts": 1784804400.0,
        },
    ]
    pairs = extract_ssl_pairs(rows, uid_map)
    assert len(pairs) == 1
    assert pairs[0]["name"] == "www.example.com"
    assert pairs[0]["source"] == "ssl"


def test_zeek_intel_cycle_posts(tmp_path):
    log_dir = tmp_path / "zeek"
    log_dir.mkdir()
    (log_dir / "conn.log").write_text(
        json.dumps(
            {
                "uid": "Cu1",
                "id.orig_h": "192.168.1.10",
                "id.resp_h": "93.184.216.34",
                "id.resp_p": 443,
                "proto": "tcp",
                "ts": 1784804400.0,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (log_dir / "dns.log").write_text(
        json.dumps(
            {
                "qtype_name": "A",
                "query": "cdn.example.net.",
                "answers": ["93.184.216.34"],
                "ts": 1784804400.0,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (log_dir / "ssl.log").write_text(
        json.dumps(
            {
                "uid": "Cu1",
                "id.resp_h": "93.184.216.34",
                "id.resp_p": 443,
                "server_name": "www.example.com",
                "ts": 1784804401.0,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    posted: list[dict] = []

    def _post(items):
        posted.extend(items)

    stats = run_zeek_intel_cycle(log_dir=log_dir, post_intel=_post)
    assert stats["posted"] == 1
    assert posted[0]["ip"] == "93.184.216.34"
    # SSL wins over DNS in collapse
    assert posted[0]["name"] == "www.example.com"
    assert posted[0]["source"] == "ssl"
    # second cycle: no new lines
    posted.clear()
    stats2 = run_zeek_intel_cycle(log_dir=log_dir, post_intel=_post)
    assert stats2["posted"] == 0


def test_habits_dst_name_from_ip_intel(db):
    now = datetime(2026, 7, 23, 12, 0, 0)
    asset = upsert_observation_asset(
        db,
        mac="aa:bb:cc:dd:ee:01",
        ip="192.168.1.50",
        seen_at=now - timedelta(days=1),
        source="test",
    )
    db.flush()
    for iface in asset.interfaces:
        for addr in iface.addresses:
            addr.first_seen = now - timedelta(days=1)
            addr.is_current = True
    db.add(
        FlowObservation(
            dedup_key=str(uuid.uuid4()),
            sensor_id="zeek-span",
            src_ip="192.168.1.50",
            dst_ip="93.184.216.34",
            dst_port=443,
            proto="tcp",
            bytes=100,
            bytes_out=40,
            bytes_in=60,
            observed_at=now,
        )
    )
    db.add(
        FlowObservation(
            dedup_key=str(uuid.uuid4()),
            sensor_id="zeek-span",
            src_ip="192.168.1.50",
            dst_ip="192.168.1.1",
            dst_port=53,
            proto="udp",
            bytes=50,
            observed_at=now,
        )
    )
    gw = upsert_observation_asset(
        db,
        mac="aa:bb:cc:dd:ee:99",
        ip="192.168.1.1",
        seen_at=now - timedelta(days=1),
        source="test",
        hostname="FritzBox",
    )
    db.flush()
    gw.name = "FritzBox"
    for iface in gw.interfaces:
        for addr in iface.addresses:
            addr.first_seen = now - timedelta(days=1)
            addr.is_current = True
    upsert_ip_intel(
        db,
        ip="93.184.216.34",
        name="www.example.com",
        source="ssl",
        confidence=0.95,
        seen_at=now,
    )
    db.commit()

    habits = asset_habits(db, asset.id, days=7, now=now + timedelta(hours=1))
    assert habits is not None
    by_ip = {d["dst_ip"]: d for d in habits["destinations"]}
    assert by_ip["93.184.216.34"]["dst_name"] == "www.example.com"
    assert by_ip["192.168.1.1"]["dst_name"] == "FritzBox"


def test_enrich_destination_names_public_only_table(db):
    dests = [
        {"dst_ip": "8.8.8.8", "dst_name": None},
        {"dst_ip": "192.168.2.10", "dst_name": None},
    ]
    upsert_ip_intel_batch(
        db,
        [
            {
                "ip": "8.8.8.8",
                "name": "dns.google",
                "source": "dns",
                "confidence": 0.8,
            },
            {
                "ip": "192.168.2.10",
                "name": "should-skip.lan",
                "source": "dns",
                "confidence": 0.9,
            },
        ],
    )
    db.commit()
    enrich_destination_names(db, dests)
    assert dests[0]["dst_name"] == "dns.google"
    assert dests[1]["dst_name"] is None  # private, no unique asset
